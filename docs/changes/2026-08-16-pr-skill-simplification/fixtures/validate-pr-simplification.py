#!/usr/bin/env python3
"""Validate change-local PR simplification ledgers and deterministic baseline."""

import hashlib
import json
from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = CHANGE.parents[2]


def load(name: str) -> dict:
    with (CHANGE / name).open(encoding="utf-8") as stream:
        return json.load(stream)


def unique(rows: list[dict], field: str, label: str) -> None:
    values = [row[field] for row in rows]
    assert values, f"{label} must not be empty"
    assert len(values) == len(set(values)), f"duplicate {label} {field}"


rules = load("pr-rule-disposition.yaml")["rules"]
unique(rules, "id", "rules")
allowed_dispositions = {
    "preserve-inline", "clarify-inline", "add-inline", "move-reference",
    "clarify-verify", "replace-inline", "move-asset"
}
assert all(row["disposition"] in allowed_dispositions for row in rules)

literals = load("pr-literal-compatibility.yaml")["literals"]
unique(literals, "id", "literals")
allowed_classes = {"normative-contract", "structural-contract", "test-consumed"}
assert all(row["classification"] in allowed_classes for row in literals)

basis = load("verify-basis-disposition.yaml")["fields"]
unique(basis, "id", "verification-basis fields")
assert {row["field"] for row in basis} == {
    "repository_identity", "remote_identity", "base_branch", "base_revision",
    "merge_base_revision", "head_branch", "verified_subject_revision"
}

fixture = load("fixtures/pr-simplification-scenarios.json")
for name, vocabulary in fixture["vocabularies"].items():
    assert vocabulary["allowed"], f"empty vocabulary: {name}"
    assert "unknown_value" in vocabulary["invalid"], f"missing unknown fixture: {name}"
    assert not set(vocabulary["allowed"]) & set(vocabulary["invalid"])
scenarios = fixture["scenarios"]
unique(scenarios, "id", "scenarios")
required_families = {"intent", "authority", "refresh", "branch", "pr-state", "ci", "basis", "evidence-tail", "reread", "concurrency", "partial-success", "read-back", "resource"}
assert required_families <= {row["family"] for row in scenarios}
allowed_results = set(fixture["vocabularies"]["operation"]["allowed"])
assert all(row["result"] in allowed_results for row in scenarios)

skill = (ROOT / "skills/pr/SKILL.md").read_bytes().replace(b"\r\n", b"\n")
assert len(skill) == 11375, f"PR baseline bytes changed: {len(skill)}"
assert len(skill.decode("utf-8").split()) == 1678, "PR baseline words changed"
assert hashlib.sha256(skill).hexdigest() == "c122a3bca9c59c19075464b9bda1d69f3dc1f51e13b40724deb684c6912cd407"

print(f"validated {len(rules)} rules, {len(literals)} literals, {len(basis)} basis fields, and {len(scenarios)} scenarios")
