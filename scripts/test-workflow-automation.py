#!/usr/bin/env python3
"""Target, position, capability, and one-stage coordinator tests."""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from workflow_automation import (
    ActivePlanContext,
    ArtifactEvidence,
    AutomationContractError,
    CanonicalSyncResult,
    PrePlanEvidence,
    StageExecutionResult,
    bind_target,
    coordinate_one_stage,
    create_parent_authorization,
    derive_effective_capability,
    invalidate_effective_capabilities,
    normalize_command,
    persist_target,
    record_plan_ownership_handoff,
    resolve_canonical_position,
    resolve_command_target,
    resume_target,
)
from workflow_automation_policy import PUBLIC_TARGET_STAGES, STAGE_POLICY_BY_STAGE
from workflow_automation_state import WorkflowAutomationStateStore, dump_yaml
from validate_workflow_automation import validate_workflow_automation


ROOT = Path(__file__).resolve().parents[1]


def _load_fixtures():
    path = ROOT / "scripts" / "test-validate-workflow-automation.py"
    spec = importlib.util.spec_from_file_location("workflow_engine_fixtures", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


FIXTURES = _load_fixtures()


def plan_text(
    *,
    current: str = "M2. Engine Slice",
    current_state: str = "implementing",
    remaining: str = "M2, M3",
    next_stage: str = "implement M2",
    milestone_two_state: str | None = None,
    duplicate_m2: bool = False,
) -> str:
    state = milestone_two_state or current_state
    duplicate = (
        f"\n### M2. Engine Slice\n\n- Milestone state: {current_state}\n"
        if duplicate_m2
        else ""
    )
    return f"""# Engine Plan

## Status

Plan lifecycle state: active
Terminal disposition: none
Change ID: 2026-07-20-example

## Current Handoff Summary

- Current milestone: {current}
- Current milestone state: {current_state}
- Latest review evidence: reviews/code-review.md
- Review status: approved; stage=code-review; round=r1
- Remaining in-scope implementation milestones: {remaining}
- Next stage: {next_stage}
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, explain-change-pending, verify-pending, pr-handoff-pending — fixture work remains.

## Milestones

### M1. Prior Slice

- Milestone state: closed

### M2. Engine Slice

- Milestone state: {state}
{duplicate}
### M3. Later Slice

- Milestone state: planned
"""


class WorkflowAutomationEngineTests(unittest.TestCase):
    def make_store(self, automation: dict) -> WorkflowAutomationStateStore:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "change.yaml"
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Engine fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                    "workflow": {"automation": automation},
                }
            ),
            encoding="utf-8",
        )
        return WorkflowAutomationStateStore(path)

    def test_target_command_normalization_is_closed_and_legacy_is_adapter_only(self) -> None:
        current = normalize_command("$workflow auto: code-review")
        self.assertEqual((current.action, current.target_stage, current.legacy), ("target", "code-review", False))

        legacy = normalize_command("workflow auto-through: verify")
        self.assertEqual((legacy.action, legacy.target_stage, legacy.legacy), ("target", "verify", True))
        self.assertEqual(normalize_command("workflow auto: status").action, "status")
        self.assertEqual(normalize_command("workflow auto-through: off").action, "off")
        legacy_target = resolve_command_target(
            "workflow auto-through: verify",
            bound_at="2026-07-22T00:00:00Z",
        )
        self.assertEqual(legacy_target["stage"], "verify")
        self.assertEqual(legacy_target["occurrence"]["kind"], "final")

        for command in ("workflow auto: future", "workflow auto-through: spec", "auto: verify"):
            with self.subTest(command=command), self.assertRaises(AutomationContractError):
                normalize_command(command)

    def test_target_occurrence_and_completion_are_bound_before_persistence(self) -> None:
        plan = ActivePlanContext.from_text(plan_text(), plan_identity="sha256:plan-v1")
        for stage in sorted(PUBLIC_TARGET_STAGES, key=lambda item: item.value):
            with self.subTest(stage=stage.value):
                target = bind_target(
                    stage.value,
                    bound_at="2026-07-22T00:00:00Z",
                    plan=plan if stage.value in {"implement", "code-review"} else None,
                )
                expected_kind = STAGE_POLICY_BY_STAGE[stage.value].occurrence_rule.value
                self.assertEqual(target["occurrence"]["kind"], expected_kind)
                self.assertTrue(target["completion"])
                if expected_kind == "milestone":
                    self.assertEqual(target["occurrence"]["milestone_id"], "M2")
                    self.assertEqual(target["plan_identity"], "sha256:plan-v1")

                tampered = copy.deepcopy(target)
                tampered["completion"] = {"rule": "attacker-chosen"}
                with self.assertRaisesRegex(
                    AutomationContractError, "completion predicate"
                ):
                    resume_target(tampered)

        invalid_pairs = (("implement", "singleton"), ("code-review", "final"), ("verify", "milestone"), ("spec", "final"))
        for stage, occurrence in invalid_pairs:
            with self.subTest(stage=stage, occurrence=occurrence), self.assertRaises(AutomationContractError):
                bind_target(
                    stage,
                    bound_at="2026-07-22T00:00:00Z",
                    plan=plan,
                    requested_occurrence=occurrence,
                )

    def test_target_repeated_stage_requires_one_current_in_scope_milestone(self) -> None:
        diagnostic = (
            "cannot bind implement target: active plan does not identify exactly one "
            "current in-scope implementation milestone"
        )
        cases = (
            None,
            ActivePlanContext.from_text(plan_text(current="M9. Missing"), plan_identity="sha256:plan"),
            ActivePlanContext.from_text(plan_text(current_state="closed", milestone_two_state="closed"), plan_identity="sha256:plan"),
            ActivePlanContext.from_text(plan_text(remaining="M3"), plan_identity="sha256:plan"),
        )
        for plan in cases:
            with self.subTest(plan=plan), self.assertRaisesRegex(AutomationContractError, diagnostic):
                bind_target("implement", bound_at="2026-07-22T00:00:00Z", plan=plan)

        with self.assertRaisesRegex(AutomationContractError, diagnostic):
            ambiguous = ActivePlanContext.from_text(
                plan_text(duplicate_m2=True), plan_identity="sha256:plan"
            )
            bind_target("implement", bound_at="2026-07-22T00:00:00Z", plan=ambiguous)

    def test_target_resume_never_rebinds_after_plan_advances(self) -> None:
        original_plan = ActivePlanContext.from_text(plan_text(), plan_identity="sha256:plan-v1")
        persisted = bind_target("code-review", bound_at="2026-07-22T00:00:00Z", plan=original_plan)
        advanced = ActivePlanContext.from_text(
            plan_text(current="M3. Later Slice", remaining="M3", next_stage="implement M3"),
            plan_identity="sha256:plan-v2",
        )

        resumed = resume_target(persisted, current_plan=advanced)

        self.assertEqual(resumed["occurrence"]["milestone_id"], "M2")
        self.assertEqual(resumed["plan_identity"], "sha256:plan-v1")

        malformed = copy.deepcopy(persisted)
        del malformed["bound_at"]
        with self.assertRaises(AutomationContractError):
            resume_target(malformed, current_plan=advanced)

    def test_position_preplan_uses_current_unambiguous_evidence(self) -> None:
        evidence = PrePlanEvidence(
            positions={
                "proposal": ("sha256:proposal",),
                "proposal-review": ("sha256:proposal-review",),
                "spec": ("sha256:spec",),
                "spec-review": ("sha256:spec-review",),
            },
            review_outcomes={"proposal-review": "approved", "spec-review": "approved"},
            review_resolution_closed=True,
            architecture_applicability="not-required",
        )

        position = resolve_canonical_position(pre_plan=evidence)

        self.assertEqual(position.position, "spec-review")
        self.assertEqual(position.source, "authoritative-artifact-review-evidence")
        self.assertNotIn("current_stage", position.observed_identities)

    def test_position_preplan_ambiguity_staleness_and_contradiction_pause(self) -> None:
        base = {
            "positions": {"proposal": ("sha256:proposal",), "proposal-review": ("sha256:review",)},
            "review_outcomes": {"proposal-review": "approved"},
            "review_resolution_closed": True,
            "architecture_applicability": "required",
        }
        cases = (
            PrePlanEvidence(**{**base, "positions": {"proposal": ("sha256:a", "sha256:b")}}),
            PrePlanEvidence(**base, stale_identities=frozenset({"sha256:review"})),
            PrePlanEvidence(**{**base, "positions": {**base["positions"], "spec": ("sha256:spec",)}, "review_outcomes": {"proposal-review": "changes-requested"}}),
            PrePlanEvidence(**{**base, "architecture_applicability": "ambiguous"}),
            PrePlanEvidence(**{**base, "review_outcomes": {"proposal-review": "unknown"}}),
            PrePlanEvidence(
                **base,
                transition_identities={"unknown-stage": "sha256:transition"},
            ),
        )
        for evidence in cases:
            with self.subTest(evidence=evidence), self.assertRaises(AutomationContractError):
                resolve_canonical_position(pre_plan=evidence)

    def test_position_valid_plan_handoff_becomes_canonical_owner(self) -> None:
        plan = ActivePlanContext.from_text(plan_text(), plan_identity="sha256:plan-v1")

        position = resolve_canonical_position(active_plan=plan)

        self.assertEqual(position.position, "code-review")
        self.assertEqual(position.source, "plan-current-handoff-summary")
        self.assertEqual(position.milestone_id, "M2")
        self.assertEqual(position.observed_identities["plan"], "sha256:plan-v1")

        pre_plan = PrePlanEvidence(
            positions={
                "proposal": ("sha256:proposal",),
                "proposal-review": ("sha256:proposal-review",),
                "spec": ("sha256:spec",),
                "spec-review": ("sha256:spec-review",),
                "architecture-assessment": ("sha256:assessment",),
                "plan": ("sha256:plan-artifact",),
            },
            review_outcomes={"proposal-review": "approved", "spec-review": "approved"},
            review_resolution_closed=True,
            architecture_applicability="not-required",
        )
        handoff = record_plan_ownership_handoff(pre_plan, plan)
        self.assertEqual(handoff["plan_identity"], "sha256:plan-v1")
        self.assertEqual(handoff["pre_plan_evidence"]["plan"], "sha256:plan-artifact")

        stale = dataclasses.replace(
            pre_plan, stale_identities=frozenset({"sha256:spec-review"})
        )
        with self.assertRaisesRegex(AutomationContractError, "stale canonical"):
            record_plan_ownership_handoff(stale, plan)

    def test_position_observed_identity_drift_pauses(self) -> None:
        plan = ActivePlanContext.from_text(plan_text(), plan_identity="sha256:plan-v2")
        with self.assertRaisesRegex(AutomationContractError, "canonical-state-mismatch"):
            resolve_canonical_position(
                active_plan=plan,
                previously_observed={"plan": "sha256:plan-v1"},
            )

        inconsistent = ActivePlanContext.from_text(
            plan_text(next_stage="code-review M2"), plan_identity="sha256:plan-v2"
        )
        with self.assertRaisesRegex(AutomationContractError, "active plan next stage"):
            resolve_canonical_position(active_plan=inconsistent)

        pre_plan = PrePlanEvidence(
            positions={
                "proposal": ("sha256:proposal",),
                "proposal-review": ("sha256:proposal-review",),
            },
            review_outcomes={"proposal-review": "approved"},
            review_resolution_closed=True,
            architecture_applicability="not-required",
            transition_identities={"proposal-review": "sha256:transition"},
        )
        with self.assertRaisesRegex(AutomationContractError, "canonical-state-mismatch"):
            resolve_canonical_position(
                pre_plan=pre_plan,
                previously_observed={"spec": "sha256:spec"},
            )

    def test_capability_parent_is_non_executable_and_risk_scoped(self) -> None:
        target = bind_target("verify", bound_at="2026-07-22T00:00:00Z")
        parent = create_parent_authorization(
            authorization_id="auth-authoring",
            authorization_class="authoring",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=("proposal-review",),
            maximum_path_roots=("docs/changes/2026-07-20-example/",),
            maximum_mutation_categories=("change-local-review-evidence",),
        )
        self.assertNotIn("execute", parent)

        with self.assertRaisesRegex(AutomationContractError, "parent authorization is non-executable"):
            coordinate_one_stage(parent_authorization=parent)  # type: ignore[call-arg]

        with self.assertRaisesRegex(AutomationContractError, "future-contingent verification authorization"):
            create_parent_authorization(
                authorization_id="auth-verify",
                authorization_class="verification",
                change_id="2026-07-20-example",
                authorized_by="user",
                authorized_at="2026-07-22T00:00:00Z",
                maximum_target=target,
                allowed_capability_kinds=("verification",),
                maximum_path_roots=("docs/changes/2026-07-20-example/",),
                maximum_mutation_categories=("verification-evidence",),
            )

        with self.assertRaisesRegex(AutomationContractError, "unknown policy version"):
            create_parent_authorization(
                authorization_id="auth-unknown-policy",
                authorization_class="authoring",
                change_id="2026-07-20-example",
                authorized_by="user",
                authorized_at="2026-07-22T00:00:00Z",
                maximum_target=target,
                allowed_capability_kinds=("proposal-review",),
                maximum_path_roots=("docs/changes/2026-07-20-example/",),
                maximum_mutation_categories=("change-local-review-evidence",),
                policy_version=99,
            )

        verification_basis = {
            "closed_milestones_identity": "sha256:milestones",
            "final_code_review_identity": "sha256:review",
            "promotion_evidence_identity": "sha256:promotion",
            "explanation_inputs_identity": "sha256:explanation",
            "branch_state_identity": "sha256:branch",
            "verification_commands_identity": "sha256:commands",
        }
        verification_parent = create_parent_authorization(
            authorization_id="auth-verify-complete",
            authorization_class="verification",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=("verification",),
            maximum_path_roots=("docs/changes/2026-07-20-example/",),
            maximum_mutation_categories=("verification-evidence",),
            verification_basis=verification_basis,
        )
        self.assertEqual(verification_parent["authorization_class"], "verification")

        with self.assertRaises(AutomationContractError):
            create_parent_authorization(
                authorization_id="auth-invalid-category",
                authorization_class="authoring",
                change_id="2026-07-20-example",
                authorized_by="user",
                authorized_at="2026-07-22T00:00:00Z",
                maximum_target=target,
                allowed_capability_kinds=("proposal-review",),
                maximum_path_roots=("docs/changes/2026-07-20-example/",),
                maximum_mutation_categories=("production-code",),
            )

    def test_capability_derivation_requires_current_complete_subset_basis(self) -> None:
        target = bind_target("spec", bound_at="2026-07-22T00:00:00Z")
        parent = create_parent_authorization(
            authorization_id="auth-authoring",
            authorization_class="authoring",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=("post-proposal-authoring",),
            maximum_path_roots=("specs/", "docs/changes/2026-07-20-example/"),
            maximum_mutation_categories=("downstream-authoring-artifacts",),
        )
        basis = {
            "proposal_identity": "sha256:proposal",
            "approved_proposal_review_identity": "sha256:proposal-review",
            "closed_review_resolution_identity": "sha256:resolution",
            "stage_scope_identity": "sha256:scope",
        }
        capability = derive_effective_capability(
            capability_id="cap-spec",
            parent=parent,
            stage="spec",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("specs/",),
            mutation_categories=("downstream-authoring-artifacts",),
            derived_at="2026-07-22T00:01:00Z",
        )
        self.assertEqual(capability["parent_authorization_id"], "auth-authoring")
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["run"]["target"] = copy.deepcopy(target)
        state["parent_authorizations"] = {"auth-authoring": parent}
        state["effective_capabilities"] = {"cap-spec": capability}
        self.assertEqual(validate_workflow_automation(state), [])

        invalid = (
            {"basis": {"proposal_identity": "sha256:proposal"}},
            {"basis_current": False},
            {"affected_path_roots": ("scripts/",)},
            {"mutation_categories": ("production-code",)},
        )
        for overrides in invalid:
            with self.subTest(overrides=overrides), self.assertRaises(AutomationContractError):
                derive_effective_capability(
                    capability_id="cap-invalid",
                    parent=parent,
                    stage="spec",
                    occurrence={"kind": "singleton"},
                    basis=overrides.get("basis", basis),
                    basis_current=overrides.get("basis_current", True),
                    affected_path_roots=overrides.get("affected_path_roots", ("specs/",)),
                    mutation_categories=overrides.get("mutation_categories", ("downstream-authoring-artifacts",)),
                    derived_at="2026-07-22T00:01:00Z",
                )

    def test_capability_conflict_and_cross_risk_derivation_fail_closed(self) -> None:
        target = bind_target("spec", bound_at="2026-07-22T00:00:00Z")
        parent = create_parent_authorization(
            authorization_id="auth-authoring",
            authorization_class="authoring",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=("post-proposal-authoring",),
            maximum_path_roots=("specs/",),
            maximum_mutation_categories=("downstream-authoring-artifacts",),
        )
        basis = {
            "proposal_identity": "sha256:proposal",
            "approved_proposal_review_identity": "sha256:proposal-review",
            "closed_review_resolution_identity": "sha256:resolution",
            "stage_scope_identity": "sha256:scope",
        }
        existing = derive_effective_capability(
            capability_id="cap-existing",
            parent=parent,
            stage="spec",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("specs/",),
            mutation_categories=("downstream-authoring-artifacts",),
            derived_at="2026-07-22T00:01:00Z",
        )
        with self.assertRaisesRegex(AutomationContractError, "conflicting active capability"):
            derive_effective_capability(
                capability_id="cap-second",
                parent=parent,
                stage="spec",
                occurrence={"kind": "singleton"},
                basis=basis,
                affected_path_roots=("specs/",),
                mutation_categories=("downstream-authoring-artifacts",),
                derived_at="2026-07-22T00:02:00Z",
                existing_capabilities=(existing,),
            )
        with self.assertRaises(AutomationContractError):
            derive_effective_capability(
                capability_id="cap-implement",
                parent=parent,
                stage="implement",
                occurrence={"kind": "milestone", "milestone_id": "M2"},
                basis={},
                affected_path_roots=("scripts/",),
                mutation_categories=("production-code",),
                derived_at="2026-07-22T00:02:00Z",
            )

        invalidated = invalidate_effective_capabilities(
            (existing,),
            parent_authorization_id="auth-authoring",
            reason="basis-changed",
        )
        self.assertEqual(invalidated[0]["status"], "invalidated")
        self.assertEqual(invalidated[0]["invalidation_reason"], "basis-changed")
        self.assertEqual(existing["status"], "active")

    def test_capability_correction_budget_must_be_current_remaining_and_bounded(self) -> None:
        parent = create_parent_authorization(
            authorization_id="auth-correction",
            authorization_class="authoring",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=bind_target("spec", bound_at="2026-07-22T00:00:00Z"),
            allowed_capability_kinds=("proposal-correction",),
            maximum_path_roots=("docs/proposals/",),
            maximum_mutation_categories=("proposal-content",),
            correction_budget={"cycles": 2, "findings": 4},
        )
        basis = {
            "reviewed_proposal_identity": "sha256:proposal",
            "review_record_identity": "sha256:review",
            "accepted_finding_set_identity": "sha256:findings",
            "classifier_policy_identity": "sha256:classifier",
            "correction_budget_identity": "sha256:budget-v1",
            "affected_proposal_roots": ["docs/proposals/"],
        }

        capability = derive_effective_capability(
            capability_id="cap-correction",
            parent=parent,
            stage="proposal",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("docs/proposals/",),
            mutation_categories=("proposal-content",),
            correction_budget={"cycles": 1, "findings": 2},
            correction_budget_identity="sha256:budget-v1",
            derived_at="2026-07-22T00:01:00Z",
        )
        self.assertEqual(capability["scope"]["correction_budget"]["cycles"], 1)

        invalid_budgets = (
            {"cycles": 0, "findings": 2},
            {"cycles": 3, "findings": 2},
            {"cycles": 1},
        )
        for index, budget in enumerate(invalid_budgets):
            with self.subTest(budget=budget), self.assertRaises(AutomationContractError):
                derive_effective_capability(
                    capability_id=f"cap-invalid-budget-{index}",
                    parent=parent,
                    stage="proposal",
                    occurrence={"kind": "singleton"},
                    basis=basis,
                    affected_path_roots=("docs/proposals/",),
                    mutation_categories=("proposal-content",),
                    correction_budget=budget,
                    correction_budget_identity="sha256:budget-v1",
                    derived_at="2026-07-22T00:01:00Z",
                )
        with self.assertRaisesRegex(AutomationContractError, "budget identity"):
            derive_effective_capability(
                capability_id="cap-stale-budget",
                parent=parent,
                stage="proposal",
                occurrence={"kind": "singleton"},
                basis=basis,
                affected_path_roots=("docs/proposals/",),
                mutation_categories=("proposal-content",),
                correction_budget={"cycles": 1, "findings": 2},
                correction_budget_identity="sha256:budget-v2",
                derived_at="2026-07-22T00:01:00Z",
            )

        implementation_parent = create_parent_authorization(
            authorization_id="auth-implementation-correction",
            authorization_class="implementation",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=bind_target(
                "code-review",
                bound_at="2026-07-22T00:00:00Z",
                plan=ActivePlanContext.from_text(
                    plan_text(), plan_identity="sha256:plan-v1"
                ),
            ),
            allowed_capability_kinds=("implementation-correction",),
            maximum_path_roots=("docs/changes/2026-07-20-example/",),
            maximum_mutation_categories=("change-local-evidence",),
            correction_budget={"cycles": 1},
        )
        implementation_basis = {
            "code_review_identity": "sha256:implementation-review",
            "accepted_finding_set_identity": "sha256:implementation-findings",
            "reviewer_classification_identity": "sha256:reviewer-classification",
            "correction_budget_identity": "sha256:implementation-budget",
            "affected_paths_identity": "sha256:paths",
        }
        implementation_capability = derive_effective_capability(
            capability_id="cap-implementation-correction",
            parent=implementation_parent,
            stage="review-resolution",
            occurrence={"kind": "singleton"},
            basis=implementation_basis,
            affected_path_roots=("docs/changes/2026-07-20-example/",),
            mutation_categories=("change-local-evidence",),
            correction_budget={"cycles": 1},
            correction_budget_identity="sha256:implementation-budget",
            derived_at="2026-07-22T00:01:00Z",
        )
        self.assertEqual(
            implementation_capability["scope"]["correction_budget"], {"cycles": 1}
        )
        incomplete_implementation_basis = dict(implementation_basis)
        incomplete_implementation_basis.pop("correction_budget_identity")
        with self.assertRaisesRegex(AutomationContractError, "basis is incomplete"):
            derive_effective_capability(
                capability_id="cap-implementation-correction-missing-budget-identity",
                parent=implementation_parent,
                stage="review-resolution",
                occurrence={"kind": "singleton"},
                basis=incomplete_implementation_basis,
                affected_path_roots=("docs/changes/2026-07-20-example/",),
                mutation_categories=("change-local-evidence",),
                correction_budget={"cycles": 1},
                correction_budget_identity="sha256:implementation-budget",
                derived_at="2026-07-22T00:01:00Z",
            )
        with self.assertRaisesRegex(AutomationContractError, "exhausted"):
            derive_effective_capability(
                capability_id="cap-implementation-correction-exhausted",
                parent=implementation_parent,
                stage="review-resolution",
                occurrence={"kind": "singleton"},
                basis=implementation_basis,
                affected_path_roots=("docs/changes/2026-07-20-example/",),
                mutation_categories=("change-local-evidence",),
                correction_budget={"cycles": 0},
                correction_budget_identity="sha256:implementation-budget",
                derived_at="2026-07-22T00:01:00Z",
            )

    def test_capability_verify_target_persists_without_future_authority(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        store = self.make_store(state)
        target = bind_target("verify", bound_at="2026-07-22T00:00:00Z")

        persist_target(store, target, expected_document_identity=store.read().document_identity)

        persisted = store.read().automation
        self.assertEqual(persisted["run"]["target"], target)
        self.assertFalse(
            any(
                parent["authorization_class"] == "verification"
                for parent in persisted["parent_authorizations"].values()
            )
        )

    def test_capability_one_stage_coordination_persists_receipt_before_invocation(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)
        observed: list[str] = []
        proposal_identity = self.write_proposal(store)

        def invoke() -> StageExecutionResult:
            snapshot = store.read().automation
            receipt = snapshot["transition_receipts"]["transition-engine-001"]
            self.assertEqual(receipt["status"], "prepared")
            self.assertEqual(receipt["effective_capability_id"], "capability-engine-001")
            observed.append("invoked")
            evidence = self.write_evidence(store)
            return StageExecutionResult(
                outputs=(evidence,),
                completion_evidence={"proposal-review": evidence},
            )

        result = coordinate_one_stage(
            store=store,
            parent_authorization_id="authorization-authoring-001",
            capability_id="capability-engine-001",
            stage="proposal-review",
            occurrence={"kind": "singleton"},
            basis={
                "proposal_identity": proposal_identity,
                "standing_gates_identity": "sha256:gates",
                "review_policy_identity": "sha256:policy",
                "structured_target_identity": "sha256:target",
                "review_evidence_roots": ["docs/changes/2026-07-20-example/"],
            },
            affected_path_roots=("docs/changes/2026-07-20-example/",),
            mutation_categories=("change-local-review-evidence",),
            derived_at="2026-07-22T00:01:00Z",
            transition_id="transition-engine-001",
            input_identities=self.proposal_input_identities(proposal_identity),
            invoke_stage=invoke,
            repository_root=store.metadata_path.parent,
            pre_plan=self.proposal_pre_plan(proposal_identity),
            synchronize_canonical_state=lambda result: self.synchronize_review(
                store, result
            ),
        )

        self.assertEqual(observed, ["invoked"])
        self.assertEqual(result.status, "completed")
        completed = store.read().automation["transition_receipts"]["transition-engine-001"]
        self.assertEqual(completed["status"], "completed")
        self.assertEqual(
            completed["expected_postcondition"],
            {
                "completion_rule": "formal review occurrence is recorded",
                "required_evidence": ["proposal-review"],
            },
        )
        self.assertEqual(
            completed["canonical_sync"]["observed_identities"]["proposal-review"],
            completed["canonical_sync"]["evidence"]["proposal-review"]["identity"],
        )
        self.assertEqual(
            store.read().automation["effective_capabilities"]["capability-engine-001"]["status"],
            "consumed",
        )

    def test_capability_one_stage_failure_records_failure_without_consuming(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)

        def invoke() -> StageExecutionResult:
            raise RuntimeError("stage failed")

        with self.assertRaisesRegex(RuntimeError, "stage failed"):
            self.coordinate_proposal_review(store, invoke)

        persisted = store.read().automation
        self.assertEqual(
            persisted["transition_receipts"]["transition-engine-001"]["status"],
            "failed",
        )
        self.assertEqual(
            persisted["effective_capabilities"]["capability-engine-001"]["status"],
            "active",
        )

    def test_capability_one_stage_rejects_in_flight_transition_without_mutation(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        FIXTURES.add_valid_receipt(state)
        store = self.make_store(state)
        before = store.read().document_identity

        with self.assertRaisesRegex(AutomationContractError, "already in flight"):
            self.coordinate_proposal_review(
                store,
                lambda: StageExecutionResult(
                    outputs=(ArtifactEvidence("missing", "sha256:missing"),),
                    completion_evidence={
                        "proposal-review": ArtifactEvidence("missing", "sha256:missing")
                    },
                ),
            )

        self.assertEqual(store.read().document_identity, before)
        self.assertNotIn(
            "capability-engine-001", store.read().automation["effective_capabilities"]
        )

    def test_capability_coordination_rejects_foreign_repository_before_invocation(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)
        foreign = tempfile.TemporaryDirectory()
        self.addCleanup(foreign.cleanup)
        invoked: list[bool] = []
        before = store.read().document_identity

        with self.assertRaisesRegex(
            AutomationContractError, "repository root does not match state store"
        ):
            self.coordinate_proposal_review(
                store,
                lambda: invoked.append(True),
                repository_root=Path(foreign.name),
            )

        self.assertEqual(invoked, [])
        self.assertEqual(store.read().document_identity, before)
        self.assertNotIn(
            "capability-engine-001", store.read().automation["effective_capabilities"]
        )

    def test_capability_coordination_rejects_identity_drift_before_invocation(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)
        invoked: list[bool] = []

        cases = (
            ({"proposal": "sha256:different-proposal"}, "canonical identity mismatch"),
            ({"standing_gates_identity": "sha256:different-gates"}, "basis input mismatch"),
        )
        for identities, expected in cases:
            with self.subTest(identities=identities), self.assertRaisesRegex(
                AutomationContractError, expected
            ):
                self.coordinate_proposal_review(
                    store,
                    lambda: invoked.append(True),
                    input_identities=identities,
                )

        self.assertEqual(invoked, [])
        self.assertEqual(store.read().automation["transition_receipts"], {})

    def test_capability_coordination_pauses_when_completion_or_sync_is_unproven(self) -> None:
        for label in ("missing-artifact", "stale-artifact", "sync"):
            state = copy.deepcopy(FIXTURES.valid_automation())
            state["effective_capabilities"] = {}
            store = self.make_store(state)
            if label == "missing-artifact":
                missing = ArtifactEvidence(
                    "docs/changes/2026-07-20-example/reviews/missing.md",
                    "sha256:missing",
                )
                invoke = lambda: StageExecutionResult(
                    outputs=(missing,), completion_evidence={"proposal-review": missing}
                )
                synchronize = lambda result: self.synchronize_review(store, result)
            elif label == "stale-artifact":
                def invoke() -> StageExecutionResult:
                    evidence = self.write_evidence(store)
                    stale = ArtifactEvidence(evidence.path, "sha256:stale")
                    return StageExecutionResult(
                        outputs=(stale,),
                        completion_evidence={"proposal-review": stale},
                    )

                synchronize = lambda result: self.synchronize_review(store, result)
            else:
                def invoke() -> StageExecutionResult:
                    evidence = self.write_evidence(store)
                    return StageExecutionResult(
                        outputs=(evidence,),
                        completion_evidence={"proposal-review": evidence},
                    )

                synchronize = lambda result: CanonicalSyncResult(
                    status="failed", evidence=result.completion_evidence
                )
            with self.subTest(label=label), self.assertRaises(AutomationContractError):
                self.coordinate_proposal_review(store, invoke, synchronize=synchronize)
            receipt = store.read().automation["transition_receipts"]["transition-engine-001"]
            self.assertEqual(receipt["status"], "paused")
            self.assertEqual(
                store.read().automation["effective_capabilities"]["capability-engine-001"]["status"],
                "active",
            )

    def test_capability_coordination_rejects_arbitrary_review_bytes(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)

        def invoke() -> StageExecutionResult:
            relative = Path(
                "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md"
            )
            path = store.metadata_path.parent / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("arbitrary bytes; not a formal review\n", encoding="utf-8")
            evidence = ArtifactEvidence(
                relative.as_posix(),
                "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            return StageExecutionResult(
                outputs=(evidence,), completion_evidence={"proposal-review": evidence}
            )

        with self.assertRaisesRegex(
            AutomationContractError, "stage-native|formal review"
        ):
            self.coordinate_proposal_review(store, invoke)

        persisted = store.read().automation
        self.assertEqual(
            persisted["transition_receipts"]["transition-engine-001"]["status"],
            "paused",
        )
        self.assertEqual(
            persisted["effective_capabilities"]["capability-engine-001"]["status"],
            "active",
        )

    def test_capability_coordination_requires_independent_review_log_reread(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)

        def invoke() -> StageExecutionResult:
            evidence = self.write_evidence(store)
            return StageExecutionResult(
                outputs=(evidence,), completion_evidence={"proposal-review": evidence}
            )

        with self.assertRaisesRegex(
            AutomationContractError, "canonical-review-log-missing"
        ):
            self.coordinate_proposal_review(
                store,
                invoke,
                synchronize=lambda result: CanonicalSyncResult(
                    status="synchronized", evidence=result.completion_evidence
                ),
            )

    def test_capability_coordination_rejects_review_target_identity_mismatch(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)
        other = store.repository_root / "docs/proposals/other.md"
        other.parent.mkdir(parents=True, exist_ok=True)
        other.write_text("# Other proposal\n", encoding="utf-8")

        def invoke() -> StageExecutionResult:
            evidence = self.write_evidence(
                store, target="docs/proposals/other.md"
            )
            return StageExecutionResult(
                outputs=(evidence,), completion_evidence={"proposal-review": evidence}
            )

        with self.assertRaisesRegex(
            AutomationContractError, "reviewed-artifact-identity-mismatch"
        ):
            self.coordinate_proposal_review(store, invoke)

    def test_capability_coordination_rejects_unknown_review_outcome(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)

        def invoke() -> StageExecutionResult:
            evidence = self.write_evidence(store, status="rubber-stamp")
            return StageExecutionResult(
                outputs=(evidence,), completion_evidence={"proposal-review": evidence}
            )

        with self.assertRaisesRegex(
            AutomationContractError, "stage-native-review-outcome-invalid"
        ):
            self.coordinate_proposal_review(store, invoke)

    @staticmethod
    def proposal_pre_plan(proposal_identity: str = "sha256:proposal") -> PrePlanEvidence:
        return PrePlanEvidence(
            positions={"proposal": (proposal_identity,)},
            review_outcomes={},
            review_resolution_closed=True,
            architecture_applicability="not-required",
        )

    @staticmethod
    def proposal_input_identities(
        proposal_identity: str = "sha256:proposal",
    ) -> dict[str, object]:
        return {
            "proposal": proposal_identity,
            "proposal_identity": proposal_identity,
            "standing_gates_identity": "sha256:gates",
            "review_policy_identity": "sha256:policy",
            "structured_target_identity": "sha256:target",
            "review_evidence_roots": ["docs/changes/2026-07-20-example/"],
        }

    def synchronize_review(
        self,
        store: WorkflowAutomationStateStore,
        result: StageExecutionResult,
    ) -> CanonicalSyncResult:
        change_root = (
            store.metadata_path.parent / "docs/changes/2026-07-20-example"
        )
        change_root.mkdir(parents=True, exist_ok=True)
        (change_root / "review-log.md").write_text(
            """# Review Log

### Review entry
Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Status: approved
Detailed record: reviews/proposal-review-r1.md
Resolution: none
Material findings: None
Open findings: None
""",
            encoding="utf-8",
        )
        return CanonicalSyncResult(
            status="synchronized",
            evidence=result.completion_evidence,
        )

    @staticmethod
    def write_proposal(store: WorkflowAutomationStateStore) -> str:
        relative = Path("docs/proposals/example.md")
        path = store.metadata_path.parent / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Example proposal\n", encoding="utf-8")
        return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def write_evidence(
        store: WorkflowAutomationStateStore,
        *,
        target: str = "docs/proposals/example.md",
        status: str = "approved",
    ) -> ArtifactEvidence:
        relative = Path("docs/changes/2026-07-20-example/reviews/proposal-review-r1.md")
        path = store.metadata_path.parent / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"""# Proposal review

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: fixture reviewer
Target: {target}
Status: {status}
Material findings: None
""",
            encoding="utf-8",
        )
        identity = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        return ArtifactEvidence(relative.as_posix(), identity)

    def coordinate_proposal_review(
        self,
        store,
        invoke,
        *,
        input_identities=None,
        synchronize=None,
        repository_root=None,
    ):
        proposal_identity = self.write_proposal(store)
        receipt_inputs = self.proposal_input_identities(proposal_identity)
        if input_identities is not None:
            receipt_inputs.update(input_identities)
        return coordinate_one_stage(
            store=store,
            parent_authorization_id="authorization-authoring-001",
            capability_id="capability-engine-001",
            stage="proposal-review",
            occurrence={"kind": "singleton"},
            basis={
                "proposal_identity": proposal_identity,
                "standing_gates_identity": "sha256:gates",
                "review_policy_identity": "sha256:policy",
                "structured_target_identity": "sha256:target",
                "review_evidence_roots": ["docs/changes/2026-07-20-example/"],
            },
            affected_path_roots=("docs/changes/2026-07-20-example/",),
            mutation_categories=("change-local-review-evidence",),
            derived_at="2026-07-22T00:01:00Z",
            transition_id="transition-engine-001",
            input_identities=receipt_inputs,
            invoke_stage=invoke,
            repository_root=repository_root or store.metadata_path.parent,
            pre_plan=self.proposal_pre_plan(proposal_identity),
            synchronize_canonical_state=synchronize
            or (lambda result: self.synchronize_review(store, result)),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
