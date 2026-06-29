---
doc_id: MJD-SEC-0008
title: Data Classification and Handling Standard
department: SECURITY
doc_type: STANDARD
classification: INTERNAL
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT, SOFTWARE_ENGINEER, COMPLIANCE_OFFICER, RISK_ANALYST, OPERATIONS_ANALYST, FINANCE_CONTROLLER, BRANCH_STAFF]
effective_date: 2026-01-10
version: 3.1.0
review_cycle_months: 12
regulatory_refs: ["GLBA Safeguards Rule (16 CFR Part 314)", "NIST SP 800-53 Rev 5 (MP, SC families)", "PCI DSS 4.0 Requirement 3", "ISO/IEC 27001:2022 Annex A.5.12", "FFIEC Information Security Booklet"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Data Classification and Handling Standard

## Purpose and Scope

This standard establishes the single, institution-wide scheme for classifying Meridian John Doe Financial (Meridian J.D.) data by sensitivity and defines the mandatory handling requirements for each level: how data may be stored, transmitted, shared, retained, and destroyed. Because every workforce member creates and handles data, this standard is deliberately the most broadly readable security document: it is classified INTERNAL and readable by all seven canonical roles. Everyone must know how to classify and handle data correctly.

This standard is the authoritative definition of the four classification levels that the entire control library and every access-control system depend on. The classification a document carries, combined with a principal's clearance and authorized role set, determines who may read it. The four levels defined here (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED) are the same four levels used in the document metadata schema and enforced by the retrieval access filter.

Scope covers all data in all forms (electronic, physical, verbal) across all environments and all media, including data held by third parties on Meridian J.D.'s behalf.

## Definitions

**Data classification.** The assignment of a sensitivity label to data based on the harm that would result from its unauthorized disclosure, alteration, or loss.

**Data owner.** The accountable role that determines the classification of a data set and approves access to it.

**Data custodian.** The role that operates the systems storing or processing the data on the owner's behalf.

**Nonpublic personal information (NPI).** Customer financial information protected under GLBA.

**Handling requirement.** A mandatory control on how data of a given classification may be stored, transmitted, shared, or destroyed.

**Clearance.** The set of classifications a role is permitted to access (defined in MJD-SEC-0001 and MJD-SEC-0003).

**Need to know.** The requirement that access be limited to those whose duties require the specific data, layered on top of clearance.

**Aggregation.** The combination of two or more data elements, each of lower sensitivity in isolation, that together produce a data set of higher sensitivity.

**k-anonymity.** A property of a dataset in which each record is indistinguishable from at least k-1 other records with respect to a defined set of quasi-identifier fields.

## 1. The Four Classification Levels

### 1.1 Level Definitions

1.1.1 Meridian J.D. uses exactly four classification levels, in ascending order of sensitivity. These are the only valid classification values; no other label is permitted.

| Level | Definition | Impact of unauthorized disclosure | Examples |
|---|---|---|---|
| PUBLIC | Information approved for public release | None | Marketing material, published rates, public website content |
| INTERNAL | Information for internal use; not for public release | Minor; embarrassment or minor operational disadvantage | Internal procedures, org charts, this standard, branch operations manuals |
| CONFIDENTIAL | Sensitive information whose disclosure would cause significant harm | Significant; financial, legal, or reputational harm | Customer NPI, AML procedures, authentication standards, risk frameworks |
| RESTRICTED | The most sensitive information; disclosure would cause severe harm | Severe; existential security or major regulatory harm | Cryptographic key parameters, network/zero-trust topology, privileged-access workflow |

### 1.2 Default and Escalation

1.2.1 Unclassified data defaults to INTERNAL. Data is never treated as PUBLIC by default; PUBLIC requires an explicit approval to release.

1.2.2 A data set takes the classification of its most sensitive element. Aggregation that increases sensitivity (combining INTERNAL fields into a CONFIDENTIAL profile) is reclassified upward.

1.2.3 Downgrading a classification requires data-owner approval and a documented justification; it is never automatic.

### 1.3 Relationship to Access Control

1.3.1 Classification alone does not grant access. A principal may read data only if it clears the data's classification AND is enumerated in the data's authorized role set. The two conditions are joined by AND, never OR. RESTRICTED data is readable only by the SECURITY_ARCHITECT role, which is the only role clearing the RESTRICTED level.

1.3.2 Access decisions fail closed: missing or invalid classification, or a missing authorized role set, results in denial. This applies to every system, including automated retrieval.

### 1.4 Classification Decision Tree

1.4.1 When a workforce member is unsure how to classify a new data set or document, they use the following step-by-step decision flow. Each question must be answered in order; stop at the first question that yields a definitive classification.

Step 1: Is this information explicitly approved for public release by an authorized manager or the communications team?
- Yes: Classify as PUBLIC. Stop.
- No or unsure: Continue to Step 2.

Step 2: Does the data set contain any of the following: customer account numbers, balances, transaction history, SSNs, card numbers, loan details, credit scores, or any other customer financial information protected under GLBA?
- Yes: Classify as CONFIDENTIAL at minimum. If the data also includes cryptographic key material or network topology details, escalate to RESTRICTED. Stop.
- No: Continue to Step 3.

Step 3: Would unauthorized disclosure of this data cause legal harm to Meridian J.D. or its customers? (Examples: AML investigation details, litigation materials, regulatory examination findings, materials covered by attorney-client privilege.)
- Yes: Classify as CONFIDENTIAL. Stop.
- No: Continue to Step 4.

Step 4: Would unauthorized disclosure compromise a security control? (Examples: firewall rule sets, PAM workflows, cryptographic key parameters, SIEM detection logic, network topology.)
- Yes: Classify as RESTRICTED. Stop.
- No: Continue to Step 5.

Step 5: Is this data intended only for internal use, even if it is not particularly sensitive? (Examples: internal procedures, org charts, meeting notes, project plans.)
- Yes: Classify as INTERNAL. Stop.
- No: This data may be PUBLIC, but explicit release approval is still required before treating it as such.

1.4.2 When the decision tree yields an ambiguous result, or when the data set is novel or cross-functional, escalate to the data owner for a classification ruling. The ruling is documented in the data set's metadata. Classify at the higher level while awaiting the ruling.

1.4.3 Aggregation check: after completing the decision tree for individual fields, apply the aggregation test. If combining multiple INTERNAL fields would create a profile that meets the CONFIDENTIAL definition (for example, combining a customer name with transaction timestamps and account number), classify the combined data set as CONFIDENTIAL even if each individual field would be INTERNAL in isolation.

## 2. Handling Requirements by Level

### 2.1 Storage

| Level | Storage requirement |
|---|---|
| PUBLIC | No special control |
| INTERNAL | Stored on Meridian J.D. managed systems; access limited to workforce |
| CONFIDENTIAL | Encrypted at rest (AES-256-GCM per MJD-SEC-0002); access logged |
| RESTRICTED | Encrypted at rest; stored only in approved, segmented systems (MJD-SEC-0004 Z3/Z4); access logged and reviewed every 30 days |

### 2.2 Transmission

| Level | Transmission requirement |
|---|---|
| PUBLIC | No special control |
| INTERNAL | Within Meridian J.D. networks or encrypted channels |
| CONFIDENTIAL | TLS 1.2+ AEAD or TLS 1.3 only (MJD-SEC-0002 Section 2.2); never over unencrypted channels |
| RESTRICTED | Encrypted in transit; mTLS for service-to-service; no transmission to endpoints outside approved zones |

### 2.3 Sharing and Disclosure

2.3.1 CONFIDENTIAL data is shared only with authorized roles on a need-to-know basis and never sent to personal accounts or unsanctioned third-party services (including unsanctioned AI tools).

2.3.2 RESTRICTED data is not shared outside the SECURITY_ARCHITECT role except through a scoped, approved release. The full RESTRICTED documents themselves are never distributed.

2.3.3 Customer NPI is disclosed only as permitted under the GLBA Privacy and Safeguards Policy (MJD-CMP-0005).

### 2.4 Labeling

2.4.1 Documents carry their classification in metadata (and visibly where practical). Every corpus document declares its classification in the metadata header; an unlabeled document is rejected at ingestion (fail closed).

### 2.5 Retention and Destruction

2.5.1 Data is retained per the Records Retention Schedule (MJD-CMP-0008) and destroyed securely at end of life: CONFIDENTIAL and RESTRICTED electronic media are cryptographically erased or physically destroyed; physical CONFIDENTIAL and RESTRICTED documents are cross-cut shredded.

### 2.6 Email and Collaboration Tool Controls

2.6.1 CONFIDENTIAL data may be shared via email only within Meridian J.D. managed email infrastructure, using the corporate email domain, between employees who have a documented need-to-know. External email transmission of CONFIDENTIAL data (to counterparties, regulators, or vendors) is permitted only where there is a business necessity and the recipient is bound by a non-disclosure or data-processing agreement. All external CONFIDENTIAL transmissions are logged.

2.6.2 CONFIDENTIAL data must not be sent to personal email accounts (any account not on a corporate domain), personal cloud storage (Google Drive, Dropbox, iCloud, or equivalent), or collaboration platforms not approved by the IT security team. The approved collaboration platforms list is maintained by IT operations and available on the intranet.

2.6.3 RESTRICTED data must not be transmitted via email or collaboration tools under any circumstances. RESTRICTED information is shared only in person or through approved secure channels with explicit SECURITY_ARCHITECT authorization.

2.6.4 Data Loss Prevention (DLP) controls are deployed on corporate email and approved collaboration platforms. DLP rules automatically detect patterns consistent with CONFIDENTIAL and RESTRICTED data (account number patterns, SSN patterns, key material patterns) and: for CONFIDENTIAL, alert the sender and the security team; for RESTRICTED, block transmission and generate an immediate security alert. DLP alerts are reviewed by the SOC within 2 hours.

2.6.5 Sending CONFIDENTIAL or RESTRICTED data to a personal account is a policy violation subject to disciplinary action and is reported to the SECURITY_ARCHITECT and the employee's manager. If customer NPI was involved, the incident is escalated under the Incident Response Plan (MJD-SEC-0006).

### 2.7 End-User Device Controls

2.7.1 All Meridian J.D. laptops and mobile devices used to access CONFIDENTIAL or RESTRICTED data must have full-disk encryption enabled (BitLocker or FileVault, configured centrally by IT). A device that fails the encryption posture check is blocked from accessing CONFIDENTIAL and RESTRICTED systems until compliance is restored.

2.7.2 Screen lock must activate after no more than 5 minutes of inactivity on any device that accesses INTERNAL, CONFIDENTIAL, or RESTRICTED data. Devices must require authentication (password, PIN, or biometric) to unlock.

2.7.3 Clean desk policy by classification: at end of day and when leaving the workstation unattended for more than 15 minutes, all physical documents must be secured per the table below. Digital screens must be locked.

| Classification | Clean desk requirement |
|---|---|
| PUBLIC | No requirement; may be left on desk |
| INTERNAL | Place face-down or in a desk drawer when leaving the area |
| CONFIDENTIAL | Lock in a secured drawer or cabinet; never left unattended on desk |
| RESTRICTED | Must be stored in an approved secure container (locked safe or secure room); may not be taken outside the approved secure area |

2.7.4 Removable media (USB drives, external hard disks) may not be used to store CONFIDENTIAL or RESTRICTED data unless the media is encrypted and the use is approved by the SECURITY_ARCHITECT. Unapproved removable media is blocked by endpoint device controls.

### 2.8 Print and Physical Media Controls

2.8.1 Printing CONFIDENTIAL or RESTRICTED data is discouraged and permitted only where there is a clear business necessity. The decision to print is made by the data owner or an authorized delegate, and the reason is documented.

2.8.2 Printing CONFIDENTIAL data requires use of the secure-print function: the print job is held in the print queue until the user authenticates at the printer using their corporate badge or PIN. Print jobs are not released to an unattended tray. Printers used for CONFIDENTIAL printing must be in a secured area accessible only to authorized personnel.

2.8.3 RESTRICTED data may not be printed without explicit written SECURITY_ARCHITECT approval. Printed RESTRICTED documents are treated as physical RESTRICTED media, handled under the clean desk policy in Section 2.7.3, and shredded immediately after use.

2.8.4 Physical shredding cadence: CONFIDENTIAL physical documents are shredded using cross-cut or micro-cut shredders no later than 5 business days after the retention period expires, or immediately when they are no longer needed within their retention period. RESTRICTED physical documents are shredded immediately when no longer needed. Shredding is documented by the individual performing it, with a witness signature for RESTRICTED documents.

## 3. Special Categories

### 3.1 Synthetic Test Data (PII canary)

3.1.1 Test data must never contain real customer information. Synthetic records are clearly marked as test data. The following is a planted synthetic-PII test record used to verify that personal data never leaks into logs or AI output; it is entirely fabricated and references no real person:

```
TEST RECORD (SYNTHETIC, NOT REAL):
  Name: Jordan Q. Testerson
  Account: 0000-1111-2222-3333
  SSN: 900-00-0000
  Routing: 110000000
  Note: fabricated for PII-leakage testing only
```

3.1.2 Any appearance of a record matching this pattern in a durable log or in an AI answer is a PII-leakage control failure (MJD-SEC-0009 redaction requirement).

### 3.2 Cardholder Data

3.2.1 Primary account numbers and related cardholder data are CONFIDENTIAL at minimum and handled under the cardholder data environment controls referenced in MJD-SEC-0004. The primary account number is masked to the last four digits in all displays and logs; the full value is encrypted at rest and never stored in plaintext.

### 3.3 Customer Nonpublic Personal Information (NPI)

3.3.1 Customer NPI (account balances, transaction history, identifying details) is CONFIDENTIAL. It is collected, used, and disclosed only as permitted by the GLBA Privacy and Safeguards Policy (MJD-CMP-0005) and is never used for a purpose incompatible with the one for which it was collected.

3.3.2 NPI is minimized: only the fields required for a business purpose are collected and retained, and they are deleted when no longer required (MJD-CMP-0008).

### 3.4 Handling in AI and Retrieval Systems

3.4.1 When data is indexed by an internal AI or retrieval system, the document's classification and authorized role set travel with every chunk derived from it. A chunk that loses its classification or role set is invisible at retrieval (fail closed) and is rejected at ingestion.

3.4.2 The retrieval system never returns, cites, or even reveals the existence of a document to a principal that does not clear its classification and appear in its authorized role set. Out-of-scope content produces a boundary response, not a partial leak.

3.4.3 No CONFIDENTIAL or RESTRICTED data may be sent to an external model provider that has not been approved and contractually bound to the handling requirements of this standard.

### 3.5 Source Code and Configuration Data

3.5.1 Source code is classified based on its content and the sensitivity of the logic it encodes. Code that implements or documents security controls (authentication logic, encryption key handling, access-control enforcement), code that contains embedded configuration for CONFIDENTIAL or RESTRICTED systems, and code that reveals network topology or security architecture is classified CONFIDENTIAL at minimum.

3.5.2 Source code repositories are access-controlled on a need-to-know basis. Access is granted by repository, not globally; a developer working on the payments service does not automatically have access to the risk-scoring model repository. Repository access is reviewed quarterly by the repository owner.

3.5.3 Hardcoded secrets (API keys, passwords, cryptographic key material, tokens) in source code are strictly prohibited. Secrets must be injected at runtime from the approved secrets vault (MJD-SEC-0010, MJD-SEC-0002 Section 5). Any hardcoded secret discovered in a repository is treated as a compromised secret: it is revoked and rotated immediately, and the incident is reported to the SECURITY_ARCHITECT. Automated secret scanning runs on every commit in the CI/CD pipeline (MJD-TEC-0005) and blocks merges that include detected secret patterns.

3.5.4 Configuration files that specify security-relevant settings (firewall rules, TLS configuration, authentication provider endpoints, database connection strings) are classified at the same level as the systems they configure and are stored in the secrets vault or encrypted configuration store, not in plaintext in the repository.

### 3.6 AI Training and Model Artifacts

3.6.1 Training data inherits the classification of its source data. If a training corpus includes documents classified CONFIDENTIAL (such as internal operational procedures or customer transaction summaries), the training dataset as a whole is classified CONFIDENTIAL. If the corpus includes RESTRICTED documents, the dataset is classified RESTRICTED.

3.6.2 Model weights trained on CONFIDENTIAL or RESTRICTED data are themselves classified at the same level as the most sensitive training data. They are stored in an approved, access-controlled model registry with the same handling requirements as the data they were trained on.

3.6.3 No CONFIDENTIAL or RESTRICTED data may be used to train or fine-tune a model hosted by an external provider unless the provider has been approved by the SECURITY_ARCHITECT and has executed a data processing agreement that binds them to the handling requirements of this standard. In practice, this means customer NPI and any RESTRICTED data must not be transmitted to external model APIs for any purpose without this contractual foundation.

3.6.4 Inference requests that include CONFIDENTIAL or RESTRICTED data are subject to the same transmission controls as any other CONFIDENTIAL or RESTRICTED data (Section 2.2). Sending such data to an external model provider in an inference request is subject to the same approval requirement as using it for training.

3.6.5 Model outputs are classified based on the information they may reveal about their training data. A model that can reliably reproduce training data (as measured by membership inference or extraction attacks) is classified at the same level as the training data. Security evaluations of internally deployed models include extraction-attack testing.

## 4. Quick-Reference Handling Summary

4.1.1 The following one-line summary helps workforce members classify on the fly:

| If disclosure would cause... | Classify as | Minimum encryption standard |
|---|---|---|
| No harm; approved for public | PUBLIC | None required |
| Minor internal disadvantage only | INTERNAL | In transit over public networks: TLS 1.2+ |
| Significant financial, legal, or reputational harm | CONFIDENTIAL | At rest: AES-256-GCM; in transit: TLS 1.2+ AEAD or TLS 1.3 |
| Severe security or regulatory harm | RESTRICTED | At rest: AES-256-GCM in approved segmented system; in transit: mTLS only |

4.1.2 When in doubt, classify higher and ask the data owner. Over-classification is a minor inconvenience; under-classification is a potential breach.

### 4.2 Classification Examples by Department

The following table provides one representative example per major department of data at each classification level, to assist workforce members in calibrating their classification decisions.

| Department | PUBLIC example | INTERNAL example | CONFIDENTIAL example | RESTRICTED example |
|---|---|---|---|---|
| Operations | Branch location and hours posted on public website | Internal branch operations manual and staffing schedules | Customer account activity report used for AML monitoring | Network zone diagram showing ACH processing infrastructure |
| Finance | Published annual report | Internal budget planning documents | Customer loan ledger with account balances and NPI | Encryption key rotation schedule for the treasury system |
| Compliance | Published AML policy summary | Internal compliance training materials | Full SAR (Suspicious Activity Report) filing with customer details | Examination findings referencing specific security control weaknesses |
| Technology | Public API documentation | Internal architecture decision records | Application logs containing customer transaction identifiers | Firewall rule sets and privileged access management workflow |
| Security | Published responsible disclosure policy | Internal security awareness training content | Vulnerability scan reports with affected assets and CVE details | Threat intelligence on active nation-state campaigns targeting MJD |
| Risk | Published risk appetite summary | Internal risk committee meeting minutes | Enterprise risk register with financial exposure estimates | Details of compensating controls for RESTRICTED systems |
| Branch staff | Rate sheets and product brochures | Internal branch policy and procedure updates | Customer signature cards and account opening documentation | Not applicable; BRANCH_STAFF role does not clear RESTRICTED |

## 5. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this standard and the classification scheme. |
| Data owners | Classify their data and approve access. |
| Data custodians | Apply the handling controls for the assigned classification. |
| All workforce members | Classify data they create and handle all data per its label. |
| SOFTWARE_ENGINEER | Build systems that enforce labels and handling controls. |
| COMPLIANCE_OFFICER, RISK_ANALYST, OPERATIONS_ANALYST, FINANCE_CONTROLLER, BRANCH_STAFF | Handle data within their roles per this standard. |

### 5.1 RACI Table

| Activity | SECURITY_ARCHITECT | Data owner | Data custodian | SOFTWARE_ENGINEER | All workforce |
|---|---|---|---|---|---|
| Define classification levels and handling rules | R/A | C | I | C | I |
| Classify new data sets | C | R/A | I | C | R (for data they create) |
| Apply handling controls to stored data | A | C | R | R | I |
| Apply handling controls in transit | A | C | R | R | I |
| Approve classification downgrade | R/A | R | I | I | I |
| Approve exceptions to handling requirements | R/A | R | I | I | I |
| Enforce classification in systems | A | I | C | R | I |
| Report suspected misclassification | A | R | C | C | R (report) |
| Conduct annual classification review | R/A | R | C | C | I |

## 6. Exceptions and Escalation

6.1.1 Exceptions to a handling requirement require data-owner and SECURITY_ARCHITECT approval, a compensating control, and an expiry no later than 12 months.

6.1.2 A suspected misclassification that exposes sensitive data is reported immediately and, if disclosure occurred, escalated as a potential incident (MJD-SEC-0006).

6.1.3 Disputes over the correct classification are resolved in favor of the higher level until the data owner rules (fail safe).

6.1.4 Downgrading a classification is appropriate in two specific scenarios: aggregation reversal, and data anonymization. Aggregation reversal occurs when a combined data set that was classified higher due to aggregation is decomposed back into its non-sensitive individual fields, and the component fields are being used in isolation; each component field may then revert to its original lower classification. Data anonymization is the other permissible path: a data set classified CONFIDENTIAL due to the presence of customer identifiers may be reclassified to INTERNAL if a k-anonymity test with k >= 5 (or an equivalent differential privacy guarantee) is applied and validated by the COMPLIANCE_OFFICER and SECURITY_ARCHITECT. The anonymization method and the test results are documented and retained with the data set.

6.1.5 Downgrading is not permitted as a workaround to share data with an unapproved recipient or platform. A downgrade performed for this reason is a policy violation and is escalated as a potential incident.

## 7. Worked Example: Classifying a Combined Dataset

The following example illustrates the application of the classification decision tree and the aggregation rule to a new analytics dataset.

**Scenario:** The data analytics team proposes to create a dataset that combines two existing data sources: (1) internal transaction timestamps extracted from the operations system, classified INTERNAL (each timestamp in isolation identifies only when a transaction occurred, with no customer identifier attached); and (2) a customer account table from the CRM system, containing customer name, account number, and branch assignment, classified CONFIDENTIAL.

**Step 1: Apply the decision tree to each source individually.**

The transaction timestamp file: Step 1 (approved for public release): No. Step 2 (customer financial information): No, timestamps in isolation do not identify customers. Step 3 (legal harm): No. Step 4 (security controls): No. Step 5 (internal use): Yes. Classification: INTERNAL.

The customer account table: Step 1: No. Step 2 (customer account numbers and identifying details): Yes. Classification: CONFIDENTIAL.

**Step 2: Apply the aggregation check to the combined dataset.**

The proposed combined dataset joins transaction timestamps to customer names and account numbers. Once joined, each timestamp row is linked to a named customer and their account number. The combined dataset reveals: which customers transacted, when they transacted, and at which branch. This constitutes customer transaction history linked to customer identifiers, meeting the GLBA NPI definition. The aggregation rule in Section 1.2.2 applies: the combined dataset is classified CONFIDENTIAL, even though one component was INTERNAL.

**Step 3: Resulting handling requirements.**

The combined CONFIDENTIAL dataset must be: encrypted at rest using AES-256-GCM (MJD-SEC-0002); transmitted only over TLS 1.2+ AEAD or TLS 1.3; stored on Meridian J.D. managed systems with access logs; shared only with roles authorized for CONFIDENTIAL data on a need-to-know basis; and retained per the customer data schedule in MJD-CMP-0008. The dataset must not be sent to any external analytics platform without SECURITY_ARCHITECT approval and a data processing agreement.

**Outcome:** The analytics team documents the classification decision (CONFIDENTIAL, due to aggregation) in the dataset metadata and implements the required handling controls before loading the dataset into the analytics environment.

## 8. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent policy that mandates classification and references these four levels)
- MJD-SEC-0002 Cryptographic Standard (the encryption controls the handling table requires for CONFIDENTIAL and RESTRICTED)
- MJD-SEC-0009 Logging, Monitoring, and SIEM Standard (the PII-redaction control protecting the test record in Section 3.1)
- MJD-CMP-0005 GLBA Privacy and Safeguards Policy (the customer-NPI disclosure rules referenced in Section 2.3.3)
- MJD-CMP-0008 Records Retention Schedule (the retention periods governing Section 2.5)
- MJD-SEC-0004 Network Segmentation and Zero Trust Architecture (the segmented zones for RESTRICTED storage)

## 9. Regulatory References

- GLBA Safeguards Rule (16 CFR Part 314): protection of customer nonpublic personal information.
- NIST SP 800-53 Rev 5 (MP, SC families): media protection and system/communications protection.
- PCI DSS 4.0 Requirement 3: protection of stored account data.
- ISO/IEC 27001:2022 Annex A.5.12: classification of information.
- FFIEC Information Security Booklet: data classification expectations.

## 10. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2020-09-01 | SECURITY_ARCHITECT | Initial three-level classification scheme. |
| 2.0.0 | 2022-04-18 | SECURITY_ARCHITECT | Added RESTRICTED level; four-level model. |
| 3.0.0 | 2024-05-22 | SECURITY_ARCHITECT | Added handling tables and access-control relationship. |
| 3.1.0 | 2026-01-10 | SECURITY_ARCHITECT | Annual review; added synthetic-PII test record and AI-handling notes. |
