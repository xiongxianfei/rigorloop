#!/usr/bin/env python3
"""The retired projection helper rejects before reading or modifying input."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import runpy

SCRIPT = Path(__file__).with_name("query-change-record.py")


class RetiredQueryTests(unittest.TestCase):
    def test_public_queries_reject_without_reading_or_mutating_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "docs/changes/example/change.yaml"
            archive.parent.mkdir(parents=True)
            archive.write_bytes(b"private malformed archival bytes\xff")
            before = sorted(root.rglob("*"))
            for query in ("summary", "artifacts", "validation", "unknown_value"):
                result = subprocess.run([sys.executable, str(SCRIPT), "example", query, "--repo-root", str(root)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["code"], "unsupported-record-interface")
                self.assertNotIn("private", result.stdout + result.stderr)
                self.assertEqual(archive.read_bytes(), b"private malformed archival bytes\xff")
                self.assertEqual(sorted(root.rglob("*")), before)

    def test_no_input_decoder_or_filesystem_probe_is_used(self):
        module = runpy.run_path(str(SCRIPT))
        with patch("pathlib.Path.read_bytes", side_effect=AssertionError("must not read")), patch("builtins.print"):
            self.assertEqual(module["main"](["example", "summary"]), 2)


if __name__ == "__main__":
    unittest.main()
