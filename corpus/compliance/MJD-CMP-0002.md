---
doc_id: MJD-CMP-0002
title: Suspicious Activity Report (SAR) Filing Procedure
department: COMPLIANCE
doc_type: PROCEDURE
classification: CONFIDENTIAL
owner_role: BSA Officer (Chief Compliance Officer)
allowed_roles: [COMPLIANCE_OFFICER, RISK_ANALYST]
effective_date: 2026-02-01
version: 3.1.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1020.320 (SAR requirement for banks)", "31 U.S.C. 5318(g)", "FinCEN BSA E-Filing System guidance", "FFIEC BSA/AML Examination Manual"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Suspicious Activity Report (SAR) Filing Procedure

## Purpose and Scope

This procedure defines how Meridian John Doe Financial (Meridian J.D.), a synthetic fintech for demonstration, identifies, investigates, documents, files, and retains Suspicious Activity Reports. It operationalizes the reporting pillar of the BSA/AML Program Policy (MJD-CMP-0001) and is binding on all Compliance staff who triage alerts, conduct investigations, and make filing decisions.

The procedure covers the full SAR lifecycle: alert intake, investigation, the filing decision, the regulatory filing deadlines, who signs off, continuing-activity review, confidentiality, and recordkeeping. It applies to suspicious activity surfaced by automated monitoring (MJD-CMP-0004), by sanctions screening (MJD-OPS-0008), by frontline referral, by law-enforcement inquiry, and by any other channel.

A SAR is filed whenever the institution knows, suspects, or has reason to suspect that a transaction or pattern involves funds from illegal activity, is designed to evade BSA requirements, has no apparent lawful purpose, or involves the use of the institution to facilitate criminal activity. This procedure states the concrete monetary thresholds and the concrete filing deadline in calendar days.

## Definitions

- **SAR**: Suspicious Activity Report, filed confidentially with FinCEN through the BSA E-Filing System.
- **Alert**: A system-generated or manually raised item indicating potentially unusual activity, requiring triage.
- **Case**: A structured investigation file opened when an alert or referral warrants deeper review.
- **SAR decision date**: The date on which the institution makes the determination that a SAR is required. The filing deadline runs from this date.
- **Continuing activity**: Suspicious activity that persists after an initial SAR has been filed, triggering a follow-up SAR review.
- **30-day rule**: The requirement to file a SAR within 30 calendar days of initial detection of facts that constitute a basis for filing.
- **60-day rule**: The extended deadline of 60 calendar days that applies when no suspect can be identified on the date of initial detection.
- **SAR Review Committee**: The standing body that approves filing or no-filing decisions for cases above a defined complexity or dollar level.
- **Initial detection date**: The date facts first become known that, after reasonable inquiry, constitute a basis for filing. This is the date from which the 30-day and 60-day clocks run, not the alert generation date and not the case-open date.
- **Tipping off**: Disclosing to the subject of a SAR, or to any unauthorized person, that a SAR has been or may be filed, or disclosing its contents. Tipping off is a federal violation.
- **Disposition**: The documented outcome of an alert or case: closed-no-action, escalated, or filed.
- **Narrative**: The free-text section of the SAR that explains the suspicious activity in the who, what, when, where, why, and how structure.
- **SAR backfiling**: The filing of one or more SARs to cover historical suspicious activity discovered after the fact, for example during a lookback review.
- **Keep-open request**: A documented request, typically from law enforcement, to maintain an account that the institution would otherwise close, so that an investigation can continue.

## 1. Detection and Alert Intake

### 1.1 Sources of Suspicious Activity

1.1.1 Suspicious activity reaches Compliance from automated monitoring alerts (MJD-CMP-0004), sanctions screening hits (MJD-OPS-0008), frontline branch referrals (MJD-RET-0003 complaint and unusual-activity referrals), CTR-adjacent patterns such as structuring (MJD-CMP-0003), and external sources including law enforcement.

1.1.2 Every source funnels into a single alert queue with a unique alert identifier, the detection date, the triggering rule or referral reason, and the customer and account references.

### 1.2 Triage Service Levels

1.2.1 Alerts are triaged within 5 business days of generation. Triage either closes the alert with a documented rationale or escalates it to a case.

