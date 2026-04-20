# Plan index lifecycle ownership plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-20
- Last updated: 2026-04-20
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved plan-index lifecycle ownership change so `docs/plan.md` remains a trustworthy lifecycle index and plan bodies stop drifting away from the real initiative state.

This initiative exists because the repository already hit the failure mode the spec describes: a finished initiative remained under `## Active`, later work had to reason around stale guidance, and lifecycle-closeout ownership stayed too implicit across `plan`, `implement`, `verify`, `pr`, and `learn`.

The implementation needs to do three things in one coherent sequence:

- update the normative and summary workflow guidance;
- align the canonical skill instructions and regenerate `.codex/skills/`;
- migrate the plan template and any already-known stale plan/index state to the clarified ownership model.

## Source artifacts

- Proposal: `docs/proposals/2026-04-20-plan-index-lifecycle-ownership.md`
- Spec: `specs/plan-index-lifecycle-ownership.md`
- Spec-review findings:
  - the user explicitly confirmed in chat on 2026-04-20 that spec generation and review are complete and planning should continue;
  - no standalone tracked spec-review artifact exists yet, so implementation should rely on the current reviewed spec text and record any later review-resolution in tracked artifacts if needed.
- Architecture context:
  - `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
  - `docs/adr/ADR-20260419-repository-source-layout.md`
  - these are background constraints only; no new architecture artifact is planned because this initiative changes workflow ownership and plan-state handling, not repository layout.
- Test spec: `specs/plan-index-lifecycle-ownership.test.md`
- Related evidence:
  - `docs/explain/2026-04-20-constitution-governance-migration.md` already records the stale-plan follow-up that motivated this initiative.

## Context and orientation

- `docs/plan.md` is the repository index of `Active`, `Blocked`, `Done`, and `Superseded` plans. It is not the body of a plan.
- Concrete plan bodies live under `docs/plans/` and currently expose lifecycle state through a mix of:
  - the top status line;
  - progress notes;
  - readiness wording;
  - outcome and retrospective text.
- Current contributor-facing workflow guidance is split across:
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - canonical skill instructions under `skills/`
  - generated Codex compatibility output under `.codex/skills/`
- The canonical-versus-generated boundary already exists:
  - edit `skills/` first;
  - do not hand-edit `.codex/skills/`;
  - use `python scripts/build-skills.py --check` as the drift proof surface.
- Existing tracked plan artifacts already show the lifecycle surfaces this change must keep coherent:
  - `docs/plans/0000-00-00-example-plan.md`
  - `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
  - `docs/plans/2026-04-20-constitution-governance-migration.md`
- `docs/explain/2026-04-20-constitution-governance-migration.md` identifies this initiative as a follow-up and calls out stale plan wording as a visible concern. That makes plan-surface audit part of the real migration scope rather than optional cleanup.
- There is no `docs/project-map.md`. The existing architecture doc and ADR provide enough repository-orientation context for this workflow-only change.

## Non-goals

- Introduce CI or script automation that infers lifecycle state from git or PR status.
- Redesign the overall section structure of every historical plan file.
- Replace `docs/plan.md` with a new planning system.
- Turn `learn` into mandatory lifecycle bookkeeping.
- Rewrite archival proposals, explain artifacts, or review notes unless they are still acting as active contributor guidance.
- Broaden this work into unrelated workflow or governance cleanup beyond plan lifecycle ownership.

## Pre-implementation prerequisites

- Before `test-spec` or `implement`, normalize tracked approval metadata so downstream stages can cite repository artifacts instead of chat history.
- Satisfy that prerequisite in one of these two ways:
  - update the status/readiness lines in `docs/proposals/2026-04-20-plan-index-lifecycle-ownership.md` and `specs/plan-index-lifecycle-ownership.md` so they reflect the approved review state; or
  - add a tracked review artifact that records proposal/spec approval and can be cited by `test-spec`, `implement`, `verify`, and `pr`.
