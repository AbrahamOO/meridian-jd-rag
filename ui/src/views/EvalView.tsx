import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ApiError, getEvals } from "../api";
import { EmptyState, ErrorState, Loading } from "../components/States";
import { PERSONAS, PERSONA_META } from "../types";
import type { EvalReport, EvalResult, Persona, RetrievalMetrics } from "../types";

const RETRIEVAL_KEYS: (keyof RetrievalMetrics)[] = [
  "context_precision",
  "context_recall",
  "hit_rate_at_k",
  "mrr",
  "ndcg",
];

export function EvalView() {
  const [report, setReport] = useState<EvalReport | null>(null);
  const [runs, setRuns] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    getEvals()
      .then((res) => {
        if (!active) return;
        setReport(res.latest);
        setRuns(res.runs);
        setError(null);
      })
      .catch((e) => {
        if (!active) return;
        setError(e instanceof ApiError ? e.message : "Unexpected error.");
      })
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  if (loading) return <Loading title="Loading eval report" />;
  if (error) return <ErrorState title="Could not load evals" detail={error} />;
  if (!report)
    return (
      <EmptyState
        title="No eval report yet"
        detail="Run the eval harness to populate evals/reports/latest.json."
      />
    );

  return <Dashboard report={report} runs={runs} />;
}

