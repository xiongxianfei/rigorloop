# Boundary-First Proof Modeling for Published Lifecycle Skills

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Change ID: 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills
- Start date: 2026-07-25
- Last updated: 2026-07-27
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved boundary-model v1 contract so examples remain useful
without becoming the completeness model.
The implementation must move omitted-boundary detection before code review,
preserve the behavior of eight published lifecycle skills, and establish one
portable, computed capability baseline before progressive-disclosure work
resumes.

## Source artifacts

- Proposal: `docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md`
- Specs: `specs/rigorloop-workflow.md` R28-R28z and `specs/skill-contract.md` R56-R56q
- Latest spec review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r55.md` (approved extension-oracle correction)
- Architecture: `docs/architecture/system/architecture.md` (approved by architecture-review R27)
- ADR: `docs/adr/ADR-20260725-boundary-first-proof-modeling.md` (accepted by architecture-review R15)
- Transport ADR: `docs/adr/ADR-20260726-stage-authored-artifact-envelope-transport.md` (accepted; scoped clauses superseded by the capability-projection ADR)
- Capability-projection ADR: `docs/adr/ADR-20260727-capability-projected-file-change-control.md` (accepted by architecture-review R22)
- Three-category projection ADR: `docs/adr/ADR-20260727-three-category-runtime-feature-projection.md` (accepted by architecture-review R25)
- Runtime-attestation ADR: `docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md`
- Architecture review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/architecture-review-r27.md`
- Plan review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/plan-review-r21.md` (approved extension-oracle synchronization)
- Test specs: `specs/rigorloop-workflow.test.md` R28-R28z and `specs/skill-contract.test.md` R56-R56q; R55/R27/R21 identity synchronization is complete and focused test-spec review remains pending

## Context and orientation

The approved R54 R28y contract and R26 architecture are now normative.
Live M2 generation proved that the pinned app-server returns
schema-constrained stage messages but does not expose the assumed stage-agent
workspace-write surface or a file-change operation under the approved
configuration. The accepted replacement gives every child a read-only
workspace with no writable root, selects an exact-runtime-bound immutable
capability projection, proves the production deny-only dispatcher before both
capability branches, captures a root-anchored before/after integrity
observation, and lets only the parent materialize the stage-authored envelope
after an unchanged result. Implementation remains paused until this plan and
the matching test spec project that replacement and pass review.
`scripts/boundary_proof_model.py` will be their immutable typed projection and
pure aggregate evaluator.
`scripts/boundary_proof_behavior.py` will be the standalone hermetic behavior
harness and immutable-run publisher; it is not a workflow-automation engine.
`scripts/validate-boundary-proof.py` will be the sole capability-report writer.
The first release governs exactly:

```text
spec
spec-review
test-spec
test-spec-review
implement
code-review
verify
workflow
```

Each skill will map a byte-identical
`references/boundary-proof-model.md` resource copied from
`templates/shared/boundary-proof-model.md`.
Existing adapter generation and resource-integrity validation must carry that
resource through generated, packed, and installed outputs.

## Non-goals

- Do not add a lifecycle stage or a universal per-change boundary artifact.
- Do not update the other six lifecycle skills in this slice.
- Do not let executable constants override approved spec semantics.
- Do not make structural validators judge semantic adequacy.
- Do not resume capability-preserving progressive disclosure.
- Do not activate a release or perform publication, PR, or deployment actions.

## Requirements covered

| Requirement set | Implementation milestone |
| --- | --- |
| R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p | M1 typed projection, structural validation, executable incidents, synthetic trace, and report correction |
| R28y, R56-R56e, R56j-R56k, R56p | M2 pre-harness feasibility, standalone harness/recovery, upstream skills, and fresh upstream behavior |
| R28f-R28j, R56f-R56i, R56l | M3 downstream implementation/review/verify/workflow projection and preservation |
| R28l-R28o, R28z, R56n, R56q | M4 selector, adapter parity, current aggregation, activation, and rollback proof |

## Current Handoff Summary

- Current milestone: M2. Hermetic harness, upstream skills, and fresh upstream behavior
- Current milestone state: resolution-needed
- Latest review evidence: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r9.md
- Review status: changes-requested; stage=code-review; round=r9
- Remaining in-scope implementation milestones: M2, M3, M4
- Next stage: spec-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending — review-state=open; open-count=2; open-findings=BFP-CR-M2-14,BFP-CR-M2-15

## Milestones

### M1. Deterministic core correction

- Milestone state: closed
- Goal: Close every M1 code-review finding in the deterministic model, fixtures, synthetic trace, and report engine without invoking lifecycle skills.
- Requirements: R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p
- Files/components likely touched:
  - `scripts/boundary_proof_model.py`
  - `scripts/validate-boundary-proof.py`
  - `scripts/test-boundary-proof.py`
  - `tests/fixtures/boundary-proof/`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/validation-m1.md`
- Dependencies:
  - Approved R13 specs, accepted R4 architecture/ADR, and revised active test specs
- Tests to add/update:
  - Stable and unique regression/discovery IDs plus exact requirement ownership for each proof reference
  - Exact eight-row incident ID, seeded-omission, and gate registry mutation cases
  - Complete marker/scope presence and parity matrix, including fully markerless grandfathering and contradictory partial state
  - Missing, unsafe, non-regular, stale, substituted, and wrong-kind evidence references plus exact not-run blockers
  - Canonical byte serialization across semantically equivalent mapping permutations
  - Eight executable boundary-state incident fixtures with detected stage, diagnostic, code-review escape, and sibling-bypass results
  - Synthetic four-stage simple-change trace with derived applicable-only proof map, artifact count, false blocking, and correction cycles
- Implementation steps:
  - Add failing tests for BFP-M1-CR1 through BFP-M1-CR7 before correcting production behavior.
  - Enforce the complete closed ID/ownership, incident registry, marker parity, evidence identity/blocker, canonical serialization, incident replay, and synthetic trace contracts.
  - Keep M1 behavior proof synthetic: do not invoke lifecycle skills or claim published-skill preservation.
- Validation commands:
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py --help`
  - `python -m py_compile scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
- Promotion evidence:
  - direct negative regression for every BFP-M1-CR1 through BFP-M1-CR7 escape
  - current synthetic incident and simple-trace results only
  - focused validation recorded in `validation-m1.md`
  - clean M1 code-review R2 or later before M2 starts
- Failure stop:
  - Stop on any remaining adversarial escape, unknown-value fall-through, stale evidence acceptance, noncanonical report bytes, or failed validation.
- Expected observable result: Every R1 adversarial probe fails closed and the deterministic engine computes synthetic results without asserting published behavior.
- Commit message: `M1: close boundary core review findings`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Parser correction could still compress multi-property requirements or accept unknown values through fall-through.
- Rollback/recovery:
  - Revert the M1 script/fixture correction as one unit; no published skill depends on it before M2.

### M2. Hermetic harness, upstream skills, and fresh upstream behavior

