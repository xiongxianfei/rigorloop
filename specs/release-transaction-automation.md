# Release Transaction Automation and Evidence Generation

## Status

approved

## Related proposal

- Proposal: [Release Transaction Automation and Evidence Generation](../docs/proposals/2026-06-29-release-transaction-automation.md)
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-06-29-release-transaction-automation/reviews/proposal-review-r1.md)

## Goal and context

Routine RigorLoop releases should be executed as typed release transactions instead of hand-edited version checklists. The release transaction profile is the durable source of truth for routine release identity, target support, evidence classes, publication expectations, and generated release-prep surfaces.

The spec preserves the existing public release safety model: full release verification remains mandatory, GitHub release archives remain verified, npm publication remains verified, public `npx` smoke remains required after publication, and historical release evidence is not rewritten by routine release preparation.

This spec covers routine releases only. It defines the observable contract for release profiles, release preparation, release preflight, published evidence closeout, timing evidence, and local/CI gate parity.

## Glossary

- `routine release`: a release with the same npm package, same supported targets (`codex`, `claude`, `opencode`), same publication channels, same evidence schema, no emergency/security exception, no new adapter class, no release-schema migration, and no historical evidence rewrite.
- `special release`: a release outside the routine boundary that requires explicit owner decision and may use manual or extended release steps.
- `release profile`: the durable release transaction artifact at `docs/releases/profiles/<tag>.yaml`.
- `profile-owned generated surface`: a release surface whose routine content is generated from the release profile.
- `human-authored profile-checked surface`: a release surface with human narrative or decision content that is checked against the profile.
- `historical immutable surface`: prior release evidence, prior profile snapshots, or historical fixtures that routine release prep must not rewrite.
- `release preflight`: the cheap deterministic profile/schema/state check run before full release verification.
- `full release gate`: `bash scripts/release-verify.sh <tag>`, the authoritative local release verification command.
- `published evidence closeout`: post-publication evidence generation from public GitHub release assets, npm registry metadata, and fresh public `npx` smoke.

## Examples first

Example E1: routine release profile drives pending evidence
Given a maintainer prepares `v0.3.5` as a routine release
When `prepare-release` runs from `docs/releases/profiles/v0.3.5.yaml`
Then generated release metadata, pending release evidence, current-version fixture data, and package metadata pointers agree with the profile
And human-authored release notes narrative is not overwritten outside generated regions.

Example E2: cheap drift fails before full release verification
Given `packages/rigorloop/package.json` says `0.3.5`
And the active release profile says `0.3.6`
When release preflight runs for `v0.3.5`
Then preflight fails with a diagnostic naming the profile/package version mismatch
And the maintainer is not required to run the full release gate to discover that mismatch.

Example E3: published evidence uses validator-compatible shape
Given GitHub release assets and `@xiongxianfei/rigorloop@0.3.5` are public
When published evidence closeout runs for `v0.3.5`
Then npm metadata, tarball identity, archive metadata, public target smoke rows, tree hashes, file counts, and closeout status are written in validator-compatible form
And generated command strings match the validator's expected command shape.

Example E4: public evidence is not available yet
Given the GitHub release exists but npm registry metadata is not yet observable
When published evidence closeout runs
Then the command fails clearly with a pending external evidence diagnostic
And no unrelated files are modified.

Example E5: special release stays explicit
Given a release introduces a new adapter target
When the release profile is classified as routine
Then profile validation or preflight rejects the release as outside routine scope
And the release requires an explicit owner decision before automation proceeds.

## Requirements

R1. Routine release profiles MUST live at `docs/releases/profiles/<tag>.yaml`.

R2. A release profile MUST identify release tag, package version, npm package name, supported targets, adapter artifact expectations, publication requirements, evidence requirements, and validation requirements.

R3. The release profile MUST be the source of truth for routine release version state, target set, publication requirements, required evidence classes, and generated release-prep surfaces.

R4. Release tooling MAY read and validate the release profile, but scripts MUST NOT be the source of truth for routine release state once the profile exists for a release.

R5. The profile schema MUST distinguish routine releases from special releases.

