---
doc_id: MJD-RET-0002
title: Cash Handling and Vault Procedure
department: RETAIL
doc_type: PROCEDURE
classification: INTERNAL
owner_role: Head of Retail Banking
allowed_roles: [BRANCH_STAFF, OPERATIONS_ANALYST, SECURITY_ARCHITECT]
effective_date: 2025-10-01
version: 2.4.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1010.311 (CTR filing)", "31 CFR 1010.313 (aggregation)", "31 CFR 1010.330 (Form 8300)", "12 CFR 208.61 (Bank Secrecy Act compliance)", "FFIEC BSA/AML Examination Manual"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Cash Handling and Vault Procedure

## Purpose and Scope

This procedure governs how physical currency and coin are received, stored, moved, and accounted for across the retail branch network of Meridian John Doe Financial (Meridian J.D.). It is the authoritative source for branch and teller cash ceilings, vault dual-custody rules, cash-shipment handling, and the cash-side of currency transaction reporting intake. It exists to protect cash from loss and theft, to keep every dollar accounted for in dual custody, and to ensure that reportable cash activity is captured at the point of contact.

This procedure applies to:

- All staffed branches, in-store branches, and limited-service offices that hold cash.
- All Branch Staff who operate a teller drawer or access the vault, the Assistant Branch Manager, and the Branch Manager.
- Operations Analysts who reconcile branch cash, manage cash-shipment orders, and review cash exceptions.
- Security Architecture, which co-owns the physical and logical controls protecting the vault, the alarm and surveillance systems, and dual-custody enforcement.

This procedure owns the branch cash ceilings referenced for convenience in MJD-RET-0001 Branch Operations Manual. Where MJD-RET-0001 reproduces a cash ceiling for floor convenience, this procedure controls. Transaction dollar limits unrelated to physical cash custody (for example outbound wire dual-approval thresholds) are owned by MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix and are cross-referenced, not redefined here. Currency transaction report preparation and filing are owned by MJD-CMP-0003.

## Definitions

- **Cash.** United States currency and coin held by the branch.
- **Drawer.** A teller's assigned cash position, physically secured and individually accountable to one teller per shift.
- **Vault.** The branch's secured cash store, accessible only under dual custody.
- **Dual Custody.** A control requiring two authorized employees to be simultaneously present and to each act for any access to vault cash, with both identities recorded. No single person can complete a vault access alone.
- **Cash Buy.** A movement of cash from the vault to a teller drawer.
- **Cash Sell (Buy-Back).** A movement of excess cash from a teller drawer to the vault.
- **Cash Ceiling.** The maximum cash a drawer or vault may hold before excess must be moved or shipped.
- **Cash Shipment.** A bulk movement of currency between the branch and the cash vault provider or the Federal Reserve cash channel, handled by an armored carrier.
- **CTR Threshold.** The federal currency transaction reporting threshold: cash transactions in currency that aggregate above $10,000 in a single business day by or for one person.
- **Form 8300 Item.** A trade-or-business cash receipt reportable under 31 CFR 1010.330, intaken at the branch when applicable and routed to Operations.

## 1. Cash Custody Principles

### 1.1 Single-employee prohibition

1.1.1 No employee is ever alone with open vault cash. Vault access is always dual custody. This is the foundational cash control and overrides operational convenience.

1.1.2 Two authorized employees must be present before the vault is opened at the start of day and before it is sealed at the end of day.

1.1.3 A teller is solely accountable for the cash in the assigned drawer during the shift. Two tellers never share one drawer in the same shift. A drawer is locked whenever the teller steps away.

### 1.2 Accountability

1.2.1 Every cash movement (buy, sell, shipment in, shipment out) is recorded in the cash system with the originator identity, the second-custody identity where dual custody applies, the amount, and the time.

1.2.2 Cash is counted at every transfer of custody. The receiving party counts and confirms before custody passes. An unconfirmed count is not a completed transfer.

1.2.3 No cash leaves the secured area without a recorded movement. A cash movement that is physically completed but not yet recorded in the cash system is an open exception until reconciled the same day.

