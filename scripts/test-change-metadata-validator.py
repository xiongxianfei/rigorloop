#!/usr/bin/env python3
"""Fixture-driven tests for change metadata validation."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-change-metadata.py"
FIXTURES = ROOT / "tests" / "fixtures" / "change-metadata"
SKILL_VALIDATOR_EXAMPLE = ROOT / "docs" / "changes" / "0001-skill-validator" / "change.yaml"


def run_validator(*targets: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *(str(target) for target in targets)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


class ChangeMetadataValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def assertPathPasses(self, target: Path) -> None:
        result = run_validator(target)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected '{target}' to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def assertPathFails(self, target: Path, expected_text: str) -> None:
        result = run_validator(target)
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"expected '{target}' to fail",
        )
        self.assertIn(expected_text, combined_output)

    def test_valid_basic_fixture_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "valid-basic" / "change.yaml")

    def test_shipped_0001_example_passes(self) -> None:
        self.assertPathPasses(SKILL_VALIDATOR_EXAMPLE)

    def test_noncanonical_artifact_key_fails(self) -> None:
        self.assertPathFails(
            FIXTURES / "bad-artifact-key" / "change.yaml",
            "artifacts.explain-change: invalid artifact key",
        )

    def test_nested_artifact_value_shape_fails(self) -> None:
        self.assertPathFails(
            FIXTURES / "bad-artifact-value-shape" / "change.yaml",
            "artifacts.explain_change: expected string",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
