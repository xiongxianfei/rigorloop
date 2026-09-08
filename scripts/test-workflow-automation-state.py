#!/usr/bin/env python3
"""Transaction, recovery, cancellation, and migration tests for automation state."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import os
import sys
import tempfile
import unittest
from pathlib import Path

from lifecycle_state_sync import evaluate_implementation_autoprogression_route

from workflow_automation_policy import (
    STAGE_POLICY_BY_STAGE,
    project_proposal_review_result,
)
from workflow_automation_state import (
    _canonical_review_occurrence,
    _verify_package_review_completion,
    _review_resolution_gate,
    ConcurrentStateChange,
    StateContractError,
    StageOwnedChangeStateStore,
    WorkflowAutomationStateStore,
    compute_transition_key,
    dump_yaml,
    evaluate_receipt_recovery,
    project_automation_status,
    parse_stage_evidence_fields,
    STAGE_NATIVE_VERIFIER_STAGES,
)
from validate_workflow_automation import proposal_review_route_binding


ROOT = Path(__file__).resolve().parents[1]


def _load_fixture_module():
    path = ROOT / "scripts" / "test-validate-workflow-automation.py"
    spec = importlib.util.spec_from_file_location("workflow_automation_test_fixtures", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


FIXTURES = _load_fixture_module()


def valid_automation() -> dict:
    return copy.deepcopy(FIXTURES.valid_automation())


def valid_receipt(state: dict) -> dict:
    holder = copy.deepcopy(state)
    receipt = FIXTURES.add_valid_receipt(holder)
    result = copy.deepcopy(receipt)
    result["transition_key"] = compute_transition_key(result)
    return result


def persist_receipt(state: dict, receipt: dict | None = None) -> dict:
    persisted = receipt or valid_receipt(state)
    state["transition_receipts"] = {persisted["transition_id"]: persisted}
    return persisted


def artifact_evidence() -> dict[str, str]:
    return {
        "path": "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md",
        "identity": "sha256:review-output",
    }


def synchronized_evidence() -> dict[str, object]:
    return {
        "status": "synchronized",
        "evidence": {"proposal-review": artifact_evidence()},
        "observed_identities": {"proposal-review": "sha256:review-output"},
    }


class RetiredStorageAdapterTests(unittest.TestCase):
    def test_canonical_review_occurrence_rejects_stored_basis_but_retains_standalone(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = root / "standalone"
            review = evidence / "reviews/code-review-r1.md"
            review.parent.mkdir(parents=True)
            review.write_text("# Review\n\nReview ID: code-review-r1\nStage: code-review\nRound: 1\nReviewer: Independent reviewer\nTarget: specs/example.md\nStatus: approved\n\n## Findings\n\nNo material findings.\n")
            (evidence / "review-log.md").write_text("# Review Log\n\n### Review entry\nReview ID: code-review-r1\nStage: code-review\nRound: 1\nStatus: approved\nDetailed record: reviews/code-review-r1.md\nResolution: None\nMaterial findings: None\nOpen findings: None\n")
            occurrence = _canonical_review_occurrence(review, repository_root=root)
            self.assertIsNotNone(occurrence)
            self.assertEqual(occurrence[0].status, "approved")
            for marker in ("change.yaml", "change.json"):
                with self.subTest(marker=marker):
                    path = evidence / marker
                    path.write_bytes(b"stored basis must not be decoded\xff")
                    self.assertIsNone(_canonical_review_occurrence(review, repository_root=root))
                    self.assertEqual(path.read_bytes(), b"stored basis must not be decoded\xff")
                    path.unlink()

    def test_legacy_adapters_reject_before_path_access_and_preserve_bytes(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "change.yaml"
            path.write_bytes(b"private archive bytes\xff")
            for factory in (WorkflowAutomationStateStore, StageOwnedChangeStateStore):
                with self.subTest(adapter=factory.__name__):
                    with patch.object(Path, "resolve", side_effect=AssertionError("must not resolve")), patch.object(Path, "read_bytes", side_effect=AssertionError("must not read")):
                        with self.assertRaisesRegex(StateContractError, "storage is unsupported"):
                            factory(path)
                    self.assertEqual(path.read_bytes(), b"private archive bytes\xff")
                    self.assertEqual(list(path.parent.iterdir()), [path])

    def test_v2_does_not_imply_an_automation_storage_mapping(self):
        with self.assertRaisesRegex(StateContractError, "storage is unsupported"):
            WorkflowAutomationStateStore(Path("docs/changes/example/change.json"))


class WorkflowAutomationStateTests(unittest.TestCase):
    def test_v3_phase_boundary_targets_verify_and_rejects_explain_change(self) -> None:
        fixture = {
            "profile": "implementation-through-verify",
            "profile_state": "armed",
            "phase": "B",
            "durable_authorization": "persisted",
            "invocation_context": "workflow-managed",
            "current_stage": "final-clean-code-review",
            "authoring_gates": "completed",
            "plan_review_status": "approved",
            "plan_review_recording": "recorded",
            "plan_synchronized": True,
            "milestones_ordered": True,
            "working_tree_baseline": "recorded",
            "unrelated_dirty_state": "absent",
            "required_commands_approved": True,
            "governing_findings_open": False,
            "artifact_placement_unambiguous": True,
            "workflow_state_synchronized": True,
            "milestones": [{"id": "M1", "state": "closed"}],
            "lifecycle_contract": "stage-owned-change-local-v3",
        }
        result = evaluate_implementation_autoprogression_route(fixture)
        self.assertEqual(result.stop_reason, "phase-boundary-verify")
        fixture["current_stage"] = "explain-change"
        result = evaluate_implementation_autoprogression_route(fixture)
        self.assertEqual(result.stop_reason, "stage-unknown_value:explain-change")
        fixture["lifecycle_contract"] = "future-v9"
        result = evaluate_implementation_autoprogression_route(fixture)
        self.assertIn("unknown_value", result.stop_reason)

    def test_stage_native_verifier_registry_covers_internal_m5_stages(self) -> None:
        self.assertEqual(
            STAGE_NATIVE_VERIFIER_STAGES,
            frozenset(
                {
                    "proposal",
                    "proposal-review",
                    "architecture",
                    "spec",
                    "design-review",
                    "plan",
                    "delivery-review",
                    "implement",
                    "code-review",
                    "review-resolution",
                    "ci-maintenance",
                    "final-holistic-code-review",
                    "verify",
                }
            ),
        )

    def test_stage_evidence_rejects_duplicate_and_conflicting_fields(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "validation.md"
        path.write_text(
            "Stage: implement\nMilestone: M2\nResult: passed\nResult: failed\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(StateContractError, "duplicate evidence field"):
            parse_stage_evidence_fields(
                path,
                required_fields={"Stage", "Milestone", "Result"},
            )




    def package_review_completion_fixture(self, kind: str, *, lifecycle_contract: str = "stage-owned-change-local-v3"):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        stage = f"{kind}-review"
        review_id = f"{stage}-r1"
        change_root = root / "docs/changes/2026-07-20-example"
        review_path = change_root / f"reviews/{review_id}.md"
        review_path.parent.mkdir(parents=True)
        members = (
            {"architecture": "docs/architecture/example.md", "spec": "specs/example.md"}
            if kind == "design"
            else (
                {"plan": "docs/plans/example.md", "test-spec": "specs/example.test.md"}
                if lifecycle_contract == "stage-owned-change-local-v1"
                else {"plan": "docs/plans/example.md"}
            )
        )
        for member_path in members.values():
            member = root / member_path
            member.parent.mkdir(parents=True, exist_ok=True)
            member.write_text(f"# {member_path}\n", encoding="utf-8")
        upstream = "proposal-review-r1" if kind == "design" else "design-review-r1"
        review_path.write_text(
            f"""# {stage}

