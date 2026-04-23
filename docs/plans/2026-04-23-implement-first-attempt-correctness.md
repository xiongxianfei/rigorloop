# Implement first-attempt correctness plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-23
- Last updated: 2026-04-24
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved first-pass completeness contract as a narrow workflow-guidance change centered on `skills/implement/SKILL.md`, with aligned wording in `skills/workflow/SKILL.md` and only the summary or generated surfaces that would otherwise become stale.

This initiative should make the repository's implementation-stage guidance say the same observable thing about:

- what counts as a first-pass acceptable result before handoff to `code-review`;
- which edge cases are required in the first pass for the approved slice;
- what makes a change the smallest scope-complete change rather than merely the smallest diff;
- what later review findings count as preventable first-pass misses; and
- when aligned workflow summary or generated skill output must be updated in the same slice.

The implementation must stay inside the approved first slice:

- no stage-order, lane-selection, autoprogression, stop-condition, or ownership changes;
- no `bugfix` or other implementation-adjacent skill alignment in this change;
- no validator-backed scoring or enforcement in v1;
- no `specs/rigorloop-workflow.md` fold-in unless a later approved follow-up deliberately broadens the contract; and
- no broader workflow-skill normalization beyond `implement`, `workflow`, and the summary/generated surfaces that would otherwise drift.

## Source artifacts

- Proposal: `docs/proposals/2026-04-23-implement-first-attempt-correctness.md`
- Spec: `specs/implement-first-attempt-correctness.md`
- Spec-review findings carried into this plan:
  - define `Approved slice` explicitly instead of relying on repo shorthand;
  - enumerate acceptable authoritative surfaces for unaffected rationale under `R5b`;
  - make `docs/workflows.md` summary drift and generated `.codex/skills/` drift explicit instead of relying on vague alignment language.
- Architecture: none. The approved spec says no separate architecture artifact is expected for this slice.
- Architecture-review findings: none.
- Test spec: `specs/implement-first-attempt-correctness.test.md` is now active and owns the focused proof surface for this initiative.
- Related workflow and proof surfaces:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md` when changed canonical skill wording would otherwise leave the short workflow summary stale
  - generated `.codex/skills/`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md`

## Context and orientation

- This is workflow-governance work, not product runtime behavior, but it is contributor-facing and compatibility-sensitive because it changes canonical skill guidance.
- The focused approved spec is the current change vehicle. This first implementation slice should not fold the rule into `specs/rigorloop-workflow.md`; that durable follow-up remains optional future work under `R10a`.
- The main authored surfaces expected in the first implementation slice are:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/implement-first-attempt-correctness.test.md`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md`
  - `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- The aligned companion surfaces are conditional, not automatic:
  - `docs/workflows.md` only if the changed canonical skill wording would otherwise leave the short operational summary stale under `R8d`;
  - generated `.codex/skills/` only if canonical `skills/` changes would otherwise leave adapter guidance stale under `R8e`.
- The active plan is the authoritative pre-`code-review` audit surface for unchanged required aligned-surface decisions in this slice. Final aligned-surface decisions should be mirrored in `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md` when the change reaches handoff.
- Generated `.codex/skills/` output remains derived. Regenerate it; do not hand-edit it.
- The repository currently has no `docs/project-map.md`. The feature is narrow enough that no project map is required for planning.
- The current `implement` skill already requires approved inputs, tests-first behavior, narrow validation, and plan upkeep, but it does not yet define first-pass completeness in the observable vocabulary approved by the spec.
- The current `workflow` skill already owns artifact order, lane routing, and stage-owned language. This slice should add aligned first-pass completeness wording without changing those routing rules.
- `AGENTS.md` and `CONSTITUTION.md` are expected to remain unchanged in this slice because the approved change is narrower than a practical-summary or principle-level rewrite. If implementation proves otherwise, stop and revisit scope instead of widening M1 silently.
- This is ordinary non-trivial work. Implementation must carry the baseline change-local pack:
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md`