- Milestone state: resolution-needed
- Goal: Prove runtime feasibility, freeze the pre-mutation baseline, implement the standalone recoverable harness, update the five participating skill packages, and publish the one fresh upstream behavior run owned by R28y M2.
- Requirements: R28y, R56-R56e, R56j-R56k, R56p
- Files/components likely touched:
  - `scripts/boundary_proof_behavior.py`
  - `scripts/boundary_proof_model.py`
  - `scripts/validate-boundary-proof.py`
  - `scripts/test-boundary-proof.py`
  - `tests/fixtures/boundary-proof/behavior/`
  - `tests/fixtures/boundary-proof/runtime/`
  - `tests/fixtures/boundary-proof/transport/`
  - `tests/fixtures/boundary-proof/simple-change/`
  - `templates/shared/boundary-proof-model.md`
  - `skills/workflow/SKILL.md`
  - `skills/workflow/references/boundary-proof-model.md`
  - `skills/spec/SKILL.md`
  - `skills/spec/references/boundary-proof-model.md`
  - `skills/spec-review/SKILL.md`
  - `skills/spec-review/references/boundary-proof-model.md`
  - `skills/test-spec/SKILL.md`
  - `skills/test-spec/references/boundary-proof-model.md`
  - `skills/test-spec-review/SKILL.md`
  - `skills/test-spec-review/references/boundary-proof-model.md`
  - `tests/fixtures/skills/boundary-proof/`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/behavior-implementation-manifest.json`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/boundary-proof-baseline.json`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/validation-m2.md`
- Dependencies:
  - M1 closed
- Tests to add/update:
  - Runtime supported/unsupported version; exact executable and generated
    experimental-schema identity; experimental-API negotiation; missing,
    null, additional, or incompatible app-server fields
  - SemVer cases below, at, and above 0.138.0, prerelease/build precedence,
    malformed versions, and exact CLI/package version equality
  - Launcher and runtime-package removal, replacement, or raw-byte/filesystem
    identity mutation before and after schema generation, every sandbox probe,
    app-server negotiation, and the accepted lifecycle invocation
  - Fully paginated `experimentalFeature/list`; missing, duplicate, unknown,
    newly enabled prohibited, and disabled prohibited feature rows; exact
    `config/read`, `configRequirements/read`, `app/list`, `plugin/list`,
    `mcpServerStatus/list`; and complete `skills/list` inventory with exactly
    five enabled manifested lifecycle packages plus the exact six
    generated-config-bound disabled, runtime-home-rooted, classified
    runtime-system rows; force reload, empty errors, exact scopes, and unique
    raw and normalized paths
  - Exact Codex 0.145.0 canonical schema and protocol-classification
    identities; exact launcher and runtime-package identities; exact
    eleven-field runtime-projection identity; exact 96-row feature partition;
    exact equality between each projection collection and its corresponding
    feature-classification category; and explicit disabled `review-agent`
    within the six-row system roster.
    Prove no match, multiple matches, duplicate ID/key/identity, unknown field,
    identity/content disagreement, and changed runtime bytes with unchanged
    version/schema/protocol/feature declarations. Swap one member between every
    category pair while preserving 3/4/89 counts, uniqueness, disjointness,
    exhaustiveness, and a recomputed identity; every swap must fail before
    `thread/start`.
  - Empty runtime roots in the exact 0.145.0 `thread/start` response while
    both outbound thread and turn requests bind one exact isolated workspace
    root; missing, added, substituted, or reordered-root contrasts
  - Every observed request/notification classified against the pinned
    projection; unknown and prohibited traffic rejected; remote-control status
    accepted only when disabled and unbound
  - Parent runtime proxy environment closed to the upper/lowercase proxy-name
    set while spawned commands retain the exact inherit-none environment
  - Empty `dynamicTools` and `environments`; command tools closed to
    `shell_tool`, `unified_exec`, and `shell_snapshot` under the exact
    read-only profile; direct create, overwrite, remove, and mode-change
    denial; the same four denials for a detached descendant followed by
    bounded exit/reap; prohibited schema variants that remain disabled; and
    rejection of every observed prohibited item/event
  - Exactly-one feature-row classification as permitted built-in tool,
    permitted non-tool runtime behavior, or must-be-disabled tool-bearing
    behavior; independently, exactly-one generated protocol-item
    classification as permitted side effect, non-side-effect protocol traffic,
    or prohibited capability event; missing, duplicate, unknown, and
    unclassified contrasts for both mappings; and proof that
    `permitted-side-effect` classifies protocol traffic rather than granting
    mutation authority
  - Exact `stage-file-change-authorization-policy-v1` fields, ordering, and
    canonical identity; complete effective-tool projection identity; and the
    exact `stage-file-change-handler-conformance-v1` policy/result schemas.
    Exercise every conformance case against the production dispatch and
    response-validation functions in fresh preflight and generation runs.
    Missing, failed, malformed, stale, reordered, incomplete, or
    identity-inconsistent conformance results must leave invocation counters
    for both capability branches, the canary, every governed lifecycle turn,
    and successful attestation assembly at zero.
  - Capability-state branches: `exposed-live-probe-required` additionally
    proves one matching request, `decision: decline`, generic carriers,
    terminal `declined`, unchanged workspace, no lifecycle output, and clean
    stop/reap; `not-exposed-projection` additionally proves the exact reviewed
    runtime bytes, all 89 required-disabled tool-bearing features disabled,
    four permitted non-tool behaviors allowed to remain enabled, only three
    permitted command features enabled within the effective-tool projection,
    and rejection of any observed
    file-change event as drift. Event absence alone is never sufficient.
  - Closed file-change cause-to-phase and diagnostic precedence rows,
    including unknown and cross-phase rejection plus separation of successful
    attestation fields from failure-only diagnostic evidence. Directly prove
    `required-disabled-feature-enabled` maps only to
    `file-change-control-mismatch` at `pre-turn-start`; reject the stale
    `pre-thread-start` pair and every alternate phase before runtime execution.
  - One shared file-change policy and handler identity across denial probe,
    materialization canary, lifecycle stage, and fresh retry; missing,
    substituted, widened, or response-selected handlers fail before output
    acceptance; reconciliation performs no child turn.
  - Missing profile attestation, wrong effective sandbox, writable child root,
    mismatched `boundary-proof-stage-readonly-v1` or
    `isolated-workspace-readonly-no-network-v1`, profile/config
    mismatch between app-server and `codex sandbox --include-managed-config`,
    unavailable or unsafe model metadata, and secret-free evidence cases
  - Transient-canary absence from the exact child environment-name allowlist,
    argv, stdin, private paths, and readable process metadata
  - Sole allowed repository import plus relative, wildcard, third-party, other local, and dynamic-import rejections
  - Complete five-skill resource-map set; missing, extra, stale, escaping, non-regular, and unmapped resource contrasts
  - Root and nested applicable/inapplicable `AGENTS.md` discovery
  - Harness prompt identity from module constant plus scenario identity
  - Runtime executable/version/model/instruction/tool/Python identity mismatch, unavailable, and unsafe cases
  - Caller-supplied instruction, unexpected tool, connector, subagent, network, and unmanifested read rejection
  - Validation under a different validator environment without profile replacement
  - Crash points before prepared-receipt write, after prepared-receipt fsync,
    after immutable-run install, after pointer replace, after parent fsync, and
    before receipt removal; every resume validates staged or installed
    identities and never reinvokes lifecycle skills
  - Phase-aware rollback with an absent, reconcilable, or irreconcilable
    prepared receipt; validated prior pointer versus no prior current run;
    exact registered-v1 restoration versus no current manifest; complete
    compatibility-unit reversion; non-current v3 retention; and rejection of
    every dangling v3 manifest, attestation, pointer, selector, or report
    reference
  - Stage timeout with absent output then one success; two absent-output
    timeouts; complete-output reconciliation without reinvocation; partial or
    extra output stop; and non-retry of protocol or security failures
  - Exact lifecycle and canary workspace-integrity policies; retained-root,
    no-follow, strict-UTF-8, descriptor-stability, regular-file hashing, entry,
    path-byte, aggregate-path-byte, observation-byte, and deadline boundaries;
    complete/overflow/invalid scan states; every closed failure reason and
    precedence; and the intrinsic 271-byte maximum for
    `workspace-baseline-failure-v1`
  - Pre-turn baseline failure before `thread/start`; post-turn comparison only
    after normal completion or confirmed stop/reap; no inspection under
    uncertain liveness; created, changed, removed, symlinked, replaced, or
    non-regular entries route to `stage-workspace-mutated`; unavailable,
    raced, unstable, unreadable, or unsupported inspection routes to
    `stage-workspace-inspection-failed`; neither route materializes,
    publishes, or retries
  - Candidate-message raw-byte equality/one-byte-over and canonical-envelope
    equality/one-byte-over limits, cardinality and aggregate overflow,
    complete/absent/partial/extra/contradictory states, complete diagnostic
    tuples, and exact closed routing for accept, reconcile, retry, pause, and
    fail-closed
  - Parent-only materialization after a complete unchanged observation, using
    the retained root descriptor; exact ordered paths and UTF-8 bytes; complete
    reread and structural content observations; no harness-authored or repaired
    normative content; and no materialization for a non-accepting decision
  - Preflight crash before replacement and after replacement but before
    directory fsync; pass-before-fsync rejection; malformed temporary cleanup;
    prior-attestation preservation on failure; and stale prior evidence never
    satisfying the current preflight
  - Every closed preflight diagnostic/result/phase combination, malformed,
    mismatched, absent, and symlinked change roots before runtime discovery
  - Fresh `boundary-runtime-attestation-v3` embedded in the
    `boundary-behavior-implementation-v3`
    `behavior-implementation-manifest.json`; missing, stale, substituted, and
    tampered nested attestation invalidating the manifest reference, input-set
    identity, immutable run, pointer, and report selector without
    validation-time substitution
  - Exact historical-v1 registry path, regular-file kind, and raw-byte
    identity producing only `registered-opaque-history`; moved, altered,
    additional, ambiguous, caller-supplied, or structurally parsed v1 records
    produce `unsupported-historical-evidence`; no v1 record satisfies a
    current preflight, manifest, run, pointer, validation, report, capability,
    or activation role
  - Every v2-labeled record classified as unsupported historical evidence,
    with no structural parsing, current selection, field injection, or silent
    upgrade to v3
  - Later commits with unchanged referenced bytes versus changed referenced bytes
  - Resource-map, raw-byte-copy, trigger, stop, claim, handoff, complete review-bundle, and isolation tests
  - Example-only spec/test-spec rejection and valid compact simple-change cases
  - Exact candidate and produced invariant projections for model version,
    scope, requirement IDs, all twelve core-dimension IDs, and proof-map
    governing requirement IDs; missing, additional, duplicate, unknown,
    malformed, and unequal members emit
    `boundary-oracle-mismatch`
  - Pairwise and combined alternatives for stage-owned stable IDs,
    extension presence and decomposition, applicability choices,
    non-applicability rationale prose, boundary rows, examples, selected
    interactions, automation levels, proof grouping, and test-case IDs; every
    R28s-R28w-valid alternative reaches formal review instead of failing
    candidate comparison
  - Candidate files absent from child-readable roots and every lifecycle
    request; exact scenario request present in both formal review invocations;
    `check-environment` cannot emit `boundary-oracle-mismatch`
- Implementation steps:
  - First correct the pure immutable projection and tests in
    `boundary_proof_model.py`: add the exact eleven-field runtime row, selection
    and content identities, complete feature partition, effective-tool and
    handler-conformance schemas, common/state-specific proof rules, v3
    preflight/attestation/implementation-manifest schemas, closed file-change
    cause/phase/precedence, exact opaque-v1 registry, and unsupported-v2
    treatment. Unknown fields, values, identities, policies, causes, phases,
    and tuples fail closed before consistency checks.
    In this same first slice, require exact collection-to-classification
    equality, reject all three pairwise count-preserving category swaps before
    `thread/start`, and prove
    `required-disabled-feature-enabled → file-change-control-mismatch /
    pre-turn-start` while rejecting the historical `pre-thread-start` pair.
  - Implement only the minimal evidence-only `check-environment` preflight as
    the first runtime-executing M2 correction slice.
  - Require the exact change ID, select only its existing non-symlink change
    root, and accept Codex only when SemVer precedence is at least 0.138.0.
  - Resolve and identity-bind one Codex launcher and runtime package, reject
    versions before 0.138.0, and capture their raw-byte and filesystem
    identities before and after schema generation, each sandbox probe,
    app-server negotiation, and the accepted lifecycle invocation. Any
    removal, replacement, or mutation stops the run.
  - Generate the experimental app-server schema with that same identified
    runtime and bind every generated JSON file through a path-sorted
    canonical-JSON schema bundle before starting the server. Object-key order
    is non-semantic; every member and array position remains identity-bound.
    Require the exact approved Codex 0.145.0 launcher, runtime-package, schema,
    protocol-classification, and feature-classification identities before
    `thread/start`; select exactly one immutable projection and require exactly
    96 classified feature rows.
  - Build a fresh mode-restricted `CODEX_HOME` with exact profile
    `boundary-proof-stage-readonly-v1`: root denied, only minimal runtime paths
    and manifested scenario roots readable, no child writable root, and
    child-command network disabled. Do not combine the profile with legacy
    `sandbox_mode`.
  - Initialize app-server over stdio with `experimentalApi: true`. Before
    `turn/start`, require exact non-null `thread/start` metadata, fully
    paginate `experimentalFeature/list`, and require exact closed results from
    `config/read`, `configRequirements/read`, `app/list`, `plugin/list`,
    `mcpServerStatus/list`, and `skills/list`.
  - Normalize the exact generated-config origin and recognized temporary roots
    in the complete `config/read` projection; require every origin row to name
    the sole generated user config and share one format-valid runtime-owned
    version before replacing it with the stable
    `runtime-generated-config-origin` logical value.
  - Require exactly the five manifest-bound lifecycle skills enabled and the
    exact six generated-config-bound runtime system skills, including
    `review-agent`, disabled. Force
    reload; require the exact workspace row, empty errors, exact scopes, and
    unique raw and normalized paths.
  - Apply one exhaustive version/schema-bound exactly-once feature-row
    classification: permitted built-in tool, permitted non-tool runtime
    behavior, or must-be-disabled tool-bearing behavior. Reject missing,
    duplicate, unknown, or unclassified feature mappings and any enabled
    must-be-disabled behavior.
  - Independently apply one exhaustive version/schema-bound exactly-once
    protocol-item classification: permitted side effect, non-side-effect
    protocol traffic, or prohibited capability event. Treat
    `permitted-side-effect` only as a protocol classification, never as
    mutation authority. Reject missing, duplicate, unknown, or unclassified
    item mappings.
  - Keep `shell_tool`, `unified_exec`, and `shell_snapshot` read-only under the
    named profile. Configure the exact parent-owned production deny-only
    dispatcher before every governed thread. In preflight and again in
    generation, run every closed conformance case against the same dispatch
    and response-validation functions, then validate the complete policy and
    result through `boundary_proof_model` before selecting or invoking either
    capability branch. Missing, failed, malformed, stale, reordered,
    incomplete, or identity-inconsistent conformance emits only the bounded
    failure result and stops before any live probe, non-exposure acceptance,
    canary, governed lifecycle turn, or successful attestation.
  - Build both thread and turn requests from closed builders that bind one
    exact isolated workspace root. Record the exact empty 0.145.0
    thread-start root response, then classify every observed request and
    notification. Reject unknown/prohibited traffic; accept remote-control
    status only when disabled with no environment identity.
  - Forward only the closed upper/lowercase proxy-name set to the parent
    app-server process. Keep the generated child shell environment
    inherit-none and prove no proxy or unrelated parent variable crosses it.
  - Run positive and negative probes with the same executable, generated and
    managed configuration, and named profile through
    `codex sandbox --include-managed-config`. Require manifested workspace
    read; deny direct create, overwrite, remove, and mode change; repeat those
    four attempts from a detached descendant and require bounded exit/reap;
    and deny unmanifested source, private-auth path, and network access.
  - For `exposed-live-probe-required`, run the separate fresh app-server probe
    and require the exact correlated decline trace, unchanged workspace, and
    complete stop/reap. For `not-exposed-projection`, do not prompt for the
    absent operation; require exact runtime bytes, all required-disabled rows
    disabled, the complete effective-tool projection, and reject any observed
    file-change request or item as drift.
  - Route runtime observations, selected policy objects, and bounded
    conformance results through pure model validation before assembling either
    v3 attestation. Successful attestations contain only their closed fields;
    validated diagnostic decisions route to a separate bounded failure
    response/evidence path.
  - Inject a transient parent canary and require exact child environment names
    plus canary absence from environment values, argv, stdin, readable paths,
    and process metadata. Persist only typed non-secret decisions.
  - Execute the separate noncanonical `materialization-canary-v1` turn through
    `workflow` and `spec` under the same deny-only handler and a canary
    workspace-integrity baseline. Require an unchanged post-turn observation,
    one complete canary envelope, parent-only exact-byte materialization, and
    complete reread equality; discard the workspace and semantic bytes and
    retain only the bounded pass result.
  - Publish the successful preflight attestation only at
    `evidence/runtime-preflight-attestation.json`: sibling temporary write,
    file flush/fsync, same-filesystem atomic replace, evidence-directory
    fsync, then pass emission. Reconcile interrupted publication without
    promoting stale prior or temporary evidence.
  - On failed or interrupted preflight, preserve installed prior evidence as
    historical bytes but never treat it as current feasibility authority.
    Remove only malformed or identity-mismatched sibling temporary files and
    repeat replacement/fsync after an after-replace/before-directory-fsync
    interruption.
  - Before any other harness mutation or any participating-skill mutation, run
    that preflight and record only bounded non-secret results in
    `validation-m2.md`. On `environment-unavailable`, stop M2 and route to
    architecture without a weaker fallback.
  - Create and validate `evidence/boundary-proof-baseline.json` from the harness-derived current HEAD before the first participating-skill edit. If an immutable baseline already exists with a different value, stop.
  - Freeze the two-module AST import policy and exact manifest/input-set schemas.
  - Assemble the five skill packages, applicable instructions, contracts, and
    authoritative scenario into a fresh child-readable workspace. Bind
    candidate identities in the input set but retain their bytes in a separate
    parent-only comparison root.
  - Launch the identified runtime through the preflight-proven read-only
    sandbox and private runtime home; independently repeat command and
    capability-state-appropriate file-change proof, then derive a fresh
    `boundary-runtime-attestation-v3` for the
    exact eleven-row runtime inventory—five enabled manifested lifecycle rows and
    six generated-config-bound disabled system rows—while keeping the
    five-package resource set as a distinct input; embed the attestation in
    a fresh `boundary-behavior-implementation-v3`
    `behavior-implementation-manifest.json`, and bind that manifest reference
    transitively through the input-set identity, immutable run, pointer, and
    report selector. The preflight artifact is feasibility evidence only and
    is not substituted for this fresh generation record.
  - Recognize the exact tracked v1 manifest only through the closed historical
    registry before current generation. Do not parse, normalize, inject,
    upgrade, or select it. Fresh generation replaces current authority with a
    newly derived v3 manifest; every nonregistered v1 input and every
    v2-labeled input fails closed.
  - Before the canary and every lifecycle turn, open and retain the isolated
    workspace root descriptor and capture the complete bounded no-follow
    baseline. Child tools remain read-only. After terminal completion, or only
    after the exact timed-out child is confirmed stopped and reaped, run the
    complete bounded post-turn scan before considering output or
    materialization.
  - Route any complete or overflowing mutation observation to
    `stage-workspace-mutated` and any invalid/uncertain inspection to
    `stage-workspace-inspection-failed`; discard the workspace and stop before
    materialization, publication, or retry. Under uncertain liveness, perform
    no output or workspace inspection.
  - Collect the complete bounded agent-message candidate set, validate raw and
    canonical byte limits, the parent-selected policy, exact stage occurrence,
    artifact-set variant, paths, roles, content state, and UTF-8 without
    interpreting semantic content. Only one complete candidate plus a
    complete unchanged workspace may reach the parent materializer.
  - Materialize accepted stage-authored bytes relative to the retained root
    descriptor, reread the complete leaf set, record value-free exact-byte
    equality, run the closed structural lifecycle validators, and snapshot the
    complete stage output before advancing. Project candidate and produced
    feature/test-spec records independently through the pure invariant
    evaluator. Compare only the R54 closed invariant fields; route deterministic
    structure or projection failure to `boundary-oracle-mismatch`. Remove all
    substantive harness renderers and keep candidate oracles parent-only and
    comparison-only.
  - Build and validate the sibling temporary run; move it to the deterministic
    non-authoritative staging root and fsync; exclusively write and fsync the
    prepared receipt; install and fsync the immutable run; validate it;
    replace/fsync the pointer; reconcile; remove the receipt and fsync.
  - Implement validation-only reuse that never invokes a lifecycle skill and never substitutes validation-time environment data.
  - Exercise the full pipeline with controlled fixture packages without writing canonical evidence.
  - Write and map the shared boundary reference in the five participating packages, keeping stage-specific triggers, claims, stops, and handoffs in each `SKILL.md`.
  - Generate the real `spec -> spec-review -> test-spec -> test-spec-review`
    run through one public `workflow` orchestration. Each stage skill returns
    one complete policy-bound artifact envelope; the parent materializes and
    snapshots it before advancing; no harness renderer supplies, repairs, or
    completes normative artifact content. Include the exact scenario request
    in both formal review invocations so independent review, rather than a
    hidden candidate decomposition, owns semantic-fidelity judgment.
  - Reconcile a timed-out stage before retry using the exact transport matrix:
    complete valid output plus unchanged workspace reconciles without
    reinvocation; confirmed stop, zero candidates, unchanged workspace, and no
    non-output diagnostic permit one fresh-runtime retry; a second absence,
    partial/extra/contradictory evidence, mutation, inspection uncertainty,
    protocol/security failure, or uncertain liveness stops or pauses exactly
    as specified.
- Validation commands:
  - `python scripts/boundary_proof_behavior.py check-environment --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --json`
  - `python scripts/boundary_proof_behavior.py freeze-baseline --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`
  - `tmpdir="$(mktemp -d)" && python scripts/boundary_proof_behavior.py exercise-fixture --fixture tests/fixtures/boundary-proof/behavior/happy-path.json --output-root "$tmpdir" && python scripts/boundary_proof_behavior.py validate-fixture --root "$tmpdir"`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py --help`
  - `python -m py_compile scripts/boundary_proof_behavior.py scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py`
  - `python scripts/boundary_proof_behavior.py generate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --scenario tests/fixtures/boundary-proof/simple-change/scenario.json`
  - `python scripts/boundary_proof_behavior.py validate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`
