# Single Source of Workflow State Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-09
- Last updated: 2026-05-09
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: standard
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow-governance Markdown, canonical skill text, generated local skill mirrors, public adapter package copies, tests, and change-local evidence. It does not add runtime services, persistence, network behavior, release packaging format, or deployed infrastructure.

## Purpose / Big Picture

Implement the approved single-source workflow-state contract.

The intended invariant is:

```text
Write current state once.
Link to it everywhere else.
Update it at every handoff.
```

The implementation makes the active plan `Current Handoff Summary` the live state owner for planned initiatives, prevents other artifacts from duplicating live next-stage claims, adds state-sync expectations at handoff boundaries, and keeps public skill wording portable.

## Source Artifacts

- Proposal: [Single Source of Workflow State](../proposals/2026-05-09-single-source-of-workflow-state.md), accepted after proposal-review R2.
- Spec: [Single Source of Workflow State](../../specs/single-source-of-workflow-state.md), approved after spec-review.
- Architecture: no runtime architecture impact expected. No-impact rationale: the change updates workflow contracts, skills, validation checks, generated skill/adapters, and durable artifacts; it does not alter service boundaries, storage, runtime data flow, deployment, security boundaries, or public API behavior.
- Test spec: [Single Source of Workflow State Test Spec](../../specs/single-source-of-workflow-state.test.md), active after test-spec authoring.
- Change metadata: `docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`.
- Review records: `docs/changes/2026-05-09-single-source-of-workflow-state/review-log.md` and `review-resolution.md` cover proposal-review R1/R2.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on project-map claims for runtime ownership, storage, service boundaries, or module topology. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, the accepted proposal, approved spec, existing skills, generator scripts, and validator patterns.

## Context and Orientation

- `specs/single-source-of-workflow-state.md` owns the behavior contract, especially R1-R36 and EB1-EB7.
- `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` are the contributor/governance surfaces likely to need wording alignment.
- `skills/workflow/SKILL.md`, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, and `skills/verify/SKILL.md` are the canonical skill sources most likely to carry current-state, milestone, review, final-closeout, or verification wording.
- `.codex/skills/` is generated local Codex runtime output. It must be refreshed with `python scripts/build-skills.py`, not hand-edited.
- `dist/adapters/` is generated public adapter output. It must be refreshed with `python scripts/build-adapters.py`, not hand-edited.
- Published skill text must remain portable. Repository-maintainer mechanics such as canonical source paths, generated mirrors, adapter paths, selector path constraints, drift checks, and shared-block mechanics belong in contributor/governance surfaces rather than shipped skills.

## Non-Goals

- Do not redesign the standard workflow stage order.
- Do not reintroduce a fast lane or small-change lane.
- Do not create a new lifecycle stage.
- Do not make every artifact carry a full workflow-state table.
- Do not make `change.yaml` a long-form state tracker.
- Do not make `review-resolution.md` own plan readiness.
- Do not make `verify` own PR readiness.
- Do not add broad semantic plan-state validation in the first implementation slice.
- Do not migrate historical plans that are not active, touched, generated, or relied on.
- Do not hand-edit `.codex/skills/` or `dist/adapters/`.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R14` | Workflow/spec/test guidance, plan skill, review-resolution/change metadata guidance, explain-change/verify/PR wording where affected. |
| `R15`-`R20` | Plan, implement, code-review, and workflow skill milestone-state guidance plus tests/static checks. |
| `R21`-`R28`, `EB1`-`EB7` | State-sync checklist, active-plan current handoff guidance, review-resolution/review-log/change metadata closeout expectations, validation coverage. |
| `R29`-`R31`, `EC1`, `EC5` | Workflow and plan guidance for final lifecycle closeout and merge not being a routine completion event. |
| `R32`-`R36`, `EC6` | Public skill portability checks, generated skill and adapter refresh, adapter drift and validation commands. |
| Acceptance criteria | Test spec and validator/static checks for current-state ownership, milestone state vocabulary, state-sync, portability, and generated-output currency. |

## Current Handoff Summary

- Current milestone: M2. Workflow and Governance Guidance
- Current milestone state: planned
- Last reviewed milestone: M1. Test Spec and Validator Coverage
- Review status: M1 code-review completed after `SSWS-CR1-F1` was resolved; no material findings remain open.
- Remaining in-scope implementation milestones: M2, M3, M4
- Next stage: implement M2
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M2-M4 are not started, generated output is not refreshed, final explain-change is not complete, verify has not run, and PR handoff is not prepared.

## Milestones

### M1. Test Spec and Validator Coverage

- Milestone state: closed
- Goal: Create the test spec and focused static proof for the single-source workflow-state contract.
- Requirements: `R1`-`R36`, `EB1`-`EB7`, acceptance criteria.
- Files/components likely touched:
  - `specs/single-source-of-workflow-state.test.md`
  - `scripts/test-skill-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - this plan
