#!/usr/bin/env python3
"""Validate broad-smoke child classification against scripts/ci.sh."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CI = ROOT / "scripts" / "ci.sh"
DEFAULT_CLASSIFICATION = (
    ROOT
    / "docs"
    / "changes"
    / "2026-06-27-broad-smoke-safe-parallelism"
    / "broad-smoke-child-classification.yaml"
)

CHECK_IDS_BY_RUN_CHECK_LABEL = {
    "Validate canonical skills": "broad_smoke.skills.validate",
    "Run skill validator fixtures": "broad_smoke.skills.regression",
    "Run local skill mirror generation fixtures": "broad_smoke.skills.generation_regression",
    "Validate generated skill mirror output": "broad_smoke.skills.drift",
    "Run adapter distribution fixtures": "broad_smoke.adapters.regression",
    "Build generated adapter archives": "broad_smoke.adapters.build_archives",
    "Validate generated adapter archives": "broad_smoke.adapters.validate_archives",
    "Run change metadata validator fixtures": "broad_smoke.change_metadata.regression",
    "Run artifact lifecycle validator fixtures": "broad_smoke.artifact_lifecycle.regression",
    "Run review artifact validator fixtures": "broad_smoke.review_artifacts.regression",
    "$review_artifact_label": "broad_smoke.review_artifacts.changed_roots",
    "$artifact_lifecycle_label": "broad_smoke.artifact_lifecycle.scoped",
}

REQUIRED_TOP_LEVEL_FIELDS = {
    "check_id",
    "run_check_label",
    "command",
    "current_order",
    "required",
    "classification",
    "side_effects",
    "paths",
    "isolation_plan",
    "result",
}
REQUIRED_CLASSIFICATION_FIELDS = {"parallel_candidate", "confidence", "reason"}
REQUIRED_SIDE_EFFECT_FIELDS = {
    "mutates_tracked_files",
    "mutates_generated_files",
    "writes_shared_temp",
    "writes_shared_output",
    "changes_cwd_assumptions",
    "relies_on_command_order",
    "network_sensitive",
    "network_hermetic",
    "uses_shared_cache",
    "starts_nested_parallelism",
    "cpu_intensity",
    "io_intensity",
    "diagnostic_order_sensitive",
    "failure_output_captured",
}
BLOCKING_SIDE_EFFECT_FIELDS = (
    "mutates_tracked_files",
    "mutates_generated_files",
    "writes_shared_temp",
    "writes_shared_output",
    "changes_cwd_assumptions",
    "relies_on_command_order",
    "uses_shared_cache",
    "starts_nested_parallelism",
    "diagnostic_order_sensitive",
)


class ClassificationError(ValueError):
    """Raised when classification cannot safely drive scheduling decisions."""


def extract_ci_functions(ci_text: str) -> dict[str, str]:
    functions: dict[str, str] = {}
    for match in re.finditer(
        r"(?ms)^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\(\) \{\n(?P<body>.*?)\n\}",
        ci_text,
    ):
        functions[match.group("name")] = match.group("body")
    return functions


def normalize_command(lines: list[str]) -> str:
    parts = []
    for line in lines:
        stripped = line.strip()
        if stripped.endswith("\\"):
            stripped = stripped[:-1].strip()
        parts.append(stripped)
    return " ".join(part for part in parts if part)


def extract_run_check_invocations(ci_text: str) -> list[dict[str, Any]]:
    functions = extract_ci_functions(ci_text)
    if "run_broad_smoke" not in functions:
        raise ClassificationError("scripts/ci.sh is missing run_broad_smoke")

    lines = functions["run_broad_smoke"].splitlines()
    invocations: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(
            r"^\s*run_check\s+(?P<label>\"[^\"]+\"|\$[A-Za-z_][A-Za-z0-9_]*)\s*\\?\s*$",
            line,
        )
        if not match:
            index += 1
            continue

        label = match.group("label")
        if label.startswith('"') and label.endswith('"'):
            label = label[1:-1]
        if label not in CHECK_IDS_BY_RUN_CHECK_LABEL:
            raise ClassificationError(f"unmapped broad-smoke run_check label: {label}")

        command_lines: list[str] = []
        index += 1
        while index < len(lines):
            current = lines[index]
            if command_lines and not command_lines[-1].rstrip().endswith("\\"):
                break
            if current.strip():
                command_lines.append(current)
            index += 1
        if not command_lines:
            raise ClassificationError(f"broad-smoke child has no command: {label}")

        invocations.append(
            {
                "check_id": CHECK_IDS_BY_RUN_CHECK_LABEL[label],
                "run_check_label": label,
                "command": normalize_command(command_lines),
                "current_order": len(invocations) + 1,
                "required": True,
            }
        )
    return invocations


def load_classification(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ClassificationError("classification artifact must be a mapping")
    children = data.get("children")
    if not isinstance(children, list):
        raise ClassificationError("classification artifact must define children as a list")
    return data


def require_fields(check_id: str, data: dict[str, Any], fields: set[str], context: str) -> None:
    missing = sorted(field for field in fields if field not in data)
    if missing:
        raise ClassificationError(f"{check_id}: missing {context} fields: {', '.join(missing)}")


def validate_child_metadata(child: dict[str, Any]) -> None:
    check_id = str(child.get("check_id", "<unknown>"))
    require_fields(check_id, child, REQUIRED_TOP_LEVEL_FIELDS, "top-level")
    classification = child["classification"]
    side_effects = child["side_effects"]
    result = child["result"]
    if not isinstance(classification, dict):
        raise ClassificationError(f"{check_id}: classification must be a mapping")
    if not isinstance(side_effects, dict):
        raise ClassificationError(f"{check_id}: side_effects must be a mapping")
    if not isinstance(result, dict):
        raise ClassificationError(f"{check_id}: result must be a mapping")

    require_fields(check_id, classification, REQUIRED_CLASSIFICATION_FIELDS, "classification")
    require_fields(check_id, side_effects, REQUIRED_SIDE_EFFECT_FIELDS, "side_effects")
    require_fields(check_id, result, {"eligible_for_parallelism"}, "result")

    confidence = classification["confidence"]
    if confidence not in {"high", "medium", "low"}:
        raise ClassificationError(f"{check_id}: invalid classification confidence: {confidence}")

    parallel_candidate = bool(classification["parallel_candidate"])
    eligible = bool(result["eligible_for_parallelism"])
    if eligible != parallel_candidate:
        raise ClassificationError(
            f"{check_id}: eligible_for_parallelism must match classification.parallel_candidate"
        )

    if not side_effects["failure_output_captured"]:
        raise ClassificationError(f"{check_id}: failure output must be captured")

    if parallel_candidate:
        if confidence != "high":
            raise ClassificationError(f"{check_id}: parallel candidate must have high confidence")
        blocking = [field for field in BLOCKING_SIDE_EFFECT_FIELDS if side_effects[field]]
        if blocking:
            raise ClassificationError(
                f"{check_id}: parallel candidate has blocking side-effect fields: {', '.join(blocking)}"
            )
        if side_effects["network_sensitive"] and not side_effects["network_hermetic"]:
            raise ClassificationError(f"{check_id}: network-sensitive candidate is not hermetic")


def validate(ci_path: Path, classification_path: Path) -> None:
    invocations = extract_run_check_invocations(ci_path.read_text(encoding="utf-8"))
    data = load_classification(classification_path)
    children = data["children"]
    by_id = {child.get("check_id"): child for child in children if isinstance(child, dict)}

    expected_ids = [child["check_id"] for child in invocations]
    actual_ids = [child.get("check_id") for child in children if isinstance(child, dict)]
    if actual_ids != expected_ids:
        raise ClassificationError(
            "classification child inventory mismatch: "
            f"expected {expected_ids}; found {actual_ids}"
        )

    for expected in invocations:
        child = by_id[expected["check_id"]]
        validate_child_metadata(child)
        for field in ("run_check_label", "command", "current_order", "required"):
            if child[field] != expected[field]:
                raise ClassificationError(
                    f"{expected['check_id']}: stale {field}: "
                    f"expected {expected[field]!r}; found {child[field]!r}"
                )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ci-path", type=Path, default=DEFAULT_CI)
    parser.add_argument("--classification", type=Path, default=DEFAULT_CLASSIFICATION)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validate(args.ci_path, args.classification)
    except ClassificationError as exc:
        print(f"broad-smoke classification validation failed: {exc}", file=sys.stderr)
        return 1
    print("broad-smoke classification validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
