#!/usr/bin/env python3
"""Build or check deterministic public adapter package output."""

from __future__ import annotations

import argparse

from adapter_distribution import (
    ADAPTER_OUTPUT_ROOT,
    DEFAULT_ADAPTER_VERSION,
    collect_adapter_drift_entries,
    format_adapter_drift_normal,
    format_adapter_drift_verbose,
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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="With --check, print complete adapter drift diagnostics.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.verbose and not args.check:
        parser.error("--verbose is only supported with --check")

    if args.check:
        drift = collect_adapter_drift_entries(args.version)
        if drift:
            if args.verbose:
                print(
                    format_adapter_drift_verbose(
                        drift,
                        version=args.version,
                        output_root=ADAPTER_OUTPUT_ROOT,
                    )
                )
            else:
                print(
                    format_adapter_drift_normal(
                        drift,
                        version=args.version,
                        output_root=ADAPTER_OUTPUT_ROOT,
                    )
                )
            return 1
        print(
            format_adapter_drift_normal(
                drift,
                version=args.version,
                output_root=ADAPTER_OUTPUT_ROOT,
            )
        )
        return 0

    sync_adapter_output(args.version)
    print(f"synced generated adapter output under {ADAPTER_OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