## Non-goals

- Changing stage order, lane selection, autoprogression, stop conditions, or stage ownership.
- Changing `code-review`, `verify`, or `pr` claim ownership.
- Aligning `bugfix` or other implementation-adjacent skills in the same slice.
- Folding the durable invariant into `specs/rigorloop-workflow.md` in this first implementation pass.
- Adding validator-backed scoring, automatic completeness detection, or other new enforcement tooling.
- Authorizing unrelated refactors in the name of first-pass completeness.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R5c`, observability, edge cases 1-5, acceptance criteria about first-pass acceptability, required edge-case sources, smallest scope-complete change, preventable misses, unaffected rationale, and blocker handling | `skills/implement/SKILL.md`, `specs/implement-first-attempt-correctness.test.md`, `docs/changes/2026-04-23-implement-first-attempt-correctness/`, this active plan |
| `R6`-`R6d`, edge case 6, acceptance criteria about workflow alignment and preserved ownership/routing boundaries | `skills/workflow/SKILL.md`, `docs/workflows.md` only if summary drift would otherwise remain |
| `R7`-`R8e`, edge cases 7-8, acceptance criteria about targeted validation, required aligned surfaces, summary drift, and generated-output drift | `skills/implement/SKILL.md`, `skills/workflow/SKILL.md`, `docs/workflows.md` conditionally, generated `.codex/skills/`, `specs/implement-first-attempt-correctness.test.md` |
| `R9`-`R10b`, non-goals, scope-control, tests-first preservation, and bugfix deferral | `skills/implement/SKILL.md`, `skills/workflow/SKILL.md`, `specs/implement-first-attempt-correctness.test.md`, change-local reasoning surfaces |
| `R10a` | No edit in this plan. The focused spec remains the reviewable change contract for this slice, and any fold-in to `specs/rigorloop-workflow.md` is a separate approved follow-up only if the repository later adopts this rule as durable generic workflow behavior. |

## Milestones

### M1. Implement first-pass completeness guidance and aligned workflow wording

- Goal:
  - Update the canonical `implement` and `workflow` skills to use the approved first-pass completeness vocabulary, carry the required change-local proof surfaces, and align any summary or generated companion surfaces that would otherwise be left stale.
- Requirements:
  - `R1`-`R10b`, with `R10a` explicitly deferred
- Files/components likely touched:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md` only if canonical wording changes would otherwise leave the workflow summary stale
  - `specs/implement-first-attempt-correctness.test.md`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md`
  - generated `.codex/skills/`
  - `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `docs/plan.md` only if lifecycle state changes during later execution
- Dependencies:
  - accepted proposal
  - approved focused spec
  - `plan-review`
  - active focused test spec created after `plan-review`
  - no separate architecture artifact unless scope expands beyond the approved slice
- Required aligned-surface audit:
  - The active plan is the authoritative pre-`code-review` audit surface for required aligned-surface decisions in M1.
  - Each audited surface must carry one current decision: `update`, `no-change`, `out-of-scope`, or `not-applicable`.
  - Every `no-change` decision must include rationale.
  - Final audit decisions must be mirrored in `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md` when the change reaches handoff.
  - Initial audit state:

    | Surface | Current decision | Rationale / trigger | Validation impact |
    | --- | --- | --- | --- |
    | `skills/workflow/SKILL.md` | `update` | `R6a` and `R8c` require aligned canonical workflow wording in the first slice. | Include in targeted pre-`code-review` proof. |
    | `docs/workflows.md` | `update` | The short operational summary would otherwise omit the new first-pass completeness wording added to canonical `implement` and aligned `workflow` guidance under `R8d`. | Include in targeted pre-`code-review` proof. |
    | generated `.codex/skills/` | `update` | Canonical `skills/` wording changed, so generated adapter guidance must be rebuilt to avoid drift under `R8e`. | Keep on the targeted `build-skills.py --check` proof path. |
    | `AGENTS.md` | `no-change` | The practical summary already points to higher-priority workflow artifacts and remains truthful once the canonical skills, plan audit, change-local pack, and `docs/workflows.md` are aligned. | Keep in targeted patch-hygiene proof to show it stayed unchanged intentionally. |
    | `CONSTITUTION.md` | `no-change` | This slice sharpens stage-local workflow guidance without changing repository principles or the source-of-truth order. | Keep in targeted patch-hygiene proof to show it stayed unchanged intentionally. |