- Do not start implementation while proposal/spec approval still exists only as chat context.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`, `R2` | `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `docs/plan.md` wording that keeps plan-index lifecycle bookkeeping scoped to planned initiatives and clearly separate from plan bodies |
| `R3`, `R3a`, `R3b`, `R5` | `docs/plan.md`, `docs/plans/0000-00-00-example-plan.md`, and any concrete plan bodies corrected during migration so lifecycle state and readiness wording stay synchronized |
| `R4`, `R6`, `R6a`, `R6b`, `R7`, `R7a` | `specs/rigorloop-workflow.md`, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/learn/SKILL.md`, and `skills/workflow/SKILL.md` |
| `R8`, `R8a` | `docs/workflows.md`, `AGENTS.md`, canonical `skills/`, generated `.codex/skills/`, and the canonical plan example under `docs/plans/` |
| `R9` | `docs/plan.md` plus any already-known stale lifecycle state in tracked plan bodies that the migration can truthfully correct at adoption time |

## Milestones

### M1. Encode lifecycle ownership in workflow and governance docs

- Goal:
  - Make the ownership model explicit in the normative workflow contract and the top-level contributor guidance before touching plan bodies or skill-stage instructions.
- Requirements:
  - `R1`, `R2`, `R4`, `R6`, `R6a`, `R6b`, `R7`, `R7a`, `R8`, `R8a`
- Files/components likely touched:
  - `CONSTITUTION.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
- Dependencies:
  - reviewed spec: `specs/plan-index-lifecycle-ownership.md`
  - no new architecture work expected
  - test spec should exist before implementation starts, even though this plan is being created first
- Tests to add/update:
  - create `specs/plan-index-lifecycle-ownership.test.md` before implementation with coverage for:
    - lifecycle ownership visibility in workflow docs;
    - `docs/plan.md` being an index rather than a plan body;
    - `verify` blocking PR readiness when lifecycle state is stale;
    - `learn` remaining non-authoritative for lifecycle closeout.
- Implementation steps:
  - review `CONSTITUTION.md` against the approved lifecycle-ownership rule and either update its workflow/governance guidance or record explicit evidence that its existing guidance already covers the change without drift
  - update `specs/rigorloop-workflow.md` so the stage contract names lifecycle-closeout ownership and the `verify` stale-state gate explicitly
  - update `docs/workflows.md` so contributors can discover index-versus-body ownership without reading the spec first
  - update `AGENTS.md` where planning, verification, or change-management wording would otherwise conflict with the new ownership split
- Validation commands:
  - `rg -n "docs/plan\\.md|plan body|lifecycle closeout|Blocked|Done|Superseded|stale lifecycle|learn|verify" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
  - manual review: `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` remain mutually consistent with the updated workflow spec
- Expected observable result:
  - contributors can identify who owns plan creation, ongoing plan-body updates, final lifecycle closeout, and stale-state verification from the repository’s core docs
- Commit message: `M1: define plan lifecycle ownership in workflow docs`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - wording may drift between the normative spec and the summary docs
  - `AGENTS.md` could accidentally over-specify rules that belong in the workflow spec
- Rollback/recovery:
  - revert the doc/spec edits as one unit if the wording proves confusing
  - keep any truthfully corrected guidance direction that the repository already depends on

### M2. Align lifecycle-stage skills and regenerate compatibility output

- Goal:
  - Make the canonical stage skills reflect the same ownership split as the updated docs, then regenerate `.codex/skills/` so the runtime guidance stays synchronized.
- Requirements:
  - `R4`, `R7`, `R7a`, `R8`, `R8a`
- Files/components likely touched:
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
  - `skills/workflow/SKILL.md`
  - generated `.codex/skills/`
- Dependencies:
  - M1 guidance wording should be stable first
  - existing generator and drift check:
    - `python scripts/build-skills.py`
    - `python scripts/build-skills.py --check`
- Tests to add/update:
  - the future test spec should include manual guidance checks for the updated stage skills and a generated-output drift proof step
  - no new executable test harness is expected for this milestone
- Implementation steps:
  - update `skills/plan/SKILL.md` so it clearly owns plan creation and startup indexing, not all later lifecycle transitions
  - update `skills/implement/SKILL.md` so it keeps progress, decisions, discoveries, and validation notes current during execution
  - update `skills/verify/SKILL.md` so stale lifecycle state becomes an explicit readiness blocker when relevant
  - update `skills/pr/SKILL.md`, `skills/learn/SKILL.md`, and `skills/workflow/SKILL.md` where they describe closeout, PR readiness, or retrospective ownership
  - regenerate `.codex/skills/` from canonical `skills/`
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n "docs/plan\\.md|plan body|lifecycle|closeout|stale|learn|verify" skills .codex/skills`
  - `git diff --check -- skills .codex/skills`
