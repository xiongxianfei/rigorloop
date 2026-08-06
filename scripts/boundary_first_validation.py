#!/usr/bin/env python3
"""Deterministic boundary-first record and activation validation."""

from __future__ import annotations

import getpass
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from boundary_first_reference import (
    CANONICAL_REFERENCE,
    GOVERNED_SKILLS,
    METHOD_VERSION,
    RESOURCE_MANIFEST,
    ProjectionContractError,
    project_reference,
)
from adapter_distribution import (
    AdapterArtifactEntry,
    adapter_archive_name,
    parse_adapter_artifact_metadata_yaml,
    parse_manifest_yaml,
)
from artifact_lifecycle_validation import _parse_change_yaml_text


ACTIVATION_RECORD = Path("specs/boundary-first-activation.yaml")
PROOF_MODEL_SPEC = Path("specs/boundary-first-proof-model.md")
ACTIVATION_CANDIDATE_RELEASE = "v0.4.0"
ACTIVATION_CANDIDATE_ROLLBACK = "v0.3.6"
ACTIVATION_CHANGE_ROOT = Path(
    "docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7"
)
ACTIVATION_STATES = frozenset({"pending", "active"})
CORE_DIMENSIONS = (
    "input-domain",
    "state-lifecycle",
    "identity-authority",
    "composition-path",
    "temporal-retry",
    "failure-recovery",
    "compatibility-migration",
    "external-environment",
)
DIMENSION_PREFIXES = {
    "input-domain": "BND-INPUT-",
    "state-lifecycle": "BND-STATE-",
    "identity-authority": "BND-AUTH-",
    "composition-path": "BND-COMPOSE-",
    "temporal-retry": "BND-TEMPORAL-",
    "failure-recovery": "BND-RECOVERY-",
    "compatibility-migration": "BND-COMPAT-",
    "external-environment": "BND-ENV-",
}
APPLICABILITY_VALUES = frozenset({"applicable", "not-applicable"})
COVERAGE_STATES = frozenset({"covered", "gap"})
PROOF_LEVELS = frozenset(
    {"unit", "integration", "contract", "end-to-end", "smoke", "manual"}
)
AUTOMATION_MODES = frozenset({"automated", "manual", "hybrid"})
EXAMPLE_CLASSES = frozenset({"illustration", "regression", "discovery"})
BOUNDARY_ID_RE = re.compile(
    r"^BND-(INPUT|STATE|AUTH|COMPOSE|TEMPORAL|RECOVERY|COMPAT|ENV)-[0-9]{3}$"
)
INTERACTION_ID_RE = re.compile(r"^INT-[0-9]{3}$")
PROOF_ID_RE = re.compile(r"^PRF-[0-9]{3}$")
STABLE_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FEATURE_HEADINGS = (
    "Boundary model",
    "Boundary definitions",
    "Selected interactions",
    "Example ownership",
)
BOUNDARY_MODEL_COLUMNS = (
    "Dimension ID",
    "Applicability",
    "Governing requirement IDs",
    "Boundary IDs",
    "Non-applicability rationale",
)
BOUNDARY_DEFINITION_COLUMNS = (
    "Boundary ID",
    "Dimension ID",
    "Governing requirement IDs",
    "Partitions or transitions",
    "Invariants",
    "Outcomes",
    "Owner requirement ID",
)
INTERACTION_COLUMNS = (
    "Interaction ID",
    "Governing requirement IDs",
    "Boundary IDs",
    "Hazard",
    "Required composed outcome",
)
EXAMPLE_COLUMNS = (
    "Example ID",
    "Classification",
    "Governing requirement IDs",
    "Boundary IDs",
    "Regression ID",
    "Discovery gap ID",
)
PROOF_COLUMNS = (
    "Proof obligation ID",
    "Coverage state",
    "Governing requirement IDs",
    "Boundary or interaction IDs",
    "Test case IDs",
    "Proof level",
    "Automation mode",
    "Command IDs",
    "Evidence artifact",
    "Required milestone",
    "Manual procedure IDs",
    "Uncovered gap ID",
)
ACTIVATION_FIELDS = frozenset(
    {
        "contract_version",
        "state",
        "activating_release",
        "rollback_release",
        "canonical_reference",
        "canonical_reference_sha256",
        "resource_manifest",
        "resource_manifest_sha256",
        "grandfathering_baseline_revision",
        "grandfathered_specs",
        "governed_skills",
        "projection_sha256",
    }
)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    offending_value: str
    expected: str

    def as_dict(self) -> dict[str, str]:
        return {
            "check_id": self.code,
            "path": self.path,
            "message": self.message,
            "offending_value": _redacted_value(self.offending_value),
            "expected": self.expected,
        }


@dataclass(frozen=True)
class RollbackArtifactIdentity:
    adapter: str
    archive: str
    sha256: str


@dataclass(frozen=True)
class RollbackSelection:
    release: str
    artifacts: tuple[RollbackArtifactIdentity, ...]


@dataclass(frozen=True)
class ActivationCandidateResult:
    candidate_release: str
    publication_base: str
    grandfathering_baseline: str
    transition_commit: str
    candidate_validation_head: str
    rollback_release: str
    tag_state: str
    bundle_identity: tuple[tuple[str, str], ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "status": "passed",
            "mode": "activation-candidate",
            "publication_state": "candidate-ready-unpublished",
            "candidate_release": self.candidate_release,
            "publication_base": self.publication_base,
            "grandfathering_baseline": self.grandfathering_baseline,
            "transition_commit": self.transition_commit,
            "candidate_validation_head": self.candidate_validation_head,
            "rollback_release": self.rollback_release,
            "tag_state": self.tag_state,
            "bundle_identity": dict(self.bundle_identity),
        }


def _issue(
    code: str,
    path: str,
    message: str,
    value: object = "-",
    expected: object = "-",
) -> ValidationIssue:
    return ValidationIssue(code, path, message, str(value), str(expected))


def _redacted_value(value: str) -> str:
    encoded = value.encode("utf-8")
    return (
        "redacted:sha256:"
        + hashlib.sha256(encoded).hexdigest()
        + f":bytes={len(encoded)}"
    )


