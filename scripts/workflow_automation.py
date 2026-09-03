#!/usr/bin/env python3
"""Target-bound workflow automation coordinator.

This module contains the unified executable boundary.  It normalizes commands,
binds structured targets, resolves canonical workflow position, evaluates
bounded authority, and coordinates one stage operation through the sole state
writer. Public commands enter through the M6 adapters; direct skill and raw
context calls remain isolated.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass, field
from os import replace as _replace_file
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping

from lifecycle_state_sync import (
    AUTO_FIX_CLASSES as IMPLEMENTATION_AUTO_FIX_CLASSES,
    DECLARED_SAFE_REQUIRED_FIELDS as IMPLEMENTATION_DECLARED_SAFE_FIELDS,
    HandoffSummary,
    IMPLEMENTATION_CORRECTION_ROUND_CAP,
    MECHANICAL_AUTO_FIX_KINDS as IMPLEMENTATION_MECHANICAL_AUTO_FIX_KINDS,
    MECHANICAL_REQUIRED_FIELDS as IMPLEMENTATION_MECHANICAL_FIELDS,
    parse_handoff_summary,
)
from review_artifact_validation import (
    REVIEW_FIX_AUTO_RESOLUTION_CLASSES,
    REVIEW_FIX_BUDGET_LIMITS,
    parse_formal_review_findings,
    parse_formal_review_log,
    parse_formal_review_resolution,
)
from validate_workflow_automation import (
    CAPABILITY_AUTHORIZATION_CLASSES,
    CAPABILITY_BASIS_FIELDS,
    CAPABILITY_BASIS_LIST_FIELDS,
    CAPABILITY_STAGES,
    PROPOSAL_CORRECTION_VALIDATION_RULES,
    validate_workflow_automation,
)
from workflow_automation_policy import (
    CAPABILITY_MUTATION_CATEGORIES,
    LIFECYCLE_CONTRACT_V3,
    PUBLIC_TARGET_STAGES,
    STAGE_POLICY_BY_STAGE,
    AuthorizationClass,
    CapabilityKind,
    OccurrenceKind,
    WorkflowPosition,
    WorkflowStage,
    can_operation_fit_target,
    public_target_stages_for_contract,
    project_proposal_review_result,
    target_completion_predicate,
    stage_policy_by_stage_for_contract,
    verification_correction_owner,
)
from workflow_automation_state import (
    _canonical_review_occurrence,
    evaluate_receipt_recovery,
    StateContractError,
    VerifiedCompletion,
    WorkflowAutomationStateStore,
    compute_transition_key,
    parse_stage_evidence_fields,
    verify_transition_completion,
)
from workflow_code_state import (
    CanonicalCodeState,
    CodeStateError,
    CodeStateProvider,
    resolve_canonical_code_state,
)


CURRENT_COMMAND_RE = re.compile(r"^route\s+auto:\s*(?P<value>[a-z][a-z-]*)$")
MILESTONE_HEADER_RE = re.compile(r"^###\s+(?P<id>M[0-9]+)\.\s+(?P<title>.+?)\s*$")
MILESTONE_STATE_RE = re.compile(r"^-\s+Milestone state:\s*(?P<state>[a-z-]+)\s*$")
RFC3339_UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
CHANGE_ID_RE = re.compile(
    r"^Change ID:\s*(?P<value>[a-zA-Z0-9][a-zA-Z0-9._-]+)\s*$"
)

LEGACY_TARGETS = frozenset({"delivery-review", "verify"})
PUBLIC_ENGINE_CONTEXT = "bounded-review-fix-engine"
TERMINAL_MILESTONE_STATES = frozenset({"closed"})
KNOWN_MILESTONE_STATES = frozenset(
    {"planned", "implementing", "review-requested", "resolution-needed", "closed"}
)
PRE_PLAN_SEQUENCE = (
    "proposal",
    "proposal-review",
    "architecture",
    "spec",
    "design-review",
    "plan",
    "delivery-review",
)
REVIEW_POSITIONS = frozenset(
    {
        "proposal-review",
        "design-review",
        "delivery-review",
    }
)
REVIEW_OUTCOMES = frozenset({"approved", "changes-requested", "blocked", "inconclusive"})
TRANSITION_EVIDENCE_POSITIONS = frozenset(PRE_PLAN_SEQUENCE[1:])
CANONICAL_BASIS_FIELDS = {
    "proposal": ("proposal_identity", "reviewed_proposal_identity"),
    "proposal-review": ("approved_proposal_review_identity", "review_record_identity"),
    "architecture": ("architecture_identity",),
    "spec": ("spec_identity",),
    "design-review": ("design_review_identity",),
    "plan": ("plan_identity",),
    "delivery-review": ("delivery_review_identity",),
}


class AutomationContractError(RuntimeError):
    """Raised before persistence or invocation when an M3 contract is unsafe."""


@dataclass(frozen=True)
class NormalizedCommand:
    action: str
    target_stage: str | None = None
    legacy: bool = False


@dataclass(frozen=True)
class MilestoneRecord:
    milestone_id: str
    title: str
    state: str

    @property
    def display_name(self) -> str:
        return f"{self.milestone_id}. {self.title}"


@dataclass(frozen=True)
class ActivePlanContext:
    plan_identity: str
    handoff: HandoffSummary
    milestones: tuple[MilestoneRecord, ...]
    in_scope_milestone_ids: frozenset[str]

    @classmethod
    def from_text(cls, text: str, *, plan_identity: str) -> "ActivePlanContext":
        if not isinstance(plan_identity, str) or not plan_identity.strip():
            raise AutomationContractError("active plan identity is required")
        handoff, errors = parse_handoff_summary(text)
        if handoff is None or errors:
            detail = "; ".join(errors) if errors else "unknown handoff error"
            raise AutomationContractError(f"invalid active plan handoff: {detail}")

        milestones: list[MilestoneRecord] = []
        lines = text.splitlines()
        index = 0
        while index < len(lines):
            header = MILESTONE_HEADER_RE.match(lines[index])
            if header is None:
                index += 1
                continue
            values: list[str] = []
            cursor = index + 1
            while cursor < len(lines) and not lines[cursor].startswith(("### ", "## ")):
                match = MILESTONE_STATE_RE.match(lines[cursor].strip())
                if match is not None:
                    values.append(match.group("state"))
                cursor += 1
            if len(values) != 1 or values[0] not in KNOWN_MILESTONE_STATES:
                raise AutomationContractError(
                    f"invalid active plan milestone state: {header.group('id')}"
                )
            milestones.append(
                MilestoneRecord(header.group("id"), header.group("title"), values[0])
            )
            index = cursor

        remaining = handoff.fields["Remaining in-scope implementation milestones"]
        in_scope = frozenset(
            match.group(0)
            for item in remaining.split(",")
            if (match := re.search(r"M[0-9]+", item.strip())) is not None
        )
        if not milestones:
            raise AutomationContractError("active plan contains no implementation milestones")
        milestone_ids = [milestone.milestone_id for milestone in milestones]
        duplicates = sorted(
            milestone_id
            for milestone_id in set(milestone_ids)
            if milestone_ids.count(milestone_id) > 1
        )
        if duplicates:
            raise AutomationContractError(
                "duplicate active plan milestone identity: "
                + ", ".join(duplicates)
            )
        return cls(plan_identity, handoff, tuple(milestones), in_scope)

    def current_candidates(self) -> tuple[MilestoneRecord, ...]:
        return tuple(
            milestone
            for milestone in self.milestones
            if milestone.display_name == self.handoff.current_milestone
            and milestone.milestone_id in self.in_scope_milestone_ids
            and milestone.state not in TERMINAL_MILESTONE_STATES
            and milestone.state == self.handoff.current_milestone_state
        )


@dataclass(frozen=True)
class PrePlanEvidence:
    positions: Mapping[str, tuple[str, ...]]
    review_outcomes: Mapping[str, str]
    review_resolution_closed: bool
    architecture_applicability: str
    stale_identities: frozenset[str] = field(default_factory=frozenset)
    transition_identities: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalPosition:
    position: str
    source: str
    observed_identities: dict[str, str]
    milestone_id: str | None = None


@dataclass(frozen=True)
class CoordinationResult:
    status: str
    transition_id: str
    capability_id: str
    outputs: tuple[Any, ...]
    verified_completion: VerifiedCompletion


@dataclass(frozen=True)
class ArtifactEvidence:
    """Repository-backed evidence whose identity can be independently verified."""

    path: str
    identity: str


@dataclass(frozen=True)
class StageExecutionResult:
    outputs: tuple[ArtifactEvidence, ...]
    completion_evidence: Mapping[str, ArtifactEvidence]


@dataclass(frozen=True)
class CanonicalSyncResult:
    status: str
    evidence: Mapping[str, ArtifactEvidence]


@dataclass(frozen=True)
class ProposalReviewDecision:
    occurrence_recorded: bool
    review_id: str
    reviewed_artifact_identity: str
    outcome: str
    clean_gate: str
    routing_action: str
    next_stage: str | None = None
    pause_reason: str | None = None


@dataclass(frozen=True)
class ProposalCorrectionDecision:
    status: str
    next_stage: str | None = None
    pause_reason: str | None = None
    prior_review_stale: bool = False
    historical_review_preserved: bool = False


@dataclass(frozen=True)
class ProposalCorrectionAuthority:
    capability_id: str
    reviewed_review_identity: str
    accepted_finding_ids: frozenset[str]
    finding_classifications: Mapping[str, str]
    correction_budget: Mapping[str, int]
    allowed_path_roots: tuple[str, ...]
    reviewed_proposal_path: str | None = None
    review_record_path: str | None = None
    review_resolution_path: str | None = None
    proposal_review_basis: Mapping[str, Any] = field(default_factory=dict)
    correction_plans: Mapping[str, Mapping[str, str]] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class AuthoringCoordinationResult:
    coordination: CoordinationResult
    route: AuthoringRouteDecision


@dataclass(frozen=True)
class ImplementationCoordinationResult:
    coordination: CoordinationResult
    route: ImplementationRouteDecision


@dataclass(frozen=True)
class AuthoringRouteDecision:
    status: str
    next_stage: str | None = None
    pause_reason: str | None = None
    record_not_applicable: bool = False


@dataclass(frozen=True)
class ImplementationCorrectionDecision:
    status: str
    pause_reason: str | None = None


@dataclass(frozen=True)
class ImplementationRouteDecision:
    status: str
    next_stage: str | None = None
    next_milestone_id: str | None = None
    return_stage: str | None = None
    pause_reason: str | None = None
    automatic_repair: bool = False
    external_action_performed: bool = False


@dataclass(frozen=True)
class VerificationReadiness:
    basis_identities: Mapping[str, str]
    final_review_clean: bool


def _canonical_final_code_identity(
    *,
    branch_state_path: Path,
    canonical: CanonicalCodeState,
) -> str:
    try:
        fields = parse_stage_evidence_fields(
            branch_state_path,
            required_fields={
                "Stage",
                "Status",
                "Final code identity",
                "Final code paths",
                "Final code anchor identity",
                "Final code base revision",
                "Final code reviewed revision",
            },
        )
        paths = json.loads(fields["Final code paths"])
    except (StateContractError, json.JSONDecodeError) as error:
        raise AutomationContractError(
            "verification basis branch state is incomplete"
        ) from error
    if (
        fields.get("Stage") != "branch-state"
        or fields.get("Status") != "current"
        or not isinstance(paths, list)
        or not paths
        or not all(isinstance(path, str) and path for path in paths)
        or len(set(paths)) != len(paths)
    ):
        raise AutomationContractError(
            "verification basis branch state is invalid"
        )
    if tuple(sorted(paths)) != canonical.paths:
        raise AutomationContractError(
            "verification basis final code path projection is incomplete"
        )
    if fields.get("Final code anchor identity") != canonical.anchor_identity:
        raise AutomationContractError(
            "verification basis final code anchor projection is stale"
        )
    if (
        fields.get("Final code base revision") != canonical.base_revision
        or fields.get("Final code reviewed revision")
        != canonical.reviewed_revision
    ):
        raise AutomationContractError(
            "verification basis final code revision projection is stale"
        )
    if fields.get("Final code identity") != canonical.identity:
        raise AutomationContractError(
            "verification basis final code identity is stale"
        )
    return canonical.identity


def require_complete_ordered_evidence_tail(
    canonical: CanonicalCodeState,
    *,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> None:
    """Require the exact derived final-review-to-handoff tail for verify."""

    if (
        lifecycle_contract != LIFECYCLE_CONTRACT_V3
        or canonical.tail_state != "review-recorded"
        or canonical.final_review_recording_revision is None
        or canonical.explanation_recording_revision is not None
        or canonical.handoff_revision is not None
    ):
        raise AutomationContractError(
            "verification basis ordered final-review evidence tail is incomplete"
        )


def resolve_verification_readiness(
    *,
    repository_root: Path,
    basis: Mapping[str, Any],
    basis_paths: Mapping[str, Any],
    code_state_provider: CodeStateProvider | None = None,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> VerificationReadiness:
    """Resolve verification authority only from current repository evidence."""

    if lifecycle_contract != LIFECYCLE_CONTRACT_V3:
        raise AutomationContractError(
            f"lifecycle_contract: unknown_value {lifecycle_contract}"
        )
    required = CAPABILITY_BASIS_FIELDS[CapabilityKind.VERIFICATION.value] - {
        "explanation_inputs_identity"
    }
    if set(basis) != set(required) or set(basis_paths) != set(required):
        raise AutomationContractError("verification basis evidence is incomplete")
    artifacts: dict[str, Path] = {}
    identities: dict[str, str] = {}
    for name in required:
        artifact = _resolve_repository_file(repository_root, basis_paths[name])
        identity = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()
        if basis.get(name) != identity:
            raise AutomationContractError(
                f"verification basis identity is stale: {name}"
            )
        artifacts[name] = artifact
        identities[name] = identity

    plan_text_value = artifacts["closed_milestones_identity"].read_text(
        encoding="utf-8"
    )
    plan = ActivePlanContext.from_text(
        plan_text_value,
        plan_identity=identities["closed_milestones_identity"],
    )
    if not _all_implementation_milestones_closed(plan):
        raise AutomationContractError("verification basis milestones are open")

    review_path = artifacts["final_code_review_identity"]
    occurrence = _canonical_review_occurrence(
        review_path,
        repository_root=repository_root,
    )
    if occurrence is None:
        raise AutomationContractError("verification basis final review is not canonical")
    review, entry, _review_log, _review_log_identity = occurrence
    try:
        review_fields = parse_stage_evidence_fields(
            review_path,
            required_fields={
                "Review ID",
                "Stage",
                "Round",
                "Reviewer",
                "Target",
                "Status",
                "Material findings",
                "Review scope",
                "complete_final_diff",
                "cross_milestone_interactions",
                "governing_artifacts",
                "review_resolutions",
                "final_validation_selection",
                "generated_and_derived_artifacts",
                "cross_milestone_scope",
                "Reviewed commit",
                "Final code identity",
            },
        )
    except StateContractError as error:
        raise AutomationContractError(
            "verification basis final review is incomplete"
        ) from error
    change_ids = {
        match.group("value")
        for line in plan_text_value.splitlines()
        if (match := CHANGE_ID_RE.match(line.strip())) is not None
    }
    if len(change_ids) != 1:
        raise AutomationContractError(
            "verification basis plan change identity is invalid"
        )
    try:
        canonical = resolve_canonical_code_state(
            repository_root=repository_root,
            change_id=next(iter(change_ids)),
            reviewed_revision=review_fields["Reviewed commit"],
            final_review_id=review_fields["Review ID"],
            lifecycle_evidence_paths=frozenset(),
            test_provider=code_state_provider,
        )
    except (CodeStateError, ValueError) as error:
        raise AutomationContractError(
            "verification basis canonical code-state anchor is invalid"
        ) from error
    require_complete_ordered_evidence_tail(
        canonical, lifecycle_contract=lifecycle_contract
    )
    final_code_identity = _canonical_final_code_identity(
        branch_state_path=artifacts["branch_state_identity"],
        canonical=canonical,
    )
    if (
        review.stage != WorkflowStage.CODE_REVIEW.value
        or review.status not in {"approved", "clean-with-notes"}
        or review_fields.get("Review scope") != "final-holistic"
        or review_fields.get("complete_final_diff") != "reviewed"
        or review_fields.get("cross_milestone_interactions") != "reviewed"
        or review_fields.get("governing_artifacts") != "reviewed"
        or review_fields.get("review_resolutions")
        not in {"closed", "not-required"}
        or review_fields.get("final_validation_selection") != "reviewed"
        or review_fields.get("generated_and_derived_artifacts") != "current"
        or review_fields.get("cross_milestone_scope") != "reviewed"
        or review_fields.get("Final code identity") != final_code_identity
        or entry.material_finding_ids
        or entry.open_finding_ids
    ):
        raise AutomationContractError("verification basis final review is not clean")

    for name, expected_stage, expected_status in (
        ("promotion_evidence_identity", "promotion", "valid"),
        ("verification_commands_identity", "verification-commands", "current"),
    ):
        try:
            fields = parse_stage_evidence_fields(
                artifacts[name],
                required_fields={"Stage", "Status", "Final code identity"},
            )
        except StateContractError as error:
            raise AutomationContractError(
                f"verification basis evidence is incomplete: {name}"
            ) from error
        if (
            fields.get("Stage") != expected_stage
            or fields.get("Status") != expected_status
            or fields.get("Final code identity") != final_code_identity
        ):
            raise AutomationContractError(
                f"verification basis evidence is invalid: {name}"
            )
    return VerificationReadiness(identities, True)


@dataclass(frozen=True)
class _ImplementationCorrectionOperation:
    finding_id: str
    path: str
    old: str
    new: str
    expected_replacements: int
    expected_identity: str


@dataclass(frozen=True)
class _ImplementationCorrectionEvidence:
    review_identity: str
    review_id: str
    review_log_path: str
    review_resolution_path: str
    reviewed_milestone_id: str
    finding_ids: tuple[str, ...]
    classifications: Mapping[str, str]
    recipes: Mapping[str, Mapping[str, Any]]
    affected_paths: tuple[str, ...]
    operations: tuple[_ImplementationCorrectionOperation, ...]


def _one_finding_field(record: Any, label: str) -> str:
    values = record.fields.get(label, ())
    if len(values) != 1 or not values[0].value.strip():
        raise AutomationContractError(
            f"implementation correction finding {record.finding_id} "
            f"requires exactly one {label}"
        )
    return values[0].value.strip()


def _parse_correction_json(value: str, *, label: str) -> Mapping[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise AutomationContractError(
            f"implementation correction {label} must be strict JSON"
        ) from error
    if not isinstance(parsed, Mapping):
        raise AutomationContractError(
            f"implementation correction {label} must be an object"
        )
    return parsed


def _parse_correction_string_list(value: str, *, label: str) -> tuple[str, ...]:
    stripped = value.strip()
    if stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError as error:
            raise AutomationContractError(
                f"implementation correction {label} must be strict JSON"
            ) from error
        if (
            not isinstance(parsed, list)
            or not parsed
            or not all(isinstance(item, str) and item.strip() for item in parsed)
        ):
            raise AutomationContractError(
                f"implementation correction {label} must be a non-empty string list"
            )
        values = tuple(item.strip() for item in parsed)
    else:
        values = (stripped,)
    if (
        not values
        or any(not value for value in values)
        or len(set(values)) != len(values)
    ):
        raise AutomationContractError(
            f"implementation correction {label} must be unique"
        )
    return values


def _correction_objects(
    value: Mapping[str, Any],
    *,
    singular_fields: frozenset[str],
    collection_key: str,
    label: str,
) -> tuple[Mapping[str, Any], ...]:
    if set(value) == singular_fields:
        return (value,)
    if set(value) != {collection_key}:
        raise AutomationContractError(
            f"implementation correction {label} has unknown fields"
        )
    items = value[collection_key]
    if (
        not isinstance(items, list)
        or not items
        or not all(isinstance(item, Mapping) for item in items)
        or any(set(item) != singular_fields for item in items)
    ):
        raise AutomationContractError(
            f"implementation correction {label} must contain closed objects"
        )
    return tuple(items)


def _compile_implementation_correction_recipe(
    finding_id: str,
    fields: Mapping[str, str],
) -> tuple[Mapping[str, Any], tuple[_ImplementationCorrectionOperation, ...]]:
    """Compile one reviewer-owned finding into closed deterministic operations."""

    classification = fields.get("auto_fix_class", "").strip()
    if classification not in IMPLEMENTATION_AUTO_FIX_CLASSES - {"none"}:
        raise AutomationContractError(
            "implementation correction has no closed executable recipe"
        )
    affected_paths = _parse_correction_string_list(
        fields.get("affected_paths", ""),
        label="affected_paths",
    )
    if classification == "mechanical":
        missing = [
            name
            for name in IMPLEMENTATION_MECHANICAL_FIELDS
            if not fields.get(name, "").strip()
        ]
        if missing:
            raise AutomationContractError(
                "implementation correction mechanical recipe is incomplete"
            )
        kind = fields["auto_fix_kind"].strip()
        if kind not in IMPLEMENTATION_MECHANICAL_AUTO_FIX_KINDS:
            raise AutomationContractError(
                "implementation correction has no closed executable recipe"
            )
        authority_label = "deterministic_authority"
        validation_label = "required_validation"
        normalized: dict[str, Any] = {
            "auto_fix_class": classification,
            "auto_fix_kind": kind,
            "affected_paths": list(affected_paths),
        }
    else:
        missing = [
            name
            for name in IMPLEMENTATION_DECLARED_SAFE_FIELDS
            if not fields.get(name, "").strip()
        ]
        if missing:
            raise AutomationContractError(
                "implementation correction declared-safe recipe is incomplete"
            )
        for label in (
            "named_inputs",
            "named_outputs",
            "forbidden_paths",
            "acceptance_criteria",
        ):
            _parse_correction_string_list(fields[label], label=label)
        if (
            fields["scope_preservation_rule"].strip()
            != "changed-paths-subset-of-affected-paths"
            or fields["production_code_change"].strip() not in {"yes", "no"}
            or (
                fields["production_code_change"].strip() == "yes"
                and not fields["behavior_test"].strip()
            )
        ):
            raise AutomationContractError(
                "implementation correction declared-safe guard is invalid"
            )
        forbidden = _parse_correction_string_list(
            fields["forbidden_paths"],
            label="forbidden_paths",
        )
        if any(
            _path_is_within_roots(path, forbidden)
            for path in affected_paths
        ):
            raise AutomationContractError(
                "implementation correction affected path is forbidden"
            )
        authority_label = "resolution_recipe"
        validation_label = "required_validation_commands"
        normalized = {
            "auto_fix_class": classification,
            "affected_paths": list(affected_paths),
            "resolution_recipe": _parse_correction_json(
                fields[authority_label],
                label=authority_label,
            ),
            "named_inputs": list(
                _parse_correction_string_list(
                    fields["named_inputs"], label="named_inputs"
                )
            ),
            "named_outputs": list(
                _parse_correction_string_list(
                    fields["named_outputs"], label="named_outputs"
                )
            ),
            "forbidden_paths": list(forbidden),
            "acceptance_criteria": list(
                _parse_correction_string_list(
                    fields["acceptance_criteria"],
                    label="acceptance_criteria",
                )
            ),
            "required_validation_commands": _parse_correction_json(
                fields[validation_label],
                label=validation_label,
            ),
            "scope_preservation_rule": fields[
                "scope_preservation_rule"
            ].strip(),
            "production_code_change": fields[
                "production_code_change"
            ].strip(),
            "behavior_test": fields["behavior_test"].strip(),
        }

    authority = _parse_correction_json(
        fields[authority_label],
        label=authority_label,
    )
    validation = _parse_correction_json(
        fields[validation_label],
        label=validation_label,
    )
    operation_fields = frozenset(
        {"operation", "path", "old", "new", "expected_replacements"}
    )
    validation_fields = frozenset({"operation", "path", "identity"})
    authorities = _correction_objects(
        authority,
        singular_fields=operation_fields,
        collection_key="operations",
        label=authority_label,
    )
    validations = _correction_objects(
        validation,
        singular_fields=validation_fields,
        collection_key="checks",
        label=validation_label,
    )
    validation_by_path = {
        item.get("path"): item for item in validations
    }
    if (
        len(validation_by_path) != len(validations)
        or len(authorities) != len(affected_paths)
        or set(validation_by_path) != set(affected_paths)
        or {item.get("path") for item in authorities} != set(affected_paths)
    ):
        raise AutomationContractError(
            "implementation correction recipe paths do not match affected paths"
        )
    operations: list[_ImplementationCorrectionOperation] = []
    for item in authorities:
        path = item.get("path")
        check = validation_by_path.get(path)
        if (
            item.get("operation") != "exact-text-replace"
            or not isinstance(path, str)
            or not isinstance(item.get("old"), str)
            or not item["old"]
            or not isinstance(item.get("new"), str)
            or item["new"] == item["old"]
            or not isinstance(item.get("expected_replacements"), int)
            or isinstance(item.get("expected_replacements"), bool)
            or item["expected_replacements"] <= 0
            or not isinstance(check, Mapping)
            or check.get("operation") != "sha256"
            or not isinstance(check.get("identity"), str)
            or not check["identity"].startswith("sha256:")
        ):
            raise AutomationContractError(
                "implementation correction recipe is not closed and deterministic"
            )
        operations.append(
            _ImplementationCorrectionOperation(
                finding_id,
                path,
                item["old"],
                item["new"],
                item["expected_replacements"],
                check["identity"],
            )
        )
    if classification == "mechanical":
        normalized["deterministic_authority"] = dict(authority)
        normalized["required_validation"] = dict(validation)
    return normalized, tuple(operations)


def _load_implementation_correction_evidence(
    *,
    repository_root: Path,
    review_record_path: Any,
    review_resolution_path: Any,
    review_log_path: Any,
) -> _ImplementationCorrectionEvidence:
    """Load the latest reviewer-owned correction authority from canonical files."""

    review_path = _resolve_repository_file(repository_root, review_record_path)
    resolution_path = _resolve_repository_file(
        repository_root, review_resolution_path
    )
    log_path = _resolve_repository_file(repository_root, review_log_path)
    change_root = review_path.parent.parent
    if (
        review_path.parent.name != "reviews"
        or resolution_path != change_root / "review-resolution.md"
        or log_path != change_root / "review-log.md"
    ):
        raise AutomationContractError(
            "implementation correction evidence is not canonical change-local evidence"
        )
    occurrence = _canonical_review_occurrence(
        review_path, repository_root=repository_root
    )
    review, log_entry, canonical_log, _log_identity = (
        occurrence if occurrence is not None else (None, None, None, None)
    )
    parsed_review, findings, review_errors = parse_formal_review_findings(
        review_path
    )
    try:
        review_fields = parse_stage_evidence_fields(
            review_path,
            required_fields={"Reviewed milestone"},
        )
    except StateContractError as error:
        raise AutomationContractError(
            "implementation correction review milestone is invalid"
        ) from error
    reviewed_milestone_id = review_fields["Reviewed milestone"].split(".", 1)[0]
    if not re.fullmatch(r"M[0-9]+", reviewed_milestone_id):
        raise AutomationContractError(
            "implementation correction review milestone is invalid"
        )
    resolution, resolution_errors = parse_formal_review_resolution(
        resolution_path
    )
    if (
        review is None
        or parsed_review is None
        or review_errors
        or resolution_errors
        or review.review_id != parsed_review.review_id
        or review.stage != WorkflowStage.CODE_REVIEW.value
        or review.status != "changes-requested"
        or canonical_log != log_path
    ):
        raise AutomationContractError(
            "implementation correction review evidence is stale or invalid"
        )
    finding_ids = tuple(sorted(finding.finding_id for finding in findings))
    if (
        not finding_ids
        or tuple(sorted(log_entry.material_finding_ids)) != finding_ids
        or tuple(sorted(log_entry.open_finding_ids)) != finding_ids
    ):
        raise AutomationContractError(
            "implementation correction finding set is not current"
        )
    resolution_by_id = {
        entry.finding_id: entry
        for entry in resolution.entries
        if entry.finding_id in finding_ids
    }
    if (
        set(resolution_by_id) != set(finding_ids)
        or any(
            entry.disposition != "accepted"
            or entry.fields.get("Status") is None
            or entry.fields["Status"].value != "open"
            for entry in resolution_by_id.values()
        )
    ):
        raise AutomationContractError(
            "implementation correction resolution is not open and accepted"
        )

    classifications: dict[str, str] = {}
    recipes: dict[str, Mapping[str, Any]] = {}
    operations: list[_ImplementationCorrectionOperation] = []
    affected_paths: set[str] = set()
    for finding in findings:
        classification = _one_finding_field(finding, "auto_fix_class")
        required_names = (
            IMPLEMENTATION_MECHANICAL_FIELDS
            if classification == "mechanical"
            else IMPLEMENTATION_DECLARED_SAFE_FIELDS
            if classification == "declared-safe"
            else ()
        )
        field_values = {
            name: _one_finding_field(finding, name)
            for name in ("auto_fix_class", *required_names)
        }
        recipe, finding_operations = (
            _compile_implementation_correction_recipe(
                finding.finding_id,
                field_values,
            )
        )
        classifications[finding.finding_id] = classification
        recipes[finding.finding_id] = recipe
        affected_paths.update(recipe["affected_paths"])
        operations.extend(finding_operations)
    return _ImplementationCorrectionEvidence(
        review_identity="sha256:" + hashlib.sha256(review_path.read_bytes()).hexdigest(),
        review_id=review.review_id,
        review_log_path=log_path.relative_to(repository_root.resolve()).as_posix(),
        review_resolution_path=resolution_path.relative_to(
            repository_root.resolve()
        ).as_posix(),
        reviewed_milestone_id=reviewed_milestone_id,
        finding_ids=finding_ids,
        classifications=classifications,
        recipes=recipes,
        affected_paths=tuple(sorted(affected_paths)),
        operations=tuple(operations),
    )


def evaluate_implementation_correction(
    *,
    findings: Mapping[str, Mapping[str, Any]],
    previous_unresolved: Iterable[str],
    current_unresolved: Iterable[str],
    correction_rounds_completed: int,
    correction_round_cap: int,
    changed_paths: Iterable[str],
    allowed_path_roots: Iterable[str],
    evidence_current: bool,
    deterministic_validation_passed: bool,
    previous_classifications: Mapping[str, str] | None = None,
    owner_decision_required: bool = False,
    scope_expanded: bool = False,
) -> ImplementationCorrectionDecision:
    """Evaluate reviewer-owned implementation correction without legacy state."""

    def pause(reason: str) -> ImplementationCorrectionDecision:
        return ImplementationCorrectionDecision("paused", reason)

    if owner_decision_required:
        return pause("owner-decision-required")
    if not evidence_current:
        return pause("review-evidence-stale")
    if (
        not isinstance(correction_rounds_completed, int)
        or not isinstance(correction_round_cap, int)
        or correction_round_cap < 0
        or correction_round_cap > IMPLEMENTATION_CORRECTION_ROUND_CAP
        or correction_rounds_completed >= correction_round_cap
    ):
        return pause("correction-budget-exhausted")
    if scope_expanded:
        return pause("scope-expansion-required")

    previous = frozenset(previous_unresolved)
    current = frozenset(current_unresolved)
    if not current.issubset(previous):
        return pause("new-finding-or-class")
    if len(current) >= len(previous):
        return pause("unresolved-findings-did-not-shrink")
    corrected = previous - current
    if set(findings) != corrected:
        return pause("finding-evidence-does-not-match-corrected-set")

    declared_paths: set[str] = set()
    for finding_id in sorted(corrected):
        record = findings.get(finding_id)
        if not isinstance(record, Mapping):
            return pause("finding-evidence-invalid")
        auto_fix_class = record.get("auto_fix_class") or "none"
        if auto_fix_class not in IMPLEMENTATION_AUTO_FIX_CLASSES:
            return pause("unknown-auto-fix-class")
        if auto_fix_class == "none":
            return pause("finding-not-auto-fixable")
        if (
            previous_classifications is not None
            and previous_classifications.get(finding_id) != auto_fix_class
        ):
            return pause("new-finding-or-class")
        required_fields = (
            IMPLEMENTATION_MECHANICAL_FIELDS
            if auto_fix_class == "mechanical"
            else IMPLEMENTATION_DECLARED_SAFE_FIELDS
        )
        if any(not record.get(field_name) for field_name in required_fields):
            return pause("reviewer-correction-recipe-incomplete")
        if (
            auto_fix_class == "mechanical"
            and record.get("auto_fix_kind")
            not in IMPLEMENTATION_MECHANICAL_AUTO_FIX_KINDS
        ):
            return pause("reviewer-correction-recipe-incomplete")
        if (
            auto_fix_class == "declared-safe"
            and str(record.get("production_code_change", "")).lower() == "yes"
            and not (
                record.get("behavior_test") or record.get("test_spec_mapping")
            )
        ):
            return pause("reviewer-correction-recipe-incomplete")
        paths = record.get("affected_paths")
        if (
            not isinstance(paths, (list, tuple))
            or not paths
            or not all(isinstance(path, str) and path.strip() for path in paths)
        ):
            return pause("reviewer-correction-recipe-incomplete")
        declared_paths.update(paths)

    changed = frozenset(changed_paths)
    if not changed or not changed.issubset(declared_paths):
        return pause("correction-path-out-of-scope")
    roots = tuple(allowed_path_roots)
    if any(not _path_is_within_roots(path, roots) for path in changed):
        return pause("correction-path-out-of-scope")
    if not deterministic_validation_passed:
        return pause("deterministic-validation-missing")
    return ImplementationCorrectionDecision("authorized")


def _milestone_by_id(
    active_plan: ActivePlanContext,
    milestone_id: str,
) -> tuple[int, MilestoneRecord] | None:
    for index, milestone in enumerate(active_plan.milestones):
        if milestone.milestone_id == milestone_id:
            return index, milestone
    return None


def _all_implementation_milestones_closed(
    active_plan: ActivePlanContext | None,
) -> bool:
    return bool(active_plan and active_plan.milestones) and all(
        milestone.state == "closed" for milestone in active_plan.milestones
    )


def evaluate_non_public_implementation_route(
    *,
    current_stage: str,
    target_stage: str,
    target_milestone_id: str | None,
    capability_kind: str,
    capability_status: str,
    invocation_context: str,
    occurrence_kind: str,
    active_plan: ActivePlanContext | None,
    milestone_id: str | None = None,
    milestone_validation_passed: bool | None = None,
    review_outcome: str | None = None,
    review_resolution_closed: bool | None = None,
    review_resolution_status: str | None = None,
    verification_authorized: bool = False,
    final_review_clean: bool | None = None,
    verification_passed: bool | None = None,
    verification_finding_kind: str | None = None,
    ci_maintenance_required: bool = False,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> ImplementationRouteDecision:
    """Route one verified M5 stage while the integration remains non-public."""

    def pause(reason: str) -> ImplementationRouteDecision:
        return ImplementationRouteDecision("paused", pause_reason=reason)

    resolution_satisfied = (
        review_resolution_status in {"not-required", "closed"}
        if review_resolution_status is not None
        else review_resolution_closed is True
    )

    if invocation_context not in {"non-public-test-harness", PUBLIC_ENGINE_CONTEXT}:
        return pause("non-public-harness-required")
    policy = stage_policy_by_stage_for_contract(lifecycle_contract).get(current_stage)
    if policy is None or current_stage not in {
        WorkflowStage.IMPLEMENT.value,
        WorkflowStage.CODE_REVIEW.value,
        WorkflowStage.REVIEW_RESOLUTION.value,
        WorkflowStage.CI_MAINTENANCE.value,
        WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW.value,
        WorkflowStage.VERIFY.value,
    }:
        raise AutomationContractError(
            f"unknown implementation integration stage: {current_stage}"
        )
    if (
        capability_status != "active"
        or capability_kind != policy.capability_kind.value
    ):
        return pause("effective-capability-required")
    if occurrence_kind != policy.occurrence_rule.value:
        raise AutomationContractError("stage occurrence does not match policy")
    target = _target_stage(target_stage, lifecycle_contract=lifecycle_contract)
    if occurrence_kind == OccurrenceKind.MILESTONE.value and not milestone_id:
        raise AutomationContractError("milestone stage requires milestone identity")
    if not can_operation_fit_target(
        WorkflowStage(current_stage), target, lifecycle_contract=lifecycle_contract
    ):
        raise AutomationContractError("implementation stage exceeds structured target")
    if (
        target in {WorkflowStage.IMPLEMENT, WorkflowStage.CODE_REVIEW}
        and target_milestone_id != milestone_id
    ):
        raise AutomationContractError(
            "implementation stage exceeds structured target occurrence"
        )

    if current_stage in {
        WorkflowStage.IMPLEMENT.value,
        WorkflowStage.CODE_REVIEW.value,
    }:
        if active_plan is None or milestone_id is None:
            return pause("active-plan-required")
        found = _milestone_by_id(active_plan, milestone_id)
        if found is None:
            return pause("bound-milestone-missing")
        milestone_index, milestone = found
        if any(
            prior.state != "closed"
            for prior in active_plan.milestones[:milestone_index]
        ):
            return pause("milestone-order-violation")

        if current_stage == WorkflowStage.IMPLEMENT.value:
            if milestone_validation_passed is not True:
                return pause("milestone-validation-failed")
            if milestone.state != "review-requested":
                return pause("plan-handoff-not-review-requested")
            if target == WorkflowStage.IMPLEMENT and target_milestone_id == milestone_id:
                return ImplementationRouteDecision("target-reached")
            return ImplementationRouteDecision(
                "continue",
                WorkflowStage.CODE_REVIEW.value,
                milestone_id,
            )

        if review_outcome not in {"approved", "clean-with-notes"}:
            if review_outcome == "changes-requested":
                return ImplementationRouteDecision(
                    "correction-loop",
                    WorkflowStage.REVIEW_RESOLUTION.value,
                    milestone_id,
                )
            return pause("milestone-review-not-approved")
        if not resolution_satisfied:
            return pause("review-resolution-open")
        if milestone.state != "closed":
            return pause("plan-milestone-not-closed")
        if target == WorkflowStage.CODE_REVIEW and target_milestone_id == milestone_id:
            return ImplementationRouteDecision("target-reached")
        remaining = [
            item
            for item in active_plan.milestones[milestone_index + 1 :]
            if item.state != "closed"
        ]
        if remaining:
            next_milestone = remaining[0]
            if any(
                item.state != "closed"
                for item in active_plan.milestones[: active_plan.milestones.index(next_milestone)]
            ):
                return pause("milestone-order-violation")
            return ImplementationRouteDecision(
                "continue",
                WorkflowStage.IMPLEMENT.value,
                next_milestone.milestone_id,
            )
        next_stage = (
            WorkflowStage.CI_MAINTENANCE.value
            if ci_maintenance_required
            else WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW.value
        )
        return ImplementationRouteDecision("continue", next_stage)

    if current_stage == WorkflowStage.REVIEW_RESOLUTION.value:
        if not resolution_satisfied:
            return pause("review-resolution-open")
        next_stage = (
            WorkflowStage.CODE_REVIEW.value
            if milestone_id
            else WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW.value
        )
        return ImplementationRouteDecision("continue", next_stage, milestone_id)
    if current_stage == WorkflowStage.CI_MAINTENANCE.value:
        return ImplementationRouteDecision(
            "continue", WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW.value
        )
    if not _all_implementation_milestones_closed(active_plan):
        return pause("implementation-milestones-open")
    if current_stage == WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW.value:
        if review_outcome not in {"approved", "clean-with-notes"}:
            if review_outcome == "changes-requested":
                return ImplementationRouteDecision(
                    "correction-loop", WorkflowStage.REVIEW_RESOLUTION.value
                )
            return pause("final-holistic-review-not-clean")
        if not resolution_satisfied:
            return pause("review-resolution-open")
        if not verification_authorized:
            return pause("verification-authorization-required")
        return ImplementationRouteDecision("continue", WorkflowStage.VERIFY.value)
    if not verification_authorized:
        return pause("verification-authorization-required")
    if final_review_clean is not True:
        return pause("final-holistic-review-not-clean")
    if verification_passed is not True:
        if verification_finding_kind is not None:
            owner = verification_correction_owner(verification_finding_kind)
            return_stage = {
                "spec": "design-review",
                "architecture": "design-review",
                "plan": "delivery-review",
                "implement": "code-review",
                "code-review": "code-review",
                "ci-maintenance": "verify",
                "external-evidence-acquisition": "verify",
            }[owner]
            return ImplementationRouteDecision(
                "correction-loop",
                owner,
                return_stage=return_stage,
                automatic_repair=False,
            )
        return pause("verification-failed")
    return ImplementationRouteDecision(
        "target-reached",
        "pr",
        external_action_performed=False,
    )


def authorize_proposal_review_invocation(
    *,
    current_basis_identity: str,
    previous_inconclusive_basis_identity: str | None = None,
) -> None:
    """Reject an inconclusive rereview when no material input changed."""

    if not isinstance(current_basis_identity, str) or not current_basis_identity.strip():
        raise AutomationContractError("proposal-review basis identity is required")
    if previous_inconclusive_basis_identity == current_basis_identity:
        raise AutomationContractError(
            "unchanged inconclusive proposal-review cannot be invoked again"
        )


def evaluate_proposal_review(
    *,
    outcome: str,
    review_id: str,
    proposal_identity: str,
    reviewed_proposal_identity: str,
    target_stage: str,
    review_record_identity: str | None = None,
    correction_authority: ProposalCorrectionAuthority | None = None,
) -> ProposalReviewDecision:
    """Separate a recorded proposal-review occurrence from clean-gate routing."""

    if outcome not in REVIEW_OUTCOMES:
        raise AutomationContractError(f"unknown proposal-review outcome: {outcome}")
    if not isinstance(review_id, str) or not review_id.strip():
        raise AutomationContractError("proposal-review identity is required")
    if (
        not isinstance(proposal_identity, str)
        or not proposal_identity.strip()
        or reviewed_proposal_identity != proposal_identity
    ):
        raise AutomationContractError("proposal-review target identity is stale")
    target = _target_stage(target_stage)
    if not can_operation_fit_target(WorkflowStage.PROPOSAL_REVIEW, target):
        raise AutomationContractError("proposal-review exceeds structured target")

    correction_capability_id = None
    if (
        correction_authority is not None
        and review_record_identity
        == correction_authority.reviewed_review_identity
        and set(correction_authority.correction_budget) == set(REVIEW_FIX_BUDGET_LIMITS)
        and all(
            isinstance(value, int)
            and not isinstance(value, bool)
            and value > 0
            and value <= REVIEW_FIX_BUDGET_LIMITS[label]
            for label, value in correction_authority.correction_budget.items()
        )
    ):
        correction_capability_id = correction_authority.capability_id
    try:
        projection = project_proposal_review_result(
            outcome=outcome,
            target_stage=target_stage,
            review_id=review_id,
            reviewed_artifact_identity=proposal_identity,
            review_record_identity=review_record_identity,
            correction_capability_id=correction_capability_id,
        )
    except ValueError as error:
        raise AutomationContractError(str(error)) from error
    review_result = projection.review_result
    return ProposalReviewDecision(
        occurrence_recorded=True,
        review_id=review_id,
        reviewed_artifact_identity=proposal_identity,
        outcome=outcome,
        clean_gate=str(review_result["clean_gate"]),
        routing_action=str(review_result["routing_action"]),
        next_stage=projection.next_stage,
        pause_reason=review_result.get("pause_reason"),
    )


def _path_is_within_roots(path: str, roots: Iterable[str]) -> bool:
    candidate = PurePosixPath(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False
    for root in roots:
        parent = PurePosixPath(root)
        if parent.is_absolute() or ".." in parent.parts:
            continue
        if candidate == parent or parent in candidate.parents:
            return True
    return False


def _structured_identity(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


@dataclass(frozen=True)
class _ProposalCorrectionOperation:
    kind: str
    payload: bytes


def _compile_proposal_correction_operation(
    plan: Mapping[str, str],
) -> _ProposalCorrectionOperation:
    if (
        plan.get("classification") == "mechanical"
        and plan.get("recipe")
        == "Append one newline to the reviewed proposal."
        and plan.get("validation_rule") == "proposal-exact-append"
    ):
        return _ProposalCorrectionOperation("append-exact-bytes", b"\n")
    raise AutomationContractError(
        "proposal-correction recipe has no closed executable operation"
    )


def _verify_applied_proposal_correction(
    *,
    proposal_path: Path,
    reviewed_proposal_identity: str,
    operations: Iterable[_ProposalCorrectionOperation],
) -> str:
    """Reconstruct one applied correction from durable authority and live bytes."""

    payload = b"".join(operation.payload for operation in operations)
    current = proposal_path.read_bytes()
    if not payload or len(current) < len(payload) or not current.endswith(payload):
        raise AutomationContractError(
            "proposal correction does not match compiled operation"
        )
    reviewed = current[: -len(payload)]
    reconstructed_reviewed_identity = (
        "sha256:" + hashlib.sha256(reviewed).hexdigest()
    )
    if reconstructed_reviewed_identity != reviewed_proposal_identity:
        raise AutomationContractError(
            "proposal correction does not match reviewed proposal"
        )
    return "sha256:" + hashlib.sha256(current).hexdigest()


def _atomic_replace_regular_file(path: Path, content: bytes) -> None:
    """Replace one non-symlink regular file without exposing partial bytes."""

    if path.is_symlink() or not path.is_file():
        raise AutomationContractError(
            "proposal-correction target must be a regular repository file"
        )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, path.stat().st_mode)
        _replace_file(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _resolve_repository_file(repository_root: Path, relative_path: Any) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        raise AutomationContractError("canonical evidence path is required")
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise AutomationContractError("canonical evidence path must be repository-relative")
    root = repository_root.resolve()
    candidate = root / relative
    cursor = root
    for part in relative.parts:
        cursor /= part
        if cursor.is_symlink():
            raise AutomationContractError("canonical evidence path cannot contain symlinks")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise AutomationContractError("canonical evidence file does not exist")
    return resolved


@dataclass(frozen=True)
class _ProposalCorrectionRepositoryEvidence:
    review_identity: str
    review_id: str
    reviewed_proposal_path: str
    material_finding_ids: frozenset[str]
    unresolved_finding_ids: frozenset[str]
    correction_plans: Mapping[str, Mapping[str, str]]


def _load_proposal_correction_repository_evidence(
    *,
    repository_root: Path,
    review_record_path: Any,
    review_resolution_path: Any,
) -> _ProposalCorrectionRepositoryEvidence:
    review_path = _resolve_repository_file(repository_root, review_record_path)
    resolution_path = _resolve_repository_file(
        repository_root, review_resolution_path
    )
    if (
        review_path.parent.name != "reviews"
        or resolution_path != review_path.parent.parent / "review-resolution.md"
    ):
        raise AutomationContractError(
            "proposal-correction review evidence is not change-local"
        )
    review_identity = "sha256:" + hashlib.sha256(review_path.read_bytes()).hexdigest()
    review, findings, review_errors = parse_formal_review_findings(review_path)
    resolution, resolution_errors = parse_formal_review_resolution(resolution_path)
    review_log_path = review_path.parent.parent / "review-log.md"
    review_log_path = _resolve_repository_file(
        repository_root,
        review_log_path.relative_to(repository_root.resolve()).as_posix(),
    )
    review_log, review_log_errors = parse_formal_review_log(review_log_path)
    if (
        review is None
        or review_errors
        or resolution_errors
        or review_log_errors
        or review.stage != WorkflowStage.PROPOSAL_REVIEW.value
        or review.status != "changes-requested"
    ):
        raise AutomationContractError(
            "proposal-correction canonical review evidence is invalid"
        )
    matching_log_entries = [
        entry
        for entry in review_log
        if entry.review_id == review.review_id
        and entry.stage == review.stage
        and entry.round == review.round
        and entry.status == review.status
        and entry.detailed_record.strip("`")
        == review_path.relative_to(review_path.parent.parent).as_posix()
        and frozenset(entry.material_finding_ids)
        == frozenset(finding.finding_id for finding in findings)
    ]
    if len(matching_log_entries) != 1:
        raise AutomationContractError(
            "proposal-correction review occurrence is not canonical"
        )
    material_ids = frozenset(finding.finding_id for finding in findings)
    matching_resolution_entries = [
        entry for entry in resolution.entries if entry.finding_id in material_ids
    ]
    resolution_by_id = {
        entry.finding_id: entry for entry in matching_resolution_entries
    }
    if (
        len(matching_resolution_entries) != len(material_ids)
        or set(resolution_by_id) != set(material_ids)
        or any(
            entry.disposition != "accepted"
            or entry.fields.get("Status") is None
            or entry.fields["Status"].value not in {"open", "resolved"}
            for entry in matching_resolution_entries
        )
    ):
        raise AutomationContractError(
            "proposal-correction review resolution is incomplete"
        )
    unresolved = frozenset(
        finding_id
        for finding_id, entry in resolution_by_id.items()
        if entry.disposition == "accepted"
        and entry.fields.get("Status") is not None
        and entry.fields["Status"].value == "open"
    )
    if frozenset(matching_log_entries[0].open_finding_ids) != unresolved:
        raise AutomationContractError(
            "proposal-correction review log and resolution disagree"
        )
    correction_plans: dict[str, dict[str, str]] = {}
    for finding_id, entry in resolution_by_id.items():
        plan = {
            "classification": (
                entry.fields.get("Planned driver classification").value
                if entry.fields.get("Planned driver classification") is not None
                else ""
            ),
            "rationale": (
                entry.fields.get("Planned correction rationale").value
                if entry.fields.get("Planned correction rationale") is not None
                else ""
            ),
            "recipe": (
                entry.fields.get("Planned correction recipe").value
                if entry.fields.get("Planned correction recipe") is not None
                else ""
            ),
            "validation_rule": (
                entry.fields.get("Planned validation rule").value
                if entry.fields.get("Planned validation rule") is not None
                else ""
            ),
        }
        if (
            plan["classification"] not in REVIEW_FIX_AUTO_RESOLUTION_CLASSES
            or not plan["rationale"]
            or not plan["recipe"]
            or plan["validation_rule"]
            not in PROPOSAL_CORRECTION_VALIDATION_RULES
        ):
            raise AutomationContractError(
                "proposal-correction driver classification evidence is incomplete"
            )
        _compile_proposal_correction_operation(plan)
        correction_plans[finding_id] = plan
    if "sha256:" + hashlib.sha256(review_path.read_bytes()).hexdigest() != review_identity:
        raise AutomationContractError("proposal-correction review identity drifted")
    return _ProposalCorrectionRepositoryEvidence(
        review_identity,
        review.review_id,
        review.target.strip("`"),
        material_ids,
        unresolved,
        correction_plans,
    )


def resolve_proposal_correction_authority(
    automation: Mapping[str, Any],
    capability_id: str,
    *,
    repository_root: Path,
) -> ProposalCorrectionAuthority:
    """Resolve correction authority from an active capability and bound evidence."""

    capabilities = automation.get("effective_capabilities")
    capability = capabilities.get(capability_id) if isinstance(capabilities, Mapping) else None
    if not isinstance(capability, Mapping):
        raise AutomationContractError("proposal-correction capability not found")
    parents = automation.get("parent_authorizations")
    parent_id = capability.get("parent_authorization_id")
    parent = parents.get(parent_id) if isinstance(parents, Mapping) else None
    stage = capability.get("stage")
    if (
        capability.get("status") != "active"
        or capability.get("capability_kind") != CapabilityKind.PROPOSAL_CORRECTION.value
        or not isinstance(stage, Mapping)
        or stage.get("name") != WorkflowStage.PROPOSAL.value
        or not isinstance(parent, Mapping)
        or parent.get("status") != "active"
    ):
        raise AutomationContractError("proposal-correction capability is not executable")
    basis = capability.get("basis")
    scope = capability.get("scope")
    if not isinstance(basis, Mapping) or not isinstance(scope, Mapping):
        raise AutomationContractError("proposal-correction capability basis is invalid")
    accepted_value = scope.get("accepted_finding_ids")
    classifications_value = scope.get("finding_classifications")
    correction_plans_value = scope.get("correction_plans")
    budget_value = scope.get("correction_budget")
    proposal_review_basis = scope.get("proposal_review_basis")
    if (
        not isinstance(accepted_value, list)
        or not accepted_value
        or not all(isinstance(item, str) and item for item in accepted_value)
        or not isinstance(classifications_value, Mapping)
        or not isinstance(correction_plans_value, Mapping)
        or not isinstance(budget_value, Mapping)
        or not isinstance(proposal_review_basis, Mapping)
    ):
        raise AutomationContractError(
            "proposal-correction persisted evidence is incomplete"
        )
    accepted = frozenset(accepted_value)
    classifications = dict(classifications_value)
    correction_plans = {
        finding_id: dict(plan)
        for finding_id, plan in correction_plans_value.items()
        if isinstance(finding_id, str) and isinstance(plan, Mapping)
    }
    budget = dict(budget_value)
    repository_evidence = _load_proposal_correction_repository_evidence(
        repository_root=repository_root,
        review_record_path=scope.get("review_record_path"),
        review_resolution_path=scope.get("review_resolution_path"),
    )
    repository_classifications = {
        finding_id: plan["classification"]
        for finding_id, plan in repository_evidence.correction_plans.items()
    }
    expected = {
        "review_record_identity": repository_evidence.review_identity,
        "accepted_finding_set_identity": _structured_identity(sorted(accepted)),
        "classifier_policy_identity": _structured_identity(
            repository_evidence.correction_plans
        ),
        "correction_budget_identity": _structured_identity(budget),
    }
    if any(basis.get(name) != identity for name, identity in expected.items()):
        raise AutomationContractError("proposal-correction evidence does not match capability basis")
    if scope.get("correction_budget_identity") != expected["correction_budget_identity"]:
        raise AutomationContractError("proposal-correction budget identity is stale")
    if repository_evidence.unresolved_finding_ids != accepted:
        raise AutomationContractError(
            "proposal-correction unresolved finding evidence is stale"
        )
    if set(classifications) != accepted:
        raise AutomationContractError(
            "proposal-correction classification evidence is incomplete"
        )
    if classifications != repository_classifications:
        raise AutomationContractError(
            "proposal-correction driver classification evidence does not "
            "match capability scope"
        )
    if correction_plans != repository_evidence.correction_plans:
        raise AutomationContractError(
            "proposal-correction driver plan evidence does not match "
            "capability scope"
        )
    roots = scope.get("affected_path_roots")
    if not isinstance(roots, list) or not all(isinstance(root, str) for root in roots):
        raise AutomationContractError("proposal-correction path scope is invalid")
    return ProposalCorrectionAuthority(
        capability_id,
        repository_evidence.review_identity,
        accepted,
        classifications,
        budget,
        tuple(roots),
        repository_evidence.reviewed_proposal_path,
        str(scope["review_record_path"]),
        str(scope["review_resolution_path"]),
        dict(proposal_review_basis),
        {
            finding_id: dict(plan)
            for finding_id, plan in repository_evidence.correction_plans.items()
        },
    )


def evaluate_proposal_correction(
    *,
    authority: ProposalCorrectionAuthority,
    finding_classifications: Mapping[str, str],
    accepted_finding_ids: Iterable[str],
    current_finding_ids: Iterable[str],
    current_review_identity: str,
    unresolved_before: Iterable[str],
    unresolved_after: Iterable[str],
    affected_paths: Iterable[str],
    proposal_identity_before: str,
    proposal_identity_after: str,
    reviewed_finding_classifications: Mapping[str, str],
    basis_current: bool = True,
    deterministic_validation_passed: bool = True,
    scope_expanded: bool = False,
    owner_decision_required: bool = False,
    mutation_completed: bool = True,
) -> ProposalCorrectionDecision:
    """Evaluate the driver-owned bounded proposal-correction contract."""

    def pause(reason: str) -> ProposalCorrectionDecision:
        return ProposalCorrectionDecision("paused", pause_reason=reason)

    accepted = frozenset(accepted_finding_ids)
    current = frozenset(current_finding_ids)
    classifications = dict(finding_classifications)
    if owner_decision_required:
        return pause("owner-decision-required")
    if not basis_current or authority.reviewed_review_identity != current_review_identity:
        return pause("stale-review-evidence")
    if current != accepted or accepted != authority.accepted_finding_ids or set(classifications) != accepted:
        return pause("finding-set-changed")
    if dict(reviewed_finding_classifications) != classifications or classifications != dict(authority.finding_classifications):
        return pause("finding-classification-changed")
    unknown_classes = set(classifications.values()) - REVIEW_FIX_AUTO_RESOLUTION_CLASSES
    if unknown_classes:
        return pause("unknown-correction-classification")
    if "not-auto-safe" in classifications.values():
        return pause("not-auto-safe")
    if scope_expanded:
        return pause("scope-expanded")
    correction_budget = authority.correction_budget
    if set(correction_budget) != set(REVIEW_FIX_BUDGET_LIMITS):
        return pause("correction-budget-invalid")
    if any(
        not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
        or value > REVIEW_FIX_BUDGET_LIMITS[label]
        for label, value in correction_budget.items()
    ):
        return pause("correction-budget-exhausted")
    roots = authority.allowed_path_roots
    paths = tuple(affected_paths)
    if not paths or not roots or any(not _path_is_within_roots(path, roots) for path in paths):
        return pause("affected-path-scope-exceeded")
    if not mutation_completed:
        return ProposalCorrectionDecision("authorized")
    before = frozenset(unresolved_before)
    after = frozenset(unresolved_after)
    if not before or not after < before:
        return pause("unresolved-findings-did-not-shrink")
    if not deterministic_validation_passed:
        return pause("deterministic-validation-missing")
    if (
        not proposal_identity_before
        or not proposal_identity_after
        or proposal_identity_before == proposal_identity_after
    ):
        return pause("proposal-identity-unchanged")
    return ProposalCorrectionDecision(
        "rereview-required",
        next_stage=WorkflowStage.PROPOSAL_REVIEW.value,
        prior_review_stale=True,
        historical_review_preserved=True,
    )


_AUTHORING_NEXT_STAGE = {
    WorkflowStage.ARCHITECTURE.value: WorkflowStage.SPEC.value,
    WorkflowStage.SPEC.value: WorkflowStage.DESIGN_REVIEW.value,
    WorkflowStage.DESIGN_REVIEW.value: WorkflowStage.PLAN.value,
    WorkflowStage.PLAN.value: WorkflowStage.DELIVERY_REVIEW.value,
}
_AUTHORING_REVIEW_STAGES = frozenset(
    {
        WorkflowStage.DESIGN_REVIEW.value,
        WorkflowStage.DELIVERY_REVIEW.value,
    }
)


def evaluate_non_public_authoring_route(
    *,
    current_stage: str,
    target_stage: str,
    capability_kind: str,
    capability_status: str,
    invocation_context: str,
    review_outcome: str | None = None,
    architecture_applicability: str | None = None,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> AuthoringRouteDecision:
    """Evaluate M4 authoring progression without exposing a public route."""

    if invocation_context not in {"non-public-test-harness", PUBLIC_ENGINE_CONTEXT}:
        return AuthoringRouteDecision("paused", pause_reason="non-public-harness-required")
    target = _target_stage(target_stage, lifecycle_contract=lifecycle_contract)
    policy = stage_policy_by_stage_for_contract(lifecycle_contract).get(current_stage)
    if policy is None:
        raise AutomationContractError(f"unknown authoring stage: {current_stage}")
    if capability_status != "active" or capability_kind != policy.capability_kind.value:
        return AuthoringRouteDecision("paused", pause_reason="effective-capability-required")
    if not can_operation_fit_target(WorkflowStage(current_stage), target, lifecycle_contract=lifecycle_contract):
        raise AutomationContractError("authoring stage exceeds structured target")

    if current_stage == WorkflowStage.PROPOSAL_REVIEW.value:
        if review_outcome is None:
            return AuthoringRouteDecision("paused", pause_reason="proposal-review-outcome-required")
        review = evaluate_proposal_review(
            outcome=review_outcome,
            review_id="non-public-harness-review",
            proposal_identity="non-public-harness-proposal",
            reviewed_proposal_identity="non-public-harness-proposal",
            target_stage=target_stage,
        )
        status = "continue" if review.routing_action == "continue" else review.routing_action
        return AuthoringRouteDecision(status, review.next_stage, review.pause_reason)

    if current_stage in _AUTHORING_REVIEW_STAGES:
        if review_outcome not in REVIEW_OUTCOMES:
            return AuthoringRouteDecision("paused", pause_reason="review-outcome-required")
        if current_stage == target_stage and review_outcome in {"approved", "changes-requested"}:
            return AuthoringRouteDecision("target-reached")
        if review_outcome != "approved":
            return AuthoringRouteDecision(
                "paused", pause_reason=f"{current_stage}-{review_outcome}"
            )
    elif current_stage == target_stage:
        return AuthoringRouteDecision("target-reached")

    if current_stage == WorkflowStage.DELIVERY_REVIEW.value:
        return AuthoringRouteDecision(
            "paused", pause_reason="implementation-authorization-required"
        )
    next_stage = _AUTHORING_NEXT_STAGE.get(current_stage)
    if next_stage is None:
        raise AutomationContractError(f"authoring route is undefined for stage: {current_stage}")
    return AuthoringRouteDecision("continue", next_stage)


def _change_lifecycle_contract(document: Mapping[str, Any]) -> str:
    contract = document.get("lifecycle_contract", LIFECYCLE_CONTRACT_V3)
    try:
        stage_policy_by_stage_for_contract(contract)
    except ValueError as error:
        raise AutomationContractError(str(error)) from error
    return contract


def coordinate_non_public_authoring_stage(
    *,
    invocation_context: str,
    target_stage: str,
    store: WorkflowAutomationStateStore,
    repository_root: Path,
    **coordination: Any,
) -> AuthoringCoordinationResult:
    """Run one M4 authoring stage transaction, then route from verified evidence."""

    if invocation_context not in {"non-public-test-harness", PUBLIC_ENGINE_CONTEXT}:
        raise AutomationContractError("non-public authoring harness is required")
    lifecycle_contract = _change_lifecycle_contract(store.read().document)
    stage_request = coordination.get("stage")
    correction_decision: ProposalCorrectionDecision | None = None
    proposal_path_for_rollback: Path | None = None
    proposal_content_before: bytes | None = None
    proposal_mutation_completed = False
    post_completion_capabilities: Callable[
        [VerifiedCompletion, Mapping[str, Any], Mapping[str, Any]],
        Iterable[Mapping[str, Any]],
    ] | None = None
    if stage_request == WorkflowStage.PROPOSAL.value:
        snapshot = store.read()
        if snapshot.automation is None:
            raise AutomationContractError("unified automation state does not exist")
        capability_id = coordination.get("capability_id")
        authority = resolve_proposal_correction_authority(
            snapshot.automation,
            capability_id,
            repository_root=repository_root,
        )
        correction_decision = evaluate_proposal_correction(
            authority=authority,
            finding_classifications=authority.finding_classifications,
            reviewed_finding_classifications=authority.finding_classifications,
            accepted_finding_ids=authority.accepted_finding_ids,
            current_finding_ids=authority.accepted_finding_ids,
            current_review_identity=authority.reviewed_review_identity,
            unresolved_before=authority.accepted_finding_ids,
            unresolved_after=authority.accepted_finding_ids,
            affected_paths=(authority.reviewed_proposal_path or "",),
            proposal_identity_before="",
            proposal_identity_after="",
            mutation_completed=False,
        )
        if correction_decision.status != "authorized":
            raise AutomationContractError(
                "proposal correction paused: " + str(correction_decision.pause_reason)
            )
        assert authority.review_record_path is not None
        assert authority.review_resolution_path is not None
        assert authority.reviewed_proposal_path is not None

        proposal_path = _resolve_repository_file(
            repository_root, authority.reviewed_proposal_path
        )
        proposal_path_for_rollback = proposal_path
        operations = tuple(
            _compile_proposal_correction_operation(
                authority.correction_plans[finding_id]
            )
            for finding_id in sorted(authority.accepted_finding_ids)
        )

        def invoke_bounded_proposal_correction() -> StageExecutionResult:
            nonlocal proposal_content_before
            nonlocal proposal_mutation_completed
            before = proposal_path.read_bytes()
            after = before + b"".join(operation.payload for operation in operations)
            proposal_content_before = before
            _atomic_replace_regular_file(proposal_path, after)
            proposal_mutation_completed = True
            proposal_identity_after = (
                "sha256:" + hashlib.sha256(after).hexdigest()
            )
            evidence = ArtifactEvidence(
                authority.reviewed_proposal_path,
                proposal_identity_after,
            )
            return StageExecutionResult(
                (evidence,),
                {"proposal": evidence},
            )

        coordination = dict(coordination)
        coordination["invoke_stage"] = invoke_bounded_proposal_correction
        coordination["synchronize_canonical_state"] = (
            lambda stage_result: CanonicalSyncResult(
                "synchronized", stage_result.completion_evidence
            )
        )

        def derive_post_correction_capabilities(
            proof: VerifiedCompletion,
            automation: Mapping[str, Any],
            capability: Mapping[str, Any],
        ) -> Iterable[Mapping[str, Any]]:
            def pause(reason: str) -> None:
                raise AutomationContractError("proposal correction paused: " + reason)

            try:
                post_evidence = _load_proposal_correction_repository_evidence(
                    repository_root=repository_root,
                    review_record_path=authority.review_record_path,
                    review_resolution_path=authority.review_resolution_path,
                )
            except AutomationContractError as error:
                pause(str(error))
            proposal_proof = proof.canonical_evidence.get("proposal")
            if (
                not isinstance(proposal_proof, Mapping)
                or proposal_proof.get("path") != authority.reviewed_proposal_path
            ):
                pause("mutation escaped effective capability")
            proposal_before = str(
                capability["basis"].get("reviewed_proposal_identity", "")
            )
            proposal_after = proof.observed_identities.get("proposal", "")
            try:
                expected_proposal_identity_after = (
                    _verify_applied_proposal_correction(
                        proposal_path=proposal_path,
                        reviewed_proposal_identity=proposal_before,
                        operations=operations,
                    )
                )
            except AutomationContractError as error:
                pause(str(error))
            if proposal_after != expected_proposal_identity_after:
                pause("proposal correction completion identity mismatch")
            affected_paths = frozenset({authority.reviewed_proposal_path})
            post_decision = evaluate_proposal_correction(
                authority=authority,
                finding_classifications=authority.finding_classifications,
                reviewed_finding_classifications=authority.finding_classifications,
                accepted_finding_ids=authority.accepted_finding_ids,
                current_finding_ids=authority.accepted_finding_ids,
                current_review_identity=post_evidence.review_identity,
                unresolved_before=authority.accepted_finding_ids,
                unresolved_after=(),
                affected_paths=affected_paths,
                proposal_identity_before=proposal_before,
                proposal_identity_after=proposal_after,
                deterministic_validation_passed=True,
                mutation_completed=True,
            )
            if post_decision.status != "rereview-required":
                pause(str(post_decision.pause_reason))
            if post_evidence.review_identity != authority.reviewed_review_identity:
                pause("historical-review-not-preserved")
            fresh_basis = dict(authority.proposal_review_basis)
            fresh_basis["proposal_identity"] = proposal_after
            expected_fresh_fields = CAPABILITY_BASIS_FIELDS[
                CapabilityKind.PROPOSAL_REVIEW.value
            ]
            if set(fresh_basis) != set(expected_fresh_fields):
                pause("fresh-review-basis-incomplete")
            review_roots = fresh_basis.get("review_evidence_roots")
            if not isinstance(review_roots, list) or not review_roots:
                pause("fresh-review-roots-invalid")
            parents = automation.get("parent_authorizations")
            parent = (
                parents.get(capability["parent_authorization_id"])
                if isinstance(parents, Mapping)
                else None
            )
            capabilities = automation.get("effective_capabilities")
            if not isinstance(parent, Mapping) or not isinstance(capabilities, Mapping):
                pause("fresh-review-authority-missing")
            fresh_capability_id = (
                f"{capability['capability_id']}-rereview-"
                f"{proposal_after.split(':', 1)[-1][:12]}"
            )
            try:
                fresh_capability = derive_effective_capability(
                    capability_id=fresh_capability_id,
                    parent=parent,
                    stage=WorkflowStage.PROPOSAL_REVIEW.value,
                    occurrence={"kind": "singleton"},
                    basis=fresh_basis,
                    affected_path_roots=tuple(review_roots),
                    mutation_categories=("change-local-review-evidence",),
                    derived_at=str(capability.get("derived_at", "")),
                    existing_capabilities=tuple(capabilities.values()),
                )
            except AutomationContractError as error:
                pause("fresh-review-capability-invalid: " + str(error))
            return (fresh_capability,)

        post_completion_capabilities = derive_post_correction_capabilities
    try:
        result = coordinate_one_stage(
            store=store,
            repository_root=repository_root,
            post_completion_capabilities=post_completion_capabilities,
            **coordination,
        )
    except Exception as error:
        if (
            correction_decision is not None
            and proposal_mutation_completed
            and proposal_path_for_rollback is not None
            and proposal_content_before is not None
        ):
            try:
                _atomic_replace_regular_file(
                    proposal_path_for_rollback, proposal_content_before
                )
            except Exception as rollback_error:
                raise AutomationContractError(
                    "proposal correction rollback failed after rejected "
                    f"transaction: {rollback_error}"
                ) from error
        if str(error).startswith("proposal correction paused:"):
            paused_snapshot = store.read()
            assert paused_snapshot.automation is not None
            replacement = copy.deepcopy(paused_snapshot.automation)
            replacement["run"]["status"] = "paused"
            replacement["run"]["pause_reason"] = str(error).removeprefix(
                "proposal correction paused: "
            )
            store.replace_automation(
                replacement,
                expected_document_identity=paused_snapshot.document_identity,
            )
        raise
    snapshot = store.read()
    assert snapshot.automation is not None
    receipt = snapshot.automation["transition_receipts"][result.transition_id]
    capability = snapshot.automation["effective_capabilities"][result.capability_id]
    stage = capability["stage"]["name"]
    review_outcome = result.verified_completion.stage_facts.get("review_outcome")
    architecture_applicability = result.verified_completion.stage_facts.get(
        "architecture_applicability"
    )
    if correction_decision is not None:
        return AuthoringCoordinationResult(
            result,
            AuthoringRouteDecision("continue", WorkflowStage.PROPOSAL_REVIEW.value),
        )
    route = evaluate_non_public_authoring_route(
        current_stage=stage,
        target_stage=target_stage,
        capability_kind=capability["capability_kind"],
        # Completion consumed this exact capability; routing describes that
        # verified operation and never authorizes another mutation.
        capability_status="active",
        invocation_context=invocation_context,
        review_outcome=review_outcome,
        architecture_applicability=architecture_applicability,
        lifecycle_contract=lifecycle_contract,
    )
    return AuthoringCoordinationResult(result, route)


def coordinate_non_public_implementation_stage(
    *,
    invocation_context: str,
    target_stage: str,
    target_milestone_id: str | None,
    store: WorkflowAutomationStateStore,
    repository_root: Path,
    verification_basis_paths: Mapping[str, Any] | None = None,
    code_state_provider: CodeStateProvider | None = None,
    ci_maintenance_required: bool = False,
    **coordination: Any,
) -> ImplementationCoordinationResult:
    """Run one M5 transaction and route only from verifier-derived facts."""

    if invocation_context not in {"non-public-test-harness", PUBLIC_ENGINE_CONTEXT}:
        raise AutomationContractError(
            "non-public implementation harness is required"
        )
    lifecycle_contract = _change_lifecycle_contract(store.read().document)
    try:
        repository_root = store.require_repository_root(repository_root)
    except StateContractError as error:
        raise AutomationContractError(str(error)) from error
    verification_readiness: VerificationReadiness | None = None
    if coordination.get("stage") == WorkflowStage.VERIFY.value:
        basis = coordination.get("basis")
        if (
            not isinstance(basis, Mapping)
            or verification_basis_paths is None
        ):
            raise AutomationContractError(
                "repository-backed verification basis is required"
            )
        verification_readiness = resolve_verification_readiness(
            repository_root=repository_root,
            basis=basis,
            basis_paths=verification_basis_paths,
            code_state_provider=code_state_provider,
        )
    try:
        result = coordinate_one_stage(
            store=store,
            repository_root=repository_root,
            **coordination,
        )
    except AutomationContractError as error:
        if (
            coordination.get("stage") == WorkflowStage.VERIFY.value
            and "stage-native-verification-failed" in str(error)
        ):
            snapshot = store.read()
            if snapshot.automation is not None:
                replacement = copy.deepcopy(snapshot.automation)
                replacement["run"]["status"] = "paused"
                replacement["run"]["pause_reason"] = "verification-failed"
                store.replace_automation(
                    replacement,
                    expected_document_identity=snapshot.document_identity,
                )
            raise AutomationContractError(
                "verification failed; automatic repair is prohibited"
            ) from error
        raise
    snapshot = store.read()
    if snapshot.automation is None:
        raise AutomationContractError("unified automation state does not exist")
    capability = snapshot.automation["effective_capabilities"][
        result.capability_id
    ]
    stage = capability["stage"]
    occurrence = stage["occurrence"]
    facts = result.verified_completion.stage_facts

    route_plan = coordination.get("active_plan")
    plan_evidence = result.verified_completion.canonical_evidence.get(
        "plan-handoff"
    )
    if isinstance(plan_evidence, Mapping):
        plan_path = _resolve_repository_file(
            repository_root, plan_evidence.get("path")
        )
        plan_identity = result.verified_completion.observed_identities.get(
            "plan-handoff"
        )
        route_plan = ActivePlanContext.from_text(
            plan_path.read_text(encoding="utf-8"),
            plan_identity=str(plan_identity),
        )

    route = evaluate_non_public_implementation_route(
        current_stage=stage["name"],
        target_stage=target_stage,
        target_milestone_id=target_milestone_id,
        capability_kind=capability["capability_kind"],
        # This exact capability was active when the prepared receipt was
        # written. Completion consumes it before routing.
        capability_status="active",
        invocation_context=invocation_context,
        occurrence_kind=occurrence["kind"],
        milestone_id=occurrence.get("milestone_id"),
        active_plan=route_plan,
        milestone_validation_passed=(
            facts.get("milestone_validation_passed") == "true"
        ),
        review_outcome=facts.get("review_outcome"),
        review_resolution_closed=(
            facts.get("review_resolution_closed") == "true"
        ),
        review_resolution_status=facts.get("review_resolution_status"),
        verification_authorized=verification_readiness is not None,
        final_review_clean=(
            facts.get("final_review_clean") == "true"
            if "final_review_clean" in facts
            else (
                verification_readiness.final_review_clean
                if verification_readiness is not None
                else None
            )
        ),
        verification_passed=(
            facts.get("verification_passed") == "true"
            if "verification_passed" in facts
            else None
        ),
        verification_finding_kind=facts.get("verification_finding_kind"),
        ci_maintenance_required=ci_maintenance_required,
        lifecycle_contract=lifecycle_contract,
    )
    return ImplementationCoordinationResult(result, route)


def _replace_record_field(
    text: str,
    *,
    marker_label: str,
    marker_value: str,
    field_label: str,
    expected_value: str,
    replacement_value: str,
) -> str:
    """Replace one exact field inside one marker-delimited Markdown record."""

    lines = text.splitlines(keepends=True)
    marker = f"{marker_label}: {marker_value}"
    starts = [
        index for index, line in enumerate(lines) if line.strip() == marker
    ]
    if len(starts) != 1:
        raise AutomationContractError(
            f"implementation correction requires one {marker}"
        )
    start = starts[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].strip().startswith(f"{marker_label}: "):
            end = index
            break
    expected = f"{field_label}: {expected_value}"
    matches = [
        index
        for index in range(start, end)
        if lines[index].strip() == expected
    ]
    if len(matches) != 1:
        raise AutomationContractError(
            f"implementation correction requires one {expected}"
        )
    index = matches[0]
    prefix = lines[index][: len(lines[index]) - len(lines[index].lstrip())]
    newline = "\n" if lines[index].endswith("\n") else ""
    lines[index] = f"{prefix}{field_label}: {replacement_value}{newline}"
    return "".join(lines)


def _implementation_correction_artifact(
    repository_root: Path, relative_path: str
) -> ArtifactEvidence:
    path = _resolve_repository_file(repository_root, relative_path)
    return ArtifactEvidence(
        relative_path,
        "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
    )


def _pause_implementation_correction(
    store: WorkflowAutomationStateStore,
    capability_id: str,
) -> None:
    snapshot = store.read()
    if snapshot.automation is None:
        return
    replacement = copy.deepcopy(snapshot.automation)
    if replacement.get("run", {}).get("status") != "active":
        return
    replacement["run"]["status"] = "paused"
    replacement["run"]["pause_reason"] = "implementation-correction-paused"
    capability = replacement.get("effective_capabilities", {}).get(
        capability_id
    )
    if isinstance(capability, dict) and capability.get("status") == "active":
        capability["status"] = "invalidated"
        capability["invalidation_reason"] = "implementation-correction-paused"
    store.replace_automation(
        replacement,
        expected_document_identity=snapshot.document_identity,
    )


def coordinate_non_public_implementation_correction(
    *,
    invocation_context: str,
    target_stage: str,
    target_milestone_id: str | None,
    store: WorkflowAutomationStateStore,
    repository_root: Path,
    parent_authorization_id: str,
    capability_id: str,
    review_record_path: str,
    review_resolution_path: str,
    review_log_path: str,
    affected_path_roots: Iterable[str],
    mutation_categories: Iterable[str],
    correction_budget: Mapping[str, int],
    correction_budget_identity: str,
    derived_at: str,
    transition_id: str,
    active_plan: ActivePlanContext,
    previously_observed: Mapping[str, str] | None = None,
) -> ImplementationCoordinationResult:
    """Execute one closed reviewer-owned correction and require fresh rereview."""

    if invocation_context not in {"non-public-test-harness", PUBLIC_ENGINE_CONTEXT}:
        raise AutomationContractError(
            "non-public implementation harness is required"
        )
    try:
        repository_root = store.require_repository_root(repository_root)
    except StateContractError as error:
        raise AutomationContractError(str(error)) from error
    try:
        evidence = _load_implementation_correction_evidence(
            repository_root=repository_root,
            review_record_path=review_record_path,
            review_resolution_path=review_resolution_path,
            review_log_path=review_log_path,
        )
    except Exception:
        _pause_implementation_correction(store, capability_id)
        raise
    if (
        target_stage != WorkflowStage.CODE_REVIEW.value
        or target_milestone_id != evidence.reviewed_milestone_id
    ):
        _pause_implementation_correction(store, capability_id)
        raise AutomationContractError(
            "implementation correction must return to its bound milestone review"
        )
    roots = tuple(affected_path_roots)
    changed_paths = set(evidence.affected_paths) | {
        evidence.review_resolution_path,
        evidence.review_log_path,
    }
    if any(not _path_is_within_roots(path, roots) for path in changed_paths):
        _pause_implementation_correction(store, capability_id)
        raise AutomationContractError(
            "implementation correction path exceeds capability roots"
        )
    budget_identity = _structured_identity(dict(correction_budget))
    if budget_identity != correction_budget_identity:
        _pause_implementation_correction(store, capability_id)
        raise AutomationContractError(
            "implementation correction budget identity is stale"
        )
    basis = {
        "code_review_identity": evidence.review_identity,
        "accepted_finding_set_identity": _structured_identity(
            list(evidence.finding_ids)
        ),
        "reviewer_classification_identity": _structured_identity(
            evidence.recipes
        ),
        "correction_budget_identity": correction_budget_identity,
        "affected_paths_identity": _structured_identity(
            list(evidence.affected_paths)
        ),
    }
    correction_scope = {
        "review_record_path": review_record_path,
        "review_resolution_path": review_resolution_path,
        "review_log_path": review_log_path,
        "accepted_finding_ids": list(evidence.finding_ids),
        "reviewer_recipes": copy.deepcopy(dict(evidence.recipes)),
        "reviewed_milestone_id": evidence.reviewed_milestone_id,
    }
    snapshot = store.read()
    if snapshot.automation is None:
        raise AutomationContractError("unified automation state does not exist")
    completed_rounds = sum(
        1
        for receipt in snapshot.automation.get("transition_receipts", {}).values()
        if isinstance(receipt, Mapping)
        and receipt.get("status") == "completed"
        and isinstance(
            snapshot.automation.get("effective_capabilities", {}).get(
                receipt.get("effective_capability_id")
            ),
            Mapping,
        )
        and snapshot.automation["effective_capabilities"][
            receipt["effective_capability_id"]
        ].get("capability_kind")
        == CapabilityKind.IMPLEMENTATION_CORRECTION.value
        and snapshot.automation["effective_capabilities"][
            receipt["effective_capability_id"]
        ].get("parent_authorization_id")
        == parent_authorization_id
    )
    round_cap = correction_budget.get("cycles")
    if not isinstance(round_cap, int) or isinstance(round_cap, bool):
        _pause_implementation_correction(store, capability_id)
        raise AutomationContractError(
            "implementation correction cycle budget is required"
        )

    original_bytes: dict[Path, bytes] = {}
    actual_changed_paths: set[str] = set()

    def invoke_closed_correction() -> StageExecutionResult:
        try:
            for operation in evidence.operations:
                path = _resolve_repository_file(repository_root, operation.path)
                before = path.read_bytes()
                try:
                    text = before.decode("utf-8")
                except UnicodeDecodeError as error:
                    raise AutomationContractError(
                        "implementation correction target must be UTF-8 text"
                    ) from error
                if text.count(operation.old) != operation.expected_replacements:
                    raise AutomationContractError(
                        "implementation correction exact input no longer matches"
                    )
                after = text.replace(operation.old, operation.new).encode("utf-8")
                actual_identity = (
                    "sha256:" + hashlib.sha256(after).hexdigest()
                )
                if actual_identity != operation.expected_identity:
                    raise AutomationContractError(
                        "implementation correction deterministic validation failed"
                    )
                original_bytes.setdefault(path, before)
                _atomic_replace_regular_file(path, after)
                actual_changed_paths.add(operation.path)

            resolution = _resolve_repository_file(
                repository_root, evidence.review_resolution_path
            )
            resolution_text = resolution.read_text(encoding="utf-8")
            original_bytes.setdefault(resolution, resolution.read_bytes())
            parsed_resolution, resolution_errors = (
                parse_formal_review_resolution(resolution)
            )
            if resolution_errors:
                raise AutomationContractError(
                    "implementation correction resolution is structurally invalid"
                )
            for finding_id in evidence.finding_ids:
                resolution_text = _replace_record_field(
                    resolution_text,
                    marker_label="Finding ID",
                    marker_value=finding_id,
                    field_label="Status",
                    expected_value="open",
                    replacement_value="resolved",
                )
                resolution_text = _replace_record_field(
                    resolution_text,
                    marker_label="Finding ID",
                    marker_value=finding_id,
                    field_label="Validation evidence",
                    expected_value="pending",
                    replacement_value=(
                        "closed deterministic recipe and SHA-256 validation passed"
                    ),
                )
            if resolution_text.count("Closeout status: open") != 1:
                raise AutomationContractError(
                    "implementation correction closeout state is ambiguous"
                )
            other_resolution_open = any(
                entry.finding_id not in evidence.finding_ids
                and (
                    entry.disposition == "needs-decision"
                    or entry.fields.get("Status") is None
                    or entry.fields["Status"].value != "resolved"
                    or entry.fields.get("Validation evidence") is None
                    or entry.fields["Validation evidence"].value.strip()
                    in {"", "pending"}
                )
                for entry in parsed_resolution.entries
            )
            review_log = _resolve_repository_file(
                repository_root, evidence.review_log_path
            )
            parsed_log_entries, log_errors = parse_formal_review_log(review_log)
            if log_errors:
                raise AutomationContractError(
                    "implementation correction review log is structurally invalid"
                )
            other_log_open = any(
                finding_id not in evidence.finding_ids
                for entry in parsed_log_entries
                for finding_id in entry.open_finding_ids
            )
            if not other_resolution_open and not other_log_open:
                resolution_text = resolution_text.replace(
                    "Closeout status: open", "Closeout status: closed", 1
                )
            _atomic_replace_regular_file(
                resolution, resolution_text.encode("utf-8")
            )
            actual_changed_paths.add(evidence.review_resolution_path)

            log_text = review_log.read_text(encoding="utf-8")
            original_bytes.setdefault(review_log, review_log.read_bytes())
            open_value = ", ".join(evidence.finding_ids)
            log_text = _replace_record_field(
                log_text,
                marker_label="Review ID",
                marker_value=evidence.review_id,
                field_label="Open findings",
                expected_value=open_value,
                replacement_value="None",
            )
            _atomic_replace_regular_file(review_log, log_text.encode("utf-8"))
            actual_changed_paths.add(evidence.review_log_path)

            decision = evaluate_implementation_correction(
                findings=evidence.recipes,
                previous_unresolved=evidence.finding_ids,
                current_unresolved=(),
                correction_rounds_completed=completed_rounds,
                correction_round_cap=round_cap,
                changed_paths=evidence.affected_paths,
                allowed_path_roots=roots,
                evidence_current=True,
                deterministic_validation_passed=True,
                previous_classifications=evidence.classifications,
            )
            if decision.status != "authorized":
                raise AutomationContractError(
                    "implementation correction paused: "
                    + str(decision.pause_reason)
                )
            expected_changed = changed_paths
            if actual_changed_paths != expected_changed:
                raise AutomationContractError(
                    "implementation correction changed an unexpected path set"
                )
            resolution_evidence = _implementation_correction_artifact(
                repository_root, evidence.review_resolution_path
            )
            outputs = tuple(
                _implementation_correction_artifact(repository_root, path)
                for path in sorted(actual_changed_paths)
            )
            return StageExecutionResult(
                outputs,
                {"review-resolution": resolution_evidence},
            )
        except Exception:
            for path, content in reversed(tuple(original_bytes.items())):
                _atomic_replace_regular_file(path, content)
            raise

    try:
        result = coordinate_one_stage(
            store=store,
            parent_authorization_id=parent_authorization_id,
            capability_id=capability_id,
            stage=WorkflowStage.REVIEW_RESOLUTION.value,
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=roots,
            mutation_categories=tuple(mutation_categories),
            correction_budget=correction_budget,
            correction_budget_identity=correction_budget_identity,
            implementation_correction_scope=correction_scope,
            derived_at=derived_at,
            transition_id=transition_id,
            input_identities={
                **basis,
                "plan": active_plan.plan_identity,
                "review_outcome": "changes-requested",
                "review_identity": evidence.review_identity,
            },
            invoke_stage=invoke_closed_correction,
            synchronize_canonical_state=lambda stage_result: CanonicalSyncResult(
                "synchronized", stage_result.completion_evidence
            ),
            repository_root=repository_root,
            active_plan=active_plan,
            previously_observed=previously_observed,
        )
    except Exception:
        for path, content in reversed(tuple(original_bytes.items())):
            if path.exists() and path.read_bytes() != content:
                _atomic_replace_regular_file(path, content)
        _pause_implementation_correction(store, capability_id)
        raise
    return ImplementationCoordinationResult(
        result,
        ImplementationRouteDecision(
            "continue",
            WorkflowStage.CODE_REVIEW.value,
            evidence.reviewed_milestone_id,
        ),
    )


def coordinate_public_authoring_stage(
    *,
    command: str,
    **coordination: Any,
) -> AuthoringCoordinationResult:
    """Execute one stage selected by a public authoring target command."""

    store = coordination.get("store")
    if not isinstance(store, WorkflowAutomationStateStore):
        raise AutomationContractError("public authoring execution requires a state store")
    lifecycle_contract = _change_lifecycle_contract(store.read().document)
    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError("public authoring execution requires a target")
    return coordinate_non_public_authoring_stage(
        invocation_context=PUBLIC_ENGINE_CONTEXT,
        target_stage=normalized.target_stage,
        **coordination,
    )


def coordinate_public_implementation_stage(
    *,
    command: str,
    target_milestone_id: str | None,
    **coordination: Any,
) -> ImplementationCoordinationResult:
    """Execute one stage selected by a public implementation target command."""

    store = coordination.get("store")
    if not isinstance(store, WorkflowAutomationStateStore):
        raise AutomationContractError("public implementation execution requires a state store")
    lifecycle_contract = _change_lifecycle_contract(store.read().document)
    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError(
            "public implementation execution requires a target"
        )
    return coordinate_non_public_implementation_stage(
        invocation_context=PUBLIC_ENGINE_CONTEXT,
        target_stage=normalized.target_stage,
        target_milestone_id=target_milestone_id,
        **coordination,
    )


def coordinate_public_implementation_correction(
    *,
    command: str,
    **coordination: Any,
) -> ImplementationCoordinationResult:
    """Execute reviewer-owned correction inside a public unified run."""

    store = coordination.get("store")
    if not isinstance(store, WorkflowAutomationStateStore):
        raise AutomationContractError("public implementation correction requires a state store")
    lifecycle_contract = _change_lifecycle_contract(store.read().document)
    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError(
            "public implementation correction requires a target"
        )
    return coordinate_non_public_implementation_correction(
        invocation_context=PUBLIC_ENGINE_CONTEXT,
        target_stage=normalized.target_stage,
        **coordination,
    )


def normalize_command(command: str, *, lifecycle_contract: str = LIFECYCLE_CONTRACT_V3) -> NormalizedCommand:
    """Normalize the current route command without persisting state."""

    if not isinstance(command, str):
        raise AutomationContractError("workflow command must be text")
    normalized = command.strip()
    if normalized.startswith("$"):
        normalized = normalized[1:].strip()
    current = CURRENT_COMMAND_RE.fullmatch(normalized)
    if current is None:
        raise AutomationContractError("unknown workflow automation command")
    value = current.group("value")
    is_legacy = False
    if value in {"status", "off"}:
        return NormalizedCommand(value, legacy=is_legacy)
    public_values = {stage.value for stage in public_target_stages_for_contract(lifecycle_contract)}
    if value not in public_values or (is_legacy and value not in LEGACY_TARGETS):
        raise AutomationContractError(f"unknown workflow automation target: {value}")
    return NormalizedCommand("target", value, is_legacy)


def _target_stage(stage: str, *, lifecycle_contract: str = LIFECYCLE_CONTRACT_V3) -> WorkflowStage:
    try:
        parsed = WorkflowStage(stage)
    except (TypeError, ValueError) as exc:
        raise AutomationContractError(f"unknown workflow automation target: {stage}") from exc
    if parsed not in public_target_stages_for_contract(lifecycle_contract):
        raise AutomationContractError(f"stage is not a public target: {stage}")
    return parsed


def _binding_diagnostic(stage: str) -> str:
    return (
        f"cannot bind {stage} target: active plan does not identify exactly one "
        "current in-scope implementation milestone"
    )


def bind_target(
    stage: str,
    *,
    bound_at: str,
    plan: ActivePlanContext | None = None,
    requested_occurrence: str | None = None,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> dict[str, Any]:
    """Bind one complete structured target before run or authority persistence."""

    parsed = _target_stage(stage, lifecycle_contract=lifecycle_contract)
    if not RFC3339_UTC_RE.fullmatch(bound_at):
        raise AutomationContractError("target binding time must be RFC3339 UTC")
    policy = stage_policy_by_stage_for_contract(lifecycle_contract)[parsed.value]
    expected = policy.occurrence_rule.value
    if requested_occurrence is not None and requested_occurrence != expected:
        raise AutomationContractError(
            f"incompatible target occurrence for {stage}: expected {expected}"
        )
    occurrence: dict[str, Any] = {"kind": expected}
    target: dict[str, Any] = {
        "stage": parsed.value,
        "occurrence": occurrence,
        "bound_at": bound_at,
        "completion": target_completion_predicate(parsed, lifecycle_contract=lifecycle_contract),
    }
    if expected == OccurrenceKind.MILESTONE.value:
        if plan is None:
            raise AutomationContractError(_binding_diagnostic(stage))
        candidates = plan.current_candidates()
        if len(candidates) != 1:
            raise AutomationContractError(_binding_diagnostic(stage))
        occurrence["milestone_id"] = candidates[0].milestone_id
        target["plan_identity"] = plan.plan_identity
    return target


def resolve_command_target(
    command: str,
    *,
    bound_at: str,
    plan: ActivePlanContext | None = None,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> dict[str, Any]:
    """Normalize a target command and bind its complete occurrence envelope."""

    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError("workflow command does not select a target")
    return bind_target(
        normalized.target_stage,
        bound_at=bound_at,
        plan=plan,
        lifecycle_contract=lifecycle_contract,
    )


def evaluate_public_authoring_route(
    *,
    command: str,
    current_stage: str,
    capability_kind: str,
    capability_status: str,
    review_outcome: str | None = None,
    architecture_applicability: str | None = None,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> AuthoringRouteDecision:
    """Route one public authoring operation through the unified engine."""

    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError("public authoring route requires a target command")
    return evaluate_non_public_authoring_route(
        current_stage=current_stage,
        target_stage=normalized.target_stage,
        capability_kind=capability_kind,
        capability_status=capability_status,
        invocation_context=PUBLIC_ENGINE_CONTEXT,
        review_outcome=review_outcome,
        architecture_applicability=architecture_applicability,
        lifecycle_contract=lifecycle_contract,
    )


def evaluate_public_implementation_route(
    *,
    command: str,
    current_stage: str,
    capability_kind: str,
    capability_status: str,
    occurrence_kind: str,
    active_plan: ActivePlanContext | None,
    target_milestone_id: str | None = None,
    milestone_id: str | None = None,
    milestone_validation_passed: bool | None = None,
    review_outcome: str | None = None,
    review_resolution_closed: bool | None = None,
    review_resolution_status: str | None = None,
    verification_authorized: bool = False,
    final_review_clean: bool | None = None,
    verification_passed: bool | None = None,
    verification_finding_kind: str | None = None,
    ci_maintenance_required: bool = False,
    lifecycle_contract: str = LIFECYCLE_CONTRACT_V3,
) -> ImplementationRouteDecision:
    """Route one public implementation operation through the unified engine."""

    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError(
            "public implementation route requires a target command"
        )
    return evaluate_non_public_implementation_route(
        current_stage=current_stage,
        target_stage=normalized.target_stage,
        target_milestone_id=target_milestone_id,
        capability_kind=capability_kind,
        capability_status=capability_status,
        invocation_context=PUBLIC_ENGINE_CONTEXT,
        occurrence_kind=occurrence_kind,
        active_plan=active_plan,
        milestone_id=milestone_id,
        milestone_validation_passed=milestone_validation_passed,
        review_outcome=review_outcome,
        review_resolution_closed=review_resolution_closed,
        review_resolution_status=review_resolution_status,
        verification_authorized=verification_authorized,
        final_review_clean=final_review_clean,
        verification_passed=verification_passed,
        verification_finding_kind=verification_finding_kind,
        ci_maintenance_required=ci_maintenance_required,
        lifecycle_contract=lifecycle_contract,
    )


def _legacy_public_projection(
    projection: Mapping[str, Any],
) -> dict[str, Any]:
    """Project a read-only legacy record into the complete public result shape."""

    legacy = projection.get("legacy")
    if not isinstance(legacy, Mapping):
        raise AutomationContractError("legacy status projection is incomplete")
    record: Mapping[str, Any] = legacy
    mechanism = legacy.get("profile")
    if not isinstance(mechanism, str):
        candidates = [
            (name.replace("_", "-"), candidate)
            for name in (
                "authoring_through_plan_review",
                "implementation_through_verify",
                "review_fix",
            )
            if isinstance((candidate := legacy.get(name)), Mapping)
        ]
        if len(candidates) != 1:
            raise AutomationContractError(
                "legacy status requires exactly one source record"
            )
        mechanism, record = candidates[0]
        candidate_mechanism = record.get("profile") or record.get("mechanism")
        if isinstance(candidate_mechanism, str):
            mechanism = candidate_mechanism
    target_stage = {
        "authoring-through-plan-review": WorkflowStage.DELIVERY_REVIEW.value,
        "implementation-through-verify": WorkflowStage.VERIFY.value,
    }.get(mechanism)
    if target_stage is None and mechanism == "bounded-review-fix":
        candidate = record.get("target_stage")
        if isinstance(candidate, str):
            target_stage = candidate
    target = None
    if target_stage in {stage.value for stage in PUBLIC_TARGET_STAGES}:
        occurrence_kind = STAGE_POLICY_BY_STAGE[target_stage].occurrence_rule.value
        target = {
            "stage": target_stage,
            "occurrence": {"kind": occurrence_kind},
        }
    authorization_boundary = {
        "authoring-through-plan-review": AuthorizationClass.AUTHORING.value,
        "implementation-through-verify": AuthorizationClass.IMPLEMENTATION.value,
        "bounded-review-fix": AuthorizationClass.AUTHORING.value,
    }.get(str(mechanism))
    source_identity = projection.get("source_record_identity")
    state = record.get("state", record.get("status"))
    return {
        **copy.deepcopy(dict(projection)),
        "mechanism": "bounded-review-fix",
        "target": target,
        "authorization_boundary": authorization_boundary,
        "effective_capability_kind": None,
        "canonical_position_source": "legacy-projection",
        "latest_evidence_identities": (
            {"legacy": source_identity}
            if isinstance(source_identity, str)
            else {}
        ),
        "transition_history": [],
        "fixes_applied": [],
        "artifacts_changed": [],
        "run_status": (
            "completed"
            if state in {"completed", "complete"}
            else "cancelled"
            if state in {"cancelled", "off", "inactive", "stopped"}
            else "active"
        ),
    }


def _public_command_result(
    projection: Mapping[str, Any],
    *,
    stage_outcome: str,
) -> dict[str, Any]:
    review = projection.get("latest_review_result")
    review_result = review if isinstance(review, Mapping) else {}
    run_status = projection.get("run_status")
    stop_reason = projection.get("stop_reason") or projection.get("pause_reason")
    next_action = {
        "cancelled": "explicit-stage-invocation",
        "completed": "none",
        "no-active-run": "select-target",
    }.get(str(run_status), "evaluate-next-stage")
    result = copy.deepcopy(dict(projection))
    result.update({
        "mechanism": projection.get("mechanism"),
        "structured_target": copy.deepcopy(projection.get("target")),
        "canonical_position_source": projection.get("canonical_position_source"),
        "active_parent_authorization_class": copy.deepcopy(
            projection.get("authorization_boundary")
        ),
        "effective_capability_kind": copy.deepcopy(
            projection.get("effective_capability_kind")
        ),
        "stage_outcome": stage_outcome,
        "review_outcome": review_result.get("outcome"),
        "clean_gate_state": review_result.get("clean_gate"),
        "transitions_attempted": copy.deepcopy(
            projection.get("transition_history", [])
        ),
        "fixes_applied": copy.deepcopy(projection.get("fixes_applied", [])),
        "human_decisions_required": (
            [stop_reason]
            if run_status == "paused" and isinstance(stop_reason, str)
            else []
        ),
        "artifacts_changed": copy.deepcopy(
            projection.get("artifacts_changed", [])
        ),
        "stop_reason": stop_reason,
        "next_action": next_action,
    })
    return result


def execute_public_control_command(
    store: WorkflowAutomationStateStore,
    command: str,
    *,
    actor: str,
    occurred_at: str,
    completion_evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute public ``status`` or ``off`` without a legacy write path."""

    normalized = normalize_command(command)
    if normalized.action not in {"status", "off"}:
        raise AutomationContractError("public control command must be status or off")
    if not isinstance(actor, str) or not actor.strip():
        raise AutomationContractError("public control command actor is required")
    if not RFC3339_UTC_RE.fullmatch(occurred_at):
        raise AutomationContractError(
            "public control command time must be RFC3339 UTC"
        )
    if normalized.action == "status":
        status = store.status()
        if status.get("source") == "legacy-read-only":
            status = _legacy_public_projection(status)
        return _public_command_result(status, stage_outcome="status")

    before = store.status()
    if before.get("source") == "legacy-read-only":
        legacy = before.get("legacy")
        if not isinstance(legacy, dict):
            raise AutomationContractError("legacy status projection is incomplete")
        try:
            mechanism, record = store._select_legacy_record(legacy)
        except StateContractError as error:
            raise AutomationContractError(str(error)) from error
        target_stage = {
            "authoring-through-plan-review": WorkflowStage.DELIVERY_REVIEW.value,
            "implementation-through-verify": WorkflowStage.VERIFY.value,
        }.get(mechanism)
        if target_stage is None and mechanism == "bounded-review-fix":
            candidate = record.get("target_stage")
            if isinstance(candidate, str):
                target_stage = candidate
        if target_stage is None:
            raise AutomationContractError(
                f"unsupported legacy automation mechanism: {mechanism}"
            )
        source_identity = before.get("source_record_identity")
        if not isinstance(source_identity, str) or ":" not in source_identity:
            raise AutomationContractError("legacy source identity is missing")
        target = bind_target(target_stage, bound_at=occurred_at)
        run_id = f"run-migrated-{source_identity.split(':', 1)[1][:16]}"
        legacy_snapshot = store.read(allow_legacy_without_change_id=True)
        cancelled = {
            "mechanism": "bounded-review-fix",
            "schema_version": 1,
            "run": {
                "run_id": run_id,
                "change_id": legacy_snapshot.document.get("change_id"),
                "status": "cancelled",
                "policy_version": 1,
                "target": target,
                "stop_reason": "run-cancelled",
            },
            "parent_authorizations": {},
            "effective_capabilities": {},
            "transition_receipts": {},
            "canonical_position_source": "legacy-projection",
            "observed_identities": {"legacy": source_identity},
            "cancellation": {
                "cancelled_by": actor,
                "cancelled_at": occurred_at,
                "reason": "run-cancelled",
            },
            "external_actions": "prohibited",
        }
        mutation = store.cancel_legacy(
            cancelled,
            cancelled_at=occurred_at,
            expected_document_identity=legacy_snapshot.document_identity,
        )
        if mutation.mutated:
            projection = store.status()
        else:
            projection = _legacy_public_projection(before)
            projection["run_status"] = (
                "completed"
                if mutation.status == "already-completed"
                else "cancelled"
            )
            projection["stop_reason"] = (
                "already-completed"
                if mutation.status == "already-completed"
                else "run-cancelled"
            )
        return _public_command_result(
            projection,
            stage_outcome=mutation.status,
        )

    mutation = store.cancel(
        cancelled_by=actor,
        cancelled_at=occurred_at,
        completion_evidence=(
            copy.deepcopy(dict(completion_evidence))
            if completion_evidence is not None
            else None
        ),
    )
    projection = store.status()
    return _public_command_result(projection, stage_outcome=mutation.status)