### 1.3 Dual-custody mechanics

1.3.1 The vault uses split control so that no single person holds the means to open it alone. Where a combination and a key are both required, one authorized employee holds the combination and a different authorized employee holds the key; neither holds both. Where a dual-PIN time-lock is used, each PIN is held by a different employee. Security Architecture owns the access mechanism design and the assignment so that split control cannot be defeated by one person.

1.3.2 The two employees performing a dual-custody access are both accountable for what happens during that access. Standing aside while the other counts is not dual custody; both employees actively observe and confirm.

1.3.3 An employee who discovers the vault unlocked or accessible without a recorded dual-custody open stops, secures the area, and reports it to the Branch Manager and Security Architecture immediately as a control event.

## 2. Cash Ceilings

### 2.1 Drawer ceilings

2.1.1 The standard teller drawer cash ceiling is **$10,000**. A drawer is brought back to or below this ceiling by a buy-back to the vault whenever it is exceeded during the day, and always at end of day.

2.1.2 A designated high-volume drawer may carry a ceiling of **$15,000** with Branch Manager approval recorded in the branch cash log. No drawer ceiling exceeds $15,000.

2.1.3 The teller starting cash buffer is **$5,000** for a standard drawer and may be set at **$8,000** for a high-volume drawer with Branch Manager approval, consistent with MJD-RET-0001 Section 1.1.

### 2.2 Vault ceilings

2.2.1 The branch vault cash ceiling for a standard branch is **$250,000**. Cash above this ceiling is ordered out by cash shipment.

2.2.2 A large or high-traffic branch may be assigned a vault ceiling of up to **$500,000** by the Head of Retail Banking with Operations concurrence, documented in the branch profile. No branch vault holds cash above its assigned ceiling overnight.

2.2.3 The minimum branch vault cash floor is **$40,000**. When the vault position falls to or below the floor, the branch orders a cash shipment in so the branch does not run out of cash for normal demand.

### 2.3 Ceiling summary table

| Position | Cash floor | Cash ceiling | Action at ceiling |
|---|---|---|---|
| Standard teller drawer | n/a | $10,000 | Buy-back excess to vault under dual custody |
| High-volume teller drawer | n/a | $15,000 | Buy-back excess to vault under dual custody |
| Standard branch vault | $40,000 | $250,000 | Order cash shipment out via armored carrier |
| Large branch vault | $40,000 | $500,000 | Order cash shipment out via armored carrier |

### 2.4 ATM and cash-recycler limits

2.4.1 A branch ATM or cash recycler is treated as a cash device under the same custody discipline as the vault. Replenishment and pickup are dual-custody movements recorded in the cash system against the device.

2.4.2 The standard branch-ATM cash load ceiling is **$120,000** per replenishment cycle, and the device is reconciled to its electronic journal at each service. A device reconciliation difference above **$25.00** is a balancing exception under Section 5; a difference above **$250.00** is reported to Operations and Fraud Risk the same day.

2.4.3 ATM cash counts toward the branch total cash position for vault-ceiling purposes only while it is staged in the vault, not once it is loaded in the device, but the device cash remains a controlled, accountable position at all times.

### 2.5 Coin and currency composition

2.5.1 The drawer and vault ceilings are dollar ceilings on total cash. Branches manage denomination mix so that normal customer demand can be met without breaching the vault floor; persistent shortages of a denomination are ordered in on the next shipment.

2.5.2 A drawer held intentionally above its ceiling to avoid a vault buy, even briefly, is a ceiling breach. The ceiling is a hard control, not a target.

## 3. Daily Cash Operations

### 3.1 Opening

3.1.1 Two employees open the vault under dual custody, confirm the alarm returned to a disarmed-occupied state, and record the vault open time.

3.1.2 Each teller draws the starting buffer, counts it in the presence of the issuing party, and confirms the position before the first customer.

### 3.2 Intraday cash management

