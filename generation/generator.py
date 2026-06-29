"""Grounded generation over an AssembledContext (contracts.md sections 1.2, 9).

``generate_answer`` builds the system + user prompt from an AssembledContext,
calls the configured Generator provider at temperature 0.0, and returns the raw
answer text plus the citations the model emitted, parsed from the inline
``[doc_id section_path]`` tags. Citation re-validation and groundedness are the
job of the output guardrail (generation/guardrails_output.py); this module only
produces the candidate answer and its raw citations.

The Generator provider is swappable behind the contract (default local, mock in
CI, anthropic/gemini in hybrid); the model choice is not load-bearing here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from core.models import AssembledContext, Citation
from generation.prompts import SYSTEM_PROMPT, build_user_message
from providers.base import Generator

# Inline citation tag: [doc_id section_path]. doc_id matches the MJD id regex; the
# section path is whatever follows up to the closing bracket (e.g. "3 > 3.2.1").
_CITATION_RE = re.compile(
    r"\[(?P<doc_id>MJD-(?:OPS|CMP|TEC|SEC|RSK|FIN|RET)-\d{4})\s+(?P<section>[^\]]+)\]"
)


@dataclass(frozen=True)
class GeneratedAnswer:
    text: str
    citations: list[Citation]
    finish_reason: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float


def parse_citations(text: str, assembled: AssembledContext) -> list[Citation]:
    """Parse inline [doc_id section_path] tags into Citation objects.

    title and version are recovered from the matching ContextBlock so the emitted
    citation is the full contract-3.6 shape. A tag whose doc_id is not in the
    assembled context still produces a Citation (with empty title/version) so the
    output guardrail can STRIP it; we never fabricate metadata for an unknown doc.
    Duplicate (doc_id, section_path) tags are de-duplicated, order preserved.
    """
    by_doc = {block.doc_id: block for block in assembled.blocks}
    seen: set[tuple[str, str]] = set()
    citations: list[Citation] = []
    for match in _CITATION_RE.finditer(text):
        doc_id = match.group("doc_id")
        section = match.group("section").strip()
        key = (doc_id, section)
        if key in seen:
            continue
        seen.add(key)
        block = by_doc.get(doc_id)
        citation: Citation = {
            "doc_id": doc_id,
            "title": block.title if block is not None else "",
            "section_path": section,
            "version": block.version if block is not None else "",
        }
        citations.append(citation)
    return citations


def generate_answer(
    query: str,
    assembled: AssembledContext,
    generator: Generator,
    *,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    history: list[dict] | None = None,
) -> GeneratedAnswer:
    """Build the prompt, call the generator at temperature 0.0, return the answer
    and the raw (un-revalidated) citations parsed from it."""
    history = history or []
    user_message = build_user_message(query, assembled)
    messages: list[dict] = list(history) + [{"role": "user", "content": user_message}]

    result = generator.generate(
        system=SYSTEM_PROMPT,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    citations = parse_citations(result.text, assembled)
    return GeneratedAnswer(
        text=result.text,
        citations=citations,
        finish_reason=result.finish_reason,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
        cost_usd=result.cost_usd,
    )


__all__ = ["generate_answer", "parse_citations", "GeneratedAnswer"]
