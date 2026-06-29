#!/usr/bin/env python3
"""Tests for the RigorLoop npm package publication boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from npm_package_validation import (  # noqa: E402
    FORBIDDEN_PATH_PATTERNS,
    REQUIRED_PACKAGE_PATHS,
    NpmPackageValidationError,
    inspect_package_tarball,
    is_forbidden_path,
    validate_package_policy,
)

PACKAGE_ROOT = ROOT / "packages" / "rigorloop"
PACKAGE_VERSION = "0.3.4"
RELEASE_TAG = f"v{PACKAGE_VERSION}"
METADATA_FILE = f"adapter-artifacts-{RELEASE_TAG}.json"
TARGET_SKILL_ROOTS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
    "opencode": Path(".opencode/skills"),
}


def run_command(args: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


def pack_package(destination: Path) -> Path:
    result = run_command(
        ["npm", "pack", "--json", "--prefix", str(PACKAGE_ROOT), "--pack-destination", str(destination), str(PACKAGE_ROOT)]
    )
    if result.returncode != 0:
        raise AssertionError(f"npm pack failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    payload = json.loads(result.stdout)
    filename = payload[0]["filename"]
    return destination / filename


class NpmPackagePublicationTests(unittest.TestCase):
    def test_package_policy_rejects_lifecycle_scripts_and_runtime_dependencies(self) -> None:
        validate_package_policy(
            {
                "name": "@xiongxianfei/rigorloop",
                "version": PACKAGE_VERSION,
                "bin": {"rigorloop": "dist/bin/rigorloop.js"},
                "files": ["dist/", "package.json", "README.md", "LICENSE"],
                "scripts": {"test": "node --test"},
                "license": "MIT",
            }
        )

        for script_name in ("preinstall", "install", "postinstall", "prepare", "prepack"):
            with self.subTest(script=script_name):
                with self.assertRaisesRegex(NpmPackageValidationError, script_name):
                    validate_package_policy({"scripts": {script_name: "echo unsafe"}})

        with self.assertRaisesRegex(NpmPackageValidationError, "runtime dependencies"):
            validate_package_policy({"dependencies": {"left-pad": "1.3.0"}})

    def test_forbidden_path_patterns_are_explicit(self) -> None:
        self.assertIn("package/dist/adapters/**", FORBIDDEN_PATH_PATTERNS)
        self.assertIn("package/**/*.zip", FORBIDDEN_PATH_PATTERNS)
        self.assertIn("package/.codex/**", FORBIDDEN_PATH_PATTERNS)
        self.assertIn("package/.agents/**", FORBIDDEN_PATH_PATTERNS)
        self.assertIn("package/**/*.env", FORBIDDEN_PATH_PATTERNS)

    def test_forbidden_path_detection_rejects_root_and_nested_sensitive_files(self) -> None:
        forbidden_paths = [
            "package/rigorloop-adapter-codex-v0.2.0.zip",
            "package/archive.tgz",
            "package/.env",
            "package/secret.pem",
            "package/secret.key",
            "package/assets/rigorloop-adapter-codex-v0.2.0.zip",
            "package/tmp/archive.tgz",
            "package/config/.env",
            "package/secrets/secret.pem",
            "package/secrets/secret.key",
            "package/dist/adapters/codex/skills/proposal/SKILL.md",
            "package/.codex/skills/proposal/SKILL.md",
            "package/.agents/skills/proposal/SKILL.md",
        ]
        for path in forbidden_paths:
            with self.subTest(path=path):
                self.assertTrue(is_forbidden_path(path))

        allowed_paths = [
            "package/package.json",
            "package/README.md",
            "package/LICENSE",
            "package/dist/bin/rigorloop.js",
            "package/dist/lib/some-runtime-file.js",
            f"package/dist/metadata/{METADATA_FILE}",
        ]
        for path in allowed_paths:
            with self.subTest(path=path):
                self.assertFalse(is_forbidden_path(path))

    def test_actual_tarball_contains_required_runtime_files_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="rigorloop-npm-pack-") as temp:
            tarball = pack_package(Path(temp))
            report = inspect_package_tarball(tarball)

        self.assertTrue(REQUIRED_PACKAGE_PATHS.issubset(report.paths))
        self.assertEqual(report.forbidden_paths, ())
        self.assertIn(f"package/dist/metadata/{METADATA_FILE}", report.paths)
        self.assertNotIn("package/dist/metadata/adapter-artifacts-v0.1.3.json", report.paths)

    def test_inspector_rejects_forbidden_paths(self) -> None:
        cases = [
            "package/rigorloop-adapter-codex-v0.2.0.zip",
            "package/archive.tgz",
            "package/.env",
            "package/secret.pem",
            "package/secret.key",
            "package/assets/rigorloop-adapter-codex-v0.2.0.zip",
            "package/tmp/archive.tgz",
            "package/config/.env",
            "package/secrets/secret.pem",
            "package/secrets/secret.key",
            "package/dist/adapters/codex/skills/proposal/SKILL.md",
        ]
        for forbidden_path in cases:
            with self.subTest(path=forbidden_path):
                with tempfile.TemporaryDirectory(prefix="rigorloop-npm-forbidden-") as temp:
                    tarball = Path(temp) / "fixture.tgz"
                    with tarfile.open(tarball, "w:gz") as archive:
                        for name in sorted(REQUIRED_PACKAGE_PATHS | {forbidden_path}):
                            info = tarfile.TarInfo(name)
                            info.size = 0
                            archive.addfile(info)

                    with self.assertRaisesRegex(NpmPackageValidationError, "forbidden"):
                        inspect_package_tarball(tarball)

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
        elif target == "opencode":
            self.assertFalse((project_root / ".agents").exists())
            self.assertFalse((project_root / ".claude").exists())

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
            self.assertIn("rigorloop init codex|claude|opencode", help_result.stdout)

            version_result = run_command([str(bin_path), "version"], cwd=Path(project_temp))
            self.assertEqual(version_result.returncode, 0, version_result.stderr)
            self.assertEqual(version_result.stdout.strip(), f"@xiongxianfei/rigorloop {PACKAGE_VERSION}")

            for target in ("codex", "claude", "opencode"):
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

                with self.subTest(target=target, mode="write-state"):
                    state_project = Path(project_temp) / f"state-{target}"
                    state_project.mkdir()
                    archive = release_output / f"rigorloop-adapter-{target}-{RELEASE_TAG}.zip"
                    init_result = run_command(
                        [str(bin_path), "init", target, "--write-state", "--from-archive", str(archive), "--json"],
                        cwd=state_project,
                    )
                    self.assertEqual(init_result.returncode, 0, init_result.stderr or init_result.stdout)
                    self.assertEqual(init_result.stderr, "")
                    init_payload = json.loads(init_result.stdout)
                    self.assertEqual(init_payload["command"], "init")
                    self.assert_default_target_install(state_project, target)
                    self.assertTrue((state_project / "rigorloop.yaml").is_file())
                    self.assertTrue((state_project / "rigorloop.lock").is_file())

            new_change_result = run_command(
                [str(bin_path), "new-change", "test-change", "--title", "Test change", "--dry-run", "--json"],
                cwd=Path(project_temp),
            )
            self.assertEqual(new_change_result.returncode, 0, new_change_result.stderr)
            self.assertEqual(new_change_result.stderr, "")
            new_change_payload = json.loads(new_change_result.stdout)
            self.assertEqual(new_change_payload["command"], "new-change")


if __name__ == "__main__":
    unittest.main()
