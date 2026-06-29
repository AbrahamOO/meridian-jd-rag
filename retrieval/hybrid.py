"""Hybrid dense + sparse retrieval with RRF fusion (contracts.md section 3.2;
gap-register G-01, G-02).

``hybrid_retrieve`` takes the access filter and a repository, runs the dense
(cosine) and sparse (BM25/ts_rank_cd-equivalent) lists, both carrying the SAME
access filter, fuses them with Reciprocal Rank Fusion, then applies the
multiplicative superseded penalty (G-02) and sorts.

RRF math (normative): each list is ranked starting at rank 1; per-chunk
contribution is ``1 / (rrf_k + rank)``; a chunk's ``rrf_score`` is the sum of its
contributions across the dense and sparse lists. Then
``final = rrf_score * (superseded_penalty if is_superseded else 1.0)``. Sort by
``final`` descending, ties broken by ``chunk_id`` ascending.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from core.models import Candidate, Chunk


class ChunkRepository(Protocol):
    def dense_candidates(
        self, query_vector: list[float], access_filter: Mapping[str, Any], *, top_k: int
    ) -> list[tuple[Chunk, float]]: ...

    def sparse_candidates(
        self, query_text: str, access_filter: Mapping[str, Any], *, top_k: int
    ) -> list[tuple[Chunk, float]]: ...


def rrf_contribution(rrf_k: int, rank: int) -> float:
    """RRF contribution for a chunk at 1-based ``rank``: 1 / (rrf_k + rank)."""
    return 1.0 / (rrf_k + rank)


def hybrid_retrieve(
    query_text: str,
    query_vector: list[float],
    access_filter: Mapping[str, Any],
    repository: ChunkRepository,
    *,
    top_k_dense: int,
    top_k_sparse: int,
    rrf_k: int,
    superseded_penalty: float,
) -> list[Candidate]:
    """Fuse dense + sparse access-filtered lists with RRF and apply the superseded
    penalty. Both lists carry the SAME ``access_filter`` (contract 3.2)."""
    dense = repository.dense_candidates(query_vector, access_filter, top_k=top_k_dense)
    sparse = repository.sparse_candidates(query_text, access_filter, top_k=top_k_sparse)

    # Accumulate per-chunk fusion state keyed by chunk_id.
    state: dict[str, dict[str, Any]] = {}

    for rank, (chunk, score) in enumerate(dense, start=1):
        entry = state.setdefault(
            chunk.chunk_id,
            {
                "chunk": chunk,
                "dense_rank": None,
                "sparse_rank": None,
                "dense_score": None,
                "sparse_score": None,
                "rrf": 0.0,
            },
        )
        entry["dense_rank"] = rank
        entry["dense_score"] = score
        entry["rrf"] += rrf_contribution(rrf_k, rank)

    for rank, (chunk, score) in enumerate(sparse, start=1):
        entry = state.setdefault(
            chunk.chunk_id,
            {
                "chunk": chunk,
                "dense_rank": None,
                "sparse_rank": None,
                "dense_score": None,
                "sparse_score": None,
                "rrf": 0.0,
            },
        )
        entry["sparse_rank"] = rank
        entry["sparse_score"] = score
        entry["rrf"] += rrf_contribution(rrf_k, rank)

    candidates: list[Candidate] = []
    for entry in state.values():
        chunk = entry["chunk"]
        penalty = superseded_penalty if chunk.is_superseded else 1.0
        final = entry["rrf"] * penalty
        candidates.append(
            Candidate(
                chunk=chunk,
                dense_rank=entry["dense_rank"],
                sparse_rank=entry["sparse_rank"],
                rrf_score=final,
                dense_score=entry["dense_score"],
                sparse_score=entry["sparse_score"],
            )
        )

    # Sort by final score descending, ties broken by chunk_id ascending.
    candidates.sort(key=lambda c: (-c.rrf_score, c.chunk.chunk_id))
    return candidates


__all__ = ["hybrid_retrieve", "rrf_contribution", "ChunkRepository"]