R6. Routine release automation MUST reject or pause on releases outside the routine boundary unless an explicit owner decision records special-release handling.

R7. The system MUST classify every routine release-prep surface as `profile-owned generated`, `human-authored profile-checked`, or `historical immutable`.

R8. `prepare-release` MUST update profile-owned generated surfaces from the active release profile.

R9. `prepare-release` MUST NOT overwrite human-authored narrative content except inside explicitly marked generated regions.

R10. `prepare-release` MUST NOT rewrite historical immutable release surfaces.

R11. Manual overrides to generated surfaces MUST be explicit, review-visible, and checked by release preflight.

R12. `prepare-release` MUST be idempotent for the same complete release profile and same repository state.

R13. `prepare-release` MUST NOT publish, create tags, push commits, create GitHub releases, or read npm registry publication state.

R14. `prepare-release` MAY update release fixture data and expected values derived from the profile.

R15. `prepare-release` MUST NOT generate or rewrite test logic.

R16. Pending evidence generated by `prepare-release` MUST pass pre-publication release evidence validation.

R17. Pending evidence MUST use placeholders only where pre-publication validation explicitly permits them.

R18. Release preflight MUST be available as a Python-owned command, with preferred invocation `python scripts/release-preflight.py <tag>`, unless the spec is amended with an explicit exception.

R19. Release preflight MUST be idempotent and side-effect-light.

R20. Release preflight MUST NOT create or modify release artifacts except for an explicitly requested timing or log artifact.

R21. Release preflight MUST check release profile completeness, package/profile version agreement, generated metadata pointer drift, unauthorized current-version literals, pending evidence shape, local tag conflicts, remote tag conflicts when reachable, release-output directory state, and required local preflight inputs.

R22. Release preflight MUST fail for newly changed unauthorized current-version literals.

R23. Release preflight MUST report existing unauthorized current-version literals as baseline drift until they are cleaned or explicitly classified.

R24. Release preflight MUST allow historical version literals only when the affected surface is classified as historical.

R25. Release preflight MUST allow generated current-version literals only when they are derived from the active release profile.

R26. Literal-audit diagnostics MUST name the literal, file, classification, and expected owner.

R27. When full release verification fails on a cheap deterministic drift issue that preflight could have detected under the same inputs, the change that fixes the issue MUST add or update a preflight regression.

R28. `bash scripts/release-verify.sh <tag>` MUST remain the authoritative full local release gate.

R29. Local release verification and the GitHub Actions release workflow MUST invoke the same repository-owned release verification command set for a given release profile.

R30. Release automation MUST NOT remove or weaken GitHub release asset validation, npm publication validation, public `npx` smoke, archive SHA checks, tree hash checks, file count checks, adapter metadata validation, or package content checks.

R31. Published evidence closeout MUST be available as a deterministic rerunnable command for a release tag.

R32. Published evidence closeout MUST read public GitHub release asset metadata and npm registry metadata before marking publication evidence as published.

R33. Published evidence closeout MUST run fresh public `npx` smoke for `version`, `init codex`, `init claude`, and `init opencode` before marking post-publication target smoke as passed.

R34. Published evidence closeout MUST write target smoke command strings in the validator-expected shape, without recording local convenience flags such as `-y` when the validator contract excludes them.

R35. Published evidence closeout MUST write tree hashes in validator-compatible `sha256:<hex>` form, including root-qualified entries when a target has multiple install roots.

R36. Published evidence closeout MUST record file counts, archive verification status, tree verification status, closeout blockers, and post-publication closeout state for each target.

R37. Published evidence closeout MUST fail clearly when required public GitHub or npm evidence is not yet available.

R38. Published evidence closeout MUST NOT modify unrelated files when public evidence is unavailable.

R39. Release timing evidence MUST be recorded for routine releases.

R40. Missing timing evidence MUST fail when the profile requires timing.

R41. Duration values above human-time or wall-clock targets SHOULD be warning or observation evidence in the first slice, not hard release failures.

R42. Timing evidence MUST separate at least preflight, local release verification, GitHub release job, npm publish job, public smoke, and closeout when the data is available.

