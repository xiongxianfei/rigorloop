# Simplify Architecture Skill Surfaces Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-09
- Last updated: 2026-05-09
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: standard
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow-governance Markdown, canonical skill text, generated local skill mirrors, public adapter package copies, test specifications, and review evidence. It does not add runtime services, persistence, network behavior, release packaging format, or deployed infrastructure.

## Purpose / Big Picture

Implement the accepted simplification direction for architecture and architecture-review skill surfaces.

The intended contract is:

```text
Proposal resolves uncertainty.
Architecture records accepted design.
ADR records durable decisions.
```

The implementation removes change-local architecture deltas from the normal architecture skill contract, makes architecture-review classify the review surface before applying checks, preserves C4 plus arc42 plus ADR as the architecture method, and refreshes generated skill and adapter output through the repository generators.

## Source Artifacts

- Proposal: [Simplify Architecture Skill Surfaces](../proposals/2026-05-09-simplify-architecture-skill-surfaces.md), accepted after proposal-review R2.
- Spec: [Architecture Package Method](../../specs/architecture-package-method.md), approved after spec-review R1.
- Architecture: [Canonical System Architecture](../architecture/system/architecture.md), reviewed by architecture-review R1.
- ADR: [ADR-20260509 Architecture Skill Surface Simplification](../adr/ADR-20260509-architecture-skill-surface-simplification.md), reviewed by architecture-review R1.
- Existing method ADR: [ADR-20260428 Architecture Package Method](../adr/ADR-20260428-architecture-package-method.md), remains accepted decision history.
- Test spec: [Architecture Package Method Test Spec](../../specs/architecture-package-method.test.md), revised for the 2026-05-09 simplification in M1.
- Change metadata: `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`.
- Review records: `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md` and `review-resolution.md` cover proposal-review R1/R2, spec-review R1, and architecture-review R1.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on project-map claims for runtime ownership, storage, service boundaries, or module topology. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, the accepted proposal, approved spec, reviewed architecture and ADR, current skill files, generator scripts, and existing validator patterns.

## Context and Orientation

- `specs/architecture-package-method.md` owns the normative architecture package method, including R32-R39, R56-R58, R61, R85-R86, R110, R119-R124, AC21, and AC22 for this simplification.
- `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` are canonical authored skill sources. They currently still contain normal change-local delta and merge-back wording that must be replaced.
- `.codex/skills/` is generated local Codex runtime output. It must be refreshed with `python scripts/build-skills.py`, not hand-edited.
- `dist/adapters/` is generated public adapter output. It must be refreshed with `python scripts/build-adapters.py`, not hand-edited.
- Published skill text must remain portable. Repository-maintainer mechanics such as generated mirror paths, adapter output paths, selector constraints, and drift-check commands belong in plans, specs, tests, docs, scripts, or change metadata rather than shipped skill instructions.
- `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` summarize governance. They should be changed only where current wording conflicts with the approved spec.
- Architecture-review R1 approved the canonical update and ADR with no material findings. It noted one minor non-blocking cleanup: the Building Block View row for `Change-local evidence` can stop saying "Temporary working architecture."

## Non-Goals

- Do not remove the canonical architecture package.
- Do not remove C4, arc42, or ADRs from the architecture method.
- Do not require ADRs for every small architecture edit.
- Do not use architecture-review to settle product direction.
- Do not create a new skill for this behavior.
- Do not hand-edit `.codex/skills/` or `dist/adapters/`.
- Do not normalize all historical architecture deltas or delete existing change-local architecture evidence.
- Do not mark this initiative done until implementation, code-review, required review-resolution, explain-change, verify, and PR handoff are complete.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R32`-`R34` | Test-spec, architecture skill, architecture-review skill, workflow guidance, and static/stale-wording checks remove change-local architecture deltas from the normal authoring path while preserving historical and exceptional evidence. |
| `R36`-`R39` | Architecture skill output and guidance choose no-impact rationale, direct canonical update, ADR, or proposal/spec blocker as the normal surfaces. |
| `R56`-`R58` | Canonical skill updates plus generated `.codex/skills/` and `dist/adapters/` refresh through existing generation scripts. |
| `R61`, `R85`-`R86` | Historical/exceptional change-local evidence remains non-canonical and diagram lifecycle remains inherited from its owning artifact. |
| `R108`-`R110` | Architecture skill stays concise and includes the new smallest-valid-surface output shape. |
| `R119`-`R124` | Architecture-review skill classifies review surface first and applies surface-specific checks without requiring a change-local delta. |
| `AC21` | Normal architecture authoring no longer includes change-local deltas. |
| `AC22` | Architecture-review classification and no-delta review behavior are test-spec covered and skill implemented. |

## Current Handoff Summary

- Current milestone: M3. Architecture-Review Surface Classification and Guidance Alignment
- Current milestone state: review-requested
- Last reviewed milestone: M2
- Review status: M3 implementation handoff is ready for code-review; M2 is closed.
- Remaining in-scope implementation milestones: M3, M4
- Next stage: code-review M3
- Final closeout readiness: not ready
- Reason final closeout is not ready: M3 code-review, M4 implementation, code-review for each implementation milestone, review-resolution when triggered, explain-change, verify, and PR handoff remain.

## Milestones

### M1. Test Spec and Source Lifecycle Alignment

- Milestone state: closed
- Goal: Revise the architecture package method test spec for the simplification and normalize reviewed source artifacts before implementation relies on them.
- Requirements: `R32`-`R39`, `R56`-`R58`, `R61`, `R85`-`R86`, `R110`, `R119`-`R124`, `AC21`, `AC22`.
- Files/components likely touched:
  - `specs/architecture-package-method.test.md`
  - `docs/architecture/system/architecture.md`
  - `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
