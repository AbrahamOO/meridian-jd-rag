import { useState } from "react";
import { ApiError, postQuery } from "../api";
import { EmptyState, ErrorState } from "../components/States";
import { PERSONAS, PERSONA_META } from "../types";
import type { ExplainCandidate, Persona, QueryExplain, QueryResponse } from "../types";

type Strategy = "production" | "naive";

interface Props {
  persona: Persona;
  onPersonaChange: (p: Persona) => void;
}

interface ExplainBundle {
  strategy: Strategy;
  explain: QueryExplain | null;
  response: QueryResponse;
}

export function ChunkView({ persona, onPersonaChange }: Props) {
  const [query, setQuery] = useState("How are encryption keys rotated and managed?");
  const [strategy, setStrategy] = useState<Strategy>("production");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [bundles, setBundles] = useState<Record<Strategy, ExplainBundle | null>>({
    production: null,
    naive: null,
  });

  async function run(target: Strategy) {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await postQuery(persona, query.trim(), {
        explain: true,
        chunk_strategy: target,
      });
      setBundles((prev) => ({
        ...prev,
        [target]: { strategy: target, explain: res.explain, response: res },
      }));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Unexpected error.");
    } finally {
      setLoading(false);
    }
  }

  async function runBoth() {
    await run("production");
    await run("naive");
    setStrategy("production");
  }

  const active = bundles[strategy];

  return (
    <>
      <div className="view-head">
        <h1>Chunking and retrieval visualizer</h1>
        <p>
          Run a query under the explain payload to see which chunks are retrieved
          and how they score. Toggle naive against production chunking to see the
          difference. The explain payload is restricted to in-scope content for
          the selected role.
        </p>
      </div>

      <div className="card stack">
        <div className="grid" style={{ gridTemplateColumns: "minmax(0, 1fr) minmax(0, 1fr)" }}>
          <div>
            <label className="label" htmlFor="chunk-query">
              Query
            </label>
            <input
              id="chunk-query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          <div>
            <label className="label" htmlFor="chunk-persona">
              Persona
            </label>
            <select
              id="chunk-persona"
              value={persona}
              onChange={(e) => onPersonaChange(e.target.value as Persona)}
            >
              {PERSONAS.map((p) => (
                <option key={p} value={p}>
                  {PERSONA_META[p].label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="spread">
          <div className="toggle-row" role="group" aria-label="Chunking strategy">
            {(["production", "naive"] as Strategy[]).map((s) => (
              <button
                key={s}
                type="button"
                aria-pressed={strategy === s}
                onClick={() => setStrategy(s)}
              >
                {s}
              </button>
            ))}
          </div>
          <button type="button" className="btn btn-primary" onClick={runBoth} disabled={loading}>
            {loading ? "Retrieving..." : "Retrieve under both strategies"}
          </button>
        </div>
      </div>

      {error ? (
        <div style={{ marginTop: "1.2rem" }}>
          <ErrorState title="Retrieval failed" detail={error} />
        </div>
      ) : null}

      {active ? (
        <ExplainPanel bundle={active} />
      ) : (
        <div className="card" style={{ marginTop: "1.2rem" }}>
          <EmptyState
            title={`No ${strategy} run yet`}
            detail="Run a query to populate the explain payload for this strategy."
          />
        </div>
      )}

      {bundles.production && bundles.naive ? (
        <DeltaSummary production={bundles.production} naive={bundles.naive} />
      ) : null}
    </>
  );
}

function ExplainPanel({ bundle }: { bundle: ExplainBundle }) {
  const explain = bundle.explain;
  const candidates = explain?.candidates ?? [];
  const rerankOrder = explain?.rerank_order ?? [];
  const dropped = new Set(explain?.dropped_for_budget ?? []);
  const topRerank = new Set(rerankOrder.slice(0, 6));
  const rerankRank = new Map(rerankOrder.map((id, i) => [id, i + 1]));

  const sorted = [...candidates].sort((a, b) => b.rrf_score - a.rrf_score);

  return (
    <div className="card stack" style={{ marginTop: "1.2rem" }}>
      <div className="spread">
        <h2 className="section-title" style={{ margin: 0 }}>
          {bundle.strategy} retrieval &middot; {candidates.length} candidates
        </h2>
        <span className="small muted">
          {bundle.response.retrieved_doc_ids.length} doc(s) assembled
          {dropped.size > 0 ? `, ${dropped.size} parent(s) dropped for budget` : ""}
        </span>
      </div>

      {explain?.transformed ? (
        <div className="small muted">
          Transforms used:{" "}
          {explain.transformed.used.length ? (
            explain.transformed.used.map((t) => (
              <span key={t} className="badge neutral" style={{ marginRight: "0.3rem" }}>
                {t}
              </span>
            ))
          ) : (
            <span>none</span>
          )}
          {explain.transformed.rewritten &&
          explain.transformed.rewritten !== bundle.response.answer ? (
            <div>
              Rewritten query: <span className="mono">{explain.transformed.rewritten}</span>
            </div>
          ) : null}
        </div>
      ) : null}

      {candidates.length === 0 ? (
        <EmptyState
          title="No candidates retrieved for this role"
          detail="Either the access filter matched nothing or the index has no chunks for this strategy."
        />
      ) : (
        <div className="chunk-stream">
          {sorted.map((c) => (
            <ChunkRow
              key={c.chunk_id}
              c={c}
              isTopRerank={topRerank.has(c.chunk_id)}
              rerankRank={rerankRank.get(c.chunk_id)}
              dropped={dropped.has(c.chunk_id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function ChunkRow({
  c,
  isTopRerank,
  rerankRank,
  dropped,
}: {
  c: ExplainCandidate;
  isTopRerank: boolean;
  rerankRank: number | undefined;
  dropped: boolean;
}) {
  const cls = ["chunk", "retrieved"];
  if (isTopRerank) cls.push("reranked-top");
  if (c.is_superseded) cls.push("superseded");

  return (
    <div className={cls.join(" ")}>
      <div className="chunk-head">
        <span className="chunk-id">{c.chunk_id}</span>
        <span className="section">{c.doc_id} &middot; {c.section_path}</span>
        {rerankRank ? <span className="badge pass">rerank #{rerankRank}</span> : null}
        {c.is_superseded ? <span className="badge boundary">superseded</span> : null}
        {dropped ? <span className="badge fail">dropped for budget</span> : null}
        <span className="chunk-score">rrf {c.rrf_score.toFixed(5)}</span>
      </div>
      <div className="small muted">
        dense rank {c.dense_rank ?? "n/a"} &middot; sparse rank {c.sparse_rank ?? "n/a"}
      </div>
    </div>
  );
}

function DeltaSummary({
  production,
  naive,
}: {
  production: ExplainBundle;
  naive: ExplainBundle;
}) {
  const pCount = production.explain?.candidates.length ?? 0;
  const nCount = naive.explain?.candidates.length ?? 0;
  const pDocs = production.response.retrieved_doc_ids;
  const nDocs = naive.response.retrieved_doc_ids;
  const onlyProd = pDocs.filter((d) => !nDocs.includes(d));
  const onlyNaive = nDocs.filter((d) => !pDocs.includes(d));

  return (
    <div className="card stack" style={{ marginTop: "1.2rem" }}>
      <h2 className="section-title" style={{ margin: 0 }}>
        Production vs naive
      </h2>
      <div className="stat-grid">
        <div className="stat">
          <div className="stat-value">{pCount}</div>
          <div className="stat-label">production candidates</div>
        </div>
        <div className="stat">
          <div className="stat-value">{nCount}</div>
          <div className="stat-label">naive candidates</div>
        </div>
        <div className="stat">
          <div className="stat-value">{pDocs.length}</div>
          <div className="stat-label">production docs assembled</div>
        </div>
        <div className="stat">
          <div className="stat-value">{nDocs.length}</div>
          <div className="stat-label">naive docs assembled</div>
        </div>
      </div>
      <div className="small">
        <div>
          Docs only production found:{" "}
          <span className="mono">{onlyProd.length ? onlyProd.join(", ") : "none"}</span>
        </div>
        <div>
          Docs only naive found:{" "}
          <span className="mono">{onlyNaive.length ? onlyNaive.join(", ") : "none"}</span>
        </div>
      </div>
    </div>
  );
}
