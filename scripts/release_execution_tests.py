"""Release execution authority and persistence proof; public services are fixtures."""
import copy
import json
import hashlib
import io
import zipfile
from pathlib import Path
import subprocess
import tempfile
import unittest

from release_execution import ExecutionError, GitEvidence, validate_approval, environment_identity


class ReleaseApprovalTests(unittest.TestCase):
    def test_ci_only_candidate_cannot_receive_publication_authority(self):
        self.candidate['inputs'] = {'ci_only': True}
        with self.assertRaisesRegex(ExecutionError, 'CI-only'):
            validate_approval(self.candidate, self.binding, self.facts)

    def setUp(self):
        self.candidate = {'candidate_id': 'a' * 64, 'source_commit': 'b' * 40,
            'source_ref': 'refs/heads/main', 'repository': 'xiongxianfei/rigorloop'}
        self.binding = {'run_id': 12, 'artifact_id': 13, 'artifact_digest': 'sha256:' + 'c' * 64,
            'candidate_id': 'a' * 64, 'environment': 'release', 'artifact_name': 'release-candidate-12'}
        self.facts = {
            'repository': {'full_name': 'xiongxianfei/rigorloop', 'id': 7, 'default_branch': 'main'},
            'run': {'id': 12, 'event': 'push', 'head_sha': 'b' * 40, 'head_branch': 'main',
                'path': '.github/workflows/release.yml', 'status': 'in_progress', 'run_attempt': 1},
            'artifact': {'id': 13, 'name': 'release-candidate-12', 'digest': self.binding['artifact_digest'],
                'expired': False, 'workflow_run': {'id': 12, 'head_sha': 'b' * 40, 'repository_id': 7, 'head_repository_id': 7}},
            'environment': {'id': 9, 'name': 'release', 'deployment_branch_policy': {'protected_branches': True, 'custom_branch_policies': False},
                'protection_rules': [{'type': 'required_reviewers', 'reviewers': [{'type': 'User', 'reviewer': {'id': 2}}]}]},
            'approvals': [{'state': 'approved', 'environments': [{'id': 9, 'name': 'release'}], 'user': {'id': 2, 'login': 'maintainer'}}]}

        self.candidate['approval_environment_identity'] = environment_identity(self.facts['environment'])

    def test_exact_provider_approval_binds_candidate(self):
        result = validate_approval(self.candidate, self.binding, self.facts)
        self.assertEqual(result['candidate_id'], self.candidate['candidate_id'])
        self.assertEqual(result['reviewer_id'], 2)

    def test_missing_rejected_stale_or_unknown_value_approval_rejects(self):
        for state in ['rejected', 'pending', 'unknown_value']:
            with self.subTest(state=state):
                facts = copy.deepcopy(self.facts); facts['approvals'][0]['state'] = state
                with self.assertRaises(ExecutionError): validate_approval(self.candidate, self.binding, facts)
        for field in ['approvals', 'artifact', 'environment']:
            facts = copy.deepcopy(self.facts); facts.pop(field)
            with self.assertRaises(ExecutionError): validate_approval(self.candidate, self.binding, facts)

    def test_material_provider_changes_and_unprotected_environment_reject(self):
        changes = [('artifact', 'expired', True), ('artifact', 'digest', 'sha256:' + 'd' * 64),
            ('run', 'head_sha', 'd' * 40), ('run', 'event', 'push_tag'), ('run', 'status', 'completed'),
            ('environment', 'protection_rules', []), ('repository', 'full_name', 'another/repository')]
        for section, field, value in changes:
            with self.subTest(field=field):
                facts = copy.deepcopy(self.facts); facts[section][field] = value
                with self.assertRaises(ExecutionError): validate_approval(self.candidate, self.binding, facts)
        self.facts['approvals'][0]['user']['id'] = 99
        with self.assertRaises(ExecutionError): validate_approval(self.candidate, self.binding, self.facts)

    def test_unknown_value_approval_field_rejects_before_consistency(self):
        self.binding['unknown_value'] = 'must-not-be-retained'
        with self.assertRaisesRegex(ExecutionError, 'binding field'):
            validate_approval(self.candidate, self.binding, self.facts)


