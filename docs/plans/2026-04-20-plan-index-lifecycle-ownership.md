# Plan index lifecycle ownership plan

- Status: done
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
- 2026-04-20: code-review approved the completed M1-M3 implementation with no blocking findings.
- 2026-04-20: verify reran the feature proof surface, confirmed the implementation is complete, and closed this plan to `Done` before PR because the outcome is already known on-branch.
- 2026-04-20: explain-change published the durable rationale artifact at `docs/explain/2026-04-20-plan-index-lifecycle-ownership.md`.
- 2026-04-20: PR #3 opened against `main`.
- 2026-04-20: learn captured the retrospective lessons in this completed plan.
- 2026-04-20: PR #3 merged into `main` as `8040a54`.

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
- 2026-04-20: Close this initiative to `Done` during verify before `pr`. Rationale: the implementation, code review, and verification outcome are already known on-branch, so deferring `Done` until after PR or merge would violate the lifecycle-closeout rule this feature just introduced.
- 2026-04-20: Open PR #3 against `main` even though this branch tracks `origin/feat/rigorloop-first-release`. Rationale: `main` is the repository default branch and the branch-specific cherry set against `origin/main` contains only this feature's five commits.

## Surprises and discoveries

- 2026-04-20: no `docs/project-map.md` exists, but the repository architecture doc and ADR already provide enough planning context for this initiative.
- 2026-04-20: lifecycle ownership is currently expressed across both top-level docs and stage skills, so a docs-only fix would leave runtime guidance inconsistent.
- 2026-04-20: the constitution migration explain artifact already calls out plan-lifecycle follow-up risk, which makes stale plan-state review part of this initiative’s adoption scope.
- 2026-04-20: `docs/plan.md` was already described as an index, but the repo’s core workflow and governance docs still lacked explicit ownership for ongoing plan-body updates, lifecycle closeout, and stale-state verification.
- 2026-04-20: the canonical `plan` skill still used `complete` and omitted `Blocked`, so lifecycle vocabulary drift existed inside skill guidance in addition to the missing ownership language.
- 2026-04-20: the example plan template still modeled a `proposed` plan and lacked explicit outcome/readiness guidance, so it could not teach contributors how to avoid stale lifecycle wording.
- 2026-04-20: the branch tracked `origin/feat/rigorloop-first-release`, but the actual pull request target still needed to be `main`; review-scoping base and PR base can differ once earlier feature work is already merged.

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
- 2026-04-20 verify:
  - pre-closeout proof:
    - `docs/plan.md` still listed this initiative under `## Active`
    - this plan body still used `Status: active`
    - this plan body's readiness still named `code-review` as the next expected work even though code review had already passed
  - validation:
    - `rg -n "docs/plan\\.md|plan body|lifecycle closeout|Blocked|Done|Superseded|stale lifecycle|learn|verify" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
    - `python scripts/validate-skills.py`
    - `python scripts/build-skills.py --check`
    - `rg -n "docs/plan\\.md|plan body|lifecycle|closeout|stale|learn|verify|merge-dependent|post-merge|Blocked|Superseded|authoritative" skills .codex/skills`
    - `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`
    - `for slug in 2026-04-19-rigorloop-first-release-implementation 2026-04-20-constitution-governance-migration 2026-04-20-plan-index-lifecycle-ownership; do test "$(rg -c "${slug}\\.md" docs/plan.md)" -eq 1; done`
    - `rg -n "Status|Outcome and retrospective|Readiness|ready for PR|ready for code-review|complete and now belongs|blocked|superseded" docs/plans/0000-00-00-example-plan.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md docs/plans/2026-04-20-constitution-governance-migration.md docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
    - `git diff --check 155be39..HEAD`
    - `bash scripts/ci.sh`
  - manual review:
    - reviewed `docs/plan.md` `Done` section after closeout
    - reviewed this plan body's `Status`, `Outcome and retrospective`, and `Readiness` surfaces after closeout
    - confirmed the full feature range `155be39..HEAD` changes only the planned workflow, skill, spec, and plan surfaces for this initiative
    - confirmed hosted CI is defined in `.github/workflows/ci.yml` as a thin wrapper over `bash scripts/ci.sh`, but no hosted run was observed from this environment
  - result: pass with hosted CI still unobserved

