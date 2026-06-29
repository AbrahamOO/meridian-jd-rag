"""Eval metric families (docs/contracts.md section 7; spec section 12).

Four families, each a focused module:

- retrieval:   context_precision, context_recall, hit_rate_at_k, mrr, ndcg
- generation:  faithfulness/groundedness, answer_relevance, answer_correctness,
               completeness, citation_accuracy
- security:    access_enforced, leaked_doc_ids, injection_obeyed, pii_leaked
- operational: latency_ms, cost_usd, tokens

All built-in implementations are deterministic and dependency-free so the CI
mock path needs no heavy extras. RAGAS / DeepEval are wired in evals.metrics.
optional as LAZY, OPTIONAL backends that augment the built-ins when installed;
their absence never breaks a run.
"""

from __future__ import annotations
