#!/usr/bin/env python3
"""Immutable executable projection of the approved workflow-automation policy.

The approved specification remains normative.  This module deliberately contains
no state writer or command router; M1 only makes the closed policy representable
and mechanically checkable.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Iterable


class ClosedStringEnum(str, Enum):
    """String enum whose values serialize directly into tracked YAML evidence."""


class WorkflowStage(ClosedStringEnum):
    PROPOSAL = "proposal"
    PROPOSAL_REVIEW = "proposal-review"
    SPEC = "spec"
    SPEC_REVIEW = "spec-review"
    ARCHITECTURE_ASSESSMENT = "architecture-assessment"
    ARCHITECTURE = "architecture"
    ARCHITECTURE_REVIEW = "architecture-review"
    PLAN = "plan"
    PLAN_REVIEW = "plan-review"
    TEST_SPEC = "test-spec"
    TEST_SPEC_REVIEW = "test-spec-review"
    IMPLEMENT = "implement"
    CODE_REVIEW = "code-review"
    REVIEW_RESOLUTION = "review-resolution"
    CI_MAINTENANCE = "ci-maintenance"
    FINAL_HOLISTIC_CODE_REVIEW = "final-holistic-code-review"
    EXPLAIN_CHANGE = "explain-change"
    VERIFY = "verify"


class OccurrenceKind(ClosedStringEnum):
    SINGLETON = "singleton"
    MILESTONE = "milestone"
    FINAL = "final"


class AuthorizationClass(ClosedStringEnum):
    AUTHORING = "authoring"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"


class CapabilityKind(ClosedStringEnum):
    PROPOSAL_REVIEW = "proposal-review"
    PROPOSAL_CORRECTION = "proposal-correction"
    POST_PROPOSAL_AUTHORING = "post-proposal-authoring"
    IMPLEMENTATION = "implementation"
    IMPLEMENTATION_CORRECTION = "implementation-correction"
    VERIFICATION = "verification"


class MutationCategory(ClosedStringEnum):
    PROPOSAL_CONTENT = "proposal-content"
    DOWNSTREAM_AUTHORING_ARTIFACTS = "downstream-authoring-artifacts"
    CHANGE_LOCAL_REVIEW_EVIDENCE = "change-local-review-evidence"
    TESTS = "tests"
    PRODUCTION_CODE = "production-code"
    CHANGE_LOCAL_EVIDENCE = "change-local-evidence"
    VERIFICATION_EVIDENCE = "verification-evidence"


class ApplicabilityRule(ClosedStringEnum):
    REQUIRED = "required"
    CONDITIONAL = "conditional"
    TRIGGERED = "triggered"


class RetryPolicy(ClosedStringEnum):
    IDEMPOTENT_RETRY = "idempotent-retry"
    RECONCILE_ONLY = "reconcile-only"
    MANUAL_RECOVERY = "manual-recovery"


class CorrectionPolicy(ClosedStringEnum):
    NONE = "none"
    DRIVER_OWNED = "driver-owned"
    REVIEWER_OWNED = "reviewer-owned"
    NO_AUTOMATIC_REPAIR = "no-automatic-repair"


class StopBehavior(ClosedStringEnum):
    TARGET_AWARE = "target-aware"
    PAUSE_ON_UNSATISFIED_GATE = "pause-on-unsatisfied-gate"
    NOT_APPLICABLE_AWARE = "not-applicable-aware"
    PAUSE_ON_FAILURE = "pause-on-failure"
    STOP_BEFORE_PR = "stop-before-pr"


PUBLIC_TARGET_STAGES = frozenset(
    {
        WorkflowStage.PROPOSAL_REVIEW,
        WorkflowStage.SPEC,
        WorkflowStage.SPEC_REVIEW,
        WorkflowStage.ARCHITECTURE,
        WorkflowStage.ARCHITECTURE_REVIEW,
        WorkflowStage.PLAN,
        WorkflowStage.PLAN_REVIEW,
        WorkflowStage.TEST_SPEC,
        WorkflowStage.TEST_SPEC_REVIEW,
        WorkflowStage.IMPLEMENT,
        WorkflowStage.CODE_REVIEW,
        WorkflowStage.VERIFY,
    }
)

INTERNAL_STAGES = frozenset(
    {
        WorkflowStage.PROPOSAL,
        WorkflowStage.ARCHITECTURE_ASSESSMENT,
        WorkflowStage.REVIEW_RESOLUTION,
        WorkflowStage.CI_MAINTENANCE,
        WorkflowStage.EXPLAIN_CHANGE,
        WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW,
    }
)


@dataclass(frozen=True)
class StagePolicy:
    stage: WorkflowStage
    predecessor_rule: str
    owning_skill: str
    occurrence_rule: OccurrenceKind
    required_authorization_class: AuthorizationClass
    capability_kind: CapabilityKind
    permitted_mutation_category: MutationCategory
    applicability_rule: ApplicabilityRule
    prerequisite_rule: str
    required_input_identities: frozenset[str]
    completion_rule: str
    completion_evidence: frozenset[str]
    next_stage_calculation: str
    retry_policy: RetryPolicy
    correction_policy: CorrectionPolicy
    stop_behavior: StopBehavior


def _policy(
    stage: WorkflowStage,
    predecessor: str,
    skill: str,
    occurrence: OccurrenceKind,
    authorization: AuthorizationClass,
    capability: CapabilityKind,
    mutation: MutationCategory,
    applicability: ApplicabilityRule,
    prerequisite: str,
    inputs: tuple[str, ...],
    completion: str,
    evidence: tuple[str, ...],
    next_stage: str,
    retry: RetryPolicy,
    correction: CorrectionPolicy,
    stop: StopBehavior,
) -> StagePolicy:
    return StagePolicy(
        stage=stage,
        predecessor_rule=predecessor,
        owning_skill=skill,
        occurrence_rule=occurrence,
        required_authorization_class=authorization,
        capability_kind=capability,
        permitted_mutation_category=mutation,
        applicability_rule=applicability,
        prerequisite_rule=prerequisite,
        required_input_identities=frozenset(inputs),
        completion_rule=completion,
        completion_evidence=frozenset(evidence),
        next_stage_calculation=next_stage,
        retry_policy=retry,
        correction_policy=correction,
        stop_behavior=stop,
    )


S = WorkflowStage
O = OccurrenceKind
A = AuthorizationClass
C = CapabilityKind
M = MutationCategory
P = ApplicabilityRule
R = RetryPolicy
X = CorrectionPolicy
B = StopBehavior

CAPABILITY_MUTATION_CATEGORIES = {
    CapabilityKind.PROPOSAL_REVIEW: frozenset({MutationCategory.CHANGE_LOCAL_REVIEW_EVIDENCE}),
    CapabilityKind.PROPOSAL_CORRECTION: frozenset({MutationCategory.PROPOSAL_CONTENT}),
    CapabilityKind.POST_PROPOSAL_AUTHORING: frozenset(
        {
            MutationCategory.DOWNSTREAM_AUTHORING_ARTIFACTS,
            MutationCategory.CHANGE_LOCAL_REVIEW_EVIDENCE,
            MutationCategory.CHANGE_LOCAL_EVIDENCE,
        }
    ),
    CapabilityKind.IMPLEMENTATION: frozenset(
        {
            MutationCategory.TESTS,
            MutationCategory.PRODUCTION_CODE,
            MutationCategory.CHANGE_LOCAL_REVIEW_EVIDENCE,
        }
    ),
    CapabilityKind.IMPLEMENTATION_CORRECTION: frozenset(
        {MutationCategory.CHANGE_LOCAL_EVIDENCE}
    ),
    CapabilityKind.VERIFICATION: frozenset({MutationCategory.VERIFICATION_EVIDENCE}),
}

# The tuple is intentionally explicit: reviews can compare every stage projection
# with the approved contract without interpreting a generated policy DSL.
STAGE_POLICIES: tuple[StagePolicy, ...] = (
    _policy(S.PROPOSAL, "change-created", "proposal", O.SINGLETON, A.AUTHORING, C.PROPOSAL_CORRECTION, M.PROPOSAL_CONTENT, P.TRIGGERED, "proposal authoring or accepted correction is authorized", ("change", "proposal-scope"), "proposal identity is current and reviewable", ("proposal",), "proposal-review", R.RECONCILE_ONLY, X.DRIVER_OWNED, B.TARGET_AWARE),
    _policy(S.PROPOSAL_REVIEW, "proposal", "proposal-review", O.SINGLETON, A.AUTHORING, C.PROPOSAL_REVIEW, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "proposal and standing gates are current", ("proposal", "standing-gates", "review-policy"), "formal review occurrence is recorded", ("proposal-review",), "review outcome routing", R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.SPEC, "approved proposal review", "spec", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.REQUIRED, "clean proposal gate and resolution are current", ("proposal", "proposal-review", "review-resolution"), "spec is authored against current upstream identities", ("spec",), "spec-review", R.RECONCILE_ONLY, X.NONE, B.TARGET_AWARE),
    _policy(S.SPEC_REVIEW, "spec", "spec-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "spec identity is current", ("spec",), "formal spec review is recorded", ("spec-review",), "architecture-assessment", R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.ARCHITECTURE_ASSESSMENT, "approved spec review", "architecture", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_EVIDENCE, P.REQUIRED, "approved spec is current", ("spec", "spec-review"), "architecture applicability is recorded", ("architecture-assessment",), "architecture or plan", R.IDEMPOTENT_RETRY, X.NONE, B.NOT_APPLICABLE_AWARE),
    _policy(S.ARCHITECTURE, "architecture assessment", "architecture", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.CONDITIONAL, "architecture is required", ("spec", "architecture-assessment"), "architecture package is complete", ("architecture",), "architecture-review", R.RECONCILE_ONLY, X.NONE, B.NOT_APPLICABLE_AWARE),
    _policy(S.ARCHITECTURE_REVIEW, "architecture", "architecture-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.CONDITIONAL, "architecture identity is current", ("architecture",), "formal architecture review is recorded", ("architecture-review",), "plan", R.RECONCILE_ONLY, X.NONE, B.NOT_APPLICABLE_AWARE),
    _policy(S.PLAN, "approved spec and applicable architecture", "plan", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.REQUIRED, "upstream authoring gates are clean", ("spec", "applicable-architecture"), "valid active plan handoff is established", ("plan", "current-handoff-summary"), "plan-review", R.RECONCILE_ONLY, X.NONE, B.TARGET_AWARE),
    _policy(S.PLAN_REVIEW, "plan", "plan-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "plan identity is current", ("plan",), "formal plan review is recorded", ("plan-review",), "test-spec", R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.TEST_SPEC, "approved plan review", "test-spec", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.REQUIRED, "plan and upstream identities are current", ("plan", "plan-review", "spec"), "active test spec is authored", ("test-spec",), "test-spec-review", R.RECONCILE_ONLY, X.NONE, B.TARGET_AWARE),
    _policy(S.TEST_SPEC_REVIEW, "test-spec", "test-spec-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "test-spec identity is current", ("test-spec", "plan"), "formal test-spec review is recorded", ("test-spec-review",), "implement", R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.IMPLEMENT, "approved test-spec review or prior milestone close", "implement", O.MILESTONE, A.IMPLEMENTATION, C.IMPLEMENTATION, M.PRODUCTION_CODE, P.REQUIRED, "bound plan milestone and implementation basis are current", ("plan", "plan-review", "test-spec", "test-spec-review", "milestone"), "bound implementation exists, validation passes, and plan requests review", ("implementation-diff", "validation", "plan-handoff"), "code-review for bound milestone", R.MANUAL_RECOVERY, X.NONE, B.TARGET_AWARE),
    _policy(S.CODE_REVIEW, "implement for bound milestone", "code-review", O.MILESTONE, A.IMPLEMENTATION, C.IMPLEMENTATION, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "bound milestone is review-requested", ("plan", "milestone", "implementation-diff", "validation"), "milestone review is approved and resolution is closed", ("code-review", "review-resolution", "plan-handoff"), "next milestone or final holistic review", R.RECONCILE_ONLY, X.REVIEWER_OWNED, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.REVIEW_RESOLUTION, "material review findings", "review-resolution", O.SINGLETON, A.IMPLEMENTATION, C.IMPLEMENTATION_CORRECTION, M.CHANGE_LOCAL_EVIDENCE, P.TRIGGERED, "accepted implementation findings require resolution", ("review", "finding-set", "plan"), "required findings have final dispositions and evidence", ("review-resolution",), "rereview or next canonical stage", R.RECONCILE_ONLY, X.REVIEWER_OWNED, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.CI_MAINTENANCE, "implementation risk assessment", "ci-maintenance", O.SINGLETON, A.IMPLEMENTATION, C.IMPLEMENTATION, M.TESTS, P.TRIGGERED, "approved implementation scope requires CI maintenance", ("plan", "test-spec", "implementation-scope"), "required CI proof is current", ("ci-configuration", "ci-validation"), "implementation closeout", R.MANUAL_RECOVERY, X.NONE, B.PAUSE_ON_FAILURE),
    _policy(S.FINAL_HOLISTIC_CODE_REVIEW, "all implementation milestones closed", "code-review", O.FINAL, A.IMPLEMENTATION, C.IMPLEMENTATION, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "all milestone reviews and resolution are closed", ("plan", "milestone-reviews", "review-resolution"), "final holistic code review is clean", ("final-code-review",), "explain-change", R.RECONCILE_ONLY, X.REVIEWER_OWNED, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.EXPLAIN_CHANGE, "clean final holistic review", "explain-change", O.FINAL, A.VERIFICATION, C.VERIFICATION, M.VERIFICATION_EVIDENCE, P.REQUIRED, "verification basis is concrete", ("plan", "final-code-review", "implementation-diff"), "durable explanation is current", ("explain-change",), "verify", R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_FAILURE),
    _policy(S.VERIFY, "current explain-change", "verify", O.FINAL, A.VERIFICATION, C.VERIFICATION, M.VERIFICATION_EVIDENCE, P.REQUIRED, "all closeout evidence and verification inputs are current", ("plan", "final-code-review", "explain-change", "verification-commands"), "fresh verification passes", ("verify-report", "validation"), "pr", R.MANUAL_RECOVERY, X.NO_AUTOMATIC_REPAIR, B.STOP_BEFORE_PR),
)


def _unknown_enum_error(index: int, field_name: str, value: object, enum: type[Enum]) -> str | None:
    if isinstance(value, enum):
        return None
    allowed_values = {member.value for member in enum}
    label = "workflow stage" if field_name == "stage" else field_name.replace("_", " ")
    if any(value == allowed for allowed in allowed_values):
        return f"policy[{index}].{field_name}: expected typed {label}: {value}"
    return f"policy[{index}].{field_name}: unknown {label}: {value}"


def validate_policy_registry(policies: Iterable[StagePolicy]) -> list[str]:
    """Validate vocabulary before completeness and cross-field consistency."""

    records = tuple(policies)
    enum_fields: tuple[tuple[str, type[Enum]], ...] = (
        ("stage", WorkflowStage),
        ("occurrence_rule", OccurrenceKind),
        ("required_authorization_class", AuthorizationClass),
        ("capability_kind", CapabilityKind),
        ("permitted_mutation_category", MutationCategory),
        ("applicability_rule", ApplicabilityRule),
        ("retry_policy", RetryPolicy),
        ("correction_policy", CorrectionPolicy),
        ("stop_behavior", StopBehavior),
    )
    vocabulary_errors: list[str] = []
    for index, policy in enumerate(records):
        for field_name, enum in enum_fields:
            error = _unknown_enum_error(index, field_name, getattr(policy, field_name), enum)
            if error:
                vocabulary_errors.append(error)
    if vocabulary_errors:
        return vocabulary_errors

    errors: list[str] = []
    expected_fields = {field.name for field in fields(StagePolicy)}
    for index, policy in enumerate(records):
        for field_name in sorted(expected_fields):
            if getattr(policy, field_name) in (None, "", frozenset()):
                errors.append(f"policy[{index}].{field_name}: incomplete stage policy")

    seen: set[WorkflowStage] = set()
    for index, policy in enumerate(records):
        if policy.stage in seen:
            errors.append(f"policy[{index}].stage: duplicate stage policy: {policy.stage.value}")
        seen.add(policy.stage)

    expected = PUBLIC_TARGET_STAGES | INTERNAL_STAGES
    for missing in sorted(expected - seen, key=lambda stage: stage.value):
        errors.append(f"stage policy missing: {missing.value}")

    milestone_stages = {WorkflowStage.IMPLEMENT, WorkflowStage.CODE_REVIEW}
    final_stages = {
        WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW,
        WorkflowStage.EXPLAIN_CHANGE,
        WorkflowStage.VERIFY,
    }
    for policy in records:
        expected_occurrence = (
            OccurrenceKind.MILESTONE
            if policy.stage in milestone_stages
            else OccurrenceKind.FINAL
            if policy.stage in final_stages
            else OccurrenceKind.SINGLETON
        )
        if policy.occurrence_rule != expected_occurrence:
            errors.append(
                f"{policy.stage.value}.occurrence_rule: expected {expected_occurrence.value}"
            )
        allowed_mutations = CAPABILITY_MUTATION_CATEGORIES[policy.capability_kind]
        if policy.permitted_mutation_category not in allowed_mutations:
            errors.append(
                f"{policy.stage.value}.permitted_mutation_category: "
                f"{policy.permitted_mutation_category.value} exceeds {policy.capability_kind.value} capability"
            )
    return errors


POLICY_VALIDATION_ERRORS = tuple(validate_policy_registry(STAGE_POLICIES))
if POLICY_VALIDATION_ERRORS:
    raise RuntimeError("invalid workflow automation policy registry: " + "; ".join(POLICY_VALIDATION_ERRORS))

STAGE_POLICY_BY_STAGE = MappingProxyType({policy.stage.value: policy for policy in STAGE_POLICIES})
