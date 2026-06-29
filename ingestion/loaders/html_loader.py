"""HTML loader (BeautifulSoup, lazy import).

Layout-aware: <h1>..<h6> become Markdown headings and <table> becomes a pipe
table so the structure-aware chunker and the never-split-a-table rule (G-10)
apply uniformly. The leading metadata block (contract 2.1) may be supplied
either as <meta> tags or as a leading text block; <meta name="doc_id" ...> style
tags are read first, then any leading key:value block in the visible text.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ingestion.loaders._metablock import _SCHEMA_KEYS, split_meta_block
from ingestion.loaders.base import LoadedDocument, LoaderError, _read_text_utf8


def _table_to_md(table) -> str:
    rows = table.find_all("tr")
    if not rows:
        return ""
    parsed: list[list[str]] = []
    for tr in rows:
        cells = tr.find_all(["th", "td"])
        parsed.append([c.get_text(" ", strip=True) for c in cells])
    parsed = [r for r in parsed if r]
    if not parsed:
        return ""
    header = parsed[0]
    out = ["| " + " | ".join(header) + " |"]
    out.append("| " + " | ".join("---" for _ in header) + " |")
    for body_row in parsed[1:]:
        cells = (body_row + [""] * len(header))[: len(header)]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def _meta_tags(soup) -> dict[str, Any]:
    header: dict[str, Any] = {}
    import yaml

    for tag in soup.find_all("meta"):
        name = tag.get("name")
        content = tag.get("content")
        if name in _SCHEMA_KEYS and content is not None:
            header[name] = yaml.safe_load(content)
    return header


def load_html(path: Path) -> LoadedDocument:
    text, raw = _read_text_utf8(path)
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:  # pragma: no cover - dep absent
        raise LoaderError("parse_error", "beautifulsoup4 not installed; cannot load HTML.") from exc

    try:
        soup = BeautifulSoup(text, "html.parser")
    except Exception as exc:  # noqa: BLE001
        raise LoaderError("parse_error", f"HTML parse failed: {type(exc).__name__}: {exc}") from exc

    meta_header = _meta_tags(soup)

    parts: list[str] = []
    body_root = soup.body or soup
    for el in body_root.descendants:
        name = getattr(el, "name", None)
        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(name[1])
            txt = el.get_text(" ", strip=True)
            if txt:
                parts.append("#" * level + " " + txt)
        elif name == "p":
            txt = el.get_text(" ", strip=True)
            if txt:
                parts.append(txt)
        elif name == "table":
            md = _table_to_md(el)
            if md:
                parts.append(md)

    body = "\n\n".join(parts)
    block_header, content = split_meta_block(body)
    # <meta> tags win over an in-body block when both are present.
    header = {**block_header, **meta_header}
    if meta_header:
        content = body if not block_header else content
    return LoadedDocument(path=str(path), header=header, body=content, raw_bytes=raw)
