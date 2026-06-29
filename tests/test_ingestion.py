"""Ingestion-layer tests against a small synthetic fixture (NOT the real corpus).

Proves the fail-closed and propagation guarantees the contracts demand:
metadata rejections (G-06/G-13/G-08), chunk metadata propagation, table-not-split
(G-10), the contextual-header format with section_path (4.2), watermark stripping,
both chunk strategies, the PII canary catch (G-03), the manifest write (6.2), and
an idempotent re-run. Everything runs on the light CI path (MJD_PROFILE=ci).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from config.loader import load_config
from ingestion.chunkers.base import build_chunks
from ingestion.loaders.base import load_path
from ingestion.metadata import compute_superseded_flags, validate_corpus
from ingestion.pii import make_redactor

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests" / "fixtures"
GOOD_DIR = FIXTURES / "good"


@pytest.fixture(autouse=True)
def _ci_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MJD_PROFILE", "ci")


def _parse(*paths: Path) -> list[tuple[str, dict]]:
    return [(str(p), load_path(p).header) for p in paths]


# --- Metadata fail-closed rejections (G-06, G-13, G-08) ---------------------


def test_reject_missing_classification() -> None:
    valid, rejections = validate_corpus(_parse(FIXTURES / "bad_missing_classification.md"))
    assert valid == {}
    assert any(r.reason == "missing_classification" for r in rejections)


def test_reject_unknown_role() -> None:
    valid, rejections = validate_corpus(_parse(FIXTURES / "bad_unknown_role.md"))
    assert valid == {}
    assert any(r.reason == "unknown_role" for r in rejections)


def test_reject_bad_doc_id() -> None:
    valid, rejections = validate_corpus(_parse(FIXTURES / "bad_doc_id.md"))
    assert valid == {}
    assert any(r.reason == "bad_doc_id" for r in rejections)


def test_reject_duplicate_doc_id_rejects_all_copies() -> None:
    dup = FIXTURES / "dup"
    valid, rejections = validate_corpus(
        _parse(dup / "MJD-OPS-9201-a.md", dup / "MJD-OPS-9201-b.md")
    )
    assert valid == {}
    dup_rejections = [r for r in rejections if r.reason == "duplicate_doc_id"]
    assert len(dup_rejections) == 2  # ALL copies rejected, not "keep the first"


def test_reject_dangling_supersedes() -> None:
    valid, rejections = validate_corpus(_parse(FIXTURES / "bad_dangling_supersedes.md"))
    assert valid == {}
    assert any(r.reason == "dangling_supersedes" for r in rejections)


def test_good_fixture_validates_and_computes_superseded() -> None:
    valid, rejections = validate_corpus(
        _parse(GOOD_DIR / "MJD-OPS-9001.md", GOOD_DIR / "MJD-OPS-9002.md")
    )
    assert rejections == []
    assert set(valid) == {"MJD-OPS-9001", "MJD-OPS-9002"}
    # 9002 supersedes 9001, so 9001 carries is_superseded.
    assert compute_superseded_flags(valid) == {"MJD-OPS-9001"}


# --- Chunk metadata propagation + chunker behavior --------------------------


def _chunk_good(strategy: str):
    cfg = load_config(REPO_ROOT / "config")
    valid, _ = validate_corpus(_parse(GOOD_DIR / "MJD-OPS-9001.md"))
    meta = valid["MJD-OPS-9001"]
    doc = load_path(GOOD_DIR / "MJD-OPS-9001.md")
    return build_chunks(
        meta,
        doc.body,
        content_hash="sha256:test",
        is_superseded=False,
        cfg=cfg.chunking,
        strategy=strategy,
    )


def test_every_chunk_propagates_access_metadata() -> None:
    for strategy in ("production", "naive"):
        result = _chunk_good(strategy)
        assert result.chunks, f"{strategy} produced no chunks"
        for chunk in result.chunks:
            assert chunk.allowed_roles == ["OPERATIONS_ANALYST", "BRANCH_STAFF"]
            assert chunk.classification == "INTERNAL"
            assert chunk.entity_status == "FICTIONAL"


def test_table_is_not_split() -> None:
    result = _chunk_good("production")
    table_chunks = [c for c in result.chunks if "| Step |" in c.text]
    assert len(table_chunks) == 1
    table_text = table_chunks[0].text
    # The whole table stays atomic: header row plus both data rows in one chunk.
    assert "Identity check" in table_text
    assert "Approval" in table_text


def test_contextual_header_includes_section_path() -> None:
    result = _chunk_good("production")
    purpose = next(c for c in result.chunks if "1.1" in c.section_path)
    title = "Synthetic Onboarding Procedure"
    expected_prefix = f"{title} > {purpose.section_path}\n\n"
    assert purpose.embed_text.startswith(expected_prefix)
    assert purpose.embed_text == f"{title} > {purpose.section_path}\n\n{purpose.text}"


def test_naive_has_no_contextual_header() -> None:
    result = _chunk_good("naive")
    for chunk in result.chunks:
        assert chunk.section_path == ""
        assert chunk.embed_text == chunk.text


def test_both_strategies_produced() -> None:
    prod = _chunk_good("production")
    naive = _chunk_good("naive")
    assert all(c.chunk_strategy == "production" for c in prod.chunks)
    assert all(c.chunk_strategy == "naive" for c in naive.chunks)
    assert prod.chunks and naive.chunks


# --- Watermark stripping (loader) -------------------------------------------


def test_watermark_stripped_from_body_and_chunks() -> None:
    for name in ("MJD-OPS-9001.md", "MJD-OPS-9002.md"):
        doc = load_path(GOOD_DIR / name)
        assert "FICTIONAL DOCUMENT" not in doc.body
    for strategy in ("production", "naive"):
        result = _chunk_good(strategy)
        for chunk in result.chunks:
            assert "FICTIONAL DOCUMENT" not in chunk.text
            assert "FICTIONAL DOCUMENT" not in chunk.embed_text


# --- PII canary (G-03) ------------------------------------------------------


def test_pii_canary_is_caught_and_redacted() -> None:
    redactor = make_redactor(profile="ci")
    doc = load_path(GOOD_DIR / "MJD-OPS-9001.md")
    result = redactor.redact(doc.body)
    assert result.count >= 1
    assert "123-45-6789" not in result.text
    assert "US_SSN" in result.entities


# --- /ingest CLI: manifest written + idempotent re-run ----------------------


@pytest.fixture()
def _isolated_dirs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect the file index and manifest writers at a tmp dir."""
    import ingestion.index as index_mod

    index_dir = tmp_path / "index"
    manifest_dir = tmp_path / "manifests"
    monkeypatch.setattr(index_mod, "DEFAULT_INDEX_DIR", index_dir)
    monkeypatch.setattr(index_mod, "DEFAULT_MANIFEST_DIR", manifest_dir)
    return tmp_path


