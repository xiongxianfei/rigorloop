# Published Skill Design Implement And Code-Review Rollout Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-19
- Last updated: 2026-05-19
- Related proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md)
- Related spec: [Skill Contract](../../specs/skill-contract.md)
- Related pilot: [RigorLoop Published Skill Design Contract Execution Plan](2026-05-19-rigorloop-published-skill-design-contract.md)
- Related previous rollout: [Published Skill Design Spec Family Rollout](2026-05-19-published-skill-design-spec-family.md)
- Change root: [docs/changes/2026-05-19-published-skill-design-implement-code-review](../changes/2026-05-19-published-skill-design-implement-code-review/change.yaml)
- Supersedes: none

## Purpose / big picture

Continue the published-skill design rollout after the merged proposal and spec-family slices by applying the accepted design contract to the execution/review pair: `implement` and `code-review`.

This slice is intentionally narrow. It should make the implementation and review skills more portable, routing-focused, self-contained, and output-explicit without changing workflow stage order, review recording semantics, validation selectors, adapter roots, or ownership of any skill.

## Source artifacts

- Proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md), accepted.
- Proposal review: [proposal-review-r2](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r2.md), approved.
- Spec: [Skill Contract](../../specs/skill-contract.md), approved after [spec-review-r3](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/spec-review-r3.md).
- Test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), active for the merged pilot and spec-family rollout, and to be amended for this execution/review slice during `test-spec`.
- Architecture: not required. This change affects canonical skill text, deterministic validation fixtures, generated skill checks, temporary adapter validation, and change-local evidence; it does not add runtime components, persistence, APIs, deployment, or hard-to-reverse data flow.
- Project map: [RigorLoop Project Map](../project-map.md), available as orientation only.

## Context and orientation

- `skills/` remains the only authored skill source.
- Generated public adapter skill bodies are release archives for `v0.1.3` and later. Do not hand-edit generated adapter package output.
- The skill body edit scope is limited to:
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
- The slice may extend deterministic regression tests in `scripts/test-skill-validator.py` only when needed for this pair. It must not introduce broad semantic scoring or runtime model auto-selection claims.
- Change-local audit, routing coverage, behavior-preservation, behavior-parity, and token evidence for this slice should live under `docs/changes/2026-05-19-published-skill-design-implement-code-review/`.
- `implement` owns implementation handoff and plan progress updates; `code-review` owns independent first-pass review, finding recording, and milestone-aware next-stage routing. The rewrite must preserve those stage boundaries.

## Non-goals

- Do not rewrite all skills.
- Do not merge, retire, rename, remove, or change ownership of any skill.
- Do not edit `proposal`, `proposal-review`, `spec`, or `spec-review` unless validation exposes drift caused by this slice.
- Do not add a required `when_to_use` frontmatter field.
- Do not introduce broad semantic scoring of skill prose or CI claims about deterministic model auto-selection.
- Do not add a build-time partial/include system.
- Do not change adapter install roots, lockfile semantics, release archive trust boundaries, CLI behavior, validation selector semantics, or workflow stage order.
- Do not weaken `implement` first-pass completeness, milestone handoff, review-resolution, formal review recording, or `code-review` independence requirements.

## Requirements covered

| Requirement | Planned coverage |
| --- | --- |
| R27-R28 | Audit `implement` and `code-review` against the existence gate and portable operating-documentation standard. |
| R29 | Ensure `description` is the portable routing surface for implementation and implementation review, including near-miss boundaries. |
| R30-R31 | Ensure lifecycle role, execution procedure, body-routing boundaries, and rationale are explicit without duplicating all routing text. |
| R32-R33 | Confirm no missing resource maps or required repository-root internal dependencies are introduced. |
| R34 | Preserve or improve compact output skeletons for implementation handoff and first-pass code-review records. |
| R35 | Create deterministic routing coverage tables and prompt fixture expectations for the pair. |
| R36 principles | Reuse audit-first, behavior-preservation, behavior-parity, and token-cost discipline from the merged rollout slices. |

## Current Handoff Summary

