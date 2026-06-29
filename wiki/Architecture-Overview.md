# Architecture Overview

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist.

---

Meridian J.D. RAG is a retrieval-augmented generation system for policy documents, with two distinguishing properties: access control is enforced as a SQL `WHERE` clause before any vector similarity is scored, and both the ingestion and query loops share a single provider interface so models can be swapped without touching loop logic.

---

## System purpose

The system serves 7 distinct employee personas across a fictional fintech. A `COMPLIANCE_OFFICER` asking about AML procedures gets a different answer than a `BRANCH_STAFF` asking the same question: not because business logic filters results after retrieval, but because the `COMPLIANCE_OFFICER`'s allowed documents differ from `BRANCH_STAFF`'s, and that difference is a SQL `WHERE` clause applied before any vector similarity is computed. Disallowed chunks are never scored, never ranked, never seen by the generator.

---

## Two retrieval loops, one provider interface

An offline ingestion loop and an online query loop both call the same `providers/` abstraction. The embedding model, generator, and reranker are selected by profile name: swapping from `local` to `anthropic` or `openai` requires no changes to either loop.

```text
Offline: corpus/ -> Loader -> PII Redactor -> Chunker -> EmbeddingProvider -> Index
Online:  /query -> LangGraph 8-node graph -> Index -> EmbeddingProvider -> Generator -> Response
```

The offline loop runs once (or on corpus update). The online loop runs per request. Sharing a provider interface means a local `bge-small-en-v1.5` embedding used during ingestion is the same code path used at query time: no embedding mismatch across loops.

---

## Technology choices

| Layer | Choice | Reason |
| --- | --- | --- |
| Vector store | PostgreSQL 16 + pgvector | One service for both dense vector index (pgvector `<->` operator) and sparse BM25-equivalent (native `tsvector` + GIN + `ts_rank_cd`). One-command startup, no extra service. |
| Sparse retrieval | Postgres FTS (`tsvector`, `simple` + `english` configs) | Preserves exact regulatory tokens ("FR Y-9C", "SR 11-7", "OAuth2") in `simple` mode while providing recall on natural language in `english` mode. |
| Fusion | Reciprocal Rank Fusion (RRF, k=60) | Robust, parameter-light, well-studied combination of dense and sparse lists. |
| Chunking (production) | Structure-aware + contextual header + small-to-big | Respects Markdown heading hierarchy, never splits tables, adds title+section path to every embedded string, stores the parent section for generation. |
| Access control | SQL WHERE clause (pre-scoring) | Disallowed chunks are never scored, never ranked, never seen by the generator. Not a post-filter. |
| Query graph | LangGraph | Typed state, pure-function nodes, deterministic node ordering, easy to test in isolation. |
| API | FastAPI | Pydantic validation on all inputs, typed response models, OpenAPI schema for free. |
| UI | React 19 + Vite | 4 views: Chat (role-switch), Eval dashboard, Chunk visualizer, Audit viewer. |
| Evals | Custom harness over golden records + ragas metrics | CI gate on security metrics (faithfulness, access_control_pass_pct). |
| Default providers | Local bge-small-en-v1.5 (embed) + bge-reranker-base (rerank) + abstain stub (generate) | Zero API keys required. System starts and serves with no network calls. |
| CI providers | All-mock (sha256-seeded hash embedder, deterministic extractive generator, Jaccard reranker) | Deterministic, reproducible, zero keys, zero network. Eval numbers are assertable across CI runs. |

I picked Postgres + pgvector so dense and sparse retrieval live in one service. The alternative: a dedicated vector DB alongside Postgres for metadata: adds operational cost for no query-correctness gain at this scale. RRF at k=60 is the fusion algorithm because it degrades gracefully when one list is noisy and needs no per-corpus tuning.

---

## Hybrid retrieval architecture

The retrieval pipeline runs dense and sparse queries in parallel, fuses them with RRF, then cross-encoder reranks the access-filtered candidate set. The access filter is applied first: before dense scoring, before sparse scoring: so the reranker only ever sees chunks the requesting persona is permitted to read. See [Access-Control Model](Access-Control-Model) for the full role-to-classification mapping and SQL predicate construction.

---

## LangGraph query graph

