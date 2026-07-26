#!/usr/bin/env python3
"""Validate deterministic boundary-proof JSON and capability-report inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from boundary_proof_model import (
    BoundaryProofError,
    capability_report_result,
    normalize_feature_model,
    normalize_proof_map,
    validate_capability_report,
    validate_incident_registry,
)


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
    args = parser.parse_args(argv)
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
