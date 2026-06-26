#!/usr/bin/env python3
"""Shared semantic checks for RigorLoop change metadata."""

from __future__ import annotations

import re
from typing import Any


REVIEW_GATE_INDEPENDENCE_LEVELS = {"L1", "L2", "L3"}
REVIEW_GATE_PHASE_RECEIPTS = (
    "risk-map-recorded",
    "evidence-menu-released",
    "evidence-results-released",
    "verdict-recorded",
)
REVIEW_GATE_PHASE_ORDER = (
    "risk-map-recorded",
    "evidence-menu-released",
    "evidence-results-released",
    "prior-findings-released",
    "verdict-recorded",
)
REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS = {"applicable", "not-applicable"}
REQUIREMENT_FIDELITY_PATH_TRIGGERS = {
    "skills/",
    "scripts/*validator*",
    "scripts/validate-*",
    "schemas/",
    "specs/",
    "templates/",
    "docs/workflows.md",
    "docs/changes/**/reviews/",
    "docs/changes/**/review-*.md",
}
REQUIREMENT_FIDELITY_CATEGORY_TRIGGERS = {
    "spec-derived validators",
    "skill instructions derived from specs",
    "review-recording contracts",
    "workflow routing contracts",
    "closed enums",
    "multi-surface public skill guidance",
    "artifact lifecycle validators",
    "metadata validators",
    "generated-output or package parity validators",
    "autoprogression gates",
    "material-finding schemas",
}
REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS = {
    "change unrelated to normative contracts",
    "decomposition already accepted upstream and unchanged",
    "surfaces covered by spec-derived constants exercised in tests",
}
SHA256_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")


def is_declared_clean_receipt_root(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    review = data.get("review")
    if not isinstance(review, dict):
        return False
    return (
        review.get("status") == "clean"
        or ("reviewed_artifact" in review and "review_log" in review)
    )


def validate_clean_receipt_root_review_metadata(
    data: Any,
    *,
    require_clean_receipt_root: bool = False,
) -> list[str]:
    if not isinstance(data, dict):
        return []
    if not require_clean_receipt_root and not is_declared_clean_receipt_root(data):
        return []

    errors: list[str] = []
    review = data.get("review")
    if not isinstance(review, dict):
        return ["review: required for clean receipt roots"]

    status = review.get("status")
    if not isinstance(status, str) or not status.strip():
        errors.append("review.status must identify clean receipt root status")
    elif status != "clean":
        errors.append("review.status must be 'clean' for clean receipt roots")

    reviewed_artifact = review.get("reviewed_artifact")
    if reviewed_artifact is None:
        errors.append("review.reviewed_artifact is required for clean receipt roots")
    elif not isinstance(reviewed_artifact, str):
        errors.append("review.reviewed_artifact: expected string")

    review_log = review.get("review_log")
    if review_log is None:
        errors.append("review.review_log is required for clean receipt roots")
    elif not isinstance(review_log, str):
        errors.append("review.review_log: expected string")

    if review.get("unresolved_items") != 0:
        errors.append("review.unresolved_items must be 0 for clean receipt roots")

    return errors


def validate_review_gate_metadata(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []
    review = data.get("review")
    if not isinstance(review, dict):
        return []
    gate = review.get("review_gate")
    if gate is None:
        return []
    if not isinstance(gate, dict):
        return ["review.review_gate: expected object"]

    errors: list[str] = []
    for field in ("manifest", "independence_level", "initial_packet_sha256", "phase_receipts"):
        if field not in gate:
            errors.append(f"review.review_gate.{field}: missing required field")

    manifest = gate.get("manifest")
    if "manifest" in gate and not _nonempty_string(manifest):
        errors.append("review.review_gate.manifest: expected string")

    independence = gate.get("independence_level")
    if "independence_level" in gate:
        if independence == "L0":
            errors.append("review.review_gate.independence_level: L0 is not valid for automated handoff")
        elif independence not in REVIEW_GATE_INDEPENDENCE_LEVELS:
            errors.append("review.review_gate.independence_level: expected one of L1, L2, L3")

    packet_hash = gate.get("initial_packet_sha256")
    if "initial_packet_sha256" in gate and (
        not isinstance(packet_hash, str) or SHA256_RE.fullmatch(packet_hash) is None
    ):
        errors.append("review.review_gate.initial_packet_sha256: expected sha256:<64 hex>")

    receipts = gate.get("phase_receipts")
    if "phase_receipts" in gate:
        if not isinstance(receipts, list) or not all(isinstance(item, str) for item in receipts):
            errors.append("review.review_gate.phase_receipts: expected list of strings")
        else:
            for receipt in REVIEW_GATE_PHASE_RECEIPTS:
                if receipt not in receipts:
                    errors.append(f"review.review_gate.phase_receipts: missing {receipt}")
            for earlier, later in zip(REVIEW_GATE_PHASE_ORDER, REVIEW_GATE_PHASE_ORDER[1:]):
                if earlier in receipts and later in receipts and receipts.index(later) < receipts.index(earlier):
                    errors.append(f"review.review_gate.phase_receipts: {later} appears before {earlier}")
            if len(set(receipts)) != len(receipts):
                errors.append("review.review_gate.phase_receipts: duplicate phase receipt")

    return errors


def validate_requirement_fidelity_metadata(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []
    review = data.get("review")
    if not isinstance(review, dict):
        return []
    fidelity = review.get("requirement_fidelity")
    if fidelity is None:
        return []
    if not isinstance(fidelity, dict):
        return ["review.requirement_fidelity: expected object"]

    errors: list[str] = []
    applicability = fidelity.get("applicability")
    if applicability not in REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS:
        errors.append("review.requirement_fidelity.applicability: expected one of applicable, not-applicable")

    _validate_string_list_closed(
        fidelity.get("matched_path_triggers"),
        "review.requirement_fidelity.matched_path_triggers",
        REQUIREMENT_FIDELITY_PATH_TRIGGERS | {"none"},
        errors,
    )
    _validate_string_list_closed(
        fidelity.get("matched_category_triggers"),
        "review.requirement_fidelity.matched_category_triggers",
        REQUIREMENT_FIDELITY_CATEGORY_TRIGGERS | {"none"},
        errors,
    )

    review_stage = fidelity.get("review_stage")
    if not _nonempty_string(review_stage):
        errors.append("review.requirement_fidelity.review_stage: expected string")

    if applicability == "applicable":
        if fidelity.get("receipt_valid") is not True:
            errors.append("review.requirement_fidelity.receipt_valid: expected true when applicability is applicable")
    if applicability == "not-applicable":
        reason = fidelity.get("not_applicable_reason")
        if reason not in REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS:
            errors.append("review.requirement_fidelity.not_applicable_reason: expected closed reason")

    return errors


def _validate_string_list_closed(value: Any, path: str, allowed: set[str], errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: expected non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{path}[{index}]: expected string")
            continue
        if item not in allowed:
            kind = "path trigger" if "path" in path else "category trigger"
            errors.append(f"{path}[{index}]: unknown {kind} {item}")


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
