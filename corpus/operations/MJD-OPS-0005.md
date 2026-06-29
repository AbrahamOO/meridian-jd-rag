---
doc_id: MJD-OPS-0005
title: Account Onboarding Workflow
department: OPERATIONS
doc_type: PROCEDURE
classification: INTERNAL
owner_role: Head of Deposit Operations
allowed_roles: [OPERATIONS_ANALYST, BRANCH_STAFF]
effective_date: 2025-08-20
version: 3.3.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1020.220", "FinCEN CDD Rule 31 CFR 1010.230", "Regulation CC (12 CFR 229)", "Expedited Funds Availability Act"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Account Onboarding Workflow

## Purpose and Scope

This procedure defines the end-to-end workflow for onboarding a new customer account at Meridian John Doe Financial (Meridian J.D.), from application intake through account activation and welcome. It sequences the identity, due-diligence, screening, and funding steps that other procedures define in detail, and assigns ownership and service-level targets to each stage.

This procedure applies to all account-opening channels (branch, digital, contact center, and business banking) and to Operations Analysts and Branch Staff who process onboarding. It is the orchestration layer; the substantive controls live in MJD-OPS-0001 (CIP), MJD-OPS-0002 (CDD), and MJD-OPS-0008 (sanctions screening).

## Definitions

- **Application.** A submitted request to open an account, complete with applicant-provided information.
- **Onboarding Case.** The work item tracking an application through the workflow stages.
- **Activation.** The point at which an account is fully open, verified, funded, and available for transactions.
- **Funding Hold.** A temporary restriction on availability of deposited funds under the bank's funds-availability policy.
- **Stage Gate.** A control checkpoint that must pass before the case advances.
- **Conditional Open.** An account opened before identity verification fully completes, restricted in function and bounded by a five-business-day verification deadline under MJD-OPS-0001.
- **Control Owner.** The named role accountable for the outcome of a specific gate or control, distinct from the analyst who executes the work.
- **Case Age.** Elapsed business days from intake to the current stage, measured against the cumulative service-level target.
- **Routing Reason.** A structured code recorded whenever a case is moved off the straight-through path, used for aging analysis and audit.
- **Funds-Availability Schedule.** The bank's published timetable, aligned to Regulation CC, governing when deposited funds become available for withdrawal.

## Workflow Principles

This procedure operates on four standing principles that govern every onboarding case.

- **Sequenced gates.** Identity precedes screening, screening precedes due diligence, and due diligence precedes setup and funding. No gate is skipped, and no gate is run out of order, because each later control depends on the output of the earlier one.
- **Single case of record.** Each application produces exactly one onboarding case. All actions, decisions, holds, and approvals attach to that case so that the audit trail is complete and reconstructable.
- **Default deny on activation.** An account does not activate until every required gate has passed and opening funds are received. Activation is an affirmative event, never a default that occurs through inaction.
- **Documented exceptions only.** Any deviation from the straight-through path carries a routing reason, a named approver, and a timestamp. Undocumented exceptions are treated as control failures.

## 1. Workflow Stages

### 1.1 Stage overview

| Stage | Owner | Service-level target |
|---|---|---|
| 1. Intake | Branch Staff or system | Same business day |
| 2. Identity (CIP) | Operations Analyst | 1 business day |
| 3. Screening | System and Operations Analyst | Same business day |
| 4. Due diligence (CDD) | Operations Analyst | 2 business days |
| 5. Account setup | Operations Analyst | 1 business day |
| 6. Funding | Branch Staff or system | At customer instruction |
| 7. Activation and welcome | System | Within 1 business day of funding |

The targets in the table are per-stage. The cumulative straight-through target from intake to activation, excluding any time the case waits on the customer for funds or documents, is five business days. Time spent in a customer-pending state stops the internal service-level clock and is tracked separately as wait time.

### 1.2 Stage gates

Each stage is a gate. A case may not advance until the prior stage passes. A failed gate routes the case to the appropriate queue with a documented reason.

### 1.3 Stage-gate decision table

