---
doc_id: MJD-RSK-0005
title: Stress Testing Framework (CCAR/DFAST)
department: RISK
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: Head of Stress Testing
allowed_roles: [RISK_ANALYST, FINANCE_CONTROLLER]
effective_date: 2026-02-10
version: 2.2.0
review_cycle_months: 12
regulatory_refs: ["12 CFR 252 (Regulation YY)", "Dodd-Frank Act Stress Test (DFAST)", "Comprehensive Capital Analysis and Review (CCAR)", "SR 15-18", "SR 15-19", "Basel III"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Stress Testing Framework (CCAR/DFAST)

## Purpose and Scope

This Stress Testing Framework establishes how Meridian John Doe Financial ("Meridian J.D." or the "Bank") designs, governs, executes, and reports enterprise capital stress testing in line with supervisory expectations for company-run and supervisory stress testing. It defines the stress testing frequency, the scenario set, the modeling and aggregation approach, the link to capital planning, and the controls that make the results credible to the Board and to examiners.

The Framework supports the Bank's compliance with the supervisory stress testing rules applicable to a Category III institution and with the company-run stress test requirements under the Dodd-Frank Act stress testing rules. It governs the projection of pre-provision net revenue, losses, the allowance, balance sheet and risk-weighted assets, and regulatory capital ratios over the projection horizon.

The Framework applies to every business line and material portfolio. It binds the stress testing team, model owners and validators, the finance function that produces the financial projections, risk analysts who run and aggregate results, and finance controllers who tie results to the capital plan and regulatory reporting.

## Definitions

**Scenario.** A coherent, internally consistent set of macroeconomic and financial variable paths used as stress test inputs.

**Baseline scenario.** The Bank's expected path of the economy used as the reference case.

**Adverse scenario.** A moderate recessionary path.

**Severely adverse scenario.** A severe, broad-based recession with sharp asset price declines, used as the binding stress case.

**Projection horizon.** The forward quarters over which results are projected; the Bank uses a nine-quarter horizon.

**Pre-Provision Net Revenue (PPNR).** Net interest income plus noninterest income less noninterest expense, before provisions.

**Stressed capital ratio.** A regulatory capital ratio projected under a stress scenario, including the post-stress minimum across the horizon.

**Reverse stress test.** An exercise that starts from a defined failure outcome and identifies the scenarios that would produce it.

## 1. Governance

### 1.1 Oversight

The Board Risk Committee approves this Framework and the stress testing results that support the capital plan. The Enterprise Risk Management Committee and a dedicated Stress Testing Steering Committee oversee execution. The Head of Stress Testing owns the Framework and reports through the CRO.

### 1.2 Independent review

Stress testing models are validated under the Model Risk Management Policy (MJD-RSK-0002) as Tier 1 models and receive a full independent validation every 12 months. The end-to-end stress testing process, including scenario design, model aggregation, and controls, is subject to independent review at least annually.

## 2. Stress Testing Frequency

### 2.1 Enterprise capital stress test

The Bank conducts a comprehensive enterprise capital stress test at least annually, aligned to the supervisory cycle. This annual exercise covers the full nine-quarter horizon under all approved scenarios and supports the annual capital plan.

### 2.2 Interim and event-driven stress tests

In addition to the annual exercise, the Bank conducts:

| Stress test | Frequency |
|---|---|
| Enterprise capital stress test (full) | Annual, at least once per calendar year |
| Internal interim capital stress test | Semi-annual |
| Liquidity stress test | Monthly |
| Reverse stress test | Annual |
| Ad hoc event-driven stress test | As triggered (see Section 2.3) |

### 2.3 Event-driven triggers

An ad hoc stress test is triggered by a material change in the macroeconomic outlook, a large idiosyncratic exposure event, a significant acquisition, or a regulatory request. The CRO may invoke an ad hoc test at any time.

## 3. Scenario Design

### 3.1 Scenario set

Each annual exercise uses at minimum three scenarios: a baseline, an adverse, and a severely adverse scenario. The Bank also designs at least one bank-specific scenario targeting its idiosyncratic vulnerabilities, such as its commercial real estate concentration.

### 3.2 Scenario variables

Scenarios specify paths for a consistent set of variables over the nine-quarter horizon, including real GDP growth, the unemployment rate, equity price indices, house and commercial property price indices, interest rates and the yield curve, credit spreads, and, where relevant, international variables. The severely adverse scenario is calibrated to a severe recession comparable in depth to historical severe downturns.

### 3.3 Scenario governance

Scenarios are proposed by the stress testing team, challenged by independent risk management, and approved by the Stress Testing Steering Committee before use. Scenario assumptions and rationale are documented for examiner review.

## 4. Modeling and Aggregation

### 4.1 Loss, revenue, and balance sheet projection

Credit losses are projected from stressed PD, LGD, and EAD parameters consistent with the Credit Risk Policy (MJD-RSK-0004). PPNR is projected from balance sheet, rate, and fee models. Operational losses are projected from the scenario analysis in the Operational Risk Procedure (MJD-RSK-0003). The allowance is projected under the expected credit loss methodology.

### 4.2 Capital projection

Projected net income after taxes and dividends flows to capital. Risk-weighted assets are projected under the Basel III standardized approach. The Bank projects each regulatory capital ratio over the horizon and identifies the post-stress minimum, which must remain above the minimums and buffers in the Capital Adequacy Standard (MJD-RSK-0006).

### 4.3 Aggregation controls

Results are aggregated through a controlled process with documented data lineage, reconciliation to the starting balance sheet and capital, and four-eyes review of every manual adjustment above USD 5 million. Aggregation tooling is under change control per the Change Management and Release Policy (MJD-TEC-0008).

## 5. Use of Results

### 5.1 Capital planning linkage

Stress test results are a primary input to the annual capital plan. The plan must demonstrate that the Bank maintains capital above regulatory minimums plus the stress capital buffer throughout the severely adverse scenario before any planned capital distributions.

### 5.2 Limit and risk appetite linkage

Where the severely adverse results show a binding constraint, management proposes risk-reducing actions, which may include tightening the concentration limits in the Credit Risk Policy (MJD-RSK-0004) or adjusting the enterprise risk appetite in the Enterprise Risk Management Framework (MJD-RSK-0001).

### 5.3 Worked capital-path example

The following illustrative nine-quarter severely adverse path shows how results are read. The starting CET1 ratio is 11.5 percent. Cumulative stressed losses and lower PPNR draw the ratio to a trough before recovery. The post-stress minimum, 8.3 percent in this illustration, is the figure compared against the requirement.

| Quarter | Q0 | Q2 | Q4 (trough) | Q6 | Q9 |
|---|---|---|---|---|---|
| CET1 ratio | 11.5% | 9.8% | 8.3% | 9.1% | 10.4% |
| Cumulative loss (USD B) | 0.0 | 2.1 | 4.6 | 5.8 | 6.4 |

Because the 8.3 percent trough exceeds the 7.0 percent effective regulatory requirement under the Capital Adequacy Standard (MJD-RSK-0006), the Bank passes with a 1.3 percentage point margin, which is the capacity available for planned distributions and the stress capital buffer calibration.

## 6. Liquidity Stress Testing

Liquidity stress testing runs monthly and is distinct from the capital stress test. It projects the net cumulative cash-flow gap under an idiosyncratic stress (a name-specific funding shock), a market-wide stress, and a combined scenario over horizons of overnight, 30 days, and 90 days. The 30-day combined scenario must be survivable using the high-quality liquid asset buffer consistent with a Liquidity Coverage Ratio at or above the 110 percent enterprise red threshold in the Enterprise Risk Management Framework (MJD-RSK-0001). A projected breach of the survival horizon triggers the contingency funding plan and escalation to the Asset Liability Committee.

## 7. Data, Controls, and Model Inventory for Stress Testing

### 7.1 Data integrity

Stress testing draws on a controlled data layer with documented lineage from source systems to the starting balance sheet. The starting position is reconciled to the regulatory reports filed under the Regulatory Reporting Procedure (MJD-FIN-0003). Data quality issues above a materiality threshold of USD 10 million in affected exposure are logged and resolved before results are finalized.

### 7.2 Model inventory and supporting models

Every model used in the exercise (loss projection, PPNR, balance sheet, allowance, and RWA models) is in the model inventory and validated under the Model Risk Management Policy (MJD-RSK-0002) as a Tier 1 model with annual full validation. A material modeling limitation is disclosed in the results with its estimated directional effect, so the Board understands the uncertainty around the headline ratio.

## 8. Reporting

The Head of Stress Testing reports the full results to the Stress Testing Steering Committee, the Enterprise Risk Management Committee, and the Board Risk Committee. The report includes scenario narratives, projected losses by portfolio, projected PPNR, the projected capital ratio path with the post-stress minimums, key assumptions and limitations, and reverse stress test findings. Results that feed regulatory submissions are coordinated with the Regulatory Reporting Procedure (MJD-FIN-0003).

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Board Risk Committee | Approve the Framework and the results supporting the capital plan |
| Stress Testing Steering Committee | Approve scenarios; oversee execution |
| Head of Stress Testing | Own the Framework; lead execution |
| Model owners and validators | Maintain and validate stress models per MJD-RSK-0002 |
| RISK_ANALYST | Run scenarios; aggregate results; prepare reporting |
| FINANCE_CONTROLLER | Produce financial projections; tie results to the capital plan and regulatory reporting |

## Exceptions and Escalation

Any deviation from this Framework, including use of an unapproved scenario or an aggregation control bypass, requires a documented exception approved by the Stress Testing Steering Committee with a compensating control. Use of an un-validated Tier 1 stress model in an official submission is prohibited and may not be granted by exception.

Escalation: a post-stress capital ratio that falls below the regulatory minimum plus buffer in any scenario is escalated to the CRO within 24 hours and to the Board Risk Committee, triggering the capital actions in the Capital Adequacy Standard (MJD-RSK-0006). A material modeling or data error discovered after submission is escalated immediately to the Head of Stress Testing and the CRO.

## Related Documents

- MJD-RSK-0001 Enterprise Risk Management Framework
- MJD-RSK-0002 Model Risk Management Policy (SR 11-7)
- MJD-RSK-0003 Operational Risk Procedure
- MJD-RSK-0004 Credit Risk Policy
- MJD-RSK-0006 Capital Adequacy Standard (Basel III)
- MJD-FIN-0003 Regulatory Reporting Procedure (Call Report / FR Y-9C)
- MJD-TEC-0008 Change Management and Release Policy

## Regulatory References

- 12 CFR 252 (Regulation YY), Enhanced Prudential Standards and Stress Testing
- Dodd-Frank Act Stress Test (DFAST) rules
- Comprehensive Capital Analysis and Review (CCAR)
- SR 15-18 and SR 15-19, Supervisory Expectations for Risk Management
- Basel III: A global regulatory framework for more resilient banks and banking systems

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-06-01 | Head of Stress Testing | Initial stress testing framework |
| 2.0.0 | 2024-02-01 | Head of Stress Testing | Added nine-quarter horizon and reverse stress testing |
| 2.2.0 | 2026-02-10 | Head of Stress Testing | Updated frequency table and capital linkage |