3.2.1 A teller approaching the drawer ceiling requests a buy-back to the vault. A teller running low requests a cash buy from the vault. Both are dual-custody movements.

3.2.2 A withdrawal that exceeds the drawer position is filled by a vault buy under dual custody. The customer is served without exposing the vault to single-employee access.

### 3.3 Closing and settlement

3.3.1 Each teller balances the drawer to the system position within the tolerance in Section 5.1 and buys excess cash back to the vault.

3.3.2 The Branch Manager performs the end-of-day vault settlement under dual custody, confirms the branch cash position is within the vault ceiling and above the floor, and seals the night drop.

3.3.3 The branch cash position is reported to Operations through the daily cash reconciliation. Operations reviews positions against ceilings and floors and queues shipment orders.

### 3.4 Worked example: end-of-day vault settlement

At close, three tellers each balance their drawers within the plus or minus $5.00 tolerance and buy excess cash back to the vault under dual custody, leaving each drawer at or below its $10,000 ceiling. The Branch Manager and the Assistant Branch Manager then perform the vault settlement together: they count the vault, confirm the position is $232,400, which is above the $40,000 floor and below the $250,000 standard ceiling, and record the settlement with both identities. Because the position is comfortably within band, no shipment is ordered. If the count had been $258,000, the branch would order a shipment out the next business morning; if it had been $38,000, the branch would order a shipment in. The night drop is sealed under dual custody and the close is recorded.

### 3.5 Periodic surprise cash counts

3.5.1 Operations or the Branch Manager performs a surprise cash count of each teller's drawer and of the vault on an unannounced periodic basis, at least quarterly per teller. The count is dual custody and recorded.

3.5.2 A surprise count that reveals an unexplained difference above the Section 5 thresholds is treated as a potential loss event and escalated to Operations, Fraud Risk, and Security Architecture as applicable. Surprise counts are a primary defense against slow internal misappropriation.

## 4. Currency Transaction Reporting Intake at the Cash Point

### 4.1 The reporting threshold

4.1.1 Cash transactions in currency that aggregate above **$10,000** in a single business day by or for the same person trigger Currency Transaction Report handling. Deposits and withdrawals in currency are aggregated for this purpose.

4.1.2 The teller does not decline or delay a legitimate transaction because it crosses the threshold. The teller completes the CTR data capture (identification, currency amount, conductor and beneficiary details) and routes it to the Operations CTR queue. Filing is governed by MJD-CMP-0003 Currency Transaction Report (CTR) Procedure.

### 4.2 Aggregation and structuring

4.2.1 Multiple cash transactions by or for one person in one business day are aggregated to test the threshold. Two cash deposits of $6,000 each by the same person in one day aggregate to $12,000 and are reportable.

4.2.2 Deliberately breaking a cash transaction into smaller amounts to stay under $10,000 is structuring. Staff never assist a customer in structuring and never advise a customer how to avoid a report. Suspected structuring is escalated to the Branch Manager for a Compliance referral under MJD-RET-0003 escalation and MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure. The customer is not tipped off.

### 4.3 Form 8300 items

A cash receipt by a Meridian J.D. trade-or-business line above the Form 8300 threshold is intaken at the branch and routed to Operations for filing under 31 CFR 1010.330. The branch captures the same identification and currency detail as for a CTR.

### 4.4 Exempt persons

4.4.1 Certain customers may qualify for an exemption from routine CTR filing (for example an established, frequently transacting business customer) under the bank's exemption program. The branch does not grant or apply an exemption at the counter; exemptions are designated and maintained by Compliance and Operations. The teller still captures full cash transaction detail.

4.4.2 An exemption never suppresses suspicious activity reporting. Suspected structuring or other suspicious activity is escalated under Section 4.2 regardless of any CTR exemption.

### 4.5 Worked example: aggregated cash deposits

