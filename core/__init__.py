"""Cross-component shared models for Meridian J.D. RAG.

This package is the single source of truth for the contract dataclasses and
TypedDicts that retrieval, generation, and the api layers all consume. Field
names and shapes are normative per docs/contracts.md and case-sensitive. Import
from here, never redefine these types locally.
"""

from __future__ import annotations

from core.models import (
    ACCESS_BOUNDARY_STRING,
    INSUFFICIENT_CONTEXT_STRING,
    AccessDecision,
    AssembledContext,
    Candidate,
    Chunk,
    Citation,
    ContextBlock,
    DocumentMetadata,
    QueryState,
)

__all__ = [
    "ACCESS_BOUNDARY_STRING",
    "INSUFFICIENT_CONTEXT_STRING",
    "AccessDecision",
    "AssembledContext",
    "Candidate",
    "Chunk",
    "Citation",
    "ContextBlock",
    "DocumentMetadata",
    "QueryState",
]
