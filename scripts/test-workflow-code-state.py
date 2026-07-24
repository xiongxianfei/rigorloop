#!/usr/bin/env python3
"""Canonical final-code state provider regression tests."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from workflow_code_state import (
    CodeStateError,
    GitCodeStateAnchorResolver,
    GitCodeStateProvider,
    resolve_canonical_code_state,
)


class GitCodeStateProviderTests(unittest.TestCase):
    def git(self, root: Path, *args: str) -> str:
        result = subprocess.run(
            ("git", "-C", str(root), *args),
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def write(self, root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, root: Path, message: str) -> str:
        self.git(root, "add", "-A")
        self.git(root, "commit", "-m", message)
        return self.git(root, "rev-parse", "HEAD")

    def make_repository(self) -> tuple[Path, str]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.git(root, "init", "-q")
        self.git(root, "config", "user.name", "Test User")
        self.git(root, "config", "user.email", "test@example.com")
        self.write(root, "scripts/modified.py", "value = 1\n")
        self.write(root, "scripts/deleted.py", "delete_me = True\n")
        self.write(root, "scripts/renamed.py", "rename_me = True\n")
        base = self.commit(root, "base")
        self.git(root, "checkout", "-q", "-b", "feature")
        return root, base

    def provider(
        self, root: Path, reviewed: str
    ) -> GitCodeStateProvider:
        anchor = GitCodeStateAnchorResolver().resolve(
            root,
            change_id="2026-07-20-example",
            reviewed_revision=reviewed,
            final_review_id="code-review-final-r1",
            lifecycle_evidence_paths=frozenset(),
        )
        return GitCodeStateProvider(anchor=anchor)

    def test_snapshot_covers_added_modified_deleted_and_renamed_paths(self) -> None:
        root, base = self.make_repository()
        self.write(root, "scripts/modified.py", "value = 2\n")
        self.write(root, "scripts/added.py", "added = True\n")
        (root / "scripts/deleted.py").unlink()
        self.git(root, "mv", "scripts/renamed.py", "scripts/moved.py")
        reviewed = self.commit(root, "reviewed")

        snapshot = self.provider(root, reviewed).snapshot(root)

        self.assertEqual(
            set(snapshot.paths),
            {
                "scripts/added.py",
                "scripts/deleted.py",
                "scripts/modified.py",
                "scripts/moved.py",
                "scripts/renamed.py",
            },
        )
        self.assertEqual(
            {entry.status for entry in snapshot.entries},
            {"A", "D", "M", "R"},
        )

    def test_snapshot_rejects_dirty_tracked_and_untracked_code(self) -> None:
        root, base = self.make_repository()
        self.write(root, "scripts/modified.py", "value = 2\n")
        reviewed = self.commit(root, "reviewed")
        provider = self.provider(root, reviewed)

        self.write(root, "scripts/modified.py", "value = 3\n")
        with self.assertRaisesRegex(CodeStateError, "worktree differs"):
            provider.snapshot(root)

        self.git(root, "restore", "scripts/modified.py")
        self.write(root, "scripts/untracked.py", "untracked = True\n")
        with self.assertRaisesRegex(CodeStateError, "worktree differs"):
            provider.snapshot(root)

    def test_snapshot_rejects_committed_code_after_reviewed_revision(self) -> None:
        root, base = self.make_repository()
        self.write(root, "scripts/modified.py", "value = 2\n")
        reviewed = self.commit(root, "reviewed")
        self.write(root, "scripts/later.py", "later = True\n")
        self.commit(root, "later code")

        with self.assertRaisesRegex(CodeStateError, "HEAD differs"):
            self.provider(root, reviewed).snapshot(root)

    def test_resolver_rejects_code_path_post_review_exemptions(self) -> None:
        root, _base = self.make_repository()
        reviewed = self.git(root, "rev-parse", "HEAD")
        with self.assertRaisesRegex(
            CodeStateError, "not a lifecycle evidence path"
        ):
            GitCodeStateAnchorResolver().resolve(
                root,
                change_id="2026-07-20-example",
                reviewed_revision=reviewed,
                final_review_id="code-review-final-r1",
                lifecycle_evidence_paths=frozenset(
                    {"scripts/hidden.py"}
                ),
            )

    def test_resolver_uses_default_branch_merge_base_not_later_commit(self) -> None:
        root, base = self.make_repository()
        self.write(root, "scripts/earlier.py", "earlier = True\n")
        self.commit(root, "earlier")
        later_base = self.git(root, "rev-parse", "HEAD")
        self.write(root, "scripts/later.py", "later = True\n")
        reviewed = self.commit(root, "reviewed")

        anchor = GitCodeStateAnchorResolver().resolve(
            root,
            change_id="2026-07-20-example",
            reviewed_revision=reviewed,
            final_review_id="code-review-final-r1",
            lifecycle_evidence_paths=frozenset(),
        )
        snapshot = GitCodeStateProvider(anchor=anchor).snapshot(root)

        self.assertEqual(anchor.base_revision, base)
        self.assertNotEqual(anchor.base_revision, later_base)
        self.assertEqual(
            set(snapshot.paths),
            {"scripts/earlier.py", "scripts/later.py"},
        )

    def test_git_repository_rejects_test_only_provider_substitution(self) -> None:
        root, _base = self.make_repository()
        reviewed = self.git(root, "rev-parse", "HEAD")

        class TestOnlyProvider:
            test_only = True

            def snapshot(self, _repository_root: Path):
                raise AssertionError("fixture provider must not be invoked")

        with self.assertRaisesRegex(
            CodeStateError, "test-only code-state provider"
        ):
            resolve_canonical_code_state(
                repository_root=root,
                change_id="2026-07-20-example",
                reviewed_revision=reviewed,
                final_review_id="code-review-final-r1",
                lifecycle_evidence_paths=frozenset(),
                test_provider=TestOnlyProvider(),
            )

    def test_provider_rejects_target_branch_drift_after_anchor_resolution(self) -> None:
        root, _base = self.make_repository()
        self.write(root, "scripts/feature.py", "feature = True\n")
        reviewed = self.commit(root, "reviewed")
        anchor = GitCodeStateAnchorResolver().resolve(
            root,
            change_id="2026-07-20-example",
            reviewed_revision=reviewed,
            final_review_id="code-review-final-r1",
            lifecycle_evidence_paths=frozenset(),
        )
        self.git(root, "checkout", "-q", "master")
        self.write(root, "scripts/target.py", "target = True\n")
        self.commit(root, "target moved")
        self.git(root, "checkout", "-q", "feature")

        with self.assertRaisesRegex(
            CodeStateError, "target branch identity is stale"
        ):
            GitCodeStateProvider(anchor=anchor).snapshot(root)


if __name__ == "__main__":
    unittest.main()