The following table states, for each gate, the pass condition, the fail outcome, the routing reason recorded on fail, and the control owner accountable for the gate.

| Gate | Pass condition | Fail outcome | Routing reason | Control owner |
|---|---|---|---|---|
| 1. Intake | Application complete and product eligible | Return to applicant | INTAKE_INCOMPLETE | Branch Staff |
| 2. Identity | Full or conditional CIP match recorded | Conditional open or decline | CIP_PARTIAL or CIP_NOMATCH | Operations Analyst |
| 3. Screening | No unresolved sanctions or watchlist match | Hold for Compliance | SCREEN_POTENTIAL_MATCH | Compliance Officer |
| 4. Due diligence | Risk rating set; EDD complete if High | Hold for EDD approval | CDD_HIGH_RISK_EDD | Operations Analyst |
| 5. Account setup | Record created; limits configured | Return to analyst queue | SETUP_INCOMPLETE | Operations Analyst |
| 6. Funding | Opening funds received | Await funding | FUNDING_PENDING | Branch Staff or system |
| 7. Activation | All gates passed; funds posted | Remain conditional or restricted | ACTIVATION_BLOCKED | System |

### 1.4 Channel variations

The seven stages apply to every channel, but execution differs by channel.

1.4.1 Branch. CIP is performed in person with documentary verification of presented identification. Funding is typically same-session by cash, check, or internal transfer.

1.4.2 Digital self-service. The applicant completes intake online and CIP runs through non-documentary verification with step-up to documentary if the non-documentary result is partial. Funding is by external ACH pull or inbound transfer.

1.4.3 Contact center. An agent captures intake on the customer's behalf and triggers the same downstream gates as the digital channel, with verbal disclosure delivery confirmed and logged.

1.4.4 Business banking. Entity onboarding always runs the beneficial-ownership and entity-verification steps in Stage 4 and is never eligible for straight-through digital activation.

## 2. Stage 1: Intake

### 2.1 Application capture

2.1.1 Capture applicant data, product selection, and intended use. For entities, capture entity formation details and the individual opening on the entity's behalf.

2.1.2 Validate completeness; an incomplete application is returned to the applicant with the missing items itemized.

2.1.3 Validate product eligibility against the applicant's stated residency, age, and tax-reporting status. An applicant who is not eligible for the selected product is offered an eligible alternative rather than declined outright, and the substitution is logged on the case.

2.1.4 Record the intended use of the account and the expected funding source. This data feeds the nature-and-purpose documentation collected in Stage 4 and the initial limit configuration in Stage 5.

### 2.2 Duplicate and existing-customer check

Check whether the applicant is an existing customer. An existing customer with a current verified identity record may skip re-verification under MJD-OPS-0001 Section 1.

2.2.1 Match candidates are surfaced on name, date of birth, tax identification number, and address. A confirmed match links the new application to the existing customer profile.

2.2.2 If an existing customer's identity record is stale or the underlying documentation has expired, treat the application as requiring full CIP at Stage 2 rather than relying on the prior record.

2.2.3 A near-match that cannot be confirmed as the same person is treated as a new customer, and full CIP applies. Never merge profiles on an unconfirmed match.

### 2.3 Intake completeness checklist

The following items must be present before a case advances past Stage 1. A missing item holds the case at the intake gate with routing reason INTAKE_INCOMPLETE.

| Item | Consumer | Entity |
|---|---|---|
| Legal name | Required | Required (legal entity name) |
| Date of birth or formation date | Required | Required |
| Residential or principal business address | Required | Required |
| Tax identification number | Required | Required (EIN) |
| Government identification reference | Required | Required for the individual opening |
| Product selection and intended use | Required | Required |
| Beneficial owner roster | Not applicable | Required (collected in Stage 4) |

## 3. Stage 2: Identity (CIP)

3.1 Execute the Customer Identification Program per MJD-OPS-0001: collect the four elements and perform documentary or non-documentary verification.

3.2 A partial or no-match result follows the adjudication and conditional-opening rules in MJD-OPS-0001 Section 4. The onboarding case reflects conditional-open status and the five-business-day verification deadline.

