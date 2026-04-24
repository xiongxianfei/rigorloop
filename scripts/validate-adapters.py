#!/usr/bin/env python3
"""Validate generated public adapter package output."""

from __future__ import annotations

import argparse

from adapter_distribution import ADAPTER_OUTPUT_ROOT, validate_adapter_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate dist/adapters package structure, manifest consistency, and security."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Expected generated adapter manifest version, such as 0.1.0-rc.1.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = validate_adapter_output(args.version)
    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"validated generated adapters for version {args.version} under {ADAPTER_OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
