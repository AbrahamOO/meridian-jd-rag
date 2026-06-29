---
doc_id: MJD-SEC-0002
title: Cryptographic Standard
department: SECURITY
doc_type: STANDARD
classification: RESTRICTED
owner_role: SECURITY_ARCHITECT
allowed_roles: [SECURITY_ARCHITECT]
effective_date: 2026-02-01
version: 5.1.0
review_cycle_months: 12
regulatory_refs: ["PCI DSS 4.0 Requirement 3", "PCI DSS 4.0 Requirement 4", "NIST SP 800-57 Part 1 Rev 5", "NIST SP 800-52 Rev 2", "FIPS 140-3", "NIST SP 800-131A Rev 2"]
supersedes: null
entity_status: FICTIONAL
---

> **FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.**

# Cryptographic Standard

## Purpose and Scope

This Cryptographic Standard defines the mandatory cryptographic algorithms, protocol versions, key lengths, key lifecycle controls, hardware security module (HSM) requirements, and key management service (KMS) rotation intervals for Meridian John Doe Financial (Meridian J.D.). It is the single authoritative source for what cryptography is approved, prohibited, and deprecated across the institution. Every system that protects data in transit or at rest, signs artifacts, or manages secrets must comply with this standard without exception.

This document is classified RESTRICTED and is readable only by the SECURITY_ARCHITECT role. It is one of the three RESTRICTED security documents that form the sharpest access boundary in the corpus. The cryptographic algorithm selections, key lengths, and rotation schedules below are operational secrets: disclosing them narrows an attacker's search space, so this standard is invisible to OPERATIONS_ANALYST, SOFTWARE_ENGINEER, and every other role. Engineers who must implement cryptography receive the necessary parameters through a controlled, scoped release approved by the SECURITY_ARCHITECT, not through direct access to this document.

The scope covers: transport encryption, data-at-rest encryption, application-layer encryption, digital signatures, message authentication, password and credential hashing, random number generation, certificate management, the HSM estate, and the cloud KMS configuration. The scope explicitly includes cryptography used by Meridian J.D.'s internal AI and retrieval systems for protecting indexed content and audit logs.

## Definitions

**AEAD.** Authenticated Encryption with Associated Data, a cipher mode that provides confidentiality and integrity simultaneously (for example AES-GCM and ChaCha20-Poly1305).

**KMS.** Key Management Service, the centralized service that generates, stores, rotates, and controls access to cryptographic keys.

**HSM.** Hardware Security Module, a tamper-resistant hardware device that generates and stores key material and performs cryptographic operations without exposing private keys.

**KEK.** Key Encryption Key, a key used only to wrap (encrypt) other keys.

**DEK.** Data Encryption Key, a key used to encrypt application data; DEKs are wrapped by a KEK (envelope encryption).

**Root key.** The top of the key hierarchy, held in an HSM, never exported in plaintext.

**Crypto-period.** The time span during which a specific key is authorized for use before it must be rotated.

**Perfect forward secrecy (PFS).** A property of a key exchange whereby compromise of a long-term key does not compromise past session keys.

## 1. Approved Algorithms and Key Lengths

### 1.1 Symmetric Encryption

1.1.1 The approved symmetric cipher is AES in an authenticated mode. The mandatory minimum key length is 256 bits. AES-128 is permitted only for legacy interoperability with a documented exception expiring no later than 2026-12-31.

1.1.2 Approved symmetric modes, in order of preference:

| Algorithm | Key length | Mode | Use |
|---|---|---|---|
| AES-256-GCM | 256-bit | AEAD | Default for data at rest and application-layer encryption |
| ChaCha20-Poly1305 | 256-bit | AEAD | Approved alternative, mobile and constrained clients |
| AES-256-GCM-SIV | 256-bit | AEAD, nonce-misuse resistant | High-volume encryption where nonce uniqueness is hard to guarantee |

1.1.3 AES-GCM nonces must be 96 bits and must never repeat under a given key. Nonce generation uses a deterministic counter or a 96-bit cryptographically secure random value with collision tracking. A repeated nonce under one key is a reportable cryptographic incident.

1.1.4 Prohibited symmetric algorithms and modes: DES, 3DES, RC4, Blowfish, AES-ECB, and any unauthenticated CBC mode without a separate verified MAC.

### 1.2 Asymmetric Encryption and Key Exchange