## Outcome and retrospective

- M1-M3 are implemented, reviewed, and verified.
- The workflow docs, skill guidance, plan index, example plan, and already-known stale plan bodies now follow the same lifecycle-closeout model.
- This initiative is done on-branch and now belongs in `docs/plan.md` under `Done`.
- What changed: the feature added a full proposal/spec/test-spec/plan/explain trail, updated governing workflow docs and stage skills, normalized the canonical plan template and touched historical plan bodies, and closed the initiative to `Done` before PR.
- What went well: milestone slicing kept the review surface small, and the manual plus structural proof surface was strong enough to catch real lifecycle-state drift without inventing low-value executable tests.
- What was harder than expected: the plan body drifted after `plan-review`, after M1 code review, and again before PR, so keeping stage metadata current required explicit follow-through after each review pass rather than only at milestone commit time.
- Spec accuracy: the feature spec correctly captured lifecycle ownership, stale-state blocking, and the default done-before-PR rule; the main readiness gap was approval-state traceability, which the plan had to normalize before `test-spec` and implementation.
- Test effectiveness: the test spec's document scans, plan/index comparisons, and repo-owned validation commands were the right checks for this change; `code-review` and `verify` both found stale plan metadata that would have been easy to miss in a prose-only review.
- Architecture accuracy: no new architecture artifact was needed; the existing repository architecture and ADR were enough to preserve the canonical `skills/` versus generated `.codex/skills/` boundary and the single canonical plan template.
- Process issues: chat-only approval state created avoidable ambiguity until the proposal and spec status markers were normalized, and shell-expanded commit bodies proved less reliable than the plan and explain artifact as a record of exact validation commands.
- Durable updates made: the repository now documents lifecycle ownership in governance docs, stage skills, the canonical plan template, and the touched plan/index surfaces; this retrospective also records that future agents should treat active-plan metadata as live state after each review/verify pass and should confirm the actual PR base instead of assuming the branch upstream is the merge target.
- Follow-up actions: observe hosted CI on PR #3; if PR-base confusion recurs, update `skills/pr/SKILL.md` and `.codex/skills/pr/SKILL.md` to make the base-branch check explicit; continue using plan and explain artifacts as the authoritative source for exact validation commands when commit-message quoting could distort them.

## Readiness

This plan is done.

Tracked approval metadata is normalized, `test-spec` is complete, and the full M1-M3 implementation has passed code review, verify, and learn.

PR #3 merged into `main` as `8040a54`.

No further workflow stage is expected for this initiative unless PR review or hosted CI reopens work.

This plan remains as a historical execution record rather than an active initiative.

## Historical closeout rationale

Retained from `docs/explain/2026-04-20-plan-index-lifecycle-ownership.md` when the legacy explanation directory was retired during the 2026-09-07 repository cleanup. The quoted text preserves the original account, commands and paths; it is historical evidence, not current plan state or a fresh verification result. New work uses the owning change’s contract-selected Verify report.

