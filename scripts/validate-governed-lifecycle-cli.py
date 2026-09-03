#!/usr/bin/env python3
"""Invoke the public lifecycle validator for every governed change record."""

from __future__ import annotations

import json
import runpy
import subprocess
import sys
from pathlib import Path

from artifact_lifecycle_contracts import (
    FINAL_VERIFICATION_ACTIVATION_MANIFEST_PATH,
    LEGACY_UNVERSIONED_CONTRACT,
    LIFECYCLE_ACTIVATION_MANIFEST_PATH,
    LIFECYCLE_CONTRACT_V1,
    LIFECYCLE_CONTRACT_V3,
    parse_lifecycle_activation_manifest,
    validate_lifecycle_activation_manifest,
    validate_lifecycle_activation_prerequisites,
    validate_final_verification_activation_manifest,
)


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
    "2026-08-24-governed-lifecycle-cli": {
        "blocker_codes": ["RL_STALE_EVIDENCE"],
        "finding_ids": [],
    },
    "2026-08-25-cli-observability-token-efficient-results": {
        "blocker_codes": ["RL_STALE_EVIDENCE"],
        "finding_ids": [],
    },
}
RETIRED_PROGRESSION_STAGES = frozenset({
    "spec-review", "architecture-review", "plan-review", "test-spec-review",
})
GOVERNED_CONTRACTS = frozenset({LIFECYCLE_CONTRACT_V1, LIFECYCLE_CONTRACT_V3, "stage-owned-change-local-v2"})
_DEFAULT_METADATA_LOADER = None


def change_metadata_loader():
    """Load the repository's safe YAML parser once for semantic contract discovery."""
    global _DEFAULT_METADATA_LOADER
    if _DEFAULT_METADATA_LOADER is None:
        scripts_dir = str(ROOT / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        _DEFAULT_METADATA_LOADER = runpy.run_path(
            str(ROOT / "scripts" / "validate-change-metadata.py")
        )["load_yaml"]
    return _DEFAULT_METADATA_LOADER


def parsed_change_inventory(root: Path = ROOT, *, loader=None) -> tuple[dict[str, dict], list[str]]:
    """Return semantic lifecycle classes for every tracked change record."""
    load = loader or change_metadata_loader()
    records: dict[str, dict] = {}
    errors: list[str] = []
    paths = sorted(
        (root / "docs" / "changes").glob("*/change.yaml"),
        key=lambda path: path.parent.name.encode("utf-8"),
    )
    for path in paths:
        change_id = path.parent.name
        try:
            metadata = load(path)
        except Exception as exc:
            errors.append(f"change metadata {change_id} unreadable: {exc}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"change metadata {change_id} must be a mapping")
            continue
        if "lifecycle_contract" in metadata:
            contract = metadata.get("lifecycle_contract")
            if contract not in GOVERNED_CONTRACTS:
                errors.append(f"change metadata {change_id} lifecycle_contract: unknown_value {contract}")
                continue
        else:
            contract = LEGACY_UNVERSIONED_CONTRACT
        records[change_id] = {"path": path, "metadata": metadata, "contract": contract}
    return records, errors


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
    records, _ = parsed_change_inventory(root)
    return [
        (change_id, entry["path"])
        for change_id, entry in records.items()
        if entry["contract"] in GOVERNED_CONTRACTS
    ]


def activation_inventory_errors(root: Path = ROOT, *, loader=None) -> list[str]:
    """Validate the active manifest against every tracked prior change."""
    manifest_path = root / LIFECYCLE_ACTIVATION_MANIFEST_PATH
    try:
        manifest = parse_lifecycle_activation_manifest(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"activation manifest unreadable: {exc}"]
    errors = validate_lifecycle_activation_manifest(manifest)
    if errors or manifest.get("state") != "active":
        return errors or ["activation manifest state must be active"]

    inventory, inventory_errors = parsed_change_inventory(root, loader=loader)
    if inventory_errors:
        return inventory_errors
    actual_classes = {
        change_id: entry["contract"]
        for change_id, entry in inventory.items()
        if entry["contract"] in {LIFECYCLE_CONTRACT_V1, LEGACY_UNVERSIONED_CONTRACT}
    }

    frozen_classes = {entry["change_id"]: entry["contract_class"] for entry in manifest["changes"]}
    if frozen_classes != actual_classes:
        missing = sorted(set(actual_classes) - set(frozen_classes), key=lambda item: item.encode("utf-8"))
        extra = sorted(set(frozen_classes) - set(actual_classes), key=lambda item: item.encode("utf-8"))
        changed = sorted(
            (change_id for change_id in set(actual_classes) & set(frozen_classes) if actual_classes[change_id] != frozen_classes[change_id]),
            key=lambda item: item.encode("utf-8"),
        )
        return [f"activation inventory mismatch: missing={missing}, extra={extra}, class_mismatch={changed}"]

    records = {}
    for change_id, entry in inventory.items():
        if change_id not in actual_classes:
            continue
        if actual_classes[change_id] == LEGACY_UNVERSIONED_CONTRACT:
            records[change_id] = {"workflow_state": {"lifecycle_state": "completed"}}
        else:
            records[change_id] = entry["metadata"]
    return validate_lifecycle_activation_prerequisites(manifest, records)


def final_verification_manifest_errors(root: Path = ROOT, *, loader=None) -> list[str]:
    """Validate the inactive or active v3 activation boundary."""
    manifest_path = root / FINAL_VERIFICATION_ACTIVATION_MANIFEST_PATH
    try:
        manifest = parse_lifecycle_activation_manifest(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"final verification activation manifest unreadable: {exc}"]
    errors = validate_final_verification_activation_manifest(manifest)
    return errors


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
    report["activation_errors"] = activation_inventory_errors(root)
    report["final_verification_activation_errors"] = final_verification_manifest_errors(root)
    if report["activation_errors"] or report["final_verification_activation_errors"]:
        report["status"] = "failed"
    print(json.dumps(report, indent=2, sort_keys=True), file=output)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
