---
doc_id: MJD-TEC-0006
title: Infrastructure as Code Standard
department: TECHNOLOGY
doc_type: STANDARD
classification: INTERNAL
owner_role: Head of Platform Engineering
allowed_roles: [SOFTWARE_ENGINEER, SECURITY_ARCHITECT]
effective_date: 2026-02-25
version: 2.6.0
review_cycle_months: 12
regulatory_refs: ["NIST SP 800-53 Rev 5 (CM-2, CM-3, CM-6)", "CIS Benchmarks", "PCI DSS 4.0 Requirement 1", "SOC 2 CC8.1"]
supersedes: null
entity_status: FICTIONAL
---

> FICTIONAL DOCUMENT: Meridian John Doe Financial is a synthetic company. All content is fabricated for demonstration. See NOTICE.md.

# Infrastructure as Code Standard

## Purpose and Scope

This standard requires that all Meridian John Doe Financial cloud and platform infrastructure be defined, provisioned, and changed exclusively through version-controlled, reviewed, and tested infrastructure-as-code (IaC). Manual changes to production infrastructure are prohibited. Codifying infrastructure makes every change reviewable, every environment reproducible, and every drift detectable, which is the foundation for both reliability and demonstrable control to examiners.

This standard applies to all infrastructure provisioning: compute, networking, storage, identity and access bindings, databases, message infrastructure, secrets-manager and KMS configuration, and observability stacks. It applies across every cloud and platform the bank uses.

It is binding on all Technology and Platform Engineering teams and on any team that provisions its own infrastructure. Where a vendor-managed or SaaS control plane is used, its configuration is brought under IaC wherever the provider exposes a programmatic interface, so third-party platform settings are reviewable and reproducible rather than clicked into place by hand.

## Definitions

**Infrastructure as Code (IaC).** The practice of defining infrastructure in declarative, version-controlled configuration that a tool applies to reach the desired state.

**Module.** A reusable, versioned IaC component encapsulating a hardened pattern (for example, a compliant database or a network subnet).

**State.** The IaC tool's record of the real resources it manages. State can contain sensitive values and is itself a protected asset.

**Drift.** A divergence between the real infrastructure and the desired state declared in code, usually caused by an out-of-band manual change.

**Policy as code.** Machine-enforced guardrails that evaluate proposed infrastructure changes against security and compliance rules before they are applied.

**Landing zone.** The governed account or project baseline into which workloads are deployed (see MJD-TEC-0007, Cloud Governance and Landing Zone Policy).

**Composition.** An environment-specific assembly of one or more modules with concrete parameter values that produces the infrastructure for a single environment in a single account.

**Enforcement point.** The stage in the delivery flow at which a guardrail is evaluated: pre-merge (during pull request validation), pre-apply (immediately before the plan is applied), or runtime (continuously, against live infrastructure).

## 1. Core Principles

1.1 All infrastructure is defined as code in version control. There is no sanctioned path to create or change production infrastructure by hand in a cloud console.

1.2 Every infrastructure change flows through the same pipeline (MJD-TEC-0005) and the same review controls (MJD-TEC-0009) as application code.

1.3 Infrastructure is immutable where feasible: changes replace resources rather than mutating them in place, which removes configuration drift and makes rollback deterministic.

1.4 Environments (development, test, staging, production) are provisioned from the same code with environment-specific parameters, so staging is a faithful proxy for production.

1.5 The code is authoritative. If the live infrastructure and the code disagree, the code is correct and the live infrastructure is wrong until the divergence is either reconciled or codified through review. This single rule is what makes drift a defect rather than an accepted state of the world.

1.6 Security defaults are inherited, not configured. Engineers receive the secure outcome by composing approved modules; they do not have to remember to turn security on. An insecure configuration should require deliberate, reviewable, exception-approved effort rather than being a forgotten default.

## 2. Repository and Module Structure

2.1 IaC lives in version control with a clear separation between reusable modules and environment compositions that instantiate them. Modules are published from a dedicated module repository; compositions live alongside the service or platform they provision.

2.2 Hardened, security-reviewed modules are the only approved way to provision sensitive resources (databases holding regulated data, internet-facing load balancers, IAM roles). Teams compose approved modules rather than writing raw resource definitions for these.

2.3 Modules are versioned; a composition pins the module version it uses, so a module change does not silently alter every environment.

### 2.4 Module Standards

Every published module conforms to the following standards so that consumers receive a predictable, hardened, and supportable building block.

