#!/usr/bin/env python3
"""Generate published release evidence from public GitHub/npm/npx proof."""

from __future__ import annotations

import argparse
from pathlib import Path

from release_transaction import ReleaseProfileError, close_release_publication


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Close published release evidence from public GitHub, npm, and npx proof."
    )
    parser.add_argument("tag", help="Release tag to close, such as v0.3.5.")
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--public-evidence",
        help=(
            "Path to collected public evidence. Defaults to "
            "docs/releases/<tag>/public-evidence.yaml."
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report pending closeout changes without writing files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    public_evidence = Path(args.public_evidence) if args.public_evidence else None
    try:
        result = close_release_publication(
            args.tag,
            root=Path(args.root),
            public_evidence=public_evidence,
            check=args.check,
        )
    except ReleaseProfileError as exc:
        for error in exc.errors:
            print(error)
        return 1
    if result.errors:
        for error in result.errors:
            print(error)
        return 1
    if result.changed_paths:
        print(f"closed {result.release_tag}: {len(result.changed_paths)} file(s) updated")
        for path in result.changed_paths:
            print(path)
    else:
        print(f"closed {result.release_tag}: no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
