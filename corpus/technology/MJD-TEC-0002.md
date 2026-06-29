---
doc_id: MJD-TEC-0002
title: Public and Internal API Standard
department: TECHNOLOGY
doc_type: STANDARD
classification: INTERNAL
owner_role: Head of Platform Engineering
allowed_roles: [SOFTWARE_ENGINEER, SECURITY_ARCHITECT, OPERATIONS_ANALYST]
effective_date: 2026-02-01
version: 3.3.0
review_cycle_months: 12
regulatory_refs: ["PCI DSS 4.0 Requirement 6.2", "OWASP API Security Top 10 (2023)", "NIST SP 800-204", "FFIEC Information Security Booklet"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Public and Internal API Standard

## Purpose and Scope

This standard defines how Application Programming Interfaces (APIs) are designed, secured, versioned, documented, and operated at Meridian John Doe Financial. It applies to every HTTP API the bank exposes, whether to external partners, to customer-facing applications, or strictly to other internal services. The objective is a consistent, secure, and observable API surface that an engineer can reason about, an operations analyst can troubleshoot, and a security architect can defend.

The standard applies to:

1. Public APIs exposed to the internet, including partner and open-banking interfaces.
2. Internal APIs exposed only inside the bank's trust boundaries, including service-to-service calls.
3. Backend-for-frontend (BFF) layers that aggregate downstream services for a specific client.

It does not cover message-bus or event-streaming contracts, which are governed separately, although the authentication and data-classification rules here apply equally to any synchronous request-response interface built on those transports.

This standard is binding on all teams in Technology and Platform Engineering. Operations analysts are granted read access because they rely on the standard to interpret API behavior, rate-limit responses, and error semantics during incident triage. Where this standard overlaps with the Secure SDLC Policy (MJD-TEC-0001), the design-review and pipeline-gate requirements there apply in addition to the API-specific gates defined here.

## Definitions

**Public API.** An API reachable from outside the bank's network perimeter, terminating at an internet-facing API gateway.

**Internal API.** An API reachable only from within the bank's private network or service mesh, never exposed to the internet.

**API gateway.** The managed ingress component that terminates TLS, authenticates callers, enforces rate limits, and routes to backend services.

**Idempotency key.** A client-supplied unique value that lets the server safely de-duplicate a retried write so the same operation is not performed twice.

**Breaking change.** Any change that can cause a conforming existing client to fail: removing or renaming a field, tightening validation, changing a status code's meaning, or altering authentication requirements.

**Service-to-service token.** A short-lived OAuth2 access token obtained by a service to call another service, issued under the Authentication and Authorization Standard (MJD-TEC-0003).

**Cursor.** An opaque, server-issued token that encodes a position in a result set for pagination. A cursor is never a raw database offset or primary key.

**Persisted query.** A GraphQL operation registered ahead of time and invoked by a stable identifier, so the runtime executes only operations that have already been reviewed.

## 1. Transport and Connectivity

1.1 All APIs, public and internal, are served exclusively over TLS 1.2 or higher. Plaintext HTTP is rejected at the gateway and is never used between internal services.

1.2 Public APIs terminate at the internet-facing gateway, which enforces HTTP Strict Transport Security with a max-age of at least 31536000 seconds (one year) including subdomains.

1.3 Internal service-to-service calls use mutual TLS within the service mesh where the mesh is deployed; where it is not, callers authenticate with a service-to-service token (section 3).

1.4 The gateway negotiates only AEAD cipher suites and disables renegotiation. Certificate and key material used for TLS termination and mTLS is managed exclusively under the Secrets and Key Management Policy (MJD-TEC-0004); private keys are never embedded in application images or configuration files.

## 2. Resource Design and Versioning

2.1 APIs follow RESTful resource conventions: nouns for resources, standard HTTP verbs, and meaningful status codes. GraphQL is permitted only for read-heavy aggregation BFFs and is subject to the query depth and complexity limits in section 13.

2.2 The major version is carried in the URL path, for example `/v2/accounts`. The current supported major versions are v1 (deprecated) and v2 (current).

2.3 Breaking changes require a new major version. Non-breaking additive changes (new optional fields, new endpoints) are made within the existing major version.

2.4 A deprecated major version is supported for a minimum of 12 months after the successor version is generally available. Deprecation is communicated with the `Deprecation` and `Sunset` response headers carrying the planned end-of-life date.

2.5 Resource collections are plural and lowercase, path segments use hyphen-free single nouns, and identifiers in paths are opaque resource identifiers, never internal database keys. Field names in request and response bodies use lower snake_case for consistency across every service.

## 3. Authentication and Authorization

3.1 Every API requires authentication. There are no anonymous endpoints except `/health` liveness probes, which return no business data.

3.2 Public APIs authenticate callers using OAuth2 bearer access tokens issued by the bank's identity provider, validated per the Authentication and Authorization Standard (MJD-TEC-0003). Access tokens have a maximum lifetime of 15 minutes.

3.3 Service-to-service calls use the OAuth2 client-credentials grant. The resulting access tokens are also short-lived (15 minutes) and are scoped to the minimum set of operations the caller needs.

3.4 Authorization is enforced at the resource level. The API checks that the authenticated principal is entitled to the specific object being acted on; object-level authorization failures return 403 or 404 per section 5 and never leak the existence of objects the caller may not see.

3.5 API keys, where used for partner identification, are never the sole authentication factor; they accompany an OAuth2 token and are treated as secrets under the Secrets and Key Management Policy (MJD-TEC-0004).

### 3.6 Token validation expectations

3.6.1 The authoritative rules for token issuance, signature algorithms, key rotation, and revocation live in MJD-TEC-0003. APIs defer to that standard and do not implement bespoke token parsing. At minimum, every resource server verifies the token signature against the published issuer keys, the issuer (`iss`) and audience (`aud`) claims, the expiry (`exp`) and not-before (`nbf`) claims with no clock skew beyond 60 seconds, and the presence of the required scopes for the operation.

3.6.2 Access tokens are never accepted from query strings or request bodies. They are presented only in the `Authorization: Bearer` header, so they do not leak into access logs, browser history, or referrer headers.

3.6.3 A token that is structurally valid but lacks the required scope returns 403. A token that is missing, expired, or fails signature or claim validation returns 401.

### 3.7 Scope naming convention

3.7.1 Scopes follow a stable three-part convention so that a reviewer can read intent from the scope string alone.

| Part | Meaning | Allowed values |
|---|---|---|
| resource | The resource family the scope grants access to | accounts, payments, cards, statements, profiles |
| action | The operation class | read, write, admin |
| qualifier | Optional narrowing of the grant | self, partner, batch |

3.7.2 Scopes are composed as `resource.action` with an optional `.qualifier`, for example `accounts.read.self`. The qualifier distinguishes a customer acting on their own data from a partner or batch process acting across many principals.

### 3.8 Scope examples per resource

| Resource | Scope | Grants |
|---|---|---|
| Accounts | `accounts.read.self` | Read the authenticated customer's own accounts |
| Accounts | `accounts.read.partner` | Read accounts a consenting customer shared with a partner |
| Payments | `payments.write.self` | Initiate a payment from the customer's own account |
| Payments | `payments.admin` | Operational reversal and reconciliation, internal only |
| Cards | `cards.read.self` | Read masked card metadata for the customer |
| Statements | `statements.read.self` | Download the customer's own statements |

3.8.3 No single client is issued both customer-acting (`self`) and cross-principal (`partner`, `batch`) scopes. Separation of these grant classes is a design-review checkpoint per MJD-TEC-0001.

## 4. Input Validation and Output Encoding

4.1 All input is validated against an explicit schema at the edge. Requests that fail schema validation are rejected with 400 before reaching business logic.

4.2 Servers reject unexpected fields rather than silently ignoring them for any write that affects money or authorization, preventing mass-assignment abuse.

4.3 All output is serialized through a defined response model. Internal fields, stack traces, and database identifiers are never serialized into responses.

4.4 String inputs carry maximum lengths, numeric inputs carry explicit ranges, and monetary amounts are validated as minor units (integer cents) with an explicit currency code. Free-text fields that may later be rendered are encoded for their output context to prevent injection downstream.

## 5. Error Semantics

5.1 Errors use a consistent body shape:

```json
{ "error": { "code": "string", "message": "human-readable, non-sensitive", "trace_id": "uuid" } }
```

5.2 Status code usage:

| Status | Meaning | Notes |
|---|---|---|
| 400 | Malformed or schema-invalid request | No retry without change |
| 401 | Missing or invalid authentication | Token expired or absent |
| 403 | Authenticated but not authorized | Used when revealing existence is acceptable |
| 404 | Not found, or hidden-for-authorization | Used when existence must not be revealed |
| 409 | Conflict, including idempotency-key reuse with different body | |
| 422 | Semantically invalid (valid schema, invalid values) | |
| 429 | Rate limit exceeded | Carries `Retry-After` |
| 5xx | Server error | Never leaks internal detail |

5.3 Error messages never contain customer PII, secret material, SQL, or internal hostnames.

5.4 The machine-readable `error.code` is drawn from a fixed, documented vocabulary per service so that clients can branch on a stable string rather than parsing human text. New codes are additive and are published in the OpenAPI contract.

## 6. Rate Limiting and Quotas

6.1 Every public endpoint is rate-limited at the gateway. Default public limits are 100 requests per minute per authenticated principal for read operations and 30 requests per minute for write operations, tunable per endpoint.

6.2 Rate-limited responses return 429 with a `Retry-After` header and a `X-RateLimit-Remaining` header. Operations analysts rely on these headers during incident triage, which is why they have read access to this standard.

6.3 Money-movement endpoints additionally enforce per-principal daily caps coordinated with the operational limits in MJD-OPS-0007, Transaction Limits and Dual-Approval Matrix.

6.4 Rate-limit counters are keyed on the authenticated principal, not on source IP alone, so that a shared egress address cannot exhaust another tenant's budget. The gateway publishes `X-RateLimit-Limit` and `X-RateLimit-Reset` alongside the remaining count so a well-behaved client can self-throttle before it is rejected.

## 7. Idempotency and Concurrency

7.1 Every non-idempotent write endpoint (POST that creates, money movement) accepts an `Idempotency-Key` header. The server stores the key and the response for at least 24 hours and returns the original response on a retry with the same key.

7.2 Reuse of an idempotency key with a different request body returns 409.

7.3 Optimistic concurrency on mutable resources uses `ETag` and `If-Match`; a mismatch returns 412.

7.4 Idempotency keys are scoped to the authenticated principal and the target endpoint; a key presented by one principal can never replay another principal's stored response. Keys are required to be client-generated UUIDs and are rejected if they exceed 128 characters.

## 8. Pagination, Filtering, and Sorting

8.1 List endpoints use cursor-based pagination. The client sends `page[size]` and an opaque `page[cursor]`; the server returns the next cursor and a flag indicating whether more results exist. Offset-based pagination is not used for large or security-sensitive collections because it is unstable under concurrent writes and can leak total counts.

8.2 The default page size is 25 and the maximum is 100. A request for more than the maximum is clamped to the maximum rather than rejected, and the response indicates the effective size.

8.3 Filtering uses an allowlist of fields per resource, expressed as `filter[field]=value`. Unknown filter fields are rejected with 400 so that a client cannot probe for unindexed or unauthorized attributes.

8.4 Sorting uses `sort=field` for ascending and `sort=-field` for descending, restricted to an allowlist of sortable fields. At most two sort keys are accepted per request to bound query cost.

8.5 Cursors are signed and time-bounded. A tampered or expired cursor returns 400 and the client restarts the listing from the beginning.

## 9. Request and Response Header Standards

9.1 The bank standardizes a common set of headers across every API so that tracing, content negotiation, caching, and browser-facing protections behave identically everywhere.

| Header | Direction | Purpose |
|---|---|---|
| `Authorization` | Request | Bearer access token; only accepted transport for the token |
| `X-Correlation-Id` | Request and response | Client-supplied correlation identifier echoed back; generated by the gateway if absent |
| `traceparent` | Request and response | W3C Trace Context for distributed tracing across services |
| `Idempotency-Key` | Request | De-duplicates retried writes (section 7) |
| `Content-Type` | Request and response | `application/json` is the default; charset is UTF-8 |
| `Accept` | Request | Drives content negotiation; unsupported types return 406 |
| `ETag` / `If-Match` | Response / request | Optimistic concurrency (section 7) |
| `Cache-Control` | Response | `no-store` for authenticated, principal-specific resources |
| `X-Content-Type-Options` | Response | `nosniff` on every response |
| `X-RateLimit-Remaining` | Response | Remaining quota in the current window (section 6) |
| `Deprecation` / `Sunset` | Response | Lifecycle signaling for deprecated versions (section 2) |

9.2 Responses that carry customer-specific data set `Cache-Control: no-store` to prevent shared caches from retaining one principal's data. Public, non-sensitive reference data may set a short `max-age`.

9.3 The gateway strips inbound hop-by-hop and infrastructure headers that a client must not control, including any attempt to spoof internal trust headers.

## 10. Webhook and Callback Security

10.1 Webhooks the bank sends to partners are signed. Each delivery carries an `X-MJD-Signature` header containing an HMAC over the raw request body using a per-partner signing secret managed under MJD-TEC-0004. Receivers must verify the signature against the raw bytes before parsing.

10.2 Each delivery carries an `X-MJD-Timestamp` and a unique `X-MJD-Delivery-Id`. Receivers reject deliveries whose timestamp is outside a five-minute window and de-duplicate on the delivery identifier to defeat replay.

10.3 Deliveries are retried with exponential backoff and jitter on 5xx or timeout, up to a bounded number of attempts over 24 hours, after which the delivery is parked for manual replay. Webhook endpoints are expected to respond within five seconds and to acknowledge before performing heavy downstream work.

10.4 Inbound callbacks the bank receives from partners are subject to the same controls in reverse: signature verification, timestamp and nonce checks, and source allowlisting at the gateway.

## 11. API Lifecycle and Governance

11.1 Every API has a named owning team and a registered entry in the API catalog. An API without a catalog entry, an OpenAPI contract, and an owner is not permitted in production.

11.2 New public APIs and any change to authentication, authorization, or data classification pass a design review with a Security Architect before build, consistent with the Secure SDLC Policy (MJD-TEC-0001). The review confirms scope design, error semantics, rate limits, and data classification per MJD-SEC-0008.

11.3 The API catalog records, for each API, its owner, supported versions, deprecation state, data classification, and the scopes it requires. The catalog is the source of truth for partner onboarding and for incident routing.

11.4 Service level objectives are tracked per API and reviewed monthly. The default targets below apply unless a service publishes stricter ones in its catalog entry.

| Tier | Availability | Latency p50 | Latency p95 | Latency p99 |
|---|---|---|---|---|
| Tier 1 (money movement) | 99.95% | 120 ms | 400 ms | 800 ms |
| Tier 2 (customer read) | 99.9% | 80 ms | 250 ms | 600 ms |
| Tier 3 (internal support) | 99.5% | 150 ms | 500 ms | 1200 ms |

11.5 Latency targets are measured at the gateway and exclude client network time. Sustained breach of an SLO opens an error-budget review with the owning team and feeds the operational reporting in MJD-OPS-0007.

## 12. Security Controls Mapped to OWASP API Security Top 10 (2023)

12.1 The bank maps each OWASP API Security Top 10 (2023) risk to the concrete control this standard mandates.

| Risk | Control applied |
|---|---|
| API1 Broken Object Level Authorization | Per-object authorization check on every access; 403/404 hiding (section 3.4) |
| API2 Broken Authentication | OAuth2 bearer tokens, 15-minute max lifetime, signature and claim validation (section 3) |
| API3 Broken Object Property Level Authorization | Explicit response models; mass-assignment rejection on sensitive writes (section 4) |
| API4 Unrestricted Resource Consumption | Gateway rate limits, page-size caps, GraphQL complexity budget (sections 6, 8, 13) |
| API5 Broken Function Level Authorization | Scope-gated operations; separation of self and admin scopes (section 3.7) |
| API6 Unrestricted Access to Sensitive Business Flows | Per-principal daily caps and dual approval via MJD-OPS-0007 |
| API7 Server Side Request Forgery | Outbound allowlisting; no user-supplied URLs fetched without validation |
| API8 Security Misconfiguration | Mandatory security headers, TLS floor, no debug surfaces (sections 1, 9) |
| API9 Improper Inventory Management | API catalog with owners, versions, and deprecation state (section 11) |
| API10 Unsafe Consumption of APIs | Signature and timestamp checks on inbound callbacks (section 10) |

12.2 New risks published in future OWASP revisions are triaged by the Security Architect community and folded into this table at the next review cycle.

## 13. GraphQL BFF Limits

13.1 GraphQL is permitted only for read-heavy aggregation BFFs (section 2.1) and is governed by hard runtime limits that bound the cost of any single operation.

13.2 Query depth is capped at 8 levels. A query exceeding the depth limit is rejected before execution.

13.3 Each query is scored against a complexity budget that weights fields and list multipliers; a query exceeding the budget is rejected with a 400-class error rather than partially executed.

13.4 In production, only persisted queries are accepted: clients send a registered operation identifier, and ad hoc queries are refused. This narrows the executable surface to operations that passed design review.

13.5 Schema introspection is disabled in production. Introspection remains available in the sandbox so partners can explore the schema during integration.

13.6 GraphQL endpoints inherit the same authentication, scope checks, rate limits, and tracing requirements as REST endpoints; the BFF resolves each field only after confirming the principal's entitlement to it.

## 14. Partner and Open-Banking Onboarding

14.1 Partner and open-banking interfaces require mutual TLS in addition to OAuth2. The partner presents a client certificate issued or pinned through the process in MJD-TEC-0004, and the gateway rejects connections whose certificate is unknown, expired, or revoked.

14.2 Each partner is bound to an IP allowlist at the gateway. Production access is granted only after the partner completes integration in the sandbox environment, which mirrors production contracts but uses synthetic data.

14.3 Partners receive per-partner quotas distinct from the default per-principal limits in section 6, sized to their contracted volume and tunable without a code change. Quota breaches return 429 and are visible to operations analysts for triage.

14.4 Partner scopes are limited to the `partner` qualifier (section 3.7) and are reviewed by a Security Architect before activation. Partner credentials and signing secrets are rotated on the schedule defined in MJD-TEC-0004.

## 15. Documentation and Contracts

15.1 Every API publishes an OpenAPI 3.x specification as its contract. The specification is generated from or validated against the running service in the pipeline; documentation drift is a pipeline failure.

15.2 The contract records authentication requirements, scopes, rate limits, and the data classification of each field per MJD-SEC-0008.

15.3 The contract is the artifact registered in the API catalog (section 11) and the basis for partner sandbox access (section 14). A change to the contract that constitutes a breaking change triggers the versioning rules in section 2.

## 16. Observability

16.1 Every request and response carries a `trace_id` propagated end to end. The trace_id appears in logs and error bodies so an operations analyst can correlate a customer report to a server-side trace.

16.2 Logs follow the Logging, Monitoring, and SIEM Standard (MJD-SEC-0009). Request and response bodies are never logged in full; PII fields are redacted before any durable log write.

16.3 The gateway emits per-endpoint metrics for request rate, error rate, and the latency percentiles used to evaluate the SLOs in section 11. These feeds back the error-budget reviews and the incident triage workflows operations analysts depend on.

## 17. Roles and Responsibilities

**Software Engineer.** Designs APIs to this standard, publishes and maintains the OpenAPI contract, implements authentication, validation, idempotency, pagination, and rate limiting. Registers each API in the catalog and keeps its SLO targets current.

**Security Architect.** Reviews public API designs and any change to authentication or authorization, owns the threat models for the API gateway, approves partner scope grants, and maintains the OWASP control mapping in section 12.

**Operations Analyst.** Uses error semantics, rate-limit headers, trace_ids, and the SLO dashboards to triage incidents; tracks SLO breaches against error budgets and reports systemic API defects to the owning team. Default SLO targets the analyst monitors are 99.95% availability for Tier 1 money-movement APIs, 99.9% for Tier 2 customer-read APIs, and 99.5% for Tier 3 internal support APIs.

**Head of Platform Engineering.** Owner of this standard, accountable for the consistency and security of the overall API surface and for the integrity of the API catalog.

## 18. Exceptions and Escalation

18.1 Deviations require an exception record approved by the Head of Platform Engineering and a Security Architect before deployment.

18.2 No exception is granted to the requirements that all APIs use TLS, that all endpoints authenticate, or that money-movement endpoints support idempotency. These are non-waivable.

18.3 A public API discovered to be exposed without authentication is a security incident handled under the Incident Response Plan (MJD-SEC-0006).

18.4 An exception is time-bounded, carries a remediation date, and is recorded in the API catalog entry so that operations analysts and security architects can see the deviation during triage and review.

## 19. Related Documents

- MJD-TEC-0001, Secure SDLC Policy
- MJD-TEC-0003, Authentication and Authorization Standard (OAuth2/OIDC)
- MJD-TEC-0004, Secrets and Key Management Policy
- MJD-SEC-0008, Data Classification and Handling Standard
- MJD-SEC-0009, Logging, Monitoring, and SIEM Standard
- MJD-OPS-0007, Transaction Limits and Dual-Approval Matrix

## 20. Regulatory References

- PCI DSS 4.0, Requirement 6.2 (Secure development of bespoke software)
- OWASP API Security Top 10 (2023)
- NIST SP 800-204, Security Strategies for Microservices-based Applications
- FFIEC IT Examination Handbook, Information Security Booklet

## 21. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2022-07-10 | Platform Engineering | Initial API standard. |
| 2.0.0 | 2023-09-05 | Platform Engineering | Added OAuth2 requirement and versioning policy. |
| 3.0.0 | 2024-10-18 | Platform Engineering | Added idempotency, rate-limit, and error-semantics sections. |
| 3.2.0 | 2025-08-22 | Platform Engineering | Aligned with OWASP API Top 10 2023; tightened token lifetime to 15 minutes. |
| 3.3.0 | 2026-02-01 | Platform Engineering | Added deprecation header requirements and BFF GraphQL limits. |
