"""Chunk repository: the access-filtered source of candidate chunks.

Two backends mirror ingestion/index.py:

- ``FileChunkRepository`` reads the JSONL file index written by FileIndexWriter
  and applies the access pre-filter (retrieval/access.chunk_is_visible) BEFORE any
  scoring. This is the equivalent of the Postgres ``WHERE`` clause for the
  zero-Postgres CI path. Disallowed chunks never leave this layer.
- ``PostgresChunkRepository`` (lazy psycopg) applies the access predicate in the
  SQL ``WHERE`` clause of the pgvector + tsvector queries.

Both expose ``dense_candidates`` and ``sparse_candidates`` which return only
access-visible chunks, already scored, so hybrid.py can fuse them with RRF. The
access filter is identical for both lists (contract 3.2 hard rule).
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from core.models import Chunk
from ingestion.index import DEFAULT_INDEX_DIR, load_latest_manifest
from retrieval.access import access_sql_where, chunk_is_visible

# Fields of Chunk, used to reconstruct frozen Chunk records from the JSONL rows
# (which also carry "embedding" and "index_version" that are not Chunk fields).
_CHUNK_FIELDS = set(Chunk.__dataclass_fields__.keys())

_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./-]*")


def _tokenize(text: str) -> list[str]:
    """Lexical tokenizer for the file-index sparse scorer. Lowercased, keeps
    regulatory tokens like ``fr y-9c``, ``sr 11-7``, ``oauth2`` intact (the same
    intent as the Postgres ``simple`` tsvector config, G-01)."""
    return [match.group(0).lower() for match in _WORD.finditer(text)]


def _to_chunk(record: Mapping[str, Any]) -> Chunk:
    return Chunk(**{k: v for k, v in record.items() if k in _CHUNK_FIELDS})


def _cosine(a: list[float], b: list[float]) -> float:
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b, strict=False):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


class FileChunkRepository:
    """In-memory repository over the FileIndexWriter JSONL index.

    All public retrieval methods apply the access filter FIRST. A chunk that fails
    the filter is never scored and never returned, so it cannot be ranked,
    reranked, assembled, or cited.
    """

    def __init__(
        self,
        index_dir: Path | None = None,
        index_version: str | None = None,
    ) -> None:
        base = index_dir or DEFAULT_INDEX_DIR
        if index_version is None:
            manifest = load_latest_manifest()
            if manifest is None:
                raise FileNotFoundError("No manifest found; build the index before retrieval.")
            index_version = manifest["index_version"]
        path = base / index_version / "chunks.jsonl"
        if not path.exists():
            raise FileNotFoundError(f"File index not found at {path}.")
        self.index_version = index_version
        self._records: list[dict] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    self._records.append(json.loads(line))

    def _visible(self, access_filter: Mapping[str, Any]) -> Iterable[dict]:
        for record in self._records:
            if chunk_is_visible(record, access_filter):
                yield record

    def dense_candidates(
        self,
        query_vector: list[float],
        access_filter: Mapping[str, Any],
        *,
        top_k: int,
    ) -> list[tuple[Chunk, float]]:
        """Cosine-ranked, access-filtered dense candidates, best first."""
        scored: list[tuple[float, str, dict]] = []
        for record in self._visible(access_filter):
            score = _cosine(query_vector, record["embedding"])
            scored.append((score, record["chunk_id"], record))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [(_to_chunk(rec), score) for score, _, rec in scored[: max(0, top_k)]]

    def sparse_candidates(
        self,
        query_text: str,
        access_filter: Mapping[str, Any],
        *,
        top_k: int,
    ) -> list[tuple[Chunk, float]]:
        """Lexical (BM25-equivalent) ranked, access-filtered sparse candidates.

        File-index analogue of Postgres ts_rank_cd over the dual tsvector columns
        (G-01). Scores each visible chunk's ``embed_text`` (header + child text, so
        exact regulatory terms survive) with a tf-idf-ish BM25 score against the
        query terms. Zero-score chunks are dropped so the sparse list is honest.
        """
        q_terms = _tokenize(query_text)
        if not q_terms:
            return []
        q_set = list(dict.fromkeys(q_terms))

        visible = list(self._visible(access_filter))
        n_docs = len(visible)
        if n_docs == 0:
            return []

        # Document frequencies over the visible set only (so scoring never leaks
        # statistics about out-of-scope chunks).
        doc_tokens: list[tuple[dict, list[str]]] = [
            (rec, _tokenize(rec["embed_text"])) for rec in visible
        ]
        avg_len = sum(len(toks) for _, toks in doc_tokens) / n_docs if n_docs else 0.0
        df: dict[str, int] = {}
        for term in q_set:
            df[term] = sum(1 for _, toks in doc_tokens if term in toks)

        k1 = 1.5
        b = 0.75
        scored: list[tuple[float, str, dict]] = []
        for rec, toks in doc_tokens:
            if not toks:
                continue
            length = len(toks)
            tf_counts: dict[str, int] = {}
            for tok in toks:
                tf_counts[tok] = tf_counts.get(tok, 0) + 1
            score = 0.0
            for term in q_set:
                tf = tf_counts.get(term, 0)
                if tf == 0 or df.get(term, 0) == 0:
                    continue
                idf = math.log(1.0 + (n_docs - df[term] + 0.5) / (df[term] + 0.5))
                denom = tf + k1 * (1.0 - b + b * (length / avg_len if avg_len else 1.0))
                score += idf * (tf * (k1 + 1.0)) / denom
            if score > 0.0:
                scored.append((score, rec["chunk_id"], rec))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [(_to_chunk(rec), score) for score, _, rec in scored[: max(0, top_k)]]


class PostgresChunkRepository:
    """pgvector + tsvector repository (lazy psycopg). The access predicate is
    AND-ed into the SQL WHERE clause of BOTH the dense and sparse queries so
    disallowed rows are never scored (contract 3.1, 3.2)."""

    def __init__(self, dsn: str, index_version: str) -> None:
        self._dsn = dsn
        self.index_version = index_version

    def _connect(self):
        import psycopg  # lazy

        return psycopg.connect(self._dsn)

    def dense_candidates(
        self,
        query_vector: list[float],
        access_filter: Mapping[str, Any],
        *,
        top_k: int,
    ) -> list[tuple[Chunk, float]]:
        where, params = access_sql_where(access_filter)
        from pgvector.psycopg import register_vector

        with self._connect() as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT {_SELECT_COLS},
                           1 - (embedding <=> %(qvec)s) AS dense_score
                    FROM chunks
                    WHERE {where} AND index_version = %(idx)s
                    ORDER BY embedding <=> %(qvec)s
                    LIMIT %(k)s
                    """,
                    {**params, "qvec": query_vector, "idx": self.index_version, "k": top_k},
                )
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]
        return _rows_to_scored(rows, cols, "dense_score")

    def sparse_candidates(
        self,
        query_text: str,
        access_filter: Mapping[str, Any],
        *,
        top_k: int,
    ) -> list[tuple[Chunk, float]]:
        where, params = access_sql_where(access_filter)
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT {_SELECT_COLS},
                       ts_rank_cd(tsv_simple, plainto_tsquery('simple', %(q)s))
                       + ts_rank_cd(tsv_english, plainto_tsquery('english', %(q)s))
                           AS sparse_score
                FROM chunks
                WHERE {where} AND index_version = %(idx)s
                  AND (tsv_simple @@ plainto_tsquery('simple', %(q)s)
                       OR tsv_english @@ plainto_tsquery('english', %(q)s))
                ORDER BY sparse_score DESC
                LIMIT %(k)s
                """,
                {**params, "q": query_text, "idx": self.index_version, "k": top_k},
            )
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
        return _rows_to_scored(rows, cols, "sparse_score")


_SELECT_COLS = ", ".join(sorted(_CHUNK_FIELDS))


def _rows_to_scored(rows, cols, score_key) -> list[tuple[Chunk, float]]:
    out: list[tuple[Chunk, float]] = []
    for row in rows:
        record = dict(zip(cols, row, strict=False))
        score = float(record.pop(score_key))
        out.append((_to_chunk(record), score))
    return out


__all__ = ["FileChunkRepository", "PostgresChunkRepository"]
