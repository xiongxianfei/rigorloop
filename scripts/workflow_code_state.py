#!/usr/bin/env python3
"""Independent canonical final-code state providers."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Protocol


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
    base_revision: str
    reviewed_revision: str
    entries: tuple[CodeStateEntry, ...]

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
    def snapshot(self, repository_root: Path) -> CanonicalCodeState:
        """Return the independently derived complete final-code state."""


class GitCodeStateProvider:
    """Derive final-code state from trusted Git revisions and live worktree."""

    _POST_REVIEW_EVIDENCE_PREFIXES = (
        "docs/changes/",
        "docs/plans/",
    )
    _POST_REVIEW_EVIDENCE_PATHS = frozenset({"docs/plan.md"})

    def __init__(
        self,
        *,
        base_revision: str,
        reviewed_revision: str,
        allowed_post_review_evidence_paths: frozenset[str] = frozenset(),
    ) -> None:
        if not base_revision or not reviewed_revision:
            raise CodeStateError("base and reviewed revisions are required")
        self._base_revision = base_revision
        self._reviewed_revision = reviewed_revision
        allowed_paths: set[str] = set()
        for path in allowed_post_review_evidence_paths:
            relative_path = self._validate_relative_path(path)
            if (
                relative_path not in self._POST_REVIEW_EVIDENCE_PATHS
                and not relative_path.startswith(
                    self._POST_REVIEW_EVIDENCE_PREFIXES
                )
            ):
                raise CodeStateError(
                    "post-review exemption is not a lifecycle evidence path: "
                    f"{relative_path}"
                )
            allowed_paths.add(relative_path)
        self._allowed_post_review_paths = frozenset(allowed_paths)

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

        base = self._commit(root, self._base_revision)
        reviewed = self._commit(root, self._reviewed_revision)
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

        post_review = self._changed_paths(root, reviewed, head)
        unexpected_committed = post_review - self._allowed_post_review_paths
        if unexpected_committed:
            raise CodeStateError(
                "canonical code state is stale because HEAD differs after "
                f"review: {sorted(unexpected_committed)}"
            )
        unexpected_worktree = (
            self._worktree_paths(root) - self._allowed_post_review_paths
        )
        if unexpected_worktree:
            raise CodeStateError(
                "canonical code state is stale because worktree differs "
                f"after review: {sorted(unexpected_worktree)}"
            )

        return CanonicalCodeState(
            base_revision=base,
            reviewed_revision=reviewed,
            entries=self._entries(root, base, reviewed),
        )
