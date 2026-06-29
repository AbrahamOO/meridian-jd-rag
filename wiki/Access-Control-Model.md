# Access-Control Model

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist.

---

Meridian J.D. RAG enforces attribute-based access control (ABAC) in the SQL `WHERE` clause before any chunk is scored, is fail-closed by design, and re-validates access at citation time.

---

## Attribute-Based Access Control: how the model works

Access is determined by the conjunction of two attributes stored on every chunk:

- `classification`: the sensitivity level of the document (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`).
- `allowed_roles`: the explicit set of personas permitted to see this document.

Both must hold. Clearance level alone never grants access; `allowed_roles` still gates regardless of how high a persona's ceiling is.

### Why enforce access in SQL rather than after retrieval?

A post-retrieval filter is a single point of failure. If it has a bug, disallowed content reaches the generator. Pre-scoring enforcement removes that failure mode entirely: disallowed chunks never enter the candidate set, so there is nothing to filter in a second pass. The SQL fragment is AND-ed into both the pgvector dense query and the BM25 sparse query. For an `UNKNOWN_ROLE` or a `match_none` decision, the fragment collapses to `FALSE`, which yields zero rows. The chunks are never scored, never ranked, never assembled.

---

## Role-based clearance levels: the 7 canonical personas

| Persona | Department | Clearance ceiling | Permitted classifications |
| --- | --- | --- | --- |
| `OPERATIONS_ANALYST` | Operations | INTERNAL | PUBLIC, INTERNAL |
| `BRANCH_STAFF` | Retail | INTERNAL | PUBLIC, INTERNAL |
| `FINANCE_CONTROLLER` | Finance | CONFIDENTIAL | PUBLIC, INTERNAL, CONFIDENTIAL |
| `SOFTWARE_ENGINEER` | Technology | CONFIDENTIAL | PUBLIC, INTERNAL, CONFIDENTIAL |
| `RISK_ANALYST` | Risk | CONFIDENTIAL | PUBLIC, INTERNAL, CONFIDENTIAL |
| `COMPLIANCE_OFFICER` | Compliance | CONFIDENTIAL | PUBLIC, INTERNAL, CONFIDENTIAL |
| `SECURITY_ARCHITECT` | Security | RESTRICTED | PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED |

Any role string not in this table is an `UNKNOWN_ROLE`. `resolve_access(unknown)` returns `allowed=False`, `build_access_filter` returns `{"match_none": True}` (SQL `FALSE`), and zero chunks are scored. The access-boundary string is returned and the audit record is written. There is no fallback to a least-privilege role.

---

## Retrieval-time access control: enforcement in code

The enforcement chain lives in [`retrieval/access.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/retrieval/access.py):

```python
def resolve_access(role: str) -> AccessDecision:
    if role not in CANONICAL_PERSONAS:
        return AccessDecision(role=role, permitted_classifications=set(), allowed=False, reason="unknown_role")
    return AccessDecision(role=role, permitted_classifications=set(PERMITTED_CLASSIFICATIONS[role]), allowed=True, reason="ok")

def build_access_filter(decision: AccessDecision, *, active_strategy: str) -> dict:
    if not decision.allowed:
        return {"match_none": True, "chunk_strategy": active_strategy}
    return {
        "allowed_roles_contains": decision.role,
        "classification_in": sorted(decision.permitted_classifications),
        "chunk_strategy": active_strategy,
    }

def access_sql_where(access_filter: Mapping[str, Any]) -> tuple[str, dict]:
    if access_filter.get("match_none"):
        return "FALSE", {}
    fragment = (
        "(%(acl_role)s = ANY(allowed_roles) "
        "AND classification = ANY(%(acl_classes)s) "
        "AND chunk_strategy = %(acl_strategy)s "
        "AND allowed_roles IS NOT NULL AND classification IS NOT NULL)"
    )
    return fragment, params
```

In the CI file-index path (no Postgres), the identical logic runs as `chunk_is_visible(record, access_filter)`, a pure Python function that applies the same AND check before any scoring.

---

## Citation re-validation: no leak through citations

Access is enforced twice: at retrieval (pre-scoring) and at citation time via output_guardrail (G-04).

The citation re-validation strips any citation the generator produced that:

(a) references a `doc_id` not present in the assembled context, OR  
(b) would fail the requesting role's access filter.

If stripping a citation leaves an answer claim uncited, the output_guardrail discards the entire answer and returns the insufficient-context boundary string. The system never emits an uncited claim.

This closes the hallucinated-citation attack vector. Even if a model hallucinated a reference to `MJD-SEC-0002` (RESTRICTED, `SECURITY_ARCHITECT` only) while generating an answer for an `OPERATIONS_ANALYST`, the output_guardrail would strip that citation and force abstention: `MJD-SEC-0002` is not in the assembled context and would fail the OA access filter.

---

## Access boundary examples