2.4.1 **Versioning.** Modules are versioned with semantic versioning (MAJOR.MINOR.PATCH). A MAJOR increment signals a breaking change to inputs, outputs, or default behavior; a MINOR increment adds backward-compatible capability; a PATCH increment is a backward-compatible fix. Compositions pin an exact version or a constrained range that excludes the next MAJOR, so an upgrade is always a deliberate, reviewed pull request.

2.4.2 **Required inputs and outputs.** Each module declares its inputs with explicit types, descriptions, and validation. Inputs that would weaken security (for example, a flag to allow public access) either do not exist or default to the secure value and require an exception to set otherwise. Each module exports a documented set of outputs (resource identifiers, endpoint references, role ARNs) so that compositions wire resources together through declared contracts rather than hard-coded strings.

2.4.3 **Security defaults.** Modules ship secure by default: encryption at rest is on, TLS is enforced, network exposure is private, and logging is enabled. A consumer cannot accidentally provision an unencrypted or publicly reachable resource through an approved module.

2.4.4 **Mandatory tags.** Modules accept and propagate the four mandatory tags (owner, environment, data-classification, cost-center) to every resource they create. A module that cannot tag a resource is not approved for provisioning regulated workloads.

2.4.5 **Module registry.** Approved modules are published to an internal module registry with their version, changelog, security review status, and owning team. Consumers source modules only from the registry; sourcing a module directly from an arbitrary external URL or unreviewed branch is prohibited for sensitive resources.

2.4.6 **Deprecation.** A module version is deprecated with a published end-of-support date and a documented migration path to its successor. Deprecated versions emit a pipeline warning; end-of-life versions are blocked from new applies. Security-relevant deprecations (for example, retiring a module that pins an outdated TLS policy) follow the change-workflow timelines rather than waiting for a convenient release window.

## 3. State Management and Security

3.1 IaC state is stored in a centralized, access-controlled, encrypted backend with versioning and state locking. State is never stored on a workstation or committed to source control.

3.2 State is treated as Confidential because it may contain secret references and resource details. Access to state is least-privilege and audited (MJD-SEC-0009).

3.3 Secrets are never written into IaC source or into state as plaintext. IaC references secrets in the secrets manager (MJD-TEC-0004); it does not generate and persist them in code.

### 3.4 State Security Deep-Dive

3.4.1 **Remote backend.** All state lives in a remote, server-side backend operated by Platform Engineering. There is no local state for any shared or production environment. The backend is versioned, so every state mutation is recoverable and any unintended change can be rolled back to a prior generation.

3.4.2 **Encryption.** State is encrypted at rest with KMS-managed keys and encrypted in transit over TLS. The KMS keys protecting state follow the key lifecycle and rotation requirements of MJD-TEC-0004; access to the decryption key is itself least-privilege and audited.

3.4.3 **Locking.** State locking is mandatory. Before any apply, the pipeline acquires an exclusive lock so that two concurrent applies cannot corrupt state. A stale lock is cleared only through a controlled, audited procedure, never by deleting the lock object by hand.

3.4.4 **Access control.** Read and write access to the state backend is granted to pipeline identities, not to individual engineers, and follows least-privilege. The state-backend access policy denies broad list-and-read access; an identity can reach only the state paths for the environments it is authorized to manage. All access is logged to the SIEM (MJD-SEC-0009).

3.4.5 **State contains sensitive data.** Because state can record resource attributes, references, and in some providers materialized values, the state file is classified Confidential in its entirety. State is never copied to a laptop for debugging, never pasted into a ticket or chat, and never shared outside the access-controlled backend. Sensitive outputs are marked so they are not echoed in plan or log output.

3.4.6 **No secrets in state.** Secrets are referenced by name and resolved at runtime by the consuming workload; they are not generated by IaC and persisted into state as plaintext. Where a provider would otherwise write a generated credential into state, the module is designed to delegate generation and storage to the secrets manager (MJD-TEC-0004) instead.

## 4. Environment Topology and Isolation

4.1 Environments are isolated into separate accounts or projects so that a fault, a misconfiguration, or a compromise in one environment cannot reach another. Isolation is enforced at the account and network boundary, not merely by naming convention.

4.2 The standard environment topology is the following.

