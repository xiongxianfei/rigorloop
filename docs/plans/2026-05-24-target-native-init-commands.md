# Target-Native Init Commands

## Status

Plan lifecycle state: done
Terminal disposition: merged

- Owner: maintainers
- Start date: 2026-05-24
- Last updated: 2026-05-26
- Related issue or PR: PR #92
- Supersedes: none

## Purpose / big picture

Implement the approved `0.3.0` target-native init contract for the RigorLoop npm CLI. The change removes public `--adapter`, makes default init install-only, adds explicit `--write-state`, writes target-oriented state schemas, preserves legacy state safely, and hardens release smoke so dry-run output cannot stand in for real install proof.

## Source artifacts

- Proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- Spec: `specs/target-native-init.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260524-target-native-init-state-boundary.md`
- Architecture review: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/architecture-review-r1.md`
- Change metadata: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
- Test spec: `specs/target-native-init.test.md`

## Context and orientation

The current CLI package is under `packages/rigorloop/` and is shipped as one npm binary, `rigorloop`.

Key implementation surfaces:

- `packages/rigorloop/dist/bin/rigorloop.js`: current parser, init runtime flow, metadata loading, archive verification, install mutation, manifest/lockfile writing, and human/JSON output.
- `packages/rigorloop/dist/lib/adapters.js`: current internal descriptor registry for `codex`, `claude`, and `opencode`.
- `packages/rigorloop/dist/lib/lockfile.js`: current schema v1/v2 lockfile parser and serializer using `generated.adapters`.
- `packages/rigorloop/test/cli.test.js`: CLI tests, fixture archive helpers, package fixture helpers, metadata tests, lockfile tests, local/network archive install tests, and new-change regression tests.
- `packages/rigorloop/README.md`: npm package usage surface currently teaching `init --adapter`.
- `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`, `scripts/release-verify.sh`, `scripts/npm_package_validation.py`, `scripts/test-npm-package-publication.py`: release metadata, package-content, docs, and packed-smoke validation surfaces that currently assume `0.2.0` and `--adapter`.

Important constraints:

- `dist/adapters/`, archive filenames, package-bundled metadata field names, and historical release evidence may keep adapter naming in this slice.
- Public CLI syntax, package README, public docs, CLI help, release notes for `0.3.0`, and new `rigorloop.yaml` / `rigorloop.lock` state keys must use target terminology.
- Default `init <target>` must not create or mutate `rigorloop.yaml` or `rigorloop.lock`, but it must parse existing state when needed for safe target-root mutation.
- `--write-state` may overwrite or regenerate `rigorloop.yaml` and `rigorloop.lock` only after successful verification.

## Non-goals

- Do not rename non-user-visible `dist/adapters/` paths, archive filenames, package-bundled metadata fields, or internal adapter generator concepts.
- Do not add target aliases such as `claude-code`, `open-code`, `openai`, or `codex-cli`.
- Do not add a top-level `rigorloop codex` command.
- Do not change generated skill content or target runtime behavior beyond command/state semantics.
- Do not introduce a general lockfile repair command.
- Do not publish or tag the release in this implementation plan.

## Requirements covered

- TNI-R1 through TNI-R13: M1 parser, help, error, and docs command contract; M3 docs and package release surfaces.
- TNI-R14 through TNI-R28: M1 state flag, default install-only behavior, state-write ordering, and output distinctions; M2 safety parsing and mutation behavior.
- TNI-R29 through TNI-R35: M2 target root install behavior and opencode compatibility preservation.
- TNI-R36 through TNI-R49: M2 trusted metadata, archive verification, tree hashing, file counts, and local archive behavior; M3 metadata/package publication validation.
- TNI-R50 through TNI-R75: M1 target-oriented schemas and lockfile parser/serializer; M2 legacy state compatibility and migration safety.
- TNI-R76 through TNI-R85: M1 dry-run and output behavior; M2 integration edge cases.
- TNI-R86 through TNI-R94: M3 packed-package smoke, live post-publish smoke contract, docs sweep, and release validation changes.
- AC-TNI-001 through AC-TNI-016: M1 through M3 implementation and test coverage, with final proof in M4.

## Current Handoff Summary

- Current milestone: final closeout
- Current milestone state: done
- Last reviewed milestone: M3. Release, Docs, And Package Validation Hardening
- Review status: M4 closed after clean code-review-r7
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: done
- Reason final closeout is or is not ready: PR #92 merged into the stacked cache-aware branch on 2026-05-25 and the merge commit is present on `main`.

## Milestones

### M1. CLI Command And State Schema Contract

- Milestone state: closed
- Goal: Replace the public init parser and state serialization contract with target-native commands, removed `--adapter`, explicit `--write-state`, target-oriented dry-run output, and schema v2/v3 state writers.
- Requirements: TNI-R1 through TNI-R13, TNI-R14 through TNI-R18, TNI-R25 through TNI-R28, TNI-R50 through TNI-R69, TNI-R76 through TNI-R85, AC-TNI-002 through AC-TNI-008, AC-TNI-014.
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`
  - `packages/rigorloop/dist/lib/adapters.js`
  - `packages/rigorloop/dist/lib/lockfile.js`
  - `packages/rigorloop/test/cli.test.js`
  - `packages/rigorloop/README.md`