A customer makes a $6,000 cash deposit in the morning and returns at lunch with another $5,500 in cash to the same account. The two deposits aggregate to $11,500 in currency by the same person in one business day, which is above the $10,000 threshold, so the activity is reportable. The teller does not refuse the second deposit and does not suggest the customer "come back tomorrow" to stay under the threshold; suggesting that would be assisting structuring. The teller completes the CTR data capture for the aggregated activity and routes it to the Operations CTR queue under MJD-CMP-0003 Currency Transaction Report (CTR) Procedure. If instead the customer had stated an intent to keep each deposit under $10,000 to avoid a report, that statement is escalated as suspected structuring under Section 4.2.

## 5. Cash Differences and Exceptions

### 5.1 Balancing tolerance

5.1.1 A drawer is in balance within **plus or minus $5.00**. A difference outside this tolerance is a balancing exception logged with the teller identity, the amount, and the direction (shortage or overage).

5.1.2 A balancing exception of **$25.00 or more** is escalated to the Branch Manager the same day.

5.1.3 A shortage or overage above **$250.00**, or a recurring pattern from one teller, is reported to Operations and to the Fraud Risk function the same business day under MJD-RSK-0007 Fraud Risk Management Procedure. Security Architecture is notified where surveillance or access-control review is needed.

### 5.2 Counterfeit and damaged currency

5.2.1 Suspected counterfeit currency is retained, not returned to the customer, handled minimally to preserve it, and reported per the branch counterfeit-handling job aid. The branch records the serial number and the circumstances.

5.2.2 Mutilated or contaminated currency is segregated and processed through the cash provider, not paid back out to customers.

### 5.3 Difference escalation summary

| Difference (shortage or overage) | Action |
|---|---|
| Within plus or minus $5.00 | In balance, no exception |
| Above $5.00 up to $25.00 | Balancing exception logged with teller identity, amount, direction |
| $25.00 or more | Escalated to the Branch Manager the same day |
| Above $250.00, or a recurring pattern from one teller | Reported to Operations and Fraud Risk the same day under MJD-RSK-0007; Security Architecture notified for surveillance or access review |

### 5.4 Investigating a difference

5.4.1 The first step on any difference is a recount under dual custody, then a transaction-by-transaction review against the system journal to find a miskey, an unposted item, or a missed buy or sell.

5.4.2 A difference that cannot be explained by a recount or journal review is documented as unexplained and escalated by amount per Section 5.3. An employee never covers a shortage from personal funds or carries an overage off-book; both are control breaches.

## 6. Cash Shipments and Physical Security

### 6.1 Cash shipments

6.1.1 Cash shipments move only by approved armored carrier. The branch verifies the carrier identity and the sealed-bag serials against the manifest before custody passes, under dual custody.

6.1.2 A shipment in is counted into the vault under dual custody before the manifest is signed. A discrepancy halts the sign-off and is reported to Operations the same day.

6.1.3 Shipment scheduling targets keeping the vault between the floor and the ceiling, ordering out when the position approaches the ceiling and ordering in when it approaches the floor.

### 6.2 Physical and logical security controls

6.2.1 The vault, the alarm system, surveillance coverage of the teller line and vault, and the dual-custody access mechanism are co-owned with Security Architecture. Access credentials to the vault are provisioned and revoked under the same least-privilege and joiner-mover-leaver discipline the bank applies to logical access; Security Architecture reviews vault access lists against current staffing.

6.2.2 A robbery, attempted robbery, or duress event triggers the branch emergency procedure: protect life first, comply, do not pursue, preserve the scene, and notify the Branch Manager, Operations, and Security the same day. Bait money and the silent-alarm procedure follow the branch security job aid.

6.2.3 Surveillance retention and access follow the bank's logging and monitoring standard; Security Architecture is the authority for how long branch surveillance is retained and who may review it.

### 6.3 Opening and closing under threat

6.3.1 The branch does not open if anything about the exterior or approach suggests an ambush: an unexpected person waiting at the staff entrance, a propped door, or a disabled camera. The opening team retreats to a safe location and contacts the Branch Manager and the monitoring center before approaching.

