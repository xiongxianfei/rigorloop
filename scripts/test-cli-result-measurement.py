#!/usr/bin/env python3
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cli_measurement", ROOT / "scripts/measure-cli-result-bytes.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MeasurementTests(unittest.TestCase):
    def test_repository_profile_passes_without_changing_default(self):
        report = MODULE.measure(
            ROOT / "packages/rigorloop/test/fixtures/observability/token-profiles-v1.json",
            ROOT / "docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json",
        )
        self.assertGreaterEqual(report["median_reduction_percent"], 30)
        self.assertTrue(all(report["gates"].values()))
        self.assertFalse(report["default_changed"])

    def test_changed_profile_vocabulary_fails_closed(self):
        baseline = ROOT / "docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json"
        data = json.loads((ROOT / "packages/rigorloop/test/fixtures/observability/token-profiles-v1.json").read_text())
        data["profiles"].pop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.json"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "exactly the six"):
                MODULE.measure(path, baseline)


if __name__ == "__main__":
    unittest.main()
