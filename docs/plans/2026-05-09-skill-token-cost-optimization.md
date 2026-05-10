# Skill Token Cost Optimization Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-09
- Last updated: 2026-05-10
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: standard
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow-governance Markdown, specs, canonical skill guidance, static validation, generated local skill mirrors, public adapter package copies, and change-local evidence. It does not add runtime services, persistence, network behavior, deployment infrastructure, release packaging format, or public API behavior.

## Purpose / Big Picture

Implement the approved skill token-cost optimization contract.

The intended invariant is:

```text
Find the smallest evidence surface that can answer the current question.
Correctness still outranks token savings.
```

The implementation tightens the skill contract, test coverage, shared evidence guidance, selected high-volume skills, generated skill output, and public adapters so agents prefer bounded evidence before broad reads without weakening full-file review obligations or validation coverage.

## Source Artifacts

- Proposal: [Skill Token Cost Optimization](../proposals/2026-05-09-skill-token-cost-optimization.md), accepted after clean proposal-review.
- Spec: [Skill Token Cost Optimization](../../specs/skill-token-cost-optimization.md), approved after clean spec-review.
- Architecture: no runtime architecture impact. No-impact rationale is recorded in the spec. Architecture-review approved that rationale on 2026-05-09 with no material findings.
- Test spec: [Skill Token Cost Optimization Test Spec](../../specs/skill-token-cost-optimization.test.md), active.
- Change metadata: `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on project-map claims for runtime ownership, storage, service boundaries, or module topology. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, the accepted proposal, approved spec, existing skill-contract artifacts, canonical skills, generator scripts, and validator patterns.

## Context and Orientation

- `specs/skill-token-cost-optimization.md` owns the behavior contract for bounded evidence, full-file-read escape conditions, output-cap limits, first-slice skill scope, public portability, and adapter validation.
- `specs/skill-contract.md` is the normative skill-contract source that must receive the accepted amendment.
- `specs/skill-contract.test.md` and `scripts/test-skill-validator.py` are the likely static proof surfaces.
- `templates/shared/evidence-collection-efficiency.md` is the shared evidence guidance block used by normalized skills.
- The first-slice skill set from the spec is `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `implement`, `code-review`, `verify`, `pr`, and `learn`.
- Additional skills with existing evidence guidance may be included only when doing so reduces drift without broadening the behavior contract.
- `.codex/skills/` and `dist/adapters/` are generated output. Do not hand-edit them.

## Non-Goals

- Do not change workflow stage order.
- Do not add a new token-budget skill.
- Do not reduce required validation coverage.
- Do not remove full-file-read obligations.
- Do not replace formal artifacts with chat summaries.
- Do not add broad natural-language quality scoring.
- Do not expose repository-maintainer-only generated-output or adapter mechanics in published skill text.
- Do not migrate historical learn sessions or historical proposals.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`, `R1a`, `R1b` | `specs/skill-contract.md`, skill-contract test spec, selected skills, manual review. |
| `R2`, `R2a`, `R2b`, `R2c` | Shared evidence block, selected high-volume skills, static validator checks. |
| `R3`, `R3a`-`R3f` | Skill-contract amendment, shared block, selected skills, validator checks, manual review. |
| `R4`, `R4a`, `R4b` | Skill-contract amendment, shared block, selected skills, validator checks for output-cap distinction. |
| `R5`, `R5a`-`R5c` | Workflow summary and skill wording where summary-first output guidance applies. |
| `R6`, `R6a`-`R6e` | First implementation slice, test spec, skill-contract tests, selected skills. |
| `R7`, `R7a`-`R7c` | Published skill wording and public-surface portability checks. |
| `R8`, `R8a`-`R8d` | `scripts/test-skill-validator.py` and manual review. |
| `R9`, `R9a`-`R9c` | Generated skill drift, adapter drift, adapter validation, adapter distribution tests. |
| `R10`, `R10a`, `R10b` | Review guidance in affected review skills and test-spec/manual review coverage. |
| Acceptance criteria | Test spec and validator/static checks for bounded evidence, escape conditions, output caps, portability, no new token-budget skill, and generated/adapter validation. |

## Current Handoff Summary

- Current milestone: PR handoff
- Current milestone state: final-verified
- Last reviewed milestone: M5. Final Verification and PR Handoff
- Review status: code-review M5 completed cleanly with no material findings. Final verification passed.
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: ready
- Reason final closeout is or is not ready: M1-M4 implementation review loops passed, required review-resolution is closed, and final verify passed; PR handoff remains open.

## Pre-Implementation Gates

These gates are not in-scope implementation milestones and do not count toward M1-M4 closeout.

- Plan-review rerun approves the revised plan after `STCO-PR1-F1` resolution. Completed on 2026-05-09.
- Architecture-review approves the no-impact rationale recorded in the approved spec. Completed on 2026-05-09.
- `test-spec` creates `specs/skill-token-cost-optimization.test.md`. Completed on 2026-05-09.
- The test spec maps each `MUST` to static validation, generated-output validation, adapter validation, or manual review. Completed on 2026-05-09.
- Change metadata and this plan are updated after test-spec with current readiness. Completed on 2026-05-09.
- Validation after test-spec:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- docs/proposals/2026-05-09-skill-token-cost-optimization.md specs/skill-token-cost-optimization.md specs/skill-token-cost-optimization.test.md docs/plans/2026-05-09-skill-token-cost-optimization.md docs/plan.md docs/changes/2026-05-09-skill-token-cost-optimization`

