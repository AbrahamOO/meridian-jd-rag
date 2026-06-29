"""Output guardrails on the generated answer (contracts.md sections 3.6, 5;
gap-register G-04).

Run by the graph ``output_guardrail`` node AFTER generate, BEFORE serialization.
In order:

1. citation re-validation (G-04): call retrieval.citations.validate_citations to
   strip any citation pointing to a doc not in the assembled context or one the
   role may no longer access. Defense in depth on top of the in-query pre-filter.
2. groundedness: every factual claim (sentence) must be supported by retrieved
   context AND carry a surviving citation. A claim left uncited after stripping,
   or unsupported by any context block, fails groundedness.
3. PII leakage: the synthetic-PII canary (or any detectable PII) must never
   appear in the answer. If it does, redact it and flag leakage.
4. advice-exceeding-policy refusal: an answer that gives a directive
   recommendation the context does not state (for example "you should ignore the
   limit") is refused.

If groundedness fails (any claim uncited or unsupported) OR a citation strip
leaves a claim uncited, the guardrail FORCES the insufficient-context boundary
rather than emit an uncited or hallucinated claim.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from core.models import (
    INSUFFICIENT_CONTEXT_STRING,
    AssembledContext,
    Citation,
)
from ingestion.pii import PIIRedactor, make_redactor
from retrieval.citations import validate_citations

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_CITATION_TAG = re.compile(r"\[MJD-(?:OPS|CMP|TEC|SEC|RSK|FIN|RET)-\d{4}\s+[^\]]+\]")
# A citation that trails its sentence (". [MJD-...]") is glued to that sentence so
# sentence splitting does not orphan the tag into a citationless fragment.
_TRAILING_CITATION = re.compile(
    r"([.!?])\s+(\[MJD-(?:OPS|CMP|TEC|SEC|RSK|FIN|RET)-\d{4}\s+[^\]]+\])"
)
_WORD = re.compile(r"[a-z0-9]+")
# Any MJD doc-id mentioned anywhere in the answer body (cited or not). Used to
# detect leakage of a document NOT present in the assembled context, which is how
# a document-sourced injection canary tries to surface a RESTRICTED doc id.
_DOC_ID_MENTION = re.compile(r"MJD-(?:OPS|CMP|TEC|SEC|RSK|FIN|RET)-\d{4}")

# Directive phrases that, if NOT echoing the context, indicate advice exceeding
# documented policy. High-precision so grounded imperative restatements pass.
_ADVICE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bi\s+(would\s+)?recommend\b", re.I),
    re.compile(r"\bmy\s+(advice|recommendation|opinion)\b", re.I),
    re.compile(r"\byou\s+should\s+(ignore|bypass|override|skip|disregard)\b", re.I),
    re.compile(r"\bin\s+my\s+(view|opinion|experience)\b", re.I),
)


@dataclass(frozen=True)
class OutputVerdict:
    """Result of the output guardrail.

    ``answer`` and ``citations`` are the possibly-rewritten outputs. ``abstained``
    / ``boundary_reason`` are set when the guardrail forces the
    insufficient-context boundary. ``flags`` accumulates guardrail_flags."""

    answer: str
    citations: list[Citation]
    abstained: bool
    boundary_triggered: bool
    boundary_reason: str
    flags: list[str] = field(default_factory=list)


def _strip_citation_tags(text: str) -> str:
    return _CITATION_TAG.sub("", text)


def _is_boundary(text: str) -> bool:
    stripped = text.strip().strip('"')
    return stripped == INSUFFICIENT_CONTEXT_STRING or stripped == (
        "That information is outside your current access scope."
    )


def _claim_sentences(answer: str) -> list[str]:
    """Sentences that assert a factual claim (non-empty after removing citation
    tags and not a pure boundary string)."""
    glued = _TRAILING_CITATION.sub(r"\1\2", answer.strip())
    sentences = _SENTENCE_SPLIT.split(glued)
    claims: list[str] = []
    for sentence in sentences:
        body = _strip_citation_tags(sentence).strip()
        if body:
            claims.append(sentence.strip())
    return claims


def _context_terms(assembled: AssembledContext) -> set[str]:
    terms: set[str] = set()
    for block in assembled.blocks:
        terms.update(_WORD.findall(block.text.lower()))
    return terms


def check_groundedness(
    answer: str,
    valid_citations: list[Citation],
    assembled: AssembledContext,
) -> tuple[bool, list[str]]:
    """Every claim sentence must (a) carry a surviving citation tag and (b) share
    lexical support with the context. Returns (grounded, flags)."""
    flags: list[str] = []
    valid_doc_ids = {c["doc_id"] for c in valid_citations}
    ctx_terms = _context_terms(assembled)

    for sentence in _claim_sentences(answer):
        tags = _CITATION_TAG.findall(sentence)
        cited_doc_ids = {
            m.group(0) for m in re.finditer(r"MJD-(?:OPS|CMP|TEC|SEC|RSK|FIN|RET)-\d{4}", sentence)
        }
        # (a) the sentence must carry a citation whose doc survived re-validation.
        if not tags or not (cited_doc_ids & valid_doc_ids):
            flags.append("uncited_claim")
            return False, flags
        # (b) lexical support: some content word of the claim appears in context.
        claim_words = {
            w for w in _WORD.findall(_strip_citation_tags(sentence).lower()) if len(w) > 3
        }
        if claim_words and ctx_terms and claim_words.isdisjoint(ctx_terms):
            flags.append("unsupported_claim")
            return False, flags

    return True, flags


def check_pii_leakage(answer: str, redactor: PIIRedactor | None = None) -> tuple[str, bool]:
    """Redact any PII that leaked into the answer. Returns (redacted, leaked)."""
    redactor = redactor or make_redactor(profile="ci")
    result = redactor.redact(answer)
    return result.text, result.count > 0


def check_advice_exceeds_policy(answer: str, assembled: AssembledContext) -> bool:
    """True if the answer offers a directive recommendation the context does not
    state (advice exceeding documented policy)."""
    for pattern in _ADVICE_PATTERNS:
        if pattern.search(answer):
            return True
    return False


def _force_insufficient(flags: list[str], reason_flag: str) -> OutputVerdict:
    out_flags = list(flags)
    if reason_flag not in out_flags:
        out_flags.append(reason_flag)
    return OutputVerdict(
        answer=INSUFFICIENT_CONTEXT_STRING,
        citations=[],
        abstained=True,
        boundary_triggered=True,
        boundary_reason="insufficient_context",
        flags=out_flags,
    )


def check_output(
    answer: str,
    citations: list[Citation],
    role: str,
    assembled: AssembledContext,
    *,
    active_strategy: str = "production",
    redactor: PIIRedactor | None = None,
) -> OutputVerdict:
    """Run the full output guardrail chain (G-04 + groundedness + PII + advice).

    Forces the insufficient-context boundary when stripping a citation leaves a
    claim uncited, when groundedness fails, or when advice exceeds policy.
    """
    flags: list[str] = []

    # If the generator already abstained / hit a boundary, pass it through clean
    # (no citations on a boundary answer).
    if _is_boundary(answer):
        return OutputVerdict(
            answer=answer.strip().strip('"'),
            citations=[],
            abstained=True,
            boundary_triggered=True,
            boundary_reason="insufficient_context",
            flags=flags,
        )

    # 1. Citation re-validation (G-04): strip out-of-context / out-of-scope cites.
    validation = validate_citations(citations, role, assembled, active_strategy=active_strategy)
    valid = validation.valid
    if validation.stripped:
        flags.append("citation_stripped")

    # Foreign-doc-id leakage: the answer body must never name a document not in
    # the assembled context. A document-sourced injection canary tries to surface
    # a RESTRICTED doc id (for example MJD-SEC-0002) by embedding it in retrieved
    # text the model then echoes. Any such mention is leakage of out-of-scope
    # document existence (invariant 10.2) and forces the boundary, fail-closed.
    context_doc_ids = {block.doc_id for block in assembled.blocks}
    mentioned = set(_DOC_ID_MENTION.findall(answer))
    if mentioned - context_doc_ids:
        return _force_insufficient(flags, "foreign_doc_reference")

    # 4. Advice exceeding documented policy -> refuse.
    if check_advice_exceeds_policy(answer, assembled):
        return _force_insufficient(flags, "advice_exceeds_policy")

    # 2. Groundedness: every claim must carry a surviving citation and be
    # supported by context. A strip that left a claim uncited fails here and
    # forces the boundary (contract 3.6).
    grounded, ground_flags = check_groundedness(answer, valid, assembled)
    flags.extend(ground_flags)
    if not grounded:
        return _force_insufficient(flags, "groundedness_failed")

    # 3. PII leakage: redact any PII that reached the answer, flag the leak.
    redacted, leaked = check_pii_leakage(answer, redactor)
    if leaked:
        flags.append("pii_leaked")

    return OutputVerdict(
        answer=redacted,
        citations=valid,
        abstained=False,
        boundary_triggered=False,
        boundary_reason="",
        flags=flags,
    )


__all__ = [
    "OutputVerdict",
    "check_output",
    "check_groundedness",
    "check_pii_leakage",
    "check_advice_exceeds_policy",
]
