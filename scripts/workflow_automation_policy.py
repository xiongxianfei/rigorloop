#!/usr/bin/env python3
"""Immutable executable projection of the approved workflow-automation policy.

The approved specification remains normative.  This module deliberately contains
no state writer or command router; M1 only makes the closed policy representable
and mechanically checkable.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum
from types import MappingProxyType
from typing import Any, Iterable, Mapping


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


class WorkflowPosition(ClosedStringEnum):
    CHANGE_CREATED = "change-created"
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
    PR = "pr"


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


class TransitionGuard(ClosedStringEnum):
    ALWAYS = "always"
    PROPOSAL_CORRECTION = "proposal-correction"
    ARCHITECTURE_REQUIRED = "architecture-required"
    ARCHITECTURE_NOT_REQUIRED = "architecture-not-required"
    IMPLEMENTATION_FINDINGS = "implementation-findings"
    NEXT_MILESTONE = "next-milestone"
    CI_TRIGGERED = "ci-triggered"
    ALL_MILESTONES_CLOSED = "all-milestones-closed"
    FINAL_REVIEW_FINDINGS = "final-review-findings"


class OccurrenceConstraint(ClosedStringEnum):
    STAGE_POLICY = "stage-policy"
    SAME_MILESTONE = "same-milestone"
    NEXT_MILESTONE = "next-milestone"


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


PUBLIC_TARGET_SEQUENCE = (
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
)


def _targets_from(stage: WorkflowStage) -> frozenset[WorkflowStage]:
    index = PUBLIC_TARGET_SEQUENCE.index(stage)
    return frozenset(PUBLIC_TARGET_SEQUENCE[index:])


@dataclass(frozen=True)
class TransitionRule:
    from_position: WorkflowPosition
    to_position: WorkflowPosition
    operation: WorkflowStage | None
    allowed_targets: frozenset[WorkflowStage]
    guard: TransitionGuard
    occurrence_constraint: OccurrenceConstraint = OccurrenceConstraint.STAGE_POLICY


@dataclass(frozen=True)
class TransitionContext:
    from_position: WorkflowPosition
    operation: WorkflowStage
    target: WorkflowStage
    operation_milestone_id: str | None = None
    operation_milestone_identity: str | None = None
    target_milestone_id: str | None = None
    plan_identity: str | None = None
    evidence: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence", MappingProxyType(dict(self.evidence)))


@dataclass(frozen=True)
class TransitionEvaluation:
    rule: TransitionRule | None
    errors: tuple[str, ...]

    @property
    def allowed(self) -> bool:
        return not self.errors and self.rule is not None


def _transition(
    from_position: WorkflowPosition,
    operation: WorkflowStage,
    target_frontier: WorkflowStage,
    guard: TransitionGuard = TransitionGuard.ALWAYS,
    occurrence: OccurrenceConstraint = OccurrenceConstraint.STAGE_POLICY,
) -> TransitionRule:
    return TransitionRule(
        from_position=from_position,
        to_position=WorkflowPosition(operation.value),
        operation=operation,
        allowed_targets=_targets_from(target_frontier),
        guard=guard,
        occurrence_constraint=occurrence,
    )


def _terminal_transition(
    from_position: WorkflowPosition,
    to_position: WorkflowPosition,
) -> TransitionRule:
    return TransitionRule(
        from_position=from_position,
        to_position=to_position,
        operation=None,
        allowed_targets=frozenset(),
        guard=TransitionGuard.ALWAYS,
    )


T = TransitionGuard
Q = OccurrenceConstraint

# Target permission belongs to the concrete edge, not to generic graph
# reachability.  Cycle edges deliberately use a later target frontier.
TRANSITION_RULES: tuple[TransitionRule, ...] = (
    _transition(
        WorkflowPosition.CHANGE_CREATED,
        WorkflowStage.PROPOSAL,
        WorkflowStage.PROPOSAL_REVIEW,
    ),
    _transition(
        WorkflowPosition.PROPOSAL_REVIEW,
        WorkflowStage.PROPOSAL,
        WorkflowStage.SPEC,
        T.PROPOSAL_CORRECTION,
    ),
    _transition(
        WorkflowPosition.PROPOSAL,
        WorkflowStage.PROPOSAL_REVIEW,
        WorkflowStage.PROPOSAL_REVIEW,
    ),
    _transition(WorkflowPosition.PROPOSAL_REVIEW, WorkflowStage.SPEC, WorkflowStage.SPEC),
    _transition(WorkflowPosition.SPEC, WorkflowStage.SPEC_REVIEW, WorkflowStage.SPEC_REVIEW),
    _transition(
        WorkflowPosition.SPEC_REVIEW,
        WorkflowStage.ARCHITECTURE_ASSESSMENT,
        WorkflowStage.ARCHITECTURE,
    ),
    _transition(
        WorkflowPosition.ARCHITECTURE_ASSESSMENT,
        WorkflowStage.ARCHITECTURE,
        WorkflowStage.ARCHITECTURE,
        T.ARCHITECTURE_REQUIRED,
    ),
    _transition(
        WorkflowPosition.ARCHITECTURE_ASSESSMENT,
        WorkflowStage.PLAN,
        WorkflowStage.PLAN,
        T.ARCHITECTURE_NOT_REQUIRED,
    ),
    _transition(
        WorkflowPosition.ARCHITECTURE,
        WorkflowStage.ARCHITECTURE_REVIEW,
        WorkflowStage.ARCHITECTURE_REVIEW,
    ),
    _transition(WorkflowPosition.ARCHITECTURE_REVIEW, WorkflowStage.PLAN, WorkflowStage.PLAN),
    _transition(WorkflowPosition.PLAN, WorkflowStage.PLAN_REVIEW, WorkflowStage.PLAN_REVIEW),
    _transition(WorkflowPosition.PLAN_REVIEW, WorkflowStage.TEST_SPEC, WorkflowStage.TEST_SPEC),
    _transition(WorkflowPosition.TEST_SPEC, WorkflowStage.TEST_SPEC_REVIEW, WorkflowStage.TEST_SPEC_REVIEW),
    _transition(WorkflowPosition.TEST_SPEC_REVIEW, WorkflowStage.IMPLEMENT, WorkflowStage.IMPLEMENT),
    _transition(
        WorkflowPosition.IMPLEMENT,
        WorkflowStage.CODE_REVIEW,
        WorkflowStage.CODE_REVIEW,
        occurrence=Q.SAME_MILESTONE,
    ),
    _transition(
        WorkflowPosition.CODE_REVIEW,
        WorkflowStage.IMPLEMENT,
        WorkflowStage.VERIFY,
        T.NEXT_MILESTONE,
        Q.NEXT_MILESTONE,
    ),
    _transition(
        WorkflowPosition.CODE_REVIEW,
        WorkflowStage.REVIEW_RESOLUTION,
        WorkflowStage.CODE_REVIEW,
        T.IMPLEMENTATION_FINDINGS,
    ),
    _transition(
        WorkflowPosition.REVIEW_RESOLUTION,
        WorkflowStage.CODE_REVIEW,
        WorkflowStage.CODE_REVIEW,
        T.IMPLEMENTATION_FINDINGS,
    ),
    _transition(WorkflowPosition.CODE_REVIEW, WorkflowStage.CI_MAINTENANCE, WorkflowStage.VERIFY, T.CI_TRIGGERED),
    _transition(
        WorkflowPosition.CODE_REVIEW,
        WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW,
        WorkflowStage.VERIFY,
        T.ALL_MILESTONES_CLOSED,
    ),
    _transition(
        WorkflowPosition.CI_MAINTENANCE,
        WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW,
        WorkflowStage.VERIFY,
        T.ALL_MILESTONES_CLOSED,
    ),
    _transition(
        WorkflowPosition.FINAL_HOLISTIC_CODE_REVIEW,
        WorkflowStage.REVIEW_RESOLUTION,
        WorkflowStage.VERIFY,
        T.FINAL_REVIEW_FINDINGS,
    ),
    _transition(
        WorkflowPosition.REVIEW_RESOLUTION,
        WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW,
        WorkflowStage.VERIFY,
        T.FINAL_REVIEW_FINDINGS,
    ),
    _transition(
        WorkflowPosition.FINAL_HOLISTIC_CODE_REVIEW,
        WorkflowStage.EXPLAIN_CHANGE,
        WorkflowStage.VERIFY,
    ),
    _transition(WorkflowPosition.EXPLAIN_CHANGE, WorkflowStage.VERIFY, WorkflowStage.VERIFY),
    _terminal_transition(WorkflowPosition.VERIFY, WorkflowPosition.PR),
)


@dataclass(frozen=True)
class StagePolicy:
    stage: WorkflowStage
    predecessor_rule: frozenset[TransitionRule]
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
    next_stage_calculation: frozenset[TransitionRule]
    retry_policy: RetryPolicy
    correction_policy: CorrectionPolicy
    stop_behavior: StopBehavior


def _policy(
    stage: WorkflowStage,
    predecessor: tuple[WorkflowPosition, ...],
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
    next_stage: tuple[WorkflowPosition, ...],
    retry: RetryPolicy,
    correction: CorrectionPolicy,
    stop: StopBehavior,
) -> StagePolicy:
    incoming_rules = frozenset(rule for rule in TRANSITION_RULES if rule.operation == stage)
    outgoing_rules = frozenset(
        rule
        for rule in TRANSITION_RULES
        if rule.from_position == WorkflowPosition(stage.value)
    )
    declared_predecessors = frozenset(predecessor)
    projected_predecessors = frozenset(rule.from_position for rule in incoming_rules)
    declared_successors = frozenset(next_stage)
    projected_successors = frozenset(rule.to_position for rule in outgoing_rules)
    if declared_predecessors != projected_predecessors:
        raise ValueError(f"{stage.value}: predecessor projection does not match transition rules")
    if declared_successors != projected_successors:
        raise ValueError(f"{stage.value}: next-stage projection does not match transition rules")
    return StagePolicy(
        stage=stage,
        predecessor_rule=incoming_rules,
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
        next_stage_calculation=outgoing_rules,
        retry_policy=retry,
        correction_policy=correction,
        stop_behavior=stop,
    )


S = WorkflowStage
W = WorkflowPosition
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
    _policy(S.PROPOSAL, (W.CHANGE_CREATED, W.PROPOSAL_REVIEW), "proposal", O.SINGLETON, A.AUTHORING, C.PROPOSAL_CORRECTION, M.PROPOSAL_CONTENT, P.TRIGGERED, "proposal authoring or accepted correction is authorized", ("change", "proposal-scope"), "proposal identity is current and reviewable", ("proposal",), (W.PROPOSAL_REVIEW,), R.RECONCILE_ONLY, X.DRIVER_OWNED, B.TARGET_AWARE),
    _policy(S.PROPOSAL_REVIEW, (W.PROPOSAL,), "proposal-review", O.SINGLETON, A.AUTHORING, C.PROPOSAL_REVIEW, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "proposal and standing gates are current", ("proposal", "standing-gates", "review-policy"), "formal review occurrence is recorded", ("proposal-review",), (W.PROPOSAL, W.SPEC), R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.SPEC, (W.PROPOSAL_REVIEW,), "spec", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.REQUIRED, "clean proposal gate and resolution are current", ("proposal", "proposal-review", "review-resolution"), "spec is authored against current upstream identities", ("spec",), (W.SPEC_REVIEW,), R.RECONCILE_ONLY, X.NONE, B.TARGET_AWARE),
    _policy(S.SPEC_REVIEW, (W.SPEC,), "spec-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "spec identity is current", ("spec",), "formal spec review is recorded", ("spec-review",), (W.ARCHITECTURE_ASSESSMENT,), R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.ARCHITECTURE_ASSESSMENT, (W.SPEC_REVIEW,), "architecture", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_EVIDENCE, P.REQUIRED, "approved spec is current", ("spec", "spec-review"), "architecture applicability is recorded", ("architecture-assessment",), (W.ARCHITECTURE, W.PLAN), R.IDEMPOTENT_RETRY, X.NONE, B.NOT_APPLICABLE_AWARE),
    _policy(S.ARCHITECTURE, (W.ARCHITECTURE_ASSESSMENT,), "architecture", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.CONDITIONAL, "architecture is required", ("spec", "architecture-assessment"), "architecture package is complete", ("architecture",), (W.ARCHITECTURE_REVIEW,), R.RECONCILE_ONLY, X.NONE, B.NOT_APPLICABLE_AWARE),
    _policy(S.ARCHITECTURE_REVIEW, (W.ARCHITECTURE,), "architecture-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.CONDITIONAL, "architecture identity is current", ("architecture",), "formal architecture review is recorded", ("architecture-review",), (W.PLAN,), R.RECONCILE_ONLY, X.NONE, B.NOT_APPLICABLE_AWARE),
    _policy(S.PLAN, (W.ARCHITECTURE_ASSESSMENT, W.ARCHITECTURE_REVIEW), "plan", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.REQUIRED, "upstream authoring gates are clean", ("spec", "applicable-architecture"), "valid active plan handoff is established", ("plan", "current-handoff-summary"), (W.PLAN_REVIEW,), R.RECONCILE_ONLY, X.NONE, B.TARGET_AWARE),
    _policy(S.PLAN_REVIEW, (W.PLAN,), "plan-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "plan identity is current", ("plan",), "formal plan review is recorded", ("plan-review",), (W.TEST_SPEC,), R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.TEST_SPEC, (W.PLAN_REVIEW,), "test-spec", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.DOWNSTREAM_AUTHORING_ARTIFACTS, P.REQUIRED, "plan and upstream identities are current", ("plan", "plan-review", "spec"), "active test spec is authored", ("test-spec",), (W.TEST_SPEC_REVIEW,), R.RECONCILE_ONLY, X.NONE, B.TARGET_AWARE),
    _policy(S.TEST_SPEC_REVIEW, (W.TEST_SPEC,), "test-spec-review", O.SINGLETON, A.AUTHORING, C.POST_PROPOSAL_AUTHORING, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "test-spec identity is current", ("test-spec", "plan"), "formal test-spec review is recorded", ("test-spec-review",), (W.IMPLEMENT,), R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.IMPLEMENT, (W.TEST_SPEC_REVIEW, W.CODE_REVIEW), "implement", O.MILESTONE, A.IMPLEMENTATION, C.IMPLEMENTATION, M.PRODUCTION_CODE, P.REQUIRED, "bound plan milestone and implementation basis are current", ("plan", "plan-review", "test-spec", "test-spec-review", "milestone"), "bound implementation exists, validation passes, and plan requests review", ("implementation-diff", "validation", "plan-handoff"), (W.CODE_REVIEW,), R.MANUAL_RECOVERY, X.NONE, B.TARGET_AWARE),
    _policy(S.CODE_REVIEW, (W.IMPLEMENT, W.REVIEW_RESOLUTION), "code-review", O.MILESTONE, A.IMPLEMENTATION, C.IMPLEMENTATION, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "bound milestone is review-requested", ("plan", "milestone", "implementation-diff", "validation"), "milestone review is approved and resolution is closed", ("code-review", "review-resolution", "plan-handoff"), (W.IMPLEMENT, W.REVIEW_RESOLUTION, W.CI_MAINTENANCE, W.FINAL_HOLISTIC_CODE_REVIEW), R.RECONCILE_ONLY, X.REVIEWER_OWNED, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.REVIEW_RESOLUTION, (W.CODE_REVIEW, W.FINAL_HOLISTIC_CODE_REVIEW), "review-resolution", O.SINGLETON, A.IMPLEMENTATION, C.IMPLEMENTATION_CORRECTION, M.CHANGE_LOCAL_EVIDENCE, P.TRIGGERED, "accepted implementation findings require resolution", ("review", "finding-set", "plan"), "required findings have final dispositions and evidence", ("review-resolution",), (W.CODE_REVIEW, W.FINAL_HOLISTIC_CODE_REVIEW), R.RECONCILE_ONLY, X.REVIEWER_OWNED, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.CI_MAINTENANCE, (W.CODE_REVIEW,), "ci-maintenance", O.SINGLETON, A.IMPLEMENTATION, C.IMPLEMENTATION, M.TESTS, P.TRIGGERED, "approved implementation scope requires CI maintenance", ("plan", "test-spec", "implementation-scope"), "required CI proof is current", ("ci-configuration", "ci-validation"), (W.FINAL_HOLISTIC_CODE_REVIEW,), R.MANUAL_RECOVERY, X.NONE, B.PAUSE_ON_FAILURE),
    _policy(S.FINAL_HOLISTIC_CODE_REVIEW, (W.CODE_REVIEW, W.CI_MAINTENANCE, W.REVIEW_RESOLUTION), "code-review", O.FINAL, A.IMPLEMENTATION, C.IMPLEMENTATION, M.CHANGE_LOCAL_REVIEW_EVIDENCE, P.REQUIRED, "all milestone reviews and resolution are closed", ("plan", "milestone-reviews", "review-resolution"), "final holistic code review is clean", ("final-code-review",), (W.REVIEW_RESOLUTION, W.EXPLAIN_CHANGE), R.RECONCILE_ONLY, X.REVIEWER_OWNED, B.PAUSE_ON_UNSATISFIED_GATE),
    _policy(S.EXPLAIN_CHANGE, (W.FINAL_HOLISTIC_CODE_REVIEW,), "explain-change", O.FINAL, A.VERIFICATION, C.VERIFICATION, M.VERIFICATION_EVIDENCE, P.REQUIRED, "verification basis is concrete", ("plan", "final-code-review", "implementation-diff"), "durable explanation is current", ("explain-change",), (W.VERIFY,), R.RECONCILE_ONLY, X.NONE, B.PAUSE_ON_FAILURE),
    _policy(S.VERIFY, (W.EXPLAIN_CHANGE,), "verify", O.FINAL, A.VERIFICATION, C.VERIFICATION, M.VERIFICATION_EVIDENCE, P.REQUIRED, "all closeout evidence and verification inputs are current", ("plan", "final-code-review", "explain-change", "verification-commands"), "fresh verification passes", ("verify-report", "validation"), (W.PR,), R.MANUAL_RECOVERY, X.NO_AUTOMATIC_REPAIR, B.STOP_BEFORE_PR),
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
        for field_name in ("predecessor_rule", "next_stage_calculation"):
            value = getattr(policy, field_name)
            if not isinstance(value, frozenset):
                vocabulary_errors.append(
                    f"policy[{index}].{field_name}: expected immutable workflow-position set"
                )
                continue
            for rule in value:
                if not isinstance(rule, TransitionRule):
                    vocabulary_errors.append(
                        f"policy[{index}].{field_name}: unknown transition rule: {rule}"
                    )
                    continue
                for nested_field, nested_value, nested_enum in (
                    ("from_position", rule.from_position, WorkflowPosition),
                    ("to_position", rule.to_position, WorkflowPosition),
                    ("guard", rule.guard, TransitionGuard),
                    ("occurrence_constraint", rule.occurrence_constraint, OccurrenceConstraint),
                ):
                    error = _unknown_enum_error(
                        index,
                        f"{field_name}.{nested_field}",
                        nested_value,
                        nested_enum,
                    )
                    if error:
                        vocabulary_errors.append(error)
                if rule.operation is not None:
                    error = _unknown_enum_error(
                        index,
                        f"{field_name}.operation",
                        rule.operation,
                        WorkflowStage,
                    )
                    if error:
                        vocabulary_errors.append(error)
                if not isinstance(rule.allowed_targets, frozenset):
                    vocabulary_errors.append(
                        f"policy[{index}].{field_name}.allowed_targets: expected immutable target set"
                    )
                else:
                    for target in rule.allowed_targets:
                        if target not in PUBLIC_TARGET_STAGES:
                            vocabulary_errors.append(
                                f"policy[{index}].{field_name}.allowed_targets: unknown public target: {target}"
                            )
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

    for policy in records:
        expected_incoming = frozenset(
            rule for rule in TRANSITION_RULES if rule.operation == policy.stage
        )
        expected_outgoing = frozenset(
            rule
            for rule in TRANSITION_RULES
            if rule.from_position == WorkflowPosition(policy.stage.value)
        )
        if policy.predecessor_rule != expected_incoming:
            errors.append(f"{policy.stage.value}.predecessor_rule: transition projection drift")
        if policy.next_stage_calculation != expected_outgoing:
            errors.append(f"{policy.stage.value}.next_stage_calculation: transition projection drift")
    return errors


POLICY_VALIDATION_ERRORS = tuple(validate_policy_registry(STAGE_POLICIES))
if POLICY_VALIDATION_ERRORS:
    raise RuntimeError("invalid workflow automation policy registry: " + "; ".join(POLICY_VALIDATION_ERRORS))

STAGE_POLICY_BY_STAGE = MappingProxyType({policy.stage.value: policy for policy in STAGE_POLICIES})
TRANSITION_RULES_BY_OPERATION = MappingProxyType(
    {
        stage: frozenset(rule for rule in TRANSITION_RULES if rule.operation == stage)
        for stage in WorkflowStage
    }
)


def is_immediate_predecessor(
    from_position: WorkflowPosition,
    to_stage: WorkflowStage,
) -> bool:
    """Check structural adjacency without granting transition permission."""

    return any(
        rule.from_position == from_position
        for rule in TRANSITION_RULES_BY_OPERATION[to_stage]
    )


def can_operation_fit_target(operation: WorkflowStage, target: WorkflowStage) -> bool:
    """Return whether an operation can fit a parent target structurally.

    Parent authorization validation has no concrete transition predecessor and
    therefore cannot evaluate a transition guard.  Receipt validation must use
    ``evaluate_transition`` instead.
    """

    return any(
        target in rule.allowed_targets
        for rule in TRANSITION_RULES_BY_OPERATION[operation]
    )


def _required_evidence(
    evidence: Mapping[str, Any],
    field_name: str,
    expected: str | None = None,
) -> tuple[str, ...]:
    value = evidence.get(field_name)
    if not isinstance(value, str) or not value.strip():
        return (f"transition evidence.{field_name}: required non-empty value",)
    if expected is not None and value != expected:
        return (f"transition evidence.{field_name}: expected {expected}",)
    return ()


def _evaluate_guard(
    rule: TransitionRule,
    evidence: Mapping[str, Any],
) -> tuple[str, ...]:
    guard = rule.guard
    if guard == TransitionGuard.ALWAYS:
        return ()
    if guard == TransitionGuard.PROPOSAL_CORRECTION:
        requirements = (
            ("review_outcome", "changes-requested"),
            ("review_identity", None),
            ("accepted_finding_set_identity", None),
            ("correction_budget_state", "remaining"),
            ("correction_budget_identity", None),
        )
    elif guard == TransitionGuard.ARCHITECTURE_REQUIRED:
        requirements = (
            ("architecture_applicability", "required"),
            ("architecture_applicability_identity", None),
        )
    elif guard == TransitionGuard.ARCHITECTURE_NOT_REQUIRED:
        requirements = (
            ("architecture_applicability", "not-applicable"),
            ("architecture_applicability_identity", None),
        )
    elif guard == TransitionGuard.IMPLEMENTATION_FINDINGS:
        requirements = (
            ("review_outcome", "changes-requested"),
            ("review_identity", None),
            ("accepted_finding_set_identity", None),
        )
    elif guard == TransitionGuard.NEXT_MILESTONE:
        requirements = (
            ("source_milestone_id", None),
            ("next_milestone_id", None),
            ("milestone_order_identity", None),
        )
    elif guard == TransitionGuard.CI_TRIGGERED:
        requirements = (("ci_trigger_identity", None),)
    elif guard == TransitionGuard.ALL_MILESTONES_CLOSED:
        requirements = (
            ("milestone_state", "all-closed"),
            ("closed_milestones_identity", None),
        )
    elif guard == TransitionGuard.FINAL_REVIEW_FINDINGS:
        requirements = (
            ("final_review_outcome", "changes-requested"),
            ("final_review_identity", None),
            ("accepted_finding_set_identity", None),
        )
    else:
        return (f"transition guard: unsupported value {guard!r}",)

    return tuple(
        error
        for field_name, expected in requirements
        for error in _required_evidence(evidence, field_name, expected)
    )


def _evaluate_occurrence(
    rule: TransitionRule,
    context: TransitionContext,
) -> tuple[str, ...]:
    constraint = rule.occurrence_constraint
    if constraint == OccurrenceConstraint.STAGE_POLICY:
        return ()

    errors: list[str] = []
    source_errors = _required_evidence(context.evidence, "source_milestone_id")
    errors.extend(source_errors)
    errors.extend(_required_evidence(context.evidence, "source_milestone_identity"))
    plan_errors = _required_evidence(context.evidence, "plan_identity")
    errors.extend(plan_errors)
    source_milestone_id = context.evidence.get("source_milestone_id")
    if not isinstance(context.operation_milestone_id, str) or not context.operation_milestone_id:
        errors.append("transition operation milestone_id: required non-empty value")

    if constraint == OccurrenceConstraint.SAME_MILESTONE:
        if (
            not source_errors
            and context.operation_milestone_id != source_milestone_id
        ):
            errors.append(
                "transition operation milestone_id: must match source_milestone_id"
            )
        if context.operation_milestone_identity != context.evidence.get(
            "source_milestone_identity"
        ):
            errors.append(
                "transition operation milestone identity: must match source_milestone_identity"
            )
        if (
            context.target == WorkflowStage.CODE_REVIEW
            and context.target_milestone_id != context.operation_milestone_id
        ):
            errors.append(
                "transition target milestone_id: must match operation milestone_id"
            )
    elif constraint == OccurrenceConstraint.NEXT_MILESTONE:
        next_errors = _required_evidence(context.evidence, "next_milestone_id")
        errors.extend(next_errors)
        errors.extend(_required_evidence(context.evidence, "next_milestone_identity"))
        errors.extend(
            _required_evidence(context.evidence, "milestone_order_identity")
        )
        next_milestone_id = context.evidence.get("next_milestone_id")
        if (
            not next_errors
            and context.operation_milestone_id != next_milestone_id
        ):
            errors.append(
                "transition operation milestone_id: must match next_milestone_id"
            )
        if context.operation_milestone_identity != context.evidence.get(
            "next_milestone_identity"
        ):
            errors.append(
                "transition operation milestone identity: must match next_milestone_identity"
            )
        if (
            not source_errors
            and not next_errors
            and source_milestone_id == next_milestone_id
        ):
            errors.append(
                "transition next_milestone_id: must differ from source_milestone_id"
            )
    if not plan_errors and context.plan_identity != context.evidence.get("plan_identity"):
        errors.append("transition plan identity: must match evidence plan_identity")
    if constraint in {
        OccurrenceConstraint.SAME_MILESTONE,
        OccurrenceConstraint.NEXT_MILESTONE,
    }:
        return tuple(errors)

    return (f"transition occurrence constraint: unsupported value {constraint!r}",)


def evaluate_transition(context: TransitionContext) -> TransitionEvaluation:
    """Evaluate one exact transition rule against target and predicate context."""

    candidates = tuple(
        rule
        for rule in TRANSITION_RULES_BY_OPERATION[context.operation]
        if rule.from_position == context.from_position
        and context.target in rule.allowed_targets
    )
    if not candidates:
        return TransitionEvaluation(
            rule=None,
            errors=("transition: no rule permits operation toward target",),
        )

    candidate_errors: list[str] = []
    for rule in candidates:
        errors = (
            *_evaluate_guard(rule, context.evidence),
            *_evaluate_occurrence(rule, context),
        )
        if not errors:
            return TransitionEvaluation(rule=rule, errors=())
        for error in errors:
            if error not in candidate_errors:
                candidate_errors.append(error)
    return TransitionEvaluation(rule=candidates[0], errors=tuple(candidate_errors))
