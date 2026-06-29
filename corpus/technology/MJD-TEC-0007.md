---
doc_id: MJD-TEC-0007
title: Cloud Governance and Landing Zone Policy
department: TECHNOLOGY
doc_type: POLICY
classification: INTERNAL
owner_role: Head of Platform Engineering
allowed_roles: [SOFTWARE_ENGINEER, SECURITY_ARCHITECT, RISK_ANALYST]
effective_date: 2026-03-01
version: 2.2.0
review_cycle_months: 12
regulatory_refs: ["FFIEC Outsourcing Technology Services Booklet", "NIST SP 800-53 Rev 5 (AC, CM, SC families)", "PCI DSS 4.0 Requirement 1", "OCC 2013-29 Third-Party Relationships"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Cloud Governance and Landing Zone Policy

## Purpose and Scope

This policy establishes how Meridian John Doe Financial governs its use of public cloud: the account and project structure, the mandatory baseline controls every workload inherits, the network architecture, the cost and tagging discipline, and the division of security responsibility with cloud providers. The mechanism is the landing zone, a pre-governed account baseline into which all workloads deploy so that security, logging, and guardrails are present from the first resource rather than retrofitted. Risk Analysts are granted read access because cloud concentration, resilience, and third-party dependency are material enterprise risks they must assess.

This policy applies to all cloud accounts, subscriptions, and projects owned by Meridian J.D. and to every workload deployed into them. It is binding on Technology and Platform Engineering and is read by the Risk function for oversight under the Enterprise Risk Management Framework (MJD-RSK-0001). Meridian J.D. is a synthetic entity; every account number, region name, control identifier, and recovery target in this document is fabricated for demonstration and must not be read as describing a real institution.

The policy governs commercial public cloud only. On-premises data centers, colocation footprints, and software-as-a-service products purchased by business units are out of scope here, though the third-party oversight principles in section 11 are consistent with how those relationships are managed elsewhere.

## Definitions

**Landing zone.** A governed cloud account or project baseline with mandatory controls, network plumbing, logging, and guardrails pre-applied, into which workloads deploy.

**Organization hierarchy.** The tree of management accounts, organizational units, and workload accounts that structures the cloud estate and applies policy at scale.

**Service control policy (guardrail).** An organization-level restriction that no workload account can override, for example forbidding the disabling of audit logging.

**Shared responsibility.** The division of security duties between the cloud provider (security of the cloud) and Meridian J.D. (security in the cloud).

**Account vending.** The automated, governed process that issues a new landing-zone-compliant account on request.

**Organizational unit (OU).** A grouping node in the organization hierarchy to which guardrails are attached so that policy is inherited by every account beneath it.

**Drift.** Any divergence of an account's live configuration from its declared baseline, whether introduced by manual change, by a defective deployment, or by an attacker.

## 1. Cloud Operating Model

1.1 The cloud estate is organized into an account hierarchy with environment and sensitivity separation: production workloads, non-production workloads, security tooling, logging, and shared services live in separate accounts.

1.2 Production and non-production are strongly isolated. A non-production account never has a network path or credential path to production data. This is a structural property of the hierarchy, not a runtime check: the absence of any peering, trust relationship, or shared key between the two estates is what guarantees it.

1.3 New accounts are issued only through automated account vending; manually created ungoverned accounts are prohibited and are flagged by continuous compliance scanning.

1.4 The account is the unit of blast-radius containment. A compromise, a runaway cost event, or a faulty deployment is bounded by the account it occurs in, which is why workloads of different sensitivity and different lifecycle stages are never co-located in one account.

## 2. Organization and Account Hierarchy

2.1 The hierarchy applies controls at the highest node where they are universally true, so that a workload account inherits its security posture rather than declaring it. The table below describes the structure and the controls bound at each node.

| Node | Purpose | Controls applied |
|---|---|---|
| Organization root | Top of the tree; holds the management account | Org-wide guardrails: deny leaving the org, deny disabling logging, deny root usage, region allowlist |
| Security OU | Security tooling, compliance scanning, threat detection | Restricted human access; read access to all accounts for monitoring; no workloads |
| Logging OU | Central append-only logging account and log archive | Write-once log delivery; no interactive access except break-glass; immutable retention |
| Infrastructure OU | Shared services: networking hub, DNS, identity, golden images | Change only via pipeline; no direct human mutation |
| Workloads OU (prod) | Production workloads | Full baseline; strictest data-classification guardrails; change-controlled |
| Workloads OU (non-prod) | Development, test, staging | Full baseline; Confidential/Restricted data prohibited; no path to prod |
| Sandbox OU | Time-boxed experimentation | Hard spend cap; auto-expiry; no production data; isolated network |
| Suspended OU | Decommissioned or quarantined accounts | All access revoked; resources frozen pending deletion or forensic review |

2.2 The management account at the organization root runs no workloads. It exists only to administer the organization, attach guardrails, and operate account vending, and human access to it is held under the Privileged Access Management Policy (MJD-SEC-0010) as a break-glass path.

2.3 An account is moved to the Suspended OU when it is decommissioned or when continuous compliance scanning detects it is ungoverned or has been compromised. Suspension severs access immediately while preserving state for the Risk function and for incident responders.

## 3. Service Control Policies and Guardrails

3.1 Guardrails are preventive controls expressed at the organization or OU level that no workload account can override. They are the floor beneath the landing zone: even an account owner with broad in-account permissions cannot escape them.

| Guardrail | Effect |
|---|---|
| Deny disabling logging | Blocks any action that would turn off or redirect org-wide audit logging |
| Deny public storage | Blocks making object storage or snapshots publicly readable or writable |
| Region allowlist | Denies resource creation outside approved regions |
| Deny root usage | Blocks day-to-day use of the root or owner principal except vaulted break-glass |
| Deny unencrypted resources | Blocks creation of storage, volumes, or databases without KMS encryption at rest |
| Deny leaving the organization | Blocks an account from detaching itself from central governance |

3.2 Guardrails are deny-by-default for the actions they cover. A workload that needs a capability a guardrail blocks does not get the guardrail relaxed; it gets an architecture review, and in the rare sanctioned case a scoped exception under section 12, never a removal of the org-wide control.

3.3 The guardrail catalog is versioned and provisioned as code alongside the landing zone, consistent with the Infrastructure as Code Standard (MJD-TEC-0006). A change to the catalog is itself a change-controlled deployment, reviewed by a Security Architect.

## 4. Mandatory Baseline Controls (Landing Zone)

4.1 Every landing-zone account inherits, non-negotiably, the following baseline. These are enforced by organization-level guardrails that workload accounts cannot disable.

| Control | Requirement |
|---|---|
| Audit logging | Organization-wide audit logging enabled and delivered to a central, append-only logging account |
| Network flow logs | Enabled on all networks |
| Encryption | KMS encryption at rest enforced; provider default keys replaced with managed keys |
| Identity | Centralized identity federation; no local long-lived users for humans |
| Guardrails | Public-storage prohibition, region restriction, root-account protection, mandatory tagging |
| Baseline network | Private-by-default networking with controlled egress |
| Configuration recording | Continuous configuration and compliance recording enabled |

4.2 The baseline aligns with the Infrastructure as Code Standard (MJD-TEC-0006) guardrails; the landing zone is itself provisioned as code. Because the baseline is code, every account is identical by construction, and any divergence is drift that the compliance scanner detects in section 9.

4.3 The baseline is inherited, not opt-in. A team requesting an account does not assemble these controls; they receive them already applied at handover, which is the point of the landing-zone model.

## 5. Account Vending

5.1 Account vending is the only sanctioned way to create an account. It is automated end to end so that no account exists without the baseline, and so that there is an auditable record of who requested what and why. The procedure is:

1. **Request.** The requesting team submits an account request specifying intended environment (prod, non-prod, sandbox), owning team, cost-center, expected data classification, and business justification.
2. **Approval.** The request is approved by the owning team's engineering lead and, for production or for any account expected to hold Confidential or Restricted data, by a Security Architect.
3. **Automated baseline apply.** The vending pipeline creates the account, places it under the correct OU, and applies the full landing-zone baseline and guardrails as code.
4. **Security validation.** Continuous compliance scanning runs an initial evaluation against the baseline and the guardrail catalog; the account is not handed over while any baseline control is failing.
5. **Handover.** The account is delivered to the owning team with its mandatory tags populated, its federation roles wired, and its budgets and anomaly alerts configured.

5.2 A vended account arrives with the following pre-applied inventory: org-wide audit logging delivery, network flow logs, a private-by-default network attached to the hub, KMS keys for encryption at rest, federated permission sets in place of local users, continuous configuration recording, the four mandatory tags, and account budgets with anomaly alerting.

5.3 Sandbox accounts are vended with a hard spend cap and an automatic expiry date. They carry the same guardrails as any other account, including the prohibition on production data, so experimentation never becomes an ungoverned back door.

## 6. Network Architecture

6.1 Networks are private by default. Internet ingress terminates only at sanctioned, security-reviewed edge points (API gateways, load balancers) consistent with the Public and Internal API Standard (MJD-TEC-0002).

6.2 Connectivity follows a hub-and-spoke topology. A central network hub in the Infrastructure OU provides shared connectivity, inspection, and routing; workload accounts attach as spokes. Spokes do not peer directly with one another, so a compromise in one spoke does not yield lateral reach to its neighbors.

6.3 Egress to the internet is controlled and inspected; workloads do not have unrestricted outbound access. Outbound traffic is routed through the hub's egress inspection layer, where it is filtered against an allowlist of approved destinations. Unexplained egress is both a control failure and a potential exfiltration signal.

6.4 Connectivity between accounts and to on-premises is through reviewed, least-privilege private connectivity, never broad peering. There is no transitive trust: an account reachable from the hub does not become reachable from every other spoke.

6.5 DNS is centralized through the hub so that name resolution is consistent, logged, and resolvable to private endpoints without traversing the public internet. DNS query logs feed the same central logging account as the rest of the estate.

6.6 Network segmentation aligns with the security network architecture standards and with PCI DSS 4.0 Requirement 1. Any new edge exposure is reviewed by a Security Architect before it is allowed to terminate internet traffic, per MJD-TEC-0002.

## 7. Identity and Access in the Cloud

7.1 Human access to cloud accounts is exclusively through centralized identity federation with MFA. No account has standing local privileged users, and no human holds a long-lived cloud credential.

7.2 Access is granted through permission sets mapped to job function, not through per-person policies. A permission set is assigned to a federated group, the user's membership in that group is governed by the joiner-mover-leaver process, and entitlement therefore follows role and is revoked automatically when the role ends.

7.3 There are no standing privileged users. Elevated access in any account is obtained just-in-time, time-boxed, and logged, consistent with the Privileged Access Management Policy (MJD-SEC-0010). Standing administrative entitlement is itself a finding.

7.4 Workloads use short-lived workload identity (MJD-TEC-0005), never long-lived embedded cloud keys. Any long-lived cloud key is a finding and is subject to the 90-day service-account rotation interval of the Secrets and Key Management Policy (MJD-TEC-0004) as an interim control until it is eliminated.

7.5 Root and break-glass credentials are vaulted, MFA-protected, and alarmed on use, and are governed by MJD-SEC-0010. The break-glass procedure is: the credential is retrieved from the vault under dual control, its use raises an immediate alarm to the Security Architect on call, every action taken is logged to the central logging account, and the session is reviewed after the fact with the credential re-vaulted and rotated. Break-glass is for the failure of federation itself, not for routine administration.

## 8. Region, Residency, and Resilience

8.1 Workloads deploy only into approved regions. Region restriction is enforced by guardrail to control data residency and to keep regulated data within approved jurisdictions. The mapping of data classification to permitted region is:

| Data classification | Permitted regions |
|---|---|
| Public | Any approved region |
| Internal | Approved regions within sanctioned jurisdictions |
| Confidential | Primary in-jurisdiction region plus one approved in-jurisdiction recovery region |
| Restricted | Primary in-jurisdiction region only, with in-jurisdiction recovery; no cross-jurisdiction replication |

8.2 The region allowlist is the enforcement surface for residency. Because it is a guardrail, a workload cannot create a resource outside an approved region even by mistake, and cross-region movement of regulated data is constrained by the same control rather than by convention.

8.3 Critical workloads are designed for resilience across availability zones, and tier-1 workloads have a tested cross-region recovery capability. Recovery targets are:

| Workload tier | RTO target | RPO target | DR test cadence |
|---|---|---|---|
| Tier 1 (critical) | 1 hour | 5 minutes | Cross-region failover tested semi-annually |
| Tier 2 (important) | 4 hours | 1 hour | Recovery tested annually |
| Tier 3 (standard) | 24 hours | 24 hours | Restore validated annually |

8.4 Disaster-recovery tests are scheduled, evidenced, and their results retained for the Risk function. A failed or skipped DR test for a tier-1 workload is an operational risk event reported under the Operational Risk Procedure (MJD-RSK-0003).

8.5 Cloud concentration risk (over-reliance on a single provider or region) is reported to the Risk function for inclusion in the enterprise risk register (MJD-RSK-0001).

## 9. Continuous Compliance and Remediation

9.1 Continuous compliance scanning evaluates every account against the baseline and the guardrails. Configuration recording captures the live state continuously, and the scanner compares that state to the declared baseline so that drift is detected close to when it occurs rather than at audit time.

9.2 Deviations raise findings with remediation SLAs aligned to the severity model in MJD-TEC-0001 section 6. A critical finding, such as disabled audit logging or regulated data outside an approved region, carries the shortest SLA and is treated as an incident under section 12.

9.3 A workload account that drifts out of baseline is automatically remediated where the remediation is safe and deterministic. For example, an object store that becomes publicly readable is re-secured automatically; audit logging that is disabled is re-enabled automatically. Where automated remediation is unsafe, the finding is escalated to the owning team and the Security Architect.

9.4 Findings that cannot be remediated within SLA are recorded in an exception register with an owner, a compensating control, and an expiry date. The register is reviewed by a Security Architect, and entries affecting concentration or residency are surfaced to the Risk function.

9.5 Compliance scan results are summarized for the Risk function on a recurring basis so that cloud control posture is visible at the enterprise level, not only inside engineering, supporting the oversight role the Risk Analyst holds under this policy.

## 10. Data Protection in the Cloud

10.1 All regulated data stored in the cloud is encrypted at rest with KMS-managed keys and classified per the Data Classification and Handling Standard (MJD-SEC-0008). The data-classification tag required in section 13 drives automated controls: more sensitive classifications attract stricter network and access guardrails and a narrower region allowlist per section 8.1.

10.2 Confidential and Restricted data never lands in a non-production account. Copying production data into a lower environment is prohibited; lower environments use synthetic or masked data, consistent with the Infrastructure as Code Standard (MJD-TEC-0006 section 7.3). The structural isolation in section 1.2 makes this enforceable: a non-prod account has no path to production data to copy in the first place.

10.3 Cross-account and cross-region data movement of regulated data is logged and is constrained by the region restriction in section 8.1, so residency obligations are enforced by control rather than by convention.

10.4 Backups of regulated data are encrypted, access-controlled, and stored in approved regions. Backup and recovery capability is tested as part of the resilience requirements in section 8.3.

10.5 Encryption keys are managed under the Secrets and Key Management Policy (MJD-TEC-0004). Provider default keys are replaced with managed keys at vending, and key access is itself logged to the central logging account.

## 11. Shared Responsibility and Cloud Concentration Risk

11.1 The bank documents, per service consumed, which controls the provider owns and which Meridian J.D. owns. Provider-owned controls are evidenced through the provider's attestations, for example SOC 2 Type II and ISO 27001 reports, which are reviewed by the Risk function on a recurring basis.

11.2 Cloud providers are material third parties governed by the bank's third-party risk program; their use is subject to ongoing oversight consistent with OCC Bulletin 2013-29 third-party guidance.

11.3 For the Risk function, cloud concentration is tracked through metrics including the share of tier-1 workloads on a single provider, the share of regulated data in a single region, and the recovery dependence of critical services on a single provider's services. These metrics feed the enterprise risk register (MJD-RSK-0001) and are reviewed against the institution's risk appetite.

11.4 An exit strategy is maintained for the primary cloud provider so that concentration does not become lock-in. The strategy identifies which workloads are portable, the recovery posture if a provider relationship must be wound down, and the data egress and re-platforming path. The exit strategy is reviewed by the Risk function and is a standing input to the concentration assessment, because a third party the bank cannot leave is a third party the bank cannot fully govern.

11.5 Provider attestation gaps, adverse audit findings, or service degradations that affect resilience are escalated to the Risk function and assessed under the Operational Risk Procedure (MJD-RSK-0003).

## 12. Cost Governance and Tagging

12.1 Every resource carries mandatory tags: owner, environment, data-classification, and cost-center. Untagged resources are flagged by the compliance scanner and may be quarantined; a resource that cannot be attributed to an owner, an environment, a classification, and a cost-center is by definition ungoverned.

12.2 Budgets and anomaly alerts are configured per account at vending. Sustained anomalous spend is investigated as both a cost and a potential security signal, for example cryptomining from a compromised workload, and a spike that coincides with anomalous egress under section 6.3 is treated as a possible compromise.

12.3 The data-classification tag is load-bearing beyond cost: it drives the automated controls in section 10.1 and the region mapping in section 8.1. For this reason an incorrect or missing classification tag is a security finding, not merely a cost-attribution gap.

## 13. Roles and Responsibilities

**Software Engineer.** Deploys workloads only into landing-zone accounts, honors guardrails, uses short-lived workload identity rather than long-lived keys, applies the four mandatory tags correctly, and remediates findings on owned accounts within SLA.

**Security Architect.** Owns the guardrail and baseline control set, approves account requests for production and for sensitive data, reviews edge-network exposure and break-glass usage, owns the cloud threat model, and reviews the exception register.

**Risk Analyst.** Assesses cloud concentration, residency, and resilience risk; reviews provider attestations such as SOC 2 and ISO 27001 reports; tracks the concentration metrics in section 11.3 against risk appetite; reviews the exit strategy and DR test outcomes; consumes the recurring compliance summaries in section 9.5; and maintains the related entries in the enterprise risk register (MJD-RSK-0001), escalating residency or concentration breaches under the Operational Risk Procedure (MJD-RSK-0003).

**Platform Engineering.** Operates account vending, the landing zone, the network hub, and the compliance-scanning tooling, and executes safe automated remediation.

**Head of Platform Engineering.** Owner of this policy, accountable for a governed, compliant cloud estate.

## 14. Exceptions and Escalation

14.1 No exception is granted to: organization-wide audit logging, the public-storage prohibition, region restriction for regulated data, or centralized human identity federation. These are non-waivable guardrails.

14.2 Other deviations require an exception approved by a Security Architect and the Head of Platform Engineering, recorded in the exception register with a compensating control and an expiry date, with Risk notified when the deviation affects concentration or residency.

14.3 An ungoverned account, disabled audit logging, or regulated data found outside an approved region is a security and compliance incident escalated under the Incident Response Plan (MJD-SEC-0006).

## 15. Related Documents

- MJD-TEC-0002, Public and Internal API Standard
- MJD-TEC-0004, Secrets and Key Management Policy
- MJD-TEC-0005, CI/CD Pipeline Standard
- MJD-TEC-0006, Infrastructure as Code Standard
- MJD-SEC-0008, Data Classification and Handling Standard
- MJD-SEC-0010, Privileged Access Management (PAM) Policy
- MJD-RSK-0001, Enterprise Risk Management Framework
- MJD-RSK-0003, Operational Risk Procedure

## 16. Regulatory References

- FFIEC IT Examination Handbook, Outsourcing Technology Services Booklet
- NIST SP 800-53 Rev 5, Access Control, Configuration Management, and System and Communications Protection families
- PCI DSS 4.0, Requirement 1 (Network Security Controls)
- OCC Bulletin 2013-29, Third-Party Relationships: Risk Management Guidance

## 17. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2023-01-19 | Platform Engineering | Initial cloud governance and landing zone policy. |
| 2.0.0 | 2024-05-08 | Platform Engineering | Added organization guardrails and account-vending mandate. |
| 2.1.0 | 2025-07-23 | Platform Engineering | Added region restriction and cloud concentration risk reporting. |
| 2.2.0 | 2026-03-01 | Platform Engineering | Granted Risk read access; tightened workload-identity requirement. |
