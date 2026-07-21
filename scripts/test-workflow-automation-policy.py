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
    PUBLIC_TARGET_STAGES,
    RetryPolicy,
    STAGE_POLICIES,
    OccurrenceKind,
    StopBehavior,
    WorkflowStage,
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
