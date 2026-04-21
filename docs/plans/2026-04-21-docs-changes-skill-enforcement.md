# Docs changes skill enforcement plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-21
- Last updated: 2026-04-21
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved follow-up that aligns the canonical workflow skills with the docs-changes contract already established by the stacked docs-changes policy feature.

This initiative should make the operator-facing skill layer stop treating the baseline change-local pack as optional for ordinary non-trivial work:

- `workflow` should classify ordinary non-trivial work as carrying the baseline pack;
- `implement` should create or update that baseline pack;
- `verify` and `pr` should block when the required baseline pack is missing;
- `explain-change` should align with the default change-local durable reasoning surface for new work;
- generated `.codex/skills/` output should stay synchronized.

The implementation must stay inside the approved narrow boundary:

- no `change.yaml` schema redesign;
- no change to the baseline-versus-conditional docs-changes contract itself;
- no broad validator redesign in this slice;
- no fast-lane broadening;
- no historical backfill of old changes.

## Source artifacts

- Proposal: `docs/proposals/2026-04-21-docs-changes-skill-enforcement.md`
- Spec: `specs/docs-changes-skill-enforcement.md`
- Test spec: `specs/docs-changes-skill-enforcement.test.md`
- Spec-review findings carried into this plan:
  - no architecture artifact is required for this small skill-alignment slice;
  - the feature should stay focused on `workflow`, `implement`, `verify`, `explain-change`, and `pr`;
  - validator-side missing-pack enforcement remains a possible later feature, not part of this plan's required scope.
- Related governing artifacts:
  - `specs/rigorloop-workflow.md`
  - `specs/docs-changes-usage-policy.md`
  - `specs/docs-changes-usage-policy.test.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `.codex/skills/`

## Context and orientation

- The approved docs-changes policy already requires the baseline change-local pack for ordinary non-trivial work.
- The observed gap is in stage-local execution guidance, not in the top-level contract.
- The current skills do not consistently operationalize the required baseline pack:
  - `workflow` does not make it an ordinary non-trivial expectation;
  - `implement` does not tell the agent to create/update it;
  - `verify` uses the pack when present but does not yet clearly block on missing required pack artifacts;
  - `pr` does not name the baseline pack as an explicit readiness check;
  - `explain-change` does not yet align its durable-output guidance with the default change-local reasoning surface.
- Existing relied-on test specs already cover part of the behavior this feature will change:
  - `specs/docs-changes-usage-policy.test.md` already covers fast-lane omission, required `change.yaml`, and the default durable reasoning surface;
  - `specs/workflow-stage-autoprogression.test.md` already covers direct-`pr`, readiness blockers, and isolated-stage behavior.
- The future feature test spec must therefore add focused coverage for this follow-up without leaving those existing proof surfaces stale.
- Generated `.codex/skills/` output must be regenerated from canonical edits and must not be hand-edited.
- This initiative is stacked on the docs-changes usage-policy branch because the governing contract it depends on is not yet merged to `main`.

## Non-goals

- Redesign `schemas/change.schema.json`.
- Reopen the docs-changes baseline-versus-conditional contract.
- Add repository-wide validator inference for missing packs without a `change.yaml` file.
- Require docs-changes artifacts for approved fast-lane work.
- Expand the touched-skill set far beyond the small stage-local owners unless review reveals a real gap.

## Pre-implementation prerequisites

- Track the accepted proposal, approved spec, and this plan before `test-spec` or `implement` relies on them as authoritative repository state:
  - `docs/proposals/2026-04-21-docs-changes-skill-enforcement.md`
  - `specs/docs-changes-skill-enforcement.md`
  - `docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
- Create `specs/docs-changes-skill-enforcement.test.md` after `plan-review` and before implementation.
- Keep this follow-up stacked on the docs-changes policy branch until that base feature merges or is restacked cleanly.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R3b` | `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, matching `.codex/skills/` |
| `R4`-`R6a` | `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/explain-change/SKILL.md`, matching `.codex/skills/` |
| `R7` | generated-skill regeneration and drift proof |
| `R8`-`R9` | scope control in touched skills, related workflow wording review, and final validation |

## Milestones

### M1. Align workflow and implement guidance with the baseline docs-changes pack

- Goal:
  - Make the entrypoint and implementation skills explicitly require the baseline change-local pack for ordinary non-trivial work without broadening fast-lane scope.
- Requirements:
  - `R1`-`R3b`, `R9`
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `specs/docs-changes-usage-policy.test.md`
  - matching `.codex/skills/`
  - `docs/workflows.md` only if wording drift appears
