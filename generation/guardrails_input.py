"""Input guardrails on the USER query (contracts.md section 5; gap-register
G-15, G-16, G-17).

Three checks, run by the graph ``input_guardrail`` node, in this order:

1. injection / jailbreak detection (G-17): user-supplied attempts to override the
   system prompt or exfiltrate out-of-scope content. Match -> boundary
   ``injection_blocked``.
2. PII detection on the query: flagged so the audit sink redacts before durable
   logging (G-03). Detection here is a flag, not a block: a legitimate question
   may contain an account number.
3. scope check (G-16): a clearly non-bank question -> boundary ``out_of_scope``.
   Conservative: when uncertain, PROCEED (retrieval will abstain on empty
   results) rather than falsely refuse a real bank question.

This is the defense against USER-vector injection. Document-sourced injection is
a separate vector handled by prompt delimiting in generate and is never trusted
(see generation/prompts.py and generation/guardrails_output.py).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ingestion.pii import PIIRedactor, make_redactor

# --- injection / jailbreak patterns (G-17) ----------------------------------
# Conservative, high-precision patterns for user-vector jailbreak attempts. We
# match the intent to override instructions or exfiltrate restricted/out-of-scope
# content, not mere mentions of policy words.
_INJECTION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bignore\b.{0,40}\b(previous|prior|above|all|your)\b.{0,20}\binstruction", re.I),
    re.compile(
        r"\bdisregard\b.{0,40}\b(previous|prior|above|all|your|the)\b.{0,20}\b(instruction|polic|rule)",
        re.I,
    ),
    re.compile(r"\boverride\b.{0,30}\b(instruction|polic|rule|access|control)", re.I),
    re.compile(r"\bsystem\s+(prompt|override|message)\b", re.I),
    re.compile(
        r"\b(reveal|disclose|show|dump|leak|exfiltrate|print)\b.{0,40}\b(restricted|confidential|secret|all\s+document|every\s+document|system\s+prompt)",
        re.I,
    ),
    re.compile(
        r"\b(bypass|circumvent|escalate|defeat)\b.{0,30}\b(access|control|restriction|permission|role)",
        re.I,
    ),
    re.compile(r"\bregardless\s+of\b.{0,20}\b(role|access|permission|scope|clearance)", re.I),
    re.compile(
        r"\b(you\s+are\s+now|act\s+as|pretend\s+to\s+be)\b.{0,30}\b(admin|root|superuser|developer\s+mode|dan)\b",
        re.I,
    ),
    re.compile(r"\bdeveloper\s+mode\b", re.I),
    re.compile(r"\bjailbreak\b", re.I),
)

# --- scope check (G-16) -----------------------------------------------------
# Lexicon of bank-knowledge terms. Presence of ANY term marks the query in-scope.
# This is a recall-biased allowlist: we would rather pass a borderline question to
# retrieval (which abstains on empty) than falsely refuse it.
_BANK_TERMS: tuple[str, ...] = (
    "policy",
    "policies",
    "procedure",
    "procedures",
    "standard",
    "standards",
    "runbook",
    "guideline",
    "control",
    "controls",
    "compliance",
    "aml",
    "bsa",
    "kyc",
    "cdd",
    "edd",
    "cip",
    "sar",
    "ctr",
    "ofac",
    "sanction",
    "sanctions",
    "wire",
    "transfer",
    "transaction",
    "account",
    "onboarding",
    "dispute",
    "chargeback",
    "limit",
    "limits",
    "approval",
    "dual-approval",
    "fraud",
    "risk",
    "credit",
    "capital",
    "stress",
    "basel",
    "model",
    "reconciliation",
    "ledger",
    "gl",
    "reporting",
    "call report",
    "audit",
    "evidence",
    "branch",
    "vault",
    "cash",
    "complaint",
    "privacy",
    "glba",
    "reg",
    "ecoa",
    "lending",
    "retention",
    "records",
    "incident",
    "vulnerability",
    "patch",
    "crypto",
    "cryptographic",
    "cipher",
    "encryption",
    "key",
    "secret",
    "secrets",
    "rotation",
    "iam",
    "access",
    "authentication",
    "authorization",
    "oauth",
    "oidc",
    "network",
    "segmentation",
    "zero trust",
    "siem",
    "logging",
    "monitoring",
    "pam",
    "privileged",
    "sdlc",
    "pipeline",
    "ci/cd",
    "infrastructure",
    "cloud",
    "change management",
    "release",
    "threat",
    "data classification",
    "meridian",
    "bank",
    "customer",
    "regulatory",
    "regulation",
    "due diligence",
    "screening",
    "escalation",
    "threshold",
    "thresholds",
    "document",
    "section",
)

# Clearly non-bank topics: if the query is dominated by these and carries no bank
# term, it is out of scope. Kept small and high-precision (G-16 conservatism).
_OUT_OF_SCOPE_TERMS: tuple[str, ...] = (
    "weather",
    "recipe",
    "joke",
    "poem",
    "movie",
    "song",
    "lyrics",
    "football",
    "basketball",
    "celebrity",
    "horoscope",
    "stock price",
    "bitcoin price",
    "capital of",
    "tallest mountain",
    "who won",
    "translate",
    "math homework",
)

_WORD = re.compile(r"[a-z0-9/]+(?:[-' ][a-z0-9/]+)?")


@dataclass(frozen=True)
class InputVerdict:
    """Result of the input guardrail. ``blocked`` true means short-circuit to a
    boundary; ``boundary_reason`` is one of "" | "injection_blocked" |
    "out_of_scope". ``pii_detected`` flags that the audit sink must redact."""

    blocked: bool
    boundary_reason: str
    pii_detected: bool
    flags: list[str] = field(default_factory=list)


def detect_injection(query: str) -> bool:
    """True if the USER query contains a prompt-injection / jailbreak attempt."""
    if not query:
        return False
    return any(pattern.search(query) for pattern in _INJECTION_PATTERNS)


def detect_pii(query: str, redactor: PIIRedactor | None = None) -> bool:
    """True if the query contains detectable PII (SSN, account, email, phone)."""
    if not query:
        return False
    redactor = redactor or make_redactor(profile="ci")
    return redactor.redact(query).count > 0


def is_in_scope(query: str) -> bool:
    """Conservative bank-knowledge scope check (G-16).

    In-scope when the query contains any bank term. Out-of-scope only when it
    contains a clearly non-bank term AND no bank term. An empty-but-nonblank query
    with no signal at all is treated as IN scope so it falls through to retrieval,
    which abstains on empty results (failing toward abstention, not refusal)."""
    lowered = query.lower()
    has_bank_term = any(term in lowered for term in _BANK_TERMS)
    if has_bank_term:
        return True
    has_out_term = any(term in lowered for term in _OUT_OF_SCOPE_TERMS)
    if has_out_term:
        return False
    # No signal either way: proceed (G-16 conservatism).
    return True


def check_input(query: str, *, redactor: PIIRedactor | None = None) -> InputVerdict:
    """Run injection -> scope checks and PII detection on the user query.

    Order matters: injection is checked first (it is the most hostile signal and
    must block even if the query also looks in-scope). PII is a non-blocking flag.
    """
    flags: list[str] = []
    pii_detected = detect_pii(query, redactor)
    if pii_detected:
        flags.append("query_pii_detected")

    if detect_injection(query):
        flags.append("injection_blocked")
        return InputVerdict(
            blocked=True,
            boundary_reason="injection_blocked",
            pii_detected=pii_detected,
            flags=flags,
        )

    if not is_in_scope(query):
        flags.append("out_of_scope")
        return InputVerdict(
            blocked=True,
            boundary_reason="out_of_scope",
            pii_detected=pii_detected,
            flags=flags,
        )

    return InputVerdict(
        blocked=False,
        boundary_reason="",
        pii_detected=pii_detected,
        flags=flags,
    )


__all__ = [
    "InputVerdict",
    "check_input",
    "detect_injection",
    "detect_pii",
    "is_in_scope",
]
