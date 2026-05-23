#!/usr/bin/env python3
"""Unit tests for validation cache identity primitives."""

from __future__ import annotations

import shutil
import tempfile
import time
import unittest
from pathlib import Path

import validation_cache


ROOT = Path(__file__).resolve().parents[1]


class ValidationCacheIdentityTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp_root = Path(tempfile.mkdtemp(prefix="validation-cache-test-"))
        self.addCleanup(lambda: shutil.rmtree(self.temp_root, ignore_errors=True))
        (self.temp_root / "scripts").mkdir(parents=True)
        (self.temp_root / "docs").mkdir(parents=True)
        (self.temp_root / "specs").mkdir(parents=True)
        (self.temp_root / "CONSTITUTION.md").write_text("constitution\n", encoding="utf-8")
        (self.temp_root / "docs" / "workflows.md").write_text("workflow\n", encoding="utf-8")
        (self.temp_root / "specs" / "plan-index-lifecycle-ownership.md").write_text(
            "plan policy\n",
            encoding="utf-8",
        )

    def write_file(self, relative_path: str, text: str) -> Path:
        path = self.temp_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_cacheable_command_family_is_lifecycle_explicit_paths_only(self) -> None:
        eligible = validation_cache.evaluate_command_family(
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ]
        )
        self.assertTrue(eligible.cache_eligible)
        self.assertEqual(eligible.validator_id, "artifact-lifecycle")

        unsupported_commands = [
            ["python", "scripts/validate-artifact-lifecycle.py", "--mode", "local"],
            ["python", "scripts/validate-change-metadata.py", "docs/changes/x/change.yaml"],
            ["python", "scripts/validate-review-artifacts.py", "--mode", "closeout", "docs/changes/x"],
        ]
        for command in unsupported_commands:
            with self.subTest(command=command):
                result = validation_cache.evaluate_command_family(command)
                self.assertFalse(result.cache_eligible)

    def test_normalized_argv_and_command_hash_are_deterministic(self) -> None:
        argv = ["python", "scripts/validate-artifact-lifecycle.py", "--mode", "explicit-paths"]
        self.assertEqual(validation_cache.normalize_command(argv), argv)
        self.assertEqual(
            validation_cache.normalize_command(
                "python scripts/validate-artifact-lifecycle.py --mode explicit-paths"
            ),
            argv,
        )
        self.assertEqual(
            validation_cache.command_hash(argv),
            validation_cache.command_hash(
                "python scripts/validate-artifact-lifecycle.py --mode explicit-paths"
            ),
        )

        glob_command = validation_cache.normalize_command(
            "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path 'docs/*.md'"
        )
        self.assertIn("docs/*.md", glob_command)

    def test_explicit_path_order_affects_command_hash(self) -> None:
        first = validation_cache.normalize_lifecycle_explicit_command(
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/a.md",
                "--path",
                "docs/b.md",
            ],
            self.temp_root,
        )
        second = validation_cache.normalize_lifecycle_explicit_command(
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/b.md",
                "--path",
                "docs/a.md",
            ],
            self.temp_root,
        )

        self.assertEqual(first.explicit_paths, ("docs/a.md", "docs/b.md"))
        self.assertEqual(second.explicit_paths, ("docs/b.md", "docs/a.md"))
        self.assertNotEqual(first.command_hash, second.command_hash)

    def test_repository_relative_path_normalization_accepts_safe_variants(self) -> None:
        self.assertEqual(
            validation_cache.normalize_repo_path("./docs/./plan.md", self.temp_root),
            "docs/plan.md",
        )
        self.assertEqual(
            validation_cache.normalize_repo_path("Docs/Plan.md", self.temp_root),
            "Docs/Plan.md",
        )

    def test_duplicate_explicit_paths_disable_cache_eligibility(self) -> None:
        with self.assertRaisesRegex(validation_cache.CacheIdentityError, "duplicate explicit --path"):
            validation_cache.normalize_lifecycle_explicit_command(
                [
                    "python",
                    "scripts/validate-artifact-lifecycle.py",
                    "--mode",
                    "explicit-paths",
                    "--path",
                    "./docs/plan.md",
                    "--path",
                    "docs/plan.md",
                ],
                self.temp_root,
            )

    def test_input_surface_hash_uses_content_hashes_and_missing_markers(self) -> None:
        self.write_file("docs/a.md", "alpha\n")
        first = validation_cache.build_input_surface_manifest(
            self.temp_root,
            ("docs/a.md", "docs/missing.md"),
        )
        second = validation_cache.build_input_surface_manifest(
            self.temp_root,
            ("docs/a.md", "docs/missing.md"),
        )
        self.assertEqual(first.manifest_hash, second.manifest_hash)
        self.assertEqual(first.files[1]["state"], "missing")

        self.write_file("docs/a.md", "changed\n")
        changed = validation_cache.build_input_surface_manifest(
            self.temp_root,
            ("docs/a.md", "docs/missing.md"),
        )
        self.assertNotEqual(first.manifest_hash, changed.manifest_hash)

        self.write_file("docs/missing.md", "now present\n")
        present = validation_cache.build_input_surface_manifest(
            self.temp_root,
            ("docs/a.md", "docs/missing.md"),
        )
        self.assertNotEqual(changed.manifest_hash, present.manifest_hash)

    def test_unsafe_path_values_are_rejected_before_cache_lookup(self) -> None:
        unsafe_values = [
            "/tmp/file.md",
            "C:\\Users\\alice\\repo\\docs\\plan.md",
            "~/docs/plan.md",
            "../outside.md",
            "https://example.com/docs/plan.md",
            "example.com/docs/plan.md",
            "https://token@example.com/docs/plan.md",
            "$HOME/docs/plan.md",
            "docs/*.md",
        ]
        for value in unsafe_values:
            with self.subTest(value=value):
                with self.assertRaises(validation_cache.CacheIdentityError):
                    validation_cache.normalize_repo_path(value, self.temp_root)

    def test_implementation_manifest_is_deterministic_and_complete(self) -> None:
        self.write_file(
            "scripts/validate-artifact-lifecycle.py",
            "import os\nimport helper\nfrom nested import tool\n",
        )
        self.write_file("scripts/helper.py", "import json\n")
        self.write_file("scripts/nested.py", "from sub import leaf\n")
        self.write_file("scripts/sub.py", "VALUE = 1\n")

        manifest = validation_cache.build_implementation_manifest(
            self.temp_root,
            "scripts/validate-artifact-lifecycle.py",
            manifest_generator="scripts/validation_cache.py",
        )
        paths = [entry["path"] for entry in manifest.files]
        self.assertIn("scripts/validate-artifact-lifecycle.py", paths)
        self.assertIn("scripts/helper.py", paths)
        self.assertIn("scripts/nested.py", paths)
        self.assertIn("scripts/sub.py", paths)
        self.assertIn("scripts/validation_cache.py", paths)
        self.assertNotIn("os.py", paths)
        self.assertEqual(manifest.manifest_hash, validation_cache.build_implementation_manifest(
            self.temp_root,
            "scripts/validate-artifact-lifecycle.py",
            manifest_generator="scripts/validation_cache.py",
        ).manifest_hash)

    def test_policy_config_manifest_is_deterministic(self) -> None:
        manifest = validation_cache.build_policy_manifest(
            self.temp_root,
            extra_policy_files=("specs/validation-idempotency-and-cache-hit-safety.md",),
        )
        paths = [entry["path"] for entry in manifest.files]
        self.assertEqual(
            paths,
            [
                "CONSTITUTION.md",
                "docs/workflows.md",
                "specs/plan-index-lifecycle-ownership.md",
                "specs/validation-idempotency-and-cache-hit-safety.md",
            ],
        )
        self.assertEqual(manifest.files[-1]["state"], "missing")

        self.write_file("specs/validation-idempotency-and-cache-hit-safety.md", "spec\n")
        changed = validation_cache.build_policy_manifest(
            self.temp_root,
            extra_policy_files=("specs/validation-idempotency-and-cache-hit-safety.md",),
        )
        self.assertNotEqual(manifest.manifest_hash, changed.manifest_hash)

    def test_local_execution_cache_is_branch_worktree_and_change_local(self) -> None:
        now = time.time()
        record = validation_cache.LocalCacheRecord(
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="2026-05-23-change",
            command_hash="sha256:command",
            input_surface_hash="sha256:input",
            implementation_hash="sha256:impl",
            policy_hash="sha256:policy",
            result="pass",
            created_at=now,
        )
        context = validation_cache.LocalCacheContext(
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="2026-05-23-change",
            command_hash="sha256:command",
            input_surface_hash="sha256:input",
            implementation_hash="sha256:impl",
            policy_hash="sha256:policy",
            now=now + 1,
            ttl_seconds=24 * 60 * 60,
        )
        self.assertTrue(validation_cache.local_cache_entry_eligible(record, context).eligible)

        mismatches = {
            "branch": "other",
            "worktree_id": "/other/worktree",
            "change_id": "2026-05-23-other",
            "result": "fail",
        }
        for field, value in mismatches.items():
            with self.subTest(field=field):
                changed_record = record.with_updates(**{field: value})
                result = validation_cache.local_cache_entry_eligible(changed_record, context)
                self.assertFalse(result.eligible)

        expired = validation_cache.local_cache_entry_eligible(
            record,
            context.with_updates(now=now + 90_000),
        )
        self.assertFalse(expired.eligible)


if __name__ == "__main__":
    unittest.main()