The online path is an 8-node LangGraph `StateGraph`. Nodes are pure functions over a typed `QueryState`; each node can be tested independently without running the full graph. Node ordering is deterministic. The graph handles query rewriting, decomposition, HyDE, retrieval, reranking, generation, and guardrails as separate nodes: easier to profile and swap than a monolithic chain.

---

## Module map

```text
api/
  app.py              FastAPI app. Endpoints: /query, /ingest, /evals, /health, /audit.
  graph/
    builder.py        Constructs the LangGraph StateGraph and compiles it.
    nodes.py          8 node functions (pure functions over QueryState).

retrieval/
  access.py           resolve_access, build_access_filter, chunk_is_visible, access_sql_where.
  pipeline.py         Orchestrates the retrieval flow: access -> retrieve -> rerank -> assemble.
  hybrid.py           RRF fusion of dense vector query and BM25 sparse query.
  rerank.py           Cross-encoder reranking on access-filtered candidates.
  assemble.py         Small-to-big parent assembly, token-budget management.
  citations.py        Citation re-validation (G-04): strip hallucinated or out-of-scope citations.
  repository.py       Repository abstraction over pgvector + file-index backends.
  transform.py        Query rewriting, decomposition, HyDE.

generation/
  prompts.py          System prompt template + CONTEXT_BLOCK delimiter wrapping.
  guardrails_input.py Injection detection (G-17), scope check (G-16).
  guardrails_output.py Citation strip, groundedness check, PII output scan.
  pipeline.py         Orchestrates generate -> guardrail.
  generator.py        Calls the GeneratorProvider.

ingestion/
  chunkers/
    production.py     Structure-aware chunker with contextual headers.
    naive.py          Fixed-size baseline chunker.
    base.py           BaseChunker protocol.
  loaders/            MD / DOCX / PDF / HTML loaders.
  pii.py              PII redactor (Presidio in production, regex fallback in CI).
  embed.py            Embedding orchestration with content_hash dedup.
  index.py            Index writer: SQL schema creation, row insertion, manifest write.
  metadata.py         Metadata validation: doc_id regex, allowed_roles, classification.
  tokens.py           Token counting abstraction (tiktoken or len//4 heuristic).

providers/
  base.py             EmbeddingProvider, Generator, Reranker protocols + result dataclasses.
  factory.py          get_embedding_provider, get_generator, get_reranker (name -> class).
  secrets.py          resolve_secret: env -> /run/secrets -> None.
  local.py            Local bge adapters (sentence-transformers, cross-encoder).
  mock.py             Deterministic CI adapters.
  anthropic_adapter.py  Anthropic Claude generator.
  openai_adapter.py   OpenAI text-embedding-3 adapter.
  gemini_adapter.py   Gemini embedding + generator adapter.

observability/
  audit.py            AuditWriter: redacted audit log + restricted debug trace (G-03).
  tracing.py          Trace ID generation, latency tracking.

config/
  default.yaml        Zero-key config.
  ci.yaml             All-mock CI config.

core/
  models.py           Canonical enums: CANONICAL_PERSONAS, PERMITTED_CLASSIFICATIONS,
                      AccessDecision, and other shared dataclasses.
```

---

## Configuration and profile layering

Configuration follows a strict precedence: `default.yaml` (lowest) < profile YAML (selected by `MJD_PROFILE`) < `config/local.yaml` (gitignored, user overrides) < environment variables (highest).

The key profiles are:

- `default` (zero-key): local bge embeddings, local bge reranker, abstain-only generator stub. System starts and serves without any API keys.
- `ci`: all-mock deterministic providers. Used exclusively in CI. Eval numbers are byte-identical across runs.
- `hybrid` (requires `.env`): OpenAI embeddings, Anthropic generator, local reranker. Full answer-correctness.

The `access.fail_closed` config key is hardwired `true`. The config loader raises on any attempt to set it `false`. There is no production path that fails open.

---

## Related pages

- [Access-Control Model](Access-Control-Model)
- [Ingestion Pipeline](Chunking-Strategy)
- [Query Graph](RAG-Pipeline-Deep-Dive)
- [Provider Abstraction](Provider-and-Config-Guide)
- [Evaluation Harness](Eval-Methodology)
