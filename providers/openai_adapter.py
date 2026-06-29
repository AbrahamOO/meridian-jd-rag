"""OpenAI adapter (contracts section 1.4).

Provides an embedding provider (text-embedding-3-large) and a generator. No
first-party reranker (the factory resolves reranking to local for openai).
Keys via resolve_secret; a missing key raises MissingSecretError at
construction.
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
_EMBED_USD_PER_TOKEN = 0.13 / 1_000_000  # text-embedding-3-large
_GEN_INPUT_USD_PER_TOKEN = 2.5 / 1_000_000  # gpt-4o
_GEN_OUTPUT_USD_PER_TOKEN = 10.0 / 1_000_000


def _client():
    api_key = resolve_secret("OPENAI_API_KEY")
    if not api_key:
        raise MissingSecretError("OPENAI_API_KEY is required for the openai adapter.")
    try:
        import openai  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise MissingSecretError(
            "The 'openai' SDK is not installed; install the 'cloud' extra."
        ) from exc
    return openai.OpenAI(api_key=api_key)


class OpenAIEmbeddingProvider:
    name = "openai"

    def __init__(self, model: str = "text-embedding-3-large") -> None:
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
        response = self._sdk.embeddings.create(model=self._model, input=items)
        vectors = [list(item.embedding) for item in response.data]
        dim = len(vectors[0]) if vectors else 0
        tokens = int(response.usage.total_tokens)
        return EmbeddingResult(
            vectors=vectors,
            model=self._model,
            model_version=self._model,
            dim=dim,
            tokens=tokens,
            cost_usd=round(tokens * _EMBED_USD_PER_TOKEN, 6),
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "dim": 3072, "detail": "openai"}


class OpenAIGenerator:
    name = "openai"

    def __init__(self, model: str = "gpt-4o") -> None:
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
        chat_messages = [{"role": "system", "content": system}, *messages]
        response = self._sdk.chat.completions.create(
            model=self._model,
            messages=chat_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop or None,
        )
        choice = response.choices[0]
        text = choice.message.content or ""
        prompt_tokens = int(response.usage.prompt_tokens)
        completion_tokens = int(response.usage.completion_tokens)
        finish = choice.finish_reason or "stop"
        finish_reason = {
            "length": "length",
            "stop": "stop",
            "content_filter": "content_filter",
        }.get(finish, finish)
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
            raw_meta={"adapter": "openai", "finish_reason": finish},
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "detail": "openai"}
