#!/usr/bin/env python3
"""Fixture-driven tests for change metadata validation."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-change-metadata.py"
FIXTURES = ROOT / "tests" / "fixtures" / "change-metadata"
SKILL_VALIDATOR_EXAMPLE = ROOT / "docs" / "changes" / "0001-skill-validator" / "change.yaml"
CLEAN_RECEIPT_ROOT = ROOT / "tests" / "fixtures" / "review-artifacts" / "valid-clean-receipt-root" / "change.yaml"


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

    def test_clean_receipt_root_metadata_passes(self) -> None:
        self.assertPathPasses(CLEAN_RECEIPT_ROOT)

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

    def test_clean_receipt_review_metadata_shape_fails(self) -> None:
        fixture_text = CLEAN_RECEIPT_ROOT.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="change-metadata-clean-receipt-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                fixture_text.replace("reviewed_artifact: specs/example.md", "reviewed_artifact: 1"),
                encoding="utf-8",
            )
            self.assertPathFails(target, "review.reviewed_artifact: expected string")

        with tempfile.TemporaryDirectory(prefix="change-metadata-clean-receipt-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                fixture_text.replace("review_log: tests/fixtures/review-artifacts/valid-clean-receipt-root/review-log.md", "review_log: 1"),
                encoding="utf-8",
            )
            self.assertPathFails(target, "review.review_log: expected string")

    def test_clean_receipt_review_metadata_required_fields_fail(self) -> None:
        fixture_text = CLEAN_RECEIPT_ROOT.read_text(encoding="utf-8")
        cases = [
            (
                "  reviewed_artifact: specs/example.md\n",
                "",
                "review.reviewed_artifact is required for clean receipt roots",
            ),
            (
                "  review_log: tests/fixtures/review-artifacts/valid-clean-receipt-root/review-log.md\n",
                "",
                "review.review_log is required for clean receipt roots",
            ),
            (
                "  status: clean\n",
                "",
                "review.status: missing required field",
            ),
            (
                "  status: clean\n",
                "  status: approved\n",
                "review.status must be 'clean' for clean receipt roots",
            ),
            (
                "  status: clean\n",
                "  status: changes-requested\n",
                "review.status must be 'clean' for clean receipt roots",
            ),
            (
                "  unresolved_items: 0\n",
                "",
                "review.unresolved_items: missing required field",
            ),
            (
                "  unresolved_items: 0\n",
                "  unresolved_items: 1\n",
                "review.unresolved_items must be 0 for clean receipt roots",
            ),
            (
                "  unresolved_items: 0\n",
                "  unresolved_items: \"0\"\n",
                "review.unresolved_items: expected integer",
            ),
        ]
        for old, new, expected in cases:
            with self.subTest(expected=expected):
                with tempfile.TemporaryDirectory(prefix="change-metadata-clean-receipt-") as temp_dir:
                    target = Path(temp_dir) / "change.yaml"
                    target.write_text(fixture_text.replace(old, new), encoding="utf-8")
                    self.assertPathFails(target, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
