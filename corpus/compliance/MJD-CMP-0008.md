---
doc_id: MJD-CMP-0008
title: Records Retention Schedule
department: COMPLIANCE
doc_type: STANDARD
classification: INTERNAL
owner_role: Records and Information Management Officer
allowed_roles: [COMPLIANCE_OFFICER, SOFTWARE_ENGINEER, FINANCE_CONTROLLER, OPERATIONS_ANALYST, RISK_ANALYST, SECURITY_ARCHITECT, BRANCH_STAFF]
effective_date: 2026-01-30
version: 4.0.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1010.430 (BSA recordkeeping)", "31 CFR 1020.410 (records to be made and retained)", "12 CFR 1005.13 (Reg E records)", "12 CFR 1002.12 (Reg B records)", "SEC Rule 17a-4 (where applicable)", "Sarbanes-Oxley Act Section 802"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Records Retention Schedule

## Purpose and Scope

This standard defines how long Meridian John Doe Financial (Meridian J.D.), a synthetic fintech for demonstration, retains records, how records are stored and protected, and how they are disposed of at end of life. It harmonizes the retention obligations across the Bank Secrecy Act, consumer protection regulations, financial reporting requirements, and litigation-hold needs into a single authoritative schedule.

The standard applies to records in every form, paper and electronic, across every department. It is deliberately classified INTERNAL and readable by all seven personas because every employee creates and handles records and must know the applicable retention period. It is the controlling reference cited by the AML, privacy, and consumer-protection procedures for "how long" questions.

Where another document specifies a longer retention period for a specific record type, the longer period governs. Where litigation hold is in effect, the hold overrides routine disposal until released.

## Definitions

- **Record**: Recorded information, regardless of medium, created or received in the course of business.
- **Retention period**: The minimum time a record must be kept before eligible disposal, measured from a defined trigger date.
- **Trigger date**: The event that starts the retention clock, such as account closure, transaction date, or filing date.
- **Litigation hold**: A directive suspending disposal of records relevant to actual or reasonably anticipated litigation, investigation, or examination.
- **Disposition**: The final action on a record at end of retention, either secure destruction or permanent archival.
- **System of record**: The authoritative source for a given record type.
- **Legal hold custodian**: An individual whose records are subject to a specific litigation hold.
- **Certificate of destruction**: A written attestation that records were disposed of per policy.

## 1. Retention Principles

### 1.1 Minimum Retention and Triggers

1.1.1 Retention periods are minimums. Records are retained at least for the stated period from the stated trigger date, then disposed of unless a hold applies.

1.1.2 Records are stored so they are accessible, legible, and retrievable for the full retention period. Electronic records preserve integrity and are protected against alteration consistent with MJD-SEC-0008.

1.1.3 When the trigger date is ambiguous (for example, an open account with no closure date), the retention clock does not start until the triggering event occurs. In the interim the record is retained.

### 1.2 Litigation Hold

1.2.1 When litigation, examination, or investigation is reasonably anticipated, Legal issues a litigation hold. Holds suspend disposal of in-scope records immediately and override the routine schedule until Legal releases the hold in writing.

1.2.2 A litigation hold in effect does not pause the retention clock; it only prevents disposal. When the hold is released, the normal retention period applies to determine the remaining retention time.

### 1.3 Records Inventory and Mapping

1.3.1 The Records and Information Management Officer maintains a records inventory. The inventory maps each record type to: its system of record, the business unit that creates it, its classification level per MJD-SEC-0008, the applicable retention period and trigger, and the disposition method.

1.3.2 Systems of record are registered with the Records and Information Management Officer before a system is placed in production. No new system may become a system of record for a record type without a records inventory entry. The SOFTWARE_ENGINEER persona is responsible for providing the necessary system metadata at the time of registration.

1.3.3 The records inventory is reviewed and updated annually by the Records and Information Management Officer, with confirmation from each business unit owner that the inventory for their records remains accurate.

