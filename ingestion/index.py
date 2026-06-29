"""Index writers and the manifest (contract 6.2; gap-register G-01, G-20).

Two backends share one `IndexWriter` protocol:

- `PostgresIndexWriter` (lazy psycopg + pgvector): applies schema.sql with the
  active embedding dim, bulk-inserts chunks + vectors + the dual tsvector columns
  are generated, builds the dense ANN index. Used in production.
- `FileIndexWriter`: a zero-dependency JSONL index under
  `data/index/<index_version>/` so unit tests and zero-Postgres CI run without a
  DB. It stores the exact same chunk records + vectors, enough for an in-memory
  retrieval fallback.

Both write a NEW manifest per run under `data/manifests/<index_version>.json`
(never mutating the live one, G-20). Incremental re-embedding compares per-doc
`content_hash` against the previous manifest.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from core.models import Chunk

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_DIR = REPO_ROOT / "data" / "manifests"
DEFAULT_INDEX_DIR = REPO_ROOT / "data" / "index"
SCHEMA_SQL = Path(__file__).resolve().parent / "schema.sql"


def now_rfc3339() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.") + (
        f"{datetime.now(UTC).microsecond // 1000:03d}Z"
    )


def make_index_version(seq: int = 1) -> str:
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    return f"idx-{day}-{seq:03d}"


class IndexWriter(Protocol):
    def write(
        self, chunks: list[Chunk], vectors: list[list[float]], index_version: str
    ) -> None: ...


class FileIndexWriter:
    """Zero-dependency file index for tests and zero-Postgres CI."""

    def __init__(self, index_dir: Path | None = None) -> None:
        self._dir = index_dir or DEFAULT_INDEX_DIR

    def write(self, chunks: list[Chunk], vectors: list[list[float]], index_version: str) -> None:
        target = self._dir / index_version
        target.mkdir(parents=True, exist_ok=True)
        path = target / "chunks.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for chunk, vector in zip(chunks, vectors, strict=True):
                record = asdict(chunk)
                record["embedding"] = vector
                record["index_version"] = index_version
                handle.write(json.dumps(record) + "\n")

    def load(self, index_version: str) -> list[dict]:
        path = self._dir / index_version / "chunks.jsonl"
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]


class PostgresIndexWriter:
    """pgvector-backed index writer (lazy psycopg import)."""

    def __init__(self, dsn: str, dim: int) -> None:
        self._dsn = dsn
        self._dim = dim

    def _connect(self):
        import psycopg  # lazy

        return psycopg.connect(self._dsn)

    def ensure_schema(self) -> None:
        ddl = SCHEMA_SQL.read_text(encoding="utf-8").replace("{DIM}", str(self._dim))
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(ddl)
            conn.commit()

    def write(self, chunks: list[Chunk], vectors: list[list[float]], index_version: str) -> None:
        self.ensure_schema()
        from pgvector.psycopg import register_vector

        with self._connect() as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                for chunk, vector in zip(chunks, vectors, strict=True):
                    cur.execute(
                        """
                        INSERT INTO chunks (
                            chunk_id, doc_id, parent_id, title, department, doc_type,
                            classification, owner_role, allowed_roles, effective_date,
                            version, supersedes, is_superseded, entity_status,
                            section_path, text, embed_text, parent_text, char_start,
                            char_end, token_count, content_hash, chunk_strategy,
                            embedding, index_version
                        ) VALUES (
                            %(chunk_id)s, %(doc_id)s, %(parent_id)s, %(title)s,
                            %(department)s, %(doc_type)s, %(classification)s,
                            %(owner_role)s, %(allowed_roles)s, %(effective_date)s,
                            %(version)s, %(supersedes)s, %(is_superseded)s,
                            %(entity_status)s, %(section_path)s, %(text)s,
                            %(embed_text)s, %(parent_text)s, %(char_start)s,
                            %(char_end)s, %(token_count)s, %(content_hash)s,
                            %(chunk_strategy)s, %(embedding)s, %(index_version)s
                        )
                        ON CONFLICT (chunk_id) DO UPDATE SET
                            embedding = EXCLUDED.embedding,
                            index_version = EXCLUDED.index_version
                        """,
                        {**asdict(chunk), "embedding": vector, "index_version": index_version},
                    )
            conn.commit()


def write_manifest(
    *,
    manifest_dir: Path | None,
    index_version: str,
    corpus_version: str,
    embedding: dict,
    chunking: dict,
    documents: list[dict],
    counts: dict,
) -> Path:
    """Write a NEW manifest file (contract 6.2). Never mutates an existing one."""
    target_dir = manifest_dir or DEFAULT_MANIFEST_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "manifest_version": "1.0.0",
        "corpus_version": corpus_version,
        "index_version": index_version,
        "created_at": now_rfc3339(),
        "embedding": embedding,
        "chunking": chunking,
        "documents": documents,
        "counts": counts,
    }
    path = target_dir / f"{index_version}.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def load_latest_manifest(manifest_dir: Path | None = None) -> dict | None:
    """Load the most recent manifest for incremental content_hash comparison."""
    target_dir = manifest_dir or DEFAULT_MANIFEST_DIR
    if not target_dir.exists():
        return None
    manifests = sorted(target_dir.glob("idx-*.json"))
    if not manifests:
        return None
    return json.loads(manifests[-1].read_text(encoding="utf-8"))


def prior_hashes(manifest: dict | None) -> dict[str, str]:
    """Map doc_id -> content_hash from a prior manifest for incremental diff."""
    if not manifest:
        return {}
    return {d["doc_id"]: d.get("content_hash", "") for d in manifest.get("documents", [])}
