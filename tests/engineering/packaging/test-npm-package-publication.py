#!/usr/bin/env python3
"""Package policy, actual tarball and installed CLI behavior with native collection."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from npm_fixture_helpers import (
    ROOT, PACKAGE_ROOT, PACKAGE_VERSION, RELEASE_TAG, METADATA_FILE,
    TARGET_SKILL_ROOTS, run_command, pack_package, configure_npm_case,
)
from lib.packaging.npm_package_validation import (
    NpmPackageValidationError, inspect_package_tarball,
    is_forbidden_path, validate_package_policy,
)


# Packaging DIST-SR-23: public entrypoint, current Records runtime/schema/template
# and bundled installation trust. The producer/inspector inventory is observed
# separately; it must not define this expected runtime population.
EXPECTED_RUNTIME_PATHS = frozenset({
    "package/package.json", "package/README.md", "package/LICENSE",
    "package/dist/bin/rigorloop.js",
    "package/dist/lib/command-result.js",
    "package/dist/lib/installer-replacement.js",
        "package/dist/lib/operational-cli.js",
        "package/dist/lib/operational-contract.js",
        "package/dist/lib/operational-receipt.js",
        "package/dist/lib/operational-files.js",
        "package/dist/lib/operational-store.js",
        "package/dist/lib/operational-layout.js",
        "package/dist/lib/operational-rows.js",
        "package/dist/lib/operational-model.js",
        "package/dist/lib/operational-tasks.js",
        "package/dist/lib/operational-attachments.js",
        "package/dist/lib/operational-maintenance.js",
        "package/dist/lib/operational-maintenance-contract.js",
        "package/dist/lib/operational-bundle.js",
        "package/dist/lib/operational-coordination.js",
        "package/dist/lib/operational-legacy-import.js",
        "package/dist/lib/record-store-files.js",
        "package/dist/lib/workflow-package.js",
        "package/dist/lib/migrations/operational-schema-1.sql",
        "package/dist/schemas/rigorloop-records-v4.schema.json",
        "package/dist/schemas/targeted-recording-v2.schema.json",
        "package/dist/schemas/store-maintenance-v1.schema.json",
        "package/dist/templates/shared/rigorloop-workflow.json",
    "package/dist/lib/record-json.js",
    "package/dist/lib/record-format-v3.js",
    "package/dist/lib/record-format-core.js",
    "package/dist/schemas/rigorloop-records-v3.schema.json",
    "package/dist/lib/official-archive-url.js",
    "package/dist/metadata/adapter-artifacts-v0.3.4.json",
    "package/dist/metadata/releases.json",
})


def project_snapshot(root: Path) -> dict:
    """Observe all entries without following destination symlinks."""
    result = {}
    def visit(path):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(mode):
            result[relative] = (mode, os.readlink(path))
        elif stat.S_ISDIR(mode):
            result[relative] = (mode,)
            for child in sorted(path.iterdir()):
                visit(child)
        else:
            result[relative] = (mode, path.read_bytes())
    visit(root)
    return result


class NpmPackagePublicationTests(unittest.TestCase):
    def setUp(self):
        configure_npm_case(self.addCleanup)

    def test_actual_tarball_contains_required_runtime_files_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="rigorloop-npm-pack-") as temp:
            tarball = pack_package(Path(temp))
            report = inspect_package_tarball(tarball)

        self.assertEqual(EXPECTED_RUNTIME_PATHS - report.paths, frozenset(), "missing required runtime members")
        self.assertEqual(report.forbidden_paths, ())
        self.assertIn(f"package/dist/metadata/{METADATA_FILE}", report.paths)
        self.assertNotIn("package/dist/metadata/adapter-artifacts-v0.1.3.json", report.paths)

    def assert_no_state_files(self, project_root: Path) -> None:
        self.assertFalse((project_root / "rigorloop.yaml").exists())
        self.assertFalse((project_root / "rigorloop.lock").exists())

    def assert_default_target_install(self, project_root: Path, target: str) -> None:
        self.assertTrue((project_root / TARGET_SKILL_ROOTS[target]).is_dir(), target)
        if target == "codex":
            self.assertFalse((project_root / ".claude").exists())
            self.assertFalse((project_root / ".opencode").exists())
        elif target == "claude":
            self.assertFalse((project_root / ".agents").exists())
            self.assertFalse((project_root / ".opencode").exists())

    def test_packed_package_smoke_executes_installed_binary_and_real_target_init(self) -> None:
        with tempfile.TemporaryDirectory(prefix="rigorloop-npm-pack-") as pack_temp, tempfile.TemporaryDirectory(
            prefix="rigorloop-npm-install-"
        ) as install_temp, tempfile.TemporaryDirectory(prefix="rigorloop-npm-project-") as project_temp, tempfile.TemporaryDirectory(
            prefix="rigorloop-npm-release-output-"
        ) as release_temp:
            tarball = pack_package(Path(pack_temp))
            release_output = Path(release_temp)
            build_result = run_command(
                ["python", "scripts/build-adapters.py", "--version", RELEASE_TAG, "--output-dir", str(release_output)]
            )
            self.assertEqual(build_result.returncode, 0, build_result.stderr)

            install_root = Path(install_temp)
            install = run_command(["npm", "install", "--prefix", str(install_root), str(tarball)])
            self.assertEqual(install.returncode, 0, install.stderr)

            bin_path = install_root / "node_modules" / ".bin" / "rigorloop"
            self.assertTrue(bin_path.exists())
            self.assertNotEqual(bin_path.resolve(), (PACKAGE_ROOT / "dist" / "bin" / "rigorloop.js").resolve())

            help_result = run_command([str(bin_path), "--help"], cwd=Path(project_temp))
            self.assertEqual(help_result.returncode, 0, help_result.stderr)
            self.assertIn("rigorloop init codex|claude", help_result.stdout)

            version_result = run_command([str(bin_path), "version"], cwd=Path(project_temp))
            self.assertEqual(version_result.returncode, 0, version_result.stderr)
            self.assertEqual(version_result.stdout.strip(), f"@xiongxianfei/rigorloop {PACKAGE_VERSION}")

            for target in ("codex", "claude"):
                with self.subTest(target=target, mode="default"):
                    target_project = Path(project_temp) / f"default-{target}"
                    target_project.mkdir()
                    archive = release_output / f"rigorloop-adapter-{target}-{RELEASE_TAG}.zip"
                    init_result = run_command(
                        [str(bin_path), "init", target, "--from-archive", str(archive), "--json"],
                        cwd=target_project,
                    )
                    self.assertEqual(init_result.returncode, 0, init_result.stderr or init_result.stdout)
                    self.assertEqual(init_result.stderr, "")
                    init_payload = json.loads(init_result.stdout)
                    self.assertEqual(init_payload["command"], "init")
                    self.assert_default_target_install(target_project, target)
                    self.assert_no_state_files(target_project)

                with self.subTest(target=target, mode="empty-unit-default-and-force"):
                    conflict_project = Path(project_temp) / f"empty-{target}"
                    unit = conflict_project / TARGET_SKILL_ROOTS[target] / "system-design"
                    unit.mkdir(parents=True)
                    sentinels = {"rigorloop.yaml": b"preserve state\r\n",
                                 "rigorloop.lock": b"preserve lock\x00",
                                 "unrelated.txt": b"user data\n"}
                    for name, content in sentinels.items():
                        (conflict_project / name).write_bytes(content)
                    before = project_snapshot(conflict_project)
                    command = [str(bin_path), "init", target, "--from-archive", str(archive), "--json"]
                    conflict = run_command(command, cwd=conflict_project)
                    self.assertEqual(conflict.returncode, 5, conflict.stdout + conflict.stderr)
                    self.assertEqual(json.loads(conflict.stdout)["blockers"][0]["code"], "destination-conflict")
                    self.assertEqual(project_snapshot(conflict_project), before)
                    forced = run_command([*command, "--force"], cwd=conflict_project)
                    self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
                    # Compare every installed member with the actual immutable ZIP;
                    # archive inventory/parity has its separate canonical oracle.
                    prefix = TARGET_SKILL_ROOTS[target].as_posix() + "/"
                    with zipfile.ZipFile(archive) as zipped:
                        expected = {name: zipped.read(name) for name in zipped.namelist()
                                    if name.startswith(prefix) and not name.endswith("/")}
                    actual = {path.relative_to(conflict_project).as_posix(): path.read_bytes()
                              for path in (conflict_project / TARGET_SKILL_ROOTS[target]).rglob("*")
                              if path.is_file()}
                    self.assertEqual(actual, expected)
                    for name, content in sentinels.items():
                        self.assertEqual((conflict_project / name).read_bytes(), content)

                with self.subTest(target=target, mode="unsafe-unit-default-and-force"):
                    unsafe_project = Path(project_temp) / f"unsafe-{target}"
                    victim = Path(project_temp) / f"outside-{target}"
                    victim.mkdir()
                    (victim / "keep.md").write_bytes(b"outside destination\r\n")
                    unsafe_unit = unsafe_project / TARGET_SKILL_ROOTS[target] / "system-design"
                    unsafe_unit.parent.mkdir(parents=True)
                    unsafe_unit.symlink_to(victim, target_is_directory=True)
                    (unsafe_project / "rigorloop.yaml").write_bytes(b"keep state")
                    before = project_snapshot(unsafe_project)
                    victim_before = project_snapshot(victim)
                    for options in ([], ["--force"]):
                        rejected = run_command(
                            [str(bin_path), "init", target, "--from-archive", str(archive), "--json", *options],
                            cwd=unsafe_project,
                        )
                        self.assertEqual(rejected.returncode, 5, rejected.stdout + rejected.stderr)
                        self.assertEqual(json.loads(rejected.stdout)["blockers"][0]["code"], "unsafe-destination")
                        self.assertEqual(project_snapshot(unsafe_project), before)
                        self.assertEqual(project_snapshot(victim), victim_before)

                with self.subTest(target=target, mode="removed-write-state"):
                    state_project = Path(project_temp) / f"state-{target}"
                    state_project.mkdir()
                    result = run_command([str(bin_path), "init", target, "--write-state", "--force", "--json"], cwd=state_project)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assert_no_state_files(state_project)
                    self.assertFalse((state_project / TARGET_SKILL_ROOTS[target]).exists())

            new_change_result = run_command(
                [str(bin_path), "new-change", "test-change", "--title", "Test change", "--dry-run", "--json"],
                cwd=Path(project_temp),
            )
            self.assertEqual(new_change_result.returncode, 4, new_change_result.stderr)
            self.assertEqual(new_change_result.stderr, "")
            new_change_payload = json.loads(new_change_result.stdout)
            self.assertEqual(new_change_payload["errors"][0]["code"], "invalid-usage")
            self.assertFalse((Path(project_temp) / "docs/changes/test-change").exists())
            workflow = run_command(
                ["node", "--test", "--test-name-pattern=owner-selected bases", "packages/rigorloop/test/operational-review.test.js"],
                env={**os.environ, "RIGORLOOP_TEST_PACKAGED_BIN": str(bin_path)},
            )
            self.assertEqual(workflow.returncode, 0, workflow.stdout + workflow.stderr)


if __name__ == "__main__":
    unittest.main()
