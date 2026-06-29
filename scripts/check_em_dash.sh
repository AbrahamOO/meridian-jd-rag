#!/usr/bin/env bash
# Style guard: no Unicode em dash (U+2014) anywhere in source or docs.
# The project doctrine forbids em dashes; use commas, colons, or rewording.
# Run by CI and by the .githooks/pre-commit hook. Exit 0 = clean.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# The em dash byte sequence in UTF-8 is E2 80 94. Search source/doc files only,
# excluding vendored, build, VCS, and local agent directories.
EMDASH=$'\xe2\x80\x94'

HITS="$(grep -rIn "$EMDASH" \
  --include='*.py' --include='*.md' --include='*.mdx' --include='*.markdown' \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' \
  --include='*.yaml' --include='*.yml' --include='*.json' --include='*.toml' \
  --include='*.sh' --include='*.sql' --include='*.tf' \
  . 2>/dev/null \
  | grep -vE '(^|/)(\.git|\.venv|venv|node_modules|\.claude|dist|build|\.next)/' \
  || true)"

if [ -n "$HITS" ]; then
  echo "em-dash check: FAIL. Found U+2014 em dashes:"
  printf '%s\n' "$HITS"
  echo "Replace each with a comma, colon, or reworded sentence."
  exit 1
fi

echo "em-dash check: OK (no U+2014 found)."
