#!/usr/bin/env python3
"""Generate routine pending release artifacts from a release profile."""

from __future__ import annotations

import argparse
from pathlib import Path

from release_transaction import ReleaseProfileError, prepare_release


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate pending routine release artifacts from docs/releases/profiles/<tag>.yaml."
    )
    parser.add_argument("tag", help="Release tag to prepare, such as v0.3.5.")
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report pending changes without writing files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = prepare_release(args.tag, root=Path(args.root), check=args.check)
    except ReleaseProfileError as exc:
        for error in exc.errors:
            print(error)
        return 1
    if result.changed_paths:
        print(f"prepared {result.release_tag}: {len(result.changed_paths)} file(s) updated")
        for path in result.changed_paths:
            print(path)
    else:
        print(f"prepared {result.release_tag}: no changes")
    print(f"next: python scripts/release-preflight.py {result.release_tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
