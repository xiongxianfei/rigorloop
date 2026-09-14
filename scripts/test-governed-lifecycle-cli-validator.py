#!/usr/bin/env python3
"""The repository wrapper uses current discovery, including its failure boundary."""
import io
import json
import runpy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(Path(__file__).with_name("validate-governed-lifecycle-cli.py")))


class CurrentRecordDiscoveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "docs/changes").mkdir(parents=True)

    def run_check(self, **kwargs):
        output = io.StringIO()
        code = MODULE["main"](root=self.root, output=output, **kwargs)
        return code, json.loads(output.getvalue())

    def test_archive_is_excluded_and_current_set_validates_without_activation(self):
        archive = self.root / "docs/changes/old/change.yaml"
        archive.parent.mkdir()
        archive.write_bytes(b"malformed archived bytes\xff")
        fixture = json.loads((ROOT / "tests/fixtures/rigorloop-records-v3/records.json").read_text())["change"]
        fixture.update(records=[], applicability=[], blockers=[])
        target = self.root / "docs/changes/example/change.json"
        target.parent.mkdir()
        target.write_text(json.dumps(fixture) + "\n")
        code, report = self.run_check()
        self.assertEqual(code, 0, report)
        self.assertEqual(report["context"]["scope"]["candidate_count"], 1)
        self.assertEqual(report["context"]["scope"]["excluded_noncurrent"], 1)
        self.assertEqual(archive.read_bytes(), b"malformed archived bytes\xff")

    def test_invalid_current_residue_does_not_become_an_archive(self):
        target = self.root / "docs/changes/example/evidence.json"
        target.parent.mkdir()
        target.write_text("{}\n")
        code, report = self.run_check()
        self.assertEqual(code, 1)
        self.assertFalse(report["context"]["scope"]["complete"])

    def test_unavailable_malformed_and_incomplete_results_fail(self):
        for result in (SimpleNamespace(returncode=1, stdout=""), SimpleNamespace(returncode=0, stdout='{}'), SimpleNamespace(returncode=0, stdout='{"schema_version":2,"command":"workflow-context","status":"success","scope":{"complete":false}}')):
            with self.subTest(result=result):
                self.assertEqual(self.run_check(runner=lambda *a, **k: result)[0], 1)





