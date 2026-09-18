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

import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_execution import ExecutionError, GitEvidence, validate_approval, environment_identity
from release_fixture_helpers import approval_fixture
from release_provider_fixtures import FixtureApprovals, FixturePublisher


class ReleaseApprovalTests(unittest.TestCase):
    def test_ci_only_candidate_cannot_receive_publication_authority(self):
        self.candidate['inputs'] = {'ci_only': True}
        with self.assertRaisesRegex(ExecutionError, 'CI-only'):
            validate_approval(self.candidate, self.binding, self.facts)

    def setUp(self):
        self.candidate, self.binding, self.facts = approval_fixture()

    def test_approval_policy_runs_without_usable_package_metadata(self):
        # Policy must not need package generation merely to inspect provider facts.
        import shutil
        for metadata in (None, "malformed package metadata"):
            with self.subTest(metadata=metadata), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                shutil.copytree(ROOT / "scripts/lib", root / "scripts/lib",
                                ignore=shutil.ignore_patterns("__pycache__"))
                package = root / "packages/rigorloop/package.json"
                if metadata is not None:
                    package.parent.mkdir(parents=True)
                    package.write_text(metadata)
                command = ("import json,sys; sys.path.insert(0,'scripts'); "
                           "from lib.release.release_execution import validate_approval; "
                           "print(json.dumps(validate_approval(*json.load(sys.stdin))))")
                result = subprocess.run([sys.executable, "-B", "-c", command], cwd=root,
                    input=json.dumps([self.candidate, self.binding, self.facts]),
                    text=True, capture_output=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["candidate_id"], self.candidate["candidate_id"])
                self.assertEqual(json.loads(result.stdout)["reviewer_id"], 2)
                self.assertEqual(package.read_text() if package.exists() else None, metadata)

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
        accepted = validate_approval(self.candidate, self.binding, self.facts)
        self.assertEqual(accepted['candidate_id'], self.candidate['candidate_id'])
        self.assertEqual(accepted['reviewer_id'], 2)
        candidate, facts = copy.deepcopy(self.candidate), copy.deepcopy(self.facts)
        binding = dict(self.binding, unknown_value='must-not-be-retained', candidate_id='f' * 64)
        self.assertNotEqual(binding['candidate_id'], candidate['candidate_id'])
        before = copy.deepcopy(binding)
        with self.assertRaises(ExecutionError) as raised:
            validate_approval(candidate, binding, facts)
        self.assertEqual(str(raised.exception), 'unknown or missing approval binding field')
        self.assertEqual(binding, before)
        binding.pop('unknown_value')
        with self.assertRaises(ExecutionError) as raised:
            validate_approval(candidate, binding, facts)
        self.assertEqual(str(raised.exception), 'approval candidate mismatch')
        self.assertEqual(candidate, self.candidate)
        self.assertEqual(facts, self.facts)


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

    def test_source_ref_collision_is_rejected(self):
        with self.assertRaises(ExecutionError): GitEvidence('remote', 'refs/heads/main', source_ref='refs/heads/main')


