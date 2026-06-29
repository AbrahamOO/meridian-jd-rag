"""Batch embedding over the provider interface (contract 1.1).

Embeds each chunk's `embed_text` (contextual header + child text) with kind
"document". Empty-after-normalization strings are rejected by the caller, never
silently embedded (contract 1.1 hard rule). Returns vectors aligned to the input
chunk order plus the provider's model/version/dim/token/cost so the manifest can
record exactly what produced the index.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from core.models import Chunk
from providers.base import EmbeddingProvider


@dataclass(frozen=True)
class EmbeddedBatch:
    vectors: list[list[float]]
    model: str
    model_version: str
    dim: int
    tokens: int
    cost_usd: float
    resolved_from: str | None


def embed_chunks(
    provider: EmbeddingProvider,
    chunks: Sequence[Chunk],
    *,
    batch_size: int = 64,
) -> EmbeddedBatch:
    if not chunks:
        return EmbeddedBatch([], "", "", 0, 0, 0.0, None)

    for chunk in chunks:
        if not chunk.embed_text.strip():
            raise ValueError(
                f"FATAL: chunk {chunk.chunk_id} has empty embed_text; refusing to embed."
            )

    vectors: list[list[float]] = []
    total_tokens = 0
    total_cost = 0.0
    model = ""
    model_version = ""
    dim = 0
    texts = [c.embed_text for c in chunks]
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        result = provider.embed(batch, kind="document")
        vectors.extend(result.vectors)
        total_tokens += result.tokens
        total_cost += result.cost_usd
        model = result.model
        model_version = result.model_version
        dim = result.dim

    if len(vectors) != len(chunks):
        raise ValueError(
            f"Embedding count mismatch: {len(vectors)} vectors for {len(chunks)} chunks."
        )

    resolved_from = getattr(provider, "resolved_from", None)
    return EmbeddedBatch(
        vectors=vectors,
        model=model,
        model_version=model_version,
        dim=dim,
        tokens=total_tokens,
        cost_usd=round(total_cost, 6),
        resolved_from=resolved_from,
    )
