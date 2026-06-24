# Implementation Autoprogression Through Verify Execution Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-24-separately-armed-implementation-autoprogression-through-verify
- Owner: maintainer
- Start date: 2026-06-24
- Last updated: 2026-06-24
- Related issue or PR: none yet
- Supersedes: none

## Goal

Implement the first slice of the separately armed `implementation-through-verify` profile so RigorLoop can persist the profile policy, evaluate activation and phase gates, settle test-spec readiness, enforce reviewer-owned auto-fix classification, and prove bounded implementation/code-review autoprogression behavior without crossing the PR boundary.

## Why now

The proposal, spec amendments, architecture package update, and ADR are accepted or approved. Planning is needed before implementation because the change touches workflow orchestration, change metadata, review finding semantics, validators, skills, generated adapters, and fixture coverage.

## Source artifacts

- Proposal: [Separately Armed Implementation Autoprogression Through Verify](../proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md)
- Proposal-review: [proposal-review-r1](../changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/proposal-review-r1.md)
- Specs: [workflow-stage-autoprogression](../../specs/workflow-stage-autoprogression.md), [rigorloop-workflow](../../specs/rigorloop-workflow.md), [review-finding-resolution-contract](../../specs/review-finding-resolution-contract.md)
- Test spec: [Implementation Autoprogression Through Verify test spec](../../specs/implementation-autoprogression-through-verify.test.md)
- Spec-review: [spec-review-r1](../changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/spec-review-r1.md)
- Architecture: [canonical system architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260624-implementation-through-verify-autoprogression](../adr/ADR-20260624-implementation-through-verify-autoprogression.md)
- Architecture-review: [architecture-review-r1](../changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/architecture-review-r1.md)
- Change metadata: [change.yaml](../changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/change.yaml)

## Scope

### In scope

- Add change-local `implementation-through-verify` profile policy support and fail-closed unknown profile handling.
- Persist implementation-profile authorization independently from authoring-profile authorization, including phase `A`, `B`, or `C`.
- Implement audit-only Phase A transition evaluation and Phase B implementation-through-final-clean-code-review routing.
- Keep Phase C `explain-change` and fresh `verify` behavior designed and guarded, but disabled until promotion evidence exists.
- Add deterministic test-spec settlement and first-code-review settlement identity recheck surfaces.
- Add reviewer-owned `auto_fix_class`, `auto_fix_kind`, affected-path, deterministic-authority, recipe, forbidden-path, acceptance, and validation fields for implementation-profile code-review findings.
- Enforce three correction rounds per milestone, shrinking findings, no-new-findings, path locality, governing-artifact stop, scope-budget stop, and approved-command boundaries.
- Update canonical skills and generated adapters after authored guidance changes.
- Add fixture and validator coverage for the acceptance criteria required by the approved specs.

### Out of scope

- Opening, publishing, or updating hosted PRs automatically.
- Automatic deploy, release, package publish, branch push, or remote notification behavior.
- Automatic verify-failure repair.
- Project-wide default autoprogression profiles.
- Independent `test-spec-review`.
- Background or asynchronous execution.
- Phase C enablement before Phase B promotion evidence exists.

## Constraints

- Profile-off behavior remains unchanged.
- Authoring-profile authorization must not authorize implementation.
- Profile policy metadata must not own live current stage, next stage, review status, branch readiness, PR readiness, or active-plan state.
- Reviewers own auto-fix classification; the orchestrator only enforces recorded classifications and recipes.
- Governing-artifact substantive edits during automatic correction are hard stops.
- Final verify evidence in Phase C must be fresh actual-run evidence for correctness-bearing and release-sensitive checks.
- Generated public adapter output must be refreshed from canonical skills, not hand-edited.

## Current Handoff Summary