### 3.3 Identity outcome routing

The Stage 2 result drives the next action as follows.

| CIP result | Account status | Next action | Deadline |
|---|---|---|---|
| Full match | Verified | Advance to Stage 3 | None |
| Partial match | Conditional open | Resolve discrepancies; advance with restriction | Five business days |
| No match | Decline or conditional open per adjudication | Branch to manual review | Five business days if conditionally opened |
| Document fraud indicator | Hold | Refer to fraud per MJD-OPS-0001 | Immediate hold |

### 3.4 Conditional-open restrictions

While a case is conditional open, the following restrictions apply and are released only on full verification.

3.4.1 Outbound wires and external ACH originations are blocked.

3.4.2 Deposit posting is permitted, but availability follows the standard and new-account hold schedule with no early release.

3.4.3 If verification is not completed by the five-business-day deadline, the account is restricted and closed per MJD-OPS-0001 Section 4.3, and any funded balance is returned to the source of funds.

## 4. Stage 3: Screening

4.1 The system invokes sanctions and watchlist screening per MJD-OPS-0008. A potential match holds the case at this gate until Compliance clears or confirms the match.

4.2 No account may advance past Stage 3 with an unresolved potential sanctions match.

### 4.3 Screening scope at onboarding

4.3.1 Screen the applicant, and for entities screen the legal entity, each beneficial owner identified at Stage 4, and any authorized signer added at setup.

4.3.2 Screening covers sanctions lists, internal watchlists, and politically exposed person references. A politically exposed person hit does not block the case at Stage 3 but is carried forward as an input to the Stage 4 risk rating and may trigger Enhanced Due Diligence.

4.3.3 A potential match holds the case with routing reason SCREEN_POTENTIAL_MATCH and notifies Compliance. The control owner for clearance is the Compliance Officer, not the onboarding analyst, preserving separation of duties.

4.3.4 Record the disposition of every potential match (cleared as false positive, or confirmed) on the case before the gate releases. A confirmed sanctions match results in decline and the reporting steps defined in MJD-OPS-0008.

## 5. Stage 4: Due Diligence (CDD)

5.1 Apply the Customer Due Diligence Standard (MJD-OPS-0002): compute the Customer Risk Rating, document nature and purpose, and collect and verify beneficial ownership for entities.

5.2 A High risk rating routes the case into Enhanced Due Diligence (MJD-OPS-0003) before activation; activation is blocked until EDD onboarding approval is recorded.

### 5.3 Risk-rating routing

The Customer Risk Rating computed under MJD-OPS-0002 determines the onboarding path from Stage 4 forward.

| Risk rating | EDD required | Setup limits | Activation approver |
|---|---|---|---|
| Low | No | Standard per MJD-OPS-0007 | System auto-approve |
| Medium | No | Standard, with periodic review flag | Operations Analyst |
| High | Yes | Reduced initial limits pending review | EDD approver per MJD-OPS-0003 |

### 5.4 Beneficial ownership for entities

5.4.1 For entity applications, collect and verify each beneficial owner who owns 25 percent or more and the single control person, per the FinCEN Customer Due Diligence Rule and MJD-OPS-0002.

5.4.2 Each beneficial owner is screened at Stage 3 scope and contributes to the entity risk rating. An entity with a beneficial owner that cannot be verified does not advance to setup.

### 5.5 High-risk hold management

A case routed into EDD is held with routing reason CDD_HIGH_RISK_EDD. The hold is released only when the EDD onboarding approval is recorded by the designated EDD approver. The onboarding analyst may not self-approve a High-risk activation under any circumstance.

## 6. Stage 5: Account Setup

6.1 Create the account record, assign product features and fee schedule, establish online-banking enrollment, and link any authorized signers.

6.2 Configure transaction limits in line with MJD-OPS-0007 based on product and risk rating.

### 6.3 Setup sequence

The setup steps run in the following order so that no payment capability exists before controls are in place.

6.3.1 Create the account record with product code, fee schedule, and statement preferences.

