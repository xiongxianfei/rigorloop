#!/usr/bin/env python3
"""Validate target-scoped release metadata and release notes."""

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
    ADAPTER_TEMPLATE_ROOT,
    RELEASE_ROOT,
    ReleaseValidationProfile,
    parse_adapter_artifact_metadata_yaml,
    validate_release_output,
)
from release_transaction import (
    profile_path_for_tag,
    validate_published_release_artifacts,
    validate_release_timing_evidence,
)


GATE_NAME = "Gate C (release integrity)"


def read_changed_paths_file(path: Path) -> list[str]:
    changed_paths: list[str] = []
    seen: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        value = raw_line.strip()
        if not value or value.startswith("#"):
            continue
        normalized = value.replace("\\", "/")
        if normalized in seen:
            continue
        seen.add(normalized)
        changed_paths.append(normalized)
    return changed_paths


def merge_changed_paths(
    inline_paths: list[str],
    file_path: str | None,
) -> tuple[str, ...]:
    changed_paths: list[str] = []
    seen: set[str] = set()
    for value in inline_paths:
        normalized = value.strip().replace("\\", "/")
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        changed_paths.append(normalized)
    if file_path:
        for normalized in read_changed_paths_file(Path(file_path)):
            if normalized in seen:
                continue
            seen.add(normalized)
            changed_paths.append(normalized)
    return tuple(changed_paths)


def current_git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


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
    return subprocess.run(args).returncode


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
                print(f"{GATE_NAME}: unsafe git archive member: {member.name}", file=sys.stderr)
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

        print(
            "[INFO] recorded-source profile: current canonical skill/archive "
            f"content policy is not applied to historical release source {version}"
        )
        errors = validate_release_output(
            version,
            skills_root=source_root / "skills",
            template_root=source_root / "scripts" / "adapter_templates"
            if (source_root / "scripts" / "adapter_templates").is_dir()
            else ADAPTER_TEMPLATE_ROOT,
            release_output_dir=release_output,
            release_commit=source_commit,
            profile=ReleaseValidationProfile.RECORDED_SOURCE,
        )
        if errors:
            for error in errors:
                print(f"{GATE_NAME}: {error}")
            return 1

    print(f"{GATE_NAME}: validated release metadata for {version} from recorded source {source_commit}")
    return 0


def validate_release_transaction_timing(version: str) -> tuple[list[str], list[str]]:
    profile_path = profile_path_for_tag(version)
    if not profile_path.exists():
        return [], []

    result = validate_release_timing_evidence(version)
    return list(result.errors), list(result.warnings)


def validate_release_transaction_published_evidence(version: str) -> list[str]:
    npm_publication = Path("docs") / "releases" / version / "npm-publication.md"
    if not npm_publication.exists():
        return []
    text = npm_publication.read_text(encoding="utf-8")
    if "Status: published" not in text:
        return []
    return validate_published_release_artifacts(version)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate docs/releases/<version>/ release metadata and notes."
    )
    parser.add_argument(
        "--version",
        nargs="+",
        required=True,
        help="Release tag or tags to validate, such as v0.1.0-rc.1 or v0.1.0.",
    )
    parser.add_argument(
        "--recorded-source-auto",
        action="store_true",
        help=(
            "For repository CI, rebuild historical releases from the source commit "
            "recorded in adapter artifact metadata."
        ),
    )
    parser.add_argument(
        "--changed-path",
        action="append",
        default=[],
        help="Repo-relative changed path to use for release changed-surface analysis.",
    )
    parser.add_argument(
        "--changed-paths-file",
        help="Line-based file of repo-relative changed paths for release changed-surface analysis.",
    )
    parser.add_argument(
        "--release-output-dir",
        help="Directory containing generated release adapter archives for archive metadata validation.",
    )
    parser.add_argument(
        "--release-commit",
        help=(
            "Release/source commit expected in adapter artifact metadata. "
            "Defaults to the current Git HEAD."
        ),
    )
    parser.add_argument(
        "--npm-tarball-root",
        help="Directory containing the packed npm tarball named by bootstrap publication evidence.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.recorded_source_auto and (
        args.changed_path
        or args.changed_paths_file
        or args.release_output_dir
        or args.release_commit
        or args.npm_tarball_root
    ):
        parser.error(
            "--recorded-source-auto cannot be combined with changed-path, "
            "release-output, release-commit, or npm-tarball options"
        )

    changed_paths = merge_changed_paths(args.changed_path, args.changed_paths_file)
    changed_paths_arg = changed_paths if args.changed_path or args.changed_paths_file else ()
    release_output_dir = Path(args.release_output_dir) if args.release_output_dir else None
    npm_tarball_root = Path(args.npm_tarball_root) if args.npm_tarball_root else None
    for version in args.version:
        if args.recorded_source_auto:
            source_commit = adapter_artifact_source_commit(version)
            if source_commit is not None:
                status = validate_from_recorded_source(version, source_commit)
                if status:
                    return status
                continue

        release_commit = args.release_commit or current_git_commit()
        errors = validate_release_output(
            version,
            changed_paths=changed_paths_arg,
            release_output_dir=release_output_dir,
            release_commit=release_commit,
            npm_tarball_root=npm_tarball_root,
        )
        timing_errors, timing_warnings = validate_release_transaction_timing(version)
        errors.extend(timing_errors)
        for warning in timing_warnings:
            print(f"{GATE_NAME}: [WARN] {warning}", file=sys.stderr)
        errors.extend(validate_release_transaction_published_evidence(version))
        if errors:
            for error in errors:
                print(f"{GATE_NAME}: {error}")
            return 1

        print(f"{GATE_NAME}: validated release metadata for {version} under {RELEASE_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
