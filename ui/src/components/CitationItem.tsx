import type { Citation } from "../types";

interface Props {
  citation: Citation;
  onSelect: (c: Citation) => void;
}

// First-class clickable citation: doc_id + section_path + version (contracts 3.6).
export function CitationItem({ citation, onSelect }: Props) {
  return (
    <li>
      <button
        type="button"
        className="citation"
        onClick={() => onSelect(citation)}
        aria-label={`Open source ${citation.doc_id}, section ${citation.section_path}, version ${citation.version}`}
      >
        <span className="doc-id">{citation.doc_id}</span>
        <span className="cite-title">{citation.title}</span>
        <span className="cite-meta">
          {citation.section_path} &middot; v{citation.version}
        </span>
      </button>
    </li>
  );
}
