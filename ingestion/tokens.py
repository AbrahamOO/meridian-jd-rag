"""Deterministic token counting (gap-register G-05).

A single shared heuristic so ingestion chunk token counts and retrieval budget
math agree. When a real tokenizer is unavailable (the CI/mock path has none),
fall back to ``len(text) // 4``, the contract-mandated heuristic. Whitespace
word count is used where the contract specifies word-count accounting (mock
generator), but chunk sizing uses the char-based heuristic consistently so eval
numbers are stable regardless of the active generator.
"""

from __future__ import annotations

_CHARS_PER_TOKEN = 4


def count_tokens(text: str) -> int:
    """Estimate token count with the contract heuristic ``len(text) // 4``.

    Deterministic, dependency-free, and consistent across ingestion and
    retrieval so eval numbers do not drift with the active provider.
    """
    if not text:
        return 0
    return max(1, len(text) // _CHARS_PER_TOKEN)
