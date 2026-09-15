#!/usr/bin/env python3
"""Validate target-scoped release metadata and release notes."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

GATE_NAME = "Gate C (release integrity)"


def current_git_commit(root: Path | None = None) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()


def current_source_errors(version: str, root: Path, release_commit: str | None = None) -> list[str]:
    """Admit current explicit source/profile identities before any output write."""
    from lib.release.release_candidate import local_file, version_tuple
    from lib.release.release_transaction import load_release_profile, is_routine_release_profile
    try:
        if not version.startswith('v'):
            raise ValueError('release tag must start with v')
        version_tuple(version[1:])
        package = json.loads(local_file(root, 'packages/rigorloop/package.json').read_text())
        if package.get('name') != '@xiongxianfei/rigorloop' or version != 'v' + str(package.get('version')):
            return ['historical-replay: requested tag does not match the selected current source package']
        local_file(root, 'docs/releases/profiles/' + version + '.yaml')
        profile = load_release_profile(version, root=root)
        if not is_routine_release_profile(profile) or profile.package_version != package['version']:
            return ['current-source: release profile does not match the selected source package']
        if release_commit is not None and release_commit != current_git_commit(root):
            return ['current-source: explicit recorded commit does not match selected source HEAD']
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        return ['current-source: missing or invalid matching source package, release profile or recorded commit']
    return []






def validate_prepared_release(version: str, root: Path, output: Path) -> list[str]:
    """Prepublication applicability of the retained release/evidence/security checks.

    Pending public observations are expectations, never passes. Actual local
    correctness is recorded by the full verifier, separately from those fields.
    Historical finalized-release recipes are not replayed by this command.
    """
    import json
    from lib.release.release_transaction import (load_release_profile, is_routine_release_profile,
        validate_pending_release_artifacts, _release_notes_generated_block)
    from lib.packaging.adapter_distribution import scan_security_paths
    from lib.release.release_candidate import file_identity, local_file, run, CandidateError
    errors = current_source_errors(version, root)
    if errors:
        return errors
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
    from lib.release.release_candidate import run, run_packed_smoke, timing_diagnostics, canonical_bytes, local_file
    root = Path.cwd()
    receipt = output / 'release-verification.json'
    errors = current_source_errors(version, root)
    if errors:
        for error in errors:
            print('Release integrity: ' + error, file=sys.stderr)
        return 1
    errors = validate_prepared_release(version, root, output)
    if errors:
        for error in errors:
            print('Release integrity: ' + error, file=sys.stderr)
        return 1
    # Reject invalid admission without changing prior evidence. Once admitted,
    # invalidate a prior pass before running checks that can fail.
    receipt.unlink(missing_ok=True)
    facts = json.loads((output / 'preparation.json').read_text())
    checks = []
    commands = [
        ['python', 'scripts/validate-skills.py'],
        ['python', 'tests/skill/test-skill-validator.py'],
        ['python', 'tests/engineering/packaging/test-adapter-distribution.py'],
        ['python', 'tests/engineering/packaging/test-npm-package-publication.py'],
        ['python', 'scripts/validate-adapters.py', '--version', version, '--adapter-root', str(output)],
        ['python', 'scripts/validate-npm-package.py', '--tarball', str(local_file(output, facts['tarball']))],
    ]
    for command in commands:
        started = time.monotonic()
        print('Release check: ' + ' '.join(command[:2]), flush=True)
        run(command, root)
        checks.append({'command': recorded_command(command, root, output), 'result': 'pass', 'duration_seconds': time.monotonic() - started})
    run_packed_smoke(root, local_file(output, facts['tarball']), output, version)
    checks.append({'command': 'packed CLI version and init codex/claude', 'result': 'pass'})
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
        help="Release tag matching the explicitly selected source package and profile.",
    )
    parser.add_argument(
        "--recorded-source-auto",
        action="store_true",
        help=(
            "For repository CI, validate the current prepared candidate and its source "
            "identities without replaying historical releases."
        ),
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
        if len(args.version) != 1 or args.recorded_source_auto or args.release_output_dir or args.release_commit or args.npm_tarball_root:
            parser.error("prepared-candidate requires one version and no historical-mode options")
        return verify_prepared_release(args.version[0], Path(args.prepared_candidate).resolve())
    if args.recorded_source_auto and (
        args.release_output_dir
        or args.release_commit
        or args.npm_tarball_root
    ):
        parser.error(
            "--recorded-source-auto cannot be combined with "
            "release-output, release-commit, or npm-tarball options"
        )

    root = Path.cwd()
    for version in args.version:
        errors = current_source_errors(version, root, args.release_commit)
        if errors:
            for error in errors:
                print(f"{GATE_NAME}: {error}", file=sys.stderr)
            return 1
        context = (os.environ.get('RIGORLOOP_CI_CANDIDATE')
                   if os.environ.get('RIGORLOOP_CI_WORKSPACE') == str(root) else None)
        if context and args.recorded_source_auto:
            from lib.release.release_candidate import ci_subject
            output = Path(context)
            try:
                ci_subject(output, root)
                errors = validate_prepared_release(version, root, output)
            except (OSError, ValueError, KeyError, TypeError):
                errors = ['current-source: missing or mismatched prepared candidate identity']
            if errors:
                for error in errors:
                    print(f"{GATE_NAME}: {error}", file=sys.stderr)
                return 1
            print(f"{GATE_NAME}: current prepared candidate and verification receipt agree for {version}")
        elif args.release_output_dir and not args.npm_tarball_root:
            status = verify_prepared_release(version, Path(args.release_output_dir).resolve())
            if status:
                return status
        else:
            print(f"{GATE_NAME}: current-source: current qualification requires an explicit prepared output or CI candidate; historical replay is unsupported", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
