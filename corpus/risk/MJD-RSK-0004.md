---
doc_id: MJD-RSK-0004
title: Credit Risk Policy
department: RISK
doc_type: POLICY
classification: CONFIDENTIAL
owner_role: Chief Credit Officer
allowed_roles: [RISK_ANALYST, FINANCE_CONTROLLER]
effective_date: 2026-01-25
version: 3.1.0
review_cycle_months: 12
regulatory_refs: ["Basel III", "12 CFR 217 (Regulation Q)", "ASC 326 (CECL)", "SR 11-7", "Interagency Guidelines for Real Estate Lending (12 CFR 34 Subpart D)"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Credit Risk Policy

## Purpose and Scope

This Credit Risk Policy establishes how Meridian John Doe Financial ("Meridian J.D." or the "Bank") governs the assumption, measurement, monitoring, and control of credit risk. It defines the credit risk appetite, the rating and approval framework, concentration limits, the expected credit loss methodology, and the credit risk reporting that feeds the enterprise risk profile under the Enterprise Risk Management Framework (MJD-RSK-0001).

Credit risk is the risk of loss arising from a borrower or counterparty failing to meet its obligations in accordance with agreed terms. The Policy covers wholesale and commercial lending, retail lending, counterparty credit risk in treasury and trading activity, and credit concentration risk. It binds credit officers, underwriters, portfolio managers, the independent credit risk review function, risk analysts who measure and report credit risk, and finance controllers who consume credit data for provisioning and regulatory reporting.

The Policy applies enterprise-wide to all on- and off-balance-sheet credit exposures, including loans, commitments, letters of credit, guarantees, and derivative counterparty exposures.

## Definitions

**Probability of Default (PD).** The likelihood that an obligor defaults within a one-year horizon.

**Loss Given Default (LGD).** The share of an exposure expected to be lost if default occurs, net of recoveries.

**Exposure at Default (EAD).** The expected amount outstanding at the time of default, including undrawn commitments expected to be drawn.

**Expected Credit Loss (ECL).** The probability-weighted estimate of credit losses over the relevant horizon, computed under the current expected credit loss methodology.

**Allowance for Credit Losses (ACL).** The balance-sheet reserve established to absorb expected credit losses.

**Risk rating.** The internal grade assigned to an obligor and facility reflecting credit quality.

**Concentration.** An exposure or group of related exposures large enough that its deterioration could materially affect the Bank.

**Nonperforming.** A loan on which principal or interest is 90 days or more past due, or otherwise placed on nonaccrual.

## 1. Credit Risk Appetite

The Bank's credit risk appetite is expressed through portfolio-level limits, single-name and sector concentration limits, and minimum portfolio credit quality. The appetite metrics roll up to the enterprise credit metrics in the Enterprise Risk Management Framework (MJD-RSK-0001). Lending outside approved products, geographies, or risk grades is prohibited absent an approved exception.

## 2. Credit Risk Rating

### 2.1 Dual rating

Every wholesale obligor receives an obligor risk rating mapped to a PD, and every facility receives a facility risk rating reflecting LGD given collateral and structure. Retail exposures are rated using approved scoring models governed by the Model Risk Management Policy (MJD-RSK-0002).

### 2.2 Rating scale

| Grade | Description | Indicative one-year PD |
|---|---|---|
| 1 to 3 | Strong | <= 0.25% |
| 4 to 6 | Satisfactory | 0.25% to 2.0% |
| 7 | Special mention | 2.0% to 8.0% |
| 8 | Substandard | 8.0% to 25% |
| 9 | Doubtful | 25% to 75% |
| 10 | Loss | > 75% |

### 2.3 Rating review

Ratings are reviewed at least annually for all exposures, semi-annually for exposures above USD 10 million, and immediately upon a material adverse change. Grades 7 and worse are reviewed quarterly by the credit risk review function.

## 3. Credit Approval Authority

### 3.1 Approval matrix

Credit is approved within delegated authority based on aggregate obligor exposure and risk grade. Exposures above the highest delegated level require Credit Risk Committee approval.

| Aggregate obligor exposure | Approval authority |
|---|---|
| Up to USD 5 million | Senior underwriter |
| USD 5 million to USD 25 million | Credit officer and division credit head (dual) |
| USD 25 million to USD 100 million | Chief Credit Officer and one Credit Risk Committee member |
| Above USD 100 million | Credit Risk Committee |

### 3.2 Independence

Credit approval is independent of loan production. No individual may both originate and grant final approval on the same credit.

## 4. Concentration Limits

### 4.1 Single-name limit

Aggregate exposure to a single obligor or group of connected obligors is limited to 15 percent of the Bank's Tier 1 capital. Exposures between 10 and 15 percent are reported to the Credit Risk Committee monthly. This single-name limit is consistent with the enterprise concentration appetite in the Enterprise Risk Management Framework (MJD-RSK-0001) and with the legal lending limit constraints.

### 4.2 Sector and product limits

| Concentration dimension | Limit (% of total credit exposure) |
|---|---|
| Commercial real estate | <= 30% |
| Single industry sector | <= 20% |
| Leveraged lending | <= 10% |
| Single geographic region | <= 25% |

Breaches require a remediation plan approved by the Credit Risk Committee within 30 days.

## 5. Expected Credit Losses and Allowance

### 5.1 Methodology

The Bank estimates expected credit losses under the current expected credit loss methodology using PD, LGD, and EAD parameters, reasonable and supportable forecasts, and a reversion to historical averages beyond the forecast horizon. The ECL models are governed by the Model Risk Management Policy (MJD-RSK-0002) and are Tier 1 models subject to annual independent validation.

### 5.2 Allowance governance

The Allowance for Credit Losses is reviewed quarterly by a cross-functional committee including credit risk and finance. The allowance and its drivers are reconciled to the general ledger and disclosed in regulatory reporting per the Regulatory Reporting Procedure (MJD-FIN-0003). Qualitative adjustments above USD 5 million require documented Chief Credit Officer and Finance Controller sign-off.

## 6. Problem Asset Management

### 6.1 Nonaccrual

A loan is placed on nonaccrual when principal or interest is 90 days or more past due, or when full collection of principal and interest is in doubt, whichever is earlier. Accrued but uncollected interest is reversed.

### 6.2 Charge-off

A loan, or the uncollectible portion, is charged off no later than when it is classified Loss (grade 10), and for retail unsecured exposures no later than 120 days past due. Charge-offs feed the operational loss and ECL processes.

## 7. Underwriting Standards

### 7.1 Wholesale underwriting

Wholesale credit decisions are based on repayment capacity, not collateral alone. Underwriting documents the source of repayment, a cash-flow analysis with a minimum debt-service coverage ratio of 1.25 times for income-producing real estate and 1.20 times for general commercial credit, a sensitivity analysis under rising rates and revenue stress, the borrower's leverage, and the quality and lien position of collateral. Exceptions to a minimum coverage or leverage standard are tracked as policy exceptions in Section Exceptions and Escalation.

### 7.2 Collateral and loan-to-value

Secured exposures observe maximum loan-to-value limits at origination. The limits below apply at origination; ongoing monitoring revalues collateral for exposures above USD 5 million at least annually.

| Collateral type | Maximum loan-to-value |
|---|---|
| Owner-occupied residential | 90% |
| Investment residential | 80% |
| Commercial real estate (income producing) | 75% |
| Construction and land | 65% |
| Marketable securities | 70% |

### 7.3 Covenants

Material wholesale facilities include financial covenants (for example leverage and coverage ratios) tested at least quarterly. A covenant breach triggers a watch-list review within 15 business days and a rating reassessment under Section 2.3.

## 8. Counterparty Credit Risk

Counterparty credit risk on derivatives and securities financing is measured under the standardized approach for counterparty credit risk and limited by counterparty under the single-name framework in Section 4.1. Exposure is mitigated through netting agreements, daily variation margin, and initial margin for non-centrally-cleared derivatives. Wrong-way risk, where exposure rises as the counterparty's credit quality falls, is identified and assigned a conservative add-on. Counterparty limits are monitored daily and breaches are escalated to the Credit Risk Committee.

## 9. Portfolio Management and Watch List

### 9.1 Watch list

Obligors rated grade 7 (special mention) and worse, and any obligor with a covenant breach or material adverse change, are placed on the watch list. The watch list is reviewed monthly by the Credit Risk Committee with a written action plan per name covering strategy, expected loss, and timeline.

### 9.2 Risk-based pricing

Credit is priced to cover the expected loss (PD times LGD times EAD), the cost of capital allocated to the exposure, and the cost of funds and servicing. A facility priced below its risk-based floor requires documented Chief Credit Officer approval, preventing the silent accumulation of under-priced risk.

## 10. Stress Testing of the Credit Portfolio

The credit portfolio is stress tested under the enterprise scenarios in the Stress Testing Framework (MJD-RSK-0005). Stressed PD and LGD parameters produce projected losses that inform the allowance, capital planning, and the single-name and sector limits in Section 4. A worked illustration: a commercial real estate sub-portfolio of USD 4.0 billion with a through-the-cycle expected loss rate of 0.40 percent contributes USD 16 million of expected loss in baseline; under the severely adverse scenario the stressed loss rate of 3.5 percent contributes USD 140 million, which is tested against the 30 percent commercial real estate concentration limit and the capital buffers in the Capital Adequacy Standard (MJD-RSK-0006).

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Credit Risk Committee | Own credit appetite; approve large exposures and limit breaches |
| Chief Credit Officer | Own this Policy; lead the credit function |
| Underwriters and credit officers | Originate and assess credit within delegated authority |
| Credit risk review function | Independently review ratings and problem assets |
| RISK_ANALYST | Measure PD/LGD/EAD; monitor concentrations; report credit risk |
| FINANCE_CONTROLLER | Own the allowance reconciliation and regulatory credit disclosures |

## Exceptions and Escalation

Any exception to this Policy, including a concentration breach, an out-of-appetite grade, or a delegated-authority override, requires documented approval: single-name and sector breaches by the Credit Risk Committee; rating or product exceptions up to USD 25 million by the Chief Credit Officer. Every exception carries a compensating condition and an expiry not exceeding 12 months.

Escalation: a single-name exposure breach above 15 percent of Tier 1 capital, a sector limit breach, or a material rating migration is escalated to the Chief Credit Officer within two business days and to the Credit Risk Committee at its next meeting. A credit event that could threaten capital adequacy is escalated to the CRO within 24 hours under the Enterprise Risk Management Framework (MJD-RSK-0001).

## Related Documents

- MJD-RSK-0001 Enterprise Risk Management Framework
- MJD-RSK-0002 Model Risk Management Policy (SR 11-7)
- MJD-RSK-0005 Stress Testing Framework (CCAR/DFAST)
- MJD-RSK-0006 Capital Adequacy Standard (Basel III)
- MJD-FIN-0003 Regulatory Reporting Procedure (Call Report / FR Y-9C)

## Regulatory References

- Basel III: A global regulatory framework for more resilient banks and banking systems
- 12 CFR 217 (Regulation Q), Capital Adequacy of Bank Holding Companies
- ASC 326, Financial Instruments, Credit Losses (CECL)
- SR 11-7, Guidance on Model Risk Management
- Interagency Guidelines for Real Estate Lending, 12 CFR 34 Subpart D

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-03-01 | Chief Credit Officer | Initial credit risk policy |
| 2.0.0 | 2022-11-01 | Chief Credit Officer | Adopted CECL allowance methodology |
| 3.0.0 | 2025-04-01 | Chief Credit Officer | Recalibrated concentration limits to Tier 1 capital |
| 3.1.0 | 2026-01-25 | Chief Credit Officer | Updated approval matrix and rating review cadence |
