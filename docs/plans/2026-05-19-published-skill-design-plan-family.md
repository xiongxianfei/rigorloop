# Published Skill Design Plan Family Rollout Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-19
- Last updated: 2026-05-19
- Related proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md)
- Related spec: [Skill Contract](../../specs/skill-contract.md)
- Related test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md)
- Related prior rollout: [Published Skill Design Spec Family Rollout](2026-05-19-published-skill-design-spec-family.md)
- Change root: [docs/changes/2026-05-19-published-skill-design-plan-family](../changes/2026-05-19-published-skill-design-plan-family/change.yaml)
- Supersedes: none

## Purpose / big picture

Continue the published-skill design rollout after the merged proposal-family and spec-family slices by applying the same contract to the next lifecycle pair: `plan` and `plan-review`.

This plan keeps the rollout incremental. The planning pair owns active execution planning and formal plan review, including milestone state, current handoff summaries, review recording, and readiness boundaries. Those behaviors are important enough to deserve their own slice before touching the higher-risk `implement` and `code-review` pair.

## Source artifacts

- Proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md), accepted.
- Proposal review: [proposal-review-r2](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r2.md), approved.
- Spec: [Skill Contract](../../specs/skill-contract.md), approved after [spec-review-r3](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/spec-review-r3.md).
- Test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), active for the merged pilot and spec-family rollout; to be amended for this plan-family slice during `test-spec`.
- Prior rollout: [Published Skill Design Spec Family Rollout](2026-05-19-published-skill-design-spec-family.md), done after PR #72 merged and hosted CI passed.
- Architecture: not required. This slice changes canonical skill text, deterministic validator fixtures only if needed, and change-local lifecycle evidence. It does not add runtime components, persistence, APIs, deployment, or hard-to-reverse data flow.
- Project map: [RigorLoop Project Map](../project-map.md), available as orientation only.

## Context and orientation

- PR #71 merged the proposal-family pilot for `proposal` and `proposal-review`.
- PR #72 merged the spec-family rollout for `spec` and `spec-review`.
- `skills/` remains the only authored skill source.
- Generated public adapter skill bodies are release archives for `v0.1.3` and later. Do not hand-edit generated adapter package output.
- The next skill body edit scope is limited to:
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
- The next slice may extend deterministic validator fixtures only when needed for the plan pair. It must not broaden validation into natural-language scoring or runtime auto-selection proof.
- Change-local audit, routing coverage, behavior-preservation, behavior-parity, and token evidence for this slice should live under `docs/changes/2026-05-19-published-skill-design-plan-family/`.
- `plan` owns creating or revising concrete plan bodies and the `docs/plan.md` lifecycle index when an initiative starts or is replanned.
- `plan-review` is a formal review gate. It must preserve durable review evidence, material finding recording, downstream-blocking semantics, and the boundary between plan readiness and implementation completion.

## Non-goals

- Do not rewrite all skills.
- Do not edit `implement`, `code-review`, `verify`, `pr`, or `workflow` in this slice.
- Do not merge, retire, rename, remove, or change ownership of any skill.
- Do not change workflow stage order, milestone-state vocabulary, review-resolution semantics, adapter install roots, lockfile semantics, release archive trust boundaries, or CLI behavior.
- Do not add a required `when_to_use` frontmatter field.
- Do not introduce broad semantic scoring of skill prose or CI claims about deterministic model auto-selection.
- Do not add a build-time partial/include system.
- Do not require resource-map sections for skills without packaged resources.
- Do not claim final verification, branch readiness, PR readiness, or Done from this plan stage.

## Requirements covered

| Requirement | Planned coverage |
| --- | --- |
| R27-R28 | Audit `plan` and `plan-review` against the existence gate and portable operating-documentation standard. |
| R29 | Ensure `description` is the portable routing surface for execution planning and plan review, including near-miss boundaries against `spec`, `test-spec`, `implement`, and `code-review`. |
| R30-R31 | Ensure lifecycle role, normal-path execution procedure, stop conditions, body-routing boundaries, and claim boundaries are explicit without duplicating all routing text. |
| R32-R33 | Confirm no missing resource maps or required repository-root internal dependencies are introduced. |
| R34 | Preserve or improve compact output skeletons for plans and plan-review results. |
| R35 | Create deterministic routing coverage tables and prompt fixture expectations for the plan pair. |
| R36 principles | Reuse the pilot's audit-first, behavior-preservation, behavior-parity, and token-cost discipline without applying the pilot-only `proposal`/`proposal-review` edit boundary to this follow-on slice. |

