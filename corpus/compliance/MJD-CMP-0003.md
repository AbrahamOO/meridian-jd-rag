---
doc_id: MJD-CMP-0003
title: Currency Transaction Report (CTR) Procedure
department: COMPLIANCE
doc_type: PROCEDURE
classification: CONFIDENTIAL
owner_role: BSA Officer (Chief Compliance Officer)
allowed_roles: [COMPLIANCE_OFFICER, OPERATIONS_ANALYST, RISK_ANALYST]
effective_date: 2026-02-01
version: 2.3.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1010.311 (CTR filing requirement)", "31 CFR 1010.313 (aggregation)", "31 CFR 1010.306 (filing and retention)", "31 CFR 1010.315 (exemptions)", "FinCEN CTR (FinCEN Form 112)"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Currency Transaction Report (CTR) Procedure

## Purpose and Scope

This procedure defines how Meridian John Doe Financial (Meridian J.D.), a synthetic fintech for demonstration, identifies, aggregates, files, and retains Currency Transaction Reports for qualifying cash transactions. It operationalizes the reporting controls of the BSA/AML Program Policy (MJD-CMP-0001) and is binding on Compliance and on the frontline operations staff whose transactions feed CTR detection.

The procedure covers the cash dollar threshold, same-day aggregation, multiple-business-day handling, identification requirements for the persons involved, the filing deadline, exemptions, structuring detection, and recordkeeping. Because branch and operations activity originates the cash flows that trigger CTRs, this document is readable by the OPERATIONS_ANALYST persona in addition to Compliance and Risk, but it remains CONFIDENTIAL and is not visible to branch staff.

A CTR reports transactions in currency, not all large transactions. Wires, checks, ACH, and book transfers are not currency and do not trigger a CTR, though they may trigger monitoring under MJD-CMP-0004 or a SAR under MJD-CMP-0002.

## Definitions

- **Currency**: Coin and paper money of the United States or any other country that is designated as legal tender and that circulates and is customarily used as a medium of exchange.
- **CTR**: Currency Transaction Report, FinCEN Form 112, filed for reportable currency transactions.
- **Cash in / cash out**: Deposits, withdrawals, exchanges, or payments involving physical currency, tracked separately for aggregation.
- **Aggregation**: Combining multiple currency transactions by or on behalf of the same person on the same business day to determine whether the threshold is met.
- **Person**: An individual or an entity. Transactions on behalf of the same person are aggregated even across multiple accounts.
- **Structuring**: Breaking currency transactions into smaller amounts to evade the CTR filing requirement. Structuring is illegal and triggers a SAR.
- **Exempt person**: A customer that qualifies for a CTR exemption under 31 CFR 1010.315, removing the routine CTR obligation for that customer's currency activity.
- **Conductor**: The individual who physically presents or receives the currency, whether or not the transaction is for that individual's own benefit.
- **Beneficiary / on-behalf-of party**: The person for whose benefit a transaction is conducted. Both the conductor and the on-behalf-of party are recorded.
- **Business day**: A day on which Meridian J.D. is open to the public for substantially all of its banking functions. Currency activity is aggregated within a single business day.
- **Phase I exempt person**: A bank, government agency or entity, or entity whose stock is listed on a major national exchange, and certain subsidiaries, exemptible without an annual review of currency activity.
- **Phase II exempt person**: A non-listed business or a payroll customer with regular, frequent, large currency activity that qualifies for exemption subject to an annual review.
- **Currency in transit / multiple transactions log**: The teller-level record used to capture currency activity that may aggregate to a reportable amount.

## 1. The Reporting Threshold

### 1.1 Dollar Threshold

1.1.1 A CTR is required for each transaction in currency of more than **10,000 USD** conducted by, through, or to the institution by or on behalf of any one person on a single business day.

1.1.2 The threshold is "more than 10,000 USD," meaning a transaction of exactly 10,000 USD does not by itself require a CTR. Cash in and cash out are evaluated separately: more than 10,000 USD in, or more than 10,000 USD out, each triggers a CTR.

1.1.3 The 10,000 USD threshold is fixed by regulation and is not adjustable by Meridian J.D. No internal policy may raise or lower it.

### 1.2 Aggregation Rules

