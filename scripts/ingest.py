"""Ingestion CLI implementing /ingest semantics (contract 8.2).

Loads and validates every corpus document (fail-closed, all-or-nothing on
rejections in mode=full per G-06/G-11/G-13), runs PII redaction over the body
before embedding, chunks each requested strategy, embeds each chunk's
embed_text via the provider factory, writes the index, and writes a new
manifest under data/manifests/<index_version>.json (contract 6.2). The /ingest
JSON response shape (contract 8.2) is printed to stdout.

Under MJD_PROFILE=ci the factory yields the deterministic mock embedder and the
FileIndexWriter fallback is used so no Postgres is needed.

Usage:
    MJD_PROFILE=ci python -m scripts.ingest --mode full \\
        --strategies production,naive [--paths corpus/] [--dry-run]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from config.loader import load_config  # noqa: E402
from ingestion.chunkers.base import build_chunks  # noqa: E402
from ingestion.embed import embed_chunks  # noqa: E402
from ingestion.index import (  # noqa: E402
    FileIndexWriter,
    PostgresIndexWriter,
    load_latest_manifest,
    make_index_version,
    write_manifest,
)
from ingestion.loaders.base import LoaderError, load_path  # noqa: E402
from ingestion.metadata import (  # noqa: E402
    Rejection,
    compute_superseded_flags,
    validate_corpus,
)
from ingestion.pii import make_redactor  # noqa: E402
from providers.factory import get_embedding_provider  # noqa: E402

DEFAULT_CORPUS_VERSION = "2026.06.0"
SUPPORTED_SUFFIXES = {".md", ".markdown", ".docx", ".pdf", ".html", ".htm"}


def _discover(paths: list[str]) -> list[Path]:
    """Expand path arguments into a sorted, deduped list of supported files."""
    found: set[Path] = set()
    for raw in paths:
        p = (REPO_ROOT / raw) if not Path(raw).is_absolute() else Path(raw)
        if p.is_dir():
            for child in p.rglob("*"):
                if child.is_file() and child.suffix.lower() in SUPPORTED_SUFFIXES:
                    found.add(child)
        elif p.is_file():
            found.add(p)
    return sorted(found)


def _content_hash(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def ingest(
    *,
    mode: str,
    paths: list[str],
    strategies: list[str],
    dry_run: bool,
) -> dict:
    """Run the ingestion pipeline and return the /ingest response dict."""
    started = time.monotonic()
    cfg = load_config()
    files = _discover(paths)

    # Load every file; loader failures are rejections (G-11).
    loaded: list = []
    rejections: list[Rejection] = []
    for file_path in files:
        try:
            doc = load_path(file_path)
        except LoaderError as exc:
            rejections.append(Rejection(str(file_path), None, exc.reason, exc.message))
            continue
        loaded.append(doc)

    # Validate the whole corpus (fail-closed, corpus-wide G-06/G-13/G-08).
    parsed = [(doc.path, doc.header) for doc in loaded]
    valid, meta_rejections = validate_corpus(parsed)
    rejections.extend(meta_rejections)

    rejected_payload = [
        {"path": r.path, "doc_id": r.doc_id, "reason": r.reason} for r in rejections
    ]

    # mode=full is all-or-nothing: ANY rejection fails the run, no index written.
    if mode == "full" and rejections:
        return {
            "ingested": 0,
            "rejected": rejected_payload,
            "error": {
                "code": "ingest_rejected",
                "message": (
                    f"{len(rejections)} document(s) rejected; full ingest is "
                    "all-or-nothing and wrote no index."
                ),
            },
        }

    superseded = compute_superseded_flags(valid)
    by_doc_id = {doc.header.get("doc_id"): doc for doc in loaded}
    redactor = make_redactor(profile=cfg.profile)

    chunk_counts: dict[str, int] = {s: 0 for s in strategies}
    pii_redactions = 0
    per_doc_chunk_count: dict[str, int] = {}
    all_chunks: list = []
    documents_meta: list[dict] = []

    for doc_id, meta in valid.items():
        loaded_doc = by_doc_id[doc_id]
        content_hash = _content_hash(loaded_doc.raw_bytes)
        is_superseded = doc_id in superseded

        # PII redaction over the body BEFORE chunking/embedding (G-03).
        redaction = redactor.redact(loaded_doc.body)
        pii_redactions += redaction.count
        body = redaction.text

        doc_chunk_total = 0
        for strategy in strategies:
            result = build_chunks(
                meta,
                body,
                content_hash=content_hash,
                is_superseded=is_superseded,
                cfg=cfg.chunking,
                strategy=strategy,
            )
            chunk_counts[strategy] += len(result.chunks)
            doc_chunk_total += len(result.chunks)
            all_chunks.extend(result.chunks)

        per_doc_chunk_count[doc_id] = doc_chunk_total
        documents_meta.append(
            {
                "doc_id": doc_id,
                "version": meta.version,
                "content_hash": content_hash,
                "is_superseded": is_superseded,
                "supersedes": meta.supersedes,
                "chunk_count": doc_chunk_total,
            }
        )

    index_version = make_index_version()

    if dry_run:
        return {
            "index_version": index_version,
            "manifest_path": None,
            "ingested": len(valid),
            "rejected": rejected_payload,
            "chunks": chunk_counts,
            "duration_s": round(time.monotonic() - started, 1),
            "pii_redactions": pii_redactions,
            "dry_run": True,
        }

    # Embed every chunk's embed_text via the configured provider.
    provider = get_embedding_provider(cfg)
    embedded = embed_chunks(provider, all_chunks)

    # Write the index. CI / zero-Postgres uses the file fallback.
    writer = _make_writer(cfg, embedded.dim)
    writer.write(all_chunks, embedded.vectors, index_version)

    manifest_path = write_manifest(
        manifest_dir=None,
        index_version=index_version,
        corpus_version=DEFAULT_CORPUS_VERSION,
        embedding={
            "adapter": cfg.providers.embedding.adapter,
            "model": embedded.model,
            "model_version": embedded.model_version,
            "dim": embedded.dim,
            "resolved_from": embedded.resolved_from,
        },
        chunking={
            "strategy": cfg.chunking.strategy,
            "child_target_tokens": cfg.chunking.child_target_tokens,
            "child_overlap_pct": cfg.chunking.child_overlap_pct,
            "parent_max_tokens": cfg.chunking.parent_max_tokens,
        },
        documents=documents_meta,
        counts={
            "documents": len(valid),
            "chunks_production": chunk_counts.get("production", 0),
            "chunks_naive": chunk_counts.get("naive", 0),
        },
    )

    try:
        manifest_str = str(manifest_path.relative_to(REPO_ROOT))
    except ValueError:
        manifest_str = str(manifest_path)

    return {
        "index_version": index_version,
        "manifest_path": manifest_str,
        "ingested": len(valid),
        "rejected": rejected_payload,
        "chunks": chunk_counts,
        "duration_s": round(time.monotonic() - started, 1),
        "pii_redactions": pii_redactions,
    }


def _make_writer(cfg, dim: int):
    """Return the index writer for the active profile.

    The mock/ci and default-local profiles use the zero-dependency file writer so
    no Postgres is required. A real deployment that sets a DSN env override gets
    the pgvector writer.
    """
    import os

    dsn = os.environ.get("MJD_PG_DSN")
    if dsn and cfg.profile not in {"ci"}:
        return PostgresIndexWriter(dsn=dsn, dim=dim)
    return FileIndexWriter()


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ingest",
        description="Meridian J.D. corpus ingestion (contract 8.2).",
    )
    parser.add_argument("--mode", choices=["full", "incremental"], default="full")
    parser.add_argument(
        "--paths",
        default="corpus/",
        help="Comma-separated paths or directories to ingest.",
    )
    parser.add_argument(
        "--strategies",
        default="production,naive",
        help="Comma-separated chunk strategies to build.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    paths = [p.strip() for p in args.paths.split(",") if p.strip()]
    strategies = [s.strip() for s in args.strategies.split(",") if s.strip()]

    # Touch the prior manifest so incremental mode can reason about it later;
    # currently full and incremental both re-embed (content_hash is recorded for
    # the diff). Loading here keeps the read on the documented path.
    if args.mode == "incremental":
        load_latest_manifest()

    response = ingest(
        mode=args.mode,
        paths=paths,
        strategies=strategies,
        dry_run=args.dry_run,
    )
    print(json.dumps(response, indent=2))
    # Fail-closed exit code: a rejected full ingest is a non-zero exit.
    return 1 if response.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
