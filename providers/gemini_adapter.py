"""Gemini adapter (contracts section 1.4).

Provides an embedding provider (text-embedding-004) and a generator
(gemini-1.5-pro). No first-party reranker (the factory resolves reranking to
local for gemini). Keys via resolve_secret; a missing key raises
MissingSecretError at construction.
"""

from __future__ import annotations

from collections.abc import Sequence

from providers.base import (
    EmbeddingResult,
    GenerationResult,
    MissingSecretError,
)
from providers.secrets import resolve_secret

# Pinned indicative pricing (USD per token) for reproducible cost accounting.
_EMBED_USD_PER_TOKEN = 0.0  # text-embedding-004 is free-tier; recorded as 0.0
_GEN_INPUT_USD_PER_TOKEN = 1.25 / 1_000_000  # gemini-1.5-pro
_GEN_OUTPUT_USD_PER_TOKEN = 5.0 / 1_000_000


def _client():
    api_key = resolve_secret("GEMINI_API_KEY")
    if not api_key:
        raise MissingSecretError("GEMINI_API_KEY is required for the gemini adapter.")
    try:
        from google import genai  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise MissingSecretError(
            "The 'google-genai' SDK is not installed; install the 'cloud' extra."
        ) from exc
    return genai.Client(api_key=api_key)


def _word_tokens(*parts: str) -> int:
    return sum(len(part.split()) for part in parts)


class GeminiEmbeddingProvider:
    name = "gemini"

    def __init__(self, model: str = "text-embedding-004") -> None:
        self._model = model
        self._sdk = _client()

    def embed(self, texts: Sequence[str], *, kind: str = "document") -> EmbeddingResult:
        items = list(texts)
        if not items:
            return EmbeddingResult(
                vectors=[],
                model=self._model,
                model_version=self._model,
                dim=0,
                tokens=0,
                cost_usd=0.0,
            )
        result = self._sdk.models.embed_content(model=self._model, contents=items)
        vectors = [list(embedding.values) for embedding in result.embeddings]
        dim = len(vectors[0]) if vectors else 0
        tokens = _word_tokens(*items)
        return EmbeddingResult(
            vectors=vectors,
            model=self._model,
            model_version=self._model,
            dim=dim,
            tokens=tokens,
            cost_usd=round(tokens * _EMBED_USD_PER_TOKEN, 6),
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "dim": 768, "detail": "gemini"}


class GeminiGenerator:
    name = "gemini"

    def __init__(self, model: str = "gemini-1.5-pro") -> None:
        self._model = model
        self._sdk = _client()

    def generate(
        self,
        *,
        system: str,
        messages: list[dict],
        temperature: float = 0.0,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
    ) -> GenerationResult:
        from google.genai import types  # type: ignore

        contents = [
            {
                "role": "model" if m.get("role") == "assistant" else "user",
                "parts": [{"text": str(m.get("content", ""))}],
            }
            for m in messages
        ]
        config = types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            max_output_tokens=max_tokens,
            stop_sequences=stop or None,
        )
        response = self._sdk.models.generate_content(
            model=self._model, contents=contents, config=config
        )
        text = response.text or ""
        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
        completion_tokens = int(getattr(usage, "candidates_token_count", 0) or 0)
        finish_reason = "stop"
        cost = (
            prompt_tokens * _GEN_INPUT_USD_PER_TOKEN + completion_tokens * _GEN_OUTPUT_USD_PER_TOKEN
        )
        return GenerationResult(
            text=text,
            model=self._model,
            model_version=self._model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=round(cost, 6),
            finish_reason=finish_reason,
            raw_meta={"adapter": "gemini"},
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "detail": "gemini"}
