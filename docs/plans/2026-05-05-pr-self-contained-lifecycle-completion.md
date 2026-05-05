# PR-Self-Contained Lifecycle Completion Plan

## Status

- active

- Owner: maintainers
- Start date: 2026-05-05
- Last updated: 2026-05-05
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow governance, docs, lifecycle validation, selector routing, skills, and generated outputs when canonical skills change. Focused selector-selected checks, lifecycle and review-artifact regression tests, skill validation, generated-output drift checks, adapter validation, and final explicit-path CI are the required proof unless plan-review, test-spec, code-review, review-resolution, or verify elevates broad smoke.

## Purpose / Big Picture

Implement the approved PR-self-contained lifecycle completion amendment. The implementation must remove routine merge-dependent lifecycle closeout, make plan and lifecycle artifact state true inside review-open PRs, preserve real downstream completion events, and add repository-owned validation or reviewer-visible warnings for stale lifecycle wording.

This is workflow-governance and repository-validation work. It changes contributor-visible workflow policy, validation behavior, and generated guidance. It does not introduce runtime product behavior, storage services, deployment changes, external dependencies, or hosted orchestration.

## Source Artifacts

- Proposal: [PR-Self-Contained Lifecycle Completion](../proposals/2026-05-05-pr-self-contained-lifecycle-completion.md), accepted.
- Proposal-review outcome: approved with no material findings.
- Spec: [RigorLoop Workflow](../../specs/rigorloop-workflow.md), approved after spec-review on 2026-05-05.
- Spec-review outcome: approved with no material findings. Minor non-blocking note SR-1: the test spec should decide where merge-dependent language classification is recorded before implementation, such as a tracked file, review-visible output, or change-local artifact.
- Architecture: not required. The approved work changes workflow governance, docs, validation scripts, skill guidance, and generated output without adding a runtime architecture boundary, persistent storage, external integration, or deployment topology.
- Test spec: [RigorLoop workflow test spec](../../specs/rigorloop-workflow.test.md) exists for the broader workflow contract and must be updated by the `test-spec` stage before implementation.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for architecture, data flow, runtime flow, or ownership. Orientation comes from the approved proposal, approved workflow spec, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, current validators, current selector, current skills, and bounded file inventories. If implementation later relies on broader repository-shape claims, refresh `docs/project-map.md` or record a narrower no-map rationale before relying on those claims.

## Context and Orientation

- `specs/rigorloop-workflow.md` is the canonical workflow contract. `docs/workflows.md` is the short operational summary.
- `CONSTITUTION.md` is the top repository governance surface and must receive the targeted PR-self-contained synchronization wording required by `R6dc`.
- `docs/plan.md` is the plan lifecycle index. Concrete plan bodies live under `docs/plans/`.
- Existing `docs/workflows.md` and `docs/learn/topics/plan-lifecycle-closeout.md` still describe merge-dependent `Done` as allowed in limited cases. They need alignment with the approved amendment.
- Existing lifecycle validation covers top-level proposal/spec/test-spec/architecture/ADR status and some related-scope expansion. It does not yet enforce plan-index/body lifecycle agreement or tracked merge-dependent language warnings.
- Existing review-artifact validation owns `review-log.md` and `review-resolution.md` structure. The PR-self-contained amendment may require focused review-artifact or lifecycle-validator proof that open/closed closeout wording cannot contradict recorded findings.
- Existing validation selector routes lifecycle, plan-index, change-local, governance, and workflow-guidance paths to different check sets. The implementation must ensure the warning and blocking checks are selected for the surfaces that can carry stale lifecycle state.
- Canonical authored skill sources live under `skills/`. Generated `.codex/skills/` and public adapter output under `dist/adapters/` must be refreshed only through repository generators when canonical skills change.

## Non-Goals

