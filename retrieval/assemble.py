"""Parent-document assembly and token budgeting (contracts.md section 3.5;
gap-register G-05, G-10).

``assemble_context`` walks the reranked candidates best-first, resolves each to
its parent section, dedupes parents, enforces the token budget, and attaches the
citation metadata ({doc_id, title, section_path, version}) on each ContextBlock.

Token-budget math (normative G-05):
- Reserve a fixed 600-token system+question overhead inside ``token_budget``.
- Add a parent only if ``running + parent_tokens <= token_budget - 600``.
  Otherwise record it in ``dropped_for_budget`` and KEEP scanning (a later,
  smaller parent may still fit).
- A parent longer than ``parent_max_tokens`` is truncated on a paragraph boundary
  (never mid-table, G-10) and the truncation is recorded by capping length.
- At least ONE block is always included if any candidate survived: if the single
  best parent alone exceeds the budget it is truncated to fit rather than dropped,
  so a non-empty allowed retrieval never yields an empty context.
"""

from __future__ import annotations

from core.models import AssembledContext, Candidate, ContextBlock

OVERHEAD_TOKENS = 600  # reserved system+question overhead (G-05)


def _count_tokens(text: str) -> int:
    """Token count heuristic (G-05): word count, stable across runs. The real
    generators may pass a tokenizer-backed count; the file/CI path uses words so
    eval numbers are deterministic."""
    return len(text.split())


def _truncate_paragraph(text: str, max_tokens: int) -> str:
    """Truncate ``text`` to at most ``max_tokens`` tokens on a paragraph boundary,
    never splitting a Markdown table (G-10). Falls back to a word-boundary cut
    only if the first paragraph alone already exceeds the budget AND is not a
    table; a leading table is kept whole to preserve interpretability."""
    if _count_tokens(text) <= max_tokens:
        return text
    paragraphs = text.split("\n\n")
    kept: list[str] = []
    running = 0
    for para in paragraphs:
        ptoks = _count_tokens(para)
        is_table = para.lstrip().startswith("|")
        if running + ptoks <= max_tokens:
            kept.append(para)
            running += ptoks
            continue
        # Cannot fit this paragraph whole.
        if not kept:
            # Must include at least something. A leading table stays whole (G-10);
            # otherwise cut on a word boundary.
            if is_table:
                return para
            words = para.split()
            return " ".join(words[:max_tokens])
        break
    return "\n\n".join(kept)


def assemble_context(
    reranked: list[Candidate],
    *,
    token_budget: int,
    parent_max_tokens: int,
) -> AssembledContext:
    """Assemble parent-document context within the token budget (G-05)."""
    blocks: list[ContextBlock] = []
    dropped: list[str] = []
    seen_parents: set[str] = set()
    running = 0
    effective_budget = token_budget - OVERHEAD_TOKENS

    for candidate in reranked:
        chunk = candidate.chunk
        parent_id = chunk.parent_id
        if parent_id in seen_parents:
            continue  # dedupe parents (do not double count)
        seen_parents.add(parent_id)

        parent_text = chunk.parent_text or chunk.text
        # Cap to parent_max_tokens on a paragraph boundary (never mid-table).
        capped = _truncate_paragraph(parent_text, parent_max_tokens)
        parent_tokens = _count_tokens(capped)

        if not blocks:
            # Guarantee at least one block. If the single best parent alone
            # exceeds the remaining budget, truncate it to fit rather than drop.
            if parent_tokens > effective_budget and effective_budget > 0:
                capped = _truncate_paragraph(capped, effective_budget)
                parent_tokens = _count_tokens(capped)
            blocks.append(_to_block(chunk, capped))
            running += parent_tokens
            continue

        if running + parent_tokens <= effective_budget:
            blocks.append(_to_block(chunk, capped))
            running += parent_tokens
        else:
            dropped.append(parent_id)
            # keep scanning for a smaller parent (G-05)

    total_tokens = sum(_count_tokens(b.text) for b in blocks)
    return AssembledContext(blocks=blocks, total_tokens=total_tokens, dropped_for_budget=dropped)


def _to_block(chunk, text: str) -> ContextBlock:
    """Attach citation metadata {doc_id, title, section_path, version} (3.5/3.6)."""
    return ContextBlock(
        parent_id=chunk.parent_id,
        doc_id=chunk.doc_id,
        title=chunk.title,
        section_path=chunk.section_path,
        version=chunk.version,
        text=text,
        is_superseded=chunk.is_superseded,
    )


__all__ = ["assemble_context", "OVERHEAD_TOKENS"]
