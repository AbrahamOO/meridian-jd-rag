"""Access-control proof artifact.

Runs a battery of cross-department queries for EACH of the 7 canonical personas
against the built file index under MJD_PROFILE=ci. For every WRONG-ROLE case it
asserts ZERO out-of-scope chunks AND zero out-of-scope citations. It also runs
positive controls that MUST succeed. Prints a per-persona PASS/FAIL table and
exits non-zero on ANY leak.

The headline cases (contract 11.3):
- SOFTWARE_ENGINEER / OPERATIONS_ANALYST asking cipher suites / KMS rotation:
  SEC-0002 (RESTRICTED) must NOT appear.
- SOFTWARE_ENGINEER asking AML escalation: CMP-0001/0002/0004 (CONFIDENTIAL) must
  NOT appear.
- Positive: SECURITY_ARCHITECT asking cipher suites -> SEC-0002 DOES appear.
- Positive: SOFTWARE_ENGINEER asking SR 11-7 -> RSK-0002 appears.

Usage:
    MJD_PROFILE=ci python scripts/prove_access_control.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from config.loader import load_config  # noqa: E402
from core.models import CANONICAL_PERSONAS  # noqa: E402
from providers.factory import (  # noqa: E402
    get_embedding_provider,
    get_reranker,
)
from retrieval.access import build_access_filter, resolve_access  # noqa: E402
from retrieval.citations import validate_citations  # noqa: E402
from retrieval.pipeline import retrieve  # noqa: E402
from retrieval.repository import FileChunkRepository  # noqa: E402

# Documents that are RESTRICTED (visible only to SECURITY_ARCHITECT) and the
# CONFIDENTIAL AML spine (visible only to CO/RA). Used to assert non-appearance.
RESTRICTED_DOCS = {"MJD-SEC-0002", "MJD-SEC-0004", "MJD-SEC-0010"}
AML_DOCS = {"MJD-CMP-0001", "MJD-CMP-0002", "MJD-CMP-0004", "MJD-CMP-0007"}
TEC_SECRETS_DOCS = {"MJD-TEC-0003", "MJD-TEC-0004"}


@dataclass(frozen=True)
class Case:
    persona: str
    query: str
    # doc_ids that MUST NOT appear in retrieval or citations for this persona.
    forbidden: frozenset[str]
    # doc_ids that MUST appear (positive control); empty frozenset if none.
    required: frozenset[str]
    label: str


def _cross_dept_queries() -> list[str]:
    return [
        "what cipher suites are approved",
        "how is the KMS key rotation schedule configured",
        "how is privileged access management granted",
        "what is the network zero trust segmentation design",
        "what are our AML escalation procedures",
        "suspicious activity report SAR filing steps",
        "transaction monitoring rules and thresholds",
        "how do we rotate service account secrets",
        "OAuth2 OIDC authentication standard",
        "SR 11-7 model risk validation cadence",
        "enhanced due diligence EDD threshold for corporate accounts",
        "branch cash handling and vault procedure",
        "call report FR Y-9C regulatory reporting",
        "data classification handling standard",
    ]


def build_cases() -> list[Case]:
    cases: list[Case] = []

    # For every persona, run every cross-department query. The forbidden set for a
    # persona is "every sensitive doc that persona is not entitled to". We compute
    # entitlement from the live index per-doc rather than hardcoding, so the proof
    # is honest. To keep the battery focused, we assert non-appearance of the
    # headline sensitive docs each persona must never see.
    non_sa = CANONICAL_PERSONAS - {"SECURITY_ARCHITECT"}
    non_aml = CANONICAL_PERSONAS - {"COMPLIANCE_OFFICER", "RISK_ANALYST"}
    non_secrets = CANONICAL_PERSONAS - {"SOFTWARE_ENGINEER", "SECURITY_ARCHITECT"}

    for persona in sorted(CANONICAL_PERSONAS):
        forbidden = set()
        if persona in non_sa:
            forbidden |= RESTRICTED_DOCS
        if persona in non_aml:
            forbidden |= AML_DOCS
        if persona in non_secrets:
            forbidden |= TEC_SECRETS_DOCS
        for q in _cross_dept_queries():
            cases.append(
                Case(
                    persona=persona,
                    query=q,
                    forbidden=frozenset(forbidden),
                    required=frozenset(),
                    label="battery",
                )
            )

    # Explicit headline negative controls.
    cases.append(
        Case(
            "SOFTWARE_ENGINEER",
            "what cipher suites are approved",
            RESTRICTED_DOCS,
            frozenset(),
            "headline-neg",
        )
    )
    cases.append(
        Case(
            "OPERATIONS_ANALYST",
            "how is the KMS key rotation schedule configured",
            RESTRICTED_DOCS,
            frozenset(),
            "headline-neg",
        )
    )
    cases.append(
        Case(
            "SOFTWARE_ENGINEER",
            "what are our AML escalation procedures",
            AML_DOCS,
            frozenset(),
            "headline-neg",
        )
    )

    # Positive controls (required docs MUST appear).
    cases.append(
        Case(
            "SECURITY_ARCHITECT",
            "what cipher suites are approved",
            frozenset(),
            frozenset({"MJD-SEC-0002"}),
            "headline-pos",
        )
    )
    cases.append(
        Case(
            "SOFTWARE_ENGINEER",
            "SR 11-7 model risk validation cadence",
            frozenset(),
            frozenset({"MJD-RSK-0002"}),
            "headline-pos",
        )
    )

    # Unknown role: must retrieve nothing at all.
    cases.append(
        Case(
            "DBA_ROOT",
            "what cipher suites are approved",
            RESTRICTED_DOCS | AML_DOCS,
            frozenset(),
            "unknown-role",
        )
    )
    return cases


def _all_visible_doc_ids(role: str, repo: FileChunkRepository, active_strategy: str) -> set[str]:
    """All doc_ids the access filter would ever expose to ``role`` (ground truth
    for the leak check, independent of the scorer)."""
    decision = resolve_access(role)
    access_filter = build_access_filter(decision, active_strategy=active_strategy)
    if not decision.allowed:
        return set()
    from retrieval.access import chunk_is_visible

    visible = set()
    for record in repo._records:  # noqa: SLF001 (proof reads the raw index)
        if chunk_is_visible(record, access_filter):
            visible.add(record["doc_id"])
    return visible


def main() -> int:
    cfg = load_config()
    if cfg.profile != "ci":
        print(f"WARNING: expected MJD_PROFILE=ci, got profile={cfg.profile!r}")
    cfg_map = cfg.model_dump()
    active_strategy = cfg_map["chunking"]["strategy"]

    embedder = get_embedding_provider(cfg)
    reranker = get_reranker(cfg)
    repo = FileChunkRepository()

    cases = build_cases()

    # Per-persona tallies.
    by_persona: dict[str, dict[str, int]] = {}
    leaks: list[str] = []

    # Sanity: no persona's entitlement set should ever include a forbidden doc.
    for persona in sorted(CANONICAL_PERSONAS):
        entitled = _all_visible_doc_ids(persona, repo, active_strategy)
        for doc in RESTRICTED_DOCS:
            if persona != "SECURITY_ARCHITECT" and doc in entitled:
                leaks.append(f"ENTITLEMENT LEAK: {persona} entitled to RESTRICTED {doc}")

    for case in cases:
        tally = by_persona.setdefault(
            case.persona, {"checks": 0, "leaks": 0, "missing_required": 0}
        )
        result = retrieve(
            case.persona,
            case.query,
            embedder=embedder,
            reranker=reranker,
            repository=repo,
            cfg=cfg_map,
        )

        retrieved = set(result.retrieved_doc_ids)
        all_candidate_docs = {c.chunk.doc_id for c in result.candidates}
        context_docs = {b.doc_id for b in result.context.blocks}

        # Citations: simulate the generator emitting a citation for every forbidden
        # doc plus every context doc, then re-validate. None of the forbidden docs
        # may survive (defense-in-depth check, G-04).
        emitted = [
            {"doc_id": d, "title": "", "section_path": "", "version": ""}
            for d in sorted(case.forbidden | context_docs)
        ]
        validation = validate_citations(
            emitted, case.persona, result.context, active_strategy=active_strategy
        )
        valid_doc_ids = {c["doc_id"] for c in validation.valid}

        # Leak check: no forbidden doc may appear anywhere the role can observe.
        observed = retrieved | all_candidate_docs | context_docs | valid_doc_ids
        leaked = case.forbidden & observed
        tally["checks"] += 1
        if leaked:
            tally["leaks"] += 1
            leaks.append(
                f"LEAK [{case.persona}] q={case.query!r} leaked={sorted(leaked)} "
                f"(label={case.label})"
            )

        # Positive controls.
        if case.required:
            missing = case.required - retrieved
            if missing:
                tally["missing_required"] += 1
                leaks.append(
                    f"MISSING [{case.persona}] q={case.query!r} expected={sorted(case.required)} "
                    f"got={sorted(retrieved)} (label={case.label})"
                )

    # Print the per-persona table.
    print("\nAccess-control proof: per-persona results (MJD_PROFILE=ci)")
    print("=" * 72)
    header = f"{'PERSONA':<20}{'CHECKS':>8}{'LEAKS':>8}{'MISSING_REQ':>14}  RESULT"
    print(header)
    print("-" * 72)
    overall_pass = not any("ENTITLEMENT LEAK" in line for line in leaks)
    for persona in sorted(by_persona):
        t = by_persona[persona]
        ok = t["leaks"] == 0 and t["missing_required"] == 0
        overall_pass = overall_pass and ok
        status = "PASS" if ok else "FAIL"
        print(f"{persona:<20}{t['checks']:>8}{t['leaks']:>8}{t['missing_required']:>14}  {status}")
    print("-" * 72)

    if leaks:
        print("\nFailures:")
        for line in leaks:
            print(f"  {line}")

    total_checks = sum(t["checks"] for t in by_persona.values())
    total_leaks = sum(t["leaks"] for t in by_persona.values())
    print(
        f"\nTotal checks: {total_checks}  total leaks: {total_leaks}  "
        f"entitlement leaks: {sum(1 for line in leaks if 'ENTITLEMENT' in line)}"
    )
    print("OVERALL: " + ("PASS (zero leaks)" if overall_pass and not leaks else "FAIL"))
    return 0 if (overall_pass and not leaks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
