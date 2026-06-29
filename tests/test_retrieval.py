"""Retrieval-layer tests (contracts.md section 3; gap-register G-02, G-04, G-05,
G-07, G-14). All under MJD_PROFILE=ci against the deterministic mock providers
and the real file index built by scripts/ingest.py.

Proves:
- RRF math is exactly 1/(rrf_k+rank) summed across lists,
- superseded chunks are down-weighted below their live successor on a
  version-sensitive query,
- citation re-validation strips out-of-scope and not-in-context citations,
- assembly token budget reserves overhead, dedupes parents, and always keeps
  at least one block,
- end-to-end: unknown role retrieves nothing; RESTRICTED invisible to non-SA;
  positive controls (SA cipher suites -> SEC-0002; SE SR 11-7 -> RSK-0002).
"""

from __future__ import annotations

import pytest

from config.loader import load_config
from core.models import (
    AssembledContext,
    Candidate,
    Chunk,
    ContextBlock,
)
from providers.factory import get_embedding_provider, get_reranker
from retrieval.access import build_access_filter, resolve_access
from retrieval.assemble import OVERHEAD_TOKENS, assemble_context
from retrieval.citations import attach_access_metadata, validate_citations
from retrieval.hybrid import hybrid_retrieve, rrf_contribution
from retrieval.pipeline import retrieve
from retrieval.repository import FileChunkRepository
from retrieval.transform import expand_for_retrieval, transform_query


@pytest.fixture(autouse=True)
def _ci_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MJD_PROFILE", "ci")


@pytest.fixture(scope="module")
def cfg_map():
    import os

    os.environ["MJD_PROFILE"] = "ci"
    return load_config().model_dump()


@pytest.fixture(scope="module")
def repo():
    import os

    os.environ["MJD_PROFILE"] = "ci"
    return FileChunkRepository()


@pytest.fixture(scope="module")
def embedder():
    import os

    os.environ["MJD_PROFILE"] = "ci"
    return get_embedding_provider(load_config())


@pytest.fixture(scope="module")
def reranker():
    import os

    os.environ["MJD_PROFILE"] = "ci"
    return get_reranker(load_config())


# --- helpers ----------------------------------------------------------------


def _mk_chunk(
    chunk_id: str,
    *,
    parent_id=None,
    is_superseded=False,
    text="x",
    doc_id=None,
    classification="INTERNAL",
    allowed_roles=("SECURITY_ARCHITECT",),
) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        doc_id=doc_id or chunk_id.split("::")[0],
        parent_id=parent_id or (chunk_id.replace("::c", "::p")),
        title="T",
        department="SECURITY",
        doc_type="STANDARD",
        classification=classification,
        owner_role="CISO",
        allowed_roles=list(allowed_roles),
        effective_date="2026-01-01",
        version="1.0.0",
        supersedes=None,
        is_superseded=is_superseded,
        entity_status="FICTIONAL",
        section_path="1 > 1.1",
        text=text,
        embed_text=text,
        parent_text=text,
        char_start=0,
        char_end=len(text),
        token_count=len(text.split()),
        content_hash="sha256:x",
        chunk_strategy="production",
    )


class _StubRepo:
    def __init__(self, dense, sparse):
        self._dense = dense
        self._sparse = sparse

    def dense_candidates(self, query_vector, access_filter, *, top_k):
        return self._dense[:top_k]

    def sparse_candidates(self, query_text, access_filter, *, top_k):
        return self._sparse[:top_k]


# --- RRF math ---------------------------------------------------------------


def test_rrf_contribution_formula() -> None:
    assert rrf_contribution(60, 1) == pytest.approx(1.0 / 61)
    assert rrf_contribution(60, 2) == pytest.approx(1.0 / 62)


def test_rrf_fusion_sums_across_lists() -> None:
    a = _mk_chunk("MJD-SEC-0001::c0001")
    b = _mk_chunk("MJD-SEC-0001::c0002")
    # a is rank1 dense, rank2 sparse; b is rank2 dense, rank1 sparse.
    dense = [(a, 0.9), (b, 0.8)]
    sparse = [(b, 5.0), (a, 4.0)]
    repo = _StubRepo(dense, sparse)
    out = hybrid_retrieve(
        "q",
        [0.0],
        {
            "allowed_roles_contains": "SECURITY_ARCHITECT",
            "classification_in": ["INTERNAL"],
            "chunk_strategy": "production",
        },
        repo,
        top_k_dense=10,
        top_k_sparse=10,
        rrf_k=60,
        superseded_penalty=0.5,
    )
    scores = {c.chunk.chunk_id: c.rrf_score for c in out}
    expected_a = 1.0 / 61 + 1.0 / 62
    expected_b = 1.0 / 62 + 1.0 / 61
    assert scores["MJD-SEC-0001::c0001"] == pytest.approx(expected_a)
    assert scores["MJD-SEC-0001::c0002"] == pytest.approx(expected_b)
    # Tie on score -> chunk_id ascending.
    assert out[0].chunk.chunk_id == "MJD-SEC-0001::c0001"