- Dependencies:
  - Test spec must define exact test IDs before implementation begins.
  - Existing archive verification and tree-hash semantics remain authoritative.
- Tests to add/update:
  - Parser tests for `init codex`, `init claude`, `init opencode`, missing target, unknown target, aliases, removed `--adapter`, and mixed forms.
  - Help and README tests proving public command examples teach `init <target>`.
  - Default dry-run tests proving no state-file write plan.
  - `--write-state --dry-run --json` tests proving target-oriented planned state content.
  - Lockfile parser/serializer tests for schema v3 `generated.targets`.
- Implementation steps:
  - Add target positional parsing and `--write-state` flag while rejecting any `--adapter` use before mutation.
  - Keep internal descriptor lookup but expose `target` in new public output fields.
  - Split state planning from install planning so default init has no manifest or lockfile write plan.
  - Add `rigorloop.yaml` schema v2 writer using top-level `targets`.
  - Add `rigorloop.lock` schema v3 writer/parser using `generated.targets`.
  - Keep legacy schema v1/v2 parsing available as compatibility input.
  - Update CLI help and package README command examples.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
  - `git diff --check -- packages/rigorloop docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`
- Expected observable result: target-native syntax is accepted, removed `--adapter` fails early, default dry-run remains install-only, and `--write-state` previews target-oriented state.
- Commit message: `M1: add target-native init parser and state schema contract`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated
  - validation notes updated
  - code-review requested
- Risks:
  - Existing tests and helper fixtures assume `generated.adapters` and default state writes.
  - Over-eager rename could break deferred internal adapter metadata compatibility.
- Rollback/recovery:
  - Revert parser/state-writer changes for M1 before starting M2 if target-native and legacy compatibility cannot coexist cleanly.

### M2. Verified Install, Existing State Safety, And Target Roots

