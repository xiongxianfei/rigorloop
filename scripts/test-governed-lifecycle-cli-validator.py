#!/usr/bin/env python3
"""Regression tests for the governed lifecycle CI wrapper."""

from __future__ import annotations

import importlib.util
import io
import json
import unittest
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-governed-lifecycle-cli.py")
SPEC = importlib.util.spec_from_file_location("governed_lifecycle_validator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BaselineWarningTests(unittest.TestCase):
    def payload(self):
        expected = MODULE.BASELINE_WARNINGS["2026-08-05-activate-boundary-first-v1-v0-3-7"]
        return {
            "status": "blocked",
            "errors": [],
            "blockers": [{"code": code} for code in expected["blocker_codes"]],
            "effective_state": {"unresolved_findings": list(expected["finding_ids"])},
        }

    def test_exact_approved_baseline_matches(self):
        self.assertTrue(MODULE.baseline_matches("2026-08-05-activate-boundary-first-v1-v0-3-7", self.payload()))

    def test_new_error_does_not_match_baseline(self):
        payload = self.payload()
        payload["errors"] = [{"code": "RL_UNSUPPORTED_SCHEMA"}]
        self.assertFalse(MODULE.baseline_matches("2026-08-05-activate-boundary-first-v1-v0-3-7", payload))

    def test_changed_finding_set_does_not_match_baseline(self):
        payload = self.payload()
        payload["effective_state"]["unresolved_findings"].append("NEW-FINDING")
        self.assertFalse(MODULE.baseline_matches("2026-08-05-activate-boundary-first-v1-v0-3-7", payload))


class WrapperExecutionTests(unittest.TestCase):
    class Result:
        def __init__(self, returncode, payload):
            self.returncode = returncode
            self.stdout = json.dumps(payload)
            self.stderr = "child-private-stderr"

    def test_t13_child_result_matrix_preserves_exit_classification_and_codes(self):
        payloads = {
            "success": self.Result(0, {"schema_version": 1, "status": "success", "private_summary": "do-not-repeat"}),
            "blocked": self.Result(2, {"schema_version": 1, "status": "blocked", "errors": [{"code": "RL_OPERATION_NOT_PERMITTED"}]}),
            "usage": self.Result(4, {"schema_version": 1, "status": "error", "errors": [{"code": "RL_INVALID_REQUEST"}]}),
            "invalid-repository": self.Result(4, {"schema_version": 1, "status": "error", "errors": [{"code": "RL_UNSUPPORTED_SCHEMA"}]}),
            "stale": self.Result(5, {"schema_version": 1, "status": "blocked", "errors": [{"code": "RL_STALE_OPERATION"}]}),
            "internal": self.Result(3, {"schema_version": 1, "status": "error", "errors": [{"code": "RL_POST_VALIDATION_FAILED"}]}),
            "concise": self.Result(2, {"schema_version": 2, "projection": "concise", "status": "blocked", "codes": ["RL_OPERATION_NOT_PERMITTED"]}),
            "malformed": self.Result(3, {"schema_version": 2, "projection": "concise", "status": "error", "codes": "PRIVATE_INVALID_SHAPE"}),
        }

        def runner(command, **_kwargs):
            return payloads[command[command.index("--change") + 1]]

        report = MODULE.build_report([(name, Path(f"{name}/change.yaml")) for name in payloads], runner=runner)
        self.assertEqual(report["status"], "failed")
        by_id = {item["change_id"]: item for item in report["failures"]}
        self.assertEqual({name: item["exit_code"] for name, item in by_id.items()}, {
            "blocked": 2,
            "usage": 4,
            "invalid-repository": 4,
            "stale": 5,
            "internal": 3,
            "concise": 2,
            "malformed": 3,
        })
        self.assertEqual(by_id["concise"]["errors"], ["RL_OPERATION_NOT_PERMITTED"])
        self.assertEqual(by_id["malformed"]["errors"], ["invalid-structured-result"])
        self.assertNotIn("success", by_id)

    def test_t13_main_emits_one_aggregate_and_suppresses_successful_child_stdout(self):
        result = self.Result(0, {"schema_version": 1, "status": "success", "private_summary": "CHILD_SUCCESS_SENTINEL"})
        commands = []

        def runner(command, **_kwargs):
            commands.append(command)
            return result

        output = io.StringIO()
        exit_code = MODULE.main(records=[("success", Path("success/change.yaml"))], runner=runner, output=output)
        rendered = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertEqual(len(commands), 1)
        self.assertEqual(rendered.count('"schema_version"'), 1)
        self.assertNotIn("CHILD_SUCCESS_SENTINEL", rendered)
        self.assertEqual(json.loads(rendered)["status"], "passed")

    def test_cutover_rejects_nonterminal_retired_stage_but_ignores_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blocked = root / "blocked.yaml"
            blocked.write_text(
                "workflow_state:\n  lifecycle_state: active\n  current_stage: spec-review\n  next_stage: architecture\nreview:\n  latest_review: spec-review-r1\n",
                encoding="utf-8",
            )
            historical = root / "historical.yaml"
            historical.write_text(
                "workflow_state:\n  lifecycle_state: terminal\n  current_stage: pr\n  next_stage: none\nreview:\n  latest_review: spec-review-r1\n",
                encoding="utf-8",
            )
            self.assertEqual(MODULE.legacy_progression_dependency(blocked), ["spec-review"])
            self.assertEqual(MODULE.legacy_progression_dependency(historical), [])

    def test_unknown_stage_is_not_mistaken_for_legacy_compatibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unknown.yaml"
            path.write_text(
                "workflow_state:\n  lifecycle_state: active\n  current_stage: unknown-review\n  next_stage: unknown-review\n",
                encoding="utf-8",
            )
            self.assertEqual(MODULE.legacy_progression_dependency(path), [])

    def test_active_inventory_rejects_unfrozen_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "docs" / "changes" / "old").mkdir(parents=True)
            (root / "docs" / "changes" / "new").mkdir(parents=True)
            (root / "docs" / "changes" / "old" / "change.yaml").write_text("{}\n", encoding="utf-8")
            (root / "docs" / "changes" / "new" / "change.yaml").write_text("{}\n", encoding="utf-8")
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [{"change_id": "old", "contract_class": "legacy-unversioned"}],
            }
            (root / "specs" / "lifecycle-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(
                MODULE.activation_inventory_errors(root, loader=lambda path: {}),
                ["activation inventory mismatch: missing=['new'], extra=[], class_mismatch=[]"],
            )

    def test_final_verification_manifest_unknown_class_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [{"change_id": "old", "contract_class": "stage-owned-change-local-v1"}],
            }
            (root / "specs" / "final-verification-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertRegex(
                MODULE.final_verification_manifest_errors(root)[0],
                r"changes must be empty",
            )

    def test_active_final_verification_manifest_does_not_allowlist_v2(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "docs" / "changes" / "old-v2").mkdir(parents=True)
            (root / "docs" / "changes" / "old-v2" / "change.yaml").write_text(
                "lifecycle_contract: stage-owned-change-local-v2\n",
                encoding="utf-8",
            )
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [],
            }
            (root / "specs" / "final-verification-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(MODULE.final_verification_manifest_errors(root), [])

    def test_quoted_v2_remains_history_without_allowlist_membership(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "docs" / "changes" / "quoted-v2").mkdir(parents=True)
            (root / "docs" / "changes" / "quoted-v2" / "change.yaml").write_text(
                'change_id: quoted-v2\nlifecycle_contract: "stage-owned-change-local-v2"\n',
                encoding="utf-8",
            )
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [],
            }
            (root / "specs" / "final-verification-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(MODULE.final_verification_manifest_errors(root), [])

    def test_comments_do_not_select_a_lifecycle_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "docs" / "changes" / "comment-only").mkdir(parents=True)
            (root / "docs" / "changes" / "comment-only" / "change.yaml").write_text(
                "change_id: comment-only\n# lifecycle_contract: stage-owned-change-local-v2\n",
                encoding="utf-8",
            )
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [],
            }
            (root / "specs" / "final-verification-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(MODULE.final_verification_manifest_errors(root), [])
            self.assertEqual(MODULE.governed_records(root), [])

    def test_quoted_v3_is_discovered_as_governed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "changes" / "quoted-v3").mkdir(parents=True)
            path = root / "docs" / "changes" / "quoted-v3" / "change.yaml"
            path.write_text(
                "change_id: quoted-v3\nlifecycle_contract: 'stage-owned-change-local-v3'\n",
                encoding="utf-8",
            )
            self.assertEqual(MODULE.governed_records(root), [("quoted-v3", path)])

    def test_final_verification_manifest_ordering_fails_before_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [
                    {"change_id": "z-v2", "contract_class": "stage-owned-change-local-v2"},
                    {"change_id": "a-v2", "contract_class": "stage-owned-change-local-v2"},
                ],
            }
            (root / "specs" / "final-verification-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertRegex(
                MODULE.final_verification_manifest_errors(root)[0],
                r"changes must be empty",
            )

    def test_final_verification_manifest_duplicate_fails_before_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            entry = {"change_id": "same-v2", "contract_class": "stage-owned-change-local-v2"}
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [entry, dict(entry)],
            }
            (root / "specs" / "final-verification-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertRegex(
                MODULE.final_verification_manifest_errors(root)[0],
                r"changes must be empty",
            )

    def test_unknown_parsed_contract_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").mkdir()
            (root / "docs" / "changes" / "future").mkdir(parents=True)
            (root / "docs" / "changes" / "future" / "change.yaml").write_text(
                'change_id: future\nlifecycle_contract: "stage-owned-change-local-v9"\n',
                encoding="utf-8",
            )
            manifest = {
                "schema_version": 1,
                "state": "active",
                "activating_source_revision": "a" * 40,
                "changes": [],
            }
            (root / "specs" / "final-verification-contract-activation.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            _inventory, errors = MODULE.parsed_change_inventory(root)
            self.assertRegex(errors[0], r"lifecycle_contract: unknown_value stage-owned-change-local-v9")

if __name__ == "__main__":
    unittest.main(verbosity=2)
