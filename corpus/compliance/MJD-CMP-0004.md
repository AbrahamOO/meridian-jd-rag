---
doc_id: MJD-CMP-0004
title: Transaction Monitoring Rules and Thresholds
department: COMPLIANCE
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: BSA Officer (Chief Compliance Officer)
allowed_roles: [COMPLIANCE_OFFICER, RISK_ANALYST]
effective_date: 2026-02-15
version: 3.0.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1020.320 (suspicious activity)", "31 U.S.C. 5318(h) (program requirement)", "FFIEC BSA/AML Examination Manual (Transaction Monitoring)"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Transaction Monitoring Rules and Thresholds

## Purpose and Scope

This standard specifies the automated transaction monitoring rules, the quantitative thresholds, the alert scoring, and the tuning governance that Meridian John Doe Financial (Meridian J.D.), a synthetic fintech for demonstration, uses to detect potentially suspicious activity. It implements the monitoring control of the BSA/AML Program Policy (MJD-CMP-0001) and feeds the SAR Filing Procedure (MJD-CMP-0002).

The standard applies to all monitored activity across deposits, payments, cards, and lending. It is binding on Compliance, which owns rule calibration and alert disposition, and on Risk, which provides independent challenge of thresholds. The concrete dollar and velocity thresholds in this document are the ground truth for monitoring; where MJD-CMP-0001 states the principle, this document states the number.

This is a CONFIDENTIAL standard because it exposes detection logic. It lists only the COMPLIANCE_OFFICER and RISK_ANALYST personas. A SOFTWARE_ENGINEER, even though clearing CONFIDENTIAL, cannot read it because engineering is not in allowed_roles.

## Definitions

- **Rule**: A deterministic or statistical condition that, when met, generates an alert.
- **Threshold**: The numeric boundary at or above which a rule fires.
- **Velocity**: The count or volume of transactions over a defined time window.
- **Baseline**: The expected activity profile established at CDD (MJD-OPS-0002) against which deviation is measured.
- **Alert score**: A weighted 0 to 100 score combining rule severity, customer risk rating, and deviation from baseline, used to prioritize triage.
- **Tuning**: The governed process of adjusting thresholds based on alert-to-SAR conversion and false-positive rates.
- **Above-the-line / below-the-line testing**: Validation that alerts at and just under a threshold are correctly captured or excluded.
- **False positive**: An alert that, on investigation, reflects legitimate, explainable activity and is closed with no action.
- **True positive**: An alert that, on investigation, reflects genuinely suspicious activity and converts to a case and potentially a SAR.
- **Alert-to-SAR conversion rate**: The proportion of alerts that ultimately result in a SAR filing. A useful but not sole indicator of rule effectiveness.
- **Rolling window**: A look-back period that moves with each new transaction, as opposed to a fixed calendar window.
- **Segment**: A grouping of customers with similar expected behavior (for example consumer checking, small business, MSB) used to set segment-specific thresholds.
- **Suppression**: A governed rule that prevents known-benign patterns from generating repeat alerts, always documented and time-bound.
- **Model**: A statistical or machine-learning component that scores or classifies activity, governed additionally under MJD-RSK-0002.

## 1. Monitoring Coverage

### 1.1 Channels Monitored

1.1.1 Monitoring covers currency transactions, wire transfers, ACH, card activity, internal book transfers, and lending disbursements and repayments.

1.1.2 Every monitored transaction carries the customer risk rating from MJD-CMP-0001 section 2.2 and the expected-activity baseline from MJD-OPS-0002 so that rules can compare actual to expected.

### 1.2 Run Cadence

1.2.1 Batch rules run at end of each business day. Real-time rules (sanctions and high-value wire holds) run synchronously at transaction time and coordinate with MJD-OPS-0008.

1.2.2 A monitoring run that fails or completes partially is treated as an incident. Compliance is notified, the run is rerun, and any delay in alert generation that risks a filing deadline is escalated to the BSA Officer. No business day's activity is allowed to go unmonitored.

### 1.3 Data Completeness and Segmentation

