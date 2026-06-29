# Chunking Strategy

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist.

---

Meridian J.D. RAG uses structure-aware contextual-header small-to-big chunking in production, with a fixed-size naive baseline retained for apples-to-apples eval comparison.

---

## Why chunking strategy matters for financial RAG

Retrieval quality is determined by what units get embedded and what units the generator sees. A financial policy document has a real hierarchy: part > section > subsection > paragraph > table row: and chunking that ignores it creates two concrete failure modes.

**Context-free fragments.** A chunk like "This threshold applies to all accounts." is meaningless without the surrounding document, section, and threshold it refers to. Its embedding matches weakly against queries because the relevant signal lives outside the chunk boundary.

**Table destruction.** Financial documents are dense with tables: transaction limits, dual-approval matrices, regulatory references. Splitting a table mid-row separates cells from headers, producing fragments that retrieve garbage and generate garbage.

The production chunker addresses both. The naive chunker deliberately does neither; it exists so the eval delta has a meaningful baseline to measure against.

---

## Production chunker

**Source:** [`ingestion/chunkers/production.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/ingestion/chunkers/production.py)

### Structure-aware splitting

The production chunker reads the Markdown heading hierarchy (`#`, `##`, `###`, …) and treats each section as a structural unit. Splits happen at heading boundaries first. If a leaf section is within `child_target_tokens` (default 320 tokens), it becomes one child chunk. If it is larger, the chunker recurses on paragraph boundaries, then sentence boundaries, maintaining `child_overlap_pct` (default 12%) overlap between adjacent chunks so nothing is lost at the split point.

A 5,000-word section becomes several overlapping child chunks, each anchored to its heading path. A 200-word subsection stays undivided. Structure drives the split decision, not a fixed stride.

### Markdown table protection (G-10)

A Markdown table is treated as atomic: the production chunker never splits a table across chunk boundaries. An oversized table (larger than `child_target_tokens`) becomes its own chunk, flagged `oversized_table=true` in the side-channel metadata the chunk visualizer reads. Its parent is the enclosing section.

If the table exceeds `parent_max_tokens` (default 1,200 tokens) during parent assembly, it is truncated by removing whole trailing rows only. The header row is always preserved, keeping the table interpretable under extreme token-budget pressure.

### Contextual headers

Every child chunk carries two text fields:

- `text`: the raw chunk body, what BM25 indexes and what is displayed.
- `embed_text`: what actually goes to the embedding model: `"{title} > {section_path}\n\n{text}"`.

Example:
```
Cryptographic Standard > 4 > 4.3

Keys are rotated every 90 days and must use AES-256-GCM or ChaCha20-Poly1305 ...
```

Prepending the document title and full section path to every embedded string solves the context-free fragment problem: the embedding encodes not just what the text says but where it came from. A query for "key rotation policy" can match the `section_path` token "4.3" even when the body is sparse. The reranker also receives `embed_text`, not bare `text`, so the cross-encoder sees the same context the embedder saw.

### Small-to-big retrieval

Embedding, scoring, and reranking all operate on child chunks (320-token target). Generation receives the parent section (up to 1,200 tokens). That is the small-to-big pattern.

The split makes sense for different reasons in each direction. Dense retrieval benefits from small, focused chunks that match precisely. Generation benefits from wide, coherent sections that provide full context. The `parent_id` on every child chunk links them. A query for "EDD threshold" may match a 60-token child chunk inside a 900-token EDD procedure section; the reranker confirms relevance, and the assembler promotes the child to the full 900-token parent for the generator.

### Production chunk counts

A verified ingest run over the 51-document corpus produced:

| Strategy | Chunks |
|---|---|
| Production (structure-aware) | **1,974** |
| Naive (fixed-size baseline) | **944** |

The production chunker produces more chunks because heading-driven splitting creates more leaf units, particularly in documents with many subsections. Each leaf is smaller and more precise.

---

## Naive chunker (baseline)

**Source:** [`ingestion/chunkers/naive.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/ingestion/chunkers/naive.py)

The naive chunker is not a fallback or a deprecated path. It is an intentional baseline that makes the eval retrieval delta meaningful.

It splits every document at fixed `child_target_tokens` (320) with no overlap, no structure awareness, no table protection, and no contextual header. `parent_text` is identical to `text`: there is no parent promotion.

The eval harness runs both strategies on the same query set:

| metric | production | naive | delta |
|---|---|---|---|
| context_precision | 0.338 | 0.303 | +0.035 |
| context_recall | 0.859 | 0.846 | +0.013 |
| hit_rate_at_k | 0.603 | 0.603 | +0.000 |
| mrr | 0.529 | 0.516 | +0.013 |
| ndcg | 0.545 | 0.530 | +0.014 |

These numbers come from the `MJD_PROFILE=ci` run (mock providers, deterministic). Under real providers (local bge or hybrid), the delta is larger: contextual headers have more impact on a production embedding model than on the mock's hash embedder.

---

## Chunk record schema

Every chunk stored in the index carries:

```python
@dataclass(frozen=True)
class Chunk:
    chunk_id: str           # "{doc_id}::c{NNNN}" stable, zero-padded
    doc_id: str
    parent_id: str          # "{doc_id}::p{NNNN}"
    title: str
    department: str
    doc_type: str
    classification: str     # inherited from document, MANDATORY
    owner_role: str
    allowed_roles: list[str]  # inherited from document, MANDATORY
    effective_date: str
    version: str
    supersedes: str | None
    is_superseded: bool
    entity_status: str      # always "FICTIONAL"
    section_path: str       # "3 > 3.2 > 3.2.1"
    text: str               # child body without header
    embed_text: str         # header + text (what the embedder sees)
    parent_text: str        # full parent section (what generation gets)
    char_start: int
    char_end: int
    token_count: int
    content_hash: str       # sha256 of source doc
    chunk_strategy: str     # "production" | "naive"
```

`classification` and `allowed_roles` are mandatory and non-null on every stored chunk. A chunk that arrives at the index writer without them is a fatal ingestion error. This is what makes the SQL `WHERE` clause access filter safe: the filter can reference these columns on every row without a join.

---

## Chunk visualizer

The ChunkView tab in the UI ([`ui/src/views/ChunkView.tsx`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/ui/src/views/ChunkView.tsx)) shows the chunk breakdown for any document using the `explain` payload from `POST /query` with `options.explain=true`. It renders:

- Which child chunks were retrieved and their RRF scores
- Which parent sections were assembled (or dropped for budget)
- The `embed_text` (header + body) vs the raw `text`
- `oversized_table` flags

The explain payload never includes content the requesting role could not retrieve: enforced in [`api/app.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/api/app.py) at `_build_explain`.

---

## Related pages

- [Architecture](Architecture-Overview)
- [Eval Harness](Eval-Methodology)
- [Ingestion Pipeline](Chunking-Strategy)
- [Access Control](Access-Control-Model)