1.2.2 The detection date for deadline purposes is the date facts first become known that, after reasonable inquiry, constitute a basis for filing. Triage must not be used to artificially delay the start of the filing clock.

### 1.3 Triage Decision Matrix

1.3.1 At triage, the analyst dispositions each alert into one of three outcomes, each requiring documentation:

| Triage outcome | Criteria | Documentation required |
|---|---|---|
| Closed, no action | Activity explained by legitimate, expected behavior consistent with the CDD baseline (MJD-OPS-0002) | Rationale, supporting evidence, analyst identity, date |
| Escalated to case | Activity unexplained or consistent with a suspicious typology and warrants deeper review | Case opened, initial detection date recorded, investigator assigned |
| Filed immediately | Clear suspicious activity already supported by the record (for example a confirmed structuring pattern) | Case opened and fast-tracked to filing decision |

1.3.2 An alert closed at triage that later recurs for the same customer is reopened and re-evaluated, and the prior closure rationale is reviewed for adequacy. Repeated closures of recurring activity for the same customer are a quality flag reviewed by the BSA Officer.

1.3.3 The triage analyst records the basis for the initial detection date in the case file so that the filing clock is auditable.

## 2. Investigation

### 2.1 Case File Contents

2.1.1 Every case file documents: the customer profile and risk rating, the expected activity baseline, the actual activity under review, the investigator's analysis, supporting transaction records, prior SAR history for the subject, and the recommended disposition. The file also records the initial detection date and its basis, the lookback period reviewed, every external source consulted, and the identity and date of each reviewer in the approval chain.

2.1.1A The SAR narrative is held to a documented quality standard. It states, in plain language: who conducted the activity and their relationship to the institution; what instruments and amounts were involved; when the activity occurred, including the date range; where it occurred across accounts, branches, and channels; why the institution considers it suspicious, referencing the baseline and the typology; and how the activity was conducted as a transaction flow. The narrative avoids unsupported conclusions, defines any internal codes, and does not paste raw system dumps in place of analysis.

2.1.2 The investigator reviews a lookback period of at least 90 days of activity, extended to 12 months when a pattern such as structuring or rapid movement of funds is suspected. Where the investigation reveals suspicious activity predating the lookback, the lookback is extended further and any required SARs are backfiled.

### 2.1A Suspicious Activity Typologies

2.1.2A.1 Investigators evaluate activity against the institution's documented typology catalog. The catalog maps each typology to the monitoring rules in MJD-CMP-0004 that most often surface it:

| Typology | Indicators | Related monitoring rule |
|---|---|---|
| Structuring | Multiple sub-threshold cash transactions, just-under-CTR amounts | R-STR-01, R-STR-02 |
| Layering / rapid movement | Funds in and quickly out, pass-through accounts | R-VEL-02 |
| Funnel account activity | Deposits in many locations, withdrawals concentrated elsewhere | R-VEL-01, R-CTP-01 |
| Trade-based money laundering | Payment patterns inconsistent with stated business | R-GEO-01 |
| Dormant account abuse | Sudden reactivation with large flows | R-BEH-01 |
| Mule / third-party activity | Round-number transfers, new counterparty concentration | R-BEH-02, R-CTP-01 |

2.1.2A.2 The narrative ties the observed activity to the identified typology, the customer's expected baseline, and the specific transactions, so that a reader of the SAR can reconstruct the analysis.

### 2.2 Reportable Activity Thresholds

2.2.1 A SAR is required, regardless of dollar amount, whenever the institution suspects involvement of an identifiable insider or believes the activity may relate to terrorist financing or money laundering with no apparent lawful purpose.

2.2.2 For other suspicious activity, the regulatory minimum aggregate dollar thresholds that trigger a mandatory SAR are:

| Scenario | Minimum aggregate amount | SAR required |
|---|---|---|
| Suspect identified | 5,000 USD | Yes, if activity is suspicious |
| No suspect identified | 25,000 USD | Yes, if activity is suspicious |
| Insider abuse, any amount | 0 USD | Yes |
| Suspected terrorist financing or money laundering | Any amount | Yes |

2.2.3 Meridian J.D. may file a SAR voluntarily below these thresholds when the activity is suspicious and a filing serves a legitimate purpose. Voluntary filings receive the same safe-harbor protection.

