# Meridian J.D. RAG: one-command packaging targets (devops-packaging contract 5).
#
# Profile selection is via MJD_PROFILE (default: ci for test/eval reproducibility,
# default for `up`). All targets are runnable from a clean clone with no API keys.

PYTHON ?= python
PROFILE ?= ci
COMPOSE ?= docker compose -f infra/docker-compose.yml

.DEFAULT_GOAL := help
.PHONY: help up down ingest eval prove-access test lint fmt docs-sync hooks

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

up: ## Bring up the full stack (postgres + api + ui) with one command.
	$(COMPOSE) up --build

down: ## Tear the stack down and remove volumes.
	$(COMPOSE) down -v

ingest: ## Build the index from the corpus (MJD_PROFILE selects providers).
	MJD_PROFILE=$(PROFILE) $(PYTHON) -m scripts.ingest --mode full --strategies production,naive

eval: ## Run the eval suite (ci|full via SUITE=...). Skips cleanly if absent.
	@if [ -f scripts/run_evals.py ]; then \
		MJD_PROFILE=$(PROFILE) $(PYTHON) scripts/run_evals.py --suite $(or $(SUITE),ci); \
	elif [ -f evals/run.py ]; then \
		MJD_PROFILE=$(PROFILE) $(PYTHON) -m evals.run --suite $(or $(SUITE),ci); \
	else \
		echo "eval: harness not present yet (part of the eval suite); nothing to run."; \
	fi

prove-access: ## Run the access-control proof battery (zero leaks required).
	MJD_PROFILE=$(PROFILE) $(PYTHON) scripts/prove_access_control.py

test: ## Run the test suite under MJD_PROFILE=ci.
	MJD_PROFILE=ci $(PYTHON) -m pytest tests/ -q

lint: ## Run ruff + mypy + black --check.
	ruff check .
	black --check .
	mypy api observability config core providers retrieval generation ingestion

fmt: ## Auto-format with black + ruff --fix.
	black .
	ruff check --fix .

docs-sync: ## Run the docs-sync drift guard.
	bash scripts/check_docs_sync.sh

hooks: ## Install the docs-sync git pre-commit hook.
	@mkdir -p .git/hooks
	@printf '#!/usr/bin/env bash\nexec bash scripts/check_docs_sync.sh\n' > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "Installed docs-sync pre-commit hook."
