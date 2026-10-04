"""Candidate-specific release authority, external observation and durable evidence.

No hosted trigger is registered here. External effects use explicit provider
boundaries; tests replace public services, never authority/identity validators.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import io
import stat
import zipfile
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import time

from lib.release.release_candidate import (CandidateError, canonical_bytes, file_identity, local_file,
    run, verify_candidate, SOURCE_REPOSITORY, script_identity)


class ExecutionError(ValueError):
    pass


class EvidenceUnavailable(ExecutionError):
    """Reporting failed; this does not change an observed public identity."""


class ExternalUnavailable(ExecutionError):
    """An unknown external outcome, not proof of absence."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def environment_identity(environment: dict) -> str:
    selected = {key: environment.get(key) for key in ['id', 'name', 'protection_rules', 'deployment_branch_policy']}
    return hashlib.sha256(canonical_bytes(selected)).hexdigest()


AUTHORITY_FIELDS = frozenset({'run_id', 'artifact_id', 'artifact_digest', 'candidate_id', 'environment', 'artifact_name'})


def validate_release_environment(environment: dict) -> str:
    """Credential/branch scope only; never a second human or waiting gate."""
    try:
        if (environment['name'] != 'release' or type(environment['id']) is not int
            or environment['id'] <= 0 or environment['deployment_branch_policy'] !=
                {'protected_branches': True, 'custom_branch_policies': False}):
            raise ExecutionError('release environment must restrict execution to protected branches')
        rules = environment['protection_rules']
        if not isinstance(rules, list) or any(rule['type'] != 'branch_policy' for rule in rules):
            raise ExecutionError('release environment has an unsupported approval or waiting rule; reconcile setup')
        return environment_identity(environment)
    except (KeyError, TypeError, AttributeError) as exc:
        raise ExecutionError('missing or malformed release environment scope') from exc


def validate_authority(candidate: dict, binding: dict, facts: dict) -> dict:
    """Validate run/source/artifact facts without a reviewer approval response."""
    if candidate.get('inputs', {}).get('ci_only'):
        raise ExecutionError('CI-only candidate cannot authorize publication')
    try:
        if set(binding) != AUTHORITY_FIELDS:
            raise ExecutionError('unknown or missing authority binding field')
        for field in ['run_id', 'artifact_id']:
            if type(binding[field]) is not int or binding[field] <= 0:
                raise ExecutionError('invalid provider identity')
        initiation = candidate.get('initiation')
        if initiation is None:
            raise ExecutionError('candidate lacks workflow-start authority; preserve original and prepare a new authorized run')
        if (not isinstance(initiation, dict) or set(initiation) != {'policy', 'run_id'}
            or initiation['policy'] != 'workflow-start-v1' or type(initiation['run_id']) is not int
            or initiation['run_id'] <= 0):
            raise ExecutionError('unknown or malformed initiation policy')
        if binding['candidate_id'] != candidate['candidate_id']:
            raise ExecutionError('authority candidate mismatch')
        if initiation['run_id'] != binding['run_id']:
            raise ExecutionError('candidate belongs to a different initiating run')
        repo, run_info, artifact, environment, branch = (facts[x] for x in
            ['repository', 'run', 'artifact', 'environment', 'branch'])
        if repo['full_name'] != candidate['repository'] or repo['full_name'] != SOURCE_REPOSITORY:
            raise ExecutionError('authority destination mismatch')
        if (repo['default_branch'] != 'main' or candidate['source_ref'] != 'refs/heads/main'
            or branch['name'] != 'main' or branch['protected'] is not True):
            raise ExecutionError('routine source is not protected main')
        if (type(run_info['id']) is not int or run_info['id'] != binding['run_id']
            or run_info['head_sha'] != candidate['source_commit'] or run_info['head_branch'] != 'main'
            or run_info['event'] != 'push' or run_info['path'] != '.github/workflows/release.yml'
            or run_info['status'] != 'in_progress'):
            raise ExecutionError('stale or mismatched workflow run')
        if type(run_info['run_attempt']) is not int or run_info['run_attempt'] < 1:
            raise ExecutionError('invalid workflow attempt')
        expected_name = 'release-candidate-' + str(binding['run_id'])
        if (binding['artifact_name'] != expected_name or artifact['name'] != expected_name
            or artifact['id'] != binding['artifact_id'] or artifact['expired'] is not False
            or artifact['digest'] != binding['artifact_digest']
            or not re.fullmatch(r'sha256:[0-9a-f]{64}', artifact['digest'])):
            raise ExecutionError('expired or mismatched immutable artifact')
        artifact_run = artifact['workflow_run']
        if (artifact_run['id'] != binding['run_id'] or artifact_run['head_sha'] != candidate['source_commit']
            or artifact_run['repository_id'] != repo['id'] or artifact_run['head_repository_id'] != repo['id']):
            raise ExecutionError('artifact producer mismatch')
        if binding['environment'] != 'release':
            raise ExecutionError('authority environment mismatch')
        config_id = validate_release_environment(environment)
        if candidate['release_environment_identity'] != config_id:
            raise ExecutionError('environment policy changed after preparation')
        return dict(binding, policy='workflow-start-v1', source_commit=candidate['source_commit'],
                    environment_id=environment['id'], environment_identity=config_id,
                    run_attempt=run_info['run_attempt'])
    except (KeyError, TypeError, AttributeError) as exc:
        raise ExecutionError('missing or malformed workflow authority evidence') from exc


