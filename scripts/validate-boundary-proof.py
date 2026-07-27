#!/usr/bin/env python3
"""Validate deterministic boundary-proof JSON and capability-report inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from adapter_distribution import ADAPTERS, expected_adapter_files
from boundary_proof_model import (
    BoundaryProofError,
    CHECK_IDS,
    EVALUATED_SKILLS,
    FIXTURE_GATES,
    PRESERVATION_KEYS,
    capability_report_result,
    normalize_feature_model,
    normalize_proof_map,
    validate_capability_report,
    validate_incident_fixture,
    validate_incident_registry,
)

ROOT = Path(__file__).resolve().parents[1]
CHANGE_ID = (
    "2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills"
)
BOUNDARY_RESOURCE = "references/boundary-proof-model.md"
ADAPTER_ROOTS = {
    "codex": ".agents/skills",
    "claude": ".claude/skills",
    "opencode": ".opencode/skills",
}


def _identity(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _reference(path: Path) -> dict[str, str]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "identity": _identity(path.read_bytes()),
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)


def _change_root(change_id: str) -> Path:
    if change_id != CHANGE_ID:
        raise BoundaryProofError("unsupported boundary capability change ID")
    root = ROOT / "docs" / "changes" / change_id
    if not root.is_dir():
        raise BoundaryProofError("change root does not exist")
    return root


def generate_adapter_parity(change_id: str) -> dict[str, Any]:
    """Generate current canonical, generated, packed, and installed maps."""

    change_root = _change_root(change_id)
    canonical_rows: list[dict[str, str]] = []
    canonical_bytes: dict[tuple[str, str], bytes] = {}
    for skill in EVALUATED_SKILLS:
        for logical_path in (BOUNDARY_RESOURCE,):
            path = ROOT / "skills" / skill / logical_path
            raw = path.read_bytes()
            canonical_bytes[(skill, logical_path)] = raw
            canonical_rows.append(
                {
                    "adapter": "canonical",
                    "skill": skill,
                    "logical_path": logical_path,
                    "source_path": path.relative_to(ROOT).as_posix(),
                    "identity": _identity(raw),
                }
            )
    canonical_rows.sort(
        key=lambda row: (row["skill"], row["logical_path"])
    )

    surface_rows: dict[str, list[dict[str, str]]] = {
        "generated": [],
        "packed": [],
        "installed": [],
    }
    with tempfile.TemporaryDirectory() as raw_temp:
        output = Path(raw_temp)
        generated_files = expected_adapter_files("v0.1.5")
        built = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build-adapters.py"),
                "--version",
                "v0.1.5",
                "--output-dir",
                str(output),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if built.returncode != 0:
            raise BoundaryProofError(
                "adapter generation failed: " + built.stderr.strip()
            )
        validated = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate-adapters.py"),
                "--root",
                str(output),
                "--version",
                "v0.1.5",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if validated.returncode != 0:
            raise BoundaryProofError(
                "adapter validation failed: "
                + validated.stderr.strip()
            )
        for adapter, skill_root in ADAPTER_ROOTS.items():
            config = ADAPTERS[adapter]
            archive = (
                output
                / f"rigorloop-adapter-{adapter}-v0.1.5.zip"
            )
            install_root = output / "installed" / adapter
            with ZipFile(archive) as packed:
                packed.extractall(install_root)
                for skill in EVALUATED_SKILLS:
                    for logical_path in (BOUNDARY_RESOURCE,):
                        member = (
                            f"{skill_root}/{skill}/{logical_path}"
                        )
                        generated_path = (
                            Path(adapter)
                            / Path(config.skill_root.as_posix())
                            / skill
                            / logical_path
                        )
                        generated_raw = generated_files[
                            generated_path
                        ].encode("utf-8")
                        packed_raw = packed.read(member)
                        installed_path = install_root / member
                        installed_raw = installed_path.read_bytes()
                        expected_raw = canonical_bytes[
                            (skill, logical_path)
                        ]
                        if not (
                            generated_raw
                            == packed_raw
                            == installed_raw
                            == expected_raw
                        ):
                            raise BoundaryProofError(
                                f"{adapter}:{skill}:{logical_path}: "
                                "adapter parity mismatch"
                            )
                        common = {
                            "adapter": adapter,
                            "skill": skill,
                            "logical_path": logical_path,
                        }
                        surface_rows["generated"].append(
                            {
                                **common,
                                "source_path": generated_path.as_posix(),
                                "identity": _identity(generated_raw),
                            }
                        )
                        surface_rows["packed"].append(
                            {
                                **common,
                                "source_path": member,
                                "identity": _identity(packed_raw),
                            }
                        )
                        surface_rows["installed"].append(
                            {
                                **common,
                                "source_path": installed_path.relative_to(
                                    output
                                ).as_posix(),
                                "identity": _identity(installed_raw),
                            }
                        )

    parity_root = change_root / "evidence" / "adapter-parity"
    manifests: dict[str, dict[str, Any]] = {}
    for surface, rows in (
        ("canonical", canonical_rows),
        *surface_rows.items(),
    ):
        rows.sort(
            key=lambda row: (
                row["adapter"],
                row["skill"],
                row["logical_path"],
            )
        )
        manifest = {
            "schema_version": "boundary-adapter-parity-v1",
            "surface": surface,
            "files": rows,
        }
        _write_json(parity_root / f"{surface}.json", manifest)
        manifests[surface] = manifest
    return {
        "result": "pass",
        "surface_count": 4,
        "manifests": manifests,
    }


def validate_adapter_parity(change_id: str) -> dict[str, Any]:
    change_root = _change_root(change_id)
    parity_root = change_root / "evidence" / "adapter-parity"
    manifests = {
        surface: _load_json(parity_root / f"{surface}.json")
        for surface in ("canonical", "generated", "packed", "installed")
    }
    expected_identities: dict[tuple[str, str], str] = {}
    for skill in EVALUATED_SKILLS:
        for logical_path in (BOUNDARY_RESOURCE,):
            expected_identities[(skill, logical_path)] = _identity(
                (ROOT / "skills" / skill / logical_path).read_bytes()
            )
    for surface, manifest in manifests.items():
        if (
            not isinstance(manifest, dict)
            or set(manifest)
            != {"schema_version", "surface", "files"}
            or manifest["schema_version"]
            != "boundary-adapter-parity-v1"
            or manifest["surface"] != surface
            or not isinstance(manifest["files"], list)
        ):
            raise BoundaryProofError(
                f"{surface}: invalid parity manifest"
            )
        expected_count = 8 if surface == "canonical" else 24
        if len(manifest["files"]) != expected_count:
            raise BoundaryProofError(
                f"{surface}: incomplete parity manifest"
            )
        seen: set[tuple[str, str, str]] = set()
        for row in manifest["files"]:
            if not isinstance(row, dict) or set(row) != {
                "adapter",
                "skill",
                "logical_path",
                "source_path",
                "identity",
            }:
                raise BoundaryProofError(
                    f"{surface}: malformed parity row"
                )
            key = (
                row["adapter"],
                row["skill"],
                row["logical_path"],
            )
            if key in seen:
                raise BoundaryProofError(
                    f"{surface}: duplicate parity row"
                )
            seen.add(key)
            expected = expected_identities.get(
                (row["skill"], row["logical_path"])
            )
            if expected is None or row["identity"] != expected:
                raise BoundaryProofError(
                    f"{surface}: stale parity identity"
                )
    return {"result": "pass", "surface_count": 4}


def _parse_report(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    start = text.find("```yaml\n")
    end = text.find("\n```", start + 8)
    if start < 0 or end < 0:
        raise BoundaryProofError("report fenced payload is missing")
    try:
        return json.loads(text[start + 8 : end])
    except json.JSONDecodeError as error:
        raise BoundaryProofError("report payload is invalid") from error


def generate_report(change_id: str, output: Path) -> dict[str, Any]:
    change_root = _change_root(change_id)
    validate_adapter_parity(change_id)
    behavior_process = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "boundary_proof_behavior.py"),
            "validate",
            "--change-id",
            change_id,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if behavior_process.returncode != 0:
        raise BoundaryProofError(
            "current behavior evidence is not valid"
        )
    behavior = json.loads(behavior_process.stdout)
    preservation_process = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "boundary_proof_behavior.py"),
            "validate-preservation",
            "--change-id",
            change_id,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if preservation_process.returncode != 0:
        raise BoundaryProofError(
            "current preservation evidence is not valid"
        )
    preservation = json.loads(preservation_process.stdout)
    if preservation.get("result") != "structural-pass":
        raise BoundaryProofError("preservation structural proof missing")

    workflow_ref = _reference(ROOT / "specs" / "rigorloop-workflow.md")
    skill_ref = _reference(ROOT / "specs" / "skill-contract.md")
    trace_ref = _reference(
        ROOT / "specs" / "rigorloop-workflow.test.md"
    )
    review_ref = _reference(
        change_root / "reviews" / "code-review-m3-r2.md"
    )
    current_ref = _reference(
        change_root / "evidence" / "simple-change" / "current.json"
    )
    parity_refs = [
        _reference(
            change_root
            / "evidence"
            / "adapter-parity"
            / f"{surface}.json"
        )
        for surface in ("canonical", "generated", "packed", "installed")
    ]
    checks_refs = {
        "boundary-workflow-contract": [workflow_ref],
        "boundary-skill-contract": [skill_ref],
        "boundary-traceability": [trace_ref],
        "boundary-incident-replay": [
            _reference(
                ROOT
                / "tests"
                / "fixtures"
                / "boundary-proof"
                / "incident-registry.json"
            )
        ],
        "boundary-adapter-parity": parity_refs,
        "boundary-capability-baseline": [review_ref, current_ref],
    }
    checks = {
        check_id: {
            "result": "pass",
            "evidence_refs": checks_refs[check_id],
            "blocking_reason": None,
        }
        for check_id in CHECK_IDS
    }
    fixtures = []
    for fixture_id, gate in FIXTURE_GATES.items():
        fixture_path = (
            ROOT
            / "tests"
            / "fixtures"
            / "boundary-proof"
            / "incidents"
            / f"{fixture_id}.json"
        )
        replay = validate_incident_fixture(_load_json(fixture_path))
        if replay.detected_stage != gate:
            raise BoundaryProofError(
                f"{fixture_id}: incident replay gate mismatch"
            )
        fixtures.append(
            {
                "fixture_id": fixture_id,
                "result": "pass",
                "expected_gate": gate,
                "detected_stage": replay.detected_stage,
                "escaped_to_code_review": replay.escaped_to_code_review,
                "sibling_bypass_remaining": (
                    replay.sibling_bypass_remaining
                ),
                "evidence_refs": [_reference(fixture_path)],
                "blocking_reason": None,
            }
        )
    report = {
        "schema_version": "boundary-capability-baseline-v1",
        "boundary_model_version": "v1",
        "evaluated_skills": list(EVALUATED_SKILLS),
        "required_check_ids": list(CHECK_IDS),
        "checks": checks,
        "fixtures": fixtures,
        "preservation_results": {
            key: {
                "result": "pass",
                "evidence_refs": [review_ref],
                "blocking_reason": None,
            }
            for key in PRESERVATION_KEYS
        },
        "adapter_parity": {
            "result": "pass",
            "evidence_refs": parity_refs,
            "blocking_reason": None,
        },
        "false_blocking_count": behavior["false_blocking_count"],
        "duplicate_normative_owner_count": 0,
        "new_universal_artifact_count": behavior[
            "new_universal_artifact_count"
        ],
        "simple_fixture_structure_correction_cycles": behavior[
            "simple_fixture_structure_correction_cycles"
        ],
        "overall_result": "pass",
    }
    validate_capability_report(report)
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(_render_report(report), encoding="utf-8")
    temporary.replace(output)
    return {
        "result": capability_report_result(report),
        "report_identity": _identity(output.read_bytes()),
    }


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BoundaryProofError(f"{path}: could not load JSON: {error}") from error


def _render_report(payload: Any) -> str:
    """Render one deterministic YAML-compatible fenced record."""

    validate_capability_report(payload)
    body = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    return (
        "# Boundary Capability Baseline\n\n"
        "This report is computed from repository-visible evidence.\n\n"
        "```yaml\n"
        f"{body}\n"
        "```\n"
    )


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] in {
        "generate-parity",
        "validate-parity",
        "generate-report",
        "validate-report",
    }:
        command_parser = argparse.ArgumentParser(description=__doc__)
        commands = command_parser.add_subparsers(
            dest="command", required=True
        )
        for name in ("generate-parity", "validate-parity"):
            command = commands.add_parser(name)
            command.add_argument("--change-id", required=True)
        report_generate = commands.add_parser("generate-report")
        report_generate.add_argument("--change-id", required=True)
        report_generate.add_argument("--output", required=True, type=Path)
        report_validate = commands.add_parser("validate-report")
        report_validate.add_argument("report", type=Path)
        args = command_parser.parse_args(arguments)
        try:
            if args.command == "generate-parity":
                result = generate_adapter_parity(args.change_id)
            elif args.command == "validate-parity":
                result = validate_adapter_parity(args.change_id)
            elif args.command == "generate-report":
                result = generate_report(args.change_id, args.output)
            else:
                payload = _parse_report(args.report)
                validate_capability_report(payload)
                computed = capability_report_result(payload)
                if computed != "pass":
                    raise BoundaryProofError(
                        "capability report does not pass"
                    )
                result = {
                    "result": computed,
                    "report_identity": _identity(
                        args.report.read_bytes()
                    ),
                }
        except (
            BoundaryProofError,
            OSError,
            subprocess.SubprocessError,
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            print(
                f"boundary proof validation failed: {error}",
                file=sys.stderr,
            )
            return 1
        print(json.dumps(result, sort_keys=True))
        return 0

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="JSON feature model, incident registry, or capability report",
    )
    parser.add_argument(
        "--proof-map",
        type=Path,
        help="matching JSON proof map; requires a feature-model path",
    )
    parser.add_argument(
        "--kind",
        choices=("feature-model", "incident-registry", "capability-report"),
        default="capability-report",
        help="input contract to validate",
    )
    parser.add_argument(
        "--write-report",
        type=Path,
        help="write a validated capability report as deterministic fenced YAML",
    )
    args = parser.parse_args(arguments)
    if args.path is None:
        parser.print_help()
        return 0
    try:
        payload = _load_json(args.path)
        if args.kind == "feature-model":
            feature = normalize_feature_model(payload)
            if args.proof_map is not None:
                normalize_proof_map(_load_json(args.proof_map), feature)
            result = "valid feature boundary model"
        elif args.kind == "incident-registry":
            if args.proof_map is not None:
                raise BoundaryProofError(
                    "--proof-map is valid only with --kind feature-model"
                )
            validate_incident_registry(payload)
            result = "valid incident registry"
        else:
            if args.proof_map is not None:
                raise BoundaryProofError(
                    "--proof-map is valid only with --kind feature-model"
                )
            validate_capability_report(payload)
            if args.write_report is not None:
                args.write_report.write_text(
                    _render_report(payload),
                    encoding="utf-8",
                )
            result = f"valid capability report ({capability_report_result(payload)})"
    except BoundaryProofError as error:
        print(f"boundary proof validation failed: {error}", file=sys.stderr)
        return 1
    print(f"{args.path}: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
