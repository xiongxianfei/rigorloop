#!/usr/bin/env python3
"""Tests for token-cost measurement scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEASURE = ROOT / "scripts" / "measure-skill-tokens.py"
ANALYZE = ROOT / "scripts" / "analyze-codex-jsonl.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class StaticSkillMeasurementTests(unittest.TestCase):
    def test_reports_required_fields_and_largest_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "sample" / "SKILL.md"
            skill_dir.parent.mkdir(parents=True)
            skill_dir.write_text(
                "\n".join(
                    [
                        "---",
                        "name: sample",
                        "description: Sample skill.",
                        "---",
                        "# Sample",
                        "",
                        "## Short",
                        "Small section.",
                        "",
                        "## Longer",
                        "This section has enough words to be the larger section.",
                    ]
                ),
                encoding="utf-8",
            )

            result = run_command(str(MEASURE), "--skills-root", tmp)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sample/SKILL.md", result.stdout)
        self.assertIn("bytes", result.stdout)
        self.assertIn("lines", result.stdout)
        self.assertIn("estimated_tokens", result.stdout)
        self.assertIn("status", result.stdout)
        self.assertIn("largest_sections", result.stdout)
        self.assertIn("Longer", result.stdout)

    def test_budget_warning_is_non_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "sample" / "SKILL.md"
            skill_dir.parent.mkdir(parents=True)
            skill_dir.write_text("# Sample\n\n" + ("word " * 60), encoding="utf-8")

            result = run_command(str(MEASURE), "--skills-root", tmp, "--warn-tokens", "1")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARNING", result.stdout)

    def test_empty_skill_root_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_command(str(MEASURE), "--skills-root", tmp)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no canonical skills found", result.stderr.lower())


class CodexJsonlAnalyzerTests(unittest.TestCase):
    def write_jsonl(self, *records: object) -> Path:
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".jsonl", delete=False)
        with handle:
            for record in records:
                handle.write(json.dumps(record))
                handle.write("\n")
        return Path(handle.name)

    def test_reports_usage_tool_output_and_cost_drivers(self) -> None:
        path = self.write_jsonl(
            {
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 40,
                    "output_tokens": 20,
                    "reasoning_output_tokens": 5,
                }
            },
            {
                "tool": "functions.exec_command",
                "args": {
                    "cmd": "rg -n TODO .",
                    "max_output_tokens": 50000,
                },
                "output": "a\nb\nc\n",
            },
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "sed -n '1,260p' docs/workflows.md"},
                "result": {"output": "x\n" * 12},
            },
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "sed -n '1,260p' docs/workflows.md"},
                "output": "again\n",
            },
        )
        try:
            result = run_command(str(ANALYZE), str(path))
        finally:
            path.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("input_tokens: 100", result.stdout)
        self.assertIn("cached_input_tokens: 40", result.stdout)
        self.assertIn("command_output_lines:", result.stdout)
        self.assertIn("command_output_bytes:", result.stdout)
        self.assertIn("estimated_command_output_tokens:", result.stdout)
        self.assertIn("broad_searches", result.stdout)
        self.assertIn("full_file_reads", result.stdout)
        self.assertIn("high_max_output_tokens", result.stdout)
        self.assertIn("repeated_file_reads", result.stdout)
        self.assertIn("top_cost_drivers", result.stdout)

    def test_usage_absent_still_reports_output(self) -> None:
        path = self.write_jsonl(
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "date"},
                "output": "Sun May 10\n",
            }
        )
        try:
            result = run_command(str(ANALYZE), str(path))
        finally:
            path.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("token_usage: unavailable", result.stdout)
        self.assertIn("command_output_lines: 1", result.stdout)

    def test_unknown_events_and_no_output_are_reported_without_fake_drivers(self) -> None:
        path = self.write_jsonl({"unexpected": {"shape": True}}, {"message": "hello"})
        try:
            result = run_command(str(ANALYZE), str(path))
        finally:
            path.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unknown_records: 2", result.stdout)
        self.assertIn("command_output_lines: 0", result.stdout)
        self.assertIn("no command-output amplification observed", result.stdout)

    def test_missing_and_malformed_input_fail_clearly(self) -> None:
        missing = run_command(str(ANALYZE), "/tmp/does-not-exist-codex-session.jsonl")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("missing file", missing.stderr.lower())

        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".jsonl", delete=False)
        with handle:
            handle.write('{"ok": true}\n')
            handle.write("{bad json}\n")
        malformed_path = Path(handle.name)
        try:
            malformed = run_command(str(ANALYZE), str(malformed_path))
        finally:
            malformed_path.unlink()

        self.assertNotEqual(malformed.returncode, 0)
        self.assertIn("malformed jsonl at line 2", malformed.stderr.lower())


if __name__ == "__main__":
    unittest.main()
