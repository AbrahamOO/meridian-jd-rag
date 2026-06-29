#!/usr/bin/env bash
# Evals ci_suite gate (devops-packaging contract item 6).
# Runs the ci eval suite and enforces the ci_gate from the eval report
# (contract 7.3): faithfulness >= threshold AND access_control_pass_pct == 100.
#
# The eval harness is part of the eval suite. When it is not yet present this
# gate PASSES with a clear notice rather than blocking the pipeline, so the API/
# packaging CI is green before the harness lands and HARD-gates once it exists.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

export MJD_PROFILE=ci

RUNNER=""
if [ -f scripts/run_evals.py ]; then
  RUNNER="python scripts/run_evals.py --suite ci"
elif [ -f evals/run.py ]; then
  RUNNER="python -m evals.run --suite ci"
fi

if [ -n "$RUNNER" ]; then
  echo "eval-gate: running ci suite via: $RUNNER"
  $RUNNER
fi

REPORT="evals/reports/latest.json"
if [ ! -f "$REPORT" ]; then
  echo "eval-gate: no eval report at $REPORT and no harness present yet."
  echo "eval-gate: SKIPPING (eval harness part of the eval suite). PASS."
  exit 0
fi

echo "eval-gate: enforcing ci_gate from $REPORT"
python - "$REPORT" <<'PY'
import json, sys
report = json.load(open(sys.argv[1]))
gate = report.get("ci_gate", {})
passed = gate.get("passed")
if passed is None:
    sec = report.get("security", {})
    gen = report.get("generation", {})
    thresholds = gate.get("thresholds", {})
    faith_min = thresholds.get("faithfulness_min", 0.9)
    acl_min = thresholds.get("access_control_pass_pct_min", 100.0)
    faith = gen.get("faithfulness", 0.0)
    acl = sec.get("access_control_pass_pct", 0.0)
    passed = faith >= faith_min and acl >= acl_min
    print(f"eval-gate: faithfulness={faith} (min {faith_min}), "
          f"access_control_pass_pct={acl} (min {acl_min})")
print("eval-gate:", "PASS" if passed else "FAIL")
sys.exit(0 if passed else 1)
PY
