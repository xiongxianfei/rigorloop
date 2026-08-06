<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->

# Usability-First Boundary-First v0.4.0 Release Test Spec

## Owning change record

`docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`

## Related spec and plan

- Spec: `specs/usability-first-boundary-release.md`
- Plan: `docs/plans/2026-08-06-usability-first-boundary-release.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/usability-first-boundary-release.md` | `spec` | `spec-review-r3`; `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r3.md` |
| Architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-r2`; `docs/changes/2026-08-06-usability-first-boundary-release/reviews/architecture-review-r2.md` |
| Activation ADR | `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md` | `adr-checked-revision-activation` | `architecture-review-r2`; `docs/changes/2026-08-06-usability-first-boundary-release/reviews/architecture-review-r2.md` |
| Execution plan | `docs/plans/2026-08-06-usability-first-boundary-release.md` | `plan` | `plan-review-r2`; `docs/changes/2026-08-06-usability-first-boundary-release/reviews/plan-review-r2.md` |

## Testing strategy

Fixture-backed unit tests prove closed activation fields, derivation inputs and outputs, fail-closed vocabularies, rollback selection, and release identity values.
Integration tests prove automatic concise behavior across the ten governed skills, stage ownership, checked-revision validation, selector cleanup, routine release preservation, and bounded diagnostics.
Local end-to-end tests generate and inspect Codex, Claude, and opencode packages, adapter archives, and the packed npm package in temporary directories.
Smoke proof executes the release-selected CI bundle and standing full gate twice: M3 proves the reviewed pending baseline, and M4 proves the changed active state.
Contract proof checks normalized boundary records, exact custom-path retirement, release-profile authority, trusted workflow retention, and public-claim separation.
Migration proof covers the frozen historical inventory, post-activation adoption, exact `v0.3.6` rollback, and immutable `v0.4.0` recovery.

No manual proof is required before implementation handoff.
External tagging, publication, registry access, and public `npx` smoke are outside lifecycle execution; repository tests prove that their routine mechanisms remain present and that unavailable public evidence stays open.
The proof set combines partitions only when an approved boundary or selected interaction changes the outcome.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| UBR-R001 | T1, T5 | integration, e2e | All ten skills apply the compact scan without a keyword, including generated packages. |
| UBR-R002 | T1, T2 | integration | Material cases are included and irrelevant dimensions are omitted semantically. |
| UBR-R003 | T3 | integration | Contract, risk, and explicit-request triggers expand only the applicable analysis. |
| UBR-R004 | T4 | contract | Every stage retains its approved artifact and gate authority. |
| UBR-R005 | T4, T23 | contract | Formal records remain normalized; informal work creates no extra record. |
| UBR-R006 | T6, T7 | unit, integration | Pending and active are exact, independently valid snapshots. |
| UBR-R007 | T7, T8, T9 | unit, integration | One-time derivation and current-file validation cover all coherent and divergent surfaces. |
| UBR-R008 | T9, T10 | integration | Success reports snapshot and release intent without public-release claims. |
| UBR-R009 | T13 | contract | Profile, Git tag, package version, and dist-tag agree exactly. |
| UBR-R010 | T14, T16, T17 | e2e, smoke | Canonical, generated, archived, packed, and installed resources agree. |
| UBR-R011 | T15, T16, T17 | integration, smoke | Preparation, preflight, and full-gate categories remain effective. |
| UBR-R012 | T11, T15, T20 | contract, integration | Custom cleanup cannot replace the routine trusted release and closeout path. |
| UBR-R013 | T11 | integration | The closed delete/remove inventory is exact and ordinary selection remains. |
| UBR-R014 | T21 | integration | Lifecycle commands cannot tag, push, publish, merge, or claim availability. |
| UBR-R015 | T12, T19 | migration | Exact complete `v0.3.6` metadata remains the rollback authority. |
| UBR-R016 | T19 | migration | Pre-public failure is reversible; post-public recovery is immutable and phase-owned. |
| UBR-R017 | T10, T22 | integration | Diagnostics and evidence suppress private and machine-local values. |
| UBR-R018 | T1, T2, T3 | integration | Representative journeys use semantic assertions rather than prose metrics. |
| UBR-R019 | T12 | migration | Historical inventory and prospective adoption remain distinct and authoritative. |
| UBR-R020 | T13, T18, T20 | contract, integration | Exact reviewed tag identity is required; mismatch and rewrite fail. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Level | Notes |
| --- | --- | --- | --- |
| AC-UBR-001 | T1, T6, T8 | integration | Specification and inspection journeys cover the named snapshot and caller boundaries. |
| AC-UBR-002 | T1, T9, T11 | integration | Local journeys omit public-state expansion while cleanup preserves release and rollback. |
| AC-UBR-003 | T4, T23 | contract | Formal records remain normalized and informal output remains artifact-free. |
| AC-UBR-004 | T7, T9, T17 | integration, smoke | Active state passes locally without baseline reachability, tag, network, or public claim. |
| AC-UBR-005 | T5, T8, T14 | integration, e2e | Every named stale or divergent layer fails with bounded diagnostics. |
| AC-UBR-006 | T13, T14, T16 | contract, e2e | Profile, package, notes, evidence, and three targets agree. |
| AC-UBR-007 | T15, T16, T20 | integration, smoke | The original release gates, trusted publication, public smoke, and closeout remain. |
| AC-UBR-008 | T11 | integration | All eight retirement dispositions and retained selection paths are proved. |
| AC-UBR-009 | T12, T19 | migration | Rollback remains complete and post-public recovery fixes forward. |
| AC-UBR-010 | T21 | integration | No pre-release lifecycle command mutates external publication state. |
| AC-UBR-011 | T1, T2, T3 | integration | Tests reject exact wording, count, or method-name assertions as the semantic oracle. |
| AC-UBR-012 | T23 | contract | Requirement, boundary, interaction, command, and milestone references fail closed when incomplete. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T6 | The existing boundary validator specification journey covers snapshot inputs without public-release expansion. |
| E2 | T1, T8 | Loader and public-caller inspection covers the observed call path and excludes unrelated provider behavior. |
| E3 | T1, T11 | Code review checks exact custom retirement and retained validator, release, and rollback paths. |
| E4 | T9 | Active checked-revision validation passes without a tag and never claims publication. |
| E5 | T15, T16 | The routine release mechanism prepares and verifies one coherent package. |
| E6 | T19 | Failure and rollback use phase-specific immutable recovery. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: UBR-R001, UBR-R002, UBR-R003, UBR-R004, UBR-R005, UBR-R006, UBR-R007, UBR-R008, UBR-R009, UBR-R010, UBR-R011, UBR-R012, UBR-R013, UBR-R014, UBR-R015, UBR-R016, UBR-R017, UBR-R018, UBR-R019, UBR-R020

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | UBR-R001, UBR-R002, UBR-R003, UBR-R018 | BND-INPUT-001 | T1, T2, T3 | integration | automated | CMD01, CMD02 | `evidence/implementation-m1.md` | M1 | - | - |
| PRF-002 | covered | UBR-R006, UBR-R007, UBR-R008, UBR-R014, UBR-R016, UBR-R019 | BND-STATE-001 | T6, T7, T8, T9, T19, T21 | integration | automated | CMD05, CMD06 | `evidence/implementation-m2.md`; `evidence/implementation-m4.md` | M2, M4 | - | - |
| PRF-003 | covered | UBR-R009, UBR-R020 | BND-AUTH-001 | T13, T18, T20 | contract | automated | CMD13, CMD17, CMD18 | `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | M3, M4 | - | - |
| PRF-004 | covered | UBR-R004, UBR-R005, UBR-R010, UBR-R011, UBR-R012, UBR-R013 | BND-COMPOSE-001 | T4, T5, T11, T14, T15, T16, T17, T20 | end-to-end | automated | CMD01, CMD02, CMD07, CMD14, CMD15, CMD17, CMD18 | `evidence/implementation-m1.md`; `evidence/implementation-m2.md`; `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | M1, M2, M3, M4 | - | - |
| PRF-005 | covered | UBR-R012, UBR-R016, UBR-R020 | BND-TEMPORAL-001 | T18, T19, T20 | integration | automated | CMD13, CMD14, CMD18 | `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | M3, M4 | - | - |
| PRF-006 | covered | UBR-R015, UBR-R016 | BND-RECOVERY-001 | T12, T19 | integration | automated | CMD06, CMD13, CMD18 | `evidence/implementation-m2.md`; `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | M2, M3, M4 | - | - |
| PRF-007 | covered | UBR-R006, UBR-R007, UBR-R013, UBR-R015, UBR-R019 | BND-COMPAT-001 | T11, T12 | contract | automated | CMD06, CMD07 | `evidence/implementation-m2.md` | M2 | - | - |
| PRF-008 | covered | UBR-R007, UBR-R012, UBR-R014, UBR-R017 | BND-ENV-001 | T9, T10, T21, T22 | integration | automated | CMD05, CMD06, CMD12, CMD17, CMD18 | `evidence/implementation-m2.md`; `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | M2, M3, M4 | - | - |
| PRF-009 | covered | UBR-R002, UBR-R003, UBR-R004, UBR-R005 | INT-001 | T1, T2, T3, T4 | integration | automated | CMD01, CMD02 | `evidence/implementation-m1.md` | M1 | - | - |
| PRF-010 | covered | UBR-R006, UBR-R008, UBR-R009, UBR-R012, UBR-R014, UBR-R020 | INT-002 | T9, T13, T18, T20, T21 | integration | automated | CMD05, CMD13, CMD17, CMD18 | `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | M3, M4 | - | - |
| PRF-011 | covered | UBR-R010, UBR-R011, UBR-R012, UBR-R013, UBR-R015, UBR-R016 | INT-003 | T11, T12, T15, T16, T17, T19, T20 | end-to-end | automated | CMD07, CMD13, CMD14, CMD15, CMD17, CMD18 | `evidence/implementation-m2.md`; `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | M2, M3, M4 | - | - |

