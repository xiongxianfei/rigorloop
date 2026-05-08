# Review Resolution: Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: spec-review-r4
Review closeout: spec-review-r5
Review closeout: plan-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `spec-review-r4`, `spec-review-r5`, `plan-review-r1`, `architecture-review-r1`, `plan-review-r2`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`
- Findings resolved: 23
- Unresolved findings: 0
- Final result: proposal-review R1 identified five major findings and three concerns. Those findings are closed by proposal revisions. Proposal-review R2 approved the revised proposal with no material findings. Spec-review R1 findings are closed by removing the proportional-evidence/tiny-change contract, routing final milestone closeout through `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`, and refreshing current next-artifact sections. Spec-review R2 findings are closed by removing remaining retired route vocabulary, replacing direct-verify closeout wording with final-closeout readiness, aligning autoprogression vocabulary with mandatory or triggered downstream stages, and updating matching test specs. Spec-review R3 finding is closed by replacing remaining stale direct-`verify` milestone-aware closeout wording in examples, tests, code-review guidance, and plan guidance. Spec-review R4 finding is closed by replacing the remaining retired wording, regenerating derived skill and adapter output, and adding case-insensitive hyphen/space-aware static checks for public workflow and shipped skill surfaces. Spec-review R5 approved the amended workflow spec and related proof surfaces with no material findings. Architecture-review R1 approved the latest canonical architecture package update with no material findings. Plan-review R1 findings are closed by normalizing architecture status/readiness, updating plan handoff, moving proof-map confirmation into implementation readiness, and marking M6 as `Milestone type: lifecycle-closeout`. Plan-review R2 approved the execution plan with no material findings. Code-review R1 finding CR1 is closed by the review bookkeeping that made the M1 plan-state surfaces consistent. Code-review R2 found no material findings and closes M1. Code-review R3 found no material findings and closes M2. Code-review R4 findings CR2 and CR3 are closed by canonical skill fixes, generated skill and adapter refresh, and static wording checks that reject the stale direct-final-verify and verify-before-explanation phrases. M3 remains ready for code-review rerun before it can be considered clean.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SWF1 | accepted | resolved | Replaced the proportional-evidence contract with one standard workflow and isolated manual skill invocation language. |
| SWF2 | accepted | resolved | Added the claim boundary that `explain-change` cannot claim final verification, branch-ready, PR-ready, or CI-final status. |
| SWF3 | accepted | resolved | Added public skill allowlist, blocklist, and internal-surface boundary. |
| SWF4 | accepted | resolved | Added required `docs/workflows.md` guide content and reaffirmed that it is not a competing workflow spec. |
| SWF5 | accepted | resolved | Added exact static validation expectations for retired and required wording. |
| SWF6 | accepted | resolved | Added the durable active-plan transition-note surface and required note content. |
| SWF7 | accepted | resolved | Clarified that `ci-maintenance` changes automation/configuration and does not run validation. |
| SWF8 | accepted | resolved | Scoped public skill portability checks to shipped skill surfaces and excluded internal maintenance surfaces. |
| SR1 | accepted | resolved | Removed the tiny-change proportional-evidence contract and replaced it with isolated manual skill invocation language. |
| SR2 | accepted | resolved | Updated milestone final-closeout routing so clean final milestone reviews reach final closeout rather than direct `verify`. |
| SR3 | accepted | resolved | Updated amended spec lifecycle sections so current next artifacts match the draft amendment state. |
| SR4 | accepted | resolved | Removed "trivial work" goal wording and replaced the `architecture-review` trigger with concrete broad-impact, cross-component, migration-heavy, security-sensitive, boundary-changing, or hard-to-reverse conditions. |
| SR5 | accepted | resolved | Replaced direct final-milestone-to-`verify` wording with final closeout routing and final closeout readiness language. |
| SR6 | accepted | resolved | Replaced required-or-default autoprogression wording with mandatory-or-triggered downstream stage wording. |
| SR7 | accepted | resolved | Updated matching test specs to assert one standard workflow, isolated manual skill invocation, and final closeout order without fast-lane preservation. |
| SR8 | accepted | resolved | Replaced remaining milestone-aware examples, tests, code-review guidance, and plan guidance with final closeout routing. |
| SR9 | accepted | resolved | Removed remaining proportional-evidence and fast-lane wording from the workflow spec and public constitution skill, regenerated derived output, and extended static checks for case and hyphen variants. |
| PLR1 | accepted | resolved | Architecture-review R1 approved the canonical architecture package; architecture status/readiness and plan handoff were normalized before plan-review rerun. |
| PLR2 | accepted | resolved | Reworded `test-spec` readiness as readiness to author test-spec and moved proof-map confirmation into implementation readiness. |
| PLR3 | accepted | resolved | Marked M6 as `Milestone type: lifecycle-closeout` rather than a planned implementation milestone state. |
| CR1 | accepted | resolved | M1 plan state surfaces were made internally consistent and M1 is ready for code-review rerun. |
| CR2 | accepted | resolved | Updated `code-review` so a clean final implementation milestone reaches final closeout, not direct `verify`, and added static checks that reject the stale handoff phrase across shipped skill surfaces. |
| CR3 | accepted | resolved | Updated `verify` so workflow-managed final verification runs after durable rationale and before PR while preserving isolated direct `verify`, and added static checks that reject verify-before-explanation wording across shipped skill surfaces. |

## Resolution Entries

### proposal-review-r1

Reconstruction note: This review record was created after proposal edits began, based on the user-provided proposal-review findings in chat and the resulting proposal revisions.

#### SWF1 - Proportional evidence needs a minimum observable contract

Finding ID: SWF1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Replaced the proportional-evidence direction with one recommended standard workflow plus isolated manual skill invocation language. The proposal now says manual skill output does not imply upstream or downstream workflow stages have completed.
Rationale: Removing the alternate evidence-path term avoids ambiguity about whether tiny or size-classified work has a separate completion contract.
Validation target: Proposal contains the standard workflow, manual skill invocation isolation, and no current alternate lane or proportional-evidence contract.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

#### SWF2 - Explain-change must not claim final verification before verify

Finding ID: SWF2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Explain-change before verify` with allowed pre-verify summary content and prohibited claims: final `verify`, `branch-ready`, PR-ready, and CI-final status.
Rationale: Moving `explain-change` before final `verify` requires a clear claim boundary so rationale does not become verification.
Validation target: Proposal defines `explain-change`, `verify`, and `pr` ownership and says `verify` validates that `explain-change.md` exists and is current.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

