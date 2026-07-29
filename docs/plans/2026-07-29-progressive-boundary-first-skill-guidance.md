<!-- Template: plan-skeleton-v3 -->
<!-- Skill: plan -->
<!-- Template status: normative -->

# Progressive Boundary-First Skill Guidance

## Purpose / big picture

Refine the pending `boundary-first-v1` capability so related published skills
consider key boundaries without requiring the user to name the method, while
keeping routine work concise.

The implementation replaces one full reference in every governed skill with a
compact common core, two owner-scoped formal resources, exact approved-artifact
slices for downstream stages, hazard-driven scenario selection, and
surface-owned validation.
It preserves one semantic model, deterministic portable packages, and the
existing prospective activation boundary.

This plan does not delete artifact-lifecycle validation.
It removes skill text as a reason to select that validator while preserving
lifecycle checks for actual governed artifacts and mixed changed sets.

## Current Handoff Summary

- Owning change record:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers,
routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal:
  `docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Spec:
  `specs/progressive-boundary-first-skill-guidance.md`
- Approved spec review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-r1.md`
- Architecture:
  `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Approved architecture review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r2.md`
- Boundary-first method:
  `skills/plan/references/boundary-first-method-v1.md`
- Test spec: pending `test-spec` after plan-review

## Context and orientation

The current repository has one authored boundary method at
`specs/references/boundary-first-method-v1.md`.
`scripts/boundary_first_reference.py` owns a hard-coded ten-skill projection
inventory, and `scripts/project-boundary-first-reference.py` exposes
deterministic `--check` and `--write` modes.
Every governed skill currently maps one full projected copy at
`references/boundary-first-method-v1.md`.

`scripts/boundary_first_validation.py` validates feature records, proof maps,
the pending or active activation record, projection identity, grandfathering,
and immutable-release rollback.
`specs/boundary-first-activation.yaml` currently binds the one canonical
reference and one projection-set digest.

`scripts/skill_validation.py` validates skill shape and mapped-resource
containment.
`scripts/test-skill-validator.py` owns cross-skill resource and shared-block
regressions.
The ten canonical `skills/<skill>/SKILL.md` bodies are the only authored
published skill sources.

`scripts/validation_selection.py` classifies changed paths and builds
check-owned affected-path sets.
It currently treats `skills/` as an authoritative lifecycle surface in paths
that can select `artifact_lifecycle.validate`.
The selector already has dedicated skill, boundary, projection, adapter, and
prose checks that must remain.

`scripts/build-skills.py`, `scripts/adapter_distribution.py`,
`scripts/build-adapters.py`, and `scripts/validate-adapters.py` already copy
complete skill roots and compare mapped-resource identities through generated,
packed, and clean-installed Codex, Claude, and opencode surfaces.
The progressive implementation extends the expected resource inventory rather
than creating a second packaging system.

The exact-owning-change-record lifecycle-validator correction in
`scripts/artifact_lifecycle_validation.py` and
`scripts/test-artifact-lifecycle-validator.py` is an already-completed
prerequisite on this branch.
It remains in validation scope, but it is not reimplemented by these
milestones.

Capability activation remains `pending` throughout this first implementation
slice.
Active-state behavior is proved with isolated candidate fixtures.
A later release-bound transaction supplies immutable activating and rollback
release identities and performs the atomic accepted-state switch.

## Non-goals

- Do not add, remove, or rename the eight boundary dimensions.
- Do not introduce `boundary-first-v2`, a stage-local vocabulary, or a second
  semantic owner.
- Do not require formal boundary records for non-behavior work.
- Do not require Cartesian combinations of boundary partitions.
- Do not create a runtime service, context-packet artifact, attestation store,
  network dependency, or model gate.
- Do not remove artifact-lifecycle validation from proposals, specs, test
  specs, architecture, ADRs, plans, change records, or mixed changed sets.
- Do not let structural validators judge semantic completeness.
- Do not hand-edit generated adapter packages or track temporary install trees.
- Do not impose a hard byte, token, document-length, or runtime budget.
- Do not change repository activation from `pending` in this implementation
  slice.
- Do not publish, release, install from a live registry, or perform another
  external mutation.

## Requirements covered