- Do not inspect hosted PR-description event metadata for merge-dependent language in the first enforcement slice.
- Do not define a merge-SHA recording exception.
- Do not treat deploy, release, package publication, external migration, or unobserved hosted checks as repo-local lifecycle state.
- Do not build post-merge automation as the primary closeout mechanism.
- Do not replace `docs/plan.md` or redesign plan file structure.
- Do not add a broad project-management system.
- Do not add semantic review-quality scoring to validators.
- Do not migrate unrelated historical artifacts unless they are touched, referenced, generated, or authoritative for this change.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R6d`-`R6dc` | Affected-surface alignment in `CONSTITUTION.md`, `AGENTS.md` if needed, `docs/workflows.md`, this plan, and change-local evidence. |
| `R8h`-`R8hc` | Plan lifecycle synchronization wording in governance docs, workflow summary, plan template/guidance if needed, lifecycle validator coverage, and selector/CI proof. |
| `R8j`-`R8jb` | Stale plan lifecycle detection and merge-dependent plan wording classification through lifecycle validation and test fixtures. |
| `R8k`-`R8kj` | Lifecycle artifact status, broader lifecycle inconsistency, review-resolution closeout consistency, readiness wording consistency, and tracked merge-dependent language warnings. |
| Inputs/outputs, state, error behavior, compatibility, observability, edge cases, non-goals, acceptance criteria | Test-spec coverage, workflow docs, validation output, change-local evidence, and final verification notes. |

## Immediate Test-Spec Handoff

After `plan-review` approval, the immediate next repository stage is `test-spec`, not implementation.

The `test-spec` stage must update `specs/rigorloop-workflow.test.md` so it maps the approved PR-self-contained lifecycle completion amendment to concrete proof. It must cover examples E11-E13, requirements `R6dc`, `R8h`-`R8hc`, `R8jb`, `R8kh`-`R8kj`, the new edge cases, and the new acceptance criteria.

The test spec must also resolve spec-review minor note SR-1 by deciding where merge-dependent language classification is recorded before a warning is treated as addressed. The decision must be testable or explicitly manual-verification based.

Implementation milestones are test-first within their scope: add or update the relevant assertion, fixture, or manual test-spec checklist before changing the paired governance wording, validator behavior, selector routing, skill guidance, or generated output.

## Milestones

### M1. Align Governance and Workflow Guidance

- Goal: Make the authoritative and contributor-facing workflow guidance state the PR-self-contained lifecycle rule and remove routine merge-dependent `Done` guidance.
- Requirements: `R6d`-`R6dc`, `R8h`-`R8hc`, `R8jb`, `R8kh`-`R8kj`, acceptance criteria for plan synchronization, downstream events, and merge as fast-forward.
- Files/components likely touched:
  - `CONSTITUTION.md`
  - `AGENTS.md` if its concise guidance conflicts or needs a targeted summary
  - `docs/workflows.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`
  - `docs/plans/0000-00-00-example-plan.md` if plan-template closeout wording needs alignment
  - `specs/rigorloop-workflow.test.md`
  - this plan
- Dependencies:
  - approved `specs/rigorloop-workflow.md`
  - accepted plan-review
  - active updated workflow test spec
- Tests to add/update:
  - Add or update the matching test-spec entries before changing governance wording.
  - Use manual test-spec checks for contributor-facing wording when automation would be brittle.
  - Add stable selector or lifecycle assertions only where the test spec requires machine-checkable proof.
- Implementation steps:
  - Add the targeted constitution wording from `R6dc`.
  - Replace `docs/workflows.md` merge-dependent closeout guidance with PR-self-contained closeout and downstream event handling.
  - Update `AGENTS.md` only if it conflicts or needs a concise pointer after the constitution and workflow summary change.
  - Update the plan lifecycle learn topic so curated guidance no longer recommends the removed merge-dependent exception.
  - Update the example plan only if its closeout wording leaves the old exception ambiguous.
  - Record any affected surface that is intentionally unchanged with rationale in this plan or the change-local pack.
- Validation commands:
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/learn/topics/plan-lifecycle-closeout.md --path docs/plans/0000-00-00-example-plan.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/learn/topics/plan-lifecycle-closeout.md --path docs/plans/0000-00-00-example-plan.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md docs/learn/topics/plan-lifecycle-closeout.md docs/plans/0000-00-00-example-plan.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Expected observable result:
  - Contributors can read governance and workflow guidance and see that repo-local lifecycle synchronization happens in the PR that performs the transition, before review opens.
- Commit message: `M1: align pr-contained lifecycle guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Guidance may overstate the rule and make real downstream deploy or release completion look impossible.
- Rollback/recovery:
  - Revert the guidance edits and keep the approved workflow spec as the source of truth while narrower wording is reviewed.

### M2. Add Lifecycle Validator Coverage

