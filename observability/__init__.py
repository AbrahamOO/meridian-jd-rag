"""Observability: append-only audit log, audit reader, optional tracing hooks.

- ``AuditWriter`` writes the contract 6.1 record to a durable, append-only log
  with the query PII-REDACTED (G-03). The raw query goes only to an
  access-restricted, TTL-bounded debug trace that is OFF by default.
- ``AuditReader`` is the read API the UI audit viewer uses; it never mutates the
  log and role-scopes the view so a reader never sees out-of-scope doc ids.
- ``tracing`` exposes OPTIONAL lazy OpenTelemetry/Phoenix hooks that are no-ops
  unless explicitly enabled and the libraries are installed.
"""

from __future__ import annotations

from observability.audit import (
    AuditReader,
    AuditWriter,
    build_audit_record,
    default_writer,
)
from observability.tracing import maybe_start_span, tracing_enabled

__all__ = [
    "AuditWriter",
    "AuditReader",
    "build_audit_record",
    "default_writer",
    "maybe_start_span",
    "tracing_enabled",
]
