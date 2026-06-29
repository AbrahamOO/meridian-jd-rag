# ADR-003: Provider Interface and Adapter Pattern

**Status:** Accepted
**Created: 2026-06-29**
**Last updated: 2026-06-29**

---

## Context

The system uses three different AI services: an embedding model, a generator, and a reranker. For each, there are multiple viable providers: local sentence-transformers, Anthropic, OpenAI, Gemini, and a deterministic mock for CI. Several requirements are in tension:

1. **Zero-key default:** The system must come up and serve with no API keys present. The default must use local models.
2. **CI determinism:** The CI eval gate must be reproducible with byte-identical results across runs. This requires fully deterministic providers with no network calls and no randomness.
3. **Cloud quality:** A portfolio reviewer should be able to swap to Anthropic/OpenAI/Gemini with a config change and get better answer quality. No code changes.
4. **Provider gaps:** Anthropic has no first-party embedding model. OpenAI has no first-party cross-encoder reranker. These gaps must be handled without surprising the caller.

The naive approach (hardcoding the provider choice in the embedding, retrieval, and generation code) makes it impossible to swap providers without code changes, and makes CI determinism impossible without mocking at a coarser level.

---

## Decision

Define three Protocol classes (`providers/base.py`): `EmbeddingProvider`, `Generator`, `Reranker`. Each has a minimal interface: `embed`, `generate`, or `rerank`, plus a `health` method. All return typed dataclasses (`EmbeddingResult`, `GenerationResult`, `RerankResult`).

Implement named adapters for each: `local`, `mock`, `anthropic`, `openai`, `gemini`. Each adapter is a class that implements the relevant protocol(s). Adapters are constructed only in `providers/factory.py` by the three factory functions: `get_embedding_provider(cfg)`, `get_generator(cfg)`, `get_reranker(cfg)`.

**Provider gap resolution:** When a provider lacks a capability (e.g., `anthropic` has no embedding), the factory resolves to the configured `embedding.fallback` adapter (default `local`) and records the substitution in the manifest under `embedding.resolved_from`. This keeps the config coherent ("I want anthropic as my primary") while being honest about what actually ran.

**Secret resolution:** `providers/secrets.py:resolve_secret(name)` resolves keys in order: env var, `/run/secrets/<name>`, None. Adapters that require a key call this in `__init__` and raise `MissingSecretError` if the key is None. Keys never appear in code, config files, logs, or prompts.

**Mock adapter determinism (G-12):** The mock adapters are fully specified in `docs/contracts.md` section 1.7. The mock embedder uses sha256-seeded stdlib RNG (no network, no randomness beyond the fixed seed). The mock generator extracts the first sentence of each context block (no model call). The mock reranker uses Jaccard token overlap (no model call). All costs are 0.0.

Configuration selects the adapter: `MJD_PROFILE=ci` forces all three to `mock`. `MJD_PROFILE=default` uses all `local`. A `config/local.yaml` override selects cloud adapters. No adapter name appears in code outside `providers/factory.py`.

---

## Consequences

**Enables:**
- Zero-key default and CI determinism coexist naturally: different adapters for different profiles.
- Cloud providers swappable with one config line change. No code changes anywhere else.
- The eval harness can swap adapters between runs (ci vs. full suite) by changing `MJD_PROFILE`.
- New adapters added by implementing the protocol and registering in the factory. No changes to retrieval, generation, or ingestion code.
- Provider health surfaces through `/health` uniformly, regardless of which adapter is active.

**Constrains:**
- The mock adapter's determinism guarantee is normative: any change to the mock embedder formula is a breaking change to CI eval reproducibility, because stored eval results would no longer be comparable.
- Provider gap resolution logs a substitution but does not error. A caller asking for `anthropic` embeddings silently gets `local` embeddings. This is the correct production behavior (the system stays up), but a developer must check the manifest's `embedding.resolved_from` to know what actually ran.
- Adding a provider that requires a multi-step auth flow (OAuth, not a static API key) requires extending `resolve_secret` beyond the current two-step (env, file) resolution.

---

## Change History

- 2026-06-29: Initial ADR accepted.
