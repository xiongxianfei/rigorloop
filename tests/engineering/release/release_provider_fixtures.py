"""Controlled external service fixtures; real execution and persistence remain in the callers."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import GitHubReleaseAsset, NpmPackageMetadata, PublicEvidenceUnavailable, PublicSmokeResult
import copy
from lib.release.release_execution import ExecutionError
from lib.release.release_provider import NetworkPublisher


class RecordingPublicEvidenceProvider:
    def __init__(
        self,
        *,
        fail_github: bool = False,
        fail_npm: bool = False,
        fail_smoke_command: str | None = None,
        github_assets: tuple[GitHubReleaseAsset, ...] | None = None,
        npm_metadata: NpmPackageMetadata | None = None,
    ) -> None:
        self.fail_github = fail_github
        self.fail_npm = fail_npm
        self.fail_smoke_command = fail_smoke_command
        self.github_calls: list[str] = []
        self.npm_calls: list[tuple[str, str]] = []
        self.smoke_calls: list[str] = []
        self.github_assets = github_assets or (
            GitHubReleaseAsset(
                name="rigorloop-adapter-codex-v0.3.5.zip",
                url="https://provider.example/releases/codex-provider.zip",
                size=123,
                sha256="provider-codex-archive",
            ),
            GitHubReleaseAsset(
                name="rigorloop-adapter-claude-v0.3.5.zip",
                url="https://provider.example/releases/claude-provider.zip",
                size=124,
                sha256="sha256:provider-claude-archive",
            ),
        )
        self.npm_metadata = npm_metadata or NpmPackageMetadata(
            package="@xiongxianfei/rigorloop",
            version="0.3.5",
            tarball_url="https://registry.provider.example/rigorloop-0.3.5.tgz",
            integrity="sha512-provider-integrity",
            shasum="provider-shasum",
            published_at="2026-06-29T00:00:00Z",
        )

    def fetch_github_release_assets(self, *, tag: str) -> tuple[GitHubReleaseAsset, ...]:
        self.github_calls.append(tag)
        if self.fail_github:
            raise PublicEvidenceUnavailable(f"GitHub release asset metadata not found for {tag}")
        return self.github_assets

    def fetch_npm_package_metadata(self, *, package: str, version: str) -> NpmPackageMetadata:
        self.npm_calls.append((package, version))
        if self.fail_npm:
            raise PublicEvidenceUnavailable(f"npm metadata for {package}@{version} not available")
        return self.npm_metadata

    def run_public_npx_smoke(self, *, command: str, cwd: Path) -> PublicSmokeResult:
        self.smoke_calls.append(command)
        if command == self.fail_smoke_command:
            return PublicSmokeResult(
                command=command,
                exit_code=1,
                stdout="",
                stderr="smoke failed",
                summary="smoke failed",
            )
        target = command.split()[-1]
        if command.endswith(" version"):
            stdout = "0.3.5\n"
            summary = "0.3.5"
        else:
            stdout = (
                f"created {target} adapter\n"
                f"tree_hashes=sha256:provider-{target}-tree\n"
                "file_counts=12\n"
            )
            summary = f"created {target} adapter"
        return PublicSmokeResult(
            command=command,
            exit_code=0,
            stdout=stdout,
            stderr="",
            summary=summary,
        )

class FixtureApprovals:
    def __init__(self, facts, payload=b''): self.facts, self.payload = facts, payload
    def artifact_bytes(self, binding): return self.payload
    def fetch(self, binding): return copy.deepcopy(self.facts)


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
        from lib.release.release_execution import ExternalUnavailable
        if self.unknown == boundary: raise ExternalUnavailable('fixture unavailable')
        return copy.deepcopy(self.states[boundary])

    def publish(self, boundary, candidate, output, source):
        import hashlib, base64
        from lib.release.release_execution import public_files, ExternalUnavailable
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
        from lib.release.release_transaction import GitHubReleaseAsset
        return tuple(GitHubReleaseAsset(name=a['name'], url=f'https://github.com/xiongxianfei/rigorloop/releases/download/{tag}/{a["name"]}',
            size=self.candidate['files'][a['name']]['size'], sha256='sha256:' + a['sha256']) for a in self.states['github']['assets'] if a['name'].endswith('.zip'))

    def fetch_npm_package_metadata(self, *, package, version):
        from lib.release.release_transaction import NpmPackageMetadata
        state = self.states['npm']
        return NpmPackageMetadata(package=package, version=version, tarball_url=state['tarball'], integrity=state['integrity'], published_at=state['published_at'])

    def run_public_npx_smoke(self, *, command, cwd):
        import zipfile, hashlib
        from lib.release.release_transaction import PublicSmokeResult, _target_install_roots
        from lib.packaging.adapter_distribution import _normalized_tree_hash_bytes
        if self.fail_smoke: return PublicSmokeResult(command, 1, '', '', 'fixture smoke failed')
        target = command.split()[-1]
        if target != 'version':
            with zipfile.ZipFile(self.output / f'rigorloop-adapter-{target}-{self.candidate["tag"]}.zip') as archive:
                archive.extractall(cwd)  # Trusted test-created archive, not a production loader.
            for name in _target_install_roots(target):
                root = cwd / name
                rows = [(p.relative_to(root).as_posix(), hashlib.sha256(_normalized_tree_hash_bytes(p.name, p.read_bytes())).hexdigest()) for p in root.rglob('*') if p.is_file() and not p.is_symlink()]
                self.record_installed_rows(name, rows)
        return PublicSmokeResult(command, 0, '@xiongxianfei/rigorloop ' + self.candidate['version'], '', 'fixture public ' + target + ' completed')
