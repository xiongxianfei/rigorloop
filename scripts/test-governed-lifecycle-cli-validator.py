#!/usr/bin/env python3
"""Regression tests for the governed lifecycle CI wrapper."""

from __future__ import annotations

import importlib.util
import io
import json
import unittest
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

if __name__ == "__main__":
    unittest.main(verbosity=2)
