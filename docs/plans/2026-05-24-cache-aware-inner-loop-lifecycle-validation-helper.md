# Cache-Aware Inner-Loop Lifecycle Validation Helper Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Start date: 2026-05-24
- Last updated: 2026-05-24
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved cache-aware inner-loop lifecycle validation helper without broadening validation cache eligibility or weakening closeout. The work makes the safe repeated inner-loop path short and explicit through `validate-artifact-lifecycle.py --mode explicit-paths-inner-loop`, while preserving direct `--mode explicit-paths` actual-run validation for closeout, verify, branch readiness, PR readiness, and CI.

The plan keeps the helper inside the existing validation-cache architecture. It must normalize helper cache identity to canonical direct `--mode explicit-paths` argv, record both displayed and canonical argv in formal helper evidence, fall back to actual validation on uncertainty, reject helper cache hits as closeout proof, keep CI actual-run, and record helper-specific measurement before any future cache expansion proposal.

## Source artifacts

- Proposal: `docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`
- Test spec: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Proposal review: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/proposal-review-r1.md`
- Spec reviews: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/spec-review-r1.md`, `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/spec-review-r2.md`
- Architecture review: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md`
- Review resolution: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
- Change metadata: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`

## Context and orientation

- `scripts/validate-artifact-lifecycle.py` already owns lifecycle validation modes and the existing opt-in validation-cache flags.
- `scripts/validation_cache.py` already owns command normalization, explicit-path input-surface identity, implementation/policy manifests, local cache lookup, cache-hit evidence writing, and cache measurement helpers.
- Current cache eligibility is direct `--mode explicit-paths` with explicit cache flags. The helper must make the common inner-loop shape easy without making direct actual-run closeout cache-aware by default.
- Helper cache identity must normalize to the canonical direct `--mode explicit-paths` command. Formal helper evidence must preserve the user-invoked helper command separately as `displayed_command_argv`.
- Direct `--mode explicit-paths` remains the required actual-run command for closeout, verify, branch readiness, PR readiness, and CI.
- `scripts/validate-change-metadata.py` and `scripts/validate-artifact-lifecycle.py` own closeout rejection for cache-only or helper-only pass claims.
- `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh` own changed-path routing. New deterministic evidence files need registered selector routes before verify.
- Published skills must not expose RigorLoop-internal validator commands. Any validation command examples must remain in repository-local plan/test evidence surfaces, not shipped public skill text.

## Non-goals

- Do not cache validators outside the explicit-path lifecycle command family.
- Do not cache `validate-change-metadata.py`, `validate-review-artifacts.py`, selected CI, broad smoke, npm tests, release checks, GitHub metadata, external-state proof, generated-output verification, or unlisted validators.
- Do not make direct `--mode explicit-paths` cache-aware by default.
- Do not use the helper in CI.
- Do not let helper cache hits satisfy closeout, verify, branch-readiness, PR-readiness, release, or CI evidence.
- Do not change validator pass/fail semantics, selected checks, exit codes, or failure detection.
- Do not introduce a wrapper script in the first slice.
- Do not implement edit-scoped validation or changed-path validator narrowing.
- Do not expose repository-internal cache commands in published skills.

## Requirements covered

- R1-R3, R131-R138, AC33-AC35, AC41-AC42, AC48-AC49: M1 and M2.
- R6-R17, R38a-R40, R78-R100, R133a-R133g, AC35, AC46-AC47: M1 and M2.
- R32-R50, R145-R149, AC37-AC39: M2.
- R50-R59, R101-R116, R150-R151, AC11-AC14, AC24-AC28, AC40: M3.
- R117-R130, R157-R159, AC29-AC32, AC45, AC50: M4.
- R152-R154, AC44: M4.
- R155-R156, AC43: M5.
- R73-R77, R139-R144, AC16, AC18, AC36: all implementation milestones and final closeout.

## Current Handoff Summary