1.2.1 Approved asymmetric algorithms:

| Algorithm | Minimum size | Use |
|---|---|---|
| RSA (OAEP padding, SHA-256) | 3072-bit | Key transport, legacy signatures |
| ECDSA (P-256, P-384) | 256-bit / 384-bit | Digital signatures, TLS certificates |
| EdDSA (Ed25519) | 256-bit | Signatures, service identity |
| ECDH / X25519 | 256-bit | Key agreement with PFS |

1.2.2 RSA key transport must use OAEP padding. RSA PKCS#1 v1.5 encryption padding is prohibited. RSA keys shorter than 3072 bits are prohibited for new issuance; existing 2048-bit keys must be retired by 2026-12-31.

1.2.3 The institution maintains a post-quantum readiness posture: ML-KEM (Kyber) hybrid key exchange is approved for pilot in non-production and is the planned successor for key agreement. No production system may rely solely on classical key exchange after the migration deadline set annually by the SECURITY_ARCHITECT.

### 1.3 Hashing and Message Authentication

1.3.1 Approved hash functions: SHA-256, SHA-384, SHA-512, and SHA-3. SHA-256 is the default.

1.3.2 Prohibited hash functions for any security purpose: MD5, SHA-1. SHA-1 is permitted only inside legacy HMAC constructions during a documented migration, never for digital signatures or certificate fingerprints.

1.3.3 Message authentication uses HMAC-SHA-256 or the AEAD tag of the cipher. Standalone integrity checks use HMAC, never a bare hash.

### 1.4 Password and Credential Hashing

1.4.1 User passwords and other low-entropy secrets are hashed with Argon2id. Mandatory parameters: memory 64 MiB, iterations (time cost) 3, parallelism 4, and a 16-byte cryptographically random salt per credential.

1.4.2 Where Argon2id is unavailable, scrypt (N=2^17, r=8, p=1) or PBKDF2-HMAC-SHA-256 (minimum 600,000 iterations) is approved as a fallback. Plain or single-round hashes for passwords are prohibited.

1.4.3 Credential comparison must be constant-time to prevent timing oracles.

### 1.5 Random Number Generation

1.5.1 All cryptographic randomness derives from a NIST SP 800-90A approved DRBG seeded from a hardware entropy source or the operating system CSPRNG. Application-language non-cryptographic PRNGs are prohibited for any security purpose.

1.5.2 Initialization vectors, nonces, salts, and key material are generated from the approved CSPRNG. Reuse of an IV or nonce under a single key is prohibited and is a reportable cryptographic incident (Section 9). For high-volume encryption where nonce uniqueness cannot be guaranteed operationally, AES-256-GCM-SIV is used so that an accidental nonce repeat does not catastrophically break confidentiality.

### 1.6 Binding Minimums (selection rationale)

1.6.1 The following minimums are binding for new design. Stronger equivalents are permitted; anything weaker requires an exception (Section 9):

| Purpose | Minimum approved | Notes |
|---|---|---|
| Symmetric confidentiality | AES-256-GCM | AEAD mandatory |
| Key agreement | X25519 or ECDH P-256 | PFS mandatory |
| Signatures | ECDSA P-256, Ed25519, or RSA-3072 (PSS) | PKCS#1 v1.5 signatures: legacy verify only |
| Hashing | SHA-256 | SHA-384/512 for higher assurance |
| Password hashing | Argon2id (64 MiB, t=3, p=4) | scrypt or PBKDF2-600k fallback |
| MAC | HMAC-SHA-256 | or AEAD tag |

1.6.2 RSA signatures for new issuance use RSA-PSS, not PKCS#1 v1.5. The selection rationale is recorded so that future reviews can re-evaluate against the algorithm-transition guidance (NIST SP 800-131A): AEAD ciphers eliminate padding-oracle and unauthenticated-ciphertext classes, elliptic-curve key agreement provides strong security at small key sizes with PFS, and memory-hard password hashing resists GPU and ASIC cracking.

### 1.7 Application-Layer Encryption

1.7.1 Fields containing the most sensitive data (for example, stored authentication secrets, full account numbers, and any RESTRICTED-classified field) are encrypted at the application layer with AES-256-GCM under a DEK distinct from the storage-level DEK, so that database-level access alone does not expose plaintext.

