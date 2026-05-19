# Published Skill Design Spec Family Rollout Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-19
- Last updated: 2026-05-19
- Related proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md)
- Related spec: [Skill Contract](../../specs/skill-contract.md)
- Related pilot: [RigorLoop Published Skill Design Contract Execution Plan](2026-05-19-rigorloop-published-skill-design-contract.md)
- Change root: [docs/changes/2026-05-19-published-skill-design-spec-family](../changes/2026-05-19-published-skill-design-spec-family/change.yaml)
- Supersedes: none

## Purpose / big picture

Continue the published-skill design work after the merged `proposal` and `proposal-review` pilot by applying the contract to the next smallest lifecycle pair: `spec` and `spec-review`.

This plan deliberately keeps the next rollout narrow. The merged pilot proved the contract on the proposal pair; this slice should improve the specification pair without rewriting every skill, changing skill ownership, or making runtime model-selection claims.

## Source artifacts

- Proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md), accepted.
- Proposal review: [proposal-review-r2](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r2.md), approved.
- Spec: [Skill Contract](../../specs/skill-contract.md), approved after [spec-review-r3](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/spec-review-r3.md).
- Test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), active for the merged pilot and to be amended for this next slice during `test-spec`.
- Architecture: not required. This change affects canonical skill text, deterministic validation, fixtures, and generated adapter validation; it does not add runtime components, persistence, APIs, deployment, or hard-to-reverse data flow.
- Project map: [RigorLoop Project Map](../project-map.md), available as orientation only.

## Context and orientation

- PR #71 merged the first published-skill design pilot and changed only `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, validator support, selector support, and pilot evidence.
- `skills/` remains the only authored skill source.
- Generated public adapter skill bodies are release archives for `v0.1.3` and later. Do not hand-edit generated adapter package output.
- The next skill body edit scope is limited to:
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
- The next slice may extend deterministic validator fixtures only when needed for the spec pair. It must not broaden validation into natural-language scoring or runtime auto-selection proof.
- Change-local audit, routing coverage, behavior-preservation, behavior-parity, and token evidence for this slice should live under `docs/changes/2026-05-19-published-skill-design-spec-family/`.

## Non-goals

- Do not rewrite all skills.
- Do not merge, retire, rename, remove, or change ownership of any skill.
- Do not edit `proposal` or `proposal-review` again unless validation exposes drift from the merged pilot.
- Do not add a required `when_to_use` frontmatter field.
- Do not introduce broad semantic scoring of skill prose or CI claims about deterministic model auto-selection.
- Do not add a build-time partial/include system.
- Do not change adapter install roots, lockfile semantics, release archive trust boundaries, or CLI behavior.
- Do not require resource-map sections for skills without packaged resources.

## Requirements covered

| Requirement | Planned coverage |
| --- | --- |
| R27-R28 | Audit `spec` and `spec-review` against the existence gate and portable operating-documentation standard. |
| R29 | Ensure `description` is the portable routing surface for spec authoring and spec review, including near-miss boundaries. |
| R30-R31 | Ensure lifecycle role, execution procedure, and body-routing boundaries are explicit without duplicating all routing text. |
| R32-R33 | Confirm no missing resource maps or required repository-root internal dependencies are introduced. |
| R34 | Preserve or improve compact output skeletons for spec and spec-review artifacts. |
| R35 | Create deterministic routing coverage tables and prompt fixture expectations for the spec pair. |
| R36 principles | Reuse the pilot's audit-first, behavior-preservation, behavior-parity, and token-cost discipline without applying the pilot-only `proposal`/`proposal-review` edit boundary to this new slice. |

## Current Handoff Summary

- Current milestone: M1. Spec Family Audit And Evidence Scaffold
- Current milestone state: review-requested
- Last reviewed milestone: planning
- Review status: plan-review-r1 approved; no material findings
- Remaining in-scope implementation milestones: M1 code-review, M2, M3
- Next stage: code-review for M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 code-review, later implementation milestones, explain-change, verify, and PR handoff remain.

## Milestones

### M1. Spec Family Audit And Evidence Scaffold