- Expected observable result:
  - canonical and generated skill guidance no longer imply that `plan` or `learn` owns final lifecycle bookkeeping, and `verify` explicitly challenges stale state before PR readiness
- Commit message: `M2: align skills with plan lifecycle ownership`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - generated skill output may drift if canonical edits are incomplete
  - stage descriptions may partially overlap and create contradictory ownership wording
- Rollback/recovery:
  - revert canonical skill edits, regenerate `.codex/skills/`, and rerun drift validation

### M3. Migrate plan surfaces and correct known stale lifecycle state

- Goal:
  - Make the canonical plan example and currently relevant tracked plan/index surfaces obey the clarified lifecycle model, including any already-known stale state that should be corrected as part of adoption.
- Requirements:
  - `R2`, `R3`, `R3a`, `R3b`, `R5`, `R6`, `R6a`, `R6b`, `R7`, `R7a`, `R8a`, `R9`
- Files/components likely touched:
  - `docs/plan.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `docs/plans/2026-04-19-rigorloop-first-release-implementation.md` only if lifecycle wording still conflicts with its indexed `Done` state
  - `docs/plans/2026-04-20-constitution-governance-migration.md` if active-state wording or readiness text is already known to be wrong
  - `docs/plans/2026-04-20-plan-index-lifecycle-ownership.md` for implementation progress and any planning decisions discovered during the work
- Dependencies:
  - M1 and M2 must establish the shared wording first
  - test spec should define the manual comparison cases before implementation starts
- Tests to add/update:
  - `specs/plan-index-lifecycle-ownership.test.md` should cover:
    - one-section-per-plan indexing in `docs/plan.md`;
    - synchronized active versus done/blocked/superseded state between index and body;
    - merge-dependent done exception handling;
    - migration-time correction of already-known stale state.
- Implementation steps:
  - update `docs/plans/0000-00-00-example-plan.md` so the example plan visibly models lifecycle-aware status, closeout expectations, and non-stale outcome/readiness wording
  - adjust `docs/plan.md` only as needed to keep it an unambiguous lifecycle index
  - audit current concrete plan bodies that are referenced by `docs/plan.md` and related explain artifacts for already-known stale lifecycle state or readiness wording
  - correct only the state and wording that the repository can truthfully classify today; do not guess future closeout state for still-active work
  - record any merge-dependent `Done` exception explicitly where it is actually needed instead of implying it by silence
- Validation commands:
  - `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`
  - `for slug in 2026-04-19-rigorloop-first-release-implementation 2026-04-20-constitution-governance-migration 2026-04-20-plan-index-lifecycle-ownership; do test "$(rg -c "${slug}\\.md" docs/plan.md)" -eq 1; done`
  - `rg -n "Status|Outcome and retrospective|Readiness|ready for PR|ready for code-review|complete and now belongs|blocked|superseded" docs/plans/0000-00-00-example-plan.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md docs/plans/2026-04-20-constitution-governance-migration.md docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
  - `git diff --check -- docs/plan.md docs/plans`
  - `bash scripts/ci.sh`
  - manual review: compare `docs/plan.md` against each touched plan body, confirm lifecycle state matches reality, and confirm each touched indexed plan slug appears exactly once under one lifecycle section
- Expected observable result:
  - the plan index and touched plan bodies agree about lifecycle state, and the canonical plan example teaches contributors how to keep them synchronized
- Commit message: `M3: synchronize plan index and plan bodies`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - the change could accidentally rewrite historical meaning rather than correcting only clearly known stale state
  - active plans may be over-closed if readiness wording is interpreted too aggressively