def start_public_run(
    store: WorkflowAutomationStateStore,
    command: str,
    *,
    run_id: str,
    actor: str,
    occurred_at: str,
    pre_plan: PrePlanEvidence | None = None,
    plan: ActivePlanContext | None = None,
    proposal_correction_budget: Mapping[str, int] | None = None,
    implementation_basis: Mapping[str, Any] | None = None,
    implementation_path_roots: Iterable[str] = (),
    implementation_correction_budget: Mapping[str, int] | None = None,
    verification_basis: Mapping[str, Any] | None = None,
    verification_basis_paths: Mapping[str, Any] | None = None,
    code_state_provider: CodeStateProvider | None = None,
) -> dict[str, Any]:
    """Persist one new public target and its currently valid consent envelope."""

    snapshot = store.read(allow_legacy_without_change_id=True)
    lifecycle_contract = _change_lifecycle_contract(snapshot.document)
    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError("public run creation requires a target command")
    if not all(
        isinstance(value, str) and value.strip()
        for value in (run_id, actor)
    ):
        raise AutomationContractError("public run identity and actor are required")
    if not RFC3339_UTC_RE.fullmatch(occurred_at):
        raise AutomationContractError("public run time must be RFC3339 UTC")

    if snapshot.automation is not None:
        raise AutomationContractError("active writable automation run already exists")
    change_id = snapshot.document.get("change_id")
    if not isinstance(change_id, str) or not change_id.strip():
        raise AutomationContractError("change identity is required before automation")

    target = bind_target(
        normalized.target_stage,
        bound_at=occurred_at,
        plan=plan,
        lifecycle_contract=lifecycle_contract,
    )
    canonical = resolve_canonical_position(
        pre_plan=pre_plan,
        active_plan=plan,
    )
    parents: dict[str, Any] = {}
    target_policy = stage_policy_by_stage_for_contract(lifecycle_contract)[normalized.target_stage]
    if target_policy.required_authorization_class == AuthorizationClass.AUTHORING:
        authorization_id = f"authorization-authoring-{run_id}"
        authoring_kinds = [
            CapabilityKind.PROPOSAL_REVIEW.value,
            CapabilityKind.POST_PROPOSAL_AUTHORING.value,
        ]
        authoring_categories = [
            "change-local-review-evidence",
            "downstream-authoring-artifacts",
            "change-local-evidence",
        ]
        if proposal_correction_budget is not None:
            authoring_kinds.insert(
                1, CapabilityKind.PROPOSAL_CORRECTION.value
            )
            authoring_categories.append("proposal-content")
        parent = create_parent_authorization(
            authorization_id=authorization_id,
            authorization_class=AuthorizationClass.AUTHORING.value,
            change_id=change_id,
            authorized_by=actor,
            authorized_at=occurred_at,
            maximum_target=target,
            allowed_capability_kinds=authoring_kinds,
            maximum_path_roots=(
                "docs/proposals/",
                "specs/",
                "docs/architecture/",
                "docs/adr/",
                "docs/plans/",
                f"docs/changes/{change_id}/",
            ),
            maximum_mutation_categories=authoring_categories,
            correction_budget=proposal_correction_budget,
        )
        parents[authorization_id] = parent
    if normalized.target_stage in {
        WorkflowStage.IMPLEMENT.value,
        WorkflowStage.CODE_REVIEW.value,
        WorkflowStage.VERIFY.value,
    } and implementation_basis is not None:
        if not _basis_complete(
            CapabilityKind.IMPLEMENTATION.value,
            implementation_basis,
        ):
            raise AutomationContractError(
                "implementation authorization basis is incomplete"
            )
        implementation_roots = _require_nonempty_strings(
            implementation_path_roots,
            "implementation authorization path roots",
        )
        authorization_id = f"authorization-implementation-{run_id}"
        implementation_kinds = [CapabilityKind.IMPLEMENTATION.value]
        implementation_categories = [
            "tests",
            "production-code",
            "change-local-review-evidence",
        ]
        if implementation_correction_budget is not None:
            implementation_kinds.append(
                CapabilityKind.IMPLEMENTATION_CORRECTION.value
            )
            implementation_categories.append("change-local-evidence")
        parents[authorization_id] = create_parent_authorization(
            authorization_id=authorization_id,
            authorization_class=AuthorizationClass.IMPLEMENTATION.value,
            change_id=change_id,
            authorized_by=actor,
            authorized_at=occurred_at,
            maximum_target=target,
            allowed_capability_kinds=implementation_kinds,
            maximum_path_roots=implementation_roots,
            maximum_mutation_categories=implementation_categories,
            correction_budget=implementation_correction_budget,
        )
    if (
        normalized.target_stage == WorkflowStage.VERIFY.value
        and verification_basis is not None
    ):
        if not _basis_complete(
            CapabilityKind.VERIFICATION.value,
            verification_basis,
        ):
            raise AutomationContractError(
                "verification authorization basis is incomplete"
            )
        if verification_basis_paths is None:
            raise AutomationContractError(
                "repository-backed verification basis is required"
            )
        try:
            repository_root = store.require_repository_root(
                store.repository_root
            )
        except StateContractError as error:
            raise AutomationContractError(str(error)) from error
        readiness = resolve_verification_readiness(
            repository_root=repository_root,
            basis=verification_basis,
            basis_paths=verification_basis_paths,
            code_state_provider=code_state_provider,
        )
        authorization_id = f"authorization-verification-{run_id}"
        parents[authorization_id] = create_parent_authorization(
            authorization_id=authorization_id,
            authorization_class=AuthorizationClass.VERIFICATION.value,
            change_id=change_id,
            authorized_by=actor,
            authorized_at=occurred_at,
            maximum_target=target,
            allowed_capability_kinds=(CapabilityKind.VERIFICATION.value,),
            maximum_path_roots=(f"docs/changes/{change_id}/",),
            maximum_mutation_categories=("verification-evidence",),
            verification_basis=readiness.basis_identities,
        )

    automation = {
        "mechanism": "bounded-review-fix",
        "schema_version": 1,
        "run": {
            "run_id": run_id,
            "change_id": change_id,
            "status": "active",
            "policy_version": 1,
            "target": target,
        },
        "parent_authorizations": parents,
        "effective_capabilities": {},
        "transition_receipts": {},
        "canonical_position_source": canonical.source,
        "observed_identities": copy.deepcopy(canonical.observed_identities),
        "external_actions": "prohibited",
    }
    workflow = snapshot.document.get("workflow")
    legacy = workflow.get("autoprogression") if isinstance(workflow, Mapping) else None
    try:
        if isinstance(legacy, Mapping):
            store.migrate_legacy(
                automation,
                migrated_at=occurred_at,
                expected_document_identity=snapshot.document_identity,
            )
        else:
            store.replace_automation(
                automation,
                expected_document_identity=snapshot.document_identity,
            )
    except StateContractError as error:
        raise AutomationContractError(str(error)) from error
    return _public_command_result(store.status(), stage_outcome="target-selected")


