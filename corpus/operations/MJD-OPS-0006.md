---
doc_id: MJD-OPS-0006
title: Dispute and Chargeback Resolution Procedure
department: OPERATIONS
doc_type: PROCEDURE
classification: INTERNAL
owner_role: Head of Card and Payments Operations
allowed_roles: [OPERATIONS_ANALYST, BRANCH_STAFF, COMPLIANCE_OFFICER]
effective_date: 2025-07-10
version: 2.6.0
review_cycle_months: 12
regulatory_refs: ["Regulation E (12 CFR 1005)", "Regulation Z (12 CFR 1026)", "Electronic Fund Transfer Act", "Fair Credit Billing Act"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Dispute and Chargeback Resolution Procedure

## Purpose and Scope

This procedure defines how Meridian John Doe Financial (Meridian J.D.) intakes, investigates, and resolves customer disputes for debit-card, ACH, and credit-card transactions, including the chargeback lifecycle with card networks. It implements the consumer-protection timelines of Regulation E for electronic fund transfers and Regulation Z for credit transactions.

This procedure applies to Operations Analysts who investigate disputes, Branch Staff who intake them, and Compliance Officers who oversee regulatory-timeline adherence. It covers provisional credit, investigation, network chargeback representment, and final resolution.

## Definitions

- **Dispute.** A customer assertion that a transaction is unauthorized, erroneous, or not as described.
- **Chargeback.** The reversal of a card transaction initiated by the issuing bank through the card network.
- **Representment.** The merchant or acquirer response contesting a chargeback.
- **Provisional Credit.** A temporary credit issued to the customer during investigation.
- **Error.** Under Regulation E, an unauthorized electronic fund transfer, an incorrect amount, a computational error, or an omission from a statement, among others.
- **Notice of Error.** A customer communication asserting an error that starts the regulatory clock.

## 1. Intake

### 1.1 Channels and capture

1.1.1 Disputes are accepted by branch, contact center, secure message, and digital banking.

1.1.2 Capture: account, transaction date and amount, merchant or counterparty, dispute reason code, and the date the customer first noticed the error.

### 1.2 Regulation E clock

1.2.1 An oral or written notice of error starts the Regulation E timeline. The customer must report within 60 days of the statement on which the error first appeared to preserve full protections.

1.2.2 Record the notice date precisely; it anchors all downstream deadlines. The notice date is the calendar date on which Meridian J.D. first received the assertion through any channel, not the date a case is keyed into the dispute system. Where intake occurs after hours, the notice date is the business day of receipt for oral notice taken by a representative and the timestamp of submission for digital channels.

1.2.3 An oral notice is sufficient to start the clock. Meridian J.D. does not require the customer to submit a signed written affidavit before opening a case or before the provisional-credit obligation attaches. An affidavit may be requested, but a delay or refusal by the customer in returning it does not extend the regulatory deadlines or relieve the bank of the provisional-credit obligation when the conditions in Section 2 are met.

### 1.3 Reason-code capture and triage

1.3.1 At intake, classify each dispute into one of the standard internal triage categories so that the correct timeline and chargeback path are assigned from the outset.

| Internal triage category | Typical examples | Governing rule |
|---|---|---|
| Unauthorized EFT | Lost or stolen debit card use, account takeover debit, unrecognized ACH debit | Regulation E |
| Processing error | Duplicate posting, incorrect amount, wrong account debited, ATM dispense shortage | Regulation E |
| Credit billing error | Unrecognized credit-card charge, computational error, undelivered goods on credit | Regulation Z |
| Cardholder service dispute | Goods not as described, cancelled recurring charge, credit not processed | Network reason code, Regulation Z if credit |

1.3.2 If a single case spans more than one category (for example, a debit-card charge that is both unauthorized and duplicated), apply the most protective timeline to the case and document each underlying assertion separately in the case file.

1.3.3 A first-party fraud indicator (the customer is suspected of having authorized or benefited from the transaction) is flagged at intake but does not change the intake handling. Suspicion alone is recorded for later review under Section 8 and does not justify refusing intake or withholding the regulatory clock.

## 2. Provisional Credit (Regulation E)

### 2.1 When provisional credit applies

2.1.1 For a Regulation E error, if the investigation will exceed 10 business days, the bank issues provisional credit for the disputed amount (including applicable fees) within 10 business days of the notice of error.

2.1.2 For new accounts (open less than 30 days), point-of-sale, and foreign-initiated transactions, the provisional-credit and investigation windows extend per Regulation E (up to 20 business days for provisional credit).

### 2.2 Provisional-credit decision logic

2.2.1 The analyst applies the following decision sequence on every Regulation E dispute. The questions are answered in order, and the first matching outcome governs.

| Step | Question | If yes | If no |
|---|---|---|---|
| 1 | Is the assertion a Regulation E error (unauthorized EFT, wrong amount, or processing error)? | Continue to step 2 | Route to the applicable rule; no Regulation E provisional credit |
| 2 | Can the investigation be completed within 10 business days of the notice? | No provisional credit required; resolve and notify | Continue to step 3 |
| 3 | Does the account or transaction fall in an extended category (new account, POS, or foreign)? | Provisional credit within up to 20 business days of notice | Provisional credit within 10 business days of notice |
| 4 | Has a documented provisional-credit exception been approved under Section 8? | Withhold and document; obligation is not waived by suspicion alone | Issue provisional credit per step 3 |

2.2.2 Provisional credit covers the full disputed principal plus any fees and, where applicable, interest the customer was charged as a direct result of the disputed transaction. The credit is posted with a transaction descriptor that identifies it as provisional so it can be cleanly reversed or made permanent at resolution.

2.2.3 Where the customer has provided only oral notice and has not returned a requested written confirmation within 10 business days, provisional credit is still issued on time. The bank may, where the customer fails to provide written confirmation within 10 business days of an oral notice, decline to issue provisional credit only if it has provided the written-confirmation request and the customer did not comply; absent that documented request, provisional credit is issued.

### 2.3 Notice to customer

2.3.1 The customer is notified of provisional credit within two business days of issuance. The notice states the amount credited, that the credit is provisional pending investigation, and that it may be reversed if the investigation finds no error, subject to the advance-notice protection in Section 5.

2.3.2 The control owner for provisional-credit timeliness is the Operations Analyst assigned to the case, with second-line monitoring by the Compliance Officer through the monthly timeline report in Section 7. The target service level is provisional credit posted no later than the close of business on the applicable deadline day in 100 percent of qualifying cases.

## 3. Investigation Timelines

### 3.1 Standard timelines

| Scenario | Investigation deadline |
|---|---|
| Standard Regulation E error | 45 calendar days from notice |
| Extended (new account, POS, foreign) | 90 calendar days from notice |
| Regulation Z billing error | 2 complete billing cycles, not exceeding 90 days |

### 3.2 Investigation steps

3.2.1 Gather evidence: transaction logs, device and location data, prior customer behavior, and merchant documentation.

3.2.2 For card transactions, evaluate whether a network chargeback right exists and the applicable reason code.

3.2.3 Determine whether the transaction was unauthorized, authorized in error, or valid.

### 3.3 Evidence standards by dispute type

3.3.1 The minimum evidence set differs by dispute type. The analyst documents which items were obtained and, where an item could not be obtained, the reason.

| Dispute type | Core evidence | Corroborating evidence |
|---|---|---|
| Unauthorized debit card | Authorization log, terminal or device ID, geolocation, EMV or CVM result | Customer location at time of use, prior chargeback history, velocity data |
| ATM dispense shortage | Dispense log, cash-balancing record for the terminal, camera reference | Prior over- or under-dispense events on that terminal |
| Duplicate or wrong amount | Posting record showing both entries, merchant settlement file | Customer receipt, merchant confirmation |
| Goods not received or not as described | Customer cancellation evidence, shipping or delivery record | Merchant terms, attempts to resolve with merchant first |

3.3.2 For goods-related disputes, confirm the customer attempted to resolve the matter with the merchant before a chargeback is raised, where the network reason code requires it. Record the date and outcome of that contact.

3.3.3 The investigation file documents the analyst's reasoning, not only the conclusion. A bank-favorable finding must cite the specific evidence relied upon, because that evidence is disclosable to the customer under Section 5.

### 3.4 Timeline decision table

3.4.1 The applicable deadline is derived from the notice date and the dispute attributes as follows.

| Trigger condition | Provisional-credit deadline | Final-resolution deadline |
|---|---|---|
| Standard Regulation E error | Within 10 business days of notice if not resolved by then | 45 calendar days from notice |
| New account (open less than 30 days) | Up to 20 business days of notice | 90 calendar days from notice |
| Point-of-sale transaction | Up to 20 business days of notice | 90 calendar days from notice |
| Foreign-initiated transaction | Up to 20 business days of notice | 90 calendar days from notice |
| Regulation Z credit billing error | Not applicable; no Regulation E provisional credit | 2 complete billing cycles, not exceeding 90 days |

3.4.2 Deadlines are calendar days for resolution and business days for provisional credit. Meridian J.D. observes its published holiday calendar for business-day counting; weekends and federal holidays do not count as business days for the provisional-credit windows.

## 4. Chargeback Lifecycle

### 4.1 Initiating a chargeback

4.1.1 Where a valid chargeback right exists, submit the chargeback to the card network within the network's filing window using the correct reason code and required documentation.

4.1.2 Track the chargeback to the network's response deadline.

### 4.2 Reason-code handling

4.2.1 The analyst selects the network reason code that matches the documented dispute type. An incorrect reason code is the most common cause of an invalid chargeback and a successful representment, so the selection is verified against the evidence on file before filing.

| Dispute condition | Reason-code family | Required documentation |
|---|---|---|
| Fraud, card-present | Fraud or unauthorized use | Cardholder statement, confirmation card was not used by an authorized party |
| Fraud, card-not-present | Fraud or unauthorized use | Cardholder statement, no-authorization confirmation, address mismatch where present |
| Duplicate processing | Processing error | Both posting records, settlement evidence |
| Incorrect amount | Processing error | Receipt or authorized amount versus settled amount |
| Goods or services not received | Cardholder dispute | Expected delivery date, evidence of non-receipt, merchant contact record |
| Not as described or defective | Cardholder dispute | Description of discrepancy, return or cancellation evidence |
| Credit not processed | Cardholder dispute | Cancellation or return confirmation, merchant credit policy |
| Recurring charge after cancellation | Cardholder dispute | Cancellation notice and date provided to merchant |

4.2.2 Filing windows differ by network and reason code. The analyst confirms the applicable window before filing and does not allow the network filing window to lapse while waiting on optional customer documentation; the chargeback is filed on the available evidence and supplemented if needed.

### 4.3 Representment and pre-arbitration

4.3.1 If the merchant represents, review the rebuttal evidence. Accept the representment, or escalate to a second chargeback or pre-arbitration where the evidence supports it.

4.3.2 Arbitration is pursued only with Operations supervisor approval given the network fees at stake.

4.3.3 The representment review follows a fixed sequence: confirm the merchant's evidence actually rebuts the specific reason code used; check whether the original reason code was correct; obtain any further evidence from the customer; and decide whether the case can be won on the merits before incurring further network fees.

| Representment outcome | Action | Approval |
|---|---|---|
| Evidence clearly rebuts the claim | Accept representment; reverse provisional credit per Section 5 | Operations Analyst |
| Evidence does not rebut the claim and a second presentment right exists | File pre-arbitration or second chargeback | Operations Analyst |
| Marginal case with material network fee exposure | Decide whether to proceed to arbitration | Operations supervisor |

4.3.4 The service level for acting on a received representment is five business days from receipt of the network notification, so that any reversal of provisional credit can still meet the advance-notice requirement in Section 5 before the resolution deadline.

## 5. Resolution

### 5.1 Customer-favorable resolution

5.1.1 If the dispute is resolved in the customer's favor, make any provisional credit permanent and notify the customer.

### 5.2 Bank-favorable resolution

5.2.1 If the investigation finds no error, the bank may reverse provisional credit after providing the customer at least five business days' advance notice, along with a written explanation and the right to request the documents relied upon.

5.2.2 Documents relied upon are provided to the customer on request within three business days.

5.2.3 The reversal is not posted before the fifth business day after the advance notice is sent. The analyst schedules the reversal date in the dispute system at the time the notice is generated so that the posting cannot run early. If the customer presents new evidence during the advance-notice period, the reversal is held and the investigation is reopened.

5.2.4 The advance-notice letter states the date the provisional credit will be reversed, the reason the bank found no error, that the customer may request the documents relied upon, and the customer's right to escalate through the complaint process under MJD-RET-0003.

### 5.3 Final notice

5.3.1 In all cases the customer receives written notice of the resolution within three business days of completing the investigation.

### 5.4 Worked example: unauthorized debit-card dispute with provisional credit

5.4.1 A customer calls the contact center on day 0 reporting two debit-card charges totaling 318.40 dollars at an out-of-state merchant she does not recognize. The card is in her possession. Branch-equivalent intake captures the account, the two transactions, the merchant, an unauthorized-EFT reason, and the notice date of day 0. The account is more than 30 days old and the transactions are domestic card-present, so the standard windows apply.

5.4.2 The analyst pulls the authorization log and finds the transactions were card-present with a chip read and a successful PIN, but the terminal geolocation places both in a city 600 miles from the customer's confirmed location at the same time, and a prior card-present transaction posted in her home city 40 minutes earlier. The investigation cannot be completed within 10 business days because merchant documentation is outstanding.

5.4.3 On day 8, within the 10-business-day window, the analyst issues provisional credit of 318.40 dollars plus a 12.00 dollar overdraft fee the disputed charges caused, and sends the provisional-credit notice within two business days. A fraud chargeback is filed under the card-present fraud reason code with the cardholder statement and the geolocation conflict as supporting evidence.

5.4.4 The merchant does not represent within the network window. On day 26, well within the 45-calendar-day deadline, the analyst confirms the customer-favorable outcome, makes the provisional credit permanent, removes the overdraft fee, and sends the final resolution notice within three business days. Because the facts indicate a counterfeit or cloned-card pattern, the case is referred to Fraud Risk under MJD-RSK-0007.

### 5.5 Worked example: Regulation Z billing-error dispute

5.5.1 A credit-card customer submits a secure message asserting a 540.00 dollar charge for a hotel stay that was cancelled within the merchant's free-cancellation window. The charge appeared on the statement dated day 0, and the customer's notice is received on day 12, within 60 days of the statement, so it is a timely Regulation Z billing-error assertion.

5.5.2 Regulation E provisional credit does not apply because this is a credit transaction. The analyst sends the customer the written acknowledgement of the billing-error notice and suspends collection activity and finance charges on the disputed amount while the investigation proceeds. The resolution deadline is two complete billing cycles, not exceeding 90 days.

5.5.3 The analyst confirms the customer holds a dated cancellation confirmation from the merchant and that the merchant's policy allowed free cancellation. A chargeback is filed under the credit-not-processed cardholder-dispute reason code with the cancellation confirmation attached.

5.5.4 The merchant represents with a no-show claim, but the merchant's own confirmation shows the cancellation predated the stay. The analyst proceeds to pre-arbitration. The case resolves in the customer's favor on day 58, within the second billing cycle. The 540.00 dollar charge and any related finance charges are credited, and the customer receives written notice of the resolution within three business days.

## 6. Fraud and SAR Referral

6.1 A dispute exhibiting a fraud pattern (account takeover, card-not-present fraud ring, first-party fraud) is referred to the Fraud Risk function under MJD-RSK-0007.

6.2 Activity suggesting money laundering or that meets SAR criteria is referred to Compliance under MJD-CMP-0002. Operations does not file the SAR; it refers.

6.3 Referral to Fraud Risk does not pause the Regulation E or Regulation Z clock. Provisional credit, investigation, and resolution deadlines continue to run while a parallel fraud or SAR review proceeds. The two workstreams are tracked as linked cases so neither deadline is lost to the other.

6.4 First-party fraud (the customer is the suspected perpetrator) is the only category that interacts with provisional credit, and only through the documented exception in Section 8. Even then, the regulatory obligation is not waived by suspicion; an exception requires the evidence and approval described there.

6.5 Where the same merchant, terminal, or device appears across multiple unrelated customer disputes, the analyst raises a pattern alert to Fraud Risk so the common point of compromise can be investigated independently of the individual cases.

## 7. Recordkeeping and Reporting

7.1 Dispute case files, including evidence, timelines, and customer notices, are retained for five years per MJD-CMP-0008.

7.2 Compliance receives a monthly report of dispute volumes, timeline adherence, and any missed Regulation E deadlines, which are tracked as control issues under MJD-RSK-0003.

7.3 Each case file is structured so that a reviewer can reconstruct the timeline without reference to other systems. The required contents are the notice date, the triage category and reason code, all deadline dates derived in Section 3.4, the provisional-credit decision and posting date, every customer notice with its send date, the evidence relied upon, the resolution and its basis, and any exception approvals.

7.4 The monthly control report tracks the following metrics, each with an owner and a target.

| Control metric | Owner | Target |
|---|---|---|
| Provisional credit issued by the applicable deadline | Operations Analyst | 100 percent of qualifying cases |
| Standard Regulation E cases resolved within 45 calendar days | Operations Analyst | At least 99 percent |
| Extended cases resolved within 90 calendar days | Operations Analyst | At least 99 percent |
| Regulation Z billing errors resolved within two cycles, not exceeding 90 days | Operations Analyst | At least 99 percent |
| Advance notice of at least five business days before any provisional-credit reversal | Operations Analyst | 100 percent |
| Final resolution notice sent within three business days | Operations Analyst | 100 percent |

7.5 Any breach of a target is logged as a control issue under MJD-RSK-0003 with a root-cause note and a corrective action. Repeated breaches of the same control are escalated to the Head of Card and Payments Operations.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Branch Staff | Intake disputes, capture the notice date and reason, deliver customer notices |
| Operations Analyst | Investigate, issue provisional credit on time, manage chargebacks and representments, resolve and notify |
| Compliance Officer | Oversee Regulation E and Z timeline adherence, receive fraud and SAR referrals, review missed-deadline reporting |
| Head of Card and Payments Operations | Own this procedure, approve arbitration, report dispute metrics |

## Exceptions and Escalation

- A provisional-credit exception (for example, suspected first-party fraud) requires Operations supervisor approval and documented justification; the Regulation E obligation is not waived by suspicion alone. The justification records the specific facts supporting the suspicion, not a general concern, and the case remains subject to the standard resolution deadlines.
- A missed regulatory deadline is escalated immediately to Compliance and logged as a control issue under MJD-RSK-0003. The escalation includes the deadline that was missed, the cause, the remediation taken for the affected customer, and the preventive action.
- High-value or pattern fraud is escalated to Fraud Risk and, where applicable, Compliance for SAR evaluation.
- A dispute that also constitutes a complaint, or that the customer escalates after a bank-favorable resolution, is handled jointly with the complaint process under MJD-RET-0003 without restarting the dispute clock.

### Escalation matrix

| Trigger | Escalate to | Timing |
|---|---|---|
| Provisional-credit exception request | Operations supervisor | Before the provisional-credit deadline |
| Arbitration decision with material fee exposure | Operations supervisor | Before the network arbitration filing window closes |
| Approaching regulatory deadline at risk of breach | Compliance Officer | At least three business days before the deadline |
| Missed regulatory deadline | Compliance Officer | Immediately on discovery |
| Suspected fraud pattern or high-value loss | Fraud Risk, then Compliance for SAR review | Same business day |
| Repeated control-metric breach | Head of Card and Payments Operations | At month-end reporting or sooner |

## Related Documents

- MJD-OPS-0004 Wire Transfer Operations Runbook
- MJD-RSK-0007 Fraud Risk Management Procedure
- MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure
- MJD-CMP-0006 Regulation E Error Resolution Procedure
- MJD-RET-0003 Customer Complaint Handling Procedure
- MJD-CMP-0008 Records Retention Schedule

## Regulatory References

- Regulation E, 12 CFR 1005 (electronic fund transfers)
- Regulation Z, 12 CFR 1026 (credit billing errors)
- Electronic Fund Transfer Act
- Fair Credit Billing Act

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2019-05-01 | Head of Card and Payments Operations | Initial dispute procedure |
| 2.0.0 | 2021-08-20 | Head of Card and Payments Operations | Added chargeback representment and pre-arbitration |
| 2.3.0 | 2023-07-15 | Head of Card and Payments Operations | Codified Regulation E provisional-credit timelines |
| 2.5.0 | 2024-10-01 | Head of Card and Payments Operations | Added extended-window scenarios table |
| 2.6.0 | 2025-07-10 | Head of Card and Payments Operations | Clarified bank-favorable reversal notice requirements |
