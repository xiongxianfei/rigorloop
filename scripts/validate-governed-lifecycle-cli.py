#!/usr/bin/env python3
"""Invoke the public lifecycle validator for every governed change record."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_WARNINGS = {
    "2026-08-05-activate-boundary-first-v1-v0-3-7": {
        "blocker_codes": ["RL_OPERATION_NOT_PERMITTED", "RL_UNRESOLVED_MATERIAL_FINDING"],
        "finding_ids": [
            "BFA-M2-R1-002", "BFA-M2-R10-001", "BFA-M2-R10-002",
            "BFA-M2-R11-001", "BFA-M2-R11-002", "BFA-M2-R2-001",
            "BFA-M2-R7-001", "BFA-M2-R8-001", "BFA-M2-R8-002",
            "BFA-M2-R9-001",
        ],
    },
}


def baseline_matches(change_id: str, payload: dict) -> bool:
    expected = BASELINE_WARNINGS.get(change_id)
    if expected is None or payload.get("status") != "blocked" or payload.get("errors"):
        return False
    blocker_codes = sorted(item.get("code") for item in payload.get("blockers", []))
    finding_ids = sorted(payload.get("effective_state", {}).get("unresolved_findings", []))
    return blocker_codes == expected["blocker_codes"] and finding_ids == expected["finding_ids"]


def governed_records(root: Path = ROOT) -> list[tuple[str, Path]]:
    records = []
    for path in sorted((root / "docs" / "changes").glob("*/change.yaml")):
        if "lifecycle_contract: stage-owned-change-local-v1" in path.read_text(encoding="utf-8"):
            records.append((path.parent.name, path))
    return records


def result_codes(payload: dict) -> list[str]:
    if not isinstance(payload, dict):
        return ["invalid-structured-result"]
    errors = payload.get("errors", [])
    codes = payload.get("codes", [])
    if not isinstance(errors, list) or not isinstance(codes, list):
        return ["invalid-structured-result"]
    values = [item.get("code") for item in errors if isinstance(item, dict)]
    values.extend(codes)
    return list(dict.fromkeys(value for value in values if isinstance(value, str)))


def build_report(records: list[tuple[str, Path]], *, runner=subprocess.run, root: Path = ROOT) -> dict:
    failures = []
    warned = []
    for change_id, _ in records:
        command = [
            "node", "packages/rigorloop/dist/bin/rigorloop.js", "lifecycle", "validate",
            "--change", change_id, "--format", "json",
        ]
        result = runner(command, cwd=root, text=True, capture_output=True, check=False)
        if result.returncode == 0:
            continue
        payload = {}
        try:
            payload = json.loads(result.stdout)
            errors = result_codes(payload)
            if not isinstance(payload, dict):
                payload = {}
        except json.JSONDecodeError:
            errors = ["invalid-json-result"]
        item = {"change_id": change_id, "exit_code": result.returncode, "errors": errors}
        if baseline_matches(change_id, payload):
            warned.append(item)
        else:
            failures.append(item)
    return {"schema_version": 1, "validated": len(records), "baseline_warnings": warned, "failures": failures, "status": "passed" if not failures else "failed"}


def main(*, records=None, runner=subprocess.run, root: Path = ROOT, output=sys.stdout) -> int:
    report = build_report(governed_records(root) if records is None else records, runner=runner, root=root)
    print(json.dumps(report, indent=2, sort_keys=True), file=output)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