1.3.1 Monitoring depends on complete, accurate, and timely transaction data from every in-scope product and channel. A data-completeness reconciliation confirms daily that the volume and value of transactions feeding the monitoring system match the source systems of record. A material discrepancy is an incident.

1.3.2 Customers are assigned to behavioral segments (for example consumer checking, small business, money services business, partner-program indirect customer). Thresholds may be tuned per segment so that expected high-volume segments do not generate excessive false positives while genuinely anomalous activity still alerts.

1.3.3 The baseline for each customer is derived from the expected activity captured at CDD (MJD-OPS-0002) and is refreshed as actual behavior is observed, subject to governance so that illicit activity cannot silently become the new baseline.

## 2. Rule Library and Thresholds

### 2.1 Structuring and Threshold Avoidance

2.1.1 **R-STR-01 Cash structuring**: Three or more currency transactions by the same person, each between 8,000 USD and 10,000 USD, in the same direction within a rolling 5 business-day window. Aggregate over 9,000 USD across two business days by the same person also fires. Links to MJD-CMP-0003 and triggers SAR review.

2.1.2 **R-STR-02 Just-under CTR**: A single currency transaction between 9,500 USD and 10,000 USD where the customer has a prior just-under event in the trailing 30 days.

### 2.2 Velocity and Volume

2.2.1 **R-VEL-01 Deposit velocity**: Aggregate credits exceeding 300 percent of the 90-day baseline average within any rolling 7-day window, with a floor of 25,000 USD to suppress small-account noise.

2.2.2 **R-VEL-02 Rapid movement of funds**: Funds in and substantially out (90 percent or more) within 72 hours, aggregate over 20,000 USD. Classic layering pattern.

2.2.3 **R-VEL-03 Wire burst**: Five or more outbound wires within 24 hours, or any single outbound wire over 50,000 USD that deviates from the customer's wire baseline (MJD-OPS-0004).

### 2.3 Geography and Counterparty

2.3.1 **R-GEO-01 High-risk jurisdiction**: Any cross-border transaction with a counterparty in a high-risk or monitored jurisdiction, aggregate over 5,000 USD in a rolling 30-day window.

2.3.2 **R-CTP-01 New counterparty concentration**: More than 60 percent of monthly outbound volume to a counterparty first seen within the trailing 30 days.

### 2.4 Behavioral and Profile Deviation

2.4.1 **R-BEH-01 Dormant reactivation**: An account dormant for 180 days or more that resumes activity exceeding 10,000 USD aggregate within 7 days of reactivation.

2.4.2 **R-BEH-02 Round-number pattern**: Repeated round-number transactions (multiples of 1,000 USD) inconsistent with the baseline, five or more in a rolling 14-day window.

### 2.5A High-Risk Customer and PEP Rules

2.5A.1 **R-PEP-01 PEP activity deviation**: For a customer confirmed as a Politically Exposed Person, aggregate activity exceeding 150 percent of the established baseline within a rolling 30-day window, with a floor of 10,000 USD. PEP alerts are scored with the HIGH-risk uplift in section 3.

2.5A.2 **R-HRC-01 High-risk customer threshold compression**: For any customer rated HIGH under MJD-CMP-0001, the velocity and geography thresholds in sections 2.2 and 2.3 are compressed by 40 percent so that smaller deviations alert. HIGH-risk customers are monitored with greater sensitivity by design.

### 2.5B Funnel and Pass-Through Rules

2.5B.1 **R-FNL-01 Funnel account**: Cash or deposit credits originating from three or more distinct geographies within a rolling 14-day window, followed by concentrated withdrawals or transfers, aggregate over 15,000 USD.

2.5B.2 **R-PAS-01 Pass-through / nested activity**: For correspondent or partner-program accounts, third-party originated flows that pass through the account without an apparent business purpose, aggregate over 25,000 USD in a rolling 30-day window. Links to the nested-account risk in MJD-CMP-0001.

### 2.5 Threshold Summary Table

