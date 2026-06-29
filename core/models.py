"""Shared contract models (docs/contracts.md sections 2, 3, 5).

ALL cross-component dataclasses and TypedDicts live here so retrieval,
generation, evals, and api import them from one place. Field names and types
match the contract exactly and are case-sensitive. Frozen dataclasses are used
for immutable records; QueryState is a TypedDict because LangGraph nodes mutate
a shared state dict.

The canonical persona set and the persona-to-clearance mapping (contract 11.1)
also live here so the access layer and ingestion validation share one definition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict

# Re-exported boundary strings so generation/api import them from core without
# reaching into providers.base directly.
from providers.base import (  # noqa: F401
    ACCESS_BOUNDARY_STRING,
    INSUFFICIENT_CONTEXT_STRING,
)

# --- Canonical enums and personas (contracts section 2, 11) -----------------

CANONICAL_PERSONAS: frozenset[str] = frozenset(
    {
        "OPERATIONS_ANALYST",
        "COMPLIANCE_OFFICER",
        "SOFTWARE_ENGINEER",
        "SECURITY_ARCHITECT",
        "RISK_ANALYST",
        "FINANCE_CONTROLLER",
        "BRANCH_STAFF",
    }
)

DEPARTMENTS: frozenset[str] = frozenset(
    {
        "OPERATIONS",
        "COMPLIANCE",
        "TECHNOLOGY",
        "SECURITY",
        "RISK",
        "FINANCE",
        "RETAIL",
    }
)

DOC_TYPES: frozenset[str] = frozenset(
    {"POLICY", "STANDARD", "PROCEDURE", "RUNBOOK", "GUIDELINE", "REFERENCE"}
)

CLASSIFICATIONS: frozenset[str] = frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"})

# Department name to doc-id code (contracts conventions block).
DEPARTMENT_CODE: dict[str, str] = {
    "OPERATIONS": "OPS",
    "COMPLIANCE": "CMP",
    "TECHNOLOGY": "TEC",
    "SECURITY": "SEC",
    "RISK": "RSK",
    "FINANCE": "FIN",
    "RETAIL": "RET",
}

# Persona to permitted_classifications (contract 11.1). The AND of this set and
# the chunk's allowed_roles is what grants access.
PERMITTED_CLASSIFICATIONS: dict[str, frozenset[str]] = {
    "OPERATIONS_ANALYST": frozenset({"PUBLIC", "INTERNAL"}),
    "BRANCH_STAFF": frozenset({"PUBLIC", "INTERNAL"}),
    "FINANCE_CONTROLLER": frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL"}),
    "SOFTWARE_ENGINEER": frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL"}),
    "RISK_ANALYST": frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL"}),
    "COMPLIANCE_OFFICER": frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL"}),
    "SECURITY_ARCHITECT": frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"}),
}


# --- Document metadata (contract 2.1) ---------------------------------------


@dataclass(frozen=True)
class DocumentMetadata:
    """Validated document header. Produced by ingestion/metadata.py after the
    fail-closed checks in contract 2.1 / gap-register G-06."""

    doc_id: str
    title: str
    department: str
    doc_type: str
    classification: str
    owner_role: str
    allowed_roles: list[str]
    effective_date: str  # YYYY-MM-DD
    version: str  # semver
    review_cycle_months: int
    regulatory_refs: list[str]
    supersedes: str | None
    entity_status: str  # literal "FICTIONAL"


# --- Chunk record (contract 2.2) --------------------------------------------


@dataclass(frozen=True)
class Chunk:
    chunk_id: str  # "{doc_id}::c{NNNN}"
    doc_id: str
    parent_id: str  # "{doc_id}::p{NNNN}"
    title: str
    department: str
    doc_type: str
    classification: str  # inherited from document
    owner_role: str
    allowed_roles: list[str]  # inherited, the access backbone
    effective_date: str
    version: str
    supersedes: str | None
    is_superseded: bool
    entity_status: str
    section_path: str  # "3 > 3.2 > 3.2.1"
    text: str  # child body WITHOUT the contextual header
    embed_text: str  # contextual header + text, the embedded string
    parent_text: str  # full parent-section text, for generation
    char_start: int
    char_end: int
    token_count: int  # token count of `text`
    content_hash: str  # sha256 of source doc content
    chunk_strategy: str  # "production" | "naive"


# --- Access decision (contract 3.1) -----------------------------------------


@dataclass(frozen=True)
class AccessDecision:
    role: str
    permitted_classifications: set[str]
    allowed: bool  # false only for UNKNOWN_ROLE
    reason: str  # "ok" | "unknown_role"


# --- Retrieval candidate (contract 3.2) -------------------------------------


@dataclass(frozen=True)
class Candidate:
    chunk: Chunk
    dense_rank: int | None
    sparse_rank: int | None
    rrf_score: float
    dense_score: float | None  # cosine similarity
    sparse_score: float | None  # BM25/ts_rank score


# --- Assembled context (contract 3.5) ---------------------------------------


@dataclass(frozen=True)
class ContextBlock:
    parent_id: str
    doc_id: str
    title: str
    section_path: str
    version: str
    text: str  # parent-section text
    is_superseded: bool


@dataclass(frozen=True)
class AssembledContext:
    blocks: list[ContextBlock]
    total_tokens: int
    dropped_for_budget: list[str]  # parent_ids dropped to fit budget


# --- Citation (contract 3.6) ------------------------------------------------


class Citation(TypedDict):
    """The only citation shape the UI and generator emit."""

    doc_id: str
    title: str
    section_path: str
    version: str


# --- Query graph state (contract 5) -----------------------------------------


class TokenUsage(TypedDict, total=False):
    prompt: int
    completion: int
    embed: int


class QueryState(TypedDict, total=False):
    trace_id: str
    role: str
    query: str
    history: list[dict]
    access: AccessDecision
    transformed: object  # TransformedQuery, owned by retrieval; loosely typed here
    candidates: list[Candidate]
    reranked: list[Candidate]
    context: AssembledContext
    answer: str
    citations: list[Citation]
    boundary_triggered: bool
    boundary_reason: str
    guardrail_flags: list[str]
    latency_ms: float
    cost_usd: float
    tokens: TokenUsage
    error: str


__all__ = [
    "ACCESS_BOUNDARY_STRING",
    "INSUFFICIENT_CONTEXT_STRING",
    "CANONICAL_PERSONAS",
    "DEPARTMENTS",
    "DOC_TYPES",
    "CLASSIFICATIONS",
    "DEPARTMENT_CODE",
    "PERMITTED_CLASSIFICATIONS",
    "DocumentMetadata",
    "Chunk",
    "AccessDecision",
    "Candidate",
    "ContextBlock",
    "AssembledContext",
    "Citation",
    "TokenUsage",
    "QueryState",
]

# `field` is imported for downstream dataclass defaults; referenced to satisfy
# linters even though the contract dataclasses above need no mutable defaults.
_ = field