class ReleaseEvidenceStoreTests(unittest.TestCase):
    def test_real_git_compare_and_swap_preserves_unrelated_and_rejects_race(self):
        with tempfile.TemporaryDirectory() as temporary:
            remote = Path(temporary) / 'remote.git'
            subprocess.run(['git', 'init', '--bare', '--quiet', str(remote)], check=True)
            with GitEvidence(str(remote), 'refs/heads/release-evidence') as a, GitEvidence(str(remote), 'refs/heads/release-evidence') as b:
                a.refresh(); b.refresh()
                a.save({'docs/releases/v0.5.1.md': b'first observation\n'})
                with self.assertRaises(ExecutionError): b.save({'docs/releases/v0.5.2.md': b'racing\n'})
                b.refresh()
                self.assertEqual(b.read('docs/releases/v0.5.1.md'), b'first observation\n')
                b.save({'docs/releases/v0.5.2.md': b'later observation\n'})
                a.refresh()
                self.assertEqual(a.read('docs/releases/v0.5.1.md'), b'first observation\n')
                self.assertEqual(a.read('docs/releases/v0.5.2.md'), b'later observation\n')

    def test_source_ref_and_path_escape_rejected(self):
        with self.assertRaises(ExecutionError): GitEvidence('remote', 'refs/heads/main', source_ref='refs/heads/main')