- Dependencies:
  - approved spec
  - tracked-source prerequisite must be satisfied before downstream stages rely on this milestone
- Tests to add/update:
  - review and update `specs/docs-changes-usage-policy.test.md` where existing proof cases already cover:
    - fast-lane omission staying narrow;
    - required `change.yaml` for ordinary non-trivial work;
    - the default `docs/changes/<change-id>/explain-change.md` durable reasoning surface.
  - the future test spec should cover:
    - ordinary non-trivial work carries the baseline change-local pack in workflow and implement guidance;
    - fast-lane omission remains unchanged;
    - generated skill output stays synchronized;
    - cross-references to the updated docs-changes usage-policy test coverage where that existing test spec already owns the governing contract proof.
- Implementation steps:
  - update `skills/workflow/SKILL.md` to make the baseline pack part of ordinary non-trivial work guidance;
  - update `skills/implement/SKILL.md` to create or update `change.yaml` plus the default durable reasoning surface for ordinary non-trivial work;
  - review and update `specs/docs-changes-usage-policy.test.md` where the existing docs-changes proof surface would otherwise drift from the revised stage-local guidance;
  - regenerate `.codex/skills/`;
  - review `docs/workflows.md` for wording drift and adjust only if needed.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'docs/changes|change.yaml|explain-change|fast-lane' skills/workflow/SKILL.md skills/implement/SKILL.md .codex/skills`
  - `git diff --check -- skills/workflow/SKILL.md skills/implement/SKILL.md specs/docs-changes-usage-policy.test.md .codex/skills docs/workflows.md`
- Expected observable result:
  - the entrypoint and implementation skills now make the baseline change-local pack an explicit ordinary non-trivial work requirement without widening fast-lane behavior, and the existing docs-changes test spec remains aligned where it already owns that contract proof.
- Commit message: `M1: align docs-changes workflow guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - skill wording may copy too much contract detail and drift from the workflow spec;
  - fast-lane wording may be broadened accidentally.
- Rollback/recovery:
  - revert the canonical/generated skill edits together and return to the top-level workflow/spec guidance while reworking the narrower wording.

### M2. Align verify, explain-change, and PR readiness guidance

- Goal:
  - Make the downstream gate skills treat missing required baseline packs as blockers and align explanation output with the default change-local durable reasoning surface.
- Requirements:
  - `R4`-`R6a`, `R9`
- Files/components likely touched:
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - matching `.codex/skills/`
- Dependencies:
  - M1 should settle the baseline entrypoint/implementation wording first
- Tests to add/update:
  - review and update `specs/workflow-stage-autoprogression.test.md` where existing proof cases already cover:
    - direct `pr` behavior;
    - readiness blockers;
    - isolated-stage behavior.
  - the future test spec should cover:
    - `verify` treats missing required baseline packs as blockers;
    - `pr` names docs-changes pack presence in readiness checks;
    - `explain-change` aligns with the default change-local durable reasoning artifact for new ordinary non-trivial work;
    - cross-references to the updated workflow-stage autoprogression test coverage where that existing test spec already owns direct-`pr` and isolated-stage proof.
- Implementation steps:
  - update `skills/verify/SKILL.md` to block on missing required baseline packs for ordinary non-trivial work;
  - update `skills/pr/SKILL.md` to check required docs-changes artifacts in readiness;
  - update `skills/explain-change/SKILL.md` to align with the default change-local reasoning surface;
  - review and update `specs/workflow-stage-autoprogression.test.md` where the existing workflow-stage proof surface would otherwise drift from the revised stage-local blocker and readiness guidance;
  - regenerate `.codex/skills/`.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'docs/changes|change.yaml|explain-change|blocker|readiness' skills/verify/SKILL.md skills/explain-change/SKILL.md skills/pr/SKILL.md .codex/skills`
  - `git diff --check -- skills/verify/SKILL.md skills/explain-change/SKILL.md skills/pr/SKILL.md specs/workflow-stage-autoprogression.test.md .codex/skills`
- Expected observable result:
  - downstream stage-local skills now make missing required baseline packs visible as blockers and use the approved durable reasoning default consistently, while the existing workflow-stage autoprogression test spec remains aligned where it already owns direct-`pr` and isolated-stage proof.
- Commit message: `M2: enforce docs-changes skill gates`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - verify/pr wording may overpromise executable enforcement that the repository still lacks outside the skill layer;
  - explain-change wording may accidentally conflict with existing top-level explain artifact compatibility rules.
- Rollback/recovery:
  - revert the downstream skill changes and generated mirrors together while preserving the approved top-level docs-changes contract.

### M3. Finish proof and reconcile any related summary drift

- Goal:
  - Ensure the updated skills are internally coherent, generated output is synchronized, and no directly related workflow summary surface still teaches the old behavior.
- Requirements:
  - `R7`-`R9`
- Files/components likely touched:
  - `docs/workflows.md` only if drift remains after M1/M2
  - `specs/docs-changes-skill-enforcement.test.md`
  - `docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - `.codex/skills/`
