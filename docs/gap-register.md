# Meridian J.D. RAG: Gap and Edge-Case Register

Status: BINDING. Version 1.0.0.
Created: 2026-06-29
Last updated: 2026-06-29

Every entry is a place where the spec is silent, ambiguous, or where a real
edge case will arise. Each carries the decision and rationale. Every decision is
fail-closed and production-safe. Builders implement the decision, not their own
interpretation. Decision IDs are referenced from `contracts.md`.

---

## G-01: BM25 / sparse backend inside pgvector

Gap: the spec asks for a hybrid dense+sparse (BM25) index but pgvector has no
native BM25.

Decision: use Postgres native full-text search as the sparse backend.
Build a `tsvector` column over `embed_text` (header + child text, so exact terms
like "FR Y-9C", "SR 11-7", "OAuth2" survive) with a GIN index, and rank with
`ts_rank_cd`. Treat the `ts_rank_cd` ordering as the "BM25-equivalent" ranked
list feeding RRF. Tokenize with the `simple` configuration (no stemming/stopword
loss) so regulatory tokens are preserved exactly, plus a parallel `english`
configuration column for recall on natural-language queries; the sparse list is
the RRF fusion of both tsvector rankings, deduped by chunk_id keeping best rank.

Rationale: keeps everything in one Postgres instance (the spec's stated reason
for pgvector), needs no extra service, and is reproducible. The `simple` config
protects exact-term recall, which is the whole point of adding sparse. A separate
service (Elasticsearch/OpenSearch) is the credible alternative and is noted in
the manifest comments, but is not used to keep one-command startup true.

---

## G-02: Superseded down-weighting math

Gap: spec says superseded docs are "down-weighted" but gives no formula.

Decision: multiplicative penalty applied AFTER RRF fusion and BEFORE rerank:
`final_score = rrf_score * superseded_penalty` where `superseded_penalty`
defaults to `0.5` (config `retrieval.superseded_penalty`). A chunk is superseded
(`is_superseded = true`) iff some OTHER live document's `supersedes` field points
at this chunk's `doc_id`. The penalty never zeroes the score, so a superseded doc
can still surface if no live version covers the query, but it can never outrank
its live successor on equal relevance. Additionally, at generation, if both a
live doc and its superseded predecessor are in context, the live one is presented
as authoritative and the superseded one is annotated `(superseded, see vX.Y)` and
never cited as the authoritative source (G-08).

Rationale: multiplicative keeps relative ordering within the superseded set
intact while reliably ranking live content above it. 0.5 is strong enough to flip
near-ties but soft enough not to hide content when it is the only match (avoids a
false "no answer"). Hard exclusion would fail the version-sensitivity eval which
requires the system to retrieve the current version AND flag the superseded one.

---

## G-03: PII redaction in logs versus traces

Gap: spec says redact PII before logging and restrict trace access, but does not
separate the two artifacts.

Decision: two distinct sinks. (1) The AUDIT LOG (durable, append-only, read by
the audit-viewer UI and any examiner) stores the query with PII REDACTED by the
Presidio-equivalent redactor, plus role, retrieved_doc_ids, boundary flags,
trace_id, latency, cost, tokens, timestamp. No document content, ever. (2) The
DEBUG TRACE (short-lived, default 7-day TTL, access-restricted to an admin scope,
off by default in the default profile) may store the raw query and retrieval
internals for debugging, behind an explicit `observability.debug_trace=true`
flag. Redaction runs at the boundary BEFORE the audit write; the raw value never
touches the audit sink. The synthetic-PII canary must be caught and redacted in
the audit log; the security eval asserts no synthetic PII string appears in any
audit record.

Rationale: examiners need an audit trail without PII exposure; engineers
occasionally need raw data to debug. Separating durability from sensitivity, with
the raw sink off-by-default, TTL-bounded, and access-restricted, satisfies both
while failing closed (default profile logs only redacted).

---

## G-04: Precise citation re-validation point

Gap: spec says citations are re-checked "before citation rendering" but not the
exact pipeline location.

Decision: re-validation happens in the `output_guardrail` node, AFTER `generate`
and BEFORE the API serializes the response. For each citation the generator
emitted: (a) the cited doc_id must be in the assembled context's doc_ids, and
(b) `resolve_access(role)` plus the doc's stored `allowed_roles`/`classification`
must still permit it. A citation failing either is stripped. If stripping leaves
any answer claim uncited, the guardrail discards the answer and returns the
insufficient-context boundary string rather than emitting an uncited claim. This
is a second, independent enforcement of access on top of the in-query pre-filter
(defense in depth).