- Dependencies:
  - Plan-review approval.
  - Architecture-review R1 approval remains valid.
- Tests to add/update:
  - Add coverage for normal architecture surfaces: no-impact rationale, canonical update, ADR, and blocked proposal/spec routing.
  - Add coverage that normal authoring does not require or recommend change-local architecture deltas.
  - Add coverage that existing deltas remain historical evidence and new deltas are legacy-closeout or explicit exceptional evidence only.
  - Add coverage that architecture-review classifies `canonical-architecture-update`, `ADR`, `no-architecture-impact-rationale`, or `proposal-or-spec-gap` before applying checks.
  - Add explicit adapter drift check plus adapter validation expectations for published skill changes.
- Implementation steps:
  - Update the test spec coverage maps and affected test cases to cite the 2026-05-09 requirements and acceptance criteria.
  - Replace stale normal-delta and merge-back expectations in test cases with historical/exceptional evidence expectations.
  - Normalize the reviewed architecture document and ADR status if still in draft state.
  - Clean up the minor architecture-review note about "Temporary working architecture" if it remains in the canonical package.
  - Keep change metadata and plan progress current.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260509-architecture-skill-surface-simplification.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/plan.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260509-architecture-skill-surface-simplification.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/plan.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `rg -n 'normal .*change-local architecture delta|directing authors to a change-local delta|change-local merge-back|merge-back behavior is explicit|produces a delta' specs/architecture-package-method.test.md docs/architecture/system/architecture.md`
  - `git diff --check -- specs/architecture-package-method.test.md docs/architecture/system/architecture.md docs/adr/ADR-20260509-architecture-skill-surface-simplification.md docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/plan.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
- Expected observable result: The test spec operationalizes the approved simplification, reviewed architecture sources are lifecycle-current, and stale normal-delta proof wording is removed from the active test plan.
- Implementation result:
  - `specs/architecture-package-method.test.md` covers the 2026-05-09 simplification requirements and proof surfaces.
  - `docs/architecture/system/architecture.md` is normalized to `approved`.
  - `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md` is normalized to `accepted`.
  - The `Change-local evidence` Building Block row now describes historical and exceptional evidence instead of temporary working architecture.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M1
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M2
- Commit message: `M1: align architecture surface test spec`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Rewriting old historical tests too broadly could erase proof for legacy architecture-delta evidence.
  - Normalizing lifecycle state before review evidence exists would overclaim readiness.
- Rollback/recovery:
  - Revert only the test-spec and lifecycle edits for this initiative and keep the plan active with the blocker named.

### M2. Canonical Architecture Skill Contract

- Milestone state: closed
- Goal: Update `architecture` to choose the smallest valid architecture surface and remove change-local deltas from the normal skill contract.
- Requirements: `R32`-`R39`, `R56`, `R108`-`R110`, `AC21`.
- Files/components likely touched:
  - `skills/architecture/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
- Dependencies:
  - M1 test-spec alignment.
- Tests to add/update:
  - Static checks that architecture skill output includes no-impact rationale, canonical update, ADR, and blocked proposal/spec routing.
  - Static checks that architecture skill text does not present change-local architecture deltas as a normal output.
  - Static checks that public skill text uses portable canonical architecture wording rather than RigorLoop-only universal path requirements.
