#!/usr/bin/env python3
"""Validate retained repository v3 record sources without operational CLI dispatch.

The historical script name is retained for repository check callers. Archives
are excluded by the qualified source classifier; this wrapper owns no eligibility. SQLite runtime state is private and is not Git validation input.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "packages/rigorloop/dist/bin/rigorloop.js"


def snapshot_report(root, revision, runner):
    if not re.fullmatch(r'(?:[a-f0-9]{40}|[a-f0-9]{64})', revision):
        raise ValueError('immutable commit required')
    import os
    environment = {
        'PATH': os.environ.get('PATH', ''), 'LANG': 'C', 'LC_ALL': 'C',
        'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
        'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_NO_LAZY_FETCH': '1',
        'GIT_ALLOW_PROTOCOL': '', 'GIT_OPTIONAL_LOCKS': '0', 'GIT_TERMINAL_PROMPT': '0',
    }
    def run(args):
        result = runner(args, cwd=root, capture_output=True, text=True, timeout=60, env=environment)
        if result.returncode or len(result.stdout.encode()) > 8 * 1024 * 1024:
            raise ValueError('snapshot unavailable')
        return result.stdout
    if Path(run(['git', 'rev-parse', '--show-toplevel']).strip()).resolve() != root.resolve():
        raise ValueError('snapshot root mismatch')
    commit = run(['git', 'rev-parse', '--verify', revision + '^{commit}']).strip()
    if commit != revision:
        raise ValueError('commit mismatch')
    for directory in ('docs', 'docs/changes'):
        entry = run(['git', 'ls-tree', '-z', revision, '--', directory])
        if entry and not entry.startswith('040000 tree '):
            raise ValueError('unsafe snapshot directory')
    paths = run(['git', 'ls-tree', '-r', '--name-only', '-z', revision, '--', 'docs/changes']).split('\0')
    ids = sorted({p.split('/')[2] for p in paths if p.startswith('docs/changes/') and len(p.split('/')) >= 3})
    if len(ids) > 1024:
        raise ValueError('snapshot limit exceeded')
    validated = excluded = 0
    for change_id in ids:
        kind = run(['node', str(ROOT / 'scripts/classify-record-store.mjs'), str(root), change_id, revision]).strip()
        if kind in ('archive', 'noncurrent'):
            excluded += 1
        elif kind == 'current':
            if validated >= 64:
                raise ValueError('snapshot limit exceeded')
            run(['node', str(ROOT / 'scripts/validate-record-store.mjs'),
                 str(root / 'docs/changes' / change_id / 'change.json'), '--revision', revision])
            validated += 1
        else:
            raise ValueError('unknown snapshot classification')
    return {'schema_version': 1, 'status': 'passed', 'snapshot': {
        'revision': revision, 'validated': validated, 'excluded_noncurrent': excluded}}


def main(*, runner=subprocess.run, root: Path = ROOT, output=sys.stdout, revision=None) -> int:
    if revision is not None:
        try:
            report = snapshot_report(root, revision, runner)
        except (OSError, subprocess.TimeoutExpired, ValueError, AttributeError):
            report = {'schema_version': 1, 'status': 'failed', 'errors': ['current-record-snapshot-unavailable']}
        print(json.dumps(report, indent=2, sort_keys=True), file=output)
        return 0 if report['status'] == 'passed' else 1

    try:
        directory=root / "docs/changes"
        for part in (root / "docs",directory):
            if part.is_symlink() or part.exists() and not part.is_dir():
                raise ValueError('unsafe source directory')
        entries=sorted(directory.iterdir()) if directory.exists() else []
        if len(entries)>1024: raise ValueError('source limit exceeded')
        validated=excluded=0
        for entry in entries:
            if entry.is_symlink(): raise ValueError('unsafe source entry')
            if not entry.is_dir(): continue
            result=runner(["node",str(ROOT / "scripts/classify-record-store.mjs"),str(root),entry.name],cwd=root,capture_output=True,text=True,timeout=60)
            if result.returncode: raise ValueError('source classification failed')
            kind=result.stdout.strip()
            if kind in ('archive','noncurrent'): excluded+=1
            elif kind=='current':
                if validated>=64: raise ValueError('source limit exceeded')
                result=runner(["node",str(ROOT / "scripts/validate-record-store.mjs"),str(entry / "change.json")],cwd=root,capture_output=True,text=True,timeout=60)
                if result.returncode: raise ValueError('source validation failed')
                validated+=1
            else: raise ValueError('unknown source classification')
        report={"schema_version":1,"status":"passed","context":{"source_contract":"rigorloop-records-v3","scope":{"complete":True,"candidate_count":validated,"excluded_noncurrent":excluded}}}
    except (OSError, subprocess.TimeoutExpired, ValueError, AttributeError):
        report = {"schema_version": 1, "status": "failed", "errors": ["retained-record-source-unavailable"],"context":{"scope":{"complete":False}}}
    print(json.dumps(report, indent=2, sort_keys=True), file=output)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", help="Exact committed record snapshot")
    args = parser.parse_args()
    sys.exit(main(revision=args.revision))
