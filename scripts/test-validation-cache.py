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

        helper = validation_cache.evaluate_command_family(
            [
                "python",
                "scripts/validate-artifact-lifecycle.py",
                "--mode",
                "explicit-paths-inner-loop",
                "--path",
                "docs/plan.md",
            ]
        )
        self.assertTrue(helper.cache_eligible)
        self.assertEqual(helper.validator_id, "artifact-lifecycle")
        self.assertEqual(helper.command_family, "validate-artifact-lifecycle-explicit-paths")

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

    def test_implementation_manifest_missing_entrypoint_is_cache_ineligible(self) -> None:
        with self.assertRaises(validation_cache.CacheIdentityError) as context:
            validation_cache.build_implementation_manifest(
                self.temp_root,
                "scripts/missing-validator.py",
                manifest_generator="scripts/validation_cache.py",
            )

        self.assertEqual(context.exception.code, "implementation-entrypoint-missing")
        self.assertIn("cache eligibility disabled", str(context.exception))

    def test_implementation_manifest_unresolved_repository_import_is_cache_ineligible(self) -> None:
        self.write_file(
            "scripts/validate-artifact-lifecycle.py",
            "from scripts.missing_helper import helper\n",
        )
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")

        with self.assertRaises(validation_cache.CacheIdentityError) as context:
            validation_cache.build_implementation_manifest(
                self.temp_root,
                "scripts/validate-artifact-lifecycle.py",
                manifest_generator="scripts/validation_cache.py",
            )

        self.assertEqual(context.exception.code, "repository-local-import-unresolved")
        self.assertIn("scripts.missing_helper", str(context.exception))
        self.assertIn("cache eligibility disabled", str(context.exception))

    def test_implementation_manifest_unparseable_repository_helper_is_cache_ineligible(self) -> None:
        self.write_file(
            "scripts/validate-artifact-lifecycle.py",
            "from scripts.bad_helper import helper\n",
        )
        self.write_file("scripts/bad_helper.py", "def broken(:\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")

        with self.assertRaises(validation_cache.CacheIdentityError) as context:
            validation_cache.build_implementation_manifest(
                self.temp_root,
                "scripts/validate-artifact-lifecycle.py",
                manifest_generator="scripts/validation_cache.py",
            )

        self.assertEqual(context.exception.code, "repository-local-helper-unparseable")
        self.assertIn("scripts/bad_helper.py", str(context.exception))
        self.assertIn("cache eligibility disabled", str(context.exception))

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
            cache_key=SHA_KEY,
            validator_id="artifact-lifecycle",
            command_family="validate-artifact-lifecycle-explicit-paths",
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
            cache_key=SHA_KEY,
            validator_id="artifact-lifecycle",
            command_family="validate-artifact-lifecycle-explicit-paths",
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
            "cache_key": SHA_OTHER_KEY,
            "validator_id": "other-validator",
            "command_family": "other-family",
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

    def test_helper_reuses_direct_actual_run_cache_identity(self) -> None:
        self.write_file("scripts/validate-artifact-lifecycle.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/plan.md", "plan\n")
        direct_identity = validation_cache.build_lifecycle_cache_identity(
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
        helper_identity = validation_cache.build_lifecycle_cache_identity(
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
        context = validation_cache.LocalCacheContext(
            cache_key=helper_identity.cache_key,
            validator_id=helper_identity.validator_id,
            command_family=helper_identity.command_family,
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="2026-05-24-change",
            command_hash=helper_identity.normalized_command.command_hash,
            input_surface_hash=helper_identity.input_surface.manifest_hash,
            implementation_hash=helper_identity.implementation.manifest_hash,
            policy_hash=helper_identity.policy.manifest_hash,
        )
        record = validation_cache.make_local_cache_record(
            identity=direct_identity,
            context=context,
            prior_event_stage="closeout",
            prior_event_evidence="docs/changes/2026-05-24-change/change.yaml#validation-events",
        )

        self.assertTrue(validation_cache.local_cache_entry_eligible(record, context).eligible)

    def test_local_cache_store_reuses_only_matching_prior_pass(self) -> None:
        cache_dir = self.temp_root / ".rigorloop-validation-cache"
        now = time.time()
        record = validation_cache.LocalCacheRecord(
            cache_key=SHA_KEY,
            validator_id="artifact-lifecycle",
            command_family="validate-artifact-lifecycle-explicit-paths",
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
            prior_event_stage="unit-pass",
            prior_event_evidence="docs/changes/change/change.yaml#validation-events",
        )
        context = validation_cache.LocalCacheContext(
            cache_key=SHA_KEY,
            validator_id="artifact-lifecycle",
            command_family="validate-artifact-lifecycle-explicit-paths",
            repository_id="repo",
            branch="feature",
            worktree_id="/local/worktree",
            change_id="2026-05-23-change",
            command_hash="sha256:command",
            input_surface_hash="sha256:input",
            implementation_hash="sha256:impl",
            policy_hash="sha256:policy",
            now=now + 1,
            ttl_seconds=None,
        )

        validation_cache.store_local_cache_record(cache_dir, record)
        lookup = validation_cache.find_local_cache_hit(cache_dir, context)
        self.assertIsNotNone(lookup.record)
        self.assertEqual(lookup.record.cache_key, SHA_KEY)

        failed_dir = self.temp_root / ".rigorloop-validation-cache-failed"
        failed = record.with_updates(result="fail", cache_key=SHA_FAILED_KEY)
        validation_cache.store_local_cache_record(failed_dir, failed)
        failed_lookup = validation_cache.find_local_cache_hit(failed_dir, context)
        self.assertIsNone(failed_lookup.record)
        self.assertEqual(failed_lookup.reason, "previous result was not pass")

        for field, value, reason in (
            ("cache_key", SHA_OTHER_KEY, "cache_key changed"),
            ("validator_id", "other-validator", "validator_id changed"),
            ("command_family", "other-family", "command_family changed"),
        ):
            with self.subTest(field=field):
                mismatch_dir = self.temp_root / f".rigorloop-validation-cache-{field}"
                validation_cache.store_local_cache_record(
                    mismatch_dir,
                    record.with_updates(**{field: value}),
                )
                mismatch_lookup = validation_cache.find_local_cache_hit(mismatch_dir, context)
                self.assertIsNone(mismatch_lookup.record)
                self.assertEqual(mismatch_lookup.reason, reason)

        missing_key_dir = self.temp_root / ".rigorloop-validation-cache-missing-key"
        missing_key_record = as_local_cache_payload(record)
        del missing_key_record["cache_key"]
        write_raw_local_cache(missing_key_dir, missing_key_record)
        self.assertIsNone(validation_cache.find_local_cache_hit(missing_key_dir, context).record)

        missing_family_dir = self.temp_root / ".rigorloop-validation-cache-missing-family"
        missing_family_record = as_local_cache_payload(record)
        del missing_family_record["command_family"]
        write_raw_local_cache(missing_family_dir, missing_family_record)
        self.assertIsNone(validation_cache.find_local_cache_hit(missing_family_dir, context).record)

        missing_validator_dir = self.temp_root / ".rigorloop-validation-cache-missing-validator"
        missing_validator_record = as_local_cache_payload(record)
        del missing_validator_record["validator_id"]
        write_raw_local_cache(missing_validator_dir, missing_validator_record)
        self.assertIsNone(validation_cache.find_local_cache_hit(missing_validator_dir, context).record)

        malformed = validation_cache.local_cache_entry_eligible(
            record.with_updates(cache_key="not-a-sha-key"),
            context.with_updates(cache_key="not-a-sha-key"),
        )
        self.assertFalse(malformed.eligible)
        self.assertEqual(malformed.reason, "cache_key malformed")

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

    def test_cache_lookup_misses_after_helper_or_policy_change(self) -> None:
        cache_dir = self.temp_root / ".rigorloop-validation-cache"
        self.write_file(
            "scripts/validate-artifact-lifecycle.py",
            "from scripts.helper import VALUE\n",
        )
        self.write_file("scripts/helper.py", "VALUE = 1\n")
        self.write_file("scripts/validation_cache.py", "VALUE = 1\n")
        self.write_file("docs/plan.md", "plan\n")
        command = [
            "python",
            "scripts/validate-artifact-lifecycle.py",
            "--mode",
            "explicit-paths",
            "--path",
            "docs/plan.md",
        ]
        identity = validation_cache.build_lifecycle_cache_identity(self.temp_root, command)
        context = validation_cache.LocalCacheContext(
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
            now=time.time(),
        )
        validation_cache.store_local_cache_record(
            cache_dir,
            validation_cache.make_local_cache_record(
                identity=identity,
                context=context,
                prior_event_stage="unit-pass",
                prior_event_evidence="docs/changes/example/change.yaml#validation-events",
            ),
        )

        self.write_file("scripts/helper.py", "VALUE = 2\n")
        helper_changed = validation_cache.build_lifecycle_cache_identity(self.temp_root, command)
        helper_context = context.with_updates(
            implementation_hash=helper_changed.implementation.manifest_hash
        )
        self.assertIsNone(validation_cache.find_local_cache_hit(cache_dir, helper_context).record)

        self.write_file("scripts/helper.py", "VALUE = 1\n")
        self.write_file("docs/workflows.md", "changed workflow policy\n")
        policy_changed = validation_cache.build_lifecycle_cache_identity(self.temp_root, command)
        policy_context = context.with_updates(policy_hash=policy_changed.policy.manifest_hash)
        self.assertIsNone(validation_cache.find_local_cache_hit(cache_dir, policy_context).record)


if __name__ == "__main__":
    unittest.main()