- Dependencies:
  - M1 and M2 completed
- Tests to add/update:
  - the future test spec should cover:
    - manual contract review across touched skills and any touched workflow summary surfaces;
    - generated-skill synchronization proof;
    - repo-owned smoke validation continuing to pass.
- Implementation steps:
  - resolve any remaining wording drift in `docs/workflows.md` if needed;
  - run the full repo-owned skill validation and smoke proof set;
  - update the active plan with final implementation evidence.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`
  - `git diff --check -- skills .codex/skills docs/workflows.md docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
- Expected observable result:
  - canonical/generated skills stay synchronized, related summary wording is truthful, and repo-owned smoke validation remains green.
- Commit message: `M3: finish docs-changes skill alignment proof`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - related summary surfaces may still lag the touched skill wording;
  - generated output may drift if regeneration is skipped.
- Rollback/recovery:
  - revert the proof and summary-alignment changes together, or narrow the touched surface set if the implementation proves smaller than expected.

## Validation plan

- Planning change validation:
  - `rg -n "^# Docs changes skill enforcement plan$|^## (Purpose / big picture|Source artifacts|Context and orientation|Non-goals|Pre-implementation prerequisites|Requirements covered|Milestones|Validation plan|Risks and recovery|Dependencies|Progress|Decision log|Surprises and discoveries|Validation notes|Outcome and retrospective|Readiness)$|^### M[0-9]+\\." docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
- Per-milestone validation is listed inside each milestone and should be copied into the later test spec.
- Final initiative validation should run:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`
  - targeted manual review of the touched stage-local skills against the approved docs-changes contract.

## Risks and recovery

- Risk: the plan may accidentally broaden into validator or schema redesign work.
  - Recovery: keep M1-M3 skill-focused and challenge any attempt to infer missing packs repo-wide without a separate approved change.
- Risk: stacked-branch dependency may be forgotten during PR preparation.
  - Recovery: keep the dependency explicit in the plan and prepare the eventual review branch only after the base docs-changes policy change is merged or intentionally restacked.
- Risk: generated `.codex/skills/` drift may hide canonical skill mistakes.
  - Recovery: keep `build-skills.py --check` in every milestone and the final proof set.

## Dependencies

- The accepted proposal, approved spec, and this plan must be tracked before `test-spec` or `implement`.
- `plan-review` must approve the milestone split before implementation.
- `specs/docs-changes-skill-enforcement.test.md` must exist before `implement`.
- This follow-up remains logically dependent on the docs-changes usage-policy feature branch until that base change merges.

## Progress

- [x] 2026-04-21: proposal created for docs-changes skill enforcement.
- [x] 2026-04-21: proposal accepted and narrowed to the small stage-local skill alignment slice.
- [x] 2026-04-21: spec created and approved without requiring a separate architecture artifact.
- [x] 2026-04-21: plan created and indexed under `Active` in `docs/plan.md`.
- [x] 2026-04-21: test spec created and linked as the active proof-planning surface for implementation.
- [x] 2026-04-21: M1 completed. `workflow` and `implement` now make the baseline change-local pack explicit for ordinary non-trivial work, the existing docs-changes test spec stays aligned, and generated `.codex/skills/` output is synchronized.
- [x] 2026-04-21: M1 code-review and verify passed with no follow-up fixes, so the initiative is back in `implement` for M2.
- [x] 2026-04-21: M2 completed. `verify`, `pr`, and `explain-change` now surface docs-changes baseline-pack expectations explicitly, the existing workflow-stage test spec stays aligned, and this feature itself now carries a baseline change-local pack.

## Decision log