| Environment | Account isolation | Network | Data | Promotion |
|---|---|---|---|---|
| Development | Separate dev account per team or domain | Private, no inbound from internet | Synthetic only | Code flows upward via pull request and pipeline |
| Test | Isolated test account, no path to production | Private, segmented from dev and prod | Synthetic only; never production data | Module tests provision and tear down here |
| Staging | Dedicated staging account, prod-like | Private, mirrors production segmentation | Synthetic or masked; no live regulated data | Built from the same code as production |
| Production | Dedicated production account(s) | Private-by-default, deny-by-default ingress | Live regulated data, access-controlled | Apply via short-lived OIDC identity only |

4.3 Production data never flows downstream into a lower environment. A lower environment that needs realistic data uses synthetic data only. There is no sanctioned process that copies a production database into development, test, or staging.

4.4 The account and landing-zone baselines that back this topology are governed by the Cloud Governance and Landing Zone Policy (MJD-TEC-0007); this standard governs how those accounts are populated and changed through code.

## 5. Policy as Code (Guardrails)

5.1 Every proposed infrastructure change is evaluated by policy-as-code before it is applied. A High-severity policy violation blocks the change. Guardrails run at the enforcement point appropriate to the rule: pre-merge to give fast feedback in the pull request, pre-apply to evaluate the concrete plan, and runtime to catch drift and out-of-band change against live infrastructure.

5.2 The mandatory guardrails include, at minimum:

| Guardrail | Rule |
|---|---|
| No public storage | Object storage buckets are private by default; public exposure requires explicit, security-approved exception |
| Encryption at rest | All data stores are encrypted with KMS-managed keys |
| Encryption in transit | TLS enforced; plaintext listeners prohibited |
| No wide-open network | Security groups and firewall rules deny by default; no 0.0.0.0/0 ingress to sensitive ports |
| Least-privilege IAM | No wildcard administrative permissions on workload roles |
| Tagging | Every resource carries owner, environment, data-classification, and cost-center tags |
| Logging enabled | Audit and flow logging enabled on all accounts and networks |

### 5.3 Guardrail Catalog

The mandatory guardrails are implemented as the following catalog. Each guardrail has an identifier, a severity, the enforcement point at which it runs, and a benchmark reference. High-severity guardrails block; Medium-severity guardrails block in production and warn in lower environments; Low-severity guardrails warn and are tracked.

| ID | Rule | Severity | Enforcement point | Benchmark reference |
|---|---|---|---|---|
| GR-STORE-01 | No public object storage; public ACL or policy denied | High | Pre-merge and pre-apply | CIS Storage, public access |
| GR-ENC-01 | Encryption at rest with KMS-managed keys on all data stores | High | Pre-merge and pre-apply | CIS encryption-at-rest |
| GR-ENC-02 | TLS enforced; plaintext or downgraded listeners prohibited | High | Pre-merge and pre-apply | CIS in-transit encryption |
| GR-NET-01 | No 0.0.0.0/0 ingress to sensitive ports; deny-by-default rules | High | Pre-merge and pre-apply | CIS network, PCI DSS Req 1 |
| GR-IAM-01 | No wildcard administrative permission on workload roles | High | Pre-merge and pre-apply | CIS IAM least-privilege |
| GR-IAM-02 | No long-lived static keys provisioned for workloads | High | Pre-apply | CIS IAM, MJD-TEC-0004 |
| GR-TAG-01 | Mandatory tags present: owner, environment, data-classification, cost-center | Medium | Pre-merge | Internal tagging baseline |
| GR-LOG-01 | Audit and flow logging enabled on accounts and networks | High | Pre-apply and runtime | CIS logging, SOC 2 CC8.1 |
| GR-STATE-01 | No secret value written to state as plaintext | High | Pre-apply | MJD-TEC-0004 |
| GR-MOD-01 | Sensitive resources provisioned only from registry modules | Medium | Pre-merge | Internal module standard |
| GR-DESTROY-01 | Destruction of a stateful production resource requires extra approval and verified backup | High | Pre-apply | MJD-TEC-0008 |
| GR-DRIFT-01 | Live infrastructure matches code; unexplained drift flagged | Medium | Runtime, daily | NIST CM-2, CM-3, CM-6 |

5.4 Guardrails align with the CIS Benchmarks for each platform and with the landing-zone controls in MJD-TEC-0007. The guardrail set is owned by the Security Architect, version-controlled, and changed through the same review path as any other code; a new guardrail is socialized and run in warn mode before it is promoted to a blocking severity, so that teams are not surprised by a new block.

### 5.5 Network and Identity Baseline