- Rollback/recovery:
  - revert wording and template changes if needed
  - preserve any lifecycle-state correction that is demonstrably true even if closeout prose needs refinement later

## Validation plan

- Before implementation, create `specs/plan-index-lifecycle-ownership.test.md` so each `MUST` in the spec maps to named manual or structural proof.
- Use milestone-scoped validation first:
  - M1: focused path scans and diff checks for workflow/governance docs
  - M2: `python scripts/validate-skills.py` plus generated-output drift check
  - M3: focused plan/index scans, manual lifecycle comparison, and `bash scripts/ci.sh`
- Use manual review as a first-class proof surface for this initiative:
  - compare `docs/plan.md` entries against the corresponding plan bodies
  - confirm updated guidance makes the ownership split discoverable without chat history
  - confirm any corrected lifecycle state reflects known reality, not guesswork
- Before `verify` and `pr`, rerun the repo-owned wrapper:
  - `bash scripts/ci.sh`
- Record the exact commands and lifecycle-state evidence in this plan’s `Validation notes` during implementation.

## Risks and recovery

- Risk: the implementation changes workflow wording but misses one stage skill, leaving contradictory ownership guidance.
  - Recovery: use M2 path scans across canonical and generated skills before closing the milestone.
- Risk: the migration corrects a plan’s lifecycle state too early and turns still-active work into historical state.
  - Recovery: only correct state that is already known from tracked evidence; leave genuinely active work active.
- Risk: the plan template change becomes a hidden redesign of plan structure rather than a targeted lifecycle clarification.
  - Recovery: keep edits focused on lifecycle status, closeout, and readiness wording only.

## Dependencies

