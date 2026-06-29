"""PDF loader (pypdf, lazy import).

PDF carries no reliable heading-style metadata, so extraction is best-effort
text per page joined with blank lines; the leading metadata block convention
(contract 2.1) supplies the schema header. A parse exception is a rejection with
the exception class name (G-11), never a partial/garbled extraction sent to the
embedder.
"""

from __future__ import annotations

from pathlib import Path

from ingestion.loaders._metablock import split_meta_block
from ingestion.loaders.base import LoadedDocument, LoaderError


def load_pdf(path: Path) -> LoadedDocument:
    raw = path.read_bytes()
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - heavy dep absent
        raise LoaderError("parse_error", "pypdf not installed; cannot load PDF.") from exc

    try:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception as exc:  # noqa: BLE001 - any parse failure is a rejection
        raise LoaderError("parse_error", f"PDF parse failed: {type(exc).__name__}: {exc}") from exc

    full = "\n\n".join(p.strip() for p in pages if p.strip())
    header, content = split_meta_block(full)
    return LoadedDocument(path=str(path), header=header, body=content, raw_bytes=raw)