5.5.1 **Private by default.** Resources are provisioned into private network space with no inbound internet path unless an internet-facing role is the explicit, reviewed purpose of the resource. Internet-facing resources sit behind approved load-balancing and edge modules that terminate TLS and apply the deny-by-default rule set.

5.5.2 **Segmentation.** Networks are segmented so that environments and sensitivity tiers do not share a flat address space. Movement between segments is allowed only through explicit, reviewed rules; there is no implicit any-to-any reachability. This directly supports the no-wide-open-network guardrail and PCI DSS 4.0 Requirement 1.

5.5.3 **Least-privilege identity by construction.** IAM roles and identity bindings created by IaC are scoped to the specific actions and resources a workload needs. The policy-as-code guardrails reject any workload role that grants wildcard administrative permission, so an over-broad role cannot be introduced even by mistake. Roles created for the pipeline to perform applies are scoped per environment and assumed through short-lived OIDC workload identity, never backed by long-lived static keys.

## 6. Change Workflow

6.1 An infrastructure change is proposed as a pull request. The pipeline produces a plan (a preview of the exact resources to be created, changed, or destroyed) which is reviewed by a human before apply.

6.2 The plan output is attached to the change record (MJD-TEC-0008). A change that would destroy a stateful production resource requires explicit, additional approval and a verified backup.

6.3 Apply to production is performed by the pipeline using short-lived OIDC workload identity (MJD-TEC-0005 section 5), never by an engineer's personal credentials.

### 6.4 Change Procedure

The end-to-end procedure for a production infrastructure change is the following ordered sequence. No step may be skipped, and a failure at any gate stops the change.

6.4.1 **Propose.** The engineer opens a pull request against the composition, pinning module versions and parameters. CODEOWNERS routing (MJD-TEC-0009) requires the appropriate reviewers, including a Security Architect for security-sensitive resources.

6.4.2 **Plan.** The pipeline generates a plan showing the exact create, change, and destroy actions. The plan is deterministic and attached to the change record (MJD-TEC-0008).

6.4.3 **Policy check.** Policy-as-code evaluates the plan at the pre-merge and pre-apply enforcement points. A High-severity violation blocks; the change cannot proceed until it is resolved or an approved exception covers it.

6.4.4 **Human review.** A human reviews the plan. The reviewer confirms the plan matches the intended change, that no unexpected destroy actions appear, and that any destructive action against a stateful production resource carries the section 6.2 additional approval and a verified backup.

6.4.5 **Approval.** The change is approved in the change record. For a destroy of a stateful production resource, the additional approver and the backup verification are recorded.

6.4.6 **Apply via OIDC.** The pipeline assumes a scoped, short-lived OIDC workload identity for the specific apply and applies the reviewed plan. No engineer's personal credentials are used. State locking (section 3.4.3) prevents a concurrent apply.

6.4.7 **Post-apply drift baseline.** Immediately after apply, the pipeline records a drift baseline so that subsequent daily drift scans (section 7) compare against the known-good state established by this change.

## 7. Drift Detection and Remediation

7.1 Automated drift detection runs at least daily against production. Detected drift raises an alert to the owning team and to the SIEM (MJD-SEC-0009).

7.2 Drift is remediated by reconciling the real infrastructure back to code, or by codifying the intentional change through the normal review path. The team chooses based on intent: if the live change was unintended, code is reapplied to restore the declared state; if it was a legitimate change that bypassed process, it is captured as a pull request so the code becomes authoritative again.

7.3 Manual out-of-band changes that caused the drift are investigated. A single accidental change is corrected and recorded. Repeated unauthorized manual changes by the same actor or team are escalated as a security and change-management concern (MJD-TEC-0008) and may result in access being revoked; the console offers no durable benefit, because anything done by hand is detected within a day and reverted.

7.4 Drift detection runs against all production accounts continuously enough that no out-of-band change survives a full day undetected. Lower environments are scanned on a schedule appropriate to their risk.

## 8. Testing

8.1 IaC is validated in the pipeline: syntax and lint checks, policy-as-code evaluation, and a plan review. Modules carry automated tests that provision and tear down in an isolated test account.

8.2 Disaster-recovery and rebuild capability is exercised: critical environments are periodically rebuilt from code in a clean account to prove the code is the source of truth.

8.3 Module tests run in an isolated test account that never holds production data and never has a path to production, consistent with the production and non-production isolation of the Cloud Governance and Landing Zone Policy (MJD-TEC-0007 section 1.2). A test that requires production-like data uses synthetic data only.

### 8.4 Testing Strategy