These boundaries are each proved by [`scripts/prove_access_control.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/scripts/prove_access_control.py) (exit 0, 104 checks, 0 leaks):

**RESTRICTED content:**

- `MJD-SEC-0002` (Cryptographic Standard, RESTRICTED, SA only): invisible to `OPERATIONS_ANALYST`, `SOFTWARE_ENGINEER`, `COMPLIANCE_OFFICER`, `RISK_ANALYST`, `FINANCE_CONTROLLER`, `BRANCH_STAFF`. Only `SECURITY_ARCHITECT` can read it.
- `MJD-SEC-0004` (Network Segmentation and Zero Trust, RESTRICTED, SA only): same invisibility.
- `MJD-SEC-0010` (Privileged Access Management, RESTRICTED, SA only): same.

**CONFIDENTIAL AML content: clearance alone is not enough:**

- `MJD-CMP-0001` (BSA/AML Program Policy, CONFIDENTIAL, CO + RA only): invisible to `SOFTWARE_ENGINEER` even though SE clears CONFIDENTIAL. SE is not in `allowed_roles`. Invisible to `BRANCH_STAFF` (fails ceiling AND roles).
- `MJD-CMP-0002` (SAR Filing, CONFIDENTIAL, CO + RA only): same.

**CONFIDENTIAL technology content:**

- `MJD-TEC-0003` (OAuth2/OIDC Standard, CONFIDENTIAL, SE + SA only): invisible to `COMPLIANCE_OFFICER` and `FINANCE_CONTROLLER` despite their CONFIDENTIAL clearance. They are not in `allowed_roles`.
- `MJD-TEC-0004` (Secrets and Key Management, CONFIDENTIAL, SE + SA only): same.

**Deliberate cross-role allows: access is not department-equals-role:**

- `SOFTWARE_ENGINEER` can read `MJD-RSK-0002` (Model Risk, SR 11-7): engineers validate models.
- `RISK_ANALYST` can read `MJD-OPS-0002` and `MJD-OPS-0003` (CDD/EDD): risk consumes ops procedures.
- `SECURITY_ARCHITECT` can read `MJD-CMP-0005` (GLBA Safeguards) and `MJD-FIN-0005` (Audit Evidence): recursive touch.
- All 7 personas can read `MJD-SEC-0008` (Data Classification, INTERNAL): everyone must know how to classify data.

---

## Full access table: all 51 documents

Complete per-document access assignments are in [`docs/contracts.md`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/docs/contracts.md) section 11.2. Summary by department:

**OPERATIONS (9 docs):** Mostly INTERNAL, broad operational audience. EDD and OFAC escalated to CONFIDENTIAL to exclude `BRANCH_STAFF`. `MJD-OPS-0009` is the superseded predecessor of `MJD-OPS-0007` (near-duplicate pair test fixture).

**COMPLIANCE (8 docs):** CONFIDENTIAL AML spine (BSA/AML, SAR, CTR monitoring, Fair Lending). Engineers and branch staff doubly excluded. GLBA Safeguards (0005) deliberately INTERNAL and lists SE for recursive touch.

**TECHNOLOGY (9 docs):** INTERNAL engineering standards. Auth (0003) and Secrets (0004) escalated to CONFIDENTIAL, SE + SA only. Cloud governance and change management include RA for risk oversight.

**SECURITY (10 docs):** Three RESTRICTED documents (Crypto 0002, Zero Trust 0004, PAM 0010) visible only to SA. Master InfoSec Policy (0001) is CONFIDENTIAL and broadly co-owned.

**RISK (7 docs):** CONFIDENTIAL risk frameworks. SE can read Model Risk (0002) for model validation work. FC reads Credit/Stress/Capital. Fraud (0007) includes SA and OA.

**FINANCE (5 docs):** INTERNAL accounting ops, two CONFIDENTIAL (Regulatory Reporting, Audit Evidence). SA co-owns Audit Evidence (recursive touch).

**RETAIL (3 docs):** INTERNAL, centered on `BRANCH_STAFF` and OA. Vault (0002) includes SA (physical security). Complaints (0003) includes CO.

---

## Fail-closed posture

Every ambiguity resolves toward denial:

- Unknown role: denies.
- Missing `classification` or `allowed_roles` on a chunk at retrieval time: treated as invisible (G-06b).
- Database error applying the access filter: query fails closed with a boundary, never serves unfiltered results (G-19).
- Hallucinated citation to an out-of-scope doc: stripped and answer forced to boundary (G-04).
- Duplicate `doc_id` at ingestion: all copies rejected, no index written (G-13).

The config key `access.fail_closed` is hardwired `true`. The config loader raises an error if any configuration attempts to set it `false`.

---

## Access-control proof

The proof battery ([`scripts/prove_access_control.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/scripts/prove_access_control.py)) runs 104 cross-department access checks across all 7 canonical personas plus one unknown role (`DBA_ROOT`). Verified result (2026-06-29):

```text
PERSONA               CHECKS   LEAKS   MISSING_REQ  RESULT
BRANCH_STAFF              14       0             0  PASS
COMPLIANCE_OFFICER        14       0             0  PASS
DBA_ROOT                   1       0             0  PASS
FINANCE_CONTROLLER        14       0             0  PASS
OPERATIONS_ANALYST        15       0             0  PASS
RISK_ANALYST              14       0             0  PASS
SECURITY_ARCHITECT        15       0             0  PASS
SOFTWARE_ENGINEER         17       0             0  PASS
Total checks: 104  total leaks: 0  entitlement leaks: 0
OVERALL: PASS (zero leaks)
```

This runs as part of the CI pipeline (`make prove-access`). Any leak is a release blocker.

---

## FAQ

**Why enforce access in SQL instead of after retrieval?**
Post-retrieval filters are a single point of failure: one bug and disallowed content reaches the generator. Enforcing in SQL means disallowed chunks are absent from the query result entirely. There is nothing to filter downstream.

**What happens for an unknown role?**
`resolve_access` returns `allowed=False`. `build_access_filter` returns `{"match_none": True}`, which becomes SQL `FALSE`. Zero chunks are scored. The audit record is written. No fallback to any least-privilege role.

**Does clearance level alone grant access?**
No. Both `classification` and `allowed_roles` must pass. A `SOFTWARE_ENGINEER` clears CONFIDENTIAL but cannot read `MJD-CMP-0001` because SE is not in its `allowed_roles`.