#### SWF3 - Public skill portability needs an exact allow/block policy

Finding ID: SWF3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Public skill surface boundary` with allowed portable project surfaces and blocked RigorLoop repository-internal surfaces.
Rationale: Static checks need a concrete boundary that is strict enough to keep published skills portable and specific enough to avoid overreach.
Validation target: Proposal lists allowed public skill references and blocked internal references, including RigorLoop-local examples, selector details, drift checks, and shared-block implementation mechanics.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

#### SWF4 - docs/workflows.md generation responsibility needs a required output shape

Finding ID: SWF4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Workflow guide responsibility` with required guide content for `docs/workflows.md`, including the standard workflow and manual skill invocation isolation behavior.
Rationale: The `workflow` skill can own guide creation and refresh by instruction, but the proposal should define the expected guide shape before spec authoring.
Validation target: Proposal lists the required guide sections and states that `docs/workflows.md` is a readable guide, not a competing workflow spec.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

#### SWF5 - Static validation must cover the exact retired and required wording

Finding ID: SWF5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added exact static validation expectations for retired wording, old ordering, public skill internal-path leakage, and required standard workflow plus manual skill invocation wording.
Rationale: The later spec and implementation need narrow, phrase-based validation targets rather than broad prose-quality checks.
Validation target: Proposal names retired phrases such as `fast lane`, `fast-lane`, `mini-spec`, `full-feature lane`, old order patterns, and required replacement phrases.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

#### SWF6 - Active-plan transition rule needs a durable surface