- Promotion evidence:
  - accepted runtime-attestation receipt binding launcher and runtime-package
    raw-byte/filesystem identities across every execution boundary, CLI,
    model, provider, generated-schema bundle, effective permission profile,
    runtime roots, instruction sources, effective configuration/inventories,
    exact feature/item classification, sandbox probes, and
    credential-isolation result without secret values or private paths
  - exact pinned Codex 0.145.0 schema and protocol-classification identities,
    exact launcher and package bytes, eleven-field projection identity, 96
    feature rows partitioned into three permitted tools, four permitted
    non-tool behaviors, and 89 required-disabled tool-bearing features, five
    enabled user plus six disabled system skill rows, exact
    thread/turn root requests, classified observed events, and closed
    parent-proxy/child-environment evidence
  - durable current `runtime-preflight-attestation.json` whose reference
    matches the `boundary-runtime-preflight-v3` pass receipt, plus a fresh
    nested `boundary-runtime-attestation-v3` bound by the current behavior
    implementation manifest and immutable run
  - current `boundary-behavior-implementation-v3`
    `behavior-implementation-manifest.json`, including exact transport,
    lifecycle artifact, workspace-integrity, canary, runtime projection,
    effective-tool, shared file-change policy, and fresh handler-conformance
    identities
  - direct and descendant command-write denial, common production-dispatch
    conformance, capability-state-specific file-change proof, unchanged canary
    workspace, and parent-only materialization pass evidence
  - complete transport-attempt rows with candidate, workspace-integrity,
    materialization, and content-validation observations for every lifecycle
    event; no raw failed candidate or child-authored path retained
  - direct contrast evidence that R28s-R28w-valid alternative decompositions
    reach formal review, invariant mutations fail with
    `boundary-oracle-mismatch`, candidate bytes never reach a child, and
    preflight never emits that generation-only diagnostic
  - exact registered v1 path/raw-byte identity recognized only as opaque
    history and absent from every current authority chain; all v2 evidence
    rejected as unsupported history
  - immutable `boundary-proof-baseline.json`
  - controlled test-owned transport-failure fixtures below
    `tests/fixtures/boundary-proof/transport/`, all schema-valid and
    `canonical_evidence_eligible: false`
  - current `simple-change/current.json` pointing to a fully validated immutable run
  - `prepared.json` absent after successful reconciliation
  - focused and skill validation pass evidence
  - clean M2 code review before M3 starts
- Failure stop:
  - Stop on unavailable enforcement, unstable launcher or runtime-package
    identity, incomplete pagination, schema/protocol drift, missing, duplicate,
    unknown, or unclassified feature-row or protocol-item mapping, enabled or observed
    prohibited capability, config/profile mismatch, credential-canary
    exposure, baseline conflict, unmanifested input, invalid run, unresolved
    receipt, stale pointer, or any failed validation; do not mutate
    participating skills after a failed preflight or baseline step.
  - Stop on projection no-match/multiple-match/identity drift, a pinned
    launcher/package/schema/protocol/feature-classification mismatch, any
    feature count other than 96, enabled or missing `review-agent`, missing/additional/
    substituted/reordered request roots, non-disabled or bound remote-control
    status, unknown/prohibited observed traffic, an unlisted parent
    environment variable, or any proxy leakage into a spawned command.
  - Stop on any unknown or mismatched preflight diagnostic/phase, invalid
    change root, pass emitted before file and directory durability, unresolved
    preflight temporary state, substituted generation attestation, or attempt
    to replace recorded attestation with validation-time runtime evidence.
  - Stop on any writable child root, successful or ambiguous direct/descendant
    mutation, incomplete descendant reap, missing/failed/widened handler
    conformance, invalid exposed live trace, any file-change event under a
    non-exposed projection, child workspace mutation, incomplete or unstable
    integrity inspection, unvalidated attestation input, diagnostic content in
    a successful attestation, or canary materialization before a complete
    unchanged observation.
  - Stop on unknown or inconsistent transport tuple, candidate overflow,
    malformed/partial/extra/contradictory output, materialization/content
    mismatch, unsafe retry, registered-v1 use as current authority, unknown v1
    or any v2 evidence, or any attempt to synthesize stage-owned normative
    bytes in the harness.
  - Stop on malformed or unequal invariant projection with
    `boundary-oracle-mismatch`; fail review or enter only the governed
    correction branch for semantic nonapproval. Do not relabel either case as
    `unexpected-prohibited-event`.
