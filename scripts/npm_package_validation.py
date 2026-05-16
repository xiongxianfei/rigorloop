#!/usr/bin/env python3
"""Validation helpers for the public RigorLoop npm package tarball."""

from __future__ import annotations

import json
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_PACKAGE_PATHS = frozenset(
    {
        "package/package.json",
        "package/README.md",
        "package/LICENSE",
        "package/dist/bin/rigorloop.js",
        "package/dist/lib/command-result.js",
        "package/dist/lib/lockfile.js",
        "package/dist/lib/new-change-filesystem.js",
        "package/dist/lib/new-change.js",
        "package/dist/lib/official-archive-url.js",
        "package/dist/metadata/adapter-artifacts-v0.1.4.json",
        "package/dist/metadata/releases.json",
    }
)

FORBIDDEN_PATH_PATTERNS = (
    "package/test/**",
    "package/tests/**",
    "package/__fixtures__/**",
    "package/docs/**",
    "package/release-output/**",
    "package/.codex/**",
    "package/.agents/**",
    "package/dist/adapters/**",
    "package/**/*.zip",
    "package/**/*.tgz",
    "package/**/*.pem",
    "package/**/*.key",
    "package/**/*.env",
    "package/.npmrc",
    "package/**/*.npmrc",
)

FORBIDDEN_CONTENT_MARKERS = (
    "NPM_TOKEN",
    "npm_",
    "BEGIN PRIVATE KEY",
    "/tmp/",
    "/home/",
)

FORBIDDEN_LIFECYCLE_SCRIPTS = frozenset({"preinstall", "install", "postinstall", "prepare", "prepack"})
FORBIDDEN_SUFFIXES = (".zip", ".tgz", ".pem", ".key")


class NpmPackageValidationError(Exception):
    """Raised when the npm package publication boundary is invalid."""


@dataclass(frozen=True)
class PackageTarballReport:
    tarball: Path
    paths: frozenset[str]
    missing_paths: tuple[str, ...]
    forbidden_paths: tuple[str, ...]


def validate_package_policy(package_json: dict[str, Any]) -> None:
    scripts = package_json.get("scripts") or {}
    for script_name in sorted(FORBIDDEN_LIFECYCLE_SCRIPTS):
        if script_name in scripts:
            raise NpmPackageValidationError(f"forbidden lifecycle script: {script_name}")

    dependencies = package_json.get("dependencies") or {}
    if dependencies:
        raise NpmPackageValidationError("runtime dependencies require an approved recorded purpose before publication")


def inspect_package_json(package_root: Path) -> None:
    package_json_path = package_root / "package.json"
    package_json = json.loads(package_json_path.read_text(encoding="utf-8"))
    validate_package_policy(package_json)


def inspect_package_tarball(tarball: Path) -> PackageTarballReport:
    tarball = tarball.resolve()
    with tarfile.open(tarball, "r:gz") as archive:
        members = archive.getmembers()
        paths = frozenset(member.name for member in members)
        forbidden_paths = tuple(sorted(path for path in paths if is_forbidden_path(path)))
        missing_paths = tuple(sorted(REQUIRED_PACKAGE_PATHS - paths))

        if missing_paths:
            raise NpmPackageValidationError(f"missing required package paths: {', '.join(missing_paths)}")
        if forbidden_paths:
            raise NpmPackageValidationError(f"forbidden package paths: {', '.join(forbidden_paths)}")

        for member in members:
            if member.isfile() and member.size <= 1024 * 1024:
                stream = archive.extractfile(member)
                if stream is None:
                    continue
                text = stream.read().decode("utf-8", errors="ignore")
                marker = first_forbidden_content_marker(text)
                if marker is not None:
                    raise NpmPackageValidationError(f"forbidden content marker in {member.name}: {marker}")

    return PackageTarballReport(tarball=tarball, paths=paths, missing_paths=missing_paths, forbidden_paths=forbidden_paths)


def is_forbidden_path(path: str) -> bool:
    normalized = normalize_tarball_path(path)
    if not normalized.startswith("package/"):
        return True

    relative = normalized[len("package/") :]
    parts = [part for part in relative.split("/") if part]
    if not parts:
        return False

    filename = parts[-1].lower()
    if filename.endswith(FORBIDDEN_SUFFIXES):
        return True
    if filename == ".env" or filename.endswith(".env"):
        return True

    if parts[0] in {".codex", ".agents"}:
        return True
    if parts[0] in {"test", "tests", "__fixtures__", "docs", "release-output"}:
        return True
    if len(parts) >= 2 and parts[0] == "dist" and parts[1] == "adapters":
        return True

    return False


def normalize_tarball_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def first_forbidden_content_marker(text: str) -> str | None:
    for marker in FORBIDDEN_CONTENT_MARKERS:
        if marker in text:
            return marker
    return None
