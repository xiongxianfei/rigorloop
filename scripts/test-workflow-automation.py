#!/usr/bin/env python3
"""Target, position, capability, and one-stage coordinator tests."""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import workflow_automation as workflow_automation_module
from review_artifact_validation import REVIEW_FIX_BUDGET_LIMITS
from workflow_automation import (
    ActivePlanContext,
    ArtifactEvidence,
    AutomationContractError,
    CanonicalSyncResult,
    PrePlanEvidence,
    ProposalCorrectionAuthority,
    StageExecutionResult,
    VerificationReadiness,
    bind_target,
    _compile_implementation_correction_recipe,
    coordinate_one_stage,
    coordinate_non_public_authoring_stage,
    coordinate_non_public_implementation_correction,
    coordinate_non_public_implementation_stage,
    create_parent_authorization,
    derive_effective_capability,
    authorize_proposal_review_invocation,
    evaluate_implementation_correction,
    evaluate_non_public_implementation_route,
    evaluate_non_public_authoring_route,
    evaluate_public_authoring_route,
    evaluate_public_implementation_route,
    evaluate_proposal_correction,
    evaluate_proposal_review,
    execute_public_control_command,
    invalidate_effective_capabilities,
    normalize_command,
    persist_target,
    record_plan_ownership_handoff,
    resolve_canonical_position,
    resolve_command_target,
    resolve_verification_readiness,
    resolve_proposal_correction_authority,
    resume_target,
    start_public_run,
)
from workflow_automation_policy import (
    PUBLIC_TARGET_STAGES,
    STAGE_POLICY_BY_STAGE,
    target_completion_predicate,
)
from workflow_automation_state import (
    StateContractError,
    WorkflowAutomationStateStore,
    dump_yaml,
    evaluate_receipt_recovery,
)
from workflow_code_state import CanonicalCodeState, CodeStateEntry
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


def run_exact_read_only_git_probe(
    command,
    *args,
    expected_root: Path,
    real_popen,
    **kwargs,
) -> subprocess.CompletedProcess:
    """Run only the canonical root-discovery probe allowed by T18."""

    expected_command = (
        "git",
        "-C",
        str(expected_root.resolve()),
        "rev-parse",
        "--show-toplevel",
    )
    expected_keyword_names = {"check", "capture_output", "env"}
    if (
        type(command) is not tuple
        or command != expected_command
        or args
        or set(kwargs) != expected_keyword_names
        or kwargs["check"] is not False
        or kwargs["capture_output"] is not True
        or not isinstance(kwargs["env"], dict)
    ):
        raise AssertionError("prohibited external action was invoked")
    process = real_popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=kwargs["env"],
    )
    stdout, stderr = process.communicate()
    return subprocess.CompletedProcess(
        command,
        process.returncode,
        stdout,
        stderr,
    )


class FixtureCodeStateProvider:
    """Trusted non-Git provider whose path domain is fixture-owned."""

    test_only = True

    def __init__(
        self,
        paths: tuple[str, ...],
        *,
        tail_state: str = "review-recorded",
    ) -> None:
        self.paths = paths
        self.tail_state = tail_state

    def snapshot(self, repository_root: Path) -> CanonicalCodeState:
        entries = tuple(
            CodeStateEntry(
                status="M",
                path=path,
                identity="sha256:"
                + hashlib.sha256(
                    (repository_root / path).read_bytes()
                ).hexdigest(),
            )
            for path in self.paths
        )
        return CanonicalCodeState(
            anchor_identity="sha256:fixture-anchor",
            base_revision="fixture-base",
            reviewed_revision="fixture-reviewed",
            entries=entries,
            final_review_recording_revision=(
                "fixture-review-recording"
                if self.tail_state != "reviewed-subject"
                else None
            ),
            explanation_recording_revision=(
                "fixture-explanation-recording"
                if self.tail_state == "complete"
                else None
            ),
            handoff_revision=(
                "fixture-explanation-recording"
                if self.tail_state == "complete"
                else None
            ),
            tail_state=self.tail_state,
        )


