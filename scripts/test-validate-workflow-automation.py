#!/usr/bin/env python3
"""Unit tests for unified workflow-automation state validation."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import unittest
from pathlib import Path

from validate_workflow_automation import validate_workflow_automation
from validate_workflow_automation import (
    CAPABILITY_STATUS_TRANSITIONS,
    PARENT_STATUS_TRANSITIONS,
    RUN_STATUS_TRANSITIONS,
    validate_cross_spec_disposition_rows,
    validate_repository_cross_spec_dispositions,
    validate_status_transition,
)
from workflow_automation_policy import (
    PUBLIC_TARGET_STAGES,
    STAGE_POLICY_BY_STAGE,
    WorkflowStage,
    target_completion_predicate,
)
from workflow_automation_state import compute_transition_key


ROOT = Path(__file__).resolve().parents[1]


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
                "completion": target_completion_predicate("proposal-review"),
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
                    "completion": target_completion_predicate("proposal-review"),
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
        "expected_postcondition": {
            "completion_rule": "formal review occurrence is recorded",
            "required_evidence": ["proposal-review"],
        },
        "status": "prepared",
        "retry_policy": "reconcile-only",
        "outputs": [],
        "canonical_sync": {"status": "pending"},
    }
    receipt["transition_key"] = compute_transition_key(receipt)
    state["transition_receipts"] = {"transition-001": receipt}
    return receipt


def add_completed_proposal_review(
    state: dict[str, object],
    review_result: dict[str, object],
) -> dict[str, object]:
    receipt = add_valid_receipt(state)
    evidence = {
        "path": (
            "docs/changes/2026-07-20-example/reviews/"
            "proposal-review-r1.md"
        ),
        "identity": review_result["review_record_identity"],
    }
    receipt["status"] = "completed"
    receipt["outputs"] = [copy.deepcopy(evidence)]
    receipt["canonical_sync"] = {
        "status": "synchronized",
        "evidence": {"proposal-review": copy.deepcopy(evidence)},
        "observed_identities": {
            "proposal-review": review_result["review_record_identity"],
        },
    }
    receipt["proposal_review_route"] = {
        "review_id": review_result["review_id"],
        "outcome": review_result["outcome"],
        "target": copy.deepcopy(receipt["target"]),
        "reviewed_artifact_identity": review_result[
            "reviewed_artifact_identity"
        ],
        "review_record_identity": review_result["review_record_identity"],
        "routing_action": review_result["routing_action"],
        "correction_capability_id": review_result.get(
            "correction_capability_id"
        ),
    }
    receipt["proposal_review_evidence"] = {
        "review_id": review_result["review_id"],
        "outcome": review_result["outcome"],
        "reviewed_artifact_identity": review_result[
            "reviewed_artifact_identity"
        ],
        "review_record_identity": review_result["review_record_identity"],
    }
    state["effective_capabilities"]["capability-proposal-review-001"][  # type: ignore[index]
        "status"
    ] = "consumed"
    review_result["source_transition_id"] = "transition-001"
    state["latest_review_result"] = review_result
    return receipt


def add_historical_completed_proposal_review(
    state: dict[str, object],
) -> dict[str, object]:
    """Add a second valid completed review without changing the latest result."""

    capabilities = state["effective_capabilities"]  # type: ignore[index]
    original_capability = capabilities["capability-proposal-review-001"]  # type: ignore[index]
    historical_capability = copy.deepcopy(original_capability)
    historical_capability["capability_id"] = "capability-proposal-review-000"  # type: ignore[index]
    historical_capability["status"] = "consumed"  # type: ignore[index]
    capabilities["capability-proposal-review-000"] = historical_capability  # type: ignore[index]

    receipts = state["transition_receipts"]  # type: ignore[index]
    latest_receipt = receipts["transition-001"]  # type: ignore[index]
    historical_receipt = copy.deepcopy(latest_receipt)
    historical_receipt["transition_id"] = "transition-000"  # type: ignore[index]
    historical_receipt[
        "effective_capability_id"
    ] = "capability-proposal-review-000"  # type: ignore[index]
    historical_receipt["proposal_review_route"].update(  # type: ignore[index,union-attr]
        {
            "review_id": "proposal-review-r0",
            "review_record_identity": "sha256:review-r0",
        }
    )
    historical_receipt["proposal_review_evidence"].update(  # type: ignore[index,union-attr]
        {
            "review_id": "proposal-review-r0",
            "review_record_identity": "sha256:review-r0",
        }
    )
    historical_receipt["outputs"][0][  # type: ignore[index]
        "identity"
    ] = "sha256:review-r0"
    historical_receipt["canonical_sync"]["evidence"]["proposal-review"][  # type: ignore[index]
        "identity"
    ] = "sha256:review-r0"
    historical_receipt["canonical_sync"]["observed_identities"][  # type: ignore[index]
        "proposal-review"
    ] = "sha256:review-r0"
    historical_receipt["transition_key"] = compute_transition_key(  # type: ignore[index]
        historical_receipt
    )
    receipts["transition-000"] = historical_receipt  # type: ignore[index]
    return historical_receipt


def add_proposal_correction_capability(
    state: dict[str, object],
    *,
    capability_id: str,
    reviewed_proposal_identity: str,
    review_record_identity: str,
    status: str = "consumed",
) -> dict[str, object]:
    """Add a structurally valid correction capability for route-history tests."""

    budget = {
        "Review-fix cycle count": 1,
        "Findings auto-applied this cycle": 1,
        "Files changed this cycle": 1,
        "Files changed this invocation": 1,
    }
    accepted = ["BRF-1"]
    classifications = {"BRF-1": "mechanical"}
    correction_plans = {
        "BRF-1": {
            "classification": "mechanical",
            "rationale": "fixture rationale",
            "recipe": "Append one newline to the reviewed proposal.",
            "validation_rule": "proposal-exact-append",
        }
    }

    def structured(value: object) -> str:
        payload = json.dumps(
            value, sort_keys=True, separators=(",", ":")
        ).encode()
        return "sha256:" + hashlib.sha256(payload).hexdigest()

    parent = state["parent_authorizations"][  # type: ignore[index]
        "authorization-authoring-001"
    ]
    parent["allowed_capability_kinds"] = [  # type: ignore[index]
        "proposal-review",
        "proposal-correction",
    ]
    parent["maximum_path_roots"] = [  # type: ignore[index]
        "docs/changes/2026-07-20-example/",
        "docs/proposals/",
    ]
    parent["maximum_mutation_categories"] = [  # type: ignore[index]
        "change-local-review-evidence",
        "proposal-content",
    ]
    parent["correction_budget"] = copy.deepcopy(budget)  # type: ignore[index]

    capability = {
        "capability_id": capability_id,
        "capability_kind": "proposal-correction",
        "parent_authorization_id": "authorization-authoring-001",
        "policy_version": 1,
        "change_id": "2026-07-20-example",
        "stage": {
            "name": "proposal",
            "occurrence": {"kind": "singleton"},
        },
        "basis": {
            "reviewed_proposal_identity": reviewed_proposal_identity,
            "review_record_identity": review_record_identity,
            "accepted_finding_set_identity": structured(accepted),
            "classifier_policy_identity": structured(correction_plans),
            "correction_budget_identity": structured(budget),
            "affected_proposal_roots": ["docs/proposals/"],
        },
        "scope": {
            "affected_path_roots": ["docs/proposals/"],
            "mutation_categories": ["proposal-content"],
            "correction_budget": copy.deepcopy(budget),
            "correction_budget_identity": structured(budget),
            "review_record_path": (
                "docs/changes/2026-07-20-example/reviews/"
                "proposal-review-r0.md"
            ),
            "review_resolution_path": (
                "docs/changes/2026-07-20-example/review-resolution.md"
            ),
            "accepted_finding_ids": accepted,
            "finding_classifications": classifications,
            "correction_plans": correction_plans,
            "proposal_review_basis": {
                "standing_gates_identity": "sha256:gates",
                "review_policy_identity": "sha256:policy",
                "structured_target_identity": "sha256:target",
                "review_evidence_roots": [
                    "docs/changes/2026-07-20-example/"
                ],
            },
        },
        "derived_at": "2026-07-20T00:02:00Z",
        "status": status,
        "invalidation": {"on_parent_revocation": "invalidate"},
    }
    state["effective_capabilities"][capability_id] = capability  # type: ignore[index]
    return capability


def set_policy_postcondition(receipt: dict[str, object], stage_name: str) -> None:
    policy = STAGE_POLICY_BY_STAGE[stage_name]
    receipt["expected_postcondition"] = {
        "completion_rule": policy.completion_rule,
        "required_evidence": sorted(policy.completion_evidence),
    }


def add_valid_migration_receipt(state: dict[str, object]) -> dict[str, object]:
    receipt = {
        "migration_id": "migration-001",
        "source_mechanism": "implementation-through-verify",
        "source_record_identity": "sha256:legacy",
        "migrated_at": "2026-07-22T00:00:00Z",
        "unified_run_id": "run-001",
        "projection_result": "equivalent",
        "legacy_read_only": True,
    }
    state["migration_receipts"] = {"migration-001": receipt}
    return receipt


def configure_post_proposal_transition(
    state: dict[str, object],
    *,
    stage_name: str,
    target_stage: str,
) -> dict[str, object]:
    target = {
        "stage": target_stage,
        "occurrence": {"kind": "singleton"},
        "bound_at": "2026-07-20T00:00:00Z",
        "completion": target_completion_predicate(target_stage),
    }
    state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
    parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
    parent["maximum_target"] = copy.deepcopy(target)  # type: ignore[index]
    parent["allowed_capability_kinds"] = ["post-proposal-authoring"]  # type: ignore[index]
    stage_mutation_category = sorted(
        category.value
        for category in STAGE_POLICY_BY_STAGE[stage_name].permitted_mutation_category
    )[0]
    parent["maximum_mutation_categories"] = [stage_mutation_category]  # type: ignore[index]
    capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
    capability["capability_kind"] = "post-proposal-authoring"  # type: ignore[index]
    capability["stage"] = {"name": stage_name, "occurrence": {"kind": "singleton"}}  # type: ignore[index]
    capability["basis"] = {  # type: ignore[index]
        "proposal_identity": "sha256:proposal",
        "approved_proposal_review_identity": "sha256:proposal-review",
        "closed_review_resolution_identity": "sha256:resolution",
        "stage_scope_identity": "sha256:scope",
    }
    capability["scope"]["mutation_categories"] = [stage_mutation_category]  # type: ignore[index]
    receipt = add_valid_receipt(state)
    receipt["retry_policy"] = STAGE_POLICY_BY_STAGE[stage_name].retry_policy.value
    set_policy_postcondition(receipt, stage_name)
    return receipt


def configure_next_milestone_transition(
    state: dict[str, object],
    *,
    milestone_id: str,
) -> dict[str, object]:
    target = {
        "stage": "verify",
        "occurrence": {"kind": "final"},
        "bound_at": "2026-07-20T00:00:00Z",
        "completion": target_completion_predicate("verify"),
    }
    state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
    parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
    parent["authorization_class"] = "implementation"  # type: ignore[index]
    parent["maximum_target"] = copy.deepcopy(target)  # type: ignore[index]
    parent["allowed_capability_kinds"] = ["implementation"]  # type: ignore[index]
    parent["maximum_mutation_categories"] = ["production-code"]  # type: ignore[index]
    capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
    capability["capability_kind"] = "implementation"  # type: ignore[index]
    capability["stage"] = {  # type: ignore[index]
        "name": "implement",
        "occurrence": {"kind": "milestone", "milestone_id": milestone_id},
    }
    capability["basis"] = {  # type: ignore[index]
        "plan_identity": "sha256:plan",
        "plan_review_identity": "sha256:plan-review",
        "test_spec_identity": "sha256:test-spec",
        "test_spec_review_identity": "sha256:test-spec-review",
        "milestone_identity": f"sha256:{milestone_id}",
        "affected_paths_identity": "sha256:paths",
        "mutation_categories_identity": "sha256:categories",
        "validation_commands_identity": "sha256:commands",
    }
    capability["scope"]["mutation_categories"] = ["production-code"]  # type: ignore[index]
    receipt = add_valid_receipt(state)
    receipt["retry_policy"] = STAGE_POLICY_BY_STAGE[
        WorkflowStage.IMPLEMENT.value
    ].retry_policy.value
    set_policy_postcondition(receipt, WorkflowStage.IMPLEMENT.value)
    return receipt


class WorkflowAutomationVocabularyTests(unittest.TestCase):
    def test_repository_cross_spec_disposition_contract_is_consistent(self) -> None:
        self.assertEqual(validate_repository_cross_spec_dispositions(ROOT), [])

    def test_cross_spec_disposition_rows_fail_closed_before_consistency(self) -> None:
        rows = [
            {
                "source": "specs/legacy.md",
                "selector": "R1",
                "disposition": "preserved-rebound",
                "new_subject": "unified implementation capability",
            },
            {
                "source": "specs/legacy.md",
                "selector": "R2",
                "disposition": "superseded",
                "new_subject": "BRF-R001",
            },
        ]
        required = {
            ("specs/legacy.md", "R1"),
            ("specs/legacy.md", "R2"),
        }
        self.assertEqual(
            validate_cross_spec_disposition_rows(
                rows,
                required_selectors=required,
            ),
            [],
        )

        unknown = copy.deepcopy(rows)
        unknown[0]["disposition"] = "keep"
        errors = validate_cross_spec_disposition_rows(
            unknown,
            required_selectors=required,
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("unknown disposition", errors[0])

        duplicate = rows + [copy.deepcopy(rows[0])]
        errors = validate_cross_spec_disposition_rows(
            duplicate,
            required_selectors=required,
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate source selector", errors[0])

        missing = validate_cross_spec_disposition_rows(
            rows[:1],
            required_selectors=required,
        )
        self.assertTrue(any("missing disposition" in error for error in missing))

        retired = copy.deepcopy(rows)
        retired[0]["new_subject"] = "implementation-through-verify profile"
        errors = validate_cross_spec_disposition_rows(
            retired,
            required_selectors=required,
        )
        self.assertTrue(any("retired writer" in error for error in errors))

    def test_proposal_correction_unknown_value_classification_fails_closed(
        self,
    ) -> None:
        state = valid_automation()
        capability = state["effective_capabilities"][
            "capability-proposal-review-001"
        ]
        accepted = ["BRF-1"]
        classifications = {"BRF-1": "future-classification"}
        correction_plans = {
            "BRF-1": {
                "classification": "future-classification",
                "rationale": "fixture rationale",
                "recipe": "Append one newline to the reviewed proposal.",
                "validation_rule": "proposal-exact-append",
            }
        }
        budget = {
            "Review-fix cycle count": 1,
            "Findings auto-applied this cycle": 1,
            "Files changed this cycle": 1,
            "Files changed this invocation": 1,
        }
        structured = lambda value: "sha256:" + hashlib.sha256(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        capability["capability_kind"] = "proposal-correction"
        capability["stage"] = {
            "name": "proposal",
            "occurrence": {"kind": "singleton"},
        }
        capability["basis"] = {
            "reviewed_proposal_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "accepted_finding_set_identity": structured(accepted),
            "classifier_policy_identity": structured(correction_plans),
            "correction_budget_identity": structured(budget),
            "affected_proposal_roots": ["docs/proposals/"],
        }
        capability["scope"] = {
            "affected_path_roots": ["docs/proposals/"],
            "mutation_categories": ["proposal-content"],
            "correction_budget": budget,
            "correction_budget_identity": structured(budget),
            "review_record_path": "docs/changes/example/reviews/proposal-review-r1.md",
            "review_resolution_path": "docs/changes/example/review-resolution.md",
            "accepted_finding_ids": accepted,
            "finding_classifications": classifications,
            "correction_plans": correction_plans,
            "proposal_review_basis": {
                "standing_gates_identity": "sha256:gates",
                "review_policy_identity": "sha256:policy",
                "structured_target_identity": "sha256:target",
                "review_evidence_roots": ["docs/changes/example/"],
            },
        }

        errors = validate_workflow_automation(state)

        self.assertTrue(
            any("unsupported classification" in error for error in errors),
            errors,
        )

        classifications["BRF-1"] = "mechanical"
        correction_plans["BRF-1"]["classification"] = "mechanical"
        correction_plans["BRF-1"]["validation_rule"] = "future-validation"
        capability["basis"]["classifier_policy_identity"] = structured(
            correction_plans
        )
        errors = validate_workflow_automation(state)
        self.assertTrue(
            any("unsupported validation rule" in error for error in errors),
            errors,
        )

    def test_proposal_correction_budget_content_must_match_identity(self) -> None:
        state = valid_automation()
        capability = state["effective_capabilities"]["capability-proposal-review-001"]
        capability["capability_kind"] = "proposal-correction"
        capability["stage"] = {
            "name": "proposal",
            "occurrence": {"kind": "singleton"},
        }
        budget = {
            "Review-fix cycle count": 1,
            "Findings auto-applied this cycle": 1,
            "Files changed this cycle": 1,
            "Files changed this invocation": 1,
        }
        budget_identity = "sha256:" + hashlib.sha256(
            json.dumps(budget, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        capability["basis"] = {
            "reviewed_proposal_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "accepted_finding_set_identity": "sha256:findings",
            "classifier_policy_identity": "sha256:classifier",
            "correction_budget_identity": budget_identity,
            "affected_proposal_roots": ["docs/proposals/"],
        }
        capability["scope"] = {
            "affected_path_roots": ["docs/proposals/"],
            "mutation_categories": ["proposal-content"],
            "correction_budget": copy.deepcopy(budget),
            "correction_budget_identity": budget_identity,
        }
        capability["scope"]["correction_budget"]["Review-fix cycle count"] = 2

        errors = validate_workflow_automation(state)

        self.assertTrue(
            any("correction_budget_identity: does not match" in error for error in errors),
            errors,
        )

    def test_valid_unified_state_passes(self) -> None:
        self.assertEqual(validate_workflow_automation(valid_automation()), [])

    def test_target_completion_must_match_immutable_policy_for_every_public_stage(self) -> None:
        for stage in PUBLIC_TARGET_STAGES:
            with self.subTest(stage=stage.value):
                state = valid_automation()
                occurrence = {
                    "kind": STAGE_POLICY_BY_STAGE[stage.value].occurrence_rule.value
                }
                target = {
                    "stage": stage.value,
                    "occurrence": occurrence,
                    "bound_at": "2026-07-20T00:00:00Z",
                    "completion": {"rule": "attacker-selected"},
                }
                if occurrence["kind"] == "milestone":
                    occurrence["milestone_id"] = "M1"
                    target["plan_identity"] = "sha256:plan"
                state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
                state["parent_authorizations"]["authorization-authoring-001"][  # type: ignore[index]
                    "maximum_target"
                ] = copy.deepcopy(target)

                errors = validate_workflow_automation(state)

                self.assertTrue(
                    any("completion: must match immutable stage policy" in error for error in errors),
                    errors,
                )

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
        add_completed_proposal_review(state, {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        })
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

    def test_proposal_review_result_requires_concrete_consistent_projection(
        self,
    ) -> None:
        invalid_results = (
            {
                "review_id": "",
                "reviewed_artifact_identity": "",
                "review_record_identity": "",
                "outcome": "approved",
                "occurrence_recorded": True,
                "clean_gate": "satisfied",
                "routing_action": "stop-at-target",
            },
            {
                "review_id": "proposal-review-r1",
                "reviewed_artifact_identity": "sha256:proposal",
                "review_record_identity": "sha256:review",
                "outcome": "blocked",
                "occurrence_recorded": True,
                "clean_gate": "satisfied",
                "routing_action": "continue",
            },
            {
                "review_id": "proposal-review-r1",
                "reviewed_artifact_identity": "sha256:proposal",
                "review_record_identity": "sha256:review",
                "outcome": "changes-requested",
                "occurrence_recorded": True,
                "clean_gate": "not-satisfied",
                "routing_action": "pause",
            },
        )
        for review_result in invalid_results:
            with self.subTest(review_result=review_result):
                state = valid_automation()
                state["latest_review_result"] = review_result
                errors = validate_workflow_automation(state)
                self.assertTrue(errors)
                self.assertTrue(
                    any("latest_review_result" in error for error in errors),
                    errors,
                )

    def test_completed_proposal_review_requires_route_linked_latest_occurrence(
        self,
    ) -> None:
        state = valid_automation()
        review_result = {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        }
        add_completed_proposal_review(state, review_result)

        missing_latest = copy.deepcopy(state)
        missing_latest.pop("latest_review_result")
        errors = validate_workflow_automation(missing_latest)
        self.assertTrue(
            any(
                "completed proposal-review transition requires"
                in error
                for error in errors
            ),
            errors,
        )

        missing_route = copy.deepcopy(state)
        missing_route["transition_receipts"]["transition-001"].pop(
            "proposal_review_route"
        )
        errors = validate_workflow_automation(missing_route)
        self.assertTrue(
            any(
                "completed proposal-review transition requires"
                in error
                for error in errors
            ),
            errors,
        )

    def test_every_completed_proposal_review_receipt_has_a_canonical_route(
        self,
    ) -> None:
        state = valid_automation()
        add_completed_proposal_review(state, {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        })
        state["run"]["status"] = "completed"  # type: ignore[index]
        historical_receipt = add_historical_completed_proposal_review(state)
        self.assertEqual(validate_workflow_automation(state), [])

        cases = (
            (
                "empty-route",
                lambda receipt: receipt.__setitem__(
                    "proposal_review_route", {}
                ),
                "immutable",
            ),
            (
                "wrong-review-id",
                lambda receipt: receipt["proposal_review_route"].__setitem__(  # type: ignore[index]
                    "review_id", "proposal-review-forged"
                ),
                "stage-native completion evidence",
            ),
            (
                "wrong-target",
                lambda receipt: receipt["proposal_review_route"].__setitem__(  # type: ignore[index]
                    "target",
                    {
                        "stage": "spec",
                        "occurrence": {"kind": "singleton"},
                        "bound_at": "2026-07-20T00:00:00Z",
                        "completion": target_completion_predicate("spec"),
                    },
                ),
                "stage-native completion evidence",
            ),
            (
                "wrong-proposal-identity",
                lambda receipt: receipt["proposal_review_route"].__setitem__(  # type: ignore[index]
                    "reviewed_artifact_identity", "sha256:other-proposal"
                ),
                "stage-native completion evidence",
            ),
            (
                "wrong-known-outcome",
                lambda receipt: receipt["proposal_review_route"].update(  # type: ignore[index]
                    {
                        "outcome": "changes-requested",
                        "routing_action": "stop-at-target",
                    }
                ),
                "stage-native completion evidence",
            ),
            (
                "wrong-output-identity",
                lambda receipt: receipt["outputs"][0].__setitem__(  # type: ignore[index]
                    "identity", "sha256:other-review"
                ),
                "output evidence",
            ),
            (
                "wrong-review-identity",
                lambda receipt: receipt["proposal_review_route"].__setitem__(  # type: ignore[index]
                    "review_record_identity", "sha256:other-review"
                ),
                "stage-native completion evidence",
            ),
        )
        for label, mutate, expected in cases:
            with self.subTest(case=label):
                candidate = copy.deepcopy(state)
                receipt = candidate["transition_receipts"]["transition-000"]  # type: ignore[index]
                mutate(receipt)
                errors = validate_workflow_automation(candidate)
                self.assertTrue(errors)
                self.assertTrue(
                    any(expected in error for error in errors),
                    errors,
                )

        self.assertEqual(
            historical_receipt["proposal_review_route"]["review_id"],  # type: ignore[index]
            "proposal-review-r0",
        )

    def test_historical_route_rejects_every_alternative_known_outcome(
        self,
    ) -> None:
        state = valid_automation()
        add_completed_proposal_review(state, {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        })
        state["run"]["status"] = "completed"  # type: ignore[index]
        add_historical_completed_proposal_review(state)

        for outcome, routing_action in (
            ("changes-requested", "stop-at-target"),
            ("blocked", "pause"),
            ("inconclusive", "pause"),
        ):
            with self.subTest(outcome=outcome):
                candidate = copy.deepcopy(state)
                route = candidate["transition_receipts"]["transition-000"][  # type: ignore[index]
                    "proposal_review_route"
                ]
                route["outcome"] = outcome
                route["routing_action"] = routing_action
                errors = validate_workflow_automation(candidate)
                self.assertTrue(
                    any(
                        "stage-native completion evidence" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_latest_route_cannot_rewrite_stage_native_review_facts(
        self,
    ) -> None:
        state = valid_automation()
        add_completed_proposal_review(state, {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        })
        state["run"]["status"] = "completed"  # type: ignore[index]

        forged_id = copy.deepcopy(state)
        forged_id["transition_receipts"]["transition-001"][  # type: ignore[index]
            "proposal_review_route"
        ]["review_id"] = "proposal-review-forged"
        forged_id["latest_review_result"][
            "review_id"
        ] = "proposal-review-forged"
        errors = validate_workflow_automation(forged_id)
        self.assertTrue(
            any("stage-native completion evidence" in error for error in errors),
            errors,
        )

        forged_outcome = copy.deepcopy(state)
        forged_outcome["transition_receipts"]["transition-001"][  # type: ignore[index]
            "proposal_review_route"
        ]["outcome"] = "changes-requested"
        forged_outcome["latest_review_result"].update(  # type: ignore[index,union-attr]
            {
                "outcome": "changes-requested",
                "clean_gate": "not-satisfied",
            }
        )
        errors = validate_workflow_automation(forged_outcome)
        self.assertTrue(
            any("stage-native completion evidence" in error for error in errors),
            errors,
        )

    def test_completed_proposal_review_requires_stage_native_evidence(
        self,
    ) -> None:
        state = valid_automation()
        add_completed_proposal_review(state, {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        })
        state["run"]["status"] = "completed"  # type: ignore[index]
        state["transition_receipts"]["transition-001"].pop(  # type: ignore[index]
            "proposal_review_evidence"
        )
        errors = validate_workflow_automation(state)
        self.assertTrue(
            any("stage-native completion evidence" in error for error in errors),
            errors,
        )

    def test_historical_proposal_review_route_vocabulary_fails_closed(
        self,
    ) -> None:
        state = valid_automation()
        add_completed_proposal_review(state, {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        })
        state["run"]["status"] = "completed"  # type: ignore[index]
        add_historical_completed_proposal_review(state)
        for field, value in (
            ("outcome", "unknown-outcome"),
            ("routing_action", "unknown-action"),
        ):
            with self.subTest(field=field):
                candidate = copy.deepcopy(state)
                candidate["transition_receipts"]["transition-000"][  # type: ignore[index]
                    "proposal_review_route"
                ][field] = value
                errors = validate_workflow_automation(candidate)
                self.assertTrue(errors)
                self.assertIn(
                    f"proposal_review_route.{field}",
                    errors[0],
                )
                self.assertIn("unknown value", errors[0])

        unknown_evidence = copy.deepcopy(state)
        unknown_evidence["transition_receipts"]["transition-000"][  # type: ignore[index]
            "proposal_review_evidence"
        ]["outcome"] = "unknown-evidence-outcome"
        errors = validate_workflow_automation(unknown_evidence)
        self.assertTrue(errors)
        self.assertIn(
            "proposal_review_evidence.outcome",
            errors[0],
        )
        self.assertIn("unknown value", errors[0])

    def test_historical_correction_route_retains_its_original_capability(
        self,
    ) -> None:
        state = valid_automation()
        target = {
            "stage": "spec",
            "occurrence": {"kind": "singleton"},
            "bound_at": "2026-07-20T00:00:00Z",
            "completion": target_completion_predicate("spec"),
        }
        state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
        state["parent_authorizations"]["authorization-authoring-001"][  # type: ignore[index]
            "maximum_target"
        ] = copy.deepcopy(target)
        add_completed_proposal_review(state, {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "continue",
        })
        historical_receipt = add_historical_completed_proposal_review(state)
        correction_id = "capability-proposal-correction-000"
        add_proposal_correction_capability(
            state,
            capability_id=correction_id,
            reviewed_proposal_identity="sha256:proposal",
            review_record_identity="sha256:review-r0",
        )
        historical_receipt["proposal_review_route"].update(  # type: ignore[index,union-attr]
            {
                "outcome": "changes-requested",
                "routing_action": "correction-loop",
                "correction_capability_id": correction_id,
            }
        )
        historical_receipt["proposal_review_evidence"][  # type: ignore[index]
            "outcome"
        ] = "changes-requested"
        self.assertEqual(validate_workflow_automation(state), [])

        missing = copy.deepcopy(state)
        missing["effective_capabilities"].pop(correction_id)  # type: ignore[index]
        errors = validate_workflow_automation(missing)
        self.assertTrue(
            any("correction capability does not exist" in error for error in errors),
            errors,
        )

        mismatched = copy.deepcopy(state)
        mismatched["effective_capabilities"][correction_id]["basis"][  # type: ignore[index]
            "review_record_identity"
        ] = "sha256:other-review"
        errors = validate_workflow_automation(mismatched)
        self.assertTrue(
            any(
                "correction capability does not match review basis"
                in error
                for error in errors
            ),
            errors,
        )

        invalidated = copy.deepcopy(state)
        invalidated["effective_capabilities"][correction_id][  # type: ignore[index]
            "status"
        ] = "invalidated"
        self.assertEqual(validate_workflow_automation(invalidated), [])

    def test_cancelled_run_preserves_valid_proposal_review_result_and_authority_shutdown(
        self,
    ) -> None:
        state = valid_automation()
        review_result = {
            "review_id": "proposal-review-r1",
            "reviewed_artifact_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "outcome": "approved",
            "occurrence_recorded": True,
            "clean_gate": "satisfied",
            "routing_action": "stop-at-target",
        }
        add_completed_proposal_review(state, review_result)
        state["run"]["status"] = "cancelled"
        state["run"]["stop_reason"] = "run-cancelled"
        state["parent_authorizations"]["authorization-authoring-001"][
            "status"
        ] = "revoked"
        state["parent_authorizations"]["authorization-authoring-001"][
            "revocation"
        ] = {
            "revoked": True,
            "revoked_by": "user",
            "revoked_at": "2026-07-22T00:00:00Z",
            "reason": "run-cancelled",
        }
        state["cancellation"] = {
            "cancelled_by": "user",
            "cancelled_at": "2026-07-22T00:00:00Z",
            "reason": "run-cancelled",
        }
        self.assertEqual(validate_workflow_automation(state), [])

        cases = (
            ("missing-cancellation", lambda candidate: candidate.pop("cancellation")),
            (
                "active-parent",
                lambda candidate: candidate["parent_authorizations"][
                    "authorization-authoring-001"
                ].__setitem__("status", "active"),
            ),
            (
                "pause-reason",
                lambda candidate: candidate["run"].__setitem__(
                    "pause_reason", "stale-pause"
                ),
            ),
        )
        for label, mutate in cases:
            with self.subTest(case=label):
                candidate = copy.deepcopy(state)
                mutate(candidate)
                self.assertTrue(validate_workflow_automation(candidate))

        active_correction = copy.deepcopy(state)
        correction = add_proposal_correction_capability(
            active_correction,
            capability_id="capability-proposal-correction-001",
            reviewed_proposal_identity="sha256:proposal",
            review_record_identity="sha256:review",
            status="active",
        )
        errors = validate_workflow_automation(active_correction)
        self.assertTrue(
            any(
                "cancelled run cannot retain active capability" in error
                for error in errors
            ),
            errors,
        )
        correction["status"] = "invalidated"
        self.assertEqual(validate_workflow_automation(active_correction), [])

    def test_proposal_review_result_requires_exact_run_pause_projection(
        self,
    ) -> None:
        cases = (
            (
                "proposal-review",
                "approved",
                "satisfied",
                "stop-at-target",
                "completed",
                None,
            ),
            (
                "proposal-review",
                "changes-requested",
                "not-satisfied",
                "stop-at-target",
                "completed",
                None,
            ),
            ("spec", "approved", "satisfied", "continue", "active", None),
            (
                "spec",
                "changes-requested",
                "not-satisfied",
                "pause",
                "paused",
                "proposal-correction-authorization-required",
            ),
            (
                "spec",
                "blocked",
                "not-satisfied",
                "pause",
                "paused",
                "proposal-review-blocked",
            ),
            (
                "spec",
                "inconclusive",
                "not-satisfied",
                "pause",
                "paused",
                "proposal-review-inconclusive",
            ),
        )
        for (
            target_stage,
            outcome,
            gate,
            route,
            run_status,
            expected_pause_reason,
        ) in cases:
            with self.subTest(target=target_stage, outcome=outcome):
                state = valid_automation()
                target = {
                    "stage": target_stage,
                    "occurrence": {"kind": "singleton"},
                    "bound_at": "2026-07-20T00:00:00Z",
                    "completion": target_completion_predicate(target_stage),
                }
                state["run"]["target"] = copy.deepcopy(target)
                state["run"]["status"] = run_status
                state["run"]["pause_reason"] = "wrong-pause-reason"
                state["parent_authorizations"][
                    "authorization-authoring-001"
                ]["maximum_target"] = copy.deepcopy(target)
                review_result = {
                    "review_id": "proposal-review-r1",
                    "reviewed_artifact_identity": "sha256:proposal",
                    "review_record_identity": "sha256:review",
                    "outcome": outcome,
                    "occurrence_recorded": True,
                    "clean_gate": gate,
                    "routing_action": route,
                }
                if expected_pause_reason is not None:
                    review_result["pause_reason"] = expected_pause_reason
                add_completed_proposal_review(state, review_result)

                errors = validate_workflow_automation(state)

                self.assertTrue(
                    any("run.pause_reason" in error for error in errors),
                    errors,
                )

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

    def test_transition_policy_covers_every_stage_without_validator_local_policy(self) -> None:
        self.assertEqual(set(STAGE_POLICY_BY_STAGE), {stage.value for stage in WorkflowStage})

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

    def test_capability_scope_must_be_subset_of_stage_policy(self) -> None:
        state = valid_automation()
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["maximum_mutation_categories"].append("proposal-content")  # type: ignore[index]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["scope"]["mutation_categories"] = ["proposal-content"]  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertIn(
            "workflow.automation.effective_capabilities.capability-proposal-review-001."
            "scope.mutation_categories: exceeds proposal-review stage policy",
            errors,
        )

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
                    "completion": target_completion_predicate(maximum_stage),
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
                if kind in {"proposal-correction", "implementation-correction"}:
                    budget_identity = "sha256:" + hashlib.sha256(
                        json.dumps(
                            {"max_cycles": 1},
                            sort_keys=True,
                            separators=(",", ":"),
                        ).encode()
                    ).hexdigest()
                    capability["basis"]["correction_budget_identity"] = budget_identity  # type: ignore[index]
                    capability["scope"].update(  # type: ignore[index]
                        {
                            "correction_budget": {"max_cycles": 1},
                            "correction_budget_identity": budget_identity,
                        }
                    )
                if kind == "proposal-correction":
                    accepted = ["BRF-1"]
                    classifications = {"BRF-1": "mechanical"}
                    correction_plans = {
                        "BRF-1": {
                            "classification": "mechanical",
                            "rationale": "fixture rationale",
                            "recipe": "Append one newline to the reviewed proposal.",
                            "validation_rule": "proposal-exact-append",
                        }
                    }
                    budget = {
                        "Review-fix cycle count": 1,
                        "Findings auto-applied this cycle": 1,
                        "Files changed this cycle": 1,
                        "Files changed this invocation": 1,
                    }
                    structured = lambda value: "sha256:" + hashlib.sha256(
                        json.dumps(
                            value, sort_keys=True, separators=(",", ":")
                        ).encode()
                    ).hexdigest()
                    parent["correction_budget"] = copy.deepcopy(budget)  # type: ignore[index]
                    capability["basis"].update(  # type: ignore[index]
                        {
                            "accepted_finding_set_identity": structured(accepted),
                            "classifier_policy_identity": structured(correction_plans),
                            "correction_budget_identity": structured(budget),
                        }
                    )
                    capability["scope"].update(  # type: ignore[index]
                        {
                            "correction_budget": budget,
                            "correction_budget_identity": structured(budget),
                            "review_record_path": "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md",
                            "review_resolution_path": "docs/changes/2026-07-20-example/review-resolution.md",
                            "accepted_finding_ids": accepted,
                            "finding_classifications": classifications,
                            "correction_plans": correction_plans,
                            "proposal_review_basis": {
                                "standing_gates_identity": "sha256:gates",
                                "review_policy_identity": "sha256:policy",
                                "structured_target_identity": "sha256:target",
                                "review_evidence_roots": [
                                    "docs/changes/2026-07-20-example/"
                                ],
                            },
                        }
                    )
                if kind == "implementation-correction":
                    accepted = ["BRF-M5-CR1"]
                    recipes = {
                        "BRF-M5-CR1": {
                            "auto_fix_class": "mechanical",
                            "auto_fix_kind": "exact-approved-rename",
                            "affected_paths": ["scripts/example.py"],
                            "deterministic_authority": {
                                "operation": "exact-text-replace",
                                "path": "scripts/example.py",
                                "old": "old_name",
                                "new": "new_name",
                                "expected_replacements": 1,
                            },
                            "required_validation": {
                                "operation": "sha256",
                                "path": "scripts/example.py",
                                "identity": "sha256:corrected",
                            },
                        }
                    }
                    structured = lambda value: "sha256:" + hashlib.sha256(
                        json.dumps(
                            value, sort_keys=True, separators=(",", ":")
                        ).encode()
                    ).hexdigest()
                    capability["basis"].update(  # type: ignore[index]
                        {
                            "accepted_finding_set_identity": structured(accepted),
                            "reviewer_classification_identity": structured(recipes),
                            "affected_paths_identity": structured(
                                ["scripts/example.py"]
                            ),
                        }
                    )
                    capability["scope"].update(  # type: ignore[index]
                        {
                            "review_record_path": "docs/changes/2026-07-20-example/reviews/code-review-m2-r1.md",
                            "review_resolution_path": "docs/changes/2026-07-20-example/review-resolution.md",
                            "review_log_path": "docs/changes/2026-07-20-example/review-log.md",
                            "accepted_finding_ids": accepted,
                            "reviewer_recipes": recipes,
                            "reviewed_milestone_id": "M2",
                        }
                    )
                self.assertEqual(validate_workflow_automation(state), [])
                if kind == "implementation-correction":
                    capability["basis"].pop("correction_budget_identity")  # type: ignore[index]
                    missing_errors = validate_workflow_automation(state)
                    self.assertTrue(
                        any("basis.correction_budget_identity: missing" in error for error in missing_errors),
                        missing_errors,
                    )
                    capability["basis"]["correction_budget_identity"] = "sha256:other-budget"  # type: ignore[index]
                    mismatch_errors = validate_workflow_automation(state)
                    self.assertTrue(
                        any("must match capability basis" in error for error in mismatch_errors),
                        mismatch_errors,
                    )
                    capability["basis"]["correction_budget_identity"] = capability[  # type: ignore[index]
                        "scope"
                    ]["correction_budget_identity"]
                    recipes = capability["scope"]["reviewer_recipes"]  # type: ignore[index]
                    mechanical_kinds = (
                        "formatter-output",
                        "lint-autofix",
                        "generated-output-refresh",
                        "exact-approved-rename",
                        "unique-required-field-value",
                        "mechanical-state-projection-sync",
                        "deterministic-manifest-regeneration",
                    )
                    for mechanical_kind in mechanical_kinds:
                        recipes["BRF-M5-CR1"]["auto_fix_kind"] = mechanical_kind
                        capability["basis"][
                            "reviewer_classification_identity"
                        ] = structured(recipes)
                        self.assertEqual(
                            validate_workflow_automation(state),
                            [],
                            mechanical_kind,
                        )
                    recipes["BRF-M5-CR1"] = {
                        "auto_fix_class": "declared-safe",
                        "affected_paths": ["scripts/example.py"],
                        "resolution_recipe": {
                            "operation": "exact-text-replace",
                            "path": "scripts/example.py",
                            "old": "old_name",
                            "new": "new_name",
                            "expected_replacements": 1,
                        },
                        "named_inputs": ["scripts/example.py"],
                        "named_outputs": ["scripts/example.py"],
                        "forbidden_paths": ["specs/", "docs/architecture/"],
                        "acceptance_criteria": ["exact reviewed replacement"],
                        "required_validation_commands": {
                            "operation": "sha256",
                            "path": "scripts/example.py",
                            "identity": "sha256:corrected",
                        },
                        "scope_preservation_rule": "changed-paths-subset-of-affected-paths",
                        "production_code_change": "yes",
                        "behavior_test": "T13",
                    }
                    capability["basis"][
                        "reviewer_classification_identity"
                    ] = structured(recipes)
                    self.assertEqual(validate_workflow_automation(state), [])
                    recipes["BRF-M5-CR1"] = {
                        "auto_fix_class": "mechanical",
                        "auto_fix_kind": "exact-approved-rename",
                        "affected_paths": ["scripts/example.py"],
                        "deterministic_authority": {
                            "operation": "exact-text-replace",
                            "path": "scripts/example.py",
                            "old": "old_name",
                            "new": "new_name",
                            "expected_replacements": 1,
                        },
                        "required_validation": {
                            "operation": "sha256",
                            "path": "scripts/example.py",
                            "identity": "sha256:corrected",
                        },
                    }
                    recipes["BRF-M5-CR1"]["deterministic_authority"][
                        "operation"
                    ] = "future-operation"
                    capability["basis"][
                        "reviewer_classification_identity"
                    ] = "sha256:" + hashlib.sha256(
                        json.dumps(
                            recipes, sort_keys=True, separators=(",", ":")
                        ).encode()
                    ).hexdigest()
                    unknown_value_errors = validate_workflow_automation(state)
                    self.assertTrue(
                        any(
                            "expected closed reviewer recipes" in error
                            for error in unknown_value_errors
                        ),
                        unknown_value_errors,
                    )

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
                    "completion": target_completion_predicate("implement"),
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
            "completion": target_completion_predicate("spec"),
        }
        add_valid_receipt(state)
        self.assertEqual(validate_workflow_automation(state), [])

    def test_receipt_from_position_must_be_canonical_and_reach_operation(self) -> None:
        cases = (
            ("unknown", "not-a-canonical-position"),
            ("backward", "verify"),
        )
        for label, from_position in cases:
            with self.subTest(case=label):
                state = valid_automation()
                receipt = add_valid_receipt(state)
                receipt["from_position"] = from_position
                errors = validate_workflow_automation(state)
                self.assertTrue(any("from_position" in error for error in errors), errors)

    def test_receipt_accepts_conditional_skip_and_review_resolution_edges(self) -> None:
        cases = (
            ("architecture-assessment", "plan", "post-proposal-authoring"),
            ("review-resolution", "code-review", "implementation"),
        )
        for from_position, stage_name, capability_kind in cases:
            with self.subTest(stage=stage_name):
                policy = STAGE_POLICY_BY_STAGE[stage_name]
                self.assertIn(
                    from_position,
                    {rule.from_position.value for rule in policy.predecessor_rule},
                )
                self.assertEqual(policy.capability_kind.value, capability_kind)

    def test_exact_implement_target_rejects_code_review_for_same_milestone(self) -> None:
        state = valid_automation()
        target = {
            "stage": "implement",
            "occurrence": {"kind": "milestone", "milestone_id": "M1"},
            "plan_identity": "sha256:plan",
            "bound_at": "2026-07-20T00:00:00Z",
            "completion": target_completion_predicate("implement"),
        }
        state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent.update(  # type: ignore[union-attr]
            {
                "authorization_class": "implementation",
                "maximum_target": copy.deepcopy(target),
                "allowed_capability_kinds": ["implementation"],
                "maximum_mutation_categories": ["change-local-review-evidence"],
            }
        )
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability.update(  # type: ignore[union-attr]
            {
                "capability_kind": "implementation",
                "stage": {
                    "name": "code-review",
                    "occurrence": {"kind": "milestone", "milestone_id": "M1"},
                },
                "basis": {
                    "plan_identity": "sha256:plan",
                    "plan_review_identity": "sha256:plan-review",
                    "test_spec_identity": "sha256:test-spec",
                    "test_spec_review_identity": "sha256:test-spec-review",
                    "milestone_identity": "sha256:M1",
                    "affected_paths_identity": "sha256:paths",
                    "mutation_categories_identity": "sha256:categories",
                    "validation_commands_identity": "sha256:commands",
                },
                "scope": {
                    "affected_path_roots": ["docs/changes/2026-07-20-example/"],
                    "mutation_categories": ["change-local-review-evidence"],
                },
            }
        )
        receipt = add_valid_receipt(state)
        receipt["from_position"] = "implement"
        errors = validate_workflow_automation(state)
        self.assertTrue(any("run target" in error for error in errors), errors)

    def test_exact_proposal_review_target_rejects_post_review_correction(self) -> None:
        state = valid_automation()
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["allowed_capability_kinds"] = ["proposal-correction"]  # type: ignore[index]
        parent["maximum_mutation_categories"] = ["proposal-content"]  # type: ignore[index]
        parent["correction_budget"] = {"max_cycles": 1}  # type: ignore[index]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability.update(  # type: ignore[union-attr]
            {
                "capability_kind": "proposal-correction",
                "stage": {"name": "proposal", "occurrence": {"kind": "singleton"}},
                "basis": {
                    "reviewed_proposal_identity": "sha256:proposal",
                    "review_record_identity": "sha256:review",
                    "accepted_finding_set_identity": "sha256:findings",
                    "classifier_policy_identity": "sha256:classifier",
                    "correction_budget_identity": "sha256:budget",
                    "affected_proposal_roots": ["docs/proposals/"],
                },
                "scope": {
                    "affected_path_roots": ["docs/changes/2026-07-20-example/"],
                    "mutation_categories": ["proposal-content"],
                },
            }
        )
        receipt = add_valid_receipt(state)
        receipt["from_position"] = "proposal-review"
        set_policy_postcondition(receipt, WorkflowStage.PROPOSAL.value)
        errors = validate_workflow_automation(state)
        self.assertTrue(any("run target" in error for error in errors), errors)

    def test_proposal_correction_toward_later_target_requires_review_context(self) -> None:
        state = valid_automation()
        target = {
            "stage": "spec",
            "occurrence": {"kind": "singleton"},
            "bound_at": "2026-07-20T00:00:00Z",
            "completion": target_completion_predicate("spec"),
        }
        state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["maximum_target"] = copy.deepcopy(target)  # type: ignore[index]
        parent["allowed_capability_kinds"] = ["proposal-correction"]  # type: ignore[index]
        parent["maximum_mutation_categories"] = ["proposal-content"]  # type: ignore[index]
        budget = {
            "Review-fix cycle count": 1,
            "Findings auto-applied this cycle": 1,
            "Files changed this cycle": 1,
            "Files changed this invocation": 1,
        }
        accepted = ["BRF-1"]
        classifications = {"BRF-1": "mechanical"}
        correction_plans = {
            "BRF-1": {
                "classification": "mechanical",
                "rationale": "fixture rationale",
                "recipe": "Append one newline to the reviewed proposal.",
                "validation_rule": "proposal-exact-append",
            }
        }
        structured = lambda value: "sha256:" + hashlib.sha256(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        parent["correction_budget"] = copy.deepcopy(budget)  # type: ignore[index]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["capability_kind"] = "proposal-correction"  # type: ignore[index]
        capability["stage"] = {"name": "proposal", "occurrence": {"kind": "singleton"}}  # type: ignore[index]
        capability["basis"] = {  # type: ignore[index]
            "reviewed_proposal_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "accepted_finding_set_identity": structured(accepted),
            "classifier_policy_identity": structured(correction_plans),
            "correction_budget_identity": structured(budget),
            "affected_proposal_roots": ["docs/proposals/"],
        }
        capability["scope"]["mutation_categories"] = ["proposal-content"]  # type: ignore[index]
        capability["scope"].update(  # type: ignore[index]
            {
                "correction_budget": budget,
                "correction_budget_identity": structured(budget),
                "review_record_path": "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md",
                "review_resolution_path": "docs/changes/2026-07-20-example/review-resolution.md",
                "accepted_finding_ids": accepted,
                "finding_classifications": classifications,
                "correction_plans": correction_plans,
                "proposal_review_basis": {
                    "standing_gates_identity": "sha256:gates",
                    "review_policy_identity": "sha256:policy",
                    "structured_target_identity": "sha256:target",
                    "review_evidence_roots": [
                        "docs/changes/2026-07-20-example/"
                    ],
                },
            }
        )
        receipt = add_valid_receipt(state)
        receipt["from_position"] = "proposal-review"
        set_policy_postcondition(receipt, WorkflowStage.PROPOSAL.value)
        errors = validate_workflow_automation(state)
        self.assertTrue(any("review_outcome" in error for error in errors), errors)

        receipt["input_identities"] = {
            "review_outcome": "changes-requested",
            "review_identity": "sha256:review",
            "accepted_finding_set_identity": structured(accepted),
            "correction_budget_state": "remaining",
            "correction_budget_identity": structured(budget),
        }
        receipt["transition_key"] = compute_transition_key(receipt)
        self.assertEqual(validate_workflow_automation(state), [])

    def test_architecture_skip_requires_matching_applicability_evidence(self) -> None:
        state = valid_automation()
        receipt = configure_post_proposal_transition(
            state,
            stage_name="plan",
            target_stage="plan",
        )
        receipt["from_position"] = "architecture-assessment"
        receipt["input_identities"] = {"proposal": "sha256:proposal"}
        errors = validate_workflow_automation(state)
        self.assertTrue(any("architecture_applicability" in error for error in errors), errors)

        receipt["input_identities"].update(  # type: ignore[union-attr]
            {
                "architecture_applicability": "not-applicable",
                "architecture_applicability_identity": "sha256:assessment",
            }
        )
        receipt["transition_key"] = compute_transition_key(receipt)
        self.assertEqual(validate_workflow_automation(state), [])

    def test_next_milestone_requires_ordered_source_and_destination_evidence(self) -> None:
        state = valid_automation()
        receipt = configure_next_milestone_transition(state, milestone_id="M99")
        receipt["from_position"] = "code-review"
        receipt["input_identities"] = {"plan": "sha256:plan"}
        errors = validate_workflow_automation(state)
        self.assertTrue(any("source_milestone_id" in error for error in errors), errors)

        receipt["input_identities"].update(  # type: ignore[union-attr]
            {
                "source_milestone_id": "M1",
                "source_milestone_identity": "sha256:M1",
                "next_milestone_id": "M2",
                "next_milestone_identity": "sha256:M2",
                "milestone_order_identity": "sha256:order",
                "plan_identity": "sha256:plan",
            }
        )
        errors = validate_workflow_automation(state)
        self.assertTrue(any("next_milestone_id" in error for error in errors), errors)

        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["stage"]["occurrence"]["milestone_id"] = "M2"  # type: ignore[index]
        capability["basis"]["milestone_identity"] = "sha256:M2"  # type: ignore[index]
        receipt["transition_key"] = compute_transition_key(receipt)
        self.assertEqual(validate_workflow_automation(state), [])

    def test_next_milestone_allows_only_the_bound_repeated_target_occurrence(self) -> None:
        for target_stage in ("implement", "code-review"):
            with self.subTest(target=target_stage):
                state = valid_automation()
                receipt = configure_next_milestone_transition(state, milestone_id="M2")
                target = {
                    "stage": target_stage,
                    "occurrence": {"kind": "milestone", "milestone_id": "M2"},
                    "plan_identity": "sha256:plan",
                    "bound_at": "2026-07-20T00:00:00Z",
                    "completion": target_completion_predicate(target_stage),
                }
                state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
                parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
                parent["maximum_target"] = copy.deepcopy(target)  # type: ignore[index]
                receipt["target"] = copy.deepcopy(target)
                receipt["from_position"] = "code-review"
                receipt["input_identities"] = {
                    "source_milestone_id": "M1",
                    "source_milestone_identity": "sha256:M1",
                    "next_milestone_id": "M2",
                    "next_milestone_identity": "sha256:M2",
                    "milestone_order_identity": "sha256:order",
                    "plan_identity": "sha256:plan",
                }
                receipt["transition_key"] = compute_transition_key(receipt)
                self.assertEqual(validate_workflow_automation(state), [])

                stale_target = copy.deepcopy(target)
                stale_target["occurrence"]["milestone_id"] = "M1"
                state["run"]["target"] = copy.deepcopy(stale_target)  # type: ignore[index]
                parent["maximum_target"] = copy.deepcopy(stale_target)  # type: ignore[index]
                receipt["target"] = copy.deepcopy(stale_target)
                errors = validate_workflow_automation(state)
                self.assertTrue(any("milestone_id" in error for error in errors), errors)

    def test_milestone_code_review_requires_same_source_occurrence(self) -> None:
        state = valid_automation()
        receipt = configure_next_milestone_transition(state, milestone_id="M1")
        target = {
            "stage": "code-review",
            "occurrence": {"kind": "milestone", "milestone_id": "M1"},
            "plan_identity": "sha256:plan",
            "bound_at": "2026-07-20T00:00:00Z",
            "completion": target_completion_predicate("code-review"),
        }
        state["run"]["target"] = copy.deepcopy(target)  # type: ignore[index]
        parent = state["parent_authorizations"]["authorization-authoring-001"]  # type: ignore[index]
        parent["maximum_target"] = copy.deepcopy(target)  # type: ignore[index]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["stage"]["name"] = "code-review"  # type: ignore[index]
        capability["scope"]["mutation_categories"] = ["change-local-review-evidence"]  # type: ignore[index]
        parent["maximum_mutation_categories"] = ["change-local-review-evidence"]  # type: ignore[index]
        receipt["target"] = copy.deepcopy(target)
        receipt["from_position"] = "implement"
        receipt["retry_policy"] = STAGE_POLICY_BY_STAGE[
            WorkflowStage.CODE_REVIEW.value
        ].retry_policy.value
        set_policy_postcondition(receipt, WorkflowStage.CODE_REVIEW.value)
        receipt["input_identities"] = {
            "source_milestone_id": "M0",
            "source_milestone_identity": "sha256:M0",
            "plan_identity": "sha256:plan",
        }
        errors = validate_workflow_automation(state)
        self.assertTrue(any("source_milestone_id" in error for error in errors), errors)

        receipt["input_identities"] = {
            "source_milestone_id": "M1",
            "source_milestone_identity": "sha256:M1",
            "plan_identity": "sha256:plan",
        }
        receipt["transition_key"] = compute_transition_key(receipt)
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
                        "completion": target_completion_predicate("spec"),
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
            "completion": target_completion_predicate("spec"),
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

    def test_receipt_rejects_non_deterministic_concrete_evidence(self) -> None:
        cases = (
            ("whitespace", {"review_occurrence": "   "}),
            ("nan", {"review_occurrence": math.nan}),
            ("positive-infinity", {"review_occurrence": math.inf}),
            ("negative-infinity", {"review_occurrence": -math.inf}),
            ("nested-whitespace", {"nested": ["valid", {"value": "\t"}]}),
            ("nested-nan", {"nested": [{"value": math.nan}]}),
        )
        for label, postcondition in cases:
            with self.subTest(case=label):
                state = valid_automation()
                receipt = add_valid_receipt(state)
                receipt["expected_postcondition"] = postcondition
                errors = validate_workflow_automation(state)
                self.assertTrue(any("expected_postcondition" in error for error in errors), errors)

        state = valid_automation()
        receipt = add_valid_receipt(state)
        receipt["input_identities"] = {"proposal": "   "}
        errors = validate_workflow_automation(state)
        self.assertTrue(any("input_identities.proposal" in error for error in errors), errors)

    def test_receipt_rejects_cyclic_concrete_evidence(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        postcondition: dict[str, object] = {"review_occurrence": "recorded"}
        postcondition["cycle"] = postcondition
        receipt["expected_postcondition"] = postcondition
        errors = validate_workflow_automation(state)
        self.assertTrue(any("cyclic concrete evidence" in error for error in errors), errors)

    def test_receipt_rejects_caller_defined_postcondition(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        receipt["expected_postcondition"] = {
            "attempt": 1,
            "ratio": 0.5,
            "large_counter": 10**1000,
        }
        receipt["transition_key"] = compute_transition_key(receipt)
        errors = validate_workflow_automation(state)
        self.assertTrue(any("must match immutable stage policy" in error for error in errors), errors)

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

    def test_receipt_requires_retry_policy_projection(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        del receipt["retry_policy"]
        errors = validate_workflow_automation(state)
        self.assertTrue(
            any("transition-001.retry_policy: missing required field" in error for error in errors),
            errors,
        )

    def test_receipt_retry_policy_must_match_immutable_stage_policy(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        receipt["retry_policy"] = "idempotent-retry"
        errors = validate_workflow_automation(state)
        self.assertIn(
            "workflow.automation.transition_receipts.transition-001.retry_policy: "
            "must match immutable stage policy reconcile-only",
            errors,
        )

    def test_receipt_transition_key_must_match_immutable_inputs(self) -> None:
        for status in ("prepared", "completed"):
            with self.subTest(status=status):
                state = valid_automation()
                receipt = add_valid_receipt(state)
                receipt["transition_key"] = compute_transition_key(receipt)
                if status == "completed":
                    receipt.update(
                        status="completed",
                        outputs=["sha256:proposal-review"],
                        canonical_sync={"status": "synchronized"},
                    )
                    capability = state["effective_capabilities"][
                        "capability-proposal-review-001"
                    ]
                    capability["status"] = "consumed"
                receipt["input_identities"] = {
                    "proposal": "sha256:tampered-after-key"
                }
                errors = validate_workflow_automation(state)
                self.assertTrue(
                    any(
                        "transition_key: does not match immutable operation inputs"
                        in error
                        for error in errors
                    ),
                    errors,
                )

    def test_completed_receipt_accepts_consumed_capability(self) -> None:
        state = valid_automation()
        add_completed_proposal_review(
            state,
            {
                "review_id": "proposal-review-r1",
                "reviewed_artifact_identity": "sha256:proposal",
                "review_record_identity": "sha256:proposal-review",
                "outcome": "approved",
                "occurrence_recorded": True,
                "clean_gate": "satisfied",
                "routing_action": "stop-at-target",
            },
        )
        state["run"]["status"] = "completed"
        self.assertEqual(validate_workflow_automation(state), [])

    def test_completed_receipt_requires_independent_sync_evidence(self) -> None:
        for missing_field in ("evidence", "observed_identities"):
            state = valid_automation()
            receipt = add_valid_receipt(state)
            receipt["status"] = "completed"
            receipt["outputs"] = [
                {
                    "path": "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md",
                    "identity": "sha256:proposal-review",
                }
            ]
            receipt["canonical_sync"] = {
                "status": "synchronized",
                "evidence": {
                    "proposal-review": {
                        "path": "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md",
                        "identity": "sha256:proposal-review",
                    }
                },
                "observed_identities": {
                    "proposal-review": "sha256:proposal-review"
                },
            }
            del receipt["canonical_sync"][missing_field]
            capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
            capability["status"] = "consumed"  # type: ignore[index]
            errors = validate_workflow_automation(state)
            self.assertTrue(
                any(f"canonical_sync.{missing_field}" in error for error in errors),
                errors,
            )

    def test_completed_receipt_evidence_must_remain_in_capability_scope(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        outside = {
            "path": "docs/outside/review.md",
            "identity": "sha256:proposal-review",
        }
        receipt["status"] = "completed"
        receipt["outputs"] = [outside]
        receipt["canonical_sync"] = {
            "status": "synchronized",
            "evidence": {"proposal-review": outside},
            "observed_identities": {"proposal-review": "sha256:proposal-review"},
        }
        capability = state["effective_capabilities"]["capability-proposal-review-001"]  # type: ignore[index]
        capability["status"] = "consumed"  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertTrue(any("exceeds effective capability scope" in error for error in errors), errors)

    def test_multiple_prepared_receipts_fail_closed(self) -> None:
        state = valid_automation()
        receipt = add_valid_receipt(state)
        second = copy.deepcopy(receipt)
        second["transition_id"] = "transition-002"
        second["transition_key"] = "sha256:transition-002"
        state["transition_receipts"]["transition-002"] = second  # type: ignore[index]
        errors = validate_workflow_automation(state)
        self.assertIn(
            "workflow.automation.transition_receipts: at most one prepared transition is permitted",
            errors,
        )

    def test_valid_migration_receipt_is_accepted(self) -> None:
        state = valid_automation()
        add_valid_migration_receipt(state)
        self.assertEqual(validate_workflow_automation(state), [])

    def test_unknown_migration_source_mechanism_fails_closed(self) -> None:
        state = valid_automation()
        migration = add_valid_migration_receipt(state)
        migration["source_mechanism"] = "unknown-value"
        errors = validate_workflow_automation(state)
        self.assertTrue(any("source_mechanism: unknown value" in error for error in errors), errors)

    def test_unknown_migration_projection_result_fails_closed(self) -> None:
        state = valid_automation()
        migration = add_valid_migration_receipt(state)
        migration["projection_result"] = "close-enough"
        errors = validate_workflow_automation(state)
        self.assertTrue(any("projection_result: unknown value" in error for error in errors), errors)

    def test_forbidden_live_state_fields_fail(self) -> None:
        state = valid_automation()
        state["next_stage"] = "spec"
        self.assertIn(
            "workflow.automation.next_stage: automation state must not own live workflow state",
            validate_workflow_automation(state),
        )


if __name__ == "__main__":
    unittest.main()
