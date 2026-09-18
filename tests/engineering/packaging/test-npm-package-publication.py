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
from npm_recording_tests import PackedRecordingTests


# Packaging DIST-SR-23: public entrypoint, current Records runtime/schema/template
# and bundled installation trust. The producer/inspector inventory is observed
# separately; it must not define this expected runtime population.
EXPECTED_RUNTIME_PATHS = frozenset({
    "package/package.json", "package/README.md", "package/LICENSE",
    "package/dist/bin/rigorloop.js",
    "package/dist/lib/command-result.js",
    "package/dist/lib/installer-replacement.js",
    "package/dist/lib/record-store.js",
    "package/dist/lib/record-json.js",
    "package/dist/lib/record-format-v3.js",
    "package/dist/lib/record-format-core.js",
    "package/dist/schemas/rigorloop-records-v3.schema.json",
    "package/dist/templates/rigorloop-records-v3/records.json",
    "package/dist/lib/recording-cli.js",
    "package/dist/lib/record-discovery.js",
    "package/dist/lib/record-store-transport.js",
    "package/dist/schemas/targeted-recording-v1.schema.json",
    "package/dist/schemas/record-store-transport.schema.json",
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

    def test_publication_validation_step_supports_selected_tag_layouts(self):
        # Execute the actual workflow step, without publication or remote services.
        parser = "const fs=require('fs'),YAML=require('yaml'); console.log(JSON.stringify(YAML.parse(fs.readFileSync(process.argv[1],'utf8'),{uniqueKeys:true})))"
        parsed = run_command(['node', '-e', parser, str(ROOT / '.github/workflows/publish-github-packages.yml')], cwd=PACKAGE_ROOT)
        self.assertEqual(parsed.returncode, 0, parsed.stderr)
        steps = json.loads(parsed.stdout)['jobs']['publish']['steps']
        command = next(step['run'] for step in steps if step.get('name') == 'Verify package before publication')
        current = 'tests/engineering/packaging/test-npm-package-publication.py'
        historical = 'scripts/test-npm-package-publication.py'
        scenarios = (
            ('current', {current: ('current', 0)}, 0, 'current'),
            ('historical', {historical: ('historical', 0)}, 0, 'historical'),
            ('both', {current: ('current', 0), historical: ('historical', 0)}, 0, 'current'),
            ('missing', {}, None, ''),
            ('failure', {current: ('current', 7)}, 7, 'current'),
        )
        for name, files, expected_code, expected_output in scenarios:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                for relative, (marker, code) in files.items():
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(f'print({marker!r})\nraise SystemExit({code})\n')
                result = run_command(['bash', '-e', '-c', command], cwd=root)
                if expected_code is None:
                    self.assertNotEqual(result.returncode, 0)
                else:
                    self.assertEqual(result.returncode, expected_code, result.stderr)
                self.assertEqual(result.stdout.strip(), expected_output)

    def test_package_policy_rejects_lifecycle_scripts_and_runtime_dependencies(self) -> None:
        validate_package_policy(
            {
                "name": "@xiongxianfei/rigorloop",
                "version": PACKAGE_VERSION,
                "bin": {"rigorloop": "dist/bin/rigorloop.js"},
                "files": ["dist/", "package.json", "README.md", "LICENSE"],
                "scripts": {"test": "node --test"},
                "dependencies": {"yaml": "2.9.0"},
                "license": "MIT",
            }
        )

        for script_name in ("preinstall", "install", "postinstall", "prepare", "prepack"):
            with self.subTest(script=script_name):
                with self.assertRaisesRegex(NpmPackageValidationError, script_name):
                    validate_package_policy({"scripts": {script_name: "echo unsafe"}})

        self.assertIsNone(validate_package_policy({"dependencies": {"yaml": "2.9.0"}}))
        with self.assertRaisesRegex(NpmPackageValidationError, "unapproved runtime dependency"):
            validate_package_policy({"dependencies": {"left-pad": "1.3.0"}})
        with self.assertRaisesRegex(NpmPackageValidationError, "unapproved runtime dependency"):
            validate_package_policy({"dependencies": {"yaml": "2.8.1"}})

    def test_forbidden_path_detection_rejects_root_and_nested_sensitive_files(self) -> None:
        forbidden_paths = [
            "package/dist/lib/compact-operations.js",
            "package/dist/lib/lifecycle-read.js",
            "package/dist/lib/new-change.js",
            "package/dist/lib/final-verification-protocol.js",
            "package/dist/schemas/explicit-recording-v1.schema.json",
            "package/dist/templates/explicit-recording/records.json",
            "package/dist/metadata/compact-current-state-activation.json",
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

        self.assertEqual(EXPECTED_RUNTIME_PATHS - report.paths, frozenset(), "missing required runtime members")
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
                        for name in sorted(EXPECTED_RUNTIME_PATHS | {forbidden_path}):
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
                    unit = conflict_project / TARGET_SKILL_ROOTS[target] / "design"
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
                    unsafe_unit = unsafe_project / TARGET_SKILL_ROOTS[target] / "design"
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
                ["node", "--test", "--test-name-pattern=TG-05 actors", "packages/rigorloop/test/record-store-workflow.test.js"],
                env={**os.environ, "RIGORLOOP_TEST_PACKAGED_BIN": str(bin_path)},
            )
            self.assertEqual(workflow.returncode, 0, workflow.stdout + workflow.stderr)

    def test_packed_package_observability_surface_matches_documentation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="rigorloop-npm-pack-") as pack_temp, tempfile.TemporaryDirectory(
            prefix="rigorloop-npm-install-"
        ) as install_temp, tempfile.TemporaryDirectory(prefix="rigorloop-npm-observability-") as project_temp, tempfile.TemporaryDirectory(
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
            package_root = install_root / "node_modules" / "@xiongxianfei" / "rigorloop"
            project_root = Path(project_temp)
            log_root = project_root / "logs"
            archive = release_output / f"rigorloop-adapter-codex-{RELEASE_TAG}.zip"
            command_env = {**os.environ, "RIGORLOOP_LOG_DIR": str(log_root)}

            concise = run_command(
                [str(bin_path), "init", "codex", "--from-archive", str(archive), "--dry-run", "--format", "concise-json"],
                cwd=project_root,
                env=command_env,
            )
            self.assertEqual(concise.returncode, 0, concise.stderr or concise.stdout)
            self.assertEqual(concise.stderr, "")
            concise_payload = json.loads(concise.stdout)
            self.assertEqual(concise_payload["projection"], "concise")
            self.assertEqual(concise_payload["observability"], "recorded")
            invocation_id = concise_payload["invocation_id"]

            path_result = run_command([str(bin_path), "logs", "path"], cwd=project_root, env=command_env)
            self.assertEqual(path_result.returncode, 0, path_result.stderr)
            self.assertEqual(Path(path_result.stdout.strip()), log_root)

            show_result = run_command(
                [str(bin_path), "logs", "show", invocation_id, "--format", "json"], cwd=project_root, env=command_env
            )
            self.assertEqual(show_result.returncode, 0, show_result.stderr or show_result.stdout)
            show_payload = json.loads(show_result.stdout)
            self.assertEqual(show_payload["status"], "success")
            self.assertEqual({event["event"] for event in show_payload["events"]}, {"invocation-start", "invocation-complete"})

            concise_human = run_command(
                [
                    str(bin_path),
                    "init",
                    "codex",
                    "--from-archive",
                    str(archive),
                    "--dry-run",
                    "--format",
                    "concise-human",
                    "--no-file-log",
                    "--console-log-level",
                    "off",
                ],
                cwd=project_root,
                env=command_env,
            )
            self.assertEqual(concise_human.returncode, 0, concise_human.stderr or concise_human.stdout)
            self.assertEqual(concise_human.stderr, "")
            self.assertLessEqual(len([line for line in concise_human.stdout.splitlines() if line.strip()]), 2)

            detailed = run_command(
                [
                    str(bin_path),
                    "init",
                    "codex",
                    "--from-archive",
                    str(archive),
                    "--dry-run",
                    "--format",
                    "detailed-json",
                    "--no-file-log",
                ],
                cwd=project_root,
                env=command_env,
            )
            self.assertEqual(detailed.returncode, 0, detailed.stderr or detailed.stdout)
            self.assertEqual(json.loads(detailed.stdout)["command"], "init")

            legacy = run_command(
                [str(bin_path), "init", "codex", "--from-archive", str(archive), "--dry-run", "--json", "--no-file-log"],
                cwd=project_root,
                env=command_env,
            )
            self.assertEqual(legacy.returncode, 0, legacy.stderr or legacy.stdout)
            self.assertEqual(json.loads(legacy.stdout)["command"], "init")

            readme = (package_root / "README.md").read_text(encoding="utf-8")
            for documented_surface in (
                "rigorloop logs path",
                "rigorloop logs show <invocation-id>",
                "--no-file-log",
                "--console-log-level debug|info|warning|error|off",
                "--format concise-json",
                "--format concise-human",
                "--format detailed-json",
            ):
                with self.subTest(documented_surface=documented_surface):
                    self.assertIn(documented_surface, readme)


if __name__ == "__main__":
    unittest.main()
