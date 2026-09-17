"""Preparation idempotency, preserved narrative and pending evidence."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest
import subprocess

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging.adapter_distribution import parse_manifest_yaml
from lib.release.release_transaction import ReleaseProfileError, prepare_release, validate_pending_release_artifacts
from release_fixture_helpers import (assert_errors_contain, prepared_release, release_repo, relative_file_texts)


# Required standing-record rows, independently declared by the tests.
PREFLIGHT_ROWS = (
    'clean worktree except intentional release artifacts',
    'release notes or not-required rationale',
    'generated output current',
    'tests / selected CI / broad smoke',
    'package build or pack proof',
    'package preview',
    'local packed-install smoke',
    'no unresolved release blockers',
    'publish path selected',
    'evidence path prepared',
)


class PrepareReleaseTests(unittest.TestCase):
    maxDiff = None

    def test_approval_driven_preparation_preserves_reviewed_version_and_no_generated_passes(self):
        with release_repo() as root:
            path = root / "docs/releases/v0.3.5.md"
            original = "# Release v0.3.5\n\n## Version Decision\n\n- Version decision: patch\n- Change summary: Reviewed compatibility repair.\n"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(original)
            prepare_release("v0.3.5", root=root, approval_driven=True)
            first = path.read_text()
            self.assertTrue(first.startswith(original))
            self.assertNotIn("| pass |", first)
            self.assertNotIn("routine reviewed product and package updates", first)
            prepare_release("v0.3.5", root=root, approval_driven=True)
            self.assertEqual(path.read_text(), first)

    def test_approval_driven_preserves_human_notes_outside_generated_region(self):
        with release_repo() as root:
            notes = root / "docs/releases/v0.3.5/release-notes.md"
            notes.parent.mkdir(parents=True, exist_ok=True)
            human = "# RigorLoop v0.3.5\n\n| Existing result | pass |\n\nHuman example:\nstatus: pass\n"
            notes.write_text(human)
            prepare_release("v0.3.5", root=root, approval_driven=True)
            self.assertTrue(notes.read_text().startswith(human))
            first = notes.read_bytes()
            prepare_release("v0.3.5", root=root, approval_driven=True)
            self.assertEqual(notes.read_bytes(), first)

    def test_prepare_release_generates_pending_artifacts_idempotently(self) -> None:
        with release_repo() as root:
            before = relative_file_texts(root)

            result = prepare_release("v0.3.5", root=root)
            after_first = relative_file_texts(root)
            second = prepare_release("v0.3.5", root=root)
            after_second = relative_file_texts(root)

        self.assertEqual(after_first, after_second)
        self.assertFalse(second.changed_paths)
        self.assertEqual(
            set(result.changed_paths),
            {
                "docs/releases/v0.3.5/npm-publication.md",
                "docs/releases/v0.3.5/release-notes.md",
                "docs/releases/v0.3.5.md",
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
        self.assertIn("npm dist-tag: latest", after_first["docs/releases/v0.3.5.md"])
        self.assertIn("Version decision: patch", after_first["docs/releases/v0.3.5.md"])

    def test_prepare_release_check_accepts_finalized_prepublication_evidence(self) -> None:
        with release_repo() as root:
            prepare_release("v0.3.5", root=root)

            metadata_path = root / "packages" / "rigorloop" / "dist" / "metadata" / "adapter-artifacts-v0.3.5.json"
            metadata_path.write_text("{}\n", encoding="utf-8")

            release_path = root / "docs" / "releases" / "v0.3.5" / "release.yaml"
            release_text = release_path.read_text(encoding="utf-8")
            manifest_path = root / "dist" / "adapters" / "manifest.yaml"
            manifest_version = parse_manifest_yaml(
                manifest_path.read_text(encoding="utf-8"), manifest_path
            ).version
            release_text = release_text.replace(
                "manifest_version: pending", f"manifest_version: {manifest_version}"
            )
            release_text = release_text.replace("result: pending", "result: pass")
            release_text = release_text.replace(": pending\n", ": pass\n")
            release_path.write_text(release_text, encoding="utf-8")

            report_path = root / "docs" / "reports" / "adapter-artifacts" / "releases" / "v0.3.5.yaml"
            report_text = report_path.read_text(encoding="utf-8")
            report_text = report_text.replace("source_commit: pending", "source_commit: 0123456789abcdef0123456789abcdef01234567")
            report_text = report_text.replace("date: pending", 'date: "2026-08-06"')
            report_text = report_text.replace("sha256: pending", "sha256: " + "a" * 64)
            report_text = report_text.replace("result: pending", "result: pass")
            report_path.write_text(report_text, encoding="utf-8")

            prepare_release("v0.3.5", root=root)
            prepare_release("v0.3.5", root=root, approval_driven=True)
            finalized = relative_file_texts(root)
            checked = prepare_release("v0.3.5", root=root, check=True)

        self.assertFalse(checked.changed_paths)
        self.assertEqual(finalized["docs/releases/v0.3.5/release.yaml"], release_text)
        self.assertEqual(finalized["docs/reports/adapter-artifacts/releases/v0.3.5.yaml"], report_text)

    def test_prepare_release_check_mode_reports_pending_changes_without_writing(self) -> None:
        with release_repo() as root:
            before = relative_file_texts(root)

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)

            after = relative_file_texts(root)

        self.assertEqual(before, after)
        self.assertIn("prepare-release would update", "\n".join(raised.exception.errors))
        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_generated_pending_release_artifacts_validate_shape(self) -> None:
        with release_repo() as root:
            prepare_release("v0.3.5", root=root)

            errors = validate_pending_release_artifacts("v0.3.5", root=root)

        self.assertEqual(errors, [])

    def test_pending_release_artifacts_reject_incomplete_release_yaml(self) -> None:
        with prepared_release() as (root, _):
            path = root / "docs" / "releases" / "v0.3.5" / "release.yaml"
            text = path.read_text(encoding="utf-8")
            start = text.index("adapter_paths:\n")
            end = text.index("instruction_entrypoints:\n")
            path.write_text(text[:start] + text[end:], encoding="utf-8")

            errors = validate_pending_release_artifacts("v0.3.5", root=root)

        self.assertTrue(any("adapter_paths" in error for error in errors), errors)

    def test_pending_release_artifacts_reject_incomplete_standing_record(self) -> None:
        with prepared_release() as (root, _):
            path = root / "docs" / "releases" / "v0.3.5.md"
            text = path.read_text(encoding="utf-8")
            start = text.index("## Recovery / Rollback Notes\n")
            end = text.index("## Follow-up\n")
            path.write_text(text[:start] + text[end:], encoding="utf-8")

            errors = validate_pending_release_artifacts("v0.3.5", root=root)

        self.assertTrue(any("Recovery / Rollback Notes" in error for error in errors), errors)

    def test_pending_standing_record_requires_every_preflight_row(self) -> None:
        for row_name in PREFLIGHT_ROWS:
            with self.subTest(row_name=row_name), prepared_release() as (root, _):
                path = root / "docs" / "releases" / "v0.3.5.md"
                lines = path.read_text(encoding="utf-8").splitlines()
                path.write_text(
                    "\n".join(line for line in lines if not line.startswith(f"| {row_name} |")) + "\n",
                    encoding="utf-8",
                )

                errors = validate_pending_release_artifacts("v0.3.5", root=root)

            self.assertTrue(any(row_name in error and "missing" in error for error in errors), errors)

    def test_pending_standing_record_rejects_unknown_or_duplicate_preflight_rows(self) -> None:
        for row_name in PREFLIGHT_ROWS:
            for mutation in ("unknown", "duplicate"):
                with self.subTest(row_name=row_name, mutation=mutation), prepared_release() as (root, _):
                    path = root / "docs" / "releases" / "v0.3.5.md"
                    text = path.read_text(encoding="utf-8")
                    original = next(line for line in text.splitlines() if line.startswith(f"| {row_name} |"))
                    if mutation == "unknown":
                        replacement = original.replace("| pending |", "| unknown |").replace("| pass |", "| unknown |")
                    else:
                        replacement = original + "\n" + original.replace("| pending |", "| pass |")
                    path.write_text(text.replace(original, replacement), encoding="utf-8")

                    errors = validate_pending_release_artifacts("v0.3.5", root=root)

                expected = "exactly once" if mutation == "duplicate" else "must be"
                self.assertTrue(any(row_name in error and expected in error for error in errors), errors)

    def test_pending_standing_record_rejects_missing_or_duplicate_registry_rows(self) -> None:
        registry_rows = (
            "registry version query",
            "dist-tag points correctly",
            "integrity metadata available",
            "fresh registry install smoke",
            "CLI or npx smoke",
        )
        for row_name in registry_rows:
            for mutation in ("missing", "duplicate"):
                with self.subTest(row_name=row_name, mutation=mutation), prepared_release() as (root, _):
                    path = root / "docs" / "releases" / "v0.3.5.md"
                    text = path.read_text(encoding="utf-8")
                    original = next(line for line in text.splitlines() if line.startswith(f"| {row_name} |"))
                    replacement = "" if mutation == "missing" else original + "\n" + original.replace("not-applicable", "pass", 1)
                    path.write_text(text.replace(original, replacement), encoding="utf-8")

                    errors = validate_pending_release_artifacts("v0.3.5", root=root)

                self.assertTrue(any(row_name in error and "exactly once" in error for error in errors), errors)

    def test_pending_release_artifacts_reject_premature_public_status(self) -> None:
        with prepared_release() as (root, _):
            path = root / "docs" / "releases" / "v0.3.5.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace("- Status: pending-publication", "- Status: published"),
                encoding="utf-8",
            )

            errors = validate_pending_release_artifacts("v0.3.5", root=root)

        self.assertTrue(any("Status" in error and "pending-publication" in error for error in errors), errors)

    def test_prepare_release_does_not_preserve_partial_finalized_release_yaml(self) -> None:
        with release_repo() as root:
            prepare_release("v0.3.5", root=root)
            path = root / "docs" / "releases" / "v0.3.5" / "release.yaml"
            text = path.read_text(encoding="utf-8")
            text = text.replace("manifest_version: pending", "manifest_version: v0.1.5")
            text = text.replace("result: pending", "result: pass")
            text = text.replace(": pending\n", ": pass\n")
            start = text.index("adapter_paths:\n")
            end = text.index("instruction_entrypoints:\n")
            path.write_text(text[:start] + text[end:], encoding="utf-8")

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)

        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_prepare_release_does_not_preserve_bogus_finalized_manifest(self) -> None:
        with release_repo() as root:
            prepare_release("v0.3.5", root=root)
            path = root / "docs" / "releases" / "v0.3.5" / "release.yaml"
            text = path.read_text(encoding="utf-8")
            text = text.replace("manifest_version: pending", "manifest_version: bogus")
            text = text.replace("result: pending", "result: pass")
            text = text.replace(": pending\n", ": pass\n")
            path.write_text(text, encoding="utf-8")

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)

        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_prepare_release_does_not_preserve_empty_passing_smoke_evidence(self) -> None:
        with release_repo() as root:
            prepare_release("v0.3.5", root=root)
            path = root / "docs" / "releases" / "v0.3.5" / "release.yaml"
            text = path.read_text(encoding="utf-8")
            text = text.replace("manifest_version: pending", "manifest_version: v0.1.5")
            text = text.replace("result: pending", "result: pass")
            text = text.replace(": pending\n", ": pass\n")
            text = text.replace(
                '    evidence: "Pending packed-package smoke for v0.3.5 codex."',
                '    evidence: ""',
            )
            path.write_text(text, encoding="utf-8")

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)

        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_prepare_release_does_not_preserve_whitespace_passing_smoke_fields(self) -> None:
        for field in ("tool_version", "evidence"):
            with self.subTest(field=field), release_repo() as root:
                prepare_release("v0.3.5", root=root)
                path = root / "docs" / "releases" / "v0.3.5" / "release.yaml"
                text = path.read_text(encoding="utf-8")
                text = text.replace("manifest_version: pending", "manifest_version: v0.1.5")
                text = text.replace("result: pending", "result: pass")
                text = text.replace(": pending\n", ": pass\n")
                line = next(
                    item for item in text.splitlines()
                    if item.strip().startswith(f"{field}:")
                )
                path.write_text(text.replace(line, f'    {field}: "   "', 1), encoding="utf-8")

                with self.assertRaises(ReleaseProfileError) as raised:
                    prepare_release("v0.3.5", root=root, check=True)

            self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_pending_release_artifacts_require_standing_release_record(self) -> None:
        with prepared_release() as (root, _):
            (root / "docs" / "releases" / "v0.3.5.md").unlink()

            errors = validate_pending_release_artifacts("v0.3.5", root=root)

        self.assertTrue(any("docs/releases/v0.3.5.md" in error and "missing" in error for error in errors), errors)

    def test_pending_release_artifacts_reject_target_result_published(self) -> None:
        def mutate(text: str) -> str:
            return text.replace('    result: "pending-publication"\n', '    result: "published"\n', 1)

        with prepared_release() as (root, pending):
            original = pending.read_text(encoding="utf-8")
            changed = (mutate)(original)
            self.assertNotEqual(changed, original, "fixture mutation must change the pending evidence")
            pending.write_text(changed, encoding="utf-8")
            errors = validate_pending_release_artifacts("v0.3.5", root=root)
        assert_errors_contain(self, errors, 'codex', 'result', 'pending-publication')

    def test_pending_release_artifacts_reject_npx_y_command_shape(self) -> None:
        def mutate(text: str) -> str:
            return text.replace(
                "npx @xiongxianfei/rigorloop@0.3.5 init codex --json",
                "npx -y @xiongxianfei/rigorloop@0.3.5 init codex --json",
                1,
            )

        with prepared_release() as (root, pending):
            original = pending.read_text(encoding="utf-8")
            changed = (mutate)(original)
            self.assertNotEqual(changed, original, "fixture mutation must change the pending evidence")
            pending.write_text(changed, encoding="utf-8")
            errors = validate_pending_release_artifacts("v0.3.5", root=root)
        assert_errors_contain(self, errors, 'codex', 'command', 'npx @xiongxianfei/rigorloop@0.3.5 init codex --json')

    def test_pending_release_artifacts_reject_missing_target_row(self) -> None:
        def mutate(text: str) -> str:
            start = text.index("  claude:\n")
            end = text.index("\n```", start)
            return text[:start] + text[end:]

        with prepared_release() as (root, pending):
            original = pending.read_text(encoding="utf-8")
            changed = (mutate)(original)
            self.assertNotEqual(changed, original, "fixture mutation must change the pending evidence")
            pending.write_text(changed, encoding="utf-8")
            errors = validate_pending_release_artifacts("v0.3.5", root=root)
        assert_errors_contain(self, errors, 'missing target: claude')

    def test_pending_release_artifacts_reject_duplicate_target_row(self) -> None:
        def mutate(text: str) -> str:
            start = text.index("  codex:\n")
            end = text.index("  claude:\n")
            return text[:end] + text[start:end] + text[end:]

        with prepared_release() as (root, pending):
            original = pending.read_text(encoding="utf-8")
            changed = (mutate)(original)
            self.assertNotEqual(changed, original, "fixture mutation must change the pending evidence")
            pending.write_text(changed, encoding="utf-8")
            errors = validate_pending_release_artifacts("v0.3.5", root=root)
        assert_errors_contain(self, errors, 'duplicate target: codex')

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

        with prepared_release() as (root, pending):
            original = pending.read_text(encoding="utf-8")
            changed = (mutate)(original)
            self.assertNotEqual(changed, original, "fixture mutation must change the pending evidence")
            pending.write_text(changed, encoding="utf-8")
            errors = validate_pending_release_artifacts("v0.3.5", root=root)
        assert_errors_contain(self, errors, 'unknown target: cursor')

    def test_pending_release_artifacts_reject_table_projection_mismatch(self) -> None:
        def mutate(text: str) -> str:
            return text.replace(
                "| codex | `npx @xiongxianfei/rigorloop@0.3.5 init codex --json` | `0.3.5` | pending publication | pending public archive URL | pending | pending | pending | pending live command output summary | pending | pending | pending-publication | live-smoke-pending |",
                "| codex | `npx @xiongxianfei/rigorloop@0.3.5 init codex --json` | `0.3.5` | pending publication | pending public archive URL | pending | pending | pending | pending live command output summary | pending | pending | published | live-smoke-pending |",
            )

        with prepared_release() as (root, pending):
            original = pending.read_text(encoding="utf-8")
            changed = (mutate)(original)
            self.assertNotEqual(changed, original, "fixture mutation must change the pending evidence")
            pending.write_text(changed, encoding="utf-8")
            errors = validate_pending_release_artifacts("v0.3.5", root=root)
        assert_errors_contain(self, errors, 'codex', 'table projection mismatch', 'result')

    def test_prepare_release_does_not_publish_or_require_external_state(self) -> None:
        with release_repo() as root:
            result = prepare_release("v0.3.5", root=root)

        self.assertEqual(result.external_actions, ())

    def test_prepare_release_cli_check_succeeds_after_generation(self) -> None:
        with release_repo() as root:
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
