// Types mirror the binding contracts in docs/contracts.md sections 3.6, 6.1, 7.3,
// 7.4, and 8. No field here is invented; every field is returned by api/app.py.

export const PERSONAS = [
  "OPERATIONS_ANALYST",
  "COMPLIANCE_OFFICER",
  "SOFTWARE_ENGINEER",
  "SECURITY_ARCHITECT",
  "RISK_ANALYST",
  "FINANCE_CONTROLLER",
  "BRANCH_STAFF",
] as const;

export type Persona = (typeof PERSONAS)[number];

// Clearance mapping from contracts section 11.1 (display only; access is enforced
// server side at retrieval time).
export const PERSONA_META: Record<
  Persona,
  { label: string; department: string; ceiling: string }
> = {
  OPERATIONS_ANALYST: { label: "Operations Analyst", department: "Operations", ceiling: "INTERNAL" },
  COMPLIANCE_OFFICER: { label: "Compliance Officer", department: "Compliance", ceiling: "CONFIDENTIAL" },
  SOFTWARE_ENGINEER: { label: "Software Engineer", department: "Technology", ceiling: "CONFIDENTIAL" },
  SECURITY_ARCHITECT: { label: "Security Architect", department: "Security", ceiling: "RESTRICTED" },
  RISK_ANALYST: { label: "Risk Analyst", department: "Risk", ceiling: "CONFIDENTIAL" },
  FINANCE_CONTROLLER: { label: "Finance Controller", department: "Finance", ceiling: "CONFIDENTIAL" },
  BRANCH_STAFF: { label: "Branch Staff", department: "Retail", ceiling: "INTERNAL" },
};

// contracts 3.6
export interface Citation {
  doc_id: string;
  title: string;
  section_path: string;
  version: string;
}

// contracts 8.1 explain payload (subset of contracts 3.2 Candidate)
export interface ExplainCandidate {
  chunk_id: string;
  doc_id: string;
  section_path: string;
  rrf_score: number;
  dense_rank: number | null;
  sparse_rank: number | null;
  is_superseded: boolean;
}

export interface ExplainTransformed {
  rewritten: string;
  subqueries: string[];
  used: string[];
}

export interface QueryExplain {
  transformed: ExplainTransformed | null;
  candidates: ExplainCandidate[];
  rerank_order: string[];
  dropped_for_budget: string[];
}

// contracts 8.1
export interface QueryResponse {
  trace_id: string;
  answer: string;
  citations: Citation[];
  boundary_triggered: boolean;
  boundary_reason: string;
  abstained: boolean;
  retrieved_doc_ids: string[];
  latency_ms: number;
  cost_usd: number;
  tokens: { prompt: number; completion: number; embed: number };
  explain: QueryExplain | null;
  error?: { code: string; message: string };
}

export interface QueryRequestOptions {
  chunk_strategy?: string | null;
  explain?: boolean;
}

// contracts 8.4
export interface HealthProvider {
  ok: boolean;
  adapter?: string;
  model?: string | null;
  dim?: number | null;
  detail?: string;
}

export interface HealthResponse {
  ok: boolean;
  providers: Record<string, HealthProvider>;
  index?: {
    loaded: boolean;
    index_version: string | null;
    documents: number;
    chunks: number;
    embedding_model_mismatch?: boolean;
  };
  profile?: string;
  graph_backend?: string;
  error?: string;
}

// contracts 7.2 (per-record result inside the report)
export interface EvalResult {
  id: string;
  run_id: string;
  persona: Persona;
  type: string;
  chunk_strategy: string;
  passed: boolean;
  metrics: Record<string, number>;
  security: {
    access_enforced: boolean;
    leaked_doc_ids: string[];
    injection_obeyed: boolean;
    pii_leaked: boolean;
  };
  operational: { latency_ms: number; cost_usd: number; tokens: number };
  retrieved_doc_ids: string[];
  boundary_triggered: boolean;
  notes: string;
}

export interface RetrievalMetrics {
  context_precision: number;
  context_recall: number;
  hit_rate_at_k: number;
  mrr: number;
  ndcg: number;
}

// contracts 7.3 / 7.4
export interface EvalReport {
  run_id: string;
  created_at: string;
  profile: string;
  manifest: { index_version: string; corpus_version: string };
  totals: { records: number; passed: number; failed: number };
  by_type: Record<string, { passed: number; failed: number }>;
  retrieval: {
    production: RetrievalMetrics;
    naive: RetrievalMetrics;
    delta: RetrievalMetrics;
  };
  generation: {
    faithfulness: number;
    answer_relevance: number;
    answer_correctness: number;
    citation_accuracy: number;
  };
  security: {
    access_control_pass_pct: number;
    injection_resistance_pass_pct: number;
    pii_leakage_pass_pct: number;
    hallucination_abstention_pass_pct: number;
    blocking_failures: unknown[];
  };
  operational: {
    latency_p50_ms: number;
    latency_p95_ms: number;
    cost_per_query_usd: number;
    tokens_per_query: number;
  };
  ci_gate: { passed: boolean; thresholds: Record<string, number> };
  results?: EvalResult[];
  history?: EvalHistoryEntry[];
}

export interface EvalHistoryEntry {
  run_id: string;
  created_at: string;
  totals: { records: number; passed: number; failed: number };
  security: { access_control_pass_pct: number };
  generation: { faithfulness: number };
}

export interface EvalsResponse {
  latest: EvalReport | null;
  runs: string[];
}

// contracts 6.1
export interface AuditRecord {
  trace_id: string;
  role: string;
  query: string;
  retrieved_doc_ids: string[];
  boundary_triggered: boolean;
  boundary_reason: string;
  guardrail_flags: string[];
  latency_ms: number;
  cost_usd: number;
  tokens: { prompt: number; completion: number; embed: number };
  timestamp: string;
}

export interface AuditResponse {
  records: AuditRecord[];
  count: number;
}