- Dependencies:
  - Plan-review approval.
- Tests to add/update:
  - Coverage that active plans use `Current Handoff Summary` as live state owner.
  - Coverage that `Readiness` points to the summary instead of duplicating next-stage claims.
  - Coverage for allowed milestone states and rejected legacy state labels.
  - Coverage for state-sync checklist expectations.
  - Coverage for public skill portability and versioned adapter validation expectations.
- Implementation steps:
  - Create `specs/single-source-of-workflow-state.test.md` mapping every `MUST` to tests or manual proof.
  - Add or update focused validator/static tests for skill wording and artifact lifecycle expectations.
  - Keep semantic plan-state validation out of scope unless a small static check already exists and is safe.
  - Update plan progress and change metadata.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `git diff --check -- specs/single-source-of-workflow-state.md specs/single-source-of-workflow-state.test.md scripts/test-skill-validator.py scripts/test-artifact-lifecycle-validator.py docs/plans/2026-05-09-single-source-of-workflow-state.md docs/plan.md docs/changes/2026-05-09-single-source-of-workflow-state`
- Expected observable result: The test spec and focused tests make the workflow-state contract implementable without guessing.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M1
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M2
- Commit message: `M1: specify workflow state proof`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Overbroad static checks could reject legitimate historical wording.
  - Missing requirement-test mapping could let skill behavior drift.
- Rollback/recovery:
  - Revert only the test-spec/static-check edits and keep the plan active with the blocker named.

### M2. Workflow and Governance Guidance

- Milestone state: planned
- Goal: Align contributor-facing workflow and governance wording with the single-source state contract.
- Requirements: `R1`-`R31`, `EB1`-`EB6`, `EC1`-`EC5`.
- Files/components likely touched:
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - this plan
- Dependencies:
  - M1 test-spec and focused proof.
- Tests to add/update:
  - Existing lifecycle and workflow tests where touched.
  - Static checks from M1 should cover the updated wording.
- Implementation steps:
  - Make `Current Handoff Summary` the named live state owner for planned initiatives.
  - Make `Readiness` guidance point to the summary for live state.
  - Add state-sync checklist expectations to workflow guidance.
  - Clarify that change metadata, review-resolution, explain-change, verify, and PR handoff own scoped evidence rather than competing next-stage state.
  - Update the example plan to model the new current handoff summary.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path AGENTS.md --path CONSTITUTION.md --path docs/plans/0000-00-00-example-plan.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/plan.md --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `git diff --check -- docs/workflows.md AGENTS.md CONSTITUTION.md docs/plans/0000-00-00-example-plan.md docs/plans/2026-05-09-single-source-of-workflow-state.md docs/plan.md docs/changes/2026-05-09-single-source-of-workflow-state`
- Expected observable result: Contributor-facing guidance identifies one live state owner and no longer encourages duplicated next-stage claims.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M2
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M3
- Commit message: `M2: align workflow state guidance`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Governance wording could become too detailed for `AGENTS.md`.
  - Example-plan updates could accidentally imply historical plans must migrate.