| Requirement group | Owning milestones |
| --- | --- |
| PBS-R001 through PBS-R006: semantic-version preservation, pending state, and active-only adoption | M2, M4 |
| PBS-R007 through PBS-R011: automatic compact scan and proportional formalization | M2 |
| PBS-R012 through PBS-R016: closed resource layers, maps, and scan placement | M1, M2 |
| PBS-R017 through PBS-R020: stage ownership, sliced reads, expansion, and upstream routing | M2 |
| PBS-R021 through PBS-R024: outcome- and hazard-driven scenario selection | M2 |
| PBS-R025 through PBS-R031: path-owned validation and structural claim limits | M2, M3 |
| PBS-R032 through PBS-R038: deterministic projection, parity, activation, recovery, diagnostics, and portability | M1, M3, M4 |
| AC-PBS-001 through AC-PBS-007: prompt-independent and progressively loaded behavior | M1, M2 |
| AC-PBS-008 through AC-PBS-009: skill-only and mixed validation selection | M3 |
| AC-PBS-010 through AC-PBS-016: parity, failure closure, pending activation, compatibility, diagnostics, and measurements | M1, M2, M3, M4 |

### Boundary and interaction ownership

| Boundary or interaction | Owning milestone | Affected surfaces | Rollback unit | Proof timing |
| --- | --- | --- | --- | --- |
| BND-INPUT-001 | M2 | ten compact scans and formalization conditions | canonical skill-guidance commit | M2 skill fixtures before code review |
| BND-INPUT-002 | M2 | cited row reads, expansion, and upstream-gap routing | canonical skill-guidance commit | M2 known, missing, stale, unknown, ambiguous, conflicting, and escaped-ID fixtures |
| BND-STATE-001 | M4 | pending manifest and isolated active candidate | parity and activation-readiness commit | M4 pending/live and active-fixture checks |
| BND-STATE-002 | M4 | preactivation source rollback and immutable-release rollback validation | parity and activation-readiness commit | M4 rollback fixtures before code review |
| BND-AUTH-001 | M1 | closed resource manifest, canonical owners, consumer matrix, and skill maps | resource-contract and projection commit | M1 schema, ownership, and projection tests |
| BND-AUTH-002 | M2 | feature, proof, plan, implementation, review, and validator responsibilities | canonical skill-guidance commit | M2 semantic-owner and negative-mutation fixtures |
| BND-AUTH-003 | M3 | skill-only, governed-artifact, change-record, and mixed selector paths | selector-routing commit | M3 affected-path assertions |
| BND-COMPOSE-001 | M1, M4 | canonical, projected, generated, packed, and installed resources | M1 resource projection; M4 derived parity evidence | M1 canonical/projection proof, M4 package/install proof |
| BND-COMPOSE-002 | M2 | approved row slices and public, helper, sibling, or alternate paths | canonical skill-guidance commit | M2 expansion and material-sibling fixtures |
| BND-COMPOSE-003 | M3 | skill-only, lifecycle-only, mixed, and selector-change sets | selector-routing commit | M3 complete path matrix |
| BND-TEMPORAL-001 | M1, M4 | repeated and interrupted projection, retry, candidate activation, and rollback | M1 projection engine; M4 activation-readiness evidence | M1 idempotency/interruption proof, M4 coherent candidate proof |
| BND-RECOVERY-001 | M1, M2 | missing resources or IDs, semantic discovery, and proof gaps | owning M1 or M2 commit | local failure and owner-route tests in each milestone |
| BND-RECOVERY-002 | M3, M4 | selector omission, projection drift, mixed bundles, and rollback validation | M3 selector route; M4 parity evidence | M3 mixed-route proof, M4 divergent-package and rollback proof |
| BND-COMPAT-001 | M2, M4 | pending, active candidate, grandfathered artifacts, and substantive revision | skill-guidance commit; activation-readiness commit | M2 compatibility guidance, M4 isolated state fixtures |
| BND-COMPAT-002 | M3, M4 | old and refined selector routes plus pre- and post-activation rollback | selector-routing commit; activation-readiness commit | M3 selection proof, M4 rollback composition |
| BND-ENV-001 | M1, M4 | repository, temporary generated tree, archive, clean install, and unavailable tool | M1 tracked resources; M4 derived evidence only | M1 path safety, M4 three-adapter parity and explicit unavailable-proof handling |
| INT-001 | M1, M4 | stale stage-family projection during activation | resource projection plus activation-readiness evidence | M4 blocks incomplete candidate after M1 identities exist |
| INT-002 | M2 | insufficient artifact slice and differing sibling result | canonical skill-guidance commit | M2 expansion, proof-gap, and spec-gap scenarios |
| INT-003 | M3 | skill-path optimization combined with a changed feature spec | selector-routing commit | M3 mixed-set affected-path proof |
| INT-004 | M2, M4 | prompt-independent adoption while pending, non-behavioral, or grandfathered | skill-guidance commit; activation-state fixtures | M2 guidance proof and M4 pending/active matrix |
| INT-005 | M1, M4 | missing installed family resource hidden by runtime fallback | resource projection plus package/install proof | M4 fails at first divergent layer |

