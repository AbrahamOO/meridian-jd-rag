"""The eight LangGraph query-graph nodes (contracts.md section 5).

Each node is a pure function ``(state, deps) -> partial_state``: it reads the
fields the contract assigns it, writes only its own outputs, and never reaches
into a sibling node's responsibility. Retrieval and generation logic is REUSED
from retrieval/ and generation/; nothing here reimplements scoring, ranking,
assembly, or generation. The node order is fixed:

    input_guardrail -> query_transform -> retrieve -> rerank -> assemble
    -> generate -> output_guardrail -> audit_sink

A node sets ``boundary_triggered``/``boundary_reason`` (and, on a terminal
condition, ``_short_circuit``) to route the executor straight to ``audit_sink``.
Every path reaches ``audit_sink`` exactly once (invariant 10.7).

Boundary reasons (contract QueryState):
    "" | unknown_role | no_access | empty_retrieval | out_of_scope
    | injection_blocked | insufficient_context
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, cast

from core.models import (
    ACCESS_BOUNDARY_STRING,
    AssembledContext,
    QueryState,
)
from generation.generator import generate_answer
from generation.guardrails_input import check_input
from generation.guardrails_output import check_output
from generation.prompts import build_user_message
from providers.base import EmbeddingProvider, Generator, Reranker
from retrieval.access import build_access_filter, resolve_access
from retrieval.assemble import assemble_context
from retrieval.citations import attach_access_metadata
from retrieval.hybrid import ChunkRepository, hybrid_retrieve
from retrieval.rerank import rerank_candidates
from retrieval.transform import TransformedQuery, expand_for_retrieval, transform_query

# Internal routing key (never serialized to the API response). When a node sets
# this True the executor jumps straight to audit_sink.
SHORT_CIRCUIT_KEY = "_short_circuit"


@dataclass
class GraphDeps:
    """Everything the nodes need that is not part of the request state.

    Built once per request (or reused across requests) by the API layer so the
    nodes stay pure functions of (state, deps). The providers come from the
    provider factory; the repository is the access-filtered chunk source.
    """

    embedder: EmbeddingProvider
    reranker: Reranker
    generator: Generator
    repository: ChunkRepository
    cfg: Mapping[str, Any]
    redactor: Any | None = None


def _retrieval_cfg(deps: GraphDeps) -> Mapping[str, Any]:
    return deps.cfg.get("retrieval", {})


def _chunking_cfg(deps: GraphDeps) -> Mapping[str, Any]:
    return deps.cfg.get("chunking", {})


def _active_strategy(state: QueryState, deps: GraphDeps) -> str:
    # options.chunk_strategy may override the configured default for the visualizer
    # (eval harness compares both); falls back to the config strategy.
    override = state.get("_chunk_strategy")
    if isinstance(override, str) and override in {"production", "naive"}:
        return override
    return _chunking_cfg(deps).get("strategy", "production")


# --- node 1: input_guardrail ------------------------------------------------


def input_guardrail(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Resolve access AND run injection / PII / scope checks (contract 5, G-07,
    G-16, G-17). Terminal short-circuits: unknown_role, injection_blocked,
    out_of_scope. A no-access decision for a known role is not possible here (a
    known role always clears at least PUBLIC/INTERNAL); access denial surfaces as
    empty retrieval downstream."""
    role = state.get("role", "")
    query = state.get("query", "")

    decision = resolve_access(role)
    flags: list[str] = []

    # Unknown role: match-none, boundary, but still audited (G-07).
    if not decision.allowed:
        return {
            "access": decision,
            "boundary_triggered": True,
            "boundary_reason": "unknown_role",
            "guardrail_flags": flags,
            "answer": ACCESS_BOUNDARY_STRING,
            "citations": [],
            SHORT_CIRCUIT_KEY: True,
        }

    verdict = check_input(query, redactor=deps.redactor)
    flags.extend(verdict.flags)
    if verdict.blocked:
        return {
            "access": decision,
            "boundary_triggered": True,
            "boundary_reason": verdict.boundary_reason,
            "guardrail_flags": flags,
            "answer": ACCESS_BOUNDARY_STRING,
            "citations": [],
            SHORT_CIRCUIT_KEY: True,
        }

    return {
        "access": decision,
        "boundary_triggered": False,
        "boundary_reason": "",
        "guardrail_flags": flags,
    }


# --- node 2: query_transform ------------------------------------------------