class ReleaseExecutorTests(unittest.TestCase):
    def setUp(self):
        import shutil
        import zipfile
        from release_candidate import (derive_release_inputs, profile_text, write_archive_metadata,
            file_identity, seal_candidate, CANDIDATE_CHECKS, run, script_identity)
        from release_transaction import prepare_release
        self.temp = tempfile.TemporaryDirectory(prefix='release-execution-fixture-')
        self.addCleanup(self.temp.cleanup)
        workspace = Path(self.temp.name)
        self.source, self.output = workspace / 'source', workspace / 'candidate'
        self.source.mkdir(); self.output.mkdir()
        repo = Path(__file__).resolve().parents[1]
        shutil.copytree(repo / 'scripts', self.source / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        (self.source / '.github/workflows').mkdir(parents=True)
        shutil.copyfile(repo / '.github/workflows/release.yml', self.source / '.github/workflows/release.yml')
        (self.source / 'packages/rigorloop/dist/metadata').mkdir(parents=True)
        (self.source / 'packages/rigorloop/package.json').write_text(json.dumps({'name': '@xiongxianfei/rigorloop', 'version': '0.5.1'}))
        (self.source / 'dist/adapters').mkdir(parents=True)
        shutil.copyfile(repo / 'dist/adapters/manifest.yaml', self.source / 'dist/adapters/manifest.yaml')
        (self.source / 'docs/releases').mkdir(parents=True)
        (self.source / 'docs/releases/v0.5.1.md').write_text('# Release v0.5.1\n\n## Version Decision\n\n- Version decision: patch\n- Change summary: Reviewed isolated execution fixture.\n')
        def git(*args):
            return run(['git', '-c', 'user.name=Release Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', *args], self.source)
        git('init', '--quiet', '-b', 'main'); git('add', '.'); git('commit', '--quiet', '-m', 'Reviewed fixture')
        original = git('rev-parse', 'HEAD')
        inputs = derive_release_inputs(self.source, '0.5.0')
        profile = self.source / 'docs/releases/profiles/v0.5.1.yaml'
        profile.parent.mkdir(); profile.write_text(profile_text('v0.5.1'))
        prepare_release('v0.5.1', root=self.source, approval_driven=True)
        git('add', '.'); git('commit', '--quiet', '-m', 'Prepared fixture')
        commit = git('rev-parse', 'HEAD')
        for target in ['codex', 'claude', 'opencode']:
            with zipfile.ZipFile(self.output / f'rigorloop-adapter-{target}-v0.5.1.zip', 'w') as archive:
                root = {'codex': '.agents/skills', 'claude': '.claude/skills', 'opencode': '.opencode/skills'}[target]
                archive.writestr(root + '/example/SKILL.md', '# Fixture capability\n')
                if target == 'opencode': archive.writestr('.opencode/commands/example.md', '# Fixture command\n')
        write_archive_metadata(self.source, self.output, 'v0.5.1', commit, self.source / 'packages/rigorloop')
        (self.output / 'package.tgz').write_bytes(b'isolated publication-boundary fixture, not package-validation proof')
        (self.output / 'release-verification.json').write_text(json.dumps({'prepared_commit': commit, 'result': 'pass',
            'checks': [{'command': 'fixture identity basis; full validation covered by candidate integration', 'result': 'pass'}]}))
        shutil.copyfile(profile, self.output / 'profile.yaml')
        shutil.copyfile(self.source / 'docs/releases/v0.5.1/release-notes.md', self.output / 'release-notes.md')
        git('bundle', 'create', str(self.output / 'source.bundle'), 'HEAD')
        authority = ReleaseApprovalTests(); authority.setUp()
        self.binding, self.facts = authority.binding, authority.facts
        self.facts['run']['head_sha'] = original
        self.facts['artifact']['workflow_run']['head_sha'] = original
        self.candidate = seal_candidate(self.output, {'source_commit': original, 'prepared_commit': commit,
            'source_ref': 'refs/heads/main', 'version': '0.5.1', 'tag': 'v0.5.1', 'package': '@xiongxianfei/rigorloop',
            'channel': 'latest', 'repository': 'xiongxianfei/rigorloop', 'publication_path': 'trusted-publishing',
            'evidence_ref': 'refs/heads/release-evidence', 'inputs': inputs, 'tarball': 'package.tgz',
            'files': {p.name: file_identity(p) for p in self.output.iterdir()},
            'checks': [{'id': key, 'result': 'pass'} for key in sorted(CANDIDATE_CHECKS)],
            'approval_environment_identity': environment_identity(self.facts['environment']),
            'tool_identity': script_identity(repo / 'scripts'), 'workflow_identity': file_identity(repo / '.github/workflows/release.yml'),
            'environment': {name: run([name, '--version'], repo) for name in ['python', 'node', 'npm']}})
        self.binding['candidate_id'] = self.candidate['candidate_id']
        self.remote = workspace / 'evidence.git'
        subprocess.run(['git', 'init', '--bare', '--quiet', str(self.remote)], check=True)
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, 'w') as retained:
            for entry in self.output.iterdir(): retained.write(entry, entry.name)
        self.payload = archive.getvalue()
        self.binding['artifact_digest'] = 'sha256:' + hashlib.sha256(self.payload).hexdigest()
        self.facts['artifact']['digest'] = self.binding['artifact_digest']
        self.approvals = FixtureApprovals(self.facts, self.payload)
        self.publisher = FixturePublisher(self.candidate, self.output)

    def execute(self, store=None):
        from release_execution import execute_candidate
        if store is not None:
            return execute_candidate(self.output, self.binding, approvals=self.approvals, publisher=self.publisher, evidence=store)
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            return self.execute(evidence)

    def stored(self):
        from release_execution import read_execution_state
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            evidence.refresh()
            return read_execution_state(evidence.read('docs/releases/v0.5.1.md'))

    def test_one_approval_path_persists_and_duplicate_never_republishes(self):
        self.assertEqual(self.execute()['status'], 'completed')
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertEqual(self.stored()['status'], 'completed')
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            evidence.refresh()
            from adapter_distribution import parse_release_yaml
            metadata = parse_release_yaml(evidence.read('docs/releases/v0.5.1/release.yaml').decode())
            self.assertEqual(metadata.publication_status, 'published')
            self.assertTrue(all(row.result == 'pass' for row in metadata.smoke.values()))
            self.assertIsNotNone(evidence.read('docs/reports/adapter-artifacts/releases/v0.5.1.yaml'))
        self.assertEqual(self.execute()['status'], 'completed')
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])

    def test_lost_write_response_observes_matching_state_without_second_write(self):
        self.publisher.lose_response = 'npm'
        self.assertEqual(self.execute()['status'], 'completed')
        self.assertEqual(self.publisher.writes.count('npm'), 1)
        self.assertTrue(any(e['result'] == 'write-response-unavailable' for e in self.stored()['events']))
        self.assertNotIn('must-not-be-recorded', json.dumps(self.stored()))

    def test_failed_smoke_preserves_publication_and_retry_only_observes(self):
        self.publisher.fail_smoke = True
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.stored()['status'], 'failed-after-publication')
        self.publisher.fail_smoke = False
        self.execute()
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertTrue(any(e['result'] == 'incomplete' for e in self.stored()['events']))

    def test_candidate_tamper_and_rejected_approval_cause_no_external_writes(self):
        self.facts['approvals'][0]['state'] = 'rejected'
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.publisher.writes, [])
        self.facts['approvals'][0]['state'] = 'approved'
        (self.output / 'package.tgz').write_bytes(b'tampered')
        from release_candidate import CandidateError
        with self.assertRaises(CandidateError): self.execute()
        self.assertEqual(self.publisher.writes, [])

    def test_conflicting_public_identity_stops_without_overwrite(self):
        self.publisher.states['tag'] = {'commit': 'f' * 40}
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.publisher.writes, [])

    def test_public_uncertainty_never_implies_absence_or_republish(self):
        self.publisher.unknown = 'npm'
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.publisher.writes, ['tag', 'github'])
        self.publisher.unknown = None
        self.execute()
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])

    def test_competing_executor_is_excluded_by_durable_active_attempt(self):
        def compete():
            with self.assertRaisesRegex(ExecutionError, 'already active'): self.execute()
        self.publisher.before_write = compete
        self.execute()
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])

    def test_failed_reporting_retains_observations_and_recovery_cannot_republish(self):
        class FailingStore(GitEvidence):
            calls = 0
            def save(self, changes):
                self.calls += 1
                if self.calls >= 7: raise ExecutionError('fixture persistence unavailable')
                return super().save(changes)
        with FailingStore(str(self.remote), self.candidate['evidence_ref']) as store:
            with self.assertRaises(ExecutionError): self.execute(store)
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertTrue((self.output / 'observed-outcome.json').is_file())
        self.assertIn('reporting', json.loads((self.output / 'observed-outcome.json').read_text())['failure'])
        self.facts['run']['run_attempt'] = 2
        self.execute()
        self.assertEqual([a['run_attempt'] for a in self.stored()['approvals']], [1, 2])
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertEqual(self.stored()['status'], 'completed')
        self.assertTrue(any(e['boundary'] == 'reporting' and e['result'] == 'incomplete' for e in self.stored()['events']))

    def test_first_persistence_failure_cannot_publish(self):
        class FailingStore(GitEvidence):
            def save(self, changes): raise ExecutionError('fixture persistence unavailable')
        with FailingStore(str(self.remote), self.candidate['evidence_ref']) as store:
            with self.assertRaises(ExecutionError): self.execute(store)
        self.assertEqual(self.publisher.writes, [])

    def test_unknown_value_execution_state_and_boundary_reject(self):
        from release_execution import read_execution_state, classify_observation, STATE_START, STATE_END
        with self.assertRaises(ExecutionError): classify_observation('unknown_value', None, self.candidate)
        data = {'status': 'unknown_value', 'active': False, 'events': []}
        with self.assertRaises(ExecutionError): read_execution_state((STATE_START + '\n```json\n' + json.dumps(data) + '\n```\n' + STATE_END).encode())

    def test_partial_github_assets_resume_only_missing_publication(self):
        self.publisher.publish('tag', self.candidate, self.output, self.source)
        self.publisher.publish('github', self.candidate, self.output, self.source)
        self.publisher.states['github']['assets'].pop()
        self.publisher.writes.clear()
        self.execute()
        self.assertEqual(self.publisher.writes, ['github', 'npm'])

    def test_public_tree_mismatch_keeps_failed_closeout(self):
        original = self.publisher.verify_smoke_identity
        def corrupt(candidate, output):
            self.publisher.installed['.agents/skills']['tree_sha256'] = '0' * 64
            original(candidate, output)
        self.publisher.verify_smoke_identity = corrupt
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.stored()['status'], 'failed-after-publication')

    def test_provider_digest_does_not_authorize_another_valid_local_candidate(self):
        from release_candidate import seal_candidate
        candidate = dict(self.candidate)
        candidate.pop('candidate_id'); candidate['inputs'] = dict(candidate['inputs'], summary='Changed review subject')
        changed = seal_candidate(self.output, candidate)
        self.binding['candidate_id'] = changed['candidate_id']
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.publisher.writes, [])

    def test_unsafe_or_mismatched_retained_zip_rejects(self):
        from release_execution import retained_artifact_files
        for payload in [b'not original ZIP', self.payload[:-4]]:
            with self.assertRaises(ExecutionError): retained_artifact_files(payload, self.binding)
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as archive: archive.writestr('../candidate.json', '{}')
        binding = dict(self.binding, artifact_digest='sha256:' + hashlib.sha256(data.getvalue()).hexdigest())
        with self.assertRaises(ExecutionError): retained_artifact_files(data.getvalue(), binding)

    def test_successful_first_write_with_unknown_observation_stays_uncertain(self):
        original = self.publisher.publish
        def publish(boundary, *args):
            original(boundary, *args)
            self.publisher.unknown = boundary
        self.publisher.publish = publish
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.publisher.writes, ['tag'])
        self.assertEqual(self.stored()['status'], 'uncertain-publication')
        self.assertEqual(self.stored()['uncertain_write'], 'tag')

    def test_subprocess_timeout_inspects_matching_write_before_continuation(self):
        original = self.publisher.publish
        def publish(boundary, *args):
            original(boundary, *args)
            raise subprocess.TimeoutExpired('private-sensitive-command', 1)
        self.publisher.publish = publish
        self.assertEqual(self.execute()['status'], 'completed')
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertNotIn('private-sensitive-command', json.dumps(self.stored()))

    def test_delayed_npm_visibility_completes_without_duplicate_publication(self):
        original = self.publisher.observe
        pending = 120
        waits = []

        def observe(boundary, candidate):
            nonlocal pending
            result = original(boundary, candidate)
            if boundary == 'npm' and result is not None and pending:
                pending -= 1
                return None
            return result

        self.publisher.observe = observe
        self.publisher.wait_for_visibility = waits.append
        self.assertEqual(self.execute()['status'], 'completed')
        self.assertEqual(pending, 0)
        self.assertEqual(waits, list(range(120)))
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])

    def test_timing_diagnostic_is_reported_without_changing_publication_success(self):
        self.assertEqual(self.execute()['status'], 'completed')
        diagnostic = self.stored()['timing_diagnostic']
        self.assertEqual(diagnostic['result'], 'fail')
        self.assertIn('missing timing phase: prepare_release', diagnostic['errors'])
        self.assertIn('diagnostic only', diagnostic['consequence'])

    def test_network_publish_uses_retained_tarball_and_oidc_without_token_fallback(self):
        from unittest.mock import patch
        from release_provider import NetworkPublisher
        environment = {'GITHUB_ACTIONS': 'true', 'ACTIONS_ID_TOKEN_REQUEST_URL': 'fixture',
            'ACTIONS_ID_TOKEN_REQUEST_TOKEN': 'fixture', 'NODE_AUTH_TOKEN': 'must-not-use', 'NPM_TOKEN': 'must-not-use'}
        with patch.dict('os.environ', environment), patch('release_provider.run') as command:
            NetworkPublisher().publish('npm', self.candidate, self.output, self.source)
            argv = command.call_args.args[0]
            self.assertEqual(argv[:3], ['npm', 'publish', str(self.output / 'package.tgz')])
            self.assertIn('--provenance', argv); self.assertIn('--ignore-scripts', argv)
            self.assertNotIn('NODE_AUTH_TOKEN', command.call_args.kwargs['env'])
            self.assertNotIn('NPM_TOKEN', command.call_args.kwargs['env'])
        with patch.dict('os.environ', {'GITHUB_ACTIONS': 'false'}), patch('release_provider.run') as command:
            with self.assertRaises(ExecutionError): NetworkPublisher().publish('npm', self.candidate, self.output, self.source)
            command.assert_not_called()


