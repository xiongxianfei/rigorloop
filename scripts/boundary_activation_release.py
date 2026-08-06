#!/usr/bin/env python3
"""Guarded publication for the one approved boundary-first activation release."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from boundary_first_validation import (
    _private_runtime_values,
    validate_activation_publication_readiness,
)


ACTIVATION_RELEASE = "v0.4.0"
CANONICAL_CANDIDATE = Path(
    "docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/"
    "evidence/boundary-activation-candidate.json"
)


_ERROR_DETAILS = {
    "release-not-approved": ("publication-readiness", "release is exact v0.4.0", "use exact release v0.4.0"),
    "candidate-evidence-path-invalid": ("publication-readiness", "candidate evidence uses the canonical non-symlink path", "use the canonical candidate evidence file"),
    "publication-readiness-failed": ("publication-readiness", "stored provenance and current release authority are settled", "restore settled lifecycle and release authority, then rerun"),
    "candidate-evidence-invalid": ("publication-readiness", "candidate evidence is valid JSON with required identities", "regenerate canonical candidate evidence"),
    "candidate-identity-invalid": ("publication-readiness", "candidate identities are full commit SHAs", "regenerate canonical candidate evidence"),
    "identity-unavailable": ("publication-readiness", "required local identity is available", "restore the reviewed local history and rerun"),
    "identity-invalid": ("publication-readiness", "required local identity is a full commit SHA", "restore the reviewed local history and rerun"),
    "local-tag-mismatch": ("publication-readiness", "local v0.4.0 peels to transition T", "recreate the unpublished local tag at T and rerun"),
    "remote-advertisement-unavailable": ("publication-readiness", "origin advertises authoritative refs", "restore origin connectivity and rerun"),
    "remote-main-drift": ("atomic-publication", "advertised remote main equals publication base P", "regenerate from current remote main and rerun validation and review"),
    "remote-tag-exists": ("atomic-publication", "remote v0.4.0 is absent", "stop and reconcile the existing public tag"),
    "publication-not-fast-forward": ("publication-readiness", "publication head H fast-forwards publication base P", "replace the candidate from current authorized remote main"),
    "local-head-drift": ("atomic-publication", "live HEAD remains readiness-bound H", "rerun publication readiness at the reviewed head"),
    "push-mapping-invalid": ("atomic-publication", "one push maps exact H to main and T to v0.4.0", "restore the approved two-ref mapping and rerun"),
    "atomic-capability-unavailable": ("atomic-publication", "origin supports one atomic two-ref update", "restore atomic push capability; do not fall back to sequential pushes"),
    "atomic-publication-failed": ("atomic-publication", "both authorized refs update atomically", "reconcile remote state and regenerate or rerun without force"),
    "publication-confirmation-unavailable": ("publication-confirmation", "published remote main equals H and v0.4.0 equals T", "stop public closeout and reconcile both exact remote refs; do not rerun publication"),
    "published-refs-unconfirmed": ("publication-confirmation", "remote main equals H and v0.4.0 equals T", "stop public closeout and reconcile the remote refs"),
}

_IDENTITY_CONTEXT_FIELDS = {
    "publication_base",
    "grandfathering_baseline",
    "transition_commit",
    "candidate_validation_head",
    "current_reviewed_head",
    "conflicting_remote_main",
    "conflicting_remote_tag",
}


def _safe_context(context: dict[str, str]) -> dict[str, str]:
    safe: dict[str, str] = {}
    private_values = _private_runtime_values()
    for key, value in context.items():
        if not isinstance(value, str) or not value:
            continue
        if any(private in value for private in private_values):
            continue
        if key == "mode" and value in {"readiness", "check", "publish"}:
            safe[key] = value
        elif key == "release" and value == ACTIVATION_RELEASE:
            safe[key] = value
        elif key in _IDENTITY_CONTEXT_FIELDS and (
            re.fullmatch(r"[0-9a-f]{40}", value)
            or (key.startswith("conflicting_remote_") and value == "absent")
        ):
            safe[key] = value
    return safe


class PublicationError(RuntimeError):
    """A bounded activation-publication failure."""

    def __init__(self, code: str, **context: str) -> None:
        super().__init__(code)
        self.code = code
        self.context = _safe_context(context)

    def add_context(self, **context: str) -> "PublicationError":
        for key, value in _safe_context(context).items():
            if key not in self.context:
                self.context[key] = value
        return self


@dataclass(frozen=True)
class PublicationReadiness:
    release: str
    publication_base: str
    grandfathering_baseline: str
    transition_commit: str
    candidate_validation_head: str
    publication_head: str

    def as_dict(self) -> dict[str, str]:
        return {
            "release": self.release,
            "publication_base": self.publication_base,
            "grandfathering_baseline": self.grandfathering_baseline,
            "transition_commit": self.transition_commit,
            "candidate_validation_head": self.candidate_validation_head,
            "publication_head": self.publication_head,
        }

    def error_context(self, mode: str) -> dict[str, str]:
        return {
            "mode": mode,
            "release": self.release,
            "publication_base": self.publication_base,
            "grandfathering_baseline": self.grandfathering_baseline,
            "transition_commit": self.transition_commit,
            "candidate_validation_head": self.candidate_validation_head,
            "current_reviewed_head": self.publication_head,
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
    *,
    mode: str = "readiness",
) -> PublicationReadiness:
    """Return the exact live publication identities without mutating refs."""

    if release != ACTIVATION_RELEASE:
        raise PublicationError("release-not-approved", mode=mode)
    root_absolute = Path(os.path.abspath(root))
    canonical = Path(os.path.abspath(root_absolute / CANONICAL_CANDIDATE))
    supplied_lexical = (
        candidate_evidence
        if candidate_evidence.is_absolute()
        else root_absolute / candidate_evidence
    )
    supplied = Path(os.path.abspath(supplied_lexical))
    try:
        canonical_parts = canonical.relative_to(root_absolute).parts
    except ValueError as error:
        raise PublicationError(
            "candidate-evidence-path-invalid", mode=mode, release=release
        ) from error
    path_cursor = root_absolute
    path_has_symlink = root_absolute.is_symlink()
    for part in canonical_parts:
        path_cursor /= part
        path_has_symlink = path_has_symlink or path_cursor.is_symlink()
    exact_lexical_path = (
        candidate_evidence == canonical
        if candidate_evidence.is_absolute()
        else candidate_evidence == CANONICAL_CANDIDATE
    )
    if (
        not exact_lexical_path
        or supplied != canonical
        or supplied_lexical.is_symlink()
        or path_has_symlink
    ):
        raise PublicationError(
            "candidate-evidence-path-invalid", mode=mode, release=release
        )
    try:
        candidate = json.loads(supplied.read_text(encoding="utf-8"))
        publication_base = candidate["publication_base"]
        grandfathering_baseline = candidate["grandfathering_baseline"]
        transition_commit = candidate["transition_commit"]
        candidate_validation_head = candidate["candidate_validation_head"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise PublicationError(
            "candidate-evidence-invalid", mode=mode, release=release
        ) from error
    if not all(
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
        for value in (
            publication_base,
            grandfathering_baseline,
            transition_commit,
            candidate_validation_head,
        )
    ):
        raise PublicationError(
            "candidate-identity-invalid", mode=mode, release=release
        )
    issues = validate_activation_publication_readiness(root)
    if issues:
        raise PublicationError(
            "publication-readiness-failed", mode=mode, release=release
        )
    candidate_context = {
        "mode": mode,
        "release": release,
        "publication_base": publication_base,
        "grandfathering_baseline": grandfathering_baseline,
        "transition_commit": transition_commit,
        "candidate_validation_head": candidate_validation_head,
    }
    try:
        publication_head = _identity(root, "HEAD")
    except PublicationError as error:
        raise error.add_context(**candidate_context)
    live_context = {**candidate_context, "current_reviewed_head": publication_head}
    try:
        local_tag_commit = _identity(root, f"refs/tags/{release}^{{commit}}")
    except PublicationError as error:
        raise error.add_context(**live_context)
    if local_tag_commit != transition_commit:
        raise PublicationError("local-tag-mismatch", **live_context)
    try:
        advertised = _advertised_refs(root, release)
    except PublicationError as error:
        raise error.add_context(**live_context)
    if advertised.get("refs/heads/main") != publication_base:
        raise PublicationError(
            "remote-main-drift",
            **live_context,
            conflicting_remote_main=advertised.get("refs/heads/main", "absent"),
        )
    if f"refs/tags/{release}" in advertised:
        raise PublicationError(
            "remote-tag-exists",
            **live_context,
            conflicting_remote_tag=advertised[f"refs/tags/{release}"],
        )
    if _git(
        root,
        "merge-base",
        "--is-ancestor",
        publication_base,
        publication_head,
        check=False,
    ).returncode != 0:
        raise PublicationError("publication-not-fast-forward", **live_context)
    return PublicationReadiness(
        release=release,
        publication_base=publication_base,
        grandfathering_baseline=grandfathering_baseline,
        transition_commit=transition_commit,
        candidate_validation_head=candidate_validation_head,
        publication_head=publication_head,
    )


def _guard_script() -> str:
    return """#!/usr/bin/env python3
