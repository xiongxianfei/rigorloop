#!/usr/bin/env python3
"""Validate the versioned CLI result byte profile and adoption gates."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


PROFILE_NAMES = {
    "status", "context", "mutation-success", "mutation-blocked",
    "validation-failure", "unexpected-error",
}
ONE_PASS = {"status", "context", "mutation-success", "mutation-blocked"}


def measure(profiles_path: Path, baseline_path: Path) -> dict:
    profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if profiles.get("schema_version") != 1 or baseline.get("schema_version") != 1:
        raise ValueError("unsupported measurement schema")
    if profiles.get("profile_version") != baseline.get("profile_version"):
        raise ValueError("profile and baseline identities differ")
    current = {item["name"]: item for item in profiles.get("profiles", [])}
    prior = {item["name"]: item for item in baseline.get("profiles", [])}
    if set(current) != PROFILE_NAMES or set(prior) != PROFILE_NAMES:
        raise ValueError("profile vocabulary must contain exactly the six v1 profiles")
    rows = []
    for name in sorted(PROFILE_NAMES):
        before = prior[name]["complete_interaction_bytes"]
        after = current[name]["concise_bytes"]
        reduction = round((before - after) * 100 / before, 2)
        rows.append({"name": name, "baseline_bytes": before, "concise_bytes": after, "reduction_percent": reduction})
    median = round(statistics.median(row["reduction_percent"] for row in rows), 2)
    field_gate = all(item.get("required_fields_present") is True for item in current.values())
    one_pass_gate = all(current[name].get("lookup_required") is False for name in ONE_PASS)
    growth_gate = all(row["reduction_percent"] >= -10 for row in rows)
    eligible = median >= 30 and field_gate and one_pass_gate and growth_gate
    return {
        "schema_version": 1,
        "profile_version": profiles["profile_version"],
        "profiles": rows,
        "median_reduction_percent": median,
        "gates": {"median_30_percent": median >= 30, "per_profile_growth_limit": growth_gate, "required_fields": field_gate, "one_pass_continuation": one_pass_gate},
        "decision": "eligible-for-v0.5.0-review" if eligible else "keep-concise-opt-in",
        "default_changed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        report = measure(args.profiles, args.baseline)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"schema_version": 1, "status": "failed", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not args.check or all(report["gates"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
