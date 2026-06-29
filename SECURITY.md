# Security Policy

> **FICTIONAL SYSTEM:** Meridian John Doe Financial does not exist. All data, documents, policies, and identifiers in this repository are synthetic. See NOTICE.md for the full disclaimer.

---

## Scope

This security policy applies to the `meridian-jd-rag` repository. It covers vulnerabilities in:

- The RAG query pipeline (access control enforcement, injection defense, PII handling)
- The ingestion pipeline (metadata validation, PII redaction)
- The API (authentication bypass, injection endpoints)
- The provider abstraction (secrets handling, key leakage)
- Infrastructure configuration (`docker-compose.yml`, Dockerfiles)

---

## Fictional data notice

Everything in `corpus/`, `data/`, `evals/`, and all example outputs is **synthetic and fictional**. There are intentionally planted test artifacts:

- A **prompt-injection canary**: a document line that attempts to issue instructions to an AI assistant. This is a test fixture to verify the system ignores it.
- A **synthetic-PII canary**: fabricated personal data (SSN, account number) in a marked test record. Used to verify PII never leaks into logs or output.
- A **near-duplicate superseded pair** (MJD-OPS-0007 current, MJD-OPS-0009 superseded): used to verify version handling.

These are not security incidents. Reporting them as vulnerabilities will receive a polite no-action response.

---

## Responsible disclosure

If you discover a genuine security vulnerability in the system architecture or code (not the test fixtures), please report it via:

**Email:** theimpressionzbox@gmail.com

**Subject line:** `[SECURITY] meridian-jd-rag: <brief description>`

Please include:
- A description of the vulnerability and the affected component
- Steps to reproduce
- Your assessment of the severity and impact
- Whether you have a proposed fix

You will receive an acknowledgement within 5 business days.

---

## Known limitations and accepted risks

The following are documented, accepted risks for a portfolio demonstration context. They are not actionable for a responsible disclosure:

- No HTTP-layer rate limiter at the FastAPI API (application-level rate limiting is present; an API gateway layer would be needed for production).
- Timing-based membership inference (T-04 in `security/THREAT_MODEL.md`): the system does not attempt to hide that different roles see different content.
- Default Postgres credentials `mjd:mjd` in `docker-compose.yml`: this is an example credential for local development.
- Debug trace (`observability.debug_trace: false` by default): if enabled in a misconfigured production deployment, raw queries would be stored for up to 7 days.

---

## Security contacts

For responsible disclosure: theimpressionzbox@gmail.com

For questions about the security architecture (not vulnerabilities): read `security/THREAT_MODEL.md` first, then open a GitHub Discussion.
