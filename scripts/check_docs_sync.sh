#!/usr/bin/env bash
# Docs-sync drift guard (devops-packaging contract item 6/7).
#
# Fails if any code/infra change in the diff is NOT accompanied by a docs change.
# "Code/infra" = files under api/ retrieval/ ingestion/ generation/ providers/
# infra/ or a manifest. "Docs" = README.md, anything under docs/ or wiki/.
#
# Used by CI and as a git pre-commit hook. The base for the diff is resolved in
# this order: explicit $1 ref, then origin/main, then the previous commit (HEAD~1),
# then (for an initial commit or a clean tree) the staged set. Exit 0 = in sync.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Patterns that count as "code/infra" (a docs-sync trigger).
CODE_REGEX='^(api/|retrieval/|ingestion/|generation/|providers/|infra/|.*manifest.*)'
# Patterns that count as "docs" (satisfy the requirement).
DOCS_REGEX='^(README\.md|docs/|wiki/)'

resolve_base() {
  if [ "${1:-}" != "" ]; then
    echo "$1"
    return 0
  fi
  if git rev-parse --verify --quiet origin/main >/dev/null 2>&1; then
    echo "origin/main"
    return 0
  fi
  if git rev-parse --verify --quiet HEAD~1 >/dev/null 2>&1; then
    echo "HEAD~1"
    return 0
  fi
  echo ""  # no base: fall back to staged/working set
}

BASE="$(resolve_base "${1:-}")"

if [ -n "$BASE" ]; then
  CHANGED="$(git diff --name-only "$BASE"...HEAD 2>/dev/null || git diff --name-only "$BASE" 2>/dev/null || true)"
else
  # No base ref: use the staged set, else the full working-tree change set.
  CHANGED="$(git diff --cached --name-only 2>/dev/null || true)"
  if [ -z "$CHANGED" ]; then
    CHANGED="$(git diff --name-only 2>/dev/null || true)"
  fi
fi

if [ -z "$CHANGED" ]; then
  echo "docs-sync: no changes detected; OK."
  exit 0
fi

CODE_CHANGED="$(printf '%s\n' "$CHANGED" | grep -E "$CODE_REGEX" || true)"
DOCS_CHANGED="$(printf '%s\n' "$CHANGED" | grep -E "$DOCS_REGEX" || true)"

if [ -z "$CODE_CHANGED" ]; then
  echo "docs-sync: no code/infra/manifest changes; OK."
  exit 0
fi

if [ -n "$DOCS_CHANGED" ]; then
  echo "docs-sync: code/infra changed AND docs changed; in sync. OK."
  exit 0
fi

echo "docs-sync: DRIFT DETECTED."
echo "The following code/infra/manifest files changed without any docs update:"
printf '  %s\n' $CODE_CHANGED
echo ""
echo "Update one of: README.md, docs/**, or wiki/** to document the change,"
echo "or split the change so the docs land together. Drift guard failed."
exit 1
