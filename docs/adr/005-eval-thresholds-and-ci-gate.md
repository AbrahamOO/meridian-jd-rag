# ADR-005: Eval Thresholds and CI Gate

**Status:** Accepted
**Created: 2026-06-29**
**Last updated: 2026-06-29**

---

## Context

The eval harness runs 78 golden questions against the query pipeline and produces a structured report. Some of these metrics must gate CI to prevent regressions. The challenge is choosing thresholds that are:

1. **Meaningful with mock providers.** CI runs `MJD_PROFILE=ci` (all-mock, deterministic). The mock generator is extractive and triggers the output_guardrail's insufficiency check on most content questions, resulting in low `answer_correctness`. Any threshold on `answer_correctness` would require the mock to produce correct prose, which defeats the purpose of a zero-key mock.

2. **Actually assertable as regressions.** A threshold that would never be breached by any plausible code change is useless. A threshold that is breached by normal mock behavior is wrong.

3. **Security-first.** The most important properties (access control, injection resistance, PII containment) must be gated at 100.0% with no tolerance. A single individual record failure is a release blocker, not just an aggregate metric degradation.

The naive approach (gate on every metric including answer_correctness) would require the CI mock to produce realistic prose, which requires a real language model and API keys. This violates the zero-key CI requirement.

---

## Decision

Gate CI on exactly two aggregate metrics:

1. **`faithfulness >= 0.9`** (currently: 1.000). Faithfulness measures whether generated claims are grounded in the retrieved context. The mock generator, being extractive, produces only grounded output (first sentence of context, verbatim). Faithfulness 1.0 under mock is the correct expectation. A regression below 0.9 indicates the output_guardrail or the prompt delimiting has been broken.

2. **`access_control_pass_pct >= 100.0`** (currently: 100.0%). Must be exactly 100%. Any value below 100% means at least one `access_boundary` eval record failed, meaning the system leaked a doc_id or returned content for a denied query. This is a security regression.

Additionally, enforce hard fails at the individual record level (regardless of aggregate):

- `access_enforced=false` on any record: release blocker.
- `injection_obeyed=true` on any record: release blocker.
- `pii_leaked=true` on any record: release blocker.

These are security properties where a single violation is unacceptable. They are checked individually, not as aggregates.

**Profile honesty rule (normative):** documentation, the README, and any public-facing description of eval results must state clearly that `answer_correctness=0.295` and `citation_accuracy=0.295` under CI are expected and correct for the mock profile. They are not bugs. The CI-gated metrics (faithfulness, access_control_pass_pct) are the quality guarantees. Real answer-correctness requires running under a non-mock profile.

**What is explicitly NOT gated in CI:**
- `answer_correctness`
- `citation_accuracy`
- Retrieval metrics (context_precision, context_recall, etc.)
- Latency (useful as a trend signal but not gated, because the mock latency is dominated by test harness overhead)

These metrics are reported and visible on the dashboard, but regressions in them require a non-mock eval run to be meaningful.

---

## Consequences

**Enables:**
- CI is zero-key, deterministic, and fast (~30 seconds for 78 evals).
- Security regressions (access control, injection, PII) block CI immediately with a clear failure message.
- Faithfulness regressions (broken prompt, broken output_guardrail, broken context assembly) are caught by the CI gate.
- The dashboard accurately reports all metrics, including the ones that are low under CI, with an honest note about the mock profile.

**Constrains:**
- Answer quality regressions (model changed, prompt degraded, retrieval quality dropped) are not visible in CI. They require running `make eval SUITE=full` with a real provider profile. This is a deliberate trade-off: CI is fast and zero-key; full-suite evals require a deployment environment.
- The eval report must always carry a `profile` field so that CI results are clearly distinct from real-provider results. Mixing CI and hybrid-key results in the same trend line is a documentation error.

---

## Change History

- 2026-06-29: Initial ADR accepted.
