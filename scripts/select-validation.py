#!/usr/bin/env python3
"""Select repository validation checks for changed paths."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validation_selection import (
    SelectionRequest,
    error_result,
    exit_code_for_status,
    select_validation,
    selection_result_to_json,
)


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = JsonArgumentParser(description=__doc__, add_help=True)
    parser.add_argument("--mode", choices=["local", "explicit", "pr", "main", "release"])
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--release-version")
    parser.add_argument("--broad-smoke", action="store_true")
    parser.add_argument("--trigger-context-path", action="append", default=[])
    parser.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--repo-root", default=".", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
    except ValueError as exc:
        result = error_result("unknown", str(exc))
        sys.stdout.write(selection_result_to_json(result))
        return exit_code_for_status(result.status)

    request = SelectionRequest(
        mode=args.mode or "",
        paths=tuple(args.path),
        base=args.base,
        head=args.head,
        release_version=args.release_version,
        broad_smoke=args.broad_smoke,
        trigger_context_paths=tuple(args.trigger_context_path),
        repo_root=Path(args.repo_root),
    )

    try:
        result = select_validation(request)
    except Exception as exc:  # pragma: no cover - CLI safety net
        result = error_result(args.mode or "unknown", f"internal selector failure: {exc}", code="internal-error")
    sys.stdout.write(selection_result_to_json(result))
    return exit_code_for_status(result.status)


if __name__ == "__main__":
    raise SystemExit(main())
