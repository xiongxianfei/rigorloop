# Release Transaction Automation and Evidence Generation

## Status

accepted

## Problem

RigorLoop releases cost too much human time because a release is currently handled as a coordinated checklist of hand-edited surfaces instead of a typed transaction.

The `v0.3.4` release retrospective separated the cost into three layers:

1. Required cost: public supply-chain release work, external GitHub/npm availability, and public smoke.
2. Structural avoidable cost: release-state duplication across Python, shell, JSON, Markdown, package metadata, tests, and evidence files.
3. Execution avoidable cost: expensive validators discover missing version registrations and evidence-shape mismatches late, causing fix-and-rerun loops.

The strongest avoidable root cause is not a single slow test. Routine release state is duplicated across many manually edited locations instead of generated from one release profile source of truth.

The release process currently requires manual coordination of surfaces such as:

- npm package version
- package README examples
- bundled release metadata
- GitHub release archive URLs and checksums
- adapter archive metadata
- release validation allowlists
- target-native init release expectations
- CLI tests with exact version behavior
- `release.yaml`
- release notes
- npm publication evidence
- public `npx` smoke evidence

`v0.3.4` showed concrete rework from this model. Version-specific release data was scattered through Python constants, shell case lists, JS tests, package validation expectations, and Markdown evidence. Missed or stale surfaces caused validation failures and repeated release loops.

There was also a post-publication evidence-shape loop. The evidence draft used command strings and hash formats that the validator rejected, such as `npx -y` instead of the expected command shape and raw tree hashes without the required `sha256:<hex>` prefix. The validator was right to fail closed, but the process exposed schema requirements only after manual evidence was written incorrectly.

The release process is showing the same repeated anti-pattern seen elsewhere in the project: hand-listed subsets of a contract enumeration drift from the source contract. The proposed fix is source-derived enumeration, generated downstream surfaces, and a fail-closed audit for hardcoded literals that should be derived.

## Goals

- Reduce human time and rework for routine public releases.
- Preserve the full public supply-chain safety gate.
- Create a single release profile source of truth.
- Generate routine release-prep artifacts from that profile.
- Generate validator-compatible pending and published evidence.
- Add cheap release preflight before expensive release verification.
- Make local and CI release gates use the same release verification command set.
- Detect stale current-version literals and release-profile drift before broad release validation.
- Capture per-release timing evidence.
- Separate required publication wait time from avoidable human-attention cost.
- Keep full `release-verify` as the authoritative confirmation gate.
- Avoid weakening GitHub release, npm trusted publication, archive integrity, adapter metadata, or public `npx` smoke requirements.

## Non-goals

- Do not weaken the full release gate.
- Do not remove GitHub release asset validation.
- Do not remove npm publication validation.
- Do not remove public `npx` smoke.
- Do not skip archive SHA, tree hash, file count, or adapter metadata validation.
- Do not treat external publication wait time as waste.
- Do not make release publication asynchronous without explicit workflow support.
- Do not introduce remote or shared caches in the first slice.
- Do not optimize by deleting evidence fields.
- Do not replace `release-verify.sh` with an unreviewed parallel implementation.
- Do not make every historical release conform retroactively.
- Do not require live registry proof before publication.
- Do not hand-edit generated release metadata after generator adoption except through explicit override rules.
- Do not use parallelism to mask release-state drift.

## Vision fit

fits the current vision

RigorLoop's release process is part of the project's supply-chain trust boundary. This proposal improves release reliability by making release state explicit, generated, reviewable, and traceable while preserving durable evidence and the existing safety gate.

