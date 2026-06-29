---
doc_id: MJD-SEC-0004
title: Network Segmentation and Zero Trust Architecture
department: SECURITY
doc_type: STANDARD
classification: RESTRICTED
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT]
effective_date: 2026-02-05
version: 4.0.0
review_cycle_months: 12
regulatory_refs: ["NIST SP 800-207 (Zero Trust Architecture)", "PCI DSS 4.0 Requirement 1", "NIST SP 800-53 Rev 5 (SC family)", "FFIEC Information Security Booklet", "CISA Zero Trust Maturity Model v2"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Network Segmentation and Zero Trust Architecture

## Purpose and Scope

This standard defines the network segmentation model and the zero-trust architecture of Meridian John Doe Financial (Meridian J.D.). It specifies the trust zones, the segmentation boundaries, the policy enforcement points, the service-to-service authentication model, and the rules that govern every flow between zones. It is the authoritative topology of the bank's production network and the binding source for what may communicate with what, under what identity, and with what encryption.

This document is classified RESTRICTED and readable only by the SECURITY_ARCHITECT role. The trust-zone topology is an operational secret: it maps the attack surface and the internal segmentation that contains lateral movement, so it is one of the three RESTRICTED security documents that form the sharpest access boundary in the corpus. It is invisible to OPERATIONS_ANALYST, SOFTWARE_ENGINEER, and every other role. Engineers receive only the specific firewall and service-mesh policies that apply to their workloads, through a scoped release approved by the SECURITY_ARCHITECT.

Scope covers all production, staging, and disaster-recovery networks, cloud virtual networks, the service mesh, ingress and egress controls, micro-segmentation, and remote access. It explicitly includes the network placement and segmentation of internal AI and retrieval systems, which sit in the application data zone and must reach the index and the KMS only through authenticated, encrypted, policy-controlled flows.

## Definitions

**Zero trust.** A security model in which no principal or network location is implicitly trusted; every request is authenticated, authorized, and encrypted regardless of origin.

**Trust zone.** A logically isolated network segment with a defined sensitivity and an explicit allowlist of permitted flows.

**Micro-segmentation.** Fine-grained segmentation at the workload level, isolating individual services rather than only network ranges.

**Policy enforcement point (PEP).** The component that enforces an access decision on a flow (firewall, service-mesh sidecar, API gateway).

**Policy decision point (PDP).** The component that evaluates policy and returns an allow or deny decision.

**East-west traffic.** Communication between services inside the data center or cloud.

**North-south traffic.** Communication between external clients and internal services.

**Default-deny.** A firewall posture in which all flows are denied unless explicitly allowed.

**SPIFFE.** The Secure Production Identity Framework for Everyone: an open standard for workload identity using X.509 SVIDs.

**mTLS.** Mutual Transport Layer Security: both client and server present and validate certificates.

## 1. Zero Trust Principles

### 1.1 Core Tenets

1.1.1 No implicit trust is granted based on network location. Being inside the perimeter confers no access.

1.1.2 Every flow is authenticated with a strong identity, authorized against explicit policy, and encrypted in transit using the suites in the Cryptographic Standard (MJD-SEC-0002).

1.1.3 Access is least-privilege and per-session. Authorization is re-evaluated continuously, not granted once and trusted indefinitely.

1.1.4 The architecture assumes breach: segmentation and monitoring are designed to contain and detect an attacker who has already obtained a foothold.

### 1.2 Policy Architecture

1.2.1 The PDP centrally evaluates flow policy from declarative rules. PEPs (firewalls, service-mesh sidecars, API gateways) enforce the decision at the boundary of each zone and at each workload.

1.2.2 Policy is expressed as code, version controlled, peer reviewed, and deployed through the change pipeline (MJD-TEC-0008). No flow rule is changed manually in production.

## 2. Trust Zones

### 2.1 Zone Model

2.1.1 The production network is divided into the following trust zones, in ascending sensitivity:

| Zone | Contents | Default posture |
|---|---|---|
| Z0 Public edge | CDN, WAF, public load balancers | Default-deny, north-south only |
| Z1 DMZ | Public API gateways, reverse proxies | Default-deny |
| Z2 Application | Stateless application services, AI/retrieval services | Default-deny, mTLS east-west |
| Z3 Data | Databases, object storage, vector index | Default-deny, no direct external reachability |
| Z4 Secrets and crypto | KMS, HSM, secrets manager | Default-deny, quorum-controlled, no general workload reachability |
| Z5 Management | Bastion, CI/CD runners, observability | Default-deny, privileged-only via PAM |

2.1.2 Flows always move toward equal or lower sensitivity only through an explicit allowlist. A Z2 service may reach Z3 only for the specific datastore it owns. No workload reaches Z4 except through the brokered KMS and secrets API.

2.1.3 The cardholder data environment is a dedicated sub-segment of Z3 with its own firewall boundary, satisfying PCI DSS network segmentation.

### 2.2 Inter-Zone Flow Rules

2.2.1 All inter-zone flows are default-deny. A flow is permitted only by an approved, peer-reviewed rule naming the source identity, the destination service, the port, and the protocol.

2.2.2 Z3 (Data) and Z4 (Secrets and crypto) have no outbound internet access. Egress from Z2 is restricted to an allowlisted egress proxy.

2.2.3 Management plane (Z5) access requires privileged elevation through the PAM workflow (MJD-SEC-0010) and a bastion; there is no direct administrative path from a workstation to production.

### 2.3 Zone-to-Zone Allowlist Register

2.3.1 The SECURITY_ARCHITECT maintains a Zone-to-Zone Allowlist Register. Every permitted inter-zone flow must have an entry in this register before the corresponding firewall or mesh rule is deployed. The register is version-controlled and changes require peer review by a second SECURITY_ARCHITECT before merge.

2.3.2 Required fields for each allowlist entry:

| Field | Description |
|---|---|
| Flow ID | Unique identifier (e.g., FLOW-0042) |
| Source zone | Z0 through Z5 |
| Source identity | SPIFFE ID, role, or CIDR (CIDR entries require SECURITY_ARCHITECT justification) |
| Destination zone | Z0 through Z5 |
| Destination service | Service name and port |
| Protocol | TCP / UDP / HTTP / gRPC |
| Encryption required | mTLS / TLS / none (none is only permitted for Z0 CDN to WAF on the same host) |
| Identity auth required | Yes / No (Yes for all Z2 to Z3 and above) |
| Approved by | SECURITY_ARCHITECT name |
| Approval date | ISO 8601 |
| Review expiry | 12 months from approval date for standard flows; 90 days for exceptions |

2.3.3 Sample allowlist entries (illustrative, fictional):

| Flow ID | Source zone / identity | Destination zone / service | Port | Protocol | mTLS | Review expiry |
|---|---|---|---|---|---|---|
| FLOW-0001 | Z1 API gateway (spiffe://mjd/api-gateway) | Z2 Account service (spiffe://mjd/account-svc) | 8443 | gRPC | Yes | 2027-02-05 |
| FLOW-0012 | Z2 Account service (spiffe://mjd/account-svc) | Z3 Account DB (spiffe://mjd/account-db) | 5432 | TCP | Yes | 2027-02-05 |
| FLOW-0031 | Z2 RAG retrieval service (spiffe://mjd/rag-retrieval) | Z3 Vector index (spiffe://mjd/vector-index) | 8443 | gRPC | Yes | 2027-02-05 |
| FLOW-0032 | Z2 RAG retrieval service (spiffe://mjd/rag-retrieval) | Z4 KMS API (spiffe://mjd/kms-api) | 443 | HTTPS | Yes | 2026-05-05 |

2.3.4 Flows with a review expiry within 30 days generate an automated reminder to the SECURITY_ARCHITECT. An expired flow entry is disabled by the policy-as-code pipeline until the entry is renewed. Renewal requires the same peer-review process as a new entry.

### 2.4 Cardholder Data Environment Sub-Segment

2.4.1 The cardholder data environment (CDE) is a dedicated sub-segment of Z3. It has its own dedicated firewall boundary (a separate security group or network ACL layer) in addition to the Z3 boundary controls. No traffic from Z2 reaches the CDE unless it is specifically named in the CDE allowlist, which is a separate register from the main Zone-to-Zone Allowlist.

2.4.2 The CDE sub-segment hosts: the payment card tokenization service, the PAN vault, and the card transaction processing integrations. No service in the CDE sub-segment is reachable from any zone other than Z2 payment processing services and Z5 management via PAM.

2.4.3 The CDE boundary is reviewed quarterly by the SECURITY_ARCHITECT to confirm PCI DSS network segmentation is maintained. The quarterly review documents: (a) all services in the CDE sub-segment; (b) all permitted flows in and out; (c) any new services added since the last review. The review is retained as PCI DSS audit evidence per MJD-CMP-0008.

2.4.4 Any proposed change to the CDE boundary (adding a service, changing a flow) requires written approval from both the SECURITY_ARCHITECT and the PCI compliance lead before the change is deployed.

## 3. Micro-Segmentation and Service Mesh

3.1.1 Within Z2, workloads are micro-segmented: each service can communicate only with the specific peers its policy allows, enforced by service-mesh sidecars.

3.1.2 Service-to-service communication uses mutual TLS (mTLS) with short-lived workload certificates rotated every 30 days per MJD-SEC-0002 Section 5.2. Each service presents a SPIFFE-style verifiable identity; the mesh authorizes the flow against policy before forwarding.

3.1.3 Plaintext east-west traffic inside production is prohibited. A service that cannot present a valid workload certificate is denied (fail closed).

### 3.4 Certificate Lifecycle Management

3.4.1 Workload certificates are issued by the internal certificate authority (CA) integrated with the service mesh control plane. The CA is located in Z4 and is accessible only through the brokered KMS API. No workload requests certificates directly from the CA; the mesh control plane brokers all issuance.

3.4.2 Certificate rotation cadence: workload certificates are issued with a 30-day validity period. The mesh control plane initiates rotation at day 25 (5 days before expiry). If rotation fails, the control plane retries every 5 minutes until day 29. If the certificate is not renewed by the end of day 29 (1 day before expiry), the workload is moved to a quarantine state: it cannot initiate outbound connections to other mesh services, and inbound connections from healthy peers are refused. This is fail-closed behavior: a workload with a stale or expired certificate loses connectivity rather than gaining it.

3.4.3 Certificate revocation: if a workload is compromised or a certificate must be revoked before expiry, the SECURITY_ARCHITECT initiates revocation through the CA management interface in Z4. The mesh control plane propagates the revocation to all PEPs within 60 seconds of the CA updating the CRL or OCSP status. All revocations are logged to the SIEM (MJD-SEC-0009) as a High priority event.

3.4.4 Certificate expiry events generate a SIEM alert at T-5 days (rotation initiation), T-1 day (quarantine threshold), and T-0 (expiry). A workload in quarantine due to certificate failure generates an immediate incident under MJD-SEC-0006 if it handles production traffic.

### 3.5 Service Identity Registry

3.5.1 Every service that participates in the mesh must be registered in the Service Identity Registry before it can receive a SPIFFE identity and workload certificate. The registry is maintained by the SECURITY_ARCHITECT and is the authoritative source for the SPIFFE trust domain.

3.5.2 Registry entry fields: service name, owning team, SPIFFE ID (spiffe://mjd/[service-name]), zone placement (Z2, Z3, etc.), permitted inbound peers (list of SPIFFE IDs), permitted outbound peers (list of SPIFFE IDs), and registration date.

3.5.3 A service that is not in the registry cannot receive a workload certificate from the control plane. The mesh control plane consults the registry on each certificate issuance request and rejects requests for unregistered services.

3.5.4 Registry changes (new service, modified peer list, decommission) require a pull request to the registry repository with SECURITY_ARCHITECT approval. The PR is linked to the Zone-to-Zone Allowlist entry for the corresponding flow. Registry entries for decommissioned services are flagged as Retired and the mesh control plane ceases issuing certificates for them; existing certificates for retired services are revoked within 24 hours.

## 4. North-South Controls

4.1.1 All inbound public traffic terminates at the Z0 edge behind a web application firewall and DDoS protection, then passes to the Z1 API gateway, which authenticates and rate-limits before any Z2 service is reached.

4.1.2 TLS is terminated and re-originated at policy boundaries so that traffic is inspected and re-encrypted; no end-to-end plaintext segment exists.

4.1.3 The API gateway enforces authentication (OIDC per MJD-TEC-0003), schema validation, and per-client rate limits before forwarding.

### 4.4 Rate Limiting and DDoS Controls at the Edge

4.4.1 The Z0 edge enforces DDoS protection in three tiers:

- **Network-layer (L3/L4) protection**: Always-on volumetric DDoS scrubbing at the CDN/anycast layer. Capacity threshold: the CDN provider's scrubbing capacity (contracted minimum: 1 Tbps). Attacks below 10 Gbps are absorbed transparently. Attacks above 10 Gbps trigger automatic traffic diversion to scrubbing centers.
- **Application-layer (L7) WAF rate limiting**: The WAF enforces per-IP rate limits at the edge before traffic reaches Z1. Default thresholds: 100 HTTP requests per second per IP for unauthenticated endpoints; 500 requests per second per authenticated client-id. Breaches trigger a 429 response and, if sustained for more than 60 seconds from the same IP, a 10-minute block.
- **API gateway rate limiting (Z1)**: The API gateway enforces per-client rate limits based on the authenticated client-id in the OIDC token. Default limits: 60 requests per minute per client for standard API endpoints; 10 requests per minute per client for high-sensitivity endpoints (payments, account modification). Rate limit configuration is in the API gateway policy-as-code and changes require SECURITY_ARCHITECT approval.

4.4.2 WAF rule categories active at the Z0/Z1 boundary: OWASP Core Rule Set (CRS); custom rules for Meridian J.D. API schema enforcement; IP reputation blocking (threat intelligence feed updated daily); geographic restriction rules as directed by the SECURITY_ARCHITECT; and bot-detection rules.

4.4.3 DDoS events are detected by the edge layer and forwarded to the SIEM (MJD-SEC-0009) within 60 seconds. A sustained DDoS event generating more than 1,000 blocked requests per minute is automatically classified as a High severity incident and paged to the SOC.

### 4.5 API Gateway Authentication Enforcement

4.5.1 The Z1 API gateway validates OIDC access tokens on every inbound request to Z2 services. Validation steps: (a) verify the JWT signature against the IdP's JWKS endpoint (cached with a 5-minute TTL); (b) verify the token is not expired (checking exp claim with a 30-second clock skew tolerance); (c) verify the aud claim matches the API gateway's registered audience; (d) verify the required scope claim is present for the requested endpoint.

4.5.2 Token lifetime enforcement: access tokens with a remaining lifetime of less than 60 seconds are rejected to prevent race-condition attacks on near-expiry tokens. Clients must obtain a fresh token before expiry using the refresh token flow.

4.5.3 Scope enforcement: each API endpoint is mapped to a required scope in the API gateway configuration. A token lacking the required scope receives a 403 response with a WWW-Authenticate header describing the missing scope. The scope-to-endpoint mapping is maintained as policy-as-code and changes require SECURITY_ARCHITECT review.

4.5.4 Token validation failures (invalid signature, expired, missing scope) are logged to the SIEM at INFO severity. A burst of more than 50 validation failures from a single client-id within 60 seconds is escalated to WARN and correlated as a potential credential stuffing or token replay attempt.

## 5. Remote and Administrative Access

5.1.1 Remote workforce access uses a zero-trust network access broker, not a flat VPN. Each application is reached individually after device-posture and identity checks; access to one application never implies network access to others.

5.1.2 Administrative access to production is exclusively through the PAM-brokered bastion in Z5 with just-in-time elevation and full session recording (MJD-SEC-0010).

### 5.3 Zero-Trust Network Access Broker Controls

5.3.1 The ZTNA broker evaluates device posture on every connection attempt. A device that fails a posture check is placed in a quarantine zone with access restricted to a remediation portal only. Posture checks evaluate:

| Posture check | Pass criteria | Fail action |
|---|---|---|
| OS version | Within 2 major patch versions of the current OS release | Quarantine; user directed to OS update |
| Disk encryption | Full-disk encryption enabled and verified by MDM | Quarantine; security advisory sent to user and manager |
| MDM enrollment | Device is enrolled in and compliant with the MDM policy | Quarantine; MDM enrollment link sent |
| Patch status | No Critical OS or browser patches pending for more than 7 days | Quarantine; patch required before access restored |
| Endpoint protection | Approved endpoint protection agent running and definitions current | Quarantine; agent restart required |

5.3.2 Posture checks are re-evaluated at session initiation and at each 30-minute interval during a session. A device that fails a mid-session posture check has its session terminated immediately and the user is sent to the remediation portal. The session termination event is logged to the SIEM.

5.3.3 A device in quarantine cannot access any CONFIDENTIAL or RESTRICTED resource. Quarantine duration is indefinite until posture is restored. The identity operations team is notified of devices that remain in quarantine for more than 24 hours.

5.3.4 Contractor and third-party devices are evaluated against the same posture checks. Third parties who cannot meet the posture requirements must access Meridian J.D. systems through a SECURITY_ARCHITECT-approved virtual desktop infrastructure (VDI) session; no Meridian J.D. data is downloaded to the non-compliant device.

## 6. Monitoring and Detection

6.1.1 All inter-zone flows are logged and streamed to the SIEM (MJD-SEC-0009). Denied flows are correlated to detect reconnaissance and lateral-movement attempts.

6.1.2 Network detection rules align to the threat model (MJD-SEC-0007); unexpected east-west connections, egress to unknown destinations, and Z3/Z4 access anomalies generate high-severity alerts.

6.1.3 A baseline of expected flows is maintained as policy-as-code; any flow not in the baseline is, by definition, a deny and a detection event. Because the network is default-deny, a denied flow is signal, not noise: a cluster of denied flows from a single source is a reconnaissance indicator routed to the SOC.

### 6.2 Continuous Verification

6.2.1 Segmentation is verified continuously, not assumed. Automated reachability tests run on a schedule to confirm that prohibited paths (for example Z2 to Z4 directly, or Z3 to the internet) remain blocked. A test that finds an unexpected open path is a Critical finding handled under MJD-SEC-0005.

6.2.2 Penetration testing (MJD-SEC-0005 Section 1.1.4) includes an explicit lateral-movement objective: starting from a simulated foothold in Z2, the tester attempts to reach Z3 and Z4. Success is a release-blocking finding.

### 6.3 Detection Playbooks for Network Events

6.3.1 The following detection playbooks are maintained by the SOC and reviewed annually by the SECURITY_ARCHITECT. Each playbook is triggered by a specific SIEM rule.

**Playbook NET-001: Lateral Movement from Z2**

- Detection signal: A Z2 service initiates a connection to a Z3 or Z4 resource that is not in the Zone-to-Zone Allowlist for that service's SPIFFE ID. The service mesh PEP denies the connection and logs DENY with the source SPIFFE ID and destination address.
- SIEM correlation rule: more than 3 DENY events from the same source SPIFFE ID to different Z3 or Z4 destinations within 5 minutes.
- SOC action: (1) Identify the source service and its owning team. (2) Determine whether the connection attempt is legitimate but misconfigured (missing allowlist entry) or anomalous. (3) If anomalous, isolate the source service by removing it from the mesh (mesh control plane quarantine). (4) Notify the SECURITY_ARCHITECT within 15 minutes.
- Escalation path: SECURITY_ARCHITECT immediately; CISO if service holds customer NPI; incident opened under MJD-SEC-0006 at High or Critical severity depending on data sensitivity.

**Playbook NET-002: Unexpected Z3 Egress**

- Detection signal: Any outbound connection from Z3 to the internet or to a zone other than Z2 is detected by the network-level egress filter. Z3 has no permitted internet egress by design; any such connection is a policy violation.
- SIEM correlation rule: any egress packet from the Z3 IP range to a destination outside Z2 or Z5 (management).
- SOC action: (1) Immediately block the egress at the firewall. (2) Identify the source IP and the database or service it belongs to. (3) Capture a packet sample for forensic analysis. (4) Notify the SECURITY_ARCHITECT within 5 minutes.
- Escalation path: This event is always Critical (severity S1 under MJD-SEC-0006). SECURITY_ARCHITECT and CISO are notified immediately. Board committee is notified within 24 hours.

**Playbook NET-003: Z4 Access Anomaly**

- Detection signal: A connection to Z4 (KMS, HSM, secrets manager) from any SPIFFE ID not in the Z4 allowlist, or from any non-SPIFFE source (such as an IP-based connection rather than a mesh-authenticated connection).
- SIEM correlation rule: any Z4 inbound connection where the TLS client certificate does not present a valid SPIFFE ID registered in the Service Identity Registry, or where the client SPIFFE ID is not in the Z4 allowlist.
- SOC action: (1) Block the connection at the Z4 firewall immediately. (2) Identify the source. (3) If the source is a legitimate service with a missing allowlist entry, escalate to SECURITY_ARCHITECT for emergency allowlist review. (4) If the source is unknown or anomalous, treat as a potential credential compromise and initiate MJD-SEC-0006 at Critical severity.
- Escalation path: SECURITY_ARCHITECT within 5 minutes; CISO within 15 minutes; board notification within 24 hours. Z4 access is quorum-controlled; any anomaly triggers an immediate quorum review.

## 7. Cloud and Hybrid Considerations

7.1.1 Cloud virtual networks map to the same zone model. Security groups, network ACLs, and the service mesh jointly enforce the zone boundaries; a single misconfigured security group never collapses a boundary because the mesh provides a second, identity-based enforcement layer.

7.1.2 Cross-account and cross-region flows follow the same default-deny allowlist discipline and are reviewed as code (MJD-TEC-0007 Cloud Governance and Landing Zone Policy).

7.1.3 Provider-managed services that hold CONFIDENTIAL or RESTRICTED data are placed behind private endpoints in Z3; public service endpoints for such data are prohibited.

### 7.4 Provider-Managed Service Network Controls

7.4.1 When a cloud provider-managed service (such as a managed database, managed queue, or managed AI endpoint) holds CONFIDENTIAL or RESTRICTED data, the following network controls are mandatory:

- **Private endpoint provisioning**: The managed service is accessed exclusively through a private endpoint (AWS VPC Endpoint, Azure Private Link, or GCP Private Service Connect as applicable) that places the service's network interface inside Z3. The public endpoint of the managed service is disabled.
- **Private endpoint verification**: After provisioning, the SECURITY_ARCHITECT verifies that: (a) the service resolves to the private IP address from within Z3; (b) the public endpoint returns a connection refused or access denied response from outside the private network; and (c) the private endpoint DNS entry is in the private hosted zone, not the public DNS.
- **Periodic audit**: Every 90 days, an automated scan confirms that no CONFIDENTIAL or RESTRICTED managed service has a public endpoint enabled. The scan result is logged and reviewed by the SECURITY_ARCHITECT. A public endpoint discovered during the scan is treated as a Critical finding under MJD-SEC-0005 and remediated within 7 days.

7.4.2 Prohibited configurations for CONFIDENTIAL or RESTRICTED data in provider-managed services: public endpoint enabled (any configuration that allows internet-routable access to the service); security group or ACL permitting inbound access from 0.0.0.0/0 or ::/0; managed service credentials stored in environment variables or application code (credentials must be in the secrets manager per MJD-TEC-0004).

7.4.3 Provider-managed services in the Z2 application zone (not holding CONFIDENTIAL or RESTRICTED data, such as a managed cache for public content) are permitted to use provider-managed networking without private endpoints, subject to SECURITY_ARCHITECT review of the data handled.

## 8. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this standard and the zone topology; approves all flow-rule and zone changes; maintains the Zone-to-Zone Allowlist Register and Service Identity Registry; sole authorized reader of this document; performs quarterly CDE review and annual zone model review. |
| Network and platform engineers | Implement segmentation and mesh policy as code under SECURITY_ARCHITECT review; cannot independently approve changes to the Zone-to-Zone Allowlist; receive scoped firewall policy releases from SECURITY_ARCHITECT for their workload only. |
| Incident response / SOC | Uses zone telemetry to contain lateral movement during incidents (MJD-SEC-0006); executes the detection playbooks in Section 6.3; notifies SECURITY_ARCHITECT within the time bounds in each playbook. |
| Change management | Gates production flow changes through the pipeline (MJD-TEC-0008); confirms each change has a linked Zone-to-Zone Allowlist entry before deployment. |
| PCI compliance lead | Co-approves CDE boundary changes (Section 2.4); receives the quarterly CDE review artifact. |

## 9. Exceptions and Escalation

9.1.1 Any deviation (a temporary flow, a legacy flat segment) requires SECURITY_ARCHITECT approval, a compensating control, time-boxing, and an expiry no later than 90 days for network exceptions.

9.1.2 Exceptions to Z3/Z4 isolation may not be delegated and are reported to the CISO.

9.1.3 Detection of an unauthorized inter-zone flow is escalated immediately under the Incident Response Plan (MJD-SEC-0006) as a potential lateral-movement event.

### 9.4 Network Exception Register

9.4.1 The SECURITY_ARCHITECT maintains a Network Exception Register for all approved deviations from this standard. The register is separate from the Zone-to-Zone Allowlist and specifically tracks deviations (flows or configurations that are not standard).

9.4.2 Required fields for each exception register entry:

| Field | Description |
|---|---|
| Exception ID | Unique identifier (e.g., NETEX-0007) |
| Zone(s) affected | Which zones the exception touches |
| Deviation description | What the exception permits that standard policy prohibits |
| Business justification | Why the exception is necessary |
| Compensating control | Control in place to reduce risk during the exception |
| Approved by | SECURITY_ARCHITECT (required); CISO required for Z3/Z4 exceptions |
| Approval date | ISO 8601 |
| Expiry date | Maximum 90 days from approval |
| Remediation plan | How the exception will be closed (permanent fix or accepted risk) |

9.4.3 Exceptions approaching expiry (within 14 days) generate an automated reminder to the SECURITY_ARCHITECT. An expired exception that has not been renewed or closed is automatically disabled by the policy-as-code pipeline. The SECURITY_ARCHITECT is alerted and has 24 hours to either renew (with a new approval cycle) or confirm the exception is closed.

9.4.4 The exception register is reviewed monthly by the SECURITY_ARCHITECT and quarterly by the CISO. The register count and the count of exceptions by zone are included in the IAM health metrics report to the board committee (MJD-SEC-0003 Section 6.3 covers the broader IAM metrics; network exception count is a sub-metric within the security program report).

## Worked Example: Onboarding a New AI/Retrieval Service to Z2

The following example illustrates the network provisioning steps, mTLS configuration, and verification required before a new AI/retrieval service may communicate with Z3.

**Context:** The Platform Engineering team is deploying a new RAG (retrieval-augmented generation) retrieval service that needs to query the Z3 vector index and retrieve decryption keys from the Z4 KMS API.

**Step 1: Service registration in Service Identity Registry.** The team's SECURITY_ARCHITECT liaison submits a PR to the Service Identity Registry adding: service name "rag-retrieval-v2", owning team Platform Engineering, SPIFFE ID spiffe://mjd/rag-retrieval-v2, zone Z2, permitted inbound peers [spiffe://mjd/api-gateway (from Z1)], permitted outbound peers [spiffe://mjd/vector-index (Z3), spiffe://mjd/kms-api (Z4)]. The SECURITY_ARCHITECT reviews the PR, confirms the scope is least-privilege, and approves.

**Step 2: Zone-to-Zone Allowlist entries.** Two new entries are added to the allowlist register: FLOW-0033 (rag-retrieval-v2 to vector-index, port 8443, gRPC, mTLS required, 12-month expiry) and FLOW-0034 (rag-retrieval-v2 to kms-api, port 443, HTTPS, mTLS required, 90-day expiry for Z4 exception tracking). Each entry is peer-reviewed and approved per Section 2.3.

**Step 3: mTLS configuration.** The mesh control plane is updated with the new service identity. On first deployment of the rag-retrieval-v2 pod, the mesh sidecar requests a SPIFFE certificate from the CA via the control plane. The CA issues a certificate with SPIFFE ID spiffe://mjd/rag-retrieval-v2, 30-day validity.

**Step 4: Firewall rule deployment.** The allowlist entries are translated to firewall rules and mesh authorization policies by the policy-as-code pipeline. The pipeline requires the Zone-to-Zone Allowlist entry IDs (FLOW-0033, FLOW-0034) to be referenced in the rule PR; the pipeline fails without them.

**Step 5: Verification tests before production traffic is permitted.** The SECURITY_ARCHITECT runs the following verification tests: (a) from a Z2 test pod NOT registered as rag-retrieval-v2, attempt to reach vector-index on port 8443; expect: DENY (mesh rejects due to SPIFFE ID mismatch); (b) from the rag-retrieval-v2 pod, attempt to reach vector-index; expect: ALLOW after mTLS handshake; (c) from the rag-retrieval-v2 pod, attempt to reach a Z3 database other than vector-index; expect: DENY; (d) from the rag-retrieval-v2 pod, attempt to reach the internet (egress); expect: DENY by Z2 egress filter; (e) certificate rotation simulation: force a certificate renewal and confirm the pod continues to operate without interruption.

**Step 6: Go-live.** All five verification tests pass. The SECURITY_ARCHITECT signs the go-live confirmation. Production traffic is enabled. The Zone-to-Zone Allowlist entries and Service Identity Registry entry are now the binding policy for the service.

## 10. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent zero-trust principle)
- MJD-SEC-0002 Cryptographic Standard (the mTLS suites and certificate rotation enforcing Section 3.1.2)
- MJD-SEC-0003 Identity and Access Management (IAM) Policy (the identity controls that the zone model enforces)
- MJD-SEC-0010 Privileged Access Management (PAM) Policy (the brokered administrative access of Section 5.2)
- MJD-SEC-0009 Logging, Monitoring, and SIEM Standard (the destination for inter-zone flow telemetry)
- MJD-TEC-0008 Change Management and Release Policy (the gated pipeline for flow-rule changes)
- MJD-SEC-0007 Threat Modeling Standard (the threat model the detection rules in Section 6 align to)

## 11. Regulatory References

- NIST SP 800-207: Zero Trust Architecture reference model.
- PCI DSS 4.0 Requirement 1: install and maintain network security controls and segmentation.
- NIST SP 800-53 Rev 5 (SC family): system and communications protection controls.
- FFIEC Information Security Booklet: network security examination expectations.
- CISA Zero Trust Maturity Model v2: maturity pillars for zero-trust adoption.

## 12. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2020-08-15 | SECURITY_ARCHITECT | Initial network segmentation standard (perimeter model). |
| 2.0.0 | 2022-05-30 | SECURITY_ARCHITECT | Introduced trust zones and default-deny inter-zone rules. |
| 3.0.0 | 2023-10-12 | SECURITY_ARCHITECT | Adopted zero-trust tenets; added micro-segmentation and mesh mTLS. |
| 3.1.0 | 2024-09-08 | SECURITY_ARCHITECT | Added zero-trust network access broker; retired flat VPN. |
| 4.0.0 | 2026-02-05 | SECURITY_ARCHITECT | Annual review; added Z4 crypto zone and AI/retrieval placement. |
