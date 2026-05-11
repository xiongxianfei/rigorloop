#!/usr/bin/env python3
"""Tests for token-cost measurement scripts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEASURE = ROOT / "scripts" / "measure-skill-tokens.py"
ANALYZE = ROOT / "scripts" / "analyze-codex-jsonl.py"
RUNNER = ROOT / "scripts" / "run-token-cost-benchmarks.py"
BASELINE_REPORT = ROOT / "docs" / "reports" / "token-cost" / "2026-05-10-baseline.md"
CHANGE_METADATA = (
    ROOT
    / "docs"
    / "changes"
    / "2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation"
    / "change.yaml"
)
BENCHMARK_ROOT = ROOT / "benchmarks" / "token-cost"
BENCHMARK_MANIFEST = BENCHMARK_ROOT / "manifest.yaml"
BENCHMARK_FIXTURE = BENCHMARK_ROOT / "fixtures" / "minimal-public-project"
EXPECTED_BENCHMARKS = {
    "workflow-route": "workflow",
    "proposal-short": "proposal",
    "implement-handoff": "implement",
    "code-review-small": "code-review",
    "verify-final-pack": "verify",
    "architecture-no-impact": "architecture",
    "learn-no-durable-lesson": "learn",
}


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

    def test_current_codex_command_execution_events_report_aggregated_output(self) -> None:
        path = self.write_jsonl(
            {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "command": "sed -n '1,220p' /tmp/example/SKILL.md",
                    "aggregated_output": "alpha\nbeta\n",
                },
            }
        )
        summary = Path(tempfile.NamedTemporaryFile(suffix=".analysis.yaml", delete=True).name)
        try:
            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "current-codex-shape",
            )
            summary_text = summary.read_text(encoding="utf-8")
        finally:
            path.unlink()
            if summary.exists():
                summary.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("tool_calls: 1", result.stdout)
        self.assertIn("command_output_lines: 2", result.stdout)
        self.assertRegex(result.stdout, r"estimated_command_output_tokens: [1-9][0-9]*")
        self.assertIn("unknown_records: 0", result.stdout)
        self.assertIn("kind: command_execution", summary_text)
        self.assertIn("sed -n", summary_text)
        self.assertRegex(summary_text, r"estimated_tokens: [1-9][0-9]*")

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

    def test_writes_schema_version_1_summary_for_tracked_raw_jsonl(self) -> None:
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
                "args": {"cmd": "sed -n '1,260p' docs/workflows.md"},
                "output": "x\n" * 300,
            },
        )
        summary = Path(tempfile.NamedTemporaryFile(suffix=".analysis.yaml", delete=True).name)
        try:
            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "proposal-short",
            )
            summary_text = summary.read_text(encoding="utf-8")
        finally:
            path.unlink()
            if summary.exists():
                summary.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("schema_version: 1", summary_text)
        self.assertIn("id: proposal-short", summary_text)
        self.assertIn("raw_jsonl_tracked: true", summary_text)
        self.assertIn(f"jsonl: {path}", summary_text)
        self.assertIn("input_tokens: 100", summary_text)
        self.assertIn("total_estimated_tokens:", summary_text)
        self.assertIn("largest_event:", summary_text)
        self.assertIn("full_file_read_count: 1", summary_text)
        self.assertIn("result: warning", summary_text)

    def test_summary_uses_repo_relative_jsonl_path_when_under_repo(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            run_dir = Path(tmp)
            path = run_dir / "proposal-short-run1.jsonl"
            summary = run_dir / "proposal-short-run1.analysis.yaml"
            path.write_text(
                json.dumps(
                    {
                        "usage": {
                            "input_tokens": 1,
                            "cached_input_tokens": 0,
                            "output_tokens": 1,
                            "reasoning_output_tokens": 0,
                        }
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "proposal-short",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary_text = summary.read_text(encoding="utf-8")
            self.assertIn(f"jsonl: {path.relative_to(ROOT)}", summary_text)
            self.assertNotIn(str(ROOT), summary_text)

    def test_writes_schema_version_1_summary_for_omitted_raw_jsonl(self) -> None:
        path = self.write_jsonl(
            {
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 40,
                    "output_tokens": 20,
                    "reasoning_output_tokens": 5,
                }
            }
        )
        summary = Path(tempfile.NamedTemporaryFile(suffix=".analysis.yaml", delete=True).name)
        sanitized_summary = "docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.summary.yaml"
        try:
            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "proposal-short",
                "--raw-jsonl-omitted",
                "--sanitized-source",
                "codex-jsonl-local-run",
                "--sanitized-summary",
                sanitized_summary,
                "--raw-omission-reason",
                "raw JSONL contained local machine paths",
            )
            summary_text = summary.read_text(encoding="utf-8")
        finally:
            path.unlink()
            if summary.exists():
                summary.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("raw_jsonl_tracked: false", summary_text)
        self.assertIn('jsonl: ""', summary_text)
        self.assertIn("sanitized_source: codex-jsonl-local-run", summary_text)
        self.assertIn(f"sanitized_summary: {sanitized_summary}", summary_text)
        self.assertIn('raw_omission_reason: "raw JSONL contained local machine paths"', summary_text)

    def test_repeated_capped_same_file_reads_are_reported_as_signal(self) -> None:
        path = self.write_jsonl(
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "sed -n '1,20p' docs/workflows.md"},
                "output": "a\nb\n",
            },
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "sed -n '1,20p' docs/workflows.md"},
                "output": "c\nd\n",
            },
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "sed -n '1,20p' docs/workflows.md"},
                "output": "e\nf\n",
            },
        )
        summary = Path(tempfile.NamedTemporaryFile(suffix=".analysis.yaml", delete=True).name)
        try:
            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "repeated-check",
            )
            summary_text = summary.read_text(encoding="utf-8")
        finally:
            path.unlink()
            if summary.exists():
                summary.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("repeated_file_read_count: 1", summary_text)
        self.assertIn("path: docs/workflows.md", summary_text)
        self.assertIn("count: 3", summary_text)
        self.assertIn("result: none", summary_text)

    def test_justified_full_file_read_classification(self) -> None:
        path = self.write_jsonl(
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "cat docs/workflows.md"},
                "output": "x\n" * 120,
            },
        )
        summary = Path(tempfile.NamedTemporaryFile(suffix=".analysis.yaml", delete=True).name)
        try:
            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "justified-check",
                "--justified-read",
                "docs/workflows.md",
                "--justification",
                "explicit benchmark target",
            )
            summary_text = summary.read_text(encoding="utf-8")
        finally:
            path.unlink()
            if summary.exists():
                summary.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("result: justified", summary_text)
        self.assertIn('justification: "explicit benchmark target"', summary_text)
        self.assertIn("path: docs/workflows.md", summary_text)

    def test_mixed_justified_and_unjustified_reads_remain_confirmed(self) -> None:
        path = self.write_jsonl(
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "cat docs/workflows.md"},
                "output": "x\n" * 120,
            },
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "cat AGENTS.md"},
                "output": "y\n" * 120,
            },
        )
        summary = Path(tempfile.NamedTemporaryFile(suffix=".analysis.yaml", delete=True).name)
        try:
            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "mixed-check",
                "--justified-read",
                "docs/workflows.md",
                "--justification",
                "explicit benchmark target",
            )
            summary_text = summary.read_text(encoding="utf-8")
        finally:
            path.unlink()
            if summary.exists():
                summary.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("result: confirmed", summary_text)
        self.assertIn("justified_reads:", summary_text)
        self.assertIn("confirmed_reads:", summary_text)
        self.assertIn("path: AGENTS.md", summary_text)

    def test_justified_generated_output_read_classification(self) -> None:
        path = self.write_jsonl(
            {
                "tool": "functions.exec_command",
                "args": {"cmd": "cat dist/adapters/codex/.agents/skills/workflow/SKILL.md"},
                "output": "x\n" * 120,
            },
        )
        summary = Path(tempfile.NamedTemporaryFile(suffix=".analysis.yaml", delete=True).name)
        try:
            result = run_command(
                str(ANALYZE),
                str(path),
                "--summary-output",
                str(summary),
                "--run-id",
                "generated-check",
                "--justified-read",
                "dist/adapters/codex/.agents/skills/workflow/SKILL.md",
                "--justification",
                "generated-output validation",
            )
            summary_text = summary.read_text(encoding="utf-8")
        finally:
            path.unlink()
            if summary.exists():
                summary.unlink()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("result: justified", summary_text)
        self.assertIn("generated_output_read_count: 1", summary_text)
        self.assertIn('justification: "generated-output validation"', summary_text)


class BaselineReportTests(unittest.TestCase):
    def test_baseline_report_shape_and_change_link(self) -> None:
        self.assertTrue(BASELINE_REPORT.exists(), "baseline report must exist")
        report = BASELINE_REPORT.read_text(encoding="utf-8")
        for heading in [
            "# Token Cost Baseline: 2026-05-10",
            "## Summary",
            "## Static Skill Cost",
            "## Codex Session Cost",
            "## Tool-Output Amplification",
            "## Top Cost Drivers",
            "## Comparison To Previous Report",
            "## Conclusions",
            "## Next Actions",
        ]:
            self.assertIn(heading, report)
        self.assertIn("No previous baseline exists.", report)

        metadata = CHANGE_METADATA.read_text(encoding="utf-8")
        self.assertIn(
            "docs/reports/token-cost/2026-05-10-baseline.md",
            metadata,
        )


class BenchmarkFixtureTests(unittest.TestCase):
    def read_manifest(self) -> str:
        self.assertTrue(BENCHMARK_MANIFEST.exists(), "benchmark manifest must exist")
        return BENCHMARK_MANIFEST.read_text(encoding="utf-8")

    def test_manifest_lists_all_initial_prompt_fixtures(self) -> None:
        manifest = self.read_manifest()
        self.assertIn("suite: skill-token-runtime-v1", manifest)

        ids = set(re.findall(r"^\s+- id: ([a-z0-9-]+)$", manifest, flags=re.MULTILINE))
        self.assertEqual(set(EXPECTED_BENCHMARKS), ids)

        for benchmark_id, expected_skill in EXPECTED_BENCHMARKS.items():
            prompt_path = BENCHMARK_ROOT / "prompts" / f"{benchmark_id}.md"
            self.assertTrue(prompt_path.exists(), f"{benchmark_id} prompt must exist")
            prompt = prompt_path.read_text(encoding="utf-8")
            self.assertIn("Do not edit files.", prompt)
            self.assertIn(f"expected_skill: {expected_skill}", manifest)
            self.assertIn(f"path: prompts/{benchmark_id}.md", manifest)
            self.assertIn("tool: codex", manifest)
            self.assertIn("expected_result: pass", manifest)

    def test_minimal_public_project_fixture_is_clean_and_complete(self) -> None:
        required_files = [
            "AGENTS.md",
            "VISION.md",
            "README.md",
            "docs/workflows.md",
            "docs/changes/.gitkeep",
            "src/example.txt",
        ]
        for relative_path in required_files:
            self.assertTrue(
                (BENCHMARK_FIXTURE / relative_path).exists(),
                f"fixture missing {relative_path}",
            )

        forbidden_paths = [
            BENCHMARK_FIXTURE / ".codex" / "skills",
            BENCHMARK_FIXTURE / ".agents" / "skills",
        ]
        for path in forbidden_paths:
            self.assertFalse(path.exists(), f"fixture must not contain installed skills: {path}")

        fixture_files = [path for path in BENCHMARK_FIXTURE.rglob("*") if path.is_file()]
        self.assertLessEqual(len(fixture_files), 8, "fixture should stay intentionally small")

        fixture_text = "\n".join(path.read_text(encoding="utf-8") for path in fixture_files)
        self.assertNotIn("dist/adapters", fixture_text)
        self.assertNotIn(".codex/skills", fixture_text)


class BenchmarkRunnerTests(unittest.TestCase):
    def test_runner_dry_run_installs_public_skills_and_writes_analyzer_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp) / "temp"
            output_dir = ROOT / "docs" / "reports" / "token-cost" / "runs" / "review-check"
            if output_dir.exists():
                for path in output_dir.iterdir():
                    path.unlink()
            result = run_command(
                str(RUNNER),
                "--release",
                "v0.1.1",
                "--suite",
                str(BENCHMARK_MANIFEST),
                "--tool",
                "codex",
                "--temp-root",
                str(temp_root),
                "--output-dir",
                str(output_dir),
                "--keep-temp",
                "--dry-run",
            )

            try:
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("dry_run: true", result.stdout)
                self.assertIn("skill_source: dist/adapters/codex/.agents/skills/", result.stdout)
                self.assertIn(
                    "codex_command: codex exec --json --ephemeral --skip-git-repo-check",
                    result.stdout,
                )
                self.assertIn("analyzer_command:", result.stdout)
                self.assertEqual(
                    sorted(path.name for path in output_dir.glob("*.jsonl")),
                    [f"{benchmark_id}-run1.jsonl" for benchmark_id in sorted(EXPECTED_BENCHMARKS)],
                )
                for benchmark_id in EXPECTED_BENCHMARKS:
                    summary = output_dir / f"{benchmark_id}-run1.analysis.yaml"
                    self.assertTrue(summary.exists(), f"missing analyzer summary for {benchmark_id}")
                    summary_text = summary.read_text(encoding="utf-8")
                    self.assertIn("schema_version: 1", summary_text)
                    self.assertIn(
                        f"jsonl: {output_dir.relative_to(ROOT)}/{benchmark_id}-run1.jsonl",
                        summary_text,
                    )
                    self.assertNotIn(str(ROOT), summary_text)

                temp_runs = list(temp_root.glob("rigorloop-token-bench-v0.1.1-*"))
                self.assertEqual(len(temp_runs), 1)
                self.assertTrue(
                    (temp_runs[0] / ".agents" / "skills" / "proposal" / "SKILL.md").exists()
                )
                self.assertFalse((BENCHMARK_FIXTURE / ".agents" / "skills").exists())
            finally:
                if output_dir.exists():
                    for path in output_dir.iterdir():
                        path.unlink()
                    output_dir.rmdir()

    def test_runner_rejects_repository_local_codex_skill_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_command(
                str(RUNNER),
                "--release",
                "v0.1.1",
                "--suite",
                str(BENCHMARK_MANIFEST),
                "--tool",
                "codex",
                "--skill-source",
                ".codex/skills/",
                "--temp-root",
                tmp,
                "--dry-run",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "skill source must be dist/adapters/codex/.agents/skills/",
            result.stderr,
        )

    def test_runner_rejects_temp_root_inside_repository(self) -> None:
        result = run_command(
            str(RUNNER),
            "--release",
            "v0.1.1",
            "--suite",
            str(BENCHMARK_MANIFEST),
            "--tool",
            "codex",
            "--temp-root",
            str(ROOT / ".tmp-token-bench"),
            "--dry-run",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("temporary root must be outside the repository", result.stderr)

    def test_runner_deletes_temp_directory_after_success_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp) / "temp"
            output_dir = Path(tmp) / "runs"
            result = run_command(
                str(RUNNER),
                "--release",
                "v0.1.1",
                "--suite",
                str(BENCHMARK_MANIFEST),
                "--tool",
                "codex",
                "--temp-root",
                str(temp_root),
                "--output-dir",
                str(output_dir),
                "--dry-run",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(list(temp_root.glob("rigorloop-token-bench-v0.1.1-*")))

    def test_runner_does_not_generate_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "runs"
            result = run_command(
                str(RUNNER),
                "--release",
                "v0.1.1",
                "--suite",
                str(BENCHMARK_MANIFEST),
                "--tool",
                "codex",
                "--temp-root",
                tmp,
                "--output-dir",
                str(output_dir),
                "--dry-run",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(list(output_dir.glob("*.md")))


if __name__ == "__main__":
    unittest.main()
