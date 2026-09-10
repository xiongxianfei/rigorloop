#!/usr/bin/env python3
"""Validate target-scoped release metadata and release notes."""

from __future__ import annotations

import argparse
import io
import json
import os
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


def validate_prepared_release(version: str, root: Path, output: Path) -> list[str]:
    """Prepublication applicability of the retained release/evidence/security checks.

    Pending public observations are expectations, never passes. Actual local
    correctness is recorded by the full verifier, separately from those fields.
    Historical finalized-release validation continues through validate_release_output.
    """
    import json
    from release_transaction import (load_release_profile, is_routine_release_profile,
        validate_pending_release_artifacts, _release_notes_generated_block)
    from adapter_distribution import scan_security_paths
    from release_candidate import file_identity, local_file, run, CandidateError
    errors = []
    try:
        profile = load_release_profile(version, root=root)
        if not is_routine_release_profile(profile):
            return ['prepared verification requires a supported routine profile']
        errors.extend(validate_pending_release_artifacts(version, root=root))
        paths = [root / 'docs/releases' / version, root / 'docs/releases' / (version + '.md'), profile.path]
        errors.extend(scan_security_paths(paths))
        notes = (paths[0] / 'release-notes.md').read_text()
        if not notes.startswith('# RigorLoop ' + version + '\n'):
            errors.append('release notes version mismatch')
        if _release_notes_generated_block(profile).strip() not in notes:
            errors.append('release notes generated metadata does not match profile')
        facts = json.loads((output / 'preparation.json').read_text())
        if facts['tag'] != version or facts['prepared_commit'] != run(['git', 'rev-parse', 'HEAD'], root):
            errors.append('prepared release source identity mismatch')
        if run(['git', 'rev-parse', 'HEAD^'], root) != facts['source_commit']:
            errors.append('prepared release parent identity mismatch')
        for name, identity in facts['files'].items():
            if file_identity(local_file(output, name)) != identity:
                errors.append('prepared artifact identity mismatch: ' + name)
        metadata = json.loads((output / ('adapter-artifacts-' + version + '.json')).read_text())
        if metadata['release']['source_commit'] != facts['prepared_commit'] or metadata['release']['release_tag'] != version:
            errors.append('adapter metadata release identity mismatch')
        proof = output / ('archive-proof-' + version + '.json')
        if metadata['metadata']['sha256'] != file_identity(proof)['sha256']:
            errors.append('adapter proof identity mismatch')
        if {a['adapter'] for a in metadata['artifacts']} != set(profile.targets):
            errors.append('adapter metadata target inventory mismatch')
        for artifact in metadata['artifacts']:
            if artifact['sha256'] != file_identity(local_file(output, artifact['archive']))['sha256']:
                errors.append('adapter metadata archive identity mismatch')
        # The package-bound metadata must be exactly the archive-derived public
        # metadata; its index is the trust root consumed by the installed CLI.
        with tarfile.open(local_file(output, facts['tarball'])) as packed:
            raw = packed.extractfile('package/dist/metadata/adapter-artifacts-' + version + '.json').read()
            index = json.load(packed.extractfile('package/dist/metadata/releases.json'))
            import hashlib
            if raw != (output / ('adapter-artifacts-' + version + '.json')).read_bytes():
                errors.append('packed/public metadata mismatch')
            if index['releases'][version]['bundled_metadata_sha256'] != hashlib.sha256(raw).hexdigest():
                errors.append('packed metadata trust index mismatch')
    except (OSError, ValueError, KeyError, TypeError, AttributeError, tarfile.TarError) as exc:
        errors.append('missing or invalid prepared release facts: ' + str(exc))
    return errors


def recorded_command(command: list[str], root: Path, output: Path) -> str:
    """Describe exact arguments by declared inputs, without worker-local paths."""
    shown = []
    for argument in command:
        path = Path(argument)
        if path.is_absolute():
            if path.is_relative_to(output):
                argument = '<candidate>/' + path.relative_to(output).as_posix()
            elif path.is_relative_to(root):
                argument = path.relative_to(root).as_posix()
            else:
                raise ValueError('undeclared external command input cannot enter release evidence')
        shown.append(argument)
    return ' '.join(shown)


def verify_prepared_release(version: str, output: Path) -> int:
    """Complete new-path composition, reached through release-verify.sh.

    Keep the actual validators and their security/negative/regression protection;
    only the public-event/timing applicability differs before publication.
    """
    import json
    import time
    from release_candidate import run, run_packed_smoke, timing_diagnostics, canonical_bytes, local_file
    root = Path.cwd()
    receipt = output / 'release-verification.json'
    receipt.unlink(missing_ok=True)
    errors = validate_prepared_release(version, root, output)
    if errors:
        for error in errors:
            print('Release integrity: ' + error, file=sys.stderr)
        return 1
    facts = json.loads((output / 'preparation.json').read_text())
    checks = []
    commands = [
        ['python', 'scripts/validate-skills.py'],
        ['python', 'scripts/test-skill-validator.py'],
        ['python', 'scripts/build-skills.py', '--check'],
        ['python', 'scripts/test-adapter-distribution.py'],
        ['python', 'scripts/test-npm-package-publication.py'],
        ['python', 'scripts/validate-adapters.py', '--version', version, '--adapter-root', str(output)],
        ['python', 'scripts/validate-npm-package.py', '--tarball', str(local_file(output, facts['tarball']))],
    ]
    for command in commands:
        started = time.monotonic()
        print('Release check: ' + ' '.join(command[:2]), flush=True)
        run(command, root)
        checks.append({'command': recorded_command(command, root, output), 'result': 'pass', 'duration_seconds': time.monotonic() - started})
    run_packed_smoke(root, local_file(output, facts['tarball']), output, version)
    checks.append({'command': 'packed CLI version and init codex/claude/opencode', 'result': 'pass'})
    errors = validate_prepared_release(version, root, output)
    if errors:
        raise ValueError('; '.join(errors))
    checks.append({'command': 'python scripts/validate-release.py --prepared-candidate (release facts, notes, evidence, metadata and security)', 'result': 'pass'})
    receipt.write_bytes(canonical_bytes({'prepared_commit': facts['prepared_commit'], 'checks': checks,
        'diagnostics': timing_diagnostics(root, version), 'result': 'pass'}))
    return 0


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
    parser.add_argument("--prepared-candidate", help="Exact local candidate output; complete prepublication checks, no publication.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.prepared_candidate:
        if len(args.version) != 1 or args.recorded_source_auto or args.changed_path or args.changed_paths_file or args.release_output_dir or args.release_commit or args.npm_tarball_root:
            parser.error("prepared-candidate requires one version and no historical-mode options")
        return verify_prepared_release(args.version[0], Path(args.prepared_candidate).resolve())
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
        context = (os.environ.get('RIGORLOOP_CI_CANDIDATE')
                   if os.environ.get('RIGORLOOP_CI_WORKSPACE') == str(Path.cwd()) else None)
        if context and args.recorded_source_auto:
            from release_candidate import ci_subject
            output = Path(context)
            candidate_tag = json.loads((output / 'candidate.json').read_text())['tag']
            if version == candidate_tag:
                ci_subject(output, Path.cwd())
                errors = validate_prepared_release(version, Path.cwd(), output)
                if errors:
                    for error in errors:
                        print('Release integrity: ' + error, file=sys.stderr)
                    return 1
                print('Release integrity: checked prepared candidate and its full verification receipt for ' + version)
                continue
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
