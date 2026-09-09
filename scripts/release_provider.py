"""GitHub/npm boundaries for the approved Release operation.

API contracts: https://docs.github.com/en/rest/actions/workflow-runs
https://docs.github.com/en/rest/actions/artifacts
https://docs.github.com/en/rest/deployments/environments
https://docs.npmjs.com/trusted-publishers/
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request

from release_candidate import SOURCE_REPOSITORY, local_file, run
from release_execution import ExecutionError, ExternalUnavailable, public_files
from release_transaction import NetworkPublicEvidenceProvider, PublicSmokeResult


def github_json(path: str):
    if not path.startswith('repos/' + SOURCE_REPOSITORY):
        raise ExecutionError('unexpected GitHub API destination')
    headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'Cache-Control': 'no-cache'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    try:
        with urllib.request.urlopen(urllib.request.Request('https://api.github.com/' + path, headers=headers), timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise ExternalUnavailable('GitHub observation unavailable') from exc
    except (OSError, ValueError) as exc:
        raise ExternalUnavailable('GitHub observation unavailable') from exc


def public_bytes(url: str, prefix: str) -> bytes:
    if not url.startswith(prefix):
        raise ExecutionError('unexpected public download destination')
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'Cache-Control': 'no-cache'}), timeout=60) as response:
            # This is a bounded release artifact, not an arbitrary unbounded feed.
            result = response.read(256 * 1024 * 1024 + 1)
            if len(result) > 256 * 1024 * 1024:
                raise ExternalUnavailable('public release artifact exceeds supported size')
            return result
    except OSError as exc:
        raise ExternalUnavailable('public artifact is not yet observable') from exc


class GitHubApprovals:
    def artifact_bytes(self, binding: dict) -> bytes:
        from release_execution import MAX_ARTIFACT_BYTES
        identity = binding.get('artifact_id')
        if type(identity) is not int or identity <= 0:
            raise ExecutionError('invalid retained artifact identity')
        # gh handles authenticated API redirects without exposing signed URLs or
        # authorization in our reports. Binary output remains a private file.
        with tempfile.TemporaryFile() as target:
            try:
                result = subprocess.run(['gh', 'api', f'repos/{SOURCE_REPOSITORY}/actions/artifacts/{identity}/zip'],
                    stdout=target, stderr=subprocess.PIPE, timeout=120)
                if result.returncode or target.tell() > MAX_ARTIFACT_BYTES:
                    raise ExternalUnavailable('retained candidate download unavailable')
                target.seek(0)
                return target.read(MAX_ARTIFACT_BYTES + 1)
            except (OSError, subprocess.SubprocessError) as exc:
                raise ExternalUnavailable('retained candidate download unavailable') from exc

    def fetch(self, binding: dict) -> dict:
        from release_execution import APPROVAL_FIELDS
        import re
        if set(binding) != APPROVAL_FIELDS or any(type(binding[k]) is not int or binding[k] <= 0 for k in ('run_id', 'artifact_id')) or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', binding['environment']):
            raise ExecutionError('invalid approval provider request')
        base = 'repos/' + SOURCE_REPOSITORY
        environment = urllib.parse.quote(binding['environment'], safe='')
        return {'repository': github_json(base),
            'run': github_json(f"{base}/actions/runs/{binding['run_id']}"),
            'artifact': github_json(f"{base}/actions/artifacts/{binding['artifact_id']}"),
            'environment': github_json(f'{base}/environments/{environment}'),
            'approvals': github_json(f"{base}/actions/runs/{binding['run_id']}/approvals")}


class NetworkPublisher(NetworkPublicEvidenceProvider):
    def __init__(self):
        super().__init__(github_repository=SOURCE_REPOSITORY)
        self.installed = {}

    def wait_for_visibility(self, attempt: int):
        import time
        time.sleep(min(2 ** attempt, 10))

    def observe(self, boundary: str, candidate: dict):
        try:
            return self._observe(boundary, candidate)
        except (KeyError, TypeError, AttributeError, ValueError) as exc:
            if isinstance(exc, ExecutionError):
                raise
            raise ExternalUnavailable('public provider response is incomplete') from exc

    def _observe(self, boundary: str, candidate: dict):
        base = 'repos/' + SOURCE_REPOSITORY
        tag = urllib.parse.quote(candidate['tag'], safe='')
        if boundary == 'tag':
            data = github_json(f'{base}/git/ref/tags/{tag}')
            if data is None:
                return None
            obj = data['object']
            for _ in range(4):
                if obj['type'] == 'commit':
                    return {'commit': obj['sha']}
                if obj['type'] != 'tag':
                    raise ExternalUnavailable('unknown Git tag object type')
                obj = github_json(f"{base}/git/tags/{obj['sha']}")['object']
            raise ExternalUnavailable('tag cannot be resolved within supported bounds')
        if boundary == 'github':
            data = github_json(f'{base}/releases/tags/{tag}')
            if data is None:
                return None
            assets = []
            for asset in data['assets']:
                if asset['name'] not in public_files(candidate):
                    continue  # Preserve additional evidence without adopting its claims.
                prefix = f"https://github.com/{SOURCE_REPOSITORY}/releases/download/{tag}/"
                content = public_bytes(asset['browser_download_url'], prefix)
                assets.append({'name': asset['name'], 'sha256': hashlib.sha256(content).hexdigest()})
            return {'tag': data['tag_name'], 'draft': data['draft'], 'assets': assets}
        if boundary != 'npm':
            raise ExecutionError('unknown publication boundary')
        url = 'https://registry.npmjs.org/' + urllib.parse.quote(candidate['package'], safe='')
        try:
            data = json.loads(public_bytes(url, 'https://registry.npmjs.org/'))
            record = data['versions'].get(candidate['version'])
            if record is None:
                return None
            dist = record['dist']
            tarball = public_bytes(dist['tarball'], 'https://registry.npmjs.org/')
            integrity = 'sha512-' + base64.b64encode(hashlib.sha512(tarball).digest()).decode()
            if integrity != dist['integrity']:
                raise ExecutionError('registry integrity contradicts downloaded bytes')
            return {'package': record['name'], 'version': record['version'],
                'dist_tag': data['dist-tags'].get(candidate['channel']), 'integrity': integrity,
                'sha256': hashlib.sha256(tarball).hexdigest(), 'tarball': dist['tarball'],
                'published_at': data['time'][candidate['version']]}
        except (ValueError, KeyError, TypeError) as exc:
            raise ExternalUnavailable('npm publication identity is incomplete') from exc

    def publish(self, boundary: str, candidate: dict, output: Path, source: Path):
        if boundary == 'tag':
            # No force and no checkout of a mutable remote branch.
            from release_execution import GitEvidence
            with GitEvidence(f'https://github.com/{SOURCE_REPOSITORY}.git', candidate['evidence_ref'], source_ref=candidate['source_ref']) as auth:
                run(['git', 'push', f'https://github.com/{SOURCE_REPOSITORY}.git',
                     candidate['prepared_commit'] + ':refs/tags/' + candidate['tag']], source, env=auth.env)
            return
        if boundary == 'github':
            data = github_json(f"repos/{SOURCE_REPOSITORY}/releases/tags/{candidate['tag']}")
            files = public_files(candidate)
            if data is None:
                run(['gh', 'release', 'create', candidate['tag'], '--repo', SOURCE_REPOSITORY,
                     '--verify-tag', '--notes-file', str(local_file(output, 'release-notes.md')),
                     *[str(local_file(output, name)) for name in files]], source)
            else:
                present = {a['name'] for a in data['assets']}
                missing = [str(local_file(output, name)) for name in files if name not in present]
                if missing:
                    # Never clobber existing public assets; executor checked them.
                    run(['gh', 'release', 'upload', candidate['tag'], '--repo', SOURCE_REPOSITORY, *missing], source)
            return
        if boundary != 'npm':
            raise ExecutionError('unknown publication boundary')
        if os.environ.get('GITHUB_ACTIONS') != 'true' or not all(os.environ.get(k) for k in ('ACTIONS_ID_TOKEN_REQUEST_URL', 'ACTIONS_ID_TOKEN_REQUEST_TOKEN')):
            raise ExecutionError('trusted publishing credentials are unavailable')
        # Force the selected registry/OIDC path; never fall back to a token or run
        # package lifecycle scripts against an already-checked tarball.
        env = {k: v for k, v in os.environ.items() if not k.lower().startswith('npm_config_') and k not in {'NODE_AUTH_TOKEN', 'NPM_TOKEN'}}
        with tempfile.TemporaryDirectory(prefix='rigorloop-npm-config-') as temporary:
            config = Path(temporary) / 'npmrc'
            config.write_text('registry=https://registry.npmjs.org/\n')
            env['NPM_CONFIG_USERCONFIG'] = str(config)
            run(['npm', 'publish', str(local_file(output, candidate['tarball'])), '--provenance',
                 '--access', 'public', '--tag', candidate['channel'], '--registry', 'https://registry.npmjs.org/',
                 '--ignore-scripts'], Path(temporary), env=env)

    def run_public_npx_smoke(self, *, command: str, cwd: Path) -> PublicSmokeResult:
        from adapter_distribution import _normalized_tree_hash_bytes, _tree_hash_for_rows
        with tempfile.TemporaryDirectory(prefix='rigorloop-fresh-npx-') as cache:
            env = dict(os.environ, npm_config_cache=cache, npm_config_yes='true', npm_config_registry='https://registry.npmjs.org/')
            result = subprocess.run(command.split(), cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
        target = command.split()[-1]
        code = result.returncode
        if target == 'version':
            expected = command.split()[1].rsplit('@', 1)
            if result.stdout.strip() != expected[0] + ' ' + expected[1]:
                code = 1
            summary = expected[0] + ' ' + expected[1] if code == 0 else 'public version smoke failed'
        else:
            from release_transaction import _target_install_roots
            for relative in _target_install_roots(target):
                root = cwd / relative
                if root.is_symlink() or not root.is_dir() or not root.resolve().is_relative_to(cwd.resolve()):
                    code = 1
                    continue
                rows = []
                for path in sorted(root.rglob('*')):
                    if path.is_symlink():
                        code = 1
                    elif path.is_file():
                        name = path.relative_to(root).as_posix()
                        rows.append((name, hashlib.sha256(_normalized_tree_hash_bytes(name, path.read_bytes())).hexdigest()))
                self.installed[relative] = {'tree_sha256': _tree_hash_for_rows(rows), 'file_count': len(rows)}
            summary = 'public init ' + target + (' completed' if code == 0 else ' failed')
        return PublicSmokeResult(command, code, result.stdout, '', summary)

    def verify_smoke_identity(self, candidate: dict, output: Path):
        metadata = json.loads((output / f"adapter-artifacts-{candidate['tag']}.json").read_text())
        for artifact in metadata['artifacts']:
            if 'install_roots' in artifact:
                for key, root in artifact['install_roots'].items():
                    if self.installed.get(root) != artifact['root_hashes'][key]:
                        raise ExecutionError('public installed tree differs from approved archive')
            elif self.installed.get(artifact['install_root']) != {'tree_sha256': artifact['tree_sha256'], 'file_count': artifact['file_count']}:
                raise ExecutionError('public installed tree differs from approved archive')
