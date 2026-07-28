#!/usr/bin/env python3
"""Deterministic boundary-first record and activation validation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from boundary_first_reference import (
    CANONICAL_REFERENCE,
    GOVERNED_SKILLS,
    METHOD_VERSION,
    ProjectionContractError,
    inventory_digest,
    project_reference,
    raw_sha256,
)


ACTIVATION_RECORD = Path("specs/boundary-first-activation.yaml")
PROOF_MODEL_SPEC = Path("specs/boundary-first-proof-model.md")
ACTIVATION_STATES = frozenset({"pending", "active", "rolled-back"})
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
        "activated_at",
        "canonical_reference",
        "canonical_reference_sha256",
        "grandfathered_specs",
        "grandfathered_inventory_sha256",
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


def _historical_spec_path(
    root: Path,
    relative_path: str,
) -> tuple[Path | None, ValidationIssue | None]:
    if not re.fullmatch(r"specs/[^/]+\.md", relative_path):
        return None, _issue(
            "BFR-GRANDFATHERED-PATH-UNSAFE",
            "<grandfathered-spec-path>",
            "historical path is not a top-level feature spec",
            relative_path,
            "specs/<name>.md",
        )
    specs_issue = _specs_root_issue(root)
    if specs_issue:
        return None, specs_issue
    candidate = root / relative_path
    resolved_specs = (root / "specs").resolve()
    resolved_candidate = candidate.resolve(strict=False)
    if (
        candidate.is_symlink()
        or resolved_candidate.parent != resolved_specs
    ):
        return None, _issue(
            "BFR-GRANDFATHERED-PATH-UNSAFE",
            relative_path,
            "historical spec path must be repository-contained and non-symlink",
            relative_path,
            "repository-owned regular file",
        )
    return candidate, None


def _eligible_grandfathered_specs(
    root: Path,
) -> tuple[tuple[str, ...], tuple[ValidationIssue, ...]]:
    eligible: list[str] = []
    issues: list[ValidationIssue] = []
    specs_issue = _specs_root_issue(root)
    if specs_issue:
        return (), (specs_issue,)
    specs_root = root / "specs"
    if not specs_root.is_dir():
        return (), ()
    for path in sorted(specs_root.glob("*.md")):
        relative = path.relative_to(root).as_posix()
        if path.name == "README.md" or path.name.endswith(".test.md"):
            continue
        safe_path, path_issue = _historical_spec_path(root, relative)
        if path_issue:
            issues.append(path_issue)
            continue
        assert safe_path is not None
        text = safe_path.read_text(encoding="utf-8")
        if _lifecycle_status(text) not in {"accepted", "approved", "active"}:
            continue
        if _line_value(_live_markdown(text), "boundary_contract") is not None:
            continue
        eligible.append(relative)
    return tuple(eligible), tuple(issues)


def validate_activation(root: Path) -> tuple[ValidationIssue, ...]:
    specs_issue = _specs_root_issue(root)
    if specs_issue:
        return (specs_issue,)
    record_path = root / ACTIVATION_RECORD
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

    spec_path = root / PROOF_MODEL_SPEC
    spec_state = None
    if spec_path.is_file():
        spec_state = _line_value(spec_path.read_text(encoding="utf-8"), "Boundary-first contract activation")
    if spec_state != state:
        issues.append(_issue("BFR-ACTIVATION-STATE-MISMATCH", PROOF_MODEL_SPEC.as_posix(), "activation YAML and authoritative spec state differ", state, spec_state))

    expected_source = data.get("canonical_reference")
    if expected_source != CANONICAL_REFERENCE.as_posix():
        issues.append(_issue("BFR-CANONICAL-PATH", ACTIVATION_RECORD.as_posix(), "canonical reference path differs", expected_source, CANONICAL_REFERENCE.as_posix()))
    try:
        projection_result = project_reference(root, mode="check")
    except ProjectionContractError as exc:
        projection_result = None
        issues.append(
            _issue(
                "BFR-PROJECTION-PATH",
                CANONICAL_REFERENCE.as_posix(),
                "canonical or governed projection path is unsafe",
                str(exc),
                "repository-contained non-symlink paths",
            )
        )
    if projection_result is not None:
        actual_source_hash = projection_result.source_sha256
        if data.get("canonical_reference_sha256") != actual_source_hash:
            issues.append(_issue("BFR-CANONICAL-HASH", CANONICAL_REFERENCE.as_posix(), "canonical reference hash differs", data.get("canonical_reference_sha256"), actual_source_hash))
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

    grandfathered = data.get("grandfathered_specs")
    if not isinstance(grandfathered, list):
        issues.append(_issue("BFR-GRANDFATHERED-SHAPE", ACTIVATION_RECORD.as_posix(), "grandfathered_specs must be a list", type(grandfathered).__name__, "list"))
    else:
        records: dict[str, str] = {}
        preserved_marked: set[str] = set()
        previous = ""
        for item in grandfathered:
            if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
                issues.append(_issue("BFR-GRANDFATHERED-ENTRY", ACTIVATION_RECORD.as_posix(), "grandfathered entry must contain path and sha256", item, "path and sha256"))
                continue
            item_path = item.get("path")
            item_hash = item.get("sha256")
            if not isinstance(item_path, str) or not isinstance(item_hash, str) or not SHA256_RE.fullmatch(item_hash):
                issues.append(_issue("BFR-GRANDFATHERED-ENTRY", ACTIVATION_RECORD.as_posix(), "grandfathered entry values are invalid", item, "spec path and sha256"))
                continue
            if (
                item_path <= previous
                or not re.fullmatch(r"specs/[^/]+\.md", item_path)
                or item_path.endswith(".test.md")
                or item_path == "specs/README.md"
            ):
                issues.append(_issue("BFR-GRANDFATHERED-ORDER", ACTIVATION_RECORD.as_posix(), "grandfathered paths must be sorted unique top-level feature specs", item_path, "sorted specs/*.md"))
            previous = item_path
            records[item_path] = item_hash
            grandfathered_path, grandfathered_path_issue = _historical_spec_path(
                root,
                item_path,
            )
            if grandfathered_path_issue:
                issues.append(grandfathered_path_issue)
                continue
            assert grandfathered_path is not None
            if not grandfathered_path.is_file():
                issues.append(_issue("BFR-GRANDFATHERED-MISSING", item_path, "grandfathered spec is missing", "-", "file with recorded raw-byte identity"))
            else:
                current_text = grandfathered_path.read_text(encoding="utf-8")
                current_marker = _line_value(
                    _live_markdown(current_text),
                    "boundary_contract",
                )
                if current_marker == METHOD_VERSION:
                    if _lifecycle_status(current_text) not in {
                        "accepted",
                        "approved",
                        "active",
                    }:
                        issues.append(
                            _issue(
                                "BFR-GRANDFATHERED-REVISION-STATUS",
                                item_path,
                                "marked historical revision must have an accepted lifecycle status",
                                _lifecycle_status(current_text),
                                "accepted, approved, or active",
                            )
                        )
                    else:
                        preserved_marked.add(item_path)
                    issues.extend(validate_feature_record(current_text, item_path))
                    proof_relative = item_path.removesuffix(".md") + ".test.md"
                    proof_path, proof_path_issue = _changed_spec_path(
                        root,
                        proof_relative,
                    )
                    if proof_path_issue:
                        issues.append(proof_path_issue)
                    elif proof_path is None or not proof_path.is_file():
                        issues.append(
                            _issue(
                                "BFR-PROOF-MAP-MISSING",
                                proof_relative,
                                "marked historical revision requires a matching proof map",
                                "-",
                                "matching test spec",
                            )
                        )
                    else:
                        issues.extend(
                            validate_proof_map(
                                proof_path.read_text(encoding="utf-8"),
                                current_text,
                                proof_relative,
                            )
                        )
                elif item_path == PROOF_MODEL_SPEC.as_posix() and state == "rolled-back":
                    pass
                else:
                    actual_hash = raw_sha256(grandfathered_path.read_bytes())
                    if actual_hash != item_hash:
                        issues.append(_issue("BFR-GRANDFATHERED-STALE", item_path, "grandfathered spec bytes differ from activation baseline", actual_hash, item_hash))
        actual_inventory = inventory_digest(records)
        if data.get("grandfathered_inventory_sha256") != actual_inventory:
            issues.append(_issue("BFR-GRANDFATHERED-HASH", ACTIVATION_RECORD.as_posix(), "grandfathered inventory identity differs", data.get("grandfathered_inventory_sha256"), actual_inventory))
        if state in {"active", "rolled-back"}:
            actual_membership = tuple(records)
            eligible_membership, eligibility_issues = _eligible_grandfathered_specs(root)
            issues.extend(eligibility_issues)
            expected_membership = tuple(
                sorted(set(eligible_membership) | preserved_marked)
            )
            if actual_membership != expected_membership:
                issues.append(
                    _issue(
                        "BFR-GRANDFATHERED-MEMBERSHIP",
                        ACTIVATION_RECORD.as_posix(),
                        "grandfathered inventory does not match lifecycle-eligible historical specs",
                        actual_membership,
                        expected_membership,
                    )
                )

    activated_at = data.get("activated_at")
    if state in {"active", "rolled-back"} and not isinstance(activated_at, str):
        issues.append(_issue("BFR-ACTIVATED-AT", ACTIVATION_RECORD.as_posix(), "active or rolled-back record preserves activation time", activated_at, "timestamp"))
    if state == "pending" and activated_at is not None:
        issues.append(_issue("BFR-ACTIVATED-AT", ACTIVATION_RECORD.as_posix(), "pending record must use null activation time", activated_at, "null"))
    return tuple(issues)


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
    activation, parse_issue = _activation_data(root / ACTIVATION_RECORD)
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
        item["path"]
        for item in activation.get("grandfathered_specs", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    if state == "pending" and marker is not None:
        return (_issue("BFR-MARKER-INACTIVE", feature_relative, "marker is forbidden while activation is inactive", marker, "-"),)
    if (
        state == "rolled-back"
        and marker is not None
        and _lifecycle_status(feature_text) not in {"accepted", "approved", "active"}
    ):
        return (_issue("BFR-MARKER-INACTIVE", feature_relative, "rollback preserves only already accepted marked artifacts", marker, "accepted marked artifact"),)
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
