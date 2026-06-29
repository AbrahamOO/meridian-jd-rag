"""Provider factory (contracts section 1.5).

The ONLY place that maps an adapter name to a concrete class. Selection is
config-driven. Cloud SDKs are imported lazily inside each branch so the light
mock/CI install never needs them.

Resolution of provider gaps (section 1.4):
- anthropic has no first-party embedding model: embedding selection resolves to
  the configured embedding.fallback adapter (default local). The substitution is
  reported via the returned provider's `resolved_from` marker for the manifest.
- anthropic/gemini have no first-party reranker: reranking resolves to local.
"""

from __future__ import annotations

import logging

from config.loader import Config
from providers.base import EmbeddingProvider, Generator, Reranker
from providers.local import LocalEmbeddingProvider, LocalGenerator, LocalReranker
from providers.mock import MockEmbeddingProvider, MockGenerator, MockReranker

logger = logging.getLogger("mjd.providers.factory")

# Adapters that cannot embed with a first-party model and must resolve embedding
# to the configured fallback adapter.
_NO_NATIVE_EMBEDDING = {"anthropic"}
# Adapters with no first-party reranker; reranking resolves to local.
_NO_NATIVE_RERANK = {"anthropic", "openai", "gemini"}


def _build_embedding(adapter: str, model: str) -> EmbeddingProvider:
    if adapter == "local":
        return LocalEmbeddingProvider(model=model)
    if adapter == "mock":
        return MockEmbeddingProvider(model=model)
    if adapter == "openai":
        from providers.openai_adapter import OpenAIEmbeddingProvider

        return OpenAIEmbeddingProvider(model=model)
    if adapter == "gemini":
        from providers.gemini_adapter import GeminiEmbeddingProvider

        return GeminiEmbeddingProvider(model=model)
    raise ValueError(f"Unknown embedding adapter: {adapter!r}")


def get_embedding_provider(cfg: Config) -> EmbeddingProvider:
    """Return the configured embedding provider.

    For adapters with no native embedding (anthropic), resolve to the configured
    embedding.fallback adapter and tag the provider with `resolved_from` so the
    manifest can record the substitution.
    """
    spec = cfg.providers.embedding
    adapter = spec.adapter
    resolved_from: str | None = None
    if adapter in _NO_NATIVE_EMBEDDING:
        resolved_from = adapter
        adapter = spec.fallback
        logger.info(
            "Embedding adapter %r has no native embedding; resolving to %r.",
            resolved_from,
            adapter,
        )
    provider = _build_embedding(adapter, spec.model)
    # Attach the substitution marker for the manifest (None when no resolution).
    try:
        object.__setattr__(provider, "resolved_from", resolved_from)
    except (AttributeError, TypeError):
        pass
    return provider


def get_generator(cfg: Config) -> Generator:
    spec = cfg.providers.generator
    adapter = spec.adapter
    if adapter == "local":
        return LocalGenerator(model=spec.model)
    if adapter == "mock":
        return MockGenerator(model=spec.model)
    if adapter == "anthropic":
        from providers.anthropic_adapter import AnthropicGenerator

        return AnthropicGenerator(model=spec.model)
    if adapter == "openai":
        from providers.openai_adapter import OpenAIGenerator

        return OpenAIGenerator(model=spec.model)
    if adapter == "gemini":
        from providers.gemini_adapter import GeminiGenerator

        return GeminiGenerator(model=spec.model)
    raise ValueError(f"Unknown generator adapter: {adapter!r}")


def get_reranker(cfg: Config) -> Reranker:
    spec = cfg.providers.reranker
    adapter = spec.adapter
    if adapter in _NO_NATIVE_RERANK:
        logger.info("Reranker adapter %r has no native reranker; resolving to local.", adapter)
        adapter = "local"
    if adapter == "local":
        return LocalReranker(model=spec.model)
    if adapter == "mock":
        return MockReranker(model=spec.model)
    raise ValueError(f"Unknown reranker adapter: {adapter!r}")