- Current milestone: M1. Execution/review evidence scaffold
- Current milestone state: review-requested
- Last reviewed milestone: M0. Plan and change metadata
- Review status: M1 implementation complete; code-review pending
- Remaining in-scope implementation milestones: M1. Execution/review evidence scaffold; M2. Deterministic validator and fixture support; M3. Implement and code-review skill rewrite
- Next stage: code-review for M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones have not started; implementation, code-review, explain-change, verify, PR handoff, hosted CI, human review, and merge remain.

## Milestones

### M0. Plan and change metadata

- Milestone state: closed
- Goal: create the active rollout plan and compact change metadata for the `implement` and `code-review` slice.
- Requirements: R27-R36 planning coverage.
- Files/components likely touched:
  - `docs/plans/2026-05-19-published-skill-design-implement-code-review.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Dependencies: accepted proposal, approved skill contract, merged prior rollout slices.
- Tests to add/update: none in M0.
- Implementation steps:
  - Create a scoped rollout plan for `implement` and `code-review`.
  - Update the plan index to make this the only active plan.
  - Create compact change metadata for downstream validation.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `git diff --check -- docs/plans/2026-05-19-published-skill-design-implement-code-review.md docs/plan.md docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Expected observable result: the next rollout has a reviewable plan and plan index state before skill-body edits begin.
- Commit message: `Plan published skill design implement/code-review rollout`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated
  - validation notes updated
  - milestone committed
- Risks: planning could skip required test-spec or over-broaden into all workflow skills.
- Rollback/recovery: revert M0 plan and metadata files.

### M1. Execution/review evidence scaffold

- Milestone state: review-requested
- Goal: create the evidence structure for `implement` and `code-review` before changing validators or skill bodies.
- Requirements: R27-R31, R34-R35, R36 audit/preservation/parity discipline.
- Files/components likely touched:
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Dependencies: approved plan-review and owner-approved test spec amendment for this slice.
- Tests to add/update: none unless the test-spec amendment requires new evidence-file selector fixtures first.
- Implementation steps:
  - Audit `implement` and `code-review` descriptions, workflow-role blocks, output skeletons, stop conditions, self-containment wording, and behavior-significant obligations.
  - Record routing coverage tables for obvious positives, casual positives, edge positives, near negatives, competing-skill prompts, and should-not-trigger prompt classes.
  - Record behavior-preservation notes for behavior-significant wording likely to be rewritten.
  - Define representative implementation handoff and code-review artifacts for behavior parity.
  - Record baseline static token estimates for `implement` and `code-review`.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml --path docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md --path docs/plan.md`
  - `git diff --check -- docs/plans/2026-05-19-published-skill-design-implement-code-review.md docs/plan.md docs/changes/2026-05-19-published-skill-design-implement-code-review`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml --path docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md`
- Expected observable result: reviewers can inspect evidence before any `implement` or `code-review` skill rewrite closes.
- Commit message: `M1: scaffold published skill design execution-review evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: evidence could accidentally authorize behavior changes before preservation/parity proof exists.
- Rollback/recovery: remove or revise change-local evidence files; no canonical skill bodies are changed in this milestone.

### M2. Deterministic validator and fixture support

- Milestone state: planned
- Goal: make any deterministic checks needed for `implement` and `code-review` enforceable without broad semantic scoring.
- Requirements: R29, R32-R33, R35.
- Files/components likely touched:
  - `scripts/test-skill-validator.py`
  - `scripts/skill_validation.py` only if M1 exposes a production validator gap
  - `tests/fixtures/skills/`
  - `specs/skill-contract.test.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Dependencies: M1 evidence and approved test-spec amendment.
- Tests to add/update:
  - Add or reuse focused fixtures for execution/review routing coverage and body routing boundaries.
  - Add regression coverage only for deterministic failure modes discovered by M1 or required by the amended test spec.
  - Keep repository-root versus packaged-resource checks unchanged unless M1 exposes a same-class gap.
