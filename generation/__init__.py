"""Generation layer: grounded, citation-required generation plus the input and
output safety envelope (contracts.md sections 9, 5; gap-register G-04, G-14,
G-16, G-17).

- prompts.py: the system prompt and the untrusted-data CONTEXT_BLOCK delimiting.
- generator.py: build the prompt from an AssembledContext, call the Generator,
  parse raw citations.
- guardrails_input.py: injection/jailbreak + PII + scope checks on the query.
- guardrails_output.py: groundedness + PII leakage + citation re-validation
  (G-04) + advice-exceeds-policy refusal.
- pipeline.py: generate + output guardrail over an AssembledContext + role.
"""

from __future__ import annotations

from generation.generator import GeneratedAnswer, generate_answer, parse_citations
from generation.guardrails_input import InputVerdict, check_input
from generation.guardrails_output import OutputVerdict, check_output
from generation.pipeline import GenerationResponse, generate_with_guardrails
from generation.prompts import SYSTEM_PROMPT, build_user_message, render_context

__all__ = [
    "SYSTEM_PROMPT",
    "build_user_message",
    "render_context",
    "generate_answer",
    "parse_citations",
    "GeneratedAnswer",
    "check_input",
    "InputVerdict",
    "check_output",
    "OutputVerdict",
    "generate_with_guardrails",
    "GenerationResponse",
]
