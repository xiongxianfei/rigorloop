"""Hosted composition and setup regressions; real complete path joins M1 proof."""
import copy
import unittest
from pathlib import Path
from release_coordination import validate_setup, validate_workflow, runtime_credentials
from release_execution_tests import ReleaseApprovalTests
from release_execution import ExecutionError

ROOT = Path(__file__).resolve().parents[1]

class ReleaseCoordinationTests(unittest.TestCase):
    def setUp(self):
        fixture = ReleaseApprovalTests(); fixture.setUp()
        self.facts = fixture.facts
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

    def test_evidence_mirror_reuses_exact_bytes_and_rejects_conflict(self):
        from release_provider import NetworkPublisher
        from unittest.mock import patch
        candidate, commit, payload = {'tag': 'v0.5.1'}, 'd' * 40, b'exact evidence zip fixture'
        name = 'release-evidence-' + commit + '.zip'
        release = {'assets': [{'name': name, 'browser_download_url': 'https://github.com/xiongxianfei/rigorloop/releases/download/v0.5.1/' + name}]}
        with patch('release_provider.github_json', return_value=release), patch('release_provider.public_bytes', return_value=payload), patch('release_provider.run') as command:
            NetworkPublisher().mirror_evidence(candidate, commit, payload)
            command.assert_not_called()
        with patch('release_provider.github_json', return_value=release), patch('release_provider.public_bytes', return_value=b'conflict'), patch('release_provider.run') as command:
            with self.assertRaises(ExecutionError): NetworkPublisher().mirror_evidence(candidate, commit, payload)
            command.assert_not_called()

    def test_missing_retry_observations_require_explicit_recovery(self):
        from release_coordination import restore_recovery
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


class FixtureHostedServices:
    """Only provider effects substituted; caller uses real coordinator and checks."""
    def __init__(self, event, remote):
        from release_execution_tests import FixtureApprovals
        baseline = ReleaseCoordinationTests(); baseline.setUp()
        self.event, self.remote = event, remote
        self.facts = baseline.facts
        self.facts['run'].update(id=event['run_id'], head_sha=event['source_commit'], run_attempt=event['attempt'])
        self.facts['artifact']['workflow_run'].update(id=event['run_id'], head_sha=event['source_commit'])
        self.facts['approvals'] = []
        class ArtifactService(FixtureApprovals):
            payloads = None
            def artifact_bytes(self, binding):
                return self.payloads.get(binding['artifact_id'], self.payload)
        self.approvals = ArtifactService(self.facts)
        self.approvals.payloads = {}
        self.approval_count = 0
        self.retained = []
        self.public_version = '0.5.0'

    def setup(self, event): return copy.deepcopy(self.facts)
    def latest(self): return self.public_version
    def artifacts(self, event): return copy.deepcopy(self.retained)
    def credentials(self): pass  # Substituted runtime service; negative checked separately.
    def evidence(self, ref, source_ref):
        from release_execution import GitEvidence
        return GitEvidence(str(self.remote), ref, source_ref=source_ref)

    def retain_and_approve(self, candidate, output):
        import io, zipfile, hashlib
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            for path in output.iterdir(): archive.write(path, path.name)
        self.approvals.payload = stream.getvalue()
        digest = 'sha256:' + hashlib.sha256(stream.getvalue()).hexdigest()
        artifact = self.facts['artifact']
        artifact.update(digest=digest, name='release-candidate-' + str(self.event['run_id']))
        self.retained = [artifact]
        self.facts['approvals'] = [{'state': 'approved', 'environments': [{'id': 9, 'name': 'release'}], 'user': {'id': 2}}]
        self.approval_count += 1
        self.publisher = PackedPublicFixture(candidate, output)
        return {'run_id': self.event['run_id'], 'artifact_id': artifact['id'], 'artifact_digest': digest,
            'candidate_id': candidate['candidate_id'], 'environment': 'release', 'artifact_name': artifact['name']}

    def retain_observations(self, output, attempt):
        import io, zipfile, hashlib
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as archive:
            archive.write(output / 'observed-outcome.json', 'observed-outcome.json')
        artifact_id = 100 + attempt
        self.approvals.payloads[artifact_id] = data.getvalue()
        self.retained.append({'id': artifact_id, 'name': f"release-observation-{self.event['run_id']}-{attempt}",
            'digest': 'sha256:' + hashlib.sha256(data.getvalue()).hexdigest(), 'expired': False})


