"""Supported profiles, surface ownership and literal classification."""

from __future__ import annotations

import sys
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import ReleaseProfileError, is_routine_release_profile, load_literal_audit_baseline_file, load_release_profile, load_release_profile_file, load_surface_inventory_file
from release_fixture_helpers import (CHANGE_ROOT, REQUIRED_PROFILE_FIELD_CASES, literal_audit_fixture, profile_fixture, surface_inventory_fixture)


class ReleaseProfileTests(unittest.TestCase):
    maxDiff = None

    def accepted_private_profile(self, root: Path, version: str = "0.3.5") -> tuple[Path, str]:
        path = root / f"v{version}.yaml"
        body = profile_fixture("valid-routine-v0.3.5.yaml").read_text().replace("0.3.5", version)
        path.write_text(body)
        (root / "neighbor.txt").write_text("Preserve unrelated profile input.\n")
        profile = load_release_profile_file(path)
        self.assertEqual(profile.release_tag, "v" + version)
        self.assertEqual(profile.package_version, version)
        self.assertEqual(profile.targets, ("codex", "claude"))
        self.assertTrue(is_routine_release_profile(profile))
        return path, body

    @staticmethod
    def profile_files(root: Path) -> dict[str, bytes]:
        return {path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*") if path.is_file()}

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
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, _ = self.accepted_private_profile(root)
            path.unlink()
            before = self.profile_files(root)
            with self.assertRaises(ReleaseProfileError) as raised:
                load_release_profile_file(path)
            self.assertEqual(raised.exception.errors, [f"release profile not found: {path}"])
            self.assertIn(str(path), str(raised.exception))
            self.assertEqual(self.profile_files(root), before)

    def test_missing_required_profile_fields_fail_with_named_field(self) -> None:
        for _, field_name in REQUIRED_PROFILE_FIELD_CASES:
            with self.subTest(field=field_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                # The owning contract retains implicit latest only for v0.3.5/v0.3.6.
                # Preserve the existing non-legacy missing-channel partition.
                version = "0.4.0" if field_name == "npm_dist_tag" else "0.3.5"
                path, body = self.accepted_private_profile(root, version)
                lines = body.splitlines(keepends=True)
                starts = [i for i, line in enumerate(lines) if line.startswith(field_name + ":")]
                self.assertEqual(len(starts), 1)
                start = starts[0]
                end = next((i for i in range(start + 1, len(lines))
                            if lines[i].strip() and not lines[i].startswith(" ")), len(lines))
                path.write_text("".join(lines[:start] + lines[end:]))
                before = self.profile_files(root)
                with self.assertRaises(ReleaseProfileError) as raised:
                    load_release_profile_file(path)
                self.assertEqual(raised.exception.errors,
                                 [f"release profile missing required field: {field_name}"])
                self.assertEqual(self.profile_files(root), before)

    def test_malformed_profile_fails_with_path_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, body = self.accepted_private_profile(root)
            self.assertEqual(body.count("release_kind: routine"), 1)
            path.write_text(body.replace("release_kind: routine", "release_kind routine"))
            before = self.profile_files(root)
            with self.assertRaises(ReleaseProfileError) as raised:
                load_release_profile_file(path)
            self.assertEqual(raised.exception.errors,
                             ["could not parse release profile: line 2 is missing ':'"])
            self.assertIn(str(path), str(raised.exception))
            self.assertEqual(self.profile_files(root), before)

    def test_package_version_must_match_release_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, body = self.accepted_private_profile(root)
            self.assertEqual(body.count("package_version: 0.3.5"), 1)
            path.write_text(body.replace("package_version: 0.3.5", "package_version: 0.3.6"))
            before = self.profile_files(root)
            with self.assertRaises(ReleaseProfileError) as raised:
                load_release_profile_file(path)
            self.assertEqual(raised.exception.errors,
                             ["package_version 0.3.6 does not match release_tag v0.3.5"])
            self.assertEqual(self.profile_files(root), before)

    def test_unknown_profile_values_precede_version_consistency(self) -> None:
        # REL-IN-001: all three vocabularies must reject before consistency.
        for field, old, new, diagnostic in (
            ("release_kind", "release_kind: routine", "release_kind: preview", "unknown release_kind: preview"),
            ("target", "  - claude", "  - cursor", "unknown target: cursor"),
            ("npm_dist_tag", "npm_dist_tag: latest", "npm_dist_tag: next", "unknown npm_dist_tag: next"),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "v0.3.5.yaml"
                body = profile_fixture("valid-routine-v0.3.5.yaml").read_text()
                path.write_text(body)
                self.assertEqual(load_release_profile_file(path).package_version, "0.3.5")
                self.assertEqual(body.count(old), 1)
                self.assertEqual(body.count("package_version: 0.3.5"), 1)
                path.write_text(body.replace(old, new).replace("package_version: 0.3.5", "package_version: 0.3.6"))
                with self.assertRaises(ReleaseProfileError) as raised:
                    load_release_profile_file(path)
                self.assertTrue(raised.exception.errors[0].endswith(diagnostic), raised.exception.errors)

    def test_special_release_without_owner_decision_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, body = self.accepted_private_profile(root)
            special = body.replace("release_kind: routine", "release_kind: special")
            decision = 'owner_decision: "Fixture owner decision for a special release path."\n'
            path.write_text(special + decision)
            accepted = load_release_profile_file(path)
            self.assertEqual(accepted.release_kind, "special")
            self.assertEqual(accepted.owner_decision, "Fixture owner decision for a special release path.")
            self.assertFalse(is_routine_release_profile(accepted))
            path.write_text(special)
            before = self.profile_files(root)
            with self.assertRaises(ReleaseProfileError) as raised:
                load_release_profile_file(path)
            self.assertEqual(raised.exception.errors, ["special release requires owner_decision"])
            self.assertEqual(self.profile_files(root), before)

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
