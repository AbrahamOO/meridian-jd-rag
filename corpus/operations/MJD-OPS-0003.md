---
doc_id: MJD-OPS-0003
title: Enhanced Due Diligence (EDD) Procedure
department: OPERATIONS
doc_type: PROCEDURE
classification: CONFIDENTIAL
owner_role: Head of Financial Crimes Operations
allowed_roles: [OPERATIONS_ANALYST, COMPLIANCE_OFFICER, RISK_ANALYST]
effective_date: 2025-11-01
version: 2.4.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1010.610", "FinCEN CDD Rule 31 CFR 1010.230", "FFIEC BSA/AML Examination Manual", "31 USC 5318(i)"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Enhanced Due Diligence (EDD) Procedure

## Purpose and Scope

This procedure defines the Enhanced Due Diligence (EDD) that Meridian John Doe Financial (Meridian J.D.) applies to higher-risk customers and transactions. EDD is the heightened-scrutiny layer that sits above standard Customer Due Diligence (MJD-OPS-0002). It exists to mitigate the elevated money-laundering, terrorist-financing, and sanctions-evasion risks presented by certain customers, products, geographies, and activity patterns.

This procedure applies to all customer relationships that meet any EDD trigger in Section 1, and to all Operations Analysts, Compliance Officers, and Risk Analysts who perform, review, or oversee EDD. Because EDD reveals risk thresholds and screening logic, this document is classified CONFIDENTIAL and is not visible to Branch Staff.

## Definitions

- **EDD Trigger.** A customer, product, geography, ownership, or activity condition that mandates EDD.
- **Source of Funds (SoF).** The origin of the specific funds used in a transaction or deposit.
- **Source of Wealth (SoW).** The origin of the customer's overall net worth and how it was accumulated.
- **Politically Exposed Person (PEP).** An individual entrusted with a prominent public function, their immediate family, and known close associates.
- **High-Risk Jurisdiction.** A country identified as higher risk in the bank's country-risk model, including FATF-listed jurisdictions and jurisdictions subject to comprehensive sanctions.
- **EDD File.** The consolidated documentation package supporting an EDD decision, retained per Section 6.
- **Beneficial Owner.** Any natural person who, directly or indirectly, owns 25 percent or more of the equity interests of a legal-entity customer, plus the single individual with significant managerial control, consistent with MJD-OPS-0002.
- **Control Owner.** The named accountable individual responsible for the design and operating effectiveness of a specific control step in this procedure, as listed in Section 7.
- **Service Level Agreement (SLA).** The maximum elapsed business time within which a defined EDD task must be completed, measured from the trigger event to task closure in the case management system.
- **Trigger Event.** The dated, system-recorded moment at which an EDD condition in Section 1 first becomes true for a relationship.
- **Re-trigger Window.** The 15-business-day period within which EDD must be commenced after a relationship crosses any mandatory trigger during the life of the account.
- **Risk-Acceptance Memorandum (RAM).** A documented, time-bound decision by an approved authority to continue a relationship that carries an unresolved residual risk, recorded in the EDD file.
- **Adverse Media.** Credible negative information from independent sources concerning financial crime, sanctions, corruption, fraud, or predicate offenses associated with a customer or related party.

## 1. EDD Triggers

### 1.1 Mandatory triggers

EDD is mandatory when any of the following is present:

1. A Customer Risk Rating of High under MJD-OPS-0002.
2. A politically exposed person as customer, beneficial owner, or controlling individual.
3. A money services business, virtual-asset service provider, or other higher-risk business type.
4. A cash-intensive business with monthly cash activity exceeding the cash-intensive review level.
5. Any beneficial owner, controlling party, or material counterparty located in a high-risk jurisdiction.
6. A new corporate (legal-entity) account whose expected or actual aggregate annual transaction volume meets or exceeds the monetary trigger in Section 1.2.
7. Ownership structures that cannot be reasonably traced to natural persons.

### 1.2 Monetary trigger for new corporate accounts

A new corporate account is subject to mandatory EDD when its expected aggregate annual transaction volume, or its actual trailing volume measured over any rolling 12-month window, **meets or exceeds 5,000,000 US dollars (USD 5,000,000)**. This threshold is evaluated at onboarding using the customer's stated expected activity and re-evaluated continuously against actual activity. Crossing the USD 5,000,000 threshold at any time triggers EDD within 15 business days even if no other trigger is present.

