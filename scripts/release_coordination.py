"""Thin repository coordinator for the approved one-environment Release path."""
from __future__ import annotations
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

from release_candidate import (SOURCE_REPOSITORY, CandidateError, canonical_bytes, derive_release_inputs,
    prepare_candidate, seal_candidate, run, version_tuple)
from release_execution import (ExecutionError, ExternalUnavailable, GitEvidence, environment_identity,
    execute_candidate, materialize_artifact, read_execution_state, retained_artifact_files,
    classify_observation, BOUNDARIES)
from release_provider import GitHubApprovals, NetworkPublisher, github_json, public_bytes

ENVIRONMENT = 'release'
TRUSTED_PUBLISHER = 'github:' + SOURCE_REPOSITORY + ':release.yml:' + ENVIRONMENT


def validate_setup(facts: dict, settings: dict, event: dict) -> dict:
    try:
        if set(settings) != {'evidence_ref', 'trusted_publisher'} or settings['trusted_publisher'] != TRUSTED_PUBLISHER:
            raise ExecutionError('missing established trusted-publisher configuration intent')
        repo, workflow, branch, environment = (facts[k] for k in ('repository', 'run', 'branch', 'environment'))
        if (repo['full_name'] != SOURCE_REPOSITORY or event['source_ref'] != 'refs/heads/' + repo['default_branch']
            or branch['name'] != repo['default_branch'] or branch['protected'] is not True
            or workflow['id'] != event['run_id'] or workflow['head_sha'] != event['source_commit']
            or workflow['head_branch'] != repo['default_branch'] or workflow['event'] != 'push'
            or workflow['path'] != '.github/workflows/release.yml' or workflow['run_attempt'] != event['attempt']
            or workflow['status'] != 'in_progress'):
            raise ExecutionError('unprotected or mismatched reviewed workflow source')
        ref = settings['evidence_ref']
        if not re.fullmatch(r'refs/heads/[a-z0-9][a-z0-9/-]*', ref) or '..' in ref or ref.endswith('/') or ref == event['source_ref']:
            raise ExecutionError('configure a separate valid release evidence ref')
        if (environment['name'] != ENVIRONMENT or environment['deployment_branch_policy'] !=
            {'protected_branches': True, 'custom_branch_policies': False}):
            raise ExecutionError('release environment must require protected branches')
        rules = [r for r in environment['protection_rules'] if r['type'] == 'required_reviewers']
        if len(rules) != 1 or not rules[0]['reviewers'] or any(r['type'] != 'User' for r in rules[0]['reviewers']):
            raise ExecutionError('configure authorized individual release reviewers')
        return {'environment': ENVIRONMENT, 'evidence_ref': ref,
            'approval_environment_identity': environment_identity(environment),
            'npm_configuration': 'declared; runtime authorization required'}
    except (KeyError, TypeError, AttributeError) as exc:
        raise ExecutionError('required release setup is missing or unavailable') from exc


def runtime_credentials(environment: dict):
    if environment.get('GITHUB_ACTIONS') != 'true' or not all(environment.get(k) for k in
        ('GH_TOKEN', 'ACTIONS_ID_TOKEN_REQUEST_URL', 'ACTIONS_ID_TOKEN_REQUEST_TOKEN')):
        raise ExecutionError('protected runtime GitHub/OIDC credentials unavailable; no publication attempted')


