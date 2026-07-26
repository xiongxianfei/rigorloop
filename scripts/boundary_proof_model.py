#!/usr/bin/env python3
"""Immutable executable projection of the boundary-first proof contract.

The approved workflow and skill specifications remain normative.  This module
implements only deterministic shape, vocabulary, traceability, and aggregate
rules.  It deliberately does not judge semantic completeness, applicability,
partition quality, interaction sufficiency, or review reasoning.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
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
INCIDENT_RULES = {
    "BFP-FX-CANONICAL-001": (
        "caller assertion accepted instead of canonical evidence",
        "canonical_source",
        "caller-asserted",
        "owner-derived",
        "spec-review",
        "bfp-canonical-source-invalid",
    ),
    "BFP-FX-VOCAB-001": (
        "unknown closed-vocabulary value is not rejected",
        "vocabulary_state",
        "unknown",
        "known",
        "test-spec-review",
        "bfp-unknown-vocabulary",
    ),
    "BFP-FX-TRANSITION-001": (
        "illegal state transition is unmodeled",
        "transition_state",
        "illegal",
        "legal",
        "test-spec-review",
        "bfp-illegal-transition",
    ),
    "BFP-FX-IDENTITY-001": (
        "stale or substituted identity is accepted",
        "identity_state",
        "non-current",
        "current",
        "test-spec-review",
        "bfp-non-current-identity",
    ),
    "BFP-FX-ATOMICITY-001": (
        "partial durable write is unproved",
        "mutation_state",
        "partial",
        "complete",
        "test-spec-review",
        "bfp-partial-mutation",
    ),
    "BFP-FX-RECOVERY-001": (
        "retry repeats work instead of reconciling",
        "recovery_state",
        "repeated",
        "reconciled",
        "test-spec-review",
        "bfp-repeat-without-reconcile",
    ),
    "BFP-FX-COMPOSITION-001": (
        "helper proof omits the composed public path",
        "composition_state",
        "helper-only",
        "complete",
        "test-spec-review",
        "bfp-composed-path-omitted",
    ),
    "BFP-FX-SIBLING-001": (
        "reported bypass is fixed while a sibling bypass remains",
        "sibling_state",
        "one-only",
        "complete",
        "implement",
        "bfp-sibling-bypass-remains",
    ),
}
FIXTURE_GATES = {key: value[4] for key, value in INCIDENT_RULES.items()}
BOUNDARY_STATE_VALUES = {
    "canonical_source": ("owner-derived", "caller-asserted"),
    "vocabulary_state": ("known", "unknown"),
    "transition_state": ("legal", "illegal", "not-applicable"),
    "identity_state": ("current", "non-current"),
    "mutation_state": ("complete", "partial", "not-applicable"),
    "recovery_state": ("reconciled", "repeated", "not-applicable"),
    "composition_state": ("complete", "helper-only", "not-applicable"),
    "sibling_state": ("complete", "one-only", "not-applicable"),
}
BLOCKING_REASON_CODES = (
    "prerequisite-unsatisfied",
    "authorization-required",
    "environment-unavailable",
    "upstream-failure",
)
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


@dataclass(frozen=True)
class StageGateResult:
    detected_stage: str
    diagnostic_id: str
    escaped_to_code_review: bool
    sibling_bypass_remaining: bool


@dataclass(frozen=True)
class SimpleTraceMetrics:
    false_blocking_count: int
    new_universal_artifact_count: int
    structure_only_correction_cycles: int


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
    regression_ids: set[str] = set()
    discovery_gap_ids: set[str] = set()
    boundary_requirements = {
        boundary_id: frozenset(entry.governing_requirement_ids)
        for entry in (*core, *extensions)
        for boundary_id in entry.boundary_ids
    }
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
        if regression_id is not None:
            if not STABLE_ID_RE.fullmatch(regression_id):
                raise BoundaryProofError(f"{label}: invalid regression ID")
            if regression_id in regression_ids:
                raise BoundaryProofError(f"{label}: duplicate regression ID")
            regression_ids.add(regression_id)
        if discovery_gap is not None:
            if not STABLE_ID_RE.fullmatch(discovery_gap):
                raise BoundaryProofError(f"{label}: invalid discovery gap ID")
            if discovery_gap in discovery_gap_ids:
                raise BoundaryProofError(f"{label}: duplicate discovery gap ID")
            discovery_gap_ids.add(discovery_gap)
        if boundaries:
            owned_requirements = set().union(
                *(boundary_requirements[boundary_id] for boundary_id in boundaries)
            )
            if not set(requirements) <= owned_requirements:
                raise BoundaryProofError(
                    f"{label}: governing requirement does not own cited boundary"
                )
            for boundary_id in boundaries:
                if not set(requirements) & boundary_requirements[boundary_id]:
                    raise BoundaryProofError(
                        f"{label}: cited boundary lacks governing requirement overlap"
                    )
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
    reference_requirements = {
        boundary_id: frozenset(entry.governing_requirement_ids)
        for entry in (*feature.core_dimensions, *feature.extensions)
        if entry.applicability == "applicable"
        for boundary_id in entry.boundary_ids
    }
    reference_requirements.update(
        {
            entry.interaction_id: frozenset(entry.governing_requirement_ids)
            for entry in feature.interactions
        }
    )
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
        owned_requirements = set().union(
            *(reference_requirements[reference] for reference in references)
        )
        unrelated = sorted(set(requirements) - owned_requirements)
        if unrelated:
            raise BoundaryProofError(
                f"{label}: governing requirement does not own cited reference: "
                + unrelated[0]
            )
        for reference in references:
            if not set(requirements) & reference_requirements[reference]:
                raise BoundaryProofError(
                    f"{label}: cited reference lacks governing requirement overlap: "
                    + reference
                )
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


def evaluate_boundary_state(payload: Mapping[str, Any]) -> StageGateResult:
    """Derive a gate result only from one closed boundary-state envelope."""

    state = _object(payload, "boundary_state")
    _exact_fields(state, frozenset(BOUNDARY_STATE_VALUES), "boundary_state")
    for field, allowed in BOUNDARY_STATE_VALUES.items():
        if state[field] not in allowed:
            raise BoundaryProofError(
                f"boundary_state.{field}: unknown closed value: {state[field]!r}"
            )
    matches = [
        rule
        for rule in INCIDENT_RULES.values()
        if state[rule[1]] == rule[2]
    ]
    if not matches:
        return StageGateResult("not-detected", "none", False, False)
    if len(matches) != 1:
        raise BoundaryProofError("boundary_state: multiple seeded triggers")
    rule = matches[0]
    return StageGateResult(
        detected_stage=rule[4],
        diagnostic_id=rule[5],
        escaped_to_code_review=False,
        sibling_bypass_remaining=False,
    )


def validate_incident_fixture(payload: Mapping[str, Any]) -> StageGateResult:
    """Validate one incident fixture and replay it through the shared evaluator."""

    record = _object(payload, "incident_fixture")
    _exact_fields(
        record,
        frozenset(
            {
                "fixture_id",
                "seeded_omission",
                "expected_gate",
                "expected_diagnostic",
                "boundary_state",
                "valid_contrast_state",
            }
        ),
        "incident_fixture",
    )
    fixture_id = record["fixture_id"]
    if fixture_id not in INCIDENT_RULES:
        raise BoundaryProofError(f"incident_fixture: unknown fixture: {fixture_id!r}")
    omission, trigger_field, trigger_value, contrast_value, gate, diagnostic = (
        INCIDENT_RULES[fixture_id]
    )
    expected = (omission, gate, diagnostic)
    actual = (
        record["seeded_omission"],
        record["expected_gate"],
        record["expected_diagnostic"],
    )
    if actual != expected:
        raise BoundaryProofError("incident_fixture: closed registry mismatch")
    state = _object(record["boundary_state"], "boundary_state")
    contrast = _object(record["valid_contrast_state"], "valid_contrast_state")
    result = evaluate_boundary_state(state)
    if (
        state.get(trigger_field) != trigger_value
        or contrast.get(trigger_field) != contrast_value
    ):
        raise BoundaryProofError("incident_fixture: trigger/contrast mismatch")
    changed = [field for field in BOUNDARY_STATE_VALUES if state.get(field) != contrast.get(field)]
    if changed != [trigger_field]:
        raise BoundaryProofError("incident_fixture: contrast must change exactly the trigger")
    contrast_result = evaluate_boundary_state(contrast)
    if contrast_result.diagnostic_id != "none":
        raise BoundaryProofError("incident_fixture: valid contrast contains a trigger")
    if result.detected_stage != gate or result.diagnostic_id != diagnostic:
        raise BoundaryProofError("incident_fixture: derived result mismatch")
    return result


def validate_incident_registry(
    payload: Mapping[str, Any],
    *,
    repository_root: Path | None = None,
) -> tuple[StageGateResult, ...]:
    """Validate the exact registry and all eight executable incident fixtures."""

    record = _object(payload, "incident_registry")
    _exact_fields(record, frozenset({"fixtures"}), "incident_registry")
    rows = _records(record["fixtures"], "fixtures")
    if len(rows) != len(INCIDENT_RULES):
        raise BoundaryProofError("incident_registry: expected every exact fixture")
    root = repository_root or Path(__file__).resolve().parents[1]
    results: list[StageGateResult] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = f"fixtures[{index}]"
        _exact_fields(row, frozenset({"fixture_id", "path"}), label)
        fixture_id = row["fixture_id"]
        if fixture_id not in INCIDENT_RULES:
            raise BoundaryProofError(f"{label}: unknown fixture: {fixture_id!r}")
        if fixture_id in seen:
            raise BoundaryProofError(f"{label}: duplicate fixture")
        seen.add(fixture_id)
        expected_path = (
            f"tests/fixtures/boundary-proof/incidents/{fixture_id}.json"
        )
        if row["path"] != expected_path:
            raise BoundaryProofError(f"{label}: fixture path mismatch")
        path = root / expected_path
        if not path.is_file() or path.is_symlink():
            raise BoundaryProofError(f"{label}: fixture file is missing or unsafe")
        results.append(validate_incident_fixture(json.loads(path.read_text())))
    return tuple(results)


def _evidence_ref(value: Any, label: str, repository_root: Path) -> None:
    record = _object(value, label)
    _exact_fields(record, frozenset({"path", "identity"}), label)
    raw_path = _nonempty_string(record["path"], f"{label}.path")
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != raw_path:
        raise BoundaryProofError(f"{label}: unsafe evidence path")
    candidate = repository_root / path
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(repository_root.resolve(strict=True))
    except (OSError, ValueError):
        raise BoundaryProofError(f"{label}: missing or out-of-repository evidence")
    current = repository_root
    traverses_symlink = False
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            traverses_symlink = True
            break
    if not resolved.is_file() or traverses_symlink:
        raise BoundaryProofError(f"{label}: evidence must be a non-symlink regular file")
    identity = _nonempty_string(record["identity"], f"{label}.identity")
    expected = "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest()
    if identity != expected:
        raise BoundaryProofError(f"{label}: stale or substituted evidence identity")


def _blocking_reason(value: Any, label: str) -> None:
    record = _object(value, label)
    _exact_fields(record, frozenset({"code", "detail"}), label)
    if record["code"] not in BLOCKING_REASON_CODES:
        raise BoundaryProofError(f"{label}: unknown blocking reason code")
    _nonempty_string(record["detail"], f"{label}.detail")


def _result_record(
    value: Any,
    label: str,
    repository_root: Path,
) -> str:
    record = _object(value, label)
    _exact_fields(
        record,
        frozenset({"result", "evidence_refs", "blocking_reason"}),
        label,
    )
    result = record["result"]
    if result not in RESULT_VALUES:
        raise BoundaryProofError(f"{label}: unknown result: {result!r}")
    evidence = record["evidence_refs"]
    if not isinstance(evidence, list):
        raise BoundaryProofError(f"{label}.evidence_refs: expected list")
    if result == "not-run":
        if evidence:
            raise BoundaryProofError(f"{label}: not-run cannot cite evidence")
        _blocking_reason(record["blocking_reason"], f"{label}.blocking_reason")
    else:
        if not evidence:
            raise BoundaryProofError(f"{label}.evidence_refs: expected one or more values")
        if record["blocking_reason"] is not None:
            raise BoundaryProofError(f"{label}: executed result cannot have blocking reason")
        for index, reference in enumerate(evidence):
            _evidence_ref(
                reference,
                f"{label}.evidence_refs[{index}]",
                repository_root,
            )
    return result


def _validate_report_shape(
    report: Mapping[str, Any],
    repository_root: Path | None = None,
) -> None:
    root = repository_root or Path(__file__).resolve().parents[1]
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
        _result_record(checks[check_id], f"checks.{check_id}", root)

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
            "blocking_reason",
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
        _result_record(
            {
                "result": result,
                "evidence_refs": row["evidence_refs"],
                "blocking_reason": row["blocking_reason"],
            },
            label,
            root,
        )
    if seen != set(FIXTURE_GATES):
        raise BoundaryProofError("fixtures must contain every exact seeded fixture")

    preservation = _object(report["preservation_results"], "preservation_results")
    if set(preservation) != set(PRESERVATION_KEYS):
        raise BoundaryProofError("preservation_results must contain exact preservation keys")
    for key in PRESERVATION_KEYS:
        _result_record(preservation[key], f"preservation_results.{key}", root)
    _result_record(report["adapter_parity"], "adapter_parity", root)
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
    markers_absent = feature_version is None and proof_version is None
    if (feature_version is None) != (proof_version is None):
        raise BoundaryProofError("boundary-model marker presence mismatch")
    if feature != proof:
        raise BoundaryProofError("boundary-model version mismatch")
    if markers_absent:
        if feature_scope is not None or proof_scope is not None:
            raise BoundaryProofError("markerless legacy pair cannot contain scope")
    else:
        if not isinstance(feature_scope, str) or not SCOPE_RE.fullmatch(feature_scope):
            raise BoundaryProofError("feature boundary-model scope is invalid")
        if not isinstance(proof_scope, str) or not SCOPE_RE.fullmatch(proof_scope):
            raise BoundaryProofError("proof boundary-model scope is invalid")
        if feature_scope != proof_scope:
            raise BoundaryProofError("boundary-model scope mismatch")
    if feature == "v1":
        if not public_activation and not explicitly_reviewed_opt_in:
            raise BoundaryProofError("pre-activation v1 requires reviewed opt-in")
    return feature


def capability_report_result(
    payload: Mapping[str, Any],
    *,
    repository_root: Path | None = None,
) -> str:
    """Compute the capability baseline without trusting an asserted outcome."""

    report = _object(payload, "capability_report")
    _validate_report_shape(report, repository_root)
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


def validate_capability_report(
    payload: Mapping[str, Any],
    *,
    repository_root: Path | None = None,
) -> None:
    """Validate report shape and reject caller-asserted aggregate results."""

    report = _object(payload, "capability_report")
    computed = capability_report_result(report, repository_root=repository_root)
    if report["overall_result"] != computed:
        raise BoundaryProofError(
            "overall_result does not match computed capability result"
        )


def evaluate_simple_change_trace(payload: Mapping[str, Any]) -> SimpleTraceMetrics:
    """Compute M1 synthetic simple-change metrics from a closed event trace."""

    record = _object(payload, "simple_trace")
    _exact_fields(
        record,
        frozenset({"events", "before_inventory", "after_inventory"}),
        "simple_trace",
    )
    events = _records(record["events"], "events")
    allowed_event_fields = frozenset(
        {
            "stage",
            "attempt",
            "structural_result",
            "observed_result",
            "diagnostic_id",
        }
    )
    allowed_stages = ("spec", "spec-review", "test-spec", "test-spec-review")
    false_blocking = 0
    correction_cycles = 0
    correction_used = False
    awaiting_correction_approval: tuple[str, int] | None = None
    expected_stage = "spec"
    expected_attempt = 1
    terminal = False
    for index, event in enumerate(events):
        label = f"events[{index}]"
        _exact_fields(event, allowed_event_fields, label)
        stage = event["stage"]
        if stage not in allowed_stages:
            raise BoundaryProofError(f"{label}: unknown stage")
        attempt = event["attempt"]
        if attempt not in (1, 2):
            raise BoundaryProofError(f"{label}: invalid attempt")
        if (stage, attempt) != (expected_stage, expected_attempt):
            raise BoundaryProofError(
                f"{label}: unsupported stage sequence; expected "
                f"{expected_stage}#{expected_attempt}"
            )
        structural = event["structural_result"]
        if structural not in ("pass", "fail"):
            raise BoundaryProofError(f"{label}: unknown structural result")
        observed = event["observed_result"]
        diagnostic = _nonempty_string(event["diagnostic_id"], f"{label}.diagnostic_id")
        if terminal:
            raise BoundaryProofError(f"{label}: event follows terminal result")
        is_review = stage.endswith("-review")
        if is_review:
            if observed not in ("approved", "changes-requested", "blocked"):
                raise BoundaryProofError(f"{label}: invalid review result")
            if structural == "fail" and observed == "approved":
                raise BoundaryProofError(f"{label}: failed structure cannot be approved")
            if structural == "pass" and observed == "approved" and diagnostic != "none":
                raise BoundaryProofError(f"{label}: approved review requires no diagnostic")
            if structural == "pass" and observed != "approved":
                false_blocking += 1
            if observed == "changes-requested":
                if correction_used or attempt != 1:
                    raise BoundaryProofError(f"{label}: more than one correction")
                correction_used = True
                expected_stage = stage.removesuffix("-review")
                expected_attempt = 2
                awaiting_correction_approval = (stage, 2)
            elif observed == "blocked":
                terminal = True
            elif awaiting_correction_approval is not None:
                if (stage, attempt) != awaiting_correction_approval:
                    raise BoundaryProofError(f"{label}: correction approval mismatch")
                correction_cycles += 1
                awaiting_correction_approval = None
                if stage == "spec-review":
                    expected_stage, expected_attempt = "test-spec", 1
                else:
                    terminal = True
            elif stage == "spec-review":
                expected_stage, expected_attempt = "test-spec", 1
            else:
                terminal = True
        else:
            if observed != "produced":
                raise BoundaryProofError(f"{label}: authoring result must be produced")
            if structural == "fail":
                terminal = True
            else:
                expected_stage, expected_attempt = f"{stage}-review", attempt
    if not terminal:
        raise BoundaryProofError("simple_trace: incomplete terminal branch")

    def inventory(value: Any, label: str) -> set[tuple[str, str]]:
        rows = _records(value, label)
        result: set[tuple[str, str]] = set()
        for index, row in enumerate(rows):
            item_label = f"{label}[{index}]"
            _exact_fields(row, frozenset({"path", "artifact_kind"}), item_label)
            path = _nonempty_string(row["path"], f"{item_label}.path")
            kind = row["artifact_kind"]
            if kind not in (
                "feature-spec",
                "test-spec",
                "review-evidence",
                "other-lifecycle",
                "non-lifecycle",
            ):
                raise BoundaryProofError(f"{item_label}: unknown artifact kind")
            item = (path, kind)
            if item in result:
                raise BoundaryProofError(f"{item_label}: duplicate inventory entry")
            result.add(item)
        return result

    before = inventory(record["before_inventory"], "before_inventory")
    after = inventory(record["after_inventory"], "after_inventory")
    allowed_outputs = {
        item for item in after - before if item[1] in {"feature-spec", "test-spec", "review-evidence"}
    }
    new_universal = sum(
        1
        for item in after - before - allowed_outputs
        if item[1] != "non-lifecycle"
    )
    return SimpleTraceMetrics(false_blocking, new_universal, correction_cycles)


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
    "INCIDENT_RULES",
    "FeatureBoundaryModel",
    "INTERACTION_RATIONALES",
    "PRESERVATION_KEYS",
    "ProofObligation",
    "RESULT_VALUES",
    "SimpleTraceMetrics",
    "StageGateResult",
    "capability_report_result",
    "evaluate_boundary_state",
    "evaluate_simple_change_trace",
    "normalize_feature_model",
    "normalize_proof_map",
    "validate_capability_report",
    "validate_incident_registry",
    "validate_incident_fixture",
    "validate_version_parity",
]