- Implementation steps:
  - Replace the output shape with the architecture surface decision model.
  - Remove normal change-local delta authoring and merge-back instructions from the skill contract.
  - Keep C4, arc42, ADR triggers, minimal snippets, evidence-efficiency guidance, and full-file-read guidance.
  - Keep repository-maintainer validation and generator mechanics out of shipped skill text.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `rg -n 'change-local architecture delta|merge-back|working architecture lives|docs/changes/<change-id>/architecture.md' skills/architecture/SKILL.md`
  - `git diff --check -- skills/architecture/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
- Expected observable result: The canonical architecture skill no longer requires or recommends a change-local architecture delta in the normal authoring path.
- Implementation result:
  - `skills/architecture/SKILL.md` now starts architecture authoring from the smallest valid architecture surface: no-impact rationale, blocked proposal/spec routing, direct canonical architecture update, or ADR.
  - The normal change-local architecture delta output and merge-back wording were removed from the canonical architecture skill contract.
  - The skill keeps portable canonical architecture wording and preserves arc42, C4 snippets, ADR triggers, evidence-efficiency guidance, and full-file-read guidance.
  - `scripts/test-skill-validator.py` now asserts the simplified architecture skill surface and stale normal-delta exclusions.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M2
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M3
- Commit message: `M2: simplify architecture skill surfaces`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Removing too much guidance could make C4, arc42, and ADR expectations unclear.
  - Leaving maintainer-only generator commands in shipped skill text would violate public skill portability.
- Rollback/recovery:
  - Restore the prior skill text only for the affected sections and keep the approved spec as the blocker until a compliant rewrite is ready.

### M3. Architecture-Review Surface Classification and Guidance Alignment

- Milestone state: review-requested
- Goal: Update architecture-review and affected contributor guidance so review starts with surface classification and does not require a change-local delta for canonical updates.
- Requirements: `R57`, `R119`-`R124`, `AC22`.
- Files/components likely touched:
  - `skills/architecture-review/SKILL.md`
  - `docs/workflows.md`
  - `AGENTS.md`, only if direct wording conflicts with the approved spec
  - `CONSTITUTION.md`, only if direct wording conflicts with the approved spec
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`, only if finding-shape or review-surface validation needs adjustment
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
- Dependencies:
  - M2 canonical architecture skill rewrite.
- Tests to add/update:
  - Static checks that architecture-review names `canonical-architecture-update`, `ADR`, `no-architecture-impact-rationale`, and `proposal-or-spec-gap`.
  - Static checks that architecture-review does not require a change-local architecture delta for canonical architecture updates.
  - Existing review finding format tests remain intact: finding, location, severity, recommendation, plus repository-wide material-finding fields when material.
- Implementation steps:
  - Add review-surface classification as the first review step.
  - Add surface-specific checks for canonical updates, ADRs, no-impact rationale, and proposal/spec gaps.
  - Remove old normal delta and merge-back checklist language from architecture-review.
  - Update workflow or governance summaries only where they directly conflict; otherwise record them as unaffected in plan progress.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture-review/SKILL.md --path docs/workflows.md --path AGENTS.md --path CONSTITUTION.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `rg -n 'merge-back|docs/changes/<change-id>/architecture.md|must not compete with the canonical package' skills/architecture-review/SKILL.md docs/workflows.md AGENTS.md CONSTITUTION.md`
  - `git diff --check -- skills/architecture-review/SKILL.md docs/workflows.md AGENTS.md CONSTITUTION.md scripts/test-skill-validator.py scripts/test-review-artifact-validator.py docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
- Expected observable result: Architecture-review applies checks to the classified review surface and routes unresolved direction or behavior back to proposal or spec.
- Implementation result:
  - `skills/architecture-review/SKILL.md` now classifies review surfaces before applying checks.
  - Canonical architecture updates, ADRs, no-impact rationales, and proposal/spec gaps have surface-specific review guidance.
  - The skill keeps C4, arc42, ADR completeness, quality, and material-finding safeguards.
  - `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` are unaffected with rationale: they do not contain the stale normal-delta or merge-back checklist wording targeted by M3, and their architecture-review references remain stage-level guidance.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M3
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting M4
- Commit message: `M3: classify architecture review surfaces`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Review guidance could become too thin and lose C4 or arc42 quality checks.
  - Updating governance summaries unnecessarily could create broad review churn.
- Rollback/recovery:
  - Revert only the affected review-skill and guidance edits and reopen the milestone with a narrower rewrite.

### M4. Generated Output, Adapter Validation, and Lifecycle Closeout Preparation

- Milestone state: planned
- Goal: Refresh generated local skills and public adapters, prove drift is closed, and prepare the change for downstream code-review and final lifecycle gates.
- Requirements: `R58`, `AC20`, plus the proposal's adapter drift check and adapter validation requirement.
- Files/components likely touched:
  - `.codex/skills/architecture/SKILL.md`
  - `.codex/skills/architecture-review/SKILL.md`
  - generated architecture and architecture-review skill copies under `dist/adapters/`
  - adapter manifests under `dist/adapters/`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
- Dependencies:
  - M2 and M3 canonical skill source changes.
- Tests to add/update:
  - Generated-output drift checks for `.codex/skills/`.
  - Adapter drift check and adapter validation.
  - Adapter distribution tests if generated adapter output changes.
  - Selected validation for concrete generated output paths; do not pass broad generated directories as generic lifecycle paths.
- Implementation steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py`.
  - Run generated skill drift check.
  - Run adapter drift check and adapter validation. The normal commands are:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py --version 0.1.1
