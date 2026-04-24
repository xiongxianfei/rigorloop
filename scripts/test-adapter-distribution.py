#!/usr/bin/env python3
"""Fixture-driven tests for adapter distribution helpers."""

from __future__ import annotations

import sys
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "adapters"
sys.path.insert(0, str(ROOT / "scripts"))

from adapter_distribution import (  # noqa: E402
    ADAPTERS,
    SUPPORTED_ADAPTERS,
    collect_adapter_drift,
    evaluate_skill,
    expected_adapter_files,
    render_manifest_yaml,
    sync_adapter_output,
    validate_adapter_output,
)


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
    ) -> tuple[Path, Path]:
        skills_root = self.copy_fixture_skills(root, names)
        output_root = root / "dist" / "adapters"
        sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
        return skills_root, output_root

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
                any("generated skill is not listed in manifest: claude/portable-basic" in error for error in errors)
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
                "0.1.0-rc.1",
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
        self.assertIn("validated generated adapters for version 0.1.0-rc.1", result.stdout)

    def test_ci_script_runs_adapter_checks_and_filters_generated_paths(self) -> None:
        ci_text = (ROOT / "scripts" / "ci.sh").read_text(encoding="utf-8")

        self.assertIn("python scripts/test-adapter-distribution.py", ci_text)
        self.assertIn("python scripts/build-adapters.py --version 0.1.0-rc.1 --check", ci_text)
        self.assertIn("python scripts/validate-adapters.py --version 0.1.0-rc.1", ci_text)
        self.assertIn('"$path" == dist/adapters/*', ci_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
