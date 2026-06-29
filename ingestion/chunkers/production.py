"""Production chunker (contract 4.1, 4.2; gap-register G-10).

Algorithm:
1. Parse the body into structural segments (headings, paragraphs, tables).
2. Group segments into sections keyed by section_path. Each section becomes a
   parent (capped at parent_max_tokens for storage).
3. Within a section, build child chunks targeting child_target_tokens by packing
   paragraphs; oversized paragraphs are recursively split on sentence boundaries
   with child_overlap_pct overlap. A table is ALWAYS its own atomic child chunk,
   never split, flagged oversized_table when it exceeds the target (G-10).
4. embed_text = "{title} > {section_path}\n\n{text}" (4.2).
5. Every chunk inherits classification + allowed_roles from the document; a chunk
   built without them is a fatal error.
"""

from __future__ import annotations

import re

from config.loader import ChunkingConfig
from core.models import Chunk, DocumentMetadata
from ingestion.chunkers.base import ChunkResult
from ingestion.chunkers.structure import Segment, parse_segments
from ingestion.tokens import count_tokens

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _embed_text(title: str, section_path: str, text: str) -> str:
    """Contextual header format (contract 4.2)."""
    header = f"{title} > {section_path}" if section_path else title
    return f"{header}\n\n{text}"


def _split_oversized(text: str, target: int, overlap_pct: float) -> list[str]:
    """Recursively split an oversized paragraph on sentence boundaries with
    overlap. Returns one or more pieces each <= ~target tokens where possible."""
    if count_tokens(text) <= target:
        return [text]
    sentences = [s for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    if len(sentences) <= 1:
        # A single huge sentence: hard-split on character budget.
        approx_chars = target * 4
        hard_pieces = [text[i : i + approx_chars] for i in range(0, len(text), approx_chars)]
        return [p for p in hard_pieces if p.strip()]

    overlap_tokens = max(0, int(target * overlap_pct))
    pieces: list[str] = []
    current: list[str] = []
    current_tokens = 0
    for sentence in sentences:
        s_tokens = count_tokens(sentence)
        if current and current_tokens + s_tokens > target:
            pieces.append(" ".join(current))
            # Carry overlap: keep trailing sentences up to overlap_tokens.
            carry: list[str] = []
            carry_tokens = 0
            for prev in reversed(current):
                pt = count_tokens(prev)
                if carry_tokens + pt > overlap_tokens:
                    break
                carry.insert(0, prev)
                carry_tokens += pt
            current = carry
            current_tokens = carry_tokens
        current.append(sentence)
        current_tokens += s_tokens
    if current:
        pieces.append(" ".join(current))
    return pieces


def _group_sections(segments: list[Segment]) -> list[tuple[str, str, list[Segment]]]:
    """Group content segments by their section_path, preserving order. Returns
    [(section_path, heading_title, [content segments])]. Heading segments are
    used only to set context; they are not themselves content."""
    groups: list[tuple[str, str, list[Segment]]] = []
    index: dict[str, int] = {}
    for seg in segments:
        if seg.kind == "heading":
            continue
        key = seg.section_path
        if key not in index:
            index[key] = len(groups)
            groups.append((seg.section_path, seg.heading_title, []))
        groups[index[key]][2].append(seg)
    return groups


def chunk_production(
    meta: DocumentMetadata,
    body: str,
    *,
    content_hash: str,
    is_superseded: bool,
    cfg: ChunkingConfig,
) -> ChunkResult:
    if not meta.classification or not meta.allowed_roles:
        raise ValueError(f"FATAL: chunk for {meta.doc_id} missing classification/allowed_roles.")

    segments = parse_segments(body)
    groups = _group_sections(segments)

    chunks: list[Chunk] = []
    side: list[dict] = []
    child_seq = 0
    parent_seq = 0

    for section_path, _heading_title, seg_list in groups:
        parent_seq += 1
        parent_id = f"{meta.doc_id}::p{parent_seq:04d}"
        parent_full = "\n\n".join(s.text for s in seg_list).strip()
        if not parent_full:
            continue
        # Parent storage cap (small-to-big): truncate on a paragraph boundary.
        parent_text = _cap_parent(parent_full, cfg.parent_max_tokens)

        # Build children: pack paragraphs, split oversized, tables atomic (G-10).
        child_units = _build_children(seg_list, cfg)

        section_title = meta.title
        for text, oversized_table in child_units:
            text = text.strip()
            if not text:
                continue
            child_seq += 1
            chunk_id = f"{meta.doc_id}::c{child_seq:04d}"
            start, end = _locate(body, text)
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
                    section_path=section_path,
                    text=text,
                    embed_text=_embed_text(section_title, section_path, text),
                    parent_text=parent_text,
                    char_start=start,
                    char_end=end,
                    token_count=count_tokens(text),
                    content_hash=content_hash,
                    chunk_strategy="production",
                )
            )
            side.append({"chunk_id": chunk_id, "oversized_table": oversized_table})

    return ChunkResult(chunks=chunks, side_meta=side)


def _cap_parent(text: str, max_tokens: int) -> str:
    """Truncate a parent on a paragraph boundary, never mid-table (G-10).
    If the first paragraph is itself a table that exceeds the cap, keep the whole
    table (atomic) rather than truncating it mid-row."""
    if count_tokens(text) <= max_tokens:
        return text
    paragraphs = text.split("\n\n")
    kept: list[str] = []
    running = 0
    for para in paragraphs:
        pt = count_tokens(para)
        if kept and running + pt > max_tokens:
            break
        kept.append(para)
        running += pt
        if running >= max_tokens:
            break
    return "\n\n".join(kept) if kept else paragraphs[0]


def _locate(body: str, text: str) -> tuple[int, int]:
    """Best-effort char offsets of a chunk's first line within the body."""
    probe = text.split("\n", 1)[0][:80]
    idx = body.find(probe) if probe else -1
    if idx < 0:
        return 0, len(text)
    return idx, idx + len(text)


def _build_children(seg_list: list[Segment], cfg: ChunkingConfig) -> list[tuple[str, bool]]:
    """Pack a section's segments into child units (text, oversized_table).

    Paragraphs are buffered up to the child token target; an oversized paragraph
    is split with overlap; a table is its own atomic child and is never merged or
    split (G-10). Factored out of the section loop so the flush closure does not
    bind a loop variable (ruff B023)."""
    child_units: list[tuple[str, bool]] = []
    buffer: list[str] = []
    buffer_tokens = 0

    def _flush() -> None:
        nonlocal buffer, buffer_tokens
        if buffer:
            child_units.append(("\n\n".join(buffer), False))
            buffer = []
            buffer_tokens = 0

    for seg in seg_list:
        if seg.kind == "table":
            _flush()
            child_units.append((seg.text, count_tokens(seg.text) > cfg.child_target_tokens))
            continue
        seg_tokens = count_tokens(seg.text)
        if seg_tokens > cfg.child_target_tokens:
            _flush()
            for piece in _split_oversized(seg.text, cfg.child_target_tokens, cfg.child_overlap_pct):
                child_units.append((piece, False))
            continue
        if buffer and buffer_tokens + seg_tokens > cfg.child_target_tokens:
            _flush()
        buffer.append(seg.text)
        buffer_tokens += seg_tokens
    _flush()
    return child_units
