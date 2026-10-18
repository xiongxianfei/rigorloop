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

from lib.release.release_execution import ExecutionError, GitEvidence, validate_authority, environment_identity

from release_fixture_helpers import authority_fixture

from release_provider_fixtures import FixtureReleaseAuthority, FixturePublisher

class ReleaseAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.candidate, self.binding, self.facts = authority_fixture()

    def test_exact_workflow_authority_binds_candidate_without_reviewer(self):
        result = validate_authority(self.candidate, self.binding, self.facts)
        self.assertEqual(result['candidate_id'], self.candidate['candidate_id'])
        self.assertEqual(result['policy'], 'workflow-start-v1')

    def test_unknown_value_authority_field_rejects_before_consistency(self):
        accepted = validate_authority(self.candidate, self.binding, self.facts)
        self.assertEqual(accepted['candidate_id'], self.candidate['candidate_id'])
        self.assertEqual(accepted['policy'], 'workflow-start-v1')
        candidate, facts = copy.deepcopy(self.candidate), copy.deepcopy(self.facts)
        binding = dict(self.binding, unknown_value='must-not-be-retained', candidate_id='f' * 64)
        self.assertNotEqual(binding['candidate_id'], candidate['candidate_id'])
        before = copy.deepcopy(binding)
        with self.assertRaises(ExecutionError) as raised:
            validate_authority(candidate, binding, facts)
        self.assertEqual(str(raised.exception), 'unknown or missing authority binding field')
        self.assertEqual(binding, before)
        binding.pop('unknown_value')
        with self.assertRaises(ExecutionError) as raised:
            validate_authority(candidate, binding, facts)
        self.assertEqual(str(raised.exception), 'authority candidate mismatch')
        self.assertEqual(candidate, self.candidate)
        self.assertEqual(facts, self.facts)

    def test_unsupported_trigger_and_different_start_cannot_publish(self):
        for event in ['pull_request', 'workflow_dispatch', 'push_tag', 'unknown_value']:
            facts = copy.deepcopy(self.facts); facts['run']['event'] = event
            with self.subTest(event=event), self.assertRaises(ExecutionError):
                validate_authority(self.candidate, self.binding, facts)
        for initiation in [None, {'policy': 'unknown_value', 'run_id': 12},
                           {'policy': 'workflow-start-v1', 'run_id': 99}]:
            candidate = dict(self.candidate, initiation=initiation)
            with self.subTest(initiation=initiation), self.assertRaises(ExecutionError):
                validate_authority(candidate, self.binding, self.facts)

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
        prepare_release('v0.5.1', root=self.source, workflow_driven=True)
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
        _, self.binding, self.facts = authority_fixture()
        self.facts['run']['head_sha'] = original
        self.facts['artifact']['workflow_run']['head_sha'] = original
        self.candidate = seal_candidate(self.output, {'source_commit': original, 'prepared_commit': commit,
            'source_ref': 'refs/heads/main', 'version': '0.5.1', 'tag': 'v0.5.1', 'package': '@xiongxianfei/rigorloop',
            'channel': 'latest', 'repository': 'xiongxianfei/rigorloop', 'publication_path': 'trusted-publishing',
            'evidence_ref': 'refs/heads/release-evidence', 'inputs': inputs, 'tarball': 'package.tgz',
            'files': {p.name: file_identity(p) for p in self.output.iterdir()},
            'checks': [{'id': key, 'result': 'pass'} for key in sorted(CANDIDATE_CHECKS)],
            'release_environment_identity': environment_identity(self.facts['environment']),
            'initiation': {'policy': 'workflow-start-v1', 'run_id': self.binding['run_id']},
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
        self.authorities = FixtureReleaseAuthority(self.facts, self.payload)
        self.publisher = FixturePublisher(self.candidate, self.output)

    def execute(self, store=None, *, attempt=None):
        from lib.release.release_execution import execute_candidate
        if store is not None:
            return execute_candidate(self.output, self.binding, attempt=self.facts['run']['run_attempt'] if attempt is None else attempt, authorities=self.authorities, publisher=self.publisher, evidence=store)
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            return self.execute(evidence, attempt=attempt)

    def stored(self):
        from lib.release.release_execution import read_execution_state
        with GitEvidence(str(self.remote), self.candidate['evidence_ref']) as evidence:
            evidence.refresh()
            return read_execution_state(evidence.read('docs/releases/v0.5.1.md'))




    def test_one_start_path_persists_and_duplicate_never_republishes(self):
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

    def test_failed_smoke_preserves_publication_and_retry_only_observes(self):
        self.publisher.fail_smoke = True
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.stored()['status'], 'failed-after-publication')
        self.publisher.fail_smoke = False
        self.execute()
        self.assertEqual(self.publisher.writes, ['tag', 'github', 'npm'])
        self.assertTrue(any(e['result'] == 'incomplete' for e in self.stored()['events']))

    def test_candidate_tamper_and_cancelled_run_cause_no_external_writes(self):
        self.facts['run']['status'] = 'completed'
        with self.assertRaises(ExecutionError): self.execute()
        self.assertEqual(self.publisher.writes, [])
        self.facts['run']['status'] = 'in_progress'
        (self.output / 'package.tgz').write_bytes(b'tampered')
        from lib.release.release_candidate import CandidateError
        with self.assertRaises(CandidateError): self.execute()
        self.assertEqual(self.publisher.writes, [])