Rationale: the pre-filter already prevents out-of-scope retrieval, but a model
could hallucinate a citation to a doc it never saw, or to a real doc out of
scope. Re-validating at the last node before serialization closes the
citation-leak vector the spec explicitly warns about, and does so fail-closed.

---

## G-05: Token-budget math for small-to-big assembly

Gap: spec gives child/parent token ranges but no assembly budget algorithm.

Decision: as specified in contracts.md section 3.5. Reserve a fixed 600-token
overhead inside `context_token_budget` (default 3500) for the system prompt and
question. Add parents best-first, dedupe by parent_id, skip-and-record a parent
that would overflow but keep scanning for smaller ones, truncate an
over-`parent_max_tokens` parent on a paragraph boundary (never mid-table). If the
single best parent alone exceeds the remaining budget, truncate it to fit rather
than drop it, guaranteeing a non-empty allowed retrieval yields non-empty
context. Token counting uses the active generator's tokenizer when available,
else a `len(text)//4` heuristic, recorded consistently so eval numbers are stable.

Rationale: deterministic, never silently empties context on an allowed query,
respects the generation budget, and the skip-smaller-fits behavior maximizes
recall within budget without nondeterministic packing.

---

## G-06: Missing metadata at ingestion

Gap: spec says a doc missing classification/allowed_roles "fails ingestion
loudly" but not the run-level behavior.

Decision: fail-closed at two levels. (1) Per-document: any doc missing
`classification` or `allowed_roles`, or carrying an empty/unknown-role
`allowed_roles`, or a malformed `doc_id`, is REJECTED and recorded in
`rejected[]`. (2) Run-level: in `mode=full`, ANY rejection fails the whole
ingest with HTTP 422 and writes no index (the index is all-or-nothing so a
partial corpus never goes live). `mode=incremental` skips the bad doc, keeps the
prior index for that doc, and still fails the run if a NEW doc is rejected.
`dry_run=true` reports rejections without writing. Belt-and-suspenders: the
retrieval layer treats any chunk somehow stored with null
allowed_roles/classification as invisible (G-06b).

Rationale: a bank index with a silently dropped policy is worse than no update.
All-or-nothing full ingest plus invisible-on-null at retrieval guarantees no
mislabeled chunk is ever served.

---

## G-07: Unknown role at query time

Gap: spec says fail closed on unknown role but not the user-facing behavior.

Decision: `resolve_access(unknown)` returns `allowed=False`, reason
`unknown_role`, and `build_access_filter` returns a match-none predicate so zero
chunks are scored. The query graph short-circuits at `input_guardrail` to a
boundary response with `boundary_reason="unknown_role"` and the access-boundary
string. HTTP status is 200 (the boundary is correct product behavior, not a
client error). The audit record is still written. There is no fallback to a
"default" or "least-privilege-but-some" role; unknown means nothing.

Rationale: silently mapping an unknown role to a real role is a privilege-grant
bug. Returning zero and logging it is the only safe behavior. 200 keeps the UI
flow uniform; a malformed request (missing the role field entirely) is the only
4xx case.

---

## G-08: Staleness / superseded flag semantics

Gap: spec uses "superseded" loosely. Need precise semantics for both ends of a
supersession pair.

Decision: `supersedes` is a forward pointer on the NEW doc to the OLD doc_id.
`is_superseded` is a DERIVED boolean on the OLD doc, computed at ingestion as
"some live doc's supersedes points here." Both docs may be indexed
simultaneously (the near-duplicate pair test fixture). The live doc is
authoritative; the superseded doc is down-weighted (G-02), and when surfaced is
annotated and never cited as authoritative. A superseded doc is removed from the
index only when its source file is deleted (G, retention), not merely because a
successor exists, because the eval must demonstrate the system flagging the
superseded version.

Rationale: keeping both indexed is required by the version-sensitivity eval. The
forward-pointer plus derived-flag model is unambiguous and computable in one pass.

---

## G-09: Empty retrieval (allowed role, zero matches)

Gap: spec does not say what happens when an authorized query simply matches
nothing.