Supplementary monetary triggers, applied independently of the USD 5,000,000 annual-volume trigger:

| Condition | EDD trigger level |
|---|---|
| Single inbound or outbound international wire, new corporate account | 250,000 USD or more |
| Aggregate cash deposits, any 30-day window, business account | 1,000,000 USD or more |
| Single transaction with a counterparty in a high-risk jurisdiction | 100,000 USD or more |

### 1.3 Discretionary triggers

A Compliance Officer or Risk Analyst may designate any relationship for EDD based on adverse media, unusual activity, or examiner feedback, regardless of monetary thresholds. Discretionary designations are recorded with a written rationale in the case management system and are subject to the same SLAs, refresh cadence, and de-escalation rules as mandatory designations.

### 1.4 Trigger detection and intake

1.4.1 Triggers are detected through three channels: onboarding intake at account opening, automated threshold monitoring against actual activity, and manual referral from Branch Staff, Compliance, Risk, or Legal.

1.4.2 The trigger-detection engine evaluates each corporate relationship nightly against the thresholds in Sections 1.1 and 1.2. When a threshold is crossed, the engine creates an EDD case, stamps the Trigger Event date, and assigns the case to the EDD work queue.

1.4.3 Each EDD case is risk-tiered at intake to determine SLA and approval routing.

| Tier | Definition | Examples |
|---|---|---|
| EDD-1 Critical | PEP, unresolved sanctions exposure, or opaque ownership | Foreign PEP, nominee-layered structure |
| EDD-2 Elevated | Volume-trigger corporate, money services business, virtual-asset, or high-risk jurisdiction nexus | USD 5,000,000 annual-volume corporate, MSB |
| EDD-3 Standard EDD | High Customer Risk Rating or discretionary designation without EDD-1 or EDD-2 conditions | High-rated domestic corporate |

1.4.4 Where multiple conditions apply, the case is assigned the highest applicable tier. A single relationship may carry more than one trigger; all triggers are recorded and each must be independently cleared before de-escalation under Section 4.2.

### 1.5 Onboarding SLA matrix

EDD must be commenced within the Re-trigger Window of 15 business days for in-life triggers, and at onboarding for new relationships. Completion SLAs are measured from the Trigger Event to documented senior approval.

| Tier | Commence EDD | Complete EDD file | Senior approval |
|---|---|---|---|
| EDD-1 Critical | 1 business day | 10 business days | Head of Financial Crimes Operations |
| EDD-2 Elevated | 3 business days | 20 business days | Compliance Officer, plus Head of Financial Crimes Operations for volume-trigger and PEP |
| EDD-3 Standard EDD | 5 business days | 30 business days | Compliance Officer |

A case that cannot be completed within its SLA is escalated under Section 5 and may not be released to normal activity until cleared or covered by a Risk-Acceptance Memorandum.

## 2. EDD Steps

### 2.1 Source of funds and source of wealth

2.1.1 For every EDD customer, document and corroborate the source of funds for opening and ongoing activity. Corroboration follows a tiered evidence standard: at least one independent document for EDD-3, two independent documents for EDD-2, and two independent documents plus a documented analyst narrative reconciling expected activity to stated funds for EDD-1.

2.1.2 For PEPs and customers crossing the USD 5,000,000 annual-volume trigger, additionally document and corroborate the source of wealth with independent evidence (for example, audited financials, sale-of-business documentation, or tax records). Self-attestation alone is insufficient.

2.1.3 The following evidence matrix sets the acceptable corroboration by funds category. At least one item from the relevant row is required, and items must be dated within the stated validity window.

| Funds or wealth category | Acceptable corroborating evidence | Validity window |
|---|---|---|
| Business operating revenue | Audited financial statements, management accounts, bank statements | 12 months |
| Sale of a business or asset | Executed sale agreement, completion statement, escrow release | 36 months |
| Investment proceeds | Brokerage statements, fund redemption notices, capital account statements | 12 months |
| Inheritance or gift | Probate grant, will, gift deed, donor identification | No expiry, event-based |
| Salary or director remuneration | Pay records, employment contract, tax filings | 12 months |
| Loan or credit facility | Executed facility agreement, lender confirmation | Life of facility |