- Rollback/recovery:
  - Revert governance/workflow wording changes and keep the spec/test-spec active for replanning.

### M3. Canonical Skill Contract Updates

- Milestone state: planned
- Goal: Update canonical skills that create, review, or verify workflow-state claims.
- Requirements: `R1`-`R36`, `EB1`-`EB7`, `EC2`-`EC7`.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`, if final-rationale wording conflicts
  - `skills/pr/SKILL.md`, if PR handoff wording conflicts
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - this plan
- Dependencies:
  - M1 test-spec and M2 guidance alignment.
- Tests to add/update:
  - Skill validator checks for current handoff summary ownership, allowed milestone states, state-sync, no stale readiness duplication, verify/explain/pr claim boundaries, and portable public wording.
- Implementation steps:
  - Update `plan` guidance to create and maintain `Current Handoff Summary`.
  - Update `implement` guidance to set `review-requested` after targeted validation and avoid review/verify claims.
  - Update `code-review` guidance to transition clean or finding-bearing milestone states correctly.
  - Update `verify`, `explain-change`, and `pr` guidance so each owns only its proper readiness/evidence surface.
  - Keep repository-maintainer validation mechanics out of shipped skill text.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `git diff --check -- skills/workflow/SKILL.md skills/plan/SKILL.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/explain-change/SKILL.md skills/pr/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-single-source-of-workflow-state.md docs/changes/2026-05-09-single-source-of-workflow-state`
- Expected observable result: Canonical skills guide agents to write current state once, link elsewhere, and update it at handoffs.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M3
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M4
- Commit message: `M3: update workflow state skills`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Updating too many skills at once could broaden the diff.
  - Public skill text could expose repository-internal validation mechanics.
- Rollback/recovery:
  - Revert only the affected skill and validator edits, then split M3 into smaller skill groups if review asks for it.

### M4. Generated Output and Adapter Validation

- Milestone state: planned
- Goal: Refresh generated local skills and public adapters after canonical skill changes, and prove generated output is current.
- Requirements: `R32`-`R36`, `EC6`.
- Files/components likely touched:
  - `.codex/skills/`
  - `dist/adapters/`
  - `docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - this plan
- Dependencies:
  - M3 canonical skill changes.
- Tests to add/update:
  - Existing generated-output drift and adapter distribution tests should cover this milestone.
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run generated skill and adapter drift checks.
  - Run adapter validation and adapter distribution tests.
  - Record validation evidence in the plan and change metadata.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-05-09-single-source-of-workflow-state.md docs/changes/2026-05-09-single-source-of-workflow-state`
- Expected observable result: Generated `.codex/skills/` and `dist/adapters/` match canonical skill sources and adapter validation passes.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M4
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M5
- Commit message: `M4: refresh workflow state adapters`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Running generators after stale canonical skill text would propagate wrong guidance.
  - Adapter validation requires the versioned repository command.
- Rollback/recovery:
  - Re-run generators from the last accepted canonical skill sources or revert generated output together with the corresponding source edits.

### M5. Lifecycle Closeout

- Milestone state: planned
- Goal: Complete downstream gates after implementation milestones are closed.
- Requirements: repository workflow closeout, review, rationale, verification, and PR-readiness rules.
- Files/components likely touched:
  - `docs/changes/2026-05-09-single-source-of-workflow-state/review-log.md`
  - `docs/changes/2026-05-09-single-source-of-workflow-state/review-resolution.md`, when triggered
  - `docs/changes/2026-05-09-single-source-of-workflow-state/explain-change.md`
  - `docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - this plan
  - `docs/plan.md`
- Dependencies:
  - M1 through M4 are closed.
  - M1 through M4 have each completed their milestone code-review loop.
  - Material findings from M1 through M4 code-review are resolved or explicitly dispositioned.
  - Required review-resolution is closed.
- Tests to add/update:
  - No new implementation tests expected; this milestone validates final artifact coherence.
