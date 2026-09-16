"""Cheap release preflight, explicit failures and real Git state."""

from __future__ import annotations

import sys
from pathlib import Path
import shutil
import tempfile
import unittest
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import release_preflight
from release_fixture_helpers import (PROFILE_FIXTURES, assert_errors_contain, init_release_git_fixture, make_prepared_release, relative_file_texts)


class ReleasePreflightTests(unittest.TestCase):
    maxDiff = None

    def test_release_preflight_clean_fixture_is_idempotent_and_side_effect_light(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            before = relative_file_texts(root)

            first = release_preflight("v0.3.5", root=root)
            second = release_preflight("v0.3.5", root=root)
            after = relative_file_texts(root)

        self.assertEqual(first.errors, ())
        self.assertEqual(second.errors, ())
        self.assertEqual(before, after)
        self.assertEqual(first.external_actions, ())

    def test_release_preflight_cli_succeeds_on_clean_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            init_release_git_fixture(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "release-preflight.py"),
                    "v0.3.5",
                    "--root",
                    str(root),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("release-preflight v0.3.5: pass", result.stdout)
        self.assertIn("release preflight changed-file source: git", result.stdout)

    def test_release_preflight_cli_requires_changed_file_or_git_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "release-preflight.py"),
                    "v0.3.5",
                    "--root",
                    str(root),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("could not derive changed files", result.stdout)

    def test_release_preflight_fails_missing_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = release_preflight("v0.3.5", root=Path(tmp))

        self.assertTrue(any("release profile not found" in error for error in result.errors), result.errors)

    def test_release_preflight_rejects_malformed_profile(self) -> None:
        def mutate(root: Path) -> None:
            profile = root / "docs" / "releases" / "profiles" / "v0.3.5.yaml"
            profile.write_text(
                "schema_version: release-profile-v1\n"
                "release_tag: v0.3.5\n"
                "  package_version: 0.3.5\n",
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (mutate)(root)
            result = release_preflight("v0.3.5", root=root)
        assert_errors_contain(self, result.errors, 'release profile', 'parse')

    def test_release_preflight_rejects_incomplete_profile(self) -> None:
        def mutate(root: Path) -> None:
            profile = root / "docs" / "releases" / "profiles" / "v0.3.5.yaml"
            shutil.copy2(PROFILE_FIXTURES / "invalid-missing-validation.yaml", profile)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (mutate)(root)
            result = release_preflight("v0.3.5", root=root)
        assert_errors_contain(self, result.errors, 'missing required field', 'validation')

    def test_release_preflight_rejects_missing_required_local_input(self) -> None:
        def mutate(root: Path) -> None:
            metadata = root / "packages" / "rigorloop" / "dist" / "metadata" / "releases.json"
            metadata.unlink()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (mutate)(root)
            result = release_preflight("v0.3.5", root=root)
        assert_errors_contain(self, result.errors, 'packages/rigorloop/dist/metadata/releases.json', 'missing required local input')

    def test_release_preflight_fails_package_profile_version_mismatch(self) -> None:
        def mutate(root: Path) -> None:
            package_json = root / "packages" / "rigorloop" / "package.json"
            data = json.loads(package_json.read_text(encoding="utf-8"))
            data["version"] = "0.3.4"
            package_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (mutate)(root)
            result = release_preflight("v0.3.5", root=root)
        assert_errors_contain(self, result.errors, 'package version', '0.3.4', '0.3.5')

    def test_release_preflight_fails_stale_metadata_pointer(self) -> None:
        def mutate(root: Path) -> None:
            releases_json = root / "packages" / "rigorloop" / "dist" / "metadata" / "releases.json"
            data = json.loads(releases_json.read_text(encoding="utf-8"))
            data["releases"]["v0.3.5"]["bundled_metadata"] = "adapter-artifacts-v0.3.4.json"
            releases_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (mutate)(root)
            result = release_preflight("v0.3.5", root=root)
        assert_errors_contain(self, result.errors, 'metadata pointer', 'adapter-artifacts-v0.3.4.json', 'adapter-artifacts-v0.3.5.json')

    def test_release_preflight_fails_invalid_pending_evidence_shape(self) -> None:
        def mutate(root: Path) -> None:
            npm_publication = root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"
            text = npm_publication.read_text(encoding="utf-8")
            npm_publication.write_text(
                text.replace('    result: "pending-publication"\n', '    result: "published"\n', 1),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (mutate)(root)
            result = release_preflight("v0.3.5", root=root)
        assert_errors_contain(self, result.errors, 'codex', 'result', 'pending-publication')

    def test_release_preflight_fails_dirty_release_output(self) -> None:
        def mutate(root: Path) -> None:
            output = root / "release-output"
            output.mkdir()
            (output / "leftover.txt").write_text("stale\n", encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (mutate)(root)
            result = release_preflight("v0.3.5", root=root)
        assert_errors_contain(self, result.errors, 'release-output', 'not clean')

    def test_release_preflight_fails_changed_unauthorized_literal(self) -> None:
        def mutate(root: Path) -> None:
            baseline = root / "docs" / "changes" / "2026-06-29-release-transaction-automation" / "release-literal-audit-baseline.yaml"
            baseline.parent.mkdir(parents=True)
            baseline.write_text(
                "schema_version: release-literal-audit-baseline-v1\n"
                "change_id: 2026-06-29-release-transaction-automation\n"
                "audited_release_tag: v0.3.5\n"
                "release_profile: docs/releases/profiles/v0.3.5.yaml\n"
                "\n"
                "entries:\n"
                "  - id: literal-baseline-001\n"
                "    literal: v0.3.5\n"
                "    file: scripts/new_release_state.py\n"
                "    line: 1\n"
                "    classification: unauthorized\n"
                "    expected_owner: release-profile\n"
                "    disposition: must-fix\n",
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            mutate(root)

            result = release_preflight(
                "v0.3.5",
                root=root,
                changed_files=("scripts/new_release_state.py",),
            )

        self.assertTrue(any("unauthorized changed literal" in error for error in result.errors), result.errors)

    def test_release_preflight_cli_discovers_changed_unauthorized_literal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            init_release_git_fixture(root)
            changed_file = root / "scripts" / "new_release_state.py"
            changed_file.parent.mkdir(parents=True, exist_ok=True)
            changed_file.write_text('CURRENT_RELEASE = "v0.3.5"\n', encoding="utf-8")
            baseline = root / "docs" / "changes" / "2026-06-29-release-transaction-automation" / "release-literal-audit-baseline.yaml"
            baseline.parent.mkdir(parents=True, exist_ok=True)
            baseline.write_text(
                "schema_version: release-literal-audit-baseline-v1\n"
                "change_id: 2026-06-29-release-transaction-automation\n"
                "audited_release_tag: v0.3.5\n"
                "release_profile: docs/releases/profiles/v0.3.5.yaml\n"
                "\n"
                "entries:\n"
                "  - id: literal-baseline-001\n"
                "    literal: v0.3.5\n"
                "    file: scripts/new_release_state.py\n"
                "    line: 1\n"
                "    classification: unauthorized\n"
                "    expected_owner: release-profile\n"
                "    disposition: must-fix\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "release-preflight.py"),
                    "v0.3.5",
                    "--root",
                    str(root),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        output = result.stderr + result.stdout
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn("release preflight changed-file source: git", result.stdout)
        self.assertIn("scripts/new_release_state.py", output)
        self.assertIn("unauthorized changed literal", output)
        self.assertIn("v0.3.5", output)

    def test_release_preflight_fails_local_tag_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "tag", "v0.3.5"], cwd=root, check=True)

            result = release_preflight("v0.3.5", root=root)

        self.assertTrue(any("local tag conflict" in error and "v0.3.5" in error for error in result.errors), result.errors)

    def test_release_preflight_reports_unreachable_remote_tag_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "remote", "add", "origin", str(root / "missing-remote.git")], cwd=root, check=True)

            result = release_preflight("v0.3.5", root=root)

        self.assertFalse(any("remote tag conflict" in error for error in result.errors), result.errors)
        self.assertTrue(any("remote tag state unreachable" in warning for warning in result.warnings), result.warnings)

    def test_release_preflight_fails_reachable_remote_tag_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            root = fixture / "repo"
            remote = fixture / "remote.git"
            root.mkdir()
            make_prepared_release(root)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=root, check=True)
            subprocess.run(["git", "tag", "v0.3.5"], cwd=root, check=True)
            subprocess.run(["git", "push", "origin", "v0.3.5"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "tag", "-d", "v0.3.5"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            result = release_preflight("v0.3.5", root=root)

        self.assertTrue(any("remote tag conflict" in error and "v0.3.5" in error for error in result.errors), result.errors)