import os
import re
import subprocess
import sys

remote = sys.argv[2]
release = os.environ["RIGORLOOP_ACTIVATION_RELEASE"]
expected_main = os.environ["RIGORLOOP_EXPECTED_REMOTE_MAIN"]
expected_head = os.environ["RIGORLOOP_EXPECTED_PUBLICATION_HEAD"]
expected_transition = os.environ["RIGORLOOP_EXPECTED_TRANSITION"]
main_ref = "refs/heads/main"
tag_ref = f"refs/tags/{release}"

def stop(code, identity=""):
    suffix = f":{identity}" if re.fullmatch(r"[0-9a-f]{40}", identity) else ""
    print(f"RIGORLOOP_GUARD:{code}{suffix}", file=sys.stderr)
    raise SystemExit(1)

updates = {}
for raw in sys.stdin:
    fields = raw.split()
    if len(fields) != 4:
        stop("push-mapping-invalid")
    _local_ref, local_identity, remote_ref, remote_identity = fields
    if remote_ref in updates:
        stop("push-mapping-invalid")
    updates[remote_ref] = (local_identity, remote_identity)
if set(updates) != {main_ref, tag_ref}:
    stop("push-mapping-invalid")
if updates[main_ref][0] != expected_head or updates[tag_ref][0] != expected_transition:
    stop("push-mapping-invalid")
