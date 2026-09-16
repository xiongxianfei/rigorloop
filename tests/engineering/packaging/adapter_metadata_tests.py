"""Adapter descriptors, factual metadata, manifests and supported inventory."""

from __future__ import annotations

import sys
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging import adapter_distribution as adapter_distribution_module
from lib.packaging.adapter_distribution import ADAPTERS, POST_CUTOVER_ADAPTER_SKILLS, RETIRED_PROGRESSION_SKILLS, SUPPORTED_ADAPTERS, build_adapter_archives, collect_skill_reports, evaluate_skill, render_manifest_yaml, validate_adapter_artifact_metadata
from adapter_fixture_helpers import (copy_fixture_skills, fixture_path, write_adapter_artifact_metadata)


class AdapterMetadataTests(unittest.TestCase):
    maxDiff = None

    def test_default_adapter_version_requires_current_metadata_at_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "packages/rigorloop/package.json"
            with patch.object(adapter_distribution_module, "ROOT", root):
                with self.assertRaises(FileNotFoundError):
                    adapter_distribution_module.default_adapter_version()
                package.parent.mkdir(parents=True)
                package.write_text("malformed")
                with self.assertRaises(json.JSONDecodeError):
                    adapter_distribution_module.default_adapter_version()
                package.write_text('{"version": "9.8.7"}')
                self.assertEqual(adapter_distribution_module.default_adapter_version(), "v9.8.7")

    def test_build_adapter_parser_preserves_default_and_explicit_versions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "packages/rigorloop/package.json"
            package.parent.mkdir(parents=True)
            package.write_text('{"version": "9.8.7"}')
            with patch.object(adapter_distribution_module, "ROOT", root):
                spec = importlib.util.spec_from_file_location("build_adapter_defaults", ROOT / "scripts/build-adapters.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                parser = module.build_parser()
                self.assertEqual(parser.parse_args([]).version, "v9.8.7")
                self.assertEqual(parser.parse_args(["--version", "v3.2.1"]).version, "v3.2.1")
                self.assertIn("Default: v9.8.7.", " ".join(parser.format_help().split()))

    def test_metadata_unknown_value_profile_fails_before_metadata_reads(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for profile in ('unknown_value', 'recorded-source'):
                with self.subTest(profile=profile):
                    errors = validate_adapter_artifact_metadata('v1.0.0', root, metadata_root=root, profile=profile)
                    self.assertEqual(errors, [f'invalid release validation profile: {profile}'])

    def test_adapter_model_matches_required_paths(self) -> None:
        self.assertEqual(SUPPORTED_ADAPTERS, ("codex", "claude"))

        self.assertEqual(ADAPTERS["codex"].package_root.as_posix(), "dist/adapters/codex")
        self.assertEqual(ADAPTERS["codex"].entrypoint.as_posix(), "AGENTS.md")
        self.assertEqual(
            ADAPTERS["codex"].skill_path("route").as_posix(),
            ".agents/skills/route/SKILL.md",
        )

        self.assertEqual(ADAPTERS["claude"].package_root.as_posix(), "dist/adapters/claude")
        self.assertEqual(ADAPTERS["claude"].entrypoint.as_posix(), "CLAUDE.md")
        self.assertEqual(
            ADAPTERS["claude"].skill_path("route").as_posix(),
            ".claude/skills/route/SKILL.md",
        )

        self.assertNotIn("opencode", ADAPTERS)

    def test_adapter_artifact_metadata_validation_accepts_schema_and_optional_combined(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = write_adapter_artifact_metadata(root, output_dir).parent

            errors = validate_adapter_artifact_metadata(
                "v0.1.2",
                output_dir,
                metadata_root=metadata_root,
                release_commit="0123456789abcdef0123456789abcdef01234567",
            )

            self.assertEqual([], errors)

    def test_adapter_artifact_metadata_validation_rejects_bad_results_checksums_and_source_commit_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = write_adapter_artifact_metadata(
                root,
                output_dir,
                artifact_overrides={"codex": {"result": "fail"}},
            ).parent

            errors = validate_adapter_artifact_metadata(
                "v0.1.2",
                output_dir,
                metadata_root=metadata_root,
                release_commit="0123456789abcdef0123456789abcdef01234567",
            )

            self.assertTrue(any("artifact codex result must be pass" in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = write_adapter_artifact_metadata(
                root,
                output_dir,
                artifact_overrides={"claude": {"sha256": "0" * 64}},
            ).parent

            errors = validate_adapter_artifact_metadata(
                "v0.1.2",
                output_dir,
                metadata_root=metadata_root,
                release_commit="0123456789abcdef0123456789abcdef01234567",
            )

            self.assertTrue(any("sha256 mismatch: claude" in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = write_adapter_artifact_metadata(root, output_dir).parent

            errors = validate_adapter_artifact_metadata(
                "v0.1.2",
                output_dir,
                metadata_root=metadata_root,
                release_commit="fedcba9876543210fedcba9876543210fedcba98",
            )

            self.assertTrue(any("release.source_commit mismatch" in error for error in errors), errors)

    def test_dollar_invocation_vocabulary_matches_published_skills(self) -> None:
        published_names = {
            path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")
        }

        self.assertEqual(
            set(adapter_distribution_module.PUBLISHED_SKILL_INVOCATION_NAMES),
            published_names,
        )

    def test_post_cutover_adapter_inventory_is_explicit_and_retires_old_gates(self) -> None:
        reports = collect_skill_reports(ROOT / "skills")
        report_names = tuple(report.name for report in reports)

        self.assertEqual(report_names, tuple(sorted(POST_CUTOVER_ADAPTER_SKILLS)))
        self.assertTrue(RETIRED_PROGRESSION_SKILLS.isdisjoint(report_names))
        self.assertIn("design-review", report_names)
        self.assertIn("delivery-review", report_names)

    def test_canonical_adapter_inventory_rejects_unknown_value_before_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(
                root, ("portable-basic", "portable-with-assets")
            )
            with (
                patch.object(adapter_distribution_module, "CANONICAL_SKILLS_DIR", skills_root),
                patch.object(
                    adapter_distribution_module,
                    "PUBLISHED_SKILL_INVOCATION_NAMES",
                    ("portable-basic",),
                ),
                patch.object(
                    adapter_distribution_module,
                    "POST_CUTOVER_ADAPTER_SKILLS",
                    ("portable-basic",),
                ),
            ):
                with self.assertRaisesRegex(
                    ValueError, "undeclared canonical skills: portable-with-assets"
                ):
                    collect_skill_reports(skills_root)

    def test_manifest_render_ignores_retired_target_only_restrictions(self) -> None:
        portable = evaluate_skill(fixture_path("portable-basic"))
        partial = evaluate_skill(fixture_path("partial-portability"))

        manifest = render_manifest_yaml("0.1.0-rc.1", [partial, portable])

        self.assertEqual(
            manifest,
            "\n".join(
                [
                    "version: 0.1.0-rc.1",
                    "skills:",
                    "  partial-portability:",
                    "    portable: true",
                    "    adapters: [codex, claude]",
                    "  portable-basic:",
                    "    portable: true",
                    "    adapters: [codex, claude]",
                    "",
                ]
            ),
        )

    def test_manifest_render_quotes_yaml_sensitive_reasons(self) -> None:
        report = evaluate_skill(fixture_path("unsupported-frontmatter"))

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
