#!/usr/bin/env python3
"""Regression tests for the governed lifecycle CI wrapper."""

from __future__ import annotations

import importlib.util
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
