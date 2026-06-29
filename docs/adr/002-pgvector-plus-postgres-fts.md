# ADR-002: pgvector + Postgres FTS as BM25 Equivalent

**Status:** Accepted
**Created: 2026-06-29**
**Last updated: 2026-06-29**

---

## Context

The spec requires hybrid dense+sparse (BM25) retrieval. The dense side is clearly served by pgvector. The sparse side requires a BM25-capable store.

The two main alternatives are:

**Option A: Separate BM25 service (Elasticsearch/OpenSearch).** Full BM25 implementation with tunable parameters. Adds a second service to the docker-compose, requires a separate index, separate access filter logic, and separate result fusion code. Startup is no longer one command without extra dependencies.

**Option B: Postgres native full-text search.** Postgres `tsvector` columns with GIN indexes and `ts_rank_cd` ranking approximate BM25 behavior. The corpus (51 documents, ~2,000 chunks) fits comfortably in one Postgres instance. All access filter logic lives in one SQL WHERE clause applied identically to both dense and sparse queries in the same database.

The spec explicitly values one-command startup and a single Postgres dependency (the main motivation for choosing pgvector over a dedicated vector store). A second service undermines this.

The critical concern for this corpus is exact-term recall for regulatory tokens: "FR Y-9C", "SR 11-7", "OAuth2", "OFAC", "Basel III". These tokens are not stemmed or stopped if they appear verbatim in the text; they must survive the tokenization step exactly.

---

## Decision

Use Postgres native full-text search as the sparse backend (gap-register G-01):

1. Add a `tsvector` column over `embed_text` (header + child text, not bare `text`, so regulatory tokens in the section path survive) indexed with GIN.
2. Use the `simple` text search configuration for one ranking column (no stemming, no stopword removal, preserves exact regulatory tokens).
3. Use the `english` text search configuration for a second ranking column (stemming and stopwords for natural-language recall).
4. The sparse ranked list is the RRF fusion of both `ts_rank_cd` orderings, deduped by `chunk_id` keeping the best rank.
5. The access filter SQL WHERE clause applies identically to the `tsvector` query and the pgvector cosine distance query in the same Postgres session.

The RRF fusion (k=60) combines the dense list and the sparse list. A chunk's `rrf_score` is the sum of `1/(60+rank)` contributions from each list it appears in.

The `ts_rank_cd` ordering is treated as the "BM25-equivalent" ranked list for RRF input purposes. It is not identical to BM25 (it lacks exact IDF weighting in the pgvector BM25 sense), but it is adequate for this corpus size and preserves exact-term recall, which is the primary reason for adding sparse retrieval.

---

## Consequences

**Enables:**
- One-command startup with zero extra services.
- Identical access filter SQL applied to both dense and sparse queries without code duplication.
- Exact-term recall for regulatory identifiers ("SR 11-7", "FR Y-9C") via the `simple` configuration.
- Natural-language recall via the `english` configuration.
- Manifest versioning aligned to the same Postgres instance (no out-of-sync vector store vs. keyword store).

**Constrains:**
- `ts_rank_cd` is not pure BM25. For very large corpora (millions of documents), a dedicated BM25 service would deliver better sparse ranking. For this corpus (2,000 chunks, 51 documents), the difference is immaterial.
- Both dense and sparse indexes must be rebuilt together on re-index (they are co-located in the same Postgres table). This is the expected behavior for the manifest's immutability guarantee (G-20) and is not a practical constraint.
- The alternative (Elasticsearch/OpenSearch) is noted in the manifest comments as the credible large-scale option. Switching requires implementing a second `hybrid.py` path and a second access-filter expression, but the provider interface abstraction and the access-filter contract (section 3.1) are written to allow this extension.

---

## Change History

- 2026-06-29: Initial ADR accepted.
