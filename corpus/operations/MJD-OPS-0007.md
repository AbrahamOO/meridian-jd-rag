---
doc_id: MJD-OPS-0007
title: Transaction Limits and Dual-Approval Matrix
department: OPERATIONS
doc_type: STANDARD
classification: INTERNAL
owner_role: Head of Payment Operations
allowed_roles: [OPERATIONS_ANALYST, BRANCH_STAFF, FINANCE_CONTROLLER]
effective_date: 2026-01-15
version: 3.0.0
review_cycle_months: 12
regulatory_refs: ["UCC Article 4A", "FFIEC Wholesale Payment Systems Guidance", "31 CFR 1010.410", "Sarbanes-Oxley Act Section 404"]
supersedes: MJD-OPS-0009
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Transaction Limits and Dual-Approval Matrix

## Purpose and Scope

This standard establishes the current transaction limits and dual-approval requirements that govern outbound payments and account-level activity at Meridian John Doe Financial (Meridian J.D.). It is the authoritative source for the limit figures and approval thresholds referenced operationally by the Wire Transfer Operations Runbook (MJD-OPS-0004) and the Account Onboarding Workflow (MJD-OPS-0005).

This standard applies to all payment channels and to Operations Analysts, Branch Staff, and Finance Controllers who prepare, approve, or oversee transactions. It is binding bank-wide. This version (3.0.0, effective 2026-01-15) supersedes MJD-OPS-0009 (the 2024 Edition); the figures in this document are current and authoritative. Where this document and MJD-OPS-0009 differ, this document governs.

## Definitions

- **Dual Approval (Maker-Checker).** A control requiring one individual to prepare a transaction and a different authorized individual to approve and release it.
- **Triple Approval.** Dual approval plus an additional approval at the Finance Controller level.
- **Daily Aggregate.** The sum of an account's outbound transactions of a given type within one business day.
- **Limit.** A maximum value permitted per transaction or per aggregate window.
- **Approval Threshold.** The value at or above which a heightened approval requirement applies.
- **Single-Approval Ceiling.** The value below which one authorized individual may both prepare and release a transaction.
- **Maker.** The individual who prepares and submits a transaction for approval.
- **Checker.** The distinct individual who reviews and releases a transaction prepared by the maker.
- **Account Tier.** The product-and-risk classification that determines an account's daily aggregate limits.
- **Override.** A documented, time-boxed, Finance-Controller-approved increase above a standing limit.
- **Standard Owner.** The Head of Payment Operations, accountable for the design and currency of this matrix.

## 1. Approval-Threshold Matrix (Current)

The matrix below is the authoritative current set of approval thresholds. Each band is expressed as a single-approval ceiling and the value at which dual or triple approval becomes mandatory. All values are in US dollars and apply per single transaction unless an aggregation rule applies.

### 1.1 Wire transfers

| Transaction | Single-approval ceiling | Dual approval required at | Triple approval required at |
|---|---|---|---|
| Domestic Fedwire | Below 100,000 USD | 100,000 USD or more | 1,000,000 USD or more |
| International SWIFT | Below 50,000 USD | 50,000 USD or more | 500,000 USD or more |
| Book transfer | Below 250,000 USD | 250,000 USD or more | 2,000,000 USD or more |

The current **daily wire limit before dual approval is 100,000 USD** for domestic Fedwire. A single domestic wire at or above 100,000 USD requires dual approval; at or above 1,000,000 USD it requires triple approval including a Finance Controller.

1.1.1 **Aggregation rule.** The thresholds apply per single transaction and, separately, per account daily aggregate. Multiple same-day domestic wires from one account whose aggregate reaches 100,000 USD trigger dual approval on the transaction that crosses the threshold and on every subsequent same-day wire, preventing threshold splitting.

1.1.2 **Currency conversion.** For an international wire denominated in a foreign currency, the USD-equivalent at the day's posted conversion rate determines the applicable threshold band.

1.1.3 **Worked example.** An Operations Analyst prepares a 120,000 USD domestic Fedwire. Because 120,000 USD is at or above 100,000 USD, the analyst (maker) routes it to a separate authorized checker who reviews instructions, callback evidence, and sanctions clearance, then releases it. A second 90,000 USD wire from the same account later that day brings the daily aggregate to 210,000 USD; that second wire also requires dual approval under the aggregation rule even though, standing alone, it is below 100,000 USD.

