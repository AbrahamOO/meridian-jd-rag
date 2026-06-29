"""Leading metadata-block parser for non-Markdown formats (contract 2.1).

DOCX/PDF/HTML carry the same schema fields in a leading metadata block rather
than YAML front-matter. The convention used here: the document begins with the
same key: value lines the YAML header would contain, optionally fenced by a line
of `---`, before the first heading or body paragraph. This keeps one schema
across all four formats. The block is parsed as YAML so list fields like
`allowed_roles: [A, B]` work identically to Markdown front-matter.
"""

from __future__ import annotations

from typing import Any

import yaml

from ingestion.loaders.base import LoaderError

_SCHEMA_KEYS = {
    "doc_id",
    "title",
    "department",
    "doc_type",
    "classification",
    "owner_role",
    "allowed_roles",
    "effective_date",
    "version",
    "review_cycle_months",
    "regulatory_refs",
    "supersedes",
    "entity_status",
}


def split_meta_block(text: str) -> tuple[dict[str, Any], str]:
    """Extract a leading metadata block from plain text.

    Strategy: collect consecutive leading lines (skipping blank lines and an
    optional `---` fence) that look like `key: value` schema keys. Stop at the
    first line that is not a schema key/value, treating the remainder as body.
    The collected block is parsed as YAML so list and scalar coercion match the
    Markdown loader exactly.
    """
    lines = text.splitlines()
    header_lines: list[str] = []
    body_start = 0
    seen_key = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "---":
            body_start = idx + 1
            continue
        if not stripped:
            if seen_key:
                # Blank line after header keys ends the block.
                body_start = idx + 1
                break
            body_start = idx + 1
            continue
        key = stripped.split(":", 1)[0].strip()
        if ":" in stripped and key in _SCHEMA_KEYS:
            header_lines.append(line)
            seen_key = True
            body_start = idx + 1
            continue
        # First non-schema line ends the header.
        body_start = idx
        break

    if not header_lines:
        return {}, text

    try:
        parsed = yaml.safe_load("\n".join(header_lines)) or {}
    except yaml.YAMLError as exc:
        raise LoaderError("parse_error", f"Invalid metadata block: {exc}") from exc
    if not isinstance(parsed, dict):
        raise LoaderError("parse_error", "Metadata block must be a mapping.")
    body = "\n".join(lines[body_start:]).lstrip("\n")
    return parsed, body