All evidence paths in the proof map are relative to `docs/changes/2026-08-06-usability-first-boundary-release/`.

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 no admitted boundary | T2 | No scenario matrix or boundary artifact is emitted. |
| EC2 contract-owned unmentioned boundary | T1, T4 | Governing requirements still produce owned coverage. |
| EC3 explicit depth for one risk | T3 | Only the requested material risk expands. |
| EC4 six inapplicable formal dimensions | T23 | Normalized concise non-applicability remains valid. |
| EC5 one generated target stale | T5, T14 | The first divergent target is identified and validation fails. |
| EC6 active snapshot without tag | T9, T17 | Local activation passes while public-release proof remains unavailable. |
| EC7 mismatched `v0.4.0` tag | T18 | Local and public identity checks fail closed. |
| EC8 partial public evidence | T19, T20 | Closeout remains open and rerunnable. |
| EC9 retired helper or selectable custom check | T11 | Exact retirement validation fails. |
| EC10 activation bypasses routine release | T15, T20 | Static and executable gate proof fails. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD01 | `python scripts/test-skill-validator.py` | existing/configured | implement | M1 | code-review M1 | Block semantic guidance or skill-contract handoff. | Zero tests is failure. | `evidence/implementation-m1.md` | Repository-local fixtures only. |
| CMD02 | `python scripts/test-boundary-first-reference.py` | existing/configured | implement | M1 | code-review M1 | Block resource, projection, or semantic-journey handoff. | Zero tests is failure. | `evidence/implementation-m1.md` | Temporary local fixtures only. |
| CMD03 | `python scripts/validate-skills.py` | existing/configured | implement | M1 | code-review M1 | Block invalid canonical skills. | Not applicable; deterministic validator. | `evidence/implementation-m1.md` | Read-only canonical validation. |
| CMD04 | `python scripts/build-skills.py --check` | existing/configured | implement | M1 | code-review M1 | Block generated skill drift. | Not applicable; deterministic check. | `evidence/implementation-m1.md` | Temporary output only; no canonical write. |
| CMD05 | `python scripts/validate-boundary-first.py --check` | existing/configured | implement | M1, M2, M4 | code-review M1 | Block incoherent records, resources, projections, activation, or rollback. | Not applicable; deterministic check. | Owning milestone evidence. | Read-only checked-revision validation; no history, remote, tag, or network. |
| CMD06 | `python scripts/test-boundary-first-validation.py` | existing/configured | implement | M2, M4 | code-review M2 | Block structural, activation, derivation, compatibility, privacy, or rollback regression. | Zero tests is failure. | `evidence/implementation-m2.md`; `evidence/implementation-m4.md` | Repository-local temporary fixtures only. |
| CMD07 | `python scripts/test-select-validation.py` | existing/configured | implement | M2 | code-review M2 | Block custom-path retirement or ordinary/release selection regression. | Zero tests is failure. | `evidence/implementation-m2.md` | Local selector fixtures; selected checks are not executed. |
| CMD08 | `python scripts/select-validation.py --mode explicit --path scripts/boundary_first_validation.py --path scripts/validate-boundary-first.py --path scripts/test-boundary-first-validation.py --path scripts/validation_selection.py --path scripts/test-select-validation.py` | existing/configured | implement | M2 | code-review M2 | Block if affected validation paths are missing or the retired check remains selected. | Not applicable; deterministic selector. | `evidence/implementation-m2.md` | Read-only selection; executes no selected command. |
| CMD09 | `python -m py_compile scripts/boundary_first_validation.py scripts/validate-boundary-first.py scripts/validation_selection.py` | existing/configured | implement | M2 | code-review M2 | Block syntax-invalid retained modules. | Not applicable; compilation check. | `evidence/implementation-m2.md` | Writes interpreter cache only; no repository or external mutation. |
| CMD10 | `python scripts/prepare-release.py v0.4.0` | release-owned | release preparation | M3 | code-review M3 | Block incomplete or inconsistent profile-owned release surfaces. | Not applicable; release preparation command. | `evidence/implementation-m3.md` | Writes only reviewed profile-owned local surfaces; no tag, push, registry, or publication. |
| CMD11 | `python scripts/prepare-release.py v0.4.0 --check` | release-owned | release preparation | M3 | code-review M3 | Block non-idempotent or stale prepared output. | Not applicable; deterministic check. | `evidence/implementation-m3.md` | Read-only comparison; no publication. |
| CMD12 | `python scripts/release-preflight.py v0.4.0 --skip-remote` | release-owned | release preflight | M3, M4 | code-review M3 | Block profile, schema, or local release drift. | Not applicable; deterministic preflight. | `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | Explicitly skips remote checks and publication. |
| CMD13 | `python scripts/test-release-transaction.py` | existing/configured | implement | M3 | code-review M3 | Block routine preparation, recovery, closeout, or release-identity regression. | Zero tests is failure. | `evidence/implementation-m3.md` | Local fixtures and process stubs only. |
| CMD14 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | code-review M3 | Block archive, adapter metadata, workflow, rollback, or target parity regression. | Zero tests is failure. | `evidence/implementation-m3.md` | Temporary local archives only; no publication. |
| CMD15 | `python scripts/test-npm-package-publication.py` | existing/configured | implement | M3 | code-review M3 | Block package allowlist, packed binary, or real target-initialization smoke. | Zero tests is failure. | `evidence/implementation-m3.md` | Local `npm pack` and temporary installs only; no registry access or publish. |
| CMD16 | `python scripts/select-validation.py --mode release --release-version v0.4.0` | existing/configured | implement | M3 | code-review M3 | Block missing release-selected checks or retained custom check selection. | Not applicable; deterministic selector. | `evidence/implementation-m3.md` | Read-only selection; executes no selected command. |
| CMD17 | `bash scripts/ci.sh --mode release --release-version v0.4.0` | ci-owned | repository CI wrapper | M3, M4 | code-review M3 | Block on any selected release check, unclassified path, or broad-smoke failure. | A selected test command reporting zero tests is failure. | `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | Local selected commands only; no tag, push, registry write, or publication. |
| CMD18 | `bash scripts/release-verify.sh v0.4.0` | release-owned | standing full release gate | M3, M4 | code-review M3 | Block generated drift, archive/package integrity, adapter metadata, packed smoke, notes, rollback, or security failure. | Any delegated test suite reporting zero tests is failure. | `evidence/implementation-m3.md`; `evidence/implementation-m4.md` | Full local gate with temporary archives and package; no tag, push, registry write, or publication. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1, T2, T3, T4, T5 | none | CMD01, CMD02, CMD03, CMD04, CMD05 | `docs/changes/2026-08-06-usability-first-boundary-release/evidence/implementation-m1.md` | code-review M1 | Proves automatic concise behavior, stage ownership, normalized records, and all ten governed skill/resource surfaces. |
| M2 | T6, T7, T8, T9, T10, T11, T12, T22, T23 | none | CMD05, CMD06, CMD07, CMD08, CMD09 | `docs/changes/2026-08-06-usability-first-boundary-release/evidence/implementation-m2.md` | code-review M2 | Proves checked-revision snapshots, one-time derivation, proof-map mutation handling, privacy, exact custom retirement, compatibility, and rollback. |
| M3 | T13, T14, T15, T16, T18, T19, T20, T21, T22 | none | CMD10, CMD11, CMD12, CMD13, CMD14, CMD15, CMD16, CMD17, CMD18 | `docs/changes/2026-08-06-usability-first-boundary-release/evidence/implementation-m3.md` | code-review M3 and pending-baseline selection | Executes both release gates while activation remains pending; selector output alone is not closeout evidence. |
| M4 | T7, T9, T12, T14, T17, T18, T19, T20, T21, T22 | none | CMD05, CMD06, CMD12, CMD17, CMD18 | `docs/changes/2026-08-06-usability-first-boundary-release/evidence/implementation-m4.md` | code-review M4 | Repeats release proof only after the active snapshot changes the checked state and stops before external publication. |

