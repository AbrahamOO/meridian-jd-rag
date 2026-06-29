"""PII detection and redaction (gap-register G-03).

Runs over content BEFORE embedding and over queries BEFORE durable logging. Two
backends:

1. Presidio (lazy import) when the `pii` extra is installed, for production
   recall across many entity types.
2. A deterministic stdlib regex detector used in CI / when Presidio is absent.
   It MUST catch the planted synthetic canaries: US SSNs and account numbers.

Both return a `RedactionResult` carrying the redacted text and a count of
redactions, so ingestion can report `pii_redactions` (contract 8.2) and the
security eval can assert no canary string survives.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Deterministic fallback patterns. Order matters: more specific first.
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
# Account number canary: 8 to 17 contiguous digits (covers synthetic account and
# card-like numbers) not part of a longer token. Kept conservative to avoid
# nuking ordinary years/section numbers (which are <= 4 digits).
_ACCOUNT_RE = re.compile(r"\b\d{8,17}\b")
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")

_FALLBACK_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("US_SSN", _SSN_RE),
    ("PHONE_NUMBER", _PHONE_RE),
    ("EMAIL_ADDRESS", _EMAIL_RE),
    ("ACCOUNT_NUMBER", _ACCOUNT_RE),
]

_REDACTION_TOKEN = "[REDACTED:{label}]"


@dataclass(frozen=True)
class RedactionResult:
    text: str
    count: int
    entities: list[str]  # labels redacted, in order found


class PIIRedactor:
    """Redactor with a Presidio backend and a deterministic regex fallback.

    Selection is automatic: if `use_presidio` is True and the library imports,
    Presidio is used; otherwise the deterministic fallback runs. The fallback is
    the path used under MJD_PROFILE=ci so tests need no spaCy/torch.
    """

    def __init__(self, *, use_presidio: bool = True) -> None:
        self._analyzer = None
        self._anonymizer = None
        self._backend = "fallback"
        if use_presidio:
            self._try_presidio()

    def _try_presidio(self) -> None:
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine
        except ImportError:
            return
        try:
            self._analyzer = AnalyzerEngine()
            self._anonymizer = AnonymizerEngine()
            self._backend = "presidio"
        except Exception:  # noqa: BLE001 - any init failure falls back safely
            self._analyzer = None
            self._anonymizer = None
            self._backend = "fallback"

    @property
    def backend(self) -> str:
        return self._backend

    def redact(self, text: str) -> RedactionResult:
        if not text:
            return RedactionResult(text=text, count=0, entities=[])
        if self._backend == "presidio":
            return self._redact_presidio(text)
        return self._redact_fallback(text)

    def _redact_fallback(self, text: str) -> RedactionResult:
        entities: list[str] = []
        redacted = text
        for label, pattern in _FALLBACK_RULES:
            token = _REDACTION_TOKEN.format(label=label)

            def _sub(_match: re.Match[str], _label: str = label, _token: str = token) -> str:
                entities.append(_label)
                return _token

            redacted = pattern.sub(_sub, redacted)
        return RedactionResult(text=redacted, count=len(entities), entities=entities)

    def _redact_presidio(self, text: str) -> RedactionResult:
        assert self._analyzer is not None and self._anonymizer is not None
        results = self._analyzer.analyze(text=text, language="en")
        from presidio_anonymizer.entities import OperatorConfig

        operators = {"DEFAULT": OperatorConfig("replace", {"new_value": "[REDACTED:PII]"})}
        anonymized = self._anonymizer.anonymize(
            text=text, analyzer_results=results, operators=operators
        )
        entities = [r.entity_type for r in results]
        return RedactionResult(text=anonymized.text, count=len(results), entities=entities)


def make_redactor(*, profile: str | None = None) -> PIIRedactor:
    """Construct a redactor. Under the `ci` profile force the deterministic
    fallback so tests never import spaCy/torch."""
    use_presidio = profile != "ci"
    return PIIRedactor(use_presidio=use_presidio)
