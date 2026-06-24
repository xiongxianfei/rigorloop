#!/usr/bin/env python3
"""Regression tests for documentation prose source-line validation."""

from __future__ import annotations

import hashlib
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-documentation-prose.py"
FIXTURES = ROOT / "tests" / "fixtures" / "documentation-prose"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_documentation_prose", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load documentation prose validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DocumentationProseValidatorTests(unittest.TestCase):
    maxDiff = None

    def validate(self, *paths: Path, mode: str = "enforce"):
        validator = load_validator()
        return validator.validate_paths(paths, mode=mode)

    def test_semantic_lines_and_structural_markdown_pass(self) -> None:
        result = self.validate(
            FIXTURES / "pass" / "semantic-lines.md",
            FIXTURES / "pass" / "structural-exclusions.md",
        )

        self.assertEqual([], result.errors)
        self.assertEqual([], result.warnings)

    def test_explicit_hard_break_two_space_passes_enforce(self) -> None:
        result = self.validate(FIXTURES / "pass" / "explicit-hard-break.md")

        self.assertEqual([], result.errors)
        self.assertEqual([], result.warnings)

    def test_explicit_hard_break_backslash_passes_enforce(self) -> None:
        result = self.validate(FIXTURES / "pass" / "explicit-hard-break-backslash.md")

        self.assertEqual([], result.errors)
        self.assertEqual([], result.warnings)

    def test_mechanical_wrap_without_hard_break_still_fails_enforce(self) -> None:
        result = self.validate(FIXTURES / "fail" / "no-hard-break-mechanical-wrap.md")

        self.assertTrue(result.errors)
        self.assertTrue(any("mechanical mid-sentence wrap" in finding.reason for finding in result.errors))

    def test_mechanically_continued_list_item_fails_enforce(self) -> None:
        result = self.validate(FIXTURES / "fail" / "list-item-mechanical-continuation.md")

        self.assertTrue(result.errors)
        self.assertTrue(any("mechanically continued list item" in finding.reason for finding in result.errors))

    def test_nested_list_structure_passes_enforce(self) -> None:
        result = self.validate(
            FIXTURES / "pass" / "list-item-nested-structure.md",
            FIXTURES / "pass" / "list-item-single-line.md",
            FIXTURES / "pass" / "list-item-with-fenced-code.md",
        )

        self.assertEqual([], result.errors)
        self.assertEqual([], result.warnings)

    def test_mechanical_mid_sentence_wrap_fails(self) -> None:
        result = self.validate(FIXTURES / "fail" / "mechanical-wrap.md")

        self.assertTrue(result.errors)
        self.assertTrue(any("mechanical mid-sentence wrap" in finding.reason for finding in result.errors))
        finding = result.errors[0]
        self.assertEqual("error", finding.severity)
        self.assertIn("join lines", finding.suggested_actions)
        self.assertGreaterEqual(finding.line_end, finding.line_start)

    def test_named_regressions_fail(self) -> None:
        result = self.validate(FIXTURES / "fail" / "named-regressions.md")
        reasons = "\n".join(finding.reason for finding in result.errors)

        self.assertIn("AI agents", reasons)
        self.assertIn("proposal to spec", reasons)
        self.assertIn("reviewable in Git", reasons)

    def test_command_and_lifecycle_splits_fail(self) -> None:
        result = self.validate(FIXTURES / "fail" / "command-and-lifecycle.md")
        reasons = "\n".join(finding.reason for finding in result.errors)

        self.assertIn("command split", reasons)
        self.assertIn("lifecycle chain split", reasons)

    def test_ambiguous_clause_break_warns_without_failure(self) -> None:
        result = self.validate(FIXTURES / "warn" / "ambiguous-clause.md")

        self.assertEqual([], result.errors)
        self.assertTrue(result.warnings)
        self.assertTrue(any("ambiguous" in finding.reason for finding in result.warnings))

    def test_audit_mode_does_not_fail_for_warning_fixtures(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--mode",
                "audit",
                "--path",
                str(FIXTURES / "warn" / "ambiguous-clause.md"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("warnings=1", result.stdout)

    def test_enforce_mode_returns_nonzero_for_errors(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--mode",
                "enforce",
                "--path",
                str(FIXTURES / "fail" / "mechanical-wrap.md"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("mechanical mid-sentence wrap", result.stdout)

    def test_validator_does_not_mutate_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="documentation-prose-") as temp_name:
            temp_root = Path(temp_name)
            target = temp_root / "mechanical-wrap.md"
            shutil.copy2(FIXTURES / "fail" / "mechanical-wrap.md", target)
            before = digest(target)

            result = self.validate(target, mode="audit")

            self.assertTrue(result.errors)
            self.assertEqual(before, digest(target))


if __name__ == "__main__":
    unittest.main(verbosity=2)
