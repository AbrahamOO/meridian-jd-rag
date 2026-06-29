---
doc_id: MJD-TEC-0003
title: Authentication and Authorization Standard (OAuth2/OIDC)
department: TECHNOLOGY
doc_type: STANDARD
classification: CONFIDENTIAL
owner_role: Head of Platform Engineering
allowed_roles: [SOFTWARE_ENGINEER, SECURITY_ARCHITECT]
effective_date: 2026-02-10
version: 2.4.0
review_cycle_months: 12
regulatory_refs: ["RFC 6749 (OAuth 2.0)", "RFC 7636 (PKCE)", "OpenID Connect Core 1.0", "NIST SP 800-63B", "PCI DSS 4.0 Requirement 8"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Authentication and Authorization Standard (OAuth2/OIDC)

## Purpose and Scope

This standard defines how identity is proven and how access is granted across all Meridian John Doe Financial software. It specifies the OAuth 2.0 and OpenID Connect (OIDC) flows the bank uses, the token types and their exact lifetimes, the cryptographic validation rules tokens must pass, and the authorization model that turns an authenticated identity into a permitted action. It is classified CONFIDENTIAL because it exposes token lifetimes, validation logic, and trust relationships that materially aid an attacker if disclosed, and is therefore readable only by Software Engineers and Security Architects, the two roles that build and defend the identity plane.

This standard applies to:

1. All human authentication to bank applications (customers, employees, partners).
2. All service-to-service authentication using the client-credentials grant.
3. All token validation performed by APIs and gateways.

It does not define the workforce identity governance lifecycle (joiner-mover-leaver), which is owned by the Identity and Access Management Policy (MJD-SEC-0003), nor the privileged-access elevation flow, owned by the Privileged Access Management Policy. This standard governs the protocol-level mechanics; those policies govern who is entitled to what. The bank operates a single logical authorization server with regional deployments, and every application named in the Secure SDLC Policy (MJD-TEC-0001) inherits the rules below as a build-time gate.

## Definitions

**Authorization server (AS).** The bank's identity provider that authenticates principals and issues tokens. It is the single source of issued tokens; applications never mint their own.

**Access token.** A short-lived bearer credential presented to APIs to authorize a request. Format: signed JWT.

**ID token.** An OIDC token asserting the authenticated user's identity to a client. Format: signed JWT. Never used to authorize API calls.

**Refresh token.** A long-lived credential used to obtain new access tokens without re-prompting the user. Opaque, stored server-side, rotated on use.

**PKCE.** Proof Key for Code Exchange (RFC 7636), a mechanism that binds an authorization code to the client that requested it, mandatory for all authorization-code flows here.

**Scope.** A coarse-grained permission string requested by a client and granted by the AS, for example `accounts.read`.

**Claim.** An assertion inside a token, for example `sub` (subject) or `roles`.

**Entitlement.** A fine-grained, object-level grant resolved in the resource server, distinct from a scope. Scopes say what kind of action a client may attempt; entitlements say which specific objects a principal may touch.

**Assurance level.** The strength and freshness of the authentication behind a token, expressed in the `acr` claim and used to gate high-risk operations.

## 1. Approved Flows

1.1 The bank uses exactly the following OAuth2/OIDC flows. Any other flow is prohibited.

| Use case | Flow | Notes |
|---|---|---|
| Browser and mobile apps (public clients) | Authorization Code with PKCE | Mandatory PKCE, no implicit flow |
| Confidential server-side web apps | Authorization Code with PKCE plus client secret | |
| Service-to-service | Client Credentials | Scoped to least privilege |
| Device or CLI | Device Authorization Grant | Restricted, security-approved only |

1.2 The OAuth2 Implicit grant and the Resource Owner Password Credentials grant are prohibited everywhere. They must not appear in any client configuration. The implicit grant returns tokens in the URL fragment where they leak through history, referrers, and logs; the password grant teaches users to hand credentials to clients and cannot carry phishing-resistant MFA. Neither has a compensating control that makes it acceptable in a regulated bank.

1.3 PKCE with the `S256` code challenge method is mandatory for every authorization-code flow, including confidential clients. The `plain` challenge method is rejected by the AS.

## 2. Authorization Code with PKCE Walkthrough

2.1 The following is the normative sequence for a public client (browser or mobile). Each numbered step is mandatory; skipping any one is a defect.

1. The client generates a cryptographically random `code_verifier` of 43 to 128 characters from an unreserved character set, sourced from a secure random generator.
2. The client computes `code_challenge = BASE64URL(SHA256(code_verifier))` and sets `code_challenge_method=S256`.
3. The client generates a single-use `state` value to bind the response to this request and defeat cross-site request forgery on the redirect.
4. The client generates a single-use `nonce` to bind the resulting ID token to this authentication and defeat replay.
5. The client redirects the user agent to the AS `/authorize` endpoint carrying `response_type=code`, `client_id`, the exact registered `redirect_uri`, requested `scope`, `state`, `nonce`, `code_challenge`, and `code_challenge_method=S256`.
6. The AS authenticates the user, applies MFA and any step-up policy from section 8, and obtains consent where required.
7. The AS redirects back to the registered `redirect_uri` with a single-use `code` (lifetime 60 seconds) and the unchanged `state`.
8. The client verifies the returned `state` matches the value it generated; a mismatch aborts the flow.
9. The client calls the AS `/token` endpoint with `grant_type=authorization_code`, the `code`, the `redirect_uri`, the `client_id`, and the original `code_verifier`.
10. The AS recomputes `SHA256(code_verifier)` and compares it to the stored `code_challenge`. A mismatch rejects the exchange, which defeats an attacker who intercepted the code but never held the verifier.
11. The AS returns an access token (15 minutes), an ID token (10 minutes), and, where the `offline_access` scope was granted, a refresh token (12 hours).
12. The client validates the ID token per section 4, including that the `nonce` matches the value sent in step 4, then discards the `code_verifier`.

2.2 The authorization code is single-use and expires 60 seconds after issuance. A code presented twice, or after expiry, is rejected, and a repeated presentation of an already-redeemed code is treated as a security event under MJD-SEC-0009.

## 3. Token Types and Lifetimes

3.1 The following lifetimes are normative and are enforced by the authorization server configuration. They are not tunable by individual applications.

| Token | Maximum lifetime | Renewable | Storage |
|---|---|---|---|
| Access token (user) | 15 minutes | via refresh token | Memory only on client, never persisted |
| Access token (service, client-credentials) | 15 minutes | re-request | Memory only |
| ID token | 10 minutes | re-authenticate | Memory only |
| Refresh token | 12 hours | rotated on each use | Server-side, encrypted at rest |
| Authorization code | 60 seconds | single use | Never stored by client |

3.2 Refresh tokens are rotated on every use: each refresh issues a new refresh token and invalidates the prior one. Detection of a reused (already-rotated) refresh token revokes the entire token family and is raised as a security event per MJD-SEC-0009.

3.3 Access tokens are never persisted to disk, local storage, cookies readable by script, or logs. They live in memory for their 15-minute lifetime.

3.4 The short 15-minute access-token lifetime is the bank's primary compensating control against token theft; it bounds the window of a leaked access token. Service-to-service callers re-request tokens on expiry rather than caching beyond the lifetime.

3.5 Clock skew tolerance across all lifetime checks is fixed at 60 seconds. No application may widen this window to mask a misconfigured clock; time synchronization is a platform responsibility, not a per-application waiver.

## 4. Token Format and Validation

4.1 Access and ID tokens are signed JWTs using `RS256` or `ES256`. The `none` algorithm is rejected unconditionally. Symmetric `HS256` is not accepted for tokens issued by the AS, because a shared symmetric key gives every verifier the power to forge.

4.2 Every resource server validates, on every request, all of the following before honoring a token. Failure of any check rejects the request with 401.

4.2.1 Signature verifies against the AS's published JWKS, with key rotation honored via the `kid` header.

4.2.2 `iss` (issuer) equals the bank's authorization server issuer URL exactly.

4.2.3 `aud` (audience) contains the resource server's own identifier. A token minted for a different audience is rejected.

4.2.4 `exp` (expiry) is in the future and `nbf`/`iat` are sane (not in the future beyond clock skew tolerance of 60 seconds).

4.2.5 The token has not been revoked, checked against the AS revocation signal for security-critical operations.

4.3 Resource servers cache the JWKS but refresh it on a `kid` miss to handle key rotation gracefully. Signing keys at the AS are rotated on the schedule defined in the Secrets and Key Management Policy (MJD-TEC-0004).

4.4 The algorithm is selected from the JWKS key type, never from the token header alone. A resource server must reject a token whose header `alg` does not match the algorithm bound to the key identified by `kid`, which closes the algorithm-confusion class of attack.

### 4.5 JWT Claims Reference

The following claims are recognized. Required claims must be present and must pass their validation rule or the request is rejected.

| Claim | Meaning | Required | Validation rule |
|---|---|---|---|
| `iss` | Issuer | Required | Exact string match to the AS issuer URL |
| `sub` | Subject (principal id) | Required | Non-empty, stable, maps to a known principal |
| `aud` | Audience | Required | Must contain this resource server's identifier |
| `exp` | Expiry | Required | In the future allowing 60s skew |
| `iat` | Issued at | Required | Not in the future beyond 60s skew |
| `nbf` | Not before | Optional | If present, current time is at or after it within 60s skew |
| `jti` | Token id | Required | Unique; used for replay detection on sender-constrained tokens |
| `scope` | Granted scopes | Required (access) | Space-delimited; requested action maps to a granted scope |
| `amr` | Auth methods references | Conditional | Required for step-up; must list an approved factor |
| `auth_time` | Time of authentication | Conditional | Required for step-up; within the operation freshness window |
| `acr` | Authentication context class | Conditional | Required for step-up; meets or exceeds the required level |
| `azp` | Authorized party | Optional | If present, equals the `client_id` that obtained the token |

4.6 ID tokens additionally carry `nonce`, which the client validates against the value it generated in the authorization-code flow. An ID token is never accepted by a resource server as an API authorization credential; only access tokens authorize API calls.

## 5. Client Credentials Walkthrough

5.1 Service-to-service callers use the client-credentials grant. There is no user and no refresh token; the caller re-requests an access token on expiry.

1. The calling service authenticates to the AS `/token` endpoint with `grant_type=client_credentials` and its client authentication material (a managed secret or, preferably, an mTLS client certificate).
2. The service requests only the scopes its registration permits, following least privilege.
3. The AS issues an access token with a 15-minute lifetime, an `aud` naming the target resource server, and an `azp` naming the calling client.
4. The caller presents the access token to the resource server, which runs the full section 4.2 validation.
5. On expiry the caller obtains a fresh token; it never caches a token beyond its 15-minute lifetime and never shares a token across distinct callers.

5.2 High-value service tokens (for example, tokens that authorize payment submission or ledger posting) are sender-constrained per section 6 so that a stolen bearer token cannot be replayed by a different sender.

## 6. Sender-Constrained Tokens

6.1 By default an access token is a bearer token: whoever holds it may use it. For high-value service-to-service paths the bank binds the token to the caller so that possession alone is insufficient.

6.2 Two binding mechanisms are approved:

| Mechanism | Binding | Where used |
|---|---|---|
| mTLS-bound tokens (RFC 8705) | Token bound to the client certificate thumbprint in `cnf.x5t#S256` | Service-to-service over mutual TLS |
| DPoP (RFC 9449) | Token bound to a client-held key; each request carries a signed DPoP proof over method, URL, and a unique `jti` | Confidential clients where mTLS is impractical |

6.3 A resource server receiving a sender-constrained token verifies the binding: for mTLS-bound tokens, the presenting TLS client certificate thumbprint matches the `cnf` claim; for DPoP, the proof signature, the bound public key, the HTTP method and URI, and the freshness and uniqueness of the proof `jti` all verify. A binding failure rejects the request even when the token signature is otherwise valid.

6.4 Sender-constraint is mandatory for tokens authorizing money movement between services and is recommended for all internal service tokens.

## 7. Authorization Model

7.1 Authorization is two-layered and deny-by-default. A request is permitted only when an explicit grant covers it; absence of a grant is a denial. Scopes grant coarse capability (`accounts.read`, `payments.write`). Fine-grained, object-level authorization is enforced in the resource server against the principal's entitlements; a valid scope never alone authorizes access to a specific object.

7.2 The model combines role-based access control (RBAC) and attribute-based access control (ABAC). RBAC resolves what a role may do; ABAC then evaluates request attributes (account ownership, transaction amount, channel, customer segment, time of day) to allow or deny the specific request. Both must permit the action.

7.3 Scopes follow least privilege. A client is granted only the scopes it demonstrably needs, recorded in its registration and reviewed at least annually.

7.4 Roles and entitlements are sourced from the authoritative identity store, not embedded as long-lived claims. Where roles appear as claims for performance, they are short-lived (bounded by the 15-minute access-token lifetime) so a revoked role takes effect within one token cycle.

### 7.5 Scope to Entitlement Mapping

The table below illustrates how a coarse scope narrows to an object-level entitlement check. The scope is necessary but never sufficient.

| Scope | Capability granted | Entitlement check in resource server |
|---|---|---|
| `accounts.read` | Read account data | Principal owns or is delegated on the specific account id |
| `payments.write` | Initiate a payment | Principal owns the debit account and the amount is within the principal limit (ABAC) |
| `payees.write` | Add or change a payee | Step-up assurance present and `auth_time` within 5 minutes |
| `statements.read` | Read statements | Principal owns the account; document not legal-hold restricted |
| `admin.users.read` | Read user records | Caller holds an employee role with a matching ABAC business-unit attribute |

7.6 Object-level checks are enforced on every read and write, including list endpoints, to prevent insecure direct object reference. A scope check alone never satisfies authorization for a specific resource.

## 8. Assurance Levels and Step-Up

8.1 Step-up authentication is required for high-risk operations. The AS asserts the strength of the authentication in `acr` and its recency in `auth_time`. The resource server denies the operation unless both the required level and the freshness window are satisfied.

| `acr` level | Meaning | Example operations | Freshness window |
|---|---|---|---|
| `aal1` | Single factor | Read-only, low-risk views | Session lifetime |
| `aal2` | MFA, phishing-resistant preferred | Standard money movement, profile edits | 12 hours |
| `aal3` | Hardware-backed phishing-resistant factor | Payee changes, raising transfer limits, admin actions | 5 minutes |

8.2 Changing a payee or raising a transfer limit requires `aal3` with `auth_time` within the last 5 minutes. A token old enough to fall outside the window forces re-authentication for that operation even though the session remains otherwise valid.

8.3 The freshness check uses `auth_time`, not `iat`. A refreshed access token carries a newer `iat` but the original `auth_time`, so refresh alone cannot satisfy a step-up requirement; only a fresh authentication can.

## 9. Multi-Factor Authentication

9.1 Multi-factor authentication is mandatory for all employee access and for all customer money-movement operations. Phishing-resistant factors (FIDO2/WebAuthn) are the preferred second factor; SMS one-time passcodes are permitted only as a fallback and are being deprecated.

9.2 MFA assertion is carried in the `amr` (authentication methods references) claim and is validated by resource servers for step-up operations. An operation requiring a phishing-resistant factor is denied when `amr` indicates only a deprecated factor such as SMS OTP.

9.3 FIDO2/WebAuthn enrollment is offered at first login for customers and is mandatory at onboarding for employees, aligned with the IAM Policy (MJD-SEC-0003).

## 10. Client Registration and Secrets

10.1 Every OAuth2 client is registered with the AS with a fixed set of redirect URIs (exact match, no wildcards on public clients), permitted grant types, and granted scopes.

10.2 Redirect URI matching is exact, including scheme, host, port, and path. No wildcard, no prefix match, and no open redirect through a registered URI parameter. This is the primary control against authorization-code interception via a forged redirect.

10.3 Confidential client secrets are managed under the Secrets and Key Management Policy (MJD-TEC-0004) and rotated on the standard service-account secret rotation cadence. Client secrets are never embedded in mobile or browser apps, which are public clients and rely on PKCE instead.

## 11. Signing Key Management

11.1 The AS holds its token-signing private keys in the platform key management service (KMS); private key material is non-exportable and never appears in application configuration. The full lifecycle, custody, and rotation cadence are governed by the Secrets and Key Management Policy (MJD-TEC-0004).

11.2 Each signing key has a stable `kid` published in the JWKS. Rotation uses an overlap window: the new key is published in the JWKS and begins signing only after verifiers have had time to fetch it, while the previous key remains in the JWKS until every token it signed has expired. This guarantees no valid token is orphaned mid-rotation.

11.3 Resource servers cache the JWKS and refresh it on a `kid` miss, with a minimum refresh interval to prevent a flood of forged `kid` values from being used as a denial-of-service amplifier against the JWKS endpoint.

11.4 A suspected signing-key compromise triggers emergency rotation and revocation under MJD-TEC-0004 and is escalated as an incident under the Incident Response Plan (MJD-SEC-0006).

## 12. Session and Cookie Security

12.1 Browser sessions backed by these tokens use hardened cookies for any server-side session reference. Refresh tokens are never exposed to client-side script.

| Attribute | Setting | Reason |
|---|---|---|
| `Secure` | On | Cookie sent only over TLS |
| `HttpOnly` | On | Not readable by script, mitigates token theft via XSS |
| `SameSite` | `Strict` | Defeats cross-site request forgery on session cookies |
| Name prefix | `__Host-` | Binds the cookie to the host with a secure, path-scoped origin |
| `Max-Age` | 43200 seconds (12 hours) | Aligns to the absolute session lifetime |
| `Path` | `/` | Required for the `__Host-` prefix |

12.2 Idle session timeout for employee applications is 15 minutes; absolute session lifetime is 12 hours, after which re-authentication is required, aligning with the refresh-token lifetime in section 3.

12.3 Logout clears the server-side session reference and revokes the associated refresh-token family at the AS, so a logged-out session cannot be silently refreshed.

## 13. Threat and Abuse Mitigations

13.1 The controls in this standard map to concrete attacks. The table below states the control of record for each.

| Threat | Attack | Control |
|---|---|---|
| Token theft | Stolen bearer access token replayed | 15-minute lifetime; memory-only storage; sender-constraint for high-value tokens (section 6) |
| Token replay | Captured token or proof reused | `exp`/`nbf`/`iat` checks; `jti` uniqueness on DPoP; revocation check on critical operations |
| CSRF | Forged cross-site request | `SameSite=Strict` cookies; `state` parameter on the authorization-code flow |
| Open redirect | Code sent to an attacker URI | Exact-match redirect URIs, no wildcards (section 10.2) |
| Mix-up attack | Client confused about which AS issued a code | `iss` validation; per-AS client configuration; single registered issuer |
| Authorization code injection | Attacker injects a stolen code | PKCE `S256` binding; single-use 60-second code |
| Algorithm confusion | Forged token with attacker-chosen `alg` | `none` rejected; HS256 not accepted; `alg` bound to the JWKS key by `kid` (section 4.4) |
| Refresh-token theft | Long-lived credential exfiltrated | Rotation on use; family revocation on reuse detection (section 3.2) |
| Phishing of a second factor | Real-time relay of an OTP | FIDO2/WebAuthn preferred; SMS OTP deprecated; `amr` enforced for step-up |

13.2 Every rejection in this section is logged with sufficient context for detection and is forwarded to the SIEM per MJD-SEC-0009. Repeated rejections from a single principal or client are correlated for credential-stuffing and token-replay patterns.

## 14. Roles and Responsibilities

**Software Engineer.** Implements the approved flows exactly as specified in sections 2 and 5, including correct PKCE `S256` generation, `state` and `nonce` handling, and exact redirect URIs. Performs the full token-validation checklist in section 4.2 on every request, including the `alg`-to-`kid` binding check. Never persists access tokens and never logs token contents. Integrates step-up assurance and `auth_time` freshness checks for high-risk operations, and implements sender-constraint verification where the path requires it.

**Security Architect.** Owns the authorization-server configuration policy, the scope catalog, and the assurance-level matrix. Reviews every new client registration, redirect-URI set, and scope grant before it is provisioned, and reviews each grant annually. Owns the identity-plane threat model in section 13, approves any device-flow use, and approves which service paths require sender-constrained tokens. Coordinates signing-key rotation policy with the owner of MJD-TEC-0004.

**Head of Platform Engineering.** Owner of this standard, accountable for the integrity of the authentication and authorization plane, for enforcement of the non-waivable controls, and for ensuring the AS configuration matches this document.

## 15. Exceptions and Escalation

15.1 No exception is granted to: the prohibition of the implicit and password grants, the mandatory PKCE `S256` requirement, the 15-minute access-token ceiling, the rejection of the `none` algorithm and non-acceptance of HS256, the full token-validation checklist in section 4.2, exact-match redirect URIs on public clients, or the prohibition on persisting access tokens. These are non-waivable.

15.2 Other deviations require an exception approved by a Security Architect and the Head of Platform Engineering, with a documented compensating control and a remediation date. Exceptions are time-boxed and re-reviewed at expiry.

15.3 A token-validation bypass, an accepted `none`-algorithm token, a leaked refresh token, a redeemed-code replay, or a suspected signing-key compromise is a security incident escalated under the Incident Response Plan (MJD-SEC-0006).

## 16. Related Documents

- MJD-TEC-0001, Secure SDLC Policy
- MJD-TEC-0002, Public and Internal API Standard
- MJD-TEC-0004, Secrets and Key Management Policy
- MJD-SEC-0003, Identity and Access Management (IAM) Policy
- MJD-SEC-0006, Incident Response Plan
- MJD-SEC-0009, Logging, Monitoring, and SIEM Standard

## 17. Regulatory References

- RFC 6749, The OAuth 2.0 Authorization Framework
- RFC 7636, Proof Key for Code Exchange (PKCE)
- RFC 8705, OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens
- RFC 9449, OAuth 2.0 Demonstrating Proof of Possession (DPoP)
- OpenID Connect Core 1.0
- NIST SP 800-63B, Digital Identity Guidelines: Authentication and Lifecycle Management
- PCI DSS 4.0, Requirement 8 (Identify Users and Authenticate Access)

## 18. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2022-05-14 | Platform Engineering | Initial OAuth2/OIDC standard. |
| 2.0.0 | 2023-11-01 | Platform Engineering | Mandated PKCE; prohibited implicit and password grants. |
| 2.2.0 | 2024-12-09 | Platform Engineering | Set 15-minute access-token ceiling and refresh-token rotation. |
| 2.3.0 | 2025-09-15 | Platform Engineering | Added phishing-resistant MFA preference and step-up rules. |
| 2.4.0 | 2026-02-10 | Platform Engineering | Reclassified CONFIDENTIAL; codified full token validation checklist and token lifetime table. |