function Dashboard({ report, runs }: { report: EvalReport; runs: string[] }) {
  const sec = report.security;
  const perPersona = usePerPersonaAccess(report.results ?? []);

  const retrievalChart = RETRIEVAL_KEYS.map((k) => ({
    metric: k.replace(/_/g, " "),
    production: round(report.retrieval.production[k]),
    naive: round(report.retrieval.naive[k]),
  }));

  const historyChart = (report.history ?? [])
    .slice()
    .reverse()
    .concat([
      {
        run_id: report.run_id,
        created_at: report.created_at,
        totals: report.totals,
        security: { access_control_pass_pct: sec.access_control_pass_pct },
        generation: { faithfulness: report.generation.faithfulness },
      },
    ])
    .map((h) => ({
      run: h.run_id.replace(/^run-/, "").slice(0, 8),
      access: round(h.security.access_control_pass_pct),
      faithfulness: round(h.generation.faithfulness * 100),
    }));

  return (
    <div className="stack">
      <div className="view-head">
        <h1>Evaluation dashboard</h1>
        <p>
          Run <span className="mono">{report.run_id}</span> &middot; profile{" "}
          <span className="mono">{report.profile}</span> &middot; index{" "}
          <span className="mono">{report.manifest.index_version}</span> &middot;{" "}
          {report.totals.passed}/{report.totals.records} records passed
        </p>
      </div>

      {/* Headline security board */}
      <div className="card stack">
        <div className="spread">
          <h2 className="section-title" style={{ margin: 0 }}>
            Access-control pass / fail board
          </h2>
          <span
            className={`badge ${sec.access_control_pass_pct >= 100 ? "pass" : "fail"}`}
          >
            overall {round(sec.access_control_pass_pct)}%
          </span>
        </div>
        <div className="board-grid">
          {PERSONAS.map((p) => {
            const stat = perPersona[p];
            const allPass = stat.total > 0 && stat.failed === 0;
            return (
              <div key={p} className={`board-cell ${allPass ? "pass" : stat.total ? "fail" : ""}`}>
                <div className="persona-name">{PERSONA_META[p].label}</div>
                <div className="board-stat">
                  {stat.total === 0 ? "n/a" : `${stat.passed}/${stat.total}`}
                </div>
                <div className="board-detail">
                  {stat.total === 0
                    ? "no access-control records"
                    : allPass
                      ? "access enforced on all records"
                      : `${stat.failed} access failure(s)`}
                </div>
              </div>
            );
          })}
        </div>

        <div className="stat-grid">
          <SecStat label="Access control" value={sec.access_control_pass_pct} />
          <SecStat label="Injection resistance" value={sec.injection_resistance_pass_pct} />
          <SecStat label="PII leakage" value={sec.pii_leakage_pass_pct} />
          <SecStat label="Abstention" value={sec.hallucination_abstention_pass_pct} />
        </div>

        <div>
          <span className="label">Blocking failures</span>
          {sec.blocking_failures.length === 0 ? (
            <span className="badge pass">none</span>
          ) : (
            <ul className="small">
              {sec.blocking_failures.map((f, i) => (
                <li key={i} className="mono">
                  {JSON.stringify(f)}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Retrieval naive vs production */}
      <div className="card stack">
        <h2 className="section-title" style={{ margin: 0 }}>
          Retrieval metrics: production vs naive
        </h2>
        <div style={{ width: "100%", height: 280 }}>
          <ResponsiveContainer>
            <BarChart data={retrievalChart} margin={{ top: 8, right: 8, bottom: 8, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a313c" />
              <XAxis dataKey="metric" tick={{ fill: "#9aa6b2", fontSize: 12 }} />
              <YAxis domain={[0, 1]} tick={{ fill: "#9aa6b2", fontSize: 12 }} />
              <Tooltip
                contentStyle={{ background: "#161b22", border: "1px solid #2a313c", color: "#e6edf3" }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="production" fill="#2f81f7" radius={[3, 3, 0, 0]} />
              <Bar dataKey="naive" fill="#6b7682" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <DeltaTable retrieval={report.retrieval} />
      </div>

      {/* Generation + operational */}
      <div className="grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))" }}>
        <div className="card stack">
          <h2 className="section-title" style={{ margin: 0 }}>
            Generation
          </h2>
          <div className="stat-grid">
            <SecStat label="Faithfulness" value={report.generation.faithfulness * 100} />
            <SecStat label="Answer relevance" value={report.generation.answer_relevance * 100} />
            <SecStat label="Answer correctness" value={report.generation.answer_correctness * 100} />
            <SecStat label="Citation accuracy" value={report.generation.citation_accuracy * 100} />
          </div>
        </div>
        <div className="card stack">
          <h2 className="section-title" style={{ margin: 0 }}>
            Latency and cost
          </h2>
          <div className="stat-grid">
            <Stat label="Latency p50" value={`${round(report.operational.latency_p50_ms)} ms`} />
            <Stat label="Latency p95" value={`${round(report.operational.latency_p95_ms)} ms`} />
            <Stat
              label="Cost / query"
              value={`$${report.operational.cost_per_query_usd.toFixed(6)}`}
            />
            <Stat label="Tokens / query" value={round(report.operational.tokens_per_query)} />
          </div>
        </div>
      </div>

      {/* Trend */}
      {historyChart.length > 1 ? (
        <div className="card stack">
          <h2 className="section-title" style={{ margin: 0 }}>
            Trend across runs
          </h2>
          <div style={{ width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <LineChart data={historyChart} margin={{ top: 8, right: 8, bottom: 8, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2a313c" />
                <XAxis dataKey="run" tick={{ fill: "#9aa6b2", fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fill: "#9aa6b2", fontSize: 12 }} />
                <Tooltip
                  contentStyle={{ background: "#161b22", border: "1px solid #2a313c", color: "#e6edf3" }}
                />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Line type="monotone" dataKey="access" stroke="#3fb950" strokeWidth={2} name="access %" />
                <Line
                  type="monotone"
                  dataKey="faithfulness"
                  stroke="#2f81f7"
                  strokeWidth={2}
                  name="faithfulness %"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      ) : null}

      <div className="card">
        <span className="label">Available runs ({runs.length})</span>
        <div className="small mono">{runs.length ? runs.join("  ") : "none"}</div>
      </div>
    </div>
  );
}

interface PersonaAccessStat {
  total: number;
  passed: number;
  failed: number;
}

// Per-persona access-control pass derived from the per-record results: a record
// counts as an access-control record when its security.access_enforced is present
// and the type is an access boundary or any record that exercises the filter.
// A record fails access control iff access_enforced is false or a doc leaked.
function usePerPersonaAccess(results: EvalResult[]): Record<Persona, PersonaAccessStat> {
  return useMemo(() => {
    const base = Object.fromEntries(
      PERSONAS.map((p) => [p, { total: 0, passed: 0, failed: 0 }]),
    ) as Record<Persona, PersonaAccessStat>;
    for (const r of results) {
      const persona = r.persona;
      if (!base[persona]) continue;
      base[persona].total += 1;
      const enforced = r.security.access_enforced && r.security.leaked_doc_ids.length === 0;
      if (enforced) base[persona].passed += 1;
      else base[persona].failed += 1;
    }
    return base;
  }, [results]);
}

function DeltaTable({ retrieval }: { retrieval: EvalReport["retrieval"] }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>Production</th>
          <th>Naive</th>
          <th>Delta</th>
        </tr>
      </thead>
      <tbody>
        {RETRIEVAL_KEYS.map((k) => {
          const delta = retrieval.delta[k];
          return (
            <tr key={k}>
              <td>{k.replace(/_/g, " ")}</td>
              <td className="mono">{retrieval.production[k].toFixed(4)}</td>
              <td className="mono">{retrieval.naive[k].toFixed(4)}</td>
              <td className={`mono ${delta >= 0 ? "delta-pos" : "delta-neg"}`}>
                {delta >= 0 ? "+" : ""}
                {delta.toFixed(4)}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

function SecStat({ label, value }: { label: string; value: number }) {
  const good = value >= 100;
  return (
    <div className={`stat ${good ? "good" : ""}`}>
      <div className="stat-value" style={{ color: good ? "var(--ok)" : undefined }}>
        {round(value)}%
      </div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="stat">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

function round(n: number): number {
  return Math.round(n * 100) / 100;
}