- Expected observable result: The upstream skills require complete boundary/proof maps and one input-bound immutable behavior run proves the real upstream workflow with zero false blocking and no new universal artifact.
- Commit message: `M2: implement and prove hermetic upstream behavior`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Nondeterministic runtime output or crash recovery could make tests flaky or repeat work.
  - Sandbox attestation could be accidentally treated as child self-report.
  - Descriptor scanning or a detached child could race parent materialization
    if the read-only profile, root retention, or stop/reap proof is weakened.
  - Historical v1 evidence could be accidentally parsed or rebound as current
    authority, or unsupported v2 data could be silently upgraded during the
    v3 migration.
  - Shared reference use could hide stage-specific stop or claim boundaries.
  - A broad candidate comparison could silently restore one hidden golden
    decomposition, while an under-specified invariant comparison could miss
    the explicit scenario contract.
- Rollback/recovery:
  - Acquire the publisher lock before rollback. Reconcile any prepared receipt
    against staged and installed identities; if reconciliation cannot prove one
    complete state, fail closed without changing current authority.
  - Restore the current pointer to a previously validated immutable state, or
    remove it when no validated current run exists. Restore the exact
    registered opaque-v1 manifest path and bytes only when reverting to that
    historical baseline; otherwise leave no current behavior manifest.
  - Revert the M2 model, harness, validator, fixtures, shared template, and five
    package/resource edits as one compatibility unit. Remove the current v3
    preflight attestation when its bound implementation is reverted.
  - Retain installed v3 immutable runs only as non-current history, remove no
    audit evidence needed for recovery, and ensure no current pointer,
    implementation manifest, selector, or report references those runs.
  - Revalidate registered history, prepared/staged/installed publication state,
    current-pointer and manifest coherence, skill/resource parity, and absence
    of dangling v3 authority before declaring rollback complete. Retain the M1
    deterministic engine.

### M3. Downstream skill projection and preservation

- Milestone state: planned
- Goal: Carry the boundary contract through implementation, review, verification, and workflow routing, then compute downstream preservation from the frozen pre-M2 baseline without rerunning upstream skills.
- Requirements: R28f-R28j, R28y; R56f-R56i, R56l
- Files/components likely touched:
  - `skills/implement/SKILL.md`
  - `skills/implement/references/boundary-proof-model.md`
  - `skills/code-review/SKILL.md`
  - `skills/code-review/references/boundary-proof-model.md`
  - `skills/verify/SKILL.md`
  - `skills/verify/references/boundary-proof-model.md`
  - `skills/workflow/SKILL.md`
  - `skills/workflow/references/boundary-proof-model.md`
  - `tests/fixtures/skills/boundary-proof/`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/manifest.json`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/<run-id>/before/`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/<run-id>/after/`
- Dependencies:
  - M1-M2 closed
  - frozen `boundary-proof-baseline.json` and current M2 immutable run validate
- Tests to add/update:
  - Proof-before-change, sibling-remediation, public-path composition, stale-evidence, and pause behavior
  - Behavior, claim-boundary, review-recording, isolation, and handoff preservation for all eight skills
  - Missing, duplicate, stale, mismatched, and cross-skill preservation pair keys
  - Historical snapshot origin, current materialization identity, and no-direct-historical-reference contrasts
- Implementation steps:
  - Add mapped copies and stage-local proof, sibling analysis, independence, verification, and pause rules to the remaining skill surfaces.
  - Materialize before snapshots from the immutable baseline commit and current after artifacts under the exact preservation run root.
  - Generate the exact `preservation/manifest.json` and all 40 `<skill>:<category>` pairs.
  - Evaluate preservation from recorded before/after evidence only; do not invoke the upstream lifecycle workflow.
  - Validate origin commits, current snapshot identities, pair completeness, category results, and typed dependencies.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/boundary_proof_behavior.py generate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`
  - `python scripts/boundary_proof_behavior.py validate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`
- Promotion evidence:
  - current exact preservation manifest
  - complete immutable before and current after snapshot roots
  - 40 validated pair results for eight skills and five categories
  - no upstream behavior reinvocation
  - clean M3 code review before M4 starts
- Failure stop:
  - Stop on missing baseline, stale M2 pointer, origin mismatch, incomplete pair set, direct historical reference, behavior regression, or failed validation.
- Expected observable result: The full eight-skill chain preserves behavior and stops on missing, stale, partial, or example-only boundary evidence.
- Commit message: `M3: preserve boundary behavior across delivery skills`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Workflow guidance could claim authority or duplicate reviewer judgment.
  - Historical materialization could cite stale Git bytes instead of current evidence.
- Rollback/recovery:
  - Revert M3 skill projections and current preservation evidence together; retain M1-M2 without claiming the complete baseline.

### M4. Selection, adapter parity, capability baseline, and activation proof