- Current milestone: M5. Behavior preservation and rollout evidence
- Current milestone state: closed
- Latest review evidence: docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/code-review-m5-r2.md
- Last reviewed milestone: M5. Behavior preservation and rollout evidence
- Review status: approved; stage=code-review; round=r2
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: ready
- Reason final closeout is or is not ready: ready — verify passed from tracked branch state; PR handoff is next.

## Milestones

### M1. Profile schema and authorization policy

- Milestone state: closed
- Deliverable: change metadata schema/validator support for `implementation-through-verify`, independent policy records, phase values, authorization persistence, cancellation, and fail-closed unknown values.
- Requirements: `workflow-stage-autoprogression` R2am-R2ax; `rigorloop-workflow` R7et-R7ew.
- Likely files: `schemas/change.schema.json`, `scripts/validate-change-metadata.py`, validator tests and fixtures, workflow guidance as needed.
- Validation: targeted change-metadata validator tests plus explicit validation of this change pack.
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M1
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] plan progress updated before starting M2
- Milestone commit message: `M1: add implementation profile policy persistence`

### M2. Test-spec settlement and workflow transition evaluator

- Milestone state: closed
- Deliverable: workflow routing support for Phase A audit-only evaluation, Phase B routing through implementation/code-review, deterministic test-spec settlement, first-review identity recheck, ordered milestones, and phase-boundary refusal.
- Requirements: `workflow-stage-autoprogression` R2ay-R2bd; `rigorloop-workflow` R7ex-R7ey.
- Likely files: workflow skill guidance, workflow routing fixtures or scripts, artifact-lifecycle/state-sync validation, test-spec skill guidance, relevant tests.
- Validation: fixture coverage for clean settlement, stale identity pause, phase A no-execution, Phase B stop before closeout, ordered milestone routing, and no duplicate resume.
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M2
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] plan progress updated before starting M3
- Milestone commit message: `M2: route implementation profile through settlement and milestones`

### M3. Reviewer-owned finding classification and correction guardrails

- Milestone state: closed
- Deliverable: review-finding schema/guidance and validation for `auto_fix_class`, closed mechanical kinds, declared-safe recipes, path and command constraints, shrinking-set/no-new-findings invariants, round caps, and governing-artifact hard stops.
- Requirements: `workflow-stage-autoprogression` R2be-R2bu; `review-finding-resolution-contract` R1e-R1l and R11.
- Likely files: review-finding contract tests, review artifact validator, code-review and review-resolution skill guidance, fixtures.
- Validation: fixtures for missing classification, invalid class/kind, incomplete mechanical fields, incomplete declared-safe recipes, owner-decision pause, governing-artifact edit pause, new finding pause, non-shrinking pause, and fourth-round block.
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M3
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] plan progress updated before starting M4
- Milestone commit message: `M3: enforce reviewer-owned auto-fix classifications`

### M4. Skills, adapters, and Phase C guard surfaces

- Milestone state: closed
- Deliverable: canonical skill updates for workflow, test-spec, implement, code-review, review-resolution, explain-change, verify, plan, and plan-review; generated adapter refresh; Phase C refusal until promotion evidence; final verify and PR-boundary guidance.
- Requirements: `workflow-stage-autoprogression` R2bv-R2bz; `rigorloop-workflow` R7fac-R7fad.
- Likely files: `skills/`, generated adapter support surfaces, skill contract fixtures, adapter generation validation.
- Validation: generated-skill drift/adapters validation, fixture checks for Phase C disabled behavior, fresh verify evidence rules, verify failure pause, and stop-before-PR behavior.
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M4
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] plan progress updated before starting M5
- Milestone commit message: `M4: update skills and guard verify-boundary behavior`

### M5. Behavior preservation and rollout evidence

