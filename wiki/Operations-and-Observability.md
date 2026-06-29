# Operations and Observability

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist.

This page covers Meridian J.D. RAG's PII-redacted append-only audit log, opt-in restricted debug trace, health check endpoints, and re-indexing with atomic index pointer swap.

---

## Starting the stack

```bash
# One-command startup (Postgres + API + UI):
docker compose up --build

# Tear down and remove volumes:
make down

# Check health:
curl http://localhost:8000/health
```

Start order in `docker-compose.yml`:

1. Postgres (`pgvector/pgvector:pg16`) waits for `pg_isready`.
2. API container runs `scripts.ingest --mode full --strategies production,naive` (idempotent), then launches `uvicorn`. Waits for `/health` to return 200.
3. UI container starts after the API is healthy.

---

## Re-indexing and atomic index swap

Re-index after:

- Adding or removing documents from `corpus/`
- A metadata change (classification, allowed_roles, version)
- An embedding model or chunking strategy change

```bash
# Re-index via Makefile (uses MJD_PROFILE env var, default: ci):
make ingest

# Re-index with a specific profile:
MJD_PROFILE=default make ingest

# Re-index via the API:
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"mode": "full", "paths": ["corpus/"], "strategies": ["production", "naive"], "dry_run": false}'

# Dry run (validate without writing the index):
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"mode": "full", "paths": ["corpus/"], "strategies": ["production", "naive"], "dry_run": true}'
```

Re-indexing writes a new `manifest.json` with a new `index_version`. The live manifest pointer swaps atomically: but only after a post-build smoke check passes (G-20). A failed smoke check leaves the old index live. No request ever reads a half-built index.

A successful re-index response:
```json
{
  "index_version": "idx-YYYY-MM-DD-001",
  "manifest_path": "data/manifests/idx-YYYY-MM-DD-001.json",
  "ingested": 51,
  "rejected": [],
  "chunks": {"production": 1974, "naive": 944},
  "duration_s": 1.0,
  "pii_redactions": 18
}
```

---

## Audit logging and PII redaction

Location: `data/audit.log.jsonl`: append-only, one JSON object per line.

Every request, including boundary responses, produces exactly one audit record:

```json
{
  "trace_id": "uuid4",
  "role": "OPERATIONS_ANALYST",
  "query": "[REDACTED: contains PII]",
  "retrieved_doc_ids": ["MJD-OPS-0002", "MJD-OPS-0005"],
  "boundary_triggered": false,
  "boundary_reason": "",
  "guardrail_flags": [],
  "latency_ms": 412.7,
  "cost_usd": 0.001834,
  "tokens": {"prompt": 1840, "completion": 210, "embed": 14},
  "timestamp": "2026-06-29T14:03:22.481Z"
}
```

Design decisions worth noting:
- The `query` field is PII-redacted before writing. The raw query never reaches this log.
- `retrieved_doc_ids` lists only doc IDs the role was allowed to retrieve: never a doc the role could not access.
- No document content, ever.
- The log is append-only. The UI `AuditView` reads it via `GET /audit` but never mutates it.

This is a two-sink design: the audit log (redacted, retained indefinitely) and the debug trace (raw, 7-day TTL, admin-only). Separating them keeps compliance artifacts clean while still allowing full retrieval internals to be inspected when needed.

The AuditView tab in the UI renders the audit log with filtering by role, `boundary_triggered`, and timestamp range.

---

## Debug trace observability

Location: `data/debug_trace.jsonl`

The debug trace stores the raw (un-redacted) query and full retrieval internals. It is off by default (`observability.debug_trace: false`). Enable only when actively debugging:

```yaml
# config/local.yaml
observability:
  debug_trace: true
```

TTL is 7 days. Access is restricted to admin scope. Do not enable in production without explicit policy justification and access controls. A misconfigured debug trace that persists indefinitely with broad read access is a GLBA compliance risk.

---

## Tracing and latency observability

Every request gets a `trace_id` (UUID4) at the API boundary. It flows through all 8 graph nodes and appears in the audit record, the API response, and the debug trace.

[`observability/tracing.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/observability/tracing.py) records `start_time` at each node entry and computes `elapsed_ms` at exit. `QueryState.latency_ms` accumulates end-to-end latency from request receipt through `audit_sink` completion.

The `/health` endpoint includes `"latency_ms"` for the health check itself: a useful baseline for API responsiveness without embedding or generation overhead.

---

## Cost and token tracking

`QueryState.cost_usd` and `QueryState.tokens` accumulate across all provider calls in a single request:
- `tokens.embed`: input tokens billed by the embedding provider
- `tokens.prompt`: input tokens billed by the generator
- `tokens.completion`: output tokens billed by the generator
- `cost_usd`: sum of all provider `cost_usd` fields (6 decimal places)

Under mock and local adapters, `cost_usd=0.0`. Under cloud adapters, the provider adapter computes cost from published token pricing and records it in `GenerationResult.cost_usd` and `EmbeddingResult.cost_usd`.

The eval dashboard's `cost_per_query_usd` is the average across all 78 eval records. Under CI (mock): $0.000.

---

## Health check endpoints

```bash
GET /health
```

Returns per-provider health (`ok`, `adapter`, `model`, `dim` for embedding) and index health (`loaded`, `index_version`, `documents`, `chunks`). An embedding model mismatch (G-18) sets `ok=false` for the embedding provider and blocks queries.

```bash
GET /evals
```

Returns `{"latest": <full eval report>, "runs": ["run-...", ...]}`. The UI EvalView reads this endpoint to populate the dashboard.

```bash
GET /audit
```

Returns paginated audit records (redacted). The UI AuditView reads this endpoint.

---

## Maintenance checklist

**After adding documents to `corpus/`:**

1. Verify YAML front-matter is complete (`doc_id`, `classification`, `allowed_roles`, etc.)
2. Run `make ingest` (or `POST /ingest` with `dry_run: true` first)
3. Check the response's `rejected` field is empty
4. Run `make prove-access` to confirm zero leaks
5. Run `make eval` to confirm the CI gate still passes

**After changing the embedding model:**

1. Update `config/default.yaml` (or `config/local.yaml`) with the new adapter and model
2. Run `make ingest` to rebuild the index with the new model
3. The manifest records the new model and dim
4. Confirm `/health` shows `ok: true` with the new model
5. A mismatch between the live index model and the active adapter blocks queries with `embedding_model_mismatch`

**To run only the security proof:**
```bash
make prove-access
```
Exit 0 = pass (zero leaks). Exit non-zero = leak found: check output for the persona and check that failed.

---

## CI pipeline steps

See [`https://github.com/AbrahamOO/meridian-jd-rag/blob/main/.github/workflows/ci.yml`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/.github/workflows/ci.yml):

1. Dependency pinning check ([`scripts/check_pinning.sh`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/scripts/check_pinning.sh)): fails if any `>=` or `~=` in requirements files.
2. Ruff linting.
3. Black formatting check.
4. Mypy type checking.
5. Build the CI index (`MJD_PROFILE=ci python -m scripts.ingest --mode full`).
6. Pytest (144 tests, `MJD_PROFILE=ci`).
7. Access-control proof ([`scripts/prove_access_control.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/scripts/prove_access_control.py), exit 0 required).
8. Evals CI gate ([`scripts/ci_eval_gate.sh`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/scripts/ci_eval_gate.sh), asserts faithfulness and `access_control_pass_pct`).
9. Secret scan ([`scripts/secret_scan.sh`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/scripts/secret_scan.sh)).
10. Docs-sync drift guard ([`scripts/check_docs_sync.sh`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/scripts/check_docs_sync.sh)).
