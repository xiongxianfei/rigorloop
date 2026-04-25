#!/usr/bin/env python3
"""Validate change-local review artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from review_artifact_validation import format_finding, validate_change_root


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        default="structure",
        choices=["structure"],
        help="validation mode; closeout mode is added in a later milestone",
    )
    parser.add_argument("change_roots", nargs="+", help="docs/changes/<change-id> roots to validate")
    args = parser.parse_args(argv)

    failed = False
    for raw_root in args.change_roots:
        change_root = Path(raw_root)
        result = validate_change_root(change_root, mode=args.mode)
        if result.blocking_findings:
            failed = True
            print(
                f"{raw_root}: review artifact validation failed "
                f"(mode={result.mode}, findings={len(result.blocking_findings)})",
                file=sys.stderr,
            )
            for finding in result.blocking_findings:
                print(f"  - {format_finding(finding, root=ROOT)}", file=sys.stderr)
            continue

        print(
            f"{raw_root}: review artifact validation passed "
            f"(mode={result.mode}, reviews={result.review_count}, "
            f"findings={result.finding_count}, log_entries={result.review_log_entry_count}, "
            f"resolution_entries={result.resolution_entry_count})"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
