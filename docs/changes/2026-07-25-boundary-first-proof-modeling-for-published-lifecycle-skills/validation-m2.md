# M2 Hermetic Upstream-Behavior Evidence

Stage: implement
Milestone: M2
Result: pass
Diagnostic: none

## 2026-07-27 current canonical result

The current immutable upstream behavior run is:

```json
{"false_blocking_count":0,"input_set_identity":"sha256:381be42985b3bf9d52f6cd17b298ddc8adb1d67cc05c0b633b391b11f2716a18","new_universal_artifact_count":0,"result":"pass","run_id":"run-8f095d95abb863dbcbd642fe61abd65e","simple_fixture_structure_correction_cycles":1}
```

The run completed fresh `spec`, `spec-review`, `test-spec`, and
`test-spec-review` occurrences with stage-owned artifacts and independent
approving reviews.
It introduced no universal lifecycle artifact and produced no false block.

The current run also closes the publisher transaction gap:

- its exact manifest contains
  `publisher_instance_id: publisher-fdedafd502f871013353ae28a7af7683`;
- the lease was durable before the first stage workspace existed;
- every child workspace was created below the lease-bound working root with a
  hermetic project marker, preventing ancestor skill/instruction discovery;
- the prepared receipt bound publisher, run, input, staged snapshot, immutable
  target, and prior pointer identities;
- successful publication left no publisher lease, prepared receipt, working
  root, staging root, or temporary pointer; and
- five deliberately interrupted live attempts were preserved through
  evidence-bound completed recovery records and quarantine rather than
  adoption or silent deletion; and
- the focused recovery proof crashes and resumes after each durable recovery
  boundary: temporary-state fsync, immutable basis installation, authorized
  state persistence, quarantine rename, orphan-detached persistence, and
  publisher-lease deletion.

The R6 correction additionally proves object-complete recovery classification:

- completed history consumes only its exact validated history objects and
  cannot hide same-run active staging;
- recoverable staging must pass the same complete semantic validation used
  before publication;
- recovery authority is contained within the selected change record;
- fixed control roots have exact object kinds before candidate routing; and
- malformed correction traces fail before staged publication.

The R7 correction closes destructive-recovery authority:

- the only accepted authority path is
  `docs/changes/<change-id>/recovery-decisions/<run-id>.json`;
- the decision has one closed schema and an `authorized` outcome;
- change, run, publisher, input identity, action, and actor must match the
  selected lease and recovery basis exactly;
- every missing, added, or changed decision field rejects before mutation;
- arbitrary change-local Markdown and wrong decision paths reject; and
- decision-byte drift after authorization cannot resume an active recovery.

The focused correction also closed both bounded correction publication paths:

- feature-spec and test-spec corrections each assemble one identity-bound
  trace with one correction maximum;
- both assemblers write the canonical `manifest.json`;
- extension presence and decomposition remain stage-owned and review-owned;
- the deterministic fixture oracle excludes extension identity;
- the published boundary reference and parser define one closed optional
  extension table; and
- the published reference exposes the narrower `x.<namespace>.<dimension>`
  extension-ID grammar already required by R28c and R28t.

Current validation:

- `python scripts/boundary_proof_behavior.py validate --change-id
  2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` —
  passed against the immutable current run without lifecycle reinvocation.
- `python scripts/test-boundary-proof.py` — passed 100 tests.
- `python scripts/validate-skills.py` — validated 24 skills.
- `python scripts/test-skill-validator.py` — passed 259 tests.
- `python scripts/build-skills.py --check` — passed.
- `python -m py_compile scripts/boundary_proof_behavior.py
  scripts/boundary_proof_model.py scripts/validate-boundary-proof.py
  scripts/test-boundary-proof.py` — passed.
- `git diff --check` — passed.

All sections below this current result are chronological implementation
history. They do not override the current passing result.

## 2026-07-27 invariant-oracle implementation correction

The R54 invariant-oracle contract is now implemented and locally proved:

- candidate and produced artifacts are normalized independently;
- deterministic comparison uses only version, scope, requirement, core
  dimension, extension, and proof-governing-requirement invariants;
- stage-owned IDs, applicability, rationale, decomposition, examples,
  interactions, automation levels, proof grouping, and test IDs are excluded
  from candidate equality;
- candidate paths, identities, and bytes are checked across serialized child
  requests, child workspace inventory, and bounded access surfaces;
- both formal reviews receive the exact authoritative scenario;
- deterministic stage structure failures emit `boundary-oracle-mismatch`;
- valid formal nonapproval emits `review-nonapproval`; and
- mutually exclusive approval and nonapproval artifact sets retain their bound
  occurrence and reconcile independently.

The public boundary reference now states the previously implicit executable
boundaries: exact dotted stable-ID grammar, the allowed uppercase numeric test
ID grammar, ASCII empty-cell sentinel, applicability-dependent fields, global
boundary uniqueness, example ownership, interaction selection, proof-map
coverage, and contiguous boundary-record ordering. These are general
serialization and proof rules, not fixture-candidate examples.

Focused validation passes:

- `python scripts/test-boundary-proof.py` — passed 73 tests.
- `python scripts/validate-skills.py` — validated 24 skills.
- `python scripts/test-skill-validator.py` — passed 259 tests.
- `python scripts/build-skills.py --check` — passed.
- `python -m py_compile scripts/boundary_proof_behavior.py
  scripts/boundary_proof_model.py scripts/validate-boundary-proof.py
  scripts/test-boundary-proof.py` — passed.
- `git diff --check` — passed.

The live capability-bound path advanced through accepted `spec`,
`spec-review`, and `test-spec` envelopes in multiple attempts. Independent
review correctly found omitted interaction and record-ordering boundaries
before the published guidance was corrected; later review passed those gates.
The proof parser now accepts equivalent Markdown test headings rather than
requiring the fixture candidate's bare-heading presentation.

No fresh immutable run has been published. The most recent two clean attempts
stopped before the first accepted envelope at the fixed transport boundary.
Earlier failed attempts stopped with deterministic `boundary-oracle-mismatch`
or semantic `review-nonapproval` and changed neither immutable staging nor the
current pointer. The historical pointer remains non-current. M2 therefore
remains `resolution-needed` and is not ready for code review.

## 2026-07-27 current implementation discovery

The capability-bound v3 preflight now passes and publishes current evidence:

```json
{"attestation_ref":{"identity":"sha256:7ca2cfb30c6d8926dbb2439b68dedf686a121da1542a9dc28723118493034835","path":"docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/runtime-preflight-attestation.json"},"diagnostic_id":"none","phase":"pre-turn-start","result":"pass","schema_version":"boundary-runtime-preflight-v3","workspace_failure":null}
```

The pass binds the exact launcher, runtime package, schema bundle, protocol
classification, feature classification, eleven-field runtime projection,
3/4/89 feature partition, effective-tool projection, and production-handler
conformance. The reported Codex version is one selector field, not sufficient
authority by itself.

Focused validation also passes:

- `python scripts/test-boundary-proof.py` — passed 64 tests.
- `python scripts/validate-skills.py` — validated 24 skills.
- `python scripts/test-skill-validator.py` — passed 259 tests.
- `python scripts/build-skills.py --check` — passed.
- `python -m py_compile scripts/boundary_proof_behavior.py
  scripts/boundary_proof_model.py scripts/validate-boundary-proof.py
  scripts/test-boundary-proof.py` — passed.
- `git diff --check` — passed.

Canonical generation still fails closed before staging, receipt creation,
immutable installation, or pointer replacement. The current pointer remains
on historical run `run-91e41340b56169c06158eca244fb117c`.

The fresh stage now receives the exact user-request semantics, the installed
boundary reference, an inline capability-preserving completion gate, and an
exact portable record skeleton. The resulting records nevertheless vary in
stable IDs, non-applicability rationales, row ownership, and proof
decomposition. R28y currently requires equality of every normalized oracle
field, so structurally closed and independently reviewable alternatives are
rejected unless they reproduce one hidden golden decomposition.

That is an upstream contract issue. Retrying another model sample is not a
safe resolution, and relaxing the implementation below the approved R28y
comparison would violate the spec. M2 remains blocked pending formal
code-review classification and, if confirmed, a focused spec amendment that
separates exact structural/semantic invariants from reviewer-owned modeling
choices.

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

## 2026-07-27 capability-projection preflight correction

The v3 evidence-only preflight stopped before publication:

```json
{"attestation_ref":null,"diagnostic_id":"file-change-control-mismatch","phase":"pre-thread-start","result":"environment-unavailable","schema_version":"boundary-runtime-preflight-v3","workspace_failure":null}
```

This receipt failed closed but is not conforming current evidence: its
`file-change-control-mismatch` / `pre-thread-start` pair is forbidden by the
closed cause-to-phase table, which assigns the observed
`required-disabled-feature-enabled` cause to `pre-turn-start`. The receipt is
retained only as a negative diagnostic fixture. The independently observed
96-row inventory below remains bounded discovery evidence.

The deterministic implementation suite passed 60 tests before this live
preflight. The exact bound runtime inventory contained 96 unique rows with
these enabled features:

```text
shell_snapshot
shell_tool
unified_exec
terminal_resize_reflow
tool_search_always_defer_mcp_tools
resize_all_images
tui_app_server
```

The first three are the reviewed permitted command tools. The remaining four
are already classified by the approved feature model as permitted non-tool
runtime behavior. They do not expose a child-invocable tool or file-change
operation, but the approved ten-field runtime row incorrectly included them in
the 93-member required-disabled set.

The preflight therefore proved a contract-model gap: the runtime projection
needs three pairwise-disjoint exhaustive feature sets rather than the approved
binary partition. The focused correction adds
`permitted_non_tool_features`, yielding an eleven-field row with three
permitted tools, four permitted non-tool behaviors, and 89 required-disabled
tool-bearing features. No pass attestation, implementation manifest, immutable
run, pointer, skill mutation, or publication was produced.

Implementation remains blocked until the focused spec, architecture, plan, and
test-spec amendments are independently approved.
