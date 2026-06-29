# Packaging and import convention

Flat layout: each top-level directory (`providers/`, `config/`, `ingestion/`,
`retrieval/`, ...) is its own importable package with an `__init__.py`. Import
absolutely from the repo root, e.g. `from providers.factory import
get_generator` and `from config.loader import load_config`. There is no `mjd/`
umbrella package; the repo root is the import root (installed editable via
`pyproject.toml`). Cloud adapters and heavy ML deps are lazily imported so the
zero-key mock/CI path stays light.