2.1.4 Worked example. A new freight-forwarding corporate states expected annual throughput of USD 7,200,000, which exceeds the USD 5,000,000 annual-volume trigger and routes the case to EDD-2 with Head of Financial Crimes Operations approval. The Operations Analyst obtains two years of audited financials and the prior year tax filing, reconciles stated revenue of USD 6,900,000 to bank statement inflows within a 10 percent tolerance, documents source of wealth from retained earnings, and records the reconciliation narrative in the EDD file. The residual variance of 4.3 percent is within tolerance and is noted but does not require escalation.

2.1.5 Where reconciliation variance exceeds 15 percent, the analyst documents the discrepancy, requests supplementary evidence, and refers the case to a Compliance Officer if the variance cannot be explained within the applicable SLA.

### 2.2 Enhanced beneficial-ownership analysis

2.2.1 Trace ownership fully to natural persons, including through intermediate entities and nominee arrangements. Where a layer is opaque, escalate per Section 5.

2.2.2 The analyst constructs an ownership map that records, for each layer, the entity name, jurisdiction of formation, percentage held, and the corroborating registry or document. Tracing continues until every natural person at or above the 25 percent beneficial-ownership threshold is identified, plus the controlling individual.

2.2.3 The following decision table governs the ownership outcome.

| Ownership condition | Required action | Outcome |
|---|---|---|
| All natural persons identified, no high-risk nexus | Document map, screen each owner | Proceed to approval |
| Owner in a high-risk jurisdiction | Apply Section 1.2 transaction trigger, expand screening | Proceed with EDD-2 controls |
| Nominee or bearer-share arrangement | Obtain nominee declaration and underlying principal identity | Proceed only if principal corroborated, else escalate |
| Layer cannot be traced to natural persons | Escalate to Compliance under Section 5 | Decline or Risk-Acceptance Memorandum only |

2.2.4 Each identified beneficial owner and controlling individual is screened for sanctions, PEP status, and adverse media before approval. A confirmed PEP among beneficial owners elevates the case to EDD-1 regardless of the original tier.

### 2.3 Senior approval

2.3.1 Onboarding or continuing an EDD relationship requires documented approval by a Compliance Officer.

2.3.2 PEP relationships and relationships crossing the USD 5,000,000 annual-volume trigger additionally require Head of Financial Crimes Operations approval.

2.3.3 Approval authority is tiered to prevent self-approval and to match risk. No individual may approve a case they prepared.

| Case condition | Preparer | First approver | Final approver |
|---|---|---|---|
| EDD-3 Standard EDD | Operations Analyst | Compliance Officer | Compliance Officer |
| EDD-2 volume-trigger or business-type | Operations Analyst | Compliance Officer | Head of Financial Crimes Operations |
| EDD-1 PEP or opaque ownership | Operations Analyst | Compliance Officer | Head of Financial Crimes Operations |
| Risk-Acceptance Memorandum | Compliance Officer | Head of Financial Crimes Operations | Chief Compliance Officer |

2.3.4 Approval records capture the approver identity, date, the triggers reviewed, the residual-risk statement, and any conditions imposed (for example, deposit-only restriction or reduced limits). Approval conditions are entered into the account management system and monitored by the Operations Analyst.

### 2.4 Negative-news and sanctions screening

2.4.1 Perform expanded adverse-media screening and re-run sanctions screening per MJD-OPS-0008 at a heightened frequency. Any potential sanctions match halts the relationship pending resolution.

2.4.2 Adverse-media screening covers the customer, all beneficial owners, controlling individuals, and material counterparties. Screening uses structured search terms across financial-crime, sanctions, corruption, fraud, and predicate-offense categories and is documented with the search date, sources reviewed, and disposition of each hit.

2.4.3 Adverse-media hits are dispositioned on a four-point scale.

