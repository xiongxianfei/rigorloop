#!/usr/bin/env python3
"""Shared semantic checks for RigorLoop change metadata."""

from __future__ import annotations

from typing import Any


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
