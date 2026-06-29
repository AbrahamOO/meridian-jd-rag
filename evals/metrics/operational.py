"""Operational metrics (contract 7.2, 7.3; spec section 12).

Per-record: latency_ms, cost_usd, tokens (total). Aggregate: latency p50/p95,
cost per query, tokens per query. Deterministic given the mock providers (all
costs are 0.0; token counts are word-counts). Latency is wall-clock and the ONLY
non-deterministic field, so it is excluded from any byte-identity assertion.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TypedDict


class OperationalMetrics(TypedDict):
    latency_ms: float
    cost_usd: float
    tokens: int


def operational_metrics(*, latency_ms: float, cost_usd: float, tokens: int) -> OperationalMetrics:
    return OperationalMetrics(
        latency_ms=round(latency_ms, 4),
        cost_usd=round(cost_usd, 6),
        tokens=int(tokens),
    )


def percentile(values: Sequence[float], pct: float) -> float:
    """Nearest-rank percentile (pct in [0, 100]). Empty -> 0.0."""
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = math.ceil((pct / 100.0) * len(ordered))
    rank = min(max(rank, 1), len(ordered))
    return ordered[rank - 1]


def aggregate_operational(records: Sequence[OperationalMetrics]) -> dict:
    """Aggregate per-record operational metrics into the report 7.3 shape."""
    if not records:
        return {
            "latency_p50_ms": 0.0,
            "latency_p95_ms": 0.0,
            "cost_per_query_usd": 0.0,
            "tokens_per_query": 0.0,
        }
    latencies = [r["latency_ms"] for r in records]
    costs = [r["cost_usd"] for r in records]
    tokens = [r["tokens"] for r in records]
    n = len(records)
    return {
        "latency_p50_ms": round(percentile(latencies, 50), 4),
        "latency_p95_ms": round(percentile(latencies, 95), 4),
        "cost_per_query_usd": round(sum(costs) / n, 6),
        "tokens_per_query": round(sum(tokens) / n, 4),
    }


__all__ = [
    "OperationalMetrics",
    "operational_metrics",
    "percentile",
    "aggregate_operational",
]