Decision: zero candidates after the access filter sets
`boundary_reason="empty_retrieval"` and the generator returns the
insufficient-context string ("I do not have an authoritative policy on that in
the documents available to your role."), `abstained=true`, empty citations. This
is distinct from `no_access`/`unknown_role` (which are access boundaries) and from
`out_of_scope` (caught at input guardrail). The audit record logs it; a high
empty_retrieval rate is a content-gap signal on the dashboard.

Rationale: abstention is a feature (spec section 10). Distinguishing
empty-retrieval from access-denial in the boundary_reason lets the dashboard
separate "we lack the content" from "you lack the access," which matters
operationally and for the demo.

---

## G-10: Oversized table chunk

Gap: spec says never split mid-table; does not say what to do when a single table
exceeds the chunk target.

Decision: a Markdown table is an atomic unit. The production chunker emits the
entire table (with its preceding heading as section context) as ONE child chunk
even if it exceeds `child_target_tokens`, flagged `oversized_table=true` in a
side-channel metadata file consumed by the chunk visualizer. Its parent is the
containing section. If the table alone exceeds `parent_max_tokens`, the parent is
the table itself (no further section text) and assembly may truncate trailing
ROWS (never columns, never the header row) on a row boundary, recording the
truncation. The header row is always preserved so the table stays interpretable.

Rationale: splitting a table destroys its meaning and produces garbage retrieval.
Keeping it atomic, preserving the header row, and truncating only whole trailing
rows under extreme budget pressure preserves interpretability while staying
within budget.

---

## G-11: Non-UTF8 / binary input

Gap: spec specifies loaders for MD/DOCX/PDF/HTML but not malformed/binary files.

Decision: the loader attempts UTF-8 decode for text formats; on UnicodeDecodeError
it retries with `errors="strict"` under a declared charset from the file's
metadata if present, else REJECTS the file with reason `non_utf8_or_binary`. A
file whose extension is unsupported, or whose detected MIME is binary and not one
of the four supported types, is REJECTED, not best-effort parsed. DOCX/PDF are
parsed by their libraries; a parse exception is a rejection with the exception
class name, never a partial/garbled extraction fed to embedding. Rejections
follow G-06 run-level rules.

Rationale: garbled text silently embedded poisons retrieval and could smuggle
unredacted bytes into logs. Rejecting loudly is the only safe path; a partial
parse is worse than a clean failure.

---

## G-12: Mock-adapter determinism

Gap: spec requires CI to be deterministic but does not define how the providers
achieve it.

Decision: as specified in contracts.md section 1.7. Mock embedder = sha256-seeded
stdlib RNG over (model_id, kind, text), 256 dims, L2-normalized, pure stdlib.
Mock generator = deterministic first-sentence extraction plus verbatim citation
tags, fixed boundary strings, word-count token accounting. Mock reranker =
Jaccard overlap, index tie-break. All costs 0.0. No network, no clock, no
randomness without a fixed seed. CI asserts byte-identical eval reports across
runs (modulo run_id/timestamp which are excluded from the determinism assertion).

Rationale: deterministic mocks make eval thresholds assertable in CI without
flakiness, which is the entire point of the CI regression gate.

---

## G-13: Duplicate doc_id

Gap: spec assumes unique doc_ids; corpus generation by multiple agents could
collide.

Decision: doc_id uniqueness is validated at ingestion across the full corpus
BEFORE any embedding. A duplicate doc_id is a fatal rejection for ALL copies
sharing the id (not "keep the first"), reason `duplicate_doc_id`, listing every
offending path. Run fails per G-06. The content_hash is separately checked: two
DIFFERENT files with the SAME content_hash but DIFFERENT doc_ids are allowed
(legitimate near-duplicate pair) but logged as a warning; SAME doc_id AND same
hash across two paths is the duplicate-file case and rejected.

Rationale: a duplicate doc_id corrupts access metadata resolution and citation
integrity. Rejecting all copies (rather than arbitrarily keeping one) forces the
authoring agent to fix the collision rather than ship an ambiguous corpus.

---

## G-14: Multi-part question spanning allowed and denied scope

Gap: spec mentions decomposition but not how mixed-scope compound questions are
handled (e.g. SOFTWARE_ENGINEER asks "compare our secrets rotation policy with
our AML escalation procedure").

Decision: decomposition (G query_transform) splits into subqueries. Every
subquery is retrieved under the SAME single access filter for the requesting
role. Subqueries hitting allowed content return context; subqueries hitting only
denied content return zero (the denied content is never scored). The generator
answers the answerable parts from context and, for the unanswerable part, emits
the access-boundary string scoped to that part, WITHOUT revealing the existence,
title, or content of the denied document. The response can therefore be a partial
answer plus a boundary note. `boundary_triggered=true` if any part was denied,
with `retrieved_doc_ids` listing only the allowed docs.

Rationale: refusing the entire compound question would be a worse UX and would
itself leak (it signals the denied part exists and is sensitive). Answering the
allowed part and giving a generic boundary for the rest is both helpful and
non-leaking. Using one filter for all subqueries guarantees no subquery can
escalate scope.

---

## G-15: Empty or whitespace-only query

Decision: the input guardrail rejects an empty/whitespace-only query at the API
boundary with HTTP 422 (malformed request), no retrieval, no audit content beyond
a minimal "empty_query" event. Distinct from out_of_scope (a real but non-bank
question) which returns a 200 boundary.

Rationale: an empty query is a client error, not a product behavior; failing fast
avoids embedding empty strings (which the embedder rejects anyway).

---

## G-16: Out-of-scope (non-bank) question

Decision: the input guardrail runs a scope check. A clearly non-bank question
("what is the weather") yields `boundary_reason="out_of_scope"`, the abstention
string, no retrieval, 200. The hallucination eval's out_of_scope records assert
this. The scope check is conservative: when uncertain whether a question is
in-scope, it PROCEEDS to retrieval (which will simply abstain on empty results)
rather than falsely refusing a legitimate bank question.

Rationale: false refusals of real questions hurt the demo more than letting a
borderline question fall through to a correct empty-retrieval abstention. Failing
closed here means failing toward abstention, not toward answering.

---

## G-17: Query containing user-supplied injection

Decision: the input guardrail detects injection patterns in the USER query
("ignore previous instructions", "reveal restricted", role-spoofing attempts) and
short-circuits to `boundary_reason="injection_blocked"`, 200, no retrieval. This
is separate from document-sourced injection (handled by prompt delimiting in
generate, never trusted). The security eval covers both vectors.

Rationale: a user trying to jailbreak via the query is blocked before it can
influence retrieval or generation; document injection is contained by treating
all context as untrusted data. Two independent defenses for two distinct vectors.

---

## G-18: Cross-model embedding comparison

Decision: embeddings are only ever compared within one (model, model_version,
dim) recorded in the manifest. A query embedded with a different model than the
index is a fatal error at query time (`embedding_model_mismatch`), not a silent
degraded search. `/health` surfaces the active embedding model and the index's
embedding model; a mismatch sets `ok=false`.

Rationale: cross-model cosine similarity is meaningless and would silently
destroy retrieval quality. Failing loudly protects correctness.

---

## G-19: Reranker or generator provider unavailable at runtime

Decision: fail-degraded, not fail-open. If the reranker is unavailable, retrieval
falls back to RRF order (logged, `guardrail_flags += "rerank_unavailable"`) and
serves, because access control is unaffected by rerank. If the GENERATOR is
unavailable, the service returns the insufficient-context boundary with an error
flag rather than fabricating; it never bypasses guardrails. Access control is
NEVER degraded: if the access filter cannot be applied (DB error), the query
fails closed with a boundary and an error, returning nothing.

Rationale: degrade non-security components gracefully to stay available, but the
access filter is load-bearing and must fail closed, never serve unfiltered
results.

---

## G-20: Concurrent re-index while serving

Decision: re-index writes a new index_version and a new manifest; the live
service holds a manifest pointer that is swapped atomically only after the new
index passes a post-build smoke check (loads, document count matches, an
access-control spot check on RESTRICTED docs passes). A failed smoke check leaves
the old manifest live. No request ever reads a half-built index.

Rationale: zero-downtime, atomic, and a failed build can never expose a partial
or mis-permissioned index.

---

## Summary of fail-closed posture

In every ambiguous case the chosen behavior is the one that, if wrong, denies
rather than leaks: unknown role denies, missing metadata denies, null-at-retrieval
is invisible, citation re-validation strips, DB error on the access filter denies,
mismatched embedding model errors, partial parse rejects, duplicate id rejects
all copies, full ingest is all-or-nothing. The only place the system leans toward
proceeding is the out-of-scope check, and there "proceeding" leads to a safe
empty-retrieval abstention, not to answering out of scope.

## Change History

- 2026-06-29: Added the Created, Last updated, and Change History headers to satisfy the documentation date policy. No decisions changed.
- 2026-06-29: Initial gap and edge-case register (G-01 through G-20), all decisions fail-closed and production-safe.
