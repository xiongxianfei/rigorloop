#!/usr/bin/env python3
"""Build or check deterministic public adapter package output."""

from __future__ import annotations

import argparse

from adapter_distribution import (
    ADAPTER_OUTPUT_ROOT,
    DEFAULT_ADAPTER_VERSION,
    collect_adapter_drift,
    sync_adapter_output,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build or check dist/adapters from canonical skills and adapter templates."
    )
    parser.add_argument(
        "--version",
        default=DEFAULT_ADAPTER_VERSION,
        help=f"Adapter package manifest version to render. Default: {DEFAULT_ADAPTER_VERSION}.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated adapter output is missing, stale, or hand-edited.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.check:
        drift = collect_adapter_drift(args.version)
        if drift:
            for entry in drift:
                print(entry)
            return 1
        print(f"generated adapter output is in sync under {ADAPTER_OUTPUT_ROOT}")
        return 0

    sync_adapter_output(args.version)
    print(f"synced generated adapter output under {ADAPTER_OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
