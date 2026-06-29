---
doc_id: MJD-CMP-0005
title: GLBA Privacy and Safeguards Policy
department: COMPLIANCE
doc_type: POLICY
classification: INTERNAL
owner_role: Chief Privacy Officer
allowed_roles: [COMPLIANCE_OFFICER, SOFTWARE_ENGINEER, SECURITY_ARCHITECT, OPERATIONS_ANALYST, BRANCH_STAFF]
effective_date: 2026-01-20
version: 2.1.0
review_cycle_months: 12
regulatory_refs: ["Gramm-Leach-Bliley Act (15 U.S.C. 6801-6809)", "Regulation P (12 CFR Part 1016)", "FTC Safeguards Rule (16 CFR Part 314)", "Interagency Guidelines Establishing Information Security Standards"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# GLBA Privacy and Safeguards Policy

## Purpose and Scope

This policy establishes how Meridian John Doe Financial (Meridian J.D.), a synthetic fintech for demonstration, protects the privacy and security of nonpublic personal information (NPI) under the Gramm-Leach-Bliley Act. It covers both the Privacy Rule (Regulation P), governing notices and information sharing, and the Safeguards Rule, governing the administrative, technical, and physical controls that protect customer information.

The policy applies to all NPI in any form, across every business line, system, and third party. It is deliberately classified INTERNAL and readable by a broad audience, including software engineers and security architects who implement safeguards controls, operations and branch staff who handle customer information daily, and compliance who owns the privacy program. This broad readership is intentional: everyone who touches customer data must understand their privacy obligations.

The technical implementation of safeguards controls is co-owned with the Technology and Security functions. Where this policy states a control objective, the engineering and security standards referenced in Related Documents state the implementation detail.

## Definitions

- **Nonpublic personal information (NPI)**: Personally identifiable financial information that a consumer provides, that results from a transaction, or that the institution otherwise obtains, and that is not publicly available.
- **Consumer**: An individual who obtains a financial product or service primarily for personal, family, or household purposes.
- **Customer**: A consumer with a continuing relationship with the institution.
- **Privacy notice**: The disclosure of the institution's information-collection and sharing practices, provided at the start of the customer relationship and annually where required.
- **Opt out**: The consumer's right to direct the institution not to share certain NPI with nonaffiliated third parties.
- **Safeguards**: The administrative, technical, and physical measures protecting NPI.
- **Qualified Individual**: The person designated to oversee, implement, and enforce the information security program under the Safeguards Rule.
- **Service provider**: A nonaffiliated third party that receives NPI to perform services for the institution.
- **Affiliate**: A company that controls, is controlled by, or is under common control with Meridian J.D.

## 1. Privacy Rule Program (Regulation P)

### 1.1 Privacy Notices

1.1.1 Meridian J.D. provides a clear and conspicuous initial privacy notice to each customer no later than the time the customer relationship is established, describing the categories of NPI collected and shared and the categories of recipients.

1.1.2 An annual privacy notice is provided where the institution's sharing practices require it. When sharing is limited to the exceptions that do not require annual delivery, the institution documents that determination, including the specific exception relied upon and the date the determination was made.

1.1.3 Notices are delivered in a manner calculated to reach the customer: electronically for customers enrolled in electronic delivery, by mail for others. Delivery confirmation records are retained per MJD-CMP-0008.

1.1.4 The content of the initial and annual privacy notices is reviewed by the Chief Privacy Officer and Legal before issuance. Changes to sharing practices that would require notice amendment are evaluated against the requirement to provide a revised notice and a new opt-out opportunity before implementation.

### 1.2 Information Sharing and Opt Out

1.2.1 Before sharing NPI with a nonaffiliated third party outside a permitted exception, the institution provides the consumer a reasonable opportunity to opt out and honors opt-out elections.

1.2.2 Opt-out elections are recorded, applied across systems within 30 days, and retained per MJD-CMP-0008. Sharing in violation of an opt-out is a reportable privacy incident.

1.2.3 Consumers may submit opt-out elections by any clearly communicated method: secure message, written notice, phone, or the opt-out mechanism in the online banking portal. All methods are monitored to confirm the election is captured and applied.

1.2.4 The institution does not condition the provision of a product or service on the consumer's waiver of opt-out rights.

### 1.3 Permitted Disclosures

1.3.1 Disclosures necessary to process a transaction the consumer requested, to service the account, or as legally required are permitted without opt out, consistent with Regulation P exceptions.

1.3.2 The institution maintains an internal register of its sharing relationships, the Regulation P exception relied upon, and the controls confirming that sharing does not exceed the exception scope. The register is reviewed by the Chief Privacy Officer annually and whenever a new sharing relationship is established.

### 1.4 Affiliate Sharing

1.4.1 Meridian J.D. may share NPI with its affiliates. Sharing of transaction and experience information with affiliates does not require an opt out under Regulation P. However, sharing NPI with affiliates for marketing purposes is conditioned on an affiliate-marketing opt-out opportunity provided in the privacy notice, and the institution honors those elections.

1.4.2 An affiliate that receives NPI from Meridian J.D. may not reuse that NPI for its own marketing beyond the scope described in the original notice without a new opt-out opportunity. The interaffiliate data-sharing agreement documents the permitted uses, the prohibition on reuse beyond scope, and each affiliate's obligation to maintain safeguards consistent with this policy.

1.4.3 Before establishing a new affiliate-sharing relationship, the Chief Privacy Officer must confirm: (a) the affiliate is within the corporate family by documented ownership; (b) the notice describes the affiliate-sharing category; and (c) the information security posture of the affiliate has been reviewed by the Qualified Individual. Sharing begins only after those conditions are satisfied.

1.4.4 Affiliate-sharing relationships are listed in the sharing register and are reviewed annually. If a company ceases to be an affiliate, existing NPI shared with it under the affiliate exception must be treated according to the nonaffiliated third-party rules from the date of cessation.

### 1.5 Joint Marketing Agreements

1.5.1 Meridian J.D. may share NPI with a nonaffiliated financial institution under a joint marketing agreement without triggering the consumer opt-out requirement, provided the agreement meets the Regulation P exception criteria: (a) the parties have a written agreement; (b) the agreement prohibits the nonaffiliated institution from using the NPI for any purpose other than the joint marketing and requires it to maintain the confidentiality of the NPI; and (c) the sharing is described in the privacy notice.

1.5.2 Before executing a joint marketing agreement, Legal confirms the counterparty qualifies as a "financial institution" under the GLBA, and the Chief Privacy Officer reviews the agreement to confirm the data-use restrictions are sufficient. The agreement must include: an audit right, a prohibition on further re-sharing, and a requirement to notify Meridian J.D. of any security incident affecting the shared NPI within 72 hours.

1.5.3 Joint marketing agreements are listed in the sharing register. Each agreement is reviewed annually, and no later than 30 days before renewal, to confirm the counterparty's practices continue to meet the exception conditions.

## 2. Safeguards Rule Program

### 2.1 Governance

2.1.1 The Qualified Individual oversees the information security program. At Meridian J.D. this responsibility is coordinated between the Chief Privacy Officer and the security function (SECURITY_ARCHITECT persona), with implementation by engineering (SOFTWARE_ENGINEER persona).

2.1.2 The information security program is documented, risk-based, and reviewed at least annually and after any material change. It reports to the board or a designated committee.

2.1.3 The Qualified Individual maintains authority to direct the allocation of resources to safeguards controls and to escalate unresolved security risks to the board committee. No other function may override a safeguards control decision without written approval from the Qualified Individual and board acknowledgment.

### 2.2 Risk Assessment

2.2.1 A written risk assessment identifies reasonably foreseeable internal and external risks to the confidentiality, integrity, and availability of NPI, and evaluates the sufficiency of safeguards in place. The risk assessment is updated at least annually and after any significant operational or technological change.

2.2.2 The risk assessment covers each of the following risk categories:

| Risk category | Examples | Control adequacy metric |
|---|---|---|
| Employee error and insider threat | Misdirected email, unauthorized access, data exfiltration | Access review completion rate (target: 100% within cadence window); insider-threat detection alert volume |
| External cyberattack | Phishing, credential stuffing, ransomware | Phishing simulation failure rate (target: less than 5%); mean time to detect (target: less than 4 hours for critical events) |
| Third-party / service provider | Breach at a service provider, contract non-compliance | Assessment completion rate (target: 100% of Tier 1 and Tier 2 providers per cadence); unresolved critical findings (target: 0 beyond SLA) |
| Physical security | Unauthorized physical access to workstations or paper records | Physical access review cadence; clean-desk audit findings |
| System failure and data loss | Backup failure, corruption | Backup verification success rate (target: 100% monthly); RTO/RPO test results |
| Change-induced vulnerability | New code introducing a security flaw | SAST/DAST defect escape rate; mean time to remediate Critical vulnerabilities (target: 7 days) |

2.2.3 Where a control is rated insufficient in the risk assessment, the Qualified Individual assigns a remediation owner and a target date, and tracks the finding to closure. Open findings are reported to the board committee at each reporting cycle.

### 2.3 Required Safeguards

2.3.1 **Access controls**: Access to NPI is restricted to authorized personnel on a least-privilege basis and is periodically reviewed. Implementation follows the IAM standard (MJD-SEC-0003).

2.3.2 **Encryption**: NPI is encrypted in transit and at rest. Where encryption is infeasible, compensating controls approved by the security function are documented.

2.3.3 **Multi-factor authentication**: MFA is required for any individual accessing systems holding NPI.

2.3.4 **Logging and monitoring**: Access to and changes affecting NPI are logged and monitored. Logs must never contain NPI in cleartext; the data classification and handling standard governs what may be logged.

2.3.5 **Secure disposal**: NPI is securely disposed of when no longer needed for a legitimate business or legal purpose, consistent with the retention schedule (MJD-CMP-0008).

2.3.6 **Change management and secure development**: Systems handling NPI follow secure development and change controls so that privacy is preserved through the software lifecycle.

### 2.4 Service Provider Oversight

2.4.1 Service providers that receive NPI are selected and contractually required to maintain safeguards consistent with this policy, and are periodically assessed. Detailed due diligence procedures are in Section 2.7.

### 2.5 Incident Response

2.5.1 A security event affecting NPI is handled under the incident response process (MJD-SEC-0006). A reportable breach is escalated to the Qualified Individual, the Chief Privacy Officer, and Legal, and customer notification is provided where required. The interplay with incident severity levels and notification windows is in Section 2.8.

### 2.6 Penetration Testing and Vulnerability Management

2.6.1 Systems that store, process, or transmit NPI are included in the annual penetration test scope managed under MJD-SEC-0005. The penetration test must include:

- External network testing targeting the perimeter of NPI-holding systems.
- Application-layer testing of any web or API interface that accepts or returns NPI.
- Social engineering and phishing simulation targeting personnel with access to NPI.
- Verification that prior-year penetration test findings are remediated.

2.6.2 Penetration tests are conducted by an independent external firm approved by the Qualified Individual. Independence means the firm did not implement the controls being tested and has no financial relationship with any vendor supplying those controls.

2.6.3 The penetration test cadence is:

| Assessment type | Frequency | Trigger event (additional test required if any occur) |
|---|---|---|
| External penetration test | Annual | Material new perimeter exposure; Critical vulnerability in production |
| Application penetration test | Annual, or on major release | Any new system processing NPI; major architecture change |
| Internal network test | Annual | Any lateral-movement incident in the prior 12 months |
| Social engineering / phishing | Semi-annual | Any confirmed phishing compromise of an NPI-access account |
| Vulnerability scan | Monthly (authenticated) | After any production deployment to NPI-holding systems |

2.6.4 Remediation SLAs for penetration test findings: Critical severity within 7 calendar days; High within 30 days; Medium within 90 days; Low within 180 days. Findings that exceed SLA without written risk acceptance by the Qualified Individual are escalated to the board committee.

2.6.5 Vulnerability management for NPI systems is a joint responsibility of the SOFTWARE_ENGINEER and SECURITY_ARCHITECT personas. A Critical vulnerability (CVSS 9.0 or above) in a production system holding NPI triggers an immediate incident bridge with the Qualified Individual as the required participant.

### 2.7 Third-Party Service Provider Assessment Program

2.7.1 Before sharing NPI with a service provider, the COMPLIANCE_OFFICER and SECURITY_ARCHITECT jointly complete a pre-contract due diligence assessment. No NPI is shared until the assessment is satisfactory and the contract is executed.

2.7.2 Service providers are tiered based on sensitivity of NPI access and criticality to operations:

| Tier | Criteria | Due diligence before contract | Ongoing assessment cadence |
|---|---|---|---|
| Tier 1 (Critical) | Direct access to unencrypted NPI, or a processor critical to core banking functions | Full security questionnaire; SOC 2 Type II or ISO 27001 report review; right-to-audit clause; references; legal review of DPA | Annual (full reassessment) |
| Tier 2 (Significant) | Access to encrypted NPI or aggregated/de-identified data; moderate operational dependency | Security questionnaire; SOC 2 Type II report review (current year); contractual safeguards clause | Every 18 months |
| Tier 3 (Limited) | Incidental NPI access (for example, a shipping provider that sees a name/address); low operational dependency | Contractual safeguards clause; self-attestation | Every 36 months or on contract renewal |

2.7.3 All service provider contracts for Tier 1 and Tier 2 providers must include: (a) a requirement to maintain safeguards appropriate to the NPI; (b) a right to audit or obtain audit reports; (c) a notification obligation within 72 hours if the provider discovers or suspects an NPI breach; (d) a requirement to return or destroy NPI upon contract termination; and (e) a prohibition on sub-sharing NPI with a fourth party without Meridian J.D. written consent.

2.7.4 The COMPLIANCE_OFFICER maintains a service provider register listing each provider, its tier classification, the most recent assessment date, the next assessment due date, and any open findings. The register is reviewed by the Chief Privacy Officer quarterly.

2.7.5 If a Tier 1 service provider's annual assessment reveals a Critical finding, the service provider must provide a written remediation plan within 15 business days. If the finding is not remediated within the agreed timeline and poses ongoing risk to NPI, the Chief Privacy Officer and Legal evaluate whether to suspend NPI sharing with the provider.

### 2.8 Incident Response Integration

2.8.1 Privacy incidents are handled under the Incident Response Plan (MJD-SEC-0006). For the purposes of GLBA coordination, privacy incidents are categorized using the MJD-SEC-0006 severity scale as follows:

| SEC-0006 severity | Privacy-incident examples | Chief Privacy Officer notification SLA | Board notification |
|---|---|---|---|
| Critical (S1) | Confirmed breach of NPI affecting more than 500 customers; ransomware encrypting NPI datastores; confirmed data exfiltration | Immediate (within 1 hour of detection) | Within 24 hours |
| High (S2) | Breach of NPI affecting fewer than 500 customers; unauthorized access to NPI without confirmed exfiltration; service provider notifying of NPI breach | Within 4 hours | Within 48 hours |
| Medium (S3) | Near-miss: unauthorized access attempt to NPI systems that was blocked; misdirected NPI email affecting fewer than 10 consumers | Within 24 hours | Monthly board report |
| Low (S4) | Policy violation with no NPI exposure; individual consumer data request error corrected same day | Within 48 hours | Quarterly summary |

2.8.2 The GLBA Safeguards Rule requires customer notification in the event of a notification event (as defined by applicable FTC rules). The Qualified Individual and Legal determine whether a specific incident meets the notification threshold. Where notification is required, customers are notified as expeditiously as possible and no later than 30 days after the determination that the event is a notification event. Where notification to the FTC is required (500 or more customers affected), the FTC is notified within 30 days.

2.8.3 Notification letters are pre-drafted in template form by Legal and the Chief Privacy Officer, and are reviewed for accuracy before each issuance. The notification log is retained per MJD-CMP-0008.

### 2.9 Board and Management Reporting

2.9.1 The Qualified Individual reports on the safeguards program to the board or its designated committee at least annually. The annual report includes:

- Status of the written information security program and any material changes since the last report.
- Results of the most recent risk assessment, including control adequacy ratings.
- Penetration test outcomes and remediation status.
- Third-party service provider assessment completion rates and outstanding material findings.
- Incidents and near-misses since the last report, with root cause and remediation.
- Training completion rates by role.
- Open exceptions to required safeguards and their risk-acceptance status.

2.9.2 The board committee reviews and acknowledges the annual report. If the report identifies any Critical open risk without an accepted remediation plan, the committee must document its consideration of that risk before the next cycle.

2.9.3 In addition to the annual report, the Qualified Individual provides a quarterly management summary to the Chief Privacy Officer and the Chief Risk Officer covering: (a) any new incidents or significant near-misses; (b) status of Critical and High vulnerability remediations; (c) any service provider assessments with outstanding Critical findings; and (d) any exception that has exceeded its approved duration.

## 3. Training and Awareness

3.1 All personnel with access to NPI complete privacy and safeguards training at hire and annually. Training is administered through the compliance learning management system, and completion is tracked with a timestamp, the version of the training completed, and the employee identifier. Records are retained per MJD-CMP-0008.

3.2 Role-specific training curricula are as follows:

| Role | Core privacy and safeguards module | Additional required modules | Frequency |
|---|---|---|---|
| BRANCH_STAFF | 60-minute privacy fundamentals: what is NPI, how to handle it, what not to do, how to report a privacy incident | Physical document handling; oral disclosure rules; opt-out capture | Annual; at hire within 30 days |
| OPERATIONS_ANALYST | 60-minute privacy fundamentals; 30-minute data handling and system access module | Secure file transfer; opt-out processing; service provider incident notification recognition | Annual; at hire within 30 days |
| SOFTWARE_ENGINEER | 60-minute privacy fundamentals; 45-minute privacy-by-design and secure development module | Encryption implementation requirements; logging-NPI prohibition; incident detection and escalation | Annual; at hire within 14 days; after any major policy change |
| SECURITY_ARCHITECT / Qualified Individual | 90-minute comprehensive safeguards and risk assessment module | Penetration test planning; vendor assessment; incident response; board reporting | Annual; at hire within 14 days |
| COMPLIANCE_OFFICER | 60-minute privacy fundamentals; 45-minute compliance testing module | Opt-out auditing; notice review; third-party register management | Annual; at hire within 14 days |

3.3 Failure to complete required training by the annual deadline results in the following escalation steps: (a) automated reminder at 30 days before due date; (b) manager notification at 7 days before due date; (c) system access restriction to NPI-holding systems at 1 business day after due date, lifted only upon completion confirmation from the learning management system; (d) escalation to HR for performance review consideration if not completed within 30 days after due date.

3.4 Personnel who fail the knowledge-check component of any module with a score below 80% are required to retake the training within 14 days. Persistent failure (three or more failed attempts) is reported to the employee's manager and Compliance.

3.5 Training content is reviewed by the Chief Privacy Officer annually for accuracy and updated whenever there is a material regulatory change or a significant privacy incident that reveals a training gap.

## 4. Privacy-by-Design Requirements

4.1 All new systems, features, or data flows that will collect, store, or process NPI must undergo a Privacy Impact Assessment (PIA) before design is finalized. The PIA is the mechanism by which privacy principles are embedded in architecture rather than retrofitted.

4.2 PIA trigger criteria: a PIA is required when any of the following apply: (a) a new system will collect NPI not previously collected by the institution; (b) an existing system will be materially changed to expand NPI collection or sharing; (c) a new third-party integration will provide NPI to or receive NPI from the institution; or (d) a new AI or automated decision-making system will process NPI.

4.3 PIA process steps:

1. The SOFTWARE_ENGINEER or product owner completes the PIA template, describing: the categories of NPI to be processed, the purpose and legal basis, the data flows (source, storage, transmission, sharing), and the retention period.
2. The Chief Privacy Officer reviews the completed PIA within 10 business days, assessing whether the proposed design is consistent with this policy, the notice, and opt-out elections on file.
3. Where the PIA identifies a privacy risk, the Chief Privacy Officer specifies a required design change or compensating control. Development may not proceed past design review until the risk is resolved.
4. The approved PIA is retained with the project's design documentation.

4.4 Data minimization: systems must collect only the NPI fields that are necessary for the stated purpose. The PIA template requires the engineer to document why each NPI field is necessary. Optional fields that consumers voluntarily provide are clearly labeled as optional in the interface.

4.5 Privacy-default settings: where a feature offers a choice that affects NPI sharing or visibility, the default setting must be the most privacy-protective option. Any deviation from this principle requires written approval from the Chief Privacy Officer.

4.6 Purpose limitation: NPI collected for one purpose must not be repurposed for an incompatible secondary purpose without a new privacy notice and, where required, a new opt-out opportunity. Engineers who identify a proposed repurposing must escalate to the Chief Privacy Officer before any development begins.

4.7 Engineers are responsible for ensuring that: (a) NPI is never written to application logs in cleartext; (b) NPI is masked in non-production environments; (c) NPI is encrypted in transit and at rest before the feature is deployed to any environment beyond the engineer's local workstation; and (d) test data does not use real NPI without the specific written approval of the Chief Privacy Officer.

## 5. Consumer Rights and Requests

5.1 Meridian J.D. recognizes the following consumer rights with respect to NPI, consistent with applicable law:

- **Access**: A consumer may request confirmation of whether the institution holds NPI about them, and a copy of the categories of NPI held.
- **Correction**: A consumer may request correction of inaccurate NPI.
- **Opt out**: A consumer may opt out of nonaffiliated third-party sharing as described in Section 1.2.
- **Complaint**: A consumer may submit a complaint about how the institution has handled their NPI.

5.2 Response SLAs:

| Request type | Acknowledgment | Response / resolution | Escalation if not resolved |
|---|---|---|---|
| Access request | 5 business days | 30 calendar days | Chief Privacy Officer at 20 calendar days; Legal at 25 calendar days |
| Correction request | 5 business days | 15 calendar days | Chief Privacy Officer at 10 calendar days |
| Opt-out election | Immediate (automated confirmation) | Applied within 30 days; confirmed to consumer | COMPLIANCE_OFFICER if not applied within 30 days |
| Privacy complaint | 5 business days | 30 calendar days; complex cases up to 45 days with notice to consumer | Chief Privacy Officer at 20 calendar days |

5.3 All consumer rights requests are logged in the privacy request management system, assigned a unique reference number, and tracked to closure. The log is retained per MJD-CMP-0008.

5.4 When responding to an access request, the institution verifies the identity of the requestor using the same identity verification steps applied at account opening, before disclosing any NPI. A request that cannot be identity-verified is declined, and the consumer is advised of alternative verification methods.

5.5 If an access or correction request reveals an error in NPI that originated from a credit bureau, service provider, or other third party, the institution notifies the third party of the correction and requests that the third party update its records.

5.6 Consumers who are dissatisfied with the institution's response to a privacy request may escalate to the Chief Privacy Officer. The Chief Privacy Officer's determination is final at the institution level. Consumers are informed of the right to file a complaint with the Consumer Financial Protection Bureau or the relevant federal banking regulator.

## Roles and Responsibilities

- **Chief Privacy Officer**: Owns this policy, the privacy notice program, opt-out handling, PIA review, and consumer rights responses.
- **Qualified Individual / Security Architect (SECURITY_ARCHITECT persona)**: Oversees the safeguards program and approves compensating controls; signs off on penetration test scope and vendor security assessments.
- **Software Engineer (SOFTWARE_ENGINEER persona)**: Implements technical safeguards (access controls, encryption, logging, secure disposal); completes PIAs for new systems; ensures no NPI in logs.
- **Compliance Officer (COMPLIANCE_OFFICER persona)**: Monitors privacy compliance; maintains service provider register; handles privacy incidents; validates opt-out processing.
- **Operations and Branch Staff (OPERATIONS_ANALYST, BRANCH_STAFF personas)**: Handle NPI per this policy at the point of service; report suspected privacy incidents immediately.

## Exceptions and Escalation

Any exception to a required safeguard must be documented with a risk justification and compensating controls and approved by the Qualified Individual and the Chief Privacy Officer. A suspected privacy breach is escalated immediately to the Chief Privacy Officer, the security function, and Legal. Violations of opt-out elections or unauthorized NPI sharing are escalated to Compliance and may trigger SAR consideration if linked to suspicious activity (MJD-CMP-0002).

## Related Documents

- **MJD-CMP-0001** BSA/AML Program Policy
- **MJD-CMP-0008** Records Retention Schedule
- **MJD-SEC-0003** Identity and Access Management (IAM) Policy
- **MJD-SEC-0005** Penetration Testing and Vulnerability Management Standard
- **MJD-SEC-0006** Incident Response Plan
- **MJD-SEC-0008** Data Classification and Handling Standard
- **MJD-TEC-0004** Secrets and Key Management Policy

## Regulatory References

- Gramm-Leach-Bliley Act, 15 U.S.C. 6801-6809
- Regulation P, 12 CFR Part 1016, privacy of consumer financial information
- FTC Safeguards Rule, 16 CFR Part 314
- Interagency Guidelines Establishing Information Security Standards

## Revision History

| Version | Effective date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2021-05-01 | Chief Privacy Officer | Initial GLBA privacy and safeguards policy. |
| 2.0.0 | 2024-03-01 | Chief Privacy Officer | Updated to revised FTC Safeguards Rule: Qualified Individual, MFA, encryption mandates. |
| 2.1.0 | 2026-01-20 | Chief Privacy Officer | Annual review; clarified logging-no-NPI requirement and service-provider assessment cadence. |
