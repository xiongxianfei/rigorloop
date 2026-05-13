#!/usr/bin/env python3
"""CI-friendly release validation wrapper."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from adapter_distribution import (
    ADAPTER_ARTIFACT_REPORT_ROOT,
    parse_adapter_artifact_metadata_yaml,
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run release validation in the shape required by CI."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Release tag to validate, such as v0.1.1 or v0.1.2.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source_commit = adapter_artifact_source_commit(args.version)
    if source_commit is None:
        return run_command(
            [sys.executable, "scripts/validate-release.py", "--version", args.version]
        )

    with tempfile.TemporaryDirectory(prefix="rigorloop-release-ci-") as release_output:
        build_status = run_command(
            [
                sys.executable,
                "scripts/build-adapters.py",
                "--version",
                args.version,
                "--output-dir",
                release_output,
            ]
        )
        if build_status:
            return build_status
        return run_command(
            [
                sys.executable,
                "scripts/validate-release.py",
                "--version",
                args.version,
                "--release-output-dir",
                release_output,
                "--release-commit",
                source_commit,
            ]
        )


if __name__ == "__main__":
    raise SystemExit(main())
