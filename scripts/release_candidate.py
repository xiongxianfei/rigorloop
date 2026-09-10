"""Repository-owned immutable Release candidate construction.

Policy: docs/design/release/release.md. No publication or remote writes here.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any

from release_transaction import (
    EXPECTED_NPM_PACKAGE, ROUTINE_TARGETS, REQUIRED_EVIDENCE_FIELDS,
    REQUIRED_PUBLICATION_FIELDS, REQUIRED_VALIDATION_FIELDS,
    load_release_profile, validate_release_timing_evidence, ReleaseProfileError,
)

VERSION_DECISIONS = frozenset({'patch', 'minor', 'major'})
CANDIDATE_CHECKS = frozenset({'profile', 'preflight', 'release-integrity'})
SOURCE_REPOSITORY = 'xiongxianfei/rigorloop'
STABLE_VERSION = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z')
SHA = re.compile(r'[0-9a-f]{40}\Z')


class CandidateError(ValueError):
    """An actionable exception that must precede any publication approval."""


def canonical_bytes(data: Any) -> bytes:
    return (json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


def file_identity(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise CandidateError('artifact path is missing or a symlink')
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'size': path.stat().st_size}


def local_file(root: Path, name: str) -> Path:
    if not isinstance(name, str):
        raise CandidateError('invalid artifact path')
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name or p.as_posix() != name:
        raise CandidateError('invalid artifact path')
    path = root.joinpath(*p.parts)
    if any(parent.is_symlink() for parent in [path, *path.parents] if parent != root.parent):
        raise CandidateError('artifact path traverses symlink')
    if not path.resolve().is_relative_to(root.resolve()):
        raise CandidateError('artifact path escapes candidate')
    return path


def version_tuple(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not STABLE_VERSION.fullmatch(value):
        raise CandidateError('supported routine release requires stable semantic version')
    return tuple(map(int, value.split('.')))


def derive_release_inputs(root: Path, published_version: str) -> dict:
    package = json.loads((root / 'packages/rigorloop/package.json').read_text())
    if package.get('name') != EXPECTED_NPM_PACKAGE:
        raise CandidateError('unsupported package')
    version = package.get('version')
    current, previous = version_tuple(version), version_tuple(published_version)
    if current == previous:
        return {'status': 'already-published', 'version': version}
    if current < previous:
        raise CandidateError('source version is older than public version')
    tag = 'v' + version
    path = root / 'docs/releases' / f'{tag}.md'
    if not path.is_file():
        raise CandidateError('missing reviewed version decision in standing release record')
    text = path.read_text()
    section = re.search(r'^## Version [Dd]ecision\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not section:
        raise CandidateError('missing reviewed version decision section')
    decision = re.findall(r'^- Version decision: (\S+)\s*$', section[1], re.M)
    summary = re.findall(r'^- Change summary: (.+)$', section[1], re.M)
    if len(decision) != 1 or decision[0] not in VERSION_DECISIONS:
        raise CandidateError('unknown or ambiguous reviewed version decision')
    if len(summary) != 1 or any(x in summary[0].lower() for x in ['pending', 'todo', 'tbd']):
        raise CandidateError('missing reviewed version decision rationale/change summary')
    increment = 'major' if current[0] != previous[0] else 'minor' if current[1] != previous[1] else 'patch'
    if increment != decision[0]:
        raise CandidateError('version decision does not match reviewed increment')
    return {'status': 'prepare', 'version': version, 'tag': tag,
            'version_decision': decision[0], 'summary': summary[0],
            'decision_source': path.relative_to(root).as_posix(),
            'decision_identity': file_identity(path)}


def profile_text(tag: str) -> str:
    if not tag.startswith('v'):
        raise CandidateError('invalid release tag')
    version_tuple(tag[1:])
    lines = ['schema_version: release-profile-v1', 'release_kind: routine',
             f'release_tag: {tag}', f'package_version: {tag[1:]}', 'npm_dist_tag: latest',
             f'npm_package: "{EXPECTED_NPM_PACKAGE}"', 'targets:']
    lines += ['  - ' + t for t in ROUTINE_TARGETS]
    lines += ['adapter_artifacts:', '  required: true',
              f'  metadata_file: adapter-artifacts-{tag}.json', f'  archive_version: {tag}']
    for name, fields, value in [('publication', REQUIRED_PUBLICATION_FIELDS, 'true'),
                                 ('evidence', REQUIRED_EVIDENCE_FIELDS, 'required'),
                                 ('validation', REQUIRED_VALIDATION_FIELDS, 'true')]:
        lines += [name + ':'] + [f'  {field}: {value}' for field in fields]
    return '\n'.join(lines) + '\n'


def timing_diagnostics(root: Path, tag: str) -> list[str]:
    # Invalid policy input is not a telemetry failure. Validate it first.
    try:
        load_release_profile(tag, root=root)
    except ReleaseProfileError as exc:
        raise CandidateError('invalid release profile for timing diagnostics') from exc
    result = validate_release_timing_evidence(tag, root=root)
    return list(result.errors) + list(result.warnings)


def _validate_binding(data: dict) -> None:
    if type(data.get('schema_version')) is not int or data.get('schema_version') != 1:
        raise CandidateError('unknown candidate schema')
    for field in ['source_commit', 'prepared_commit']:
        if not isinstance(data.get(field), str) or not SHA.fullmatch(data[field]):
            raise CandidateError('invalid source identity')
    version_tuple(data.get('version'))
    if data.get('tag') != 'v' + data['version'] or data.get('package') != EXPECTED_NPM_PACKAGE:
        raise CandidateError('invalid release identity')
    if data.get('repository') != SOURCE_REPOSITORY or data.get('channel') != 'latest' or data.get('publication_path') != 'trusted-publishing':
        raise CandidateError('unsupported publication identity')
    source_ref = data.get('source_ref', '')
    if not re.fullmatch(r'refs/heads/[a-z0-9][a-z0-9/-]*', source_ref):
        raise CandidateError('invalid source ref')
    ref = data.get('evidence_ref', '')
    if not re.fullmatch(r'refs/heads/[a-z0-9][a-z0-9/-]*', ref) or '..' in ref or ref.endswith('/') or ref == source_ref:
        raise CandidateError('invalid evidence ref')
    files = data.get('files')
    if not isinstance(files, dict) or not files:
        raise CandidateError('missing artifact identities')
    for identity in files.values():
        if (not isinstance(identity, dict) or set(identity) != {'sha256', 'size'}
                or not isinstance(identity.get('sha256'), str)
                or not re.fullmatch(r'[0-9a-f]{64}', identity['sha256'])
                or type(identity.get('size')) is not int or identity['size'] < 0):
            raise CandidateError('invalid artifact identity')
    checks = data.get('checks')
    if not isinstance(checks, list) or not checks:
        raise CandidateError('missing checks')
    seen = set()
    for check in checks:
        if not isinstance(check, dict) or check.get('result') != 'pass' or check.get('id') not in CANDIDATE_CHECKS or check['id'] in seen:
            raise CandidateError('failed, unknown or duplicate check')
        seen.add(check['id'])
    if seen != CANDIDATE_CHECKS:
        raise CandidateError('missing required candidate checks')


def seal_candidate(root: Path, data: dict) -> dict:
    data = dict(data, schema_version=1)
    _validate_binding(data)
    if not isinstance(data.get('files'), dict) or not data['files']:
        raise CandidateError('missing artifact identities')
    for name, expected in data['files'].items():
        if name == 'candidate.json' or file_identity(local_file(root, name)) != expected:
            raise CandidateError('artifact identity differs from build evidence')
    if 'candidate_id' in data:
        raise CandidateError('cannot reseal an identified candidate')
    data['candidate_id'] = hashlib.sha256(canonical_bytes(data)).hexdigest()
    (root / 'candidate.json').write_bytes(canonical_bytes(data))
    return data


def verify_candidate(root: Path, expected_id: str) -> dict:
    data = json.loads(local_file(root, 'candidate.json').read_bytes())
    actual_id = data.pop('candidate_id', None)
    if actual_id != expected_id or hashlib.sha256(canonical_bytes(data)).hexdigest() != expected_id:
        raise CandidateError('candidate identity changed')
    _validate_binding(data)
    for name, expected in data['files'].items():
        if file_identity(local_file(root, name)) != expected:
            raise CandidateError('artifact identity changed')
    data['candidate_id'] = actual_id
    return data


def run(argv: list[str], cwd: Path, *, env: dict | None = None, timeout: int = 1800) -> str:
    # Commands are fixed argument arrays; never expose subprocess stderr/environment.
    result = subprocess.run(argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=timeout)
    if len(argv) > 1 and Path(argv[1]).name.startswith('test-') and re.search(r'Ran 0 tests', result.stdout + result.stderr):
        raise CandidateError('required test command discovered zero tests')
    if result.returncode:
        # Retain diagnostic output locally with private permissions; never dump
        # potentially sensitive tool output into an approval or public report.
        fd, log = tempfile.mkstemp(prefix='rigorloop-release-check-', suffix='.log')
        with os.fdopen(fd, 'w') as handle:
            handle.write(result.stdout + '\n' + result.stderr)
        raise CandidateError(f'{Path(argv[0]).name} {Path(argv[1]).name if len(argv) > 1 else ""} command failed ({result.returncode}); private diagnostic log: {log}')
    return result.stdout.rstrip()


def write_archive_metadata(root: Path, output: Path, tag: str, commit: str, package_root: Path) -> list[Path]:
    """Reuse archive facts; a separate immutable proof document avoids a self-hash."""
    from adapter_distribution import _local_release_candidate_metadata
    metadata = _local_release_candidate_metadata(tag, output)
    # The archived proof is an actual prepublication observation, not public success.
    proof = {'source_commit': commit, 'release_tag': tag, 'artifacts': metadata['artifacts'],
             'validation': {'command': 'python scripts/validate-adapters.py --version ' + tag,
                            'result': 'pass'}}
    proof_path = output / f'archive-proof-{tag}.json'
    proof_path.write_bytes(canonical_bytes(proof))
    metadata['release']['source_commit'] = commit
    metadata['release']['published_at'] = 'pending-publication'
    metadata['metadata'] = {
        'url': f'https://github.com/{SOURCE_REPOSITORY}/releases/download/{tag}/{proof_path.name}',
        'sha256': file_identity(proof_path)['sha256'],
    }
    metadata_dir = package_root / 'dist/metadata'
    metadata_dir.mkdir(parents=True, exist_ok=True)
    path = metadata_dir / f'adapter-artifacts-{tag}.json'
    path.write_bytes(canonical_bytes(metadata))
    public = output / path.name
    shutil.copyfile(path, public)
    index_path = metadata_dir / 'releases.json'
    index = json.loads(index_path.read_text()) if index_path.exists() else {'schema_version': 1, 'releases': {}}
    index['releases'][tag] = {'source_repository': SOURCE_REPOSITORY, 'release_tag': tag,
                             'bundled_metadata': path.name,
                             'bundled_metadata_sha256': file_identity(path)['sha256']}
    index_path.write_bytes(canonical_bytes(index))
    return [proof_path, public]


def script_identity(directory: Path) -> str:
    return hashlib.sha256(canonical_bytes({p.name: file_identity(p) for p in sorted(p for p in directory.iterdir() if p.is_file() and p.suffix in {'.py', '.sh'})})).hexdigest()


def prepare_candidate(source: Path, source_commit: str, merged_ref: str, published_version: str,
                      output: Path, *, evidence_ref: str = 'refs/heads/release-evidence') -> dict:
    """Build from an exact merged input in isolation; leave no publication capability."""
    from release_transaction import prepare_release, release_preflight
    if not re.fullmatch(r'refs/(heads|remotes/origin)/[a-z0-9][a-z0-9/-]*', merged_ref):
        raise CandidateError('invalid merged source ref')
    source_ref = merged_ref.replace('refs/remotes/origin/', 'refs/heads/')
    if evidence_ref == source_ref:
        raise CandidateError('evidence ref must be separate from source')
    if not SHA.fullmatch(source_commit):
        raise CandidateError('source identity must be an exact commit')
    if run(['git', 'rev-parse', '--verify', merged_ref + '^{commit}'], source) != source_commit:
        raise CandidateError('source must match selected merged branch identity')
    if output.exists() and any(output.iterdir()):
        # Never erase an earlier candidate or silently update its identity.
        raise CandidateError('candidate output must be empty; retain earlier candidate for inspection')
    output = output.resolve()
    if output.is_relative_to(source.resolve()):
        raise CandidateError('candidate output must be outside source checkout')
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='rigorloop-candidate-') as temporary:
        root = Path(temporary) / 'source'
        run(['git', 'clone', '--no-hardlinks', '--no-checkout', '--quiet', str(source.resolve()), str(root)], source)
        run(['git', 'checkout', '--detach', source_commit], root)
        if script_identity(root / 'scripts') != LOADED_SCRIPT_IDENTITY or script_identity(Path(__file__).parent) != LOADED_SCRIPT_IDENTITY:
            raise CandidateError('candidate builder does not match reviewed source implementation')
        inputs = derive_release_inputs(root, published_version)
        if inputs['status'] == 'already-published':
            return inputs
        tag = inputs['tag']
        profile = root / 'docs/releases/profiles' / f'{tag}.yaml'
        if profile.exists():
            # A supplied stricter or special profile is never overwritten into eligibility.
            existing = load_release_profile(tag, root=root)
            if existing.release_kind != 'routine' or existing.targets != ROUTINE_TARGETS:
                raise CandidateError('unsupported special release profile')
        else:
            profile.parent.mkdir(parents=True, exist_ok=True)
            profile.write_text(profile_text(tag))
        prepared = prepare_release(tag, root=root, approval_driven=True)
        notes = root / 'docs/releases' / tag / 'release-notes.md'
        original_notes = run(['git', 'ls-tree', source_commit, '--', str(notes.relative_to(root))], root)
        if not original_notes:
            notes.write_text(notes.read_text() + '\n## Changes\n\n' + inputs['summary'] + '\n')
        allowed = {
            f'docs/releases/profiles/{tag}.yaml', f'docs/releases/{tag}.md',
            *(f'docs/releases/{tag}/{name}' for name in
              ['release.yaml', 'release-notes.md', 'npm-publication.md', 'timing.yaml']),
            f'docs/reports/adapter-artifacts/releases/{tag}.yaml',
            'packages/rigorloop/package.json', 'packages/rigorloop/README.md',
            'packages/rigorloop/dist/metadata/releases.json',
            'tests/fixtures/release-transaction/current-version.json',
        }
        changed = set(prepared.changed_paths) | {profile.relative_to(root).as_posix(), notes.relative_to(root).as_posix()}
        if not changed.issubset(allowed):
            raise CandidateError('unexpected generated source path')
        allowed = {name for name in allowed if (root / name).exists()}
        run(['git', 'add', '--', *sorted(allowed)], root)
        staged = run(['git', 'diff', '--cached', '--name-only'], root).splitlines()
        pending = run(['git', 'status', '--porcelain', '--untracked-files=all'], root).splitlines()
        if any(row[3:] not in allowed or row[:2] == '??' or row[1] != ' ' for row in pending):
            raise CandidateError('unexpected uncommitted source edit')
        if not set(staged).issubset(allowed):
            raise CandidateError('unexpected prepared source edit')
        env = dict(os.environ)
        stamp = run(['git', 'show', '-s', '--format=%cI', source_commit], root)
        env.update({'GIT_AUTHOR_NAME': 'RigorLoop Release', 'GIT_COMMITTER_NAME': 'RigorLoop Release',
                    'GIT_AUTHOR_EMAIL': 'release@users.noreply.github.com',
                    'GIT_COMMITTER_EMAIL': 'release@users.noreply.github.com',
                    'GIT_AUTHOR_DATE': stamp, 'GIT_COMMITTER_DATE': stamp})
        run(['git', '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null',
             'commit', '--allow-empty', '-m', 'Prepare ' + tag], root, env=env)
        commit = run(['git', 'rev-parse', 'HEAD'], root)
        checks = []

        def checked(key: str, command: list[str]):
            import sys
            print('Candidate check: ' + key, file=sys.stderr, flush=True)
            started = time.monotonic()
            result = run(command, root)
            checks.append({'id': key, 'command': ' '.join(command[:2]), 'result': 'pass',
                           'duration_seconds': round(time.monotonic() - started, 3)})
            return result

        load_release_profile(tag, root=root)
        checks.append({'id': 'profile', 'result': 'pass'})
        preflight = release_preflight(tag, root=root, changed_files=tuple(staged), check_remote=False)
        if preflight.errors:
            raise CandidateError('candidate preflight failed: ' + '; '.join(preflight.errors))
        checks.append({'id': 'preflight', 'result': 'pass'})
        run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], root / 'packages/rigorloop')
        run(['python', 'scripts/build-adapters.py', '--version', tag, '--output-dir', str(output)], root)
        run(['python', 'scripts/validate-adapters.py', '--version', tag, '--adapter-root', str(output)], root)
        package = root / 'packages/rigorloop'
        write_archive_metadata(root, output, tag, commit, package)
        overlay_paths = ['packages/rigorloop/dist/metadata/' + 'adapter-artifacts-' + tag + '.json',
                         'packages/rigorloop/dist/metadata/releases.json']
        actual_overlay = run(['git', 'status', '--porcelain', '--untracked-files=all'], root)
        for row in actual_overlay.splitlines():
            if row[3:] not in overlay_paths:
                raise CandidateError('unexpected build overlay edit')
        packed = json.loads(run(['npm', 'pack', '--json', '--ignore-scripts', '--pack-destination', str(output)], package))
        tarball = local_file(output, packed[0]['filename'])
        # Full composition belongs to the retained release verifier. Inputs are
        # bound before checking; the final candidate adds its actual result.
        (output / 'preparation.json').write_bytes(canonical_bytes({
            'tag': tag, 'source_commit': source_commit, 'prepared_commit': commit,
            'tarball': tarball.name,
            'files': {p.name: file_identity(p) for p in sorted(output.iterdir()) if p.is_file()}}))
        checked('release-integrity', ['bash', 'scripts/release-verify.sh', tag, '--prepared-candidate', str(output)])
        run(['git', 'bundle', 'create', str(output / 'source.bundle'), 'HEAD'], root)
        shutil.copyfile(profile, output / 'profile.yaml')
        shutil.copyfile(notes, output / 'release-notes.md')
        (output / 'build-overlay.json').write_bytes(canonical_bytes({
            name: file_identity(root / name) for name in overlay_paths}))
        files = {p.name: file_identity(p) for p in sorted(output.iterdir()) if p.is_file()}
        data = {'source_commit': source_commit, 'prepared_commit': commit, 'source_ref': source_ref,
                'version': inputs['version'], 'tag': tag, 'package': EXPECTED_NPM_PACKAGE,
                'repository': SOURCE_REPOSITORY, 'channel': 'latest', 'publication_path': 'trusted-publishing',
                'evidence_ref': evidence_ref, 'inputs': inputs, 'source_diff': sorted(staged),
                'files': files, 'tarball': tarball.name, 'checks': checks,
                'diagnostics': timing_diagnostics(root, tag),
                'workflow_identity': file_identity(root / '.github/workflows/release.yml'),
                'tool_identity': LOADED_SCRIPT_IDENTITY,
                'source_timestamp': stamp,
                'environment': {name: run([name, '--version'], root) for name in ['python', 'node', 'npm']}}
        if script_identity(Path(__file__).parent) != LOADED_SCRIPT_IDENTITY:
            raise CandidateError('candidate builder changed during execution')
        return seal_candidate(output, data)


def run_packed_smoke(root: Path, tarball: Path, output: Path, tag: str) -> None:
    """Install the actual packed CLI; use local archives for safe filesystem proof."""
    with tempfile.TemporaryDirectory(prefix='rigorloop-packed-') as temporary:
        install = Path(temporary)
        run(['npm', 'install', '--ignore-scripts', '--no-audit', '--no-fund',
             '--prefix', str(install), str(tarball)], root)
        cli = install / 'node_modules/@xiongxianfei/rigorloop/dist/bin/rigorloop.js'
        if run(['node', str(cli), 'version'], root) != EXPECTED_NPM_PACKAGE + ' ' + tag[1:]:
            raise CandidateError('packed CLI version mismatch')
        for target in ROUTINE_TARGETS:
            target_root = install / ('target-' + target)
            target_root.mkdir()
            run(['node', str(cli), 'init', target, '--from-archive',
                 str(output / f'rigorloop-adapter-{target}-{tag}.zip')], target_root)


LOADED_SCRIPT_IDENTITY = script_identity(Path(__file__).parent)
