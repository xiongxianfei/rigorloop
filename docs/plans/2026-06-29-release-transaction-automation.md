# Release Transaction Automation Execution Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-29-release-transaction-automation
- Owner: maintainer
- Start date: 2026-06-29
- Last updated: 2026-06-29
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement routine release automation as a typed release transaction. The work moves routine release state into `docs/releases/profiles/<tag>.yaml`, generates or checks release-prep surfaces from that profile, catches cheap drift before full verification, preserves `release-verify.sh <tag>` as the authoritative release gate, generates validator-compatible public closeout evidence, and records timing evidence.

The plan keeps release safety ahead of speed. It reduces human release time by removing duplicated hand-edited state and late evidence-shape loops, not by deleting release checks.

## Source artifacts

- Proposal: [Release Transaction Automation and Evidence Generation](../proposals/2026-06-29-release-transaction-automation.md)
- Proposal-review: [proposal-review-r1](../changes/2026-06-29-release-transaction-automation/reviews/proposal-review-r1.md)
- Spec: [Release Transaction Automation and Evidence Generation](../../specs/release-transaction-automation.md)
- Spec-review: [spec-review-r1](../changes/2026-06-29-release-transaction-automation/reviews/spec-review-r1.md)
- Architecture: [canonical system architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260629-release-transaction-profile](../adr/ADR-20260629-release-transaction-profile.md)
- Architecture-review: [architecture-review-r1](../changes/2026-06-29-release-transaction-automation/reviews/architecture-review-r1.md)
- Change metadata: [change.yaml](../changes/2026-06-29-release-transaction-automation/change.yaml)

## Context and orientation

This is repository release tooling and evidence work. It touches release profiles under `docs/releases/profiles/`, release evidence under `docs/releases/`, adapter artifact metadata under `docs/reports/adapter-artifacts/releases/`, npm package metadata under `packages/rigorloop/`, release validators under `scripts/`, tests and fixtures, and `.github/workflows/release.yml` only as a thin CI wrapper around repository-owned release commands.

Important existing boundaries:

- `docs/releases/` owns durable release evidence.
- `release-verify.sh <tag>` is the full maintainer-facing release gate.
- `validate-release.py` owns structured release evidence validation delegated from the release gate.
- Generated adapter archives are release assets; metadata and checksums are tracked evidence.
- Historical release evidence must not be rewritten by routine release prep.
- Public npm/GitHub/npx evidence is external state and may require rerunnable closeout.

## Non-goals

- Do not weaken full release verification.
- Do not remove GitHub release asset validation, npm publication validation, public `npx` smoke, archive SHA checks, tree hash checks, file count checks, adapter metadata validation, or package content checks.
- Do not migrate historical release evidence.
- Do not add release-gate parallelism in this slice.
- Do not add remote/shared caches.
- Do not add background publication monitoring.
- Do not generate or rewrite test logic.
- Do not proceed to implementation until plan-review and the matching test spec are complete.

## Requirements covered

- `R1`-`R6`: M1, M2, M3
- `R7`-`R17`: M1, M2, M3
- `R18`-`R27`: M4
- `R28`-`R30`: M5
- `R31`-`R38`: M6
- `R39`-`R42`: M5, M6
- `R43`-`R44`: M2, M3, M6
- `R45`: completed by this authoring profile after clean plan-review
- `AC1`-`AC7`: M1, M2, M3, M4
- `AC8`-`AC11`: M4, M5
- `AC12`-`AC17`: M6
- `AC18`-`AC20`: M2, M3, M5, M6

## Current Handoff Summary

- Current milestone: M6. Published evidence closeout and behavior preservation
- Current milestone state: closed
- Latest review evidence: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m6-r2.md
- Last reviewed milestone: M6
- Review status: approved; stage=code-review; round=r2
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: pr-handoff-pending — all in-scope implementation milestones are closed and final verify passed locally, but PR handoff remains.

## Milestones

### M1. Release profile schema and loader

- Milestone state: closed
- Goal: Define `release-profile-v1`, load profiles from `docs/releases/profiles/<tag>.yaml`, and validate routine versus special release boundaries.
- Requirements: `R1`-`R6`, `AC1`, `AC19`
- Files/components likely touched:
  - `schemas/` or existing schema location selected by test spec
  - `scripts/validate-release.py`
  - new shared release-profile helper under `scripts/`
  - `docs/releases/profiles/`
  - release-profile fixtures under the existing test fixture tree
