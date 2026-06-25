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


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
