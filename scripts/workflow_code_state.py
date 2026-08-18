#!/usr/bin/env python3
"""Independent canonical final-code state providers."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Protocol

from artifact_lifecycle_validation import _parse_change_yaml_text


class CodeStateError(ValueError):
    """Raised when canonical code state cannot be established safely."""


@dataclass(frozen=True)
class CodeStateEntry:
    status: str
    path: str
    identity: str | None
    source_path: str | None = None

    def record(self) -> dict[str, str | None]:
        return {
            "status": self.status,
            "path": self.path,
            "source_path": self.source_path,
            "identity": self.identity,
        }


@dataclass(frozen=True)
class CanonicalCodeState:
    anchor_identity: str
    base_revision: str
    reviewed_revision: str
    entries: tuple[CodeStateEntry, ...]
    final_review_recording_revision: str | None = None
    explanation_recording_revision: str | None = None
    handoff_revision: str | None = None
    tail_state: str = "reviewed-subject"

    @property
    def paths(self) -> tuple[str, ...]:
        paths: set[str] = set()
        for entry in self.entries:
            paths.add(entry.path)
            if entry.source_path is not None:
                paths.add(entry.source_path)
        return tuple(sorted(paths))

    @property
    def identity(self) -> str:
        payload = {
            "anchor_identity": self.anchor_identity,
            "base_revision": self.base_revision,
            "reviewed_revision": self.reviewed_revision,
            "entries": [
                entry.record()
                for entry in sorted(
                    self.entries,
                    key=lambda item: (
                        item.path,
                        item.source_path or "",
                        item.status,
                    ),
                )
            ],
        }
        encoded = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return "sha256:" + hashlib.sha256(encoded).hexdigest()


class CodeStateProvider(Protocol):
    test_only: bool

    def snapshot(self, repository_root: Path) -> CanonicalCodeState:
        """Return the independently derived complete final-code state."""


@dataclass(frozen=True)
class CodeStateAnchor:
    change_id: str
    target_ref: str
    target_revision: str
    base_revision: str
    reviewed_revision: str
    final_review_id: str
    lifecycle_evidence_paths: tuple[str, ...]
    post_handoff_evidence_paths: tuple[str, ...] = ()

    @property
    def identity(self) -> str:
        payload = {
            "change_id": self.change_id,
            "target_ref": self.target_ref,
            "target_revision": self.target_revision,
            "base_revision": self.base_revision,
            "reviewed_revision": self.reviewed_revision,
            "final_review_id": self.final_review_id,
            "lifecycle_evidence_paths": self.lifecycle_evidence_paths,
        }
        encoded = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return "sha256:" + hashlib.sha256(encoded).hexdigest()


class GitCodeStateProvider:
    """Derive final-code state from trusted Git revisions and live worktree."""

    test_only = False

    _POST_REVIEW_EVIDENCE_PREFIXES = (
        "docs/changes/",
        "docs/plans/",
    )
    _POST_REVIEW_EVIDENCE_PATHS = frozenset({"docs/plan.md"})
    _REVIEW_CHANGE_FIELD_PREFIXES = (
        ("workflow_state", "lifecycle_state"),
        ("workflow_state", "current_stage"),
        ("workflow_state", "next_stage"),
        ("workflow_state", "blocker"),
        ("workflow_state", "evidence"),
        ("workflow_state", "planned_work", "current_milestone"),
        ("workflow_state", "planned_work", "milestones"),
        ("workflow_state", "planned_work", "remaining_implementation_milestones"),
        ("workflow_state", "planned_work", "latest_review"),
        ("workflow_state", "planned_work", "final_closeout"),
        ("workflow", "automation", "status"),
        ("workflow", "automation", "current_stage"),
        ("workflow", "automation", "stop_reason"),
        ("workflow", "automation", "evidence"),
        ("review",),
        ("changed_files",),
    )
    _EXPLANATION_CHANGE_FIELD_PREFIXES = (
        ("workflow_state", "lifecycle_state"),
        ("workflow_state", "current_stage"),
        ("workflow_state", "next_stage"),
        ("workflow_state", "blocker"),
        ("workflow_state", "evidence"),
        ("workflow_state", "planned_work", "final_closeout"),
        ("workflow", "automation", "status"),
        ("workflow", "automation", "current_stage"),
        ("workflow", "automation", "stop_reason"),
        ("workflow", "automation", "evidence"),
        ("artifacts", "explain_change"),
        ("changed_files",),
    )

    def __init__(
        self,
        *,
        anchor: CodeStateAnchor,
    ) -> None:
        if not isinstance(anchor, CodeStateAnchor):
            raise CodeStateError("resolved code-state anchor is required")
        self._anchor = anchor
        self._allowed_post_review_paths = frozenset(
            anchor.lifecycle_evidence_paths
        )
        self._allowed_post_handoff_paths = frozenset(
            anchor.post_handoff_evidence_paths
        )

    @staticmethod
    def _validate_relative_path(value: str) -> str:
        path = PurePosixPath(value)
        if (
            not value
            or path.is_absolute()
            or ".." in path.parts
            or value != path.as_posix()
        ):
            raise CodeStateError(f"invalid repository path: {value!r}")
        return value

    @staticmethod
    def _git(root: Path, *args: str) -> bytes:
        try:
            result = subprocess.run(
                ("git", "-C", str(root), *args),
                check=True,
                capture_output=True,
            )
        except (OSError, subprocess.CalledProcessError) as error:
            raise CodeStateError(
                f"cannot derive canonical Git code state: {' '.join(args)}"
            ) from error
        return result.stdout

    def _commit(self, root: Path, revision: str) -> str:
        return self._git(
            root, "rev-parse", "--verify", f"{revision}^{{commit}}"
        ).decode("ascii").strip()

    def _changed_paths(
        self, root: Path, older: str, newer: str
    ) -> frozenset[str]:
        output = self._git(
            root, "diff", "--name-only", "-z", older, newer
        )
        return frozenset(
            self._validate_relative_path(item.decode("utf-8"))
            for item in output.split(b"\0")
            if item
        )

    def _worktree_paths(self, root: Path) -> frozenset[str]:
        output = self._git(
            root, "status", "--porcelain=v1", "-z", "--untracked-files=all"
        )
        fields = output.split(b"\0")
        paths: set[str] = set()
        index = 0
        while index < len(fields):
            field = fields[index]
            index += 1
            if not field:
                continue
            text = field.decode("utf-8")
            if len(text) < 4:
                raise CodeStateError("cannot parse Git worktree state")
            status = text[:2]
            paths.add(self._validate_relative_path(text[3:]))
            if "R" in status or "C" in status:
                if index >= len(fields) or not fields[index]:
                    raise CodeStateError("cannot parse Git rename state")
                paths.add(
                    self._validate_relative_path(
                        fields[index].decode("utf-8")
                    )
                )
                index += 1
        return frozenset(paths)

    def _blob_identity(
        self, root: Path, revision: str, path: str
    ) -> str:
        blob = self._git(root, "show", f"{revision}:{path}")
        return "sha256:" + hashlib.sha256(blob).hexdigest()

    def _blob_text(self, root: Path, revision: str, path: str) -> str:
        try:
            return self._git(root, "show", f"{revision}:{path}").decode("utf-8")
        except UnicodeError as error:
            raise CodeStateError(
                f"cannot decode lifecycle evidence path: {path}"
            ) from error

    @staticmethod
    def _changed_fields(
        older: object,
        newer: object,
        prefix: tuple[str, ...] = (),
    ) -> frozenset[tuple[str, ...]]:
        if isinstance(older, dict) and isinstance(newer, dict):
            changed: set[tuple[str, ...]] = set()
            for key in set(older) | set(newer):
                key_text = str(key)
                if key not in older or key not in newer:
                    changed.add((*prefix, key_text))
                    continue
                changed.update(
                    GitCodeStateProvider._changed_fields(
                        older[key], newer[key], (*prefix, key_text)
                    )
                )
            return frozenset(changed)
        if older != newer:
            return frozenset({prefix})
        return frozenset()

    def _validate_change_metadata_fields(
        self,
        root: Path,
        older: str,
        newer: str,
        *,
        stage: str,
        change_path: str,
    ) -> None:
        try:
            before = _parse_change_yaml_text(
                self._blob_text(root, older, change_path)
            )
            after = _parse_change_yaml_text(
                self._blob_text(root, newer, change_path)
            )
        except Exception as error:
            raise CodeStateError(
                "cannot parse change metadata for stage-evidence validation"
            ) from error
        prefixes = (
            self._REVIEW_CHANGE_FIELD_PREFIXES
            if stage == "final-review"
            else self._EXPLANATION_CHANGE_FIELD_PREFIXES
        )
        changed = self._changed_fields(before, after)
        unowned = sorted(
            ".".join(path)
            for path in changed
            if not any(path[: len(prefix)] == prefix for prefix in prefixes)
        )
        if unowned:
            raise CodeStateError(
                f"unowned change metadata field in {stage} revision: {unowned}"
            )

    def _validate_stage_commit(
        self,
        root: Path,
        older: str,
        newer: str,
        *,
        stage: str,
    ) -> None:
        change_root = f"docs/changes/{self._anchor.change_id}"
        change_path = f"{change_root}/change.yaml"
        paths = self._changed_paths(root, older, newer)
        if stage == "final-review":
            required = frozenset(
                {
                    f"{change_root}/reviews/{self._anchor.final_review_id}.md",
                    f"{change_root}/review-invocation-{self._anchor.final_review_id}.yaml",
                    f"{change_root}/review-log.md",
                    change_path,
                }
            )
            allowed = required | frozenset(
                {f"{change_root}/review-resolution.md"}
            )
            label = "final-review recording paths"
        else:
            required = self._allowed_post_review_paths | frozenset({change_path})
            allowed = required
            label = "explanation recording paths"
        if not required.issubset(paths) or not paths.issubset(allowed):
            raise CodeStateError(
                f"{label} are invalid: {sorted(paths)}"
            )
        self._validate_change_metadata_fields(
            root, older, newer, stage=stage, change_path=change_path
        )

    def _linear_tail(self, root: Path, reviewed: str, head: str) -> tuple[str, ...]:
        if head == reviewed:
            return ()
        output = self._git(
            root, "rev-list", "--reverse", f"{reviewed}..{head}"
        ).decode("ascii").splitlines()
        commits = tuple(item.strip() for item in output if item.strip())
        previous = reviewed
        for commit in commits:
            parent_line = self._git(
                root, "rev-list", "--parents", "-n", "1", commit
            ).decode("ascii").strip().split()
            if len(parent_line) != 2 or parent_line[1] != previous:
                raise CodeStateError(
                    "post-review evidence tail must be linear non-merge direct children"
                )
            previous = commit
        return commits

    def _entries(
        self, root: Path, base: str, reviewed: str
    ) -> tuple[CodeStateEntry, ...]:
        output = self._git(
            root,
            "diff",
            "--name-status",
            "-z",
            "--find-renames",
            base,
            reviewed,
        )
        fields = output.split(b"\0")
        entries: list[CodeStateEntry] = []
        index = 0
        while index < len(fields):
            raw_status = fields[index]
            index += 1
            if not raw_status:
                continue
            status_text = raw_status.decode("ascii")
            status = status_text[0]
            if status not in {"A", "M", "D", "R"}:
                raise CodeStateError(
                    f"unsupported Git change status: {status_text}"
                )
            if index >= len(fields) or not fields[index]:
                raise CodeStateError("cannot parse Git changed path")
            first = self._validate_relative_path(
                fields[index].decode("utf-8")
            )
            index += 1
            if status == "R":
                if index >= len(fields) or not fields[index]:
                    raise CodeStateError("cannot parse Git renamed path")
                path = self._validate_relative_path(
                    fields[index].decode("utf-8")
                )
                index += 1
                entries.append(
                    CodeStateEntry(
                        status="R",
                        path=path,
                        source_path=first,
                        identity=self._blob_identity(root, reviewed, path),
                    )
                )
            elif status == "D":
                entries.append(
                    CodeStateEntry(status="D", path=first, identity=None)
                )
            else:
                entries.append(
                    CodeStateEntry(
                        status=status,
                        path=first,
                        identity=self._blob_identity(root, reviewed, first),
                    )
                )
        if not entries:
            raise CodeStateError("canonical final-code state is empty")
        return tuple(entries)

    def snapshot(self, repository_root: Path) -> CanonicalCodeState:
        root = repository_root.resolve()
        top = Path(
            self._git(root, "rev-parse", "--show-toplevel")
            .decode("utf-8")
            .strip()
        ).resolve()
        if top != root:
            raise CodeStateError("repository root does not match Git root")

        base = self._commit(root, self._anchor.base_revision)
        reviewed = self._commit(root, self._anchor.reviewed_revision)
        target = self._commit(root, self._anchor.target_revision)
        current_target = self._commit(root, self._anchor.target_ref)
        if (
            base != self._anchor.base_revision
            or reviewed != self._anchor.reviewed_revision
            or target != self._anchor.target_revision
        ):
            raise CodeStateError("code-state anchor revision identity is stale")
        if current_target != target:
            raise CodeStateError(
                "code-state anchor target branch identity is stale"
            )
        observed_base = self._git(
            root, "merge-base", target, reviewed
        ).decode("ascii").strip()
        if observed_base != base:
            raise CodeStateError("code-state anchor base is stale")
        head = self._commit(root, "HEAD")
        try:
            subprocess.run(
                (
                    "git",
                    "-C",
                    str(root),
                    "merge-base",
                    "--is-ancestor",
                    reviewed,
                    head,
                ),
                check=True,
                capture_output=True,
            )
        except (OSError, subprocess.CalledProcessError) as error:
            raise CodeStateError(
                "reviewed revision is not an ancestor of HEAD"
            ) from error

        tail = self._linear_tail(root, reviewed, head)
        if len(tail) > 2 and not self._allowed_post_handoff_paths:
            raise CodeStateError(
                "post-review evidence tail contains additional pre-verify commits"
            )
        final_review_recording = tail[0] if tail else None
        explanation_recording = tail[1] if len(tail) >= 2 else None
        if final_review_recording is not None:
            self._validate_stage_commit(
                root,
                reviewed,
                final_review_recording,
                stage="final-review",
            )
        if explanation_recording is not None:
            self._validate_stage_commit(
                root,
                final_review_recording,
                explanation_recording,
                stage="explanation",
            )
        previous = explanation_recording
        for commit in tail[2:]:
            assert previous is not None
            paths = self._changed_paths(root, previous, commit)
            if not paths or not paths.issubset(self._allowed_post_handoff_paths):
                raise CodeStateError(
                    "post-handoff evidence revision contains unowned paths: "
                    f"{sorted(paths)}"
                )
            previous = commit

        unexpected_worktree = self._worktree_paths(root)
        if unexpected_worktree:
            raise CodeStateError(
                "canonical code state is stale because worktree differs "
                f"after review: {sorted(unexpected_worktree)}"
            )

        return CanonicalCodeState(
            anchor_identity=self._anchor.identity,
            base_revision=base,
            reviewed_revision=reviewed,
            entries=self._entries(root, base, reviewed),
            final_review_recording_revision=final_review_recording,
            explanation_recording_revision=explanation_recording,
            handoff_revision=explanation_recording,
            tail_state=(
                "complete"
                if explanation_recording is not None
                else "review-recorded"
                if final_review_recording is not None
                else "reviewed-subject"
            ),
        )


class GitCodeStateAnchorResolver:
    """Resolve immutable code-state anchors from repository-owned refs."""

    def _default_branch_ref(self, root: Path) -> str:
        symbolic = subprocess.run(
            (
                "git",
                "-C",
                str(root),
                "symbolic-ref",
                "--quiet",
                "refs/remotes/origin/HEAD",
            ),
            check=False,
            capture_output=True,
        )
        if symbolic.returncode == 0:
            value = symbolic.stdout.decode("utf-8").strip()
            if value:
                return value
        candidates: list[str] = []
        for candidate in ("refs/heads/main", "refs/heads/master"):
            result = subprocess.run(
                (
                    "git",
                    "-C",
                    str(root),
                    "rev-parse",
                    "--verify",
                    "--quiet",
                    f"{candidate}^{{commit}}",
                ),
                check=False,
                capture_output=True,
            )
            if result.returncode == 0:
                candidates.append(candidate)
        if len(candidates) != 1:
            raise CodeStateError(
                "canonical default branch ref is missing or ambiguous"
            )
        return candidates[0]

    def resolve(
        self,
        repository_root: Path,
        *,
        change_id: str,
        reviewed_revision: str,
        final_review_id: str,
        lifecycle_evidence_paths: frozenset[str],
        post_handoff_evidence_paths: frozenset[str] = frozenset(),
    ) -> CodeStateAnchor:
        root = repository_root.resolve()
        if not all(
            isinstance(value, str) and value
            for value in (
                change_id,
                reviewed_revision,
                final_review_id,
            )
        ):
            raise CodeStateError("code-state anchor basis is incomplete")
        target_ref = self._default_branch_ref(root)
        target = GitCodeStateProvider._git(
            root, "rev-parse", "--verify", f"{target_ref}^{{commit}}"
        ).decode("ascii").strip()
        reviewed = GitCodeStateProvider._git(
            root,
            "rev-parse",
            "--verify",
            f"{reviewed_revision}^{{commit}}",
        ).decode("ascii").strip()
        if reviewed_revision != reviewed:
            raise CodeStateError(
                "reviewed revision must be a canonical commit identity"
            )
        base = GitCodeStateProvider._git(
            root, "merge-base", target, reviewed
        ).decode("ascii").strip()
        allowed_paths: set[str] = set()
        for path in lifecycle_evidence_paths:
            relative_path = GitCodeStateProvider._validate_relative_path(path)
            if (
                relative_path
                not in GitCodeStateProvider._POST_REVIEW_EVIDENCE_PATHS
                and not relative_path.startswith(
                    GitCodeStateProvider._POST_REVIEW_EVIDENCE_PREFIXES
                )
            ):
                raise CodeStateError(
                    "post-review exemption is not a lifecycle evidence path: "
                    f"{relative_path}"
                )
            allowed_paths.add(relative_path)
        allowed_post_handoff_paths: set[str] = set()
        for path in post_handoff_evidence_paths:
            relative_path = GitCodeStateProvider._validate_relative_path(path)
            if (
                relative_path
                not in GitCodeStateProvider._POST_REVIEW_EVIDENCE_PATHS
                and not relative_path.startswith(
                    GitCodeStateProvider._POST_REVIEW_EVIDENCE_PREFIXES
                )
            ):
                raise CodeStateError(
                    "post-handoff exemption is not a lifecycle evidence path: "
                    f"{relative_path}"
                )
            allowed_post_handoff_paths.add(relative_path)
        return CodeStateAnchor(
            change_id=change_id,
            target_ref=target_ref,
            target_revision=target,
            base_revision=base,
            reviewed_revision=reviewed,
            final_review_id=final_review_id,
            lifecycle_evidence_paths=tuple(sorted(allowed_paths)),
            post_handoff_evidence_paths=tuple(
                sorted(allowed_post_handoff_paths)
            ),
        )


def resolve_canonical_code_state(
    *,
    repository_root: Path,
    change_id: str,
    reviewed_revision: str,
    final_review_id: str,
    lifecycle_evidence_paths: frozenset[str],
    post_handoff_evidence_paths: frozenset[str] = frozenset(),
    test_provider: CodeStateProvider | None = None,
) -> CanonicalCodeState:
    """Resolve Git state internally; allow injection only outside Git."""

    root = repository_root.resolve()
    try:
        git_probe = subprocess.run(
            ("git", "-C", str(root), "rev-parse", "--show-toplevel"),
            check=False,
            capture_output=True,
            env={**os.environ, "LC_ALL": "C", "LANG": "C"},
        )
    except OSError as error:
        raise CodeStateError(
            "cannot classify repository for canonical code state"
        ) from error
    if git_probe.returncode == 0:
        try:
            git_root_value = git_probe.stdout.decode("utf-8").strip()
            if not git_root_value:
                raise CodeStateError(
                    "canonical Git repository root is invalid"
                )
            git_root = Path(git_root_value).resolve()
        except (OSError, UnicodeError) as error:
            raise CodeStateError(
                "canonical Git repository root is invalid"
            ) from error
        if test_provider is not None:
            raise CodeStateError(
                "test-only code-state provider is prohibited for Git repositories"
            )
        if git_root != root:
            raise CodeStateError("repository root does not match Git root")
        anchor = GitCodeStateAnchorResolver().resolve(
            root,
            change_id=change_id,
            reviewed_revision=reviewed_revision,
            final_review_id=final_review_id,
            lifecycle_evidence_paths=lifecycle_evidence_paths,
            post_handoff_evidence_paths=post_handoff_evidence_paths,
        )
        return GitCodeStateProvider(anchor=anchor).snapshot(root)
    diagnostic = git_probe.stderr.decode("utf-8", errors="replace").lower()
    if "not a git repository" not in diagnostic:
        raise CodeStateError(
            "cannot classify repository for canonical code state"
        )
    if test_provider is None or not getattr(test_provider, "test_only", False):
        raise CodeStateError(
            "non-Git repository requires an explicit test-only code-state provider"
        )
    snapshot = test_provider.snapshot(root)
    if snapshot.reviewed_revision != reviewed_revision:
        raise CodeStateError(
            "test-only code-state provider reviewed revision is stale"
        )
    return snapshot