1.2.1 Multiple currency transactions are aggregated when they are conducted by or on behalf of the same person on the same business day and total more than 10,000 USD in the same direction (cash in or cash out).

1.2.2 Aggregation crosses accounts and channels. Currency activity by the same person across multiple branches or products on the same business day is aggregated by the automated CTR detection job.

1.2.3 The automated detection job runs at end of each business day, aggregates by person and direction, and produces a CTR work queue for Compliance review the next business day.

### 1.3 Worked Aggregation Examples

1.3.1 Example A, single transaction. A customer deposits 12,500 USD in cash at a branch. This single cash-in transaction exceeds 10,000 USD and requires a CTR. The conductor and any on-behalf-of party are identified.

1.3.2 Example B, same-day aggregation across accounts. The same customer deposits 6,000 USD cash to a personal account in the morning and 5,500 USD cash to a business account they control in the afternoon, same business day. Cash-in aggregates to 11,500 USD, which exceeds 10,000 USD, so a CTR is required even though no single deposit exceeded the threshold.

1.3.3 Example C, offsetting directions do not net. A customer deposits 11,000 USD cash and, the same day, withdraws 11,000 USD cash. Cash-in (11,000 USD) and cash-out (11,000 USD) are evaluated separately. Each direction independently exceeds 10,000 USD, so the activity is reported. Directions are never netted against each other.

1.3.4 Example D, exactly at the threshold. A customer deposits exactly 10,000 USD cash and conducts no other currency activity that day. Because the rule is "more than 10,000 USD," this single transaction does not by itself require a CTR. A pattern of repeated exactly-at-threshold or just-under transactions is evaluated for structuring under section 5.

### 1.4 Multiple Conductors and On-Behalf-Of Parties

1.4.1 When a reportable transaction involves more than one conductor or is conducted on behalf of one or more parties, each conductor and each on-behalf-of party is identified and recorded on the CTR.

1.4.2 Currency activity conducted on behalf of the same person by different conductors on the same business day is aggregated to that person. The detection job aggregates by the on-behalf-of party as well as by the conductor.

## 2. Identification and Data Collection

### 2.1 Verifying the Person

2.1.1 For each reportable currency transaction, the institution records the identity of the person who conducted the transaction and the person on whose behalf it was conducted, including name, address, identification type and number, date of birth, and tax identification number where applicable.

2.1.2 Frontline operations staff verify identity at the point of transaction using acceptable identification consistent with MJD-OPS-0001 (CIP). Incomplete identification on a reportable transaction is escalated to Compliance before filing.

### 2.2 Cash Handling Linkage

2.2.1 Currency totals are reconciled against the cash handling controls in MJD-RET-0002 so that teller-level cash movements feed CTR detection accurately.

2.2.2 Tellers maintain a multiple-transactions awareness so that a customer attempting to conduct several sub-threshold currency transactions in a single day, whether at one window or across windows, is captured. Teller systems flag a returning customer's same-day currency activity to support aggregation.

### 2.3 Required CTR Data Elements

2.3.1 Each CTR captures, at minimum: the filing institution's identifying information; the date and total amount of cash in and cash out; for each person involved, full legal name, residential or business address, date of birth for individuals, identification type and number, and tax identification number where applicable; the account numbers affected; and the role of each person as conductor, on-behalf-of party, or both.

2.3.2 A transaction conducted by a person who refuses to provide identification, or for which identification cannot be obtained, is still reported with the information available, and the gap is documented and evaluated for suspicious-activity reporting under MJD-CMP-0002.

## 3. Filing

### 3.1 Filing Deadline

3.1.1 The institution files each required CTR electronically through the FinCEN BSA E-Filing System within **15 calendar days** following the date of the reportable transaction.

3.1.2 The CTR work queue is reviewed daily so that no filing approaches the 15-day deadline without action. A queued CTR reaching day 12 without filing is escalated to the BSA Officer.

### 3.2 Review and Sign-Off

3.2.1 A Compliance analyst (COMPLIANCE_OFFICER persona) reviews each CTR for completeness and accuracy before filing. The BSA Officer or delegate holds filing authority and approves exceptions.

3.2.2 The FinCEN acknowledgment (BSA Identifier) is recorded as proof of filing and filing date.

