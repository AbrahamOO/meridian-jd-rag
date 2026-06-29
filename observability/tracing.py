"""Optional tracing hooks (OpenTelemetry / Arize Phoenix), lazy and off by default.

The system MUST run with no tracing backend installed (the zero-key / CI path).
These hooks are no-ops unless tracing is explicitly enabled via
``observability.tracing=true`` (config) or ``MJD__OBSERVABILITY__TRACING=true``
AND the optional OpenTelemetry libraries import. ``maybe_start_span`` is a context
manager that yields a span when tracing is active and a harmless null span
otherwise, so call sites never branch on availability.

Tracing carries spans tagged with the requesting role (contract: every online
request emits one trace tagged with the role); it never carries PII or document
content. The durable audit log (observability/audit.py) is the source of truth
for compliance; tracing is an optional engineering aid only.
"""

from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any


def tracing_enabled(cfg: Mapping[str, Any] | None = None) -> bool:
    """True only when tracing is explicitly enabled in config or env."""
    enabled = False
    if cfg is not None and isinstance(cfg, Mapping):
        obs = cfg.get("observability", {})
        enabled = bool(obs.get("tracing", False))
    env = os.environ.get("MJD__OBSERVABILITY__TRACING", "").strip().lower()
    if env in {"1", "true", "yes"}:
        enabled = True
    return enabled


class _NullSpan:
    """A no-op span used when tracing is disabled or the backend is absent."""

    def set_attribute(self, *_args: Any, **_kwargs: Any) -> None:  # noqa: D401
        return None

    def record_exception(self, *_args: Any, **_kwargs: Any) -> None:
        return None


def _tracer() -> Any | None:
    """Lazily obtain an OpenTelemetry tracer if the library is installed."""
    try:
        from opentelemetry import trace  # type: ignore
    except Exception:  # noqa: BLE001 - backend absent: tracing degrades to no-op
        return None
    return trace.get_tracer("mjd.api")


@contextmanager
def maybe_start_span(
    name: str,
    *,
    role: str | None = None,
    cfg: Mapping[str, Any] | None = None,
    attributes: Mapping[str, Any] | None = None,
) -> Iterator[Any]:
    """Yield a tracing span when tracing is active, else a null span.

    The span is tagged with the requesting role (never PII or content). Safe to
    use unconditionally: when tracing is off or the backend is missing it yields a
    null span and does nothing.
    """
    if not tracing_enabled(cfg):
        yield _NullSpan()
        return
    tracer = _tracer()
    if tracer is None:
        yield _NullSpan()
        return
    with tracer.start_as_current_span(name) as span:
        if role is not None:
            span.set_attribute("mjd.role", role)
        for key, value in (attributes or {}).items():
            span.set_attribute(key, value)
        yield span


__all__ = ["tracing_enabled", "maybe_start_span"]
