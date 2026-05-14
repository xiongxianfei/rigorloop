#!/usr/bin/env python3
"""Fixture-driven tests for token-cost release report validation."""

from __future__ import annotations

import importlib.util
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
LIFECYCLE_TEMPLATE = ROOT / "templates" / "lifecycle-token-cost-summary.md"
M4_LIFECYCLE_SUMMARY = (
    ROOT
    / "docs"
    / "reports"
    / "token-cost"
    / "lifecycle"
    / "2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md"
)
LIFECYCLE_REQUIRED_HEADINGS = [
    "## Identity",
    "## Trigger",
    "## Scope",
    "## Source Artifacts",
    "## Observed Cost Drivers",
    "## Largest Observed Event",
    "## Result / Rationale",
]
LIFECYCLE_COST_DRIVER_TERMS = [
    "broad searches",
    "large command outputs",
    "full-skill reads",
    "repeated file reads",
    "generated-output reads",
    "review rounds",
    "validation runs",
]
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


def run_validator(path: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path), *extra_args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load_validator_module():
    spec = importlib.util.spec_from_file_location("token_cost_validator_test", VALIDATOR)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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

    def assertContainsAll(self, text: str, terms: list[str]) -> None:
        lowered = text.lower()
        missing = [term for term in terms if term.lower() not in lowered]
        self.assertEqual(missing, [])

    def assertLifecycleHeadingsPresent(self, text: str) -> None:
        for heading in LIFECYCLE_REQUIRED_HEADINGS:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def assertNoLifecycleHardGateCues(self, text: str) -> None:
        lowered = text.lower()
        forbidden = [
            "hard_gate_recommendation:",
            "threshold_regression_result:",
            "release_may_proceed:",
            "ci must block",
            "release must block",
        ]
        present = [term for term in forbidden if term in lowered]
        self.assertEqual(present, [])

    def v2_context_text(
        self,
        *,
        core: list[str] | None = None,
        transition_carryover: list[str] | None = None,
        required_due_to_changes: str = "",
    ) -> str:
        core = core if core is not None else ["proposal-short"]
        transition_carryover = transition_carryover if transition_carryover is not None else []
        core_block = "\n".join(["  core:", *[f"    - {item}" for item in core]]) if core else "  core: []"
        carryover_block = (
            "\n".join(
                ["  transition_carryover:", *[f"    - {item}" for item in transition_carryover]]
            )
            if transition_carryover
            else "  transition_carryover: []"
        )
        changed_block = (
            "\n".join(["  required_due_to_changes:", required_due_to_changes])
            if required_due_to_changes
            else "  required_due_to_changes: []"
        )
        return "\n".join(
            [
                "schema_version: 1",
                "context_source: test",
                "",
                "release:",
                "  version: v0.1.1",
                "  stage: final",
                "  commit: abc123",
                "",
                "benchmark_suite:",
                "  id: skill-token-runtime-v2",
                "  manifest: benchmarks/token-cost/manifest.yaml",
                "",
                "required_benchmarks:",
                core_block,
                carryover_block,
                changed_block,
                "",
                "optional_benchmarks:",
                "  extended:",
                "    - architecture-review",
                "",
                "waiver_policy:",
                "  final_release_requires_pass_or_waiver: true",
                "  inconclusive_requires_waiver_for_required_benchmarks: true",
                "  allowed_approver_roles:",
                "    - release-owner",
                "    - release-manager",
                "    - repository-maintainer",
                "",
            ]
        )

    def v2_report_text(
        self,
        *,
        proposal_quality_status: str = "pass",
        proposal_waiver: str = "",
        include_proposal_run: bool = True,
        optional_quality_status: str = "pass",
        optional_claimed: bool = False,
        optional_required: bool = False,
        optional_coverage_quality_status: str | None = None,
        optional_warning: str = "",
        include_optional_run: bool = True,
    ) -> str:
        md = "tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.md"
        optional_coverage_quality_status = (
            optional_coverage_quality_status
            if optional_coverage_quality_status is not None
            else optional_quality_status
        )
        proposal_run = ""
        if include_proposal_run:
            proposal_run = f"""
    - id: proposal-short
      prompt: tests/fixtures/token-cost/reports/valid-final-pass/prompts/proposal-short.md
      fixture: tests/fixtures/token-cost/reports/valid-final-pass/minimal-public-project
      result: pass
      evidence:
        raw_jsonl_tracked: true
        jsonl: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.jsonl
        analysis: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.analysis.yaml
        sanitized_summary: ""
        raw_omission_reason: ""
      result_quality:
        status: {proposal_quality_status}
        reviewed_by: maintainer
        review_surface: {md}
        reviewed_at: "2026-05-11"
        criteria:
          - id: output_shape
            expectation: Output followed the requested shape.
            result: pass
            notes: ""
        notes: Manual review accepted this benchmark.
        blockers: []{proposal_waiver}
"""
        optional_run = ""
        if include_optional_run:
            optional_run = f"""
    - id: architecture-review
      prompt: benchmarks/token-cost/prompts/architecture-review.md
      fixture: benchmarks/token-cost/fixtures/minimal-public-project-architecture-review
      result: pass
      evidence:
        raw_jsonl_tracked: true
        jsonl: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.jsonl
        analysis: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.analysis.yaml
        sanitized_summary: ""
        raw_omission_reason: ""
      result_quality:
        status: {optional_quality_status}
        reviewed_by: maintainer
        review_surface: {md}
        reviewed_at: "2026-05-11"
        criteria:
          - id: no_change_local_delta_required
            expectation: Output does not require a change-local architecture delta.
            result: pass
            notes: ""
        notes: Manual review accepted this optional benchmark.
        blockers: []
"""
        warning_field = (
            "  warnings:\n" + optional_warning
            if optional_warning
            else "  warnings: []"
        )
        return f"""schema_version: 1

report:
  release: v0.1.1
  report_date: 2026-05-11
  repository: xiongxianfei/rigorloop
  commit: abc123
  report_markdown: {md}

benchmark_suite:
  id: skill-token-runtime-v2
  previous_suite_id: skill-token-runtime-v1
  baseline_for_suite: true
  manifest: benchmarks/token-cost/manifest.yaml
  prompt_count: 10
  fixture: benchmarks/token-cost/fixtures/minimal-public-project
  runs_per_prompt: 1

benchmark_coverage:
  suite_id: skill-token-runtime-v2
  required_core_status: pass
  required_core:
    - proposal-short
  transition_carryover_status: pass
  transition_carryover_required: []
  changed_skill_benchmark_status: pass
  optional_extended:
    - architecture-review
  optional_run:
    - benchmark: architecture-review
      skill: architecture-review
      claimed_as_release_coverage: {'true' if optional_claimed else 'false'}
      required_for_release: {'true' if optional_required else 'false'}
      result_quality_status: {optional_coverage_quality_status}
  missing_required: []
  missing_optional: []

environment:
  primary_tool: codex
  codex_available: true
  codex_version: fixture
  model: fixture-model
  os: fixture-os
  runner: maintainer-local

runner:
  command: python scripts/run-token-cost-benchmarks.py --release v0.1.1 --suite benchmarks/token-cost/manifest.yaml --tool codex
  tool: codex
  suite: benchmarks/token-cost/manifest.yaml
  fixture: benchmarks/token-cost/fixtures/minimal-public-project
  skill_source: dist/adapters/codex/.agents/skills/
  output_dir: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1
  temp_policy: system-temp
  install_public_skills: true

static_skill_size:
  status: pass
  command: python scripts/measure-skill-tokens.py
  skills_measured: 1
  total_estimated_tokens: 100
  max_skill:
    path: skills/proposal/SKILL.md
    estimated_tokens: 100
  warnings: []

dynamic_runtime:
  status: pass
  tool: codex
  command_pattern: codex exec --json --ephemeral ...
  incomplete: null
  runs:{proposal_run}{optional_run}

summary:
  median_input_tokens: 100
  median_cached_input_tokens: 50
  median_output_tokens: 10
  median_reasoning_output_tokens: 5
  max_single_tool_output_estimated_tokens: 20
  full_file_read_count: 0
  broad_search_count: 0
  generated_output_read_count: 0

portability:
  status: pass
  public_skill_internal_path_leaks: 0
  generated_output_internals_in_public_skills: 0
  local_examples_in_public_skills: 0
  notes: []

comparison:
  baseline: true
  previous_release: null
  previous_report: null
  comparable: false
  deltas: null
  rationale: First skill-token-runtime-v2 report.

waiver:
  required: false
  status: none
  reason: ""
  approved_by: ""
  approval_surface: ""
  evidence: ""

release_gate:
  result: pass
  blockers: []
{warning_field}
  notes:
    - Token thresholds are warning-only for this release unless required evidence fails.
"""

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

    def assertPassesWithContext(self, text: str, context_text: str) -> None:
        report = self.write_case(text)
        context = self.write_case(context_text)
        try:
            result = run_validator(
                report,
                "--required-benchmark-context",
                str(context),
            )
        finally:
            report.unlink()
            context.unlink()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("valid token-cost report metadata", result.stdout)

    def assertFailsWithContext(self, text: str, context_text: str, expected_text: str) -> None:
        report = self.write_case(text)
        context = self.write_case(context_text)
        try:
            result = run_validator(
                report,
                "--required-benchmark-context",
                str(context),
            )
        finally:
            report.unlink()
            context.unlink()
        combined = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0, "expected validator to fail")
        self.assertIn(expected_text, combined)

    def test_lifecycle_summary_template_has_required_field_groups_and_warning_only_boundary(self) -> None:
        template = LIFECYCLE_TEMPLATE.read_text(encoding="utf-8")
        self.assertLifecycleHeadingsPresent(template)
        self.assertContainsAll(
            template,
            [
                "docs/reports/token-cost/lifecycle/<change-id>.md",
                "large workflow-governance change",
                "release change",
                "dynamic benchmark warning",
                "broad-search incident",
                "explicit maintainer request",
                "not observed",
                "not measured",
                "not applicable",
                "warning-only",
                "not a hard token gate",
                "bounded evidence",
            ],
        )
        self.assertContainsAll(template, LIFECYCLE_COST_DRIVER_TERMS)
        self.assertNoLifecycleHardGateCues(template)

    def test_m4_lifecycle_summary_has_required_shape_and_bounded_evidence_cues(self) -> None:
        summary = M4_LIFECYCLE_SUMMARY.read_text(encoding="utf-8")
        self.assertLifecycleHeadingsPresent(summary)
        self.assertContainsAll(
            summary,
            [
                "2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary",
                "large workflow-governance change",
                "docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md",
                "specs/cost-bounded-rigor-m4-lifecycle-token-cost-summary.test.md",
                "informational",
                "not measured",
                "not observed",
                "bounded evidence",
                "no hard token gate",
                "follow-up routing",
            ],
        )
        self.assertContainsAll(summary, LIFECYCLE_COST_DRIVER_TERMS)
        self.assertNoLifecycleHardGateCues(summary)

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

    def test_v2_result_quality_and_required_context_are_enforced_by_cli(self) -> None:
        context = self.v2_context_text(core=["proposal-short"])
        self.assertPassesWithContext(self.v2_report_text(), context)
        self.assertFailsWithContext(
            self.v2_report_text(proposal_quality_status="not-reviewed"),
            context,
            "dynamic_runtime.runs[0].result_quality.status: required benchmark must not be not-reviewed",
        )
        self.assertFailsWithContext(
            self.v2_report_text(include_proposal_run=False),
            context,
            "dynamic_runtime.runs: missing required benchmark proposal-short",
        )

    def test_v2_required_benchmark_context_is_supported_in_process(self) -> None:
        module = load_validator_module()
        report_path = self.write_case(self.v2_report_text())
        context_path = self.write_case(self.v2_context_text(core=["proposal-short"]))
        try:
            report = module.load_yaml(report_path)
            context = module.load_yaml(context_path)
        finally:
            report_path.unlink()
            context_path.unlink()
        errors = module.validate_token_cost_report(
            report,
            required_benchmark_context=context,
        )
        self.assertEqual(errors, [])

    def test_v2_required_benchmark_result_quality_waiver_roles_are_enforced(self) -> None:
        waiver = """
        waiver:
          status: approved
          approved_by: xiongxianfei
          approved_role: release-owner
          approval_surface: release checklist
          approved_at: "2026-05-11"
          reason: Benchmark output was inconclusive but no affected public skill changed.
          evidence: tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml"""
        context = self.v2_context_text(core=["proposal-short"])
        for role in ["release-owner", "release-manager", "repository-maintainer"]:
            with self.subTest(role=role):
                self.assertPassesWithContext(
                    self.v2_report_text(
                        proposal_quality_status="inconclusive",
                        proposal_waiver=waiver.replace("approved_role: release-owner", f"approved_role: {role}"),
                    ),
                    context,
                )
        self.assertFailsWithContext(
            self.v2_report_text(
                proposal_quality_status="inconclusive",
                proposal_waiver=waiver.replace("approved_role: release-owner", "approved_role: owner"),
            ),
            context,
            "dynamic_runtime.runs[0].result_quality.waiver.approved_role: expected one of",
        )
        self.assertFailsWithContext(
            self.v2_report_text(
                proposal_quality_status="inconclusive",
                proposal_waiver=waiver.replace("approved_by: xiongxianfei", 'approved_by: ""'),
            ),
            context,
            "dynamic_runtime.runs[0].result_quality.waiver.approved_by: expected non-empty string",
        )
        self.assertFailsWithContext(
            self.v2_report_text(proposal_quality_status="fail"),
            context,
            "dynamic_runtime.runs[0].result_quality.waiver: required for required benchmark result_quality.status fail",
        )

    def test_v2_claimed_optional_coverage_is_gated_and_unclaimed_optional_warns(self) -> None:
        context = self.v2_context_text(core=["proposal-short"])
        failed_warning = """    - severity: warning
      code: optional-benchmark-failed
      benchmark: architecture-review
      skill: architecture-review
      message: Optional benchmark failed, but it is not required for this release.
      follow_up: Review before claiming coverage."""
        inconclusive_warning = """    - severity: warning
      code: optional-benchmark-inconclusive
      benchmark: architecture-review
      skill: architecture-review
      message: Optional benchmark result quality was inconclusive.
      follow_up: Rerun or improve expected-output criteria before relying on this benchmark."""
        self.assertPassesWithContext(
            self.v2_report_text(optional_quality_status="fail", optional_warning=failed_warning),
            context,
        )
        self.assertPassesWithContext(
            self.v2_report_text(
                optional_quality_status="inconclusive",
                optional_warning=inconclusive_warning,
            ),
            context,
        )
        self.assertFailsWithContext(
            self.v2_report_text(optional_quality_status="fail", optional_claimed=True),
            context,
            "dynamic_runtime.runs[1].result_quality.waiver: required for required benchmark result_quality.status fail",
        )
        self.assertFailsWithContext(
            self.v2_report_text(optional_quality_status="inconclusive", optional_claimed=True),
            context,
            "dynamic_runtime.runs[1].result_quality.waiver: required for required benchmark result_quality.status inconclusive",
        )
        self.assertFailsWithContext(
            self.v2_report_text(optional_quality_status="not-reviewed", optional_claimed=True),
            context,
            "dynamic_runtime.runs[1].result_quality.status: required benchmark must not be not-reviewed",
        )
        self.assertFailsWithContext(
            self.v2_report_text(
                optional_claimed=True,
                include_optional_run=False,
            ),
            context,
            "dynamic_runtime.runs: missing required benchmark architecture-review",
        )
        self.assertFailsWithContext(
            self.v2_report_text(
                optional_quality_status="fail",
                optional_claimed=True,
                optional_warning=failed_warning,
            ),
            context,
            "release_gate.warnings: required benchmark architecture-review must not use optional warning code optional-benchmark-failed",
        )

    def test_v2_optional_coverage_result_quality_must_match_dynamic_run(self) -> None:
        context = self.v2_context_text(core=["proposal-short"])
        failed_warning = """    - severity: warning
      code: optional-benchmark-failed
      benchmark: architecture-review
      skill: architecture-review
      message: Optional benchmark failed, but it is not required for this release.
      follow_up: Review before claiming coverage."""
        inconclusive_warning = """    - severity: warning
      code: optional-benchmark-inconclusive
      benchmark: architecture-review
      skill: architecture-review
      message: Optional benchmark result quality was inconclusive.
      follow_up: Rerun or improve expected-output criteria before relying on this benchmark."""
        self.assertFailsWithContext(
            self.v2_report_text(
                optional_quality_status="fail",
                optional_coverage_quality_status="pass",
                optional_warning=failed_warning,
            ),
            context,
            "benchmark_coverage.optional_run[architecture-review].result_quality_status must match dynamic_runtime.runs[architecture-review].result_quality.status",
        )
        self.assertFailsWithContext(
            self.v2_report_text(
                optional_quality_status="inconclusive",
                optional_coverage_quality_status="pass",
                optional_warning=inconclusive_warning,
            ),
            context,
            "benchmark_coverage.optional_run[architecture-review].result_quality_status must match dynamic_runtime.runs[architecture-review].result_quality.status",
        )
        self.assertPassesWithContext(
            self.v2_report_text(
                optional_quality_status="fail",
                optional_coverage_quality_status="fail",
                optional_warning=failed_warning,
            ),
            context,
        )
        self.assertPassesWithContext(
            self.v2_report_text(
                optional_quality_status="inconclusive",
                optional_coverage_quality_status="inconclusive",
                optional_warning=inconclusive_warning,
            ),
            context,
        )
        self.assertFailsWithContext(
            self.v2_report_text(include_optional_run=False),
            context,
            "benchmark_coverage.optional_run[architecture-review] has no matching dynamic_runtime.runs entry",
        )

    def test_v2_changed_skill_required_context_requires_optional_benchmark(self) -> None:
        changed = "\n".join(
            [
                "    - benchmark: architecture-review",
                "      skill: architecture-review",
                "      reason: public-skill-changed",
                "      changed_surfaces:",
                "        canonical:",
                "          - skills/architecture-review/SKILL.md",
                "        generated: []",
            ]
        )
        context = self.v2_context_text(
            core=["proposal-short"],
            required_due_to_changes=changed,
        )
        self.assertPassesWithContext(
            self.v2_report_text(optional_required=True),
            context,
        )
        self.assertFailsWithContext(
            self.v2_report_text(include_optional_run=False, optional_required=True),
            context,
            "dynamic_runtime.runs: missing required benchmark architecture-review",
        )
        self.assertFailsWithContext(
            self.v2_report_text(optional_quality_status="fail", optional_required=True),
            context,
            "dynamic_runtime.runs[1].result_quality.waiver: required for required benchmark result_quality.status fail",
        )

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
            "runner.skill_source: .codex/skills/ is repository-local generated output and "
            "must not be used as a public benchmark source",
        )
        self.assertPasses(
            self.valid_text.replace(
                "skill_source: dist/adapters/codex/.agents/skills/",
                "skill_source: <temporary-public-adapter-output>/.agents/skills/",
            )
        )
        self.assertFails(
            self.valid_text.replace("release: v0.1.1", "release: v0.1.3"),
            "runner.skill_source: dist/adapters/codex/.agents/skills/ is the retired "
            "repository-tree adapter source for v0.1.3 and later",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
