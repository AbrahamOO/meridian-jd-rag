# Glossary

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist. Regulatory references name real frameworks but every interpretation, threshold, and procedure in this system is synthetic.

---

This glossary covers banking and compliance terms used in Meridian J.D. RAG's document corpus, plus the retrieval-augmented generation and machine-learning terms that describe how the system works.

---

## Banking and compliance terms

**Basel III**: International regulatory framework setting standards for bank capital adequacy, stress testing, and liquidity risk. Implemented in the U.S. via federal capital rule frameworks.

**BSA (Bank Secrecy Act)**: U.S. law requiring financial institutions to detect and report suspicious activity to combat money laundering and financial crime. The primary source of AML obligations in the U.S.

**CCAR/DFAST (Comprehensive Capital Analysis and Review / Dodd-Frank Act Stress Tests)**: Annual stress-testing requirements for large U.S. bank holding companies.

**CDD (Customer Due Diligence)**: The process of verifying a customer's identity and assessing the risk they pose to the institution. A core AML compliance requirement.

**CIP (Customer Identification Program)**: A subset of CDD: the minimum identity-verification procedures required when opening new accounts under the USA PATRIOT Act.

**CTR (Currency Transaction Report)**: A report financial institutions must file with FinCEN for cash transactions exceeding $10,000, or structured to evade that threshold.

**ECOA (Equal Credit Opportunity Act) / Regulation B**: Federal law prohibiting credit discrimination on the basis of race, color, religion, national origin, sex, marital status, or age.

**EDD (Enhanced Due Diligence)**: Heightened scrutiny applied to higher-risk customers such as politically exposed persons or high-transaction-volume entities. Exceeds standard CDD in depth and ongoing monitoring.

**FFIEC (Federal Financial Institutions Examination Council)**: U.S. interagency body that prescribes uniform examination principles and procedures for financial institutions, covering cybersecurity, AML, and IT risk.

**FR Y-9C**: The Federal Reserve's quarterly consolidated financial statement filing for bank holding companies.

**GLBA (Gramm-Leach-Bliley Act)**: U.S. law requiring financial institutions to protect consumer financial privacy. The Safeguards Rule under GLBA prescribes information security standards.

**OFAC (Office of Foreign Assets Control)**: U.S. Treasury body that administers sanctions programs. Financial institutions must screen transactions against OFAC's SDN (Specially Designated Nationals) list.

**SAR (Suspicious Activity Report)**: A report financial institutions must file with FinCEN when they detect suspected money laundering, fraud, or other financial crime.

**SR 11-7**: Federal Reserve supervisory guidance on model risk management. Requires institutions to maintain a framework covering model validation, governance, and ongoing monitoring.

---

## RAG and machine-learning terms

**ABAC (Attribute-Based Access Control)**: An access control model where decisions are based on attributes of the subject (role, clearance), the resource (classification, allowed_roles), and optionally the environment. This system requires two attributes: clearance level and explicit role membership.

**BM25**: A sparse retrieval algorithm that scores documents by term frequency weighted against inverse document frequency. The standard keyword-retrieval baseline. Here approximated by Postgres `tsvector` + `ts_rank_cd` (gap-register G-01).

**Chunk (child chunk)**: The unit stored in the vector index and used for retrieval. In the production chunking strategy, a small (320-token target) piece of a document section with a contextual header prepended to the embedded text.

**Chunking strategy**: The algorithm for splitting documents into chunks. This system has two: production (structure-aware, contextual headers, small-to-big) and naive (fixed-size, no structure awareness).

**Contextual header**: The string `"{title} > {section_path}\n\n"` prepended to every child chunk before embedding. Encodes provenance, improving dense retrieval accuracy.

**Cross-encoder**: A reranking model that scores a (query, passage) pair together rather than separately, giving higher accuracy than bi-encoder cosine similarity at the cost of not being able to precompute passage vectors. Used in the reranker step (`bge-reranker-base` in local mode).

**Dense retrieval**: Vector similarity search using embedding vectors and approximate nearest-neighbor search. Captures semantic similarity but can miss exact-term matches. Implemented here with pgvector and cosine distance.

**Embed text**: The string actually fed to the embedding model: `contextual_header + text`. Distinct from `text` (raw body) and `parent_text` (the full parent section).

**Fail-closed**: A design principle where the system denies rather than permits when facing ambiguity or failure. Applied to access control, ingestion validation, and provider failures.

**Faithfulness**: An eval metric measuring whether every claim in a generated answer is grounded in the retrieved context. 1.0 = fully grounded; 0.0 = fully fabricated.

