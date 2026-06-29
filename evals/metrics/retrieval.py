"""Retrieval metrics computed from retrieved vs expected doc_ids (contract 7.2).

All metrics are computed at the DOCUMENT granularity: the golden record's
``expected_source`` is a set of doc_ids, and the system's retrieved order is the
``retrieved_doc_ids`` list (the doc_ids that survived the access filter, in
rerank order, deduped). This is the only honest granularity here because the
golden ground truth is authored at the document level.

Definitions (deterministic, dependency-free):

- context_precision: |retrieved ∩ expected| / |retrieved|
- context_recall:    |retrieved ∩ expected| / |expected|
- hit_rate_at_k:     1.0 if any expected doc appears in the top-k retrieved else 0
- mrr:               reciprocal rank of the FIRST expected doc in retrieved order
- ndcg:              normalized DCG with binary relevance (expected = 1)

For a ``deny`` / out-of-scope record expected_source is empty; the correct
behavior is empty retrieval, so an empty retrieved list scores 1.0 on every
metric (perfect) and any non-empty retrieval scores 0.0 on precision.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TypedDict


class RetrievalMetrics(TypedDict):
    context_precision: float
    context_recall: float
    hit_rate_at_k: float
    mrr: float
    ndcg: float


def context_precision(retrieved: Sequence[str], expected: Sequence[str]) -> float:
    if not retrieved:
        # No retrieval is perfect precision iff nothing was expected.
        return 1.0 if not expected else 0.0
    exp = set(expected)
    hits = sum(1 for d in dict.fromkeys(retrieved) if d in exp)
    distinct = len(dict.fromkeys(retrieved))
    return hits / distinct if distinct else 0.0


def context_recall(retrieved: Sequence[str], expected: Sequence[str]) -> float:
    if not expected:
        # Nothing expected: recall is trivially satisfied.
        return 1.0
    ret = set(retrieved)
    found = sum(1 for d in set(expected) if d in ret)
    return found / len(set(expected))


def hit_rate_at_k(retrieved: Sequence[str], expected: Sequence[str], *, k: int) -> float:
    if not expected:
        return 1.0 if not retrieved else 0.0
    topk = set(dict.fromkeys(retrieved))
    # honor k against the deduped order
    topk = set(list(dict.fromkeys(retrieved))[: max(0, k)])
    return 1.0 if topk & set(expected) else 0.0


def mrr(retrieved: Sequence[str], expected: Sequence[str]) -> float:
    if not expected:
        return 1.0 if not retrieved else 0.0
    exp = set(expected)
    for rank, doc_id in enumerate(dict.fromkeys(retrieved), start=1):
        if doc_id in exp:
            return 1.0 / rank
    return 0.0


def ndcg(retrieved: Sequence[str], expected: Sequence[str]) -> float:
    """Binary-relevance NDCG over the deduped retrieved order."""
    if not expected:
        return 1.0 if not retrieved else 0.0
    exp = set(expected)
    order = list(dict.fromkeys(retrieved))
    dcg = 0.0
    for i, doc_id in enumerate(order, start=1):
        if doc_id in exp:
            dcg += 1.0 / math.log2(i + 1)
    ideal_hits = min(len(exp), len(order)) if order else len(exp)
    ideal_hits = min(len(exp), max(len(order), 1))
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 0.0


def retrieval_metrics(
    retrieved: Sequence[str], expected: Sequence[str], *, k: int
) -> RetrievalMetrics:
    """Compute the full retrieval metric family for one record."""
    return RetrievalMetrics(
        context_precision=round(context_precision(retrieved, expected), 6),
        context_recall=round(context_recall(retrieved, expected), 6),
        hit_rate_at_k=round(hit_rate_at_k(retrieved, expected, k=k), 6),
        mrr=round(mrr(retrieved, expected), 6),
        ndcg=round(ndcg(retrieved, expected), 6),
    )


__all__ = [
    "RetrievalMetrics",
    "context_precision",
    "context_recall",
    "hit_rate_at_k",
    "mrr",
    "ndcg",
    "retrieval_metrics",
]
