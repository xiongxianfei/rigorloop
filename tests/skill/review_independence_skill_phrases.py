"""Structural phrases for the retained optional automated-review method.

Current consumers are Code Review's workflow-managed-automated-review reference
and Implement's automated-review-correction reference. These immutable inputs
protect instruction presence; they do not prove reviewer independence at runtime.
Historical R5/R8 names remain to preserve the existing test interface.
"""

from __future__ import annotations


# Neutral initial-packet exclusions in both current consumer references.
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


# Prior-finding reconciliation categories in the Code Review reference.
R8D_RECONCILIATION_CATEGORIES = (
    "resolved",
    "still-present",
    "failed-remediation",
    "reopened",
    "superseded",
    "new-finding",
)


# Failed-remediation meaning in that same retained method.
R8D_FAILED_REMEDIATION_REQUIRED_PHRASES = (
    "failed-remediation",
    "claimed or expected to be fixed",
    "independently rediscovered during the blind-first pass",
)