class FixtureApprovals:
    def __init__(self, facts, payload=b''): self.facts, self.payload = facts, payload
    def artifact_bytes(self, binding): return self.payload
    def fetch(self, binding): return copy.deepcopy(self.facts)


from release_provider import NetworkPublisher
class FixturePublisher(NetworkPublisher):
    """External service fixture only. Executor, Git CAS and closeout validators run."""
    def __init__(self, candidate, output):
        super().__init__()
        self.candidate, self.output = candidate, output
        self.states = {key: None for key in ['tag', 'github', 'npm']}
        self.writes = []
        self.lose_response = self.unknown = self.before_write = None
        self.fail_smoke = False

    def wait_for_visibility(self, attempt):
        pass  # Only the external visibility clock is substituted.

    def observe(self, boundary, candidate):
        from release_execution import ExternalUnavailable
        if self.unknown == boundary: raise ExternalUnavailable('fixture unavailable')
        return copy.deepcopy(self.states[boundary])

    def publish(self, boundary, candidate, output, source):
        import hashlib, base64
        from release_execution import public_files, ExternalUnavailable
        if self.before_write:
            callback, self.before_write = self.before_write, None
            callback()
        self.writes.append(boundary)
        if boundary == 'tag': self.states[boundary] = {'commit': candidate['prepared_commit']}
        elif boundary == 'github': self.states[boundary] = {'tag': candidate['tag'], 'draft': False,
            'assets': [{'name': name, 'sha256': candidate['files'][name]['sha256']} for name in public_files(candidate)]}
        else: self.states[boundary] = {'package': candidate['package'], 'version': candidate['version'],
            'dist_tag': candidate['version'], 'sha256': candidate['files'][candidate['tarball']]['sha256'],
            'integrity': 'sha512-' + base64.b64encode(hashlib.sha512((output / candidate['tarball']).read_bytes()).digest()).decode(),
            'tarball': 'https://registry.npmjs.org/@xiongxianfei/rigorloop/-/rigorloop-0.5.1.tgz',
            'published_at': '2026-09-09T12:00:00Z'}
        if self.lose_response == boundary: raise ExternalUnavailable('fixture lost response with TOKEN=must-not-be-recorded')

    def fetch_github_release_assets(self, *, tag):
        from release_transaction import GitHubReleaseAsset
        return tuple(GitHubReleaseAsset(name=a['name'], url=f'https://github.com/xiongxianfei/rigorloop/releases/download/{tag}/{a["name"]}',
            size=self.candidate['files'][a['name']]['size'], sha256='sha256:' + a['sha256']) for a in self.states['github']['assets'] if a['name'].endswith('.zip'))

    def fetch_npm_package_metadata(self, *, package, version):
        from release_transaction import NpmPackageMetadata
        state = self.states['npm']
        return NpmPackageMetadata(package=package, version=version, tarball_url=state['tarball'], integrity=state['integrity'], published_at=state['published_at'])

    def run_public_npx_smoke(self, *, command, cwd):
        import zipfile, hashlib
        from release_transaction import PublicSmokeResult, _target_install_roots
        from adapter_distribution import _tree_hash_for_rows, _normalized_tree_hash_bytes
        if self.fail_smoke: return PublicSmokeResult(command, 1, '', '', 'fixture smoke failed')
        target = command.split()[-1]
        if target != 'version':
            with zipfile.ZipFile(self.output / f'rigorloop-adapter-{target}-{self.candidate["tag"]}.zip') as archive:
                archive.extractall(cwd)  # Trusted test-created archive, not a production loader.
            for name in _target_install_roots(target):
                root = cwd / name
                rows = [(p.relative_to(root).as_posix(), hashlib.sha256(_normalized_tree_hash_bytes(p.name, p.read_bytes())).hexdigest()) for p in root.rglob('*') if p.is_file()]
                self.installed[name] = {'tree_sha256': _tree_hash_for_rows(rows), 'file_count': len(rows)}
        return PublicSmokeResult(command, 0, '@xiongxianfei/rigorloop ' + self.candidate['version'], '', 'fixture public ' + target + ' completed')
