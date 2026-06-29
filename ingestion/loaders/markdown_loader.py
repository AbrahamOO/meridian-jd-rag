"""Markdown loader: YAML front-matter header plus Markdown body.

The body is already Markdown so headings (`#`) and pipe tables are preserved
verbatim for the structure-aware chunker. Front-matter is the leading
`---`-delimited YAML block. A file with no front-matter yields an empty header
mapping, which metadata validation then rejects loudly (missing classification).

The synthetic watermark blockquote (the line starting
``> **FICTIONAL DOCUMENT:``) is stripped from the chunkable body so it never
appears inside chunk text or embed_text; entity_status=FICTIONAL is already
carried in the metadata and on every chunk.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from ingestion.loaders.base import LoadedDocument, LoaderError, _read_text_utf8

_FENCE = "---"
# The fictional-document watermark blockquote line, stripped from the body.
_WATERMARK_RE = re.compile(r"^>\s*(?:\*\*)?FICTIONAL DOCUMENT:.*$", re.MULTILINE)


def _strip_watermark(body: str) -> str:
    """Remove the watermark blockquote line so it never enters a chunk."""
    return _WATERMARK_RE.sub("", body).lstrip("\n")


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    stripped = text.lstrip("﻿")  # drop a leading BOM if present
    if not stripped.startswith(_FENCE):
        return {}, text
    lines = stripped.splitlines()
    # First line is the opening fence; find the closing fence.
    for idx in range(1, len(lines)):
        if lines[idx].strip() == _FENCE:
            header_block = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1 :])
            try:
                parsed = yaml.safe_load(header_block) or {}
            except yaml.YAMLError as exc:
                raise LoaderError("parse_error", f"Invalid YAML front-matter: {exc}") from exc
            if not isinstance(parsed, dict):
                raise LoaderError("parse_error", "Front-matter must be a YAML mapping.")
            return parsed, body.lstrip("\n")
    # Opening fence with no close: treat the whole thing as body (no header).
    return {}, text


def load_markdown(path: Path) -> LoadedDocument:
    text, raw = _read_text_utf8(path)
    header, body = _split_front_matter(text)
    body = _strip_watermark(body)
    return LoadedDocument(path=str(path), header=header, body=body, raw_bytes=raw)