**Generator (abstain stub)**: When no local LLM is configured and the adapter is `local`, the generator returns the insufficient-context boundary string for every content question. The system is callable but cannot produce prose answers. This is the zero-key degraded mode.

**Golden record (eval)**: A hand-curated test case with a question, expected source documents, expected answer keywords, persona, and type. The 78 golden records in the eval suite are the ground truth for all reported metrics.

**Hybrid retrieval**: Combining dense (vector) and sparse (BM25/FTS) retrieval results with a fusion algorithm (here: RRF). Captures both semantic similarity and keyword overlap.

**HyDE (Hypothetical Document Embedding)**: A query transformation technique that generates a hypothetical answer, embeds it, and uses that vector to retrieve real passages that are semantically similar to what a good answer would look like.

**LangGraph**: A Python library for building stateful, graph-structured workflows for LLM applications. Used here for the 8-node query graph.

**Manifest**: The `data/manifests/<index_version>.json` file recording index state: embedding model, dimension, chunking parameters, per-document content hashes, and chunk counts. Immutable once written. Used for embedding model mismatch detection (G-18) and incremental re-embedding.

**MRR (Mean Reciprocal Rank)**: The mean of 1/rank across queries, where rank is the position of the first relevant result. MRR = 1.0 means the top result was always relevant.

**NDCG (Normalized Discounted Cumulative Gain)**: A ranking quality metric that rewards relevant results appearing higher in the ranked list, with a logarithmic discount. NDCG = 1.0 means the ranking was perfect.

**Parent (parent section)**: The section a child chunk belongs to. The generator receives the parent's text (up to `parent_max_tokens` tokens), not the child chunk text. This is the "big" in small-to-big retrieval.

**Persona**: One of the 7 canonical role strings in this system: `OPERATIONS_ANALYST`, `COMPLIANCE_OFFICER`, `SOFTWARE_ENGINEER`, `SECURITY_ARCHITECT`, `RISK_ANALYST`, `FINANCE_CONTROLLER`, `BRANCH_STAFF`. Access control is defined in terms of personas.

**pgvector**: A Postgres extension adding a `vector` data type and approximate nearest-neighbor index types (IVFFlat, HNSW). Used here for dense vector storage and retrieval.

**PII (Personally Identifiable Information)**: Information that can identify a specific individual. Redacted before embedding (at ingestion) and before logging (at the audit_sink). A synthetic PII canary in the corpus verifies that redaction works.

**Prompt injection**: An attack where malicious instructions in retrieved documents or user queries attempt to override the model's system prompt. Defended by structural delimiting (`CONTEXT_BLOCK` tags) and the foreign-doc-id scan.

**RAG (Retrieval-Augmented Generation)**: A pattern where a language model's response is grounded in retrieved documents rather than solely in its parametric memory. Retrieved documents provide factual context; the model synthesizes an answer from them.

**Reranker (cross-encoder)**: A model that takes a (query, passage) pair and produces a single relevance score, more accurate than bi-encoder cosine similarity. Operates only on access-filtered retrieval candidates.

**RRF (Reciprocal Rank Fusion)**: A fusion algorithm that combines multiple ranked lists by summing `1 / (k + rank)` contributions from each list. Default `k = 60`. RRF is robust, parameter-light, and requires no score normalization.

**Small-to-big**: A retrieval pattern where small child chunks are retrieved for precision, but the larger parent section is passed to the generator for context. Child chunks are the retrieval unit; parent sections are the generation context.

**Sparse retrieval**: Keyword-based retrieval using term frequency statistics (BM25 or similar). Excels at exact-term matching for regulatory tokens like "FR Y-9C" or "SR 11-7". Implemented here via Postgres `tsvector` with `simple` and `english` configurations.

**STRIDE**: A threat modeling framework covering six categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. Used to categorize threats in [`security/THREAT_MODEL.md`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/security/THREAT_MODEL.md).

**Superseded**: A document replaced by a newer version. In this system, superseded documents (e.g., MJD-OPS-0009) remain in the index with `is_superseded=true` and a 0.5 RRF score penalty (G-02). They can still be retrieved but cannot outrank their live successor, and are annotated `(superseded, see vX.Y)` when surfaced in generation.

**Token budget**: The maximum tokens the assembler can include in the context sent to the generator. Default 3,500 tokens (3,500 − 600 for system/question overhead = 2,900 for context blocks).

**tsvector**: A Postgres data type representing a sorted, deduplicated list of lexemes for full-text search. GIN-indexed for fast lookups.
