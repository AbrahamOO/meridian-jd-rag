# Architecture Decision Records: Meridian J.D. RAG

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist.

---

This index lists every Architecture Decision Record (ADR) for the Meridian J.D. RAG system: a portfolio RAG pipeline for financial documents: covering retrieval strategy, storage, provider abstraction, access control, evaluation gates, and documentation drift.

| ADR | Title | Status |
|---|---|---|
| [ADR-001](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/docs/adr/001-chunking-strategy.md) | Structure-Aware Contextual Small-to-Big Chunking | Accepted |
| [ADR-002](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/docs/adr/002-pgvector-plus-postgres-fts.md) | pgvector + Postgres FTS as BM25 Equivalent | Accepted |
| [ADR-003](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/docs/adr/003-provider-interface-and-adapters.md) | Provider Interface and Adapter Pattern | Accepted |
| [ADR-004](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/docs/adr/004-fail-closed-retrieval-time-abac.md) | Fail-Closed Retrieval-Time ABAC | Accepted |
| [ADR-005](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/docs/adr/005-eval-thresholds-and-ci-gate.md) | Eval Thresholds and CI Gate | Accepted |
| [ADR-006](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/docs/adr/006-docs-sync-rule.md) | Docs-Sync Rule and Drift Guard | Accepted |

---

## Decision Summaries

**ADR-001** chose structure-aware chunking with contextual headers over naive fixed-size chunking. The contextual header (title + section_path prepended to `embed_text`) solves the context-free fragment problem. Small-to-big retrieval separates the retrieval unit (child chunk, 320 tokens) from the generation context (parent section, up to 1,200 tokens). The naive chunker is kept as an eval baseline.

**ADR-002** chose Postgres native full-text search (`tsvector` + GIN + `ts_rank_cd`) as the BM25-equivalent sparse backend instead of a separate Elasticsearch/OpenSearch service. This keeps one-command startup true and allows the access control SQL WHERE clause to apply identically to both dense and sparse queries in the same database.

**ADR-003** chose a strict provider interface (Protocol classes for EmbeddingProvider, Generator, Reranker) with named adapters selected purely by config. No provider name is hardcoded outside the factory. This makes the zero-key default (local adapters) and the CI mock adapters interchangeable with cloud adapters without code changes.

**ADR-004** chose pre-scoring SQL WHERE clause enforcement for access control rather than post-retrieval Python filtering. The SQL WHERE clause is the only enforcement point for the primary access filter; post-scoring filtering is defense-in-depth only (citation re-validation at the output_guardrail). `fail_closed: true` is hardwired; the config loader rejects any attempt to set it false.

**ADR-005** chose two CI-gated thresholds: `faithfulness >= 0.9` and `access_control_pass_pct >= 100.0`. These are the only metrics appropriate for a deterministic mock CI run. Answer-correctness is explicitly not gated in CI because the mock generator is extractive by design. Security metrics are hard fails at any individual record level, not just aggregate.

**ADR-006** chose a docs-sync rule enforced by a CI step and a git pre-commit hook. Architecture-bearing files (`api/`, `retrieval/`, `ingestion/`, `generation/`, `providers/`, `infra/`, `manifest.json`, config) trigger a drift guard that fails CI if the README or wiki diagrams have not been updated in the same commit.