- Milestone state: planned
- Goal: Make the complete boundary capability selectable, portable, measurable, and release-safe without activating or publishing it.
- Requirements: R28l-R28o, R28z; R56n, R56q
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `scripts/adapter_distribution.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/validate-release.py`
  - `scripts/test-release-transaction.py`
  - `dist/adapters/manifest.yaml`
  - `scripts/test-boundary-proof.py`
  - `tests/fixtures/boundary-proof/release/valid-activation/release-notes.md`
  - `tests/fixtures/boundary-proof/release/invalid-partial-activation/release-notes.md`
  - `tests/fixtures/boundary-proof/release/valid-rollback/release-notes.md`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/canonical.json`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/generated.json`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/packed.json`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/installed.json`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`
- Dependencies:
  - M1-M3 closed with clean code reviews
  - current M2 immutable run and M3 preservation manifest validate
- Tests to add/update:
  - Exact routing for the six boundary check IDs
  - Canonical/generated/packed/installed raw-byte parity
  - Report provenance, required-order aggregation, hash mismatch, partial activation, and rollback
  - No-new-universal-artifact and simple-fixture overhead assertions
- Implementation steps:
  - Register exact affected paths and checks in the selector.
  - Extend existing generation and resource-integrity proof for all supported adapters, using `dist/adapters/manifest.yaml` as the tracked support matrix.
  - Copy the validated canonical, generated, packed, and installed parity maps
    to the four exact durable `evidence/adapter-parity/*.json` paths before
    aggregating them.
  - Freshly execute the closed deterministic operation registry, consume the current immutable and preservation results, and serialize the report only through `validate-boundary-proof.py generate-report`.
  - Add valid activation, partial-activation rejection, and rollback release-note
    fixtures to the release transaction suite without writing an activation
    marker in this non-release change.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
  - `python scripts/test-release-transaction.py`
  - `python scripts/validate-release.py --version v0.3.6`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py generate-report --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --output docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`
  - `python scripts/validate-boundary-proof.py validate-report docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`
- Promotion evidence:
  - current canonical skill/resource manifest
  - exact durable `evidence/adapter-parity/canonical.json`,
    `generated.json`, `packed.json`, and `installed.json` manifest set
  - freshly generated passing capability report and raw-byte identity
  - exact selector routing proof for all six check IDs
  - passing activation, partial-activation, rollback, and current v0.3.6
    non-publishing release validation
  - clean M4 code review before final holistic review
- Failure stop:
  - Stop on any not-run/fail operation, stale dependency identity, parity mismatch, selector gap, asserted result, activation mismatch, or failed report validation; do not write release activation.
- Expected observable result: A passing, provenance-bound R28y report proves the eight-skill implementation checks across canonical and distributed surfaces. It does not by itself satisfy R28o, and release activation remains a later release action.
- Commit message: `M4: prove portable boundary capability baseline`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Adapter or report evidence could be stale, asserted, or coupled to a working-tree-only path.
- Rollback/recovery:
  - Remove selector and activation checks, regenerate adapters from the last known good canonical skills, and retain the report only as failed historical evidence.

## Validation plan

- `python scripts/test-boundary-proof.py`: focused typed-model, parser, fixture, and aggregate proof.
- `python scripts/boundary_proof_behavior.py check-environment --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --json`: live, evidence-only, non-secret runtime sandbox/profile and credential-isolation feasibility transaction.
- `python scripts/boundary_proof_behavior.py freeze-baseline --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: immutable pre-skill-mutation preservation baseline creation.
- `tmpdir="$(mktemp -d)" && python scripts/boundary_proof_behavior.py exercise-fixture --fixture tests/fixtures/boundary-proof/behavior/happy-path.json --output-root "$tmpdir" && python scripts/boundary_proof_behavior.py validate-fixture --root "$tmpdir"`: controlled noncanonical harness generation and validation.
- `python scripts/boundary_proof_behavior.py generate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --scenario tests/fixtures/boundary-proof/simple-change/scenario.json`: one canonical upstream behavior generation.
- `python scripts/boundary_proof_behavior.py validate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: deterministic current immutable-run validation without lifecycle reinvocation.
- `python scripts/boundary_proof_behavior.py generate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: preservation manifest and current snapshot/result generation.
- `python scripts/boundary_proof_behavior.py validate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: preservation-only validation without upstream reinvocation.
- `python scripts/validate-boundary-proof.py generate-report --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --output docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`: fresh closed-registry execution and sole-writer report generation.
- `python scripts/validate-boundary-proof.py validate-report docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`: deterministic current report validation.
- `python scripts/validate-skills.py`: canonical skill structure and mapped-resource contract.
- `python scripts/test-skill-validator.py`: public-skill regressions, including unknown values.
- `python scripts/build-skills.py --check`: generated local mirror parity.
- `python scripts/test-select-validation.py`: exact changed-path and check-ID routing.
- `python scripts/test-adapter-distribution.py`: generated, packed, and installed adapter parity.
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`: active generated adapter archive and resource parity.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: formal-review closeout.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml`: lifecycle metadata consistency.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md --path specs/rigorloop-workflow.md --path specs/skill-contract.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260725-boundary-first-proof-modeling.md --path docs/plans/2026-07-25-boundary-first-proof-modeling.md --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md`: exact touched lifecycle artifact state.
- `bash scripts/ci.sh --mode explicit --path scripts/boundary_proof_behavior.py --path scripts/boundary_proof_model.py --path scripts/validate-boundary-proof.py --path scripts/test-boundary-proof.py --path tests/fixtures/boundary-proof/incident-registry.json --path tests/fixtures/boundary-proof/simple-change.json --path templates/shared/boundary-proof-model.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/test-spec/SKILL.md --path skills/test-spec-review/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md`: selected integration proof after focused suites.
- `git diff --check`: whitespace and patch integrity.

## Risks and recovery

- Risk: Structural checks may be mistaken for semantic completeness.
  - Recovery: Keep semantic applicability and proof adequacy in formal reviews and reject any validator claim beyond exact structure and aggregation.
- Risk: Eight copied references may drift.
  - Recovery: Treat the shared template as copy source and require raw-byte equality across every canonical and distributed copy.
- Risk: The first slice could expand to all lifecycle skills.
  - Recovery: Fail review when a changed skill is outside the closed eight-skill list unless a separate approved slice exists.
- Risk: Capability reporting could become a new universal artifact.
  - Recovery: Keep the report path fixed to this initiative and reject generic scaffolding or schema registration.
- Risk: Release activation could be claimed from branch-local evidence.
  - Recovery: Validate activation only in tracked release notes against an actual release tag and report byte identity.
- Risk: The selected runtime cannot prove its effective sandbox or isolate credentials from child tools.
  - Recovery: Stop M2 with `environment-unavailable`, record bounded evidence
    in `validation-m2.md`, and route to architecture revision; do not proceed
    beyond the minimal preflight implementation or add an unreviewed weaker
    execution mode.
- Risk: Nondeterministic generation could be mistaken for deterministic validation.
  - Recovery: Keep generation and validation commands separate; validation never invokes lifecycle skills and a stale input identity requires a new explicit generation.
- Risk: A pinned model runtime may support structured responses without
  exposing a stage-agent file-write tool.
  - Recovery: Keep semantic authorship in the stage-owning skill's closed
    response envelope, permit the transport adapter only byte-for-byte
    materialization after complete validation, and prove that path with a
    noncanonical preflight canary before accepting lifecycle output.

## Dependencies

- Plan-review approval before test-spec authoring.
- Matching test-spec amendments and clean test-spec review before implementation.
- M1 deterministic correction before M2.
- In M2, implement only the minimal feasibility probe first; require its pass
  under the exact reviewed runtime projection before any other harness or
  participating-skill mutation.
- M2 harness and recovery proof before any canonical published-skill behavior generation.
- M3 before M4 so downstream skills consume a stable upstream record contract and current immutable run.
- M1-M3 before M4 computes capability outcomes.
- M4 writes the R28y report from implementation evidence; its code review then closes the implementation milestone without recursively rewriting the report to cite its own review.
- R28o remains unsatisfied until all milestone reviews and the final holistic code review are clean, review resolution is closed, explain-change is current, and final verification passes.
- Separate implementation authorization before M1.
- Separate verification authorization only after implementation closeout and final review evidence exist.

## Progress

- 2026-07-27: Focused R28y spec revision separates
  `changes-requested` from correction authority. It derives the closed
  `automatic-eligible`, `owner-decision-required`, or `not-applicable`
  disposition from complete finding records; only all-eligible findings may
  reach attempt 2. Owner-decision findings stop before mutation and require a
  fresh run with clarified authoritative input. The draft amendment is ready
  for focused spec review.

- 2026-07-27: Code-review M2 R9 opened `BFP-CR-M2-15`. The canonical
  scenario expects zero correction, but the current run contains `spec#2` and
  still passes because expectation fields are shape-validated but never
  compared with the derived trace. This implementation finding remains queued
  behind the focused `BFP-CR-M2-14` spec revision.

- 2026-07-27: Code-review M2 R8 confirmed the exact recovery-decision
  correction and opened spec-blocking `BFP-CR-M2-14`. Fresh behavior evidence
  recorded a `needs-decision` review finding but the harness treated
  `changes-requested` alone as correction authority and executed `spec#2`.
  M2 remains `resolution-needed`; the next stage is focused spec revision.

- 2026-07-27: Published the decision-bound recovery correction as immutable
  run `run-8f095d95abb863dbcbd642fe61abd65e` for input identity
  `sha256:381be42985b3bf9d52f6cd17b298ddc8adb1d67cc05c0b633b391b11f2716a18`.
  Its manifest binds publisher
  `publisher-fdedafd502f871013353ae28a7af7683`; canonical validation, 100
  focused tests, and the skill/build validators pass. M2 remains
  `resolution-needed` pending code-review R8.

- 2026-07-27: Code-review M2 R7 confirmed the R6 object-validity corrections
  and opened `BFP-CR-M2-13`. The remaining authority check proves only that
  evidence is current Markdown within the change root; it does not prove a
  review or owner decision authorizes the exact recovery subject and action.
  M2 remains `resolution-needed`.

- 2026-07-27: Published the object-complete R6 correction as immutable run
  `run-7c219a9daabd04402fa8345812f74b33` for input identity
  `sha256:a581eb599479874f3b043c51dbc9acc8ed3728cb023a017676378e29bc26d5e6`.
  Its manifest binds publisher
  `publisher-f21c802b33474485382e5e2088179ae3`; canonical validation passes with
  zero false blocks, zero universal artifacts, and one justified test-spec
  correction cycle. Ninety-seven focused tests and the skill/build validators
  pass. M2 remains `resolution-needed` pending code-review R7.

- 2026-07-27: Code-review M2 R6 classified the R5 correction as incomplete
  and opened `BFP-CR-M2-12`. Direct sibling probes showed completed-history
  run-ID subtraction hides a same-run staging orphan, shallow staged validation
  accepts an empty semantic run, unrelated repository bytes grant recovery,
  and a malformed fixed `runs` root survives discovery. M2 remains
  `resolution-needed`.

- 2026-07-27: Published boundary-complete recovery run
  `run-f6bb6b5f5d7912166d28fa37d012242f` for input identity
  `sha256:06124df85f7efe1b3a16304aa9e5eba5f173b4f049462da11325db9282a130bd`.
  The manifest binds publisher
  `publisher-fcde95cf6ab70c087aacc09a9330d998`; canonical validation passes with
  zero false blocks, zero universal artifacts, and zero correction cycles.
  Ninety-three focused tests cover the four R5 escapes, exact nested recovery
  schemas, lock contention, multiple-temp conflict, quarantine integrity, and
  every durable recovery resume point. M2 remains `resolution-needed` pending
  code-review R6.

- 2026-07-27: Code-review M2 R5 classified the broad publisher recovery
  remediation as incomplete and opened `BFP-CR-M2-11`. Direct probes showed
  malformed completed history is ignored, unknown working bytes and invalid
  staged bytes are accepted for recovery, and the required constrained
  malformed-temp cleanup route is absent. M2 remains `resolution-needed`.

- 2026-07-27: Published crash-resumable immutable canonical run
  `run-c9cf75951ba54219a13fe8f7c237c63d` for input identity
  `sha256:59c301f845c1d08b76c0505b379208537844a781058b13798df99f7cee72705e`.
  The manifest binds publisher
  `publisher-af486cb89d256f672f1c1e0aee59dad2`; non-regenerating validation
  reports zero false blocks, zero universal artifacts, and zero correction
  cycles. The 85-test focused suite now proves resumable manual recovery after
  every durable recovery boundary. M2 remains review-requested.

- 2026-07-27: Published lease-bound immutable canonical run
  `run-b59926e65e17a9debcf00ddc5b5ede03`.
  The exact manifest binds
  `publisher-bc63226fdb604e1a7fbc208835202a5d`; the transaction left no active
  lease, receipt, working, staging, or temporary-pointer object. Four
  interrupted live attempts were completed through authorized immutable
  recovery basis/state records with preserved quarantine. Non-regenerating
  validation passes, focused tests pass 84 cases, all 24 skills validate, and
  generated-skill drift checking passes. M2 is review-requested.

- 2026-07-27: Published immutable canonical run
  `run-95e4759a48cb46d183b8222e73ecc5ec`.
  Fresh upstream generation and non-regenerating validation report zero false
  blocking, zero universal artifacts, and zero correction cycles.
  Focused tests pass 77 cases, all 24 skills validate, 259 skill-validator
  tests pass, and generated-skill drift checking passes.
  M2 is review-requested.

- 2026-07-27: A fresh M2 run exercised the spec-correction branch and exposed
  the remaining R28y contradiction: extension IDs were declared stage-owned
  while also belonging to the exact fixture-candidate projection.
  Spec-review R55 and architecture-review R27 approved removing extension
  identity from that projection while preserving R28s-R28w structural
  validation and independent semantic review.
  This plan now requires an extension-presence contrast before M2 resumes.

- 2026-07-27: Implemented the R54 invariant-only oracle, parent-only candidate
  checks, scenario-bound formal reviews, dedicated oracle and review
  diagnostics, occurrence-bound materialization, and mutually exclusive
  artifact-set reconciliation. Published boundary references now state the
  executable ID, sentinel, uniqueness, ownership, interaction, coverage, and
  record-order constraints that were previously implicit. Seventy-three
  focused harness tests and the skill/build validators pass. Live stages have
  advanced through accepted spec, review, and test-spec envelopes, but no
  current immutable run is published because the latest clean attempts stopped
  at the fixed transport boundary. M2 remains `resolution-needed`.

- 2026-07-27: Test-spec-review R22 approved the direct parent-only candidate
  isolation proof with no findings, closed BFP-TSR21-1, and allowed M2
  implementation to resume.

- 2026-07-27: Resolved BFP-TSR21-1 in the proof map by requiring complete
  child-workspace, serialized request, attachment, artifact-context, and
  access-observation inspection. Candidate path, identity, and content
  injection must stop with `unmanifested-input` before materialization or
  publication.

- 2026-07-27: Test-spec-review R21 requested one focused correction:
  directly inspect every child-visible workspace, request, attachment,
  artifact-context, and access-observation surface and reject deliberate
  candidate exposure before output acceptance or publication.

- 2026-07-27: Synchronized the active R28y proof map and its exact input
  identities to spec-review R54, architecture-review R26, and plan-review R20.
  Independent test-spec review is the remaining authoring gate for M2.

- 2026-07-27: Plan-review R20 approved the focused R54/R26 M2 sequence with no
  material findings. Test-spec synchronization and independent review remain
  before implementation resumes.

- 2026-07-27: Synchronized M2 to R54/R26. The plan now orders pure invariant
  projection and contrast tests before generation, keeps candidate bytes
  parent-only, binds the scenario into both reviews, and distinguishes
  deterministic `boundary-oracle-mismatch` from semantic nonapproval.

- 2026-07-27: Architecture-review R26 approved the parent-only candidate,
  authoritative-scenario, pure invariant-evaluator, and dedicated diagnostic
  boundaries with no material findings and no new ADR requirement.

- 2026-07-27: Canonical architecture and the boundary-proof component view now
  keep comparison candidates outside child-readable roots, route the
  authoritative scenario into both reviews, and assign the closed invariant
  projection to a pure evaluator. No new ADR is required because this
  specializes the already accepted structural-validator/semantic-review
  boundary without changing the system or persistence design.

- 2026-07-27: Spec-review R54 approved the focused R28y invariant-oracle
  correction with no material findings. Affected architecture, plan, and
  proof-map surfaces remain to be synchronized before M2 resumes.

- 2026-07-27: Focused R28y spec and proof-map correction separates the
  scenario-owned behavior contract, stage-owned modeling choices, independent
  semantic review, and deterministic invariant projection. It adds the
  dedicated `boundary-oracle-mismatch` diagnostic and awaits spec review.

- 2026-07-27: Code-review M2 R3 blocked on BFP-CR-M2-9. Exact equality
  against every field of one hidden golden boundary/proof decomposition
  conflicts with independent stage ownership. The review routes a focused
  R28y correction before M2 implementation resumes.

- 2026-07-27: M2 now binds exact runtime implementation identities instead of
  trusting the Codex version alone, and the v3 evidence-only preflight passes.
  Deterministic validation passes 64 boundary-proof tests and 259 skill
  validator tests. Fresh generation remains fail-closed because R28y exact
  semantic-oracle equality appears to require one golden modeling
  decomposition from an independent stage author. The implementation is
  handed to code-review for upstream-contract classification; the prior
  immutable pointer remains unchanged.

- 2026-07-27: Test-spec-review R20 approved the exact
  R53/R25/R19-synchronized proof map with no findings. M2 implementation may
  resume with the pure-model tests before the live preflight.

- 2026-07-27: Synchronized the active proof map to the exact approved R53 spec,
  R25 architecture and successor ADR, and R19 plan identities. The remaining
  authoring gate is independent test-spec review.

- 2026-07-27: Plan-review R19 approved the explicit category and diagnostic
  contrasts with no findings. The next gate is exact test-spec identity
  synchronization and independent rereview.

- 2026-07-27: Plan-review R18 approved sequencing and recovery but required
  R53's exact category-equality, pairwise swap, and corrected diagnostic-phase
  contrasts in the first pure-model slice. The R19 candidate adds them before
  the live preflight.

- 2026-07-27: Architecture-review R25 approved the append-only successor and
  canonical architecture. Their statuses and lifecycle wording were normalized
  together; this plan now binds R53/R25 and routes to focused plan review.

- 2026-07-27: Architecture-review R24 confirmed the append-only correction and
  found only the successor ADR's missing mandatory follow-up. The R25
  candidate adds approval-gated status normalization and downstream identity
  synchronization without changing the decision.

- 2026-07-27: Architecture-review R23 accepted the technical 3/4/89 boundary
  but rejected rewriting the accepted binary-partition ADR in place. The R24
  candidate restores accepted history, adds a proposed append-only successor,
  and keeps the canonical architecture draft until rereview.

- 2026-07-27: Spec-review R53 approved the stable eleven-field 3/4/89
  projection contract with no findings. The next gate is focused architecture
  synchronization and rereview before plan and proof-map identities settle.

- 2026-07-27: Spec-review R52 found one remaining named R50 pending cell.
  The next candidate removes round-specific pending references from the proof
  map entirely while keeping the active plan and change metadata bound to the
  exact latest durable review.

- 2026-07-27: Spec-review R51 found only three round-specific proof-map
  references lagging the newly recorded R50 state. The next candidate binds
  the latest recorded R51 review and uses a stable clean-rereview requirement
  so recording the next result cannot recreate the defect.

- 2026-07-27: Spec-review R50 confirmed the category and diagnostic fixes but
  found stale R48/R22/R17 readiness prose and unsynchronized change metadata.
  The R51 candidate removes those claims and derives the durable counters and
  latest-review pointer from the recorded R50 evidence.

- 2026-07-27: Spec-review R49 confirmed the eleven-field 3/4/89 projection
  direction and requested exact category-equality binding, correction of the
  nonconforming discovery diagnostic phase, and removal of stale proof-map
  identities/readiness. The focused R50 candidate addresses all three before
  architecture and plan rereview.

- 2026-07-27: Resolved test-spec-review R18 by synchronizing companion command
  CMD-SBFP-8 with the exact change-root-bound primary preflight command,
  failure-before-mutation behavior, both evidence surfaces, and the
  evidence-only parent-observed side-effect boundary. The next gate is
  test-spec-review R19.

- 2026-07-27: Revised both active test specifications to the approved
  R48/R22/R17 contract. The proof map now binds exact runtime implementation
  identities, the ten-field projection, pure-model-validated common handler
  conformance, both capability branches, v3-only current evidence,
  opaque-v1/unsupported-v2 history, success/failure separation, and
  phase-aware rollback. The next gate is independent test-spec review.

- 2026-07-27: Resolved plan-review R16 by making pure-model validation of the
  complete production-dispatch conformance result the common pre-branch gate
  in both preflight and generation, adding zero-invocation contrast proof, and
  defining phase-aware rollback across receipts, pointer, manifests,
  attestations, code, fixtures, skills, and retained non-current history. The
  next gate is plan-review R17.

- 2026-07-27: Revised M2 planning to the approved R48/R22 contract: pure
  ten-field runtime registry and validators first; production dispatch and
  fresh common conformance second; capability-state-specific proof and v3
  attestation assembly third; then canary, generation, publication, and skill
  changes. The next gate is plan-review before test-spec revision.

- 2026-07-27: Architecture-review R22 approved the v3 capability-projected
  architecture with no findings. AR19 through AR21 are closed, the scoped
  successor ADR is accepted, and the next stage is plan revision.

- 2026-07-27: The R22 architecture candidate routes the selected canary policy
  through pure validation into both v3 success attestations, removes
  diagnostics from those closed records, and sends validated failure
  cause/phase/precedence decisions to a separate bounded failure surface.

- 2026-07-27: Architecture-review R21 found one final attestation-flow defect:
  canary policy bypassed pure validation and successful evidence edges carried
  failure diagnostics. The R22 correction separates those paths.

- 2026-07-27: The R21 architecture candidate synchronizes the assessment's
  common conformance gate and routes runtime observations, policy identity, and
  bounded conformance results through pure model validation before either v3
  attestation receives evidence.

- 2026-07-27: Architecture-review R20 found two residual synchronization
  defects: the assessment retained asymmetric conformance wording, and the
  diagram bypassed pure validation for runtime evidence. Both route to a
  narrow R21 candidate.

- 2026-07-27: The R20 architecture candidate resolves R19 by making fresh
  production-dispatch conformance a common gate before either capability
  branch, assigning registry/validation to `boundary_proof_model.py`, assigning
  runtime dispatch/execution to `boundary_proof_behavior.py`, and labeling
  every component relationship.

- 2026-07-27: Architecture-review R19 requested two focused corrections:
  make handler conformance common to both capability branches, and assign the
  new registry/dispatch/conformance components to exact modules with fully
  labeled C4 relationships. Plan revision remains blocked until R20.

- 2026-07-27: Synchronized the R48 architecture candidate across the canonical
  Runtime View, component diagram, architecture assessment, accepted
  predecessor observation, and proposed capability-projected file-change ADR.
  The candidate preserves the read-only child and parent-only materialization
  boundary while replacing only unconditional live probing and v2 evidence.

- 2026-07-27: Spec-review R48 approved the exact-runtime-bound v3 projection
  contract with no findings. R46 and R47 are closed; the required next stage
  is architecture synchronization before plan and test-spec updates.

- 2026-07-27: The R48 candidate resolves BFP-SR47-1 by adding exact launcher
  and runtime-package identities to the immutable projection and selection
  key, recomputing the ten-field projection identity, and rejecting changed
  runtime bytes even when declared version, schemas, protocol, and features
  remain equal.

- 2026-07-27: Spec-review R47 confirmed R46's migration and routing
  corrections but found the non-exposure projection was not yet bound to the
  exact launcher and runtime-package bytes that implement tool exposure.
  BFP-SR47-1 routes to a focused projection-identity revision before R48.

- 2026-07-27: The R47 spec candidate resolves R46 with one uniformly current
  v3 contract, an exact content-identified Codex 0.145.0 projection, complete
  invocation-owned effective-tool and decline-handler evidence, and closed
  file-change cause/phase/precedence routing. The next gate is independent
  spec review; architecture and implementation remain blocked until approval.

- 2026-07-27: Spec-review R46 accepted the capability-projection direction
  and requested four closure corrections: complete v3 migration, immutable
  projection content identity, invocation-owned non-exposure evidence, and
  deterministic file-change diagnostic routing. Architecture remains blocked
  until R47 approves the corrected contract.

- 2026-07-27: Reopened R28y as the R46 candidate after the live preflight
  proved its file-change event unreachable. The candidate replaces
  repository-wide single-version gating with immutable capability projections,
  distinguishes live-probe-required from projection-proven non-exposure,
  advances current evidence to v3, and fails closed on projection drift. The
  next gate is independent spec review before architecture alignment.

- 2026-07-26: The R45 read-only preflight now passes direct and detached
  descendant create, overwrite, remove, and mode-change denial, but fails
  closed at the required real app-server file-change probe. Codex 0.145.0
  exposes no file-change operation under the approved configuration, so the
  model returns the terminal marker without an approval request. Enabling the
  candidate apply-patch feature flags still leaves those features disabled in
  the runtime inventory, including under a disposable workspace-write probe
  profile. M2 is blocked and routes to architecture; no participating skill
  was mutated and no v2 pass attestation was published.

- 2026-07-26: Test-spec-review R17 approved the complete M2 proof map with no
  findings. BFP-TSR15-1 and BFP-TSR16-1 are closed; the Current Handoff
  Summary owns the next stage against the three accepted M2 code-review
  findings.

- 2026-07-26: The R17 test-spec candidate resolves BFP-TSR16-1 by proving
  working-run object validation before staging rename, invalid working-run
  failure before every publication mutation, and the
  post-working-validation/pre-rename crash boundary while retaining the staged
  validation proof added for R16.

- 2026-07-26: Test-spec-review R16 confirmed BFP-TSR15-1 substantively
  resolved and found BFP-TSR16-1: T51 must separately prove working-run
  validation before staging rename. M2 remains paused for focused test-spec
  revision and rereview.

- 2026-07-26: Test-spec-review R15 approved the broader R45 proof map and
  found one T51 ordering omission. The R16 candidate now proves complete
  staged-run/current-input validation before receipt creation, rejects invalid
  or stale staging without receipt/install/pointer mutation, and covers the
  post-validation/pre-receipt crash boundary.

- 2026-07-26: Revised the active workflow test spec for R45/R18/R15. The
  candidate adds v2/opaque-v1 compatibility, direct and descendant command
  denial, cause-specific app-server file-change decline, bounded root-anchored
  integrity inspection, exhaustive transport routing, and parent-only
  materialization proof. Independent test-spec review is next.

- 2026-07-26: Plan-review R15 approved the R45/R18 M2 correction sequence
  with no findings. The stale R14 test proof map must now be revised and
  independently approved before implementation resumes.

- 2026-07-26: Architecture-review R18 approved the complete read-only
  stage-transport amendment and closed BFP-AR16-1, BFP-AR16-2, and
  BFP-AR17-1. The canonical architecture and transport ADR are accepted, the
  predecessor ADR clauses are narrowly superseded, and focused plan revision
  is next.

- 2026-07-26: Architecture-review R17 confirmed the Runtime View, component
  trace, evidence compatibility, and ADR lifecycle, but found one stale
  writable-root statement in the Building Block View. The R18 candidate
  replaces it with the approved parent-owned output-root contract: child
  access is read-only with no writable root, and parent materialization is
  permitted only after the unchanged-workspace gate.

- 2026-07-26: Spec-review R45 approved the read-only transport contract and
  closed all R41-R44 spec findings. The R17 architecture candidate rewrites
  the numbered runtime sequence, trust boundary, transport boundary, quality
  scenarios, risks, component view, architecture assessment, and proposed
  stage-envelope ADR around parent-only materialization, shared file-change
  denial, root-anchored workspace integrity, v2 current evidence, and exact
  opaque v1 history.

- 2026-07-26: Spec-review R44 approved the current v2 transport/security
  contract and found only that reused historical v1 labels could not select a
  deterministic parser. The R45 candidate removes structural v1 parsing and
  recognizes only the one actually persisted manifest by exact path,
  regular-file kind, and raw-byte identity as opaque read-only history;
  unknown v1 records fail closed and no v1 record can satisfy a current role.

- 2026-07-26: Spec-review R43 confirmed the typed baseline-failure surface but
  found that the probe-local decline did not govern accepted turns, the
  expanded attestation reused v1, and the fixed failure record declared an
  unreachable size boundary. The R44 candidate defines one deny-only
  authorization policy for probe, canary, stage, retry, and reconciliation
  contexts; advances current attestation and implementation-manifest evidence
  to v2 with explicit historical-v1 treatment; and relies on the reachable
  intrinsic 271-byte maximum of the closed failure schema.

- 2026-07-26: Spec-review R42 confirmed the R41 workspace-integrity
  corrections and retained two gaps: the app-server file-change path lacked an
  independent denial probe, and baseline inspection failures lacked a typed
  preflight and generation-start surface. The R43 candidate adds an
  identity-bound file-change denial policy and fresh app-server probe, binds
  its pass result into runtime attestation, and adds a bounded,
  privacy-preserving `workspace-baseline-failure-v1` record to both exact
  failure responses.

- 2026-07-26: Spec-review R41 required writer-quiescence proof, total
  race-resistant scan failures, and bounded privacy-safe evidence. The R42
  candidate removes child workspace-write authority, adds direct and detached
  descendant denial probes, binds lifecycle/canary integrity limits, and uses
  root-anchored no-follow descriptor inspection with closed mutation,
  inspection-failure, overflow, and baseline-failure routes.

- 2026-07-26: Architecture-review R16 found that child workspace writes could
  bypass adapter-exclusive materialization and that the canonical Runtime View
  remained on the pre-R40 protocol. The focused R41 spec candidate adds a
  complete pre-turn workspace baseline, bounded post-turn comparison, a
  replayable value-free integrity observation, and the closed
  `stage-workspace-mutated` fail-closed route before materialization.

- 2026-07-26: Spec-review R39 confirmed every prior transport finding and
  retained only the missing distinction between raw pre-parse message size and
  post-parse canonical envelope size. The R40 candidate binds both exact
  limits through lifecycle and canary policies with equality and one-byte-over
  behavior.

- 2026-07-26: Spec-review R38 confirmed the canary policy and requested exact
  lifecycle-policy serialization/binding, canonical malformed/oversized
  candidate rows, replayable post-materialization observations, and a terminal
  second-correction branch. The R39 candidate closes those four contracts.

- 2026-07-26: Spec-review R37 requested exhaustive review/correction artifact
  variants, bounded replayable candidate-set evidence, and a canary policy
  separate from lifecycle output policy. The R38 candidate adds all three,
  keeps the adapter semantics-free, and retains raw content only transiently
  for the sole complete candidate.

- 2026-07-26: Live M2 generation against the pinned app-server failed closed
  because each stage returned its completion message without creating the
  required workspace files. Direct isolated probes confirmed that the runtime
  supports schema-constrained agent messages but does not expose the assumed
  stage-agent workspace-write surface. The workflow routed upstream rather
  than restoring harness-owned normative renderers.
- 2026-07-26: The focused R37 spec candidate separates semantic authorship
  from physical materialization: the stage-owning skill returns one closed,
  size-bounded artifact envelope and the transport adapter validates then
  writes its UTF-8 bytes unchanged. The candidate also adds timeout retention,
  byte-equality proof, and a noncanonical preflight materialization canary.

- 2026-07-25: Plan created after spec-review R2 and architecture-review R2 approval.
- 2026-07-25: Plan-review R2 approved the corrected four-milestone sequence.
- 2026-07-25: Matching workflow and skill-contract test specs were amended with v1 proof maps, fixtures, commands, and milestone gates.
- 2026-07-26: M1 added the immutable typed model, deterministic validator CLI, frozen incident registry, compact simple-change fixture, and synthetic capability aggregation proof.
- 2026-07-26: M1 code-review R1 recorded seven findings; BFP-M1-CR4, BFP-M1-CR6, and BFP-M1-CR7 require owner decisions before correction.
- 2026-07-26: The user authorized the recommended contract-first resolution; the workflow and skill specs now define identity-bound evidence, boundary-state incident replay, and computed simple-change traces pending spec-review R3.
- 2026-07-26: Spec-review R3 requested exact incident rules, trace formulas, and operation-bound evidence receipts before M1 correction.
- 2026-07-26: The R4 candidate freezes incident derivation, operation-bound evidence receipts, a closed stage-event grammar, and deterministic simple-change metrics.
- 2026-07-26: Spec-review R4 retained the R3 findings and required fresh operation recomputation plus phase-appropriate workflow proof.
- 2026-07-26: The R5 candidate replaces caller-authored receipts with fresh closed-registry execution, makes incident triggers unique, and phases real skill behavior after M1's synthetic engine proof.
- 2026-07-26: Spec-review R5 resolved incident derivation and retained only snapshot/trace closure and operation-registry projection.
- 2026-07-26: The R6 candidate closes the operation-to-report registry, input/output provenance, preservation and adapter manifests, behavior-output capture, snapshot/event cardinality, structural/result consistency, and reproducible artifact-inventory formulas.
- 2026-07-26: Spec-review R6 retained BFP-SR3-2 and BFP-SR3-3 for oracle/input/output separation, complete workspace inventory, historical and typed-result identity, aggregate observation projection, marker-absence selection, and frozen fixture paths.
- 2026-07-26: The R7 candidate makes candidates oracle-only, closes stage input cardinality and terminal branches, inventories the behavior artifact tree with a closed classifier, materializes historical evidence, identity-binds typed results and dependencies, and losslessly projects aggregate observations.
- 2026-07-26: Spec-review R7 retained BFP-SR3-2 and BFP-SR3-3 for oracle-label independence, exact normalized assertions, complete formal-review output bundles, pre-run HEAD authority, canonical manifest paths, and normalized result identities.
- 2026-07-26: The R8 candidate makes scenario labels comparison-only, closes normalized oracle records, bundles complete formal review evidence, derives simple-run HEAD and pre-M2 preservation baselines separately, freezes support-manifest paths and schemas, and normalizes typed-result identities.
- 2026-07-26: Spec-review R8 retained only review-event evidence-union, portable immutable-run publication, and filesystem-versus-typed selector separation gaps.
- 2026-07-26: The R9 candidate defines authoring and review evidence sets separately, counts complete review bundles, publishes immutable runs through one atomically replaced pointer, and separates filesystem input references from typed-result dependencies.
- 2026-07-26: Spec-review R9 resolved BFP-SR3-2 and BFP-SR3-3 and opened BFP-SR9-1 because generation and validation still reran nondeterministic skill invocations and stale pointer reuse was not input-bound.
- 2026-07-26: The R10 candidate separates one-shot behavior generation from deterministic recorded-run validation, binds immutable evidence to an exact current input set, and reconciles prepared publication without repeating skills or accepting stale pointers.
- 2026-07-26: Spec-review R10 retained BFP-SR9-1 only for immutable prior-pointer history and complete behavior-harness/orchestration implementation identity.
- 2026-07-26: The R11 candidate stores the prior pointer as immutable inline history and binds every behavior-affecting workflow, harness, capture, serialization, evaluation, contract, and runtime input through one closed implementation manifest.
- 2026-07-26: Spec-review R11 retained BFP-SR9-1 because the manual component list omitted transitive workflow imports, governing instructions, and exact environment derivation.
- 2026-07-26: The R12 candidate replaces the manual component list with a validated transitive import/resource/instruction closure, runs against an allowlisted read view, and derives normalized non-secret execution-environment fields from authoritative runtime sources.
- 2026-07-26: Spec-review R12 retained BFP-SR9-1 because that transitive closure omitted participating resources and runtime instructions and could not deterministically model dynamic imports or the observable runtime boundary.
- 2026-07-26: The R13 candidate replaces the open-ended transitive closure with a standalone hermetic behavior harness, a closed two-module import policy, complete five-skill resource-map binding, applicable instruction discovery, and an observable runtime/model/tool invocation profile.
- 2026-07-26: Spec-review R13 approved the revised contract with no new findings and resolved BFP-SR9-1; architecture amendment is required before test-spec revision or implementation.
- 2026-07-26: The architecture R3 candidate assigns the standalone harness, five-skill package assembly, isolated child runtime, observable invocation attestation, transient access enforcement, and prepared-receipt immutable publication to explicit components and updates the ADR and C4 views.
- 2026-07-26: Architecture-review R3 requested the exact R28y publication order, trusted parent/runtime enforcement with opaque control-plane authentication, and durable ADR rationale for the hermetic design.
- 2026-07-26: The R4 candidate corrects publication to validated run installation, fsynced receipt, atomic pointer replacement, parent fsync, and receipt cleanup; assigns confinement to parent-attested runtime sandboxing; keeps credentials in a private runtime-only channel; and records rejected alternatives and operating costs.
- 2026-07-26: Architecture-review R4 approved the hermetic child-runtime boundary, exact publication recovery, ADR tradeoffs, and C4 views; plan revision must start with runtime feasibility proof.
- 2026-07-26: The plan R3 candidate replaces the stale four-milestone sequence with five reviewed boundaries: runtime feasibility and core correction, standalone harness and recovery, upstream behavior generation, downstream preservation, and portable capability aggregation.
- 2026-07-26: Plan-review R3 requested restoration of normative R28y M1-M4 ownership and exact production, validation, promotion, baseline, and recovery commands.
- 2026-07-26: The plan R4 candidate restores normative M1-M4 ownership, makes runtime feasibility and baseline capture the first M2 gates, and names exact controlled/canonical generation, validation, preservation, aggregation, promotion, and failure-stop commands and artifacts.
- 2026-07-26: Plan-review R4 confirmed phase ownership and retained BFP-PL4 for inconsistent M2 feasibility wording and BFP-PL5 for missing exact release/parity paths and commands.
- 2026-07-26: The plan R5 candidate makes the minimal preflight the first bounded
  M2 implementation slice and freezes M4 adapter, parity, release-fixture, and
  release-validation surfaces.
- 2026-07-26: Plan-review R5 resolved BFP-PL4 and BFP-PL5 and approved
  the M1-M4 execution plan for matching test-spec revision.
- 2026-07-26: The workflow and skill-contract test specs were revised against
  the approved R13 specification, R4 architecture, and R5 plan with hermetic
  input closure, runtime-boundary, immutable-publication, crash-recovery,
  preservation, parity, and release proof mapped to M1-M4.
- 2026-07-26: Architecture-review R6 resolved the R5 runtime-evidence findings
  and requested one final correction: bind a fully paginated experimental
  feature inventory to an exhaustive pre-turn built-in-tool classification.
- 2026-07-26: Architecture-review R7 confirmed that closure and requested one
  feasibility correction: distinguish complete protocol vocabulary from the
  effective capability set, while rejecting prohibited events at runtime.
- 2026-07-26: Architecture-review R8 approved the corrected permission-profile
  and app-server boundary with no material findings.
- 2026-07-26: The M2 plan projection now makes exact schema identity,
  app-server inventory closure, profile-equivalent sandbox probes, exhaustive
  feature/item classification, and child credential isolation mandatory
  pre-mutation gates.
- 2026-07-26: Plan-review R6 requested end-to-end runtime identity continuity,
  exact tool/item mapping, and unambiguous review/pagination wording; the R7
  candidate now closes all three gaps.
- 2026-07-26: Plan-review R7 requested separate closed vocabularies for
  pre-turn feature enablement and in-turn protocol events; the R8 candidate
  now proves both independently.
- 2026-07-26: Plan-review R8 approved the corrected M2 plan with no material
  findings and routed the initiative to matching test-spec revision.
- 2026-07-26: The test-spec R5 candidate maps runtime identity continuity,
  experimental protocol closure, independent feature/item classifications,
  equivalent sandbox probes, and credential isolation into explicit contrasts.
- 2026-07-26: Test-spec-review R5 requested exact schema/negotiation/pagination
  negatives and exposed a spec-shape gap; the focused R14 spec candidate now
  embeds bounded runtime attestation in the existing implementation manifest.
- 2026-07-26: Spec-review R14 required exact thread metadata, deterministic
  identity preimages, phase-correct failure receipts, and explicit transitive
  binding; the R15 candidate defines all four contracts.
- 2026-07-26: Spec-review R15 required complete provider/instruction equality,
  deterministic package and secret rules, evidence-bound preflight pass, and
  report-selector proof; the R16 candidate closes each residual gap.
- 2026-07-26: Spec-review R16 required exact version-floor semantics and a
  durable explicitly targeted preflight transaction; the R17 candidate adds
  SemVer closure, `--change-id`, fsync ordering, and crash recovery.
- 2026-07-26: Spec-review R17 found one stale duplicate preflight command; the
  R18 candidate synchronizes it with CMD-BFP-8 and the M2 command.
- 2026-07-26: Spec-review R18 approved the focused contract; the R9 plan
  candidate projects the SemVer floor and durable preflight evidence
  transaction before test-spec rereview.
- 2026-07-26: Plan-review R9 requested current source pointers and full
  preflight/generation transaction projection; the R10 candidate closes both.
- 2026-07-26: Plan-review R10 confirmed the transaction projection and found
  one stale rereview-round label; the R11 candidate corrects it.
- 2026-07-26: Plan-review R11 approved the current plan with no material
  findings and routed the amended proof map to test-spec review.
- 2026-07-26: Test-spec-review R6 requested exact preflight recovery and fresh
  generation-attestation contrast matrices; the R7 candidate adds both.
- 2026-07-26: Test-spec-review R7 confirmed the proof bodies and requested
  current governing identities and M2 ownership; the R8 candidate synchronizes
  them.
- 2026-07-26: Test-spec-review R8 approved the proof map and allowed M2
  implementation handoff.
- 2026-07-26: The live M2 preflight exposed that Codex 0.144.6 reports five
  disabled runtime-system skills alongside the five enabled manifested
  lifecycle skills. Spec-review R19 requested an exact request, roster, scope,
  error, and uniqueness contract; spec-review R20 approved the config-bound
  ten-row correction.
- 2026-07-26: Before canonical generation, the installed runtime advanced to
  Codex 0.145.0. The exact projection adds four feature rows and one
  runtime-system `review-agent` row. The M2 correction uses a version-keyed
  closed feature registry, explicitly disables every added tool-bearing
  feature and `review-agent`, and requires the resulting five-user/six-system
  eleven-row inventory. Because `thread/start` now reports an empty
  runtime-root list, the version-bound contract records that value while both
  thread and turn requests bind the isolated workspace and the parent sandbox
  probes remain authoritative.
- 2026-07-26: Focused runtime-contract review requested exact schema/protocol
  pinning, observed-event enforcement, direct thread/turn request proof, and
  refreshed governing identities. The correction pins both 0.145.0
  identities, rejects unknown/prohibited observed variants, tests both root
  requests and the closed parent proxy environment, and keeps the lifecycle
  gates open pending rereview.
- 2026-07-26: Architecture-review R9 approved the focused correction without
  changing components, persistence, deployment, or trust boundaries. The live
  preflight now passes and publishes a durable bounded attestation; plan and
  test-spec review synchronization remain before broader M2 implementation.
- 2026-07-26: Test-spec-review R3 retained one gap: aggregate hermetic-input
  coverage must become field-complete mutation proof before implementation.
- 2026-07-26: The R4 test-spec candidate now mutates every manifest collection,
  all nine invocation-profile fields, all five contract refs, instruction
  ordering/deduplication/symlink behavior, the exact baseline record, the exact
  input-set fields and members, and comparison-only scenario expectations.
- 2026-07-26: Test-spec-review R4 resolved BFP-TSR3-1 and approved the
  field-complete proof map for M1 implementation.
- 2026-07-26: M1 correction added direct negative regressions and deterministic
  fixes for BFP-M1-CR1 through BFP-M1-CR7; focused tests and lifecycle
  validation pass and the milestone is review-requested.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-25 | Use four implementation milestones ordered engine, upstream skills, downstream skills, distribution evidence. | This was the approved initial sequence before the R13 hermetic behavior contract. | One large milestone; skill edits before the proof engine; adapter work before canonical behavior settles. |
| 2026-07-25 | Keep release activation validation in the final baseline milestone but perform no activation or publication. | The spec requires activation semantics, while external release actions remain outside this change and automation authority. | Omitting activation tests; writing a premature activation marker. |
| 2026-07-26 | Use frozen dataclasses plus pure mapping validators and JSON fixture inputs for M1. | The executable projection remains dependency-free, immutable, deterministic, and separate from Markdown serialization or semantic review. | A second YAML registry; validator-owned semantic scoring; mutable global records. |
| 2026-07-26 | Revise to five milestones: feasibility/core, harness, upstream behavior, downstream preservation, and distribution baseline. | The accepted R13/R4 design adds a high-risk runtime boundary and recoverable publication flow that need an independent review before public skill mutation. | Hide the harness inside upstream skill work; build the full harness before proving runtime support; keep stale four-milestone mapping. |
| 2026-07-26 | Restore normative M1-M4 ownership and make runtime feasibility the first M2 promotion gate. | R28y explicitly assigns synthetic proof, upstream behavior, downstream preservation, and aggregation to M1-M4. | Renumber the approved phases; amend the spec only to preserve an unnecessary fifth phase. |
| 2026-07-26 | Keep one M2 milestone but order its correction as immutable projection/tests, read-only preflight, integrity-gated envelope transport, workflow-owned generation, then durable publication. | The approved R45/R18 contract resolves the three open M2 findings without changing normative milestone ownership; each internal slice has a fail-closed promotion gate before the next riskier slice. | Reopen milestone numbering; implement the live runtime before closed validators; retain child writes; allow the harness to render normative artifacts. |
| 2026-07-26 | Use staged validation, durable exclusive prepared receipt, immutable install, installed-run validation, atomic pointer replacement, and receipt cleanup as the only publication order. | This is the approved recovery transaction and closes the governing-artifact half of BFP-CR-M2-8. | Install before receipt; validate only after pointer publication; adopt orphan output. |
| 2026-07-27 | Select file-change proof through one exact-runtime-bound immutable projection and make pure-model-validated production-dispatch conformance common to both branches. | The approved R53/R25 contract proves enforcement without asking a model to invoke an operation the reviewed runtime does not expose, binds all 96 features to exact tool/non-tool/disabled categories, and validates conformance before branch selection. | Version-only gating; feature flags alone; event absence alone; unconditional live probing; binary feature partitions; branching before conformance validation; removing the deny-only handler. |
| 2026-07-27 | Exclude extension identity from the fixture-candidate oracle and prove structurally valid extension alternatives reach review. | R28y assigns extension modeling to the stage and reviewer; exact candidate equality made that authority contradictory and hidden. | Forbid all extensions in the scenario; inject candidate extension choices into child stages; let the evaluator judge extension semantics. |

## Surprises and discoveries

- The earlier writable sandbox probe proved only a neighboring command
  capability and left the stage-output boundary bypassable. R45/R18 replace
  that design with direct and descendant write denial, a separate
  cause-specific app-server file-change decline probe, read-only stage turns,
  and parent-only envelope materialization after workspace-integrity proof.

- The pinned Codex 0.145.0 package exposes the three approved command
  features but no file-change operation under the reviewed configuration.
  Exact runtime-byte projection plus fresh production-dispatch conformance
  replaces the unreachable live probe without weakening drift detection.

- The unified automation state adapter writes `run.pause_reason`, while the
  change-metadata schema currently accepts `run.stop_reason`. The run was
  normalized through the sole state writer. This pre-existing harness mismatch
  is outside the boundary-proof implementation scope and requires a focused
  workflow-automation bugfix before the next release.
- M1 aligned-surface audit: selector registration, public skills, shared
  references, adapters, release notes, and the canonical capability report are
  intentionally unaffected because M2-M4 own those surfaces.

## Validation notes

- `python scripts/boundary_proof_behavior.py validate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` passed for current run `run-f6bb6b5f5d7912166d28fa37d012242f`.
- `python scripts/test-boundary-proof.py` passed 93 tests including all eight named T51 publisher property rows, four direct R5 escape regressions, exact recovery-schema mutations, and resumable recovery after every durable recovery boundary.
- `python scripts/validate-skills.py` validated 24 skills.
- `python scripts/test-skill-validator.py` passed 259 tests.
- `python scripts/build-skills.py --check` passed.
- `python -m py_compile scripts/boundary_proof_behavior.py scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py` passed.
- `git diff --check` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-25-boundary-first-proof-modeling.md` passed after R1 corrections, with unrelated existing workflow-spec lifecycle-language warnings.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml` passed after R1 corrections.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` passed after R1 recording.
- `python scripts/test-boundary-proof.py` passed 12 tests covering closed values, exact fields, version parity, traceability, fixtures, aggregation, evidence, and sole-writer serialization.
- `python scripts/validate-boundary-proof.py --help` passed.
- `python -m py_compile scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py` passed.
- `python scripts/test-artifact-lifecycle-validator.py` passed 156 tests.

## Outcome and retrospective

- Pending implementation, milestone reviews, the R28y capability report, final holistic code review, closed review resolution, explain-change, and final verification.
- Progressive-disclosure proposal review remains paused until the complete R28o predicate passes; a passing report alone is insufficient.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not milestone completion or final closeout.
