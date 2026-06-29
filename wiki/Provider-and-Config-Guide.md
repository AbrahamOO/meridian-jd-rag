# Provider and Config Guide

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist.

---

Meridian J.D. RAG routes every embedding, generation, and reranking call through a single swappable adapter interface: selectable per config profile, runnable with zero API keys in the default local mode.

---

## Provider adapter architecture

All provider logic lives in `providers/`. Three provider types: embedding, generator, reranker: each expose a typed Protocol. Available adapters per type: `local`, `mock`, `anthropic`, `openai`, `gemini`. The active adapter is resolved by the factory from config; no adapter name is hardcoded outside [`providers/factory.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/providers/factory.py).

In practice this means switching from local BGE embeddings to OpenAI embeddings is one line in `config/local.yaml`. No code changes.

---

## Configuration precedence

```
config/default.yaml          (committed, zero-key, shippable)
  config/ci.yaml             (committed, all-mock, CI only)
  config/local.yaml          (gitignored, your overrides)
    environment variables    (highest, used by Docker)
```

`MJD_PROFILE` selects the profile YAML. Setting `MJD_PROFILE=ci` loads `config/ci.yaml` on top of `config/default.yaml`. Each layer overrides only the keys it defines; unmentioned keys fall through from the layer below.

---

## Profile reference

### default: zero-key local profile

```yaml
profile: default
providers:
  embedding:
    adapter: local
    model: bge-small-en-v1.5
    fallback: local
  generator:
    adapter: local
    model: local-instruct        # abstain-only stub if no local LLM present
  reranker:
    adapter: local
    model: bge-reranker-base
```

No API keys required. The system starts and serves with zero network calls. If no local LLM is present, the generator degrades to an abstain-only stub that returns the insufficient-context boundary string. It never crashes.

### ci: all-mock deterministic profile

```yaml
profile: ci
providers:
  embedding: { adapter: mock, model: mock-embed-256 }
  generator: { adapter: mock, model: mock-gen }
  reranker:  { adapter: mock, model: mock-rerank }
```

The mock adapters are deterministic (sha256-seeded for embeddings, Jaccard for reranking, first-sentence extraction for generation). No network, no randomness beyond a fixed seed. CI eval numbers are byte-identical across runs (modulo `run_id` and timestamp, which are excluded from the determinism assertion). **Always use `MJD_PROFILE=ci` in CI.**

### hybrid-key: Anthropic generator + OpenAI embeddings + local reranker

Create `config/local.yaml`:

```yaml
providers:
  embedding:
    adapter: openai
    model: text-embedding-3-large
  generator:
    adapter: anthropic
    model: claude-3-5-haiku-20241022
  reranker:
    adapter: local
    model: bge-reranker-base
```

And `.env` (gitignored):

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```

Then `docker compose up --build`. The factory reads the adapter name from config, resolves the key via [`providers/secrets.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/providers/secrets.py), and constructs the adapter. Missing keys raise `MissingSecretError` at construction time.

---

## Embedding, generator, and reranker providers: adapter reference

| Adapter | Embedding | Generator | Reranker | Keys required |
|---|---|---|---|---|
| `local` | bge-small-en-v1.5 (sentence-transformers) | Optional local LLM; abstain stub if absent | bge-reranker-base (cross-encoder) | NO (default) |
| `mock` | sha256-seeded 256-dim hash | First-sentence extraction + verbatim citations | Jaccard overlap | NO (CI) |
| `anthropic` | No first-party embedding (falls back to `local`; logged in manifest) | Claude (claude-3-5-haiku or claude-3-5-sonnet) | Falls back to `local` | YES |
| `openai` | text-embedding-3-large or text-embedding-3-small | gpt-4o or gpt-4o-mini (optional) | Not supported; falls back to `local` | YES |
| `gemini` | text-embedding-004 | gemini-1.5-flash or gemini-1.5-pro | Not supported; falls back to `local` | YES |

**Provider gap resolution:** When a provider lacks a capability (e.g., `anthropic` has no first-party embedding model), the factory substitutes the configured `embedding.fallback` adapter (default `local`) and records the substitution in the manifest under `embedding.resolved_from`. This keeps the config coherent ("I want anthropic") while being honest about what actually ran.

---

## Provider protocol: what every adapter implements

```python
class EmbeddingProvider(Protocol):
    name: str
    def embed(self, texts: Sequence[str], *, kind: str = "document") -> EmbeddingResult: ...
    def health(self) -> dict: ...

class Generator(Protocol):
    name: str
    def generate(self, *, system: str, messages: list[dict], temperature: float = 0.0,
                 max_tokens: int = 1024, stop: list[str] | None = None) -> GenerationResult: ...
    def health(self) -> dict: ...

class Reranker(Protocol):
    name: str
    def rerank(self, query: str, candidates: list[str], *, top_n: int) -> RerankResult: ...
    def health(self) -> dict: ...
```

All adapters implement these protocols. The factory never inspects anything beyond the Protocol surface: which is why a new adapter slots in without touching existing code.

---

## Mock adapter internals: CI reproducibility

The mock adapters are fully specified in `docs/contracts.md` section 1.7:

**Mock embedder:** for each input string, computes `h = sha256(model_id + "\x1f" + kind + "\x1f" + text)`, derives 256 floats by seeding `random.Random(int.from_bytes(h, 'big'))` and drawing `random.uniform(-1, 1)` 256 times, then L2-normalizes. Identical input gives identical output across processes and OSes (pure stdlib).

**Mock generator:** extracts the first sentence of each `CONTEXT_BLOCK` and concatenates with verbatim citation tags from the block's metadata. If no context is provided, returns the exact insufficient-context boundary string. Token counts use `len(text.split())`. All costs 0.0.

**Mock reranker:** scores each candidate by Jaccard token overlap with the query (lowercased, whitespace-tokenized), ties broken by original index ascending. Fully deterministic.

---

## Secret resolution order

[`providers/secrets.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/providers/secrets.py): `resolve_secret(name: str) -> str | None`:

1. Environment variable with that name (e.g., `ANTHROPIC_API_KEY`).
2. Mounted secret file `/run/secrets/<name>` (Docker secrets pattern).
3. `None`. Adapters that require a key and receive None raise `MissingSecretError` at construction time.

The key value is never logged anywhere. No adapter ever writes the key to stdout, a logger, or a metrics emitter.

---

## Adding a new adapter

1. Create `providers/my_adapter.py` implementing `EmbeddingProvider`, `Generator`, and/or `Reranker` protocols.
2. Register the adapter name in [`providers/factory.py`](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/providers/factory.py) in the appropriate factory function.
3. Call `resolve_secret("MY_API_KEY")` inside the adapter's `__init__`. Raise `MissingSecretError` if the key is None and the adapter requires it.
4. Add the adapter name to the adapter set documentation in `docs/contracts.md` section 1.4.
5. The adapter's `health()` method must return `{"ok": bool, "model": str, ...}` so the `/health` endpoint can surface its status.

---

## Health endpoint

```bash
curl http://localhost:8000/health
```

Returns:

```json
{
  "ok": true,
  "providers": {
    "embedding": {"ok": true, "adapter": "local", "model": "bge-small-en-v1.5", "dim": 384},
    "generator": {"ok": true, "adapter": "local", "model": "local-instruct"},
    "reranker": {"ok": true, "adapter": "local", "model": "bge-reranker-base"}
  },
  "index": {"loaded": true, "index_version": "idx-YYYY-MM-DD-001", "documents": 51, "chunks": 1974},
  "profile": "default"
}
```

A mismatch between the index's recorded embedding model and the active adapter's model (G-18) sets `ok=false`. Queries fail with `embedding_model_mismatch` until the mismatch is resolved (re-index or revert the adapter config).