- Milestone state: closed
- Deliverable: acceptance-criteria fixtures, behavior-preservation matrix, rollout/promotion evidence placeholders, and final validation bundle alignment for the first slice.
- Requirements: approved proposal acceptance criteria `AC-ITV-001` through `AC-ITV-025` and testing strategy `ITV-001` through `ITV-039`.
- Likely files: test fixtures, validation scripts, `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/behavior-preservation.md`, and change-local rollout evidence.
- Validation: targeted test suites from M1-M4 plus artifact lifecycle, review artifacts, change metadata, generated output checks, and selected broad smoke when selectors require it.
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M5
- Review closeout:
  - [x] final full code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] all implementation milestones closed before explain-change
- Milestone commit message: `M5: prove implementation autoprogression behavior preservation`

## Validation plan

- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/change.yaml`
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/review-finding-resolution-contract.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md --path docs/plans/2026-06-24-implementation-autoprogression-through-verify.md --path docs/plan.md --path docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/change.yaml --path docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/review-log.md`
- Milestone-specific validator and fixture commands added by the matching test spec before implementation.
- Generated output and adapter validation after canonical skill guidance changes.
- Final `explain-change` and `verify` after all implementation milestones and code-review close.

## Test-spec handoff

The matching test spec is active at `specs/implementation-autoprogression-through-verify.test.md` and maps approved requirements, acceptance criteria, edge cases, and the M1-M5 proof obligations into concrete validator, fixture, and manual-proof coverage.

## Risks and recovery

- Profile metadata could become live workflow state. Recovery: keep metadata as policy/audit only and validate forbidden live-state fields.
- Reviewer classification could be over-trusted. Recovery: require closed kinds or complete recipes, path bounds, validation, and pause on owner decisions.
- Loop enforcement could chase new work. Recovery: pause on new finding IDs/classes and non-shrinking sets.
- Phase C could become enabled by documentation only. Recovery: persist phase and require promotion evidence before transition.
- Generated skill output could drift. Recovery: regenerate from canonical skill sources and run adapter validation.
- Validator support could lag spec language. Recovery: keep unsupported behavior fail-closed and record fixture gaps before plan closeout.

## Dependencies

- Approved specs and architecture records listed in Source artifacts.
- Existing review recording and artifact lifecycle validators.
- Existing generated skill and adapter build/validation scripts.
- No new runtime dependency is planned.

## Progress

- 2026-06-24: Proposal accepted, spec amendments approved, architecture package and ADR approved by architecture-review, and execution plan created.
- 2026-06-24: Test spec authored and activated for M1-M5 proof coverage.
- 2026-06-24: M1 implemented named implementation-profile policy validation, schema support, and focused regression coverage; ready for code-review M1.
- 2026-06-24: Code-review M1 R1 requested changes for CR-M1-R1-F1; M1 moved to review-resolution.
- 2026-06-24: CR-M1-R1-F1 resolved by centralizing forbidden live-state validation across autoprogression containers and records; M1 returned to code-review R2.
- 2026-06-24: Code-review M1 R2 found no material findings; M1 closed and the plan advanced to implement M2.
- 2026-06-24: Started M2 implementation against `scripts/lifecycle_state_sync.py` and workflow route fixture tests.
- 2026-06-24: M2 implemented fixture-driven `implementation-through-verify` route evaluation for activation gates, phase boundaries, test-spec settlement, first-review identity recheck, ordered milestone routing, and idempotent resume; ready for code-review M2.
- 2026-06-24: Code-review M2 R1 found no material findings; M2 closed and the plan advanced to implement M3.
- 2026-06-24: M3 implemented parser-owned `auto_fix_class` structure validation for implementation-profile code-review findings and fixture-driven correction guardrails for round caps, shrinking/no-new-finding invariants, path locality, governing-artifact stops, scope-budget stops, command approval, CI deny-list gating, and audit evidence; ready for code-review M3.
- 2026-06-24: Code-review M3 R1 requested changes for CR-M3-R1-F1 and CR-M3-R1-F2; M3 moved to review-resolution.
- 2026-06-24: Resolved CR-M3-R1-F1 and CR-M3-R1-F2 by deriving correction path locality from unresolved findings' reviewer-declared paths, verifying top-level path redundancy, adding required-field constants for mechanical and declared-safe correction eligibility, and requiring mechanical deterministic authority; ready for code-review M3 R2.
- 2026-06-24: Code-review M3 R2 found no material findings; M3 closed and the plan advanced to implement M4.
- 2026-06-24: M4 updated canonical workflow, test-spec, implement, code-review, explain-change, verify, plan, and plan-review skill surfaces for `implementation-through-verify` phase boundaries, promotion evidence, fresh verify evidence, verify-failure pause, and stop-before-PR behavior; ready for code-review M4.
- 2026-06-24: Code-review M4 R1 found no material findings; M4 closed and the plan advanced to implement M5.
- 2026-06-24: M5 added behavior-preservation evidence covering `AC-ITV-001` through `AC-ITV-025` and `ITV-001` through `ITV-039`, plus static no-`test-spec-review` stage checks; ready for code-review M5.
- 2026-06-24: Code-review M5 R1 found no material findings; M5 closed and final closeout advanced to explain-change.
- 2026-06-24: Explain-change recorded the implementation rationale and advanced final closeout to verify.
- 2026-06-24: Verify blocked on broad local lifecycle validation for the invalid autoprogression metadata fixture; branch readiness and PR handoff were not claimed.
- 2026-06-24: Verification-fix implementation moved the invalid autoprogression metadata fixture under a directory matching the active change ID, preserving the intended forbidden `workflow.autoprogression.next_stage` failure while allowing broad local lifecycle validation to pass; ready for code-review.
- 2026-06-24: Code-review M5 R2 found no material findings for the verification-fix slice; final closeout returned to verify.