| Rule | Trigger | Primary threshold | Window |
|---|---|---|---|
| R-STR-01 | Cash structuring | 3+ txns of 8,000 to 10,000 USD | 5 business days |
| R-STR-02 | Just-under CTR | 9,500 to 10,000 USD with prior event | 30 days |
| R-VEL-01 | Deposit velocity | 300% of baseline, floor 25,000 USD | 7 days |
| R-VEL-02 | Rapid movement | 90% out, over 20,000 USD | 72 hours |
| R-VEL-03 | Wire burst | 5+ wires or single over 50,000 USD | 24 hours |
| R-GEO-01 | High-risk jurisdiction | over 5,000 USD aggregate | 30 days |
| R-CTP-01 | New counterparty concentration | over 60% of monthly volume | 30 days |
| R-BEH-01 | Dormant reactivation | over 10,000 USD after 180-day dormancy | 7 days |
| R-BEH-02 | Round-number pattern | 5+ round-number txns | 14 days |
| R-PEP-01 | PEP activity deviation | 150% of baseline, floor 10,000 USD | 30 days |
| R-HRC-01 | HIGH-risk threshold compression | 40% tighter on velocity/geography | as parent rule |
| R-FNL-01 | Funnel account | 3+ geographies, over 15,000 USD | 14 days |
| R-PAS-01 | Pass-through / nested | over 25,000 USD third-party flow | 30 days |

### 2.6 Rule Lifecycle and Suppression

2.6.1 Every rule has a documented owner, a stated detection objective, the typology it targets (cross-referenced to MJD-CMP-0002 section 2.1A), its threshold and window, and its current status (active, suppressed, or retired).

2.6.2 A suppression that prevents a known-benign pattern from re-alerting is itself a governed change. Suppressions are documented with the rationale, scoped as narrowly as possible, time-bound, and reviewed at expiry. A blanket suppression that would mask a typology is prohibited.

2.6.3 New rules are deployed first in a shadow mode that generates alerts for evaluation without committing them to the production queue, so that volume and quality can be assessed before activation.

## 3. Alert Scoring and Triage

3.1 Each alert receives a score from 0 to 100 = (rule base severity x 0.5) + (customer risk weight x 0.3) + (baseline deviation factor x 0.2), normalized to 100. HIGH-risk customers add a fixed 15 points.

3.2 Triage priority: score 80 to 100 triaged within 2 business days; 50 to 79 within 5 business days; below 50 within 10 business days. All triage outcomes are documented per MJD-CMP-0002 section 1.2.

3.3 An alert that converts to a case follows the SAR Filing Procedure (MJD-CMP-0002), including the 30-day and 60-day filing deadlines.

3.4 Worked scoring example. An alert from R-VEL-02 (rule base severity 70) on a HIGH-risk customer (customer risk weight 90) with a baseline deviation factor of 80 scores (70 x 0.5) + (90 x 0.3) + (80 x 0.2) = 35 + 27 + 16 = 78, plus the fixed 15-point HIGH-risk uplift, for a final 93. The alert is triaged within 2 business days. The worked computation is recorded so the triage priority is auditable.

3.5 Alert aging is tracked. An alert breaching its triage service level escalates automatically: 80 to 100 at day 2, 50 to 79 at day 5, below 50 at day 10. Aged-alert reports are reviewed by the BSA Officer weekly, because alert backlog directly threatens the downstream SAR filing deadlines.

### 3.6 Case Management Linkage

3.6.1 When an alert converts to a case, the alert score, the triggering rule, the matched typology, and the investigator's initial notes carry into the case file defined in MJD-CMP-0002 section 2.1. The initial detection date for filing-deadline purposes is set per MJD-CMP-0002 and is not the alert generation date unless triage on the same day establishes a basis for filing.

3.6.2 Multiple alerts on the same customer that reflect a single course of conduct are consolidated into one case to avoid fragmented analysis and to ensure the SAR narrative captures the full pattern.

## 4. Tuning and Validation Governance

4.1 Thresholds are reviewed at least every 12 months and after any material product or customer-base change. Tuning decisions are documented with the supporting alert-to-SAR conversion rate and false-positive rate.

4.2 Above-the-line and below-the-line testing is performed before any threshold change is promoted. Risk (RISK_ANALYST persona) provides independent challenge and signs off on threshold changes alongside the BSA Officer.

