#!/usr/bin/env python3
"""Executable lifecycle contracts for top-level workflow artifacts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


PROPOSAL_ID_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ADR_ID_PATTERN = re.compile(r"^ADR-\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_CONTRACT_HEADINGS = (
    "## Status",
    "## Goal and context",
    "## Requirements",
    "## Acceptance criteria",
)


@dataclass(frozen=True)
class ArtifactContract:
    class_name: str
    allowed_statuses: frozenset[str]
    settlement_statuses: frozenset[str]
    terminal_statuses: frozenset[str]
    required_sections: tuple[str, ...]
    identifier_pattern: re.Pattern[str] | None = None
    identifier_label: str | None = None


PROPOSAL_CONTRACT = ArtifactContract(
    class_name="proposal",
    allowed_statuses=frozenset(
        {"draft", "under review", "accepted", "rejected", "abandoned", "superseded", "archived"}
    ),
    settlement_statuses=frozenset({"accepted"}),
    terminal_statuses=frozenset({"rejected", "abandoned", "superseded", "archived"}),
    required_sections=("Problem", "Goals", "Non-goals", "Recommended direction"),
    identifier_pattern=PROPOSAL_ID_PATTERN,
    identifier_label="proposal identifier",
)

SPEC_CONTRACT = ArtifactContract(
    class_name="spec",
    allowed_statuses=frozenset({"draft", "approved", "abandoned", "superseded", "archived"}),
    settlement_statuses=frozenset({"approved"}),
    terminal_statuses=frozenset({"abandoned", "superseded", "archived"}),
    required_sections=("Goal and context", "Requirements", "Acceptance criteria"),
    identifier_pattern=SPEC_ID_PATTERN,
    identifier_label="top-level spec identifier",
)

TEST_SPEC_CONTRACT = ArtifactContract(
    class_name="test-spec",
    allowed_statuses=frozenset({"draft", "active", "abandoned", "superseded", "archived"}),
    settlement_statuses=frozenset({"active"}),
    terminal_statuses=frozenset({"abandoned", "superseded", "archived"}),
    required_sections=("Related spec and plan", "Testing strategy", "Requirement coverage map", "Test cases"),
)

ARCHITECTURE_CONTRACT = ArtifactContract(
    class_name="architecture",
    allowed_statuses=frozenset({"draft", "approved", "abandoned", "superseded", "archived"}),
    settlement_statuses=frozenset({"approved"}),
    terminal_statuses=frozenset({"abandoned", "superseded", "archived"}),
    required_sections=("Related artifacts", "Summary", "Requirements covered", "Proposed architecture", "Interfaces and contracts"),
)

ADR_CONTRACT = ArtifactContract(
    class_name="adr",
    allowed_statuses=frozenset(
        {"draft", "proposed", "accepted", "active", "deprecated", "superseded", "archived", "abandoned"}
    ),
    settlement_statuses=frozenset({"accepted", "active"}),
    terminal_statuses=frozenset({"deprecated", "superseded", "archived", "abandoned"}),
    required_sections=("Context", "Decision", "Alternatives considered", "Consequences"),
    identifier_pattern=ADR_ID_PATTERN,
    identifier_label="ADR identifier",
)


def _is_lifecycle_managed_spec(text: str) -> bool:
    matches = sum(1 for heading in SPEC_CONTRACT_HEADINGS if heading in text)
    return matches >= 2


def classify_artifact(relative_path: Path, text: str | None = None) -> ArtifactContract | None:
    path_text = relative_path.as_posix()
    name = relative_path.name

    if path_text.startswith("docs/proposals/") and name.endswith(".md"):
        return PROPOSAL_CONTRACT
    if path_text.startswith("specs/") and name.endswith(".test.md") and name != "feature-template.test.md":
        return TEST_SPEC_CONTRACT
    if path_text.startswith("specs/") and name.endswith(".md") and name not in {
        "feature-template.md",
        "feature-template.test.md",
    } and not name.endswith(".test.md"):
        if text is None:
            return None
        if _is_lifecycle_managed_spec(text):
            return SPEC_CONTRACT
        return None
    if path_text.startswith("docs/architecture/") and name.endswith(".md"):
        return ARCHITECTURE_CONTRACT
    if path_text.startswith("docs/adr/") and name.endswith(".md"):
        return ADR_CONTRACT
    return None
