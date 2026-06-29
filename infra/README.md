# Infrastructure: containers, compose, and IaC

Last updated: 2026-06-29

This directory packages Meridian J.D. RAG to run anywhere with one command and to
land cleanly in cloud.

## Contents

- `Dockerfile.api`: the FastAPI service on `python:3.12-slim`. Light core only
  (no torch, no cloud SDKs); the default profile is zero-key and runs the
  local/abstain providers, degrading to the deterministic mock embedder/reranker
  when `sentence-transformers` is absent. Runs as a non-root user. Healthcheck
  hits `/health`.
- `Dockerfile.ui`: a tiny static UI placeholder so the full stack is navigable
  before the React UI (owned by the frontend-engineer) lands.
- `docker-compose.yml`: brings up `postgres` (pgvector), `api`, and `ui` with one
  `docker compose up`. Init ordering: Postgres healthy -> the API runs an
  idempotent ingest -> uvicorn serves -> the UI waits for the API to be healthy.
  Every service has a healthcheck.
- `terraform/`: a minimal IaC stub. The root `main.tf` declares the provider and
  a single `platform` module; `modules/platform` documents the resource boundary
  (managed Postgres with pgvector, a container service for the API, a host for the
  UI, secrets for optional cloud keys). It is a stub on purpose: `terraform
  validate` stays clean without cloud credentials, and the variables/outputs are
  the contract a real module must satisfy.

## One-command startup

```bash
docker compose -f infra/docker-compose.yml up --build
# API:    http://localhost:8000  (/health, /query, /ingest, /evals)
# UI:     http://localhost:3000
# Postgres: localhost:5432  (mjd/mjd)
```

Zero keys are required. Set `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` /
`GEMINI_API_KEY` in a `.env` file (next to the compose file) only when switching a
provider to a cloud adapter in `config/local.yaml`. A cloud adapter constructed
without its key raises `MissingSecretError` at construction time, never at call
time, and never logs the key value (`providers/secrets.py`).

## Validating the compose file

```bash
docker compose -f infra/docker-compose.yml config   # parse + interpolate only
```

This validates structure and variable interpolation without requiring a running
Docker daemon.

## Change History

- 2026-06-29: Initial infra: API and UI Dockerfiles on python:3.12-slim,
  docker-compose with postgres/pgvector + api + ui (healthchecks + init ordering),
  Terraform provider + platform module stub. Added Last updated and Change History
  per the documentation date policy.
