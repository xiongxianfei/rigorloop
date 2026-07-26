#!/usr/bin/env python3
"""Immutable executable projection of the boundary-first proof contract.

The approved workflow and skill specifications remain normative.  This module
implements only deterministic shape, vocabulary, traceability, and aggregate
rules.  It deliberately does not judge semantic completeness, applicability,
partition quality, interaction sufficiency, or review reasoning.
"""

from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


CORE_DIMENSION_IDS = (
    "canonical-trust",
    "identity-freshness",
    "closed-vocabulary",
    "state-transition",
    "authorization-scope",
    "mutation-atomicity",
    "interruption-recovery",
    "concurrency-idempotency",
    "composition-bypass",
    "compatibility-migration",
    "outcome-stop",
    "evidence-claims",
)
APPLICABILITY_VALUES = ("applicable", "not-applicable")
EXAMPLE_ROLES = ("illustration", "regression", "discovery", "non-normative")
INTERACTION_RATIONALES = (
    "state-coupling",
    "trust-or-authority",
    "mutation-or-recovery",
    "compatibility-or-migration",
    "composed-path",
    "incident-evidence",
)
BOUNDARY_MODEL_VERSIONS = ("legacy", "v1")
AUTOMATION_LEVELS = ("automated", "manual", "hybrid")
RESULT_VALUES = ("pass", "fail", "not-run")
EXPECTED_GATES = ("spec", "spec-review", "test-spec", "test-spec-review", "implement")
DETECTED_STAGES = (*EXPECTED_GATES, "not-detected")
EVALUATED_SKILLS = (
    "spec",
    "spec-review",
    "test-spec",
    "test-spec-review",
    "implement",
    "code-review",
    "verify",
    "workflow",
)
CHECK_IDS = (
    "boundary-workflow-contract",
    "boundary-skill-contract",
    "boundary-traceability",
    "boundary-incident-replay",
    "boundary-adapter-parity",
    "boundary-capability-baseline",
)
FIXTURE_GATES = {
    "BFP-FX-CANONICAL-001": "spec-review",
    "BFP-FX-VOCAB-001": "test-spec-review",
    "BFP-FX-TRANSITION-001": "test-spec-review",
    "BFP-FX-IDENTITY-001": "test-spec-review",
    "BFP-FX-ATOMICITY-001": "test-spec-review",
    "BFP-FX-RECOVERY-001": "test-spec-review",
    "BFP-FX-COMPOSITION-001": "test-spec-review",
    "BFP-FX-SIBLING-001": "implement",
}
PRESERVATION_KEYS = (
    "behavior",
    "claim-boundary",
    "review-recording",
    "isolation",
    "handoff",
)
CAPABILITY_REPORT_SCHEMA = "boundary-capability-baseline-v1"

STABLE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")
EXTENSION_ID_RE = re.compile(r"^x\.[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")
TEST_ID_RE = re.compile(r"^T[1-9][0-9]*$")
SCOPE_RE = re.compile(r"^(?:whole-spec|[A-Za-z][A-Za-z0-9]*-[A-Za-z][A-Za-z0-9]*)$")

CORE_FIELDS = frozenset(
    {
        "dimension_id",
        "applicability",
        "governing_requirement_ids",
        "boundary_ids",
        "non_applicability_rationale",
    }
)
EXTENSION_FIELDS = frozenset(
    {
        "extension_id",
        "title",
        "applicability",
        "rationale",
        "governing_requirement_ids",
        "boundary_ids",
        "non_applicability_rationale",
    }
)
EXAMPLE_FIELDS = frozenset(
    {
        "example_id",
        "role",
        "governing_requirement_ids",
        "boundary_ids",
        "regression_id",
        "discovery_gap",
        "non_normative_purpose",
    }
)
INTERACTION_FIELDS = frozenset(
    {
        "interaction_id",
        "boundary_ids",
        "rationale",
        "governing_requirement_ids",
    }
)
PROOF_FIELDS = frozenset(
    {
        "proof_obligation_id",
        "governing_requirement_ids",
        "boundary_or_interaction_ids",
        "test_case_ids",
        "automation_level",
        "manual_procedure_ids",
    }
)
REPORT_FIELDS = frozenset(
    {
        "schema_version",
        "boundary_model_version",
        "evaluated_skills",
        "required_check_ids",
        "checks",
        "fixtures",
        "preservation_results",
        "adapter_parity",
        "false_blocking_count",
        "duplicate_normative_owner_count",
        "new_universal_artifact_count",
        "simple_fixture_structure_correction_cycles",
        "overall_result",
    }
)


