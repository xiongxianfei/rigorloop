#!/usr/bin/env python3
"""Validate README structure and optional vision marker boundaries."""

from __future__ import annotations

import argparse
from pathlib import Path


VISION_START = "<!-- vision:start -->"
VISION_END = "<!-- vision:end -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="README.md")
    parser.add_argument(
        "--vision-markers",
        action="store_true",
        help="validate standalone vision front-matter marker boundaries when present",
    )
    return parser.parse_args()


def validate_readme(path: Path, *, vision_markers: bool) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path} does not exist"]
    if not path.is_file():
        return [f"{path} is not a file"]

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [f"{path} is not valid UTF-8: {exc}"]

    lines = text.splitlines()
    if not text.strip():
        errors.append(f"{path} is empty")
    if not any(line.startswith("# ") for line in lines):
        errors.append(f"{path} has no Markdown H1 heading")

    if vision_markers:
        errors.extend(validate_vision_markers(lines))

    return errors


def validate_vision_markers(lines: list[str]) -> list[str]:
    start_lines = [index for index, line in enumerate(lines, start=1) if line == VISION_START]
    end_lines = [index for index, line in enumerate(lines, start=1) if line == VISION_END]

    if not start_lines and not end_lines:
        return []
    if len(start_lines) != 1 or len(end_lines) != 1:
        return [
            "vision front-matter markers must appear as zero or one standalone pair; "
            f"found {len(start_lines)} start marker(s) and {len(end_lines)} end marker(s)"
        ]
    if start_lines[0] > end_lines[0]:
        return [
            "vision front-matter start marker must appear before the end marker; "
            f"found start on line {start_lines[0]} and end on line {end_lines[0]}"
        ]
    return []


def marker_summary(path: Path, *, vision_markers: bool) -> str | None:
    if not vision_markers:
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    if VISION_START not in lines and VISION_END not in lines:
        return "Vision marker validation passed: no standalone marker block present"
    return "Vision marker validation passed: one standalone marker block present"


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    errors = validate_readme(path, vision_markers=args.vision_markers)
    if errors:
        print(f"README validation failed: {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"README validation passed: {path}")
    summary = marker_summary(path, vision_markers=args.vision_markers)
    if summary:
        print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