## Test cases

### T1. Representative journeys apply boundary coverage automatically

- Covers: UBR-R001, UBR-R002, UBR-R018, E1, E2, E3, AC-UBR-001, AC-UBR-002, AC-UBR-011, EC2
- Level: integration
- Command IDs: CMD01, CMD02
- Fixture/setup: Semantic specification, loader-inspection, and custom-cleanup code-review journeys with required inclusion and exclusion outcomes.
- Steps: Invoke the owning skill behavior without naming the method; inspect semantic outcomes and forbidden expansions.
- Expected result: Each journey covers its material stage-owned boundaries once and omits unrelated release, provider, or history scenarios.
- Failure proves: Automatic coverage is missing, superficial, exhaustive, or prompt-keyword dependent.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: `scripts/test-skill-validator.py`; `scripts/test-boundary-first-reference.py`; `scripts/fixtures/boundary-first/semantic/`
- Required by milestone: M1

### T2. Concise default omits unowned scenarios

- Covers: UBR-R002, UBR-R018, AC-UBR-011, EC1
- Level: integration
- Command IDs: CMD01, CMD02
- Fixture/setup: Ordinary behavior task plus wording-only and no-admitted-boundary tasks.
- Steps: Evaluate semantic decisions; perturb fixtures with irrelevant dimensions, fixed bullet counts, exact prose, word counts, and method-name requirements.
- Expected result: Material outcomes remain covered; irrelevant expansions and brittle presentation assertions are rejected as proof.
- Failure proves: Concision either omits correctness or becomes a fixed scenario/prose checker.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: `scripts/test-skill-validator.py`; semantic fixtures
- Required by milestone: M1