- Tests to add/update:
  - create `specs/implement-first-attempt-correctness.test.md` as the focused proof surface for M1
  - require the focused test spec to prove the full `R1a` first-pass acceptable-result checklist
  - require the focused test spec to prove required edge-case sources under `R2` and the touched-failure-path rule under `R2b`
  - require the focused test spec to prove `smallest scope-complete change` is not the same as the smallest diff
  - require the focused test spec to prove preventable first-pass misses are distinguished from ordinary later review comments
  - require the focused test spec to prove `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` are updated together in this slice
  - require the focused test spec to prove `docs/workflows.md` and generated `.codex/skills/` are updated only when the changed canonical wording would otherwise leave them stale
  - require the focused test spec to prove this slice preserves routing behavior, ownership split, and bugfix boundaries
- Implementation steps:
  - create the baseline change-local pack for this initiative before implementation completion claims
  - use this active plan as the pre-`code-review` required aligned-surface audit and keep each candidate surface decision current as `update`, `no-change`, `out-of-scope`, or `not-applicable`
  - update `skills/implement/SKILL.md` so its pre-edit and handoff guidance uses the approved observable contract terms:
    - `first-pass acceptable result`
    - `required edge case`
    - `smallest scope-complete change`
    - `preventable first-pass miss`
  - make `skills/implement/SKILL.md` explicitly require identifying the same-slice completeness set, recording unaffected rationale in an acceptable authoritative surface when needed, running targeted validation before handoff, and stopping on blocker conditions instead of handing off an incomplete slice
  - update `skills/workflow/SKILL.md` only where the repository-level lifecycle summary must mirror the same implementation-stage expectation without changing lane routing, stage order, autoprogression, stop conditions, or stage ownership
  - inspect `docs/workflows.md`, generated `.codex/skills/`, `AGENTS.md`, and `CONSTITUTION.md` after the canonical edits and record the current aligned-surface decision for each entry in the audit table
  - if an audited surface remains `no-change`, record the rationale directly in the audit table before handoff
  - update `docs/workflows.md` only if leaving it unchanged would make the short workflow summary stale under `R8d`
  - regenerate `.codex/skills/` after the canonical `skills/` edits so generated adapter guidance does not drift under `R8e`
  - keep `bugfix` and other implementation-adjacent skills unchanged and record any needed future alignment as deferred follow-up rather than widening M1
- M1 aligned-surface closeout:
  1. Re-read the required aligned-surface audit.
  2. Replace every `TBD` decision with `update`, `no-change`, `out-of-scope`, or `not-applicable`.
  3. For every `no-change` decision, write a rationale.
  4. Add any newly affected surface to the implementation scope.
  5. Add any changed surface to targeted validation.
  6. Record the final audit state in the M1 progress log.
  7. Mirror the final aligned-surface decisions in `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md` when the slice reaches handoff.
- Validation commands:
  - Targeted pre-`code-review` proof:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/test-artifact-lifecycle-validator.py`
    - `python scripts/build-skills.py`
    - `python scripts/build-skills.py --check`
    - `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
    - `rg -n 'first-pass acceptable result|required edge case|smallest scope-complete change|preventable first-pass miss|unaffected with rationale|code-review' skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md .codex/skills`
    - `git diff --check -- skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md specs/implement-first-attempt-correctness.test.md docs/changes/2026-04-23-implement-first-attempt-correctness .codex/skills docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/plan.md AGENTS.md CONSTITUTION.md`
  - Optional broad smoke:
    - `bash scripts/ci.sh`