- Dependencies:
  - Test spec must settle exact schema fields, fixture names, and whether schema validation is YAML-schema, Python validator, or both.
- Tests to add/update:
  - Valid routine profile for supported targets.
  - Missing profile, malformed profile, wrong package version, unknown target, and special-release classification fixtures.
  - Unknown closed-vocabulary values fail closed before consistency checks.
- Validation commands:
  - `python scripts/test-release-transaction.py` after M1 introduces it
  - `python scripts/validate-release.py --help`
- Expected observable result: A routine release profile is a loadable, validated source of truth, and invalid/special profiles block routine automation.
- Commit message: `M1: add release profile schema`
- Risks:
  - The profile could duplicate existing constants without displacing them.
  - Schema validation could accept unknown fields too broadly.
- Rollback/recovery:
  - Revert profile loader/schema changes while leaving existing hand-authored release process and `release-verify.sh` intact.

### M2. Release-surface inventory and ownership classification

- Milestone state: closed
- Goal: Inventory routine release-prep surfaces, classify them as profile-owned generated, human-authored profile-checked, or historical immutable, and add the baseline literal-audit classification needed before enforcement.
- Requirements: `R7`, `R10`, `R11`, `R14`, `R15`, `R22`-`R26`, `R43`, `R44`, `AC5`-`AC7`, `AC18`
- Files/components likely touched:
  - release validation fixtures and expected values
  - `scripts/validate-release.py`
  - new or existing release literal audit helper
  - `docs/changes/2026-06-29-release-transaction-automation/` evidence for baseline classification if required by test spec
- Dependencies:
  - M1 profile model must exist before generated-current literals can be classified as derived from the active profile.
- Tests to add/update:
  - Changed unauthorized current-version literal fails.
  - Existing baseline unauthorized current-version literal reports without blocking initial adoption.
  - Historical fixture literal is allowed only when classified historical.
  - Generated current literal is allowed only when profile-derived.
- Validation commands:
  - `python scripts/test-release-transaction.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-29-release-transaction-automation/change.yaml`
- Expected observable result: Every routine release surface has an ownership classification, and literal-drift diagnostics name literal, file, classification, and expected owner.
- Commit message: `M2: classify release surfaces and literals`
- Risks:
  - Baseline reporting could become permanent drift.
  - Classification rules could accidentally flag historical release evidence.
- Rollback/recovery:
  - Keep audit in report-only mode and disable enforcement while preserving the inventory.

### M3. `prepare-release` pending artifact generation

- Milestone state: closed
- Goal: Implement idempotent release preparation from the active profile, generating profile-owned surfaces and pending evidence while preserving human-authored narrative and historical evidence.
- Requirements: `R8`-`R17`, `R43`, `R44`, `AC2`-`AC5`, `AC18`
- Files/components likely touched:
  - `scripts/prepare-release.py`
  - shared release-profile helper
  - `docs/releases/<tag>/release.yaml`
  - `docs/releases/<tag>/release-notes.md`
  - `docs/releases/<tag>/npm-publication.md`
  - package metadata and release fixture data selected by test spec
- Dependencies:
  - M1 profile schema and M2 ownership classification.
  - Test spec must settle generated-region marker syntax.
- Tests to add/update:
  - `prepare-release` idempotency.
  - Pending evidence passes pre-publication validation.
  - Human-authored release-note narrative outside generated regions is preserved.
  - Historical release evidence is not modified.
  - The command does not publish, tag, push, or read npm publication state.
- Validation commands:
  - `python scripts/test-release-transaction.py`
  - `python scripts/prepare-release.py <fixture-tag> --check` if implemented by the milestone
  - `python scripts/validate-release.py <fixture-tag> --phase pre-publication` or the test-spec-selected equivalent
- Expected observable result: Routine release prep becomes a repeatable generated transaction from a complete profile.
- Commit message: `M3: generate pending release artifacts`
- Risks:
  - Generator breadth could overwrite narrative or unrelated files.
  - Generated diffs could become hard to review if ownership regions are vague.
- Rollback/recovery:
  - Disable the generator entrypoint and keep validator-compatible templates if useful.

### M4. Release preflight command

