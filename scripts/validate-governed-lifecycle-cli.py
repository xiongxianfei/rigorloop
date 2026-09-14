#!/usr/bin/env python3
"""Validate current record discovery through the supported public CLI.

The historical script name is retained for repository check callers. Archives
are excluded by the shared discovery contract; this wrapper owns no eligibility.
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
        result = runner(
            ["node", str(CLI), "workflow-context", "--format", "json"],
            cwd=root, capture_output=True, text=True, timeout=60,
            env={**__import__("os").environ, "RIGORLOOP_FILE_LOG": "off", "RIGORLOOP_CONSOLE_LOG_LEVEL": "off"},
        )
        payload = json.loads(result.stdout)
        complete = (result.returncode == 0 and payload.get("schema_version") == 2
                    and payload.get("command") == "workflow-context"
                    and payload.get("status") == "success"
                    and payload.get("scope", {}).get("complete") is True)
        report = {"schema_version": 1, "status": "passed" if complete else "failed",
                  "context": payload}
    except (OSError, subprocess.TimeoutExpired, ValueError, AttributeError):
        report = {"schema_version": 1, "status": "failed", "errors": ["current-record-discovery-unavailable"]}
    print(json.dumps(report, indent=2, sort_keys=True), file=output)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", help="Exact committed record snapshot")
    args = parser.parse_args()
    sys.exit(main(revision=args.revision))