R43. Historical release evidence MUST NOT be migrated or rewritten by routine release automation.

R44. Generated diffs MUST remain reviewable and committed as tracked artifacts.

R45. The proposal-to-plan authoring profile MUST stop after clean plan-review and MUST NOT invoke test-spec, implementation, verification, PR, release, or publication.

## Inputs and outputs

Inputs include release tag, release profile, package metadata, adapter artifact metadata, generated release archive metadata, existing release evidence, release notes, npm package metadata, GitHub release asset metadata, npm registry metadata, local and remote tag state, current changed files, historical literal classifications, and timing data.

Outputs include generated or checked release profiles, package metadata updates, release metadata pointers, pending release evidence, pending npm-publication evidence, release notes generated regions, current-version fixture data, preflight diagnostics, full release-gate invocation evidence, published npm-publication evidence, public target smoke rows, timing evidence, and validation diagnostics.

## State and invariants

- A routine release has one active release profile.
- Profile-owned generated surfaces derive from the active profile.
- Human-authored profile-checked surfaces preserve human narrative outside generated regions.
- Historical immutable surfaces are not rewritten by routine release prep.
- Preflight catches cheap deterministic local/profile/schema drift before the full gate when inputs are the same.
- Full release verification remains authoritative for generated outputs, archive integrity, package contents, adapter metadata, and full validation.
- Published evidence is not marked published until public GitHub/npm/npx evidence exists.
- Timing evidence informs future optimization but does not initially fail duration budgets.

## Error and boundary behavior

- Missing release profile blocks routine release preparation and preflight.
- Malformed release profile blocks release preparation and preflight.
- Profile/package version mismatch blocks preflight.
- Unauthorized current-version literals in newly changed files block preflight.
- Existing baseline literal drift is reported until classified or cleaned.
- Missing or invalid pending evidence blocks preflight.
- Local tag conflicts block preflight unless explicitly allowed by an owner decision.
- Remote tag conflicts block preflight when remote state is reachable.
- Unreachable remote tag checks produce an explicit diagnostic and must not be silently treated as pass.
- Public evidence unavailability blocks published closeout and leaves pending evidence unchanged except for explicitly requested logs.
- Special releases pause or require explicit owner decision before routine automation proceeds.

## Compatibility and migration

Existing hand-authored historical release evidence remains valid. This spec does not require rewriting historical release files, historical fixtures, or prior release reports.

The first implementation may introduce literal-audit baseline reporting so existing drift can be classified without blocking adoption. Enforcement applies immediately to newly changed unauthorized current-version literals.

Existing `release-verify.sh` remains the full release gate. The release workflow should continue to delegate to repository-owned scripts.

Rollback keeps `release-verify.sh` and the last hand-authored release process available. Generators can be disabled before generated surfaces are removed. Validator-compatible evidence templates may remain useful even if command automation is reverted.

## Observability

Release preparation, preflight, full release verification, and published closeout should emit concise success summaries and actionable failure diagnostics.

Preflight diagnostics include literal, file, classification, expected owner, profile path, release tag, and corrective action when applicable.

Timing evidence records phase names, durations, result, and limitations. Public closeout evidence records package version, dist-tag, integrity, tarball URL, archive URLs, target smoke summaries, tree hashes, file counts, and closeout blockers.

## Security and privacy

Release tooling MUST NOT commit secrets, npm tokens, credentials, private keys, private environment dumps, private hostnames, usernames, or machine-local temp paths.

Local preflight MUST NOT require secrets. Published closeout may call public GitHub and npm endpoints and run public `npx` smoke, but evidence must summarize outputs without committing unnecessary machine-local details.

Manual override records must be review-visible and must not include private credentials or sensitive environment values.

## Accessibility and UX

No end-user UI is introduced. CLI and script output should remain readable, concise on success, and specific on failure.

## Performance expectations

Release preflight SHOULD target under 30 seconds on a typical maintainer machine by avoiding broad adapter distribution tests and full archive validation.

Full release verification remains intentionally broader and may take longer. Published closeout includes external network and registry latency, which should be recorded rather than treated as local script performance alone.

