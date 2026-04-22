# Test-spec readiness and skill workflow alignment plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-22
- Last updated: 2026-04-22
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved workflow-facing distinction between:

- the immediate next repository stage; and
- downstream readiness for later stages such as `test-spec`.

This initiative should make the repository's workflow guidance and directly affected skills say the same thing:

- `spec-review` reports a repository-stage next step plus eventual `test-spec` readiness;
- approved `spec-review` never pairs with `not-ready` or `not-assessed`;
- missing reviewer inputs and blocker conditions stay stop conditions rather than pseudo-stages;
- `test-spec` preserves approved spec, spec-review findings, concrete plan, and relevant architecture/ADR context as prerequisites; and
- the enduring invariant lands in `specs/rigorloop-workflow.md` while the focused spec remains the change-scoped review contract.

The implementation must stay inside the approved first slice:

- no stage-order redesign;
- no broadened review-to-next-authoring autoprogression;
- no pseudo-routing states in immediate-next-stage fields;
- no wording-pattern validator in v1; and
- no separate architecture artifact unless implementation expands beyond workflow guidance and skill alignment.

## Source artifacts

- Proposal: `docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- Spec: `specs/test-spec-readiness-and-skill-workflow-alignment.md`
- Spec-review findings carried into this plan:
  - restore architecture / ADR context as a preserved `test-spec` prerequisite;
  - ban pseudo-routing states from the immediate-next-stage field;
  - treat missing context and blockers as stop conditions, not stages;
  - define exact negative output shapes for `not-ready` and `not-assessed`;
  - make approved `spec-review` incompatible with `not-ready` or `not-assessed`.
- Architecture: none. The approved spec says no separate architecture artifact is expected for this slice.
- Architecture-review findings: none.
- Test spec: `specs/test-spec-readiness-and-skill-workflow-alignment.test.md` is now active and owns the focused proof surface for this initiative.
- Related workflow and proof surfaces:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/spec-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan-review/SKILL.md` only if its current wording actually conflicts with the approved contract
  - generated `.codex/skills/`

## Context and orientation

- This is workflow-governance work, not runtime product behavior, but it is compatibility-sensitive because it changes contributor-visible workflow wording and the durable workflow spec.
- The focused approved spec is the change vehicle. Implementation must also fold the enduring invariant into `specs/rigorloop-workflow.md` without creating a second long-term normative home.
- The main authored surfaces likely to change are:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/spec-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan-review/SKILL.md` only if its current wording conflicts with the approved contract
  - `AGENTS.md` if the approved change materially affects the practical workflow summary for agents
  - `CONSTITUTION.md` only if implementation reveals a governance- or principle-level change rather than lower-level workflow guidance
  - `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
  - `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/explain-change.md`
  - generated `.codex/skills/`
