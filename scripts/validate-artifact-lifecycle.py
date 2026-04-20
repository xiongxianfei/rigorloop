#!/usr/bin/env python3
"""Validate lifecycle state for top-level workflow artifacts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from artifact_lifecycle_validation import ValidationFinding, ValidationInputError, validate_repository


ROOT = Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate lifecycle state for top-level workflow artifacts."
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=("explicit-paths", "local", "pr-ci", "push-main-ci"),
        help="How to determine validation scope.",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Repo-relative path to validate in explicit-paths mode. May be repeated.",
    )
    parser.add_argument("--base", help="Base SHA for pr-ci mode.")
    parser.add_argument("--head", help="Head SHA for pr-ci mode.")
    parser.add_argument("--before", help="Before SHA for push-main-ci mode.")
    parser.add_argument("--after", help="After SHA for push-main-ci mode.")
    parser.add_argument(
        "--pr-body-file",
        help="Optional repo-relative draft PR body file whose artifact references join scope.",
    )
    return parser


def format_finding(finding: ValidationFinding) -> str:
    path = finding.path.relative_to(ROOT).as_posix()
    prefix = "BLOCK" if finding.severity == "block" else "WARN"
    detail = f"{prefix} {path}"
    if finding.artifact_class:
        detail += f" [{finding.artifact_class}"
        if finding.status:
            detail += f", status={finding.status}"
        detail += "]"
    detail += f": {finding.message}"
    return detail


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        result = validate_repository(
            ROOT,
            mode=args.mode,
            paths=args.path,
            base=args.base,
            head=args.head,
            before=args.before,
            after=args.after,
            pr_body_file=args.pr_body_file,
        )
    except ValidationInputError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or str(exc), file=sys.stderr)
        return 2

    for finding in result.warning_findings:
        print(format_finding(finding))
    for finding in result.blocking_findings:
        print(format_finding(finding), file=sys.stderr)

    if result.blocking_findings:
        return 1

    print(f"validated {len(result.checked_artifacts)} artifact files in {args.mode} mode")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
