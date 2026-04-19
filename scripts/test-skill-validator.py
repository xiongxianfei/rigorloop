#!/usr/bin/env python3
"""Fixture-driven tests for the first-release skill validator."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-skills.py"
FIXTURES = ROOT / "tests" / "fixtures" / "skills"


def run_validator(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(target)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


class SkillValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def assertFixturePasses(self, relative_path: str) -> None:
        result = run_validator(FIXTURES / relative_path)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected fixture '{relative_path}' to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def assertFixtureFails(self, relative_path: str, expected_text: str) -> None:
        result = run_validator(FIXTURES / relative_path)
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"expected fixture '{relative_path}' to fail",
        )
        self.assertIn(expected_text, combined_output)

    def test_valid_skill_passes(self) -> None:
        self.assertFixturePasses("valid-basic")

    def test_missing_name_fails(self) -> None:
        self.assertFixtureFails("missing-name", "name: missing required field")

    def test_missing_description_fails(self) -> None:
        self.assertFixtureFails("missing-description", "description: missing required field")

    def test_missing_title_fails(self) -> None:
        self.assertFixtureFails("missing-title", "expected exactly one top-level # title")

    def test_missing_expected_output_fails(self) -> None:
        self.assertFixtureFails(
            "missing-expected-output", "missing required '## Expected output' section"
        )

    def test_duplicate_name_fails(self) -> None:
        self.assertFixtureFails("duplicate-name", "duplicate skill name: duplicate-name")

    def test_placeholder_text_fails(self) -> None:
        self.assertFixtureFails("placeholder-text", "placeholder text is not allowed")

    def test_generated_output_path_is_rejected(self) -> None:
        result = run_validator(ROOT / ".codex" / "skills")
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generated output path must not be used as authored source of truth", combined_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
