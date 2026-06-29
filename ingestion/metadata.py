"""Fail-closed document metadata parsing and validation (contract 2.1, G-06).

Validation is loud and fail-closed. A document missing or carrying an invalid
`classification` or `allowed_roles` is REJECTED, never silently defaulted. Each
rejection carries the offending doc_id (or path when the id itself is bad) and
the field. Corpus-wide checks (duplicate doc_id G-13, dangling supersedes) run
across the parsed set before any embedding.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from core.models import (
    CANONICAL_PERSONAS,
    CLASSIFICATIONS,
    DEPARTMENTS,
    DOC_TYPES,
    DocumentMetadata,
)

DOC_ID_RE = re.compile(r"^MJD-(OPS|CMP|TEC|SEC|RSK|FIN|RET)-\d{4}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class Rejection:
    """A fail-closed validation failure (maps to /ingest rejected[] entries)."""

    path: str
    doc_id: str | None
    reason: str
    detail: str


class MetadataError(Exception):
    """Raised when validation produces one or more rejections. Carries the full
    list so an all-or-nothing full ingest can report every offender at once."""

    def __init__(self, rejections: list[Rejection]) -> None:
        self.rejections = rejections
        joined = "; ".join(f"{r.doc_id or r.path}: {r.reason} ({r.detail})" for r in rejections)
        super().__init__(f"metadata validation failed: {joined}")


def _as_str(value: object) -> str | None:
    if isinstance(value, str):
        return value
    if value is None:
        return None
    return str(value)


def validate_header(path: str, header: dict[str, object]) -> DocumentMetadata | Rejection:
    """Validate one parsed header. Returns a DocumentMetadata on success or a
    Rejection (never raises) so the caller can aggregate all failures."""

    doc_id_raw = header.get("doc_id")
    doc_id = _as_str(doc_id_raw)

    if not doc_id or not DOC_ID_RE.match(doc_id):
        return Rejection(
            path,
            doc_id if isinstance(doc_id, str) else None,
            "bad_doc_id",
            f"doc_id {doc_id_raw!r} must match {DOC_ID_RE.pattern}.",
        )

    classification = _as_str(header.get("classification"))
    if not classification:
        return Rejection(
            path, doc_id, "missing_classification", "classification is empty or absent."
        )
    if classification not in CLASSIFICATIONS:
        return Rejection(
            path,
            doc_id,
            "invalid_classification",
            f"classification {classification!r} not in {sorted(CLASSIFICATIONS)}.",
        )

    allowed_roles = header.get("allowed_roles")
    if not isinstance(allowed_roles, list) or not allowed_roles:
        return Rejection(path, doc_id, "missing_allowed_roles", "allowed_roles is empty or absent.")
    bad_roles = [r for r in allowed_roles if r not in CANONICAL_PERSONAS]
    if bad_roles:
        return Rejection(
            path, doc_id, "unknown_role", f"allowed_roles contains unknown roles {bad_roles}."
        )

    title = _as_str(header.get("title"))
    if not title or not title.strip():
        return Rejection(path, doc_id, "missing_title", "title is empty or absent.")

    department = _as_str(header.get("department"))
    if department not in DEPARTMENTS:
        return Rejection(path, doc_id, "invalid_department", f"department {department!r} invalid.")

    doc_type = _as_str(header.get("doc_type"))
    if doc_type not in DOC_TYPES:
        return Rejection(path, doc_id, "invalid_doc_type", f"doc_type {doc_type!r} invalid.")

    version = _as_str(header.get("version"))
    if not version or not SEMVER_RE.match(version):
        return Rejection(path, doc_id, "invalid_semver", f"version {version!r} is not semver.")

    effective_date = _as_str(header.get("effective_date"))
    if not effective_date or not DATE_RE.match(effective_date):
        return Rejection(
            path, doc_id, "invalid_date", f"effective_date {effective_date!r} invalid."
        )

    review_cycle = header.get("review_cycle_months")
    if not isinstance(review_cycle, int) or isinstance(review_cycle, bool) or review_cycle <= 0:
        return Rejection(
            path,
            doc_id,
            "invalid_review_cycle",
            f"review_cycle_months {review_cycle!r} must be a positive int.",
        )

    entity_status = _as_str(header.get("entity_status"))
    if entity_status != "FICTIONAL":
        return Rejection(
            path, doc_id, "invalid_entity_status", "entity_status must be the literal FICTIONAL."
        )

    owner_role = _as_str(header.get("owner_role")) or ""

    regulatory_refs = header.get("regulatory_refs", [])
    if regulatory_refs is None:
        regulatory_refs = []
    if not isinstance(regulatory_refs, list):
        return Rejection(path, doc_id, "invalid_regulatory_refs", "regulatory_refs must be a list.")

    supersedes_raw = header.get("supersedes")
    supersedes = _as_str(supersedes_raw) if supersedes_raw is not None else None
    if supersedes is not None and not DOC_ID_RE.match(supersedes):
        return Rejection(
            path, doc_id, "bad_supersedes", f"supersedes {supersedes!r} is not a valid doc_id."
        )

    return DocumentMetadata(
        doc_id=doc_id,
        title=title.strip(),
        department=department,  # type: ignore[arg-type]
        doc_type=doc_type,  # type: ignore[arg-type]
        classification=classification,
        owner_role=owner_role,
        allowed_roles=[str(r) for r in allowed_roles],
        effective_date=effective_date,
        version=version,
        review_cycle_months=review_cycle,
        regulatory_refs=[str(r) for r in regulatory_refs],
        supersedes=supersedes,
        entity_status="FICTIONAL",
    )


def validate_corpus(
    parsed: list[tuple[str, dict[str, object]]],
) -> tuple[dict[str, DocumentMetadata], list[Rejection]]:
    """Validate a whole corpus. Returns (valid_by_doc_id, rejections).

    Corpus-wide rules:
    - duplicate doc_id rejects ALL copies sharing the id (G-13).
    - dangling supersedes (points at a doc_id not in the corpus) rejects the
      pointing doc.
    """
    per_doc: list[tuple[str, DocumentMetadata]] = []
    rejections: list[Rejection] = []

    # Pass 1: per-document validation.
    for path, header in parsed:
        result = validate_header(path, header)
        if isinstance(result, Rejection):
            rejections.append(result)
        else:
            per_doc.append((path, result))

    # Pass 2: duplicate doc_id detection (G-13) across all valid headers.
    by_id: dict[str, list[tuple[str, DocumentMetadata]]] = {}
    for path, meta in per_doc:
        by_id.setdefault(meta.doc_id, []).append((path, meta))

    valid: dict[str, DocumentMetadata] = {}
    for doc_id, entries in by_id.items():
        if len(entries) > 1:
            paths = [p for p, _ in entries]
            for p in paths:
                rejections.append(
                    Rejection(p, doc_id, "duplicate_doc_id", f"doc_id reused across {paths}.")
                )
            continue
        valid[doc_id] = entries[0][1]

    # Pass 3: dangling supersedes (G-08). Re-check against the surviving set.
    for doc_id, meta in list(valid.items()):
        if meta.supersedes is not None and meta.supersedes not in valid:
            path = next(p for p, m in per_doc if m.doc_id == doc_id)
            rejections.append(
                Rejection(
                    path,
                    doc_id,
                    "dangling_supersedes",
                    f"supersedes {meta.supersedes!r} not in corpus.",
                )
            )
            valid.pop(doc_id, None)

    return valid, rejections


def compute_superseded_flags(valid: dict[str, DocumentMetadata]) -> set[str]:
    """Return the set of doc_ids that some OTHER live doc supersedes (G-08).
    These doc_ids carry is_superseded=true on every chunk."""
    superseded: set[str] = set()
    for meta in valid.values():
        if meta.supersedes is not None and meta.supersedes in valid:
            superseded.add(meta.supersedes)
    return superseded
