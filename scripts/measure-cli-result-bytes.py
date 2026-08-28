#!/usr/bin/env python3
"""Validate the versioned CLI result byte profile and adoption gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import statistics
import tempfile
from pathlib import Path


PROFILE_NAMES = {
    "status", "context", "mutation-success", "mutation-blocked",
    "validation-failure", "unexpected-error",
}
ONE_PASS = {"status", "context", "mutation-success", "mutation-blocked"}
ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "packages/rigorloop/dist/bin/rigorloop.js"
BASELINE_SOURCE_REVISION = "bcc7ef14ae45e8df737d8a97e72eff3a3823446b"
BASELINE_COMMANDS = {
    "status": ["lifecycle", "status", "--change", "example", "--format", "json"],
    "context": ["lifecycle", "context", "code-review", "--change", "example", "--format", "json"],
    "mutation-success": ["init", "codex", "--dry-run", "--json"],
    "mutation-blocked": ["init", "unsupported", "--json"],
    "validation-failure": ["lifecycle", "validate", "--change", "example", "--format", "json"],
    "unexpected-error": ["init", "codex", "--from-archive", "{archive}", "--dry-run", "--json"],
}


def profile_fingerprint(profiles: list[dict]) -> str:
    encoded = json.dumps(profiles, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def write_governed_fixture(root: Path, malformed: bool = False) -> None:
    change_root = root / "docs/changes/example"
    spec_root = root / "specs"
    change_root.mkdir(parents=True)
    spec_root.mkdir(parents=True)
    (spec_root / "example.md").write_text("# Example\n", encoding="utf-8")
    if malformed:
        content = "change_id: example\nchange_id: duplicate\n"
    else:
        content = """change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  spec:
    kind: spec
    path: specs/example.md
    role: primary
    lifecycle_state: approved
workflow_state:
  lifecycle_state: active
  current_stage: implement
  next_stage: implement
  blocker: null
  evidence: []
  planned_work:
    current_milestone: M1
    milestones:
      M1:
        kind: implementation
        state: implementing
    remaining_implementation_milestones:
      - M1
review:
  status: approved
  unresolved_items: 0
"""
    (change_root / "change.yaml").write_text(content, encoding="utf-8")


def prepare_profile(profile: dict, root: Path) -> tuple[list[str], dict[str, str]]:
    setup = profile.get("setup")
    substitutions: dict[str, str] = {}
    if setup == "governed-active":
        write_governed_fixture(root)
    elif setup == "malformed-change":
        write_governed_fixture(root, malformed=True)
    elif setup == "invalid-archive":
        archive = root / "invalid-adapter.zip"
        archive.write_bytes(b"not-a-zip")
        substitutions["archive"] = str(archive)
    elif setup != "empty":
        raise ValueError(f"unknown profile setup: {setup}")
    args = [str(value).format(**substitutions) for value in profile.get("args", [])]
    if not args:
        raise ValueError(f"profile {profile.get('name')} has no CLI args")
    return args, substitutions


def normalized_bytes(stdout: bytes, stderr: bytes) -> int:
    return len(stdout.replace(b"\r\n", b"\n") + stderr.replace(b"\r\n", b"\n"))


def run_interaction(profile: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix="rigorloop-token-profile-") as directory:
        cwd = Path(directory)
        args, substitutions = prepare_profile(profile, cwd)
        env = {**os.environ, "RIGORLOOP_FILE_LOG": "off", "NO_COLOR": "1"}
        completed = subprocess.run([os.environ.get("NODE", "node"), str(CLI), *args], cwd=cwd, env=env, capture_output=True, check=False, timeout=30)
        expected_exit = profile.get("expected_exit")
        if completed.returncode != expected_exit:
            raise ValueError(f"profile {profile['name']} exited {completed.returncode}, expected {expected_exit}")
        try:
            payload = json.loads(completed.stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"profile {profile['name']} did not emit one JSON result") from error
        if payload.get("exit_code") != completed.returncode:
            raise ValueError(f"profile {profile['name']} projection exit differs from process exit")
        if payload.get("schema_version") != 2 or payload.get("projection") != "concise":
            raise ValueError(f"profile {profile['name']} did not emit concise result schema 2")
        missing = sorted(set(profile.get("required_fields", [])) - set(payload))
        total = normalized_bytes(completed.stdout, completed.stderr)
        follow_ups = profile.get("follow_ups", [])
        for follow_up in follow_ups:
            follow_args = [str(value).format(**substitutions, invocation_id=payload.get("invocation_id", "")) for value in follow_up]
            follow = subprocess.run([os.environ.get("NODE", "node"), str(CLI), *follow_args], cwd=cwd, env=env, capture_output=True, check=False, timeout=30)
            total += normalized_bytes(follow.stdout, follow.stderr)
        return {
            "concise_bytes": total,
            "required_fields_present": not missing,
            "missing_fields": missing,
            "lookup_required": bool(follow_ups),
            "observed_exit": completed.returncode,
        }


def measure(profiles_path: Path, baseline_path: Path) -> dict:
    profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if profiles.get("schema_version") != 1 or baseline.get("schema_version") != 1:
        raise ValueError("unsupported measurement schema")
    if profiles.get("profile_version") != baseline.get("profile_version"):
        raise ValueError("profile and baseline identities differ")
    if baseline.get("source_revision") != BASELINE_SOURCE_REVISION:
        raise ValueError("baseline source revision is missing or unsupported")
    if baseline.get("source_package_version") != "0.4.1":
        raise ValueError("baseline package version is missing or unsupported")
    if baseline.get("commands") != BASELINE_COMMANDS:
        raise ValueError("baseline detailed command mapping differs")
    if baseline.get("normalization") != "stdout-plus-stderr UTF-8 bytes after CRLF-to-LF normalization":
        raise ValueError("baseline normalization contract differs")
    profile_items = profiles.get("profiles", [])
    current = {item["name"]: item for item in profile_items}
    prior = {item["name"]: item for item in baseline.get("profiles", [])}
    if set(current) != PROFILE_NAMES or set(prior) != PROFILE_NAMES:
        raise ValueError("profile vocabulary must contain exactly the six v1 profiles")
    fingerprint = profile_fingerprint(profile_items)
    if baseline.get("profile_fingerprint") != fingerprint:
        raise ValueError("profile fixture identity differs from the immutable baseline")
    measured = {name: run_interaction(current[name]) for name in sorted(PROFILE_NAMES)}
    rows = []
    for name in sorted(PROFILE_NAMES):
        before = prior[name]["complete_interaction_bytes"]
        after = measured[name]["concise_bytes"]
        reduction = round((before - after) * 100 / before, 2)
        rows.append({"name": name, "baseline_bytes": before, "concise_bytes": after, "reduction_percent": reduction, "observed_exit": measured[name]["observed_exit"]})
    median = round(statistics.median(row["reduction_percent"] for row in rows), 2)
    field_gate = all(item["required_fields_present"] for item in measured.values())
    one_pass_gate = all(measured[name]["lookup_required"] is False for name in ONE_PASS)
    growth_gate = all(row["reduction_percent"] >= -10 for row in rows)
    eligible = median >= 30 and field_gate and one_pass_gate and growth_gate
    return {
        "schema_version": 1,
        "profile_version": profiles["profile_version"],
        "profile_fingerprint": fingerprint,
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
