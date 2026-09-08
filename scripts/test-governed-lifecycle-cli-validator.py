#!/usr/bin/env python3
"""The repository wrapper uses current discovery, including its failure boundary."""
import io
import json
import runpy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(Path(__file__).with_name("validate-governed-lifecycle-cli.py")))


class CurrentRecordDiscoveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "docs/changes").mkdir(parents=True)

    def run_check(self, **kwargs):
        output = io.StringIO()
        code = MODULE["main"](root=self.root, output=output, **kwargs)
        return code, json.loads(output.getvalue())

    def test_archive_is_excluded_and_current_set_validates_without_activation(self):
        archive = self.root / "docs/changes/old/change.yaml"
        archive.parent.mkdir()
        archive.write_bytes(b"malformed archived bytes\xff")
        fixture = json.loads((ROOT / "tests/fixtures/rigorloop-records-v2/records.json").read_text())["change"]
        fixture.update(records=[], applicability=[], blockers=[])
        target = self.root / "docs/changes/example/change.json"
        target.parent.mkdir()
        target.write_text(json.dumps(fixture) + "\n")
        code, report = self.run_check()
        self.assertEqual(code, 0, report)
        self.assertEqual(report["context"]["scope"]["candidate_count"], 1)
        self.assertEqual(report["context"]["scope"]["excluded_noncurrent"], 1)
        self.assertEqual(archive.read_bytes(), b"malformed archived bytes\xff")

    def test_invalid_current_residue_does_not_become_an_archive(self):
        target = self.root / "docs/changes/example/evidence.json"
        target.parent.mkdir()
        target.write_text("{}\n")
        code, report = self.run_check()
        self.assertEqual(code, 1)
        self.assertFalse(report["context"]["scope"]["complete"])

    def test_unavailable_malformed_and_incomplete_results_fail(self):
        for result in (SimpleNamespace(returncode=1, stdout=""), SimpleNamespace(returncode=0, stdout='{}'), SimpleNamespace(returncode=0, stdout='{"schema_version":2,"command":"workflow-context","status":"success","scope":{"complete":false}}')):
            with self.subTest(result=result):
                self.assertEqual(self.run_check(runner=lambda *a, **k: result)[0], 1)


if __name__ == "__main__":
    unittest.main()
