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

    def __init__(self, paths: tuple[str, ...]) -> None:
        self.paths = paths

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
- Reason final closeout is or is not ready: implementation-milestones-open, explain-change-pending, verify-pending, pr-handoff-pending — fixture work remains.

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

    def write_plan_state_owner(
        self,
        store: WorkflowAutomationStateStore,
        *,
        plan_path: str,
        milestone_id: str,
        milestone_state: str,
    ) -> None:
        metadata = (
            store.repository_root
            / "docs/changes/2026-07-20-plan-state/change.yaml"
        )
        metadata.parent.mkdir(parents=True, exist_ok=True)
        metadata.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-plan-state",
                    "lifecycle_contract": "stage-owned-change-local-v1",
                    "artifact_states": {
                        "plan": {
                            "kind": "plan",
                            "path": plan_path,
                            "role": "primary",
                            "lifecycle_state": "active",
                        }
                    },
                    "workflow_state": {
                        "planned_work": {
                            "milestones": {
                                milestone_id: {
                                    "kind": "implementation",
                                    "state": milestone_state,
                                }
                            }
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    def write_verification_readiness_evidence(
        self,
        store: WorkflowAutomationStateStore,
    ) -> tuple[dict[str, str], dict[str, str], FixtureCodeStateProvider]:
        root = store.repository_root

        def artifact(relative: str, content: str) -> tuple[str, str]:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return (
                relative,
                "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
            )

        source_path, _source_identity = artifact(
            "scripts/final-code.py",
            "final_value = 1\n",
        )
        provider = FixtureCodeStateProvider((source_path,))
        code_state = provider.snapshot(root)
        plan_path, plan_identity = artifact(
            "docs/plans/closed.md",
            plan_text(
                current="M3. Later Slice",
                current_state="closed",
                remaining="M3",
                next_stage="verify",
                milestone_two_state="closed",
                milestone_three_state="closed",
            ),
        )
        review_path, review_identity = artifact(
            "docs/changes/2026-07-20-example/reviews/code-review-final-r1.md",
            f"""# Final code review

Review ID: code-review-final-r1
Stage: code-review
Round: final R1
Reviewer: fixture reviewer
Target: final implementation
Status: approved
Material findings: None
Review scope: final-holistic
complete_final_diff: reviewed
cross_milestone_interactions: reviewed
governing_artifacts: reviewed
review_resolutions: closed
final_validation_selection: reviewed
generated_and_derived_artifacts: current
cross_milestone_scope: reviewed
Reviewed commit: fixture-reviewed
Final code identity: {code_state.identity}
""",
        )
        artifact(
            "docs/changes/2026-07-20-example/review-log.md",
            """# Review Log

### Review entry
Review ID: code-review-final-r1
Stage: code-review
Round: final R1
Status: approved
Detailed record: reviews/code-review-final-r1.md
Resolution: none
Material findings: None
Open findings: None
""",
        )
        explanation_path, explanation_identity = artifact(
            "docs/changes/2026-07-20-example/explain-change.md",
            "Stage: explain-change\nStatus: current\n"
            f"Final diff identity: {code_state.identity}\n"
            f"Final review identity: {review_identity}\n"
            f"Reviewed subject revision: {code_state.reviewed_revision}\n"
            "Explanation basis: sha256:explanation-basis\n"
            "Validation-evidence cutoff: sha256:validation-cutoff\n",
        )
        promotion_path, promotion_identity = artifact(
            "docs/changes/2026-07-20-example/promotion-evidence.md",
            "Stage: promotion\nStatus: valid\n"
            f"Final code identity: {code_state.identity}\n",
        )
        branch_path, branch_identity = artifact(
            "docs/changes/2026-07-20-example/branch-state.md",
            "Stage: branch-state\nStatus: current\n"
            f"Final code identity: {code_state.identity}\n"
            f"Final code paths: {json.dumps([source_path])}\n"
            f"Final code anchor identity: {code_state.anchor_identity}\n"
            f"Final code base revision: {code_state.base_revision}\n"
            f"Final code reviewed revision: {code_state.reviewed_revision}\n",
        )
        commands_path, commands_identity = artifact(
            "docs/changes/2026-07-20-example/verification-commands.md",
            "Stage: verification-commands\nStatus: current\n"
            f"Final code identity: {code_state.identity}\n",
        )
        basis = {
            "closed_milestones_identity": plan_identity,
            "final_code_review_identity": review_identity,
            "promotion_evidence_identity": promotion_identity,
            "explanation_inputs_identity": explanation_identity,
            "branch_state_identity": branch_identity,
            "verification_commands_identity": commands_identity,
        }
        paths = {
            "closed_milestones_identity": plan_path,
            "final_code_review_identity": review_path,
            "promotion_evidence_identity": promotion_path,
            "explanation_inputs_identity": explanation_path,
            "branch_state_identity": branch_path,
            "verification_commands_identity": commands_path,
        }
        return basis, paths, provider

    def write_proposal_correction_evidence(
        self,
        store: WorkflowAutomationStateStore,
        *,
        proposal_path: str,
    ) -> tuple[str, str, str]:
        change_root = (
            store.repository_root / "docs/changes/2026-07-20-example"
        )
        review_relative = (
            "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md"
        )
        review = store.repository_root / review_relative
        review.parent.mkdir(parents=True, exist_ok=True)
        review.write_text(
            f"""# Proposal review

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: fixture reviewer
Target: {proposal_path}
Status: changes-requested
Material findings: BRF-1

## Material Findings

### BRF-1 - Fixture correction

Finding ID: BRF-1
Severity: major
Location: proposal
Evidence: fixture evidence
Required outcome: apply the deterministic fixture correction
Safe resolution path: update the proposal and rerun review
auto_fix_class: none
""",
            encoding="utf-8",
        )
        (change_root / "review-log.md").write_text(
            """# Review Log

### Review entry
Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Status: changes-requested
Detailed record: reviews/proposal-review-r1.md
Resolution: review-resolution.md#proposal-review-r1
Material findings: BRF-1
Open findings: BRF-1
""",
            encoding="utf-8",
        )
        resolution_relative = (
            "docs/changes/2026-07-20-example/review-resolution.md"
        )
        (store.repository_root / resolution_relative).write_text(
            """# Review Resolution

Closeout status: open
Review closeout: proposal-review-r1

### proposal-review-r1

Finding ID: BRF-1
Disposition: accepted
Status: open
Owner: fixture owner
Owning stage: review-resolution
Rationale: deterministic fixture correction
Chosen action: apply the correction
Validation target: rereview
Planned driver classification: mechanical
Planned correction rationale: The requested change is deterministic and bounded.
Planned correction recipe: Append one newline to the reviewed proposal.
Planned validation rule: proposal-exact-append
""",
            encoding="utf-8",
        )
        identity = "sha256:" + hashlib.sha256(review.read_bytes()).hexdigest()
        return review_relative, resolution_relative, identity

    def prepare_proposal_correction_transaction(
        self,
        *,
        transition_id: str,
        allow_rereview: bool = True,
        store: WorkflowAutomationStateStore | None = None,
        public_authorization: bool = False,
    ) -> dict[str, object]:
        accepted = ["BRF-1"]
        classifications = {"BRF-1": "mechanical"}
        correction_plans = {
            "BRF-1": {
                "classification": "mechanical",
                "rationale": "The requested change is deterministic and bounded.",
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
        identity = lambda value: "sha256:" + hashlib.sha256(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        target = bind_target("spec", bound_at="2026-07-22T00:00:00Z")
        allowed_kinds = (
            ("proposal-correction", "proposal-review")
            if allow_rereview
            else ("proposal-correction",)
        )
        maximum_roots = (
            (
                "docs/proposals/",
                "docs/changes/2026-07-20-example/",
            )
            if allow_rereview
            else ("docs/proposals/",)
        )
        maximum_categories = (
            ("proposal-content", "change-local-review-evidence")
            if allow_rereview
            else ("proposal-content",)
        )
        parent = create_parent_authorization(
            authorization_id="auth-correction",
            authorization_class="authoring",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=allowed_kinds,
            maximum_path_roots=maximum_roots,
            maximum_mutation_categories=maximum_categories,
            correction_budget=budget,
        )
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["run"]["target"] = target
        state["parent_authorizations"] = {"auth-correction": parent}
        state["effective_capabilities"] = {}
        state["transition_receipts"] = {}
        state["observed_identities"] = {}
        if store is None:
            store = self.make_store(state)
        elif not public_authorization:
            snapshot = store.read()
            store.replace_automation(
                state,
                expected_document_identity=snapshot.document_identity,
            )
        relative = Path("docs/proposals/2026-07-20-example.md")
        proposal = store.repository_root / relative
        proposal.parent.mkdir(parents=True, exist_ok=True)
        proposal.write_text(
            (ROOT / "docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md").read_text(),
            encoding="utf-8",
        )
        proposal_before = "sha256:" + hashlib.sha256(proposal.read_bytes()).hexdigest()
        review_path, resolution_path, review_identity = (
            self.write_proposal_correction_evidence(
                store,
                proposal_path=relative.as_posix(),
            )
        )
        if public_authorization:
            start_public_run(
                store,
                "$workflow auto: spec",
                run_id="run-correction",
                actor="user",
                occurred_at="2026-07-22T00:00:00Z",
                pre_plan=PrePlanEvidence(
                    positions={
                        "proposal": (proposal_before,),
                        "proposal-review": (review_identity,),
                    },
                    review_outcomes={
                        "proposal-review": "changes-requested"
                    },
                    review_resolution_closed=True,
                    architecture_applicability="not-required",
                ),
                proposal_correction_budget=budget,
            )
            state = store.read()
            parent_authorization_id = "authorization-authoring-run-correction"
            parent = state.automation["parent_authorizations"][
                parent_authorization_id
            ]
        else:
            state = store.read()
            replacement = copy.deepcopy(state.automation)
            replacement["observed_identities"] = {
                "proposal": proposal_before,
                "proposal-review": review_identity,
            }
            store.replace_automation(
                replacement,
                expected_document_identity=state.document_identity,
            )
            parent_authorization_id = "auth-correction"
        budget_identity = identity(budget)
        basis = {
            "reviewed_proposal_identity": proposal_before,
            "review_record_identity": review_identity,
            "accepted_finding_set_identity": identity(accepted),
            "classifier_policy_identity": identity(correction_plans),
            "correction_budget_identity": budget_identity,
            "affected_proposal_roots": ["docs/proposals/"],
        }
        capability = derive_effective_capability(
            capability_id="cap-correction-transaction",
            parent=parent,
            stage="proposal",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("docs/proposals/",),
            mutation_categories=("proposal-content",),
            correction_budget=budget,
            correction_budget_identity=budget_identity,
            derived_at="2026-07-22T00:01:00Z",
        )
        capability["scope"].update(
            {
                "review_record_path": review_path,
                "review_resolution_path": resolution_path,
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
        # This capability represents stage-owned review/classification evidence.
        # The user-facing target and parent consent above enter through the
        # public command adapter when public_authorization is requested.
        replacement = store.read().automation
        replacement["effective_capabilities"] = {
            capability["capability_id"]: capability
        }
        store.replace_automation(
            replacement,
            expected_document_identity=store.read().document_identity,
        )
        inputs = dict(
            basis,
            proposal=proposal_before,
            **{
                "proposal-review": review_identity,
                "review_outcome": "changes-requested",
                "review_identity": review_identity,
                "accepted_finding_set_identity": identity(accepted),
                "correction_budget_state": "remaining",
                "correction_budget_identity": budget_identity,
            },
        )
        return {
            "store": store,
            "proposal": proposal,
            "proposal_relative": relative,
            "review_path": review_path,
            "resolution_path": resolution_path,
            "coordination": {
                "invocation_context": "non-public-test-harness",
                "target_stage": "spec",
                "store": store,
                "repository_root": store.repository_root,
                "parent_authorization_id": parent_authorization_id,
                "capability_id": "cap-correction-transaction",
                "stage": "proposal",
                "occurrence": {"kind": "singleton"},
                "basis": basis,
                "affected_path_roots": ("docs/proposals/",),
                "mutation_categories": ("proposal-content",),
                "derived_at": "2026-07-22T00:01:00Z",
                "transition_id": transition_id,
                "input_identities": inputs,
                "synchronize_canonical_state": lambda stage_result: CanonicalSyncResult(
                    "synchronized", stage_result.completion_evidence
                ),
                "pre_plan": PrePlanEvidence(
                    positions={
                        "proposal": (proposal_before,),
                        "proposal-review": (review_identity,),
                    },
                    review_outcomes={
                        "proposal-review": "changes-requested"
                    },
                    review_resolution_closed=True,
                    architecture_applicability="not-required",
                ),
            },
        }

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

    def test_public_routes_enter_only_through_the_unified_engine_adapter(self) -> None:
        authoring = evaluate_public_authoring_route(
            command="$workflow auto: spec-review",
            current_stage="spec",
            capability_kind="post-proposal-authoring",
            capability_status="active",
        )
        self.assertEqual(
            (authoring.status, authoring.next_stage),
            ("continue", "spec-review"),
        )

        plan = ActivePlanContext.from_text(
            plan_text(
                current_state="review-requested",
                next_stage="code-review M2",
            ),
            plan_identity="sha256:plan-v1",
        )
        implementation = evaluate_public_implementation_route(
            command="$workflow auto: code-review",
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
            command="workflow auto-through: verify",
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

    def test_public_status_and_off_use_the_unified_state_store(self) -> None:
        state = FIXTURES.valid_automation()
        store = self.make_store(state)
        before = store.metadata_path.read_bytes()

        status = execute_public_control_command(
            store,
            "$workflow auto: status",
            actor="user",
            occurred_at="2026-07-24T00:00:00Z",
        )
        self.assertEqual(status["mechanism"], "bounded-review-fix")
        self.assertEqual(status["stage_outcome"], "status")
        self.assertEqual(before, store.metadata_path.read_bytes())

        cancelled = execute_public_control_command(
            store,
            "workflow auto-through: off",
            actor="user",
            occurred_at="2026-07-24T00:01:00Z",
        )
        self.assertEqual(cancelled["stage_outcome"], "cancelled")
        self.assertEqual(cancelled["stop_reason"], "run-cancelled")
        self.assertEqual(store.read().automation["run"]["status"], "cancelled")
        self.assertNotIn("autoprogression", store.read().document["workflow"])

        repeated = execute_public_control_command(
            store,
            "$workflow auto: off",
            actor="user",
            occurred_at="2026-07-24T00:02:00Z",
        )
        self.assertEqual(repeated["stage_outcome"], "cancelled")

    def test_public_target_creation_is_single_write_and_risk_bounded(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "change.yaml"
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Public cutover fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(path)

        started = start_public_run(
            store,
            "workflow auto-through: plan-review",
            run_id="run-public-001",
            actor="user",
            occurred_at="2026-07-24T00:00:00Z",
            pre_plan=PrePlanEvidence(
                positions={"proposal": ("sha256:proposal",)},
                review_outcomes={},
                review_resolution_closed=True,
                architecture_applicability="not-required",
            ),
            proposal_correction_budget=REVIEW_FIX_BUDGET_LIMITS,
        )
        state = store.read()
        self.assertEqual(started["structured_target"]["stage"], "plan-review")
        self.assertEqual(
            started["canonical_position_source"],
            "authoritative-artifact-review-evidence",
        )
        self.assertEqual(
            started["latest_evidence_identities"],
            {"proposal": "sha256:proposal"},
        )
        self.assertEqual(started["transitions_attempted"], [])
        self.assertEqual(started["artifacts_changed"], [])
        self.assertEqual(state.automation["mechanism"], "bounded-review-fix")
        self.assertEqual(
            [
                parent["authorization_class"]
                for parent in state.automation["parent_authorizations"].values()
            ],
            ["authoring"],
        )
        authoring_parent = next(
            iter(state.automation["parent_authorizations"].values())
        )
        self.assertEqual(
            authoring_parent["allowed_capability_kinds"],
            [
                "proposal-review",
                "proposal-correction",
                "post-proposal-authoring",
            ],
        )
        self.assertEqual(
            authoring_parent["correction_budget"],
            REVIEW_FIX_BUDGET_LIMITS,
        )
        self.assertEqual(state.automation["effective_capabilities"], {})
        self.assertNotIn("autoprogression", state.document["workflow"])

        with self.assertRaisesRegex(
            AutomationContractError, "active writable automation run"
        ):
            start_public_run(
                store,
                "$workflow auto: verify",
                run_id="run-public-002",
                actor="user",
                occurred_at="2026-07-24T00:01:00Z",
                pre_plan=PrePlanEvidence(
                    positions={"proposal": ("sha256:proposal",)},
                    review_outcomes={},
                    review_resolution_closed=True,
                    architecture_applicability="not-required",
                ),
            )

        verify_temp = tempfile.TemporaryDirectory()
        self.addCleanup(verify_temp.cleanup)
        verify_path = Path(verify_temp.name) / "change.yaml"
        verify_path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Verify alias fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        verify_store = WorkflowAutomationStateStore(verify_path)
        start_public_run(
            verify_store,
            "workflow auto-through: verify",
            run_id="run-public-verify",
            actor="user",
            occurred_at="2026-07-24T00:03:00Z",
            pre_plan=PrePlanEvidence(
                positions={"proposal": ("sha256:proposal",)},
                review_outcomes={},
                review_resolution_closed=True,
                architecture_applicability="not-required",
            ),
        )
        verify_state = verify_store.read().automation
        self.assertEqual(verify_state["run"]["target"]["stage"], "verify")
        self.assertEqual(verify_state["run"]["target"]["occurrence"]["kind"], "final")
        self.assertEqual(verify_state["parent_authorizations"], {})
        self.assertEqual(verify_state["effective_capabilities"], {})

        basis_temp = tempfile.TemporaryDirectory()
        self.addCleanup(basis_temp.cleanup)
        basis_path = Path(basis_temp.name) / "change.yaml"
        basis_path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Basis-valid verify alias fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        basis_store = WorkflowAutomationStateStore(basis_path)
        implementation_basis = {
            "plan_identity": "sha256:plan",
            "plan_review_identity": "sha256:plan-review",
            "test_spec_identity": "sha256:test-spec",
            "test_spec_review_identity": "sha256:test-spec-review",
            "milestone_identity": "sha256:M1",
            "affected_paths_identity": "sha256:paths",
            "mutation_categories_identity": "sha256:categories",
            "validation_commands_identity": "sha256:commands",
        }
        start_public_run(
            basis_store,
            "workflow auto-through: verify",
            run_id="run-public-basis",
            actor="user",
            occurred_at="2026-07-24T00:04:00Z",
            pre_plan=PrePlanEvidence(
                positions={"proposal": ("sha256:proposal",)},
                review_outcomes={},
                review_resolution_closed=True,
                architecture_applicability="not-required",
            ),
            implementation_basis=implementation_basis,
            implementation_path_roots=("scripts/", "tests/"),
            implementation_correction_budget={"cycles": 1},
        )
        basis_state = basis_store.read().automation
        self.assertEqual(
            [
                parent["authorization_class"]
                for parent in basis_state["parent_authorizations"].values()
            ],
            ["implementation"],
        )
        implementation_parent = next(
            iter(basis_state["parent_authorizations"].values())
        )
        self.assertEqual(
            implementation_parent["allowed_capability_kinds"],
            ["implementation", "implementation-correction"],
        )
        self.assertNotIn(
            "verification",
            [
                parent["authorization_class"]
                for parent in basis_state["parent_authorizations"].values()
            ],
        )
        with self.assertRaisesRegex(
            AutomationContractError,
            "verification authorization basis is incomplete",
        ):
            workflow_automation_module.authorize_public_run(
                verify_store,
                "$workflow auto: verify",
                authorization_id="authorization-verification-incomplete",
                authorization_class="verification",
                actor="user",
                occurred_at="2026-07-24T00:05:00Z",
                verification_basis={"closed_milestones_identity": "sha256:plan"},
            )
        with self.assertRaisesRegex(
            AutomationContractError,
            "legacy verify adapter must not infer authoring authority",
        ):
            workflow_automation_module.authorize_public_run(
                verify_store,
                "workflow auto-through: verify",
                authorization_id="authorization-authoring-inferred",
                authorization_class="authoring",
                actor="user",
                occurred_at="2026-07-24T00:05:30Z",
            )
        paused = verify_store.read()
        paused_automation = copy.deepcopy(paused.automation)
        paused_automation["run"]["status"] = "paused"
        paused_automation["run"]["pause_reason"] = (
            "verification-authorization-required"
        )
        verify_store.replace_automation(
            paused_automation,
            expected_document_identity=paused.document_identity,
        )
        (
            verification_basis,
            verification_basis_paths,
            code_state_provider,
        ) = self.write_verification_readiness_evidence(verify_store)
        authorized = workflow_automation_module.authorize_public_run(
            verify_store,
            "$workflow auto: verify",
            authorization_id="authorization-verification-current",
            authorization_class="verification",
            actor="user",
            occurred_at="2026-07-24T00:06:00Z",
            verification_basis=verification_basis,
            repository_root=verify_store.repository_root,
            verification_basis_paths=verification_basis_paths,
            code_state_provider=code_state_provider,
        )
        self.assertEqual(authorized["stage_outcome"], "authorization-recorded")
        resumed_state = verify_store.read().automation
        self.assertEqual(resumed_state["run"]["status"], "active")
        self.assertNotIn("pause_reason", resumed_state["run"])
        self.assertEqual(
            [
                parent["authorization_class"]
                for parent in resumed_state["parent_authorizations"].values()
            ],
            ["verification"],
        )

    def test_legacy_status_is_read_only_and_off_migrates_then_cancels_once(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "change.yaml"
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Legacy control fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                    "workflow": {
                        "autoprogression": {
                            "profile": "implementation-through-verify",
                            "authorized_by": "user",
                            "authorized_at": "2026-07-20T00:00:00Z",
                            "change_id": "2026-07-20-example",
                            "phase": "B",
                            "state": "armed",
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(path)
        before = path.read_bytes()
        status = execute_public_control_command(
            store,
            "workflow auto-through: status",
            actor="user",
            occurred_at="2026-07-24T00:00:00Z",
        )
        self.assertEqual(status["source"], "legacy-read-only")
        self.assertEqual(path.read_bytes(), before)

        cancelled = execute_public_control_command(
            store,
            "workflow auto-through: off",
            actor="user",
            occurred_at="2026-07-24T00:01:00Z",
        )
        snapshot = store.read()
        self.assertEqual(cancelled["stage_outcome"], "cancelled")
        self.assertEqual(snapshot.automation["run"]["status"], "cancelled")
        self.assertEqual(
            len(snapshot.automation["migration_receipts"]),
            1,
        )
        self.assertEqual(
            snapshot.document["workflow"]["autoprogression"]["state"],
            "armed",
        )

    def test_legacy_off_is_atomic_when_the_old_second_step_would_fail(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "change.yaml"
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Atomic legacy cancellation fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                    "workflow": {
                        "autoprogression": {
                            "profile": "implementation-through-verify",
                            "authorized_by": "user",
                            "authorized_at": "2026-07-20T00:00:00Z",
                            "change_id": "2026-07-20-example",
                            "phase": "B",
                            "state": "armed",
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(path)

        with patch.object(
            store,
            "cancel",
            side_effect=AssertionError("legacy off must not use a second write"),
        ):
            result = execute_public_control_command(
                store,
                "workflow auto-through: off",
                actor="user",
                occurred_at="2026-07-24T00:01:00Z",
            )

        self.assertEqual(result["stage_outcome"], "cancelled")
        self.assertEqual(store.read().automation["run"]["status"], "cancelled")

    def test_terminal_legacy_off_is_read_only_and_idempotent(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "change.yaml"
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Terminal legacy cancellation fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                    "workflow": {
                        "autoprogression": {
                            "profile": "implementation-through-verify",
                            "authorized_by": "user",
                            "authorized_at": "2026-07-20T00:00:00Z",
                            "change_id": "2026-07-20-example",
                            "phase": "C",
                            "state": "completed",
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(path)
        before = path.read_bytes()

        result = execute_public_control_command(
            store,
            "workflow auto-through: off",
            actor="user",
            occurred_at="2026-07-24T00:01:00Z",
        )

        self.assertEqual(result["stage_outcome"], "already-completed")
        self.assertEqual(result["run_status"], "completed")
        self.assertEqual(path.read_bytes(), before)

    def test_public_resume_executes_stage_through_persisted_target_and_parent(
        self,
    ) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        change = root / "change.yaml"
        change.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Public resume fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(change, repository_root=root)
        pre_plan = PrePlanEvidence(
            positions={
                "proposal": ("sha256:proposal",),
                "proposal-review": ("sha256:proposal-review",),
            },
            review_outcomes={"proposal-review": "approved"},
            review_resolution_closed=True,
            architecture_applicability="not-required",
        )
        start_public_run(
            store,
            "$workflow auto: test-spec-review",
            run_id="run-public-resume",
            actor="user",
            occurred_at="2026-07-24T00:00:00Z",
            pre_plan=pre_plan,
        )
        basis = {
            "proposal_identity": "sha256:proposal",
            "approved_proposal_review_identity": "sha256:proposal-review",
            "closed_review_resolution_identity": "sha256:resolution",
            "stage_scope_identity": "sha256:scope",
        }
        inputs = {
            **basis,
            "proposal": "sha256:proposal",
            "proposal-review": "sha256:proposal-review",
        }

        def invoke() -> StageExecutionResult:
            relative = Path("specs/example.md")
            artifact = root / relative
            artifact.parent.mkdir(parents=True)
            artifact.write_text(
                (
                    ROOT
                    / "specs/single-bounded-review-fix-workflow-automation.md"
                ).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            evidence = ArtifactEvidence(
                relative.as_posix(),
                "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest(),
            )
            return StageExecutionResult((evidence,), {"spec": evidence})

        result = workflow_automation_module.resume_public_run(
            store,
            "$workflow auto: test-spec-review",
            repository_root=root,
            stage="spec",
            occurrence={"kind": "singleton"},
            capability_id="cap-public-spec",
            basis=basis,
            affected_path_roots=("specs/",),
            mutation_categories=("downstream-authoring-artifacts",),
            derived_at="2026-07-24T00:01:00Z",
            transition_id="transition-public-spec",
            input_identities=inputs,
            invoke_stage=invoke,
            synchronize_canonical_state=lambda stage_result: CanonicalSyncResult(
                "synchronized", stage_result.completion_evidence
            ),
            pre_plan=pre_plan,
        )

        self.assertEqual(result["stage_outcome"], "continue")
        self.assertEqual(result["transitions_attempted"][0]["status"], "completed")
        self.assertEqual(result["artifacts_changed"], ["specs/example.md"])
        self.assertEqual(result["next_action"], "spec-review")
        self.assertEqual(
            store.read().automation["observed_identities"],
            {
                "proposal": "sha256:proposal",
                "proposal-review": "sha256:proposal-review",
                "spec": result["latest_evidence_identities"]["spec"],
            },
        )

    def test_public_verify_missing_authority_pauses_durably_and_reactivates(
        self,
    ) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        change = root / "docs/changes/2026-07-20-example/change.yaml"
        change.parent.mkdir(parents=True)
        change.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Public verification authority boundary fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(change, repository_root=root)
        start_public_run(
            store,
            "$workflow auto: verify",
            run_id="run-verification-boundary",
            actor="user",
            occurred_at="2026-07-24T00:00:00Z",
            pre_plan=PrePlanEvidence(
                positions={"proposal": ("sha256:proposal",)},
                review_outcomes={},
                review_resolution_closed=True,
                architecture_applicability="not-required",
            ),
        )

        result = workflow_automation_module.resume_public_run(
            store,
            "$workflow auto: verify",
            repository_root=root,
            stage="verify",
        )

        paused = store.read().automation
        self.assertEqual(
            (paused["run"]["status"], paused["run"]["pause_reason"]),
            ("paused", "verification-authorization-required"),
        )
        self.assertEqual(
            (result["stage_outcome"], result["stop_reason"]),
            ("paused", "verification-authorization-required"),
        )
        self.assertEqual(
            result["latest_evidence_identities"],
            {"proposal": "sha256:proposal"},
        )
        self.assertEqual(paused["effective_capabilities"], {})
        self.assertEqual(paused["transition_receipts"], {})

        basis, basis_paths, provider = self.write_verification_readiness_evidence(
            store
        )
        workflow_automation_module.authorize_public_run(
            store,
            "$workflow auto: verify",
            authorization_id="authorization-verification-later",
            authorization_class="verification",
            actor="user",
            occurred_at="2026-07-24T00:01:00Z",
            verification_basis=basis,
            repository_root=root,
            verification_basis_paths=basis_paths,
            code_state_provider=provider,
        )
        reactivated = store.read().automation
        self.assertEqual(reactivated["run"]["status"], "active")
        self.assertNotIn("pause_reason", reactivated["run"])

    def test_public_resume_uses_durable_observed_identities_and_pauses_on_drift(
        self,
    ) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        change = root / "change.yaml"
        change.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Public resume drift fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(change, repository_root=root)
        original = PrePlanEvidence(
            positions={
                "proposal": ("sha256:proposal-v1",),
                "proposal-review": ("sha256:proposal-review-v1",),
            },
            review_outcomes={"proposal-review": "approved"},
            review_resolution_closed=True,
            architecture_applicability="not-required",
        )
        start_public_run(
            store,
            "$workflow auto: test-spec-review",
            run_id="run-public-drift",
            actor="user",
            occurred_at="2026-07-24T00:00:00Z",
            pre_plan=original,
        )
        drifted = dataclasses.replace(
            original,
            positions={
                "proposal": ("sha256:proposal-v2",),
                "proposal-review": ("sha256:proposal-review-v2",),
            },
        )
        invoked = 0

        def invoke() -> StageExecutionResult:
            nonlocal invoked
            invoked += 1
            raise AssertionError("stage must not run after canonical drift")

        with self.assertRaisesRegex(
            AutomationContractError, "canonical-state-mismatch: proposal"
        ):
            workflow_automation_module.resume_public_run(
                store,
                "$workflow auto: test-spec-review",
                repository_root=root,
                stage="spec",
                occurrence={"kind": "singleton"},
                capability_id="cap-public-drift",
                basis={
                    "proposal_identity": "sha256:proposal-v2",
                    "approved_proposal_review_identity":
                        "sha256:proposal-review-v2",
                    "closed_review_resolution_identity": "sha256:resolution",
                    "stage_scope_identity": "sha256:scope",
                },
                affected_path_roots=("specs/",),
                mutation_categories=("downstream-authoring-artifacts",),
                derived_at="2026-07-24T00:01:00Z",
                transition_id="transition-public-drift",
                input_identities={
                    "proposal_identity": "sha256:proposal-v2",
                    "approved_proposal_review_identity":
                        "sha256:proposal-review-v2",
                    "closed_review_resolution_identity": "sha256:resolution",
                    "stage_scope_identity": "sha256:scope",
                    "proposal": "sha256:proposal-v2",
                    "proposal-review": "sha256:proposal-review-v2",
                },
                invoke_stage=invoke,
                synchronize_canonical_state=lambda result:
                    CanonicalSyncResult(
                        "synchronized", result.completion_evidence
                    ),
                pre_plan=drifted,
            )

        automation = store.read().automation
        assert automation is not None
        self.assertEqual(invoked, 0)
        self.assertEqual(
            (automation["run"]["status"], automation["run"]["pause_reason"]),
            ("paused", "canonical-state-mismatch"),
        )
        self.assertEqual(automation["effective_capabilities"], {})
        self.assertEqual(automation["transition_receipts"], {})
        self.assertEqual(
            automation["observed_identities"],
            {
                "proposal": "sha256:proposal-v1",
                "proposal-review": "sha256:proposal-review-v1",
            },
        )
        self.assertFalse((root / "specs/example.md").exists())

    def test_public_verification_authorization_rejects_unbacked_shaped_hashes(
        self,
    ) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        path = root / "change.yaml"
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Verification authorization fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(path, repository_root=root)
        start_public_run(
            store,
            "$workflow auto: verify",
            run_id="run-public-unbacked-verify",
            actor="user",
            occurred_at="2026-07-24T00:00:00Z",
            pre_plan=PrePlanEvidence(
                positions={"proposal": ("sha256:proposal",)},
                review_outcomes={},
                review_resolution_closed=True,
                architecture_applicability="not-required",
            ),
        )
        shaped = {
            "closed_milestones_identity": "sha256:closed",
            "final_code_review_identity": "sha256:final-review",
            "promotion_evidence_identity": "sha256:promotion",
            "explanation_inputs_identity": "sha256:explanation",
            "branch_state_identity": "sha256:branch",
            "verification_commands_identity": "sha256:commands",
        }
        with self.assertRaisesRegex(
            AutomationContractError,
            "repository-backed verification basis is required",
        ):
            workflow_automation_module.authorize_public_run(
                store,
                "$workflow auto: verify",
                authorization_id="authorization-verification-unbacked",
                authorization_class="verification",
                actor="user",
                occurred_at="2026-07-24T00:01:00Z",
                verification_basis=shaped,
            )
        automation = store.read().automation
        assert automation is not None
        self.assertEqual(automation["parent_authorizations"], {})

    def test_public_verification_authorization_validates_each_closeout_gate(
        self,
    ) -> None:
        cases = (
            (
                "closed_milestones_identity",
                "- Milestone state: closed",
                "- Milestone state: implementing",
                "milestones are open",
            ),
            (
                "final_code_review_identity",
                "complete_final_diff: reviewed",
                "complete_final_diff: future-value",
                "final review is not clean",
            ),
            (
                "promotion_evidence_identity",
                "Status: valid",
                "Status: stale",
                "evidence is invalid: promotion_evidence_identity",
            ),
            (
                "explanation_inputs_identity",
                "Status: current",
                "Status: stale",
                "explanation is not current",
            ),
            (
                "branch_state_identity",
                "Status: current",
                "Status: stale",
                "branch state is invalid",
            ),
            (
                "verification_commands_identity",
                "Status: current",
                "Status: stale",
                "evidence is invalid: verification_commands_identity",
            ),
        )
        for name, old, new, expected in cases:
            with self.subTest(gate=name):
                temp = tempfile.TemporaryDirectory()
                self.addCleanup(temp.cleanup)
                root = Path(temp.name)
                path = root / "change.yaml"
                path.write_text(
                    dump_yaml(
                        {
                            "change_id": "2026-07-20-example",
                            "title": "Verification gate fixture",
                            "classification": "default",
                            "risk": "medium",
                            "review": {
                                "status": "resolved",
                                "unresolved_items": 0,
                            },
                        }
                    ),
                    encoding="utf-8",
                )
                store = WorkflowAutomationStateStore(
                    path, repository_root=root
                )
                start_public_run(
                    store,
                    "$workflow auto: verify",
                    run_id=f"run-public-{name}",
                    actor="user",
                    occurred_at="2026-07-24T00:00:00Z",
                    pre_plan=PrePlanEvidence(
                        positions={"proposal": ("sha256:proposal",)},
                        review_outcomes={},
                        review_resolution_closed=True,
                        architecture_applicability="not-required",
                    ),
                )
                basis, paths, provider = (
                    self.write_verification_readiness_evidence(store)
                )
                artifact = root / paths[name]
                text = artifact.read_text(encoding="utf-8")
                self.assertIn(old, text)
                artifact.write_text(
                    text.replace(old, new, 1),
                    encoding="utf-8",
                )
                basis[name] = (
                    "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()
                )
                if name == "final_code_review_identity":
                    explanation = root / paths["explanation_inputs_identity"]
                    explanation.write_text(
                        explanation.read_text(encoding="utf-8").replace(
                            next(
                                line.split(": ", 1)[1]
                                for line in explanation.read_text(
                                    encoding="utf-8"
                                ).splitlines()
                                if line.startswith("Final review identity: ")
                            ),
                            basis[name],
                        ),
                        encoding="utf-8",
                    )
                    basis["explanation_inputs_identity"] = (
                        "sha256:"
                        + hashlib.sha256(explanation.read_bytes()).hexdigest()
                    )
                with self.assertRaisesRegex(
                    AutomationContractError, expected
                ):
                    workflow_automation_module.authorize_public_run(
                        store,
                        "$workflow auto: verify",
                        authorization_id=f"authorization-{name}",
                        authorization_class="verification",
                        actor="user",
                        occurred_at="2026-07-24T00:01:00Z",
                        verification_basis=basis,
                        repository_root=root,
                        verification_basis_paths=paths,
                        code_state_provider=provider,
                    )
                automation = store.read().automation
                assert automation is not None
                self.assertEqual(automation["parent_authorizations"], {})

    def test_public_composition_is_deterministic_and_order_independent(
        self,
    ) -> None:
        class SimulatedProcessInterruption(BaseException):
            def __init__(self, result: StageExecutionResult) -> None:
                super().__init__("simulated process interruption")
                self.result = result

        def run_scenario(name: str) -> dict[str, object]:
            temporary = tempfile.TemporaryDirectory()
            root_path = Path(temporary.name)
            external_calls: list[str] = []
            try:
                root = root_path
                path = root / "change.yaml"
                if name in {"migration"}:
                    document = {
                        "change_id": "2026-07-20-example",
                        "title": "Legacy deterministic fixture",
                        "classification": "default",
                        "risk": "medium",
                        "review": {"status": "resolved", "unresolved_items": 0},
                        "workflow": {
                            "autoprogression": {
                                "profile": "implementation-through-verify",
                                "authorized_by": "user",
                                "authorized_at": "2026-07-20T00:00:00Z",
                                "change_id": "2026-07-20-example",
                                "phase": "B",
                                "state": "armed",
                            }
                        },
                    }
                else:
                    document = {
                        "change_id": "2026-07-20-example",
                        "title": "Authoring deterministic fixture",
                        "classification": "default",
                        "risk": "medium",
                        "review": {"status": "resolved", "unresolved_items": 0},
                    }
                path.write_text(dump_yaml(document), encoding="utf-8")
                store = WorkflowAutomationStateStore(
                    path, repository_root=root
                )

                def prohibited_external_action(*_args, **_kwargs):
                    external_calls.append("called")
                    raise AssertionError("prohibited external action was invoked")

                real_popen = subprocess.Popen

                def allow_root_probe(command, *args, **kwargs):
                    return run_exact_read_only_git_probe(
                        command,
                        *args,
                        expected_root=root,
                        real_popen=real_popen,
                        **kwargs,
                    )

                def run_authoring(*, interrupted: bool = False) -> dict[str, object]:
                    pre_plan = PrePlanEvidence(
                        positions={
                            "proposal": ("sha256:proposal",),
                            "proposal-review": ("sha256:proposal-review",),
                        },
                        review_outcomes={"proposal-review": "approved"},
                        review_resolution_closed=True,
                        architecture_applicability="not-required",
                    )
                    start_public_run(
                        store,
                        "$workflow auto: test-spec-review",
                        run_id="run-deterministic",
                        actor="user",
                        occurred_at="2026-07-24T00:00:00Z",
                        pre_plan=pre_plan,
                    )
                    basis = {
                        "proposal_identity": "sha256:proposal",
                        "approved_proposal_review_identity":
                            "sha256:proposal-review",
                        "closed_review_resolution_identity":
                            "sha256:resolution",
                        "stage_scope_identity": "sha256:scope",
                    }

                    def completed_invoke() -> StageExecutionResult:
                        relative = Path("specs/example.md")
                        artifact = root / relative
                        artifact.parent.mkdir(parents=True)
                        artifact.write_text(
                            (
                                ROOT
                                / "specs/single-bounded-review-fix-workflow-automation.md"
                            ).read_text(encoding="utf-8"),
                            encoding="utf-8",
                        )
                        evidence = ArtifactEvidence(
                            relative.as_posix(),
                            "sha256:"
                            + hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        )
                        return StageExecutionResult(
                            (evidence,), {"spec": evidence}
                        )

                    if interrupted:
                        def interrupt_after_stage_write() -> StageExecutionResult:
                            raise SimulatedProcessInterruption(
                                completed_invoke()
                            )

                        try:
                            workflow_automation_module.resume_public_run(
                                store,
                                "$workflow auto: test-spec-review",
                                repository_root=root,
                                stage="spec",
                                occurrence={"kind": "singleton"},
                                capability_id="cap-deterministic",
                                basis=basis,
                                affected_path_roots=("specs/",),
                                mutation_categories=(
                                    "downstream-authoring-artifacts",
                                ),
                                derived_at="2026-07-24T00:01:00Z",
                                transition_id="transition-interrupted",
                                input_identities={
                                    **basis,
                                    "proposal": "sha256:proposal",
                                    "proposal-review":
                                        "sha256:proposal-review",
                                },
                                invoke_stage=interrupt_after_stage_write,
                                synchronize_canonical_state=lambda result:
                                    CanonicalSyncResult(
                                        "synchronized",
                                        result.completion_evidence,
                                    ),
                                pre_plan=pre_plan,
                            )
                        except SimulatedProcessInterruption as error:
                            interruption = str(error)
                            interrupted_result = error.result
                        else:
                            self.fail("simulated interruption was not raised")
                        prepared = store.read().automation
                        self.assertEqual(
                            prepared["transition_receipts"][
                                "transition-interrupted"
                            ]["status"],
                            "prepared",
                        )
                        self.assertEqual(
                            prepared["effective_capabilities"][
                                "cap-deterministic"
                            ]["status"],
                            "active",
                        )
                        serialized_outputs = [
                            {
                                "path": evidence.path,
                                "identity": evidence.identity,
                            }
                            for evidence in interrupted_result.outputs
                        ]
                        serialized_canonical = {
                            evidence_name: {
                                "path": evidence.path,
                                "identity": evidence.identity,
                            }
                            for evidence_name, evidence in (
                                interrupted_result.completion_evidence.items()
                            )
                        }
                        recovery_completion_evidence = {
                            "input_identities": {
                                **basis,
                                "proposal": "sha256:proposal",
                                "proposal-review":
                                    "sha256:proposal-review",
                            },
                            "expected_postcondition": prepared[
                                "transition_receipts"
                            ]["transition-interrupted"][
                                "expected_postcondition"
                            ],
                            "outputs": serialized_outputs,
                            "canonical_sync": {
                                "status": "synchronized",
                                "evidence": serialized_canonical,
                                "observed_identities": {
                                    "proposal": "sha256:proposal",
                                    "proposal-review":
                                        "sha256:proposal-review",
                                    **{
                                        evidence_name: evidence.identity
                                        for evidence_name, evidence in (
                                            interrupted_result
                                            .completion_evidence.items()
                                        )
                                    },
                                },
                            },
                        }
                    result = workflow_automation_module.resume_public_run(
                        store,
                        "$workflow auto: test-spec-review",
                        repository_root=root,
                        stage="spec",
                        occurrence={"kind": "singleton"},
                        capability_id="cap-deterministic",
                        basis=basis,
                        affected_path_roots=("specs/",),
                        mutation_categories=(
                            "downstream-authoring-artifacts",
                        ),
                        derived_at="2026-07-24T00:01:00Z",
                        transition_id=(
                            "transition-interrupted"
                            if interrupted
                            else "transition-deterministic"
                        ),
                        input_identities={
                            **basis,
                            "proposal": "sha256:proposal",
                            "proposal-review": "sha256:proposal-review",
                        },
                        invoke_stage=(
                            (
                                lambda: self.fail(
                                    "recovery reran the interrupted stage"
                                )
                            )
                            if interrupted
                            else completed_invoke
                        ),
                        synchronize_canonical_state=lambda stage_result:
                            CanonicalSyncResult(
                                "synchronized",
                                stage_result.completion_evidence,
                        ),
                        pre_plan=(
                            PrePlanEvidence(
                                positions={
                                    "proposal": ("sha256:proposal",),
                                    "proposal-review": (
                                        "sha256:proposal-review",
                                    ),
                                    "spec": tuple(
                                        evidence.identity
                                        for evidence in (
                                            interrupted_result
                                            .completion_evidence.values()
                                        )
                                    ),
                                },
                                review_outcomes={
                                    "proposal-review": "approved"
                                },
                                review_resolution_closed=True,
                                architecture_applicability="not-required",
                            )
                            if interrupted
                            else pre_plan
                        ),
                        recovery_completion_evidence=(
                            recovery_completion_evidence
                            if interrupted
                            else None
                        ),
                    )
                    if interrupted:
                        result["interruption"] = interruption
                        recovered = store.read().automation
                        self.assertEqual(
                            recovered["transition_receipts"][
                                "transition-interrupted"
                            ]["status"],
                            "completed",
                        )
                        self.assertEqual(
                            list(recovered["transition_receipts"]),
                            ["transition-interrupted"],
                        )
                    return result

                with patch.dict(
                    os.environ,
                    {
                        "TZ": "UTC",
                        "LC_ALL": "C",
                        "PATH": os.environ.get("PATH", ""),
                    },
                    clear=True,
                ), patch(
                    "subprocess.run", side_effect=allow_root_probe
                ), patch(
                    "subprocess.Popen", side_effect=prohibited_external_action
                ), patch(
                    "socket.create_connection",
                    side_effect=prohibited_external_action,
                ), patch(
                    "urllib.request.urlopen",
                    side_effect=prohibited_external_action,
                ), patch(
                    "os.system", side_effect=prohibited_external_action
                ):
                    sanitized_environment = {
                        key: os.environ.get(key)
                        for key in ("TZ", "LC_ALL")
                    }
                    self.assertEqual(
                        sanitized_environment,
                        {"TZ": "UTC", "LC_ALL": "C"},
                    )
                    if name == "clean":
                        result = run_authoring()
                    elif name == "interruption":
                        result = run_authoring(interrupted=True)
                    elif name == "cancellation":
                        start_public_run(
                            store,
                            "$workflow auto: spec",
                            run_id="run-cancel",
                            actor="user",
                            occurred_at="2026-07-24T00:00:00Z",
                            pre_plan=PrePlanEvidence(
                                positions={
                                    "proposal": ("sha256:proposal",)
                                },
                                review_outcomes={},
                                review_resolution_closed=True,
                                architecture_applicability="not-required",
                            ),
                        )
                        result = execute_public_control_command(
                            store,
                            "$workflow auto: off",
                            actor="user",
                            occurred_at="2026-07-24T00:01:00Z",
                        )
                    elif name == "migration":
                        result = start_public_run(
                            store,
                            "workflow auto-through: verify",
                            run_id="run-migration",
                            actor="user",
                            occurred_at="2026-07-24T00:00:00Z",
                            pre_plan=PrePlanEvidence(
                                positions={
                                    "proposal": ("sha256:proposal",)
                                },
                                review_outcomes={},
                                review_resolution_closed=True,
                                architecture_applicability="not-required",
                            ),
                        )
                    elif name == "missing-authority":
                        start_public_run(
                            store,
                            "$workflow auto: verify",
                            run_id="run-missing-authority",
                            actor="user",
                            occurred_at="2026-07-24T00:00:00Z",
                            pre_plan=PrePlanEvidence(
                                positions={
                                    "proposal": ("sha256:proposal",)
                                },
                                review_outcomes={},
                                review_resolution_closed=True,
                                architecture_applicability="not-required",
                            ),
                        )
                        result = workflow_automation_module.resume_public_run(
                            store,
                            "$workflow auto: verify",
                            repository_root=root,
                            stage="verify",
                        )
                        self.assertEqual(
                            (
                                store.read().automation["run"]["status"],
                                store.read().automation["run"]["pause_reason"],
                            ),
                            (
                                "paused",
                                "verification-authorization-required",
                            ),
                        )
                    elif name == "correction":
                        fixture = self.prepare_proposal_correction_transaction(
                            transition_id="transition-correction",
                            store=store,
                            public_authorization=True,
                        )
                        request = dict(fixture["coordination"])
                        for field in (
                            "invocation_context",
                            "target_stage",
                            "store",
                            "repository_root",
                            "parent_authorization_id",
                        ):
                            request.pop(field)
                        result = workflow_automation_module.resume_public_run(
                            store,
                            "$workflow auto: spec",
                            repository_root=root,
                            **request,
                        )
                    elif name == "final-success":
                        basis, basis_paths, provider = (
                            self.write_verification_readiness_evidence(store)
                        )
                        plan_path = root / basis_paths[
                            "closed_milestones_identity"
                        ]
                        active_plan = ActivePlanContext.from_text(
                            plan_path.read_text(encoding="utf-8"),
                            plan_identity=basis[
                                "closed_milestones_identity"
                            ],
                        )
                        start_public_run(
                            store,
                            "$workflow auto: verify",
                            run_id="run-final-success",
                            actor="user",
                            occurred_at="2026-07-24T00:00:00Z",
                            plan=active_plan,
                            verification_basis=basis,
                            verification_basis_paths=basis_paths,
                            code_state_provider=provider,
                        )

                        def verify_invoke() -> StageExecutionResult:
                            report_path = (
                                "docs/changes/2026-07-20-example/"
                                "verify-report.md"
                            )
                            validation_path = (
                                "docs/changes/2026-07-20-example/"
                                "verify-validation.md"
                            )
                            report_file = root / report_path
                            report_file.write_text(
                                "Stage: verify\nResult: passed\n"
                                "Next stage: pr\n"
                                "External actions performed: no\n",
                                encoding="utf-8",
                            )
                            validation_file = root / validation_path
                            validation_file.write_text(
                                "Stage: verify\nResult: passed\n",
                                encoding="utf-8",
                            )
                            report = ArtifactEvidence(
                                report_path,
                                "sha256:"
                                + hashlib.sha256(
                                    report_file.read_bytes()
                                ).hexdigest(),
                            )
                            validation = ArtifactEvidence(
                                validation_path,
                                "sha256:"
                                + hashlib.sha256(
                                    validation_file.read_bytes()
                                ).hexdigest(),
                            )
                            return StageExecutionResult(
                                (report, validation),
                                {
                                    "verify-report": report,
                                    "validation": validation,
                                },
                            )

                        result = workflow_automation_module.resume_public_run(
                            store,
                            "$workflow auto: verify",
                            repository_root=root,
                            verification_basis_paths=basis_paths,
                            code_state_provider=provider,
                            stage="verify",
                            occurrence={"kind": "final"},
                            capability_id="cap-final-success",
                            basis=basis,
                            affected_path_roots=(
                                "docs/changes/2026-07-20-example/",
                            ),
                            mutation_categories=(
                                "verification-evidence",
                            ),
                            derived_at="2026-07-24T00:01:00Z",
                            transition_id="transition-final-success",
                            input_identities={
                                **basis,
                                "plan": basis[
                                    "closed_milestones_identity"
                                ],
                            },
                            invoke_stage=verify_invoke,
                            active_plan=active_plan,
                            synchronize_canonical_state=lambda execution:
                                CanonicalSyncResult(
                                    "synchronized",
                                    execution.completion_evidence,
                                ),
                        )
                    else:
                        self.fail(f"unknown deterministic scenario: {name}")
                    status_before = path.read_bytes()
                    status = execute_public_control_command(
                        store,
                        "$workflow auto: status",
                        actor="user",
                        occurred_at="2026-07-24T00:02:00Z",
                    )
                    self.assertEqual(path.read_bytes(), status_before)
                    payload = {
                        "result": result,
                        "status": status,
                        "automation": store.read().automation,
                        "environment": sanitized_environment,
                        "external_action_calls": len(external_calls),
                    }
            finally:
                temporary.cleanup()
            self.assertFalse(root_path.exists())
            payload["teardown_complete"] = True
            return payload

        def run_order(order: tuple[str, ...]) -> dict[str, dict[str, object]]:
            return {name: run_scenario(name) for name in order}

        declared = (
            "clean",
            "correction",
            "interruption",
            "cancellation",
            "migration",
            "missing-authority",
            "final-success",
        )
        first = run_order(declared)
        repeated = run_order(declared)
        reversed_result = run_order(tuple(reversed(declared)))

        self.assertEqual(first, repeated)
        self.assertEqual(first, reversed_result)
        for evidence in first.values():
            self.assertEqual(evidence["external_action_calls"], 0)
            self.assertEqual(
                evidence["environment"], {"TZ": "UTC", "LC_ALL": "C"}
            )
            self.assertTrue(evidence["teardown_complete"])

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

    def test_position_artifact_sequence_reaches_test_spec_review(self) -> None:
        evidence = PrePlanEvidence(
            positions={
                "proposal": ("sha256:proposal",),
                "proposal-review": ("sha256:proposal-review",),
                "spec": ("sha256:spec",),
                "spec-review": ("sha256:spec-review",),
                "architecture-assessment": ("sha256:assessment",),
                "architecture": ("sha256:architecture",),
                "architecture-review": ("sha256:architecture-review",),
                "plan": ("sha256:plan",),
                "plan-review": ("sha256:plan-review",),
                "test-spec": ("sha256:test-spec",),
                "test-spec-review": ("sha256:test-spec-review",),
            },
            review_outcomes={
                "proposal-review": "approved",
                "spec-review": "approved",
                "architecture-review": "approved",
                "plan-review": "approved",
                "test-spec-review": "approved",
            },
            review_resolution_closed=True,
            architecture_applicability="required",
        )

        position = resolve_canonical_position(pre_plan=evidence)

        self.assertEqual(position.position, "test-spec-review")
        self.assertEqual(
            position.observed_identities["plan-review"],
            "sha256:plan-review",
        )
        self.assertEqual(
            position.observed_identities["test-spec"],
            "sha256:test-spec",
        )

    def test_position_active_plan_represents_post_plan_authoring_handoffs(
        self,
    ) -> None:
        cases = (
            ("plan-review", "plan"),
            ("test-spec", "plan-review"),
            ("test-spec-review", "test-spec"),
            ("implement M1", "test-spec-review"),
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
        latest_review = store.read().automation["latest_review_result"]
        self.assertEqual(
            latest_review,
            {
                "review_id": "proposal-review-r1",
                "reviewed_artifact_identity": proposal_identity,
                "review_record_identity": completed["canonical_sync"][
                    "observed_identities"
                ]["proposal-review"],
                "outcome": "approved",
                "occurrence_recorded": True,
                "clean_gate": "satisfied",
                "routing_action": "stop-at-target",
                "source_transition_id": "transition-engine-001",
            },
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
            target_stage="spec",
        )
        self.assertEqual((approved.clean_gate, approved.routing_action), ("satisfied", "continue"))
        self.assertEqual(approved.next_stage, "spec")

        correction = evaluate_proposal_review(
            outcome="changes-requested",
            review_id="proposal-review-r1",
            proposal_identity="sha256:proposal-v1",
            reviewed_proposal_identity="sha256:proposal-v1",
            target_stage="test-spec-review",
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
            target_stage="test-spec-review",
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
            target_stage="test-spec-review",
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

    def test_proposal_review_transaction_persists_complete_outcome_matrix(
        self,
    ) -> None:
        for target_stage in ("proposal-review", "spec"):
            for outcome in (
                "approved",
                "changes-requested",
                "blocked",
                "inconclusive",
            ):
                with self.subTest(target=target_stage, outcome=outcome):
                    state = copy.deepcopy(FIXTURES.valid_automation())
                    state["effective_capabilities"] = {}
                    target = bind_target(
                        target_stage, bound_at="2026-07-22T00:00:00Z"
                    )
                    state["run"]["target"] = copy.deepcopy(target)
                    state["run"]["pause_reason"] = "stale-before-review"
                    state["parent_authorizations"][
                        "authorization-authoring-001"
                    ]["maximum_target"] = copy.deepcopy(target)
                    store = self.make_store(state)

                    def invoke() -> StageExecutionResult:
                        evidence = self.write_evidence(store, status=outcome)
                        return StageExecutionResult(
                            (evidence,), {"proposal-review": evidence}
                        )

                    result = self.coordinate_proposal_review(store, invoke)
                    self.assertEqual(result.status, "completed")
                    persisted = store.read().automation[
                        "latest_review_result"
                    ]
                    required = {
                        "review_id",
                        "reviewed_artifact_identity",
                        "review_record_identity",
                        "outcome",
                        "occurrence_recorded",
                        "clean_gate",
                        "routing_action",
                    }
                    self.assertTrue(required <= set(persisted))
                    self.assertEqual(persisted["outcome"], outcome)
                    self.assertTrue(persisted["occurrence_recorded"])
                    self.assertEqual(
                        persisted["clean_gate"],
                        "satisfied"
                        if outcome == "approved"
                        else "not-satisfied",
                    )
                    if outcome in {"blocked", "inconclusive"}:
                        expected_action = "pause"
                    elif target_stage == "proposal-review":
                        expected_action = "stop-at-target"
                    elif outcome == "approved":
                        expected_action = "continue"
                    else:
                        expected_action = "pause"
                    self.assertEqual(
                        persisted["routing_action"], expected_action
                    )
                    self.assertEqual(
                        "pause_reason" in persisted,
                        expected_action == "pause",
                    )
                    run = store.read().automation["run"]
                    self.assertEqual(
                        run["status"],
                        "paused"
                        if expected_action == "pause"
                        else "completed"
                        if expected_action == "stop-at-target"
                        else "active",
                    )
                    if expected_action == "pause":
                        self.assertEqual(
                            run["pause_reason"],
                            persisted["pause_reason"],
                        )
                    else:
                        self.assertNotIn("pause_reason", run)

    def test_proposal_review_transaction_persists_authorized_correction_loop(
        self,
    ) -> None:
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="transition-correction-after-review"
        )
        store = fixture["store"]

        capability = store.read().automation["effective_capabilities"][
            "cap-correction-transaction"
        ]
        review_path = fixture["review_path"]
        review_identity = capability["basis"]["review_record_identity"]
        proposal_identity = capability["basis"]["reviewed_proposal_identity"]

        def invoke() -> StageExecutionResult:
            evidence = ArtifactEvidence(review_path, review_identity)
            return StageExecutionResult(
                (evidence,), {"proposal-review": evidence}
            )

        result = self.coordinate_proposal_review(
            store,
            invoke,
            parent_authorization_id="auth-correction",
            capability_id="cap-review-for-correction-loop",
            proposal_identity=proposal_identity,
            synchronize=lambda stage_result: CanonicalSyncResult(
                "synchronized", stage_result.completion_evidence
            ),
        )

        self.assertEqual(result.status, "completed")
        automation = store.read().automation
        self.assertEqual(
            automation["latest_review_result"],
            {
                "review_id": "proposal-review-r1",
                "reviewed_artifact_identity": automation[
                    "transition_receipts"
                ]["transition-engine-001"]["input_identities"]["proposal"],
                "review_record_identity": review_identity,
                "outcome": "changes-requested",
                "occurrence_recorded": True,
                "clean_gate": "not-satisfied",
                "routing_action": "correction-loop",
                "correction_capability_id": "cap-correction-transaction",
                "source_transition_id": "transition-engine-001",
            },
        )
        self.assertEqual(
            automation["transition_receipts"]["transition-engine-001"][
                "proposal_review_route"
            ]["correction_capability_id"],
            "cap-correction-transaction",
        )
        self.assertEqual(automation["run"]["status"], "active")

        correction = coordinate_non_public_authoring_stage(
            **fixture["coordination"]
        )
        self.assertEqual(
            (correction.coordination.status, correction.route.next_stage),
            ("completed", "proposal-review"),
        )
        corrected = store.read().automation
        self.assertEqual(
            corrected["latest_review_result"],
            automation["latest_review_result"],
        )
        self.assertEqual(
            corrected["effective_capabilities"][
                "cap-correction-transaction"
            ]["status"],
            "consumed",
        )
        fresh_review_capabilities = [
            capability
            for capability in corrected["effective_capabilities"].values()
            if capability["capability_kind"] == "proposal-review"
            and capability["status"] == "active"
        ]
        self.assertEqual(len(fresh_review_capabilities), 1)
        self.assertEqual(validate_workflow_automation(corrected), [])
        tampered_cases = []
        missing_capability = copy.deepcopy(corrected)
        missing_capability["effective_capabilities"].pop(
            "cap-correction-transaction"
        )
        tampered_cases.append(("missing-capability", missing_capability))
        stale_basis = copy.deepcopy(corrected)
        stale_basis["effective_capabilities"]["cap-correction-transaction"][
            "basis"
        ]["review_record_identity"] = "sha256:stale-review"
        tampered_cases.append(("stale-basis", stale_basis))
        missing_review_receipt = copy.deepcopy(corrected)
        missing_review_receipt["transition_receipts"].pop(
            "transition-engine-001"
        )
        tampered_cases.append(("missing-review-receipt", missing_review_receipt))
        wrong_source_transition = copy.deepcopy(corrected)
        wrong_source_transition["latest_review_result"][
            "source_transition_id"
        ] = "transition-later"
        tampered_cases.append(
            ("wrong-source-transition", wrong_source_transition)
        )
        changed_route_binding = copy.deepcopy(corrected)
        changed_route_binding["transition_receipts"]["transition-engine-001"][
            "proposal_review_route"
        ]["correction_capability_id"] = None
        tampered_cases.append(("changed-route-binding", changed_route_binding))
        for label, candidate in tampered_cases:
            with self.subTest(tamper=label):
                errors = validate_workflow_automation(candidate)
                self.assertTrue(
                    any(
                        "invalid recorded proposal-review route" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_proposal_review_authorization_pause_is_stable_after_later_capability(
        self,
    ) -> None:
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="unused-later-correction"
        )
        store = fixture["store"]
        snapshot = store.read()
        correction_capability = copy.deepcopy(
            snapshot.automation["effective_capabilities"][
                "cap-correction-transaction"
            ]
        )
        without_correction = copy.deepcopy(snapshot.automation)
        without_correction["effective_capabilities"] = {}
        store.replace_automation(
            without_correction,
            expected_document_identity=snapshot.document_identity,
        )

        review_path = fixture["review_path"]
        review_identity = correction_capability["basis"][
            "review_record_identity"
        ]
        proposal_identity = correction_capability["basis"][
            "reviewed_proposal_identity"
        ]

        def invoke() -> StageExecutionResult:
            evidence = ArtifactEvidence(review_path, review_identity)
            return StageExecutionResult(
                (evidence,), {"proposal-review": evidence}
            )

        self.coordinate_proposal_review(
            store,
            invoke,
            parent_authorization_id="auth-correction",
            capability_id="cap-review-without-correction",
            proposal_identity=proposal_identity,
            synchronize=lambda stage_result: CanonicalSyncResult(
                "synchronized", stage_result.completion_evidence
            ),
        )
        paused_snapshot = store.read()
        recorded_result = copy.deepcopy(
            paused_snapshot.automation["latest_review_result"]
        )
        self.assertEqual(recorded_result["routing_action"], "pause")
        self.assertEqual(
            recorded_result["source_transition_id"],
            "transition-engine-001",
        )
        self.assertEqual(
            recorded_result["pause_reason"],
            "proposal-correction-authorization-required",
        )
        self.assertIsNone(
            paused_snapshot.automation["transition_receipts"][
                recorded_result["source_transition_id"]
            ]["proposal_review_route"]["correction_capability_id"]
        )

        with_later_capability = copy.deepcopy(paused_snapshot.automation)
        with_later_capability["effective_capabilities"][
            correction_capability["capability_id"]
        ] = correction_capability
        store.replace_automation(
            with_later_capability,
            expected_document_identity=paused_snapshot.document_identity,
        )

        persisted = store.read().automation
        self.assertEqual(persisted["latest_review_result"], recorded_result)
        self.assertEqual(persisted["run"]["status"], "paused")
        self.assertEqual(
            persisted["run"]["pause_reason"],
            "proposal-correction-authorization-required",
        )

        retroactive_route = copy.deepcopy(persisted)
        retroactive_route["latest_review_result"].pop("pause_reason")
        retroactive_route["latest_review_result"]["routing_action"] = (
            "correction-loop"
        )
        retroactive_route["latest_review_result"]["correction_capability_id"] = (
            correction_capability["capability_id"]
        )
        retroactive_route["run"]["status"] = "active"
        retroactive_route["run"].pop("pause_reason")
        errors = validate_workflow_automation(retroactive_route)
        self.assertTrue(
            any(
                "invalid recorded proposal-review route" in error
                for error in errors
            ),
            errors,
        )

        rewritten_receipt = copy.deepcopy(retroactive_route)
        route_binding = rewritten_receipt["transition_receipts"][
            recorded_result["source_transition_id"]
        ]["proposal_review_route"]
        route_binding["routing_action"] = "correction-loop"
        route_binding["correction_capability_id"] = correction_capability[
            "capability_id"
        ]
        self.assertEqual(validate_workflow_automation(rewritten_receipt), [])
        current_snapshot = store.read()
        with self.assertRaisesRegex(
            StateContractError,
            "finalized transition receipt is immutable",
        ):
            store.replace_automation(
                rewritten_receipt,
                expected_document_identity=current_snapshot.document_identity,
            )

    def test_proposal_review_transaction_rejects_stale_correction_capability(
        self,
    ) -> None:
        cases = ("review_record_identity", "reviewed_proposal_identity")
        for stale_field in cases:
            with self.subTest(stale_field=stale_field):
                fixture = self.prepare_proposal_correction_transaction(
                    transition_id=f"unused-stale-{stale_field}"
                )
                store = fixture["store"]
                snapshot = store.read()
                automation = snapshot.automation
                capability = automation["effective_capabilities"][
                    "cap-correction-transaction"
                ]
                review_path = fixture["review_path"]
                review_identity = capability["basis"]["review_record_identity"]
                proposal_identity = capability["basis"][
                    "reviewed_proposal_identity"
                ]
                capability["basis"][stale_field] = f"sha256:stale-{stale_field}"
                store.replace_automation(
                    automation,
                    expected_document_identity=snapshot.document_identity,
                )

                def invoke() -> StageExecutionResult:
                    evidence = ArtifactEvidence(review_path, review_identity)
                    return StageExecutionResult(
                        (evidence,), {"proposal-review": evidence}
                    )

                self.coordinate_proposal_review(
                    store,
                    invoke,
                    parent_authorization_id="auth-correction",
                    capability_id=f"cap-review-stale-{stale_field}",
                    proposal_identity=proposal_identity,
                )

                persisted = store.read().automation
                self.assertEqual(
                    persisted["latest_review_result"]["routing_action"],
                    "pause",
                )
                self.assertEqual(
                    persisted["latest_review_result"]["pause_reason"],
                    "proposal-correction-authorization-required",
                )
                self.assertEqual(persisted["run"]["status"], "paused")
                self.assertEqual(
                    persisted["run"]["pause_reason"],
                    "proposal-correction-authorization-required",
                )

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

    def test_proposal_review_rejects_target_mutation(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)

        def invoke() -> StageExecutionResult:
            evidence = self.write_evidence(store)
            proposal = store.repository_root / "docs/proposals/example.md"
            proposal.write_text("# Mutated by reviewer\n", encoding="utf-8")
            return StageExecutionResult(
                outputs=(evidence,), completion_evidence={"proposal-review": evidence}
            )

        with self.assertRaisesRegex(
            AutomationContractError, "reviewed-artifact-identity-mismatch"
        ):
            self.coordinate_proposal_review(store, invoke)

    def test_non_public_review_routing_uses_identity_stable_verified_facts(self) -> None:
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["effective_capabilities"] = {}
        store = self.make_store(state)
        proposal_identity = self.write_proposal(store)

        def invoke() -> StageExecutionResult:
            evidence = self.write_evidence(store)
            return StageExecutionResult(
                outputs=(evidence,),
                completion_evidence={"proposal-review": evidence},
            )

        result = coordinate_non_public_authoring_stage(
            invocation_context="non-public-test-harness",
            target_stage="proposal-review",
            store=store,
            repository_root=store.repository_root,
            parent_authorization_id="authorization-authoring-001",
            capability_id="capability-stable-routing",
            stage="proposal-review",
            occurrence={"kind": "singleton"},
            basis={
                "proposal_identity": proposal_identity,
                "standing_gates_identity": "sha256:gates",
                "review_policy_identity": "sha256:policy",
                "structured_target_identity": "sha256:target",
                "review_evidence_roots": [
                    "docs/changes/2026-07-20-example/"
                ],
            },
            affected_path_roots=(
                "docs/changes/2026-07-20-example/",
            ),
            mutation_categories=("change-local-review-evidence",),
            derived_at="2026-07-22T00:01:00Z",
            transition_id="transition-stable-routing",
            input_identities=self.proposal_input_identities(
                proposal_identity
            ),
            invoke_stage=invoke,
            synchronize_canonical_state=lambda stage_result: self.synchronize_review(
                store, stage_result
            ),
            pre_plan=self.proposal_pre_plan(proposal_identity),
        )

        self.assertEqual(result.route.status, "stop-at-target")
        self.assertEqual(
            result.coordination.verified_completion.stage_facts[
                "review_outcome"
            ],
            "approved",
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

    def test_proposal_correction_authority_is_bound_to_capability_evidence(self) -> None:
        accepted = ["BRF-1"]
        classifications = {"BRF-1": "mechanical"}
        correction_plans = {
            "BRF-1": {
                "classification": "mechanical",
                "rationale": "The requested change is deterministic and bounded.",
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
        identity = lambda value: "sha256:" + hashlib.sha256(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        state = copy.deepcopy(FIXTURES.valid_automation())
        parent = state["parent_authorizations"]["authorization-authoring-001"]
        parent["allowed_capability_kinds"] = [
            "proposal-correction",
            "proposal-review",
        ]
        capability = state["effective_capabilities"]["capability-proposal-review-001"]
        store = self.make_store(state)
        review_path, resolution_path, review_identity = (
            self.write_proposal_correction_evidence(
                store,
                proposal_path="docs/proposals/example.md",
            )
        )
        capability.update(
            capability_kind="proposal-correction",
            stage={"name": "proposal", "occurrence": {"kind": "singleton"}},
            basis={
                "reviewed_proposal_identity": "sha256:proposal-v1",
                "review_record_identity": review_identity,
                "accepted_finding_set_identity": identity(accepted),
                "classifier_policy_identity": identity(correction_plans),
                "correction_budget_identity": identity(budget),
                "affected_proposal_roots": ["docs/proposals/"],
            },
            scope={
                "affected_path_roots": ["docs/proposals/"],
                "mutation_categories": ["proposal-content"],
                "correction_budget": budget,
                "correction_budget_identity": identity(budget),
                "review_record_path": review_path,
                "review_resolution_path": resolution_path,
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
        )
        authority = resolve_proposal_correction_authority(
            state,
            "capability-proposal-review-001",
            repository_root=store.repository_root,
        )
        self.assertEqual(authority.accepted_finding_ids, frozenset(accepted))
        review = store.repository_root / review_path
        review.write_text(
            review.read_text(encoding="utf-8") + "\n<!-- stale -->\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            AutomationContractError, "does not match capability basis"
        ):
            resolve_proposal_correction_authority(
                state,
                "capability-proposal-review-001",
                repository_root=store.repository_root,
            )
        review.write_text(
            review.read_text(encoding="utf-8").replace(
                "\n<!-- stale -->\n", ""
            ),
            encoding="utf-8",
        )
        capability["scope"]["accepted_finding_ids"] = ["BRF-1", "BRF-forged"]
        with self.assertRaisesRegex(
            AutomationContractError, "does not match capability basis"
        ):
            resolve_proposal_correction_authority(
                state,
                "capability-proposal-review-001",
                repository_root=store.repository_root,
            )

    def test_proposal_correction_rejects_noncanonical_occurrence_and_classification(
        self,
    ) -> None:
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="transition-canonical-correction"
        )
        store = fixture["store"]
        automation = store.read().automation
        capability = automation["effective_capabilities"][
            "cap-correction-transaction"
        ]
        review_log = (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        )
        original_log = review_log.read_text(encoding="utf-8")
        review_log.write_text(
            original_log.replace("Round: r1", "Round: r2"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            AutomationContractError, "review occurrence is not canonical"
        ):
            resolve_proposal_correction_authority(
                automation,
                "cap-correction-transaction",
                repository_root=store.repository_root,
            )
        review_log.write_text(original_log, encoding="utf-8")

        forged = {"BRF-1": "format-preserving"}
        forged_plans = copy.deepcopy(capability["scope"]["correction_plans"])
        forged_plans["BRF-1"]["classification"] = "format-preserving"
        capability["scope"]["finding_classifications"] = forged
        capability["scope"]["correction_plans"] = forged_plans
        capability["basis"]["classifier_policy_identity"] = (
            "sha256:"
            + hashlib.sha256(
                json.dumps(
                    forged_plans, sort_keys=True, separators=(",", ":")
                ).encode()
            ).hexdigest()
        )
        with self.assertRaisesRegex(
            AutomationContractError,
            "evidence does not match capability basis|driver classification evidence",
        ):
            resolve_proposal_correction_authority(
                automation,
                "cap-correction-transaction",
                repository_root=store.repository_root,
            )

    def test_proposal_correction_rejects_recipe_without_closed_operation(
        self,
    ) -> None:
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="transition-unsupported-recipe"
        )
        store = fixture["store"]
        resolution = store.repository_root / fixture["resolution_path"]
        resolution.write_text(
            resolution.read_text(encoding="utf-8").replace(
                "Append one newline to the reviewed proposal.",
                "Rewrite the proposal however the callback chooses.",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            AutomationContractError, "no closed executable operation"
        ):
            resolve_proposal_correction_authority(
                store.read().automation,
                "cap-correction-transaction",
                repository_root=store.repository_root,
            )

    def test_non_public_authoring_stage_uses_receipt_backed_spec_completion(self) -> None:
        target = bind_target("test-spec-review", bound_at="2026-07-22T00:00:00Z")
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
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["run"]["target"] = target
        state["parent_authorizations"] = {"auth-authoring": parent}
        state["effective_capabilities"] = {}
        state["transition_receipts"] = {}
        store = self.make_store(state)
        proposal_identity = "sha256:proposal"
        review_identity = "sha256:proposal-review"
        basis = {
            "proposal_identity": proposal_identity,
            "approved_proposal_review_identity": review_identity,
            "closed_review_resolution_identity": "sha256:resolution",
            "stage_scope_identity": "sha256:scope",
        }
        inputs = dict(basis, proposal=proposal_identity, **{"proposal-review": review_identity})

        def invoke() -> StageExecutionResult:
            relative = Path("specs/example.md")
            artifact = store.repository_root / relative
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text(
                (ROOT / "specs/single-bounded-review-fix-workflow-automation.md").read_text(),
                encoding="utf-8",
            )
            evidence = ArtifactEvidence(
                relative.as_posix(),
                "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest(),
            )
            return StageExecutionResult((evidence,), {"spec": evidence})

        coordinated = coordinate_non_public_authoring_stage(
            invocation_context="non-public-test-harness",
            target_stage="test-spec-review",
            store=store,
            repository_root=store.repository_root,
            parent_authorization_id="auth-authoring",
            capability_id="cap-spec-transaction",
            stage="spec",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("specs/",),
            mutation_categories=("downstream-authoring-artifacts",),
            derived_at="2026-07-22T00:01:00Z",
            transition_id="transition-spec-001",
            input_identities=inputs,
            invoke_stage=invoke,
            synchronize_canonical_state=lambda result: CanonicalSyncResult(
                "synchronized", result.completion_evidence
            ),
            pre_plan=PrePlanEvidence(
                positions={
                    "proposal": (proposal_identity,),
                    "proposal-review": (review_identity,),
                },
                review_outcomes={"proposal-review": "approved"},
                review_resolution_closed=True,
                architecture_applicability="not-required",
            ),
        )
        self.assertEqual(coordinated.coordination.status, "completed")
        self.assertEqual((coordinated.route.status, coordinated.route.next_stage), ("continue", "spec-review"))
        persisted = store.read().automation
        self.assertEqual(persisted["transition_receipts"]["transition-spec-001"]["status"], "completed")
        self.assertEqual(persisted["effective_capabilities"]["cap-spec-transaction"]["status"], "consumed")
        completed = persisted["transition_receipts"]["transition-spec-001"]
        recovered = evaluate_receipt_recovery(
            persisted,
            "transition-spec-001",
            completion_evidence={
                "outputs": copy.deepcopy(completed["outputs"]),
                "canonical_sync": copy.deepcopy(completed["canonical_sync"]),
            },
            repository_root=store.repository_root,
        )
        self.assertEqual(
            (recovered.action, recovered.reason),
            ("continue", "completed-evidence-current"),
        )

    def test_test_spec_transition_is_authorized_after_plan_review(self) -> None:
        target = bind_target(
            "test-spec-review",
            bound_at="2026-07-22T00:00:00Z",
        )
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
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["run"]["target"] = target
        state["parent_authorizations"] = {"auth-authoring": parent}
        state["effective_capabilities"] = {}
        state["transition_receipts"] = {}
        state["canonical_position_source"] = "plan-current-handoff-summary"
        state["observed_identities"] = {"plan": "sha256:plan-v1"}
        store = self.make_store(state)
        basis = {
            "proposal_identity": "sha256:proposal",
            "approved_proposal_review_identity": "sha256:proposal-review",
            "closed_review_resolution_identity": "sha256:resolution",
            "stage_scope_identity": "sha256:test-spec-scope",
        }
        inputs = {
            **basis,
            "spec": "sha256:spec",
            "plan": "sha256:plan-v1",
            "plan-review": "sha256:plan-review",
        }
        plan = ActivePlanContext.from_text(
            plan_text(
                current="M1. Prior Slice",
                current_state="planned",
                remaining="M1, M2, M3",
                next_stage="test-spec",
                milestone_one_state="planned",
            ),
            plan_identity="sha256:plan-v1",
        )

        def invoke() -> StageExecutionResult:
            relative = Path("specs/example.test.md")
            artifact = store.repository_root / relative
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text(
                (
                    ROOT
                    / "specs/single-bounded-review-fix-workflow-automation.test.md"
                ).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            evidence = ArtifactEvidence(
                relative.as_posix(),
                "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest(),
            )
            return StageExecutionResult(
                (evidence,),
                {"test-spec": evidence},
            )

        coordinated = coordinate_non_public_authoring_stage(
            invocation_context="non-public-test-harness",
            target_stage="test-spec-review",
            store=store,
            repository_root=store.repository_root,
            parent_authorization_id="auth-authoring",
            capability_id="cap-test-spec-transaction",
            stage="test-spec",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("specs/",),
            mutation_categories=("downstream-authoring-artifacts",),
            derived_at="2026-07-22T00:01:00Z",
            transition_id="transition-test-spec-001",
            input_identities=inputs,
            invoke_stage=invoke,
            synchronize_canonical_state=lambda result: CanonicalSyncResult(
                "synchronized", result.completion_evidence
            ),
            active_plan=plan,
            previously_observed={"plan": "sha256:plan-v1"},
        )

        self.assertEqual(coordinated.coordination.status, "completed")
        self.assertEqual(
            (coordinated.route.status, coordinated.route.next_stage),
            ("continue", "test-spec-review"),
        )
        persisted = store.read().automation
        receipt = persisted["transition_receipts"][
            "transition-test-spec-001"
        ]
        self.assertEqual(receipt["from_position"], "plan-review")
        self.assertEqual(receipt["status"], "completed")
        self.assertEqual(
            persisted["effective_capabilities"][
                "cap-test-spec-transaction"
            ]["status"],
            "consumed",
        )

    def test_completed_recovery_is_stage_semantic_for_assessment_and_plan(
        self,
    ) -> None:
        cases = (
            (
                "architecture-assessment",
                Path(
                    "docs/changes/2026-07-20-example/architecture-assessment.md"
                ),
                {
                    "proposal": ("sha256:proposal",),
                    "proposal-review": ("sha256:proposal-review",),
                    "spec": ("sha256:spec",),
                    "spec-review": ("sha256:spec-review",),
                },
            ),
            (
                "plan",
                Path("docs/plans/example.md"),
                {
                    "proposal": ("sha256:proposal",),
                    "proposal-review": ("sha256:proposal-review",),
                    "spec": ("sha256:spec",),
                    "spec-review": ("sha256:spec-review",),
                    "architecture-assessment": ("sha256:assessment",),
                },
            ),
        )
        for stage, relative, positions in cases:
            with self.subTest(stage=stage):
                stage_mutation_category = sorted(
                    category.value
                    for category in STAGE_POLICY_BY_STAGE[
                        stage
                    ].permitted_mutation_category
                )[0]
                target = bind_target(
                    "plan", bound_at="2026-07-22T00:00:00Z"
                )
                parent = create_parent_authorization(
                    authorization_id="auth-authoring",
                    authorization_class="authoring",
                    change_id="2026-07-20-example",
                    authorized_by="user",
                    authorized_at="2026-07-22T00:00:00Z",
                    maximum_target=target,
                    allowed_capability_kinds=("post-proposal-authoring",),
                    maximum_path_roots=(
                        "docs/changes/2026-07-20-example/",
                        "docs/plans/",
                    ),
                    maximum_mutation_categories=(
                        stage_mutation_category,
                    ),
                )
                state = copy.deepcopy(FIXTURES.valid_automation())
                state["run"]["target"] = target
                state["parent_authorizations"] = {
                    "auth-authoring": parent
                }
                state["effective_capabilities"] = {}
                state["transition_receipts"] = {}
                store = self.make_store(state)
                basis = {
                    "proposal_identity": "sha256:proposal",
                    "approved_proposal_review_identity": "sha256:proposal-review",
                    "closed_review_resolution_identity": "sha256:resolution",
                    "stage_scope_identity": "sha256:scope",
                }
                inputs = dict(basis)
                inputs.update(
                    {
                        name: identities[0]
                        for name, identities in positions.items()
                    }
                )
                if stage == "plan":
                    inputs.update(
                        {
                            "architecture_applicability": "not-applicable",
                            "architecture_applicability_identity": "sha256:assessment",
                        }
                    )

                def invoke() -> StageExecutionResult:
                    artifact = store.repository_root / relative
                    artifact.parent.mkdir(parents=True, exist_ok=True)
                    if stage == "architecture-assessment":
                        artifact.write_text(
                            "Stage: architecture-assessment\n"
                            "Applicability: not-required\n"
                            "Spec identity: sha256:spec\n",
                            encoding="utf-8",
                        )
                    else:
                        artifact.write_text(
                            plan_text(
                                current="M2. Engine Slice",
                                current_state="implementing",
                                remaining="M2, M3",
                                next_stage="implement M2",
                            ),
                            encoding="utf-8",
                        )
                    evidence = ArtifactEvidence(
                        relative.as_posix(),
                        "sha256:"
                        + hashlib.sha256(artifact.read_bytes()).hexdigest(),
                    )
                    return StageExecutionResult(
                        (evidence,),
                        {
                            evidence_name: evidence
                            for evidence_name in STAGE_POLICY_BY_STAGE[
                                stage
                            ].completion_evidence
                        },
                    )

                result = coordinate_non_public_authoring_stage(
                    invocation_context="non-public-test-harness",
                    target_stage="plan",
                    store=store,
                    repository_root=store.repository_root,
                    parent_authorization_id="auth-authoring",
                    capability_id=f"cap-{stage}",
                    stage=stage,
                    occurrence={"kind": "singleton"},
                    basis=basis,
                    affected_path_roots=(
                        "docs/changes/2026-07-20-example/"
                        if stage == "architecture-assessment"
                        else "docs/plans/",
                    ),
                    mutation_categories=(
                        stage_mutation_category,
                    ),
                    derived_at="2026-07-22T00:01:00Z",
                    transition_id=f"transition-{stage}",
                    input_identities=inputs,
                    invoke_stage=invoke,
                    synchronize_canonical_state=lambda stage_result: CanonicalSyncResult(
                        "synchronized", stage_result.completion_evidence
                    ),
                    pre_plan=PrePlanEvidence(
                        positions=positions,
                        review_outcomes={
                            "proposal-review": "approved",
                            "spec-review": "approved",
                        },
                        review_resolution_closed=True,
                        architecture_applicability="not-required",
                    ),
                )
                persisted = store.read().automation
                receipt = persisted["transition_receipts"][
                    f"transition-{stage}"
                ]
                recovered = evaluate_receipt_recovery(
                    persisted,
                    f"transition-{stage}",
                    completion_evidence={
                        "outputs": copy.deepcopy(receipt["outputs"]),
                        "canonical_sync": copy.deepcopy(
                            receipt["canonical_sync"]
                        ),
                    },
                    repository_root=store.repository_root,
                )
                self.assertEqual(result.coordination.status, "completed")
                self.assertEqual(
                    (recovered.action, recovered.reason),
                    ("continue", "completed-evidence-current"),
                )

    def test_proposal_correction_uses_bound_capability_and_receipt(self) -> None:
        accepted = ["BRF-1"]
        classifications = {"BRF-1": "mechanical"}
        correction_plans = {
            "BRF-1": {
                "classification": "mechanical",
                "rationale": "The requested change is deterministic and bounded.",
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
        identity = lambda value: "sha256:" + hashlib.sha256(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        target = bind_target("spec", bound_at="2026-07-22T00:00:00Z")
        parent = create_parent_authorization(
            authorization_id="auth-correction",
            authorization_class="authoring",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-22T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=("proposal-correction", "proposal-review"),
            maximum_path_roots=(
                "docs/proposals/",
                "docs/changes/2026-07-20-example/",
            ),
            maximum_mutation_categories=(
                "proposal-content",
                "change-local-review-evidence",
            ),
            correction_budget=budget,
        )
        relative = Path("docs/proposals/2026-07-20-example.md")
        state = copy.deepcopy(FIXTURES.valid_automation())
        state["run"]["target"] = target
        state["parent_authorizations"] = {"auth-correction": parent}
        state["effective_capabilities"] = {}
        state["transition_receipts"] = {}
        store = self.make_store(state)
        proposal = store.repository_root / relative
        proposal.parent.mkdir(parents=True, exist_ok=True)
        proposal.write_text(
            (ROOT / "docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md").read_text(),
            encoding="utf-8",
        )
        proposal_before = "sha256:" + hashlib.sha256(proposal.read_bytes()).hexdigest()
        review_path, resolution_path, review_identity = (
            self.write_proposal_correction_evidence(
                store,
                proposal_path=relative.as_posix(),
            )
        )
        snapshot = store.read()
        replacement = copy.deepcopy(snapshot.automation)
        replacement["observed_identities"] = {
            "proposal": proposal_before,
            "proposal-review": review_identity,
        }
        store.replace_automation(
            replacement,
            expected_document_identity=snapshot.document_identity,
        )
        budget_identity = identity(budget)
        basis = {
            "reviewed_proposal_identity": proposal_before,
            "review_record_identity": review_identity,
            "accepted_finding_set_identity": identity(accepted),
            "classifier_policy_identity": identity(correction_plans),
            "correction_budget_identity": budget_identity,
            "affected_proposal_roots": ["docs/proposals/"],
        }
        capability = derive_effective_capability(
            capability_id="cap-correction-transaction",
            parent=parent,
            stage="proposal",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("docs/proposals/",),
            mutation_categories=("proposal-content",),
            correction_budget=budget,
            correction_budget_identity=budget_identity,
            derived_at="2026-07-22T00:01:00Z",
        )
        capability["scope"].update(
            {
                "review_record_path": review_path,
                "review_resolution_path": resolution_path,
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
        state = store.read().automation
        state["effective_capabilities"] = {capability["capability_id"]: capability}
        store.replace_automation(state, expected_document_identity=store.read().document_identity)
        inputs = dict(
            basis,
            proposal=proposal_before,
            **{
                "proposal-review": review_identity,
                "review_outcome": "changes-requested",
                "review_identity": review_identity,
                "accepted_finding_set_identity": identity(accepted),
                "correction_budget_state": "remaining",
                "correction_budget_identity": budget_identity,
            },
        )

        def invoke() -> StageExecutionResult:
            proposal.write_text(proposal.read_text() + "\n", encoding="utf-8")
            evidence = ArtifactEvidence(
                relative.as_posix(),
                "sha256:" + hashlib.sha256(proposal.read_bytes()).hexdigest(),
            )
            return StageExecutionResult((evidence,), {"proposal": evidence})

        result = workflow_automation_module.resume_public_run(
            store=store,
            command="$workflow auto: spec",
            repository_root=store.repository_root,
            stage="proposal",
            capability_id="cap-correction-transaction",
            occurrence={"kind": "singleton"},
            basis=basis,
            affected_path_roots=("docs/proposals/",),
            mutation_categories=("proposal-content",),
            derived_at="2026-07-22T00:01:00Z",
            transition_id="transition-correction-001",
            input_identities=inputs,
            invoke_stage=invoke,
            synchronize_canonical_state=lambda stage_result: CanonicalSyncResult(
                "synchronized", stage_result.completion_evidence
            ),
            pre_plan=PrePlanEvidence(
                positions={"proposal": (proposal_before,), "proposal-review": (review_identity,)},
                review_outcomes={"proposal-review": "changes-requested"},
                review_resolution_closed=True,
                architecture_applicability="not-required",
            ),
        )
        self.assertEqual(
            (
                result["transitions_attempted"][-1]["status"],
                result["next_action"],
            ),
            ("completed", "proposal-review"),
        )
        persisted = store.read().automation
        self.assertEqual(persisted["transition_receipts"]["transition-correction-001"]["status"], "completed")
        self.assertEqual(persisted["effective_capabilities"]["cap-correction-transaction"]["status"], "consumed")
        fresh = [
            capability
            for capability in persisted["effective_capabilities"].values()
            if capability["capability_kind"] == "proposal-review"
            and capability["status"] == "active"
        ]
        self.assertEqual(len(fresh), 1)
        self.assertEqual(
            fresh[0]["basis"]["proposal_identity"],
            persisted["transition_receipts"]["transition-correction-001"][
                "canonical_sync"
            ]["observed_identities"]["proposal"],
        )

    def test_proposal_correction_post_mutation_failures_pause_durably(self) -> None:
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="transition-fresh-review-authority",
            allow_rereview=False,
        )
        store = fixture["store"]
        proposal = fixture["proposal"]
        proposal_before = proposal.read_bytes()
        coordination = dict(fixture["coordination"])
        with self.assertRaisesRegex(
            AutomationContractError, "proposal correction paused"
        ):
            coordinate_non_public_authoring_stage(**coordination)

        persisted = store.read().automation
        self.assertEqual(persisted["run"]["status"], "paused")
        self.assertEqual(
            persisted["transition_receipts"][
                "transition-fresh-review-authority"
            ]["status"],
            "paused",
        )
        self.assertEqual(
            persisted["effective_capabilities"][
                "cap-correction-transaction"
            ]["status"],
            "invalidated",
        )
        self.assertFalse(
            any(
                capability["capability_kind"] == "proposal-review"
                and capability["status"] == "active"
                for capability in persisted[
                    "effective_capabilities"
                ].values()
            )
        )
        self.assertEqual(proposal.read_bytes(), proposal_before)

    def test_proposal_correction_executes_bound_recipe_without_caller_callback(
        self,
    ) -> None:
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="transition-bound-recipe"
        )
        store = fixture["store"]
        proposal = fixture["proposal"]
        before = proposal.read_bytes()
        escaped = store.repository_root / "scripts/escaped-link"
        callback_invoked = False

        def invoke() -> StageExecutionResult:
            nonlocal callback_invoked
            callback_invoked = True
            escaped.parent.mkdir(parents=True, exist_ok=True)
            escaped.symlink_to(proposal)
            raise RuntimeError("untrusted correction callback executed")

        coordination = dict(fixture["coordination"])
        coordination["invoke_stage"] = invoke
        result = coordinate_non_public_authoring_stage(**coordination)

        self.assertFalse(callback_invoked)
        self.assertFalse(escaped.exists())
        self.assertEqual(proposal.read_bytes(), before + b"\n")
        self.assertEqual(result.coordination.status, "completed")
        persisted = store.read().automation
        self.assertEqual(
            persisted["transition_receipts"]["transition-bound-recipe"]["status"],
            "completed",
        )

    def assert_public_proposal_correction_recovers_after_process_loss_without_replay(
        self,
        *,
        recovery_derived_at: str | None,
    ) -> None:
        class SimulatedProcessLoss(BaseException):
            pass

        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        change = root / "docs/changes/2026-07-20-example/change.yaml"
        change.parent.mkdir(parents=True)
        change.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Proposal correction recovery fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                }
            ),
            encoding="utf-8",
        )
        store = WorkflowAutomationStateStore(change, repository_root=root)
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="transition-correction-recovery",
            store=store,
            public_authorization=True,
        )
        proposal = fixture["proposal"]
        proposal_before = proposal.read_bytes()
        review_record = root / fixture["review_path"]
        review_before = review_record.read_bytes()
        public_request = dict(fixture["coordination"])
        for field in (
            "invocation_context",
            "target_stage",
            "store",
            "repository_root",
            "parent_authorization_id",
        ):
            public_request.pop(field)

        real_replace = workflow_automation_module._atomic_replace_regular_file

        def interrupt_after_proposal_write(path: Path, content: bytes) -> None:
            real_replace(path, content)
            raise SimulatedProcessLoss("process lost after proposal replacement")

        with patch(
            "workflow_automation._atomic_replace_regular_file",
            side_effect=interrupt_after_proposal_write,
        ):
            with self.assertRaisesRegex(
                SimulatedProcessLoss,
                "process lost after proposal replacement",
            ):
                workflow_automation_module.resume_public_run(
                    store,
                    "$workflow auto: spec",
                    repository_root=root,
                    **public_request,
                )

        proposal_after = proposal.read_bytes()
        proposal_after_identity = (
            "sha256:" + hashlib.sha256(proposal_after).hexdigest()
        )
        prepared = store.read().automation
        receipt = prepared["transition_receipts"][
            "transition-correction-recovery"
        ]
        self.assertEqual(receipt["status"], "prepared")
        self.assertEqual(
            prepared["effective_capabilities"][
                "cap-correction-transaction"
            ]["status"],
            "active",
        )
        self.assertEqual(proposal_after, proposal_before + b"\n")

        recovery_completion_evidence = {
            "input_identities": copy.deepcopy(receipt["input_identities"]),
            "expected_postcondition": copy.deepcopy(
                receipt["expected_postcondition"]
            ),
            "outputs": [
                {
                    "path": fixture["proposal_relative"].as_posix(),
                    "identity": proposal_after_identity,
                }
            ],
            "canonical_sync": {
                "status": "synchronized",
                "evidence": {
                    "proposal": {
                        "path": fixture["proposal_relative"].as_posix(),
                        "identity": proposal_after_identity,
                    }
                },
                "observed_identities": {
                    "proposal": proposal_after_identity,
                },
            },
        }
        public_request["recovery_completion_evidence"] = (
            recovery_completion_evidence
        )
        if recovery_derived_at is None:
            public_request.pop("derived_at")
        else:
            public_request["derived_at"] = recovery_derived_at

        with patch(
            "workflow_automation._atomic_replace_regular_file",
            side_effect=AssertionError(
                "recovery replayed the proposal correction"
            ),
        ):
            result = workflow_automation_module.resume_public_run(
                store,
                "$workflow auto: spec",
                repository_root=root,
                **public_request,
            )

        recovered = store.read().automation
        recovered_receipt = recovered["transition_receipts"][
            "transition-correction-recovery"
        ]
        self.assertEqual(
            list(recovered["transition_receipts"]),
            ["transition-correction-recovery"],
        )
        self.assertEqual(recovered_receipt["status"], "completed")
        self.assertEqual(
            recovered_receipt["canonical_sync"]["observed_identities"][
                "proposal"
            ],
            proposal_after_identity,
        )
        self.assertEqual(
            recovered["effective_capabilities"][
                "cap-correction-transaction"
            ]["status"],
            "consumed",
        )
        fresh_review_capabilities = [
            capability
            for capability in recovered["effective_capabilities"].values()
            if capability["capability_kind"] == "proposal-review"
            and capability["status"] == "active"
        ]
        self.assertEqual(len(fresh_review_capabilities), 1)
        self.assertEqual(
            fresh_review_capabilities[0]["basis"]["proposal_identity"],
            proposal_after_identity,
        )
        self.assertEqual(
            fresh_review_capabilities[0]["derived_at"],
            "2026-07-22T00:01:00Z",
        )
        self.assertEqual(proposal.read_bytes(), proposal_after)
        self.assertEqual(review_record.read_bytes(), review_before)
        self.assertEqual(
            result["transitions_attempted"][-1]["transition_id"],
            "transition-correction-recovery",
        )

    def test_public_proposal_correction_recovery_ignores_altered_resume_timestamp(
        self,
    ) -> None:
        self.assert_public_proposal_correction_recovers_after_process_loss_without_replay(
            recovery_derived_at="2099-01-01T00:00:00Z",
        )

    def test_public_proposal_correction_recovery_does_not_require_resume_timestamp(
        self,
    ) -> None:
        self.assert_public_proposal_correction_recovers_after_process_loss_without_replay(
            recovery_derived_at=None,
        )

    def test_proposal_correction_atomic_replace_failure_leaves_no_mutation(
        self,
    ) -> None:
        fixture = self.prepare_proposal_correction_transaction(
            transition_id="transition-atomic-replace-failure"
        )
        store = fixture["store"]
        proposal = fixture["proposal"]
        before = proposal.read_bytes()
        coordination = dict(fixture["coordination"])

        with patch(
            "workflow_automation._replace_file",
            side_effect=OSError("simulated atomic replace failure"),
        ):
            with self.assertRaisesRegex(
                OSError, "simulated atomic replace failure"
            ):
                coordinate_non_public_authoring_stage(**coordination)

        self.assertEqual(proposal.read_bytes(), before)
        self.assertEqual(
            list(proposal.parent.glob(f".{proposal.name}.*.tmp")),
            [],
        )
        persisted = store.read().automation
        self.assertEqual(
            persisted["transition_receipts"][
                "transition-atomic-replace-failure"
            ]["status"],
            "failed",
        )
        self.assertEqual(
            persisted["effective_capabilities"][
                "cap-correction-transaction"
            ]["status"],
            "active",
        )

    def test_authoring_non_public_harness_routes_through_test_spec_review(self) -> None:
        cases = (
            ("proposal-review", "approved", "spec"),
            ("spec", None, "spec-review"),
            ("spec-review", "approved", "architecture-assessment"),
            ("plan", None, "plan-review"),
            ("plan-review", "approved", "test-spec"),
            ("test-spec", None, "test-spec-review"),
        )
        for current_stage, review_outcome, expected in cases:
            with self.subTest(stage=current_stage):
                capability = (
                    "proposal-review" if current_stage == "proposal-review" else "post-proposal-authoring"
                )
                decision = evaluate_non_public_authoring_route(
                    current_stage=current_stage,
                    target_stage="test-spec-review",
                    capability_kind=capability,
                    capability_status="active",
                    invocation_context="non-public-test-harness",
                    review_outcome=review_outcome,
                )
                self.assertEqual((decision.status, decision.next_stage), ("continue", expected))

        boundary = evaluate_non_public_authoring_route(
            current_stage="test-spec-review",
            target_stage="verify",
            capability_kind="post-proposal-authoring",
            capability_status="active",
            invocation_context="non-public-test-harness",
            review_outcome="approved",
        )
        self.assertEqual(boundary.status, "paused")
        self.assertEqual(boundary.pause_reason, "implementation-authorization-required")

    def test_authoring_conditional_architecture_routes(self) -> None:
        required = evaluate_non_public_authoring_route(
            current_stage="architecture-assessment",
            target_stage="plan",
            capability_kind="post-proposal-authoring",
            capability_status="active",
            invocation_context="non-public-test-harness",
            architecture_applicability="required",
        )
        self.assertEqual(required.next_stage, "architecture")
        skipped = evaluate_non_public_authoring_route(
            current_stage="architecture-assessment",
            target_stage="plan",
            capability_kind="post-proposal-authoring",
            capability_status="active",
            invocation_context="non-public-test-harness",
            architecture_applicability="not-required",
        )
        self.assertEqual((skipped.next_stage, skipped.record_not_applicable), ("plan", True))
        explicit = evaluate_non_public_authoring_route(
            current_stage="architecture-assessment",
            target_stage="architecture",
            capability_kind="post-proposal-authoring",
            capability_status="active",
            invocation_context="non-public-test-harness",
            architecture_applicability="not-required",
        )
        self.assertEqual(explicit.status, "target-not-applicable")
        ambiguous = evaluate_non_public_authoring_route(
            current_stage="architecture-assessment",
            target_stage="plan",
            capability_kind="post-proposal-authoring",
            capability_status="active",
            invocation_context="non-public-test-harness",
            architecture_applicability="unknown",
        )
        self.assertEqual(ambiguous.pause_reason, "architecture-applicability-ambiguous")

    def test_non_public_authoring_harness_rejects_public_direct_and_legacy_entry(self) -> None:
        for context in ("public-command", "direct-skill", "bugfix", "legacy-adapter"):
            with self.subTest(context=context):
                decision = evaluate_non_public_authoring_route(
                    current_stage="proposal-review",
                    target_stage="spec",
                    capability_kind="proposal-review",
                    capability_status="active",
                    invocation_context=context,
                    review_outcome="approved",
                )
                self.assertEqual(decision.status, "paused")
                self.assertEqual(decision.pause_reason, "non-public-harness-required")

        store = self.make_store(copy.deepcopy(FIXTURES.valid_automation()))
        before = store.read().document_identity
        for context in ("public-command", "direct-skill", "bugfix", "legacy-adapter"):
            with self.subTest(transaction_context=context), self.assertRaisesRegex(
                AutomationContractError, "non-public authoring harness"
            ):
                coordinate_non_public_authoring_stage(
                    invocation_context=context,
                    target_stage="spec",
                    store=store,
                    repository_root=store.repository_root,
                )
        self.assertEqual(store.read().document_identity, before)

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

    def test_implementation_correction_uses_review_recipe_and_prepared_receipt(
        self,
    ) -> None:
        automation = copy.deepcopy(FIXTURES.valid_automation())
        plan = ActivePlanContext.from_text(
            plan_text(
                current_state="resolution-needed",
                next_stage="review-resolution M2",
            ),
            plan_identity="sha256:plan-m2-resolution",
        )
        target = bind_target(
            "code-review",
            bound_at="2026-07-24T00:00:00Z",
            plan=plan,
        )
        budget = {"cycles": 1}
        budget_identity = "sha256:" + hashlib.sha256(
            json.dumps(
                budget, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        parent = create_parent_authorization(
            authorization_id="auth-implementation-correction",
            authorization_class="implementation",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-24T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=("implementation-correction",),
            maximum_path_roots=(
                "scripts/",
                "docs/changes/2026-07-20-example/",
            ),
            maximum_mutation_categories=(
                "production-code",
                "change-local-review-evidence",
            ),
            correction_budget=budget,
        )
        automation["run"]["target"] = target
        automation["parent_authorizations"] = {
            parent["authorization_id"]: parent
        }
        automation["effective_capabilities"] = {}
        automation["transition_receipts"] = {}
        automation["observed_identities"] = {
            "plan": "sha256:plan-m2-resolution"
        }
        store = self.make_store(automation)
        source = store.repository_root / "scripts/example.py"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("old_name = 1\n", encoding="utf-8")
        corrected = b"new_name = 1\n"
        corrected_identity = (
            "sha256:" + hashlib.sha256(corrected).hexdigest()
        )
        change_root = (
            store.repository_root / "docs/changes/2026-07-20-example"
        )
        review = change_root / "reviews/code-review-m2-r1.md"
        review.parent.mkdir(parents=True, exist_ok=True)
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
                "identity": corrected_identity,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        review.write_text(
            f"""# Code review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: M2 R1
Reviewer: fixture reviewer
Target: M2 implementation
Reviewed milestone: M2. Implementation
Status: changes-requested
Material findings: CR-M2-1

## Material Findings

### CR-M2-1 - Exact rename

Finding ID: CR-M2-1
Severity: major
Evidence: old_name remains in the implementation
Required outcome: apply the exact reviewed rename
Safe resolution path: execute the closed reviewer recipe
auto_fix_class: mechanical
auto_fix_kind: formatter-output
affected_paths: scripts/example.py
deterministic_authority: {authority}
required_validation: {validation}
""",
            encoding="utf-8",
        )
        review_log = change_root / "review-log.md"
        review_log.write_text(
            """# Review Log

### Review entry
Review ID: code-review-m2-r1
Stage: code-review
Round: M2 R1
Status: changes-requested
Detailed record: reviews/code-review-m2-r1.md
Resolution: review-resolution.md#code-review-m2-r1
Material findings: CR-M2-1
Open findings: CR-M2-1
""",
            encoding="utf-8",
        )
        resolution = change_root / "review-resolution.md"
        resolution.write_text(
            """# Review Resolution

Closeout status: open
Review closeout: code-review-m2-r1

### code-review-m2-r1

Finding ID: CR-M2-1
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: review-resolution
Rationale: the reviewer supplied a bounded deterministic rename
Chosen action: execute the exact reviewer recipe
Validation target: SHA-256 identity and independent rereview
Validation evidence: pending

### older-review

Finding ID: OLDER-OPEN
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: review-resolution
Rationale: older unrelated work remains open
Chosen action: complete the older correction separately
Validation target: older review validation
Validation evidence: pending
""",
            encoding="utf-8",
        )

        result = workflow_automation_module.resume_public_run(
            store=store,
            command="$workflow auto: code-review",
            repository_root=store.repository_root,
            stage="review-resolution",
            capability_id="cap-implementation-correction-m2-r1",
            review_record_path=review.relative_to(
                store.repository_root
            ).as_posix(),
            review_resolution_path=resolution.relative_to(
                store.repository_root
            ).as_posix(),
            review_log_path=review_log.relative_to(
                store.repository_root
            ).as_posix(),
            affected_path_roots=(
                "scripts/",
                "docs/changes/2026-07-20-example/",
            ),
            mutation_categories=(
                "production-code",
                "change-local-review-evidence",
            ),
            correction_budget=budget,
            correction_budget_identity=budget_identity,
            derived_at="2026-07-24T00:01:00Z",
            transition_id="transition-implementation-correction-m2-r1",
            active_plan=plan,
        )

        self.assertEqual(source.read_bytes(), corrected)
        self.assertIn("Closeout status: open", resolution.read_text())
        self.assertIn("Status: open", resolution.read_text())
        self.assertIn("Open findings: None", review_log.read_text())
        self.assertEqual(
            (
                result["transitions_attempted"][-1]["status"],
                result["stage_outcome"],
                result["next_action"],
            ),
            ("completed", "continue", "code-review"),
        )
        persisted = store.read().automation
        assert persisted is not None
        receipt = persisted["transition_receipts"][
            "transition-implementation-correction-m2-r1"
        ]
        self.assertEqual(receipt["status"], "completed")
        self.assertEqual(
            receipt["effective_capability_id"],
            "cap-implementation-correction-m2-r1",
        )
        self.assertEqual(
            persisted["effective_capabilities"][
                "cap-implementation-correction-m2-r1"
            ]["status"],
            "consumed",
        )
        with self.assertRaisesRegex(
            AutomationContractError, "finding set is not current"
        ):
            coordinate_non_public_implementation_correction(
                invocation_context="non-public-test-harness",
                target_stage="code-review",
                target_milestone_id="M2",
                store=store,
                repository_root=store.repository_root,
                parent_authorization_id=parent["authorization_id"],
                capability_id="cap-implementation-correction-m2-stale",
                review_record_path=review.relative_to(
                    store.repository_root
                ).as_posix(),
                review_resolution_path=resolution.relative_to(
                    store.repository_root
                ).as_posix(),
                review_log_path=review_log.relative_to(
                    store.repository_root
                ).as_posix(),
                affected_path_roots=(
                    "scripts/",
                    "docs/changes/2026-07-20-example/",
                ),
                mutation_categories=(
                    "production-code",
                    "change-local-review-evidence",
                ),
                correction_budget=budget,
                correction_budget_identity=budget_identity,
                derived_at="2026-07-24T00:02:00Z",
                transition_id="transition-implementation-correction-m2-stale",
                active_plan=plan,
            )
        paused = store.read().automation
        assert paused is not None
        self.assertEqual(
            (paused["run"]["status"], paused["run"]["pause_reason"]),
            ("paused", "implementation-correction-paused"),
        )

    def test_active_plan_rejects_duplicate_milestone_identity(self) -> None:
        with self.assertRaisesRegex(
            AutomationContractError, "duplicate active plan milestone"
        ):
            ActivePlanContext.from_text(
                plan_text(duplicate_m2=True),
                plan_identity="sha256:duplicate-plan",
            )

    def test_verification_readiness_is_repository_backed(self) -> None:
        store = self.make_store(copy.deepcopy(FIXTURES.valid_automation()))
        root = store.repository_root

        def artifact(relative: str, content: str) -> tuple[str, str]:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return relative, "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

        source_path, source_identity = artifact(
            "scripts/final-code.py",
            "final_value = 1\n",
        )
        code_state_provider = FixtureCodeStateProvider((source_path,))
        final_code_state = code_state_provider.snapshot(root)
        final_code_identity = final_code_state.identity
        plan_path, plan_identity = artifact(
            "docs/plans/closed.md",
            plan_text(
                current="M3. Later Slice",
                current_state="closed",
                remaining="M3",
                next_stage="verify",
                milestone_two_state="closed",
                milestone_three_state="closed",
            ),
        )
        review_path, review_identity = artifact(
            "docs/changes/2026-07-20-example/reviews/code-review-final-r1.md",
            f"""# Final code review

Review ID: code-review-final-r1
Stage: code-review
Round: final R1
Reviewer: fixture reviewer
Target: final implementation
Status: approved
Material findings: None
Review scope: final-holistic
complete_final_diff: reviewed
cross_milestone_interactions: reviewed
governing_artifacts: reviewed
review_resolutions: closed
final_validation_selection: reviewed
generated_and_derived_artifacts: current
cross_milestone_scope: reviewed
Reviewed commit: fixture-reviewed
Final code identity: {final_code_identity}
""",
        )
        artifact(
            "docs/changes/2026-07-20-example/review-log.md",
            """# Review Log

### Review entry
Review ID: code-review-final-r1
Stage: code-review
Round: final R1
Status: approved
Detailed record: reviews/code-review-final-r1.md
Resolution: none
Material findings: None
Open findings: None
""",
        )
        explanation_path, explanation_identity = artifact(
            "docs/changes/2026-07-20-example/explain-change.md",
            "Stage: explain-change\nStatus: current\n"
            f"Final diff identity: {final_code_identity}\n"
            f"Final review identity: {review_identity}\n"
            f"Reviewed subject revision: {final_code_state.reviewed_revision}\n"
            "Explanation basis: sha256:explanation-basis\n"
            "Validation-evidence cutoff: sha256:validation-cutoff\n",
        )
        promotion_path, promotion_identity = artifact(
            "docs/changes/2026-07-20-example/promotion-evidence.md",
            "Stage: promotion\nStatus: valid\n"
            f"Final code identity: {final_code_identity}\n",
        )
        branch_path, branch_identity = artifact(
            "docs/changes/2026-07-20-example/branch-state.md",
            "Stage: branch-state\nStatus: current\n"
            f"Final code identity: {final_code_identity}\n"
            f"Final code paths: {json.dumps([source_path])}\n"
            f"Final code anchor identity: {final_code_state.anchor_identity}\n"
            f"Final code base revision: {final_code_state.base_revision}\n"
            f"Final code reviewed revision: {final_code_state.reviewed_revision}\n",
        )
        commands_path, commands_identity = artifact(
            "docs/changes/2026-07-20-example/verification-commands.md",
            "Stage: verification-commands\nStatus: current\n"
            f"Final code identity: {final_code_identity}\n",
        )
        basis = {
            "closed_milestones_identity": plan_identity,
            "final_code_review_identity": review_identity,
            "promotion_evidence_identity": promotion_identity,
            "explanation_inputs_identity": explanation_identity,
            "branch_state_identity": branch_identity,
            "verification_commands_identity": commands_identity,
        }
        paths = {
            "closed_milestones_identity": plan_path,
            "final_code_review_identity": review_path,
            "promotion_evidence_identity": promotion_path,
            "explanation_inputs_identity": explanation_path,
            "branch_state_identity": branch_path,
            "verification_commands_identity": commands_path,
        }
        readiness = resolve_verification_readiness(
            repository_root=root,
            basis=basis,
            basis_paths=paths,
            code_state_provider=code_state_provider,
        )
        self.assertTrue(readiness.final_review_clean)
        self.assertTrue(readiness.explanation_current)

        explanation_file = root / explanation_path
        original_explanation = explanation_file.read_text(encoding="utf-8")
        explanation_file.write_text(
            original_explanation.replace(
                f"Reviewed subject revision: {final_code_state.reviewed_revision}",
                "Reviewed subject revision: stale-reviewed-subject",
            ),
            encoding="utf-8",
        )
        stale_subject_basis = dict(basis)
        stale_subject_basis["explanation_inputs_identity"] = (
            "sha256:" + hashlib.sha256(explanation_file.read_bytes()).hexdigest()
        )
        with self.assertRaisesRegex(
            AutomationContractError, "explanation is not current"
        ):
            resolve_verification_readiness(
                repository_root=root,
                basis=stale_subject_basis,
                basis_paths=paths,
                code_state_provider=code_state_provider,
            )
        explanation_file.write_text(original_explanation, encoding="utf-8")

        branch_file = root / branch_path
        original_branch = branch_file.read_text(encoding="utf-8")
        branch_file.write_text(
            original_branch.replace(
                final_code_state.anchor_identity,
                "sha256:stale-anchor",
            ),
            encoding="utf-8",
        )
        stale_anchor_basis = dict(basis)
        stale_anchor_basis["branch_state_identity"] = (
            "sha256:" + hashlib.sha256(branch_file.read_bytes()).hexdigest()
        )
        with self.assertRaisesRegex(
            AutomationContractError, "anchor projection is stale"
        ):
            resolve_verification_readiness(
                repository_root=root,
                basis=stale_anchor_basis,
                basis_paths=paths,
                code_state_provider=code_state_provider,
            )
        branch_file.write_text(original_branch, encoding="utf-8")

        omitted_path, _omitted_identity = artifact(
            "scripts/omitted-final-code.py",
            "omitted = True\n",
        )
        with self.assertRaisesRegex(
            AutomationContractError, "path projection is incomplete"
        ):
            resolve_verification_readiness(
                repository_root=root,
                basis=basis,
                basis_paths=paths,
                code_state_provider=FixtureCodeStateProvider(
                    (source_path, omitted_path)
                ),
            )

        source_file = root / source_path
        source_file.write_text("final_value = 2\n", encoding="utf-8")
        with self.assertRaisesRegex(
            AutomationContractError, "final code identity is stale"
        ):
            resolve_verification_readiness(
                repository_root=root,
                basis=basis,
                basis_paths=paths,
                code_state_provider=code_state_provider,
            )
        source_file.write_text("final_value = 1\n", encoding="utf-8")

        review_file = root / review_path
        original_review = review_file.read_text(encoding="utf-8")
        review_file.write_text(
            original_review.replace(
                "complete_final_diff: reviewed",
                "complete_final_diff: future-value",
            ),
            encoding="utf-8",
        )
        semantic_basis = dict(basis)
        semantic_review_identity = (
            "sha256:" + hashlib.sha256(review_file.read_bytes()).hexdigest()
        )
        semantic_basis["final_code_review_identity"] = semantic_review_identity
        explanation_file.write_text(
            "Stage: explain-change\nStatus: current\n"
            f"Final diff identity: {final_code_identity}\n"
            f"Final review identity: {semantic_review_identity}\n"
            f"Reviewed subject revision: {final_code_state.reviewed_revision}\n"
            "Explanation basis: sha256:explanation-basis\n"
            "Validation-evidence cutoff: sha256:validation-cutoff\n",
            encoding="utf-8",
        )
        semantic_basis["explanation_inputs_identity"] = (
            "sha256:" + hashlib.sha256(explanation_file.read_bytes()).hexdigest()
        )
        with self.assertRaisesRegex(
            AutomationContractError, "final review is not clean"
        ):
            resolve_verification_readiness(
                repository_root=root,
                basis=semantic_basis,
                basis_paths=paths,
                code_state_provider=code_state_provider,
            )

        review_file.write_text(original_review, encoding="utf-8")
        (root / explanation_path).write_text(
            "Stage: explain-change\nStatus: current\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            AutomationContractError, "verification basis identity"
        ):
            resolve_verification_readiness(
                repository_root=root,
                basis=basis,
                basis_paths=paths,
                code_state_provider=code_state_provider,
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

    def test_implementation_transaction_uses_stage_native_milestone_proof(self) -> None:
        automation = copy.deepcopy(FIXTURES.valid_automation())
        target = {
            "stage": "verify",
            "occurrence": {"kind": "final"},
            "bound_at": "2026-07-24T00:00:00Z",
            "completion": target_completion_predicate("verify"),
        }
        automation["run"]["target"] = copy.deepcopy(target)
        parent = automation["parent_authorizations"]["authorization-authoring-001"]
        parent.update(
            {
                "authorization_class": "implementation",
                "maximum_target": copy.deepcopy(target),
                "allowed_capability_kinds": ["implementation"],
                "maximum_path_roots": ["scripts/", "docs/plans/"],
                "maximum_mutation_categories": ["production-code"],
            }
        )
        automation["effective_capabilities"] = {}
        store = self.make_store(automation)

        pre_plan_text = plan_text(
            current="M2. Engine Slice",
            current_state="implementing",
            remaining="M2, M3",
            next_stage="implement M2",
        )
        plan_relative = Path("docs/plans/m5-plan.md")
        plan_path = store.repository_root / plan_relative
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(pre_plan_text, encoding="utf-8")
        plan_identity = "sha256:" + hashlib.sha256(plan_path.read_bytes()).hexdigest()
        active_plan = ActivePlanContext.from_text(
            pre_plan_text, plan_identity=plan_identity
        )
        snapshot = store.read()
        replacement = copy.deepcopy(snapshot.automation)
        replacement["canonical_position_source"] = (
            "plan-current-handoff-summary"
        )
        replacement["observed_identities"] = {"plan": plan_identity}
        store.replace_automation(
            replacement,
            expected_document_identity=snapshot.document_identity,
        )
        basis = {
            "plan_identity": plan_identity,
            "plan_review_identity": "sha256:plan-review",
            "test_spec_identity": "sha256:test-spec",
            "test_spec_review_identity": "sha256:test-spec-review",
            "milestone_identity": "sha256:M2",
            "affected_paths_identity": "sha256:paths",
            "mutation_categories_identity": "sha256:categories",
            "validation_commands_identity": "sha256:commands",
        }

        def write_artifact(relative: str, content: str) -> ArtifactEvidence:
            path = store.repository_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return ArtifactEvidence(
                relative,
                "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
            )

        def invoke() -> StageExecutionResult:
            implementation = write_artifact(
                "scripts/m5-implementation.txt", "M2 implementation\n"
            )
            validation = write_artifact(
                "scripts/m5-validation.txt",
                "Stage: implement\nMilestone: M2\nResult: passed\n",
            )
            plan = write_artifact(
                plan_relative.as_posix(),
                plan_text(
                    current="M2. Engine Slice",
                    current_state="review-requested",
                    remaining="M2, M3",
                    next_stage="code-review M2",
                ),
            )
            self.write_plan_state_owner(
                store,
                plan_path=plan_relative.as_posix(),
                milestone_id="M2",
                milestone_state="review-requested",
            )
            return StageExecutionResult(
                (implementation, validation, plan),
                {
                    "implementation-diff": implementation,
                    "validation": validation,
                    "plan-handoff": plan,
                },
            )

        result = workflow_automation_module.resume_public_run(
            store=store,
            command="$workflow auto: verify",
            repository_root=store.repository_root,
            stage="implement",
            capability_id="capability-implementation-M2",
            occurrence={"kind": "milestone", "milestone_id": "M2"},
            basis=basis,
            affected_path_roots=("scripts/", "docs/plans/"),
            mutation_categories=("production-code",),
            derived_at="2026-07-24T00:01:00Z",
            transition_id="transition-implementation-M2",
            input_identities={
                **basis,
                "plan": plan_identity,
                "source_milestone_id": "M1",
                "next_milestone_id": "M2",
                "milestone_order_identity": "sha256:milestone-order",
                "source_milestone_identity": "sha256:M1",
                "next_milestone_identity": "sha256:M2",
            },
            invoke_stage=invoke,
            active_plan=active_plan,
            synchronize_canonical_state=lambda execution: CanonicalSyncResult(
                "synchronized", execution.completion_evidence
            ),
        )
        self.assertEqual(
            (
                result["transitions_attempted"][-1]["status"],
                result["stage_outcome"],
                result["next_action"],
            ),
            ("completed", "continue", "code-review"),
        )
        persisted = store.read().automation
        assert persisted is not None
        self.assertEqual(
            persisted["observed_identities"],
            {
                "plan": "sha256:"
                + hashlib.sha256(plan_path.read_bytes()).hexdigest()
            },
        )
        self.assertEqual(
            persisted["effective_capabilities"][
                "capability-implementation-M2"
            ]["status"],
            "consumed",
        )

    def test_code_review_transaction_closes_only_its_bound_milestone(self) -> None:
        automation = copy.deepcopy(FIXTURES.valid_automation())
        target = {
            "stage": "verify",
            "occurrence": {"kind": "final"},
            "bound_at": "2026-07-24T00:00:00Z",
            "completion": target_completion_predicate("verify"),
        }
        automation["run"]["target"] = copy.deepcopy(target)
        parent = automation["parent_authorizations"]["authorization-authoring-001"]
        parent.update(
            {
                "authorization_class": "implementation",
                "maximum_target": copy.deepcopy(target),
                "allowed_capability_kinds": ["implementation"],
                "maximum_path_roots": [
                    "docs/changes/2026-07-20-example/",
                    "docs/plans/",
                ],
                "maximum_mutation_categories": [
                    "change-local-review-evidence"
                ],
            }
        )
        automation["effective_capabilities"] = {}
        store = self.make_store(automation)
        pre_text = plan_text(
            current="M2. Engine Slice",
            current_state="review-requested",
            remaining="M2, M3",
            next_stage="code-review M2",
        )
        plan_path = store.repository_root / "docs/plans/m5-review-plan.md"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(pre_text, encoding="utf-8")
        plan_identity = "sha256:" + hashlib.sha256(plan_path.read_bytes()).hexdigest()
        active_plan = ActivePlanContext.from_text(
            pre_text, plan_identity=plan_identity
        )
        snapshot = store.read()
        replacement = copy.deepcopy(snapshot.automation)
        replacement["canonical_position_source"] = (
            "plan-current-handoff-summary"
        )
        replacement["observed_identities"] = {"plan": plan_identity}
        store.replace_automation(
            replacement,
            expected_document_identity=snapshot.document_identity,
        )
        basis = {
            "plan_identity": plan_identity,
            "plan_review_identity": "sha256:plan-review",
            "test_spec_identity": "sha256:test-spec",
            "test_spec_review_identity": "sha256:test-spec-review",
            "milestone_identity": "sha256:M2",
            "affected_paths_identity": "sha256:paths",
            "mutation_categories_identity": "sha256:categories",
            "validation_commands_identity": "sha256:commands",
        }

        def evidence(relative: str, content: str) -> ArtifactEvidence:
            path = store.repository_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return ArtifactEvidence(
                relative,
                "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
            )

        def invoke() -> StageExecutionResult:
            review = evidence(
                "docs/changes/2026-07-20-example/reviews/code-review-m2-r1.md",
                """# Code review

Review ID: code-review-m2-r1
Stage: code-review
Round: M2 R1
Reviewer: fixture reviewer
Target: M2 implementation
Status: approved
Material findings: None
Reviewed milestone: M2. Engine Slice
""",
            )
            review_log = evidence(
                "docs/changes/2026-07-20-example/review-log.md",
                """# Review Log

### Review entry
Review ID: code-review-m2-r1
Stage: code-review
Round: M2 R1
Status: approved
Detailed record: reviews/code-review-m2-r1.md
Resolution: none
Material findings: None
Open findings: None
""",
            )
            plan = evidence(
                "docs/plans/m5-review-plan.md",
                plan_text(
                    current="M3. Later Slice",
                    current_state="planned",
                    remaining="M3",
                    next_stage="implement M3",
                    milestone_two_state="closed",
                ),
            )
            self.write_plan_state_owner(
                store,
                plan_path="docs/plans/m5-review-plan.md",
                milestone_id="M2",
                milestone_state="closed",
            )
            return StageExecutionResult(
                (review, review_log, plan),
                {
                    "code-review": review,
                    "review-resolution": review_log,
                    "plan-handoff": plan,
                },
            )

        result = workflow_automation_module.resume_public_run(
            store=store,
            command="$workflow auto: verify",
            repository_root=store.repository_root,
            stage="code-review",
            capability_id="capability-code-review-M2",
            occurrence={"kind": "milestone", "milestone_id": "M2"},
            basis=basis,
            affected_path_roots=(
                "docs/changes/2026-07-20-example/",
                "docs/plans/",
            ),
            mutation_categories=("change-local-review-evidence",),
            derived_at="2026-07-24T00:02:00Z",
            transition_id="transition-code-review-M2",
            input_identities={
                **basis,
                "plan": plan_identity,
                "source_milestone_id": "M2",
                "source_milestone_identity": "sha256:M2",
            },
            invoke_stage=invoke,
            active_plan=active_plan,
            synchronize_canonical_state=lambda execution: CanonicalSyncResult(
                "synchronized", execution.completion_evidence
            ),
        )
        self.assertEqual(
            (
                result["stage_outcome"],
                result["next_action"],
            ),
            ("continue", "implement"),
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
            explanation_current=True,
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
            explanation_current=True,
        )
        self.assertEqual((passed.status, passed.next_stage), ("target-reached", "pr"))
        self.assertFalse(passed.external_action_performed)

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

    def test_verify_transaction_stops_before_pr_without_external_action(self) -> None:
        automation = copy.deepcopy(FIXTURES.valid_automation())
        target = {
            "stage": "verify",
            "occurrence": {"kind": "final"},
            "bound_at": "2026-07-24T00:00:00Z",
            "completion": target_completion_predicate("verify"),
        }
        verification_basis = {
            "closed_milestones_identity": "sha256:closed-milestones",
            "final_code_review_identity": "sha256:final-review",
            "promotion_evidence_identity": "sha256:promotion",
            "explanation_inputs_identity": "sha256:explanation",
            "branch_state_identity": "sha256:branch",
            "verification_commands_identity": "sha256:commands",
        }
        parent = create_parent_authorization(
            authorization_id="authorization-verification-001",
            authorization_class="verification",
            change_id="2026-07-20-example",
            authorized_by="user",
            authorized_at="2026-07-24T00:00:00Z",
            maximum_target=target,
            allowed_capability_kinds=("verification",),
            maximum_path_roots=("docs/changes/2026-07-20-example/",),
            maximum_mutation_categories=("verification-evidence",),
            verification_basis=verification_basis,
        )
        automation["run"]["target"] = copy.deepcopy(target)
        automation["parent_authorizations"] = {
            parent["authorization_id"]: parent
        }
        automation["effective_capabilities"] = {}
        store = self.make_store(automation)
        closed_text = plan_text(
            current="M3. Later Slice",
            current_state="closed",
            remaining="M3",
            next_stage="verify",
            milestone_two_state="closed",
            milestone_three_state="closed",
        )
        plan_path = store.repository_root / "docs/plans/m5-closed-plan.md"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(closed_text, encoding="utf-8")
        plan_identity = "sha256:" + hashlib.sha256(plan_path.read_bytes()).hexdigest()
        active_plan = ActivePlanContext.from_text(
            closed_text, plan_identity=plan_identity
        )
        snapshot = store.read()
        replacement = copy.deepcopy(snapshot.automation)
        replacement["canonical_position_source"] = (
            "plan-current-handoff-summary"
        )
        replacement["observed_identities"] = {"plan": plan_identity}
        store.replace_automation(
            replacement,
            expected_document_identity=snapshot.document_identity,
        )

        def write_evidence(relative: str, content: str) -> ArtifactEvidence:
            path = store.repository_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return ArtifactEvidence(
                relative,
                "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
            )

        final_source = write_evidence(
            "scripts/final-code.py",
            "final_value = 1\n",
        )
        code_state_provider = FixtureCodeStateProvider((final_source.path,))
        final_code_state = code_state_provider.snapshot(store.repository_root)
        final_code_identity = final_code_state.identity
        final_review = write_evidence(
            "docs/changes/2026-07-20-example/reviews/code-review-final-r1.md",
            f"""# Final code review

Review ID: code-review-final-r1
Stage: code-review
Round: final R1
Reviewer: fixture reviewer
Target: final implementation
Status: approved
Material findings: None
Review scope: final-holistic
complete_final_diff: reviewed
cross_milestone_interactions: reviewed
governing_artifacts: reviewed
review_resolutions: closed
final_validation_selection: reviewed
generated_and_derived_artifacts: current
cross_milestone_scope: reviewed
Reviewed commit: fixture-reviewed
Final code identity: {final_code_identity}
""",
        )
        write_evidence(
            "docs/changes/2026-07-20-example/review-log.md",
            """# Review Log

### Review entry
Review ID: code-review-final-r1
Stage: code-review
Round: final R1
Status: approved
Detailed record: reviews/code-review-final-r1.md
Resolution: none
Material findings: None
Open findings: None
""",
        )
        explanation = write_evidence(
            "docs/changes/2026-07-20-example/explain-change.md",
            "Stage: explain-change\nStatus: current\n"
            f"Final diff identity: {final_code_identity}\n"
            f"Final review identity: {final_review.identity}\n"
            f"Reviewed subject revision: {final_code_state.reviewed_revision}\n"
            "Explanation basis: sha256:explanation-basis\n"
            "Validation-evidence cutoff: sha256:validation-cutoff\n",
        )
        promotion = write_evidence(
            "docs/changes/2026-07-20-example/promotion.md",
            "Stage: promotion\nStatus: valid\n"
            f"Final code identity: {final_code_identity}\n",
        )
        branch = write_evidence(
            "docs/changes/2026-07-20-example/branch-state.md",
            "Stage: branch-state\nStatus: current\n"
            f"Final code identity: {final_code_identity}\n"
            f"Final code paths: {json.dumps([final_source.path])}\n"
            f"Final code anchor identity: {final_code_state.anchor_identity}\n"
            f"Final code base revision: {final_code_state.base_revision}\n"
            f"Final code reviewed revision: {final_code_state.reviewed_revision}\n",
        )
        commands = write_evidence(
            "docs/changes/2026-07-20-example/verification-commands.md",
            "Stage: verification-commands\nStatus: current\n"
            f"Final code identity: {final_code_identity}\n",
        )
        verification_basis = {
            "closed_milestones_identity": plan_identity,
            "final_code_review_identity": final_review.identity,
            "promotion_evidence_identity": promotion.identity,
            "explanation_inputs_identity": explanation.identity,
            "branch_state_identity": branch.identity,
            "verification_commands_identity": commands.identity,
        }
        verification_basis_paths = {
            "closed_milestones_identity": plan_path.relative_to(
                store.repository_root
            ).as_posix(),
            "final_code_review_identity": final_review.path,
            "promotion_evidence_identity": promotion.path,
            "explanation_inputs_identity": explanation.path,
            "branch_state_identity": branch.path,
            "verification_commands_identity": commands.path,
        }

        def invoke() -> StageExecutionResult:
            report = write_evidence(
                "docs/changes/2026-07-20-example/verify-report.md",
                "Stage: verify\nResult: passed\nNext stage: pr\n"
                "External actions performed: no\n",
            )
            validation = write_evidence(
                "docs/changes/2026-07-20-example/verify-validation.md",
                "Stage: verify\nResult: passed\n",
            )
            return StageExecutionResult(
                (report, validation),
                {"verify-report": report, "validation": validation},
            )

        def prohibited_external_action(*_args, **_kwargs):
            raise AssertionError("prohibited external action was invoked")

        real_popen = subprocess.Popen
        expected_git_root = store.repository_root.resolve()

        def allow_read_only_git_probe(command, *args, **kwargs):
            return run_exact_read_only_git_probe(
                command,
                *args,
                expected_root=expected_git_root,
                real_popen=real_popen,
                **kwargs,
            )

        with patch(
            "subprocess.run", side_effect=allow_read_only_git_probe
        ), patch(
            "subprocess.Popen", side_effect=prohibited_external_action
        ), patch(
            "socket.create_connection", side_effect=prohibited_external_action
        ), patch(
            "urllib.request.urlopen", side_effect=prohibited_external_action
        ), patch(
            "os.system", side_effect=prohibited_external_action
        ):
            with self.assertRaisesRegex(
                AssertionError, "prohibited external action"
            ):
                subprocess.Popen(
                    (
                        "git",
                        "-C",
                        str(expected_git_root),
                        "rev-parse",
                        "--show-toplevel",
                    )
                )
            result = workflow_automation_module.resume_public_run(
                store=store,
                command="$workflow auto: verify",
                repository_root=store.repository_root,
                verification_basis_paths=verification_basis_paths,
                code_state_provider=code_state_provider,
                capability_id="capability-verification-001",
                stage="verify",
                occurrence={"kind": "final"},
                basis=verification_basis,
                affected_path_roots=("docs/changes/2026-07-20-example/",),
                mutation_categories=("verification-evidence",),
                derived_at="2026-07-24T00:01:00Z",
                transition_id="transition-verification-001",
                input_identities={**verification_basis, "plan": plan_identity},
                invoke_stage=invoke,
                active_plan=active_plan,
                synchronize_canonical_state=lambda execution: CanonicalSyncResult(
                    "synchronized", execution.completion_evidence
                ),
            )
        self.assertEqual(
            (
                result["transitions_attempted"][-1]["status"],
                result["stage_outcome"],
                result["next_action"],
                result["external_actions"],
            ),
            ("completed", "target-reached", "pr", "prohibited"),
        )

    def test_verify_failure_pauses_durably_without_automatic_repair(self) -> None:
        store = self.make_store(copy.deepcopy(FIXTURES.valid_automation()))
        with patch(
            "workflow_automation.resolve_verification_readiness",
            return_value=VerificationReadiness({}, True, True),
        ), patch(
            "workflow_automation.coordinate_one_stage",
            side_effect=AutomationContractError(
                "stage-native completion verification failed: "
                "stage-native-verification-failed"
            ),
        ), self.assertRaisesRegex(
            AutomationContractError, "automatic repair is prohibited"
        ):
            coordinate_non_public_implementation_stage(
                invocation_context="non-public-test-harness",
                target_stage="verify",
                target_milestone_id=None,
                store=store,
                repository_root=store.repository_root,
                stage="verify",
                basis={},
                verification_basis_paths={},
                code_state_provider=FixtureCodeStateProvider(("unused",)),
            )
        automation = store.read().automation
        assert automation is not None
        self.assertEqual(
            (automation["run"]["status"], automation["run"]["pause_reason"]),
            ("paused", "verification-failed"),
        )

    def test_verify_rejects_foreign_repository_before_readiness(self) -> None:
        store = self.make_store(copy.deepcopy(FIXTURES.valid_automation()))
        foreign = tempfile.TemporaryDirectory()
        self.addCleanup(foreign.cleanup)

        with patch(
            "workflow_automation.resolve_verification_readiness"
        ) as readiness, self.assertRaisesRegex(
            AutomationContractError, "repository root does not match state store"
        ):
            coordinate_non_public_implementation_stage(
                invocation_context="non-public-test-harness",
                target_stage="verify",
                target_milestone_id=None,
                store=store,
                repository_root=Path(foreign.name),
                stage="verify",
                basis={},
                verification_basis_paths={},
                code_state_provider=FixtureCodeStateProvider(("unused",)),
            )

        readiness.assert_not_called()

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

    def synchronize_review(
        self,
        store: WorkflowAutomationStateStore,
        result: StageExecutionResult,
    ) -> CanonicalSyncResult:
        review_evidence = result.completion_evidence["proposal-review"]
        review_text = (
            store.repository_root / review_evidence.path
        ).read_text(encoding="utf-8")
        status_match = re.search(r"^Status:\s*(\S+)\s*$", review_text, re.MULTILINE)
        status = status_match.group(1) if status_match is not None else "approved"
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
Status: {status}
Detailed record: reviews/proposal-review-r1.md
Resolution: none
Material findings: None
Open findings: None
""".format(status=status),
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
        parent_authorization_id="authorization-authoring-001",
        capability_id="capability-engine-001",
        input_identities=None,
        synchronize=None,
        repository_root=None,
        proposal_identity=None,
    ):
        proposal_identity = proposal_identity or self.write_proposal(store)
        receipt_inputs = self.proposal_input_identities(proposal_identity)
        if input_identities is not None:
            receipt_inputs.update(input_identities)
        return coordinate_one_stage(
            store=store,
            parent_authorization_id=parent_authorization_id,
            capability_id=capability_id,
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
