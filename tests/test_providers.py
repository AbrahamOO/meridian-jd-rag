"""Foundation-layer tests: mock determinism, factory selection, fail-closed
config, and MissingSecretError on cloud-adapter construction without a key.

These run on the light CI path (MJD_PROFILE=ci). The mock adapters are pure
stdlib, so nothing here requires torch or any cloud SDK.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from config.loader import FailClosedError, load_config
from providers.base import (
    INSUFFICIENT_CONTEXT_STRING,
    MissingSecretError,
)
from providers.factory import get_embedding_provider, get_generator, get_reranker
from providers.mock import MockEmbeddingProvider, MockGenerator, MockReranker

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"


# --- Mock determinism -------------------------------------------------------


def test_mock_embedding_is_deterministic_across_instances() -> None:
    a = MockEmbeddingProvider()
    b = MockEmbeddingProvider()
    text = "Enhanced due diligence threshold for a new corporate account."
    ra = a.embed([text], kind="query")
    rb = b.embed([text], kind="query")
    assert ra.dim == 256
    assert len(ra.vectors[0]) == 256
    assert ra.vectors == rb.vectors  # byte-identical across two instances
    # L2-normalized: unit length within float tolerance.
    norm = sum(v * v for v in ra.vectors[0]) ** 0.5
    assert abs(norm - 1.0) < 1e-9


def test_mock_embedding_kind_changes_vector() -> None:
    provider = MockEmbeddingProvider()
    text = "Same text, different kind."
    as_doc = provider.embed([text], kind="document").vectors[0]
    as_query = provider.embed([text], kind="query").vectors[0]
    assert as_doc != as_query


def test_mock_embedding_empty_input() -> None:
    result = MockEmbeddingProvider().embed([])
    assert result.vectors == []
    assert result.tokens == 0
    assert result.cost_usd == 0.0
    assert result.dim == 256


def test_mock_generator_abstains_without_context() -> None:
    result = MockGenerator().generate(system="answer only from context", messages=[])
    assert result.text == INSUFFICIENT_CONTEXT_STRING
    assert result.cost_usd == 0.0
    assert result.completion_tokens == len(INSUFFICIENT_CONTEXT_STRING.split())


def test_mock_generator_extracts_first_sentence_and_cites() -> None:
    block = (
        '<<<CONTEXT_BLOCK id=MJD-OPS-0003 section="3 > 3.2">>>'
        "Enhanced due diligence is triggered above the threshold. "
        "Further detail follows here."
        "<<<END_CONTEXT_BLOCK>>>"
    )
    result = MockGenerator().generate(
        system="system", messages=[{"role": "user", "content": block}]
    )
    assert "Enhanced due diligence is triggered above the threshold." in result.text
    assert "[MJD-OPS-0003 3 > 3.2]" in result.text
    assert "Further detail follows here." not in result.text


def test_mock_reranker_jaccard_order_is_deterministic() -> None:
    reranker = MockReranker()
    query = "edd threshold corporate account"
    candidates = [
        "wire transfer operations runbook",
        "edd threshold for a corporate account",
        "edd threshold corporate",
    ]
    r1 = reranker.rerank(query, candidates, top_n=3)
    r2 = reranker.rerank(query, candidates, top_n=3)
    assert r1.order == r2.order
    assert r1.order[0] in (1, 2)  # the two relevant candidates outrank the runbook
    assert r1.order[-1] == 0
    assert reranker.rerank(query, [], top_n=3).order == []


# --- Factory selection from the ci profile ----------------------------------


def test_factory_selects_mock_under_ci_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MJD_PROFILE", "ci")
    cfg = load_config(CONFIG_DIR)
    assert cfg.profile == "ci"
    embedder = get_embedding_provider(cfg)
    generator = get_generator(cfg)
    reranker = get_reranker(cfg)
    assert embedder.name == "mock"
    assert generator.name == "mock"
    assert reranker.name == "mock"
    assert embedder.embed(["x"]).dim == 256


def test_default_profile_is_local(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MJD_PROFILE", raising=False)
    cfg = load_config(CONFIG_DIR)
    assert cfg.profile == "default"
    assert cfg.providers.embedding.adapter == "local"
    assert cfg.providers.generator.adapter == "local"
    assert cfg.providers.reranker.adapter == "local"


# --- MissingSecretError on cloud-adapter construction -----------------------


@pytest.mark.parametrize("env_var", ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"])
def test_cloud_adapter_raises_without_key(env_var: str, monkeypatch: pytest.MonkeyPatch) -> None:
    # Ensure no key is present from env or the secret file path.
    monkeypatch.delenv(env_var, raising=False)
    monkeypatch.setattr("providers.secrets.SECRETS_DIR", Path("/nonexistent-mjd-secrets"))

    if env_var == "ANTHROPIC_API_KEY":
        from providers.anthropic_adapter import AnthropicGenerator

        with pytest.raises(MissingSecretError):
            AnthropicGenerator()
    elif env_var == "OPENAI_API_KEY":
        from providers.openai_adapter import OpenAIEmbeddingProvider, OpenAIGenerator

        with pytest.raises(MissingSecretError):
            OpenAIEmbeddingProvider()
        with pytest.raises(MissingSecretError):
            OpenAIGenerator()
    else:
        from providers.gemini_adapter import GeminiEmbeddingProvider, GeminiGenerator

        with pytest.raises(MissingSecretError):
            GeminiEmbeddingProvider()
        with pytest.raises(MissingSecretError):
            GeminiGenerator()


# --- Config loader rejects fail_closed=false --------------------------------


def test_loader_rejects_fail_closed_false(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Build a throwaway config dir whose default.yaml sets fail_closed: false.
    (tmp_path / "default.yaml").write_text(
        "profile: default\n"
        "providers:\n"
        "  embedding: {adapter: mock, model: mock-embed-256}\n"
        "  generator: {adapter: mock, model: mock-gen}\n"
        "  reranker: {adapter: mock, model: mock-rerank}\n"
        "access:\n"
        "  fail_closed: false\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("MJD_PROFILE", raising=False)
    with pytest.raises(FailClosedError):
        load_config(tmp_path)


def test_loader_rejects_fail_closed_false_via_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MJD_PROFILE", "ci")
    monkeypatch.setenv("MJD__ACCESS__FAIL_CLOSED", "false")
    with pytest.raises(FailClosedError):
        load_config(CONFIG_DIR)


def test_env_override_applies(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MJD_PROFILE", "ci")
    monkeypatch.setenv("MJD__RETRIEVAL__TOP_K_DENSE", "30")
    cfg = load_config(CONFIG_DIR)
    assert cfg.retrieval.top_k_dense == 30
