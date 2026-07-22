#!/usr/bin/env python3
"""Non-public target-bound workflow automation coordinator.

This module contains the M3 executable boundary.  It normalizes commands,
binds structured targets, resolves canonical workflow position, evaluates
bounded authority, and coordinates one stage operation through the sole state
writer.  Public command routing remains disabled until the approved cutover
milestone.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Mapping

from lifecycle_state_sync import HandoffSummary, parse_handoff_summary
from validate_workflow_automation import (
    CAPABILITY_AUTHORIZATION_CLASSES,
    CAPABILITY_BASIS_FIELDS,
    CAPABILITY_BASIS_LIST_FIELDS,
    CAPABILITY_STAGES,
    validate_workflow_automation,
)
from workflow_automation_policy import (
    CAPABILITY_MUTATION_CATEGORIES,
    PUBLIC_TARGET_STAGES,
    STAGE_POLICY_BY_STAGE,
    AuthorizationClass,
    CapabilityKind,
    OccurrenceKind,
    WorkflowPosition,
    WorkflowStage,
    can_operation_fit_target,
    target_completion_predicate,
)
from workflow_automation_state import (
    WorkflowAutomationStateStore,
    compute_transition_key,
)


CURRENT_COMMAND_RE = re.compile(r"^workflow\s+auto:\s*(?P<value>[a-z][a-z-]*)$")
LEGACY_COMMAND_RE = re.compile(r"^workflow\s+auto-through:\s*(?P<value>[a-z][a-z-]*)$")
MILESTONE_HEADER_RE = re.compile(r"^###\s+(?P<id>M[0-9]+)\.\s+(?P<title>.+?)\s*$")
MILESTONE_STATE_RE = re.compile(r"^-\s+Milestone state:\s*(?P<state>[a-z-]+)\s*$")
RFC3339_UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

LEGACY_TARGETS = frozenset({"plan-review", "verify"})
TERMINAL_MILESTONE_STATES = frozenset({"closed"})
KNOWN_MILESTONE_STATES = frozenset(
    {"planned", "implementing", "review-requested", "resolution-needed", "closed"}
)
PRE_PLAN_SEQUENCE = (
    "proposal",
    "proposal-review",
    "spec",
    "spec-review",
    "architecture-assessment",
    "architecture",
    "architecture-review",
    "plan",
)
REVIEW_POSITIONS = frozenset({"proposal-review", "spec-review", "architecture-review"})
REVIEW_OUTCOMES = frozenset({"approved", "changes-requested", "blocked", "inconclusive"})
TRANSITION_EVIDENCE_POSITIONS = frozenset(PRE_PLAN_SEQUENCE[1:])
CANONICAL_BASIS_FIELDS = {
    "proposal": ("proposal_identity", "reviewed_proposal_identity"),
    "proposal-review": ("approved_proposal_review_identity", "review_record_identity"),
    "plan": ("plan_identity",),
    "plan-review": ("plan_review_identity",),
    "test-spec": ("test_spec_identity",),
    "test-spec-review": ("test_spec_review_identity",),
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


@dataclass(frozen=True)
class StageExecutionResult:
    outputs: tuple[Any, ...]
    completion_evidence: Mapping[str, Any]


@dataclass(frozen=True)
class CanonicalSyncResult:
    status: str
    evidence: Mapping[str, Any]
    observed_identities: Mapping[str, str]


def normalize_command(command: str) -> NormalizedCommand:
    """Normalize current and supported legacy forms without persisting state."""

    if not isinstance(command, str):
        raise AutomationContractError("workflow command must be text")
    normalized = command.strip()
    if normalized.startswith("$"):
        normalized = normalized[1:].strip()
    current = CURRENT_COMMAND_RE.fullmatch(normalized)
    legacy = LEGACY_COMMAND_RE.fullmatch(normalized)
    if current is None and legacy is None:
        raise AutomationContractError("unknown workflow automation command")
    value = (current or legacy).group("value")  # type: ignore[union-attr]
    is_legacy = legacy is not None
    if value in {"status", "off"}:
        return NormalizedCommand(value, legacy=is_legacy)
    public_values = {stage.value for stage in PUBLIC_TARGET_STAGES}
    if value not in public_values or (is_legacy and value not in LEGACY_TARGETS):
        raise AutomationContractError(f"unknown workflow automation target: {value}")
    return NormalizedCommand("target", value, is_legacy)


def _target_stage(stage: str) -> WorkflowStage:
    try:
        parsed = WorkflowStage(stage)
    except (TypeError, ValueError) as exc:
        raise AutomationContractError(f"unknown workflow automation target: {stage}") from exc
    if parsed not in PUBLIC_TARGET_STAGES:
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
) -> dict[str, Any]:
    """Bind one complete structured target before run or authority persistence."""

    parsed = _target_stage(stage)
    if not RFC3339_UTC_RE.fullmatch(bound_at):
        raise AutomationContractError("target binding time must be RFC3339 UTC")
    policy = STAGE_POLICY_BY_STAGE[parsed.value]
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
        "completion": target_completion_predicate(parsed),
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
) -> dict[str, Any]:
    """Normalize a target command and bind its complete occurrence envelope."""

    normalized = normalize_command(command)
    if normalized.action != "target" or normalized.target_stage is None:
        raise AutomationContractError("workflow command does not select a target")
    return bind_target(normalized.target_stage, bound_at=bound_at, plan=plan)


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
    if evidence.architecture_applicability not in {"required", "not-required"}:
        raise AutomationContractError("architecture applicability is ambiguous")
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

    if "spec" in observed and evidence.review_outcomes.get("proposal-review") != "approved":
        raise AutomationContractError("contradictory proposal-review evidence")
    if any(
        position in observed
        for position in ("architecture-assessment", "architecture", "architecture-review", "plan")
    ) and evidence.review_outcomes.get("spec-review") != "approved":
        raise AutomationContractError("contradictory spec-review evidence")
    if "plan" in observed and evidence.architecture_applicability == "required":
        if evidence.review_outcomes.get("architecture-review") != "approved":
            raise AutomationContractError("contradictory architecture-review evidence")
    if "spec" in observed and not evidence.review_resolution_closed:
        raise AutomationContractError("required review resolution is not closed")

    applicable_sequence = list(PRE_PLAN_SEQUENCE)
    if evidence.architecture_applicability == "not-required":
        applicable_sequence.remove("architecture")
        applicable_sequence.remove("architecture-review")
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
        raise AutomationContractError("active plan current milestone is ambiguous")
    current = candidates[0]
    state = current.state
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
            else WorkflowPosition.TEST_SPEC_REVIEW.value
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
        category.value
        for category in CAPABILITY_MUTATION_CATEGORIES[policy.capability_kind]
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
        if basis_budget_identity is not None and basis_budget_identity != correction_budget_identity:
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


def _validate_stage_result(
    result: Any,
    expected_postcondition: Mapping[str, Any],
) -> StageExecutionResult:
    if not isinstance(result, StageExecutionResult):
        raise AutomationContractError("stage invocation requires a typed execution result")
    if not result.outputs:
        raise AutomationContractError("stage invocation requires concrete outputs")
    if dict(result.completion_evidence) != dict(expected_postcondition):
        raise AutomationContractError("stage completion evidence does not satisfy postcondition")
    return result


def _validate_sync_result(
    result: Any,
    canonical: CanonicalPosition,
) -> CanonicalSyncResult:
    if not isinstance(result, CanonicalSyncResult):
        raise AutomationContractError("canonical synchronization requires a typed result")
    if result.status != "synchronized" or not result.evidence:
        raise AutomationContractError("canonical synchronization did not complete")
    for name, identity in canonical.observed_identities.items():
        if result.observed_identities.get(name) != identity:
            raise AutomationContractError(f"canonical synchronization identity mismatch: {name}")
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
    derived_at: str | None = None,
    transition_id: str | None = None,
    input_identities: Mapping[str, Any] | None = None,
    expected_postcondition: Mapping[str, Any] | None = None,
    invoke_stage: Callable[[], StageExecutionResult] | None = None,
    synchronize_canonical_state: Callable[[StageExecutionResult], CanonicalSyncResult] | None = None,
    pre_plan: PrePlanEvidence | None = None,
    active_plan: ActivePlanContext | None = None,
    previously_observed: Mapping[str, str] | None = None,
    parent_authorization: Mapping[str, Any] | None = None,
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
        "derived_at": derived_at,
        "transition_id": transition_id,
        "input_identities": input_identities,
        "expected_postcondition": expected_postcondition,
        "invoke_stage": invoke_stage,
        "synchronize_canonical_state": synchronize_canonical_state,
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
    assert derived_at is not None
    assert transition_id is not None
    assert input_identities is not None
    assert expected_postcondition is not None
    assert invoke_stage is not None
    assert synchronize_canonical_state is not None

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
    parents = snapshot.automation.get("parent_authorizations")
    parent = parents.get(parent_authorization_id) if isinstance(parents, dict) else None
    if not isinstance(parent, dict):
        raise AutomationContractError("active parent authorization not found")
    capabilities = snapshot.automation.get("effective_capabilities")
    existing = tuple(capabilities.values()) if isinstance(capabilities, dict) else ()
    capability = derive_effective_capability(
        capability_id=capability_id,
        parent=parent,
        stage=stage,
        occurrence=occurrence,
        basis=basis,
        affected_path_roots=affected_path_roots,
        mutation_categories=mutation_categories,
        correction_budget=correction_budget,
        correction_budget_identity=correction_budget_identity,
        derived_at=derived_at,
        existing_capabilities=existing,
    )
    policy = STAGE_POLICY_BY_STAGE[stage]
    receipt = {
        "transition_id": transition_id,
        "transition_key": "pending",
        "policy_version": capability["policy_version"],
        "run_id": snapshot.automation["run"]["run_id"],
        "change_id": capability["change_id"],
        "from_position": canonical.position,
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

    replacement = copy.deepcopy(snapshot.automation)
    replacement["effective_capabilities"][capability_id] = capability
    replacement["transition_receipts"][transition_id] = copy.deepcopy(receipt)
    preflight_errors = validate_workflow_automation(
        replacement, top_level_change_id=capability["change_id"]
    )
    if preflight_errors:
        raise AutomationContractError(
            "one-stage coordination preflight failed: " + "; ".join(preflight_errors)
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
        stage_result = _validate_stage_result(stage_result, expected_postcondition)
        sync_result = _validate_sync_result(
            synchronize_canonical_state(stage_result), canonical
        )
    except Exception:
        paused_snapshot = store.read()
        outputs = list(stage_result.outputs) if isinstance(stage_result, StageExecutionResult) else []
        store.finalize_transition(
            transition_id,
            status="paused",
            outputs=outputs,
            canonical_sync_status="failed",
            expected_document_identity=paused_snapshot.document_identity,
        )
        raise
    completed_snapshot = store.read()
    store.finalize_transition(
        transition_id,
        status="completed",
        outputs=list(stage_result.outputs),
        canonical_sync_status="synchronized",
        canonical_sync_evidence=dict(sync_result.evidence),
        canonical_sync_observed_identities=dict(sync_result.observed_identities),
        expected_document_identity=completed_snapshot.document_identity,
    )
    return CoordinationResult(
        "completed", transition_id, capability_id, tuple(stage_result.outputs)
    )


__all__ = [
    "ActivePlanContext",
    "AutomationContractError",
    "CanonicalPosition",
    "CanonicalSyncResult",
    "CoordinationResult",
    "MilestoneRecord",
    "NormalizedCommand",
    "PrePlanEvidence",
    "StageExecutionResult",
    "bind_target",
    "coordinate_one_stage",
    "create_parent_authorization",
    "derive_effective_capability",
    "invalidate_effective_capabilities",
    "normalize_command",
    "persist_target",
    "record_plan_ownership_handoff",
    "resolve_canonical_position",
    "resolve_command_target",
    "resume_target",
]
