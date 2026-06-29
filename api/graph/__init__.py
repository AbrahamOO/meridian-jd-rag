"""LangGraph query graph (contracts.md section 5).

The eight contract nodes over ``QueryState`` in fixed order, with terminal
short-circuits to ``audit_sink`` on a boundary or error. ``build_graph`` returns
a runnable that uses real langgraph when installed and a deterministic in-process
fallback executor (running the identical node sequence) when it is not, so the
CI mock path needs no langgraph dependency.
"""

from __future__ import annotations

from api.graph.builder import GraphDeps, build_graph, run_query
from api.graph.nodes import NODE_SEQUENCE

__all__ = ["GraphDeps", "build_graph", "run_query", "NODE_SEQUENCE"]