- Generated `.codex/skills/` output remains derived. Regenerate it; do not hand-edit it.
- The repository currently has no `docs/project-map.md`. The change is narrow enough that a project map is not required for planning.
- `specs/rigorloop-workflow.test.md` is archived. This initiative should create a focused new test spec rather than reviving the archived workflow test artifact unless a later approved change deliberately reopens broader proof ownership.
- This is ordinary non-trivial work. Implementation must carry the baseline change-local pack:
  - `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
  - `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/explain-change.md`

## Non-goals

- Redesigning the repository stage order.
- Broadening review-to-next-authoring autoprogression.
- Rewriting every review-stage skill in one pass.
- Adding validator enforcement for wording patterns in the same v1 slice.
- Creating a second readiness registry separate from the workflow contract and workflow-facing skills.
- Introducing a new orchestration subsystem, persistent workflow state store, or runtime router.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R3k`, observability section, acceptance criteria | `skills/spec-review/SKILL.md`, `skills/workflow/SKILL.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, generated `.codex/skills/` |
| `R4`-`R5b`, state/invariants, edge cases | `skills/workflow/SKILL.md`, `skills/plan-review/SKILL.md` only if needed, `docs/workflows.md`, `specs/rigorloop-workflow.md`, generated `.codex/skills/` |
| `R6`-`R6b`, error/boundary behavior, compatibility/migration | `skills/test-spec/SKILL.md`, `skills/spec-review/SKILL.md`, `specs/rigorloop-workflow.md`, generated `.codex/skills/` |
| `R7`-`R8a`, v1 scope control, change-local durability, and workflow summary alignment | `skills/spec-review/SKILL.md`, `skills/test-spec/SKILL.md`, `skills/workflow/SKILL.md`, `docs/workflows.md`, `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/`, generated `.codex/skills/` |

## Milestones

### M1. Implement immediate-next-stage versus downstream-readiness alignment

- Goal:
  - Align the durable workflow spec, short workflow summary, directly affected workflow-facing skills, and generated output with the approved readiness/output matrix without broadening stage order or autoprogression scope.
- Requirements:
  - `R1`-`R8a`
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/spec-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan-review/SKILL.md` only if wording drift is actually present
  - `AGENTS.md` if the guidance-impact check shows practical agent workflow guidance changed
  - `CONSTITUTION.md` only if the same check shows a governance or principle change rather than lower-level workflow guidance
  - `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
  - `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/explain-change.md`
  - generated `.codex/skills/`
- Dependencies:
  - accepted proposal
  - approved focused spec
  - `plan-review`
  - active focused test spec created after `plan-review`
- Tests to add/update:
  - use the active `specs/test-spec-readiness-and-skill-workflow-alignment.test.md` as the focused proof surface for M1
  - require the focused test spec to prove `spec-review` reports immediate next repository stage separately from eventual `test-spec` readiness
  - require the focused test spec to prove `approved` is incompatible with `not-ready` and `not-assessed`
  - require the focused test spec to prove `inconclusive` produces no immediate-next-stage value and records the missing-input stop condition
  - require the focused test spec to prove `plan-review` preserves `test-spec` as the immediate next handoff when its wording is in scope
  - require the focused test spec to prove `test-spec` preserves approved spec, spec-review findings, concrete plan, and relevant architecture or ADR inputs when needed
  - require the focused test spec to prove the touched workflow-facing skill surfaces, workflow summary, durable workflow spec, and generated `.codex/skills/` output stay aligned
  - do not revive archived `specs/rigorloop-workflow.test.md` for this slice unless later review explicitly reopens broader workflow proof ownership
  - update any currently active broader proof surface only if implementation shows genuine overlap that would otherwise drift
- Implementation steps:
  - update `specs/rigorloop-workflow.md` to record the enduring invariant:
    - immediate next repository stage versus downstream readiness are distinct;
    - immediate-next-stage values use repository stages only;
    - `approved`, `changes-requested`, `blocked`, and `inconclusive` map to the approved immediate-next-stage and eventual-readiness matrix;
    - missing input and blocker conditions remain stop conditions rather than pseudo-stages;
    - approved `spec-review` is incompatible with `not-ready` or `not-assessed`;
  - update `skills/spec-review/SKILL.md` so its closing contract uses the approved review outcomes, immediate-next-stage field, eventual readiness field, and exact negative output shapes;
  - update `skills/test-spec/SKILL.md` so it preserves approved spec, spec-review findings, concrete plan, and relevant architecture or ADR context as prerequisites and rejects upstream `not-ready` / `not-assessed` states;
  - update `skills/workflow/SKILL.md` and `docs/workflows.md` only where the shared workflow summary must mention the distinction, preserved stage order, and stop-condition behavior to avoid stale contributor guidance;
  - inspect `skills/plan-review/SKILL.md` and update it only if its existing wording obscures `test-spec` as the immediate next stage or treats downstream implementation readiness as the handoff itself;
  - explicitly assess whether the approved contract affects `AGENTS.md` or `CONSTITUTION.md`;
  - if `AGENTS.md` is affected because practical workflow guidance changed, update it in this milestone;
  - if `CONSTITUTION.md` is affected because the change rises to a governance or principle change, update it in this milestone;
  - if neither file is affected, record that no-change decision in the plan validation notes instead of leaving the omission implicit;
  - create the baseline change-local pack for this initiative;
  - regenerate `.codex/skills/` after canonical skill changes.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/rigorloop-workflow.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `rg -n 'immediate next repository stage|downstream readiness|eventual `?test-spec`? readiness|ready|conditionally-ready|not-ready|not-assessed|approved|changes-requested|blocked|inconclusive|stop condition' skills/spec-review/SKILL.md skills/test-spec/SKILL.md skills/workflow/SKILL.md skills/plan-review/SKILL.md docs/workflows.md specs/test-spec-readiness-and-skill-workflow-alignment.md specs/rigorloop-workflow.md .codex/skills`
  - `rg -n 'spec-review|test-spec|plan-review|architecture|workflow' AGENTS.md CONSTITUTION.md docs/workflows.md specs/rigorloop-workflow.md`
  - `git diff --check -- specs/test-spec-readiness-and-skill-workflow-alignment.test.md specs/test-spec-readiness-and-skill-workflow-alignment.md specs/rigorloop-workflow.md skills/spec-review/SKILL.md skills/test-spec/SKILL.md skills/workflow/SKILL.md skills/plan-review/SKILL.md docs/workflows.md docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md docs/plan.md`
  - `bash scripts/ci.sh`
- Expected observable result:
  - the durable workflow spec, workflow summary, and directly affected workflow-facing skills all use the same approved matrix for immediate next stage, eventual `test-spec` readiness, negative output shapes, stop conditions, and preserved prerequisites.
- Commit message: `M1: implement test-spec readiness alignment`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - `specs/rigorloop-workflow.md` and the focused spec may drift if the implementation duplicates wording instead of folding the invariant cleanly;
  - `skills/plan-review/SKILL.md` may be changed unnecessarily even if no real defect exists there;
  - `AGENTS.md` or `CONSTITUTION.md` may be over-edited when no practical/principled guidance change actually occurred;
  - the absence of a v1 validator means wording drift must be caught through the focused test spec and review surfaces.
- Rollback/recovery:
  - revert canonical and generated workflow-facing skill changes together;
  - revert `specs/rigorloop-workflow.md` together with the focused skill updates if the invariant lands inconsistently;
  - if implementation shows a broader workflow or architecture problem than approved, stop and create a separate architecture/proposal track instead of widening M1 silently.

## Validation plan

- Before implementation:
  - complete `plan-review`;
  - the active `specs/test-spec-readiness-and-skill-workflow-alignment.test.md` now owns concrete proof for:
    - `spec-review` immediate next stage versus eventual `test-spec` readiness
    - `approved` being incompatible with `not-ready` and `not-assessed`
    - `inconclusive` producing no immediate-next-stage value plus a recorded stop condition
    - `plan-review` preserving `test-spec` as the immediate next handoff when in scope
    - `test-spec` preserving approved spec, spec-review findings, concrete plan, and relevant architecture or ADR inputs when needed
    - touched workflow-facing skill surfaces, workflow summary, durable workflow spec, and generated output staying aligned
  - confirm whether any currently active broader workflow proof surface needs overlap updates; do not revive archived workflow test artifacts by default.
- During implementation:
  - run the narrow skill/generation checks first:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/test-artifact-lifecycle-validator.py`
    - `python scripts/build-skills.py`
    - `python scripts/build-skills.py --check`
  - run `python scripts/validate-change-metadata.py docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml` once the change-local pack exists;
  - run explicit-path artifact validation once the focused test spec exists and the durable workflow spec is touched;
  - record the explicit `AGENTS.md` / `CONSTITUTION.md` impact decision in validation notes;
  - use targeted `rg` and `git diff --check` commands before the repo-wide smoke pass.