### 3.3 Late, Corrected, and Amended Filings

3.3.1 A reportable transaction discovered after the 15-day deadline is filed promptly upon discovery. The late filing is documented with the reason, the date of discovery, and the corrective action to prevent recurrence, and is reported to the BSA Officer as a control exception.

3.3.2 A CTR found to contain an error is corrected by filing an amended report referencing the original BSA Identifier. Material recurring errors trigger a root-cause review of the upstream data capture in section 2.

3.3.3 The 15-day clock runs from the date of the reportable transaction. For aggregated activity, the clock runs from the business day on which the aggregated currency activity occurred.

### 3.4 Filing Timeline Summary

| Event | Timing |
|---|---|
| Reportable transaction occurs | Day 0 |
| Detection job aggregates and queues | Day 0 end of business |
| Compliance review of queue | Day 1 |
| Day-12 escalation if unfiled | Day 12 |
| Regulatory filing deadline | Day 15 (calendar) |

## 4. Exemptions

4.1 Meridian J.D. may designate certain customers as exempt persons under 31 CFR 1010.315, including specified banks, listed entities, and qualifying non-listed business customers with established, regular, large-volume currency activity.

4.2 Exemption designations are documented, approved by the BSA Officer, reviewed at least annually, and filed where the regulation requires a designation of exempt person filing. An exemption removes the routine CTR obligation but never removes the SAR obligation for suspicious activity.

### 4.1 Exemption Categories

4.1.1 Phase I exempt persons include other banks operating in the United States, federal, state, and local government agencies and entities exercising governmental authority, and entities (and certain majority-owned subsidiaries) whose common stock is listed on a major national securities exchange. Phase I exemptions do not require an annual review of currency activity but are confirmed periodically for continued eligibility.

4.1.2 Phase II exempt persons are non-listed businesses and payroll customers that maintain a transaction account, have done so for the required qualifying period, and conduct frequent, regular currency transactions above the threshold. Phase II exemptions require an annual review confirming continued eligibility.

4.1.3 Certain businesses are ineligible for exemption, including those deriving substantial revenue from activities such as certain cash-intensive or higher-risk lines. The eligibility determination is documented.

### 4.2A Exemption Lifecycle Controls

4.2A.1 Exemptions are tracked in a register recording the designation date, category, eligibility basis, last annual review date, and next review due date. A review that is overdue suspends reliance on the exemption until completed, and currency activity reverts to standard CTR filing in the interim.

4.2A.2 Loss of eligibility (for example a listed entity delisting) triggers prompt removal of the exemption and resumption of CTR filing for that customer.

## 5. Structuring Detection

5.1 Currency activity that appears designed to stay below the 10,000 USD threshold, such as repeated deposits of 9,000 USD across days or branches by the same person, is treated as suspected structuring.

5.2 Suspected structuring is escalated to Compliance and is reported via SAR under MJD-CMP-0002 regardless of whether any single transaction exceeded the CTR threshold. The transaction monitoring rules in MJD-CMP-0004 include dedicated structuring patterns.

5.3 Employees must never advise or assist a customer in avoiding a CTR, for example by suggesting the customer split a deposit across days. Such conduct is prohibited, may constitute a federal crime, and is escalated immediately to the BSA Officer.

5.4 Common structuring red flags captured at the frontline and in monitoring include: a customer who asks whether a transaction will be reported and then reduces the amount; repeated currency transactions just below 10,000 USD; the same customer transacting at multiple branches the same day; and currency activity that breaks a known larger obligation into sub-threshold pieces. These red flags align with rules R-STR-01 and R-STR-02 in MJD-CMP-0004.

## 6. CTR Versus SAR and Recordkeeping

6.1 A CTR and a SAR serve different purposes and are not substitutes. A CTR is an objective report of a large currency transaction; it is filed regardless of whether the activity is suspicious. A SAR is filed when activity is suspicious, regardless of amount. A single event can require both: for example, a 15,000 USD cash deposit that also appears designed to disguise illicit proceeds is both CTR-reportable and SAR-reportable.

6.2 Filing a CTR is never a reason to omit a SAR, and filing a SAR is never a reason to omit a required CTR. Compliance evaluates every reportable currency transaction for both obligations.

