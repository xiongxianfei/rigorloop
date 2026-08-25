#!/usr/bin/env python3
"""Measure governed-skill lifecycle mechanics after CLI migration."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANGE_ID = "2026-08-24-governed-lifecycle-cli"
BASELINE_REVISION = "c043b2c2"
MINIMUM_REDUCTION_PERCENT = 30.0

PROFILES = (
    ("proposal", "proposal", "skills/proposal/references/governed-proposal-authoring.md", 759),
    ("spec", "spec", "skills/spec/references/governed-spec-authoring.md", 882),
    ("architecture", "architecture", "skills/architecture/references/governed-architecture-authoring.md", 994),
    ("plan", "plan", "skills/plan/references/governed-plan-authoring.md", 899),
    ("test-spec", "test-spec", "skills/test-spec/references/governed-test-spec-authoring.md", 1074),
    ("proposal-review", "proposal-review", "skills/proposal-review/references/proposal-review-recording-and-settlement.md", 1342),
    ("spec-review", "spec-review", "skills/spec-review/references/governed-spec-review-settlement.md", 881),
    ("architecture-review", "architecture-review", "skills/architecture-review/references/architecture-review-recording-and-settlement.md", 1382),
    ("plan-review", "plan-review", "skills/plan-review/references/governed-plan-review-settlement.md", 690),
    ("test-spec-review", "test-spec-review", "skills/test-spec-review/references/test-spec-review-recording-and-settlement.md", 1241),
)


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text.split()), math.ceil(len(text) / 4))


def context_tokens(stage: str) -> int:
    command = [
        "node", "packages/rigorloop/dist/bin/rigorloop.js", "lifecycle", "context", stage,
        "--change", CHANGE_ID, "--format", "json",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if not result.stdout.strip():
        raise RuntimeError(f"context command produced no JSON for {stage}: {result.stderr.strip()}")
    parsed = json.loads(result.stdout)
    return estimate_tokens(json.dumps(parsed.get("context", {}), sort_keys=True, separators=(",", ":")))


def main() -> int:
    rows = []
    baseline_mechanics = current_mechanics = semantic_guidance = returned_context = 0
    for name, stage, reference, baseline in PROFILES:
        current = estimate_tokens((ROOT / reference).read_text(encoding="utf-8"))
        semantic = estimate_tokens((ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8"))
        context = context_tokens(stage)
        rows.append({"profile": name, "baseline_mechanics": baseline, "current_mechanics": current, "semantic_guidance": semantic, "returned_cli_context": context})
        baseline_mechanics += baseline
        current_mechanics += current
        semantic_guidance += semantic
        returned_context += context
    reduction = round((baseline_mechanics - current_mechanics) * 100 / baseline_mechanics, 1)
    mechanics_plus_context = current_mechanics + returned_context
    combined_reduction = round((baseline_mechanics - mechanics_plus_context) * 100 / baseline_mechanics, 1)
    report = {
        "schema_version": 1,
        "change_id": CHANGE_ID,
        "baseline_revision": BASELINE_REVISION,
        "token_estimate": "max(words, ceil(utf8-text-characters/4))",
        "profiles": rows,
        "totals": {
            "baseline_mechanics": baseline_mechanics,
            "current_mechanics": current_mechanics,
            "mechanics_reduction_percent": reduction,
            "mechanics_plus_context": mechanics_plus_context,
            "mechanics_plus_context_reduction_percent": combined_reduction,
            "semantic_guidance": semantic_guidance,
            "returned_cli_context": returned_context,
        },
        "threshold_percent": MINIMUM_REDUCTION_PERCENT,
        "status": "passed" if reduction >= MINIMUM_REDUCTION_PERCENT and combined_reduction >= MINIMUM_REDUCTION_PERCENT else "failed",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
