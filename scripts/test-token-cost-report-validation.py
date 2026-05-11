#!/usr/bin/env python3
"""Fixture-driven tests for token-cost release report validation."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-token-cost-report.py"
VALID_FIXTURE = (
    ROOT / "tests" / "fixtures" / "token-cost" / "reports" / "valid-final-pass" / "v0.1.1.yaml"
)
OMITTED_ANALYSIS = (
    "tests/fixtures/token-cost/reports/valid-raw-omitted/proposal-short-run1.analysis.yaml"
)
OMITTED_SUMMARY = "tests/fixtures/token-cost/reports/valid-raw-omitted/sanitized-summary.yaml"
RC_REUSE_SURFACE_TEXT = (
    "No public skills, adapter output, workflow guide, benchmark prompts, "
    "analyzer scripts, fixtures, model/tool version, or release packaging changes since RC."
)
RC_REUSE_SURFACE_REMOVALS = {
    "public_skills": "public skills, ",
    "adapter_output": "adapter output, ",
    "workflow_guide": "workflow guide, ",
    "benchmark_prompts": "benchmark prompts, ",
    "analyzer": "analyzer scripts, ",
    "fixture": "fixtures, ",
    "model_or_tool_version": "model/tool version, ",
    "release_packaging": "or release packaging ",
}


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class TokenCostReportValidatorTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.valid_text = VALID_FIXTURE.read_text(encoding="utf-8")

    def with_valid_rc_reuse(self, text: str, relevant_changes: bool = False) -> str:
        return text + "\n".join(
            [
                "",
                "rc_reuse:",
                "  reused_from: v0.1.1-rc.1",
                f"  benchmark_relevant_changes_since_rc: {'true' if relevant_changes else 'false'}",
                "  checked_by: release-owner",
                "  checked_surface: release checklist",
                f"  rationale: {RC_REUSE_SURFACE_TEXT}",
                "",
            ]
        )

    def write_case(self, text: str) -> Path:
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".yaml", delete=False)
        with handle:
            handle.write(text)
        return Path(handle.name)

    def assertPasses(self, text: str) -> None:
        path = self.write_case(text)
        try:
            result = run_validator(path)
        finally:
            path.unlink()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("valid token-cost report metadata", result.stdout)

    def assertFails(self, text: str, expected_text: str) -> None:
        path = self.write_case(text)
        try:
            result = run_validator(path)
        finally:
            path.unlink()
        combined = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0, "expected validator to fail")
        self.assertIn(expected_text, combined)

    def test_markdown_report_must_name_yaml_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "v0.1.1.md"
            yaml_path = root / "v0.1.1.yaml"
            md.write_text("# Token-Friendliness Report\n\nNo metadata link.\n", encoding="utf-8")
            metadata = self.valid_text.replace(
                "report_markdown: tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.md",
                f"report_markdown: {md}",
            )
            yaml_path.write_text(metadata, encoding="utf-8")

            result = run_validator(yaml_path)

        combined = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "report.report_markdown must name or link the YAML metadata file",
            combined,
        )

    def test_markdown_report_may_name_yaml_metadata_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "v0.1.1.md"
            yaml_path = root / "v0.1.1.yaml"
            md.write_text(
                f"# Token-Friendliness Report\n\nStructured metadata: `{yaml_path}`\n",
                encoding="utf-8",
            )
            metadata = self.valid_text.replace(
                "report_markdown: tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.md",
                f"report_markdown: {md}",
            )
            yaml_path.write_text(metadata, encoding="utf-8")

            result = run_validator(yaml_path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("valid token-cost report metadata", result.stdout)

    def test_valid_final_pass_metadata_passes(self) -> None:
        result = run_validator(VALID_FIXTURE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("valid token-cost report metadata", result.stdout)

    def test_required_fields_and_enums_are_enforced(self) -> None:
        self.assertFails(
            self.valid_text.replace("schema_version: 1\n\n", "", 1),
            "schema_version: missing required field",
        )
        self.assertFails(
            self.valid_text.replace("release_gate:\n  result: pass", "release_gate:\n  result: done"),
            "release_gate.result: expected one of",
        )
        self.assertFails(
            self.valid_text.replace("status: pass", "status: hard warning", 1),
            "static_skill_size.status: expected one of",
        )

    def test_dynamic_status_rules_for_final_and_non_final_reports(self) -> None:
        self.assertFails(
            self.valid_text.replace("dynamic_runtime:\n  status: pass", "dynamic_runtime:\n  status: blocked"),
            "dynamic_runtime.status: final public releases require pass or waived",
        )
        self.assertFails(
            self.valid_text.replace("release: v0.1.1", "release: v0.1.1-rc.1").replace(
                "dynamic_runtime:\n  status: pass",
                "dynamic_runtime:\n  status: not-run",
            ),
            "dynamic_runtime.incomplete: required when dynamic runtime is blocked or not-run",
        )
        self.assertPasses(
            self.valid_text.replace("release: v0.1.1", "release: v0.1.1-rc.1")
            .replace("dynamic_runtime:\n  status: pass", "dynamic_runtime:\n  status: not-run")
            .replace(
                "  incomplete: null",
                "\n".join(
                    [
                        "  incomplete:",
                        "    reason: Codex CLI unavailable",
                        "    owner: release owner",
                        "    environment: maintainer-local",
                        "    follow_up: Run before final release",
                        "    release_may_proceed: true",
                    ]
                ),
            )
        )

    def test_final_waiver_requires_approved_reason_and_evidence(self) -> None:
        waived = (
            self.valid_text.replace("dynamic_runtime:\n  status: pass", "dynamic_runtime:\n  status: waived")
            .replace("  required: false", "  required: true")
            .replace("  status: none", "  status: approved")
            .replace('  reason: ""', "  reason: Codex unavailable; no benchmark-relevant changes since passing RC run.")
            .replace('  approved_by: ""', "  approved_by: release-owner")
            .replace('  approval_surface: ""', "  approval_surface: release checklist")
            .replace('  evidence: ""', "  evidence: tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml")
        )
        self.assertFails(waived, "rc_reuse: required when final waiver references RC benchmark evidence")
        self.assertPasses(self.with_valid_rc_reuse(waived))
        self.assertFails(
            self.with_valid_rc_reuse(waived).replace("  status: approved", "  status: requested"),
            "waiver.status: waived dynamic runtime requires approved waiver",
        )
        self.assertFails(
            self.with_valid_rc_reuse(waived).replace(
                "Codex unavailable; no benchmark-relevant changes since passing RC run.",
                "forgot to run it",
            ),
            "waiver.reason: invalid waiver reason",
        )

    def test_rc_reuse_metadata_is_required_and_validated(self) -> None:
        waived = (
            self.valid_text.replace("dynamic_runtime:\n  status: pass", "dynamic_runtime:\n  status: waived")
            .replace("  required: false", "  required: true")
            .replace("  status: none", "  status: approved")
            .replace('  reason: ""', "  reason: Codex unavailable; no benchmark-relevant changes since passing RC run.")
            .replace('  approved_by: ""', "  approved_by: release-owner")
            .replace('  approval_surface: ""', "  approval_surface: release checklist")
            .replace('  evidence: ""', "  evidence: tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml")
        )
        self.assertFails(waived, "rc_reuse: required when final waiver references RC benchmark evidence")

        valid = self.with_valid_rc_reuse(waived)
        self.assertPasses(valid)
        self.assertFails(
            valid.replace("  reused_from: v0.1.1-rc.1\n", ""),
            "rc_reuse.reused_from: expected non-empty string",
        )
        self.assertFails(
            valid.replace("  checked_by: release-owner\n", ""),
            "rc_reuse.checked_by: expected non-empty string",
        )
        self.assertFails(
            valid.replace("  checked_surface: release checklist\n", ""),
            "rc_reuse.checked_surface: expected non-empty string",
        )
        self.assertFails(
            valid.replace(
                "  rationale: No public skills, adapter output, workflow guide, benchmark prompts, analyzer scripts, fixtures, model/tool version, or release packaging changes since RC.\n",
                "",
            ),
            "rc_reuse.rationale: expected non-empty string",
        )
        self.assertFails(
            valid.replace(
                RC_REUSE_SURFACE_TEXT,
                "No relevant changes.",
            ),
            "rc_reuse checked_surface/rationale must cover all required benchmark-relevant surface categories",
        )
        self.assertPasses(self.with_valid_rc_reuse(waived, relevant_changes=True))

    def test_rc_reuse_false_requires_every_checked_surface_category(self) -> None:
        waived = (
            self.valid_text.replace("dynamic_runtime:\n  status: pass", "dynamic_runtime:\n  status: waived")
            .replace("  required: false", "  required: true")
            .replace("  status: none", "  status: approved")
            .replace('  reason: ""', "  reason: Codex unavailable; no benchmark-relevant changes since passing RC run.")
            .replace('  approved_by: ""', "  approved_by: release-owner")
            .replace('  approval_surface: ""', "  approval_surface: release checklist")
            .replace('  evidence: ""', "  evidence: tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml")
        )
        self.assertPasses(self.with_valid_rc_reuse(waived))

        for category, text in RC_REUSE_SURFACE_REMOVALS.items():
            with self.subTest(category=category):
                self.assertFails(
                    self.with_valid_rc_reuse(waived).replace(text, ""),
                    f"missing: {category}",
                )

    def test_raw_jsonl_and_sanitized_evidence_contracts_are_enforced(self) -> None:
        omitted = (
            self.valid_text.replace("raw_jsonl_tracked: true", "raw_jsonl_tracked: false")
            .replace(
                "jsonl: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.jsonl",
                'jsonl: ""',
            )
            .replace(
                "analysis: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.analysis.yaml",
                f"analysis: {OMITTED_ANALYSIS}",
            )
            .replace('sanitized_summary: ""', f"sanitized_summary: {OMITTED_SUMMARY}")
            .replace('raw_omission_reason: ""', "raw_omission_reason: raw JSONL contained local machine paths")
        )
        self.assertPasses(omitted)
        self.assertFails(
            self.valid_text.replace(
                "tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.jsonl",
                "tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/missing.jsonl",
            ),
            "dynamic_runtime.runs[0].evidence.jsonl: referenced path does not exist",
        )
        self.assertFails(
            omitted.replace(
                "raw_omission_reason: raw JSONL contained local machine paths",
                'raw_omission_reason: ""',
            ),
            "dynamic_runtime.runs[0].evidence.raw_omission_reason: expected non-empty string",
        )

    def test_comparison_portability_and_runner_rules_are_enforced(self) -> None:
        self.assertFails(
            self.valid_text.replace("baseline: true", "baseline: false").replace(
                "deltas: null",
                "deltas: null",
            ),
            "comparison.previous_report: required for non-baseline comparable reports",
        )
        self.assertFails(
            self.valid_text.replace("portability:\n  status: pass", "portability:\n  status: fail"),
            "portability.status: public skill portability failure blocks release",
        )
        self.assertFails(
            self.valid_text.replace(
                "skill_source: dist/adapters/codex/.agents/skills/",
                "skill_source: .codex/skills/",
            ),
            "runner.skill_source: expected dist/adapters/codex/.agents/skills/",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