- Expected observable result:
  - `implement` guidance defines first-pass acceptability, required edge cases, same-slice completeness, targeted validation, unaffected rationale, and blocker handling in observable terms before handoff to `code-review`
  - `workflow` guidance mirrors that expectation in narrower companion wording without altering routing behavior
  - the active plan carries the aligned-surface audit through handoff, and `explain-change.md` mirrors the final aligned-surface decisions once the slice reaches handoff
  - `docs/workflows.md` and generated `.codex/skills/` remain truthful when canonical skill wording changes would otherwise make them stale
  - `bugfix`, other adjacent skills, and durable workflow-spec fold-in remain untouched
- Commit message:
  - `M1: implement first-pass completeness guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` may drift if one is updated without the other
  - `docs/workflows.md` or generated `.codex/skills/` may be treated as optional even when the canonical wording makes them stale
  - the change may over-expand into `bugfix`, durable workflow-spec folding, or other skill normalization
  - the new wording could accidentally blur `implement` with `code-review` if handoff ownership is not kept explicit
- Rollback/recovery:
  - revert canonical and generated skill changes together if they land inconsistently
  - revert any summary-surface update together with the canonical wording that required it
  - if implementation reveals a need to change routing behavior, `bugfix`, or `specs/rigorloop-workflow.md`, stop and create the required follow-up artifact instead of widening M1 silently

## Validation plan

| Validation level | When | Required for M1 handoff? | Purpose |
| --- | --- | ---: | --- |
| Targeted proof | before `code-review` | yes | Prove the slice-specific contract and touched surfaces. |
| Optional broad smoke | any time | no | Catch unexpected repo-wide breakage early. |
| Final CI / PR proof | before PR handoff | yes, if repo policy requires | Prove final branch readiness after review-resolution. |

