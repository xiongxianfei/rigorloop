#!/usr/bin/env python3
"""CI-friendly release validation wrapper."""

from __future__ import annotations

import argparse
import io
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

from adapter_distribution import (
    ADAPTER_ARTIFACT_REPORT_ROOT,
    parse_adapter_artifact_metadata_yaml,
    validate_adapter_artifact_metadata,
)


def adapter_artifact_source_commit(version: str) -> str | None:
    metadata_path = ADAPTER_ARTIFACT_REPORT_ROOT / f"{version}.yaml"
    if not metadata_path.is_file():
        return None
    metadata = parse_adapter_artifact_metadata_yaml(
        metadata_path.read_text(encoding="utf-8"),
        metadata_path,
    )
    return metadata.source_commit


def run_command(args: list[str]) -> int:
    completed = subprocess.run(args)
    return completed.returncode


def materialize_git_source(commit: str, destination: Path) -> int:
    completed = subprocess.run(
        ["git", "archive", commit],
        stdout=subprocess.PIPE,
    )
    if completed.returncode:
        return completed.returncode
    destination.mkdir(parents=True, exist_ok=True)
    destination_root = destination.resolve()
    with tarfile.open(fileobj=io.BytesIO(completed.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if target != destination_root and destination_root not in target.parents:
                print(f"unsafe git archive member: {member.name}", file=sys.stderr)
                return 1
        archive.extractall(destination)
    return 0


def validate_from_recorded_source(version: str, source_commit: str) -> int:
    with tempfile.TemporaryDirectory(prefix="rigorloop-release-ci-") as temp_root:
        temp_path = Path(temp_root)
        source_root = temp_path / "source"
        release_output = temp_path / "release-output"

        materialize_status = materialize_git_source(source_commit, source_root)
        if materialize_status:
            return materialize_status

        build_status = run_command(
            [
                sys.executable,
                str(source_root / "scripts" / "build-adapters.py"),
                "--version",
                version,
                "--output-dir",
                str(release_output),
            ]
        )
        if build_status:
            return build_status

        errors = validate_adapter_artifact_metadata(
            version,
            release_output,
            release_commit=source_commit,
        )
        if errors:
            for error in errors:
                print(error)
            return 1

    print(f"validated release metadata for {version} from recorded source {source_commit}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run release validation in the shape required by CI."
    )
    parser.add_argument(
        "--version",
        nargs="+",
        required=True,
        help="Release tag or tags to validate, such as v0.1.1 or v0.1.2.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    for version in args.version:
        source_commit = adapter_artifact_source_commit(version)
        if source_commit is None:
            status = run_command(
                [sys.executable, "scripts/validate-release.py", "--version", version]
            )
        else:
            status = validate_from_recorded_source(version, source_commit)
        if status:
            return status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
