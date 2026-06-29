# ADR-004: Fail-Closed Retrieval-Time ABAC

**Status:** Accepted
**Created: 2026-06-29**
**Last updated: 2026-06-29**

---

## Context

The system serves 7 employee personas with different document access rights. At minimum, four classification levels must be respected: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. RESTRICTED documents (cryptographic standards, PAM policy, zero-trust architecture) must be invisible to every persona except SECURITY_ARCHITECT.

Two design choices are available:

**Option A: Post-retrieval filtering.** Retrieve documents using semantic similarity, then filter the result set in Python based on the requesting role. This is simpler to implement but has a single point of failure: if the Python filter has a bug, out-of-scope content reaches the generator. The reranker also operates on the unfiltered set, potentially learning signal from documents the role should not see.

**Option B: Pre-scoring SQL WHERE clause.** Apply the access filter as a SQL WHERE clause inside the vector query. Disallowed chunks are never scored, never ranked, never seen by the reranker, never assembled, never cited. A Python filter runs at the output_guardrail as defense in depth, but the primary enforcement is structural.

For a financial policy system serving employees at different clearance levels, Option A is not acceptable. A post-filter bug would be invisible in logs (the chunks were retrieved and filtered, not absent). The attack is a code-review failure, not an observable event.

---

## Decision

Enforce access control as a SQL WHERE clause applied before any scoring (contracts.md section 3.1, `retrieval/access.py`):

**Primary enforcement:** `access_sql_where(access_filter)` returns a SQL fragment AND-ed into both the pgvector cosine distance query and the Postgres FTS query. For an authorized role, the fragment is: `acl_role = ANY(allowed_roles) AND classification = ANY(acl_classes) AND chunk_strategy = strategy AND allowed_roles IS NOT NULL AND classification IS NOT NULL`. For an unknown role (`match_none=True`), the fragment is `FALSE`, yielding zero rows.

**File-index equivalent:** In the CI path (no Postgres), `chunk_is_visible(record, access_filter)` applies the identical AND logic before any scoring in the Python file-index path. Verified by 104 cross-department access checks.

**Defense in depth:** The `output_guardrail` node re-validates every citation the generator produced against (a) the assembled context and (b) the role's access filter. A citation to an out-of-scope document is stripped even if it was hallucinated by the model (G-04).

**Fail-closed rules:**
- Unknown role: `match_none` predicate, zero chunks scored, access-boundary string returned, audit record written.
- Missing `classification` or `allowed_roles` on a chunk: treated as invisible (G-06b), both at ingestion (rejection) and at retrieval (invisible predicate).
- DB error applying the access filter: query fails closed with a boundary (G-19).
- `access.fail_closed` config key is hardwired `true`. The config loader raises on any attempt to set it `false`.

**Access condition:** `role IN allowed_roles` AND `classification IN permitted_classifications`. Both conditions, AND, never OR. Clearance level alone never grants access; explicit role membership is always required.

---

## Consequences

**Enables:**
- Zero possibility of post-filter bypass: there is no code path that retrieves unfiltered chunks and then filters them. Disallowed chunks do not exist in the candidate set.
- Provable via SQL inspection: the access filter is a first-class SQL predicate, auditable by any DBA.
- 104-check access proof battery (`scripts/prove_access_control.py`) that confirms zero leaks at the system level.
- CI gate asserts `access_control_pass_pct: 100.0%` on every run.

**Constrains:**
- Requires `classification` and `allowed_roles` to be indexed columns on every chunk row (mandatory, non-null). This is enforced at ingestion (G-06) and checked at retrieval (G-06b).
- The access filter logic in `access_sql_where` and `chunk_is_visible` must be kept in sync. A divergence between the SQL path and the file-index path would be a security regression. Tests cover both paths.
- The `output_guardrail` citation re-validation adds latency (it calls `resolve_access` again). This is an intentional security trade-off: defense in depth is worth a small latency cost.
- Unknown roles get no answer at all, even for PUBLIC documents. A caller who misspells their role string gets a boundary. This is intentional: silently mapping an unknown role to a default role is a privilege-grant bug.

---

## Change History

- 2026-06-29: Initial ADR accepted.
