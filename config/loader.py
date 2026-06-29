"""Layered configuration loader for Meridian J.D. RAG.

Precedence, lowest to highest (contracts section 1.5):

    default.yaml < profile(MJD_PROFILE).yaml < config/local.yaml < env overrides

The loader is fail-closed: it RAISES if anything tries to set
``access.fail_closed`` to false. There is no production path that fails open.
The returned ``Config`` is fully typed via pydantic models.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, field_validator

CONFIG_DIR = Path(__file__).resolve().parent

# Environment variable prefix for flat overrides, e.g.
# MJD__RETRIEVAL__TOP_K_DENSE=30 overrides retrieval.top_k_dense.
ENV_PREFIX = "MJD__"
ENV_NESTED_SEP = "__"


class FailClosedError(ValueError):
    """Raised when configuration attempts to disable the fail-closed access posture."""


class _Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EmbeddingConfig(_Base):
    adapter: str
    model: str
    fallback: str = "local"


class GeneratorConfig(_Base):
    adapter: str
    model: str


class RerankerConfig(_Base):
    adapter: str
    model: str


class ProvidersConfig(_Base):
    embedding: EmbeddingConfig
    generator: GeneratorConfig
    reranker: RerankerConfig


class ChunkingConfig(_Base):
    strategy: str = "production"
    child_target_tokens: int = 320
    child_overlap_pct: float = 0.12
    parent_max_tokens: int = 1200


class RetrievalConfig(_Base):
    top_k_dense: int = 20
    top_k_sparse: int = 20
    rrf_k: int = 60
    rerank_top_n: int = 6
    context_token_budget: int = 3500
    superseded_penalty: float = 0.5


class AccessConfig(_Base):
    fail_closed: bool = True

    @field_validator("fail_closed")
    @classmethod
    def _must_be_true(cls, value: bool) -> bool:
        if value is not True:
            raise FailClosedError(
                "access.fail_closed must be true; the loader refuses to run a "
                "fail-open access posture."
            )
        return value


class GenerationConfig(_Base):
    temperature: float = 0.0
    max_tokens: int = 1024


class Config(_Base):
    profile: str
    providers: ProvidersConfig
    chunking: ChunkingConfig = ChunkingConfig()
    retrieval: RetrievalConfig = RetrievalConfig()
    access: AccessConfig = AccessConfig()
    generation: GenerationConfig = GenerationConfig()


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file {path} must contain a YAML mapping at the top level.")
    return data


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge ``overlay`` onto ``base`` without mutating either."""
    merged = dict(base)
    for key, value in overlay.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _coerce_scalar(raw: str) -> Any:
    """Coerce an env string into bool/int/float/str using YAML scalar rules."""
    return yaml.safe_load(raw)


def _env_overrides(prefix: str = ENV_PREFIX) -> dict[str, Any]:
    """Build a nested override dict from MJD__ environment variables."""
    overrides: dict[str, Any] = {}
    for name, value in os.environ.items():
        if not name.startswith(prefix):
            continue
        path = name[len(prefix) :].lower().split(ENV_NESTED_SEP)
        cursor = overrides
        for part in path[:-1]:
            cursor = cursor.setdefault(part, {})
            if not isinstance(cursor, dict):
                raise ValueError(f"Conflicting env override structure at {name}.")
        cursor[path[-1]] = _coerce_scalar(value)
    return overrides


def load_config(config_dir: Path | None = None) -> Config:
    """Load the layered, typed configuration.

    Layers (lowest to highest precedence):
      1. default.yaml
      2. <profile>.yaml where profile = MJD_PROFILE (default "default")
      3. config/local.yaml (optional, gitignored)
      4. MJD__* environment variable overrides

    Raises FailClosedError (a ValueError) if access.fail_closed resolves false.
    """
    base_dir = config_dir or CONFIG_DIR
    profile = os.environ.get("MJD_PROFILE", "default").strip() or "default"

    merged = _read_yaml(base_dir / "default.yaml")
    if profile != "default":
        profile_data = _read_yaml(base_dir / f"{profile}.yaml")
        merged = _deep_merge(merged, profile_data)
    merged = _deep_merge(merged, _read_yaml(base_dir / "local.yaml"))
    merged = _deep_merge(merged, _env_overrides())

    # Pin the resolved profile name so it reflects the selection, not the file.
    merged["profile"] = merged.get("profile", profile)

    # Fail-closed pre-check: raise the typed FailClosedError directly rather than
    # letting pydantic wrap it in a generic ValidationError.
    access = merged.get("access")
    if isinstance(access, dict) and access.get("fail_closed", True) is not True:
        raise FailClosedError(
            "access.fail_closed must be true; the loader refuses to run a "
            "fail-open access posture."
        )

    return Config.model_validate(merged)
