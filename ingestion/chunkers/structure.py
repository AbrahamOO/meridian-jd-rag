"""Markdown structure parser shared by the chunkers.

Parses a normalized Markdown body into a flat list of `Segment`s, each tagged as
a heading, a paragraph, or an atomic table. Heading levels build the
`section_path` ("3 > 3.2 > 3.2.1") that the production chunker uses for both the
contextual header and small-to-big parent grouping. Tables are kept whole (G-10).
Character offsets into the source body are tracked for the chunk visualizer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
# A numbered-section prefix like "3.2.1" at the start of a heading text, used to
# build the canonical section_path "3 > 3.2 > 3.2.1".
_NUM_PREFIX_RE = re.compile(r"^(\d+(?:\.\d+)*)")
_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:\-|]+\|?\s*$")


@dataclass
class Segment:
    kind: str  # "heading" | "paragraph" | "table"
    text: str
    char_start: int
    char_end: int
    level: int = 0  # heading level for kind == "heading"
    section_path: str = ""  # path of the section this segment lives in
    heading_title: str = ""  # nearest heading text for paragraphs/tables


@dataclass
class _Block:
    lines: list[str] = field(default_factory=list)
    start: int = 0
    end: int = 0


def _line_offsets(body: str) -> list[int]:
    offsets = [0]
    for line in body.split("\n"):
        offsets.append(offsets[-1] + len(line) + 1)  # +1 for the newline
    return offsets


def _section_path_from_stack(stack: list[tuple[int, str]]) -> str:
    """Build a section_path. Prefer numeric prefixes if every level has one,
    else join heading titles. Returns segments joined by ' > '."""
    if not stack:
        return ""
    numeric: list[str] = []
    for _level, title in stack:
        m = _NUM_PREFIX_RE.match(title.strip())
        if m:
            numeric.append(m.group(1))
    if len(numeric) == len(stack) and numeric:
        return " > ".join(numeric)
    return " > ".join(title.strip() for _level, title in stack)


def parse_segments(body: str) -> list[Segment]:
    """Parse Markdown into ordered segments with section paths and offsets."""
    lines = body.split("\n")
    offsets = _line_offsets(body)
    segments: list[Segment] = []
    heading_stack: list[tuple[int, str]] = []  # (level, title)

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        heading_match = _HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            # Pop deeper-or-equal levels off the stack.
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))
            path = _section_path_from_stack(heading_stack)
            segments.append(
                Segment(
                    kind="heading",
                    text=title,
                    char_start=offsets[i],
                    char_end=offsets[i] + len(line),
                    level=level,
                    section_path=path,
                    heading_title=title,
                )
            )
            i += 1
            continue

        # Table: a run of consecutive pipe rows. Kept atomic (G-10).
        if _TABLE_ROW_RE.match(line):
            start_line = i
            table_lines = [line]
            j = i + 1
            while j < n and _TABLE_ROW_RE.match(lines[j]):
                table_lines.append(lines[j])
                j += 1
            # Only treat as a table if it has a separator row (real MD table).
            is_table = len(table_lines) >= 2 and _TABLE_SEP_RE.match(table_lines[1])
            if is_table:
                path = _section_path_from_stack(heading_stack)
                title = heading_stack[-1][1] if heading_stack else ""
                segments.append(
                    Segment(
                        kind="table",
                        text="\n".join(table_lines),
                        char_start=offsets[start_line],
                        char_end=offsets[j - 1] + len(table_lines[-1]),
                        section_path=path,
                        heading_title=title,
                    )
                )
                i = j
                continue

        if line.strip() == "":
            i += 1
            continue

        # Paragraph: a run of non-blank, non-heading, non-table lines.
        start_line = i
        para_lines = [line]
        j = i + 1
        while j < n:
            nxt = lines[j]
            if nxt.strip() == "" or _HEADING_RE.match(nxt) or _TABLE_ROW_RE.match(nxt):
                break
            para_lines.append(nxt)
            j += 1
        path = _section_path_from_stack(heading_stack)
        title = heading_stack[-1][1] if heading_stack else ""
        segments.append(
            Segment(
                kind="paragraph",
                text="\n".join(para_lines),
                char_start=offsets[start_line],
                char_end=offsets[j - 1] + len(para_lines[-1]),
                section_path=path,
                heading_title=title,
            )
        )
        i = j

    return segments
