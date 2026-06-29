# Meridian J.D. RAG UI

Created: 2026-06-29
Last updated: 2026-06-29

Demo UI for the Meridian J.D. RAG system. Meridian John Doe Financial is a
synthetic, fictional company. Every document carries entity_status: FICTIONAL.
This single-page app is the showcase layer a reviewer clicks through. It renders
data from the API only and never recomputes metrics.

## Stack

Vite + React + TypeScript single-page app. Charts use Recharts. Pinned to the
latest published versions at build time:

| Package | Version |
| --- | --- |
| react | 19.2.7 |
| react-dom | 19.2.7 |
| vite | 8.1.0 |
| @vitejs/plugin-react | 6.0.3 |
| typescript | 6.0.3 |
| recharts | 3.9.0 |
| @types/react | 19.2.17 |
| @types/react-dom | 19.2.3 |

## The four views

1. Chat with role switcher. Pick one of the seven personas, ask a question, and
   read the answer with first-class clickable citations (doc_id, section_path,
   version). Switch persona and ask the same question to watch the access
   boundary change. A boundary or abstention response renders distinctly from a
   grounded answer. Citations open a side drawer with the exact source
   coordinates.
2. Chunking visualizer. Run a query under the explain payload to see which chunks
   are retrieved, their RRF scores, dense and sparse ranks, rerank order, and
   parents dropped for budget. Toggle naive against production chunking and view
   the difference, including a docs-only-in-each summary.
3. Eval dashboard. Reads the latest report from GET /evals. Shows the
   access-control pass or fail board per persona (derived from per-record
   security.access_enforced plus the aggregate
   security.access_control_pass_pct and blocking_failures), the naive vs
   production retrieval delta panel, generation faithfulness, latency, cost, and
   a trend line across runs.
4. Audit log viewer. Recent requests with role, retrieved doc_ids,
   boundary_triggered with reason, guardrail flags, latency, and trace_id.
   Filterable by role and to boundary responses only.

## Configuration

The API base URL is config-driven through the VITE_API_BASE environment
variable. It defaults to http://localhost:8000 when unset. Copy .env.example to
.env to override during local development.

## Develop

    npm install
    npm run dev      # http://localhost:3000

## Build

    npm install
    npm run build    # type-checks then emits the production bundle to dist/
    npm run preview  # serve the built bundle on http://localhost:3000

## Container

Built and served by infra/Dockerfile.ui (multi-stage: Node build, nginx serve on
port 3000). It comes up alongside the API and Postgres under
`docker compose up` from the infra directory.

## API contract notes

This UI is built strictly to docs/contracts.md and the real endpoints in
api/app.py. One observation, surfaced not worked around: the eval report
security block (contracts 7.3) exposes only the aggregate
security.access_control_pass_pct and a blocking_failures list, with no
per-persona breakdown. The per-persona access board is therefore derived
client side from the per-record results array (each record carries persona and
security.access_enforced). No fields were invented.

## Change History

- 2026-06-29: Initial UI build: Vite + React + TypeScript single-page app with the four reviewer views (chat with role switcher and clickable citations, chunking visualizer with naive vs production toggle, eval dashboard with per-persona access board, audit log viewer), fictional banner, health pill, config-driven API base URL, and multi-stage nginx container.
