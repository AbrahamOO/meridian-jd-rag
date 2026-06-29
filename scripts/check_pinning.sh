#!/usr/bin/env bash
# Dependency pinning check (devops-packaging contract item 6).
# Every dependency in requirements*.txt MUST be pinned with `==`. Unpinned (>=,
# ~=, *, or bare) deps fail CI so builds stay reproducible.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

status=0
for file in requirements.txt requirements-ci.txt; do
  [ -f "$file" ] || continue
  while IFS= read -r line; do
    # Strip comments and whitespace.
    trimmed="$(printf '%s' "$line" | sed 's/#.*//' | xargs || true)"
    [ -z "$trimmed" ] && continue
    if ! printf '%s' "$trimmed" | grep -Eq '=='; then
      echo "UNPINNED dependency in $file: $trimmed"
      status=1
    fi
  done < "$file"
done

if [ "$status" -eq 0 ]; then
  echo "pinning: all dependencies are pinned with ==. OK."
fi
exit $status