6.3.2 Apply the risk-based transaction limits from MJD-OPS-0007. High-risk accounts receive reduced initial limits that are revisited at the first periodic review.

6.3.3 Enroll the customer in digital banking and provision credentials, withholding payment-origination entitlements until activation.

6.3.4 Link authorized signers for entities, screening each new signer at Stage 3 scope before the link is finalized.

6.3.5 Record dual-approval requirements for the account where MJD-OPS-0007 mandates them, so that the controls are live from the first transaction.

### 6.4 Setup verification

Before the case leaves Stage 5, the analyst confirms that the product, fee schedule, limits, and signer roster on the live account record match the approved case data. A mismatch returns the case with routing reason SETUP_INCOMPLETE.

## 7. Stage 6: Funding and Availability

### 7.1 Funding methods

Accept opening funds by branch deposit, internal transfer, external ACH pull, or inbound wire (processed under MJD-OPS-0004).

### 7.2 Funds availability

7.2.1 Apply the bank's funds-availability schedule under Regulation CC. The first 225 USD of a non-next-day check deposit is available the next business day; the remainder follows the standard hold schedule.

7.2.2 New-account holds: for the first 30 days of a new relationship, extended holds may apply to check deposits per the new-account provisions.

### 7.3 Funds-availability detail

7.3.1 Next-day items, including cash, electronic payments such as ACH credits and wires, and certain check types defined in Regulation CC, are available on the first business day after the banking day of deposit.

7.3.2 For a non-next-day check deposit, the first 225 USD is made available on the next business day, and the remainder follows the standard hold schedule. This 225 USD threshold is the Regulation CC minimum the bank applies uniformly.

7.3.3 During the first 30 days of a new account relationship, the new-account exception permits extended holds on check deposits beyond the standard schedule. The next-day availability of cash and electronic credits is not affected by the new-account status.

7.3.4 The following table summarizes availability by item type for a deposit made on a business day before the cutoff.

| Item type | Standard availability | New-account (first 30 days) |
|---|---|---|
| Cash | Next business day | Next business day |
| ACH credit or wire | Next business day | Next business day |
| Check, first 225 USD | Next business day | Next business day |
| Check, remainder | Standard hold schedule | Extended hold may apply |

7.3.5 A deposit made after the daily cutoff or on a non-business day is treated as received on the next business day for availability calculation. Exception holds beyond the schedule, such as large-deposit or redeposited-item holds, require a hold notice to the customer stating the reason and the availability date.

## 8. Stage 7: Activation and Welcome

8.1 On completion of all gates and receipt of opening funds, the system activates the account and removes the conditional-open restriction.

8.2 The customer receives a welcome package with account details, disclosures, and digital-banking access. Required disclosures are delivered and acknowledgment is logged.

### 8.3 Activation preconditions

The system verifies all of the following before it activates an account. If any is unmet, activation is blocked with routing reason ACTIVATION_BLOCKED and the case returns to the responsible queue.

8.3.1 Identity is fully verified, or the conditional-open deadline has not lapsed and the restriction set in Section 3.4 remains in force.

8.3.2 No unresolved sanctions or watchlist match exists.

8.3.3 For a High risk rating, the EDD onboarding approval is recorded.

8.3.4 Account setup is complete with limits and dual-approval controls configured.

8.3.5 Opening funds are posted.

### 8.4 Welcome and disclosure delivery

8.4.1 Deliver the deposit account agreement, fee schedule, funds-availability policy, privacy notice, and electronic-communications consent. Delivery channel matches the opening channel, with branch openings receiving printed or emailed copies and digital openings receiving electronic copies.

8.4.2 Log the disclosure delivery timestamp and the customer acknowledgment on the case. An unacknowledged required disclosure keeps the welcome step open even after the account is otherwise active.

## 9. Worked Examples

### 9.1 Consumer digital onboarding, straight-through

9.1.1 Day 1, Stage 1. An applicant submits a checking-account application through the digital channel with name, date of birth, address, and tax identification number. The intake checklist passes and no existing-customer match is found.

