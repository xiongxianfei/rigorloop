#!/usr/bin/env python3
"""Fixture-driven tests for change metadata validation."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-change-metadata.py"
FIXTURES = ROOT / "tests" / "fixtures" / "change-metadata"
SKILL_VALIDATOR_EXAMPLE = ROOT / "docs" / "changes" / "0001-skill-validator" / "change.yaml"
CLEAN_RECEIPT_ROOT = (
    ROOT
    / "tests"
    / "fixtures"
    / "review-artifacts"
    / "valid-clean-receipt-root"
    / "change.yaml"
)


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_change_metadata", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load validate-change-metadata.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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

    def test_compact_valid_fixture_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "compact-valid" / "change.yaml")

    def test_compact_path_variable_helpers(self) -> None:
        validator = load_validator_module()
        self.assertEqual(
            validator.derive_compact_slug("2026-05-21-compact-change-validation-metadata"),
            "compact-change-validation-metadata",
        )
        self.assertEqual(
            validator.resolve_compact_path_template(
                "docs/changes/{change_id}/notes/{{draft}}.md",
                {
                    "change_id": "2026-05-21-compact-change-validation-metadata",
                    "slug": "compact-change-validation-metadata",
                },
            ),
            "docs/changes/2026-05-21-compact-change-validation-metadata/notes/{draft}.md",
        )
        with self.assertRaisesRegex(validator.MetadataValidationError, r"unmatched"):
            validator.resolve_compact_path_template("docs/{change_id", {"change_id": "x"})
        with self.assertRaisesRegex(validator.MetadataValidationError, r"unsupported interpolation"):
            validator.resolve_compact_path_template("docs/${change_id}", {"change_id": "x"})
        with self.assertRaisesRegex(validator.MetadataValidationError, r"unknown variable"):
            validator.resolve_compact_path_template("docs/{missing}", {"change_id": "x"})

    def test_compact_path_safety_helper_rejects_unsafe_values(self) -> None:
        validator = load_validator_module()
        unsafe_values = [
            "/tmp/change.yaml",
            "~/change.yaml",
            "../change.yaml",
            "example.com/change.yaml",
            "https://example.com/change.yaml",
            "https://user:pass@example.com/change.yaml",
            "docs/changes/token=value/change.yaml",
            "home/alice/change.yaml",
        ]
        for value in unsafe_values:
            with self.subTest(value=value):
                self.assertTrue(
                    validator.validate_repo_relative_path(value, "path_vars.example"),
                    msg=f"expected {value!r} to be unsafe",
                )

    def test_compact_invalid_fixtures_fail(self) -> None:
        cases = [
            (
                "compact-invalid-missing-section",
                "validation_events: missing required compact field",
            ),
            (
                "compact-invalid-mixed-shape",
                "mixed legacy and compact validation metadata",
            ),
            (
                "compact-invalid-undefined-bundle",
                "validation_events[0].bundles[0]: unknown validation bundle 'metadata'",
            ),
            (
                "compact-invalid-result-enum",
                "validation_events[0].result: expected one of",
            ),
            (
                "compact-invalid-noninteger-count",
                "validation_events[0].counts.reviews: expected integer",
            ),
            (
                "compact-invalid-fail-without-details",
                "validation_events[0].failures: required when result is fail",
            ),
            (
                "compact-invalid-blocked-without-details",
                "validation_events[0].failures: required when result is blocked",
            ),
            (
                "compact-invalid-conflicting-slug",
                "path_vars.slug: must match derived slug",
            ),
            (
                "compact-invalid-recursive-var",
                "path_vars.change_root: recursive variable reference",
            ),
            (
                "compact-invalid-unresolved-var",
                "path_vars.change_root: unknown variable 'missing'",
            ),
            (
                "compact-invalid-brace-syntax",
                "path_vars.change_root: unsupported interpolation syntax '${'",
            ),
            (
                "compact-invalid-unsafe-path",
                "path_vars.change_root: unsafe absolute path",
            ),
            (
                "compact-invalid-dated-spec-path",
                "path_vars.spec: expected canonical spec path 'specs/compact-change-validation-metadata.md'",
            ),
            (
                "compact-invalid-dated-test-spec-path",
                "path_vars.test_spec: expected canonical test spec path 'specs/compact-change-validation-metadata.test.md'",
            ),
            (
                "compact-invalid-lifecycle-stage",
                "validation_events[0].lifecycle_stage: expected one of",
            ),
            (
                "compact-invalid-missing-first-exists",
                "path_vars.spec: required artifact does not exist",
            ),
            (
                "compact-invalid-path-opt-out",
                "validation_events[0].not_yet_created: per-path existence opt-out flags are not allowed",
            ),
            (
                "compact-invalid-transcript-missing",
                "validation_events[0].evidence.transcript: referenced transcript file does not exist",
            ),
            (
                "compact-invalid-unknown-path-var",
                "path_vars.mystery: unknown compact path variable",
            ),
        ]
        for fixture, expected in cases:
            with self.subTest(fixture=fixture):
                self.assertPathFails(FIXTURES / fixture / "change.yaml", expected)

    def test_compact_pre_stage_missing_artifact_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "compact-valid-pre-stage-missing-artifact" / "change.yaml")

    def test_clean_receipt_root_metadata_passes(self) -> None:
        self.assertPathPasses(CLEAN_RECEIPT_ROOT)

    def test_shipped_0001_example_passes(self) -> None:
        self.assertPathPasses(SKILL_VALIDATOR_EXAMPLE)

    def test_inline_empty_collections_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-inline-empty-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                """change_id: "inline-empty"
title: "Inline empty collections"
classification: "test"
risk: "low"
artifacts: {}
requirements: []
tests: []
validation: []
changed_files: []
review:
  status: "pending"
  unresolved_items: 0
""",
                encoding="utf-8",
            )
            self.assertPathPasses(target)

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
