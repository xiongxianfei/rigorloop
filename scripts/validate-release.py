#!/usr/bin/env python3
"""Validate target-scoped release metadata and release notes."""

from __future__ import annotations

import argparse

from adapter_distribution import RELEASE_ROOT, validate_release_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate docs/releases/<version>/ release metadata and notes."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Release tag to validate, such as v0.1.0-rc.1 or v0.1.0.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = validate_release_output(args.version)
    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"validated release metadata for {args.version} under {RELEASE_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
