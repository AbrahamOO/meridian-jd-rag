---
doc_id: MJD-OPS-0009
title: Transaction Limits and Dual-Approval Matrix (2024 Edition)
department: OPERATIONS
doc_type: STANDARD
classification: INTERNAL
owner_role: Head of Payment Operations
allowed_roles: [OPERATIONS_ANALYST, BRANCH_STAFF, FINANCE_CONTROLLER]
effective_date: 2024-02-01
version: 2.3.0
review_cycle_months: 12
regulatory_refs: ["UCC Article 4A", "FFIEC Wholesale Payment Systems Guidance", "31 CFR 1010.410", "Sarbanes-Oxley Act Section 404"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Transaction Limits and Dual-Approval Matrix (2024 Edition)

> SUPERSEDED: This 2024 Edition has been superseded by MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix (version 3.0.0, effective 2026-01-15). The figures in this document are historical and must not be used to authorize current transactions. Refer to MJD-OPS-0007 for current limits.

## Purpose and Scope

This standard established the transaction limits and dual-approval requirements in effect at Meridian John Doe Financial (Meridian J.D.) for the 2024 cycle. It is retained for historical and audit reference only. The current authoritative version is MJD-OPS-0007.

This 2024 Edition applied to all payment channels and to Operations Analysts, Branch Staff, and Finance Controllers. Its figures differ from the current edition; where any reader encounters a conflict, the current edition (MJD-OPS-0007) governs and this document is non-authoritative.

## Definitions

- **Dual Approval (Maker-Checker).** A control requiring one individual to prepare a transaction and a different authorized individual to approve and release it.
- **Triple Approval.** Dual approval plus an additional approval at the Finance Controller level.
- **Daily Aggregate.** The sum of an account's outbound transactions of a given type within one business day.
- **Limit.** A maximum value permitted per transaction or per aggregate window.
- **Approval Threshold.** The value at or above which a heightened approval requirement applied.

## 1. Approval-Threshold Matrix (2024, Historical)

### 1.1 Wire transfers (2024 figures)

| Transaction | Single-approval ceiling | Dual approval required at | Triple approval required at |
|---|---|---|---|
| Domestic Fedwire | Below 50,000 USD | 50,000 USD or more | 500,000 USD or more |
| International SWIFT | Below 25,000 USD | 25,000 USD or more | 250,000 USD or more |
| Book transfer | Below 100,000 USD | 100,000 USD or more | 1,000,000 USD or more |

Under this 2024 Edition the daily wire limit before dual approval was **50,000 USD** for domestic Fedwire. The current edition (MJD-OPS-0007) raised this threshold to 100,000 USD. A single domestic wire at or above 50,000 USD required dual approval under this edition; at or above 500,000 USD it required triple approval.

The 50,000 USD domestic wire dual-approval threshold was calibrated in 2023 during the design of this edition for three reasons. First, FFIEC Wholesale Payment Systems Guidance directed institutions to apply layered controls at amounts where a single unauthorized wire could represent material customer harm. At the time, analysis of Meridian J.D.'s consumer wire population showed the 95th percentile consumer wire was 42,000 USD, placing the 50,000 USD threshold above the routine consumer range while still catching outlier consumer wires and the full small-business wire population. Second, the institution experienced one near-miss in 2022 in which a credential-compromised Operations Analyst account initiated a domestic wire of 48,000 USD that cleared before detection. Setting the threshold at 50,000 USD would have required a second approver for that transaction, and the 2024 Edition was designed specifically to prevent recurrence. Third, the SOX Section 404 control testing team confirmed that a 50,000 USD threshold was a clearly demarcated, system-enforced key control that could be tested with high precision.

### 1.2 ACH and other electronic transfers (2024 figures)

| Transaction | Single-approval ceiling | Dual approval required at |
|---|---|---|
| ACH credit origination, per file | Below 100,000 USD | 100,000 USD or more |
| External account transfer (push) | Below 25,000 USD | 25,000 USD or more |
| Bill pay, per item | Below 10,000 USD | 10,000 USD or more |

### 1.3 Cash and branch transactions (2024 figures)

| Transaction | Threshold for supervisor approval |
|---|---|
| Cash withdrawal, branch | 10,000 USD or more |
| Cash advance | 3,000 USD or more |
| Official check issuance | 25,000 USD or more |

### 1.4 Cryptocurrency and Digital Asset Limits (2024 figures, historical)

1.4.1 In 2024 Meridian J.D. piloted a limited digital asset settlement service under a sandbox arrangement. The following limits were in effect for the pilot. They are historical and the current position on digital assets is governed by MJD-OPS-0007 and any successor digital asset policy in effect.

| Transaction | Single-approval ceiling | Dual approval required at | Triple approval required at |
|---|---|---|---|
| On-chain stablecoin settlement (USD-denominated) | Below 10,000 USD equivalent | 10,000 USD equivalent or more | 100,000 USD equivalent or more |
| Crypto custody withdrawal (institutional) | None permitted without dual approval | All amounts | 50,000 USD equivalent or more |

1.4.2 All digital asset transactions under the 2024 pilot required real-time valuation using the reference price source designated by the Head of Payment Operations, with the USD-equivalent computed at the time of the approval, not the time of initiation.

1.4.3 The pilot was suspended in Q3 2024. No digital asset limits are carried forward to this archived document for post-2024 use. Current position: see MJD-OPS-0007.

### 1.5 Card and Debit Limits (2024 figures, historical)

| Transaction type | Per-transaction limit | Daily aggregate limit | Dual approval required |
|---|---|---|---|
| Debit card, consumer | 2,500 USD | 5,000 USD | Not applicable (card-present; PIN or signature) |
| Debit card, business | 10,000 USD | 25,000 USD | Not applicable (card-present) |
| ACH debit pull, consumer | 5,000 USD per item | 10,000 USD | At 10,000 USD aggregate |
| ACH debit pull, business | 25,000 USD per item | 100,000 USD | At 100,000 USD aggregate |
| Prepaid card load | 2,500 USD per load | 5,000 USD | Not applicable |

1.5.1 Card-present transactions were controlled through the card network authorization system with real-time velocity checks at the limits above. Dual approval was not technically applicable to card-present transactions; the control was the EMV chip and PIN or signature at the point of sale.

1.5.2 Temporary card limit increases for business customers in 2024 required a written request, Finance Controller approval, and a time-box of no more than 7 calendar days.

### 1.6 Real-Time Payments (RTP) Limits (2024 figures, historical)

1.6.1 Meridian J.D. joined The Clearing House RTP network in 2023. The following per-transaction limits were in effect during the 2024 cycle:

| Account tier | Per-transaction RTP limit | Daily RTP aggregate | Dual approval required at |
|---|---|---|---|
| Consumer standard | 25,000 USD | 25,000 USD | 10,000 USD or more |
| Consumer premier | 50,000 USD | 100,000 USD | 25,000 USD or more |
| Business standard | 100,000 USD | 500,000 USD | 25,000 USD or more |
| Business commercial | 1,000,000 USD | 5,000,000 USD | 100,000 USD or more |

1.6.2 The RTP network maximum per-transaction limit in 2024 was 1,000,000 USD (The Clearing House ceiling at the time). Meridian J.D. did not offer business commercial RTP transactions above 1,000,000 USD in this edition.

1.6.3 Because RTP transactions are irrevocable and settle in real time, the dual-approval thresholds for RTP were set lower than the corresponding domestic Fedwire thresholds (25,000 USD for Consumer premier vs. 50,000 USD for Fedwire). The irrevocability risk justified a more conservative threshold.

## 2. Per-Account Daily Limits (2024, Historical)

| Account tier | Daily outbound wire aggregate | Daily ACH aggregate | Daily external transfer aggregate |
|---|---|---|---|
| Consumer standard | 25,000 USD | 10,000 USD | 10,000 USD |
| Consumer premier | 100,000 USD | 50,000 USD | 50,000 USD |
| Business standard | 500,000 USD | 250,000 USD | 100,000 USD |
| Business commercial | 5,000,000 USD | 2,500,000 USD | 1,000,000 USD |

These 2024 tier ceilings are lower than the current edition. The current ceilings are in MJD-OPS-0007 Section 2.

### 2.1 Tier Qualification Table (2024, Historical)

The following criteria determined account tier assignment during the 2024 cycle. Tier assignment was reviewed at account opening and annually thereafter.

| Tier | Consumer criteria (2024) | Business criteria (2024) |
|---|---|---|
| Standard | New or existing consumer accounts with average daily balance below 10,000 USD over the prior 90 days; or accounts open less than 12 months | New or existing business accounts with annual revenue below 1,000,000 USD (self-certified and verified); or accounts open less than 12 months |
| Premier / Commercial | Average daily balance of 10,000 USD or more over the prior 90 days AND account open 12 months or more AND no adverse BSA/AML flag in prior 12 months | Annual revenue of 1,000,000 USD or more (verified with financial statements); or accounts with a signed commercial lending relationship; AND account open 12 months or more AND no adverse BSA/AML flag |

2.1.1 Tier downgrades in 2024 were automatic and monthly for consumer accounts; for business accounts, a tier downgrade required notification to the relationship manager 5 business days before effect.

2.1.2 BSA/AML adverse flags (any open SAR or currency transaction flag) suspended tier upgrades until the flag was resolved. This prevented a high-risk customer from accessing the higher transaction limits during an active monitoring period.

## 3. Maker-Checker Separation Rules

3.1 The maker and the checker had to be distinct individuals; self-approval was system-blocked and logged.

3.2 Triple-approval transactions required three distinct approvers, the third holding Finance Controller authority.

### 3.3 Maker-Checker Technical Controls (Historical)

3.3.1 The 2024 payment operations system enforced maker-checker separation through the following technical controls:

- **Identity binding**: Each transaction was linked to the authenticated user ID of the maker at initiation. The approval screen displayed the maker's user ID and prevented the same user ID from appearing as the approver.
- **Role-based queue routing**: Transactions above the dual-approval threshold were automatically routed to the approval queue. The approval queue was inaccessible to the maker's user session; the UI rendered the approve button inactive if the session user matched the maker's user ID.
- **Triple-approval enforcement**: Transactions above 500,000 USD for domestic Fedwire were routed to a separate Finance Controller queue after initial dual-approval. The Finance Controller queue required a distinct user with the Finance Controller role. The system blocked any Finance Controller from serving as the maker on a triple-approval transaction.
- **System-generated audit trail**: Every transaction created an immutable audit record containing: maker user ID, maker action timestamp, first approver user ID, first approver timestamp, Finance Controller user ID (if applicable), Finance Controller timestamp (if applicable), transaction amount, type, destination, and outcome. Audit records were written to a write-once log stream per MJD-FIN-0005.
- **Session separation requirement**: The system required the approver to initiate a fresh authentication before accessing the approval queue if the approver's session had been idle for more than 10 minutes. This prevented a scenario where the maker left their session unlocked and a colleague approved from the same workstation without re-authenticating.

3.3.2 Circumvention attempts (for example, creating two user accounts to serve as both maker and checker) were detected by comparing user attributes in the HR directory with the approver record. Any approval where the approver's directory attributes matched the maker's physical location, supervisor, or network session generated an alert to the Head of Payment Operations within 5 minutes.

## 4. Limit Overrides and Temporary Increases

4.1 Temporary limit increases were requested in writing, approved by the Finance Controller, time-boxed, and reverted automatically.

4.2 Each override was logged and reportable for SOX control testing under MJD-FIN-0005.

### 4.3 Override Approval Chain (2024, Historical)

The following approval chain governed limit override requests in 2024. All overrides were time-boxed and the system automatically reverted the account to the standard limit at the expiry time.

| Override amount (domestic Fedwire, per transaction) | Maximum time-box | Required approvers | Escalation if not resolved in time |
|---|---|---|---|
| 50,000 USD to 249,999 USD (single-transaction override of dual-approval) | 1 business day | Finance Controller | Override auto-expires; Head of Payment Operations notified |
| 250,000 USD to 499,999 USD | 1 business day | Finance Controller plus Head of Payment Operations | Override auto-expires; CISO notified if override was security-motivated |
| 500,000 USD to 4,999,999 USD (triple-approval tier) | 1 business day | Finance Controller plus Head of Payment Operations plus CISO sign-off | Override auto-expires; Board committee notified next business day |
| 5,000,000 USD or above | Not permitted under any override; requires board resolution | N/A | Board resolution process |

4.3.1 The CISO sign-off requirement for overrides above 500,000 USD was added in 2023 Q4 following FFIEC guidance on the importance of information security representation in high-value payment approvals.

4.3.2 Time-boxing was enforced by the payment operations system automatically: at the expiry timestamp, the account reverted to the standard tier limit without any manual action required. Override logs were retained per MJD-CMP-0008.

## 5. Governance and Review

5.1 This edition was reviewed annually. It was superseded by MJD-OPS-0007 effective 2026-01-15, which raised the domestic wire dual-approval threshold from 50,000 USD to 100,000 USD and increased the per-account daily limits across all tiers.

### 5.2 Reconciliation and Reporting (2024, Historical)

5.2.1 During the 2024 cycle, the following monitoring and reporting cadence applied to transaction limit controls:

| Report | Content | Frequency | Recipient |
|---|---|---|---|
| Daily limit breach report | Any transaction that triggered a dual or triple-approval requirement; outcome (approved, rejected, auto-expired) | Daily (T+1 morning) | Head of Payment Operations, Finance Controller |
| Self-approval attempt log | Any system-blocked self-approval attempt, with user ID, timestamp, and transaction amount | Daily (T+1 morning) | Head of Payment Operations; escalation to CISO if more than 1 per user per week |
| Override log | All temporary limit increases, amount, approver, duration, and expiry status | Weekly | Head of Payment Operations, Finance Controller |
| SOX control testing evidence package | Quarterly sample of dual and triple-approval transactions with full audit trail | Quarterly | Internal Audit, Finance Controller |
| Annual limit review memo | Results of annual threshold review, calibration analysis, and recommendation for next-year limits | Annual (January) | Head of Payment Operations, Finance Controller, CISO |

5.2.2 The SOX Section 404 control testing under MJD-FIN-0005 treated the 50,000 USD domestic wire dual-approval threshold as a key control. Internal Audit tested it quarterly by: (a) verifying the system blocked self-approval on a sample of transactions; (b) tracing a sample of approved transactions to the audit log to confirm distinct maker and approver user IDs; and (c) confirming that no transaction above 500,000 USD was approved without a Finance Controller approver on record.

## 6. Transition to MJD-OPS-0007

6.1 This 2024 Edition was superseded by MJD-OPS-0007 (version 3.0.0, effective 2026-01-15). The primary changes in the transition were:

| Parameter | 2024 Edition (this document) | 2026 Edition (MJD-OPS-0007) | Rationale for change |
|---|---|---|---|
| Domestic Fedwire dual-approval threshold | 50,000 USD | 100,000 USD | Customer experience friction for routine business wires; updated calibration showed 99th percentile consumer wire was 85,000 USD, making 50,000 USD threshold overly broad for consumer segment |
| International SWIFT dual-approval threshold | 25,000 USD | 50,000 USD | Aligned to updated SWIFT payment risk profile after enhanced monitoring controls implemented |
| Consumer standard daily wire aggregate | 25,000 USD | 50,000 USD | Consumer demand for higher limits; offset by enhanced transaction monitoring rules |
| Business commercial daily wire aggregate | 5,000,000 USD | 10,000,000 USD | Commercial client growth requiring higher operational limits |
| RTP consumer standard dual-approval threshold | 10,000 USD | 25,000 USD | Aligned to updated real-time payment risk model |

6.2 Implementation timeline: MJD-OPS-0007 was approved by the Finance Controller and Head of Payment Operations on 2025-12-01. A parallel-run period ran from 2026-01-01 to 2026-01-14, during which both the old and new limits were monitored simultaneously to confirm no operational disruption. All transactions during the parallel-run period were evaluated against both the 2024 and 2026 thresholds; any transaction that would have required a different approval level under the two editions was flagged for review.

6.3 The parallel run confirmed zero transactions that would have been mis-approved under the 2026 Edition. The Head of Payment Operations signed the transition confirmation memo on 2026-01-14, and MJD-OPS-0007 became effective 2026-01-15.

6.4 This document (MJD-OPS-0009) is retained per MJD-CMP-0008 as a historical record for audit and examination reference.

## Worked Example: 2024-Era Domestic Wire at 475,000 USD

The following example illustrates the maker-checker workflow under the 2024 figures for a domestic Fedwire transaction of 475,000 USD.

**Transaction details (historical, fictional):** Business commercial client requests a domestic Fedwire of 475,000 USD to a supplier account. Date: 2024-09-10.

**Step 1 - Maker initiation:** Operations Analyst A logs into the payment operations system under their authenticated user ID (OA-1042). They enter the wire details: amount 475,000 USD, beneficiary routing number, beneficiary account, date of execution 2024-09-10. The system validates the amount against the Business commercial daily aggregate (5,000,000 USD limit; current daily total is 200,000 USD; 475,000 USD brings total to 675,000 USD, within limit).

**Step 2 - Dual-approval routing:** The system detects that 475,000 USD is at or above the 50,000 USD domestic Fedwire dual-approval threshold. The system routes the transaction to the approval queue and displays a pending status to OA-1042. The system blocks OA-1042 from accessing the approval queue.

**Step 3 - First approval (checker):** Operations Analyst B (OA-2017, a distinct individual) logs into their own session and opens the approval queue. The queue displays the transaction, the maker's user ID (OA-1042), and the transaction details. OA-2017 reviews the wire instructions against the client's written authorization on file, confirms the beneficiary details are consistent, and approves. The system records OA-2017's approval timestamp: 2024-09-10 10:42:17.

**Step 4 - Triple-approval check:** The system checks whether the 500,000 USD triple-approval threshold is reached. 475,000 USD is below 500,000 USD, so no triple approval is required. The transaction proceeds to the Fedwire release queue after dual approval.

**Step 5 - Fedwire release:** The payment operations system releases the wire to the Federal Reserve's Fedwire Funds Service. Settlement occurs same day (RTGS).

**Step 6 - Audit trail:** The system writes the audit record: maker OA-1042 at 10:31:05; approver OA-2017 at 10:42:17; amount 475,000 USD; type Domestic Fedwire; beneficiary routing [redacted]; outcome Released. The record is written to the write-once log stream per MJD-FIN-0005.

**What would have changed if the amount were 500,000 USD:** At exactly 500,000 USD, the triple-approval threshold is met. After OA-2017's approval, the transaction would have routed to the Finance Controller queue. A Finance Controller (FC-0003, a distinct individual from both OA-1042 and OA-2017) would have been required to review and approve before release. The total approval time would have extended to accommodate the Finance Controller availability window, subject to the override time-box rules in Section 4.3.

## Escalation Chain Table (2024, Historical)

| Event type | First escalation | Second escalation | Time to first escalation |
|---|---|---|---|
| Self-approval attempt | Head of Payment Operations | CISO (if more than 1 per user per week) | Immediate (system alert) |
| Transaction above 500,000 USD pending Finance Controller approval for more than 2 hours | Head of Payment Operations | Finance Controller manager | 2 hours after entering FC queue |
| Override request above 250,000 USD | Finance Controller plus Head of Payment Operations | CISO | At request submission |
| Override auto-expiry triggered without transaction completion | Head of Payment Operations | Operations team lead | At expiry event |
| Triple-approval transaction rejected by Finance Controller | Head of Payment Operations | Legal (if client dispute likely) | Within 30 minutes of rejection |

## Roles and Responsibilities

| Role | Responsibility (historical) |
|---|---|
| Operations Analyst | Prepared transactions within 2024 limits, routed for approval |
| Branch Staff | Obtained supervisor approval for cash thresholds |
| Finance Controller | Provided triple-approval authority and approved overrides |
| Head of Payment Operations | Owned this edition and led its annual review |

## Exceptions and Escalation

- No transaction could exceed a 2024 account daily limit without a documented, time-boxed Finance Controller override.
- Self-approval attempts were hard-blocked and escalated.
- This document must not be used to authorize current transactions; any such attempt is a control violation. Use MJD-OPS-0007.

## Related Documents

- MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix (current edition)
- MJD-OPS-0004 Wire Transfer Operations Runbook
- MJD-OPS-0005 Account Onboarding Workflow
- MJD-FIN-0005 Audit Trail and Evidence Standard
- MJD-FIN-0002 Account Reconciliation Procedure
- MJD-RSK-0003 Operational Risk Procedure
- MJD-CMP-0008 Records Retention Schedule

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
| 2.2.0 | 2023-03-01 | Head of Payment Operations | Adjusted ACH thresholds |
| 2.3.0 | 2024-02-01 | Head of Payment Operations | 2024 Edition limits; domestic wire dual-approval threshold 50,000 USD |
| - | 2026-01-15 | Head of Payment Operations | SUPERSEDED by MJD-OPS-0007 version 3.0.0; this edition is historical |
