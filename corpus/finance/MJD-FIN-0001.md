---
doc_id: MJD-FIN-0001
title: Chart of Accounts and General Ledger Policy
department: FINANCE
doc_type: POLICY
classification: INTERNAL
owner_role: FINANCE_CONTROLLER
allowed_roles: [FINANCE_CONTROLLER, RISK_ANALYST, OPERATIONS_ANALYST]
effective_date: 2026-01-15
version: 2.3.0
review_cycle_months: 12
regulatory_refs: ["FFIEC Call Report Instructions", "FR Y-9C Instructions", "US GAAP ASC 105", "GLBA Safeguards Rule", "Sarbanes-Oxley Act Section 404"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Chart of Accounts and General Ledger Policy

## Purpose and Scope

### Purpose

This policy establishes the authoritative structure, governance, and operating rules for the Chart of Accounts (COA) and the General Ledger (GL) of Meridian John Doe Financial (Meridian J.D.). The COA is the backbone of every financial statement, every regulatory filing, and every management report the institution produces. A disciplined, well-controlled COA is what allows Meridian J.D. to map an individual transaction at a branch teller window to a line on the quarterly Call Report and the consolidated FR Y-9C. This policy exists so that account creation, classification, posting, and mapping are consistent, auditable, and resistant to error or manipulation.

### Scope

This policy applies to all general ledger activity across every legal entity, branch, business line, and subsidiary consolidated by Meridian J.D. It governs:

1. The numbering and structure of all GL accounts in the production ledger.
2. The lifecycle of an account from request through approval, activation, dormancy, and retirement.
3. The mapping of internal GL accounts to external regulatory and statutory reporting schedules.
4. The posting rules, including who may post, when subledgers close, and how the GL is locked at period end.
5. The segregation of duties controls that prevent any single individual from creating, posting to, and reconciling the same account.

This policy does not define the detailed reconciliation steps for any specific account class (see MJD-FIN-0002, Account Reconciliation Procedure) and it does not define the mechanics of preparing the Call Report or FR Y-9C (see MJD-FIN-0003, Regulatory Reporting Procedure). It defines the COA and GL controls those documents depend upon.

### Audience

The intended readers are finance controllers and their staff who own the ledger, risk analysts who rely on GL data for risk aggregation, and operations analysts whose transaction processing feeds the subledgers. This document is classified INTERNAL.

## Definitions

**Account Segment.** A defined position within the GL account string that carries a specific dimension of meaning, for example entity, natural account, cost center, or product.

**Chart of Accounts (COA).** The complete, structured list of all accounts available for posting in the production general ledger, including each account's number, name, type, normal balance, and reporting mappings.

**Control Account.** A GL account whose balance is the aggregate of detail held in a subsidiary ledger (subledger), for example the loans control account whose detail lives in the loan servicing subledger.

**Dormant Account.** A GL account with no posting activity for two consecutive fiscal quarters and a zero or immaterial balance, flagged for review and potential retirement.

**General Ledger (GL).** The master accounting record of Meridian J.D. into which all subledgers post and from which all financial statements and regulatory filings are derived.

**Mapping (Regulatory Mapping).** The deterministic assignment of each GL natural account to one or more external reporting lines, including FFIEC 031/041 Call Report schedules and FR Y-9C schedules.

**Natural Account.** The segment of the GL string that identifies what the account represents in accounting terms, for example cash, loans, deposits, interest income, or salaries expense.

**Normal Balance.** The side (debit or credit) on which an account class is expected to carry a positive balance. Assets and expenses are normal debit; liabilities, equity, and income are normal credit.

**Posting.** The act of recording a debit and offsetting credit entry into the GL, either automatically from a subledger feed or manually by way of a journal entry.

**Subledger.** A detailed transaction ledger for a specific domain (loans, deposits, fixed assets, accounts payable) that summarizes into a control account in the GL.

**Suspense Account.** A temporary GL account used to hold transactions that cannot yet be classified to their final account, pending research and clearing. Governed for reconciliation by MJD-FIN-0002.

## 1. Chart of Accounts Structure

### 1.1 Account String Format

The Meridian J.D. GL account string is a fixed twenty-character segmented identifier. Every posting in the production ledger carries a fully qualified account string. The segments, in order, are:

| Position | Segment | Length | Purpose |
|---|---|---|---|
| 1 | Entity | 3 | Legal entity or consolidation unit |
| 2 | Natural Account | 6 | Accounting nature of the balance |
| 3 | Cost Center | 4 | Owning department or branch |
| 4 | Product | 4 | Product or instrument code |
| 5 | Intercompany | 3 | Counterparty entity for intercompany, else 000 |

A representative (fictional) example string is `010-110200-2040-3015-000`, read as legal entity 010, natural account 110200 (Cash and Due from Banks), cost center 2040 (Treasury Operations), product 3015 (Operating Cash), no intercompany counterparty.

### 1.2 Natural Account Ranges

The six-digit natural account is the segment that determines financial statement classification and regulatory mapping. Ranges are reserved as follows and may not be repurposed without Controller approval under section 3.

| Range | Class | Normal Balance |
|---|---|---|
| 100000 to 199999 | Assets | Debit |
| 200000 to 299999 | Liabilities | Credit |
| 300000 to 399999 | Equity | Credit |
| 400000 to 499999 | Interest and Fee Income | Credit |
| 500000 to 599999 | Interest Expense | Debit |
| 600000 to 699999 | Noninterest Income | Credit |
| 700000 to 799999 | Noninterest Expense | Debit |
| 900000 to 999999 | Suspense, Clearing, and Memo | Varies |

### 1.3 Suspense and Clearing Block

The 900000 to 999999 block is reserved for suspense, clearing, and memo accounts. These accounts must carry a target balance of zero at each period close. Accounts in this block are subject to the heightened reconciliation cadence in MJD-FIN-0002 because an unreconciled suspense balance is both a misstatement risk and a fraud indicator. No suspense account may be used as a permanent home for any balance. A balance that remains in suspense beyond the clearing window defined in MJD-FIN-0002 is escalated under section 6 of this policy.

#### 1.3.1 Suspense Sub-Ranges

The suspense and clearing block is further partitioned so that the source of an unclassified balance is visible from the account number alone. The sub-ranges are reserved as follows.

| Sub-range | Use | Owning function |
|---|---|---|
| 900000 to 909999 | Payments and ACH suspense | Operations |
| 910000 to 919999 | Wire and settlement clearing | Treasury Operations |
| 920000 to 929999 | Card and dispute clearing | Operations |
| 930000 to 939999 | Deposit and item processing suspense | Operations |
| 940000 to 949999 | Intercompany clearing | Finance |
| 990000 to 999999 | Memo and statistical (nonfinancial) accounts | Finance |

#### 1.3.2 Memo Accounts

Memo and statistical accounts (990000 to 999999) carry nonfinancial quantities such as account counts or notional amounts used in management reporting. They never post to a financial statement line and are excluded from the regulatory mapping completeness check in section 4.3. They are clearly flagged `statement_excluded: true` in the COA master so that they cannot be mapped to a Call Report or FR Y-9C line in error.

### 1.4 Prohibited Practices

The following are prohibited at all times:

1. Posting to a parent or summary account; only detail (postable) accounts accept entries.
2. Creating a natural account outside the reserved ranges in section 1.2.
3. Using a suspense account to manage earnings, defer expense, or smooth results.
4. Reusing a retired account number within thirty-six months of retirement.

## 2. Account Lifecycle

### 2.1 Account Request

Any new GL account begins as a request submitted through the finance service workflow. The request must specify the proposed natural account name, the class and range, the normal balance, the owning cost center, and the intended regulatory mapping under section 4. A request that omits the regulatory mapping is returned to the requester; an unmapped account cannot be activated.

#### 2.1.1 Required Request Attributes

A complete account request carries the following attributes. A request missing any mandatory attribute is rejected automatically by the workflow before it reaches review.

| Attribute | Mandatory | Notes |
|---|---|---|
| Proposed natural account name | Yes | Must follow the naming convention in section 2.1.2 |
| Class and range | Yes | Must fall in a reserved range from section 1.2 |
| Normal balance | Yes | Debit or credit, consistent with the class |
| Owning cost center | Yes | A valid, active cost center |
| Regulatory mapping | Yes, unless statement_excluded | Call Report and FR Y-9C line per section 4 |
| Business justification | Yes | One paragraph describing the need |
| Capitalization treatment | Conditional | Required for asset requests, expense or capitalize |
| Currency | Yes | Functional currency is USD; foreign accounts flagged |

#### 2.1.2 Naming Convention

Natural account names are written as a noun phrase that states the balance, from general to specific, with no abbreviations that are not in the approved abbreviation list. For example, "Loans, Commercial and Industrial, Fixed Rate" rather than "C&I Loans FR". Consistent naming is what lets a reader and a retrieval system disambiguate similar accounts.

### 2.2 Review and Approval

#### 2.2.1 Functional Review

The General Ledger Accountant reviews the request for structural correctness: range, normal balance, naming convention, and duplication against existing accounts.

#### 2.2.2 Mapping Review

The Regulatory Reporting Analyst confirms the proposed Call Report and FR Y-9C mapping is correct and complete. This control prevents the most common reporting defect, an account that posts correctly to the GL but is mapped to the wrong external line.

#### 2.2.3 Controller Approval

The Finance Controller, or a delegate at Director level or above, provides final approval. Approval is recorded in the GL change log with the approver identity, timestamp, and rationale, satisfying the audit trail requirements of MJD-FIN-0005.

### 2.3 Activation

On approval, the account is created in the production COA with an effective date. Accounts are never backdated; the effective date is the date of activation or later.

### 2.4 Dormancy and Retirement

An account with no activity for two consecutive fiscal quarters and an immaterial balance is flagged dormant. The account owner is notified and must either justify retention or approve retirement. Retired account numbers are quarantined for thirty-six months.

#### 2.4.1 Dormancy Review

The General Ledger Accountant produces a dormant-account report at each quarter close. For each dormant account the owner responds within ten business days with one of: retain (with reason), retire, or merge into another account. No response defaults to a retention hold for one additional quarter, after which a non-response routes to the Finance Controller for disposition.

#### 2.4.2 Retirement Steps

Retirement follows fixed steps so that history is preserved: confirm a zero balance, confirm no open commitments or reconciling items reference the account, remove the account from active mapping, mark the account inactive with an effective date, and quarantine the number. The retired account remains queryable for historical reporting; only new postings are blocked.

#### 2.4.3 Worked Example

A clearing account 920500 (Card Dispute Clearing, legacy product) shows no activity for three quarters and a zero balance after the legacy card product is decommissioned. The owner approves retirement. The accountant confirms no open reconciling items, removes the mapping, marks 920500 inactive effective the first day of the next period, and quarantines 920500 until the same date thirty-six months later. A new card dispute clearing account, if needed, takes the next free number in the 920000 sub-range, never 920500.

## 3. General Ledger Governance and Change Control

### 3.1 Single Source of Truth

The production GL is the single authoritative accounting record. No business line may maintain a parallel ledger as a system of record. Shadow spreadsheets used for analysis are not ledgers and may never be the basis of a financial statement balance.

### 3.2 Change Control

Any change to the COA structure, a natural account range, or a regulatory mapping is a controlled change requiring Controller approval and a logged change record. Structural changes that affect regulatory mappings must be coordinated with the regulatory reporting cycle so that a mapping change does not take effect mid-quarter without a documented restatement plan.

### 3.3 Segregation of Duties

No individual may simultaneously hold the ability to create an account, post to it, and reconcile it. The system enforces these as distinct entitlements. Where staffing constraints force a temporary overlap, a compensating control of independent monthly review by the Controller is documented and the exception is logged under MJD-FIN-0004 section on control exceptions and under MJD-FIN-0005.

#### 3.3.1 Conflicting Entitlement Matrix

The four sensitive GL entitlements and their permitted combinations are defined below. A cell marked No means the two entitlements may not be held by the same individual without a documented compensating control.

| Holds \ Also holds | Create account | Post journal | Approve journal | Reconcile |
|---|---|---|---|---|
| Create account | n/a | Yes | No | No |
| Post journal | Yes | n/a | No | No |
| Approve journal | No | No | n/a | No |
| Reconcile | No | No | No | n/a |

The two combinations that are never permitted, even with a compensating control, are post-and-approve of the same journal and post-and-reconcile of the same account, because each defeats the core check on misstatement and fraud.

### 3.4 Journal Entry Standard

#### 3.4.1 Manual Journal Requirements

A manual journal entry must be balanced (debits equal credits), carry a description that states the business reason and not merely the accounts, reference its supporting evidence, and be approved by someone other than the preparer at the threshold in section 3.4.2. Round-dollar entries with no support, entries posted in the final hour before a GL lock, and entries to suspense accounts are flagged for heightened review.

#### 3.4.2 Journal Approval Thresholds

| Journal absolute value (USD) | Approver |
|---|---|
| Up to 25,000 | GL Accountant (peer, not preparer) |
| 25,001 to 250,000 | Finance Controller |
| Above 250,000 | Finance Controller and Chief Financial Officer |

#### 3.4.3 Recurring and Automated Journals

Recurring journals (accruals, allocations) are templated and approved once at template creation and then on material change. Automated subledger feeds post under a system account whose activity is reconciled daily under MJD-FIN-0002; a feed that fails validation routes its items to the relevant suspense sub-range rather than posting an unbalanced or misclassified entry.

## 4. Regulatory Mapping

### 4.1 Mapping Principle

Every postable natural account maps deterministically to the external reporting lines it feeds. The mapping table is version controlled. The two primary external consumers are the FFIEC Call Report (Consolidated Reports of Condition and Income, FFIEC 031 or 041) and the Federal Reserve FR Y-9C (Consolidated Financial Statements for Holding Companies).

### 4.2 Representative Mapping Extract

The following is a representative (fictional) extract of the mapping table.

| Natural Account | Name | Call Report Schedule | FR Y-9C Schedule |
|---|---|---|---|
| 110200 | Cash and Due from Banks | RC line 1 | HC line 1 |
| 140100 | Loans, Commercial and Industrial | RC-C line 4 | HC-C line 4 |
| 210300 | Deposits, Interest Bearing | RC-E | HC-E |
| 410100 | Interest Income on Loans | RI line 1 | HI line 1 |
| 710400 | Salaries and Employee Benefits | RI line 7 | HI line 7 |

### 4.3 Mapping Integrity Check

Before each regulatory filing cycle, the Regulatory Reporting Analyst runs a completeness check that asserts every account with a nonzero balance maps to at least one external line. Any unmapped balance is a blocking exception resolved before filing under MJD-FIN-0003.

#### 4.3.1 Completeness Assertions

The integrity check evaluates four assertions and fails the cycle if any fails:

1. Every postable account with a nonzero balance maps to at least one Call Report line and one FR Y-9C line, unless flagged `statement_excluded`.
2. No account maps to a line that does not exist in the current FFIEC or Federal Reserve instruction set version.
3. The sum of accounts mapped to a given reported line equals the reported line value, with no balance double-counted across mutually exclusive lines.
4. No suspense or memo account is mapped to a financial statement line.

#### 4.3.2 Mapping Versioning

The mapping table is versioned alongside the FFIEC and Federal Reserve instruction versions it targets. When the instructions change for a reporting period, the mapping is updated and the change is approved under section 3.2 before the period it takes effect. A mapping version is never changed retroactively for a closed period; a closed-period correction is handled as an amended filing under MJD-FIN-0003.

### 4.4 Multi-Entity Consolidation

#### 4.4.1 Entity Segment

The three-character entity segment distinguishes the insured depository institution, the holding company, and consolidated subsidiaries. The Call Report is filed at the insured depository level; the FR Y-9C is filed at the consolidated holding-company level. The same natural account therefore rolls up to different filings depending on its entity segment.

#### 4.4.2 Intercompany Elimination

Intercompany accounts (intercompany segment not equal to 000) are eliminated in consolidation so that the FR Y-9C reflects only external positions. The intercompany clearing sub-range (940000 to 949999) must net to zero across the consolidated group at each close; a nonzero net intercompany balance is a reconciling item escalated under MJD-FIN-0002.

## 5. Period Close and Locking

### 5.1 Subledger Cutoff

Each subledger has a defined cutoff time at period close. After cutoff, the subledger is closed and its control account in the GL is reconciled to subledger detail under MJD-FIN-0002.

### 5.2 GL Lock

After all subledgers are reconciled and management adjustments are posted, the Finance Controller locks the GL for the period. A locked period accepts no further postings. A correction to a locked period is made only by a documented prior-period adjustment with Controller approval, never by reopening the lock silently.

### 5.3 Close Calendar

The financial close targets a five business day soft close and a ten business day hard close after month end. The quarterly hard close must complete with sufficient lead time to support the regulatory filing deadlines in MJD-FIN-0003.

#### 5.3.1 Detailed Close Steps

| Business day | Step | Owner |
|---|---|---|
| BD 1 | Subledger cutoffs enforced, automated feeds posted | GL Accountant |
| BD 1 to 2 | Tier 1 (daily) accounts reconciled per MJD-FIN-0002 | Reconcilers |
| BD 2 to 4 | Accruals and allocation journals posted | GL Accountant |
| BD 5 | Soft close, draft trial balance to Controller | Finance Controller |
| BD 5 to 7 | Tier 2 control-account reconciliations signed | Reconcilers |
| BD 7 to 9 | Management adjustments, variance review | Finance Controller |
| BD 8 to 10 | Tier 3 reconciliations signed | Reconcilers |
| BD 10 | Hard close, GL locked, suspense confirmed zero | Finance Controller |

#### 5.3.2 Close Dependencies for Filing

The hard close at BD 10 is the precondition for the regulatory filing milestone calendar in MJD-FIN-0003. A delayed hard close compresses the filing buffer and is escalated to the Chief Financial Officer if it threatens the FR Y-9C or Call Report deadline.

## 6. Exceptions and Escalation

### 6.1 Requesting an Exception

Any deviation from this policy, including an out-of-range account, a posting to a locked period outside the prior-period adjustment process, or a temporary segregation-of-duties overlap, requires a written exception request to the Finance Controller. The request states the business reason, the duration, and the compensating control.

### 6.2 Approval Authority

| Exception Type | Approver |
|---|---|
| Temporary segregation-of-duties overlap | Finance Controller |
| Out-of-range or nonstandard account | Finance Controller |
| Mapping change mid-quarter | Finance Controller and Head of Regulatory Reporting |
| Reopening a locked period | Chief Financial Officer |

### 6.3 Escalation Triggers

The following conditions are escalated immediately to the Finance Controller and, where indicated, to the Chief Financial Officer and the Risk function:

1. A suspense or clearing account that does not clear to zero within the window defined in MJD-FIN-0002. Escalate to Controller.
2. A material unmapped balance discovered during the pre-filing integrity check. Escalate to Controller and Head of Regulatory Reporting.
3. Evidence of posting to a parent account, a retired account, or a locked period without authorization. Escalate to Controller, CFO, and Risk; treat as a potential control failure and notify under MJD-FIN-0005.
4. Any indication that a suspense account is being used to manage earnings. Escalate to CFO and Risk as a potential fraud indicator.

## 7. Roles and Responsibilities

**Finance Controller.** Owns this policy. Approves account creation, structural changes, mapping changes, and GL locking. Final approver for most exceptions.

**Chief Financial Officer.** Approves the reopening of locked periods and prior-period adjustments above materiality. Receives escalations involving potential earnings management.

**General Ledger Accountant.** Performs functional review of account requests, executes period-close postings, and maintains the COA day to day.

**Regulatory Reporting Analyst.** Owns the regulatory mapping table, performs the pre-filing mapping integrity check, and coordinates mapping changes with the filing calendar in MJD-FIN-0003.

**Risk Analyst.** Consumes GL data for risk aggregation and receives escalations relating to suspense misuse or control failures.

**Operations Analyst.** Ensures transaction processing feeds the correct subledgers and supports research on suspense items per MJD-FIN-0002.

## 8. Related Documents

- MJD-FIN-0002, Account Reconciliation Procedure. Defines the reconciliation cadence and the suspense-account clearing window referenced throughout this policy.
- MJD-FIN-0003, Regulatory Reporting Procedure (Call Report / FR Y-9C). Consumes the regulatory mapping defined here and depends on the GL close calendar.
- MJD-FIN-0005, Audit Trail and Evidence Standard. Defines the evidentiary standard for the GL change log, approvals, and exception records this policy requires.
- MJD-FIN-0004, Expense and Budget Approval Policy. Governs approval of noninterest expense that posts to the 700000 range.
- MJD-RSK-0001, Enterprise Risk Management Framework. Provides the risk aggregation context that consumes GL balances.

## 9. Regulatory References

The following real frameworks are named for realism. Every threshold and procedure built around them in this fictional document is synthetic and must not be used as compliance guidance.

- FFIEC Consolidated Reports of Condition and Income (Call Report) Instructions, FFIEC 031 and 041.
- Federal Reserve FR Y-9C, Consolidated Financial Statements for Holding Companies, Instructions.
- US GAAP, ASC 105 Generally Accepted Accounting Principles.
- Gramm-Leach-Bliley Act, Safeguards Rule, as it relates to protecting financial records.
- Sarbanes-Oxley Act Section 404, internal control over financial reporting.

## 10. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2023-02-01 | Finance Controller | Initial COA and GL policy. |
| 2.0.0 | 2024-06-15 | Finance Controller | Added twenty-character segmented account string and reserved suspense block. |
| 2.1.0 | 2025-01-10 | Finance Controller | Added pre-filing mapping integrity check and tied to FR Y-9C cycle. |
| 2.2.0 | 2025-08-20 | Finance Controller | Strengthened segregation-of-duties enforcement and exception authority table. |
| 2.3.0 | 2026-01-15 | Finance Controller | Clarified suspense escalation triggers and aligned close calendar to regulatory deadlines. |