```

  - Record validation evidence in the plan and change metadata.
  - Hand off to code-review after implementation milestones and targeted validation are complete.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path .codex/skills/architecture/SKILL.md --path .codex/skills/architecture-review/SKILL.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/plan.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path scripts/test-adapter-distribution.py --path specs/architecture-package-method.test.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/plan.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `git diff --check -- skills/architecture/SKILL.md skills/architecture-review/SKILL.md .codex/skills/architecture/SKILL.md .codex/skills/architecture-review/SKILL.md dist/adapters specs/architecture-package-method.test.md docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/plan.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
- Expected observable result: Generated local skill mirrors and public adapter packages match canonical skill sources, adapter validation passes, and the implementation is ready for code-review.
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for M4
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before entering M5 lifecycle closeout
- Commit message: `M4: refresh architecture skill adapters`
- Milestone closeout:
  - targeted validation passed
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Running generators after stale canonical skill text would faithfully propagate wrong guidance.
  - Adapter validation requires the repository's current versioned form for `validate-adapters.py`.
- Rollback/recovery:
  - Re-run generators from the last accepted canonical skill sources or revert generated output together with the corresponding source edits.

### M5. Lifecycle Closeout

- Milestone state: planned
- Goal: Complete downstream gates after implementation milestones are closed.
- Requirements: repository workflow closeout, review, rationale, verification, and PR-readiness rules.
- Files/components likely touched:
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md`, when triggered
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/explain-change.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - `docs/plan.md`
- Dependencies:
  - M1 through M4 are closed.
  - M1 through M4 have each completed their milestone code-review loop.
  - Material findings from M1 through M4 code-review are resolved or explicitly dispositioned.
  - Review closeout for M1 through M4 is recorded before M5 starts.
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
  - Commands selected by `code-review`, `explain-change`, and `verify` based on the final diff.
  - At minimum, rerun the M4 generated-output, adapter, lifecycle, selected-validation, and diff checks after all fixes.
- Expected observable result: Final lifecycle closeout starts only after M1-M4 have each passed their milestone review loop; the change has current rationale and verification evidence, plan/index lifecycle state is synchronized, and PR handoff can truthfully describe readiness.
- Commit message: `M5: close architecture surface simplification`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Marking the plan done before final verify or PR handoff would conflict with repository lifecycle rules.
  - A code-review finding could require returning to M1-M4 instead of closing out.
- Rollback/recovery:
  - Keep the plan active and record the blocker, finding, or failed validation until corrected.

## Validation Plan

- Use the smallest relevant validation scope for each milestone first.
- Run `python scripts/validate-change-metadata.py` whenever `change.yaml` changes.
- Run artifact lifecycle validation for touched proposal/spec/test-spec/architecture/ADR/plan/change metadata surfaces.
- Run `python scripts/validate-skills.py` and `python scripts/test-skill-validator.py` for canonical skill text changes.
- Run `python scripts/build-skills.py --check` after local generated skill mirrors are refreshed.
- Run both adapter drift check and adapter validation for public adapter output:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py --version 0.1.1
```

- Run `python scripts/test-adapter-distribution.py` when adapter output or adapter validation behavior is in scope.
- Run `bash scripts/ci.sh --mode explicit ...` over the touched authoritative and proof surfaces before implementation handoff to code-review.
- Run final `verify` after durable explain-change evidence exists.

