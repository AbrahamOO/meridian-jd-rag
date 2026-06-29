"""Offline ingestion pipeline for Meridian J.D. RAG.

Loaders -> fail-closed metadata validation -> PII redaction -> chunking
(production + naive) -> embedding -> index write + manifest. Heavy ML and DB
deps are lazy-imported so the zero-key mock/CI path stays light.
"""