### 1.2 ACH and other electronic transfers

| Transaction | Single-approval ceiling | Dual approval required at |
|---|---|---|
| ACH credit origination, per file | Below 250,000 USD | 250,000 USD or more |
| External account transfer (push) | Below 50,000 USD | 50,000 USD or more |
| Bill pay, per item | Below 25,000 USD | 25,000 USD or more |

### 1.3 Cash and branch transactions

| Transaction | Threshold for supervisor approval |
|---|---|
| Cash withdrawal, branch | 10,000 USD or more |
| Cash advance | 5,000 USD or more |
| Official check issuance | 50,000 USD or more |

1.3.1 A branch cash withdrawal at or above 10,000 USD that involves currency is also subject to Currency Transaction Report obligations handled under the Compliance CTR procedure; the supervisor approval here is an operational control and does not replace any regulatory reporting.

### 1.4 Approval-authority matrix

The following roles hold approval authority at each level. The system enforces that the releasing approver holds at least the required authority and is distinct from the maker.

| Approval level | Minimum approver authority |
|---|---|
| Single approval | Operations Analyst or trained Branch Staff |
| Dual approval (checker) | Senior Operations Analyst or Operations supervisor |
| Triple approval (third) | Finance Controller |
| Override approval | Finance Controller |

## 2. Per-Account Daily Limits (Current)

| Account tier | Daily outbound wire aggregate | Daily ACH aggregate | Daily external transfer aggregate |
|---|---|---|---|
| Consumer standard | 50,000 USD | 25,000 USD | 25,000 USD |
| Consumer premier | 250,000 USD | 100,000 USD | 100,000 USD |
| Business standard | 1,000,000 USD | 500,000 USD | 250,000 USD |
| Business commercial | 10,000,000 USD | 5,000,000 USD | 2,000,000 USD |

Limits above a tier ceiling require a documented limit increase approved by the Finance Controller and are reviewed annually.

### 2.1 Tier assignment

2.1.1 The account tier is set at onboarding (MJD-OPS-0005) based on product and Customer Risk Rating, and is revisited at each CDD refresh under MJD-OPS-0002.

2.1.2 A higher tier than the product default requires Finance Controller approval and documented business justification. A tier downgrade follows a sustained reduction in activity or a risk-rating increase.

### 2.2 Daily-aggregate enforcement

2.2.1 The system tracks each account's running daily aggregate by transaction type and blocks any transaction that would breach the tier limit unless an active override is in place.

2.2.2 A blocked transaction is surfaced to the originator with the limit and the override path; it is never silently rejected.

2.2.3 **Business-day boundary.** The daily aggregate resets at the start of each business day in US Eastern time. Transactions submitted after the applicable rail cutoff but before the calendar-day boundary count against the next business day's aggregate, consistent with the cutoff times in MJD-OPS-0004.

2.2.4 **Holiday handling.** On a Federal Reserve holiday, domestic wire and ACH activity is queued for the next business day and counts against that day's aggregate. Book transfers continue to settle and count against the current calendar day.

### 2.3 System enforcement and controls

2.3.1 The thresholds and tier limits are configured in the payment platform as enforced controls, not advisory guidance. A maker cannot release a transaction above a single-approval ceiling; the system routes it for the required approvals.

2.3.2 Configuration of thresholds and tier limits is itself a controlled change requiring joint Head of Payment Operations and Finance Controller approval and is logged for audit. No individual can both change a limit and transact against the change.

2.3.3 The single-approval ceilings, dual-approval thresholds, and triple-approval thresholds are version-pinned to this document. A discrepancy between the configured values and this matrix is a control incident escalated to the Head of Payment Operations.

## 3. Maker-Checker Separation Rules

3.1 The maker and the checker must be distinct individuals. The system enforces this; an attempt to self-approve is rejected and logged.

3.2 For triple-approval transactions, all three approvers must be distinct, and the third must hold Finance Controller authority.

3.3 Callback verification (MJD-OPS-0004 Section 2.2) is a separate control and is required independently of dual approval where the runbook specifies.

3.4 **Segregation evidence.** Each approval records the approver identity, role, timestamp, and the value approved. These records are the SOX evidence consumed under MJD-FIN-0005 and are immutable once written.

