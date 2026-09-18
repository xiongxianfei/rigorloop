"""Preparation idempotency, preserved narrative and pending evidence."""

from __future__ import annotations

from contextlib import ExitStack
import json
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging.adapter_distribution import parse_manifest_yaml
from lib.release.release_transaction import ReleaseProfileError, prepare_release, validate_pending_release_artifacts
from release_fixture_helpers import (assert_errors_contain, prepared_release, release_repo, relative_file_texts, relative_tree)


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


def finalize_prepublication(root: Path) -> tuple[str, str]:
    """Build controlled prepublication input; these values are not live release proof."""
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
    release_text = release_text.replace('tool_version: "packed-package"', 'tool_version: "0.3.5"')
    release_text = release_text.replace("Pending packed-package smoke", "Controlled fixture: packed-package smoke passed")
    release_text = release_text.replace("pending release verification", "controlled fixture verification completed")
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
    return release_text, report_text


class PrepareReleaseTests(unittest.TestCase):
    maxDiff = None

    def test_prepare_release_rejects_malformed_generated_regions_before_writing(self):
        start = "<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v0.3.5.yaml -->"
        end = "<!-- rigorloop:generated:end release-transaction surface=release-metadata -->"
        variants = {
            "missing-end": (lambda text: text.replace(end, "", 1), "missing end marker"),
            "nested": (lambda text: text.replace(start, start + "\n" + start, 1).replace(end, end + "\n" + end, 1), "nested"),
            "mismatched-namespace": (lambda text: text.replace("start release-transaction", "start another-namespace", 1), "namespace"),
            "mismatched-surface": (lambda text: text.replace("start release-transaction surface=release-metadata", "start release-transaction surface=timing-evidence", 1), "does not match"),
            "unknown-surface": (lambda text: text.replace("surface=release-metadata", "surface=unknown_value"), "unknown surface: unknown_value"),
            "unknown-before-missing-end": (lambda text: text.replace(end, "", 1).replace("surface=release-metadata", "surface=unknown_value"), "unknown surface: unknown_value"),
        }
        for name, (mutate, diagnostic) in variants.items():
            with self.subTest(variant=name), release_repo() as root:
                prepare_release("v0.3.5", root=root)
                self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
                path = root / "docs/releases/v0.3.5/release-notes.md"
                original = path.read_text()
                malformed = mutate(original)
                self.assertNotEqual(malformed, original)
                path.write_text(malformed)
                before = relative_tree(root)
                with self.assertRaises(ReleaseProfileError) as raised:
                    prepare_release("v0.3.5", root=root)
                self.assertIn("generated region", "\n".join(raised.exception.errors))
                self.assertIn(diagnostic, "\n".join(raised.exception.errors))
                self.assertEqual(relative_tree(root), before)

    def test_prepare_release_preserves_other_known_generated_regions(self):
        with release_repo() as root:
            notes = root / "docs/releases/v0.3.5/release-notes.md"
            retained = "".join(
                f"\n<!-- rigorloop:generated:start release-transaction surface={surface} profile=docs/releases/profiles/v0.3.5.yaml -->\n"
                f"retained {surface}\n"
                f"<!-- rigorloop:generated:end release-transaction surface={surface} -->\n"
                for surface in ("adapter-artifact-expectations", "pending-npm-publication", "published-npm-publication", "target-init-smoke", "current-version-fixtures", "timing-evidence")
            )
            notes.write_text(notes.read_text() + retained)
            prepare_release("v0.3.5", root=root)
            self.assertTrue(notes.read_text().endswith(retained))
            before = relative_tree(root)
            self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
            self.assertEqual(relative_tree(root), before)

    def test_approval_driven_preparation_preserves_reviewed_version_and_no_generated_passes(self):
        for existing_timing in (None, b"# existing diagnostic evidence\ncreated_at: pending\n"):
            with self.subTest(existing_timing=existing_timing is not None), release_repo() as root:
                path = root / "docs/releases/v0.3.5.md"
                original = "# Release v0.3.5\n\n## Version Decision\n\n- Version decision: patch\n- Change summary: Reviewed compatibility repair.\n"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(original)
                timing = root / "docs/releases/v0.3.5/timing.yaml"
                if existing_timing is not None:
                    timing.write_bytes(existing_timing)
                prepare_release("v0.3.5", root=root, approval_driven=True)
                first = path.read_text()
                self.assertTrue(first.startswith(original))
                self.assertNotIn("| pass |", first)
                self.assertNotIn("routine reviewed product and package updates", first)
                self.assertEqual(timing.read_bytes() if timing.exists() else None, existing_timing)
                pending = (root / "docs/releases/v0.3.5/npm-publication.md").read_text()
                self.assertIn("Status: pending-publication", pending)
                self.assertIn("  published: false\n", pending)
                for target in ("codex", "claude"):
                    row = pending.split(f"  {target}:\n", 1)[1].split("\n  claude:\n", 1)[0].split("\n```", 1)[0]
                    self.assertIn('result: "pending-publication"', row)
                before = relative_tree(root)
                prepare_release("v0.3.5", root=root, approval_driven=True)
                self.assertEqual(path.read_text(), first)
                self.assertEqual(relative_tree(root), before)

    def test_approval_driven_preserves_human_notes_outside_generated_region(self):
        for existing_region in (False, True):
            with self.subTest(existing_region=existing_region), release_repo() as root:
                notes = root / "docs/releases/v0.3.5/release-notes.md"
                notes.parent.mkdir(parents=True, exist_ok=True)
                prefix = "# RigorLoop v0.3.5\n\n| Existing result | pass |\n\nHuman example:\nstatus: pass\n"
                suffix = "\n\nHuman closing notes, spacing preserved.  \n"
                original = notes.read_text()
                start = original.index("<!-- rigorloop:generated:start")
                end = original.index("<!-- rigorloop:generated:end")
                end = original.index("-->", end) + 3
                notes.write_text(prefix + (original[start:end] if existing_region else "") + suffix)
                history = (root / "docs/releases/v0.3.4/release.yaml").read_bytes()
                prepare_release("v0.3.5", root=root, approval_driven=True)
                actual = notes.read_text()
                if existing_region:
                    self.assertEqual(actual[:actual.index("<!-- rigorloop:generated:start")], prefix)
                    end = actual.index("<!-- rigorloop:generated:end")
                    self.assertEqual(actual[actual.index("-->", end) + 3:], suffix)
                else:
                    self.assertTrue(actual.startswith(prefix + suffix))
                self.assertEqual((root / "docs/releases/v0.3.4/release.yaml").read_bytes(), history)
                self.assertIn("Status: pending-publication", (root / "docs/releases/v0.3.5/npm-publication.md").read_text())
                first = notes.read_bytes()
                prepare_release("v0.3.5", root=root, approval_driven=True)
                self.assertEqual(notes.read_bytes(), first)

    def test_prepare_release_generates_pending_artifacts_idempotently(self) -> None:
        with release_repo() as root:
            package = root / "packages/rigorloop/package.json"
            package_before = json.loads(package.read_text())
            package_before.update(name="@example/previous-name", **{"x-test-preserved": {"enabled": True, "values": [1, 2]}})
            package.write_text(json.dumps(package_before) + "\n")
            before = relative_file_texts(root)
            tree_before = relative_tree(root)

            result = prepare_release("v0.3.5", root=root)
            after_first = relative_file_texts(root)
            second = prepare_release("v0.3.5", root=root)
            after_second = relative_file_texts(root)
            tree_after = relative_tree(root)
            self.assertEqual(json.loads(package.read_text()), {**package_before, "name": "@xiongxianfei/rigorloop", "version": "0.3.5"})
            self.assertEqual(set(before) - set(after_first), set())
            actual_changes = {path for path in after_first if after_first[path] != before.get(path)}
            self.assertEqual(actual_changes, set(result.changed_paths))
            for path in tree_before.keys() & tree_after.keys():
                if path not in actual_changes:
                    self.assertEqual(tree_after[path], tree_before[path], path)
            expected_entries = set(tree_before) | set(after_first)
            for path in after_first:
                expected_entries.update(parent.as_posix() for parent in Path(path).parents if parent != Path("."))
            self.assertEqual(set(tree_after), expected_entries)

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
        original_notes = before["docs/releases/v0.3.5/release-notes.md"]
        prepared_notes = after_first["docs/releases/v0.3.5/release-notes.md"]
        self.assertEqual(prepared_notes.split("<!-- rigorloop:generated:start", 1)[0], original_notes.split("<!-- rigorloop:generated:start", 1)[0])
        self.assertEqual(prepared_notes.split("<!-- rigorloop:generated:end", 1)[1], original_notes.split("<!-- rigorloop:generated:end", 1)[1])
        self.assertIn("npx @xiongxianfei/rigorloop@0.3.5 init codex --json", after_first["packages/rigorloop/README.md"])
        self.assertNotIn("@0.3.4 init codex", after_first["packages/rigorloop/README.md"])
        self.assertIn("npm dist-tag: latest", after_first["docs/releases/v0.3.5.md"])
        self.assertIn("Version decision: patch", after_first["docs/releases/v0.3.5.md"])
        pending = after_first["docs/releases/v0.3.5/npm-publication.md"]
        self.assertIn("Status: pending-publication", pending)
        self.assertIn("  published: false\n", pending)
        self.assertEqual(pending.count('    result: "pending-publication"'), 2)

    def test_prepare_release_check_accepts_finalized_prepublication_evidence(self) -> None:
        with release_repo() as root:
            release_text, report_text = finalize_prepublication(root)
            finalized = relative_file_texts(root)
            before = relative_tree(root)
            checked = prepare_release("v0.3.5", root=root, check=True)
            self.assertEqual(relative_tree(root), before)

        self.assertFalse(checked.changed_paths)
        self.assertEqual(finalized["docs/releases/v0.3.5/release.yaml"], release_text)
        self.assertEqual(finalized["docs/reports/adapter-artifacts/releases/v0.3.5.yaml"], report_text)

    def test_prepare_release_check_mode_reports_pending_changes_without_writing(self) -> None:
        with release_repo() as root:
            before = relative_tree(root)

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)

            after = relative_tree(root)
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/prepare-release.py"), "v0.3.5", "--root", str(root), "--check"],
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("prepare-release would update", result.stdout + result.stderr)
            self.assertEqual(relative_tree(root), before)

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
            finalize_prepublication(root)
            self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
            path = root / "docs/releases/v0.3.5/release.yaml"
            original = path.read_text(encoding="utf-8")
            text = original
            start = text.index("adapter_paths:\n")
            end = text.index("instruction_entrypoints:\n")
            path.write_text(text[:start] + text[end:], encoding="utf-8")

            self.assertNotEqual(path.read_text(), original)
            before = relative_tree(root)

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)
            self.assertEqual(relative_tree(root), before)
            self.assertIn("prepare-release would update", "\n".join(raised.exception.errors))

        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_prepare_release_does_not_preserve_bogus_finalized_manifest(self) -> None:
        with release_repo() as root:
            finalize_prepublication(root)
            self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
            path = root / "docs/releases/v0.3.5/release.yaml"
            original = path.read_text(encoding="utf-8")
            text = original
            line = next(line for line in text.splitlines() if line.startswith("manifest_version:"))
            text = text.replace(line, "manifest_version: bogus", 1)
            path.write_text(text, encoding="utf-8")

            self.assertNotEqual(path.read_text(), original)
            before = relative_tree(root)

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)
            self.assertEqual(relative_tree(root), before)
            self.assertIn("prepare-release would update", "\n".join(raised.exception.errors))

        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_prepare_release_does_not_preserve_empty_passing_smoke_evidence(self) -> None:
        with release_repo() as root:
            finalize_prepublication(root)
            self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
            path = root / "docs/releases/v0.3.5/release.yaml"
            original = path.read_text(encoding="utf-8")
            text = original
            text = text.replace(
                '    evidence: "Controlled fixture: packed-package smoke passed for v0.3.5 codex."',
                '    evidence: ""',
            )
            path.write_text(text, encoding="utf-8")

            self.assertNotEqual(path.read_text(), original)
            before = relative_tree(root)

            with self.assertRaises(ReleaseProfileError) as raised:
                prepare_release("v0.3.5", root=root, check=True)
            self.assertEqual(relative_tree(root), before)
            self.assertIn("prepare-release would update", "\n".join(raised.exception.errors))

        self.assertIn("docs/releases/v0.3.5/release.yaml", "\n".join(raised.exception.errors))

    def test_prepare_release_does_not_preserve_whitespace_passing_smoke_fields(self) -> None:
        for field in ("tool_version", "evidence"):
            with self.subTest(field=field), release_repo() as root:
                finalize_prepublication(root)
                self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
                path = root / "docs/releases/v0.3.5/release.yaml"
                original = path.read_text(encoding="utf-8")
                text = original
                line = next(
                    item for item in text.splitlines()
                    if item.strip().startswith(f"{field}:")
                )
                path.write_text(text.replace(line, f'    {field}: "   "', 1), encoding="utf-8")

                self.assertNotEqual(path.read_text(), original)
                before = relative_tree(root)

                with self.assertRaises(ReleaseProfileError) as raised:
                    prepare_release("v0.3.5", root=root, check=True)
                self.assertEqual(relative_tree(root), before)
                self.assertIn("prepare-release would update", "\n".join(raised.exception.errors))

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
            attempts = []
            def forbid(boundary):
                def observed(*args, **kwargs):
                    attempts.append(boundary)
                    raise AssertionError(f"preparation attempted {boundary}")
                return observed
            with ExitStack() as stack:
                for boundary in ("subprocess.run", "subprocess.Popen", "urllib.request.urlopen", "socket.create_connection"):
                    stack.enter_context(patch(boundary, side_effect=forbid(boundary)))
                result = prepare_release("v0.3.5", root=root)
            self.assertEqual(attempts, [])

        self.assertEqual(result.external_actions, ())

    def test_prepare_release_cli_check_succeeds_after_generation(self) -> None:
        with release_repo() as root:
            prepare_release("v0.3.5", root=root)
            before = relative_tree(root)
            self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
            self.assertEqual(relative_tree(root), before)

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
            self.assertEqual(relative_tree(root), before)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("prepared v0.3.5: no changes", result.stdout)
        self.assertIn("next: python scripts/release-preflight.py v0.3.5", result.stdout)

    def test_prepare_release_partial_write_retry_matches_clean_preparation(self):
        with release_repo() as control, release_repo() as root:
            prepare_release("v0.3.5", root=control)
            expected = relative_tree(control)
            target = root / "docs/releases/v0.3.5/release.yaml"
            original_write = Path.write_text
            attempted = []

            def write_with_late_fault(path, *args, **kwargs):
                if path == target:
                    attempted.append(path.relative_to(root).as_posix())
                    raise OSError("injected release.yaml write failure")
                return original_write(path, *args, **kwargs)

            with patch.object(Path, "write_text", write_with_late_fault):
                with self.assertRaisesRegex(OSError, "injected release.yaml write failure"):
                    prepare_release("v0.3.5", root=root)
            self.assertEqual(attempted, ["docs/releases/v0.3.5/release.yaml"])
            self.assertEqual(json.loads((root / "packages/rigorloop/package.json").read_text())["version"], "0.3.5")
            self.assertFalse(target.exists())
            errors = validate_pending_release_artifacts("v0.3.5", root=root)
            self.assertTrue(any("release.yaml" in error and "missing" in error for error in errors), errors)
            prepare_release("v0.3.5", root=root)
            self.assertEqual(relative_tree(root), expected)
            self.assertEqual(validate_pending_release_artifacts("v0.3.5", root=root), [])
            self.assertEqual(prepare_release("v0.3.5", root=root, check=True).changed_paths, ())