The proposal is falsified if a release can publish with missing archive, npm, or public-smoke evidence; generated evidence is accepted without matching validator schema; local and CI release gates diverge; runtime improves only by removing checks; or routine releases still require hand-editing many version-specific constants.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Understand release-time root cause | in scope | Problem, Context |
| Reduce release time | in scope | Goals, Recommended Direction |
| Preserve release safety | in scope | Non-goals, Recommended Direction |
| Automate duplicated version state | in scope | Release profile, Expected Behavior Changes |
| Avoid evidence-shape loops | in scope | Schema-first evidence generation |
| Keep public smoke | in scope | Non-goals, Testing and Verification Strategy |
| Reduce expensive reruns | in scope | Release preflight |
| Consider parallelism | deferred follow-up | Scope budget, Next Artifacts |
| Rewrite historical releases | out of scope | Non-goals |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Release profile source of truth | core to this proposal | Eliminates scattered version state. |
| Current-version literal audit | core to this proposal | Identifies and prevents hand-edited version drift. |
| `prepare-release.py <tag>` | first-slice candidate | Generates routine pre-publication surfaces. |
| Pending evidence generation | core to this proposal | Avoids schema mismatch before publication. |
| Published evidence generation | core to this proposal | Avoids post-publication field-shape loops. |
| Release preflight | core to this proposal | Fails cheap issues before the broad release gate. |
| Local/CI gate alignment | same-slice dependency | Prevents local and hosted release gate skew. |
| Release timing capture | first-slice candidate | Provides data before parallelism decisions. |
| Release-gate parallelism | deferable follow-up | Useful only after drift is reduced and timings exist. |
| Full release-tooling rewrite | out of scope | First slice should target routine version drift and evidence generation. |
| Historical release migration | separate proposal | Different compatibility risk. |
| Background publication monitor | deferable follow-up | Useful after closeout automation exists. |
| Routine release automation | core to this proposal | Defines the supported first-slice release boundary. |
| Special release automation | deferable follow-up | One-off, emergency, schema-migration, and new-channel releases need explicit owner decisions first. |

## Context

The release retrospective identified that some release time is irreducible. GitHub release assets and npm registry metadata must exist before public smoke can prove them. The `v0.3.4` GitHub Actions release and npm trusted-publishing jobs each took roughly a minute.

The avoidable time came from release-state drift and late evidence-shape discovery. The release prep commit touched release docs, package metadata, package tests, adapter metadata, release validation scripts, and package validation scripts. The post-publication closeout required another evidence commit after npm and GitHub surfaces became public.

The deeper recommendation is to treat a release as a typed transaction object. Hand-edited surfaces in a routine release are themselves the defect class.

The release profile should define the version, package identity, adapter artifacts, required evidence, publication surfaces, smoke requirements, and validator expectations. Routine release files should be generated or checked from that profile, not hand-synchronized by memory.

## Options considered

### Option 1: Do nothing

Pros:

- No tooling risk.
- Current release process remains explicit and fail-closed.

Cons:

- Manual version-state drift continues.
- Expensive release gates keep discovering cheap errors late.
- Post-publication evidence remains edit-heavy.
- Human time remains high.

Rejected because it preserves the root cause.

### Option 2: Parallelize the release gate first

Pros:

- Could reduce wall-clock time of the successful full gate.
- Existing test suites may have independent portions.

Cons:

- Does not solve release-state drift.
- Does not solve evidence-shape mismatches.
- Can hide, but not remove, release checklist complexity.
- Requires timing data and parallel-safety proof.

Deferred because parallelism should follow drift reduction and timing capture.

### Option 3: Add only release preflight

Pros:

- Cheap and useful.
- Prevents some obvious failures before full verification.

Cons:

- Still requires hand-editing many version-specific surfaces.
- Does not generate pending or published evidence.
- Does not remove the root duplication.

Useful but incomplete.

### Option 4: Add evidence templates only

Pros:

- Directly addresses post-publication evidence shape errors.
- Smaller than full release automation.

Cons:

- Does not address release-version allowlist drift.
- Does not generate package metadata or test expectations.
- Does not define the release transaction source of truth.

Useful but incomplete.

### Option 5: Release profile, generators, preflight, and timing

Pros:

- Addresses the main root cause.
- Preserves full release verification.
- Makes drift visible before expensive gates.
- Converts release evidence into schema-first generated artifacts.
- Produces timing data for later parallelism.

Cons:

- Touches release tooling, tests, metadata generation, and docs.
- Requires careful source-of-truth boundaries.

Recommended.

## Recommended direction

Choose Option 5.

Build the release process around a typed release profile:

```text
release profile:
  owns release version, package version, required evidence classes, adapter
  artifact expectations, target support, publication requirements, and smoke
  requirements.

prepare-release:
  generates routine pre-publication surfaces from the profile.

release-preflight:
  fails cheap drift before broad release verification.

release-verify:
  remains the authoritative local full release gate.

publish workflow:
  invokes the same full release gate as local.

close-release-publication:
  collects public GitHub/npm/npx evidence and writes validator-compatible
  published evidence.
```

The first slice should focus on routine releases with the current package and adapter targets. Special releases can still use explicit owner decisions until the generated path supports them.

## Release profile

The release profile is a durable release evidence artifact and lives at:

```text
docs/releases/profiles/<tag>.yaml
```

The profile is the source of truth for routine release version state, publication requirements, target set, required evidence classes, and generated release-prep surfaces. Release tooling may read the profile, but scripts are not the source of truth for routine release state.

The profile should represent the routine release transaction, including:

```yaml
schema_version: release-profile-v1
release_tag: v0.3.5
package_version: 0.3.5
npm_package: "@xiongxianfei/rigorloop"

targets:
  - codex
  - claude
  - opencode

adapter_artifacts:
  required: true
  metadata_file: adapter-artifacts-v0.3.5.json
  archive_version: v0.3.5

publication:
  github_release_required: true
  npm_publication_required: true
  trusted_publishing_required: true
  public_smoke_required: true

evidence:
  release_yaml: required
  release_notes: required
  npm_publication: required
  public_target_init_smoke: required
  archive_hashes: required
  tree_hashes: required
  file_counts: required
  timing: required

validation:
  local_release_verify_required: true
  ci_release_verify_required: true
  security_scanning_required: true
```

The exact schema belongs in the spec. The important proposal decision is that routine release surfaces derive from one profile.

## Routine and special release boundary

The first slice targets routine releases.

A routine release keeps the same npm package, the same supported target set (`codex`, `claude`, and `opencode`), the same publication channels, and the same release evidence schema. It does not introduce a new adapter class, emergency/security exception, release-schema migration, or historical evidence rewrite.

A special release is any release outside that boundary. Special releases should require an explicit owner decision and may use manual or extended release steps until the generated path supports that release class.

## Generated-surface ownership

Release surfaces are classified into three ownership groups:

| Surface class | Examples | Rule |
|---|---|---|
| Profile-owned generated | release metadata pointers, adapter artifact expectations, pending npm-publication skeleton, target smoke rows, current-version fixture data | Generated from the profile; manual changes need explicit, review-visible override handling. |
| Human-authored but profile-checked | release notes narrative, migration notes, risk notes | Human-authored; validators check required headings, required fields, and profile consistency. |
| Historical immutable | prior release evidence, prior profile snapshots, historical fixtures | Not rewritten by routine release prep. |

`prepare-release.py` may update profile-owned generated surfaces. It should not overwrite human-authored narrative content except inside explicitly marked generated regions. It should not rewrite historical release evidence.

Manual overrides to generated surfaces should be explicit, review-visible, and checked by release preflight.

## Version-literal audit

Add a release preflight check that finds hardcoded current-version literals outside approved generated surfaces or historical fixtures.

The current release tag or version should appear only in the active release profile, generated release surfaces, approved historical fixtures, current generated package metadata, and validator-approved expected outputs.

First-slice behavior:

- new or changed unauthorized current-version literal: fail;
- existing baseline unauthorized literal: report-only until the baseline is clean or explicitly classified;
- historical fixture literal: allowed only when classified as historical;
- generated current literal: allowed only when derived from the active release profile.

Diagnostics should include:

- literal
- file
- classification
- expected owner

Example diagnostic:

```text
release literal drift: v0.3.5 appears in scripts/adapter_distribution.py outside generated release-profile output
```

The first slice should record a release-literal audit baseline in change-local evidence so existing debt is visible without blocking all release-tooling adoption.

## Schema-first evidence generation

Pending evidence should be generated from validator-compatible templates:

- `docs/releases/<tag>/release.yaml`
- `docs/releases/<tag>/release-notes.md`
- `docs/releases/<tag>/npm-publication.md`

`prepare-release.py` may update release fixture data and expected values derived from the profile. It should not generate or rewrite test logic. Stable tests should remain hand-authored and version-independent where practical.

Published evidence should be generated from public data after publication:

- GitHub release asset metadata
- npm registry metadata
- npm tarball integrity and SHA
- fresh public `npx` smoke for `version`, `init codex`, `init claude`, and `init opencode`
- tree hashes and file counts in validator-compatible form

The generator should emit command strings exactly as validators expect. The `npx -y` versus `npx` mismatch and raw-hash versus `sha256:<hex>` mismatch should not be possible in generated evidence.

## Release preflight

The release preflight should be fast and state/schema-oriented. A target of under 30 seconds on a typical maintainer machine is reasonable for the first slice.

The preferred command is:

```bash
python scripts/release-preflight.py v0.3.5
```

Python should own the preflight logic because profile parsing, evidence-shape validation, and literal-audit classification are structured checks. A thin shell wrapper can be added later if maintainers want ergonomic parity with `release-verify.sh`.

The preflight should check:

- release profile exists and is complete
- package version matches profile
- generated metadata pointer matches profile
- release files exist in pending state
- current-version literal audit passes
- local tag does not exist unless explicitly allowed
- remote tag does not exist when remote is available
- release notes skeleton exists
- npm-publication pending evidence validates shape
- validator vocabulary and enum values align
- release-output directory is clean or absent
- required secrets are not required for local preflight

Preflight should be idempotent and side-effect-light. It may read and validate release surfaces, but generation belongs to `prepare-release.py`. It should not create or modify release artifacts except for an explicitly requested timing or log artifact.

## Preflight/full-gate boundary

`release-preflight` owns cheap, deterministic local release-state checks:

- release profile completeness;
- package/profile version agreement;
- generated metadata pointer drift;
- unauthorized current-version literals;
- pending evidence shape;
- local tag conflicts;
- remote tag conflicts when remote state is reachable;
- release-output directory state.

`release-verify` remains authoritative for full generated output, archive integrity, adapter metadata, package contents, full validation, and checks whose inputs are created or materially changed during the full release gate.

Boundary rule:

```text
When release-verify fails on a cheap deterministic drift issue that preflight
could have detected under the same inputs, add a preflight regression.
```

This preserves the full gate while preventing repeated expensive failures for issues that a cheap profile/schema/state preflight can catch.

## Expected behavior changes

- Routine release prep is generated from a release profile.
- Current-version drift is detected before broad release verification.
- Pending evidence is validator-compatible before publication.
- Published evidence is generated from public GitHub/npm/npx data.
- Full release verification remains mandatory.
- Local and CI release gates use the same command set.
- Release timing is recorded.
- External wait remains, but human attention cost is reduced.
- Historical release files are not rewritten.
- Routine releases and special releases have an explicit boundary.
- `prepare-release.py` generates fixture data and expected values, not test logic.

## Architecture impact

| Surface | Impact |
|---|---|
| Release profile | New source-of-truth artifact for routine release state. |
| Release prep tooling | New generator for routine release-prep surfaces. |
| Release evidence tooling | New pending and published evidence generation. |
| Release preflight | New cheap fail-fast gate. |
| Release verification | Remains authoritative and should read or validate against the profile. |
| CI release workflow | Should call the same release command set as local verification. |
| Validator constants | Derived from the profile where practical. |
| Test fixtures | Separate current-version, historical-version, and version-independent cases. |
| Release docs | Generated or profile-backed where routine. |
| Publication evidence | Generated after public smoke. |
| Historical releases | No migration in this proposal. |

