"""Deterministic mock adapters (contracts section 1.7, gap-register G-12).

These are pure stdlib and fully deterministic across processes and OSes so CI
eval numbers are byte-stable. No network, no clock, no unseeded randomness.
"""

from __future__ import annotations

import hashlib
import math
import random
import re
from collections.abc import Sequence

from providers.base import (
    INSUFFICIENT_CONTEXT_STRING,
    EmbeddingResult,
    GenerationResult,
    RerankResult,
)

MOCK_EMBED_DIM = 256
_UNIT_SEP = "\x1f"
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
# Matches a CONTEXT_BLOCK opening tag carrying the doc id and section path so the
# mock generator can emit verbatim citation tags taken from the context metadata.
_CONTEXT_BLOCK = re.compile(
    r"<<<CONTEXT_BLOCK\s+id=(?P<doc_id>\S+)\s+section=\"(?P<section>[^\"]*)\">>>"
    r"(?P<body>.*?)<<<END_CONTEXT_BLOCK>>>",
    re.DOTALL,
)


def _seed_from_digest(digest: bytes) -> int:
    return int.from_bytes(digest, byteorder="big", signed=False)


def _mock_vector(model_id: str, kind: str, text: str) -> list[float]:
    digest = hashlib.sha256(
        (model_id + _UNIT_SEP + kind + _UNIT_SEP + text).encode("utf-8")
    ).digest()
    rng = random.Random(_seed_from_digest(digest))
    raw = [rng.uniform(-1.0, 1.0) for _ in range(MOCK_EMBED_DIM)]
    norm = math.sqrt(sum(value * value for value in raw))
    if norm == 0.0:
        return raw
    return [value / norm for value in raw]


class MockEmbeddingProvider:
    name = "mock"

    def __init__(self, model: str = "mock-embed-256") -> None:
        self._model = model

    def embed(self, texts: Sequence[str], *, kind: str = "document") -> EmbeddingResult:
        items = list(texts)
        if not items:
            return EmbeddingResult(
                vectors=[],
                model=self._model,
                model_version="mock",
                dim=MOCK_EMBED_DIM,
                tokens=0,
                cost_usd=0.0,
            )
        vectors = [_mock_vector(self._model, kind, text) for text in items]
        tokens = sum(len(text.split()) for text in items)
        return EmbeddingResult(
            vectors=vectors,
            model=self._model,
            model_version="mock",
            dim=MOCK_EMBED_DIM,
            tokens=tokens,
            cost_usd=0.0,
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "dim": MOCK_EMBED_DIM, "detail": "mock"}


class MockGenerator:
    name = "mock"

    def __init__(self, model: str = "mock-gen") -> None:
        self._model = model

    def _extract(self, system: str, messages: list[dict]) -> str:
        """Build a deterministic grounded answer: first sentence of each context
        block plus a verbatim citation tag taken from the block metadata. If no
        context block is present, return the insufficient-context boundary."""
        corpus = system + "\n" + "\n".join(str(m.get("content", "")) for m in messages)
        blocks = list(_CONTEXT_BLOCK.finditer(corpus))
        if not blocks:
            return INSUFFICIENT_CONTEXT_STRING

        parts: list[str] = []
        for block in blocks:
            body = block.group("body").strip()
            if not body:
                continue
            first_sentence = _SENTENCE_SPLIT.split(body, maxsplit=1)[0].strip()
            if not first_sentence:
                continue
            doc_id = block.group("doc_id")
            section = block.group("section")
            parts.append(f"{first_sentence} [{doc_id} {section}]")

        if not parts:
            return INSUFFICIENT_CONTEXT_STRING
        return " ".join(parts)

    def generate(
        self,
        *,
        system: str,
        messages: list[dict],
        temperature: float = 0.0,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
    ) -> GenerationResult:
        text = self._extract(system, messages)
        prompt_tokens = len(
            (system + " " + " ".join(str(m.get("content", "")) for m in messages)).split()
        )
        completion_tokens = len(text.split())
        return GenerationResult(
            text=text,
            model=self._model,
            model_version="mock",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=0.0,
            finish_reason="stop",
            raw_meta={"adapter": "mock"},
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "detail": "mock"}


def _tokens(text: str) -> set[str]:
    return set(text.lower().split())


class MockReranker:
    name = "mock"

    def __init__(self, model: str = "mock-rerank") -> None:
        self._model = model

    def rerank(self, query: str, candidates: list[str], *, top_n: int) -> RerankResult:
        if not candidates:
            return RerankResult(
                order=[],
                scores=[],
                model=self._model,
                model_version="mock",
                cost_usd=0.0,
            )
        query_tokens = _tokens(query)
        scored: list[tuple[float, int]] = []
        for index, candidate in enumerate(candidates):
            cand_tokens = _tokens(candidate)
            union = query_tokens | cand_tokens
            jaccard = (len(query_tokens & cand_tokens) / len(union)) if union else 0.0
            scored.append((jaccard, index))
        # Higher Jaccard first; ties broken by original index ascending.
        scored.sort(key=lambda pair: (-pair[0], pair[1]))
        limit = max(0, top_n)
        chosen = scored[:limit]
        return RerankResult(
            order=[index for _, index in chosen],
            scores=[score for score, _ in chosen],
            model=self._model,
            model_version="mock",
            cost_usd=0.0,
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "detail": "mock"}
