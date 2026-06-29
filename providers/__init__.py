"""Meridian J.D. RAG provider abstraction layer.

Exposes the Protocols, result dataclasses, the typed error, the secret
resolver, and the factory entry points. Concrete cloud adapters are imported
lazily by the factory so the light mock/CI path never pulls their SDKs.
"""

from providers.base import (
    ACCESS_BOUNDARY_STRING,
    INSUFFICIENT_CONTEXT_STRING,
    EmbeddingProvider,
    EmbeddingResult,
    GenerationResult,
    Generator,
    MissingSecretError,
    Reranker,
    RerankResult,
)
from providers.factory import (
    get_embedding_provider,
    get_generator,
    get_reranker,
)
from providers.secrets import resolve_secret

__all__ = [
    "ACCESS_BOUNDARY_STRING",
    "INSUFFICIENT_CONTEXT_STRING",
    "EmbeddingProvider",
    "EmbeddingResult",
    "Generator",
    "GenerationResult",
    "MissingSecretError",
    "RerankResult",
    "Reranker",
    "get_embedding_provider",
    "get_generator",
    "get_reranker",
    "resolve_secret",
]