A separate architecture artifact is recommended only if the implementation introduces a reusable release-state generator framework beyond release tooling.

## Testing and verification strategy

Likely proof areas:

| Check ID | What is verified |
|---|---|
| `REL-001` | Release profile schema validates. |
| `REL-002` | `prepare-release.py` is idempotent. |
| `REL-003` | Package version matches profile. |
| `REL-004` | Bundled release metadata pointer matches profile. |
| `REL-005` | Adapter artifact metadata pointer matches profile. |
| `REL-006` | Current-version literal audit catches unauthorized hardcoded versions. |
| `REL-007` | Historical fixtures may retain historical versions. |
| `REL-008` | Pending evidence generated by `prepare-release.py` passes pre-publication validation. |
| `REL-009` | Published evidence generated by `close-release-publication.py` passes published validation. |
| `REL-010` | `npx` smoke command strings match validator expectations exactly. |
| `REL-011` | Tree hashes are written as `sha256:<hex>`. |
| `REL-012` | Missing release profile entry fails preflight. |
| `REL-013` | Local tag conflict fails preflight. |
| `REL-014` | Remote tag conflict fails preflight when remote is available. |
| `REL-015` | Full `release-verify.sh` remains required. |
| `REL-016` | CI release workflow invokes the same command set as local release verify. |
| `REL-017` | Timing evidence is recorded. |
| `REL-018` | Release-prep tooling does not publish. |
| `REL-019` | Closeout tooling does not pass until public evidence exists. |
| `REL-020` | Historical releases are not modified. |
| `REL-021` | Release profiles live at `docs/releases/profiles/<tag>.yaml`. |
| `REL-022` | Every release-prep surface is classified as generated, human-authored but profile-checked, or historical immutable. |
| `REL-023` | `prepare-release.py` generates fixture data and expected values, not test logic. |
| `REL-024` | `release-preflight` is implemented in Python, or the spec records an explicit exception. |
| `REL-025` | Unauthorized current-version literals fail for newly changed files. |
| `REL-026` | Existing unauthorized current-version literals are report-only until the baseline audit is clean or explicitly classified. |
| `REL-027` | `close-release-publication.py` is rerunnable and fails clearly when public evidence is unavailable. |
| `REL-028` | Timing evidence is required, but duration budgets are not hard failures in the first slice. |
| `REL-029` | Routine-release scope and special-release escape handling are defined. |

Behavior-preservation evidence should cover:

| Surface | Baseline | New proof | Result |
|---|---|---|---|
| Full release verification | `release-verify.sh <tag>` required | same command remains required | preserved |
| GitHub release evidence | manual and validator checked | generated and validator checked | strengthened |
| npm publication evidence | manual and validator checked | generated and validator checked | strengthened |
| Public `npx` smoke | required | still required | preserved |
| Adapter metadata | version-specific hand edits | profile-derived | strengthened |
| Current-version tests | hand-updated | profile-derived, generated, or audited | strengthened |
| Historical fixtures | stable | allowed as historical | preserved |
| Release timing | ad hoc | durable timing file | strengthened |
| External wait | required | unchanged, rerunnable closeout | preserved |

## Rollout and rollback

Rollout should proceed in reviewable stages:

1. Inventory release-state surfaces and add a report-only current-version literal audit.
2. Define the release profile schema and validation fixtures.
3. Add `prepare-release.py <tag>` for generated pending release artifacts.
4. Add fast release preflight.
5. Add `close-release-publication.py <tag>` for public evidence closeout.
6. Align local and CI release verification around the same command set and record timing.
7. Update workflow guidance and close with behavior-preservation evidence.

Rollback:

- Disable generators before removing generated surfaces.
- Preserve the last hand-authored release process until the generated process passes against a full fixture.
- Do not remove `release-verify.sh`.
- Keep version-literal audit in report-only mode if enforcement causes unexpected false positives.
- Preserve generated evidence templates if they remain validator-compatible.
- Do not rewrite published historical release evidence during rollback.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Release profile becomes another duplicated source | Generate downstream constants from it and audit unauthorized literals. |
| Generator emits invalid evidence | Generate from validator-compatible templates and test pending and published states. |
| Preflight duplicates full release verification | Keep preflight cheap and state/schema-oriented only. |
| CI/local skew persists | CI calls the same repository-owned release command set. |
| Historical versions are falsely flagged | Classify historical fixture surfaces explicitly. |
| Tooling hides release changes | Generated diffs remain reviewed and committed. |
| Public evidence unavailable immediately | Closeout command is rerunnable and reports pending external state. |
| Automation expands too far | Keep first slice to routine releases; special releases use explicit owner decisions. |
| Timing becomes flaky | Record timing as evidence first; do not enforce hard budgets immediately. |

## Open questions

No proposal-blocking open questions remain.

Spec authoring should still settle the exact `release-profile-v1` schema, generated-region markers, release-literal audit baseline format, and timing file schema.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-06-29 | Treat routine release as a typed transaction. | Hand-synchronized version state caused repeated release loops. | Continue release checklist by memory. |
| 2026-06-29 | Use release profile as source of truth. | Version-specific release state is duplicated across many surfaces. | Add more allowlists manually. |
| 2026-06-29 | Generate evidence from validator-compatible schemas. | `v0.3.4` failed on hand-written evidence shape. | Keep manual evidence drafting. |
| 2026-06-29 | Add cheap preflight before full verify. | Expensive validators discovered cheap drift late. | Always run full gate first. |
| 2026-06-29 | Defer parallelism until drift is reduced and timing exists. | Parallelism does not solve manual release-state drift. | Optimize raw runtime first. |
| 2026-06-29 | Store release profiles under `docs/releases/profiles/<tag>.yaml`. | The profile is durable release evidence and should live near release evidence. | Put routine release truth under implementation-only script directories. |
| 2026-06-29 | Classify generated, human-authored/profile-checked, and historical immutable release surfaces. | Prevents generators from being either too weak or too broad. | Leave generated-surface ownership implicit. |
| 2026-06-29 | Scope preflight to deterministic local/profile/schema drift under the same inputs. | Avoids impossible guarantees while preserving cheap failure detection. | Claim preflight can prevent every later release-verify failure. |

## Next artifacts

- implementation
- `code-review`
- `explain-change`
- `verify`
- `pr`

A dedicated spec is recommended because this changes release-state ownership, generator outputs, release evidence schemas, and release-gate sequencing.

## Follow-on artifacts

- Spec: `specs/release-transaction-automation.md`
- Spec-review: `docs/changes/2026-06-29-release-transaction-automation/reviews/spec-review-r1.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260629-release-transaction-profile.md`
- Architecture-review: `docs/changes/2026-06-29-release-transaction-automation/reviews/architecture-review-r1.md`
- Plan: `docs/plans/2026-06-29-release-transaction-automation.md`
- Plan-review: `docs/changes/2026-06-29-release-transaction-automation/reviews/plan-review-r1.md`
- Test spec: `specs/release-transaction-automation.test.md`
- Test-spec-review R1: `docs/changes/2026-06-29-release-transaction-automation/reviews/test-spec-review-r1.md`
- Test-spec-review R2: `docs/changes/2026-06-29-release-transaction-automation/reviews/test-spec-review-r2.md`
- Test-spec-review R3: `docs/changes/2026-06-29-release-transaction-automation/reviews/test-spec-review-r3.md`

## Readiness

Accepted after `proposal-review-r1`. Downstream spec, architecture, ADR, plan, plan-review, test spec, and clean test-spec-review are recorded. The active plan `Current Handoff Summary` owns the next workflow action.