## Milestones

### Preimplementation gate. Test-proof alignment

- Gate kind: upstream lifecycle gate, not an implementation milestone.
- Owner: `test-spec`, followed by `test-spec-review`.
- Goal: Turn every approved requirement, boundary, interaction, acceptance
  criterion, and edge case into concrete proof before production code changes.
- Inputs are read-only during implementation:
  - approved feature specification;
  - approved architecture and accepted ADR;
  - this plan;
  - existing boundary, skill, selector, adapter, lifecycle-validator, and
    release fixtures.
- Exit criteria:
  - every PBS-R requirement maps to one or more stable test cases;
  - every boundary and selected interaction maps to direct proof or a visible
    blocking gap;
  - the proof map distinguishes repository-live pending behavior from isolated
    active-candidate fixtures;
  - exact commands and derived-output locations are approved;
  - selector proof includes skill-only, generated-only, lifecycle-only, mixed,
    and selector-change path sets;
  - the completed exact-owning-change-record regression is cited as a
    prerequisite rather than specified as new implementation work.
- Failure behavior: route missing normative behavior to `spec` or design gaps
  to `architecture`; implementation does not repair an upstream artifact.

### M1. Closed progressive resource contract and deterministic projection

- Milestone kind: implementation
- Goal: Replace the hard-coded one-reference inventory with the reviewed
  three-resource manifest and deterministic, preflight-first projection while
  retaining the compatibility-stable compact-core path.
- Requirements: PBS-R002, PBS-R012 through PBS-R016, PBS-R032 through PBS-R034,
  PBS-R037, PBS-R038; BND-AUTH-001, BND-COMPOSE-001,
  BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001.
- Files/components likely touched:
  - `specs/boundary-first-resources.yaml`
  - `specs/references/boundary-first-method-v1.md`
  - `specs/references/boundary-first-feature-authoring-v1.md`
  - `specs/references/boundary-first-proof-v1.md`
  - `specs/boundary-first-activation.yaml`
  - `scripts/boundary_first_reference.py`
  - `scripts/project-boundary-first-reference.py`
  - `scripts/boundary_first_validation.py`
  - `scripts/test-boundary-first-reference.py`
  - `scripts/test-boundary-first-validation.py`
  - the ten governed `skills/*/references/` projection directories
  - the ten governed `skills/*/SKILL.md` resource maps
  - focused resource-map checks in `scripts/test-skill-validator.py`
- Dependencies:
  - approved plan-review;
  - approved preimplementation test specification;
  - existing resource-integrity and adapter-copy contracts remain unchanged.
- Tests to add/update:
  - exact top-level and entry field sets, schema and contract versions,
    resource order, paths, and consumer order;
  - explicit `unknown_value` or `not_in_vocabulary` failures before
    consistency checks for fields, IDs, versions, and consumers;
  - missing and duplicate fields, resources, sources, targets, and consumers;
  - absolute, dot-segment, escaping, symlink, missing-source, and
    outside-`references/` path failures;
  - complete preflight before write, no partial mutation on invalid input,
    deterministic retry, raw-byte identity, manifest identity, and sorted
    projection-set identity;
  - missing, additional, stale, unexpected, path-divergent, and byte-divergent
    projections;
  - exact compact-core membership for all ten skills, exact
    feature-authoring membership for `spec` and `spec-review`, and exact proof
    membership for `test-spec` and `test-spec-review`;
  - activation compatibility fields plus resource-manifest and complete
    projection-set identities while repository state remains `pending`.
- Implementation steps:
  - write manifest parser and invalid-manifest tests before changing live
    projection;
  - split the full method into one non-overlapping compact core and the two
    owner-scoped formal resources;
  - make the projection engine derive its complete matrix only from the
    manifest;
  - preflight the complete matrix before write mode mutates any target;
  - update governed resource maps with allowed `READ` verbs and stage-specific
    load conditions;
  - write the exact expected projections and reject unexpected copies;
  - extend activation validation with manifest and projection identities
    without changing `state: pending`.