def plan_text(
    *,
    current: str = "M2. Engine Slice",
    current_state: str = "implementing",
    remaining: str = "M2, M3",
    next_stage: str = "implement M2",
    milestone_one_state: str = "closed",
    milestone_two_state: str | None = None,
    milestone_three_state: str = "planned",
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
- Reason final closeout is or is not ready: implementation-milestones-open, verify-pending, pr-handoff-pending — fixture work remains.

## Milestones

### M1. Prior Slice

- Milestone state: {milestone_one_state}

### M2. Engine Slice

- Milestone state: {state}
{duplicate}
### M3. Later Slice

- Milestone state: {milestone_three_state}
"""


class WorkflowAutomationEngineTests(unittest.TestCase):
    def test_only_v3_authoring_progresses_and_test_spec_is_not_a_target(self) -> None:
        decision = evaluate_non_public_authoring_route(
            current_stage="plan",
            target_stage="delivery-review",
            capability_kind="post-proposal-authoring",
            capability_status="active",
            invocation_context="non-public-test-harness",
        )
        self.assertEqual((decision.status, decision.next_stage), ("continue", "delivery-review"))
        with self.assertRaisesRegex(ValueError, "lifecycle_contract: unknown_value"):
            evaluate_non_public_authoring_route(
                current_stage="plan",
                target_stage="delivery-review",
                capability_kind="post-proposal-authoring",
                capability_status="active",
                invocation_context="non-public-test-harness",
                lifecycle_contract="stage-owned-change-local-v2",
            )
        with self.assertRaisesRegex(AutomationContractError, "unknown workflow automation target"):
            bind_target("test-spec", bound_at="2026-07-22T00:00:00Z")

    def test_preserved_implementation_correction_recipe_vocabulary_compiles(self) -> None:
        mechanical_kinds = {
            "formatter-output",
            "lint-autofix",
            "generated-output-refresh",
            "exact-approved-rename",
            "unique-required-field-value",
            "mechanical-state-projection-sync",
            "deterministic-manifest-regeneration",
        }
        authority = json.dumps(
            {
                "operation": "exact-text-replace",
                "path": "scripts/example.py",
                "old": "old_name",
                "new": "new_name",
                "expected_replacements": 1,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        validation = json.dumps(
            {
                "operation": "sha256",
                "path": "scripts/example.py",
                "identity": "sha256:corrected",
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        for kind in mechanical_kinds:
            with self.subTest(kind=kind):
                recipe, operations = _compile_implementation_correction_recipe(
                    "BRF-M5-TEST",
                    {
                        "auto_fix_class": "mechanical",
                        "auto_fix_kind": kind,
                        "affected_paths": "scripts/example.py",
                        "deterministic_authority": authority,
                        "required_validation": validation,
                    },
                )
                self.assertEqual(recipe["auto_fix_kind"], kind)
                self.assertEqual([operation.path for operation in operations], ["scripts/example.py"])

        declared_recipe, declared_operations = _compile_implementation_correction_recipe(
            "BRF-M5-DECLARED",
            {
                "auto_fix_class": "declared-safe",
                "affected_paths": json.dumps(["scripts/example.py"]),
                "resolution_recipe": authority,
                "named_inputs": json.dumps(["scripts/example.py"]),
                "named_outputs": json.dumps(["scripts/example.py"]),
                "forbidden_paths": json.dumps(["specs/", "docs/architecture/"]),
                "acceptance_criteria": json.dumps(["exact reviewed replacement"]),
                "required_validation_commands": validation,
                "scope_preservation_rule": "changed-paths-subset-of-affected-paths",
                "production_code_change": "yes",
                "behavior_test": "T13",
            },
        )
        self.assertEqual(declared_recipe["auto_fix_class"], "declared-safe")
        self.assertEqual(
            [operation.path for operation in declared_operations],
            ["scripts/example.py"],
        )






    def test_target_command_normalization_is_closed_and_old_public_forms_are_rejected(self) -> None:
        current = normalize_command("$route auto: code-review")
        self.assertEqual((current.action, current.target_stage, current.legacy), ("target", "code-review", False))

        target = normalize_command("route auto: verify")
        self.assertEqual((target.action, target.target_stage, target.legacy), ("target", "verify", False))
        self.assertEqual(normalize_command("route auto: status").action, "status")
        self.assertEqual(normalize_command("$route auto: off").action, "off")
        resolved_target = resolve_command_target(
            "$route auto: verify",
            bound_at="2026-07-22T00:00:00Z",
        )
        self.assertEqual(resolved_target["stage"], "verify")
        self.assertEqual(resolved_target["occurrence"]["kind"], "final")

        for command in (
            "route auto: future",
            "$workflow auto: spec",
            "workflow auto-through: verify",
            "route auto-through: spec",
            "auto: verify",
        ):
            with self.subTest(command=command), self.assertRaises(AutomationContractError):
                normalize_command(command)

    def test_public_routes_enter_only_through_the_unified_engine_adapter(self) -> None:
        authoring = evaluate_public_authoring_route(
            command="$route auto: design-review",
            current_stage="spec",
            capability_kind="post-proposal-authoring",
            capability_status="active",
        )
        self.assertEqual(
            (authoring.status, authoring.next_stage),
            ("continue", "design-review"),
        )

        plan = ActivePlanContext.from_text(
            plan_text(
                current_state="review-requested",
                next_stage="code-review M2",
            ),
            plan_identity="sha256:plan-v1",
        )
        implementation = evaluate_public_implementation_route(
            command="$route auto: code-review",
            current_stage="implement",
            capability_kind="implementation",
            capability_status="active",
            active_plan=plan,
            occurrence_kind="milestone",
            target_milestone_id="M2",
            milestone_id="M2",
            milestone_validation_passed=True,
        )
        self.assertEqual(
            (
                implementation.status,
                implementation.next_stage,
                implementation.next_milestone_id,
            ),
            ("continue", "code-review", "M2"),
        )

        legacy = evaluate_public_implementation_route(
            command="route auto: verify",
            current_stage="verify",
            capability_kind="verification",
            capability_status="active",
            active_plan=ActivePlanContext.from_text(
                plan_text(
                    current_state="closed",
                    remaining="None",
                    next_stage="verify",
                    milestone_two_state="closed",
                    milestone_three_state="closed",
                ),
                plan_identity="sha256:plan-v2",
            ),
            occurrence_kind="final",
            verification_authorized=False,
        )
        self.assertEqual(
            (legacy.status, legacy.pause_reason),
            ("paused", "verification-authorization-required"),
        )












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

        with self.assertRaisesRegex(
            AutomationContractError, "duplicate active plan milestone identity"
        ):
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
                "architecture": ("sha256:architecture",),
                "spec": ("sha256:spec",),
                "design-review": ("sha256:design-review",),
            },
            review_outcomes={"proposal-review": "approved", "design-review": "approved"},
            review_resolution_closed=True,
            architecture_applicability="required",
        )

        position = resolve_canonical_position(pre_plan=evidence)

        self.assertEqual(position.position, "design-review")
        self.assertEqual(position.source, "authoritative-artifact-review-evidence")
        self.assertNotIn("current_stage", position.observed_identities)

    def test_position_artifact_sequence_reaches_delivery_review(self) -> None:
        evidence = PrePlanEvidence(
            positions={
                "proposal": ("sha256:proposal",),
                "proposal-review": ("sha256:proposal-review",),
                "architecture": ("sha256:architecture",),
                "spec": ("sha256:spec",),
                "design-review": ("sha256:design-review",),
                "plan": ("sha256:plan",),
                "delivery-review": ("sha256:delivery-review",),
            },
            review_outcomes={
                "proposal-review": "approved",
                "design-review": "approved",
                "delivery-review": "approved",
            },
            review_resolution_closed=True,
            architecture_applicability="required",
        )

        position = resolve_canonical_position(pre_plan=evidence)

        self.assertEqual(position.position, "delivery-review")
        self.assertEqual(
            position.observed_identities["design-review"],
            "sha256:design-review",
        )

    def test_position_active_plan_represents_post_plan_authoring_handoffs(
        self,
    ) -> None:
        cases = (
            ("delivery-review", "plan"),
            ("implement M1", "delivery-review"),
        )
        for next_stage, expected_position in cases:
            with self.subTest(next_stage=next_stage):
                plan = ActivePlanContext.from_text(
                    plan_text(
                        current="M1. Prior Slice",
                        current_state="planned",
                        remaining="M1, M2, M3",
                        next_stage=next_stage,
                        milestone_one_state="planned",
                    ),
                    plan_identity="sha256:plan-v1",
                )

                position = resolve_canonical_position(active_plan=plan)

                self.assertEqual(position.position, expected_position)
                self.assertEqual(position.milestone_id, "M1")

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
                "architecture": ("sha256:architecture",),
                "spec": ("sha256:spec",),
                "design-review": ("sha256:design-review",),
                "plan": ("sha256:plan-artifact",),
            },
            review_outcomes={"proposal-review": "approved", "design-review": "approved"},
            review_resolution_closed=True,
            architecture_applicability="not-required",
        )
        handoff = record_plan_ownership_handoff(pre_plan, plan)
        self.assertEqual(handoff["plan_identity"], "sha256:plan-v1")
        self.assertEqual(handoff["pre_plan_evidence"]["plan"], "sha256:plan-artifact")

        stale = dataclasses.replace(
            pre_plan, stale_identities=frozenset({"sha256:design-review"})
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
        implementation_scope = {
            "review_record_path": "docs/changes/2026-07-20-example/reviews/code-review-m2-r1.md",
            "review_resolution_path": "docs/changes/2026-07-20-example/review-resolution.md",
            "review_log_path": "docs/changes/2026-07-20-example/review-log.md",
            "accepted_finding_ids": ["BRF-M5-CR1"],
            "reviewer_recipes": {
                "BRF-M5-CR1": {
                    "auto_fix_class": "mechanical",
                    "auto_fix_kind": "exact-approved-rename",
                    "affected_paths": ["docs/changes/2026-07-20-example/example.py"],
                    "deterministic_authority": {
                        "operation": "exact-text-replace",
                        "path": "docs/changes/2026-07-20-example/example.py",
                        "old": "old_name",
                        "new": "new_name",
                        "expected_replacements": 1,
                    },
                    "required_validation": {
                        "operation": "sha256",
                        "path": "docs/changes/2026-07-20-example/example.py",
                        "identity": "sha256:corrected",
                    },
                }
            },
            "reviewed_milestone_id": "M2",
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
            implementation_correction_scope=implementation_scope,
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












    def test_proposal_review_outcome_matrix_and_exact_target(self) -> None:
        for outcome in ("approved", "changes-requested", "blocked", "inconclusive"):
            with self.subTest(exact_outcome=outcome):
                exact = evaluate_proposal_review(
                    outcome=outcome,
                    review_id="proposal-review-r1",
                    proposal_identity="sha256:proposal-v1",
                    reviewed_proposal_identity="sha256:proposal-v1",
                    target_stage="proposal-review",
                )
                self.assertTrue(exact.occurrence_recorded)
                self.assertEqual(
                    exact.clean_gate,
                    "satisfied" if outcome == "approved" else "not-satisfied",
                )
                self.assertEqual(
                    exact.routing_action,
                    "pause" if outcome in {"blocked", "inconclusive"} else "stop-at-target",
                )

        approved = evaluate_proposal_review(
            outcome="approved",
            review_id="proposal-review-r1",
            proposal_identity="sha256:proposal-v1",
            reviewed_proposal_identity="sha256:proposal-v1",
            target_stage="architecture",
        )
        self.assertEqual((approved.clean_gate, approved.routing_action), ("satisfied", "continue"))
        self.assertEqual(approved.next_stage, "architecture")

        correction = evaluate_proposal_review(
            outcome="changes-requested",
            review_id="proposal-review-r1",
            proposal_identity="sha256:proposal-v1",
            reviewed_proposal_identity="sha256:proposal-v1",
            target_stage="delivery-review",
            review_record_identity="sha256:review-v1",
            correction_authority=ProposalCorrectionAuthority(
                "capability-correction-001",
                "sha256:review-v1",
                frozenset({"BRF-1"}),
                {"BRF-1": "mechanical"},
                {
                    "Review-fix cycle count": 1,
                    "Findings auto-applied this cycle": 1,
                    "Files changed this cycle": 1,
                    "Files changed this invocation": 1,
                },
                ("docs/proposals/",),
            ),
        )
        self.assertEqual(correction.routing_action, "correction-loop")
        self.assertEqual(correction.next_stage, "proposal-correction")

        empty_budget = evaluate_proposal_review(
            outcome="changes-requested",
            review_id="proposal-review-r1",
            proposal_identity="sha256:proposal-v1",
            reviewed_proposal_identity="sha256:proposal-v1",
            target_stage="delivery-review",
            correction_authority=ProposalCorrectionAuthority(
                "capability-correction-empty",
                "sha256:review-v1",
                frozenset({"BRF-1"}),
                {"BRF-1": "mechanical"},
                {},
                ("docs/proposals/",),
            ),
        )
        self.assertEqual(
            (empty_budget.routing_action, empty_budget.pause_reason),
            ("pause", "proposal-correction-authorization-required"),
        )

        over_budget = evaluate_proposal_review(
            outcome="changes-requested",
            review_id="proposal-review-r1",
            proposal_identity="sha256:proposal-v1",
            reviewed_proposal_identity="sha256:proposal-v1",
            target_stage="delivery-review",
            correction_authority=ProposalCorrectionAuthority(
                "capability-correction-over-budget",
                "sha256:review-v1",
                frozenset({"BRF-1"}),
                {"BRF-1": "mechanical"},
                {
                    label: limit + 1
                    for label, limit in REVIEW_FIX_BUDGET_LIMITS.items()
                },
                ("docs/proposals/",),
            ),
        )
        self.assertEqual(
            (over_budget.routing_action, over_budget.pause_reason),
            ("pause", "proposal-correction-authorization-required"),
        )

        for outcome in ("blocked", "inconclusive"):
            with self.subTest(outcome=outcome):
                decision = evaluate_proposal_review(
                    outcome=outcome,
                    review_id="proposal-review-r1",
                    proposal_identity="sha256:proposal-v1",
                    reviewed_proposal_identity="sha256:proposal-v1",
                    target_stage="spec",
                )
                self.assertTrue(decision.occurrence_recorded)
                self.assertEqual(decision.clean_gate, "not-satisfied")
                self.assertEqual(decision.routing_action, "pause")
                self.assertEqual(decision.pause_reason, f"proposal-review-{outcome}")





    def test_proposal_review_unknown_and_unchanged_inconclusive_fail_closed(self) -> None:
        with self.assertRaisesRegex(AutomationContractError, "unknown proposal-review outcome"):
            evaluate_proposal_review(
                outcome="rubber-stamp",
                review_id="proposal-review-r1",
                proposal_identity="sha256:proposal-v1",
                reviewed_proposal_identity="sha256:proposal-v1",
                target_stage="spec",
            )
        with self.assertRaisesRegex(AutomationContractError, "unchanged inconclusive"):
            authorize_proposal_review_invocation(
                current_basis_identity="sha256:basis-v1",
                previous_inconclusive_basis_identity="sha256:basis-v1",
            )



    def test_proposal_correction_guardrails_and_rereview(self) -> None:
        authority = ProposalCorrectionAuthority(
            "capability-correction-001",
            "sha256:review-v1",
            frozenset({"BRF-1"}),
            {"BRF-1": "mechanical"},
            {
                "Review-fix cycle count": 1,
                "Findings auto-applied this cycle": 1,
                "Files changed this cycle": 1,
                "Files changed this invocation": 1,
            },
            ("docs/proposals/",),
        )
        safe = evaluate_proposal_correction(
            authority=authority,
            finding_classifications={"BRF-1": "mechanical"},
            accepted_finding_ids=("BRF-1",),
            current_finding_ids=("BRF-1",),
            current_review_identity="sha256:review-v1",
            unresolved_before=("BRF-1",),
            unresolved_after=(),
            affected_paths=("docs/proposals/example.md",),
            proposal_identity_before="sha256:proposal-v1",
            proposal_identity_after="sha256:proposal-v2",
            reviewed_finding_classifications={"BRF-1": "mechanical"},
        )
        self.assertEqual(safe.status, "rereview-required")
        self.assertTrue(safe.prior_review_stale)
        self.assertTrue(safe.historical_review_preserved)
        self.assertEqual(safe.next_stage, "proposal-review")

        unsafe_cases = (
            (
                {
                    "authority": dataclasses.replace(
                        authority, finding_classifications={"BRF-1": "not-auto-safe"}
                    ),
                    "finding_classifications": {"BRF-1": "not-auto-safe"},
                    "reviewed_finding_classifications": {"BRF-1": "not-auto-safe"},
                },
                "not-auto-safe",
            ),
            ({"current_finding_ids": ("BRF-1", "BRF-2")}, "finding-set-changed"),
            (
                {"reviewed_finding_classifications": {"BRF-1": "format-preserving"}},
                "finding-classification-changed",
            ),
            ({"unresolved_after": ("BRF-1",)}, "unresolved-findings-did-not-shrink"),
            (
                {
                    "authority": dataclasses.replace(
                        authority,
                        correction_budget={
                            "Review-fix cycle count": 0,
                            "Findings auto-applied this cycle": 1,
                            "Files changed this cycle": 1,
                            "Files changed this invocation": 1,
                        },
                    )
                },
                "correction-budget-exhausted",
            ),
            (
                {
                    "authority": dataclasses.replace(
                        authority,
                        correction_budget={},
                    )
                },
                "correction-budget-invalid",
            ),
            (
                {
                    "authority": dataclasses.replace(
                        authority,
                        correction_budget={
                            **authority.correction_budget,
                            "Unknown budget": 1,
                        },
                    )
                },
                "correction-budget-invalid",
            ),
            (
                {
                    "authority": dataclasses.replace(
                        authority,
                        correction_budget={
                            **authority.correction_budget,
                            "Review-fix cycle count": 3,
                        },
                    )
                },
                "correction-budget-exhausted",
            ),
            ({"current_review_identity": "sha256:review-v2"}, "stale-review-evidence"),
            ({"affected_paths": ("scripts/escape.py",)}, "affected-path-scope-exceeded"),
            ({"scope_expanded": True}, "scope-expanded"),
            ({"owner_decision_required": True}, "owner-decision-required"),
            ({"deterministic_validation_passed": False}, "deterministic-validation-missing"),
        )
        base = {
            "authority": authority,
            "finding_classifications": {"BRF-1": "mechanical"},
            "accepted_finding_ids": ("BRF-1",),
            "current_finding_ids": ("BRF-1",),
            "current_review_identity": "sha256:review-v1",
            "unresolved_before": ("BRF-1",),
            "unresolved_after": (),
            "affected_paths": ("docs/proposals/example.md",),
            "proposal_identity_before": "sha256:proposal-v1",
            "proposal_identity_after": "sha256:proposal-v2",
            "reviewed_finding_classifications": {"BRF-1": "mechanical"},
        }
        for override, reason in unsafe_cases:
            with self.subTest(reason=reason):
                decision = evaluate_proposal_correction(**(base | override))
                self.assertEqual((decision.status, decision.pause_reason), ("paused", reason))





    def test_test_spec_transition_is_not_executable(self) -> None:
        with self.assertRaisesRegex(AutomationContractError, "unknown workflow automation target"):
            bind_target(
                "test-spec",
                bound_at="2026-07-22T00:00:00Z",
            )








    def test_authoring_non_public_harness_routes_through_delivery_review(self) -> None:
        cases = (
            ("proposal-review", "approved", "architecture"),
            ("architecture", None, "spec"),
            ("spec", None, "design-review"),
            ("design-review", "approved", "plan"),
            ("plan", None, "delivery-review"),
        )
        for current_stage, review_outcome, expected in cases:
            with self.subTest(stage=current_stage):
                capability = (
                    "proposal-review" if current_stage == "proposal-review" else "post-proposal-authoring"
                )
                decision = evaluate_non_public_authoring_route(
                    current_stage=current_stage,
                    target_stage="delivery-review",
                    capability_kind=capability,
                    capability_status="active",
                    invocation_context="non-public-test-harness",
                    review_outcome=review_outcome,
                )
                self.assertEqual((decision.status, decision.next_stage), ("continue", expected))

        boundary = evaluate_non_public_authoring_route(
            current_stage="delivery-review",
            target_stage="verify",
            capability_kind="post-proposal-authoring",
            capability_status="active",
            invocation_context="non-public-test-harness",
            review_outcome="approved",
        )
        self.assertEqual(boundary.status, "paused")
        self.assertEqual(boundary.pause_reason, "implementation-authorization-required")

    def test_retired_authoring_review_stages_are_rejected(self) -> None:
        for retired in ("spec-review", "architecture-review", "plan-review", "test-spec-review"):
            with self.subTest(stage=retired), self.assertRaises(AutomationContractError):
                evaluate_non_public_authoring_route(
                    current_stage=retired,
                    target_stage="delivery-review",
                    capability_kind="post-proposal-authoring",
                    capability_status="active",
                    invocation_context="non-public-test-harness",
                    review_outcome="approved",
                )


    def test_implementation_correction_is_reviewer_owned_and_convergent(self) -> None:
        finding = {
            "BRF-M5-2": {
                "auto_fix_class": "mechanical",
                "auto_fix_kind": "formatter-output",
                "affected_paths": ["scripts/example.py"],
                "deterministic_authority": "ruff format",
                "required_validation": "python -m py_compile scripts/example.py",
            }
        }
        authorized = evaluate_implementation_correction(
            findings=finding,
            previous_unresolved={"BRF-M5-1", "BRF-M5-2"},
            current_unresolved={"BRF-M5-1"},
            correction_rounds_completed=0,
            correction_round_cap=2,
            changed_paths={"scripts/example.py"},
            allowed_path_roots=("scripts/",),
            evidence_current=True,
            deterministic_validation_passed=True,
        )
        self.assertEqual(authorized.status, "authorized")

        cases = (
            (
                "missing-class",
                {"BRF-M5-2": {**finding["BRF-M5-2"], "auto_fix_class": ""}},
                {"BRF-M5-1", "BRF-M5-2"},
                {"BRF-M5-1"},
                {"scripts/example.py"},
                True,
                True,
                "finding-not-auto-fixable",
            ),
            (
                "new-finding",
                finding,
                {"BRF-M5-2"},
                {"BRF-M5-1"},
                {"scripts/example.py"},
                True,
                True,
                "new-finding-or-class",
            ),
            (
                "non-shrinking",
                finding,
                {"BRF-M5-1"},
                {"BRF-M5-1"},
                {"scripts/example.py"},
                True,
                True,
                "unresolved-findings-did-not-shrink",
            ),
            (
                "scope-expansion",
                finding,
                {"BRF-M5-1", "BRF-M5-2"},
                {"BRF-M5-1"},
                {"docs/architecture/system/architecture.md"},
                True,
                True,
                "correction-path-out-of-scope",
            ),
            (
                "stale-evidence",
                finding,
                {"BRF-M5-1", "BRF-M5-2"},
                {"BRF-M5-1"},
                {"scripts/example.py"},
                False,
                True,
                "review-evidence-stale",
            ),
            (
                "missing-validation",
                finding,
                {"BRF-M5-1", "BRF-M5-2"},
                {"BRF-M5-1"},
                {"scripts/example.py"},
                True,
                False,
                "deterministic-validation-missing",
            ),
        )
        for (
            label,
            findings,
            previous,
            current,
            changed,
            evidence_current,
            validation_passed,
            reason,
        ) in cases:
            with self.subTest(case=label):
                decision = evaluate_implementation_correction(
                    findings=findings,
                    previous_unresolved=previous,
                    current_unresolved=current,
                    correction_rounds_completed=0,
                    correction_round_cap=2,
                    changed_paths=changed,
                    allowed_path_roots=("scripts/",),
                    evidence_current=evidence_current,
                    deterministic_validation_passed=validation_passed,
                )
                self.assertEqual((decision.status, decision.pause_reason), ("paused", reason))
        unknown_class = evaluate_implementation_correction(
            findings={
                "BRF-M5-2": {
                    **finding["BRF-M5-2"],
                    "auto_fix_class": "future-class",
                }
            },
            previous_unresolved={"BRF-M5-1", "BRF-M5-2"},
            current_unresolved={"BRF-M5-1"},
            correction_rounds_completed=0,
            correction_round_cap=2,
            changed_paths={"scripts/example.py"},
            allowed_path_roots=("scripts/",),
            evidence_current=True,
            deterministic_validation_passed=True,
        )
        self.assertEqual(unknown_class.pause_reason, "unknown-auto-fix-class")
        changed_class = evaluate_implementation_correction(
            findings=finding,
            previous_unresolved={"BRF-M5-1", "BRF-M5-2"},
            current_unresolved={"BRF-M5-1"},
            correction_rounds_completed=0,
            correction_round_cap=2,
            changed_paths={"scripts/example.py"},
            allowed_path_roots=("scripts/",),
            evidence_current=True,
            deterministic_validation_passed=True,
            previous_classifications={"BRF-M5-2": "declared-safe"},
        )
        self.assertEqual(changed_class.pause_reason, "new-finding-or-class")


    def test_active_plan_rejects_duplicate_milestone_identity(self) -> None:
        with self.assertRaisesRegex(
            AutomationContractError, "duplicate active plan milestone"
        ):
            ActivePlanContext.from_text(
                plan_text(duplicate_m2=True),
                plan_identity="sha256:duplicate-plan",
            )

    def test_implementation_milestones_and_reviews_remain_ordered_and_distinct(self) -> None:
        implementing = ActivePlanContext.from_text(
            plan_text(
                current="M2. Engine Slice",
                current_state="review-requested",
                remaining="M2, M3",
                next_stage="code-review M2",
            ),
            plan_identity="sha256:plan-m2-review",
        )
        validation_failure = evaluate_non_public_implementation_route(
            current_stage="implement",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="implementation",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="milestone",
            milestone_id="M2",
            active_plan=implementing,
            milestone_validation_passed=False,
        )
        self.assertEqual(
            (validation_failure.status, validation_failure.pause_reason),
            ("paused", "milestone-validation-failed"),
        )
        implementation_complete = evaluate_non_public_implementation_route(
            current_stage="implement",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="implementation",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="milestone",
            milestone_id="M2",
            active_plan=implementing,
            milestone_validation_passed=True,
        )
        self.assertEqual(
            (implementation_complete.status, implementation_complete.next_stage),
            ("continue", "code-review"),
        )
        self.assertEqual(implementation_complete.next_milestone_id, "M2")

        reviewed = ActivePlanContext.from_text(
            plan_text(
                current="M3. Later Slice",
                current_state="planned",
                remaining="M3",
                next_stage="implement M3",
                milestone_two_state="closed",
            ),
            plan_identity="sha256:plan-m3",
        )
        open_resolution = evaluate_non_public_implementation_route(
            current_stage="code-review",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="implementation",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="milestone",
            milestone_id="M2",
            active_plan=reviewed,
            review_outcome="approved",
            review_resolution_closed=False,
        )
        self.assertEqual(open_resolution.pause_reason, "review-resolution-open")
        review_complete = evaluate_non_public_implementation_route(
            current_stage="code-review",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="implementation",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="milestone",
            milestone_id="M2",
            active_plan=reviewed,
            review_outcome="approved",
            review_resolution_closed=True,
        )
        self.assertEqual(
            (
                review_complete.status,
                review_complete.next_stage,
                review_complete.next_milestone_id,
            ),
            ("continue", "implement", "M3"),
        )



    def test_verify_integration_requires_holistic_closeout_and_stops_before_pr(self) -> None:
        closed_plan = ActivePlanContext.from_text(
            plan_text(
                current="M3. Later Slice",
                current_state="closed",
                remaining="M3",
                next_stage="final-holistic-code-review",
                milestone_two_state="closed",
                milestone_three_state="closed",
            ),
            plan_identity="sha256:closed-plan",
        )
        missing_authority = evaluate_non_public_implementation_route(
            current_stage="final-holistic-code-review",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="implementation",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="final",
            active_plan=closed_plan,
            review_outcome="approved",
            review_resolution_closed=True,
            verification_authorized=False,
        )
        self.assertEqual(
            (missing_authority.status, missing_authority.pause_reason),
            ("paused", "verification-authorization-required"),
        )
        failed = evaluate_non_public_implementation_route(
            current_stage="verify",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="verification",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="final",
            active_plan=closed_plan,
            verification_passed=False,
            verification_authorized=True,
            final_review_clean=True,
        )
        self.assertEqual((failed.status, failed.pause_reason), ("paused", "verification-failed"))
        self.assertFalse(failed.automatic_repair)

        passed = evaluate_non_public_implementation_route(
            current_stage="verify",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="verification",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="final",
            active_plan=closed_plan,
            verification_passed=True,
            verification_authorized=True,
            final_review_clean=True,
        )
        self.assertEqual((passed.status, passed.next_stage), ("target-reached", "pr"))
        self.assertFalse(passed.external_action_performed)

    def test_v3_routes_final_review_directly_to_verify_without_explanation_prerequisite(self) -> None:
        closed_plan = ActivePlanContext.from_text(
            plan_text(
                current="M3. Later Slice",
                current_state="closed",
                remaining="M3",
                next_stage="final-holistic-code-review",
                milestone_two_state="closed",
                milestone_three_state="closed",
            ),
            plan_identity="sha256:closed-plan",
        )
        routed = evaluate_non_public_implementation_route(
            current_stage="final-holistic-code-review",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="implementation",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="final",
            active_plan=closed_plan,
            review_outcome="approved",
            review_resolution_closed=True,
            verification_authorized=True,
            lifecycle_contract="stage-owned-change-local-v3",
        )
        self.assertEqual((routed.status, routed.next_stage), ("continue", "verify"))
        passed = evaluate_non_public_implementation_route(
            current_stage="verify",
            target_stage="verify",
            target_milestone_id=None,
            capability_kind="verification",
            capability_status="active",
            invocation_context="non-public-test-harness",
            occurrence_kind="final",
            active_plan=closed_plan,
            verification_passed=True,
            verification_authorized=True,
            final_review_clean=True,
            lifecycle_contract="stage-owned-change-local-v3",
        )
        self.assertEqual((passed.status, passed.next_stage), ("target-reached", "pr"))
        with self.assertRaisesRegex(AutomationContractError, "explain-change"):
            evaluate_non_public_implementation_route(
                current_stage="explain-change",
                target_stage="verify",
                target_milestone_id=None,
                capability_kind="verification",
                capability_status="active",
                invocation_context="non-public-test-harness",
                occurrence_kind="final",
                active_plan=closed_plan,
                verification_authorized=True,
                lifecycle_contract="stage-owned-change-local-v3",
            )
        expected_routes = {
            "system-requirement-gap": ("spec", "design-review"),
            "technical-realization-gap": ("architecture", "design-review"),
            "verification-allocation-gap": ("plan", "delivery-review"),
            "implementation-defect": ("implement", "code-review"),
            "stale-or-incomplete-review": ("code-review", "code-review"),
            "ci-or-environment-gap": ("ci-maintenance", "verify"),
            "external-evidence-gap": ("external-evidence-acquisition", "verify"),
        }
        for finding_kind, expected in expected_routes.items():
            routed_finding = evaluate_non_public_implementation_route(
                current_stage="verify",
                target_stage="verify",
                target_milestone_id=None,
                capability_kind="verification",
                capability_status="active",
                invocation_context="non-public-test-harness",
                occurrence_kind="final",
                active_plan=closed_plan,
                verification_passed=False,
                verification_finding_kind=finding_kind,
                verification_authorized=True,
                final_review_clean=True,
                lifecycle_contract="stage-owned-change-local-v3",
            )
            self.assertEqual(
                (routed_finding.status, routed_finding.next_stage, routed_finding.return_stage),
                ("correction-loop", *expected),
            )
            self.assertFalse(routed_finding.automatic_repair)
        with self.assertRaisesRegex(ValueError, "unknown_value"):
            evaluate_non_public_implementation_route(
                current_stage="verify",
                target_stage="verify",
                target_milestone_id=None,
                capability_kind="verification",
                capability_status="active",
                invocation_context="non-public-test-harness",
                occurrence_kind="final",
                active_plan=closed_plan,
                verification_passed=False,
                verification_finding_kind="future-gap",
                verification_authorized=True,
                final_review_clean=True,
                lifecycle_contract="stage-owned-change-local-v3",
            )

    def test_verify_git_probe_allowlist_is_exact_and_root_bound(self) -> None:
        repository_root = Path("/canonical/repository")
        expected_command = (
            "git",
            "-C",
            str(repository_root),
            "rev-parse",
            "--show-toplevel",
        )
        popen_calls: list[tuple[str, ...]] = []

        class FakeProcess:
            returncode = 0

            @staticmethod
            def communicate() -> tuple[bytes, bytes]:
                return b"/canonical/repository\n", b""

        def fake_popen(command, **_kwargs):
            popen_calls.append(command)
            return FakeProcess()

        class EqualitySpoofingTuple(tuple):
            def __eq__(self, _other) -> bool:
                return True

            def __ne__(self, _other) -> bool:
                return False

        result = run_exact_read_only_git_probe(
            expected_command,
            expected_root=repository_root,
            real_popen=fake_popen,
            check=False,
            capture_output=True,
            env={"LC_ALL": "C", "LANG": "C"},
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(popen_calls, [expected_command])

        rejected_commands = (
            (
                "git",
                "-C",
                "/alternate/repository",
                "rev-parse",
                "--show-toplevel",
            ),
            (
                "git",
                "-C",
                str(repository_root),
                "push",
                "origin",
                "HEAD",
                "rev-parse",
                "--show-toplevel",
            ),
            ("env", *expected_command),
            (*expected_command, "--extra"),
            list(expected_command),
            "git -C /canonical/repository rev-parse --show-toplevel",
            EqualitySpoofingTuple(
                (
                    "git",
                    "-C",
                    str(repository_root),
                    "push",
                    "origin",
                    "HEAD",
                )
            ),
        )
        for command in rejected_commands:
            with self.subTest(command=command), self.assertRaisesRegex(
                AssertionError, "prohibited external action"
            ):
                run_exact_read_only_git_probe(
                    command,
                    expected_root=repository_root,
                    real_popen=fake_popen,
                    check=False,
                    capture_output=True,
                    env={"LC_ALL": "C", "LANG": "C"},
                )

        with self.assertRaisesRegex(
            AssertionError, "prohibited external action"
        ):
            run_exact_read_only_git_probe(
                expected_command,
                expected_root=repository_root,
                real_popen=fake_popen,
                check=False,
                capture_output=True,
                env={"LC_ALL": "C", "LANG": "C"},
                shell=True,
            )
        self.assertEqual(popen_calls, [expected_command])

    def test_verify_git_probe_rejects_before_custom_comparison(self) -> None:
        comparison_calls: list[tuple[str, ...]] = []

        class ComparisonSentinel:
            def __eq__(self, other) -> bool:
                comparison_calls.append(("eq", *other))
                return False

            def __ne__(self, other) -> bool:
                comparison_calls.append(("ne", *other))
                return True

        def prohibited_popen(*_args, **_kwargs):
            raise AssertionError("saved launcher was invoked")

        with self.assertRaisesRegex(
            AssertionError, "prohibited external action"
        ):
            run_exact_read_only_git_probe(
                ComparisonSentinel(),
                expected_root=Path("/canonical/repository"),
                real_popen=prohibited_popen,
                check=False,
                capture_output=True,
                env={"LC_ALL": "C", "LANG": "C"},
            )
        self.assertEqual(comparison_calls, [])




    def test_implementation_non_public_harness_rejects_every_public_entry(self) -> None:
        closed_plan = ActivePlanContext.from_text(
            plan_text(
                current="M3. Later Slice",
                current_state="closed",
                remaining="M3",
                next_stage="final-holistic-code-review",
                milestone_two_state="closed",
                milestone_three_state="closed",
            ),
            plan_identity="sha256:closed-plan",
        )
        for context in ("public-command", "direct-skill", "bugfix", "legacy-adapter"):
            with self.subTest(context=context):
                decision = evaluate_non_public_implementation_route(
                    current_stage="verify",
                    target_stage="verify",
                    target_milestone_id=None,
                    capability_kind="verification",
                    capability_status="active",
                    invocation_context=context,
                    occurrence_kind="final",
                    active_plan=closed_plan,
                    verification_passed=True,
                    verification_authorized=True,
                )
                self.assertEqual(
                    (decision.status, decision.pause_reason),
                    ("paused", "non-public-harness-required"),
                )

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



if __name__ == "__main__":
    unittest.main(verbosity=2)