Review ID: {review_id}
Stage: {stage}
Round: r1
Reviewer authority: {stage}
Package kind: {kind}
Package members: {", ".join(f"{key}={value}" for key, value in members.items())}
Upstream review ID: {upstream}
Status: approved
Material findings: none
Correction targets: none
Recording status: recorded
""",
            encoding="utf-8",
        )
        review_identity = "sha256:" + hashlib.sha256(review_path.read_bytes()).hexdigest()
        (change_root / "review-log.md").write_text(
            f"""# Review Log

### Review entry

Review ID: {review_id}
Stage: {stage}
Round: r1
Status: approved
Detailed record: reviews/{review_id}.md
Resolution: not-required
Material findings: none
Open findings: none
Recording status: recorded
""",
            encoding="utf-8",
        )
        artifact_states = {
            "proposal": {"kind": "proposal", "role": "primary", "path": "docs/proposals/example.md", "lifecycle_state": "accepted", "review": {"id": "proposal-review-r1", "outcome": "approved"}},
            "architecture": {"kind": "architecture", "role": "primary", "path": "docs/architecture/example.md"},
            "spec": {"kind": "spec", "role": "primary", "path": "specs/example.md"},
            "plan": {"kind": "plan", "role": "primary", "path": "docs/plans/example.md"},
        }
        if lifecycle_contract == "stage-owned-change-local-v1":
            artifact_states["test-spec"] = {"kind": "test-spec", "role": "primary", "path": "specs/example.test.md"}
        registration = {
            "review_id": review_id,
            "round": "r1",
            "outcome": "approved",
            "reviewer_authority": stage,
            "package_kind": kind,
            "members": members,
            "upstream_review_id": upstream,
            "evidence_path": review_path.relative_to(root).as_posix(),
            "evidence_sha256": review_identity.removeprefix("sha256:"),
            "stage_authority": stage,
        }
        artifact_registrations = {
            artifact_id: {
                "artifact_path": entry["path"],
                "artifact_kind": entry["kind"],
                "artifact_role": entry["role"],
            }
            for artifact_id, entry in artifact_states.items()
        }
        document = {
            "change_id": "2026-07-20-example",
            "lifecycle_contract": lifecycle_contract,
            "artifact_states": artifact_states,
            "review_packages": {"design": {"status": "approved", "authority": "granted", "review_id": "design-review-r1"}} if kind == "delivery" else {},
            "lifecycle_cli": {"artifacts": artifact_registrations, "package_reviews": {kind: registration}},
        }
        (change_root / "change.yaml").write_text(dump_yaml(document), encoding="utf-8")
        evidence = {"path": review_path.relative_to(root).as_posix(), "identity": review_identity}
        return root, review_path, review_identity, evidence
















    def test_transition_key_is_order_independent_and_input_bound(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        reordered = dict(reversed(list(receipt.items())))
        reordered["input_identities"] = dict(
            reversed(list(receipt["input_identities"].items()))
        )
        self.assertEqual(compute_transition_key(reordered), receipt["transition_key"])
        changed = copy.deepcopy(receipt)
        changed["input_identities"]["proposal"] = "sha256:changed"
        self.assertNotEqual(compute_transition_key(changed), receipt["transition_key"])

        changed = copy.deepcopy(receipt)
        changed["retry_policy"] = "idempotent-retry"
        self.assertNotEqual(compute_transition_key(changed), receipt["transition_key"])


    def test_recovery_rejects_tampered_transition_key(self) -> None:
        state = valid_automation()
        receipt = persist_receipt(state)
        receipt["input_identities"] = {"proposal": "sha256:tampered-after-key"}
        decision = evaluate_receipt_recovery(
            state,
            receipt["transition_id"],
            completion_evidence=None,
        )
        self.assertEqual(decision.action, "fail-closed")
        self.assertEqual(decision.reason, "transition-key-mismatch")





    def test_recovery_rejects_unpersisted_or_substituted_receipt_identity(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        self.assertEqual(
            evaluate_receipt_recovery(
                state, receipt["transition_id"], completion_evidence=None
            ).reason,
            "transition-receipt-not-found",
        )

        persist_receipt(state, receipt)
        self.assertEqual(
            evaluate_receipt_recovery(
                state, "transition-substituted", completion_evidence=None
            ).reason,
            "transition-receipt-not-found",
        )

    def test_recovery_rejects_retry_policy_projection_mismatch(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        receipt["retry_policy"] = "idempotent-retry"
        receipt["transition_key"] = compute_transition_key(receipt)
        persist_receipt(state, receipt)
        decision = evaluate_receipt_recovery(
            state, receipt["transition_id"], completion_evidence=None
        )
        self.assertEqual(decision.action, "fail-closed")
        self.assertEqual(decision.reason, "retry-policy-projection-mismatch")

    def test_recovery_fails_closed_on_partial_or_identity_drift(self) -> None:
        state = valid_automation()
        receipt = persist_receipt(state)
        partial = evaluate_receipt_recovery(
            state,
            receipt["transition_id"],
            completion_evidence={"partial": True, "outputs": ["one"]},
        )
        self.assertEqual(partial.action, "fail-closed")
        drift = evaluate_receipt_recovery(
            state,
            receipt["transition_id"],
            completion_evidence={
                "input_identities": {"proposal": "sha256:changed"},
                "expected_postcondition": copy.deepcopy(receipt["expected_postcondition"]),
                "outputs": ["sha256:review-output"],
                "canonical_sync": {"status": "synchronized"},
            },
        )
        self.assertEqual(drift.action, "pause")

    def test_completed_recovery_pauses_on_output_identity_drift(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        receipt.update(
            status="completed",
            outputs=[artifact_evidence()],
            canonical_sync=synchronized_evidence(),
        )
        persist_receipt(state, receipt)
        decision = evaluate_receipt_recovery(
            state,
            receipt["transition_id"],
            completion_evidence={
                "outputs": ["sha256:changed"],
                "canonical_sync": {"status": "synchronized"},
            },
        )
        self.assertEqual(decision.action, "pause")




























    def test_status_projection_is_read_only_and_complete(self) -> None:
        state = valid_automation()
        state["transition_receipts"] = {"transition-001": valid_receipt(state)}
        state["run"]["stop_reason"] = "authorization-required"
        state["run"]["pause_reason"] = "authorization-required"
        state["canonical_position_source"] = "artifact-review-evidence"
        state["observed_identities"] = {"proposal": "sha256:proposal"}
        state["latest_review_result"] = {
            "outcome": "changes-requested",
            "clean_gate": "not-satisfied",
            "routing_action": "pause",
        }
        before = copy.deepcopy(state)
        projection = project_automation_status(state)
        self.assertEqual(projection["target"]["stage"], "proposal-review")
        self.assertEqual(projection["authorization_boundary"], "authoring")
        self.assertEqual(projection["canonical_position_source"], "artifact-review-evidence")
        self.assertEqual(projection["latest_evidence_identities"], {"proposal": "sha256:proposal"})
        self.assertEqual(projection["in_flight_transition"], "transition-001")
        self.assertEqual(projection["pause_reason"], "authorization-required")
        self.assertEqual(projection["latest_review_result"]["clean_gate"], "not-satisfied")
        self.assertEqual(state, before)










class StageOwnedChangeStateStoreTests(unittest.TestCase):

    def current_parts(self):
        artifacts = {
            "proposal": {
                "kind": "proposal",
                "path": "docs/proposals/example.md",
                "role": "primary",
                "lifecycle_state": "accepted",
                "review": {
                    "id": "proposal-review-r1",
                    "artifact_id": "proposal",
                    "outcome": "approved",
                    "record": "docs/changes/example/reviews/proposal-review-r1.md",
                    "round": "r1",
                },
            }
        }
        state = {
            "lifecycle_state": "active",
            "current_stage": "spec",
            "next_stage": "design-review",
            "blocker": None,
            "evidence": ["docs/changes/example/reviews/proposal-review-r1.md"],
        }
        automation = {
            "mechanism": "bounded-review-fix",
            "target": {
                "stage": "verify",
                "occurrence": {"kind": "final"},
                "bound_at": "2026-07-29T00:00:00Z",
                "completion": {
                    "rule": "verification passes and the final explanation is recorded"
                },
            },
            "status": "active",
            "current_stage": "spec",
            "stop_reason": None,
            "evidence": [],
        }
        return artifacts, state, automation







if __name__ == "__main__":
    unittest.main()