- Validation commands:
  - `python scripts/test-boundary-first-reference.py`
  - `python scripts/project-boundary-first-reference.py --check`
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/validate-boundary-first.py --check`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
- Expected observable result: One closed manifest determines every canonical
  and projected resource, every governed skill contains exactly its
  stage-family resource set, repetition preserves byte identity, and invalid
  or partial matrices fail before activation or partial write.
- Commit message: `M1: add progressive boundary resource projection`
- Milestone closeout evidence:
  - manifest failure matrix and projection identity results;
  - focused skill resource-map results;
  - M1 implementation evidence under the owning change root;
  - clean or resolved code-review for M1.
- Risks:
  - changing the compatibility-stable core contents can leave a consumer with
    missing formal guidance or an unexpected extra projection.
- Rollback/recovery:
  - revert the manifest, three-source split, activation identity fields,
    resource-map changes, projection engine, and projected files as one
    tracked unit;
  - restore the preceding single full reference and ten projections;
  - keep activation `pending` and discard any temporary derived output.

### M2. Automatic compact scan and stage-owned progressive guidance

- Milestone kind: implementation
- Goal: Make boundary awareness prompt-independent and proportional while
  preserving one feature owner, one proof owner, exact downstream slices, and
  hazard-driven scenario selection.
- Requirements: PBS-R001 through PBS-R011, PBS-R015 through PBS-R024,
  PBS-R030, PBS-R031, PBS-R035, PBS-R037, PBS-R038;
  BND-INPUT-001, BND-INPUT-002, BND-AUTH-002, BND-COMPOSE-002,
  BND-RECOVERY-001, BND-COMPAT-001; INT-002, INT-004.
- Files/components likely touched:
  - `templates/shared/boundary-first-compact-scan.md`
  - `skills/workflow/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/test-spec-review/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - focused shared-block and semantic-contract checks in
    `scripts/test-skill-validator.py`
- Dependencies:
  - M1 resource ownership and projections reviewed and closed.
- Tests to add/update:
  - exact shared four-question scan appears in all ten governed skill bodies
    and drift from the contributor source fails;
  - method-name presence never controls scan or formal applicability;
  - non-behavior work creates no formal record or scenario inventory;
  - `spec` authors and `spec-review` judges the feature record only when the
    active contract requires it;
  - `test-spec` authors and `test-spec-review` judges the proof record;
  - plan, implementation, review, and verify consume approved cited rows
    before optional compact-core expansion and never load family resources;
  - missing, stale, unknown, ambiguous, conflicting, or escaped IDs expand
    context or route to the correct upstream owner;
  - a materially different sibling path adds proof, while duplicate outcome
    combinations do not;
  - structural validators cannot create, repair, or approve semantic content;
  - pending, active candidate, grandfathered non-substantive revision, and
    substantive revision guidance remain distinct.