def query_transform(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Run configurable query transforms (contract 3.3). No short-circuit."""
    transform_cfg = _retrieval_cfg(deps).get("transform", {})
    transformed = transform_query(
        state.get("query", ""), state.get("history", []) or [], transform_cfg
    )
    return {"transformed": transformed}


# --- node 3: retrieve -------------------------------------------------------


def retrieve(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Embed + hybrid retrieve under the SINGLE shared access filter (contract
    3.2, G-14). Empty candidates set boundary empty_retrieval but continue (the
    generator abstains). Access is enforced in-query via the filter; this node
    never re-introduces filtered content."""
    decision = state["access"]
    transformed = cast(TransformedQuery, state["transformed"])
    rcfg = _retrieval_cfg(deps)
    active_strategy = _active_strategy(state, deps)

    access_filter = build_access_filter(decision, active_strategy=active_strategy)
    queries = expand_for_retrieval(transformed, rcfg.get("transform", {}))

    top_k_dense = rcfg.get("top_k_dense", 20)
    top_k_sparse = rcfg.get("top_k_sparse", 20)
    rrf_k = rcfg.get("rrf_k", 60)
    superseded_penalty = rcfg.get("superseded_penalty", 0.5)

    fused: dict[str, Any] = {}
    embed_tokens = 0
    for sub in queries:
        emb = deps.embedder.embed([sub], kind="query")
        embed_tokens += emb.tokens
        vector = emb.vectors[0]
        partial = hybrid_retrieve(
            sub,
            vector,
            access_filter,
            deps.repository,
            top_k_dense=top_k_dense,
            top_k_sparse=top_k_sparse,
            rrf_k=rrf_k,
            superseded_penalty=superseded_penalty,
        )
        for cand in partial:
            existing = fused.get(cand.chunk.chunk_id)
            if existing is None or cand.rrf_score > existing.rrf_score:
                fused[cand.chunk.chunk_id] = cand

    candidates = sorted(fused.values(), key=lambda c: (-c.rrf_score, c.chunk.chunk_id))

    tokens: dict[str, int] = dict(cast("Mapping[str, int]", state.get("tokens") or {}))
    tokens["embed"] = tokens.get("embed", 0) + embed_tokens

    out: dict[str, Any] = {"candidates": candidates, "tokens": tokens}
    if not candidates:
        out["boundary_triggered"] = True
        out["boundary_reason"] = "empty_retrieval"
    return out


# --- node 4: rerank ---------------------------------------------------------


def rerank(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Rerank access-filtered candidates (contract 3.4). No short-circuit. If the
    candidate set is empty the rerank is a no-op."""
    candidates = state.get("candidates", [])
    top_n = _retrieval_cfg(deps).get("rerank_top_n", 6)
    transformed = cast(TransformedQuery, state["transformed"])
    reranked = rerank_candidates(transformed.rewritten, candidates, deps.reranker, top_n=top_n)
    return {"reranked": reranked}


# --- node 5: assemble -------------------------------------------------------


def assemble(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Parent-document assembly + token budget (contract 3.5, G-05). Empty context
    sets boundary empty_retrieval (contract node table)."""
    reranked = state.get("reranked", [])
    rcfg = _retrieval_cfg(deps)
    token_budget = rcfg.get("context_token_budget", 3500)
    parent_max_tokens = _chunking_cfg(deps).get("parent_max_tokens", 1200)

    context = assemble_context(
        reranked, token_budget=token_budget, parent_max_tokens=parent_max_tokens
    )
    # Record access metadata for the citation re-validator (defense in depth).
    attach_access_metadata(context, reranked)

    out: dict[str, Any] = {"context": context}
    if not context.blocks:
        out["boundary_triggered"] = True
        # Keep empty_retrieval unless an earlier reason already set it.
        if not state.get("boundary_reason"):
            out["boundary_reason"] = "empty_retrieval"
    return out


# --- node 6: generate -------------------------------------------------------


def generate(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Grounded generation over the assembled context (contract 1.2, 9). On an
    empty context the generator abstains with the insufficient-context boundary
    string; we keep the upstream boundary_reason (empty_retrieval) when set,
    otherwise mark insufficient_context.

    This node only PRODUCES the candidate answer + raw citations + token counts;
    citation re-validation and groundedness are the output_guardrail's job."""
    context: AssembledContext = state.get(
        "context", AssembledContext(blocks=[], total_tokens=0, dropped_for_budget=[])
    )
    gcfg = deps.cfg.get("generation", {})
    temperature = gcfg.get("temperature", 0.0)
    max_tokens = gcfg.get("max_tokens", 1024)

    generated = generate_answer(
        state.get("query", ""),
        context,
        deps.generator,
        temperature=temperature,
        max_tokens=max_tokens,
        history=state.get("history", []) or [],
    )

    tokens: dict[str, int] = dict(cast("Mapping[str, int]", state.get("tokens") or {}))
    tokens["prompt"] = tokens.get("prompt", 0) + generated.prompt_tokens
    tokens["completion"] = tokens.get("completion", 0) + generated.completion_tokens

    cost = float(state.get("cost_usd", 0.0)) + generated.cost_usd

    out: dict[str, Any] = {
        "answer": generated.text,
        "citations": generated.citations,
        "tokens": tokens,
        "cost_usd": round(cost, 6),
        # carry finish_reason through so the output guardrail can downgrade on
        # truncated answers (contract 1.2).
        "_finish_reason": generated.finish_reason,
    }
    if not context.blocks and not state.get("boundary_reason"):
        out["boundary_reason"] = "insufficient_context"
        out["boundary_triggered"] = True
    return out


# --- node 7: output_guardrail -----------------------------------------------


def output_guardrail(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Citation re-validation (G-04) + groundedness + PII + advice checks
    (contract 3.6, 5). Forces the insufficient-context boundary when stripping a
    citation leaves a claim uncited or groundedness fails. Defense in depth on top
    of the in-query access pre-filter."""
    context: AssembledContext = state.get(
        "context", AssembledContext(blocks=[], total_tokens=0, dropped_for_budget=[])
    )
    role = state.get("role", "")
    active_strategy = _active_strategy(state, deps)

    verdict = check_output(
        state.get("answer", ""),
        state.get("citations", []),
        role,
        context,
        active_strategy=active_strategy,
        redactor=deps.redactor,
    )

    flags = list(state.get("guardrail_flags", []))
    for flag in verdict.flags:
        if flag not in flags:
            flags.append(flag)
    # Truncated answer risk (contract 1.2): downgrade groundedness confidence.
    if state.get("_finish_reason") == "length" and "truncated_answer" not in flags:
        flags.append("truncated_answer")

    out: dict[str, Any] = {
        "answer": verdict.answer,
        "citations": verdict.citations,
        "guardrail_flags": flags,
    }
    if verdict.boundary_triggered:
        out["boundary_triggered"] = True
        # An upstream empty_retrieval reason is preserved; only set the guardrail's
        # reason when no earlier boundary reason was recorded.
        out["boundary_reason"] = state.get("boundary_reason") or verdict.boundary_reason
    elif state.get("boundary_reason"):
        out["boundary_triggered"] = True
        out["boundary_reason"] = state["boundary_reason"]
    return out


# --- node 8: audit_sink -----------------------------------------------------


def audit_sink(state: QueryState, deps: GraphDeps) -> dict[str, Any]:
    """Persist exactly one audit record (contract 6.1, invariant 10.7) for EVERY
    path including boundaries. Writing is delegated to the observability writer
    passed via deps.cfg['_audit_writer'] when present so this node stays a pure
    function over state (the API injects the writer). The redacted-query rule
    (G-03) is enforced inside the writer."""
    writer = deps.cfg.get("_audit_writer") if isinstance(deps.cfg, Mapping) else None
    if writer is not None:
        try:
            writer.write(state)
        except Exception as exc:  # noqa: BLE001 - audit must never crash a request
            return {"error": f"audit_write_failed: {type(exc).__name__}"}
    return {}


# Fixed node order (contract 5). The executor walks this list; a node that sets
# SHORT_CIRCUIT_KEY jumps directly to the final node (audit_sink).
NODE_SEQUENCE: list[tuple[str, Callable[[QueryState, GraphDeps], dict[str, Any]]]] = [
    ("input_guardrail", input_guardrail),
    ("query_transform", query_transform),
    ("retrieve", retrieve),
    ("rerank", rerank),
    ("assemble", assemble),
    ("generate", generate),
    ("output_guardrail", output_guardrail),
    ("audit_sink", audit_sink),
]

AUDIT_NODE = "audit_sink"

__all__ = [
    "GraphDeps",
    "NODE_SEQUENCE",
    "AUDIT_NODE",
    "SHORT_CIRCUIT_KEY",
    "input_guardrail",
    "query_transform",
    "retrieve",
    "rerank",
    "assemble",
    "generate",
    "output_guardrail",
    "audit_sink",
]

# build_user_message is imported for the explain payload assembled in builder.py;
# referenced here to keep the import meaningful to linters.
_ = build_user_message
