"""API tests (contracts.md section 8). FastAPI TestClient under MJD_PROFILE=ci.

Proves the contract endpoints:
- GET /health is 200 and reports providers + index,
- POST /query happy path returns answer + citations + trace_id,
- unknown role -> 200 boundary (never 4xx), reason unknown_role,
- malformed body (missing role/query, empty query) -> 422,
- a wrong-role /query returns zero out-of-scope citations,
- an audit record is written for a boundary query,
- the explain payload never carries out-of-scope content,
- /ingest dry_run validates, /evals reads latest.json shape.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("MJD_PROFILE", "ci")

from fastapi.testclient import TestClient  # noqa: E402

import api.app as appmod  # noqa: E402
from api.app import STATE, app  # noqa: E402
from api.graph.nodes import GraphDeps  # noqa: E402
from config.loader import load_config  # noqa: E402
from observability.audit import AuditReader, AuditWriter  # noqa: E402
from providers.factory import (  # noqa: E402
    get_embedding_provider,
    get_generator,
    get_reranker,
)
from tests.test_graph import _clean_chunk, _InMemoryRepo  # noqa: E402


@pytest.fixture(autouse=True)
def _ci_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MJD_PROFILE", "ci")


@pytest.fixture()
def client(tmp_path) -> TestClient:
    """A TestClient whose app deps are reset and whose audit writer points at a
    temp dir so the audit assertions are isolated."""
    STATE.reset()
    STATE.set_deps_override(None)
    yield TestClient(app)
    STATE.reset()
    STATE.set_deps_override(None)


def _override_with_clean_repo(tmp_path) -> AuditWriter:
    """Override the app deps with an in-memory clean-prose repo so the happy path
    returns a grounded answer through the real graph + API. Returns the writer."""
    cfg = load_config()
    writer = AuditWriter(audit_dir=tmp_path)
    cfg_map = cfg.model_dump()
    cfg_map["_audit_writer"] = writer
    deps = GraphDeps(
        embedder=get_embedding_provider(cfg),
        reranker=get_reranker(cfg),
        generator=get_generator(cfg),
        repository=_InMemoryRepo([_clean_chunk()]),
        cfg=cfg_map,
    )
    STATE.set_deps_override(deps)
    return writer


# --- /health ----------------------------------------------------------------


def test_health_ok(client) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert "ok" in body
    assert "providers" in body
    assert set(body["providers"]) == {"embedding", "generator", "reranker"}
    assert body["profile"] == "ci"
    assert body["graph_backend"] in {"langgraph", "fallback"}


# --- /query happy path ------------------------------------------------------


def test_query_happy_path_returns_answer_citations_trace(client, tmp_path) -> None:
    _override_with_clean_repo(tmp_path)
    resp = client.post(
        "/query",
        json={
            "role": "OPERATIONS_ANALYST",
            "query": "What is the enhanced due diligence requirement for corporate accounts?",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["trace_id"]
    assert body["boundary_triggered"] is False
    assert body["answer"]
    assert body["citations"]
    assert body["citations"][0]["doc_id"] == "MJD-OPS-0003"
    assert body["retrieved_doc_ids"] == ["MJD-OPS-0003"]
    assert set(body["tokens"]) == {"prompt", "completion", "embed"}


# --- unknown role -> 200 boundary, never 4xx --------------------------------


def test_unknown_role_is_200_boundary_not_4xx(client) -> None:
    resp = client.post(
        "/query", json={"role": "DBA_ROOT", "query": "what cipher suites are approved"}
    )
    assert resp.status_code == 200  # boundary IS the product behavior (G-07)
    body = resp.json()
    assert body["boundary_triggered"] is True
    assert body["boundary_reason"] == "unknown_role"
    assert body["citations"] == []
    assert body["retrieved_doc_ids"] == []


# --- malformed body -> 422 --------------------------------------------------


def test_missing_role_is_422(client) -> None:
    resp = client.post("/query", json={"query": "something"})
    assert resp.status_code == 422


def test_missing_query_is_422(client) -> None:
    resp = client.post("/query", json={"role": "OPERATIONS_ANALYST"})
    assert resp.status_code == 422


def test_empty_query_is_422(client) -> None:
    resp = client.post("/query", json={"role": "OPERATIONS_ANALYST", "query": "   "})
    assert resp.status_code == 422


def test_non_json_body_is_422(client) -> None:
    resp = client.post("/query", content="not json", headers={"content-type": "application/json"})
    assert resp.status_code == 422


# --- wrong-role query: zero out-of-scope citations --------------------------


def test_wrong_role_query_zero_out_of_scope_citations(client) -> None:
    # SOFTWARE_ENGINEER cannot see RESTRICTED SEC-0002 (cipher suites). Uses the
    # real file index built by scripts.ingest.
    resp = client.post(
        "/query",
        json={"role": "SOFTWARE_ENGINEER", "query": "what cipher suites are approved"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "MJD-SEC-0002" not in {c["doc_id"] for c in body["citations"]}
    assert "MJD-SEC-0002" not in body["retrieved_doc_ids"]


# --- audit record for a boundary query --------------------------------------


def test_audit_record_written_for_boundary_query(client, tmp_path) -> None:
    _override_with_clean_repo(tmp_path)
    client.post("/query", json={"role": "DBA_ROOT", "query": "what cipher suites are approved"})
    records = AuditReader(tmp_path).read(admin=True)
    assert len(records) == 1
    assert records[0]["boundary_triggered"] is True
    assert records[0]["boundary_reason"] == "unknown_role"


def test_audit_endpoint_returns_records(client, tmp_path) -> None:
    _override_with_clean_repo(tmp_path)
    client.post(
        "/query",
        json={"role": "OPERATIONS_ANALYST", "query": "enhanced due diligence corporate"},
    )
    resp = client.get("/audit", params={"admin": True})
    assert resp.status_code == 200
    assert resp.json()["count"] >= 1


# --- explain payload restriction --------------------------------------------


def test_explain_never_includes_out_of_scope_content(client) -> None:
    resp = client.post(
        "/query",
        json={
            "role": "SOFTWARE_ENGINEER",
            "query": "what cipher suites are approved",
            "options": {"explain": True},
        },
    )
    assert resp.status_code == 200
    explain = resp.json()["explain"]
    assert explain is not None
    cand_docs = {c["doc_id"] for c in explain["candidates"]}
    assert "MJD-SEC-0002" not in cand_docs  # RESTRICTED never in the explain set


def test_explain_absent_by_default(client) -> None:
    resp = client.post(
        "/query",
        json={"role": "OPERATIONS_ANALYST", "query": "customer identification program"},
    )
    assert resp.json()["explain"] is None


# --- /ingest ----------------------------------------------------------------


def test_ingest_dry_run_validates(client) -> None:
    resp = client.post("/ingest", json={"mode": "full", "dry_run": True})
    assert resp.status_code == 200
    body = resp.json()
    assert body["ingested"] == 51
    assert body["rejected"] == []
    assert body.get("dry_run") is True


# --- /evals -----------------------------------------------------------------


def test_evals_get_shape(client) -> None:
    resp = client.get("/evals")
    assert resp.status_code == 200
    body = resp.json()
    assert "latest" in body
    assert "runs" in body
    assert isinstance(body["runs"], list)


def test_evals_post_returns_run_id(client) -> None:
    resp = client.post("/evals", json={"suite": "ci"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["run_id"]
    assert body["status"] in {"started", "unavailable"}


def test_app_imports_cleanly() -> None:
    assert appmod.app is not None


def test_rate_limiter_trips_and_recovers(client, monkeypatch: pytest.MonkeyPatch) -> None:
    """DoS mitigation (threat model T-05): the sliding-window limiter throttles
    expensive POST endpoints past the configured per-window cap with HTTP 429."""
    from api.app import _RATE_BUCKETS

    monkeypatch.setenv("MJD_RATE_LIMIT_ENABLED", "1")
    monkeypatch.setenv("MJD_RATE_LIMIT_PER_MIN", "3")
    _RATE_BUCKETS.clear()
    try:
        codes = [client.post("/evals", json={"suite": "ci"}).status_code for _ in range(4)]
        assert codes[:3] == [200, 200, 200]
        assert codes[3] == 429
    finally:
        _RATE_BUCKETS.clear()
