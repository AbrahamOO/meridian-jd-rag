---
doc_id: MJD-TEC-0001
title: Secure SDLC Policy
department: TECHNOLOGY
doc_type: POLICY
classification: INTERNAL
owner_role: Chief Technology Officer
allowed_roles: [SOFTWARE_ENGINEER, SECURITY_ARCHITECT]
effective_date: 2026-01-15
version: 4.2.0
review_cycle_months: 12
regulatory_refs: ["NIST SP 800-218 (SSDF v1.1)", "PCI DSS 4.0 Requirement 6", "FFIEC Development and Acquisition Booklet", "SOC 2 CC8.1"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Secure Software Development Lifecycle (SDLC) Policy

## Purpose and Scope

This policy establishes the mandatory secure software development lifecycle for all software built, customized, or materially integrated by Meridian John Doe Financial (Meridian J.D.). It defines the security gates, threat-modeling requirements, dependency controls, and verification activities that every product team must satisfy before code reaches a production-bearing environment. The policy exists so that security is engineered into the product from inception rather than inspected in at the end, and so that the bank can demonstrate to examiners and auditors that controls described in NIST SP 800-218 and PCI DSS 4.0 Requirement 6 are operating effectively.

This policy applies to:

1. All first-party application code, infrastructure-as-code, and automation owned by the Technology and Platform Engineering organization.
2. All service code that processes, stores, or transmits customer data, money movement instructions, or authentication material.
3. Significant configuration of third-party platforms where Meridian J.D. owns the deployment (for example, identity provider tenants, API gateways, and data pipeline orchestrators).

This policy does not govern the procurement risk assessment of commercial off-the-shelf software, which is handled under the vendor risk program, nor does it govern model development governance, which is owned by Model Risk Management. Where software embeds a quantitative model, both this policy and the Model Risk Management Policy apply jointly.

Compliance is mandatory. A release that has not passed every required gate in this policy is unauthorized regardless of business pressure, and deploying it is a policy violation subject to the Exceptions and Escalation process in section 11.

## Definitions

**SDLC gate.** A control checkpoint at a defined phase of development where specific evidence must exist before work may advance. Gates are enforced by automation in the pipeline wherever technically feasible (see MJD-TEC-0005, CI/CD Pipeline Standard).

**Threat model.** A structured analysis of how an adversary could compromise a system, the assets at risk, the trust boundaries crossed, and the controls that mitigate each identified threat. Meridian J.D. uses the STRIDE methodology as its baseline, supplemented by data-flow diagrams. The RAG platform that retrieves this very document maintains a recursive self-threat-model of its own pipeline; that model references the Secrets and Key Management Policy (MJD-TEC-0004) for its secret-handling assumptions.

**Software Bill of Materials (SBOM).** A machine-readable inventory of all direct and transitive components in a software artifact, generated in CycloneDX format at build time.

**Production-bearing environment.** Any environment that can affect customers, money, or regulated data, including production and any pre-production environment that holds a copy of production data.

**Security champion.** An engineer embedded in a product team, trained by the Security Architecture function, who is the first point of contact for security questions and who owns the team's threat models.

**Critical and High severity finding.** A vulnerability rated using CVSS v3.1 base score, where Critical is 9.0 to 10.0 and High is 7.0 to 8.9. Severity drives remediation SLAs in section 8.

**Abuse case.** A negative requirement that describes how a feature could be intentionally misused by an adversary, expressed as a testable statement (for example, "an authenticated user must not be able to initiate a payment from an account they do not own").

**Definition of done (security).** The fixed set of security activities that must be complete before any user story is accepted, independent of functional acceptance criteria.

## 1. Lifecycle Phases and Mandatory Gates

The Meridian J.D. SDLC has six phases. Each phase has an entry gate that must be satisfied with recorded evidence in the engineering system of record (the ticketing platform plus the pipeline artifact store).

### 1.1 Phase 1: Inception and Requirements

1.1.1 Every new service or material feature begins with a recorded security requirements review. The product owner and the team's security champion jointly complete the Security Requirements Checklist, which captures data classification (per MJD-SEC-0008, Data Classification and Handling Standard), authentication and authorization needs, regulatory scope, and whether the work touches money movement.

1.1.2 If the work processes Confidential or Restricted data, or moves money, it is automatically designated **high-assurance** and is subject to the additional controls in section 6.

1.1.3 At least one abuse case must be authored for every new feature and recorded in the story. High-assurance features require an abuse case for each trust boundary the feature crosses. Abuse cases are owned by the product owner with input from the security champion, and each one becomes a candidate security test in Phase 4.

1.1.4 The output of this phase is a signed-off requirements record containing the data classification, the assurance tier, the regulatory scope, and the abuse-case set. Work may not enter design until this record exists.

### 1.2 Phase 2: Design and Threat Modeling

1.2.1 A threat model is mandatory for every new service, every change that crosses a trust boundary, and every high-assurance change. The threat model uses STRIDE and a current data-flow diagram. It is reviewed and signed off by a Security Architect.

1.2.2 The threat model gate cannot be waived for high-assurance work. For standard-assurance work, a Security Architect may accept a lightweight threat model attestation in lieu of a full review.

1.2.3 Authentication and authorization design must conform to the Authentication and Authorization Standard (MJD-TEC-0003). API designs must conform to the Public and Internal API Standard (MJD-TEC-0002).

1.2.4 Designs must apply the following secure-design principles, and the threat model must record how each is satisfied or why it is not applicable:

1. **Least privilege.** Every component, service account, and credential receives the minimum scope required, with no standing administrative access.
2. **Defense in depth.** No single control is the sole barrier protecting a Restricted asset; at least two independent controls protect any money-movement path.
3. **Secure defaults.** A misconfiguration must fail closed. Features ship disabled until explicitly enabled with a recorded owner.
4. **Complete mediation.** Every access to a protected resource is checked at the server, never trusted from a client-supplied assertion.
5. **Economy of mechanism.** Authorization logic is centralized in shared, reviewed libraries rather than reimplemented per endpoint.
6. **Separation of duties.** No single human identity can both author and unilaterally release a high-assurance change.

1.2.5 High-assurance threat models receive a peer review on a defined cadence. The authoring team's security champion and at least one Security Architect from outside the team review the model at design time, again before first production release, and at least once every six months while the service is active. Each review is recorded with a date and reviewer identity. The Threat Modeling Standard (MJD-SEC-0007) governs the review template and rating scheme.

### 1.3 Phase 3: Implementation

1.3.1 All code is written against the secure coding standards maintained by Security Architecture for each supported language (currently Python, TypeScript, Go, and Java). Coding standards prohibit the construction of SQL or other interpreted strings from untrusted input, mandate parameterized queries, and require that all output crossing a trust boundary be contextually encoded.

1.3.2 Secrets must never be committed to source control. Secret material is resolved at runtime per the Secrets and Key Management Policy (MJD-TEC-0004). Pre-commit secret scanning is mandatory and is enforced again in the pipeline.

1.3.3 All changes are submitted as pull requests and reviewed per the Code Review and Branch Protection Standard (MJD-TEC-0009). Direct commits to protected branches are technically prevented.

1.3.4 No user story is accepted until its security definition of done is complete. The security definition of done requires all of the following:

1. Every input deserialized from outside a trust boundary is validated against an explicit allowlist schema.
2. Every authorization decision is enforced server-side using the shared authorization library, with a test proving denial for an unauthorized principal.
3. All secrets are resolved at runtime; no credential, token, or key appears in source, configuration committed to source, or logs.
4. Errors returned to callers reveal no stack traces, internal hostnames, or query fragments; full detail is logged to the secure log sink only.
5. Each abuse case from Phase 1 has a corresponding automated test that demonstrates the abuse is prevented.
6. The change introduces no new SAST or SCA Critical or High finding, and any pre-existing finding it touches is remediated or has a recorded exception.

### 1.3.5 Secure Coding Standards by Language Family

The secure coding standards apply common rules across all languages: no string-concatenated queries, no dynamic code evaluation on untrusted input, no disabled certificate validation, and timing-safe comparison for secrets. The table below records the most enforced language-specific prohibited and required patterns. These are checked by SAST rules and reinforced in code review.

| Language | Prohibited patterns | Required patterns |
|---|---|---|
| Python | String-formatted SQL; `pickle`/`yaml.load` on untrusted data; `subprocess` with `shell=True`; `eval`/`exec` on input | Parameterized DB drivers; `yaml.safe_load`; `subprocess` with argument lists; `secrets` module for tokens; `hmac.compare_digest` for secret comparison |
| TypeScript | `innerHTML` with unsanitized data; `eval`/`Function` constructor; `any` on external payloads; building queries by concatenation | Framework auto-escaping or DOMPurify; parameterized queries or query builders; Zod/schema validation at every boundary; `strict` compiler mode |
| Go | `fmt.Sprintf` into SQL; ignoring returned `error` values; `math/rand` for tokens; unbounded `io.ReadAll` on requests | `database/sql` placeholders; explicit error handling; `crypto/rand` for tokens; `context` deadlines and body size limits |
| Java | String-concatenated JDBC; native Java deserialization of untrusted input; `Runtime.exec` with a parsed string; disabling TLS hostname checks | `PreparedStatement`; `SecureRandom`; allowlist deserialization filters; validated `ProcessBuilder` argument arrays |

### 1.4 Phase 4: Verification

1.4.1 The pipeline runs the following security verifications on every pull request and again on the merge commit:

| Verification | Tool class | Blocking threshold |
|---|---|---|
| Static analysis (SAST) | Semantic SAST engine | Any new Critical or High finding blocks |
| Software composition analysis (SCA) | Dependency scanner against SBOM | Any new Critical or High CVE blocks |
| Secret scanning | Entropy plus rule-based scanner | Any verified secret blocks |
| Infrastructure-as-code scanning | Policy-as-code engine | Any High misconfiguration blocks |
| Unit and integration tests | Test runner | Coverage below team baseline blocks |

1.4.2 Dynamic application security testing (DAST) is run against high-assurance services on a nightly schedule in the staging environment, and the results are triaged within one business day.

1.4.3 High-assurance services undergo a manual security code review by a Security Architect or a trained security champion outside the authoring team before their first production release and after any change to authentication, authorization, or cryptographic logic.

### 1.4.4 Security Testing Matrix

The following matrix maps each verification activity to when it runs, what it blocks, and which assurance tier requires it. Standard-assurance services run the full set of automated gates; high-assurance services additionally require interactive, manual, and adversarial testing.

| Test type | When it runs | What it blocks | Standard tier | High-assurance tier |
|---|---|---|---|---|
| SAST | Every pull request and merge | New Critical or High finding | Required | Required |
| SCA | Every build, against the SBOM | New Critical or High CVE | Required | Required |
| Secret scan | Pre-commit and in pipeline | Any verified secret | Required | Required |
| IaC scan | Every infrastructure change | Any High misconfiguration | Required | Required |
| IAST | Integration test runs in staging | Confirmed exploitable High finding | Recommended | Required |
| DAST | Nightly in staging | Confirmed Critical or High; triage in one business day | Recommended | Required |
| Manual code review | Before first release; after auth, authz, or crypto change | Unresolved reviewer security objection | Risk-based | Required |
| Penetration test | Before first production release; annually thereafter | Open Critical or High at release decision | Not required | Required |

### 1.5 Phase 5: Release

1.5.1 Release requires a passing pipeline, an approved change record per the Change Management and Release Policy (MJD-TEC-0008), and a signed build artifact whose provenance attestation matches the source commit (see MJD-TEC-0005).

1.5.2 The release gate verifies that no required verification in section 1.4 was skipped, overridden, or marked as a non-blocking exception without an approved exception record.

1.5.3 The release record captures the artifact digest, the SBOM reference, the set of gate evidence, the approvers, and the rollback plan. A release that cannot produce this record may not proceed.

### 1.6 Phase 6: Operation and Decommission

1.6.1 Production services are continuously monitored for newly disclosed vulnerabilities against their SBOM. A newly disclosed Critical CVE affecting a running service triggers the remediation SLA in section 8 from the moment of disclosure, not the next release.

1.6.2 Decommissioned services have their credentials and service-account secrets revoked immediately and their infrastructure destroyed through the same infrastructure-as-code path that created it (MJD-TEC-0006).

1.6.3 Operational security telemetry from running services feeds back into the threat model. A confirmed production security incident requires the affected service's threat model to be reviewed within ten business days and updated where the incident revealed a gap.

## 2. Threat Modeling Requirements

2.1 Threat models are living documents stored alongside the code repository. They are updated whenever a trust boundary changes.

2.2 Each identified threat must be linked to a mitigating control, an accepted-risk decision recorded by the appropriate risk owner, or a tracked remediation item with a due date.

2.3 The Security Architecture function maintains a library of reference threat models for common patterns (public API, internal service, batch pipeline, browser front end). Teams start from the closest reference and tailor it.

2.4 STRIDE categories map to baseline control families as follows: Spoofing maps to authentication controls in MJD-TEC-0003; Tampering and Information Disclosure map to data classification and encryption in MJD-SEC-0008; Repudiation maps to tamper-evident logging in section 9; Denial of Service maps to rate limiting and quotas defined in MJD-TEC-0002; and Elevation of Privilege maps to the least-privilege and complete-mediation principles in section 1.2.4.

## 3. Dependency and Supply-Chain Controls

3.1 Every build produces a CycloneDX SBOM that is stored with the artifact and is queryable for the life of the artifact in production.

3.2 New direct dependencies require explicit approval in code review. A dependency from an untrusted or unvetted registry is prohibited; internal package resolution is configured to prevent dependency-confusion substitution.

3.3 Build artifacts are signed and their provenance is attested per the CI/CD Pipeline Standard (MJD-TEC-0005). Unsigned artifacts cannot be deployed.

3.4 Dependencies are evaluated on intake for maintenance health, license compatibility, and known-vulnerability history. A direct dependency that is unmaintained or has an unresolved Critical vulnerability is not approved, and an existing one that becomes unmaintained is scheduled for replacement.

## 4. Vulnerability Triage and Exploitability

4.1 Severity from CVSS v3.1 sets the remediation SLA in section 8, but the triage order within a queue is refined by exploitability signals so that the most dangerous findings are addressed first.

4.2 Triage uses the following prioritization model. Findings are first sorted by the priority tier below, then by CVSS severity within the tier.

| Priority tier | Trigger condition | Action |
|---|---|---|
| P0 | On the CISA Known Exploited Vulnerabilities (KEV) catalog and reachable in a production-bearing service | Treat as Critical regardless of base CVSS; remediate on the Critical SLA |
| P1 | EPSS exploit-probability at or above 0.5, or a public weaponized exploit exists | Escalate one effective severity band for scheduling |
| P2 | CVSS Critical or High with no current exploit signal | Remediate on the SLA for its CVSS band |
| P3 | Present in the SBOM but not reachable from any exposed code path (confirmed) | Track; remediate on next dependency refresh; no SLA acceleration |
| P4 | Medium or Low with no exploit signal | Remediate per section 8 Medium or Low SLA |

4.3 A reachability or non-exploitability claim used to lower a finding from P2 to P3 must be evidenced (for example, by call-graph analysis or a configuration that disables the vulnerable path) and recorded by the security champion. An unverified claim does not change the tier.

4.4 Any deviation from these timelines requires a time-boxed risk acceptance under section 8.1. A finding may never be silently closed as "won't fix" without a recorded exception and a compensating control.

## 5. Developer Training and Security Champions

5.1 Every engineer completes secure development onboarding training before being granted write access to a production-bearing repository. Onboarding covers the secure coding standards, the abuse-case method, threat-modeling basics, and secret handling per MJD-TEC-0004.

5.2 All engineers complete an annual secure development refresh aligned to the current OWASP Top 10 and the language-specific standards in section 1.3.5. Completion is tracked and reported to the Engineering Manager; lapsed training is a finding against the team.

5.3 Each product team designates at least one security champion. Champions receive deeper training from Security Architecture, including threat-model authorship and finding triage, and attend a recurring champions forum to share emerging threats and patterns. The champion role is recognized in performance objectives, not treated as unpaid overhead.

5.4 High-assurance teams require at least two trained champions so that threat-model review and security definition-of-done verification are never blocked by a single person's absence.

## 6. Additional Controls for High-Assurance Work

6.1 Mandatory full threat model with Security Architect sign-off (no lightweight path).

6.2 Mandatory manual security code review before first production release and after any change to authentication, authorization, cryptography, or money-movement logic.

6.3 Mandatory DAST coverage and penetration testing before first production release.

6.4 Mandatory four-eyes deployment approval (two distinct human approvers) regardless of automation, per MJD-TEC-0008.

6.5 Mandatory IAST coverage during integration testing and at least two trained security champions per section 5.4.

## 7. Worked Example: A High-Assurance Feature Through All Six Phases

This non-normative example illustrates how a high-assurance feature, an instant peer-to-peer payment between Meridian J.D. account holders, moves through the lifecycle.

**Phase 1, Inception.** The product owner and security champion complete the Security Requirements Checklist. Because the feature moves money and reads account data classified Restricted under MJD-SEC-0008, it is designated high-assurance. They author abuse cases including "a user must not initiate a payment from an account they do not own" and "a replayed payment request must not move money twice." The signed requirements record fixes the assurance tier and the abuse-case set.

**Phase 2, Design and Threat Modeling.** The team starts from the public-API reference threat model and tailors it. STRIDE analysis flags Tampering of the payment amount in transit and Elevation of Privilege through a missing ownership check. The design centralizes the ownership check in the shared authorization library (complete mediation), requires idempotency keys to defeat replay, and applies defense in depth by validating the amount both at the API boundary and at the ledger service. A Security Architect signs off, and the model is scheduled for the six-month review cadence.

**Phase 3, Implementation.** Engineers implement in Go using `database/sql` placeholders and `crypto/rand` for idempotency keys per section 1.3.5. Secrets are resolved at runtime per MJD-TEC-0004. Each abuse case gets an automated test, including one proving a payment from a non-owned account is denied. The security definition of done in section 1.3.4 is completed before the stories are accepted.

**Phase 4, Verification.** SAST, SCA, secret scan, and IaC scan pass with no new Critical or High findings. IAST runs during integration tests, DAST runs nightly in staging, and a Security Architect outside the team performs a manual review of the authorization and money-movement logic. A penetration test is commissioned before release per the testing matrix.

**Phase 5, Release.** The pipeline is green, a change record is approved under MJD-TEC-0008, the artifact is signed with provenance matching the source commit, and two distinct human approvers authorize the deployment under the four-eyes rule. The release record captures the artifact digest, SBOM reference, evidence set, approvers, and rollback plan.

**Phase 6, Operation.** The service is monitored against its SBOM for new CVEs, with disclosure-time SLAs in effect. Payment telemetry feeds anomaly detection, and any confirmed incident triggers a threat-model review within ten business days.

## 8. Remediation Service Levels

The following SLAs apply from the time a finding is confirmed, measured against the deployed production state, not the next planned release:

| Severity (CVSS v3.1) | Production remediation SLA | Non-production remediation SLA |
|---|---|---|
| Critical (9.0 to 10.0) | 7 calendar days | 30 calendar days |
| High (7.0 to 8.9) | 30 calendar days | 60 calendar days |
| Medium (4.0 to 6.9) | 90 calendar days | next planned release |
| Low (0.1 to 3.9) | best effort, tracked | best effort, tracked |

8.1 A finding that cannot be remediated within its SLA requires a recorded, time-boxed risk acceptance approved by the service's risk owner and the Security Architecture function, with a compensating control documented.

8.2 SLA timers do not pause for sprint boundaries, release freezes, or staffing gaps. A team unable to meet an SLA must expedite the fix, deploy a compensating control, or record a time-boxed risk acceptance under 8.1.

## 9. Tooling and Evidence

9.1 All gate evidence (SAST, SCA, secret scan, test results, threat model sign-off, change approval, artifact signature) is retained for a minimum of 13 months to support audit, consistent with the Records Retention Schedule (MJD-CMP-0008).

9.2 Evidence is generated by the pipeline and is tamper-evident; manual assertions without pipeline backing are not accepted for high-assurance work.

9.3 Security-relevant events from the pipeline and production services are written to the central log sink referenced by the Incident Response Plan (MJD-SEC-0006), so that gate evidence and operational telemetry share a common, queryable record.

## 10. Security Metrics and Key Performance Indicators

Security Architecture reports the following KPIs to the Chief Technology Officer and the Chief Information Security Officer at least quarterly. Trends, not single readings, drive decisions.

| Metric | Definition | Target |
|---|---|---|
| Escaped-defect rate | Security findings discovered in production divided by total security findings for the period | Decreasing quarter over quarter |
| Mean-time-to-remediate, Critical | Average elapsed time from confirmation to fix for Critical findings | Within the 7-day Critical SLA |
| Mean-time-to-remediate, High | Average elapsed time from confirmation to fix for High findings | Within the 30-day High SLA |
| Gate pass rate | Pull requests passing all security gates without override on first run | At or above 90 percent |
| Exception backlog | Count of open time-boxed risk acceptances past their remediation date | Zero past-due |
| Coverage | Automated test coverage against each team's agreed baseline | At or above baseline |
| Training currency | Engineers with current annual secure development training | At or above 95 percent |

10.1 Any KPI breaching target for two consecutive periods is escalated to the Engineering Manager with a corrective action plan, and persistent breach is reported to the Board Technology Committee.

## 11. Roles and Responsibilities

**Software Engineer.** Writes secure code against the standards in section 1.3.5, authors and maintains threat models with the security champion, completes the security definition of done, resolves findings within SLA, and never bypasses gates.

**Product Owner.** Owns the abuse-case set for each feature, ensures security requirements are captured in Phase 1, and accepts that the security definition of done is a non-negotiable acceptance criterion, not a tradeable scope item.

**Security Champion.** Embedded engineer who owns the team's threat models, triages and tiers security findings per section 4, verifies the security definition of done, and escalates to Security Architecture when needed.

**Security Architect.** Reviews and signs off threat models and high-assurance code, owns the secure coding standards and reference threat models, runs the champions forum, and approves time-boxed risk acceptances.

**Engineering Manager.** Accountable for the team's adherence to this policy, for training currency, and for ensuring capacity exists to meet remediation SLAs.

**Chief Technology Officer.** Owner of this policy; accountable to the Board Technology Committee for the overall secure SDLC posture.

**Chief Information Security Officer.** Co-approves exceptions to high-assurance gates, receives the security KPIs in section 10, and owns the independent assurance functions (penetration testing and incident response per MJD-SEC-0006) that validate this policy from outside the engineering line.

**Risk Owner.** The accountable executive for the service who may accept time-boxed residual risk within delegated authority.

## 12. Exceptions and Escalation

12.1 Any deviation from a mandatory gate requires a formal exception request submitted before the deviation, not after. The request states the gate, the business justification, the compensating control, and a remediation date.

12.2 Exceptions to standard-assurance gates may be approved by an Engineering Manager plus a Security Architect. Exceptions to high-assurance gates (section 6) require the additional approval of the Chief Technology Officer and the Chief Information Security Officer.

12.3 No exception may be granted to the prohibition on committing secrets, to artifact signing, or to the access controls of the pipeline itself. These are non-waivable.

12.4 Discovery of a deployed release that bypassed a required gate is a security incident and is escalated under the Incident Response Plan (MJD-SEC-0006).

12.5 Every exception carries an expiry date. An exception reaching its expiry without remediation is automatically escalated to the Chief Information Security Officer, and the affected change may be rolled back at the discretion of Security Architecture.

## 13. Related Documents

- MJD-TEC-0002, Public and Internal API Standard
- MJD-TEC-0003, Authentication and Authorization Standard (OAuth2/OIDC)
- MJD-TEC-0004, Secrets and Key Management Policy
- MJD-TEC-0005, CI/CD Pipeline Standard
- MJD-TEC-0006, Infrastructure-as-Code Standard
- MJD-TEC-0008, Change Management and Release Policy
- MJD-TEC-0009, Code Review and Branch Protection Standard
- MJD-SEC-0006, Incident Response Plan
- MJD-SEC-0007, Threat Modeling Standard
- MJD-SEC-0008, Data Classification and Handling Standard
- MJD-CMP-0008, Records Retention Schedule

## 14. Regulatory References

- NIST SP 800-218, Secure Software Development Framework (SSDF) v1.1
- PCI DSS 4.0, Requirement 6 (Develop and Maintain Secure Systems and Software)
- FFIEC IT Examination Handbook, Development and Acquisition Booklet
- SOC 2 Trust Services Criteria, CC8.1 (Change Management)

## 15. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2022-03-01 | CTO Office | Initial secure SDLC policy. |
| 2.0.0 | 2023-04-12 | CTO Office | Added mandatory SBOM and SCA gates. |
| 3.0.0 | 2024-06-20 | CTO Office | Introduced high-assurance designation and remediation SLAs. |
| 4.0.0 | 2025-05-30 | CTO Office | Aligned gates with NIST SSDF v1.1 and PCI DSS 4.0; added provenance attestation requirement. |
| 4.2.0 | 2026-01-15 | CTO Office | Clarified threat model recursion for the RAG platform; tightened non-waivable controls; added secure coding standards by language, vulnerability triage and exploitability model, security testing matrix, KPIs, training and champions program, and a worked high-assurance example. |