- Milestone state: closed
- Goal: Implement real install behavior for all targets under the new command contract, including existing-state safety parsing, legacy state handling, metadata/archive verification, opencode roots, local archive mode, and partial failure semantics.
- Requirements: TNI-R19 through TNI-R24, TNI-R29 through TNI-R49, TNI-R70 through TNI-R75, TNI-R81 through TNI-R85, AC-TNI-001, AC-TNI-005, AC-TNI-009 through AC-TNI-011, AC-TNI-016.
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`
  - `packages/rigorloop/dist/lib/lockfile.js`
  - `packages/rigorloop/test/cli.test.js`
  - `packages/rigorloop/dist/metadata/*.json`
- Dependencies:
  - M1 target and state schema contract must be in place.
  - Fixture metadata must include Codex, Claude Code, and opencode entries for the package version under test.
- Tests to add/update:
  - Default non-dry-run install for `codex`, `claude`, and `opencode` verifies target roots and creates no state files.
  - `--write-state` install for each target verifies target-oriented manifest and lockfile.
  - Valid unrelated state is byte-preserved by default.
  - Valid implicated state with matching installed tree follows the approved replacement behavior.
  - Drifted, conflicting, malformed, ambiguous, duplicate, and unsupported state blocks before target-root mutation.
  - Local archive wrong target, wrong SHA-256, wrong size, path traversal, symlink, and file-count mismatch still fail before extraction or success.
  - opencode declared commands install or fail verification; skills-only compatibility keeps the existing warning behavior.
- Implementation steps:
  - Add a state-safety reader that can classify target-oriented, legacy, malformed, ambiguous, unrelated, implicated, drifted, and conflicting state.
  - Run state safety checks before target-root mutation whenever state files exist.
  - Keep default init state files byte-identical.
  - Gate `--write-state` rewrites on successful verification and safe migration checks.
  - Update install result JSON and human output to distinguish skipped, planned, written, and failed state actions.
  - Ensure target roots and installed file counts are verified for every target.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/test-adapter-distribution.py`
  - `git diff --check -- packages/rigorloop scripts docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`
- Expected observable result: all supported targets install through `init <target>`, default state is preserved or safely blocks, and `--write-state` records verified target state only after successful install.
- Commit message: `M2: implement target-native verified install and state safety`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - code-review requested
- Risks:
  - Safety parsing can become a partial YAML parser with surprising unsupported-shape behavior.
  - Default install-only behavior can conflict with existing drift checks that currently depend on `rigorloop.lock` writes.
- Rollback/recovery:
  - Keep compatibility parser read-only and block ambiguous state rather than attempting more migration logic.
  - If a target-specific root behavior is uncertain, block the milestone and return to spec rather than guessing.

### M3. Release, Docs, And Package Validation Hardening

- Milestone state: closed
- Goal: Update package/release surfaces for `0.3.0`, enforce target-native docs, and add packed pre-publish plus live post-publish smoke contracts so dry-run-only release proof cannot pass.
- Requirements: TNI-R12, TNI-R13, TNI-R39 through TNI-R42, TNI-R86 through TNI-R94, AC-TNI-012 through AC-TNI-015.
- Files/components likely touched:
  - `packages/rigorloop/package.json`
  - `packages/rigorloop/README.md`
  - `packages/rigorloop/dist/metadata/*.json`
  - `scripts/adapter_distribution.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/release-verify.sh`
  - `scripts/npm_package_validation.py`
  - `scripts/test-npm-package-publication.py`
  - `docs/releases/v0.3.0/`
  - `docs/releases/v0.3.0.md`
  - `docs/releases/index.md`
  - `README.md`
  - `dist/adapters/README.md`
- Dependencies:
  - M1 and M2 CLI behavior must be available for packed-package smoke.
  - Release metadata for `v0.3.0` must be generated from or checked against actual release archives before publication readiness is claimed.
- Tests to add/update:
  - Package README and root README docs sweep for canonical `init <target>` examples and absence of public `init --adapter` teaching.
  - Release-note validation for `v0.3.0` target-native quick start, pinned automation command, release archive compatibility language, and no dry-run-only install proof.
  - Package-content tests updated for `0.3.0` metadata files.
  - Packed-package smoke tests covering default no-state install and `--write-state` for `codex`, `claude`, and `opencode`.
  - Post-publish evidence schema/test updates requiring live registry/download smoke entries for every target.
- Implementation steps:
  - Bump package version and release metadata references to `0.3.0` in package tests and release validators.
  - Update package README, root README usage, adapter install guidance, and release note expectations to teach `init <target>`.
  - Extend package validation to require real non-dry-run packed-package smoke for every supported target and reject dry-run-only proof.
  - Extend release validation/evidence expectations for live post-publish registry/download smoke after publication.
  - Keep historical release notes and old version evidence intact except where validators need version-aware expectations.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.3.0 --release-output-dir <release-output-dir> --release-commit <commit>`
  - `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`
  - `git grep -n "init --adapter\\|installing an adapter\\|Install the .* adapter" README.md packages docs dist || true`
- Release verification uses the current `scripts/release-verify.sh` interface: the release tag is positional, and release output directory / release commit are supplied through `RELEASE_OUTPUT_DIR` and `RELEASE_COMMIT`.
- Expected observable result: `0.3.0` release/package validation requires target-native real install proof and public docs no longer teach adapter-first init.
- Commit message: `M3: harden target-native release and docs validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Release validation is version-specific and currently has hard-coded `v0.2.0`/`--adapter` assumptions.
  - Live post-publish smoke cannot be executed before publish; the implementation must distinguish pre-publish required proof from post-publish evidence placeholders.
- Rollback/recovery:
  - Keep `v0.3.0` validation additions version-scoped to avoid breaking historical release checks.
  - If live registry evidence cannot be proven pre-publish, require structured post-publish evidence fields rather than pretending live smoke passed.

### M4. Lifecycle Closeout And Broad Validation

- Milestone state: closed
- Goal: Close implementation evidence after all code/docs/release surfaces are complete, resolve any code-review findings, refresh durable rationale, and prepare for final verify.
- Requirements: all acceptance criteria, plus repository workflow obligations for planned initiatives.
- Files/components likely touched:
  - `docs/plans/2026-05-24-target-native-init-commands.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
  - `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/explain-change.md`
  - possible review-resolution updates if code-review finds material issues
- Dependencies:
  - M1 through M3 are closed after code-review.
  - Test spec exists and maps every spec MUST to coverage or explicit deferral.
- Tests to add/update:
  - No new product tests unless code-review or verify finds a gap.
  - Lifecycle artifact validation and broad selected validation proof.
- Implementation steps:
  - Ensure the active plan reflects actual milestone states, validation, discoveries, and remaining gates.
  - Record explain-change after implementation and review-resolution are complete.
  - Run final selected validation, then verify.
  - Prepare PR handoff only after verify.
- Validation commands:
  - `bash scripts/ci.sh --mode explicit --path scripts/adapter_distribution.py --path scripts/npm_package_validation.py --path scripts/release-verify.sh --path scripts/test-adapter-distribution.py --path scripts/test-npm-package-publication.py --path docs/releases/index.md --path docs/releases/v0.3.0.md --path docs/releases/v0.3.0/release.yaml --path docs/releases/v0.3.0/release-notes.md --path docs/releases/v0.3.0/npm-publication.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/explain-change.md --path README.md --path packages/rigorloop --path specs/target-native-init.md --path docs/plans/2026-05-24-target-native-init-commands.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md --path specs/target-native-init.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260524-target-native-init-state-boundary.md --path docs/plans/2026-05-24-target-native-init-commands.md --path docs/plan.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
  - `git diff --check --`
- Verify report: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/verify-report.md`
- Expected observable result: all implementation milestones are closed, required review-resolution is closed if triggered, explain-change exists, and verify can assess branch readiness.
- Commit message: `M4: close target-native init lifecycle evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Multiple active plans in `docs/plan.md` increase stale-index risk.
  - Broad validation may expose unrelated baseline debt.
- Rollback/recovery:
  - Keep this plan active until final closeout gates complete; do not mark done because implementation milestones are coded.
  - Record unrelated baseline debt as verify warnings only when repository validators classify it that way.

## Validation plan

- `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`: validate change metadata after plan creation and later milestone updates.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`: validate prior proposal/spec/architecture review evidence remains closed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md --path specs/target-native-init.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260524-target-native-init-state-boundary.md --path docs/plans/2026-05-24-target-native-init-commands.md --path docs/plan.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`: validate lifecycle-managed planning surfaces.
- `npm test --prefix packages/rigorloop`: primary CLI behavior regression suite.
- `python scripts/test-npm-package-publication.py`: npm package-content and packed-smoke regression suite.
- `python scripts/test-adapter-distribution.py`: adapter/release metadata and docs validation regression suite.
- `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`: final pre-publish release gate after release artifacts exist, using the current release script interface.
- `git diff --check --`: whitespace and patch hygiene.

## Risks and recovery

- Risk: The current CLI combines parsing, metadata verification, install mutation, manifest writing, and lockfile writing in one file.
  - Recovery: Split only enough helper logic to make target/state behavior testable; avoid broad refactors not needed for the spec.
- Risk: Existing tests and validators use adapter terminology as current public behavior.
  - Recovery: Update public-facing tests for `0.3.0`, while preserving historical release evidence and internal adapter metadata tests where the proposal explicitly defers rename.
- Risk: Real packed-package smoke can be expensive or awkward in unit tests.
  - Recovery: Use package fixture smoke in unit/regression tests and reserve full `npm pack` release proof for release validation.
- Risk: Existing state parsing can over-accept malformed or future schemas.
  - Recovery: Prefer conservative blocking for malformed, ambiguous, unsupported, or duplicate state per TNI-R23 and TNI-R73.
- Risk: Publication/live registry smoke cannot pass before publication.
  - Recovery: Pre-publish gates require packed-package smoke; release evidence schema requires live post-publish entries to close after publish.

## Dependencies

- Plan-review must approve this plan before test-spec and implementation.
- Test spec must be written before implementation starts.
- Release archive output for `v0.3.0` is required before final release validation can pass.
- Network/live registry post-publish smoke is a release execution gate, not an implementation milestone completion claim.

## Progress

- 2026-05-24: Created plan after proposal, spec, architecture, and architecture-review approval.
- 2026-05-24: Added active test spec at `specs/target-native-init.test.md`; M1 is ready for implementation.
- 2026-05-24: Started M1 implementation. Scope is parser/state schema contract, default install-only planning, removed `--adapter`, `--write-state`, target-oriented dry-run/state output, and package README/help alignment.
- 2026-05-24: Completed M1 implementation and moved it to code-review. The package CLI accepts `init <target>`, rejects `--adapter`, keeps default init install-only for state files, and writes target-oriented schema v2/v3 state only with `--write-state`.
- 2026-05-24: `code-review-r1` requested changes for `TNI-CR1-F1`: add direct package CLI tests for named alias targets and mixed removed `--adapter` forms before M1 can close.
- 2026-05-24: Resolved `TNI-CR1-F1` by adding direct package CLI tests for the named rejected aliases and mixed removed syntax forms. M1 is back in code-review handoff.
- 2026-05-24: `code-review-r2` approved M1 with no material findings. M1 is closed and M2 is the next implementation milestone.
- 2026-05-24: Started M2 implementation. Scope is verified install behavior, existing-state safety parsing, legacy state compatibility, target roots, opencode install compatibility, and archive/tree verification behavior under target-native init.
- 2026-05-24: Completed M2 implementation and moved it to code-review. Default non-dry-run init now installs targets without state files, preserves unrelated valid state byte-for-byte, parses existing state before target-root mutation, blocks malformed or implicated drifted state before mutation, and keeps explicit filesystem conflicts classified as mutation conflicts.
- 2026-05-24: `code-review-r3` requested changes for `TNI-CR3-F1`: add direct M2 package CLI tests for default opencode no-state install, default implicated drift/conflict blocking, and default legacy adapter state preservation before M2 can close.
- 2026-05-24: Resolved `TNI-CR3-F1` by adding direct default-init package CLI tests for opencode skills/commands install without state files, selected-target drift blocking, overlapping managed-root conflict blocking, and legacy adapter state byte preservation. The new tests passed without production runtime changes. M2 is back in code-review handoff.
- 2026-05-24: `code-review-r4` approved M2 with no material findings. M2 is closed and M3 is the next implementation milestone.
- 2026-05-24: Started M3 implementation. Scope is v0.3.0 package metadata, target-native public docs, package-bundled release metadata, packed-package real install smoke, release verification support, and post-publish live smoke evidence contracts.
- 2026-05-24: Completed M3 implementation and moved it to code-review. The package is versioned as 0.3.0, bundled v0.3.0 metadata is derived from generated release archives, docs and release notes teach `init <target>`, npm package smoke now runs real non-dry-run default and `--write-state` installs for all supported targets, and release evidence records the live post-publish target smoke contract.
- 2026-05-24: `code-review-r5` requested changes for `TNI-CR5-F1`: extend v0.3.0 post-publish target-smoke evidence and validation so published live-smoke rows include installed root(s), tree hash value(s), file count(s), and command output summary.
- 2026-05-24: Resolved `TNI-CR5-F1` by extending v0.3.0 target-smoke evidence fields, adding pending placeholders and a visible evidence table, enforcing published evidence details in `scripts/adapter_distribution.py`, and adding positive/negative release validation tests. M3 is back in code-review handoff.
- 2026-05-24: `code-review-r6` approved M3 with no material findings. M3 is closed and M4 lifecycle closeout is the next implementation milestone.
- 2026-05-24: Started M4 implementation. Scope is lifecycle state synchronization, durable explain-change rationale, broad selected validation evidence, and handoff to code-review; no product behavior changes are planned.
- 2026-05-24: M4 added `explain-change.md`, aligned the flat v0.3.0 release evidence file with the standing release-evidence checklist, and moved M4 to code-review handoff after validation passed.
- 2026-05-24: `code-review-r7` approved M4 with no material findings. All in-scope implementation milestones are closed; verify is the next stage.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-24 | Split implementation into parser/state schema, verified install/state safety, release/docs validation, and lifecycle closeout milestones. | The change crosses CLI parsing, state schemas, archive install behavior, docs, package metadata, and release validation; each slice has distinct review risks. | One large implementation milestone; docs/release validation before CLI behavior exists. |
| 2026-05-24 | Keep release/live smoke validation as a separate milestone from core CLI behavior. | Packed and live smoke gates need package/release artifacts and have different recovery paths from parser or install failures. | Hiding release validation inside the CLI milestone. |
| 2026-05-24 | Use the existing environment-variable interface for `scripts/release-verify.sh` in the plan. | Resolves `TNI-PLR1-F1` without adding a new release script option parser to M3 scope. | Adding `--release-output-dir` and `--release-commit` parsing in this slice. |
| 2026-05-24 | Keep M1 internal descriptor and archive metadata naming adapter-oriented while changing public command/state schema keys. | The approved boundary defers non-user-visible internal archive and descriptor renames, and package-bundled metadata remains a later milestone surface. | Renaming `dist/adapters`, archive filenames, or package-bundled metadata fields during M1. |
| 2026-05-24 | Let generated-output path conflicts classify before existing-state drift safety during M2. | Both checks run before mutation, but explicit file/directory conflicts already have the public exit class `mutation_conflict` and must not be downgraded to a generic state block. | Running state drift checks before conflict classification for all write-state reruns. |

## Surprises and discoveries

- The current package tests, package README, release validators, and npm publication tests still have hard-coded `0.2.0` and `init --adapter` assumptions that must be updated in a version-scoped way.
- `scripts/adapter_distribution.py` owns several release-note and npm publication checks that will need target-native expectations for `v0.3.0`.
- Plan-review R1 found that the original `release-verify.sh` validation command used unsupported long options; the plan now uses `RELEASE_OUTPUT_DIR` and `RELEASE_COMMIT` with a positional `v0.3.0` tag.
- M1 needed schema v2 manifest parsing in addition to writing, because `--write-state` reruns and legacy-upgrade tests immediately read the new `targets` state before later install safety work begins.
- Code-review R1 found the parser implementation path appears broader than the direct test proof: aliases and mixed removed syntax need explicit durable coverage, not only generic unknown-target and simple removed-syntax cases.
- The parser-edge review-resolution did not require production parser changes; the added tests passed against the existing early-rejection behavior.
- M2 exposed that default install-only still needs safety reads: unrelated valid lockfile drift must not block a different target, but malformed state must block before mutation because target/root implication cannot be proven.
- The package publication smoke test still expected the old `init --adapter` help and dry-run command; it was updated to assert the target-native packed binary behavior already implemented by M1/M2.
- M3 packed-package smoke against generated release archives exposed that Claude archives include top-level `CLAUDE.md`; the installer now treats `CLAUDE.md` as a support entry like `AGENTS.md` so real release archives can verify without treating the entrypoint as an unsafe target-root file.
- v0.3.0 release evidence needs two distinct gates: packed-package pre-publish smoke can pass before publication, while live registry/download post-publish smoke remains pending evidence until npm and GitHub release assets are externally observable.
- The initial M4 selected CI command used broad directory paths from the plan and the selector blocked `scripts`, `docs/releases`, and the change root as unclassified explicit paths. The M4 validation command now uses concrete changed files that the selector can classify.
- The first concrete-path selected CI run found that `docs/releases/v0.3.0.md` was a skeletal release summary, but the repository now treats flat `docs/releases/v<version>.md` files as standing release-evidence records. M4 aligned `docs/releases/v0.3.0.md` to the release evidence template before rerunning validation.

## Validation notes

- 2026-05-24: `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml` passed.
- 2026-05-24: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement` passed before plan creation with 7 reviews, 4 findings, 7 log entries, and 4 resolution entries.
- 2026-05-24: `git diff --check -- docs/plans/2026-05-24-target-native-init-commands.md docs/plan.md docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement` passed.
- 2026-05-24: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md --path specs/target-native-init.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260524-target-native-init-state-boundary.md --path docs/plans/2026-05-24-target-native-init-commands.md --path docs/plan.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r1.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r2.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r3.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r1.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r2.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r3.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/architecture-review-r1.md` passed with 4 artifact files validated.
- 2026-05-24: Revised the M3 and global validation plan release-verify command to use `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`, resolving the plan command-shape issue from `TNI-PLR1-F1`.
- 2026-05-24: Added `specs/target-native-init.test.md` to map the approved spec and plan to concrete CLI, state, archive, docs, release, migration, security, and smoke tests.
- 2026-05-24: `npm test --prefix packages/rigorloop` passed for M1 with 109 tests passing.
- 2026-05-24: Recorded `code-review-r1` with material finding `TNI-CR1-F1`; review artifact structure validation, change metadata validation, lifecycle validation, and patch hygiene passed for the review record and handoff updates.
- 2026-05-24: `npm test --prefix packages/rigorloop` passed with 110 tests after resolving `TNI-CR1-F1`.
- 2026-05-24: After resolving `TNI-CR1-F1`, `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`, and `git diff --check --` passed.
- 2026-05-24: Recorded clean `code-review-r2`; review artifact closeout validation, change metadata validation, lifecycle validation, and patch hygiene passed for the review record and handoff updates.
- 2026-05-24: Focused M2 regression command `npm test --prefix packages/rigorloop -- --test-name-pattern "TTNI-INST-001|TTNI-STATE-003|TTNI-STATE-006"` passed after implementing state safety.
- 2026-05-24: `npm test --prefix packages/rigorloop -- --test-name-pattern "TTNI-INST-001|TTNI-STATE-003|TTNI-STATE-006|TLF-027"` passed after preserving mutation-conflict classification for generated file path conflicts.
- 2026-05-24: `npm test --prefix packages/rigorloop` passed with 113 tests after M2 implementation.
- 2026-05-24: `python scripts/test-npm-package-publication.py` passed after aligning packed binary smoke expectations with target-native help and dry-run syntax.
- 2026-05-24: `python scripts/test-adapter-distribution.py` passed with 103 tests after M2 implementation.
- 2026-05-24: `git diff --check -- packages/rigorloop scripts docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement` passed after M2 implementation.
- 2026-05-24: After M2 handoff updates, `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/target-native-init.md --path specs/target-native-init.test.md --path docs/plans/2026-05-24-target-native-init-commands.md --path docs/plan.md --path docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`, and `git diff --check -- packages/rigorloop scripts docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement docs/plans/2026-05-24-target-native-init-commands.md docs/plan.md` passed.
- 2026-05-24: `npm test --prefix packages/rigorloop -- --test-name-pattern "TTNI-INST-002|TTNI-STATE-005|TTNI-MIG-001"` passed after resolving `TNI-CR3-F1`.
- 2026-05-24: `npm test --prefix packages/rigorloop` passed with 117 tests after resolving `TNI-CR3-F1`.
- 2026-05-24: `python scripts/test-npm-package-publication.py` passed after resolving `TNI-CR3-F1`.
- 2026-05-24: `python scripts/test-adapter-distribution.py` passed with 103 tests after resolving `TNI-CR3-F1`.
- 2026-05-24: `git diff --check -- packages/rigorloop scripts docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement docs/plans/2026-05-24-target-native-init-commands.md docs/plan.md` passed after resolving `TNI-CR3-F1`.
- 2026-05-24: `npm test --prefix packages/rigorloop` passed with 117 tests after M3 package/version, metadata, and archive support-entry updates.
- 2026-05-24: `python scripts/test-npm-package-publication.py` passed after adding real non-dry-run packed-package smoke for default and `--write-state` init across `codex`, `claude`, and `opencode`.
- 2026-05-24: `python scripts/test-adapter-distribution.py` passed with 104 tests after adding v0.3.0 release-gate coverage.
- 2026-05-24: `python scripts/validate-release.py --version v0.3.0 --release-output-dir <temp-release-output-dir> --release-commit 02a9d7d6d514fc99908abf32898494dbbbae00c9` passed after building v0.3.0 release archives into the temp output directory.
- 2026-05-24: `RELEASE_OUTPUT_DIR=<temp-release-output-dir> RELEASE_COMMIT=02a9d7d6d514fc99908abf32898494dbbbae00c9 bash scripts/release-verify.sh v0.3.0` passed, including package publication smoke and v0.3.0 release metadata validation.
- 2026-05-24: `git grep -n "init --adapter\\|installing an adapter\\|Install the .* adapter" README.md packages docs dist || true` returned only historical/compatibility records plus the v0.3.0 removed-syntax diagnostic in CLI source; current root README, package README, and v0.3.0 release notes teach target-native init.
- 2026-05-24: M3 handoff validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check --`.
- 2026-05-24: Recorded `code-review-r5` with material finding `TNI-CR5-F1`; review artifact structure validation, change metadata validation, lifecycle validation, and patch hygiene passed for the review record and handoff updates.
- 2026-05-24: Focused `TNI-CR5-F1` target-smoke evidence tests passed after adding post-publish live-smoke detail enforcement.
- 2026-05-24: `python scripts/test-adapter-distribution.py` passed with 112 tests after resolving `TNI-CR5-F1`.
- 2026-05-24: `python scripts/test-npm-package-publication.py` passed with 6 tests after resolving `TNI-CR5-F1`.
- 2026-05-24: `npm test --prefix packages/rigorloop` passed with 117 tests after resolving `TNI-CR5-F1`.
- 2026-05-24: `python scripts/validate-release.py --version v0.3.0 --release-output-dir /tmp/tmp.cWJYJ5cs7M --release-commit 02a9d7d6d514fc99908abf32898494dbbbae00c9` passed after resolving `TNI-CR5-F1`.
- 2026-05-24: `RELEASE_OUTPUT_DIR=/tmp/tmp.cWJYJ5cs7M RELEASE_COMMIT=02a9d7d6d514fc99908abf32898494dbbbae00c9 bash scripts/release-verify.sh v0.3.0` passed after resolving `TNI-CR5-F1`.
- 2026-05-24: After resolving `TNI-CR5-F1`, `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`, and `git diff --check --` passed.
- 2026-05-24: Recorded clean `code-review-r6`; review artifact closeout validation, change metadata validation, lifecycle validation, and patch hygiene passed for the review record and M3-to-M4 handoff updates.
- 2026-05-24: `npm pack --dry-run --json` from `packages/rigorloop` passed and reported `xiongxianfei-rigorloop-0.3.0.tgz`, 14 entries, 25902 bytes packed, 118691 bytes unpacked, and integrity `sha512-IR/gzYwXfd/Nvg0Wkcd5QQK9YRtnITVOqaf17i2KVw1pMy99L2Z2Bk7PqXlxEDWrWe+OuKEWAewPLFPoM4EhiQ==`.
- 2026-05-24: Initial M4 selected CI command with directory paths failed before checks with selector `unclassified-path` for `scripts`, `docs/releases`, and `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`.
- 2026-05-24: First concrete-path M4 selected CI run executed selected checks but failed `artifact_lifecycle.validate` because `docs/releases/v0.3.0.md` did not satisfy the standing release-evidence checklist.
- 2026-05-24: After aligning `docs/releases/v0.3.0.md`, focused lifecycle validation passed for `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`, `explain-change.md`, `docs/plans/2026-05-24-target-native-init-commands.md`, `docs/releases/index.md`, `docs/releases/v0.3.0.md`, and `specs/target-native-init.md`.
- 2026-05-24: M4 selected CI passed with checks `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `release.validate`, `readme.validate`, `readme.vision_markers`, `selector.regression`, `broad_smoke.repo`, `rigorloop_cli.test`, and `npm_package_publication.test`.
- 2026-05-24: M4 explicit lifecycle validation, review-artifact closeout validation, change metadata validation, and `git diff --check --` passed after the selected CI run.
- 2026-05-24: Initial verify blocked because authoritative new artifacts were still untracked. The full change pack was committed in `33d41c6`, resolving the tracked-branch-state blocker.
- 2026-05-24: Final verify passed after commit. `python scripts/query-change-record.py 2026-05-24-target-native-init-commands-and-adapter-terminology-retirement summary`, review-artifact closeout validation, change metadata validation, explicit artifact lifecycle validation, and `bash scripts/ci.sh --mode pr --base main --head HEAD` passed. PR-mode selected CI included broad smoke and validated the full stacked branch range.
- 2026-05-25: PR #92 merged at `a4fcca4b57acc703ac2fe337ed29b596be75dfda`; the stacked merge is present on `main`.

## Outcome and retrospective

- Implementation milestones are complete and code-reviewed. Final verification passed. PR #92 merged and is present on `main`.

## Readiness

- Done. PR #92 merged and no downstream lifecycle gates remain.
