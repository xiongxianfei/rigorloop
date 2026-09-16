"""Hosted composition and setup regressions; real complete path joins M1 proof."""
import copy
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_coordination import validate_setup, validate_workflow, runtime_credentials
from release_fixture_helpers import approval_fixture
from lib.release.release_execution import ExecutionError


class ReleaseCoordinationTests(unittest.TestCase):
    def setUp(self):
        _, _, self.facts = approval_fixture()
        self.facts['branch'] = {'name': 'main', 'protected': True}
        self.settings = {'evidence_ref': 'refs/heads/release-evidence',
            'trusted_publisher': 'github:xiongxianfei/rigorloop:release.yml:release'}
        self.event = {'run_id': 12, 'source_commit': 'b' * 40, 'source_ref': 'refs/heads/main', 'attempt': 1}

    def test_supported_setup_has_explicit_inspected_and_unobservable_boundary(self):
        result = validate_setup(self.facts, self.settings, self.event)
        self.assertEqual(result['environment'], 'release')
        self.assertEqual(result['npm_configuration'], 'declared; runtime authorization required')

    def test_missing_or_unprotected_setup_cannot_request_approval(self):
        for field in ['environment', 'branch', 'run']:
            facts = copy.deepcopy(self.facts); facts.pop(field)
            with self.assertRaises(ExecutionError): validate_setup(facts, self.settings, self.event)
        for key, value in [('evidence_ref', 'refs/heads/main'), ('trusted_publisher', ''), ('unknown_value', True)]:
            settings = dict(self.settings, **{key: value})
            with self.assertRaises(ExecutionError): validate_setup(self.facts, settings, self.event)
        self.facts['branch']['protected'] = False
        with self.assertRaises(ExecutionError): validate_setup(self.facts, self.settings, self.event)

    def test_missing_runtime_oidc_stops_before_any_publication(self):
        with self.assertRaises(ExecutionError): runtime_credentials({'GITHUB_ACTIONS': 'true'})
        runtime_credentials({'GITHUB_ACTIONS': 'true', 'GH_TOKEN': 'fixture',
            'ACTIONS_ID_TOKEN_REQUEST_URL': 'fixture', 'ACTIONS_ID_TOKEN_REQUEST_TOKEN': 'fixture'})

    def test_actual_cli_does_not_report_private_filesystem_errors(self):
        import importlib.util, io, tempfile, contextlib, os
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('release_dispatcher', ROOT / 'scripts/release-coordinator.py')
        cli = importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)
        class FailedStorage:
            def evidence(self, *args): raise PermissionError(13, 'Permission denied', '/private/worker/user/release-secret')
        with tempfile.TemporaryDirectory() as temporary:
            summary = Path(temporary) / 'summary'; error = io.StringIO()
            with patch.dict(os.environ, {'RELEASE_EVIDENCE_REF': 'refs/heads/release-evidence', 'GITHUB_STEP_SUMMARY': str(summary)}), contextlib.redirect_stderr(error):
                self.assertEqual(cli.main(['read-evidence', '--tag', 'v0.5.1'], services=FailedStorage()), 1)
            self.assertNotIn('/private/worker', error.getvalue() + summary.read_text())

    def test_actual_ci_dispatch_does_not_report_private_diagnostics(self):
        import importlib.util, io, contextlib
        from unittest.mock import patch
        from lib.release.release_candidate import CandidateError
        spec = importlib.util.spec_from_file_location('release_dispatcher', ROOT / 'scripts/release-coordinator.py')
        cli = importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)
        for failure in [OSError('/private/worker/credential-file unavailable'),
                        FileNotFoundError(2, 'missing file', '/private/worker/credential-file'),
                        CandidateError('check failed; private diagnostic log: /private/worker/check.log'),
                        KeyError('candidate_id'), TypeError('wrong object'), AttributeError('wrong shape')]:
            error = io.StringIO()
            with self.subTest(failure=type(failure).__name__), patch('lib.release.release_candidate.check_ci', side_effect=failure), contextlib.redirect_stderr(error):
                self.assertEqual(cli.main(['check-ci', '--mode', 'main']), 1)
            self.assertNotIn('/private/worker', error.getvalue())
            self.assertIn('CI release preparation stopped:', error.getvalue())
            if isinstance(failure, OSError) and failure.errno == 2:
                self.assertIn('OS error 2', error.getvalue())

    def test_evidence_mirror_reuses_exact_bytes_and_rejects_conflict(self):
        from lib.release.release_provider import NetworkPublisher
        from unittest.mock import patch
        candidate, commit, payload = {'tag': 'v0.5.1'}, 'd' * 40, b'exact evidence zip fixture'
        name = 'release-evidence-' + commit + '.zip'
        release = {'assets': [{'name': name, 'browser_download_url': 'https://github.com/xiongxianfei/rigorloop/releases/download/v0.5.1/' + name}]}
        with patch('lib.release.release_provider.github_json', return_value=release), patch('lib.release.release_provider.public_bytes', return_value=payload), patch('lib.release.release_provider.run') as command:
            NetworkPublisher().mirror_evidence(candidate, commit, payload)
            command.assert_not_called()
        with patch('lib.release.release_provider.github_json', return_value=release), patch('lib.release.release_provider.public_bytes', return_value=b'conflict'), patch('lib.release.release_provider.run') as command:
            with self.assertRaises(ExecutionError): NetworkPublisher().mirror_evidence(candidate, commit, payload)
            command.assert_not_called()

    def test_missing_retry_observations_require_explicit_recovery(self):
        from lib.release.release_coordination import restore_recovery
        class EmptyArtifacts:
            def artifacts(self, event): return []
        with self.assertRaisesRegex(ExecutionError, 'observation artifact unavailable'):
            restore_recovery(Path('/unused'), EmptyArtifacts(), dict(self.event, attempt=2), {})

    def test_actual_workflow_has_one_protected_executor_and_no_tag_bypass(self):
        self.assertEqual(validate_workflow(ROOT), [])

    def test_unknown_workflow_job_or_unguarded_write_rejects(self):
        import tempfile
        original = (ROOT / '.github/workflows/release.yml').read_text()
        for bad in [original.replace('environment: release', 'environment: unprotected'),
                    original + '\n  unsafe:\n    steps:\n      - run: npm publish\n']:
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary); path = root / '.github/workflows/release.yml'; path.parent.mkdir(parents=True)
                path.write_text(bad)
                self.assertTrue(validate_workflow(root))