- Milestone state: review-requested
- Goal: create the change-local evidence structure for `spec` and `spec-review` before changing validators or skill bodies.
- Requirements: R27-R31, R34-R35, R36 audit/preservation/parity discipline.
- Files/components likely touched:
  - `docs/changes/2026-05-19-published-skill-design-spec-family/skill-audit.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
- Dependencies: approved plan-review for this plan and owner-approved test spec amendment for this slice before implementation.
- Tests to add/update: none in M1 unless the test-spec amendment requires new evidence-file selector fixtures first.
- Implementation steps:
  - Audit `spec` and `spec-review` descriptions, workflow-role blocks, output skeletons, stop conditions, and self-containment wording.
  - Record routing coverage tables for obvious positives, casual positives, edge positives, near negatives, competing-skill prompts, and should-not-trigger prompts.
  - Record behavior-preservation notes for behavior-significant wording that might be rewritten.
  - Define representative spec and spec-review artifacts for behavior parity.
  - Record baseline static token estimates for `spec` and `spec-review`.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - `git diff --check -- docs/plans/2026-05-19-published-skill-design-spec-family.md docs/changes/2026-05-19-published-skill-design-spec-family`
- Expected observable result: reviewers can inspect evidence before any spec-family skill wording changes.
- Commit message: `M1: scaffold published skill design spec-family evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated
  - validation notes updated
  - milestone committed
- Risks: audit scope could expand into broad all-skill rewrite.
- Rollback/recovery: remove or revise change-local evidence files; no canonical skills are changed in this milestone.

### M2. Spec Family Validator And Fixture Support

- Milestone state: planned
- Goal: make any deterministic checks needed for `spec` and `spec-review` enforceable without broad semantic scoring.
- Requirements: R29, R32-R33, R35.
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `specs/skill-contract.test.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
- Dependencies: M1 evidence and approved test-spec amendment.
- Tests to add/update:
  - Add or reuse focused fixtures for spec-family routing coverage and body routing boundaries.
  - Add regression coverage only for deterministic failure modes discovered by M1.
  - Keep repository-root versus packaged-resource checks unchanged unless M1 exposes a same-class gap.
- Implementation steps:
  - Extend existing published-design checks only where the spec pair needs deterministic coverage.
  - Avoid adding runtime skill-selection claims.
  - Keep checks phrase/path/table based.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - `git diff --check -- scripts tests specs docs/changes/2026-05-19-published-skill-design-spec-family`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path specs/skill-contract.test.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
- Expected observable result: deterministic validation can support the spec-family rewrite without pretending to judge prose quality broadly.
- Commit message: `M2: validate published skill design spec-family checks`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: selector or validator changes could over-block future change-local proof files.
- Rollback/recovery: revert validator/fixture changes and keep M1 evidence for replanning.

### M3. Spec And Spec-Review Skill Rewrite

- Milestone state: planned
- Goal: update only `spec` and `spec-review` to the published-skill design contract.
- Requirements: R27-R35 and M1 preservation/parity evidence.
- Files/components likely touched:
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
- Dependencies: M1 and M2 closed or explicitly found no validator changes needed.
- Tests to add/update:
  - Update focused validator tests if the skill opt-in shape requires it.
  - No broad semantic scoring or runtime model-selection tests.
- Implementation steps:
  - Tighten `description` routing for `spec` and `spec-review`, including competing-skill near misses.
  - Keep `SKILL.md` bodies execution-focused and preserve output skeletons.
  - Remove or reframe any required maintainer-only repository dependency if found.
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
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
  - `git diff --check -- skills/spec/SKILL.md skills/spec-review/SKILL.md specs/skill-contract.test.md docs/plans/2026-05-19-published-skill-design-spec-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-spec-family`
  - `bash scripts/ci.sh --mode explicit --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
- Expected observable result: `spec` and `spec-review` route more reliably, remain portable, preserve lifecycle claim boundaries, and validate from canonical skill source.
- Commit message: `M3: roll out published skill design to spec family`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: spec-review has formal review recording obligations that must not be weakened by readability or routing rewrites.
- Rollback/recovery: revert the M3 skill-body changes and preserve M1/M2 evidence for a smaller rewrite.

## Validation plan

- Use the smallest direct command first for each milestone, then selected CI for changed supported paths.
- Use temporary adapter archive output for adapter proof; do not hand-edit generated public adapter output.
- Run broad smoke only if the active plan, test spec, review-resolution, release metadata, selector output, or reviewer explicitly requires it.
- Before PR handoff, final verify must include skill validation, skill regression tests, generated-skill checks, adapter archive checks, review closeout validation, change metadata validation, artifact lifecycle validation, selected CI, and whitespace checks.

## Risks and recovery

- Risk: the next slice accidentally becomes an all-skill migration.
  Recovery: stop and revise the plan; only `spec` and `spec-review` are in scope.
- Risk: rewriting `spec-review` weakens material-finding, recording, or downstream-blocking semantics.
  Recovery: use behavior-preservation evidence and code-review before closing M3.
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