- Current milestone: M5. Repository-local guidance and behavior-preservation evidence
- Current milestone state: review-requested
- Last reviewed milestone: M4 measurement schema and selector routing
- Review status: M5 implemented with targeted validation passing; ready for code-review M5.
- Remaining in-scope implementation milestones: M5, M6.
- Next stage: code-review M5
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M5 is implemented but not reviewed; M6, explain-change, verify, and PR handoff remain.

## Milestones

### M0. Plan-review and test-spec handoff

- Milestone state: closed
- Goal: Review this plan, resolve any sequencing findings, then amend the validation-idempotency test spec before implementation starts.
- Requirements: all helper amendment requirements and acceptance criteria.
- Files/components likely touched:
  - `docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
  - `docs/plan.md`
  - `specs/validation-idempotency-and-cache-hit-safety.test.md`
  - `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/`
- Dependencies:
  - Accepted proposal.
  - Approved spec.
  - Approved architecture-review.
- Tests to add/update:
  - None in this milestone; test-spec is the next lifecycle artifact after plan-review.
- Implementation steps:
  - Run plan-review against this plan.
  - Resolve any material plan-review findings before test-spec.
  - Amend `specs/validation-idempotency-and-cache-hit-safety.test.md` after plan-review approval.
  - Ensure the test spec covers helper normalization, evidence shape, fallback behavior, closeout rejection, selector routing, measurement consistency, and published-skill non-exposure.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/architecture-review-r1.md`
  - `git diff --check -- docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md docs/plan.md docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
- Expected observable result: plan-review can approve or challenge concrete sequencing, and test-spec has a complete downstream scope.
- Commit message: `M0: plan cache-aware lifecycle helper`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Starting implementation before test-spec would risk missing closeout, measurement, or selector-routing edge cases.
- Rollback/recovery:
  - Keep implementation blocked and revise the plan, spec, or architecture if plan-review finds an uncovered contract gap.

### M1. Helper mode and canonical identity tests

- Milestone state: closed
- Goal: Add failing tests and cache-identity support for `--mode explicit-paths-inner-loop` without changing closeout semantics.
- Requirements: R1-R3, R6-R17, R38a-R40, R78-R100, R131-R138, R133a-R133g; AC33-AC35, AC41-AC42, AC46-AC49.
- Files/components likely touched:
  - `scripts/validation_cache.py`
  - `scripts/test-validation-cache.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/validation-cache/**`
- Dependencies:
  - Approved plan-review.
  - Approved test spec.
- Tests to add/update:
  - Direct `explicit-paths` actual run cache record can be reused by helper with the same paths.
  - Helper and direct commands share canonical cache argv but evidence preserves displayed helper argv.
  - Changed path order changes canonical command hash and misses cache.
  - Helper prior passing event must resolve to an actual run, not a cache-hit-only chain.
  - Unsupported modes remain cache-ineligible.
- Implementation steps:
  - Extend command-family evaluation to recognize `explicit-paths-inner-loop` as helper-only.
  - Add helper normalization that replaces helper mode with canonical direct `explicit-paths` for cache identity.
  - Preserve displayed helper argv for evidence without using it as the cache-key command.
  - Keep duplicate path, unsafe path, missing manifest, implementation hash, and policy hash behavior unchanged.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `git diff --check --`
- Expected observable result: cache identity primitives distinguish displayed helper argv from canonical cache argv and can reuse safe prior direct actual-run passes.
- Commit message: `M1: add helper cache identity normalization`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Literal helper-mode hashes could prevent reuse of prior direct actual runs.
  - Over-normalization could hide the user-invoked helper command from evidence.
- Rollback/recovery:
  - Revert helper-mode recognition and leave direct `explicit-paths` cache behavior unchanged.

### M2. Inner-loop helper runtime and formal cache-hit evidence

- Milestone state: closed
- Goal: Expose `--mode explicit-paths-inner-loop`, supply approved cache context by default, and write or merge formal helper evidence only in safe workflow contexts.
- Requirements: R32-R50, R131-R149; AC33-AC39, AC46-AC47.
- Files/components likely touched:
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/validation_cache.py`
  - `scripts/test-validation-cache.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/validation-cache/**`
- Dependencies:
  - M1 canonical identity support.
- Tests to add/update:
  - Helper supplies cache context without caller-provided long cache flags.
  - Helper cache hit emits visibly distinct `[CACHE HIT]` output.
  - Helper cache miss or disabled cache reports reason and runs actual validation.
  - Helper actual-run fallback preserves validator pass/fail behavior and exit codes.
  - Helper writes or merges `validation-cache-evidence.yaml` only with safe change root or explicit safe evidence path.
  - Ad hoc helper use outside safe change root prints status but writes no formal evidence.
  - Existing cache-hit evidence is merged without overwriting unrelated records.
- Implementation steps:
  - Add `explicit-paths-inner-loop` to the lifecycle validator mode surface.
  - Internally map helper invocation to approved cache flags and `inner-loop` cache context.
  - Keep direct `explicit-paths` unchanged for actual-run closeout use.
  - Update helper evidence writer to include `displayed_command_argv`, `canonical_cache_argv`, `scope: inner-loop`, and `closeout_evidence: false`.
  - Fail closed to actual validation on unknown, missing, malformed, stale, unsupported, changed, or unsafe identity.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
  - `git diff --check --`
- Expected observable result: repeated inner-loop lifecycle validation has a short helper command that safely uses cache or falls back to actual validation.
- Commit message: `M2: add inner-loop lifecycle helper mode`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Helper output could look like actual-run proof.
  - Formal evidence could be written for unsafe ad hoc contexts.
- Rollback/recovery:
  - Disable or remove the helper mode; direct `explicit-paths` actual-run validation remains available.

### M3. Closeout rejection and actual-run boundary enforcement

- Milestone state: closed
- Goal: Make helper cache hits structurally unable to satisfy closeout, verify, branch-readiness, PR-readiness, release, or CI proof.
- Requirements: R50-R59, R101-R116, R135-R138, R150-R151; AC11-AC14, AC24-AC28, AC40-AC42.
- Files/components likely touched:
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/artifact-lifecycle/**`
  - `tests/fixtures/change-metadata/**`
- Dependencies:
  - M2 helper evidence shape.
- Tests to add/update:
  - Closeout record with helper command as sole passing proof fails.
  - Closeout record with only helper-produced `cache-hit-inner-loop` evidence fails.
  - Closeout record with separate `actual-run-pass` can include helper cache-hit supporting evidence.
  - CI proof does not use helper and direct `explicit-paths` remains actual-run.
  - Legacy metadata cannot promote cache-hit evidence into closeout.
- Implementation steps:
  - Add closeout rejection for `explicit-paths-inner-loop` proof commands.
  - Ensure `evidence_kind: cache-hit-inner-loop` remains invalid as closeout proof.
  - Keep `actual-run-pass` compact metadata as the closeout-eligible path.
  - Preserve existing legacy metadata compatibility except for invalid cache-hit closeout claims.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `git diff --check --`
- Expected observable result: helper evidence is enforceably inner-loop only, and closeout still requires actual-run evidence.
- Commit message: `M3: enforce helper closeout boundary`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Closeout validation could accidentally reject valid actual-run evidence when helper evidence is present only as support.
- Rollback/recovery:
  - Revert closeout-specific helper checks while keeping direct actual-run validation as the required fallback until fixed.

### M4. Measurement schema and selector routing

- Milestone state: closed
- Goal: Add helper-specific measurement fields, consistency validation, and deterministic selector routing for helper evidence and measurement artifacts.
- Requirements: R117-R130, R152-R154, R157-R159; AC29-AC32, AC44-AC45, AC50.
- Files/components likely touched:
  - `scripts/validation_cache.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/validation_selection.py`
  - `scripts/test-validation-cache.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/test-select-validation.py`
  - `tests/fixtures/validation-cache/**`
  - `tests/fixtures/change-metadata/**`
  - `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml`
- Dependencies:
  - M2 helper runtime and M3 closeout semantics.
- Tests to add/update:
  - Valid measurement with helper hit, fallback, and closeout run passes.
  - Missing `helper_invocations`, `actual_run_fallbacks`, or `closeout_actual_runs` fails.
  - Impossible count relationships fail.
  - Cache hit counted as closeout actual run fails.
  - Invalid Workstream B recommendation or missing rationale fails.
  - Selector routes `validation-cache-evidence.yaml` to lifecycle/cache regression coverage.
  - Selector routes `validation-cache-measurement.yaml` to lifecycle and measurement/change-metadata validation coverage.
- Implementation steps:
  - Extend measurement schema helpers and validators with helper-specific fields.
  - Enforce count relationships from the approved spec.
  - Add or update selector routes for cache evidence and measurement files.
  - Record first-slice measurement evidence for this change, with expansion recommendation defaulting to `defer` unless implementation data justifies a reviewed follow-up.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-evidence.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `git diff --check --`
- Expected observable result: helper adoption and savings are measurable, count-consistent, selector-routed, and not confused with closeout actual runs.
- Commit message: `M4: add helper measurement and routing`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Selector routes for new evidence files could be too broad or miss actual changed paths.
  - Measurement could overstate savings or count helper cache hits as closeout actual runs.
- Rollback/recovery:
  - Remove helper measurement evidence and selector routes while leaving direct actual-run validation available; defer expansion decisions.

### M5. Repository-local command guidance and behavior preservation

- Milestone state: review-requested
- Goal: Record repository-local validation command guidance and behavior-preservation evidence without exposing internal commands in published skills.
- Requirements: R73-R77, R155-R156; AC16, AC18, AC43.
- Files/components likely touched:
  - `specs/validation-idempotency-and-cache-hit-safety.test.md`
  - `docs/examples/plans/example-plan.md` if repo-local examples are the selected guidance surface
  - `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md`
  - `skills/plan/SKILL.md` and `skills/test-spec/SKILL.md` only for no-exposure review, not internal command insertion
- Dependencies:
  - M2 helper command behavior.
  - M3 closeout boundary.
  - M4 measurement and routing if guidance references measurement evidence.
- Tests to add/update:
  - Published skill text does not expose `explicit-paths-inner-loop`, internal validator paths, selector mechanics, generated-output paths, or maintenance details.
  - Behavior-preservation matrix proves direct actual-run validation remains unchanged, helper cache misses run actual validation, helper cache hits are inner-loop evidence, and selector/CI routing remains actual-run.
  - Any repo-local example command table distinguishes inner-loop helper from closeout actual-run command.
- Implementation steps:
  - Add or update repository-local guidance only where it is allowed by the spec and useful for maintainers.
  - Do not put RigorLoop-internal helper commands into published skill bodies.
  - Record behavior-preservation proof for direct lifecycle actual run, helper cache miss, helper cache hit, closeout validation, failure detection, cache evidence, selector/CI routing, and measurement.
  - Update generated adapters only if canonical published skill text changes; otherwise record generated-output surfaces as unaffected.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md --path specs/validation-idempotency-and-cache-hit-safety.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md --path specs/validation-idempotency-and-cache-hit-safety.md`
  - `git diff --check --`
- Expected observable result: maintainers can see the two-command inner-loop versus closeout pattern, while published skills remain free of repository-internal command details.
- Commit message: `M5: document helper validation boundary`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Internal helper commands could leak into published skills.
  - Repo-local guidance could imply cache hits are closeout proof.
- Rollback/recovery:
  - Revert guidance changes and keep behavior-preservation evidence as the source of truth until a safer guidance surface is chosen.

### M6. Lifecycle closeout

- Milestone state: planned
- Goal: Complete implementation evidence, explain the change, verify the branch, and prepare PR handoff after all implementation milestones are reviewed and closed.
- Requirements: all in-scope requirements and acceptance criteria.
- Files/components likely touched:
  - `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/explain-change.md`
  - `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/verify-report.md` if verify requires a report
  - `docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
  - `docs/plan.md`
- Dependencies:
  - M1-M5 implementation milestones closed after code-review.
  - Required review-resolution closed if any code-review finding triggers it.
- Tests to add/update:
  - None specific; this milestone runs final validation from the plan and test spec.
- Implementation steps:
  - Record explain-change after implementation and review-resolution are complete.
  - Run final verify using exact plan/test-spec commands.
  - Synchronize plan body and `docs/plan.md` lifecycle state before PR handoff.
  - Prepare PR summary after verify passes.
- Validation commands:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
  - `git diff --check --`
- Expected observable result: all helper work is implemented, reviewed, explained, verified, and ready for PR handoff without claiming closeout before downstream gates pass.
- Commit message: `M6: close cache-aware lifecycle helper`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Final closeout could miss stale lifecycle state between the plan body and plan index.
- Rollback/recovery:
  - Keep the plan active and fix stale state or validation failures before PR handoff.

## Validation plan

- `python scripts/test-validation-cache.py`: cache identity, helper normalization, evidence, and measurement behavior.
- `python scripts/test-artifact-lifecycle-validator.py`: lifecycle validator modes, helper runtime, and closeout rejection.
- `python scripts/test-change-metadata-validator.py`: compact metadata evidence-kind and measurement consistency checks.
- `python scripts/test-select-validation.py`: selector routes for cache evidence and measurement.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`: formal review closeout evidence.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`: change metadata integrity.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: actual-run lifecycle validation for closeout and final gates.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop ...`: inner-loop helper proof after the helper exists; not used as closeout proof.
- `git diff --check --`: whitespace and patch hygiene.

## Risks and recovery

- Risk: helper mode is mistaken for closeout proof.
  - Recovery: keep direct `explicit-paths` as the closeout command, reject helper proof commands in closeout validation, and label helper evidence `cache-hit-inner-loop` with `closeout_evidence: false`.
- Risk: helper cache identity cannot reuse prior direct actual-run passes.
  - Recovery: normalize helper cache identity to canonical direct argv and preserve displayed helper argv only as evidence context.
- Risk: stale cache hit after selector, CI, validator, or policy changes.
  - Recovery: implementation and policy hashes invalidate cache; selector and CI proof remain actual-run and separately routed.
- Risk: formal evidence writes unsafe local data.
  - Recovery: require safe change root or safe evidence path, repository-relative paths, and secret/local-path validation.
- Risk: measurement overstates savings or supports premature expansion.
  - Recovery: enforce helper count relationships, keep closeout actual runs distinct, and default expansion recommendation to `defer`.
- Risk: published skills expose internal RigorLoop commands.
  - Recovery: keep command guidance in repository-local surfaces only; validate skill text if touched.

## Dependencies

- Plan-review must approve this plan before test-spec.
- Test-spec amendment must be complete before implementation.
- Implementation must proceed through code-review per milestone.
- Any material code-review finding must be resolved before the affected milestone closes.
- CI remains actual-run for this first slice.
- Broader cache eligibility and edit-scoped validation require separate approved proposals or spec amendments.

## Progress

- 2026-05-24: Proposal accepted, spec approved after R2, architecture updated, and architecture-review R1 approved with no material findings.
- 2026-05-24: Execution plan created and added to `docs/plan.md` for plan-review.
- 2026-05-24: Plan-review R1 approved with no material findings.
- 2026-05-24: Test spec amended in `specs/validation-idempotency-and-cache-hit-safety.test.md` for helper normalization, runtime fallback, evidence, closeout rejection, selector routing, measurement, and published-skill boundaries; approved by user; M1 is ready for implementation.
- 2026-05-24: M1 implemented helper-mode parser support, canonical direct-command cache identity normalization, displayed helper argv preservation on `LifecycleCacheIdentity`, and tests for direct-pass reuse, helper path-order invalidation, unsupported command exclusion, and helper explicit-path CLI behavior.
- 2026-05-24: Code-review M1 R1 completed clean-with-notes with no material findings; M1 closed and M2 is ready for implementation.
- 2026-05-24: M2 implemented automatic inner-loop helper cache use, cache-miss fallback output, inferable safe change-root evidence writes, ad hoc no-evidence behavior, displayed/canonical argv evidence rendering, and focused tests for helper cache hits and formal evidence.
- 2026-05-24: Code-review M2 R1 recorded VIC-IH-CR-M2-001 against an over-broad ad hoc no-evidence test assertion; M2 is in review-resolution.
- 2026-05-24: Review-resolution for VIC-IH-CR-M2-001 narrowed the ad hoc no-evidence assertion to compare evidence files before and after the command, preserving compatibility with legitimate formal evidence files; M2 is ready for re-review.
- 2026-05-24: Code-review M2 R2 completed clean-with-notes with no material findings; M2 closed and M3 is ready for implementation.
- 2026-05-24: M3 implemented closeout rejection for `explicit-paths-inner-loop` lifecycle proof commands in compact change metadata and artifact lifecycle validation, while preserving direct `explicit-paths` actual-run closeout evidence.
- 2026-05-24: Code-review M3 R1 recorded VIC-IH-CR-M3-001 because helper closeout rejection missed the accepted `--mode=explicit-paths-inner-loop` flag spelling; M3 is in review-resolution.
- 2026-05-24: Review-resolution for VIC-IH-CR-M3-001 normalized helper mode detection for both `--mode VALUE` and `--mode=VALUE` forms; M3 is ready for re-review.
- 2026-05-24: Code-review M3 R2 completed clean-with-notes with no material findings; M3 closed and M4 is ready for implementation.
- 2026-05-24: M4 updated validation-cache measurement validation for helper-specific fields and count relationships, added helper measurement fixtures, recorded first-slice measurement evidence, and confirmed the existing selector routes for cache evidence and measurement select lifecycle, cache regression, and change-metadata validation without manual routing debt.
- 2026-05-24: Code-review M4 R1 completed clean-with-notes with no material findings; M4 closed and M5 is ready for implementation.
- 2026-05-24: M5 recorded repository-local inner-loop versus closeout command guidance in behavior-preservation evidence, proved direct actual-run validation and helper fallback behavior, confirmed published skills do not contain internal helper commands or validator/cache evidence paths, and left canonical skill/adapters unchanged.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-24 | Plan the helper as a new lifecycle validator mode, not a wrapper script. | The approved spec chooses `--mode explicit-paths-inner-loop`, and architecture records it as an adoption surface inside the existing validator boundary. | Wrapper script in the first slice. |
| 2026-05-24 | Keep direct `--mode explicit-paths` as the actual-run closeout command. | Closeout, verify, branch-readiness, PR-readiness, and CI must remain actual-run evidence in the first slice. | Cache by default for direct explicit-path lifecycle validation. |
| 2026-05-24 | Keep published skills out of scope for internal command examples. | The approved spec forbids exposing RigorLoop-internal validator paths and selector mechanics in published skills. | Adding helper command tables to public skill text. |
| 2026-05-24 | M1 preserves helper displayed argv on cache identity but does not write helper formal evidence yet. | Formal helper evidence writing and prior-actual-run evidence validation are assigned to M2/M3; M1 only prepares the identity surface needed by those milestones. | Expanding M1 into evidence-file schema and closeout validation work. |
| 2026-05-24 | Let `RIGORLOOP_VALIDATION_CACHE_DIR` override the helper's default local cache directory. | M2 tests need isolated cache directories while keeping normal CLI use free of long cache flags. | Requiring tests or helper users to pass the long cache flag set. |

## Surprises and discoveries

- The existing validator already has opt-in cache flags, so implementation should reuse the existing cache primitives and focus on helper adoption, canonical identity, evidence, measurement, and closeout boundaries.
- M1 could expose the helper CLI mode without enabling automatic helper cache use yet by routing validator execution through the existing explicit-path lifecycle implementation and leaving cache-context defaults to M2.
- R133f/R133g are unaffected in M1 because no helper-produced formal cache-hit evidence is written in this slice; M2/M3 remain responsible for enforcing prior actual-run ancestry when helper formal evidence exists.
- M2 can infer formal helper evidence only when exactly one safe change root is present and the corresponding `change.yaml` exists; otherwise helper cache hits remain local/ad hoc status output with no formal evidence write.
- M4 found `validation-cache-evidence.yaml` and `validation-cache-measurement.yaml` were already registered in the selector; no selector code change was needed. The existing route selects `artifact_lifecycle.validate` and `validation_cache.regression` for evidence, and `artifact_lifecycle.validate`, `change_metadata.validate`, and `change_metadata.regression` for measurement.
- M5 selected `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md` as the repository-local guidance surface for the two-command table. Published skill source stayed unchanged, so generated adapter output is unaffected.

## Validation notes

- 2026-05-24 test-spec handoff validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/architecture-review-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/plan-review-r1.md`
  - `git diff --check -- specs/validation-idempotency-and-cache-hit-safety.test.md docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md docs/plan.md docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
- 2026-05-24 M1 validation passed:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/architecture-review-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/plan-review-r1.md`
  - `git diff --check --`
- 2026-05-24 M2 focused validation passed before artifact-state updates:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
- 2026-05-24 M2 implementation validation passed:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path specs/validation-idempotency-and-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
  - `git diff --check --`
- 2026-05-24 M2 handoff artifact validation passed after plan and change-metadata updates:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/architecture-review-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/plan-review-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m1-r1.md`
  - `git diff --check --`
- 2026-05-24 code-review M2 R1 recording validation passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r1.md`
  - `git diff --check --`
- 2026-05-24 review-resolution validation for VIC-IH-CR-M2-001 passed:
  - `python scripts/test-artifact-lifecycle-validator.py`
- 2026-05-24 review-resolution handoff validation passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r1.md`
  - `git diff --check --`
- 2026-05-24 code-review M2 R2 validation passed:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
- 2026-05-24 code-review M2 R2 artifact closeout validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r2.md`
  - `git diff --check --`
- 2026-05-24 M3 targeted validation passed:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `git diff --check --`
- 2026-05-24 M3 handoff artifact validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m2-r2.md`
  - `git diff --check --`
- 2026-05-24 review-resolution validation for VIC-IH-CR-M3-001 passed:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
- 2026-05-24 review-resolution handoff validation passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r1.md`
  - `git diff --check --`
- 2026-05-24 code-review M3 R2 validation passed:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
- 2026-05-24 code-review M3 R2 artifact closeout validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r2.md`
  - `git diff --check --`
- 2026-05-24 M4 red test confirmed old measurement schema behavior before implementation:
  - `python scripts/test-change-metadata-validator.py` failed because the validator still required `closeout.full_bundle_actual_runs` and the old `eligible_commands = cache_hits + cache_misses + cache_disabled` rule instead of helper-specific count relationships.
- 2026-05-24 M4 targeted validation passed:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-evidence.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml`
- 2026-05-24 M4 handoff artifact validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r2.md`
  - `git diff --check --`
- 2026-05-24 code-review M4 R1 validation passed:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-select-validation.py`
- 2026-05-24 code-review M4 R1 artifact closeout validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r1.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r2.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m4-r1.md`
  - `git diff --check --`
- 2026-05-24 M5 published-skill no-exposure proof passed:
  - `rg -n "explicit-paths-inner-loop|validate-artifact-lifecycle.py|validation-cache-evidence.yaml|validation-cache-measurement.yaml|validation_selection.py|scripts/select-validation.py" skills` returned no matches.
- 2026-05-24 M5 validation passed:
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py` initially failed one timing-sensitive broad-smoke assertion with a negative fixture duration, then the targeted failing test passed on rerun and the full suite passed on rerun.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md --path specs/validation-idempotency-and-cache-hit-safety.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md --path specs/validation-idempotency-and-cache-hit-safety.md`
  - `git diff --check --`
- 2026-05-24 M5 handoff artifact validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path specs/validation-idempotency-and-cache-hit-safety.md --path specs/validation-idempotency-and-cache-hit-safety.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md --path docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md --path docs/plan.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m4-r1.md`
  - `git diff --check --`

## Outcome and retrospective

- Pending until all implementation milestones, reviews, explain-change, verify, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
- Ready for code-review M5. Readiness is not Done; M5 has not been reviewed, and remaining implementation milestones, explain-change, verify, and PR gates remain.