## 3. Filing Decision and Sign-Off

### 3.1 Who Signs Off

3.1.1 An investigating Compliance analyst (COMPLIANCE_OFFICER persona) prepares the SAR recommendation and the narrative.

3.1.2 The filing decision is approved by the BSA Officer (Chief Compliance Officer) or a named delegate with documented signing authority. The BSA Officer's approval is the controlling sign-off and is recorded in the case file with date and identity.

3.1.3 Cases involving an aggregate amount of 100,000 USD or more, an insider, a PEP, or suspected terrorist financing are reviewed by the SAR Review Committee before the BSA Officer signs off. The committee comprises the BSA Officer, a senior Compliance analyst, and a Risk representative.

3.1.4 A decision not to file ("no-SAR") on an escalated case is itself documented, with rationale, and approved at the same authority level as a filing decision.

### 3.2 Filing Deadlines

3.2.1 The institution files the SAR no later than **30 calendar days** after the SAR decision date (the date initial detection facts establish a basis for filing).

3.2.2 If no suspect can be identified on the date of initial detection, the institution may delay filing for an additional 30 calendar days to identify a suspect, but in no case may filing exceed **60 calendar days** after the date of initial detection.

3.2.3 The filing clock is tracked per case. A case approaching day 25 without an approved filing is escalated automatically to the BSA Officer. Missing the 30-day or 60-day deadline is a reportable control failure escalated to the board.

### 3.3 Filing Mechanics

3.3.1 SARs are filed electronically through the FinCEN BSA E-Filing System. The narrative follows the who, what, when, where, why, and how structure and avoids speculation unsupported by the record.

3.3.2 The acknowledgment (BSA Identifier) returned by FinCEN is recorded in the case file as proof of filing and filing date.

### 3.4 Worked Example: Computing the Filing Deadline

3.4.1 Example A, suspect identified. On day 0 (for instance March 3), monitoring rule R-STR-01 fires and triage on the same day establishes that facts constitute a basis for filing, with the customer identified as the suspect. The initial detection date is March 3. The SAR must be filed no later than 30 calendar days after March 3, that is by April 2. The day-25 automatic escalation to the BSA Officer occurs on March 28 if no approved filing exists.

3.4.2 Example B, no suspect identified. On day 0 a wire pattern is detected but the beneficial actor cannot be identified. The institution may take an additional 30 calendar days to identify a suspect, but filing may never exceed 60 calendar days from initial detection. If a suspect is identified on day 20, the institution should file promptly and in no case later than the 60-day outer limit.

3.4.3 Example C, continuing activity. A SAR is filed on June 1 on an account that continues to show suspicious activity. Compliance reviews the account every 90 days from June 1. A follow-up SAR covering the continuing activity is filed no later than 120 calendar days after June 1, that is by September 29. Any newly detected, distinct suspicious activity starts its own independent 30-day or 60-day clock.

### 3.5 Account Decision and Keep-Open Requests

3.5.1 Filing a SAR does not by itself require closing the account. The relationship decision (retain, restrict, or exit) is made separately, documented, and based on the institution's risk appetite (MJD-CMP-0001).

3.5.2 A law-enforcement keep-open request is honored only when documented in writing by the requesting agency with a defined duration and a point of contact. The institution continues to file SARs on continuing activity during a keep-open period. Verbal keep-open requests are not actioned without written confirmation.

## 4. Continuing Activity

4.1 When suspicious activity continues after an initial SAR, Compliance reviews the account on a 90-day cycle from the prior filing.

4.2 If the continuing activity warrants it, a follow-up SAR is filed no later than **120 calendar days** after the date of the previously filed SAR, covering the period since that filing. The 30-day and 60-day deadlines in section 3.2 apply independently to any newly detected, distinct suspicious activity.

4.3 Each continuing-activity SAR references the prior filing's BSA Identifier so that FinCEN and any reviewer can trace the sequence of filings on the same subject. The 90-day review cadence continues until Compliance documents that the suspicious activity has ceased or the relationship has been exited, at which point a final review is recorded.

4.4 A keep-open request under section 3.5 does not suspend the continuing-activity filing obligation. The institution keeps filing on a continuing-activity basis throughout the keep-open period while coordinating with the requesting agency.

## 5. Confidentiality and Safe Harbor

