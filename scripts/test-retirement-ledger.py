#!/usr/bin/env python3
"""Regression tests for the repository-simplification retirement ledger."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from retirement_ledger import load_ledger, validate_ledger  # noqa: E402
from validation_selection import CHECK_CATALOG  # noqa: E402


LEDGER = (
    ROOT
    / "docs"
    / "changes"
    / "2026-08-10-published-skill-first-repository-simplification"
    / "retirement-ledger.yaml"
)


class RetirementLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = load_ledger(LEDGER)

    def assert_invalid(self, ledger: dict, fragment: str) -> None:
        errors = validate_ledger(ledger, expected_check_ids=set(CHECK_CATALOG))
        self.assertTrue(errors, "malformed ledger unexpectedly passed")
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in: {errors}",
        )

    def make_removable(self, candidate: dict) -> dict:
        entry = candidate["entries"][0]
        entry["state"] = "removable"
        entry["transition_evidence"] = {
            "status": "complete",
            "prior_states": ["inventoried", "dual-proof"],
            "old_proof": {"command": "old-check", "result": "pass"},
            "replacement_proof": {"command": "new-check", "result": "pass"},
            "comparison_result": "match",
            "removal_decision": "approved",
            "evidence_paths": ["evidence/m6-ci-retirement.md"],
            "rollback_point": "parent-commit",
        }
        return entry

    def test_repository_ledger_is_complete(self) -> None:
        self.assertEqual(
            validate_ledger(self.ledger, expected_check_ids=set(CHECK_CATALOG)), []
        )

    def test_every_selector_check_id_has_exactly_one_owner(self) -> None:
        owned = [
            check_id
            for entry in self.ledger["entries"]
            for check_id in entry["check_ids"]
        ]
        self.assertEqual(set(owned), set(CHECK_CATALOG))
        self.assertEqual(len(owned), len(set(owned)))

    def test_every_top_level_proof_script_is_inventoried(self) -> None:
        discovered = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "scripts").iterdir()
            if path.is_file()
            and (
                path.name.startswith(("test-", "validate-", "build-"))
                or path.name in {"ci.sh", "release-verify.sh"}
            )
        }
        owned = {
            script
            for entry in self.ledger["entries"]
            for script in entry["scripts"]
        }
        self.assertEqual(discovered - owned, set())

    def test_missing_protected_failure_fails_closed(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        del candidate["entries"][0]["protected_failure"]
        self.assert_invalid(candidate, "protected_failure")

    def test_unknown_state_fails_closed(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        candidate["entries"][0]["state"] = "probably-retired"
        self.assert_invalid(candidate, "unknown state")

    def test_unknown_contract_disposition_fails_closed(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        candidate["entries"][0]["contract_disposition"] = "maybe"
        self.assert_invalid(candidate, "unknown contract_disposition")

    def test_r26_unknown_value_fails_closed(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        candidate["r26_disposition"]["R35"] = "still-required"
        self.assert_invalid(candidate, "unknown R26 disposition")

    def test_duplicate_check_owner_fails_closed(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        candidate["entries"][1]["check_ids"].append(
            candidate["entries"][0]["check_ids"][0]
        )
        self.assert_invalid(candidate, "owned more than once")

    def test_unknown_fixture_behavior_pauses_removal(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        candidate["entries"][0]["state"] = "removable"
        candidate["entries"][0]["fixture_inventory"] = ["unknown"]
        self.assert_invalid(candidate, "unknown fixture behavior")

    def test_removal_requires_dual_proof_and_rollback(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        entry = self.make_removable(candidate)
        del entry["transition_evidence"]["replacement_proof"]
        del entry["transition_evidence"]["rollback_point"]
        self.assert_invalid(candidate, "transition_evidence.replacement_proof")
        self.assert_invalid(candidate, "transition_evidence.rollback_point")

    def test_pending_evidence_cannot_authorize_removal(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        candidate["entries"][0]["state"] = "removable"
        self.assert_invalid(candidate, "transition_evidence.status")

    def test_removal_requires_prior_dual_proof_state(self) -> None:
        candidate = copy.deepcopy(self.ledger)
        entry = self.make_removable(candidate)
        entry["transition_evidence"]["prior_states"] = ["inventoried"]
        self.assert_invalid(candidate, "prior_states")

    def test_r26_disposition_is_exact(self) -> None:
        expected = {
            "R35", "R35a", "R35b", "R35e", "R35f", "R35g",
            "R36i", "R36j", "R43d", "R44a", "R44e", "R45",
            "R45a", "R45b", "R45c", "R45d", "R52", "R52a",
            "R52b", "R55a:installed-target-tree", "R59b",
        }
        self.assertEqual(set(self.ledger["r26_disposition"]), expected)
        self.assertEqual(self.ledger["retained_clauses"], ["R35c", "R35d"])
        self.assertIn("R50a", self.ledger["retained_deterministic_parity"])
        self.assertIn("R50b", self.ledger["retained_deterministic_parity"])

    def test_admission_budget_forbids_new_subsystems(self) -> None:
        self.assertEqual(
            self.ledger["admission_budget"],
            {
                "standalone_validator_clis": 0,
                "selector_systems": 0,
                "validation_caches": 0,
                "validation_schedulers": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
