"""Loader dispatch and the shared LoadedDocument record.

A loader's job is narrow: turn a source file into (raw_header_mapping,
markdown_body, raw_bytes) or REJECT it. Heavy parsers (python-docx, pypdf, bs4)
are imported lazily inside their loader so the Markdown-only CI path needs none
of them. All rejections raise LoaderError carrying a machine-readable reason
string aligned with the /ingest rejected[] reasons (gap-register G-11).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

SUPPORTED_SUFFIXES = {".md", ".markdown", ".docx", ".pdf", ".html", ".htm"}


class LoaderError(Exception):
    """Raised when a file cannot be loaded. ``reason`` is the machine code used
    in the /ingest rejected[] payload (e.g. ``non_utf8_or_binary``,
    ``unsupported_type``, ``parse_error``)."""

    def __init__(self, reason: str, message: str) -> None:
        super().__init__(message)
        self.reason = reason
        self.message = message


@dataclass(frozen=True)
class LoadedDocument:
    path: str
    header: dict[str, Any]  # parsed front-matter / leading metadata block
    body: str  # normalized Markdown body, headings + tables preserved
    raw_bytes: bytes  # source bytes, for content_hash idempotency


def _read_text_utf8(path: Path) -> tuple[str, bytes]:
    """Read a text file strictly as UTF-8. Reject on any decode error (G-11)."""
    raw = path.read_bytes()
    if b"\x00" in raw:
        raise LoaderError("non_utf8_or_binary", f"{path} contains NUL bytes (binary).")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise LoaderError(
            "non_utf8_or_binary",
            f"{path} is not valid UTF-8: {exc.reason} at byte {exc.start}.",
        ) from exc
    return text, raw


def load_path(path: str | Path) -> LoadedDocument:
    """Dispatch to the loader for the file's extension. Unsupported extensions
    are rejected, never best-effort parsed (G-11)."""
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise LoaderError(
            "unsupported_type",
            f"{p} has unsupported extension {suffix!r}; supported: "
            f"{sorted(SUPPORTED_SUFFIXES)}.",
        )

    if suffix in {".md", ".markdown"}:
        from ingestion.loaders.markdown_loader import load_markdown

        return load_markdown(p)
    if suffix == ".docx":
        from ingestion.loaders.docx_loader import load_docx

        return load_docx(p)
    if suffix == ".pdf":
        from ingestion.loaders.pdf_loader import load_pdf

        return load_pdf(p)
    # .html / .htm
    from ingestion.loaders.html_loader import load_html

    return load_html(p)


__all__ = [
    "SUPPORTED_SUFFIXES",
    "LoaderError",
    "LoadedDocument",
    "load_path",
    "_read_text_utf8",
]