- Implementation steps:
  - Extend existing published-design checks only where this pair needs deterministic coverage.
  - Avoid adding runtime skill-selection claims.
  - Keep checks phrase/path/table based.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `git diff --check -- scripts tests specs docs/changes/2026-05-19-published-skill-design-implement-code-review`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path specs/skill-contract.test.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Expected observable result: deterministic validation supports the rewrite without pretending to judge prose quality broadly.
- Commit message: `M2: validate published skill design execution-review checks`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: checks could overfit wording or block unrelated future skill work.
- Rollback/recovery: revert validator/fixture changes while preserving M1 evidence for replanning.

### M3. Implement and code-review skill rewrite

- Milestone state: planned
- Goal: update only `implement` and `code-review` to the published-skill design contract.
- Requirements: R27-R35 and M1 preservation/parity evidence.
- Files/components likely touched:
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Dependencies: M1 and M2 closed or explicitly found no validator changes needed.
- Tests to add/update:
  - Update focused validator tests if the skill opt-in shape requires it.
  - No broad semantic scoring or runtime model-selection tests.
- Implementation steps:
  - Tighten `description` routing for implementation and code review, including competing-skill near misses.
  - Keep bodies execution-focused and preserve first-pass completeness, milestone-aware handoff, independent-review mode, material finding recording, review-resolution routing, stop conditions, validation obligations, and claim boundaries.
  - Remove or reframe any required maintainer-only repository dependency if found.
  - Add or preserve compact output skeletons for implementation result/handoff and first-pass review records.
  - Record behavior-preservation and behavior-parity results.
  - Record after-change static token estimates and compare against baseline.
  - Validate generated skills and temporary adapter archives from canonical skills.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
  - `git diff --check -- skills/implement/SKILL.md skills/code-review/SKILL.md specs/skill-contract.test.md docs/plans/2026-05-19-published-skill-design-implement-code-review.md docs/plan.md docs/changes/2026-05-19-published-skill-design-implement-code-review`
  - `bash scripts/ci.sh --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml`
- Expected observable result: `implement` and `code-review` route more reliably, remain portable, preserve lifecycle claim boundaries, and validate from canonical skill source.
- Commit message: `M3: roll out published skill design to execution-review skills`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: `implement` and `code-review` carry high-value workflow guardrails; rewrites could accidentally weaken milestone state, review recording, review-resolution, or branch/PR readiness boundaries.
- Rollback/recovery: revert the M3 skill-body changes and preserve M1/M2 evidence for a smaller rewrite.

## Validation plan

- Use the smallest direct command first for each milestone, then selected CI for changed supported paths.
- Use temporary adapter archive output for adapter proof; do not hand-edit generated public adapter output.
- Run broad smoke only if the active plan, test spec, review-resolution, release metadata, selector output, or reviewer explicitly requires it.
- Before PR handoff, final verify must include skill validation, skill regression tests, generated-skill checks, adapter archive checks, review closeout validation, change metadata validation, artifact lifecycle validation, selected CI, and whitespace checks.

## Risks and recovery

- Risk: the next slice accidentally becomes an all-skill migration.
  Recovery: stop and revise the plan; only `implement` and `code-review` are in scope.
- Risk: rewriting `implement` weakens first-pass completeness, plan update ownership, or milestone handoff semantics.
  Recovery: use behavior-preservation evidence and code-review before closing M3.
- Risk: rewriting `code-review` weakens independent-review mode, material-finding recording, direct-proof expectations, or downstream routing.
  Recovery: use behavior-parity evidence and code-review before closing M3.
- Risk: new validation overfits wording.
  Recovery: keep checks deterministic, narrow, and fixture-backed; do not use broad semantic scoring.
- Risk: token cost regresses materially.
  Recovery: move rare detail out of the common path or reduce duplicated routing text before accepting the rewrite.

## Dependencies

- Plan-review must approve this plan before implementation.
- A test-spec amendment must be active and owner-approved before implementation starts.
- M1 evidence must exist before M2 or M3 relies on it.
- M2 must close before M3 unless M1/test-spec explicitly shows no validator changes are needed.
- M3 code-review must close before explain-change, verify, and PR handoff.

## Progress

