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
CHANGE_ROOT = ROOT / "docs" / "changes" / "2026-06-29-release-transaction-automation"
sys.path.insert(0, str(ROOT / "scripts"))

from release_transaction import (  # noqa: E402
    ReleaseProfileError,
    is_routine_release_profile,
    load_literal_audit_baseline_file,
    load_release_profile,
    load_release_profile_file,
    load_surface_inventory_file,
    profile_path_for_tag,
)

REQUIRED_PROFILE_FIELD_CASES = (
    ("invalid-missing-release-tag.yaml", "release_tag"),
    ("invalid-missing-package-version.yaml", "package_version"),
    ("invalid-missing-npm-package.yaml", "npm_package"),
    ("invalid-missing-targets.yaml", "targets"),
    ("invalid-missing-adapter-artifacts.yaml", "adapter_artifacts"),
    ("invalid-missing-publication.yaml", "publication"),
    ("invalid-missing-evidence.yaml", "evidence"),
    ("invalid-missing-validation.yaml", "validation"),
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

    def test_missing_profile_path_fails_with_named_path(self) -> None:
        missing_path = self.profile_fixture("does-not-exist.yaml")

        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(missing_path)

        self.assertIn("release profile not found", "\n".join(raised.exception.errors))
        self.assertIn("does-not-exist.yaml", str(raised.exception))

    def test_missing_required_profile_fields_fail_with_named_field(self) -> None:
        for fixture_name, field_name in REQUIRED_PROFILE_FIELD_CASES:
            with self.subTest(field=field_name):
                self.assert_profile_error(
                    fixture_name,
                    f"release profile missing required field: {field_name}",
                )

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


class ReleaseSurfaceInventoryTests(unittest.TestCase):
    maxDiff = None

    def fixture(self, name: str) -> Path:
        return FIXTURES / "surface-inventory" / name

    def test_valid_surface_inventory_classifies_release_surfaces(self) -> None:
        inventory = load_surface_inventory_file(self.fixture("valid-inventory.yaml"))

        classifications = {surface["id"]: surface["classification"] for surface in inventory.surfaces}

        self.assertEqual(classifications["release-metadata"], "profile-owned-generated")
        self.assertEqual(classifications["release-notes-narrative"], "human-authored-profile-checked")
        self.assertEqual(classifications["prior-release-evidence"], "historical-immutable")

    def test_unknown_surface_classification_fails_closed(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_surface_inventory_file(self.fixture("invalid-unknown-classification.yaml"))

        self.assertIn("unknown surface classification: generated", "\n".join(raised.exception.errors))

    def test_manual_override_without_rationale_fails(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_surface_inventory_file(self.fixture("invalid-manual-override-without-rationale.yaml"))

        self.assertIn(
            "manual override requires rationale: release-metadata",
            "\n".join(raised.exception.errors),
        )

    def test_change_local_surface_inventory_artifact_loads(self) -> None:
        inventory = load_surface_inventory_file(CHANGE_ROOT / "release-surface-inventory.yaml")

        surface_ids = {surface["id"] for surface in inventory.surfaces}
        self.assertIn("release-metadata", surface_ids)
        self.assertIn("release-notes-narrative", surface_ids)
        self.assertIn("prior-release-evidence", surface_ids)


class LiteralAuditBaselineTests(unittest.TestCase):
    maxDiff = None

    def fixture(self, name: str) -> Path:
        return FIXTURES / "literal-audit" / name

    def test_valid_literal_audit_baseline_reports_baseline_drift(self) -> None:
        baseline = load_literal_audit_baseline_file(self.fixture("valid-baseline.yaml"))

        self.assertEqual(baseline.schema_version, "release-literal-audit-baseline-v1")
        self.assertEqual(len(baseline.entries), 3)
        self.assertEqual(
            baseline.warnings,
            (
                (
                    "literal audit report-only: literal=v0.3.4 file=scripts/stale.py "
                    "classification=baseline-drift expected_owner=release-profile"
                ),
            ),
        )

    def test_literal_audit_unknown_classification_fails_closed(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(self.fixture("invalid-unknown-classification.yaml"))

        self.assertIn("unknown literal classification: stale-current", "\n".join(raised.exception.errors))

    def test_changed_unauthorized_current_literal_fails(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(
                self.fixture("unauthorized-new-literal.yaml"),
                changed_files=("scripts/new_release_state.py",),
            )

        self.assertIn(
            (
                "unauthorized changed literal: literal=v0.3.5 file=scripts/new_release_state.py "
                "classification=unauthorized expected_owner=release-profile"
            ),
            "\n".join(raised.exception.errors),
        )

    def test_historical_literal_requires_rationale(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(self.fixture("historical-fixture-without-rationale.yaml"))

        self.assertIn(
            "historical fixture requires rationale: literal=v0.3.4 file=tests/history.py",
            "\n".join(raised.exception.errors),
        )

    def test_generated_current_literal_requires_profile_or_generated_region_owner(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(self.fixture("generated-current-without-owner.yaml"))

        self.assertIn(
            "generated-current literal requires release_profile or generated_region owner",
            "\n".join(raised.exception.errors),
        )

    def test_change_local_literal_audit_baseline_artifact_loads(self) -> None:
        baseline = load_literal_audit_baseline_file(
            CHANGE_ROOT / "release-literal-audit-baseline.yaml"
        )

        self.assertEqual(baseline.change_id, "2026-06-29-release-transaction-automation")
        self.assertEqual(baseline.audited_release_tag, "v0.3.5")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