| Disposition | Criteria | Action |
|---|---|---|
| No match | Different individual or entity confirmed | Document and close |
| Match, not material | Confirmed but unrelated to financial crime | Note in EDD file, proceed |
| Match, material, mitigated | Financial-crime nexus with credible mitigating context | Compliance Officer review and documented rationale |
| Match, material, unresolved | Financial-crime nexus without mitigation | Escalate under Section 5, consider SAR and exit |

2.4.4 Sanctions re-screening frequency for EDD relationships is daily against the consolidated watchlist load and immediately upon any list update affecting a customer's jurisdiction or counterparties. A potential true match is referred to MJD-OPS-0008 for adjudication within four business hours, and outbound payments to the affected party are suspended during adjudication.

### 2.5 Risk-based limits and conditions

2.5.1 Upon approval, EDD relationships may be assigned transaction limits proportionate to corroborated expected activity. A volume-trigger corporate is assigned a monitoring ceiling at 120 percent of its corroborated expected annual volume; sustained activity above the ceiling generates an alert and a documentation refresh.

2.5.2 New EDD relationships that opened under a documentation exception are restricted to deposit-only activity until the exception is cleared, consistent with the Exceptions and Escalation section.

## 3. Enhanced Ongoing Monitoring

### 3.1 Monitoring intensity

3.1.1 EDD relationships are monitored at a heightened sensitivity in the transaction-monitoring system (MJD-CMP-0004), with lowered alert thresholds and a mandatory monthly manual review for the highest-risk subset.

3.1.2 EDD relationships are flagged in the monitoring system so that scenario thresholds applied to them are reduced relative to standard customers. The reduction is calibrated by the Risk Analyst and validated annually.

| Scenario family | Standard threshold reference | EDD threshold treatment |
|---|---|---|
| Structuring and rapid movement | Baseline per MJD-CMP-0004 | Reduced by 40 percent |
| High-risk-jurisdiction transfers | 100,000 USD per Section 1.2 | Reduced to 50,000 USD for EDD-1 |
| Large single international wire | 250,000 USD per Section 1.2 | Reduced to 150,000 USD for EDD-1 and EDD-2 |
| Aggregate cash, 30-day | 1,000,000 USD per Section 1.2 | Reduced to 500,000 USD |

3.1.3 The Section 1.2 trigger levels remain the authoritative onboarding and EDD-trigger thresholds. The reduced figures in 3.1.2 are monitoring-alert sensitivities applied after a relationship is already in EDD and do not replace or contradict the Section 1.2 trigger levels.

### 3.2 Alert handling SLA

Alerts on EDD relationships are worked ahead of standard alerts.

| Tier | Alert acknowledgment | Alert disposition |
|---|---|---|
| EDD-1 Critical | 1 business day | 5 business days |
| EDD-2 Elevated | 2 business days | 10 business days |
| EDD-3 Standard EDD | 3 business days | 15 business days |

An alert that cannot be dispositioned within SLA is escalated to a Compliance Officer with a documented interim risk note.

### 3.2 Review cadence

| EDD population | Manual review cadence |
|---|---|
| PEP and sanctions-adjacent | Monthly |
| Money services business and virtual-asset | Quarterly |
| Volume-trigger corporate (USD 5,000,000+) | Quarterly |
| Other EDD | Semi-annually |

## 4. Periodic Reassessment

### 4.1 Full EDD refresh

4.1.1 A full EDD refresh is performed at least every 12 months and on any trigger event. The refresh re-corroborates SoF and SoW, re-traces ownership, and re-confirms senior approval.

4.1.2 Refresh due dates are scheduled by tier so that the highest-risk relationships are reviewed more frequently than the minimum.

| Tier | Refresh interval | Event-driven refresh |
|---|---|---|
| EDD-1 Critical | 6 months | On any new adverse media, ownership change, or PEP status change |
| EDD-2 Elevated | 12 months | On crossing a new Section 1.2 trigger or a 25 percent activity increase |
| EDD-3 Standard EDD | 12 months | On Customer Risk Rating change |

4.1.3 A refresh is opened 30 calendar days before its due date and must be completed by the due date. An overdue refresh places the relationship into a restricted state with new outbound activity suspended until the refresh is closed, unless a Compliance Officer grants a documented short extension not exceeding 15 business days.

### 4.2 De-escalation