- Implementation steps:
  - add semantic fixtures before editing shipped skill prose;
  - copy the compact scan directly into every governed skill from the checked
    shared block;
  - revise each stage only for its approved responsibility, load condition,
    stop behavior, mutation authority, and handoff;
  - make exact artifact slices the default downstream input and full-resource
    expansion the exception;
  - state the distinct-outcome and material-hazard stop rule without a
    Cartesian inventory;
  - keep repository-maintainer manifest, projection, selector-path, and
    shared-block mechanics out of shipped skill prose.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/project-boundary-first-reference.py --check`
  - `python scripts/validate-boundary-first.py --check`
- Expected observable result: Equivalent behavior-changing requests receive
  the same concise scan whether or not the user names the method; only owning
  stages load formal guidance, downstream stages rely on approved IDs, and
  non-behavior work remains concise.
- Commit message: `M2: make boundary guidance automatic and stage scoped`
- Milestone closeout evidence:
  - ten-skill compact-scan drift result;
  - stage responsibility and negative-mutation matrix;
  - representative non-behavior, qualifying, slice-expansion, sibling-path,
    and gap-routing scenarios;
  - clean or resolved code-review for M2.
- Risks:
  - generic shared wording can either force formalization too broadly or omit
    a stage-specific stop and authority boundary.
- Rollback/recovery:
  - revert the compact shared block, ten canonical skill bodies, and focused
    skill tests together;
  - leave M1 resource packaging present but dormant under the still-pending
    capability;
  - regenerate temporary mirrors from restored canonical skills.

### M3. Surface-owned validation selection

- Milestone kind: implementation
- Goal: Stop treating canonical or generated published skill text as
  lifecycle-managed state while preserving every purpose-built skill check
  and every lifecycle check owned by actual governed artifacts.
- Requirements: PBS-R025 through PBS-R031, PBS-R036, PBS-R037;
  BND-AUTH-003, BND-COMPOSE-003, BND-RECOVERY-002, BND-COMPAT-002;
  INT-003.
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - selector-facing classifications for canonical skills, generated mirrors,
    boundary resources, adapters, lifecycle artifacts, and change records
- Read-only prerequisite:
  - the completed exact-owning-change-record correction in
    `scripts/artifact_lifecycle_validation.py` and its regression tests.
- Dependencies:
  - M1 purpose-built boundary and projection surfaces exist;
  - M2 skill validation and prose ownership are settled;
  - the lifecycle-validator prerequisite passes independently.
- Tests to add/update:
  - canonical governed skill-only changes select skill, boundary, projection,
    adapter, and applicable prose checks without
    `artifact_lifecycle.validate`;
  - generated skill-only changes select derivation and drift proof without
    lifecycle validation;
  - lifecycle-only proposal, spec, test-spec, architecture, ADR, plan, review,
    and change-record paths retain lifecycle validation with owned affected
    paths;
  - mixed skill plus feature-spec paths retain both check families and do not
    broaden either check's affected paths;
  - selector and selector-test changes select the full selector regression
    suite;
  - lifecycle-like words in skill prose do not affect classification;
  - unrelated check coverage, failure propagation, exit codes, and
    fail-fast behavior remain unchanged.
- Implementation steps:
  - add the five changed-set regression classes before altering
    classification;
  - separate published skill/resource ownership from lifecycle-managed
    artifact ownership at the narrowest selector decision;
  - preserve existing purpose-built selection and affected-path aggregation;
  - prove mixed-set composition rather than relying on union-by-assumption;
  - retain artifact-lifecycle validation unchanged for actual governed
    artifacts and change records.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path skills/spec/SKILL.md`
  - `python scripts/select-validation.py --mode explicit --path skills/spec/SKILL.md --path specs/progressive-boundary-first-skill-guidance.md`
  - `python scripts/test-artifact-lifecycle-validator.py`
- Expected observable result: Skill-only validation is relevant and smaller,
  governed artifacts remain protected, and a mixed changed set selects both
  families with correctly scoped paths.
- Commit message: `M3: scope lifecycle validation to governed artifacts`
- Milestone closeout evidence:
  - canonical-skill, generated-skill, lifecycle-only, mixed, and
    selector-change selection snapshots;
  - exact affected-path assertions;
  - completed lifecycle-validator prerequisite result;
  - clean or resolved code-review for M3.
- Risks:
  - a broad prefix change can accidentally suppress lifecycle validation for
    specs or change records, or remove a boundary/package check from skills.
- Rollback/recovery:
  - revert only the selector classification and its focused tests;
  - restore the former extra skill-path lifecycle route without changing the
    lifecycle validator or M1/M2 resource and guidance behavior.

### M4. Derived package parity, loading measurement, and pending activation readiness

- Milestone kind: implementation
- Goal: Prove the complete tracked progressive bundle and derived
  Codex/Claude/opencode package layers against one candidate identity, record
  proportional-loading baselines, and leave the accepted repository state
  `pending`.
- Requirements: PBS-R003 through PBS-R006, PBS-R014, PBS-R032 through
  PBS-R038; BND-STATE-001, BND-STATE-002, BND-COMPOSE-001,
  BND-TEMPORAL-001, BND-RECOVERY-002, BND-COMPAT-001,
  BND-COMPAT-002, BND-ENV-001; INT-001, INT-004, INT-005.
- Files/components likely touched:
  - `scripts/fixtures/boundary-first/loading-profiles.yaml`
  - focused measurement support in existing boundary or skill validation
    modules
  - `scripts/test-boundary-first-validation.py`
  - `scripts/test-adapter-distribution.py`
  - change-local M4 implementation evidence and identity references
  - `specs/boundary-first-activation.yaml`, retaining `state: pending`