def authorize_public_run(
    store: WorkflowAutomationStateStore,
    command: str,
    *,
    authorization_id: str,
    authorization_class: str,
    actor: str,
    occurred_at: str,
    proposal_correction_budget: Mapping[str, int] | None = None,
    implementation_basis: Mapping[str, Any] | None = None,
    implementation_path_roots: Iterable[str] = (),
    implementation_correction_budget: Mapping[str, int] | None = None,
    verification_basis: Mapping[str, Any] | None = None,
    repository_root: Path | None = None,
    verification_basis_paths: Mapping[str, Any] | None = None,
    code_state_provider: CodeStateProvider | None = None,
) -> dict[str, Any]:
    """Add one current risk-class consent envelope to an existing public run."""

    snapshot = store.read()
    lifecycle_contract = _change_lifecycle_contract(snapshot.document)
    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError(
            "public authorization requires a target command"
        )
    auth_class = _authorization_class(authorization_class)
    if (
        normalized.legacy
        and normalized.target_stage == WorkflowStage.VERIFY.value
        and auth_class == AuthorizationClass.AUTHORING
    ):
        raise AutomationContractError(
            "legacy verify adapter must not infer authoring authority"
        )
    if snapshot.automation is None:
        raise AutomationContractError("unified automation state does not exist")
    run = snapshot.automation.get("run")
    if (
        not isinstance(run, Mapping)
        or run.get("status") not in {"active", "paused"}
    ):
        raise AutomationContractError(
            "public authorization requires an active or paused run"
        )
    target = run.get("target")
    if (
        not isinstance(target, Mapping)
        or target.get("stage") != normalized.target_stage
    ):
        raise AutomationContractError(
            "public authorization target does not match persisted target"
        )
    parents = snapshot.automation.get("parent_authorizations")
    if not isinstance(parents, Mapping):
        raise AutomationContractError("public authorization state is invalid")
    if authorization_id in parents:
        raise AutomationContractError("parent authorization identity already exists")
    if any(
        isinstance(parent, Mapping)
        and parent.get("status") == "active"
        and parent.get("authorization_class") == auth_class.value
        for parent in parents.values()
    ):
        raise AutomationContractError(
            "active parent authorization already exists for risk class"
        )
    change_id = run.get("change_id")
    if not isinstance(change_id, str):
        raise AutomationContractError("automation change identity is missing")
    if auth_class == AuthorizationClass.AUTHORING:
        kinds = [
            CapabilityKind.PROPOSAL_REVIEW.value,
            CapabilityKind.POST_PROPOSAL_AUTHORING.value,
        ]
        categories = [
            "change-local-review-evidence",
            "downstream-authoring-artifacts",
            "change-local-evidence",
        ]
        if proposal_correction_budget is not None:
            kinds.insert(1, CapabilityKind.PROPOSAL_CORRECTION.value)
            categories.append("proposal-content")
        parent = create_parent_authorization(
            authorization_id=authorization_id,
            authorization_class=auth_class.value,
            change_id=change_id,
            authorized_by=actor,
            authorized_at=occurred_at,
            maximum_target=target,
            allowed_capability_kinds=kinds,
            maximum_path_roots=(
                "docs/proposals/",
                "specs/",
                "docs/architecture/",
                "docs/adr/",
                "docs/plans/",
                f"docs/changes/{change_id}/",
            ),
            maximum_mutation_categories=categories,
            correction_budget=proposal_correction_budget,
        )
    elif auth_class == AuthorizationClass.IMPLEMENTATION:
        if implementation_basis is None or not _basis_complete(
            CapabilityKind.IMPLEMENTATION.value,
            implementation_basis,
        ):
            raise AutomationContractError(
                "implementation authorization basis is incomplete"
            )
        roots = _require_nonempty_strings(
            implementation_path_roots,
            "implementation authorization path roots",
        )
        kinds = [CapabilityKind.IMPLEMENTATION.value]
        categories = [
            "tests",
            "production-code",
            "change-local-review-evidence",
        ]
        if implementation_correction_budget is not None:
            kinds.append(CapabilityKind.IMPLEMENTATION_CORRECTION.value)
            categories.append("change-local-evidence")
        parent = create_parent_authorization(
            authorization_id=authorization_id,
            authorization_class=auth_class.value,
            change_id=change_id,
            authorized_by=actor,
            authorized_at=occurred_at,
            maximum_target=target,
            allowed_capability_kinds=kinds,
            maximum_path_roots=roots,
            maximum_mutation_categories=categories,
            correction_budget=implementation_correction_budget,
        )
    else:
        if verification_basis is None or not _basis_complete(
            CapabilityKind.VERIFICATION.value,
            verification_basis,
        ):
            raise AutomationContractError(
                "verification authorization basis is incomplete"
            )
        if repository_root is None or verification_basis_paths is None:
            raise AutomationContractError(
                "repository-backed verification basis is required"
            )
        try:
            repository_root = store.require_repository_root(repository_root)
        except StateContractError as error:
            raise AutomationContractError(str(error)) from error
        readiness = resolve_verification_readiness(
            repository_root=repository_root,
            basis=verification_basis,
            basis_paths=verification_basis_paths,
            code_state_provider=code_state_provider,
        )
        parent = create_parent_authorization(
            authorization_id=authorization_id,
            authorization_class=auth_class.value,
            change_id=change_id,
            authorized_by=actor,
            authorized_at=occurred_at,
            maximum_target=target,
            allowed_capability_kinds=(CapabilityKind.VERIFICATION.value,),
            maximum_path_roots=(f"docs/changes/{change_id}/",),
            maximum_mutation_categories=("verification-evidence",),
            verification_basis=readiness.basis_identities,
        )
    replacement = copy.deepcopy(snapshot.automation)
    replacement["parent_authorizations"][authorization_id] = parent
    if run.get("status") == "paused":
        pause_reason = run.get("pause_reason")
        accepted_pause_reasons = {
            AuthorizationClass.AUTHORING: {
                "authoring-authorization-required",
                "proposal-review-authorization-required",
            },
            AuthorizationClass.IMPLEMENTATION: {
                "implementation-authorization-required",
            },
            AuthorizationClass.VERIFICATION: {
                "verification-authorization-required",
            },
        }[auth_class]
        if pause_reason in accepted_pause_reasons:
            replacement["run"]["status"] = "active"
            replacement["run"].pop("pause_reason", None)
    try:
        store.replace_automation(
            replacement,
            expected_document_identity=snapshot.document_identity,
        )
    except StateContractError as error:
        raise AutomationContractError(str(error)) from error
    return _public_command_result(
        store.status(),
        stage_outcome="authorization-recorded",
    )