- Milestone state: closed
- Goal: Add Python-owned `release-preflight` as the cheap deterministic local/profile/schema gate before full release verification.
- Requirements: `R18`-`R27`, `AC8`, `AC9`
- Files/components likely touched:
  - `scripts/release-preflight.py`
  - shared release-profile and literal-audit helpers
  - release validator tests and fixtures
  - optional thin shell wrapper only if test spec allows it
- Dependencies:
  - M1-M3 must provide profiles, ownership classes, and pending evidence surfaces.
- Tests to add/update:
  - Missing profile, malformed profile, version mismatch, stale metadata pointer, unauthorized changed literal, invalid pending evidence shape, local tag conflict, reachable remote tag conflict, unreachable remote diagnostic, and dirty release-output fixtures.
  - Idempotency and side-effect-light behavior.
  - No broad adapter distribution tests are run by preflight.
- Validation commands:
  - `python scripts/test-release-transaction.py`
  - `python scripts/release-preflight.py <fixture-tag>`
- Expected observable result: Cheap deterministic drift fails before `release-verify.sh`, with actionable diagnostics and no publication side effects.
- Commit message: `M4: add release preflight`
- Risks:
  - Preflight could duplicate expensive release verification.
  - Remote tag checks could be flaky if unreachable state is not explicit.
- Rollback/recovery:
  - Keep preflight advisory or report-only while full release gate remains unchanged.

M4 code review status:

- `code-review-m4-r1` requested changes for `CR-RTA-M4-F1` and `CR-RTA-M4-F2`; both findings are resolved in review-resolution and M4 is ready for rerun review.
- `CR-RTA-M4-F1`: default `python scripts/release-preflight.py <tag>` now derives changed files from Git when `--changed-file` is absent. CLI regression coverage proves a changed unauthorized current-version literal fails under the default invocation.
- `CR-RTA-M4-F2`: direct M4 preflight negative tests now cover malformed profile, incomplete profile, and missing required local input.
- Validation: `python scripts/test-release-transaction.py` passed with 50 tests; `python scripts/release-preflight.py --help` passed; Python compilation passed; selector validation remains blocked on known manual-routing for release transaction scripts and unclassified fixture directories while tracked-authoritative-artifact preflights passed.
- `code-review-m4-r2` completed with no material findings. M4 is closed.
- Next action: implement M5.

### M5. Full release gate parity and timing evidence

- Milestone state: closed
- Goal: Preserve `release-verify.sh <tag>` as the full local gate, align CI release workflow with the same repository-owned command set, and record timing evidence.
- Requirements: `R28`-`R30`, `R39`-`R42`, `AC10`, `AC11`, `AC16`, `AC17`, `AC20`
- Files/components likely touched:
  - `scripts/release-verify.sh`
  - `.github/workflows/release.yml`
  - `scripts/validate-release.py`
  - timing evidence helper or template
  - release validation tests
- Dependencies:
  - M4 preflight must exist so the full gate boundary can be tested against cheap deterministic drift.
- Tests to add/update:
  - CI workflow invokes the same repository-owned command set.
  - Full release gate remains required after preflight.
  - Timing evidence presence is required when profile requires it.
  - Over-target duration records warning/observation, not a hard first-slice failure.
  - Safety checks are not removed from `release-verify.sh`.