## Decision log

- 2026-06-24: Split implementation into five milestones -> separates metadata, workflow routing, review classification, skill/adapters, and proof surfaces so each can receive focused code-review.
- 2026-06-24: Keep Phase C guarded in the first implementation plan -> matches the approved rollout requirement that Phase C cannot run until Phase B promotion evidence exists.

## Surprises and discoveries

- None yet.

## Validation notes

- 2026-06-24: Pre-plan checks passed for change metadata, review artifacts, artifact lifecycle explicit paths, and diff whitespace. Artifact lifecycle emitted an existing `rigorloop-workflow.md` lifecycle-language warning for reviewer attention.
- 2026-06-24: M1 targeted validation passed: `python scripts/test-change-metadata-validator.py -k autoprogression_policy` (6 passed), `python scripts/test-change-metadata-validator.py -k named_autoprogression_policy` (1 passed), and `python scripts/test-change-metadata-validator.py` (28 passed).
- 2026-06-24: CR-M1-R1-F1 resolution validation passed: `python scripts/test-change-metadata-validator.py -k autoprogression_policy` (6 passed), `python scripts/test-change-metadata-validator.py -k named_autoprogression_policy` (1 passed), `python scripts/test-change-metadata-validator.py -k forbidden_live_state` (1 passed), `python scripts/test-change-metadata-validator.py -k forbidden` (5 passed), `python scripts/test-change-metadata-validator.py` (39 passed), and direct invalid fixture validation failed with the expected live-state policy error.
- 2026-06-24: M2 targeted validation passed: `python scripts/test-artifact-lifecycle-validator.py -k implementation_profile` (5 tests), and `python scripts/test-artifact-lifecycle-validator.py` (113 tests).
- 2026-06-24: M2 code-review R1 recorded `clean-with-notes`; post-review change metadata, review artifacts, review closeout, artifact lifecycle, and diff whitespace validation passed.
- 2026-06-24: M3 targeted validation passed: `python scripts/test-review-artifact-validator.py -k auto_fix` (4 tests), `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails` (4 tests), `python scripts/test-review-artifact-validator.py` (52 tests), and `python scripts/test-artifact-lifecycle-validator.py` (117 tests).
- 2026-06-24: M3 handoff validation passed: change metadata validation, review artifact structure validation, artifact lifecycle explicit-path validation, and scoped `git diff --check`.
- 2026-06-24: M3 review-resolution validation passed: `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails` (15 tests, +11 over the previous 4-test M3 focused pass), `python scripts/test-artifact-lifecycle-validator.py` (128 tests), and `python scripts/test-review-artifact-validator.py` (52 tests).
- 2026-06-24: M3 review-resolution closeout validation passed: change metadata validation, review artifact structure validation, review artifact closeout validation, artifact lifecycle explicit-path validation, and scoped `git diff --check`.
- 2026-06-24: M4 targeted validation passed: `python scripts/test-skill-validator.py -k implementation_through_verify_public_skill_surfaces` (1 test), `python scripts/validate-skills.py` (23 skill files), `python scripts/build-skills.py --check`, `python scripts/test-build-skills.py` (7 tests), `python scripts/build-adapters.py --version v0.1.3 --output-dir /tmp/rigorloop-adapters-m4`, `python scripts/validate-adapters.py --root /tmp/rigorloop-adapters-m4 --version v0.1.3`, `python scripts/test-adapter-distribution.py` (129 tests), and `python scripts/test-skill-validator.py` (232 tests).
- 2026-06-24: M5 focused validation passed: `python scripts/test-skill-validator.py -k implementation_through_verify` (3 tests).
- 2026-06-24: M5 regression validation passed: `python scripts/test-change-metadata-validator.py -k autoprogression_policy` (6 passed), `python scripts/test-change-metadata-validator.py -k named_autoprogression_policy` (1 passed), `python scripts/test-artifact-lifecycle-validator.py -k implementation_profile` (5 tests), `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails` (15 tests), and `python scripts/test-review-artifact-validator.py -k auto_fix` (4 tests).
- 2026-06-24: M5 broad validation passed: `python scripts/test-change-metadata-validator.py` (39 passed), `python scripts/test-review-artifact-validator.py` (52 tests), `python scripts/test-artifact-lifecycle-validator.py` (128 tests), `python scripts/build-skills.py --check`, `python scripts/validate-skills.py` (23 skill files), `python scripts/test-build-skills.py` (7 tests), `python scripts/build-adapters.py --version v0.1.3 --output-dir /tmp/rigorloop-adapters-m5`, `python scripts/validate-adapters.py --root /tmp/rigorloop-adapters-m5 --version v0.1.3`, `python scripts/test-adapter-distribution.py` (129 tests), and `python scripts/test-skill-validator.py` (234 tests).
- 2026-06-24: Explain-change handoff validation passed: change metadata validation, review artifact closeout validation, artifact lifecycle explicit-path validation, and scoped `git diff --check`.
- 2026-06-24: Verify validation passed for change metadata, review closeout, full change-metadata tests, full review-artifact tests, full artifact-lifecycle tests, explicit-path lifecycle validation, skill validation, generated-skill checks, adapter archive validation, adapter distribution tests, and full skill-validator tests. Verify blocked on `python scripts/validate-artifact-lifecycle.py --mode local` because `tests/fixtures/change-metadata/implementation-autoprogression-container-next-stage/change.yaml` fails unrelated lifecycle ownership checks before its intended forbidden-field failure.
- 2026-06-24: Verification-fix validation passed: `python scripts/test-change-metadata-validator.py -k container_next_stage` (1 test), direct fixture validation failed for the intended `workflow.autoprogression.next_stage` forbidden policy field, and `python scripts/validate-artifact-lifecycle.py --mode local` passed with unrelated baseline warnings only.

## Outcome and retrospective

- Not started. Keep this section final-only until implementation, review, explain-change, verify, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- Follow-up proposal remains required for automatic PR opening.
- Follow-up proposal remains required for automatic verify-failure repair.
- Follow-up proposal remains required for project-wide default profiles.