def validate_workflow(root: Path) -> list[str]:
    """Parse actual YAML using the repository's existing YAML dependency."""
    try:
        module_root = Path(__file__).resolve().parents[1] / 'packages/rigorloop'
        script = "const fs=require('fs'), YAML=require('yaml'); console.log(JSON.stringify(YAML.parse(fs.readFileSync(process.argv[1],'utf8'),{uniqueKeys:true})))"
        result = subprocess.run(['node', '-e', script, str((root / '.github/workflows/release.yml').resolve())],
            cwd=module_root, text=True, capture_output=True)
        if result.returncode: return ['release workflow YAML could not be parsed with the owning dependency']
        data = json.loads(result.stdout)
        errors = []
        if data.get('on') != {'push': {'branches': ['main']}}: errors.append('release workflow must have only the supported default-branch push trigger')
        if data.get('permissions') != {'contents': 'read'}: errors.append('release workflow defaults must be read-only')
        if data.get('concurrency') != {'group': 'rigorloop-release', 'cancel-in-progress': False}: errors.append('release execution must serialize without cancelling active writes')
        jobs = data.get('jobs', {})
        if set(jobs) != {'prepare', 'execute'}: errors.append('release workflow has unknown or missing jobs')
        prepare, execute = jobs.get('prepare', {}), jobs.get('execute', {})
        if 'environment' in prepare or prepare.get('permissions') != {'contents': 'read', 'actions': 'read'}:
            errors.append('preparation must be read-only and precede approval')
        if execute.get('needs') != 'prepare' or execute.get('environment') != ENVIRONMENT:
            errors.append('exactly one protected executor must depend on preparation')
        if execute.get('permissions') != {'contents': 'write', 'actions': 'read', 'deployments': 'read', 'id-token': 'write'}:
            errors.append('executor permissions must match the approved release operation')
        for name, job in jobs.items():
            if job.get('runs-on') != 'ubuntu-latest' or job.get('timeout-minutes') != 60:
                errors.append('unsupported release runner or timeout')
            steps = job.get('steps', [])
            commands = [s['run'] for s in steps if 'run' in s]
            if any('if' in step for step in steps if 'run' in step):
                errors.append('required coordinator/dependency steps cannot be skipped')
            allowed_actions = {'actions/checkout@v4', 'actions/setup-python@v5', 'actions/setup-node@v4', 'actions/upload-artifact@v4'}
            if any(step.get('uses') not in allowed_actions for step in steps if 'uses' in step):
                errors.append('unsupported action in privileged release workflow')
            for action, configuration in [('actions/setup-python@v5', {'python-version': '3.12'}), ('actions/setup-node@v4', {'node-version': 24})]:
                selected = [step for step in steps if step.get('uses') == action]
                if len(selected) != 1 or selected[0].get('with') != configuration:
                    errors.append('preparation/execution toolchain configuration must agree')
            expected = 'python scripts/release-coordinator.py ' + name
            if commands != ['npm ci --prefix packages/rigorloop --ignore-scripts --no-audit --no-fund', expected]: errors.append('release workflow must delegate to coordinator and release-verify.sh; no direct validate-release.py or publication bypass')
            checkouts = [s for s in steps if s.get('uses') == 'actions/checkout@v4']
            if len(checkouts) != 1 or checkouts[0].get('with') != {'ref': '${{ github.sha }}', 'fetch-depth': 0, 'persist-credentials': False}:
                errors.append('release checkout must bind exact source and avoid persisted credentials')
        uploads = [s for s in prepare.get('steps', []) if s.get('uses') == 'actions/upload-artifact@v4']
        if len(uploads) != 1 or uploads[0].get('with') != {
            'name': 'release-candidate-${{ github.run_id }}', 'path': '${{ runner.temp }}/release-candidate/*',
            'if-no-files-found': 'error', 'retention-days': 30, 'overwrite': False, 'compression-level': 0}:
            errors.append('candidate retention must be immutable with explicit expiry and complete inventory')
        if uploads and uploads[0].get('if') != "steps.candidate.outputs.ready == 'true' && github.run_attempt == 1":
            errors.append('retry cannot replace the approved candidate artifact')
        if execute.get('if') != "needs.prepare.outputs.ready == 'true'": errors.append('failed or no-op preparation cannot request approval')
        recovery = [s for s in execute.get('steps', []) if s.get('uses') == 'actions/upload-artifact@v4']
        if (len(recovery) != 1 or recovery[0].get('if') != "always() && steps.operation.outcome != 'skipped'"
            or recovery[0].get('with') != {'name': 'release-observation-${{ github.run_id }}-${{ github.run_attempt }}',
                'path': '${{ runner.temp }}/release-candidate/observed-outcome.json', 'if-no-files-found': 'warn', 'retention-days': 30, 'overwrite': False}):
            errors.append('executor must retain recovery observations after failure')
        return errors
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return ['missing or malformed release workflow composition']


