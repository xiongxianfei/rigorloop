#!/usr/bin/env python3
"""Run cheap deterministic release-state checks before full release verification."""

from __future__ import annotations

import argparse
from pathlib import Path

from release_transaction import (
    ReleasePreflightChangedFilesError,
    discover_changed_files,
    release_preflight,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate cheap local release state before running release-verify."
    )
    parser.add_argument("tag", help="Release tag to preflight, such as v0.3.5.")
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=(),
        help="Changed file path used by the current-version literal audit. May be repeated.",
    )
    parser.add_argument(
        "--skip-remote",
        action="store_true",
        help="Skip reachable remote tag checks.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root)
    if args.changed_file:
        changed_files = tuple(args.changed_file)
        changed_file_source = "explicit --changed-file"
    else:
        try:
            changed_files = discover_changed_files(root)
        except ReleasePreflightChangedFilesError as exc:
            print(f"release-preflight {args.tag}: fail")
            print(str(exc))
            return 1
        changed_file_source = "git"
    result = release_preflight(
        args.tag,
        root=root,
        changed_files=changed_files,
        check_remote=not args.skip_remote,
    )
    print(f"release preflight changed-file source: {changed_file_source}")
    if changed_files:
        print("release preflight changed files: " + ", ".join(changed_files))
    else:
        print("release preflight changed files: none")
    for warning in result.warnings:
        print(f"warning: {warning}")
    if result.errors:
        print(f"release-preflight {result.release_tag}: fail")
        for error in result.errors:
            print(error)
        return 1
    print(f"release-preflight {result.release_tag}: pass")
    print(f"next: bash scripts/release-verify.sh {result.release_tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