Finding ID: SWF6
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Active plan transition note`, naming active plan current handoff, readiness, or progress sections as the durable surface and listing required note content.
Rationale: Affected active plans should record the current workflow behavior without carrying a long historical explanation of the old order.
Validation target: Proposal says affected active plans record the current final order, preliminary status of prior verification evidence, and the final verify dependency on current `explain-change.md`.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

#### SWF7 - ci-maintenance placement should clarify trigger timing

Finding ID: SWF7
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `CI-maintenance boundary`, stating that `ci-maintenance` is triggered only when hosted workflow automation, validation automation, or related platform configuration must be created or changed.
Rationale: `ci-maintenance` should not become a general validation-running stage or replace `verify`.
Validation target: Proposal says `ci-maintenance` is not the stage that runs validation and that validation execution and branch-ready proof remain owned by `verify`.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

#### SWF8 - Public-skill check must distinguish canonical public skills from internal docs

Finding ID: SWF8
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added portability-check scope: canonical skill files shipped to users, generated public skill copies, and public adapter skill copies are in scope; internal specs, plans, tests, generator scripts, maintainer docs, and repository-only contributor docs are out of scope.
Rationale: The boundary should protect published skills without blocking repository maintenance documents.
Validation target: Proposal names both in-scope and out-of-scope surfaces for public skill portability checks.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed; `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` passed.

### proposal-review-r2

No material findings.

### spec-review-r1

#### SR1 - Proportional evidence conflicts with mandatory stage wording

Finding ID: SR1
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Removed the tiny-change and proportional-evidence contract from the amended workflow spec and proposal. Replaced it with one recommended standard workflow plus isolated manual skill invocation language, and aligned public workflow docs and shipped skill text to the same model.
Rationale: The owner decision avoids an ambiguous alternate evidence path. Manual skill output remains useful but does not claim omitted upstream or downstream stages completed.
Validation target: Updated `specs/rigorloop-workflow.md`, `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`, `CONSTITUTION.md`, `README.md`, `docs/workflows.md`, canonical skills, and generated skill/adapter copies.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed; `bash scripts/ci.sh --mode explicit ...` passed selected review-artifact, lifecycle, skill, adapter, README, selector, and change-metadata checks.

#### SR2 - Milestone closeout still routes clean final reviews directly to verify

Finding ID: SR2
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Replaced direct final-milestone-to-`verify` routing with final-closeout routing. Clean final implementation milestone review now reaches `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`, once implementation milestones and required review-resolution are closed.
Rationale: The accepted proposal and new autoprogression direction require final closeout to run `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`. Direct `verify` routing would recreate the old ordering bug for milestone-based work.
Validation target: Updated milestone routing requirements, edge cases, acceptance criteria, public workflow docs, and stage-local handoff guidance.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed; `bash scripts/ci.sh --mode explicit ...` passed selected review-artifact, lifecycle, skill, adapter, README, selector, and change-metadata checks.

#### SR3 - Amended spec lifecycle sections have stale or incomplete next-artifact guidance

Finding ID: SR3
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Updated current `Next artifacts` sections in the amended workflow, autoprogression, and skill-contract specs to name spec-review, matching test-spec updates after spec-review approval, and execution planning after spec-review resolves.
Rationale: Draft specs should route downstream work without requiring agents to infer which historical next-artifact entries still apply to this amendment.
Validation target: Updated `Next artifacts`, `Follow-on artifacts`, and `Readiness` sections in the amended specs.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed; `bash scripts/ci.sh --mode explicit ...` passed selected review-artifact, lifecycle, skill, adapter, README, selector, and change-metadata checks.

### spec-review-r2

#### SR4 - Retired size and risk route vocabulary still appears in the workflow contract

Finding ID: SR4
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Rewrote the workflow goal around isolated individual skill output instead of "trivial work" and replaced the `architecture-review` trigger with concrete broad-impact, cross-component, migration-heavy, security-sensitive, boundary-changing, or hard-to-reverse design conditions.
Rationale: The accepted direction says RigorLoop has one recommended standard workflow and does not classify work into public route categories such as tiny, low-risk, high-risk, fast-lane, or full-lane.
Validation target: `specs/rigorloop-workflow.md` no longer uses size or risk route vocabulary to define workflow routing; concrete triggers remain available for conditional review stages.
Validation evidence: A focused stale-term `rg` scan returned no matches on the amended workflow specs, matching test specs, workflow guide, constitution, and affected skills; selected CI passed.

#### SR5 - Lifecycle closeout still exposes direct verify routing and old verify-readiness terms

Finding ID: SR5
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Updated governing specs, workflow guide wording, and matching test specs so final closeout routes through `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`.
Rationale: Direct final-milestone-to-`verify` wording recreates the old ordering problem after the amendment moved durable rationale before final verification.
Validation target: `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/milestone-aware-review-handoff.md`, `docs/workflows.md`, and matching test specs use final-closeout readiness and the current final order.
Validation evidence: `bash scripts/ci.sh --mode explicit ...` passed selected skills, adapter, review artifact, lifecycle, metadata, and selector checks after the final-closeout wording update.

#### SR6 - Autoprogression still uses undefined required-or-default routing

Finding ID: SR6
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Replaced "required or default downstream stage" and "required or default downstream step" with "mandatory or triggered downstream stage" or "mandatory or triggered downstream step" in the autoprogression spec, matching tests, and affected stage skills.
Rationale: The main workflow contract now defines continuation with mandatory or triggered downstream stages. Keeping an undefined default-stage term makes conditional review handoff behavior ambiguous.
Validation target: `specs/workflow-stage-autoprogression.md` and its matching tests use routing vocabulary that matches `specs/rigorloop-workflow.md`.
Validation evidence: `rg -n 'required or default downstream stage|required or default downstream step' skills .codex/skills dist/adapters specs/workflow-stage-autoprogression.md specs/workflow-stage-autoprogression.test.md` returned no matches; generated skill and adapter drift checks passed.

#### SR7 - Matching test specs still assert retired fast-lane and direct-verify behavior

Finding ID: SR7
Disposition: accepted
Status: resolved
Owner: test-spec owner
Owning stage: test-spec
Chosen action: Updated `specs/rigorloop-workflow.test.md`, `specs/workflow-stage-autoprogression.test.md`, and `specs/milestone-aware-review-handoff.test.md` so they assert one recommended standard workflow, isolated manual skill invocation, `ci-maintenance` before `explain-change` when triggered, and final `explain-change -> verify -> pr` ordering.
Rationale: Tests that preserve fast-lane eligibility or direct lifecycle-closeout entry into `verify` would prove behavior the amendment is retiring.
Validation target: `specs/rigorloop-workflow.test.md`, `specs/workflow-stage-autoprogression.test.md`, and `specs/milestone-aware-review-handoff.test.md` assert one standard workflow, isolated manual skill invocation, and final closeout order without fast-lane preservation.
Validation evidence: `python scripts/test-skill-validator.py` passed 43 tests; `bash scripts/ci.sh --mode explicit ...` passed selected regression, drift, adapter, review-artifact, lifecycle, change-metadata, and selector checks.

### spec-review-r3

#### SR8 - Stale direct-verify closeout wording remains in milestone-aware surfaces

Finding ID: SR8
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Updated milestone-aware examples, matching test specs, code-review handoff guidance, and plan guidance so final milestone closeout routes through `ci-maintenance` when triggered, otherwise `explain-change`, before `verify` and `pr`.
Rationale: Direct final-milestone-to-`verify` wording conflicts with the current final closeout sequence and would let tests or public skill guidance preserve the ordering bug this amendment is meant to remove.
Validation target: `specs/milestone-aware-review-handoff.md`, `specs/workflow-stage-autoprogression.md`, `specs/workflow-stage-autoprogression.test.md`, `specs/milestone-aware-review-handoff.test.md`, and `skills/code-review/SKILL.md` use final closeout readiness and the current final closeout order rather than direct final-milestone-to-`verify` routing.
Validation evidence: Focused stale direct-`verify` closeout scan over amended specs, matching test specs, `code-review`, `plan`, workflow docs, constitution, and root guidance returned no matches; `python scripts/test-skill-validator.py` passed 43 tests; generated skill and adapter drift checks passed.

### spec-review-r4

#### SR9 - Retired proportional-evidence and fast-lane wording remains

Finding ID: SR9
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Replaced the workflow spec UX bullet with concise contributor-facing workflow and isolated-manual-skill wording, replaced the public constitution skill section with standard workflow and manual skill invocation guidance, regenerated generated skill and adapter copies, and extended static retired-term checks to catch case-insensitive hyphen or space variants.
Rationale: The accepted direction uses one standard workflow and isolated manual skill invocation. Keeping retired evidence or lane vocabulary in public contract or skill text preserves the route confusion the amendment is intended to remove.
Validation target: `specs/rigorloop-workflow.md`, `skills/constitution/SKILL.md`, generated skill copies, generated adapter copies when affected, and static wording checks no longer allow proportional-evidence or fast-lane variants on public workflow or shipped skill surfaces.
Validation evidence: `python -m unittest scripts.test-skill-validator.SkillValidatorFixtureTests.test_public_workflow_and_skill_surfaces_block_retired_route_vocabulary` failed before generated output was refreshed, then passed after regeneration; focused public-surface retired-term `rg` scan returned no matches; `python scripts/test-skill-validator.py` passed 45 tests after adding the workflow-spec forbidden-context check; generated skill and adapter drift checks passed.

### spec-review-r5

No material findings.

### plan-review-r1

#### PLR1 - Plan-review is premature while required architecture-review is still pending

Finding ID: PLR1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: architecture-review
Chosen action: Ran architecture-review R1 for the latest canonical architecture package update, normalized the architecture package to `approved`, and updated the active plan handoff to `plan-review` rerun.
Rationale: The plan itself identifies architecture-review as the next gate, and the architecture package remains draft. Approving plan-review now would create an invalid handoff to `test-spec`.
Validation target: `docs/architecture/system/architecture.md` and its C4 diagrams have a completed architecture-review outcome, and the plan's handoff reflects the next actual gate before plan-review rerun.
Validation evidence: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/architecture-review-r1.md` approved the canonical package with no material findings; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed; `bash scripts/ci.sh --mode explicit --path docs/architecture/system/architecture.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.

#### PLR2 - Test-spec readiness is stated as requiring test-spec completion

Finding ID: PLR2
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Rewrote `test-spec` readiness so `test-spec` authoring is not ready until architecture-review and plan-review are complete, and moved proof-map confirmation against the approved plan into implementation readiness.
Rationale: The current wording makes readiness for `test-spec` depend on the output of `test-spec` itself, which blurs immediate handoff and downstream proof completion.
Validation target: The plan distinguishes `test-spec` readiness from test-spec closeout and keeps immediate handoff wording aligned with `specs/rigorloop-workflow.md` R7p-R7q.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed; `bash scripts/ci.sh --mode explicit --path docs/architecture/system/architecture.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.

