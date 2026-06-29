"""Optional RAGAS / DeepEval backends (LAZY, never required).

The eval harness ships deterministic built-in metrics so CI on the mock path
needs no heavy dependencies. RAGAS and DeepEval add value on a REAL-model profile
(LLM-graded faithfulness, answer relevancy, context precision/recall). They are
imported lazily and only when explicitly requested via config or env, and their
absence is a clean no-op, never an error.

``available()`` reports which optional backends import. ``maybe_ragas_scores``
returns extra metric values when RAGAS is installed AND enabled, else ``{}``.
This keeps the contract numbers coming from the deterministic built-ins while
letting a richer run augment them.
"""

from __future__ import annotations

import os
from typing import Any


def _try_import(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:  # noqa: BLE001 - any import failure means "not available"
        return False


def available() -> dict[str, bool]:
    """Report which optional eval backends are importable in this environment."""
    return {
        "ragas": _try_import("ragas"),
        "deepeval": _try_import("deepeval"),
    }


def _enabled(flag_env: str) -> bool:
    return os.environ.get(flag_env, "").strip().lower() in {"1", "true", "yes", "on"}


def maybe_ragas_scores(
    *,
    question: str,
    answer: str,
    contexts: list[str],
    ground_truth: str,
) -> dict[str, float]:
    """Return RAGAS metric values if RAGAS is installed AND MJD_EVAL_RAGAS is set.

    Returns ``{}`` on the mock/CI path (RAGAS absent or disabled), so the
    deterministic built-ins remain the sole source of the contract numbers. This
    function never raises; any failure degrades to ``{}``.
    """
    if not _enabled("MJD_EVAL_RAGAS") or not _try_import("ragas"):
        return {}
    try:  # pragma: no cover - exercised only on a real-model profile
        from datasets import Dataset  # type: ignore
        from ragas import evaluate  # type: ignore
        from ragas.metrics import (  # type: ignore
            answer_relevancy,
            context_precision,
            context_recall,
            faithfulness,
        )

        ds = Dataset.from_dict(
            {
                "question": [question],
                "answer": [answer],
                "contexts": [contexts],
                "ground_truth": [ground_truth],
            }
        )
        result = evaluate(
            ds,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        )
        scores: dict[str, float] = {}
        for key, value in result.items():  # type: ignore[attr-defined]
            try:
                scores[f"ragas_{key}"] = float(value)
            except (TypeError, ValueError):
                continue
        return scores
    except Exception:  # noqa: BLE001 - lazy backend must never break a run
        return {}


def maybe_deepeval_scores(**_: Any) -> dict[str, float]:
    """DeepEval placeholder: enabled only when installed and MJD_EVAL_DEEPEVAL set.

    Kept as a stable extension point; returns ``{}`` on the mock/CI path so the
    deterministic built-ins remain authoritative. A real-model integration plugs
    DeepEval metrics here without changing any caller.
    """
    if not _enabled("MJD_EVAL_DEEPEVAL") or not _try_import("deepeval"):
        return {}
    return {}  # pragma: no cover


__all__ = [
    "available",
    "maybe_ragas_scores",
    "maybe_deepeval_scores",
]
