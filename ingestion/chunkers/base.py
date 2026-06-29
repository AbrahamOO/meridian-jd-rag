"""Chunker dispatch and the ChunkResult container.

`build_chunks(meta, body, content_hash, is_superseded, cfg, strategy)` returns a
ChunkResult: the list of Chunk records plus a side-channel list of per-chunk
extra metadata (e.g. `oversized_table`) kept OUT of the frozen Chunk but surfaced
to the visualizer through a side file (contract 4.1, G-10).
"""

from __future__ import annotations

from dataclasses import dataclass

from config.loader import ChunkingConfig
from core.models import Chunk, DocumentMetadata


@dataclass(frozen=True)
class ChunkResult:
    chunks: list[Chunk]
    side_meta: list[dict]  # aligned to chunks: {"chunk_id":..., "oversized_table":bool}


def build_chunks(
    meta: DocumentMetadata,
    body: str,
    *,
    content_hash: str,
    is_superseded: bool,
    cfg: ChunkingConfig,
    strategy: str,
) -> ChunkResult:
    """Dispatch to the requested chunk strategy. Both strategies emit the same
    Chunk schema; every chunk inherits classification + allowed_roles from meta
    (enforced inside each chunker and asserted by tests)."""
    if strategy == "production":
        from ingestion.chunkers.production import chunk_production

        return chunk_production(
            meta,
            body,
            content_hash=content_hash,
            is_superseded=is_superseded,
            cfg=cfg,
        )
    if strategy == "naive":
        from ingestion.chunkers.naive import chunk_naive

        return chunk_naive(
            meta,
            body,
            content_hash=content_hash,
            is_superseded=is_superseded,
            cfg=cfg,
        )
    raise ValueError(f"Unknown chunk strategy: {strategy!r}")