1.7.2 Application-layer DEKs are wrapped by a KMS KEK (envelope encryption) and never embedded in application code or configuration; they are fetched at runtime from the KMS or secrets manager (MJD-TEC-0004).

1.7.3 Tokenization is used in preference to encryption for primary account numbers where the downstream system does not need the real value; the token vault is itself protected as RESTRICTED.

## 2. Data in Transit (Transport Encryption)

### 2.1 Approved TLS Versions

2.1.1 TLS 1.3 is mandatory for all new services and is the default. TLS 1.2 is permitted only where a peer cannot negotiate TLS 1.3, and only with the AEAD cipher suites in Section 2.2. TLS 1.0, TLS 1.1, and SSL (all versions) are prohibited and must be refused at the listener.

### 2.2 Approved Cipher Suites for Data in Transit

2.2.1 For TLS 1.3, the following cipher suites are approved, in preference order:

| Cipher suite | Notes |
|---|---|
| TLS_AES_256_GCM_SHA384 | Preferred default for all TLS 1.3 endpoints |
| TLS_CHACHA20_POLY1305_SHA256 | Approved for mobile and constrained clients |
| TLS_AES_128_GCM_SHA256 | Permitted; minimum acceptable TLS 1.3 suite |

2.2.2 For TLS 1.2 (legacy peers only), only the following ECDHE AEAD suites are approved, providing perfect forward secrecy:

| Cipher suite |
|---|
| TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 |
| TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 |

2.2.3 All non-PFS suites, all CBC suites, all RC4 suites, and all suites using SHA-1 for the MAC are prohibited. Static RSA key exchange is prohibited.

### 2.3 TLS Hardening

2.3.1 HTTP Strict Transport Security (HSTS) is mandatory on all public endpoints with a max-age of at least 31536000 seconds (one year) and the preload directive set.

2.3.2 OCSP stapling is mandatory. Certificate Transparency logging is required for all publicly trusted certificates.

2.3.3 Mutual TLS (mTLS) is mandatory for service-to-service communication inside the production trust zones, per the Network Segmentation and Zero Trust Architecture (MJD-SEC-0004).

2.3.4 Session resumption that weakens forward secrecy is disabled. TLS 1.3 0-RTT (early data) is prohibited for any request that mutates state or returns sensitive data, because early data is replayable.

2.3.5 Certificate pinning is applied in mobile applications for the bank's own API endpoints, with a documented pin-rotation plan to avoid bricking clients during certificate rotation.

### 2.4 TLS Configuration Baseline

2.4.1 Every TLS listener is configured to the following baseline, validated by automated scanning:

| Setting | Required value |
|---|---|
| Minimum protocol | TLS 1.2 (TLS 1.3 preferred) |
| Cipher suites | Only those in Section 2.2 |
| Key exchange | ECDHE (PFS) only |
| HSTS max-age | >= 31536000 with preload |
| OCSP stapling | Enabled |
| Renegotiation | Secure renegotiation only; client-initiated disabled |
| Compression | Disabled (mitigates CRIME) |

2.4.2 A listener failing the baseline scan is a finding remediated under the Vulnerability and Patch Management Standard (MJD-SEC-0005), escalated by exposure tier.

## 3. Data at Rest

3.1.1 All CONFIDENTIAL and RESTRICTED data at rest is encrypted with AES-256-GCM using envelope encryption: a per-resource DEK encrypts the data, and a KEK held in the KMS wraps the DEK.

3.1.2 Database transparent data encryption, object storage server-side encryption, and disk-level encryption all use KMS-managed keys (customer-managed keys, not provider-default keys).

3.1.3 Backups inherit the classification of their source and are encrypted with the same standard. Backup encryption keys are distinct from production keys and are rotated on the schedule in Section 5.

## 4. Hardware Security Modules (HSM)

4.1.1 Root keys and KEKs are generated and stored in FIPS 140-3 Level 3 validated HSMs. Private key material in the HSM is never exported in plaintext.

4.1.2 HSM administration requires dual control and split knowledge: no single administrator can perform a sensitive HSM operation alone. Quorum authentication (M-of-N, minimum 2-of-3) is enforced for key ceremonies.

4.1.3 HSM firmware is kept at the vendor-supported version. HSM audit logs are streamed to the SIEM (MJD-SEC-0009) and retained for seven years.