def resume_public_run(
    store: WorkflowAutomationStateStore,
    command: str,
    *,
    repository_root: Path,
    stage: str,
    **coordination: Any,
) -> dict[str, Any]:
    """Execute one public stage through the persisted target and consent envelope."""

    snapshot = store.read()
    lifecycle_contract = _change_lifecycle_contract(snapshot.document)
    normalized = normalize_command(command, lifecycle_contract=lifecycle_contract)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError("public resume requires a target command")
    if snapshot.automation is None:
        raise AutomationContractError("unified automation state does not exist")
    run = snapshot.automation.get("run")
    if not isinstance(run, Mapping) or run.get("status") != "active":
        raise AutomationContractError("public resume requires an active run")
    target = run.get("target")
    if (
        not isinstance(target, Mapping)
        or target.get("stage") != normalized.target_stage
    ):
        raise AutomationContractError(
            "public resume command does not match the persisted structured target"
        )
    policy = stage_policy_by_stage_for_contract(lifecycle_contract).get(stage)
    if policy is None:
        raise AutomationContractError(f"unknown public stage operation: {stage}")
    if not can_operation_fit_target(
        WorkflowStage(stage),
        WorkflowStage(normalized.target_stage),
        lifecycle_contract=lifecycle_contract,
    ):
        raise AutomationContractError(
            "public stage operation exceeds the persisted structured target"
        )
    parents = snapshot.automation.get("parent_authorizations")
    candidates = [
        parent
        for parent in parents.values()
        if isinstance(parents, Mapping)
        and isinstance(parent, Mapping)
        and parent.get("status") == "active"
        and parent.get("authorization_class")
        == policy.required_authorization_class.value
        and policy.capability_kind.value
        in parent.get("allowed_capability_kinds", [])
    ] if isinstance(parents, Mapping) else []
    if (
        len(candidates) == 0
        and policy.required_authorization_class
        == AuthorizationClass.VERIFICATION
    ):
        try:
            store.pause_run(
                reason="verification-authorization-required",
                expected_document_identity=snapshot.document_identity,
            )
        except StateContractError as error:
            raise AutomationContractError(str(error)) from error
        result = _public_command_result(
            store.status(),
            stage_outcome="paused",
        )
        result["stop_reason"] = "verification-authorization-required"
        result["human_decisions_required"] = [
            "verification-authorization-required"
        ]
        result["next_action"] = "explicit-user-decision"
        return result
    if len(candidates) != 1:
        raise AutomationContractError(
            "public resume requires exactly one matching active parent authorization"
        )
    parent_id = candidates[0].get("authorization_id")
    if not isinstance(parent_id, str):
        raise AutomationContractError(
            "public parent authorization identity is missing"
        )
    request = dict(coordination)
    if "parent_authorization_id" in request:
        raise AutomationContractError(
            "public resume selects parent authorization from durable state"
        )
    if "previously_observed" in request:
        raise AutomationContractError(
            "public resume selects observed identities from durable state"
        )
    observed = snapshot.automation.get("observed_identities")
    if not isinstance(observed, Mapping) or any(
        not isinstance(name, str)
        or not isinstance(identity, str)
        or not identity
        for name, identity in observed.items()
    ):
        raise AutomationContractError(
            "public resume durable observed identities are invalid"
        )
    request["parent_authorization_id"] = parent_id
    request["previously_observed"] = dict(observed)
    request["stage"] = stage
    try:
        if policy.capability_kind == CapabilityKind.IMPLEMENTATION_CORRECTION:
            request.pop("stage", None)
            target_occurrence = target.get("occurrence")
            milestone_id = (
                target_occurrence.get("milestone_id")
                if isinstance(target_occurrence, Mapping)
                else None
            )
            coordinated = coordinate_public_implementation_correction(
                command=command,
                target_milestone_id=milestone_id,
                store=store,
                repository_root=repository_root,
                **request,
            )
        elif policy.required_authorization_class == AuthorizationClass.AUTHORING:
            coordinated = coordinate_public_authoring_stage(
                command=command,
                store=store,
                repository_root=repository_root,
                **request,
            )
        else:
            target_occurrence = target.get("occurrence")
            target_milestone_id = (
                target_occurrence.get("milestone_id")
                if isinstance(target_occurrence, Mapping)
                else None
            )
            coordinated = coordinate_public_implementation_stage(
                command=command,
                target_milestone_id=target_milestone_id,
                store=store,
                repository_root=repository_root,
                **request,
            )
    except AutomationContractError as error:
        if "canonical-state-mismatch:" not in str(error):
            raise
        replacement = copy.deepcopy(snapshot.automation)
        replacement["run"]["status"] = "paused"
        replacement["run"]["pause_reason"] = "canonical-state-mismatch"
        try:
            store.replace_automation(
                replacement,
                expected_document_identity=snapshot.document_identity,
            )
        except StateContractError as state_error:
            raise AutomationContractError(str(state_error)) from state_error
        raise
    projection = store.status()
    result = _public_command_result(
        projection,
        stage_outcome=coordinated.route.status,
    )
    if coordinated.route.pause_reason is not None:
        result["stop_reason"] = coordinated.route.pause_reason
        result["human_decisions_required"] = [coordinated.route.pause_reason]
        result["next_action"] = "explicit-user-decision"
    elif coordinated.route.next_stage is not None:
        result["next_action"] = coordinated.route.next_stage
    elif coordinated.route.status in {"target-reached", "target-not-applicable"}:
        result["next_action"] = "none"
    return result


