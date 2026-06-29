# ADR-001: Structure-Aware Contextual Small-to-Big Chunking

**Status:** Accepted
**Created: 2026-06-29**
**Last updated: 2026-06-29**

---

## Context

The corpus consists of 51 financial policy documents with deeply hierarchical structure (parts, sections, subsections, tables, bullet lists). Three problems must be solved simultaneously:

1. **Context-free fragments:** Fixed-size chunking produces fragments like "This threshold applies to all accounts." without the document and section context needed to embed meaningfully or to answer "which threshold for what?"

2. **Table destruction:** Financial documents are dense with tables (transaction limits, dual-approval matrices, fee schedules). A naive fixed-size split will cut a table mid-row, separating cells from their headers and producing uninterpretable fragments.

3. **Precision vs. context tradeoff:** Dense retrieval benefits from small, focused chunks with precise semantic signals. Generation benefits from wide, coherent sections with sufficient context to produce a complete answer. These are in tension if the retrieval unit equals the generation unit.

The naive alternative is a fixed-size chunker at 320 tokens with no structure awareness and no header. This is implemented and kept for the eval baseline but is explicitly not the production strategy.

---

## Decision

Use a three-part production chunking approach implemented in `ingestion/chunkers/production.py`:

**1. Structure-aware splitting:** Parse the document's Markdown heading hierarchy (`#`, `##`, `###`) and use heading boundaries as the primary split points. Leaf sections within `child_target_tokens` (default 320) become single child chunks. Oversized leaf sections are recursively split on paragraph boundaries, then sentence boundaries, maintaining `child_overlap_pct` (default 12%) overlap so context is preserved at chunk boundaries.

**2. Contextual headers:** Every child chunk's `embed_text` field is `"{title} > {section_path}\n\n{text}"`. Example: `"Cryptographic Standard > 4 > 4.3\n\nKeys are rotated every 90 days ..."`. This header encodes the document and section location in the embedding, solving the context-free fragment problem without requiring a separate metadata-lookup at retrieval time.

**3. Small-to-big retrieval:** Child chunks (320-token target) are the retrieval and reranking unit. Parent sections (up to 1,200 tokens, the heading section the child belongs to) are the generation unit. Every child chunk carries a `parent_id` and `parent_text`. Assembly deduplicates by `parent_id` and promotes to `parent_text` for the generator.

**4. Table protection (G-10):** A Markdown table is treated as an atomic unit. The production chunker never splits a table across chunk boundaries. An oversized table becomes its own single chunk flagged `oversized_table=true`. Truncation (when the table exceeds `parent_max_tokens`) removes whole trailing rows only, preserving the header row.

The naive chunker (`ingestion/chunkers/naive.py`) is retained as the eval baseline. Both strategies coexist in the index, distinguished by `chunk_strategy`, so the eval harness can compare them without cross-contamination.

---

## Consequences

**Enables:**
- Meaningful dense retrieval: contextual headers give the embedding model enough signal to distinguish "EDD threshold > 3.2 > threshold criteria" from a generic "threshold" reference.
- Complete generation context: parent section promotion gives the generator the full surrounding procedure, not just the 60-token matching sentence.
- Table interpretability: tables are never corrupted by mid-row splits.
- Quantitative validation of the approach: the eval delta (production vs. naive) directly measures the chunking contribution to retrieval quality.

**Constrains:**
- More chunks per document than naive (1,974 production vs. 944 naive), requiring more storage and slightly longer ingestion time.
- Requires Markdown heading structure in the source documents. Documents without headings fall back to paragraph-based splitting (still better than fixed-size).
- The contextual header in `embed_text` means the embedding and display text differ. The chunk visualizer must show both fields to avoid confusion.

---

## Change History

- 2026-06-29: Initial ADR accepted.
