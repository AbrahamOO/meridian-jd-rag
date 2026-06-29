# Contributing to Meridian J.D. RAG

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist. This is a portfolio demonstration. See NOTICE.md.

---

## House rules

### The mock-provider rule

CI always runs `MJD_PROFILE=ci`. Every test, eval, and CI gate uses the all-mock deterministic provider profile. No test in `tests/` may make a real network call, require an API key, or depend on a real language model. If you need to test provider-specific behavior, mock it via the `MockEmbeddingProvider`, `MockGenerator`, or `MockReranker` in `providers/mock.py`.

### The no-em-dash rule

No Unicode em dashes (the U+2014 character) anywhere: not in code comments, not in docstrings, not in Markdown documentation, not in error messages, not in prompts, not in generated corpus text. Use commas, colons, parentheses, or reword the sentence. This rule is enforced by `scripts/check_em_dash.sh`, which runs in CI and in the `.githooks/pre-commit` hook.

Example:
- WRONG: a sentence that uses an em dash to set off a clause.
- RIGHT: "Access control, enforced pre-scoring, prevents leaks."
- RIGHT: "Access control (enforced pre-scoring) prevents leaks."

### The doc-date and Change History rule

Every Markdown document you create or modify (except LICENSE, CONTRIBUTING.md, and SECURITY.md) must:

1. Carry `Created: YYYY-MM-DD` and `Last updated: YYYY-MM-DD` near the top, below the title.
2. Have a `## Change History` section at the bottom.
3. List changes newest-first with a colon separator: `- YYYY-MM-DD: <summary of change>`.

Use a colon. Never an em dash. Example:
```
## Change History

- 2026-06-29: Added section on provider gap resolution.
- 2026-06-28: Initial version.
```

---

## Setting up the pre-commit hook

The docs-sync drift guard runs as a pre-commit hook. Install it with:

```bash
git config core.hooksPath .githooks
```

Or via Make:

```bash
make hooks
```

The hook checks that any architecture-bearing code change (`api/`, `retrieval/`, `ingestion/`, `generation/`, `providers/`, `infra/`, config files) is accompanied by an update to `README.md` or the relevant `wiki/*.md` page. If not, the commit is blocked with a list of the files that need updating.

---

## Development workflow

```bash
# Install dev dependencies:
pip install -r requirements-ci.txt

# Lint and type-check:
make lint

# Auto-format:
make fmt

# Run tests:
make test

# Build the CI index and run the eval gate:
make ingest
make eval

# Run the access-control proof battery:
make prove-access
```

All commands should exit 0 before you submit a pull request.

---

## Adding a new document to the corpus

1. Create the document file in `corpus/<department>/` following the metadata schema in `docs/contracts.md` section 2.1.
2. Set `doc_id`, `classification`, `allowed_roles`, `entity_status: FICTIONAL`, and all other required fields.
3. Run `make ingest` with `dry_run: true` first to validate without writing the index.
4. Confirm `rejected: []` in the response.
5. Run `make prove-access` to confirm zero leaks.
6. Run `make eval` to confirm the CI gate still passes.

---

## Adding a new provider adapter

See `wiki/Provider-and-Config-Guide.md` and ADR-003 (`docs/adr/003-provider-interface-and-adapters.md`).

---

## Pull request checklist

- [ ] `make lint` passes (ruff + black --check + mypy)
- [ ] `make test` passes (144+ tests, MJD_PROFILE=ci, exit 0)
- [ ] `make prove-access` passes (0 leaks, exit 0)
- [ ] `make eval` passes (CI gate, faithfulness >= 0.9, access_control_pass_pct = 100.0%)
- [ ] If architecture-bearing files changed, README diagrams and wiki pages updated
- [ ] No em dashes in any new or modified text
- [ ] New/modified Markdown docs carry `Created:`, `Last updated:`, and `## Change History`
- [ ] No hardcoded API keys, secrets, or real PII introduced