- Internal:
  - `docs/proposals/2026-04-20-plan-index-lifecycle-ownership.md`
  - `specs/plan-index-lifecycle-ownership.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - canonical `skills/`
  - generated `.codex/skills/`
  - existing plan index and tracked plan files under `docs/plans/`
  - `python scripts/build-skills.py`
  - `bash scripts/ci.sh`
- External:
  - none

## Progress

- [x] M1. Encode lifecycle ownership in workflow and governance docs
- [x] M2. Align lifecycle-stage skills and regenerate compatibility output
- [x] M3. Migrate plan surfaces and correct known stale lifecycle state
- 2026-04-20: plan created
- 2026-04-20: tracked approval metadata normalized in the proposal/spec and test spec created at `specs/plan-index-lifecycle-ownership.test.md`.
- 2026-04-20: M1 implemented. Updated `CONSTITUTION.md`, `specs/rigorloop-workflow.md`, `docs/workflows.md`, and `AGENTS.md` so planned-initiative lifecycle ownership, closeout timing, and stale-state verification are explicit.
- 2026-04-20: post-M1 code review found stale pre-implementation readiness text in this plan. Updated the stage metadata so the active plan body matches the completed `plan-review`, `test-spec`, and M1 work.
- 2026-04-20: M2 implemented. Updated canonical `plan`, `implement`, `verify`, `pr`, `learn`, and `workflow` skills with explicit lifecycle ownership guidance and regenerated matching `.codex/skills/` output.
- 2026-04-20: M3 implemented. Updated `docs/plan.md`, the canonical plan example, and the already-indexed first-release and constitution-migration plans so lifecycle state, closeout wording, and `Done` classification now match known reality.

## Decision log

- 2026-04-20: Treat the reviewed spec as approved for planning despite its tracked `draft` status line. Rationale: the user explicitly directed the workflow to continue after spec review.
- 2026-04-20: Use the existing first-release architecture and ADR only as background constraints. Rationale: this initiative changes workflow ownership and plan-state handling, not repository layout.
- 2026-04-20: Split implementation into three milestones. Rationale: core docs, skill guidance, and plan-surface migration are distinct reviewable slices with different validation surfaces.
- 2026-04-20: Require tracked approval metadata before `test-spec` or `implement`. Rationale: downstream stages should cite repository artifacts rather than depend on chat-only approval state.
- 2026-04-20: Encode the lifecycle rule twice: as concise governance in `CONSTITUTION.md` and as stage-specific contract detail in `specs/rigorloop-workflow.md`. Rationale: the constitution must reflect affected workflow guidance, while the workflow spec still needs the normative owner and timing detail.
- 2026-04-20: Keep the active plan's stage metadata synchronized with actual workflow progress after each milestone and review pass. Rationale: the clarified lifecycle rule requires plan bodies to remain current enough for later stages to trust them.
- 2026-04-20: Keep `plan` focused on startup and replanning ownership, and move ongoing lifecycle-closeout timing into `implement`, `verify`, `pr`, `learn`, and `workflow`. Rationale: the ownership split should stay discoverable without turning the planning skill into the authority for all later lifecycle transitions.
- 2026-04-20: Reclassify the constitution-governance migration plan as `Done` during M3. Rationale: its tracked outcome, verification, and explain artifact already showed the migration work was complete, so keeping it under `Active` was stale rather than a merge-dependent exception.
- 2026-04-20: Normalize historical plan wording from `complete` to `done` where the plan index already uses `Done`. Rationale: the migration should teach one lifecycle vocabulary across `docs/plan.md`, the example plan, and the touched historical plan bodies.

## Surprises and discoveries

- 2026-04-20: no `docs/project-map.md` exists, but the repository architecture doc and ADR already provide enough planning context for this initiative.
- 2026-04-20: lifecycle ownership is currently expressed across both top-level docs and stage skills, so a docs-only fix would leave runtime guidance inconsistent.
- 2026-04-20: the constitution migration explain artifact already calls out plan-lifecycle follow-up risk, which makes stale plan-state review part of this initiative’s adoption scope.
- 2026-04-20: `docs/plan.md` was already described as an index, but the repo’s core workflow and governance docs still lacked explicit ownership for ongoing plan-body updates, lifecycle closeout, and stale-state verification.
- 2026-04-20: the canonical `plan` skill still used `complete` and omitted `Blocked`, so lifecycle vocabulary drift existed inside skill guidance in addition to the missing ownership language.
- 2026-04-20: the example plan template still modeled a `proposed` plan and lacked explicit outcome/readiness guidance, so it could not teach contributors how to avoid stale lifecycle wording.

## Validation notes

- 2026-04-20 M1:
  - pre-change proof:
    - `rg -n "docs/plan\\.md|plan body|lifecycle closeout|stale lifecycle|Blocked|Done|Superseded|learn|verify" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
    - result: the repo already described `docs/plan.md` as an index, but M1 surfaces did not yet assign lifecycle-closeout ownership or stale-state verification consistently.
  - no-test rationale:
    - M1 is a workflow and governance documentation milestone. The approved proof surface comes from manual and structural checks in `specs/plan-index-lifecycle-ownership.test.md` (`T1`, `T3`, `T4`, `T5`) rather than new executable tests.
  - milestone validation:
    - `rg -n "docs/plan\\.md|plan body|lifecycle closeout|Blocked|Done|Superseded|stale lifecycle|learn|verify" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
    - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
  - manual review:
    - `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` now align with `specs/rigorloop-workflow.md`
    - `specs/rigorloop-workflow.md` now makes planned-initiative lifecycle ownership, timing, and stale-state blocking explicit through `R8f` to `R8ja`
  - result: pass
- 2026-04-20 M2:
  - pre-change proof:
    - `python scripts/validate-skills.py`
    - `python scripts/build-skills.py --check`
    - `rg -n "docs/plan\\.md|plan body|lifecycle closeout|lifecycle state|stale lifecycle|Blocked|Superseded|merge-dependent|post-merge|plan body|non-authoritative|authoritative|readiness blocker" skills/plan/SKILL.md skills/implement/SKILL.md skills/verify/SKILL.md skills/pr/SKILL.md skills/learn/SKILL.md skills/workflow/SKILL.md .codex/skills/plan/SKILL.md .codex/skills/implement/SKILL.md .codex/skills/verify/SKILL.md .codex/skills/pr/SKILL.md .codex/skills/learn/SKILL.md .codex/skills/workflow/SKILL.md`
    - result: skill structure was valid and generated output was in sync, but the targeted stage skills still lacked the approved lifecycle-ownership wording.
  - no-test rationale:
    - M2 updates contributor/runtime guidance rather than application runtime logic. The approved proof surface comes from manual and structural checks in `specs/plan-index-lifecycle-ownership.test.md` (`T2`, `T3`, `T4`, `T5`, `T6`) plus the existing skill validator and drift check.
  - milestone validation:
    - `python scripts/build-skills.py`
    - `python scripts/validate-skills.py`
    - `python scripts/build-skills.py --check`
    - `rg -n "docs/plan\\.md|plan body|lifecycle|closeout|stale|learn|verify|merge-dependent|post-merge|Blocked|Superseded|authoritative" skills .codex/skills`
    - `git diff --check -- skills .codex/skills`
  - manual review:
    - canonical and generated `plan`, `implement`, `verify`, `pr`, `learn`, and `workflow` skills now agree that `docs/plan.md` is the lifecycle index and plan bodies carry initiative detail
    - `implement` now owns ongoing plan-body progress/decision/discovery/validation-note updates during execution
    - `verify` now treats stale lifecycle state as a readiness blocker and requires explicit lifecycle-evidence review when relevant
    - `pr` and `workflow` now describe done-before-PR as the default, the merge-dependent post-merge exception, and immediate `Blocked`/`Superseded` handling
    - `learn` now remains explicitly retrospective and non-authoritative for lifecycle bookkeeping
  - result: pass
- 2026-04-20 M3:
  - pre-change proof:
    - `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`
    - `for slug in 2026-04-19-rigorloop-first-release-implementation 2026-04-20-constitution-governance-migration 2026-04-20-plan-index-lifecycle-ownership; do test "$(rg -c "${slug}\\.md" docs/plan.md)" -eq 1; done`
    - `rg -n "Status|Outcome and retrospective|Readiness|ready for PR|ready for code-review|complete and now belongs|blocked|superseded" docs/plans/0000-00-00-example-plan.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md docs/plans/2026-04-20-constitution-governance-migration.md docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
    - result: `docs/plan.md` still listed the constitution-governance migration under `Active`, the example plan still modeled `Status: proposed`, and the first-release plan still used `complete` wording while the index used `Done`.
  - no-test rationale:
    - M3 changes lifecycle bookkeeping and plan-template guidance, not application runtime behavior. The approved proof surface comes from manual and structural checks in `specs/plan-index-lifecycle-ownership.test.md` (`T4`, `T7`, `T8`, `T9`, `T10`) plus the existing repo wrapper in `bash scripts/ci.sh`.
  - milestone validation:
    - `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`
    - `for slug in 2026-04-19-rigorloop-first-release-implementation 2026-04-20-constitution-governance-migration 2026-04-20-plan-index-lifecycle-ownership; do test "$(rg -c "${slug}\\.md" docs/plan.md)" -eq 1; done`
    - `rg -n "Status|Outcome and retrospective|Readiness|ready for PR|ready for code-review|complete and now belongs|blocked|superseded" docs/plans/0000-00-00-example-plan.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md docs/plans/2026-04-20-constitution-governance-migration.md docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
    - `git diff --check -- docs/plan.md docs/plans`
    - `bash scripts/ci.sh`
  - manual review:
    - `docs/plan.md` now lists the touched plan slugs exactly once under one lifecycle section
    - the first-release and constitution-governance migration plan bodies now match their `Done` index placement without stale active-stage readiness wording
    - the example plan now teaches contributors to keep `docs/plan.md` and the plan body synchronized when lifecycle state changes
  - result: pass

## Outcome and retrospective

- M1-M3 are implemented.
- The workflow docs, skill guidance, plan index, example plan, and already-known stale plan bodies now follow the same lifecycle-closeout model.
- This initiative remains active only because downstream review stages are still pending; lifecycle closeout for this plan should happen after those stages determine the real final state.

## Readiness

This plan remains active.

Tracked approval metadata is normalized, `test-spec` is complete, and M1-M3 are implemented.

Next expected work is `code-review` for the completed implementation. If review passes, proceed to `verify`, then `explain-change`, then `pr`. Do not move this plan to `Done` until those downstream stages confirm the initiative is actually closed or an explicit merge-dependent exception applies.