5.1 The existence and contents of a SAR are strictly confidential. No employee may disclose to the subject, or to any person not authorized, that a SAR has been filed or considered. Unauthorized disclosure is a federal violation.

5.2 SAR-related communications are restricted to the COMPLIANCE_OFFICER and RISK_ANALYST personas authorized for this document and to law enforcement and regulators acting in their official capacity.

5.3 Good-faith filings are protected by the safe harbor at 31 U.S.C. 5318(g)(3). No employee is retaliated against for raising or filing in good faith.

5.4 SAR records, supporting documentation, and the BSA Identifier acknowledgments are retained for 5 years from the filing date per MJD-CMP-0008. Access is logged. A request for SAR information from law enforcement or a regulator is verified and routed through the BSA Officer; a subpoena or request from any other party is referred to FinCEN and Legal and never answered directly.

## 6. Quality Assurance and Metrics

6.1 A quality-assurance review samples filed SARs and closed alerts at least quarterly. QA evaluates narrative completeness, accuracy of the initial detection date, timeliness against the 30-day and 60-day deadlines, and the adequacy of no-SAR rationales.

6.2 The program tracks and reports to the Steering Committee and board: alert volume and aging, case backlog, SAR filing volume and on-time filing percentage, alert-to-SAR conversion rate, and continuing-activity filing compliance. A sustained on-time filing rate below 100 percent is treated as a control deficiency, since every missed statutory deadline is reportable.

6.3 QA findings feed back into monitoring tuning (MJD-CMP-0004) and training (MJD-CMP-0001 section 5), closing the loop between detection quality and program improvement.

6.4 The program retains evidence of the QA reviews, including the sample selected, the criteria applied, the defects found, and the corrective actions taken. QA evidence is itself an input to the annual independent test (MJD-CMP-0001 section 4) and to examinations, demonstrating that the institution monitors the quality of its own reporting and remediates gaps before they become systemic.

## Roles and Responsibilities

- **BSA Officer (Chief Compliance Officer)**: Controlling sign-off on all SAR and no-SAR decisions; ensures deadlines are met; reports failures to the board.
- **Compliance Analyst (COMPLIANCE_OFFICER persona)**: Triages alerts, investigates cases, drafts narratives, recommends dispositions, files in BSA E-Filing.
- **SAR Review Committee**: Reviews high-dollar, insider, PEP, and terrorist-financing cases before sign-off.
- **Risk Analyst (RISK_ANALYST persona)**: Sits on the committee and integrates SAR trends into enterprise risk reporting.
- **Frontline Staff**: Refer unusual activity promptly; never tip off the subject.

## Exceptions and Escalation

No exception may shorten or waive a statutory filing deadline. Any operational exception (for example, a system outage delaying access to records) must be documented, approved by the BSA Officer, and accompanied by a manual control to preserve the deadline. A case at risk of missing a deadline is escalated to the BSA Officer at day 25 and to the board committee if a deadline is breached. Suspected tipping-off is escalated immediately to the BSA Officer and Legal.

## Related Documents

- **MJD-CMP-0001** BSA/AML Program Policy
- **MJD-CMP-0003** Currency Transaction Report (CTR) Procedure
- **MJD-CMP-0004** Transaction Monitoring Rules and Thresholds
- **MJD-OPS-0008** Sanctions (OFAC) Screening Procedure
- **MJD-RET-0003** Customer Complaint Handling Procedure
- **MJD-CMP-0008** Records Retention Schedule

## Regulatory References

- 31 CFR 1020.320, suspicious activity report requirement for banks
- 31 U.S.C. 5318(g), reporting of suspicious transactions and safe harbor
- FinCEN BSA E-Filing System guidance
- FFIEC BSA/AML Examination Manual, SAR sections

## Revision History

| Version | Effective date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2021-03-01 | BSA Officer | Initial SAR filing procedure. |
| 2.0.0 | 2023-04-15 | BSA Officer | Added SAR Review Committee and 100,000 USD escalation tier. |
| 3.0.0 | 2025-02-01 | BSA Officer | Clarified 30/60-day deadline computation and continuing-activity 120-day rule. |
| 3.1.0 | 2026-02-01 | BSA Officer | Annual review; added automated day-25 escalation control. |
