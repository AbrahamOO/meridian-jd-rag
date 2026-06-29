"""Chunkers (contract section 4). Two strategies, one Chunk output schema.

`production`: structure-aware (heading hierarchy), recursive paragraph/sentence
split in oversized leaves with overlap, never splits a Markdown table (G-10),
contextual headers (4.2), small-to-big parents capped at parent_max_tokens.

`naive`: fixed-size, no header, no parent (parent_text == text). Eval baseline.
"""

from __future__ import annotations

from ingestion.chunkers.base import ChunkResult, build_chunks

__all__ = ["ChunkResult", "build_chunks"]
