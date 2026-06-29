"""FastAPI service for Meridian J.D. RAG (contracts.md section 8).

Endpoints, exactly per contract section 8:

- POST /query  : runs the query graph (api/graph). Unknown role -> 200 boundary
  (never 4xx); malformed body (missing role/query, empty query) -> 422; the
  options.explain payload is restricted to in-scope content only.
- POST /ingest : runs scripts.ingest logic; a rejected full ingest -> 422.
- GET  /evals  : reads evals/reports/latest.json + lists runs.
  POST /evals   : triggers a run (suite ci|full) and returns {run_id, status}.
- GET  /health : provider health + index load status (ok=false on any failure).
- GET  /audit  : audit-viewer read API (observability) for the UI.

Providers come from the config-driven factory; nothing here hardcodes a provider.
The service starts even when the index is missing or a provider is degraded (so
the UI can show a degraded banner); /query then returns a boundary error.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from api.graph.builder import USING_LANGGRAPH, build_graph, run_query  # noqa: E402
from api.graph.nodes import GraphDeps  # noqa: E402
from config.loader import load_config  # noqa: E402
from core.models import ACCESS_BOUNDARY_STRING  # noqa: E402
from ingestion.index import load_latest_manifest  # noqa: E402
from ingestion.pii import make_redactor  # noqa: E402
from observability.audit import AuditReader, default_writer  # noqa: E402
from providers.factory import (  # noqa: E402
    get_embedding_provider,
    get_generator,
    get_reranker,
)
from retrieval.repository import FileChunkRepository  # noqa: E402

EVALS_REPORTS_DIR = REPO_ROOT / "evals" / "reports"
LATEST_REPORT = EVALS_REPORTS_DIR / "latest.json"


# --- request models (validation -> 422 on malformed body) -------------------


class QueryOptions(BaseModel):
    chunk_strategy: str | None = None
    explain: bool = False


class QueryRequest(BaseModel):
    role: str = Field(..., min_length=1)
    query: str = Field(..., min_length=1)
    history: list[dict] = Field(default_factory=list)
    options: QueryOptions = Field(default_factory=QueryOptions)


class IngestRequest(BaseModel):
    mode: str = "full"
    paths: list[str] = Field(default_factory=lambda: ["corpus/"])
    strategies: list[str] = Field(default_factory=lambda: ["production", "naive"])
    dry_run: bool = False


class EvalRunRequest(BaseModel):
    suite: str = "ci"


# --- app state --------------------------------------------------------------


class _AppState:
    """Lazily-built, cached providers + repository + graph deps.

    Built on first use so importing the module (and `import api.app`) never
    requires an index or provider. Rebuilt if the profile env changes.
    """

    def __init__(self) -> None:
        self._cfg = None
        self._deps: GraphDeps | None = None
        self._graph: Any | None = None
        self._writer = None
        self._profile: str | None = None
        self._deps_override: GraphDeps | None = None

    def _profile_key(self) -> str:
        return os.environ.get("MJD_PROFILE", "default")

    def reset(self) -> None:
        self._cfg = self._deps = self._graph = self._writer = None
        self._profile = None

    def set_deps_override(self, deps: GraphDeps | None) -> None:
        """Inject a GraphDeps for tests (in-memory repository, etc.). Passing None
        clears the override and restores factory-built deps."""
        self._deps_override = deps
        self._graph = None

    def config(self):
        if self._cfg is None or self._profile != self._profile_key():
            self._cfg = load_config()
            self._profile = self._profile_key()
            self._deps = self._graph = self._writer = None
        return self._cfg

    def deps(self) -> GraphDeps:
        if self._deps_override is not None:
            if self._graph is None:
                self._graph = build_graph(self._deps_override)
            return self._deps_override
        if self._deps is None or self._profile != self._profile_key():
            cfg = self.config()
            cfg_map = cfg.model_dump()
            cfg_map["_audit_writer"] = self.writer()
            cfg_map["observability"] = cfg_map.get("observability", {})
            repository = FileChunkRepository()
            self._deps = GraphDeps(
                embedder=get_embedding_provider(cfg),
                reranker=get_reranker(cfg),
                generator=get_generator(cfg),
                repository=repository,
                cfg=cfg_map,
                redactor=make_redactor(profile=cfg.profile),
            )
            self._graph = build_graph(self._deps)
        return self._deps

    def graph(self) -> Any:
        self.deps()
        return self._graph

    def writer(self):
        if self._writer is None:
            cfg_map = self.config().model_dump()
            self._writer = default_writer(cfg_map)
        return self._writer


STATE = _AppState()

app = FastAPI(title="Meridian J.D. RAG API", version="1.0.0")


# --- rate limiting (DoS mitigation: threat model T-05, spec section 14) ------
# Dependency-free sliding-window limiter over the expensive write/compute
# endpoints. Config-driven via env so deployments tune it without code changes;
# disabled or generous by default so it never throttles the test suite. A real
# deployment would back this with Redis for multi-instance correctness.
_RATE_BUCKETS: dict[str, list[float]] = {}
_RATE_LIMITED_PATHS = ("/query", "/ingest", "/evals")


def _rate_limit_config() -> tuple[bool, int, float]:
    enabled = os.environ.get("MJD_RATE_LIMIT_ENABLED", "1") not in ("0", "false", "False")
    per_min = int(os.environ.get("MJD_RATE_LIMIT_PER_MIN", "1000"))
    return enabled, per_min, 60.0


@app.middleware("http")
async def _rate_limiter(request: Request, call_next: Any) -> Any:
    enabled, limit, window = _rate_limit_config()
    if enabled and request.method == "POST" and request.url.path in _RATE_LIMITED_PATHS:
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        cutoff = now - window
        bucket = _RATE_BUCKETS.setdefault(client, [])
        bucket[:] = [t for t in bucket if t > cutoff]
        if len(bucket) >= limit:
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "rate_limited",
                        "message": f"Rate limit exceeded: max {limit} requests per {int(window)}s.",
                        "trace_id": None,
                    }
                },
            )
        bucket.append(now)
    return await call_next(request)


# --- error envelope (contract section 8) ------------------------------------


def _error(code: str, message: str, status: int, trace_id: str | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"error": {"code": code, "message": message, "trace_id": trace_id}},
    )


# --- POST /query ------------------------------------------------------------


@app.post("/query")
async def query(request: Request) -> JSONResponse:
    """Run one access-controlled query through the graph.

    Malformed body (missing/empty role or query) -> 422. Unknown role -> 200 with
    a boundary (the boundary IS the product behavior, G-07). The explain payload
    is restricted to in-scope content only.
    """
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001 - non-JSON body is malformed -> 422
        return _error("malformed_body", "Request body must be valid JSON.", 422)

    try:
        req = QueryRequest.model_validate(body)
    except ValidationError as exc:
        return _error("malformed_body", exc.errors().__str__(), 422)

    # Empty / whitespace-only query is a client error, not product behavior (G-15).
    if not req.query.strip():
        return _error("empty_query", "Query must be non-empty.", 422)

    try:
        deps = STATE.deps()
        graph = STATE.graph()
    except FileNotFoundError:
        # Index not loaded: serve a boundary error (contract 8.4) not a crash.
        return JSONResponse(
            status_code=200,
            content={
                "trace_id": str(uuid.uuid4()),
                "answer": ACCESS_BOUNDARY_STRING,
                "citations": [],
                "boundary_triggered": True,
                "boundary_reason": "empty_retrieval",
                "abstained": True,
                "retrieved_doc_ids": [],
                "latency_ms": 0.0,
                "cost_usd": 0.0,
                "tokens": {"prompt": 0, "completion": 0, "embed": 0},
                "explain": None,
                "error": {"code": "index_not_loaded", "message": "No index is loaded."},
            },
        )

    final = run_query(
        deps,
        role=req.role,
        query=req.query,
        history=req.history,
        chunk_strategy=req.options.chunk_strategy,
        explain=req.options.explain,
        graph=graph,
    )

    response = _serialize_query(dict(final), explain=req.options.explain)
    return JSONResponse(status_code=200, content=response)


def _serialize_query(state: dict, *, explain: bool) -> dict:
    """Map the final QueryState to the contract 8.1 response shape."""
    citations = state.get("citations", []) or []
    retrieved = []
    for c in citations:
        if c.get("doc_id") and c["doc_id"] not in retrieved:
            retrieved.append(c["doc_id"])
    ctx = state.get("context")
    if ctx is not None:
        for block in getattr(ctx, "blocks", []):
            if block.doc_id not in retrieved:
                retrieved.append(block.doc_id)

    boundary = bool(state.get("boundary_triggered", False))
    abstained = boundary or not state.get("answer")

    tokens = state.get("tokens", {}) or {}
    response = {
        "trace_id": state.get("trace_id", ""),
        "answer": state.get("answer", ""),
        "citations": citations,
        "boundary_triggered": boundary,
        "boundary_reason": state.get("boundary_reason", ""),
        "abstained": bool(abstained),
        "retrieved_doc_ids": retrieved,
        "latency_ms": float(state.get("latency_ms", 0.0)),
        "cost_usd": round(float(state.get("cost_usd", 0.0)), 6),
        "tokens": {
            "prompt": int(tokens.get("prompt", 0)),
            "completion": int(tokens.get("completion", 0)),
            "embed": int(tokens.get("embed", 0)),
        },
        "explain": _build_explain(state) if explain else None,
    }
    if state.get("error"):
        response["error"] = {"code": "graph_error", "message": state["error"]}
    return response


def _build_explain(state: dict) -> dict:
    """Build the explain payload (contract 8.1). RESTRICTED to in-scope content:
    it reports candidate scores, rerank order, and dropped-for-budget parent ids
    drawn ONLY from the access-filtered candidates/context the role could
    retrieve. It never includes content or ids the role could not see."""
    candidates = state.get("candidates", []) or []
    reranked = state.get("reranked", []) or []
    ctx = state.get("context")

    cand_view = [
        {
            "chunk_id": c.chunk.chunk_id,
            "doc_id": c.chunk.doc_id,
            "section_path": c.chunk.section_path,
            "rrf_score": round(c.rrf_score, 6),
            "dense_rank": c.dense_rank,
            "sparse_rank": c.sparse_rank,
            "is_superseded": c.chunk.is_superseded,
        }
        for c in candidates
    ]
    rerank_order = [c.chunk.chunk_id for c in reranked]
    dropped = list(getattr(ctx, "dropped_for_budget", []) or []) if ctx else []
    transformed = state.get("transformed")
    return {
        "transformed": (
            {
                "rewritten": getattr(transformed, "rewritten", ""),
                "subqueries": list(getattr(transformed, "subqueries", []) or []),
                "used": list(getattr(transformed, "used", []) or []),
            }
            if transformed is not None
            else None
        ),
        "candidates": cand_view,
        "rerank_order": rerank_order,
        "dropped_for_budget": dropped,
    }


# --- POST /ingest -----------------------------------------------------------


@app.post("/ingest")
async def ingest(request: Request) -> JSONResponse:
    """Run ingestion (contract 8.2). A rejected full ingest -> 422 listing all
    rejections (fail-closed, G-06/G-11/G-13). dry_run validates without writing."""
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001
        return _error("malformed_body", "Request body must be valid JSON.", 422)

    try:
        req = IngestRequest.model_validate(body)
    except ValidationError as exc:
        return _error("malformed_body", exc.errors().__str__(), 422)

    from scripts.ingest import ingest as run_ingest

    result = run_ingest(
        mode=req.mode,
        paths=req.paths,
        strategies=req.strategies,
        dry_run=req.dry_run,
    )

    if result.get("error"):
        # Fail-closed: a rejected full ingest is 422 with the rejection list.
        return JSONResponse(status_code=422, content=result)

    # Refresh cached deps so a new index is picked up by /query and /health.
    STATE.reset()
    return JSONResponse(status_code=200, content=result)


# --- GET/POST /evals --------------------------------------------------------


@app.get("/evals")
async def get_evals(run_id: str | None = None) -> JSONResponse:
    """Read the latest eval report (contract 8.3) or a specific run.

    Reads evals/reports/latest.json. When a run_id is given, reads that run's
    report file. Degrades gracefully (200 with latest=null) when no report exists
    yet so the UI can render an empty dashboard before the first eval run."""
    runs = _list_runs()
    if run_id is not None:
        path = EVALS_REPORTS_DIR / f"{run_id}.json"
        if not path.exists():
            return _error("run_not_found", f"No eval report for run_id={run_id}.", 404)
        return JSONResponse(status_code=200, content=json.loads(path.read_text("utf-8")))

    latest = None
    if LATEST_REPORT.exists():
        latest = json.loads(LATEST_REPORT.read_text("utf-8"))
    return JSONResponse(status_code=200, content={"latest": latest, "runs": runs})


@app.post("/evals")
async def post_evals(request: Request) -> JSONResponse:
    """Trigger an eval run (contract 8.3): {suite: ci|full} -> {run_id, status}.

    Invokes the eval harness (scripts/run_evals.py or evals.run) when present. The
    harness is part of the eval suite; if it is absent this returns a clear
    'unavailable' status rather than failing, so the API contract holds even
    before the harness lands."""
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001
        body = {}
    try:
        req = EvalRunRequest.model_validate(body or {})
    except ValidationError as exc:
        return _error("malformed_body", exc.errors().__str__(), 422)

    runner = _find_eval_runner()
    run_id = "run-" + uuid.uuid4().hex[:12]
    if runner is None:
        return JSONResponse(
            status_code=200,
            content={
                "run_id": run_id,
                "status": "unavailable",
                "detail": "Eval harness not installed; run `make eval` once available.",
            },
        )
    # Fire-and-report: kick off the harness in a subprocess so the request returns
    # promptly with status=started (contract 8.3).
    env = dict(os.environ)
    env.setdefault("MJD_PROFILE", "ci")
    subprocess.Popen(  # noqa: S603 - controlled args, no shell
        [sys.executable, str(runner), "--suite", req.suite, "--run-id", run_id],
        cwd=str(REPO_ROOT),
        env=env,
    )
    return JSONResponse(status_code=200, content={"run_id": run_id, "status": "started"})


def _list_runs() -> list[str]:
    if not EVALS_REPORTS_DIR.exists():
        return []
    runs = sorted(
        (p.stem for p in EVALS_REPORTS_DIR.glob("run-*.json")),
        reverse=True,
    )
    return runs


def _find_eval_runner() -> Path | None:
    for candidate in (
        REPO_ROOT / "scripts" / "run_evals.py",
        REPO_ROOT / "evals" / "run.py",
        REPO_ROOT / "evals" / "harness.py",
    ):
        if candidate.exists():
            return candidate
    return None


# --- GET /health ------------------------------------------------------------


@app.get("/health")
async def health() -> JSONResponse:
    """Provider health + index load status (contract 8.4).

    ok=false (with per-component detail) when any provider health or the index
    load fails, or when the active embedding model mismatches the index (G-18).
    The service still answers /health so the UI can show a degraded banner."""
    try:
        cfg = STATE.config()
    except Exception as exc:  # noqa: BLE001 - config error is reported, not crashed
        return JSONResponse(
            status_code=200,
            content={"ok": False, "error": f"config_error: {type(exc).__name__}", "providers": {}},
        )

    providers: dict[str, Any] = {}
    overall = True
    try:
        emb = get_embedding_provider(cfg)
        eh = emb.health()
        providers["embedding"] = {
            "ok": bool(eh.get("ok")),
            "adapter": cfg.providers.embedding.adapter,
            "model": eh.get("model"),
            "dim": eh.get("dim"),
        }
        overall = overall and bool(eh.get("ok"))
    except Exception as exc:  # noqa: BLE001
        providers["embedding"] = {"ok": False, "detail": type(exc).__name__}
        overall = False

    try:
        gen = get_generator(cfg)
        gh = gen.health()
        providers["generator"] = {
            "ok": bool(gh.get("ok")),
            "adapter": cfg.providers.generator.adapter,
            "model": gh.get("model"),
        }
        overall = overall and bool(gh.get("ok"))
    except Exception as exc:  # noqa: BLE001
        providers["generator"] = {"ok": False, "detail": type(exc).__name__}
        overall = False

    try:
        rer = get_reranker(cfg)
        rh = rer.health()
        providers["reranker"] = {
            "ok": bool(rh.get("ok")),
            "adapter": cfg.providers.reranker.adapter,
            "model": rh.get("model"),
        }
        overall = overall and bool(rh.get("ok"))
    except Exception as exc:  # noqa: BLE001
        providers["reranker"] = {"ok": False, "detail": type(exc).__name__}
        overall = False

    manifest = load_latest_manifest()
    if manifest is None:
        index_status = {"loaded": False, "index_version": None, "documents": 0, "chunks": 0}
        overall = False
    else:
        counts = manifest.get("counts", {})
        index_status = {
            "loaded": True,
            "index_version": manifest.get("index_version"),
            "documents": counts.get("documents", 0),
            "chunks": counts.get("chunks_production", 0),
        }
        # G-18: active embedding model must match the index's embedding model.
        idx_model = manifest.get("embedding", {}).get("model")
        active_model = providers.get("embedding", {}).get("model")
        if idx_model and active_model and idx_model != active_model:
            index_status["embedding_model_mismatch"] = True
            overall = False

    return JSONResponse(
        status_code=200,
        content={
            "ok": overall,
            "providers": providers,
            "index": index_status,
            "profile": cfg.profile,
            "graph_backend": "langgraph" if USING_LANGGRAPH else "fallback",
        },
    )


# --- GET /audit (audit-viewer read API) -------------------------------------


@app.get("/audit")
async def audit(limit: int = 100, role: str | None = None, admin: bool = False) -> JSONResponse:
    """Read the append-only audit log (observability) for the UI audit viewer.

    Role-scoped by default: a non-admin reader only sees records for its own role,
    mirroring the contract rule that a role-scoped viewer never sees out-of-scope
    ids. Admin sees all records (ids only, never content). Read-only."""
    reader = AuditReader(STATE.writer().audit_dir)
    records = reader.read(limit=limit, role=role, admin=admin)
    return JSONResponse(status_code=200, content={"records": records, "count": len(records)})


__all__ = ["app"]
