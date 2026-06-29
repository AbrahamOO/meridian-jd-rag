"""Query transformation (contracts.md section 3.3; gap-register G-14).

``transform_query`` runs configurable transforms BEFORE retrieval:
- conversational rewrite (fold prior turns into a standalone query),
- multi-query expansion (paraphrase variants for recall),
- optional HyDE (a hypothetical-answer string embedded for dense recall),
- decomposition (split a compound question into subqueries).

Every subquery is retrieved by the caller under the SAME single access filter for
the requesting role (G-14): denied subqueries simply return nothing, they can
never escalate scope. This module is deterministic and config-driven; it performs
no network calls (the mock/CI path needs no LLM for transforms).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

_WS = re.compile(r"\s+")
# Conjunctions that mark a compound question worth decomposing.
_DECOMP_SPLIT = re.compile(
    r"\s+(?:\band\b|\bvs\.?\b|\bversus\b|\bas well as\b|\bcompared with\b|"
    r"\bcompared to\b)\s+|[;?]\s*(?=\S)",
    re.IGNORECASE,
)
_HYDE_TEMPLATE = "The relevant policy states that {q}"


@dataclass(frozen=True)
class TransformedQuery:
    original: str
    rewritten: str  # may equal original
    subqueries: list[str]  # [] if not decomposed; each retrieved separately
    used: list[str]  # which transforms ran: ["rewrite","decompose","hyde", ...]


def _normalize(text: str) -> str:
    return _WS.sub(" ", text).strip()


def _rewrite(query: str, history: list[dict]) -> str:
    """Conversational rewrite: prepend the last user turn's subject when the new
    query is a short follow-up (pronoun/ellipsis heuristic). Deterministic."""
    base = _normalize(query)
    if not history:
        return base
    last_user = ""
    for turn in reversed(history):
        if turn.get("role") == "user" and str(turn.get("content", "")).strip():
            last_user = _normalize(str(turn["content"]))
            break
    if not last_user:
        return base
    follow_up = len(base.split()) <= 6 or bool(
        re.match(r"^(what about|and|it|its|that|this|those|they)\b", base, re.IGNORECASE)
    )
    if follow_up:
        return _normalize(f"{last_user} {base}")
    return base


def _multi_query(query: str) -> list[str]:
    """Deterministic paraphrase variants for recall. No LLM in the CI path."""
    q = _normalize(query)
    variants = [
        q,
        f"policy and procedure for {q}",
        f"what does the standard say about {q}",
    ]
    seen: list[str] = []
    for v in variants:
        nv = _normalize(v)
        if nv and nv not in seen:
            seen.append(nv)
    return seen


def _decompose(query: str) -> list[str]:
    """Split a compound question into subqueries on conjunctions. Returns [] when
    the query is a single clause (nothing to decompose)."""
    parts = [_normalize(p) for p in _DECOMP_SPLIT.split(query) if _normalize(p)]
    # Only treat as decomposed when there is genuinely more than one clause and
    # each clause is substantive (avoids splitting "due diligence" style phrases).
    parts = [p for p in parts if len(p.split()) >= 2]
    if len(parts) >= 2:
        return parts
    return []


def transform_query(
    query: str, history: list[dict], cfg: Mapping[str, Any] | None = None
) -> TransformedQuery:
    """Apply the configured transforms. ``cfg`` is the ``retrieval.transform``
    sub-config; absent keys default to enabled rewrite/multi_query/decompose and
    disabled HyDE (HyDE needs a generator, off in the deterministic CI path)."""
    cfg = cfg or {}
    do_rewrite = cfg.get("rewrite", True)
    do_multi = cfg.get("multi_query", True)
    do_decompose = cfg.get("decompose", True)
    do_hyde = cfg.get("hyde", False)

    original = _normalize(query)
    used: list[str] = []

    rewritten = original
    if do_rewrite:
        rewritten = _rewrite(original, history or [])
        if rewritten != original:
            used.append("rewrite")

    subqueries: list[str] = []
    if do_decompose:
        subqueries = _decompose(rewritten)
        if subqueries:
            used.append("decompose")

    if do_multi:
        used.append("multi_query")

    if do_hyde:
        used.append("hyde")

    return TransformedQuery(
        original=original,
        rewritten=rewritten,
        subqueries=subqueries,
        used=used,
    )


def expand_for_retrieval(
    transformed: TransformedQuery, cfg: Mapping[str, Any] | None = None
) -> list[str]:
    """Return the full list of query strings to retrieve, each under the SAME
    access filter (G-14). Decomposed subqueries take priority; otherwise the
    rewritten query plus multi-query variants. HyDE adds a hypothetical-answer
    string for dense recall when enabled."""
    cfg = cfg or {}
    queries: list[str]
    if transformed.subqueries:
        queries = list(transformed.subqueries)
    elif cfg.get("multi_query", True):
        queries = _multi_query(transformed.rewritten)
    else:
        queries = [transformed.rewritten]

    if cfg.get("hyde", False):
        queries.append(_normalize(_HYDE_TEMPLATE.format(q=transformed.rewritten)))

    out: list[str] = []
    for q in queries:
        nq = _normalize(q)
        if nq and nq not in out:
            out.append(nq)
    return out


__all__ = ["TransformedQuery", "transform_query", "expand_for_retrieval"]
