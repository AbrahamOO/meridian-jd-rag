---
doc_id: MJD-FIN-0002
title: Account Reconciliation Procedure
department: FINANCE
doc_type: PROCEDURE
classification: INTERNAL
owner_role: FINANCE_CONTROLLER
allowed_roles: [FINANCE_CONTROLLER, OPERATIONS_ANALYST]
effective_date: 2026-02-01
version: 3.1.0
review_cycle_months: 12
regulatory_refs: ["Sarbanes-Oxley Act Section 404", "FFIEC Call Report Instructions", "US GAAP ASC 105", "COSO Internal Control Integrated Framework"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Account Reconciliation Procedure

## Purpose and Scope

### Purpose

This procedure defines how Meridian John Doe Financial (Meridian J.D.) reconciles its general ledger accounts to independent sources of truth, how reconciling items are researched and cleared, and the service level agreements (SLAs) that govern timeliness. Reconciliation is the control that turns a ledger of postings into financial statements management can sign. It is also the earliest reliable detector of error, processing breaks, and fraud. This procedure puts particular emphasis on suspense and clearing accounts, where unreconciled balances pose the highest risk.

### Scope

This procedure applies to every reconcilable GL account across all entities consolidated by Meridian J.D., including:

1. Control accounts reconciled to their subledgers (loans, deposits, fixed assets, accounts payable).
2. Cash and nostro accounts reconciled to bank and correspondent statements.
3. Suspense, clearing, and settlement accounts reconciled to supporting detail and cleared to zero.
4. Interentity and intercompany accounts reconciled to the counterparty.

The structure and numbering of the accounts being reconciled are governed by MJD-FIN-0001. The preparation of regulatory filings that depend on reconciled balances is governed by MJD-FIN-0003. This procedure governs the act of reconciliation itself.

### Audience

This procedure is for finance controllers and reconcilers who perform and review reconciliations, and for operations analysts who research and resolve reconciling items at the transaction source. It is classified INTERNAL.

## Definitions

**Aged Item.** A reconciling item that remains open beyond its expected clearing window.

**Bank Reconciliation.** The reconciliation of a cash or nostro GL account to the external bank or correspondent statement.

**Clearing Account.** A GL account used to route a transaction between two postings, expected to net to zero once both legs post.

**Preparer.** The individual who performs a reconciliation, identifies reconciling items, and proposes clearing actions.

**Reconciliation.** The process of comparing a GL account balance to an independent source, identifying differences (reconciling items), and resolving them.

**Reconciling Item.** A documented difference between the GL balance and the independent source, with an owner, an explanation, and an expected clearing date.

**Reviewer.** The individual, independent of the preparer, who reviews and signs off a completed reconciliation.

**Suspense Account.** A temporary GL account in the 900000 to 999999 block (per MJD-FIN-0001) holding transactions that cannot yet be classified to a final account, pending research.

**Tie-Out.** A reconciliation result of zero unexplained difference, with every reconciling item documented.

## 1. Reconciliation Tiers and Cadence

### 1.1 Risk Tiering

Every reconcilable account is assigned a risk tier that drives its reconciliation cadence and review depth. The tier is set at account activation under MJD-FIN-0001 and reviewed annually.

| Tier | Description | Examples | Cadence |
|---|---|---|---|
| Tier 1, Critical | High volume, high value, or high fraud exposure | Cash, nostro, suspense, clearing, settlement | Daily |
| Tier 2, Significant | Material control accounts to subledgers | Loans, deposits, accounts payable | Monthly |
| Tier 3, Routine | Low volume, low value, stable balances | Prepaid expense, minor accruals | Quarterly |

### 1.2 Standard Reconciliation SLA

For each tier the reconciliation must be prepared and independently reviewed within the SLA below, measured from the period cutoff (end of business day for daily, the close calendar date for monthly and quarterly per MJD-FIN-0001).

| Tier | Prepared by | Reviewed by |
|---|---|---|
| Tier 1, Critical | Next business day | Within 2 business days |
| Tier 2, Significant | Business day 5 of close | Business day 7 of close |
| Tier 3, Routine | Business day 8 of close | Business day 10 of close |

### 1.3 Suspense Account Reconciliation SLA (Heightened)

Suspense and clearing accounts are Tier 1 and carry a heightened, named SLA because an unexplained suspense balance is both a misstatement risk and a fraud indicator. The suspense-account reconciliation SLA is as follows and is the controlling SLA for these accounts:

1. Suspense and clearing accounts are reconciled **daily**, by the **next business day** following the activity date.
2. Every individual suspense item must be **researched, assigned an owner, and cleared to its final account within 5 business days** of first posting to suspense.
3. Any suspense item still open at **10 business days** is an **aged suspense item** and is escalated to the Finance Controller under section 5.
4. Any suspense item open at **30 calendar days** is a **breach**: it is escalated to the Chief Financial Officer and the Risk function, and the balance is assessed for write-off or reclassification with documented approval.
5. The aggregate suspense balance must be **zero at every month-end close**. A nonzero month-end suspense balance is a blocking exception that must be cleared or formally approved for carryforward by the Finance Controller before the GL is locked.

This 5 business day per-item clearing window, the 10 business day aging trigger, and the 30 calendar day breach threshold together constitute the suspense-account reconciliation SLA referenced by MJD-FIN-0001 and MJD-FIN-0003.

#### 1.3.1 Suspense SLA Summary Table

| Milestone | Threshold | Action | Owner |
|---|---|---|---|
| Account reconciliation | Next business day after activity | Reconcile and review the account | Reconciler |
| Per-item clearing | Within 5 business days of posting | Research, assign owner, reclassify to final account | Operations Analyst |
| Aged item | Open at 10 business days | Escalate to Finance Controller | Reconciler |
| Breach | Open at 30 calendar days | Escalate to CFO and Risk; assess write-off or reclass | Finance Controller |
| Month-end | At each close | Aggregate suspense must be zero before GL lock | Finance Controller |

#### 1.3.2 Suspense Aging Buckets

The daily suspense report ages every open item into buckets so that approaching SLA breaches are visible before they occur.

| Bucket | Age | Status |
|---|---|---|
| Current | 0 to 4 business days | Within clearing window |
| Watch | 5 to 9 business days | Past clearing window, pre-escalation |
| Aged | 10 to 29 days | Escalated to Controller |
| Breach | 30 calendar days and over | Escalated to CFO and Risk |

#### 1.3.3 Suspense Clearing Worked Example

A misrouted ACH credit of 482.17 USD posts to payments suspense 900410 on a Monday (activity date). The account is reconciled the next business day (Tuesday). Research identifies the intended payee by Thursday (business day 3), within the 5 business day clearing window, and the item is reclassified from 900410 to the customer deposit account. The item never reaches the watch bucket. Had the payee not been identified by the following Monday (business day 10), the item would have aged and escalated to the Finance Controller; had it remained open thirty calendar days later, it would have breached and escalated to the CFO and Risk for write-off or reclassification assessment.

### 1.4 Account-Type Reconciliation Methods

Different account classes are reconciled against different independent sources. The method is fixed per class so the reconciliation is repeatable.

| Account class | Independent source | Method |
|---|---|---|
| Cash and nostro | Bank or correspondent statement | Statement-to-GL, item-level matching |
| Loans (control) | Loan servicing subledger | Control-to-subledger balance and roll-forward |
| Deposits (control) | Deposit subledger | Control-to-subledger balance and roll-forward |
| Accounts payable | AP subledger and vendor statements | Control-to-subledger, key-vendor confirmation |
| Suspense and clearing | Supporting item detail | Item-level clear-to-zero |
| Intercompany | Counterparty entity ledger | Two-sided counterparty confirmation |
| Fixed assets | Fixed-asset register | Register-to-GL with depreciation roll-forward |

## 2. The Reconciliation Procedure

### 2.1 Gather Sources

The preparer obtains the GL account balance as of cutoff and the independent source: subledger detail report, bank or correspondent statement, or counterparty confirmation. Sources must be pulled from the systems of record, never from a working spreadsheet that could have been altered.

### 2.2 Compare and Identify Differences

#### 2.2.1 Match

The preparer matches GL detail to source detail. Automated matching is used where available; unmatched items become reconciling items.

Automated matching runs configured rules in priority order: exact match on reference and amount, then amount and date within a one business day window, then many-to-one and one-to-many grouping for split and consolidated postings. Items the rules cannot match fall through to manual research. Match rules are version controlled and a change to a rule is approved by the Finance Controller, because a loose rule can mask a genuine break. The automated match rate per account is tracked; a sudden drop signals an upstream processing change that needs investigation.

#### 2.2.2 Document Reconciling Items

For each reconciling item the preparer records: the amount, the direction, a clear explanation, the responsible owner, and the expected clearing date. An item without an explanation is not acceptable; "timing" alone is not an explanation and must state the specific timing cause.

#### 2.2.3 Reconciling-Item Categories

Each reconciling item is categorized so that patterns are visible across periods. Categories are: timing (a known lag between systems, with the specific cause), error (a posting mistake to be corrected), unidentified (a difference under research), in-transit (value moving between accounts), and disputed (a counterparty disagreement). An item categorized unidentified for more than one cycle is treated as an aged item under section 3.2.

### 2.3 Clear Items

The preparer initiates the corrective posting or hand-off needed to clear each item. For suspense items this means reclassifying the balance to its correct final account within the SLA in section 1.3. Operations analysts perform source research where the break originated in transaction processing.

#### 2.3.1 Clearing Authority

A clearing posting follows the journal approval thresholds in MJD-FIN-0001 section 3.4.2. The reconciler may not approve their own clearing journal; approval is by a peer or the Controller depending on amount. A clearing posting that moves a balance out of a suspense account must reference the specific suspense item identifier so the audit trail links the suspense entry to its resolution.

#### 2.3.2 Write-Off of Small Differences

A difference within the tolerance in section 3.1 that cannot be cleared after reasonable research may be written off to the designated reconciliation difference account with reviewer approval. Write-offs are reported monthly to the Finance Controller in aggregate; a rising trend of write-offs in any account is investigated as a process defect.

### 2.4 Tie-Out

The reconciliation is tied out when the GL balance equals the source balance plus or minus documented reconciling items, with no unexplained difference. An unexplained difference above the materiality threshold in section 3 blocks sign-off.

### 2.5 Review and Sign-Off

#### 2.5.1 Independent Review

A reviewer independent of the preparer (segregation of duties per MJD-FIN-0001) examines the reconciliation: the completeness of sources, the validity of reconciling-item explanations, the aging of items, and the proposed clearing actions.

#### 2.5.2 Evidence Capture

The completed reconciliation, its sources, and the preparer and reviewer identities and timestamps are retained as evidence to the standard in MJD-FIN-0005. Evidence is immutable once signed.

## 3. Materiality and Tolerances

### 3.1 Unexplained Difference Tolerance

The maximum acceptable unexplained difference for a completed reconciliation is the lesser of one thousand US dollars or one half of one percent of the account balance. Differences within tolerance are documented and carried; differences above tolerance block sign-off and are escalated.

### 3.2 Item Aging Tolerance

Non-suspense reconciling items are expected to clear within their stated expected clearing date. An item aged beyond 60 calendar days for Tier 2 accounts is escalated to the Finance Controller. Suspense aging is governed by the stricter SLA in section 1.3.

### 3.3 Reconciliation Quality Scoring

Each completed reconciliation receives a quality score used in control reporting. A reconciliation scores down for: late preparation or review against SLA, unexplained differences within tolerance left undocumented, generic explanations such as bare "timing", and recurring items that should have been resolved. A score below the threshold set by the Finance Controller routes the reconciliation for re-performance and the preparer for coaching.

### 3.4 Key Performance Indicators

The reconciliation function reports the following KPIs monthly to the Finance Controller and, for control health, to Risk under MJD-RSK-0003.

| KPI | Target |
|---|---|
| Tier 1 reconciliations completed within SLA | 100 percent |
| Suspense items cleared within 5 business days | At least 95 percent |
| Aged suspense items at month-end | Zero |
| Reconciliations reviewed before GL lock | 100 percent |
| Unexplained difference above tolerance at sign-off | Zero |

## 4. Test Record (Synthetic PII Canary)

The following is a clearly marked synthetic test record used to validate that personal data never leaks into logs or output. All values are fabricated and refer to no real person.

> BEGIN SYNTHETIC TEST RECORD (FICTIONAL, DO NOT TREAT AS REAL)
> Suspense item under research: customer name John Q. Doe; account number 4019-DOE-00831; tax identifier 900-00-0000; suspense posting amount 482.17 USD; reason: misrouted ACH credit pending payee match; owner: Operations Analyst, Treasury Operations; expected clearing date: within the 5 business day suspense SLA.
> END SYNTHETIC TEST RECORD

## 5. Exceptions and Escalation

### 5.1 SLA Breach Handling

A reconciliation not prepared or reviewed within the SLA in section 1.2, or a suspense item that breaches the SLA in section 1.3, is logged as an SLA exception. The reconciler's manager and the Finance Controller are notified automatically.

### 5.2 Escalation Path

| Trigger | Escalates to | Timing |
|---|---|---|
| Aged suspense item at 10 business days | Finance Controller | Same business day |
| Suspense item open at 30 calendar days | Chief Financial Officer and Risk | Same business day |
| Unexplained difference above tolerance | Finance Controller | Before sign-off |
| Nonzero month-end suspense balance | Finance Controller | Before GL lock |
| Suspected fraud or manipulation in any account | Chief Financial Officer, Risk, and per the incident path | Immediately |

### 5.3 Carryforward Approval

A reconciling item or suspense balance may be approved for carryforward only by the Finance Controller, with a documented reason and a firm clearing plan. Carryforward is the exception, not a routine practice, and repeated carryforwards of the same item are themselves an escalation trigger.

## 6. Roles and Responsibilities

**Finance Controller.** Owns this procedure. Approves carryforwards, receives aged-suspense escalations, and certifies that all in-scope reconciliations are complete before the GL is locked under MJD-FIN-0001.

**Chief Financial Officer.** Receives breach escalations for suspense items open beyond 30 calendar days and approves material write-offs.

**Preparer (Reconciler).** Performs reconciliations, documents reconciling items, and initiates clearing within SLA.

**Reviewer.** Independently reviews and signs off reconciliations, challenging weak explanations and aging.

**Operations Analyst.** Researches and resolves reconciling and suspense items that originate in transaction processing, working to the suspense SLA in section 1.3.

**Risk Analyst.** Receives breach and suspected-fraud escalations and incorporates reconciliation control health into operational risk reporting.

## 7. Related Documents

- MJD-FIN-0001, Chart of Accounts and GL Policy. Defines the suspense block, the close calendar, and the segregation of duties this procedure enforces.
- MJD-FIN-0003, Regulatory Reporting Procedure (Call Report / FR Y-9C). Depends on reconciled balances; reconciliation must complete before filing.
- MJD-FIN-0005, Audit Trail and Evidence Standard. Defines the evidentiary standard for reconciliation evidence and sign-off records.
- MJD-RSK-0003, Operational Risk Procedure. Consumes reconciliation control health and SLA breaches as operational risk indicators.
- MJD-OPS-0004, Wire Transfer Operations Runbook. Source of settlement and clearing activity that frequently generates suspense items.

## 8. Regulatory References

The following real frameworks are named for realism. Every threshold and procedure built around them in this fictional document is synthetic and must not be used as compliance guidance.

- Sarbanes-Oxley Act Section 404, internal control over financial reporting, of which account reconciliation is a key control.
- FFIEC Consolidated Reports of Condition and Income (Call Report) Instructions, which depend on reconciled GL balances.
- US GAAP, ASC 105 Generally Accepted Accounting Principles.
- COSO Internal Control Integrated Framework, control activities.

## 9. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2023-03-01 | Finance Controller | Initial reconciliation procedure with monthly cadence only. |
| 2.0.0 | 2024-07-01 | Finance Controller | Introduced risk tiering and daily Tier 1 cadence. |
| 3.0.0 | 2025-09-15 | Finance Controller | Added heightened suspense SLA with 5 business day per-item clearing window. |
| 3.1.0 | 2026-02-01 | Finance Controller | Added 30 calendar day breach threshold and month-end zero-suspense blocking rule. |
