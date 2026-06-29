"""Generation pipeline: generate + output guardrail (contracts.md sections 5, 9).

``generate_with_guardrails`` ties the generator and the output guardrail together
over an AssembledContext and a role, returning the contract response fields the
graph ``generate`` + ``output_guardrail`` nodes (and the API) emit:

    {answer, citations, boundary_triggered, boundary_reason, abstained,
     guardrail_flags, tokens}

The INPUT guardrail (generation/guardrails_input.py) runs earlier in the graph
``input_guardrail`` node, before retrieval; it is not re-run here. If the
assembled context is empty (allowed role, zero matches), the generator abstains
and the boundary reason is the insufficient-context boundary.
"""

from __future__ import annotations

from typing import TypedDict

from core.models import AssembledContext, Citation, TokenUsage
from generation.generator import generate_answer
from generation.guardrails_output import check_output
from ingestion.pii import PIIRedactor
from providers.base import Generator


class GenerationResponse(TypedDict):
    answer: str
    citations: list[Citation]
    boundary_triggered: bool
    boundary_reason: str
    abstained: bool
    guardrail_flags: list[str]
    tokens: TokenUsage


def generate_with_guardrails(
    query: str,
    role: str,
    assembled: AssembledContext,
    generator: Generator,
    *,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    active_strategy: str = "production",
    history: list[dict] | None = None,
    redactor: PIIRedactor | None = None,
) -> GenerationResponse:
    """Generate a grounded answer over ``assembled`` and run the output guardrail.

    Temperature is 0.0 by default (contract 1.2). Returns the contract response
    fields; ``tokens`` carries prompt/completion counts from the generator.
    """
    generated = generate_answer(
        query,
        assembled,
        generator,
        temperature=temperature,
        max_tokens=max_tokens,
        history=history,
    )

    verdict = check_output(
        generated.text,
        generated.citations,
        role,
        assembled,
        active_strategy=active_strategy,
        redactor=redactor,
    )

    tokens: TokenUsage = {
        "prompt": generated.prompt_tokens,
        "completion": generated.completion_tokens,
    }

    return GenerationResponse(
        answer=verdict.answer,
        citations=verdict.citations,
        boundary_triggered=verdict.boundary_triggered,
        boundary_reason=verdict.boundary_reason,
        abstained=verdict.abstained,
        guardrail_flags=verdict.flags,
        tokens=tokens,
    )


__all__ = ["generate_with_guardrails", "GenerationResponse"]
