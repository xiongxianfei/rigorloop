"""Spec-cited phrase sets for review-independence skill guidance tests."""

from __future__ import annotations


# Source: specs/review-independence-and-criticality.md R5 plus M3 auto-fix budget handoff guidance.
R5_FORBIDDEN_INITIAL_PACKET_ITEMS = (
    "author hidden reasoning",
    "author chain-of-thought",
    "author self-assessment",
    "claims that the change is correct",
    "desired review outcome",
    "autoprogression round budget",
    "message that approval is needed to continue",
    "auto-fix budget",
    "auto-fix eligibility",
    "implementation-stage safety narrative",
    "prior reviewer conclusion",
    "prior finding content",
    "validation-result summaries",
    "evidence menu",
)


# Source: specs/review-independence-and-criticality.md R8c.
R8D_RECONCILIATION_CATEGORIES = (
    "resolved",
    "still-present",
    "failed-remediation",
    "reopened",
    "superseded",
    "new-finding",
)


# Source: specs/review-independence-and-criticality.md R8d.
R8D_FAILED_REMEDIATION_REQUIRED_PHRASES = (
    "failed-remediation",
    "claimed or expected to be fixed",
    "independently rediscovered during the blind-first pass",
)
