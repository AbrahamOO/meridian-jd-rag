---
doc_id: MJD-RSK-0006
title: Capital Adequacy Standard (Basel III)
department: RISK
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: Head of Capital Management
allowed_roles: [RISK_ANALYST, FINANCE_CONTROLLER]
effective_date: 2026-02-15
version: 2.0.0
review_cycle_months: 12
regulatory_refs: ["Basel III", "12 CFR 217 (Regulation Q)", "12 CFR 252 (Regulation YY)", "Basel III Leverage Ratio Framework", "SR 15-18"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Capital Adequacy Standard (Basel III)

## Purpose and Scope

This Capital Adequacy Standard establishes how Meridian John Doe Financial ("Meridian J.D." or the "Bank") measures, maintains, and manages regulatory capital to remain well capitalized under the Basel III capital framework as implemented in the U.S. capital rules. It defines the capital components, the binding minimum ratios and buffers, the management buffers the Bank holds above the minimums, the capital planning and contingency process, and the controls that ensure capital is measured and reported accurately.

The Standard applies to the consolidated Bank and to each regulated legal entity required to maintain capital. It governs the calculation of regulatory capital, risk-weighted assets under the standardized approach, the leverage exposure measure, and the supplementary leverage ratio. It binds the capital management function, risk analysts who compute and monitor ratios, and finance controllers who own the regulatory capital reporting.

This Standard is the authoritative source for the Bank's binding regulatory capital minimums. The enterprise risk appetite thresholds in the Enterprise Risk Management Framework (MJD-RSK-0001) sit at or above these minimums; where they differ, the more conservative figure governs.

## Definitions

**Common Equity Tier 1 (CET1) capital.** The highest quality regulatory capital, principally common stock and retained earnings, net of regulatory deductions.

**Additional Tier 1 (AT1) capital.** Qualifying instruments such as noncumulative perpetual preferred stock.

**Tier 1 capital.** CET1 plus AT1.

**Tier 2 capital.** Qualifying subordinated debt and a limited portion of the allowance.

**Total capital.** Tier 1 plus Tier 2.

**Risk-Weighted Assets (RWA).** On- and off-balance-sheet exposures weighted by regulatory risk weights under the standardized approach.

**Capital conservation buffer.** A CET1 buffer above the minimums; falling into it restricts capital distributions and discretionary bonus payments.

**Leverage ratio.** Tier 1 capital divided by average total consolidated assets.

**Supplementary Leverage Ratio (SLR).** Tier 1 capital divided by total leverage exposure, including certain off-balance-sheet items.

**Stress capital buffer.** A buffer set from supervisory stress test results that sits above the CET1 minimum.

## 1. Regulatory Capital Minimums

### 1.1 Binding minimum ratios

The Bank maintains, at all times, regulatory capital ratios at or above the following minimums plus the applicable capital conservation buffer. The base minimums under the standardized approach are:

| Ratio | Regulatory minimum | Plus capital conservation buffer | Effective requirement |
|---|---|---|---|
| Common Equity Tier 1 (CET1) | 4.5% | 2.5% | 7.0% |
| Tier 1 capital | 6.0% | 2.5% | 8.5% |
| Total capital | 8.0% | 2.5% | 10.5% |
| Tier 1 leverage ratio | 4.0% | not applicable | 4.0% |
| Supplementary leverage ratio | 3.0% | not applicable | 3.0% |

The 2.5 percent capital conservation buffer must be met with CET1 capital. Where a stress capital buffer applies from the supervisory stress test, it replaces the fixed 2.5 percent conservation buffer for the CET1, Tier 1, and total ratios and is never less than 2.5 percent.

### 1.2 Well-capitalized thresholds

To be considered well capitalized under the prompt corrective action framework, the Bank targets CET1 at or above 6.5 percent, Tier 1 at or above 8.0 percent, total capital at or above 10.0 percent, and a Tier 1 leverage ratio at or above 5.0 percent. The Bank manages to the higher of these thresholds and the buffered minimums in Section 1.1.

## 2. Management Buffers

The Bank holds management buffers above the effective regulatory requirements to absorb volatility and stress without breaching minimums. The internal operating targets, consistent with the enterprise risk appetite in the Enterprise Risk Management Framework (MJD-RSK-0001), are:

| Ratio | Effective regulatory requirement | Internal management target | Management buffer |
|---|---|---|---|
| CET1 | 7.0% | 11.0% | 4.0% |
| Tier 1 | 8.5% | 12.5% | 4.0% |
| Total capital | 10.5% | 14.5% | 4.0% |
| Tier 1 leverage | 4.0% | 6.0% | 2.0% |

A ratio falling below its internal management target but above the regulatory requirement is amber and triggers a management action plan. A ratio approaching the regulatory requirement is red and triggers the contingency capital plan in Section 4.

## 3. Capital Calculation

### 3.1 Numerator (capital)

CET1 is computed as qualifying common equity and retained earnings less regulatory deductions, including goodwill, certain deferred tax assets, and other prescribed items. AT1 and Tier 2 instruments are included only to the extent they meet the qualifying criteria and the recognition limits.

### 3.2 Denominator (RWA)

Risk-weighted assets are computed under the standardized approach. Each exposure category receives a prescribed risk weight; for example, qualifying residential mortgages, corporate exposures, and past-due exposures carry their respective standardized weights, and off-balance-sheet items are converted using the applicable credit conversion factors before weighting. Counterparty credit exposure on derivatives is measured under the standardized approach for counterparty credit risk.

### 3.3 Calculation controls

The capital calculation is reconciled to the general ledger and to regulatory reporting each quarter. Manual adjustments above USD 5 million require documented sign-off by the Head of Capital Management and the Finance Controller. The calculation tooling is under change control per the Change Management and Release Policy (MJD-TEC-0008), and any capital model is validated under the Model Risk Management Policy (MJD-RSK-0002).

## 4. Capital Planning and Contingency

### 4.1 Capital plan

The Bank produces an annual capital plan supported by the enterprise stress test in the Stress Testing Framework (MJD-RSK-0005). The plan must show that all ratios remain above the regulatory requirement plus the stress capital buffer throughout the severely adverse scenario before any planned distributions.

### 4.2 Contingency capital plan

The contingency capital plan defines actions by escalating trigger: at the amber level, restrict discretionary distributions and review risk-weighted asset growth; at the red level, suspend distributions, reduce risk-weighted assets, and prepare capital-raising options. Each action has an owner and an execution timeline.

### 4.3 Capital distribution governance

No dividend, share repurchase, or other capital distribution is executed unless the Bank projects remaining above the regulatory requirement plus the stress capital buffer for every ratio across the full stress horizon after the distribution. The maximum payout is constrained by the capital conservation buffer payout-restriction schedule: as the buffer is consumed, the permitted payout ratio falls in steps, reaching zero permitted payout when the buffer is fully depleted. Distributions are approved by the Board on the recommendation of the Asset Liability Committee and the CRO.

| Buffer remaining (of 2.5% conservation buffer) | Maximum payout ratio of eligible retained income |
|---|---|
| Greater than 1.875% (top quartile) | 100% |
| 1.25% to 1.875% | 60% |
| 0.625% to 1.25% | 40% |
| 0% to 0.625% (bottom quartile) | 20% |
| Buffer fully depleted | 0% |

## 5. Capital Composition and Quality

### 5.1 Composition targets

The Bank maintains the predominant share of its capital in CET1, the highest-quality component. Internal composition targets require CET1 to represent at least 80 percent of Tier 1 capital and Tier 2 instruments to represent no more than 25 percent of total capital, so the Bank is not reliant on lower-quality or maturing instruments to meet its ratios.

### 5.2 Instrument maturity and refinancing

AT1 and Tier 2 instruments approaching their final five years to maturity amortize out of regulatory capital recognition on the prescribed schedule for Tier 2. The Head of Capital Management maintains a maturity ladder and a refinancing plan so that no ratio falls below its internal management target due to a foreseeable instrument roll-off.

### 5.3 Pillar 2 and internal capital adequacy

Beyond the Pillar 1 minimums, the Bank performs an internal capital adequacy assessment that allocates capital to risks not fully captured by the standardized RWA, including interest-rate risk in the banking book, concentration risk beyond the single-name limit in the Credit Risk Policy (MJD-RSK-0004), and model risk. The internal assessment is a primary input to the management buffer calibration in Section 2.

## 6. Monitoring and Reporting

Capital ratios are computed at least monthly and reported to the Asset Liability Committee and the Enterprise Risk Management Committee monthly and to the Board Risk Committee quarterly. Regulatory capital is reported externally on the schedule in the Regulatory Reporting Procedure (MJD-FIN-0003). Any actual or projected breach of a regulatory minimum is reported immediately. The capital report includes the ratio levels against both the regulatory requirement and the internal management targets, the RWA drivers quarter over quarter, the buffer-consumption position from Section 4.3, and the maturity ladder from Section 5.2.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Board Risk Committee | Approve the capital plan; oversee capital adequacy |
| Asset Liability Committee | Review capital ratios and management buffers monthly |
| Head of Capital Management | Own this Standard; manage capital to targets |
| RISK_ANALYST | Compute and monitor ratios; analyze RWA drivers |
| FINANCE_CONTROLLER | Own capital calculation reconciliation and regulatory reporting |

## Exceptions and Escalation

No exception may permit the Bank to operate below a binding regulatory minimum plus its applicable buffer. A planned, temporary operation below an internal management target requires documented approval by the Head of Capital Management and the CRO with a remediation timeline. Any methodology deviation requires Board Risk Committee approval.

Escalation: a ratio at the red level, an actual breach of a regulatory minimum, or a projected post-stress breach is escalated to the CRO within 24 hours and to the Board Risk Committee immediately, invoking the contingency capital plan in Section 4 and the stress escalation in the Stress Testing Framework (MJD-RSK-0005).

## Related Documents

- MJD-RSK-0001 Enterprise Risk Management Framework
- MJD-RSK-0002 Model Risk Management Policy (SR 11-7)
- MJD-RSK-0004 Credit Risk Policy
- MJD-RSK-0005 Stress Testing Framework (CCAR/DFAST)
- MJD-FIN-0003 Regulatory Reporting Procedure (Call Report / FR Y-9C)
- MJD-TEC-0008 Change Management and Release Policy

## Regulatory References

- Basel III: A global regulatory framework for more resilient banks and banking systems
- 12 CFR 217 (Regulation Q), Capital Adequacy
- 12 CFR 252 (Regulation YY), Enhanced Prudential Standards
- Basel III Leverage Ratio Framework and Disclosure Requirements
- SR 15-18, Supervisory Expectations for Risk Management

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-07-01 | Head of Capital Management | Initial capital adequacy standard |
| 1.5.0 | 2024-05-01 | Head of Capital Management | Added supplementary leverage ratio and stress capital buffer |
| 2.0.0 | 2026-02-15 | Head of Capital Management | Updated management buffers and contingency triggers |