def _live_markdown(text: str) -> str:
    """Preserve line positions while removing fenced-code content."""

    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(?:[^`]*)$", line)
        if fence_character is None:
            if match:
                token = match.group(1)
                fence_character = token[0]
                fence_length = len(token)
                output.append("")
            else:
                output.append(line)
            continue
        close = re.match(
            rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}\s*$",
            line,
        )
        output.append("")
        if close:
            fence_character = None
            fence_length = 0
    return "\n".join(output)


def _split_ids(value: str) -> tuple[str, ...]:
    if value == "-":
        return ()
    return tuple(value.split(", "))


def _heading_positions(text: str) -> dict[str, int]:
    positions: dict[str, int] = {}
    for index, line in enumerate(text.splitlines()):
        if line.startswith("## "):
            positions.setdefault(line[3:].strip(), index)
    return positions


def _level_two_headings(text: str) -> tuple[str, ...]:
    return tuple(
        line[3:].strip()
        for line in text.splitlines()
        if line.startswith("## ")
    )


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def _table(section: str) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return (), ()

    def cells(line: str) -> tuple[str, ...]:
        return tuple(cell.strip() for cell in line.strip("|").split("|"))

    header = cells(lines[0])
    rows = tuple(cells(line) for line in lines[2:])
    return header, rows


def _table_separator_issue(
    section: str,
    *,
    path: str,
    surface: str,
    expected_width: int,
) -> ValidationIssue | None:
    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip().startswith("|")
    ]
    if len(lines) < 2:
        return None
    separator = tuple(cell.strip() for cell in lines[1].strip("|").split("|"))
    valid_cells = len(separator) == expected_width and all(
        re.fullmatch(r":?-{3,}:?", cell) for cell in separator
    )
    if not valid_cells:
        return _issue(
            "BFR-INVALID-TABLE-SEPARATOR",
            path,
            f"{surface} table separator is not exact",
            separator,
            f"{expected_width} cells matching ^:?-{{3,}}:?$",
        )
    return None


def _line_value(text: str, label: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(label)}:\s*(\S(?:.*\S)?)\s*$", text)
    return match.group(1) if match else None


def _marker_issues(text: str, path: str) -> list[ValidationIssue]:
    marker_pattern = re.compile(r"(?m)^boundary_contract:\s*(\S+)\s*$")
    markers = tuple(marker_pattern.finditer(text))
    if len(markers) != 1:
        return [
            _issue(
                "BFR-MARKER-COUNT",
                path,
                "adopting feature spec requires exactly one boundary contract marker",
                len(markers),
                1,
            )
        ]
    status = _section(text, "Status")
    status_markers = tuple(marker_pattern.finditer(status))
    if len(status_markers) != 1:
        return [
            _issue(
                "BFR-MARKER-PLACEMENT",
                path,
                "boundary contract marker must be inside the Status section",
                "outside-status",
                "after lifecycle status value",
            )
        ]
    marker_line = status[: status_markers[0].start()].splitlines()
    lifecycle_lines = [
        line.strip()
        for line in marker_line
        if line.strip() and not line.lstrip().startswith("<!--")
    ]
    if not lifecycle_lines:
        return [
            _issue(
                "BFR-MARKER-PLACEMENT",
                path,
                "boundary contract marker must follow the lifecycle status value",
                "before-status",
                "after lifecycle status value",
            )
        ]
    return []


def _id_list_vocabulary_issues(
    value: str,
    *,
    path: str,
    code: str,
) -> list[ValidationIssue]:
    if value == "-":
        return []
    if ", " not in value and "," in value:
        return [_issue(code, path, "ID lists require comma-space serialization", value, "ID, ID")]
    ids = _split_ids(value)
    if len(ids) != len(set(ids)) or any(not STABLE_ID_RE.fullmatch(item) for item in ids):
        return [_issue(code, path, "ID list is not unique stable IDs", value, "unique stable IDs")]
    return []


def _sentinel_issues(
    rows: tuple[tuple[str, ...], ...],
    *,
    path: str,
    surface: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for row_index, row in enumerate(rows, start=1):
        for column_index, value in enumerate(row, start=1):
            if value == "" or value in {"—", "–", "−"}:
                issues.append(
                    _issue(
                        "BFR-INVALID-SENTINEL",
                        path,
                        f"{surface} row {row_index} column {column_index} requires ASCII '-' for no value",
                        value or "<blank>",
                        "-",
                    )
                )
    return issues


def validate_feature_record(
    text: str,
    path: str = "<feature-record>",
) -> tuple[ValidationIssue, ...]:
    text = _live_markdown(text)
    vocabulary: list[ValidationIssue] = []
    marker_structure = _marker_issues(text, path)
    if marker_structure:
        return tuple(marker_structure)
    marker = _line_value(text, "boundary_contract")
    if marker is not None and marker != METHOD_VERSION:
        vocabulary.append(
            _issue("BFR-UNKNOWN-CONTRACT-VERSION", path, "unknown boundary contract", marker, METHOD_VERSION)
        )

    positions = _heading_positions(text)
    level_two_headings = _level_two_headings(text)
    forbidden_headings = tuple(
        heading
        for heading in level_two_headings
        if heading in {"Boundary extensions", "Boundary imports"}
    )
    if forbidden_headings or re.search(
        r"(?im)^(?:Boundary extensions|Boundary imports|Extensions|Imports):",
        text,
    ):
        vocabulary.append(
            _issue(
                "BFR-FORBIDDEN-EXTENSION-IMPORT",
                path,
                "boundary-first-v1 forbids extension dimensions and imported boundary records",
                ", ".join(forbidden_headings) or "extension/import declaration",
                "feature-local core dimensions",
            )
        )
    heading_indexes = [positions.get(heading) for heading in FEATURE_HEADINGS]
    if any(index is None for index in heading_indexes):
        return (
            _issue(
                "BFR-MISSING-HEADING",
                path,
                "feature boundary record requires all four exact headings",
                ",".join(sorted(positions)),
                ", ".join(FEATURE_HEADINGS),
            ),
        )
    if heading_indexes != sorted(heading_indexes):  # type: ignore[arg-type]
        return (
            _issue("BFR-HEADING-ORDER", path, "boundary headings are out of order", heading_indexes, FEATURE_HEADINGS),
        )
    first_heading = level_two_headings.index(FEATURE_HEADINGS[0])
    if level_two_headings[first_heading : first_heading + len(FEATURE_HEADINGS)] != FEATURE_HEADINGS:
        vocabulary.append(
            _issue(
                "BFR-NONCONTIGUOUS-RECORD",
                path,
                "boundary record headings must be contiguous and in exact order",
                level_two_headings[first_heading : first_heading + len(FEATURE_HEADINGS)],
                FEATURE_HEADINGS,
            )
        )

    model = _section(text, "Boundary model")
    version = _line_value(model, "Boundary model version")
    if version != METHOD_VERSION:
        vocabulary.append(
            _issue("BFR-UNKNOWN-MODEL-VERSION", path, "unknown boundary model version", version, METHOD_VERSION)
        )
    scope_value = _line_value(model, "Boundary model scope") or "-"
    vocabulary.extend(_id_list_vocabulary_issues(scope_value, path=path, code="BFR-INVALID-SCOPE-ID"))

    model_header, model_rows = _table(model)
    definition_header, definition_rows = _table(_section(text, "Boundary definitions"))
    interaction_section = _section(text, "Selected interactions")
    interaction_header, interaction_rows = _table(interaction_section)
    example_header, example_rows = _table(_section(text, "Example ownership"))
    for rows, surface in (
        (model_rows, "Boundary model"),
        (definition_rows, "Boundary definitions"),
        (interaction_rows, "Selected interactions"),
        (example_rows, "Example ownership"),
    ):
        vocabulary.extend(_sentinel_issues(rows, path=path, surface=surface))
    for actual, expected, surface in (
        (model_header, BOUNDARY_MODEL_COLUMNS, "Boundary model"),
        (definition_header, BOUNDARY_DEFINITION_COLUMNS, "Boundary definitions"),
        (example_header, EXAMPLE_COLUMNS, "Example ownership"),
    ):
        if actual != expected:
            vocabulary.append(
                _issue("BFR-UNKNOWN-COLUMNS", path, f"{surface} columns are not closed", actual, expected)
            )
    for section, surface, width in (
        (model, "Boundary model", len(BOUNDARY_MODEL_COLUMNS)),
        (_section(text, "Boundary definitions"), "Boundary definitions", len(BOUNDARY_DEFINITION_COLUMNS)),
        (_section(text, "Example ownership"), "Example ownership", len(EXAMPLE_COLUMNS)),
    ):
        separator_issue = _table_separator_issue(
            section,
            path=path,
            surface=surface,
            expected_width=width,
        )
        if separator_issue:
            vocabulary.append(separator_issue)
    if interaction_header and interaction_header != INTERACTION_COLUMNS:
        vocabulary.append(
            _issue("BFR-UNKNOWN-COLUMNS", path, "Selected interactions columns are not closed", interaction_header, INTERACTION_COLUMNS)
        )
    if interaction_header:
        separator_issue = _table_separator_issue(
            interaction_section,
            path=path,
            surface="Selected interactions",
            expected_width=len(INTERACTION_COLUMNS),
        )
        if separator_issue:
            vocabulary.append(separator_issue)

    for row in model_rows:
        if len(row) != len(BOUNDARY_MODEL_COLUMNS):
            vocabulary.append(_issue("BFR-ROW-SHAPE", path, "boundary model row has wrong width", len(row), len(BOUNDARY_MODEL_COLUMNS)))
            continue
        dimension, applicability, requirements, boundaries, _rationale = row
        if dimension not in CORE_DIMENSIONS:
            vocabulary.append(
                _issue("BFR-UNKNOWN-DIMENSION", path, "unknown core dimension", dimension, ", ".join(CORE_DIMENSIONS))
            )
        if applicability not in APPLICABILITY_VALUES:
            vocabulary.append(
                _issue("BFR-UNKNOWN-APPLICABILITY", path, "unknown applicability", applicability, "applicable, not-applicable")
            )
        vocabulary.extend(_id_list_vocabulary_issues(requirements, path=path, code="BFR-INVALID-REQUIREMENT-ID"))
        for boundary_id in _split_ids(boundaries):
            if not BOUNDARY_ID_RE.fullmatch(boundary_id):
                vocabulary.append(
                    _issue("BFR-INVALID-BOUNDARY-ID", path, "invalid boundary ID", boundary_id, BOUNDARY_ID_RE.pattern)
                )

    for row in definition_rows:
        if len(row) != len(BOUNDARY_DEFINITION_COLUMNS):
            vocabulary.append(_issue("BFR-ROW-SHAPE", path, "boundary definition row has wrong width", len(row), len(BOUNDARY_DEFINITION_COLUMNS)))
            continue
        if not BOUNDARY_ID_RE.fullmatch(row[0]):
            vocabulary.append(_issue("BFR-INVALID-BOUNDARY-ID", path, "invalid boundary ID", row[0], BOUNDARY_ID_RE.pattern))
        if row[1] not in CORE_DIMENSIONS:
            vocabulary.append(_issue("BFR-UNKNOWN-DIMENSION", path, "unknown boundary dimension", row[1], ", ".join(CORE_DIMENSIONS)))
        elif not row[0].startswith(DIMENSION_PREFIXES[row[1]]):
            vocabulary.append(
                _issue(
                    "BFR-BOUNDARY-PREFIX-MISMATCH",
                    path,
                    "boundary ID prefix does not match its core dimension",
                    row[0],
                    DIMENSION_PREFIXES[row[1]],
                )
            )
        vocabulary.extend(_id_list_vocabulary_issues(row[2], path=path, code="BFR-INVALID-REQUIREMENT-ID"))
        if row[6] == "-" or not STABLE_ID_RE.fullmatch(row[6]):
            vocabulary.append(_issue("BFR-INVALID-OWNER-ID", path, "boundary owner must be one stable requirement ID", row[6], "stable requirement ID"))

    for row in interaction_rows:
        if len(row) != len(INTERACTION_COLUMNS):
            vocabulary.append(_issue("BFR-ROW-SHAPE", path, "interaction row has wrong width", len(row), len(INTERACTION_COLUMNS)))
            continue
        if not INTERACTION_ID_RE.fullmatch(row[0]):
            vocabulary.append(_issue("BFR-INVALID-INTERACTION-ID", path, "invalid interaction ID", row[0], INTERACTION_ID_RE.pattern))
        vocabulary.extend(_id_list_vocabulary_issues(row[1], path=path, code="BFR-INVALID-REQUIREMENT-ID"))
        for boundary_id in _split_ids(row[2]):
            if not BOUNDARY_ID_RE.fullmatch(boundary_id):
                vocabulary.append(_issue("BFR-INVALID-BOUNDARY-ID", path, "invalid interaction boundary ID", boundary_id, BOUNDARY_ID_RE.pattern))

    for row in example_rows:
        if len(row) != len(EXAMPLE_COLUMNS):
            vocabulary.append(_issue("BFR-ROW-SHAPE", path, "example row has wrong width", len(row), len(EXAMPLE_COLUMNS)))
            continue
        if row[1] not in EXAMPLE_CLASSES:
            vocabulary.append(_issue("BFR-UNKNOWN-EXAMPLE-CLASS", path, "unknown example classification", row[1], ", ".join(sorted(EXAMPLE_CLASSES))))
        if not STABLE_ID_RE.fullmatch(row[0]):
            vocabulary.append(_issue("BFR-INVALID-EXAMPLE-ID", path, "invalid example ID", row[0], "stable project ID"))
        vocabulary.extend(_id_list_vocabulary_issues(row[2], path=path, code="BFR-INVALID-REQUIREMENT-ID"))
        for boundary_id in _split_ids(row[3]):
            if not BOUNDARY_ID_RE.fullmatch(boundary_id):
                vocabulary.append(_issue("BFR-INVALID-BOUNDARY-ID", path, "invalid example boundary ID", boundary_id, BOUNDARY_ID_RE.pattern))
        for value, label in ((row[4], "regression"), (row[5], "discovery-gap")):
            if value != "-" and not STABLE_ID_RE.fullmatch(value):
                vocabulary.append(_issue("BFR-INVALID-EXAMPLE-OWNER-ID", path, f"invalid {label} ID", value, "stable project ID"))

    if vocabulary:
        priority = {
            "BFR-UNKNOWN-CONTRACT-VERSION": 0,
            "BFR-UNKNOWN-MODEL-VERSION": 1,
            "BFR-UNKNOWN-DIMENSION": 2,
            "BFR-UNKNOWN-APPLICABILITY": 3,
        }
        return tuple(sorted(vocabulary, key=lambda issue: priority.get(issue.code, 10)))

    issues: list[ValidationIssue] = []
    dimensions = [row[0] for row in model_rows]
    if len(dimensions) != len(CORE_DIMENSIONS) or set(dimensions) != set(CORE_DIMENSIONS):
        issues.append(_issue("BFR-CORE-DIMENSION-MEMBERSHIP", path, "every core dimension must appear exactly once", dimensions, CORE_DIMENSIONS))
    scope = set(_split_ids(scope_value))
    declared_boundaries = [row[0] for row in definition_rows]
    if len(declared_boundaries) != len(set(declared_boundaries)):
        issues.append(_issue("BFR-DUPLICATE-BOUNDARY", path, "boundary IDs must be unique", declared_boundaries, "unique IDs"))
    boundary_rows = {row[0]: row for row in definition_rows}
    model_boundary_ids = {
        boundary_id
        for row in model_rows
        for boundary_id in _split_ids(row[3])
    }
    unowned_definitions = sorted(set(declared_boundaries) - model_boundary_ids)
    if unowned_definitions:
        issues.append(
            _issue(
                "BFR-UNOWNED-BOUNDARY-DEFINITION",
                path,
                "every boundary definition must be owned by one applicability row",
                ", ".join(unowned_definitions),
                "owned boundary IDs",
            )
        )
    for definition in definition_rows:
        if any(value == "-" for value in definition[2:]):
            issues.append(
                _issue(
                    "BFR-INCOMPLETE-BOUNDARY-DEFINITION",
                    path,
                    "boundary definitions require requirements, partitions or transitions, invariants, outcomes, and owner",
                    definition,
                    "complete boundary definition",
                )
            )

    for row in model_rows:
        dimension, applicability, requirements, boundaries, rationale = row
        requirement_ids = _split_ids(requirements)
        boundary_ids = _split_ids(boundaries)
        if applicability == "applicable":
            if not requirement_ids or not boundary_ids or rationale != "-":
                issues.append(_issue("BFR-APPLICABLE-MISSING-OWNER", path, "applicable dimension requires requirements and boundaries and '-' rationale", row, "owned applicable row"))
        else:
            if requirement_ids or boundary_ids or rationale in {"", "-"}:
                issues.append(_issue("BFR-NOT-APPLICABLE-SHAPE", path, "not-applicable dimension requires '-' IDs and concise rationale", row, "unowned row with rationale"))
        for boundary_id in boundary_ids:
            definition = boundary_rows.get(boundary_id)
            if (
                definition is None
                or definition[1] != dimension
                or set(_split_ids(definition[2])) != set(requirement_ids)
                or definition[6] not in requirement_ids
            ):
                issues.append(_issue("BFR-BOUNDARY-DEFINITION-MISMATCH", path, "boundary must be defined once under its dimension", boundary_id, dimension))
        if not set(requirement_ids).issubset(scope):
            issues.append(_issue("BFR-REQUIREMENT-OUTSIDE-SCOPE", path, "boundary requirements must be in model scope", requirements, scope_value))

    interaction_ids: set[str] = set()
    if interaction_rows:
        for row in interaction_rows:
            interaction_id, requirements, boundaries, hazard, outcome = row
            if interaction_id in interaction_ids:
                issues.append(_issue("BFR-DUPLICATE-INTERACTION", path, "interaction IDs must be unique", interaction_id, "unique ID"))
            interaction_ids.add(interaction_id)
            boundary_ids = _split_ids(boundaries)
            if len(boundary_ids) < 2:
                issues.append(_issue("BFR-INTERACTION-BOUNDARY-COUNT", path, "interaction requires at least two boundaries", boundaries, "two or more IDs"))
            if any(boundary_id not in boundary_rows for boundary_id in boundary_ids):
                issues.append(_issue("BFR-UNKNOWN-BOUNDARY-REFERENCE", path, "interaction cites undefined boundary", boundaries, declared_boundaries))
            if not set(_split_ids(requirements)).issubset(scope):
                issues.append(_issue("BFR-REQUIREMENT-OUTSIDE-SCOPE", path, "interaction requirements must be in model scope", requirements, scope_value))
            if requirements == "-" or hazard == "-" or outcome == "-":
                issues.append(_issue("BFR-INCOMPLETE-INTERACTION", path, "interaction requires requirements, hazard, and outcome", row, "complete interaction"))
    elif not re.search(r"(?m)^No interaction selected:\s*\S", interaction_section):
        issues.append(_issue("BFR-MISSING-INTERACTION-RATIONALE", path, "no-interaction record requires rationale", "-", "No interaction selected: <rationale>"))

    example_ids: set[str] = set()
    for row in example_rows:
        example_id, classification, requirements, boundaries, regression_id, gap_id = row
        if example_id in example_ids:
            issues.append(_issue("BFR-DUPLICATE-EXAMPLE", path, "example IDs must be unique", example_id, "unique ID"))
        example_ids.add(example_id)
        boundary_ids = _split_ids(boundaries)
        if any(boundary_id not in boundary_rows for boundary_id in boundary_ids):
            issues.append(_issue("BFR-UNKNOWN-BOUNDARY-REFERENCE", path, "example cites undefined boundary", boundaries, declared_boundaries))
        example_requirements = set(_split_ids(requirements))
        for boundary_id in boundary_ids:
            definition = boundary_rows.get(boundary_id)
            if definition is not None and not example_requirements.issubset(set(_split_ids(definition[2]))):
                issues.append(_issue("BFR-EXAMPLE-OWNER-MISMATCH", path, "example requirements must be governed by every cited boundary", requirements, definition[2]))
        if classification == "illustration" and (requirements == "-" or not boundary_ids or regression_id != "-" or gap_id != "-"):
            issues.append(_issue("BFR-ILLUSTRATION-SHAPE", path, "illustration links requirements and boundaries only", row, "governed illustration"))
        if classification == "regression" and regression_id == "-":
            issues.append(_issue("BFR-REGRESSION-MISSING-ID", path, "regression requires regression ID", row, "regression ID"))
        if classification == "regression" and (requirements == "-" or not boundary_ids or gap_id != "-"):
            issues.append(_issue("BFR-REGRESSION-SHAPE", path, "regression links requirements and boundaries plus only a regression ID", row, "governed regression"))
        if classification == "discovery" and gap_id == "-":
            issues.append(_issue("BFR-DISCOVERY-MISSING-GAP", path, "discovery requires gap ID", row, "gap ID"))
        if classification == "discovery" and regression_id != "-":
            issues.append(_issue("BFR-DISCOVERY-SHAPE", path, "discovery cannot carry a regression ID", row, "discovery gap"))
    return tuple(issues)


def _feature_contract(
    text: str,
) -> tuple[dict[str, set[str]], dict[str, set[str]], str, str]:
    text = _live_markdown(text)
    boundaries = {
        row[0]: set(_split_ids(row[2]))
        for row in _table(_section(text, "Boundary definitions"))[1]
        if len(row) == len(BOUNDARY_DEFINITION_COLUMNS)
    }
    interactions = {
        row[0]: set(_split_ids(row[1]))
        for row in _table(_section(text, "Selected interactions"))[1]
        if len(row) == len(INTERACTION_COLUMNS)
    }
    model = _section(text, "Boundary model")
    return (
        boundaries,
        interactions,
        _line_value(model, "Boundary model version") or "-",
        _line_value(model, "Boundary model scope") or "-",
    )


def validate_proof_map(
    text: str,
    feature_text: str,
    path: str = "<proof-map>",
) -> tuple[ValidationIssue, ...]:
    feature_issues = validate_feature_record(feature_text)
    if feature_issues:
        return feature_issues
    text = _live_markdown(text)
    vocabulary: list[ValidationIssue] = []
    version = _line_value(text, "Boundary model version")
    scope = _line_value(text, "Boundary model scope")
    if version != METHOD_VERSION:
        vocabulary.append(_issue("BFR-UNKNOWN-MODEL-VERSION", path, "unknown proof model version", version, METHOD_VERSION))
    header, rows = _table(_section(text, "Proof map"))
    if header != PROOF_COLUMNS:
        vocabulary.append(_issue("BFR-UNKNOWN-COLUMNS", path, "proof columns are not closed", header, PROOF_COLUMNS))
    separator_issue = _table_separator_issue(
        _section(text, "Proof map"),
        path=path,
        surface="Proof map",
        expected_width=len(PROOF_COLUMNS),
    )
    if separator_issue:
        vocabulary.append(separator_issue)
    vocabulary.extend(_sentinel_issues(rows, path=path, surface="Proof map"))
    for row in rows:
        if len(row) != len(PROOF_COLUMNS):
            vocabulary.append(_issue("BFR-ROW-SHAPE", path, "proof row has wrong width", len(row), len(PROOF_COLUMNS)))
            continue
        if not PROOF_ID_RE.fullmatch(row[0]):
            vocabulary.append(_issue("BFR-INVALID-PROOF-ID", path, "invalid proof ID", row[0], PROOF_ID_RE.pattern))
        if row[1] not in COVERAGE_STATES:
            vocabulary.append(_issue("BFR-UNKNOWN-COVERAGE", path, "unknown proof coverage state", row[1], ", ".join(sorted(COVERAGE_STATES))))
        if row[5] != "-" and row[5] not in PROOF_LEVELS:
            vocabulary.append(_issue("BFR-UNKNOWN-PROOF-LEVEL", path, "unknown proof level", row[5], ", ".join(sorted(PROOF_LEVELS))))
        if row[6] != "-" and row[6] not in AUTOMATION_MODES:
            vocabulary.append(_issue("BFR-UNKNOWN-AUTOMATION-MODE", path, "unknown automation mode", row[6], ", ".join(sorted(AUTOMATION_MODES))))
        for value, code in (
            (row[2], "BFR-INVALID-REQUIREMENT-ID"),
            (row[3], "BFR-INVALID-PROOF-REFERENCE"),
            (row[4], "BFR-INVALID-TEST-ID"),
            (row[7], "BFR-INVALID-COMMAND-ID"),
            (row[10], "BFR-INVALID-MANUAL-ID"),
        ):
            vocabulary.extend(_id_list_vocabulary_issues(value, path=path, code=code))
        for reference_id in _split_ids(row[3]):
            if not (
                BOUNDARY_ID_RE.fullmatch(reference_id)
                or INTERACTION_ID_RE.fullmatch(reference_id)
            ):
                vocabulary.append(
                    _issue(
                        "BFR-INVALID-PROOF-REFERENCE",
                        path,
                        "proof reference is not a boundary or interaction ID",
                        reference_id,
                        "BND-... or INT-...",
                    )
                )
        if row[11] != "-" and not STABLE_ID_RE.fullmatch(row[11]):
            vocabulary.append(
                _issue(
                    "BFR-INVALID-GAP-ID",
                    path,
                    "uncovered gap ID is not a stable project ID",
                    row[11],
                    "stable project ID",
                )
            )
    if vocabulary:
        priority = {
            "BFR-UNKNOWN-MODEL-VERSION": 0,
            "BFR-UNKNOWN-COVERAGE": 1,
            "BFR-UNKNOWN-PROOF-LEVEL": 2,
            "BFR-UNKNOWN-AUTOMATION-MODE": 3,
        }
        return tuple(sorted(vocabulary, key=lambda issue: priority.get(issue.code, 10)))

    feature_boundaries, feature_interactions, feature_version, feature_scope = _feature_contract(feature_text)
    issues: list[ValidationIssue] = []
    if version != feature_version or scope != feature_scope:
        issues.append(_issue("BFR-PROOF-MODEL-MISMATCH", path, "proof version and scope must match feature record", f"{version}:{scope}", f"{feature_version}:{feature_scope}"))
    reference_requirements = feature_boundaries | feature_interactions
    allowed_refs = set(reference_requirements)
    proof_ids: set[str] = set()
    covered_refs: set[str] = set()
    for row in rows:
        (
            proof_id,
            coverage,
            requirements,
            references,
            test_ids,
            proof_level,
            automation,
            commands,
            evidence,
            milestone,
            manual,
            gap,
        ) = row
        if proof_id in proof_ids:
            issues.append(_issue("BFR-DUPLICATE-PROOF", path, "proof IDs must be unique", proof_id, "unique ID"))
        proof_ids.add(proof_id)
        reference_ids = _split_ids(references)
        if not reference_ids or any(item not in allowed_refs for item in reference_ids):
            issues.append(_issue("BFR-UNKNOWN-BOUNDARY-REFERENCE", path, "proof cites unknown boundary or interaction", references, ", ".join(sorted(allowed_refs))))
        proof_requirements = set(_split_ids(requirements))
        for reference_id in reference_ids:
            owner_requirements = reference_requirements.get(reference_id)
            if owner_requirements is not None and not proof_requirements.issubset(owner_requirements):
                issues.append(_issue("BFR-PROOF-OWNER-MISMATCH", path, "proof requirements must be governed by every cited boundary or interaction", requirements, ", ".join(sorted(owner_requirements))))
        if coverage == "covered":
            covered_refs.update(reference_ids)
            required = (requirements, test_ids, proof_level, automation, evidence, milestone)
            if any(value == "-" for value in required) or gap != "-":
                issues.append(_issue("BFR-COVERED-INCOMPLETE", path, "covered proof row is incomplete", row, "complete covered row"))
            if automation == "automated" and manual != "-":
                issues.append(_issue("BFR-AUTOMATED-MANUAL-PROCEDURE", path, "automated proof must not cite manual procedure", manual, "-"))
            if automation in {"manual", "hybrid"} and (manual == "-" or evidence == "-"):
                issues.append(_issue("BFR-MANUAL-PROCEDURE-MISSING", path, "manual or hybrid proof requires procedure and evidence", row, "manual procedure and evidence"))
        else:
            forbidden = (test_ids, proof_level, automation, commands, evidence, manual)
            if any(value != "-" for value in forbidden) or gap == "-" or requirements == "-" or milestone == "-":
                issues.append(_issue("BFR-GAP-HAS-PROOF", path, "gap row must not carry proof metadata", row, "blocking gap row"))
    required_refs = set(feature_boundaries) | set(feature_interactions)
    missing = sorted(required_refs - covered_refs)
    if missing:
        issues.append(_issue("BFR-MISSING-DIRECT-PROOF", path, "applicable boundaries and interactions require covered proof", ", ".join(missing), "covered proof"))
    return tuple(issues)


def _activation_data(path: Path) -> tuple[dict[str, object] | None, ValidationIssue | None]:
    if not path.is_file():
        return None, _issue("BFR-ACTIVATION-MISSING", path.as_posix(), "activation record is missing", "-", ACTIVATION_RECORD.as_posix())
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, _issue("BFR-ACTIVATION-PARSE", path.as_posix(), "activation record is not deterministic JSON-compatible YAML", type(exc).__name__, "valid object")
    if not isinstance(data, dict):
        return None, _issue("BFR-ACTIVATION-SHAPE", path.as_posix(), "activation record must be an object", type(data).__name__, "object")
    return data, None


def _lifecycle_status(text: str) -> str | None:
    status_section = _section(_live_markdown(text), "Status")
    for line in status_section.splitlines():
        value = line.strip().lstrip("-").strip().strip("`").rstrip(".").casefold()
        if value:
            return value
    return None


def _specs_root_issue(root: Path) -> ValidationIssue | None:
    specs_root = root / "specs"
    if specs_root.is_symlink():
        return _issue(
            "BFR-SPECS-ROOT-UNSAFE",
            "specs",
            "specs root must not be a symlink",
            "symlink",
            "repository-owned directory",
        )
    resolved_root = root.resolve()
    resolved_specs = specs_root.resolve(strict=False)
    if not resolved_specs.is_relative_to(resolved_root):
        return _issue(
            "BFR-SPECS-ROOT-UNSAFE",
            "specs",
            "specs root resolves outside the repository",
            resolved_specs,
            resolved_root / "specs",
        )
    return None


def _fixed_authoritative_path(
    root: Path,
    relative_path: Path,
) -> tuple[Path | None, ValidationIssue | None]:
    specs_issue = _specs_root_issue(root)
    if specs_issue:
        return None, specs_issue
    candidate = root / relative_path
    resolved_specs = (root / "specs").resolve()
    resolved_candidate = candidate.resolve(strict=False)
    if (
        candidate.is_symlink()
        or resolved_candidate.parent != resolved_specs
        or (candidate.exists() and not candidate.is_file())
    ):
        return None, _issue(
            "BFR-AUTHORITATIVE-PATH-UNSAFE",
            relative_path.as_posix(),
            "authoritative input must be repository-contained and non-symlink",
            relative_path.as_posix(),
            "repository-owned regular file",
        )
    return candidate, None


def _contained_regular_file(
    root: Path,
    relative_path: Path,
) -> tuple[Path | None, ValidationIssue | None]:
    candidate = root / relative_path
    current = root
    for part in relative_path.parts:
        current = current / part
        if current.is_symlink():
            return None, _issue(
                "BFR-ROLLBACK-PATH-UNSAFE",
                relative_path.as_posix(),
                "rollback metadata path must not traverse a symlink",
                relative_path.as_posix(),
                "repository-contained regular file",
            )
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve(strict=False)
    if (
        not resolved_candidate.is_relative_to(resolved_root)
        or not candidate.is_file()
    ):
        return None, _issue(
            "BFR-ROLLBACK-PATH-UNSAFE",
            relative_path.as_posix(),
            "rollback metadata input must be a repository-contained regular file",
            relative_path.as_posix(),
            "repository-contained regular file",
        )
    return candidate, None


def _rollback_package_matrix(
    root: Path,
    activation_data: dict[str, object],
) -> tuple[tuple[RollbackArtifactIdentity, ...], tuple[ValidationIssue, ...]]:
    """Select existing rollback package identities without mutation or installation."""

    rollback_release = activation_data.get("rollback_release")
    if (
        activation_data.get("state") != "active"
        or not isinstance(rollback_release, str)
        or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", rollback_release)
    ):
        return (), (
            _issue(
                "BFR-ROLLBACK-SELECTION",
                ACTIVATION_RECORD.as_posix(),
                "rollback package selection requires an active manifest and release tag",
                [activation_data.get("state"), rollback_release],
                ["active", "v<major>.<minor>.<patch>"],
            ),
        )

    manifest_relative = Path("dist/adapters/manifest.yaml")
    metadata_relative = (
        Path("docs/reports/adapter-artifacts/releases")
        / f"{rollback_release}.yaml"
    )
    manifest_path, manifest_issue = _contained_regular_file(root, manifest_relative)
    metadata_path, metadata_issue = _contained_regular_file(root, metadata_relative)
    path_issues = tuple(
        issue for issue in (manifest_issue, metadata_issue) if issue is not None
    )
    if path_issues:
        return (), path_issues
    assert manifest_path is not None
    assert metadata_path is not None

    try:
        manifest = parse_manifest_yaml(
            manifest_path.read_text(encoding="utf-8"),
            manifest_path,
        )
        metadata = parse_adapter_artifact_metadata_yaml(
            metadata_path.read_text(encoding="utf-8"),
            metadata_path,
        )
    except (OSError, ValueError) as exc:
        return (), (
            _issue(
                "BFR-ROLLBACK-METADATA",
                metadata_relative.as_posix(),
                "rollback package metadata is malformed or unreadable",
                str(exc),
                "valid existing adapter support and artifact metadata",
            ),
        )

    expected_adapters = tuple(
        sorted(
            {
                adapter
                for skill in manifest.skills.values()
                for adapter in skill.adapters
            },
            key=lambda value: value.encode("utf-8"),
        )
    )
    by_adapter: dict[str, list[AdapterArtifactEntry]] = {}
    for artifact in metadata.artifacts:
        by_adapter.setdefault(artifact.adapter, []).append(artifact)

    issues: list[ValidationIssue] = []
    if metadata.version != rollback_release:
        issues.append(
            _issue(
                "BFR-ROLLBACK-MIXED-VERSION",
                metadata_relative.as_posix(),
                "rollback artifact metadata release differs from the selected release",
                metadata.version,
                rollback_release,
            )
        )
    if tuple(sorted(by_adapter, key=lambda value: value.encode("utf-8"))) != expected_adapters:
        issues.append(
            _issue(
                "BFR-ROLLBACK-ADAPTER-SET",
                metadata_relative.as_posix(),
                "rollback artifacts must match the adapter support inventory exactly",
                sorted(by_adapter),
                expected_adapters,
            )
        )
    if metadata.validation_result != "pass":
        issues.append(
            _issue(
                "BFR-ROLLBACK-RESULT",
                metadata_relative.as_posix(),
                "rollback release validation result must pass",
                metadata.validation_result,
                "pass",
            )
        )

    matrix: list[RollbackArtifactIdentity] = []
    for adapter in expected_adapters:
        artifacts = by_adapter.get(adapter, [])
        if len(artifacts) != 1:
            issues.append(
                _issue(
                    "BFR-ROLLBACK-ADAPTER-COUNT",
                    metadata_relative.as_posix(),
                    "rollback metadata must contain exactly one artifact per adapter",
                    [adapter, len(artifacts)],
                    [adapter, 1],
                )
            )
            continue
        artifact = artifacts[0]
        expected_archive = adapter_archive_name(adapter, rollback_release)
        if (
            artifact.archive != expected_archive
            or artifact.result != "pass"
            or not SHA256_RE.fullmatch(artifact.sha256)
        ):
            issues.append(
                _issue(
                    "BFR-ROLLBACK-ARTIFACT",
                    metadata_relative.as_posix(),
                    "rollback artifact identity must match the selected release and pass",
                    [adapter, artifact.archive, artifact.sha256, artifact.result],
                    [adapter, expected_archive, "64 lowercase hex characters", "pass"],
                )
            )
            continue
        matrix.append(
            RollbackArtifactIdentity(
                adapter=adapter,
                archive=artifact.archive,
                sha256=artifact.sha256,
            )
        )

    if issues:
        return (), tuple(issues)
    return tuple(matrix), ()


def rollback_package_selection(
    root: Path,
) -> tuple[RollbackSelection | None, tuple[ValidationIssue, ...]]:
    """Select rollback identities from the fixed, validated activation manifest."""

    record_path, path_issue = _fixed_authoritative_path(root, ACTIVATION_RECORD)
    if path_issue:
        return None, (path_issue,)
    assert record_path is not None
    data, parse_issue = _activation_data(record_path)
    if parse_issue:
        return None, (parse_issue,)
    assert data is not None
    activation_issues = validate_activation(root)
    if activation_issues:
        return None, activation_issues
    rollback_release = data.get("rollback_release")
    if data.get("state") != "active" or not isinstance(rollback_release, str):
        return None, (
            _issue(
                "BFR-ROLLBACK-SELECTION",
                ACTIVATION_RECORD.as_posix(),
                "authoritative activation manifest is not active",
                data.get("state"),
                "active",
            ),
        )
    matrix, matrix_issues = _rollback_package_matrix(root, data)
    if matrix_issues:
        return None, matrix_issues
    return RollbackSelection(release=rollback_release, artifacts=matrix), ()


def _eligible_grandfathered_specs(
    root: Path,
    baseline_revision: str,
) -> tuple[tuple[str, ...], tuple[ValidationIssue, ...]]:
    eligible: list[str] = []
    if not re.fullmatch(r"[0-9a-f]{40,64}", baseline_revision):
        return (), (
            _issue(
                "BFR-BASELINE-REVISION",
                ACTIVATION_RECORD.as_posix(),
                "grandfathering baseline must be a full commit identity",
                baseline_revision,
                "full source-control commit identity",
            ),
        )
    try:
        listing = subprocess.run(
            ["git", "ls-tree", "-rz", baseline_revision, "--", "specs"],
            cwd=root,
            check=True,
            capture_output=True,
        ).stdout.split(b"\0")
    except (OSError, subprocess.CalledProcessError):
        return (), (
            _issue(
                "BFR-BASELINE-UNAVAILABLE",
                ACTIVATION_RECORD.as_posix(),
                "grandfathering baseline is unavailable",
                baseline_revision,
                "readable source-control commit",
            ),
        )
    for entry in listing:
        if not entry:
            continue
        try:
            header, raw_relative = entry.split(b"\t", 1)
            mode, object_type, object_id = header.decode("ascii").split(" ", 2)
            relative = raw_relative.decode("utf-8")
        except (UnicodeDecodeError, ValueError):
            return (), (
                _issue(
                    "BFR-BASELINE-TREE",
                    ACTIVATION_RECORD.as_posix(),
                    "baseline tree entry is malformed or not UTF-8",
                    entry,
                    "regular UTF-8 Git tree entry",
                ),
            )
        if (
            not re.fullmatch(r"specs/[^/]+\.md", relative)
            or relative == "specs/README.md"
            or relative.endswith(".test.md")
            or relative == PROOF_MODEL_SPEC.as_posix()
        ):
            continue
        if object_type != "blob" or mode not in {"100644", "100755"}:
            return (), (
                _issue(
                    "BFR-BASELINE-MODE",
                    relative,
                    "baseline feature spec must be a regular blob",
                    f"{mode} {object_type}",
                    "100644 blob or 100755 blob",
                ),
            )
        try:
            raw_text = subprocess.run(
                ["git", "cat-file", "blob", object_id],
                cwd=root,
                check=True,
                capture_output=True,
            ).stdout
            text = raw_text.decode("utf-8")
        except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
            return (), (
                _issue(
                    "BFR-BASELINE-UNAVAILABLE",
                    relative,
                    "baseline feature spec cannot be read",
                    baseline_revision,
                    "readable source-control object",
                ),
            )
        if _lifecycle_status(text) not in {"accepted", "approved", "active"}:
            continue
        if _line_value(_live_markdown(text), "boundary_contract") is not None:
            continue
        eligible.append(relative)
    return tuple(sorted(eligible, key=lambda value: value.encode("utf-8"))), ()


def _activation_transition(
    root: Path,
) -> tuple[tuple[str, str, dict[str, object]] | None, tuple[ValidationIssue, ...]]:
    try:
        commits = subprocess.run(
            ["git", "rev-list", "--first-parent", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        commits = []
    transitions: list[tuple[str, str, dict[str, object]]] = []
    for commit in commits:
        try:
            ancestry = subprocess.run(
                ["git", "rev-list", "--parents", "-n", "1", commit],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.split()
            if len(ancestry) < 2:
                continue
            parent = ancestry[1]
            current = json.loads(
                subprocess.run(
                    ["git", "show", f"{commit}:{ACTIVATION_RECORD.as_posix()}"],
                    cwd=root,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout
            )
            previous = json.loads(
                subprocess.run(
                    ["git", "show", f"{parent}:{ACTIVATION_RECORD.as_posix()}"],
                    cwd=root,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout
            )
        except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        if (
            isinstance(current, dict)
            and isinstance(previous, dict)
            and current.get("state") == "active"
            and previous.get("state") == "pending"
        ):
            transitions.append((commit, parent, current))
    if len(transitions) != 1:
        return None, (
            _issue(
                "BFR-ACTIVATION-TRANSITION",
                ACTIVATION_RECORD.as_posix(),
                "source control must contain exactly one pending-to-active transition",
                len(transitions),
                1,
            ),
        )
    return transitions[0], ()


def _release_predecessor(
    root: Path,
    activating_release: object,
) -> tuple[str | None, str | None, tuple[ValidationIssue, ...]]:
    if not isinstance(activating_release, str) or not re.fullmatch(
        r"v[0-9]+\.[0-9]+\.[0-9]+", activating_release
    ):
        return None, None, (
            _issue(
                "BFR-ACTIVATING-RELEASE",
                ACTIVATION_RECORD.as_posix(),
                "active manifest requires an immutable semantic-version tag",
                activating_release,
                "existing v<major>.<minor>.<patch> tag",
            ),
        )
    try:
        tag_names = subprocess.run(
            ["git", "tag", "--list", "v[0-9]*"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        tag_names = []
    versions: list[tuple[tuple[int, int, int], str, str]] = []
    for tag in tag_names:
        match = re.fullmatch(r"v([0-9]+)\.([0-9]+)\.([0-9]+)", tag)
        if not match:
            continue
        try:
            commit = subprocess.run(
                ["git", "rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            continue
        versions.append((tuple(int(part) for part in match.groups()), tag, commit))
    ordered = [(tag, commit) for _, tag, commit in sorted(versions)]
    ordered_tags = [tag for tag, _ in ordered]
    if activating_release not in ordered_tags:
        return None, None, (
            _issue(
                "BFR-ACTIVATING-RELEASE",
                ACTIVATION_RECORD.as_posix(),
                "activating release tag does not exist",
                activating_release,
                "existing immutable release tag",
            ),
        )
    index = ordered_tags.index(activating_release)
    if index == 0:
        return None, ordered[index][1], (
            _issue(
                "BFR-ROLLBACK-RELEASE",
                ACTIVATION_RECORD.as_posix(),
                "activating release has no published predecessor",
                activating_release,
                "release tag with an immediate predecessor",
            ),
        )
    return ordered[index - 1][0], ordered[index][1], ()


def _validate_activation(
    root: Path,
    *,
    candidate_release: str | None = None,
) -> tuple[ValidationIssue, ...]:
    record_path, record_path_issue = _fixed_authoritative_path(
        root,
        ACTIVATION_RECORD,
    )
    if record_path_issue:
        return (record_path_issue,)
    assert record_path is not None
    spec_path, spec_path_issue = _fixed_authoritative_path(
        root,
        PROOF_MODEL_SPEC,
    )
    if spec_path_issue:
        return (spec_path_issue,)
    assert spec_path is not None
    data, parse_issue = _activation_data(record_path)
    if parse_issue:
        return (parse_issue,)
    assert data is not None
    vocabulary: list[ValidationIssue] = []
    state = data.get("state")
    if state not in ACTIVATION_STATES:
        vocabulary.append(
            _issue("BFR-UNKNOWN-ACTIVATION-STATE", ACTIVATION_RECORD.as_posix(), "unknown activation state", state, ", ".join(sorted(ACTIVATION_STATES)))
        )
    if set(data) != ACTIVATION_FIELDS:
        vocabulary.append(_issue("BFR-ACTIVATION-FIELDS", ACTIVATION_RECORD.as_posix(), "activation fields are not closed", sorted(data), sorted(ACTIVATION_FIELDS)))
    if data.get("contract_version") != METHOD_VERSION:
        vocabulary.append(_issue("BFR-UNKNOWN-CONTRACT-VERSION", ACTIVATION_RECORD.as_posix(), "unknown activation contract version", data.get("contract_version"), METHOD_VERSION))
    governed_skills = data.get("governed_skills")
    if not isinstance(governed_skills, list) or any(
        not isinstance(skill, str) or skill not in GOVERNED_SKILLS
        for skill in governed_skills
    ):
        vocabulary.append(_issue("BFR-UNKNOWN-GOVERNED-SKILL", ACTIVATION_RECORD.as_posix(), "governed skill inventory contains an unknown value", governed_skills, list(GOVERNED_SKILLS)))
    if vocabulary:
        priority = {
            "BFR-UNKNOWN-ACTIVATION-STATE": 0,
            "BFR-UNKNOWN-CONTRACT-VERSION": 1,
            "BFR-UNKNOWN-GOVERNED-SKILL": 2,
            "BFR-ACTIVATION-FIELDS": 3,
        }
        return tuple(sorted(vocabulary, key=lambda issue: priority[issue.code]))

    issues: list[ValidationIssue] = []

    spec_state = None
    if spec_path.is_file():
        spec_state = _line_value(spec_path.read_text(encoding="utf-8"), "Boundary-first contract activation")
    if spec_state != state:
        issues.append(_issue("BFR-ACTIVATION-STATE-MISMATCH", PROOF_MODEL_SPEC.as_posix(), "activation YAML and authoritative spec state differ", state, spec_state))

    expected_source = data.get("canonical_reference")
    if expected_source != CANONICAL_REFERENCE.as_posix():
        issues.append(_issue("BFR-CANONICAL-PATH", ACTIVATION_RECORD.as_posix(), "canonical reference path differs", expected_source, CANONICAL_REFERENCE.as_posix()))
    expected_manifest = data.get("resource_manifest")
    if expected_manifest != RESOURCE_MANIFEST.as_posix():
        issues.append(_issue("BFR-RESOURCE-MANIFEST-PATH", ACTIVATION_RECORD.as_posix(), "resource manifest path differs", expected_manifest, RESOURCE_MANIFEST.as_posix()))
    try:
        projection_result = project_reference(root, mode="check")
    except ProjectionContractError as exc:
        projection_result = None
        issues.append(
            _issue(
                exc.code,
                (
                    exc.path
                    if exc.path != "-"
                    else CANONICAL_REFERENCE.as_posix()
                ),
                exc.message,
                exc.offending_value,
                exc.expected,
            )
        )
    if projection_result is not None:
        actual_source_hash = projection_result.source_sha256
        if data.get("canonical_reference_sha256") != actual_source_hash:
            issues.append(_issue("BFR-CANONICAL-HASH", CANONICAL_REFERENCE.as_posix(), "canonical reference hash differs", data.get("canonical_reference_sha256"), actual_source_hash))
        if data.get("resource_manifest_sha256") != projection_result.manifest_sha256:
            issues.append(_issue("BFR-RESOURCE-MANIFEST-HASH", RESOURCE_MANIFEST.as_posix(), "resource manifest hash differs", data.get("resource_manifest_sha256"), projection_result.manifest_sha256))
        for error in projection_result.errors:
            code, _, affected_path = error.partition(": ")
            issues.append(
                _issue(
                    "BFR-PROJECTION-DIVERGENT"
                    if code == "BFR-PROJECTION-STALE"
                    else code,
                    affected_path or ACTIVATION_RECORD.as_posix(),
                    "governed projection check failed",
                    code,
                    "canonical raw-byte projection",
                )
            )
        if data.get("projection_sha256") != projection_result.projection_sha256:
            issues.append(_issue("BFR-PROJECTION-HASH", ACTIVATION_RECORD.as_posix(), "projection identity differs", data.get("projection_sha256"), projection_result.projection_sha256))

    if governed_skills != list(GOVERNED_SKILLS):
        issues.append(_issue("BFR-GOVERNED-SKILLS", ACTIVATION_RECORD.as_posix(), "governed skill inventory differs", data.get("governed_skills"), list(GOVERNED_SKILLS)))

    activating_release = data.get("activating_release")
    rollback_release = data.get("rollback_release")
    baseline_revision = data.get("grandfathering_baseline_revision")
    if state == "pending":
        for field, value in (
            ("activating_release", activating_release),
            ("rollback_release", rollback_release),
            ("grandfathering_baseline_revision", baseline_revision),
        ):
            if value != "-":
                issues.append(
                    _issue(
                        "BFR-PENDING-ACTIVATION-VALUE",
                        ACTIVATION_RECORD.as_posix(),
                        f"pending {field} must use the sentinel",
                        value,
                        "-",
                    )
                )
    else:
        transition, transition_issues = _activation_transition(root)
        issues.extend(transition_issues)
        if candidate_release is None:
            expected_rollback, activating_tag_commit, release_issues = _release_predecessor(
                root,
                activating_release,
            )
            issues.extend(release_issues)
        else:
            expected_rollback = ACTIVATION_CANDIDATE_ROLLBACK
            activating_tag_commit = None
        if rollback_release != expected_rollback:
            issues.append(
                _issue(
                    "BFR-ROLLBACK-RELEASE",
                    ACTIVATION_RECORD.as_posix(),
                    "rollback release must be the immediately preceding published release",
                    rollback_release,
                    expected_rollback or "immediate predecessor tag",
                )
            )
        transition_commit = transition[0] if transition else None
        expected_baseline = transition[1] if transition else None
        transition_data = transition[2] if transition else {}
        if candidate_release is None and activating_tag_commit != transition_commit:
            issues.append(
                _issue(
                    "BFR-ACTIVATING-TAG-COMMIT",
                    ACTIVATION_RECORD.as_posix(),
                    "activating release tag must resolve to the activation transition commit",
                    activating_tag_commit,
                    transition_commit or "pending-to-active transition commit",
                )
            )
        if (
            transition
            and (
                activating_release != transition_data.get("activating_release")
                or rollback_release != transition_data.get("rollback_release")
            )
        ):
            issues.append(
                _issue(
                    "BFR-ACTIVATION-IMMUTABLE",
                    ACTIVATION_RECORD.as_posix(),
                    "active release fields must match the activation transition snapshot",
                    [activating_release, rollback_release],
                    [
                        transition_data.get("activating_release"),
                        transition_data.get("rollback_release"),
                    ],
                )
            )
        transition_baseline = transition_data.get("grandfathering_baseline_revision")
        if transition and transition_baseline != expected_baseline:
            issues.append(
                _issue(
                    "BFR-BASELINE-PARENT",
                    ACTIVATION_RECORD.as_posix(),
                    "activation transition snapshot must record its exact first parent",
                    transition_baseline,
                    expected_baseline or "transition parent commit",
                )
            )
        if not isinstance(baseline_revision, str) or not re.fullmatch(
            r"[0-9a-f]{40,64}",
            baseline_revision,
        ):
            issues.append(
                _issue(
                    "BFR-BASELINE-REVISION",
                    ACTIVATION_RECORD.as_posix(),
                    "active baseline must be a full commit identity",
                    baseline_revision,
                    "full source-control commit identity",
                )
            )
        elif baseline_revision != expected_baseline:
            issues.append(
                _issue(
                    "BFR-BASELINE-PARENT",
                    ACTIVATION_RECORD.as_posix(),
                    "baseline must be the exact parent of the pending-to-active transition",
                    baseline_revision,
                    expected_baseline or "transition parent commit",
                )
            )

    grandfathered = data.get("grandfathered_specs")
    if not isinstance(grandfathered, list):
        issues.append(_issue("BFR-GRANDFATHERED-SHAPE", ACTIVATION_RECORD.as_posix(), "grandfathered_specs must be a list", type(grandfathered).__name__, "list"))
    else:
        previous: bytes | None = None
        valid_paths: list[str] = []
        for item_path in grandfathered:
            encoded = item_path.encode("utf-8") if isinstance(item_path, str) else b""
            if (
                not isinstance(item_path, str)
                or (previous is not None and encoded <= previous)
                or not re.fullmatch(r"specs/[^/]+\.md", item_path)
                or item_path.endswith(".test.md")
                or item_path == "specs/README.md"
                or item_path == PROOF_MODEL_SPEC.as_posix()
            ):
                issues.append(
                    _issue(
                        "BFR-GRANDFATHERED-ORDER",
                        ACTIVATION_RECORD.as_posix(),
                        "grandfathered paths must be eligible unique top-level feature specs sorted by raw UTF-8 bytes",
                        item_path,
                        "eligible sorted specs/*.md paths",
                    )
                )
                continue
            previous = encoded
            valid_paths.append(item_path)
        if state == "pending" and grandfathered:
            issues.append(
                _issue(
                    "BFR-PENDING-GRANDFATHERED",
                    ACTIVATION_RECORD.as_posix(),
                    "pending manifest must have an empty grandfathered inventory",
                    grandfathered,
                    [],
                )
            )
        if (
            state == "active"
            and isinstance(expected_baseline, str)
            and re.fullmatch(r"[0-9a-f]{40,64}", expected_baseline)
        ):
            eligible_membership, eligibility_issues = _eligible_grandfathered_specs(
                root,
                expected_baseline,
            )
            issues.extend(eligibility_issues)
            transition_inventory = transition_data.get("grandfathered_specs")
            if (
                not isinstance(transition_inventory, list)
                or tuple(transition_inventory) != eligible_membership
            ):
                issues.append(
                    _issue(
                        "BFR-GRANDFATHERED-MEMBERSHIP",
                        ACTIVATION_RECORD.as_posix(),
                        "activation transition snapshot inventory does not match its first parent",
                        transition_inventory,
                        eligible_membership,
                    )
                )
            if transition and (
                baseline_revision != transition_baseline
                or grandfathered != transition_inventory
            ):
                issues.append(
                    _issue(
                        "BFR-ACTIVATION-IMMUTABLE",
                        ACTIVATION_RECORD.as_posix(),
                        "active baseline and inventory must match the activation transition snapshot",
                        [baseline_revision, grandfathered],
                        [transition_baseline, transition_inventory],
                    )
                )
            if tuple(valid_paths) != eligible_membership:
                issues.append(
                    _issue(
                        "BFR-GRANDFATHERED-MEMBERSHIP",
                        ACTIVATION_RECORD.as_posix(),
                        "grandfathered inventory does not match eligible parent-revision feature specs",
                        valid_paths,
                        eligible_membership,
                    )
                )

    if state == "active":
        _, rollback_issues = _rollback_package_matrix(root, data)
        issues.extend(rollback_issues)

    return tuple(issues)


def validate_activation(root: Path) -> tuple[ValidationIssue, ...]:
    """Validate the standing strict activation contract."""

    return _validate_activation(root)


def _candidate_lifecycle_paths() -> tuple[Path, ...]:
    return tuple(
        ACTIVATION_CHANGE_ROOT / relative
        for relative in (
            "evidence/proposal-authoring.md",
            "evidence/spec-authoring.md",
            "evidence/architecture-authoring.md",
            "evidence/plan-authoring.md",
            "evidence/test-spec-authoring.md",
            "evidence/implementation-m1.md",
            "evidence/implementation-m2.md",
            "evidence/implementation-m3.md",
            "evidence/implementation-m4.md",
            "explain-change.md",
        )
    )


def validate_activation_publication_readiness(
    root: Path,
) -> tuple[ValidationIssue, ...]:
    """Check release-lifecycle evidence required before external publication."""

    missing = [
        path.as_posix()
        for path in _candidate_lifecycle_paths()
        if not (root / path).is_file()
    ]
    reviews_root = root / ACTIVATION_CHANGE_ROOT / "reviews"
    for milestone in range(1, 5):
        if not any(reviews_root.glob(f"code-review-m{milestone}-r*.md")):
            missing.append(
                (
                    ACTIVATION_CHANGE_ROOT
                    / "reviews"
                    / f"code-review-m{milestone}-r*.md"
                ).as_posix()
            )
    change_yaml = root / ACTIVATION_CHANGE_ROOT / "change.yaml"
    metadata: object = None
    if change_yaml.is_file():
        try:
            metadata = _parse_change_yaml_text(change_yaml.read_text(encoding="utf-8"))
        except Exception:
            missing.append(change_yaml.relative_to(root).as_posix() + "#valid-metadata")
    else:
        missing.append(change_yaml.relative_to(root).as_posix())
    if isinstance(metadata, dict):
        states = metadata.get("artifact_states")
        expected_states = {
            "proposal": "accepted",
            "spec": "approved",
            "adr-activation-publication": "active",
            "plan": "active",
            "test-spec": "active",
        }
        if not isinstance(states, dict):
            missing.append(change_yaml.relative_to(root).as_posix() + "#artifact-states")
        else:
            for artifact_id, lifecycle_state in expected_states.items():
                entry = states.get(artifact_id)
                review = entry.get("review") if isinstance(entry, dict) else None
                if (
                    not isinstance(entry, dict)
                    or entry.get("lifecycle_state") != lifecycle_state
                    or not isinstance(review, dict)
                    or review.get("outcome") != "approved"
                ):
                    missing.append(
                        change_yaml.relative_to(root).as_posix()
                        + f"#settled-{artifact_id}"
                    )
        workflow_state = metadata.get("workflow_state")
        planned = (
            workflow_state.get("planned_work")
            if isinstance(workflow_state, dict)
            else None
        )
        milestones = planned.get("milestones") if isinstance(planned, dict) else None
        if not isinstance(milestones, dict) or any(
            not isinstance(milestones.get(f"M{number}"), dict)
            or milestones[f"M{number}"].get("state") != "closed"
            for number in range(1, 5)
        ):
            missing.append(change_yaml.relative_to(root).as_posix() + "#closed-milestones")
        latest = planned.get("latest_review") if isinstance(planned, dict) else None
        if (
            not isinstance(latest, dict)
            or latest.get("status") != "approved"
            or latest.get("stage") != "code-review"
            or latest.get("milestone_id") != "M4"
        ):
            missing.append(change_yaml.relative_to(root).as_posix() + "#approved-m4-review")
        review_state = metadata.get("review")
        if (
            not isinstance(review_state, dict)
            or review_state.get("status") != "approved"
            or review_state.get("unresolved_items") != 0
        ):
            missing.append(change_yaml.relative_to(root).as_posix() + "#review-closeout")

    resolution = root / ACTIVATION_CHANGE_ROOT / "review-resolution.md"
    if not resolution.is_file() or "Closeout status: closed" not in resolution.read_text(
        encoding="utf-8"
    ):
        missing.append(resolution.relative_to(root).as_posix() + "#closed")
    review_log = root / ACTIVATION_CHANGE_ROOT / "review-log.md"
    if not review_log.is_file() or re.search(
        r"^Open findings:\s+(?!None\s*$).+",
        review_log.read_text(encoding="utf-8") if review_log.is_file() else "",
        re.MULTILINE,
    ):
        missing.append(review_log.relative_to(root).as_posix() + "#no-open-findings")
    candidate_path = root / ACTIVATION_CHANGE_ROOT / "evidence/boundary-activation-candidate.json"
    try:
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        candidate = None
    if not isinstance(candidate, dict):
        missing.append(candidate_path.relative_to(root).as_posix() + "#valid-candidate")

    if not missing:
        candidate_issues = _candidate_evidence_issues(root, candidate)
        if candidate_issues:
            return candidate_issues
        authority_issues = _publication_authority_issues(root)
        if not authority_issues:
            return ()
        return authority_issues
    return (
        _issue(
            "BFR-CANDIDATE-EVIDENCE-MISSING",
            ACTIVATION_CHANGE_ROOT.as_posix(),
            "required activation lifecycle evidence is unsettled",
            missing,
            "settled proposal-through-rationale implementation and review evidence",
        ),
    )


def _publication_authority_issues(root: Path) -> tuple[ValidationIssue, ...]:
    scripts_root = Path(__file__).resolve().parent
    relative_change = ACTIVATION_CHANGE_ROOT / "change.yaml"
    paths = (
        relative_change,
        ACTIVATION_CHANGE_ROOT / "review-log.md",
        ACTIVATION_CHANGE_ROOT / "review-resolution.md",
    )
    commands = (
        [
            sys.executable,
            str(scripts_root / "validate-change-metadata.py"),
            relative_change.as_posix(),
        ],
        [
            sys.executable,
            str(scripts_root / "validate-review-artifacts.py"),
            ACTIVATION_CHANGE_ROOT.as_posix(),
        ],
        [
            sys.executable,
            str(scripts_root / "validate-artifact-lifecycle.py"),
            "--mode",
            "explicit-paths",
            *(
                argument
                for path in paths
                for argument in ("--path", path.as_posix())
            ),
        ],
    )
    issues: list[ValidationIssue] = []
    for index, command in enumerate(commands, start=1):
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError:
            completed = None
        if completed is None or completed.returncode != 0:
            issues.append(
                _issue(
                    "BFR-CANDIDATE-EVIDENCE-UNSETTLED",
                    ACTIVATION_CHANGE_ROOT.as_posix(),
                    "canonical lifecycle authority rejects publication readiness",
                    f"authority-check-{index}-failed",
                    "change metadata, formal review, and artifact lifecycle checks pass",
                )
            )
    return tuple(issues)


def _is_activation_lifecycle_path(relative: str) -> bool:
    path = PurePosixPath(relative)
    root = PurePosixPath(ACTIVATION_CHANGE_ROOT.as_posix())
    if root not in path.parents:
        return False
    child = path.relative_to(root)
    if child in {
        PurePosixPath("change.yaml"),
        PurePosixPath("review-log.md"),
        PurePosixPath("review-resolution.md"),
        PurePosixPath("explain-change.md"),
        PurePosixPath("verify-report.md"),
        PurePosixPath("pr.md"),
    }:
        return True
    if len(child.parts) == 2 and child.parts[0] == "evidence":
        return bool(
            re.fullmatch(
                r"(?:(?:proposal|spec|architecture|plan|test-spec)-authoring|implementation-m[1-4]|release-checkpoint)\.md|"
                r"(?:boundary-activation-candidate|atomic-publication)\.json",
                child.name,
            )
        )
    if len(child.parts) == 2 and child.parts[0] == "reviews":
        return bool(
            re.fullmatch(
                r"(?:proposal|spec|architecture|plan|test-spec|code-review|verify)-review(?:-[a-z0-9-]+)?-r[0-9]+\.md|"
                r"code-review-(?:m[1-4]|final)-r[0-9]+\.md",
                child.name,
            )
        )
    return bool(
        len(child.parts) == 1
        and re.fullmatch(
            r"review-invocation-(?:proposal-review-r[0-9]+|spec-review-r[0-9]+|architecture-review-activation-r[0-9]+|plan-review-r[0-9]+|test-spec-review-r[0-9]+|code-review-(?:m[1-4]|final)-r[0-9]+)\.yaml",
            child.name,
        )
    )


def _private_runtime_values() -> tuple[str, ...]:
    values: set[str] = set()
    try:
        values.add(getpass.getuser())
    except (KeyError, OSError):
        pass
    try:
        values.add(socket.gethostname())
    except OSError:
        pass
    for name, value in os.environ.items():
        if len(value) >= 6 or re.search(
            r"(?i)(token|otp|pin|passcode|mfa|2fa|api[_-]?key|auth(?:entication|orization)?[_-]?(?:code|token)?|verification[_-]?code|secret|credential|private|username|hostname|password)",
            name,
        ):
            values.add(value)
    return tuple(value for value in values if value)


def _bounded_diagnostic_path(relative: str) -> str:
    if (
        len(relative.encode("utf-8")) > 240
        or re.search(
            r"(?i)(token|otp|secret|credential|private|username|hostname|password)",
            relative,
        )
        or any(ord(character) < 32 for character in relative)
        or any(value in relative for value in _private_runtime_values())
    ):
        encoded = relative.encode("utf-8")
        return (
            "redacted-path:sha256:"
            + hashlib.sha256(encoded).hexdigest()
            + f":bytes={len(encoded)}"
        )
    return relative


def _candidate_changed_paths(
    root: Path,
    transition_commit: str,
    head: str,
) -> tuple[tuple[str, ...], tuple[ValidationIssue, ...]]:
    try:
        commits = subprocess.run(
            ["git", "rev-list", "--topo-order", "--reverse", f"{transition_commit}..{head}"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        return (), (
            _issue(
                "BFR-CANDIDATE-CHANGED-PATHS",
                "<candidate-history>",
                "post-transition commits are unavailable",
                "unavailable",
                "readable first-parent Git history",
            ),
        )
    rejected: set[str] = set()
    invocations: set[str] = set()
    for commit in commits:
        try:
            ancestry = subprocess.run(
                ["git", "rev-list", "--parents", "-n", "1", commit],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.split()
            if len(ancestry) < 2:
                raise subprocess.CalledProcessError(1, "git rev-list")
            changed = subprocess.run(
                [
                    "git", "diff-tree", "--no-commit-id", "--name-only", "-r",
                    "-z", "--no-renames", ancestry[1], commit,
                ],
                cwd=root,
                check=True,
                capture_output=True,
            ).stdout.split(b"\0")
            decoded = [raw.decode("utf-8") for raw in changed if raw]
        except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
            return (), (
                _issue(
                    "BFR-CANDIDATE-CHANGED-PATHS",
                    "<candidate-history>",
                    "post-transition changed paths are unavailable",
                    commit,
                    "readable UTF-8 Git path set",
                ),
            )
        rejected.update(path for path in decoded if not _is_activation_lifecycle_path(path))
        invocations.update(
            path
            for path in decoded
            if PurePosixPath(path).name.startswith("review-invocation-")
            and _is_activation_lifecycle_path(path)
        )
    lifecycle_issues = tuple(
        issue
        for relative in sorted(invocations, key=lambda path: path.encode("utf-8"))
        if (issue := _review_invocation_issue(root, relative)) is not None
    )
    return tuple(sorted(rejected, key=lambda path: path.encode("utf-8"))), lifecycle_issues


def _review_invocation_issue(root: Path, relative: str) -> ValidationIssue | None:
    path = root / relative
    try:
        manifest_text = path.read_text(encoding="utf-8")
        manifest = _parse_change_yaml_text(manifest_text)
        change = _parse_change_yaml_text(
            (root / ACTIVATION_CHANGE_ROOT / "change.yaml").read_text(encoding="utf-8")
        )
    except Exception:
        manifest = None
        change = None
    name = PurePosixPath(relative).name
    review_id = name.removeprefix("review-invocation-").removesuffix(".yaml")
    identity_patterns = (
        (r"proposal-review-r[0-9]+", "proposal-review"),
        (r"spec-review-r[0-9]+", "spec-review"),
        (r"architecture-review-activation-r[0-9]+", "architecture-review"),
        (r"plan-review-r[0-9]+", "plan-review"),
        (r"test-spec-review-r[0-9]+", "test-spec-review"),
        (r"code-review-(?:m[1-4]|final)-r[0-9]+", "code-review"),
    )
    stage = next(
        (candidate_stage for pattern, candidate_stage in identity_patterns
         if re.fullmatch(pattern, review_id)),
        "unknown",
    )
    evidence = (
        change.get("workflow_state", {}).get("evidence", [])
        if isinstance(change, dict)
        and isinstance(change.get("workflow_state"), dict)
        else []
    )
    required_fields = {
        "schema_version", "review_id", "review_stage", "review_target",
        "base_revision", "head_revision", "native_review_status",
        "review_gate_outcome", "independence_level", "author_context_id",
        "reviewer_context_id", "context_separation_mechanism", "risk_tier",
        "governing_artifacts", "formal_criteria", "initial_packet_inventory",
        "manifest_owner", "forbidden_initial_context_excluded",
    }
    allowed_fields = required_fields | {
        "architecture", "phase_receipts", "prompt_template_version",
        "initial_packet_sha256",
        "requirement_fidelity", "review_focus", "risk_map",
        "risk_tier_classifier", "risk_tier_triggers", "second_review",
    }
    target = manifest.get("review_target") if isinstance(manifest, dict) else None
    packets = (
        manifest.get("initial_packet_inventory")
        if isinstance(manifest, dict)
        else None
    )
    packet_revisions = re.findall(
        r"(?m)^\s{4}revision:\s*([0-9a-f]{8,64})\s*$",
        manifest_text if isinstance(manifest, dict) else "",
    )
    packet_shape_valid = bool(packets) and isinstance(packets, list) and all(
        isinstance(packet, dict)
        and set(packet) == {"path", "revision", "sha256"}
        and isinstance(packet.get("path"), str)
        and bool(packet.get("path"))
        and isinstance(packet.get("sha256"), str)
        and bool(re.fullmatch(r"[0-9a-f]{64}", packet["sha256"]))
        for packet in packets
    ) and len(packet_revisions) == len(packets)
    list_fields_valid = isinstance(manifest, dict) and all(
        isinstance(manifest.get(field), list) and bool(manifest[field])
        for field in ("governing_artifacts", "formal_criteria")
    )
    status_pairs = {
        ("approved", "approved"),
        ("blocked", "blocked"),
        ("changes-requested", "changes-requested"),
        ("changes-requested", "stop"),
    }
    scalar_fields_valid = isinstance(manifest, dict) and all(
        isinstance(manifest.get(field), str) and bool(manifest[field])
        for field in (
            "review_target", "author_context_id", "reviewer_context_id",
            "context_separation_mechanism",
        )
    )
    if (
        not isinstance(manifest, dict)
        or set(manifest) - allowed_fields
        or required_fields - set(manifest)
        or manifest.get("schema_version") != 1
        or manifest.get("review_id") != review_id
        or manifest.get("review_stage") != stage
        or not scalar_fields_valid
        or not isinstance(target, str)
        or not (
            target.startswith(("docs/", "specs/", "commit:", "range:"))
        )
        or not isinstance(manifest.get("base_revision"), str)
        or not re.fullmatch(r"[0-9a-f]{8,64}", manifest["base_revision"])
        or not isinstance(manifest.get("head_revision"), str)
        or not re.fullmatch(r"[0-9a-f]{8,64}", manifest["head_revision"])
        or (
            manifest.get("native_review_status"),
            manifest.get("review_gate_outcome"),
        ) not in status_pairs
        or manifest.get("independence_level") not in {"L1", "L2"}
        or manifest.get("risk_tier") not in {"standard", "elevated"}
        or manifest.get("context_separation_mechanism") not in {
            "existing-separate-agents-blind-first",
            "separate-agent-blind-first",
            "separate-agent-bounded-amendment-review",
        }
        or not list_fields_valid
        or not packet_shape_valid
        or (
            "initial_packet_sha256" in manifest
            and (
                not isinstance(manifest["initial_packet_sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", manifest["initial_packet_sha256"])
            )
        )
        or manifest.get("manifest_owner") != "workflow-orchestrator"
        or manifest.get("forbidden_initial_context_excluded") is not True
        or relative not in evidence
    ):
        return _issue(
            "BFR-CANDIDATE-LIFECYCLE-EVIDENCE",
            relative,
            "review invocation must have a recognized identity, valid shape, and change-record ownership",
            "invalid-or-unowned",
            "valid referenced review invocation manifest",
        )
    return None


def _git_identity(root: Path, revision: str) -> str | None:
    try:
        value = subprocess.run(
            ["git", "rev-parse", "--verify", revision],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return value if re.fullmatch(r"[0-9a-f]{40,64}", value) else None


def _git_ref_exists(root: Path, reference: str) -> bool:
    try:
        return subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", reference],
            cwd=root,
            check=False,
            capture_output=True,
        ).returncode == 0
    except OSError:
        return False


def _activation_candidate_authority(
    root: Path,
    release: str,
    *,
    publication_readiness: bool,
) -> tuple[ActivationCandidateResult | None, tuple[ValidationIssue, ...]]:
    """Derive candidate authority under its pre-tag or tagged-readiness phase."""

    if release != ACTIVATION_CANDIDATE_RELEASE:
        return None, (
            _issue(
                "BFR-CANDIDATE-RELEASE",
                "<activation-candidate>",
                "candidate mode is closed to the approved activation release",
                release,
                ACTIVATION_CANDIDATE_RELEASE,
            ),
        )

    issues = list(
        _validate_activation(root)
        if publication_readiness
        else _validate_activation(root, candidate_release=release)
    )
    data, parse_issue = _activation_data(root / ACTIVATION_RECORD)
    if parse_issue or data is None:
        return None, tuple(issues or ([parse_issue] if parse_issue else []))
    if (
        data.get("state") != "active"
        or data.get("activating_release") != release
        or data.get("rollback_release") != ACTIVATION_CANDIDATE_ROLLBACK
    ):
        issues.append(
            _issue(
                "BFR-CANDIDATE-ACTIVATION",
                ACTIVATION_RECORD.as_posix(),
                "candidate requires the exact active release and rollback tuple",
                [data.get("state"), data.get("activating_release"), data.get("rollback_release")],
                ["active", release, ACTIVATION_CANDIDATE_ROLLBACK],
            )
        )

    if not publication_readiness and _git_ref_exists(root, f"refs/tags/{release}"):
        issues.append(
            _issue(
                "BFR-CANDIDATE-LOCAL-TAG",
                f"refs/tags/{release}",
                "candidate tag must be absent locally",
                "present",
                "absent",
            )
        )
    try:
        local_tags = subprocess.run(
            ["git", "tag", "--list", "v[0-9]*"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        local_tags = []
    ordered_tags = sorted(
        (
            (tuple(int(part) for part in match.groups()), tag)
            for tag in local_tags
            if not publication_readiness or tag != release
            if (match := re.fullmatch(r"v([0-9]+)\.([0-9]+)\.([0-9]+)", tag))
        ),
        key=lambda row: row[0],
    )
    predecessor = ordered_tags[-1][1] if ordered_tags else None
    if predecessor != ACTIVATION_CANDIDATE_ROLLBACK:
        issues.append(
            _issue(
                "BFR-CANDIDATE-ROLLBACK-PREDECESSOR",
                "refs/tags",
                "candidate rollback must be the immediate local release predecessor",
                predecessor,
                ACTIVATION_CANDIDATE_ROLLBACK,
            )
        )

    try:
        advertisement = subprocess.run(
            [
                "git", "ls-remote", "--refs", "origin",
                "refs/heads/main", f"refs/tags/{release}",
            ],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        advertisement = []
        issues.append(
            _issue(
                "BFR-CANDIDATE-REMOTE-UNAVAILABLE",
                "refs/remotes/origin",
                "candidate remote advertisement is unavailable",
                "unavailable",
                "reachable origin main and tag namespace",
            )
        )
    remote_refs = {
        ref: identity
        for line in advertisement
        if "\t" in line
        for identity, ref in (line.split("\t", 1),)
    }
    publication_base = remote_refs.get("refs/heads/main")
    if publication_base is None:
        issues.append(
            _issue(
                "BFR-CANDIDATE-REMOTE-MAIN",
                "refs/heads/main",
                "candidate publication base is absent from the remote advertisement",
                "absent",
                "full remote main identity",
            )
        )
    if f"refs/tags/{release}" in remote_refs:
        issues.append(
            _issue(
                "BFR-CANDIDATE-REMOTE-TAG",
                f"refs/tags/{release}",
                "candidate tag must be absent remotely",
                "present",
                "absent",
            )
        )

    transition, transition_issues = _activation_transition(root)
    for issue in transition_issues:
        if issue not in issues:
            issues.append(issue)
    transition_commit = transition[0] if transition else None
    baseline = transition[1] if transition else None
    head = _git_identity(root, "HEAD")
    try:
        worktree_state = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        worktree_state = b"unavailable"
    if worktree_state:
        issues.append(
            _issue(
                "BFR-CANDIDATE-WORKTREE",
                "<candidate-worktree>",
                "candidate validation requires the exact clean reviewed head",
                f"dirty-bytes={len(worktree_state)}",
                "clean HEAD worktree",
            )
        )
    if publication_base and baseline:
        try:
            first_parent = subprocess.run(
                ["git", "rev-list", "--first-parent", baseline],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
        except (OSError, subprocess.CalledProcessError):
            first_parent = []
        if publication_base not in first_parent:
            issues.append(
                _issue(
                    "BFR-CANDIDATE-PUBLICATION-BASE",
                    "refs/heads/main",
                    "publication base must equal or precede the transition baseline on first-parent history",
                    publication_base,
                    baseline,
                )
            )

    if transition_commit and head:
        rejected, changed_path_issues = _candidate_changed_paths(
            root,
            transition_commit,
            head,
        )
        issues.extend(changed_path_issues)
        for rejected_path in rejected:
            issues.append(
                _issue(
                    "BFR-CANDIDATE-POST-TRANSITION-DRIFT",
                    _bounded_diagnostic_path(rejected_path),
                    "post-transition history changes release-gated paths",
                    "changed-after-transition",
                    "activation-change lifecycle evidence paths only",
                )
            )

    if issues or not all((publication_base, baseline, transition_commit, head)):
        return None, tuple(issues)
    bundle = tuple(
        (name, str(data[name]))
        for name in (
            "contract_version",
            "canonical_reference_sha256",
            "resource_manifest_sha256",
            "projection_sha256",
        )
    )
    return ActivationCandidateResult(
        candidate_release=release,
        publication_base=publication_base,
        grandfathering_baseline=baseline,
        transition_commit=transition_commit,
        candidate_validation_head=head,
        rollback_release=ACTIVATION_CANDIDATE_ROLLBACK,
        tag_state="absent",
        bundle_identity=bundle,
    ), ()


def validate_activation_candidate(
    root: Path,
    release: str,
) -> tuple[ActivationCandidateResult | None, tuple[ValidationIssue, ...]]:
    """Validate the one approved pre-tag activation candidate without mutation."""

    return _activation_candidate_authority(
        root,
        release,
        publication_readiness=False,
    )


def _candidate_evidence_issues(
    root: Path,
    candidate: dict[str, object],
) -> tuple[ValidationIssue, ...]:
    fresh, fresh_issues = _activation_candidate_authority(
        root,
        ACTIVATION_CANDIDATE_RELEASE,
        publication_readiness=True,
    )
    if fresh_issues or fresh is None:
        return (
            _issue(
                "BFR-CANDIDATE-EVIDENCE-UNSETTLED",
                (
                    ACTIVATION_CHANGE_ROOT
                    / "evidence/boundary-activation-candidate.json"
                ).as_posix(),
                "persisted candidate evidence cannot be reproduced from current authority",
                "candidate-revalidation-failed",
                "fresh candidate validation succeeds",
            ),
        )
    fresh_data = fresh.as_dict()
    candidate_validation_head = candidate.get("candidate_validation_head")
    candidate_path = ACTIVATION_CHANGE_ROOT / "evidence/boundary-activation-candidate.json"
    try:
        evidence_commit = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", candidate_path.as_posix()],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        ancestry = subprocess.run(
            ["git", "rev-list", "--parents", "-n", "1", evidence_commit],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.split()
        first_parent = ancestry[1] if len(ancestry) >= 2 else None
        first_parent_history = subprocess.run(
            ["git", "rev-list", "--first-parent", fresh.candidate_validation_head],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        evidence_commit = ""
        first_parent = None
        first_parent_history = []
    comparable = dict(candidate)
    comparable["candidate_validation_head"] = fresh.candidate_validation_head
    if (
        comparable != fresh_data
        or not isinstance(candidate_validation_head, str)
        or not re.fullmatch(r"[0-9a-f]{40,64}", candidate_validation_head)
        or first_parent != candidate_validation_head
        or evidence_commit not in first_parent_history
    ):
        return (
            _issue(
                "BFR-CANDIDATE-EVIDENCE-UNSETTLED",
                candidate_path.as_posix(),
                "persisted candidate evidence does not match its producing validation head and current authority",
                "stale-or-forged-candidate-evidence",
                "exact candidate result committed by the immediate child of its candidate-validation head",
            ),
        )
    return ()


_CANDIDATE_CORRECTIVE_ACTIONS = {
    "BFR-CANDIDATE-RELEASE": "use exact candidate release v0.4.0",
    "BFR-CANDIDATE-ACTIVATION": "restore the exact active v0.4.0 and rollback v0.3.6 tuple",
    "BFR-CANDIDATE-LOCAL-TAG": "remove the unpublished local v0.4.0 tag",
    "BFR-CANDIDATE-REMOTE-TAG": "stop because v0.4.0 already exists remotely",
    "BFR-CANDIDATE-REMOTE-UNAVAILABLE": "restore reachable origin advertisement and rerun",
    "BFR-CANDIDATE-REMOTE-MAIN": "restore remote main authority and rerun",
    "BFR-CANDIDATE-PUBLICATION-BASE": "regenerate the candidate from current authorized remote main",
    "BFR-CANDIDATE-POST-TRANSITION-DRIFT": "replace the candidate history from current authorized remote main",
    "BFR-CANDIDATE-WORKTREE": "commit or remove local changes and rerun at the reviewed head",
    "BFR-ACTIVATION-TRANSITION": "create exactly one first-parent pending-to-active transition",
}


def activation_candidate_failure_context(
    root: Path,
    release: str,
    issues: tuple[ValidationIssue, ...],
) -> dict[str, object]:
    """Return bounded, non-authorizing context for a failed candidate check."""

    data, _ = _activation_data(root / ACTIVATION_RECORD)
    transition, _ = _activation_transition(root)
    publication_base = "-"
    remote_tag_present = False
    remote_available = False
    try:
        advertisement = subprocess.run(
            [
                "git", "ls-remote", "--refs", "origin",
                "refs/heads/main", f"refs/tags/{ACTIVATION_CANDIDATE_RELEASE}",
            ],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        remote_available = True
        refs = {
            ref: identity
            for line in advertisement
            if "\t" in line
            for identity, ref in (line.split("\t", 1),)
        }
        publication_base = refs.get("refs/heads/main", "-")
        remote_tag_present = f"refs/tags/{ACTIVATION_CANDIDATE_RELEASE}" in refs
    except (OSError, subprocess.CalledProcessError):
        pass
    local_tag_present = _git_ref_exists(
        root,
        f"refs/tags/{ACTIVATION_CANDIDATE_RELEASE}",
    )
    tag_state = (
        "local-present"
        if local_tag_present
        else "remote-present"
        if remote_tag_present
        else "absent"
        if remote_available
        else "unknown"
    )
    actions = sorted(
        {
            _CANDIDATE_CORRECTIVE_ACTIONS.get(
                issue.code,
                "correct the named invariant and rerun candidate validation",
            )
            for issue in issues
        }
    )
    safe_release = (
        release
        if re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", release)
        else _redacted_value(release)
    )
    rollback = str(data.get("rollback_release", "-")) if data is not None else "-"
    safe_rollback = (
        rollback
        if rollback == "-" or re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", rollback)
        else _redacted_value(rollback)
    )
    return {
        "status": "failed",
        "mode": "activation-candidate",
        "publication_state": "candidate-invalid-unpublished",
        "candidate_release": safe_release,
        "publication_base": publication_base,
        "grandfathering_baseline": transition[1] if transition else "-",
        "transition_commit": transition[0] if transition else "-",
        "candidate_validation_head": _git_identity(root, "HEAD") or "-",
        "rollback_release": safe_rollback,
        "tag_state": tag_state,
        "corrective_actions": actions,
    }


def _changed_spec_path(
    root: Path,
    relative_path: str,
) -> tuple[Path | None, ValidationIssue | None]:
    if (
        not relative_path
        or "\\" in relative_path
        or PurePosixPath(relative_path).is_absolute()
        or ".." in PurePosixPath(relative_path).parts
        or not re.fullmatch(r"specs/[^/]+(?:\.test)?\.md", relative_path)
        or relative_path == "specs/README.md"
    ):
        return None, _issue(
            "BFR-INVALID-CHANGED-PATH",
            "<changed-spec-path>",
            "changed path must be a repository-relative top-level feature or test spec",
            relative_path,
            "specs/<name>.md or specs/<name>.test.md",
        )
    specs_issue = _specs_root_issue(root)
    if specs_issue:
        return None, specs_issue
    resolved_root = root.resolve()
    candidate = root / relative_path
    resolved_candidate = candidate.resolve(strict=False)
    resolved_specs_root = (resolved_root / "specs").resolve(strict=False)
    if (
        candidate.is_symlink()
        or not resolved_candidate.is_relative_to(resolved_root)
        or resolved_candidate.parent != resolved_specs_root
    ):
        return None, _issue(
            "BFR-CHANGED-PATH-ESCAPE",
            "<changed-spec-path>",
            "changed spec path resolves outside the repository",
            relative_path,
            "repository-contained path",
        )
    return candidate, None


def validate_changed_spec(root: Path, relative_path: str) -> tuple[ValidationIssue, ...]:
    path, path_issue = _changed_spec_path(root, relative_path)
    if path_issue:
        return (path_issue,)
    assert path is not None
    activation_path, activation_path_issue = _fixed_authoritative_path(
        root,
        ACTIVATION_RECORD,
    )
    if activation_path_issue:
        return (activation_path_issue,)
    assert activation_path is not None
    activation, parse_issue = _activation_data(activation_path)
    if parse_issue or activation is None:
        return (parse_issue,) if parse_issue else ()
    is_test_spec = relative_path.endswith(".test.md")
    feature_relative = (
        relative_path.removesuffix(".test.md") + ".md"
        if is_test_spec
        else relative_path
    )
    proof_relative = feature_relative.removesuffix(".md") + ".test.md"
    feature_path, feature_path_issue = _changed_spec_path(root, feature_relative)
    if feature_path_issue:
        return (feature_path_issue,)
    proof_path, proof_path_issue = _changed_spec_path(root, proof_relative)
    if proof_path_issue:
        return (proof_path_issue,)
    assert feature_path is not None and proof_path is not None
    if not feature_path.is_file():
        if proof_path.is_file():
            return (
                _issue(
                    "BFR-FEATURE-CONTRACT-MISSING",
                    feature_relative,
                    "test spec has no governing feature spec",
                    "-",
                    "matching feature spec",
                ),
            )
        return ()
    feature_text = feature_path.read_text(encoding="utf-8")
    marker = _line_value(_live_markdown(feature_text), "boundary_contract")
    state = activation.get("state")
    grandfathered = {
        item
        for item in activation.get("grandfathered_specs", [])
        if isinstance(item, str)
    }
    if state == "pending" and marker is not None:
        return (_issue("BFR-MARKER-INACTIVE", feature_relative, "marker is forbidden while activation is inactive", marker, "-"),)
    if state == "active" and feature_relative not in grandfathered and marker != METHOD_VERSION:
        return (_issue("BFR-NEW-SPEC-MARKER", feature_relative, "new feature spec requires active boundary marker", marker, METHOD_VERSION),)
    if (
        state == "active"
        and feature_relative in grandfathered
        and marker is None
    ):
        if is_test_spec:
            return ()
        return (_issue("BFR-GRANDFATHERED-REVIEW", feature_relative, "changed grandfathered spec requires spec-review classification", "-", "semantic spec-review"),)
    if marker == METHOD_VERSION:
        issues = list(validate_feature_record(feature_text, feature_relative))
        if not proof_path.is_file():
            issues.append(
                _issue(
                    "BFR-PROOF-MAP-MISSING",
                    proof_relative,
                    "adopting feature spec requires a matching proof map",
                    "-",
                    "matching test spec",
                )
            )
        else:
            issues.extend(
                validate_proof_map(
                    proof_path.read_text(encoding="utf-8"),
                    feature_text,
                    proof_relative,
                )
            )
        return tuple(issues)
    return ()
