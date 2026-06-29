import { useEffect, useState } from "react";
import { ApiError, getHealth } from "./api";
import { CitationDrawer } from "./components/CitationDrawer";
import { AuditView } from "./views/AuditView";
import { ChatView } from "./views/ChatView";
import { ChunkView } from "./views/ChunkView";
import { EvalView } from "./views/EvalView";
import type { Citation, HealthResponse, Persona } from "./types";

type Tab = "chat" | "chunks" | "evals" | "audit";

const TABS: { id: Tab; label: string }[] = [
  { id: "chat", label: "Chat" },
  { id: "chunks", label: "Chunking visualizer" },
  { id: "evals", label: "Eval dashboard" },
  { id: "audit", label: "Audit log" },
];

export function App() {
  const [tab, setTab] = useState<Tab>("chat");
  const [persona, setPersona] = useState<Persona>("SOFTWARE_ENGINEER");
  const [citation, setCitation] = useState<Citation | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthErr, setHealthErr] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const poll = () => {
      getHealth()
        .then((h) => active && (setHealth(h), setHealthErr(null)))
        .catch((e) => active && setHealthErr(e instanceof ApiError ? e.message : "unreachable"));
    };
    poll();
    const id = window.setInterval(poll, 20000);
    return () => {
      active = false;
      window.clearInterval(id);
    };
  }, []);

  return (
    <div className="app-shell">
      <div className="fictional-banner" role="note">
        <strong>Fictional</strong>
        <span>
          Meridian John Doe Financial is a synthetic company. All documents, data,
          and policies are fabricated for demonstration. entity_status: FICTIONAL.
        </span>
      </div>

      <header className="app-header">
        <div className="brand">
          <span className="brand-mark">
            Meridian J<span className="dot">.</span>D<span className="dot">.</span> RAG
          </span>
          <span className="brand-sub">Access-controlled retrieval demo</span>
        </div>
        <HealthPill health={health} error={healthErr} />
      </header>

      <nav className="nav-tabs" aria-label="Views">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            className="nav-tab"
            aria-current={tab === t.id ? "page" : undefined}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <main>
        {tab === "chat" && (
          <ChatView
            persona={persona}
            onPersonaChange={setPersona}
            onOpenCitation={setCitation}
          />
        )}
        {tab === "chunks" && <ChunkView persona={persona} onPersonaChange={setPersona} />}
        {tab === "evals" && <EvalView />}
        {tab === "audit" && <AuditView />}
      </main>

      <CitationDrawer citation={citation} onClose={() => setCitation(null)} />
    </div>
  );
}

function HealthPill({
  health,
  error,
}: {
  health: HealthResponse | null;
  error: string | null;
}) {
  let dot = "warn";
  let text = "checking API";
  if (error) {
    dot = "bad";
    text = "API unreachable";
  } else if (health) {
    dot = health.ok ? "ok" : "warn";
    const idx = health.index?.loaded ? "index loaded" : "no index";
    text = health.ok ? `healthy (${health.profile})` : `degraded, ${idx}`;
  }
  return (
    <span className="health-pill" title={error ?? JSON.stringify(health?.providers ?? {})}>
      <span className={`health-dot ${dot}`} aria-hidden="true" />
      {text}
    </span>
  );
}
