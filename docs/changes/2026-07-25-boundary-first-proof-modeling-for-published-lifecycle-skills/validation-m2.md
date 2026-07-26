# M2 Runtime-Feasibility Evidence

Stage: implement
Milestone: M2 preflight
Result: pass
Diagnostic: none

## Commands

- `python scripts/test-boundary-proof.py BoundaryProofEnvironmentTests` —
  passed 18 focused tests.
- `python scripts/test-boundary-proof.py` — passed 34 tests.
- `python scripts/validate-skills.py` — validated 24 skills.
- `python scripts/test-skill-validator.py` — passed 259 tests.
- `python scripts/build-skills.py --check` — passed.
- `python -m py_compile scripts/boundary_proof_behavior.py
  scripts/test-boundary-proof.py` — passed.
- `python scripts/boundary_proof_behavior.py check-environment --change-id
  2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills
  --json` — passed and durably published the current attestation.
- `git diff --check` — passed.
- A minimal structured app-server turn through the same identified runtime,
  exact schema/protocol projection, event classifier, root requests, and
  permission profile returned `{"ok":true}` with 21 classified event methods.

## Bounded receipt

```json
{"attestation_ref":{"identity":"sha256:e8b2054a33be70ba0aef11d8040631bb3d0a402c95e8cfe9a2a9a2acf38a537d","path":"docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/runtime-preflight-attestation.json"},"diagnostic_id":"none","phase":"pre-turn-start","result":"pass","schema_version":"boundary-runtime-preflight-v1"}
```

The installed `boundary-runtime-attestation-v1` record binds the resolved
Codex launcher and runtime package, generated experimental schema bundle,
generated configuration, managed requirements, feature and capability
inventories, exact skill inventory, feature and protocol classifications,
thread metadata, named permission profile, direct sandbox probes, and
credential-isolation results.

No credential, canary, private path, raw configuration, raw inventory, or raw
protocol log is serialized. The preflight attestation is feasibility evidence
only; the later behavior-generation manifest must derive its own fresh
generation-time attestation.

## Implementation-discovered contract correction

Codex 0.144.6 reports five runtime-bundled system skills in the complete
`skills/list` result even when they are disabled. The first approved wording
required only the five manifested lifecycle skills and therefore could not
accept an honest complete runtime result.

The focused correction now requires an exact config-bound ten-row inventory:
five enabled manifested `user` skills and five disabled runtime `system`
skills, with forced refresh, one exact workspace row, empty errors, exact
paths and scopes, and unique raw and normalized paths. Spec-review R19 recorded
two determinism findings; the R20 candidate closes both before implementation
continues beyond the preflight boundary.

The runtime also emits one aggregate schema JSON file with nondeterministic
object-key order. The focused R21 candidate therefore hashes canonical JSON
for each generated schema file while preserving every object member and array
position. The complete `config/read` projection similarly verifies one
generated user-config source and a consistent format-valid runtime-owned
origin version before replacing temporary roots and that opaque version with
stable logical roles. Two consecutive live collections now produce identical
bounded attestations.

Codex advanced to 0.145.0 before canonical generation. The exact current
projection adds four feature rows and the runtime-system `review-agent`
package. The harness now requires a version-keyed 0.145.0 feature set,
explicitly disables all non-permitted additions and `review-agent`, and
requires an eleven-row skill inventory: the unchanged five enabled manifested
user skills plus six disabled runtime-system skills. The 0.145.0
`thread/start` response reports no runtime roots, so the bound protocol
records that exact response while requiring both thread and turn requests to
name only the isolated workspace; the independent sandbox probes remain the
enforcement proof.

## Handoff

The runtime feasibility gate and spec-review R26 are satisfied. M2 remains
`implementing` until architecture, plan, and test-spec review synchronization
and the remaining harness, immutable behavior-run, and validation work are
complete.