4.3 Model and rule changes that involve statistical or machine-learning components are additionally governed by the Model Risk Management Policy (MJD-RSK-0002).

### 4.4 Above-the-Line and Below-the-Line Testing

4.4.1 Before a threshold is loosened, below-the-line testing samples activity that would fall just under the proposed new threshold to confirm that genuinely suspicious activity is not being excluded. Before a threshold is tightened, above-the-line testing confirms the additional alerts are productive rather than pure noise.

4.4.2 Testing samples are statistically meaningful, documented, and reviewed by Risk. A proposed change that below-the-line testing shows would miss suspicious activity is rejected regardless of its effect on false-positive volume. Detection effectiveness takes precedence over efficiency.

### 4.5 Effectiveness Metrics and Reporting

4.5.1 The program tracks, per rule and in aggregate: alert volume, false-positive rate, true-positive rate, alert-to-SAR conversion rate, and average time-to-disposition. These metrics inform tuning but never override the requirement that suspicious activity be detected and reported.

4.5.2 A rule producing near-zero productive alerts over a sustained period is reviewed for whether it should be recalibrated or retired, with the decision documented and approved by the BSA Officer and Risk. A rule is never retired merely because it is noisy if it covers a typology with no alternative coverage.

4.5.3 Monitoring effectiveness metrics are reported to the BSA/AML Steering Committee and to the board per MJD-CMP-0001. A sustained rise in conversion-relevant backlog or a coverage gap is treated as a control deficiency.

### 4.6 Change Control and Audit Trail

4.6.1 Every threshold change, rule addition, suppression, and retirement is recorded in a versioned change log with the date, the approver, the prior and new values, and the supporting test results. The change log is retained per MJD-CMP-0008 and is evidence for the independent test and examinations.

4.6.2 Production rule configuration is access-controlled. Only authorized Compliance and Risk roles may propose changes, and changes require dual approval (BSA Officer and Risk) before promotion. Unauthorized configuration change is a security and compliance incident.

## Roles and Responsibilities

- **BSA Officer (Chief Compliance Officer)**: Owns the rule library, approves threshold changes, reports monitoring effectiveness to the board.
- **Compliance Analyst (COMPLIANCE_OFFICER persona)**: Triages and dispositions alerts, recommends tuning, performs above/below-the-line testing.
- **Risk Analyst (RISK_ANALYST persona)**: Independent challenge and sign-off on thresholds; monitors conversion and false-positive trends.

## Exceptions and Escalation

Temporarily disabling a rule requires written BSA Officer approval, a compensating manual control, and a fixed re-enable date logged in the exception register. A rule disabled without approval is a control failure escalated to the board. Alerts scoring 80 or above that cannot be triaged within the 2-business-day service level are escalated to the BSA Officer.

## Related Documents

- **MJD-CMP-0001** BSA/AML Program Policy
- **MJD-CMP-0002** Suspicious Activity Report (SAR) Filing Procedure
- **MJD-CMP-0003** Currency Transaction Report (CTR) Procedure
- **MJD-OPS-0002** Customer Due Diligence (CDD) Standard
- **MJD-OPS-0004** Wire Transfer Operations Runbook
- **MJD-OPS-0008** Sanctions (OFAC) Screening Procedure
- **MJD-RSK-0002** Model Risk Management Policy (SR 11-7)
- **MJD-CMP-0008** Records Retention Schedule

## Regulatory References

- 31 CFR 1020.320, suspicious activity report requirement
- 31 U.S.C. 5318(h), anti-money-laundering program requirement
- FFIEC BSA/AML Examination Manual, transaction monitoring and tuning sections

## Revision History

| Version | Effective date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2021-04-01 | BSA Officer | Initial rule library and thresholds. |
| 2.0.0 | 2023-06-01 | BSA Officer | Added alert scoring model and triage service levels. |
| 2.5.0 | 2025-02-15 | BSA Officer | Added wire-burst and new-counterparty rules; formalized tuning governance. |
| 3.0.0 | 2026-02-15 | BSA Officer | Annual review; recalibrated velocity floors and added MJD-RSK-0002 model linkage. |