9.1.2 Day 1, Stage 2. Non-documentary CIP returns a full match. The account status is set to Verified with no conditional restriction.

9.1.3 Day 1, Stage 3. Sanctions and watchlist screening returns no potential match. The screening gate releases the same day.

9.1.4 Day 2, Stage 4. The Customer Risk Rating computes to Low. No EDD is required and standard limits apply.

9.1.5 Day 2, Stage 5. The account record is created, standard limits from MJD-OPS-0007 are applied, and digital-banking enrollment completes.

9.1.6 Day 2, Stage 6. The customer funds the account with a 1,000 USD external ACH pull. The ACH credit is available the next business day.

9.1.7 Day 3, Stage 7. With all gates passed and funds posted, the system activates the account and delivers the welcome package electronically. Cumulative internal service-level time is within the five-business-day target.

### 9.2 Business entity onboarding routed into EDD

9.2.1 Day 1, Stage 1. An individual applies on behalf of a limited liability company for a business checking account, supplying the entity legal name, EIN, principal business address, and formation details. Intake completeness passes, including capture of the individual opening on the entity's behalf.

9.2.2 Day 1, Stage 2. CIP on the individual returns a full match.

9.2.3 Day 2, Stage 4 beneficial ownership. Two beneficial owners holding 30 percent and 45 percent and a control person are identified and verified.

9.2.4 Day 2, Stage 3 screening. One beneficial owner returns a politically exposed person reference. This does not block Stage 3 but is carried into the risk rating.

9.2.5 Day 3, Stage 4 risk rating. The combination of the politically exposed person, cross-border activity in the stated nature and purpose, and a cash-intensive business line produces a High Customer Risk Rating. The case routes into Enhanced Due Diligence with routing reason CDD_HIGH_RISK_EDD, and activation is blocked.

9.2.6 Day 5, EDD review. The EDD analyst completes source-of-funds and source-of-wealth review per MJD-OPS-0003 and the designated EDD approver records onboarding approval.

9.2.7 Day 5, Stage 5. The account is created with reduced initial limits per the High-risk row of Section 5.3, dual-approval controls per MJD-OPS-0007 are configured, and authorized signers are screened and linked.

9.2.8 Day 6, Stage 6 and Stage 7. The entity funds the account by inbound wire processed under MJD-OPS-0004. With EDD approval recorded and funds posted, the system activates the account and a periodic-review flag is set for the High-risk relationship.

## 10. Case Management and Aging

10.1 Onboarding cases are monitored against the Section 1.1 service-level targets. A case exceeding its target is flagged and escalated to an Operations supervisor.

10.2 A case stalled at any gate for more than five business days is reviewed for closure; a conditional-open account that fails verification is restricted and closed per MJD-OPS-0001 Section 4.3.

### 10.3 Aging bands and actions

Cases are bucketed into aging bands measured in business days from intake, with customer-pending wait time excluded. Each band has a defined action and owner.

| Aging band | Status | Action | Owner |
|---|---|---|---|
| 0 to 5 days | On track | Continue straight-through processing | Operations Analyst |
| 6 to 8 days | At risk | Daily review; analyst documents the blocker | Operations Analyst |
| 9 to 10 days | Breached | Escalate to Operations supervisor | Operations supervisor |
| Over 10 days | Critical | Escalate to Head of Deposit Operations; closure review | Head of Deposit Operations |

### 10.4 Customer-pending handling

10.4.1 When a case waits on the customer for funds or documents, it is placed in a customer-pending state with a follow-up date. The internal service-level clock pauses while wait time accrues separately.

10.4.2 A customer-pending case receives reminders at three and seven business days. A case that remains customer-pending past ten business days is reviewed for closure.

### 10.5 Closure and reopening

10.5.1 A case closed for incompleteness or expired conditional-open verification records the closure reason and the disposition of any funds. A conditional-open account that fails verification is restricted and closed per MJD-OPS-0001 Section 4.3, with funded balances returned to the source of funds.

