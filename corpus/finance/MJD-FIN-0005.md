---
doc_id: MJD-FIN-0005
title: Audit Trail and Evidence Standard
department: FINANCE
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: FINANCE_CONTROLLER
allowed_roles: [FINANCE_CONTROLLER, SECURITY_ARCHITECT, RISK_ANALYST, COMPLIANCE_OFFICER]
effective_date: 2026-02-15
version: 2.1.0
review_cycle_months: 12
regulatory_refs: ["Sarbanes-Oxley Act Section 404", "Sarbanes-Oxley Act Section 802", "FFIEC Call Report Instructions", "COSO Internal Control Integrated Framework", "GLBA Safeguards Rule", "SEC Rule 17a-4"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Audit Trail and Evidence Standard

## Purpose and Scope

### Purpose

This standard defines what constitutes acceptable audit-trail and evidence for financial processes at Meridian John Doe Financial (Meridian J.D.), and the controls that keep that evidence complete, attributable, tamper-evident, and retained for the required period. Evidence is what allows the institution to prove, after the fact, that a control operated: that a reconciliation was reviewed, that an expenditure was approved by an authorized person, that a regulatory filing was certified, and that no record was altered without trace. A control that cannot be evidenced is, for audit purposes, a control that did not happen.

### Scope

This standard applies to the audit trails and evidence for all financial processes, including general ledger postings and changes (MJD-FIN-0001), account reconciliations (MJD-FIN-0002), regulatory filings (MJD-FIN-0003), and expense and budget approvals (MJD-FIN-0004). It defines the required attributes of an evidence record, the immutability and access controls over evidence stores, retention periods by record class, and the standard for logging changes to financial data.

Because it describes the integrity controls protecting financial records and the design of the audit-evidence stores, this standard is classified CONFIDENTIAL and is co-owned with the security function (SECURITY_ARCHITECT is in allowed_roles), consistent with the institution's logging and monitoring standard.

### Audience

The readers are finance controllers who own financial evidence, security architects who design and operate the integrity controls, risk analysts who rely on evidence for control assurance, and compliance officers who present evidence to examiners.

## Definitions

**Attributability.** The property that every action in an audit trail is tied to a uniquely identified actor.

**Audit Trail.** The chronological, complete record of who did what, when, and to which financial record.

**Evidence.** A retained artifact that demonstrates a control operated, for example a signed reconciliation, an approval record, or a certified filing.

**Immutability.** The property that a stored record cannot be altered or deleted within its retention period without leaving tamper-evident trace.

**Provenance.** The traceable origin and chain of custody of an evidence record from creation to retention.

**Retention Period.** The minimum duration an evidence record class must be kept.

**Tamper-Evidence.** A control (for example cryptographic hashing or write-once storage) that makes any alteration of a record detectable.

**WORM.** Write Once Read Many storage that physically or logically prevents modification after write.

## 1. Required Attributes of an Evidence Record

### 1.1 Mandatory Fields

Every evidence record for a financial control must capture, at minimum:

| Attribute | Requirement |
|---|---|
| Actor identity | The uniquely identified individual or system account that performed the action |
| Action | What was done (created, posted, reviewed, approved, certified, amended) |
| Object | The specific record affected (account, reconciliation id, filing period, expense id) |
| Timestamp | The action time in UTC to second precision |
| Before and after state | For changes to financial data, the prior and new values |
| Authorization reference | The approval or exception that authorized the action, where applicable |

### 1.2 Completeness

An evidence record missing actor identity, action, object, or timestamp is invalid and the underlying control is treated as not evidenced until corrected. There is no anonymous action against a financial record.

### 1.3 No Personal Data Beyond Need

Evidence records capture identities of internal actors and the financial objects acted upon. They do not capture customer personal data beyond what is strictly necessary; where a customer identifier is required, it is minimized and protected consistent with the GLBA Safeguards obligations. Synthetic test records used to validate this control are clearly marked (see MJD-FIN-0002 section 4).

### 1.4 Evidence by Control

Each financial control produces a defined evidence artifact. The mapping below ties the control to its evidence so that an examiner or auditor knows what to expect.

| Control | Evidence artifact | Source document |
|---|---|---|
| Account creation and change | GL change-log entry with approval | MJD-FIN-0001 |
| Period close and GL lock | Lock record with Controller sign-off | MJD-FIN-0001 |
| Account reconciliation | Signed reconciliation with sources | MJD-FIN-0002 |
| Suspense clearing | Suspense item with clearing journal reference | MJD-FIN-0002 |
| Regulatory filing | Certified filing and edit-resolution log | MJD-FIN-0003 |
| Expenditure approval | Approval record at the correct authority level | MJD-FIN-0004 |
| Control exception | Control exceptions register entry | MJD-FIN-0004 |

### 1.5 Evidence Quality

Evidence must be sufficient (it actually demonstrates the control operated), relevant (it relates to the control asserted), and reliable (it comes from a system of record, not a re-keyed copy). A screenshot of a screen that could be edited is weaker evidence than a system-generated, hashed record; the standard prefers system-generated evidence wherever the system can produce it.

## 2. Immutability and Integrity

### 2.1 Write-Once Evidence Store

Signed evidence (reconciliations, approvals, certified filings, exception records) is stored in a write-once, tamper-evident store. Once an evidence record is finalized and signed, it cannot be edited or deleted within its retention period. A correction is made by appending a new, linked record, never by overwriting.

### 2.2 Tamper-Evidence

Each finalized evidence record carries a cryptographic hash. Hashes are chained or anchored so that any alteration of a stored record, or any gap in the sequence, is detectable. The integrity verification job runs on a scheduled basis and any failure is treated as a security incident and escalated to the security function under section 5.

### 2.3 Change Logging for Financial Data

Every change to financial data (a GL posting adjustment, a mapping change, a budget transfer, a corrected filing figure) is logged with before-and-after state and the authorization reference. The change log is itself held to this immutability standard. Disabling or bypassing change logging for any financial system is prohibited and is a reportable control failure.

### 2.4 Integrity Verification Schedule

The integrity verification job recomputes and checks the hash chain on a daily schedule for high-sensitivity evidence (filings, GL change log) and at least weekly for all other classes. The verification result (pass, fail, records checked, time) is itself an evidence record retained under section 4. A verification failure stops further writes to the affected store until the cause is found, because writing onto a broken chain destroys the ability to prove what happened.

### 2.5 Correction by Linked Record

When a finalized evidence record is wrong, the correction is a new record that references the original, states what changed and why, and carries its own approval. The original is never altered or removed. A reader following the chain sees the original, the correction, and the link between them, so the full history is preserved and the correction is itself auditable.

## 3. Access Control Over Evidence

### 3.1 Least Privilege

Access to the evidence store is least privilege. Finance staff have the access needed for their role; broad read or any write access to finalized evidence is restricted. The ability to administer the evidence store is separated from the ability to perform the financial actions it records, so that no one can both act and erase the trace of acting.

### 3.2 Read Access for Assurance

Risk analysts and compliance officers have read access sufficient to perform control assurance and to present evidence to examiners, without the ability to alter records. Security architects have the access needed to operate and verify the integrity controls.

### 3.3 Access Logging

Access to evidence records is itself logged, so that reads of sensitive evidence are attributable. Access logs are retained to the standard in section 4.

### 3.4 Role-Based Access Summary

| Role | Access to evidence store |
|---|---|
| Finance Controller | Read all financial evidence; finalize and approve corrections |
| Reconcilers and GL Accountants | Read and create evidence for their own work |
| Security Architect | Operate and verify integrity controls; read for incident response |
| Risk Analyst | Read for control assurance; no write |
| Compliance Officer | Read for examiner support; no write |
| Internal Audit | Read for independent testing; no write |

No role combines the ability to perform a financial action, finalize its evidence, and administer the store that holds it. This separation is the core control that prevents an actor from erasing the trace of their own action.

### 3.5 Periodic Access Recertification

Access to the evidence store is recertified at least every six months. Each access grant is reviewed by the Finance Controller jointly with Security; a grant no longer justified by role is removed. The recertification result is retained as evidence under section 4.

## 4. Retention

### 4.1 Retention Schedule

Evidence is retained for at least the periods below, or longer where a legal hold or a record-class retention requirement applies. These align with, and never undercut, the institution-wide records retention schedule.

| Evidence class | Minimum retention |
|---|---|
| Regulatory filings (Call Report, FR Y-9C) and their certifications | 7 years |
| Account reconciliations and sign-offs | 7 years |
| GL change log and mapping changes | 7 years |
| Expense, budget approvals, and the control exceptions register | 7 years |
| Evidence-store access logs and integrity verification results | 13 months minimum, longer where tied to a filing |

#### 4.1.1 Retention Clock

The retention clock starts at the close of the fiscal year in which the record was finalized, not the date of the underlying transaction, so that all records of a year age together and disposal can be managed by year. A record tied to a regulatory filing inherits the longer of its class retention and the filing retention.

#### 4.1.2 Storage Tiering

Evidence moves from active storage (immediately queryable) to archive storage (retrievable within a defined service window) after a class-specific period, but immutability and the hash chain are preserved across tiers. A record in archive is still tamper-evident and still subject to legal hold; tiering changes accessibility, never integrity or retention.

### 4.2 Legal Hold

A legal hold suspends destruction. Records under hold are retained until the hold is released, regardless of the standard retention period. Destruction of records under hold is prohibited.

#### 4.2.1 Hold Lifecycle

A legal hold is issued by General Counsel, names the matter and the record scope, and is logged. While active, the disposal process skips any record in scope. When General Counsel releases the hold, the release is logged and normal retention resumes; records past their standard retention at release become eligible for disposal at the next disposal cycle. A hold is never released verbally; the release is a logged, attributable action.

### 4.3 Disposal

After retention expires and absent a hold, records are disposed of under a documented, approved disposal process. Disposal is itself logged (what class, what period, who approved) so that the absence of a record is explained.

#### 4.3.1 Disposal Approval and Certificate

A disposal run is approved by the Finance Controller after confirming with General Counsel that no hold applies. The run produces a disposal certificate listing the class, the period, the count of records, the approver, and the date. The certificate is itself retained, so that the deliberate, authorized absence of a disposed record is always explainable to an examiner.

### 4.4 Worked Integrity-Incident Example

The daily verification job reports a hash-chain gap in the GL change log for a prior week. Under section 2.4, writes to that store are stopped. Under section 5.2, the event is escalated to Security and the Finance Controller and treated as a security incident. Security determines from the access log (section 3.3) which accounts touched the store in the window, Internal Audit independently reviews the affected records against source systems, and the gap is traced to a failed storage migration rather than tampering. The records are restored from the immutable archive tier (section 4.1.2), the chain is re-verified clean, writes resume, and the incident, root cause, and corrective action are documented and retained. Had the cause been alteration of a finalized record, it would have escalated as potential fraud to Security, the Finance Controller, and Internal Audit under section 5.2.

## 5. Exceptions and Escalation

### 5.1 Requesting an Exception

Any deviation, such as a temporary inability to capture a required evidence attribute or a needed broad-access grant, requires a written exception to the Finance Controller and, where it affects integrity controls, joint approval by the Security function. The exception states the compensating control and an end date.

### 5.2 Escalation Triggers

| Trigger | Escalates to | Treated as |
|---|---|---|
| Integrity verification failure or hash-chain gap | Security function and Finance Controller | Security incident |
| Change logging disabled or bypassed on a financial system | Finance Controller, CFO, and Security | Control failure |
| Evidence record found altered after finalization | Security, Finance Controller, and Internal Audit | Potential fraud |
| Destruction of a record under legal hold | General Counsel, CFO, and Compliance | Serious violation |
| Unauthorized access to evidence store | Security function and Finance Controller | Security incident |

### 5.3 Incident Handling

Integrity and unauthorized-access events follow the institution's incident response process in addition to the financial escalation here. Finance and security jointly own the response for evidence-store incidents.

## 6. Roles and Responsibilities

**Finance Controller.** Owns this standard. Ensures financial controls produce complete evidence, owns retention for financial record classes, and adjudicates exceptions.

**Security Architect.** Co-owns the integrity controls: designs and operates the tamper-evidence, hash verification, and access logging over the evidence store, and leads response to integrity incidents.

**Risk Analyst.** Uses evidence for control assurance and operational risk reporting; receives escalations of control failures.

**Compliance Officer.** Presents evidence to examiners, confirms retention meets regulatory obligations, and is informed of legal-hold and destruction matters.

**Internal Audit.** Independently tests that controls are evidenced to this standard and investigates suspected alteration.

**General Counsel.** Owns legal holds and is escalated on any destruction of held records.

## 7. Related Documents

- MJD-FIN-0001, Chart of Accounts and GL Policy. Source of the GL change log and approval records this standard governs.
- MJD-FIN-0002, Account Reconciliation Procedure. Produces reconciliation evidence and sign-offs retained under this standard.
- MJD-FIN-0003, Regulatory Reporting Procedure (Call Report / FR Y-9C). Produces filing and certification evidence retained for seven years here.
- MJD-FIN-0004, Expense and Budget Approval Policy. Produces approval and control-exception records governed by this standard.
- MJD-SEC-0009, Logging, Monitoring, and SIEM Standard. The security logging standard this evidence standard aligns with for integrity and access logging.
- MJD-CMP-0008, Records Retention Schedule. The institution-wide retention schedule this standard aligns to and never undercuts.

## 8. Regulatory References

The following real frameworks are named for realism. Every threshold and procedure built around them in this fictional document is synthetic and must not be used as compliance guidance.

- Sarbanes-Oxley Act Section 404, internal control over financial reporting.
- Sarbanes-Oxley Act Section 802, retention and prohibition on alteration of records.
- FFIEC Consolidated Reports of Condition and Income (Call Report) Instructions.
- COSO Internal Control Integrated Framework, information and communication, and monitoring.
- Gramm-Leach-Bliley Act, Safeguards Rule, for protection of financial records.
- SEC Rule 17a-4, records retention and write-once storage concepts (named for realism).

## 9. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2023-06-01 | Finance Controller | Initial audit-trail and evidence standard. |
| 1.5.0 | 2024-08-01 | Finance Controller | Added required evidence attributes and retention schedule. |
| 2.0.0 | 2025-07-10 | Finance Controller and Security Architect | Added tamper-evidence, hash chaining, and joint security co-ownership. |
| 2.1.0 | 2026-02-15 | Finance Controller and Security Architect | Added access logging over evidence store, legal-hold and disposal logging, and integrity-incident escalation. |