class HostedServices:
    def __init__(self):
        self.approvals = GitHubApprovals()
        self.publisher = NetworkPublisher()

    def setup(self, event):
        base = 'repos/' + SOURCE_REPOSITORY
        repo = github_json(base)
        return {'repository': repo, 'run': github_json(f"{base}/actions/runs/{event['run_id']}"),
            'branch': github_json(base + '/branches/' + repo['default_branch']),
            'environment': github_json(base + '/environments/' + ENVIRONMENT)}

    def latest(self):
        data = json.loads(public_bytes('https://registry.npmjs.org/@xiongxianfei%2Frigorloop', 'https://registry.npmjs.org/'))
        version = data['dist-tags']['latest']; version_tuple(version)
        return version

    def artifacts(self, event):
        base = f"repos/{SOURCE_REPOSITORY}/actions/runs/{event['run_id']}/artifacts"
        result = []
        for page in range(1, 11):
            data = github_json(base + '?per_page=100&page=' + str(page))
            if not data or not isinstance(data.get('artifacts'), list): raise ExternalUnavailable('artifact inventory unavailable')
            result.extend(data['artifacts'])
            if len(data['artifacts']) < 100: return result
        raise ExternalUnavailable('artifact inventory exceeds supported bounded inspection')

    def evidence(self, ref, source_ref):
        return GitEvidence('https://github.com/' + SOURCE_REPOSITORY + '.git', ref, source_ref=source_ref)

    def credentials(self): runtime_credentials(os.environ)


def binding_from_artifact(artifact: dict, event: dict, approvals) -> tuple[dict, bytes]:
    if artifact.get('expired') is not False or artifact.get('name') != 'release-candidate-' + str(event['run_id']):
        raise ExecutionError('required immutable candidate artifact unavailable')
    binding = {'run_id': event['run_id'], 'artifact_id': artifact['id'], 'artifact_digest': artifact['digest'],
        'candidate_id': '', 'environment': ENVIRONMENT, 'artifact_name': artifact['name']}
    payload = approvals.artifact_bytes(binding)
    if 'sha256:' + hashlib.sha256(payload).hexdigest() != binding['artifact_digest']:
        raise ExecutionError('retained candidate download digest mismatch')
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            binding['candidate_id'] = json.loads(archive.read('candidate.json'))['candidate_id']
    except (ValueError, KeyError, zipfile.BadZipFile) as exc:
        raise ExecutionError('retained candidate description unavailable') from exc
    retained_artifact_files(payload, binding)
    return binding, payload


def candidate_artifact(services, event):
    matches = [a for a in services.artifacts(event) if a['name'] == 'release-candidate-' + str(event['run_id'])]
    if len(matches) != 1: raise ExecutionError('exactly one original retained candidate is required; do not rebuild on retry')
    return matches[0]


def prepare_operation(root: Path, output: Path, event: dict, settings: dict, services) -> dict:
    setup = validate_setup(services.setup(event), settings, event)
    errors = validate_workflow(root)
    if errors: raise ExecutionError('; '.join(errors))
    if run(['git', 'rev-parse', 'HEAD'], root) != event['source_commit']:
        raise ExecutionError('checkout differs from reviewed workflow source')
    if event['attempt'] > 1:
        binding, payload = binding_from_artifact(candidate_artifact(services, event), event, services.approvals)
        # Download/validate exact original data; no builder is invoked on retry.
        candidate = materialize_artifact(output, binding, services.approvals)
        if candidate['source_commit'] != event['source_commit'] or candidate['approval_environment_identity'] != setup['approval_environment_identity']:
            raise ExecutionError('retained candidate setup/source changed; requires a new candidate decision')
        return dict(status='ready', candidate=candidate, binding=binding)
    latest = services.latest()
    inputs = derive_release_inputs(root, latest)
    if inputs['status'] == 'already-published':
        with services.evidence(setup['evidence_ref'], event['source_ref']) as store:
            store.refresh(); state = read_execution_state(store.read('docs/releases/v' + latest + '.md'))
            candidate_bytes = store.read('docs/releases/v' + latest + '/candidate.json')
        if state and state['status'] == 'completed' and candidate_bytes:
            prior = json.loads(candidate_bytes)
            # A different merged source is conservative upstream work, not an
            # inferred release/no-op based on its filenames or unchanged number.
            if prior['source_commit'] == event['source_commit'] and prior['candidate_id'] == state['candidate_id']:
                return {'status': 'already-published', 'version': latest}
        raise ExecutionError('unreleased or unclassified changed source needs a reviewed next-version decision')
    # The provider establishes this exact default-branch push. A newer remote tip
    # is not substituted for it; a local ref is only the builder input selector.
    run(['git', 'update-ref', event['source_ref'], event['source_commit']], root)
    candidate = prepare_candidate(root, event['source_commit'], event['source_ref'], latest, output, evidence_ref=setup['evidence_ref'])
    candidate.pop('candidate_id')
    candidate['approval_environment_identity'] = setup['approval_environment_identity']
    candidate['setup'] = setup
    candidate = seal_candidate(output, candidate)
    return {'status': 'ready', 'candidate': candidate}