#### PLR3 - Lifecycle closeout is formatted like an implementation milestone

Finding ID: PLR3
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Replaced the M6 implementation-style `Milestone state: planned` field with `Milestone type: lifecycle-closeout`.
Rationale: Downstream-only gates should not be interpreted as an unfinished implementation milestone that blocks final closeout readiness decisions.
Validation target: The plan unmistakably excludes lifecycle closeout from in-scope implementation milestone state decisions while preserving the final closeout sequence.
Validation evidence: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed; `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed; `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.

### architecture-review-r1

No material findings.

### plan-review-r2

No material findings.

### code-review-r1

#### CR1 - M1 milestone state conflicts with the M1 handoff state

Finding ID: CR1
Disposition: accepted
Status: resolved
Owner: implementation owner
Owning stage: review-resolution
Chosen action: Closed CR1 as already fixed by the review bookkeeping that aligned the active plan, plan index, review log, review resolution, and change metadata.
Rationale: Workflow-managed milestone handoff depends on consistent plan state. A handoff summary that says `review-requested` while the milestone section says `implementing` can mislead later review-resolution, implementation, or final-closeout routing.
Validation target: The active plan, plan index, change metadata, review log, and review resolution all reflect code-review R1 and no longer expose conflicting current M1 state.
Final action: Closed CR1 as already fixed by review bookkeeping. The active plan, plan index, review log, review resolution, and change metadata now consistently treat CR1 as resolved and route M1 back to `code-review M1` rerun.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed; `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed; `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md` passed.

### code-review-r2

No material findings.

### code-review-r3

No material findings.

### code-review-r4

#### CR2 - Code-review Handoff still routes final implementation closeout directly to verify

Finding ID: CR2
Disposition: accepted
Status: resolved
Owner: implementation owner
Owning stage: review-resolution
Chosen action: Updated `skills/code-review/SKILL.md` so a clean final implementation milestone reaches final closeout, not direct `verify`. Final closeout runs `ci-maintenance` when triggered, otherwise `explain-change`, then `verify`, then `pr`.
Rationale: The approved workflow routes final implementation closeout through `ci-maintenance` when triggered, otherwise `explain-change`, before `verify` and `pr`. A top-level public Handoff line that says final clean review can route to `verify` preserves the retired ordering.
Validation target: `skills/code-review/SKILL.md`, generated code-review skill copies, and `scripts/test-skill-validator.py` reject the stale direct-verify final-handoff phrase.
Validation evidence: `python scripts/test-skill-validator.py` passed 47 tests, including `test_code_review_and_verify_public_skills_use_final_closeout_order`; `python scripts/build-skills.py --check` passed; `python scripts/build-adapters.py --version 0.1.1 --check` passed; the stale-phrase scan over `skills`, `.codex/skills`, and `dist/adapters` returned no matches.

#### CR3 - Verify skill still describes verification before explanation

Finding ID: CR3
Disposition: accepted
Status: resolved
Owner: implementation owner
Owning stage: review-resolution
Chosen action: Updated `skills/verify/SKILL.md` so workflow-managed final `verify` runs after durable change rationale exists and before PR, while preserving isolated direct `verify` behavior.
Rationale: The approved workflow moved `explain-change` before final `verify`. Public `verify` text that says verification happens before explanation can cause future agents to recreate the ordering bug.
Validation target: `skills/verify/SKILL.md`, generated verify skill copies, and `scripts/test-skill-validator.py` reject stale verify-before-explanation wording.
Validation evidence: `python scripts/test-skill-validator.py` passed 47 tests, including `test_code_review_and_verify_public_skills_use_final_closeout_order`; `python scripts/build-skills.py --check` passed; `python scripts/build-adapters.py --version 0.1.1 --check` passed; the stale-phrase scan over `skills`, `.codex/skills`, and `dist/adapters` returned no matches.
