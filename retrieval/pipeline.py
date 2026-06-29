"""End-to-end retrieval orchestration (contracts.md section 3).

Wires the security-critical pipeline in the contract's fixed order:

    resolve_access -> build_access_filter (FIRST, fail-closed)
    -> transform_query (each subquery under the SAME access filter, G-14)
    -> embed query -> hybrid_retrieve (dense+sparse+RRF+superseded penalty)
    -> rerank_candidates -> assemble_context (+ citation access side table)

The access filter is built once per request and reused for every subquery so no
subquery can escalate scope. Unknown role short-circuits to an empty result with
``allowed=False`` (boundary). This is the function the query graph and the proof
script call.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from core.models import AccessDecision, AssembledContext, Candidate
from providers.base import EmbeddingProvider, Reranker
from retrieval.access import build_access_filter, resolve_access
from retrieval.assemble import assemble_context
from retrieval.citations import attach_access_metadata
from retrieval.hybrid import ChunkRepository, hybrid_retrieve
from retrieval.rerank import rerank_candidates
from retrieval.transform import expand_for_retrieval, transform_query


@dataclass(frozen=True)
class RetrievalResult:
    access: AccessDecision
    access_filter: dict
    candidates: list[Candidate]
    reranked: list[Candidate]
    context: AssembledContext
    retrieved_doc_ids: list[str]


def retrieve(
    role: str,
    query: str,
    *,
    embedder: EmbeddingProvider,
    reranker: Reranker,
    repository: ChunkRepository,
    cfg: Mapping[str, Any],
    history: list[dict] | None = None,
) -> RetrievalResult:
    """Run the full access-controlled retrieval pipeline for one request."""
    history = history or []
    retrieval_cfg = cfg.get("retrieval", {})
    chunking_cfg = cfg.get("chunking", {})
    transform_cfg = retrieval_cfg.get("transform", {})
    active_strategy = chunking_cfg.get("strategy", "production")

    # 1. Access pre-filter FIRST, always. Fail-closed on unknown role.
    decision = resolve_access(role)
    access_filter = build_access_filter(decision, active_strategy=active_strategy)

    empty_context = AssembledContext(blocks=[], total_tokens=0, dropped_for_budget=[])
    if not decision.allowed:
        return RetrievalResult(
            access=decision,
            access_filter=access_filter,
            candidates=[],
            reranked=[],
            context=empty_context,
            retrieved_doc_ids=[],
        )

    # 2. Query transformation. Each subquery uses the SAME access filter (G-14).
    transformed = transform_query(query, history, transform_cfg)
    queries = expand_for_retrieval(transformed, transform_cfg)

    # 3. Retrieve per query under the single shared access filter, fuse by chunk.
    top_k_dense = retrieval_cfg.get("top_k_dense", 20)
    top_k_sparse = retrieval_cfg.get("top_k_sparse", 20)
    rrf_k = retrieval_cfg.get("rrf_k", 60)
    superseded_penalty = retrieval_cfg.get("superseded_penalty", 0.5)

    fused: dict[str, Candidate] = {}
    for sub in queries:
        vector = embedder.embed([sub], kind="query").vectors[0]
        partial = hybrid_retrieve(
            sub,
            vector,
            access_filter,
            repository,
            top_k_dense=top_k_dense,
            top_k_sparse=top_k_sparse,
            rrf_k=rrf_k,
            superseded_penalty=superseded_penalty,
        )
        for cand in partial:
            existing = fused.get(cand.chunk.chunk_id)
            if existing is None or cand.rrf_score > existing.rrf_score:
                fused[cand.chunk.chunk_id] = cand

    candidates = sorted(fused.values(), key=lambda c: (-c.rrf_score, c.chunk.chunk_id))

    # 4. Rerank only the access-filtered candidates.
    rerank_top_n = retrieval_cfg.get("rerank_top_n", 6)
    reranked = rerank_candidates(transformed.rewritten, candidates, reranker, top_n=rerank_top_n)

    # 5. Parent-document assembly + token budget.
    token_budget = retrieval_cfg.get("context_token_budget", 3500)
    parent_max_tokens = chunking_cfg.get("parent_max_tokens", 1200)
    context = assemble_context(
        reranked, token_budget=token_budget, parent_max_tokens=parent_max_tokens
    )
    # Record access metadata for the citation re-validator (defense in depth).
    attach_access_metadata(context, reranked)

    retrieved_doc_ids: list[str] = []
    for cand in reranked:
        if cand.chunk.doc_id not in retrieved_doc_ids:
            retrieved_doc_ids.append(cand.chunk.doc_id)

    return RetrievalResult(
        access=decision,
        access_filter=access_filter,
        candidates=candidates,
        reranked=reranked,
        context=context,
        retrieved_doc_ids=retrieved_doc_ids,
    )


__all__ = ["retrieve", "RetrievalResult"]
