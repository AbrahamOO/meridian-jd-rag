"""Meridian J.D. RAG configuration package.

Exposes the layered config loader and the typed Config model. See
config/loader.py for the precedence rules (default < profile < local < env).
"""

from config.loader import (
    AccessConfig,
    ChunkingConfig,
    Config,
    EmbeddingConfig,
    FailClosedError,
    GenerationConfig,
    GeneratorConfig,
    ProvidersConfig,
    RerankerConfig,
    RetrievalConfig,
    load_config,
)

__all__ = [
    "AccessConfig",
    "ChunkingConfig",
    "Config",
    "EmbeddingConfig",
    "FailClosedError",
    "GenerationConfig",
    "GeneratorConfig",
    "ProvidersConfig",
    "RerankerConfig",
    "RetrievalConfig",
    "load_config",
]
