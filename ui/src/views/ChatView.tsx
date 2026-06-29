import { useState } from "react";
import { ApiError, postQuery } from "../api";
import { CitationItem } from "../components/CitationItem";
import { ErrorState } from "../components/States";
import { PERSONAS, PERSONA_META } from "../types";
import type { Citation, Persona, QueryResponse } from "../types";

const SAMPLE_QUERIES = [
  "What cipher suites are approved for use?",
  "How is privileged access granted and reviewed?",
  "What are our AML escalation procedures?",
  "What dollar threshold triggers enhanced due diligence on a new corporate account?",
  "What is the model validation cadence under SR 11-7?",
];

interface Props {
  persona: Persona;
  onPersonaChange: (p: Persona) => void;
  onOpenCitation: (c: Citation) => void;
}

export function ChatView({ persona, onPersonaChange, onOpenCitation }: Props) {
  const [query, setQuery] = useState(SAMPLE_QUERIES[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [askedAs, setAskedAs] = useState<Persona | null>(null);

  async function ask() {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await postQuery(persona, query.trim(), { explain: false });
      setResult(res);
      setAskedAs(persona);
    } catch (e) {
      const msg = e instanceof ApiError ? e.message : "Unexpected error.";
      setError(msg);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  const isBoundary = result?.boundary_triggered === true;

  return (
    <>
      <div className="view-head">
        <h1>Access-controlled chat</h1>
        <p>
          Pick a persona, ask a question, then switch persona and ask the same
          question. Access is enforced server side at retrieval time, so the
          boundary changes with the role.
        </p>
      </div>

      <div className="card">
        <span className="label" id="persona-label">
          Persona (role under test)
        </span>
        <div className="persona-bar" role="group" aria-labelledby="persona-label">
          {PERSONAS.map((p) => {
            const meta = PERSONA_META[p];
            return (
              <button
                key={p}
                type="button"
                className="persona-chip"
                aria-pressed={p === persona}
                onClick={() => onPersonaChange(p)}
              >
                <span>{meta.label}</span>
                <span className="ceiling">
                  {meta.department} &middot; clears {meta.ceiling}
                </span>
              </button>
            );
          })}
        </div>

        <div className="active-persona-banner" aria-live="polite">
          <span>Asking as</span>
          <span className="who">{PERSONA_META[persona].label}</span>
          <span className="muted small">
            (clearance ceiling {PERSONA_META[persona].ceiling})
          </span>
        </div>

        <label className="label" htmlFor="query-input">
          Question
        </label>
        <textarea
          id="query-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "Enter") ask();
          }}
          placeholder="Ask a policy question"
        />
        <div className="spread" style={{ marginTop: "0.7rem" }}>
          <div className="persona-bar">
            {SAMPLE_QUERIES.map((q) => (
              <button
                key={q}
                type="button"
                className="persona-chip"
                onClick={() => setQuery(q)}
                aria-pressed={q === query}
              >
                <span className="small">{q}</span>
              </button>
            ))}
          </div>
          <button
            type="button"
            className="btn btn-primary"
            onClick={ask}
            disabled={loading || !query.trim()}
          >
            {loading ? "Asking..." : "Ask"}
          </button>
        </div>
      </div>

      {error ? (
        <div style={{ marginTop: "1.2rem" }}>
          <ErrorState title="Query failed" detail={error} />
        </div>
      ) : null}

      {result && askedAs ? (
        <div className={`card answer-card${isBoundary ? " boundary" : ""}`}>
          <div className="spread">
            <span className={`answer-status ${isBoundary ? "boundary" : "normal"}`}>
              {isBoundary ? "Boundary response" : "Grounded answer"}
            </span>
            <span className="small muted">
              answered as <b className="mono">{askedAs}</b>
            </span>
          </div>

          {isBoundary ? (
            <p className="small muted" style={{ marginTop: "-0.2rem" }}>
              This role cannot retrieve the requested content. Reason:{" "}
              <span className="flag">{result.boundary_reason || "boundary"}</span>
            </p>
          ) : null}

          <div className="answer-text">{result.answer}</div>

          {result.citations.length > 0 ? (
            <>
              <span className="label" style={{ marginTop: "1rem" }}>
                Citations
              </span>
              <ul className="citation-list">
                {result.citations.map((c, i) => (
                  <CitationItem key={`${c.doc_id}-${i}`} citation={c} onSelect={onOpenCitation} />
                ))}
              </ul>
            </>
          ) : (
            <p className="small muted" style={{ marginTop: "0.8rem" }}>
              No citations. {isBoundary || result.abstained
                ? "The system abstained rather than emit an uncited claim."
                : ""}
            </p>
          )}

          <div className="meta-row">
            <span>
              trace_id <b>{result.trace_id || "n/a"}</b>
            </span>
            <span>
              latency <b>{result.latency_ms.toFixed(1)} ms</b>
            </span>
            <span>
              cost <b>${result.cost_usd.toFixed(6)}</b>
            </span>
            <span>
              tokens <b>
                {result.tokens.prompt}/{result.tokens.completion}/{result.tokens.embed}
              </b>{" "}
              <span className="muted">(prompt/completion/embed)</span>
            </span>
            <span>
              retrieved{" "}
              <b>{result.retrieved_doc_ids.length ? result.retrieved_doc_ids.join(", ") : "none"}</b>
            </span>
            {result.error ? (
              <span>
                note <span className="flag">{result.error.code}</span>
              </span>
            ) : null}
          </div>
        </div>
      ) : null}
    </>
  );
}