6.3 CTR filings, supporting documentation, the BSA Identifier acknowledgments, and exemption records are retained for 5 years per MJD-CMP-0008. The multiple-transactions logs and teller records that feed aggregation are retained per the same schedule so the basis for each filing decision is auditable.

6.4 Access to CTR records is restricted to the COMPLIANCE_OFFICER, OPERATIONS_ANALYST, and RISK_ANALYST personas authorized for this document. While CTRs are not subject to the strict no-disclosure rule that governs SARs, customer identifying information in CTR records is handled per the privacy and data-handling controls in MJD-CMP-0005 and MJD-SEC-0008 referenced through the AML program.

## Roles and Responsibilities

- **BSA Officer (Chief Compliance Officer)**: Owns this procedure, approves exemptions, holds filing authority, ensures deadlines are met.
- **Compliance Analyst (COMPLIANCE_OFFICER persona)**: Reviews the CTR queue, verifies completeness, files in BSA E-Filing, escalates structuring.
- **Operations Analyst (OPERATIONS_ANALYST persona)**: Ensures upstream cash transactions are captured with complete identification so CTR detection is accurate.
- **Risk Analyst (RISK_ANALYST persona)**: Monitors CTR volume trends as a risk indicator.
- **Frontline Staff**: Collect and verify identification at the point of currency transactions.

## 7. Quality Assurance and Reporting

7.1 Compliance performs a periodic quality-assurance review of filed CTRs and of the aggregation logic, at least quarterly. QA confirms that reportable transactions were detected, that aggregation across accounts and conductors was correct, that data elements were complete and accurate, and that filings met the 15-day deadline.

7.2 The program tracks and reports CTR volume, on-time filing percentage, late filings and their root causes, amended-filing rates, and the size and aging of the exemption register. A sustained pattern of late filings or material data errors triggers a root-cause review of the upstream cash-capture controls in section 2 and the detection job in section 1.

7.3 CTR metrics are reported to the BSA/AML Steering Committee and feed the quarterly board report described in MJD-CMP-0001. Unusual movements in CTR volume, for example a sharp decline that is not explained by business activity, are investigated as a possible indicator of a detection-coverage gap.

7.4 The accuracy of CTR detection depends on complete and timely currency data from every branch and channel. Data-completeness testing under the independent test (MJD-CMP-0001 section 4) confirms that all currency activity feeds the detection job, because undetected currency activity cannot be reported.

## Exceptions and Escalation

The 10,000 USD threshold and the 15-day filing deadline are regulatory and cannot be waived by exception. Operational exceptions (for example, a missing identification element) are documented, remediated before filing where possible, and approved by the BSA Officer. A CTR at risk of missing the 15-day deadline is escalated at day 12. Suspected structuring is escalated immediately and handled under the SAR procedure.

## Related Documents

- **MJD-CMP-0001** BSA/AML Program Policy
- **MJD-CMP-0002** Suspicious Activity Report (SAR) Filing Procedure
- **MJD-CMP-0004** Transaction Monitoring Rules and Thresholds
- **MJD-OPS-0001** Customer Identification Program (CIP) Procedure
- **MJD-RET-0002** Cash Handling and Vault Procedure
- **MJD-CMP-0005** GLBA Privacy and Safeguards Policy
- **MJD-SEC-0008** Data Classification and Handling Standard
- **MJD-CMP-0008** Records Retention Schedule

## Regulatory References

- 31 CFR 1010.311, filing obligations for reports of currency transactions
- 31 CFR 1010.313, aggregation of currency transactions
- 31 CFR 1010.306, filing and retention period
- 31 CFR 1010.315, exemptions from the CTR requirement
- FinCEN Form 112, Currency Transaction Report

## Revision History

| Version | Effective date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2021-03-01 | BSA Officer | Initial CTR procedure. |
| 2.0.0 | 2023-05-01 | BSA Officer | Added cross-branch aggregation and automated detection job. |
| 2.2.0 | 2025-02-01 | BSA Officer | Added day-12 escalation control and structuring linkage. |
| 2.3.0 | 2026-02-01 | BSA Officer | Annual review; clarified cash-in versus cash-out separate evaluation. |
