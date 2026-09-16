"""Actual clean installations and negative installed-resource observations."""

from __future__ import annotations

import sys
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging.adapter_distribution import ADAPTERS, adapter_archive_name, build_adapter_archives, validate_clean_install_smoke
from adapter_fixture_helpers import (configure_adapter_case, clean_install_runner_with_resource_mutation, copy_fixture_skills)


class AdapterInstallTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        configure_adapter_case(self.addCleanup)

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
            self.assertFalse(output_dir.exists())
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
                    self.assertEqual(errors, [expected])
                    self.assertFalse(output_dir.exists())

    def test_validate_adapters_cli_rejects_mixed_unknown_skill_selection(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            version = "v0.3.6"
            self.assertFalse(output_dir.exists())

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
        self.assertNotIn("clean-install archive missing", result.stdout)

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

    def test_clean_install_smoke_installs_mapped_resources_from_local_archives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-with-assets",))
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

    def test_clean_install_smoke_rejects_non_installing_command_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-with-assets",))
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
            skills_root = copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)

            errors = validate_clean_install_smoke(
                "v0.3.4",
                output_dir,
                skills_root=skills_root,
                skill_names=("portable-with-assets",),
                command_runner=clean_install_runner_with_resource_mutation(
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
            skills_root = copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)

            errors = validate_clean_install_smoke(
                "v0.3.4",
                output_dir,
                skills_root=skills_root,
                skill_names=("portable-with-assets",),
                command_runner=clean_install_runner_with_resource_mutation(
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
            skills_root = copy_fixture_skills(root, ("portable-with-assets",))
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
