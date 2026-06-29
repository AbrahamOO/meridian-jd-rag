"""Retrieval pipeline (contracts.md section 3).

Security-critical module. The access pre-filter (retrieval/access.py) runs FIRST
and is applied INSIDE the candidate query so disallowed chunks are never scored,
ranked, reranked, assembled, or cited. Everything downstream operates only on
access-filtered candidates. Fail-closed on unknown role or missing metadata.
"""

from __future__ import annotations

from retrieval.access import build_access_filter, resolve_access
from retrieval.assemble import assemble_context
from retrieval.citations import validate_citations
from retrieval.hybrid import hybrid_retrieve
from retrieval.rerank import rerank_candidates
from retrieval.transform import TransformedQuery, transform_query

__all__ = [
    "resolve_access",
    "build_access_filter",
    "hybrid_retrieve",
    "transform_query",
    "TransformedQuery",
    "rerank_candidates",
    "assemble_context",
    "validate_citations",
]
