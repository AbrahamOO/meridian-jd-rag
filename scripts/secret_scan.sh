#!/usr/bin/env bash
# Secret scan (devops-packaging contract item 6).
# Uses gitleaks when available; otherwise a grep-based fallback that catches the
# common credential shapes (API keys, private keys, AWS keys, bearer tokens) in
# tracked files. Test fixtures and synthetic canaries are excluded.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if command -v gitleaks >/dev/null 2>&1; then
  echo "secret-scan: using gitleaks."
  gitleaks detect --no-banner --redact --source . || {
    echo "secret-scan: gitleaks found potential secrets."
    exit 1
  }
  exit 0
fi

echo "secret-scan: gitleaks not found; using grep-based fallback."

# High-signal patterns. .env.example documents key NAMES with empty values, which
# is fine; we only flag NAMES followed by a real-looking value.
PATTERNS=(
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'AKIA[0-9A-Z]{16}'
  'sk-[A-Za-z0-9]{20,}'
  'sk-ant-[A-Za-z0-9_-]{20,}'
  'AIza[0-9A-Za-z_-]{30,}'
  '(ANTHROPIC|OPENAI|GEMINI)_API_KEY[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9_-]{16,}'
  'Bearer[[:space:]]+[A-Za-z0-9._-]{20,}'
)

# Files to scan: tracked files, excluding tests/fixtures, the env example, lockish
# dirs, and this script itself (which contains the patterns).
FILES="$(git ls-files \
  | grep -vE '^(tests/fixtures/|\.env\.example$|scripts/secret_scan\.sh$|.*\.lock$)' \
  | grep -vE '^(corpus/)' || true)"

status=0
for pat in "${PATTERNS[@]}"; do
  if [ -n "$FILES" ]; then
    hits="$(printf '%s\n' "$FILES" | xargs -I{} grep -EnH "$pat" "{}" 2>/dev/null || true)"
    if [ -n "$hits" ]; then
      echo "POTENTIAL SECRET (pattern: $pat):"
      printf '%s\n' "$hits"
      status=1
    fi
  fi
done

if [ "$status" -eq 0 ]; then
  echo "secret-scan: no secrets detected. OK."
fi
exit $status
