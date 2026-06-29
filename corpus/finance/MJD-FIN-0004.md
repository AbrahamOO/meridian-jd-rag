---
doc_id: MJD-FIN-0004
title: Expense and Budget Approval Policy
department: FINANCE
doc_type: POLICY
classification: INTERNAL
owner_role: FINANCE_CONTROLLER
allowed_roles: [FINANCE_CONTROLLER, OPERATIONS_ANALYST]
effective_date: 2026-01-20
version: 2.0.0
review_cycle_months: 12
regulatory_refs: ["Sarbanes-Oxley Act Section 404", "US GAAP ASC 105", "COSO Internal Control Integrated Framework", "IRS Accountable Plan Rules"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Expense and Budget Approval Policy

## Purpose and Scope

### Purpose

This policy defines how Meridian John Doe Financial (Meridian J.D.) plans, approves, commits, and controls spending. It establishes the annual budget process, the delegation-of-authority approval thresholds for expenditures, the rules for purchase commitments and contracts, the treatment of travel and entertainment expense, and the controls that keep actual spend within authorized budget. The goal is to ensure that every dollar of noninterest expense is authorized by someone with the authority to approve it, recorded to the correct account, and visible against budget.

### Scope

This policy applies to all noninterest expenditures across every department, branch, and consolidation unit, including operating expense, capital expenditure, vendor contracts, purchase orders, corporate card spending, and employee expense reimbursement. It applies to all employees who request, approve, or process spending.

This policy works alongside, and does not override, the controls in MJD-FIN-0001 governing how expense posts to the general ledger, nor the reconciliation controls in MJD-FIN-0002. Procurement of technology and the security review of vendors are governed by their own technology standards; this policy governs the financial approval. It is classified INTERNAL.

### Audience

The readers are finance controllers and budget owners who set and monitor budgets, and operations analysts who process and approve day-to-day expenditures.

## Definitions

**Approval Authority.** The maximum dollar amount an individual may approve for a single expenditure based on their delegated authority level.

**Budget Owner.** The manager accountable for a department or cost center budget.

**Capital Expenditure (CapEx).** Spending on assets that provide future economic benefit and are capitalized, not expensed immediately.

**Commitment.** A binding obligation to spend, created by a purchase order or signed contract, recorded against budget before the invoice arrives.

**Delegation of Authority (DoA).** The schedule that assigns approval authority levels to roles.

**Operating Expenditure (OpEx).** Spending consumed in the current period and expensed as incurred.

**Purchase Order (PO).** A document authorizing a purchase that creates a commitment against budget.

**Travel and Entertainment (T&E).** Employee expenses for travel, lodging, meals, and client entertainment, typically reimbursed or charged to a corporate card.

**Variance.** The difference between actual or committed spend and budget for a period.

## 1. Annual Budget Process

### 1.1 Budget Cycle

The annual budget is built in the fourth quarter for the following fiscal year. Each budget owner submits a department budget by natural account (per MJD-FIN-0001) and cost center. The Finance Controller consolidates, the executive team reviews, and the Chief Financial Officer approves the consolidated budget before fiscal year start.

### 1.2 Budget Granularity

Budgets are set at the cost-center and natural-account level so that actuals post directly comparable to budget. A budget line with no natural-account mapping is rejected back to the owner.

### 1.3 Reforecast

A formal reforecast is performed at mid-year. Material in-year changes to a department budget outside the reforecast require a budget transfer approved per section 4.

#### 1.3.1 Budget Calendar

| Step | Owner | Timing |
|---|---|---|
| Budget guidance and targets issued | CFO | Early Q4 |
| Department budgets submitted | Budget Owners | Mid Q4 |
| Consolidation and challenge | Finance Controller | Late Q4 |
| Executive review | Executive Team | Late Q4 |
| Board approval where required | Board | Before fiscal year start |
| Mid-year reforecast | Finance Controller | End of Q2 |

#### 1.3.2 Operating versus Capital Budgets

The operating budget covers OpEx (700000 range natural accounts in MJD-FIN-0001). The capital budget covers CapEx projects and is approved separately by total project cost. A project may not draw operating budget to fund capital spend or the reverse; a misclassification is corrected by a reclassifying journal under MJD-FIN-0001.

### 1.4 Zero-Based Justification

Discretionary expense categories above a threshold set annually by the CFO are budgeted zero-based: the owner justifies the full amount from a zero baseline rather than carrying the prior year forward. This control prevents budget creep in discretionary categories such as travel, events, and professional services.

## 2. Delegation of Authority and Approval Thresholds

### 2.1 Approval Matrix

Every expenditure requires approval at or above the level set by its dollar amount. Approval is by an individual with sufficient delegated authority who is not the requester (no self-approval).

| Single expenditure amount (USD) | Minimum approver |
|---|---|
| Up to 1,000 | Team Lead or Manager |
| 1,001 to 10,000 | Department Director |
| 10,001 to 50,000 | Vice President and Budget Owner |
| 50,001 to 250,000 | Finance Controller |
| 250,001 to 1,000,000 | Chief Financial Officer |
| Above 1,000,000 | CFO and Chief Executive Officer (and Board where policy requires) |

### 2.2 No Self-Approval

No individual may approve their own expenditure, their own expense report, or a payment to an entity in which they have a personal interest. A conflict of interest is disclosed and the approval is routed one level higher.

### 2.3 No Splitting

Splitting a single economic purchase into multiple smaller requests to stay under an approval threshold is prohibited and is an escalation trigger under section 5.

### 2.4 Budget Availability

An expenditure is approved only if budget is available in the relevant cost center and natural account, or a budget transfer has been approved. Approving spend with no budget coverage requires the next-higher authority level.

### 2.5 Three-Way Match for Invoices

An invoice is paid only after a three-way match: the purchase order (authorization), the receipt of goods or services (delivery), and the invoice (the bill) agree on quantity and amount within tolerance. A mismatch holds the payment for research. The three-way match is the control that prevents payment for goods not received or at a price not agreed.

| Match element | Source | Confirms |
|---|---|---|
| Purchase order | Procurement | The purchase was authorized |
| Goods or services receipt | Requesting department | The purchase was delivered |
| Invoice | Vendor | The amount billed |

### 2.6 Worked Approval Example

A department director requests new analytics software at a total contract value of 42,000 USD over two years (18,000 year one, 24,000 year two). Because the contract value (not the first-year value) sets the authority level, the request requires Vice President and Budget Owner approval (the 10,001 to 50,000 band), not Department Director approval. A purchase order is raised because the amount exceeds 5,000 USD, creating a commitment of 42,000 USD against the technology cost center. Splitting the contract into two annual 21,000 USD requests to keep each under the VP threshold would be a prohibited split under section 2.3 and an escalation trigger.

## 3. Commitments, Contracts, and Capital

### 3.1 Purchase Orders and Commitments

A purchase above five thousand US dollars requires a purchase order before the commitment is made. The PO creates a commitment recorded against budget so that available budget reflects obligations, not just invoiced spend.

### 3.2 Contracts

A contract that creates a multi-period obligation is approved at the authority level for its total contract value, not its first-year value. Contract value is the sum of all committed periods including renewals reasonably expected to be exercised.

### 3.3 Capital Expenditure

CapEx follows the same approval matrix by total project cost and additionally requires a documented business case for projects above fifty thousand US dollars. Capitalization versus expense treatment is determined under MJD-FIN-0001 account classification.

#### 3.3.1 Business Case Contents

A CapEx business case states the expected benefit, the total cost of ownership including ongoing operating cost, the alternatives considered, and the payback or return measure. The Finance Controller reviews the business case for cost realism before the approval routes to the authority level set by total project cost.

#### 3.3.2 Capitalization Threshold

An item is capitalized rather than expensed when its cost is at least 5,000 USD and its useful life is more than one year; otherwise it is expensed in the period. The threshold and the classification are applied consistently with MJD-FIN-0001 so that the GL, the budget, and the regulatory reporting in MJD-FIN-0003 agree on what is capital and what is expense.

### 3.4 Vendor and Payment Controls

#### 3.4.1 New Vendor Setup

A new vendor is set up only with verified banking details, and the verification is performed by someone other than the person who entered the vendor (segregation of duties). A change to existing vendor banking details requires call-back verification to a known contact, a control against payment-redirection fraud.

#### 3.4.2 Duplicate Payment Prevention

The payables system blocks a payment that matches an existing payment on vendor, amount, and invoice number. An override requires Finance Controller approval and is logged under MJD-FIN-0005.

## 4. Budget Transfers and Monitoring

### 4.1 Budget Transfer

A transfer of budget between cost centers or natural accounts is approved by both affected budget owners and the Finance Controller. Transfers do not increase total approved spend; they move authorized capacity.

### 4.2 Variance Monitoring

The Finance Controller reports actual and committed spend against budget monthly. A cost center projected to exceed its annual budget by more than five percent is flagged and the budget owner must present a corrective plan or a justified transfer.

### 4.3 Spend Freeze

In a period of financial stress, the CFO may impose a discretionary spend freeze. During a freeze, only contractually required and regulatory-mandated spend is approved; all discretionary spend requires CFO approval regardless of amount.

### 4.4 Accruals at Period End

At each period end, budget owners confirm goods or services received but not yet invoiced so that the expense is accrued to the correct period under MJD-FIN-0001. An owner who fails to flag a known accrual distorts both the financial statements and the budget variance; missed accruals discovered later are treated as a process defect.

### 4.5 Commitment Reporting

Available budget is reported as budget minus actual spend minus open commitments, so that an owner sees true remaining capacity rather than only invoiced spend. A commitment that will not be fulfilled is released by the owner so that the freed budget becomes available again; stale commitments are reviewed quarterly.

## 5. Travel and Entertainment

### 5.1 Reimbursable Expense

T&E is reimbursable when it is a legitimate business expense, supported by an itemized receipt, submitted within thirty calendar days, and approved by the employee's manager. Personal expenses are never reimbursable.

#### 5.1.1 Per-Category Rules and Limits

| Category | Rule |
|---|---|
| Airfare | Economy class for flights under six hours; itemized receipt required |
| Lodging | Standard room at a reasonable rate for the location; folio receipt required |
| Meals | Reasonable and actual; itemized receipt required above 25 USD |
| Ground transport | Most economical reasonable option; receipt required above 25 USD |
| Client entertainment | Business purpose and attendees documented; pre-approval above 500 USD |

Amounts that exceed a category norm without a documented reason are reduced to the norm on review. Alcohol, personal entertainment, fines, and upgrades for personal comfort are not reimbursable.

#### 5.1.2 Approval Routing

An expense report is approved by the employee's direct manager, who must not be a subordinate or peer the employee approves in return (no reciprocal approval). An expense report of an executive is approved one level up. Any single expense line above 1,000 USD additionally routes to the budget owner for the charged cost center.

### 5.2 Corporate Card

Corporate card transactions are reconciled monthly by the cardholder and approved by the manager. An unreconciled card statement beyond two consecutive cycles results in card suspension and escalation to the Finance Controller.

#### 5.2.1 Card Issuance and Limits

A corporate card is issued only with manager and Finance approval, with a credit limit set to the cardholder's role and need. Limits are reviewed annually and on role change. A card is cancelled immediately on the cardholder's departure, and the final statement is reconciled before the card is closed.

#### 5.2.2 Prohibited Card Use

Corporate cards may not be used for cash advances, personal purchases, or to circumvent the procurement and approval process in section 2. A personal charge made in error is repaid promptly; a pattern of personal use is an escalation trigger under section 6.

### 5.3 Receipts and Substantiation

Expenses must meet substantiation standards consistent with IRS accountable-plan rules. Unsubstantiated amounts are not reimbursed and, if already paid by corporate card, are recovered from the employee.

#### 5.3.1 Retention of Expense Evidence

Approved expense reports, receipts, and card reconciliations are retained as evidence under MJD-FIN-0005. The evidence ties each reimbursement to its approval and its business purpose, so that a later review can confirm the expense was legitimate, authorized, and correctly charged.

## 6. Exceptions and Escalation

### 6.1 Requesting an Exception

A deviation from the approval matrix, an emergency purchase made before approval, or an out-of-budget commitment requires a written exception to the Finance Controller stating the business reason and the corrective step. Emergency purchases are ratified within five business days or reversed.

### 6.2 Escalation Triggers

| Trigger | Escalates to |
|---|---|
| Suspected purchase splitting to evade thresholds | Finance Controller and Internal Audit |
| Self-approval or undisclosed conflict of interest | Finance Controller and CFO |
| Cost center projected over budget by more than 5 percent | Budget Owner then CFO |
| Spend during an active freeze without approval | Chief Financial Officer |
| Repeated unsubstantiated T&E by the same employee | Finance Controller and Human Resources |

### 6.3 Control Exceptions Register

All exceptions are logged in the control exceptions register and retained as evidence under MJD-FIN-0005. A pattern of exceptions by the same approver or requester is reviewed by Internal Audit.

## 7. Roles and Responsibilities

**Finance Controller.** Owns this policy. Consolidates the budget, approves budget transfers, monitors variance, approves expenditures in the 50,001 to 250,000 band, and adjudicates exceptions.

**Chief Financial Officer.** Approves the consolidated budget, approves expenditures above 250,000, may impose a spend freeze, and receives conflict and freeze-breach escalations.

**Budget Owner.** Accountable for the department budget, justifies variances, and approves transfers affecting their cost center.

**Department Director and VP.** Approve expenditures within their delegated authority and ensure budget availability before approving.

**Operations Analyst.** Processes purchase orders, expense reports, and corporate card reconciliations, and routes approvals to the correct authority level.

**Internal Audit.** Reviews patterns of exceptions, splitting, and self-approval.

## 8. Related Documents

- MJD-FIN-0001, Chart of Accounts and GL Policy. Governs the natural accounts (700000 range) that noninterest expense posts to and the capitalization classification.
- MJD-FIN-0002, Account Reconciliation Procedure. Governs reconciliation of corporate card and accounts payable balances arising from spend.
- MJD-FIN-0005, Audit Trail and Evidence Standard. Defines the evidentiary standard for approvals, exceptions, and the control exceptions register.
- MJD-RSK-0003, Operational Risk Procedure. Consumes control-exception patterns as operational risk indicators.
- MJD-TEC-0008, Change Management and Release Policy. Governs technology change approvals that frequently accompany technology spend.

## 9. Regulatory References

The following real frameworks are named for realism. Every threshold and procedure built around them in this fictional document is synthetic and must not be used as compliance guidance.

- Sarbanes-Oxley Act Section 404, internal control over financial reporting, including spend authorization controls.
- US GAAP, ASC 105 Generally Accepted Accounting Principles, for expense versus capital treatment.
- COSO Internal Control Integrated Framework, control activities.
- IRS accountable-plan rules for substantiation of reimbursed business expense.

## 10. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2023-05-01 | Finance Controller | Initial expense and budget approval policy with flat approval thresholds. |
| 1.5.0 | 2024-09-10 | Finance Controller | Added commitments, purchase orders, and contract total-value rule. |
| 2.0.0 | 2026-01-20 | Finance Controller | Reworked delegation-of-authority matrix, added spend freeze, no-splitting, and control exceptions register. |
