#!/usr/bin/env python3
"""Fixture-driven tests for adapter distribution helpers."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import sys
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "adapters"

VALIDATE_RELEASE = ROOT / "scripts" / "validate-release.py"
sys.path.insert(0, str(ROOT / "scripts"))

import adapter_distribution as adapter_distribution_module  # noqa: E402
from adapter_distribution import (  # noqa: E402
    ADAPTERS,
    AdapterDriftEntry,
    OPENCODE_COMMAND_ALIASES,
    POST_CUTOVER_ADAPTER_SKILLS,
    STAGED_V3_ADAPTER_SKILLS,
    STAGED_V3_OPENCODE_COMMAND_ALIASES,
    RETIRED_PROGRESSION_SKILLS,
    SUPPORTED_ADAPTERS,
    adapter_archive_name,
    build_adapter_archives,
    build_staged_v3_adapter_archives,
    collect_adapter_drift,
    collect_adapter_drift_entries,
    collect_skill_reports,
    evaluate_skill,
    expected_adapter_files,
    format_adapter_drift_normal,
    format_adapter_drift_verbose,
    parse_manifest_yaml,
    render_manifest_yaml,
    sync_adapter_output,
    validate_adapter_archives,
    validate_staged_v3_adapter_archives,
    validate_adapter_artifact_metadata,
    validate_adapter_output,
    validate_clean_install_smoke,
)
from boundary_first_reference import (  # noqa: E402
    GOVERNED_SKILLS,
    inventory_digest,
    load_resource_manifest,
    raw_sha256,
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
    def test_metadata_unknown_value_profile_fails_before_metadata_reads(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for profile in ('unknown_value', 'recorded-source'):
                with self.subTest(profile=profile):
                    errors = validate_adapter_artifact_metadata('v1.0.0', root, metadata_root=root, profile=profile)
                    self.assertEqual(errors, [f'invalid release validation profile: {profile}'])

    maxDiff = None

    def fixture(self, name: str) -> Path:
        return FIXTURES / name

    def test_optional_discovery_packages_have_archive_and_clean_install_parity(self) -> None:
        version = "v0.4.0"
        expected_resources = {
            "explore": {
                "assets/exploration-skeleton.md",
                "references/discovery-support.md",
                "references/option-discovery-methods.md",
                "references/high-impact-decision-method.md",
            },
            "research": {
                "assets/research-skeleton.md",
                "references/discovery-support.md",
                "references/source-and-repository-method.md",
                "references/experiment-and-confidence-method.md",
            },
        }
        shared_policy = (ROOT / "templates/shared/discovery-support.md").read_bytes()
        forbidden = (
            b"skills/explore/SKILL.md",
            b"skills/research/SKILL.md",
            b"templates/shared",
            b"dist/adapters",
        )

        with tempfile.TemporaryDirectory(prefix="discovery-adapters-") as temp_dir:
            output = Path(temp_dir)
            archives = build_adapter_archives(version, output)
            self.assertEqual(validate_adapter_archives(version, output), [])
            self.assertEqual(
                validate_clean_install_smoke(
                    version,
                    output,
                    skill_names=("explore", "research"),
                ),
                [],
            )

            self.assertEqual(len(archives), len(SUPPORTED_ADAPTERS))
            for archive_path in archives:
                adapter_name = archive_path.name.removeprefix("rigorloop-adapter-").removesuffix(
                    f"-{version}.zip"
                )
                config = ADAPTERS[adapter_name]
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    for skill_name, resources in expected_resources.items():
                        prefix = (config.skill_root / skill_name).as_posix()
                        expected_entries = {
                            f"{prefix}/SKILL.md",
                            *(f"{prefix}/{resource}" for resource in resources),
                        }
                        with self.subTest(adapter=adapter_name, skill=skill_name):
                            self.assertTrue(expected_entries <= names)
                            self.assertEqual(
                                archive.read(f"{prefix}/references/discovery-support.md"),
                                shared_policy,
                            )
                            package_bytes = b"\n".join(
                                archive.read(name)
                                for name in sorted(expected_entries)
                            )
                            self.assertFalse(any(item in package_bytes for item in forbidden))
                            expected_path = (
                                b"docs/explorations/YYYY-MM-DD-slug.md"
                                if skill_name == "explore"
                                else b"docs/research/YYYY-MM-DD-slug.md"
                            )
                            self.assertIn(expected_path, package_bytes)

    def test_targeted_profiles_match_canonical_in_every_supported_archive(self) -> None:
        names = ("proposal", "proposal-review", "design", "design-review", "plan", "delivery-review", "implement", "code-review", "route", "verify", "bugfix", "ci-maintenance", "pr", "research", "explore", "learn")
        with tempfile.TemporaryDirectory(prefix="targeted-archives-") as temporary:
            output = Path(temporary)
            build_adapter_archives("v0.5.1", output)
            self.assertEqual(validate_adapter_archives("v0.5.1", output), [])
            for adapter in SUPPORTED_ADAPTERS:
                with zipfile.ZipFile(output / adapter_archive_name(adapter, "v0.5.1")) as archive:
                    for name in names:
                        relative = {"design": "references/governed-design-authoring.md", "proposal": "references/governed-proposal-authoring.md", "proposal-review": "references/proposal-review-recording-and-settlement.md"}.get(name, "SKILL.md")
                        canonical = (ROOT / "skills" / name / relative).read_text()
                        member = ADAPTERS[adapter].skill_path(name).parent / relative
                        body = archive.read(member.as_posix()).decode()
                        if relative == "SKILL.md":
                            canonical = canonical.split("## Explicit recording\n", 1)[1].split("\n## ", 1)[0]
                            body = body.split("## Explicit recording\n", 1)[1].split("\n## ", 1)[0]
                        if name == "design":
                            for resource in ("references/architecture-view-examples.md", "assets/design-skeleton.md"):
                                expected = (ROOT / "skills" / name / resource).read_bytes()
                                actual = archive.read((ADAPTERS[adapter].skill_path(name).parent / resource).as_posix())
                                self.assertEqual(actual, expected)
                        self.assertEqual(body, canonical)
                        self.assertIn("subject inspect", canonical)
                        self.assertNotIn("record-store check|record", canonical)

    def test_current_candidate_metadata_matches_generated_route_only_archives(self) -> None:
        version = "v0.5.1"
        with tempfile.TemporaryDirectory(prefix="route-candidate-") as temp_dir:
            output = Path(temp_dir)
            archives = build_adapter_archives(version, output)
            generated = adapter_distribution_module._local_release_candidate_metadata(version, output)

            # Current canonical archives have fresh identities. Historical bundled
            # release metadata remains immutable; packed current metadata is proved
            # by the actual candidate integration test.
            self.assertEqual({row['adapter'] for row in generated['artifacts']}, {'codex', 'claude'})
            self.assertEqual(validate_adapter_archives(version, output), [])
            for artifact in generated['artifacts']:
                archive_path = output / artifact['archive']
                self.assertEqual(artifact['sha256'], hashlib.sha256(archive_path.read_bytes()).hexdigest())
                self.assertEqual(artifact['size_bytes'], archive_path.stat().st_size)
                root = artifact['install_root'] + '/'
                with zipfile.ZipFile(archive_path) as archive:
                    names = [name for name in archive.namelist() if name.startswith(root) and not name.endswith('/')]
                self.assertEqual(artifact['file_count'], len(names))
                self.assertEqual(artifact['skill_names'], sorted({name[len(root):].split('/')[0] for name in names}))
            for archive_path in archives:
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    pr_entry = next(name for name in names if name.endswith("/pr/SKILL.md"))
                    verify_entry = next(
                        name for name in names
                        if name.endswith("/verify/references/successful-explanation.md")
                    )
                    pr_body = archive.read(pr_entry).decode("utf-8")
                    verify_explanation = archive.read(verify_entry).decode("utf-8")
                self.assertTrue(any("/route/SKILL.md" in name for name in names))
                self.assertFalse(any("/workflow/" in name for name in names))
                self.assertIn("evidence suffix: `none`, `evidence-only`, `invalidating`", pr_body)
                self.assertIn("any commit count or direct-parent topology", pr_body)
                self.assertNotIn("exactly one direct-child verify-owned evidence commit", pr_body)
                self.assertIn(
                    "Keep substantive success, durable save and current reliance distinct",
                    verify_explanation,
                )

    def test_staged_v3_archives_omit_explain_change_and_package_complete_verify_resources(self) -> None:
        self.assertNotIn("explain-change", STAGED_V3_ADAPTER_SKILLS)
        self.assertNotIn("explain-change", STAGED_V3_OPENCODE_COMMAND_ALIASES)
        with tempfile.TemporaryDirectory(prefix="staged-v3-adapters-") as temp_dir:
            output = Path(temp_dir)
            archives = build_staged_v3_adapter_archives("v0.1.6", output)
            self.assertEqual(validate_staged_v3_adapter_archives("v0.1.6", output), [])
            required = {
                "final-impact-analysis.md",
                "evidence-applicability.md",
                "successful-explanation.md",
                "verify-report-skeleton.md",
            }
            for archive_path in archives:
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    verify_entry = next(name for name in names if name.endswith("/verify/SKILL.md"))
                    verify_body = archive.read(verify_entry).decode("utf-8")
                self.assertFalse(any("/explain-change/" in name for name in names))
                self.assertTrue(
                    all(any(name.endswith(f"/verify/{'assets' if item.endswith('skeleton.md') else 'references'}/{item}") for name in names) for item in required)
                )
                for forbidden in (
                    "after `explain-change`",
                    "explain-change artifact",
                    "current explanation",
                    "rationale to `explain-change`",
                ):
                    self.assertNotIn(forbidden, verify_body)
                self.assertIn(
                    "final explanation only after successful final readiness",
                    verify_body,
                )

    def test_staged_v3_archive_validation_rejects_mixed_explain_change_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory(prefix="staged-v3-mixed-") as temp_dir:
            output = Path(temp_dir)
            archives = build_staged_v3_adapter_archives("v0.1.6", output)
            target = archives[0]
            with zipfile.ZipFile(target, "a") as archive:
                archive.writestr(".agents/skills/explain-change/SKILL.md", "retired")
            errors = validate_staged_v3_adapter_archives("v0.1.6", output)
            self.assertTrue(any("unexpected entries" in error and "explain-change" in error for error in errors))

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


    def write_adapter_artifact_metadata(
        self,
        root: Path,
        release_output_dir: Path,
        *,
        version: str = "v0.1.2",
        source_commit: str = "0123456789abcdef0123456789abcdef01234567",
        artifact_overrides: dict[str, dict[str, str]] | None = None,
        combined_required: bool = False,
        validation_result: str = "pass",
        historical: bool = False,
    ) -> Path:
        metadata_root = root / "docs" / "reports" / "adapter-artifacts" / "releases"
        metadata_root.mkdir(parents=True, exist_ok=True)
        artifact_overrides = artifact_overrides or {}
        lines = [
            "schema_version: 1",
            "",
            "release:",
            f"  version: {version}",
            f"  source_commit: {source_commit}",
            '  date: "2026-05-13"',
            "",
            "generator:",
            f'  command: "python scripts/build-adapters.py --version {version} --output-dir <release-output-dir>"',
            '  source_skills: "skills/"',
            '  manifest: "dist/adapters/manifest.yaml"',
            "",
            "artifacts:",
        ]
        adapters = adapter_distribution_module.HISTORICAL_ADAPTERS if historical else ADAPTERS
        for adapter in adapters:
            archive = f"rigorloop-adapter-{adapter}-{version}.zip"
            archive_path = release_output_dir / archive
            sha256 = hashlib.sha256(archive_path.read_bytes()).hexdigest()
            row = {
                "adapter": adapter,
                "archive": archive,
                "sha256": sha256,
                "install_root": adapters[adapter].skill_root.as_posix().rstrip("/") + "/",
                "result": "pass",
            }
            row.update(artifact_overrides.get(adapter, {}))
            lines.extend(
                [
                    f"  - adapter: {row['adapter']}",
                    f"    archive: {row['archive']}",
                    f"    sha256: {row['sha256']}",
                    f"    install_root: {row['install_root']}",
                    f"    result: {row['result']}",
                ]
            )
        lines.extend(
            [
                "",
                "combined_artifact:",
                f"  required: {'true' if combined_required else 'false'}",
                f"  archive: rigorloop-adapters-{version}.tar.gz",
                '  sha256: ""',
                "  included_adapters:",
                *[f"    - {name}" for name in adapters],
                "",
                "validation:",
                f'  command: "python scripts/validate-adapters.py --root <release-output-dir> --version {version}"',
                f"  result: {validation_result}",
                '  validated_at: "2026-05-13"',
                "",
            ]
        )
        metadata_path = metadata_root / f"{version}.yaml"
        metadata_path.write_text("\n".join(lines), encoding="utf-8")
        return metadata_path


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

    def test_build_adapter_archives_creates_required_release_archives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_fixture_skills(root, ("portable-basic", "transformable-frontmatter"))
            output_dir = root / "release-output"

            archives = build_adapter_archives(
                "v0.1.2",
                output_dir,
                skills_root=root / "skills",
            )

            self.assertEqual(
                [archive.name for archive in archives],
                [
                    "rigorloop-adapter-codex-v0.1.2.zip",
                    "rigorloop-adapter-claude-v0.1.2.zip",
                ],
            )
            for archive in archives:
                self.assertEqual(archive.parent, output_dir)
                self.assertTrue(archive.is_file())

            self.assertFalse((output_dir / "dist").exists())
            self.assertEqual([], validate_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills"))

    def test_adapter_archives_install_under_target_project_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")

            expected = {
                "codex": ("AGENTS.md", ".agents/skills/portable-basic/SKILL.md"),
                "claude": ("CLAUDE.md", ".claude/skills/portable-basic/SKILL.md"),
            }
            for adapter, required_entries in expected.items():
                archive_path = output_dir / adapter_archive_name(adapter, "v0.1.2")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                for entry in required_entries:
                    self.assertIn(entry, names)
                self.assertFalse(
                    any(name.startswith(f"{adapter}/") or name.startswith("dist/") for name in names)
                )

    def test_distribution_archives_have_independent_complete_resource_inventory(self) -> None:
        # Independent filesystem oracle: do not use the producer's inventory helper.
        canonical = {path.relative_to(ROOT / "skills").as_posix(): path.read_bytes()
                     for path in (ROOT / "skills").rglob("*") if path.is_file()}
        with tempfile.TemporaryDirectory() as tmp:
            archives = build_adapter_archives("v1.0.0", Path(tmp))
            self.assertEqual(len(archives), 2)
            for target, archive_path in zip(("codex", "claude"), archives):
                prefix = {"codex": ".agents/skills/", "claude": ".claude/skills/"}[target]
                with zipfile.ZipFile(archive_path) as archive:
                    actual = {name[len(prefix):]: archive.read(name) for name in archive.namelist() if name.startswith(prefix)}
                self.assertEqual(set(actual), set(canonical), target)
                for name, expected in canonical.items():
                    if target == "codex" or not name.endswith("/SKILL.md"):
                        self.assertEqual(actual[name], expected, f"{target}/{name}")
                    else:
                        # Only declared frontmatter transformations are permitted;
                        # existing metadata tests check that projection separately.
                        self.assertEqual(actual[name].split(b"---", 2)[2], expected.split(b"---", 2)[2], name)

    def test_distribution_generated_skill_structure_is_validated_independently(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills, output = self.generate_fixture_adapters(root, ("portable-basic",))
            for target in ("codex", "claude"):
                skill = output / target / ADAPTERS[target].skill_root / "portable-basic/SKILL.md"
                original = skill.read_bytes()
                skill.write_text("# Missing frontmatter\n")
                errors = validate_adapter_output("0.1.0-rc.1", skills_root=skills, output_root=output)
                self.assertTrue(any("file must begin with YAML frontmatter" in error and str(skill) in error for error in errors), errors)
                skill.write_bytes(original)

    def test_distribution_generation_rejects_source_and_active_output_roots(self) -> None:
        for operation in ("archives", "tree", "staged"):
            for destination in ("skills", "skills/nested", ".codex/skills", ".agents/skills", ".claude/skills", ".opencode/skills", "alias"):
                with self.subTest(operation=operation, destination=destination), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    skills = self.copy_fixture_skills(root, ("portable-with-assets",))
                    if destination == "alias":
                        (root / "alias").symlink_to(skills, target_is_directory=True)
                    before = {path.relative_to(skills): path.read_bytes() for path in skills.rglob("*") if path.is_file()}
                    with self.assertRaisesRegex(ValueError, "unsafe output"):
                        if operation == "archives":
                            build_adapter_archives("v1.0.0", root / destination, skills_root=skills)
                        elif operation == "staged":
                            build_staged_v3_adapter_archives("v1.0.0", root / destination, skills_root=skills)
                        else:
                            sync_adapter_output("v1.0.0", skills_root=skills, output_root=root / destination)
                    self.assertEqual(before, {path.relative_to(skills): path.read_bytes() for path in skills.rglob("*") if path.is_file()})
                    if destination.startswith("."):
                        self.assertFalse((root / destination).exists())

    def test_distribution_generation_preserves_runtime_under_output_parent_and_symlinks(self) -> None:
        for operation in ("tree", "archives", "staged"):
            for hazard in ("parent", "ancestor", "nested-link", "archive-link", "hard-link", "special-file"):
                with self.subTest(operation=operation, hazard=hazard), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    skills = self.copy_fixture_skills(root, ("portable-basic",))
                    runtime = root / "project/.codex/skills/portable-basic/SKILL.md"
                    runtime.parent.mkdir(parents=True)
                    runtime.write_bytes(b"user runtime bytes\n")
                    output = root / "output"
                    if hazard == "parent":
                        output = root / "project/.codex"
                    elif hazard == "ancestor":
                        output = root / "project"
                    elif hazard == "nested-link":
                        (output / "codex").mkdir(parents=True)
                        (output / "codex/.agents").symlink_to(root / "project/.codex", target_is_directory=True)
                    elif hazard == "archive-link":
                        output.mkdir()
                        (output / adapter_archive_name("codex", "v1.0.0")).symlink_to(runtime)
                    elif hazard == "special-file":
                        output.mkdir()
                        os.mkfifo(output / adapter_archive_name("codex", "v1.0.0"))
                    else:
                        target = (output / "codex/.agents/skills/portable-basic/SKILL.md" if operation == "tree"
                                  else output / adapter_archive_name("codex", "v1.0.0"))
                        target.parent.mkdir(parents=True)
                        os.link(runtime, target)
                    before = runtime.read_bytes()
                    with self.assertRaisesRegex(ValueError, "unsafe output"):
                        if operation == "tree":
                            sync_adapter_output("v1.0.0", skills_root=skills, output_root=output)
                        elif operation == "archives":
                            build_adapter_archives("v1.0.0", output, skills_root=skills)
                        else:
                            build_staged_v3_adapter_archives("v1.0.0", output, skills_root=skills)
                    self.assertEqual(runtime.read_bytes(), before)
                    self.assertFalse((output / "claude").exists())

    def test_adapter_archives_include_packaged_skill_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills")

            expected = {
                "codex": ".agents/skills/portable-with-assets/assets/template.md",
                "claude": ".claude/skills/portable-with-assets/assets/template.md",
            }
            for adapter, asset_entry in expected.items():
                archive_path = output_dir / adapter_archive_name(adapter, "v0.1.5")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    self.assertIn(asset_entry, names)
                    self.assertEqual(
                        archive.read(asset_entry).decode("utf-8"),
                        (root / "skills" / "portable-with-assets" / "assets" / "template.md").read_text(
                            encoding="utf-8"
                        ),
                    )

            self.assertEqual([], validate_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills"))

    def test_adapter_archives_include_route_resources_without_retired_guide_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            build_adapter_archives("v0.1.3", output_dir, skills_root=ROOT / "skills")

            packaged_adapters: list[str] = []
            expected_text = (ROOT / "skills" / "route" / "references" / "governed-lifecycle-routing.md").read_text(encoding="utf-8")
            for adapter in SUPPORTED_ADAPTERS:
                config = ADAPTERS[adapter]
                skill_entry = config.skill_path("route").as_posix()
                resource_entry = (config.skill_root / "route" / "references" / "governed-lifecycle-routing.md").as_posix()
                archive_path = output_dir / adapter_archive_name(adapter, "v0.1.3")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    if skill_entry not in names:
                        continue
                    packaged_adapters.append(adapter)
                    self.assertIn(resource_entry, names)
                    self.assertEqual(archive.read(resource_entry).decode("utf-8"), expected_text)
                    self.assertNotIn((config.skill_root / "route" / "assets" / "workflows-skeleton.md").as_posix(), names)
                    self.assertNotIn((config.skill_root / "route" / "references" / "workflow-guide-authoring.md").as_posix(), names)

            self.assertTrue(packaged_adapters)
            self.assertEqual([], validate_adapter_archives("v0.1.3", output_dir, skills_root=ROOT / "skills"))

    def test_validate_adapter_output_rejects_stale_mapped_resource_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(
                root,
                ("portable-with-assets",),
            )
            generated_resource = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "portable-with-assets"
                / "assets"
                / "template.md"
            )
            generated_resource.write_text(
                generated_resource.read_text(encoding="utf-8") + "\nstale\n",
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(
                any(
                    "mapped resource parity mismatch: codex/portable-with-assets: "
                    "assets/template.md" in error
                    and "canonical sha256=" in error
                    and "generated sha256=" in error
                    for error in errors
                ),
                errors,
            )

    def test_validate_adapter_archives_rejects_stale_mapped_resource_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills")
            archive_path = output_dir / adapter_archive_name("codex", "v0.1.5")
            entry_name = ".agents/skills/portable-with-assets/assets/template.md"

            with zipfile.ZipFile(archive_path) as archive:
                entries = {
                    name: archive.read(name)
                    for name in archive.namelist()
                    if not name.endswith("/")
                }
            entries[entry_name] = b"stale\n"
            with zipfile.ZipFile(archive_path, "w") as archive:
                for name, content in sorted(entries.items()):
                    archive.writestr(name, content)

            errors = validate_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills")

            self.assertTrue(
                any(
                    "mapped resource parity mismatch: codex/portable-with-assets: "
                    "assets/template.md" in error
                    and "canonical sha256=" in error
                    and "archive sha256=" in error
                    for error in errors
                ),
                errors,
            )

    def test_boundary_first_archives_and_clean_installs_preserve_all_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temporary_root = Path(tmp)
            output_dir = temporary_root / "release-output"
            generated_root = temporary_root / "generated"
            version = "v0.3.6"
            sync_adapter_output(
                version,
                skills_root=ROOT / "skills",
                output_root=generated_root,
            )
            build_adapter_archives(version, output_dir, skills_root=ROOT / "skills")

            self.assertEqual(
                [],
                validate_adapter_archives(
                    version,
                    output_dir,
                    skills_root=ROOT / "skills",
                ),
            )
            manifest = load_resource_manifest(ROOT)
            reports = {
                report.name: report
                for report in collect_skill_reports(ROOT / "skills")
            }
            public_governed_skills = tuple(
                sorted(set(GOVERNED_SKILLS) & set(POST_CUTOVER_ADAPTER_SKILLS))
            )
            for skill_name in public_governed_skills:
                self.assertEqual(
                    reports[skill_name].included_adapters,
                    SUPPORTED_ADAPTERS,
                    skill_name,
                )
            expected_records = {
                (Path("skills") / skill_name / resource.target).as_posix(): raw_sha256(
                    (ROOT / resource.source).read_bytes()
                )
                for skill_name in public_governed_skills
                for resource in manifest.resources
                if skill_name in resource.consumers
            }
            expected_digest = inventory_digest(expected_records)
            seen: set[tuple[str, str, str]] = set()
            for adapter_name in SUPPORTED_ADAPTERS:
                config = ADAPTERS[adapter_name]
                archive_path = output_dir / adapter_archive_name(adapter_name, version)
                generated_records: dict[str, str] = {}
                archive_records: dict[str, str] = {}
                with zipfile.ZipFile(archive_path) as archive:
                    for skill_name in public_governed_skills:
                        skill_entry = config.skill_path(skill_name).as_posix()
                        self.assertTrue(archive.read(skill_entry))
                        for resource in manifest.resources:
                            if skill_name not in resource.consumers:
                                continue
                            reference_entry = (
                                config.skill_root
                                / skill_name
                                / resource.target
                            ).as_posix()
                            self.assertEqual(
                                archive.read(reference_entry),
                                (ROOT / resource.source).read_bytes(),
                            )
                            logical_path = (
                                Path("skills") / skill_name / resource.target
                            ).as_posix()
                            generated_path = (
                                generated_root
                                / adapter_name
                                / config.skill_root
                                / skill_name
                                / resource.target
                            )
                            generated_records[logical_path] = raw_sha256(
                                generated_path.read_bytes()
                            )
                            archive_records[logical_path] = raw_sha256(
                                archive.read(reference_entry)
                            )
                            seen.add(
                                (adapter_name, skill_name, resource.resource_id)
                            )
                self.assertEqual(len(generated_records), len(expected_records))
                self.assertEqual(inventory_digest(generated_records), expected_digest)
                self.assertEqual(len(archive_records), len(expected_records))
                self.assertEqual(inventory_digest(archive_records), expected_digest)
            expected = {
                (adapter_name, skill_name, resource.resource_id)
                for skill_name in public_governed_skills
                for adapter_name in SUPPORTED_ADAPTERS
                for resource in manifest.resources
                if skill_name in resource.consumers
            }
            self.assertEqual(seen, expected)

            installed_identities: dict[str, tuple[int, str]] = {}

            def capture_runner(command, **kwargs):
                result = subprocess.run(command, **kwargs)
                if result.returncode != 0:
                    return result
                adapter_name = command[command.index("init") + 1]
                config = ADAPTERS[adapter_name]
                project_root = Path(kwargs["cwd"])
                records: dict[str, str] = {}
                for resource in manifest.resources:
                    for skill_name in sorted(
                        set(resource.consumers) & set(public_governed_skills)
                    ):
                        installed_path = (
                            project_root
                            / config.skill_root
                            / skill_name
                            / resource.target
                        )
                        logical_path = (
                            Path("skills") / skill_name / resource.target
                        ).as_posix()
                        records[logical_path] = raw_sha256(installed_path.read_bytes())
                installed_identities[adapter_name] = (
                    len(records),
                    inventory_digest(records),
                )
                return result

            self.assertEqual(
                [],
                validate_clean_install_smoke(
                    version,
                    output_dir,
                    skills_root=ROOT / "skills",
                    skill_names=public_governed_skills,
                    command_runner=capture_runner,
                ),
            )
            self.assertEqual(
                installed_identities,
                {
                    adapter_name: (len(expected_records), expected_digest)
                    for adapter_name in SUPPORTED_ADAPTERS
                },
            )

    def test_clean_install_requested_skill_cannot_be_filtered_by_portability(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            version = "v0.3.6"
            build_adapter_archives(version, output_dir, skills_root=ROOT / "skills")
            archive_path = output_dir / adapter_archive_name("claude", version)
            route_root = (
                ADAPTERS["claude"].skill_root / "route"
            ).as_posix() + "/"
            with zipfile.ZipFile(archive_path) as archive:
                retained = {
                    name: archive.read(name)
                    for name in archive.namelist()
                    if not name.startswith(route_root)
                }
            with zipfile.ZipFile(archive_path, "w") as archive:
                for name, content in sorted(retained.items()):
                    archive.writestr(name, content)

            errors = validate_clean_install_smoke(
                version,
                output_dir,
                skills_root=ROOT / "skills",
                skill_names=("route",),
            )

        self.assertTrue(
            any(
                "clean-install skill root missing: claude/route" in error
                for error in errors
            ),
            errors,
        )

    def test_clean_install_rejects_unknown_noncanonical_and_duplicate_selections(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            version = "v0.3.6"
            build_adapter_archives(version, output_dir, skills_root=ROOT / "skills")
            cases = {
                "mixed_unknown": (
                    ("route", "does-not-exist"),
                    "clean-install selected skill is unknown or has no mapped "
                    "resources: does-not-exist",
                ),
                "noncanonical_case": (
                    ("Workflow",),
                    "clean-install selected skill is unknown or has no mapped "
                    "resources: Workflow",
                ),
                "duplicate": (
                    ("route", "route"),
                    "clean-install selected skill repeated: route",
                ),
            }
            for name, (skill_names, expected) in cases.items():
                with self.subTest(name=name):
                    errors = validate_clean_install_smoke(
                        version,
                        output_dir,
                        skills_root=ROOT / "skills",
                        skill_names=skill_names,
                    )
                    self.assertTrue(
                        any(expected in error for error in errors),
                        errors,
                    )

    def test_validate_adapters_cli_rejects_mixed_unknown_skill_selection(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            version = "v0.3.6"
            build_adapter_archives(version, output_dir, skills_root=ROOT / "skills")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-adapters.py"),
                    "--root",
                    str(output_dir),
                    "--version",
                    version,
                    "--clean-install-smoke",
                    "--skill",
                    "route",
                    "--skill",
                    "does-not-exist",
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "clean-install selected skill is unknown or has no mapped resources: "
            "does-not-exist",
            result.stdout,
        )
        self.assertNotIn("validated generated adapter archives", result.stdout)

    def test_validate_adapters_cli_preflights_selection_before_archives(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-adapters.py"),
                    "--root",
                    tmp,
                    "--version",
                    "v0.3.6",
                    "--clean-install-smoke",
                    "--skill",
                    "does-not-exist",
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "clean-install selected skill is unknown or has no mapped resources: "
            "does-not-exist",
            result.stdout,
        )
        self.assertNotIn("clean-install archive missing", result.stdout)

    def test_boundary_first_archive_drift_reports_exact_layer_and_hashes(self) -> None:
        cases = (
            ("route", "references/boundary-first-method-v1.md"),
            ("design", "references/boundary-first-feature-authoring-v1.md"),
        )
        for skill_name, relative_resource in cases:
            with self.subTest(layer=relative_resource), tempfile.TemporaryDirectory() as tmp:
                output_dir = Path(tmp) / "release-output"
                version = "v0.3.6"
                build_adapter_archives(version, output_dir, skills_root=ROOT / "skills")
                archive_path = output_dir / adapter_archive_name("codex", version)
                entry_name = (
                    ADAPTERS["codex"].skill_root
                    / skill_name
                    / relative_resource
                ).as_posix()
                with zipfile.ZipFile(archive_path) as archive:
                    entries = {
                        name: archive.read(name)
                        for name in archive.namelist()
                        if not name.endswith("/")
                    }
                entries[entry_name] = b"stale boundary reference\n"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    for name, content in sorted(entries.items()):
                        archive.writestr(name, content)

                errors = validate_adapter_archives(
                    version,
                    output_dir,
                    skills_root=ROOT / "skills",
                )

                self.assertTrue(
                    any(
                        f"mapped resource parity mismatch: codex/{skill_name}: "
                        f"{relative_resource}" in error
                        and "canonical sha256=" in error
                        and "archive sha256=" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validate_adapter_output_rejects_missing_mapped_resource(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = self.generate_fixture_adapters(
                root,
                ("portable-with-assets",),
            )
            (
                output_root
                / "claude"
                / ".claude"
                / "skills"
                / "portable-with-assets"
                / "assets"
                / "template.md"
            ).unlink()

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(
                any(
                    "mapped resource missing: claude/portable-with-assets: "
                    "assets/template.md in generated adapter output claude" in error
                    for error in errors
                ),
                errors,
            )

    def test_validate_adapter_archives_rejects_missing_required_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            (output_dir / adapter_archive_name("claude", "v0.1.2")).unlink()

            errors = validate_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")

            self.assertTrue(
                any("missing adapter archive: claude" in error for error in errors),
                errors,
            )

    def test_clean_install_smoke_installs_mapped_resources_from_local_archives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)

            commands = []

            def filesystem_only_runner(command, **kwargs):
                commands.append(tuple(command))
                return subprocess.run(command, **kwargs)

            errors = validate_clean_install_smoke(
                "v0.3.4",
                output_dir,
                skills_root=skills_root,
                skill_names=("portable-with-assets",),
                command_runner=filesystem_only_runner,
            )

        self.assertEqual([], errors)
        self.assertEqual(
            [command[command.index("init") + 1] for command in commands],
            ["codex", "claude"],
        )
        for command in commands:
            self.assertEqual(command[0], "node")
            self.assertIn("init", command)
            self.assertIn("--from-archive", command)
            self.assertNotIn("prompt", " ".join(command).lower())
            self.assertNotIn("exec", command)

    def test_proposal_stage_packages_pass_supported_archive_install_parity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            version = "v0.4.1"
            build_adapter_archives(version, output_dir, skills_root=ROOT / "skills")

            archive_errors = validate_adapter_archives(
                version,
                output_dir,
                skills_root=ROOT / "skills",
            )
            install_errors = validate_clean_install_smoke(
                version,
                output_dir,
                skills_root=ROOT / "skills",
                skill_names=("proposal", "proposal-review"),
            )

        self.assertEqual(archive_errors, [])
        self.assertEqual(install_errors, [])

    def clean_install_runner_with_resource_mutation(
        self,
        *,
        target: str,
        skill_name: str,
        relative_resource_path: str,
        mutation,
        real_runner=subprocess.run,
    ):
        def runner(command, **kwargs):
            result = real_runner(command, **kwargs)
            installed_target = command[command.index("init") + 1]
            if result.returncode != 0 or installed_target != target:
                return result

            project_root = Path(kwargs["cwd"])
            skill_root = project_root / Path(ADAPTERS[target].skill_root.as_posix()) / skill_name
            self.assertTrue(skill_root.is_dir(), skill_root)
            self.assertTrue((skill_root / "SKILL.md").is_file(), skill_root)

            resource_path = skill_root / relative_resource_path
            self.assertTrue(resource_path.is_file(), resource_path)
            mutation(resource_path)
            return result

        return runner

    def test_clean_install_smoke_rejects_non_installing_command_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)

            def fake_runner(command, **kwargs):
                return subprocess.CompletedProcess(command, 0, stdout='{"status":"success"}', stderr="")

            errors = validate_clean_install_smoke(
                "v0.3.4",
                output_dir,
                skills_root=skills_root,
                skill_names=("portable-with-assets",),
                command_runner=fake_runner,
            )

        self.assertTrue(
            any("clean-install skill root missing: codex/portable-with-assets" in error for error in errors),
            errors,
        )

    def test_clean_install_smoke_rejects_missing_installed_mapped_resource(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)

            errors = validate_clean_install_smoke(
                "v0.3.4",
                output_dir,
                skills_root=skills_root,
                skill_names=("portable-with-assets",),
                command_runner=self.clean_install_runner_with_resource_mutation(
                    target="codex",
                    skill_name="portable-with-assets",
                    relative_resource_path="assets/template.md",
                    mutation=lambda path: path.unlink(),
                ),
            )

        self.assertTrue(
            any(
                "clean-install mapped resource missing: codex/portable-with-assets: "
                "assets/template.md" in error
                for error in errors
            ),
            errors,
        )
        self.assertFalse(any("skill root missing" in error for error in errors), errors)

    def test_clean_install_smoke_rejects_stale_installed_mapped_resource(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)

            errors = validate_clean_install_smoke(
                "v0.3.4",
                output_dir,
                skills_root=skills_root,
                skill_names=("portable-with-assets",),
                command_runner=self.clean_install_runner_with_resource_mutation(
                    target="claude",
                    skill_name="portable-with-assets",
                    relative_resource_path="assets/template.md",
                    mutation=lambda path: path.write_text("stale installed bytes\n", encoding="utf-8"),
                ),
            )

        self.assertTrue(
            any(
                "clean-install mapped resource parity mismatch: claude/portable-with-assets: "
                "assets/template.md" in error
                and "canonical sha256=" in error
                and "installed sha256=" in error
                for error in errors
            ),
            errors,
        )

    def test_clean_install_smoke_rejects_unowned_boundary_resources_for_each_adapter(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)

            def runner(command, **kwargs):
                result = subprocess.run(command, **kwargs)
                if result.returncode != 0:
                    return result
                adapter_name = command[command.index("init") + 1]
                project_root = Path(kwargs["cwd"])
                skill_root = (
                    project_root
                    / Path(ADAPTERS[adapter_name].skill_root.as_posix())
                    / "portable-with-assets"
                )
                extra_name = {
                    "codex": "boundary-first-compact-core.md",
                    "claude": "boundary-first-feature-authoring.md",
                }[adapter_name]
                (skill_root / "references" / extra_name).parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                (skill_root / "references" / extra_name).write_text(
                    "unowned\n",
                    encoding="utf-8",
                )
                return result

            errors = validate_clean_install_smoke(
                "v0.3.4",
                output_dir,
                skills_root=skills_root,
                skill_names=("portable-with-assets",),
                command_runner=runner,
            )

        for adapter_name, resource_name in {
            "codex": "boundary-first-compact-core.md",
            "claude": "boundary-first-feature-authoring.md",
        }.items():
            self.assertTrue(
                any(
                    f"clean-install unowned boundary resource: "
                    f"{adapter_name}/portable-with-assets: "
                    f"references/{resource_name}" in error
                    for error in errors
                ),
                errors,
            )

    def test_validate_adapters_cli_rejects_clean_install_smoke_without_archive_root(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate-adapters.py"),
                "--version",
                "v0.3.3",
                "--clean-install-smoke",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--clean-install-smoke requires --adapter-root", result.stdout)

    def test_validate_adapters_cli_accepts_release_archive_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"

            build_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build-adapters.py"),
                    "--version",
                    "v0.1.2",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, build_result.returncode, build_result.stdout + build_result.stderr)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-adapters.py"),
                    "--adapter-root",
                    str(output_dir),
                    "--version",
                    "v0.1.2",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("Gate B (published adapter/package parity)", result.stdout)
            self.assertIn("validated generated adapter archives for version v0.1.2", result.stdout)

    def test_gate_b_does_not_accept_one_targets_archive_as_another(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = self.copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)
            codex = output_dir / adapter_archive_name("codex", "v0.3.4")
            claude = output_dir / adapter_archive_name("claude", "v0.3.4")
            claude.write_bytes(codex.read_bytes())

            errors = validate_adapter_archives(
                "v0.3.4", output_dir, skills_root=skills_root
            )

        self.assertTrue(
            any("claude" in error and ("root" in error or "missing" in error) for error in errors),
            errors,
        )

    def test_adapter_artifact_metadata_validation_accepts_schema_and_optional_combined(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = self.write_adapter_artifact_metadata(root, output_dir).parent

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
            self.copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = self.write_adapter_artifact_metadata(
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
            self.copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = self.write_adapter_artifact_metadata(
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
            self.copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            metadata_root = self.write_adapter_artifact_metadata(root, output_dir).parent

            errors = validate_adapter_artifact_metadata(
                "v0.1.2",
                output_dir,
                metadata_root=metadata_root,
                release_commit="fedcba9876543210fedcba9876543210fedcba98",
            )

            self.assertTrue(any("release.source_commit mismatch" in error for error in errors), errors)


    def test_portable_skill_includes_all_adapters(self) -> None:
        report = evaluate_skill(self.fixture("portable-basic"))

        self.assertTrue(report.portable)
        self.assertEqual(report.name, "portable-basic")
        self.assertEqual(report.included_adapters, ("codex", "claude"))
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
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        expected_transforms = (
            "drop frontmatter: argument-hint",
            "drop frontmatter: schema-version",
            "drop frontmatter: version",
        )
        self.assertEqual(report.adapter_decision("claude").transforms, expected_transforms)

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
                self.assertIn(expected_reason, report.reason)

    def test_case_variant_governed_dollar_invocations_are_codex_only(self) -> None:
        source = self.fixture("codex-dollar-skill")
        source_text = (source / "SKILL.md").read_text(encoding="utf-8")

        for token in (
            "$Proposal",
            "$PROPOSAL",
            "$Route",
            "$ROUTE",
            "$plan",
            "$PLAN",
            "$proposal-review",
        ):
            with self.subTest(token=token), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "codex-dollar-skill"
                shutil.copytree(source, target)
                (target / "SKILL.md").write_text(
                    source_text.replace("$proposal", token),
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, ("codex",))
                self.assertIn("Codex-specific $skill invocation", report.reason)

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
            skills_root = self.copy_fixture_skills(
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

    def test_post_cutover_archives_have_exact_gate_inventory_for_every_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            version = "v0.4.1"
            archives = build_adapter_archives(version, output_dir)

            self.assertEqual(len(archives), len(SUPPORTED_ADAPTERS))
            for adapter_name in SUPPORTED_ADAPTERS:
                archive_path = output_dir / adapter_archive_name(adapter_name, version)
                skill_root = ADAPTERS[adapter_name].skill_root.as_posix().rstrip("/")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                packaged = {
                    path.removeprefix(f"{skill_root}/").split("/", 1)[0]
                    for path in names
                    if path.startswith(f"{skill_root}/") and path.endswith("/SKILL.md")
                }
                with self.subTest(adapter=adapter_name):
                    self.assertEqual(packaged, set(POST_CUTOVER_ADAPTER_SKILLS))
                    self.assertTrue(RETIRED_PROGRESSION_SKILLS.isdisjoint(packaged))

    def test_retired_gate_in_generated_output_is_unexpected_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"
            sync_adapter_output("v0.4.1", output_root=output_root)
            retired_path = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "spec-review"
                / "SKILL.md"
            )
            retired_path.parent.mkdir(parents=True)
            retired_path.write_text("retired\n", encoding="utf-8")

            drift = collect_adapter_drift_entries("v0.4.1", output_root=output_root)
            self.assertTrue(
                any(entry.category == "unexpected" and entry.path == retired_path for entry in drift),
                drift,
            )

    def test_real_dollar_invocation_is_not_hidden_by_later_dollar(self) -> None:
        source = self.fixture("codex-dollar-skill")
        source_text = (source / "SKILL.md").read_text(encoding="utf-8")
        lines = (
            "Invoke `$plan`; let `$x$` denote the input.",
            "Invoke `$plan`; then read `$HOME`.",
            "Invoke `$plan`; the fallback costs $5.",
            r"Invoke `$plan`; document \$value.",
            "Invoke `$route auto: status`; let `$plan + 1$` denote input.",
            "Invoke `$plan` -> then read `$HOME`.",
            "Invoke `$plan` - then read `$HOME`.",
            "Invoke `$plan` -> budget $5.",
            r"Invoke `$plan` -> document \$value.",
            "Invoke `$plan` --verbose then inspect `$HOME`.",
            "Invoke `$plan` + compare with `$PATH`.",
            "Invoke `$plan` < input then inspect `$HOME`.",
            "Invoke $plan -> inspect ${HOME}.",
            "Invoke $plan -> run $(pwd).",
            r"Invoke $plan + 5\$.",
            r"Invoke \\$plan.",
        )

        for line in lines:
            with self.subTest(line=line), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "codex-dollar-skill"
                shutil.copytree(source, target)
                (target / "SKILL.md").write_text(
                    source_text.replace(
                        "Invoke this workflow as `$proposal` before continuing.",
                        line,
                    ),
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, ("codex",))
                self.assertIn("Codex-specific $skill invocation", report.reason)

    def test_generic_artifact_paths_remain_portable(self) -> None:
        report = evaluate_skill(self.fixture("generic-artifact-paths"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))

    def test_codex_skills_reference_with_adapter_alternatives_remains_portable(self) -> None:
        report = evaluate_skill(self.fixture("codex-install-with-alternatives"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        self.assertEqual(report.reason, "")

    def test_route_explicit_adapter_invocation_equivalents_remain_portable(
        self,
    ) -> None:
        report = evaluate_skill(ROOT / "skills" / "route")

        self.assertTrue(report.portable, report.reason)
        self.assertEqual(report.included_adapters, SUPPORTED_ADAPTERS)

    def test_route_invocation_checks_preserve_variables_and_paths(self) -> None:
        additions = (
            "Read the shell variable `$project`.",
            "Let `$x$` denote the input.",
            "Read the shell variable `$workflow_status`.",
            "Read the path from `$plan_path`.",
            "Let `$spec₂` denote the input.",
            "Let `$plan$` denote the input.",
            "Let `$plan + 1$` denote the input.",
            "Let `$plan^2$` denote the input.",
            "Let `$plan + 1 - 2$` denote the input.",
            "Let `$plan + (1)$` denote the input.",
            "Let `$plan + π$` denote the input.",
            "Let `$plan ** 2$` denote the input.",
            "Let `$plan >= 1$` denote the input.",
            "Let `$plan + -1$` denote the input.",
            r"Let `$plan + \$5$` denote the input.",
            r"Document \$plan as a literal.",
            r"Document \\\$plan as a literal.",
            "Read the variable `$plan\u0301_value`.",
            "Read the variable `$workflow\ufe0f`.",
            "Read the variable `$plan\u200c_value`.",
            "Read the variable `$plan\u200d_value`.",
            "Do not treat `$ſpec` as a published name.",
            "Do not treat `$ımplement` as a published name.",
            "Do not treat `$worKflow` as a published name.",
            "Document `/workflow-guide`.",
            "Document `/workflow.md`.",
            "Document `/workflow/status`.",
            "Document `docs-/workflow`.",
            "Do not treat `/worKflow` as a published command.",
        )
        source = ROOT / "skills" / "route" / "SKILL.md"
        source_text = source.read_text(encoding="utf-8")

        for addition in additions:
            with self.subTest(addition=addition), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "route"
                shutil.copytree(source.parent, target)
                (target / "SKILL.md").write_text(
                    source_text + f"\n{addition}\n",
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, SUPPORTED_ADAPTERS)

    def test_route_slash_commands_end_at_phrase_terminators(self) -> None:
        additions = (
            "Run /route\nThen continue.",
            "Run /route\r\nThen continue.",
            "Run `/route` before continuing.",
            "Run /route, then continue.",
            "Run /route. Then continue.",
        )
        source = ROOT / "skills" / "route" / "SKILL.md"
        source_text = source.read_text(encoding="utf-8")

        for addition in additions:
            with self.subTest(addition=addition), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "route"
                shutil.copytree(source.parent, target)
                (target / "SKILL.md").write_text(
                    source_text + f"\n{addition}\n",
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, ("codex",))
                self.assertIn("Codex-specific $skill invocation", report.reason)

    def test_route_invocation_equivalence_uses_narrow_static_scope(
        self,
    ) -> None:
        mutations = {
            "codex_skill": lambda text: text.replace(
                "$route auto: <argument>",
                "$broken auto: <argument>",
                1,
            ),
            "claude_skill": lambda text: text.replace(
                "/route auto: <argument>",
                "/broken auto: <argument>",
                1,
            ),
            "shared_argument": lambda text: text.replace(
                "Here `<argument>` is `<target-stage>`, `status`, or `off`.",
                "Here `<argument>` is `<stage>`, `status`, or `off`.",
                1,
            ),
            "bare_codex": lambda text: text + "\nUse `$route`.\n",
            "non_auto_codex": lambda text: text + "\nUse `$route manual`.\n",
            "case_codex": lambda text: text + "\nUse `$Route auto: <argument>`.\n",
            "wrong_claude_argument": lambda text: text
            + "\nUse `/route auto: <wrong>`.\n",
            "case_claude": lambda text: text
            + "\nUse `/Route auto: <argument>`.\n",
            "wrong_opencode_argument": lambda text: text
            + "\nOpenCode invokes installed `route` with `auto: <wrong>`.\n",
            "case_opencode": lambda text: text
            + "\nOpenCode invokes installed `Route` with `auto: <argument>`.\n",
            "plain_codex": lambda text: text
            + "\nUse $route manual to continue.\n",
            "html_codex": lambda text: text
            + "\nUse <code>$route manual</code> to continue.\n",
            "plain_claude": lambda text: text
            + "\nClaude users run /route manual to continue.\n",
            "whitespace_claude": lambda text: text
            + "\nClaude users run ` /route auto: <wrong>`.\n",
            "plain_opencode": lambda text: text
            + "\nOpenCode invokes route with auto: wrong.\n",
            "composed_opencode": lambda text: text
            + "\nOpenCode invokes installed `broken` skill with "
            + "`manual: <argument>`.\n",
            "codex_labeled_composed": lambda text: text
            + "\nCodex users run broken manual to continue.\n",
            "codex_labeled_html": lambda text: text
            + "\nCodex uses <code>broken manual</code>.\n",
            "codex_entity": lambda text: text
            + "\nCodex uses &#36;route manual.\n",
            "claude_call": lambda text: text
            + "\nFor Claude, call /broken auto: wrong.\n",
            "opencode_execute": lambda text: text
            + "\nOpenCode executes route with auto: wrong.\n",
            "opencode_command": lambda text: text
            + "\nOpenCode command: route auto: wrong.\n",
            "html_split_codex": lambda text: text
            + "\nCo<em>dex</em> executes broken manual.\n",
            "html_split_claude": lambda text: text
            + "\nCla<strong>ude</strong> starts broken manual.\n",
            "html_split_opencode": lambda text: text
            + "\nOpen<span>Code</span> command: broken manual.\n",
            "html_comment_codex": lambda text: text
            + "\nCo<!-- hidden -->dex executes broken manual.\n",
            "html_attribute_opencode": lambda text: text
            + '\nOpen<span title=">">Code</span> command: broken manual.\n',
            "html_unknown_tag_claude": lambda text: text
            + "\nCla<custom>ude</custom> starts broken manual.\n",
            "markdown_emphasis_codex": lambda text: text
            + "\nCo**dex** executes broken manual.\n",
            "markdown_emphasis_claude": lambda text: text
            + "\nCla**_ude_** starts broken manual.\n",
            "markdown_link_opencode": lambda text: text
            + "\nOpen[Code](https://example.invalid) command: broken manual.\n",
            "markdown_triple_emphasis_codex": lambda text: text
            + "\nCo***dex*** executes broken manual.\n",
            "markdown_mixed_emphasis_opencode": lambda text: text
            + "\nOpen**_Code_** command: broken manual.\n",
            "markdown_nested_strike_opencode": lambda text: text
            + "\nOpen~~**Code**~~ command: broken manual.\n",
            "markdown_nested_link_opencode": lambda text: text
            + "\nOpen[***Code***](https://example.invalid) command: broken manual.\n",
            "markdown_code_opencode": lambda text: text
            + "\nOpen`Code` command: broken manual.\n",
            "markdown_full_reference_codex": lambda text: text
            + "\nCo[dex][vendor] executes broken manual.\n"
            + "[vendor]: https://example.invalid\n",
            "markdown_collapsed_reference_claude": lambda text: text
            + "\nCla[ude][] starts broken manual.\n"
            + "[ude]: https://example.invalid\n",
            "markdown_shortcut_reference_opencode": lambda text: text
            + "\nOpen[Code] command: broken manual.\n"
            + "[Code]: https://example.invalid\n",
            "placeholder_tag_opencode": lambda text: text
            + "\nOpen<argument>Code</argument> command: broken manual.\n",
            "target_placeholder_tag_opencode": lambda text: text
            + "\nOpen<target-stage>Code</target-stage> command: broken manual.\n",
            "private_use_split_opencode": lambda text: text
            + "\nOpen\uf000\uf001Code command: broken manual.\n",
            "encoded_zero_width_split_opencode": lambda text: text
            + "\nOpen&#x200B;Code command: broken manual.\n",
            "combining_joiner_split_opencode": lambda text: text
            + "\nOpen\u034fCode command: broken manual.\n",
            "variation_selector_split_opencode": lambda text: text
            + "\nOpen\ufe0fCode command: broken manual.\n",
            "encoded_combining_joiner_split_opencode": lambda text: text
            + "\nOpen&#x034F;Code command: broken manual.\n",
            "encoded_variation_selector_split_opencode": lambda text: text
            + "\nOpen&#xFE0F;Code command: broken manual.\n",
            "null_control_split_opencode": lambda text: text
            + "\nOpen\u0000Code command: broken manual.\n",
            "backspace_control_split_opencode": lambda text: text
            + "\nOpen\u0008Code command: broken manual.\n",
            "unit_separator_split_opencode": lambda text: text
            + "\nOpen\u001fCode command: broken manual.\n",
            "hangul_filler_split_opencode": lambda text: text
            + "\nOpen\u115fCode command: broken manual.\n",
            "halfwidth_hangul_filler_split_opencode": lambda text: text
            + "\nOpen\uffa0Code command: broken manual.\n",
            "encoded_hangul_filler_split_opencode": lambda text: text
            + "\nOpen&#x115F;Code command: broken manual.\n",
            "mongolian_variation_split_opencode": lambda text: text
            + "\nOpen\u180bCode command: broken manual.\n",
            "encoded_mongolian_variation_split_opencode": lambda text: text
            + "\nOpen&#x180B;Code command: broken manual.\n",
            "khmer_inherent_vowel_split_opencode": lambda text: text
            + "\nOpen\u17b4Code command: broken manual.\n",
            "literal_argument_sentinel": lambda text: text.replace(
                "Claude uses `/route auto: <argument>`",
                "Claude uses `/route auto: \uf000argument\uf001`",
                1,
            ),
            "encoded_argument_sentinel": lambda text: text.replace(
                "Claude uses `/route auto: <argument>`",
                "Claude uses `/route auto: &#xF000;argument&#xF001;`",
                1,
            ),
            "literal_target_sentinel": lambda text: text.replace(
                "Here `<argument>` is `<target-stage>`",
                "Here `<argument>` is `\uf000target-stage\uf001`",
                1,
            ),
            "claude_zero_width_identity": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/rou\u200bte auto: <argument>`",
                1,
            ),
            "claude_private_use_identity": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/rou\uf000te auto: <argument>`",
                1,
            ),
            "claude_uppercase_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <ARGUMENT>`",
                1,
            ),
            "claude_spaced_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <argument >`",
                1,
            ),
            "claude_self_closing_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <argument/>`",
                1,
            ),
            "claude_encoded_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: &lt;argument&gt;`",
                1,
            ),
            "uppercase_target_placeholder": lambda text: text.replace(
                "`<target-stage>`",
                "`<TARGET-STAGE>`",
                1,
            ),
            "nested_claude_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <custom><argument></custom>`",
                1,
            ),
            "claude_nbsp_separator": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route\u00a0auto: <argument>`",
                1,
            ),
            "claude_em_space_separator": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route\u2003auto: <argument>`",
                1,
            ),
            "claude_tab_separator": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route\tauto: <argument>`",
                1,
            ),
            "slash_unit_separator": lambda text: text
            + "\nUse /work\u001fflow manual.\n",
            "slash_file_separator": lambda text: text
            + "\nUse /work\u001cflow manual.\n",
            "slash_next_line_control": lambda text: text
            + "\nUse /work\u0085flow manual.\n",
            "slash_mongolian_variation": lambda text: text
            + "\nUse /work\u180bflow manual.\n",
            "codex_status_suffix": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status-now`",
                1,
            ),
            "codex_status_trailing_argument": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status extra`",
                1,
            ),
            "codex_off_prefix": lambda text: text.replace(
                "`$route auto: off`",
                "`$route auto: office`",
                1,
            ),
            "codex_target_suffix": lambda text: text.replace(
                "`$route auto: <target-stage>`",
                "`$route auto: <target-stage>-extra`",
                1,
            ),
            "codex_command_prefix": lambda text: text.replace(
                "`$route auto: status`",
                "`x$route auto: status`",
                1,
            ),
            "codex_status_html_suffix": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status<em>-now</em>`",
                1,
            ),
            "codex_status_adjacent_suffix": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status`-now",
                1,
            ),
            "codex_off_adjacent_suffix": lambda text: text.replace(
                "`$route auto: off`",
                "`$route auto: off`-now",
                1,
            ),
            "codex_target_adjacent_suffix": lambda text: text.replace(
                "`$route auto: <target-stage>`",
                "`$route auto: <target-stage>`-extra",
                1,
            ),
            "codex_status_adjacent_argument": lambda text: text.replace(
                "`$route auto: status` is read-only",
                "`$route auto: status` extra is read-only",
                1,
            ),
            "equivalence_block_suffix": lambda text: text.replace(
                "Here `<argument>` is `<target-stage>`, `status`, or `off`.",
                "Here `<argument>` is `<target-stage>`, `status`, or `off`.extra",
                1,
            ),
        }
        nonportable = {
            "codex_skill",
            "claude_skill",
            "shared_argument",
            "bare_codex",
            "non_auto_codex",
            "case_codex",
            "wrong_claude_argument",
            "case_claude",
            "plain_codex",
            "html_codex",
            "plain_claude",
            "whitespace_claude",
            "literal_argument_sentinel",
            "encoded_argument_sentinel",
            "literal_target_sentinel",
            "claude_zero_width_identity",
            "claude_private_use_identity",
            "claude_uppercase_placeholder",
            "claude_spaced_placeholder",
            "claude_self_closing_placeholder",
            "claude_encoded_placeholder",
            "uppercase_target_placeholder",
            "nested_claude_placeholder",
            "claude_nbsp_separator",
            "claude_em_space_separator",
            "claude_tab_separator",
            "codex_status_suffix",
            "codex_status_trailing_argument",
            "codex_off_prefix",
            "codex_target_suffix",
            "codex_command_prefix",
            "codex_status_html_suffix",
            "codex_status_adjacent_suffix",
            "codex_off_adjacent_suffix",
            "codex_target_adjacent_suffix",
            "codex_status_adjacent_argument",
            "equivalence_block_suffix",
        }
        source = ROOT / "skills" / "route" / "SKILL.md"
        source_text = source.read_text(encoding="utf-8")
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "route"
                shutil.copytree(source.parent, target)
                skill_file = target / "SKILL.md"
                mutated = mutate(source_text)
                self.assertNotEqual(mutated, source_text, "mutation must exercise the current contract")
                skill_file.write_text(mutated, encoding="utf-8")

                report = evaluate_skill(target)

                if name in nonportable:
                    self.assertEqual(report.included_adapters, ("codex",))
                    self.assertIn(
                        "Codex-specific $skill invocation",
                        report.reason,
                    )
                else:
                    self.assertEqual(report.included_adapters, SUPPORTED_ADAPTERS)

    def test_route_benign_visible_boundaries_remain_portable(self) -> None:
        additions = (
            "Encode XML before parsing.",
            "Encode X509 certificates consistently.",
            "Keep open code samples in the fixture.",
            "Review open-code licensing separately.",
            "The cod_ex identifier is illustrative.",
            "The Co_dex_ key is illustrative.",
            "The Open_Code_ key is illustrative.",
            "The Co`dex token is illustrative.",
            "The Open[Code token is illustrative.",
            "The Cla]ude token is illustrative.",
            "The Open[Code] token is illustrative.",
            "The Open[Code][missing] token is illustrative.",
            "The Open[Code][] token is illustrative.",
            "The Open&#42;Code&#42; token is illustrative.",
            "The Open&#42;&#42;Code&#42;&#42; token is illustrative.",
            "The Open&#91;Code&#93; token is illustrative.",
            "The Open&#96;Code&#96; token is illustrative.",
            "An unrelated /workéflow token is illustrative.",
            "An unrelated /work☃flow token is illustrative.",
        )
        source = ROOT / "skills" / "route" / "SKILL.md"
        source_text = source.read_text(encoding="utf-8")
        for addition in additions:
            with self.subTest(addition=addition), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "route"
                shutil.copytree(source.parent, target)
                (target / "SKILL.md").write_text(
                    source_text + f"\n{addition}\n",
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, SUPPORTED_ADAPTERS)

    def test_unrelated_equivalence_prose_does_not_portabilize_dollar_skill(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "codex-dollar-skill"
            shutil.copytree(self.fixture("codex-dollar-skill"), target)
            skill_file = target / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8")
                + "\nAdapter invocation equivalents: Codex uses, Claude uses, "
                + "and opencode invokes.\n",
                encoding="utf-8",
            )

            report = evaluate_skill(target)

        self.assertEqual(report.included_adapters, ("codex",))
        self.assertIn("Codex-specific $skill invocation", report.reason)

    def test_retired_target_exclusion_does_not_reduce_current_portability(self) -> None:
        report = evaluate_skill(self.fixture("partial-portability"))
        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        self.assertTrue(report.adapter_decision("codex").included)
        self.assertTrue(report.adapter_decision("claude").included)


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

            self.assertIn("argument-hint:", codex_skill)
            self.assertIn("schema-version:", codex_skill)
            self.assertIn("version:", codex_skill)
            self.assertNotIn("argument-hint:", claude_skill)
            self.assertNotIn("schema-version:", claude_skill)
            self.assertNotIn("version:", claude_skill)


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
                        "adapters: [codex, claude]",
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
            self.assertIn("    adapters: [codex, claude]", rc_manifest)
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
            (output_root / "claude" / "CLAUDE.md").unlink()

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("missing instruction entrypoint: claude" in error for error in errors))

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
                    "adapters: [codex, claude]",
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

    def test_validate_adapters_cli_rejects_retired_repository_output(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate-adapters.py"),
                "--version",
                "v0.1.3",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing adapter directory", result.stdout)

    def test_ci_script_runs_adapter_checks_and_filters_generated_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '--quiet')
            for name in ['README.md', 'dist/adapters/example.txt']:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('before')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-m', 'Fixture')
            for name in ['README.md', 'dist/adapters/example.txt']:
                (root / name).write_text('after')
            driver = ("import json,sys; from pathlib import Path; "
                      "sys.path.insert(0,sys.argv[1]); from validation_execution import compose_mode; "
                      "print(json.dumps([dict(id=p.check_id,args=p.args,deps=p.dependencies) "
                      "for p in compose_mode('broad-smoke',Path(sys.argv[2]))]))")
            env = {k:v for k,v in os.environ.items() if not k.startswith('RIGORLOOP_CI_')
                   and k not in {'REVIEW_ARTIFACT_ROOTS','RIGORLOOP_BROAD_SMOKE_CLASSIFICATION'}}
            result = subprocess.run([sys.executable, '-c', driver, str(ROOT/'scripts'), str(root/'output')],
                                    cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            plans = {p['id']:p for p in json.loads(result.stdout)}
            self.assertEqual(plans['adapters.full_regression']['args'],
                             ['python','scripts/test-adapter-distribution.py'])
            self.assertEqual(plans['broad_smoke.adapters.build_archives']['args'],
                             ['python','scripts/build-adapters.py','--version','v0.1.3',
                              '--output-dir',str(root/'output/adapters-broad-smoke')])
            self.assertEqual(plans['broad_smoke.adapters.validate_archives']['args'],
                             ['python','scripts/validate-adapters.py','--root',
                              str(root/'output/adapters-broad-smoke'),'--version','v0.1.3'])
            self.assertIn('broad_smoke.adapters.build_archives',
                          plans['broad_smoke.adapters.validate_archives']['deps'])
            self.assertEqual(plans['current_records.validate']['args'],
                             ['python','scripts/validate-governed-lifecycle-cli.py'])




    def test_validate_release_rejects_retired_benchmark_path_options(self) -> None:
        module = load_validate_release_module()
        for option in ("--changed-path", "--changed-paths-file"):
            with self.subTest(option=option), self.assertRaises(SystemExit) as stopped:
                module.build_parser().parse_args(["--version", "v0.1.1", option, "unused"])
            self.assertEqual(stopped.exception.code, 2)








    def test_release_workflow_uses_tracked_release_notes(self) -> None:
        workflow_text = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )

        from release_coordination import validate_workflow
        self.assertEqual(validate_workflow(ROOT), [])
        provider = (ROOT / 'scripts/release_provider.py').read_text()
        self.assertIn("'--notes-file'", provider)
        self.assertIn("local_file(output, 'release-notes.md')", provider)
        self.assertNotIn('--generate-notes', provider)

    def test_release_workflow_gates_npm_publication_modes(self) -> None:
        from release_coordination import validate_workflow
        self.assertEqual(validate_workflow(ROOT), [])
        workflow_root = ROOT / '.github/workflows'
        self.assertFalse((workflow_root / 'npm.yml').exists())
        self.assertFalse((workflow_root / 'publish-npm.yml').exists())
        # Actual sealed-tarball/OIDC argv and denial cases are exercised by the
        # discovered release executor suite, not inferred from old YAML strings.

    def test_release_verify_rejects_missing_or_mismatched_trusted_commit(self) -> None:
        base_env = {
            "PATH": os.environ.get("PATH", ""),
            "GITHUB_ACTIONS": "true",
            "GITHUB_REF_NAME": "v0.4.0",
            "GITHUB_REF_TYPE": "tag",
            "RELEASE_VERIFY_DRY_RUN": "1",
        }
        missing = subprocess.run(
            ["bash", "scripts/release-verify.sh", "v0.4.0"],
            cwd=ROOT,
            env=base_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        mismatched = subprocess.run(
            ["bash", "scripts/release-verify.sh", "v0.4.0"],
            cwd=ROOT,
            env={**base_env, "RELEASE_TAG_COMMIT": "0" * 40},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("RELEASE_TAG_COMMIT", missing.stderr)
        self.assertNotEqual(mismatched.returncode, 0)
        self.assertIn("does not match checked HEAD", mismatched.stderr)

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


    def test_readme_exposes_the_current_compact_delivery_route(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        recommended = text.split("## Recommended Use", 1)[1].split("## Starting a new repository", 1)[0]

        self.assertIn(
            "proposal -> proposal-review -> design -> design-review -> plan -> delivery-review -> implement -> code-review -> verify",
            recommended,
        )
        self.assertIn("optional external integration", text)
        self.assertIn(
            "writes the final explanation only in a successful Verify report",
            text,
        )
        for retired_entrypoint in (
            "explain-change",
            "spec-review",
            "plan-review",
            "test-spec",
        ):
            self.assertNotIn(retired_entrypoint, recommended)

    def test_readme_describes_supported_invocation_and_conflict_forms(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Claude Code uses native skill slash commands", text)
        self.assertIn("--force", text)
        self.assertIn("OpenCode and `--write-state` are no longer supported", text)
        self.assertNotIn("opencode run --command", text)


    def test_public_docs_describe_adapter_support_and_generated_boundaries(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "dist/adapters/README.md": (ROOT / "dist" / "adapters" / "README.md").read_text(encoding="utf-8"),
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

    def test_public_adapter_support_surface_only_tracks_readme_and_manifest(self) -> None:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "dist/adapters/**",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        tracked = result.stdout.splitlines()

        self.assertEqual(
            tracked,
            [
                "dist/adapters/README.md",
                "dist/adapters/manifest.yaml",
            ],
        )
        self.assertFalse(any("/skills/" in path for path in tracked), tracked)
        self.assertFalse(any(path.endswith(("AGENTS.md", "CLAUDE.md")) for path in tracked), tracked)
        self.assertFalse(any("/commands/" in path for path in tracked), tracked)

    def test_public_adapter_readme_documents_archive_install_contract(self) -> None:
        text = (ROOT / "dist/adapters/README.md").read_text(encoding="utf-8")
        for required in ("skills/", "support matrix", "release archives", "rigorloop-adapter-codex-<version>.zip", "rigorloop-adapter-claude-<version>.zip", ".agents/skills/", ".claude/skills/", "--force", "--from-archive", "--dry-run", "outside skill discovery", "project `rigorloop.yaml` and `rigorloop.lock`"):
            self.assertIn(required, text)
        self.assertNotIn("rigorloop-adapter-opencode-<version>.zip", text)
        self.assertIn("Historical archives and evidence remain unchanged", text)


    def test_root_guidance_points_to_adapter_install_contract_surface(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        constitution = (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
        self.assertIn("dist/adapters/README.md", agents)
        self.assertIn("docs/design/engineering/packaging.md", agents)
        self.assertIn("docs/design/system.md", constitution)
        self.assertTrue((ROOT / "dist/adapters/README.md").is_file())


    def test_adapter_readme_records_adapter_artifact_metadata_location(self) -> None:
        text = (ROOT / "dist" / "adapters" / "README.md").read_text(encoding="utf-8")

        self.assertNotIn("docs/workflows.md", text)
        self.assertIn("Adapter artifact metadata", text)
        self.assertIn("`docs/reports/adapter-artifacts/releases/<version>.yaml`", text)
        self.assertIn("support matrix", text)


    def test_contributor_docs_keep_codex_runtime_local_and_untracked(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        }

        for path, text in docs.items():
            with self.subTest(path=path):
                self.assertIn("dist/adapters/README.md", text)
                self.assertIn("release archives", text.lower())
                self.assertIn("`.codex/skills/`", text)
                self.assertIn("untracked", text)
                self.assertNotIn(
                    "Regenerate it with `python scripts/build-skills.py` when needed.",
                    text,
                )
                self.assertNotIn("install or copy public Codex adapter output from `dist/adapters/codex/.agents/skills/`", text)
                self.assertNotIn("Do not hand-edit local Codex runtime state", text)
                self.assertNotIn("Do not hand-edit generated Codex compatibility output", text)
                self.assertNotIn("MUST NOT be hand-edited or tracked", text)

    def test_adapter_manifest_remains_metadata_only(self) -> None:
        manifest_path = ROOT / "dist" / "adapters" / "manifest.yaml"
        manifest = manifest_path.read_text(encoding="utf-8")

        self.assertIn("version:", manifest)
        self.assertIn("skills:", manifest)
        self.assertNotIn("command_aliases:", manifest)
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
