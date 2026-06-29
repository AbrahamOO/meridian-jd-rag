"""Provider abstraction layer: contract types and Protocols.

These are the BINDING interfaces from contracts.md section 1. Every adapter
(local, mock, anthropic, openai, gemini) implements these Protocols exactly.
Field names, signatures, and semantics are normative and case-sensitive.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


class MissingSecretError(RuntimeError):
    """Raised by a cloud adapter at CONSTRUCTION time when a required secret is
    absent. Never raised at call time, and never carries the secret value."""


@dataclass(frozen=True)
class EmbeddingResult:
    vectors: list[list[float]]  # one vector per input, order preserved
    model: str  # canonical model id, e.g. "text-embedding-3-large"
    model_version: str  # provider-reported version or pinned tag
    dim: int  # vector dimensionality, must equal len(vectors[0])
    tokens: int  # total input tokens billed across the batch
    cost_usd: float  # computed cost for this call, 6dp


@dataclass(frozen=True)
class GenerationResult:
    text: str
    model: str
    model_version: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float  # 6dp
    finish_reason: str  # "stop" | "length" | "content_filter" | "error"
    raw_meta: dict  # adapter-specific, never logged unredacted


@dataclass(frozen=True)
class RerankResult:
    order: list[int]  # indices into the input candidate list, best first
    scores: list[float]  # aligned to `order`, higher is more relevant
    model: str
    model_version: str
    cost_usd: float  # 6dp, 0.0 for local/mock


@runtime_checkable
class EmbeddingProvider(Protocol):
    name: str  # one of the adapter names

    def embed(self, texts: Sequence[str], *, kind: str = "document") -> EmbeddingResult:
        """Embed a batch of texts. ``kind`` in {"document","query"}; adapters that
        do not support asymmetric embedding MUST ignore kind but still accept it.
        Empty input returns EmbeddingResult(vectors=[], tokens=0, cost_usd=0.0)."""
        ...

    def health(self) -> dict:
        """{"ok": bool, "model": str, "dim": int, "detail": str}"""
        ...


@runtime_checkable
class Generator(Protocol):
    name: str

    def generate(
        self,
        *,
        system: str,
        messages: list[dict],  # [{"role":"user"|"assistant","content":str}, ...]
        temperature: float = 0.0,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
    ) -> GenerationResult: ...

    def health(self) -> dict: ...


@runtime_checkable
class Reranker(Protocol):
    name: str

    def rerank(self, query: str, candidates: list[str], *, top_n: int) -> RerankResult:
        """Return at most top_n entries in ``order``. Empty candidates returns
        RerankResult(order=[], scores=[], ...)."""
        ...

    def health(self) -> dict: ...


# Normative boundary strings (contracts section 9). Imported by mock and real
# generators so the abstention text is identical everywhere.
INSUFFICIENT_CONTEXT_STRING = (
    "I do not have an authoritative policy on that in the documents available to " "your role."
)
ACCESS_BOUNDARY_STRING = "That information is outside your current access scope."
