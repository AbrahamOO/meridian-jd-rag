-- Meridian J.D. RAG pgvector index schema (gap-register G-01).
--
-- Co-locates the dense vector, the full chunk metadata (the access backbone:
-- classification + allowed_roles), and DUAL sparse tsvector columns (simple +
-- english) so exact regulatory tokens (FR Y-9C, SR 11-7, OAuth2) survive while
-- natural-language recall still works. GIN indexes back both tsvectors; an
-- ivfflat/hnsw index backs the dense vector. The {DIM} placeholder is filled in
-- by index.py from the active embedding model's dimensionality.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id        TEXT PRIMARY KEY,
    doc_id          TEXT NOT NULL,
    parent_id       TEXT NOT NULL,
    title           TEXT NOT NULL,
    department      TEXT NOT NULL,
    doc_type        TEXT NOT NULL,
    classification  TEXT NOT NULL,
    owner_role      TEXT NOT NULL,
    allowed_roles   TEXT[] NOT NULL,
    effective_date  DATE NOT NULL,
    version         TEXT NOT NULL,
    supersedes      TEXT,
    is_superseded   BOOLEAN NOT NULL DEFAULT FALSE,
    entity_status   TEXT NOT NULL,
    section_path    TEXT NOT NULL,
    text            TEXT NOT NULL,
    embed_text      TEXT NOT NULL,
    parent_text     TEXT NOT NULL,
    char_start      INTEGER NOT NULL,
    char_end        INTEGER NOT NULL,
    token_count     INTEGER NOT NULL,
    content_hash    TEXT NOT NULL,
    chunk_strategy  TEXT NOT NULL,
    embedding       vector({DIM}) NOT NULL,
    index_version   TEXT NOT NULL,
    -- Dual sparse columns over embed_text (header + child text). `simple` keeps
    -- exact regulatory tokens; `english` adds stemmed recall (G-01).
    tsv_simple      tsvector GENERATED ALWAYS AS (to_tsvector('simple', embed_text)) STORED,
    tsv_english     tsvector GENERATED ALWAYS AS (to_tsvector('english', embed_text)) STORED
);

CREATE INDEX IF NOT EXISTS chunks_tsv_simple_gin  ON chunks USING GIN (tsv_simple);
CREATE INDEX IF NOT EXISTS chunks_tsv_english_gin ON chunks USING GIN (tsv_english);
CREATE INDEX IF NOT EXISTS chunks_doc_id_idx      ON chunks (doc_id);
CREATE INDEX IF NOT EXISTS chunks_strategy_idx    ON chunks (chunk_strategy);
CREATE INDEX IF NOT EXISTS chunks_allowed_gin     ON chunks USING GIN (allowed_roles);
-- Dense ANN index (cosine). Built after load for population efficiency.
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
    ON chunks USING hnsw (embedding vector_cosine_ops);