def resume_target(
    persisted_target: Mapping[str, Any],
    *,
    current_plan: ActivePlanContext | None = None,
) -> dict[str, Any]:
    """Return the persisted occurrence without silently rebinding it."""

    if not isinstance(persisted_target, Mapping):
        raise AutomationContractError("persisted target must be an object")
    stage = persisted_target.get("stage")
    parsed = _target_stage(stage) if isinstance(stage, str) else None
    if parsed is None:
        raise AutomationContractError("persisted target stage is missing")
    policy = STAGE_POLICY_BY_STAGE[parsed.value]
    occurrence = persisted_target.get("occurrence")
    if not isinstance(occurrence, Mapping) or occurrence.get("kind") != policy.occurrence_rule.value:
        raise AutomationContractError("persisted target occurrence is incompatible")
    bound_at = persisted_target.get("bound_at")
    if not isinstance(bound_at, str) or not RFC3339_UTC_RE.fullmatch(bound_at):
        raise AutomationContractError("persisted target binding time is invalid")
    completion = persisted_target.get("completion")
    if completion != target_completion_predicate(parsed):
        raise AutomationContractError("persisted target completion predicate is incompatible")
    if policy.occurrence_rule == OccurrenceKind.MILESTONE:
        if not occurrence.get("milestone_id") or not persisted_target.get("plan_identity"):
            raise AutomationContractError("persisted repeated target identity is incomplete")
    # current_plan is deliberately not consulted for rebinding.
    _ = current_plan
    return copy.deepcopy(dict(persisted_target))