MAX_ARTIFACT_BYTES = 256 * 1024 * 1024


def retained_artifact_files(payload: bytes, binding: dict) -> dict[str, bytes]:
    """Bind the physical provider ZIP to its digest and exact sealed contents."""
    if len(payload) > MAX_ARTIFACT_BYTES or 'sha256:' + hashlib.sha256(payload).hexdigest() != binding['artifact_digest']:
        raise ExecutionError('retained artifact bytes differ from retained provider digest')
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            entries = archive.infolist()
            names = [entry.filename for entry in entries]
            if len(names) != len(set(names)) or sum(e.file_size for e in entries) > MAX_ARTIFACT_BYTES:
                raise ExecutionError('duplicate or oversized retained artifact')
            for entry in entries:
                if (not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', entry.filename)
                    or entry.is_dir() or stat.S_ISLNK(entry.external_attr >> 16)):
                    raise ExecutionError('unsafe retained artifact member')
            contents = {name: archive.read(name) for name in names}
        candidate = json.loads(contents['candidate.json'])
        claimed = candidate.pop('candidate_id')
        if claimed != binding['candidate_id'] or hashlib.sha256(canonical_bytes(candidate)).hexdigest() != claimed:
            raise ExecutionError('retained artifact contains a different candidate')
        if set(contents) != set(candidate['files']) | {'candidate.json'}:
            raise ExecutionError('retained artifact inventory differs from sealed candidate')
        for name, identity in candidate['files'].items():
            data = contents[name]
            if identity != {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}:
                raise ExecutionError('retained artifact member differs from sealed identity')
        return contents
    except (zipfile.BadZipFile, KeyError, TypeError, ValueError, RuntimeError) as exc:
        raise ExecutionError('invalid or mismatched retained release artifact') from exc


def materialize_artifact(output: Path, binding: dict, authorities) -> dict:
    """Read-only provider download; this does not establish authority by itself."""
    contents = retained_artifact_files(authorities.artifact_bytes(binding), binding)
    output.mkdir(parents=True, exist_ok=True)
    if output.is_symlink() or any(output.iterdir()):
        raise ExecutionError('artifact extraction requires an empty regular destination')
    for name, data in contents.items():
        (output / name).write_bytes(data)
    return verify_candidate(output, binding['candidate_id'])


def bind_local_artifact(output: Path, binding: dict, authorities):
    contents = retained_artifact_files(authorities.artifact_bytes(binding), binding)
    for name, data in contents.items():
        if local_file(output, name).read_bytes() != data:
            raise ExecutionError('local candidate differs from qualified retained artifact')


def validate_recorded_authority(state: dict, authority: dict):
    """Admit current-policy observations without converting historical grants."""
    recorded = state.get('authority')
    if not isinstance(recorded, dict) or 'policy' not in recorded:
        raise ExecutionError('legacy release attempt requires explicit recovery; preserve original evidence')
    history = state.get('authorities', [])
    if not isinstance(history, list):
        raise ExecutionError('invalid recorded authority history')
    for item in [recorded, *history]:
        if not isinstance(item, dict) or item.get('policy') != 'workflow-start-v1':
            raise ExecutionError('unknown recorded authority policy; preserve original evidence')
        if set(item) != set(authority):
            raise ExecutionError('unknown or missing recorded authority field')
        attempt = item['run_attempt']
        if type(attempt) is not int or not 1 <= attempt <= authority['run_attempt']:
            raise ExecutionError('invalid recorded authority attempt')
        if any(type(item[key]) is not type(value) or item[key] != value
               for key, value in authority.items() if key != 'run_attempt'):
            raise ExecutionError('recorded authority has a different execution basis')


