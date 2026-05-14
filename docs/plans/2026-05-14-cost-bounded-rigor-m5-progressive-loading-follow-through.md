# Cost-Bounded Rigor M5 Progressive-Loading Follow-Through Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-14
- Last updated: 2026-05-14
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: standard
- broad_smoke_required: false
- broad_smoke_reason: The planned slice audits three high-cost skill surfaces, records no-change rationale or minimal alignment, and adds only focused proof if the test spec requires it. It should not change release behavior, adapter packaging, generated-output tracking, selector behavior, broad-smoke triggers, token-report schemas, hard token gates, or benchmark-suite scope.
- lifecycle_token_cost_summary_required: false
- lifecycle_token_cost_summary_reason: The planned slice is narrow follow-through against an already completed progressive-loading baseline. It does not create a new workflow-governance reporting contract, release change, benchmark warning, or known broad-search incident. If implementation observes a relevant broad-search incident or a later accepted plan/test-spec trigger, M4 lifecycle-summary rules apply.

## Purpose / big picture

Plan the M5 cost-bounded-rigor slice after PR #57 merged the M4 lifecycle token-cost summary support.

The approved M5 spec defines progressive-loading follow-through for `workflow`, `implement`, and `code-review`. The purpose is to audit the current high-cost skill baseline, preserve or lightly align cost-bounded operating cues, and avoid redoing the already completed standalone progressive-loading initiative.

This plan keeps the implementation narrow. The intended implementation milestone audits the three high-cost skills first, records no-change rationale where the current baseline already satisfies M5, and permits only minimal skill or proof edits when the active test spec identifies a concrete gap.

## Source artifacts

- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted. The rollout names M5 as progressive-loading follow-through.
- M5 spec: [Cost-Bounded Rigor M5 Progressive-Loading Follow-Through](../../specs/cost-bounded-rigor-m5-progressive-loading-follow-through.md), approved after clean [spec-review-r1](../changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/spec-review-r1.md).
- Current test spec: none yet. The next downstream authoring artifact after plan-review is the M5 test spec.
- Architecture: not required. `spec-review-r1` found no runtime architecture, persistence, external API, deployment, data-contract, security-boundary, release packaging, adapter packaging, or executable selector behavior change.
- Completed progressive-loading baseline: [Progressive Loading for High-Cost Public Skills plan](2026-05-11-progressive-loading-high-cost-public-skills.md), done after PR #43.
- Completed M4 plan: [Cost-Bounded Rigor M4 Lifecycle Token-Cost Summary](2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md), done after merged PR #57.
- Change-local pack: [docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through](../changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/) records M5 spec and review evidence.
- Project map: [docs/project-map.md](../project-map.md) orients repository layout and skill/validation surfaces. This plan relies on direct source inspection for exact high-cost skill and validation-script state.

## Context and orientation

M5 sits between two already completed lines of work:

- the standalone progressive-loading initiative, which added quick operating guides, active-plan-first handoff cues, bounded evidence cues, static proof, dynamic benchmark evidence, and an optimization report for `workflow`, `implement`, and `code-review`;
- the cost-bounded-rigor M1-M4 slices, which added scope-budget guidance, bounded-evidence reminders, validation-budget guidance, and conditional lifecycle token-cost summaries.

Current high-cost skill surfaces already contain quick operating guide sections and bounded-evidence cues:

- `skills/workflow/SKILL.md` has a `Quick operating guide`, active-plan `Current Handoff Summary` guidance, bounded evidence wording, and workflow stage-owned claim boundaries.
- `skills/implement/SKILL.md` has a `Quick operating guide`, active-plan `Current Handoff Summary` first behavior for handoff readiness, bounded evidence wording, and implementation-owned claim boundaries.
- `skills/code-review/SKILL.md` has a `Quick operating guide`, active-plan handoff guidance when a plan exists, bounded evidence wording, independent-review behavior, material-finding rules, review recording, and claim boundaries.

Current proof surfaces include:

- `scripts/test-skill-validator.py`, which already contains progressive-loading and bounded-evidence checks;
- `scripts/validate-skills.py`, which validates canonical authored skill structure;
- `scripts/measure-skill-tokens.py`, which provides static token measurement evidence;
- selector and artifact lifecycle validation scripts, which select and validate changed lifecycle, skill, and change metadata paths.

