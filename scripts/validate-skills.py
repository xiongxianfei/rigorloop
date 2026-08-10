#!/usr/bin/env python3
"""Validate canonical or fixture skill content against the first-release contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skill_validation import CANONICAL_SKILLS_DIR, ValidationResult, validate_skill_tree


GATE_NAME = "Gate A (canonical skill integrity)"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate skill structure for canonical or fixture skill trees."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=str(CANONICAL_SKILLS_DIR),
        help="Path to a skill tree or a single SKILL.md file. Defaults to canonical skills/.",
    )
    return parser


def print_result(result: ValidationResult, target: Path) -> int:
    if result.errors:
        for error in result.errors:
            print(f"{GATE_NAME}: {error}", file=sys.stderr)
        return 1
    print(f"{GATE_NAME}: validated {len(result.checked_files)} skill files under {target}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    target = Path(args.target)
    return print_result(validate_skill_tree(target), target)


if __name__ == "__main__":
    raise SystemExit(main())
