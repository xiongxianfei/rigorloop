"""Real command discovery of current models and owned examples."""

from __future__ import annotations

import sys
from pathlib import Path
import json
import subprocess
import tempfile
import unittest

from boundary_fixture_helpers import (
    EXPECTED_MODEL_PATHS,
    ROOT,
    valid_feature,
    valid_proof,
)

sys.path.insert(0, str(ROOT / "scripts"))
from catalog_admission_fixture_helpers import current_documents




class CurrentBoundaryCommandTests(unittest.TestCase):
    def run_check(self, root, *paths):
        command = [sys.executable, str(ROOT / "scripts/validate-boundary-first.py"), "--check", "--root", str(root)]
        for path in paths:
            command.extend(["--path", path])
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout)

    def test_default_checks_complete_current_model_population_without_specs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            details = current_documents(root)
            code, output = self.run_check(root)
            self.assertEqual(code, 0, output)
            self.assertEqual(set(output["paths"]), set(EXPECTED_MODEL_PATHS) | details)
            self.assertNotIn("activation", output)
            self.assertNotIn("rollback_release", output)
            (root / "docs/design/system.md").unlink()
            code, output = self.run_check(root)
            self.assertEqual(code, 1, output)
            self.assertTrue(output["issues"])

    def test_default_checks_owned_examples_and_redacts_parse_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            details = current_documents(root)
            example = root / "docs/design/cli/examples/case.json"
            example.parent.mkdir(parents=True)
            example.write_text('{"secret": "private-value"}')
            code, output = self.run_check(root)
            self.assertEqual(code, 0, output)
            self.assertIn(example.relative_to(root).as_posix(), output["examples"])
            self.assertTrue(any("#model-example-" in path for path in output["examples"]))
            example.write_text('{"secret": private-value}')
            code, output = self.run_check(root)
            self.assertEqual(code, 1)
            self.assertNotIn("private-value", json.dumps(output))
            example.unlink()
            example.symlink_to(root / "docs/design/system.md")
            code, output = self.run_check(root)
            self.assertEqual(code, 1)
            self.assertIn("BFR-EXAMPLE-PATH", {item["check_id"] for item in output["issues"]})

    def test_empty_model_population_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, output = self.run_check(Path(temporary))
            self.assertEqual(code, 1)
            self.assertTrue(output["issues"])

    def test_explicit_customer_grammar_does_not_require_repository_activation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            (root / "specs/feature.md").write_text(valid_feature())
            (root / "specs/feature.test.md").write_text(valid_proof())
            code, output = self.run_check(root, "specs/feature.test.md")
            self.assertEqual(code, 0, output)
            self.assertEqual(output["status"], "passed")