- [x] 2026-05-19: PR #72 merge confirmed and prior spec-family rollout closed as done.
- [x] 2026-05-19: new execution/review rollout plan created.
- [x] Plan-review completed.
- [x] Test-spec amendment completed and approved.
- [x] M1 implemented; code-review pending.
- [ ] M2 implemented and reviewed.
- [ ] M3 implemented and reviewed.
- [ ] Explain-change recorded.
- [ ] Final verify passed.
- [ ] PR handoff completed.

## Decision log

- 2026-05-19: choose `implement` and `code-review` as the next rollout slice. Rationale: the merged proposal and spec-family slices covered authoring and review pairs upstream; execution and implementation review are the next smallest coherent pair and carry the highest workflow guardrail risk.
- 2026-05-19: keep all other skills out of scope for this slice. Rationale: small reviewable diffs matter more than broad simultaneous normalization.
- 2026-05-19: require test-spec amendment before implementation. Rationale: the current test spec is pilot/spec-family focused and should operationalize this new execution/review slice before skill-body changes.
- 2026-05-19: approve the plan with no material findings. Rationale: the plan keeps the next slice scoped to `implement` and `code-review`, preserves lifecycle sequencing, and requires test-spec amendment before implementation.
- 2026-05-19: amend `specs/skill-contract.test.md` with execution/review proof cases before implementation. Rationale: `T25`-`T28` make audit, deterministic validation, behavior preservation, generated-output, and adapter proof concrete for `implement` and `code-review`.
- 2026-05-19: keep M1 as evidence-only. Rationale: the audit found workflow-role and output-skeleton gaps in `implement` and `code-review`, but those skill-body changes belong to M3 after deterministic validator scope is settled.

## Surprises and discoveries

- None yet.

## Validation notes

- 2026-05-19 plan validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 plan validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 plan validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-implement-code-review.md docs/plan.md docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 plan selected CI: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-19 plan-review: `plan-review-r1` approved with no material findings; review evidence recorded under `docs/changes/2026-05-19-published-skill-design-implement-code-review/reviews/plan-review-r1.md`.
- 2026-05-19 plan-review validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-published-skill-design-implement-code-review` passed.
- 2026-05-19 plan-review validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 plan-review validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml --path docs/changes/2026-05-19-published-skill-design-implement-code-review/review-log.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/reviews/plan-review-r1.md` passed.
- 2026-05-19 plan-review validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-implement-code-review.md docs/plan.md docs/changes/2026-05-19-published-skill-design-implement-code-review` passed.
- 2026-05-19 plan-review selected CI: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml --path docs/changes/2026-05-19-published-skill-design-implement-code-review/review-log.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/reviews/plan-review-r1.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-19 test-spec: amended `specs/skill-contract.test.md` with execution/review rollout cases `T25`-`T28`.
- 2026-05-19 test-spec validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 test-spec validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 test-spec validation: `git diff --check -- specs/skill-contract.test.md docs/plans/2026-05-19-published-skill-design-implement-code-review.md docs/plan.md docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 test-spec selected CI: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-19 M1 evidence: created `skill-audit.md`, `routing-coverage.md`, `behavior-preservation.md`, and `behavior-parity.md` for the execution/review rollout.
- 2026-05-19 M1 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml` passed.
- 2026-05-19 M1 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml --path docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md --path docs/plan.md` passed.
- 2026-05-19 M1 validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-implement-code-review.md docs/plan.md docs/changes/2026-05-19-published-skill-design-implement-code-review` passed.
- 2026-05-19 M1 selected CI: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-implement-code-review.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/change.yaml --path docs/changes/2026-05-19-published-skill-design-implement-code-review/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-implement-code-review/behavior-parity.md` passed selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.

## Outcome and retrospective

- Pending. Do not use this section for current handoff state while the plan is active; see `Current Handoff Summary`.

## Readiness

- See `Current Handoff Summary`.

## Remaining completion gates

- Plan-review.
- Test-spec amendment.
- M1 through M3 implementation and code-review loops.
- Explain-change.
- Verify.
- PR handoff.
- Hosted PR CI and human review.
- Merge and final plan closeout.
