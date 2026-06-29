"""Layout-aware document loaders for Markdown, DOCX, PDF, and HTML.

Each loader returns a `LoadedDocument`: the raw front-matter mapping (or an
equivalent leading metadata block) plus a normalized Markdown body that
preserves heading hierarchy and tables, which the chunker depends on. Non-UTF8 /
binary / unparseable inputs are rejected loudly per gap-register G-11.
"""

from __future__ import annotations

from ingestion.loaders.base import LoadedDocument, LoaderError, load_path

__all__ = ["LoadedDocument", "LoaderError", "load_path"]
