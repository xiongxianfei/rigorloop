#!/usr/bin/env python3
"""Integration tests for guarded boundary activation publication."""

from __future__ import annotations

import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

from boundary_activation_release import (
    CANONICAL_CANDIDATE,
    PublicationError,
    PublicationReadiness,
    _atomic_push,
    _guard_script,
    check_publication,
    error_payload,
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


def fixture_readiness(
    candidate: Path,
    publication_base: str,
    transition: str,
    head: str,
) -> PublicationReadiness:
    data = json.loads(candidate.read_text(encoding="utf-8"))
    return PublicationReadiness(
        release="v0.4.0",
        publication_base=publication_base,
        grandfathering_baseline=data["grandfathering_baseline"],
        transition_commit=transition,
        candidate_validation_head=data["candidate_validation_head"],
        publication_head=head,
    )


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
            sentinel = "PRIVATE_REMOTE_TOKEN_9471"
            hook.write_text(
                f"#!/bin/sh\nprintf '%s\\n' '{sentinel}' >&2\nexit 1\n",
                encoding="utf-8",
            )
            hook.chmod(0o755)
            before = advertised(root)
            with mock.patch.dict(os.environ, {"PRIVATE_API_KEY": sentinel}), mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), self.assertRaisesRegex(PublicationError, "atomic-publication-failed") as raised:
                publish_activation(root, "v0.4.0", candidate)
            self.assertEqual(advertised(root), before)
            self.assertNotIn(sentinel, json.dumps(error_payload(raised.exception)))

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
        readiness = PublicationReadiness(
            release="v0.4.0",
            publication_base="1" * 40,
            grandfathering_baseline="4" * 40,
            transition_commit="2" * 40,
            candidate_validation_head="5" * 40,
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
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, publication_base, transition, head = initialized_repository(temporary)
            remote = Path(git(root, "remote", "get-url", "origin"))
            git(remote, "config", "receive.advertiseAtomic", "false")
            readiness = fixture_readiness(candidate, publication_base, transition, head)
            before = advertised(root)
            with self.assertRaisesRegex(PublicationError, "atomic-capability-unavailable"):
                _atomic_push(root, readiness, dry_run=True)
            self.assertEqual(advertised(root), before)

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

    def test_candidate_path_rejects_alias_and_canonical_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, _, _ = initialized_repository(temporary)
            alias = root / "candidate-alias.json"
            alias.symlink_to(candidate)
            with self.assertRaisesRegex(PublicationError, "candidate-evidence-path-invalid"):
                publication_readiness(root, "v0.4.0", alias)

            lexical_alias = CANONICAL_CANDIDATE.parent / ".." / "evidence" / CANONICAL_CANDIDATE.name
            with self.assertRaisesRegex(PublicationError, "candidate-evidence-path-invalid"):
                publication_readiness(root, "v0.4.0", lexical_alias)

            target = candidate.with_suffix(".real.json")
            candidate.rename(target)
            candidate.symlink_to(target.name)
            with self.assertRaisesRegex(PublicationError, "candidate-evidence-path-invalid"):
                publication_readiness(root, "v0.4.0", candidate)

    def test_guard_rejects_same_push_advertisement_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            hook = temporary_root / "pre-push"
            hook.write_text(_guard_script(), encoding="utf-8")
            fake_bin = temporary_root / "bin"
            fake_bin.mkdir()
            fake_git = fake_bin / "git"
            fake_git.write_text(
                "#!/bin/sh\nprintf '%s\\trefs/heads/main\\n' \"$RIGORLOOP_EXPECTED_REMOTE_MAIN\"\n",
                encoding="utf-8",
            )
            fake_git.chmod(0o755)
            environment = {
                **os.environ,
                "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
                "RIGORLOOP_ACTIVATION_RELEASE": "v0.4.0",
                "RIGORLOOP_EXPECTED_REMOTE_MAIN": "1" * 40,
                "RIGORLOOP_EXPECTED_PUBLICATION_HEAD": "2" * 40,
                "RIGORLOOP_EXPECTED_TRANSITION": "3" * 40,
            }
            valid_tag = (
                f"{'3' * 40} {'3' * 40} refs/tags/v0.4.0 {'0' * 40}\n"
            )
            mismatched_main = (
                f"{'2' * 40} {'2' * 40} refs/heads/main {'4' * 40}\n"
            )
            valid_main = (
                f"{'2' * 40} {'2' * 40} refs/heads/main {'1' * 40}\n"
            )
            cases = (
                (mismatched_main + valid_tag, "remote-main-drift"),
                (valid_main, "push-mapping-invalid"),
                (valid_main + valid_main + valid_tag, "push-mapping-invalid"),
                (
                    valid_main
                    + f"{'3' * 40} {'3' * 40} refs/tags/other {'0' * 40}\n",
                    "push-mapping-invalid",
                ),
            )
            for hook_input, expected_code in cases:
                with self.subTest(expected_code=expected_code, hook_input=hook_input):
                    completed = subprocess.run(
                        [sys.executable, str(hook), "origin", "fixture"],
                        input=hook_input,
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertIn(f"RIGORLOOP_GUARD:{expected_code}", completed.stderr)

    def test_post_readiness_remote_race_is_classified_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, publication_base, transition, head = initialized_repository(temporary)
            readiness = fixture_readiness(candidate, publication_base, transition, head)
            remote = Path(git(root, "remote", "get-url", "origin"))
            other = Path(temporary) / "race"
            subprocess.run(["git", "clone", "-q", "--branch", "main", str(remote), str(other)], check=True)
            git(other, "config", "user.email", "fixture@example.test")
            git(other, "config", "user.name", "Fixture")
            (other / "race.txt").write_text("race\n", encoding="utf-8")
            git(other, "add", "race.txt")
            git(other, "commit", "-qm", "race")
            git(other, "push", "-q", "origin", "HEAD:refs/heads/main")
            before = advertised(root)
            with mock.patch(
                "boundary_activation_release.publication_readiness",
                return_value=readiness,
            ), self.assertRaisesRegex(PublicationError, "remote-main-drift") as raised:
                publish_activation(root, "v0.4.0", candidate)
            self.assertEqual(advertised(root), before)
            payload = error_payload(raised.exception)
            self.assertEqual(payload["mode"], "publish")
            self.assertEqual(payload["publication_base"], publication_base)
            self.assertIn("expected_invariant", payload)
            self.assertIn("corrective_action", payload)

    def test_non_fast_forward_head_and_modified_evidence_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, _, _ = initialized_repository(temporary)
            tree = git(root, "rev-parse", "HEAD^{tree}")
            detached = subprocess.run(
                ["git", "commit-tree", tree, "-m", "unrelated"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            git(root, "reset", "--hard", detached)
            with mock.patch(
                "boundary_activation_release.validate_activation_publication_readiness",
                return_value=(),
            ), self.assertRaisesRegex(PublicationError, "publication-not-fast-forward"):
                publication_readiness(root, "v0.4.0", candidate)

        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, _, _ = initialized_repository(temporary)
            data = json.loads(candidate.read_text(encoding="utf-8"))
            data["candidate_validation_head"] = "f" * 40
            candidate.write_text(json.dumps(data), encoding="utf-8")
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), self.assertRaisesRegex(PublicationError, "publication-readiness-failed") as raised:
                publication_readiness(root, "v0.4.0", candidate)
            self.assertIn("restore settled lifecycle", error_payload(raised.exception)["corrective_action"])

    def test_valid_cli_modes_and_private_diagnostics(self) -> None:
        specification = importlib.util.spec_from_file_location("publication_cli", CLI)
        assert specification is not None and specification.loader is not None
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        readiness = PublicationReadiness(
            release="v0.4.0",
            publication_base="1" * 40,
            grandfathering_baseline="2" * 40,
            transition_commit="3" * 40,
            candidate_validation_head="4" * 40,
            publication_head="5" * 40,
        )
        common = [
            str(CLI), "--release", "v0.4.0", "--candidate-evidence",
            CANONICAL_CANDIDATE.as_posix(),
        ]
        for flag, function_name, status in (
            ("--check", "check_publication", "ready"),
            ("--publish", "publish_activation", "published"),
        ):
            output = io.StringIO()
            with mock.patch.object(sys, "argv", [*common, flag]), mock.patch.object(
                module, function_name, return_value=readiness
            ), redirect_stdout(output):
                self.assertEqual(module.main(), 0)
            self.assertEqual(json.loads(output.getvalue())["status"], status)

        private_sentinels = ("PRIVATE_TOKEN_9471", "/tmp/private-machine-path", "host-secret")
        error = PublicationError(
            "atomic-publication-failed", **readiness.error_context("publish")
        )
        serialized = json.dumps(error_payload(error), sort_keys=True)
        for sentinel in private_sentinels:
            self.assertNotIn(sentinel, serialized)


if __name__ == "__main__":
    unittest.main(verbosity=2)
