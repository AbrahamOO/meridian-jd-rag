---
doc_id: MJD-RSK-0001
title: Enterprise Risk Management Framework
department: RISK
doc_type: POLICY
classification: CONFIDENTIAL
owner_role: Chief Risk Officer
allowed_roles: [RISK_ANALYST, COMPLIANCE_OFFICER, FINANCE_CONTROLLER, SECURITY_ARCHITECT]
effective_date: 2026-01-15
version: 4.2.0
review_cycle_months: 12
regulatory_refs: ["12 CFR 252 (Regulation YY)", "OCC Heightened Standards (12 CFR 30 Appendix D)", "Basel III", "COSO ERM 2017", "SR 11-7", "SR 15-18"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Enterprise Risk Management Framework

## Purpose and Scope

This Enterprise Risk Management Framework (the "Framework") establishes how Meridian John Doe Financial ("Meridian J.D." or the "Bank") identifies, measures, monitors, controls, and reports risk across the enterprise. It defines the Bank's risk taxonomy, its risk appetite architecture, the three lines of defense operating model, the governance committees that own risk decisions, and the aggregation and escalation pathways that connect a single business-unit exposure to a board-level view.

The Framework applies to every legal entity, business line, branch, function, and material outsourced arrangement of the Bank. It governs all risk types in the enterprise taxonomy defined in Section 2, including credit, market, liquidity, operational, model, compliance, strategic, reputational, and information security risk. It binds every employee, contractor, and third party acting on the Bank's behalf. Where a more specific policy exists for a single risk type (for example the Model Risk Management Policy, the Credit Risk Policy, or the Capital Adequacy Standard), that policy operates as a child of this Framework and must not contradict it. Conflicts are resolved in favor of the more conservative control.

The Framework is calibrated to a bank with consolidated assets above the USD 100 billion threshold and is therefore written to the expectations applicable to a Category III institution under the tailoring rules, including annual supervisory and company-run stress testing, enterprise risk appetite reporting, and independent risk management with a direct reporting line to the board.

## Definitions

**Risk appetite.** The aggregate level and types of risk the Bank is willing to assume to achieve its strategic objectives, expressed through qualitative statements and quantitative limits.

**Risk tolerance.** The specific maximum level of risk the Bank is prepared to accept for an individual risk type or metric before management action is required.

**Risk capacity.** The maximum level of risk the Bank can absorb given its capital, liquidity, borrowing capacity, and operational ability before breaching regulatory or contractual constraints.

**Inherent risk.** The level of risk before the effect of controls.

**Residual risk.** The level of risk remaining after controls are applied.

**Key Risk Indicator (KRI).** A forward-looking metric used to signal a change in the level of a risk exposure.

**Three Lines of Defense.** The operating model under which the business owns and manages risk (first line), independent risk management and compliance set policy and challenge (second line), and internal audit provides independent assurance (third line).

**Material risk.** A risk that, individually or in aggregate, could threaten the Bank's solvency, liquidity, earnings stability, reputation, or its ability to operate as a going concern. The materiality screening threshold is a single-event potential loss of USD 25 million or a recurring annualized loss of USD 10 million.

**Risk-Weighted Assets (RWA).** Assets weighted according to risk per the Basel III standardized approach, the denominator of the Bank's capital ratios.

## 1. Risk Governance

### 1.1 Board of Directors

The Board holds ultimate responsibility for the Bank's risk profile. The Board approves the Framework at least annually, approves the enterprise risk appetite statement, and reviews aggregate risk reporting no less than quarterly.

#### 1.1.1 Board Risk Committee

The Board Risk Committee (BRC) is a standing committee of the Board chaired by an independent director with risk management experience. The BRC meets at least eight times per year. It approves material risk policies, reviews limit breaches rated High or Critical, and confirms that the independent risk management function has adequate stature, independence, and resources.

#### 1.1.2 Board Audit Committee

The Board Audit Committee oversees the third line of defense, approves the annual internal audit plan, and reviews the adequacy of the control environment. The Chief Audit Executive reports functionally to this committee.

### 1.2 Chief Risk Officer

The Chief Risk Officer (CRO) leads the independent risk management function, owns this Framework, and has an unfiltered reporting line to the BRC. The CRO may not also hold a revenue-generating role. The CRO has the authority to halt any activity that breaches risk appetite pending committee review.

### 1.3 Management Risk Committees

#### 1.3.1 Enterprise Risk Management Committee

The Enterprise Risk Management Committee (ERMC) is chaired by the CRO and meets monthly. It reviews the enterprise risk profile, aggregate limit utilization, emerging risks, and escalations from the subordinate committees listed below.

#### 1.3.2 Subordinate Committees

The following committees report into the ERMC and meet at least monthly:

| Committee | Primary risk types | Chair |
|---|---|---|
| Credit Risk Committee | Credit, concentration, counterparty | Chief Credit Officer |
| Asset Liability Committee (ALCO) | Market, interest-rate, liquidity | Treasurer |
| Operational Risk Committee | Operational, fraud, third-party | Head of Operational Risk |
| Model Risk Committee | Model | Head of Model Risk |
| Compliance Committee | Compliance, financial crime | Chief Compliance Officer |

## 2. Risk Taxonomy

The enterprise risk taxonomy is the single authoritative classification of risk used in all reporting and aggregation. Every exposure, issue, and loss event maps to exactly one Level 1 category and at least one Level 2 subcategory.

| Level 1 category | Representative Level 2 subcategories |
|---|---|
| Credit risk | Wholesale credit, retail credit, counterparty credit, concentration |
| Market risk | Interest-rate risk in the banking book, trading market risk, FX |
| Liquidity risk | Funding liquidity, intraday liquidity, contingent liquidity |
| Operational risk | Process failure, fraud, technology, third-party, legal |
| Model risk | Development error, implementation error, misuse |
| Compliance risk | BSA/AML, consumer protection, conduct, sanctions |
| Strategic risk | Business model, competitive, execution |
| Reputational risk | Customer, market, regulatory perception |
| Information security risk | Confidentiality, integrity, availability |

## 3. Risk Appetite

### 3.1 Architecture

The risk appetite architecture has three tiers. Tier 1 is the qualitative enterprise appetite statement approved by the Board. Tier 2 is a set of quantitative enterprise metrics with green, amber, and red thresholds. Tier 3 is the cascade of business-unit limits that sum to the enterprise metrics.

### 3.2 Enterprise quantitative metrics

The following enterprise metrics and thresholds are approved by the Board and reviewed quarterly. The amber threshold triggers heightened monitoring and a management action plan; the red threshold triggers mandatory escalation to the BRC and corrective action.

| Metric | Green | Amber | Red (limit) |
|---|---|---|---|
| Common Equity Tier 1 ratio | >= 11.0% | 10.0% to 11.0% | < 10.0% |
| Total capital ratio | >= 14.5% | 13.0% to 14.5% | < 13.0% |
| Liquidity Coverage Ratio | >= 120% | 110% to 120% | < 110% |
| Net Stable Funding Ratio | >= 110% | 105% to 110% | < 105% |
| Single-name credit concentration | <= 10% of Tier 1 | 10% to 15% | > 15% |
| Annualized operational loss | <= USD 60M | USD 60M to 90M | > USD 90M |
| Material model overrides per quarter | <= 5 | 6 to 10 | > 10 |

The capital and liquidity thresholds in this table are the enterprise risk appetite expression. The binding regulatory minimums and the management buffers that sit above them are defined in the Capital Adequacy Standard (MJD-RSK-0006). Where the two differ, the more conservative figure governs.

### 3.3 Limit cascade and utilization

Each Tier 2 metric is decomposed into Tier 3 business-unit limits. Limit utilization is calculated daily for market and liquidity limits and monthly for credit, operational, and model limits. Utilization above 85 percent of any limit is reported as amber to the owning committee within two business days.

## 4. Three Lines of Defense

### 4.1 First line

Business and operational units own the risks they generate. They implement controls, self-identify issues, and remediate within agreed timelines. First-line risk officers embedded in each business attest quarterly that controls are operating.

### 4.2 Second line

Independent risk management and compliance set policy, define methodologies, set and monitor limits, perform independent challenge, and aggregate the enterprise risk profile. The second line owns this Framework and the risk taxonomy. The second line has the authority to escalate over the first line directly to the ERMC and BRC.

### 4.3 Third line

Internal audit independently assures the design and operating effectiveness of governance, risk management, and controls across both other lines. Audit does not own controls and does not perform first or second line activities.

## 5. Risk Identification and Assessment

### 5.1 Risk and Control Self-Assessment

Each business unit performs a Risk and Control Self-Assessment (RCSA) at least annually and after any material change. The RCSA rates inherent risk, documents controls, and rates residual risk on the five-by-five matrix in Section 5.2.

### 5.2 Risk rating matrix

Risk is rated by combining likelihood and impact. Impact bands are calibrated to the materiality screening threshold in Section 2 of the Definitions.

| Likelihood \ Impact | Insignificant (< USD 1M) | Minor (USD 1M to 10M) | Moderate (USD 10M to 25M) | Major (USD 25M to 100M) | Severe (> USD 100M) |
|---|---|---|---|---|---|
| Almost certain | Medium | High | High | Critical | Critical |
| Likely | Medium | Medium | High | High | Critical |
| Possible | Low | Medium | Medium | High | Critical |
| Unlikely | Low | Low | Medium | High | High |
| Rare | Low | Low | Medium | Medium | High |

### 5.3 Emerging risk process

The ERMC maintains an emerging risk register reviewed monthly. An emerging risk is a developing exposure with high uncertainty and potential enterprise impact that is not yet captured in existing limits. Each entry has an owner, a leading indicator, and a trigger for promotion into the standard taxonomy.

## 6. Risk Monitoring and Reporting

### 6.1 Enterprise risk report

The CRO presents the Enterprise Risk Report to the ERMC monthly and to the BRC quarterly. It includes the risk appetite dashboard, limit utilization, top enterprise risks, material issues and their remediation status, loss events above USD 1 million, and stress testing results.

### 6.2 Key Risk Indicators

Each risk type maintains a set of KRIs with defined thresholds. A KRI breach is logged in the governance, risk, and compliance system within one business day and reported to the owning committee at its next meeting, or immediately if rated Critical.

### 6.3 Risk data aggregation

Risk data aggregation follows the principles for effective risk data aggregation and risk reporting. Data lineage is documented from source system to report, and the Bank reconciles risk and finance figures monthly. Manual adjustments above USD 5 million require documented sign-off by the Head of Risk Reporting.

## 7. Stress Testing and Capital Linkage

The Framework requires forward-looking stress testing as a core risk management tool. Company-run enterprise stress tests are conducted at least annually under the supervisory severely adverse, supervisory adverse, and a Bank-specific baseline scenario, with the detailed methodology, scenario design, and governance defined in the Stress Testing Framework (MJD-RSK-0005). Stress results feed the capital and liquidity adequacy assessments and inform the setting of management buffers in the Capital Adequacy Standard (MJD-RSK-0006).

## 8. Issue and Remediation Management

Risk issues are logged centrally with a severity rating, an accountable owner, and a target remediation date. Remediation timelines by severity are: Critical within 30 days, High within 90 days, Medium within 180 days, and Low within 365 days. Past-due Critical and High issues are escalated to the ERMC monthly until closed. Closure requires second-line validation that the control is designed and operating effectively.

### 8.1 Issue intake and triage

Issues enter the central register from RCSAs, KRI breaches, loss events, internal audit, independent validation, examiner findings, and self-identification. Within five business days of intake the second line assigns a provisional severity using the rating matrix in Section 5.2, names an accountable first-line owner, and records the affected control and risk taxonomy node. Self-identified issues are tracked separately and reported to the ERMC as a positive indicator of control culture; a sustained decline in self-identification relative to audit-identified issues is itself treated as a control-environment KRI.

### 8.2 Remediation plan standard

Every High and Critical issue carries a written remediation plan with discrete milestones, a root-cause statement, the target control end-state, and an interim compensating control where residual risk exceeds appetite during remediation. Milestone slippage of more than 15 business days requires a revised plan approved one level above the issue owner. A second extension on the same issue escalates to the ERMC regardless of severity.

### 8.3 Thematic and aggregate analysis

The second line performs quarterly thematic analysis across the issue population to detect systemic weakness that individual issues understate. Themes are rated on the same five-by-five matrix at the aggregate level; a theme can be rated Critical even when each constituent issue is only Medium. Thematic findings feed the emerging risk register in Section 5.3 and the annual Framework review.

## 9. Risk Culture and Conduct

### 9.1 Conduct expectations

A sound risk culture is a control in its own right. Every employee is accountable for operating within risk appetite, escalating concerns without fear of retaliation, and refusing to pursue results that breach limits. Compensation for risk-taking roles includes risk-adjusted measures and a malus and clawback provision for material risk or conduct failures.

### 9.2 Culture indicators

The Bank monitors leading culture indicators including the self-identification ratio in Section 8.1, the rate of overdue High and Critical issues, the proportion of limit breaches that were escalated before detection by the second line, employee survey results on speaking up, and the timeliness of mandatory risk training completion. Indicators are reported to the BRC annually.

## 10. Risk Appetite Calibration and Annual Review

### 10.1 Calibration method

Quantitative appetite thresholds are calibrated so that the green band represents the normal operating range, the amber band represents the zone where management action restores the metric without external impact, and the red band sits with sufficient margin above the regulatory minimum or risk capacity that corrective action remains feasible before a hard constraint binds. Capital and liquidity thresholds are calibrated against the severely adverse stress results from the Stress Testing Framework (MJD-RSK-0005) so the amber band is never breached by a one-in-ordinary-year shock alone.

### 10.2 Worked calibration example

Consider the Common Equity Tier 1 (CET1) appetite. The regulatory effective requirement including the conservation buffer is 7.0 percent under the Capital Adequacy Standard (MJD-RSK-0006). The severely adverse stress test draws CET1 down by an illustrative 3.0 percentage points peak to trough. To keep the post-stress minimum above 7.0 percent the pre-stress level must sit at or above 10.0 percent, which sets the red threshold. A management margin of 1.0 percentage point above red sets the amber boundary at 10.0 to 11.0 percent and the green band at 11.0 percent and above, matching the enterprise metric table in Section 3.2. This worked example shows how the stress result, the regulatory minimum, and the management margin jointly fix every band.

### 10.3 Annual review

The CRO leads an annual review of the Framework, the taxonomy, and every appetite threshold. The review incorporates the prior-year loss experience, stress results, emerging risks, examiner feedback, and material business strategy changes. The BRC approves the revised Framework before the start of the planning cycle.

## 11. Risk Data, Systems, and Independent Validation of the Framework

### 11.1 Authoritative data sources

Each risk metric has a single designated authoritative source system and a documented transformation path to the report. Where a metric is derived from multiple sources, the reconciliation rule and tolerance are documented and owned by the Head of Risk Reporting. Use of a non-authoritative source for any Board-level metric is an exception requiring CRO approval.

### 11.2 Internal audit coverage

Internal audit assesses the design and operating effectiveness of the Framework on a cycle not exceeding 18 months for the overall framework and annually for the highest-inherent-risk components, including risk appetite governance, limit monitoring, and risk data aggregation. Audit findings rated High or Critical against the Framework are reported to the Board Audit Committee and the BRC.

### 11.3 Regulatory engagement

The CRO coordinates the Bank's engagement with its supervisors on enterprise risk matters, ensures examiner findings are entered into the issue register, and confirms that supervisory expectations under the Enhanced Prudential Standards are reflected in this Framework and its child policies.

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Board of Directors | Approve the Framework and enterprise risk appetite; oversee the risk profile |
| Board Risk Committee | Approve material risk policies; review High and Critical breaches |
| Chief Risk Officer | Own the Framework; lead independent risk management; escalate to the BRC |
| Enterprise Risk Management Committee | Review the enterprise risk profile; own the taxonomy |
| First-line business heads | Own and manage their risks; remediate issues |
| Second-line risk and compliance | Set policy; challenge; aggregate and report |
| Internal audit | Independently assure the framework and controls |
| RISK_ANALYST | Maintain registers, KRIs, and limit utilization; prepare the Enterprise Risk Report |
| FINANCE_CONTROLLER | Reconcile risk and finance data; support capital and stress linkage |
| COMPLIANCE_OFFICER | Own compliance risk inputs and financial crime escalations |
| SECURITY_ARCHITECT | Own information security risk inputs into the taxonomy |

## Exceptions and Escalation

Any deviation from this Framework requires a documented exception. Exceptions are requested through the governance, risk, and compliance system, assessed by second-line risk management, and approved as follows: Low residual risk by the Head of Operational Risk; Medium by the CRO; High and Critical by the BRC. Every exception has an expiry date not exceeding 12 months and a compensating control. Exceptions are reviewed at each ERMC meeting.

Escalation follows the rating in Section 5.2. A Critical-rated risk, a red enterprise metric breach, or a material control failure is escalated to the CRO within 24 hours and to the BRC at its next meeting or sooner if the CRO judges the exposure to threaten solvency or liquidity. Suspected fraud or financial crime is escalated in parallel under the Fraud Risk Management Procedure (MJD-RSK-0007) and the relevant compliance procedures.

## Related Documents

- MJD-RSK-0002 Model Risk Management Policy (SR 11-7)
- MJD-RSK-0003 Operational Risk Procedure
- MJD-RSK-0004 Credit Risk Policy
- MJD-RSK-0005 Stress Testing Framework (CCAR/DFAST)
- MJD-RSK-0006 Capital Adequacy Standard (Basel III)
- MJD-RSK-0007 Fraud Risk Management Procedure
- MJD-FIN-0003 Regulatory Reporting Procedure (Call Report / FR Y-9C)
- MJD-SEC-0001 Information Security Policy (master)

## Regulatory References

- 12 CFR 252 (Regulation YY), Enhanced Prudential Standards
- OCC Heightened Standards, 12 CFR 30 Appendix D
- Basel III: A global regulatory framework for more resilient banks and banking systems
- COSO Enterprise Risk Management, Integrating with Strategy and Performance (2017)
- SR 11-7, Guidance on Model Risk Management
- SR 15-18, Federal Reserve Supervisory Expectations for Risk Management

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-02-01 | Chief Risk Officer | Initial framework |
| 2.0.0 | 2022-06-15 | Chief Risk Officer | Added three lines of defense operating model |
| 3.0.0 | 2024-03-10 | Chief Risk Officer | Introduced risk appetite tier architecture |
| 4.0.0 | 2025-09-01 | Chief Risk Officer | Recalibrated to Category III tailoring |
| 4.2.0 | 2026-01-15 | Chief Risk Officer | Updated enterprise metric thresholds and added emerging risk process |
