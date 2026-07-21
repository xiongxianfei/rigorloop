#!/usr/bin/env python3
"""Unit tests for the immutable workflow-automation policy projection."""

from __future__ import annotations

import dataclasses
import unittest

from workflow_automation_policy import (
    INTERNAL_STAGES,
    PUBLIC_TARGET_STAGES,
    STAGE_POLICIES,
    OccurrenceKind,
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

    def test_duplicate_policy_fails_closed(self) -> None:
        errors = validate_policy_registry((*STAGE_POLICIES, STAGE_POLICIES[0]))
        self.assertTrue(any("duplicate stage policy" in error for error in errors), errors)

    def test_unknown_stage_fails_before_consistency(self) -> None:
        unknown = dataclasses.replace(STAGE_POLICIES[0], stage="future-stage")  # type: ignore[arg-type]
        errors = validate_policy_registry((unknown,))
        self.assertEqual(errors, ["policy[0].stage: unknown workflow stage: future-stage"])

    def test_unknown_retry_policy_fails_closed(self) -> None:
        unknown = dataclasses.replace(STAGE_POLICIES[0], retry_policy="retry-forever")  # type: ignore[arg-type]
        errors = validate_policy_registry((unknown,))
        self.assertEqual(errors, ["policy[0].retry_policy: unknown retry policy: retry-forever"])

    def test_policy_mutation_scope_cannot_exceed_capability(self) -> None:
        from workflow_automation_policy import MutationCategory

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