from release_execution_tests import FixturePublisher
class PackedPublicFixture(FixturePublisher):
    """Registry/npx transport points at the actual tarball and archive bytes."""
    def mirror_evidence(self, candidate, commit, payload):
        import zipfile, io
        if getattr(self, 'fail_mirror', False): raise ExecutionError('fixture mirror unavailable')
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            if f"docs/releases/{candidate['tag']}.md" not in archive.namelist():
                raise ExecutionError('fixture mirror lacks standing evidence')
        self.mirrored = {'commit': commit, 'bytes': payload}

    def run_public_npx_smoke(self, *, command, cwd):
        import tempfile, subprocess, hashlib
        from release_transaction import PublicSmokeResult, _target_install_roots
        from adapter_distribution import _tree_hash_for_rows, _normalized_tree_hash_bytes
        target = command.split()[-1]
        if self.fail_smoke:
            # Still execute the real package: ask its actual CLI to reject an
            # unsupported command, observing the failed external smoke result.
            target = 'unsupported-smoke-command'
        with tempfile.TemporaryDirectory() as temporary:
            install = Path(temporary)
            subprocess.run(['npm', 'install', '--ignore-scripts', '--no-audit', '--no-fund', '--prefix', str(install),
                str(self.output / self.candidate['tarball'])], check=True, capture_output=True)
            cli = install / 'node_modules/@xiongxianfei/rigorloop/dist/bin/rigorloop.js'
            args = ['version'] if target == 'version' else [target] if self.fail_smoke else ['init', target, '--from-archive', str(self.output / f'rigorloop-adapter-{target}-{self.candidate["tag"]}.zip')]
            result = subprocess.run(['node', str(cli), *args], cwd=cwd, text=True, capture_output=True)
        if target != 'version' and result.returncode == 0:
            for name in _target_install_roots(target):
                root = cwd / name
                rows = [(p.relative_to(root).as_posix(), hashlib.sha256(_normalized_tree_hash_bytes(p.name, p.read_bytes())).hexdigest()) for p in root.rglob('*') if p.is_file()]
                self.installed[name] = {'tree_sha256': _tree_hash_for_rows(rows), 'file_count': len(rows)}
        return PublicSmokeResult(command, result.returncode, result.stdout, '', 'actual packed CLI ' + target + ' through substituted public transport')


def invoke_dispatch(operation, source, services, event, workspace, binding=None):
    """Drive the production argparse/environment/output path with provider fixtures."""
    import importlib.util, os, io, contextlib
    from unittest.mock import patch
    workspace.mkdir(parents=True, exist_ok=True)
    output, summary_file = workspace / 'outputs', workspace / 'summary'
    environment = {'GITHUB_ACTIONS': 'true', 'GITHUB_RUN_ID': str(event['run_id']),
        'GITHUB_RUN_ATTEMPT': str(event['attempt']), 'GITHUB_SHA': event['source_commit'],
        'GITHUB_REF': event['source_ref'], 'GITHUB_REF_TYPE': 'branch', 'GITHUB_REF_NAME': 'main',
        'RUNNER_TEMP': str(workspace), 'GITHUB_OUTPUT': str(output), 'GITHUB_STEP_SUMMARY': str(summary_file),
        'RELEASE_EVIDENCE_REF': 'refs/heads/release-evidence',
        'RELEASE_TRUSTED_PUBLISHER': 'github:xiongxianfei/rigorloop:release.yml:release'}
    if binding:
        environment.update(RELEASE_CANDIDATE_ID=binding['candidate_id'], RELEASE_ARTIFACT_ID=str(binding['artifact_id']),
            RELEASE_ARTIFACT_DIGEST=binding['artifact_digest'])
    spec = importlib.util.spec_from_file_location('actual_release_dispatch', ROOT / 'scripts/release-coordinator.py')
    cli = importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)
    errors = io.StringIO()
    with patch.dict(os.environ, environment), contextlib.redirect_stderr(errors):
        status = cli.main([operation], services=services, root=source)
    return status, errors.getvalue(), summary_file.read_text() if summary_file.exists() else '', output.read_text() if output.exists() else ''