The testing strategy layers checks so that defects are caught at the cheapest possible stage, from static analysis before merge through a full rebuild-from-code disaster-recovery drill.

| Test | What it checks | Stage | Environment |
|---|---|---|---|
| Lint | Style, formatting, deprecated syntax | Pre-merge | None (static) |
| Validate | Syntactic and type correctness of configuration | Pre-merge | None (static) |
| Policy test | Guardrail rules evaluate as expected against fixtures | Pre-merge | None (static) |
| Plan review | The concrete create/change/destroy plan is correct and expected | Pre-apply | Target environment plan |
| Integration test | Module provisions and tears down successfully | On module change | Isolated test account, synthetic data |
| Contract test | Module inputs and outputs honor their declared contracts | On module change | Isolated test account |
| Rebuild-from-code DR drill | A critical environment can be rebuilt entirely from code | Periodic | Clean disaster-recovery account |

8.5 The integration and contract tests run in an isolated test account that holds synthetic data only and has no path to production. The periodic rebuild-from-code drill proves the code is complete and authoritative and that the bank can recover an environment from code alone, the operational expression of the principle that the code, not the live infrastructure, is the source of truth.

## 9. Secrets, Identity, and Apply Credentials

9.1 Apply to production is never performed with an engineer's personal cloud credentials. The pipeline assumes a scoped, short-lived OIDC workload identity for the specific apply, consistent with the CI/CD Pipeline Standard (MJD-TEC-0005 section 5) and the Secrets and Key Management Policy (MJD-TEC-0004).

9.2 Where IaC must reference a secret (for example, to configure a service with a database credential), it references the secret by name in the secrets manager; the value is resolved at runtime by the workload, not materialized into state. Any service-account credential that IaC provisions inherits the 90-day rotation interval of MJD-TEC-0004.

9.3 IAM and identity bindings created by IaC are least-privilege by construction. The policy-as-code guardrails reject any workload role that grants wildcard administrative permissions, so an over-broad role cannot be introduced even by mistake.

9.4 IaC that provisions identity providers, OAuth2 clients, or token-signing configuration is treated as security-sensitive code. Such changes route a Security Architect reviewer through the CODEOWNERS controls of the Code Review and Branch Protection Standard (MJD-TEC-0009) and conform to the Authentication and Authorization Standard (MJD-TEC-0003) for any client registration values they set.

9.5 Destruction of a stateful resource holding regulated data through IaC requires the same explicit additional approval and verified backup as section 6.2 demands for the change workflow; the declarative nature of IaC does not lower the bar for destructive actions, it raises the need for a careful plan review because a single line can destroy a data store.

## 10. Tagging and Cost Governance

10.1 Every resource carries the four mandatory tags: owner, environment, data-classification, and cost-center. The tagging guardrail (GR-TAG-01) blocks a change that would create an untagged resource, so there is no path to an unattributed resource.

10.2 The tags serve security, operations, and finance at once. The owner tag identifies who is accountable and who is paged when the resource misbehaves. The environment tag drives the isolation and promotion rules of section 4. The data-classification tag determines which controls apply, including whether a resource is in scope for the regulated-data protections elsewhere in this standard. The cost-center tag attributes spend.

10.3 Cost is governed through code as well. Compositions declare the size and quantity of resources they provision, so a cost change is a reviewable diff rather than a surprise on an invoice. Spend is attributed by the cost-center tag and reported back to owning teams; an untagged or mis-tagged resource cannot be attributed and is therefore treated as a tagging defect to be corrected, not an accepted exception.

10.4 Idle or orphaned resources are surfaced by joining the tag inventory against utilization data. A resource with no current owner or no traffic is a candidate for decommissioning through the normal change workflow, never by manual console deletion.

## 11. Worked Example: Provisioning a Compliant Data Store

11.1 The following worked example illustrates how the controls in this standard combine when a team provisions a new database that will hold regulated customer data.

11.2 The team does not write raw resource definitions for the database. They compose the approved, registry-published `data-store` module (section 2.4), pinning an exact version. The module ships secure by default: encryption at rest with a KMS-managed key, TLS enforced for all connections, private network placement with no public endpoint, audit logging enabled, and automated backups configured.

11.3 The composition supplies the four mandatory tags (owner, environment set to production, data-classification set to the regulated tier, and cost-center) and the environment-specific parameters. Because the module propagates tags to every resource it creates, the GR-TAG-01 guardrail passes.