- Goal: Make repository-owned validation block stale plan and broader lifecycle artifact inconsistency, and warn on tracked merge-dependent language.
- Requirements: `R8j`-`R8jb`, `R8kh`-`R8kj`, edge cases 30-34, acceptance criteria for blocking inconsistency and warning behavior.
- Files/components likely touched:
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/artifact_lifecycle_contracts.py` if a plan or warning contract helper is needed
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/review_artifact_validation.py` and `scripts/test-review-artifact-validator.py` if review-resolution closeout consistency is better enforced in the review-artifact validator
  - `tests/fixtures/artifact-lifecycle/**`
  - `tests/fixtures/review-artifacts/**` if review-resolution fixtures are needed
  - `specs/rigorloop-workflow.test.md`
  - this plan
- Dependencies:
  - active updated workflow test spec
  - M1 wording decisions, especially the warning classification surface from SR-1
- Tests to add/update:
  - Add failing fixtures for a completed plan still listed under `## Active`.
  - Add failing fixtures for `docs/plan.md` and plan body lifecycle disagreement.
  - Add failing fixtures for plan readiness wording that still describes a done plan as active or in progress.
  - Add warning fixtures for tracked merge-dependent language.
  - Add pass fixtures for true downstream completion event wording.
  - Add or update review-resolution fixtures for `Closeout status: open` after all findings are resolved and `Closeout status: closed` with missing evidence.
