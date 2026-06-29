"""Naive baseline chunker (contract 4.3).

Fixed-size split at child_target_tokens with no contextual header, no structure
awareness, no parent expansion (parent_text == text). Exists solely so the eval
harness can report a naive-vs-production delta. Still inherits the document's
classification + allowed_roles on every chunk (the access backbone is never
optional, even for the baseline).
"""

from __future__ import annotations

from config.loader import ChunkingConfig
from core.models import Chunk, DocumentMetadata
from ingestion.chunkers.base import ChunkResult
from ingestion.tokens import count_tokens


def chunk_naive(
    meta: DocumentMetadata,
    body: str,
    *,
    content_hash: str,
    is_superseded: bool,
    cfg: ChunkingConfig,
) -> ChunkResult:
    if not meta.classification or not meta.allowed_roles:
        raise ValueError(f"FATAL: chunk for {meta.doc_id} missing classification/allowed_roles.")

    # Fixed-size split by character budget approximating child_target_tokens.
    approx_chars = max(1, cfg.child_target_tokens * 4)
    text = body.strip()
    pieces = [text[i : i + approx_chars] for i in range(0, len(text), approx_chars)]
    pieces = [p for p in pieces if p.strip()]

    chunks: list[Chunk] = []
    side: list[dict] = []
    for seq, piece in enumerate(pieces, start=1):
        chunk_id = f"{meta.doc_id}::c{seq:04d}"
        parent_id = f"{meta.doc_id}::p{seq:04d}"  # naive: parent == self
        start = (seq - 1) * approx_chars
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                doc_id=meta.doc_id,
                parent_id=parent_id,
                title=meta.title,
                department=meta.department,
                doc_type=meta.doc_type,
                classification=meta.classification,
                owner_role=meta.owner_role,
                allowed_roles=list(meta.allowed_roles),
                effective_date=meta.effective_date,
                version=meta.version,
                supersedes=meta.supersedes,
                is_superseded=is_superseded,
                entity_status=meta.entity_status,
                section_path="",
                text=piece,
                embed_text=piece,  # no contextual header for the baseline
                parent_text=piece,  # no parent expansion
                char_start=start,
                char_end=start + len(piece),
                token_count=count_tokens(piece),
                content_hash=content_hash,
                chunk_strategy="naive",
            )
        )
        side.append({"chunk_id": chunk_id, "oversized_table": False})

    return ChunkResult(chunks=chunks, side_meta=side)