## Current Handoff Summary

- Current milestone: M1. Plan Family Audit And Evidence Scaffold
- Current milestone state: review-requested
- Last reviewed milestone: none
- Review status: plan-review-r1 approved with no material findings
- Remaining in-scope implementation milestones: M1, M2, M3
- Next stage: code-review for M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 evidence is implemented and ready for code-review, but M1 review, M2, M3, explain-change, verify, and PR handoff remain open.

## Milestones

### M1. Plan Family Audit And Evidence Scaffold

- Milestone state: review-requested
- Goal: create the change-local evidence structure for `plan` and `plan-review` before changing validators or skill bodies.
- Requirements: R27-R31, R34-R35, R36 audit/preservation/parity discipline.
- Files/components likely touched:
  - `docs/changes/2026-05-19-published-skill-design-plan-family/skill-audit.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
- Dependencies: approved plan-review for this plan and owner-approved test spec amendment for this slice before implementation.
- Tests to add/update: none in M1 unless the test-spec amendment requires new evidence-file selector fixtures first.
- Implementation steps:
  - Audit `plan` and `plan-review` descriptions, workflow-role blocks, output skeletons, stop conditions, review-recording obligations, and self-containment wording.
  - Record whether each skill earns its existence through a durable artifact contract, lifecycle procedure, review responsibility, output shape, validation behavior, or trust boundary.
  - Record routing coverage tables for obvious positives, casual positives, edge positives, near negatives, competing-skill prompts, and should-not-trigger prompts.
  - Record behavior-preservation notes for behavior-significant wording that might be rewritten.
  - Define representative plan and plan-review artifacts for behavior parity, including milestone handoff state and material finding outcomes.
  - Record baseline static token estimates for `plan` and `plan-review`.
- Implementation result:
  - Created `skill-audit.md`, `routing-coverage.md`, `behavior-preservation.md`, and `behavior-parity.md` under the plan-family change root.
  - Recorded that both skills earn their existence and neither is a merge/retire candidate in this slice.
  - Recorded routing tables and prompt fixture expectations for `plan` and `plan-review`.
  - Recorded behavior-preservation targets for plan state ownership, upstream status settlement, readiness-vs-Done, review recording, material finding shape, and handoff boundaries.
  - Recorded baseline token estimates: `plan` 3518 and `plan-review` 1631.
  - Found no production validator gap that must be fixed before M3; M2 remains conditional and should add only deterministic evidence checks if needed.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml --path docs/plan.md`
  - `git diff --check -- docs/plans/2026-05-19-published-skill-design-plan-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-plan-family`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
- Expected observable result: reviewers can inspect evidence before any plan-family skill wording changes.
- Commit message: `M1: scaffold published skill design plan-family evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: audit scope could expand into `implement` or `code-review`.
- Rollback/recovery: remove or revise change-local evidence files; no canonical skills are changed in this milestone.

### M2. Plan Family Validator And Fixture Support

- Milestone state: planned
- Goal: make any deterministic checks needed for `plan` and `plan-review` enforceable without broad semantic scoring.
- Requirements: R29, R32-R33, R35.
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `specs/skill-contract.test.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
- Dependencies: M1 evidence and approved test-spec amendment.
- Tests to add/update:
  - Add or reuse focused fixtures for plan-family routing coverage, output skeletons, body routing boundaries, and self-containment only when deterministic gaps are found.
  - Add regression coverage only for deterministic failure modes discovered by M1 or already required by R27-R35.
  - Keep repository-root versus packaged-resource checks unchanged unless M1 exposes a same-class gap.
