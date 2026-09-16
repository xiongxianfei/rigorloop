"""Bounded actionable drift diagnostics and public check output."""

from __future__ import annotations

import sys
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging.adapter_distribution import AdapterDriftEntry, collect_adapter_drift_entries, format_adapter_drift_normal, format_adapter_drift_verbose, sync_adapter_output
from adapter_fixture_helpers import (copy_fixture_skills)


class AdapterDiagnosticsTests(unittest.TestCase):
    maxDiff = None

    def test_clean_adapter_check_normal_output_is_summary_first(self) -> None:
        output = format_adapter_drift_normal(
            [],
            version="0.1.1",
            output_root=ROOT / "dist" / "adapters",
        )

        self.assertIn("adapters.drift: ok", output)
        self.assertIn("version: 0.1.1", output)
        self.assertIn("output_root:", output)
        self.assertIn("status: generated adapter output is in sync", output)
        self.assertNotIn("unchanged", output)
        self.assertLessEqual(len(output.splitlines()), 40)

    def test_normal_adapter_drift_output_is_bounded_and_actionable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            for path in sorted(output_root.rglob("SKILL.md"))[:20]:
                path.unlink()
            for path in sorted(output_root.rglob("AGENTS.md")):
                path.write_text(path.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
            for index in range(30):
                unexpected_file = output_root / "codex" / f"unexpected-{index}.txt"
                unexpected_file.write_text("unexpected\n", encoding="utf-8")

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )
            output = format_adapter_drift_normal(
                entries,
                version="0.1.0-rc.1",
                output_root=output_root,
                max_entries=5,
            )

            self.assertIn("adapters.drift: failed", output)
            self.assertIn("version: 0.1.0-rc.1", output)
            self.assertIn("output_root:", output)
            self.assertIn("failures: total=", output)
            self.assertIn("missing=", output)
            self.assertIn("stale=", output)
            self.assertIn("unexpected=", output)
            self.assertIn("- missing:", output)
            self.assertIn("action:", output)
            self.assertIn("omitted:", output)
            self.assertIn("--verbose", output)
            self.assertLess(len(output.splitlines()), len(entries))
            self.assertLessEqual(len(output.splitlines()), 40)

    def test_verbose_adapter_drift_output_includes_every_entry_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            (output_root / "manifest.yaml").unlink()
            stale_file = output_root / "codex" / "AGENTS.md"
            stale_file.write_text(stale_file.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
            unexpected_file = output_root / "codex" / "unexpected.txt"
            unexpected_file.write_text("unexpected\n", encoding="utf-8")

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )
            first_output = format_adapter_drift_verbose(
                entries,
                version="0.1.0-rc.1",
                output_root=output_root,
            )
            second_output = format_adapter_drift_verbose(
                entries,
                version="0.1.0-rc.1",
                output_root=output_root,
            )

            self.assertEqual(first_output, second_output)
            self.assertIn("adapters.drift: failed", first_output)
            self.assertEqual(first_output.count("\n- "), len(entries))
            for entry in entries:
                self.assertIn(entry.category, first_output)
                self.assertIn(str(entry.path), first_output)

    def test_adapter_drift_normal_output_reports_over_budget_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"
            output_root.mkdir(parents=True)
            entries = tuple(
                AdapterDriftEntry(
                    category="stale",
                    path=output_root / f"file-{index}.md",
                    detail="stale generated adapter file",
                )
                for index in range(90)
            )

            output = format_adapter_drift_normal(
                entries,
                version="0.1.1",
                output_root=output_root,
                max_entries=len(entries),
            )

            self.assertGreater(len(output.splitlines()), 80)
            self.assertIn("warning: normal output exceeded 80 lines", output)
            self.assertIn("--verbose", output)

    def test_build_adapters_cli_supports_verbose_check_only(self) -> None:
        verbose_check = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build-adapters.py"),
                "--check",
                "--verbose",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertEqual(verbose_check.returncode, 0, verbose_check.stdout + verbose_check.stderr)
        self.assertIn("adapters.drift: ok", verbose_check.stdout)

        tracked_verbose_check = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build-adapters.py"),
                "--version",
                "0.1.2",
                "--check",
                "--verbose",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(tracked_verbose_check.returncode, 0, tracked_verbose_check.stdout + tracked_verbose_check.stderr)
        self.assertIn("adapters.drift: ok", tracked_verbose_check.stdout)

        invalid_verbose = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build-adapters.py"),
                "--version",
                "0.1.1",
                "--verbose",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertNotEqual(invalid_verbose.returncode, 0)
        self.assertIn("--verbose is only supported with --check", invalid_verbose.stderr)
