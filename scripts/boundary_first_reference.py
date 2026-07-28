#!/usr/bin/env python3
"""Canonical inventory and raw-byte projection for boundary-first-v1."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping

METHOD_VERSION = "boundary-first-v1"
CANONICAL_REFERENCE = Path(
    "specs/references/boundary-first-method-v1.md"
)
PROJECTED_REFERENCE = Path("references/boundary-first-method-v1.md")
GOVERNED_SKILLS = (
    "workflow",
    "spec",
    "spec-review",
    "plan",
    "plan-review",
    "test-spec",
    "test-spec-review",
    "implement",
    "code-review",
    "verify",
)
PROJECTION_MODES = frozenset({"check", "write"})


class ProjectionContractError(ValueError):
    """Raised when a closed projection input is invalid."""


@dataclass(frozen=True)
class ProjectionResult:
    ok: bool
    mode: str
    source_sha256: str
    projection_sha256: str
    records: Mapping[str, str]
    errors: tuple[str, ...]


def raw_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory_digest(records: Mapping[str, str]) -> str:
    """Hash sorted POSIX path, NUL, raw-byte digest, newline records."""

    serialized = b"".join(
        f"{PurePosixPath(path)}\0{records[path].lower()}\n".encode("utf-8")
        for path in sorted(records)
    )
    return raw_sha256(serialized)


def projected_paths() -> tuple[Path, ...]:
    return tuple(
        Path("skills") / skill / PROJECTED_REFERENCE
        for skill in GOVERNED_SKILLS
    )


def _relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _unexpected_projections(root: Path) -> tuple[Path, ...]:
    expected = {root / path for path in projected_paths()}
    found = set(
        (root / "skills").glob(
            "*/references/boundary-first-method-v1.md"
        )
    )
    return tuple(sorted(found - expected))


def project_reference(root: Path, *, mode: str) -> ProjectionResult:
    """Write or check the closed boundary-first reference projection."""

    if mode not in PROJECTION_MODES:
        raise ProjectionContractError(
            f"BFR-MODE-UNKNOWN: unknown projection mode '{mode}'"
        )

    repository_root = root.resolve()
    source = repository_root / CANONICAL_REFERENCE
    if source.is_symlink() or not source.is_file():
        raise ProjectionContractError(
            f"BFR-SOURCE-MISSING: {CANONICAL_REFERENCE.as_posix()}"
        )
    source_bytes = source.read_bytes()
    source_sha256 = raw_sha256(source_bytes)
    errors: list[str] = []

    if mode == "write":
        for relative in projected_paths():
            target = repository_root / relative
            if target.is_symlink():
                target.unlink()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source_bytes)

    records: dict[str, str] = {}
    for relative in projected_paths():
        target = repository_root / relative
        relative_text = relative.as_posix()
        if target.is_symlink():
            errors.append(f"BFR-PROJECTION-SYMLINK: {relative_text}")
            continue
        if not target.is_file():
            errors.append(f"BFR-PROJECTION-MISSING: {relative_text}")
            continue
        actual = raw_sha256(target.read_bytes())
        records[relative_text] = actual
        if actual != source_sha256:
            errors.append(f"BFR-PROJECTION-STALE: {relative_text}")

    for unexpected in _unexpected_projections(repository_root):
        errors.append(
            "BFR-PROJECTION-UNEXPECTED: "
            + _relative_posix(unexpected, repository_root)
        )

    return ProjectionResult(
        ok=not errors,
        mode=mode,
        source_sha256=source_sha256,
        projection_sha256=inventory_digest(records),
        records=records,
        errors=tuple(sorted(errors)),
    )
