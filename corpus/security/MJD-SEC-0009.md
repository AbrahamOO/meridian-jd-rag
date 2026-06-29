---
doc_id: MJD-SEC-0009
title: Logging, Monitoring, and SIEM Standard
department: SECURITY
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT, SOFTWARE_ENGINEER]
effective_date: 2026-02-12
version: 3.0.0
review_cycle_months: 12
regulatory_refs: ["PCI DSS 4.0 Requirement 10", "NIST SP 800-92 (Log Management)", "NIST SP 800-53 Rev 5 (AU family)", "GLBA Safeguards Rule (16 CFR Part 314)", "SOC 2 CC7", "FFIEC Information Security Booklet"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Logging, Monitoring, and SIEM Standard

## Purpose and Scope

This standard defines what Meridian John Doe Financial (Meridian J.D.) logs, how logs are protected and retained, how they are monitored, and how the Security Information and Event Management (SIEM) platform turns events into detections and alerts. Logging is the foundation of detection, forensics, non-repudiation, and assurance: without complete, tamper-evident, well-retained logs, the institution cannot detect incidents, investigate them, or prove its controls work.

This document is classified CONFIDENTIAL and readable by SECURITY_ARCHITECT and SOFTWARE_ENGINEER, because engineers instrument the systems they build to emit the required telemetry and must know the schema, the redaction rules, and the retention obligations.

Scope covers all production systems, security controls, network devices, cloud services, and applications, including the internal AI and retrieval platform, whose per-request audit record is an in-scope security log. The platform must log every request (including denied and boundary responses) with the redaction rules in Section 3.

## Definitions

**Log.** A timestamped record of an event in a system.

**Audit log.** A durable, broadly readable record of security-relevant events, redacted of sensitive data.

**Debug trace.** A short-lived, access-restricted record that may contain unredacted detail for troubleshooting.

**SIEM.** Security Information and Event Management; the platform that centralizes, correlates, and alerts on logs.

**Detection rule.** Logic that matches log patterns indicating a threat.

**Retention period.** The minimum time a log must be kept before deletion.

**Tamper evidence.** A property whereby modification of a log can be detected.

**Redaction.** Removal or masking of sensitive data (PII, secrets) before durable storage.

**Log forwarder.** An agent or sidecar process that ships log events from a source system to the central SIEM in real time.

**IOC.** Indicator of Compromise: an artifact observed in a log that indicates a potential security incident.

## 1. What Must Be Logged

### 1.1 Mandatory Event Categories

1.1.1 The following are logged on every in-scope system:

| Category | Examples |
|---|---|
| Authentication | Login success/failure, MFA challenge, account lockout (MJD-SEC-0003) |
| Authorization | Access grant/deny, privilege elevation (MJD-SEC-0010), access-control boundary decisions |
| Data access | Reads/writes of CONFIDENTIAL and RESTRICTED data |
| Administrative | Configuration change, account lifecycle, policy change |
| Network | Inter-zone flow allow/deny (MJD-SEC-0004) |
| Cryptographic | Key creation, rotation, destruction, HSM operations (MJD-SEC-0002) |
| Application | Errors, security exceptions, input-validation failures |
| AI/retrieval | One audit record per request: role, redacted query, retrieved doc_ids, boundary decision, latency, cost |

1.1.2 Every log entry includes, at minimum: a timestamp in UTC (RFC 3339), the event type, the principal identity, the source, the target, the outcome, and a correlation/trace identifier.

### 1.2 What Must Never Be Logged

1.2.1 Plaintext passwords, full primary account numbers, full SSNs, cryptographic key material, and session tokens are never written to any log. The PII redactor runs before durable persistence.

1.2.2 For the AI/retrieval platform, the audit log stores the query REDACTED of PII. The raw query exists only in the short-lived, access-restricted debug trace. Any synthetic-PII canary record (MJD-SEC-0008 Section 3.1) appearing in a durable log is a control failure.

1.2.3 An audit record scoped to a role must never reveal the existence of documents outside that role's access scope; the retrieved-doc-id list contains only documents that survived the access filter.

### 1.3 Log Volume and Completeness Metrics

1.3.1 Completeness is measured by comparing the observed event rate per source against a learned baseline event rate. Each log source registered in the SIEM has an expected minimum events-per-hour rate, calibrated during onboarding and updated quarterly. A source whose observed rate falls below 20% of its expected rate for more than 15 consecutive minutes generates a "log gap" alert, routed to the SOC for investigation within 30 minutes.

1.3.2 Sources that produce zero events for any period exceeding 5 minutes (for high-frequency sources such as authentication servers and API gateways) or 60 minutes (for lower-frequency sources such as HSM audit logs) generate an immediate log-gap alert. The SOC confirms whether the silence reflects a legitimate low-activity period or a forwarder failure.

1.3.3 A weekly completeness review is performed by SIEM administrators: all registered sources are checked for log gaps in the prior 7 days, gap durations are quantified, and a coverage report is produced. Coverage reports are retained for 13 months and reviewed by the SECURITY_ARCHITECT monthly. A source with a cumulative gap exceeding 4 hours in any 7-day window is escalated to the SECURITY_ARCHITECT for root-cause resolution.

1.3.4 The coverage percentage metric (percentage of registered sources with no gap exceeding 15 minutes in the measurement period) is reported to the Information Security Steering Committee (MJD-SEC-0001) monthly. The target is 99.5% coverage.

### 1.4 Sensitive-Field Inventory

1.4.1 The following field names trigger automatic PII redaction by the logging pipeline when they appear in any log event payload. This list is normative; additions require SECURITY_ARCHITECT approval and a pipeline update.

| Field name pattern | Data type | Masked output format |
|---|---|---|
| account_number, accountNumber, acct_num | Primary account number | Last 4 digits retained: XXXX-XXXX-XXXX-1234 |
| ssn, social_security_number, tin | Social Security or Tax ID Number | Fully masked: XXX-XX-XXXX |
| card_number, pan, card_pan | Payment card number | Last 4 digits retained: XXXX-XXXX-XXXX-5678 |
| password, passwd, secret, credential | Authentication secret | Fully masked: [REDACTED] |
| api_key, api_token, access_token, bearer_token | API or session credential | Fully masked: [REDACTED] |
| routing_number, routing_no | Bank routing number | Fully masked: [REDACTED] |
| email (in customer context) | Customer email address | Domain retained: XXXXX@example.com |
| dob, date_of_birth, birthdate | Customer date of birth | Fully masked: [REDACTED] |
| cvv, cvc, security_code | Card verification value | Fully masked: [REDACTED] |
| private_key, private_key_pem | Cryptographic private key | Fully masked: [REDACTED] |

1.4.2 Field-name matching is case-insensitive and includes common camelCase, snake_case, and hyphenated variants. The pattern list is applied as a prefix or exact match; a field named account_number_verified is also redacted.

1.4.3 The sensitive-field inventory is tested quarterly against a corpus of synthetic test events that include the field names above, using the MJD-SEC-0008 Section 3.1 canary record as the primary test vector. Test results (pass/fail per field) are recorded and reviewed by the SECURITY_ARCHITECT.

## 2. Log Protection and Retention

### 2.1 Integrity

2.1.1 Logs are write-once and tamper-evident: forwarded immediately to the central SIEM over an encrypted channel, stored in append-only storage, and integrity-protected (hash chaining or equivalent). Local log deletion does not remove the central copy.

2.1.2 Access to the SIEM and to raw logs is restricted and itself logged; viewing security logs is a privileged action (MJD-SEC-0010).

### 2.2 Retention

2.2.1 Minimum retention periods:

| Log type | Minimum retention |
|---|---|
| Security audit logs (authentication, authorization, data access) | 13 months online, 7 years archived |
| AI/retrieval audit records | 13 months |
| Cryptographic and HSM logs | 7 years |
| Network flow logs | 13 months |
| Debug traces (unredacted) | 7 days, access-restricted, then purged |

2.2.2 Retention aligns to the Records Retention Schedule (MJD-CMP-0008) and applicable regulation; the longer of the two governs.

### 2.3 Log Integrity Verification

2.3.1 Hash-chain verification is performed weekly by SIEM administrators on a rolling 7-day window of audit logs. The verification process recomputes the expected hash chain for the sampled window and compares it to the stored chain. Any mismatch is a tamper indicator and triggers an immediate escalation.

2.3.2 The verification run is automated and its result (pass or fail, with the window checked and the SIEM administrator who initiated the run) is recorded in the SIEM operational log, which is itself hash-chained.

2.3.3 A failed integrity verification triggers: immediate notification to the SECURITY_ARCHITECT; quarantine of the affected log segment (access restricted to the SECURITY_ARCHITECT and SOC lead pending investigation); escalation as a potential incident under the Incident Response Plan (MJD-SEC-0006) at SEV-2 or higher; and a forensic review to determine whether log data was altered, deleted, or the hash-chain mechanism failed mechanically.

### 2.4 Log Forwarding Failure Handling

2.4.1 Log forwarders buffer events locally when the connection to the central SIEM is unavailable. The local buffer capacity is sized to retain at least 4 hours of events at peak production load without loss, for every registered log source.

2.4.2 The SLA to restore log forwarding after a detected outage is 2 hours for high-frequency sources (authentication, authorization, AI/retrieval) and 8 hours for lower-frequency sources (HSM, network device syslog). The SOC monitors forwarder health via a heartbeat metric sent every 60 seconds. A missed heartbeat after 3 consecutive intervals generates a forwarding-failure alert.

2.4.3 If log forwarding is not restored within 2 hours for a high-frequency source, the SECURITY_ARCHITECT is notified. If forwarding is not restored within 4 hours for any source, the gap is documented as a coverage exception and the affected source is placed under compensating monitoring (manual spot-checks of local logs at 30-minute intervals) until forwarding is restored.

2.4.4 Events buffered locally during a forwarding outage are forwarded to the SIEM in bulk upon connection restoration. The SIEM accepts backfill events and indexes them by their original event timestamp, not the ingestion timestamp, so correlation across sources remains accurate. The ingestion of backfill events is logged as a distinct event type, allowing auditors to identify which events were delayed.

## 3. Redaction (binding)

3.1.1 The PII redactor masks the following before any durable write: SSNs, full account numbers (last 4 retained at most), full card numbers, email addresses in customer context, and any token or secret pattern.

3.1.2 Redaction is applied at the logging boundary, not after the fact; an unredacted durable write is a control failure even if later corrected.

3.1.3 The redactor is tested against the synthetic-PII canary (MJD-SEC-0008 Section 3.1); the security eval asserts the canary never appears in a durable log or AI answer.

### 3.2 Redaction Testing Cadence

3.2.1 The PII redactor is tested monthly using a formal test suite. The test suite includes: the complete MJD-SEC-0008 Section 3.1 canary record (all five fields: name, account, SSN, routing, and note); a set of synthetic events containing each field name in the sensitive-field inventory (Section 1.4); and at least 10 adversarially crafted variants per field (for example, account numbers formatted with spaces, hyphens, or no separators; SSNs with alternative formatting).

3.2.2 Pass/fail criteria: all fields in the sensitive-field inventory must be masked in every synthetic test event. A single unmasked field in any test event is a test failure.

3.2.3 Test results are reviewed by the SECURITY_ARCHITECT within 5 business days of the test run. A passing result is documented in the compliance evidence repository. A failing result triggers immediate remediation: the redactor is patched and re-tested before the next production deployment.

3.2.4 The test corpus and test results are retained for 13 months to support audits demonstrating continuous operation of the redaction control.

### 3.3 Redaction Failure Response

3.3.1 A redaction failure is confirmed when a sensitive field from the sensitive-field inventory (Section 1.4) is identified in a durable audit log or in any AI/retrieval system output. The synthetic-PII canary (MJD-SEC-0008 Section 3.1) appearing in a durable log is always treated as a confirmed redaction failure.

3.3.2 Immediate steps on confirmation of a redaction failure:

Step 1 (Scope identification): The SOC and SIEM administrators identify the time window of the failure (from the earliest unredacted event to the time the redactor was fixed), the log sources affected, and the specific sensitive fields that were written in plaintext. This scoping must be completed within 2 hours of confirmation.

Step 2 (Log quarantine): The affected log segments are marked read-only (already append-only in normal operation) and access is restricted to the SECURITY_ARCHITECT and SOC lead pending investigation. No additional personnel access the quarantined logs without SECURITY_ARCHITECT authorization.

Step 3 (Incident declaration): A redaction failure affecting customer NPI or any RESTRICTED field is declared as a security incident under the Incident Response Plan (MJD-SEC-0006). The severity is assessed based on the data type and volume: SSNs or full account numbers for multiple customers warrant at minimum SEV-2; confirmed exposure to unauthorized parties is SEV-1. The incident declaration triggers breach notification assessment.

Step 4 (Redactor fix and re-test): The redactor is patched to close the failure mode. The fix is validated using the full test suite from Section 3.2 before re-deployment. The fix is deployed under the emergency change path (MJD-TEC-0008).

Step 5 (Post-incident review): Within 10 business days, a post-incident review is conducted per MJD-SEC-0006 Section 3.5.3. The corrective action includes updating the sensitive-field inventory if the failure revealed an uncovered field pattern, and increasing testing frequency to weekly for a minimum of 90 days following a failure.

## 4. Monitoring and Detection

### 4.1 SIEM Correlation

4.1.1 All logs are centralized in the SIEM, normalized to a common schema, and correlated across sources to detect multi-step attacks.

4.1.2 Detection rules align to the threat model (MJD-SEC-0007) and cover at minimum: brute-force and credential stuffing, privilege escalation, anomalous data access, lateral movement (unexpected inter-zone flows), data exfiltration, cryptographic anomalies, and AI/retrieval access-control bypass attempts.

### 4.2 Alerting

4.2.1 Alerts are severity-ranked and routed to the SOC. High-severity alerts page on-call within the response objectives of the Incident Response Plan (MJD-SEC-0006).

4.2.2 Detection coverage is reviewed quarterly; gaps against the threat model are tracked as findings.

4.2.3 Alert quality is managed deliberately: each detection rule has an owner, a documented rationale, and a tuned threshold. A rule whose false-positive rate degrades analyst response is tuned or retired, because alert fatigue is itself a security risk.

### 4.3 Use Cases for the AI/Retrieval Platform

4.3.1 The SIEM ingests the per-request audit record from the retrieval platform and runs dedicated detections:

| Detection | Signal |
|---|---|
| Access-control probing | A single principal generating many boundary/denied responses in a short window |
| Role spoofing attempt | Requests asserting roles the principal is not entitled to |
| Injection attempt | Queries matching known prompt-injection patterns flagged by the input guardrail |
| Cost or volume abuse | Anomalous query volume or token/cost spikes from one source |
| Citation anomaly | Generated citations stripped at re-validation, indicating an attempted out-of-scope reference |

4.3.2 A confirmed access-control bypass detection is escalated to the SOC and handled as at least a SEV-2 incident (MJD-SEC-0006).

### 4.4 SIEM Use-Case Lifecycle

4.4.1 A detection rule follows a defined lifecycle from proposal to retirement. No rule is deployed to production without passing through all required stages.

Propose: Any member of the security team may propose a new detection rule by submitting a use-case ticket containing: the threat it detects (with reference to the threat model, MJD-SEC-0007); the log source and fields it queries; the matching logic and threshold; the expected alert volume; and the expected false-positive rate. The proposal is reviewed by the SECURITY_ARCHITECT.

Review: The SECURITY_ARCHITECT and SOC lead review the proposal for: alignment to the threat model; feasibility given available log sources; expected quality (false-positive risk); and operational impact (SOC workload). Approved proposals advance to testing.

Test: The rule is deployed in the SIEM in a "simulate" mode (alerts generated but not paged) for a minimum of 14 days. During this period, the SOC triages all simulated alerts to measure the actual false-positive rate. Rules with a false-positive rate above 10% are tuned or rejected.

Deploy: After successful simulation, the rule is promoted to active status with paging enabled. The deployment is recorded with the rule version, deployment date, approver, and expected alert volume.

Operate and tune: Active rules are reviewed quarterly. Rules with a false-positive rate above 5% over a rolling 90-day window are flagged for tuning. Tuned rules re-enter the test stage for at least 7 days before returning to active status.

Retire: A rule is retired when the threat it detects is no longer applicable (for example, a system it monitored has been decommissioned) or when a superior rule supersedes it. Retired rules are archived with their retirement rationale and are not deleted, to support historical audit queries.

### 4.5 Mean Time to Detect Targets

4.5.1 Mean Time to Detect (MTTD) is defined as the elapsed time from when a security incident actually begins (as determined by forensic evidence in the post-incident review) to when the SIEM generates the first alert for that incident. MTTD is measurable only in hindsight, using post-incident timeline data.

4.5.2 MTTD targets by severity:

| Severity | MTTD target | Measurement method |
|---|---|---|
| SEV-1 | <= 15 minutes | Forensic onset time vs. SIEM first-alert time, from post-incident review |
| SEV-2 | <= 30 minutes | Same as above |
| SEV-3 | <= 2 hours | Same as above |
| SEV-4 | <= 8 hours | Same as above |

4.5.3 MTTD is computed from every closed SEV-1, SEV-2, and SEV-3 incident with sufficient forensic data to determine onset time. The rolling 12-month average MTTD by severity is reported to the Information Security Steering Committee (MJD-SEC-0001) quarterly. A sustained MTTD above target for a given severity for two consecutive quarters triggers a detection-improvement plan with the SECURITY_ARCHITECT as owner.

4.5.4 Detection gaps identified during post-incident reviews (cases where no SIEM alert was generated for an incident that subsequently required manual discovery or external notification) are tracked as detection-coverage findings in the risk register (MJD-RSK-0001) and prioritized for new use-case development.

### 4.6 Threat Intelligence Integration

4.6.1 External IOC feeds are ingested from the following sources: FS-ISAC threat intelligence feeds (financial sector-specific IOCs); CISA Known Exploited Vulnerabilities (KEV) catalog for CVE-to-IP/domain correlations (MJD-SEC-0005); commercial threat intelligence subscription (IP reputation, domain reputation, hash reputation); and government sector alerts (FBI, FinCEN advisories).

4.6.2 IOCs are ingested into the SIEM threat intelligence platform on a daily automated basis. Each IOC feed is de-duplicated against existing IOCs using an exact-match hash before ingestion. IOCs with conflicting verdicts across feeds are resolved by the most authoritative source (government and FS-ISAC feeds take precedence over commercial feeds). Stale IOCs (those not refreshed by any feed in more than 90 days) are automatically expired and removed from active correlation.

4.6.3 Active IOCs are applied to SIEM correlation rules to enrich detection. Network flow logs (MJD-SEC-0004 zone rules) are correlated against IP reputation IOCs in real time; a connection to or from a known-malicious IP generates a high-priority alert regardless of the destination port or protocol. File hash IOCs are applied to endpoint detection events. Domain IOCs are applied to DNS query logs.

4.6.4 New IOCs from a government advisory or FS-ISAC alert are manually reviewed by the SOC within 4 hours of receipt and applied to SIEM correlation rules within 24 hours. The SECURITY_ARCHITECT is notified of government advisories affecting the financial sector on the same day of receipt.

## 5. Time Synchronization and Schema

5.1.1 All systems synchronize clocks to an authoritative time source; accurate, consistent timestamps are mandatory for correlation and forensics. A system whose clock drifts beyond tolerance is a finding.

5.1.2 Logs are normalized to a common event schema at ingestion so that events from heterogeneous sources can be correlated on shared fields (principal, source, target, outcome, trace id).

### 5.3 Log Schema Reference

5.3.1 The following normative event schema defines the required fields for all audit log events ingested by the SIEM. Systems must map their native event fields to this schema at the log forwarder or SIEM ingestion layer. Fields marked "required" must be present in every event; fields marked "conditional" are required when the event type involves the specified resource or actor.

| Field name | Type | Required / Conditional | Description |
|---|---|---|---|
| timestamp | string (RFC 3339 UTC) | Required | The exact time the event occurred, in UTC, with millisecond precision. Example: 2026-03-15T14:22:07.342Z |
| event_type | string (enum) | Required | A controlled-vocabulary event type from the approved event taxonomy. Examples: AUTH_LOGIN_SUCCESS, AUTHZ_ACCESS_DENY, DATA_READ, ADMIN_CONFIG_CHANGE, CRYPTO_KEY_ROTATE, APP_SECURITY_EXCEPTION, AI_QUERY |
| principal_id | string | Required | The unique identifier of the acting principal (user account ID, service account ID, or machine identity). Never a display name; always the immutable identifier from the identity system (MJD-SEC-0003) |
| source_ip | string (IPv4 or IPv6) | Required | The originating IP address of the request or action. For server-to-server calls, the calling service's IP |
| target_resource | string | Required | The resource acted upon: for data-access events, the data store name and object identifier; for API calls, the endpoint path and HTTP method; for AI/retrieval, the platform identifier |
| outcome | string (enum) | Required | One of: SUCCESS, FAILURE, BOUNDARY (for access-control boundary decisions), ERROR |
| trace_id | string | Required | A unique correlation identifier linking all log events from the same request or transaction chain. Must be propagated across service boundaries via the W3C Trace Context header |
| classification_touched | string (enum) | Conditional (required for data-access events) | The classification of the data accessed or attempted: PUBLIC, INTERNAL, CONFIDENTIAL, or RESTRICTED. Required for all events in the data-access category (MJD-SEC-0008) |
| session_id | string | Conditional (required for authentication events) | The session identifier established at login, linking all events in a user session |
| elevation_request_id | string | Conditional (required for privilege-elevation events) | The PAM broker request identifier for the JIT elevation, linking this event to the elevation approval record (MJD-SEC-0010) |
| query_redacted | string | Conditional (required for AI/retrieval events) | The user query, redacted of all PII per Section 3. The raw query is never written to the audit log |
| retrieved_doc_ids | array of strings | Conditional (required for AI/retrieval events) | The list of document identifiers that survived the access filter and were returned to the caller. Does not include documents filtered out by the access control |
| boundary_decision | string (enum) | Conditional (required for AI/retrieval and AUTHZ events) | One of: ALLOWED, DENIED, BOUNDARY_RESPONSE. BOUNDARY_RESPONSE indicates the request was processed but one or more requested resources were excluded from the response due to access-control enforcement |
| latency_ms | integer | Conditional (required for AI/retrieval events) | End-to-end request latency in milliseconds |

## 6. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this standard, the log schema, the redaction rules, and detection coverage. |
| SOFTWARE_ENGINEER | Instruments systems to emit required, correctly redacted telemetry. |
| SOC | Monitors the SIEM, triages alerts, investigates. |
| SIEM administrators | Operate the platform, manage retention and integrity controls. |

## 7. Exceptions and Escalation

7.1.1 Exceptions to a logging or retention requirement require SECURITY_ARCHITECT approval, a compensating control, and an expiry no later than 12 months.

7.1.2 A confirmed unredacted PII write, log tampering, or a logging gap on a CONFIDENTIAL/RESTRICTED system is escalated as a potential incident (MJD-SEC-0006).

7.1.3 A detection-coverage gap against a Critical threat is escalated to the SECURITY_ARCHITECT and tracked in the risk register (MJD-RSK-0001).

7.1.4 Common exception scenarios and approval paths:

| Exception scenario | Approval authority | Compensating control required |
|---|---|---|
| Log source cannot forward in real time (legacy system with batch-only syslog) | SECURITY_ARCHITECT | Manual log review at 4-hour intervals; local log integrity check; batch forward at least every 4 hours |
| Retention below 13 months for a non-PCI log type (storage cost constraint) | SECURITY_ARCHITECT | Compensating retention in cold archive with verified retrieval capability; documented retrieval SLA |
| Sensitive field not yet covered by redactor (newly deployed system with novel field names) | SECURITY_ARCHITECT; exception valid for 30 days maximum | Debug traces disabled for the affected field until redactor is updated; field access restricted to SOC |
| SIEM coverage gap during planned maintenance window | SOC lead | Manual monitoring during window; no longer than 4 hours; SECURITY_ARCHITECT notified |

## 8. Worked Example: Instrumenting a Payment API

The following example walks through how a SOFTWARE_ENGINEER instruments a new payment API to meet the requirements of this standard.

**Scenario:** An engineer is building a new payment disbursement API endpoint that accepts a request containing a customer account number, a disbursement amount, and a destination routing number, validates the request, and initiates a disbursement transaction. The endpoint processes CONFIDENTIAL data (MJD-SEC-0008) and must emit a compliant audit log event.

**Step 1: Identify required event categories.** The endpoint involves: authentication (the caller must present a valid token); authorization (the caller must have the DISBURSEMENT entitlement); data access (reading and writing CONFIDENTIAL transaction data). All three categories require audit log events per Section 1.1.

**Step 2: Instrument the event.** The engineer adds a logging call at the completion of the request (not at receipt, to capture the outcome). The event is constructed using the log schema from Section 5.3:

- timestamp: 2026-03-15T14:22:07.342Z (the completion time of the request, in UTC)
- event_type: DATA_WRITE (the disbursement record is written to the transaction store)
- principal_id: svc-acct-disbursement-caller-88a2 (the service account ID, not a display name)
- source_ip: 10.20.5.17 (the calling service's IP in the Application Zone)
- target_resource: txn-store/disbursements (the data store and collection)
- outcome: SUCCESS
- trace_id: 4bf92f3577b34da6a3ce929d0e0e4736 (propagated from the W3C Trace Context header)
- classification_touched: CONFIDENTIAL
- session_id: (not applicable; this is a service-to-service call, no user session)

**Step 3: Apply redaction.** The request body contains the customer account number (0000-1111-2222-3333) and routing number (110000000). The logging library's PII redactor intercepts the event before durable write. It identifies "account_number" and "routing_number" in the event payload and applies the masking rules from Section 1.4. The account number is masked to XXXX-XXXX-XXXX-3333. The routing number is fully masked to [REDACTED]. The disbursement amount (not a PII field) is retained unmasked. The redacted event is written to the durable audit log. The unredacted request detail is written only to the debug trace, which expires in 7 days.

**Step 4: Forward to the SIEM.** The log forwarder on the Application Zone host picks up the audit log event within seconds and forwards it to the SIEM over an encrypted channel (TLS 1.3). The SIEM ingests the event, maps it to the normalized schema, and indexes it by timestamp and trace_id. The trace_id allows the SOC to correlate this disbursement write event with the upstream authentication event and any downstream events from the routing system, all within a single trace.

**Step 5: SIEM detection.** The SIEM applies active detection rules to the ingested event. The disbursement write is matched against the anomalous-bulk-disbursement rule (which fires if a single principal_id initiates more than 50 disbursement writes in a 5-minute window). In this case, a single disbursement is written; no alert fires.

**Outcome:** The engineer has produced a compliant, redacted audit event that is tamper-evidently stored, forwarded to the SIEM, and correlated with other events in the same transaction. The account number and routing number are not present in the durable log. The event is queryable by the SOC for 13 months.

## 9. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent assurance and monitoring requirements)
- MJD-SEC-0006 Incident Response Plan (the consumer of alerts generated by this standard)
- MJD-SEC-0008 Data Classification and Handling Standard (the synthetic-PII canary the redactor is tested against)
- MJD-SEC-0010 Privileged Access Management (PAM) Policy (the privileged-access controls on log viewing)
- MJD-SEC-0007 Threat Modeling Standard (the threat model the detection rules align to)
- MJD-CMP-0008 Records Retention Schedule (the retention periods reconciled in Section 2.2)

## 10. Regulatory References

- PCI DSS 4.0 Requirement 10: log and monitor all access to system components and cardholder data.
- NIST SP 800-92: guide to computer security log management.
- NIST SP 800-53 Rev 5 (AU family): audit and accountability controls.
- GLBA Safeguards Rule (16 CFR Part 314): monitoring and logging of access to customer information.
- SOC 2 CC7: system operations, monitoring, and incident detection.
- FFIEC Information Security Booklet: logging and monitoring expectations.

## 11. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2021-05-20 | SECURITY_ARCHITECT | Initial logging and SIEM standard. |
| 2.0.0 | 2023-03-11 | SECURITY_ARCHITECT | Added redaction rules and 13-month retention baseline. |
| 2.1.0 | 2024-10-07 | SECURITY_ARCHITECT | Added AI/retrieval audit-record category. |
| 3.0.0 | 2026-02-12 | SECURITY_ARCHITECT | Annual review; added tamper-evidence and detection-coverage review. |
