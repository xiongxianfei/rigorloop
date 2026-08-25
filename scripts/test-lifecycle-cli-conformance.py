#!/usr/bin/env python3
"""Validate the shared governed-lifecycle conformance fixture and Node parser."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "packages/rigorloop/test/fixtures/lifecycle/conformance-v1.json"


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise SystemExit("unknown conformance fixture schema_version")
    required = {"valid_yaml", "invalid_yaml", "provenance_excluded_fields", "protected_failures"}
    unknown = set(payload) - {"schema_version", *required}
    missing = required - set(payload)
    if unknown or missing:
        raise SystemExit(f"fixture vocabulary mismatch: missing={sorted(missing)} unknown={sorted(unknown)}")
    if len(set(payload["protected_failures"])) != len(payload["protected_failures"]):
        raise SystemExit("protected failure IDs must be unique")
    if payload["provenance_excluded_fields"] != ["actor", "recorded_at"]:
        raise SystemExit("provenance exclusion contract drift")
    script = """
      import { readFileSync } from 'node:fs';
      import { parseLifecycleYaml } from './packages/rigorloop/dist/lib/lifecycle-contract.js';
      const fixture = JSON.parse(readFileSync(process.argv[1], 'utf8'));
      parseLifecycleYaml(fixture.valid_yaml);
      for (const entry of fixture.invalid_yaml) {
        let rejected = false;
        try { parseLifecycleYaml(entry.source); } catch { rejected = true; }
        if (!rejected) throw new Error(`fixture unexpectedly accepted: ${entry.id}`);
      }
    """
    subprocess.run(
        ["node", "--input-type=module", "-e", script, str(FIXTURE)],
        cwd=ROOT,
        check=True,
    )
    print(
        "lifecycle CLI conformance fixture passed "
        f"(invalid={len(payload['invalid_yaml'])}, protected={len(payload['protected_failures'])})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
