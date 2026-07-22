#!/usr/bin/env python3
"""Fail-closed validation for ``workflow.automation`` durable state.

M1 validates state only.  It intentionally exposes no mutation or routing API;
the sole-writer transaction boundary is introduced by the next milestone.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from enum import Enum
from typing import Any, Iterable

from workflow_automation_policy import (
    CAPABILITY_MUTATION_CATEGORIES,
    AuthorizationClass,
    CapabilityKind,
    MutationCategory,
    OccurrenceKind,
    PUBLIC_TARGET_STAGES,
    RetryPolicy,
    STAGE_POLICY_BY_STAGE,
    TransitionContext,
    WorkflowPosition,
    WorkflowStage,
    can_operation_fit_target,
    evaluate_transition,
    is_immediate_predecessor,
    target_completion_predicate,
)


MECHANISMS = frozenset({"bounded-review-fix"})
SCHEMA_VERSIONS = frozenset({1})
POLICY_VERSIONS = frozenset({1})
RUN_STATUSES = frozenset({"active", "paused", "completed", "cancelled"})
PARENT_AUTHORIZATION_STATUSES = frozenset({"active", "revoked", "invalidated"})
EFFECTIVE_CAPABILITY_STATUSES = frozenset({"active", "consumed", "invalidated"})
RECEIPT_STATUSES = frozenset({"prepared", "completed", "failed", "paused", "cancelled"})
REVIEW_OUTCOMES = frozenset({"approved", "changes-requested", "blocked", "inconclusive"})
CLEAN_GATE_STATES = frozenset({"satisfied", "not-satisfied"})
ROUTING_ACTIONS = frozenset({"continue", "correction-loop", "stop-at-target", "pause", "fail-closed"})
CANONICAL_SYNC_STATUSES = frozenset({"pending", "synchronized", "failed"})
EXTERNAL_ACTION_VALUES = frozenset({"prohibited"})
LEGACY_SOURCE_MECHANISMS = frozenset(
    {
        "authoring-through-plan-review",
        "bounded-review-fix",
        "implementation-through-verify",
    }
)
MIGRATION_PROJECTION_RESULTS = frozenset({"equivalent"})
INVALIDATION_ACTIONS = frozenset({"pause", "invalidate"})
PARENT_INVALIDATION_TRIGGERS = frozenset(
    {
        "on_change_identity_mismatch",
        "on_policy_change",
        "on_scope_expansion",
        "on_scope_narrowing",
        "on_supersession",
    }
)
CAPABILITY_INVALIDATION_TRIGGERS = frozenset(
    {
        "on_parent_revocation",
        "on_basis_change",
        "on_proposal_identity_change",
        "on_review_staleness",
        "on_scope_expansion",
        "on_policy_change",
        "on_occurrence_change",
        "on_validation_command_change",
    }
)
RUN_STATUS_TRANSITIONS = {
    "active": frozenset({"paused", "completed", "cancelled"}),
    "paused": frozenset({"active", "cancelled"}),
    "completed": frozenset(),
    "cancelled": frozenset(),
}
PARENT_STATUS_TRANSITIONS = {
    "active": frozenset({"revoked", "invalidated"}),
    "revoked": frozenset(),
    "invalidated": frozenset(),
}
CAPABILITY_STATUS_TRANSITIONS = {
    "active": frozenset({"consumed", "invalidated"}),
    "consumed": frozenset(),
    "invalidated": frozenset(),
}
STATUS_TRANSITION_TABLES = {
    "run": RUN_STATUS_TRANSITIONS,
    "parent-authorization": PARENT_STATUS_TRANSITIONS,
    "effective-capability": CAPABILITY_STATUS_TRANSITIONS,
}
FORBIDDEN_LIVE_STATE_FIELDS = frozenset(
    {"current_stage", "next_stage", "review_status", "branch_readiness", "pr_readiness"}
)
RFC3339_UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

PUBLIC_STAGE_VALUES = frozenset(stage.value for stage in PUBLIC_TARGET_STAGES)
OCCURRENCE_VALUES = frozenset(kind.value for kind in OccurrenceKind)
AUTHORIZATION_CLASS_VALUES = frozenset(value.value for value in AuthorizationClass)
CAPABILITY_KIND_VALUES = frozenset(value.value for value in CapabilityKind)
MUTATION_CATEGORY_VALUES = frozenset(value.value for value in MutationCategory)
RETRY_POLICY_VALUES = frozenset(value.value for value in RetryPolicy)
TRANSITION_KEY_FIELDS = frozenset(
    {
        "policy_version",
        "run_id",
        "change_id",
        "from_position",
        "target",
        "effective_capability_id",
        "retry_policy",
        "input_identities",
        "expected_postcondition",
    }
)


def compute_transition_key(receipt: dict[str, Any]) -> str:
    """Compute the deterministic identity of immutable transition inputs."""

    projection = {field: receipt.get(field) for field in sorted(TRANSITION_KEY_FIELDS)}
    payload = json.dumps(
        projection, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"

CAPABILITY_AUTHORIZATION_CLASSES = {
    CapabilityKind.PROPOSAL_REVIEW.value: AuthorizationClass.AUTHORING.value,
    CapabilityKind.PROPOSAL_CORRECTION.value: AuthorizationClass.AUTHORING.value,
    CapabilityKind.POST_PROPOSAL_AUTHORING.value: AuthorizationClass.AUTHORING.value,
    CapabilityKind.IMPLEMENTATION.value: AuthorizationClass.IMPLEMENTATION.value,
    CapabilityKind.IMPLEMENTATION_CORRECTION.value: AuthorizationClass.IMPLEMENTATION.value,
    CapabilityKind.VERIFICATION.value: AuthorizationClass.VERIFICATION.value,
}

CAPABILITY_STAGES = {
    CapabilityKind.PROPOSAL_REVIEW.value: frozenset({WorkflowStage.PROPOSAL_REVIEW.value}),
    CapabilityKind.PROPOSAL_CORRECTION.value: frozenset({WorkflowStage.PROPOSAL.value}),
    CapabilityKind.POST_PROPOSAL_AUTHORING.value: frozenset(
        {
            WorkflowStage.SPEC.value,
            WorkflowStage.SPEC_REVIEW.value,
            WorkflowStage.ARCHITECTURE_ASSESSMENT.value,
            WorkflowStage.ARCHITECTURE.value,
            WorkflowStage.ARCHITECTURE_REVIEW.value,
            WorkflowStage.PLAN.value,
            WorkflowStage.PLAN_REVIEW.value,
            WorkflowStage.TEST_SPEC.value,
            WorkflowStage.TEST_SPEC_REVIEW.value,
        }
    ),
    CapabilityKind.IMPLEMENTATION.value: frozenset(
        {
            WorkflowStage.IMPLEMENT.value,
            WorkflowStage.CODE_REVIEW.value,
            WorkflowStage.CI_MAINTENANCE.value,
            WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW.value,
        }
    ),
    CapabilityKind.IMPLEMENTATION_CORRECTION.value: frozenset({WorkflowStage.REVIEW_RESOLUTION.value}),
    CapabilityKind.VERIFICATION.value: frozenset(
        {WorkflowStage.EXPLAIN_CHANGE.value, WorkflowStage.VERIFY.value}
    ),
}

CAPABILITY_BASIS_FIELDS = {
    CapabilityKind.PROPOSAL_REVIEW.value: frozenset(
        {
            "proposal_identity",
            "standing_gates_identity",
            "review_policy_identity",
            "structured_target_identity",
            "review_evidence_roots",
        }
    ),
    CapabilityKind.PROPOSAL_CORRECTION.value: frozenset(
        {
            "reviewed_proposal_identity",
            "review_record_identity",
            "accepted_finding_set_identity",
            "classifier_policy_identity",
            "correction_budget_identity",
            "affected_proposal_roots",
        }
    ),
    CapabilityKind.POST_PROPOSAL_AUTHORING.value: frozenset(
        {
            "proposal_identity",
            "approved_proposal_review_identity",
            "closed_review_resolution_identity",
            "stage_scope_identity",
        }
    ),
    CapabilityKind.IMPLEMENTATION.value: frozenset(
        {
            "plan_identity",
            "plan_review_identity",
            "test_spec_identity",
            "test_spec_review_identity",
            "milestone_identity",
            "affected_paths_identity",
            "mutation_categories_identity",
            "validation_commands_identity",
        }
    ),
    CapabilityKind.IMPLEMENTATION_CORRECTION.value: frozenset(
        {
            "code_review_identity",
            "accepted_finding_set_identity",
            "reviewer_classification_identity",
            "affected_paths_identity",
        }
    ),
    CapabilityKind.VERIFICATION.value: frozenset(
        {
            "closed_milestones_identity",
            "final_code_review_identity",
            "promotion_evidence_identity",
            "explanation_inputs_identity",
            "branch_state_identity",
            "verification_commands_identity",
        }
    ),
}

CAPABILITY_BASIS_LIST_FIELDS = frozenset(
    {
        "review_evidence_roots",
        "affected_proposal_roots",
    }
)


def _enum_values(enum: type[Enum]) -> frozenset[str]:
    return frozenset(str(member.value) for member in enum)


def _expected_occurrence(stage: Any) -> str | None:
    policy = STAGE_POLICY_BY_STAGE.get(stage) if isinstance(stage, str) else None
    return policy.occurrence_rule.value if policy is not None else None


def _required(record: Any, fields: Iterable[str], path: str) -> list[str]:
    if not isinstance(record, dict):
        return [f"{path}: expected object"]
    return [f"{path}.{field}: missing required field" for field in sorted(fields) if field not in record]


def _unknown_value(path: str, value: Any, allowed: Iterable[Any]) -> str | None:
    allowed_set = frozenset(allowed)
    if any(value == item for item in allowed_set):
        return None
    expected = ", ".join(str(item) for item in sorted(allowed_set, key=str))
    return f"{path}: unknown value {value!r}; expected one of: {expected}"


def _validate_string_list(value: Any, path: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        return [f"{path}: expected array"]
    errors = [] if value or allow_empty else [f"{path}: expected non-empty array"]
    errors.extend(
        f"{path}[{index}]: expected non-empty string"
        for index, item in enumerate(value)
        if not isinstance(item, str) or not item.strip()
    )
    return errors


def _validate_non_empty_object(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict) or not value:
        return [f"{path}: expected non-empty object"]
    return []


def _validate_concrete_value(
    value: Any,
    path: str,
    *,
    ancestors: frozenset[int] = frozenset(),
    depth: int = 0,
) -> list[str]:
    if depth > 32:
        return [f"{path}: concrete evidence exceeds maximum nesting depth"]
    if isinstance(value, str):
        return [] if value.strip() else [f"{path}: expected concrete non-empty value"]
    if isinstance(value, bool) or value is None:
        return [f"{path}: expected concrete non-empty value"]
    if isinstance(value, int):
        return []
    if isinstance(value, float):
        return [] if math.isfinite(value) else [f"{path}: expected finite numeric value"]
    if isinstance(value, dict):
        if not value:
            return [f"{path}: expected concrete non-empty object"]
        if id(value) in ancestors:
            return [f"{path}: cyclic concrete evidence is not allowed"]
        child_ancestors = ancestors | {id(value)}
        errors: list[str] = []
        for key, item in value.items():
            if not isinstance(key, str) or not key.strip():
                errors.append(f"{path}: expected non-empty string keys")
                continue
            errors.extend(
                _validate_concrete_value(
                    item,
                    f"{path}.{key}",
                    ancestors=child_ancestors,
                    depth=depth + 1,
                )
            )
        return errors
    if isinstance(value, list):
        if not value:
            return [f"{path}: expected concrete non-empty array"]
        if id(value) in ancestors:
            return [f"{path}: cyclic concrete evidence is not allowed"]
        child_ancestors = ancestors | {id(value)}
        errors = []
        for index, item in enumerate(value):
            errors.extend(
                _validate_concrete_value(
                    item,
                    f"{path}[{index}]",
                    ancestors=child_ancestors,
                    depth=depth + 1,
                )
            )
        return errors
    return [f"{path}: expected concrete non-empty value"]


def _validate_concrete_object(value: Any, path: str) -> list[str]:
    errors = _validate_non_empty_object(value, path)
    if not isinstance(value, dict):
        return errors
    for key, item in value.items():
        if not isinstance(key, str) or not key.strip():
            errors.append(f"{path}: expected non-empty string keys")
            continue
        errors.extend(_validate_concrete_value(item, f"{path}.{key}"))
    return errors


def _validate_invalidation(
    value: Any,
    path: str,
    allowed_triggers: frozenset[str],
    *,
    require_non_empty: bool = True,
) -> list[str]:
    errors = _validate_non_empty_object(value, path) if require_non_empty else []
    if not isinstance(value, dict):
        return errors
    for trigger, action in value.items():
        trigger_error = _unknown_value(f"{path}.{trigger}", trigger, allowed_triggers)
        if trigger_error:
            errors.append(trigger_error)
            continue
        action_error = _unknown_value(f"{path}.{trigger}", action, INVALIDATION_ACTIONS)
        if action_error:
            errors.append(action_error)
    return errors


def _validate_identity_value(value: Any, path: str, *, list_value: bool = False) -> list[str]:
    if list_value:
        return _validate_string_list(value, path)
    if not isinstance(value, str) or not value.strip():
        return [f"{path}: expected non-empty identity string"]
    return []


def _validate_evidence_object(value: Any, path: str) -> list[str]:
    errors = _validate_non_empty_object(value, path)
    if not isinstance(value, dict):
        return errors
    for key, item in value.items():
        if not isinstance(key, str) or not key.strip():
            errors.append(f"{path}: expected non-empty string keys")
        if isinstance(item, list):
            errors.extend(_validate_string_list(item, f"{path}.{key}"))
        elif not isinstance(item, str) or not item.strip():
            errors.append(f"{path}.{key}: expected non-empty identity string")
    return errors


def _is_sequence_subset(candidate: Any, maximum: Any) -> bool:
    if not isinstance(candidate, list) or not isinstance(maximum, list):
        return False
    return all(any(item == allowed for allowed in maximum) for item in candidate)


def _validate_operation_within_target(
    capability: dict[str, Any],
    target: Any,
    path: str,
    target_label: str,
    from_position: Any = None,
    transition_evidence: Any = None,
) -> list[str]:
    stage = capability.get("stage")
    if not isinstance(stage, dict) or not isinstance(target, dict):
        return []
    operation = stage.get("name")
    destination = target.get("stage")
    try:
        operation_stage = WorkflowStage(operation)
        destination_stage = WorkflowStage(destination)
    except (TypeError, ValueError):
        return []
    errors: list[str] = []
    if from_position is None:
        permitted = can_operation_fit_target(operation_stage, destination_stage)
    else:
        try:
            canonical_from_position = WorkflowPosition(from_position)
        except (TypeError, ValueError):
            return errors
        operation_occurrence = stage.get("occurrence")
        target_occurrence = target.get("occurrence")
        basis = capability.get("basis")
        context = TransitionContext(
            from_position=canonical_from_position,
            operation=operation_stage,
            target=destination_stage,
            operation_milestone_id=(
                operation_occurrence.get("milestone_id")
                if isinstance(operation_occurrence, dict)
                else None
            ),
            operation_milestone_identity=(
                basis.get("milestone_identity")
                if isinstance(basis, dict)
                else None
            ),
            target_milestone_id=(
                target_occurrence.get("milestone_id")
                if isinstance(target_occurrence, dict)
                else None
            ),
            plan_identity=(
                basis.get("plan_identity")
                if isinstance(basis, dict)
                else None
            ),
            evidence=(
                transition_evidence
                if isinstance(transition_evidence, dict)
                else {}
            ),
        )
        evaluation = evaluate_transition(context)
        permitted = evaluation.allowed
        if not permitted:
            errors.extend(
                f"{path}.{error}; operation exceeds {target_label}"
                for error in evaluation.errors
            )
    if not permitted and not errors:
        errors.append(f"{path}.stage.name: operation exceeds {target_label}")
        return errors
    if not permitted:
        return errors
    if operation in {WorkflowStage.IMPLEMENT.value, WorkflowStage.CODE_REVIEW.value} and destination in {
        WorkflowStage.IMPLEMENT.value,
        WorkflowStage.CODE_REVIEW.value,
    }:
        operation_occurrence = stage.get("occurrence")
        target_occurrence = target.get("occurrence")
        if isinstance(operation_occurrence, dict) and isinstance(target_occurrence, dict):
            if operation_occurrence.get("milestone_id") != target_occurrence.get("milestone_id"):
                errors.append(f"{path}.stage.occurrence.milestone_id: exceeds {target_label}")
        basis = capability.get("basis")
        if isinstance(basis, dict) and basis.get("plan_identity") != target.get("plan_identity"):
            errors.append(f"{path}.basis.plan_identity: does not match {target_label}")
    return errors


def _validate_target_vocabulary(target: Any, path: str) -> list[str]:
    if not isinstance(target, dict):
        return []
    errors: list[str] = []
    if "stage" in target:
        error = _unknown_value(f"{path}.stage", target["stage"], PUBLIC_STAGE_VALUES)
        if error:
            errors.append(error)
    occurrence = target.get("occurrence")
    if isinstance(occurrence, dict) and "kind" in occurrence:
        error = _unknown_value(f"{path}.occurrence.kind", occurrence["kind"], OCCURRENCE_VALUES)
        if error:
            errors.append(error)
    return errors


def _validate_vocabulary(automation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    vocabulary_fields = (
        ("workflow.automation.mechanism", automation.get("mechanism"), MECHANISMS),
        ("workflow.automation.schema_version", automation.get("schema_version"), SCHEMA_VERSIONS),
        ("workflow.automation.external_actions", automation.get("external_actions"), EXTERNAL_ACTION_VALUES),
    )
    for path, value, allowed in vocabulary_fields:
        if value is not None:
            error = _unknown_value(path, value, allowed)
            if error:
                errors.append(error)

    run = automation.get("run")
    if isinstance(run, dict):
        if "status" in run:
            error = _unknown_value("workflow.automation.run.status", run["status"], RUN_STATUSES)
            if error:
                errors.append(error)
        errors.extend(_validate_target_vocabulary(run.get("target"), "workflow.automation.run.target"))
        if "policy_version" in run:
            error = _unknown_value(
                "workflow.automation.run.policy_version", run["policy_version"], POLICY_VERSIONS
            )
            if error:
                errors.append(error)

    parents = automation.get("parent_authorizations")
    if isinstance(parents, dict):
        for parent_id, parent in parents.items():
            if not isinstance(parent, dict):
                continue
            path = f"workflow.automation.parent_authorizations.{parent_id}"
            for field, allowed in (
                ("authorization_class", AUTHORIZATION_CLASS_VALUES),
                ("status", PARENT_AUTHORIZATION_STATUSES),
                ("external_actions", EXTERNAL_ACTION_VALUES),
                ("policy_version", POLICY_VERSIONS),
            ):
                if field in parent:
                    error = _unknown_value(f"{path}.{field}", parent[field], allowed)
                    if error:
                        errors.append(error)
            errors.extend(_validate_target_vocabulary(parent.get("maximum_target"), f"{path}.maximum_target"))
            kinds = parent.get("allowed_capability_kinds")
            if isinstance(kinds, list):
                for index, value in enumerate(kinds):
                    error = _unknown_value(f"{path}.allowed_capability_kinds[{index}]", value, CAPABILITY_KIND_VALUES)
                    if error:
                        errors.append(error)
            categories = parent.get("maximum_mutation_categories")
            if isinstance(categories, list):
                for index, value in enumerate(categories):
                    error = _unknown_value(f"{path}.maximum_mutation_categories[{index}]", value, MUTATION_CATEGORY_VALUES)
                    if error:
                        errors.append(error)
            invalidation = parent.get("invalidation")
            if isinstance(invalidation, dict):
                errors.extend(
                    _validate_invalidation(
                        invalidation,
                        f"{path}.invalidation",
                        PARENT_INVALIDATION_TRIGGERS,
                        require_non_empty=False,
                    )
                )

    capabilities = automation.get("effective_capabilities")
    if isinstance(capabilities, dict):
        for capability_id, capability in capabilities.items():
            if not isinstance(capability, dict):
                continue
            path = f"workflow.automation.effective_capabilities.{capability_id}"
            for field, allowed in (
                ("capability_kind", CAPABILITY_KIND_VALUES),
                ("status", EFFECTIVE_CAPABILITY_STATUSES),
                ("policy_version", POLICY_VERSIONS),
            ):
                if field in capability:
                    error = _unknown_value(f"{path}.{field}", capability[field], allowed)
                    if error:
                        errors.append(error)
            stage = capability.get("stage")
            if isinstance(stage, dict):
                if "name" in stage:
                    error = _unknown_value(
                        f"{path}.stage.name",
                        stage["name"],
                        _enum_values(WorkflowStage),
                    )
                    if error:
                        errors.append(error)
                occurrence = stage.get("occurrence")
                if isinstance(occurrence, dict) and "kind" in occurrence:
                    error = _unknown_value(
                        f"{path}.stage.occurrence.kind", occurrence["kind"], OCCURRENCE_VALUES
                    )
                    if error:
                        errors.append(error)
            scope = capability.get("scope")
            if isinstance(scope, dict) and isinstance(scope.get("mutation_categories"), list):
                for index, value in enumerate(scope["mutation_categories"]):
                    error = _unknown_value(f"{path}.scope.mutation_categories[{index}]", value, MUTATION_CATEGORY_VALUES)
                    if error:
                        errors.append(error)
            invalidation = capability.get("invalidation")
            if isinstance(invalidation, dict):
                errors.extend(
                    _validate_invalidation(
                        invalidation,
                        f"{path}.invalidation",
                        CAPABILITY_INVALIDATION_TRIGGERS,
                        require_non_empty=False,
                    )
                )

    receipts = automation.get("transition_receipts")
    if isinstance(receipts, dict):
        for receipt_id, receipt in receipts.items():
            if not isinstance(receipt, dict):
                continue
            path = f"workflow.automation.transition_receipts.{receipt_id}"
            if "status" in receipt:
                error = _unknown_value(f"{path}.status", receipt["status"], RECEIPT_STATUSES)
                if error:
                    errors.append(error)
            if "policy_version" in receipt:
                error = _unknown_value(
                    f"{path}.policy_version", receipt["policy_version"], POLICY_VERSIONS
                )
                if error:
                    errors.append(error)
            if "retry_policy" in receipt:
                error = _unknown_value(
                    f"{path}.retry_policy", receipt["retry_policy"], RETRY_POLICY_VALUES
                )
                if error:
                    errors.append(error)
            if "from_position" in receipt:
                error = _unknown_value(
                    f"{path}.from_position",
                    receipt["from_position"],
                    _enum_values(WorkflowPosition),
                )
                if error:
                    errors.append(error)
            errors.extend(_validate_target_vocabulary(receipt.get("target"), f"{path}.target"))
            canonical_sync = receipt.get("canonical_sync")
            if isinstance(canonical_sync, dict) and "status" in canonical_sync:
                error = _unknown_value(
                    f"{path}.canonical_sync.status",
                    canonical_sync["status"],
                    CANONICAL_SYNC_STATUSES,
                )
                if error:
                    errors.append(error)

    migrations = automation.get("migration_receipts")
    if isinstance(migrations, dict):
        for migration_id, migration in migrations.items():
            if not isinstance(migration, dict):
                continue
            path = f"workflow.automation.migration_receipts.{migration_id}"
            if "source_mechanism" in migration:
                error = _unknown_value(
                    f"{path}.source_mechanism",
                    migration["source_mechanism"],
                    LEGACY_SOURCE_MECHANISMS,
                )
                if error:
                    errors.append(error)
            if "projection_result" in migration:
                error = _unknown_value(
                    f"{path}.projection_result",
                    migration["projection_result"],
                    MIGRATION_PROJECTION_RESULTS,
                )
                if error:
                    errors.append(error)

    review_result = automation.get("latest_review_result")
    if isinstance(review_result, dict):
        for field, allowed in (
            ("outcome", REVIEW_OUTCOMES),
            ("clean_gate", CLEAN_GATE_STATES),
            ("routing_action", ROUTING_ACTIONS),
        ):
            if field in review_result:
                error = _unknown_value(f"workflow.automation.latest_review_result.{field}", review_result[field], allowed)
                if error:
                    errors.append(error)
    return errors


def _validate_target(target: Any, path: str) -> list[str]:
    errors = _required(target, {"stage", "occurrence", "bound_at", "completion"}, path)
    if not isinstance(target, dict):
        return errors
    occurrence = target.get("occurrence")
    errors.extend(_required(occurrence, {"kind"}, f"{path}.occurrence"))
    stage = target.get("stage")
    kind = occurrence.get("kind") if isinstance(occurrence, dict) else None
    expected = _expected_occurrence(stage)
    if expected is not None and kind != expected:
        errors.append(f"{path}.occurrence.kind: incompatible with {stage}; expected {expected}")
    if stage in {WorkflowStage.IMPLEMENT.value, WorkflowStage.CODE_REVIEW.value}:
        if isinstance(occurrence, dict) and not occurrence.get("milestone_id"):
            errors.append(f"{path}.occurrence.milestone_id: required for repeated-stage target")
        if not target.get("plan_identity"):
            errors.append(f"{path}.plan_identity: required for repeated-stage target")
    bound_at = target.get("bound_at")
    if not isinstance(bound_at, str) or RFC3339_UTC_RE.fullmatch(bound_at) is None:
        errors.append(f"{path}.bound_at: expected RFC3339 UTC timestamp")
    errors.extend(_validate_concrete_object(target.get("completion"), f"{path}.completion"))
    if isinstance(stage, str) and stage in {item.value for item in PUBLIC_TARGET_STAGES}:
        if target.get("completion") != target_completion_predicate(stage):
            errors.append(f"{path}.completion: must match immutable stage policy")
    return errors


def _validate_parent(parent_id: str, parent: Any, top_change_id: Any, path: str) -> list[str]:
    required = {
        "authorization_id",
        "authorization_class",
        "policy_version",
        "change_id",
        "authorized_by",
        "authorized_at",
        "maximum_target",
        "allowed_capability_kinds",
        "maximum_path_roots",
        "maximum_mutation_categories",
        "status",
        "revocation",
        "invalidation",
        "external_actions",
    }
    errors = _required(parent, required, path)
    if not isinstance(parent, dict):
        return errors
    if parent.get("authorization_id") != parent_id:
        errors.append(f"{path}.authorization_id: must match mapping key")
    if top_change_id is not None and parent.get("change_id") != top_change_id:
        errors.append(f"{path}.change_id: must match run change_id")
    errors.extend(_validate_string_list(parent.get("maximum_path_roots"), f"{path}.maximum_path_roots"))
    errors.extend(
        _validate_string_list(
            parent.get("maximum_mutation_categories"),
            f"{path}.maximum_mutation_categories",
        )
    )
    errors.extend(
        _validate_string_list(
            parent.get("allowed_capability_kinds"),
            f"{path}.allowed_capability_kinds",
        )
    )
    if not isinstance(parent.get("revocation"), dict):
        errors.append(f"{path}.revocation: expected object")
    errors.extend(
        _validate_invalidation(
            parent.get("invalidation"),
            f"{path}.invalidation",
            PARENT_INVALIDATION_TRIGGERS,
        )
    )
    revocation = parent.get("revocation")
    if isinstance(revocation, dict) and not isinstance(revocation.get("revoked"), bool):
        errors.append(f"{path}.revocation.revoked: expected boolean")
    if isinstance(revocation, dict) and isinstance(revocation.get("revoked"), bool):
        if parent.get("status") == "revoked" and not revocation["revoked"]:
            errors.append(f"{path}.revocation.revoked: must be true when parent status is revoked")
        if parent.get("status") == "active" and revocation["revoked"]:
            errors.append(f"{path}.revocation.revoked: active parent cannot be revoked")
    for field in ("authorization_id", "change_id", "authorized_by"):
        if not isinstance(parent.get(field), str) or not parent.get(field):
            errors.append(f"{path}.{field}: expected non-empty string")
    authorized_at = parent.get("authorized_at")
    if not isinstance(authorized_at, str) or RFC3339_UTC_RE.fullmatch(authorized_at) is None:
        errors.append(f"{path}.authorized_at: expected RFC3339 UTC timestamp")
    maximum_target = parent.get("maximum_target")
    if isinstance(maximum_target, dict):
        errors.extend(_validate_target(maximum_target, f"{path}.maximum_target"))
    else:
        errors.append(f"{path}.maximum_target: expected object")
    allowed_kinds = parent.get("allowed_capability_kinds")
    authorization_class = parent.get("authorization_class")
    if isinstance(allowed_kinds, list):
        for kind in allowed_kinds:
            expected_class = CAPABILITY_AUTHORIZATION_CLASSES.get(kind)
            if expected_class and expected_class != authorization_class:
                errors.append(
                    f"{path}.allowed_capability_kinds: {kind} crosses parent authorization class"
                )
    if isinstance(allowed_kinds, list) and any(
        kind in {
            CapabilityKind.PROPOSAL_CORRECTION.value,
            CapabilityKind.IMPLEMENTATION_CORRECTION.value,
        }
        for kind in allowed_kinds
    ):
        budget = parent.get("correction_budget")
        if not isinstance(budget, dict) or not budget:
            errors.append(f"{path}.correction_budget: required non-empty object for correction authority")
        elif any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for value in budget.values()
        ):
            errors.append(f"{path}.correction_budget: expected non-negative integer limits")
    return errors


def _validate_capability(
    capability_id: str,
    capability: Any,
    parents: dict[str, Any],
    top_change_id: Any,
    path: str,
) -> list[str]:
    required = {
        "capability_id",
        "capability_kind",
        "parent_authorization_id",
        "policy_version",
        "change_id",
        "stage",
        "basis",
        "scope",
        "derived_at",
        "status",
        "invalidation",
    }
    errors = _required(capability, required, path)
    if not isinstance(capability, dict):
        return errors
    if capability.get("capability_id") != capability_id:
        errors.append(f"{path}.capability_id: must match mapping key")
    if top_change_id is not None and capability.get("change_id") != top_change_id:
        errors.append(f"{path}.change_id: must match run change_id")
    derived_at = capability.get("derived_at")
    if not isinstance(derived_at, str) or RFC3339_UTC_RE.fullmatch(derived_at) is None:
        errors.append(f"{path}.derived_at: expected RFC3339 UTC timestamp")

    kind = capability.get("capability_kind")
    parent_id = capability.get("parent_authorization_id")
    parent = parents.get(parent_id) if isinstance(parent_id, str) else None
    if not isinstance(parent, dict):
        errors.append(f"{path}.parent_authorization_id: active parent authorization not found")
        parent = None
    elif capability.get("status") == "active" and parent.get("status") != "active":
        errors.append(f"{path}.parent_authorization_id: parent authorization is not active")
    elif (
        capability.get("status") == "active"
        and isinstance(parent.get("revocation"), dict)
        and parent["revocation"].get("revoked") is True
    ):
        errors.append(f"{path}.parent_authorization_id: parent authorization is revoked")

    stage = capability.get("stage")
    if not isinstance(stage, dict):
        errors.append(f"{path}.stage: expected object")
        stage_name = None
        occurrence = None
    else:
        stage_name = stage.get("name")
        occurrence = stage.get("occurrence")
        errors.extend(_required(stage, {"name", "occurrence"}, f"{path}.stage"))
        errors.extend(_required(occurrence, {"kind"}, f"{path}.stage.occurrence"))
    if kind in CAPABILITY_STAGES and stage_name not in CAPABILITY_STAGES[kind]:
        errors.append(f"{path}.stage.name: incompatible with capability kind {kind}")
    policy = STAGE_POLICY_BY_STAGE.get(stage_name) if isinstance(stage_name, str) else None
    if policy is not None and isinstance(occurrence, dict):
        expected = policy.occurrence_rule.value
        if occurrence.get("kind") != expected:
            errors.append(f"{path}.stage.occurrence.kind: expected {expected} for {stage_name}")
        if expected == OccurrenceKind.MILESTONE.value and not occurrence.get("milestone_id"):
            errors.append(f"{path}.stage.occurrence.milestone_id: required for milestone capability")
        if expected != OccurrenceKind.MILESTONE.value and "milestone_id" in occurrence:
            errors.append(f"{path}.stage.occurrence.milestone_id: forbidden for {expected} capability")

    basis = capability.get("basis")
    if not isinstance(basis, dict):
        errors.append(f"{path}.basis: expected object")
    elif kind in CAPABILITY_BASIS_FIELDS:
        for field in sorted(CAPABILITY_BASIS_FIELDS[kind]):
            if field not in basis:
                errors.append(f"{path}.basis.{field}: missing stage-appropriate basis identity")
            else:
                errors.extend(
                    _validate_identity_value(
                        basis[field],
                        f"{path}.basis.{field}",
                        list_value=field in CAPABILITY_BASIS_LIST_FIELDS,
                    )
                )

    scope = capability.get("scope")
    if not isinstance(scope, dict):
        errors.append(f"{path}.scope: expected object")
    else:
        errors.extend(_required(scope, {"affected_path_roots", "mutation_categories"}, f"{path}.scope"))
        errors.extend(
            _validate_string_list(scope.get("affected_path_roots"), f"{path}.scope.affected_path_roots")
        )
        errors.extend(
            _validate_string_list(scope.get("mutation_categories"), f"{path}.scope.mutation_categories")
        )
        if kind in {
            CapabilityKind.PROPOSAL_CORRECTION.value,
            CapabilityKind.IMPLEMENTATION_CORRECTION.value,
        }:
            budget = scope.get("correction_budget")
            budget_identity = scope.get("correction_budget_identity")
            if not isinstance(budget, dict) or not budget:
                errors.append(f"{path}.scope.correction_budget: required for correction capability")
            elif any(
                not isinstance(value, int)
                or isinstance(value, bool)
                or value <= 0
                for value in budget.values()
            ):
                errors.append(
                    f"{path}.scope.correction_budget: expected positive remaining limits"
                )
            if not isinstance(budget_identity, str) or not budget_identity.strip():
                errors.append(
                    f"{path}.scope.correction_budget_identity: required concrete identity"
                )
            if (
                isinstance(basis, dict)
                and "correction_budget_identity" in basis
                and basis.get("correction_budget_identity") != budget_identity
            ):
                errors.append(
                    f"{path}.scope.correction_budget_identity: must match capability basis"
                )

    errors.extend(
        _validate_invalidation(
            capability.get("invalidation"),
            f"{path}.invalidation",
            CAPABILITY_INVALIDATION_TRIGGERS,
        )
    )

    if parent is not None:
        if capability.get("policy_version") != parent.get("policy_version"):
            errors.append(f"{path}.policy_version: must match parent policy version")
        expected_class = CAPABILITY_AUTHORIZATION_CLASSES.get(kind)
        if expected_class and parent.get("authorization_class") != expected_class:
            errors.append(f"{path}.capability_kind: crosses parent authorization class")
        if kind not in parent.get("allowed_capability_kinds", []):
            errors.append(f"{path}.capability_kind: exceeds parent maximum")
        if isinstance(scope, dict):
            path_roots = scope.get("affected_path_roots")
            if isinstance(path_roots, list) and not _is_sequence_subset(
                path_roots, parent.get("maximum_path_roots")
            ):
                errors.append(f"{path}.scope.affected_path_roots: exceeds parent maximum")
            categories = scope.get("mutation_categories")
            allowed_for_capability = {
                category.value
                for category in CAPABILITY_MUTATION_CATEGORIES.get(kind, frozenset())
            }
            if isinstance(categories, list) and not all(
                category in allowed_for_capability for category in categories
            ):
                errors.append(
                    f"{path}.scope.mutation_categories: exceeds {kind} capability policy"
                )
            if isinstance(categories, list) and not _is_sequence_subset(
                categories, parent.get("maximum_mutation_categories")
            ):
                errors.append(f"{path}.scope.mutation_categories: exceeds parent maximum")
            if kind in {
                CapabilityKind.PROPOSAL_CORRECTION.value,
                CapabilityKind.IMPLEMENTATION_CORRECTION.value,
            }:
                budget = scope.get("correction_budget")
                parent_budget = parent.get("correction_budget")
                if isinstance(budget, dict) and isinstance(parent_budget, dict):
                    if set(budget) != set(parent_budget) or any(
                        not isinstance(parent_budget.get(name), int)
                        or value > parent_budget[name]
                        for name, value in budget.items()
                        if isinstance(value, int) and not isinstance(value, bool)
                    ):
                        errors.append(
                            f"{path}.scope.correction_budget: exceeds parent maximum"
                        )
        errors.extend(
            _validate_operation_within_target(
                capability,
                parent.get("maximum_target"),
                path,
                "parent maximum target",
            )
        )
    return errors


def validate_status_transition(kind: str, current: str, requested: str) -> list[str]:
    """Validate one durable lifecycle transition using the closed tables."""

    if kind not in STATUS_TRANSITION_TABLES:
        return [f"status transition kind: unknown value {kind!r}"]
    table = STATUS_TRANSITION_TABLES[kind]
    if current not in table:
        return [f"{kind}.status: unknown value {current!r}"]
    known_statuses = frozenset(table)
    if requested not in known_statuses:
        return [f"{kind}.requested_status: unknown value {requested!r}"]
    if requested not in table[current]:
        return [f"{kind}.status: illegal transition {current} -> {requested}"]
    return []


def validate_workflow_automation(
    automation: Any,
    *,
    top_level_change_id: str | None = None,
) -> list[str]:
    """Return deterministic errors for one unified automation subsection."""

    if not isinstance(automation, dict):
        return ["workflow.automation: expected object"]

    vocabulary_errors = _validate_vocabulary(automation)
    if vocabulary_errors:
        return vocabulary_errors

    required = {
        "mechanism",
        "schema_version",
        "run",
        "parent_authorizations",
        "effective_capabilities",
        "transition_receipts",
        "external_actions",
    }
    errors = _required(automation, required, "workflow.automation")
    for field in sorted(FORBIDDEN_LIVE_STATE_FIELDS):
        if field in automation:
            errors.append(
                f"workflow.automation.{field}: automation state must not own live workflow state"
            )

    run = automation.get("run")
    errors.extend(
        _required(run, {"run_id", "change_id", "status", "policy_version", "target"}, "workflow.automation.run")
    )
    run_change_id = top_level_change_id
    if isinstance(run, dict):
        if top_level_change_id is not None and run.get("change_id") != top_level_change_id:
            errors.append("workflow.automation.run.change_id: must match top-level change_id")
        run_change_id = run.get("change_id")
        errors.extend(_validate_target(run.get("target"), "workflow.automation.run.target"))

    parents = automation.get("parent_authorizations")
    if not isinstance(parents, dict):
        errors.append("workflow.automation.parent_authorizations: expected object")
        parents = {}
    for parent_id, parent in parents.items():
        errors.extend(
            _validate_parent(
                parent_id,
                parent,
                run_change_id,
                f"workflow.automation.parent_authorizations.{parent_id}",
            )
        )

    capabilities = automation.get("effective_capabilities")
    if not isinstance(capabilities, dict):
        errors.append("workflow.automation.effective_capabilities: expected object")
        capabilities = {}
    for capability_id, capability in capabilities.items():
        errors.extend(
            _validate_capability(
                capability_id,
                capability,
                parents,
                run_change_id,
                f"workflow.automation.effective_capabilities.{capability_id}",
            )
        )

    active_occurrences: dict[tuple[Any, Any, Any], str] = {}
    for capability_id, capability in capabilities.items():
        if not isinstance(capability, dict) or capability.get("status") != "active":
            continue
        stage = capability.get("stage")
        occurrence = stage.get("occurrence") if isinstance(stage, dict) else None
        milestone_id = occurrence.get("milestone_id") if isinstance(occurrence, dict) else None
        key = (
            stage.get("name") if isinstance(stage, dict) else None,
            occurrence.get("kind") if isinstance(occurrence, dict) else None,
            milestone_id if isinstance(milestone_id, str) or milestone_id is None else repr(milestone_id),
        )
        previous = active_occurrences.get(key)
        if previous is not None:
            errors.append(
                "workflow.automation.effective_capabilities: conflicting active capabilities "
                f"{previous} and {capability_id} for stage occurrence {key}"
            )
        active_occurrences[key] = capability_id

    if isinstance(run, dict) and "effective_capability_id" in run:
        capability_id = run["effective_capability_id"]
        if not isinstance(capability_id, str) or capability_id not in capabilities:
            errors.append("run.effective_capability_id: must reference an effective capability")
        else:
            capability_status = capabilities[capability_id].get("status")
            expected_status = {
                "active": "active",
                "completed": "consumed",
            }.get(run.get("status"))
            if expected_status is not None and capability_status != expected_status:
                errors.append(
                    f"run.effective_capability_id: capability must be {expected_status} "
                    f"when run is {run.get('status')}"
                )

    receipts = automation.get("transition_receipts")
    if not isinstance(receipts, dict):
        errors.append("workflow.automation.transition_receipts: expected object")
    else:
        prepared_count = sum(
            1
            for receipt in receipts.values()
            if isinstance(receipt, dict) and receipt.get("status") == "prepared"
        )
        if prepared_count > 1:
            errors.append(
                "workflow.automation.transition_receipts: at most one prepared transition is permitted"
            )
        receipt_required = {
            "transition_id",
            "transition_key",
            "policy_version",
            "run_id",
            "change_id",
            "from_position",
            "target",
            "effective_capability_id",
            "retry_policy",
            "input_identities",
            "expected_postcondition",
            "status",
            "outputs",
            "canonical_sync",
        }
        for receipt_id, receipt in receipts.items():
            path = f"workflow.automation.transition_receipts.{receipt_id}"
            errors.extend(_required(receipt, receipt_required, path))
            if not isinstance(receipt, dict):
                continue
            if receipt.get("transition_id") != receipt_id:
                errors.append(f"{path}.transition_id: must match mapping key")
            for field in ("transition_id", "transition_key", "run_id", "change_id", "from_position"):
                if not isinstance(receipt.get(field), str) or not receipt.get(field):
                    errors.append(f"{path}.{field}: expected non-empty string")
            if TRANSITION_KEY_FIELDS.issubset(receipt) and isinstance(
                receipt.get("transition_key"), str
            ):
                try:
                    expected_transition_key = compute_transition_key(receipt)
                except (TypeError, ValueError, RecursionError):
                    expected_transition_key = None
                if (
                    expected_transition_key is not None
                    and receipt["transition_key"] != expected_transition_key
                ):
                    errors.append(
                        f"{path}.transition_key: does not match immutable operation inputs"
                    )
            errors.extend(_validate_target(receipt.get("target"), f"{path}.target"))
            if isinstance(run, dict):
                if receipt.get("run_id") != run.get("run_id"):
                    errors.append(f"{path}.run_id: must match automation run")
                if receipt.get("change_id") != run.get("change_id"):
                    errors.append(f"{path}.change_id: must match automation run")
                if receipt.get("policy_version") != run.get("policy_version"):
                    errors.append(f"{path}.policy_version: must match automation run")
                if receipt.get("target") != run.get("target"):
                    errors.append(f"{path}.target: must match automation run target")
            errors.extend(
                _validate_evidence_object(receipt.get("input_identities"), f"{path}.input_identities")
            )
            errors.extend(
                _validate_concrete_object(
                    receipt.get("expected_postcondition"), f"{path}.expected_postcondition"
                )
            )
            outputs = receipt.get("outputs")
            if not isinstance(outputs, list):
                errors.append(f"{path}.outputs: expected array")
            else:
                if receipt.get("status") == "completed" and not outputs:
                    errors.append(f"{path}.outputs: completed receipt requires concrete output evidence")
                for index, output in enumerate(outputs):
                    errors.extend(_validate_concrete_value(output, f"{path}.outputs[{index}]"))
            errors.extend(
                _required(receipt.get("canonical_sync"), {"status"}, f"{path}.canonical_sync")
            )
            capability_id = receipt.get("effective_capability_id")
            if not isinstance(capability_id, str) or capability_id not in capabilities:
                errors.append(f"{path}.effective_capability_id: active capability not found")
            else:
                capability = capabilities[capability_id]
                if not isinstance(capability, dict):
                    errors.append(f"{path}.effective_capability_id: capability record must be an object")
                else:
                    expected_capability_status = {
                        "prepared": "active",
                        "completed": "consumed",
                    }.get(receipt.get("status"))
                    if (
                        expected_capability_status is not None
                        and capability.get("status") != expected_capability_status
                    ):
                        errors.append(
                            f"{path}.effective_capability_id: capability must be "
                            f"{expected_capability_status} for {receipt.get('status')} receipt"
                        )
                    if receipt.get("policy_version") != capability.get("policy_version"):
                        errors.append(f"{path}.policy_version: must match effective capability")
                    stage = capability.get("stage")
                    stage_name = stage.get("name") if isinstance(stage, dict) else None
                    try:
                        from_position = WorkflowPosition(receipt.get("from_position"))
                        operation_stage = WorkflowStage(stage_name)
                    except (TypeError, ValueError):
                        pass
                    else:
                        stage_policy = STAGE_POLICY_BY_STAGE.get(stage_name)
                        if (
                            stage_policy is not None
                            and receipt.get("retry_policy")
                            != stage_policy.retry_policy.value
                        ):
                            errors.append(
                                f"{path}.retry_policy: must match immutable stage policy "
                                f"{stage_policy.retry_policy.value}"
                            )
                        if not is_immediate_predecessor(from_position, operation_stage):
                            errors.append(
                                f"{path}.from_position: {from_position.value} cannot transition "
                                f"to {operation_stage.value}"
                            )
                    errors.extend(
                        _validate_operation_within_target(
                            capability,
                            receipt.get("target"),
                            f"{path}.effective_capability",
                            "run target",
                            receipt.get("from_position"),
                            receipt.get("input_identities"),
                        )
                    )

    migrations = automation.get("migration_receipts")
    if migrations is not None and not isinstance(migrations, dict):
        errors.append("workflow.automation.migration_receipts: expected object")
    elif isinstance(migrations, dict):
        required_migration_fields = {
            "migration_id",
            "source_mechanism",
            "source_record_identity",
            "migrated_at",
            "unified_run_id",
            "projection_result",
            "legacy_read_only",
        }
        for migration_id, migration in migrations.items():
            path = f"workflow.automation.migration_receipts.{migration_id}"
            errors.extend(_required(migration, required_migration_fields, path))
            if not isinstance(migration, dict):
                continue
            if migration.get("migration_id") != migration_id:
                errors.append(f"{path}.migration_id: must match mapping key")
            if not isinstance(migration.get("source_record_identity"), str) or not migration.get(
                "source_record_identity"
            ):
                errors.append(f"{path}.source_record_identity: expected non-empty string")
            migrated_at = migration.get("migrated_at")
            if not isinstance(migrated_at, str) or RFC3339_UTC_RE.fullmatch(migrated_at) is None:
                errors.append(f"{path}.migrated_at: expected RFC3339 UTC timestamp")
            if isinstance(run, dict) and migration.get("unified_run_id") != run.get("run_id"):
                errors.append(f"{path}.unified_run_id: must match automation run")
            if migration.get("legacy_read_only") is not True:
                errors.append(f"{path}.legacy_read_only: must be true")
    return errors


def has_read_only_legacy_migration(automation: Any) -> bool:
    """Return whether unified state durably marks its legacy source read-only."""

    if not isinstance(automation, dict):
        return False
    migrations = automation.get("migration_receipts")
    return isinstance(migrations, dict) and bool(migrations) and all(
        isinstance(receipt, dict) and receipt.get("legacy_read_only") is True
        for receipt in migrations.values()
    )


__all__ = [
    "CAPABILITY_STATUS_TRANSITIONS",
    "PARENT_STATUS_TRANSITIONS",
    "RUN_STATUS_TRANSITIONS",
    "compute_transition_key",
    "has_read_only_legacy_migration",
    "validate_status_transition",
    "validate_workflow_automation",
]
