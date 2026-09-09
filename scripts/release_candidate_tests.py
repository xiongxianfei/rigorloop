"""Candidate boundary proof (REL-SR-01–09, 18–19, 22–24)."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from release_candidate import (
    CANDIDATE_CHECKS, CandidateError, derive_release_inputs, profile_text, file_identity,
    seal_candidate, verify_candidate, timing_diagnostics,
)
from release_transaction import load_release_profile_file


class ReleaseCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'packages/rigorloop').mkdir(parents=True)
        (self.root / 'packages/rigorloop/package.json').write_text(json.dumps({
            'name': '@xiongxianfei/rigorloop', 'version': '0.5.1'}))
        (self.root / 'docs/releases').mkdir(parents=True)
        (self.root / 'docs/releases/v0.5.1.md').write_text(
            '# Release v0.5.1\n\n## Version Decision\n\n'
            '- Version decision: patch\n- Change summary: Fix candidate integrity checks.\n')

    def test_reviewed_version_input_and_derived_profile(self):
        data = derive_release_inputs(self.root, '0.5.0')
        self.assertEqual(data['version_decision'], 'patch')
        p = self.root / 'profile.yaml'
        p.write_text(profile_text(data['tag']))
        profile = load_release_profile_file(p)
        self.assertEqual(profile.targets, ('codex', 'claude', 'opencode'))
        self.assertEqual(profile.package_version, '0.5.1')

    def test_missing_version_decision_is_exception_not_inferred_from_number(self):
        (self.root / 'docs/releases/v0.5.1.md').unlink()
        with self.assertRaisesRegex(CandidateError, 'reviewed version decision'):
            derive_release_inputs(self.root, '0.5.0')

    def test_unknown_value_version_decision_rejected(self):
        p = self.root / 'docs/releases/v0.5.1.md'
        p.write_text(p.read_text().replace('patch', 'unknown_value'))
        with self.assertRaisesRegex(CandidateError, 'version decision'):
            derive_release_inputs(self.root, '0.5.0')

    def test_duplicate_version_is_noop_without_new_candidate(self):
        self.assertEqual(derive_release_inputs(self.root, '0.5.1')['status'], 'already-published')

    def test_version_increment_must_agree_with_reviewed_decision(self):
        with self.assertRaisesRegex(CandidateError, 'version decision'):
            derive_release_inputs(self.root, '0.4.9')

    def candidate(self):
        files = {}
        for name in ['package.tgz', 'adapter.zip']:
            (self.root / name).write_bytes(name.encode())
            files[name] = file_identity(self.root / name)
        return seal_candidate(self.root, {
            'source_commit': 'a' * 40, 'prepared_commit': 'b' * 40, 'source_ref': 'refs/heads/main',
            'version': '0.5.1', 'tag': 'v0.5.1', 'package': '@xiongxianfei/rigorloop',
            'channel': 'latest', 'repository': 'xiongxianfei/rigorloop',
            'publication_path': 'trusted-publishing', 'evidence_ref': 'refs/heads/release-evidence',
            'files': files, 'checks': [{'id': key, 'result': 'pass'} for key in sorted(CANDIDATE_CHECKS)],
        })

    def test_material_change_invalidates_sealed_candidate(self):
        manifest = self.candidate()
        verify_candidate(self.root, manifest['candidate_id'])
        (self.root / 'package.tgz').write_bytes(b'changed after approval')
        with self.assertRaisesRegex(CandidateError, 'identity'):
            verify_candidate(self.root, manifest['candidate_id'])

    def test_manifest_change_rejects_old_binding(self):
        manifest = self.candidate()
        p = self.root / 'candidate.json'
        data = json.loads(p.read_text()); data['channel'] = 'next'
        p.write_text(json.dumps(data))
        with self.assertRaises(CandidateError):
            verify_candidate(self.root, manifest['candidate_id'])

    def test_candidate_rejects_escaped_or_symlink_artifact(self):
        manifest = self.candidate()
        manifest.pop('candidate_id')
        manifest['files']['../outside'] = {'sha256': '0' * 64, 'size': 1}
        with self.assertRaisesRegex(CandidateError, 'path'):
            seal_candidate(self.root, manifest)
        manifest['files'].pop('../outside')
        (self.root / 'adapter.zip').unlink()
        (self.root / 'adapter.zip').symlink_to(self.root / 'package.tgz')
        with self.assertRaisesRegex(CandidateError, 'symlink'):
            seal_candidate(self.root, manifest)

    def test_failed_or_unknown_value_check_cannot_seal(self):
        for result in ['fail', 'pending', 'unknown_value']:
            with self.subTest(result=result):
                manifest = self.candidate(); manifest.pop('candidate_id')
                manifest['checks'][0]['result'] = result
                with self.assertRaisesRegex(CandidateError, 'check'):
                    seal_candidate(self.root, manifest)

    def test_absent_timing_is_diagnostic_but_bad_profile_is_not_ignored(self):
        p = self.root / 'docs/releases/profiles/v0.5.1.yaml'
        p.parent.mkdir(); p.write_text(profile_text('v0.5.1'))
        self.assertTrue(timing_diagnostics(self.root, 'v0.5.1'))
        p.write_text('schema_version: unknown_value\n')
        with self.assertRaises(CandidateError):
            timing_diagnostics(self.root, 'v0.5.1')

    def test_unknown_value_check_id_is_rejected(self):
        manifest = self.candidate(); manifest.pop('candidate_id')
        manifest['checks'][0]['id'] = 'unknown_value'
        with self.assertRaisesRegex(CandidateError, 'check'):
            seal_candidate(self.root, manifest)

    def test_evidence_ref_cannot_overwrite_source_branch(self):
        manifest = self.candidate(); manifest.pop('candidate_id')
        manifest['evidence_ref'] = manifest['source_ref']
        with self.assertRaisesRegex(CandidateError, 'evidence ref'):
            seal_candidate(self.root, manifest)

    def test_boolean_artifact_size_is_not_a_valid_identity(self):
        manifest = self.candidate(); manifest.pop('candidate_id')
        (self.root / 'adapter.zip').write_bytes(b'x')
        manifest['files']['adapter.zip'] = file_identity(self.root / 'adapter.zip')
        manifest['files']['adapter.zip']['size'] = True
        with self.assertRaisesRegex(CandidateError, 'identity'):
            seal_candidate(self.root, manifest)

    def test_verification_receipt_uses_portable_artifact_paths(self):
        import importlib.util
        path = Path(__file__).parent / 'validate-release.py'
        spec = importlib.util.spec_from_file_location('receipt_validator', path)
        validator = importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
        command = ['python', 'scripts/validate-npm-package.py', '--tarball', '/private/runner/candidate/package.tgz']
        recorded = validator.recorded_command(command, Path('/private/runner/source'), Path('/private/runner/candidate'))
        self.assertEqual(recorded, 'python scripts/validate-npm-package.py --tarball <candidate>/package.tgz')
        self.assertNotIn('/private', recorded)


class ReleaseCandidateIntegrationTests(unittest.TestCase):
    def test_actual_candidate_build_and_packed_metadata_chain(self):
        """TG-01/02: real builders/validators/install consumer; no publication."""
        import shutil
        import subprocess
        import tarfile
        from release_candidate import prepare_candidate
        repository = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix='release-candidate-proof-') as temporary:
            workspace = Path(temporary)
            source, output = workspace / 'source', workspace / 'release-candidate'
            subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', str(repository), str(source)], check=True)
            # Use current authored implementation, including an uncommitted test-first slice.
            for script in (repository / 'scripts').iterdir():
                if script.is_file() and script.suffix in {'.py', '.sh'}:
                    shutil.copyfile(script, source / 'scripts' / script.name)
            shutil.copyfile(repository / '.github/workflows/release.yml', source / '.github/workflows/release.yml')
            intent = source / 'docs/releases/v0.5.1.md'
            intent.write_text('# Release v0.5.1\n\n## Version Decision\n\n- Version decision: patch\n- Change summary: Reviewed candidate fixture for integrity proof.\n')
            def git(*args):
                return subprocess.check_output(['git', '-C', str(source), *args], text=True, stderr=subprocess.DEVNULL).strip()
            git('branch', '-M', 'main')
            git('add', 'scripts', 'docs/releases/v0.5.1.md', '.github/workflows/release.yml')
            git('-c', 'user.name=Release Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-m', 'Reviewed source fixture')
            commit, ref = git('rev-parse', 'HEAD'), git('symbolic-ref', 'HEAD')
            from release_coordination import prepare_operation, execute_operation, read_evidence, ExecutionError, summary
            from release_coordination_tests import FixtureHostedServices, invoke_dispatch
            remote = workspace / 'evidence.git'
            subprocess.run(['git', 'init', '--bare', '--quiet', str(remote)], check=True)
            event = {'run_id': 12, 'source_commit': commit, 'source_ref': ref, 'attempt': 1}
            settings = {'evidence_ref': 'refs/heads/release-evidence', 'trusted_publisher': 'github:xiongxianfei/rigorloop:release.yml:release'}
            services = FixtureHostedServices(event, remote)
            bad = dict(settings, trusted_publisher='')
            with self.assertRaises(ExecutionError): prepare_operation(source, output, event, bad, services)
            self.assertFalse(output.exists())
            status, errors, approval_summary, outputs = invoke_dispatch('prepare', source, services, event, workspace)
            self.assertEqual(status, 0, errors)
            self.assertIn('ready=true', outputs)
            data = json.loads((output / 'candidate.json').read_text())
            self.assertIn(data['candidate_id'], approval_summary)
            self.assertEqual(services.approval_count, 0)
            self.assertIn(data['candidate_id'], summary(data))
            binding = services.retain_and_approve(data, output)
            status, errors, outcome_summary, _ = invoke_dispatch('execute', source, services, event, workspace / 'executor', binding)
            self.assertEqual(status, 0, errors)
            self.assertIn('completed', outcome_summary)
            state = json.loads((workspace / 'executor/release-candidate/observed-outcome.json').read_text())
            self.assertEqual(state['status'], 'completed')
            self.assertEqual(state['mirror']['result'], 'copied')
            self.assertEqual(services.approval_count, 1)
            self.assertEqual(services.publisher.writes, ['tag', 'github', 'npm'])
            self.assertEqual(read_evidence(services, settings['evidence_ref'], data['tag'])['status'], 'completed')
            execute_operation(source, workspace / 'duplicate', event, settings, binding, services)
            self.assertEqual(services.publisher.writes, ['tag', 'github', 'npm'])
            self.assertEqual(services.approval_count, 1)
            services.retain_observations(workspace / 'executor/release-candidate', 1)
            retry_event = dict(event, attempt=2)
            services.facts['run']['run_attempt'] = 2
            retried = prepare_operation(source, workspace / 'restored', retry_event, settings, services)
            self.assertEqual(retried['candidate']['candidate_id'], data['candidate_id'])
            execute_operation(source, workspace / 'retry', retry_event, settings, retried['binding'], services)
            self.assertEqual(services.publisher.writes, ['tag', 'github', 'npm'])
            self.assertEqual(services.approval_count, 1)
            services.facts['run']['run_attempt'] = 1
            for scenario in ['lost-response', 'failed-smoke', 'failed-reporting', 'missing-timing-mirror']:
                case_root = workspace / scenario; case_root.mkdir()
                case_remote = case_root / 'evidence.git'
                subprocess.run(['git', 'init', '--bare', '--quiet', str(case_remote)], check=True)
                case = FixtureHostedServices(event, case_remote)
                case_binding = case.retain_and_approve(data, output)
                if scenario == 'lost-response': case.publisher.lose_response = 'npm'
                if scenario == 'failed-smoke': case.publisher.fail_smoke = True
                if scenario == 'missing-timing-mirror': case.publisher.fail_mirror = True
                if scenario == 'failed-reporting':
                    from release_execution import GitEvidence
                    class FailingStore(GitEvidence):
                        calls = 0
                        def save(self, changes):
                            self.calls += 1
                            if self.calls >= 7: raise ExecutionError('fixture reporting unavailable')
                            return super().save(changes)
                    ordinary_store = case.evidence
                    case.evidence = lambda ref, source_ref: FailingStore(str(case_remote), ref, source_ref=source_ref)
                code, error, _, _ = invoke_dispatch('execute', source, case, event, case_root / 'attempt1', case_binding)
                should_fail = scenario in ['failed-smoke', 'failed-reporting']
                self.assertEqual(code, 1 if should_fail else 0, scenario + ': ' + error)
                observed_dir = case_root / 'attempt1/release-candidate'
                observed = json.loads((observed_dir / 'observed-outcome.json').read_text())
                self.assertEqual(case.publisher.writes, ['tag', 'github', 'npm'])
                if scenario == 'missing-timing-mirror':
                    self.assertEqual(observed['status'], 'completed')
                    self.assertEqual(observed['mirror']['result'], 'unavailable')
                    self.assertEqual(observed['timing_diagnostic']['result'], 'fail')
                if should_fail:
                    case.retain_observations(observed_dir, 1)
                    case.facts['run']['run_attempt'] = 2
                    if scenario == 'failed-reporting': case.evidence = ordinary_store
                    case.publisher.fail_smoke = False
                    code, error, _, _ = invoke_dispatch('execute', source, case, retry_event, case_root / 'attempt2', case_binding)
                    self.assertEqual(code, 0, error)
                    recovered = read_evidence(case, settings['evidence_ref'], data['tag'])
                    self.assertEqual(recovered['status'], 'completed')
                    self.assertTrue(any(e['result'] == 'incomplete' for e in recovered['events']))
                    self.assertEqual(case.publisher.writes, ['tag', 'github', 'npm'])
                    self.assertEqual(case.approval_count, 1)
            services.public_version = data['version']
            self.assertEqual(prepare_operation(source, workspace / 'noop', event, settings, services)['status'], 'already-published')
            # Same version on a different reviewed commit is an upstream exception.
            git('-c', 'user.name=Release Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-m', 'Unclassified later reviewed change')
            changed_commit = git('rev-parse', 'HEAD')
            services.facts['run']['head_sha'] = changed_commit
            changed_event = dict(event, source_commit=changed_commit)
            with self.assertRaisesRegex(ExecutionError, 'next-version decision'):
                prepare_operation(source, workspace / 'changed', changed_event, settings, services)
            services.facts['run']['head_sha'] = commit
            self.assertEqual(verify_candidate(output, data['candidate_id'])['source_commit'], commit)
            self.assertEqual({x['id'] for x in data['checks']}, CANDIDATE_CHECKS)
            self.assertEqual(len(list(output.glob('*.zip'))), 3)
            with tarfile.open(output / data['tarball']) as packed:
                metadata_bytes = packed.extractfile('package/dist/metadata/adapter-artifacts-v0.5.1.json').read()
                index = json.load(packed.extractfile('package/dist/metadata/releases.json'))
                self.assertEqual(index['releases']['v0.5.1']['bundled_metadata_sha256'], hashlib.sha256(metadata_bytes).hexdigest())
                metadata = json.loads(metadata_bytes)
                self.assertEqual(metadata['release']['source_commit'], data['prepared_commit'])
                self.assertEqual(metadata['release']['published_at'], 'pending-publication')
                self.assertNotEqual(metadata['metadata']['sha256'], '0' * 64)
                for archive in metadata['artifacts']:
                    self.assertEqual(archive['sha256'], file_identity(output / archive['archive'])['sha256'])
            self.assertNotIn(str(workspace), (output / 'release-verification.json').read_text())
            self.assertIn('release-integrity', {x['id'] for x in data['checks']})
            receipt = json.loads((output / 'release-verification.json').read_text())
            self.assertTrue(any('validate-release.py' in x.get('command', '') for x in receipt['checks']))
            # Reconstruct the actual prepared source, then prove required release facts
            # and secret-bearing notes reject independently of a good npm tarball.
            checked = workspace / 'checked'
            subprocess.run(['git', 'clone', '--quiet', str(output / 'source.bundle'), str(checked)], check=True)
            import importlib.util
            spec = importlib.util.spec_from_file_location('release_validator', repository / 'scripts/validate-release.py')
            validator = importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
            metadata_path = checked / 'docs/releases/v0.5.1/release.yaml'
            before = metadata_path.read_text()
            for bad in [before.replace('  security: pending', '  security: fail'), before.replace('  security: pending\n', '')]:
                metadata_path.write_text(bad)
                self.assertTrue(validator.validate_prepared_release('v0.5.1', checked, output))
            metadata_path.write_text(before)
            notes_path = checked / 'docs/releases/v0.5.1/release-notes.md'
            notes_path.write_text(notes_path.read_text() + '\n-----BEGIN PRIVATE KEY-----\n')
            self.assertTrue(validator.validate_prepared_release('v0.5.1', checked, output))
            (output / data['tarball']).write_bytes(b'changed after checks')
            with self.assertRaisesRegex(CandidateError, 'identity'):
                verify_candidate(output, data['candidate_id'])