### T3. Deeper analysis expands only justified risk

- Covers: UBR-R003, UBR-R018, AC-UBR-011, EC3
- Level: integration
- Command IDs: CMD01
- Fixture/setup: Three paired journeys triggered by a governing contract, one material risk, or an explicit deeper-analysis request.
- Steps: Compare concise and deeper outcomes while holding unrelated dimensions constant.
- Expected result: The justified partition or interaction expands, while unrelated scope remains unchanged.
- Failure proves: Deeper analysis is ignored or turns into an exhaustive matrix.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: `scripts/test-skill-validator.py`; semantic fixtures
- Required by milestone: M1

### T4. Stage and artifact ownership remain distinct

- Covers: UBR-R004, UBR-R005, INT-001, AC-UBR-003, EC2
- Level: integration
- Command IDs: CMD01, CMD02
- Fixture/setup: Formal spec and test-spec records plus informal inspection, plan, implementation, and review outcomes.
- Steps: Exercise every governed skill family and attempt cross-stage artifact creation or settlement.
- Expected result: Formal owners retain normalized records; each downstream stage consumes approved IDs; informal work creates no separate boundary artifact.
- Failure proves: Automatic guidance erases lifecycle authority or over-formalizes ordinary work.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: `scripts/test-skill-validator.py`; `scripts/test-boundary-first-reference.py`
- Required by milestone: M1

