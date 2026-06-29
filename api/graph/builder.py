"""Query-graph builder + executor (contracts.md section 5).

Two execution backends, identical node sequence and routing:

1. Real langgraph (``StateGraph``) when the ``graph`` extra is installed. Nodes
   are added in the fixed contract order; conditional edges route a node that
   short-circuits straight to ``audit_sink``.
2. A deterministic in-process fallback executor when langgraph is absent (the CI
   mock path). It walks ``NODE_SEQUENCE`` and honors the same short-circuit so the
   same eight nodes run in the same order with the same terminal behavior.

``run_query`` is the single entry point the API uses; it picks the backend,
measures latency, and returns the final ``QueryState``. ``USING_LANGGRAPH``
reports which backend was selected (for /health and the build summary).
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Mapping
from typing import Any, cast

from api.graph.nodes import (
    AUDIT_NODE,
    NODE_SEQUENCE,
    SHORT_CIRCUIT_KEY,
    GraphDeps,
)
from core.models import QueryState

try:  # real langgraph when the `graph` extra is installed
    from langgraph.graph import END, START, StateGraph  # type: ignore

    USING_LANGGRAPH = True
except Exception:  # noqa: BLE001 - any import failure falls back deterministically
    StateGraph = None  # type: ignore
    START = END = None  # type: ignore
    USING_LANGGRAPH = False


def _merge(state: QueryState, partial: Mapping[str, Any]) -> QueryState:
    """Apply a node's partial output onto the running state (in place + return)."""
    for key, value in partial.items():
        state[key] = value  # type: ignore[literal-required]
    return state


class _FallbackGraph:
    """Deterministic executor: same nodes, same order, same short-circuit.

    Used when langgraph is not installed. Running this is behaviorally identical to
    the langgraph backend for the contract's purposes: each node is invoked once in
    order; a node setting ``_short_circuit`` routes directly to ``audit_sink``.
    """

    def __init__(self, deps: GraphDeps) -> None:
        self._deps = deps

    def invoke(self, state: QueryState) -> QueryState:
        deps = self._deps
        audit = dict(NODE_SEQUENCE)[AUDIT_NODE]
        for name, node in NODE_SEQUENCE:
            if name == AUDIT_NODE:
                break
            partial = node(state, deps)
            _merge(state, partial)
            if cast("dict[str, Any]", state).pop(SHORT_CIRCUIT_KEY, False):
                _merge(state, audit(state, deps))
                return state
        # Normal path: run audit_sink last.
        _merge(state, audit(state, deps))
        return state


def _build_langgraph(deps: GraphDeps):
    """Compile the real langgraph StateGraph over the fixed node sequence."""
    graph = StateGraph(QueryState)  # type: ignore[misc]
    names = [name for name, _ in NODE_SEQUENCE]

    def _wrap(node):
        def _runner(state: QueryState) -> dict[str, Any]:
            return dict(node(state, deps))  # langgraph merges the returned partial

        return _runner

    for name, node in NODE_SEQUENCE:
        graph.add_node(name, _wrap(node))

    graph.add_edge(START, names[0])

    def _route(state: QueryState) -> str:
        # A short-circuited node jumps to audit_sink; otherwise continue linearly.
        if state.get(SHORT_CIRCUIT_KEY):
            return AUDIT_NODE
        return "_next"

    # Linear edges with a conditional shortcut to audit_sink from every pre-audit
    # node, so a boundary at any node still terminates through audit_sink once.
    for index, name in enumerate(names[:-1]):
        nxt = names[index + 1]
        if name == AUDIT_NODE:
            continue
        graph.add_conditional_edges(name, _route, {AUDIT_NODE: AUDIT_NODE, "_next": nxt})
    graph.add_edge(AUDIT_NODE, END)
    return graph.compile()


def build_graph(deps: GraphDeps):
    """Return a runnable graph object exposing ``.invoke(state) -> state``.

    Uses real langgraph when installed, else the deterministic fallback executor.
    Both honor the identical node order and terminal short-circuit to audit_sink.
    """
    if USING_LANGGRAPH:
        return _build_langgraph(deps)
    return _FallbackGraph(deps)


def initial_state(
    *,
    role: str,
    query: str,
    history: list[dict] | None = None,
    chunk_strategy: str | None = None,
    explain: bool = False,
    trace_id: str | None = None,
) -> QueryState:
    """Build the starting QueryState for one request (contract 5 fields)."""
    state: QueryState = {
        "trace_id": trace_id or str(uuid.uuid4()),
        "role": role,
        "query": query,
        "history": history or [],
        "boundary_triggered": False,
        "boundary_reason": "",
        "guardrail_flags": [],
        "citations": [],
        "answer": "",
        "cost_usd": 0.0,
        "tokens": {"prompt": 0, "completion": 0, "embed": 0},
        "error": "",
    }
    if chunk_strategy:
        state["_chunk_strategy"] = chunk_strategy  # type: ignore[typeddict-unknown-key]
    if explain:
        state["_explain"] = True  # type: ignore[typeddict-unknown-key]
    return state


def run_query(
    deps: GraphDeps,
    *,
    role: str,
    query: str,
    history: list[dict] | None = None,
    chunk_strategy: str | None = None,
    explain: bool = False,
    trace_id: str | None = None,
    graph: Any | None = None,
) -> QueryState:
    """Execute the full query graph for one request and return the final state.

    Measures wall-clock latency into ``latency_ms``. The graph object can be
    pre-built and passed in (the API builds it once per request after resolving
    providers); otherwise it is built here.
    """
    state = initial_state(
        role=role,
        query=query,
        history=history,
        chunk_strategy=chunk_strategy,
        explain=explain,
        trace_id=trace_id,
    )
    runnable = graph if graph is not None else build_graph(deps)

    started = time.perf_counter()
    final = runnable.invoke(state)
    final["latency_ms"] = round((time.perf_counter() - started) * 1000.0, 1)
    # langgraph returns its own dict; ensure it is a plain QueryState dict.
    return dict(final)  # type: ignore[return-value]


__all__ = [
    "GraphDeps",
    "USING_LANGGRAPH",
    "build_graph",
    "run_query",
    "initial_state",
]
