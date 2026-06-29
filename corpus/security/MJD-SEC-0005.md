---
doc_id: MJD-SEC-0005
title: Vulnerability and Patch Management Standard
department: SECURITY
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT, SOFTWARE_ENGINEER]
effective_date: 2026-01-25
version: 3.2.0
review_cycle_months: 12
regulatory_refs: ["PCI DSS 4.0 Requirement 6", "PCI DSS 4.0 Requirement 11", "NIST SP 800-40 Rev 4", "NIST SP 800-53 Rev 5 (RA, SI families)", "FFIEC Information Security Booklet", "CISA BOD 22-01 (KEV)"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Vulnerability and Patch Management Standard

## Purpose and Scope

This standard defines how Meridian John Doe Financial (Meridian J.D.) discovers, prioritizes, remediates, and verifies the closure of security vulnerabilities across its estate. It establishes the scanning regime, the severity model, the remediation service level agreements (SLAs) by severity, the patch testing and deployment process, and the exception path. Its central, binding output is the patch SLA table in Section 3: the maximum time permitted to remediate a vulnerability as a function of its severity.

This document is classified CONFIDENTIAL and readable by SECURITY_ARCHITECT and SOFTWARE_ENGINEER, because engineers own the remediation of vulnerabilities in the code and infrastructure they maintain and must know the SLAs that bind them.

Scope covers operating systems, container images, application dependencies, network devices, cloud configurations, and the application code itself, across production, staging, and development. It includes the dependencies and runtime of internal AI and retrieval systems.

## Definitions

**Vulnerability.** A weakness in a system that could be exploited to compromise confidentiality, integrity, or availability.

**CVSS.** Common Vulnerability Scoring System, the 0.0 to 10.0 numeric severity scale used to rank vulnerabilities.

**KEV.** Known Exploited Vulnerabilities, the CISA catalog of vulnerabilities with confirmed active exploitation.

**Patch.** A vendor or maintainer fix that remediates a vulnerability.

**Remediation.** Eliminating a vulnerability, by patching, reconfiguring, upgrading, or removing the affected component.

**Mitigation.** A compensating control that reduces risk when remediation is not immediately possible.

**SLA.** The maximum elapsed time, from detection to verified remediation, permitted for a vulnerability of a given severity.

**Exposure.** Whether an affected asset is internet-facing, internal, or isolated, which modifies prioritization.

**SBOM.** Software Bill of Materials: a machine-readable inventory of the components comprising a software artifact.

**EOL.** End of Life: the date after which a vendor no longer provides security updates for a product.

## 1. Vulnerability Discovery

### 1.1 Scanning Regime

1.1.1 Authenticated infrastructure vulnerability scans run weekly across all in-scope hosts and continuously for internet-facing assets.

1.1.2 Container images are scanned at build time in the CI/CD pipeline (MJD-TEC-0005) and continuously in the registry as new vulnerability data arrives. An image with an unremediated Critical vulnerability is blocked from deployment.

1.1.3 Software composition analysis scans every application dependency against vulnerability feeds on every build and daily thereafter. Cloud configuration is scanned continuously against the secure baseline.

1.1.4 External penetration testing is performed at least annually and after major architectural change. Findings are tracked under this standard's SLAs.

### 1.2 Intake and Triage

1.2.1 Vulnerabilities from all sources (scanners, penetration tests, bug bounty, vendor advisories, threat intelligence) flow into a single tracking system with a unique identifier, affected asset, CVSS score, exposure, and exploit status.

1.2.2 Triage assigns each finding a severity (Section 2) and an owning team within one business day of intake.

### 1.3 Asset Inventory and Coverage Assurance

1.3.1 Accurate asset inventory is a prerequisite for scanning coverage. The security operations team maintains a continuously updated asset inventory that includes: hostname or container image digest, environment (production, staging, development), owner team, classification of data processed (per MJD-SEC-0008), internet-facing status, operating system or base image version, and last-seen date from the scanner.

1.3.2 Asset inventory is reconciled with cloud resource APIs, CMDB records, and the container registry on a weekly automated basis. Discrepancies (assets present in cloud APIs but absent from inventory, or assets in inventory with no recent scan result) are flagged as coverage gaps.

1.3.3 Coverage gaps are tracked in the vulnerability management system with a distinct gap identifier. Every gap must be resolved within 5 business days: either the asset is onboarded to the scanning regime, or it is formally excluded with a documented justification and compensating control. An unresolved gap beyond 5 business days is escalated to the asset owner's manager.

1.3.4 Coverage completeness is reviewed weekly by security operations. The metric reported to the Information Security Steering Committee (MJD-SEC-0001) monthly is: percentage of known production assets with a scan result within the last 7 days. The target is 100%; any asset below threshold is a finding.

1.3.5 Assets newly discovered through cloud-resource enumeration and not yet assigned an owner are placed in an unowned-assets queue, and the SECURITY_ARCHITECT is notified daily until each is claimed. Unclaimed assets beyond 10 business days are subject to access restriction pending ownership determination.

### 1.4 Third-Party and Vendor Vulnerability Notifications

1.4.1 Vendor security advisories are ingested from multiple channels: vendor mailing lists and RSS feeds monitored by security operations, the CISA KEV catalog (checked daily via automated feed), coordinated disclosure notifications received from vendors under contract, and threat intelligence subscriptions.

1.4.2 On receipt of a vendor advisory, security operations performs triage within one business day: identify which Meridian J.D. assets run the affected product and version, determine if the vulnerability is already in the tracking system from scanner data, assign severity using the model in Section 2, and assign an owning team. Vendor-disclosed CVEs that match a known asset are treated as confirmed and do not require scanner confirmation before the SLA clock starts.

1.4.3 Contracts with software vendors and managed service providers require the vendor to: notify Meridian J.D. of a security vulnerability in a product or service delivered under the contract within 24 hours of the vendor's own awareness; provide a patch or mitigation timeline; and cooperate with Meridian J.D. during remediation. Failure to notify within 24 hours is a contract breach and is escalated to the vendor relationship owner.

1.4.4 Vendor-specific CVEs for products with limited scanner support (embedded firmware, proprietary appliances) are triaged manually. The owning team validates the affected version by examining the deployed configuration directly, and the result is documented in the tracking system as the confirming evidence.

## 2. Severity Model

### 2.1 Base Severity from CVSS

2.1.1 Severity is derived from the CVSS v3.1 base score, then adjusted by exploitability and exposure:

| Severity | CVSS base score |
|---|---|
| Critical | 9.0 to 10.0 |
| High | 7.0 to 8.9 |
| Medium | 4.0 to 6.9 |
| Low | 0.1 to 3.9 |

### 2.2 Severity Escalators (override the base)

2.2.1 A vulnerability listed in the CISA Known Exploited Vulnerabilities (KEV) catalog is treated as Critical regardless of its base CVSS score.

2.2.2 A vulnerability on an internet-facing asset is escalated one severity level (for example, a base High on a public endpoint is remediated on the Critical SLA).

2.2.3 A vulnerability affecting the cardholder data environment or any RESTRICTED-classified system is escalated one severity level.

### 2.3 Risk-Contextualized Prioritization

2.3.1 The CVSS base score alone is a starting point, not a final priority. Security operations applies a risk-contextualized score that adjusts the base using three additional factors: the CVSS environmental score, business criticality of the affected asset, and threat intelligence indicating active exploitation in the financial sector.

2.3.2 The CVSS environmental score accounts for the specific deployment context. The Modified Attack Vector is set to Network for internet-facing assets and to Local for isolated development hosts. The Confidentiality, Integrity, and Availability requirements are set based on the data classification (MJD-SEC-0008) of the asset: RESTRICTED data stores carry High requirements on all three vectors; CONFIDENTIAL assets carry High for Confidentiality and Medium for Integrity and Availability; INTERNAL assets carry Medium across all three.

2.3.3 Business criticality is assigned to each asset during onboarding and maintained in inventory. Criticality tiers are:

| Tier | Definition | Priority multiplier |
|---|---|---|
| Tier 1 | Revenue-generating or customer-facing; outage causes immediate customer impact | Highest: treat as one severity level higher than computed |
| Tier 2 | Internal operational; outage affects internal users but not customers directly | Standard computed severity applies |
| Tier 3 | Development, test, or non-production; no production data | May defer to the bottom of the severity queue without escalator |

2.3.4 Threat intelligence integration is performed by subscribing to financial-sector threat intelligence feeds (FS-ISAC and sector-specific CISA advisories). When a CVE is reported as actively exploited against financial institutions in the current intelligence cycle, the vulnerability is escalated to Critical (or remains Critical if already at that level) regardless of its base CVSS score. Security operations reviews the threat intelligence feed daily and annotates the tracking system with the active-exploitation flag and the source citation.

2.3.5 The effective priority for each finding is the combination of computed CVSS environmental score, business criticality tier, and active-exploitation flag. The tracking system surfaces a sorted worklist to owning teams reflecting this combined priority. Engineers remediate in effective-priority order when multiple findings compete for capacity.

## 3. Remediation SLAs by Severity (binding)

### 3.1 SLA Table

3.1.1 The maximum elapsed time from detection to verified remediation is:

| Severity | CVSS range | Remediation SLA (production) | KEV / actively exploited |
|---|---|---|---|
| Critical | 9.0 to 10.0 | 7 calendar days | 24 hours |
| High | 7.0 to 8.9 | 30 calendar days | 7 days if KEV-listed |
| Medium | 4.0 to 6.9 | 90 calendar days | n/a |
| Low | 0.1 to 3.9 | 180 calendar days | n/a |

3.1.2 The SLA clock starts at detection (the timestamp the vulnerability is confirmed in the tracking system), not at the time it is assigned. The clock stops only when remediation is verified by a confirming scan, not when a patch is merely deployed.

3.1.3 Internet-facing and RESTRICTED-system assets apply the escalator in Section 2.2, shortening the effective SLA by one tier.

3.1.4 Emergency (zero-day, KEV-listed, active exploitation) vulnerabilities follow the 24-hour Critical path and are managed jointly with the Incident Response Plan (MJD-SEC-0006) until remediated or mitigated.

### 3.2 When Remediation Cannot Meet SLA

3.2.1 If a patch is unavailable or cannot be deployed within SLA, an interim mitigation (virtual patch, network rule per MJD-SEC-0004, feature disablement) must be in place before the SLA expires, and a formal exception (Section 6) must be filed.

### 3.3 Escalation When SLA Is at Risk

3.3.1 The tracking system automatically calculates the elapsed percentage of the SLA for each open finding and triggers escalations at defined thresholds to prevent silent SLA breaches.

3.3.2 At 50% of SLA elapsed: the tracking system sends an automated notification to the owning engineer and their team lead, including the current remediation status, remaining time, and a link to the finding. No manual action is required at this stage unless the finding has no remediation activity recorded.

3.3.3 At 80% of SLA elapsed: the tracking system escalates to the engineering manager responsible for the owning team. The notification includes the full finding detail, the time remaining, the last-recorded remediation activity, and guidance on filing an exception if remediation cannot complete in time. The engineering manager is expected to acknowledge within 4 hours and either confirm a completion path or initiate exception filing.

3.3.4 At 100% of SLA elapsed (breach): the SECURITY_ARCHITECT receives an immediate alert. The finding is flagged as a control failure in the tracking system. The owning team is required to file a formal exception within 24 hours of breach with a documented compensating mitigation, residual risk assessment, and a target remediation date. The breach is recorded in the risk register (MJD-RSK-0001) regardless of whether an exception is approved. Active exploitation of an unpatched vulnerable asset at SLA breach escalates immediately under the Incident Response Plan (MJD-SEC-0006).

3.3.5 For KEV-listed Critical vulnerabilities with a 24-hour SLA, the escalation schedule is compressed: at 12 hours (50%) automated alert; at 20 hours (83%) escalation to engineering manager and SECURITY_ARCHITECT simultaneously; at 24 hours immediate SECURITY_ARCHITECT action is required.

## 4. Patch Testing and Deployment

4.1.1 Patches are deployed through the change pipeline (MJD-TEC-0008) with automated testing in staging before production, except emergency patches which follow the expedited change path with retroactive review.

4.1.2 Patch deployment uses progressive rollout (canary then full) with automated rollback on health-check failure.

4.1.3 Operating system and image patching is automated where possible; manual exceptions are tracked and minimized.

4.1.4 Container and image remediation favors rebuilding from a patched base image over in-place patching, so the fix is reproducible and the image content hash changes, allowing the registry scanner to confirm closure. Long-lived mutable hosts are the exception, not the norm; immutable infrastructure (MJD-TEC-0006) reduces the patch surface by replacement rather than modification.

### 4.2 Verification of Closure

4.2.1 A vulnerability is closed only when a confirming authenticated scan no longer detects it on the affected asset. A merged pull request, a deployed artifact, or a vendor patch applied without a confirming scan is "in progress", not "closed", and the SLA clock continues to run.

4.2.2 False positives are dispositioned with evidence (vendor advisory, configuration proof) and recorded; they do not count as breaches but are auditable.

### 4.3 Metrics and Reporting

4.3.1 Security operations reports the following monthly to the Information Security Steering Committee (MJD-SEC-0001): open vulnerabilities by severity, SLA conformance percentage by severity, count of KEV-listed vulnerabilities and their age, count of active exceptions, and mean time to remediate by severity.

4.3.2 SLA conformance for Critical and High vulnerabilities on internet-facing assets is a board-reported metric. A sustained decline triggers a remediation plan with executive sponsorship.

4.3.3 Minimum SLA conformance targets, measured monthly:

| Severity | Minimum SLA conformance target |
|---|---|
| Critical | >= 95% of Critical findings remediated within SLA |
| High | >= 90% of High findings remediated within SLA |
| Medium | >= 85% of Medium findings remediated within SLA |
| Low | >= 75% of Low findings remediated within SLA |

4.3.4 A reporting dashboard is maintained in the vulnerability management platform and is accessible to SECURITY_ARCHITECT and SOFTWARE_ENGINEER. The dashboard displays, at minimum: real-time open finding counts by severity and owning team; SLA conformance trend (12-month rolling); KEV-listed open findings with elapsed days; asset coverage percentage; exception register with expiry dates; and mean time to remediate trend by severity tier. The dashboard is the single source of truth; teams may not maintain separate tracking outside the platform.

### 4.4 Emergency Patch Deployment

4.4.1 Patches for Critical KEV-listed vulnerabilities follow the expedited change path defined in MJD-TEC-0008, which permits bypassing the standard staging-hold period with approval from the change manager and SECURITY_ARCHITECT. Testing in staging is still required but may proceed in parallel with production preparation. The retroactive review of the emergency change occurs within 5 business days.

4.4.2 For cases where a vendor patch is not yet available, the interim mitigation (virtual patch via WAF rule, network rule per MJD-SEC-0004, feature flag disablement) is deployed as a change on the emergency path and documented in the finding record as the interim closure event. The SLA exception must still be filed unless the mitigation fully eliminates exploitability as confirmed by a rescan.

### 4.5 Dependency and Third-Party Library Patching

4.5.1 Every software artifact built and deployed by Meridian J.D. must have an associated SBOM in CycloneDX or SPDX format, generated at build time by the CI/CD pipeline (MJD-TEC-0005). The SBOM lists all direct and transitive dependencies with their exact versions and known-CVE status at build time.

4.5.2 Software composition analysis tools consume the SBOM to identify vulnerabilities in the dependency tree, including transitive (indirect) dependencies. Transitive vulnerabilities are triaged under the same severity model and SLAs as direct dependencies; the depth of nesting in the dependency graph does not reduce the SLA.

4.5.3 When a transitive vulnerability is identified, the remediation path depends on the package ecosystem: in most cases, updating the direct dependency that pulls in the vulnerable transitive version is sufficient. Where the direct dependency has not yet released a fix, the owning team evaluates whether to apply a resolution override (pinning the transitive version) or to replace the direct dependency. Both paths are valid; the choice is documented in the finding record.

4.5.4 Vendored code (third-party source code copied into the repository and modified, rather than consumed as a versioned dependency) is treated as owned code for patching purposes: the owning team is responsible for applying upstream security patches manually. Vendored code must be documented in the SBOM with its upstream source and version. The number of vendored dependencies is minimized; new vendoring requires SECURITY_ARCHITECT approval.

4.5.5 Dependencies with no upstream maintainer (abandoned projects) are flagged in the SBOM with the last-maintained date. Abandoned dependencies with open vulnerabilities are treated as High or Critical (based on CVSS) and must be replaced rather than patched. A migration plan is required within 30 days of identification.

### 4.6 Legacy and End-of-Life Systems

4.6.1 An operating system, framework, runtime, or database that has reached its vendor-defined end-of-life date is ineligible to receive security patches from the vendor and therefore cannot be remediated through normal patching. EOL systems are subject to special governance under this section.

4.6.2 When a system component reaches EOL, the owning team must immediately notify security operations and register the component in the compensating control register. Within 30 days of EOL, the team must document one of the following dispositions: (a) a migration plan with a target completion date no later than 180 days after EOL; (b) a compensating control package (see 4.6.3) with SECURITY_ARCHITECT approval; or (c) decommissioning by the EOL date.

4.6.3 Compensating controls required for any approved EOL system in production include, at minimum: network isolation to the minimum required zone (MJD-SEC-0004), with no internet-facing exposure; enhanced host-based monitoring with real-time alerting on any new process, network connection, or file modification outside an approved baseline; virtual patching via WAF or IPS signature where applicable; prohibition on storing or processing RESTRICTED data; and a monthly access review by the SECURITY_ARCHITECT.

4.6.4 The maximum retention period for an EOL system in production under compensating controls is 12 months from the EOL date. An EOL system still in production at 12 months requires CISO approval and is reported to the Board Risk Committee as a material residual risk. No extensions beyond 24 months from EOL are permitted under any circumstance; the system must be decommissioned or replaced.

4.6.5 The compensating control register is maintained by security operations and reviewed monthly. It lists each EOL component, the owning team, the EOL date, the approved compensating controls, the disposition (migrate, decomm, or approved exception), the target completion date, and current status.

### 4.7 Patch Rollback Procedure

4.7.1 A patch deployment may be rolled back when: the patch causes a critical functional failure in production (as detected by health-check monitors or customer impact); the patch introduces a new vulnerability that is at least as severe as the one remediated; or the patch breaks a dependent system in a way that cannot be resolved within 2 hours of deployment.

4.7.2 Rollback authorization is required from the change manager and, for security-relevant rollbacks, from the SECURITY_ARCHITECT. The owning engineer may initiate an emergency rollback using the automated rollback mechanism in the pipeline and obtain authorization retroactively within 4 hours, provided health-check failure triggered the rollback. Manual rollback without automated health-check failure requires prior authorization.

4.7.3 A rollback that removes the patched state reinstates the vulnerability. Security operations is notified within 1 hour of any security patch rollback. The finding in the tracking system is reopened, the SLA clock resumes from the detection timestamp (not the rollback timestamp), and the patch is classified as "deployed but rolled back." The team must file a rollback incident report within 2 business days explaining the failure mode, the plan to redeploy the patch with the defect resolved, and the interim mitigation in place during the remediation gap.

4.7.4 Post-rollback re-assessment: the team reproduces the patch failure in staging, identifies the root cause (incompatible dependency, configuration conflict, regression), resolves it, and re-deploys the patch through the standard or emergency change path. The confirming scan after successful re-deployment resets the finding to "closed." The post-rollback re-assessment is documented in the finding record and reviewed by the SECURITY_ARCHITECT.

## 5. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this standard; sets severity model and SLAs; approves exceptions. |
| SOFTWARE_ENGINEER | Remediates vulnerabilities in owned code and infrastructure within SLA. |
| Security operations | Runs scans, triages findings, verifies closure, reports SLA conformance. |
| Change management | Gates and sequences patch deployments (MJD-TEC-0008). |
| Asset owners | Maintain accurate asset inventory so scanning coverage is complete. |

## 6. Exceptions and Escalation

6.1.1 An exception is required when an SLA cannot be met. It documents the affected asset, the reason, the compensating mitigation, the residual risk, and an expiry no later than the next severity-equivalent SLA period.

6.1.2 Critical and High exceptions require SECURITY_ARCHITECT approval; exceptions on RESTRICTED systems or the cardholder data environment require CISO approval and are reported to the Steering Committee.

6.1.3 An SLA breach without an approved exception is a control failure, escalated to the owning team's manager and recorded in the risk register (MJD-RSK-0001).

6.1.4 Active exploitation of an unpatched vulnerability is escalated immediately under the Incident Response Plan (MJD-SEC-0006).

6.1.5 Exception types and approval authorities:

| Exception type | Approval authority | Maximum duration |
|---|---|---|
| Patch not yet available (vendor delay) | SECURITY_ARCHITECT | 60 days; renewable once with CISO sign-off |
| Patch available but deployment would break production (compatibility) | SECURITY_ARCHITECT | 30 days; requires mitigation in place |
| EOL system with compensating controls (Section 4.6) | SECURITY_ARCHITECT | 12 months; CISO for renewals |
| Scanning tool cannot authenticate to asset (coverage gap) | SECURITY_ARCHITECT | 10 business days maximum; no renewals |
| RESTRICTED system or CDE exception | CISO | 30 days; reported to Board Risk Committee |
| Critical KEV-listed with no patch or interim mitigation available | CISO + Board Risk Committee notification | 7 days; mandatory incident management |

## 7. Worked Example: Critical KEV-Listed Vulnerability

The following example walks through the full remediation lifecycle for a Critical KEV-listed vulnerability to illustrate the application of this standard.

**Scenario:** CVE-XXXX-99999 is published with a CVSS v3.1 base score of 9.8 (Critical). CISA adds it to the KEV catalog the same day, indicating confirmed active exploitation. The vulnerability is a remote code execution flaw in the JSON parsing library used by MJD's internet-facing customer API service.

**Step 1: Detection (T+0).** The continuous software composition analysis scan running against the container registry detects CVE-XXXX-99999 in the deployed image for the customer API service at 08:14 UTC. The scanner creates a finding in the tracking system with the following attributes: CVE-XXXX-99999, CVSS 9.8 Critical, KEV-listed, internet-facing asset (escalator applies), Tier 1 business criticality. Effective severity: Critical. Effective SLA: 24 hours (KEV path). SLA expiry: 08:14 UTC the following day.

**Step 2: Automated alert (T+0).** The tracking system immediately sends notifications to the owning engineer, team lead, and security operations, flagging this as a KEV-listed Critical with a 24-hour SLA.

**Step 3: Triage (T+1 hour).** Security operations validates the finding: the deployed image version is confirmed to use the vulnerable library version. The finding is confirmed, not a false positive. The SECURITY_ARCHITECT is notified.

**Step 4: Interim virtual patch (T+2 hours).** While the patch is being prepared, the security operations team works with the network team to deploy a virtual patch: a WAF rule blocking the malformed JSON payloads identified in the CVE proof-of-concept, implemented as an emergency network change per MJD-SEC-0004. This reduces exploitability during the patching window and is documented in the finding record as the interim mitigation. The finding remains open; the SLA clock continues.

**Step 5: Patch preparation (T+4 hours).** The owning engineer updates the JSON parsing library to the patched version, rebuilds the container image, and runs the automated test suite in staging. Tests pass. The engineer initiates an emergency change request per MJD-TEC-0008, approved by the change manager and SECURITY_ARCHITECT.

**Step 6: Patch deployment (T+6 hours).** The patched image is deployed to production using the progressive rollout mechanism (canary deployment). Health checks pass. Full rollout completes at T+7 hours.

**Step 7: Confirming scan (T+8 hours).** The registry scanner runs against the newly deployed image digest. CVE-XXXX-99999 is not detected. Security operations closes the finding in the tracking system with the confirming scan result as evidence. The finding is marked "closed" at T+8 hours, well within the 24-hour SLA. No exception is filed.

**Step 8: WAF rule review (T+10 hours).** With the patch confirmed, the team assesses whether the interim WAF rule should remain in place as a defense-in-depth measure. The decision (retain or remove) is documented in the change record. In this case, the rule is retained as an additional layer.

**Outcome:** Critical KEV-listed vulnerability remediated in 8 hours against a 24-hour SLA. SLA conformance maintained. No exception required. Incident Response Plan not activated because the vulnerability was patched before confirmed exploitation of this specific instance.

## 8. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent control-effectiveness and metrics requirements)
- MJD-SEC-0006 Incident Response Plan (the emergency path for actively exploited vulnerabilities)
- MJD-TEC-0005 CI/CD Pipeline Standard (the build-time scanning and deployment gates of Sections 1.1 and 4.1)
- MJD-TEC-0008 Change Management and Release Policy (the change process for patch deployment)
- MJD-SEC-0007 Threat Modeling Standard (the prioritization context for which vulnerabilities matter most)
- MJD-SEC-0009 Logging, Monitoring, and SIEM Standard (the SLA-conformance and scan telemetry)

## 9. Regulatory References

- PCI DSS 4.0 Requirement 6: develop and maintain secure systems and software (patching, secure coding).
- PCI DSS 4.0 Requirement 11: regularly test security of systems and networks (scanning, penetration testing).
- NIST SP 800-40 Rev 4: guide to enterprise patch management planning.
- NIST SP 800-53 Rev 5 (RA, SI families): risk assessment and system/information integrity controls.
- FFIEC Information Security Booklet: vulnerability and patch management expectations.
- CISA BOD 22-01: Known Exploited Vulnerabilities catalog and remediation directive.

## 10. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-03-05 | SECURITY_ARCHITECT | Initial vulnerability and patch standard. |
| 2.0.0 | 2022-08-19 | SECURITY_ARCHITECT | Adopted CVSS severity model and SLA table. |
| 3.0.0 | 2024-01-14 | SECURITY_ARCHITECT | Added KEV escalator and internet-facing escalator. |
| 3.1.0 | 2025-05-27 | SECURITY_ARCHITECT | Tightened Critical SLA to 7 days; 24h for KEV. |
| 3.2.0 | 2026-01-25 | SECURITY_ARCHITECT | Annual review; added RESTRICTED-system escalator and verified-closure rule. |