### T5. Ten skills and generated resources remain coherent

- Covers: UBR-R001, UBR-R005, UBR-R010, BND-COMPOSE-001, AC-UBR-005, EC5
- Level: e2e
- Command IDs: CMD01, CMD02, CMD03, CMD04, CMD05
- Fixture/setup: Canonical shared block, ten governed skills, mapped resources, and generated Codex output.
- Steps: Compare exact governed inventories and resource identities; remove or stale each representative layer.
- Expected result: The complete set passes; missing, additional, stale, or divergent skill/resource layers fail closed.
- Failure proves: A supported consumer can receive different automatic guidance.
- Evidence artifact: `evidence/implementation-m1.md`
- Automation location: Skill, resource projection, build, and activation tests
- Required by milestone: M1

### T6. Pending snapshot has one exact tuple

- Covers: UBR-R006, E1, BND-STATE-001
- Level: unit
- Command IDs: CMD06
- Fixture/setup: Pending activation fixtures with exact, missing, additional, malformed, unknown, and mixed field variants.
- Steps: Validate each record and mutate release, rollback, baseline, inventory, state, and unknown fields independently.
- Expected result: Only `pending` with three `-` values and an empty inventory passes.
- Failure proves: Pending state is ambiguous or fail-open.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-first-validation.py`; `scripts/fixtures/boundary-first/activation/`
- Required by milestone: M2

### T7. Active snapshot and one-time derivation are exact

- Covers: UBR-R006, UBR-R007, AC-UBR-004, BND-STATE-001
- Level: integration
- Command IDs: CMD06
- Fixture/setup: Temporary Git object fixtures with valid, invalid, unavailable, malformed, and unreadable full baseline revisions and eligible historical specs.
- Steps: Call `derive_grandfathered_specs(root, baseline_revision)` directly; compare raw-byte-sorted output; prove no writes; populate the active tuple once.
- Expected result: A valid exact revision returns the complete sorted tuple and no issues; failure returns no inventory and bounded issues; the function writes nothing and has no public CLI.
- Failure proves: Activation authoring is non-deterministic, mutating, or dependent on an invented command.
- Evidence artifact: `evidence/implementation-m2.md`; `evidence/implementation-m4.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M2 and M4

### T8. Checked-revision validation fails every divergent layer

- Covers: UBR-R007, AC-UBR-001, AC-UBR-005, E2
- Level: integration
- Command IDs: CMD05, CMD06
- Fixture/setup: Active fixtures with missing, additional, stale, malformed, mixed, unknown, or divergent canonical references, manifest resources, skill inventory, projections, adapters, versions, inventory, and rollback metadata.
- Steps: Mutate one layer at a time and run focused validation.
- Expected result: Every divergence fails with the affected repository-relative surface and corrective action.
- Failure proves: Current-file coherence can pass with a stale or substituted component.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M2

### T9. Active local validation requires no public or historical authority

- Covers: UBR-R007, UBR-R008, INT-002, AC-UBR-002, AC-UBR-004, E4, EC6
- Level: integration
- Command IDs: CMD05, CMD06
- Fixture/setup: Active checked tree with absent tag, no remote, no network, unavailable baseline, and missing repository history.
- Steps: Run normal `--check`; instrument Git-history, tag, remote, network, and derivation seams to fail if called.
- Expected result: Validation passes from current files and frozen inventory, reports active release intent, and makes no tagged or public claim.
- Failure proves: Local activation still depends on removed authority or overclaims publication.
- Evidence artifact: `evidence/implementation-m2.md`; `evidence/implementation-m4.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M2 and M4

### T10. Activation diagnostics are bounded and private

- Covers: UBR-R008, UBR-R017, BND-ENV-001
- Level: integration
- Command IDs: CMD05, CMD06
- Fixture/setup: Success and failure fixtures containing credentials, OTPs, private environment values, usernames, hostnames, and temporary absolute paths.
- Steps: Capture structured and human diagnostics for pending, active, and divergent records.
- Expected result: Output names snapshot, release intent, repository-relative surface, and corrective action without private values or public-release claims.
- Failure proves: Local proof leaks private state or misrepresents availability.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M2

### T11. Exact custom experiment retirement preserves ordinary paths

- Covers: UBR-R012, UBR-R013, BND-COMPOSE-001, BND-COMPAT-001, INT-003, AC-UBR-002, AC-UBR-007, AC-UBR-008, E3, EC9, EC10
- Level: integration
- Command IDs: CMD06, CMD07, CMD08
- Fixture/setup: Closed eight-surface retirement inventory, selector catalog, focused validator, ordinary changed-spec paths, and release-mode selection.
- Steps: Assert three deleted files are absent; mutate five retained surfaces with each retired behavior; inspect ordinary and release selection.
- Expected result: Retired behavior is absent and unselectable; focused checked-revision validation and routine release selection remain.
- Failure proves: Cleanup is incomplete or accidentally removes the original release mechanism.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-first-validation.py`; `scripts/test-select-validation.py`
- Required by milestone: M2