4.2.1 A relationship may exit EDD only with Compliance Officer approval after two consecutive clean reassessments and the removal of every applicable trigger. De-escalation is documented in the EDD file.

4.2.2 De-escalation requires all of the following: no open alerts or SARs, no unresolved adverse media, removal of every Section 1 trigger, and a documented Compliance Officer rationale. A relationship that previously crossed the USD 5,000,000 annual-volume trigger may de-escalate only if trailing 12-month actual volume has remained below USD 5,000,000 across both clean reassessment cycles.

4.2.3 De-escalated relationships revert to standard Customer Due Diligence under MJD-OPS-0002 and remain subject to re-triggering under the 15-business-day Re-trigger Window if any condition recurs.

## 5. Escalation and Exit

5.1 An EDD relationship that cannot be corroborated, that presents unresolved sanctions exposure, or that exhibits activity consistent with money laundering is referred to Compliance for a SAR determination under MJD-CMP-0002 and may be exited.

5.2 Exit decisions are coordinated with Legal and documented, including any continuing-monitoring obligations during the wind-down.

5.3 Escalation routing follows a defined ladder with time bounds measured from the escalation trigger.

| Escalation condition | Routed to | Response SLA |
|---|---|---|
| SLA breach on EDD-3 or EDD-2 case | Compliance Officer | 2 business days |
| Untraceable ownership layer | Compliance Officer, then Head of Financial Crimes Operations | 3 business days |
| Potential true sanctions match | MJD-OPS-0008 sanctions desk | 4 business hours |
| Activity consistent with money laundering | Compliance Officer for SAR determination under MJD-CMP-0002 | 1 business day |
| Request to continue with unresolved residual risk | Risk-Acceptance Memorandum, Chief Compliance Officer | 5 business days |

5.4 A Risk-Acceptance Memorandum is permitted only where exit is not immediately feasible and the residual risk is bounded. A RAM states the specific unresolved risk, the compensating controls (for example, reduced limits, deposit-only restriction, or increased review frequency), the expiry date not exceeding 90 days, and the conditions for renewal or exit. A RAM may never be used to waive the USD 5,000,000 annual-volume mandatory trigger or to override a confirmed sanctions match.

5.5 Worked example. An EDD-1 relationship presents a third ownership layer in a jurisdiction whose registry does not disclose beneficial owners. The analyst obtains a nominee declaration but cannot independently corroborate the principal within the 10-business-day EDD-1 SLA. The case is escalated to a Compliance Officer within 1 business day of the SLA approaching breach, then to the Head of Financial Crimes Operations. Compliance determines the residual risk is not bounded, declines a RAM, refers the matter for a SAR determination under MJD-CMP-0002, and initiates exit coordinated with Legal under Section 5.2.

## 6. Documentation and Retention

6.1 The EDD file consolidates: triggers met, SoF and SoW evidence, ownership analysis, screening results, senior approvals, monitoring reviews, and reassessments.

6.2 EDD files are CONFIDENTIAL and retained for five years after account closure per MJD-CMP-0008, with access limited to Operations, Compliance, and Risk.

6.3 Each EDD file is assembled against a standard index so that an examiner or independent reviewer can locate every required element.

| Index item | Required content | Responsible role |
|---|---|---|
| Trigger record | Trigger Event date, tier, all applicable triggers | Operations Analyst |
| SoF and SoW evidence | Documents per Section 2.1 matrix, reconciliation narrative | Operations Analyst |
| Ownership map | Layered structure to natural persons, registry references | Operations Analyst |
| Screening pack | Sanctions, PEP, and adverse-media results with dispositions | Operations Analyst |
| Approval record | Approver identity, date, conditions, residual-risk statement | Compliance Officer |
| Monitoring log | Alert dispositions and periodic review notes | Operations Analyst |
| Reassessment record | Refresh outcomes and de-escalation rationale | Compliance Officer |

6.4 EDD files are subject to second-line quality assurance sampling. The Risk function reviews a risk-weighted sample of at least 10 percent of EDD-1 cases, 5 percent of EDD-2 cases, and 2 percent of EDD-3 cases each quarter, records defects against the Section 6.3 index, and tracks remediation to closure within 30 business days.

## 7. Control Ownership

7.1 Each control step in this procedure has a single accountable Control Owner responsible for its design and operating effectiveness.

