#!/usr/bin/env python3
"""Validate current record discovery through the supported public CLI.

The historical script name is retained for repository check callers. Archives
are excluded by the shared discovery contract; this wrapper owns no eligibility.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "packages/rigorloop/dist/bin/rigorloop.js"


def main(*, runner=subprocess.run, root: Path = ROOT, output=sys.stdout) -> int:
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
    sys.exit(main())
