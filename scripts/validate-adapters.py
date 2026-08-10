#!/usr/bin/env python3
"""Validate generated public adapter package output."""

from __future__ import annotations

import argparse
from pathlib import Path

from adapter_distribution import (
    ADAPTER_OUTPUT_ROOT,
    CANONICAL_SKILLS_DIR,
    validate_adapter_archives,
    validate_adapter_output,
    validate_clean_install_smoke,
    validate_clean_install_skill_selection,
)


GATE_NAME = "Gate B (published adapter/package parity)"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate dist/adapters package structure, manifest consistency, and security."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Expected generated adapter manifest version, such as 0.1.0-rc.1.",
    )
    roots = parser.add_mutually_exclusive_group()
    roots.add_argument(
        "--adapter-root",
        help="Validate release archives in this output directory.",
    )
    roots.add_argument(
        "--root",
        help="Legacy alias for --adapter-root.",
    )
    parser.add_argument(
        "--clean-install-smoke",
        action="store_true",
        help="Install locally packed release archives into empty temporary target projects and validate mapped resources.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Skill name to include in clean-install mapped-resource validation. Repeat to validate multiple skills.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    archive_root = args.adapter_root or args.root
    if args.clean_install_smoke and not archive_root:
        print(
            f"{GATE_NAME}: --clean-install-smoke requires --adapter-root "
            "(legacy --root also accepted) with locally packed release archives"
        )
        return 1
    root = Path(archive_root) if archive_root else ADAPTER_OUTPUT_ROOT
    if archive_root:
        errors = (
            validate_clean_install_skill_selection(
                CANONICAL_SKILLS_DIR,
                tuple(args.skill),
            )
            if args.clean_install_smoke
            else []
        )
        if not errors:
            errors = validate_adapter_archives(args.version, root)
        if args.clean_install_smoke and not errors:
            errors.extend(
                validate_clean_install_smoke(
                    args.version,
                    root,
                    skill_names=tuple(args.skill),
                )
            )
    else:
        errors = validate_adapter_output(args.version)
    if errors:
        for error in errors:
            print(f"{GATE_NAME}: {error}")
        return 1

    if args.clean_install_smoke:
        skills = ", ".join(args.skill) if args.skill else "all mapped-resource skills"
        print(
            f"{GATE_NAME}: validated generated adapter archives and clean installs for version {args.version} "
            f"under {root} ({skills})"
        )
    elif archive_root:
        print(f"{GATE_NAME}: validated generated adapter archives for version {args.version} under {root}")
    else:
        print(f"{GATE_NAME}: validated generated adapters for version {args.version} under {ADAPTER_OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
