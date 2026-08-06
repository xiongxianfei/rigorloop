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
            hook = remote / "hooks/update"
            sentinel = "a" * 40
            hook.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = refs/tags/v0.4.0 ]; then\n"
                f"  printf '%s\\n' 'RIGORLOOP_GUARD:remote-main-drift:{sentinel}' >&2\n"
                "  exit 1\n"
                "fi\n"
                "exit 0\n",
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
            payload = error_payload(raised.exception)
            self.assertEqual(payload["code"], "atomic-publication-failed")
            self.assertNotIn(sentinel, json.dumps(payload))

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
            result_path = temporary_root / "guard-result"
            nonce = "b" * 64
            hook.write_text(_guard_script(result_path, nonce), encoding="utf-8")
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
                    self.assertEqual(
                        result_path.read_text(encoding="utf-8").split("\t")[1].strip(),
                        expected_code,
                    )
                    result_path.unlink()

    def test_untrusted_exact_stderr_cannot_forge_guard_result(self) -> None:
        sentinel = "a" * 40
        nonce = "b" * 64
        readiness = PublicationReadiness(
            release="v0.4.0",
            publication_base="1" * 40,
            grandfathering_baseline="2" * 40,
            transition_commit="3" * 40,
            candidate_validation_head="4" * 40,
            publication_head="5" * 40,
        )
        untrusted = f"{nonce}\tremote-main-drift\t{sentinel}\n"
        failure = subprocess.CalledProcessError(
            1, ["git", "push"], stderr=untrusted
        )
        with tempfile.TemporaryDirectory() as temporary, mock.patch(
            "boundary_activation_release.secrets.token_hex", return_value=nonce
        ), mock.patch("subprocess.run", side_effect=failure), self.assertRaisesRegex(
            PublicationError, "atomic-publication-failed"
        ) as raised:
            _atomic_push(Path(temporary), readiness, dry_run=False)
        payload = error_payload(raised.exception)
        self.assertEqual(payload["code"], "atomic-publication-failed")
        self.assertNotIn(sentinel, json.dumps(payload))

    def test_malformed_guard_results_are_bounded_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, publication_base, transition, head = initialized_repository(temporary)
            readiness = fixture_readiness(candidate, publication_base, transition, head)
            before = advertised(root)
            cases = ("invalid-utf8", "oversized", "wrong-nonce", "multi-record", "symlink")

            for case in cases:
                def malformed_hook(result_path: Path, nonce: str, *, selected: str = case) -> str:
                    valid = f"{nonce}\tremote-main-drift\t{'a' * 40}\n".encode()
                    payload = {
                        "invalid-utf8": b"\xff\xfe",
                        "oversized": b"x" * 257,
                        "wrong-nonce": f"{'0' * 64}\tremote-main-drift\t{'a' * 40}\n".encode(),
                        "multi-record": valid + valid,
                        "symlink": valid,
                    }[selected]
                    if selected == "symlink":
                        target = result_path.with_name("guard-target")
                        body = (
                            "from pathlib import Path\n"
                            f"target = Path({str(target)!r})\n"
                            f"target.write_bytes({payload!r})\n"
                            f"Path({str(result_path)!r}).symlink_to(target)\n"
                            "raise SystemExit(1)\n"
                        )
                    else:
                        body = (
                            "from pathlib import Path\n"
                            f"Path({str(result_path)!r}).write_bytes({payload!r})\n"
                            "raise SystemExit(1)\n"
                        )
                    return "#!/usr/bin/env python3\n" + body

                with self.subTest(case=case), mock.patch(
                    "boundary_activation_release._guard_script",
                    side_effect=malformed_hook,
                ), self.assertRaisesRegex(
                    PublicationError, "atomic-publication-failed"
                ) as raised:
                    _atomic_push(root, readiness, dry_run=False)
                self.assertEqual(error_payload(raised.exception)["code"], "atomic-publication-failed")
                self.assertEqual(advertised(root), before)

    def test_post_readiness_tag_races_are_precise_and_read_only(self) -> None:
        for same_target in (True, False):
            with self.subTest(same_target=same_target), tempfile.TemporaryDirectory() as temporary:
                root, candidate, publication_base, transition, head = initialized_repository(temporary)
                with mock.patch(
                    "boundary_first_validation._publication_authority_issues",
                    return_value=(),
                ):
                    readiness = publication_readiness(root, "v0.4.0", candidate)
                raced_tag = transition if same_target else publication_base
                git(root, "push", "-q", "origin", f"{raced_tag}:refs/tags/v0.4.0")
                before = advertised(root)
                with mock.patch(
                    "boundary_activation_release.publication_readiness",
                    return_value=readiness,
                ), self.assertRaisesRegex(PublicationError, "remote-tag-exists") as raised:
                    publish_activation(root, "v0.4.0", candidate)
                payload = error_payload(raised.exception)
                self.assertEqual(payload["conflicting_remote_tag"], raced_tag)
                self.assertEqual(advertised(root), before)
                self.assertEqual(before["refs/heads/main"], publication_base)
                self.assertNotEqual(before["refs/heads/main"], head)

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
            root, candidate, publication_base, rejected_transition, _ = initialized_repository(temporary)
            original_candidate = json.loads(candidate.read_text(encoding="utf-8"))
            rejected_validation_head = original_candidate["candidate_validation_head"]
            forged_candidate = dict(original_candidate)
            forged_candidate["candidate_validation_head"] = "f" * 40
            candidate.write_text(json.dumps(forged_candidate), encoding="utf-8")
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), self.assertRaisesRegex(PublicationError, "publication-readiness-failed") as raised:
                publication_readiness(root, "v0.4.0", candidate)
            self.assertIn("restore settled lifecycle", error_payload(raised.exception)["corrective_action"])

            git(root, "tag", "-d", "v0.4.0")
            git(root, "checkout", "-qf", "-B", "replacement", publication_base)

            def apply_range(start: str, end: str, message: str) -> str:
                patch = subprocess.run(
                    ["git", "diff", "--binary", start, end],
                    cwd=root,
                    check=True,
                    capture_output=True,
                ).stdout
                subprocess.run(
                    ["git", "apply", "--index"],
                    cwd=root,
                    input=patch,
                    check=True,
                    capture_output=True,
                )
                git(root, "commit", "-qm", message)
                return git(root, "rev-parse", "HEAD")

            replacement_transition = apply_range(
                publication_base, rejected_transition, "replacement activate"
            )
            replacement_validation_head = apply_range(
                rejected_transition,
                rejected_validation_head,
                "replacement lifecycle evidence",
            )
            replacement_result, replacement_issues = (
                FIXTURE_SUPPORT.validate_activation_candidate(root, "v0.4.0")
            )
            self.assertEqual(replacement_issues, ())
            self.assertIsNotNone(replacement_result)
            assert replacement_result is not None
            candidate.write_text(
                json.dumps(replacement_result.as_dict()), encoding="utf-8"
            )
            git(root, "add", candidate.relative_to(root).as_posix())
            git(root, "commit", "-qm", "record replacement candidate evidence")
            replacement_head = git(root, "rev-parse", "HEAD")
            git(root, "tag", "v0.4.0", replacement_transition)
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ):
                replacement = publication_readiness(
                    root, "v0.4.0", candidate
                )
            self.assertEqual(replacement.publication_base, publication_base)
            self.assertEqual(replacement.transition_commit, replacement_transition)
            self.assertEqual(replacement.candidate_validation_head, replacement_validation_head)
            self.assertEqual(replacement.publication_head, replacement_head)
            self.assertNotEqual(replacement_transition, rejected_transition)
            first_parent = git(root, "rev-list", "--first-parent", replacement_head).splitlines()
            self.assertNotIn(rejected_transition, first_parent)
            transitions = git(
                root,
                "rev-list",
                "--first-parent",
                f"{publication_base}..{replacement_head}",
                "--",
                "specs/boundary-first-activation.yaml",
            ).splitlines()
            self.assertEqual(transitions, [replacement_transition])
            self.assertEqual(
                advertised(root), {"refs/heads/main": publication_base}
            )

    def test_untrusted_diagnostics_are_suppressed_and_safe_context_is_preserved(self) -> None:
        release_sentinel = "PRIVATE_TOKEN_9471"
        with self.assertRaises(PublicationError) as invalid_release:
            publication_readiness(
                ROOT, release_sentinel, CANONICAL_CANDIDATE, mode="check"
            )
        self.assertNotIn(release_sentinel, json.dumps(error_payload(invalid_release.exception)))
        specification = importlib.util.spec_from_file_location("privacy_cli", CLI)
        assert specification is not None and specification.loader is not None
        privacy_cli = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(privacy_cli)
        cli_output = io.StringIO()
        with mock.patch.object(
            sys,
            "argv",
            [
                str(CLI),
                "--check",
                "--release",
                release_sentinel,
                "--candidate-evidence",
                "/tmp/private-machine-path/candidate.json",
            ],
        ), redirect_stdout(cli_output):
            self.assertEqual(privacy_cli.main(), 2)
        self.assertNotIn(release_sentinel, cli_output.getvalue())
        self.assertNotIn("/tmp/private-machine-path", cli_output.getvalue())

        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, publication_base, transition, head = initialized_repository(temporary)
            forged_identity = "a" * 40
            data = json.loads(candidate.read_text(encoding="utf-8"))
            diagnostic_context = fixture_readiness(
                candidate, publication_base, transition, head
            ).error_context("publish")
            for field in (
                "publication_base",
                "grandfathering_baseline",
                "transition_commit",
                "candidate_validation_head",
                "current_reviewed_head",
            ):
                private_identity = diagnostic_context[field]
                with self.subTest(private_identity_field=field), mock.patch.dict(
                    os.environ, {"PRIVATE_API_KEY": private_identity}
                ):
                    private_payload = error_payload(
                        PublicationError(
                            "atomic-publication-failed", **diagnostic_context
                        )
                    )
                    self.assertNotIn(private_identity, json.dumps(private_payload))
            data["publication_base"] = forged_identity
            candidate.write_text(json.dumps(data), encoding="utf-8")
            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), self.assertRaises(PublicationError) as forged:
                publication_readiness(root, "v0.4.0", candidate, mode="publish")
            forged_payload = error_payload(forged.exception)
            self.assertNotIn(forged_identity, json.dumps(forged_payload))
            self.assertEqual(forged_payload["release"], "v0.4.0")

            candidate_data = json.loads(git(root, "show", f"HEAD:{CANONICAL_CANDIDATE.as_posix()}"))
            candidate.write_text(json.dumps(candidate_data), encoding="utf-8")
            real_identity = __import__("boundary_activation_release")._identity

            def fail_tag(fixture_root: Path, revision: str) -> str:
                if revision.startswith("refs/tags/"):
                    raise PublicationError("identity-unavailable")
                return real_identity(fixture_root, revision)

            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), mock.patch("boundary_activation_release._identity", side_effect=fail_tag), self.assertRaises(
                PublicationError
            ) as tag_failure:
                publication_readiness(root, "v0.4.0", candidate, mode="publish")
            tag_payload = error_payload(tag_failure.exception)
            for expected in (publication_base, transition, head):
                self.assertIn(expected, tag_payload.values())

    def test_post_push_confirmation_failure_requires_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, candidate, _, transition, head = initialized_repository(temporary)
            real_advertised = __import__("boundary_activation_release")._advertised_refs
            calls = 0

            def fail_confirmation(fixture_root: Path, release: str) -> dict[str, str]:
                nonlocal calls
                calls += 1
                if calls == 1:
                    return real_advertised(fixture_root, release)
                raise PublicationError("remote-advertisement-unavailable")

            with mock.patch(
                "boundary_first_validation._publication_authority_issues",
                return_value=(),
            ), mock.patch(
                "boundary_activation_release._advertised_refs",
                side_effect=fail_confirmation,
            ), self.assertRaisesRegex(
                PublicationError, "publication-confirmation-unavailable"
            ) as raised:
                publish_activation(root, "v0.4.0", candidate)
            payload = error_payload(raised.exception)
            self.assertEqual(payload["failed_phase"], "publication-confirmation")
            self.assertIn("do not rerun", payload["corrective_action"])
            self.assertEqual(payload["current_reviewed_head"], head)
            self.assertEqual(payload["transition_commit"], transition)
            self.assertEqual(
                advertised(root),
                {"refs/heads/main": head, "refs/tags/v0.4.0": transition},
            )

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