- Validation commands:
  - `python scripts/test-release-transaction.py`
  - `bash scripts/release-verify.sh <fixture-tag>` or a fixture-safe equivalent selected by test spec
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path .github/workflows/release.yml --path scripts/release-verify.sh --path scripts/validate-release.py`
- Expected observable result: Local and CI release readiness rely on the same command set, timing is durable evidence, and preflight does not weaken the full gate.
- Commit message: `M5: preserve release gate parity and timing`
- Risks:
  - CI workflow edits could drift from local command behavior.
  - Timing capture could become flaky if it enforces duration too early.
- Rollback/recovery:
  - Revert CI parity/timing edits while keeping full local `release-verify.sh` unchanged.

M5 implementation status:

- Added timing evidence validation helpers for `release-timing-v1`, required first-slice phase IDs, closed result values, missing timing evidence, missing duration values, and warning-only over-target durations.
- `prepare-release` now generates a reviewable `docs/releases/<tag>/timing.yaml` skeleton for routine releases when the profile requires timing evidence.
- `release-verify.sh` now registers `v0.3.5` in the existing release target, release-output, untracked-public-adapter, and npm-package release gates. The required command set remains unchanged.
- Added a static release workflow parity check proving `.github/workflows/release.yml` delegates release readiness and npm publication validation to `bash scripts/release-verify.sh` instead of duplicating release-gate checks.
- `CR-RTA-M5-F1` resolution: `scripts/validate-release.py` now wires profile-required timing validation into the repository-owned release validation path. Missing or malformed required timing evidence fails through `validate-release.py`; over-target timing produces warning output without failing; releases without profiles remain compatible.
- Unaffected aligned surface: `.github/workflows/release.yml` already used the repository-owned release command set, so M5 added validator coverage instead of changing the workflow.
- Validation: `python scripts/test-release-transaction.py` passed with 65 tests; `python scripts/validate-release.py --help` passed; `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=/tmp/rigorloop-release-output RELEASE_COMMIT=fixture-commit bash scripts/release-verify.sh v0.3.5` passed; Python compilation passed; selector validation selected `adapters.regression` and remained blocked only on known manual routing for release transaction scripts; the selected adapter/release regression command passed; lifecycle validation, review artifact validation, and whitespace validation passed.
- `code-review-m5-r1` requested changes for `CR-RTA-M5-F1`: timing validation exists as a helper but is not wired into the repository-owned release validation path.
- `CR-RTA-M5-F1` is resolved in review-resolution.
- `code-review-m5-r2` completed with no material findings. M5 is closed.
- Next action: implement M6.

### M6. Published evidence closeout and behavior preservation

- Milestone state: closed
- Goal: Add rerunnable public closeout generation from GitHub/npm/npx data, validate published evidence shape, and record behavior-preservation proof.
- Requirements: `R31`-`R38`, `R39`-`R44`, `AC12`-`AC18`, `AC20`
- Files/components likely touched:
  - `scripts/close-release-publication.py`
  - shared release-profile helper
  - `scripts/validate-release.py`
  - release evidence templates or fixtures
  - `docs/changes/2026-06-29-release-transaction-automation/behavior-preservation.md`
- Dependencies:
  - M3 pending evidence and M5 release-gate/timing behavior.
  - Test spec must choose fixture strategy for public GitHub/npm/npx evidence without requiring live publication in unit tests.
- Tests to add/update:
  - Public evidence unavailable fails clearly and modifies no unrelated files.
  - Generated published evidence uses validator-compatible `npx` command strings, `sha256:<hex>` tree hashes, root-qualified multi-root entries, file counts, archive status, and closeout blockers.
  - Fresh public smoke remains required for `version`, `init codex`, `init claude`, and `init opencode`.
  - Published evidence validation passes for fixture closeout.
  - Historical release evidence is not modified.
- Validation commands:
  - `python scripts/test-release-transaction.py`
  - `python scripts/close-release-publication.py <fixture-tag> --check` if implemented by the milestone
  - `python scripts/validate-release.py <fixture-tag> --phase published` or the test-spec-selected equivalent
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-29-release-transaction-automation/behavior-preservation.md --path docs/plans/2026-06-29-release-transaction-automation.md --path docs/plan.md --path docs/changes/2026-06-29-release-transaction-automation/change.yaml`
- Expected observable result: Post-publication evidence is generated from public data and accepted by validators without manual command/hash-shape churn.
- Commit message: `M6: generate published release evidence`
- Risks:
  - Live registry/network behavior could make tests slow or flaky if not fixture-isolated.
  - Closeout could accidentally mark pending evidence published before all public proof exists.
- Rollback/recovery:
  - Disable closeout generation and keep validator-compatible manual templates while preserving full release verification.

M6 implementation status:

