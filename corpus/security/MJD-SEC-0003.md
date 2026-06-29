---
doc_id: MJD-SEC-0003
title: Identity and Access Management (IAM) Policy
department: SECURITY
doc_type: POLICY
classification: CONFIDENTIAL
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT, SOFTWARE_ENGINEER]
effective_date: 2026-01-20
version: 3.3.0
review_cycle_months: 12
regulatory_refs: ["NIST SP 800-63B", "NIST SP 800-53 Rev 5 (AC, IA families)", "GLBA Safeguards Rule (16 CFR Part 314)", "PCI DSS 4.0 Requirement 7", "PCI DSS 4.0 Requirement 8", "SOC 2 CC6"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Identity and Access Management (IAM) Policy

## Purpose and Scope

This Identity and Access Management (IAM) Policy defines how Meridian John Doe Financial (Meridian J.D.) establishes, authenticates, authorizes, and governs the lifecycle of every identity that touches its systems. Identity is the primary security perimeter in the zero-trust model: because no network location is inherently trusted, the strength and correctness of identity controls determine the integrity of every downstream access decision.

This policy applies to all human identities (employees, contractors, third parties) and all machine identities (service accounts, workloads, automation, and AI agents) across all environments. It governs authentication, authorization, role design, joiner-mover-leaver lifecycle, multi-factor authentication, single sign-on, federation, and access certification. It is classified CONFIDENTIAL and is readable by SECURITY_ARCHITECT and SOFTWARE_ENGINEER, because engineers implement the authentication and authorization controls and must understand the model in detail.

Privileged access (administrative, root, break-glass) is governed by the separate, RESTRICTED Privileged Access Management Policy (MJD-SEC-0010); this policy covers standard identity and non-privileged access, and references the PAM policy at every boundary where elevation occurs.

## Definitions

**Identity.** A unique digital representation of a human or machine principal.

**Authentication.** Proving that a principal is who it claims to be.

**Authorization.** Determining what an authenticated principal is permitted to do.

**Entitlement.** A specific grant of access (a permission, role membership, or group).

**Role-based access control (RBAC).** Authorization based on a principal's assigned roles.

**Attribute-based access control (ABAC).** Authorization based on attributes of the principal, the resource, and the context, evaluated together.

**Single sign-on (SSO).** A mechanism allowing one authenticated session to access multiple applications.

**Joiner-mover-leaver (JML).** The identity lifecycle: onboarding, internal transfer, and offboarding.

**Service account.** A non-human identity used by an application or automation.

**Break-glass account.** An emergency access account used only when normal access paths fail (governed by MJD-SEC-0010).

**Orphaned account.** An account whose owning user has departed or been transferred without the account being properly disabled or reassigned.

**Toxic combination.** A pair or group of entitlements that, when held simultaneously by one principal, violates separation of duties.

## 1. Identity Lifecycle (Joiner-Mover-Leaver)

### 1.1 Joiner

1.1.1 Identities are provisioned only after an approved request tied to a verified workforce record from the human resources system of record. No identity exists without an owning workforce member or, for machine identities, an owning team and application.

1.1.2 New identities receive zero entitlements by default. Baseline access (email, directory, collaboration) is granted through a role template; all other access is requested explicitly and approved by the data owner.

1.1.3 Identity provisioning completes within one business day of an approved start date; access is never provisioned ahead of the verified start.

### 1.2 Mover

1.2.1 On internal transfer, the principal's prior entitlements are not retained by default. Entitlements are re-derived from the new role; access that does not map to the new role is revoked within 5 business days.

1.2.2 Accumulated entitlement drift is the primary cause of excess privilege; the mover process exists specifically to prevent it.

### 1.3 Leaver

1.3.1 On termination, all interactive access is disabled within 4 hours of the effective time, and immediately for involuntary terminations.

1.3.2 Service accounts owned by a departing individual are reassigned to a surviving owner before the leaver's access is removed; no service account is left orphaned.

1.3.3 Accounts are disabled, not deleted, for 30 days to preserve audit trails, then deleted per the Records Retention Schedule (MJD-CMP-0008).

### 1.4 Identity Governance Toolchain

1.4.1 Identity provisioning, access requests, access reviews, and deprovisioning are automated through an identity governance and administration (IGA) platform. The IGA platform is the system of record for all entitlement grants and the source of truth for access review workflows.

1.4.2 The IGA platform integrates with: the HR information system (HRIS) as the authoritative source for workforce status and role; the central identity provider (IdP) for user account creation and attribute synchronization; the application portfolio via SCIM 2.0 or proprietary connectors for provisioning and deprovisioning; and the SIEM (MJD-SEC-0009) for audit log streaming.

1.4.3 Provisioning rules are expressed as policy-as-code within the IGA platform. A new role template requires SECURITY_ARCHITECT review and approval before it can be activated. Role template changes are version-controlled and deployed through the same change pipeline as infrastructure code (MJD-TEC-0008).

1.4.4 Access requests outside the baseline role template are submitted through the IGA platform's request workflow. Each request captures: the requestor, the justification, the specific entitlement, the data owner who approves, and a proposed duration (permanent or time-limited). Permanent grants to CONFIDENTIAL resources require re-approval at each 90-day recertification cycle.

### 1.5 Orphaned Account Detection and Remediation

1.5.1 The IGA platform runs an orphaned account detection job daily. An account is classified as orphaned if it meets any of the following criteria: (a) the linked HRIS record shows a termination date that has passed; (b) the linked HRIS record is absent or inactive and the account has not been flagged as a service account with a documented owner; or (c) the account has had no authentication activity in 90 days and has no documented service account designation.

1.5.2 When a potentially orphaned account is detected, the IGA platform: (a) immediately disables the account; (b) sends an alert to the identity operations team and the account's last-known manager; and (c) opens a remediation ticket.

1.5.3 Remediation SLA: the identity operations team must resolve each orphaned account ticket within 5 business days. Resolution means one of: (a) the account is confirmed as a legitimately active service account and is reassigned to a documented owner; or (b) the account is permanently deleted. Unresolved tickets after 5 business days escalate to the SECURITY_ARCHITECT.

1.5.4 Orphaned account metrics (total detected, total remediated, mean time to remediate) are included in the IAM health dashboard reported to the CISO monthly.

## 2. Authentication

### 2.1 Credentials

2.1.1 Passwords follow NIST SP 800-63B guidance: minimum length 12 characters, screened against a breached-password list, no mandatory periodic rotation, and no composition rules that reduce entropy. Credential storage uses the hashing parameters in the Cryptographic Standard (MJD-SEC-0002).

2.1.2 Credentials are never transmitted or stored in plaintext, never embedded in source code, and never shared between principals.

### 2.2 Multi-Factor Authentication (MFA)

2.2.1 MFA is mandatory for all interactive access to CONFIDENTIAL and RESTRICTED systems, all remote access, and all administrative access.

2.2.2 Approved MFA factors, in preference order: FIDO2 / WebAuthn hardware security keys (phishing-resistant, required for administrative and RESTRICTED access), platform authenticators (passkeys), and authenticator-app TOTP. SMS and email one-time codes are prohibited as a primary second factor for CONFIDENTIAL and RESTRICTED access.

2.2.3 Account lockout: after 5 consecutive failed authentication attempts, the account is locked for 15 minutes or until verified reset. Lockout events are logged to the SIEM (MJD-SEC-0009).

### 2.3 Single Sign-On and Federation

2.3.1 All applications integrate with the central identity provider via SSO using OpenID Connect (OIDC) or SAML 2.0. Local application credentials are prohibited where SSO is feasible.

2.3.2 Federation to external identity providers (partners, third parties) uses signed assertions, scoped audiences, and short token lifetimes. The OAuth2 / OIDC implementation details are specified in MJD-TEC-0003.

### 2.4 Session Management

2.4.1 Interactive sessions for CONFIDENTIAL systems idle-timeout after 15 minutes and have a maximum lifetime of 12 hours. RESTRICTED sessions idle-timeout after 10 minutes.

2.4.2 Re-authentication is required for sensitive operations (changing MFA, viewing RESTRICTED data, initiating privileged elevation).

### 2.5 Token and API Key Lifecycle

2.5.1 OAuth2 access tokens issued for human user sessions have a maximum lifetime of 60 minutes for CONFIDENTIAL resources and 15 minutes for RESTRICTED resources. Refresh tokens are issued only to confidential clients (server-side applications) and expire after 24 hours of non-use or 7 days absolute, whichever is shorter.

2.5.2 API keys for machine-to-machine integration are considered long-lived secrets and are governed by the Secrets and Key Management Policy (MJD-TEC-0004). API keys must be: (a) stored exclusively in the approved secrets manager; (b) rotated at least every 90 days; (c) scoped to the minimum permissions required; and (d) associated with a machine identity record in the IGA platform.

2.5.3 Embedding API keys or any secret in source code, configuration files committed to version control, container images, or documentation is prohibited. Detection of an embedded secret in a code scan triggers an immediate incident under MJD-SEC-0006, the secret is revoked within 1 hour of detection, and a replacement is provisioned through the secrets manager.

2.5.4 Short-lived tokens (lifetime 60 minutes or less) are preferred for all machine-to-machine communication. Workload identity federation (using OIDC assertions from the cloud provider or CI/CD platform) is the preferred approach for eliminating long-lived static secrets from automated pipelines.

2.5.5 API key issuance requires a request through the IGA platform naming the owning team, the integration purpose, and the target API. API keys with no authentication activity in 30 days are automatically disabled and escalated to the owning team for review.

### 2.6 Identity Federation Trust Levels

2.6.1 Meridian J.D. assigns a Level of Assurance (LoA) to each federated identity based on the identity proofing and authentication strength of the external IdP, consistent with NIST SP 800-63 assurance levels.

| LoA | NIST 800-63 equivalent | Identity proofing requirement | Authentication requirement | Access permitted |
|---|---|---|---|---|
| LoA-1 | IAL1 / AAL1 | Self-asserted; no identity verification required | Single factor (password) | Public-facing, non-NPI content only; no INTERNAL or above resources |
| LoA-2 | IAL2 / AAL2 | Remote identity proofing with document verification | MFA (authenticator app TOTP or hardware key) | INTERNAL resources; no CONFIDENTIAL or RESTRICTED |
| LoA-3 | IAL3 / AAL3 | In-person or supervised remote identity proofing | FIDO2 hardware key (phishing-resistant) | CONFIDENTIAL resources; RESTRICTED requires additional step-up within session |

2.6.2 A federated identity from a partner IdP is assigned LoA based on the assurance statement in the federation agreement. If the partner IdP does not provide an assurance statement, the identity is assigned LoA-1 by default.

2.6.3 The SECURITY_ARCHITECT reviews and approves all new federation trust relationships before activation. The federation agreement documents the LoA, the token assertion format, the audience restriction, and the partner IdP's incident notification obligations to Meridian J.D.

## 3. Authorization

### 3.1 Model

3.1.1 Meridian J.D. uses RBAC as the baseline with ABAC overlays for data access. A principal's effective access is the intersection of its role entitlements and the attribute policy on the resource.

3.1.2 The canonical attribute model for document and data access is jointly enforced: a principal must clear the resource classification AND appear in the resource's authorized role set. Clearance alone never grants access; role membership alone never grants access. This is the model enforced by every system, including automated retrieval.

3.1.3 Authorization decisions fail closed. An unknown role, a missing classification, or a missing authorized role set results in denial.

### 3.2 Role Design

3.2.1 Roles are designed for least privilege and reviewed for separation of duties. No single role may both initiate and approve the same sensitive transaction.

3.2.2 The seven canonical workforce role families and their clearance ceilings are defined in the Data Classification and Handling Standard (MJD-SEC-0008) and the master policy (MJD-SEC-0001). Only the SECURITY_ARCHITECT family clears RESTRICTED.

### 3.3 Machine Identities

3.3.1 Service accounts use short-lived, automatically rotated credentials sourced from the secrets manager; long-lived static secrets are prohibited (see MJD-TEC-0004 and MJD-SEC-0002 Section 5.2).

3.3.2 Each machine identity is scoped to the minimum permissions for its function and is attributed to an owning team. Workload identity (mTLS service certificates) is preferred over shared API keys.

### 3.4 Separation of Duties Matrix

The following table documents key SoD rules enforced in the IAM and payment systems. The detective control identifies the pair post-fact; the preventive control blocks the combination from being assigned.

| Conflicting role A | Conflicting role B | Risk | Preventive control | Detective control |
|---|---|---|---|---|
| Payment Maker (initiates wires) | Payment Approver (approves wires) | Self-approval of wire transfers | IGA platform blocks simultaneous assignment; payment system blocks self-approval at UI | Daily self-approval attempt log reviewed by Head of Payment Operations |
| FINANCE_CONTROLLER (approves financials) | General Ledger Data Entry | Unauthorized financial entry with self-approval | Separate role groups; no cross-assignment in IGA | Monthly GL reconciliation by external audit per MJD-FIN-0001 |
| SAR Analyst (prepares SARs) | SAR Approver (approves SARs) | Self-approved SAR filing or suppression | Separate groups in AML platform; AML platform enforces two-person rule | BSA audit log reviewed by COMPLIANCE_OFFICER monthly |
| Software Engineer (deploys to production) | Production database write access (direct) | Direct production data manipulation without change control | Production DB access excluded from SOFTWARE_ENGINEER role; requires separate request and PAM elevation | Privileged access audit log reviewed weekly by SECURITY_ARCHITECT |
| SECURITY_ARCHITECT (approves IAM exceptions) | Identity operations (executes provisioning) | Self-approval of own access exceptions | SECURITY_ARCHITECT approvals are logged and reviewed by a second SECURITY_ARCHITECT or CISO monthly | Monthly exception log review |

### 3.5 Privileged-Role Boundary

3.5.1 This policy governs standard (non-privileged) identity and access. Privileged access begins where any of the following conditions are met: (a) the entitlement grants root, sudo, or administrative access to a production system; (b) the entitlement provides access to Z4 (Secrets and Crypto) or Z5 (Management) network zones as defined in MJD-SEC-0004; (c) the entitlement provides break-glass capability; or (d) the entitlement provides direct, unmediated access to production databases or HSMs.

3.5.2 At any of those boundaries, the request, approval, session, and audit trail are governed by MJD-SEC-0010 Privileged Access Management (PAM) Policy, not this policy. The IGA platform routes requests that cross the privileged-role boundary to the PAM workflow automatically, based on the resource classification tag on the target system.

3.5.3 The handoff is triggered as follows: a SOFTWARE_ENGINEER submitting an access request to a production database is routed by the IGA platform to the PAM workflow, which requires SECURITY_ARCHITECT approval, just-in-time session provisioning, and full session recording.

## 4. Access Reviews and Recertification

4.1.1 Access to CONFIDENTIAL systems is recertified every 90 days by the data owner. Access to RESTRICTED systems is recertified every 30 days.

4.1.2 Reviewers attest to each entitlement; unattested entitlements are revoked automatically at the end of the review window (fail closed).

4.1.3 Toxic-combination detection runs continuously to flag entitlement pairs that violate separation of duties.

### 4.2 Certification Workflow

4.2.1 The IGA platform initiates each access certification campaign 14 days before the review deadline. The following steps occur:

1. **Notification**: Data owners receive an email notification listing all principals with access to their resources, including the entitlement name, the date granted, and the last authentication date. The notification includes a direct link to the certification interface.
2. **Attestation window**: Data owners have 10 days to attest each entitlement as Certify (continue) or Revoke. The IGA platform displays entitlements with no recent authentication activity prominently to prompt reconsideration.
3. **Unattestation handling**: Any entitlement not acted on by the end of day 10 is automatically revoked at the close of the attestation window. The data owner receives a notification listing the revoked entitlements. This fail-closed behavior is intentional.
4. **Dispute handling**: If a principal believes their access was incorrectly revoked, they submit a re-access request through the IGA platform's standard request workflow. The request must include a justification and is approved by the data owner (not auto-approved). Disputes do not pause the revocation.
5. **Escalation for non-participation**: Data owners who have not opened the certification campaign by day 7 receive an automated reminder and a notification to their manager. If day 10 passes with no action, the SECURITY_ARCHITECT is alerted and all entitlements are auto-revoked (no extensions are granted).

4.2.2 Certification completion rates and auto-revocation counts are tracked as IAM health metrics and reported to the CISO monthly.

### 4.3 Toxic-Combination Detection Rules

4.3.1 The IGA platform runs toxic-combination detection continuously (evaluating each provisioning and de-provisioning event) and in a nightly batch scan. Detection is based on the SoD rule set defined in Section 3.4 and maintained by the SECURITY_ARCHITECT.

4.3.2 Example toxic pairs and detection/remediation:

| Toxic pair | Detection method | Alert recipient | Remediation SLA |
|---|---|---|---|
| Payment Maker + Payment Approver (same person) | IGA provisioning engine: blocks at provisioning; nightly batch catches legacy grants | Head of Payment Operations; SECURITY_ARCHITECT | Immediate revocation of the later-granted entitlement; 1 business day |
| SAR Analyst + SAR Approver | AML platform event log correlated in SIEM (MJD-SEC-0009); IGA nightly batch | COMPLIANCE_OFFICER; SECURITY_ARCHITECT | Revocation within 4 hours |
| Software Engineer + Production DB write | IGA nightly batch; privileged-access audit log | SECURITY_ARCHITECT | Immediate revocation; PAM elevation required for legitimate need |
| Finance Controller + GL Data Entry | IGA nightly batch | Finance Controller manager; SECURITY_ARCHITECT | Revocation within 1 business day |

4.3.3 A toxic-combination alert that cannot be resolved by revocation alone (for example, because the principal has a legitimate business need that requires both entitlements) is escalated to the SECURITY_ARCHITECT for a risk acceptance or compensating-control decision. Risk acceptances for toxic combinations are logged in MJD-RSK-0001, are time-limited to 90 days, and must be reviewed at each access certification cycle.

## 5. Worked Example: Engineer Joiner Workflow

The following step-by-step example illustrates how a new SOFTWARE_ENGINEER receives their identity and access at Meridian J.D., from the HR trigger through first-day access.

**Day -5 (5 business days before start date):** HR completes onboarding in the HRIS, setting start date 2026-03-02, role SOFTWARE_ENGINEER, team Platform Engineering, manager ENG-MGR-07. The HRIS event triggers a provisioning request in the IGA platform automatically.

**Day -4:** The IGA platform verifies the HRIS record is active and the start date is in the future. No access is provisioned yet. A placeholder identity record is created with status "pre-start."

**Day 0 (start date, 2026-03-02):** At 08:00 on the start date, the IGA platform activates the identity. The following baseline entitlements are granted via the SOFTWARE_ENGINEER role template, with no data-owner approval required:

- Email and calendar account (corporate IdP)
- Internal collaboration platform (read + write)
- Developer documentation portal (read)
- Source code repository access (read-only to all repos; write access to specific repos requires an explicit request)
- Standard laptop enrollment in MDM

**Day 0 (continued):** The new engineer receives a welcome email with instructions to enroll their FIDO2 hardware security key. They cannot access any CONFIDENTIAL resource until MFA enrollment is complete. MFA enrollment must be completed by end of Day 1.

**What is NOT automatically granted:** Production system access (requires explicit request and data-owner approval), production database access (requires PAM elevation and SECURITY_ARCHITECT approval per MJD-SEC-0010), deployment pipeline access to production (requires explicit request and SECURITY_ARCHITECT approval), access to CONFIDENTIAL documents beyond the engineering team's shared resources (each data owner must approve), and any RESTRICTED resource (requires SECURITY_ARCHITECT approval and is subject to RESTRICTED session controls).

**Day 1:** The engineer submits a request through the IGA platform for write access to the specific repos for their team assignment. The team's data owner (ENG-MGR-07) approves within 4 hours. The IGA platform provisions the entitlement and logs it: entitlement Source repo write (Platform repos), granted by ENG-MGR-07, effective 2026-03-03.

**Day 30:** The engineer completes their first month. The IGA platform records a 30-day access review flag for the data owner to confirm the repo access remains appropriate. No new entitlements are granted without explicit requests.

**Day 90:** First CONFIDENTIAL recertification cycle. ENG-MGR-07 receives the certification campaign notification for all CONFIDENTIAL resources to which the engineer has access. ENG-MGR-07 attests the repo write access as Certify. Access continues.

## 6. Exceptions and Escalation

6.1.1 Exceptions (for example a system that cannot integrate SSO) require SECURITY_ARCHITECT approval, a compensating control, and an expiry no later than 12 months.

6.1.2 Suspected credential compromise is escalated immediately to the Security Operations Center under the Incident Response Plan (MJD-SEC-0006), triggering forced reset and session revocation.

6.1.3 Failed recertification that leaves excess access is escalated to the data owner's manager and tracked in the risk register (MJD-RSK-0001).

### 6.2 Exception Type Register

| Exception type | Common examples | Approval path | Maximum duration |
|---|---|---|---|
| SSO exemption | Legacy application that cannot support OIDC or SAML | SECURITY_ARCHITECT approval; compensating MFA control documented | 12 months; renewable with annual SECURITY_ARCHITECT re-review |
| MFA method downgrade | Operational system that cannot support FIDO2; TOTP used instead | SECURITY_ARCHITECT approval; FIDO2 roadmap documented | 6 months; FIDO2 upgrade required before renewal |
| Elevated session timeout | Business process requiring session longer than 12 hours | SECURITY_ARCHITECT approval; re-authentication trigger on sensitive action required | 6 months |
| Service account with long-lived credential | Integration partner that does not support short-lived tokens | SECURITY_ARCHITECT approval; 90-day rotation in secrets manager; MJD-TEC-0004 controls apply | 12 months; migration to short-lived tokens required |
| Toxic-combination risk acceptance | Sole-practitioner role requiring both initiator and approver entitlements | SECURITY_ARCHITECT approval; compensating detective control; risk entry in MJD-RSK-0001 | 90 days; requires renewal at each access certification cycle |

### 6.3 IAM Health Metrics

The following metrics are reported to the CISO monthly and included in the quarterly security program report to the board committee:

| Metric | Target | Escalation threshold |
|---|---|---|
| Orphaned account mean time to remediate | Less than 3 business days | Any unresolved account older than 5 business days |
| Leaver access disable time (involuntary) | 100% within 1 hour of termination effective time | Any leaver access active more than 2 hours after termination |
| Leaver access disable time (voluntary) | 100% within 4 hours | Any leaver access active more than 8 hours after termination |
| MFA enrollment rate (all users with CONFIDENTIAL access) | 100% | Any user with CONFIDENTIAL access lacking MFA for more than 24 hours |
| Access certification completion rate | 100% by end of attestation window | Any campaign below 95% completion at day 7 (escalation to manager) |
| Toxic-combination detection to remediation time | 100% within SLA (see Section 4.3) | Any toxic combination unresolved beyond SLA |
| API key rotation compliance (90-day cadence) | 100% | Any API key unrotated beyond 90 days |
| Exception count (open, approved) | Fewer than 20 active exceptions | More than 20 active exceptions triggers SECURITY_ARCHITECT review of exception hygiene |

## 7. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent identity-perimeter and least-privilege principles)
- MJD-SEC-0010 Privileged Access Management (PAM) Policy (the RESTRICTED governance of administrative and break-glass access)
- MJD-TEC-0003 Authentication and Authorization Standard (OAuth2/OIDC) (the engineering implementation of SSO and federation)
- MJD-SEC-0004 Network Segmentation and Zero Trust Architecture (the zone model that identity controls enforce)
- MJD-SEC-0008 Data Classification and Handling Standard (the classification levels and clearance model used in Section 3.1)
- MJD-SEC-0009 Logging, Monitoring, and SIEM Standard (the destination for authentication and lockout events)
- MJD-TEC-0004 Secrets and Key Management Policy (the machine-identity credential controls of Section 3.3)

## 8. Regulatory References

- NIST SP 800-63B: digital identity guidelines, authentication and lifecycle management.
- NIST SP 800-53 Rev 5 (AC and IA families): access control and identification/authentication controls.
- GLBA Safeguards Rule (16 CFR Part 314): access controls on customer information.
- PCI DSS 4.0 Requirement 7: restrict access by business need to know.
- PCI DSS 4.0 Requirement 8: identify users and authenticate access.
- SOC 2 CC6: logical and physical access controls.

## 9. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-04-10 | SECURITY_ARCHITECT | Initial IAM policy. |
| 2.0.0 | 2022-11-02 | SECURITY_ARCHITECT | Added MFA mandate and SSO requirement. |
| 3.0.0 | 2024-03-18 | SECURITY_ARCHITECT | Adopted NIST 800-63B password guidance; added ABAC overlay. |
| 3.1.0 | 2024-12-01 | SECURITY_ARCHITECT | Mandated FIDO2 for admin access; banned SMS for CONFIDENTIAL. |
| 3.2.0 | 2025-07-22 | SECURITY_ARCHITECT | Added machine-identity and toxic-combination sections. |
| 3.3.0 | 2026-01-20 | SECURITY_ARCHITECT | Annual review; tightened RESTRICTED session and recertification cadence. |