def reconcile_recovery(previous: dict | None, recovery: Path, candidate: dict, authority: dict) -> dict | None:
    if not recovery.exists():
        return previous
    if recovery.is_symlink():
        raise ExecutionError('unsafe recovery observation')
    try:
        recovered = json.loads(recovery.read_bytes())
        # Validate the ordinary state vocabulary and append-only ancestry. These
        # observations preserve history; fresh provider checks still own action.
        read_execution_state((STATE_START + '\n```json\n' + json.dumps(recovered) + '\n```\n' + STATE_END).encode())
        validate_recorded_authority(recovered, authority)
        if (recovered['candidate_id'] != candidate['candidate_id']
            or recovered['authority']['run_id'] != authority['run_id']
            or recovered['authority']['run_attempt'] > authority['run_attempt']):
            raise ExecutionError('recovery observation has a different execution basis')
        if previous:
            old, new = previous['events'], recovered['events']
            if new == old[:len(new)]:
                return previous  # Older local report cannot roll back durable truth.
            if old != new[:len(old)]:
                raise ExecutionError('recovery history diverges from durable observations')
        return recovered
    except (ValueError, KeyError, TypeError) as exc:
        raise ExecutionError('invalid recovery observation; preserve for explicit disposition') from exc


class GitEvidence:
    """Version-scoped existing evidence files on a separate ref, using Git CAS."""
    def __init__(self, remote: str, ref: str, *, source_ref: str = 'refs/heads/main'):
        if not re.fullmatch(r'refs/heads/[a-z0-9][a-z0-9/-]*', ref) or '..' in ref or ref == source_ref:
            raise ExecutionError('evidence ref must be separate from source')
        self.remote, self.ref, self.base = remote, ref, None
        self.temporary = tempfile.TemporaryDirectory(prefix='rigorloop-release-evidence-')
        self.root = Path(self.temporary.name)
        self.env = dict(os.environ)
        # GitHub authentication is subprocess-scoped and never part of command
        # arguments, remote URLs, recorded evidence or diagnostic summaries.
        if remote == f'https://github.com/{SOURCE_REPOSITORY}.git' and os.environ.get('GH_TOKEN'):
            import base64
            count = int(self.env.get('GIT_CONFIG_COUNT', '0'))
            self.env['GIT_CONFIG_COUNT'] = str(count + 1)
            self.env[f'GIT_CONFIG_KEY_{count}'] = 'http.https://github.com/.extraheader'
            self.env[f'GIT_CONFIG_VALUE_{count}'] = 'AUTHORIZATION: basic ' + base64.b64encode(('x-access-token:' + os.environ['GH_TOKEN']).encode()).decode()
        self.git('init', '--quiet')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.temporary.cleanup()

    def git(self, *args, data: bytes | None = None, allowed=(0,)) -> subprocess.CompletedProcess:
        result = subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', *args], cwd=self.root,
            env=self.env, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode not in allowed:
            raise ExecutionError('evidence Git operation failed; no publication is authorized by failed persistence')
        return result

    def refresh(self):
        result = self.git('ls-remote', '--exit-code', self.remote, self.ref, allowed=(0, 2))
        if result.returncode == 2:
            self.base = None
            self.git('read-tree', '--empty')
        else:
            self.git('fetch', '--quiet', self.remote, self.ref)
            self.base = self.git('rev-parse', 'FETCH_HEAD').stdout.decode().strip()
            self.git('read-tree', self.base)
        return self.base

    def read(self, path: str) -> bytes | None:
        self.check_path(path)
        if self.base is None:
            return None
        found = self.git('ls-tree', self.base, '--', path).stdout
        if not found:
            return None
        if not found.startswith(b'100644 blob '):
            raise ExecutionError('evidence reader rejects nonregular content')
        return self.git('show', self.base + ':' + path).stdout

    @staticmethod
    def check_path(path: str):
        p = PurePosixPath(path)
        if p.is_absolute() or '..' in p.parts or '\\' in path or p.as_posix() != path or not (path.startswith('docs/releases/') or re.fullmatch(r'docs/reports/adapter-artifacts/releases/v[0-9]+\.[0-9]+\.[0-9]+\.yaml', path)):
            raise ExecutionError('invalid version-scoped evidence path')

    def save(self, changes: dict[str, bytes]):
        for path, contents in changes.items():
            self.check_path(path)
            identity = self.git('hash-object', '-w', '--stdin', data=contents).stdout.decode().strip()
            self.git('update-index', '--add', '--cacheinfo', '100644', identity, path)
        tree = self.git('write-tree').stdout.decode().strip()
        args = ['-c', 'user.name=RigorLoop Release', '-c', 'user.email=release@users.noreply.github.com',
                'commit-tree', tree]
        if self.base:
            args += ['-p', self.base]
        commit = self.git(*args, data=b'Record observed release outcome\n').stdout.decode().strip()
        result = self.git('push', '--porcelain', '--force-with-lease=' + self.ref + ':' + (self.base or ''),
                         self.remote, commit + ':' + self.ref, allowed=(0, 1))
        if result.returncode:
            raise ExecutionError('evidence compare-and-swap conflict; refresh and reassess before any publication')
        self.base = commit
        return commit