- Added `scripts/close-release-publication.py` as a rerunnable closeout command. In default production mode it collects public evidence through closeout providers instead of accepting a local public-evidence file as proof. Explicit fixture mode remains available for tests/imports through `--fixture-mode --fixture-public-evidence`.
- Added closeout provider interfaces and a production provider in `scripts/release_transaction.py` for public GitHub release assets, npm registry package metadata, npm tarball metadata, and fresh public `npx` smoke.
- Added closeout helpers in `scripts/release_transaction.py` that validate provider-collected public GitHub asset rows, npm registry metadata, version smoke, and target init smoke before writing published evidence.
- Generated published `npm-publication.md` evidence records `Status: published`, npm package metadata, version smoke, per-target public archive URL, archive `sha256:<hex>`, tree hashes, file counts, archive/tree verification status, closeout blockers, and `post_publish_closeout_blocked: false`.
- Added published evidence validation and wired it into `scripts/validate-release.py` when `npm-publication.md` is marked `Status: published`.
- Added behavior-preservation proof at `docs/changes/2026-06-29-release-transaction-automation/behavior-preservation.md`.
- Test coverage: public evidence unavailable fails without modifying files; default closeout requests GitHub assets, npm metadata, public version smoke, and public init smoke for every profile target; valid provider closeout generates published evidence accepted by validators; manually supplied evidence is rejected in default mode; fixture mode is explicit; CLI `--check` reports the generated closeout path without writing in fixture mode; `npx -y` command shape is rejected; raw tree hash is rejected through helper and `validate-release.py`; missing target is rejected; historical `v0.3.4` evidence is unchanged.
- Unaffected aligned surface: `release-verify.sh` command set remains unchanged; it inherits published evidence validation through `validate-release.py` only after publication evidence is marked published.
- Validation: `python scripts/test-release-transaction.py` passed with 84 tests; `python scripts/close-release-publication.py --help` passed; Python compilation passed; `release-verify.sh` dry-run passed; selector validation selected adapter/release regression while remaining blocked on known manual routing for release transaction scripts; selected adapter/release regression passed. Lifecycle validation, review artifact validation, and whitespace validation passed after plan and review-resolution updates.
- `code-review-m6-r1` requested changes for `CR-RTA-M6-F1`: closeout currently validates a local public-evidence file but does not collect GitHub/npm metadata or run fresh public `npx` smoke as required by `R32` and `R33`.
- `CR-RTA-M6-F1` is resolved in review-resolution.
- `code-review-m6-r2` completed with no material findings. M6 is closed.
- `explain-change` recorded the implementation rationale in `docs/changes/2026-06-29-release-transaction-automation/explain-change.md`.
- `verify` recorded `docs/changes/2026-06-29-release-transaction-automation/verify-report.md` and blocked branch readiness because `bash scripts/ci.sh --mode explicit --path ...` reports selector manual-routing/unclassified-path blockers for the new release transaction scripts and fixture directories.
- CI maintenance added deterministic selector routing for release transaction scripts and fixtures through `release_transaction.regression`.
- `explain-change` refreshed `docs/changes/2026-06-29-release-transaction-automation/explain-change.md` to cover the CI-maintenance selector-routing diff.
- `verify` passed local branch-readiness checks and recorded branch-ready evidence in `docs/changes/2026-06-29-release-transaction-automation/verify-report.md`.
- A post-verify learn session recorded the CI-maintenance-before-explain-change routing lesson. Because this touched the change pack after verify, final verify must rerun before PR handoff.
- `verify` reran after the learn-session update, passed local branch-readiness checks, and refreshed `docs/changes/2026-06-29-release-transaction-automation/verify-report.md`.
- Next action: pr.

## Progress

