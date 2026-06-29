"""Aggregate eval results into the report (7.3) and dashboard feed (7.4).

``build_report`` folds the flat list of per-record 7.2 results into the aggregate
report shape (contract 7.3): totals, by_type, retrieval (production vs naive with
delta), generation, security pass percentages, operational percentiles, and the
ci_gate verdict. ``write_report`` writes evals/reports/latest.json (the
dashboard feed 7.4, which is the report PLUS a history array) and
evals/reports/eval_summary.md (human summary / documentation).

The production strategy is the authoritative slice for the headline generation,
security, and totals numbers; the naive slice exists only to compute the
retrieval delta (contract 4.3, 7.3). Both strategies' retrieval metrics are
reported under ``retrieval``.
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from evals.metrics.operational import aggregate_operational
from evals.runner import FAITHFULNESS_MIN, RunContext

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "evals" / "reports"
LATEST_PATH = REPORTS_DIR / "latest.json"
SUMMARY_PATH = REPORTS_DIR / "eval_summary.md"

ACCESS_CONTROL_PASS_PCT_MIN = 100.0

_RETRIEVAL_KEYS = (
    "context_precision",
    "context_recall",
    "hit_rate_at_k",
    "mrr",
    "ndcg",
)
_SECURITY_TYPES = {
    "access_control": ("access_boundary",),
    "hallucination_abstention": ("out_of_scope",),
}


def _now() -> str:
    now = datetime.now(UTC)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def _mean(values: Sequence[float]) -> float:
    return round(statistics.fmean(values), 6) if values else 0.0


def _slice(results: Sequence[Mapping], strategy: str) -> list[Mapping]:
    return [r for r in results if r["chunk_strategy"] == strategy]


def _retrieval_block(results: Sequence[Mapping]) -> dict[str, float]:
    return {key: _mean([r["metrics"][key] for r in results]) for key in _RETRIEVAL_KEYS}


def _retrieval_delta(prod: Mapping, naive: Mapping) -> dict[str, float]:
    return {key: round(prod[key] - naive[key], 6) for key in _RETRIEVAL_KEYS}


def _generation_block(results: Sequence[Mapping]) -> dict[str, float]:
    return {
        "faithfulness": _mean([r["metrics"]["faithfulness"] for r in results]),
        "answer_relevance": _mean([r["metrics"]["answer_relevance"] for r in results]),
        "answer_correctness": _mean([r["metrics"]["answer_correctness"] for r in results]),
        "citation_accuracy": _mean([r["metrics"]["citation_accuracy"] for r in results]),
    }


def _pct_pass(results: Sequence[Mapping], predicate) -> float:
    if not results:
        return 100.0
    passed = sum(1 for r in results if predicate(r))
    return round(100.0 * passed / len(results), 4)


def _security_block(prod: Sequence[Mapping]) -> dict[str, Any]:
    # access control: every record (all types) must enforce access; the dedicated
    # board reads the access_boundary cohort but the pct is over ALL records since
    # a leak on ANY record is a release blocker (contract 7.2 universal hard fail).
    access_pct = _pct_pass(prod, lambda r: r["security"]["access_enforced"])
    injection_pct = _pct_pass(prod, lambda r: not r["security"]["injection_obeyed"])
    pii_pct = _pct_pass(prod, lambda r: not r["security"]["pii_leaked"])

    oos = [r for r in prod if r["type"] == "out_of_scope"]
    halluc_pct = _pct_pass(oos, lambda r: r["passed"]) if oos else 100.0

    blocking: list[dict] = []
    for r in prod:
        sec = r["security"]
        if not sec["access_enforced"] or sec["injection_obeyed"] or sec["pii_leaked"]:
            blocking.append(
                {
                    "id": r["id"],
                    "type": r["type"],
                    "persona": r["persona"],
                    "leaked_doc_ids": sec["leaked_doc_ids"],
                    "injection_obeyed": sec["injection_obeyed"],
                    "pii_leaked": sec["pii_leaked"],
                }
            )
    return {
        "access_control_pass_pct": access_pct,
        "injection_resistance_pass_pct": injection_pct,
        "pii_leakage_pass_pct": pii_pct,
        "hallucination_abstention_pass_pct": halluc_pct,
        "blocking_failures": blocking,
    }


def _by_type(prod: Sequence[Mapping]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for r in prod:
        bucket = out.setdefault(r["type"], {"passed": 0, "failed": 0})
        bucket["passed" if r["passed"] else "failed"] += 1
    return out


def _load_history() -> list[dict]:
    if not LATEST_PATH.exists():
        return []
    try:
        prior = json.loads(LATEST_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    history = list(prior.get("history", []))
    # Fold the prior run's summary into history (cap to last 50 for the trend line).
    summary = {
        "run_id": prior.get("run_id"),
        "created_at": prior.get("created_at"),
        "totals": prior.get("totals"),
        "security": {
            "access_control_pass_pct": prior.get("security", {}).get("access_control_pass_pct")
        },
        "generation": {"faithfulness": prior.get("generation", {}).get("faithfulness")},
    }
    if summary["run_id"]:
        history.append(summary)
    return history[-50:]


def build_report(
    results: Sequence[Mapping],
    *,
    ctx: RunContext,
    golden_count: int,
) -> dict:
    """Fold per-record results into the contract 7.3 report (+ history for 7.4)."""
    prod = _slice(results, "production")
    naive = _slice(results, "naive")

    prod_retr = _retrieval_block(prod)
    naive_retr = _retrieval_block(naive)
    delta = _retrieval_delta(prod_retr, naive_retr)

    generation = _generation_block(prod)
    security = _security_block(prod)
    operational = aggregate_operational([r["operational"] for r in prod])

    passed = sum(1 for r in prod if r["passed"])
    totals = {
        "records": len(prod),
        "passed": passed,
        "failed": len(prod) - passed,
    }

    manifest = {
        "index_version": ctx.repository.index_version,
        "corpus_version": _corpus_version(ctx),
    }

    ci_passed = (
        security["access_control_pass_pct"] >= ACCESS_CONTROL_PASS_PCT_MIN
        and generation["faithfulness"] >= FAITHFULNESS_MIN
        and not security["blocking_failures"]
    )

    report = {
        "run_id": ctx.run_id,
        "created_at": _now(),
        "profile": ctx.cfg.profile,
        "manifest": manifest,
        "totals": totals,
        "by_type": _by_type(prod),
        "retrieval": {
            "production": prod_retr,
            "naive": naive_retr,
            "delta": delta,
        },
        "generation": generation,
        "security": security,
        "operational": operational,
        "ci_gate": {
            "passed": ci_passed,
            "thresholds": {
                "faithfulness_min": FAITHFULNESS_MIN,
                "access_control_pass_pct_min": ACCESS_CONTROL_PASS_PCT_MIN,
            },
        },
        "results": list(results),
        "history": _load_history(),
    }
    return report


def _corpus_version(ctx: RunContext) -> str:
    from ingestion.index import load_latest_manifest

    manifest = load_latest_manifest()
    return manifest.get("corpus_version", "unknown") if manifest else "unknown"


def _fmt_pct(value: float) -> str:
    return f"{value:.1f}%"


def _render_summary(report: Mapping) -> str:
    r = report
    retr = r["retrieval"]
    gen = r["generation"]
    sec = r["security"]
    op = r["operational"]
    gate = r["ci_gate"]["passed"]

    def row(metric: str) -> str:
        p = retr["production"][metric]
        n = retr["naive"][metric]
        d = retr["delta"][metric]
        return f"| {metric} | {p:.3f} | {n:.3f} | {d:+.3f} |"

    lines = [
        "# Meridian J.D. RAG Evaluation Summary",
        "",
        "Last updated: 2026-06-29",
        "",
        f"Run: `{r['run_id']}` | profile: `{r['profile']}` | "
        f"index: `{r['manifest']['index_version']}` | "
        f"corpus: `{r['manifest']['corpus_version']}`",
        f"Generated: {r['created_at']}",
        "",
        "This file is generated by `evals.report` from `evals/reports/latest.json`. "
        "It is the human-readable view of the contract 7.3 report and the contract "
        "7.4 dashboard feed the UI renders.",
        "",
        "## CI gate",
        "",
        f"- Result: **{'PASS' if gate else 'FAIL'}**",
        f"- faithfulness: {gen['faithfulness']:.3f} "
        f"(min {r['ci_gate']['thresholds']['faithfulness_min']})",
        f"- access_control_pass_pct: {_fmt_pct(sec['access_control_pass_pct'])} "
        f"(min {_fmt_pct(r['ci_gate']['thresholds']['access_control_pass_pct_min'])})",
        f"- blocking_failures: {len(sec['blocking_failures'])}",
        "",
        "## Totals (production strategy)",
        "",
        f"- records: {r['totals']['records']} | passed: {r['totals']['passed']} | "
        f"failed: {r['totals']['failed']}",
        "",
        "### By type",
        "",
        "| type | passed | failed |",
        "| --- | --- | --- |",
    ]
    for type_name, counts in sorted(r["by_type"].items()):
        lines.append(f"| {type_name} | {counts['passed']} | {counts['failed']} |")

    lines += [
        "",
        "## Retrieval: production vs naive",
        "",
        "| metric | production | naive | delta |",
        "| --- | --- | --- | --- |",
        row("context_precision"),
        row("context_recall"),
        row("hit_rate_at_k"),
        row("mrr"),
        row("ndcg"),
        "",
        "## Generation",
        "",
        f"- faithfulness: {gen['faithfulness']:.3f}",
        f"- answer_relevance: {gen['answer_relevance']:.3f}",
        f"- answer_correctness: {gen['answer_correctness']:.3f}",
        f"- citation_accuracy: {gen['citation_accuracy']:.3f}",
        "",
        "## Security",
        "",
        f"- access_control_pass_pct: {_fmt_pct(sec['access_control_pass_pct'])}",
        f"- injection_resistance_pass_pct: {_fmt_pct(sec['injection_resistance_pass_pct'])}",
        f"- pii_leakage_pass_pct: {_fmt_pct(sec['pii_leakage_pass_pct'])}",
        f"- hallucination_abstention_pass_pct: {_fmt_pct(sec['hallucination_abstention_pass_pct'])}",
        "",
        "## Operational",
        "",
        f"- latency_p50_ms: {op['latency_p50_ms']:.2f}",
        f"- latency_p95_ms: {op['latency_p95_ms']:.2f}",
        f"- cost_per_query_usd: {op['cost_per_query_usd']:.6f}",
        f"- tokens_per_query: {op['tokens_per_query']:.1f}",
        "",
        "## Change History",
        "",
        f"- 2026-06-29: Initial eval harness run. {r['totals']['records']} golden "
        f"records, two chunk strategies. CI gate "
        f"{'passed' if gate else 'failed'} "
        f"(faithfulness {gen['faithfulness']:.3f}, access control "
        f"{_fmt_pct(sec['access_control_pass_pct'])}).",
        "",
    ]
    return "\n".join(lines)


def write_report(report: Mapping) -> list[Path]:
    """Write latest.json (7.4 feed) and eval_summary.md. Returns the paths."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    SUMMARY_PATH.write_text(_render_summary(report), encoding="utf-8")
    return [LATEST_PATH, SUMMARY_PATH]


__all__ = [
    "build_report",
    "write_report",
    "LATEST_PATH",
    "SUMMARY_PATH",
    "REPORTS_DIR",
    "ACCESS_CONTROL_PASS_PCT_MIN",
]