BOUNDARIES = ('tag', 'github', 'npm')
OUTCOMES = frozenset({'pending-publication', 'partial-publication', 'failed-before-publication',
                      'failed-after-publication', 'uncertain-publication', 'completed'})
STATE_START = '<!-- release-execution:start -->'
STATE_END = '<!-- release-execution:end -->'


def public_files(candidate: dict) -> tuple[str, ...]:
    tag = candidate['tag']
    names = [f'rigorloop-adapter-{target}-{tag}.zip' for target in ('codex', 'claude')]
    names += [candidate['tarball'], f'adapter-artifacts-{tag}.json', f'archive-proof-{tag}.json',
              'release-verification.json', 'profile.yaml', 'release-notes.md']
    if len(set(names)) != len(names) or any(name not in candidate['files'] for name in names):
        raise ExecutionError('incomplete qualified publication inventory')
    return tuple(names)


def classify_observation(boundary: str, observed: dict | None, candidate: dict) -> str:
    """None is a provider's definite absence; unavailable responses raise instead."""
    if boundary not in BOUNDARIES:
        raise ExecutionError('unknown publication boundary')
    if observed is None:
        return 'absent'
    try:
        if boundary == 'tag':
            return 'matching' if observed == {'commit': candidate['prepared_commit']} else 'conflict'
        if boundary == 'github':
            if observed['tag'] != candidate['tag'] or observed['draft'] is not False:
                return 'conflict'
            assets = observed['assets']
            if len({a['name'] for a in assets}) != len(assets):
                return 'conflict'
            by_name = {a['name']: a for a in assets}
            for name in public_files(candidate):
                if name in by_name and by_name[name]['sha256'] != candidate['files'][name]['sha256']:
                    return 'conflict'
            return 'matching' if all(name in by_name for name in public_files(candidate)) else 'incomplete'
        expected = candidate['files'][candidate['tarball']]['sha256']
        if (observed['package'] != candidate['package'] or observed['version'] != candidate['version']
            or observed['dist_tag'] != candidate['version'] or observed['sha256'] != expected
            or not observed['integrity'] or not observed['published_at']):
            return 'conflict'
        if not observed['tarball'].startswith('https://registry.npmjs.org/'):
            return 'conflict'
        return 'matching'
    except (KeyError, TypeError, AttributeError):
        raise ExternalUnavailable('incomplete public identity observation')


def safe_observation(boundary: str, observed: dict) -> dict:
    if boundary == 'tag':
        return {'commit': observed['commit']}
    if boundary == 'github':
        return {'tag': observed['tag'], 'assets': [{'name': a['name'], 'sha256': a['sha256']} for a in observed['assets']]}
    return {key: observed[key] for key in ['package', 'version', 'dist_tag', 'sha256', 'integrity', 'tarball', 'published_at']}


def read_execution_state(text: bytes | None) -> dict | None:
    if text is None:
        return None
    try:
        source = text.decode()
        if source.count(STATE_START) != 1 or source.count(STATE_END) != 1:
            raise ExecutionError('existing evidence lacks an unambiguous execution basis; preserve it')
        body = source.split(STATE_START, 1)[1].split(STATE_END, 1)[0].strip()
        state = json.loads(body.removeprefix('```json\n').removesuffix('\n```'))
        if state['status'] not in OUTCOMES or type(state['active']) is not bool or not isinstance(state['events'], list):
            raise ExecutionError('unknown or malformed execution state')
        return state
    except (UnicodeError, ValueError, KeyError, TypeError) as exc:
        raise ExecutionError('invalid existing release evidence; no overwrite') from exc