class CurrentRecordSnapshotTests(unittest.TestCase):
    def test_exact_snapshot_preserves_archive_and_ignores_later_worktree_corruption(self):
        import subprocess
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
            git('init', '-q')
            git('config', 'user.email', 'test@example.invalid')
            git('config', 'user.name', 'Test')
            fixture = json.loads((ROOT / 'tests/fixtures/rigorloop-records-v3/records.json').read_text())['change']
            fixture.update(records=[], applicability=[], blockers=[])
            path = root / 'docs/changes/example/change.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(fixture) + '\n')
            archive = root / 'docs/changes/archive/change.yaml'
            archive.parent.mkdir()
            archive.write_bytes(b'private archived bytes\xff')
            git('add', '.')
            git('commit', '-qm', 'valid records')
            revision = git('rev-parse', 'HEAD')
            path.write_text('{}\n')
            output = io.StringIO()
            self.assertEqual(MODULE['main'](root=root, output=output, revision=revision), 0, output.getvalue())
            self.assertEqual(json.loads(output.getvalue())['snapshot']['validated'], 1)
            nested = root / 'nested'; nested.mkdir()
            self.assertEqual(MODULE['main'](root=nested, output=io.StringIO(), revision=revision), 1)
            for script, args in [('classify-record-store.mjs', [str(nested), 'example', revision]), ('validate-record-store.mjs', [str(nested / 'docs/changes/example/change.json'), '--revision', revision])]:
                self.assertNotEqual(subprocess.run(['node', str(ROOT / 'scripts' / script), *args], capture_output=True).returncode, 0)
            self.assertEqual(archive.read_bytes(), b'private archived bytes\xff')
            git('add', '.')
            git('commit', '-qm', 'invalid current')
            output = io.StringIO()
            self.assertEqual(MODULE['main'](root=root, output=output, revision=git('rev-parse', 'HEAD')), 1)
            bad = git('rev-parse', 'HEAD')
            git('replace', bad, revision)
            for script, args in [('classify-record-store.mjs', [str(root), 'example', bad]), ('validate-record-store.mjs', [str(path), '--revision', bad])]:
                result = subprocess.run(['node', str(ROOT / 'scripts' / script), *args], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
            git('replace', '-d', bad)
            path.write_text(json.dumps(fixture) + '\n')
            (root / 'docs/changes/alias').symlink_to(root / 'docs/changes/example', target_is_directory=True)
            git('add', '.')
            git('commit', '-qm', 'unsafe stored directory')
            self.assertEqual(MODULE['main'](root=root, output=io.StringIO(), revision=git('rev-parse', 'HEAD')), 1)
            for revision in ('HEAD', 'unknown_value', 'a' * 40):
                self.assertEqual(MODULE['main'](root=root, output=io.StringIO(), revision=revision), 1)

    def test_snapshot_ignores_git_replacements_redirects_and_trace_writes(self):
        import os
        import subprocess
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
            git('init', '-q'); git('config', 'user.email', 'test@example.invalid'); git('config', 'user.name', 'Test')
            (root / 'README.md').write_text('good')
            git('add', '.'); git('commit', '-qm', 'good')
            good = git('rev-parse', 'HEAD')
            path = root / 'docs/changes/bad/change.json'
            path.parent.mkdir(parents=True); path.write_text('{}\n')
            git('add', '.'); git('commit', '-qm', 'bad')
            bad = git('rev-parse', 'HEAD')
            git('replace', bad, good)
            trace = root / 'must-not-write-trace'
            with patch.dict(os.environ, {'GIT_TRACE2_EVENT': str(trace)}):
                self.assertEqual(MODULE['main'](root=root, output=io.StringIO(), revision=bad), 1)
            self.assertFalse(trace.exists())
            git('replace', '-d', bad)
            other = root / 'other'; other.mkdir()
            subprocess.run(['git', 'init', '-q', str(other)], check=True)
            for key, value in [('user.email', 'test@example.invalid'), ('user.name', 'Test')]:
                subprocess.run(['git', '-C', str(other), 'config', key, value], check=True)
            (other / 'README.md').write_text('different source')
            subprocess.run(['git', '-C', str(other), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(other), 'commit', '-qm', 'other'], check=True)
            foreign = subprocess.check_output(['git', '-C', str(other), 'rev-parse', 'HEAD'], text=True).strip()
            with patch.dict(os.environ, {'GIT_DIR': str(other / '.git'), 'GIT_WORK_TREE': str(other)}):
                self.assertEqual(MODULE['main'](root=root, output=io.StringIO(), revision=foreign), 1)

    def test_missing_snapshot_object_does_not_lazy_fetch_or_write_repository(self):
        import shutil
        import subprocess
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            root = parent / 'source'; root.mkdir()
            def git(where, *args):
                return subprocess.check_output(['git', '-C', str(where), *args], text=True, stderr=subprocess.DEVNULL).strip()
            git(root, 'init', '-q'); git(root, 'config', 'user.email', 'test@example.invalid'); git(root, 'config', 'user.name', 'Test')
            fixture = json.loads((ROOT / 'tests/fixtures/rigorloop-records-v3/records.json').read_text())['change']
            fixture.update(records=[], applicability=[], blockers=[])
            path = root / 'docs/changes/example/change.json'
            path.parent.mkdir(parents=True); path.write_text(json.dumps(fixture) + '\n')
            git(root, 'add', '.'); git(root, 'commit', '-qm', 'current')
            revision = git(root, 'rev-parse', 'HEAD')
            blob = git(root, 'rev-parse', 'HEAD:docs/changes/example/change.json')
            remote = parent / 'remote.git'
            subprocess.run(['git', 'clone', '--bare', '-q', str(root), str(remote)], check=True)
            git(remote, 'config', 'uploadpack.allowAnySHA1InWant', 'true')
            for key, value in [('remote.origin.url', str(remote)), ('remote.origin.promisor', 'true'), ('core.repositoryformatversion', '1'), ('extensions.partialClone', 'origin')]:
                git(root, 'config', key, value)
            object_path = root / '.git/objects' / blob[:2] / blob[2:]
            object_path.unlink()
            control = parent / 'control'; shutil.copytree(root, control)
            # This owned partial repository would fetch the missing object without
            # the read-only snapshot boundary; establish the fixture's hazard.
            self.assertTrue(git(control, 'cat-file', 'blob', blob))
            def files():
                return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            before = files()
            self.assertEqual(MODULE['main'](root=root, output=io.StringIO(), revision=revision), 1)
            for script, args in [('classify-record-store.mjs', [str(root), 'example', revision]), ('validate-record-store.mjs', [str(path), '--revision', revision])]:
                result = subprocess.run(['node', str(ROOT / 'scripts' / script), *args], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
            self.assertEqual(files(), before)

if __name__ == "__main__":
    unittest.main()
