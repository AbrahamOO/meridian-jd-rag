---
doc_id: MJD-SEC-0006
title: Incident Response Plan
department: SECURITY
doc_type: RUNBOOK
classification: CONFIDENTIAL
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT, SOFTWARE_ENGINEER, RISK_ANALYST]
effective_date: 2026-01-30
version: 4.1.0
review_cycle_months: 12
regulatory_refs: ["NIST SP 800-61 Rev 2", "GLBA Safeguards Rule (16 CFR Part 314.4(h))", "PCI DSS 4.0 Requirement 12.10", "NYDFS 23 NYCRR 500.17", "FFIEC Information Security Booklet", "SEC Cybersecurity Disclosure Rules"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Incident Response Plan

## Purpose and Scope

This Incident Response Plan (IRP) is the operational runbook that governs how Meridian John Doe Financial (Meridian J.D.) detects, triages, contains, eradicates, recovers from, and learns from security incidents. It defines incident severity levels, response time objectives, the response team structure, the step-by-step playbook for the lifecycle phases, breach notification obligations, and the escalation chain. It is the document on call during an active incident.

This document is classified CONFIDENTIAL and readable by SECURITY_ARCHITECT, SOFTWARE_ENGINEER, and RISK_ANALYST, because engineers execute containment and recovery on the systems they operate and risk must assess and report incident impact.

Scope covers all confirmed and suspected security incidents affecting Meridian J.D. information assets, including data breaches, malware, account compromise, denial of service, insider misuse, cryptographic key compromise, and incidents involving the internal AI and retrieval systems (for example, an attempted access-control bypass or prompt-injection event that succeeds in surfacing out-of-scope content).

## Definitions

**Event.** Any observable occurrence in a system or network.

**Incident.** An event, or series of events, that compromises or threatens the confidentiality, integrity, or availability of an information asset, or violates security policy.

**Breach.** An incident confirmed to involve unauthorized acquisition of, or access to, protected customer or sensitive data.

**Mean time to detect (MTTD).** The average elapsed time from incident onset to detection.

**Mean time to respond (MTTR).** The average elapsed time from detection to containment.

**Containment.** Actions that stop an incident from spreading or causing further damage.

**Eradication.** Removal of the root cause and any attacker presence.

**Incident commander.** The single accountable leader of the response for a given incident.

**Indicator of compromise (IOC).** An artifact that indicates a system has been compromised.

**CSIRT.** Computer Security Incident Response Team: the group activated to manage SEV-1 and SEV-2 incidents.

**Chain of custody.** A documented record of who collected, handled, and transferred evidence, ensuring its integrity for forensic and legal purposes.

## 1. Incident Severity and Response Objectives

### 1.1 Severity Levels

1.1.1 Incidents are classified into four severity levels:

| Severity | Definition | Examples |
|---|---|---|
| SEV-1 Critical | Confirmed breach of customer data, RESTRICTED data exposure, or major service outage | Customer PII exfiltration, KMS key compromise, ransomware |
| SEV-2 High | Material compromise contained to internal systems, no confirmed customer-data loss | Account takeover of an admin, malware on a production host |
| SEV-3 Medium | Limited-impact incident, contained quickly | Single-workstation malware, phishing click with no credential loss |
| SEV-4 Low | Minor policy violation or anomaly with negligible impact | Isolated misconfiguration, benign scan |

### 1.2 Response Time Objectives

1.2.1 Acknowledge, contain, and begin notification within these targets, measured from detection:

| Severity | Acknowledge | Contain | Status cadence |
|---|---|---|---|
| SEV-1 | 15 minutes | 1 hour | Every 30 minutes |
| SEV-2 | 30 minutes | 4 hours | Every 2 hours |
| SEV-3 | 2 hours | 24 hours | Daily |
| SEV-4 | 1 business day | 5 business days | At closure |

### 1.3 Incident Declaration Procedure

1.3.1 The authority to declare an incident rests with the SOC duty analyst for SEV-3 and SEV-4 incidents, and with the SOC shift lead or SECURITY_ARCHITECT for SEV-1 and SEV-2 incidents. An analyst who believes an event warrants SEV-1 or SEV-2 must escalate to the shift lead immediately; they do not wait to confirm.

1.3.2 A declaration is logged in the incident tracking system within 5 minutes of the decision, with the following mandatory fields completed: incident identifier (auto-assigned), declaration timestamp, declared severity, declaring authority (named individual), initial description, affected systems, and evidence reference (SIEM alert ID or equivalent). Partial fields are not acceptable; an incomplete record is flagged for immediate correction.

1.3.3 On declaration of a SEV-1 or SEV-2, the SOC duty analyst simultaneously: pages the on-call CSIRT lead via the paging system; opens the incident communication channel (a dedicated, timestamped channel in the secure messaging platform); and sends the initial notification to the SECURITY_ARCHITECT. All three actions must be completed within 5 minutes of declaration. The communication channel is the single authoritative record during the incident; no out-of-band decisions are made.

1.3.4 Severity may be upgraded at any time as new information arrives; upgrades take immediate effect on all SLA clocks and escalation obligations. Severity may be downgraded only by the Incident Commander with documented justification; downgrade does not retroactively extend elapsed time on a higher-severity SLA that was already running.

## 2. Response Team Structure

2.1.1 The Computer Security Incident Response Team (CSIRT) is activated for SEV-1 and SEV-2 incidents and comprises: an Incident Commander (security lead), a technical lead per affected domain, a communications lead, a legal and compliance liaison, and a scribe.

2.1.2 The Incident Commander has authority to direct containment actions across teams during an active incident, including taking systems offline, regardless of normal change controls.

2.1.3 The Security Operations Center (SOC) runs 24x7 and is the first responder and the central coordination point. The SOC declares incidents and pages the CSIRT.

### 2.2 On-Call Rotation and Escalation Chain

2.2.1 The CSIRT operates a 24x7 on-call rotation with a primary and a secondary on-call responder for each week. The rotation schedule is maintained in the paging system and reviewed monthly to ensure coverage. On-call assignments are confirmed no later than the Friday before the on-call week begins.

2.2.2 On a SEV-1 or SEV-2 declaration, the SOC pages the primary on-call CSIRT lead. The primary on-call must acknowledge within 15 minutes for SEV-1 and within 30 minutes for SEV-2. Acknowledgment means active confirmation of receipt and commitment to join the incident channel, not merely that the page was seen.

2.2.3 If the primary on-call does not acknowledge within the required window, the SOC immediately pages the secondary on-call responder. If neither the primary nor the secondary acknowledges within double the acknowledgment window, the SOC pages the SECURITY_ARCHITECT directly, regardless of time of day. The SECURITY_ARCHITECT is always reachable for SEV-1 escalation.

2.2.4 The escalation chain for a SEV-1 is: primary on-call CSIRT lead (T+0), secondary on-call CSIRT lead if no ack (T+15 min), SECURITY_ARCHITECT (T+30 min), CISO (T+30 min after SECURITY_ARCHITECT notification). For a SEV-2: primary on-call CSIRT lead (T+0), secondary (T+30 min), SECURITY_ARCHITECT (T+60 min).

2.2.5 Contact information for all on-call responders and the escalation chain is maintained in the paging system and in the secure contact directory accessible to SOC analysts even if the primary communication platform is unavailable. An out-of-band contact method (personal mobile numbers registered in the system) is maintained for SEV-1 scenarios where internal systems are affected.

## 3. Incident Lifecycle Playbook

### 3.1 Phase 1: Detection and Analysis

3.1.1 Incidents are detected by SIEM alerts (MJD-SEC-0009), endpoint detection, user reports, threat intelligence, or third-party notification. Every alert is triaged by the SOC.

3.1.2 The SOC validates the event, assigns a preliminary severity, opens an incident record with a unique identifier, and preserves initial evidence (logs, memory, disk images) before any remediation that could destroy it.

3.1.3 For a suspected AI/retrieval access-control failure, the SOC immediately captures the offending query, the audit record, and the assembled context, and confirms whether out-of-scope content was actually surfaced.

3.1.4 Log and Evidence Preservation Checklist. Before any remediation action on an affected system, the following artifacts must be captured and placed under chain of custody:

- SIEM log export: all log events for the affected principal identities and source IPs from 48 hours before the first suspicious event through the current time. Export must be in a tamper-evident format with hash verification.
- Network packet capture: if a network-level capture of the relevant traffic flows is feasible without disrupting production (for example, from a network tap already in place), it must be captured for the window of the incident.
- Memory image: for any affected host where volatile memory may contain attacker tooling, credentials, or command-and-control artifacts, a full memory image is taken before any reboot or process termination.
- Disk image: for any host suspected of persistent compromise (rootkit, implant), a forensic disk image is taken before any remediation. The image is stored in a write-protected location and its SHA-256 hash is recorded in the incident record.
- Application audit trail: for the specific system affected, the full audit log from the application layer (access logs, session records, API call logs) is exported and hashed.
- Chain-of-custody form: every artifact is logged on the chain-of-custody form in the incident record: artifact description, collection timestamp, collecting analyst, hash value, storage location, and transfer log. No artifact is transferred to a third party (legal counsel, law enforcement, forensics vendor) without a signed chain-of-custody entry.

### 3.2 Phase 2: Containment

3.2.1 Short-term containment isolates the affected asset (network quarantine via MJD-SEC-0004 zone rules, account disablement via MJD-SEC-0003, session revocation).

3.2.2 For confirmed or suspected cryptographic key compromise, emergency key rotation is initiated per the Cryptographic Standard (MJD-SEC-0002 Section 5.2.3), completing within 24 hours of confirmation.

3.2.3 Evidence is preserved throughout; containment never overwrites forensic data without an image first.

3.2.4 Containment Decision Matrix. The following table specifies the containment levers and decision criteria by attack type. The Incident Commander selects from these levers based on the confirmed or suspected attack type. Multiple levers may be applied simultaneously; each lever applied is logged in the incident record with timestamp and authorizing name.

| Attack type | Containment levers | Decision criteria |
|---|---|---|
| Data breach (confirmed exfiltration) | Network egress block for the affected host; account suspension for the involved principal; audit log export before any change; legal liaison notified immediately | Apply if data is confirmed to have left the environment; prioritize forensic preservation before containment action; notify legal before any system change that could affect evidence |
| Malware (host compromise) | Network quarantine (remove host from production VLAN, move to quarantine VLAN per MJD-SEC-0004); disable auto-start mechanisms remotely if feasible without reboot; do not reboot before memory image; endpoint isolation at the EDR console | Apply quarantine immediately on confirmation; memory image before any reboot; do not attempt manual malware removal without forensic image; escalate to forensics team if rootkit is suspected |
| Account compromise (credential theft or MFA bypass) | Immediate session revocation across all active sessions for the account (MJD-SEC-0003); forced password reset; temporary account suspension if revocation is insufficient; audit all actions taken by the account in the 72 hours prior | Apply within the acknowledgment window; revoke all sessions (not only the suspicious session, as the attacker may have spawned additional sessions); do not reuse the same credential after reset until the compromise vector is identified |
| Ransomware | Network isolation of all affected hosts simultaneously (not sequentially, to prevent lateral spread); disable file shares accessible from affected hosts; identify backup integrity before any recovery; engage external incident response firm for SEV-1 ransomware per standing retainer | Act fast to limit encryption spread; isolating one host at a time may allow the attacker to pivot to the next; backup integrity check is mandatory before attempting recovery from backups |
| API access-control bypass | Rate-limit or block the offending principal at the API gateway; disable the specific endpoint if safe to do so; preserve all API logs with query content; assess whether out-of-scope data was returned in any response | Assess data exposure scope before disabling the endpoint; disabling may alert the attacker but protects further exposure; treat as at least SEV-2; if CONFIDENTIAL or RESTRICTED data was returned to an unauthorized caller, escalate to SEV-1 |

### 3.3 Phase 3: Eradication

3.3.1 The root cause is identified and removed: malware deleted, vulnerabilities patched (on the emergency path of MJD-SEC-0005), attacker persistence eliminated, and compromised credentials reset.

3.3.2 The environment is validated clean before recovery; lingering IOCs block the recovery phase.

### 3.4 Phase 4: Recovery

3.4.1 Systems are restored from known-good state, monitored intensively for recurrence, and returned to production only after the Incident Commander confirms eradication.

3.4.2 Heightened monitoring continues for a minimum of 14 days after recovery for SEV-1 and SEV-2 incidents.

### 3.5 Phase 5: Post-Incident Review

3.5.1 A blameless post-incident review is held within 10 business days of closure for SEV-1 and SEV-2 incidents, producing a timeline, root cause, and corrective actions with owners and due dates.

3.5.2 Corrective actions are tracked to completion and feed the threat model (MJD-SEC-0007) and the risk register (MJD-RSK-0001).

3.5.3 Lessons-Learned Template. Every SEV-1 and SEV-2 post-incident review must produce a lessons-learned document using the following required sections. Omitting a section requires Incident Commander approval and a written justification.

**Section A: Incident Timeline.** A chronological table with columns: timestamp (UTC), event description, source of information, and actor (system or named individual). The timeline must cover from the earliest evidence of attacker activity (even if not detected in real time) through incident closure. Time gaps greater than 30 minutes must be explained.

**Section B: Root Cause Analysis.** A concise statement of the technical root cause (the specific vulnerability, misconfiguration, or control gap that permitted the incident) and the contributing factors (the process or design weaknesses that allowed the root cause to exist). Use the "5 Whys" or a fishbone structure. The root cause must be specific enough to drive a remediation action: "weak authentication" is not acceptable; "MFA was not enforced on the affected service account class because the enforcement policy had a scope exclusion for legacy service accounts" is acceptable.

**Section C: Impact Assessment.** Quantified impact across: data exposure (what data, how many records, what classification, confirmed or probable); operational impact (system downtime, customer-facing impact, revenue or transaction impact); financial impact (estimated cost of response, potential regulatory fines, customer restitution); and reputational impact (was the incident disclosed externally, and what was the response).

**Section D: What Worked.** A candid assessment of detection, response, and containment steps that performed as designed. Attribute specific controls, procedures, or individual actions that limited impact or accelerated response. This section informs which existing controls to reinforce.

**Section E: What Failed.** A candid assessment of detection gaps, delayed responses, missing procedures, or control failures. No blame is assigned to individuals; failures are attributed to processes, tools, or gaps in standards. This section is the direct driver of corrective actions.

**Section F: Corrective Actions.** A table with columns: action description, owner (named role or individual), due date, and status. Every root cause and every failure in Section E must map to at least one corrective action. Corrective actions must be specific and verifiable. Actions are tracked in the risk register (MJD-RSK-0001) through completion.

## 4. Breach Notification

4.1.1 The legal and compliance liaison assesses notification obligations as soon as a breach is suspected. Determinations are documented.

4.1.2 Customer notification of a confirmed breach of nonpublic personal information follows the GLBA Safeguards Rule and applicable state law, without unreasonable delay. Regulator notification (for example NYDFS within 72 hours of determining a reportable cybersecurity event) is made within the applicable statutory window.

4.1.3 Material cybersecurity incidents are assessed for public disclosure obligations under the SEC cybersecurity disclosure rules.

4.1.4 All notification determinations, timelines, and communications are documented in the incident record and retained for 7 years to evidence regulatory compliance. The decision NOT to notify, where reached, is documented with its legal basis.

### 4.2 Notification Timeline Summary

4.2.1 The following are the binding internal notification targets, distinct from external statutory windows:

| Audience | Trigger | Internal target |
|---|---|---|
| SOC and CSIRT | Any declared SEV-1 or SEV-2 | Immediate page |
| CISO and executives | SEV-1 declaration | Within 30 minutes |
| Legal and compliance liaison | Suspected breach of customer data | Within 1 hour |
| Board Risk Committee | Confirmed SEV-1 breach | Within 24 hours |
| Affected customers | Confirmed breach of NPI | Without unreasonable delay, per GLBA and state law |
| Regulators (for example NYDFS) | Reportable cybersecurity event | Within the statutory window (72 hours for NYDFS) |

### 4.3 NYDFS 23 NYCRR 500 Compliance Steps

4.3.1 NYDFS 23 NYCRR 500.17 requires notification to the Superintendent of the New York State Department of Financial Services within 72 hours of determining that a Cybersecurity Event has occurred. A Cybersecurity Event under the regulation is any act or attempt, successful or unsuccessful, to gain unauthorized access to, disrupt, or misuse an information system or information stored on such a system.

4.3.2 The 72-hour clock starts when Meridian J.D. determines that a Cybersecurity Event has occurred. For purposes of this standard, a determination occurs when the Incident Commander declares the incident and the legal and compliance liaison confirms the event meets the NYDFS definition. The determination timestamp is recorded in the incident record as the "NYDFS clock start."

4.3.3 The notification to NYDFS must contain: the date of the Cybersecurity Event; a description of the event; how the event was detected; when the event was detected; the systems affected; the type of data that may have been accessed; whether customer NPI was involved; and the remediation steps taken or planned. A preliminary notification is acceptable if investigation is ongoing; a final notification with complete information follows within 90 days of the event.

4.3.4 The legal and compliance liaison is responsible for drafting the NYDFS notification in coordination with the Incident Commander. The CISO approves the notification before submission. The notification is submitted through the NYDFS Cybersecurity Portal and a copy is retained in the incident record.

4.3.5 Any incident involving an unauthorized acquisition of NPI or RESTRICTED data, or a disruption to the cardholder data environment, automatically triggers assessment of the NYDFS notification obligation. The legal liaison performs this assessment within 1 hour of the incident reaching SEV-1 status.

## 5. Communications

5.1.1 All external communications during an incident are coordinated by the communications lead under the Incident Commander's direction and reviewed by legal. No team member communicates externally about an active incident outside this channel.

5.1.2 Internal status updates follow the cadence in Section 1.2 and use a single authoritative incident channel to prevent fragmented or contradictory information.

5.1.3 A holding statement is prepared early for SEV-1 incidents so that, if disclosure becomes necessary, the institution responds quickly and consistently.

## 6. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this plan; typically serves as or appoints the Incident Commander for SEV-1. |
| SOC | 24x7 detection, triage, declaration, and coordination. |
| SOFTWARE_ENGINEER | Executes containment, eradication, and recovery on owned systems. |
| RISK_ANALYST | Assesses impact, updates the risk register, supports regulatory reporting. |
| Legal and compliance liaison | Determines and executes breach-notification obligations. |
| Communications lead | Manages internal and external communications under the IC's direction. |

### 6.1 Responsibility Assignment Matrix (RACI)

The following RACI table assigns roles across the incident lifecycle phases. R: Responsible (does the work); A: Accountable (owns the outcome); C: Consulted (provides input); I: Informed (receives status updates).

| Lifecycle phase | SECURITY_ARCHITECT | SOC | SOFTWARE_ENGINEER | RISK_ANALYST | Legal liaison | Communications lead |
|---|---|---|---|---|---|---|
| Detection and alert triage | I | R/A | I | I | I | I |
| Incident declaration | C | R | I | I | I | I |
| CSIRT activation | A | R | I | I | I | I |
| Evidence preservation | A | R | C | I | C | I |
| Severity assignment | A | R | C | C | C | I |
| Containment execution | A | C | R | I | I | I |
| Eradication | A | C | R | I | I | I |
| Recovery and validation | A | C | R | C | I | I |
| Breach determination | C | C | I | C | R/A | I |
| Regulatory notification | C | I | I | C | R/A | C |
| External communication | C | I | I | I | C | R/A |
| Post-incident review | A | R | R | C | C | I |
| Corrective action tracking | A | C | R | R | C | I |

## 7. Exceptions and Escalation

7.1.1 During an active SEV-1 or SEV-2, the Incident Commander may invoke emergency change authority, bypassing normal change controls (MJD-TEC-0008); all such actions are logged and reviewed retroactively within 5 business days.

7.1.2 SEV-1 incidents are escalated to the CISO and executive leadership immediately, and to the Board Risk Committee per the master policy (MJD-SEC-0001).

7.1.3 Disagreement over severity is resolved in favor of the higher severity until evidence supports downgrade (fail safe).

7.1.4 A confirmed AI/retrieval access-control bypass that surfaced out-of-scope content is treated as at least SEV-2 and triggers an immediate control review.

## 8. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent resilience and executive-escalation requirements)
- MJD-SEC-0009 Logging, Monitoring, and SIEM Standard (the detection telemetry feeding Phase 1)
- MJD-SEC-0002 Cryptographic Standard (the emergency key-rotation procedure invoked in containment)
- MJD-SEC-0005 Vulnerability and Patch Management Standard (the emergency patch path during eradication)
- MJD-SEC-0004 Network Segmentation and Zero Trust Architecture (the zone-quarantine containment levers)
- MJD-RSK-0001 Enterprise Risk Management Framework (the risk register receiving post-incident actions)

## 9. Regulatory References

- NIST SP 800-61 Rev 2: computer security incident handling guide (lifecycle phases).
- GLBA Safeguards Rule (16 CFR Part 314.4(h)): incident response program requirement.
- PCI DSS 4.0 Requirement 12.10: incident response plan requirement.
- NYDFS 23 NYCRR 500.17: cybersecurity event notification (72-hour window).
- FFIEC Information Security Booklet: incident response expectations.
- SEC Cybersecurity Disclosure Rules: material incident disclosure obligations.

### 9.5 Tabletop Exercise Requirements

9.5.1 Meridian J.D. conducts incident response tabletop exercises at least twice per year. One exercise annually must simulate a SEV-1 scenario (for example, a ransomware event or a confirmed customer PII breach). The second exercise may simulate a SEV-2 scenario (for example, an account takeover or an API access-control bypass).

9.5.2 Required participants in each tabletop exercise: the SECURITY_ARCHITECT (Incident Commander role), SOC shift lead, at least two SOFTWARE_ENGINEER representatives from production-facing teams, the RISK_ANALYST, the legal and compliance liaison, the communications lead, and a representative from senior management. The CISO participates in or is briefed on the SEV-1 scenario exercise.

9.5.3 Each tabletop exercise is facilitated by an independent party (either an internal security team member not playing an active role, or an external facilitator). The facilitator injects scenario updates in real time to test decision-making under uncertainty and to verify that the escalation chain and notification procedures function correctly.

9.5.4 Within 20 business days of each tabletop exercise, the facilitator produces a findings report that includes: a timeline of decisions made during the exercise, gaps identified in procedures or response capabilities, specific recommended updates to this plan or to supporting procedures, and assigned owners and due dates for each recommendation.

9.5.5 Findings from tabletop exercises feed this plan's next revision and are tracked in the risk register (MJD-RSK-0001). A finding that identifies a material gap in the plan triggers an interim plan update within 30 days, not deferred to the annual review cycle.

## 10. Worked Example: SEV-2 Account Takeover

The following example illustrates the application of this plan for a SEV-2 account takeover affecting an operations analyst's credentials.

**Scenario:** The SIEM generates an alert at 14:22 UTC: "Anomalous login - user OPERATIONS_ANALYST acct opsnl-029 - source IP 203.0.113.42 (geolocation: Eastern Europe) - device not recognized - MFA push accepted." The account's normal login pattern is from a US corporate IP with a recognized device.

**Step 1: Detection and declaration (14:22 UTC).** The SOC duty analyst reviews the alert in the SIEM (MJD-SEC-0009). The login succeeded (MFA was accepted), but the source IP, country, and device fingerprint are all anomalous. The analyst confirms the account is an active operations analyst account with access to INTERNAL and CONFIDENTIAL operational data. The analyst declares a SEV-2 incident, opens an incident record (INC-2026-0318), and pages the on-call CSIRT lead at 14:24 UTC.

**Step 2: CSIRT activation (14:24 UTC).** The on-call CSIRT lead acknowledges at 14:27 UTC (within the 30-minute SEV-2 window) and assumes the Incident Commander role. The SOC analyst opens the incident communication channel and adds the CSIRT lead, the relevant SOFTWARE_ENGINEER, and the RISK_ANALYST.

**Step 3: Evidence preservation (14:29 UTC).** Before any containment action, the SOC analyst exports the SIEM log for account opsnl-029 for the previous 72 hours, capturing all authentication events, data-access events, and API calls. The export is hashed (SHA-256: 4a7f...) and placed on the chain-of-custody form in INC-2026-0318.

**Step 4: Containment (14:33 UTC).** The Incident Commander authorizes containment. The SOFTWARE_ENGINEER executes session revocation for all active sessions for opsnl-029 using the identity platform (MJD-SEC-0003), terminating the anomalous session and any legitimate sessions that may have existed. The account is suspended in the identity system pending investigation. The incident communication channel records the timestamp (14:33 UTC) and the name of the engineer who executed the revocation.

**Step 5: Analysis (14:33 to 16:00 UTC).** The SOC analyst and CSIRT lead review the SIEM logs. The anomalous session accessed two internal operational dashboards (INTERNAL data) and downloaded a report from the loan operations system (INTERNAL data; no customer NPI or CONFIDENTIAL data confirmed). No lateral movement to other accounts is detected. The source IP is confirmed as a known threat actor egress node per threat intelligence. The likely vector is a phishing email that captured the analyst's password; the MFA approval was likely a real-time phishing relay (MFA prompt bombing or adversary-in-the-middle proxy).

**Step 6: Eradication (16:00 UTC).** The SECURITY_ARCHITECT directs a forced password reset for opsnl-029 via an out-of-band communication with the affected analyst (confirming the analyst's identity before providing reset instructions). The analyst confirms they did not approve the MFA prompt intentionally (they were confused by an unexpected push). All registered devices for the account are cleared; re-registration requires in-person verification per MJD-SEC-0003.

**Step 7: Recovery (16:30 UTC).** The account is re-enabled with the new credentials and freshly registered device. The analyst is briefed on the phishing technique used. Heightened monitoring on the account is configured in the SIEM for 14 days.

**Step 8: Notification assessment (14:29 UTC, running through the incident).** The legal and compliance liaison is notified at 14:29 UTC per the breach-notification procedure. After reviewing the evidence, the liaison determines that no customer NPI or RESTRICTED data was accessed; the accessed data was INTERNAL operational data. NYDFS notification is assessed: the event was unauthorized access, which meets the NYDFS definition of a Cybersecurity Event. The NYDFS 72-hour clock starts at 14:22 UTC (the time of determination). The liaison drafts and submits the NYDFS preliminary notification before the 72-hour window closes.

**Step 9: Post-incident review (10 business days later).** The post-incident review finds the root cause to be a real-time phishing proxy attack that bypassed time-based OTP MFA. The corrective action is to require phishing-resistant FIDO2 MFA (per MJD-SEC-0003) for all OPERATIONS_ANALYST accounts accessing CONFIDENTIAL data, with a 30-day migration deadline. The corrective action is assigned to the IAM team and tracked in the risk register (MJD-RSK-0001).

**Outcome:** SEV-2 incident contained within 4 hours. No customer data accessed. NYDFS notification submitted within 72 hours. Root cause eliminated through a targeted MFA upgrade.

## 11. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-06-01 | SECURITY_ARCHITECT | Initial incident response plan. |
| 2.0.0 | 2022-10-20 | SECURITY_ARCHITECT | Added severity model and response-time objectives. |
| 3.0.0 | 2024-04-09 | SECURITY_ARCHITECT | Aligned to NIST 800-61 phases; added breach-notification windows. |
| 4.0.0 | 2025-06-15 | SECURITY_ARCHITECT | Added AI/retrieval incident handling and SEC disclosure assessment. |
| 4.1.0 | 2026-01-30 | SECURITY_ARCHITECT | Annual review; tightened SEV-1 containment to 1 hour. |