### T12. Historical compatibility and exact rollback remain authoritative

- Covers: UBR-R015, UBR-R019, BND-COMPAT-001, BND-RECOVERY-001, AC-UBR-009
- Level: integration
- Command IDs: CMD05, CMD06
- Fixture/setup: Frozen active inventory, historical accepted specs, new and substantively revised specs, and exact `v0.3.6` three-adapter metadata.
- Steps: Validate exemptions, prospective adoption, added historical paths, incomplete adapters, wrong versions, and rollback selection.
- Expected result: Frozen historical paths remain valid; new substantive behavior adopts the normalized record; only complete exact `v0.3.6` rollback passes.
- Failure proves: Activation rewrites history, expands exemption authority, or weakens rollback.
- Evidence artifact: `evidence/implementation-m2.md`; `evidence/implementation-m4.md`
- Automation location: `scripts/test-boundary-first-validation.py`; adapter fixtures
- Required by milestone: M2 and M4

### T13. Routine profile owns one v0.4.0 release identity

- Covers: UBR-R009, UBR-R020, BND-AUTH-001, AC-UBR-006
- Level: integration
- Command IDs: CMD10, CMD11, CMD12, CMD13
- Fixture/setup: `v0.4.0` profile, package metadata, notes, pending evidence, and mutation fixtures for version, dist-tag, source commit, and tag.
- Steps: Prepare and check release surfaces; mutate each identity and validate.
- Expected result: Only `v0.4.0`, `0.4.0`, `latest`, and the exact reviewed source identity agree; mixed values fail.
- Failure proves: A release can be prepared from conflicting identity authorities.
- Evidence artifact: `evidence/implementation-m3.md`
- Automation location: `scripts/test-release-transaction.py`; release validation fixtures
- Required by milestone: M3

### T14. Three-target resources match through packed installation

- Covers: UBR-R010, BND-COMPOSE-001, AC-UBR-005, AC-UBR-006, EC5
- Level: e2e
- Command IDs: CMD14, CMD15, CMD18
- Fixture/setup: Canonical skills, generated Codex/Claude/opencode packages, adapter archives, npm tarball, and clean temporary target directories.
- Steps: Generate, archive, pack, install, and compare mapped resource identities; perturb every layer independently.
- Expected result: All layers agree exactly and initialize all three targets; the first missing, additional, stale, or divergent layer fails.
- Failure proves: Published consumers can receive different behavior from reviewed canonical sources.
- Evidence artifact: `evidence/implementation-m3.md`; `evidence/implementation-m4.md`
- Automation location: `scripts/test-adapter-distribution.py`; `scripts/test-npm-package-publication.py`; full release gate
- Required by milestone: M3 and M4

### T15. Routine release steps and full-gate categories remain intact

- Covers: UBR-R011, UBR-R012, INT-003, AC-UBR-007, E5, EC10
- Level: integration
- Command IDs: CMD12, CMD13, CMD14, CMD15, CMD18
- Fixture/setup: Release scripts, trusted workflow, closeout command, and category-level success/failure fixtures.
- Steps: Inspect and exercise preparation, preflight, full verification, trusted publication wiring, registry/asset validation, public smoke declarations, and rerunnable closeout.
- Expected result: Every standing category remains owned and effective; checked activation neither invokes nor bypasses it.
- Failure proves: Simplification weakened or replaced the standard release mechanism.
- Evidence artifact: `evidence/implementation-m3.md`
- Automation location: Release transaction, adapter distribution, npm package, workflow static, and release-gate tests
- Required by milestone: M3

### T16. Pending baseline executes both release gates

- Covers: UBR-R010, UBR-R011, INT-003, AC-UBR-006, AC-UBR-007, E5
- Level: smoke
- Command IDs: CMD10, CMD11, CMD12, CMD13, CMD14, CMD15, CMD16, CMD17, CMD18
- Fixture/setup: Complete M3 `v0.4.0` payload with activation still pending.
- Steps: Prepare and preflight; inspect selector output; execute release-mode CI; execute the standing full gate; record the reviewed pending revision only after all pass.
- Expected result: Both executable gates independently prove the pending package; selector output alone is never accepted as closeout evidence.
- Failure proves: M4 could freeze an incompletely proved pending baseline.
- Evidence artifact: `evidence/implementation-m3.md`
- Automation location: M3 validation commands
- Required by milestone: M3

### T17. Active state reruns integrated release proof

