---
doc_id: MJD-OPS-0002
title: Customer Due Diligence (CDD) Standard
department: OPERATIONS
doc_type: STANDARD
classification: INTERNAL
owner_role: Head of Financial Crimes Operations
allowed_roles: [OPERATIONS_ANALYST, COMPLIANCE_OFFICER, RISK_ANALYST]
effective_date: 2025-10-15
version: 3.2.0
review_cycle_months: 12
regulatory_refs: ["FinCEN CDD Rule 31 CFR 1010.230", "31 CFR 1020.210", "FFIEC BSA/AML Examination Manual", "USA PATRIOT Act Section 326"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Customer Due Diligence (CDD) Standard

## Purpose and Scope

This standard defines the Customer Due Diligence (CDD) that Meridian John Doe Financial (Meridian J.D.) performs to understand the nature and purpose of customer relationships, develop a customer risk profile, and conduct ongoing monitoring. CDD builds directly on the identity collected and verified under the Customer Identification Program (MJD-OPS-0001) and determines whether a relationship requires Enhanced Due Diligence (MJD-OPS-0003).

This standard applies to all customer relationships across all lines of business and to all staff who open, risk-rate, monitor, or review customer relationships. It is binding on Operations, Compliance, and Risk.

The four pillars of CDD covered here are: (1) customer identification and verification (by reference to MJD-OPS-0001), (2) beneficial ownership identification for legal-entity customers, (3) understanding the nature and purpose of the relationship to develop a risk profile, and (4) ongoing monitoring to maintain and update that profile.

## Definitions

- **Customer Risk Rating (CRR).** A composite score (Low, Moderate, High) assigned at onboarding and refreshed on a schedule, expressing money-laundering and terrorist-financing risk.
- **Beneficial Owner.** Under the ownership prong, each natural person who owns 25 percent or more of the equity interests of a legal-entity customer. Under the control prong, one individual with significant managerial responsibility.
- **Legal-Entity Customer.** A corporation, limited liability company, partnership, or similar entity formed by filing with a state or comparable authority. Excludes certain entity types listed in the CDD Rule.
- **Nature and Purpose.** The expected activity of the relationship: products used, anticipated transaction types, volumes, geographies, and counterparties.
- **Ongoing Monitoring.** The continuous process of reviewing transactions against the expected profile and updating customer information.
- **Trigger Event.** An event that requires a profile refresh outside the scheduled cycle, such as a transaction-monitoring alert, ownership change, or adverse media hit.
- **Expected-Activity Baseline.** The documented set of anticipated transaction types, volumes, values, geographies, and counterparties that becomes the reference for monitoring.
- **Politically Exposed Person (PEP).** An individual entrusted with a prominent public function, their immediate family, and known close associates.
- **Source of Funds.** The origin of the funds used in a specific transaction or opening deposit.
- **Source of Wealth.** The origin of a customer's overall net worth and how it was accumulated.
- **CDD Owner.** The Head of Financial Crimes Operations, accountable for the design and operating effectiveness of CDD.

## 1. Risk-Based CDD Framework

### 1.1 Risk factors

The CRR is computed from weighted factors:

| Factor | Examples | Weight band |
|---|---|---|
| Customer type | Consumer, small business, cash-intensive business, money services business, trust | High influence |
| Geography | Customer location, counterparties in higher-risk jurisdictions | High influence |
| Product and service | Deposit only, wires, foreign exchange, remote deposit, trade finance | Moderate influence |
| Channel | In person, digital remote, intermediated | Moderate influence |
| Expected activity | Volume and value relative to stated purpose | Moderate influence |

### 1.1A Scoring method

1.1A.1 Each factor is scored on a 1-to-5 scale and multiplied by its weight. High-influence factors carry a weight of 3, moderate-influence factors a weight of 2. The weighted sum maps to a band using the thresholds below. The numeric model parameters are owned by Risk (MJD-RSK-0003); Operations applies the published version.

| Weighted score range | Customer Risk Rating |
|---|---|
| 0 to 24 | Low |
| 25 to 44 | Moderate |
| 45 and above | High |

1.1A.2 **Override rules.** Certain conditions force a minimum rating regardless of the weighted score: any PEP forces at least High; any money services business forces at least High; any sanctioned-adjacent geography forces at least High. A downward override below the computed band is not permitted; an upward override by Compliance is always permitted and documented.

1.1A.3 **Worked scoring example.** A domestic small business using deposits and occasional domestic wires scores customer type 2 (weight 3 = 6), geography 1 (weight 3 = 3), product 3 (weight 2 = 6), channel 2 (weight 2 = 4), expected activity 2 (weight 2 = 4), for a weighted total of 23, mapping to Low. Adding regular international wires to a higher-risk geography would raise geography and product scores, pushing the total above 25 into Moderate.

### 1.2 Rating bands

1.2.1 **Low.** Consumer or established small business with domestic, predictable, deposit-centric activity.

1.2.2 **Moderate.** Business customers using wires or foreign exchange, or consumers with cross-border activity.

1.2.3 **High.** Cash-intensive businesses, money services businesses, entities with complex or opaque ownership, politically exposed persons, or any customer with counterparties in higher-risk jurisdictions. A High rating mandates Enhanced Due Diligence under MJD-OPS-0003.

### 1.3 Rating governance

The risk model weights are owned by Risk (MJD-RSK-0003) and reviewed annually. Operations applies the model; Compliance audits the application.

### 1.4 Rating at onboarding versus refresh

1.4.1 At onboarding the rating is computed from stated expected activity. At each refresh the rating is recomputed from actual observed activity, which may raise or, after sustained clean history, lower the rating subject to the override rules.

1.4.2 A rating change is effective on the date the analyst records it and drives the next scheduled refresh date and the monitoring sensitivity in MJD-CMP-0004.

## 2. Nature and Purpose of the Relationship

### 2.1 Required understanding

At onboarding, staff document the expected purpose and activity: anticipated monthly deposit volume, anticipated wire activity (count and value), expected counterparties and geographies, source of funds for the opening deposit, and source of wealth for higher-rated customers.

### 2.2 Expected-activity baseline

The documented baseline becomes the reference profile for transaction monitoring (MJD-CMP-0004). A material deviation from the baseline is a trigger event under Section 4.

2.2.1 **Baseline elements captured.** Anticipated monthly deposit count and value, anticipated wire count and value (domestic and international separately), anticipated cash activity, expected counterparties by name or type, expected geographies, and the products that will be active.

2.2.2 **Material deviation defined.** A deviation is material when observed activity exceeds 150 percent of the baseline value for a category over a calendar month, when a new transaction type not in the baseline appears at material value, or when a new high-risk geography appears. Material deviation is a trigger event under Section 4.2.

### 2.3 Source-of-funds expectations by rating

| Rating | Source-of-funds documentation |
|---|---|
| Low | Stated source recorded; no corroboration required for routine activity |
| Moderate | Stated source recorded; corroboration for opening deposits above 100,000 USD |
| High | Documented and corroborated source of funds, and source of wealth per MJD-OPS-0003 |

## 3. Beneficial Ownership

### 3.1 Collection and certification

For each legal-entity customer, the bank collects beneficial-ownership information and obtains a signed certification from the individual opening the account. The bank identifies each owner of 25 percent or more (ownership prong) and one controlling individual (control prong).

3.1.1 **Certification contents.** The certifying individual attests to the accuracy of each beneficial owner's name, date of birth, address, and identification number, and identifies one individual under the control prong. The certification is retained in the CDD record and re-obtained on any ownership change.

3.1.2 **Excluded entity types.** Certain entity types are excluded from beneficial-ownership collection under the CDD Rule, such as banks, publicly traded companies registered with the SEC, and government entities. Exclusions are documented with the basis.

### 3.2 Verification

The identity of each natural-person beneficial owner is verified using the documentary and non-documentary methods in MJD-OPS-0001 Section 2. Verification of beneficial-owner identity is required before the entity account may transact.

### 3.3 Layered ownership

Where ownership is held through intermediate entities, staff trace ownership to the natural persons. Ownership structures that cannot be reasonably traced are escalated to Enhanced Due Diligence (MJD-OPS-0003) and may warrant a SAR referral.

3.3.1 **Tracing procedure.** For each intermediate entity, obtain its ownership register and repeat the 25 percent ownership test at each layer until natural persons holding 25 percent or more of the ultimate beneficial interest are identified. Document the ownership chain.

3.3.2 **Opacity handling.** If any layer cannot be reasonably traced after documented effort, the relationship is referred to EDD. If opacity appears designed to conceal ownership, refer to Compliance for SAR evaluation under MJD-CMP-0002.

## 3A. Customer-Type-Specific CDD

### 3A.1 Cash-intensive businesses

A cash-intensive business (for example, a convenience store, restaurant, or car wash) requires documented expected cash volume, the business's licenses, and a stated rationale for the cash levels. Observed cash above 125 percent of the stated expectation over a calendar month is a trigger event.

### 3A.2 Money services businesses

A money services business requires evidence of FinCEN registration, applicable state licensing, and the MSB's own AML program attestation. MSBs are rated at least High and are subject to EDD under MJD-OPS-0003.

### 3A.3 Trusts and fiduciary accounts

For a trust account, identify and verify the trustee and the natural persons who are settlors and beneficiaries to the extent required, and obtain the trust instrument or a certification of trust. Complex or foreign trusts are referred to EDD.

### 3A.4 Nonresident and foreign customers

A foreign customer requires a verified foreign identifier, a documented purpose for a US relationship, and heightened geography scoring. A counterparty or owner in a high-risk jurisdiction forces at least High rating.

## 4. Ongoing Monitoring and Refresh

### 4.1 Scheduled refresh cadence

The customer profile is refreshed on a risk-based cadence:

| Risk rating | Periodic refresh cadence |
|---|---|
| Low | Every 36 months |
| Moderate | Every 24 months |
| High | Every 12 months |

### 4.2 Trigger-based refresh

A refresh is performed within 30 calendar days of any trigger event: a transaction-monitoring alert that is not cleared as a false positive, a change in beneficial ownership, adverse media or sanctions-list developments, or a sustained deviation from the expected-activity baseline.

### 4.3 Refresh content

A refresh re-validates identity currency, re-confirms beneficial ownership, re-evaluates the nature and purpose, and recomputes the CRR. A rating increase to High invokes MJD-OPS-0003.

### 4.4 Refresh service levels and aging

| Refresh type | Target completion | Aging escalation |
|---|---|---|
| Scheduled Low | Within 30 days of due date | Supervisor at 30 days overdue |
| Scheduled Moderate | Within 20 days of due date | Supervisor at 20 days overdue |
| Scheduled High | Within 10 days of due date | Compliance at 10 days overdue |
| Trigger-based | Within 30 days of trigger | Compliance at 30 days |

4.4.1 An overdue High refresh that reaches 30 days past due restricts new outbound activity on the account pending completion, with Compliance notification.

### 4.5 Ongoing monitoring integration

4.5.1 The expected-activity baseline feeds the transaction-monitoring rules in MJD-CMP-0004. An alert that is not cleared as a false positive is a trigger event.

4.5.2 Adverse-media and sanctions-list developments are screened continuously per MJD-OPS-0008; a hit is a trigger event and may require EDD.

### 4.6 Trigger-event catalog

The following events are recognized triggers requiring a refresh within the Section 4.4 service levels:

| Trigger | Source | Refresh action |
|---|---|---|
| Uncleared monitoring alert | MJD-CMP-0004 | Recompute rating, review baseline |
| Beneficial-ownership change | Customer notice or filing | Re-collect and re-verify ownership |
| Adverse media or sanctions development | MJD-OPS-0008, screening vendor | Reassess risk, consider EDD |
| Material deviation from baseline | Monitoring, analyst observation | Update baseline, recompute rating |
| Product or geography expansion | Account activity | Rescore product and geography factors |
| Regulatory or examiner feedback | Compliance | Targeted reassessment |

4.6.1 Every trigger event and its resolution is recorded in the CDD record with dates, the analyst, and the resulting rating, forming the dated history required in Section 5.1.

## 5. Documentation and Quality Control

### 5.1 Record contents

Each CDD record contains the CRR and its computation inputs, the documented nature and purpose, beneficial-ownership data and certification, and a dated history of refreshes and trigger events.

### 5.2 Quality control sampling

Compliance samples at least 5 percent of new Moderate and High relationships monthly for CDD completeness. Findings feed the control-issue process in MJD-RSK-0003.

5.2.1 **Sampling tests.** CRR computation correctness, completeness of nature-and-purpose documentation, beneficial-ownership certification and verification, source-of-funds documentation at the level required by rating, and timeliness of refreshes.

5.2.2 **Defect handling.** A sampling defect is logged, remediated within 10 business days, and trended; a defect rate above 3 percent in any month triggers a root-cause review by the Head of Financial Crimes Operations.

### 5.3 Retention

CDD records are retained for five years after account closure per MJD-CMP-0008.

### 5.4 Metrics

| Metric | Target |
|---|---|
| Onboarding CDD completed before activation | 100 percent |
| Scheduled refreshes completed within SLA | >= 95 percent |
| Trigger refreshes completed within 30 days | >= 98 percent |
| QC defect rate | <= 3 percent |
| High-rating relationships with current EDD | 100 percent |

## 6. Worked End-to-End Example

6.1 A regional import business opens a business checking account. At onboarding the analyst records expected activity of 40 monthly deposits totaling 800,000 USD, 8 monthly international wires totaling 600,000 USD to two named suppliers in moderate-risk geographies, and minimal cash. The weighted score lands in Moderate. Beneficial ownership resolves to two natural persons each holding 50 percent; both are verified and certified. Source of funds for the opening deposit is corroborated because it exceeds 100,000 USD.

6.2 Three months later, transaction monitoring (MJD-CMP-0004) alerts on wires to a third counterparty in a high-risk jurisdiction totaling 1,200,000 USD in one month, well above the baseline. The alert is not a false positive, so it is a trigger event. The trigger refresh recomputes geography scoring, the rating moves to High, and the relationship is referred to EDD under MJD-OPS-0003. Source of wealth is now required and corroborated, senior approval is obtained, and monitoring sensitivity is raised.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Operations Analyst | Apply the risk model, document nature and purpose, collect and verify beneficial ownership, execute scheduled and trigger refreshes |
| Compliance Officer | Own the standard, perform QC sampling, adjudicate escalations, confirm High ratings and EDD referrals |
| Risk Analyst | Own and tune the risk-rating model weights, validate model performance, consume CRR data for enterprise risk reporting |
| Head of Financial Crimes Operations | Own this standard, report CDD metrics, approve exceptions |

## Exceptions and Escalation

- A relationship that cannot meet a CDD requirement (for example, beneficial ownership that cannot be traced) is escalated to Compliance and either subjected to EDD or exited.
- An exception to a refresh deadline requires Compliance Officer approval and is capped at 30 additional days.
- Any indication of structuring, layering, or evasion is escalated immediately under MJD-CMP-0002.
- A downward CRR override below the computed band is never permitted; only Compliance may override upward.
- The beneficial-ownership certification and verification are non-waivable for non-excluded entities; an entity that will not certify is not onboarded.

### Escalation ladder

| Trigger | First escalation | Second escalation |
|---|---|---|
| Untraceable beneficial ownership | Compliance Officer | EDD or exit decision |
| Overdue High refresh (30 days) | Compliance Officer | Account restriction |
| Structuring or layering indicators | Compliance (MJD-CMP-0002) | BSA Officer |
| Model performance concern | Risk Analyst (MJD-RSK-0003) | Head of Financial Crimes Operations |

## Related Documents

- MJD-OPS-0001 Customer Identification Program (CIP) Procedure
- MJD-OPS-0003 Enhanced Due Diligence (EDD) Procedure
- MJD-OPS-0008 Sanctions (OFAC) Screening Procedure
- MJD-CMP-0004 Transaction Monitoring Rules and Thresholds
- MJD-RSK-0003 Operational Risk Procedure
- MJD-CMP-0008 Records Retention Schedule

## Regulatory References

- FinCEN Customer Due Diligence Rule, 31 CFR 1010.230
- 31 CFR 1020.210 (AML program requirements for banks)
- FFIEC BSA/AML Examination Manual, Customer Due Diligence
- USA PATRIOT Act Section 326

## Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2018-08-01 | Head of Financial Crimes Operations | Initial CDD standard |
| 2.0.0 | 2020-05-15 | Head of Financial Crimes Operations | Implemented beneficial-ownership prongs per CDD Rule |
| 3.0.0 | 2023-02-20 | Head of Financial Crimes Operations | Risk-based refresh cadence table introduced |
| 3.1.0 | 2024-09-12 | Head of Financial Crimes Operations | Added trigger-based 30-day refresh requirement |
| 3.2.0 | 2025-10-15 | Head of Financial Crimes Operations | Clarified layered-ownership escalation to EDD |