M5 should not convert this audit into a broad skill rewrite. If current skills and proof already satisfy M5, the implementation should record no-change rationale and run focused validation.

## Non-goals

- Do not redo the full progressive-loading proposal or PR #43 implementation.
- Do not rewrite every skill.
- Do not add or track generated public adapter skill bodies as authored source.
- Do not change release packaging, adapter packaging, generated archive behavior, or generated-output publication.
- Do not change validation-selector behavior or broad-smoke triggers.
- Do not add hard token thresholds, hard CI blockers, or release gates based on token totals.
- Do not require dynamic benchmark comparison for no-change or small wording-only work unless the approved test spec or plan revision identifies material runtime risk.
- Do not move the full bounded-evidence guide out of `docs/workflows.md`.
- Do not weaken review, verification, material-finding, release, validation, or milestone-handoff safety rules.

## Requirements covered

| Requirement IDs | Planned implementation surface |
|---|---|
| `R1`-`R5` | High-cost skill audit, no-change rationale, and minimal edit guardrails in plan/test spec/implementation evidence. |
| `R6`-`R8` | Audit of quick operating guide, targeted reading, and broader-read escape cues in `workflow`, `implement`, and `code-review`; minimal skill or proof edits only if gaps are found. |
| `R9` | `workflow` audit for route-only behavior, source-of-truth order, stop conditions, and stage-owned claim boundaries. |
| `R10`-`R11` | `implement` audit for active-plan `Current Handoff Summary` first behavior and missing/contradictory handoff-state blocker behavior. |
| `R12` | `code-review` audit for independent-review mode, material findings, review recording, review-resolution routing, milestone handoff, and claim boundaries. |
| `R13`-`R14` | `docs/workflows.md` ownership and no long-template duplication checks. |
| `R15`-`R19` | Scope guardrails excluding broad skill rewrites, safety-critical deletion, hard token gates, selector/release/adapter/generated-output changes, and generated adapter body tracking. |
| `R20`-`R25` | Proof selection: skill validation and static token measurement when canonical skills change; diagnostic measurement only; dynamic benchmark comparison only when required or claimed; stable behavior-cue proof. |
| `R26`-`R30` | Preservation of PR #52 single-authored-source, PR #53 follow-up routing, M4 lifecycle-summary triggers, affected/unaffected surface records, and project-portable public skill wording. |

## Current Handoff Summary

- Current milestone: M0. Plan creation and spec status settlement
- Current milestone state: closed
- Last reviewed milestone: none
- Review status: `spec-review-r1` approved with no material findings
- Remaining in-scope implementation milestones: M1. High-cost skill audit and minimal follow-through
- Next stage: plan-review
- Final closeout readiness: not-ready
- Reason final closeout is or is not ready: M5 spec status is settled to approved, this active plan is created, and planning validation passed. Final closeout is not ready because plan-review, test-spec, implementation, code-review, explain-change, verify, and PR handoff remain.

## Milestones

### M0. Plan creation and spec status settlement