def test_superseded_penalty_downweights_below_live() -> None:
    live = _mk_chunk("MJD-OPS-0007::c0001", is_superseded=False)
    old = _mk_chunk("MJD-OPS-0009::c0001", is_superseded=True)
    # Identical ranks in both lists -> equal raw RRF; penalty must flip the order.
    dense = [(live, 0.9), (old, 0.9)]
    sparse = [(live, 0.9), (old, 0.9)]
    repo = _StubRepo(dense, sparse)
    out = hybrid_retrieve(
        "transaction limits",
        [0.0],
        {
            "allowed_roles_contains": "OPERATIONS_ANALYST",
            "classification_in": ["INTERNAL"],
            "chunk_strategy": "production",
        },
        repo,
        top_k_dense=10,
        top_k_sparse=10,
        rrf_k=60,
        superseded_penalty=0.5,
    )
    by_id = {c.chunk.chunk_id: c for c in out}
    assert by_id["MJD-OPS-0009::c0001"].rrf_score < by_id["MJD-OPS-0007::c0001"].rrf_score
    assert out[0].chunk.chunk_id == "MJD-OPS-0007::c0001"


# --- assembly token budget --------------------------------------------------


def _cand(chunk: Chunk) -> Candidate:
    return Candidate(
        chunk=chunk, dense_rank=1, sparse_rank=1, rrf_score=1.0, dense_score=1.0, sparse_score=1.0
    )


def test_assembly_reserves_overhead_and_keeps_one_block() -> None:
    big = _mk_chunk("MJD-SEC-0001::c0001", text=" ".join(["w"] * 5000))
    # Even though the single parent exceeds budget, one block must survive (G-05).
    ctx = assemble_context([_cand(big)], token_budget=1000, parent_max_tokens=1200)
    assert len(ctx.blocks) == 1
    assert ctx.total_tokens <= 1000 - OVERHEAD_TOKENS


def test_assembly_dedupes_parents() -> None:
    c1 = _mk_chunk("MJD-SEC-0001::c0001", parent_id="MJD-SEC-0001::p0001", text="alpha beta")
    c2 = _mk_chunk("MJD-SEC-0001::c0002", parent_id="MJD-SEC-0001::p0001", text="alpha beta")
    ctx = assemble_context([_cand(c1), _cand(c2)], token_budget=3500, parent_max_tokens=1200)
    assert len(ctx.blocks) == 1


def test_assembly_skips_overflow_but_keeps_smaller() -> None:
    small1 = _mk_chunk("MJD-A-0001::c0001", parent_id="MJD-A-0001::p0001", text="a b c")
    huge = _mk_chunk(
        "MJD-B-0001::c0001", parent_id="MJD-B-0001::p0001", text=" ".join(["w"] * 4000)
    )
    small2 = _mk_chunk("MJD-C-0001::c0001", parent_id="MJD-C-0001::p0001", text="d e f")
    ctx = assemble_context(
        [_cand(small1), _cand(huge), _cand(small2)], token_budget=1000, parent_max_tokens=10
    )
    parent_ids = [b.parent_id for b in ctx.blocks]
    assert "MJD-A-0001::p0001" in parent_ids
    assert "MJD-C-0001::p0001" in parent_ids  # smaller one still fit after skip


# --- citation re-validation -------------------------------------------------


def test_citation_revalidation_strips_out_of_scope_and_not_in_context() -> None:
    block = ContextBlock(
        parent_id="MJD-OPS-0001::p0001",
        doc_id="MJD-OPS-0001",
        title="CIP",
        section_path="1",
        version="1.0.0",
        text="x",
        is_superseded=False,
    )
    ctx = AssembledContext(blocks=[block], total_tokens=1, dropped_for_budget=[])
    chunk = _mk_chunk(
        "MJD-OPS-0001::c0001", classification="INTERNAL", allowed_roles=("OPERATIONS_ANALYST",)
    )
    attach_access_metadata(ctx, [chunk])

    emitted = [
        {"doc_id": "MJD-OPS-0001", "title": "CIP", "section_path": "1", "version": "1.0.0"},
        {
            "doc_id": "MJD-SEC-0002",
            "title": "Crypto",
            "section_path": "4",
            "version": "3.1.0",
        },  # not in ctx
    ]
    out = validate_citations(emitted, "OPERATIONS_ANALYST", ctx)
    assert {c["doc_id"] for c in out.valid} == {"MJD-OPS-0001"}
    assert {c["doc_id"] for c in out.stripped} == {"MJD-SEC-0002"}


