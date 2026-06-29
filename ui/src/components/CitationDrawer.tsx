import { useEffect } from "react";
import type { Citation } from "../types";

interface Props {
  citation: Citation | null;
  onClose: () => void;
}

// The API does not return raw source text in the citation object (contracts 3.6
// is doc_id + title + section_path + version only), so the drawer surfaces the
// exact source coordinates a reviewer needs to locate the section in the corpus
// rather than inventing document body text.
export function CitationDrawer({ citation, onClose }: Props) {
  useEffect(() => {
    if (!citation) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [citation, onClose]);

  if (!citation) return null;

  return (
    <div
      style={overlay}
      onClick={onClose}
      role="presentation"
    >
      <aside
        style={panel}
        role="dialog"
        aria-modal="true"
        aria-label={`Source ${citation.doc_id}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="spread" style={{ marginBottom: "1rem" }}>
          <span className="doc-id" style={{ fontSize: "1rem" }}>
            {citation.doc_id}
          </span>
          <button type="button" className="btn" onClick={onClose} aria-label="Close source">
            Close
          </button>
        </div>
        <h2 style={{ margin: "0 0 1rem", fontSize: "1.1rem" }}>{citation.title}</h2>
        <dl style={{ margin: 0 }}>
          <Field label="Document" value={citation.doc_id} mono />
          <Field label="Section path" value={citation.section_path} mono />
          <Field label="Version" value={citation.version} mono />
        </dl>
        <p className="small muted" style={{ marginTop: "1.5rem" }}>
          These are the exact source coordinates returned by the access-controlled
          retrieval pipeline. The citation was re-validated against the requesting
          role after generation, so it references a document this persona is
          permitted to read.
        </p>
        <p className="small muted">
          Corpus path: <span className="mono">corpus/{deptFolder(citation.doc_id)}/</span>
        </p>
      </aside>
    </div>
  );
}

function Field({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div style={{ marginBottom: "0.8rem" }}>
      <dt className="label" style={{ marginBottom: "0.15rem" }}>
        {label}
      </dt>
      <dd className={mono ? "mono" : undefined} style={{ margin: 0 }}>
        {value}
      </dd>
    </div>
  );
}

const DEPT_MAP: Record<string, string> = {
  OPS: "operations",
  CMP: "compliance",
  TEC: "technology",
  SEC: "security",
  RSK: "risk",
  FIN: "finance",
  RET: "retail",
};

function deptFolder(docId: string): string {
  const code = docId.split("-")[1];
  return DEPT_MAP[code] ?? "unknown";
}

const overlay: React.CSSProperties = {
  position: "fixed",
  inset: 0,
  background: "rgba(0,0,0,0.55)",
  display: "flex",
  justifyContent: "flex-end",
  zIndex: 50,
};

const panel: React.CSSProperties = {
  width: "min(420px, 92vw)",
  height: "100%",
  background: "var(--bg-raised)",
  borderLeft: "1px solid var(--border-strong)",
  padding: "1.5rem",
  overflowY: "auto",
  boxShadow: "var(--shadow)",
};
