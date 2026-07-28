#!/usr/bin/env python3
"""Write or check boundary-first-v1 skill-local reference projections."""

from __future__ import annotations

import argparse
from pathlib import Path

from boundary_first_reference import (
    PROJECTION_MODES,
    ProjectionContractError,
    project_reference,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = "write" if args.write else "check"
    if selected not in PROJECTION_MODES:
        raise AssertionError("argparse emitted an unknown projection mode")
    try:
        result = project_reference(args.root, mode=selected)
    except ProjectionContractError as error:
        print(error)
        return 2
    for error in result.errors:
        print(error)
    print(f"BFR-SOURCE-SHA256: {result.source_sha256}")
    print(f"BFR-PROJECTION-SHA256: {result.projection_sha256}")
    print(f"BFR-PROJECTION-COUNT: {len(result.records)}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
