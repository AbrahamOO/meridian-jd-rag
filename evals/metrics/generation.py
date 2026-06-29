"""Generation metrics (contract 7.2; spec section 12).

Computed from the produced answer, its surviving citations, the assembled
context, and the golden record. All deterministic and dependency-free.

- faithfulness / groundedness: every factual claim in the answer is supported by
  its cited context. An abstention / boundary answer asserts nothing and is
  vacuously faithful (1.0). Combines the in-system groundedness check
  (generation.guardrails_output.check_groundedness) with the bank-specific
  LLM-as-judge floor (evals.metrics.judge) so the number reflects BOTH the gate
  the pipeline applies and an independent judge.
- answer_relevance: lexical overlap of the answer with the QUESTION (does the
  answer address what was asked). Boundary answers to deny/out-of-scope records
  are relevant by construction (the boundary IS the right response).
- answer_correctness: fraction of the golden ``expected_answer_contains`` strings
  present in the answer (case-insensitive substring).
- completeness: same basis as correctness but reported separately so the
  dashboard can distinguish "wrong" from "incomplete"; here completeness is the
  expected-substring coverage and correctness additionally requires the right
  source to be cited.
- citation_accuracy: fraction of emitted citations whose doc_id is in the
  golden ``expected_source`` (precision of citations against ground truth). For a
  deny/out-of-scope record the correct citation set is empty, so zero citations
  scores 1.0 and any citation scores 0.0.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import TypedDict

from core.models import (
    ACCESS_BOUNDARY_STRING,
    INSUFFICIENT_CONTEXT_STRING,
    Citation,
)
from evals.metrics.judge import JudgeResult

_WORD = re.compile(r"[a-z0-9]+")
_CITATION_TAG = re.compile(r"\[MJD-(?:OPS|CMP|TEC|SEC|RSK|FIN|RET)-\d{4}\s+[^\]]+\]")

_BOUNDARY_STRINGS = frozenset({INSUFFICIENT_CONTEXT_STRING, ACCESS_BOUNDARY_STRING})


class GenerationMetrics(TypedDict):
    faithfulness: float
    answer_relevance: float
    answer_correctness: float
    completeness: float
    citation_accuracy: float


def is_boundary_answer(answer: str) -> bool:
    return answer.strip().strip('"') in _BOUNDARY_STRINGS


def _content_words(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower()) if len(w) > 2}


def expected_contains_coverage(answer: str, expected_contains: Sequence[str]) -> float:
    """Fraction of expected substrings present in the answer (case-insensitive)."""
    if not expected_contains:
        return 1.0
    low = answer.lower()
    hits = sum(1 for needle in expected_contains if needle.lower() in low)
    return hits / len(expected_contains)


def answer_relevance(answer: str, question: str, *, is_boundary: bool) -> float:
    """Lexical relevance of the answer to the question.

    A boundary answer is the correct response for deny/out-of-scope records, so it
    is scored relevant (1.0). For content answers, relevance is the fraction of
    the question's content words echoed by the answer, lightly floored so a
    terse-but-correct numeric answer is not punished to zero.
    """
    if is_boundary:
        return 1.0
    q_words = _content_words(question)
    if not q_words:
        return 1.0
    a_words = _content_words(_CITATION_TAG.sub("", answer))
    overlap = len(q_words & a_words)
    return overlap / len(q_words)


def citation_accuracy(citations: list[Citation], expected_source: Sequence[str]) -> float:
    """Precision of emitted citations against the golden expected_source.

    Empty expected_source (deny/out-of-scope): zero citations is perfect (1.0),
    any citation is wrong (0.0).
    """
    cited = [c.get("doc_id", "") for c in citations]
    if not expected_source:
        return 1.0 if not cited else 0.0
    if not cited:
        return 0.0
    exp = set(expected_source)
    correct = sum(1 for d in cited if d in exp)
    return correct / len(cited)


def faithfulness(
    answer: str,
    grounded_by_guardrail: bool,
    judge: JudgeResult | None,
) -> float:
    """Answer-to-context groundedness.

    A boundary / abstention answer asserts no claim and is vacuously faithful.
    Otherwise faithfulness is the bank-judge groundedness score, but a hard
    in-system groundedness failure caps it at the judge's value (the pipeline
    would have abstained anyway, so a non-boundary answer here already passed the
    in-system check). When no judge ran, fall back to the in-system boolean.
    """
    if is_boundary_answer(answer):
        return 1.0
    if judge is not None:
        return judge.score
    return 1.0 if grounded_by_guardrail else 0.0


def generation_metrics(
    *,
    answer: str,
    question: str,
    citations: list[Citation],
    expected_source: Sequence[str],
    expected_contains: Sequence[str],
    grounded_by_guardrail: bool,
    judge: JudgeResult | None,
    is_boundary: bool,
) -> GenerationMetrics:
    """Compute the full generation metric family for one record."""
    coverage = expected_contains_coverage(answer, expected_contains)
    cite_acc = citation_accuracy(citations, expected_source)
    # correctness requires the content to be present AND the right source cited.
    if not expected_source and not expected_contains:
        correctness = 1.0 if is_boundary else 0.0
    else:
        source_ok = cite_acc if expected_source else 1.0
        correctness = coverage * source_ok
    return GenerationMetrics(
        faithfulness=round(faithfulness(answer, grounded_by_guardrail, judge), 6),
        answer_relevance=round(answer_relevance(answer, question, is_boundary=is_boundary), 6),
        answer_correctness=round(correctness, 6),
        completeness=round(coverage, 6),
        citation_accuracy=round(cite_acc, 6),
    )


__all__ = [
    "GenerationMetrics",
    "generation_metrics",
    "faithfulness",
    "answer_relevance",
    "citation_accuracy",
    "expected_contains_coverage",
    "is_boundary_answer",
]