Human-time targets are measured as release evidence first. Duration budgets do not fail routine releases in the first slice unless the profile explicitly requires timing presence and timing is missing.

## Edge cases

EC1. A release profile exists but points to the wrong package version.

EC2. A current version literal appears in a changed test file outside generated fixture data.

EC3. A historical fixture contains an old release tag.

EC4. GitHub remote tag state cannot be reached during preflight.

EC5. GitHub release assets are available but npm registry metadata is delayed.

EC6. npm metadata is available but one target archive URL is missing or has the wrong checksum.

EC7. Opencode has multiple install roots and requires root-qualified tree hashes and file counts.

EC8. Release notes contain human narrative plus generated metadata regions.

EC9. A release introduces a new adapter target and is therefore special.

EC10. A manual override to a generated surface is present without review-visible rationale.

## Non-goals

- No removal or weakening of the full release gate.
- No removal of GitHub release asset validation.
- No removal of npm publication validation.
- No removal of public `npx` smoke.
- No removal of archive SHA, tree hash, file count, or adapter metadata validation.
- No historical release migration.
- No remote/shared cache introduction.
- No release-gate parallelism in the first slice.
- No automatic background publication monitor in the first slice.
- No hard timing budgets until multiple releases establish reliable baselines.
- No generation or rewrite of test logic.

## Acceptance criteria

AC1. A `release-profile-v1` schema exists and validates routine release profiles at `docs/releases/profiles/<tag>.yaml`.

AC2. `prepare-release` is idempotent for a complete routine release profile.

AC3. `prepare-release` generates pending release artifacts and profile-owned generated surfaces without overwriting human-authored narrative outside generated regions.

AC4. Pending evidence generated by `prepare-release` passes pre-publication validation.

AC5. Every release-prep surface is classified as generated, human-authored profile-checked, or historical immutable.

AC6. Current-version literal audit fails newly changed unauthorized literals and reports existing baseline drift.

AC7. Historical literals are allowed only on classified historical surfaces.

AC8. `python scripts/release-preflight.py <tag>` performs the cheap profile/schema/state checks without running the full release gate.

AC9. Preflight rejects missing profile, malformed profile, package/profile version mismatch, stale metadata pointer, unauthorized changed current literal, invalid pending evidence shape, and tag conflict fixtures.

AC10. `bash scripts/release-verify.sh <tag>` remains required for full local release verification.

AC11. The GitHub release workflow invokes the same repository-owned release verification command set for the release profile.

AC12. `close-release-publication` is rerunnable and fails clearly when public evidence is unavailable.

AC13. Published closeout generated from public GitHub/npm/npx data passes published evidence validation.

AC14. Public `npx` smoke remains required for `version`, `init codex`, `init claude`, and `init opencode`.

AC15. Published target smoke rows use validator-compatible command strings, `sha256:<hex>` tree hash shapes, file counts, and closeout fields.

AC16. Timing evidence is recorded for routine releases, and missing required timing fails validation.

AC17. Timing duration over target records warning or observation only in the first slice.

AC18. Historical release evidence is not modified by routine release preparation.

AC19. Special release boundaries are enforced or require explicit owner decision.

AC20. Behavior-preservation evidence shows full release verification, public smoke, adapter metadata validation, package metadata validation, and historical release immutability are preserved.

## Open questions

None at the proposal-to-spec boundary.

Implementation planning should settle exact generated-region marker syntax, baseline-literal audit file format, and timing file field names without changing this behavioral contract.

## Next artifacts

- implementation
- `code-review`
- `explain-change`
- `verify`
- `pr`

## Follow-on artifacts

- Spec-review: `docs/changes/2026-06-29-release-transaction-automation/reviews/spec-review-r1.md`
- Architecture assessment: `docs/changes/2026-06-29-release-transaction-automation/change.yaml`
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

Approved after `spec-review-r1`. Architecture, ADR, architecture-review, plan, plan-review, test spec, and clean test-spec-review are recorded. The active plan `Current Handoff Summary` owns the next workflow action.