- Implementation steps:
  - Confirm M1-M4 are closed and each milestone review loop has passed.
  - Confirm required review-resolution is closed and no material finding remains open.
  - Create or update durable explain-change evidence.
  - Run final verify after explain-change exists.
  - Prepare PR handoff only after verify passes.
  - Update this plan and `docs/plan.md` together when final lifecycle state changes.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-single-source-of-workflow-state`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/plan.md`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `bash scripts/ci.sh --mode explicit --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/workflows.md --path AGENTS.md --path CONSTITUTION.md --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path scripts/test-skill-validator.py --path scripts/test-artifact-lifecycle-validator.py --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/plan.md --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `git diff --check -- .`
- Expected observable result: The change has durable rationale, final validation evidence, synchronized lifecycle state, and PR handoff readiness.
- Commit message: `M5: verify workflow state closeout`
- Milestone closeout:
  - all in-scope implementation milestones closed
  - review-resolution closed if triggered
  - explain-change complete
  - verify passed
  - PR handoff prepared
  - `docs/plan.md` and this plan synchronized when lifecycle state changes
- Risks:
  - Claiming plan Done before PR handoff evidence exists would violate lifecycle ownership.
  - Broad validation may expose unrelated baseline warnings; record them without hiding blocking failures.
- Rollback/recovery:
  - If final verify fails, keep the plan active, record the failing command, and return to the owning milestone.

## Validation Plan

- M1 proves the test spec and focused checks.
- M2 proves workflow/governance guidance alignment.
- M3 proves canonical skill behavior.
- M4 proves generated skill and adapter output currency.
- M5 proves final lifecycle coherence before PR handoff.

Use targeted validation first, then the final explicit CI scope in M5. Do not claim hosted CI unless it is actually observed.

## Risks and Recovery

- Risk: the new state owner model could over-constrain legitimate review summaries. Recovery: keep summaries allowed, but remove live next-stage authority from non-owner artifacts.
- Risk: static checks could become brittle. Recovery: limit first-slice checks to high-signal phrases and required positive wording.
- Risk: generated outputs drift from canonical skills. Recovery: regenerate through repository-owned scripts and rerun drift checks.
- Risk: plan lifecycle closeout repeats the stale-state problem this change is trying to solve. Recovery: use the plan's own `Current Handoff Summary` and M5 synchronized closeout checklist.

## Dependencies

- Spec-review approved the spec direction.
- Plan-review must approve this plan before test-spec work begins.
- Test-spec must be created before implementation.
- M1-M4 must each pass their implementation handoff and code-review loop before M5 final lifecycle closeout.
- Generated output refresh depends on canonical skill changes in M3.

## Progress

- [x] 2026-05-09: Proposal accepted after proposal-review R2.
- [x] 2026-05-09: Spec authored and approved by spec-review.
- [x] 2026-05-09: Plan created and indexed as active.
- [x] 2026-05-09: Plan-review approved the plan.
- [x] 2026-05-09: Test spec authored and activated.
- [x] 2026-05-09: M1 implementation started; scope limited to test spec plus focused validator/static proof.
- [x] 2026-05-09: M1 focused validator/static proof implemented and targeted validation passed.
- [x] 2026-05-09: Code-review M1 R1 found stale final-closeout reason wording; finding `SSWS-CR1-F1` was accepted and fixed before returning M1 to review-requested.
- [x] 2026-05-09: M1 code-review completed after `SSWS-CR1-F1` resolution; M1 closed and handoff moved to M2.
- [x] M1. Test Spec and Validator Coverage
- [ ] M2. Workflow and Governance Guidance
- [ ] M3. Canonical Skill Contract Updates
- [ ] M4. Generated Output and Adapter Validation
- [ ] M5. Lifecycle Closeout

## Decision Log

- 2026-05-09: Use a milestone plan because the change touches specs, workflow guidance, several canonical skills, generated outputs, validation scripts, and lifecycle artifacts.
- 2026-05-09: Treat architecture as no-impact for runtime architecture. The work changes workflow and artifact governance, not system boundaries or data flow.
- 2026-05-09: Keep broad semantic plan-state validation out of the first implementation slice; use focused static proof and review instead.
- 2026-05-09: Test-spec proof uses static, contract, generated-output, adapter, lifecycle, and manual review checks rather than runtime workflow simulation.
- 2026-05-09: M1 static proof pins the new test-spec/plan contract and readiness handoff behavior without adding broad semantic plan-state validation.
- 2026-05-09: Treat stale wording inside `Current Handoff Summary` as a material state-sync issue even when the milestone state field itself is correct.

## Surprises and Discoveries

- None yet.

## Validation Notes

- 2026-05-09 plan creation validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml --path docs/plan.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/proposals/2026-05-09-single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.md`
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-09-single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/plan.md --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- docs/proposals/2026-05-09-single-source-of-workflow-state.md specs/single-source-of-workflow-state.md docs/plans/2026-05-09-single-source-of-workflow-state.md docs/plan.md docs/changes/2026-05-09-single-source-of-workflow-state`
- Lifecycle validation emitted existing/intentional merge-language warnings in `docs/plan.md` line 18 and `specs/single-source-of-workflow-state.md` line 52; neither is blocking for plan creation.
- 2026-05-09 test-spec authoring validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md`
  - `python scripts/select-validation.py --mode explicit --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- specs/single-source-of-workflow-state.md specs/single-source-of-workflow-state.test.md docs/plans/2026-05-09-single-source-of-workflow-state.md docs/changes/2026-05-09-single-source-of-workflow-state`
