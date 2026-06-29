---
doc_id: MJD-RSK-0003
title: Operational Risk Procedure
department: RISK
doc_type: PROCEDURE
classification: CONFIDENTIAL
owner_role: Head of Operational Risk
allowed_roles: [RISK_ANALYST, OPERATIONS_ANALYST, COMPLIANCE_OFFICER]
effective_date: 2026-01-20
version: 2.4.0
review_cycle_months: 12
regulatory_refs: ["Basel III Standardised Approach for Operational Risk", "SR 11-7", "OCC Heightened Standards (12 CFR 30 Appendix D)", "FFIEC Outsourcing Guidance"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Operational Risk Procedure

## Purpose and Scope

This Operational Risk Procedure defines the step-by-step process by which Meridian John Doe Financial ("Meridian J.D." or the "Bank") identifies, assesses, monitors, captures, and reports operational risk. It operationalizes the operational risk requirements of the Enterprise Risk Management Framework (MJD-RSK-0001) and provides the concrete workflows that first-line and second-line staff follow day to day.

Operational risk is the risk of loss resulting from inadequate or failed internal processes, people, and systems, or from external events. The definition includes legal risk but excludes strategic and reputational risk. This Procedure covers the operational risk management tools used by the Bank: loss data collection, the Risk and Control Self-Assessment (RCSA), Key Risk Indicators (KRIs), scenario analysis, and third-party (outsourcing) risk management.

The Procedure applies to every business unit, operations team, and support function. It binds operations analysts who execute first-line controls and capture events, risk analysts who maintain the operational risk taxonomy and reporting, and compliance officers where an operational event has a regulatory dimension.

## Definitions

**Operational loss event.** An event arising from operational risk that results, or could result, in a financial loss, a near miss, or a gain.

**Gross loss.** The total financial impact of an event before recoveries.

**Net loss.** Gross loss less direct recoveries and insurance recoveries.

**Near miss.** An event that had the potential to cause a loss but did not, due to chance or control intervention.

**Loss event type.** The Basel-aligned Level 1 categories used to classify events (see Section 2.2).

**RCSA.** Risk and Control Self-Assessment, the structured first-line assessment of inherent risk, controls, and residual risk.

**Key Risk Indicator.** A metric that provides early warning of a change in operational risk exposure.

**Third party.** Any external entity that performs an activity on behalf of the Bank, including vendors, service providers, and affiliates.

## 1. Operational Loss Data Collection

### 1.1 Capture threshold and timing

All operational loss events with a gross impact at or above USD 5,000 must be captured. Events below this threshold are captured in aggregate monthly by business unit. Near misses with a potential gross impact at or above USD 100,000 must also be captured.

An event must be logged in the operational risk system within five business days of detection. The initial record may carry an estimated loss; the figure is updated as it is finalized.

### 1.2 Capture workflow

1. The discovering staff member notifies the first-line operational risk coordinator.
2. The coordinator creates an event record with date of occurrence, date of detection, business unit, description, estimated gross loss, and provisional loss event type.
3. Within ten business days the owner classifies the event using the taxonomy in Section 2.2, records root cause, and links affected controls.
4. The second-line operational risk team reviews the classification and reconciles material events to the general ledger with finance, consistent with the Account Reconciliation Procedure (MJD-FIN-0002).
5. The event is closed when the loss is finalized, recoveries are recorded, and the corrective action is logged.

### 1.3 Loss data quality

The operational loss data set is the foundation for capital and scenario analysis. Events at or above USD 1 million are independently corroborated against source documents. Quarterly, the second line reconciles total recorded operational losses to the general ledger and reports unexplained variances above USD 250,000 to the Operational Risk Committee.

## 2. Operational Risk Taxonomy

### 2.1 Causal categories

Each event is tagged with a primary cause: process, people, systems, or external event.

### 2.2 Loss event types

| Level 1 loss event type | Examples |
|---|---|
| Internal fraud | Unauthorized activity, theft by staff |
| External fraud | Account takeover, check fraud, cyber theft |
| Employment practices and workplace safety | Discrimination claims, workplace injury |
| Clients, products, and business practices | Suitability, fiduciary breaches, fair lending matters |
| Damage to physical assets | Natural disaster, vandalism |
| Business disruption and system failures | Outages, hardware and software failures |
| Execution, delivery, and process management | Transaction errors, data entry errors, vendor failure |

## 3. Risk and Control Self-Assessment

### 3.1 Frequency

Each business unit completes an RCSA at least annually and within 30 days of a material organizational, process, or system change. The RCSA uses the five-by-five rating matrix in the Enterprise Risk Management Framework (MJD-RSK-0001).

### 3.2 RCSA workflow

1. Identify the processes within scope and the inherent risks in each.
2. Rate inherent risk on likelihood and impact.
3. Document the controls mitigating each risk and rate control design and operating effectiveness.
4. Derive residual risk.
5. For any residual risk rated High or Critical, create a risk treatment plan with an owner and a due date.
6. The second line independently challenges the RCSA before it is finalized.

## 4. Key Risk Indicators

### 4.1 Thresholds and reporting

Each business unit maintains KRIs with green, amber, and red thresholds. Examples include failed-transaction rate, manual workaround volume, staff turnover in control functions, system downtime minutes, and aging of unreconciled items. An amber KRI is reported to the unit's management within two business days. A red KRI is escalated to the Operational Risk Committee at its next meeting, or immediately if the underlying exposure is rated Critical.

### 4.2 Sample KRI thresholds

| KRI | Green | Amber | Red |
|---|---|---|---|
| Failed wire transactions per 1,000 | <= 2 | 3 to 5 | > 5 |
| Aged unreconciled GL items > 30 days | <= 10 | 11 to 25 | > 25 |
| Critical system downtime per month | <= 10 min | 11 to 30 min | > 30 min |
| Privileged-access exceptions open | <= 3 | 4 to 8 | > 8 |

## 5. Scenario Analysis

The Bank performs operational risk scenario analysis at least annually for its most material exposures, including cyber incident, large-scale fraud, critical vendor failure, and major processing disruption. Each scenario estimates frequency and severity at multiple percentiles and feeds the operational risk capital estimate and the enterprise stress testing inputs used in the Stress Testing Framework (MJD-RSK-0005).

### 5.1 Scenario workshop process

Each scenario is developed in a structured workshop with the relevant first-line subject experts, facilitated by the second line. The workshop estimates a typical-loss frequency and severity and a tail (one-in-twenty-year and one-in-one-hundred-year) severity. Estimates are anchored to internal loss data where available and to external loss data and expert judgment for low-frequency high-severity events. The second line challenges anchoring bias and documents the rationale for every parameter.

### 5.2 Sample scenario library

| Scenario | Primary loss event type | Illustrative one-in-one-hundred-year gross severity |
|---|---|---|
| Major cyber incident with data exposure | External fraud, business disruption | USD 120M |
| Critical core-banking outage > 8 hours | Business disruption and system failures | USD 45M |
| Coordinated payment fraud ring | External fraud | USD 30M |
| Critical vendor insolvency | Execution, delivery, process management | USD 25M |
| Significant fair-lending remediation | Clients, products, business practices | USD 40M |

Scenario outputs are reconciled against the recorded loss history so that the modeled tail is consistent with, but not bounded by, observed experience.

## 6. Business Continuity and Resilience Linkage

Operational resilience is managed as part of operational risk. Each critical business service has a defined impact tolerance expressed as the maximum tolerable duration and data loss before intolerable harm results. Recovery time and recovery point objectives for supporting systems must be at least as strict as the impact tolerance of the services they support. A breach of an impact tolerance in a test or a live event is captured as an operational loss event under Section 1 and reported to the Operational Risk Committee.

| Critical service | Impact tolerance (max duration) | Recovery point objective |
|---|---|---|
| Customer payments (wire, ACH) | 4 hours | 15 minutes |
| Card authorization | 1 hour | near zero |
| Online and mobile banking | 4 hours | 15 minutes |
| Core deposit ledger | 8 hours | 15 minutes |

## 7. Third-Party and Outsourcing Risk

### 7.1 Risk tiering of third parties

Every third party is tiered as critical, high, medium, or low based on the criticality of the service, the sensitivity of data accessed, and the substitutability of the provider. Critical and high third parties require enhanced due diligence before onboarding and at least annual reassessment.

### 7.2 Ongoing monitoring

Critical third parties are monitored against contractual service levels, financial health, and control attestations (such as SOC 2 reports). A critical third-party service disruption is treated as an operational loss event and follows Section 1. Information security aspects of third parties are coordinated with the Information Security Policy (MJD-SEC-0001).

### 7.3 Concentration and exit

The second line monitors concentration among third parties, including reliance on a single cloud provider or a single payment processor, and on fourth parties (the critical subcontractors of the Bank's providers). Every critical third party has a documented exit and substitution plan tested or reviewed at least every two years, so that a provider failure does not breach the impact tolerances in Section 6.

## 8. Operational Risk Reporting

The Head of Operational Risk reports to the Operational Risk Committee monthly. The report covers loss events above USD 100,000, aggregate losses by event type, RCSA results and overdue treatment plans, red KRIs, scenario analysis updates, and critical third-party status. Material items roll up into the Enterprise Risk Report under the Enterprise Risk Management Framework (MJD-RSK-0001).

## Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Operational Risk Committee | Oversee operational risk; review losses, KRIs, and scenarios |
| Head of Operational Risk | Own this Procedure; lead second-line operational risk |
| First-line operational risk coordinator | Capture events; complete RCSAs; monitor KRIs |
| OPERATIONS_ANALYST | Execute first-line controls; capture loss events within five business days; track KRIs |
| RISK_ANALYST | Maintain the taxonomy; reconcile losses; prepare operational risk reporting |
| COMPLIANCE_OFFICER | Assess regulatory dimension of events; coordinate on conduct and fair-lending matters |

## Exceptions and Escalation

A deviation from this Procedure, such as a delayed loss capture or a missed RCSA deadline, requires a documented exception approved by the Head of Operational Risk with a remediation date not exceeding 90 days. Repeated exceptions by the same unit are escalated to the Operational Risk Committee.

Escalation: an operational loss event with a gross impact at or above USD 1 million is escalated to the Head of Operational Risk within 24 hours and to the Operational Risk Committee at its next meeting. An event that could threaten solvency, liquidity, or material regulatory standing is escalated to the CRO within 24 hours per the Enterprise Risk Management Framework (MJD-RSK-0001). Suspected fraud is escalated in parallel under the Fraud Risk Management Procedure (MJD-RSK-0007).

## Related Documents

- MJD-RSK-0001 Enterprise Risk Management Framework
- MJD-RSK-0005 Stress Testing Framework (CCAR/DFAST)
- MJD-RSK-0007 Fraud Risk Management Procedure
- MJD-FIN-0002 Account Reconciliation Procedure
- MJD-SEC-0001 Information Security Policy (master)

## Regulatory References

- Basel III, Standardised Approach for Operational Risk
- SR 11-7, Guidance on Model Risk Management (for operational risk models)
- OCC Heightened Standards, 12 CFR 30 Appendix D
- FFIEC, Guidance on Managing Outsourcing Risk

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-05-01 | Head of Operational Risk | Initial operational risk procedure |
| 2.0.0 | 2023-07-01 | Head of Operational Risk | Added scenario analysis and third-party tiering |
| 2.4.0 | 2026-01-20 | Head of Operational Risk | Updated capture thresholds and KRI library |
