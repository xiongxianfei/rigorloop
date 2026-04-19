#!/usr/bin/env python3
"""Build or check deterministic Codex compatibility output from canonical skills."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from skill_validation import CANONICAL_SKILLS_DIR, GENERATED_SKILLS_DIR


def collect_files(root: Path) -> dict[Path, Path]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root): path
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def collect_drift(source_root: Path, generated_root: Path) -> list[str]:
    source_files = collect_files(source_root)
    generated_files = collect_files(generated_root)
    errors: list[str] = []

    for relative_path, source_path in source_files.items():
        generated_path = generated_root / relative_path
        if relative_path not in generated_files:
            errors.append(
                f"missing generated file: {generated_path} (from {source_path})"
            )
            continue
        if source_path.read_bytes() != generated_files[relative_path].read_bytes():
            errors.append(
                f"stale generated file: {generated_path} differs from {source_path}"
            )

    for relative_path in sorted(set(generated_files) - set(source_files)):
        errors.append(f"unexpected generated file: {generated_root / relative_path}")

    return errors


def sync_generated_output(source_root: Path, generated_root: Path) -> None:
    source_files = collect_files(source_root)
    generated_files = collect_files(generated_root)

    generated_root.mkdir(parents=True, exist_ok=True)

    for relative_path, source_path in source_files.items():
        target_path = generated_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        source_bytes = source_path.read_bytes()
        if not target_path.exists() or target_path.read_bytes() != source_bytes:
            target_path.write_bytes(source_bytes)

    for relative_path in sorted(set(generated_files) - set(source_files), reverse=True):
        path = generated_root / relative_path
        if path.exists():
            path.unlink()

    empty_directories = sorted(
        (path for path in generated_root.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in empty_directories:
        try:
            directory.rmdir()
        except OSError:
            continue


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build or check .codex/skills from canonical skills/."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated output is missing, stale, or hand-edited.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.check:
        drift = collect_drift(CANONICAL_SKILLS_DIR, GENERATED_SKILLS_DIR)
        if drift:
            for entry in drift:
                print(entry)
            return 1
        print(f"generated skills are in sync under {GENERATED_SKILLS_DIR}")
        return 0

    sync_generated_output(CANONICAL_SKILLS_DIR, GENERATED_SKILLS_DIR)
    print(f"synced generated skills from {CANONICAL_SKILLS_DIR} to {GENERATED_SKILLS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
