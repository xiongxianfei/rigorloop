#!/usr/bin/env python3
"""Unit tests for unified workflow-automation state validation."""

from __future__ import annotations

import copy
import unittest

from validate_workflow_automation import validate_workflow_automation
from validate_workflow_automation import (
    CAPABILITY_STATUS_TRANSITIONS,
    PARENT_STATUS_TRANSITIONS,
    PUBLIC_TARGET_ORDER,
    RUN_STATUS_TRANSITIONS,
    STAGE_TARGET_FRONTIER,
    validate_status_transition,
)
from workflow_automation_policy import PUBLIC_TARGET_STAGES, WorkflowStage


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
                    "bound_at": "2026-07-20T00:00:00Z",
                    "completion": {"review_occurrence": "recorded"},
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


def add_valid_receipt(state: dict[str, object]) -> dict[str, object]:
    receipt = {
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
    state["transition_receipts"] = {"transition-001": receipt}
    return receipt


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
            (("external_actions",), "allowed", "external_actions"),
            (("parent_authorizations", "authorization-authoring-001", "external_actions"), "allowed", "external_actions"),
            (("parent_authorizations", "authorization-authoring-001", "allowed_capability_kinds", 0), "deploy", "allowed_capability_kinds[0]"),
            (("parent_authorizations", "authorization-authoring-001", "maximum_mutation_categories", 0), "secrets", "maximum_mutation_categories[0]"),
            (("effective_capabilities", "capability-proposal-review-001", "stage", "name"), "future-stage", "stage.name"),
            (("effective_capabilities", "capability-proposal-review-001", "stage", "occurrence", "kind"), "iteration", "stage.occurrence.kind"),
            (("effective_capabilities", "capability-proposal-review-001", "scope", "mutation_categories", 0), "secrets", "mutation_categories[0]"),
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
        add_valid_receipt(state)
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

    def test_unknown_policy_version_vocabulary_fails_closed_for_every_record(self) -> None:
        cases = (
            ("run", ("run", "policy_version")),
            ("parent", ("parent_authorizations", "authorization-authoring-001", "policy_version")),
            ("capability", ("effective_capabilities", "capability-proposal-review-001", "policy_version")),
            ("receipt", ("transition_receipts", "transition-001", "policy_version")),
        )
        for label, path in cases:
            with self.subTest(record=label):
                state = valid_automation()
                add_valid_receipt(state)
                cursor = state
                for key in path[:-1]:
                    cursor = cursor[key]  # type: ignore[index,assignment]
                cursor[path[-1]] = 99  # type: ignore[index]
                errors = validate_workflow_automation(state)
                self.assertIn("policy_version", errors[0])

    def test_unknown_invalidation_action_vocabulary_fails_closed(self) -> None:
        for record_path in (
            ("parent_authorizations", "authorization-authoring-001", "invalidation", "on_policy_change"),
            ("effective_capabilities", "capability-proposal-review-001", "invalidation", "on_parent_revocation"),
        ):
            with self.subTest(path=record_path):
                state = valid_automation()
                cursor = state
                for key in record_path[:-1]:
                    cursor = cursor[key]  # type: ignore[index,assignment]
                cursor[record_path[-1]] = "continue"  # type: ignore[index]
                errors = validate_workflow_automation(state)
                self.assertTrue(any("unknown value" in error for error in errors), errors)

    def test_unknown_invalidation_trigger_vocabulary_fails_closed(self) -> None:
        for record_path in (
            ("parent_authorizations", "authorization-authoring-001", "invalidation"),
            ("effective_capabilities", "capability-proposal-review-001", "invalidation"),
        ):
            with self.subTest(path=record_path):
                state = valid_automation()
                cursor = state
                for key in record_path:
                    cursor = cursor[key]  # type: ignore[index,assignment]
                cursor.clear()  # type: ignore[union-attr]
                cursor["on_future_event"] = "pause"  # type: ignore[index]
                errors = validate_workflow_automation(state)
                self.assertTrue(any("on_future_event" in error for error in errors), errors)

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

    def test_operation_target_frontier_covers_every_stage_and_public_target(self) -> None:
        self.assertEqual(set(STAGE_TARGET_FRONTIER), {stage.value for stage in WorkflowStage})
        self.assertEqual(set(PUBLIC_TARGET_ORDER), {stage.value for stage in PUBLIC_TARGET_STAGES})
        self.assertEqual(len(PUBLIC_TARGET_ORDER), len(set(PUBLIC_TARGET_ORDER)))

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

    def test_each_capability_kind_has_a_complete_valid_record(self) -> None:
        cases = (
            (
                "proposal-review",
                "authoring",
                "proposal-review",
                {"kind": "singleton"},
                "change-local-review-evidence",
                {
                    "proposal_identity": "sha256:proposal",
                    "standing_gates_identity": "sha256:gates",
                    "review_policy_identity": "sha256:policy",
                    "structured_target_identity": "sha256:target",
                    "review_evidence_roots": ["docs/changes/2026-07-20-example/"],
                },
            ),
            (
                "proposal-correction",
                "authoring",
                "proposal",
                {"kind": "singleton"},
                "proposal-content",
                {
                    "reviewed_proposal_identity": "sha256:proposal",
                    "review_record_identity": "sha256:review",
                    "accepted_finding_set_identity": "sha256:findings",
                    "classifier_policy_identity": "sha256:classifier",
                    "correction_budget_identity": "sha256:budget",
                    "affected_proposal_roots": ["docs/proposals/"],
                },
            ),
            (
                "post-proposal-authoring",
                "authoring",
                "spec",
                {"kind": "singleton"},
                "downstream-authoring-artifacts",
                {
                    "proposal_identity": "sha256:proposal",
                    "approved_proposal_review_identity": "sha256:proposal-review",
                    "closed_review_resolution_identity": "sha256:resolution",
                    "stage_scope_identity": "sha256:stage-scope",
                },
            ),
            (
                "implementation",
                "implementation",
                "implement",
                {"kind": "milestone", "milestone_id": "M1"},
                "production-code",
                {
                    "plan_identity": "sha256:plan",
                    "plan_review_identity": "sha256:plan-review",
                    "test_spec_identity": "sha256:test-spec",
                    "test_spec_review_identity": "sha256:test-spec-review",
                    "milestone_identity": "sha256:M1",
                    "affected_paths_identity": "sha256:paths",
                    "mutation_categories_identity": "sha256:categories",
                    "validation_commands_identity": "sha256:commands",
                },
            ),
            (
                "implementation-correction",
                "implementation",
                "review-resolution",
                {"kind": "singleton"},
                "change-local-evidence",
                {
                    "code_review_identity": "sha256:code-review",
                    "accepted_finding_set_identity": "sha256:findings",
                    "reviewer_classification_identity": "sha256:classification",
                    "affected_paths_identity": "sha256:paths",
                },
            ),
            (
                "verification",
                "verification",
                "verify",
                {"kind": "final"},
                "verification-evidence",
                {
                    "closed_milestones_identity": "sha256:milestones",
                    "final_code_review_identity": "sha256:final-review",
                    "promotion_evidence_identity": "sha256:promotion",
                    "explanation_inputs_identity": "sha256:explanation",
                    "branch_state_identity": "sha256:branch",
                    "verification_commands_identity": "sha256:commands",
                },
            ),
        )
        for kind, authorization_class, stage_name, occurrence, category, basis in cases:
            with self.subTest(kind=kind):
                state = valid_automation()
                parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
                parent["authorization_class"] = authorization_class  # type: ignore[index]
                parent["allowed_capability_kinds"] = [kind]  # type: ignore[index]
                parent["maximum_mutation_categories"] = [category]  # type: ignore[index]
                maximum_stage = (
                    "verify"
                    if authorization_class == "verification"
                    else "code-review"
                    if kind == "implementation-correction"
                    else "implement"
                    if authorization_class == "implementation"
                    else "spec"
                )
                maximum_occurrence = (
                    "final"
                    if authorization_class == "verification"
                    else "milestone"
                    if authorization_class == "implementation"
                    else "singleton"
                )
                parent["maximum_target"] = {  # type: ignore[index]
                    "stage": maximum_stage,
                    "occurrence": {"kind": maximum_occurrence},
                    "bound_at": "2026-07-20T00:00:00Z",
                    "completion": {"target": "reached"},
                }
                if maximum_occurrence == "milestone":
                    parent["maximum_target"]["occurrence"]["milestone_id"] = "M1"  # type: ignore[index]
                    parent["maximum_target"]["plan_identity"] = "sha256:plan"  # type: ignore[index]
                if kind in {"proposal-correction", "implementation-correction"}:
                    parent["correction_budget"] = {"max_cycles": 1}  # type: ignore[index]
                capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
                capability["capability_kind"] = kind  # type: ignore[index]
                capability["stage"] = {"name": stage_name, "occurrence": occurrence}  # type: ignore[index]
                capability["basis"] = basis  # type: ignore[index]
                capability["scope"] = {  # type: ignore[index]
                    "affected_path_roots": ["docs/changes/2026-07-20-example/"],
                    "mutation_categories": [category],
                }
                self.assertEqual(validate_workflow_automation(state), [])

    def test_parent_cannot_allow_cross_risk_capability_kind(self) -> None:
        state = valid_automation()
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["allowed_capability_kinds"] = ["implementation"]  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("crosses parent authorization class" in error for error in errors), errors)

    def test_revoked_parent_cannot_support_active_capability(self) -> None:
        state = valid_automation()
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["revocation"] = {"revoked": True}  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("active parent cannot be revoked" in error for error in errors), errors)
        self.assertTrue(any("parent authorization is revoked" in error for error in errors), errors)

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

    def test_parent_maximum_target_uses_complete_structured_target(self) -> None:
        required_cases = (
            ("milestone", ("occurrence", "milestone_id")),
            ("plan", ("plan_identity",)),
            ("binding-time", ("bound_at",)),
            ("completion", ("completion",)),
        )
        for label, path in required_cases:
            with self.subTest(case=label):
                state = valid_automation()
                parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
                parent["authorization_class"] = "implementation"  # type: ignore[index]
                parent["allowed_capability_kinds"] = ["implementation"]  # type: ignore[index]
                parent["maximum_mutation_categories"] = ["production-code"]  # type: ignore[index]
                parent["maximum_target"] = {  # type: ignore[index]
                    "stage": "implement",
                    "occurrence": {"kind": "milestone", "milestone_id": "M1"},
                    "plan_identity": "sha256:plan",
                    "bound_at": "2026-07-20T00:00:00Z",
                    "completion": {"milestone_state": "review-requested"},
                }
                state["effective_capabilities"] = {}
                cursor = parent["maximum_target"]  # type: ignore[index]
                for key in path[:-1]:
                    cursor = cursor[key]
                del cursor[path[-1]]
                errors = validate_workflow_automation(state)
                self.assertTrue(any("maximum_target" in error for error in errors), errors)

    def test_internal_stage_wrong_occurrence_is_rejected(self) -> None:
        state = valid_automation()
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["allowed_capability_kinds"] = ["proposal-correction"]  # type: ignore[index]
        parent["maximum_mutation_categories"] = ["proposal-content"]  # type: ignore[index]
        parent["correction_budget"] = {"max_cycles": 1}  # type: ignore[index]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["capability_kind"] = "proposal-correction"  # type: ignore[index]
        capability["stage"] = {"name": "proposal", "occurrence": {"kind": "final"}}  # type: ignore[index]
        capability["basis"] = {  # type: ignore[index]
            "reviewed_proposal_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "accepted_finding_set_identity": "sha256:findings",
            "classifier_policy_identity": "sha256:classifier",
            "correction_budget_identity": "sha256:budget",
            "affected_proposal_roots": ["docs/proposals/"],
        }
        capability["scope"] = {  # type: ignore[index]
            "affected_path_roots": ["docs/changes/2026-07-20-example/"],
            "mutation_categories": ["proposal-content"],
        }
        errors = validate_workflow_automation(state)
        self.assertTrue(any("stage.occurrence.kind" in error for error in errors), errors)

    def test_milestone_capability_requires_milestone_identity(self) -> None:
        state = valid_automation()
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["authorization_class"] = "implementation"  # type: ignore[index]
        parent["allowed_capability_kinds"] = ["implementation"]  # type: ignore[index]
        parent["maximum_mutation_categories"] = ["production-code"]  # type: ignore[index]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["capability_kind"] = "implementation"  # type: ignore[index]
        capability["stage"] = {"name": "implement", "occurrence": {"kind": "milestone"}}  # type: ignore[index]
        capability["basis"] = {  # type: ignore[index]
            "plan_identity": "sha256:plan",
            "plan_review_identity": "sha256:plan-review",
            "test_spec_identity": "sha256:test-spec",
            "test_spec_review_identity": "sha256:test-spec-review",
            "milestone_identity": "sha256:M1",
            "affected_paths_identity": "sha256:paths",
            "mutation_categories_identity": "sha256:categories",
            "validation_commands_identity": "sha256:commands",
        }
        capability["scope"] = {  # type: ignore[index]
            "affected_path_roots": ["docs/changes/2026-07-20-example/"],
            "mutation_categories": ["production-code"],
        }
        errors = validate_workflow_automation(state)
        self.assertTrue(any("milestone_id" in error for error in errors), errors)

    def test_null_required_basis_identity_is_rejected(self) -> None:
        state = valid_automation()
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["basis"]["proposal_identity"] = None  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("basis.proposal_identity" in error for error in errors), errors)

    def test_empty_invalidation_behavior_is_rejected(self) -> None:
        state = valid_automation()
        state["parent_authorizations"]["authorization-authoring-001"]["invalidation"] = {}  # type: ignore[index]
        state["effective_capabilities"]["capability-proposal-review-001"]["invalidation"] = {}  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("invalidation" in error for error in errors), errors)

    def test_receipt_incompatible_target_is_rejected(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        receipt["target"]["occurrence"] = {"kind": "milestone", "milestone_id": "M1"}  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("transition_receipts.transition-001.target.occurrence.kind" in error for error in errors), errors)

    def test_receipt_binding_and_evidence_are_validated(self) -> None:
        mutations = (
            ("wrong-run", ("run_id",), "run-other", "run_id"),
            ("wrong-change", ("change_id",), "other-change", "change_id"),
            ("empty-inputs", ("input_identities",), {}, "input_identities"),
            ("empty-postcondition", ("expected_postcondition",), {}, "expected_postcondition"),
            ("wrong-outputs", ("outputs",), {}, "outputs"),
        )
        for label, path, value, expected in mutations:
            with self.subTest(case=label):
                state = valid_automation()
                receipt = add_valid_receipt(state)
                receipt[path[0]] = value
                errors = validate_workflow_automation(state)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_receipt_later_target_allows_current_earlier_stage_capability(self) -> None:
        state = valid_automation()
        state["run"]["target"] = {  # type: ignore[index]
            "stage": "spec",
            "occurrence": {"kind": "singleton"},
            "bound_at": "2026-07-20T00:00:00Z",
            "completion": {"spec": "authored"},
        }
        add_valid_receipt(state)
        self.assertEqual(validate_workflow_automation(state), [])

    def test_capability_operation_cannot_exceed_run_or_parent_target(self) -> None:
        for boundary in ("run", "parent"):
            with self.subTest(boundary=boundary):
                state = valid_automation()
                parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
                parent["allowed_capability_kinds"] = ["post-proposal-authoring"]  # type: ignore[index]
                parent["maximum_mutation_categories"] = ["downstream-authoring-artifacts"]  # type: ignore[index]
                capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
                capability["capability_kind"] = "post-proposal-authoring"  # type: ignore[index]
                capability["stage"] = {"name": "spec", "occurrence": {"kind": "singleton"}}  # type: ignore[index]
                capability["basis"] = {  # type: ignore[index]
                    "proposal_identity": "sha256:proposal",
                    "approved_proposal_review_identity": "sha256:proposal-review",
                    "closed_review_resolution_identity": "sha256:resolution",
                    "stage_scope_identity": "sha256:scope",
                }
                capability["scope"]["mutation_categories"] = ["downstream-authoring-artifacts"]  # type: ignore[index]
                if boundary == "run":
                    parent["maximum_target"] = {  # type: ignore[index]
                        "stage": "spec",
                        "occurrence": {"kind": "singleton"},
                        "bound_at": "2026-07-20T00:00:00Z",
                        "completion": {"spec": "authored"},
                    }
                add_valid_receipt(state)
                errors = validate_workflow_automation(state)
                expected = "run target" if boundary == "run" else "parent maximum target"
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_receipt_target_must_match_run_destination(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        receipt["target"] = {
            "stage": "spec",
            "occurrence": {"kind": "singleton"},
            "bound_at": "2026-07-20T00:00:00Z",
            "completion": {"spec": "authored"},
        }
        errors = validate_workflow_automation(state)
        self.assertTrue(any("must match automation run target" in error for error in errors), errors)

    def test_receipt_rejects_placeholder_postcondition_and_output_evidence(self) -> None:
        cases = (
            ("null-postcondition", "expected_postcondition", {"review_occurrence": None}),
            ("empty-postcondition-value", "expected_postcondition", {"review_occurrence": ""}),
            ("null-output", "outputs", [None]),
            ("empty-output", "outputs", [""]),
        )
        for label, field, value in cases:
            with self.subTest(case=label):
                state = valid_automation()
                receipt = add_valid_receipt(state)
                receipt[field] = value
                errors = validate_workflow_automation(state)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_prepared_receipt_requires_active_capability(self) -> None:
        state = valid_automation()
        add_valid_receipt(state)
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["status"] = "invalidated"  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertIn(
            "workflow.automation.transition_receipts.transition-001.effective_capability_id: capability must be active for prepared receipt",
            errors,
        )

    def test_completed_receipt_accepts_consumed_capability(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        receipt["status"] = "completed"
        receipt["outputs"] = ["sha256:proposal-review"]
        receipt["canonical_sync"] = {"status": "synchronized"}
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["status"] = "consumed"  # type: ignore[index]
        self.assertEqual(validate_workflow_automation(state), [])

    def test_forbidden_live_state_fields_fail(self) -> None:
        state = valid_automation()
        state["next_stage"] = "spec"
        self.assertIn(
            "workflow.automation.next_stage: automation state must not own live workflow state",
            validate_workflow_automation(state),
        )


if __name__ == "__main__":
    unittest.main()