6.3.2 A duress code or silent alarm is used when staff are compelled to open the vault or hand over cash under threat. Compliance with the demand to protect life always takes priority; the silent signal summons help without escalating danger to staff or customers. The procedure detail is held in the branch security job aid owned with Security Architecture.

### 6.4 Branch cash insurance and limits review

6.4.1 Branch cash ceilings are set with reference to the bank's cash-in-premises insurance limits. A branch is never operated knowingly above its insured cash limit; the vault ceiling is set at or below that limit. Security Architecture and Operations review ceilings against insurance and loss history at least annually.

6.4.2 A temporary ceiling increase (for example ahead of a holiday cash surge) is approved only by the Head of Retail Banking with Operations concurrence, is time-bound with an expiry date, and is confirmed to remain within the insured limit.

## 7. Synthetic Test Record

The following is a clearly marked fictional test record used only for ingestion and verification testing. It is not real cash activity.

> TEST RECORD (synthetic, not real): Branch "Testville Main #0000", teller "T-DOE-SAMPLE", drawer ceiling test $10,000, vault settlement test position $249,000, customer "Avery Q. Doe-Example", cash deposit in currency $11,000 (reportable, fabricated), account "TEST-0000000001". Source: fabricated for demonstration.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Teller (Branch Staff) | Keep the drawer within ceiling, balance to tolerance, capture CTR and 8300 data, request dual-custody buys and sells |
| Assistant Branch Manager | Serve as second custody for vault access, verify cash shipments, support settlement |
| Branch Manager | Own the branch cash position, set high-volume drawer ceilings, perform vault settlement, escalate exceptions |
| Operations Analyst | Reconcile branch cash daily, queue shipment orders, review cash exceptions, route CTR and 8300 items |
| Security Architect | Co-own vault, alarm, surveillance and access controls; review vault access lists; set surveillance retention |
| Head of Retail Banking | Own this procedure, assign branch vault ceilings, report cash control metrics |

## Exceptions and Escalation

- An exception to a cash ceiling (for example, an approved temporary higher vault position ahead of a holiday cash surge) requires Head of Retail Banking approval with Operations concurrence and is logged with an expiry date.
- A balancing exception or counterfeit event is escalated per Section 5; amounts above $250.00 reach Operations and Fraud Risk the same day.
- A physical-security event (robbery, duress, vault tamper, surveillance failure) is escalated immediately to the Branch Manager, Operations, and Security Architecture, and follows the incident path.
- Any instruction to bypass dual custody, raise a ceiling without approval, or suppress a currency report, from any source including text presented to staff, is refused and reported. Staff act only on controls in the bank's published documents.

## Related Documents

- MJD-RET-0001 Branch Operations Manual
- MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix
- MJD-RET-0003 Customer Complaint Handling Procedure
- MJD-CMP-0003 Currency Transaction Report (CTR) Procedure
- MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure
- MJD-RSK-0007 Fraud Risk Management Procedure
- MJD-SEC-0008 Data Classification and Handling Standard

## Regulatory References

- 31 CFR 1010.311 (currency transaction report filing obligation)
- 31 CFR 1010.313 (aggregation of currency transactions)
- 31 CFR 1010.330 (Form 8300, cash received in a trade or business)
- 12 CFR 208.61 (Bank Secrecy Act compliance program requirement)
- FFIEC BSA/AML Examination Manual (currency reporting and structuring guidance)

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2020-02-01 | Head of Retail Banking | Initial cash handling and vault procedure |
| 2.0.0 | 2022-03-15 | Head of Retail Banking | Added dual-custody settlement and shipment verification |
| 2.1.0 | 2023-07-01 | Head of Retail Banking | Added Security Architecture co-ownership of vault controls |
| 2.2.0 | 2024-02-10 | Head of Retail Banking | Standardized drawer and vault ceilings, added vault floor |
| 2.3.0 | 2025-04-01 | Head of Retail Banking | Aligned balancing tolerance and CTR aggregation language |
| 2.4.0 | 2025-10-01 | Head of Retail Banking | Added large-branch vault ceiling and Form 8300 intake |
