#!/usr/bin/env python3
"""Transaction, recovery, cancellation, and migration tests for automation state."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import os
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
                        outputs=["sha256:review-output"],
                        canonical_sync={"status": "synchronized"},
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
        receipt = persist_receipt(state)
        decision = evaluate_receipt_recovery(
            state,
            receipt["transition_id"],
            completion_evidence={
                "input_identities": copy.deepcopy(receipt["input_identities"]),
                "expected_postcondition": copy.deepcopy(receipt["expected_postcondition"]),
                "outputs": ["sha256:review-output"],
                "canonical_sync": {"status": "synchronized"},
            },
        )
        self.assertEqual(decision.action, "reconcile-completed")
        self.assertFalse(decision.invoke_stage)

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
            outputs=["sha256:original"],
            canonical_sync={"status": "synchronized"},
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

    def test_finalize_consumes_capability_only_with_completed_receipt(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        state["transition_receipts"] = {"transition-001": receipt}
        store, _ = self.make_store(state)

        store.finalize_transition(
            "transition-001",
            status="completed",
            outputs=["sha256:review-output"],
            canonical_sync_status="synchronized",
            expected_document_identity=store.read().document_identity,
        )

        persisted = store.read().automation
        self.assertEqual(persisted["transition_receipts"]["transition-001"]["status"], "completed")
        self.assertEqual(
            persisted["effective_capabilities"]["capability-proposal-review-001"]["status"],
            "consumed",
        )

    def test_cancel_revokes_authority_and_preserves_receipts(self) -> None:
        state = valid_automation()
        receipt = valid_receipt(state)
        receipt.update(
            status="completed",
            outputs=["sha256:review-output"],
            canonical_sync={"status": "synchronized"},
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
        evidence = {
            "input_identities": copy.deepcopy(receipt["input_identities"]),
            "expected_postcondition": copy.deepcopy(receipt["expected_postcondition"]),
            "outputs": ["sha256:review-output"],
            "canonical_sync": {"status": "synchronized"},
        }
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
                        evidence = {
                            "input_identities": copy.deepcopy(
                                receipt["input_identities"]
                            ),
                            "expected_postcondition": copy.deepcopy(
                                receipt["expected_postcondition"]
                            ),
                            "outputs": ["sha256:review-output"],
                            "canonical_sync": {"status": "synchronized"},
                        }
                        prepared = store.read()
                        recovery = evaluate_receipt_recovery(
                            prepared.automation,
                            receipt["transition_id"],
                            completion_evidence=evidence,
                        )
                        store.finalize_transition(
                            receipt["transition_id"],
                            status="completed",
                            outputs=evidence["outputs"],
                            canonical_sync_status="synchronized",
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