- Milestone state: closed
- Goal: Normalize the cleanly reviewed M5 spec to approved, create the active M5 plan, and register it in `docs/plan.md`.
- Requirements: M5 spec `R1`-`R30` as planning source; clean spec-review before reliance.
- Files/components likely touched:
  - `specs/cost-bounded-rigor-m5-progressive-loading-follow-through.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md`
  - `docs/plan.md`
  - `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
- Dependencies:
  - clean `spec-review-r1` recorded;
  - no open material findings in the M5 review log.
- Tests to add/update:
  - none; this milestone is lifecycle planning only.
- Implementation steps:
  - Confirm spec-review evidence is clean and recorded.
  - Normalize the M5 spec status from `draft` to `approved`.
  - Create this active M5 plan.
  - Add the active M5 plan entry to `docs/plan.md`.
  - Link the M5 plan from the accepted cost-bounded-rigor proposal follow-on artifacts.
  - Update M5 change metadata with planning requirements and validation evidence.
- Validation commands:
  - `python scripts/select-validation.py --mode explicit --path specs/cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plan.md --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/spec-review-r1.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plan.md --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/spec-review-r1.md`
  - `bash scripts/ci.sh --mode explicit --path specs/cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plan.md --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/spec-review-r1.md`
  - `git diff --check --`
- Expected observable result: The M5 spec is approved, this plan is active, `docs/plan.md` points to it, and the next stage is `plan-review`.
- Commit message: `Plan M5 progressive-loading follow-through`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed, when this planning commit is created
- Risks:
  - planning could accidentally reopen the completed progressive-loading implementation;
  - lifecycle state could drift between this plan and `docs/plan.md`.
- Rollback/recovery:
  - restore M5 spec to draft and remove this active plan/index entry if plan-review rejects the planning direction;
  - keep M4 as done because PR #57 is already merged.

### M1. High-cost skill audit and minimal follow-through

- Milestone state: planned
- Goal: Audit `workflow`, `implement`, and `code-review` against M5, then record no-change rationale or make the smallest necessary skill/proof edits.
- Requirements: `R1`-`R30`.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`, only if audit finds a concrete M5 gap
  - `skills/implement/SKILL.md`, only if audit finds a concrete M5 gap
  - `skills/code-review/SKILL.md`, only if audit finds a concrete M5 gap
  - `scripts/test-skill-validator.py`, only if the active test spec requires new stable proof or existing proof has a focused gap
  - `docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
- Files/components explicitly not planned for M1 unless the plan is revised after an approved test spec requires it:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - release and adapter packaging surfaces
  - generated public adapter skill bodies
  - dynamic benchmark manifest or runner behavior
  - token-cost release report schemas
- Dependencies:
  - M0 closed;
  - plan-review approval;
  - active M5 test spec;
  - maintainer approval of the M5 test spec before implementation;
  - no later accepted artifact broadening M5 into release, adapter, selector, benchmark-suite, generated-output, or hard-token-gate work.
- Tests to add/update:
  - Audit existing `scripts/test-skill-validator.py` coverage for quick guide, targeted reading, bounded evidence, active-plan handoff, and protected review behavior.
  - Add or update stable proof only if the M5 test spec identifies a concrete gap.
  - Use section-presence, required-term, behavior-cue, and forbidden-sequence checks instead of exact full-sentence assertions unless exact text is itself the contract.
- Implementation steps:
  - Audit `workflow`, `implement`, and `code-review` against M5 requirements and the active test spec.
  - Record each high-cost skill as unchanged with rationale, changed with rationale, or blocked/deferred with owner.
  - Preserve `docs/workflows.md` as the full bounded-evidence and workflow-routing guide.
  - If a skill edit is needed, make the smallest local wording or structure change that fixes the concrete gap.
  - If no skill edit is needed, do not churn skill text; record no-change rationale and validate existing proof.
  - Do not refresh generated public adapter output in this slice; release generation owns public adapter archives.
  - Decide whether static token measurement is required based on whether canonical skills changed; record a no-run rationale if no skill text changed.
  - Do not run dynamic benchmarks unless the active test spec or a plan revision requires them, or the change claims runtime improvement.
  - Record affected and unaffected surfaces for skills, selector behavior, release behavior, adapter behavior, generated-output tracking, benchmark behavior, and lifecycle token-cost summary behavior.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`, when canonical skill text changes or the test spec requires skill validation
  - `python scripts/measure-skill-tokens.py`, when canonical skill text changes or the test spec requires static measurement; otherwise record a no-run rationale
  - `python scripts/select-validation.py --mode explicit --path skills/workflow/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path skills/workflow/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - `git diff --check --`
- Expected observable result: M5 high-cost skill follow-through is complete through audit evidence, no-change rationale or minimal diffs, focused proof, and no expansion into release, adapter, selector, benchmark-suite, generated-output, or hard-token-gate work.
- Commit message: `M1: complete M5 high-cost skill follow-through`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - audit could become a broad rewrite of all public skills;
  - static proof could become brittle exact-prose enforcement;
  - a small skill edit could accidentally remove safety-critical review or handoff guidance;
  - dynamic benchmark work could be added without a test-spec trigger.
- Rollback/recovery:
  - revert unnecessary skill wording churn and keep no-change rationale;
  - reduce brittle proof to stable behavior cues;
  - restore removed safety-critical guidance or move detail only to an approved owner surface with rationale;
  - revise the plan before adding dynamic benchmarks, selector behavior changes, release behavior, adapter packaging, generated-output publication, or hard token gates.

## Validation plan

Before implementation:

- M5 spec is approved.
- This plan is reviewed by `plan-review`.
- An active M5 test spec is created and approved or otherwise ready according to workflow state.

During implementation:

- Run focused proof first where the test spec requires new or changed static checks.
- Run the smallest selected validation set that covers changed paths and proof surfaces.
- Run `python scripts/test-skill-validator.py` whenever static skill-proof behavior is relied on.
- Run `python scripts/validate-skills.py` and `python scripts/measure-skill-tokens.py` when canonical skills change, unless the active test spec explicitly permits narrower proof and records a rationale.
- Do not run dynamic benchmarks unless the plan/test spec requires them or the change claims runtime improvement.

Before PR:

- Run review-artifact closeout validation when review records exist.
- Run change metadata validation.
- Run artifact lifecycle validation for touched lifecycle artifacts.
- Run selected CI for the final changed path set.
- Run `git diff --check --`.

## Risks and recovery

| Risk | Recovery |
|---|---|
| M5 reopens the full progressive-loading initiative. | Stop, preserve the completed baseline, and narrow implementation to audit/no-change rationale or a minimal concrete gap. |
| Skill edits remove safety-critical guidance. | Restore the guidance or route any movement to an approved owner surface with explicit rationale and review coverage. |
| Static proof becomes brittle exact prose. | Replace exact full-sentence assertions with stable section, required-term, behavior-cue, and forbidden-sequence checks. |
| Dynamic benchmarks become routine overhead. | Require them only when the active plan/test spec identifies material runtime risk or the change claims runtime improvement. |
| Generated adapter output is treated as authored source. | Keep `skills/` as authored truth and leave generated public adapter bodies to release archives. |
| Lifecycle token-cost summaries become routine. | Apply the M4 triggers only when a real trigger exists; otherwise record no-summary rationale. |

## Dependencies

- Clean M5 spec-review evidence is recorded.
- M5 spec status is approved before downstream reliance.
- `plan-review` must approve this plan before test-spec authoring relies on it.
- Test-spec must map every M5 `MUST` to concrete tests, static proof, no-change rationale, or manual review before implementation.
- Implementation must not start until the active M5 test spec is approved by the maintainer or accepted by the workflow state.

## Progress

- [x] M5 spec drafted.
- [x] M5 spec-review recorded clean approval.
- [x] M5 spec status normalized to approved.
- [x] M5 plan created.
- [x] M5 plan indexed in `docs/plan.md`.
- [ ] Plan-review complete.
- [ ] Test spec created.
- [ ] Test spec maintainer-approved.
- [ ] M1 implementation started.
- [ ] M1 implemented.
- [ ] M1 code-review complete.
- [ ] Explain-change recorded.
- [ ] Verify complete.
- [ ] PR handoff complete.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-14 | Treat completed progressive-loading work as M5 baseline. | The standalone proposal/spec/plan already completed the broad optimization; M5 should avoid duplicating that work. |
| 2026-05-14 | Keep M5 to one implementation milestone. | The expected work is audit/no-change rationale or a small targeted skill/proof adjustment, not multiple workstreams. |
| 2026-05-14 | Do not require dynamic benchmarks by default. | M5 does not claim runtime improvement unless the later test spec or implementation does so. |
| 2026-05-14 | Do not require a lifecycle token-cost summary by default. | The planned slice is narrow follow-through and does not create a new reporting contract or release change. |

## Surprises and discoveries

- Current `workflow`, `implement`, and `code-review` skills already contain quick operating guides, active-plan or handoff-state cues, bounded-evidence wording, and claim-boundary sections. M1 should audit before editing.
- Existing skill-validator tests already include progressive-loading and bounded-evidence proof surfaces. M1 should prefer reusing existing proof unless the M5 test spec finds a focused gap.

## Validation notes

- 2026-05-14: Plan creation validation passed after spec status settlement and plan-index update: selected validation, review-artifact closeout, change metadata validation, artifact lifecycle validation, selected CI, and `git diff --check --`.

## Outcome and retrospective

- Not complete yet. M5 is planned and ready for `plan-review`.

## Readiness

- See `Current Handoff Summary`.
- Ready for `plan-review`.