## Milestones

### M1. Skill Contract and Static Proof

- Milestone state: closed
- Goal: Amend the normative skill contract and add focused validator coverage for token-cost behavior.
- Requirements: `R1`-`R6`, `R8`, `R10`, acceptance criteria.
- Files/components likely touched:
  - `specs/skill-contract.md`
  - `specs/skill-contract.test.md`
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - this plan
- Dependencies:
  - Pre-implementation gates complete.
  - Test spec active.
- Tests to add/update:
  - Static checks for bounded-evidence-first wording.
  - Static checks that full-file-read escape conditions are preserved.
  - Static checks that output caps are not query design.
  - Static checks that validation semantics are not weakened.
  - Static checks that no `token-budget` skill is required.
- Implementation steps:
  - Add the accepted token-cost discipline amendment to `specs/skill-contract.md`.
  - Update `specs/skill-contract.test.md` coverage maps and test cases.
  - Add focused tests to `scripts/test-skill-validator.py`.
  - Avoid broad natural-language quality scoring.
  - Update plan progress and change metadata.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-token-cost-optimization.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- specs/skill-token-cost-optimization.md specs/skill-contract.md specs/skill-contract.test.md scripts/test-skill-validator.py docs/plans/2026-05-09-skill-token-cost-optimization.md docs/plan.md docs/changes/2026-05-09-skill-token-cost-optimization`
- Expected observable result: The normative skill contract and tests make the token-cost behavior implementable without guessing.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M1
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M2
- Commit message: `M1: define token cost skill contract`
- Milestone closeout:
  - targeted validation passed
  - lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Static tests could become brittle prose matching.
  - Skill-contract changes could conflict with existing shared-block wording.
- Rollback/recovery:
  - Revert the spec/test/validator edits and keep M1 in `resolution-needed` until the contract proof is narrowed.

### M2. Shared Evidence Guidance and Canonical Skills

- Milestone state: closed
- Goal: Update shared evidence guidance and selected canonical skills so high-volume stages use bounded evidence before broad reads.
- Requirements: `R2`-`R7`, `R10`, acceptance criteria.
- Files/components likely touched:
  - `templates/shared/evidence-collection-efficiency.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
  - `skills/workflow/SKILL.md`, as an existing shared-block consumer kept aligned to avoid drift
  - `docs/workflows.md`, only if the test spec or review determines the current summary needs tightening
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - this plan
- Dependencies:
  - M1 closed.
- Tests to add/update:
  - Skill validator checks for selected skill wording.
  - Shared-block drift checks, if existing validator structure supports them.
  - Manual review for public-skill portability and no weakening of full-file-read obligations.
