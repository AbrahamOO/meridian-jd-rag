"""Zero-key local adapters (contracts section 1.4).

Embedding: sentence-transformers bge-small-en-v1.5 (lazy import). If the ML
stack is unavailable, falls back to the deterministic mock hash embedder so the
import never hard-crashes, logging a clear warning.

Reranker: a local cross-encoder (lazy import); falls back to lexical overlap.

Generator: abstain-only stub returning the insufficient-context boundary string
when no local LLM is configured; optional Ollama HTTP call if MJD_OLLAMA_URL is
set. Never crashes the service if the LLM is unavailable.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from collections.abc import Sequence

from providers.base import (
    INSUFFICIENT_CONTEXT_STRING,
    EmbeddingResult,
    GenerationResult,
    RerankResult,
)
from providers.mock import MockEmbeddingProvider, MockReranker

logger = logging.getLogger("mjd.providers.local")

_OLLAMA_TIMEOUT_S = 60.0


class LocalEmbeddingProvider:
    name = "local"

    def __init__(self, model: str = "bge-small-en-v1.5") -> None:
        self._model = model
        self._st_model = None  # lazily loaded SentenceTransformer
        self._fallback: MockEmbeddingProvider | None = None
        self._dim: int | None = None
        self._degraded = False
        self._load()

    def _load(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
        except Exception as exc:  # noqa: BLE001 - any import failure degrades safely
            logger.warning(
                "sentence-transformers unavailable (%s); local embedder degrading "
                "to deterministic mock hash embedder. Install the 'ml' extra for "
                "real local embeddings.",
                type(exc).__name__,
            )
            self._fallback = MockEmbeddingProvider(model=self._model)
            self._degraded = True
            return
        try:
            self._st_model = SentenceTransformer(self._model)
            self._dim = int(self._st_model.get_sentence_embedding_dimension() or 0)  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001 - model load/download failure
            logger.warning(
                "Failed to load local embedding model %s (%s); degrading to "
                "deterministic mock hash embedder.",
                self._model,
                type(exc).__name__,
            )
            self._st_model = None
            self._fallback = MockEmbeddingProvider(model=self._model)
            self._degraded = True

    @staticmethod
    def _query_prefix(text: str) -> str:
        # bge models use an asymmetric instruction prefix for queries.
        return "Represent this sentence for searching relevant passages: " + text

    def embed(self, texts: Sequence[str], *, kind: str = "document") -> EmbeddingResult:
        items = list(texts)
        if self._st_model is None:
            assert self._fallback is not None
            return self._fallback.embed(items, kind=kind)

        if not items:
            return EmbeddingResult(
                vectors=[],
                model=self._model,
                model_version="1.5",
                dim=self._dim or 0,
                tokens=0,
                cost_usd=0.0,
            )

        prepared = [self._query_prefix(t) if kind == "query" else t for t in items]
        raw = self._st_model.encode(prepared, normalize_embeddings=True, convert_to_numpy=True)
        vectors = [[float(v) for v in row] for row in raw]
        dim = len(vectors[0]) if vectors else (self._dim or 0)
        tokens = sum(len(t.split()) for t in items)
        return EmbeddingResult(
            vectors=vectors,
            model=self._model,
            model_version="1.5",
            dim=dim,
            tokens=tokens,
            cost_usd=0.0,
        )

    def health(self) -> dict:
        if self._st_model is None:
            return {
                "ok": True,
                "model": self._model,
                "dim": 256,
                "detail": "degraded: mock hash embedder (sentence-transformers absent)",
            }
        return {
            "ok": True,
            "model": self._model,
            "dim": self._dim or 0,
            "detail": "sentence-transformers",
        }


class LocalReranker:
    name = "local"

    def __init__(self, model: str = "bge-reranker-base") -> None:
        self._model = model
        self._cross_encoder = None
        self._fallback: MockReranker | None = None
        self._load()

    def _load(self) -> None:
        try:
            from sentence_transformers import CrossEncoder  # type: ignore
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Cross-encoder unavailable (%s); local reranker degrading to "
                "lexical overlap. Install the 'ml' extra for the real reranker.",
                type(exc).__name__,
            )
            self._fallback = MockReranker(model=self._model)
            return
        try:
            self._cross_encoder = CrossEncoder(self._model)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Failed to load local reranker %s (%s); degrading to lexical " "overlap.",
                self._model,
                type(exc).__name__,
            )
            self._cross_encoder = None
            self._fallback = MockReranker(model=self._model)

    def rerank(self, query: str, candidates: list[str], *, top_n: int) -> RerankResult:
        if self._cross_encoder is None:
            assert self._fallback is not None
            result = self._fallback.rerank(query, candidates, top_n=top_n)
            # Re-stamp the model id so the manifest reflects local selection.
            return RerankResult(
                order=result.order,
                scores=result.scores,
                model=self._model,
                model_version="lexical-fallback",
                cost_usd=0.0,
            )

        if not candidates:
            return RerankResult(
                order=[],
                scores=[],
                model=self._model,
                model_version="local",
                cost_usd=0.0,
            )
        pairs = [[query, candidate] for candidate in candidates]
        raw_scores = self._cross_encoder.predict(pairs)
        scored = sorted(
            ((float(score), index) for index, score in enumerate(raw_scores)),
            key=lambda pair: (-pair[0], pair[1]),
        )
        chosen = scored[: max(0, top_n)]
        return RerankResult(
            order=[index for _, index in chosen],
            scores=[score for score, _ in chosen],
            model=self._model,
            model_version="local",
            cost_usd=0.0,
        )

    def health(self) -> dict:
        detail = (
            "cross-encoder"
            if self._cross_encoder is not None
            else ("degraded: lexical overlap (cross-encoder absent)")
        )
        return {"ok": True, "model": self._model, "detail": detail}


class LocalGenerator:
    name = "local"

    def __init__(self, model: str = "local-instruct") -> None:
        self._model = model
        self._ollama_url = os.environ.get("MJD_OLLAMA_URL", "").strip() or None

    def _ollama_generate(
        self, *, system: str, messages: list[dict], temperature: float, max_tokens: int
    ) -> GenerationResult:
        assert self._ollama_url is not None
        payload = {
            "model": self._model,
            "system": system,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        request = urllib.request.Request(
            self._ollama_url.rstrip("/") + "/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=_OLLAMA_TIMEOUT_S) as response:
            data = json.loads(response.read().decode("utf-8"))
        text = (data.get("message") or {}).get("content", "").strip()
        if not text:
            text = INSUFFICIENT_CONTEXT_STRING
        prompt_tokens = int(data.get("prompt_eval_count", 0))
        completion_tokens = int(data.get("eval_count", 0))
        return GenerationResult(
            text=text,
            model=self._model,
            model_version="ollama",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=0.0,
            finish_reason="stop",
            raw_meta={"adapter": "local", "backend": "ollama"},
        )

    def generate(
        self,
        *,
        system: str,
        messages: list[dict],
        temperature: float = 0.0,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
    ) -> GenerationResult:
        if self._ollama_url is not None:
            try:
                return self._ollama_generate(
                    system=system,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except (urllib.error.URLError, OSError, ValueError) as exc:
                logger.warning(
                    "Ollama generation failed (%s); degrading to abstain-only "
                    "boundary response.",
                    type(exc).__name__,
                )

        # Abstain-only stub: no local LLM configured or Ollama unreachable.
        prompt_tokens = len(
            (system + " " + " ".join(str(m.get("content", "")) for m in messages)).split()
        )
        completion_tokens = len(INSUFFICIENT_CONTEXT_STRING.split())
        return GenerationResult(
            text=INSUFFICIENT_CONTEXT_STRING,
            model=self._model,
            model_version="abstain-stub",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=0.0,
            finish_reason="stop",
            raw_meta={"adapter": "local", "backend": "abstain-stub"},
        )

    def health(self) -> dict:
        backend = "ollama" if self._ollama_url is not None else "abstain-stub"
        return {"ok": True, "model": self._model, "detail": backend}