- Planning-stage validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `git diff --check -- docs/plan.md specs/implement-first-attempt-correctness.md docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- Milestone validation:
  - use the targeted pre-`code-review` proof commands listed under `M1` before handoff to `code-review`
  - treat `bash scripts/ci.sh` as optional broad smoke during implementation, not as the minimum M1 handoff gate
- Review-time validation expectations:
  - `plan-review` should confirm that one milestone is the right execution boundary and that `docs/workflows.md` plus generated `.codex/skills/` remain conditional aligned surfaces rather than automatic scope expansion
  - the active focused test spec should own proof for `R1`-`R10b`, including the non-changing workflow boundaries and the conditional summary/generated alignment checks
  - final implementation should rerun the targeted proof before `code-review`
  - later broad smoke or pre-PR proof should run `bash scripts/ci.sh` when repo policy or downstream readiness requires it

## Risks and recovery

- Risk: the new vocabulary lands in `implement` but not in `workflow`.
  - Recovery: treat both canonical skills as the primary authored pair for M1 and rerun targeted vocabulary checks before handoff.
- Risk: implementation broadens into durable workflow-contract work.
  - Recovery: keep `specs/implement-first-attempt-correctness.md` as the current change vehicle and stop for a new approved follow-up before touching `specs/rigorloop-workflow.md`.
- Risk: unaffected-rationale handling remains implicit.
  - Recovery: keep the active plan as the authoritative aligned-surface audit, require rationale for every `no-change` decision, and mirror the final decisions in `explain-change.md` at handoff.
- Risk: summary or generated drift is missed because the change looks narrow in the canonical file.
  - Recovery: explicitly inspect `docs/workflows.md` and `.codex/skills/` after canonical edits and either update them or record why they remain unaffected.

## Dependencies

- `plan-review` must complete before implementation starts.
- the active focused test spec must exist before canonical skill changes begin.
- No separate architecture artifact is planned. If implementation expands beyond `implement`, aligned `workflow`, and conditional summary/generated alignment, stop and revisit the approved scope before coding.
- The baseline change-local pack for this ordinary non-trivial change is required during implementation.
- Generated `.codex/skills/` output must stay synchronized with canonical `skills/`.

## Progress

- [x] 2026-04-23: proposal accepted and focused spec approved.
- [x] 2026-04-23: plan created and indexed in `docs/plan.md`.
- [x] 2026-04-23: isolated `plan-review` findings were incorporated by adding the aligned-surface audit and separating targeted M1 proof from later broad smoke / PR proof.
- [x] 2026-04-23: isolated `plan-review` approved the one-milestone slice and preserved `test-spec` as the immediate next authoring stage.
- [x] 2026-04-23: `specs/implement-first-attempt-correctness.test.md` created and activated as the focused proof surface for M1.
- [x] 2026-04-23: `M1` completed. `skills/implement/SKILL.md`, `skills/workflow/SKILL.md`, and `docs/workflows.md` now use the approved first-pass completeness vocabulary; the required change-local pack exists; generated `.codex/skills/` output is synchronized; and the aligned-surface audit closed with `docs/workflows.md` plus generated `.codex/skills/` marked `update`, `AGENTS.md` marked `no-change` with rationale, and `CONSTITUTION.md` marked `no-change` with rationale.
- [x] 2026-04-24: isolated `code-review` found stale readiness text in the touched proposal and spec; the follow-up implementation synced both settled artifacts to `code-review`, updated change-local reasoning, and reran narrow lifecycle validation for the touched artifact set.
- [x] 2026-04-24: first-pass `code-review` rerun completed with `clean-with-notes` and no required changes.
- [x] 2026-04-24: post-review lifecycle bookkeeping was synchronized so the settled artifacts, active test spec, active plan, and change-local pack all point to `verify` as the next stage.

## Decision log

- 2026-04-23: No separate architecture artifact is planned for this slice. Rationale: the approved spec limits the work to workflow guidance and aligned summary/generated surfaces rather than system-shape changes.
- 2026-04-23: Start with one implementation milestone. Rationale: the canonical skill changes and any required summary/generated alignment should land together as one coherent review unit.
- 2026-04-23: Keep `specs/rigorloop-workflow.md` out of M1. Rationale: `R10a` is a later optional fold-in, while `R10b` explicitly keeps this first slice focused on `implement` plus aligned `workflow` wording.
- 2026-04-23: Keep `bugfix` and other implementation-adjacent skills out of M1. Rationale: the approved spec explicitly defers that vocabulary alignment to a later approved follow-up.
- 2026-04-23: `AGENTS.md` and `CONSTITUTION.md` remain unchanged unless implementation proves real summary or principle drift. Rationale: this slice changes stage-local skill wording, not the higher-level repository contract.
- 2026-04-23: Use the active plan as the authoritative pre-`code-review` aligned-surface audit. Rationale: `R5b` / `R5ba` require a contributor-visible authoritative surface for unchanged required surfaces, and the plan is already active for this slice before handoff.
- 2026-04-23: Separate targeted M1 handoff proof from later broad smoke and PR proof. Rationale: `R7c` requires narrower slice-specific proof before `code-review` when that is sufficient, while `bash scripts/ci.sh` remains useful later as broad smoke or final readiness proof.
- 2026-04-23: Update `docs/workflows.md` in M1. Rationale: leaving the short operational summary unchanged would have left contributor-facing workflow guidance stale relative to the canonical skill wording.
- 2026-04-23: Close the aligned-surface audit with `AGENTS.md` and `CONSTITUTION.md` as explicit `no-change` decisions. Rationale: the practical summary and repository principles already remain truthful once the lower-level workflow surfaces are updated.

## Surprises and discoveries

- 2026-04-23: The repository currently has no `docs/project-map.md`; the slice is still narrow enough that a project map is not required.
- 2026-04-23: The current `implement` and `workflow` skills already contain much of the prerequisite-reading and ownership language, so the implementation should be a contract-sharpening change rather than a structural rewrite.
- 2026-04-23: Generated `.codex/skills/` mirrors canonical `skills/` for both touched skills, so canonical wording changes require regeneration even when no generator logic changes.

## Validation notes

- 2026-04-23: plan creation validation passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `git diff --check -- docs/plan.md specs/implement-first-attempt-correctness.md docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - Result: passed.
  - Recommended next stage: `plan-review`