def test_ingest_writes_manifest(_isolated_dirs: Path) -> None:
    from scripts.ingest import ingest

    response = ingest(
        mode="full",
        paths=[str(GOOD_DIR)],
        strategies=["production", "naive"],
        dry_run=False,
    )
    assert response["ingested"] == 2
    assert response["rejected"] == []
    assert response["chunks"]["production"] > 0
    assert response["chunks"]["naive"] > 0

    # The response manifest_path is repo-relative; the actual file lives under
    # the writer's redirected manifest dir.
    assert response["manifest_path"].endswith(".json")
    manifests = list((_isolated_dirs / "manifests").glob("idx-*.json"))
    assert len(manifests) == 1
    manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
    assert manifest["counts"]["documents"] == 2
    assert manifest["counts"]["chunks_production"] == response["chunks"]["production"]
    assert manifest["embedding"]["dim"] == 256  # mock embedder
    doc_ids = {d["doc_id"] for d in manifest["documents"]}
    assert doc_ids == {"MJD-OPS-9001", "MJD-OPS-9002"}
    superseded = {d["doc_id"] for d in manifest["documents"] if d["is_superseded"]}
    assert superseded == {"MJD-OPS-9001"}


def test_ingest_full_rejects_fail_closed(_isolated_dirs: Path) -> None:
    from scripts.ingest import ingest

    response = ingest(
        mode="full",
        paths=[str(FIXTURES / "bad_missing_classification.md")],
        strategies=["production"],
        dry_run=False,
    )
    assert response["ingested"] == 0
    assert response["error"]["code"] == "ingest_rejected"
    assert response["rejected"]
    # All-or-nothing: no manifest written on a rejected full ingest.
    assert not list((_isolated_dirs / "manifests").glob("idx-*.json"))


def test_ingest_is_idempotent(_isolated_dirs: Path) -> None:
    from scripts.ingest import ingest

    first = ingest(
        mode="full",
        paths=[str(GOOD_DIR)],
        strategies=["production", "naive"],
        dry_run=False,
    )
    second = ingest(
        mode="full",
        paths=[str(GOOD_DIR)],
        strategies=["production", "naive"],
        dry_run=False,
    )
    # Deterministic mock embedder + same corpus => identical chunk counts and
    # identical per-doc content hashes across runs.
    assert first["chunks"] == second["chunks"]
    manifests = sorted((_isolated_dirs / "manifests").glob("idx-*.json"))
    payloads = [json.loads(p.read_text(encoding="utf-8")) for p in manifests]
    hashes_first = {d["doc_id"]: d["content_hash"] for d in payloads[0]["documents"]}
    hashes_last = {d["doc_id"]: d["content_hash"] for d in payloads[-1]["documents"]}
    assert hashes_first == hashes_last
