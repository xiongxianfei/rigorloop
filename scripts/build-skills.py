#!/usr/bin/env python3
"""Build or check deterministic Codex compatibility output from canonical skills."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

from skill_validation import (
    CANONICAL_SKILLS_DIR,
    GENERATED_SKILLS_DIR,
    discover_source_skill_dirs,
    mapped_resource_parity_errors,
    validate_skill_tree,
)


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


def validate_generated_output(generated_root: Path) -> list[str]:
    result = validate_skill_tree(generated_root, allow_generated=True)
    return result.errors


def collect_generated_resource_parity_errors(source_root: Path, generated_root: Path) -> list[str]:
    errors: list[str] = []
    for skill_dir in discover_source_skill_dirs(source_root):
        errors.extend(
            mapped_resource_parity_errors(
                skill_dir,
                generated_root / skill_dir.name,
                surface_label="generated local skill mirror",
            )
        )
    return errors


def check_generated_output(source_root: Path, output_root: Path) -> list[str]:
    sync_generated_output(source_root, output_root)
    errors = validate_generated_output(output_root)
    if errors:
        return errors
    resource_parity_errors = collect_generated_resource_parity_errors(source_root, output_root)
    if resource_parity_errors:
        return resource_parity_errors
    return collect_drift(source_root, output_root)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build or check .codex/skills from canonical skills/."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Generate and validate local mirror output without requiring tracked .codex/skills files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Write generated skill mirror output to this directory. Defaults to .codex/skills outside --check; --check uses a temporary directory when omitted.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.check:
        if args.output_dir is None:
            with tempfile.TemporaryDirectory(prefix="rigorloop-skills-check-") as tmpdir:
                output_root = Path(tmpdir) / "skills"
                errors = check_generated_output(CANONICAL_SKILLS_DIR, output_root)
                if errors:
                    for entry in errors:
                        print(entry)
                    return 1
                print(
                    "validated generated skills from "
                    f"{CANONICAL_SKILLS_DIR} using temporary output {output_root}"
                )
                return 0

        errors = check_generated_output(CANONICAL_SKILLS_DIR, args.output_dir)
        if errors:
            for entry in errors:
                print(entry)
            return 1
        print(
            f"validated generated skills from {CANONICAL_SKILLS_DIR} under {args.output_dir}"
        )
        return 0

    output_root = args.output_dir or GENERATED_SKILLS_DIR
    sync_generated_output(CANONICAL_SKILLS_DIR, output_root)
    print(f"synced generated skills from {CANONICAL_SKILLS_DIR} to {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