- Implementation steps:
  - Extend existing published-design checks only where the plan pair needs deterministic coverage.
  - Avoid adding runtime skill-selection claims.
  - Keep checks phrase/path/table based.
  - Record a no-production-validator-change rationale if M1 exposes no deterministic production validator gap.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
  - `git diff --check -- scripts tests specs docs/plans/2026-05-19-published-skill-design-plan-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-plan-family`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
- Expected observable result: deterministic validation can support the plan-family rewrite without pretending to judge prose quality broadly.
- Commit message: `M2: validate published skill design plan-family checks`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: validator changes could over-block legitimate plan-review wording or evidence files.
- Rollback/recovery: revert validator/fixture changes and keep M1 evidence for replanning.

### M3. Plan And Plan-Review Skill Rewrite

- Milestone state: planned
- Goal: update only `plan` and `plan-review` to the published-skill design contract.
- Requirements: R27-R35 and M1 preservation/parity evidence.
- Files/components likely touched:
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-preservation.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/behavior-parity.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md`
  - `docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
- Dependencies: M1 and M2 closed or explicitly found no validator changes needed.
- Tests to add/update:
  - Update focused validator tests if the skill opt-in shape requires it.
  - No broad semantic scoring or runtime model-selection tests.
- Implementation steps:
  - Tighten `description` routing for `plan` and `plan-review`, including competing-skill near misses.
  - Keep `SKILL.md` bodies execution-focused and preserve compact output skeletons.
  - Preserve `plan` ownership of concrete plan bodies, `docs/plan.md` indexing at initiative start/replanning, current handoff summaries, milestone states, readiness-vs-Done boundaries, and upstream status settlement.
  - Preserve `plan-review` ownership of plan critique, formal review recording, material finding shape, downstream-blocking semantics, and no-implementation/no-verification claim boundaries.
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
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
  - `git diff --check -- skills/plan/SKILL.md skills/plan-review/SKILL.md specs/skill-contract.test.md docs/plans/2026-05-19-published-skill-design-plan-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-plan-family`
  - `bash scripts/ci.sh --mode explicit --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml`
- Expected observable result: `plan` and `plan-review` route more reliably, remain portable, preserve lifecycle claim boundaries, and validate from canonical skill source.
- Commit message: `M3: roll out published skill design to plan family`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: readability or routing rewrites could weaken plan-state ownership, review recording, or readiness boundaries.
- Rollback/recovery: revert the M3 skill-body changes and preserve M1/M2 evidence for a smaller rewrite.

## Validation plan

- Use the smallest direct command first for each milestone, then selected CI for changed supported paths.
- Use temporary adapter archive output for adapter proof; do not hand-edit generated public adapter output.
- Run broad smoke only if the active plan, test spec, review-resolution, release metadata, selector output, or reviewer explicitly requires it.
- Before PR handoff, final verify must include skill validation, skill regression tests, generated-skill checks, adapter archive checks, review closeout validation, change metadata validation, artifact lifecycle validation, selected CI, and whitespace checks.

## Risks and recovery

- Risk: the next slice accidentally becomes an `implement` or `code-review` migration.
  Recovery: stop and revise the plan; only `plan` and `plan-review` are in scope.
- Risk: rewriting `plan` weakens active plan state ownership, upstream status settlement, or readiness-vs-Done language.
  Recovery: use behavior-preservation evidence and code-review before closing M3.
- Risk: rewriting `plan-review` weakens formal review recording, material finding requirements, or downstream-blocking semantics.
  Recovery: preserve representative parity cases for clean review, changes-requested review, and blocked recording before closing M3.
- Risk: new validation overfits wording.
  Recovery: keep checks deterministic, narrow, and fixture-backed; do not use broad semantic scoring.
- Risk: token cost regresses materially.
  Recovery: move rare detail out of the common path or reduce duplicated routing text before accepting the rewrite.

## Dependencies

- Plan-review must approve this plan before implementation.
- A test-spec amendment must be active and owner-approved before implementation starts.
- M1 evidence must exist before M2 or M3 relies on it.
- M2 must close before M3 unless M1/test-spec explicitly shows no validator changes are needed.
- Each implementation milestone must receive code-review before it closes.
- All in-scope implementation milestones must close before explain-change, verify, and PR handoff.

## Progress