class BoundaryProofError(ValueError):
    """Raised when deterministic boundary-proof validation fails."""


@dataclass(frozen=True)
class CoreBoundaryEntry:
    dimension_id: str
    applicability: str
    governing_requirement_ids: tuple[str, ...]
    boundary_ids: tuple[str, ...]
    non_applicability_rationale: str | None


@dataclass(frozen=True)
class BoundaryExtension:
    extension_id: str
    title: str
    applicability: str
    rationale: str
    governing_requirement_ids: tuple[str, ...]
    boundary_ids: tuple[str, ...]
    non_applicability_rationale: str | None


@dataclass(frozen=True)
class BoundaryExample:
    example_id: str
    role: str
    governing_requirement_ids: tuple[str, ...]
    boundary_ids: tuple[str, ...]
    regression_id: str | None
    discovery_gap: str | None
    non_normative_purpose: str | None


@dataclass(frozen=True)
class BoundaryInteraction:
    interaction_id: str
    boundary_ids: tuple[str, ...]
    rationale: str
    governing_requirement_ids: tuple[str, ...]


@dataclass(frozen=True)
class FeatureBoundaryModel:
    boundary_model_version: str
    boundary_model_scope: str
    core_dimensions: tuple[CoreBoundaryEntry, ...]
    extensions: tuple[BoundaryExtension, ...]
    examples: tuple[BoundaryExample, ...]
    interactions: tuple[BoundaryInteraction, ...]


@dataclass(frozen=True)
class ProofObligation:
    proof_obligation_id: str
    governing_requirement_ids: tuple[str, ...]
    boundary_or_interaction_ids: tuple[str, ...]
    test_case_ids: tuple[str, ...]
    automation_level: str
    manual_procedure_ids: tuple[str, ...]


@dataclass(frozen=True)
class BoundaryProofMap:
    boundary_model_version: str
    boundary_model_scope: str
    proof_obligations: tuple[ProofObligation, ...]


