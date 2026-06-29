---
doc_id: MJD-TEC-0009
title: Code Review and Branch Protection Standard
department: TECHNOLOGY
doc_type: STANDARD
classification: INTERNAL
owner_role: Head of Platform Engineering
allowed_roles: [SOFTWARE_ENGINEER, SECURITY_ARCHITECT]
effective_date: 2026-03-10
version: 2.5.0
review_cycle_months: 12
regulatory_refs: ["SOC 2 CC8.1", "NIST SP 800-218 (SSDF v1.1, PS and PW tasks)", "PCI DSS 4.0 Requirement 6.2.3", "NIST SP 800-53 Rev 5 (CM-5)"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Code Review and Branch Protection Standard

## Purpose and Scope

This standard defines how source code is reviewed and how protected branches are configured at Meridian John Doe Financial. Code review is the bank's primary human control for quality and security in the development process, and branch protection is the technical enforcement that makes review unavoidable. Together they ensure that no code reaches a production branch without independent human review and passing automated checks, satisfying the separation-of-duties and change-control expectations of SOC 2 and PCI DSS.

This standard applies to every source repository owned by Meridian J.D.: application code, infrastructure-as-code (MJD-TEC-0006), pipeline definitions (MJD-TEC-0005), and shared libraries. It is binding on all Technology and Platform Engineering teams. Meridian J.D. is a synthetic (FICTIONAL) entity, and every repository, identity, and control described here is illustrative.

The standard is deliberately prescriptive. Branch protection is the kind of control that decays quietly: a single relaxed setting can pass unnoticed for months and then become the path used to move unreviewed code into production. For that reason the settings below are stated as exact values, configured centrally, and reconciled continuously rather than left to per-team discretion.

## Definitions

**Pull request (PR).** A proposed change submitted for review and merge into a protected branch.

**Protected branch.** A branch (typically the default branch and release branches) whose update is governed by enforced rules; the canonical state of production code lives here.

**Required reviewer.** A reviewer whose approval is mandatory before merge, often a code owner for the affected area.

**Code owner.** The team or individual designated as the authoritative reviewer for a path in the repository.

**Required status check.** An automated check that must pass before merge is permitted.

**Signed commit.** A commit cryptographically signed so its author is verifiable and tampering is detectable.

**High-assurance repository.** A repository whose code handles authentication, authorization, cryptography, money movement, regulated data, or the integrity of the delivery pipeline itself. High-assurance status is assigned by Security Architecture and recorded in the central repository inventory.

**Standard repository.** Any repository not designated high-assurance. Standard repositories still carry full branch protection; they differ from high-assurance repositories chiefly in the minimum approval count and the mandatory presence of a security reviewer.

## 1. Code Review Principles

1.1 Every change to a protected branch is made through a pull request. Direct commits and direct pushes to a protected branch are technically blocked, not merely discouraged.

1.2 Every pull request is reviewed by at least one human other than the author before merge. High-assurance code (authentication, authorization, cryptography, money movement, regulated-data handling) requires review by a code owner and, where the change touches security controls, by a Security Architect.

1.3 Review is substantive: reviewers verify correctness, security, test coverage, and conformance to the relevant standards, not merely formatting.

1.4 Review is a control, not a courtesy. A reviewer who approves a change accepts shared accountability for it. Approval signals that the reviewer read the diff, understood the intent, exercised the rubric in section 7, and judged the change fit to merge. An approval given without that engagement is a control failure, addressed under section 8.

1.5 The author is responsible for making review possible. Pull requests are kept reviewable in size and scope (section 9), carry a clear description of intent and risk, and link to the originating change record in MJD-TEC-0008 where one is required.

## 2. Branch Protection Rules (Normative)

2.1 The following protections are enforced on every protected branch. They are configured centrally and cannot be disabled by a repository owner.

| Rule | Setting |
|---|---|
| Require pull request before merge | Enabled; no direct pushes |
| Minimum approving reviews | 2 approvals for high-assurance repositories; 1 approval minimum for all others |
| Require review from code owners | Enabled where a CODEOWNERS file designates owners |
| Dismiss stale approvals on new commits | Enabled; a new push invalidates prior approvals |
| Require required status checks to pass | Enabled; all checks in section 3 must pass |
| Require branches up to date before merge | Enabled |
| Require signed commits | Enabled |
| Require linear history | Enabled (squash or rebase merges) |
| Block force pushes | Enabled; force-push to a protected branch is prohibited |
| Block branch deletion | Enabled for protected branches |
| Include administrators | Enabled; rules apply to administrators with no bypass |
| Restrict who can push | Restricted to the pipeline service identity for merges |

2.2 The author of a pull request cannot approve their own pull request; their own approval does not count toward the required minimum. This enforces four-eyes (MJD-TEC-0008).

2.3 High-assurance repositories require two approving reviews; at least one must be from a code owner. Where the change modifies authentication, authorization, or cryptographic logic, one of the approvers must be a Security Architect.

### 2.4 Settings by Repository Tier

2.4.1 Both repository tiers carry the full protection set. The table below places the standard and high-assurance values side by side so the differences are explicit and so a reconciliation tool can compare live configuration against the baseline.

| Setting | Standard repository | High-assurance repository |
|---|---|---|
| Require pull request before merge | Enabled; no direct pushes | Enabled; no direct pushes |
| Minimum approving reviews | 1 | 2 |
| At least one approval from a code owner | Required where CODEOWNERS designates an owner | Always required |
| Security Architect approval | Required when change touches auth, authz, or crypto | Required when change touches auth, authz, or crypto |
| Author self-approval counts | No (blocked) | No (blocked) |
| Dismiss stale approvals on new commits | Enabled | Enabled |
| Require status checks to pass | Enabled (section 3) | Enabled (section 3) |
| Require branch up to date before merge | Enabled | Enabled |
| Require signed and verified commits | Enabled | Enabled |
| Require linear history | Enabled (squash or rebase) | Enabled (squash or rebase) |
| Block force pushes | Enabled | Enabled |
| Block protected-branch deletion | Enabled | Enabled |
| Include administrators (no bypass) | Enabled | Enabled |
| Restrict pushes to pipeline service identity | Enabled | Enabled |

2.4.2 The only deliberate differences between tiers are the minimum approval count and the always-on code-owner and security-reviewer requirements for high-assurance repositories. Every other protection is identical, so a standard repository is never a soft target relative to a high-assurance one; it is held to the same non-negotiable baseline and differs only in the depth of mandatory human review.

2.4.3 Repository tier is a property of the inventory, not of the local configuration. Promotion of a standard repository to high-assurance (for example, when it begins to handle cardholder data) is a Security Architecture decision that updates the inventory, which drives the central enforcement to apply the two-approval baseline automatically.

## 3. Required Automated Checks

3.1 The following pipeline checks (MJD-TEC-0005) are required status checks and must pass before a pull request can merge:

| Check | Blocking condition |
|---|---|
| Build | Build failure blocks |
| Unit and integration tests | Test failure or coverage below baseline blocks |
| SAST | New Critical or High finding blocks |
| SCA | New Critical or High CVE blocks |
| Secret scan | Any verified secret blocks |
| IaC policy-as-code | High misconfiguration blocks (for IaC repos) |
| Contract or schema validation | API contract drift blocks (for API repos) |

3.2 A required check cannot be marked passed manually. If a check is genuinely not applicable to a repository, it is removed from the required set by Platform Engineering with Security Architect concurrence, not overridden per pull request.

### 3.3 Required Status Checks Deep Dive

3.3.1 Each required check exists to gate a specific class of defect or risk. The table records what each check protects against, the threshold at which it blocks, and the system that owns and runs it, so that a blocked merge is always traceable to a named control and owner.

| Check | What it gates | Blocking threshold | Owning system |
|---|---|---|---|
| Build | Code that does not compile or assemble | Any build failure | CI build runner (MJD-TEC-0005) |
| Unit and integration tests | Functional regressions; untested change | Any failing test; line or branch coverage on changed code below the repository baseline | Test orchestration (MJD-TEC-0005) |
| SAST | Injection, unsafe deserialization, weak crypto usage, and similar code-level flaws | Any new Critical or High finding on changed lines | Static analysis platform |
| SCA | Vulnerable third-party dependencies | Any new Critical or High CVE introduced by the change | Software composition analysis service |
| Secret scan | Credentials, tokens, or keys committed to source | Any verified secret detected | Secret detection service; findings handled under MJD-TEC-0004 |
| IaC policy-as-code | Insecure infrastructure definitions (open ingress, public buckets, unencrypted stores) | Any High-severity policy violation | Policy engine (MJD-TEC-0006) |
| Contract or schema validation | Breaking changes to published API contracts | Any backward-incompatible contract drift | Contract registry and validator |

3.3.2 Coverage is measured on the changed code, not only on the repository as a whole, so that a large well-tested codebase cannot mask an untested new function. The per-repository coverage baseline is set with Security Architecture concurrence and recorded alongside the repository tier.

3.3.3 When a required check is genuinely not applicable (for example, contract validation on a repository that publishes no API), it is removed from the required set centrally under section 3.2. A check is never satisfied by re-running until it passes by chance, and a flaky check is fixed or quarantined by its owning team rather than ignored.

## 4. Commit Signing and Provenance

4.1 All commits to protected branches must be signed and verified. An unsigned commit cannot be merged. Signing keys are managed under the Secrets and Key Management Policy (MJD-TEC-0004).

4.2 The merge commit's identity flows into the artifact provenance attestation (MJD-TEC-0005 section 3), so a deployed artifact is traceable to verified, reviewed, signed source.

### 4.3 Signing, Verification, and Provenance Chain

4.3.1 Signing is identity-bound, not optional. Every engineer signs commits with a key issued and lifecycle-managed under MJD-TEC-0004. Keys are enrolled to a verified identity, rotated on the schedule defined in that policy, and revoked promptly on offboarding or suspected compromise. Personal or unmanaged signing keys are not accepted for protected-branch commits.

4.3.2 The platform verifies signatures at merge time. A commit whose signature is missing, unverified, or signed by a key that is not enrolled and currently valid is treated as unsigned and cannot merge. This makes signing a hard gate rather than an advisory marker.

4.3.3 Verified authorship feeds provenance. On merge, the verified signer identity and the pull request metadata are recorded in the artifact provenance attestation generated by the pipeline (MJD-TEC-0005 section 3). The result is an unbroken chain from a named, verified human author, through independent review and passing checks, to a signed merge, to a provenance-attested build artifact. An auditor can start from a deployed artifact and walk back to the reviewed and signed source that produced it.

4.3.4 Signing-key compromise is a security event. Suspected exposure of a signing key is reported under MJD-TEC-0004 and, where code integrity may be affected, raised as an incident under MJD-SEC-0006.

## 5. Merge Strategy and Linear History

5.1 Protected branches require linear history. Merges are completed by squash or rebase; traditional merge commits that introduce branching topology are not permitted on protected branches.

5.2 Squash merging is the default. It collapses a feature branch into a single, signed commit on the protected branch, producing a history in which each commit corresponds to one reviewed and merged pull request. This keeps the protected-branch history readable, makes provenance one-to-one with pull requests, and simplifies reverting a single change.

5.3 Rebase merging is available where a team needs to preserve a curated sequence of individual commits. Each resulting commit must still be signed and verified (section 4) and must descend from the up-to-date target branch (section 2.1).

5.4 Because force-push to a protected branch is blocked (section 2.1), history on a protected branch is append-only in practice: commits can be added through reviewed merges but cannot be silently rewritten or removed. Correcting a faulty change is done with a new, reviewed pull request (for example a revert), never by rewriting protected history.

## 6. CODEOWNERS and Ownership

6.1 Security-sensitive paths (authentication, cryptography, pipeline definitions, IAM and infrastructure modules) have explicit code owners including the Security Architecture function so that changes to them always route a security reviewer.

6.2 The CODEOWNERS file is itself a protected, reviewed artifact; changing ownership of a sensitive path requires Security Architect approval.

### 6.3 Sensitive Path Mapping

6.3.1 The CODEOWNERS file declares, for each sensitive area, the path patterns that area covers and the reviewer that must approve changes to it. The mapping below is the baseline for high-assurance repositories; individual repositories extend it but never remove coverage from a listed area.

| Sensitive area | Example path patterns | Required reviewer |
|---|---|---|
| Authentication | `/auth/`, `/identity/`, `/login/`, `**/session/**` | Identity team code owner plus Security Architect |
| Authorization | `/authz/`, `/permissions/`, `/policy/`, `**/rbac/**` | Owning team code owner plus Security Architect |
| Cryptography | `/crypto/`, `**/keys/**`, `**/signing/**`, `**/tls/**` | Security Architect (required) |
| Payments and money movement | `/payments/`, `/ledger/`, `/settlement/`, `/transfers/` | Payments team code owner plus Security Architect |
| Pipeline definitions | `/.pipelines/`, `/.ci/`, `**/*pipeline*.y*ml` | Platform Engineering code owner plus Security Architect |
| Infrastructure as code | `/infra/`, `/terraform/`, `**/*.tf`, `/k8s/` | Platform Engineering code owner plus Security Architect (MJD-TEC-0006) |
| Ownership file itself | `/CODEOWNERS`, `/.github/CODEOWNERS` | Security Architect (required) |

6.3.2 Because code-owner review is a required protection (section 2.1) and stale approvals are dismissed on new commits (section 2.1), a change that touches two sensitive areas requires approval from both designated owners, and any later push re-triggers their review.

6.3.3 The CODEOWNERS file protects itself. It lists itself as a sensitive path owned by Security Architecture, so an attempt to weaken ownership (for example, removing the Security Architect as an owner of the crypto path) is itself a change the Security Architect must approve. This closes the loop that would otherwise let an actor quietly remove the very reviewer who guards a sensitive area.

## 7. Code Review Rubric

7.1 Reviewers apply a consistent rubric so that review depth does not depend on individual habit. Every dimension below is considered on every pull request; the security and tests dimensions are weighted most heavily on high-assurance changes.

| Dimension | What the reviewer checks |
|---|---|
| Correctness | The change does what its description claims; edge cases, error paths, and concurrency are handled; no obvious logic defects. |
| Security | No injection, unsafe deserialization, broken access control, or weak crypto; secrets are not introduced (MJD-TEC-0004); input is validated and output encoded; authz checks are present where required. |
| Tests | New and changed behavior is covered by tests; coverage on changed code meets the baseline; tests assert behavior, not implementation detail, and would fail if the change regressed. |
| Performance | No needless N-plus-one queries, unbounded loops, or hot-path allocations; resource use is appropriate for expected load. |
| Readability and maintainability | Naming, structure, and comments make intent clear; the change fits existing patterns; complexity is justified. |
| Dependency hygiene | New dependencies are necessary, reputable, and license-compatible; SCA is clean (section 3); transitive risk is considered. |

7.2 The rubric is a floor, not a ceiling. Passing automated checks does not relieve the reviewer of judgment: a change can be green on every status check and still be wrong, unsafe, or unmaintainable, and it is the reviewer's job to catch that.

7.3 On a high-assurance change, the security dimension is non-negotiable. A reviewer who cannot personally vouch for the security of an auth, authz, or crypto change does not approve it; they request the required Security Architect review (section 2.3) instead.

## 8. Review Quality and Metrics

8.1 The program tracks review coverage (percent of merges with the required approvals), time-to-review, and the rate of post-merge defects, to keep review meaningful rather than perfunctory.

8.2 Repeated rubber-stamp approvals (approvals with no substantive engagement on high-assurance changes) are addressed with the relevant team and Security Architecture.

8.3 Review quality metrics feed the change-management program (MJD-TEC-0008): a repository with weak review coverage or fast-but-shallow approvals on high-assurance code is a change-discipline risk, and the two controls are assessed together rather than in isolation.

### 8.4 Review SLA and Quality Metrics

8.4.1 To keep review timely without sacrificing rigor, the program publishes service-level expectations and quality indicators. These are health signals for the control, not targets to be gamed; a metric that improves while review quality declines is itself investigated.

| Metric | Definition | Expectation |
|---|---|---|
| Time-to-first-review | Time from a pull request marked ready to the first substantive review | Within one business day for standard, prioritized for high-assurance |
| Review coverage | Percent of merges to protected branches with all required approvals recorded | 100 percent (any shortfall is a control failure, not a miss) |
| Rubber-stamp detection | Share of high-assurance approvals with no comments and time-to-approve below a credibility threshold | Trends to zero; outliers reviewed with the team |
| Re-review after changes | Percent of pull requests re-approved after a stale-approval dismissal triggered by a new push | 100 percent (enforced by section 2.1) |
| Post-merge defect rate | Defects traced to changes merged in a period, per repository | Tracked and trended; spikes feed MJD-TEC-0008 |

8.4.2 The 100 percent review-coverage figure is enforced by configuration, not by exhortation: because pull request and approval rules are required protections (section 2.1), a merge without the required approvals is impossible on a correctly configured repository. A measured shortfall therefore indicates a misconfiguration or bypass attempt and is investigated as a control failure (MJD-SEC-0009).

8.4.3 Rubber-stamp detection compares approval latency and engagement against the size and assurance level of the change. A large auth change approved in seconds with no comments is a credible signal of an empty approval and is surfaced to Security Architecture, regardless of who approved it.

## 9. Large Changes and Reviewable Scope

9.1 Oversized pull requests are a quality and security risk: reviewers fatigue, defects hide in volume, and the rubric in section 7 cannot be applied honestly to thousands of changed lines. Authors keep changes reviewable using the techniques below.

9.2.1 Split by concern. A behavioral change, a refactor, and a dependency bump are separate pull requests, each independently reviewable and revertable.

9.2.2 Draft pull requests. Work in progress is opened as a draft to gather early feedback without requesting formal approval; required reviewers are requested only when the change is ready, which keeps approval meaningful and avoids stale approvals being dismissed repeatedly.

9.2.3 Stacked pull requests. A large feature is delivered as a sequence of small, dependent pull requests, each merged in order. Every pull request in the stack is independently reviewed, signed, and subject to the same required checks and approval rules; the stack does not bypass any protection.

9.3 A large change is never an exception to branch protection. Splitting, drafting, and stacking make a big change reviewable; they do not reduce the required approvals, relax the required checks, or permit any bypass. Each constituent pull request stands on its own controls.

## 10. Bypass and Administrator Controls

10.1 There is no standing administrator bypass of branch protection. The "include administrators" setting is enabled so that even repository administrators are subject to the rules.

10.2 Any emergency situation that appears to require a protection bypass is handled through the emergency-change path (MJD-TEC-0008 section 5), not by disabling protection. Disabling branch protection on a protected branch is a security event raised under MJD-SEC-0009.

10.3 The absence of a bypass is intentional and load-bearing. A control that administrators can switch off under pressure fails exactly when it is most needed. Routing emergencies through the emergency-change path rather than a protection toggle preserves four-eyes and audit evidence even during an incident.

## 11. Worked Example: A High-Assurance Pull Request

11.1 To make the controls concrete, consider a pull request that changes token-validation logic in a payments service. The path is as follows, and no step can be skipped:

11.1.1 The engineer pushes to a feature branch and opens a pull request against the protected default branch. Direct push to the default branch is impossible (section 2.1).

11.1.2 Because the change touches authentication logic, the CODEOWNERS file (section 6.1) automatically requests a Security Architect as a required reviewer, and the high-assurance two-approval rule (section 2.3) applies.

11.1.3 The required status checks run: build, tests, SAST, SCA, secret scan, and contract validation (section 3.1). A new High SAST finding on the changed code blocks the merge until resolved.

11.1.4 Two approvals are obtained, one of them from the Security Architect. The author's own would-be approval does not count (section 2.2). A subsequent push to address review comments dismisses the prior approvals (section 2.1), so the approvers re-review the final state.

11.1.5 All commits are signed and verified (section 4.1); an unsigned commit would block the merge. On merge, the squash-or-rebase linear-history rule (section 5) keeps the branch history clean, and the merge identity flows into the artifact provenance (section 4.2).

11.1.6 The result is a deployed artifact provably built from reviewed, security-approved, signed source, satisfying separation of duties end to end.

## 12. Worked Example: Blocked Bypass Attempts

12.1 The following two attempts illustrate the controls preventing a bypass. Both fail by design, and both are visible afterward in the logs retained under MJD-SEC-0009.

### 12.2 Attempted Force-Push

12.2.1 An engineer, trying to rewrite history on the protected default branch to remove an embarrassing commit, runs a force-push to that branch.

12.2.2 The block-force-pushes protection (section 2.1) rejects the push at the server. No history is rewritten; the embarrassing commit remains, and the engineer's options are limited to a new, reviewed change (for example a revert) that adds to history rather than rewriting it.

12.2.3 Because the engineer is not the pipeline service identity, the restrict-who-can-push rule (section 2.1) would have rejected the push regardless of intent. The rejected force-push is logged; a pattern of such attempts is reviewed and, if it suggests an attempt to evade controls, escalated under MJD-SEC-0006.

### 12.3 Attempted Self-Approval

12.3.1 The same engineer opens a pull request and, wanting to merge quickly, approves their own pull request to reach the required approval count.

12.3.2 The self-approval does not count toward the minimum (section 2.2). The pull request remains short of its required approvals and cannot merge. On a high-assurance repository the change still additionally requires a code owner and, for the auth path here, a Security Architect (section 2.3), none of which the author can supply for their own change.

12.3.3 The engineer cannot fall back on administrator rights, because there is no admin bypass (section 10.1). The change merges only when genuine independent reviewers approve it. A deliberate effort to defeat four-eyes is treated as a change-discipline issue under MJD-TEC-0008 and, if warranted, a security incident under MJD-SEC-0006.

## 13. Roles and Responsibilities

**Software Engineer.** Submits changes as pull requests; keeps changes reviewable in size and scope (section 9); signs commits with a managed key (MJD-TEC-0004); applies the review rubric (section 7) when reviewing peers' code; provides substantive review; never attempts to bypass protection, force-push a protected branch, or defeat four-eyes through self-approval.

**Code Owner.** Provides authoritative review for owned paths and is accountable for the quality and security of changes merged into them; for sensitive paths this includes a security reviewer; keeps CODEOWNERS coverage for the owned area accurate.

**Security Architect.** Owns the protected-path CODEOWNERS entries (section 6); reviews changes to authentication, authorization, and cryptographic code; provides the required security approval on high-assurance auth, authz, and crypto changes; concurs on changes to the required-check set and to per-repository review counts and coverage baselines; owns the branch-protection configuration policy; investigates rubber-stamp signals, coverage shortfalls, and bypass attempts; assigns repository tier.

**Platform Engineering.** Configures and enforces branch protection centrally across all repositories; continuously reconciles live configuration against the tier baselines in section 2.4; operates the required status checks; removes truly inapplicable checks only with Security Architect concurrence (section 3.2); never grants per-pull-request overrides.

**Head of Platform Engineering.** Owner of this standard; accountable for enforced review and protection across the estate and for the review-quality program.

## 14. Exceptions and Escalation

14.1 No exception is granted to: the requirement that protected branches accept changes only via reviewed pull requests, the prohibition on self-approval, the block on force-push to protected branches, the signed-commit requirement, or the "include administrators" setting. These are non-waivable.

14.2 Adjusting the required-review count or the required-check set for a specific repository requires Security Architect concurrence and a recorded rationale; it is a configuration decision, never a per-pull-request override.

14.3 A direct push to a protected branch, a disabled protection setting, or a merged unsigned commit is a security incident escalated under the Incident Response Plan (MJD-SEC-0006).

14.4 Lowering a repository's tier (high-assurance to standard), or removing a sensitive path from CODEOWNERS, requires Security Architect approval and a recorded rationale, and is never done to expedite a single pull request.

## 15. Related Documents

- MJD-TEC-0001, Secure SDLC Policy
- MJD-TEC-0004, Secrets and Key Management Policy
- MJD-TEC-0005, CI/CD Pipeline Standard
- MJD-TEC-0006, Infrastructure as Code Standard
- MJD-TEC-0008, Change Management and Release Policy
- MJD-SEC-0006, Incident Response Plan
- MJD-SEC-0009, Logging, Monitoring, and SIEM Standard

## 16. Regulatory References

- SOC 2 Trust Services Criteria, CC8.1 (Change Management)
- NIST SP 800-218, SSDF v1.1 (Protect the Software / Produce Well-Secured Software tasks)
- PCI DSS 4.0, Requirement 6.2.3 (Code review of bespoke software)
- NIST SP 800-53 Rev 5, control CM-5 (Access Restrictions for Change)

## 17. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2022-08-08 | Platform Engineering | Initial code review and branch protection standard. |
| 2.0.0 | 2023-10-16 | Platform Engineering | Mandated branch protection on all protected branches and required status checks. |
| 2.3.0 | 2025-02-19 | Platform Engineering | Added signed-commit requirement and include-administrators setting. |
| 2.5.0 | 2026-03-10 | Platform Engineering | Set two-approval rule for high-assurance repositories; tightened CODEOWNERS for sensitive paths. |
