"""Append-only audit log + reader (contracts.md section 6.1; gap-register G-03).

Two distinct sinks (G-03):

1. AUDIT LOG: durable, append-only JSONL, broadly readable by the audit-viewer UI
   and any examiner. The ``query`` field is PII-REDACTED before persistence. It
   carries NO document content, only doc_ids that survived the access filter.
2. DEBUG TRACE: short-lived, access-restricted, OFF by default. It may store the
   RAW query and retrieval internals for debugging behind an explicit
   ``observability.debug_trace=true`` flag. The raw value NEVER touches the audit
   log sink.

The PII redactor runs at the boundary BEFORE the audit write, so the raw query
never reaches the durable artifact. Writing is append-only: each record is one
JSON line; the writer never rewrites or truncates an existing line.
"""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from core.models import AccessDecision, QueryState
from ingestion.pii import PIIRedactor, make_redactor

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT_DIR = REPO_ROOT / "data" / "audit"
AUDIT_LOG_NAME = "audit.log.jsonl"
DEBUG_TRACE_NAME = "debug_trace.jsonl"


def _now_rfc3339() -> str:
    now = datetime.now(UTC)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def build_audit_record(state: QueryState, *, redactor: PIIRedactor) -> dict[str, Any]:
    """Build the contract 6.1 audit record from the final QueryState.

    The query is REDACTED here (G-03). ``retrieved_doc_ids`` lists only doc ids
    that survived the access filter (so the log cannot leak the existence of
    out-of-scope documents). No document content is ever included.
    """
    role = state.get("role", "")
    raw_query = state.get("query", "") or ""
    redacted_query = redactor.redact(raw_query).text

    citations = state.get("citations", []) or []
    retrieved = state.get("retrieved_doc_ids")
    if retrieved is None:
        # Derive from the final, access-validated citations and assembled context.
        ids: list[str] = []
        for c in citations:
            doc_id = c.get("doc_id") if isinstance(c, Mapping) else None
            if doc_id and doc_id not in ids:
                ids.append(doc_id)
        ctx = state.get("context")
        if ctx is not None:
            for block in getattr(ctx, "blocks", []):
                if block.doc_id not in ids:
                    ids.append(block.doc_id)
        retrieved = ids

    tokens = state.get("tokens", {}) or {}
    return {
        "trace_id": state.get("trace_id", ""),
        "role": role,
        "query": redacted_query,
        "retrieved_doc_ids": list(retrieved) if isinstance(retrieved, (list, tuple)) else [],
        "boundary_triggered": bool(state.get("boundary_triggered", False)),
        "boundary_reason": state.get("boundary_reason", ""),
        "guardrail_flags": list(state.get("guardrail_flags", []) or []),
        "latency_ms": float(state.get("latency_ms", 0.0)),
        "cost_usd": round(float(state.get("cost_usd", 0.0)), 6),
        "tokens": {
            "prompt": int(tokens.get("prompt", 0)),
            "completion": int(tokens.get("completion", 0)),
            "embed": int(tokens.get("embed", 0)),
        },
        "timestamp": _now_rfc3339(),
    }


def _debug_trace_record(state: QueryState) -> dict[str, Any]:
    """Raw debug trace (access-restricted, off by default). Carries the RAW query
    and minimal retrieval internals. Never written to the durable audit log."""
    tokens = state.get("tokens", {}) or {}
    return {
        "trace_id": state.get("trace_id", ""),
        "role": state.get("role", ""),
        "raw_query": state.get("query", ""),
        "boundary_reason": state.get("boundary_reason", ""),
        "guardrail_flags": list(state.get("guardrail_flags", []) or []),
        "tokens": dict(tokens),
        "timestamp": _now_rfc3339(),
    }


@dataclass
class AuditWriter:
    """Append-only writer for the durable audit log and the optional debug trace.

    ``debug_trace`` is OFF unless explicitly enabled. The PII redactor runs before
    the audit write so the raw query never lands in the durable log (G-03).
    """

    audit_dir: Path = DEFAULT_AUDIT_DIR
    debug_trace: bool = False
    redactor: PIIRedactor | None = None
    _lock: threading.Lock = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.audit_dir = Path(self.audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        if self.redactor is None:
            self.redactor = make_redactor(profile=os.environ.get("MJD_PROFILE"))
        self._lock = threading.Lock()

    @property
    def audit_path(self) -> Path:
        return self.audit_dir / AUDIT_LOG_NAME

    @property
    def debug_path(self) -> Path:
        return self.audit_dir / DEBUG_TRACE_NAME

    def write(self, state: QueryState) -> dict[str, Any]:
        """Append one redacted audit record (and, if enabled, one raw debug trace).

        Returns the redacted record written. Append-only: each call adds exactly
        one line to the audit log.
        """
        assert self.redactor is not None
        record = build_audit_record(state, redactor=self.redactor)
        line = json.dumps(record, ensure_ascii=False) + "\n"
        with self._lock:
            with self.audit_path.open("a", encoding="utf-8") as handle:
                handle.write(line)
            if self.debug_trace:
                with self.debug_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(_debug_trace_record(state), ensure_ascii=False) + "\n")
        return record


def default_writer(cfg: Mapping[str, Any] | None = None) -> AuditWriter:
    """Construct the AuditWriter from config / env.

    ``observability.debug_trace`` (config or MJD__OBSERVABILITY__DEBUG_TRACE) gates
    the raw debug trace; it defaults to False (fail-closed on PII exposure, G-03).
    """
    debug = False
    if cfg is not None:
        obs = cfg.get("observability", {}) if isinstance(cfg, Mapping) else {}
        debug = bool(obs.get("debug_trace", False))
    env = os.environ.get("MJD__OBSERVABILITY__DEBUG_TRACE", "").strip().lower()
    if env in {"1", "true", "yes"}:
        debug = True
    return AuditWriter(
        debug_trace=debug, redactor=make_redactor(profile=os.environ.get("MJD_PROFILE"))
    )


class AuditReader:
    """Read-only API over the append-only audit log for the UI audit viewer.

    Never mutates the log. ``read`` returns records newest-first. For a non-admin
    reader scoped to a role, records for OTHER roles are excluded, mirroring the
    contract's rule that the role-scoped viewer never sees out-of-scope ids; the
    admin scope sees all records (ids only, never content).
    """

    def __init__(self, audit_dir: Path = DEFAULT_AUDIT_DIR) -> None:
        self._path = Path(audit_dir) / AUDIT_LOG_NAME

    def read(
        self,
        *,
        limit: int = 100,
        role: str | None = None,
        admin: bool = False,
    ) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        records: list[dict[str, Any]] = []
        with self._path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not admin and role is not None and rec.get("role") != role:
                    continue
                records.append(rec)
        records.reverse()  # newest first
        return records[: max(0, limit)]

    def by_trace_id(self, trace_id: str) -> dict[str, Any] | None:
        for rec in self.read(limit=10_000, admin=True):
            if rec.get("trace_id") == trace_id:
                return rec
        return None


__all__ = [
    "AuditWriter",
    "AuditReader",
    "build_audit_record",
    "default_writer",
    "DEFAULT_AUDIT_DIR",
]

# AccessDecision is part of the contract surface the audit layer reasons about
# (role scoping); referenced for the type-aware reader without importing unused.
_ = AccessDecision