def render_standing(candidate: dict, state: dict) -> bytes:
    """Existing standing evidence, generated from the same facts as companions."""
    identity = candidate['files'][candidate['tarball']]
    checks = '\n'.join(f"| {c['id']} | {c['result']} | sealed candidate verification |" for c in candidate['checks'])
    events = '\n'.join(f"| {e['at']} | {e['boundary']} | {e['result']} |" for e in state['events'])
    display_status = {'completed': 'published', 'pending-publication': 'not-published', 'partial-publication': 'failed-during-publish', 'failed-before-publication': 'failed-before-publish', 'failed-after-publication': 'failed-after-publish', 'uncertain-publication': 'failed-during-publish'}[state['status']]
    npm = state['observations'].get('npm', {})
    sections = [f"# Release {candidate['tag']}", '## Result',
        f"- Status: {display_status}\n- Routine publish: yes\n- No new decision introduced: yes; reviewed source and candidate authority bound below\n- Provenance: --provenance requested through trusted publishing; public attestation not independently asserted\n- Package: {candidate['package']}\n- Version: {candidate['version']}\n"
        f"- Release type: routine\n- Source commit: {candidate['source_commit']}\n- Source branch: {candidate['source_ref']}\n"
        f"- Prepared commit: {candidate['prepared_commit']}\n- Candidate: {candidate['candidate_id']}\n"
        f"- npm dist-tag: {candidate['channel']}\n- Publish path: trusted-publishing",
        '## Related Lifecycle Evidence',
        f"- Reporting ref: {candidate['evidence_ref']}\n- Release profile: docs/releases/profiles/{candidate['tag']}.yaml\n"
        f"- Public observations: docs/releases/{candidate['tag']}/npm-publication.md\n- Immutable check receipt: release-verification.json",
        '## Version Decision', f"- Version decision: {candidate['inputs']['version_decision']}\n- Change summary: {candidate['inputs']['summary']}",
        '## Routine Publish Boundary', 'Reviewed merged input and exact candidate authority; no new semantic recovery action selected.',
        '## Preflight Gate', '| Check | Result | Evidence |\n| --- | --- | --- |\n' + checks,
        '## Package Contents', f"- Package filename: {candidate['tarball']}\n- Package size: {identity['size']}\n"
        f"- Integrity or checksum: sha256:{identity['sha256']}\n- Included-file review: sealed package-content check\n"
        '- Unexpected inclusions/exclusions: guarded by required package validation\n- Secret-bearing file check: sealed security validation',
        '## Publish Event', f"- Command family: trusted publishing workflow / npm publish --provenance\n- Registry: npm\n- Package reference: {candidate['package']}@{candidate['version']}\n- Published at: {npm.get('published_at', 'not-published')}\n- Dist-tag: {candidate['channel']}\n- Manual fallback reason: not-applicable\n\n" + '| Observed at | Boundary | Result |\n| --- | --- | --- |\n' + events,
        '## Registry Verification', 'Actual public identities and fresh smoke appear in companion evidence; unobserved results remain pending.',
        '## Emergency Deferrals', 'None. This routine executor cannot authorize emergency deferrals or authentication/channel changes.',
        '## Recovery / Rollback Notes', '- Published version overwrite attempted: no\n- Recovery owner: release maintainer\n'
        '- Recovery: inspect public state before retry; preserve successful boundaries. Conflicts require an explicit fix-forward decision.\n'
        '- Failure detail: ' + state.get('failure', 'none'),
        '## Follow-up', 'No unresolved release work.' if state['status'] == 'completed' else 'Release maintainer owns the recorded incomplete boundary; next action is inspect public state and restore the required basis before retry.',
        '## Confidentiality', 'Only public identities and bounded outcomes are recorded; no credentials, raw environments or worker-local paths.',
        '## Recorded execution observations', STATE_START + '\n```json\n' + json.dumps(state, indent=2, sort_keys=True) + '\n```\n' + STATE_END]
    return ('\n\n'.join(sections) + '\n').encode()


def validate_execution_basis(candidate: dict, output: Path, source: Path):
    repository = Path(__file__).resolve().parents[3]
    if (script_identity(repository / 'scripts') != candidate['tool_identity']
        or script_identity(source / 'scripts') != candidate['tool_identity']
        or file_identity(repository / '.github/workflows/release.yml') != candidate['workflow_identity']):
        raise ExecutionError('workflow or check implementation changed after candidate verification')
    for name in ('python', 'node', 'npm'):
        if run([name, '--version'], repository) != candidate['environment'][name]:
            raise ExecutionError('relevant execution environment changed after verification')
    receipt = json.loads((output / 'release-verification.json').read_text())
    if receipt['prepared_commit'] != candidate['prepared_commit'] or receipt['result'] != 'pass' or not receipt['checks'] or any(x['result'] != 'pass' for x in receipt['checks']):
        raise ExecutionError('missing or contradicted required release evidence')
    profile = source / 'docs/releases/profiles' / (candidate['tag'] + '.yaml')
    if file_identity(profile) != candidate['files']['profile.yaml']:
        raise ExecutionError('profile projection differs from prepared source')


