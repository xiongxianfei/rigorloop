#!/usr/bin/env python3
"""Unit tests for the immutable workflow-automation policy projection."""

from __future__ import annotations

import dataclasses
import unittest

from workflow_automation_policy import (
    ApplicabilityRule,
    AuthorizationClass,
    CapabilityKind,
    CorrectionPolicy,
    INTERNAL_STAGES,
    MutationCategory,
    OccurrenceConstraint,
    PUBLIC_TARGET_STAGES,
    PUBLIC_TARGET_SEQUENCE,
    RetryPolicy,
    STAGE_POLICIES,
    OccurrenceKind,
    StopBehavior,
    TRANSITION_RULES,
    TRANSITION_RULES_BY_OPERATION,
    TransitionContext,
    TransitionGuard,
    WorkflowPosition,
    WorkflowStage,
    evaluate_transition,
    is_immediate_predecessor,
    validate_policy_registry,
)


class WorkflowAutomationPolicyTests(unittest.TestCase):
    def test_registry_has_exactly_one_complete_policy_per_stage(self) -> None:
        expected = set(PUBLIC_TARGET_STAGES) | set(INTERNAL_STAGES)
        self.assertEqual({policy.stage for policy in STAGE_POLICIES}, expected)
        self.assertEqual(len(STAGE_POLICIES), len(expected))
        self.assertEqual(validate_policy_registry(STAGE_POLICIES), [])
        for policy in STAGE_POLICIES:
            for field in dataclasses.fields(policy):
                value = getattr(policy, field.name)
                self.assertNotIn(value, (None, "", frozenset()), field.name)

    def test_registry_records_are_frozen(self) -> None:
        with self.assertRaises(dataclasses.FrozenInstanceError):
            STAGE_POLICIES[0].owning_skill = "other"  # type: ignore[misc]

        with self.assertRaises(TypeError):
            TRANSITION_RULES_BY_OPERATION[WorkflowStage.PROPOSAL] = (  # type: ignore[index]
                frozenset()
            )

    def test_transition_rules_own_predecessor_and_target_boundaries(self) -> None:
        self.assertTrue(
            is_immediate_predecessor(
                WorkflowPosition.PROPOSAL,
                WorkflowStage.PROPOSAL_REVIEW,
            )
        )
        self.assertFalse(
            is_immediate_predecessor(
                WorkflowPosition.VERIFY,
                WorkflowStage.PROPOSAL_REVIEW,
            )
        )
        self.assertTrue(
            is_immediate_predecessor(
                WorkflowPosition.ARCHITECTURE_ASSESSMENT,
                WorkflowStage.PLAN,
            )
        )
        self.assertTrue(
            is_immediate_predecessor(
                WorkflowPosition.REVIEW_RESOLUTION,
                WorkflowStage.CODE_REVIEW,
            )
        )
        self.assertTrue(
            is_immediate_predecessor(
                WorkflowPosition.CODE_REVIEW,
                WorkflowStage.IMPLEMENT,
            )
        )
        self.assertTrue(
            evaluate_transition(
                TransitionContext(
                WorkflowPosition.IMPLEMENT,
                WorkflowStage.CODE_REVIEW,
                    WorkflowStage.CODE_REVIEW,
                    operation_milestone_id="M1",
                    operation_milestone_identity="sha256:M1",
                    target_milestone_id="M1",
                    plan_identity="sha256:plan",
                    evidence={
                        "source_milestone_id": "M1",
                        "source_milestone_identity": "sha256:M1",
                        "plan_identity": "sha256:plan",
                    },
                )
            )
            .allowed
        )
        self.assertFalse(
            evaluate_transition(
                TransitionContext(
                    WorkflowPosition.IMPLEMENT,
                    WorkflowStage.CODE_REVIEW,
                    WorkflowStage.IMPLEMENT,
                    operation_milestone_id="M1",
                    operation_milestone_identity="sha256:M1",
                    target_milestone_id="M1",
                    plan_identity="sha256:plan",
                    evidence={
                        "source_milestone_id": "M1",
                        "source_milestone_identity": "sha256:M1",
                        "plan_identity": "sha256:plan",
                    },
                )
            )
            .allowed
        )
        self.assertTrue(
            evaluate_transition(
                TransitionContext(
                    WorkflowPosition.PROPOSAL_REVIEW,
                    WorkflowStage.PROPOSAL,
                    WorkflowStage.SPEC,
                    evidence={
                        "review_outcome": "changes-requested",
                        "review_identity": "sha256:review",
                        "accepted_finding_set_identity": "sha256:findings",
                        "correction_budget_state": "remaining",
                        "correction_budget_identity": "sha256:budget",
                    },
                )
            )
            .allowed
        )
        self.assertFalse(
            evaluate_transition(
                TransitionContext(
                    WorkflowPosition.PROPOSAL_REVIEW,
                    WorkflowStage.PROPOSAL,
                    WorkflowStage.PROPOSAL_REVIEW,
                )
            )
            .allowed
        )

    def test_transition_rules_use_closed_guards_and_occurrence_constraints(self) -> None:
        self.assertTrue(TRANSITION_RULES)
        self.assertEqual(set(PUBLIC_TARGET_SEQUENCE), set(PUBLIC_TARGET_STAGES))
        self.assertEqual(len(PUBLIC_TARGET_SEQUENCE), len(PUBLIC_TARGET_STAGES))
        self.assertTrue(
            all(isinstance(rule.guard, TransitionGuard) for rule in TRANSITION_RULES)
        )
        self.assertTrue(
            all(
                isinstance(rule.occurrence_constraint, OccurrenceConstraint)
                for rule in TRANSITION_RULES
            )
        )

    def test_every_guard_has_positive_and_missing_evidence_contrasts(self) -> None:
        cases = (
            (
                TransitionGuard.PROPOSAL_CORRECTION,
                TransitionContext(
                    WorkflowPosition.PROPOSAL_REVIEW,
                    WorkflowStage.PROPOSAL,
                    WorkflowStage.SPEC,
                    evidence={
                        "review_outcome": "changes-requested",
                        "review_identity": "sha256:review",
                        "accepted_finding_set_identity": "sha256:findings",
                        "correction_budget_state": "remaining",
                        "correction_budget_identity": "sha256:budget",
                    },
                ),
            ),
            (
                TransitionGuard.ARCHITECTURE_REQUIRED,
                TransitionContext(
                    WorkflowPosition.ARCHITECTURE_ASSESSMENT,
                    WorkflowStage.ARCHITECTURE,
                    WorkflowStage.ARCHITECTURE,
                    evidence={
                        "architecture_applicability": "required",
                        "architecture_applicability_identity": "sha256:assessment",
                    },
                ),
            ),
            (
                TransitionGuard.ARCHITECTURE_NOT_REQUIRED,
                TransitionContext(
                    WorkflowPosition.ARCHITECTURE_ASSESSMENT,
                    WorkflowStage.PLAN,
                    WorkflowStage.PLAN,
                    evidence={
                        "architecture_applicability": "not-applicable",
                        "architecture_applicability_identity": "sha256:assessment",
                    },
                ),
            ),
            (
                TransitionGuard.IMPLEMENTATION_FINDINGS,
                TransitionContext(
                    WorkflowPosition.CODE_REVIEW,
                    WorkflowStage.REVIEW_RESOLUTION,
                    WorkflowStage.CODE_REVIEW,
                    evidence={
                        "review_outcome": "changes-requested",
                        "review_identity": "sha256:review",
                        "accepted_finding_set_identity": "sha256:findings",
                    },
                ),
            ),
            (
                TransitionGuard.NEXT_MILESTONE,
                TransitionContext(
                    WorkflowPosition.CODE_REVIEW,
                    WorkflowStage.IMPLEMENT,
                    WorkflowStage.VERIFY,
                    operation_milestone_id="M2",
                    operation_milestone_identity="sha256:M2",
                    plan_identity="sha256:plan",
                    evidence={
                        "source_milestone_id": "M1",
                        "source_milestone_identity": "sha256:M1",
                        "next_milestone_id": "M2",
                        "next_milestone_identity": "sha256:M2",
                        "milestone_order_identity": "sha256:order",
                        "plan_identity": "sha256:plan",
                    },
                ),
            ),
            (
                TransitionGuard.CI_TRIGGERED,
                TransitionContext(
                    WorkflowPosition.CODE_REVIEW,
                    WorkflowStage.CI_MAINTENANCE,
                    WorkflowStage.VERIFY,
                    evidence={"ci_trigger_identity": "sha256:ci-trigger"},
                ),
            ),
            (
                TransitionGuard.ALL_MILESTONES_CLOSED,
                TransitionContext(
                    WorkflowPosition.CODE_REVIEW,
                    WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW,
                    WorkflowStage.VERIFY,
                    evidence={
                        "milestone_state": "all-closed",
                        "closed_milestones_identity": "sha256:closed",
                    },
                ),
            ),
            (
                TransitionGuard.FINAL_REVIEW_FINDINGS,
                TransitionContext(
                    WorkflowPosition.FINAL_HOLISTIC_CODE_REVIEW,
                    WorkflowStage.REVIEW_RESOLUTION,
                    WorkflowStage.VERIFY,
                    evidence={
                        "final_review_outcome": "changes-requested",
                        "final_review_identity": "sha256:review",
                        "accepted_finding_set_identity": "sha256:findings",
                    },
                ),
            ),
        )
        self.assertEqual(
            {guard for guard, _ in cases},
            set(TransitionGuard) - {TransitionGuard.ALWAYS},
        )
        for guard, context in cases:
            with self.subTest(guard=guard.value):
                result = evaluate_transition(context)
                self.assertTrue(result.allowed, result.errors)
                missing = dataclasses.replace(context, evidence={})
                rejected = evaluate_transition(missing)
                self.assertFalse(rejected.allowed)
                self.assertTrue(rejected.errors)

    def test_occurrence_constraints_are_enforced(self) -> None:
        same = TransitionContext(
            WorkflowPosition.IMPLEMENT,
            WorkflowStage.CODE_REVIEW,
            WorkflowStage.CODE_REVIEW,
            operation_milestone_id="M1",
            operation_milestone_identity="sha256:M1",
            target_milestone_id="M1",
            plan_identity="sha256:plan",
            evidence={
                "source_milestone_id": "M1",
                "source_milestone_identity": "sha256:M1",
                "plan_identity": "sha256:plan",
            },
        )
        self.assertTrue(evaluate_transition(same).allowed)
        self.assertFalse(
            evaluate_transition(
                dataclasses.replace(
                    same,
                    evidence={
                        "source_milestone_id": "M0",
                        "source_milestone_identity": "sha256:M0",
                        "plan_identity": "sha256:plan",
                    },
                )
            ).allowed
        )

        next_milestone = TransitionContext(
            WorkflowPosition.CODE_REVIEW,
            WorkflowStage.IMPLEMENT,
            WorkflowStage.VERIFY,
            operation_milestone_id="M2",
            operation_milestone_identity="sha256:M2",
            plan_identity="sha256:plan",
            evidence={
                "source_milestone_id": "M1",
                "source_milestone_identity": "sha256:M1",
                "next_milestone_id": "M2",
                "next_milestone_identity": "sha256:M2",
                "milestone_order_identity": "sha256:order",
                "plan_identity": "sha256:plan",
            },
        )
        self.assertTrue(evaluate_transition(next_milestone).allowed)
        for target in (WorkflowStage.IMPLEMENT, WorkflowStage.CODE_REVIEW):
            with self.subTest(target=target.value):
                self.assertTrue(
                    evaluate_transition(
                        dataclasses.replace(
                            next_milestone,
                            target=target,
                            target_milestone_id="M2",
                        )
                    ).allowed
                )
                self.assertFalse(
                    evaluate_transition(
                        dataclasses.replace(
                            next_milestone,
                            target=target,
                            target_milestone_id="M1",
                        )
                    ).allowed
                )
                self.assertFalse(
                    evaluate_transition(
                        dataclasses.replace(
                            next_milestone,
                            target=target,
                            target_milestone_id=None,
                        )
                    ).allowed
                )
        self.assertFalse(
            evaluate_transition(
                dataclasses.replace(next_milestone, operation_milestone_id="M99")
            ).allowed
        )
        wrong_plan = dict(next_milestone.evidence)
        wrong_plan["plan_identity"] = "sha256:other-plan"
        self.assertFalse(
            evaluate_transition(
                dataclasses.replace(next_milestone, evidence=wrong_plan)
            ).allowed
        )

    def test_public_stage_occurrence_vocabulary_matches_spec(self) -> None:
        occurrences = {
            policy.stage: policy.occurrence_rule
            for policy in STAGE_POLICIES
            if policy.stage in PUBLIC_TARGET_STAGES
        }
        for stage in PUBLIC_TARGET_STAGES - {
            WorkflowStage.IMPLEMENT,
            WorkflowStage.CODE_REVIEW,
            WorkflowStage.VERIFY,
        }:
            self.assertEqual(occurrences[stage], OccurrenceKind.SINGLETON)
        self.assertEqual(occurrences[WorkflowStage.IMPLEMENT], OccurrenceKind.MILESTONE)
        self.assertEqual(occurrences[WorkflowStage.CODE_REVIEW], OccurrenceKind.MILESTONE)
        self.assertEqual(occurrences[WorkflowStage.VERIFY], OccurrenceKind.FINAL)

    def test_internal_stage_occurrence_vocabulary_matches_spec(self) -> None:
        occurrences = {policy.stage: policy.occurrence_rule for policy in STAGE_POLICIES}
        for stage in {
            WorkflowStage.PROPOSAL,
            WorkflowStage.ARCHITECTURE_ASSESSMENT,
            WorkflowStage.REVIEW_RESOLUTION,
            WorkflowStage.CI_MAINTENANCE,
        }:
            self.assertEqual(occurrences[stage], OccurrenceKind.SINGLETON)
        for stage in {
            WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW,
            WorkflowStage.EXPLAIN_CHANGE,
        }:
            self.assertEqual(occurrences[stage], OccurrenceKind.FINAL)

    def test_duplicate_policy_fails_closed(self) -> None:
        errors = validate_policy_registry((*STAGE_POLICIES, STAGE_POLICIES[0]))
        self.assertTrue(any("duplicate stage policy" in error for error in errors), errors)

    def test_unknown_value_for_each_policy_vocabulary_fails_before_consistency(self) -> None:
        cases = (
            ("stage", "future-stage", WorkflowStage),
            ("occurrence_rule", "iteration", OccurrenceKind),
            ("required_authorization_class", "external", AuthorizationClass),
            ("capability_kind", "deploy", CapabilityKind),
            ("permitted_mutation_category", "secrets", MutationCategory),
            ("applicability_rule", "sometimes", ApplicabilityRule),
            ("retry_policy", "retry-forever", RetryPolicy),
            ("correction_policy", "author-guesses", CorrectionPolicy),
            ("stop_behavior", "continue-always", StopBehavior),
        )
        for field_name, unknown_value, enum in cases:
            with self.subTest(field=field_name):
                unknown = dataclasses.replace(  # type: ignore[arg-type]
                    STAGE_POLICIES[0], **{field_name: unknown_value}
                )
                errors = validate_policy_registry((unknown,))
                self.assertEqual(len(errors), 1, errors)
                self.assertIn(f"policy[0].{field_name}: unknown", errors[0])
                self.assertNotIn(unknown_value, {member.value for member in enum})

    def test_unknown_workflow_position_value_fails_closed(self) -> None:
        for field_name in ("predecessor_rule", "next_stage_calculation"):
            with self.subTest(field=field_name):
                unknown = dataclasses.replace(
                    STAGE_POLICIES[0], **{field_name: frozenset({"future-position"})}
                )
                errors = validate_policy_registry((unknown,))
                self.assertTrue(any(field_name in error and "unknown" in error for error in errors), errors)

    def test_unknown_transition_rule_vocabulary_fails_closed(self) -> None:
        policy = STAGE_POLICIES[0]
        original_rule = next(iter(policy.predecessor_rule))
        cases = (
            ("guard", "future-guard"),
            ("occurrence_constraint", "future-occurrence"),
        )
        for field_name, unknown_value in cases:
            with self.subTest(field=field_name):
                unknown_rule = dataclasses.replace(
                    original_rule,
                    **{field_name: unknown_value},  # type: ignore[arg-type]
                )
                unknown_policy = dataclasses.replace(
                    policy,
                    predecessor_rule=frozenset({unknown_rule}),
                )
                errors = validate_policy_registry((unknown_policy,))
                self.assertTrue(
                    any(field_name in error and "unknown" in error for error in errors),
                    errors,
                )

    def test_incomplete_policy_field_fails_closed(self) -> None:
        for field_name in (
            "predecessor_rule",
            "owning_skill",
            "prerequisite_rule",
            "required_input_identities",
            "completion_rule",
            "completion_evidence",
            "next_stage_calculation",
        ):
            with self.subTest(field=field_name):
                value = frozenset() if isinstance(getattr(STAGE_POLICIES[0], field_name), frozenset) else ""
                incomplete = dataclasses.replace(STAGE_POLICIES[0], **{field_name: value})
                errors = validate_policy_registry(
                    tuple(incomplete if policy.stage == incomplete.stage else policy for policy in STAGE_POLICIES)
                )
                self.assertIn(f"policy[0].{field_name}: incomplete stage policy", errors)

    def test_changed_internal_occurrence_fails_closed(self) -> None:
        original = next(
            policy for policy in STAGE_POLICIES
            if policy.stage == WorkflowStage.FINAL_HOLISTIC_CODE_REVIEW
        )
        changed = dataclasses.replace(original, occurrence_rule=OccurrenceKind.SINGLETON)
        errors = validate_policy_registry(
            tuple(changed if policy.stage == changed.stage else policy for policy in STAGE_POLICIES)
        )
        self.assertIn(
            "final-holistic-code-review.occurrence_rule: expected final",
            errors,
        )

    def test_policy_mutation_scope_cannot_exceed_capability(self) -> None:
        widened = dataclasses.replace(
            STAGE_POLICIES[1],
            permitted_mutation_category=MutationCategory.PRODUCTION_CODE,
        )
        errors = validate_policy_registry(
            tuple(widened if policy.stage == widened.stage else policy for policy in STAGE_POLICIES)
        )
        self.assertTrue(any("exceeds proposal-review capability" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