1.3.4 When a system of record is decommissioned, the records it holds must be migrated to an approved replacement or archived in a format that meets the accessibility and integrity requirements of this standard before the system is shut down. Migration is confirmed by the Records and Information Management Officer in writing.

### 1.4 Legal Hold Process

1.4.1 Legal issues a litigation hold when it reasonably anticipates litigation, a regulatory examination, a government investigation, or any proceeding in which records may be relevant. The hold is issued in writing and specifies: the matter name, the date of issue, the in-scope record categories, the in-scope systems of record, and the list of legal hold custodians.

1.4.2 Legal hold custodians are notified individually and required to acknowledge the hold in writing within 2 business days. The acknowledgment confirms the custodian understands that routine disposal of in-scope records is suspended.

1.4.3 The Records and Information Management Officer coordinates with the IT and records management teams to place a technical suspension on auto-disposal routines for in-scope record categories and systems of record. The technical hold is confirmed in writing to Legal within 5 business days of the hold issuance.

1.4.4 Legal hold monitoring: Legal reviews active holds at least quarterly to determine whether the triggering matter has resolved and the hold may be released. New custodians who join the institution or transfer into a custodian role during an active hold are added to the custodian list within 10 business days of their start.

1.4.5 Release: Legal issues a written hold release when the matter is resolved. The release specifies the matter, the date, and the record categories now eligible for routine disposal. Disposal of released records resumes under the normal schedule from the date of release.

1.4.6 Premature disposal of a record subject to an active litigation hold is an immediate escalation to Legal and the Chief Risk Officer, and is documented as a control failure in the risk register (MJD-RSK-0001).

### 1.5 Admissibility and Authenticity

1.5.1 Electronic records are maintained in formats that preserve their authenticity for regulatory examination and litigation. Authenticity means the record accurately represents the original business transaction and has not been altered after creation.

1.5.2 Systems of record must provide: (a) an audit log recording who created, accessed, and modified each record; (b) a date-and-time stamp at record creation; (c) access controls preventing unauthorized alteration (MJD-SEC-0003); and (d) integrity verification, such as cryptographic hash verification, for immutable record categories.

1.5.3 When records must be produced for a regulatory examination or litigation, the Records and Information Management Officer or Legal coordinates production from the system of record, not from informal copies. The production chain of custody is documented, including the source system, the date of export, the person who performed the export, and the recipient.

## 2. Retention Schedule

### 2.1 BSA/AML Records

| Record type | Retention period | Trigger | Source procedure |
|---|---|---|---|
| SAR filing and supporting documentation | 5 years | From filing date | MJD-CMP-0002 |
| CTR filing and supporting documentation | 5 years | From filing date | MJD-CMP-0003 |
| Transaction monitoring alerts and dispositions | 5 years | From disposition date | MJD-CMP-0004 |
| CIP records (identifying information) | 5 years | From account closure | MJD-OPS-0001 |
| CDD / EDD and beneficial ownership records | 5 years | From account closure | MJD-OPS-0002, MJD-OPS-0003 |
| OFAC screening records and match decisions | 5 years | From screening date | MJD-OPS-0008 |
| Funds transfer records (31 CFR 1010.410) | 5 years | From transaction date | MJD-OPS-0004 |
| BSA training records | 5 years | From training completion | MJD-CMP-0001 |

### 2.2 Consumer Protection Records

| Record type | Retention period | Trigger | Source procedure |
|---|---|---|---|
| Regulation E error resolution files | 2 years | From date of required action | MJD-CMP-0006 |
| Regulation B / fair lending application records | 25 months | From adverse action or grant | MJD-CMP-0007 |
| Adverse action notices | 25 months | From notice date | MJD-CMP-0007 |
| Appraisals and valuations (Reg B) | 25 months | From adverse action or closing | MJD-CMP-0007 |
| Reconsideration of value (ROV) records | 25 months | From ROV decision date | MJD-CMP-0007 |
| Fair lending statistical analyses | 5 years | From analysis date | MJD-CMP-0007 |
| GLBA privacy notices and opt-out elections | 5 years | From relationship end | MJD-CMP-0005 |
| Consumer rights requests and responses | 3 years | From resolution date | MJD-CMP-0005 |
| Customer complaints | 3 years | From resolution date | MJD-RET-0003 |

