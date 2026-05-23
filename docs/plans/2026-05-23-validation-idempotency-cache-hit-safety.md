# Validation Idempotency and Cache-Hit Safety Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Start date: 2026-05-23
- Last updated: 2026-05-23
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved first slice for validation idempotency without changing validation semantics or closeout gates. The work must allow cache hits only for unchanged `validate-artifact-lifecycle.py --mode explicit-paths` inputs after a previous pass, keep local cache state non-portable and non-evidence, record formal cache-hit and measurement evidence in change-local YAML, and mechanically reject cache-only closeout claims.

The plan keeps Workstream B out of scope. Changed-path or edit-class validator narrowing remains blocked until Workstream A measurement is recorded, reviewed, and authorized by a separate proposal or spec amendment.

## Source artifacts

- Proposal: `docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md`
- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Architecture: `docs/architecture/system/architecture.md`
- Container diagram: `docs/architecture/system/diagrams/container.mmd`
- ADR: `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`
- Test spec: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Proposal reviews: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/proposal-review-r1.md`, `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/proposal-review-r2.md`
- Spec reviews: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/spec-review-r1.md`, `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/spec-review-r2.md`
- Architecture review: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md`

## Context and orientation

- `scripts/validate-artifact-lifecycle.py` is the first and only cache-eligible validator command family, and only in `--mode explicit-paths`.
- `scripts/artifact_lifecycle_validation.py` owns the artifact lifecycle validation implementation used by the CLI wrapper.
- A new cache helper module is expected to own command normalization, repository-relative path normalization, input-surface hashing, deterministic implementation and policy manifests, local cache key decisions, evidence record helpers, and measurement helpers.
- `scripts/validate-change-metadata.py` owns compact `schema_version: 2` validation metadata checks and must reject invalid `evidence_kind` and `evidence_ref` claims.
- `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh` own changed-path routing. New deterministic evidence files under `docs/changes/<change-id>/` need selector coverage before verify.
- Existing validation behavior, selected checks, failure detection, and exit semantics remain authoritative when the validator actually runs.
- Local execution cache state is an optimization surface only. It is untracked, branch-local, worktree-local, change-local, and non-portable.
- Formal workflow cache-hit evidence lives at `docs/changes/<change-id>/validation-cache-evidence.yaml`; Workstream A measurement lives at `docs/changes/<change-id>/validation-cache-measurement.yaml`.
- `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/` is the change-local evidence root for this initiative.

## Non-goals

- Do not implement edit-scoped validation or changed-path validator narrowing.
- Do not cache validators other than `validate-artifact-lifecycle.py --mode explicit-paths`.
- Do not cache-skip stage or milestone closeout full bundles.
- Do not add remote, shared, cross-branch, cross-worktree, cross-machine, or CI cache reuse.
- Do not change what `validate-artifact-lifecycle.py` checks when it actually runs.
- Do not change validator exit semantics when the validator actually runs.
- Do not reuse failed, blocked, skipped, not-run, missing, or unknown prior results as passes.
- Do not make untracked local cache state lifecycle evidence.
- Do not require every historical change record to adopt cache-hit evidence files.

## Requirements covered

- R1 through R31: M1 and M2.
- R32 through R59: M2 and M3.
- R60 through R72: M1 and M2.
- R73 through R77: all implementation milestones and M5.
- R78 through R100: M1.
- R101 through R116: M3.
- R117 through R130: M4.
- AC1 through AC7: M1 and M2.
- AC8 through AC10: M2 and M4.
- AC11 through AC14: M3.
- AC15: M1 and M2.
- AC16 through AC18: all implementation milestones and M5.
- AC19 through AC23: M1.
- AC24 through AC28: M3.
- AC29 through AC32: M4.

## Current Handoff Summary

- Current milestone: M1. Cache identity primitives and local cache contract
- Current milestone state: resolution-needed
- Last reviewed milestone: M0. Plan-review and test-spec handoff
- Review status: `code-review-m1-r1` requested changes for `VIC-CR-M1-R1-F1`; `plan-review-r1` approved the plan with no material findings; test-spec is active.
- Remaining in-scope implementation milestones: M1 pending review-resolution; M2, M3, and M4 remain planned.
- Next stage: review-resolution M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 has an open code-review finding, M2 through M4 are not implemented or reviewed, final validation has not run, explain-change and verify are not recorded, and PR handoff is not prepared.

## Milestones

### M0. Plan-review and test-spec handoff

- Milestone state: closed
- Goal: Review this plan, resolve any sequencing findings, then create the focused test spec before implementation starts.
- Requirements: R1 through R130; AC1 through AC32.
- Files/components likely touched:
  - `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`
  - `docs/plan.md`
  - `specs/validation-idempotency-and-cache-hit-safety.test.md` after plan-review
  - `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/`
- Dependencies:
  - Accepted proposal.
  - Approved spec.
  - Approved architecture-review.
- Tests to add/update:
  - None in this milestone; the test-spec is the next lifecycle artifact after plan-review.
- Implementation steps:
  - Run plan-review against this plan.
  - Resolve any material plan-review findings before test-spec.
  - Create `specs/validation-idempotency-and-cache-hit-safety.test.md` after plan-review approval.
  - Ensure the test spec maps every spec `MUST` to cache-key, invalidation, metadata, closeout, measurement, selector, and behavior-preservation proof.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md --path docs/plan.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/architecture-review-r1.md`
  - `git diff --check -- docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md docs/plan.md docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later`
