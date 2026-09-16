"""Structural command results and semantic-review handoff."""

from __future__ import annotations

import sys
from pathlib import Path
import json
import io
import contextlib
import runpy
import tempfile
import unittest
from unittest import mock

from boundary_fixture_helpers import (
    ROOT,
    relevant_tree_snapshot,
    valid_feature,
    valid_proof,
)

sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.boundary_first_validation import validate_changed_spec


class AdoptionReviewHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "specs").mkdir()
        for name in ("historical", "other"):
            (self.root / f"specs/{name}.md").write_text("# Historical\n")
        self.main = runpy.run_path(str(ROOT / "scripts/validate-boundary-first.py"))["main"]

    def run_check(self, *paths: str) -> tuple[int, dict]:
        args = ["validate-boundary-first", "--check", "--root", str(self.root)]
        for path in paths:
            args.extend(["--path", path])
        output = io.StringIO()
        with mock.patch.object(sys, "argv", args), contextlib.redirect_stdout(output):
            result = self.main()
        return result, json.loads(output.getvalue())

    def test_review_required_is_structural_success_not_approval(self) -> None:
        before = relevant_tree_snapshot(self.root)
        code, output = self.run_check("specs/historical.md", "specs/other.md")
        self.assertEqual(code, 0)
        self.assertEqual(output["status"], "review-required")
        self.assertEqual(output["validation"], "structure-and-references-only")
        self.assertEqual({item["path"] for item in output["review_required"]},
                         {"specs/historical.md", "specs/other.md"})
        self.assertTrue(all(item["owner"] == "design-review" for item in output["review_required"]))
        self.assertEqual(relevant_tree_snapshot(self.root), before)

    def test_review_required_does_not_hide_mixed_structural_failure(self) -> None:
        code, output = self.run_check("specs/historical.md", "docs/design/missing.md")
        self.assertEqual(code, 1)
        self.assertEqual(output["status"], "failed")
        self.assertEqual(output["review_required"][0]["path"], "specs/historical.md")
        self.assertTrue(output["issues"])

    def test_unknown_value_marker_fails_for_explicit_features(self) -> None:
        for path in ("specs/new.md", "specs/historical.md"):
            with self.subTest(path=path):
                (self.root / path).write_text(valid_feature().replace("boundary_contract: boundary-first-v1", "boundary_contract: unknown_value"))
                code, output = self.run_check(path)
                self.assertEqual(code, 1)
                self.assertEqual(output["status"], "failed")
                self.assertTrue(output["issues"])
                self.assertFalse(output.get("review_required"))

    def test_malformed_boundary_content_is_not_review_only(self) -> None:
        for text in (valid_feature().replace("## Boundary definitions", "## Missing"),
                     "# Historical\n\n## Boundary model\n", "# Historical\nboundary_contract:\n"):
            with self.subTest(text=text):
                (self.root / "specs/historical.md").write_text(text)
                code, output = self.run_check("specs/historical.md")
                self.assertEqual(code, 1)
                self.assertFalse(output.get("review_required"))

    def test_unmarked_new_spec_requires_adoption_review(self) -> None:
        (self.root / "specs/new.md").write_text("# New\n")
        code, output = self.run_check("specs/new.md")
        self.assertEqual(code, 0)
        self.assertEqual(output["review_required"][0]["check_id"], "BFR-ADOPTION-REVIEW")


    def test_explicit_unmarked_proof_requires_review_and_partial_record_fails(self):
        path = "specs/historical.test.md"
        (self.root / path).write_text("# Customer proof\n")
        code, output = self.run_check(path)
        self.assertEqual(code, 0)
        self.assertEqual(output["status"], "review-required")
        self.assertEqual(output["review_required"][0]["path"], "specs/historical.md")
        for text in ("boundary_contract: unknown_value\n", "Boundary model version: unknown_value\n", "## Proof map\n", valid_proof()):
            with self.subTest(text=text[:40]):
                (self.root / path).write_text(text)
                code, output = self.run_check(path)
                self.assertEqual(code, 1, output)
                self.assertTrue(output["issues"])
                self.assertEqual(output["review_required"][0]["path"], "specs/historical.md")

    def test_unknown_value_diagnostic_is_not_demoted_to_review(self) -> None:
        issue = validate_changed_spec(self.root, "docs/design/missing.md")[0]
        unknown = type(issue)("unknown_value", issue.path, issue.message, issue.offending_value, issue.expected)
        with mock.patch.dict(self.main.__globals__, {"validate_changed_spec": lambda root, path: (unknown,)}):
            code, output = self.run_check("specs/historical.md")
        self.assertEqual(code, 1)
        self.assertEqual(output["issues"][0]["check_id"], "unknown_value")
        self.assertFalse(output["review_required"])