## Risks and Recovery

- Risk: stale normal-delta wording remains in the test spec or skills. Recovery: keep implementation milestone open, use targeted `rg` checks, and revise only the conflicting surface.
- Risk: public skill text leaks repository-maintainer mechanics. Recovery: move generator, adapter, selector, and drift-check details to plan/test/governance surfaces and keep shipped skill wording project-portable.
- Risk: generated output drifts from canonical skill sources. Recovery: rerun `python scripts/build-skills.py` and `python scripts/build-adapters.py`, then rerun drift and validation commands.
- Risk: architecture-review surface classification weakens architecture quality review. Recovery: preserve C4, arc42, ADR completeness, material-finding, and quality checks under the surface-specific review model.
- Risk: lifecycle status gets out of sync between `docs/plan.md` and this plan body. Recovery: treat verify as blocking until both surfaces are updated together.

## Dependencies

- Plan-review must approve this revised plan before implementation milestones proceed.
- The test-spec revision must be ready before implementation changes rely on it.
- Each in-scope implementation milestone M1-M4 must complete targeted validation, code-review, and required finding resolution before the next implementation milestone starts.
- M2 and M3 canonical skill edits must precede generated output refresh in M4.
- Generated outputs must be produced by repository scripts, not hand-edited.
- M5 final lifecycle closeout begins only after M1-M4 review loops are closed. Explain-change, verify, and PR handoff remain downstream of reviewed implementation milestones.

## Progress

- [x] 2026-05-09: Proposal accepted after proposal-review R2.
- [x] 2026-05-09: Spec amendment approved after spec-review R1.
- [x] 2026-05-09: Canonical architecture update and new ADR approved by architecture-review R1.
- [x] 2026-05-09: Plan created and indexed.
- [x] 2026-05-09: Plan revised to resolve PR-F1 by adding per-milestone code-review handoff and review closeout.
- [x] Plan-review complete.
- [x] Test-spec revised.
- [x] M1 implementation complete and handed to code-review.
- [x] M1 CR1-F1 and CR2-F1 resolved and returned to code-review.
- [x] M1 CR4-F1 resolved and returned to code-review.
- [x] M1 CR5-F1 dispositioned and returned to code-review.
- [x] M1 closed after clean code-review.
- [x] M2 implementation complete and handed to code-review.
- [x] M2 closed after clean code-review.
- [x] M3 implementation complete and handed to code-review.
- [ ] M3 closed.
- [ ] M4 closed.
- [ ] M5 closed.

## Decision Log

- 2026-05-09: Use one active plan for the remaining implementation work rather than separate plans for test-spec, skills, generated output, and closeout. This keeps the compatibility-sensitive skill and adapter refresh sequence reviewable in one lifecycle thread.
- 2026-05-09: Keep adapter validation in versioned form for this repository: `python scripts/validate-adapters.py --version 0.1.1`. The proposal's unversioned command is the normal principle, while the current repository script requires `--version`.
- 2026-05-09: Treat `AGENTS.md` and `CONSTITUTION.md` as conditional touches. They are updated only if implementation inspection finds direct conflict; otherwise the plan records them as unaffected to avoid unnecessary governance churn.

## Surprises and Discoveries

- `docs/project-map.md` is absent; the no-map rationale is recorded in Source Artifacts.
- `python scripts/validate-adapters.py` requires `--version`; this plan uses `--version 0.1.1`.

## Validation Notes

- Plan creation validation is recorded in `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`.
- Test-spec revision validation is recorded in `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`.
- M1 targeted validation passed on 2026-05-09:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260509-architecture-skill-surface-simplification.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/plan.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml` passed with the existing unrelated lifecycle warning in `docs/plan.md` line 17.
  - `python scripts/select-validation.py --mode explicit --path specs/architecture-package-method.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260509-architecture-skill-surface-simplification.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/plan.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `rg -n 'normal .*change-local architecture delta|directing authors to a change-local delta|change-local merge-back|merge-back behavior is explicit|produces a delta' specs/architecture-package-method.test.md docs/architecture/system/architecture.md` returned no matches.
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- specs/architecture-package-method.test.md docs/architecture/system/architecture.md docs/adr/ADR-20260509-architecture-skill-surface-simplification.md docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/plan.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
  - `rg -n '[[:blank:]]$|\t' specs/architecture-package-method.test.md docs/architecture/system/architecture.md docs/adr/ADR-20260509-architecture-skill-surface-simplification.md docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml` returned no matches.