- Derived, untracked proof surfaces:
  - temporary generated skill mirror;
  - temporary adapter release-output directory;
  - packed Codex, Claude, and opencode archives;
  - clean installed target trees.
- Dependencies:
  - M1 through M3 reviewed and closed;
  - no open material review finding;
  - the matching test spec owns the exact active-candidate and rollback
    fixtures;
  - current adapter support version is read from
    `dist/adapters/manifest.yaml`, not invented by the implementation.
- Tests to add/update:
  - exact mapped, initially loaded, and permitted-expansion resource IDs for
    every representative stage family;
  - before-and-after canonical bytes, mapped-resource counts, and
    representative initial and expanded loaded-resource counts;
  - no hard budget or pass/fail threshold derived from those measurements;
  - canonical-to-projected-to-generated-to-packed-to-installed raw-byte
    parity for every mapped layer and supported adapter;
  - missing or additional compact, feature-authoring, or proof resources fail
    at the first divergent layer;
  - runtime fallback cannot satisfy package parity;
  - interrupted or repeated projection cannot yield a mixed accepted bundle;
  - isolated `active` candidate fixtures require the complete progressive
    identities and immutable release fields;
  - preactivation rollback restores the single-reference tracked bundle and
    discards or regenerates derived output;
  - post-activation fixtures select an immutable rollback release with one
    passing archive identity per adapter;
  - unavailable external tools are reported as unavailable proof, never
    success.
- Implementation steps:
  - add the closed loading-profile fixture and measurement assertions first;
  - reuse the existing mapped-resource parity and adapter installation
    machinery for multiple resources;
  - generate skill and adapter outputs only in temporary directories;
  - bind derived results to the candidate source, resource-manifest, and
    projection-set identities;
  - record compact measurements as change-local evidence without raw private
    paths or runtime transcript data;
  - run pending, isolated active-candidate, preactivation rollback, and
    immutable-release rollback proof;
  - confirm the repository activation record still says `pending`.
