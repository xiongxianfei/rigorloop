#!/usr/bin/env python3
"""Unit tests for unified workflow-automation state validation."""

from __future__ import annotations

import copy
import unittest

from validate_workflow_automation import validate_workflow_automation
from validate_workflow_automation import (
    CAPABILITY_STATUS_TRANSITIONS,
    PARENT_STATUS_TRANSITIONS,
    RUN_STATUS_TRANSITIONS,
    validate_status_transition,
)


def valid_automation() -> dict[str, object]:
    return {
        "mechanism": "bounded-review-fix",
        "schema_version": 1,
        "run": {
            "run_id": "run-001",
            "change_id": "2026-07-20-example",
            "status": "active",
            "policy_version": 1,
            "target": {
                "stage": "proposal-review",
                "occurrence": {"kind": "singleton"},
                "bound_at": "2026-07-20T00:00:00Z",
                "completion": {"review_occurrence": "recorded"},
            },
        },
        "parent_authorizations": {
            "authorization-authoring-001": {
                "authorization_id": "authorization-authoring-001",
                "authorization_class": "authoring",
                "policy_version": 1,
                "change_id": "2026-07-20-example",
                "authorized_by": "user",
                "authorized_at": "2026-07-20T00:00:00Z",
                "maximum_target": {
                    "stage": "proposal-review",
                    "occurrence": {"kind": "singleton"},
                },
                "allowed_capability_kinds": ["proposal-review"],
                "maximum_path_roots": ["docs/changes/2026-07-20-example/"],
                "maximum_mutation_categories": ["change-local-review-evidence"],
                "status": "active",
                "revocation": {"revoked": False},
                "invalidation": {"on_policy_change": "pause"},
                "external_actions": "prohibited",
            }
        },
        "effective_capabilities": {
            "capability-proposal-review-001": {
                "capability_id": "capability-proposal-review-001",
                "capability_kind": "proposal-review",
                "parent_authorization_id": "authorization-authoring-001",
                "policy_version": 1,
                "change_id": "2026-07-20-example",
                "stage": {
                    "name": "proposal-review",
                    "occurrence": {"kind": "singleton"},
                },
                "basis": {
                    "proposal_identity": "sha256:proposal",
                    "standing_gates_identity": "sha256:gates",
                    "review_policy_identity": "sha256:policy",
                    "structured_target_identity": "sha256:target",
                    "review_evidence_roots": ["docs/changes/2026-07-20-example/"],
                },
                "scope": {
                    "affected_path_roots": ["docs/changes/2026-07-20-example/"],
                    "mutation_categories": ["change-local-review-evidence"],
                },
                "derived_at": "2026-07-20T00:01:00Z",
                "status": "active",
                "invalidation": {"on_parent_revocation": "invalidate"},
            }
        },
        "transition_receipts": {},
        "external_actions": "prohibited",
    }


