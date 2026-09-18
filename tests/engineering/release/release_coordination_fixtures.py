"""Explicit provider transport and real packed-command fixtures for coordination."""

from __future__ import annotations

import sys
from pathlib import Path
import contextlib
import io
import tempfile
import os
import subprocess

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import PublicSmokeResult
import copy
from release_fixture_helpers import approval_fixture
from lib.release.release_execution import ExecutionError


class FixtureHostedServices:
    """Only provider effects substituted; caller uses real coordinator and checks."""
    def __init__(self, event, remote):
        from release_provider_fixtures import FixtureApprovals
        self.event, self.remote = event, remote
        _, _, self.facts = approval_fixture()
        self.facts['branch'] = {'name': 'main', 'protected': True}
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
        from lib.release.release_execution import GitEvidence
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


from release_provider_fixtures import FixturePublisher
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
        from lib.release.release_transaction import PublicSmokeResult, _target_install_roots
        from lib.packaging.adapter_distribution import _normalized_tree_hash_bytes
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
                rows = [(p.relative_to(root).as_posix(), hashlib.sha256(_normalized_tree_hash_bytes(p.name, p.read_bytes())).hexdigest()) for p in root.rglob('*') if p.is_file() and not p.is_symlink()]
                self.record_installed_rows(name, rows)
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