- [x] 2026-05-19: PR #71 merge confirmed; prior pilot plan closed as done.
- [x] 2026-05-19: new spec-family rollout plan created.
- [x] Plan-review completed.
- [x] Test-spec amendment completed and approved.
- [x] M1 implemented; code-review pending.
- [ ] M2 implemented and reviewed.
- [ ] M3 implemented and reviewed.
- [ ] Explain-change recorded.
- [ ] Final verify passed.
- [ ] PR handoff completed.

## Decision log

- 2026-05-19: choose `spec` and `spec-review` as the next rollout slice. Rationale: the merged pilot covered proposal authoring and proposal review; the next lifecycle pair is the smallest coherent extension of the same contract.
- 2026-05-19: keep all other skills out of scope for this slice. Rationale: small reviewable diffs matter more than broad simultaneous normalization.
- 2026-05-19: require test-spec amendment before implementation. Rationale: the existing test spec is pilot-focused and should operationalize this new spec-family slice before code or skill-body changes.
- 2026-05-19: approve the plan with no material findings. Rationale: the plan keeps the next slice scoped to `spec` and `spec-review`, preserves lifecycle sequencing, and requires test-spec amendment before implementation.
- 2026-05-19: amend `specs/skill-contract.test.md` with spec-family proof cases before implementation. Rationale: `T21`-`T24` make audit, deterministic validation, behavior preservation, generated-output, and adapter proof concrete for `spec` and `spec-review`.
- 2026-05-19: keep M1 as evidence-only. Rationale: the audit found workflow-role and output-skeleton gaps in `spec` and `spec-review`, but those skill-body changes belong to M3 after deterministic validator scope is settled.

## Surprises and discoveries

- None yet.

## Validation notes

- 2026-05-19 plan validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 plan validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 plan validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-spec-family.md docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml docs/plan.md docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 plan validation: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml --path docs/plan.md --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed selected artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 plan-review: `plan-review-r1` approved with no material findings; review evidence recorded under `docs/changes/2026-05-19-published-skill-design-spec-family/reviews/plan-review-r1.md`.
- 2026-05-19 plan-review validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-published-skill-design-spec-family` passed.
- 2026-05-19 plan-review validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml` passed.
- 2026-05-19 plan-review validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml --path docs/changes/2026-05-19-published-skill-design-spec-family/review-log.md --path docs/changes/2026-05-19-published-skill-design-spec-family/reviews/plan-review-r1.md` passed.
- 2026-05-19 plan-review validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-spec-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-spec-family` passed.
- 2026-05-19 plan-review selected CI: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml --path docs/changes/2026-05-19-published-skill-design-spec-family/review-log.md --path docs/changes/2026-05-19-published-skill-design-spec-family/reviews/plan-review-r1.md` passed selected review-artifacts, artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 test-spec: amended `specs/skill-contract.test.md` with spec-family rollout cases `T21`-`T24`.
- 2026-05-19 test-spec validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml` passed.
- 2026-05-19 test-spec validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml` passed.
- 2026-05-19 test-spec validation: `git diff --check -- specs/skill-contract.test.md docs/plans/2026-05-19-published-skill-design-spec-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml` passed.
- 2026-05-19 test-spec selected CI: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml` passed selected artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 M1 evidence: created `skill-audit.md`, `routing-coverage.md`, `behavior-preservation.md`, and `behavior-parity.md` for the spec-family rollout.
- 2026-05-19 M1 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml` passed.
- 2026-05-19 M1 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml --path docs/changes/2026-05-19-published-skill-design-spec-family/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-spec-family/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-spec-family/behavior-parity.md --path docs/plan.md` passed.
- 2026-05-19 M1 validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-spec-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-spec-family` passed.
- 2026-05-19 M1 selected CI: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-spec-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml --path docs/changes/2026-05-19-published-skill-design-spec-family/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-spec-family/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-spec-family/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-spec-family/behavior-parity.md` passed selected artifact-lifecycle, change-metadata regression, and change-metadata checks.

## Outcome and retrospective

- Pending. Do not use this section for current handoff state while the plan is active; see `Current Handoff Summary`.

## Readiness

- See `Current Handoff Summary`.
- This plan is ready for `code-review` of M1, not final closeout or PR readiness.

## Remaining completion gates

- M1 implementation and code-review
- M2 implementation and code-review
- M3 implementation and code-review
- `explain-change`
- `verify`
- `pr`
