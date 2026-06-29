"""Cross-encoder reranking (contracts.md section 3.4).

``rerank_candidates`` runs the Reranker provider over candidates that ALREADY
passed the access pre-filter and returns the top_n reordered. The reranker sees
``chunk.embed_text`` (contextual header + child text, contract 3.4) and never
re-introduces filtered content: it can only reorder the candidates it is given.
"""

from __future__ import annotations

from core.models import Candidate
from providers.base import Reranker


def rerank_candidates(
    query: str,
    candidates: list[Candidate],
    reranker: Reranker,
    *,
    top_n: int,
) -> list[Candidate]:
    """Reorder access-filtered candidates with the cross-encoder, keep top_n.

    Operates ONLY on the supplied (access-filtered) candidates. The reranker is
    fed ``chunk.embed_text``; the returned ``order`` indexes back into the input
    list so no out-of-scope content can be introduced.
    """
    if not candidates:
        return []
    if top_n <= 0:
        return []

    texts = [c.chunk.embed_text for c in candidates]
    result = reranker.rerank(query, texts, top_n=top_n)
    reordered: list[Candidate] = []
    for index in result.order:
        if 0 <= index < len(candidates):
            reordered.append(candidates[index])
    return reordered


__all__ = ["rerank_candidates"]
