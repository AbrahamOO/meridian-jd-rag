---
doc_id: MJD-OPS-0001
title: Customer Identification Program (CIP) Procedure
department: OPERATIONS
doc_type: PROCEDURE
classification: INTERNAL
owner_role: Head of Deposit Operations
allowed_roles: [OPERATIONS_ANALYST, COMPLIANCE_OFFICER, BRANCH_STAFF]
effective_date: 2025-09-01
version: 4.1.0
review_cycle_months: 12
regulatory_refs: ["31 CFR 1020.220", "USA PATRIOT Act Section 326", "31 USC 5318(l)", "FinCEN CDD Rule 31 CFR 1010.230"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Customer Identification Program (CIP) Procedure

## Purpose and Scope

This procedure defines how Meridian John Doe Financial (Meridian J.D.) identifies and verifies the identity of every person who opens an account. It operationalizes the bank's Customer Identification Program (CIP) as required under the bank's BSA/AML Program Policy. The CIP is the first control in the account lifecycle and feeds downstream Customer Due Diligence and risk rating.

This procedure applies to:

- All new account openings across retail branches, the digital onboarding channel, the contact center, and business banking relationship managers.
- All account types: consumer deposit, business deposit, certificates of deposit, and small business lending relationships originated through the deposit platform.
- All Meridian J.D. staff who collect, key, verify, or approve customer identifying information, including Branch Staff, Operations Analysts, and Compliance Officers performing quality reviews.

This procedure does not cover the deeper risk-rating and beneficial-ownership analysis performed during Customer Due Diligence (see MJD-OPS-0002) or the heightened review performed during Enhanced Due Diligence (see MJD-OPS-0003). It is the identity-collection and identity-verification layer only.

## Definitions

- **Customer.** A person who opens a new account, or an existing customer who opens a new account where the bank does not already have a current verified identity record on file.
- **Account.** A formal banking relationship established to provide deposit, credit, or other financial services. A one-time wire for a non-customer is not an account for CIP purposes but is screened under MJD-OPS-0008.
- **CIP Record.** The structured set of identifying information and verification evidence retained for each customer: name, date of birth, residential or business street address, and identification number.
- **Identification Number.** For a US person, a taxpayer identification number (SSN or ITIN). For a non-US person, one or more of: a passport number and country of issuance, an alien identification card number, or a government-issued document number bearing a photograph.
- **Documentary Verification.** Verifying identity by reviewing an unexpired government-issued identification document.
- **Non-Documentary Verification.** Verifying identity through independent data sources such as a credit bureau identity check, a public-records database, or a third-party identity verification vendor.
- **CIP Exception.** A new account that is opened before identity verification is fully complete, under the time-bound conditional-opening allowance in Section 4.
- **Discrepancy.** A material difference between customer-provided information and verification evidence, for example a name mismatch, an address that fails to resolve, or an identification number that does not validate.
- **Authorized Signer.** A natural person granted authority to transact on an account who is not the primary accountholder, including officers of an entity and individuals on a consumer joint account.
- **Identity Queue.** The Operations work queue into which flagged, partial-match, and discrepant applications are routed for analyst adjudication.
- **CIP Owner.** The Head of Deposit Operations, accountable for the design and operating effectiveness of the program.

## 1. CIP Information Collection

### 1.1 Minimum required information

Before opening any account, staff must collect the following four data elements for each customer and, where applicable, each authorized signer:

1. Full legal name.
2. Date of birth (for an individual).
3. A physical residential or business street address. A post office box alone is not acceptable for an individual. An Army Post Office or Fleet Post Office address is acceptable. A registered-agent address is acceptable for an entity only when paired with the entity's principal place of business.
4. Identification number as defined above.

### 1.2 Collection by channel

1.2.1 **Branch.** Branch Staff key the four elements into the onboarding platform and scan the presented identification document into the imaging system at 300 dpi minimum. The platform validates field formats at entry: the identification number is checked for structural validity (nine digits for an SSN or ITIN), the date of birth is checked against an age floor of 18 years for an individual primary accountholder, and the address is passed to an address-standardization service that returns a deliverable, standardized format.

1.2.2 **Digital.** The applicant enters the four elements; the platform performs an automated non-documentary check and, on a flagged result, routes the application to the Operations identity queue for analyst review within one business day. The digital channel additionally captures device and session signals (device fingerprint, IP geolocation, and velocity of prior applications from the same device) that feed the fraud-screening model under MJD-RSK-0007 but are not part of the CIP record itself.

1.2.3 **Contact center.** Agents collect the four elements verbally, then trigger a non-documentary check; documentary verification by mail-in or branch visit is required if the non-documentary check does not clear. Contact-center agents follow a scripted knowledge-based authentication sequence and may not waive any element.

1.2.4 **Business banking.** Relationship managers collect the entity elements and beneficial-ownership elements together and submit a packaged application; the package is not advanced until every required field for the entity and each beneficial owner is present.

### 1.2A Data-quality gates at collection

The following gates are enforced before an application can advance from collection to verification. A failed gate returns the application for correction and is logged.

| Gate | Rule | Failure handling |
|---|---|---|
| Name completeness | Full legal first and last name present; single-name entities flagged for review | Return for correction |
| Date of birth | Valid date, age >= 18 for individual primary | Return; minor accounts follow the custodial path |
| Address | Resolves to a deliverable street address; PO box alone rejected for individuals | Return; request street address |
| Identification number | Structurally valid SSN, ITIN, or documented foreign identifier | Return; route foreign identifiers to analyst |
| Duplicate check | No exact match to an existing verified customer record unless intentional add-on | Link to existing customer or flag |

### 1.3 Entity customers

For a legal entity, in addition to the entity's own four elements, staff collect beneficial-ownership information under the FinCEN CDD Rule. Beneficial-ownership collection and certification are governed by MJD-OPS-0002 Section 3; the CIP layer captures and verifies the identity of each natural-person beneficial owner using the same four elements and the same verification methods set out below.

1.3.1 **Entity elements collected.** Legal entity name, any operating or trade name, principal place of business street address, entity taxpayer identification number (EIN), state and date of formation, and entity type.

1.3.2 **Formation evidence.** A current entity formation or registration document (articles of incorporation, articles of organization, partnership agreement, or equivalent) and, where the entity has been operating, evidence of good standing dated within the prior 12 months.

1.3.3 **Authorized-signer identity.** Each authorized signer is subject to the full individual CIP, including the four elements and verification, before that signer may transact.

## 2. Identity Verification

### 2.1 Verification method selection

Meridian J.D. uses a risk-based combination of documentary and non-documentary verification. The minimum standard is:

| Customer type | Minimum verification |
|---|---|
| Consumer, in person | One primary photo ID, documentary |
| Consumer, remote | Non-documentary check, plus one photo ID if the non-documentary check does not fully clear |
| Business entity | Entity formation document plus non-documentary entity verification, plus documentary verification of each beneficial owner |
| Higher-risk customer (per MJD-OPS-0002 risk rating) | Documentary plus non-documentary, both required |

### 2.2 Acceptable documentary evidence

2.2.1 **Primary identification (one required).** Unexpired US state driver license, unexpired US state identification card, unexpired US passport, unexpired foreign passport, US permanent resident card, or US military identification card.

2.2.2 **Secondary identification (one required when a non-photo primary is used or the primary is questioned).** Social Security card, original birth certificate, recent utility bill in the customer's name, or a major-network debit or credit card in the customer's name.

2.2.3 Documents must be unexpired. An expired document may be accepted only with a documented Operations supervisor override and a compensating non-documentary check.

2.2.4 **Document authenticity checks.** For each presented document the reviewer confirms: the photograph reasonably matches the presenter, the document is not visibly altered, security features expected for the document type are present, and the document number and expiry are legible. Branch reviewers use the document-authentication reference card maintained by Deposit Operations. Remote channels rely on the vendor's document-liveness and authenticity scoring.

### 2.2A Discrepancy resolution

2.2A.1 A discrepancy between the four elements and the verification evidence is logged and must be resolved before verification is deemed complete. Common discrepancy types and required resolution:

| Discrepancy | Required resolution |
|---|---|
| Name mismatch (maiden, hyphenation, transposition) | Obtain a linking document (marriage certificate, court order) or a second matching ID |
| Address mismatch | Obtain a current proof of address dated within 60 days |
| Date-of-birth mismatch | Re-key and re-verify; persistent mismatch escalates to analyst |
| Identification-number fails validation | Documentary re-verification in person; foreign identifiers routed to analyst |

2.2A.2 A discrepancy that cannot be reasonably resolved is treated as a verification failure under Section 4.2.

### 2.3 Non-documentary verification

2.3.1 The non-documentary check compares the customer-supplied identity to at least two independent data sources. A full clear requires a name, address, date-of-birth, and identification-number match at or above the vendor's configured confidence threshold.

2.3.2 A partial match (three of four elements) routes to the Operations identity queue for analyst adjudication. The analyst either clears with a supporting documentary item or escalates.

2.3.3 A no-match result blocks account opening and requires documentary verification in person.

2.3.4 **Independent-source requirement.** The two data sources used must be independent of each other and independent of the applicant. A source that simply echoes applicant-supplied data does not count toward the two-source minimum.

### 2.3A Verification service-level targets

| Channel and result | Verification SLA |
|---|---|
| Branch documentary, clean | Same business day |
| Digital non-documentary, full clear | Real time at submission |
| Identity-queue partial match | Adjudicated within 1 business day |
| Contact-center mail-in documentary | Within 2 business days of document receipt |
| Entity with beneficial owners | Within 3 business days of complete package |

### 2.4 Verification timing

Identity must be verified within a reasonable time. Meridian J.D. defines the standard as completion of verification before the account is used for any transaction, and in all cases no later than **five business days** after account opening under the conditional-opening allowance in Section 4. Accounts not verified within five business days are restricted and scheduled for closure under Section 4.3.

### 2.5 Worked verification examples

2.5.1 **Example A, clean in-person consumer.** An applicant presents an unexpired state driver license at a branch. Branch Staff image the license, confirm photo and security features, key the four elements, and the platform validates the SSN format and address. Verification completes same day; no non-documentary check is required because in-person documentary verification is sufficient for a standard-risk consumer.

2.5.2 **Example B, remote partial match.** A digital applicant's name, date of birth, and identification number match but the address fails to resolve. The application routes to the identity queue. The analyst requests a utility bill dated within 60 days, confirms the address, and clears the partial match within one business day.

2.5.3 **Example C, entity with layered ownership.** A newly formed limited liability company applies. The entity elements verify, but one beneficial owner is held through an intermediate holding company. CIP verifies the identity of the natural-person owners that can be reached; the unresolved layer is referred to CDD and, if it remains opaque, to EDD under MJD-OPS-0003.

## 3. Government List Screening

### 3.1 OFAC and watchlist screening

Every CIP record is screened against the applicable sanctions and government lists at account opening. The screening logic, list sources, and disposition workflow are defined in MJD-OPS-0008 Sanctions (OFAC) Screening Procedure. CIP does not duplicate that logic; it ensures the screen is invoked and that an account is not activated while a potential sanctions match is unresolved.

### 3.2 Potential match handling

A potential list match places the account in pending status. The account cannot fund or transact until Compliance clears or confirms the match per MJD-OPS-0008. A confirmed match is reported per the BSA/AML Program Policy and the account is not opened.

## 4. Conditional Opening and Verification Failures

### 4.1 Conditional opening allowance

An account may be opened and limited activity permitted before verification completes, provided:

1. The four required elements were collected.
2. Government-list screening returned no unresolved potential match.
3. Verification is completed within five business days.
4. Aggregate activity before verification does not exceed a single funding deposit and no outbound wire or external transfer is permitted.

### 4.2 Verification failure

If identity cannot be reasonably verified, staff must not open the account, or must restrict and close a conditionally opened account. The bank determines whether filing a Suspicious Activity Report is warranted under MJD-CMP-0002. Operations does not make the SAR determination; it refers the matter to Compliance.

### 4.3 Restriction and closure

4.3.1 An unverified account is placed in transaction-restricted status on day six.

4.3.2 The Operations Analyst issues a closure notice and returns funds to the originating source after a ten-business-day hold, unless Compliance directs otherwise.

4.3.3 **Restriction sequence.** Day six applies a debit block and disables outbound transfers while leaving the account viewable to the customer. Day six also triggers an automated customer outreach requesting the missing verification. If verification is supplied during the restriction window, the analyst lifts the restriction within one business day of confirming the evidence.

### 4.4 Conditional-opening control table

| Control point | Requirement | Owner |
|---|---|---|
| Pre-open screening | No unresolved sanctions match | Operations Analyst |
| Funding limit | Single funding deposit only, no outbound | System |
| Verification deadline | Complete within 5 business days | Operations Analyst |
| Day-6 restriction | Debit block, outbound disabled, customer outreach | System and analyst |
| Day-16 closure | Funds returned after 10-business-day hold | Operations Analyst |

## 5. Recordkeeping

### 5.1 What is retained

The CIP record retains: the four identifying elements, a description of each document reviewed (type, issuer, number, expiration), the method and result of any non-documentary check, and the resolution of any discrepancy.

### 5.2 Retention period

CIP records are retained for **five years after the account is closed**, consistent with the Records Retention Schedule (MJD-CMP-0008). Imaging copies of identification documents follow the same retention.

### 5.3 Synthetic test record

The following is a clearly marked fictional test record used only for ingestion and verification testing. It is not a real customer.

> TEST RECORD (synthetic, not a real person): Name "Jordan A. Doe-Sample", DOB 1990-01-01, address "100 Example Way, Testville, ZZ 00000", SSN 000-00-0000, ID "DL TEST-0000000". Source: fabricated for demonstration.

### 5.4 Customer notice

At or before account opening, the customer is provided the required CIP notice explaining that federal law requires the bank to obtain, verify, and record identifying information. The notice text and its delivery (posted at branches, displayed in the digital flow, and read in the contact-center script) are standardized and version-controlled by Compliance.

## 6. Quality Control and Program Oversight

### 6.1 Quality-control sampling

6.1.1 Compliance samples a minimum of 5 percent of new accounts per month for CIP completeness, with a higher sampling rate of 25 percent for accounts opened under the conditional-opening allowance and 100 percent review of accounts with an unresolved discrepancy that was later cleared.

6.1.2 Sampling tests: presence of all four elements, evidence of verification method and result, discrepancy resolution, sanctions screening invocation, and customer-notice delivery.

### 6.2 Metrics and reporting

The Head of Deposit Operations reports the following CIP metrics monthly to the BSA Officer:

| Metric | Target |
|---|---|
| Verification completed within SLA | >= 98 percent |
| Conditional opens verified within 5 business days | >= 95 percent |
| Open discrepancies aged over 5 business days | 0 |
| QC sample defect rate | <= 2 percent |
| Repeat non-documentary no-match rate by channel | Monitored for trend |

### 6.3 Program review

This procedure is reviewed at least every 12 months and upon any material change in law, vendor, or channel. Material changes are approved by the Head of Deposit Operations with Compliance concurrence and reflected in the revision history.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Branch Staff | Collect the four elements, perform in-person documentary verification, image documents, escalate discrepancies |
| Operations Analyst | Adjudicate non-documentary partial matches, manage the identity queue, drive conditional-opening timelines, restrict and close unverified accounts |
| Compliance Officer | Set the risk-based verification standard, review CIP quality samples, make SAR and sanctions-clearance determinations |
| Head of Deposit Operations | Own this procedure, approve exceptions, report CIP metrics to the BSA Officer |

## Exceptions and Escalation

- A documented exception (for example, accepting an expired document with a compensating control) requires Operations supervisor approval and is logged in the exception register with a 30-day review.
- Any suspected identity fraud is escalated immediately to Compliance and the Fraud Risk function under MJD-RSK-0007.
- Repeated non-documentary no-match results from a single channel are escalated to the Head of Deposit Operations as a potential control gap.
- An exception may never waive sanctions screening, the four required elements, or the requirement to verify each authorized signer. These are non-waivable controls.
- A conditional-opening verification deadline may be extended by up to three additional business days only with Operations supervisor approval and only where verification is in progress and documented; the funding-limit and outbound-block controls remain in force during any extension.

### Escalation ladder

| Trigger | First escalation | Second escalation |
|---|---|---|
| Unresolved discrepancy aged over 5 business days | Operations supervisor | Head of Deposit Operations |
| Suspected identity fraud | Fraud Risk (MJD-RSK-0007) and Compliance | BSA Officer |
| Potential sanctions match | Compliance (MJD-OPS-0008) | BSA Officer |
| Systemic verification failures by channel | Head of Deposit Operations | BSA Officer and Risk |

## Related Documents

- MJD-OPS-0002 Customer Due Diligence (CDD) Standard
- MJD-OPS-0003 Enhanced Due Diligence (EDD) Procedure
- MJD-OPS-0008 Sanctions (OFAC) Screening Procedure
- MJD-OPS-0005 Account Onboarding Workflow
- MJD-CMP-0002 Suspicious Activity Report (SAR) Filing Procedure
- MJD-CMP-0008 Records Retention Schedule

## Regulatory References

- 31 CFR 1020.220 (Customer Identification Programs for banks)
- USA PATRIOT Act Section 326
- 31 USC 5318(l)
- FinCEN Customer Due Diligence Rule, 31 CFR 1010.230 (beneficial ownership identification)

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2019-04-15 | Head of Deposit Operations | Initial CIP procedure |
| 2.0.0 | 2021-06-01 | Head of Deposit Operations | Added digital onboarding non-documentary flow |
| 3.0.0 | 2023-05-10 | Head of Deposit Operations | Aligned beneficial-ownership capture with CDD Rule |
| 4.0.0 | 2024-11-01 | Head of Deposit Operations | Added conditional-opening five-business-day standard |
| 4.1.0 | 2025-09-01 | Head of Deposit Operations | Clarified entity verification table and closure timeline |