- Final milestone proof:
  - run `bash scripts/ci.sh`;
  - record the exact commands and results in this plan body's validation notes.

## Risks and recovery

- Risk: the focused spec and `specs/rigorloop-workflow.md` diverge.
  - Recovery: treat the focused spec as the change vehicle only, fold the enduring invariant into `specs/rigorloop-workflow.md`, and verify both artifacts together.
- Risk: `spec-review` and `test-spec` preserve different prerequisite sets.
  - Recovery: align both surfaces to the approved spec and rerun the targeted `rg` and lifecycle proof.
- Risk: wording changes accidentally imply new autoprogression beyond the approved v1 contract.
  - Recovery: keep `spec-review` isolated by default and re-check every changed summary surface against the approved spec and `specs/rigorloop-workflow.md`.
- Risk: the change expands into general workflow-skill normalization.
  - Recovery: keep the implementation limited to `workflow`, `spec-review`, `test-spec`, and `plan-review` only if needed.

## Dependencies

- `plan-review` must complete before implementation starts.
- the active focused test spec must remain current before production guidance changes begin.
- No separate architecture artifact is planned; if implementation expands beyond workflow guidance and skill alignment, stop and create architecture before implementation.
- The baseline change-local pack for this ordinary non-trivial change is required during implementation.
- Generated `.codex/skills/` output must stay synchronized with canonical `skills/`.

## Progress

- [x] 2026-04-22: proposal accepted and focused spec approved.
- [x] 2026-04-22: plan created and indexed in `docs/plan.md`.
- [x] 2026-04-22: `plan-review` feedback incorporated; early validation and focused `test-spec` proof requirements tightened.
- [x] 2026-04-22: `specs/test-spec-readiness-and-skill-workflow-alignment.test.md` created and activated.
- [x] 2026-04-22: M1 updated `specs/rigorloop-workflow.md`, `docs/workflows.md`, `skills/spec-review/SKILL.md`, `skills/test-spec/SKILL.md`, `skills/workflow/SKILL.md`, `skills/plan-review/SKILL.md`, created the baseline change-local pack under `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/`, and regenerated `.codex/skills/`.

