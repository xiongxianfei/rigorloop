"""Current model document grammar and path authority."""

from __future__ import annotations

import sys
from pathlib import Path
import json
import re
import subprocess
import tempfile
import unittest

from boundary_fixture_helpers import (
    EXPECTED_MODEL_PATHS,
    ROOT,
    relevant_tree_snapshot,
)

sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.boundary_first_validation import validate_changed_spec, validate_model_record


class ModelRecordTests(unittest.TestCase):
    """TG-06: model recognition is structural, explicit and independent of lifecycle."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rigorloop-model-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "docs/design/skill/workflow.md"
        self.path.parent.mkdir(parents=True)
        self.text = (ROOT / "docs/design/skill/workflow.md").read_text(encoding="utf-8")

    def check(self, text=None, relative="docs/design/skill/workflow.md"):
        self.path.write_text(self.text if text is None else text, encoding="utf-8")
        return validate_changed_spec(self.root, relative)

    def test_model_current_files_validate_without_activation_or_change_record(self):
        for relative in EXPECTED_MODEL_PATHS:
            with self.subTest(relative=relative):
                (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
                (self.root / relative).write_bytes((ROOT / relative).read_bytes())
                self.assertEqual(validate_changed_spec(self.root, relative), ())
        self.assertFalse((self.root / "docs/changes").exists())

    def test_model_retired_marker_rejects_before_table_checks(self):
        retired = self.text.replace("Model validation contract: model-document-v1",
                                    "Model validation contract: explicit-recording-v1", 1)
        for text in (retired, retired.replace("## Requirements", "## Broken requirements", 1)):
            issues = self.check(text)
            self.assertEqual([i.code for i in issues], ["BFR-MODEL-CONTRACT"])
            self.assertIn("model-document-v1", issues[0].message)

    def test_model_design_example_and_parent_validate_without_counting_fenced_marker(self):
        parent = (ROOT / "docs/design/skill/authoring/design.md").read_text()
        examples = re.findall(r"^(`{3,})markdown\n([\s\S]*?)^\1[ \t]*$", parent, re.MULTILINE)
        example, = [text.rstrip("\n") for _,text in examples if text.startswith("# Label Normalization Design")]
        self.assertEqual(validate_model_record(parent, "docs/design/skill/authoring/design.md"), ())
        self.assertEqual(validate_model_record(example, "docs/design/label-normalization/label-normalization.md"), ())
        invalid = example.replace("Model validation contract: model-document-v1",
                                  "Model validation contract: unknown_value", 1)
        self.assertEqual([i.code for i in validate_model_record(invalid, "docs/design/label-normalization/label-normalization.md")],
                         ["BFR-MODEL-CONTRACT"])
        for source in ("skills/design/references/model-authoring.md", "skills/design/assets/design-skeleton.md"):
            text = (ROOT / source).read_text()
            self.assertIn("Model validation contract: model-document-v1", text)
            self.assertNotIn("Model validation contract: explicit-recording-v1", text)

    def test_model_mismatched_directory_examples_and_extra_nesting_reject(self):
        for relative in ("docs/design/cli/workflow.md", "docs/design/skill/examples/workflow/sample.md",
                         "docs/design/workflow/nested/workflow.md", "docs/design/skill/unknown_value.md",
                         "docs/design/skill/project-foundations/unknown_value.md", "docs/design/skill/discovery/unknown_value.md",
                         "docs/design/skill/authoring/unknown_value.md", "docs/design/skill/design.md",
                         "docs/design/cli/examples/records/records.md"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.text)
            self.assertTrue(validate_changed_spec(self.root, relative))

    def test_model_flat_historical_path_remains_explicitly_valid(self):
        path = self.root / "docs/design/workflow.md"
        path.write_text(self.text)
        self.assertEqual(validate_changed_spec(self.root, "docs/design/workflow.md"), ())

    def test_model_unknown_value_marker_and_dimension_fail_closed(self):
        for text in (
            self.text.replace("Model validation contract: model-document-v1", "Model validation contract: unknown_value", 1),
            self.text.replace("| Input domain |", "| unknown_value |", 1),
        ):
            with self.subTest(text=text[:50]):
                codes = {i.code for i in self.check(text)}
                self.assertTrue(codes & {"BFR-MODEL-CONTRACT", "BFR-MODEL-DIMENSIONS"}, codes)

    def test_model_missing_duplicate_malformed_tables_and_references_reject(self):
        variants = (
            self.text.replace("Model validation contract: model-document-v1\n", "", 1),
            self.text + "\nModel validation contract: model-document-v1\n",
            self.text + "\n## Requirements\n",
            self.text.replace("| Dimension | Requirement basis |", "| Dimension | unknown_value |", 1),
            self.text.replace(next(l for l in self.text.splitlines() if l.startswith("| Input domain |")), "| Input domain | not_in_vocabulary |", 1),
            self.text.replace(next(l for l in self.text.splitlines() if l.startswith("| Input domain |")), "| Input domain | WF-SR-02, WF-SR-02 |", 1),
            self.text.replace("| State/lifecycle |", "| Input domain |", 1),
            self.text.replace("| WF-SR-01 |", "| WF-SR-02 |", 1),
            self.text.replace("| WF-SR-01 |", "| 1-invalid |", 1),
            self.text.replace("| --- | --- | --- |\n| Input domain", "| bad | --- | --- |\n| Input domain", 1),
            self.text.replace(next(l for l in self.text.splitlines() if l.startswith("| Input domain |")), "| Input domain | WF-SR-02 | outcome | extra |", 1),
        )
        for index, text in enumerate(variants):
            with self.subTest(index=index):
                self.assertTrue(self.check(text))

    def test_model_not_applicable_requires_reason(self):
        row = next(l for l in self.text.splitlines() if l.startswith("| Input domain |"))
        self.assertEqual(self.check(self.text.replace(row, "| Input domain | - | Not applicable: no input behavior in this fixture. |")), ())
        for outcome in ("Not applicable:", "", "No reason"):
            self.assertTrue(self.check(self.text.replace(row, f"| Input domain | - | {outcome} |")))

    def test_model_unsafe_missing_and_symlink_paths_reject(self):
        self.check()
        for relative in ("docs/design/../workflow.md", "docs/design/nested/workflow.md", "docs/design/UPPER.md", "docs/design/missing.md"):
            self.assertTrue(validate_changed_spec(self.root, relative))
        self.path.unlink()
        outside = self.root / "outside.md"
        outside.write_text(self.text, encoding="utf-8")
        self.path.symlink_to(outside)
        self.assertTrue(validate_changed_spec(self.root, "docs/design/skill/workflow.md"))
        self.path.unlink()
        self.path.parent.rmdir()
        other = self.root / "other"
        other.mkdir()
        (other / "workflow.md").write_text(self.text, encoding="utf-8")
        self.path.parent.symlink_to(other, target_is_directory=True)
        self.assertTrue(validate_changed_spec(self.root, "docs/design/skill/workflow.md"))

    def test_model_fenced_contract_or_tables_are_not_authority(self):
        self.assertTrue(self.check("```md\n" + self.text + "\n```\n"))
        self.assertTrue(self.check(self.text.replace("## Requirements", "```md\n## Requirements", 1) + "\n```\n"))

    def test_model_indented_code_cannot_supply_required_sections(self):
        headings = {"## Requirements", "### Boundary scan and acceptance scenarios"}

        def indent_sections(prefix, tables_only=False):
            lines = []
            selected = False
            for line in self.text.splitlines():
                if line.startswith("#"):
                    selected = line in headings
                indent = selected and line and (not tables_only or line.startswith("|"))
                lines.append(prefix + line if indent else line)
            return "\n".join(lines) + "\n"

        for prefix in ("    ", "\t", "  \t"):
            for tables_only in (False, True):
                with self.subTest(prefix=prefix, tables_only=tables_only):
                    issues = self.check(indent_sections(prefix, tables_only))
                    self.assertIn("BFR-MODEL-TABLE", {issue.code for issue in issues})
        # Up to three spaces remain ordinary Markdown, not an indented code block.
        self.assertEqual(self.check(indent_sections("   ")), ())

    def test_model_public_check_is_read_only_and_not_activation(self):
        self.check()
        before = relevant_tree_snapshot(self.root)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate-boundary-first.py"), "--check", "--root", str(self.root), "--path", "docs/design/skill/workflow.md"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["validation"], "structure-and-references-only")
        self.assertNotIn("activation", data)
        self.assertEqual(relevant_tree_snapshot(self.root), before)