### 2.3 Financial and Corporate Records

| Record type | Retention period | Trigger | Source procedure |
|---|---|---|---|
| General ledger and financial statements | 7 years | From fiscal year end | MJD-FIN-0001 |
| Regulatory reports (Call Report / FR Y-9C) | 7 years | From filing date | MJD-FIN-0003 |
| Audit trails and evidence | 7 years | From creation | MJD-FIN-0005 |
| Tax records | 7 years | From filing date | MJD-FIN-0001 |
| Board minutes and governance records | Permanent | N/A | MJD-CMP-0001 |
| External audit workpapers | 7 years | From audit completion | MJD-FIN-0005 |
| SOX control testing evidence | 7 years | From fiscal year end | MJD-FIN-0005 |

### 2.4 Technology and Security Records

| Record type | Retention period | Trigger | Source procedure |
|---|---|---|---|
| Security and access logs | 13 months minimum | From log generation | MJD-SEC-0008 |
| Incident response records | 7 years | From incident closure | MJD-SEC-0008 |
| Change management records | 3 years | From change completion | MJD-SEC-0008 |
| Penetration test reports | 5 years | From report date | MJD-SEC-0005 |
| Vulnerability scan results | 2 years | From scan date | MJD-SEC-0005 |
| System of record backups | Per backup policy | From backup date | MJD-SEC-0008 |
| Cryptographic key lifecycle records | 7 years | From key destruction | MJD-TEC-0004 |

### 2.5 Employment and Training Records

| Record type | Retention period | Trigger | Source procedure |
|---|---|---|---|
| BSA/AML training completion records | 5 years | From completion | MJD-CMP-0001 |
| Personnel records | 7 years | From separation | MJD-CMP-0001 |
| Fair lending training completion records | 5 years | From completion | MJD-CMP-0007 |
| Privacy training completion records | 5 years | From completion | MJD-CMP-0005 |

### 2.6 Wire and Payment Records

2.6.1 Wire transfer records are governed by 31 CFR 1010.410 (BSA recordkeeping) and UCC Article 4A (Regulation J). Meridian J.D. retains the following payment records for a minimum of 5 years from the transaction date:

| Record type | Retention period | Regulatory basis |
|---|---|---|
| Outbound wire transfer records (sender name, address, account, amount, execution date, receiving institution) | 5 years | 31 CFR 1010.410(a) |
| Incoming wire transfer records | 5 years | 31 CFR 1010.410(b) |
| ACH origination records (per-file and per-entry) | 5 years | 31 CFR 1010.410; NACHA Operating Rules |
| Payment order instruction records and dual-approval records | 5 years | MJD-OPS-0007 (current edition) / MJD-OPS-0009 (historical) |
| Real-Time Payments (RTP) transaction records | 5 years | 31 CFR 1010.410 by analogy; RTP Network Operating Rules |
| Payment investigation and dispute records | 5 years | From resolution date; 31 CFR 1010.410 |

2.6.2 Wire transfer records must include sufficient detail to permit reconstruction of the transaction and identification of the parties. The minimum required fields are defined in MJD-OPS-0004 Wire Transfer Operations Runbook. Records are stored in the payment operations system of record with access restricted per MJD-SEC-0003.

### 2.7 Model and Algorithm Records

2.7.1 Models and algorithms that influence credit decisions, transaction monitoring, fraud detection, pricing, or other material business outcomes are governed by the Model Risk Management Policy (MJD-RSK-0002). The following records are retained to support model governance, regulatory examination, and SR 11-7 compliance:

| Record type | Retention period | Trigger | Source procedure |
|---|---|---|---|
| Model development documentation (conceptual soundness, data sources, assumptions) | 7 years | From model retirement | MJD-RSK-0002 |
| Model validation reports | 7 years | From model retirement | MJD-RSK-0002 |
| Model performance monitoring reports (ongoing validation) | 7 years | From model retirement | MJD-RSK-0002 |
| Model inventory entries | Permanent (model registry) | N/A | MJD-RSK-0002 |
| Model change records (version history, approvals) | 7 years | From model retirement | MJD-RSK-0002 |
| Fair lending disparate impact test results for models | 5 years | From test date | MJD-CMP-0007 |
| Model risk findings and remediation records | 5 years | From finding closure | MJD-RSK-0002 |

2.7.2 Model records must be stored in the model repository designated as the system of record. Records must be accessible to model validators, auditors, and examiners for the full retention period, including after a model is retired.

## 3. Storage, Protection, and Disposition

### 3.1 Storage and Protection

3.1.1 Records are stored in approved systems of record with access restricted on a least-privilege basis per MJD-SEC-0003 and classified and handled per MJD-SEC-0008. Records containing NPI are protected per MJD-CMP-0005.

3.1.2 Electronic records are protected against unauthorized alteration. Where a record type requires non-rewriteable, non-erasable storage, that control is documented.

### 3.2 Disposition

3.2.1 At the end of the retention period, and absent a litigation hold, records are securely disposed of. Paper records are shredded; electronic records and their backups are securely erased so they are unrecoverable.

3.2.2 Disposition is logged with the record type, the date range, and the authorizing approver. The disposition log is itself retained for 7 years.

3.2.3 Premature disposal of a record before its retention period, or disposal of a record under hold, is a reportable control failure.

## 4. Systems of Record and Storage Standards

### 4.1 Approved Systems by Record Category

4.1.1 The following systems are the approved systems of record for the record categories listed. Records may not be stored exclusively outside the system of record without prior approval from the Records and Information Management Officer:

| Record category | System of record | Approved secondary storage |
|---|---|---|
| BSA/AML filings and monitoring | AML platform (synthetic) | Compliance file repository (read-only archive) |
| Credit applications and origination | Loan origination system (LOS) | Document management system |
| Payment records | Payment operations system | Audit archive |
| Financial records and GL | Core banking ledger | Finance archive |
| Security logs | SIEM (MJD-SEC-0009) | Log archive (write-once) |
| Model development and validation | Model repository | Compliance file repository |
| Incident response records | Incident management system | Compliance file repository |
| HR and training records | HR information system (HRIS) | LMS for training completions |

4.1.2 Cloud storage for records: records stored in cloud infrastructure must be in services that: (a) operate within the network zone model defined in MJD-SEC-0004; (b) enforce encryption at rest using keys managed per MJD-TEC-0004; (c) provide access logs compatible with MJD-SEC-0009; and (d) are located in data centers in approved jurisdictions as specified in the cloud governance policy (MJD-TEC-0007).

4.1.3 Records classified as CONFIDENTIAL or RESTRICTED (per MJD-SEC-0008) must not be stored in consumer-grade cloud services. Only enterprise-contracted cloud services with executed data protection agreements may hold CONFIDENTIAL records.

### 4.2 Backup Verification

4.2.1 Backups of systems of record are verified at least monthly by the SECURITY_ARCHITECT or designated platform engineer. Verification consists of a test restore of a sample of records sufficient to confirm the backup is complete and the records are accessible and unaltered.

4.2.2 Backup verification results are logged, retained for 2 years, and reviewed by the Records and Information Management Officer quarterly. A backup failure or restoration failure for a system of record that holds legally required records is escalated to the Chief Risk Officer within 24 hours.

## 5. Disposition Procedures

