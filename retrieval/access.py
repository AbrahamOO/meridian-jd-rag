"""Access pre-filter (contracts.md section 3.1, section 11; gap-register G-06, G-07).

The most security-critical code in the system. Two functions:

- ``resolve_access(role)`` maps a requesting role to its permitted classifications
  (contract 11.1). An unknown role (anything outside the 7 canonical personas)
  returns ``allowed=False`` and reason ``unknown_role``. FAIL CLOSED.
- ``build_access_filter(decision)`` returns the predicate fragment applied INSIDE
  the candidate query (the SQL ``WHERE`` clause for Postgres, an equivalent
  pre-scoring filter step for the file index). Disallowed chunks are therefore
  never scored, ranked, reranked, assembled, or cited. For an unknown role the
  predicate is ``{"match_none": true}`` which matches zero rows.

A chunk is visible to ``role`` IFF ``role IN allowed_roles`` AND
``classification IN permitted_classifications``. Both conditions, AND, never OR.
Belt-and-suspenders (G-06b): a chunk somehow stored with null/empty
allowed_roles or classification is treated as invisible.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.models import (
    CANONICAL_PERSONAS,
    PERMITTED_CLASSIFICATIONS,
    AccessDecision,
)


def resolve_access(role: str) -> AccessDecision:
    """Resolve a requesting role to an AccessDecision (contract 3.1, 11.1).

    Unknown role (not one of the 7 canonical personas, including empty/None-like
    strings) -> ``allowed=False``, ``reason="unknown_role"``, empty permitted set.
    This is the fail-closed entry point: an unknown role can retrieve nothing.
    """
    normalized = role if isinstance(role, str) else ""
    if normalized not in CANONICAL_PERSONAS:
        return AccessDecision(
            role=normalized,
            permitted_classifications=set(),
            allowed=False,
            reason="unknown_role",
        )
    return AccessDecision(
        role=normalized,
        permitted_classifications=set(PERMITTED_CLASSIFICATIONS[normalized]),
        allowed=True,
        reason="ok",
    )


def build_access_filter(decision: AccessDecision, *, active_strategy: str) -> dict:
    """Return the predicate fragment applied INSIDE the candidate query.

    Shape (contract 3.1):
        {"allowed_roles_contains": role,
         "classification_in": [...permitted...],
         "chunk_strategy": active_strategy}

    For UNKNOWN_ROLE (``allowed=False``) this returns a match-none predicate
    ``{"match_none": true}`` so zero chunks are scored. The match-none predicate
    still carries the strategy so callers can log it, but ``match_none`` short
    circuits all matching.
    """
    if not decision.allowed:
        return {"match_none": True, "chunk_strategy": active_strategy}
    return {
        "allowed_roles_contains": decision.role,
        "classification_in": sorted(decision.permitted_classifications),
        "chunk_strategy": active_strategy,
    }


def chunk_is_visible(record: Mapping[str, Any], access_filter: Mapping[str, Any]) -> bool:
    """Apply the access filter to one stored chunk record (file-index path).

    This is the pre-scoring filter step that mirrors the Postgres ``WHERE`` clause.
    It runs BEFORE any scoring so disallowed chunks never enter the candidate set.

    Fail-closed semantics:
    - ``match_none`` -> always False (unknown role).
    - Wrong ``chunk_strategy`` -> False (strategy isolation, contract 2.2).
    - Missing/empty ``allowed_roles`` or ``classification`` -> False (G-06b).
    - role not in allowed_roles -> False.
    - classification not in permitted set -> False.
    Visible only when BOTH the role-membership AND the classification checks pass.
    """
    if access_filter.get("match_none"):
        return False

    want_strategy = access_filter.get("chunk_strategy")
    if want_strategy is not None and record.get("chunk_strategy") != want_strategy:
        return False

    allowed_roles = record.get("allowed_roles")
    classification = record.get("classification")
    # Belt-and-suspenders: null/empty access metadata is invisible (G-06b).
    if not allowed_roles or not classification:
        return False

    role = access_filter.get("allowed_roles_contains")
    permitted = access_filter.get("classification_in") or []
    role_ok = role in allowed_roles
    class_ok = classification in permitted
    # AND, never OR (contract 3.1 hard rule).
    return bool(role_ok and class_ok)


def access_sql_where(access_filter: Mapping[str, Any]) -> tuple[str, dict]:
    """Build the Postgres ``WHERE`` fragment + params for the pgvector path.

    Returned as a fragment to be AND-ed into the candidate query so disallowed
    chunks are never scored. For ``match_none`` the fragment is ``FALSE`` which
    yields zero rows. This is the in-query enforcement the contract mandates;
    the file-index path uses ``chunk_is_visible`` for the equivalent step.
    """
    if access_filter.get("match_none"):
        return "FALSE", {}
    params: dict[str, Any] = {
        "acl_role": access_filter["allowed_roles_contains"],
        "acl_classes": access_filter["classification_in"],
        "acl_strategy": access_filter["chunk_strategy"],
    }
    fragment = (
        "(%(acl_role)s = ANY(allowed_roles) "
        "AND classification = ANY(%(acl_classes)s) "
        "AND chunk_strategy = %(acl_strategy)s "
        "AND allowed_roles IS NOT NULL AND classification IS NOT NULL)"
    )
    return fragment, params


__all__ = [
    "resolve_access",
    "build_access_filter",
    "chunk_is_visible",
    "access_sql_where",
]