class WorkflowAutomationVocabularyTests(unittest.TestCase):
    def test_valid_unified_state_passes(self) -> None:
        self.assertEqual(validate_workflow_automation(valid_automation()), [])

    def test_unknown_vocabulary_values_fail_before_consistency(self) -> None:
        cases = (
            (("mechanism",), "other", "mechanism"),
            (("mechanism",), ["bounded-review-fix"], "mechanism"),
            (("schema_version",), 99, "schema_version"),
            (("run", "status"), "waiting", "run.status"),
            (("run", "target", "stage"), "future-stage", "run.target.stage"),
            (("run", "target", "occurrence", "kind"), "iteration", "occurrence.kind"),
            (("parent_authorizations", "authorization-authoring-001", "authorization_class"), "external", "authorization_class"),
            (("parent_authorizations", "authorization-authoring-001", "status"), "paused", "status"),
            (("effective_capabilities", "capability-proposal-review-001", "capability_kind"), "deploy", "capability_kind"),
            (("effective_capabilities", "capability-proposal-review-001", "status"), "paused", "status"),
        )
        for path, value, expected in cases:
            with self.subTest(path=path):
                state = valid_automation()
                cursor = state
                for key in path[:-1]:
                    cursor = cursor[key]  # type: ignore[index,assignment]
                cursor[path[-1]] = value  # type: ignore[index]
                if path != ("run", "target", "occurrence", "kind"):
                    state["run"]["target"]["occurrence"]["kind"] = "milestone"  # type: ignore[index]
                errors = validate_workflow_automation(state)
                self.assertTrue(errors)
                self.assertIn(expected, errors[0])
                self.assertFalse(any("incompatible" in error for error in errors), errors)

    def test_receipt_and_review_vocabulary_values_fail_closed(self) -> None:
        state = valid_automation()
        state["transition_receipts"] = {
            "transition-001": {
                "transition_id": "transition-001",
                "transition_key": "sha256:transition",
                "policy_version": 1,
                "run_id": "run-001",
                "change_id": "2026-07-20-example",
                "from_position": "proposal",
                "target": copy.deepcopy(state["run"]["target"]),  # type: ignore[index]
                "effective_capability_id": "capability-proposal-review-001",
                "input_identities": {"proposal": "sha256:proposal"},
                "expected_postcondition": {"review_occurrence": "recorded"},
                "status": "prepared",
                "retry_policy": "reconcile-only",
                "outputs": [],
                "canonical_sync": {"status": "pending"},
            }
        }
        state["latest_review_result"] = {
            "outcome": "approved",
            "clean_gate": "satisfied",
            "routing_action": "continue",
        }
        mutations = (
            (("transition_receipts", "transition-001", "status"), "waiting", "status"),
            (("transition_receipts", "transition-001", "retry_policy"), "retry-forever", "retry_policy"),
            (("transition_receipts", "transition-001", "canonical_sync", "status"), "unknown", "canonical_sync.status"),
            (("latest_review_result", "outcome"), "maybe", "outcome"),
            (("latest_review_result", "clean_gate"), "clean-ish", "clean_gate"),
            (("latest_review_result", "routing_action"), "skip", "routing_action"),
        )
        for path, value, expected in mutations:
            with self.subTest(path=path):
                candidate = copy.deepcopy(state)
                cursor = candidate
                for key in path[:-1]:
                    cursor = cursor[key]  # type: ignore[index,assignment]
                cursor[path[-1]] = value  # type: ignore[index]
                errors = validate_workflow_automation(candidate)
                self.assertTrue(errors)
                self.assertIn(expected, errors[0])

    def test_policy_version_vocabulary_fails_closed(self) -> None:
        state = valid_automation()
        state["run"]["policy_version"] = 99  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertIn("policy_version", errors[0])

    def test_closed_status_transition_tables_match_spec(self) -> None:
        self.assertEqual(
            RUN_STATUS_TRANSITIONS,
            {
                "active": frozenset({"paused", "completed", "cancelled"}),
                "paused": frozenset({"active", "cancelled"}),
                "completed": frozenset(),
                "cancelled": frozenset(),
            },
        )
        self.assertEqual(validate_status_transition("run", "paused", "active"), [])
        self.assertIn(
            "illegal transition completed -> active",
            validate_status_transition("run", "completed", "active")[0],
        )
        self.assertIn(
            "illegal transition consumed -> active",
            validate_status_transition("effective-capability", "consumed", "active")[0],
        )
        self.assertIn(
            "unknown value 'waiting'",
            validate_status_transition("run", "waiting", "active")[0],
        )
        self.assertEqual(
            PARENT_STATUS_TRANSITIONS,
            {
                "active": frozenset({"revoked", "invalidated"}),
                "revoked": frozenset(),
                "invalidated": frozenset(),
            },
        )
        self.assertEqual(
            CAPABILITY_STATUS_TRANSITIONS,
            {
                "active": frozenset({"consumed", "invalidated"}),
                "consumed": frozenset(),
                "invalidated": frozenset(),
            },
        )

    def test_parent_authorization_is_not_executable(self) -> None:
        state = valid_automation()
        state["run"]["effective_capability_id"] = "authorization-authoring-001"  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertIn("run.effective_capability_id: must reference an effective capability", errors)

    def test_capability_scope_must_be_subset_of_parent(self) -> None:
        state = valid_automation()
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["scope"]["mutation_categories"] = ["production-code"]  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("exceeds parent maximum" in error for error in errors), errors)

    def test_proposal_review_basis_does_not_require_prior_review(self) -> None:
        self.assertEqual(validate_workflow_automation(valid_automation()), [])

    def test_later_capability_requires_review_identity(self) -> None:
        state = valid_automation()
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["allowed_capability_kinds"] = ["post-proposal-authoring"]  # type: ignore[index]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["capability_kind"] = "post-proposal-authoring"  # type: ignore[index]
        capability["stage"]["name"] = "spec"  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("approved_proposal_review_identity" in error for error in errors), errors)

    def test_repeated_target_requires_milestone_and_plan_identity(self) -> None:
        state = valid_automation()
        target = state["run"]["target"]  # type: ignore[index]
        target["stage"] = "implement"  # type: ignore[index]
        target["occurrence"] = {"kind": "milestone", "milestone_id": "M1"}  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertIn(
            "workflow.automation.run.target.plan_identity: required for repeated-stage target",
            errors,
        )

    def test_forbidden_live_state_fields_fail(self) -> None:
        state = valid_automation()
        state["next_stage"] = "spec"
        self.assertIn(
            "workflow.automation.next_stage: automation state must not own live workflow state",
            validate_workflow_automation(state),
        )


if __name__ == "__main__":
    unittest.main()
