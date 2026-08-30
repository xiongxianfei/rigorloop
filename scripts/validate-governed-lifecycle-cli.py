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
    "2026-08-25-cli-observability-token-efficient-results": {
        "blocker_codes": ["RL_STALE_EVIDENCE"],
        "finding_ids": [],
    },
}
RETIRED_PROGRESSION_STAGES = frozenset({
    "spec-review", "architecture-review", "plan-review", "test-spec-review",
})


def legacy_progression_dependency(path: Path) -> list[str]:
    """Return retired live routing stages; historical evidence is intentionally ignored."""
    if not path.is_file():
        return []
    fields: dict[str, str] = {}
    in_workflow_state = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "workflow_state:":
            in_workflow_state = True
            continue
        if in_workflow_state and line and not line.startswith(" "):
            break
        if in_workflow_state and line.startswith("  ") and not line.startswith("    "):
            key, separator, value = line.strip().partition(":")
            if separator:
                fields[key] = value.strip()
    if fields.get("lifecycle_state") != "active":
        return []
    return [
        fields[name]
        for name in ("current_stage", "next_stage")
        if fields.get(name) in RETIRED_PROGRESSION_STAGES
    ]


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
    legacy_dependent = []
    for change_id, _ in records:
        retired_stages = legacy_progression_dependency(_)
        if retired_stages:
            legacy_dependent.append({"change_id": change_id, "stages": retired_stages})
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
    return {
        "schema_version": 1,
        "validated": len(records),
        "baseline_warnings": warned,
        "legacy_progression_dependencies": legacy_dependent,
        "failures": failures,
        "status": "passed" if not failures and not legacy_dependent else "failed",
    }


def main(*, records=None, runner=subprocess.run, root: Path = ROOT, output=sys.stdout) -> int:
    report = build_report(governed_records(root) if records is None else records, runner=runner, root=root)
    print(json.dumps(report, indent=2, sort_keys=True), file=output)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
