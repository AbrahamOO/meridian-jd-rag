---
doc_id: MJD-SEC-0007
title: Threat Modeling Standard
department: SECURITY
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT, SOFTWARE_ENGINEER]
effective_date: 2026-02-10
version: 2.4.0
review_cycle_months: 12
regulatory_refs: ["NIST SP 800-154 (Data-Centric Threat Modeling)", "NIST SP 800-53 Rev 5 (RA, SA families)", "OWASP Threat Modeling", "PCI DSS 4.0 Requirement 6.2", "FFIEC Information Security Booklet"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Threat Modeling Standard

## Purpose and Scope

This standard defines how Meridian John Doe Financial (Meridian J.D.) systematically identifies, analyzes, prioritizes, and mitigates threats to its systems before and during development. It establishes when threat modeling is mandatory, the methodology (STRIDE within a data-flow framing), the risk-ranking approach, the required artifacts, and how findings flow into the secure development lifecycle and the risk register. Threat modeling is the proactive counterpart to incident response: it finds and closes attack paths before an adversary uses them.

This document is classified CONFIDENTIAL and readable by SECURITY_ARCHITECT and SOFTWARE_ENGINEER, because engineers produce threat models for the systems they build and security architecture reviews and approves them.

Scope covers all new systems, all material changes to existing systems, all internet-facing services, all systems processing CONFIDENTIAL or RESTRICTED data, and all AI and retrieval systems. Notably, the bank's internal AI retrieval platform must itself be threat modeled, including its access-control enforcement, prompt-injection surface, and data-poisoning surface; this self-threat-model is a required artifact.

## Definitions

**Threat.** A potential cause of an unwanted incident that may harm a system or organization.

**Threat model.** A structured representation of the threats to a system, the assets at risk, and the mitigations.

**STRIDE.** A threat taxonomy: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, and Elevation of privilege.

**Data-flow diagram (DFD).** A diagram of how data moves through a system, including processes, data stores, external entities, and trust boundaries.

**Trust boundary.** A line across which the level of trust changes; the primary location where threats arise.

**Attack surface.** The set of points where an attacker can attempt to enter or extract data.

**Mitigation.** A control that reduces the likelihood or impact of a threat.

**Residual risk.** The risk remaining after mitigations are applied.

**Material change.** A system change that introduces a new trust boundary, a new data store, a new external integration, a new privilege tier, or a change in the classification of data processed.

## 1. When Threat Modeling Is Required

1.1.1 Threat modeling is mandatory at design time for: every new system or service; every material architectural change (new trust boundary, new data store, new external integration); every system newly processing CONFIDENTIAL or RESTRICTED data; and every internet-facing component.

1.1.2 Existing high-risk systems are re-threat-modeled at least annually and after any security incident affecting them (input from MJD-SEC-0006).

1.1.3 A threat model is a gating artifact in the Secure SDLC (MJD-TEC-0001): a system may not pass its design review without an approved threat model.

### 1.4 Risk Appetite Integration

1.4.1 Threat model risk ratings (Critical, High, Medium, Low) are calibrated to the enterprise risk appetite defined in the Enterprise Risk Management Framework (MJD-RSK-0001). A threat rated Critical in a threat model maps to a Critical-level risk in the enterprise risk register; this ensures threat-model output is directly comparable to financial, operational, and compliance risks at the board level.

1.4.2 Risk acceptance authority follows the enterprise risk appetite tiers. A system owner may accept residual risks rated Low or Medium without escalation, provided mitigations for all higher-rated threats are in place. Residual risks rated High require SECURITY_ARCHITECT acceptance and are recorded in the risk register (MJD-RSK-0001). Residual risks rated Critical may not be accepted at the system-owner or SECURITY_ARCHITECT level; they require escalation to the Information Security Steering Committee (MJD-SEC-0001) and, if they represent a potential material impact to the institution, to the Board Risk Committee.

1.4.3 The board-level escalation threshold for a single threat model finding is: a Critical-rated threat where no mitigation is feasible within 90 days, or a High-rated threat affecting a system that processes customer NPI at scale or that is integral to revenue operations. The SECURITY_ARCHITECT is responsible for identifying when this threshold is reached and initiating the escalation within 5 business days of the threat model approval.

1.4.4 Operationally handled residual risks (accepted at the SECURITY_ARCHITECT level) are reviewed annually during the risk register review cycle and whenever the system undergoes a material change. If the threat landscape changes such that an accepted residual risk becomes more likely or more impactful (for example, a previously theoretical attack pattern is actively exploited in the financial sector), the SECURITY_ARCHITECT may re-escalate the finding without waiting for the annual cycle.

## 2. Methodology

### 2.1 Step 1: Model the System

2.1.1 The team produces a data-flow diagram identifying processes, data stores, external entities, data flows, and, critically, trust boundaries. Each data store is labeled with the classification of the data it holds (MJD-SEC-0008).

2.1.2 Assets are enumerated and ranked by sensitivity; the most sensitive assets (RESTRICTED key material, customer PII, authentication secrets) receive the deepest analysis.

2.1.3 DFD Notation Standards. All DFDs produced under this standard must use the following notation elements, drawn consistently across all threat models to enable review and comparison:

- External entity: a rectangle representing an actor or system outside the trust boundary of the modeled system. Label with: the entity name, the trust level (Untrusted, Semi-trusted, or Trusted), and the data classification of information exchanged.
- Process: a circle or rounded rectangle representing a data-processing function within the system. Label with: the process name, the owner team, and the privilege level at which the process runs.
- Data store: a pair of parallel lines (open rectangle) representing persisted data. Label with: the store name, the classification of the highest-sensitivity data stored (per MJD-SEC-0008), and the encryption-at-rest status.
- Data flow: a directed arrow between elements. Label with: the data type or payload description, the transport protocol, and whether the channel is encrypted (and under which standard from MJD-SEC-0002).
- Trust boundary: a dashed line enclosing a group of elements that share the same trust level. Label with: the boundary name (for example, "Customer Zone," "Application Zone," "Data Zone") and the zone identifier from MJD-SEC-0004.

The approved toolchain for producing DFDs is the organization's threat-modeling tool (currently OWASP Threat Dragon or an equivalent approved by SECURITY_ARCHITECT). DFDs must be stored in the system's design repository alongside the threat model artifact, not only in the tool, so they survive tool migration.

### 2.2 Step 2: Identify Threats with STRIDE

2.2.1 For each element and each trust boundary, the team applies STRIDE to enumerate threats:

| STRIDE category | Property violated | Example mitigation domain |
|---|---|---|
| Spoofing | Authentication | IAM, MFA (MJD-SEC-0003) |
| Tampering | Integrity | Signing, mTLS (MJD-SEC-0002, 0004) |
| Repudiation | Non-repudiation | Audit logging (MJD-SEC-0009) |
| Information disclosure | Confidentiality | Encryption, access control (MJD-SEC-0002, 0008) |
| Denial of service | Availability | Rate limiting, segmentation (MJD-SEC-0004) |
| Elevation of privilege | Authorization | Least privilege, PAM (MJD-SEC-0010) |

2.2.2 For AI/retrieval systems, the threat enumeration explicitly includes: access-control bypass (information disclosure across role boundaries), prompt injection from user input and from retrieved content (tampering/elevation), training- or index-data poisoning (tampering), and model or data extraction (information disclosure).

2.2.3 Banking-Specific Threat Patterns. The following table provides common banking threat patterns mapped to STRIDE, with relevant MJD control references. These patterns must be explicitly considered when threat modeling any system that touches the corresponding asset or business function.

| Threat pattern | STRIDE category | Description | Relevant MJD controls |
|---|---|---|---|
| Credential stuffing on customer portals | Spoofing | Automated use of leaked credential pairs to gain unauthorized access to customer accounts at scale | MJD-SEC-0003 (account lockout, MFA enforcement); MJD-SEC-0009 (velocity detection rule) |
| SWIFT fraud via business email compromise | Spoofing, Tampering | Attacker compromises an employee email account and issues fraudulent payment instructions impersonating a counterparty | MJD-SEC-0003 (privileged account MFA); MJD-SEC-0006 (incident response for payment fraud) |
| ACH origination fraud | Tampering, Elevation of privilege | Insider or compromised account modifies ACH batch files or origination instructions to redirect funds | MJD-SEC-0010 (PAM on ACH origination systems); MJD-SEC-0009 (data integrity monitoring for payment files) |
| Insider trading via data access | Information disclosure | An insider with legitimate access to material non-public information (earnings, M&A) exfiltrates it for trading advantage | MJD-SEC-0008 (need-to-know enforcement); MJD-SEC-0009 (anomalous bulk-access detection); MJD-SEC-0010 (PAM on data warehouses) |
| ATM jackpotting | Tampering, Elevation of privilege | Attacker gains physical or network access to an ATM and installs malware to trigger unauthorized cash dispensing | MJD-SEC-0004 (ATM network segmentation); MJD-SEC-0005 (firmware patching); MJD-SEC-0009 (ATM behavioral monitoring) |

### 2.3 Step 3: Rank Threats

2.3.1 Each threat is ranked by likelihood and impact into a risk rating (Critical, High, Medium, Low). The ranking aligns to the enterprise risk taxonomy (MJD-RSK-0001) so threat-model output is comparable across the bank.

2.3.2 Likelihood and Impact Scoring Tables. Teams use the following 4x4 definitions to score each threat consistently. The combined risk rating is derived from the matrix below.

Likelihood definitions:

| Likelihood level | Definition |
|---|---|
| 4 - Almost Certain | Active exploitation of this attack pattern against financial institutions is confirmed in current threat intelligence; attacker tooling is publicly available; no specialized skill required |
| 3 - Likely | Attack pattern is known and feasible; exploit code or techniques are documented; similar institutions have been successfully attacked in the past 12 months |
| 2 - Possible | Attack is theoretically feasible; requires moderate skill or specific access; no confirmed exploitation in the financial sector in the past 12 months |
| 1 - Unlikely | Attack requires significant skill, specific insider access, or nation-state resources; no known exploitation in this context |

Impact definitions in a banking context:

| Impact level | Definition |
|---|---|
| 4 - Critical | Exfiltration of RESTRICTED data or large-scale customer NPI; total loss of a critical payment system; regulatory sanction or license revocation risk; estimated financial loss exceeding $10M |
| 3 - High | Unauthorized access to CONFIDENTIAL data affecting a significant number of customers; material disruption to revenue-generating systems; estimated financial loss $1M to $10M |
| 2 - Medium | Limited access to INTERNAL data; operational disruption affecting internal users only; estimated financial loss $100K to $1M |
| 1 - Low | Access to PUBLIC data; negligible operational impact; estimated financial loss below $100K |

Risk rating matrix (Likelihood x Impact):

| | Impact 1 | Impact 2 | Impact 3 | Impact 4 |
|---|---|---|---|---|
| Likelihood 4 | Medium | High | Critical | Critical |
| Likelihood 3 | Low | Medium | High | Critical |
| Likelihood 2 | Low | Low | Medium | High |
| Likelihood 1 | Low | Low | Low | Medium |

### 2.4 Step 4: Define Mitigations

2.4.1 Each threat rated Medium or above must have a mitigation mapped to a specific control or a documented, approved risk acceptance. Critical and High threats must be mitigated before release.

2.4.2 Mitigations reference the binding standards (for example, "encrypt in transit per MJD-SEC-0002 Section 2.2") rather than restating control detail.

2.4.3 Control Mapping Guidance. Mitigations in a threat model are mapped to the MJD control library by control family. The following mapping guides engineers to the correct standard for each STRIDE category mitigation:

| STRIDE category | Control family | Primary MJD reference |
|---|---|---|
| Spoofing (IAM mitigations) | Identity and authentication controls | MJD-SEC-0003: MFA requirements, account lifecycle, session management |
| Tampering (integrity mitigations) | Cryptographic integrity controls | MJD-SEC-0002: message signing, mTLS, HMAC requirements |
| Repudiation (audit mitigations) | Logging and non-repudiation controls | MJD-SEC-0009: mandatory event categories, audit log retention |
| Information disclosure (confidentiality mitigations) | Encryption and access control | MJD-SEC-0002: encryption standards; MJD-SEC-0008: classification and handling |
| Denial of service (availability mitigations) | Network and rate-limit controls | MJD-SEC-0004: segmentation, zone isolation; application rate limiting |
| Elevation of privilege (authorization mitigations) | Privileged access controls | MJD-SEC-0010: JIT elevation, PAM broker, least-privilege scoping |
| Cross-cutting (network mitigations) | Network segmentation | MJD-SEC-0004: zone model, mTLS enforcement between zones |

When a proposed mitigation does not map to an existing MJD control, the threat modeler must either: reference a new control being created as part of this system's design (and flag it for addition to the control library); or escalate the gap to the SECURITY_ARCHITECT for a control library update.

### 2.5 Step 5: Validate

2.5.1 Mitigations are validated by design review, code review (MJD-TEC-0009), and where relevant penetration testing (MJD-SEC-0005 Section 1.1.4).

2.5.2 Validation is evidence-based: a mitigation is not considered closed because a control was named, but because the control was demonstrated to operate. For an access-control mitigation on the retrieval platform, validation requires an automated test proving a disallowed role receives a boundary response and that no out-of-scope document id appears in the answer, the citations, the audit log, or the explain payload.

2.5.3 Security Test Coverage Requirements. The following test types are required to validate mitigations for each STRIDE category. Tests must be automated where feasible and integrated into the CI/CD pipeline (MJD-TEC-0005).

| STRIDE category | Required test types |
|---|---|
| Spoofing | Authentication bypass tests: attempt access with missing, expired, and forged credentials; MFA bypass simulation; replay-attack test for session tokens |
| Tampering | Input validation tests: inject malformed, oversized, and adversarially crafted payloads; integrity check tests verifying that tampered payloads are rejected; mTLS certificate validation tests |
| Repudiation | Audit log completeness tests: verify that every required event category (MJD-SEC-0009 Section 1.1) produces a log entry; verify that the log entry contains all required fields; verify that the entry is forwarded to the SIEM |
| Information disclosure | Access-control boundary tests: verify that each role receives only the data it is authorized to see; PII-in-log tests using the MJD-SEC-0008 canary record; encryption-in-transit verification (TLS version and cipher suite assertion) |
| Denial of service | Rate-limit enforcement tests: verify that requests exceeding the rate limit are rejected with the correct response code; resource exhaustion tests: verify that expensive operations are bounded |
| Elevation of privilege | Privilege escalation tests: verify that a lower-privilege principal cannot invoke higher-privilege operations; PAM broker integration tests: verify that elevation requires approval and is time-bounded |

### 2.6 Worked Example: The Retrieval Platform Self-Threat-Model

2.6.1 The internal AI retrieval platform is modeled as a worked example because it is both a required artifact and an illustrative case. Its data-flow diagram crosses several trust boundaries: the untrusted user at the edge, the query graph in the application zone, the access pre-filter, the index in the data zone, the embedding and generation providers, and the audit sink.

2.6.2 STRIDE applied to the platform yields the following representative threats and mitigations:

| Threat (STRIDE) | Description | Mitigation |
|---|---|---|
| Information disclosure | A role retrieves a document outside its access scope | Access pre-filter applied in-query, fail closed, re-validated at citation time (MJD-SEC-0008) |
| Tampering / Elevation | Instructions embedded in a user query attempt to override controls | Input guardrail blocks injection; system never executes user-supplied instructions |
| Tampering / Elevation | Instructions embedded in retrieved content attempt to override controls | Retrieved content is delimited as untrusted data and never followed (planted canary asserts this) |
| Tampering | Poisoned documents are introduced into the index | Ingestion validates metadata and rejects malformed documents (fail closed) |
| Information disclosure | Audit logs leak the existence of out-of-scope documents | Audit record lists only doc_ids that survived the access filter; PII redacted (MJD-SEC-0009) |
| Denial of service | Excessive or expensive queries exhaust resources | Rate limiting at the gateway; token and cost budgets per request |

2.6.3 The residual-risk statement for the platform is signed by the platform owner and reviewed by the SECURITY_ARCHITECT at each material change, and the threat list above drives the security eval suite.

## 3. Required Artifacts

3.1.1 A complete threat model contains: the data-flow diagram with trust boundaries, the asset inventory with classifications, the STRIDE threat list, the risk ranking, the mitigation mapping, and the residual-risk statement signed by the system owner.

3.1.2 Threat models are version controlled alongside the system design and updated when the system changes.

### 3.2 Threat Model Versioning and Change Triggers

3.2.1 Every threat model carries a semantic version number aligned with the system design version it describes. The threat model version is recorded in the threat model artifact and in the design repository.

3.2.2 A material change to a system triggers a mandatory threat model update. Material changes include: adding a new external integration or data source; crossing a new trust boundary or zone (per MJD-SEC-0004); changing the classification of data processed or stored; adding or removing a privileged operation; deploying a new public endpoint; changing the authentication or authorization model; or any change identified as security-relevant in a code review (MJD-TEC-0009).

3.2.3 Non-material changes (bug fixes, performance tuning, UI changes with no new data access, documentation updates) do not require a threat model update. The engineering lead is responsible for determining whether a change is material and documenting the determination. If there is doubt, the change is treated as material (fail safe).

3.2.4 For material changes, the team has two paths: an incremental re-model (reviewing only the portions of the threat model affected by the change) or a full re-model (re-running all five steps from the beginning). An incremental re-model is appropriate when the change is well-scoped and does not affect the overall system architecture. A full re-model is required when: the change affects more than 30% of the DFD elements; the change introduces a new trust boundary; or the SECURITY_ARCHITECT determines that accumulated incremental changes have rendered the threat model stale.

3.2.5 Threat model updates are reviewed and approved by the SECURITY_ARCHITECT before the system change is released to production. The approval is recorded in the design repository with the reviewer's name, the approval date, and the threat model version approved.

## 4. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this standard; reviews and approves threat models; facilitates for high-risk systems. |
| SOFTWARE_ENGINEER | Produces the threat model for systems they design and implements mitigations. |
| System owner | Signs the residual-risk statement and accepts or escalates residual risk. |
| RISK_ANALYST | Consumes threat-model output into the enterprise risk register where residual risk is accepted. |

### 4.1 RACI Table for the Threat Modeling Process

| Activity | SECURITY_ARCHITECT | SOFTWARE_ENGINEER | System owner | RISK_ANALYST |
|---|---|---|---|---|
| Determine that threat modeling is required | A | R | C | I |
| Produce the DFD | C | R | C | I |
| Conduct STRIDE analysis | C/R | R | I | I |
| Rank threats using the scoring table | A | R | C | I |
| Define mitigations | A | R | C | I |
| Review and approve the threat model | R/A | C | C | I |
| Sign the residual-risk statement | C | I | R/A | C |
| Record accepted residual risk in risk register | I | I | C | R/A |
| Validate mitigations (tests and reviews) | A | R | I | I |
| Update threat model on material change | A | R | C | I |
| Annual review of high-risk system threat models | R/A | R | C | C |
| Escalate Critical residual risk to Steering Committee | R/A | I | C | C |

## 5. Exceptions and Escalation

5.1.1 Skipping or deferring a required threat model requires SECURITY_ARCHITECT approval with a documented justification and a deadline; it is never silently omitted.

5.1.2 Residual risk above the system owner's authority is escalated to the SECURITY_ARCHITECT and, if it exceeds appetite, to the Information Security Steering Committee (MJD-SEC-0001).

5.1.3 A Critical or High threat released without mitigation or approved acceptance is a control failure recorded in the risk register (MJD-RSK-0001).

## 6. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent defense-in-depth and assurance principles)
- MJD-TEC-0001 Secure SDLC Policy (the lifecycle gate this standard plugs into)
- MJD-SEC-0008 Data Classification and Handling Standard (the asset-classification labels used in Step 1)
- MJD-SEC-0006 Incident Response Plan (the source of post-incident re-modeling triggers)
- MJD-SEC-0010 Privileged Access Management (PAM) Policy (the elevation-of-privilege mitigation domain)
- MJD-RSK-0001 Enterprise Risk Management Framework (the risk taxonomy the rankings align to)

## 7. Regulatory References

- NIST SP 800-154: guide to data-centric system threat modeling.
- NIST SP 800-53 Rev 5 (RA, SA families): risk assessment and system/services acquisition controls.
- OWASP Threat Modeling: industry methodology reference.
- PCI DSS 4.0 Requirement 6.2: address common software attacks during development.
- FFIEC Information Security Booklet: risk identification expectations.

## 8. Worked Example 2: ACH Origination Module Threat Model

The following example illustrates the application of this standard to a new ACH origination module being added to the payment platform.

**System description:** A new ACH origination module accepts batch payment instructions from the operations team, validates them, signs them, and transmits them to the Federal Reserve ACH network. The module processes CONFIDENTIAL financial data (account numbers, routing numbers, payment amounts) and is operated by OPERATIONS_ANALYST users with elevated access to the ACH origination function.

**DFD elements:**
- External entity: Operations analyst workstation (Semi-trusted; submits batch file over internal network)
- External entity: Federal Reserve ACH network (Trusted counterparty; receives signed outbound file)
- Process: Batch ingestion and validation service (runs as a non-privileged service account in the Application Zone)
- Process: ACH signing service (runs in the Data Zone under JIT elevation via MJD-SEC-0010; uses HSM for signing key per MJD-SEC-0002)
- Data store: Pending ACH batch queue (CONFIDENTIAL; encrypted at rest per MJD-SEC-0002)
- Data store: ACH audit log (CONFIDENTIAL; forwarded to SIEM per MJD-SEC-0009)
- Trust boundaries: Workstation Zone to Application Zone; Application Zone to Data Zone; Data Zone to ACH network

**Top 3 STRIDE threats and mitigations:**

Threat 1: Tampering (ACH batch file modification). An attacker who compromises an OPERATIONS_ANALYST workstation or intercepts the batch file in transit modifies payment amounts or destination account numbers before the file reaches the signing service. Likelihood: 3 (Likely, confirmed attack pattern against financial institutions). Impact: 4 (Critical, direct financial loss and regulatory liability). Risk rating: Critical.

Mitigation: The batch ingestion service computes an HMAC over the file at submission time, bound to the submitting principal's identity token. The signing service re-verifies the HMAC before signing; a mismatch causes the batch to be rejected and an alert generated (MJD-SEC-0009). Transmission from workstation to ingestion service uses mTLS (MJD-SEC-0002, MJD-SEC-0004). Dual authorization: ACH batches above a threshold dollar amount require a second OPERATIONS_ANALYST to approve before the batch enters the signing queue (four-eyes control, logged in MJD-SEC-0009).

Threat 2: Elevation of privilege (unauthorized ACH submission). A user without OPERATIONS_ANALYST authorization submits a batch by exploiting a missing authorization check on the ingestion API endpoint. Likelihood: 2 (Possible, requires knowledge of the API). Impact: 4 (Critical). Risk rating: High.

Mitigation: The ingestion API enforces authorization at the gateway layer (MJD-SEC-0003), requiring a valid token asserting the ACH_ORIGINATOR entitlement. The entitlement is granted only to named OPERATIONS_ANALYST accounts via the PAM broker JIT elevation (MJD-SEC-0010). Authorization checks are enforced at both the gateway and the service layer (defense in depth). Automated tests verify that requests without the entitlement receive a 403 response.

Threat 3: Repudiation (disputed payment instruction). An operations analyst disputes having submitted a payment batch after a fraudulent batch is submitted using their credentials. The institution cannot prove who authorized the batch. Likelihood: 2 (Possible, credential theft scenario). Impact: 3 (High, regulatory and financial liability). Risk rating: Medium.

Mitigation: Every batch submission is logged to the ACH audit log (MJD-SEC-0009) with the submitting principal's identity, the submission timestamp, the HMAC of the batch file, the approval principal for dual-authorization batches, and the HSM key identifier used for signing. The audit log is tamper-evident and retained for 7 years. The combination of the HMAC and the audit record allows the institution to prove the exact file content and the identity of the submitter and approver.

**Residual risk:** After mitigations are applied, the residual risk for all three threats is reduced to Low. The system owner (Head of Operations) signs the residual-risk statement. No escalation to the Steering Committee is required. The threat model is version 1.0 and is stored in the payment platform design repository alongside the DFD.

## 9. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2022-01-12 | SECURITY_ARCHITECT | Initial threat modeling standard (STRIDE). |
| 2.0.0 | 2023-07-08 | SECURITY_ARCHITECT | Added data-flow framing and required-artifact list. |
| 2.1.0 | 2024-02-26 | SECURITY_ARCHITECT | Aligned risk ranking to enterprise taxonomy. |
| 2.2.0 | 2024-11-30 | SECURITY_ARCHITECT | Added AI/retrieval threat enumeration. |
| 2.3.0 | 2025-08-14 | SECURITY_ARCHITECT | Made self-threat-model of the retrieval platform mandatory. |
| 2.4.0 | 2026-02-10 | SECURITY_ARCHITECT | Annual review; clarified gating in the SDLC design review. |