4.1.4 Key ceremonies (root key generation, rotation, and recovery) follow a scripted, witnessed procedure with a signed ceremony record retained for the life of the key plus seven years.

## 5. Key Lifecycle and Rotation Intervals

### 5.1 Key Hierarchy

5.1.1 The key hierarchy is three tiers: root key (HSM) wraps KEKs (KMS); KEKs wrap DEKs (KMS); DEKs encrypt data. Compromise is contained at the lowest possible tier.

### 5.2 KMS Key Rotation Intervals (binding)

5.2.1 The following rotation intervals are mandatory. "Rotation" means generating a new key version and directing new operations to it while retaining prior versions for decryption until re-encryption completes.

| Key type | Rotation interval | Notes |
|---|---|---|
| KMS root key (HSM-resident) | Every 3 years (1095 days) | Rotated by witnessed key ceremony |
| KMS Key Encryption Keys (KEK) | Every 365 days (annually) | Automatic KMS rotation enabled |
| Data Encryption Keys (DEK) | Every 90 days | Automatic re-wrap on rotation |
| TLS certificate keys (public-facing) | Every 90 days | Automated issuance and renewal |
| TLS / mTLS service certificate keys (internal) | Every 30 days | Short-lived workload certificates |
| Code and artifact signing keys | Every 365 days | HSM-backed, dual control |
| Service account / API signing keys | Every 90 days | Coordinated with MJD-TEC-0004 |
| Database column-encryption DEKs | Every 90 days | Re-encryption scheduled off-peak |

5.2.2 Automatic rotation is enabled in the KMS wherever the key type supports it. Manual rotation requires a change ticket and SECURITY_ARCHITECT approval.

5.2.3 Emergency rotation (suspected compromise) supersedes the scheduled interval and must complete within 24 hours of confirmation, coordinated through the Incident Response Plan (MJD-SEC-0006).

### 5.3 Key States and Destruction

5.3.1 Keys move through states: pre-active, active, deactivated (decrypt-only), and destroyed. A key is destroyed only after all data it protects has been re-encrypted under a successor key.

5.3.2 Key destruction is cryptographic erasure: the key material is securely deleted from the KMS and HSM, rendering the protected ciphertext unrecoverable. Destruction is logged and witnessed for root and KEK tiers.

### 5.4 Key Ceremony Procedure (root and KEK tiers)

5.4.1 Generation, rotation, and recovery of root keys and KEKs follow a scripted ceremony executed under dual control and quorum authentication (minimum 2-of-3):

| Step | Action | Control |
|---|---|---|
| 1 | Convene witnesses and key custodians | Identity verified; roles confirmed |
| 2 | Validate HSM state and firmware version | Tamper checks pass before proceeding |
| 3 | Generate or activate key inside the HSM | Key never leaves the HSM in plaintext |
| 4 | Split and distribute quorum credentials | Split knowledge; no single holder |
| 5 | Record key metadata and ceremony log | Signed by all participants |
| 6 | Verify with a test encrypt/decrypt | Functional confirmation |
| 7 | Archive the signed ceremony record | Retained for key life plus 7 years |

5.4.2 No ceremony step is performed by a single individual. The ceremony script is reviewed and approved by the SECURITY_ARCHITECT before execution, and any deviation aborts the ceremony.

### 5.5 Key Compromise Response

5.5.1 On suspected compromise of a key, the key is immediately moved to deactivated (decrypt-only) and emergency rotation (Section 5.2.3) begins. The incident is run under MJD-SEC-0006.

5.5.2 The blast radius is bounded by the hierarchy: compromise of a DEK affects only the data it wraps; compromise of a KEK requires re-wrapping all DEKs under it; compromise of the root key triggers a full key-ceremony rebuild. The three-tier design ensures the most expensive recovery is the least likely.

## 6. Certificate Management

6.1.1 All certificates are issued from the Meridian J.D. internal certificate authority or an approved public CA. Self-signed certificates are prohibited in production.

6.1.2 Certificate inventory is maintained automatically; certificates expiring within 30 days trigger an alert, and within 7 days trigger an incident.

6.1.3 Certificate private keys are generated in the HSM or KMS and never transmitted by email, chat, or unencrypted file.

### 6.2 Crypto-Agility and Algorithm Transition

6.2.1 Cryptography is implemented through a central, versioned crypto library so that algorithms can be changed in one place rather than scattered across applications. Direct use of low-level cryptographic primitives by application teams is prohibited; they call the approved library.

