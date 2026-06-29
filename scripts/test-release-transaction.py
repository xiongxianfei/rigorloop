#!/usr/bin/env python3
"""Focused tests for release transaction automation helpers."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "release-transaction"
PROFILE_FIXTURES = FIXTURES / "profiles"
sys.path.insert(0, str(ROOT / "scripts"))

from release_transaction import (  # noqa: E402
    ReleaseProfileError,
    is_routine_release_profile,
    load_release_profile,
    load_release_profile_file,
    profile_path_for_tag,
)


class ReleaseProfileTests(unittest.TestCase):
    maxDiff = None

    def profile_fixture(self, name: str) -> Path:
        return PROFILE_FIXTURES / name

    def assert_profile_error(self, fixture_name: str, expected: str) -> ReleaseProfileError:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(self.profile_fixture(fixture_name))
        self.assertIn(expected, "\n".join(raised.exception.errors))
        return raised.exception

    def test_valid_routine_profile_loads_source_of_truth_fields(self) -> None:
        profile = load_release_profile_file(self.profile_fixture("valid-routine-v0.3.5.yaml"))

        self.assertEqual(profile.schema_version, "release-profile-v1")
        self.assertEqual(profile.release_kind, "routine")
        self.assertEqual(profile.release_tag, "v0.3.5")
        self.assertEqual(profile.package_version, "0.3.5")
        self.assertEqual(profile.npm_package, "@xiongxianfei/rigorloop")
        self.assertEqual(profile.targets, ("codex", "claude", "opencode"))
        self.assertTrue(profile.adapter_artifacts["required"])
        self.assertEqual(
            profile.adapter_artifacts["metadata_file"],
            "adapter-artifacts-v0.3.5.json",
        )
        self.assertEqual(profile.adapter_artifacts["archive_version"], "v0.3.5")
        self.assertEqual(profile.publication["github_release_required"], True)
        self.assertEqual(profile.evidence["timing"], "required")
        self.assertEqual(profile.validation["local_release_verify_required"], True)
        self.assertTrue(is_routine_release_profile(profile))

    def test_profile_path_for_tag_uses_docs_release_profiles(self) -> None:
        self.assertEqual(
            profile_path_for_tag("v0.3.5", root=ROOT),
            ROOT / "docs" / "releases" / "profiles" / "v0.3.5.yaml",
        )

    def test_load_release_profile_reads_docs_release_profiles_by_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile_dir = root / "docs" / "releases" / "profiles"
            profile_dir.mkdir(parents=True)
            shutil.copy2(
                self.profile_fixture("valid-routine-v0.3.5.yaml"),
                profile_dir / "v0.3.5.yaml",
            )

            profile = load_release_profile("v0.3.5", root=root)

        self.assertEqual(profile.path, profile_dir / "v0.3.5.yaml")
        self.assertEqual(profile.release_tag, "v0.3.5")

    def test_missing_targets_fail_with_named_field(self) -> None:
        self.assert_profile_error("invalid-missing-targets.yaml", "missing required field: targets")

    def test_malformed_profile_fails_with_path_context(self) -> None:
        error = self.assert_profile_error("invalid-malformed.yaml", "could not parse release profile")
        self.assertIn("invalid-malformed.yaml", str(error))

    def test_package_version_must_match_release_tag(self) -> None:
        self.assert_profile_error(
            "invalid-wrong-package-version.yaml",
            "package_version 0.3.6 does not match release_tag v0.3.5",
        )

    def test_unknown_release_kind_fails_closed_before_consistency(self) -> None:
        error = self.assert_profile_error(
            "invalid-unknown-release-kind.yaml",
            "unknown release_kind: preview",
        )
        self.assertTrue(error.errors[0].endswith("unknown release_kind: preview"))

    def test_unknown_target_fails_closed_before_consistency(self) -> None:
        error = self.assert_profile_error(
            "invalid-unknown-target.yaml",
            "unknown target: cursor",
        )
        self.assertTrue(error.errors[0].endswith("unknown target: cursor"))

    def test_special_release_without_owner_decision_fails(self) -> None:
        self.assert_profile_error(
            "invalid-special-release-without-rationale.yaml",
            "special release requires owner_decision",
        )

    def test_special_release_with_owner_decision_is_not_routine(self) -> None:
        profile = load_release_profile_file(self.profile_fixture("special-release-with-rationale.yaml"))

        self.assertEqual(profile.release_kind, "special")
        self.assertEqual(profile.owner_decision, "Fixture owner decision for a special release path.")
        self.assertFalse(is_routine_release_profile(profile))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
