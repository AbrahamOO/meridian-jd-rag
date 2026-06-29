import type {
  AuditResponse,
  EvalReport,
  EvalsResponse,
  HealthResponse,
  Persona,
  QueryRequestOptions,
  QueryResponse,
} from "./types";

// Config-driven base URL: VITE_API_BASE, defaulting to localhost:8000.
export const API_BASE: string =
  (import.meta.env.VITE_API_BASE as string | undefined)?.replace(/\/+$/, "") ??
  "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_BASE}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(
      `Cannot reach the API at ${API_BASE}. Confirm the service is running.`,
      0,
    );
  }
  const text = await res.text();
  const body = text ? (JSON.parse(text) as unknown) : null;
  if (!res.ok) {
    const errObj = body as { error?: { message?: string; code?: string } } | null;
    const detail = errObj?.error?.message ?? errObj?.error?.code ?? res.statusText;
    throw new ApiError(detail, res.status);
  }
  return body as T;
}

export function postQuery(
  role: Persona | string,
  query: string,
  options: QueryRequestOptions = {},
): Promise<QueryResponse> {
  return request<QueryResponse>("/query", {
    method: "POST",
    body: JSON.stringify({ role, query, history: [], options }),
  });
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function getEvals(): Promise<EvalsResponse> {
  return request<EvalsResponse>("/evals");
}

export function getEvalRun(runId: string): Promise<EvalReport> {
  return request<EvalReport>(`/evals?run_id=${encodeURIComponent(runId)}`);
}

export function getAudit(limit = 100, admin = true): Promise<AuditResponse> {
  const params = new URLSearchParams({ limit: String(limit), admin: String(admin) });
  return request<AuditResponse>(`/audit?${params.toString()}`);
}