## Decision log

- 2026-04-22: No separate architecture artifact is planned for the first slice. Rationale: the approved spec limits the implementation to workflow guidance, workflow summary, and directly affected workflow-facing skills.
- 2026-04-22: Start with one implementation milestone. Rationale: the expected authored surfaces are narrow enough for one coherent review loop and one coherent commit; split later only if implementation expands.
- 2026-04-22: `skills/plan-review/SKILL.md` is conditional in scope. Rationale: the approved spec includes it only if the current wording actually obscures `test-spec` as the immediate next stage.
- 2026-04-22: Do not revive archived `specs/rigorloop-workflow.test.md` for this slice by default. Rationale: the feature needs a focused new test spec, and broader workflow test ownership should only be reopened deliberately.
- 2026-04-22: `AGENTS.md` and `CONSTITUTION.md` remain unchanged in M1. Rationale: `docs/workflows.md` and `specs/rigorloop-workflow.md` absorbed the new workflow wording while the higher-level practical summary and governing principles remained truthful as written.

## Surprises and discoveries

- 2026-04-22: The repository currently has no `docs/project-map.md`. The feature is still narrow enough that a project map is not required.
- 2026-04-22: `specs/rigorloop-workflow.test.md` is archived, so focused proof should live in a new feature-specific test spec rather than assuming an active top-level workflow test owner already exists.
- 2026-04-22: `skills/plan-review/SKILL.md` did need a small wording fix. Its prior expected-output text blurred immediate `test-spec` handoff with downstream implementation readiness, so it stayed within first-pass scope.

## Validation notes

- 2026-04-22: plan creation validation passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `git diff --check -- docs/plan.md docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md specs/test-spec-readiness-and-skill-workflow-alignment.md docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - Result: passed.
- 2026-04-22: plan-review follow-up edits validated with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `git diff --check -- docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - Result: passed.
- 2026-04-22: `test-spec` created `specs/test-spec-readiness-and-skill-workflow-alignment.test.md` as the active proof surface for the immediate-next-stage, eventual-readiness, stop-condition, preserved-prerequisite, and validation-alignment contract.
- 2026-04-22: `test-spec` stage validation passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `git diff --check -- docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md specs/test-spec-readiness-and-skill-workflow-alignment.md specs/test-spec-readiness-and-skill-workflow-alignment.test.md docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - Result: passed.
- 2026-04-22: M1 targeted validation passed with:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/rigorloop-workflow.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `rg -n 'immediate next repository stage|downstream readiness|eventual `?test-spec`? readiness|ready|conditionally-ready|not-ready|not-assessed|approved|changes-requested|blocked|inconclusive|stop condition' skills/spec-review/SKILL.md skills/test-spec/SKILL.md skills/workflow/SKILL.md skills/plan-review/SKILL.md docs/workflows.md specs/test-spec-readiness-and-skill-workflow-alignment.md specs/rigorloop-workflow.md .codex/skills`
  - `rg -n 'spec-review|test-spec|plan-review|architecture|workflow' AGENTS.md CONSTITUTION.md docs/workflows.md specs/rigorloop-workflow.md`
  - `git diff --check -- specs/test-spec-readiness-and-skill-workflow-alignment.test.md specs/test-spec-readiness-and-skill-workflow-alignment.md specs/rigorloop-workflow.md skills/spec-review/SKILL.md skills/test-spec/SKILL.md skills/workflow/SKILL.md skills/plan-review/SKILL.md docs/workflows.md docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md docs/plan.md`
  - `bash scripts/ci.sh`
  - Result: passed.
- 2026-04-22: No `docs/plan.md` lifecycle update was needed during M1. The initiative remains active, and the existing active-plan index entry stays truthful while the plan body moves from `implement` readiness into downstream review readiness.

## Outcome and retrospective

- While this plan is still active, say so plainly instead of implying `done`, `blocked`, or `superseded`.
- When the real lifecycle decision is known, update both this plan body and the single `docs/plan.md` entry in the same change.

## Readiness

- This plan is active.
- No separate architecture artifact is expected for this slice.
- `plan-review` feedback is incorporated.
- The active focused test spec now exists.
- M1 implementation is complete.
- The next stage is `code-review`.
- Workflow-managed handoff may proceed into first-pass review.

## Risks and follow-ups

- If implementation shows that another review-stage skill outside the approved first-pass scope must change to preserve the contract, stop and record that scope expansion explicitly instead of widening the milestone silently.
- If later work proves the wording pattern stable enough for enforcement, open a separate proposal/spec track for validator-backed readiness-pattern checks rather than adding them ad hoc during this slice.