| Control | Control Owner | Operated by | Frequency |
|---|---|---|---|
| Trigger detection engine | Risk Analyst | Automated, monitored by Operations | Nightly |
| Trigger tiering and intake | Operations Analyst | Operations | Per case |
| SoF and SoW corroboration | Operations Analyst | Operations | Per case and per refresh |
| Beneficial-ownership tracing | Operations Analyst | Operations | Per case and per refresh |
| Sanctions and adverse-media screening | Compliance Officer | Operations and sanctions desk | Daily and per case |
| Senior approval and conditions | Compliance Officer | Compliance | Per case |
| Enhanced monitoring sensitivity | Risk Analyst | Automated, reviewed by Operations | Continuous |
| Periodic refresh and de-escalation | Compliance Officer | Operations and Compliance | Per cadence |
| Quality assurance sampling | Risk Analyst | Risk | Quarterly |
| Procedure ownership and metrics | Head of Financial Crimes Operations | Financial Crimes Operations | Continuous |

7.2 Control Owners attest quarterly that their controls operated as designed and report exceptions, defect counts, and remediation status to the Head of Financial Crimes Operations for inclusion in EDD population metrics.

7.3 Key indicators reported each quarter include: EDD population by tier, percentage of cases completed within SLA, count of overdue refreshes, open RAMs and their expiry status, sanctions adjudication turnaround, and quality assurance defect rate. A sustained SLA completion rate below 90 percent for any tier triggers a documented corrective action plan owned by the Head of Financial Crimes Operations.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Operations Analyst | Execute EDD steps, gather SoF and SoW evidence, run heightened monitoring reviews, maintain the EDD file |
| Compliance Officer | Approve EDD onboarding and continuation, adjudicate escalations, own SAR determinations |
| Risk Analyst | Designate discretionary EDD, validate the country-risk and trigger models, consume EDD data for enterprise reporting |
| Head of Financial Crimes Operations | Own this procedure, approve PEP and volume-trigger relationships, own SLA corrective action, report EDD population metrics |
| Chief Compliance Officer | Approve Risk-Acceptance Memoranda, set overall risk appetite, sponsor examiner and audit engagement |

## Exceptions and Escalation

- No exceptions are permitted to the USD 5,000,000 annual-volume mandatory trigger; the trigger may only be satisfied or the relationship declined.
- A time-bound exception to a documentation step (for example, awaiting audited financials) requires Compliance Officer approval, may not exceed 30 days, and restricts the account to deposit-only activity in the interim.
- Suspected sanctions evasion is escalated immediately under MJD-OPS-0008 and MJD-CMP-0002.

## Related Documents

- MJD-OPS-0002 Customer Due Diligence (CDD) Standard
- MJD-OPS-0001 Customer Identification Program (CIP) Procedure
- MJD-OPS-0008 Sanctions (OFAC) Screening Procedure
- MJD-CMP-0004 Transaction Monitoring Rules and Thresholds
- MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure
- MJD-RSK-0007 Fraud Risk Management Procedure

## Regulatory References

- 31 CFR 1010.610 (due diligence for correspondent and private banking)
- FinCEN Customer Due Diligence Rule, 31 CFR 1010.230
- FFIEC BSA/AML Examination Manual, Enhanced Due Diligence
- 31 USC 5318(i)

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2019-01-20 | Head of Financial Crimes Operations | Initial EDD procedure |
| 2.0.0 | 2021-10-05 | Head of Financial Crimes Operations | Added PEP and source-of-wealth requirements |
| 2.1.0 | 2022-12-01 | Head of Financial Crimes Operations | Introduced USD 5,000,000 corporate annual-volume trigger |
| 2.2.0 | 2023-11-15 | Head of Financial Crimes Operations | Added supplementary monetary trigger table |
| 2.3.0 | 2024-10-10 | Head of Financial Crimes Operations | Heightened monitoring cadence table |
| 2.4.0 | 2025-11-01 | Head of Financial Crimes Operations | Clarified de-escalation criteria and 15-day re-trigger window; expanded procedural detail with tiering, SLA matrices, evidence and decision tables, control ownership, escalation ladder, and quality assurance |
