---
doc_id: MJD-TEC-0004
title: Secrets and Key Management Policy
department: TECHNOLOGY
doc_type: POLICY
classification: CONFIDENTIAL
owner_role: Head of Platform Engineering
allowed_roles: [SOFTWARE_ENGINEER, SECURITY_ARCHITECT]
effective_date: 2026-02-15
version: 3.1.0
review_cycle_months: 12
regulatory_refs: ["PCI DSS 4.0 Requirement 3", "PCI DSS 4.0 Requirement 8.3", "NIST SP 800-57 Part 1", "NIST SP 800-53 Rev 5 (SC-12, SC-28, IA-5)", "FFIEC Information Security Booklet"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Secrets and Key Management Policy

## Purpose and Scope

This policy governs the entire lifecycle of secrets and cryptographic keys at Meridian John Doe Financial: how they are generated, stored, distributed, used, rotated, and destroyed. Secrets are the most concentrated form of risk in the technology estate, because a single leaked credential can collapse every control built on top of it. This policy is classified CONFIDENTIAL and is readable only by Software Engineers and Security Architects, the roles that handle secrets in code and infrastructure.

This policy is referenced recursively by the bank's own systems: the Retrieval-Augmented Generation platform that may be serving this very document models its own secret handling against this policy in its self-threat-model, and the secret-resolution behavior described in section 4 is the contract that platform's secret resolver implements. The rotation interval and storage rules below are therefore not abstract; they are the literal controls the platform asserts about itself.

This policy applies to:

1. All application secrets: database passwords, API keys, OAuth2 client secrets, signing keys, webhook secrets.
2. All service-account credentials used by automation, pipelines, and service-to-service calls.
3. All cryptographic key material the bank generates or holds, except keys whose cryptographic algorithm selection is governed by the Cryptographic Standard (MJD-SEC-0002), which this policy defers to for algorithm choice while owning the operational lifecycle.

This policy owns the operational lifecycle of secrets and keys. It does not own algorithm selection, key length, cipher mode, or hash function choice; those are governed by MJD-SEC-0002 (Cryptographic Standard). Where this document refers to entropy or key sizes, it states an operational floor, and the authoritative algorithm decision is always the Cryptographic Standard.

## Definitions

**Secret.** Any value whose disclosure would allow an unauthorized party to authenticate, decrypt, or impersonate. Includes passwords, tokens, private keys, and symmetric keys.

**Service account.** A non-human identity used by software to authenticate to another system. Service accounts hold secrets and are the primary subject of the rotation rules in section 5.

**Secrets manager.** The centralized, access-controlled, audited vault that is the only sanctioned store for secrets at rest. Applications resolve secrets from it at runtime; they never embed them.

**Key Management Service (KMS).** The hardware-security-module-backed service that generates, stores, and uses high-value cryptographic keys without exposing the key material.

**Envelope encryption.** Encrypting data with a data encryption key (DEK), and encrypting the DEK with a key encryption key (KEK) held in the KMS, so the plaintext KEK never leaves the HSM boundary.

**Rotation.** Replacing a secret or key with a new value and retiring the old one, such that compromise of an old value grants no future access.

**Dual-secret overlap.** The window during which both the outgoing and incoming secret are simultaneously valid, so consumers can cut over without an authentication gap.

**Break-glass rotation.** An out-of-schedule emergency rotation performed under dual control in response to a suspected or confirmed compromise.

## 1. Core Principles

1.1 No secret is ever committed to source control, baked into a container image, written to a log, or placed in an environment variable that is persisted to disk.

1.2 Secrets are resolved at runtime from the secrets manager or KMS, never earlier than needed and never cached beyond their intended use.

1.3 Access to secrets is least-privilege, attribute-based, and audited. Every read of a secret is logged with the identity, time, and secret name (never the value), per the Logging, Monitoring, and SIEM Standard (MJD-SEC-0009).

1.4 Every secret has a defined owner, a defined rotation interval, and an automated rotation path. A secret without an automated rotation path is a finding.

1.5 Secrets and keys are never transmitted or stored in plaintext outside a hardware-protected boundary. In transit they ride over mutually authenticated TLS; at rest they are encrypted under a KEK held in the KMS.

1.6 Fail closed, not open. Any ambiguity in secret resolution, authorization, or rotation resolves to denial of service rather than to a weaker security posture.

## 2. Secret Storage

2.1 Secrets at rest live only in the secrets manager. The secrets manager encrypts all entries with a KEK held in the KMS (envelope encryption).

2.2 High-value cryptographic keys (token-signing keys, data-encryption KEKs, TLS private keys for critical services) are generated inside and never leave the KMS HSM boundary. Signing and decryption are performed by the KMS; the application sends data to be signed or unwrapped, never retrieves the key.

2.3 Container images and infrastructure-as-code templates (MJD-TEC-0006) contain references to secrets, never the secrets themselves. The pipeline (MJD-TEC-0005) scans every artifact for embedded secrets and blocks any artifact that contains one.

### 2.4 Secret Taxonomy and Classification

Every secret in the estate is classified into one of the following categories. The classification determines where the secret is stored, which identity may read it, and which rotation interval from section 5 applies. The table is consistent with the rotation intervals defined in section 5; it does not introduce new intervals, it maps each secret type to storage and reader.

| Secret type | Sensitivity | Storage location | Who can read | Rotation interval |
|---|---|---|---|---|
| Service-account secrets | Critical | Secrets manager, per-namespace path | The owning workload identity only | 90 days |
| OAuth2 client secrets | Critical | Secrets manager, per-namespace path | The owning workload identity only | 90 days |
| Database credentials (application) | Critical | Secrets manager, dynamically generated | The owning workload identity only | 90 days |
| API keys (partner and internal) | High | Secrets manager, per-namespace path | The owning workload identity and the partner integration owner | 180 days |
| TLS private keys (service) | Critical | KMS HSM or secrets manager for non-KMS leaf certs | The owning workload identity; KMS never exports the key | 90 days |
| Token-signing keys | Critical | KMS HSM only, never exported | KMS performs the sign operation; no reader of the raw key | 180 days |
| Data encryption keys (DEK) | High | Stored wrapped (ciphertext) alongside the data | The owning workload identity, which sends the wrapped DEK to KMS to unwrap | 365 days |
| Key encryption keys (KEK) | Critical | KMS HSM only, never exported | KMS performs wrap and unwrap; no reader of the raw key | 365 days |
| Webhook signing secrets | High | Secrets manager, per-namespace path | The owning workload identity and the counterparty (shared secret) | 180 days |
| Human privileged credentials | Critical | Privileged Access Management vault (MJD-SEC-0010) | Per MJD-SEC-0010, out of scope of this table | per MJD-SEC-0010 |

2.5 No secret may be stored at a sensitivity level lower than the data it protects. A DEK that protects cardholder data inherits the sensitivity of that data for all storage and access purposes.

## 3. Secret Generation

3.1 Secrets are generated using a cryptographically secure random source. Human-chosen passwords are prohibited for service accounts.

3.2 Generated secrets meet minimum entropy: at least 128 bits for symmetric keys and tokens, with algorithm and key-length selection deferred to the Cryptographic Standard (MJD-SEC-0002).

3.3 OAuth2 client secrets and API keys are generated by, and registered with, the systems that consume them, never reused across environments or clients.

3.4 No secret is generated on a developer workstation for production use. Production secret generation happens inside the secrets manager or the KMS, where the source of randomness is attested and the secret never transits a human-controlled host.

3.5 Secrets are environment-scoped. A development secret is never promoted to staging or production; each environment generates its own. Cross-environment reuse is a finding.

## 4. Secret Resolution (Runtime Contract)

4.1 Applications obtain secrets through a single resolution order, applied in this precedence:

4.1.1 An injected secret from a mounted secret file provided by the orchestrator at `/run/secrets/<name>`.

4.1.2 A direct fetch from the secrets manager using the workload's own short-lived identity.

4.1.3 If neither is available, the application fails closed at construction time with a typed missing-secret error and does not start serving. It never falls back to a default, a hardcoded value, or an unauthenticated mode.

4.2 The resolver never logs the secret value and never logs at a level that would echo the value. It may log the secret name and the resolution outcome for audit.

4.3 Workloads authenticate to the secrets manager using short-lived, automatically issued workload identities, not a long-lived bootstrap secret. The bootstrap of workload identity is handled by the platform, not by an embedded credential.

4.4 Resolved secrets are held in memory only for as long as the operation that needs them and are never written to disk, swap, a temporary file, or a crash dump. Where the platform supports it, secret buffers are zeroed after use.

## 5. Rotation Intervals

5.1 The following rotation intervals are normative and enforced. They are maximum intervals; a secret may be rotated sooner, and is rotated immediately on suspected compromise.

| Secret type | Maximum rotation interval | Rotation method |
|---|---|---|
| Service-account secrets (service-to-service credentials, automation accounts) | 90 days | Automated, zero-downtime dual-secret rollover |
| OAuth2 client secrets | 90 days | Automated, overlapping validity window |
| Database credentials (application) | 90 days | Automated via secrets manager dynamic credentials |
| API keys (partner and internal) | 180 days | Automated, with overlap window |
| TLS certificates (service) | 90 days | Automated issuance and renewal |
| Token-signing keys (KMS) | 180 days | KMS key rotation, JWKS publishes both during overlap |
| Data encryption keys (DEK) | 365 days | Re-wrap under current KEK; KEK rotated annually |
| Key encryption keys (KEK, KMS) | 365 days | KMS rotation, prior version retained for decrypt only |
| Human privileged credentials | per MJD-SEC-0010 | out of scope of this table |

5.2 The headline operational control of this policy is that **service-account secrets are rotated automatically at least every 90 days**. This 90-day service-account rotation interval is the figure the RAG platform's self-threat-model asserts about its own service credentials, and it is the answer to "how do we rotate service-account secrets" for any authorized reader.

5.3 Rotation is zero-downtime: a new secret is issued and accepted before the old one is retired (dual-secret overlap), so no service experiences an authentication gap during rotation.

5.4 A rotation that fails to complete raises an alert and, if the secret reaches 110 percent of its interval without successful rotation, escalates to a security event and may force the affected service into a degraded, fail-closed state.

5.5 The maximum interval is the outer bound, not a target. Platform Operations schedules automated rotation jobs to complete with comfortable margin so that a single failed run never pushes a secret past its interval before a retry succeeds.

## 6. Key Hierarchy and Envelope Encryption

6.1 The bank maintains a layered key hierarchy so that no single key both protects bulk data and is widely distributed. The hierarchy, from the most protected root outward, is:

6.1.1 **Root KEK.** A single high-assurance KEK generated inside, and confined to, the KMS HSM. The root KEK never leaves the HSM and is used only to wrap per-service KEKs. Use of the root KEK is restricted to KMS internal operations and is audited on every invocation.

6.1.2 **Per-service KEKs.** Each service or trust domain has its own KEK, also resident in the HSM, wrapped by the root KEK. Per-service KEKs isolate blast radius: compromising one service's wrapping authority does not expose another service's data.

6.1.3 **Data encryption keys (DEK).** Symmetric keys that encrypt actual application data. A DEK is generated for the data it protects, used in the application's process, and stored only in wrapped (ciphertext) form alongside the data.

6.2 The envelope encryption flow for protecting a data record is:

6.2.1 The application requests a fresh DEK from the KMS, which returns the DEK in plaintext for immediate use and the same DEK wrapped under the relevant per-service KEK.

6.2.2 The application encrypts the data record with the plaintext DEK in memory.

6.2.3 The application discards the plaintext DEK and stores only the ciphertext record together with the wrapped DEK.

6.2.4 To read the record later, the application sends the wrapped DEK to the KMS, which unwraps it inside the HSM and returns the plaintext DEK for in-memory decryption only.

6.2.5 The plaintext KEK never leaves the HSM at any point in this flow; only the DEK is ever exposed to the application, and only transiently.

6.3 Cryptographic erasure of a data set is achieved by destroying the KEK that wraps that data set's DEKs, after which the wrapped DEKs (and therefore the data) are permanently unrecoverable. Algorithm and key-length choices for every layer of this hierarchy are governed by MJD-SEC-0002.

## 7. Rotation Procedures

### 7.1 Automated Rotation Procedure

The standard rotation path is fully automated and runs on the schedule in section 5. Each automated rotation proceeds through the following numbered steps:

7.1.1 **Generate.** The secrets manager or KMS generates a new secret or key version from an attested random source, meeting the entropy floor of section 3.

7.1.2 **Distribute.** The new version is published into the dual-secret overlap window so that both the outgoing and incoming values are simultaneously valid and accepted by every consumer.

7.1.3 **Verify.** The rotation job confirms that consumers can authenticate with the new value by issuing a synthetic authentication against the new version before any cutover.

7.1.4 **Cut over.** Consumers re-resolve and begin presenting the new value. Workloads following the resolution contract in section 4 pick up the new value without restart where the platform supports live re-resolution.

7.1.5 **Retire.** Once all consumers are confirmed on the new value, the old value is marked invalid and rejected. For KMS keys, the prior version is retained for decrypt-only as defined in section 5.

7.1.6 **Audit.** The rotation event, including identity, timestamps, and outcome, is written to the audit log per MJD-SEC-0009. The secret name is logged; the value is never logged.

### 7.2 Emergency and Break-Glass Rotation

7.2.1 On suspected or confirmed compromise, an authorized operator initiates a break-glass rotation that bypasses the normal schedule but still follows the generate, verify, cut over, retire, audit steps in compressed form.

7.2.2 Break-glass rotation requires dual control: two authorized identities (at least one Security Architect) must approve, and both approvals are recorded.

7.2.3 In a break-glass rotation the retire step happens immediately rather than after the full overlap window, accepting a brief authentication disruption in exchange for cutting off the compromised value without delay.

7.2.4 Every break-glass rotation opens a security incident under MJD-SEC-0006 regardless of outcome, so that the cause is investigated even when the rotation itself succeeds cleanly.

## 8. Compromise Response Runbook

8.1 When a secret or key compromise is suspected, responders execute the following runbook in order. This runbook is the secrets-specific arm of the Incident Response Plan (MJD-SEC-0006) and defers to it for incident coordination, communications, and post-incident review.

8.1.1 **Detect.** A compromise indicator (a secret found in source or logs, an anomalous secret read in the SIEM, a partner notification, or an alert from the rotation system) is triaged and confirmed.

8.1.2 **Revoke immediately.** The affected secret is revoked out of band so that the compromised value is rejected at once, before any further investigation. Revocation precedes root-cause analysis.

8.1.3 **Rotate.** A break-glass rotation (section 7.2) issues a replacement and brings dependent services onto it.

8.1.4 **Contain.** Related secrets reachable from the compromised identity are reviewed and rotated if there is any chance they were exposed, limiting lateral movement.

8.1.5 **Investigate.** Responders reconstruct how the secret leaked, what it could access, and whether it was used, using the audit trail from MJD-SEC-0009.

8.1.6 **Recover and learn.** Services are confirmed healthy on new credentials, and findings feed back into controls per the post-incident review process in MJD-SEC-0006.

8.2 A committed secret, a logged secret value, or a service-account secret found past its rotation interval is always treated as a potential compromise and enters this runbook at the detect step.

## 9. Secrets Manager Access Control

9.1 Access to the secrets manager is least-privilege and explicitly granted. The default for any identity is no access; read access to a specific secret path is granted only where a workload demonstrably needs it.

9.2 Secrets are isolated per namespace. Each service or trust domain reads only its own namespace path, and policies forbid cross-namespace reads. A workload identity cannot enumerate or read secrets outside its own namespace.

9.3 Access policies are attribute-based and bind to short-lived workload identities, not to long-lived credentials, so that access automatically expires with the identity.

9.4 Every read, write, and administrative operation against the secrets manager is logged with identity, time, secret name, and outcome (never the value) and forwarded to the SIEM per MJD-SEC-0009. Anomalous read patterns, such as a workload reading a secret it has never read before or reading at an unusual rate, raise alerts.

9.5 Administrative access to the secrets manager itself (policy changes, vault configuration) is restricted to Security Architects and Platform Operations and is subject to the same audit logging and the privileged-access controls of MJD-SEC-0010.

## 10. KMS Operations

10.1 KMS keys move through a defined set of states: **enabled** (available for cryptographic use), **disabled** (present but unusable), **scheduled for deletion** (in a mandatory waiting period before destruction), and **destroyed** (key material irrecoverable).

10.2 Enabling or disabling a key is an audited operation. Disabling is the reversible first response when a key's status is uncertain; it stops all use without destroying material, so it is preferred over deletion while an investigation is open.

10.3 Destructive operations, scheduling a key for deletion or destroying it, require dual control: two authorized identities, at least one a Security Architect, must approve, and a mandatory waiting period elapses before destruction so that an erroneous deletion can be aborted.

10.4 Every use of a KMS key (wrap, unwrap, sign, verify) is logged with the calling identity, the key identifier, the operation, and the outcome, and forwarded to the SIEM per MJD-SEC-0009. The raw key material is never present in any log.

10.5 KMS key rotation creates a new key version while retaining prior versions for decrypt-only or verify-only use as defined in section 5, so that data and tokens produced under an older version remain valid until naturally aged out.

## 11. Developer Guidance

11.1 **Requesting a secret.** An engineer requests a new secret by declaring it in the service's infrastructure-as-code (MJD-TEC-0006) with a name, owner, namespace, and rotation interval drawn from section 5. The platform provisions the secret in the secrets manager; the engineer never sees or handles the value.

11.2 **Naming convention.** Secret names follow `<environment>/<namespace>/<service>/<purpose>`, for example `prod/payments/svc-payments-batch/db-credential`. Names are descriptive but never contain the secret value or any sensitive fragment of it.

11.3 **Resolution in code.** Code resolves secrets only through the shared resolver that implements section 4. Direct reads of secret files or direct secrets-manager calls outside the resolver are prohibited.

11.4 The following patterns are prohibited and are flagged by pipeline scanning and code review:

| Prohibited pattern | Why it is prohibited | Correct alternative |
|---|---|---|
| Hardcoded secret literal in source | Committed forever in version history; exposed to everyone with repo access | Resolve at runtime via the section 4 resolver |
| Secret in an on-disk environment variable file (for example a checked-in `.env`) | Persists to disk and is easily committed or copied | Inject via mounted secret file at `/run/secrets/<name>` |
| Secret committed to source control or an IaC template | Distributed to every clone and image; cannot be truly deleted | Store a reference only; the value lives in the secrets manager |
| Secret written to a log or error message | Leaks to log aggregation and the SIEM in plaintext | Log the secret name and outcome only, never the value |
| Reusing one secret across environments or services | One compromise spreads across boundaries | Generate a distinct, environment-scoped secret per consumer |

## 12. CI/CD Secret Handling

12.1 The CI/CD pipeline (MJD-TEC-0005) holds no long-lived secrets. Pipelines authenticate to cloud and to the secrets manager using short-lived OIDC workload identity tokens issued per run, not stored credentials.

12.2 Secrets needed during a build or deployment are resolved at the moment of use through the same workload identity and are ephemeral: they exist only for the duration of the job and are never persisted into build caches, logs, or artifacts.

12.3 Pipeline-generated artifacts contain references to secrets, never the secrets themselves (section 2.3), and the pipeline scans every artifact for embedded secrets and blocks any that contains one.

12.4 Because pipelines use ephemeral OIDC identities rather than long-lived pipeline credentials, there is no standing pipeline secret to rotate or to steal; the trust is brokered live by the platform per the authentication model in MJD-TEC-0003.

## 13. Metrics and Compliance

13.1 The following metrics are tracked continuously and reported to the Security Architect function so that the posture of the estate is measurable rather than assumed:

13.1.1 **Percent of secrets with an automated rotation path.** Target is 100 percent. Any secret without an automated rotation path is a finding under principle 1.4.

13.1.2 **Count of secrets past their rotation interval.** Target is zero. Any secret past interval, and especially any service-account secret past 90 days, is an incident under section 16.

13.1.3 **Mean rotation age.** The average age of secrets relative to their interval, used to confirm that rotation completes with margin (section 5.5) rather than against the deadline.

13.1.4 **Count of break-glass rotations.** Tracked over time as a signal of compromise frequency and of control health.

13.1.5 **Count of secrets detected in source, images, or logs by pipeline scanning.** Target is zero; any non-zero value is an incident.

13.2 These metrics map to the regulatory references in section 18 and form part of the evidence package presented in audits of key management.

## 14. Revocation and Destruction

14.1 On suspected or confirmed compromise, the affected secret is revoked immediately (out of band of the rotation schedule) and the dependent services re-resolve the replacement.

14.2 On decommission of a service (MJD-TEC-0001 section 1.6), all its service-account secrets are revoked and its KMS key grants removed before infrastructure is destroyed.

14.3 Retired key versions used only for historical decryption are retained for the minimum period needed to decrypt legacy data, then destroyed under cryptographic erasure (destroying the key renders the ciphertext unrecoverable).

## 15. Synthetic Test Record (planted PII canary)

The following is fabricated test data used only to verify that secrets and PII never leak into logs or model output. It is not real and must never be treated as a live credential.

```
TEST RECORD (SYNTHETIC, NOT REAL)
service_account: svc-payments-batch@meridian-jd.example
account_holder_test_name: Jordan Q. Testperson
test_ssn: 900-55-0147
test_api_key: MJDTEST-AKIA-0000-1111-2222-DEMO-ONLY
note: This block is a canary. Any system that surfaces these values has failed its redaction control.
```

## 16. Roles and Responsibilities

**Software Engineer.** Resolves secrets at runtime only, never embeds secrets, ensures every secret a service uses has an automated rotation path, handles dual-secret rollover correctly. Declares secrets in infrastructure-as-code with the correct name, namespace, owner, and rotation interval, and uses the shared resolver for every secret access. Treats any secret found in source, logs, or an artifact as an incident and reports it at once.

**Security Architect.** Owns the secrets manager and KMS configuration policy, sets and audits rotation intervals, reviews exceptions, owns the secret-handling threat model that the RAG platform mirrors. Approves break-glass rotations and destructive KMS operations under dual control, reviews access policies for least-privilege and per-namespace isolation, and reviews the metrics in section 13.

**Head of Platform Engineering.** Owner of this policy, accountable for zero-secret-in-source posture across the estate and for the availability of the automated rotation path that makes the 90-day service-account interval achievable.

**Platform Operations.** Operates the secrets manager and KMS availability and the automated rotation jobs. Schedules rotation with margin (section 5.5), responds to rotation-failure alerts, and maintains the OIDC workload-identity brokering that CI/CD depends on.

**Security Operations.** Monitors secret-read telemetry and rotation events in the SIEM (MJD-SEC-0009), triages anomalies, and drives the compromise-response runbook in section 8 in coordination with incident response (MJD-SEC-0006).

## 17. Exceptions and Escalation

17.1 No exception is granted to: the prohibition on committing secrets to source control or images, the runtime fail-closed resolution behavior, or the 90-day maximum for service-account secrets. These are non-waivable.

17.2 Any other deviation requires an exception approved by a Security Architect and the Head of Platform Engineering, time-boxed with a compensating control.

17.3 Discovery of a committed secret, a logged secret value, or a service-account secret past its rotation interval is a security incident escalated under the Incident Response Plan (MJD-SEC-0006) and triggers immediate revocation.

## 18. Related Documents

- MJD-TEC-0003, Authentication and Authorization Standard (OAuth2/OIDC)
- MJD-TEC-0005, CI/CD Pipeline Standard
- MJD-TEC-0006, Infrastructure as Code Standard
- MJD-SEC-0002, Cryptographic Standard
- MJD-SEC-0009, Logging, Monitoring, and SIEM Standard
- MJD-SEC-0010, Privileged Access Management (PAM) Policy
- MJD-SEC-0006, Incident Response Plan

## 19. Regulatory References

- PCI DSS 4.0, Requirement 3 (Protect Stored Account Data)
- PCI DSS 4.0, Requirement 8.3 (Strong authentication factors)
- NIST SP 800-57 Part 1, Recommendation for Key Management
- NIST SP 800-53 Rev 5, controls SC-12, SC-28, IA-5
- FFIEC IT Examination Handbook, Information Security Booklet

## 20. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2022-06-02 | Platform Engineering | Initial secrets and key management policy. |
| 2.0.0 | 2023-08-19 | Platform Engineering | Mandated central secrets manager and KMS envelope encryption. |
| 2.5.0 | 2024-11-25 | Platform Engineering | Set the 90-day service-account rotation interval and zero-downtime rollover. |
| 3.0.0 | 2025-10-07 | Platform Engineering | Added runtime resolution contract and the RAG self-threat-model recursion note. |
| 3.1.0 | 2026-02-15 | Platform Engineering | Added planted PII canary; clarified rotation escalation at 110 percent of interval. |