def _one_identity(position: str, identities: Iterable[str]) -> str:
    values = tuple(identities)
    if len(values) != 1 or not isinstance(values[0], str) or not values[0].strip():
        raise AutomationContractError(f"ambiguous canonical evidence for {position}")
    return values[0]


def _resolve_pre_plan(evidence: PrePlanEvidence) -> CanonicalPosition:
    unknown = set(evidence.positions) - set(PRE_PLAN_SEQUENCE)
    if unknown:
        raise AutomationContractError(
            "unknown pre-plan workflow position: " + ", ".join(sorted(unknown))
        )
    unknown_review_positions = set(evidence.review_outcomes) - REVIEW_POSITIONS
    if unknown_review_positions:
        raise AutomationContractError(
            "unknown review position: " + ", ".join(sorted(unknown_review_positions))
        )
    unknown_outcomes = set(evidence.review_outcomes.values()) - REVIEW_OUTCOMES
    if unknown_outcomes:
        raise AutomationContractError(
            "unknown review outcome: " + ", ".join(sorted(unknown_outcomes))
        )
    unknown_transitions = set(evidence.transition_identities) - TRANSITION_EVIDENCE_POSITIONS
    if unknown_transitions:
        raise AutomationContractError(
            "unknown transition evidence: " + ", ".join(sorted(unknown_transitions))
        )
    if any(
        not isinstance(identity, str) or not identity.strip()
        for identity in evidence.transition_identities.values()
    ):
        raise AutomationContractError("transition evidence requires concrete identities")
    observed = {
        position: _one_identity(position, identities)
        for position, identities in evidence.positions.items()
    }
    for position, identity in evidence.transition_identities.items():
        observed[f"transition:{position}"] = identity
    if set(observed.values()) & set(evidence.stale_identities):
        raise AutomationContractError("stale canonical workflow evidence")

    if "architecture" in observed and evidence.review_outcomes.get("proposal-review") != "approved":
        raise AutomationContractError("contradictory proposal-review evidence")
    if "plan" in observed and evidence.review_outcomes.get("design-review") != "approved":
        raise AutomationContractError("contradictory design-review evidence")
    if "architecture" in observed and not evidence.review_resolution_closed:
        raise AutomationContractError("required review resolution is not closed")

    applicable_sequence = list(PRE_PLAN_SEQUENCE)
    positions = [position for position in applicable_sequence if position in evidence.positions]
    if not positions:
        return CanonicalPosition(
            WorkflowPosition.CHANGE_CREATED.value,
            "authoritative-artifact-review-evidence",
            {},
        )
    highest = positions[-1]
    highest_index = applicable_sequence.index(highest)
    required_prefix = applicable_sequence[: highest_index + 1]
    if any(position not in observed for position in required_prefix):
        raise AutomationContractError("contradictory or incomplete pre-plan evidence")
    return CanonicalPosition(
        highest,
        "authoritative-artifact-review-evidence",
        observed,
    )


