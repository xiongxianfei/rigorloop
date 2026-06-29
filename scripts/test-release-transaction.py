#!/usr/bin/env python3
"""Focused tests for release transaction automation helpers."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import json
import os
import subprocess
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
    prepare_release,
    profile_path_for_tag,
    release_preflight,
    validate_release_timing_evidence,
    validate_release_workflow_parity,
    validate_pending_release_artifacts,
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
        self.assertEqual(classifications["prior-profile-snapshots"], "historical-immutable")

    def test_unknown_surface_classification_fails_closed(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_surface_inventory_file(self.fixture("invalid-unknown-classification.yaml"))

        self.assertIn("unknown surface classification: generated", "\n".join(raised.exception.errors))

    def test_surface_inventory_missing_classification_fails_with_surface_context(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_surface_inventory_file(self.fixture("invalid-missing-classification.yaml"))

        errors = "\n".join(raised.exception.errors)
        self.assertIn("prior-profile-snapshots", errors)
        self.assertIn("missing required field: classification", errors)

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

    def test_literal_audit_missing_classification_fails_with_entry_context(self) -> None:
        with self.assertRaises(ReleaseProfileError) as raised:
            load_literal_audit_baseline_file(self.fixture("invalid-missing-classification.yaml"))

        errors = "\n".join(raised.exception.errors)
        self.assertIn("literal audit entry literal-baseline-001", errors)
        self.assertIn("missing required field: classification", errors)

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


class PrepareReleaseTests(unittest.TestCase):
    maxDiff = None

    def make_repo(self, root: Path) -> None:
        profile_dir = root / "docs" / "releases" / "profiles"
        profile_dir.mkdir(parents=True)
        shutil.copy2(PROFILE_FIXTURES / "valid-routine-v0.3.5.yaml", profile_dir / "v0.3.5.yaml")
        package_root = root / "packages" / "rigorloop"
        package_root.mkdir(parents=True)
        (package_root / "package.json").write_text(
            json.dumps(
                {
                    "name": "@xiongxianfei/rigorloop",
                    "version": "0.3.4",
                    "files": ["dist/", "package.json", "README.md", "LICENSE"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (package_root / "README.md").write_text(
            "Pinned example:\n\n"
            "```bash\n"
            "npx @xiongxianfei/rigorloop@0.3.4 init codex --json\n"
            "```\n",
            encoding="utf-8",
        )
        metadata_dir = package_root / "dist" / "metadata"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "releases.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "releases": {
                        "v0.3.4": {
                            "source_repository": "xiongxianfei/rigorloop",
                            "release_tag": "v0.3.4",
                            "bundled_metadata": "adapter-artifacts-v0.3.4.json",
                            "bundled_metadata_sha256": "abc",
                        }
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        release_dir = root / "docs" / "releases" / "v0.3.5"
        release_dir.mkdir(parents=True)
        (release_dir / "release-notes.md").write_text(
            "# RigorLoop v0.3.5\n\n"
            "Human-authored opening narrative.\n\n"
            "<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v0.3.5.yaml -->\n"
            "stale generated content\n"
            "<!-- rigorloop:generated:end release-transaction surface=release-metadata -->\n\n"
            "Human-authored closing notes.\n",
            encoding="utf-8",
        )
        historical_dir = root / "docs" / "releases" / "v0.3.4"
        historical_dir.mkdir(parents=True)
        (historical_dir / "release.yaml").write_text("version: v0.3.4\n", encoding="utf-8")

    def relative_file_texts(self, root: Path) -> dict[str, str]:
        return {
            str(path.relative_to(root)): path.read_text(encoding="utf-8")
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def make_prepared_repo(self, root: Path) -> Path:
        self.make_repo(root)
        prepare_release("v0.3.5", root=root)
        return root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"

    def assert_pending_evidence_error(
        self,
        mutator,
        *needles: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            npm_publication = self.make_prepared_repo(root)
            text = npm_publication.read_text(encoding="utf-8")
            npm_publication.write_text(mutator(text), encoding="utf-8")

            errors = validate_pending_release_artifacts("v0.3.5", root=root)

        self.assertTrue(
            any(all(needle in error for needle in needles) for error in errors),
            errors,
        )

    def test_prepare_release_generates_pending_artifacts_idempotently(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            before = self.relative_file_texts(root)

            result = prepare_release("v0.3.5", root=root)
            after_first = self.relative_file_texts(root)
            second = prepare_release("v0.3.5", root=root)
            after_second = self.relative_file_texts(root)

        self.assertEqual(after_first, after_second)
        self.assertFalse(second.changed_paths)
        self.assertEqual(
            set(result.changed_paths),
            {
                "docs/releases/v0.3.5/npm-publication.md",
                "docs/releases/v0.3.5/release-notes.md",
                "docs/releases/v0.3.5/release.yaml",
                "docs/releases/v0.3.5/timing.yaml",
                "docs/reports/adapter-artifacts/releases/v0.3.5.yaml",
                "packages/rigorloop/README.md",
                "packages/rigorloop/dist/metadata/releases.json",
                "packages/rigorloop/package.json",
                "tests/fixtures/release-transaction/current-version.json",
            },
        )
        self.assertEqual(before["docs/releases/v0.3.4/release.yaml"], "version: v0.3.4\n")
        self.assertEqual(after_first["docs/releases/v0.3.4/release.yaml"], "version: v0.3.4\n")
        self.assertIn("Human-authored opening narrative.", after_first["docs/releases/v0.3.5/release-notes.md"])
        self.assertIn("Human-authored closing notes.", after_first["docs/releases/v0.3.5/release-notes.md"])
        self.assertNotIn("stale generated content", after_first["docs/releases/v0.3.5/release-notes.md"])
        self.assertIn("npx @xiongxianfei/rigorloop@0.3.5 init codex --json", after_first["packages/rigorloop/README.md"])
        self.assertNotIn("@0.3.4 init codex", after_first["packages/rigorloop/README.md"])

    def test_prepare_release_check_mode_reports_pending_changes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            before = self.relative_file_texts(root)

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)

            after = self.relative_file_texts(root)

        self.assertEqual(before, after)
        self.assertIn("prepare-release would update", "\n".join(raised.exception.errors))
        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_generated_pending_release_artifacts_validate_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            prepare_release("v0.3.5", root=root)

            errors = validate_pending_release_artifacts("v0.3.5", root=root)

        self.assertEqual(errors, [])

    def test_pending_release_artifacts_reject_target_result_published(self) -> None:
        def mutate(text: str) -> str:
            return text.replace('    result: "pending-publication"\n', '    result: "published"\n', 1)

        self.assert_pending_evidence_error(mutate, "codex", "result", "pending-publication")

    def test_pending_release_artifacts_reject_npx_y_command_shape(self) -> None:
        def mutate(text: str) -> str:
            return text.replace(
                "npx @xiongxianfei/rigorloop@0.3.5 init codex --json",
                "npx -y @xiongxianfei/rigorloop@0.3.5 init codex --json",
                1,
            )

        self.assert_pending_evidence_error(
            mutate,
            "codex",
            "command",
            "npx @xiongxianfei/rigorloop@0.3.5 init codex --json",
        )

    def test_pending_release_artifacts_reject_missing_target_row(self) -> None:
        def mutate(text: str) -> str:
            start = text.index("  claude:\n")
            end = text.index("  opencode:\n")
            return text[:start] + text[end:]

        self.assert_pending_evidence_error(mutate, "missing target: claude")

    def test_pending_release_artifacts_reject_duplicate_target_row(self) -> None:
        def mutate(text: str) -> str:
            start = text.index("  codex:\n")
            end = text.index("  claude:\n")
            return text[:end] + text[start:end] + text[end:]

        self.assert_pending_evidence_error(mutate, "duplicate target: codex")

    def test_pending_release_artifacts_reject_unknown_target_row(self) -> None:
        def mutate(text: str) -> str:
            start = text.index("  codex:\n")
            end = text.index("  claude:\n")
            cursor = text[start:end].replace("  codex:\n", "  cursor:\n").replace(
                '    target: "codex"\n',
                '    target: "cursor"\n',
            ).replace(
                " init codex --json",
                " init cursor --json",
            )
            return text[:end] + cursor + text[end:]

        self.assert_pending_evidence_error(mutate, "unknown target: cursor")

    def test_pending_release_artifacts_reject_table_projection_mismatch(self) -> None:
        def mutate(text: str) -> str:
            return text.replace(
                "| codex | `npx @xiongxianfei/rigorloop@0.3.5 init codex --json` | `0.3.5` | pending publication | pending public archive URL | pending | pending | pending | pending live command output summary | pending | pending | pending-publication | live-smoke-pending |",
                "| codex | `npx @xiongxianfei/rigorloop@0.3.5 init codex --json` | `0.3.5` | pending publication | pending public archive URL | pending | pending | pending | pending live command output summary | pending | pending | published | live-smoke-pending |",
            )

        self.assert_pending_evidence_error(mutate, "codex", "table projection mismatch", "result")

    def test_prepare_release_does_not_publish_or_require_external_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)

            result = prepare_release("v0.3.5", root=root)

        self.assertEqual(result.external_actions, ())

    def test_prepare_release_cli_check_succeeds_after_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            prepare_release("v0.3.5", root=root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "prepare-release.py"),
                    "v0.3.5",
                    "--root",
                    str(root),
                    "--check",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("prepared v0.3.5: no changes", result.stdout)
        self.assertIn("next: python scripts/release-preflight.py v0.3.5", result.stdout)


class ReleasePreflightTests(unittest.TestCase):
    maxDiff = None

    def make_prepared_repo(self, root: Path) -> None:
        PrepareReleaseTests().make_repo(root)
        prepare_release("v0.3.5", root=root)

    def init_git_fixture(self, root: Path) -> None:
        subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def relative_file_texts(self, root: Path) -> dict[str, str]:
        return {
            str(path.relative_to(root)): path.read_text(encoding="utf-8")
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def assert_preflight_error(self, mutator, *needles: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            mutator(root)

            result = release_preflight("v0.3.5", root=root)

        self.assertTrue(
            any(all(needle in error for needle in needles) for error in result.errors),
            result.errors,
        )

    def test_release_preflight_clean_fixture_is_idempotent_and_side_effect_light(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            before = self.relative_file_texts(root)

            first = release_preflight("v0.3.5", root=root)
            second = release_preflight("v0.3.5", root=root)
            after = self.relative_file_texts(root)

        self.assertEqual(first.errors, ())
        self.assertEqual(second.errors, ())
        self.assertEqual(before, after)
        self.assertEqual(first.external_actions, ())

    def test_release_preflight_cli_succeeds_on_clean_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            self.init_git_fixture(root)

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
            self.make_prepared_repo(root)

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

        self.assert_preflight_error(mutate, "release profile", "parse")

    def test_release_preflight_rejects_incomplete_profile(self) -> None:
        def mutate(root: Path) -> None:
            profile = root / "docs" / "releases" / "profiles" / "v0.3.5.yaml"
            shutil.copy2(PROFILE_FIXTURES / "invalid-missing-validation.yaml", profile)

        self.assert_preflight_error(mutate, "missing required field", "validation")

    def test_release_preflight_rejects_missing_required_local_input(self) -> None:
        def mutate(root: Path) -> None:
            metadata = root / "packages" / "rigorloop" / "dist" / "metadata" / "releases.json"
            metadata.unlink()

        self.assert_preflight_error(
            mutate,
            "packages/rigorloop/dist/metadata/releases.json",
            "missing required local input",
        )

    def test_release_preflight_fails_package_profile_version_mismatch(self) -> None:
        def mutate(root: Path) -> None:
            package_json = root / "packages" / "rigorloop" / "package.json"
            data = json.loads(package_json.read_text(encoding="utf-8"))
            data["version"] = "0.3.4"
            package_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        self.assert_preflight_error(mutate, "package version", "0.3.4", "0.3.5")

    def test_release_preflight_fails_stale_metadata_pointer(self) -> None:
        def mutate(root: Path) -> None:
            releases_json = root / "packages" / "rigorloop" / "dist" / "metadata" / "releases.json"
            data = json.loads(releases_json.read_text(encoding="utf-8"))
            data["releases"]["v0.3.5"]["bundled_metadata"] = "adapter-artifacts-v0.3.4.json"
            releases_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        self.assert_preflight_error(mutate, "metadata pointer", "adapter-artifacts-v0.3.4.json", "adapter-artifacts-v0.3.5.json")

    def test_release_preflight_fails_invalid_pending_evidence_shape(self) -> None:
        def mutate(root: Path) -> None:
            npm_publication = root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"
            text = npm_publication.read_text(encoding="utf-8")
            npm_publication.write_text(
                text.replace('    result: "pending-publication"\n', '    result: "published"\n', 1),
                encoding="utf-8",
            )

        self.assert_preflight_error(mutate, "codex", "result", "pending-publication")

    def test_release_preflight_fails_dirty_release_output(self) -> None:
        def mutate(root: Path) -> None:
            output = root / "release-output"
            output.mkdir()
            (output / "leftover.txt").write_text("stale\n", encoding="utf-8")

        self.assert_preflight_error(mutate, "release-output", "not clean")

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
            self.make_prepared_repo(root)
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
            self.make_prepared_repo(root)
            self.init_git_fixture(root)
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
            self.make_prepared_repo(root)
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
            self.make_prepared_repo(root)
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
            self.make_prepared_repo(root)
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


class ReleaseGateParityAndTimingTests(unittest.TestCase):
    maxDiff = None

    def make_prepared_repo(self, root: Path) -> None:
        PrepareReleaseTests().make_repo(root)
        prepare_release("v0.3.5", root=root)

    def write_timing(self, root: Path, text: str) -> Path:
        timing = root / "docs" / "releases" / "v0.3.5" / "timing.yaml"
        timing.parent.mkdir(parents=True, exist_ok=True)
        timing.write_text(text, encoding="utf-8")
        return timing

    def valid_timing_text(self, *, preflight_duration: int = 12) -> str:
        return (
            "schema_version: release-timing-v1\n"
            "release_tag: v0.3.5\n"
            "release_profile: docs/releases/profiles/v0.3.5.yaml\n"
            "created_at: 2026-06-29T00:00:00Z\n"
            "\n"
            "phases:\n"
            "  - id: prepare_release\n"
            "    command: python scripts/prepare-release.py v0.3.5\n"
            "    duration_seconds: 10\n"
            "    result: pass\n"
            "  - id: preflight\n"
            "    command: python scripts/release-preflight.py v0.3.5\n"
            f"    duration_seconds: {preflight_duration}\n"
            "    result: pass\n"
            "  - id: local_release_verify\n"
            "    command: bash scripts/release-verify.sh v0.3.5\n"
            "    duration_seconds: 180\n"
            "    result: pass\n"
            "  - id: ci_release_verify\n"
            "    command: bash scripts/release-verify.sh v0.3.5\n"
            "    duration_seconds: 0\n"
            "    result: pending\n"
            "  - id: publication_wait\n"
            "    command: external GitHub and npm publication wait\n"
            "    duration_seconds: 0\n"
            "    result: pending\n"
            "  - id: public_closeout\n"
            "    command: python scripts/close-release-publication.py v0.3.5\n"
            "    duration_seconds: 0\n"
            "    result: pending\n"
            "\n"
            "checks:\n"
            "  - id: adapter_distribution.regression\n"
            "    command: python scripts/test-adapter-distribution.py\n"
            "    phase: local_release_verify\n"
            "    duration_seconds: 120\n"
            "    result: pass\n"
        )

    def test_release_verify_dry_run_preserves_full_gate_checks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ)
            env["RELEASE_VERIFY_DRY_RUN"] = "1"
            env["RELEASE_OUTPUT_DIR"] = str(Path(tmp) / "release-output")
            env["RELEASE_COMMIT"] = "fixture-commit"

            result = subprocess.run(
                ["bash", "scripts/release-verify.sh", "v0.3.5"],
                cwd=ROOT,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        output = result.stderr + result.stdout
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("python scripts/test-adapter-distribution.py", output)
        self.assertIn("python scripts/test-npm-package-publication.py", output)
        self.assertIn("python scripts/validate-release.py --version v0.3.5", output)
        self.assertIn("security", output.lower())

    def test_release_workflow_delegates_to_release_verify(self) -> None:
        self.assertEqual(validate_release_workflow_parity(ROOT), [])

    def test_release_workflow_parity_rejects_direct_validate_release_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github" / "workflows" / "release.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                "name: release\n"
                "jobs:\n"
                "  release:\n"
                "    steps:\n"
                "      - run: python scripts/validate-release.py --version \"$GITHUB_REF_NAME\"\n",
                encoding="utf-8",
            )

            errors = validate_release_workflow_parity(root)

        self.assertTrue(any("release-verify.sh" in error for error in errors), errors)
        self.assertTrue(any("validate-release.py" in error for error in errors), errors)

    def test_prepare_release_generates_timing_evidence_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertEqual(result.errors, ())
        self.assertEqual(result.warnings, ())

    def test_release_timing_evidence_validates_required_phases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            self.write_timing(root, self.valid_timing_text())

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertEqual(result.errors, ())
        self.assertEqual(result.warnings, ())

    def test_release_timing_missing_when_profile_requires_it_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            PrepareReleaseTests().make_repo(root)

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("timing.yaml" in error and "missing" in error for error in result.errors), result.errors)

    def test_release_timing_missing_duration_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            self.write_timing(root, self.valid_timing_text().replace("    duration_seconds: 12\n", ""))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("preflight" in error and "duration_seconds" in error for error in result.errors), result.errors)

    def test_release_timing_unknown_phase_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            self.write_timing(root, self.valid_timing_text().replace("id: preflight", "id: fast_lane", 1))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("unknown timing phase id: fast_lane" in error for error in result.errors), result.errors)

    def test_release_timing_unknown_result_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            self.write_timing(root, self.valid_timing_text().replace("result: pass", "result: done", 1))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("unknown timing result: done" in error for error in result.errors), result.errors)

    def test_release_timing_duration_over_target_is_warning_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_prepared_repo(root)
            self.write_timing(root, self.valid_timing_text(preflight_duration=999))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertEqual(result.errors, ())
        self.assertTrue(any("preflight" in warning and "target" in warning for warning in result.warnings), result.warnings)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