- 2026-04-23: isolated `plan-review` follow-up edits validated with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `git diff --check -- docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - Result: passed.
  - Recommended next stage: `plan-review`
- 2026-04-23: `test-spec` created `specs/implement-first-attempt-correctness.test.md` as the active proof surface for first-pass acceptability, required edge-case sources, smallest scope-complete change, preventable miss handling, aligned-surface audit behavior, preserved non-changing workflow boundaries, and targeted-versus-broad validation separation.
- 2026-04-23: `test-spec` stage validation passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `git diff --check -- specs/implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.test.md docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - Result: passed.
  - Recommended next stage: `implement`
- 2026-04-23: M1 targeted pre-`code-review` proof passed after updating the canonical skills, the short workflow summary, the active plan audit, the change-local pack, and generated `.codex/skills/`.
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `rg -n 'first-pass acceptable result|required edge case|smallest scope-complete change|preventable first-pass miss|unaffected with rationale|code-review' skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md .codex/skills`
  - `git diff --check -- skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md specs/implement-first-attempt-correctness.test.md docs/changes/2026-04-23-implement-first-attempt-correctness .codex/skills docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/plan.md AGENTS.md CONSTITUTION.md`
  - Result: passed.
  - Optional broad smoke `bash scripts/ci.sh` was intentionally not run at this handoff because the approved M1 gate requires targeted proof before `code-review`, not broad smoke.
- 2026-04-24: review-driven lifecycle fix updated the accepted proposal and approved spec so their readiness text matches the active plan and active test spec after `M1` completion.
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-23-implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `git diff --check -- docs/proposals/2026-04-23-implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.test.md docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/changes/2026-04-23-implement-first-attempt-correctness`
  - Result: passed.
  - Recommended next stage: rerun `code-review`
- 2026-04-24: first-pass `code-review` record for `6b051eb..3b305fd`.
  - Review status: `clean-with-notes`
  - Findings: no blocking or required-change findings.
  - Recommended next stage: `verify`
- 2026-04-24: No `docs/plan.md` lifecycle update was needed after the clean review. The initiative remains active, and the existing active-plan index entry stays truthful while the plan body moves from `code-review` readiness into downstream `verify` readiness.
- 2026-04-24: post-review lifecycle sync updated the accepted proposal, approved spec, active test spec, active plan, and change-local pack so the tracked artifacts no longer advertise `code-review` as the next stage after the clean rerun.
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-23-implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `rg -n '^## (Active|Blocked|Done|Superseded)$|2026-04-23-implement-first-attempt-correctness' docs/plan.md`
  - `git diff --check -- docs/proposals/2026-04-23-implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.test.md docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/changes/2026-04-23-implement-first-attempt-correctness`
  - Result: passed.
  - Recommended next stage: rerun `verify`

## Outcome and retrospective

- `M1` is complete and the initiative remains active for `verify`.
- The aligned-surface audit closed with `docs/workflows.md` and generated `.codex/skills/` updated, and `AGENTS.md` plus `CONSTITUTION.md` explicitly kept unchanged with rationale.
- First-pass `code-review` completed with `clean-with-notes`; `verify` and any broader follow-up beyond this first slice remain pending.

## Readiness

- This plan is active.
- `M1` implementation, targeted pre-`code-review` proof, and first-pass `code-review` are complete.
- The immediate next repository stage is `verify`.
- This plan is ready for `verify`.
