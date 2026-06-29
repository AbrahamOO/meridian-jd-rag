---
doc_id: MJD-SEC-0010
title: Privileged Access Management (PAM) Policy
department: SECURITY
doc_type: POLICY
classification: RESTRICTED
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT]
effective_date: 2026-02-15
version: 3.0.0
review_cycle_months: 12
regulatory_refs: ["NIST SP 800-53 Rev 5 (AC-2, AC-6 enhancements)", "PCI DSS 4.0 Requirement 7", "PCI DSS 4.0 Requirement 8", "GLBA Safeguards Rule (16 CFR Part 314)", "NYDFS 23 NYCRR 500.7", "SOC 2 CC6"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Privileged Access Management (PAM) Policy

## Purpose and Scope

This policy governs how Meridian John Doe Financial (Meridian J.D.) grants, controls, monitors, and revokes privileged access: the administrative, root, and other high-power entitlements that, if misused or compromised, would cause the greatest harm. Privileged access is the most dangerous access in the institution, so it is governed by the strictest controls: no standing privilege, just-in-time elevation, dual control for the most sensitive operations, full session recording, and rapid recertification.

This document is classified RESTRICTED and readable only by the SECURITY_ARCHITECT role. The privileged-access workflow (how elevation is requested, brokered, approved, and recorded, and where the break-glass paths are) is an operational secret: disclosing it hands an attacker the map to the bank's most powerful access. It is one of the three RESTRICTED security documents that form the sharpest access boundary in the corpus and is invisible to OPERATIONS_ANALYST, SOFTWARE_ENGINEER, and every other role. This is the headline access-control boundary: a SOFTWARE_ENGINEER asking how privileged access is granted receives a clean denial.

Scope covers all privileged accounts and entitlements across infrastructure, cloud, databases, applications, network devices, the HSM/KMS estate (MJD-SEC-0002), security tooling, and the SIEM (MJD-SEC-0009), for both human and machine identities.

## Definitions

**Privileged access.** Access that exceeds that of a standard user, including administrative, root, superuser, and any access that can alter security controls or read RESTRICTED data.

**Just-in-time (JIT) elevation.** Granting privileged access only for the duration of a specific, approved task, then automatically revoking it.

**Standing privilege.** Persistent privileged access held continuously; prohibited by this policy.

**PAM broker.** The system that mediates all privileged sessions, injecting credentials and recording the session.

**Dual control.** A requirement that two authorized people act together to perform a sensitive operation.

**Break-glass.** An emergency access path used only when normal privileged paths fail.

**Session recording.** A full keystroke and screen capture of a privileged session for audit.

**Credential vaulting.** Storing privileged credentials in a vault so they are never known to or held by the user.

**Workload identity.** A cryptographically verifiable identity assigned to a machine, pipeline, or service, distinct from any human identity, used in place of static credentials for automated processes.

**Eligibility.** The pre-approved entitlement to request JIT elevation for a specific resource, granted through the recertification process and held by a named individual. Eligibility is not access; it is the right to request access through the broker.

## 1. Core Principles

### 1.1 No Standing Privilege

1.1.1 Standing privileged access is prohibited. All privileged access is just-in-time: requested for a specific task, time-boxed, approved, used through the broker, and automatically revoked at expiry.

1.1.2 The default maximum elevation duration is 4 hours; durations beyond 4 hours require explicit per-request approval and never exceed 24 hours.

### 1.2 Least Privilege

1.2.1 Privileged entitlements are scoped to the minimum required for the task. Broad "admin everything" roles are prohibited; entitlements are granular and resource-scoped.

### 1.3 Credential Vaulting

1.3.1 Privileged credentials are vaulted: users never see or hold them. The PAM broker injects credentials into the session. Vaulted credentials are rotated automatically after each use and on the schedule in MJD-SEC-0002 Section 5.2.

### 1.4 Accountability

1.4.1 Shared privileged accounts are prohibited where individual accountability is feasible. Every privileged action is attributable to a named individual through the broker.

### 1.5 Privileged Account Inventory

1.5.1 All privileged accounts, both human and machine, are catalogued in the PAM inventory. The inventory is the authoritative record of what privileged accounts exist and is reconciled monthly against the actual account state in every target system. Accounts present in a target system but absent from the inventory are orphaned accounts and are disabled immediately pending investigation.

1.5.2 Each inventory record contains: the account identifier; the account type (human JIT eligibility, machine workload identity, break-glass, service account); the named owner (for human accounts, the individual; for machine accounts, the owning team); the target resource or resource class the account has eligibility for; the date the account was created; the date of the last JIT elevation or last use; the eligibility expiry date (the next recertification deadline); and any compensating controls in effect (for accounts that cannot integrate the broker, per Section 7).

1.5.3 Monthly reconciliation compares the PAM inventory against live account enumerations from: cloud IAM APIs (AWS IAM, Azure AD, GCP IAM); on-premises Active Directory privileged groups; database privileged user tables; and network device local account stores. Discrepancies are investigated within 2 business days. An account with elevated permissions found in a target system but not in the inventory is immediately revoked and reported to the SECURITY_ARCHITECT.

1.5.4 The inventory is reviewed in full by the SECURITY_ARCHITECT quarterly. The quarterly review produces a summary of: total privileged account count by type; accounts that have not been used in 90 days (candidates for deprovisioning); accounts with eligibility expiring in the next 30 days (upcoming recertification); and any open reconciliation discrepancies.

## 2. The Elevation Workflow

### 2.1 Request and Approval

2.1.1 A user requests elevation for a named resource, a stated reason, and a duration. The request is approved by an authorized approver who is not the requester (separation of duties).

2.1.2 Elevation to the most sensitive targets (HSM/KMS key operations, the SIEM, the PAM broker itself, RESTRICTED data stores) requires dual control: two distinct approvers and, for key ceremonies, two operators (MJD-SEC-0002 Section 4.2).

2.1.3 Approvals and denials are logged to the SIEM (MJD-SEC-0009). An unknown or ineligible requester is denied (fail closed).

### 2.2 Brokered Session

2.2.1 All privileged sessions run through the PAM broker via the management zone bastion (MJD-SEC-0004 Z5). There is no direct administrative path from a workstation to production.

2.2.2 Privileged sessions require phishing-resistant MFA (FIDO2) at initiation and re-authentication for the most sensitive operations (MJD-SEC-0003 Section 2.2).

2.2.3 Every privileged session is fully recorded (keystroke and screen). Recordings are stored tamper-evidently and retained for 7 years.

### 2.3 Automatic Revocation

2.3.1 Elevation is revoked automatically at expiry. Credentials used during the session are rotated. No privilege persists after the task window.

### 2.4 Approval Escalation by Target

2.4.1 The number of approvers required, the approval window, and the notification targets vary by target sensitivity. The following table is binding; no deviation is permitted without a policy exception (Section 7).

| Target type | Approvers required | Approval window | Notification targets |
|---|---|---|---|
| HSM or KMS (key operations) | Two distinct approvers (dual control) plus SECURITY_ARCHITECT notification | 60 minutes (emergency: 20 minutes) | SECURITY_ARCHITECT, SOC, CISO for any key ceremony |
| SIEM and log platform | Two distinct approvers | 30 minutes (emergency: 15 minutes) | SECURITY_ARCHITECT, SOC lead |
| PAM broker and vault | Two distinct approvers; one must be SECURITY_ARCHITECT | 30 minutes | CISO |
| RESTRICTED data store | Two distinct approvers; one must be SECURITY_ARCHITECT | 30 minutes (emergency: 15 minutes) | SECURITY_ARCHITECT, SOC |
| Production database (CONFIDENTIAL data) | One approver (resource owner or delegate) | 30 minutes (standard); 15 minutes (emergency) | SOC |
| Network infrastructure (firewall, routing) | One approver (network team lead or SECURITY_ARCHITECT) | 30 minutes (standard); 15 minutes (emergency) | SOC |
| Standard production system | One approver (resource owner) | 60 minutes (standard) | None required beyond logging |

### 2.5 Time-to-Approve SLAs

2.5.1 Standard elevation (non-emergency): approvers must respond to an elevation request within 30 minutes during business hours (08:00 to 18:00 local time, Monday through Friday excluding holidays). Requests submitted outside business hours for non-emergency elevation are queued for the next business day unless the requester designates the request as emergency.

2.5.2 Emergency elevation (24x7): approvers must respond to an emergency elevation request within 15 minutes at any time of day or night. Emergency designations are limited to situations where a delay would result in a material operational or security impact; misuse of the emergency designation is a policy violation.

2.5.3 If the primary approver does not respond within the SLA, the PAM broker automatically escalates to the secondary approver (the named backup in the resource's approver configuration). If neither primary nor secondary approver responds, the broker escalates to the SECURITY_ARCHITECT. For HSM/KMS and PAM broker targets, the SECURITY_ARCHITECT is the final escalation authority and cannot be bypassed.

2.5.4 An elevation request that has not been approved or denied within 2 hours is automatically expired by the broker. The requester must re-submit. Expired requests are logged and, if they represent a pattern of approver non-responsiveness, are reported to the SECURITY_ARCHITECT for recertification review.

### 2.6 Session Monitoring During Elevation

2.6.1 The PAM broker monitors all privileged sessions in real time using behavioral analytics. The following patterns trigger a real-time alert to the SOC, which may result in session termination by the SOC lead at their discretion:

- Command injection patterns: execution of commands known to be associated with privilege escalation, lateral movement, or data exfiltration (for example, bulk data export commands, account enumeration, disabling audit logging).
- Data exfiltration indicators: transfer of large volumes of data to an external destination, copying RESTRICTED or CONFIDENTIAL data to a removable medium or unapproved location, or compressing large directory trees.
- Unusual process launches: execution of processes not in the approved baseline for the target system, particularly network scanning tools, exploit frameworks, or scripting interpreters launched from an unusual parent process.
- Off-hours access: a privileged session initiated outside the requester's normal working hours for a target system that does not typically require after-hours access. This is a soft alert (SOC review) rather than an automatic termination.

2.6.2 Real-time alert thresholds are calibrated per target system based on the system's normal administrative command profile, established during a 30-day baselining period when the system is first onboarded to the broker. Thresholds are reviewed and updated quarterly or after any material change to the system's administrative workflow.

2.6.3 Session termination is a significant action that may disrupt an authorized task. The SOC lead uses judgment and attempts to contact the session user before terminating, except in cases of clearly malicious activity (confirmed data exfiltration, confirmed disable-audit-log command) where immediate termination is warranted. All termination decisions are logged and reviewed by the SECURITY_ARCHITECT within 24 hours.

## 3. Break-Glass Access

3.1.1 Break-glass accounts exist only for emergencies where the normal elevation path is unavailable (for example, the PAM broker itself is down during a SEV-1 incident).

3.1.2 Break-glass credentials are vaulted, split-knowledge, and require dual control to retrieve. Their use triggers an immediate high-severity alert to the CISO and the SOC.

3.1.3 Every break-glass use is reviewed within 24 hours; an unjustified use is a control failure escalated under the Incident Response Plan (MJD-SEC-0006).

### 3.4 Break-Glass Credential Rotation Schedule

3.4.1 Break-glass credentials are rotated quarterly on a fixed schedule, regardless of whether they have been used. The rotation schedule is maintained by the SECURITY_ARCHITECT and is not disclosed outside the SECURITY_ARCHITECT and the PAM administrators who execute the rotation.

3.4.2 Rotation is performed under dual control: two PAM administrators execute the rotation together, each witnessing the other's actions. Neither PAM administrator has sole access to the new credential; the new credential is split across two vaulted components, each held by a distinct custodian, consistent with the split-knowledge requirement in Section 3.1.2.

3.4.3 After rotation, the new credential components are vaulted in separate, access-controlled vault paths. Access to either vault path requires SECURITY_ARCHITECT authorization and generates an alert to the CISO. The rotation event is logged to the SIEM (MJD-SEC-0009) with the rotation timestamp, the identities of both PAM administrators, and the target account identifier (but not the credential itself).

3.4.4 Ad-hoc rotation (outside the quarterly schedule) is performed immediately following any break-glass use, any suspected compromise of the vault storing the credential components, or any departure from the institution of a PAM administrator who was a credential custodian. Ad-hoc rotation follows the same dual-control procedure as scheduled rotation.

### 3.5 Break-Glass Audit Procedure

3.5.1 Every break-glass use must be reviewed within 24 hours of the use event. The review is conducted by the SECURITY_ARCHITECT and produces a written finding documenting: the identity of the individual who retrieved and used the break-glass credential; the timestamp of retrieval and the timestamp of use; the stated justification for use; the actions taken during the break-glass session (drawn from the session recording); and a determination of whether the use was justified (emergency use when the broker was unavailable) or unjustified (convenience use, or use when the broker was available).

3.5.2 A justified break-glass use is documented in the incident record for the triggering event and is closed after the review. The SECURITY_ARCHITECT determines whether the broker outage that precipitated the use requires a root-cause investigation and remediation.

3.5.3 An unjustified break-glass use is a control failure. It is escalated as a potential security incident under the Incident Response Plan (MJD-SEC-0006), recorded in the risk register (MJD-RSK-0001), and results in revocation of the responsible individual's break-glass eligibility. The CISO and, for SEV-1 determinations, the Board Risk Committee are notified.

## 4. Machine and Cloud Privilege

4.1.1 Privileged machine identities (deployment pipelines, automation) use short-lived, vaulted credentials or workload identity, never long-lived static keys (MJD-TEC-0004, MJD-SEC-0002 Section 5.2).

4.1.2 Cloud administrative roles follow the same JIT model: elevation is brokered, time-boxed, and recorded; permanent cloud admin assignments are prohibited.

4.1.3 The most powerful cloud roles (organization administrator, billing administrator, security-tooling administrator) require dual control and generate a high-severity alert on every elevation. No single identity, human or machine, holds standing organization-administrator rights.

### 4.2 Scope of Privileged Operations

4.2.1 Operations classified as privileged include, at minimum: creating or modifying accounts and entitlements; reading or exporting CONFIDENTIAL or RESTRICTED data in bulk; changing security controls (firewall rules, detection rules, encryption settings); accessing the HSM, KMS, or secrets vault; modifying audit logs or their retention; and deploying to production outside the standard pipeline.

4.2.2 Any operation that can disable, weaken, or evade a security control is privileged by definition and is brokered, recorded, and alerted regardless of which system it touches.

### 4.3 Monitoring Privileged Sessions

4.3.1 Privileged session recordings are reviewed on a risk-based sample and in full after any anomaly. The act of viewing a recording is itself privileged and logged.

4.3.2 Real-time behavioral analytics on privileged sessions flag deviations (unusual commands, off-hours elevation, bulk data access) to the SOC for immediate review (MJD-SEC-0009).

### 4.4 Deployment Pipeline Privilege Controls

4.4.1 CI/CD pipelines (MJD-TEC-0005) must not use static long-lived credentials for any privileged operation. All pipeline privilege is granted through short-lived workload identity tokens issued by the cloud provider's workload identity federation mechanism, or through the PAM vault's dynamic secret feature, which issues a credential valid only for the duration of the pipeline run and automatically rotates after use.

4.4.2 Pipeline elevation is brokered through the PAM platform: the pipeline requests a short-lived credential for a specific target (for example, a deployment role in a production cloud account) by presenting its workload identity token. The PAM broker validates the request against the pipeline's registered entitlements, issues a time-limited credential (maximum 60-minute lifetime), and logs the issuance to the SIEM (MJD-SEC-0009).

4.4.3 Prohibited pipeline patterns: hardcoded credentials of any kind in pipeline configuration, Dockerfile, or source code; persistent deployment tokens stored as environment variables in the pipeline platform; and credentials shared across multiple pipelines (each pipeline has its own distinct workload identity). Secret scanning in the CI/CD pipeline (MJD-TEC-0005) detects and blocks hardcoded credential patterns before they reach the repository.

4.4.4 Pipeline deployments to production outside the standard change process (MJD-TEC-0008) are themselves a privileged operation. An out-of-process production deployment requires SECURITY_ARCHITECT approval and generates a high-severity alert to the SOC. This control prevents an attacker who compromises a pipeline from deploying arbitrary code to production without triggering a review.

## 5. Recertification

5.1.1 All privileged entitlements (the eligibility to request elevation) are recertified every 30 days by the resource owner and the SECURITY_ARCHITECT.

5.1.2 Eligibility that is not re-attested is removed automatically at the end of the window (fail closed).

5.1.3 Break-glass account inventory is reviewed monthly and credentials rotated quarterly even if unused.

### 5.4 Recertification Failure Response

5.4.1 The PAM platform sends automated reminders to resource owners at T-7 days and T-3 days before each recertification deadline, listing the specific entitlements pending recertification and the deadline date. Reminders are sent to the resource owner's corporate email and to the SECURITY_ARCHITECT as a visibility copy.

5.4.2 At T+0 (the deadline): any entitlement that has not been affirmatively re-attested by the resource owner is automatically revoked by the PAM platform (fail closed). The revocation is logged to the SIEM (MJD-SEC-0009) and the affected individual is notified. Automatic revocation does not require manual action by the SECURITY_ARCHITECT; the platform enforces it without exception.

5.4.3 Following automatic revocation, the resource owner may request reinstatement by submitting a new eligibility request through the standard access-request process. The reinstatement request is treated as a new access grant and must be approved by the SECURITY_ARCHITECT before eligibility is restored. Reinstatement within 5 business days of expiry does not require a full access review; beyond 5 business days, a full review is required.

5.4.4 Resource owners who fail to certify on time in two consecutive recertification cycles have their certifier authority suspended for 90 days. During this period, the SECURITY_ARCHITECT serves as the certifier for the affected resource, and the resource owner's manager is notified. Suspension of certifier authority is recorded in the risk register (MJD-RSK-0001) as a governance finding.

5.4.5 Systemic recertification failure (more than 10% of eligible entitlements failing to be recertified in a given cycle) is escalated to the CISO and reported to the Information Security Steering Committee (MJD-SEC-0001). It indicates either a process problem (reminder delivery failure, resource owner unavailability) or a governance failure, and triggers a root-cause review within 10 business days.

## 6. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this policy and the PAM platform; approves the elevation model and break-glass inventory; sole authorized reader. |
| Resource owners | Approve elevation requests and recertify eligibility for their resources. |
| PAM administrators | Operate the broker and vault under dual control. |
| SOC | Monitors privileged sessions and break-glass alerts (MJD-SEC-0009). |
| Incident response | Reviews break-glass use and privileged-access anomalies (MJD-SEC-0006). |

### 6.1 RACI Table for PAM Operations

| Activity | SECURITY_ARCHITECT | Resource owner | PAM administrators | SOC |
|---|---|---|---|---|
| Define privileged account inventory schema | R/A | I | C | I |
| Onboard new privileged account or eligibility | A | R | R | I |
| Monthly inventory reconciliation | A | C | R | I |
| Approve standard elevation request | C | R/A | I | I |
| Approve sensitive-target elevation (HSM, SIEM, PAM broker) | R/A | C | I | I |
| Issue vaulted credential at session start | I | I | R/A | I |
| Monitor privileged session in real time | A | I | I | R |
| Terminate anomalous privileged session | A | I | I | R |
| Review session recordings (risk-based sample) | A | I | I | R |
| Perform break-glass credential rotation | A | I | R (dual) | I |
| Review break-glass use within 24 hours | R/A | I | C | C |
| Send recertification reminders (automated) | A | I | R (automated) | I |
| Certify entitlement at recertification | A | R | I | I |
| Revoke uncertified entitlement (automated) | A | I | R (automated) | I |
| Investigate orphaned privileged account | R/A | C | R | C |
| Approve PAM exception | R/A | C | I | I |

## 7. Exceptions and Escalation

7.1.1 Exceptions (a system that cannot integrate the broker, a temporary standing account) require SECURITY_ARCHITECT approval, a strong compensating control, intensified monitoring, and an expiry no later than 90 days.

7.1.2 Exceptions affecting the HSM/KMS, the SIEM, or the PAM platform itself may not be delegated and are reported to the CISO.

7.1.3 Detection of standing privilege, a bypassed broker, or unjustified break-glass use is escalated immediately as a potential incident (MJD-SEC-0006) and recorded in the risk register (MJD-RSK-0001).

## 8. Worked Example: JIT Elevation to a Production Database

The following example illustrates the complete JIT elevation workflow for a database administrator requesting access to a production database containing CONFIDENTIAL customer data.

**Scenario:** A database administrator (DBA) needs to investigate a performance anomaly on the customer transaction database (a PostgreSQL instance in the Data Zone, MJD-SEC-0004 Z3, containing CONFIDENTIAL transaction records). The DBA holds eligibility for read-only database access on this instance, recertified 12 days ago.

**Step 1: Elevation request (T+0, 14:10 UTC).** The DBA submits an elevation request through the PAM broker portal, specifying: target resource (txn-db-prod-01); entitlement requested (db-readonly); stated reason ("Investigating query latency spike reported in monitoring"); requested duration (2 hours); and their FIDO2 hardware key for identity verification. The broker validates that the DBA's eligibility for db-readonly on txn-db-prod-01 is current (recertified 12 days ago, next expiry in 18 days) and routes the request to the resource owner (the database team lead) for approval.

**Step 2: Approval (T+5 min, 14:15 UTC).** The database team lead reviews the request in the PAM approval portal. They confirm the DBA's identity, the stated reason, and the requested entitlement. The team lead approves the request. Because txn-db-prod-01 is a production database containing CONFIDENTIAL data (per the approval table in Section 2.4), a single approver is sufficient. The approval is logged to the SIEM with the approver's identity, timestamp, and the request ID.

**Step 3: Credential injection (14:15 UTC).** The PAM broker generates a time-limited database credential (PostgreSQL user dba-jit-88a2, password randomly generated, 2-hour TTL). The credential is never displayed to the DBA. The broker establishes an SSH tunnel through the management zone bastion (MJD-SEC-0004 Z5) to txn-db-prod-01 and injects the credential into the DBA's proxied psql session. The DBA connects and sees a standard database prompt; they do not know the credential value.

**Step 4: Session monitoring (14:15 to 16:15 UTC).** The PAM broker records every keystroke and screen state throughout the session. The behavioral analytics engine monitors the session. The DBA runs EXPLAIN ANALYZE on several slow queries, reviews index statistics, and runs a pg_stat_activity query. No anomalous patterns are detected (no bulk data export, no schema modification commands, no account enumeration). The SOC receives no alerts for this session.

**Step 5: Automatic revocation (16:15 UTC).** At the 2-hour mark, the PAM broker automatically terminates the DBA's session and revokes the dba-jit-88a2 database credential. The credential is deleted from the database's user table. The DBA is notified that their session has ended. If the DBA needs more time, they must submit a new elevation request.

**Step 6: Post-session credential rotation.** The PAM broker triggers rotation of any vaulted credentials associated with txn-db-prod-01 that were used to establish the proxied connection (the broker's own service account for that database). Rotation is completed within 5 minutes of session end.

**Step 7: Session recording review (risk-based).** This session is flagged for the weekly risk-based recording review sample. The SOC analyst reviews the recording summary. The commands run are consistent with the stated reason (performance investigation); no anomalies are identified. The session is marked reviewed and closed in the PAM platform.

**Outcome:** The DBA completed their investigation with time-limited, brokered, recorded access. No standing privilege was created. The credential was never known to the DBA. The session is auditable for 7 years.

## 9. Regulatory References

- NIST SP 800-53 Rev 5 (AC-2, AC-6 enhancements): account management and least privilege for privileged accounts.
- PCI DSS 4.0 Requirement 7: restrict access by business need to know.
- PCI DSS 4.0 Requirement 8: identification and authentication, including privileged users.
- GLBA Safeguards Rule (16 CFR Part 314): access controls on customer information systems.
- NYDFS 23 NYCRR 500.7: access privilege management requirements.
- SOC 2 CC6: logical access controls.

## 10. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent no-standing-privilege and least-privilege principles)
- MJD-SEC-0003 Identity and Access Management (IAM) Policy (the non-privileged identity model this policy elevates from)
- MJD-SEC-0004 Network Segmentation and Zero Trust Architecture (the management zone and bastion the broker uses)
- MJD-SEC-0002 Cryptographic Standard (the dual-control key ceremonies and credential rotation referenced in Sections 2 and 4)
- MJD-SEC-0009 Logging, Monitoring, and SIEM Standard (the destination for privileged-session recordings and approvals)
- MJD-SEC-0006 Incident Response Plan (the escalation path for break-glass misuse)

## 11. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-07-15 | SECURITY_ARCHITECT | Initial privileged access policy (credential vaulting). |
| 2.0.0 | 2023-01-30 | SECURITY_ARCHITECT | Eliminated standing privilege; introduced JIT elevation and session recording. |
| 2.1.0 | 2024-08-21 | SECURITY_ARCHITECT | Added dual control for key operations and break-glass governance. |
| 3.0.0 | 2026-02-15 | SECURITY_ARCHITECT | Annual review; tightened recertification to 30 days; added cloud-privilege section. |