def published_metadata_projection(candidate: dict, source: Path) -> bytes:
    from lib.release.release_transaction import _validate_release_yaml_contract, load_release_profile
    from lib.packaging.adapter_distribution import parse_manifest_yaml, _parse_simple_yaml
    path = source / 'docs/releases' / candidate['tag'] / 'release.yaml'
    metadata = _parse_simple_yaml(path.read_text(), path)
    metadata['publication_status'] = 'published'
    manifest = source / 'dist/adapters/manifest.yaml'
    metadata['manifest_version'] = parse_manifest_yaml(manifest.read_text(), manifest).version
    for row in metadata['smoke'].values():
        row.update(result='pass', tool_version='public CLI ' + candidate['version'],
            evidence=f"docs/releases/{candidate['tag']}/npm-publication.md", reason='fresh public smoke observed')
    for key in metadata['validation']:
        metadata['validation'][key] = 'pass'

    def lines(value, indent=0):
        prefix = ' ' * indent
        if isinstance(value, dict):
            result = []
            for key, item in value.items():
                if isinstance(item, (dict, list)):
                    result.append(prefix + key + ':')
                    result.extend(lines(item, indent + 2))
                else:
                    result.append(prefix + key + ': ' + json.dumps(item))
            return result
        result = []
        for item in value:
            if isinstance(item, dict):
                nested = lines(item, indent + 2)
                result.extend([prefix + '- ' + nested[0].lstrip(), *nested[1:]])
            else:
                result.append(prefix + '- ' + json.dumps(item))
        return result

    text = '\n'.join(lines(metadata)) + '\n'
    errors = _validate_release_yaml_contract(text, path, source, load_release_profile(candidate['tag'], root=source),
        require_finalized=True, expected_publication_status='published')
    if errors:
        raise ExecutionError('observed release metadata failed its owning contract')
    return text.encode()


def archive_report(candidate: dict) -> bytes:
    from lib.packaging.adapter_distribution import _expected_adapter_install_roots
    tag, date = candidate['tag'], now()[:10]
    lines = ['schema_version: 1', 'release:', '  version: ' + tag,
        '  source_commit: ' + candidate['prepared_commit'], '  date: "' + date + '"',
        'generator:', f'  command: "python scripts/build-adapters.py --version {tag} --output-dir <release-output-dir>"',
        '  source_skills: "skills/"', '  manifest: "dist/adapters/manifest.yaml"', 'artifacts:']
    for target, root in _expected_adapter_install_roots().items():
        name = f'rigorloop-adapter-{target}-{tag}.zip'
        lines += ['  - adapter: ' + target, '    archive: ' + name,
            '    sha256: ' + candidate['files'][name]['sha256'], '    install_root: ' + root, '    result: pass']
    lines += ['combined_artifact:', '  required: false', f'  archive: rigorloop-adapters-{tag}.tar.gz',
        '  sha256: ""', '  included_adapters:', '    - codex', '    - claude',
        'validation:', '  command: "release_execution: validate_adapter_artifact_metadata with retained full candidate proof"',
        '  result: pass', '  validated_at: "' + date + '"']
    return ('\n'.join(lines) + '\n').encode()


def timing_projection(candidate: dict, state: dict) -> bytes:
    # Existing timing representation, containing only actual available checks.
    # Missing historical phase observations stay diagnostic, never fabricated.
    lines = ['schema_version: release-timing-v1', 'release_tag: ' + candidate['tag'],
        'release_profile: docs/releases/profiles/' + candidate['tag'] + '.yaml',
        'created_at: ' + json.dumps(now()), 'phases: []', 'checks:']
    for index, observation in enumerate(state.get('timings', [])):
        lines.append('  - id: ' + observation['id'] + '-' + str(index))
        for key in ('phase', 'command', 'duration_seconds', 'result'):
            lines.append('    ' + key + ': ' + json.dumps(observation[key]))
    if not state.get('timings'):
        lines[-1] = 'checks: []'
    return ('\n'.join(lines) + '\n').encode()


