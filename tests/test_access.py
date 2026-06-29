"""Access pre-filter unit tests (contracts.md 3.1, 11; gap-register G-06, G-07).

These tests fail LOUDLY if the access filter ever fails open. They prove:
- unknown role -> allowed=False -> match-none predicate -> zero visible chunks,
- AND-not-OR semantics (clearance alone never grants; allowed_roles alone never
  grants),
- RESTRICTED invisible to every non-SECURITY_ARCHITECT role,
- CONFIDENTIAL-but-not-in-allowed_roles is denied (SOFTWARE_ENGINEER vs AML),
- belt-and-suspenders: null/empty access metadata is invisible (G-06b).
"""

from __future__ import annotations

import pytest

from core.models import PERMITTED_CLASSIFICATIONS
from retrieval.access import (
    access_sql_where,
    build_access_filter,
    chunk_is_visible,
    resolve_access,
)


@pytest.fixture(autouse=True)
def _ci_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MJD_PROFILE", "ci")


def _chunk(classification: str, allowed_roles, strategy: str = "production") -> dict:
    return {
        "classification": classification,
        "allowed_roles": list(allowed_roles),
        "chunk_strategy": strategy,
    }


# --- resolve_access ---------------------------------------------------------


@pytest.mark.parametrize("role", sorted(PERMITTED_CLASSIFICATIONS))
def test_resolve_known_roles_allowed(role: str) -> None:
    decision = resolve_access(role)
    assert decision.allowed is True
    assert decision.reason == "ok"
    assert decision.permitted_classifications == set(PERMITTED_CLASSIFICATIONS[role])


@pytest.mark.parametrize("role", ["", "ROOT", "admin", "OPERATIONS", "software_engineer"])
def test_resolve_unknown_role_fails_closed(role: str) -> None:
    decision = resolve_access(role)
    assert decision.allowed is False
    assert decision.reason == "unknown_role"
    assert decision.permitted_classifications == set()


def test_resolve_non_string_role_fails_closed() -> None:
    decision = resolve_access(None)  # type: ignore[arg-type]
    assert decision.allowed is False
    assert decision.reason == "unknown_role"


# --- build_access_filter ----------------------------------------------------


def test_unknown_role_builds_match_none() -> None:
    decision = resolve_access("ROOT")
    flt = build_access_filter(decision, active_strategy="production")
    assert flt.get("match_none") is True


def test_known_role_filter_shape() -> None:
    decision = resolve_access("SECURITY_ARCHITECT")
    flt = build_access_filter(decision, active_strategy="production")
    assert flt["allowed_roles_contains"] == "SECURITY_ARCHITECT"
    assert "RESTRICTED" in flt["classification_in"]
    assert flt["chunk_strategy"] == "production"
    assert "match_none" not in flt


# --- chunk_is_visible: fail-closed core -------------------------------------


def test_match_none_never_visible() -> None:
    decision = resolve_access("UNKNOWN")
    flt = build_access_filter(decision, active_strategy="production")
    chunk = _chunk("PUBLIC", ["SECURITY_ARCHITECT", "SOFTWARE_ENGINEER"])
    assert chunk_is_visible(chunk, flt) is False


def test_and_not_or_clearance_without_role_denied() -> None:
    # FINANCE_CONTROLLER clears CONFIDENTIAL but is NOT in allowed_roles.
    flt = build_access_filter(resolve_access("FINANCE_CONTROLLER"), active_strategy="production")
    aml = _chunk("CONFIDENTIAL", ["COMPLIANCE_OFFICER", "RISK_ANALYST"])
    assert chunk_is_visible(aml, flt) is False


def test_and_not_or_role_without_clearance_denied() -> None:
    # A role listed in allowed_roles but lacking the clearance ceiling is denied.
    # OPERATIONS_ANALYST clears only PUBLIC/INTERNAL; a CONFIDENTIAL chunk listing
    # OA must still be denied (AND semantics).
    flt = build_access_filter(resolve_access("OPERATIONS_ANALYST"), active_strategy="production")
    conf = _chunk("CONFIDENTIAL", ["OPERATIONS_ANALYST"])
    assert chunk_is_visible(conf, flt) is False
    # But an INTERNAL chunk listing OA is visible.
    internal = _chunk("INTERNAL", ["OPERATIONS_ANALYST"])
    assert chunk_is_visible(internal, flt) is True


def test_software_engineer_denied_aml_confidential() -> None:
    # Headline: SE clears CONFIDENTIAL but is not in the AML allowed_roles.
    flt = build_access_filter(resolve_access("SOFTWARE_ENGINEER"), active_strategy="production")
    aml = _chunk("CONFIDENTIAL", ["COMPLIANCE_OFFICER", "RISK_ANALYST"])
    assert chunk_is_visible(aml, flt) is False


@pytest.mark.parametrize(
    "role",
    [
        "OPERATIONS_ANALYST",
        "COMPLIANCE_OFFICER",
        "SOFTWARE_ENGINEER",
        "RISK_ANALYST",
        "FINANCE_CONTROLLER",
        "BRANCH_STAFF",
    ],
)
def test_restricted_invisible_to_every_non_security_architect(role: str) -> None:
    flt = build_access_filter(resolve_access(role), active_strategy="production")
    # RESTRICTED crypto standard lists only SA; even if it somehow listed the role,
    # the classification ceiling denies it.
    restricted = _chunk("RESTRICTED", ["SECURITY_ARCHITECT", role])
    assert chunk_is_visible(restricted, flt) is False


def test_restricted_visible_to_security_architect() -> None:
    flt = build_access_filter(resolve_access("SECURITY_ARCHITECT"), active_strategy="production")
    restricted = _chunk("RESTRICTED", ["SECURITY_ARCHITECT"])
    assert chunk_is_visible(restricted, flt) is True


def test_null_metadata_invisible_g06b() -> None:
    flt = build_access_filter(resolve_access("SECURITY_ARCHITECT"), active_strategy="production")
    assert chunk_is_visible(_chunk("RESTRICTED", []), flt) is False  # empty roles
    assert chunk_is_visible(_chunk("", ["SECURITY_ARCHITECT"]), flt) is False  # empty class
    assert (
        chunk_is_visible(
            {"allowed_roles": ["SECURITY_ARCHITECT"], "chunk_strategy": "production"}, flt
        )
        is False
    )  # missing classification key


def test_wrong_strategy_invisible() -> None:
    flt = build_access_filter(resolve_access("SECURITY_ARCHITECT"), active_strategy="production")
    naive = _chunk("RESTRICTED", ["SECURITY_ARCHITECT"], strategy="naive")
    assert chunk_is_visible(naive, flt) is False


# --- SQL where (postgres path) ----------------------------------------------


def test_access_sql_where_match_none_is_false() -> None:
    flt = build_access_filter(resolve_access("ROOT"), active_strategy="production")
    fragment, params = access_sql_where(flt)
    assert fragment == "FALSE"
    assert params == {}


def test_access_sql_where_known_role_is_and_predicate() -> None:
    flt = build_access_filter(resolve_access("SOFTWARE_ENGINEER"), active_strategy="production")
    fragment, params = access_sql_where(flt)
    assert "ANY(allowed_roles)" in fragment
    assert "classification = ANY" in fragment
    assert " AND " in fragment  # AND, never OR
    assert "OR" not in fragment.replace("FOR", "")
    assert params["acl_role"] == "SOFTWARE_ENGINEER"
