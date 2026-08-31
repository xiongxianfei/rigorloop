#!/usr/bin/env python3
"""Executable lifecycle contracts for top-level workflow artifacts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


LIFECYCLE_CONTRACT_V1 = "stage-owned-change-local-v1"
LIFECYCLE_CONTRACT_V2 = "stage-owned-change-local-v2"
LEGACY_UNVERSIONED_CONTRACT = "legacy-unversioned"
LIFECYCLE_ACTIVATION_MANIFEST_PATH = Path("specs/lifecycle-contract-activation.yaml")
LIFECYCLE_ACTIVATION_SCHEMA_PATH = Path("schemas/lifecycle-contract-activation.schema.json")
LIFECYCLE_CONTRACT_VALUES = frozenset({LIFECYCLE_CONTRACT_V1, LIFECYCLE_CONTRACT_V2})
PRIOR_CONTRACT_CLASSES = frozenset({LIFECYCLE_CONTRACT_V1, LEGACY_UNVERSIONED_CONTRACT})
ACTIVATION_STATES = frozenset({"preactivation", "active"})
WORKFLOW_LIFECYCLE_STATES = frozenset({"active", "paused", "completed", "cancelled"})
POST_DELIVERY_STAGES = frozenset(
    {"implement", "code-review", "review-resolution", "ci-maintenance", "explain-change", "verify", "pr"}
)
WORKFLOW_STAGES = frozenset(
    {
        "proposal", "proposal-review", "architecture", "architecture-review",
        "spec", "spec-review", "design-review", "plan", "plan-review",
        "test-spec", "test-spec-review", "delivery-review", *POST_DELIVERY_STAGES,
    }
)
_MANIFEST_FIELDS = frozenset({"schema_version", "state", "activating_source_revision", "changes"})
_MANIFEST_ENTRY_FIELDS = frozenset({"change_id", "contract_class"})
_SAFE_CHANGE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def parse_lifecycle_activation_manifest(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"activation manifest is not valid JSON-compatible YAML: {exc.msg}") from exc


def validate_lifecycle_activation_manifest(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict) or set(manifest) != _MANIFEST_FIELDS:
        return ["activation manifest must contain exactly schema_version, state, activating_source_revision, and changes"]
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append(f"activation manifest schema_version: unknown_value {manifest.get('schema_version')}")
    state = manifest.get("state")
    if state not in ACTIVATION_STATES:
        errors.append(f"activation manifest state: unknown_value {state}")
    changes = manifest.get("changes")
    if not isinstance(changes, list):
        return [*errors, "activation manifest changes must be an array"]

    for index, entry in enumerate(changes):
        if not isinstance(entry, dict) or set(entry) != _MANIFEST_ENTRY_FIELDS:
            errors.append(f"activation manifest changes[{index}] must contain exactly change_id and contract_class")
            continue
        if entry.get("contract_class") not in PRIOR_CONTRACT_CLASSES:
            errors.append(f"activation manifest changes[{index}].contract_class: unknown_value {entry.get('contract_class')}")
    if errors:
        return errors

    revision = manifest.get("activating_source_revision")
    if state == "preactivation":
        if revision is not None:
            errors.append("preactivation manifest activating_source_revision must be null")
        if changes:
            errors.append("preactivation manifest changes must be empty")
    elif not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        errors.append("active manifest activating_source_revision must be a 40-character lowercase Git revision")

    ids: list[str] = []
    for index, entry in enumerate(changes):
        change_id = entry.get("change_id")
        if not isinstance(change_id, str) or _SAFE_CHANGE_ID.fullmatch(change_id) is None:
            errors.append(f"activation manifest changes[{index}].change_id must be one safe identifier")
        else:
            ids.append(change_id)
    if len(set(ids)) != len(ids):
        errors.append("activation manifest changes contain a duplicate change_id")
    if any(left.encode("utf-8") >= right.encode("utf-8") for left, right in zip(ids, ids[1:])):
        errors.append("activation manifest changes must use strict raw UTF-8 byte order")
    return errors


def validate_lifecycle_activation_prerequisites(
    manifest: Any,
    changes_by_id: dict[str, Any],
) -> list[str]:
    """Validate the frozen prior-change inventory before v2 activation."""

    manifest_errors = validate_lifecycle_activation_manifest(manifest)
    if manifest_errors:
        return manifest_errors
    if not isinstance(changes_by_id, dict):
        return ["activation prerequisite change inventory must be a mapping"]

    blocking_ids: list[str] = []
    for entry in manifest["changes"]:
        change_id = entry["change_id"]
        change = changes_by_id.get(change_id)
        if not isinstance(change, dict):
            blocking_ids.append(change_id)
            continue
        recorded_class = change.get("lifecycle_contract", LEGACY_UNVERSIONED_CONTRACT)
        if recorded_class not in LIFECYCLE_CONTRACT_VALUES | {LEGACY_UNVERSIONED_CONTRACT}:
            return [f"prior-contract change {change_id} lifecycle_contract: unknown_value {recorded_class}"]
        if recorded_class != entry["contract_class"]:
            return [
                f"prior-contract change {change_id} does not match activation manifest class {entry['contract_class']}"
            ]

        workflow_state = change.get("workflow_state")
        if not isinstance(workflow_state, dict):
            blocking_ids.append(change_id)
            continue
        lifecycle_state = workflow_state.get("lifecycle_state")
        if lifecycle_state not in WORKFLOW_LIFECYCLE_STATES:
            return [
                f"prior-contract change {change_id} lifecycle_state: unknown_value {lifecycle_state}"
            ]
        if lifecycle_state in {"completed", "cancelled"}:
            continue

        current_stage = workflow_state.get("current_stage")
        if current_stage not in WORKFLOW_STAGES:
            return [
                f"prior-contract change {change_id} current_stage: unknown_value {current_stage}"
            ]
        if current_stage not in POST_DELIVERY_STAGES:
            blocking_ids.append(change_id)
            continue
        review_packages = change.get("review_packages")
        delivery = review_packages.get("delivery") if isinstance(review_packages, dict) else None
        members = delivery.get("members") if isinstance(delivery, dict) else None
        if not (
            isinstance(delivery, dict)
            and delivery.get("status") == "approved"
            and delivery.get("authority") == "granted"
            and isinstance(members, dict)
            and any(isinstance(path, str) and path.startswith("docs/plans/") for path in members.values())
            and any(isinstance(path, str) and path.startswith("specs/") and path.endswith(".test.md") for path in members.values())
        ):
            blocking_ids.append(change_id)

    if blocking_ids:
        return [
            "activation prerequisite blocked by prior-contract changes: "
            + ", ".join(sorted(blocking_ids, key=lambda item: item.encode("utf-8")))
        ]
    return []


def _has_active_test_spec_state(change: dict[str, Any]) -> bool:
    workflow_state = change.get("workflow_state")
    if isinstance(workflow_state, dict) and (
        workflow_state.get("current_stage") in {"test-spec", "test-spec-review"}
        or workflow_state.get("next_stage") in {"test-spec", "test-spec-review"}
    ):
        return True
    states = change.get("artifact_states")
    if isinstance(states, dict):
        for entry in states.values():
            if isinstance(entry, dict) and entry.get("kind") == "test-spec" and entry.get("lifecycle_state") not in {"abandoned", "archived", "superseded"}:
                return True
    packages = change.get("review_packages")
    delivery = packages.get("delivery") if isinstance(packages, dict) else None
    members = delivery.get("members") if isinstance(delivery, dict) else None
    if isinstance(members, dict) and "test-spec" in members:
        return True
    coordination = change.get("lifecycle_cli")
    if not isinstance(coordination, dict):
        return False
    artifacts = coordination.get("artifacts")
    if isinstance(artifacts, dict) and any(
        isinstance(entry, dict) and entry.get("artifact_kind") == "test-spec"
        for entry in artifacts.values()
    ):
        return True
    reviews = coordination.get("reviews")
    if isinstance(reviews, dict) and any(
        isinstance(entry, dict) and entry.get("stage_authority") == "test-spec-review"
        for entry in reviews.values()
    ):
        return True
    package_reviews = coordination.get("package_reviews")
    delivery_review = package_reviews.get("delivery") if isinstance(package_reviews, dict) else None
    review_members = delivery_review.get("members") if isinstance(delivery_review, dict) else None
    return isinstance(review_members, dict) and "test-spec" in review_members


def classify_lifecycle_contract(change_id: str, change: dict[str, Any], manifest: Any) -> dict[str, str]:
    has_explicit_contract = "lifecycle_contract" in change
    explicit = change.get("lifecycle_contract")
    if has_explicit_contract and explicit not in LIFECYCLE_CONTRACT_VALUES:
        rendered = "null" if explicit is None else str(explicit)
        raise ValueError(f"lifecycle_contract: unknown_value {rendered}")
    manifest_errors = validate_lifecycle_activation_manifest(manifest)
    if manifest_errors:
        raise ValueError(manifest_errors[0])
    contract_class = explicit if has_explicit_contract else LEGACY_UNVERSIONED_CONTRACT
    if contract_class == LIFECYCLE_CONTRACT_V2:
        if _has_active_test_spec_state(change):
            raise ValueError("v2 lifecycle contract carries active test-spec state")
        return {
            "contract_class": contract_class,
            "activation_state": manifest["state"],
            "authority": "active" if manifest["state"] == "active" else "inactive",
        }
    if manifest["state"] == "active":
        entry = next((item for item in manifest["changes"] if item["change_id"] == change_id), None)
        if entry is None:
            raise ValueError(f"prior-contract change {change_id} is not present in the activation manifest")
        if entry["contract_class"] != contract_class:
            raise ValueError(f"prior-contract change {change_id} does not match activation manifest class {entry['contract_class']}")
    return {
        "contract_class": contract_class,
        "activation_state": manifest["state"],
        "authority": "prior-compatible" if manifest["state"] == "active" else "preactivation",
    }


PROPOSAL_ID_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ADR_ID_PATTERN = re.compile(r"^ADR-\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_CONTRACT_HEADINGS = (
    "## Status",
    "## Goal and context",
    "## Requirements",
    "## Acceptance criteria",
)
SIMPLIFIED_PROPOSAL_REQUIRED_SECTIONS = (
    "Challenge",
    "Goals",
    "Scope and non-goals",
    "Governing principle",
    "Proposed direction",
    "Feasibility",
    "Decision requested",
)
SIMPLIFIED_PROPOSAL_OPTIONAL_SECTION = "Impact and major trade-offs"
SIMPLIFIED_PROPOSAL_FORBIDDEN_SECTIONS = frozenset(
    {"Status", "Owning change record", "Vision fit"}
)
SIMPLIFIED_PROPOSAL_CUTOVER_DATE = "2026-08-30"


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
    required_sections=(
        "Related artifacts",
        "Introduction and Goals",
        "Architecture Constraints",
        "Context and Scope",
        "Solution Strategy",
        "Building Block View",
        "Runtime View",
        "Deployment View",
        "Crosscutting Concepts",
        "Architecture Decisions",
        "Quality Requirements",
        "Risks and Technical Debt",
        "Glossary",
        "Next artifacts",
        "Follow-on artifacts",
        "Readiness",
    ),
)

CANONICAL_ARCHITECTURE_CONTRACT = ArtifactContract(
    class_name="architecture",
    allowed_statuses=ARCHITECTURE_CONTRACT.allowed_statuses,
    settlement_statuses=ARCHITECTURE_CONTRACT.settlement_statuses,
    terminal_statuses=ARCHITECTURE_CONTRACT.terminal_statuses,
    # First-slice compatibility is lifecycle-only; package-shape checks remain review-based.
    required_sections=(),
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


def _has_markdown_heading(text: str, heading: str) -> bool:
    pattern = re.compile(rf"^{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    return pattern.search(text) is not None


def _is_lifecycle_managed_spec(text: str) -> bool:
    matches = sum(1 for heading in SPEC_CONTRACT_HEADINGS if _has_markdown_heading(text, heading))
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
    if path_text == "docs/architecture/system/architecture.md":
        return CANONICAL_ARCHITECTURE_CONTRACT
    if path_text.startswith("docs/architecture/") and name.endswith(".md"):
        return ARCHITECTURE_CONTRACT
    if path_text.startswith("docs/adr/") and name.endswith(".md"):
        return ADR_CONTRACT
    return None