- Implementation steps:
  - Extend lifecycle validation to inspect `docs/plan.md` plus related plan bodies for lifecycle agreement.
  - Add tracked merge-dependent language warning detection in the selected validation scope.
  - Add broader lifecycle inconsistency checks for lifecycle-managed artifacts and readiness surfaces that the validator can inspect deterministically.
  - Reuse review-artifact validation for review-resolution structure where that boundary is cleaner than duplicating logic in lifecycle validation.
  - Keep warnings non-blocking unless the same evidence is also a blocking lifecycle inconsistency.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/artifact_lifecycle_validation.py --path scripts/artifact_lifecycle_contracts.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/review_artifact_validation.py --path scripts/test-review-artifact-validator.py --path tests/fixtures/artifact-lifecycle --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `git diff --check -- scripts tests/fixtures/artifact-lifecycle tests/fixtures/review-artifacts specs/rigorloop-workflow.test.md docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Expected observable result:
  - Stale lifecycle state blocks `branch-ready`, while merge-dependent language is reported as a visible warning unless it is also a blocking inconsistency.
- Commit message: `M2: validate pr-contained lifecycle state`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Warning detection may become noisy if it matches historical context or quoted rejected alternatives.
- Rollback/recovery:
  - Narrow detection to lifecycle-relevant tracked Markdown/YAML sections and keep broader matches as manual review guidance until a better rule is specified.

### M3. Wire Selector, CI, Skills, and Generated Output

- Goal: Ensure the new lifecycle checks run for the right changed surfaces and contributor-facing skills describe the approved rule.
- Requirements: `R6d`-`R6dc`, `R8jb`, `R8kh`-`R8kj`, observability, non-goals, and affected-surface acceptance criteria.
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `scripts/ci.sh` only if warning presentation needs wrapper support beyond existing stdout/stderr behavior
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `scripts/test-skill-validator.py` if stable skill assertions are needed
  - `.codex/skills/**`
  - `dist/adapters/**`
  - this plan
- Dependencies:
  - M1 guidance wording stable
  - M2 validator behavior available
  - active updated workflow test spec
- Tests to add/update:
  - Add selector tests proving changed lifecycle, plan, governance, workflow guidance, and change-local surfaces select the required lifecycle validation or warning check.
  - Add CI wrapper tests only if warning output handling changes.
  - Add focused skill-validator assertions only for stable contractual phrases.
- Implementation steps:
  - Route changed tracked files that can carry lifecycle state to the validation that emits merge-dependent language warnings.
  - Preserve existing selector behavior for generated output and unrelated unsupported paths.
  - Update workflow and stage skills so users know plan closeout, review-resolution closeout, verify, explain-change, and PR handoff must keep lifecycle state synchronized before review opens.
  - Regenerate `.codex/skills/` and public adapter output after canonical skill changes.
  - Keep hosted workflow YAML thin; do not duplicate selector logic in `.github/workflows/ci.yml`.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/ci.sh --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/implement/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `git diff --check -- scripts skills .codex/skills dist/adapters docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Expected observable result:
  - Selector-selected CI runs the new proof where lifecycle state can go stale, and generated skill/adapter guidance matches canonical sources.
- Commit message: `M3: route pr-contained lifecycle checks`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Selector routing may over-select lifecycle validation for ordinary prose-only changes.
- Rollback/recovery:
  - Revert selector expansion and keep warning detection manual for non-lifecycle paths while preserving blocking checks for plan and lifecycle artifacts.

### M4. Close Evidence, Verify, and Prepare PR Handoff

- Goal: Record durable change evidence, complete final validation, and move plan lifecycle state according to the new PR-self-contained rule.
- Requirements: all requirements covered by this plan, especially `R6da`-`R6dc`, `R8h`-`R8kj`, `R10`-`R12f`, and acceptance criteria for reviewability.
- Files/components likely touched:
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml`
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md`
  - optional `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-resolution.md` if material findings require it
  - optional `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/verify-report.md` if verification evidence cannot stay concise
  - `docs/plan.md`
  - this plan
- Dependencies:
  - M1 through M3 complete
  - code-review findings closed or validly deferred before verify
  - generated output in sync if skills changed
- Tests to add/update:
  - No new behavior tests beyond M1-M3 unless code-review, verify, or test-spec identifies a missing proof.
- Implementation steps:
  - Create the baseline non-trivial change-local pack.
  - Record affected surfaces as updated, unaffected with rationale, or deferred with owner and follow-up.
  - Record the no-map rationale and any learn follow-up or no-learn rationale in tracked or review-visible surfaces.
  - Run final selector-selected validation over all touched paths.
  - Update this plan's progress, decisions, discoveries, validation notes, outcome, readiness, and `docs/plan.md` lifecycle state before PR opens for review if the initiative is complete.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/select-validation.py --mode explicit --path <all-touched-paths>`
  - `bash scripts/ci.sh --mode explicit --path <all-touched-paths>`
  - `git diff --check -- <all-touched-paths>`
- Expected observable result:
  - The branch contains synchronized lifecycle state, complete change evidence, passing validation, and a PR-ready explanation grounded in approved artifacts.
- Commit message: `M4: close pr-contained lifecycle evidence`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Final lifecycle closeout could accidentally become self-referential if the plan is marked done before review-resolution, verify, explain-change, and PR handoff are actually complete.
- Rollback/recovery:
  - Keep the plan `Active` until the current PR tree truly contains the completed scope. If a downstream event is still required, name that event and leave the plan active.

## Validation Plan

- Planning change:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `git diff --check -- specs/rigorloop-workflow.md docs/plan.md`
  - `git diff --no-index --check /dev/null docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `git diff --no-index --check /dev/null docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Per milestone: use the validation commands listed in that milestone, then run selector-selected explicit CI for the touched paths.
- Final verification: run all final M4 commands plus any additional checks required by the active test spec, plan-review, code-review, review-resolution, or verify.

## Risks and Recovery

- Over-broad warnings could create noisy CI output. Recovery: narrow warning detection to lifecycle-relevant sections and keep broad prose detection manual.
- Under-selected checks could let stale lifecycle wording land. Recovery: expand selector coverage for changed tracked Markdown/YAML lifecycle surfaces and add selector regression tests.
- Governance docs could conflict with the approved spec. Recovery: treat `specs/rigorloop-workflow.md` as source of truth and repair lower-priority guidance before implementation continues.
- Marking this plan done too early would recreate the problem being fixed. Recovery: leave it active until the PR tree itself contains completed implementation, review-resolution when needed, verification, explain-change, and PR handoff evidence.
- Generated outputs could drift from canonical skills. Recovery: rerun repository generators and keep generated `.codex/skills/` and `dist/adapters/` changes in the same milestone as canonical skill edits.

## Dependencies

- `spec-review` approved the workflow amendment.
- `plan-review` must approve this plan before test-spec or implementation relies on it.
- `test-spec` must update `specs/rigorloop-workflow.test.md` and resolve SR-1 before implementation.
- No architecture or architecture-review is required unless plan-review or test-spec identifies a new boundary or design decision.
- Implementation must preserve user changes and avoid generated-output hand edits.

## Progress

- [x] Proposal accepted.
- [x] Proposal-review approved with no material findings.
- [x] Workflow spec amendment approved by spec-review.
- [x] Execution plan created and added to `docs/plan.md`.
- [x] Plan-review complete.
- [x] Test spec updated and active.
- [x] M1 complete.
- [x] M2 complete.
- [ ] M3 complete.
- [ ] M4 complete.
- [ ] Code-review complete.
- [ ] Verify complete.
- [ ] Explain-change complete.
- [ ] PR handoff complete.

## Decision Log

- 2026-05-05: No architecture stage for this initiative -> the change is workflow-governance and validator behavior over existing repository surfaces, not a new runtime or storage boundary.
- 2026-05-05: Keep broad smoke opt-in unless a later gate elevates it -> targeted selector-selected proof is sufficient for planning, while final verification can still run broader checks if required.
- 2026-05-05: Treat spec-review SR-1 as a test-spec decision -> the spec is approved, but the test spec must pick the observable classification-recording surface before implementation.
- 2026-05-05: Treat merge-dependent warning classification as contributor-visible review evidence, not automatic warning suppression, for the first slice -> this resolves SR-1 without coupling warning detection to hosted PR metadata.
- 2026-05-05: Emit one merge-dependent lifecycle-language warning per tracked file, not one per matching line -> this keeps reviewer attention visible without flooding selected-check output for specs and plans that discuss the old rule as historical context.

## Surprises and Discoveries

- Existing lifecycle validation validates top-level artifact status and related-scope expansion, but plan index/body lifecycle agreement still needs first-class coverage for this amendment.
- Existing selector routing sends governance and workflow guidance to selector regression, while lifecycle validation runs for lifecycle and plan-index paths. The implementation must deliberately route any new tracked-file warning scope.
- Canonical stage skills still contain stale merge-dependent closeout wording after M1; this is intentionally deferred to M3 with generated `.codex/skills/` and `dist/adapters/` refresh so canonical and generated skill output stay aligned in one slice.
- M2 warning output intentionally flags this proposal, spec, test spec, plan, plan index, and M2 review-resolution records because they discuss the removed merge-dependent rule as historical context, rejected alternatives, requirements, warning behavior, or review evidence. That language is classified here as lifecycle-policy discussion and not as an instruction to defer this initiative's closeout after merge.
- M2 review self-check found that a plan listed under both `Active` and `Done` could mask the stale `Active` listing. A focused regression fixture now covers that duplicate-index case.
- M2 code-review found that changing only `docs/plan.md` could miss the linked plan body. CR-M2-R1-F1 is accepted and fixed by expanding index-in-scope validation to linked plan bodies when no selected plan body is already in scope, which avoids turning unrelated historical plan debt into blockers for normal selected validation.

## Validation Notes

- 2026-05-05 planning validation:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md` passed.
  - `git diff --check -- specs/rigorloop-workflow.md docs/plan.md` produced no whitespace diagnostics.
  - `git diff --no-index --check /dev/null docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md` produced no whitespace diagnostics for the new proposal file.
  - `git diff --no-index --check /dev/null docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md` produced no whitespace diagnostics for the new plan file.
- 2026-05-05 test-spec update validation:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md` passed.
  - `git diff --check -- specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md` produced no whitespace diagnostics.
  - `git diff --no-index --check /dev/null docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md` produced no whitespace diagnostics for the new proposal file.
  - `git diff --no-index --check /dev/null docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md` produced no whitespace diagnostics for the new plan file.
- 2026-05-05 M1 validation:
  - `rg -n 'Only merge-dependent `Done` transitions should wait|Use merge-dependent Done only|merge-dependent `Done` transitions may wait|record why only a merge-dependent `Done` transition remains pending|Do not accept deferring a known `Done` transition until after merge|only merge-dependent `Done` transitions may wait' CONSTITUTION.md AGENTS.md docs/workflows.md docs/learn/topics/plan-lifecycle-closeout.md docs/plans/0000-00-00-example-plan.md README.md` produced no matches.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/learn/topics/plan-lifecycle-closeout.md --path docs/plans/0000-00-00-example-plan.md --path README.md --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md` passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression`.
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/learn/topics/plan-lifecycle-closeout.md --path docs/plans/0000-00-00-example-plan.md --path README.md --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md` passed with the same selected check IDs.
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md docs/learn/topics/plan-lifecycle-closeout.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` produced no whitespace diagnostics.
- 2026-05-05 M1 code-review and verify:
  - Code-review first-pass status: `clean-with-notes`, with no blocking or required-change findings.
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/learn/topics/plan-lifecycle-closeout.md --path docs/plans/0000-00-00-example-plan.md --path README.md --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md` passed on the committed M1 tree with selected check IDs `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression`.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
  - `git diff --check HEAD^ HEAD` produced no whitespace diagnostics.
- 2026-05-05 M2 validation:
  - `python scripts/test-artifact-lifecycle-validator.py` failed before implementation with four expected failing M2 lifecycle tests: completed plan under Active, plan index/body disagreement, terminal plan stale readiness, and merge-dependent lifecycle-language warning.
  - `python scripts/test-artifact-lifecycle-validator.py` later failed during M2 self-check with the expected duplicate Active/Done index fixture before the parser was tightened to preserve all index sections for a plan.
  - `python scripts/test-artifact-lifecycle-validator.py` later failed during M2 code-review with the expected index-only `docs/plan.md` regression before the validator expanded plan-index-only scope to linked plan bodies.
  - `python scripts/test-review-artifact-validator.py` passed after adding focused closeout coverage for `Closeout status: open` after resolved material findings, confirming existing closeout-mode behavior.
  - `python scripts/test-artifact-lifecycle-validator.py` passed after implementation.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` passed after recording CR-M2-R1-F1, its resolution, and the clean M2 re-review.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-log.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-resolution.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/code-review-m2-r1.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/code-review-m2-r2.md` passed with non-blocking lifecycle-language warnings classified in Surprises and Discoveries.
  - `python scripts/select-validation.py --mode explicit --path scripts/artifact_lifecycle_validation.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-review-artifact-validator.py --path tests/fixtures/artifact-lifecycle/plan-index-completed-under-active --path tests/fixtures/artifact-lifecycle/plan-index-completed-under-active-and-done --path tests/fixtures/artifact-lifecycle/plan-index-body-disagreement --path tests/fixtures/artifact-lifecycle/plan-terminal-stale-readiness --path tests/fixtures/artifact-lifecycle/plan-downstream-active --path tests/fixtures/artifact-lifecycle/merge-dependent-language-warning --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-log.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-resolution.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/code-review-m2-r1.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/code-review-m2-r2.md` passed and selected `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
  - `bash scripts/ci.sh --mode explicit --path scripts/artifact_lifecycle_validation.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-review-artifact-validator.py --path tests/fixtures/artifact-lifecycle/plan-index-completed-under-active --path tests/fixtures/artifact-lifecycle/plan-index-completed-under-active-and-done --path tests/fixtures/artifact-lifecycle/plan-index-body-disagreement --path tests/fixtures/artifact-lifecycle/plan-terminal-stale-readiness --path tests/fixtures/artifact-lifecycle/plan-downstream-active --path tests/fixtures/artifact-lifecycle/merge-dependent-language-warning --path docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-log.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-resolution.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/code-review-m2-r1.md --path docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/code-review-m2-r2.md` passed with the same selected check IDs.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
  - `git diff --check -- scripts tests/fixtures/artifact-lifecycle docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` produced no whitespace diagnostics.
  - `bash scripts/ci.sh --mode broad-smoke` passed after M2 review-resolution and clean re-review. The broad lifecycle pass reported expected reviewer-attention warnings for merge-dependent policy discussion and unrelated baseline warnings, with no blocking findings.

## Outcome and Retrospective

- Active. M1 aligned governance and workflow guidance, M2 added lifecycle validator coverage and resolved CR-M2-R1-F1, and M3 is next.

## Readiness

- M1 is complete and verified.
- M2 code-review completed with CR-M2-R1-F1 accepted, fixed, resolved, and clean on re-review.
- M3 is the next implementation milestone.
- Test-spec readiness: active; `specs/rigorloop-workflow.test.md` now maps the amendment to T29-T32 plus updated cross-cutting coverage.

## Risks and Follow-Ups

- If merge-SHA recording becomes a real need, create a separate proposal and spec rather than adding an implicit exception during implementation.