- 2026-04-21: no separate architecture artifact is required at this stage. Reason: the change is a small skill-guidance alignment, not a new subsystem or system-boundary redesign.
- 2026-04-21: split the work into entrypoint/implement guidance, downstream gate guidance, and final proof. Reason: the change spans several skills, but the slices are still reviewable if split by stage responsibility.
- 2026-04-21: use a dedicated feature test spec plus targeted updates to the existing docs-changes and workflow-stage test specs. Reason: those existing test specs already own part of the governing proof surface and must stay aligned instead of being silently replaced.
- 2026-04-21: leave `docs/workflows.md` unchanged in M1. Reason: the workflow summary already matched the approved docs-changes contract, so the stage-local fix belonged only in `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, and the existing docs-changes test spec.
- 2026-04-21: add a baseline `docs/changes/2026-04-21-docs-changes-skill-enforcement/` pack during M2. Reason: this feature is itself ordinary non-trivial work, so the branch should comply with the docs-changes contract it is teaching instead of relying only on stacked top-level planning artifacts.

## Surprises and discoveries

- 2026-04-21: this follow-up itself needed a baseline change-local pack. The earlier top-level proposal/spec/plan/test-spec stack was necessary but not sufficient under the approved docs-changes contract for new ordinary non-trivial work.

## Validation notes

- 2026-04-21: plan created after proposal and spec were normalized to settled state for downstream reliance.
- 2026-04-21: planning artifact validation passed.
  - `git diff --check -- docs/proposals/2026-04-21-docs-changes-skill-enforcement.md specs/docs-changes-skill-enforcement.md docs/plan.md docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-21-docs-changes-skill-enforcement.md --path specs/docs-changes-skill-enforcement.md --path docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - Result: passed.
- 2026-04-21: test spec created and the tracked-source prerequisite was satisfied for downstream implementation reliance.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-21-docs-changes-skill-enforcement.md --path specs/docs-changes-skill-enforcement.md --path docs/plans/2026-04-21-docs-changes-skill-enforcement.md --path specs/docs-changes-skill-enforcement.test.md`
  - `git diff --check --cached -- docs/plan.md docs/proposals/2026-04-21-docs-changes-skill-enforcement.md specs/docs-changes-skill-enforcement.md docs/plans/2026-04-21-docs-changes-skill-enforcement.md specs/docs-changes-skill-enforcement.test.md`
  - Result: passed.
- 2026-04-21: M1 updated the stage-local `workflow` and `implement` skills plus the existing docs-changes usage-policy test spec, then regenerated `.codex/skills/`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/docs-changes-usage-policy.test.md`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'docs/changes|change.yaml|explain-change|fast-lane' skills/workflow/SKILL.md skills/implement/SKILL.md .codex/skills`
  - `git diff --check -- skills/workflow/SKILL.md skills/implement/SKILL.md specs/docs-changes-usage-policy.test.md .codex/skills docs/workflows.md`
  - Result: passed. `docs/workflows.md` review found no wording drift, so no summary-surface edit was needed in this milestone.
- 2026-04-21: M1 independent code-review found no blocking, major, or minor issues, and the follow-on verification pass was clean.
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/docs-changes-usage-policy.test.md --path docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - `git diff --check c78c435..301e3ce -- skills/workflow/SKILL.md skills/implement/SKILL.md specs/docs-changes-usage-policy.test.md .codex/skills docs/workflows.md docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - Result: passed. No additional M1 fixup was required.
- 2026-04-21: M2 updated `verify`, `pr`, and `explain-change`, aligned the existing workflow-stage autoprogression test spec, added the feature's own baseline change-local pack, and regenerated `.codex/skills/`.
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-21-docs-changes-skill-enforcement/change.yaml`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-stage-autoprogression.test.md --path docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - `rg -n 'docs/changes|change.yaml|explain-change|blocker|readiness' skills/verify/SKILL.md skills/explain-change/SKILL.md skills/pr/SKILL.md .codex/skills`
  - `git diff --check -- skills/verify/SKILL.md skills/explain-change/SKILL.md skills/pr/SKILL.md specs/workflow-stage-autoprogression.test.md docs/changes/2026-04-21-docs-changes-skill-enforcement .codex/skills docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
  - Result: passed.

## Outcome and retrospective

- This initiative is active. Use this section for completion, blockage, supersession, or retrospective notes once the real lifecycle outcome is known.

## Readiness

- This plan is active.
- The proposal is accepted and the spec is approved.
- No separate architecture artifact is required unless later review broadens the change.
- `specs/docs-changes-skill-enforcement.test.md` now exists and is the active proof-planning surface.
- The tracked-source prerequisite is satisfied.
- M1 and M2 are implemented; M3 remains open.
- The next stage is `code-review` for the M2 slice.