- Implementation steps:
  - Tighten the shared evidence block with bounded-evidence-first, output-cap, and escape-condition wording.
  - Update selected first-slice skills to use the tightened guidance.
  - Keep public skill wording project-portable.
  - Update workflow summary only if needed to clarify output caps or prevent drift.
  - Update tests and plan/change metadata.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path templates/shared/evidence-collection-efficiency.md --path skills/workflow/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path skills/learn/SKILL.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- docs/workflows.md templates/shared/evidence-collection-efficiency.md skills/workflow/SKILL.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md skills/spec/SKILL.md skills/spec-review/SKILL.md skills/plan/SKILL.md skills/plan-review/SKILL.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/pr/SKILL.md skills/learn/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-skill-token-cost-optimization.md docs/changes/2026-05-09-skill-token-cost-optimization`
- Expected observable result: In-scope skills guide agents to collect bounded evidence first, preserve correctness escape conditions, and avoid treating output caps as query design.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M2
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M3
- Commit message: `M2: tighten evidence collection skills`
- Milestone closeout:
  - targeted validation passed
  - lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Updating many skills could broaden the diff.
  - Public skill text could accidentally expose maintainer-only paths or commands.
- Rollback/recovery:
  - Split M2 into smaller skill groups if review finds the slice too large, or revert the shared-block/skill edits and keep the validator proof from M1.

### M3. Generated Skill and Adapter Output

- Milestone state: closed
- Goal: Refresh derived outputs after canonical skill changes and prove public adapter packages remain valid.
- Requirements: `R7`, `R9`, acceptance criteria.
- Files/components likely touched:
  - `.codex/skills/`
  - `dist/adapters/`
  - `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - this plan
- Dependencies:
  - M2 closed.
- Tests to add/update:
  - Existing generated-output and adapter distribution tests should cover this milestone.
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run generated-output and adapter validation checks.
  - Update plan/change metadata.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-05-09-skill-token-cost-optimization.md docs/changes/2026-05-09-skill-token-cost-optimization`
- Expected observable result: Generated local skill output and public adapter packages are deterministic, current, and validation-clean.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M3
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M4
- Commit message: `M3: refresh token cost skill outputs`
- Milestone closeout:
  - targeted validation passed
  - lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Generated output can be large and obscure authored changes.
  - Adapter validation can fail if canonical skill wording violates public portability.
- Rollback/recovery:
  - Re-run generators from canonical sources or revert generated output with the canonical skill edits that caused it.

### M4. Change Evidence and Lifecycle Closeout Preparation

- Milestone state: closed
- Goal: Prepare durable explanation and lifecycle evidence after all implementation milestones are reviewed.
- Requirements: all requirements and acceptance criteria.
- Files/components likely touched:
  - `docs/changes/2026-05-09-skill-token-cost-optimization/explain-change.md`
  - `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `docs/plans/2026-05-09-skill-token-cost-optimization.md`
  - `docs/plan.md`
- Dependencies:
  - M1-M3 closed.
  - Any required review-resolution closed.
- Tests to add/update:
  - No new code tests expected; this milestone records evidence and runs lifecycle validation.
- Implementation steps:
  - Write `explain-change.md` linking the real diff to proposal, spec, architecture no-impact rationale, plan milestones, tests, review outcomes, and validation evidence.
  - Update `change.yaml` with final implementation evidence.
  - Synchronize this plan and `docs/plan.md` for final verify readiness.
  - Keep the plan active until verify and PR handoff complete.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-skill-token-cost-optimization`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml --path docs/changes/2026-05-09-skill-token-cost-optimization/explain-change.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-05-09-skill-token-cost-optimization docs/plans/2026-05-09-skill-token-cost-optimization.md docs/plan.md`
- Expected observable result: Durable change rationale and lifecycle evidence are ready for final verification.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M4
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before final verify
- Commit message: `M4: document token cost closeout`
- Milestone closeout:
  - targeted validation passed
  - lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Rationale could duplicate live state instead of linking to the active plan handoff summary.
- Rollback/recovery:
  - Revert evidence-only artifacts or update them to match the accepted review state before verify.

### M5. Final Verification and PR Handoff