> # Plan index lifecycle ownership rationale
>
> ## Summary
>
> This explanation covers the plan-index lifecycle ownership feature range `155be39..903394b`.
>
> The change adds a full proposal/spec/test-spec/plan trail for lifecycle-closeout ownership, updates the governing workflow docs and stage skills so contributors can discover the ownership split without chat history, normalizes the plan template and already-known stale plan surfaces, and closes the feature itself to `Done` during verify once the on-branch outcome was known.
>
> This feature is mostly documentation, workflow-contract, and repository-state work rather than new runtime logic. The diff is therefore large in artifact count but narrow in behavioral scope: it changes how contributors record and review lifecycle state for planned initiatives, not how the product runs.
>
> ## Problem
>
> The repository had already demonstrated the failure mode this feature addresses:
>
> - a completed initiative remained listed under `## Active` in `docs/plan.md`;
> - later work had to reason around stale active guidance;
> - ownership of lifecycle closeout was too implicit across `plan`, `implement`, `verify`, `pr`, and `learn`;
> - the plan template and touched historical plan bodies did not teach or model the intended lifecycle vocabulary consistently.
>
> If left unchanged, contributors could keep claiming PR readiness while `docs/plan.md` and plan bodies disagreed about whether an initiative was still active.
>
> ## Decision trail
>
> | Artifact | Decision carried into the change | How it shaped the diff |
> | --- | --- | --- |
> | [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md) | Reject implicit ownership, reject `learn` as lifecycle authority, and reject early automation; make final closeout own lifecycle state while `verify` enforces drift detection. | The diff changes workflow docs, skills, and plan surfaces instead of adding automation or retrospective bookkeeping rules. |
> | [`plan-index-lifecycle-ownership.md`](../../specs/plan-index-lifecycle-ownership.md) | Define the contract in `R1`-`R9`: `docs/plan.md` is an index, plan bodies stay synchronized with it, `implement` owns ongoing plan-body updates, `verify` blocks stale lifecycle state, and adoption should correct already-known stale state. | The diff updates governance/workflow docs, stage skills, plan template guidance, and touched plan/index state to reflect those rules. |
> | [`plan-index-lifecycle-ownership.test.md`](../../specs/plan-index-lifecycle-ownership.test.md) | Use manual and structural proof surfaces (`T1`-`T10`) rather than synthetic runtime tests. | The implementation records path scans, lifecycle-state scans, manual plan/index comparisons, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, and `bash scripts/ci.sh` instead of adding low-value executable tests for prose. |
> | [`2026-04-19-rigorloop-first-release-repository-architecture.md`](../architecture/2026-04-19-rigorloop-first-release-repository-architecture.md) and [`ADR-20260419-repository-source-layout.md`](../adr/ADR-20260419-repository-source-layout.md) | Keep `skills/` canonical, `.codex/skills/` generated, and `docs/plans/0000-00-00-example-plan.md` as the canonical plan template. | The feature edits canonical `skills/` first, regenerates `.codex/skills/`, and teaches lifecycle-aware plan behavior in the canonical plan example rather than adding a second plan surface. |
> | [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md) | Implement in three milestones: core workflow docs, stage skills, and plan-surface migration. Close the feature to `Done` before PR when the outcome is already known. | The branch history splits into M1 (`99907da`), M2 (`6d507c1`), M3 (`0a24fe3`), and a verify-stage closeout commit (`903394b`). |
> | Code-review and verify findings | Keep the active plan body current during the feature, and do not defer a known `Done` transition until after PR. | Review fixups updated stale plan metadata after M1, and verify performed the final lifecycle closeout for this initiative itself before `pr`. |
>
> ## Milestone map
>
> | Milestone or stage | Commits | Outcome |
> | --- | --- | --- |
> | M1 | `99907da` | Made lifecycle-closeout ownership, stale-state blocking, and index-versus-body semantics explicit in `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `specs/rigorloop-workflow.md`. |
> | M2 | `6d507c1` | Aligned canonical `plan`, `implement`, `verify`, `pr`, `learn`, and `workflow` skills with the ownership split and regenerated `.codex/skills/`. |
> | M3 | `0a24fe3` | Normalized `docs/plan.md`, the canonical plan example, and already-known stale historical plan surfaces. |
> | Verify closeout | `903394b` | Closed the feature itself to `Done` after verify confirmed the on-branch outcome was already known and no merge-dependent exception applied. |
>
> ## Diff rationale by area
>
> | Area | Files | Change | Reason | Source artifact | Test or evidence |
> | --- | --- | --- | --- | --- | --- |
> | Governing workflow contract | [`CONSTITUTION.md`](../../CONSTITUTION.md), [`AGENTS.md`](../../AGENTS.md), [`docs/workflows.md`](../workflows.md), [`specs/rigorloop-workflow.md`](../../specs/rigorloop-workflow.md) | Added explicit lifecycle-index versus plan-body semantics, `implement` ownership during execution, verify-stage stale-state blocking, and the done-before-PR default with a merge-dependent exception. | Contributors needed one clear rule for when and how lifecycle state changes, not scattered implicit expectations. | Proposal decision; spec `R1`, `R2`, `R4`, `R6`-`R8a`; plan M1 | `T1`, `T3`, `T4`, `T5`; focused doc scans recorded in the plan and rerun during verify |
> | Durable feature artifacts | [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md), [`plan-index-lifecycle-ownership.md`](../../specs/plan-index-lifecycle-ownership.md), [`plan-index-lifecycle-ownership.test.md`](../../specs/plan-index-lifecycle-ownership.test.md), [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md) | Added the proposal/spec/test-spec/plan trail and kept the active plan’s progress, decisions, surprises, validation notes, and later stage-readiness state current. | The workflow change needed tracked decision memory and test mapping, not chat-only approval context. | Proposal, spec, test spec, plan; `CONSTITUTION.md` active-plan rule | Proposal-review, plan-review, code-review, and verify findings are all reflected in the plan history |
> | Stage skill alignment | [`skills/plan/SKILL.md`](../../skills/plan/SKILL.md), [`skills/implement/SKILL.md`](../../skills/implement/SKILL.md), [`skills/verify/SKILL.md`](../../skills/verify/SKILL.md), [`skills/pr/SKILL.md`](../../skills/pr/SKILL.md), [`skills/learn/SKILL.md`](../../skills/learn/SKILL.md), [`skills/workflow/SKILL.md`](../../skills/workflow/SKILL.md), matching [`.codex/skills/`](../../.codex/skills/) files | Clarified that `plan` owns startup and replanning, `implement` owns ongoing plan-body updates, `verify` blocks stale lifecycle state, `pr` expects lifecycle closeout when final state is known, and `learn` is retrospective only. | Updating docs without runtime guidance would have left the repository teaching contradictory behavior. | Spec `R4`, `R7`, `R7a`, `R8`, `R8a`; architecture/ADR generated-boundary rule; plan M2 | `T2`, `T3`, `T5`, `T6`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; lifecycle wording scan across canonical and generated skills |
> | Plan template and historical plan normalization | [`docs/plan.md`](../plan.md), [`0000-00-00-example-plan.md`](../plans/0000-00-00-example-plan.md), [`2026-04-19-rigorloop-first-release-implementation.md`](../plans/2026-04-19-rigorloop-first-release-implementation.md), [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Made the template model lifecycle-aware closeout, moved known-done historical plans under `Done`, and removed stale active-state wording from touched plan bodies. | Adoption needed to start from a truthful baseline and teach contributors how to keep the plan index and plan body synchronized. | Spec `R3`, `R3a`, `R3b`, `R5`, `R9`; plan M3 | `T7`, `T8`, `T9`; index-section scan, per-slug uniqueness loop, lifecycle wording scan, and manual review of touched plans |
> | Verify-stage closeout | [`docs/plan.md`](../plan.md), [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md) | Closed the feature itself to `Done` during verify, recorded the verify finding that the plan was still stale after code review, and updated readiness from `explain-change` plus `pr` to `pr` only after this explanation artifact was created. | Once implementation, code review, and verify all passed on-branch, deferring `Done` until after PR would have violated the very rule this feature introduced. | Spec `R5`, `R6`, `R6a`, `R7`, `R7a`; workflow spec `R8g`-`R8ja`; verify finding | Final verify reruns plus lifecycle-state manual review; closeout commit `903394b` |
>
> ## Tests added or changed
>
> No new executable application tests were added. That was intentional.
>
> The feature added the dedicated test spec [`specs/plan-index-lifecycle-ownership.test.md`](../../specs/plan-index-lifecycle-ownership.test.md), which maps the contract to the following proof surfaces:
>
> - `T1`: manual review of governing workflow docs;
> - `T2`: canonical/generated skill alignment plus structural validation and drift checks;
> - `T3` and `T4`: manual proof of done-transition timing and immediate blocked/superseded handling;
> - `T5`: verify-stage stale-state blocking and lifecycle-evidence expectations;
> - `T6`: confirmation that `learn` remains non-authoritative;
> - `T7` through `T9`: structural plan-index checks, lifecycle-wording scans, and manual plan-body comparisons;
> - `T10`: confirmation that the change does not imply new heavyweight automation.
>
> This test level is appropriate because the feature changes contributor-visible workflow and repository-state contracts, not executable runtime behavior. The best proof surfaces are tracked docs, plan/index state, canonical/generated skill trees, and repo-owned validation commands.
>
> ## Verification evidence
>
> Final verification was run against the committed branch state through `903394b`.
>
> Commands run:
>
> - `rg -n "docs/plan\.md|plan body|lifecycle closeout|Blocked|Done|Superseded|stale lifecycle|learn|verify" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
>   - pass
> - `python scripts/validate-skills.py`
>   - pass
>   - important output: validated 22 skill files
> - `python scripts/build-skills.py --check`
>   - pass
>   - important output: generated skills are in sync
> - `rg -n "docs/plan\.md|plan body|lifecycle|closeout|stale|learn|verify|merge-dependent|post-merge|Blocked|Superseded|authoritative" skills .codex/skills`
>   - pass
> - `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`
>   - pass
> - `for slug in 2026-04-19-rigorloop-first-release-implementation 2026-04-20-constitution-governance-migration 2026-04-20-plan-index-lifecycle-ownership; do test "$(rg -c "${slug}\\.md" docs/plan.md)" -eq 1; done`
>   - pass
> - `rg -n "Status|Outcome and retrospective|Readiness|ready for PR|ready for code-review|complete and now belongs|blocked|superseded" docs/plans/0000-00-00-example-plan.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md docs/plans/2026-04-20-constitution-governance-migration.md docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
>   - pass
> - `git diff --check 155be39..HEAD`
>   - pass
> - `bash scripts/ci.sh`
>   - pass
>   - important output: 9 skill-validator fixture tests passed and generated-skill drift check passed
>
> Manual checks:
>
> - reviewed the `Done` section in [`docs/plan.md`](../plan.md);
> - reviewed the active feature plan’s `Status`, `Outcome and retrospective`, and `Readiness` surfaces after closeout;
> - confirmed the full diff range changes only the planned workflow, skill, spec, and plan surfaces for this initiative.
>
> CI boundary:
>
> - local repo-owned validation passed through [`scripts/ci.sh`](../../scripts/ci.sh);
> - [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) remains the intended thin wrapper over that script;
> - hosted GitHub Actions CI was not observed from this environment, so this explanation does not claim remote CI passed.
>
> Evidence note:
>
> - the shell loop text in commit bodies `0a24fe3` and `903394b` was shell-expanded when the commits were created, so the authoritative command text is the validation record in [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md), not those commit bodies.
>
> ## Alternatives rejected
>
> These alternatives were explicitly rejected by the proposal or later stage findings:
>
> - Keep lifecycle-closeout ownership implicit.
>   - Rejected because the repository had already produced stale active-plan state in practice.
> - Make `learn` the owner of plan-index closeout.
>   - Rejected because `learn` is optional and retrospective, while lifecycle bookkeeping is operational state.
> - Add automation or CI enforcement before the ownership rule was stable.
>   - Rejected because the problem was a workflow-contract gap first, not a missing automation system.
> - Redesign the full internal structure of every historical plan file.
>   - Rejected because the feature only needed lifecycle-status, readiness, and closeout normalization on touched plans.
> - Defer this feature’s own `Done` transition until after PR or merge.
>   - Rejected during verify because the outcome was already known on-branch and no merge-dependent exception applied.
>
> ## Scope control
>
> This feature intentionally did not:
>
> - add lifecycle automation that infers plan state from git or PR status;
> - redesign the repository layout or create a new planning system;
> - turn `learn` into required bookkeeping;
> - rewrite archival proposals, explain artifacts, or review notes beyond the touched stale plan surfaces;
> - broaden into unrelated governance, CI, or release-process cleanup beyond lifecycle-closeout ownership.
>
> ## Risks and follow-ups
>
> The feature is verified and locally ready for PR, but a few follow-ups remain visible:
>
> - hosted CI has not been observed from this environment;
> - commit bodies `0a24fe3` and `903394b` contain shell-expanded loop text, so readers should rely on the plan’s validation notes for the exact command wording;
> - the working tree still contains two unrelated untracked proposal drafts outside this explained diff:
>   - [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md)
>   - [`2026-04-20-workflow-stage-handoff-clarity.md`](../proposals/2026-04-20-workflow-stage-handoff-clarity.md)
>
> ## PR-ready summary
>
> - Added a full proposal/spec/test-spec/plan trail for lifecycle-closeout ownership.
> - Made lifecycle ownership explicit in the governing workflow docs and in the canonical and generated stage skills.
> - Normalized the plan template and the already-known stale plan/index surfaces to a truthful `Done` baseline.
> - Closed the feature itself to `Done` during verify because the final outcome was already known before PR.
> - Verified the full feature with focused lifecycle scans, skill validation and drift checks, `git diff --check`, and `bash scripts/ci.sh`.