def execute_candidate(output: Path, binding: dict, *, attempt: int, authorities, publisher, evidence: GitEvidence) -> dict:
    """One protected invocation; publication capability resides in its provider.

    A durable active attempt excludes competing execution. A later provider run
    attempt may recover an interrupted one, after fresh inspection. Writes never
    resume merely because a command raised or a previous response was lost.
    """
    candidate = verify_candidate(output, binding['candidate_id'])
    if evidence.ref != candidate['evidence_ref']:
        raise ExecutionError('evidence destination differs from authority')
    public_files(candidate)
    authority = validate_authority(candidate, binding, authorities.fetch(binding))
    if type(attempt) is not int or attempt < 1 or authority['run_attempt'] != attempt:
        raise ExecutionError('workflow attempt differs from executing invocation')
    bind_local_artifact(output, binding, authorities)
    evidence.refresh()
    path = f"docs/releases/{candidate['tag']}.md"
    previous = read_execution_state(evidence.read(path))
    if previous:
        validate_recorded_authority(previous, authority)
    if previous and previous['candidate_id'] != candidate['candidate_id']:
        raise ExecutionError('different candidate already has release evidence; preserve prior attempt for explicit disposition')
    if previous and previous['active'] and authority['run_attempt'] <= previous['authority']['run_attempt']:
        raise ExecutionError('release attempt is already active; do not compete with publication')
    previous = reconcile_recovery(previous, output / 'observed-outcome.json', candidate, authority)
    state = dict(previous) if previous else {'candidate_id': candidate['candidate_id'], 'status': 'pending-publication',
        'events': [], 'observations': {}}
    state['events'] = list(state['events'])
    state['authorities'] = list(state.get('authorities', []))
    if authority not in state['authorities']:
        state['authorities'].append(authority)
    state.update(active=True, authority=authority)
    # The source bundle is retained input, never a mutable branch checkout.
    with tempfile.TemporaryDirectory(prefix='rigorloop-release-operation-') as temporary:
        source = Path(temporary) / 'source'
        run(['git', 'clone', '--quiet', str(local_file(output, 'source.bundle')), str(source)], output)
        if (run(['git', 'rev-parse', 'HEAD'], source) != candidate['prepared_commit']
            or run(['git', 'rev-parse', 'HEAD^'], source) != candidate['source_commit']):
            raise ExecutionError('source bundle identity mismatch')
        from lib.release.release_transaction import (load_release_profile, is_routine_release_profile, close_release_publication,
            validate_published_release_artifacts)
        validate_execution_basis(candidate, output, source)
        if not is_routine_release_profile(load_release_profile(candidate['tag'], root=source)):
            raise ExecutionError('special handling is outside routine execution')
        companion = f"docs/releases/{candidate['tag']}/npm-publication.md"
        projections = {f"docs/releases/{candidate['tag']}/candidate.json": canonical_bytes(candidate),
            f"docs/releases/{candidate['tag']}/release-verification.json": (output / 'release-verification.json').read_bytes(),
            f"docs/releases/{candidate['tag']}/release.yaml": (source / 'docs/releases' / candidate['tag'] / 'release.yaml').read_bytes(),
            f"docs/releases/{candidate['tag']}/release-notes.md": (output / 'release-notes.md').read_bytes(),
            f"docs/reports/adapter-artifacts/releases/{candidate['tag']}.yaml": archive_report(candidate),
            f"docs/releases/profiles/{candidate['tag']}.yaml": (output / 'profile.yaml').read_bytes(),
            companion: evidence.read(companion) or (source / companion).read_bytes()}

        from lib.packaging.adapter_distribution import validate_adapter_artifact_metadata
        report_path = source / 'docs/reports/adapter-artifacts/releases' / (candidate['tag'] + '.yaml')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_bytes(projections[f"docs/reports/adapter-artifacts/releases/{candidate['tag']}.yaml"])
        report_errors = validate_adapter_artifact_metadata(candidate['tag'], output, metadata_root=report_path.parent, release_commit=candidate['prepared_commit'])
        if report_errors:
            raise ExecutionError('generated archive observation does not satisfy its owning validator')

        def persist():
            from lib.release.release_transaction import validate_release_timing_evidence
            telemetry = timing_projection(candidate, state)
            timing_path = source / 'docs/releases' / candidate['tag'] / 'timing.yaml'
            timing_path.write_bytes(telemetry)
            diagnostic = validate_release_timing_evidence(candidate['tag'], root=source)
            state['timing_diagnostic'] = {'result': 'fail' if diagnostic.errors else 'pass',
                'errors': list(diagnostic.errors), 'warnings': list(diagnostic.warnings),
                'consequence': 'diagnostic only; unavailable phases are not invented'}
            files = dict(projections, **{path: render_standing(candidate, state),
                f"docs/releases/{candidate['tag']}/timing.yaml": telemetry})
            # Keep a recoverable local observation copy even if durable reporting
            # fails. This is separate from immutable qualified artifacts.
            (output / 'observed-outcome.json').write_bytes(canonical_bytes(state))
            try:
                evidence.save(files)
            except ExecutionError as exc:
                raise EvidenceUnavailable('durable reporting unavailable; retained observations must be reconciled') from exc

        def event(boundary, result):
            state['events'].append({'at': now(), 'boundary': boundary, 'result': result,
                'run_id': authority['run_id'], 'run_attempt': authority['run_attempt']})

        persist()  # Required pending and authority facts precede every publication.
        boundary = 'observation'
        try:
            for boundary in BOUNDARIES:
                # Revalidate exact bytes and provider authority at actual writes.
                verify_candidate(output, binding['candidate_id'])
                validate_execution_basis(candidate, output, source)
                current_authority = validate_authority(candidate, binding, authorities.fetch(binding))
                if current_authority != authority:
                    raise ExecutionError('workflow authority changed during executing invocation')
                observed = publisher.observe(boundary, candidate)
                disposition = classify_observation(boundary, observed, candidate)
                if disposition == 'conflict':
                    state.setdefault('conflicts', {})[boundary] = safe_observation(boundary, observed)
                    raise ExecutionError('conflicting public identity at ' + boundary)
                if disposition in {'absent', 'incomplete'}:
                    event(boundary, 'write-intent')
                    state['uncertain_write'] = boundary
                    persist()
                    started = time.monotonic()
                    try:
                        publisher.publish(boundary, candidate, output, source)
                    except (ExecutionError, CandidateError, OSError, subprocess.SubprocessError):
                        # Lost responses may already have committed. Observation,
                        # not the command result, determines whether to continue.
                        event(boundary, 'write-response-unavailable')
                    state.setdefault('timings', []).append({'id': boundary + '_publication',
                        'phase': 'publication_wait', 'duration_seconds': time.monotonic() - started,
                        'result': 'pending', 'command': boundary + ' publication of qualified identity'})
                    observed = None
                    # npm scans accepted uploads before making them installable.
                    observation_attempts = 121 if boundary == 'npm' else 6
                    for observation_attempt in range(observation_attempts):
                        try:
                            observed = publisher.observe(boundary, candidate)
                            disposition = classify_observation(boundary, observed, candidate)
                        except ExternalUnavailable:
                            disposition = 'unknown'
                        if disposition in {'matching', 'conflict'}:
                            break
                        if observation_attempt < observation_attempts - 1:
                            publisher.wait_for_visibility(observation_attempt)
                    if disposition != 'matching':
                        event(boundary, disposition)
                        raise ExternalUnavailable('public outcome is not confirmed at ' + boundary)
                # Only selected public facts enter evidence, never raw responses.
                state['observations'][boundary] = safe_observation(boundary, observed)
                if state.get('uncertain_write') == boundary:
                    state.pop('uncertain_write')
                if state.get('timings') and state['timings'][-1]['id'] == boundary + '_publication':
                    state['timings'][-1]['result'] = 'pass'
                state['status'] = 'partial-publication'
                event(boundary, 'matching')
                persist()
            boundary = 'public-smoke'
            started = time.monotonic()
            result = close_release_publication(candidate['tag'], root=source, provider=publisher)
            state.setdefault('timings', []).append({'id': 'public_smoke', 'phase': 'public_closeout',
                'duration_seconds': time.monotonic() - started, 'command': 'fresh public version and target init smoke', 'result': 'fail' if result.errors else 'pass'})
            if result.errors or validate_published_release_artifacts(candidate['tag'], root=source):
                raise ExternalUnavailable('fresh public verification failed')
            publisher.verify_smoke_identity(candidate, output)
            # Fresh smoke does not freeze mutable dist-tags or public assets.
            for checked_boundary in BOUNDARIES:
                final = publisher.observe(checked_boundary, candidate)
                if classify_observation(checked_boundary, final, candidate) != 'matching':
                    raise ExternalUnavailable('public identity changed during closeout')
                state['observations'][checked_boundary] = safe_observation(checked_boundary, final)
            projections[companion] = (source / companion).read_bytes()
            projections[f"docs/releases/{candidate['tag']}/release.yaml"] = published_metadata_projection(candidate, source)
            event(boundary, 'pass')
            state.update(status='completed', active=False, failure='none')
            persist()
            return state
        except (ExecutionError, CandidateError, OSError, ValueError, subprocess.SubprocessError) as exc:
            if isinstance(exc, EvidenceUnavailable):
                boundary = 'reporting'
            state.update(status=('uncertain-publication' if state.get('uncertain_write') else 'failed-after-publication' if state['observations'] else 'failed-before-publication'),
                active=False, failure='Required ' + boundary + ' outcome unavailable or conflicting; inspect before recovery.')
            event(boundary, 'incomplete')
            persist()
            raise ExecutionError(state['failure']) from exc
