import { useCallback, useEffect, useState } from "react";
import { ApiError, getAudit } from "../api";
import { EmptyState, ErrorState, Loading } from "../components/States";
import type { AuditRecord } from "../types";

export function AuditView() {
  const [records, setRecords] = useState<AuditRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [roleFilter, setRoleFilter] = useState<string>("ALL");
  const [boundaryOnly, setBoundaryOnly] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    getAudit(200, true)
      .then((res) => {
        setRecords(res.records);
        setError(null);
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Unexpected error."))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const roles = Array.from(new Set(records.map((r) => r.role))).sort();
  const filtered = records.filter(
    (r) =>
      (roleFilter === "ALL" || r.role === roleFilter) &&
      (!boundaryOnly || r.boundary_triggered),
  );

  return (
    <div className="stack">
      <div className="view-head">
        <h1>Audit log viewer</h1>
        <p>
          Append-only record per request, including boundary responses. The admin
          view shows doc_ids only, never document content. Queries are stored
          redacted of PII.
        </p>
      </div>

      <div className="card">
        <div className="spread">
          <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "flex-end" }}>
            <div>
              <label className="label" htmlFor="role-filter">
                Role
              </label>
              <select
                id="role-filter"
                value={roleFilter}
                onChange={(e) => setRoleFilter(e.target.value)}
              >
                <option value="ALL">All roles</option>
                {roles.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </div>
            <label className="small" style={{ display: "flex", gap: "0.4rem", alignItems: "center" }}>
              <input
                type="checkbox"
                checked={boundaryOnly}
                onChange={(e) => setBoundaryOnly(e.target.checked)}
              />
              Boundary responses only
            </label>
          </div>
          <button type="button" className="btn" onClick={load} disabled={loading}>
            Refresh
          </button>
        </div>
      </div>

      {loading ? (
        <Loading title="Loading audit log" />
      ) : error ? (
        <ErrorState title="Could not load audit log" detail={error} />
      ) : filtered.length === 0 ? (
        <EmptyState
          title="No audit records"
          detail="Run a few queries in the chat view to populate the log."
        />
      ) : (
        <div className="card" style={{ overflowX: "auto" }}>
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Role</th>
                <th>Query (redacted)</th>
                <th>Retrieved doc_ids</th>
                <th>Boundary</th>
                <th>Flags</th>
                <th>Latency</th>
                <th>trace_id</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((r) => (
                <tr key={r.trace_id}>
                  <td className="mono small">{formatTime(r.timestamp)}</td>
                  <td>
                    <span className="badge neutral">{r.role}</span>
                  </td>
                  <td style={{ maxWidth: 280 }}>{r.query}</td>
                  <td className="mono small">
                    {r.retrieved_doc_ids.length ? r.retrieved_doc_ids.join(", ") : "none"}
                  </td>
                  <td>
                    {r.boundary_triggered ? (
                      <span className="badge boundary">
                        {r.boundary_reason || "yes"}
                      </span>
                    ) : (
                      <span className="badge pass">no</span>
                    )}
                  </td>
                  <td>
                    {r.guardrail_flags.length ? (
                      r.guardrail_flags.map((f) => (
                        <span key={f} className="flag" style={{ marginRight: "0.25rem" }}>
                          {f}
                        </span>
                      ))
                    ) : (
                      <span className="muted small">none</span>
                    )}
                  </td>
                  <td className="mono small">{r.latency_ms.toFixed(0)} ms</td>
                  <td className="mono small">{r.trace_id.slice(0, 8)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function formatTime(ts: string): string {
  const d = new Date(ts);
  if (Number.isNaN(d.getTime())) return ts;
  return d.toLocaleString(undefined, {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}
