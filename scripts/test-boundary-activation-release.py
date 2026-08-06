#!/usr/bin/env python3
"""Integration tests for guarded boundary activation publication."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from boundary_activation_release import (
    CANONICAL_CANDIDATE,
    PublicationError,
    _atomic_push,
    check_publication,
    publication_readiness,
    publish_activation,
)


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/publish-boundary-activation.py"


def _fixture_module():
    name = "boundary_first_activation_fixture_support"
    specification = importlib.util.spec_from_file_location(
        name,
        ROOT / "scripts/test-boundary-first-validation.py",
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


FIXTURE_SUPPORT = _fixture_module()


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def initialized_repository(temporary: str) -> tuple[Path, Path, str, str, str]:
    root = Path(temporary) / "repository"
    root.mkdir()
    _, change_root, publication_base, transition, head = (
        FIXTURE_SUPPORT.initialize_candidate_fixture(root)
    )
    git(root, "tag", "v0.4.0", transition)
    return root, change_root / "evidence/boundary-activation-candidate.json", publication_base, transition, head


def advertised(root: Path) -> dict[str, str]:
    return {
        reference: identity
        for line in git(
            root,
            "ls-remote",
            "--refs",
            "origin",
            "refs/heads/main",
            "refs/tags/v0.4.0",
        ).splitlines()
        if "\t" in line
        for identity, reference in (line.split("\t", 1),)
    }


class BoundaryActivationReleaseTests(unittest.TestCase):
    def test_check_is_read_only_and_publish_atomically_updates_both_refs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, publication_base, transition, head = initialized_repository(temporary)
            before = advertised(root)
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ):
                readiness = check_publication(root, "v0.4.0", candidate)
                self.assertEqual(advertised(root), before)
                published = publish_activation(root, "v0.4.0", candidate)

            self.assertEqual(readiness.publication_head, head)
            self.assertEqual(readiness.publication_base, publication_base)
            self.assertEqual(published, readiness)
            self.assertEqual(
                advertised(root),
                {"refs/heads/main": head, "refs/tags/v0.4.0": transition},
            )

    def test_one_ref_rejection_leaves_both_remote_refs_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, _, _ = initialized_repository(temporary)
            remote = Path(git(root, "remote", "get-url", "origin"))
            hook = remote / "hooks/pre-receive"
            hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
            hook.chmod(0o755)
            before = advertised(root)
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), self.assertRaisesRegex(PublicationError, "atomic-publication-failed"):
                publish_activation(root, "v0.4.0", candidate)
            self.assertEqual(advertised(root), before)

    def test_remote_drift_and_existing_tag_block_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, transition, _ = initialized_repository(temporary)
            git(root, "push", "-q", "origin", f"{transition}:refs/tags/v0.4.0")
            before = advertised(root)
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), self.assertRaises(PublicationError):
                publish_activation(root, "v0.4.0", candidate)
            self.assertEqual(advertised(root), before)

        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, _, _ = initialized_repository(temporary)
            remote = Path(git(root, "remote", "get-url", "origin"))
            other = Path(temporary) / "other"
            subprocess.run(
                ["git", "clone", "-q", "--branch", "main", str(remote), str(other)],
                check=True,
            )
            git(other, "config", "user.email", "fixture@example.test")
            git(other, "config", "user.name", "Fixture")
            (other / "drift.txt").write_text("drift\n", encoding="utf-8")
            git(other, "add", "drift.txt")
            git(other, "commit", "-qm", "remote drift")
            git(other, "push", "-q", "origin", "HEAD:refs/heads/main")
            before = advertised(root)
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), self.assertRaises(PublicationError):
                publish_activation(root, "v0.4.0", candidate)
            self.assertEqual(advertised(root), before)
            self.assertNotIn("refs/tags/v0.4.0", before)

    def test_publish_uses_captured_full_shas_without_force_or_fallback(self) -> None:
        readiness = mock.Mock(
            release="v0.4.0",
            publication_base="1" * 40,
            transition_commit="2" * 40,
            publication_head="3" * 40,
        )
        completed = subprocess.CompletedProcess([], 0, "", "")
        with tempfile.TemporaryDirectory() as temporary, mock.patch(
            "subprocess.run",
            return_value=completed,
        ) as run:
            _atomic_push(Path(temporary), readiness, dry_run=False)
        command = run.call_args.args[0]
        self.assertIn("--atomic", command)
        self.assertNotIn("--force", command)
        self.assertFalse(any(argument.startswith("--force") for argument in command))
        self.assertIn(f"{'3' * 40}:refs/heads/main", command)
        self.assertIn(f"{'2' * 40}:refs/tags/v0.4.0", command)
        self.assertEqual(command.count("push"), 1)

    def test_local_head_movement_requires_fresh_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, _, _ = initialized_repository(temporary)
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ):
                readiness = publication_readiness(root, "v0.4.0", candidate)
            moved = Path(root / "later.txt")
            moved.write_text("later\n", encoding="utf-8")
            git(root, "add", "later.txt")
            git(root, "commit", "-qm", "move head")
            self.assertNotEqual(git(root, "rev-parse", "HEAD"), readiness.publication_head)
            with mock.patch(
                "boundary_activation_release.publication_readiness",
                return_value=readiness,
            ), self.assertRaisesRegex(PublicationError, "local-head-drift"):
                publish_activation(root, "v0.4.0", candidate)

    def test_atomic_capability_failure_is_bounded(self) -> None:
        readiness = mock.Mock(
            release="v0.4.0",
            publication_base="1" * 40,
            transition_commit="2" * 40,
            publication_head="3" * 40,
        )
        with tempfile.TemporaryDirectory() as temporary, mock.patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, ["git"]),
        ), self.assertRaisesRegex(PublicationError, "atomic-capability-unavailable"):
            _atomic_push(Path(temporary), readiness, dry_run=True)

    def test_cli_requires_one_explicit_mode(self) -> None:
        common = [
            sys.executable,
            str(CLI),
            "--release",
            "v0.4.0",
            "--candidate-evidence",
            CANONICAL_CANDIDATE.as_posix(),
        ]
        neither = subprocess.run(common, capture_output=True, text=True, check=False)
        both = subprocess.run(
            [*common, "--check", "--publish"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(neither.returncode, 0)
        self.assertNotEqual(both.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
