# ADR-006: Docs-Sync Rule and Drift Guard

**Status:** Accepted
**Created: 2026-06-29**
**Last updated: 2026-06-29**

---

## Context

Architecture-bearing code changes (new nodes in the query graph, changes to the access filter logic, new provider adapters, ingestion pipeline changes) must be reflected in the README diagrams, the wiki pages, and the ADRs. Without enforcement, documentation drifts from the code within days of the first untracked change.

Drift is particularly harmful for this system because the documentation makes specific security claims (the Mermaid sequence diagram in the README shows the access filter enforced before scoring; the threat model walkthrough cites specific line numbers). If the code changes and the diagrams do not, reviewers may evaluate the system based on how it is documented rather than how it works.

The naive approach (rely on developer discipline) produces accurate docs at launch and drifting docs three months later.

---

## Decision

Implement a docs-sync rule with two enforcement points:

**1. Git pre-commit hook:** `bash scripts/check_docs_sync.sh` runs before every commit. If any of the following files are modified in the staged diff and `README.md` or `wiki/*.md` are NOT also modified in the staged diff, the hook prints an advisory and exits non-zero, blocking the commit. Architecture-bearing paths monitored: `api/`, `retrieval/`, `ingestion/`, `generation/`, `providers/`, `infra/`, any `manifest.json`, `config/default.yaml`, `config/ci.yaml`.

The hook is opt-in per clone: `git config core.hooksPath .githooks` installs it. It is listed in `CONTRIBUTING.md`. The Makefile target `make hooks` installs it automatically.

**2. CI drift guard:** The same `check_docs_sync.sh` script runs as a step in `.github/workflows/ci.yml` (after tests, before completion). On a pull request, it diffs the changed files against the PR's base SHA. If architecture-bearing files changed without corresponding README or wiki changes, CI fails with a list of the offending paths and a reminder to update the documentation.

The script is advisory-style (it lists what changed and what was not updated) rather than prescriptive (it does not attempt to auto-generate docs). Auto-generation of Mermaid diagrams from code is brittle; the diagrams in this system are intentionally authored and verified.

**The docs-sync rule for this system:** every Markdown document created or modified must carry the doc-date fields (`Created:` and `Last updated:`) near the top and a `## Change History` section at the bottom with a newest-first entry using a colon separator (never an em dash). No em dashes anywhere in documentation.

---

## Consequences

**Enables:**
- Documentation stays honest: a reviewer reading the README diagrams can trust they reflect the actual code.
- Security claims in the threat model remain accurate: the cited line numbers and file paths in `security/THREAT_MODEL.md` are checked against the current code by the CI drift guard.
- Contributors receive immediate feedback (via the pre-commit hook) rather than discovering at PR review time that they forgot to update the docs.

**Constrains:**
- Contributors must update docs with every architecture-bearing code change. Small refactors that do not change the public behavior of the system (renaming a local variable, extracting a helper function) do not trigger the guard because they do not touch the monitored paths.
- The pre-commit hook is opt-in per clone. It is enforced in CI, but a contributor who forgets to install the hook will discover the failure at CI time, not commit time. This is an acceptable trade-off given the CI enforcement backstop.
- Documentation maintainers regenerate affected README sections, Mermaid diagrams, and wiki pages when architecture-bearing files change. This is the docs-sync duty.

---

## Change History

- 2026-06-29: Initial ADR accepted.
