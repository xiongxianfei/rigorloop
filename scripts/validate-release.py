#!/usr/bin/env python3
"""Validate target-scoped release metadata and release notes."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from adapter_distribution import RELEASE_ROOT, validate_release_output
from release_transaction import (
    profile_path_for_tag,
    validate_published_release_artifacts,
    validate_release_timing_evidence,
)


def read_changed_paths_file(path: Path) -> list[str]:
    changed_paths: list[str] = []
    seen: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        value = raw_line.strip()
        if not value or value.startswith("#"):
            continue
        normalized = value.replace("\\", "/")
        if normalized in seen:
            continue
        seen.add(normalized)
        changed_paths.append(normalized)
    return changed_paths


def merge_changed_paths(
    inline_paths: list[str],
    file_path: str | None,
) -> tuple[str, ...]:
    changed_paths: list[str] = []
    seen: set[str] = set()
    for value in inline_paths:
        normalized = value.strip().replace("\\", "/")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        changed_paths.append(normalized)
    if file_path:
        for normalized in read_changed_paths_file(Path(file_path)):
            if normalized in seen:
                continue
            seen.add(normalized)
            changed_paths.append(normalized)
    return tuple(changed_paths)


def current_git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def validate_release_transaction_timing(version: str) -> tuple[list[str], list[str]]:
    profile_path = profile_path_for_tag(version)
    if not profile_path.exists():
        return [], []

    result = validate_release_timing_evidence(version)
    return list(result.errors), list(result.warnings)


def validate_release_transaction_published_evidence(version: str) -> list[str]:
    npm_publication = Path("docs") / "releases" / version / "npm-publication.md"
    if not npm_publication.exists():
        return []
    text = npm_publication.read_text(encoding="utf-8")
    if "Status: published" not in text:
        return []
    return validate_published_release_artifacts(version)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate docs/releases/<version>/ release metadata and notes."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Release tag to validate, such as v0.1.0-rc.1 or v0.1.0.",
    )
    parser.add_argument(
        "--changed-path",
        action="append",
        default=[],
        help="Repo-relative changed path to use for release changed-surface analysis.",
    )
    parser.add_argument(
        "--changed-paths-file",
        help="Line-based file of repo-relative changed paths for release changed-surface analysis.",
    )
    parser.add_argument(
        "--release-output-dir",
        help="Directory containing generated release adapter archives for archive metadata validation.",
    )
    parser.add_argument(
        "--release-commit",
        help=(
            "Release/source commit expected in adapter artifact metadata. "
            "Defaults to the current Git HEAD."
        ),
    )
    parser.add_argument(
        "--npm-tarball-root",
        help="Directory containing the packed npm tarball named by bootstrap publication evidence.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    changed_paths = merge_changed_paths(args.changed_path, args.changed_paths_file)
    changed_paths_arg = changed_paths if args.changed_path or args.changed_paths_file else ()
    release_output_dir = Path(args.release_output_dir) if args.release_output_dir else None
    npm_tarball_root = Path(args.npm_tarball_root) if args.npm_tarball_root else None
    release_commit = args.release_commit or current_git_commit()
    errors = validate_release_output(
        args.version,
        changed_paths=changed_paths_arg,
        release_output_dir=release_output_dir,
        release_commit=release_commit,
        npm_tarball_root=npm_tarball_root,
    )
    timing_errors, timing_warnings = validate_release_transaction_timing(args.version)
    errors.extend(timing_errors)
    for warning in timing_warnings:
        print(f"[WARN] {warning}", file=sys.stderr)
    errors.extend(validate_release_transaction_published_evidence(args.version))
    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"validated release metadata for {args.version} under {RELEASE_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