- Milestone state: lifecycle-closeout
- Goal: Perform final lifecycle closeout after M1-M4 have each passed their milestone review loop.
- Requirements: all requirements and acceptance criteria.
- Files/components likely touched:
  - `docs/plans/2026-05-09-skill-token-cost-optimization.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
- Dependencies:
  - M1-M4 closed.
  - Required review-resolution closed.
  - Explain-change evidence complete.
- Tests to add/update:
  - No new tests expected; final verification runs the approved proof scope.
- Implementation steps:
  - Run final verify.
  - Synchronize this plan and `docs/plan.md` before PR opens.
  - Prepare PR handoff only after verify passes.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-skill-token-cost-optimization`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/workflows.md --path templates/shared/evidence-collection-efficiency.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml --path docs/changes/2026-05-09-skill-token-cost-optimization/explain-change.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode explicit --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path templates/shared/evidence-collection-efficiency.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path skills/learn/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- .`
- Expected observable result: Branch is verified and ready for PR handoff, with plan/index lifecycle state synchronized inside the PR.
- Commit message: `M5: verify token cost optimization`
- Risks:
  - Final selected CI may need additional explicit paths if implementation touches additional skills.
- Rollback/recovery:
  - Fix failing validation in the owning milestone, rerun the affected review loop if material, then rerun final verify.

## Validation Plan

- Run targeted validation inside each milestone before code-review handoff.
- Run `code-review` for each in-scope implementation milestone M1-M4.
- Run review-resolution when code-review records material findings.
- Run generated skill and adapter checks after canonical skill changes.
- Run final verify only after M1-M4 are closed and required review-resolution is closed.

## Risks and Recovery

- Risk: Token-cost wording could encourage under-reading. Recovery: preserve full-file-read escape conditions and require correctness to outrank token savings.
- Risk: Static checks could become brittle. Recovery: narrow phrase checks to stable sections, examples, or requirement IDs and avoid broad semantic scoring.
- Risk: Public skill text could expose maintainer internals. Recovery: keep repository-specific commands in specs, plans, tests, and change-local evidence; use project-portable wording in shipped skills.
- Risk: Generated output can obscure authored changes. Recovery: review canonical skill diffs before generated diffs and validate generated output with repo-owned scripts.

## Dependencies

- Architecture-review of the no-impact rationale must pass before implementation starts.
- Plan-review must pass before test-spec and implementation.
- Test-spec must be active before implementation.
- M1 must close before M2 starts.
- M2 must close before M3 starts.
- M3 must close before M4 starts.
- M4 must close before final verify.
- M5 final lifecycle closeout runs only after M1-M4 have each passed their milestone review loop and any required review-resolution is closed.

## Progress

- 2026-05-09: Proposal accepted after clean proposal-review.
- 2026-05-09: Spec approved after clean spec-review.
- 2026-05-09: Architecture no-impact rationale recorded in the approved spec.
- 2026-05-09: Plan created and indexed as active.
- 2026-05-09: Plan-review R1 recorded `STCO-PR1-F1`; plan revised to remove M0 and represent pre-implementation review/test-spec work as gates outside the implementation milestone set.
- 2026-05-09: Plan-review rerun approved the revised plan with no material findings.
- 2026-05-09: Architecture-review approved the no-impact rationale with no material findings.
- 2026-05-09: Test spec created and activated.
- 2026-05-09: M1 implemented the token-cost discipline amendment in `specs/skill-contract.md`, updated `specs/skill-contract.test.md`, and added focused static proof in `scripts/test-skill-validator.py`.
- 2026-05-09: code-review M1 completed cleanly with no material findings; M1 closed and handoff moved to M2.
- 2026-05-09: M2 tightened the shared evidence guidance, copied it into the selected high-volume skills, and aligned the existing `workflow` shared-block consumer to avoid drift.
- 2026-05-09: code-review M2 completed cleanly with no material findings; M2 closed and handoff moved to M3.
- 2026-05-09: M3 refreshed generated local skill mirrors and public adapter packages from canonical skill updates.
- 2026-05-09: code-review M3 completed cleanly with no material findings; M3 closed and handoff moved to M4.
- 2026-05-10: M4 recorded durable explain-change evidence and refreshed change metadata for code-review handoff.
- 2026-05-10: `docs/plan.md` remains unchanged in M4 because the initiative is still active; the lifecycle index transition belongs to M5 after M4 code-review closes.
- 2026-05-10: code-review M4 completed cleanly with no material findings; M4 closed and handoff moved to M5 final lifecycle closeout.
- 2026-05-10: M5 final verification passed and plan/index lifecycle state was synchronized for PR handoff.
- 2026-05-10: code-review M5 completed cleanly with no material findings; PR handoff remains the next lifecycle action.

## Decision Log

- 2026-05-09: Use one focused plan with M1-M4 implementation milestones and M5 lifecycle closeout. Rationale: the work crosses specs, skills, validators, generated output, adapters, and lifecycle evidence, but can be reviewed in small slices.
- 2026-05-09: Treat architecture-review as a pre-implementation dependency rather than an implementation milestone. Rationale: the architecture surface is a no-impact rationale already recorded in the approved spec.
- 2026-05-09: Keep `docs/workflows.md` conditional in M2. Rationale: the spec leaves open whether the existing workflow summary is sufficient after skill-contract and skill updates.
- 2026-05-09: Removed M0 and made pre-implementation review/test-spec work a gate section. Rationale: plan-review cannot be an implementation step inside a milestone it approves, and test-spec authoring is not lifecycle closeout.
- 2026-05-09: Use the active test spec as the proof surface for M1-M5. Rationale: every `MUST` maps to static validation, generated-output or adapter validation, or manual review before implementation starts.
- 2026-05-09: Keep M1 proof limited to the skill contract, skill-contract test spec, validator checks, and no `token-budget` skill path. Rationale: canonical skill wording belongs to M2, while generated output and adapter proof belong to M3.
- 2026-05-09: Include `skills/workflow/SKILL.md` in M2 only as a shared-block drift alignment. Rationale: it already consumed `templates/shared/evidence-collection-efficiency.md`, so leaving it stale would violate the existing shared-block drift contract without expanding token-cost behavior scope.

## Surprises and Discoveries

- none yet

## Validation Notes

- 2026-05-09: Plan creation validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- docs/proposals/2026-05-09-skill-token-cost-optimization.md specs/skill-token-cost-optimization.md docs/plans/2026-05-09-skill-token-cost-optimization.md docs/plan.md docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
- 2026-05-09: Artifact lifecycle validation emitted the existing `docs/plan.md` lifecycle-language warning at line 19.
- 2026-05-09: Test-spec creation validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- docs/proposals/2026-05-09-skill-token-cost-optimization.md specs/skill-token-cost-optimization.md specs/skill-token-cost-optimization.test.md docs/plans/2026-05-09-skill-token-cost-optimization.md docs/plan.md docs/changes/2026-05-09-skill-token-cost-optimization`
- 2026-05-09: Artifact lifecycle validation during test-spec creation emitted the existing `docs/plan.md` lifecycle-language warning at line 19.
- 2026-05-09: M1 targeted validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-token-cost-optimization.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- specs/skill-token-cost-optimization.md specs/skill-contract.md specs/skill-contract.test.md scripts/test-skill-validator.py docs/plans/2026-05-09-skill-token-cost-optimization.md docs/plan.md docs/changes/2026-05-09-skill-token-cost-optimization`
- 2026-05-09: Artifact lifecycle validation during M1 emitted the existing `docs/plan.md` lifecycle-language warning at line 19.
- 2026-05-09: M2 targeted validation passed:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path templates/shared/evidence-collection-efficiency.md --path skills/workflow/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path skills/learn/SKILL.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- docs/workflows.md templates/shared/evidence-collection-efficiency.md skills/workflow/SKILL.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md skills/spec/SKILL.md skills/spec-review/SKILL.md skills/plan/SKILL.md skills/plan-review/SKILL.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/pr/SKILL.md skills/learn/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-skill-token-cost-optimization.md docs/changes/2026-05-09-skill-token-cost-optimization`
- 2026-05-09: Artifact lifecycle validation during M2 emitted the existing `docs/workflows.md` lifecycle-language warning at line 195.
- 2026-05-09: M3 targeted validation passed:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-05-09-skill-token-cost-optimization.md docs/changes/2026-05-09-skill-token-cost-optimization`
- 2026-05-10: M4 targeted validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-skill-token-cost-optimization`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml --path docs/changes/2026-05-09-skill-token-cost-optimization/explain-change.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-05-09-skill-token-cost-optimization docs/plans/2026-05-09-skill-token-cost-optimization.md docs/plan.md`
- 2026-05-10: Artifact lifecycle validation during M4 emitted the existing `docs/plan.md` lifecycle-language warning at line 19.
- 2026-05-10: M5 final validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-skill-token-cost-optimization`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/workflows.md --path templates/shared/evidence-collection-efficiency.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml --path docs/changes/2026-05-09-skill-token-cost-optimization/explain-change.md --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode explicit --path specs/skill-token-cost-optimization.md --path specs/skill-token-cost-optimization.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path templates/shared/evidence-collection-efficiency.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path skills/learn/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-09-skill-token-cost-optimization.md --path docs/plan.md --path docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `git diff --check -- .`
- 2026-05-10: Artifact lifecycle validation during M5 emitted the existing `docs/plan.md` lifecycle-language warning at line 19 and `docs/workflows.md` lifecycle-language warning at line 195.

## Outcome and Retrospective

- Pending final lifecycle closeout.
- Keep this section final-only or explicitly historical while the plan is active; do not duplicate the current next stage here.

## Readiness

- See `Current Handoff Summary`.
- Ready for `pr`.
- Implementation readiness: M1-M4 are closed and M5 final validation passed. The remaining lifecycle action is PR handoff.

## Risks and Follow-Ups

- none yet
