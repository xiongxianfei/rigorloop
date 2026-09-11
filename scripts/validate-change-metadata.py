#!/usr/bin/env python3
"""Validate current v2 record sets and independent validation-cache measurements."""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from project_yaml import MetadataValidationError, load_yaml, tokenize_yaml, parse_yaml_block

ROOT = Path(__file__).resolve().parents[1]

MEASUREMENT_SUMMARY_FIELDS = {
    "eligible_commands",
    "helper_invocations",
    "cache_hits",
    "cache_misses",
    "cache_disabled",
    "actual_run_fallbacks",
    "actual_runs",
    "closeout_actual_runs",
    "estimated_seconds_saved",
    "remaining_validation_seconds",
    "cache_hit_rate",
}



MEASUREMENT_VALIDATOR_COUNT_FIELDS = {
    "eligible_commands",
    "helper_invocations",
    "cache_hits",
    "cache_misses",
    "cache_disabled",
    "actual_run_fallbacks",
    "actual_runs",
    "closeout_actual_runs",
}



MEASUREMENT_RATE_TOLERANCE = 0.000001



MEASUREMENT_STILL_RERUN_REASONS = {
    "none",
    "input-changed",
    "implementation-changed",
    "policy-changed",
    "closeout-gate",
    "unsupported-surface",
    "other",
}



WORKSTREAM_B_RECOMMENDATION_STATES = {
    "defer",
    "propose-follow-up",
    "reject-for-now",
}



def path_label(path: str, key: str | int | None = None) -> str:
    if key is None:
        return path
    if isinstance(key, int):
        return f"{path}[{key}]"
    if path == "$":
        return key
    return f"{path}.{key}"



def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())



def validate_repo_relative_path(value: str, path: str) -> list[str]:
    errors: list[str] = []
    lower_value = value.lower()
    if value.startswith("/"):
        errors.append(f"{path}: unsafe absolute path")
    if re.match(r"^[A-Za-z]:[\\/]", value):
        errors.append(f"{path}: unsafe absolute path")
    if value.startswith("~"):
        errors.append(f"{path}: unsafe home-directory path")
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", value):
        errors.append(f"{path}: unsafe URL or hostname path")
    if re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/|$)", value):
        errors.append(f"{path}: unsafe hostname path")
    if "@" in value.split("/", 1)[0] or re.search(r"://[^/\s]+@", value):
        errors.append(f"{path}: unsafe credential-bearing path")
    if any(part == ".." for part in value.split("/")):
        errors.append(f"{path}: unsafe parent-directory path")
    if (
        lower_value.startswith(("home/", "users/"))
        or "/home/" in lower_value
        or "/users/" in lower_value
    ):
        errors.append(f"{path}: unsafe machine-local path")
    secret_markers = (
        "password=",
        "passwd=",
        "token=",
        "secret=",
        "private_key",
        "private-key",
        "http_proxy=",
        "https_proxy=",
    )
    if any(marker in lower_value for marker in secret_markers):
        errors.append(f"{path}: unsafe secret-like value")
    return errors