def _resolve_plan(plan: ActivePlanContext) -> CanonicalPosition:
    candidates = plan.current_candidates()
    if len(candidates) != 1:
        if candidates or not _all_implementation_milestones_closed(plan):
            raise AutomationContractError("active plan current milestone is ambiguous")
        final_predecessors = {
            WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW.value: WorkflowPosition.CODE_REVIEW.value,
            WorkflowStage.CI_MAINTENANCE.value: WorkflowPosition.CODE_REVIEW.value,
            WorkflowStage.REVIEW_RESOLUTION.value: WorkflowPosition.FINAL_HOLISTIC_CODE_REVIEW.value,
            WorkflowStage.VERIFY.value: WorkflowPosition.FINAL_HOLISTIC_CODE_REVIEW.value,
            "pr": WorkflowPosition.VERIFY.value,
        }
        position = final_predecessors.get(plan.handoff.next_stage)
        if position is None:
            raise AutomationContractError(
                "active plan final-closeout next stage is ambiguous"
            )
        return CanonicalPosition(
            position,
            "plan-current-handoff-summary",
            {"plan": plan.plan_identity},
        )
    current = candidates[0]
    state = current.state
    authoring_position = (
        {WorkflowStage.DELIVERY_REVIEW.value: WorkflowPosition.PLAN.value}.get(
            plan.handoff.next_stage
        )
        if state == "planned"
        else None
    )
    if authoring_position is not None:
        return CanonicalPosition(
            authoring_position,
            "plan-current-handoff-summary",
            {"plan": plan.plan_identity},
            milestone_id=current.milestone_id,
        )
    if state == "review-requested":
        position = WorkflowPosition.IMPLEMENT.value
    elif state == "resolution-needed":
        position = WorkflowPosition.CODE_REVIEW.value
    elif state in {"planned", "implementing"}:
        index = plan.milestones.index(current)
        prior = plan.milestones[:index]
        position = (
            WorkflowPosition.CODE_REVIEW.value
            if any(milestone.state == "closed" for milestone in prior)
            else WorkflowPosition.DELIVERY_REVIEW.value
        )
    else:
        position = WorkflowPosition.CODE_REVIEW.value
    expected_next = {
        "planned": f"implement {current.milestone_id}",
        "implementing": f"implement {current.milestone_id}",
        "review-requested": f"code-review {current.milestone_id}",
        "resolution-needed": f"review-resolution {current.milestone_id}",
    }.get(state)
    if expected_next is not None and plan.handoff.next_stage != expected_next:
        raise AutomationContractError(
            f"active plan next stage does not match current milestone: expected {expected_next}"
        )
    return CanonicalPosition(
        position,
        "plan-current-handoff-summary",
        {"plan": plan.plan_identity},
        milestone_id=current.milestone_id,
    )


def resolve_canonical_position(
    *,
    pre_plan: PrePlanEvidence | None = None,
    active_plan: ActivePlanContext | None = None,
    previously_observed: Mapping[str, str] | None = None,
) -> CanonicalPosition:
    """Resolve canonical position without persisting an automation cursor."""

    if (pre_plan is None) == (active_plan is None):
        raise AutomationContractError("exactly one canonical position epoch is required")
    result = _resolve_plan(active_plan) if active_plan is not None else _resolve_pre_plan(pre_plan)  # type: ignore[arg-type]
    if previously_observed is not None:
        for name, identity in previously_observed.items():
            current = result.observed_identities.get(name)
            if current is None or current != identity:
                raise AutomationContractError(f"canonical-state-mismatch: {name}")
    return result


def record_plan_ownership_handoff(
    pre_plan: PrePlanEvidence,
    active_plan: ActivePlanContext,
) -> dict[str, Any]:
    """Record the evidence identities establishing the plan ownership handoff."""

    _resolve_pre_plan(pre_plan)
    _resolve_plan(active_plan)
    observed = {
        position: _one_identity(position, identities)
        for position, identities in pre_plan.positions.items()
    }
    return {
        "pre_plan_evidence": observed,
        "transition_identities": dict(pre_plan.transition_identities),
        "plan_identity": active_plan.plan_identity,
    }


def _authorization_class(value: str) -> AuthorizationClass:
    try:
        return AuthorizationClass(value)
    except (TypeError, ValueError) as exc:
        raise AutomationContractError(f"unknown authorization class: {value}") from exc


def _capability_kind(value: str) -> CapabilityKind:
    try:
        return CapabilityKind(value)
    except (TypeError, ValueError) as exc:
        raise AutomationContractError(f"unknown capability kind: {value}") from exc


def _require_nonempty_strings(values: Iterable[str], label: str) -> tuple[str, ...]:
    result = tuple(values)
    if not result or any(not isinstance(value, str) or not value.strip() for value in result):
        raise AutomationContractError(f"{label} requires non-empty values")
    return result


def _basis_complete(kind: str, basis: Mapping[str, Any]) -> bool:
    required = CAPABILITY_BASIS_FIELDS[kind]
    for name in required:
        value = basis.get(name)
        if name in CAPABILITY_BASIS_LIST_FIELDS:
            if not isinstance(value, (list, tuple)) or not value:
                return False
            if any(not isinstance(item, str) or not item.strip() for item in value):
                return False
        elif not isinstance(value, str) or not value.strip():
            return False
    return True


def create_parent_authorization(
    *,
    authorization_id: str,
    authorization_class: str,
    change_id: str,
    authorized_by: str,
    authorized_at: str,
    maximum_target: Mapping[str, Any],
    allowed_capability_kinds: Iterable[str],
    maximum_path_roots: Iterable[str],
    maximum_mutation_categories: Iterable[str],
    verification_basis: Mapping[str, Any] | None = None,
    correction_budget: Mapping[str, int] | None = None,
    policy_version: int = 1,
) -> dict[str, Any]:
    """Create a non-executable bounded consent envelope."""

    auth_class = _authorization_class(authorization_class)
    if not all(
        isinstance(value, str) and value.strip()
        for value in (authorization_id, change_id, authorized_by)
    ):
        raise AutomationContractError("parent authorization identity fields are required")
    if not RFC3339_UTC_RE.fullmatch(authorized_at):
        raise AutomationContractError("authorization time must be RFC3339 UTC")
    if policy_version != 1:
        raise AutomationContractError(f"unknown policy version: {policy_version!r}")
    target = resume_target(maximum_target)
    kinds = _require_nonempty_strings(allowed_capability_kinds, "allowed capability kinds")
    paths = _require_nonempty_strings(maximum_path_roots, "maximum path roots")
    categories = _require_nonempty_strings(
        maximum_mutation_categories, "maximum mutation categories"
    )
    parsed_kinds = tuple(_capability_kind(kind) for kind in kinds)
    for kind in parsed_kinds:
        expected = CAPABILITY_AUTHORIZATION_CLASSES[kind.value]
        if expected != auth_class.value:
            raise AutomationContractError("capability kind crosses authorization risk class")
    allowed_categories = {
        category.value
        for kind in parsed_kinds
        for category in CAPABILITY_MUTATION_CATEGORIES[kind]
    }
    if not set(categories).issubset(allowed_categories):
        raise AutomationContractError(
            "parent mutation categories exceed allowed capability policy"
        )
    if auth_class == AuthorizationClass.VERIFICATION:
        if verification_basis is None or not _basis_complete(
            CapabilityKind.VERIFICATION.value, verification_basis
        ):
            raise AutomationContractError(
                "future-contingent verification authorization is forbidden"
            )
    record: dict[str, Any] = {
        "authorization_id": authorization_id,
        "authorization_class": auth_class.value,
        "policy_version": policy_version,
        "change_id": change_id,
        "authorized_by": authorized_by,
        "authorized_at": authorized_at,
        "maximum_target": target,
        "allowed_capability_kinds": [kind.value for kind in parsed_kinds],
        "maximum_path_roots": list(paths),
        "maximum_mutation_categories": list(categories),
        "status": "active",
        "revocation": {"revoked": False},
        "invalidation": {"on_policy_change": "pause"},
        "external_actions": "prohibited",
    }
    correction_kinds = {
        CapabilityKind.PROPOSAL_CORRECTION,
        CapabilityKind.IMPLEMENTATION_CORRECTION,
    }
    if any(kind in correction_kinds for kind in parsed_kinds) and correction_budget is None:
        raise AutomationContractError("correction authority requires a correction budget")
    if correction_budget is not None:
        if any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for value in correction_budget.values()
        ):
            raise AutomationContractError("correction budget must use non-negative integers")
        record["correction_budget"] = dict(correction_budget)
    return record


def invalidate_effective_capabilities(
    capabilities: Iterable[Mapping[str, Any]],
    *,
    reason: str,
    parent_authorization_id: str | None = None,
    stage: str | None = None,
) -> tuple[dict[str, Any], ...]:
    """Return a new capability set with matching active authority invalidated."""

    if not isinstance(reason, str) or not reason.strip():
        raise AutomationContractError("capability invalidation reason is required")
    result: list[dict[str, Any]] = []
    for capability in capabilities:
        updated = copy.deepcopy(dict(capability))
        bound_stage = updated.get("stage")
        matches_parent = (
            parent_authorization_id is None
            or updated.get("parent_authorization_id") == parent_authorization_id
        )
        matches_stage = (
            stage is None
            or (isinstance(bound_stage, Mapping) and bound_stage.get("name") == stage)
        )
        if updated.get("status") == "active" and matches_parent and matches_stage:
            updated["status"] = "invalidated"
            updated["invalidation_reason"] = reason
        result.append(updated)
    return tuple(result)