- Expected observable result: plan-review can approve or challenge concrete sequencing, and test-spec has a clear downstream scope.
- Commit message: `M0: plan validation cache-hit safety`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Starting implementation before test-spec exists could miss invalidation, evidence, or closeout edge cases.
- Rollback/recovery:
  - Keep implementation blocked and revise the plan, spec, or architecture if plan-review finds an uncovered contract gap.

### M1. Cache identity primitives and local cache contract

- Milestone state: resolution-needed
- Goal: Add deterministic cache-key primitives and local-cache eligibility tests without integrating cache skipping into the validator yet.
- Requirements: R1 through R31, R60 through R72, R78 through R100; AC1 through AC7, AC15, AC19 through AC23.
- Files/components likely touched:
  - `scripts/validation_cache.py`
  - `scripts/test-validation-cache.py`
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `tests/fixtures/validation-cache/**`
  - `.gitignore` if the local cache directory needs an explicit ignored path
- Dependencies:
  - Approved plan-review.
  - Approved test spec.
- Tests to add/update:
  - Normalized argv vector hashing uses canonical JSON and preserves order.
  - Repository-relative path normalization rejects absolute paths, home paths, URLs, hostnames, credentials, Windows absolute paths, repository escapes, and unsafe environment-like path values.
  - Explicit `--path` order affects the command hash.
  - Duplicate explicit paths disable cache eligibility.
  - Input-surface hashing includes content hashes and missing-file markers.
  - Implementation manifest hashing includes the validator entrypoint, repository-local imports/helpers, and manifest-generation logic.
  - Policy/config manifest hashing includes declared policy/spec/config files and missing-file markers.
  - Branch, worktree, and change ID mismatches make local cache entries ineligible.
  - Selector routing maps the new validation cache helper and regression test to `validation_cache.regression`.
- Implementation steps:
  - Add a focused cache helper module for normalization, manifest construction, hashing, local cache record shape, and eligibility decisions.
  - Use content hashes rather than timestamps.
  - Treat unresolved implementation or policy manifests as cache-disabled, not as a pass.
  - Keep local cache state untracked and non-portable. If a new directory is used, add it to `.gitignore`.
  - Avoid changing validator execution behavior in this milestone.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
  - `git diff --check --`