- Covers: UBR-R010, UBR-R011, BND-STATE-001, BND-COMPOSE-001, AC-UBR-004, EC6
- Level: smoke
- Command IDs: CMD05, CMD06, CMD12, CMD17, CMD18
- Fixture/setup: Active record derived from the exact closed M3 pending revision, with coherent current resources and packages.
- Steps: Validate the active snapshot, preflight, execute release-mode CI, and execute the full gate again after the state change.
- Expected result: Active checked-revision and full package proof pass together without requiring a tag or public evidence.
- Failure proves: M3 proof was incorrectly reused after activation changed the checked state.
- Evidence artifact: `evidence/implementation-m4.md`
- Automation location: M4 validation commands
- Required by milestone: M4

### T18. Exact immutable tag identity fails closed

- Covers: UBR-R020, BND-AUTH-001, BND-TEMPORAL-001, INT-002, EC7
- Level: integration
- Command IDs: CMD13, CMD17, CMD18
- Fixture/setup: Exact, missing, rewritten, mismatched, incomplete, and mixed-version tag/source fixtures.
- Steps: Run local release identity validation and trusted workflow contract checks for each fixture.
- Expected result: Only the immutable tag pointing to the exact reviewed release commit can support publication; every mismatch fails.
- Failure proves: A different source revision can be published or reported as `v0.4.0`.
- Evidence artifact: `evidence/implementation-m3.md`; `evidence/implementation-m4.md`
- Automation location: Release transaction and release validation tests
- Required by milestone: M3 and M4

### T19. Recovery preserves immutable releases by phase

- Covers: UBR-R015, UBR-R016, BND-TEMPORAL-001, BND-RECOVERY-001, INT-003, AC-UBR-009, E6, EC8
- Level: integration
- Command IDs: CMD06, CMD13, CMD14, CMD18
- Fixture/setup: Pre-tag validation failure, unavailable publication, partial GitHub/npm states, delayed public evidence, rollback, and later-patch fixtures.
- Steps: Fail each phase; rerun closeout; attempt rewrite; exercise dist-tag correction/deprecation and patch-only recovery where applicable.
- Expected result: Pre-tag failure leaves public state unchanged; partial publication stays open and phase-recorded; immutable versions are never rewritten.
- Failure proves: Recovery can conceal partial state or mutate a published identity.
- Evidence artifact: `evidence/implementation-m3.md`; `evidence/implementation-m4.md`
- Automation location: `scripts/test-release-transaction.py`; adapter/release fixtures
- Required by milestone: M3 and M4

### T20. Trusted publication and public closeout remain the only public authority

- Covers: UBR-R012, UBR-R020, BND-AUTH-001, INT-002, INT-003, AC-UBR-007, EC8, EC10
- Level: integration
- Command IDs: CMD13, CMD14, CMD18
- Fixture/setup: Trusted tag workflow, GitHub asset and npm registry fixtures, all-three-target public `npx` declarations, and unavailable-evidence closeout fixture.
- Steps: Inspect workflow-to-full-gate wiring and closeout checks; omit each public evidence class and introduce custom-path references.
- Expected result: Only the routine trusted path can advance public claims; incomplete evidence leaves closeout open; custom paths fail.
- Failure proves: Local activation or a retired helper can establish public availability.
- Evidence artifact: `evidence/implementation-m3.md`; `evidence/implementation-m4.md`
- Automation location: `scripts/test-release-transaction.py`; `scripts/test-adapter-distribution.py`; workflow static tests
- Required by milestone: M3 and M4

### T21. Lifecycle execution has no external mutation authority

- Covers: UBR-R014, BND-STATE-001, BND-ENV-001, INT-002, AC-UBR-010
- Level: integration
- Command IDs: CMD10, CMD12, CMD13, CMD17, CMD18
- Fixture/setup: Process and network stubs around authoring, implementation, validation, and verification command families.
- Steps: Run safe fixture modes and fail on tag creation, push, publication, merge, registry write, public-success text, or undeclared network access.
- Expected result: Lifecycle work changes only approved local surfaces and stops before external publication.
- Failure proves: A pre-public stage can mutate or overclaim external state.
- Evidence artifact: `evidence/implementation-m3.md`; `evidence/implementation-m4.md`
- Automation location: Release transaction and release-gate safety tests
- Required by milestone: M3 and M4

### T22. Release evidence suppresses secrets and machine-local data

- Covers: UBR-R017, BND-ENV-001
- Level: integration
- Command IDs: CMD06, CMD13, CMD14, CMD15, CMD18
- Fixture/setup: Failure outputs and evidence inputs seeded with credentials, tokens, OTPs, private environment values, usernames, hostnames, and temporary absolute paths.
- Steps: Exercise validation, archive, package, pre-public, and closeout failure paths; scan committed and generated evidence.
- Expected result: Only bounded public facts and repository-relative identities remain; every private sentinel is absent.
- Failure proves: Local or release proof can disclose sensitive environment state.
- Evidence artifact: Owning milestone evidence
- Automation location: Boundary, release transaction, adapter, npm, and release-gate security tests
- Required by milestone: M2, M3, and M4

### T23. Proof-map structure fails closed without inventing semantics

