#!/usr/bin/env python3
"""Fixture-driven tests for adapter distribution helpers."""

from __future__ import annotations

import importlib.util
import sys
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "adapters"
TOKEN_COST_VALID_FIXTURE = (
    ROOT / "tests" / "fixtures" / "token-cost" / "reports" / "valid-final-pass" / "v0.1.1.yaml"
)
VALIDATE_RELEASE = ROOT / "scripts" / "validate-release.py"
sys.path.insert(0, str(ROOT / "scripts"))

import adapter_distribution as adapter_distribution_module  # noqa: E402
from adapter_distribution import (  # noqa: E402
    ADAPTERS,
    AdapterDriftEntry,
    OPENCODE_COMMAND_ALIASES,
    SUPPORTED_ADAPTERS,
    build_required_benchmark_context,
    collect_adapter_drift,
    collect_adapter_drift_entries,
    evaluate_skill,
    generated_adapter_skill_owner,
    expected_adapter_files,
    format_adapter_drift_normal,
    format_adapter_drift_verbose,
    parse_manifest_yaml,
    render_opencode_command_alias,
    render_manifest_yaml,
    sync_adapter_output,
    validate_adapter_output,
    validate_release_output,
)


def load_validate_release_module():
    spec = importlib.util.spec_from_file_location("validate_release_test", VALIDATE_RELEASE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AdapterDistributionTests(unittest.TestCase):
    maxDiff = None

    def fixture(self, name: str) -> Path:
        return FIXTURES / name

    def copy_fixture_skills(self, target: Path, names: tuple[str, ...]) -> Path:
        skills_root = target / "skills"
        skills_root.mkdir()
        for name in names:
            shutil.copytree(self.fixture(name), skills_root / name)
        return skills_root

    def generate_fixture_adapters(
        self,
        root: Path,
        names: tuple[str, ...] = ("portable-basic", "transformable-frontmatter"),
        version: str = "0.1.0-rc.1",
    ) -> tuple[Path, Path]:
        skills_root = self.copy_fixture_skills(root, names)
        output_root = root / "dist" / "adapters"
        sync_adapter_output(version, skills_root=skills_root, output_root=output_root)
        return skills_root, output_root

    def write_release_artifacts(
        self,
        root: Path,
        *,
        version: str = "v0.1.0-rc.1",
        release_type: str = "rc",
        manifest_version: str = "0.1.0-rc.1",
        supported_tools: tuple[str, ...] = SUPPORTED_ADAPTERS,
        smoke_result: str = "not-run",
        smoke_overrides: dict[str, dict[str, str]] | None = None,
        validation_overrides: dict[str, str] | None = None,
        notes_tools: tuple[str, ...] = SUPPORTED_ADAPTERS,
        notes_extra: str = "",
    ) -> Path:
        release_dir = root / "docs" / "releases" / version
        release_dir.mkdir(parents=True, exist_ok=True)
        smoke_overrides = smoke_overrides or {}
        validation = {
            "generated_sync": "pass",
            "release_notes_consistency": "pass",
            "placeholder_release_check": "pass",
            "security": "pass",
        }
        if version == "v0.1.1":
            validation["token_cost_report"] = "pass"
        validation.update(validation_overrides or {})

        lines = [
            f"version: {version}",
            f"release_type: {release_type}",
            f"manifest_version: {manifest_version}",
            "supported_tools:",
            *(f"  - {tool}" for tool in supported_tools),
            "adapter_paths:",
        ]
        lines.extend(f"  {tool}: dist/adapters/{tool}/" for tool in supported_tools)
        lines.append("instruction_entrypoints:")
        for tool in supported_tools:
            entrypoint = "CLAUDE.md" if tool == "claude" else "AGENTS.md"
            lines.append(f"  {tool}: dist/adapters/{tool}/{entrypoint}")
        lines.append("smoke:")
        for tool in supported_tools:
            row = {
                "result": smoke_result,
                "tool_version": "unknown",
                "evidence": '""',
                "reason": '"RC metadata prepared before full manual smoke."',
                "owner": "maintainer",
            }
            row.update(smoke_overrides.get(tool, {}))
            lines.extend(
                [
                    f"  {tool}:",
                    f"    result: {row['result']}",
                    f"    tool_version: {row['tool_version']}",
                    f"    evidence: {row['evidence']}",
                    f"    reason: {row['reason']}",
                    f"    owner: {row['owner']}",
                ]
            )
        lines.append("validation:")
        lines.extend(f"  {key}: {value}" for key, value in validation.items())
        lines.append("")
        (release_dir / "release.yaml").write_text("\n".join(lines), encoding="utf-8")

        notes_lines = [
            f"# RigorLoop {version}",
            "",
            "## Generated Adapter Packages",
            "",
            "This release candidate ships generated adapter packages under `dist/adapters/`.",
            "",
            "## Supported Tools",
            "",
            *(
                f"- `{tool}`: `dist/adapters/{tool}/`"
                for tool in notes_tools
            ),
            "",
            "## Skill Support",
            "",
            "No current non-portable skill exclusions.",
            "",
            "## Known Limitations",
            "",
            "- Manual adapter smoke is not complete for this RC metadata.",
        ]
        if notes_extra:
            notes_lines.extend(["", notes_extra])
        notes_lines.append("")
        (release_dir / "release-notes.md").write_text("\n".join(notes_lines), encoding="utf-8")
        return release_dir

    def v0_1_1_notes_extra(self) -> str:
        aliases = ", ".join(f"`{alias}`" for alias in OPENCODE_COMMAND_ALIASES)
        return "\n".join(
            [
                "## Command Alias Usage",
                "",
                f"OpenCode command aliases are generated for {aliases}.",
                "Claude Code remains skill-native and uses native skill slash commands such as `/proposal`.",
                "",
                "OpenCode one-shot example:",
                "",
                '```text',
                'opencode run --command proposal "Draft a proposal for the requested change."',
                '```',
                "",
                "## Transition Release Boundaries",
                "",
                "`skills/` is the canonical authored skill source.",
                "`dist/adapters/` remains the public adapter install path for `v0.1.1`.",
                "The release gate does not require `.codex/skills/` generation as release evidence.",
                "No downloadable adapter archives are introduced in this release.",
            ]
        )

    def v0_1_1_smoke_overrides(self) -> dict[str, dict[str, str]]:
        smoke = {
            tool: {
                "result": "pass",
                "tool_version": f'"{tool} 1.0.0"',
                "evidence": '"manual smoke passed"',
                "reason": '""',
                "owner": "maintainer",
            }
            for tool in SUPPORTED_ADAPTERS
        }
        smoke["opencode"]["evidence"] = (
            '"opencode run --command proposal loaded the proposal skill and '
            'repeated ARGUMENT_MARKER_M3_SMOKE."'
        )
        return smoke

    def write_minimal_v2_token_report(
        self,
        token_cost_root: Path,
        *,
        run_ids: tuple[str, ...] = ("proposal-short",),
    ) -> None:
        token_cost_root.mkdir(parents=True, exist_ok=True)
        markdown = token_cost_root / "v0.1.1.md"
        metadata = token_cost_root / "v0.1.1.yaml"
        markdown.write_text(
            "# Token-Friendliness Report\n\nMetadata: v0.1.1.yaml\n",
            encoding="utf-8",
        )
        run_blocks: list[str] = []
        for run_id in run_ids:
            prompt = f"benchmarks/token-cost/prompts/{run_id}.md"
            fixture = "benchmarks/token-cost/fixtures/minimal-public-project"
            if run_id == "architecture-review":
                fixture = "benchmarks/token-cost/fixtures/minimal-public-project-architecture-review"
            run_blocks.append(
                f"""
    - id: {run_id}
      prompt: {prompt}
      fixture: {fixture}
      result: pass
      evidence:
        raw_jsonl_tracked: true
        jsonl: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.jsonl
        analysis: tests/fixtures/token-cost/reports/valid-final-pass/runs/v0.1.1/proposal-short-run1.analysis.yaml
        sanitized_summary: ""
        raw_omission_reason: ""
      result_quality:
        status: pass
        reviewed_by: maintainer
        review_surface: {markdown}
        reviewed_at: "2026-05-11"
        criteria:
          - id: output_shape
            expectation: Output followed the requested shape.
            result: pass
            notes: ""
        notes: Manual review accepted this benchmark.
        blockers: []
"""
            )
        metadata.write_text(
            f"""schema_version: 1

report:
  release: v0.1.1
  report_date: 2026-05-11
  repository: xiongxianfei/rigorloop
  commit: abc123
  report_markdown: {markdown}

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
  optional_run: []
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
  runs:{''.join(run_blocks)}

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
  warnings: []
""",
            encoding="utf-8",
        )

    def test_adapter_model_matches_required_paths(self) -> None:
        self.assertEqual(SUPPORTED_ADAPTERS, ("codex", "claude", "opencode"))

        self.assertEqual(ADAPTERS["codex"].package_root.as_posix(), "dist/adapters/codex")
        self.assertEqual(ADAPTERS["codex"].entrypoint.as_posix(), "AGENTS.md")
        self.assertEqual(
            ADAPTERS["codex"].skill_path("workflow").as_posix(),
            ".agents/skills/workflow/SKILL.md",
        )

        self.assertEqual(ADAPTERS["claude"].package_root.as_posix(), "dist/adapters/claude")
        self.assertEqual(ADAPTERS["claude"].entrypoint.as_posix(), "CLAUDE.md")
        self.assertEqual(
            ADAPTERS["claude"].skill_path("workflow").as_posix(),
            ".claude/skills/workflow/SKILL.md",
        )

        self.assertEqual(ADAPTERS["opencode"].package_root.as_posix(), "dist/adapters/opencode")
        self.assertEqual(ADAPTERS["opencode"].entrypoint.as_posix(), "AGENTS.md")
        self.assertEqual(
            ADAPTERS["opencode"].skill_path("workflow").as_posix(),
            ".opencode/skills/workflow/SKILL.md",
        )

    def test_portable_skill_includes_all_adapters(self) -> None:
        report = evaluate_skill(self.fixture("portable-basic"))

        self.assertTrue(report.portable)
        self.assertEqual(report.name, "portable-basic")
        self.assertEqual(report.included_adapters, ("codex", "claude", "opencode"))
        self.assertEqual(report.reason, "")

    def test_invalid_name_description_and_body_fail_all_adapters(self) -> None:
        invalid_name = evaluate_skill(self.fixture("invalid-name"))
        invalid_description = evaluate_skill(self.fixture("invalid-description"))
        invalid_body = evaluate_skill(self.fixture("invalid-body"))

        self.assertFalse(invalid_name.portable)
        self.assertEqual(invalid_name.included_adapters, ())
        self.assertIn("portable skill name", invalid_name.reason)

        self.assertFalse(invalid_description.portable)
        self.assertEqual(invalid_description.included_adapters, ())
        self.assertIn("description", invalid_description.reason)

        self.assertFalse(invalid_body.portable)
        self.assertEqual(invalid_body.included_adapters, ())
        self.assertIn("top-level # title", invalid_body.reason)
        self.assertIn("Expected output", invalid_body.reason)

    def test_argument_hint_is_explicit_transform_not_exclusion(self) -> None:
        report = evaluate_skill(self.fixture("transformable-frontmatter"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude", "opencode"))
        self.assertEqual(report.adapter_decision("claude").transforms, ("drop frontmatter: argument-hint",))
        self.assertEqual(
            report.adapter_decision("opencode").transforms,
            ("drop frontmatter: argument-hint",),
        )

    def test_codex_only_assumptions_exclude_non_codex_adapters(self) -> None:
        cases = {
            "unsupported-frontmatter": "unsupported frontmatter",
            "codex-invocation": "Codex-only invocation syntax",
            "agents-openai": "agents/openai.yaml",
            "codex-install-only": ".codex/skills",
            "codex-tool-assumption": "Codex-only tool, UI, approval, or runtime assumption",
            "codex-dollar-skill": "Codex-specific $skill invocation",
        }

        for fixture, expected_reason in cases.items():
            with self.subTest(fixture=fixture):
                report = evaluate_skill(self.fixture(fixture))
                self.assertFalse(report.portable)
                self.assertEqual(report.included_adapters, ("codex",))
                self.assertTrue(report.adapter_decision("codex").included)
                self.assertFalse(report.adapter_decision("claude").included)
                self.assertFalse(report.adapter_decision("opencode").included)
                self.assertIn(expected_reason, report.reason)

    def test_generic_artifact_paths_remain_portable(self) -> None:
        report = evaluate_skill(self.fixture("generic-artifact-paths"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude", "opencode"))

    def test_codex_skills_reference_with_adapter_alternatives_remains_portable(self) -> None:
        report = evaluate_skill(self.fixture("codex-install-with-alternatives"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude", "opencode"))
        self.assertEqual(report.reason, "")

    def test_partial_portability_records_exact_adapter_decision(self) -> None:
        report = evaluate_skill(self.fixture("partial-portability"))

        self.assertFalse(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        self.assertTrue(report.adapter_decision("codex").included)
        self.assertTrue(report.adapter_decision("claude").included)
        self.assertFalse(report.adapter_decision("opencode").included)
        self.assertEqual(
            report.adapter_decision("opencode").reasons,
            ("Not compatible with opencode.",),
        )

    def test_manifest_render_records_partial_portability(self) -> None:
        portable = evaluate_skill(self.fixture("portable-basic"))
        partial = evaluate_skill(self.fixture("partial-portability"))

        manifest = render_manifest_yaml("0.1.0-rc.1", [partial, portable])

        self.assertEqual(
            manifest,
            "\n".join(
                [
                    "version: 0.1.0-rc.1",
                    "skills:",
                    "  partial-portability:",
                    "    portable: false",
                    "    adapters: [codex, claude]",
                    '    reason: "Not compatible with opencode."',
                    "  portable-basic:",
                    "    portable: true",
                    "    adapters: [codex, claude, opencode]",
                    "",
                ]
            ),
        )

    def test_manifest_render_quotes_yaml_sensitive_reasons(self) -> None:
        report = evaluate_skill(self.fixture("unsupported-frontmatter"))

        manifest = render_manifest_yaml("0.1.0-rc.1", [report])

        self.assertEqual(
            manifest,
            "\n".join(
                [
                    "version: 0.1.0-rc.1",
                    "skills:",
                    "  unsupported-frontmatter:",
                    "    portable: false",
                    "    adapters: [codex]",
                    '    reason: "Uses unsupported frontmatter: codex-only-field."',
                    "",
                ]
            ),
        )

    def test_adapter_generation_creates_independent_packages_and_thin_entrypoints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(
                root,
                (
                    "portable-basic",
                    "transformable-frontmatter",
                    "partial-portability",
                    "unsupported-frontmatter",
                ),
            )
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)

            for adapter, config in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    package_root = output_root / adapter
                    entrypoint = package_root / Path(config.entrypoint.as_posix())
                    skill_root = package_root / Path(config.skill_root.as_posix())
                    copied_project = root / f"copied-{adapter}"

                    shutil.copytree(package_root, copied_project)

                    self.assertTrue(entrypoint.is_file())
                    self.assertTrue(skill_root.is_dir())
                    self.assertTrue((copied_project / Path(config.entrypoint.as_posix())).is_file())
                    self.assertTrue((copied_project / Path(config.skill_root.as_posix())).is_dir())

                    entrypoint_text = entrypoint.read_text(encoding="utf-8")
                    self.assertIn("generated adapter output", entrypoint_text)
                    self.assertIn("canonical", entrypoint_text)
                    self.assertNotIn("# Portable Basic", entrypoint_text)

            self.assertFalse(
                (
                    output_root
                    / "opencode"
                    / ".opencode"
                    / "skills"
                    / "partial-portability"
                    / "SKILL.md"
                ).exists()
            )

    def test_adapter_generation_drops_transformed_frontmatter_for_non_codex(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("transformable-frontmatter",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)

            codex_skill = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            ).read_text(encoding="utf-8")
            claude_skill = (
                output_root
                / "claude"
                / ".claude"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            ).read_text(encoding="utf-8")
            opencode_skill = (
                output_root
                / "opencode"
                / ".opencode"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            ).read_text(encoding="utf-8")

            self.assertIn("argument-hint:", codex_skill)
            self.assertNotIn("argument-hint:", claude_skill)
            self.assertNotIn("argument-hint:", opencode_skill)

    def test_opencode_generation_creates_curated_command_aliases_for_0_1_1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"

            sync_adapter_output("0.1.1", output_root=output_root)

            command_root = output_root / "opencode" / ".opencode" / "commands"
            aliases = {path.stem for path in command_root.glob("*.md")}
            self.assertEqual(aliases, set(OPENCODE_COMMAND_ALIASES))
            self.assertFalse((command_root / "workflow.md").exists())
            self.assertFalse((command_root / "verify.md").exists())
            self.assertFalse((output_root / "claude" / ".claude" / "commands").exists())

            for alias in OPENCODE_COMMAND_ALIASES:
                with self.subTest(alias=alias):
                    alias_path = command_root / f"{alias}.md"
                    skill_path = (
                        output_root
                        / "opencode"
                        / ".opencode"
                        / "skills"
                        / alias
                        / "SKILL.md"
                    )
                    self.assertTrue(skill_path.is_file())
                    alias_text = alias_path.read_text(encoding="utf-8")
                    self.assertEqual(alias_text, render_opencode_command_alias(alias))
                    self.assertIn("description:", alias_text)
                    self.assertIn("$ARGUMENTS", alias_text)

    def test_opencode_alias_generation_rejects_missing_curated_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            with self.assertRaisesRegex(ValueError, "opencode command alias proposal"):
                sync_adapter_output("0.1.1", skills_root=skills_root, output_root=output_root)

            self.assertFalse(output_root.exists())

    def test_manifest_records_exact_opencode_command_alias_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"

            sync_adapter_output("0.1.1", output_root=output_root)
            manifest = parse_manifest_yaml(
                (output_root / "manifest.yaml").read_text(encoding="utf-8"),
                output_root / "manifest.yaml",
            )

            opencode_aliases = manifest.command_aliases["opencode"]
            self.assertEqual(opencode_aliases.count, len(OPENCODE_COMMAND_ALIASES))
            self.assertEqual(tuple(opencode_aliases.aliases), OPENCODE_COMMAND_ALIASES)
            for alias in OPENCODE_COMMAND_ALIASES:
                self.assertEqual(
                    opencode_aliases.aliases[alias],
                    f"dist/adapters/opencode/.opencode/commands/{alias}.md",
                )

    def test_adapter_generation_drift_check_detects_stale_and_unexpected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            self.assertEqual(
                collect_adapter_drift(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                ),
                [],
            )

            stale_file = output_root / "codex" / "AGENTS.md"
            stale_file.write_text(
                stale_file.read_text(encoding="utf-8") + "\nstale\n",
                encoding="utf-8",
            )
            stale_drift = collect_adapter_drift(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )
            self.assertTrue(any("stale generated adapter file" in entry for entry in stale_drift))

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            unexpected_file = output_root / "codex" / "unexpected.txt"
            unexpected_file.write_text("unexpected\n", encoding="utf-8")
            unexpected_drift = collect_adapter_drift(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )
            self.assertTrue(
                any("unexpected generated adapter file" in entry for entry in unexpected_drift)
            )

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            self.assertFalse(unexpected_file.exists())
            self.assertEqual(
                collect_adapter_drift(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                ),
                [],
            )

    def test_adapter_drift_entries_classify_generated_output_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            sorted(output_root.rglob("SKILL.md"))[0].unlink()
            stale_file = output_root / "codex" / "AGENTS.md"
            stale_file.write_text(stale_file.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
            unexpected_file = output_root / "codex" / "unexpected.txt"
            unexpected_file.write_text("unexpected\n", encoding="utf-8")

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )

            categories = {entry.category for entry in entries}
            self.assertIn("missing", categories)
            self.assertIn("stale", categories)
            self.assertIn("unexpected", categories)
            self.assertTrue(
                all(entry.category in {"missing", "stale", "unexpected"} for entry in entries)
            )
            self.assertTrue(all(entry.path for entry in entries))
            self.assertTrue(all(entry.detail for entry in entries))

    def test_manifest_first_inspection_precedes_filesystem_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"
            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            missing_skill = sorted(output_root.rglob("SKILL.md"))[0]
            missing_skill.unlink()
            stale_file = output_root / "codex" / "AGENTS.md"
            stale_file.write_text(stale_file.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
            unexpected_file = output_root / "codex" / "unexpected.txt"
            unexpected_file.write_text("unexpected\n", encoding="utf-8")

            call_order: list[str] = []
            real_manifest_read = adapter_distribution_module._inspect_generated_adapter_manifest
            real_file_collect = adapter_distribution_module._collect_generated_files

            def manifest_read(output_root: Path):
                call_order.append("manifest")
                return real_manifest_read(output_root)

            def file_collect(output_root: Path):
                call_order.append("filesystem")
                return real_file_collect(output_root)

            with patch.object(
                adapter_distribution_module,
                "_inspect_generated_adapter_manifest",
                side_effect=manifest_read,
            ), patch.object(
                adapter_distribution_module,
                "_collect_generated_files",
                side_effect=file_collect,
            ):
                entries = collect_adapter_drift_entries(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                )

            self.assertEqual(call_order[:2], ["manifest", "filesystem"])
            categories = {entry.category for entry in entries}
            self.assertIn("missing", categories)
            self.assertIn("stale", categories)
            self.assertIn("unexpected", categories)
            self.assertNotIn("manifest-error", categories)

    def test_manifest_errors_are_structured_and_displayed_completely(self) -> None:
        cases = (
            (
                "missing",
                lambda manifest_path: manifest_path.unlink(),
                "generated adapter manifest is missing",
            ),
            (
                "malformed",
                lambda manifest_path: manifest_path.write_text("version: [\n", encoding="utf-8"),
                "malformed",
            ),
            (
                "version",
                lambda manifest_path: manifest_path.write_text(
                    manifest_path.read_text(encoding="utf-8").replace(
                        "version: 0.1.0-rc.1",
                        "version: 0.0.0",
                        1,
                    ),
                    encoding="utf-8",
                ),
                "version mismatch",
            ),
            (
                "contract",
                lambda manifest_path: manifest_path.write_text(
                    manifest_path.read_text(encoding="utf-8").replace(
                        "adapters: [codex, claude, opencode]",
                        "adapters: [codex]",
                        1,
                    ),
                    encoding="utf-8",
                ),
                "adapter list mismatch",
            ),
        )

        for _name, mutate_manifest, expected_detail in cases:
            with self.subTest(_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                skills_root = self.copy_fixture_skills(root, ("portable-basic",))
                output_root = root / "dist" / "adapters"
                sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
                missing_skill = sorted(output_root.rglob("SKILL.md"))[0]
                missing_skill.unlink()
                manifest_path = output_root / "manifest.yaml"
                mutate_manifest(manifest_path)

                entries = collect_adapter_drift_entries(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                )
                manifest_entries = [
                    entry for entry in entries if entry.category == "manifest-error"
                ]
                normal_output = format_adapter_drift_normal(
                    entries,
                    version="0.1.0-rc.1",
                    output_root=output_root,
                )
                verbose_output = format_adapter_drift_verbose(
                    entries,
                    version="0.1.0-rc.1",
                    output_root=output_root,
                )

                self.assertTrue(manifest_entries)
                self.assertTrue(all(entry.path == manifest_path for entry in manifest_entries))
                self.assertTrue(any(expected_detail in entry.detail for entry in manifest_entries))
                self.assertIn("missing", {entry.category for entry in entries})
                self.assertIn("manifest-error", normal_output)
                self.assertIn(str(manifest_path), normal_output)
                self.assertIn("fix or regenerate the generated adapter manifest", normal_output)
                self.assertIn(expected_detail, verbose_output)
                self.assertIn(str(manifest_path), verbose_output)

    def test_canonical_source_failures_are_structured_adapter_drift_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "skills"
            broken_skill = skills_root / "broken-skill"
            broken_skill.mkdir(parents=True)
            (broken_skill / "SKILL.md").write_text("---\nname: broken-skill\n", encoding="utf-8")
            output_root = root / "dist" / "adapters"

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )

            self.assertTrue(entries)
            self.assertTrue(all(entry.category == "canonical-source-error" for entry in entries))
            self.assertTrue(any("canonical skill validation failed" in entry.detail for entry in entries))

    def test_adapter_drift_collection_does_not_write_persistent_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            before_files = {path.relative_to(root) for path in root.rglob("*") if path.is_file()}

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )

            after_files = {path.relative_to(root) for path in root.rglob("*") if path.is_file()}
            self.assertEqual(entries, ())
            self.assertEqual(after_files, before_files)
            self.assertFalse(any(".cache" in path.parts for path in after_files))

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
            skills_root = self.copy_fixture_skills(root, ("portable-basic",))
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
            skills_root = self.copy_fixture_skills(root, ("portable-basic",))
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

    def test_adapter_drift_output_size_evidence_records_before_after_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            clean_output = format_adapter_drift_normal(
                [],
                version="0.1.0-rc.1",
                output_root=output_root,
            )
            clean_evidence = {
                "legacy_lines": 1,
                "shaped_lines": len(clean_output.splitlines()),
            }

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
            drift_output = format_adapter_drift_normal(
                entries,
                version="0.1.0-rc.1",
                output_root=output_root,
            )
            drift_evidence = {
                "legacy_lines": len(entries),
                "shaped_lines": len(drift_output.splitlines()),
            }

            self.assertGreaterEqual(clean_evidence["shaped_lines"], clean_evidence["legacy_lines"])
            self.assertGreater(drift_evidence["legacy_lines"], drift_evidence["shaped_lines"])
            self.assertLessEqual(drift_evidence["shaped_lines"], 40)

    def test_build_adapters_cli_supports_verbose_check_only(self) -> None:
        verbose_check = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build-adapters.py"),
                "--version",
                "0.1.1",
                "--check",
                "--verbose",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertEqual(
            verbose_check.returncode,
            0,
            msg=f"stdout:\n{verbose_check.stdout}\nstderr:\n{verbose_check.stderr}",
        )
        self.assertIn("adapters.drift: ok", verbose_check.stdout)

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

    def test_opencode_command_alias_validation_rejects_missing_extra_and_dangling_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"

            sync_adapter_output("0.1.1", output_root=output_root)
            proposal_alias = output_root / "opencode" / ".opencode" / "commands" / "proposal.md"
            proposal_alias.unlink()
            errors = validate_adapter_output("0.1.1", output_root=output_root)
            self.assertTrue(
                any("opencode command alias missing: proposal" in error for error in errors)
            )

            sync_adapter_output("0.1.1", output_root=output_root)
            verify_alias = output_root / "opencode" / ".opencode" / "commands" / "verify.md"
            verify_alias.write_text(render_opencode_command_alias("verify"), encoding="utf-8")
            errors = validate_adapter_output("0.1.1", output_root=output_root)
            self.assertTrue(
                any("unexpected opencode command alias: verify" in error for error in errors)
            )

            sync_adapter_output("0.1.1", output_root=output_root)
            shutil.rmtree(output_root / "opencode" / ".opencode" / "skills" / "proposal")
            errors = validate_adapter_output("0.1.1", output_root=output_root)
            self.assertTrue(
                any("opencode command alias maps to missing skill: proposal" in error for error in errors)
            )

    def test_opencode_command_alias_manifest_validation_rejects_mismatches(self) -> None:
        cases = (
            (
                "proposal: dist/adapters/opencode/.opencode/commands/proposal.md",
                "proposal: .opencode/commands/proposal.md",
                "path must be under dist/adapters/opencode/.opencode/commands",
            ),
            (
                "proposal: dist/adapters/opencode/.opencode/commands/proposal.md",
                "proposal: dist/adapters/opencode/.opencode/commands/spec.md",
                "filename stem mismatch: proposal",
            ),
            (
                "command_aliases:\n",
                (
                    "command_aliases:\n"
                    "  claude:\n"
                    "    count: 1\n"
                    "    aliases:\n"
                    "      proposal: dist/adapters/claude/.claude/commands/proposal.md\n"
                ),
                "unsupported command alias tool: claude",
            ),
            (
                "    count: 10\n    aliases:\n",
                (
                    "    count: 11\n"
                    "    aliases:\n"
                    "      verify: dist/adapters/opencode/.opencode/commands/verify.md\n"
                ),
                "unexpected opencode command alias in manifest: verify",
            ),
        )

        for old, new, expected_error in cases:
            with self.subTest(expected_error=expected_error):
                with tempfile.TemporaryDirectory() as tmp:
                    output_root = Path(tmp) / "dist" / "adapters"
                    sync_adapter_output("0.1.1", output_root=output_root)
                    manifest_path = output_root / "manifest.yaml"
                    manifest_path.write_text(
                        manifest_path.read_text(encoding="utf-8").replace(old, new, 1),
                        encoding="utf-8",
                    )

                    errors = validate_adapter_output("0.1.1", output_root=output_root)

                    self.assertTrue(any(expected_error in error for error in errors), errors)

    def test_opencode_command_alias_validation_rejects_unsafe_or_stale_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"
            sync_adapter_output("0.1.1", output_root=output_root)
            alias_path = output_root / "opencode" / ".opencode" / "commands" / "proposal.md"
            alias_path.write_text(
                (
                    "---\n"
                    "description: Use the RigorLoop proposal skill.\n"
                    "---\n\n"
                    "Load @README.md\n"
                    "!pwd\n"
                    "model: unsafe\n"
                    "permissions: elevated\n"
                ),
                encoding="utf-8",
            )

            errors = validate_adapter_output("0.1.1", output_root=output_root)

            self.assertTrue(any("file-reference interpolation" in error for error in errors))
            self.assertTrue(any("shell-output interpolation" in error for error in errors))
            self.assertTrue(any("model override" in error for error in errors))
            self.assertTrue(any("permission policy change" in error for error in errors))
            self.assertTrue(any("body mismatch" in error for error in errors))

    def test_generated_manifest_matches_version_and_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(
                root,
                (
                    "portable-basic",
                    "partial-portability",
                    "unsupported-frontmatter",
                ),
            )
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            rc_manifest = (output_root / "manifest.yaml").read_text(encoding="utf-8")

            self.assertIn("version: 0.1.0-rc.1", rc_manifest)
            self.assertIn("  portable-basic:", rc_manifest)
            self.assertIn("    adapters: [codex, claude, opencode]", rc_manifest)
            self.assertIn("  partial-portability:", rc_manifest)
            self.assertIn("    adapters: [codex, claude]", rc_manifest)
            self.assertIn("  unsupported-frontmatter:", rc_manifest)
            self.assertIn("    adapters: [codex]", rc_manifest)
            self.assertTrue(
                (
                    output_root
                    / "claude"
                    / ".claude"
                    / "skills"
                    / "portable-basic"
                    / "SKILL.md"
                ).is_file()
            )
            self.assertFalse(
                (
                    output_root
                    / "claude"
                    / ".claude"
                    / "skills"
                    / "unsupported-frontmatter"
                    / "SKILL.md"
                ).exists()
            )

            stable_files = expected_adapter_files(
                "0.1.0",
                skills_root=skills_root,
            )
            self.assertIn("version: 0.1.0", stable_files[Path("manifest.yaml")])

    def test_validate_adapter_output_accepts_generated_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertEqual(errors, [])

    def test_validate_adapter_output_rejects_missing_adapter_directory_and_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            shutil.rmtree(output_root / "claude")

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("missing adapter directory: claude" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            (output_root / "opencode" / "AGENTS.md").unlink()

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("missing instruction entrypoint: opencode" in error for error in errors))

    def test_adapter_generation_rejects_malformed_canonical_skill_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "skills"
            broken_skill = skills_root / "broken-skill"
            broken_skill.mkdir(parents=True)
            (broken_skill / "SKILL.md").write_text(
                "---\nname: broken-skill\n",
                encoding="utf-8",
            )
            output_root = root / "dist" / "adapters"

            with self.assertRaisesRegex(ValueError, "canonical skill validation failed"):
                sync_adapter_output(
                    "0.1.0-rc.1",
                    skills_root=skills_root,
                    output_root=output_root,
                )

            self.assertFalse(output_root.exists())

    def test_validate_adapter_output_rejects_missing_or_malformed_canonical_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing_skills_root = root / "missing-skills"
            output_root = root / "dist" / "adapters"

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=missing_skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("canonical skills root does not exist" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root, ("portable-basic",))
            broken_skill = skills_root / "broken-skill"
            broken_skill.mkdir()
            (broken_skill / "SKILL.md").write_text(
                "---\nname: broken-skill\n",
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("canonical skill validation failed" in error for error in errors))

    def test_validate_adapter_output_rejects_manifest_file_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root, ("portable-basic",))
            manifest_path = output_root / "manifest.yaml"
            manifest_path.write_text(
                manifest_path.read_text(encoding="utf-8").replace(
                    "adapters: [codex, claude, opencode]",
                    "adapters: [codex]",
                    1,
                ),
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("adapter list mismatch: portable-basic" in error for error in errors))
            self.assertTrue(
                any(
                    "generated skill is not listed in manifest: claude/portable-basic" in error
                    for error in errors
                )
            )

    def test_validate_adapter_output_rejects_unsupported_non_codex_metadata_leak(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root, ("transformable-frontmatter",))
            codex_skill = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            )
            claude_skill = (
                output_root
                / "claude"
                / ".claude"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            )
            claude_skill.write_text(codex_skill.read_text(encoding="utf-8"), encoding="utf-8")

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(
                any(
                    "unsupported metadata in claude/transformable-frontmatter: argument-hint" in error
                    for error in errors
                )
            )

    def test_validate_adapter_output_rejects_security_violations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root, ("portable-basic",))
            entrypoint = output_root / "codex" / "AGENTS.md"
            entrypoint.write_text(
                entrypoint.read_text(encoding="utf-8")
                + "\n-----BEGIN PRIVATE KEY-----\n/home/alice/.ssh/id_rsa\n--dangerously-skip-permissions\n",
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("private key delimiter" in error for error in errors))
            self.assertTrue(any("machine-local absolute path" in error for error in errors))
            self.assertTrue(any("permission bypass" in error for error in errors))

    def test_validate_adapters_cli_accepts_repository_output(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate-adapters.py"),
                "--version",
                "0.1.1",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("validated generated adapters for version 0.1.1", result.stdout)

    def test_ci_script_runs_adapter_checks_and_filters_generated_paths(self) -> None:
        ci_text = (ROOT / "scripts" / "ci.sh").read_text(encoding="utf-8")

        self.assertIn("python scripts/test-adapter-distribution.py", ci_text)
        self.assertIn("python scripts/build-adapters.py --version 0.1.1 --check", ci_text)
        self.assertIn("python scripts/validate-adapters.py --version 0.1.1", ci_text)
        self.assertIn('"$path" == dist/adapters/*', ci_text)

    def test_release_metadata_validation_accepts_rc_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(root)

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertEqual(errors, [])

    def test_release_metadata_validation_rejects_manifest_and_tool_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(root, manifest_version="0.1.0")

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("manifest_version" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(root, notes_tools=("codex", "claude"))

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("release notes supported tools mismatch" in error for error in errors))

    def test_release_metadata_validation_enforces_rc_smoke_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                smoke_overrides={
                    "codex": {
                        "result": "fail",
                        "tool_version": "codex 1.2.3",
                        "evidence": '"smoke failed"',
                        "reason": '"tool did not discover skills"',
                        "owner": "maintainer",
                    }
                },
            )

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("known smoke failure blocks rc" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(root, smoke_overrides={"claude": {"owner": '""'}})

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("smoke.claude.owner" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            release_dir = self.write_release_artifacts(root)
            release_yaml = release_dir / "release.yaml"
            release_yaml.write_text(
                release_yaml.read_text(encoding="utf-8").replace("    owner: maintainer\n", "", 1),
                encoding="utf-8",
            )

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("smoke.codex: missing required field owner" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                smoke_overrides={
                    "opencode": {
                        "result": "blocked",
                        "reason": '"maintainer did not run this yet"',
                    }
                },
            )

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("smoke.opencode.reason" in error for error in errors))

    def test_release_metadata_validation_enforces_final_smoke_strictness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root, version="0.1.0")
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                version="v0.1.0",
                release_type="final",
                manifest_version="0.1.0",
                smoke_result="not-run",
            )

            errors = validate_release_output(
                "v0.1.0",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("final release requires smoke pass" in error for error in errors))

    def test_v0_1_1_release_metadata_requires_command_alias_smoke_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            smoke = {
                tool: {
                    "result": "pass",
                    "tool_version": f'"{tool} 1.0.0"',
                    "evidence": '"manual smoke passed"',
                    "reason": '""',
                    "owner": "maintainer",
                }
                for tool in SUPPORTED_ADAPTERS
            }
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=smoke,
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                release_root=release_root,
                changed_paths=(),
            )

            self.assertTrue(
                any("smoke.opencode.evidence: v0.1.1 requires command alias behavior evidence" in error for error in errors),
                errors,
            )

            smoke["opencode"]["evidence"] = (
                '"opencode run --command proposal loaded the proposal skill and '
                'repeated ARGUMENT_MARKER_M3_SMOKE."'
            )
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=smoke,
                notes_extra=self.v0_1_1_notes_extra(),
            )

            self.assertEqual(
                validate_release_output(
                    "v0.1.1",
                    release_root=release_root,
                    changed_paths=(),
                ),
                [],
            )

    def test_v0_1_1_release_validation_requires_token_cost_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                release_root=release_root,
                token_cost_report_root=root / "docs" / "reports" / "token-cost" / "releases",
                changed_paths=(),
            )

            self.assertTrue(
                any("missing token-cost report metadata" in error for error in errors),
                errors,
            )

    def test_v0_1_1_release_validation_blocks_invalid_token_cost_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            token_cost_root = root / "docs" / "reports" / "token-cost" / "releases"
            token_cost_root.mkdir(parents=True)
            invalid_metadata = TOKEN_COST_VALID_FIXTURE.read_text(encoding="utf-8").replace(
                "  report_markdown: tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.md\n",
                "",
                1,
            )
            (token_cost_root / "v0.1.1.yaml").write_text(invalid_metadata, encoding="utf-8")
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                release_root=release_root,
                token_cost_report_root=token_cost_root,
            )

            self.assertTrue(
                any("token-cost report validation failed" in error for error in errors),
                errors,
            )
            self.assertTrue(
                any("report.report_markdown" in error for error in errors),
                errors,
            )

    def test_required_benchmark_context_requires_changed_skill_benchmark(self) -> None:
        context = build_required_benchmark_context(
            "v0.1.1",
            release_stage="final",
            commit="abc123",
            changed_paths=("skills/architecture-review/SKILL.md",),
        )

        required = context["required_benchmarks"]
        self.assertEqual(
            required["core"],
            [
                "workflow-route",
                "proposal-short",
                "plan-handoff",
                "implement-handoff",
                "code-review-small",
                "explain-change-summary",
                "verify-final-pack",
                "pr-handoff",
            ],
        )
        self.assertEqual(
            required["transition_carryover"],
            ["architecture-no-impact", "learn-no-durable-lesson"],
        )
        self.assertEqual(
            required["required_due_to_changes"],
            [
                {
                    "benchmark": "architecture-review",
                    "skill": "architecture-review",
                    "reason": "public-skill-changed",
                    "changed_surfaces": {
                        "canonical": ["skills/architecture-review/SKILL.md"],
                        "generated": [],
                    },
                }
            ],
        )

    def test_required_benchmark_context_traces_generated_adapter_paths(self) -> None:
        context = build_required_benchmark_context(
            "v0.1.1",
            release_stage="final",
            commit="abc123",
            changed_paths=(
                "skills/architecture-review/SKILL.md",
                "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md",
                "dist/adapters/claude/.claude/skills/architecture-review/SKILL.md",
                "dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md",
            ),
        )

        changed = context["required_benchmarks"]["required_due_to_changes"][0]
        self.assertEqual(changed["skill"], "architecture-review")
        self.assertEqual(
            changed["changed_surfaces"]["generated"],
            [
                "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md",
                "dist/adapters/claude/.claude/skills/architecture-review/SKILL.md",
                "dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md",
            ],
        )
        self.assertEqual(
            generated_adapter_skill_owner(
                "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md"
            ),
            "architecture-review",
        )

    def test_generated_only_adapter_change_traces_to_required_dynamic_benchmark(self) -> None:
        context = build_required_benchmark_context(
            "v0.1.1",
            release_stage="final",
            commit="abc123",
            changed_paths=(
                "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md",
            ),
        )

        self.assertEqual(
            context["required_benchmarks"]["required_due_to_changes"],
            [
                {
                    "benchmark": "architecture-review",
                    "skill": "architecture-review",
                    "reason": "generated-public-skill-changed",
                    "changed_surfaces": {
                        "canonical": [],
                        "generated": [
                            "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md"
                        ],
                    },
                }
            ],
        )
        self.assertEqual(
            context["required_benchmarks"]["generated_trace"],
            [
                {
                    "generated_path": "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md",
                    "owning_skill": "skills/architecture-review/SKILL.md",
                    "benchmark": "architecture-review",
                    "canonical_changed": False,
                    "action": "adapter-drift-or-regeneration-evidence",
                }
            ],
        )

    def test_changed_public_skill_without_benchmark_records_warning_follow_up(self) -> None:
        context = build_required_benchmark_context(
            "v0.1.1",
            release_stage="final",
            commit="abc123",
            changed_paths=("skills/spec-review/SKILL.md",),
        )

        self.assertEqual(context["required_benchmarks"]["required_due_to_changes"], [])
        self.assertEqual(
            context["required_benchmarks"]["missing_benchmarks"],
            [
                {
                    "skill": "spec-review",
                    "reason": "public-skill-changed",
                    "follow_up": "add token-cost benchmark fixture for spec-review",
                }
            ],
        )

    def test_release_validation_passes_required_context_to_token_cost_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            token_cost_root = root / "docs" / "reports" / "token-cost" / "releases"
            self.write_minimal_v2_token_report(token_cost_root)
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                release_root=release_root,
                token_cost_report_root=token_cost_root,
                changed_paths=("skills/architecture-review/SKILL.md",),
            )

            self.assertTrue(
                any("token-cost report validation failed" in error for error in errors),
                errors,
            )
            self.assertTrue(
                any("dynamic_runtime.runs: missing required benchmark architecture-review" in error for error in errors),
                errors,
            )

    def test_v2_final_release_validation_requires_changed_surface_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            token_cost_root = root / "docs" / "reports" / "token-cost" / "releases"
            self.write_minimal_v2_token_report(token_cost_root)
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                release_root=release_root,
                token_cost_report_root=token_cost_root,
            )

            self.assertTrue(
                any("release validation requires changed-surface input" in error for error in errors),
                errors,
            )

    def test_validate_release_cli_passes_changed_surface_inputs(self) -> None:
        module = load_validate_release_module()
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
            handle.write(
                "\n".join(
                    [
                        "# comment",
                        "skills/architecture-review/SKILL.md",
                        "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md",
                        "skills/architecture-review/SKILL.md",
                        "",
                    ]
                )
            )
            handle.flush()
            captured: dict[str, object] = {}

            def fake_validate_release_output(version: str, *, changed_paths=()):
                captured["version"] = version
                captured["changed_paths"] = changed_paths
                return [
                    "token-cost report validation failed: dynamic_runtime.runs: "
                    "missing required benchmark architecture-review"
                ]

            with patch.object(module, "validate_release_output", fake_validate_release_output):
                result = module.main(
                    [
                        "--version",
                        "v0.1.1",
                        "--changed-path",
                        "dist/adapters/claude/.claude/skills/architecture-review/SKILL.md",
                        "--changed-paths-file",
                        handle.name,
                    ]
                )

        self.assertEqual(result, 1)
        self.assertEqual(captured["version"], "v0.1.1")
        self.assertEqual(
            captured["changed_paths"],
            (
                "dist/adapters/claude/.claude/skills/architecture-review/SKILL.md",
                "skills/architecture-review/SKILL.md",
                "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md",
            ),
        )

    def test_generated_adapter_changed_path_requires_missing_benchmark_through_release_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            token_cost_root = root / "docs" / "reports" / "token-cost" / "releases"
            self.write_minimal_v2_token_report(token_cost_root)
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                release_root=release_root,
                token_cost_report_root=token_cost_root,
                changed_paths=(
                    "dist/adapters/codex/.agents/skills/architecture-review/SKILL.md",
                ),
            )

            self.assertTrue(
                any("dynamic_runtime.runs: missing required benchmark architecture-review" in error for error in errors),
                errors,
            )

    def test_changed_skill_with_complete_v2_metadata_passes_release_validation(self) -> None:
        required_runs = (
            "workflow-route",
            "proposal-short",
            "plan-handoff",
            "implement-handoff",
            "code-review-small",
            "explain-change-summary",
            "verify-final-pack",
            "pr-handoff",
            "architecture-no-impact",
            "learn-no-durable-lesson",
            "architecture-review",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            token_cost_root = root / "docs" / "reports" / "token-cost" / "releases"
            self.write_minimal_v2_token_report(token_cost_root, run_ids=required_runs)
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                release_root=release_root,
                token_cost_report_root=token_cost_root,
                changed_paths=("skills/architecture-review/SKILL.md",),
            )

            self.assertEqual(errors, [])

    def test_historical_release_validation_does_not_require_token_cost_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root, version="0.1.0")
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                version="v0.1.0",
                release_type="final",
                manifest_version="0.1.0",
                smoke_overrides={
                    tool: {
                        "result": "pass",
                        "tool_version": f"{tool} 1.0.0",
                        "evidence": '"manual smoke passed"',
                        "reason": '""',
                        "owner": "maintainer",
                    }
                    for tool in SUPPORTED_ADAPTERS
                },
            )

            errors = validate_release_output(
                "v0.1.0",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
                token_cost_report_root=root / "missing-token-cost-reports",
            )

            self.assertEqual(errors, [])

    def test_release_metadata_validation_rejects_release_security_violations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(root, notes_extra="/home/alice/.ssh/id_rsa")

            errors = validate_release_output(
                "v0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertTrue(any("machine-local absolute path" in error for error in errors))

    def test_release_metadata_validation_accepts_stable_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(root, version="0.1.0")
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                version="v0.1.0",
                release_type="final",
                manifest_version="0.1.0",
                smoke_overrides={
                    tool: {
                        "result": "pass",
                        "tool_version": f"{tool} 1.0.0",
                        "evidence": '"manual smoke passed"',
                        "reason": '""',
                        "owner": "maintainer",
                    }
                    for tool in SUPPORTED_ADAPTERS
                },
            )

            errors = validate_release_output(
                "v0.1.0",
                skills_root=skills_root,
                output_root=output_root,
                release_root=release_root,
            )

            self.assertEqual(errors, [])

    def test_validate_release_cli_accepts_repository_v0_1_1_artifacts(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as changed_paths:
            changed_paths.flush()
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-release.py"),
                    "--version",
                    "v0.1.1",
                    "--changed-paths-file",
                    changed_paths.name,
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("validated release metadata for v0.1.1", result.stdout)

    def test_v0_1_1_release_validation_accepts_ignored_untracked_codex_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            token_cost_root = root / "docs" / "reports" / "token-cost" / "releases"
            self.write_minimal_v2_token_report(token_cost_root)
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                skills_root=ROOT / "skills",
                output_root=ROOT / "dist" / "adapters",
                release_root=release_root,
                token_cost_report_root=ROOT / "docs" / "reports" / "token-cost" / "releases",
                changed_paths=(),
                tracked_files=(),
                codex_skills_ignored=True,
            )

            self.assertEqual(errors, [])

    def test_v0_1_1_release_validation_rejects_tracked_codex_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                skills_root=ROOT / "skills",
                output_root=ROOT / "dist" / "adapters",
                release_root=release_root,
                token_cost_report_root=ROOT / "docs" / "reports" / "token-cost" / "releases",
                changed_paths=(),
                tracked_files=(".codex/skills/proposal/SKILL.md",),
                codex_skills_ignored=True,
            )

            self.assertTrue(any(".codex/skills/ must be untracked" in error for error in errors))

    def test_v0_1_1_release_validation_rejects_unignored_codex_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "docs" / "releases"
            self.write_release_artifacts(
                root,
                version="v0.1.1",
                release_type="final",
                manifest_version="0.1.1",
                smoke_overrides=self.v0_1_1_smoke_overrides(),
                notes_extra=self.v0_1_1_notes_extra(),
            )

            errors = validate_release_output(
                "v0.1.1",
                skills_root=ROOT / "skills",
                output_root=ROOT / "dist" / "adapters",
                release_root=release_root,
                token_cost_report_root=ROOT / "docs" / "reports" / "token-cost" / "releases",
                changed_paths=(),
                tracked_files=(),
                codex_skills_ignored=False,
            )

            self.assertTrue(any(".codex/skills/ must be ignored" in error for error in errors))

    def test_release_verify_script_invokes_required_repository_checks(self) -> None:
        script = ROOT / "scripts" / "release-verify.sh"
        script_text = script.read_text(encoding="utf-8")
        forbidden = (
            "Replace this script with repository-specific release checks",
            "TODO: release checks",
            "placeholder release check",
        )
        for marker in forbidden:
            self.assertNotIn(marker, script_text)

        result = subprocess.run(
            ["bash", str(script), "v0.1.0"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={"RELEASE_VERIFY_DRY_RUN": "1"},
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        required_commands = (
            "python scripts/validate-skills.py",
            "python scripts/test-skill-validator.py",
            "python scripts/build-skills.py --check",
            "python scripts/test-adapter-distribution.py",
            "python scripts/build-adapters.py --version 0.1.0 --check",
            "python scripts/validate-adapters.py --version 0.1.0",
            "python scripts/validate-release.py --version v0.1.0",
        )
        for command in required_commands:
            self.assertIn(command, result.stdout)
        self.assertIn("security", result.stdout.lower())

    def test_release_verify_script_supports_v0_1_1(self) -> None:
        result = subprocess.run(
            ["bash", str(ROOT / "scripts" / "release-verify.sh"), "v0.1.1"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={"RELEASE_VERIFY_DRY_RUN": "1"},
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("python scripts/build-adapters.py --version 0.1.1 --check", result.stdout)
        self.assertIn("python scripts/validate-adapters.py --version 0.1.1", result.stdout)
        self.assertIn("python scripts/validate-release.py --version v0.1.1", result.stdout)
        self.assertNotIn("python scripts/build-skills.py --check", result.stdout)
        self.assertIn(
            "python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml",
            result.stdout,
        )

    def test_release_verify_script_accepts_github_ref_name(self) -> None:
        result = subprocess.run(
            ["bash", str(ROOT / "scripts" / "release-verify.sh")],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={"GITHUB_REF_NAME": "v0.1.0-rc.1", "RELEASE_VERIFY_DRY_RUN": "1"},
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("Release verification for v0.1.0-rc.1", result.stdout)

    def test_release_workflow_uses_tracked_release_notes(self) -> None:
        workflow_text = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn('bash scripts/release-verify.sh "$GITHUB_REF_NAME"', workflow_text)
        self.assertIn('docs/releases/${tag}/release-notes.md', workflow_text)
        self.assertIn("--notes-file", workflow_text)
        self.assertNotIn("--generate-notes", workflow_text)

    def test_claude_entrypoint_documents_native_skill_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"
            sync_adapter_output("0.1.1", output_root=output_root)

            claude_root = output_root / "claude"
            text = (claude_root / "CLAUDE.md").read_text(encoding="utf-8")

            self.assertFalse((claude_root / ".claude" / "commands").exists())
            self.assertIn("Using RigorLoop skills", text)
            self.assertIn(".claude/skills/", text)
            self.assertIn("native Claude Code slash commands", text)
            for command in ("/proposal", "/spec", "/implement", "/code-review", "/pr"):
                self.assertIn(command, text)
            self.assertNotIn("claude -p", text)
            self.assertNotIn("opencode run --command", text)

    def test_opencode_entrypoint_documents_skills_and_thin_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"
            sync_adapter_output("0.1.1", output_root=output_root)

            text = (output_root / "opencode" / "AGENTS.md").read_text(encoding="utf-8")

            self.assertIn("Using RigorLoop skills", text)
            self.assertIn(".opencode/skills/", text)
            self.assertIn(".opencode/commands/", text)
            self.assertIn("thin command aliases", text)
            for command in ("/proposal", "/spec", "/implement", "/code-review", "/pr"):
                self.assertIn(command, text)
            self.assertNotIn("/workflow", text)
            self.assertNotIn("/verify", text)
            self.assertIn("opencode run --command proposal", text)
            self.assertIn("Do not use Codex `$skill` syntax", text)

    def test_readme_distinguishes_claude_and_opencode_invocation_forms(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("Claude Code uses native skill slash commands", text)
        self.assertIn("OpenCode uses generated command aliases", text)
        self.assertIn(".opencode/skills/", text)
        self.assertIn(".opencode/commands/", text)
        for command in ("/proposal", "/spec", "/implement", "/code-review", "/pr"):
            self.assertIn(command, text)
        self.assertIn("opencode run --command proposal", text)
        self.assertNotIn("claude -p", text)
        self.assertIn("Do not use Codex `$skill` syntax", text)

    def test_public_docs_describe_adapter_support_and_generated_boundaries(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "docs/workflows.md": (ROOT / "docs" / "workflows.md").read_text(encoding="utf-8"),
            "AGENTS.md": (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            "release-notes.md": (
                ROOT / "docs" / "releases" / "v0.1.0" / "release-notes.md"
            ).read_text(encoding="utf-8"),
        }
        combined = "\n".join(docs.values()).lower()

        for term in ("codex", "claude", "opencode", "dist/adapters", ".codex/skills"):
            self.assertIn(term, combined)
        self.assertIn("ordinary contributors do not need all supported tools", combined)
        self.assertIn("external tool contracts", combined)
        self.assertIn("before changing release claims", combined)
        self.assertIn("skills/", combined)
        self.assertNotIn("marketplace package", combined)
        self.assertNotIn("package-manager distribution", combined)

    def test_public_adapter_compatibility_surface_remains_tracked(self) -> None:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "dist/adapters/*/.*/skills/*/SKILL.md",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        tracked = result.stdout.splitlines()

        for adapter in SUPPORTED_ADAPTERS:
            with self.subTest(adapter=adapter):
                self.assertTrue(
                    any(path.startswith(f"dist/adapters/{adapter}/") for path in tracked),
                    f"expected tracked generated public skill copies for {adapter}",
                )

    def test_public_adapter_readme_documents_metadata_and_install_transition(self) -> None:
        text = (ROOT / "dist" / "adapters" / "README.md").read_text(encoding="utf-8")

        self.assertIn("canonical `skills/`", text)
        self.assertIn("Do not edit generated adapter skill files by hand", text)
        self.assertIn("`dist/adapters/manifest.yaml`", text)
        self.assertIn("support matrix", text)
        self.assertIn("repository-tree install", text)
        self.assertIn("For `v0.1.1`", text)
        self.assertIn("public adapter install path", text)
        self.assertIn("No downloadable adapter archives are required for `v0.1.1`", text)
        self.assertIn("`docs/reports/adapter-artifacts/releases/<version>.yaml`", text)
        self.assertIn("release assets", text)
        self.assertIn("`.codex/skills/`", text)
        self.assertIn("ignored local runtime install directory", text)
        self.assertIn("not a public adapter install source", text)

    def test_v0_1_1_release_notes_document_transition_contract(self) -> None:
        text = (ROOT / "docs" / "releases" / "v0.1.1" / "release-notes.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("`skills/` is the canonical authored skill source", text)
        self.assertIn("`dist/adapters/` remains the public adapter install path", text)
        self.assertIn("does not require `.codex/skills/` generation as release evidence", text)
        self.assertIn("No downloadable adapter archives are introduced in this release", text)
        self.assertNotIn("checks canonical skills, generated `.codex/skills/`", text)

    def test_contributor_docs_install_local_codex_from_public_adapter(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "docs/workflows.md": (ROOT / "docs" / "workflows.md").read_text(encoding="utf-8"),
            "AGENTS.md": (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            "CONSTITUTION.md": (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8"),
        }

        for path, text in docs.items():
            with self.subTest(path=path):
                self.assertIn("public Codex adapter output", text)
                self.assertIn("`.codex/skills/`", text)
                self.assertIn("untracked", text)
                self.assertNotIn(
                    "Regenerate it with `python scripts/build-skills.py` when needed.",
                    text,
                )

    def test_adapter_manifest_remains_metadata_only(self) -> None:
        manifest_path = ROOT / "dist" / "adapters" / "manifest.yaml"
        manifest = manifest_path.read_text(encoding="utf-8")

        self.assertIn("version:", manifest)
        self.assertIn("skills:", manifest)
        self.assertIn("command_aliases:", manifest)
        self.assertNotIn("# ", manifest)
        self.assertNotIn("## ", manifest)
        self.assertNotIn("description:", manifest)
        self.assertNotIn("argument-hint:", manifest)
        self.assertNotIn("When to use", manifest)
        self.assertNotIn("How to use", manifest)

    def test_generated_adapter_archives_are_not_committed(self) -> None:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        archives = [
            path
            for path in result.stdout.splitlines()
            if path.endswith(".zip") or path.endswith(".tar.gz")
        ]

        self.assertEqual([], [path for path in archives if "rigorloop-adapter-" in path])


if __name__ == "__main__":
    unittest.main(verbosity=2)
