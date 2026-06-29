"""DOCX loader (python-docx, lazy import).

Layout-aware: Word heading styles (Heading 1..N) become Markdown `#` headings so
the structure-aware chunker sees the same hierarchy as Markdown. Tables become
GitHub-style pipe tables so the never-split-a-table rule (G-10) applies
uniformly. A parse failure is a rejection with the exception class name, never a
partial extraction fed downstream (G-11).
"""

from __future__ import annotations

from pathlib import Path

from ingestion.loaders._metablock import split_meta_block
from ingestion.loaders.base import LoadedDocument, LoaderError


def _heading_level(style_name: str | None) -> int | None:
    if not style_name:
        return None
    name = style_name.strip().lower()
    if name.startswith("heading "):
        try:
            return int(name.split(" ", 1)[1])
        except (ValueError, IndexError):
            return None
    if name in {"title"}:
        return 1
    return None


def _table_to_md(table) -> str:
    rows: list[list[str]] = []
    for row in table.rows:
        rows.append([cell.text.replace("\n", " ").strip() for cell in row.cells])
    if not rows:
        return ""
    header = rows[0]
    out = ["| " + " | ".join(header) + " |"]
    out.append("| " + " | ".join("---" for _ in header) + " |")
    for body_row in rows[1:]:
        # Pad/truncate to header width to keep the table well-formed.
        cells = (body_row + [""] * len(header))[: len(header)]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def load_docx(path: Path) -> LoadedDocument:
    raw = path.read_bytes()
    try:
        import docx  # python-docx
    except ImportError as exc:  # pragma: no cover - heavy dep absent
        raise LoaderError("parse_error", "python-docx not installed; cannot load DOCX.") from exc

    try:
        document = docx.Document(str(path))
    except Exception as exc:  # noqa: BLE001 - any parse failure is a rejection
        raise LoaderError("parse_error", f"DOCX parse failed: {type(exc).__name__}: {exc}") from exc

    parts: list[str] = []
    # Iterate body elements in document order so tables stay positioned.
    body = document.element.body
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for child in body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            para = Paragraph(child, document)
            text = para.text.strip()
            if not text:
                continue
            level = _heading_level(para.style.name if para.style else None)
            if level:
                parts.append("#" * max(1, min(level, 6)) + " " + text)
            else:
                parts.append(text)
        elif tag == "tbl":
            table = Table(child, document)
            md = _table_to_md(table)
            if md:
                parts.append(md)

    full = "\n\n".join(parts)
    header, content = split_meta_block(full)
    return LoadedDocument(path=str(path), header=header, body=content, raw_bytes=raw)