5.1 At the end of a record's retention period, the Records and Information Management Officer initiates a disposition review. Disposition proceeds only after confirming: (a) the retention period has been met; (b) no litigation hold is in effect for the record; and (c) no regulatory examination or investigation is pending that may require the record.

5.2 Step-by-step disposition procedure:

1. **Eligibility confirmation**: The Records and Information Management Officer pulls the disposal batch from the records inventory for records whose trigger date plus retention period has passed.
2. **Hold check**: Legal confirms in writing that no active litigation hold covers any record in the batch.
3. **Examination check**: Compliance confirms that no open examination or investigation request covers the records.
4. **Disposition method determination**: The Records and Information Management Officer confirms the approved destruction method for the record type (secure shred for paper, secure erase for electronic, degauss for magnetic media as appropriate).
5. **Destruction execution**: The authorized disposal vendor or IT team executes destruction. For electronic records, deletion must be a cryptographic erasure or secure overwrite to the NIST SP 800-88 Purge or Destroy standard as applicable.
6. **Certificate of destruction**: The Records and Information Management Officer receives and retains a certificate of destruction from the executing party, signed by the person who performed the destruction. The certificate states: the record type, the date range, the volume (file count or weight for paper), and the method used.
7. **Disposition log entry**: The Records and Information Management Officer records the disposition in the disposition log.

5.3 The certificate of destruction and the disposition log entry are themselves retained for 7 years.

5.4 Emergency destruction (destruction required for security reasons before the end of the retention period, for example a compromised paper document) requires approval from Legal and the Records and Information Management Officer and is documented separately from routine disposition. It does not authorize destruction of records under litigation hold.

## 6. Examination and Audit Support

6.1 When a regulatory examination is received, the Records and Information Management Officer coordinates with Legal and the applicable business unit to identify the records in scope and ensure their retrieval from systems of record.

6.2 Records produced for examination are exported from the system of record by an authorized person and documented in a production log: date of production, record type, date range, destination examiner, and the person authorizing release. The production log is retained for 7 years.

6.3 Redaction protocols: examination productions are provided with minimal redaction consistent with legal privilege and regulatory protocol. Any proposed redaction requires Legal approval before the production is sent. A privilege log is prepared for any withheld or redacted document.

6.4 Litigation-hold interaction with examinations: where an active litigation hold overlaps with an examination request, Legal coordinates to ensure the examination production does not waive privilege or conflict with the litigation hold obligations. Records produced to an examiner under a confidentiality agreement are noted in the litigation hold log.

6.5 Audit support: internal audit's access to records is governed by MJD-FIN-0005 Audit Trail and Evidence Standard. The Records and Information Management Officer provides a point of contact for audit requests and confirms that records are retrieved from systems of record rather than informal copies.

## Roles and Responsibilities (RACI)

| Task | Records Officer | Legal | Compliance | Finance Controller | SW Engineer / Sec Architect | Operations / Risk / Branch |
|---|---|---|---|---|---|---|
| Own and update this schedule | Accountable | Consulted | Responsible (BSA/consumer sections) | Consulted (finance sections) | Consulted (tech sections) | Informed |
| Issue litigation holds | Informed | Accountable | Informed | Informed | Informed | Informed |
| Acknowledge litigation hold | Responsible (coordinates custodians) | Accountable | Responsible | Responsible | Responsible | Responsible |
| Technical hold suspension | Informed | Accountable | Informed | Informed | Responsible | Informed |
| Disposition approval | Accountable | Consulted (hold check) | Consulted | Consulted | Informed | Informed |
| Execute secure destruction | Responsible | Consulted | Informed | Informed | Responsible (electronic) | Informed |
| Issue certificate of destruction | Accountable | Informed | Informed | Informed | Responsible (electronic cert) | Informed |
| Examination production | Responsible (coordination) | Accountable | Responsible | Consulted | Responsible (extraction) | Informed |
| Records inventory maintenance | Accountable | Informed | Consulted | Consulted | Consulted | Informed |
| Backup verification | Informed | Informed | Informed | Informed | Accountable | Informed |