- Expected observable result: cache identity and invalidation primitives are fixture-backed and reusable by the lifecycle validator without changing existing validator behavior.
- Commit message: `M1: add validation cache identity primitives`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Import graph discovery could miss a repository-local helper and allow stale cache hits.
  - Local cache path selection could accidentally create tracked state.
- Rollback/recovery:
  - Disable cache helper use and remove ignored local-cache state; existing validators should still run normally.

### M2. Explicit-path lifecycle cache integration and cache-hit evidence

- Milestone state: planned
- Goal: Wire cache lookup and prior-pass recording into `validate-artifact-lifecycle.py --mode explicit-paths` while preserving actual-run behavior and producing reviewable cache-hit evidence only when formal workflow claims cite a skip.
- Requirements: R1 through R17, R32 through R50, R56, R60 through R77; AC1 through AC10, AC13, AC15, AC16, AC18.
- Files/components likely touched:
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validation_cache.py`
  - `scripts/test-validation-cache.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/validation-cache/**`
  - `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/behavior-preservation.md`
- Dependencies:
  - M1 cache primitives.
  - Test spec covers cache hit, cache miss, prior failure, and actual-run preservation cases.
- Tests to add/update:
  - First eligible run executes the validator and records a passing local cache entry.
  - Repeated identical command with matching hashes can produce bounded `[CACHE HIT]` output.
  - Changed explicit input, changed helper, changed policy, failed prior result, branch/worktree/change mismatch, unsupported mode, or closeout context runs the validator.
  - Cache hits do not change exit semantics or failure detection when an actual run is required.
  - Formal cache-hit evidence, when requested by workflow context, writes `validation-cache-evidence.yaml` with required fields and without unsafe local data.
- Implementation steps:
  - Integrate cache eligibility only for `--mode explicit-paths`.
  - Ensure unsupported modes and uncertain manifests bypass cache and run normally.
  - Persist only prior passing results to local cache.
  - Emit bounded cache-hit output that names validator ID, prior passing event or local record, short key/hash, and unchanged-input reason.
  - Add an explicit workflow evidence path for writing or updating `validation-cache-evidence.yaml` when formal cache-hit evidence is requested; do not require local cache state as formal evidence.
  - Record behavior-preservation proof for pass and fail behavior when the validator actually runs.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
  - `git diff --check --`
- Expected observable result: repeated unchanged explicit-path lifecycle validation can skip through a cache hit, while every uncertain or changed condition falls back to actual validation.
- Commit message: `M2: add lifecycle validation cache hits`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - A cache hit could be mistaken for a new pass if output or evidence wording is loose.
  - Formal evidence writing could expose machine-local state if helper boundaries are not strict.
- Rollback/recovery:
  - Disable cache reads and force actual validation; retain historical cache-hit evidence only as inner-loop evidence.

### M3. Compact metadata evidence-kind and closeout enforcement

- Milestone state: planned
- Goal: Enforce the compact `schema_version: 2` evidence-kind contract and reject cache-only closeout claims through lifecycle and change-metadata validators.
- Requirements: R50 through R59, R101 through R116; AC11 through AC14, AC24 through AC28.
- Files/components likely touched:
  - `scripts/validate-change-metadata.py`
  - `scripts/change_metadata_semantics.py` if shared metadata helpers are needed
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/change-metadata/**`
  - `tests/fixtures/artifact-lifecycle/**`
- Dependencies:
  - M2 cache-hit evidence shape is known.
  - Test spec covers compact and legacy metadata behavior.
- Tests to add/update:
  - Compact `actual-run-pass` with `result: pass` can satisfy closeout when the required bundle is covered.
  - Compact `cache-hit-inner-loop` with `result: pass` is valid only as inner-loop/supporting evidence and invalid as closeout.
  - Invalid result/evidence-kind pairings fail with stable diagnostics.
  - Unsafe or unresolved `evidence_ref` values fail.
  - Legacy metadata remains valid but fails if it attempts to claim cache-hit or closeout semantics with `evidence_kind` or `evidence_ref`.
  - `validate-change-metadata.py` rejects `change.yaml` entries that promote cache hits into closeout passes.
  - `validate-artifact-lifecycle.py` rejects closeout records represented only by cache-hit evidence.
- Implementation steps:
  - Add compact metadata evidence-kind validation and safe `evidence_ref` validation.
  - Add closeout-specific rejection for cache-only evidence.
  - Keep existing legacy metadata valid except for attempts to use the new evidence-kind fields.
  - Keep diagnostics stable and specific enough for fixture assertions.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later`
  - `git diff --check --`
- Expected observable result: closeout actual-run gates are mechanically enforced and cache-hit evidence cannot be relabeled into closeout success.
- Commit message: `M3: enforce cache-hit evidence closeout rules`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - New compact metadata checks could reject valid legacy change records if legacy compatibility is too broad.
  - Closeout detection could become too heuristic if it is not tied to explicit compact fields.
- Rollback/recovery:
  - Revert the new evidence-kind enforcement while preserving legacy validation; cache hits must then remain disabled until mechanical closeout enforcement returns.

### M4. Measurement evidence, selector routing, and implementation closeout

- Milestone state: planned
- Goal: Validate Workstream A measurement evidence, register deterministic cache evidence routing, record this change's measurement/behavior evidence, and prepare implementation handoff for final code review.
- Requirements: R32 through R48, R75 through R77, R117 through R130; AC8 through AC10, AC17, AC18, AC29 through AC32.
- Files/components likely touched:
  - `scripts/validate-change-metadata.py`
  - `scripts/validation_selection.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/test-select-validation.py`
  - `tests/fixtures/change-metadata/**`
  - `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/validation-cache-measurement.yaml`
  - `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/validation-cache-evidence.yaml` if formal cache-hit evidence is produced during the slice
  - `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/behavior-preservation.md`
- Dependencies:
  - M2 cache-hit evidence shape.
  - M3 compact metadata evidence-kind enforcement.
- Tests to add/update:
  - Measurement file required fields and enum values validate.
  - Negative counts, impossible count relationships, unsafe values, invalid Workstream B state, missing follow-up rationale, and `closeout_cache_skips > 0` fail.
  - `validation-cache-evidence.yaml` and `validation-cache-measurement.yaml` route through selected validation rather than `manual-routing-required`.
  - Workstream B remains unimplemented and unselectable under this spec.
  - This branch's actual changed-path selector proof includes the new evidence files when present.
- Implementation steps:
  - Add measurement validation using existing metadata parser/helper patterns.
  - Add selector routing for validation cache evidence and measurement evidence.
  - Record behavior-preservation evidence showing actual-run behavior remains unchanged.
  - Record Workstream A measurement evidence for the implementation loop.
  - Confirm no Workstream B selector or runtime behavior was introduced.
  - Update plan progress, validation notes, and current handoff after implementation validation.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode local`
  - `bash scripts/ci.sh --mode local`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later`
  - `git diff --check --`
- Expected observable result: formal cache-hit and measurement evidence are validated and routed, Workstream A measurement exists, and the branch is ready to request final code-review for the implementation milestones.
- Commit message: `M4: add validation cache measurement evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Measurement evidence could be treated as authorization for Workstream B instead of an input to a later proposal.
  - Selector routing could accidentally broaden all change-local YAML handling.
- Rollback/recovery:
  - Disable measurement/evidence routing and require manual explicit validation until bounded routing is fixed; do not proceed to verify with `manual-routing-required` debt.

### M5. Lifecycle closeout

- Milestone state: planned
- Goal: Complete downstream closeout after all implementation milestones are closed.
- Requirements: R73 through R77; AC16 through AC18, AC32.
- Files/components likely touched:
  - `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/explain-change.md`
  - `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/verify-report.md` if verify records a standalone report
  - PR handoff artifacts when created
- Dependencies:
  - M1 through M4 closed.
  - Required code-review outcomes closed.
  - Required review-resolution closed if material findings occurred.
- Tests to add/update:
  - None unique to this milestone; it proves final coherence across the implemented tests and artifacts.
- Implementation steps:
  - Run required code-review loops for each implementation milestone.
  - Resolve material findings before final closeout.
  - Run `explain-change`.
  - Run `verify`.
  - Prepare PR handoff only after verification passes.
  - Keep the plan active until PR readiness and final lifecycle state are explicitly recorded.
- Validation commands:
  - `bash scripts/ci.sh --mode local`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md --path docs/plan.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
  - `git diff --check --`
- Expected observable result: all implementation milestones are closed, final validation passes, explain-change and verify evidence are current, and PR handoff can proceed.
- Commit message: `M5: close validation cache-hit safety plan`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Final closeout could accidentally treat cache-hit evidence as closeout pass evidence.
  - Plan index and plan body could drift during final state changes.
- Rollback/recovery:
  - Keep the plan active and block PR handoff until lifecycle state, validation evidence, and review-resolution records are synchronized.

## Validation plan

- `python scripts/test-validation-cache.py`: proves cache normalization, keying, local-cache eligibility, evidence, and measurement helper behavior.
- `python scripts/test-artifact-lifecycle-validator.py`: proves lifecycle validator integration, fallback-to-run behavior, closeout rejection ownership, and behavior preservation.
- `python scripts/test-change-metadata-validator.py`: proves compact metadata evidence-kind, evidence reference, measurement, and legacy compatibility behavior.
- `python scripts/test-select-validation.py`: proves deterministic routing for new cache evidence files and avoids `manual-routing-required`.
- `python scripts/select-validation.py --mode local`: proves the branch's actual changed paths are routed before verify.
- `bash scripts/ci.sh --mode local`: runs selected checks for the actual branch state before final closeout.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`: validates change-local metadata.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later`: validates review artifact recording and closeout.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: validates lifecycle-managed artifacts touched by each milestone.
- `git diff --check --`: catches whitespace errors.

## Risks and recovery

- Risk: incomplete implementation manifest causes stale cache hits.
  - Recovery: disable caching when manifest generation is uncertain and keep helper-module invalidation tests as blocking.
- Risk: cache-hit evidence is mistaken for a new pass or closeout pass.
  - Recovery: keep `cache-hit-inner-loop` separate from `actual-run-pass`, reject cache-only closeout, and preserve actual-run closeout validation.
- Risk: local cache state leaks machine-specific data into tracked evidence.
  - Recovery: keep local state untracked and validate tracked evidence against absolute paths, usernames, hostnames, credentials, secrets, and environment dumps.
- Risk: selector routing for new evidence files is too broad.
  - Recovery: add exact or bounded evidence-class routing tests and reject ambiguous or broad patterns.
- Risk: Workstream B behavior slips into Workstream A implementation.
  - Recovery: keep changed-path narrowing and edit-class selection out of runtime behavior and require a separate proposal or spec amendment.

## Dependencies

- Plan-review must approve this plan before test-spec.
- Test-spec must be created and approved before implementation.
- M1 cache primitives must land before lifecycle integration in M2.
- M2 cache-hit evidence shape must land before M3/M4 validation and routing can rely on it.
- M3 closeout enforcement must land before final measurement/closeout can safely cite cache-hit evidence.
- M4 measurement and selector routing must complete before explain-change, verify, and PR handoff.

## Progress

- 2026-05-23: Plan created after proposal, spec, architecture, and architecture-review approval.
- 2026-05-23: Initial plan validation passed; ready for plan-review.
- 2026-05-23: Plan-review R1 approved the plan with no material findings; test-spec created and active; M0 closed and next stage is implement M1.
- 2026-05-23: M1 implementation started for cache identity primitives and local cache contract.
- 2026-05-23: M1 added `scripts/validation_cache.py` and `scripts/test-validation-cache.py` for cacheable command-family detection, deterministic argv and path normalization, input-surface manifests, implementation and policy manifests, and branch/worktree/change-local cache eligibility. No validator cache skipping was integrated in M1.
- 2026-05-23: M1 added selector routing for `scripts/validation_cache.py` and `scripts/test-validation-cache.py` so selected CI runs `validation_cache.regression` instead of blocking on `manual-routing-required`.
- 2026-05-23: M1 direct validation passed and the milestone is ready for code-review.
- 2026-05-23: Code-review M1 R1 recorded `VIC-CR-M1-R1-F1`; M1 needs review-resolution for unresolved implementation-manifest handling before it can close.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-23 | Split implementation into cache primitives, lifecycle integration, metadata closeout enforcement, and measurement/routing. | The spec spans cache identity, validator execution, formal evidence, closeout semantics, and measurement; separating those concerns keeps review slices bounded. | One broad implementation milestone that mixes cache helpers, validators, metadata, selector routing, and measurement. |
| 2026-05-23 | Keep Workstream B out of all implementation milestones. | The approved spec blocks edit-scoped validation until Workstream A measurement is reviewed and separate authorization exists. | Adding diff-derived selector narrowing during cache implementation. |

## Surprises and discoveries

- M1 did not need a local cache directory, so no `.gitignore` change was required.
- Selected CI initially blocked on the new cache script paths; M1 added a narrow `validation-cache` selector category and regression route to avoid carrying known validation debt.

## Validation notes

- 2026-05-23: `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml` passed.
- 2026-05-23: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed.
- 2026-05-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md --path docs/plan.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/architecture-review-r1.md` passed.
- 2026-05-23: `git diff --check -- docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md docs/plan.md docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed.
- 2026-05-23: `bash scripts/ci.sh --mode explicit ...` passed selected checks `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-23: `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml` passed after test-spec authoring.
- 2026-05-23: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed after test-spec authoring.
- 2026-05-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md --path docs/plan.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/plan-review-r1.md` passed.
- 2026-05-23: `git diff --check -- specs/validation-idempotency-and-cache-hit-safety.test.md docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md docs/plan.md docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed.
- 2026-05-23: `bash scripts/ci.sh --mode explicit ...` passed selected checks `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` after test-spec authoring.
- 2026-05-23: `python scripts/test-validation-cache.py` passed for M1 cache identity primitives.
- 2026-05-23: `python scripts/test-artifact-lifecycle-validator.py` passed for existing lifecycle validator behavior after adding M1 helper code.
- 2026-05-23: `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml` passed after M1 implementation.
- 2026-05-23: `python scripts/test-select-validation.py` passed after adding `validation_cache.regression` selector routing.
- 2026-05-23: `bash scripts/ci.sh --mode explicit --path scripts/validation_cache.py --path scripts/test-validation-cache.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md --path docs/plan.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path specs/validation-idempotency-and-cache-hit-safety.test.md --path specs/validation-idempotency-and-cache-hit-safety.md` passed selected checks `artifact_lifecycle.validate`, `validation_cache.regression`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- 2026-05-23: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed after recording code-review M1 R1.
- 2026-05-23: `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml` passed after recording code-review M1 R1.
- 2026-05-23: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md --path docs/plan.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/code-review-m1-r1.md` passed after recording code-review M1 R1.
- 2026-05-23: `git diff --check -- docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md docs/plan.md docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed after recording code-review M1 R1.

## Outcome and retrospective

- Pending completion.

## Readiness

- See `Current Handoff Summary`.
- Ready for code-review M1. M2, M3, M4, explain-change, verify, PR readiness, and final closeout remain incomplete.
- Ready for review-resolution M1. M2, M3, M4, explain-change, verify, PR readiness, and final closeout remain incomplete.