def restore_recovery(output, services, event, binding):
    previous = [a for a in services.artifacts(event) if re.fullmatch(
        'release-observation-' + str(event['run_id']) + r'-[0-9]+', a['name']) and int(a['name'].rsplit('-', 1)[1]) < event['attempt']]
    if event['attempt'] > 1 and not any(a['name'].endswith('-' + str(event['attempt'] - 1)) for a in previous):
        raise ExecutionError('previous attempt observation artifact unavailable; preserve durable state for explicit recovery')
    if len({a['name'] for a in previous}) != len(previous):
        raise ExecutionError('ambiguous recovery artifact identity')
    for artifact in sorted(previous, key=lambda a: int(a['name'].rsplit('-', 1)[1]), reverse=True):
        if artifact['expired']: raise ExecutionError('recovery observations expired; inspect durable/public state before resuming')
        payload = services.approvals.artifact_bytes({'artifact_id': artifact['id']})
        if 'sha256:' + hashlib.sha256(payload).hexdigest() != artifact['digest']:
            raise ExecutionError('recovery observation digest mismatch')
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            if archive.namelist() != ['observed-outcome.json']: raise ExecutionError('unexpected recovery inventory')
            if archive.getinfo('observed-outcome.json').file_size > 16 * 1024 * 1024: raise ExecutionError('oversized recovery observations')
            data = archive.read('observed-outcome.json')
        state = json.loads(data)
        if state['candidate_id'] != binding['candidate_id']: raise ExecutionError('recovery belongs to another candidate')
        (output / 'observed-outcome.json').write_bytes(data)
        return


def execute_operation(root: Path, output: Path, event: dict, settings: dict, binding: dict, services):
    validate_setup(services.setup(event), settings, event)
    if validate_workflow(root): raise ExecutionError('current workflow composition changed')
    services.credentials()  # Missing credentials stop before tag/GitHub/npm writes.
    candidate = materialize_artifact(output, binding, services.approvals)
    if candidate['source_commit'] != event['source_commit'] or candidate['evidence_ref'] != settings['evidence_ref']:
        raise ExecutionError('candidate differs from execution source/destination')
    restore_recovery(output, services, event, binding)
    with services.evidence(candidate['evidence_ref'], candidate['source_ref']) as store:
        state = execute_candidate(output, binding, approvals=services.approvals, publisher=services.publisher, evidence=store)
        # The durable ref is authoritative. Mirror its exact version-scoped
        # snapshot when possible, never rebuild or mutate the approved package.
        commit = store.base
        paths = [f"docs/releases/{candidate['tag']}.md", f"docs/releases/{candidate['tag']}",
            f"docs/releases/profiles/{candidate['tag']}.yaml", f"docs/reports/adapter-artifacts/releases/{candidate['tag']}.yaml"]
        try:
            payload = store.git('archive', '--format=zip', commit, *paths).stdout
            services.publisher.mirror_evidence(candidate, commit, payload)
            state['mirror'] = {'result': 'copied', 'evidence_commit': commit, 'sha256': hashlib.sha256(payload).hexdigest()}
        except (ExecutionError, CandidateError, OSError, subprocess.SubprocessError):
            state['mirror'] = {'result': 'unavailable', 'evidence_commit': commit,
                'consequence': 'optional mirror only; durable evidence ref remains authoritative'}
        from release_execution import render_standing, now
        try:
            (output / 'observed-outcome.json').write_bytes(canonical_bytes(state))
            store.save({f"docs/releases/{candidate['tag']}.md": render_standing(candidate, state)})
        except (ExecutionError, OSError):
            state.update(status='failed-after-publication', active=False, failure='Required reporting unavailable after optional evidence mirroring.')
            state['events'].append({'at': now(), 'boundary': 'reporting', 'result': 'incomplete',
                'run_id': event['run_id'], 'run_attempt': event['attempt']})
            (output / 'observed-outcome.json').write_bytes(canonical_bytes(state))
            raise ExecutionError('durable reporting unavailable; retained observations require reconciliation')
        return state


