#!/usr/bin/env python3
"""Deterministic model and explicitly selected feature/proof validation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from model_layout import PROJECT_MODEL_PATHS

from boundary_first_reference import METHOD_VERSION


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


def _stage_owned_marker_authority(
    root: Path | None, change_record: str, path: str,
) -> tuple[None, ValidationIssue]:
    # This was a legacy stored-state adapter, not part of the independent
    # boundary document grammar. Never read or reinterpret its archived root.
    return None, _issue(
        "BFR-MARKER-AUTHORITY", path,
        "legacy stored-record marker authority is unsupported",
        "retired-record-interface", "standalone document or current model contract",
    )


def _marker_issues(
    text: str,
    path: str,
    root: Path | None = None,
) -> list[ValidationIssue]:
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
    owner = _section(text, "Owning change record")
    owner_markers = tuple(marker_pattern.finditer(owner))
    owner_pointer_pattern = re.compile(
        r"(?m)^`(docs/changes/[^/]+/change\.yaml)`\s*$"
    )
    owner_pointers = tuple(owner_pointer_pattern.finditer(owner))
    # V2 ownership pointers are document placement, not stored eligibility.
    # The record validator and independent reviewer assess the selected store
    # and authority separately; never decode an archive to validate this form.
    v2_pointers = tuple(re.finditer(
        r"(?m)^`docs/changes/[A-Za-z0-9][A-Za-z0-9._-]*/change\.json`\s*$", owner,
    ))
    if v2_pointers:
        if len(v2_pointers) != 1 or owner_pointers or len(owner_markers) != 1:
            return [_issue("BFR-MARKER-PLACEMENT", path,
                "v2 document marker requires one exact owning pointer",
                "ambiguous-owner", "one v2 owner followed by one marker")]
        preceding = owner[:owner_markers[0].start()].strip().splitlines()
        if preceding and preceding[-1].strip() == v2_pointers[0].group(0).strip():
            return []
        return [_issue("BFR-MARKER-PLACEMENT", path,
            "boundary contract marker must follow the v2 owning pointer",
            "misplaced-marker", "after normalized v2 owning pointer")]
    stage_owned = False
    if len(owner_pointers) == 1:
        stage_owned_result, authority_issue = _stage_owned_marker_authority(
            root,
            owner_pointers[0].group(1),
            path,
        )
        if authority_issue:
            return [authority_issue]
        stage_owned = isinstance(stage_owned_result, str)
    elif len(owner_pointers) > 1:
        return [
            _issue(
                "BFR-MARKER-AUTHORITY",
                path,
                "feature spec must identify exactly one owning change record",
                len(owner_pointers),
                1,
            )
        ]
    if len(status_markers) != 1 and len(owner_markers) != 1:
        return [
            _issue(
                "BFR-MARKER-PLACEMENT",
                path,
                "boundary contract marker must follow lifecycle status or the owning change pointer",
                "outside-governed-metadata",
                "after lifecycle status value or normalized owning change pointer",
            )
        ]
    if len(owner_markers) == 1:
        preceding_owner_lines = [
            line.strip()
            for line in owner[: owner_markers[0].start()].splitlines()
            if line.strip() and not line.lstrip().startswith("<!--")
        ]
        if preceding_owner_lines and re.fullmatch(
            r"`docs/changes/[^/]+/change\.yaml`",
            preceding_owner_lines[-1],
        ):
            if stage_owned:
                return []
            return [
                _issue(
                    "BFR-MARKER-AUTHORITY",
                    path,
                    "owner-pointer marker placement requires the stage-owned lifecycle contract",
                    "non-stage-owned-contract",
                    "lifecycle_contract: stage-owned-change-local-v1",
                )
            ]
        return [
            _issue(
                "BFR-MARKER-PLACEMENT",
                path,
                "boundary contract marker must follow the normalized owning change pointer",
                "before-owner-pointer",
                "after normalized owning change pointer",
            )
        ]
    if stage_owned:
        return [
            _issue(
                "BFR-MARKER-PLACEMENT",
                path,
                "stage-owned feature specs must place the marker after the owning change pointer",
                "status-marker-for-stage-owned-contract",
                "owner-pointer marker form",
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
    *,
    root: Path | None = None,
) -> tuple[ValidationIssue, ...]:
    text = _live_markdown(text)
    vocabulary: list[ValidationIssue] = []
    marker_structure = _marker_issues(text, path, root)
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
        cited_owner_requirements = {
            requirement_id
            for boundary_id in boundary_ids
            if (definition := boundary_rows.get(boundary_id)) is not None
            for requirement_id in _split_ids(definition[2])
        }
        cited_without_overlap = [
            boundary_id
            for boundary_id in boundary_ids
            if (definition := boundary_rows.get(boundary_id)) is not None
            and example_requirements.isdisjoint(_split_ids(definition[2]))
        ]
        if cited_without_overlap:
            issues.append(_issue("BFR-EXAMPLE-OWNER-MISMATCH", path, "each cited boundary must govern at least one example requirement", requirements, ", ".join(sorted(cited_owner_requirements))))
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
    *,
    feature_path: str = "<feature-record>",
    root: Path | None = None,
) -> tuple[ValidationIssue, ...]:
    feature_issues = validate_feature_record(
        feature_text,
        feature_path,
        root=root,
    )
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


MODEL_DIMENSIONS = (
    "Input domain", "State/lifecycle", "Identity/authority", "Composition/path",
    "Temporal/retry", "Failure/recovery", "Compatibility/migration", "External/environment",
)


def validate_model_record(text: str, path: str) -> tuple[ValidationIssue, ...]:
    """Explicit model format: structural proof only, never workflow settlement."""
    text = _live_markdown(re.sub(r"<!--[\s\S]*?(?:-->|$)", "", text))
    markers = re.findall(r"^Model validation contract:\s*(.*?)\s*$", text, re.MULTILINE)
    if markers != ["model-document-v1"]:
        return (_issue("BFR-MODEL-CONTRACT", path, "exactly one model-document-v1 model contract marker is required", markers),)

    def table(heading: str, columns: tuple[str, ...]) -> list[list[str]]:
        # Four columns (including tabs) are code, not authoritative structure.
        # Normalize only ordinary indentation; leave the historical parser alone.
        lines = ["" if line.expandtabs(4).startswith("    ") else line.strip()
                 for line in text.splitlines()]
        positions = [i for i, line in enumerate(lines) if line == heading]
        if len(positions) != 1:
            raise ValueError("one required heading is required")
        body = []
        for line in lines[positions[0] + 1:]:
            if line.startswith("#"):
                break
            body.append(line)
        starts = [i for i, line in enumerate(body) if line.startswith("|") and (i == 0 or not body[i-1].startswith("|"))]
        if len(starts) != 1:
            raise ValueError("one table is required")
        rows = []
        for line in body[starts[0]:]:
            if not line.startswith("|"):
                break
            if not line.endswith("|"):
                raise ValueError("table row is not closed")
            row = [cell.strip() for cell in line[1:-1].split("|")]
            if len(row) != len(columns):
                raise ValueError("table row has wrong width")
            rows.append(row)
        if len(rows) < 3 or tuple(rows[0]) != columns or any(not re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
            raise ValueError("table header, separator or body is invalid")
        return rows[2:]

    try:
        requirements = table("## Requirements", ("ID", "Required behavior"))
        scenarios = table("### Boundary scan and acceptance scenarios", ("Dimension", "Requirement basis", "Distinct outcome to demonstrate"))
    except ValueError as error:
        return (_issue("BFR-MODEL-TABLE", path, str(error)),)
    ids = [row[0] for row in requirements]
    if len(ids) != len(set(ids)) or any(not STABLE_ID_RE.fullmatch(row[0]) or not row[1] for row in requirements):
        return (_issue("BFR-MODEL-REQUIREMENTS", path, "requirement IDs must be unique and valid with nonempty text"),)
    dimensions = [row[0] for row in scenarios]
    # Closed vocabulary is checked before dependent reference/consistency rules.
    if len(dimensions) != len(MODEL_DIMENSIONS) or set(dimensions) != set(MODEL_DIMENSIONS):
        return (_issue("BFR-MODEL-DIMENSIONS", path, "exactly one row for each known model dimension is required", dimensions),)
    for _, basis, outcome in scenarios:
        if basis == "-":
            if not outcome.startswith("Not applicable:") or not outcome.removeprefix("Not applicable:").strip():
                return (_issue("BFR-MODEL-APPLICABILITY", path, "non-applicability requires a reason"),)
        else:
            refs = basis.split(", ")
            if len(refs) != len(set(refs)) or not set(refs).issubset(ids) or not outcome or outcome.startswith("Not applicable:"):
                return (_issue("BFR-MODEL-REFERENCES", path, "applicable rows require unique local requirement references and an outcome"),)
    return ()


def validate_model_path(root: Path, relative_path: str) -> tuple[ValidationIssue, ...]:
    if relative_path not in PROJECT_MODEL_PATHS.values() and not re.fullmatch(r"docs/design/(?P<model>[a-z0-9][a-z0-9-]{0,79})(?:/(?P=model))?\.md", relative_path):
        return (_issue("BFR-MODEL-PATH", "<model-path>", "invalid model path", relative_path),)
    root = root.resolve()
    path = root
    try:
        for part in PurePosixPath(relative_path).parts:
            path = path / part
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                return (_issue("BFR-MODEL-PATH", "<model-path>", "model path must not traverse symlinks", relative_path),)
        if not path.is_file():
            return (_issue("BFR-MODEL-PATH", relative_path, "model must be an existing regular file"),)
        return validate_model_record(path.read_text(encoding="utf-8"), relative_path)
    except (OSError, UnicodeError, RuntimeError):
        return (_issue("BFR-MODEL-READ", relative_path, "model file cannot be safely read"),)


def validate_changed_spec(root: Path, relative_path: str) -> tuple[ValidationIssue, ...]:
    if relative_path.startswith("docs/design/"):
        return validate_model_path(root, relative_path)
    path, path_issue = _changed_spec_path(root, relative_path)
    if path_issue:
        return (path_issue,)
    assert path is not None
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
    live_feature = _live_markdown(feature_text)
    marker = _line_value(live_feature, "boundary_contract")
    if marker is not None and marker != METHOD_VERSION:
        return (_issue("BFR-UNKNOWN-CONTRACT-VERSION", feature_relative, "unknown boundary contract", marker, METHOD_VERSION),)
    if marker is None:
        # A partial adoption is malformed content, not an unmarked historical
        # document awaiting substantive classification. Ignore code examples.
        if re.search(r"(?m)^boundary_contract:", live_feature) or any(
            heading in _level_two_headings(live_feature) for heading in FEATURE_HEADINGS
        ):
            return validate_feature_record(feature_text, feature_relative, root=root)
        issues = [_issue("BFR-ADOPTION-REVIEW", feature_relative, "unmarked feature requires independent Design Review adoption classification", "-", "semantic design-review")]
        if is_test_spec and proof_path.is_file():
            proof = _live_markdown(proof_path.read_text(encoding="utf-8"))
            if re.search(r"(?m)^(?:boundary_contract:|Boundary model (?:version|scope):|## Proof map(?:\s|$))", proof):
                # A claimed proof record cannot be checked against an unadopted
                # feature. Report the structural gap as well as its decision owner.
                issues.append(_issue("BFR-PROOF-FEATURE-UNADOPTED", proof_relative, "proof record requires a structurally valid governing feature record"))
        return tuple(issues)
    if marker == METHOD_VERSION:
        issues = list(
            validate_feature_record(
                feature_text,
                feature_relative,
                root=root,
            )
        )
        if issues:
            return tuple(issues)
        # V2 allocates proof in the reviewed delivery plan. Document validation
        # checks the feature grammar only; it must not recreate a retired
        # test-spec requirement or derive delivery approval from an owner path.
        if not is_test_spec and re.search(r"(?m)^`docs/changes/[A-Za-z0-9][A-Za-z0-9._-]*/change\.json`\s*$",
                     _section(live_feature, "Owning change record")):
            return tuple(issues)
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
                    feature_path=feature_relative,
                    root=root,
                )
            )
        return tuple(issues)
    return ()


def validate_repository_examples(root: Path) -> tuple[tuple[str, ...], tuple[ValidationIssue, ...]]:
    """Check model-document examples and JSON syntax in declared owned namespaces.

    Complete stored records and request/result semantics retain their schema and
    interaction checks in the model example suites; syntax never grants approval.
    """
    checked = []
    issues = []
    for namespace in ("docs/design/cli/examples", "docs/design/skill/examples/workflow"):
        base = root / namespace
        if any(parent.is_symlink() for parent in (base, *base.parents) if parent != root):
            issues.append(_issue("BFR-EXAMPLE-PATH", namespace, "example namespace must not traverse symlinks"))
            continue
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                issues.append(_issue("BFR-EXAMPLE-PATH", relative, "example must not be a symlink"))
            elif path.is_file() and path.suffix == ".json":
                checked.append(relative)
                try:
                    json.loads(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, ValueError):
                    issues.append(_issue("BFR-EXAMPLE-JSON", relative, "example must be readable valid JSON"))
    # The authoring model owns the portable model-document worked example.
    relative = PROJECT_MODEL_PATHS["design"]
    if not validate_model_path(root, relative):
        text = (root / relative).read_text(encoding="utf-8")
        for index, (_, example) in enumerate(re.findall(r"^(`{3,})markdown\n([\s\S]*?)^\1[ \t]*$", text, re.MULTILINE)):
            if "Model validation contract:" in example:
                label = f"{relative}#model-example-{index + 1}"
                checked.append(label)
                issues.extend(validate_model_record(example, label))
    return tuple(checked), tuple(issues)