- 2026-06-29: plan created after accepted proposal, approved spec-review, architecture-required assessment, accepted ADR, and clean architecture-review.
- 2026-06-29: plan-review-r1 approved the execution plan with no material findings; current next stage is `test-spec`.
- 2026-06-29: test spec authored at `specs/release-transaction-automation.test.md`; current next stage is `test-spec-review`.
- 2026-06-29: test-spec-review-r1 requested changes for RTA-TSR1 and RTA-TSR2; current next stage is `test-spec revision`.
- 2026-06-29: test spec revised to define proof-contract details and command ownership; test-spec-review-r2 approved implementation handoff; current next stage is `implement M1`.
- 2026-06-29: test-spec-review-r3 reran against the active test spec with no material findings; current next stage remains `implement M1`.
- 2026-06-29: M1 implementation started. Scope is limited to the release-profile loader/schema validator, profile fixtures, and focused release-transaction tests.
- 2026-06-29: M1 implementation added the shared release-profile loader, closed-vocabulary schema validation, profile path resolution for `docs/releases/profiles/<tag>.yaml`, and release profile fixtures. Current next stage is `code-review M1`.
- 2026-06-29: code-review-m1-r1 requested changes for `CR-RTA-M1-F1`; current next stage is `review-resolution M1`.
- 2026-06-29: review-resolution for `CR-RTA-M1-F1` added direct missing-profile-path and missing-required-field coverage for the M1 profile loader. Current next stage is `code-review M1`.
- 2026-06-29: code-review-m1-r2 completed cleanly with no material findings. M1 is closed; current next stage is `implement M2`.
- 2026-06-29: M2 implementation started. Scope is limited to release-prep surface ownership classification, literal-audit baseline classification, and focused release-transaction tests.
- 2026-06-29: M2 implementation added release surface inventory validation, literal-audit baseline validation, fixture coverage, and change-local inventory/baseline evidence. Current next stage is `code-review M2`.
- 2026-06-29: code-review-m2-r1 requested changes for `CR-RTA-M2-F1` and `CR-RTA-M2-F2`; current next stage is `review-resolution M2`.
- 2026-06-29: review-resolution for `CR-RTA-M2-F1` and `CR-RTA-M2-F2` added direct missing-classification fixture coverage for literal audit and surface inventory, and classified prior profile snapshots as historical immutable. Current next stage is `code-review M2`.
- 2026-06-29: code-review-m2-r2 completed cleanly with no material findings. M2 is closed; current next stage is `implement M3`.
- 2026-06-29: M3 implementation started. Scope is limited to fixture-safe `prepare-release` pending artifact generation, generated-region preservation, pending evidence shape proof, and the CLI wrapper.
- 2026-06-29: M3 implementation added a fixture-safe `prepare-release` generator, CLI wrapper, pending artifact shape validation helper, idempotency/narrative-preservation/historical-immutability tests, and check-mode proof. Current next stage is `code-review M3`.
- 2026-06-29: code-review-m3-r1 requested changes for `CR-RTA-M3-F1`. M3 remains in `resolution-needed` until pending-evidence validation rejects malformed target-specific placeholders and direct negative proof is added.
- 2026-06-29: review-resolution for `CR-RTA-M3-F1` added target-bound pending npm-publication validation and direct negative tests for published target result, `npx -y` command shape, missing target, duplicate target, unknown target, and table/YAML projection mismatch. Current next stage is `code-review M3`.
- 2026-06-29: code-review-m3-r2 completed cleanly with no material findings. M3 is closed; current next stage is `implement M4`.
- 2026-06-29: M4 implementation started. Scope is limited to Python-owned release preflight, cheap deterministic local/profile/schema checks, fixture-safe tag checks, and focused release transaction tests.
- 2026-06-29: M4 implementation added `scripts/release-preflight.py`, the shared `release_preflight` helper, package/profile and metadata pointer checks, pending evidence validation, literal-audit integration, release-output cleanliness checks, local tag conflict checks, reachable remote tag conflict checks, unreachable remote-state warnings, and focused tests. Current next stage is `code-review M4`.

## Decision log

- 2026-06-29: sequence profile schema before generators -> generators need a typed profile and closed vocabularies before routine surfaces can safely derive from it.
- 2026-06-29: sequence preflight after pending generation -> preflight should validate generated pending surfaces instead of inventing a parallel generation path.
- 2026-06-29: sequence public closeout last -> published evidence generation depends on stable profile parsing, pending evidence shape, release-gate preservation, and timing evidence.
- 2026-06-29: keep test logic hand-authored -> the spec allows generated fixture data and expected values, but generated test logic would reduce reviewability.
- 2026-06-29: M1 uses a Python-owned schema validator in `scripts/release_transaction.py` rather than a standalone schema file. This keeps the first slice executable by `python scripts/test-release-transaction.py`; later milestones can add schema export if generators need it.
- 2026-06-29: `scripts/validate-release.py` is unaffected in M1 because profile-backed generated-surface validation belongs to M2-M4. M1 only introduces the source-of-truth profile loader that later release validators can consume.
- 2026-06-29: M2 keeps release surface inventory and literal-audit baseline validation in `scripts/release_transaction.py` so M1-M2 release transaction proof stays in one focused command. Enforcement in preflight remains deferred to M4.
- 2026-06-29: M2 registers `release-surface-inventory.yaml` and `release-literal-audit-baseline.yaml` as exact change-evidence classes in the selector. This removes deterministic evidence-registration debt while keeping release transaction script and fixture routing manually owned by `python scripts/test-release-transaction.py`.
- 2026-06-29: M3 keeps `prepare-release` generation in `scripts/release_transaction.py` with a thin `scripts/prepare-release.py` wrapper. The first slice validates generated pending release artifacts with a release-transaction helper because existing `scripts/validate-release.py` has no `--phase pre-publication` fixture mode.
- 2026-06-29: M3 pending npm-publication validation treats the generated YAML block as canonical and validates the Markdown table as a projection of that structured target data. This keeps pending evidence checks target-bound while preserving the generated evidence file shape.
- 2026-06-29: M4 keeps preflight side-effect-light and local by default. Remote tag checks use repository-configured `origin` only when reachable; unreachable remote tag state is a warning, not a silent pass or a hard local blocker.