- Validation commands:
  - `python scripts/test-boundary-first-reference.py`
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/validate-boundary-first.py --check`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `tmp_output="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmp_output" && python scripts/validate-adapters.py --root "$tmp_output" --version v0.1.5 --clean-install-smoke --skill workflow --skill spec --skill spec-review --skill plan --skill plan-review --skill test-spec --skill test-spec-review --skill implement --skill code-review --skill verify`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: The tracked progressive bundle and every derived
  adapter layer agree exactly, representative loading is measurably
  proportional, incomplete candidates fail closed, rollback proof is
  coherent, and repository activation remains `pending`.
- Commit message: `M4: prove progressive boundary package readiness`
- Milestone closeout evidence:
  - resource and representative-loading baseline;
  - generated, archive, and clean-install mapped-resource identities for all
    three adapters;
  - pending-state, active-candidate, and rollback results;
  - broad-smoke result;
  - clean or resolved code-review for M4.
- Risks:
  - packaging proof can accidentally become tracked output, use a stale
    version, expose machine-local paths, or be mistaken for actual activation.
- Rollback/recovery:
  - revert only tracked M4 fixtures, measurement support, and evidence;
  - discard temporary generated, archive, and install trees;
  - restore or retain the reviewed `pending` activation manifest;
  - if a later release activates the capability, rollback belongs to that
    immutable release transaction and is not performed by this plan.

## Validation plan

| Proof layer | Command or check | Purpose |
| --- | --- | --- |
| Resource unit | `python scripts/test-boundary-first-reference.py` | Closed manifest, path safety, projection identity, preflight, drift, and retry behavior |
| Resource live check | `python scripts/project-boundary-first-reference.py --check` | Canonical-to-skill-local exact projection |
| Boundary/activation unit | `python scripts/test-boundary-first-validation.py` | Feature/proof structure, activation identities, candidate state, compatibility, and rollback |
| Boundary live check | `python scripts/validate-boundary-first.py --check` | Current repository boundary and pending activation consistency |
| Published skill unit | `python scripts/test-skill-validator.py` | Compact-scan drift, resource ownership, stage behavior, and semantic claim boundaries |
| Published skill live check | `python scripts/validate-skills.py` | Canonical skill contract and mapped resources |
| Generated skills | `python scripts/build-skills.py --check` | Temporary generated mirror and mapped-resource parity |
| Selector unit | `python scripts/test-select-validation.py` | Skill-only, lifecycle-only, mixed, and selector-change routing |
| Lifecycle prerequisite | `python scripts/test-artifact-lifecycle-validator.py` | Exact owning change-record state and fail-closed lifecycle regressions |
| Adapter unit | `python scripts/test-adapter-distribution.py` | Archive structure and mapped-resource behavior |
| Three-adapter clean install | temporary `build-adapters.py` plus versioned `validate-adapters.py --clean-install-smoke` command from M4 | Canonical, packed, and installed parity without tracked generated output |
| Repository integration | `bash scripts/ci.sh --mode broad-smoke` | Final repository-owned integration scope |

The matching test specification must assign stable command IDs and exact test
case IDs before M1 implementation.
Each milestone runs its smallest focused proof first.
The next milestone waits for clean or resolved code-review of the current
milestone.

## Risks and recovery

- Risk: Resource splitting creates semantic duplication or omission.
  - Recovery: keep ownership tests closed, review the three sources together,
    and roll back the M1 resource transaction atomically.
- Risk: Always-on language produces formal records for trivial work.
  - Recovery: require explicit non-behavior and method-name-only negative
    scenarios in M2 before accepting the guidance.
- Risk: Artifact slices hide a material sibling outcome.
  - Recovery: expand on insufficient IDs and route new semantics to `spec`;
    never let the downstream stage invent the outcome.
- Risk: Selector simplification suppresses a governed-artifact check.
  - Recovery: require exact mixed-set check and affected-path assertions, and
    revert M3 independently if composition fails.
- Risk: Multiple resource copies drift across package layers.
  - Recovery: fail on first divergence, discard derived trees, repair
    canonical sources or projection, and regenerate from scratch.
- Risk: A pending candidate is mistaken for activation.
  - Recovery: retain `state: pending`, label active proof as isolated fixture
    evidence, and reserve the accepted-state switch for a later
    immutable-release transaction.
- Risk: Measurements become an accidental release budget.
  - Recovery: record observed bytes and counts only; any threshold requires a
    later proposal and specification.
- Risk: Existing branch-local lifecycle-validator changes get duplicated or
  obscured.
  - Recovery: treat them as a named prerequisite, run their regression suite,
    and keep progressive implementation milestones out of those files.

## Dependencies

- Proposal, specification, architecture, ADR, and their formal reviews remain
  settled and read-only.
- Plan-review must approve this plan before test-spec authoring.
- Test-spec and test-spec-review must close the preimplementation gate before
  M1.
- The completed lifecycle-validator bug fix must continue passing before M3
  selector changes are reviewed.
- M1 through M4 execute in order, with one implementation and code-review
  closeout per milestone.
- Existing skill resource-integrity, adapter generation, release metadata, and
  immutable rollback mechanisms are reused.
- Temporary generated or installed trees require no external network or live
  registry operation.
- Actual activation depends on a later reviewed release transaction with real
  immutable activating and rollback release identities.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-29 | Use four implementation milestones plus one preimplementation proof gate. | Resource identity, shipped behavior, selector routing, and derived package proof have distinct rollback and review boundaries. | One cross-cutting implementation milestone; one milestone per skill |
| 2026-07-29 | Make M1 the complete resource split and governed resource-map unit. | A partial live split could omit owner-scoped guidance or expose a mixed projection set. | Add sources, manifest, projections, and maps in separate closeout units |
| 2026-07-29 | Keep the lifecycle-validator correction as a verified prerequisite. | The defect is already fixed under the existing contract and is not part of the new progressive selector behavior. | Reimplement or hide the fix inside M3 |
| 2026-07-29 | Keep selector routing in its own milestone. | Skill-path optimization can roll back independently without reverting published guidance or lifecycle-validator semantics. | Couple selection changes to skill prose |
| 2026-07-29 | Keep repository activation pending after parity proof. | This first slice refines resources and guidance; immutable release identities and the accepted atomic switch belong to a later release transaction. | Invent release tags; claim activation from file presence; omit active-candidate proof |
| 2026-07-29 | Measure representative loading without thresholds. | The approved contract requires a baseline before any hard budget. | Token gate, document-length gate, or no measurement |

## Readiness

- See the owning change record for current workflow state.
- After approved plan-review, the immediate next stage is `test-spec`.
- Remaining completion gates are test-spec, test-spec-review, M1 through M4
  implementation and code-review loops, review-resolution when triggered,
  explain-change, verify, and PR handoff.
- Readiness is not Done.
