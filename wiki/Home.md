# Meridian J.D. RAG: Wiki Home

**Created: 2026-06-29**
**Last updated: 2026-06-29**

> **FICTIONAL:** Meridian John Doe Financial does not exist. This is a portfolio demonstration system. See [NOTICE.md](https://github.com/AbrahamOO/meridian-jd-rag/blob/main/NOTICE.md) for the full disclaimer.

---

Meridian J.D. RAG is a retrieval-augmented generation (RAG) system built on a corpus of 51 fictional banking documents, where access control is enforced in the SQL `WHERE` clause before any chunk is scored: not as a post-retrieval Python filter.

The system includes an 8-node LangGraph pipeline, an attribute-based access control (ABAC) model with four clearance levels, a self-applied threat model covering seven threat categories, and a deterministic eval harness that runs with zero API keys and gates CI on security and faithfulness metrics.

---

## Navigation

| Page | Contents |
| --- | --- |
| [Architecture Overview](Architecture-Overview) | System shape, component responsibilities, technology choices |
| [RAG Pipeline Deep-Dive](RAG-Pipeline-Deep-Dive) | The 8-node LangGraph graph, node by node |
| [Chunking Strategy](Chunking-Strategy) | Production vs. naive chunking and why it matters |
| [Access-Control Model](Access-Control-Model) | ABAC, fail-closed design, the clearance matrix, no-leak-through-citations |
| [Eval Methodology](Eval-Methodology) | Every metric defined, how to read the dashboard, profile honesty note |
| [Threat Model Walkthrough](Threat-Model-Walkthrough) | T-01 to T-07 with mitigations and eval evidence |
| [Provider and Config Guide](Provider-and-Config-Guide) | Zero-key vs. hybrid-key modes, adding a new adapter |
| [Operations and Observability](Operations-and-Observability) | Audit log, debug trace, health endpoint, re-indexing |
| [ADR Index](ADR-Index) | All Architecture Decision Records with links |
| [Glossary](Glossary) | Banking terms and RAG/ML terms |

---

## What this covers

**Retrieval-time access control.** A COMPLIANCE_OFFICER and an OPERATIONS_ANALYST asking the same question receive different answers. The filter runs in the database `WHERE` clause: the restricted chunks are never fetched, never ranked, never available to the LLM.

**Self-applied threat model.** The system threat-models itself as an attack surface. Seven threats are documented: prompt injection, data exfiltration via crafted queries, PII in logs, embedding inversion, denial of service, secrets handling, and supply-chain drift. Each threat has a named code path and a named eval record.

**Quantitative evals with a CI gate.** The eval harness is deterministic: zero API keys, all-mock providers. It gates CI on security metrics, faithfulness, and abstention, and the results are reproducible on any machine with `make eval`.