## Surprises and discoveries

- The validation selector does not yet classify the new release transaction scripts or fixtures, so M1 uses the approved command matrix validation plus lifecycle/change-metadata checks instead of a selector-owned script check.
- `docs/releases/profiles/` does not yet exist for a live release. M3 uses temporary repository fixtures with `docs/releases/profiles/v0.3.5.yaml` so the generator contract is proven without creating a real release profile or publishing release artifacts.

## Validation notes

- Test-spec-review-r3 approved the active proof map before implementation.
- 2026-06-29: `python scripts/test-release-transaction.py` failed before implementation with `ModuleNotFoundError: No module named 'release_transaction'`, proving the new focused tests were not passing without the M1 helper.
- 2026-06-29: `python scripts/test-release-transaction.py` passed after implementation: 10 tests.
- 2026-06-29: `python scripts/test-release-transaction.py` passed after `CR-RTA-M1-F1` resolution: 11 tests.
- 2026-06-29: `python scripts/validate-release.py --help` passed and confirmed the existing release validator CLI remains available.
- 2026-06-29: `python scripts/select-validation.py --mode explicit ...` reported manual routing for the new script and fixture paths; the M1-specific test command above owns those paths for this milestone.
- 2026-06-29: `python scripts/test-change-metadata-validator.py` passed: 43 tests.
- 2026-06-29: `python scripts/validate-change-metadata.py docs/changes/2026-06-29-release-transaction-automation/change.yaml` passed.
- 2026-06-29: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-29-release-transaction-automation/change.yaml --path docs/plans/2026-06-29-release-transaction-automation.md --path docs/plan.md` initially caught a structured `Review status` format issue, then passed after the plan field was restored to the validator-owned shape.
- 2026-06-29: `git diff --check -- ...` passed for M1 implementation, plan, plan index, and change-metadata paths.
- 2026-06-29: `python scripts/validate-release.py --help` passed after `CR-RTA-M1-F1` resolution.
- 2026-06-29: `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/test-release-transaction.py --path tests/fixtures/release-transaction/profiles` reported manual routing for the new script and fixture family; the M1-specific focused test remains the owner for those paths.
- 2026-06-29: `python scripts/validate-change-metadata.py docs/changes/2026-06-29-release-transaction-automation/change.yaml` passed after `CR-RTA-M1-F1` resolution.
- 2026-06-29: `python scripts/validate-review-artifacts.py docs/changes/2026-06-29-release-transaction-automation/` passed after `CR-RTA-M1-F1` resolution.
- 2026-06-29: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-29-release-transaction-automation.md --path docs/plan.md --path docs/changes/2026-06-29-release-transaction-automation/change.yaml --path docs/changes/2026-06-29-release-transaction-automation/review-log.md --path docs/changes/2026-06-29-release-transaction-automation/review-resolution.md` passed after `CR-RTA-M1-F1` resolution.
- 2026-06-29: `git diff --check --` and `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py` passed after `CR-RTA-M1-F1` resolution.
- 2026-06-29: `python scripts/test-release-transaction.py` passed after M2 implementation: 21 tests.
- 2026-06-29: `python scripts/select-validation.py --mode explicit ...` classified M2 change-local evidence as registered and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression`; it still reported manual routing for the new release transaction script and fixture directories.
- 2026-06-29: `python scripts/test-select-validation.py` passed after M2 selector evidence-class registration: 123 tests.
- 2026-06-29: `python scripts/test-change-metadata-validator.py`, `python scripts/validate-guide-system.py`, and selected artifact lifecycle validation passed during M2 validation.
- 2026-06-29: `python scripts/test-release-transaction.py` passed after M2 review-resolution: 23 tests.
- 2026-06-29: `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/test-release-transaction.py --path tests/fixtures/release-transaction/surface-inventory --path tests/fixtures/release-transaction/literal-audit --path docs/changes/2026-06-29-release-transaction-automation/release-surface-inventory.yaml --path docs/changes/2026-06-29-release-transaction-automation/release-literal-audit-baseline.yaml` reported manual routing for release transaction script and fixture paths and selected `artifact_lifecycle.validate` for registered release transaction evidence.
- 2026-06-29: `python scripts/validate-change-metadata.py docs/changes/2026-06-29-release-transaction-automation/change.yaml`, `python scripts/validate-review-artifacts.py docs/changes/2026-06-29-release-transaction-automation/`, and `git diff --check --` passed after M2 review-resolution updates.
- 2026-06-29: `python scripts/test-release-transaction.py` failed at the start of M3 with `ImportError: cannot import name 'prepare_release'`, proving the new M3 tests were not passing before generator implementation.
- 2026-06-29: `python scripts/test-release-transaction.py` passed after M3 implementation: 28 tests.
- 2026-06-29: `python scripts/prepare-release.py --help` passed after adding the CLI wrapper.
- 2026-06-29: `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/test-release-transaction.py --path scripts/prepare-release.py` reported manual routing for release transaction script paths and initially reported the new `scripts/prepare-release.py` as untracked before staging.
- 2026-06-29: `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py`, `python scripts/validate-change-metadata.py docs/changes/2026-06-29-release-transaction-automation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-29-release-transaction-automation.md --path docs/plan.md --path docs/changes/2026-06-29-release-transaction-automation/change.yaml --path docs/changes/2026-06-29-release-transaction-automation/review-log.md --path docs/changes/2026-06-29-release-transaction-automation/review-resolution.md`, and `git diff --check --` passed after M3 implementation.
- 2026-06-29: `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/test-release-transaction.py --path scripts/prepare-release.py` reported manual routing for the release transaction scripts after staging; tracked-authoritative-artifacts preflight passed.
- 2026-06-29: `python scripts/test-release-transaction.py` failed after adding `CR-RTA-M3-F1` negative tests, proving the existing fragment-based pending evidence validator still accepted invalid target-specific evidence.
- 2026-06-29: `python scripts/test-release-transaction.py` passed after `CR-RTA-M3-F1` resolution: 34 tests.
- 2026-06-29: `python scripts/prepare-release.py --help`, `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py`, and `git diff --check --` passed after `CR-RTA-M3-F1` resolution.
- 2026-06-29: `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/prepare-release.py --path scripts/test-release-transaction.py --path tests/fixtures/release-transaction/evidence` reported manual routing for release transaction scripts and an unclassified static evidence fixture path. The `CR-RTA-M3-F1` resolution uses temporary generated repository fixtures in `python scripts/test-release-transaction.py`, so no static `tests/fixtures/release-transaction/evidence` files were added.
- 2026-06-29: `python scripts/test-release-transaction.py` failed at the start of M4 with `ImportError: cannot import name 'release_preflight'`, proving the new M4 tests were not passing before preflight implementation.
- 2026-06-29: `python scripts/test-release-transaction.py` passed after M4 implementation: 45 tests.
- 2026-06-29: `python scripts/release-preflight.py --help`, `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py scripts/release-preflight.py`, and `git diff --check --` passed after M4 implementation.
- 2026-06-29: `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/release-preflight.py --path scripts/test-release-transaction.py` initially blocked because `scripts/release-preflight.py` was untracked, then after staging reported manual routing for release transaction scripts with tracked-authoritative-artifacts preflight passed.
- Final implementation verification should include review artifact validation, change metadata validation, lifecycle explicit-path validation, selected release tooling tests, and release-gate preservation checks.

## Outcome and retrospective

- M1 implementation is review-requested. Keep this section historical until all implementation milestones and final closeout are complete.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- Profile generation can become another source of drift unless unauthorized current-version literals fail or report as baseline debt.
- Public closeout must be fixture-testable without requiring live publication in normal unit tests.
- Release timing should be captured as evidence before hard duration budgets or parallelism are proposed.
- A follow-up proposal may cover release-gate parallelism after several timing records exist.
- A follow-up proposal may cover background publication monitoring after rerunnable closeout is stable.