def test_citation_revalidation_strips_when_role_loses_access() -> None:
    # A context block for a CONFIDENTIAL AML doc; OPERATIONS_ANALYST may not cite it
    # even if the generator hallucinated it into the citation list.
    block = ContextBlock(
        parent_id="MJD-CMP-0001::p0001",
        doc_id="MJD-CMP-0001",
        title="AML",
        section_path="2",
        version="4.2.0",
        text="x",
        is_superseded=False,
    )
    ctx = AssembledContext(blocks=[block], total_tokens=1, dropped_for_budget=[])
    chunk = _mk_chunk(
        "MJD-CMP-0001::c0001",
        classification="CONFIDENTIAL",
        allowed_roles=("COMPLIANCE_OFFICER", "RISK_ANALYST"),
    )
    attach_access_metadata(ctx, [chunk])
    emitted = [{"doc_id": "MJD-CMP-0001", "title": "AML", "section_path": "2", "version": "4.2.0"}]
    out = validate_citations(emitted, "OPERATIONS_ANALYST", ctx)
    assert out.valid == []
    assert {c["doc_id"] for c in out.stripped} == {"MJD-CMP-0001"}


# --- transform / G-14 -------------------------------------------------------


def test_transform_decomposes_compound_question() -> None:
    t = transform_query(
        "what are our secrets rotation policy and our AML escalation procedure", [], {}
    )
    assert len(t.subqueries) >= 2
    assert "decompose" in t.used
    expanded = expand_for_retrieval(t, {})
    assert len(expanded) >= 2


# --- end-to-end against the real file index ---------------------------------


def test_unknown_role_retrieves_nothing(embedder, reranker, repo, cfg_map) -> None:
    res = retrieve(
        "ROOT",
        "what cipher suites are approved",
        embedder=embedder,
        reranker=reranker,
        repository=repo,
        cfg=cfg_map,
    )
    assert res.access.allowed is False
    assert res.candidates == []
    assert res.reranked == []
    assert res.context.blocks == []
    assert res.retrieved_doc_ids == []


def test_software_engineer_cannot_see_restricted_crypto(embedder, reranker, repo, cfg_map) -> None:
    res = retrieve(
        "SOFTWARE_ENGINEER",
        "what cipher suites are approved",
        embedder=embedder,
        reranker=reranker,
        repository=repo,
        cfg=cfg_map,
    )
    all_docs = {c.chunk.doc_id for c in res.candidates}
    assert "MJD-SEC-0002" not in all_docs
    assert "MJD-SEC-0002" not in res.retrieved_doc_ids


def test_software_engineer_cannot_see_aml_confidential(embedder, reranker, repo, cfg_map) -> None:
    res = retrieve(
        "SOFTWARE_ENGINEER",
        "what are our AML escalation procedures",
        embedder=embedder,
        reranker=reranker,
        repository=repo,
        cfg=cfg_map,
    )
    all_docs = {c.chunk.doc_id for c in res.candidates}
    assert all_docs.isdisjoint({"MJD-CMP-0001", "MJD-CMP-0002", "MJD-CMP-0004"})


def test_security_architect_sees_restricted_crypto(embedder, reranker, repo, cfg_map) -> None:
    res = retrieve(
        "SECURITY_ARCHITECT",
        "what cipher suites are approved",
        embedder=embedder,
        reranker=reranker,
        repository=repo,
        cfg=cfg_map,
    )
    all_docs = {c.chunk.doc_id for c in res.candidates}
    assert "MJD-SEC-0002" in all_docs


def test_software_engineer_can_read_sr_11_7(embedder, reranker, repo, cfg_map) -> None:
    res = retrieve(
        "SOFTWARE_ENGINEER",
        "SR 11-7 model risk validation cadence",
        embedder=embedder,
        reranker=reranker,
        repository=repo,
        cfg=cfg_map,
    )
    all_docs = {c.chunk.doc_id for c in res.candidates}
    assert "MJD-RSK-0002" in all_docs


def test_both_lists_carry_same_access_filter(embedder, reranker, repo, cfg_map) -> None:
    # The repository must never return a chunk the filter forbids on EITHER list.
    flt = build_access_filter(resolve_access("OPERATIONS_ANALYST"), active_strategy="production")
    vec = embedder.embed(["transaction monitoring rules"], kind="query").vectors[0]
    dense = repo.dense_candidates(vec, flt, top_k=50)
    sparse = repo.sparse_candidates("transaction monitoring rules", flt, top_k=50)
    for chunk, _ in dense + sparse:
        assert chunk.classification in {"PUBLIC", "INTERNAL"}
        assert "OPERATIONS_ANALYST" in chunk.allowed_roles