11.4 The database credential is not generated in code. The module configures the workload to reference the credential by name in the secrets manager (MJD-TEC-0004); the value is resolved at runtime and never materialized into state, so GR-STATE-01 passes and no secret appears in the plan, the logs, or the state file.

11.5 The pull request triggers the change workflow of section 6.4. Lint, validate, and policy tests run pre-merge. CODEOWNERS routes a Security Architect reviewer because the resource holds regulated data. The plan is generated and policy-checked pre-apply; GR-ENC-01, GR-ENC-02, GR-NET-01, GR-IAM-01, and GR-LOG-01 all evaluate against the concrete plan and pass because the module's secure defaults satisfy them. A human reviews the plan and confirms no unexpected destroy actions.

11.6 On approval, the pipeline assumes a scoped, short-lived OIDC workload identity for the apply, acquires the state lock, and applies the reviewed plan. After apply, the pipeline records a drift baseline. From the next day forward, daily drift detection compares the live database configuration against this baseline; any out-of-band change, such as someone widening a security group or disabling logging in the console, is detected within a day, alerted to the SIEM (MJD-SEC-0009), and reverted by reapplying the code.

11.7 Later, if the database must be destroyed or replaced, the destroy action against this stateful production resource triggers GR-DESTROY-01: the change requires explicit additional approval and a verified backup before the pipeline will apply it.

## 12. Roles and Responsibilities

**Software Engineer.** Defines infrastructure as code, composes approved hardened modules, pins module versions, reviews plans, supplies mandatory tags, references secrets by name rather than embedding them, and never makes manual production changes. Responsible for remediating drift on resources their team owns and for opening a pull request to codify any legitimate change that bypassed process.

**Security Architect.** Owns the policy-as-code guardrail catalog and its severities, performs the security review of hardened modules, approves public-exposure and wide-network exceptions with compensating controls and review dates, reviews security-sensitive IaC through CODEOWNERS, and owns the IaC threat model. Accountable for ensuring new guardrails are socialized in warn mode before they block.

**Platform Engineering.** Maintains the module library and registry, operates the encrypted state backend with versioning and locking, runs the drift-detection automation, operates the OIDC workload-identity integration for applies, and runs the periodic rebuild-from-code disaster-recovery drills.

**Head of Platform Engineering.** Owner of this standard, accountable for reproducible, drift-free infrastructure, for the integrity of the change workflow, and for ensuring that no sanctioned path to manual production change exists.

## 13. Exceptions and Escalation

13.1 No exception is granted to: the prohibition on manual production changes, the encryption-at-rest and in-transit guardrails, the prohibition on storing secrets in code or state, the use of short-lived identity for apply, or the requirement for additional approval and a verified backup before destroying a stateful production resource. These are non-waivable.

13.2 A public-exposure or wide-network exception requires Security Architect approval, a compensating control, and a review date. The exception is recorded against the specific resource and re-evaluated at the review date; an expired exception reverts the resource to the secure default.

13.3 Unauthorized manual changes to production infrastructure, or a publicly exposed sensitive resource, are escalated under the Incident Response Plan (MJD-SEC-0006) and the Change Management and Release Policy (MJD-TEC-0008).

## 14. Related Documents

- MJD-TEC-0003, Authentication and Authorization Standard
- MJD-TEC-0004, Secrets and Key Management Policy
- MJD-TEC-0005, CI/CD Pipeline Standard
- MJD-TEC-0007, Cloud Governance and Landing Zone Policy
- MJD-TEC-0008, Change Management and Release Policy
- MJD-TEC-0009, Code Review and Branch Protection Standard
- MJD-SEC-0006, Incident Response Plan
- MJD-SEC-0009, Logging, Monitoring, and SIEM Standard

## 15. Regulatory References

- NIST SP 800-53 Rev 5, controls CM-2, CM-3, CM-6 (Configuration Management)
- CIS Benchmarks (platform-specific hardening)
- PCI DSS 4.0, Requirement 1 (Network Security Controls)
- SOC 2 Trust Services Criteria, CC8.1

## 16. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0.0 | 2022-10-03 | Platform Engineering | Initial IaC standard. |
| 2.0.0 | 2024-02-14 | Platform Engineering | Mandated policy-as-code guardrails and central state backend. |
| 2.4.0 | 2025-06-11 | Platform Engineering | Added drift detection and hardened-module requirement. |
| 2.6.0 | 2026-02-25 | Platform Engineering | Tightened state classification and OIDC-only apply to production. |
