"""Citation re-validation (contracts.md section 3.6; gap-register G-04).

``validate_citations`` runs AFTER generation, BEFORE the response is serialized.
It is the second, independent enforcement of access on top of the in-query
pre-filter (defense in depth). For each citation the generator emitted:

  (a) the cited doc_id MUST be present in the assembled context's doc_ids, AND
  (b) ``resolve_access(role)`` plus the cited block's stored
      classification/allowed_roles MUST still permit it for the role.

A citation failing EITHER check is STRIPPED. A citation can never reference a
document the role could not retrieve. The function returns the surviving
citations plus the stripped ones so the output guardrail can force the
insufficient-context boundary if stripping leaves any claim uncited.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.models import AssembledContext, Citation
from retrieval.access import build_access_filter, chunk_is_visible, resolve_access


@dataclass(frozen=True)
class CitationValidation:
    valid: list[Citation]
    stripped: list[Citation]


def validate_citations(
    citations: list[Citation],
    role: str,
    assembled_context: AssembledContext,
    *,
    active_strategy: str = "production",
) -> CitationValidation:
    """Strip any citation the role could not retrieve or that is not present in the
    assembled context (G-04). Returns surviving and stripped citations."""
    decision = resolve_access(role)
    access_filter = build_access_filter(decision, active_strategy=active_strategy)

    # doc_id -> the block's access metadata, drawn from the assembled context. The
    # context already passed the pre-filter, but we re-derive the access check from
    # the block's own classification/allowed_roles for true defense in depth.
    context_blocks = {block.doc_id: block for block in assembled_context.blocks}

    valid: list[Citation] = []
    stripped: list[Citation] = []
    for citation in citations:
        doc_id = citation.get("doc_id")
        block = context_blocks.get(doc_id)
        # (a) must be in the assembled context.
        if block is None:
            stripped.append(citation)
            continue
        # (b) must still pass the access filter for this role. Re-check against the
        # block-backed access metadata via the same predicate used at retrieval.
        record = {
            "allowed_roles": getattr(block, "allowed_roles", None)
            or _roles_for(assembled_context, doc_id),
            "classification": getattr(block, "classification", None)
            or _classification_for(assembled_context, doc_id),
            "chunk_strategy": active_strategy,
        }
        if record["allowed_roles"] is None or record["classification"] is None:
            # No access metadata recoverable: fail closed, strip.
            stripped.append(citation)
            continue
        if chunk_is_visible(record, access_filter):
            valid.append(citation)
        else:
            stripped.append(citation)

    return CitationValidation(valid=valid, stripped=stripped)


# ContextBlock (contract 3.5) intentionally does not carry classification/
# allowed_roles. The retrieval layer therefore exposes a side table keyed by
# doc_id so the citation re-validator can re-derive access without trusting the
# generator. assemble_context callers attach it via ``attach_access_metadata``.
_ACCESS_SIDE_TABLE: dict[int, dict[str, dict]] = {}


def attach_access_metadata(assembled_context: AssembledContext, candidates_or_chunks) -> None:
    """Record doc_id -> {classification, allowed_roles} for the blocks in this
    assembled context, sourced from the access-filtered chunks (NOT the generator).
    Keyed by the context object's id so the side table is request-scoped."""
    table: dict[str, dict] = {}
    for item in candidates_or_chunks:
        chunk = getattr(item, "chunk", item)
        table[chunk.doc_id] = {
            "classification": chunk.classification,
            "allowed_roles": list(chunk.allowed_roles),
        }
    _ACCESS_SIDE_TABLE[id(assembled_context)] = table


def _roles_for(ctx: AssembledContext, doc_id: str):
    return _ACCESS_SIDE_TABLE.get(id(ctx), {}).get(doc_id, {}).get("allowed_roles")


def _classification_for(ctx: AssembledContext, doc_id: str):
    return _ACCESS_SIDE_TABLE.get(id(ctx), {}).get(doc_id, {}).get("classification")


__all__ = ["validate_citations", "CitationValidation", "attach_access_metadata"]