- [x] 2026-05-19: PR #71 merge confirmed for the proposal-family pilot.
- [x] 2026-05-19: PR #72 merge confirmed for the spec-family rollout.
- [x] 2026-05-19: new plan-family rollout plan created.
- [x] Plan-review completed.
- [x] Test-spec amendment completed.
- [x] Test-spec amendment approved.
- [x] M1 implemented.
- [ ] M1 reviewed.
- [ ] M2 implemented and reviewed.
- [ ] M3 implemented and reviewed.
- [ ] Explain-change recorded.
- [ ] Final verify completed.
- [ ] PR handoff completed.

## Decision log

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-05-19 | Continue with `plan` and `plan-review` before `implement` and `code-review`. | The planning pair is the next lifecycle pair after spec review and has enough stage ownership to benefit from a dedicated slice. `implement` and `code-review` are higher-risk and should follow separately. |
| 2026-05-19 | Keep validator changes conditional in M2. | The previous rollout found some proof gaps belonged in test scaffolding rather than production validation; this slice should only add deterministic checks when the audit identifies a concrete need. |
| 2026-05-19 | Keep the test spec amendment before implementation. | The skill-contract test spec currently names the completed spec-family rollout; this plan-family slice needs its own traceable test coverage before skill-body rewrites begin. |
| 2026-05-19 | Treat M2 production validator changes as conditional after M1. | The M1 audit found evidence-scaffold and future test needs, but no production validator gap that must be fixed before M3. |

## Surprises and discoveries

- M1 found both `plan` and `plan-review` need explicit `Workflow role` blocks in M3, but both already have compact result skeletons and portable project-local path handling.
- M1 found no merge, retire, rename, ownership-change, or mandatory production-validator-change candidate for this slice.

## Validation notes

- 2026-05-19 plan validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed.
- 2026-05-19 plan validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed.
- 2026-05-19 plan validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-plan-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed.
- 2026-05-19 plan selected CI: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed selected artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 plan-review: `plan-review-r1` approved with no material findings; review evidence recorded under `docs/changes/2026-05-19-published-skill-design-plan-family/reviews/plan-review-r1.md`.
- 2026-05-19 test-spec: amended `specs/skill-contract.test.md` with plan-family test cases `T25` through `T28`.
- 2026-05-19 test-spec validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed.
- 2026-05-19 test-spec validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed.
- 2026-05-19 test-spec validation: `git diff --check -- specs/skill-contract.test.md docs/plans/2026-05-19-published-skill-design-plan-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed.
- 2026-05-19 test-spec selected CI: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.test.md --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed selected artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 test-spec approval: user approved the plan-family test-spec amendment before implementation.
- 2026-05-19 M1 evidence: created `skill-audit.md`, `routing-coverage.md`, `behavior-preservation.md`, and `behavior-parity.md` for the plan-family rollout.
- 2026-05-19 M1 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml` passed.
- 2026-05-19 M1 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml --path docs/changes/2026-05-19-published-skill-design-plan-family/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-plan-family/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-plan-family/behavior-parity.md --path docs/plan.md` passed.
- 2026-05-19 M1 validation: `git diff --check -- docs/plans/2026-05-19-published-skill-design-plan-family.md docs/plan.md docs/changes/2026-05-19-published-skill-design-plan-family` passed.
- 2026-05-19 M1 selected CI: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-published-skill-design-plan-family.md --path docs/plan.md --path docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml --path docs/changes/2026-05-19-published-skill-design-plan-family/skill-audit.md --path docs/changes/2026-05-19-published-skill-design-plan-family/routing-coverage.md --path docs/changes/2026-05-19-published-skill-design-plan-family/behavior-preservation.md --path docs/changes/2026-05-19-published-skill-design-plan-family/behavior-parity.md` passed selected artifact-lifecycle, change-metadata regression, and change-metadata checks.

## Outcome and retrospective

- Pending completion.

## Readiness

Ready for `code-review` for M1.

Remaining completion gates: M1 code-review, M2 and M3 implementation and code-review, explain-change, verify, PR handoff, hosted CI observation if a PR is opened, merge, and final lifecycle closeout when no downstream gate remains.
