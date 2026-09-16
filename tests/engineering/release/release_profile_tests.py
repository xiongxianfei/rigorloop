"""Supported profiles, surface ownership and literal classification."""

from __future__ import annotations

import sys
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import ReleaseProfileError, is_routine_release_profile, load_literal_audit_baseline_file, load_release_profile, load_release_profile_file, load_surface_inventory_file, profile_path_for_tag
from release_fixture_helpers import (CHANGE_ROOT, REQUIRED_PROFILE_FIELD_CASES, literal_audit_fixture, profile_fixture, surface_inventory_fixture)


class ReleaseProfileTests(unittest.TestCase):
    maxDiff = None

    def test_valid_routine_profile_loads_source_of_truth_fields(self) -> None:
        profile = load_release_profile_file(profile_fixture("valid-routine-v0.3.5.yaml"))

        self.assertEqual(profile.schema_version, "release-profile-v1")
        self.assertEqual(profile.release_kind, "routine")
        self.assertEqual(profile.release_tag, "v0.3.5")
        self.assertEqual(profile.package_version, "0.3.5")
        self.assertEqual(profile.npm_dist_tag, "latest")
        self.assertEqual(profile.npm_package, "@xiongxianfei/rigorloop")
        self.assertEqual(profile.targets, ("codex", "claude"))
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
                profile_fixture("valid-routine-v0.3.5.yaml"),
                profile_dir / "v0.3.5.yaml",
            )

            profile = load_release_profile("v0.3.5", root=root)

        self.assertEqual(profile.path, profile_dir / "v0.3.5.yaml")
        self.assertEqual(profile.release_tag, "v0.3.5")

    def test_missing_profile_path_fails_with_named_path(self) -> None:
        missing_path = profile_fixture("does-not-exist.yaml")

        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(missing_path)

        self.assertIn("release profile not found", "\n".join(raised.exception.errors))
        self.assertIn("does-not-exist.yaml", str(raised.exception))

    def test_missing_required_profile_fields_fail_with_named_field(self) -> None:
        for fixture_name, field_name in REQUIRED_PROFILE_FIELD_CASES:
            with self.subTest(field=field_name):
                with self.assertRaises(ReleaseProfileError) as raised:
                    load_release_profile_file(profile_fixture(fixture_name))
                self.assertIn(f'release profile missing required field: {field_name}', "\n".join(raised.exception.errors))

    def test_malformed_profile_fails_with_path_context(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(profile_fixture('invalid-malformed.yaml'))
        error = raised.exception
        self.assertIn('could not parse release profile', "\n".join(raised.exception.errors))
        self.assertIn("invalid-malformed.yaml", str(error))

    def test_package_version_must_match_release_tag(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(profile_fixture('invalid-wrong-package-version.yaml'))
        self.assertIn('package_version 0.3.6 does not match release_tag v0.3.5', "\n".join(raised.exception.errors))

    def test_unknown_release_kind_fails_closed_before_consistency(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(profile_fixture('invalid-unknown-release-kind.yaml'))
        error = raised.exception
        self.assertIn('unknown release_kind: preview', "\n".join(raised.exception.errors))
        self.assertTrue(error.errors[0].endswith("unknown release_kind: preview"))

    def test_unknown_target_fails_closed_before_consistency(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(profile_fixture('invalid-unknown-target.yaml'))
        error = raised.exception
        self.assertIn('unknown target: cursor', "\n".join(raised.exception.errors))
        self.assertTrue(error.errors[0].endswith("unknown target: cursor"))

    def test_unknown_npm_dist_tag_fails_closed_before_consistency(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(profile_fixture('invalid-unknown-npm-dist-tag.yaml'))
        error = raised.exception
        self.assertIn('unknown npm_dist_tag: next', "\n".join(raised.exception.errors))
        self.assertTrue(error.errors[0].endswith("unknown npm_dist_tag: next"))

    def test_special_release_without_owner_decision_fails(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_release_profile_file(profile_fixture('invalid-special-release-without-rationale.yaml'))
        self.assertIn('special release requires owner_decision', "\n".join(raised.exception.errors))

    def test_special_release_with_owner_decision_is_not_routine(self) -> None:
        profile = load_release_profile_file(profile_fixture("special-release-with-rationale.yaml"))

        self.assertEqual(profile.release_kind, "special")
        self.assertEqual(profile.owner_decision, "Fixture owner decision for a special release path.")
        self.assertFalse(is_routine_release_profile(profile))


class ReleaseSurfaceInventoryTests(unittest.TestCase):
    maxDiff = None

    def test_valid_surface_inventory_classifies_release_surfaces(self) -> None:
        inventory = load_surface_inventory_file(surface_inventory_fixture("valid-inventory.yaml"))

        classifications = {surface["id"]: surface["classification"] for surface in inventory.surfaces}

        self.assertEqual(classifications["release-metadata"], "profile-owned-generated")
        self.assertEqual(classifications["release-notes-narrative"], "human-authored-profile-checked")
        self.assertEqual(classifications["prior-release-evidence"], "historical-immutable")
        self.assertEqual(classifications["prior-profile-snapshots"], "historical-immutable")

    def test_unknown_surface_classification_fails_closed(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_surface_inventory_file(surface_inventory_fixture("invalid-unknown-classification.yaml"))

        self.assertIn("unknown surface classification: generated", "\n".join(raised.exception.errors))

    def test_surface_inventory_missing_classification_fails_with_surface_context(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_surface_inventory_file(surface_inventory_fixture("invalid-missing-classification.yaml"))

        errors = "\n".join(raised.exception.errors)
        self.assertIn("prior-profile-snapshots", errors)
        self.assertIn("missing required field: classification", errors)

    def test_manual_override_without_rationale_fails(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_surface_inventory_file(surface_inventory_fixture("invalid-manual-override-without-rationale.yaml"))

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

    def test_valid_literal_audit_baseline_reports_baseline_drift(self) -> None:
        baseline = load_literal_audit_baseline_file(literal_audit_fixture("valid-baseline.yaml"))

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
            load_literal_audit_baseline_file(literal_audit_fixture("invalid-unknown-classification.yaml"))

        self.assertIn("unknown literal classification: stale-current", "\n".join(raised.exception.errors))

    def test_literal_audit_missing_classification_fails_with_entry_context(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(literal_audit_fixture("invalid-missing-classification.yaml"))

        errors = "\n".join(raised.exception.errors)
        self.assertIn("literal audit entry literal-baseline-001", errors)
        self.assertIn("missing required field: classification", errors)

    def test_changed_unauthorized_current_literal_fails(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(
                literal_audit_fixture("unauthorized-new-literal.yaml"),
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
            load_literal_audit_baseline_file(literal_audit_fixture("historical-fixture-without-rationale.yaml"))

        self.assertIn(
            "historical fixture requires rationale: literal=v0.3.4 file=tests/history.py",
            "\n".join(raised.exception.errors),
        )

    def test_generated_current_literal_requires_profile_or_generated_region_owner(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(literal_audit_fixture("generated-current-without-owner.yaml"))

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