def validate_safe_measurement_value(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            errors.extend(validate_safe_measurement_value(child, path_label(path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(validate_safe_measurement_value(child, path_label(path, index)))
    elif isinstance(value, str):
        errors.extend(validate_repo_relative_path(value, path))
    return errors



def is_measurement_file(path: Path) -> bool:
    return path.name == "validation-cache-measurement.yaml"



def is_nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0



def is_nonnegative_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value >= 0
    )



def validate_measurement_required_fields(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = (
        "schema_version",
        "change_id",
        "measurement_window",
        "summary",
        "validators",
        "closeout",
        "workstream_b_recommendation",
    )
    for field in required:
        if field not in data:
            errors.append(f"{field}: missing required measurement field")
    return errors



def validate_measurement_window(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["measurement_window: expected object"]
    errors: list[str] = []
    for field in ("start_stage", "end_stage", "description"):
        if not is_nonempty_string(value.get(field)):
            errors.append(f"measurement_window.{field}: expected string")
    return errors



def validate_measurement_summary(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["summary: expected object"]
    errors: list[str] = []
    for field in sorted(MEASUREMENT_SUMMARY_FIELDS):
        if field not in value:
            errors.append(f"summary.{field}: missing required field")

    for field in (
        "eligible_commands",
        "helper_invocations",
        "cache_hits",
        "cache_misses",
        "cache_disabled",
        "actual_run_fallbacks",
        "actual_runs",
        "closeout_actual_runs",
    ):
        if field in value and not is_nonnegative_integer(value[field]):
            errors.append(f"summary.{field}: expected non-negative integer")
    for field in ("estimated_seconds_saved", "remaining_validation_seconds"):
        if field in value and not is_nonnegative_number(value[field]):
            errors.append(f"summary.{field}: expected non-negative number")
    cache_hit_rate = value.get("cache_hit_rate")
    if "cache_hit_rate" in value and (
        not is_nonnegative_number(cache_hit_rate) or cache_hit_rate > 1
    ):
        errors.append("summary.cache_hit_rate: expected number between 0 and 1")

    errors.extend(validate_measurement_count_relationships(value, "summary"))
    return errors



def validate_measurement_count_relationships(value: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    eligible = value.get("eligible_commands")
    helper_invocations = value.get("helper_invocations")
    hits = value.get("cache_hits")
    misses = value.get("cache_misses")
    disabled = value.get("cache_disabled")
    fallbacks = value.get("actual_run_fallbacks")
    actual_runs = value.get("actual_runs")
    closeout_actual_runs = value.get("closeout_actual_runs")

    if all(is_nonnegative_integer(item) for item in (helper_invocations, hits, fallbacks)):
        if helper_invocations != hits + fallbacks:
            errors.append(
                f"{prefix}.helper_invocations: expected cache_hits + actual_run_fallbacks"
            )
    if all(is_nonnegative_integer(item) for item in (fallbacks, misses, disabled)):
        if fallbacks != misses + disabled:
            errors.append(
                f"{prefix}.actual_run_fallbacks: expected cache_misses + cache_disabled"
            )
    if all(is_nonnegative_integer(item) for item in (eligible, helper_invocations)):
        if eligible < helper_invocations:
            errors.append(
                f"{prefix}.eligible_commands: expected at least helper_invocations"
            )
    if all(is_nonnegative_integer(item) for item in (actual_runs, fallbacks, closeout_actual_runs)):
        if actual_runs < fallbacks + closeout_actual_runs:
            errors.append(
                f"{prefix}.actual_runs: expected at least actual_run_fallbacks + closeout_actual_runs"
            )
    if all(is_nonnegative_integer(item) for item in (hits, helper_invocations)):
        if hits > helper_invocations:
            errors.append(f"{prefix}.cache_hits: expected at most helper_invocations")
    if all(is_nonnegative_integer(item) for item in (fallbacks, helper_invocations)):
        if fallbacks > helper_invocations:
            errors.append(
                f"{prefix}.actual_run_fallbacks: expected at most helper_invocations"
            )

    if prefix == "summary":
        rate = value.get("cache_hit_rate")
        if is_nonnegative_number(rate) and rate <= 1 and is_nonnegative_integer(helper_invocations):
            expected_rate = hits / helper_invocations if helper_invocations > 0 else 0
            if is_nonnegative_integer(hits) and abs(rate - expected_rate) > MEASUREMENT_RATE_TOLERANCE:
                errors.append(
                    f"{prefix}.cache_hit_rate: expected cache_hits / helper_invocations"
                )
    return errors



def validate_measurement_validators(value: Any) -> list[str]:
    if not isinstance(value, list):
        return ["validators: expected array"]
    errors: list[str] = []
    for index, entry in enumerate(value):
        entry_path = path_label("validators", index)
        if not isinstance(entry, dict):
            errors.append(f"{entry_path}: expected object")
            continue
        if not is_nonempty_string(entry.get("validator_id")):
            errors.append(f"{entry_path}.validator_id: expected string")
        if not is_nonempty_string(entry.get("command_family")):
            errors.append(f"{entry_path}.command_family: expected string")
        for field in sorted(MEASUREMENT_VALIDATOR_COUNT_FIELDS):
            if field in entry and not is_nonnegative_integer(entry[field]):
                errors.append(f"{entry_path}.{field}: expected non-negative integer")
            elif field not in entry:
                errors.append(f"{entry_path}.{field}: missing required field")
        if "estimated_seconds_saved" not in entry:
            errors.append(f"{entry_path}.estimated_seconds_saved: missing required field")
        elif not is_nonnegative_number(entry["estimated_seconds_saved"]):
            errors.append(f"{entry_path}.estimated_seconds_saved: expected non-negative number")
        reason = entry.get("still_rerun_reason")
        if reason not in MEASUREMENT_STILL_RERUN_REASONS:
            allowed = ", ".join(sorted(MEASUREMENT_STILL_RERUN_REASONS))
            errors.append(f"{entry_path}.still_rerun_reason: expected one of: {allowed}")
        errors.extend(validate_measurement_count_relationships(entry, entry_path))
    return errors



def validate_measurement_closeout(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["closeout: expected object"]
    errors: list[str] = []
    if value.get("closeout_cache_skips") != 0:
        errors.append("closeout.closeout_cache_skips: expected 0")
    return errors



def validate_measurement_workstream_b(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["workstream_b_recommendation: expected object"]
    errors: list[str] = []
    state = value.get("state")
    if state not in WORKSTREAM_B_RECOMMENDATION_STATES:
        allowed = ", ".join(sorted(WORKSTREAM_B_RECOMMENDATION_STATES))
        errors.append(f"workstream_b_recommendation.state: expected one of: {allowed}")
    if not is_nonempty_string(value.get("rationale")):
        errors.append("workstream_b_recommendation.rationale: expected string")
    return errors



def validate_measurement_evidence(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["$: expected object"]

    errors = validate_measurement_required_fields(data)
    if data.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    if not is_nonempty_string(data.get("change_id")):
        errors.append("change_id: expected string")

    if "measurement_window" in data:
        errors.extend(validate_measurement_window(data["measurement_window"]))
    if "summary" in data:
        errors.extend(validate_measurement_summary(data["summary"]))
    if "validators" in data:
        errors.extend(validate_measurement_validators(data["validators"]))
    if "closeout" in data:
        errors.extend(validate_measurement_closeout(data["closeout"]))
    if "workstream_b_recommendation" in data:
        errors.extend(
            validate_measurement_workstream_b(data["workstream_b_recommendation"])
        )

    errors.extend(validate_safe_measurement_value(data))
    return list(dict.fromkeys(errors))


def validate_file(path: Path) -> list[str]:
    if is_measurement_file(path):
        return validate_measurement_evidence(load_yaml(path))
    # No legacy decoder: complete-set contract-selected validation owns format and path safety,
    # including malformed JSON, duplicate keys, symlinks and an absent manifest.
    try:
        result = subprocess.run(
            ["node", str(ROOT / "scripts/validate-record-store.mjs"), str(path.absolute())],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ["current record validator unavailable"]
    return [] if result.returncode == 0 else ["invalid or unsupported record set; supported contracts are rigorloop-records-v2 and rigorloop-records-v3"]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "usage: validate-change-metadata.py <change.json|validation-cache-measurement.yaml> [...]",
            file=sys.stderr,
        )
        return 2

    exit_code = 0
    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            errors = validate_file(path)
        except FileNotFoundError:
            print(f"{path}: file not found", file=sys.stderr)
            exit_code = 1
            continue
        except MetadataValidationError as exc:
            print(f"{path}: invalid change metadata", file=sys.stderr)
            print(f"  - {exc}", file=sys.stderr)
            exit_code = 1
            continue

        if errors:
            print(f"{path}: invalid change metadata", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            exit_code = 1
            continue

        print(f"{path}: valid change metadata")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
