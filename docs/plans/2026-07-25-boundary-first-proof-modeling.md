# Boundary-First Proof Modeling for Published Lifecycle Skills

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Change ID: 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills
- Start date: 2026-07-25
- Last updated: 2026-07-26
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
- Latest spec review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r38.md` (changes requested)
- Architecture: `docs/architecture/system/architecture.md` (approved by architecture-review R15)
- ADR: `docs/adr/ADR-20260725-boundary-first-proof-modeling.md` (accepted by architecture-review R15)
- Runtime-attestation ADR: `docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md`
- Architecture review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/architecture-review-r15.md`
- Plan review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/plan-review-r14.md`
- Test specs: `specs/rigorloop-workflow.test.md` R28-R28z and `specs/skill-contract.test.md` R56-R56q; current runtime-boundary proof map is approved by focused test-spec-review R14

## Context and orientation

The approved baseline outside the focused R28y amendment remains normative.
The focused R28y stage-transport text is under revision because live M2
generation proved that the pinned app-server returns schema-constrained stage
messages but does not expose the assumed stage-agent workspace-write surface.
Implementation is paused at that contract boundary pending spec-review and
the required downstream architecture, plan, and test-spec synchronization.
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
- Latest review evidence: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r38.md
- Review status: changes-requested; stage=spec-review; round=r38
- Remaining in-scope implementation milestones: M2, M3, M4
- Next stage: spec-review R39
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending — review-state=open; open-count=3; open-findings=BFP-CR-M2-1,BFP-CR-M2-7,BFP-CR-M2-8

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
    identities; exact 96-row feature projection; and explicit disabled
    `review-agent` within the six-row system roster
  - Empty runtime roots in the exact 0.145.0 `thread/start` response while
    both outbound thread and turn requests bind one exact isolated workspace
    root; missing, added, substituted, or reordered-root contrasts
  - Every observed request/notification classified against the pinned
    projection; unknown and prohibited traffic rejected; remote-control status
    accepted only when disabled and unbound
  - Parent runtime proxy environment closed to the upper/lowercase proxy-name
    set while spawned commands retain the exact inherit-none environment
  - Empty `dynamicTools` and `environments`; command tools closed to
    `shell_tool`, `unified_exec`, and `shell_snapshot`; isolated-workspace
    file-change/apply-patch events; prohibited schema variants that remain
    disabled; and rejection of every observed prohibited item/event
  - Exactly-one feature-row classification as permitted built-in tool,
    permitted non-tool runtime behavior, or must-be-disabled tool-bearing
    behavior; independently, exactly-one generated protocol-item
    classification as permitted side effect, non-side-effect protocol traffic,
    or prohibited capability event; missing, duplicate, unknown, and
    unclassified contrasts for both mappings
  - Missing profile attestation, wrong effective sandbox, profile/config
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
  - Crash points before run install, after run install, after receipt fsync, after pointer replace, after parent fsync, and before receipt removal
  - Stage timeout with absent output then one success; two absent-output
    timeouts; complete-output reconciliation without reinvocation; partial or
    extra output stop; and non-retry of protocol or security failures
  - Preflight crash before replacement and after replacement but before
    directory fsync; pass-before-fsync rejection; malformed temporary cleanup;
    prior-attestation preservation on failure; and stale prior evidence never
    satisfying the current preflight
  - Every closed preflight diagnostic/result/phase combination, malformed,
    mismatched, absent, and symlinked change roots before runtime discovery
  - Fresh generation-time attestation embedded in
    `behavior-implementation-manifest.json`; missing, stale, substituted, and
    tampered nested attestation invalidating the manifest reference, input-set
    identity, immutable run, pointer, and report selector without
    validation-time substitution
  - Later commits with unchanged referenced bytes versus changed referenced bytes
  - Resource-map, raw-byte-copy, trigger, stop, claim, handoff, complete review-bundle, and isolation tests
  - Example-only spec/test-spec rejection and valid compact simple-change cases
- Implementation steps:
  - Implement only the minimal evidence-only `check-environment` preflight as the
    first bounded M2 slice.
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
    Require the exact approved Codex 0.145.0 schema and complete
    protocol-classification identities before `thread/start`; require exactly
    96 classified feature rows.
  - Build a fresh mode-restricted `CODEX_HOME` with one named permission
    profile: root denied, minimal runtime paths readable, isolated workspace
    writable, and child-command network disabled. Do not combine the profile
    with legacy `sandbox_mode`.
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
    protocol traffic, or prohibited capability event. Reject missing,
    duplicate, unknown, or unclassified item mappings.
  - Permit command side effects only through `shell_tool`, `unified_exec`, or
    `shell_snapshot`, and file-change/apply-patch events only in the isolated
    workspace. A schema-supported prohibited variant must be disabled
    pre-turn and fails the accepted turn if observed.
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
    `codex sandbox --include-managed-config`. Require workspace read/write and
    deny unmanifested source, private-auth path, and network access.
  - Inject a transient parent canary and require exact child environment names
    plus canary absence from environment values, argv, stdin, readable paths,
    and process metadata. Persist only typed non-secret decisions.
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
  - Assemble the five skill packages, applicable instructions, contracts, scenario, and candidates into a fresh isolated workspace.
  - Launch the identified runtime through the preflight-proven sandbox and
    private runtime home; derive a fresh generation-time attestation for the
    exact eleven-row runtime inventory—five enabled manifested lifecycle rows and
    six generated-config-bound disabled system rows—while keeping the
    five-package resource set as a distinct input; embed the attestation in
    `behavior-implementation-manifest.json`, and bind that manifest reference
    transitively through the input-set identity, immutable run, pointer, and
    report selector. The preflight artifact is feasibility evidence only and
    is not substituted for this fresh generation record.
  - Build and validate the sibling temporary run; move it to the deterministic
    non-authoritative staging root and fsync; exclusively write and fsync the
    prepared receipt; install and fsync the immutable run; validate it;
    replace/fsync the pointer; reconcile; remove the receipt and fsync.
  - Implement validation-only reuse that never invokes a lifecycle skill and never substitutes validation-time environment data.
  - Exercise the full pipeline with controlled fixture packages without writing canonical evidence.
  - Write and map the shared boundary reference in the five participating packages, keeping stage-specific triggers, claims, stops, and handoffs in each `SKILL.md`.
  - Generate the real `spec -> spec-review -> test-spec -> test-spec-review`
    run through `workflow`: each stage skill writes its complete artifact below
    the isolated output root, the harness snapshots before advancing, and no
    harness renderer supplies normative artifact content.
  - Reconcile a timed-out stage before retry: accept one complete valid output
    without reinvocation, retry once only when no output exists, and stop on
    partial output or protocol/security failure.
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
    96 feature rows, five enabled user plus six disabled system skill rows,
    exact thread/turn root requests, classified observed events, and closed
    parent-proxy/child-environment evidence
  - durable current `runtime-preflight-attestation.json` whose reference
    matches the pass receipt, plus a fresh nested generation attestation bound
    by the current behavior implementation manifest and immutable run
  - current `behavior-implementation-manifest.json`
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
  - Stop on a pinned schema/protocol identity mismatch, any feature count
    other than 96, enabled or missing `review-agent`, missing/additional/
    substituted/reordered request roots, non-disabled or bound remote-control
    status, unknown/prohibited observed traffic, an unlisted parent
    environment variable, or any proxy leakage into a spawned command.
  - Stop on any unknown or mismatched preflight diagnostic/phase, invalid
    change root, pass emitted before file and directory durability, unresolved
    preflight temporary state, substituted generation attestation, or attempt
    to replace recorded attestation with validation-time runtime evidence.
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
  - Shared reference use could hide stage-specific stop or claim boundaries.
- Rollback/recovery:
  - Revert the five package edits and current pointer together, retain immutable failed runs as non-current evidence, and retain the M1 deterministic engine.

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
  before any other harness or participating-skill mutation.
- M2 harness and recovery proof before any canonical published-skill behavior generation.
- M3 before M4 so downstream skills consume a stable upstream record contract and current immutable run.
- M1-M3 before M4 computes capability outcomes.
- M4 writes the R28y report from implementation evidence; its code review then closes the implementation milestone without recursively rewriting the report to cite its own review.
- R28o remains unsatisfied until all milestone reviews and the final holistic code review are clean, review resolution is closed, explain-change is current, and final verification passes.
- Separate implementation authorization before M1.
- Separate verification authorization only after implementation closeout and final review evidence exist.

## Progress

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

## Surprises and discoveries

- The direct sandbox `workspace_write` probe proves that spawned commands can
  write under the permission profile; it does not prove that a schema-bound
  app-server stage turn exposes a file-write tool to the agent. Runtime
  feasibility must test the actual stage-output transport, not a neighboring
  capability.

- The unified automation state adapter writes `run.pause_reason`, while the
  change-metadata schema currently accepts `run.stop_reason`. The run was
  normalized through the sole state writer. This pre-existing harness mismatch
  is outside the boundary-proof implementation scope and requires a focused
  workflow-automation bugfix before the next release.
- M1 aligned-surface audit: selector registration, public skills, shared
  references, adapters, release notes, and the canonical capability report are
  intentionally unaffected because M2-M4 own those surfaces.

## Validation notes

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
- Readiness is not implementation completion or final closeout.