- Covers: UBR-R005, AC-UBR-003, AC-UBR-012, EC4
- Level: integration
- Command IDs: CMD06
- Fixture/setup: This normalized proof map plus mutations removing requirements, boundaries, interactions, commands, milestones, coverage fields, and non-applicability rationales.
- Steps: Validate the complete record; apply one structural mutation at a time; retain a structurally valid semantic-omission fixture.
- Expected result: Unknown or incomplete structure fails closed; semantic adequacy remains review-owned and is not inferred by the validator.
- Failure proves: Implementation can rely on an incomplete proof map or deterministic tooling can invent coverage.
- Evidence artifact: `evidence/implementation-m2.md`
- Automation location: `scripts/test-boundary-first-validation.py`
- Required by milestone: M2

## Fixtures and data

- `scripts/fixtures/boundary-first/semantic/`: representative E1-E3 concise and deeper-analysis journey fixtures, authored or revised in M1.
- `scripts/fixtures/boundary-first/activation/`: pending, active, divergent, no-history, privacy, derivation, compatibility, and rollback fixtures, authored or revised in M2 and M4.
- Temporary Git repositories for exact full-revision derivation; they contain no network remote and are removed after each test.
- Existing release transaction, adapter distribution, npm package, and release-validation fixture helpers extended with `v0.4.0` identities in M3.
- Temporary Codex, Claude, and opencode generated, archived, packed, and installed trees created under test-owned temporary directories and always cleaned up.
- Exact `v0.3.6` tracked metadata remains immutable input; tests copy it before mutation and never rewrite the source fixture.
- Closed-vocabulary mutations use `unknown_value` or `not_in_vocabulary` in test names.

Every expected path is repository-relative.
No fixture reads user installation state, credentials, live registries, or public network services.

## Mocking/stubbing policy

Use filesystem, subprocess, Git-object, network, and publication-boundary doubles only for interruption, unavailable history, absent remotes, tag/push/publish containment, public-evidence delay, and privacy sentinels.
Do not mock activation parsing, inventory sorting, resource projection, selector composition, archive contents, package allowlists, packed target initialization, release-profile resolution, or rollback metadata in their final proof.
Do not mock `validate-boundary-first.py`, `ci.sh --mode release`, or `release-verify.sh` in M3 and M4 milestone closeout.
No test may access a live registry, GitHub API, user secret store, or user installation.

## Migration or compatibility tests

T11 and T12 prove exact custom-experiment retirement, historical accepted-spec exemptions, prospective normalized adoption, and immutable `v0.3.6` rollback.
T18 and T19 prove immutable `v0.4.0` identity and phase-specific fix-forward recovery.
Historical source artifacts are copied into temporary fixtures before mutation and never rewritten.

## Observability verification

T8 through T10 require diagnostics to identify the snapshot, release intent, affected repository-relative surface, and corrective action.
T13 through T20 require release evidence to identify the version tuple, source identity, target parity, validation phase, rollback release, and open or closed public-evidence state.
Tests assert stable semantic fields and categories, not exact prose or line ordering.
No metrics or distributed traces are introduced.

## Security/privacy verification

T10, T21, and T22 prove network and publication containment plus suppression of credentials, tokens, OTPs, private environment values, usernames, hostnames, and machine-local temporary paths.
Archive and npm package tests retain forbidden-path and secret-scanning checks.
No test requires credentials or writes to GitHub, npm, Git remotes, or public release state.

## Performance checks

M1 semantic tests reject a separate boundary stage or unconditional exhaustive matrix.
M2 proves normal checked-revision validation does not call Git history, tag, remote, network, derivation, release, or public-smoke paths.
M3 runs focused preparation and preflight before expensive release-mode CI and the full gate.
M4 reruns the expensive gates because activation changes the checked state; no third full-gate execution is required by this test spec.
Existing release timing evidence remains profile-owned; this change adds no new numeric performance threshold.

## Manual QA checklist

Not applicable before implementation handoff.
All approved local outcomes are automatable through repository fixtures and safe command modes.
Actual tagging, publication, registry checks, and public `npx` smoke remain explicit post-merge maintainer operations governed by the routine release contract, not manual proof for this lifecycle test spec.

## What not to test and why

- Do not assert exact skill prose, word counts, bullet counts, or method-name output; UBR-R018 requires semantic journeys.
- Do not enumerate all eight dimensions for tasks with no admitted outcome; UBR-R002 requires material, owner-scoped selection.
- Do not create a runtime checker, new activation CLI, writer, candidate protocol, custom publisher, or second release mode; all are non-goals.
- Do not require Git history, tag existence, remote state, or network during normal activation validation.
- Do not publish, tag, push, merge, call live registries, or claim public availability during lifecycle execution.
- Do not migrate historical accepted specs or mutate immutable `v0.3.6`/`v0.4.0` release evidence.
- Do not treat selector output, preflight, structural validation, or M3 proof as a substitute for its distinct owning gate.

## Uncovered gaps

None.

## Next artifacts

- Test-spec review.
- M1 through M4 implementation and code-review loops after approval.
- Explain-change, verify, and PR handoff after all milestone proof closes.
- Explicit post-merge routine publication and public closeout under maintainer authority.

## Follow-on artifacts

None yet.

## Readiness

Ready for `test-spec-review` after authoring validation.
Implementation remains blocked until this proof map has an approved, current formal review.
