# M2 Hermetic Upstream-Behavior Evidence

Stage: implement
Milestone: M2
Result: blocked
Diagnostic: stage-output-transport-contract-unavailable

## Current implementation discovery

The approved R45/R18 preflight correction now proves real direct and detached
descendant create, overwrite, removal, and permission-mode denial under
`boundary-proof-stage-readonly-v1`. It then fails closed at the separate real
app-server file-change denial probe:

```json
{"attestation_ref":null,"diagnostic_id":"sandbox-probe-failed","phase":"pre-turn-start","result":"environment-unavailable","schema_version":"boundary-runtime-preflight-v2","workspace_failure":null}
```

The exact probe prompt returns `{"probe":"complete"}`, but Codex 0.145.0 emits
zero `item/fileChange/requestApproval` requests and zero terminal declined
file-change items. The approved feature projection enables only
`shell_tool`, `unified_exec`, and `shell_snapshot`; the runtime exposes no
file-change operation under that configuration. A bounded feasibility
experiment that additionally selected `apply_patch_freeform`, and then both
`apply_patch_freeform` and `apply_patch_streaming_events`, failed earlier at
the capability inventory because those features remained disabled. Repeating
that experiment with an isolated disposable workspace-write probe profile
produced the same disabled-feature inventory, so separating probe authority
from lifecycle authority cannot make the operation observable in Codex
0.145.0.

This is not permission to accept the terminal marker as denial proof. The
required decline interaction is absent, so no current v2 attestation was
published. The prior v1 attestation remains historical bytes only.
Participating skills remain unchanged. M2 is blocked and routes to
architecture because the approved plan forbids a weaker fallback on
`environment-unavailable`.

Focused implementation evidence:

- `python scripts/test-boundary-proof.py` — passed 58 tests.
- `python -m py_compile scripts/boundary_proof_behavior.py
  scripts/test-boundary-proof.py` — passed.
- `python scripts/boundary_proof_behavior.py check-environment --change-id
  2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills
  --json` — failed closed with the bounded v2 receipt above.

The partial implementation adds the immutable v2 manifest, attestation,
artifact, integrity, file-change, canary, and opaque-v1 projections; real
direct and descendant command-denial probes; a parent-owned decline handler;
and policy-bound stage-envelope validation/materialization tests. It is not an
M2 completion claim.

The latest live canonical `generate` attempt failed closed with
`unexpected-prohibited-event` before publication.
The current pointer remains on historical run
`run-91e41340b56169c06158eca244fb117c`; that run predates the current
implementation and cannot satisfy the pending M2 correction.

Direct isolated app-server probes established the narrower boundary:

- the pinned runtime returns the required schema-constrained agent completion
  message;
- the same stage turn produces no files below the isolated output root;
- adding prompt instructions to use a workspace write tool does not expose
  such a tool or produce a file;
- the existing command-level workspace-write probe therefore proves a sibling
  capability, not the lifecycle stage-output transport required by R28y.

Implementation remains stopped.
The governing spec is being revised so each stage-owning skill authors a
closed artifact envelope and a semantics-free transport adapter materializes
the returned UTF-8 bytes exactly.
Architecture, plan, test-spec, implementation, and their review gates must be
synchronized before a new canonical run is eligible.

## Historical commands

The commands and results below describe the earlier M2 candidate.
They remain historical evidence only and do not override the current blocked
result.

- `python scripts/test-boundary-proof.py` — passed 49 tests, including the
  current immutable-run validation-only regression.
- `python scripts/validate-skills.py` — validated 24 skills.
- `python scripts/test-skill-validator.py` — passed 259 tests.
- `python scripts/build-skills.py --check` — passed.
- `python -m py_compile scripts/boundary_proof_behavior.py
  scripts/boundary_proof_model.py scripts/validate-boundary-proof.py
  scripts/test-boundary-proof.py` — passed.
- `python scripts/boundary_proof_behavior.py check-environment --change-id
  2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills
  --json` — passed and durably published the current attestation.
- `git diff --check` — passed.
- A minimal structured app-server turn through the same identified runtime,
  exact schema/protocol projection, event classifier, root requests, and
  permission profile returned `{"ok":true}` with 21 classified event methods.
- The controlled `exercise-fixture` followed by `validate-fixture` passed in
  a temporary output root.
- Canonical `generate` passed and published immutable run
  `run-91e41340b56169c06158eca244fb117c`.
- Canonical `validate` passed without runtime or lifecycle-skill reinvocation.

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
only. The current `behavior-implementation-manifest.json` contains a distinct
fresh generation-time attestation and transitively binds the current immutable
run.

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

## Historical immutable behavior result

```json
{"false_blocking_count":0,"input_set_identity":"sha256:b086ccd384d50212aca6e4956868dc33947d74abac02578d85f81a8133d7cfb2","new_universal_artifact_count":0,"result":"pass","run_id":"run-91e41340b56169c06158eca244fb117c","simple_fixture_structure_correction_cycles":0}
```

The standalone workflow coordinator invoked isolated `spec`, `spec-review`,
`test-spec`, and `test-spec-review` turns. Authoring turns returned complete
typed semantic records; review turns used distinct fresh threads and returned
durable formal review records bound to the exact generated artifact identities.
Both review outcomes were approved. The harness validated and formatted those
stage-owned records, reparsed them with the candidate parser, and published
them through the prepared-receipt transaction.

The correction loop also proved that formal review is substantive rather than
label-only: `spec-review` rejected an unrealizable canonically equivalent
unknown-mode evidence class. The contract removed that empty mandatory class,
recorded its non-applicability, added a regression, and passed rereview. Exact
semantic equality separately caught and corrected missing T3 ownership in the
canonical proof obligation.

## Handoff

M2 is not ready for code review.
The immediate next stage is focused spec-review of the stage-authored
artifact-envelope correction, followed by synchronized architecture, plan, and
test-spec review before implementation resumes.