6.2.2 Each cryptographic dependency declares the algorithm and parameters it uses so the institution can inventory its cryptography and migrate when an algorithm is deprecated. The post-quantum transition (Section 1.2.3) depends on this agility: hybrid ML-KEM key agreement is introduced behind the same library interface so callers need not change.

6.2.3 An algorithm transition follows a staged plan: approve the successor for pilot, run both in parallel (hybrid), migrate new operations, re-encrypt or re-sign existing material, then deprecate and prohibit the predecessor. Each stage has a SECURITY_ARCHITECT-approved deadline.

## 7. Prohibited and Deprecated Cryptography (summary)

| Category | Prohibited |
|---|---|
| Symmetric | DES, 3DES, RC4, Blowfish, AES-ECB, unauthenticated CBC |
| Asymmetric | RSA < 3072-bit (new), RSA PKCS#1 v1.5 encryption, DH < 2048-bit |
| Hash | MD5, SHA-1 (signatures and fingerprints) |
| Protocol | SSLv2, SSLv3, TLS 1.0, TLS 1.1 |
| Padding | PKCS#1 v1.5 encryption padding |
| RNG | Language-native non-cryptographic PRNGs |

## 8. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| SECURITY_ARCHITECT | Owns this standard; approves algorithm selections, exceptions, and key ceremonies; sole authorized reader. |
| KMS administrators | Operate the KMS and HSM under dual control; execute rotations. |
| Application teams | Implement only approved algorithms via the central crypto library; never roll custom cryptography. |
| Incident response | Drives emergency key rotation on confirmed compromise (MJD-SEC-0006). |

## 9. Exceptions and Escalation

9.1.1 Any deviation from this standard (legacy algorithm, longer crypto-period, weaker key length) requires a documented exception approved by the SECURITY_ARCHITECT, with a compensating control and an expiry no later than 12 months.

9.1.2 Exceptions to RESTRICTED parameters may not be delegated below the SECURITY_ARCHITECT and are reported to the CISO.

9.1.3 A confirmed key compromise, a repeated AES-GCM nonce, or use of a prohibited algorithm in production is a cryptographic incident escalated immediately under MJD-SEC-0006.

## 10. Related Documents

- MJD-SEC-0001 Information Security Policy (master) (the parent policy mandating encryption of CONFIDENTIAL and RESTRICTED data)
- MJD-SEC-0004 Network Segmentation and Zero Trust Architecture (the mTLS trust zones consuming the suites in Section 2)
- MJD-TEC-0004 Secrets and Key Management Policy (the engineering implementation of secret storage and service-key rotation in Section 5.2)
- MJD-SEC-0009 Logging, Monitoring, and SIEM Standard (the destination for HSM and KMS audit logs)
- MJD-SEC-0006 Incident Response Plan (the emergency key rotation path of Section 5.2.3)

## 11. Regulatory References

- PCI DSS 4.0 Requirement 3: protection of stored account data, strong cryptography.
- PCI DSS 4.0 Requirement 4: strong cryptography for cardholder data in transit over open networks.
- NIST SP 800-57 Part 1 Rev 5: recommendations for key management and crypto-periods.
- NIST SP 800-52 Rev 2: guidelines for TLS implementation.
- FIPS 140-3: security requirements for cryptographic modules (HSM validation).
- NIST SP 800-131A Rev 2: transitioning the use of cryptographic algorithms and key lengths.

## 12. Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0.0 | 2020-05-01 | SECURITY_ARCHITECT | Initial cryptographic standard. |
| 2.0.0 | 2021-09-12 | SECURITY_ARCHITECT | Mandated TLS 1.2 AEAD-only; deprecated 3DES. |
| 3.0.0 | 2023-02-20 | SECURITY_ARCHITECT | Added envelope encryption and KMS rotation table. |
| 4.0.0 | 2024-07-15 | SECURITY_ARCHITECT | Mandated TLS 1.3 default; raised RSA minimum to 3072. |
| 5.0.0 | 2025-09-01 | SECURITY_ARCHITECT | Added Argon2id parameters, post-quantum readiness, FIPS 140-3. |
| 5.1.0 | 2026-02-01 | SECURITY_ARCHITECT | Annual review; tightened internal cert rotation to 30 days. |
