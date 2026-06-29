---
doc_id: MJD-OPS-0008
title: Sanctions (OFAC) Screening Procedure
department: OPERATIONS
doc_type: PROCEDURE
classification: CONFIDENTIAL
owner_role: Head of Financial Crimes Operations
allowed_roles: [OPERATIONS_ANALYST, COMPLIANCE_OFFICER, RISK_ANALYST]
effective_date: 2025-11-20
version: 4.0.0
review_cycle_months: 12
regulatory_refs: ["31 CFR Part 501 (OFAC Reporting and Procedures)", "Executive Order 13224", "International Emergency Economic Powers Act", "OFAC SDN and Consolidated Sanctions Lists"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Sanctions (OFAC) Screening Procedure

## Purpose and Scope

This procedure defines how Meridian John Doe Financial (Meridian J.D.) screens customers, counterparties, and transactions against sanctions lists administered by the US Office of Foreign Assets Control (OFAC) and other applicable authorities, and how it adjudicates, holds, blocks, rejects, and reports sanctions exposure. Because it exposes screening thresholds and match-handling logic, this procedure is classified CONFIDENTIAL and is not visible to Branch Staff.

This procedure applies to all customers, all payment channels, and all Operations Analysts, Compliance Officers, and Risk Analysts who perform or oversee screening. It is invoked by the CIP procedure (MJD-OPS-0001), the onboarding workflow (MJD-OPS-0005), and the wire runbook (MJD-OPS-0004).

## Definitions

- **SDN List.** OFAC's list of Specially Designated Nationals and Blocked Persons.
- **Consolidated List.** OFAC's non-SDN consolidated sanctions list.
- **Potential Match (Hit).** A screening result above the configured fuzzy-match threshold requiring human review.
- **True Match.** A confirmed match to a sanctioned party.
- **False Positive.** A potential match that human review determines is not the sanctioned party.
- **Block.** Freezing property of a sanctioned party and reporting it to OFAC.
- **Reject.** Refusing to process a transaction involving a prohibited party or jurisdiction where no property is held to block.
- **Hit.** A single screening result that meets or exceeds the fuzzy-match threshold and is queued for human adjudication.
- **Alert.** The work item created from one or more hits on a single screened record, customer, or payment.
- **Fuzzy-match score.** A normalized similarity value from 0 to 100 produced by the screening engine for a candidate name pair, factoring exact tokens, phonetic equivalence, transposition, and edit distance.
- **Good-guy list.** The bank's reviewed and approved register of known-false-positive entries that suppresses repeat alerts for an exact party and reference combination.
- **50 Percent Rule.** OFAC's interpretive rule that an entity owned 50 percent or more, in the aggregate, by one or more blocked persons is itself treated as blocked even when not separately named on a list.
- **L1 and L2.** Level 1 (Operations Analyst) and Level 2 (Compliance Officer) review stages defined in Section 3.
- **TAT.** Turnaround time, measured from alert creation to disposition.

## 1. Screening Scope and Cadence

### 1.1 What is screened

1.1.1 **Customers and related parties** at onboarding and on every list update: account holders, authorized signers, and beneficial owners.

1.1.2 **Transactions** in real time before release: wires (originator, beneficiary, and intermediary parties), ACH where party data is available, and book transfers.

1.1.3 **Periodic rescreening** of the full customer base against the latest lists.

1.1.4 **Static reference data** that flows through payments: the bank's correspondent and respondent bank directory, vendor and supplier master, and employee and contractor records subject to screening under the bank's payroll and accounts-payable controls.

1.1.5 **Trade and ancillary parties** where the bank has visibility: letters of credit applicants and beneficiaries, guarantors, and the named ports, vessels, and goods descriptions in documentary collections.

### 1.2 Lists screened against

1.2.1 At minimum the OFAC SDN List and the OFAC Consolidated (non-SDN) List, including the Sectoral Sanctions Identifications List, the Foreign Sanctions Evaders List, and the Non-SDN Menu-Based Sanctions List.

1.2.2 Internal lists: the bank's prohibited-party list (entities the bank has independently barred), the comprehensively sanctioned jurisdiction list, and the good-guy list of approved false positives.

1.2.3 Where business activity warrants, the bank also loads United Nations consolidated, European Union consolidated, UK OFSI, and Canadian (OSFI) lists. OFAC remains the controlling authority for US-jurisdiction obligations described in this procedure.

### 1.3 Cadence

| Activity | Frequency | Control owner |
|---|---|---|
| Transaction screening | Real time, pre-release | Operations Analyst |
| New customer screening | At onboarding, before activation | Operations Analyst |
| Full-base rescreening | Within 24 hours of an OFAC list update | Operations Analyst |
| Scheduled full-base sweep | Daily | Operations Analyst |
| List ingestion and version verification | Each OFAC publication, same business day | Operations Analyst |
| Good-guy list revalidation | Every 12 months per entry | Compliance Officer |
| Threshold and tuning review | At least annually | Risk Analyst |
| OFAC annual blocked-property report | By September 30 for the prior calendar year | Compliance Officer |

### 1.4 List ingestion and version control

1.4.1 OFAC publishes list updates on an irregular schedule, sometimes multiple times in a single day. The screening team monitors the OFAC publication feed each business day and ingests every new list version.

1.4.2 On ingestion the analyst verifies the list version identifier, record count delta, and checksum against the source, then confirms the engine reports the new version active before any rescreening relies on it. A failed checksum or unexpected count delta halts ingestion and is escalated to the Head of Financial Crimes Operations.

1.4.3 The 24-hour full-base rescreening clock starts at the moment OFAC publishes the update, not at the moment of ingestion. Ingestion delays do not extend the rescreening deadline.

## 2. Match Thresholds and Tuning

### 2.1 Fuzzy-match threshold

2.1.1 The screening engine uses a configurable fuzzy-match score from 0 to 100. The production match threshold is set at **85**; names scoring at or above 85 generate a potential match for review.

2.1.2 Threshold changes require joint approval by the Head of Financial Crimes Operations and a Compliance Officer, and are documented with the tuning rationale and a before-and-after false-positive analysis.

2.1.3 The production threshold of 85 is a floor for routing to human review, not a ceiling on diligence. Scores below 85 are not auto-cleared in a way that destroys the underlying screening record; the engine retains all scored candidate pairs for lookback and tuning analysis. The bank does not raise the threshold above 85 without documented evidence that the missed-match risk remains acceptable.

2.1.4 Field weighting. The engine scores primary name tokens most heavily, then secondary identifiers (date of birth, nationality, identifier numbers, address country). A strong identifier corroboration (for example, a matching passport number) can elevate an otherwise weak name score to a hit through the secondary-identifier rule, independent of the 85 name threshold.

### 2.2 Score bands and routing

| Fuzzy-match score | Classification | Routing |
|---|---|---|
| 0 to 84 | Below threshold | No alert generated; record retained for lookback |
| 85 to 94 | Potential match | Alert created, routed to Level 1 |
| 95 to 99 | Strong potential match | Alert created, Level 1 with mandatory identifier check |
| 100, or any list-program exact identifier match | Near-certain | Alert created, expedited to Level 2 awareness while Level 1 documents |

The score band sets handling intensity. It never auto-dispositions an alert; every alert at or above 85 requires a documented human decision.

### 2.3 Good-guy and known-false-positive lists

2.3.1 A reviewed and approved known-false-positive entry suppresses repeat alerts for the exact same party and reference, with periodic revalidation every 12 months. Suppression never applies to a new list designation.

2.3.2 A good-guy entry is keyed to the specific customer or party record plus the specific listed entry it was cleared against. If OFAC adds a new program, alias, or identifier to that listed entry, or designates a new entity with a similar name, the suppression does not apply and a fresh alert is raised.

2.3.3 Good-guy entries are created only after a completed Level 1 disposition (and Level 2 where it was escalated). Analysts cannot self-approve a good-guy entry for a party they cleared without a second reviewer signing the entry.

## 3. Match Adjudication

### 3.1 Level 1 review (Operations Analyst)

3.1.1 On a potential match, the analyst compares the screened party to the listed party across name, date of birth, address, identifiers, and program. The analyst documents the comparison.

3.1.2 A clear false positive is dispositioned and the rationale recorded. Anything not clearly a false positive escalates to Level 2.

3.1.3 Level 1 decision sequence:

1. Open the alert and record the engine score, list version, and listed-entry program.
2. Read the full listed-entry record, including all aliases (a.k.a., f.k.a.), addresses, and identifiers.
3. Compare each available data element of the screened party against the listed entry using the decision table in 3.4.
4. Check the good-guy list for a prior cleared disposition for this exact party and reference.
5. For a payment alert, read the full payment message, not only the flagged field, to confirm which party triggered the hit and whether other parties also score.
6. Reach one of three outcomes: clear as false positive (document and close), escalate to Level 2 (potential or confirmed concern), or request more information from the originating channel while the item stays held.
7. Record the disposition, the data elements compared, the deciding factor, and the analyst identifier and timestamp.

3.1.4 An analyst never clears an alert on name dissimilarity alone when a strong secondary identifier matches the listed entry. Identifier corroboration overrides a weak name argument and forces escalation.

### 3.2 Level 2 review (Compliance Officer)

3.2.1 Compliance confirms or clears the match. A confirmed true match proceeds to block or reject under Section 4.

3.2.2 The transaction or relationship remains held throughout adjudication. Nothing funds, releases, or activates with an open potential match.

3.2.3 Level 2 also applies the OFAC 50 Percent Rule: where a screened party is not itself listed but is owned 50 percent or more in the aggregate by one or more blocked persons, Compliance treats the party as blocked and proceeds under Section 4.

3.2.4 Where the available data is genuinely insufficient to confirm or clear, Compliance may direct an information request to the customer or correspondent. The item remains held during the request. If the information request cannot resolve a transaction within applicable processing windows and concern remains, Compliance rejects or holds rather than releasing.

### 3.3 Service-level targets

| Step | Target |
|---|---|
| Level 1 review of a transaction hit | Within 2 hours during business hours |
| Level 2 confirmation | Same business day |
| Level 1 review of a customer or list-update hit | Within 1 business day |
| Information request issued after Level 2 decision to hold | Same business day |
| OFAC report on a true match | Within 10 business days of the blocking action |

A transaction alert that cannot be dispositioned within the Level 1 target during business hours is escalated to a Compliance Officer for visibility rather than left to age. After-hours transaction hits are queued and worked at the start of the next business window, and the held transaction does not release in the interim.

### 3.4 Match-adjudication decision table

The analyst evaluates the screened party against the listed entry across the data elements below. The aggregate pattern, not any single row, drives the disposition.

| Data element comparison | Indication | Weight |
|---|---|---|
| Full name exact or near-exact, including alias | Toward true match | High |
| Name matches but is common and generic | Inconclusive alone | Low |
| Date of birth matches listed entry | Toward true match | High |
| Date of birth clearly differs (verified) | Toward false positive | High |
| Nationality or country matches listed program geography | Toward true match | Medium |
| Government identifier (passport, national ID, tax ID) matches | Toward true match | Decisive |
| Address in a different, unrelated country with no other corroboration | Toward false positive | Medium |
| Party is a well-known unrelated public entity with documented identity | Toward false positive | Medium |
| Hit is on a free-text field (notes, remittance info) not a party field | Toward false positive, verify context | Medium |

| Aggregate pattern | Disposition |
|---|---|
| Only a generic-name match with verified differing identifiers and geography | Clear as false positive at Level 1, document |
| Name match with no corroborating identifiers and no disqualifying data | Escalate to Level 2 |
| Name match plus any matching strong identifier | Treat as potential true match, escalate to Level 2 |
| Matching government identifier regardless of name spelling | Treat as true match, escalate to Level 2 immediately |
| Ownership 50 percent or more by a blocked person | Treat as blocked under the 50 Percent Rule, Level 2 |

## 4. Blocking, Rejecting, and Reporting

### 4.1 Blocking

4.1.1 On a true match where the bank holds property (for example, an inbound wire to a blocked party), the bank blocks the property into an interest-bearing blocked account and does not release it.

4.1.2 The block is reported to OFAC within 10 business days.

### 4.2 Rejecting

A prohibited transaction in which no property is held to block is rejected and reported to OFAC within 10 business days where reporting is required.

### 4.3 Annual report

The bank files the OFAC annual report of blocked property by the regulatory deadline (September 30 for the prior calendar year).

### 4.4 SAR coordination

A true match or evident evasion is coordinated with Compliance for a SAR determination under MJD-CMP-0002. Sanctions reporting to OFAC and SAR filing are separate obligations and both may apply.

### 4.5 Blocking and reporting step sequence

1. Level 2 confirms the true match and records the listed-entry citation and program.
2. Compliance holds the property and, where the bank holds funds, books them to a segregated interest-bearing blocked account established for blocked property. Funds are never returned to the remitter and never released to the beneficiary.
3. Compliance freezes any related accounts of the blocked party at the bank and suspends outbound activity.
4. Compliance prepares the OFAC initial block report and files it within 10 business days of the blocking action.
5. Compliance opens the SAR determination workflow under MJD-CMP-0002 in parallel.
6. The blocked property is tracked for inclusion in the OFAC annual blocked-property report due September 30 for the prior calendar year.
7. The Head of Financial Crimes Operations and the BSA Officer are notified the same business day.

### 4.6 Worked example A: Level 1 false positive cleared

An inbound wire names beneficiary "Ahmed Ali," scoring 88 against an SDN-listed "Ahmed Ali." The Operations Analyst opens the alert within the 2-hour business-hours target, reads the listed entry, and finds the SDN record carries a specific date of birth, an Iranian passport number, and a Tehran address under an Iran program. The bank's customer is a 20-year US permanent resident with a US-issued identifier on file, a US date of birth that differs by 14 years from the listed entry, and no nexus to the listed program geography. The name is common and the only matching element is the name token. Applying the decision table, the analyst records a verified differing date of birth (high weight toward false positive), a non-matching government identifier, and unrelated geography. The analyst clears the alert as a false positive, documents the elements compared and the deciding factors, releases the held wire, and creates a good-guy entry keyed to this customer and this listed entry with a 12-month revalidation date. No escalation to Level 2 is required.

### 4.7 Worked example B: true match blocked and reported

An inbound wire credits an account, and the originator field scores 96 against an SDN-listed entity. The Operations Analyst escalates to Level 2 the same business day after confirming the originator's stated address country matches the listed program geography and an enclosed registration number matches an identifier on the listed entry. The Compliance Officer confirms the true match. Because the bank holds the inbound funds, this is a block, not a reject. Compliance books the funds to a segregated interest-bearing blocked account, freezes the crediting relationship, and notifies the BSA Officer and the Head of Financial Crimes Operations the same business day. Compliance files the OFAC initial block report within 10 business days of the blocking action, opens a SAR determination under MJD-CMP-0002, and tags the property for the September 30 annual blocked-property report. The funds are not returned to the originator and not released to the intended beneficiary.

### 4.8 Worked example C: reject with no property held

An outbound wire instruction names an intermediary bank in a comprehensively sanctioned jurisdiction. No property is held at the bank to block because the instruction has not yet funded an outbound leg the bank controls. The Operations Analyst escalates, Compliance confirms the prohibited nexus, and the transaction is rejected rather than blocked. Compliance files an OFAC reject report within 10 business days where reporting is required, notifies the customer of the rejection consistent with the bank's communications controls, and refers the pattern to Section 5 evasion review.

## 5. Evasion Typologies

5.1 Watch for evasion indicators: misspelled or transliterated names, omitted party fields, use of intermediaries in high-risk jurisdictions, and last-minute beneficiary changes. Such indicators may warrant manual screening and EDD (MJD-OPS-0003).

### 5.2 Typology detail

| Typology | What it looks like | Screening response |
|---|---|---|
| Name manipulation | Deliberate misspelling, alternate transliteration, name reordering, dropped middle names, or initials in place of full names | Lower-confidence fuzzy hits worked at face value, never cleared on spelling alone; cross-check identifiers |
| Field stripping | Payment messages with blank or vague originator or beneficiary fields, or party data pushed into free-text remittance fields | Treat incomplete party data as a red flag; request complete data, hold pending |
| Front and shell companies | Newly formed entities, generic trade names, shared addresses, or ownership tracing to a blocked person | Apply 50 Percent Rule; refer to EDD under MJD-OPS-0003 |
| Nested correspondent abuse | Downstream banks routing prohibited-jurisdiction traffic through a respondent's account | Screen all named parties in the chain; review respondent activity patterns |
| Intermediary layering | Insertion of additional banks or trading parties in high-risk jurisdictions to obscure the true counterparty | Screen every party; scrutinize jurisdiction logic of the routing |
| Last-minute changes | Beneficiary, amount, or routing changed after initial submission or repeated cancel-and-resubmit | Re-screen on every amendment; flag repeated amendments for review |
| Goods and vessel concealment | Dual-use goods descriptions, vague cargo, flagged vessels, or ship-to-ship transfer indicators in trade documents | Screen ports, vessels, and goods terms; refer to trade-finance review |
| Convert-and-route | Conversion of value through instruments or accounts intended to break the audit trail to a sanctioned destination | Pattern referral to transaction monitoring under MJD-CMP-0004 |

### 5.3 Handling

5.3.1 An evasion indicator never auto-clears. The presence of an evasion typology raises the diligence floor for the alert and, where a transaction is involved, keeps the item held until the concern is resolved.

5.3.2 A pattern of evasion indicators across multiple transactions or customers is referred to transaction monitoring under MJD-CMP-0004 and to Compliance for a SAR determination under MJD-CMP-0002, independent of whether any single alert resolves to a true match.

## 6. Recordkeeping

6.1 All screening results, adjudications, blocks, rejections, and OFAC reports are retained for at least five years per MJD-CMP-0008.

6.2 Threshold-tuning decisions and false-positive analyses are retained as model-governance evidence and shared with Risk under MJD-RSK-0003.

6.3 Each alert disposition record captures, at minimum: the engine score, the list version and listed-entry citation, every data element compared, the deciding factors, the disposition reached, the reviewer identifier at each level, and timestamps for alert creation, Level 1 disposition, and any Level 2 disposition.

6.4 Block and reject records additionally capture the property amount and account, the OFAC report reference and filing date, and any related SAR reference, with cross-links so a single event can be reconstructed across sanctions and SAR records.

### 6.5 Quality assurance and tuning governance

6.5.1 A monthly quality-assurance sample of closed alerts, including a defined share of false-positive clears, is independently re-reviewed by a reviewer who did not make the original disposition. QA findings feed back into analyst coaching and tuning.

6.5.2 The Risk Analyst monitors the false-positive rate, the volume of alerts at each score band, and TAT performance against the Section 3.3 targets. Sustained drift is documented and presented at the at-least-annual tuning review.

6.5.3 Any proposal to change the production threshold of 85 follows Section 2.1.2: joint approval, a documented before-and-after false-positive analysis, and a missed-match risk assessment. Below-threshold scored pairs retained under Section 2.1.3 supply the lookback population for that analysis. No threshold change takes effect without recorded approval and a model-governance entry shared with Risk under MJD-RSK-0003.

6.5.4 Pre-deployment of any screening-engine version change, the team validates list ingestion, scoring behavior against a known test population, and good-guy suppression behavior, and records the validation as model-governance evidence.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Operations Analyst | Perform Level 1 review, document comparisons, hold transactions during adjudication |
| Compliance Officer | Perform Level 2 confirmation, direct blocks and rejects, file OFAC reports, coordinate SARs |
| Risk Analyst | Validate screening-model tuning, monitor false-positive rates and TAT, run lookback analysis, report sanctions risk to enterprise risk |
| Head of Financial Crimes Operations | Own this procedure, approve threshold changes, oversee list ingestion integrity, ensure timely OFAC reporting |
| BSA Officer | Receive immediate notice of confirmed true matches, oversee SAR coordination, escalate to senior management as warranted |
| QA Reviewer | Independently re-review sampled dispositions, surface coaching and tuning findings |

## Exceptions and Escalation

- No exception permits releasing a transaction or activating a relationship while a potential sanctions match is open. This control admits no manager override, no time-pressure waiver, and no relationship-value exception.
- A threshold-tuning exception requires joint Head of Financial Crimes Operations and Compliance approval with documented analysis.
- Any confirmed true match is escalated immediately to Compliance and the BSA Officer.
- A held transaction approaching its processing-window deadline is rejected or held, never released, where a sanctions concern remains open. The deadline pressure of a payment channel is never grounds to release an open alert.
- A failed list ingestion, a screening-engine outage, or any condition that prevents real-time pre-release screening triggers immediate escalation to the Head of Financial Crimes Operations. During such a condition, affected transactions are held and screened manually before release; they are not released unscreened.
- Suspected or attempted evasion is escalated to Compliance for SAR determination under MJD-CMP-0002 regardless of whether the underlying alert resolves to a true match.

### Escalation path

1. Operations Analyst (Level 1) identifies and adjudicates the alert; clears clear false positives, escalates everything else.
2. Compliance Officer (Level 2) confirms or clears; directs blocks, rejects, and information requests.
3. Head of Financial Crimes Operations and BSA Officer receive same-business-day notice of confirmed true matches and of any screening-capability failure.
4. Senior management and, where warranted, OFAC voluntary self-disclosure are considered by the BSA Officer for material events.

## Related Documents

- MJD-OPS-0001 Customer Identification Program (CIP) Procedure
- MJD-OPS-0003 Enhanced Due Diligence (EDD) Procedure
- MJD-OPS-0004 Wire Transfer Operations Runbook
- MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure
- MJD-CMP-0004 Transaction Monitoring Rules and Thresholds
- MJD-RSK-0003 Operational Risk Procedure

## Regulatory References

- 31 CFR Part 501 (OFAC Reporting, Procedures, and Penalties Regulations)
- Executive Order 13224
- International Emergency Economic Powers Act (IEEPA)
- OFAC Specially Designated Nationals and Consolidated Sanctions Lists

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2018-06-01 | Head of Financial Crimes Operations | Initial OFAC screening procedure |
| 2.0.0 | 2020-09-10 | Head of Financial Crimes Operations | Added real-time transaction screening |
| 3.0.0 | 2022-11-01 | Head of Financial Crimes Operations | Introduced fuzzy-match threshold governance |
| 3.5.0 | 2024-08-15 | Head of Financial Crimes Operations | Added evasion-typology guidance |
| 4.0.0 | 2025-11-20 | Head of Financial Crimes Operations | Set production match threshold at 85 and codified adjudication service levels |