## Exceptions and Escalation

An exception to a retention period requires written approval from the Records and Information Management Officer and, where a regulatory minimum is involved, Legal concurrence. No exception may shorten a regulatory minimum. A litigation hold always overrides routine disposal. Suspected premature disposal or disposal under hold is escalated immediately to the Records Officer and Legal and is reported as a control failure.

## Worked Example: BSA SAR Record Lifecycle

The following example illustrates the lifecycle of a SAR record from creation through 5-year retention to disposition.

**Date**: 2026-03-15. An analyst reviewing transaction monitoring alerts identifies a pattern of structuring by account holder "J. Smith" (fictional). The analyst documents the activity in the SAR narrative.

**Filing**: 2026-03-18. The COMPLIANCE_OFFICER approves the SAR. The BSA/AML platform files the SAR with FinCEN and assigns SAR ID MJD-SAR-2026-0042.

**Record creation**: The following records are created and stored in the AML platform: the SAR filing data (SAR form fields), the supporting documentation (alert history, transaction data, narrative), and the approval record. Classification: CONFIDENTIAL per MJD-SEC-0008.

**Retention trigger**: The 5-year retention clock starts on 2026-03-18 (the filing date).

**Retention period**: Records must be retained until 2031-03-18.

**During retention**: Records are stored in the AML platform with access restricted to COMPLIANCE_OFFICER and BSA personnel per MJD-SEC-0003. In 2028 a litigation hold is issued for an unrelated matter. Legal confirms the J. Smith SAR is not in scope. The hold does not affect this record.

**Disposition eligibility**: 2031-03-19. The Records and Information Management Officer confirms: (a) retention period met; (b) no active litigation hold; (c) no open examination covering this SAR. Legal confirms in writing.

**Destruction**: IT executes cryptographic erasure of the SAR record from the AML platform and backup systems. Certificate of destruction is issued, signed by the IT lead.

**Disposition log**: Entry created: SAR records, 2026-03-15 to 2026-03-18, destroyed 2031-03-19, cryptographic erasure, certificate MJD-COD-2031-0042.

**Disposition log retained**: The disposition log entry is retained until 2038-03-19 (7 years from disposition date).

## Related Documents

- **MJD-CMP-0001** BSA/AML Program Policy
- **MJD-CMP-0002** Suspicious Activity Report (SAR) Filing Procedure
- **MJD-CMP-0005** GLBA Privacy and Safeguards Policy
- **MJD-RSK-0001** Enterprise Risk Register
- **MJD-RSK-0002** Model Risk Management Policy (SR 11-7)
- **MJD-SEC-0003** Identity and Access Management (IAM) Policy
- **MJD-SEC-0008** Data Classification and Handling Standard
- **MJD-FIN-0005** Audit Trail and Evidence Standard

## Regulatory References

- 31 CFR 1010.430 and 31 CFR 1020.410, BSA records to be made and retained
- 12 CFR 1005.13, Regulation E record retention
- 12 CFR 1002.12, Regulation B record retention
- SEC Rule 17a-4, records preservation (where applicable)
- Sarbanes-Oxley Act Section 802, retention of records
- NIST SP 800-88, guidelines for media sanitization

## Revision History

| Version | Effective date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2021-08-01 | Records and Information Management Officer | Initial enterprise retention schedule. |
| 2.0.0 | 2023-02-01 | Records and Information Management Officer | Added technology and security records section with 13-month log minimum. |
| 3.0.0 | 2024-11-01 | Records and Information Management Officer | Harmonized BSA 5-year and SOX 7-year periods; added disposition logging. |
| 4.0.0 | 2026-01-30 | Records and Information Management Officer | Annual review; aligned cross-references to current procedure versions and added litigation-hold override detail. |
