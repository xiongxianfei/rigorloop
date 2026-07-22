#!/usr/bin/env python3
"""Transaction, recovery, cancellation, and migration tests for automation state."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from workflow_automation_policy import STAGE_POLICY_BY_STAGE
from workflow_automation_state import (
    ConcurrentStateChange,
    StateContractError,
    WorkflowAutomationStateStore,
    compute_transition_key,
    dump_yaml,
    evaluate_receipt_recovery,
    project_automation_status,
)


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


class WorkflowAutomationStateTests(unittest.TestCase):
    def make_store(self, automation: dict | None = None, *, legacy: dict | None = None):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "change.yaml"
        document = {
            "change_id": "2026-07-20-example",
            "title": "State adapter fixture",
            "classification": "default",
            "risk": "medium",
            "review": {"status": "resolved", "unresolved_items": 0},
            "workflow": {},
            "unrelated": {"owner": "keep-me", "count": 7},
        }
        if automation is not None:
            document["workflow"]["automation"] = automation
        if legacy is not None:
            document["workflow"]["autoprogression"] = legacy
        path.write_text(dump_yaml(document), encoding="utf-8")
        return WorkflowAutomationStateStore(path), path

    def materialize_valid_review_completion(
        self,
        store: WorkflowAutomationStateStore,
        *,
        transition_id: str = "transition-001",
    ) -> dict[str, object]:
        root = store.repository_root
        proposal_relative = Path("docs/proposals/example.md")
        proposal = root / proposal_relative
        proposal.parent.mkdir(parents=True, exist_ok=True)
        proposal.write_text("# Example proposal\n", encoding="utf-8")
        proposal_identity = "sha256:" + hashlib.sha256(proposal.read_bytes()).hexdigest()

        review_relative = Path(
            "docs/changes/2026-07-20-example/reviews/proposal-review-r1.md"
        )
        review = root / review_relative
        review.parent.mkdir(parents=True, exist_ok=True)
        review.write_text(
            """# Proposal review

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: fixture reviewer
Target: docs/proposals/example.md
Status: approved
Material findings: None
""",
            encoding="utf-8",
        )
        review_identity = "sha256:" + hashlib.sha256(review.read_bytes()).hexdigest()
        evidence = {"path": review_relative.as_posix(), "identity": review_identity}
        change_root = review.parent.parent
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

        snapshot = store.read()
        replacement = copy.deepcopy(snapshot.automation)
        receipt = replacement["transition_receipts"][transition_id]
        receipt["input_identities"]["proposal"] = proposal_identity
        receipt["transition_key"] = compute_transition_key(receipt)
        capability = replacement["effective_capabilities"][
            receipt["effective_capability_id"]
        ]
        capability["basis"]["proposal_identity"] = proposal_identity
        store.replace_automation(
            replacement, expected_document_identity=snapshot.document_identity
        )
        return {
            "input_identities": copy.deepcopy(receipt["input_identities"]),
            "expected_postcondition": copy.deepcopy(receipt["expected_postcondition"]),
            "outputs": [copy.deepcopy(evidence)],
            "canonical_sync": {
                "status": "synchronized",
                "evidence": {"proposal-review": copy.deepcopy(evidence)},
                "observed_identities": {"proposal-review": review_identity},
            },
        }

    def test_store_infers_canonical_repository_root_from_change_path(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        path = root / "docs/changes/2026-07-20-example/change.yaml"
        path.parent.mkdir(parents=True)
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-example",
                    "title": "Canonical state fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                    "workflow": {},
                }
            ),
            encoding="utf-8",
        )

        store = WorkflowAutomationStateStore(path)

        self.assertEqual(store.repository_root, root.resolve())
        self.assertEqual(store.read().document["change_id"], "2026-07-20-example")

    def test_store_rejects_canonical_change_directory_identity_mismatch(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        path = root / "docs/changes/2026-07-20-example/change.yaml"
        path.parent.mkdir(parents=True)
        path.write_text(
            dump_yaml(
                {
                    "change_id": "2026-07-20-other",
                    "title": "Mismatched state fixture",
                    "classification": "default",
                    "risk": "medium",
                    "review": {"status": "resolved", "unresolved_items": 0},
                    "workflow": {},
                }
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            StateContractError, "change_id must match its canonical change directory"
        ):
            WorkflowAutomationStateStore(path).read()

    def test_prepare_persists_receipt_before_caller_can_invoke_stage(self) -> None:
        state = valid_automation()
        store, _ = self.make_store(state)
        snapshot = store.read()

        result = store.prepare_transition(
            valid_receipt(state), expected_document_identity=snapshot.document_identity
        )

        self.assertEqual(result.status, "prepared")
        persisted = store.read().automation
        self.assertEqual(
            persisted["transition_receipts"]["transition-001"]["effective_capability_id"],
            "capability-proposal-review-001",
        )

    def test_prepare_rejects_second_in_flight_transition(self) -> None:
        state = valid_automation()
        first = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": first}
        store, _ = self.make_store(state)
        second = copy.deepcopy(first)
        second["transition_id"] = "transition-002"
        second["transition_key"] = compute_transition_key(second)

        with self.assertRaisesRegex(StateContractError, "one transition may be in flight"):
            store.prepare_transition(
                second, expected_document_identity=store.read().document_identity
            )

    def test_prepare_rejects_invalidated_effective_capability(self) -> None:
        state = valid_automation()
        state["effective_capabilities"]["capability-proposal-review-001"]["status"] = "invalidated"
        store, _ = self.make_store(state)

        with self.assertRaisesRegex(StateContractError, "effective capability must be active"):
            store.prepare_transition(
                valid_receipt(valid_automation()),
                expected_document_identity=store.read().document_identity,
            )

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

    def test_canonical_read_rejects_tampered_prepared_and_completed_keys(self) -> None:
        for status in ("prepared", "completed"):
            with self.subTest(status=status):
                state = valid_automation()
                receipt = valid_receipt(state)
                if status == "completed":
                    receipt.update(
                        status="completed",
                        outputs=[artifact_evidence()],
                        canonical_sync=synchronized_evidence(),
                    )
                    state["effective_capabilities"][
                        "capability-proposal-review-001"
                    ]["status"] = "consumed"
                persist_receipt(state, receipt)
                receipt["expected_postcondition"] = {
                    "review_occurrence": "tampered-after-key"
                }
                store, _ = self.make_store(state)
                with self.assertRaisesRegex(
                    StateContractError, "transition_key.*immutable operation inputs"
                ):
                    store.read()

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

    def test_prepare_rejects_transition_key_not_bound_to_inputs(self) -> None:
        state = valid_automation()
        store, _ = self.make_store(state)
        receipt = valid_receipt(state)
        receipt["transition_key"] = "sha256:stale"
        with self.assertRaisesRegex(StateContractError, "transition key"):
            store.prepare_transition(
                receipt, expected_document_identity=store.read().document_identity
            )

    def test_recovery_reconciles_valid_completion_without_retry(self) -> None:
        state = valid_automation()
        persist_receipt(state)
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        snapshot = store.read()
        receipt = snapshot.automation["transition_receipts"]["transition-001"]
        decision = evaluate_receipt_recovery(
            snapshot.automation,
            receipt["transition_id"],
            completion_evidence=evidence,
            repository_root=store.repository_root,
        )
        self.assertEqual(decision.action, "reconcile-completed")
        self.assertFalse(decision.invoke_stage)

    def test_recovery_rejects_nonexistent_stage_evidence(self) -> None:
        state = valid_automation()
        persist_receipt(state)
        store, _ = self.make_store(state)
        snapshot = store.read()
        receipt = snapshot.automation["transition_receipts"]["transition-001"]
        decision = evaluate_receipt_recovery(
            snapshot.automation,
            receipt["transition_id"],
            completion_evidence={
                "input_identities": copy.deepcopy(receipt["input_identities"]),
                "expected_postcondition": copy.deepcopy(
                    receipt["expected_postcondition"]
                ),
                "outputs": [artifact_evidence()],
                "canonical_sync": synchronized_evidence(),
            },
            repository_root=store.repository_root,
        )
        self.assertEqual(decision.action, "pause")
        self.assertEqual(decision.reason, "stage-completion-artifact-invalid")

    def test_recovery_retries_only_idempotent_policy_without_evidence(self) -> None:
        cases = []

        state = valid_automation()
        receipt = FIXTURES.configure_post_proposal_transition(
            state,
            stage_name="architecture-assessment",
            target_stage="plan",
        )
        receipt["from_position"] = "spec-review"
        receipt["input_identities"] = {
            "spec": "sha256:spec",
            "spec-review": "sha256:spec-review",
        }
        receipt["transition_key"] = compute_transition_key(receipt)
        cases.append(("architecture-assessment", state, "retry"))

        state = valid_automation()
        persist_receipt(state)
        cases.append(("proposal-review", state, "pause"))

        state = valid_automation()
        receipt = FIXTURES.configure_next_milestone_transition(
            state, milestone_id="M2"
        )
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
        cases.append(("implement", state, "manual-recovery"))

        mismatch_policy = {
            "architecture-assessment": "reconcile-only",
            "proposal-review": "idempotent-retry",
            "implement": "reconcile-only",
        }
        for stage_name, state, expected_action in cases:
            with self.subTest(stage=stage_name):
                store, _ = self.make_store(state)
                snapshot = store.read()
                receipt = snapshot.automation["transition_receipts"]["transition-001"]
                self.assertEqual(
                    evaluate_receipt_recovery(
                        snapshot.automation,
                        receipt["transition_id"],
                        completion_evidence=None,
                    ).action,
                    expected_action,
                )

                mismatched = copy.deepcopy(state)
                mismatched_receipt = mismatched["transition_receipts"]["transition-001"]
                mismatched_receipt["retry_policy"] = mismatch_policy[stage_name]
                mismatched_receipt["transition_key"] = compute_transition_key(
                    mismatched_receipt
                )
                mismatch_store, _ = self.make_store(mismatched)
                with self.assertRaisesRegex(
                    StateContractError, "retry_policy.*immutable stage policy"
                ):
                    mismatch_store.read()

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

    def test_completed_recovery_pauses_when_canonical_review_log_disappears(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        store.finalize_transition(
            "transition-001",
            status="completed",
            outputs=evidence["outputs"],
            canonical_sync_status="synchronized",
            canonical_sync_evidence=evidence["canonical_sync"]["evidence"],
            canonical_sync_observed_identities=evidence["canonical_sync"][
                "observed_identities"
            ],
            expected_document_identity=store.read().document_identity,
        )
        (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        ).unlink()
        snapshot = store.read()
        completed = snapshot.automation["transition_receipts"]["transition-001"]

        decision = evaluate_receipt_recovery(
            snapshot.automation,
            "transition-001",
            completion_evidence={
                "outputs": copy.deepcopy(completed["outputs"]),
                "canonical_sync": copy.deepcopy(completed["canonical_sync"]),
            },
            repository_root=store.repository_root,
        )

        self.assertEqual(decision.action, "pause")
        self.assertEqual(decision.reason, "canonical-review-log-missing")

    def test_prepared_recovery_rejects_external_canonical_review_log_symlink(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        review_log = (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        )
        with tempfile.TemporaryDirectory() as external_name:
            external_log = Path(external_name) / "review-log.md"
            external_log.write_bytes(review_log.read_bytes())
            review_log.unlink()
            review_log.symlink_to(external_log)

            decision = evaluate_receipt_recovery(
                store.read().automation,
                "transition-001",
                completion_evidence=evidence,
                repository_root=store.repository_root,
            )

        self.assertEqual(decision.action, "pause")
        self.assertEqual(decision.reason, "canonical-review-log-path-invalid")

    def test_cancel_does_not_consume_external_review_log_symlink(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        review_log = (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        )
        with tempfile.TemporaryDirectory() as external_name:
            external_log = Path(external_name) / "review-log.md"
            external_log.write_bytes(review_log.read_bytes())
            review_log.unlink()
            review_log.symlink_to(external_log)

            result = store.cancel(
                cancelled_by="user",
                cancelled_at="2026-07-22T00:00:00Z",
                completion_evidence=evidence,
                expected_document_identity=store.read().document_identity,
            )

        persisted = store.read().automation
        self.assertEqual(result.status, "reconciliation-required")
        self.assertEqual(
            persisted["transition_receipts"]["transition-001"]["status"],
            "prepared",
        )
        self.assertEqual(
            persisted["effective_capabilities"]["capability-proposal-review-001"][
                "status"
            ],
            "active",
        )

    def test_prepared_recovery_rejects_in_repository_review_log_symlink(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        review_log = (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        )
        alternate = store.repository_root / "docs/changes/alternate/review-log.md"
        alternate.parent.mkdir(parents=True)
        alternate.write_bytes(review_log.read_bytes())
        review_log.unlink()
        review_log.symlink_to(alternate)

        decision = evaluate_receipt_recovery(
            store.read().automation,
            "transition-001",
            completion_evidence=evidence,
            repository_root=store.repository_root,
        )

        self.assertEqual(decision.action, "pause")
        self.assertEqual(decision.reason, "canonical-review-log-path-invalid")

    def test_prepared_recovery_rejects_mismatched_review_occurrence_round(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        review_log = (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        )
        review_log.write_text(
            review_log.read_text(encoding="utf-8").replace(
                "Round: r1", "Round: r2"
            ),
            encoding="utf-8",
        )

        decision = evaluate_receipt_recovery(
            store.read().automation,
            "transition-001",
            completion_evidence=evidence,
            repository_root=store.repository_root,
        )

        self.assertEqual(decision.action, "pause")
        self.assertEqual(decision.reason, "canonical-review-occurrence-mismatch")

    def test_completed_recovery_pauses_on_canonical_review_log_identity_drift(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        store.finalize_transition(
            "transition-001",
            status="completed",
            outputs=evidence["outputs"],
            canonical_sync_status="synchronized",
            canonical_sync_evidence=evidence["canonical_sync"]["evidence"],
            canonical_sync_observed_identities=evidence["canonical_sync"][
                "observed_identities"
            ],
            expected_document_identity=store.read().document_identity,
        )
        review_log = (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        )
        review_log.write_text(
            review_log.read_text(encoding="utf-8") + "\n<!-- audit note -->\n",
            encoding="utf-8",
        )
        snapshot = store.read()
        completed = snapshot.automation["transition_receipts"]["transition-001"]

        decision = evaluate_receipt_recovery(
            snapshot.automation,
            "transition-001",
            completion_evidence={
                "outputs": copy.deepcopy(completed["outputs"]),
                "canonical_sync": copy.deepcopy(completed["canonical_sync"]),
            },
            repository_root=store.repository_root,
        )

        self.assertEqual(decision.action, "pause")
        self.assertEqual(decision.reason, "canonical-review-log-identity-drift")

    def test_completed_recovery_continues_with_current_engine_derived_proof(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        store.finalize_transition(
            "transition-001",
            status="completed",
            outputs=evidence["outputs"],
            canonical_sync_status="synchronized",
            canonical_sync_evidence=evidence["canonical_sync"]["evidence"],
            canonical_sync_observed_identities=evidence["canonical_sync"][
                "observed_identities"
            ],
            expected_document_identity=store.read().document_identity,
        )
        snapshot = store.read()
        completed = snapshot.automation["transition_receipts"]["transition-001"]

        decision = evaluate_receipt_recovery(
            snapshot.automation,
            "transition-001",
            completion_evidence={
                "outputs": copy.deepcopy(completed["outputs"]),
                "canonical_sync": copy.deepcopy(completed["canonical_sync"]),
            },
            repository_root=store.repository_root,
        )

        self.assertEqual(decision.action, "continue")
        self.assertEqual(decision.reason, "completed-evidence-current")
        self.assertIsNotNone(decision.verified_completion)

    def test_finalize_consumes_capability_only_with_completed_receipt(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)

        store.finalize_transition(
            "transition-001",
            status="completed",
            outputs=evidence["outputs"],
            canonical_sync_status="synchronized",
            canonical_sync_evidence=evidence["canonical_sync"]["evidence"],
            canonical_sync_observed_identities=evidence["canonical_sync"][
                "observed_identities"
            ],
            expected_document_identity=store.read().document_identity,
        )

        persisted = store.read().automation
        self.assertEqual(persisted["transition_receipts"]["transition-001"]["status"], "completed")
        self.assertEqual(
            persisted["effective_capabilities"]["capability-proposal-review-001"]["status"],
            "consumed",
        )

    def test_finalize_rejects_foreign_repository_root_before_mutation(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        foreign = tempfile.TemporaryDirectory()
        self.addCleanup(foreign.cleanup)
        foreign_root = Path(foreign.name)
        shutil.copytree(store.repository_root / "docs", foreign_root / "docs")
        before = store.read()

        with self.assertRaisesRegex(
            StateContractError, "repository root does not match state store"
        ):
            store.finalize_transition(
                "transition-001",
                status="completed",
                outputs=evidence["outputs"],
                canonical_sync_status="synchronized",
                canonical_sync_evidence=evidence["canonical_sync"]["evidence"],
                canonical_sync_observed_identities=evidence["canonical_sync"][
                    "observed_identities"
                ],
                expected_document_identity=before.document_identity,
                repository_root=foreign_root,
            )

        after = store.read()
        self.assertEqual(after.document_identity, before.document_identity)
        self.assertEqual(
            after.automation["transition_receipts"]["transition-001"]["status"],
            "prepared",
        )
        self.assertEqual(
            after.automation["effective_capabilities"][
                "capability-proposal-review-001"
            ]["status"],
            "active",
        )

    def test_finalize_persists_engine_derived_canonical_review_log_identity(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        evidence["canonical_sync"]["observed_identities"][
            "proposal-review-log"
        ] = "sha256:caller-fabricated"

        store.finalize_transition(
            "transition-001",
            status="completed",
            outputs=evidence["outputs"],
            canonical_sync_status="synchronized",
            canonical_sync_evidence=evidence["canonical_sync"]["evidence"],
            canonical_sync_observed_identities=evidence["canonical_sync"][
                "observed_identities"
            ],
            expected_document_identity=store.read().document_identity,
        )

        persisted = store.read().automation
        observed = persisted["transition_receipts"]["transition-001"][
            "canonical_sync"
        ]["observed_identities"]
        review_log = (
            store.repository_root
            / "docs/changes/2026-07-20-example/review-log.md"
        )
        expected = "sha256:" + hashlib.sha256(review_log.read_bytes()).hexdigest()
        self.assertEqual(observed["proposal-review-log"], expected)

    def test_cancel_revokes_authority_and_preserves_receipts(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        receipt.update(
            status="completed",
            outputs=[artifact_evidence()],
            canonical_sync=synchronized_evidence(),
        )
        state["effective_capabilities"]["capability-proposal-review-001"]["status"] = "consumed"
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)

        result = store.cancel(
            cancelled_by="user",
            cancelled_at="2026-07-22T00:00:00Z",
            expected_document_identity=store.read().document_identity,
        )

        persisted = store.read().automation
        self.assertEqual(result.status, "cancelled")
        self.assertEqual(persisted["run"]["status"], "cancelled")
        self.assertEqual(
            persisted["parent_authorizations"]["authorization-authoring-001"]["status"],
            "revoked",
        )
        self.assertIn("transition-001", persisted["transition_receipts"])

    def test_cancel_is_idempotent_and_completed_run_is_immutable(self) -> None:
        state = valid_automation()
        state["run"]["status"] = "cancelled"
        store, path = self.make_store(state)
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        result = store.cancel(cancelled_by="user", cancelled_at="2026-07-22T00:00:00Z")
        self.assertEqual(result.status, "cancelled")
        self.assertFalse(result.mutated)
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)

        completed = valid_automation()
        completed["run"]["status"] = "completed"
        completed["effective_capabilities"]["capability-proposal-review-001"]["status"] = "consumed"
        store, _ = self.make_store(completed)
        result = store.cancel(cancelled_by="user", cancelled_at="2026-07-22T00:00:00Z")
        self.assertEqual(result.status, "already-completed")
        self.assertFalse(result.mutated)

    def test_cancel_pauses_when_prepared_transition_cannot_be_reconciled(self) -> None:
        state = valid_automation()
        state["transition_receipts"] = {"transition-001": valid_receipt(state)}
        store, _ = self.make_store(state)
        result = store.cancel(
            cancelled_by="user",
            cancelled_at="2026-07-22T00:00:00Z",
            completion_evidence=None,
            expected_document_identity=store.read().document_identity,
        )
        self.assertEqual(result.status, "reconciliation-required")
        self.assertFalse(result.mutated)
        self.assertEqual(store.read().automation["run"]["status"], "active")

    def test_cancel_rejects_stale_transition_key_before_mutation(self) -> None:
        state = valid_automation()
        receipt = persist_receipt(state)
        receipt["expected_postcondition"] = {
            "review_occurrence": "tampered-after-key"
        }
        store, path = self.make_store(state)
        before = path.read_bytes()

        with self.assertRaisesRegex(
            StateContractError, "transition_key.*immutable operation inputs"
        ):
            store.cancel(
                cancelled_by="user",
                cancelled_at="2026-07-22T00:00:00Z",
            )
        self.assertEqual(path.read_bytes(), before)

    def test_cancel_reconciles_valid_prepared_completion_then_cancels(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = self.materialize_valid_review_completion(store)
        result = store.cancel(
            cancelled_by="user",
            cancelled_at="2026-07-22T00:00:00Z",
            completion_evidence=evidence,
            expected_document_identity=store.read().document_identity,
        )
        persisted = store.read().automation
        self.assertEqual(result.status, "cancelled")
        self.assertEqual(
            persisted["transition_receipts"]["transition-001"]["status"], "completed"
        )
        self.assertEqual(
            persisted["effective_capabilities"]["capability-proposal-review-001"]["status"],
            "consumed",
        )
        self.assertIn(
            "proposal-review-log",
            persisted["transition_receipts"]["transition-001"]["canonical_sync"][
                "observed_identities"
            ],
        )

    def test_cancel_does_not_consume_nonexistent_stage_evidence(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)
        evidence = {
            "input_identities": copy.deepcopy(receipt["input_identities"]),
            "expected_postcondition": copy.deepcopy(receipt["expected_postcondition"]),
            "outputs": [artifact_evidence()],
            "canonical_sync": synchronized_evidence(),
        }

        result = store.cancel(
            cancelled_by="user",
            cancelled_at="2026-07-22T00:00:00Z",
            completion_evidence=evidence,
            expected_document_identity=store.read().document_identity,
        )

        persisted = store.read().automation
        self.assertEqual(result.status, "reconciliation-required")
        self.assertEqual(
            persisted["transition_receipts"]["transition-001"]["status"],
            "prepared",
        )
        self.assertEqual(
            persisted["effective_capabilities"]["capability-proposal-review-001"]["status"],
            "active",
        )

    def test_atomic_writer_preserves_unrelated_metadata_and_detects_drift(self) -> None:
        state = valid_automation()
        store, path = self.make_store(state)
        os.chmod(path, 0o640)
        snapshot = store.read()
        replacement = copy.deepcopy(state)
        replacement["run"]["stop_reason"] = "authorization-required"
        store.replace_automation(
            replacement, expected_document_identity=snapshot.document_identity
        )
        self.assertEqual(store.read().document["unrelated"], {"owner": "keep-me", "count": 7})
        self.assertEqual(path.stat().st_mode & 0o777, 0o640)

        stale_identity = snapshot.document_identity
        with self.assertRaises(ConcurrentStateChange):
            store.replace_automation(replacement, expected_document_identity=stale_identity)
        self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"))

    def test_interrupted_atomic_write_does_not_truncate_canonical_file(self) -> None:
        state = valid_automation()
        store, path = self.make_store(state)
        before = path.read_bytes()

        def interrupt(_temporary_path: Path) -> None:
            raise RuntimeError("simulated interruption")

        with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
            store.replace_automation(
                state,
                expected_document_identity=store.read().document_identity,
                before_replace=interrupt,
            )
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(list(path.parent.glob(".change.yaml.*.tmp")), [])

    def test_yaml_round_trip_preserves_existing_change_metadata_values(self) -> None:
        source = (
            ROOT
            / "docs"
            / "changes"
            / "2026-07-20-single-bounded-review-fix-workflow-automation-mechanism"
            / "change.yaml"
        )
        source_document = WorkflowAutomationStateStore(source).read().document
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        target = Path(temp.name) / "change.yaml"
        target.write_text(dump_yaml(source_document), encoding="utf-8")
        self.assertEqual(WorkflowAutomationStateStore(target).read().document, source_document)

    def test_status_projection_is_read_only_and_complete(self) -> None:
        state = valid_automation()
        state["transition_receipts"] = {"transition-001": valid_receipt(state)}
        state["run"]["stop_reason"] = "authorization-required"
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
        self.assertEqual(projection["latest_review_result"]["clean_gate"], "not-satisfied")
        self.assertEqual(state, before)

    def test_legacy_status_projection_is_read_only(self) -> None:
        legacy = {
            "profile": "implementation-through-verify",
            "authorized_by": "user",
            "authorized_at": "2026-07-20T00:00:00Z",
            "change_id": "2026-07-20-example",
            "phase": "implementation",
            "state": "armed",
        }
        store, path = self.make_store(legacy=legacy)
        before = path.read_bytes()
        projection = store.status()
        self.assertEqual(projection["source"], "legacy-read-only")
        self.assertEqual(path.read_bytes(), before)

    def test_mixed_writable_legacy_and_unified_state_fails_closed(self) -> None:
        legacy = {
            "profile": "implementation-through-verify",
            "authorized_by": "user",
            "authorized_at": "2026-07-20T00:00:00Z",
            "change_id": "2026-07-20-example",
            "phase": "implementation",
            "state": "armed",
        }
        store, _ = self.make_store(valid_automation(), legacy=legacy)
        with self.assertRaisesRegex(StateContractError, "mixed writable"):
            store.read()

    def test_first_mutating_legacy_resume_writes_one_way_migration_receipt(self) -> None:
        legacy = {
            "profile": "implementation-through-verify",
            "authorized_by": "user",
            "authorized_at": "2026-07-20T00:00:00Z",
            "change_id": "2026-07-20-example",
            "phase": "implementation",
            "state": "armed",
        }
        store, _ = self.make_store(legacy=legacy)
        result = store.migrate_legacy(
            valid_automation(),
            migrated_at="2026-07-22T00:00:00Z",
            expected_document_identity=store.read().document_identity,
        )
        persisted = store.read().document
        self.assertEqual(result.status, "migrated")
        self.assertIn("autoprogression", persisted["workflow"])
        receipts = persisted["workflow"]["automation"]["migration_receipts"]
        self.assertEqual(len(receipts), 1)
        receipt = next(iter(receipts.values()))
        self.assertEqual(receipt["source_mechanism"], "implementation-through-verify")
        self.assertTrue(receipt["legacy_read_only"])

        second = store.migrate_legacy(
            valid_automation(), migrated_at="2026-07-22T00:01:00Z"
        )
        self.assertEqual(second.status, "already-migrated")
        self.assertFalse(second.mutated)

    def test_each_legacy_mechanism_migrates_from_its_exact_active_record(self) -> None:
        fixtures = {
            "authoring-through-plan-review": {
                "profile": "authoring-through-plan-review",
                "authorized_by": "user",
                "authorized_at": "2026-07-20T00:00:00Z",
                "change_id": "2026-07-20-example",
                "state": "armed",
            },
            "implementation-through-verify": {
                "implementation_through_verify": {
                    "profile": "implementation-through-verify",
                    "authorized_by": "user",
                    "authorized_at": "2026-07-20T00:00:00Z",
                    "change_id": "2026-07-20-example",
                    "phase": "B",
                    "state": "armed",
                }
            },
            "bounded-review-fix": {
                "review_fix": {
                    "profile": "bounded-review-fix",
                    "armed_by": "user",
                    "armed_at": "2026-07-20T00:00:00Z",
                    "change_id": "2026-07-20-example",
                    "target_stage": "spec-review",
                    "status": "armed",
                }
            },
        }
        for mechanism, legacy in fixtures.items():
            with self.subTest(mechanism=mechanism):
                store, _ = self.make_store(legacy=legacy)
                store.migrate_legacy(
                    valid_automation(),
                    migrated_at="2026-07-22T00:00:00Z",
                    expected_document_identity=store.read().document_identity,
                )
                receipt = next(
                    iter(store.read().automation["migration_receipts"].values())
                )
                self.assertEqual(receipt["source_mechanism"], mechanism)

    def test_terminal_legacy_records_remain_read_only(self) -> None:
        for mechanism in (
            "authoring-through-plan-review",
            "implementation-through-verify",
        ):
            with self.subTest(mechanism=mechanism):
                legacy = {
                    "profile": mechanism,
                    "authorized_by": "user",
                    "authorized_at": "2026-07-20T00:00:00Z",
                    "change_id": "2026-07-20-example",
                    "state": "completed",
                }
                store, path = self.make_store(legacy=legacy)
                before = path.read_bytes()
                self.assertEqual(store.status()["source"], "legacy-read-only")
                with self.assertRaisesRegex(StateContractError, "terminal legacy state"):
                    store.migrate_legacy(
                        valid_automation(), migrated_at="2026-07-22T00:00:00Z"
                    )
                self.assertEqual(path.read_bytes(), before)

        bounded = {
            "review_fix": {
                "profile": "bounded-review-fix",
                "status": "completed",
                "change_id": "2026-07-20-example",
            }
        }
        store, path = self.make_store(legacy=bounded)
        before = path.read_bytes()
        self.assertEqual(store.status()["source"], "legacy-read-only")
        with self.assertRaisesRegex(StateContractError, "exactly one active source"):
            store.migrate_legacy(valid_automation(), migrated_at="2026-07-22T00:00:00Z")
        self.assertEqual(path.read_bytes(), before)

    def test_fixed_inputs_produce_identical_migration_evidence(self) -> None:
        legacy = {
            "profile": "implementation-through-verify",
            "authorized_by": "user",
            "authorized_at": "2026-07-20T00:00:00Z",
            "change_id": "2026-07-20-example",
            "phase": "implementation",
            "state": "armed",
        }
        normalized = []
        for _ in range(2):
            store, _ = self.make_store(legacy=copy.deepcopy(legacy))
            store.migrate_legacy(
                valid_automation(),
                migrated_at="2026-07-22T00:00:00Z",
                expected_document_identity=store.read().document_identity,
            )
            normalized.append(copy.deepcopy(store.read().automation["migration_receipts"]))
        self.assertEqual(normalized[0], normalized[1])

    def test_m2_scenarios_are_deterministic_across_repetition_and_order(self) -> None:
        def run(order: tuple[str, ...]) -> dict[str, dict]:
            results: dict[str, dict] = {}
            roots: list[Path] = []
            for scenario in order:
                with tempfile.TemporaryDirectory() as name:
                    root = Path(name)
                    roots.append(root)
                    if scenario == "transition":
                        state = valid_automation()
                        store, path = self._make_store_at(root, state)
                        receipt = valid_receipt(state)
                        store.prepare_transition(
                            receipt,
                            expected_document_identity=store.read().document_identity,
                        )
                        evidence = self.materialize_valid_review_completion(store)
                        prepared = store.read()
                        receipt = prepared.automation["transition_receipts"][
                            "transition-001"
                        ]
                        recovery = evaluate_receipt_recovery(
                            prepared.automation,
                            receipt["transition_id"],
                            completion_evidence=evidence,
                            repository_root=store.repository_root,
                        )
                        store.finalize_transition(
                            receipt["transition_id"],
                            status="completed",
                            outputs=evidence["outputs"],
                            canonical_sync_status="synchronized",
                            canonical_sync_evidence=evidence["canonical_sync"]["evidence"],
                            canonical_sync_observed_identities=evidence["canonical_sync"][
                                "observed_identities"
                            ],
                            expected_document_identity=prepared.document_identity,
                        )
                        persisted = store.read().automation
                        results[scenario] = {
                            "receipt": copy.deepcopy(
                                persisted["transition_receipts"]["transition-001"]
                            ),
                            "transition_key": receipt["transition_key"],
                            "recovery": {
                                "action": recovery.action,
                                "invoke_stage": recovery.invoke_stage,
                                "reason": recovery.reason,
                            },
                            "canonical_file": path.read_bytes(),
                            "temporary_files": sorted(
                                item.name for item in root.glob(".change.yaml.*.tmp")
                            ),
                        }
                    else:
                        legacy = {
                            "profile": "implementation-through-verify",
                            "authorized_by": "user",
                            "authorized_at": "2026-07-20T00:00:00Z",
                            "change_id": "2026-07-20-example",
                            "phase": "implementation",
                            "state": "armed",
                        }
                        store, path = self._make_store_at(root, legacy=legacy)
                        store.migrate_legacy(
                            valid_automation(),
                            migrated_at="2026-07-22T00:00:00Z",
                            expected_document_identity=store.read().document_identity,
                        )
                        persisted = store.read().automation
                        results[scenario] = {
                            "migration": copy.deepcopy(persisted["migration_receipts"]),
                            "canonical_file": path.read_bytes(),
                            "temporary_files": sorted(
                                item.name for item in root.glob(".change.yaml.*.tmp")
                            ),
                        }
                self.assertFalse(root.exists())
            return results

        normal = run(("transition", "migration"))
        repeated = run(("transition", "migration"))
        reversed_order = run(("migration", "transition"))
        self.assertEqual(normal, repeated)
        self.assertEqual(normal, reversed_order)

    @staticmethod
    def _make_store_at(
        root: Path,
        automation: dict | None = None,
        *,
        legacy: dict | None = None,
    ) -> tuple[WorkflowAutomationStateStore, Path]:
        path = root / "change.yaml"
        document = {
            "change_id": "2026-07-20-example",
            "title": "State adapter fixture",
            "classification": "default",
            "risk": "medium",
            "review": {"status": "resolved", "unresolved_items": 0},
            "workflow": {},
            "unrelated": {"owner": "keep-me", "count": 7},
        }
        if automation is not None:
            document["workflow"]["automation"] = automation
        if legacy is not None:
            document["workflow"]["autoprogression"] = legacy
        path.write_text(dump_yaml(document), encoding="utf-8")
        return WorkflowAutomationStateStore(path), path


if __name__ == "__main__":
    unittest.main()