class ReleaseExecutorTests(unittest.TestCase):
    def setUp(self):
        import shutil
        import zipfile
        from lib.release.release_candidate import (derive_release_inputs, profile_text, write_archive_metadata,
            file_identity, seal_candidate, CANDIDATE_CHECKS, run, script_identity)
        from lib.release.release_transaction import prepare_release
        self.temp = tempfile.TemporaryDirectory(prefix='release-execution-fixture-')
        self.addCleanup(self.temp.cleanup)
        workspace = Path(self.temp.name)
        self.source, self.output = workspace / 'source', workspace / 'candidate'
        self.source.mkdir(); self.output.mkdir()
        repo = ROOT
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
        for target in ['codex', 'claude']:
            with zipfile.ZipFile(self.output / f'rigorloop-adapter-{target}-v0.5.1.zip', 'w') as archive:
                root = {'codex': '.agents/skills', 'claude': '.claude/skills'}[target]
                archive.writestr(root + '/example/SKILL.md', '# Fixture capability\n')
        write_archive_metadata(self.source, self.output, 'v0.5.1', commit, self.source / 'packages/rigorloop')
        (self.output / 'package.tgz').write_bytes(b'isolated publication-boundary fixture, not package-validation proof')
        (self.output / 'release-verification.json').write_text(json.dumps({'prepared_commit': commit, 'result': 'pass',
            'checks': [{'command': 'fixture identity basis; full validation covered by candidate integration', 'result': 'pass'}]}))
        shutil.copyfile(profile, self.output / 'profile.yaml')
        shutil.copyfile(self.source / 'docs/releases/v0.5.1/release-notes.md', self.output / 'release-notes.md')
        git('bundle', 'create', str(self.output / 'source.bundle'), 'HEAD')
        _, self.binding, self.facts = approval_fixture()
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
        from lib.release.release_execution import execute_candidate
        if store is not None:
            return execute_candidate(self.output, self.binding, approvals=self.approvals, publisher=self.publisher, evidence=store)
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            return self.execute(evidence)

    def stored(self):
        from lib.release.release_execution import read_execution_state
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            evidence.refresh()
            return read_execution_state(evidence.read('docs/releases/v0.5.1.md'))

    def accepted_execution_inputs(self):
        from lib.release.release_candidate import verify_candidate
        self.assertEqual(verify_candidate(self.output, self.binding['candidate_id']), self.candidate)
        approval = validate_approval(self.candidate, self.binding, self.approvals.fetch(self.binding))
        self.assertEqual(approval['candidate_id'], self.candidate['candidate_id'])
        self.assertEqual(approval['reviewer_id'], 2)
        self.assertEqual(self.publisher.states, {'tag': None, 'github': None, 'npm': None})
        self.assertEqual(self.publisher.writes, [])

    def sealed_input_bytes(self):
        return {name: (self.output / name).read_bytes()
                for name in [*self.candidate['files'], 'candidate.json']}

    def assert_visibility_exhaustion_and_recovery(self, boundary, limit, prior_boundaries):
        self.accepted_execution_inputs()
        before = self.sealed_input_bytes()
        observe = self.publisher.observe
        counts = {'total': 0, 'after_write': 0}
        waits = []
        hidden = True

        def delayed(selected, candidate):
            actual = observe(selected, candidate)
            if selected == boundary:
                counts['total'] += 1
                if actual is not None and hidden:
                    counts['after_write'] += 1
                    return None
            return actual

        self.publisher.observe = delayed
        self.publisher.wait_for_visibility = waits.append
        with self.assertRaises(ExecutionError) as raised:
            self.execute()
        self.assertEqual(str(raised.exception),
                         f'Required {boundary} outcome unavailable or conflicting; inspect before recovery.')
        self.assertEqual(counts, {'total': limit + 1, 'after_write': limit})
        self.assertEqual(waits, list(range(limit - 1)))
        self.assertEqual(self.publisher.writes, [*prior_boundaries, boundary])
        self.assertIsNotNone(self.publisher.states[boundary])
        failed = self.stored()
        self.assertEqual(failed['status'], 'uncertain-publication')
        self.assertFalse(failed['active'])
        self.assertEqual(failed['uncertain_write'], boundary)
        self.assertEqual(set(failed['observations']), set(prior_boundaries))
        self.assertEqual([(e['boundary'], e['result']) for e in failed['events'][-2:]],
                         [(boundary, 'absent'), (boundary, 'incomplete')])
        self.assertEqual(self.sealed_input_bytes(), before)

        # Only visibility changes; the provider retains the already committed write.
        committed = copy.deepcopy(self.publisher.states[boundary])
        hidden = False
        recovered = self.execute()
        self.assertEqual(recovered['status'], 'completed')
        self.assertFalse(recovered['active'])
        self.assertNotIn('uncertain_write', recovered)
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertEqual(self.publisher.states[boundary], committed)
        self.assertGreater(counts['total'], limit + 1)
        self.assertEqual(waits, list(range(limit - 1)))
        self.assertEqual(recovered['events'][:len(failed['events'])], failed['events'])
        self.assertEqual(recovered['observations']['tag']['commit'], self.candidate['prepared_commit'])
        self.assertEqual(recovered['observations']['npm']['dist_tag'], self.candidate['version'])
        self.assertEqual(self.stored(), recovered)
        self.assertEqual(self.sealed_input_bytes(), before)

    def test_tag_visibility_exhaustion_recovers_without_republication(self):
        self.assert_visibility_exhaustion_and_recovery('tag', 6, [])

    def test_github_visibility_exhaustion_recovers_without_republication(self):
        self.assert_visibility_exhaustion_and_recovery('github', 6, ['tag'])

    def test_npm_visibility_exhaustion_recovers_without_republication(self):
        self.assert_visibility_exhaustion_and_recovery('npm', 121, ['tag', 'github'])

    def test_public_identity_changed_during_smoke_blocks_closeout_until_reobserved(self):
        self.accepted_execution_inputs()
        before = self.sealed_input_bytes()
        smoke = self.publisher.run_public_npx_smoke
        commands = []

        def drift(*, command, cwd):
            result = smoke(command=command, cwd=cwd)
            self.assertEqual(result.exit_code, 0)
            commands.append(command)
            if command.endswith(' init claude'):
                self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
                self.publisher.states['npm']['dist_tag'] = '0.5.0'
            return result

        self.publisher.run_public_npx_smoke = drift
        with self.assertRaises(ExecutionError) as raised:
            self.execute()
        self.assertEqual(str(raised.exception),
                         'Required public-smoke outcome unavailable or conflicting; inspect before recovery.')
        self.assertEqual(str(raised.exception.__cause__), 'public identity changed during closeout')
        self.assertEqual(len(commands), 3)
        self.assertTrue(commands[-1].endswith(' init claude'))
        failed = self.stored()
        self.assertEqual(failed['status'], 'failed-after-publication')
        self.assertFalse(failed['active'])
        self.assertNotIn('uncertain_write', failed)
        self.assertEqual(failed['events'][-1]['boundary'], 'public-smoke')
        self.assertEqual(failed['events'][-1]['result'], 'incomplete')
        self.assertFalse(any(e['boundary'] == 'public-smoke' and e['result'] == 'pass'
                             for e in failed['events']))
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertEqual(self.publisher.states['npm']['dist_tag'], '0.5.0')
        # This is a final public reread failure, not a failing smoke or installed tree.
        self.publisher.verify_smoke_identity(self.candidate, self.output)
        self.assertEqual(self.sealed_input_bytes(), before)
        self.publisher.states['npm']['dist_tag'] = self.candidate['version']
        self.publisher.run_public_npx_smoke = smoke
        recovered = self.execute()
        self.assertEqual(recovered['status'], 'completed')
        self.assertFalse(recovered['active'])
        self.assertEqual(recovered['events'][:len(failed['events'])], failed['events'])
        self.assertEqual(recovered['observations']['npm']['dist_tag'], self.candidate['version'])
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertEqual(self.stored(), recovered)
        self.assertEqual(self.sealed_input_bytes(), before)

    def test_provider_approval_revoked_after_tag_prevents_later_boundaries(self):
        self.accepted_execution_inputs()
        before = self.sealed_input_bytes()
        fetch, observe = self.approvals.fetch, self.publisher.observe
        authority_states, observed_boundaries = [], []

        def revoked(binding):
            facts = fetch(binding)
            if self.publisher.states['tag'] is not None:
                facts['approvals'][0]['state'] = 'rejected'
            authority_states.append(facts['approvals'][0]['state'])
            return facts

        def observed(boundary, candidate):
            observed_boundaries.append(boundary)
            return observe(boundary, candidate)

        self.approvals.fetch, self.publisher.observe = revoked, observed
        with self.assertRaises(ExecutionError) as raised:
            self.execute()
        self.assertEqual(str(raised.exception),
                         'Required github outcome unavailable or conflicting; inspect before recovery.')
        self.assertEqual(str(raised.exception.__cause__), 'missing, rejected or unknown provider approval')
        self.assertEqual(authority_states, ['approved', 'approved', 'rejected'])
        self.assertEqual(observed_boundaries, ['tag', 'tag'])
        self.assertEqual(self.publisher.writes, ['tag'])
        self.assertEqual(self.publisher.states, {
            'tag': {'commit': self.candidate['prepared_commit']}, 'github': None, 'npm': None})
        failed = self.stored()
        self.assertEqual(failed['status'], 'failed-after-publication')
        self.assertFalse(failed['active'])
        self.assertNotIn('uncertain_write', failed)
        self.assertEqual(failed['observations'], {'tag': {'commit': self.candidate['prepared_commit']}})
        self.assertEqual((failed['events'][-1]['boundary'], failed['events'][-1]['result']),
                         ('github', 'incomplete'))
        self.assertEqual(self.sealed_input_bytes(), before)

    def test_one_approval_path_persists_and_duplicate_never_republishes(self):
        self.assertEqual(self.execute()['status'], 'completed')
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertEqual(self.stored()['status'], 'completed')
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            evidence.refresh()
            from lib.packaging.adapter_distribution import parse_release_yaml
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
        from lib.release.release_candidate import CandidateError
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
        from lib.release.release_execution import read_execution_state, classify_observation, STATE_START, STATE_END
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
        from lib.release.release_candidate import seal_candidate
        candidate = dict(self.candidate)
        candidate.pop('candidate_id'); candidate['inputs'] = dict(candidate['inputs'], summary='Changed review subject')
        changed = seal_candidate(self.output, candidate)
        self.binding['candidate_id'] = changed['candidate_id']
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.publisher.writes, [])

    def test_unsafe_or_mismatched_retained_zip_rejects(self):
        from lib.release.release_execution import retained_artifact_files
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
        from lib.release.release_provider import NetworkPublisher
        environment = {'GITHUB_ACTIONS': 'true', 'ACTIONS_ID_TOKEN_REQUEST_URL': 'fixture',
            'ACTIONS_ID_TOKEN_REQUEST_TOKEN': 'fixture', 'NODE_AUTH_TOKEN': 'must-not-use', 'NPM_TOKEN': 'must-not-use'}
        with patch.dict('os.environ', environment), patch('lib.release.release_provider.run') as command:
            NetworkPublisher().publish('npm', self.candidate, self.output, self.source)
            argv = command.call_args.args[0]
            self.assertEqual(argv[:3], ['npm', 'publish', str(self.output / 'package.tgz')])
            self.assertIn('--provenance', argv); self.assertIn('--ignore-scripts', argv)
            self.assertNotIn('NODE_AUTH_TOKEN', command.call_args.kwargs['env'])
            self.assertNotIn('NPM_TOKEN', command.call_args.kwargs['env'])
        with patch.dict('os.environ', {'GITHUB_ACTIONS': 'false'}), patch('lib.release.release_provider.run') as command:
            with self.assertRaises(ExecutionError): NetworkPublisher().publish('npm', self.candidate, self.output, self.source)
            command.assert_not_called()