if updates[main_ref][1] != expected_main:
    stop("remote-main-drift", updates[main_ref][1])
if updates[tag_ref][1] != "0" * 40:
    stop("remote-tag-exists", updates[tag_ref][1])

result = subprocess.run(
    ["git", "ls-remote", "--refs", remote, main_ref, tag_ref],
    check=False, capture_output=True, text=True,
)
refs = {
    ref: identity
    for line in result.stdout.splitlines()
    if "\\t" in line
    for identity, ref in (line.split("\\t", 1),)
}
if result.returncode != 0:
    stop("remote-advertisement-unavailable")
if refs.get(main_ref) != expected_main:
    stop("remote-main-drift", refs.get(main_ref, ""))
if tag_ref in refs:
    stop("remote-tag-exists", refs[tag_ref])
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
            "RIGORLOOP_EXPECTED_PUBLICATION_HEAD": readiness.publication_head,
            "RIGORLOOP_EXPECTED_TRANSITION": readiness.transition_commit,
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
            diagnostic = getattr(error, "stderr", "") or ""
            marker = next(
                (
                    matched
                    for line in diagnostic.splitlines()
                    if (
                        matched := re.fullmatch(
                            r"RIGORLOOP_GUARD:(remote-main-drift|remote-tag-exists|remote-advertisement-unavailable|push-mapping-invalid)(?::([0-9a-f]{40}))?",
                            line,
                        )
                    )
                ),
                None,
            )
            if marker:
                code = marker.group(1)
                conflict_key = {
                    "remote-main-drift": "conflicting_remote_main",
                    "remote-tag-exists": "conflicting_remote_tag",
                }.get(code)
                conflict = {conflict_key: marker.group(2)} if conflict_key and marker.group(2) else {}
                raise PublicationError(
                    code,
                    **readiness.error_context("check" if dry_run else "publish"),
                    **conflict,
                ) from error
            raise PublicationError(
                "atomic-capability-unavailable" if dry_run else "atomic-publication-failed",
                **readiness.error_context("check" if dry_run else "publish"),
            ) from error


def check_publication(
    root: Path,
    release: str,
    candidate_evidence: Path,
) -> PublicationReadiness:
    readiness = publication_readiness(root, release, candidate_evidence, mode="check")
    _atomic_push(root, readiness, dry_run=True)
    return readiness


def publish_activation(
    root: Path,
    release: str,
    candidate_evidence: Path,
) -> PublicationReadiness:
    """Recompute readiness and perform one non-forced atomic two-ref push."""

    readiness = publication_readiness(root, release, candidate_evidence, mode="publish")
    try:
        live_head = _identity(root, "HEAD")
    except PublicationError as error:
        raise error.add_context(**readiness.error_context("publish"))
    if live_head != readiness.publication_head:
        raise PublicationError("local-head-drift", **readiness.error_context("publish"))
    _atomic_push(root, readiness, dry_run=False)
    try:
        advertised = _advertised_refs(root, release)
    except PublicationError as error:
        raise PublicationError(
            "publication-confirmation-unavailable",
            **readiness.error_context("publish"),
        ) from error
    if (
        advertised.get("refs/heads/main") != readiness.publication_head
        or advertised.get(f"refs/tags/{release}") != readiness.transition_commit
    ):
        raise PublicationError(
            "published-refs-unconfirmed", **readiness.error_context("publish")
        )
    return readiness


def error_payload(error: PublicationError) -> dict[str, str]:
    phase, invariant, action = _ERROR_DETAILS.get(
        error.code,
        ("atomic-publication", "publication remains fail-closed", "inspect bounded evidence and rerun safely"),
    )
    return {
        "status": "blocked",
        "code": error.code,
        "failed_phase": phase,
        **error.context,
        "expected_invariant": invariant,
        "corrective_action": action,
    }