def read_evidence(services, ref: str, tag: str) -> dict:
    version_tuple(tag.removeprefix('v'))
    if not tag.startswith('v'): raise ExecutionError('expected stable release tag')
    with services.evidence(ref, 'refs/heads/main') as store:
        store.refresh()
        state = read_execution_state(store.read(f'docs/releases/{tag}.md'))
        if state is None: raise ExecutionError('new-path evidence absent; use historical source reader only for historical records')
        data = store.read(f'docs/releases/{tag}/candidate.json')
        if not data: raise ExecutionError('required candidate description missing')
        candidate = json.loads(data); claimed = candidate.pop('candidate_id')
        if claimed != state['candidate_id'] or hashlib.sha256(canonical_bytes(candidate)).hexdigest() != claimed:
            raise ExecutionError('evidence candidate identity mismatch')
        candidate['candidate_id'] = claimed
        if state['status'] == 'completed':
            for boundary in BOUNDARIES:
                observed = state['observations'].get(boundary)
                if boundary == 'github' and observed: observed = dict(observed, draft=False)
                if classify_observation(boundary, observed, candidate) != 'matching':
                    raise ExecutionError('completed evidence has missing/conflicting required identity')
            from release_transaction import validate_published_release_artifacts, validate_release_timing_evidence
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                for path in [f'docs/releases/profiles/{tag}.yaml', f'docs/releases/{tag}/npm-publication.md', f'docs/releases/{tag}/timing.yaml']:
                    content = store.read(path)
                    if content is None: raise ExecutionError('required evidence projection unavailable')
                    target = root / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(content)
                if validate_published_release_artifacts(tag, root=root): raise ExecutionError('published companion evidence is invalid')
                timing = validate_release_timing_evidence(tag, root=root)
                state['read_timing_diagnostic'] = list(timing.errors) + list(timing.warnings)
        return state


def summary(candidate: dict) -> str:
    rows = [f"# Prepared release {candidate['tag']} ({candidate['channel']})", candidate['inputs']['summary'],
        f"Source: `{candidate['source_commit']}`; prepared source: `{candidate['prepared_commit']}`.",
        f"Candidate: `{candidate['candidate_id']}`.",
        'Required checks: ' + ', '.join(c['id'] + '=' + c['result'] for c in candidate['checks']) + '.',
        'Generated source changes: ' + ', '.join(candidate['source_diff']) + '.',
        'Approval authorizes the retained tag, GitHub assets and npm tarball through trusted publishing; automatic public verification and reporting follow.',
        f"Destinations: GitHub `{SOURCE_REPOSITORY}`, npm `{candidate['package']}`, evidence `{candidate['evidence_ref']}`.",
        'Artifacts: ' + ', '.join(candidate['files']) + '.',
        'Setup: inspected GitHub protection; npm configuration intent declared, actual runtime authorization remains required.',
        'Timing limitations: ' + '; '.join(candidate['diagnostics'])]
    return '\n\n'.join(rows) + '\n'