- M1 review-resolution closeout validation passed on 2026-05-09:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md`
  - `rg -n '[[:blank:]]$|\t' docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md` returned no matches.
- M1 CR4-F1 review-resolution validation passed on 2026-05-09:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md`
  - `rg -n '[[:blank:]]$|\t' docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md` returned no matches.
- M2 targeted validation passed on 2026-05-09:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `rg -n 'change-local architecture delta|merge-back|working architecture lives|docs/changes/<change-id>/architecture.md' skills/architecture/SKILL.md` returned no matches.
  - `git diff --check -- skills/architecture/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path skills/architecture/SKILL.md`
  - `python scripts/test-change-metadata-validator.py`
  - `rg -n '[[:blank:]]$|\t' skills/architecture/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml` returned no matches.
- M2 code-review R7 validation passed on 2026-05-09:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path skills/architecture/SKILL.md`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `rg -n 'change-local architecture delta|merge-back|working architecture lives|docs/changes/<change-id>/architecture.md' skills/architecture/SKILL.md` returned no matches.
  - `git diff --check -- skills/architecture/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/code-review-r7.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path skills/architecture/SKILL.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/code-review-r7.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path skills/architecture/SKILL.md`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- docs/changes/2026-05-09-simplify-architecture-skill-surfaces docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md skills/architecture/SKILL.md scripts/test-skill-validator.py`
  - `rg -n '[[:blank:]]$|\t' docs/changes/2026-05-09-simplify-architecture-skill-surfaces docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md skills/architecture/SKILL.md scripts/test-skill-validator.py` returned no matches.
- M3 targeted validation passed on 2026-05-09:
  - `python -m unittest scripts.test-skill-validator.SkillValidatorFixtureTests.test_architecture_review_skill_preserves_simple_finding_and_material_contract` failed before the architecture-review rewrite and passed after it.
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/select-validation.py --mode explicit --path skills/architecture-review/SKILL.md --path docs/workflows.md --path AGENTS.md --path CONSTITUTION.md --path scripts/test-skill-validator.py --path scripts/test-review-artifact-validator.py --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
  - `rg -n 'merge-back|docs/changes/<change-id>/architecture.md|must not compete with the canonical package' skills/architecture-review/SKILL.md docs/workflows.md AGENTS.md CONSTITUTION.md` returned no matches.
  - `git diff --check -- skills/architecture-review/SKILL.md docs/workflows.md AGENTS.md CONSTITUTION.md scripts/test-skill-validator.py scripts/test-review-artifact-validator.py docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path AGENTS.md --path CONSTITUTION.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/workflows.md --path skills/architecture-review/SKILL.md` passed with the existing unrelated lifecycle warning in `docs/workflows.md` line 189.
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-select-validation.py`
  - `rg -n '[[:blank:]]$|\t' skills/architecture-review/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml` returned no matches.

## Outcome and Retrospective

This plan is active. M1 is in review-resolution after code-review R1 and R2, not implementation completion, final closeout, or PR readiness.
CR1-F1 and CR2-F1 are resolved for re-review, and M1 is back in `review-requested`.
Code-review R4 requested CR4-F1, so M1 is back in review-resolution.
CR4-F1 is resolved for re-review, and M1 is back in `review-requested`.
CR5-F1 is rejected by owner decision because the lifecycle review finding is not accepted for this plan implementation review; M1 is back in `review-requested`.
Code-review R6 completed cleanly, so M1 is closed and the next stage is M2 implementation.
M2 implementation updated the canonical architecture skill contract and matching validator coverage; M2 is now in `review-requested`.
Code-review R7 completed cleanly, so M2 is closed and the next stage is M3 implementation.
M3 implementation updated architecture-review surface classification and matching validator coverage; M3 is now in `review-requested`.

## Readiness

- Next stage: code-review M3
- Test-spec readiness: complete for the 2026-05-09 simplification.
- Implementation readiness: M3 targeted validation passed and the milestone is ready for code-review. M4 must not start until M3 completes its milestone review loop.
- Final closeout readiness: not ready until all in-scope implementation milestones are closed and downstream review, rationale, verify, and PR gates are complete.

## Risks and Follow-Ups

- Follow-up: create or update `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/explain-change.md` after implementation and before final verify.
- Follow-up: update `docs/plan.md` and this plan body together when the initiative changes lifecycle state.
