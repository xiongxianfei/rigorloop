#!/usr/bin/env python3
"""Guarded publication for the one approved boundary-first activation release."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import tempfile

from boundary_first_validation import validate_activation_publication_readiness


ACTIVATION_RELEASE = "v0.4.0"
CANONICAL_CANDIDATE = Path(
    "docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/"
    "evidence/boundary-activation-candidate.json"
)


class PublicationError(RuntimeError):
    """A bounded activation-publication failure."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class PublicationReadiness:
    release: str
    publication_base: str
    transition_commit: str
    publication_head: str

    def as_dict(self) -> dict[str, str]:
        return {
            "release": self.release,
            "publication_base": self.publication_base,
            "transition_commit": self.transition_commit,
            "publication_head": self.publication_head,
        }


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
    )


def _identity(root: Path, revision: str) -> str:
    try:
        value = _git(root, "rev-parse", "--verify", revision).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise PublicationError("identity-unavailable") from error
    if len(value) != 40 or any(character not in "0123456789abcdef" for character in value):
        raise PublicationError("identity-invalid")
    return value


def _advertised_refs(root: Path, release: str) -> dict[str, str]:
    try:
        lines = _git(
            root,
            "ls-remote",
            "--refs",
            "origin",
            "refs/heads/main",
            f"refs/tags/{release}",
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError) as error:
        raise PublicationError("remote-advertisement-unavailable") from error
    return {
        reference: identity
        for line in lines
        if "\t" in line
        for identity, reference in (line.split("\t", 1),)
    }


def publication_readiness(
    root: Path,
    release: str,
    candidate_evidence: Path,
) -> PublicationReadiness:
    """Return the exact live publication identities without mutating refs."""

    if release != ACTIVATION_RELEASE:
        raise PublicationError("release-not-approved")
    canonical = (root / CANONICAL_CANDIDATE).resolve(strict=False)
    supplied = (
        candidate_evidence
        if candidate_evidence.is_absolute()
        else root / candidate_evidence
    ).resolve(strict=False)
    if supplied != canonical or supplied.is_symlink():
        raise PublicationError("candidate-evidence-path-invalid")
    issues = validate_activation_publication_readiness(root)
    if issues:
        raise PublicationError("publication-readiness-failed")
    try:
        candidate = json.loads(supplied.read_text(encoding="utf-8"))
        publication_base = candidate["publication_base"]
        transition_commit = candidate["transition_commit"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise PublicationError("candidate-evidence-invalid") from error
    if not all(
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
        for value in (publication_base, transition_commit)
    ):
        raise PublicationError("candidate-identity-invalid")
    publication_head = _identity(root, "HEAD")
    if _identity(root, f"refs/tags/{release}^{{commit}}") != transition_commit:
        raise PublicationError("local-tag-mismatch")
    advertised = _advertised_refs(root, release)
    if advertised.get("refs/heads/main") != publication_base:
        raise PublicationError("remote-main-drift")
    if f"refs/tags/{release}" in advertised:
        raise PublicationError("remote-tag-exists")
    if _git(
        root,
        "merge-base",
        "--is-ancestor",
        publication_base,
        publication_head,
        check=False,
    ).returncode != 0:
        raise PublicationError("publication-not-fast-forward")
    return PublicationReadiness(
        release=release,
        publication_base=publication_base,
        transition_commit=transition_commit,
        publication_head=publication_head,
    )


def _guard_script() -> str:
    return """#!/usr/bin/env python3
import os
import subprocess
import sys

remote = sys.argv[2]
release = os.environ["RIGORLOOP_ACTIVATION_RELEASE"]
expected_main = os.environ["RIGORLOOP_EXPECTED_REMOTE_MAIN"]
result = subprocess.run(
    ["git", "ls-remote", "--refs", remote, "refs/heads/main", f"refs/tags/{release}"],
    check=False, capture_output=True, text=True,
)
refs = {
    ref: identity
    for line in result.stdout.splitlines()
    if "\\t" in line
    for identity, ref in (line.split("\\t", 1),)
}
if (
    result.returncode != 0
    or refs.get("refs/heads/main") != expected_main
    or f"refs/tags/{release}" in refs
):
    raise SystemExit(1)
"""


def _atomic_push(
    root: Path,
    readiness: PublicationReadiness,
    *,
    dry_run: bool,
) -> None:
    with tempfile.TemporaryDirectory(prefix="rigorloop-activation-hooks-") as temporary:
        hook = Path(temporary) / "pre-push"
        hook.write_text(_guard_script(), encoding="utf-8")
        hook.chmod(0o700)
        environment = {
            **os.environ,
            "RIGORLOOP_ACTIVATION_RELEASE": readiness.release,
            "RIGORLOOP_EXPECTED_REMOTE_MAIN": readiness.publication_base,
        }
        command = [
            "git",
            "-c",
            f"core.hooksPath={temporary}",
            "push",
            "--atomic",
        ]
        if dry_run:
            command.append("--dry-run")
        command.extend(
            [
                "origin",
                f"{readiness.publication_head}:refs/heads/main",
                f"{readiness.transition_commit}:refs/tags/{readiness.release}",
            ]
        )
        try:
            subprocess.run(
                command,
                cwd=root,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError) as error:
            raise PublicationError(
                "atomic-capability-unavailable" if dry_run else "atomic-publication-failed"
            ) from error


def check_publication(
    root: Path,
    release: str,
    candidate_evidence: Path,
) -> PublicationReadiness:
    readiness = publication_readiness(root, release, candidate_evidence)
    _atomic_push(root, readiness, dry_run=True)
    return readiness


def publish_activation(
    root: Path,
    release: str,
    candidate_evidence: Path,
) -> PublicationReadiness:
    """Recompute readiness and perform one non-forced atomic two-ref push."""

    readiness = publication_readiness(root, release, candidate_evidence)
    if _identity(root, "HEAD") != readiness.publication_head:
        raise PublicationError("local-head-drift")
    _atomic_push(root, readiness, dry_run=False)
    advertised = _advertised_refs(root, release)
    if (
        advertised.get("refs/heads/main") != readiness.publication_head
        or advertised.get(f"refs/tags/{release}") != readiness.transition_commit
    ):
        raise PublicationError("published-refs-unconfirmed")
    return readiness


def error_payload(error: PublicationError) -> dict[str, str]:
    return {"status": "blocked", "code": error.code}
