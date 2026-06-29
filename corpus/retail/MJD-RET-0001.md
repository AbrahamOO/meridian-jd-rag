---
doc_id: MJD-RET-0001
title: Branch Operations Manual
department: RETAIL
doc_type: GUIDELINE
classification: INTERNAL
owner_role: Head of Retail Banking
allowed_roles: [BRANCH_STAFF, OPERATIONS_ANALYST]
effective_date: 2025-10-01
version: 3.2.0
review_cycle_months: 12
regulatory_refs: ["12 CFR 1005 (Regulation E)", "12 CFR 1030 (Regulation DD)", "31 CFR 1010.311 (CTR filing)", "12 CFR 229 (Regulation CC)", "FFIEC BSA/AML Examination Manual"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Branch Operations Manual

## Purpose and Scope

This manual is the day-to-day operating reference for the retail branch network of Meridian John Doe Financial (Meridian J.D.). It tells a teller, a personal banker, and a branch manager how the branch floor runs from the moment the doors open until the night drop is sealed. It pulls the bank-wide control thresholds that matter at the counter into one place a branch employee can reach without leaving the floor, and it points to the authoritative source document for each control so that the branch never becomes the system of record for a number that lives somewhere else.

This manual applies to:

- All staffed retail branches, in-store branches, and limited-service offices of Meridian J.D.
- All branch personnel: Branch Staff (tellers, senior tellers, personal bankers), the Branch Manager, and the Assistant Branch Manager.
- Operations Analysts who support the branch network, perform second-line review, and adjudicate items escalated off the floor.

This manual does not redefine bank-wide limits. Where a transaction limit, a dual-approval trigger, or a hold schedule is stated here, it is reproduced from its owning document for floor convenience and the owning document controls in the event of any difference. The authoritative limit source is MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix. Cash-specific vault and drawer controls are owned by MJD-RET-0002 Cash Handling and Vault Procedure. Customer complaints are handled under MJD-RET-0003 Customer Complaint Handling Procedure. This manual coordinates those controls on the floor; it does not supersede them.

## Definitions

- **Branch Floor.** The customer-facing service area of a branch, including the teller line, the platform desks, and the self-service vestibule.
- **Teller.** A Branch Staff member who handles cash and processes over-the-counter transactions at an assigned drawer.
- **Personal Banker.** A platform-side Branch Staff member who opens accounts, originates service requests, and handles non-cash relationship transactions.
- **Branch Manager (BM).** The senior on-site officer accountable for the branch, its controls, its cash, and its staff.
- **Dual Approval.** A control requiring a second authorized employee to independently review and approve a transaction before it is released. The approver may not be the originator.
- **Override.** A supervisor action that releases a transaction the system has blocked or flagged, recorded with the supervisor identity and a reason code.
- **Hold.** A delay placed on availability of deposited funds under Regulation CC and bank policy.
- **Currency Transaction Report (CTR).** A report filed for cash transactions in currency that aggregate above the federal reporting threshold in a single business day by or on behalf of one person.
- **Cash Item.** Currency and coin handled at the drawer or in the vault.
- **Daily Wire Limit.** The dollar ceiling on an outbound wire a branch may release before the dual-approval control applies, as set in MJD-OPS-0007.

## 1. Branch Opening and Closing

### 1.1 Opening procedure

1.1.1 Two employees must be present before the vault is opened. The single-employee rule prohibits any one person from being alone with the open vault or the teller cash. Dual presence is a control, not a courtesy.

1.1.2 The opening employees perform a dual-custody vault open, record the vault open time, and verify the alarm panel returned to a disarmed-occupied state without fault.

1.1.3 Each teller draws a starting cash buffer from the vault and counts it before accepting the first customer. The starting buffer for a standard drawer is **$5,000** and may be raised to **$8,000** for a high-volume drawer with Branch Manager approval. Drawer and vault cash ceilings are governed by MJD-RET-0002.

1.1.4 The Branch Manager confirms the prior-day balancing exceptions, if any, are cleared or carried with a documented reason before the floor opens.

1.1.5 The opening employees walk the branch before unlocking the customer doors. They confirm the ATM and self-service vestibule are operational, the night drop is intact and shows no sign of tampering, the surveillance recorder shows a green status, and the duress and hold-up alarm test (where scheduled) returned a confirmed acknowledgement from the monitoring center. A surveillance recorder that is not recording is a branch-open blocker. The branch does not open the teller line until coverage is restored, or until the Branch Manager records a documented compensating control and notifies Operations and Security.

1.1.6 The opening checklist is completed in the branch system, not on paper, so that the open time, the two opening employee identities, and any exception are captured as an auditable record. An open performed without the two-employee record is itself a control exception.

### 1.2 Mid-day controls

1.2.1 The Branch Manager performs a mid-day cash and control check during a normal business day, confirming no drawer is over its ceiling, no teller has been left alone with the vault, and the official-check stock count still reconciles. The check is recorded.

1.2.2 A staffing change during the day, such as a teller going on break or a shift handover, is a transfer of custody. The outgoing and incoming employees count the drawer together and both confirm the position before custody passes. An unconfirmed handover is not a completed handover.

1.2.3 If staffing falls below two employees at any time, the branch cannot open the vault and cannot perform any dual-custody transaction. The branch operates teller-line only within drawer limits, or closes early with Operations notification.

### 1.4 Closing procedure

1.4.1 Each teller balances the drawer to the system position. A drawer is in balance when the counted cash equals the system cash within the tolerance in Section 4.2.

1.4.2 Excess cash above the drawer ceiling is bought back to the vault under dual custody. No teller leaves the branch with the drawer over its ceiling.

1.4.3 The Branch Manager performs the end-of-day vault settlement, confirms the branch cash position against MJD-RET-0002 vault limits, and seals the night drop under dual custody.

1.4.4 Official-check and money-order stock is reconciled, the controlled-inventory log is closed for the day, and any variance is investigated before the staff leaves.

1.4.5 The branch is armed and exited under the two-person rule. The last two employees leave together. The system arming time and the two closing employee identities are recorded.

### 1.5 Worked example: a short-staffed afternoon

A branch opens with three employees. After lunch, two of the three are out at the same time, leaving one employee. From that moment the vault is closed: the remaining employee serves customers from the drawer only, declines any transaction that would require a vault buy (for example a large cash withdrawal above the drawer position), and asks the customer to return when staffing is restored or refers the customer to a nearby branch. The Branch Manager is notified and decides whether to close early. No exception lets one employee open the vault alone; the single-employee prohibition has no dollar threshold and no override.

## 2. Over-the-Counter Transactions

### 2.1 Deposits

2.1.1 Tellers accept cash, check, and mixed deposits to accounts in good standing. The teller verifies the deposit slip total against the items presented and corrects any discrepancy with the customer present.

2.1.2 Funds availability follows the Regulation CC hold schedule. The standard next-business-day availability applies to the first **$275** of a non-next-day check deposit; the remainder follows the bank's case-by-case and exception hold rules. A new-account relationship (open less than 30 days) is subject to the new-account hold schedule.

2.1.3 A cash deposit that, alone or aggregated with other cash activity by or for the same person that day, exceeds **$10,000** in currency triggers Currency Transaction Report handling. The teller does not decline the transaction; the teller completes the CTR data capture and routes it to the Operations CTR queue. CTR preparation and filing are governed by MJD-CMP-0003 Currency Transaction Report (CTR) Procedure.

2.1.4 A deposited check that the teller has specific reason to doubt will be paid (for example, a stale-dated item, a post-dated item, a check returned previously on the same maker, or a large item to a new account) may be placed on an exception hold under Regulation CC. An exception hold requires a documented reason and a hold notice given to the customer at the time of deposit stating the reason and the date funds will be available. A hold is never placed to penalize a customer or without a Regulation CC-permitted reason.

2.1.5 The branch funds-availability summary, reproduced for the floor, is:

| Deposit type | Availability |
|---|---|
| Cash deposited in person to an employee | Next business day |
| Electronic direct deposit | Day of receipt |
| First $275 of a non-next-day check deposit | Next business day |
| US Treasury, on-us, cashier or certified check (in person to the payee) | Next business day |
| Remaining local check funds (standard) | Second business day |
| Exception or new-account hold | Per the hold notice given to the customer |

### 2.2 Withdrawals and check cashing

2.2.1 A customer cash withdrawal is paid from the drawer up to the drawer ceiling. A withdrawal that would breach the drawer ceiling is filled with a vault buy under dual custody per MJD-RET-0002.

2.2.2 On-us check cashing for a Meridian J.D. customer is permitted up to the available balance. Cashing an on-us check for a non-customer requires positive identification, a thumbprint signature for items above **$1,500**, and Branch Manager approval for items above **$3,500**.

2.2.3 A withdrawal of currency above **$10,000** in a single business day by or for one person triggers CTR handling identical to Section 2.1.3.

2.2.4 A large cash withdrawal request that the branch cannot fill from the vault on hand is ordered in advance. The branch asks for one business day of notice for a currency withdrawal above the standard vault working position so cash can be ordered without breaching the vault floor in MJD-RET-0002. The branch never breaches the vault floor to satisfy a single withdrawal.

2.2.5 A withdrawal that appears to be made under third-party pressure, or that the customer seems confused about, is paused for a private conversation and, where elder or vulnerable-adult exploitation is suspected, escalated under Section 6 and MJD-RET-0003. Protecting a customer from apparent exploitation takes priority over completing the transaction quickly.

### 2.3 Negotiable instruments

2.3.1 Tellers issue cashier's checks and money orders against collected funds only. A cashier's check above **$10,000** requires personal banker review of the funding source and is logged.

2.3.2 Official-check stock is controlled inventory. It is logged in and out under dual custody and reconciled at end of day. A missing or out-of-sequence official-check serial is treated as a potential loss event and reported to Operations and Fraud Risk the same day.

2.3.3 A money order is issued up to the per-item limit of **$1,000** and is sold only for immediately available funds. A request to buy multiple money orders that aggregate above the CTR currency threshold with cash is handled as a reportable cash transaction under Section 2.1.3.

### 2.4 Stop payments and holds

2.4.1 A customer stop-payment request on a check is taken with the item details (number, amount, payee, date) and entered before the item presents. The branch explains that a stop payment does not guarantee the item will not be paid if it has already cleared, and discloses the stop-payment fee under the current Regulation DD disclosure.

2.4.2 A legal hold, levy, or garnishment served on the branch is never acted on at the counter. It is routed immediately to Operations and Legal for handling; branch staff do not freeze, release, or remit funds in response to a served order without that handling.

## 3. Wires and Outbound Funds Transfers from the Branch

### 3.1 Branch wire intake

3.1.1 A customer outbound wire request is taken on the bank's wire request form with the customer's wet or verified electronic signature. The personal banker validates the customer identity, the account ownership, and the callback requirement in Section 3.3.

3.1.2 The branch keys the wire into the wire platform but does not release it. Release is an Operations function. Branch intake and Operations release together implement the separation of duties required by MJD-OPS-0004 Wire Transfer Operations Runbook.

### 3.2 Daily wire limit and dual approval at the branch

3.2.1 A single outbound customer wire of **$25,000 or less** may be submitted by one authorized personal banker for Operations release without a second branch approver, subject to the standard callback in Section 3.3.

3.2.2 A single outbound wire **above $25,000**, or branch outbound wires that **aggregate above $50,000 for one customer in one business day**, require branch dual approval before submission. The second approver must be a different authorized employee, and at least one of the two must be the Branch Manager or Assistant Branch Manager. These thresholds are reproduced from MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix, which is the controlling source; if MJD-OPS-0007 and this manual differ, MJD-OPS-0007 governs.

3.2.3 An outbound wire above the branch submission ceiling of **$250,000** may not be submitted from the branch at all. It is escalated to the Operations wire desk for direct handling under MJD-OPS-0004. The branch never releases a wire and never exceeds its submission ceiling by splitting a single instruction into multiple wires; structuring to avoid a limit is itself a control breach reportable under Section 6.

### 3.3 Callback verification

3.3.1 Every outbound wire above **$5,000** to a new or changed beneficiary requires an outbound callback to the customer on a previously verified phone number before submission. The callback is logged with the employee identity, the time, and the verified phone number.

3.3.2 A wire request received by email or fax is treated as high risk for business email compromise and always requires a callback regardless of amount.

3.3.3 The callback is made to a phone number already on the customer record, never to a number written on the wire request itself. A request to "use the new number on the form" is a known fraud pattern and is refused; the banker calls the number of record.

### 3.4 International and recurring wires

3.4.1 An outbound international wire is intaken with the beneficiary bank SWIFT or BIC, the IBAN or local account number, the beneficiary full name and address, and the purpose of payment. The same daily wire limit and dual-approval thresholds in Section 3.2 apply, and the international destination raises the sanctions-screening sensitivity handled by Operations under MJD-OPS-0008 Sanctions (OFAC) Screening Procedure.

3.4.2 A first-time wire to a high-risk or sanctioned-adjacent jurisdiction is escalated to Operations before submission regardless of amount. The branch does not assess sanctions risk itself; it ensures the screen is invoked and does not submit while a potential match is unresolved.

### 3.5 Worked example: a $40,000 customer wire

A long-standing customer asks to send a $40,000 wire to a contractor for a home renovation, to a beneficiary the customer has not paid before. The amount is above the $25,000 single-wire threshold, so branch dual approval is required: the personal banker prepares the wire and the Branch Manager independently reviews and approves it as the second approver. Because the beneficiary is new and the amount is above $5,000, a callback to the customer on the phone number of record is required and logged. The branch keys and submits the wire for Operations release; the branch does not release it. The thresholds applied here are reproduced from MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix, which governs if it and this manual ever differ.

## 4. Cash Controls on the Floor

### 4.1 Drawer and vault ceilings

The floor-facing cash ceilings are summarized here for convenience and are owned by MJD-RET-0002 Cash Handling and Vault Procedure.

| Position | Standard cash ceiling | Action when exceeded |
|---|---|---|
| Standard teller drawer | $10,000 | Buy excess to vault under dual custody |
| High-volume teller drawer | $15,000 | Buy excess to vault under dual custody |
| Branch vault (standard branch) | $250,000 | Order cash shipment out; notify Operations |

### 4.2 Balancing tolerance

4.2.1 A drawer is in balance within a tolerance of **plus or minus $5.00**. An out-of-tolerance difference is a balancing exception.

4.2.2 A balancing exception of **$25.00 or more**, or any pattern of repeated smaller differences from one teller, is escalated to the Branch Manager same day and logged for Operations review.

4.2.3 A cash shortage or overage above **$250.00** is reported to Operations and to the Fraud Risk function the same business day under MJD-RSK-0007 Fraud Risk Management Procedure.

### 4.3 Single-employee prohibition

No employee is ever alone with open vault cash. Every vault access is dual custody. This rule is absolute and is the most-tested branch control.

## 5. Account Servicing on the Platform

### 5.1 Account opening

Personal bankers open accounts under MJD-OPS-0005 Account Onboarding Workflow and collect and verify identity under MJD-OPS-0001 Customer Identification Program (CIP) Procedure. The branch does not open an account while a sanctions potential match is unresolved.

### 5.2 Maintenance and disclosures

5.2.1 Rate, fee, and account-term disclosures are delivered under Regulation DD at account opening and on change. The branch uses only the current disclosure version from the document library.

5.2.2 Address, ownership, and signer changes above the platform self-service scope require a second-employee review when they alter who controls the funds.

### 5.3 Disputes and errors

A customer assertion of an unauthorized or erroneous electronic transaction is an error claim under Regulation E and is intaken under MJD-OPS-0006 Dispute and Chargeback Resolution Procedure and, where it is also a complaint, logged under MJD-RET-0003 Customer Complaint Handling Procedure. The branch acknowledges the customer at intake and does not promise an outcome.

### 5.4 Overrides and supervisor authority

5.4.1 A system block (for example a negative-balance withdrawal, a hold release, or a fee waiver above the platform self-service amount) requires a supervisor override. The override records the supervisor identity, a reason code, and the dollar amount. A teller never overrides the teller's own transaction.

5.4.2 Supervisor override authority is delegated and tiered. A fee waiver up to **$50** may be approved by a senior teller; above $50 up to **$250** by the Assistant Branch Manager; above $250 by the Branch Manager; above **$1,000** by Operations. Higher amounts follow the delegation matrix in MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix.

5.4.3 Repeated overrides of the same type from one employee are a control signal reviewed by Operations monthly. Override volume is a monitored branch metric.

### 5.5 Dormant and deceased accounts

5.5.1 An account with no customer-initiated activity for the dormancy period is flagged dormant; reactivation requires identity reverification under MJD-OPS-0001 Customer Identification Program (CIP) Procedure. Unclaimed property escheatment timelines are governed by Operations, not by the branch.

5.5.2 On notice of a customer death, the branch does not release funds at the counter. It records the notice, restricts disbursing activity, and routes the estate to Operations for the documentary process. Branch staff express condolences and explain the process; they do not advise on estate matters.

### 6.1 Recognizing reportable activity

Branch Staff watch for cash structuring (deliberately keeping currency transactions just under $10,000), reluctance to provide identification for a reportable transaction, and third-party pressure on a customer. Staff never tip off a customer that activity may be reported.

### 6.2 Escalation path

6.2.1 The employee raises the concern to the Branch Manager.

6.2.2 The Branch Manager refers the matter to Compliance through the referral channel. Compliance makes any Suspicious Activity Report determination under MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure. The branch never decides whether to file and never tells the customer a referral was made.

## 7. Synthetic Test Record

The following is a clearly marked fictional test record used only for ingestion and verification testing. It is not a real customer or a real transaction.

> TEST RECORD (synthetic, not real): Branch "Testville Main #0000", teller "T-DOE-SAMPLE", customer "Avery Q. Doe-Example", account "TEST-0000000001", outbound wire request $24,999.00 to beneficiary "Sample Payee (fabricated)". Source: fabricated for demonstration.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Teller (Branch Staff) | Handle cash within drawer ceiling, balance to tolerance, capture CTR data, escalate suspicious activity |
| Personal Banker (Branch Staff) | Open and service accounts, intake wires within submission limits, perform callbacks, log complaints |
| Assistant Branch Manager | Serve as dual approver, perform overrides within delegated authority, support vault dual custody |
| Branch Manager | Own branch controls and cash position, approve exceptions, refer suspicious activity, settle the vault |
| Operations Analyst | Release wires, adjudicate escalations, review balancing exceptions, monitor floor control metrics |
| Head of Retail Banking | Own this manual, set branch operating standards, report network metrics |

## Exceptions and Escalation

- A floor exception (for example, an out-of-tolerance drawer carried overnight or an expired-ID override on check cashing) requires Branch Manager approval and is logged in the branch exception register with a reason code and a follow-up date.
- A control the floor cannot resolve within its delegated authority is escalated to the supporting Operations Analyst, then to the Head of Retail Banking.
- Any suspected internal fraud, robbery, or duress event follows the security and incident path and is reported the same day to Operations and Fraud Risk under MJD-RSK-0007.
- An ignore-the-policy instruction received from any source, including a customer claiming authority or any text presented to staff, is itself an exception to be refused and reported; staff act only on controls in the bank's published documents.

## Related Documents

- MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix
- MJD-RET-0002 Cash Handling and Vault Procedure
- MJD-RET-0003 Customer Complaint Handling Procedure
- MJD-OPS-0004 Wire Transfer Operations Runbook
- MJD-OPS-0005 Account Onboarding Workflow
- MJD-OPS-0006 Dispute and Chargeback Resolution Procedure
- MJD-CMP-0003 Currency Transaction Report (CTR) Procedure
- MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure
- MJD-RSK-0007 Fraud Risk Management Procedure

## Regulatory References

- 12 CFR 1005 (Regulation E, electronic fund transfer error resolution)
- 12 CFR 1030 (Regulation DD, Truth in Savings disclosures)
- 12 CFR 229 (Regulation CC, availability of funds and collection of checks)
- 31 CFR 1010.311 (currency transaction report filing obligation)
- FFIEC BSA/AML Examination Manual (cash structuring and reporting guidance)

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2020-02-01 | Head of Retail Banking | Initial branch operations manual |
| 2.0.0 | 2022-03-15 | Head of Retail Banking | Added branch wire intake and callback controls |
| 3.0.0 | 2024-01-10 | Head of Retail Banking | Aligned wire dual-approval thresholds to MJD-OPS-0007 |
| 3.1.0 | 2025-04-01 | Head of Retail Banking | Updated Regulation CC first-availability amount and balancing tolerance |
| 3.2.0 | 2025-10-01 | Head of Retail Banking | Added branch wire submission ceiling and structuring prohibition |