def derive_effective_capability(
    *,
    capability_id: str,
    parent: Mapping[str, Any],
    stage: str,
    occurrence: Mapping[str, Any],
    basis: Mapping[str, Any],
    affected_path_roots: Iterable[str],
    mutation_categories: Iterable[str],
    derived_at: str,
    correction_budget: Mapping[str, int] | None = None,
    correction_budget_identity: str | None = None,
    implementation_correction_scope: Mapping[str, Any] | None = None,
    basis_current: bool = True,
    existing_capabilities: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Derive one basis-complete capability no broader than its parent."""

    if not isinstance(capability_id, str) or not capability_id.strip():
        raise AutomationContractError("capability identity is required")
    if not RFC3339_UTC_RE.fullmatch(derived_at):
        raise AutomationContractError("capability derivation time must be RFC3339 UTC")
    if parent.get("status") != "active" or parent.get("revocation", {}).get("revoked") is True:
        raise AutomationContractError("parent authorization is not active")
    if not basis_current:
        raise AutomationContractError("capability basis is stale")
    policy = STAGE_POLICY_BY_STAGE.get(stage)
    if policy is None:
        raise AutomationContractError(f"unknown capability stage: {stage}")
    kind = policy.capability_kind.value
    if parent.get("authorization_class") != policy.required_authorization_class.value:
        raise AutomationContractError("capability derivation crosses authorization risk class")
    if kind not in parent.get("allowed_capability_kinds", []):
        raise AutomationContractError("capability kind exceeds parent maximum")
    if stage not in CAPABILITY_STAGES[kind]:
        raise AutomationContractError("stage is incompatible with capability kind")
    if occurrence.get("kind") != policy.occurrence_rule.value:
        raise AutomationContractError("capability occurrence is incompatible with stage")
    if policy.occurrence_rule == OccurrenceKind.MILESTONE and not occurrence.get("milestone_id"):
        raise AutomationContractError("milestone capability requires milestone identity")
    if not _basis_complete(kind, basis):
        raise AutomationContractError("capability basis is incomplete")
    target = parent.get("maximum_target")
    if not isinstance(target, Mapping) or not isinstance(target.get("stage"), str):
        raise AutomationContractError("parent maximum target is invalid")
    operation = WorkflowStage(stage)
    target_stage = WorkflowStage(target["stage"])
    if not can_operation_fit_target(operation, target_stage):
        raise AutomationContractError("capability operation exceeds parent maximum target")
    if stage in {WorkflowStage.IMPLEMENT.value, WorkflowStage.CODE_REVIEW.value}:
        target_occurrence = target.get("occurrence")
        if target_stage == operation and (
            not isinstance(target_occurrence, Mapping)
            or target_occurrence.get("milestone_id") != occurrence.get("milestone_id")
        ):
            raise AutomationContractError("capability milestone exceeds parent occurrence")
    paths = _require_nonempty_strings(affected_path_roots, "capability path roots")
    categories = _require_nonempty_strings(
        mutation_categories, "capability mutation categories"
    )
    if not set(paths).issubset(set(parent.get("maximum_path_roots", []))):
        raise AutomationContractError("capability path roots exceed parent maximum")
    if not set(categories).issubset(set(parent.get("maximum_mutation_categories", []))):
        raise AutomationContractError("capability mutation categories exceed parent maximum")
    permitted = {
        category.value for category in policy.permitted_mutation_category
    }
    if not set(categories).issubset(permitted):
        raise AutomationContractError("capability mutation categories exceed stage policy")
    correction_kinds = {
        CapabilityKind.PROPOSAL_CORRECTION.value,
        CapabilityKind.IMPLEMENTATION_CORRECTION.value,
    }
    bounded_budget: dict[str, int] | None = None
    if kind in correction_kinds:
        parent_budget = parent.get("correction_budget")
        if not isinstance(parent_budget, Mapping) or not parent_budget:
            raise AutomationContractError("correction parent budget is missing")
        if any(
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
            for value in parent_budget.values()
        ):
            raise AutomationContractError("correction parent budget is invalid or exhausted")
        if not isinstance(correction_budget, Mapping) or not correction_budget:
            raise AutomationContractError("correction capability budget is required")
        if set(correction_budget) != set(parent_budget):
            raise AutomationContractError("correction capability budget dimensions mismatch")
        if any(
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
            or value > parent_budget[name]
            for name, value in correction_budget.items()
        ):
            raise AutomationContractError("correction capability budget is exhausted or expanded")
        if not isinstance(correction_budget_identity, str) or not correction_budget_identity.strip():
            raise AutomationContractError("correction budget identity is required")
        basis_budget_identity = basis.get("correction_budget_identity")
        if basis_budget_identity != correction_budget_identity:
            raise AutomationContractError("correction budget identity is stale")
        bounded_budget = dict(correction_budget)
    elif correction_budget is not None or correction_budget_identity is not None:
        raise AutomationContractError("non-correction capability cannot carry correction budget")
    for existing in existing_capabilities:
        if existing.get("capability_id") == capability_id:
            raise AutomationContractError("capability identity already exists")
        if existing.get("status") != "active":
            continue
        existing_stage = existing.get("stage")
        if (
            isinstance(existing_stage, Mapping)
            and existing_stage.get("name") == stage
            and existing_stage.get("occurrence") == occurrence
        ):
            raise AutomationContractError("conflicting active capability for stage occurrence")
    capability = {
        "capability_id": capability_id,
        "capability_kind": kind,
        "parent_authorization_id": parent["authorization_id"],
        "policy_version": parent["policy_version"],
        "change_id": parent["change_id"],
        "stage": {"name": stage, "occurrence": copy.deepcopy(dict(occurrence))},
        "basis": copy.deepcopy(dict(basis)),
        "scope": {
            "affected_path_roots": list(paths),
            "mutation_categories": list(categories),
        },
        "derived_at": derived_at,
        "status": "active",
        "invalidation": {"on_parent_revocation": "invalidate"},
    }
    if bounded_budget is not None:
        capability["scope"]["correction_budget"] = bounded_budget
        capability["scope"]["correction_budget_identity"] = correction_budget_identity
    if kind == CapabilityKind.IMPLEMENTATION_CORRECTION.value:
        if implementation_correction_scope is None:
            raise AutomationContractError(
                "implementation correction scope is required"
            )
        required_scope = {
            "review_record_path",
            "review_resolution_path",
            "review_log_path",
            "accepted_finding_ids",
            "reviewer_recipes",
            "reviewed_milestone_id",
        }
        if set(implementation_correction_scope) != required_scope:
            raise AutomationContractError(
                "implementation correction scope is incomplete"
            )
        capability["scope"].update(
            copy.deepcopy(dict(implementation_correction_scope))
        )
    elif implementation_correction_scope is not None:
        raise AutomationContractError(
            "implementation correction scope requires implementation-correction"
        )
    return capability


def persist_target(
    store: WorkflowAutomationStateStore,
    target: Mapping[str, Any],
    *,
    expected_document_identity: str,
) -> None:
    """Persist only the structured destination; do not manufacture authority."""

    snapshot = store.read()
    if snapshot.automation is None:
        raise AutomationContractError("unified automation state does not exist")
    prepared = [
        receipt
        for receipt in snapshot.automation.get("transition_receipts", {}).values()
        if isinstance(receipt, dict) and receipt.get("status") == "prepared"
    ]
    if prepared:
        raise AutomationContractError("transition already in flight")
    run = snapshot.automation.get("run")
    if not isinstance(run, dict) or run.get("status") in {"completed", "cancelled"}:
        raise AutomationContractError("terminal automation run cannot accept a new target")
    replacement = copy.deepcopy(snapshot.automation)
    replacement["run"]["target"] = resume_target(target)
    store.replace_automation(
        replacement, expected_document_identity=expected_document_identity
    )


def _bind_canonical_evidence(
    canonical: CanonicalPosition,
    *,
    basis: Mapping[str, Any],
    input_identities: Mapping[str, Any],
) -> None:
    for name, identity in basis.items():
        if input_identities.get(name) != identity:
            raise AutomationContractError(f"capability basis input mismatch: {name}")
    for name, identity in canonical.observed_identities.items():
        if input_identities.get(name) != identity:
            raise AutomationContractError(f"canonical identity mismatch: {name}")
        for basis_field in CANONICAL_BASIS_FIELDS.get(name, ()):
            if basis_field in basis and basis[basis_field] != identity:
                raise AutomationContractError(
                    f"canonical identity mismatch: {name} versus {basis_field}"
                )


def _serialize_evidence(evidence: ArtifactEvidence) -> dict[str, str]:
    return {"path": evidence.path, "identity": evidence.identity}


def _validate_artifact_evidence(
    evidence: Any,
    *,
    repository_root: Path,
    affected_path_roots: Iterable[str],
) -> ArtifactEvidence:
    if not isinstance(evidence, ArtifactEvidence):
        raise AutomationContractError("stage evidence requires a typed artifact reference")
    relative = Path(evidence.path)
    if relative.is_absolute() or not evidence.path or ".." in relative.parts:
        raise AutomationContractError("stage evidence path must be repository-relative")
    allowed_roots = tuple(Path(root) for root in affected_path_roots)
    if any(root.is_absolute() or ".." in root.parts for root in allowed_roots):
        raise AutomationContractError("capability evidence roots must be repository-relative")
    if not allowed_roots or not any(
        relative == root or relative.is_relative_to(root) for root in allowed_roots
    ):
        raise AutomationContractError("stage evidence path exceeds capability scope")
    root = repository_root.resolve()
    artifact = (root / relative).resolve()
    if not artifact.is_relative_to(root) or not artifact.is_file():
        raise AutomationContractError("stage evidence artifact does not exist")
    observed_identity = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()
    if evidence.identity != observed_identity:
        raise AutomationContractError("stage evidence identity does not match artifact")
    return evidence


def _validate_stage_result(
    result: Any,
    *,
    policy: Any,
    repository_root: Path,
    affected_path_roots: Iterable[str],
) -> StageExecutionResult:
    if not isinstance(result, StageExecutionResult):
        raise AutomationContractError("stage invocation requires a typed execution result")
    if not result.outputs:
        raise AutomationContractError("stage invocation requires concrete outputs")
    if set(result.completion_evidence) != set(policy.completion_evidence):
        raise AutomationContractError("stage completion evidence does not satisfy stage policy")
    for output in result.outputs:
        _validate_artifact_evidence(
            output,
            repository_root=repository_root,
            affected_path_roots=affected_path_roots,
        )
    for evidence in result.completion_evidence.values():
        _validate_artifact_evidence(
            evidence,
            repository_root=repository_root,
            affected_path_roots=affected_path_roots,
        )
    return result


def _validate_sync_result(
    result: Any,
    *,
    stage_result: StageExecutionResult,
    policy: Any,
    repository_root: Path,
    affected_path_roots: Iterable[str],
) -> CanonicalSyncResult:
    if not isinstance(result, CanonicalSyncResult):
        raise AutomationContractError("canonical synchronization requires a typed result")
    if result.status != "synchronized" or set(result.evidence) != set(
        policy.completion_evidence
    ):
        raise AutomationContractError("canonical synchronization did not complete")
    if dict(result.evidence) != dict(stage_result.completion_evidence):
        raise AutomationContractError("canonical synchronization evidence changed")
    for evidence in result.evidence.values():
        _validate_artifact_evidence(
            evidence,
            repository_root=repository_root,
            affected_path_roots=affected_path_roots,
        )
    return result


def coordinate_one_stage(
    *,
    store: WorkflowAutomationStateStore | None = None,
    parent_authorization_id: str | None = None,
    capability_id: str | None = None,
    stage: str | None = None,
    occurrence: Mapping[str, Any] | None = None,
    basis: Mapping[str, Any] | None = None,
    affected_path_roots: Iterable[str] = (),
    mutation_categories: Iterable[str] = (),
    correction_budget: Mapping[str, int] | None = None,
    correction_budget_identity: str | None = None,
    implementation_correction_scope: Mapping[str, Any] | None = None,
    derived_at: str | None = None,
    transition_id: str | None = None,
    input_identities: Mapping[str, Any] | None = None,
    invoke_stage: Callable[[], StageExecutionResult] | None = None,
    synchronize_canonical_state: Callable[[StageExecutionResult], CanonicalSyncResult] | None = None,
    repository_root: Path | None = None,
    pre_plan: PrePlanEvidence | None = None,
    active_plan: ActivePlanContext | None = None,
    previously_observed: Mapping[str, str] | None = None,
    recovery_completion_evidence: Mapping[str, Any] | None = None,
    parent_authorization: Mapping[str, Any] | None = None,
    post_completion_capabilities: Callable[
        [VerifiedCompletion, Mapping[str, Any], Mapping[str, Any]],
        Iterable[Mapping[str, Any]],
    ] | None = None,
) -> CoordinationResult:
    """Coordinate exactly one non-public stage operation through the M2 writer."""

    if parent_authorization is not None:
        raise AutomationContractError("parent authorization is non-executable")
    required = {
        "store": store,
        "parent_authorization_id": parent_authorization_id,
        "capability_id": capability_id,
        "stage": stage,
        "occurrence": occurrence,
        "basis": basis,
        "transition_id": transition_id,
        "input_identities": input_identities,
        "invoke_stage": invoke_stage,
        "synchronize_canonical_state": synchronize_canonical_state,
        "repository_root": repository_root,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        raise AutomationContractError(
            "one-stage coordination missing: " + ", ".join(sorted(missing))
        )
    assert store is not None
    assert parent_authorization_id is not None
    assert capability_id is not None
    assert stage is not None
    assert occurrence is not None
    assert basis is not None
    assert transition_id is not None
    assert input_identities is not None
    assert invoke_stage is not None
    assert synchronize_canonical_state is not None
    assert repository_root is not None
    try:
        repository_root = store.require_repository_root(repository_root)
    except StateContractError as error:
        raise AutomationContractError(str(error)) from error
    bounded_path_roots = tuple(affected_path_roots)
    bounded_mutation_categories = tuple(mutation_categories)

    snapshot = store.read()
    if snapshot.automation is None:
        raise AutomationContractError("unified automation state does not exist")
    lifecycle_contract = _change_lifecycle_contract(snapshot.document)
    prepared = [
        receipt
        for receipt in snapshot.automation.get("transition_receipts", {}).values()
        if isinstance(receipt, dict) and receipt.get("status") == "prepared"
    ]
    if len(prepared) > 1:
        raise AutomationContractError("multiple transitions are already in flight")
    prepared_receipt = prepared[0] if prepared else None
    if (
        prepared_receipt is None
        and recovery_completion_evidence is not None
    ):
        raise AutomationContractError(
            "recovery completion evidence requires a prepared transition"
        )
    if (
        prepared_receipt is not None
        and (
            prepared_receipt.get("transition_id") != transition_id
            or prepared_receipt.get("effective_capability_id")
            != capability_id
        )
    ):
        raise AutomationContractError(
            "transition already in flight and does not match requested recovery"
        )
    canonical = None
    if prepared_receipt is None or recovery_completion_evidence is None:
        canonical = resolve_canonical_position(
            pre_plan=pre_plan,
            active_plan=active_plan,
            previously_observed=previously_observed,
        )
        _bind_canonical_evidence(
            canonical,
            basis=basis,
            input_identities=input_identities,
        )
    parents = snapshot.automation.get("parent_authorizations")
    parent = parents.get(parent_authorization_id) if isinstance(parents, dict) else None
    if not isinstance(parent, dict):
        raise AutomationContractError("active parent authorization not found")
    capabilities = snapshot.automation.get("effective_capabilities")
    existing = tuple(capabilities.values()) if isinstance(capabilities, dict) else ()
    persisted_capability = (
        capabilities.get(capability_id) if isinstance(capabilities, dict) else None
    )
    if isinstance(persisted_capability, dict):
        scope = persisted_capability.get("scope")
        if (
            persisted_capability.get("status") != "active"
            or persisted_capability.get("parent_authorization_id") != parent_authorization_id
            or persisted_capability.get("stage")
            != {"name": stage, "occurrence": dict(occurrence)}
            or persisted_capability.get("basis") != dict(basis)
            or not isinstance(scope, dict)
            or scope.get("affected_path_roots") != list(bounded_path_roots)
            or scope.get("mutation_categories") != list(bounded_mutation_categories)
            or (
                implementation_correction_scope is not None
                and any(
                    scope.get(name) != value
                    for name, value in implementation_correction_scope.items()
                )
            )
        ):
            raise AutomationContractError(
                "persisted effective capability does not match stage request"
            )
        capability = copy.deepcopy(persisted_capability)
    else:
        if derived_at is None:
            raise AutomationContractError(
                "one-stage coordination missing: derived_at"
            )
        capability = derive_effective_capability(
            capability_id=capability_id,
            parent=parent,
            stage=stage,
            occurrence=occurrence,
            basis=basis,
            affected_path_roots=bounded_path_roots,
            mutation_categories=bounded_mutation_categories,
            correction_budget=correction_budget,
            correction_budget_identity=correction_budget_identity,
            implementation_correction_scope=implementation_correction_scope,
            derived_at=derived_at,
            existing_capabilities=existing,
        )
    policy = stage_policy_by_stage_for_contract(lifecycle_contract)[stage]
    expected_postcondition = {
        "completion_rule": policy.completion_rule,
        "required_evidence": sorted(policy.completion_evidence),
    }
    receipt = {
        "transition_id": transition_id,
        "transition_key": "pending",
        "policy_version": capability["policy_version"],
        "run_id": snapshot.automation["run"]["run_id"],
        "change_id": capability["change_id"],
        "from_position": (
            prepared_receipt["from_position"]
            if prepared_receipt is not None
            else canonical.position
        ),
        "target": copy.deepcopy(snapshot.automation["run"]["target"]),
        "effective_capability_id": capability_id,
        "retry_policy": policy.retry_policy.value,
        "input_identities": copy.deepcopy(dict(input_identities)),
        "expected_postcondition": copy.deepcopy(dict(expected_postcondition)),
        "status": "prepared",
        "outputs": [],
        "canonical_sync": {"status": "pending"},
    }
    receipt["transition_key"] = compute_transition_key(receipt)

    recovering_prepared = prepared_receipt is not None
    if recovering_prepared:
        assert prepared_receipt is not None
        if prepared_receipt.get("transition_key") != receipt["transition_key"]:
            raise AutomationContractError(
                "prepared transition inputs do not match the requested recovery"
            )
        decision = evaluate_receipt_recovery(
            snapshot.automation,
            transition_id,
            completion_evidence=(
                copy.deepcopy(dict(recovery_completion_evidence))
                if recovery_completion_evidence is not None
                else None
            ),
            repository_root=repository_root,
        )
        if decision.action == "reconcile-completed":
            proof = decision.verified_completion
            if proof is None:
                raise AutomationContractError(
                    "prepared transition recovery proof is missing"
                )
            activated_capabilities: tuple[dict[str, Any], ...] = ()
            if post_completion_capabilities is not None:
                activated_capabilities = tuple(
                    copy.deepcopy(dict(item))
                    for item in post_completion_capabilities(
                        proof,
                        snapshot.automation,
                        capability,
                    )
                )
            store.finalize_transition(
                transition_id,
                status="completed",
                outputs=[copy.deepcopy(item) for item in proof.outputs],
                canonical_sync_status="synchronized",
                canonical_sync_evidence=copy.deepcopy(
                    proof.canonical_evidence
                ),
                canonical_sync_observed_identities=copy.deepcopy(
                    proof.observed_identities
                ),
                activated_capabilities=activated_capabilities,
                expected_document_identity=snapshot.document_identity,
            )
            return CoordinationResult(
                "completed",
                transition_id,
                capability_id,
                tuple(copy.deepcopy(item) for item in proof.outputs),
                proof,
            )
        if decision.action == "fail-closed":
            raise AutomationContractError(
                "prepared transition recovery failed closed: "
                + decision.reason
            )
        if decision.action != "retry" or not decision.invoke_stage:
            try:
                store.pause_run(
                    reason=decision.reason,
                    expected_document_identity=snapshot.document_identity,
                )
            except StateContractError as error:
                raise AutomationContractError(str(error)) from error
            raise AutomationContractError(
                "prepared transition recovery paused: " + decision.reason
            )
        receipt = copy.deepcopy(prepared_receipt)

    if not recovering_prepared:
        replacement = copy.deepcopy(snapshot.automation)
        replacement["effective_capabilities"][capability_id] = capability
        replacement["transition_receipts"][transition_id] = copy.deepcopy(receipt)
        preflight_errors = validate_workflow_automation(
            replacement,
            top_level_change_id=capability["change_id"],
            lifecycle_contract=lifecycle_contract,
        )
        if preflight_errors:
            raise AutomationContractError(
                "one-stage coordination preflight failed: "
                + "; ".join(preflight_errors)
            )

        capability_only = copy.deepcopy(snapshot.automation)
        capability_only["effective_capabilities"][capability_id] = capability
        store.replace_automation(
            capability_only, expected_document_identity=snapshot.document_identity
        )
        prepared_snapshot = store.read()
        store.prepare_transition(
            receipt, expected_document_identity=prepared_snapshot.document_identity
        )
    try:
        stage_result = invoke_stage()
    except Exception:
        failed_snapshot = store.read()
        store.finalize_transition(
            transition_id,
            status="failed",
            outputs=[],
            canonical_sync_status="failed",
            expected_document_identity=failed_snapshot.document_identity,
        )
        raise
    try:
        stage_result = _validate_stage_result(
            stage_result,
            policy=policy,
            repository_root=repository_root,
            affected_path_roots=bounded_path_roots,
        )
        sync_result = _validate_sync_result(
            synchronize_canonical_state(stage_result),
            stage_result=stage_result,
            policy=policy,
            repository_root=repository_root,
            affected_path_roots=bounded_path_roots,
        )
    except Exception:
        paused_snapshot = store.read()
        outputs = (
            [_serialize_evidence(output) for output in stage_result.outputs]
            if isinstance(stage_result, StageExecutionResult)
            and all(isinstance(output, ArtifactEvidence) for output in stage_result.outputs)
            else []
        )
        store.finalize_transition(
            transition_id,
            status="paused",
            outputs=outputs,
            canonical_sync_status="failed",
            expected_document_identity=paused_snapshot.document_identity,
        )
        raise
    completed_snapshot = store.read()
    serialized_outputs = [_serialize_evidence(output) for output in stage_result.outputs]
    serialized_sync_evidence = {
        name: _serialize_evidence(evidence)
        for name, evidence in sync_result.evidence.items()
    }
    if canonical is None:
        raise AutomationContractError(
            "retry requires current canonical workflow evidence"
        )
    observed_identities = dict(canonical.observed_identities)
    observed_identities.update(
        {name: evidence.identity for name, evidence in sync_result.evidence.items()}
    )
    activated_capabilities: tuple[dict[str, Any], ...] = ()
    try:
        provisional_verification = verify_transition_completion(
            completed_snapshot.automation,
            receipt,
            completion_evidence={
                "input_identities": copy.deepcopy(receipt["input_identities"]),
                "expected_postcondition": copy.deepcopy(
                    receipt["expected_postcondition"]
                ),
                "outputs": copy.deepcopy(serialized_outputs),
                "canonical_sync": {
                    "status": "synchronized",
                    "evidence": copy.deepcopy(serialized_sync_evidence),
                    "observed_identities": copy.deepcopy(observed_identities),
                },
            },
            repository_root=repository_root,
        )
        if (
            not provisional_verification.valid
            or provisional_verification.proof is None
        ):
            raise AutomationContractError(
                "stage-native completion verification failed: "
                + provisional_verification.reason
            )
        if post_completion_capabilities is not None:
            activated_capabilities = tuple(
                copy.deepcopy(dict(item))
                for item in post_completion_capabilities(
                    provisional_verification.proof,
                    completed_snapshot.automation,
                    capability,
                )
            )
        store.finalize_transition(
            transition_id,
            status="completed",
            outputs=serialized_outputs,
            canonical_sync_status="synchronized",
            canonical_sync_evidence=serialized_sync_evidence,
            canonical_sync_observed_identities=observed_identities,
            activated_capabilities=activated_capabilities,
            expected_document_identity=completed_snapshot.document_identity,
        )
    except Exception as error:
        paused_snapshot = store.read()
        store.finalize_transition(
            transition_id,
            status="paused",
            outputs=serialized_outputs,
            canonical_sync_status="failed",
            invalidate_bound_capability=post_completion_capabilities is not None,
            expected_document_identity=paused_snapshot.document_identity,
        )
        if isinstance(error, AutomationContractError):
            raise
        raise AutomationContractError(
            "stage-native completion verification failed: " + str(error)
        ) from error
    finalized_snapshot = store.read()
    assert finalized_snapshot.automation is not None
    finalized_receipt = finalized_snapshot.automation["transition_receipts"][
        transition_id
    ]
    verification = verify_transition_completion(
        finalized_snapshot.automation,
        finalized_receipt,
        completion_evidence={
            "input_identities": copy.deepcopy(
                finalized_receipt.get("input_identities")
            ),
            "expected_postcondition": copy.deepcopy(
                finalized_receipt.get("expected_postcondition")
            ),
            "outputs": copy.deepcopy(finalized_receipt.get("outputs")),
            "canonical_sync": copy.deepcopy(
                finalized_receipt.get("canonical_sync")
            ),
        },
        repository_root=repository_root,
    )
    if not verification.valid or verification.proof is None:
        raise AutomationContractError(
            "finalized stage proof could not be routed: " + verification.reason
        )
    return CoordinationResult(
        "completed",
        transition_id,
        capability_id,
        tuple(serialized_outputs),
        verification.proof,
    )


__all__ = [
    "ActivePlanContext",
    "ArtifactEvidence",
    "AuthoringCoordinationResult",
    "AutomationContractError",
    "CanonicalPosition",
    "CanonicalSyncResult",
    "CoordinationResult",
    "MilestoneRecord",
    "NormalizedCommand",
    "PrePlanEvidence",
    "StageExecutionResult",
    "authorize_public_run",
    "bind_target",
    "coordinate_one_stage",
    "coordinate_non_public_authoring_stage",
    "coordinate_non_public_implementation_correction",
    "coordinate_non_public_implementation_stage",
    "coordinate_public_authoring_stage",
    "coordinate_public_implementation_correction",
    "coordinate_public_implementation_stage",
    "create_parent_authorization",
    "derive_effective_capability",
    "evaluate_implementation_correction",
    "evaluate_non_public_implementation_route",
    "evaluate_public_authoring_route",
    "evaluate_public_implementation_route",
    "execute_public_control_command",
    "invalidate_effective_capabilities",
    "normalize_command",
    "persist_target",
    "ProposalCorrectionAuthority",
    "ImplementationCorrectionDecision",
    "ImplementationCoordinationResult",
    "ImplementationRouteDecision",
    "VerificationReadiness",
    "record_plan_ownership_handoff",
    "resolve_canonical_position",
    "resolve_proposal_correction_authority",
    "resolve_verification_readiness",
    "resolve_command_target",
    "resume_public_run",
    "resume_target",
    "start_public_run",
]