- Lifecycle validation emitted intentional merge-language warnings in `specs/single-source-of-workflow-state.md` line 52 and `specs/single-source-of-workflow-state.test.md` line 208; the warning describes the contract that merge is not the routine plan-completion event.
- 2026-05-09 M1 implementation handoff validation passed:
  - `python scripts/select-validation.py --mode explicit --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path scripts/test-skill-validator.py --path scripts/test-artifact-lifecycle-validator.py --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/plan.md --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml --path docs/changes/2026-05-09-single-source-of-workflow-state/explain-change.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml --path docs/changes/2026-05-09-single-source-of-workflow-state/explain-change.md --path docs/plan.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `git diff --check -- specs/single-source-of-workflow-state.md specs/single-source-of-workflow-state.test.md scripts/test-skill-validator.py scripts/test-artifact-lifecycle-validator.py docs/plans/2026-05-09-single-source-of-workflow-state.md docs/plan.md docs/changes/2026-05-09-single-source-of-workflow-state`
- Lifecycle validation emitted expected merge-language warnings in `docs/plan.md` line 18, `specs/single-source-of-workflow-state.md` line 52, and `specs/single-source-of-workflow-state.test.md` line 208.
- 2026-05-09 M1 code-review R1 resolution validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-single-source-of-workflow-state`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-single-source-of-workflow-state/change.yaml --path docs/changes/2026-05-09-single-source-of-workflow-state/explain-change.md --path docs/plan.md --path docs/plans/2026-05-09-single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.md --path specs/single-source-of-workflow-state.test.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `git diff --check -- docs/changes/2026-05-09-single-source-of-workflow-state docs/plans/2026-05-09-single-source-of-workflow-state.md scripts/test-skill-validator.py scripts/test-artifact-lifecycle-validator.py specs/single-source-of-workflow-state.test.md docs/plan.md`

## Outcome and Retrospective

- Plan is active for M2. M1 is closed after code-review and accepted review-resolution for `SSWS-CR1-F1` and `SSWS-CR2-F1`.
- Done is not available until M1-M4 are closed, required review-resolution is closed, explain-change is complete, verify passes, PR handoff is prepared, and `docs/plan.md` plus this plan are synchronized.

## Readiness

See `Current Handoff Summary`.

This plan is not Done until final closeout is complete.