def _object(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise BoundaryProofError(f"{label}: expected object")
    return value


def _records(value: Any, label: str) -> list[Mapping[str, Any]]:
    if not isinstance(value, list):
        raise BoundaryProofError(f"{label}: expected list")
    return [_object(item, f"{label}[{index}]") for index, item in enumerate(value)]


def _exact_fields(record: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    actual = set(record)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise BoundaryProofError(f"{label}: missing fields: {', '.join(missing)}")
    if extra:
        raise BoundaryProofError(f"{label}: unexpected fields: {', '.join(extra)}")


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BoundaryProofError(f"{label}: expected non-empty string")
    return value


def _optional_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    return _nonempty_string(value, label)


def _strings(
    value: Any,
    label: str,
    *,
    nonempty: bool,
    stable_ids: bool = False,
    test_ids: bool = False,
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise BoundaryProofError(f"{label}: expected list")
    if nonempty and not value:
        raise BoundaryProofError(f"{label}: expected one or more values")
    result: list[str] = []
    for index, item in enumerate(value):
        item = _nonempty_string(item, f"{label}[{index}]")
        if stable_ids and not STABLE_ID_RE.fullmatch(item):
            raise BoundaryProofError(f"{label}[{index}]: invalid stable ID")
        if test_ids and not (TEST_ID_RE.fullmatch(item) or STABLE_ID_RE.fullmatch(item)):
            raise BoundaryProofError(f"{label}[{index}]: invalid test-case ID")
        result.append(item)
    if len(result) != len(set(result)):
        raise BoundaryProofError(f"{label}: duplicate values")
    return tuple(result)


def _unknown_vocabulary_checks(model: Mapping[str, Any]) -> None:
    version = model.get("boundary_model_version")
    if version not in BOUNDARY_MODEL_VERSIONS:
        raise BoundaryProofError(f"unknown boundary-model version: {version!r}")
    for index, row in enumerate(_records(model.get("core_dimensions"), "core_dimensions")):
        dimension_id = row.get("dimension_id")
        if dimension_id not in CORE_DIMENSION_IDS:
            raise BoundaryProofError(
                f"core_dimensions[{index}]: unknown core dimension: {dimension_id!r}"
            )
        applicability = row.get("applicability")
        if applicability not in APPLICABILITY_VALUES:
            raise BoundaryProofError(
                f"core_dimensions[{index}]: unknown applicability: {applicability!r}"
            )
    for index, row in enumerate(_records(model.get("extensions", []), "extensions")):
        applicability = row.get("applicability")
        if applicability not in APPLICABILITY_VALUES:
            raise BoundaryProofError(
                f"extensions[{index}]: unknown applicability: {applicability!r}"
            )
    for index, row in enumerate(_records(model.get("examples", []), "examples")):
        role = row.get("role")
        if role not in EXAMPLE_ROLES:
            raise BoundaryProofError(
                f"examples[{index}]: unknown example role: {role!r}"
            )
    for index, row in enumerate(_records(model.get("interactions", []), "interactions")):
        rationale = row.get("rationale")
        if rationale not in INTERACTION_RATIONALES:
            raise BoundaryProofError(
                f"interactions[{index}]: unknown interaction rationale: {rationale!r}"
            )


def _applicability_values(
    row: Mapping[str, Any],
    label: str,
) -> tuple[tuple[str, ...], tuple[str, ...], str | None]:
    applicability = row["applicability"]
    requirements = _strings(
        row["governing_requirement_ids"],
        f"{label}.governing_requirement_ids",
        nonempty=applicability == "applicable",
    )
    boundaries = _strings(
        row["boundary_ids"],
        f"{label}.boundary_ids",
        nonempty=applicability == "applicable",
        stable_ids=True,
    )
    rationale = _optional_string(
        row["non_applicability_rationale"],
        f"{label}.non_applicability_rationale",
    )
    if applicability == "applicable":
        if rationale is not None:
            raise BoundaryProofError(
                f"{label}: applicable entry cannot have non-applicability rationale"
            )
    elif requirements or boundaries or rationale is None:
        raise BoundaryProofError(
            f"{label}: not-applicable entry requires rationale and no proof links"
        )
    return requirements, boundaries, rationale


def normalize_feature_model(payload: Mapping[str, Any]) -> FeatureBoundaryModel:
    """Validate and freeze one structured feature boundary model."""

    model = _object(payload, "feature_model")
    expected_top = {
        "boundary_model_version",
        "boundary_model_scope",
        "core_dimensions",
        "extensions",
        "examples",
        "interactions",
    }
    _exact_fields(model, frozenset(expected_top), "feature_model")
    _unknown_vocabulary_checks(model)
    version = _nonempty_string(model["boundary_model_version"], "boundary_model_version")
    scope = _nonempty_string(model["boundary_model_scope"], "boundary_model_scope")
    if not SCOPE_RE.fullmatch(scope):
        raise BoundaryProofError("boundary_model_scope: invalid closed scope")

    core: list[CoreBoundaryEntry] = []
    for index, row in enumerate(_records(model["core_dimensions"], "core_dimensions")):
        label = f"core_dimensions[{index}]"
        _exact_fields(row, CORE_FIELDS, label)
        requirements, boundaries, rationale = _applicability_values(row, label)
        core.append(
            CoreBoundaryEntry(
                row["dimension_id"],
                row["applicability"],
                requirements,
                boundaries,
                rationale,
            )
        )
    core_ids = [row.dimension_id for row in core]
    if len(core_ids) != len(set(core_ids)):
        raise BoundaryProofError("duplicate core dimension")
    missing = sorted(set(CORE_DIMENSION_IDS) - set(core_ids))
    if missing:
        raise BoundaryProofError("missing core dimensions: " + ", ".join(missing))

    extensions: list[BoundaryExtension] = []
    extension_ids: set[str] = set()
    for index, row in enumerate(_records(model["extensions"], "extensions")):
        label = f"extensions[{index}]"
        _exact_fields(row, EXTENSION_FIELDS, label)
        extension_id = _nonempty_string(row["extension_id"], f"{label}.extension_id")
        if extension_id == "other" or not EXTENSION_ID_RE.fullmatch(extension_id):
            raise BoundaryProofError(f"{label}: invalid extension ID")
        if extension_id in extension_ids:
            raise BoundaryProofError(f"{label}: duplicate extension ID")
        extension_ids.add(extension_id)
        requirements, boundaries, rationale = _applicability_values(row, label)
        extensions.append(
            BoundaryExtension(
                extension_id,
                _nonempty_string(row["title"], f"{label}.title"),
                row["applicability"],
                _nonempty_string(row["rationale"], f"{label}.rationale"),
                requirements,
                boundaries,
                rationale,
            )
        )

    all_boundary_ids = {
        boundary_id for entry in (*core, *extensions) for boundary_id in entry.boundary_ids
    }
    if len(all_boundary_ids) != sum(
        len(entry.boundary_ids) for entry in (*core, *extensions)
    ):
        raise BoundaryProofError("duplicate boundary ID")

    examples: list[BoundaryExample] = []
    example_ids: set[str] = set()
    for index, row in enumerate(_records(model["examples"], "examples")):
        label = f"examples[{index}]"
        _exact_fields(row, EXAMPLE_FIELDS, label)
        example_id = _nonempty_string(row["example_id"], f"{label}.example_id")
        if not STABLE_ID_RE.fullmatch(example_id):
            raise BoundaryProofError(f"{label}: invalid example ID")
        if example_id in example_ids:
            raise BoundaryProofError(f"{label}: duplicate example ID")
        example_ids.add(example_id)
        requirements = _strings(
            row["governing_requirement_ids"],
            f"{label}.governing_requirement_ids",
            nonempty=False,
        )
        boundaries = _strings(
            row["boundary_ids"],
            f"{label}.boundary_ids",
            nonempty=False,
            stable_ids=True,
        )
        orphan = sorted(set(boundaries) - all_boundary_ids)
        if orphan:
            raise BoundaryProofError(f"{label}: orphan boundary: {orphan[0]}")
        regression_id = _optional_string(row["regression_id"], f"{label}.regression_id")
        discovery_gap = _optional_string(row["discovery_gap"], f"{label}.discovery_gap")
        purpose = _optional_string(
            row["non_normative_purpose"], f"{label}.non_normative_purpose"
        )
        role = row["role"]
        if role == "illustration":
            if not requirements or not boundaries or any(
                value is not None for value in (regression_id, discovery_gap, purpose)
            ):
                raise BoundaryProofError(f"{label}: invalid illustration links")
        elif role == "regression":
            if not requirements or not boundaries or regression_id is None:
                raise BoundaryProofError(f"{label}: regression ID is required")
            if discovery_gap is not None or purpose is not None:
                raise BoundaryProofError(f"{label}: invalid regression links")
        elif role == "discovery":
            if requirements or boundaries or regression_id is not None or discovery_gap is None:
                raise BoundaryProofError(f"{label}: discovery gap is required")
        elif requirements or boundaries or regression_id is not None or discovery_gap is not None or purpose is None:
            raise BoundaryProofError(f"{label}: non-normative purpose is required")
        examples.append(
            BoundaryExample(
                example_id,
                role,
                requirements,
                boundaries,
                regression_id,
                discovery_gap,
                purpose,
            )
        )

    interactions: list[BoundaryInteraction] = []
    interaction_ids: set[str] = set()
    for index, row in enumerate(_records(model["interactions"], "interactions")):
        label = f"interactions[{index}]"
        _exact_fields(row, INTERACTION_FIELDS, label)
        interaction_id = _nonempty_string(
            row["interaction_id"], f"{label}.interaction_id"
        )
        if not STABLE_ID_RE.fullmatch(interaction_id):
            raise BoundaryProofError(f"{label}: invalid interaction ID")
        if interaction_id in interaction_ids:
            raise BoundaryProofError(f"{label}: duplicate interaction ID")
        interaction_ids.add(interaction_id)
        boundaries = _strings(
            row["boundary_ids"],
            f"{label}.boundary_ids",
            nonempty=True,
            stable_ids=True,
        )
        if len(boundaries) < 2:
            raise BoundaryProofError(f"{label}: at least two boundary IDs are required")
        orphan = sorted(set(boundaries) - all_boundary_ids)
        if orphan:
            raise BoundaryProofError(f"{label}: orphan boundary: {orphan[0]}")
        requirements = _strings(
            row["governing_requirement_ids"],
            f"{label}.governing_requirement_ids",
            nonempty=True,
        )
        interactions.append(
            BoundaryInteraction(
                interaction_id,
                boundaries,
                row["rationale"],
                requirements,
            )
        )

    return FeatureBoundaryModel(
        version,
        scope,
        tuple(core),
        tuple(extensions),
        tuple(examples),
        tuple(interactions),
    )


def normalize_proof_map(
    payload: Mapping[str, Any],
    feature: FeatureBoundaryModel,
) -> BoundaryProofMap:
    """Validate one proof map against an already-normalized feature model."""

    record = _object(payload, "proof_map")
    _exact_fields(
        record,
        frozenset(
            {
                "boundary_model_version",
                "boundary_model_scope",
                "proof_obligations",
            }
        ),
        "proof_map",
    )
    version = record["boundary_model_version"]
    if version not in BOUNDARY_MODEL_VERSIONS:
        raise BoundaryProofError(f"unknown boundary-model version: {version!r}")
    if version != feature.boundary_model_version:
        raise BoundaryProofError("boundary-model version mismatch")
    scope = _nonempty_string(record["boundary_model_scope"], "proof_map scope")
    if scope != feature.boundary_model_scope:
        raise BoundaryProofError("boundary-model scope mismatch")
    rows = _records(record["proof_obligations"], "proof_obligations")
    for index, row in enumerate(rows):
        level = row.get("automation_level")
        if level not in AUTOMATION_LEVELS:
            raise BoundaryProofError(
                f"proof_obligations[{index}]: unknown automation level: {level!r}"
            )

    boundary_ids = {
        boundary_id
        for entry in (*feature.core_dimensions, *feature.extensions)
        if entry.applicability == "applicable"
        for boundary_id in entry.boundary_ids
    }
    interaction_ids = {entry.interaction_id for entry in feature.interactions}
    known_ids = boundary_ids | interaction_ids
    known_requirements = {
        requirement
        for entry in (*feature.core_dimensions, *feature.extensions)
        for requirement in entry.governing_requirement_ids
    } | {
        requirement
        for entry in feature.interactions
        for requirement in entry.governing_requirement_ids
    }
    normalized: list[ProofObligation] = []
    proof_ids: set[str] = set()
    mapped_ids: set[str] = set()
    for index, row in enumerate(rows):
        label = f"proof_obligations[{index}]"
        _exact_fields(row, PROOF_FIELDS, label)
        proof_id = _nonempty_string(
            row["proof_obligation_id"], f"{label}.proof_obligation_id"
        )
        if not STABLE_ID_RE.fullmatch(proof_id):
            raise BoundaryProofError(f"{label}: invalid proof obligation ID")
        if proof_id in proof_ids:
            raise BoundaryProofError(f"{label}: duplicate proof obligation ID")
        proof_ids.add(proof_id)
        requirements = _strings(
            row["governing_requirement_ids"],
            f"{label}.governing_requirement_ids",
            nonempty=True,
        )
        unknown_requirements = sorted(set(requirements) - known_requirements)
        if unknown_requirements:
            raise BoundaryProofError(
                f"{label}: unapproved governing requirement: "
                + unknown_requirements[0]
            )
        references = _strings(
            row["boundary_or_interaction_ids"],
            f"{label}.boundary_or_interaction_ids",
            nonempty=True,
            stable_ids=True,
        )
        orphan = sorted(set(references) - known_ids)
        if orphan:
            raise BoundaryProofError(f"{label}: orphan boundary or interaction: {orphan[0]}")
        tests = _strings(
            row["test_case_ids"],
            f"{label}.test_case_ids",
            nonempty=True,
            test_ids=True,
        )
        manuals = _strings(
            row["manual_procedure_ids"],
            f"{label}.manual_procedure_ids",
            nonempty=False,
            stable_ids=True,
        )
        level = row["automation_level"]
        if level == "automated" and manuals:
            raise BoundaryProofError(f"{label}: automated proof cannot cite manual procedure")
        if level in {"manual", "hybrid"} and not manuals:
            raise BoundaryProofError(f"{label}: manual procedure is required")
        mapped_ids.update(references)
        normalized.append(
            ProofObligation(
                proof_id,
                requirements,
                references,
                tests,
                level,
                manuals,
            )
        )
    missing = sorted(known_ids - mapped_ids)
    if missing:
        raise BoundaryProofError("unmapped boundary or interaction: " + ", ".join(missing))
    return BoundaryProofMap(version, scope, tuple(normalized))


def validate_incident_registry(payload: Mapping[str, Any]) -> None:
    """Validate the exact first-release seeded fixture registry."""

    record = _object(payload, "incident_registry")
    _exact_fields(record, frozenset({"fixtures"}), "incident_registry")
    rows = _records(record["fixtures"], "fixtures")
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = f"fixtures[{index}]"
        _exact_fields(
            row,
            frozenset({"fixture_id", "seeded_omission", "expected_gate"}),
            label,
        )
        fixture_id = row["fixture_id"]
        if fixture_id not in FIXTURE_GATES:
            raise BoundaryProofError(f"{label}: unknown fixture: {fixture_id!r}")
        if fixture_id in seen:
            raise BoundaryProofError(f"{label}: duplicate fixture")
        seen.add(fixture_id)
        if row["expected_gate"] != FIXTURE_GATES[fixture_id]:
            raise BoundaryProofError(f"{label}: fixture gate mismatch")
        _nonempty_string(row["seeded_omission"], f"{label}.seeded_omission")
    missing = sorted(set(FIXTURE_GATES) - seen)
    if missing:
        raise BoundaryProofError("missing fixtures: " + ", ".join(missing))


def _result_record(value: Any, label: str) -> str:
    record = _object(value, label)
    _exact_fields(record, frozenset({"result", "evidence_refs"}), label)
    result = record["result"]
    if result not in RESULT_VALUES:
        raise BoundaryProofError(f"{label}: unknown result: {result!r}")
    _strings(record["evidence_refs"], f"{label}.evidence_refs", nonempty=True)
    return result


def _validate_report_shape(report: Mapping[str, Any]) -> None:
    _exact_fields(report, REPORT_FIELDS, "capability_report")
    if report["schema_version"] != CAPABILITY_REPORT_SCHEMA:
        raise BoundaryProofError("unknown capability report schema version")
    if report["boundary_model_version"] not in BOUNDARY_MODEL_VERSIONS:
        raise BoundaryProofError("unknown boundary-model version")
    if report["boundary_model_version"] != "v1":
        raise BoundaryProofError("capability report requires boundary model v1")
    if not isinstance(report["evaluated_skills"], list):
        raise BoundaryProofError("evaluated_skills: expected list")
    if tuple(report["evaluated_skills"]) != EVALUATED_SKILLS:
        raise BoundaryProofError("evaluated_skills must contain the exact eight skills")
    if not isinstance(report["required_check_ids"], list):
        raise BoundaryProofError("required_check_ids: expected list")
    if tuple(report["required_check_ids"]) != CHECK_IDS:
        unknown = sorted(set(report["required_check_ids"]) - set(CHECK_IDS))
        if unknown:
            raise BoundaryProofError("unknown required check ID: " + unknown[0])
        raise BoundaryProofError("required_check_ids must contain the exact six checks")
    checks = _object(report["checks"], "checks")
    if set(checks) != set(CHECK_IDS):
        unknown = sorted(set(checks) - set(CHECK_IDS))
        if unknown:
            raise BoundaryProofError("unknown required check ID: " + unknown[0])
        raise BoundaryProofError("checks must contain the exact six check IDs")
    for check_id in CHECK_IDS:
        _result_record(checks[check_id], f"checks.{check_id}")

    rows = _records(report["fixtures"], "fixtures")
    seen: set[str] = set()
    fixture_fields = frozenset(
        {
            "fixture_id",
            "result",
            "expected_gate",
            "detected_stage",
            "escaped_to_code_review",
            "sibling_bypass_remaining",
            "evidence_refs",
        }
    )
    for index, row in enumerate(rows):
        label = f"fixtures[{index}]"
        _exact_fields(row, fixture_fields, label)
        fixture_id = row["fixture_id"]
        if fixture_id not in FIXTURE_GATES:
            raise BoundaryProofError(f"{label}: unknown fixture: {fixture_id!r}")
        if fixture_id in seen:
            raise BoundaryProofError(f"{label}: duplicate fixture")
        seen.add(fixture_id)
        result = row["result"]
        if result not in RESULT_VALUES:
            raise BoundaryProofError(f"{label}: unknown result: {result!r}")
        if row["expected_gate"] not in EXPECTED_GATES:
            raise BoundaryProofError(f"{label}: unknown expected gate")
        if row["expected_gate"] != FIXTURE_GATES[fixture_id]:
            raise BoundaryProofError(f"{label}: expected gate mismatch")
        if row["detected_stage"] not in DETECTED_STAGES:
            raise BoundaryProofError(f"{label}: unknown detected stage")
        for field in ("escaped_to_code_review", "sibling_bypass_remaining"):
            if not isinstance(row[field], bool):
                raise BoundaryProofError(f"{label}.{field}: expected boolean")
        _strings(row["evidence_refs"], f"{label}.evidence_refs", nonempty=True)
    if seen != set(FIXTURE_GATES):
        raise BoundaryProofError("fixtures must contain every exact seeded fixture")

    preservation = _object(report["preservation_results"], "preservation_results")
    if set(preservation) != set(PRESERVATION_KEYS):
        raise BoundaryProofError("preservation_results must contain exact preservation keys")
    for key in PRESERVATION_KEYS:
        _result_record(preservation[key], f"preservation_results.{key}")
    _result_record(report["adapter_parity"], "adapter_parity")
    for field in (
        "false_blocking_count",
        "duplicate_normative_owner_count",
        "new_universal_artifact_count",
        "simple_fixture_structure_correction_cycles",
    ):
        value = report[field]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise BoundaryProofError(f"{field}: expected non-negative integer")
    if report["overall_result"] not in {"pass", "fail"}:
        raise BoundaryProofError("overall_result: expected pass or fail")


def validate_version_parity(
    feature_version: str | None,
    feature_scope: str | None,
    proof_version: str | None,
    proof_scope: str | None,
    *,
    public_activation: bool,
    explicitly_reviewed_opt_in: bool,
) -> str:
    """Validate prospective legacy/v1 adoption without inferring authority.

    Missing markers are grandfathered as ``legacy`` only before public
    activation.  A pre-activation ``v1`` pair requires an explicitly reviewed
    opt-in.  This function validates deterministic parity only; it does not
    decide whether an artifact is substantively revised.
    """

    def normalize(value: str | None, label: str) -> str:
        if value is None:
            if public_activation:
                raise BoundaryProofError(f"{label}: boundary-model marker required")
            return "legacy"
        if value not in BOUNDARY_MODEL_VERSIONS:
            raise BoundaryProofError(f"{label}: unknown boundary-model version")
        return value

    feature = normalize(feature_version, "feature")
    proof = normalize(proof_version, "proof")
    if feature != proof:
        raise BoundaryProofError("boundary-model version mismatch")
    if feature == "v1":
        if not isinstance(feature_scope, str) or not SCOPE_RE.fullmatch(feature_scope):
            raise BoundaryProofError("feature boundary-model scope is invalid")
        if not isinstance(proof_scope, str) or not SCOPE_RE.fullmatch(proof_scope):
            raise BoundaryProofError("proof boundary-model scope is invalid")
        if feature_scope != proof_scope:
            raise BoundaryProofError("boundary-model scope mismatch")
        if not public_activation and not explicitly_reviewed_opt_in:
            raise BoundaryProofError("pre-activation v1 requires reviewed opt-in")
    return feature


def capability_report_result(payload: Mapping[str, Any]) -> str:
    """Compute the capability baseline without trusting an asserted outcome."""

    report = _object(payload, "capability_report")
    _validate_report_shape(report)
    checks = report["checks"]
    fixtures = report["fixtures"]
    preservation = report["preservation_results"]
    pass_result = all(checks[check_id]["result"] == "pass" for check_id in CHECK_IDS)
    pass_result = pass_result and all(
        preservation[key]["result"] == "pass" for key in PRESERVATION_KEYS
    )
    pass_result = pass_result and report["adapter_parity"]["result"] == "pass"
    gate_index = {gate: index for index, gate in enumerate(EXPECTED_GATES)}
    for row in fixtures:
        detected = row["detected_stage"]
        timely = (
            detected != "not-detected"
            and gate_index[detected] <= gate_index[row["expected_gate"]]
        )
        pass_result = (
            pass_result
            and row["result"] == "pass"
            and timely
            and not row["escaped_to_code_review"]
            and not row["sibling_bypass_remaining"]
        )
    pass_result = pass_result and report["false_blocking_count"] == 0
    pass_result = pass_result and report["duplicate_normative_owner_count"] == 0
    pass_result = pass_result and report["new_universal_artifact_count"] == 0
    pass_result = (
        pass_result
        and report["simple_fixture_structure_correction_cycles"] <= 1
    )
    return "pass" if pass_result else "fail"


def validate_capability_report(payload: Mapping[str, Any]) -> None:
    """Validate report shape and reject caller-asserted aggregate results."""

    report = _object(payload, "capability_report")
    computed = capability_report_result(report)
    if report["overall_result"] != computed:
        raise BoundaryProofError(
            "overall_result does not match computed capability result"
        )


__all__ = [
    "APPLICABILITY_VALUES",
    "AUTOMATION_LEVELS",
    "BOUNDARY_MODEL_VERSIONS",
    "BoundaryExample",
    "BoundaryExtension",
    "BoundaryInteraction",
    "BoundaryProofError",
    "BoundaryProofMap",
    "CAPABILITY_REPORT_SCHEMA",
    "CHECK_IDS",
    "CORE_DIMENSION_IDS",
    "CoreBoundaryEntry",
    "DETECTED_STAGES",
    "EVALUATED_SKILLS",
    "EXAMPLE_ROLES",
    "EXPECTED_GATES",
    "FIXTURE_GATES",
    "FeatureBoundaryModel",
    "INTERACTION_RATIONALES",
    "PRESERVATION_KEYS",
    "ProofObligation",
    "RESULT_VALUES",
    "capability_report_result",
    "normalize_feature_model",
    "normalize_proof_map",
    "validate_capability_report",
    "validate_incident_registry",
    "validate_version_parity",
]
