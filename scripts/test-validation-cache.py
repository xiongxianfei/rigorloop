#!/usr/bin/env python3
"""Unit tests for validation cache identity primitives."""

from __future__ import annotations

import json
import shutil
import tempfile
import time
import unittest
from pathlib import Path

import validation_cache


ROOT = Path(__file__).resolve().parents[1]
SHA_KEY = "sha256:" + "a" * 64
SHA_OTHER_KEY = "sha256:" + "b" * 64
SHA_FAILED_KEY = "sha256:" + "c" * 64


def as_local_cache_payload(record: validation_cache.LocalCacheRecord) -> dict[str, object]:
    return dict(record.__dict__)


def write_raw_local_cache(cache_dir: Path, record: dict[str, object]) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / "validation-cache.json").write_text(
        json.dumps({"schema_version": 1, "records": [record]}, sort_keys=True),
        encoding="utf-8",
    )


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

    def test_implementation_manifest_is_deterministic_and_complete(self) -> None:
        self.write_file(
            "scripts/validate-artifact-lifecycle.py",
            "import os\nimport pathlib\nimport yaml\nimport helper\nfrom nested import tool\n",
        )
        self.write_file("scripts/helper.py", "import json\n")
        self.write_file("scripts/nested.py", "from sub import leaf\n")
        self.write_file("scripts/sub.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")

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
        self.assertNotIn("pathlib.py", paths)
        self.assertNotIn("yaml.py", paths)
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
                "AGENTS.md",
                "CONSTITUTION.md",
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

    def test_lifecycle_cache_identity_combines_key_components(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/plan.md", "plan\n")

        identity = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ],
        )

        self.assertEqual(identity.validator_id, "artifact-lifecycle")
        self.assertEqual(identity.normalized_command.explicit_paths, ("docs/plan.md",))
        self.assertTrue(identity.cache_key.startswith("sha256:"))
        self.assertIn("docs/plan.md", [entry["path"] for entry in identity.input_surface.files])

        self.write_file("docs/plan.md", "changed\n")
        changed = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ],
        )
        self.assertNotEqual(identity.cache_key, changed.cache_key)

    def test_helper_identity_uses_canonical_direct_argv_and_preserves_display_argv(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/plan.md", "plan\n")

        direct = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "./docs/plan.md",
            ],
        )
        helper = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths-inner-loop",
                "--path",
                "./docs/plan.md",
            ],
        )

        self.assertEqual(helper.normalized_command.argv, direct.normalized_command.argv)
        self.assertEqual(helper.normalized_command.command_hash, direct.normalized_command.command_hash)
        self.assertEqual(helper.cache_key, direct.cache_key)
        self.assertEqual(
            helper.displayed_command.argv,
            (
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths-inner-loop",
                "--path",
                "docs/plan.md",
            ),
        )
        self.assertEqual(
            helper.normalized_command.argv,
            (
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ),
        )

    def test_helper_path_order_changes_canonical_identity(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/a.md", "a\n")
        self.write_file("docs/b.md", "b\n")

        first = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths-inner-loop",
                "--path",
                "docs/a.md",
                "--path",
                "docs/b.md",
            ],
        )
        second = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths-inner-loop",
                "--path",
                "docs/b.md",
                "--path",
                "docs/a.md",
            ],
        )

        self.assertNotEqual(first.normalized_command.command_hash, second.normalized_command.command_hash)
        self.assertNotEqual(first.cache_key, second.cache_key)

    def test_formal_cache_hit_evidence_file_has_required_shape(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/changes/example/change.yaml", "schema_version: 2\n")
        self.write_file("docs/plan.md", "plan\n")
        identity = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ],
        )
        record = validation_cache.LocalCacheRecord(
            cache_key=identity.cache_key,
            validator_id=identity.validator_id,
            command_family=identity.command_family,
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="example",
            command_hash=identity.normalized_command.command_hash,
            input_surface_hash=identity.input_surface.manifest_hash,
            implementation_hash=identity.implementation.manifest_hash,
            policy_hash=identity.policy.manifest_hash,
            result="pass",
            created_at=time.time(),
            prior_event_stage="unit-pass",
            prior_event_evidence="docs/changes/example/change.yaml#validation-events",
        )

        evidence_path = validation_cache.write_cache_hit_evidence(
            repo_root=self.temp_root,
            evidence_file="docs/changes/example/validation-cache-evidence.yaml",
            change_id="example",
            cache_hit_id="cache-hit-001",
            identity=identity,
            record=record,
        )

        text = (self.temp_root / evidence_path).read_text(encoding="utf-8")
        self.assertIn("schema_version: 1", text)
        self.assertIn("change_id: \"example\"", text)
        self.assertIn("id: \"cache-hit-001\"", text)
        self.assertIn("validator_id: \"artifact-lifecycle\"", text)
        self.assertIn("command_family: \"validate-artifact-lifecycle-explicit-paths\"", text)
        self.assertIn("evidence_kind: cache-hit-inner-loop", text)
        self.assertIn("displayed_command_argv:", text)
        self.assertIn("canonical_cache_argv:", text)
        self.assertIn("result_reused: pass", text)
        self.assertIn("scope: inner-loop", text)
        self.assertIn("closeout_evidence: false", text)
        self.assertNotIn("/local/worktree", text)

    def test_helper_cache_hit_evidence_preserves_displayed_and_canonical_argv(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/changes/example/change.yaml", "schema_version: 2\n")
        self.write_file("docs/plan.md", "plan\n")
        identity = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths-inner-loop",
                "--path",
                "docs/plan.md",
            ],
        )
        record = validation_cache.LocalCacheRecord(
            cache_key=identity.cache_key,
            validator_id=identity.validator_id,
            command_family=identity.command_family,
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="example",
            command_hash=identity.normalized_command.command_hash,
            input_surface_hash=identity.input_surface.manifest_hash,
            implementation_hash=identity.implementation.manifest_hash,
            policy_hash=identity.policy.manifest_hash,
            result="pass",
            created_at=time.time(),
            prior_event_stage="unit-pass",
            prior_event_evidence="docs/changes/example/change.yaml#validation-events",
        )

        evidence_path = validation_cache.write_cache_hit_evidence(
            repo_root=self.temp_root,
            evidence_file="docs/changes/example/validation-cache-evidence.yaml",
            change_id="example",
            cache_hit_id="cache-hit-001",
            identity=identity,
            record=record,
        )

        text = (self.temp_root / evidence_path).read_text(encoding="utf-8")
        self.assertIn("displayed_command_argv:", text)
        self.assertIn("canonical_cache_argv:", text)
        self.assertIn("explicit-paths-inner-loop", text)
        self.assertIn("explicit-paths", text)
        self.assertIn("command_family: \"validate-artifact-lifecycle-explicit-paths\"", text)

    def test_formal_cache_hit_evidence_merges_and_replaces_by_id(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/changes/example/change.yaml", "schema_version: 2\n")
        self.write_file("docs/plan.md", "plan\n")
        identity = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ],
        )
        record = validation_cache.LocalCacheRecord(
            cache_key=identity.cache_key,
            validator_id=identity.validator_id,
            command_family=identity.command_family,
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="example",
            command_hash=identity.normalized_command.command_hash,
            input_surface_hash=identity.input_surface.manifest_hash,
            implementation_hash=identity.implementation.manifest_hash,
            policy_hash=identity.policy.manifest_hash,
            result="pass",
            prior_event_stage="first-pass",
            prior_event_evidence="docs/changes/example/change.yaml#validation-events",
        )
        evidence_file = "docs/changes/example/validation-cache-evidence.yaml"
        evidence_path = validation_cache.write_cache_hit_evidence(
            repo_root=self.temp_root,
            evidence_file=evidence_file,
            change_id="example",
            cache_hit_id="cache-hit-001",
            identity=identity,
            record=record,
        )
        validation_cache.write_cache_hit_evidence(
            repo_root=self.temp_root,
            evidence_file=evidence_file,
            change_id="example",
            cache_hit_id="cache-hit-002",
            identity=identity,
            record=record.with_updates(prior_event_stage="second-pass"),
        )

        text = (self.temp_root / evidence_path).read_text(encoding="utf-8")
        self.assertIn("id: \"cache-hit-001\"", text)
        self.assertIn("id: \"cache-hit-002\"", text)
        self.assertIn("stage: \"first-pass\"", text)
        self.assertIn("stage: \"second-pass\"", text)

        validation_cache.write_cache_hit_evidence(
            repo_root=self.temp_root,
            evidence_file=evidence_file,
            change_id="example",
            cache_hit_id="cache-hit-001",
            identity=identity,
            record=record.with_updates(prior_event_stage="replacement-pass"),
        )
        replaced = (self.temp_root / evidence_path).read_text(encoding="utf-8")
        self.assertIn("id: \"cache-hit-001\"", replaced)
        self.assertIn("id: \"cache-hit-002\"", replaced)
        self.assertIn("stage: \"replacement-pass\"", replaced)
        self.assertNotIn("stage: \"first-pass\"", replaced)
        self.assertIn("stage: \"second-pass\"", replaced)

    def test_formal_cache_hit_evidence_rejects_malformed_existing_file(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/changes/example/change.yaml", "schema_version: 2\n")
        self.write_file("docs/plan.md", "plan\n")
        identity = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ],
        )
        record = validation_cache.LocalCacheRecord(
            cache_key=identity.cache_key,
            validator_id=identity.validator_id,
            command_family=identity.command_family,
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="example",
            command_hash=identity.normalized_command.command_hash,
            input_surface_hash=identity.input_surface.manifest_hash,
            implementation_hash=identity.implementation.manifest_hash,
            policy_hash=identity.policy.manifest_hash,
            result="pass",
            prior_event_stage="unit-pass",
            prior_event_evidence="docs/changes/example/change.yaml#validation-events",
        )
        target = self.temp_root / "docs/changes/example/validation-cache-evidence.yaml"
        target.write_text(
            "schema_version: 2\nchange_id: \"example\"\ncache_hits:\n",
            encoding="utf-8",
        )

        with self.assertRaises(validation_cache.CacheIdentityError) as schema_context:
            validation_cache.write_cache_hit_evidence(
                repo_root=self.temp_root,
                evidence_file="docs/changes/example/validation-cache-evidence.yaml",
                change_id="example",
                cache_hit_id="cache-hit-001",
                identity=identity,
                record=record,
            )
        self.assertEqual(schema_context.exception.code, "invalid-cache-evidence-file")

        target.unlink()
        validation_cache.write_cache_hit_evidence(
            repo_root=self.temp_root,
            evidence_file="docs/changes/example/validation-cache-evidence.yaml",
            change_id="example",
            cache_hit_id="cache-hit-001",
            identity=identity,
            record=record,
        )
        text = target.read_text(encoding="utf-8")
        duplicate_entry = text.split("cache_hits:\n", 1)[1]
        target.write_text(text.rstrip() + "\n" + duplicate_entry, encoding="utf-8")

        with self.assertRaises(validation_cache.CacheIdentityError) as duplicate_context:
            validation_cache.write_cache_hit_evidence(
                repo_root=self.temp_root,
                evidence_file="docs/changes/example/validation-cache-evidence.yaml",
                change_id="example",
                cache_hit_id="cache-hit-002",
                identity=identity,
                record=record,
            )
        self.assertEqual(duplicate_context.exception.code, "duplicate-cache-hit-id")

    def test_formal_cache_hit_evidence_rejects_unsafe_file_path(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/plan.md", "plan\n")
        identity = validation_cache.build_lifecycle_cache_identity(
            self.temp_root,
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths",
                "--path",
                "docs/plan.md",
            ],
        )
        record = validation_cache.LocalCacheRecord(
            cache_key=identity.cache_key,
            validator_id=identity.validator_id,
            command_family=identity.command_family,
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="example",
            command_hash=identity.normalized_command.command_hash,
            input_surface_hash=identity.input_surface.manifest_hash,
            implementation_hash=identity.implementation.manifest_hash,
            policy_hash=identity.policy.manifest_hash,
            result="pass",
            prior_event_stage="unit-pass",
            prior_event_evidence="docs/changes/example/change.yaml#validation-events",
        )

        with self.assertRaises(validation_cache.CacheIdentityError):
            validation_cache.write_cache_hit_evidence(
                repo_root=self.temp_root,
                evidence_file="/tmp/validation-cache-evidence.yaml",
                change_id="example",
                cache_hit_id="cache-hit-001",
                identity=identity,
                record=record,
            )

if __name__ == "__main__":
    unittest.main()