3.5 **Emergency approval.** Where a required approver is unavailable for a time-critical payment, an alternate of equal or higher authority may act; the substitution is logged with the reason. An emergency approval never collapses two approval roles into one person.

## 4. Limit Overrides and Temporary Increases

4.1 A temporary limit increase (for example, a customer's one-time large acquisition payment) is requested in writing, approved by the Finance Controller, time-boxed to a stated effective window, and reverts automatically.

4.2 Each override is logged with requester, approver, value, and expiry, and is reportable for SOX control testing under MJD-FIN-0005.

### 4.3 Override workflow

| Step | Actor | Control |
|---|---|---|
| Request | Operations Analyst or RM | Written justification and requested value and window |
| Risk check | Operations Analyst | Confirm CDD currency and no open sanctions or fraud flag |
| Approval | Finance Controller | Approve, modify, or deny; record rationale |
| Activation | System | Apply with hard expiry |
| Reversion | System | Auto-revert at expiry; no manual extension without a new request |

4.3.1 An override may not exceed the next tier ceiling without a documented exception co-approved by the Head of Payment Operations.

## 5. Governance and Review

5.1 This matrix is reviewed at least annually and on any material change in payment risk. Changes are approved by the Head of Payment Operations and the Finance Controller jointly.

5.2 The superseded prior edition (MJD-OPS-0009) is retained for historical reference only and must not be used to authorize current transactions.

5.3 **Change log of figures.** Version 3.0.0 raised the domestic Fedwire dual-approval threshold from the prior 50,000 USD (MJD-OPS-0009) to 100,000 USD, raised the domestic triple-approval threshold from 500,000 USD to 1,000,000 USD, and increased every per-account tier ceiling. Any future change to a figure in this matrix is recorded in the revision history with the prior and new value.

5.4 **Control testing.** The Finance Controller tests the limit and approval controls at least quarterly by sampling released transactions for correct approval levels and distinct approvers, and reports results under MJD-FIN-0005 and MJD-RSK-0003.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Operations Analyst | Prepare transactions within limits, route for dual or triple approval, apply override expiry |
| Branch Staff | Obtain supervisor approval for cash thresholds, originate within account daily limits |
| Finance Controller | Provide triple-approval authority, approve limit increases and overrides, own SOX evidence for limit controls |
| Head of Payment Operations | Own this standard, set thresholds, lead the annual review |

## Exceptions and Escalation

- No transaction may exceed an account daily limit without a documented, time-boxed override approved by the Finance Controller.
- Self-approval attempts are hard-blocked and escalated as control violations.
- A suspected control bypass is escalated to the Finance Controller and to Compliance, and is logged for audit under MJD-FIN-0005.
- The dual-approval and triple-approval thresholds are non-waivable; an override raises a limit, it never removes an approval requirement.
- Use of MJD-OPS-0009 figures to authorize a current transaction is a control violation; only this matrix is authoritative.

### Escalation ladder

| Trigger | First escalation | Second escalation |
|---|---|---|
| Attempted self-approval | Operations supervisor | Finance Controller and Compliance |
| Threshold-splitting pattern | Operations supervisor | Compliance for SAR evaluation (MJD-CMP-0002) |
| Override beyond next tier | Finance Controller | Head of Payment Operations |
| Repeated limit breaches on one account | Finance Controller | Risk (MJD-RSK-0003) |

## 4A. Approval Service Levels

4A.1 Approvals are time-sensitive because they gate payment release against rail cutoffs. The following targets apply during business hours.

| Approval type | Target turnaround |
|---|---|
| Dual approval, standard wire | Within 30 minutes of maker submission |
| Triple approval, high-value wire | Within 60 minutes of dual approval |
| Override request decision | Within 2 hours of a complete request |
| Emergency alternate approval | Without undue delay, documented |

4A.2 An approval that cannot be completed before the applicable rail cutoff results in the transaction queuing to the next business day; the customer is notified consistent with MJD-OPS-0004.

4A.3 Approval queues are monitored; an item pending beyond its target is escalated to the Operations supervisor, and a high-value item at risk of missing cutoff is escalated to the Finance Controller.

## 5A. Channel-Specific Application

### 5A.1 Wires

Wire limits and approvals are enforced in the payment platform and align with the Wire Transfer Operations Runbook (MJD-OPS-0004). Callback verification at or above 25,000 USD and sanctions screening are separate controls that apply in addition to the approval thresholds here. A wire fails to release if any of approval, callback, or sanctions clearance is incomplete.

### 5A.2 ACH origination

ACH credit files are approved at the file level. A file at or above 250,000 USD requires dual approval before transmission to the ACH operator. Same-day ACH files follow the same thresholds but against the compressed same-day settlement windows.

### 5A.3 External transfers and bill pay

Customer-initiated external account transfers (push) and bill pay are subject to the per-item thresholds in Section 1.2 and to the per-account daily aggregates in Section 2. Customer-channel transactions that reach a dual-approval threshold are routed to Operations for the second approval before they leave the bank.

### 5A.4 Internal book transfers

Book transfers between two Meridian J.D. accounts settle in real time and carry higher single-approval ceilings (250,000 USD) because no external rail is involved, but they remain subject to sanctions screening and to the per-account daily aggregate.

### 5A.5 Interplay with fraud controls

A transaction that clears the approval thresholds may still be held by the fraud-screening model under MJD-RSK-0007. Approval authority does not override a fraud hold; a held transaction is reviewed by the fraud team and released only when the hold is cleared. Conversely, a transaction below all approval thresholds is not exempt from fraud screening.

### 5A.6 Control rationale

The thresholds in this matrix are calibrated so that the value at risk of any single individual's action is bounded. Dual approval bounds single-actor risk to below 100,000 USD on domestic wires; triple approval with a Finance Controller bounds it further above 1,000,000 USD. The per-account daily aggregates bound the total value that can leave an account in one day absent an explicit, approved override. Together these controls implement the segregation-of-duties principle that no single person can both initiate and complete a high-value movement of funds.

## 5B. Recordkeeping and Audit

5B.1 Every transaction record retains the maker, each approver and approval level, the value, the applicable threshold band, any override and its approval, and the sanctions and callback outcomes where applicable.

5B.2 Records supporting limit and approval controls are retained for five years per MJD-CMP-0008 and serve as SOX evidence under MJD-FIN-0005.

5B.3 The audit trail is append-only. A correction is recorded as a new entry that references the original; original entries are never overwritten.

### 5B.4 Metrics

| Metric | Target |
|---|---|
| Transactions released with correct approval level | 100 percent |
| Distinct maker and checker enforced | 100 percent |
| Overrides with documented Finance Controller approval | 100 percent |
| Overrides auto-reverting at expiry | 100 percent |
| Quarterly control-test defects | 0 |

## 6. Worked Approval Scenarios

6.1 **International wire requiring triple approval.** A 600,000 USD international SWIFT wire is at or above the 500,000 USD international triple-approval threshold. The maker prepares it, a senior checker reviews and dual-approves, and a Finance Controller provides the third approval before release.

6.2 **Override for a one-time acquisition.** A business-standard account (1,000,000 USD daily wire ceiling) needs to send 2,500,000 USD for an acquisition. The customer requests an override; the analyst confirms CDD currency and no flags; the Finance Controller approves a one-day override to 2,600,000 USD that auto-reverts. The wire still requires triple approval because it exceeds 1,000,000 USD.

## Related Documents

- MJD-OPS-0004 Wire Transfer Operations Runbook
- MJD-OPS-0005 Account Onboarding Workflow
- MJD-OPS-0009 Transaction Limits and Dual-Approval Matrix (2024 Edition)
- MJD-FIN-0005 Audit Trail and Evidence Standard
- MJD-FIN-0002 Account Reconciliation Procedure
- MJD-RSK-0003 Operational Risk Procedure

## Regulatory References

- UCC Article 4A (funds transfers)
- FFIEC Wholesale Payment Systems guidance
- 31 CFR 1010.410 (recordkeeping)
- Sarbanes-Oxley Act Section 404 (internal control over financial reporting)

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2020-01-10 | Head of Payment Operations | Initial limits matrix |
| 2.0.0 | 2022-01-15 | Head of Payment Operations | Added triple-approval tier |
| 2.3.0 | 2024-02-01 | Head of Payment Operations | 2024 Edition (issued as MJD-OPS-0009) |
| 3.0.0 | 2026-01-15 | Head of Payment Operations | Current edition; raised domestic wire dual-approval threshold to 100,000 USD and updated all tier limits; supersedes MJD-OPS-0009 |