10.5.2 A closed case may be reopened only by creating a fresh application that re-runs all gates. A closed case is never silently advanced, because the underlying controls must be revalidated against current data.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Branch Staff | Capture applications, perform in-person CIP, accept funding, deliver welcome materials |
| Operations Analyst | Drive the case through gates, perform CDD, configure setup and limits, manage aging and exceptions |
| Compliance Officer | Clear or confirm potential sanctions and watchlist matches at the Stage 3 gate |
| EDD approver | Record onboarding approval for High-risk cases per MJD-OPS-0003 |
| Operations supervisor | Manage aging escalations, approve documented routing exceptions within authority |
| Head of Deposit Operations | Own this procedure, monitor service-level performance, approve workflow exceptions |

### Control ownership by gate

Separation of duties is preserved by assigning gate ownership distinct from the executing analyst where the control warrants it.

| Gate | Executed by | Control owner |
|---|---|---|
| Identity (Stage 2) | Operations Analyst | Operations Analyst |
| Screening (Stage 3) | System | Compliance Officer |
| Due diligence and EDD (Stage 4) | Operations Analyst | EDD approver for High risk |
| Setup and limits (Stage 5) | Operations Analyst | Operations supervisor for limit overrides |
| Activation (Stage 7) | System | Head of Deposit Operations for exceptions |

## Exceptions and Escalation

- A request to activate an account before a gate completes is not permitted except under the conditional-opening allowance in MJD-OPS-0001, which is itself bounded and approved.
- A High-risk activation requires EDD approval per MJD-OPS-0003 and may not be expedited around that control.
- Stalled or failed cases escalate to the Operations supervisor, then to the Head of Deposit Operations if unresolved within two business days.

### Escalation ladder

The following ladder governs how onboarding exceptions move when they cannot be resolved at the current level.

| Trigger | First responder | Escalates to | Timebox |
|---|---|---|---|
| Aging breach (9 to 10 days) | Operations supervisor | Head of Deposit Operations | 2 business days |
| Unresolved potential sanctions match | Compliance Officer | Compliance management | Per MJD-OPS-0008 |
| High-risk activation pressure | Operations supervisor | Head of Deposit Operations | Same business day |
| Conditional-open deadline lapse | Operations Analyst | Operations supervisor for closure | At deadline |
| Limit override request beyond authority | Operations supervisor | Head of Deposit Operations | 1 business day |

### Exception logging

Every exception records the routing reason, the requesting role, the approving role, the timestamp, and the resolution. The exception log is reviewed by the Head of Deposit Operations as part of the service-level performance review. An activation that bypassed a gate without a recorded approval is treated as a control failure and is reported through the bank's incident process rather than corrected silently.

## Related Documents

- MJD-OPS-0001 Customer Identification Program (CIP) Procedure
- MJD-OPS-0002 Customer Due Diligence (CDD) Standard
- MJD-OPS-0003 Enhanced Due Diligence (EDD) Procedure
- MJD-OPS-0007 Transaction Limits and Dual-Approval Matrix
- MJD-OPS-0008 Sanctions (OFAC) Screening Procedure
- MJD-OPS-0004 Wire Transfer Operations Runbook

## Regulatory References

- 31 CFR 1020.220 (Customer Identification Program)
- FinCEN Customer Due Diligence Rule, 31 CFR 1010.230
- Regulation CC, 12 CFR 229 (funds availability)
- Expedited Funds Availability Act

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2019-02-01 | Head of Deposit Operations | Initial onboarding workflow |
| 2.0.0 | 2021-03-15 | Head of Deposit Operations | Added stage-gate model and service-level targets |
| 3.0.0 | 2023-06-01 | Head of Deposit Operations | Integrated EDD routing for High-risk ratings |
| 3.1.0 | 2024-04-10 | Head of Deposit Operations | Added new-account funds-availability provisions |
| 3.2.0 | 2024-12-05 | Head of Deposit Operations | Aligned setup limits to OPS-0007 |
| 3.3.0 | 2025-08-20 | Head of Deposit Operations | Clarified case aging and closure timelines |
