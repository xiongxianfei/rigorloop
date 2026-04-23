# Implement First-Attempt Correctness Explain Change

## Summary

This change implements the approved first-pass completeness contract for the implementation stage. It teaches `implement` to target the smallest scope-complete change and a first-pass acceptable result, aligns `workflow` to the same narrower execution-stage expectation, updates the short workflow summary so it does not drift, and records the required aligned-surface audit plus change-local reasoning for this slice.

## Problem

The repository had an approved spec for first-pass correctness, but the canonical workflow skills still left that expectation mostly implicit. That gap made it too easy for a locally correct edit to miss required aligned surfaces, skip required edge cases, or hand off an incomplete slice to `code-review` without a contributor-visible record of why unchanged companion surfaces were still acceptable.

## Decision trail

- Proposal: `docs/proposals/2026-04-23-implement-first-attempt-correctness.md`
- Spec: `specs/implement-first-attempt-correctness.md`
- Test spec: `specs/implement-first-attempt-correctness.test.md`
- Requirements: `R1`-`R10b`, with `R10a` explicitly deferred
- Architecture: none for this first slice
- Plan milestone:
  - M1: implement first-pass completeness guidance and aligned workflow wording

## Diff rationale by area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `skills/implement/SKILL.md` | adds the first-pass completeness section, same-slice completeness-set language, unaffected-rationale handling, and targeted-proof-before-handoff wording | make the implementation-stage contract observable instead of relying on quality intent alone | `R1`-`R5c`, `R7`, `R9` | focused test spec `T1`-`T4`, `T6`, `T8`, targeted proof commands |
| `skills/workflow/SKILL.md` | mirrors the new implementation-stage vocabulary under execution-stage claim ownership without widening routing behavior | keep the lifecycle entrypoint aligned with `implement` while preserving stage order and ownership boundaries | `R6`-`R6d`, `R8c` | focused test spec `T5`, targeted wording review |
| `docs/workflows.md` | adds the short-form summary of first-pass acceptable result, unaffected-rationale handling, and preventable first-pass misses | avoid summary drift after canonical skill wording changed | `R8d` | targeted wording review and vocabulary grep proof |
| `.codex/skills/` mirrors | regenerated derived skill surfaces from canonical `skills/` | keep generated adapter guidance synchronized with canonical workflow wording | `R8e` | `python scripts/build-skills.py`, `python scripts/build-skills.py --check` |
| `docs/proposals/2026-04-23-implement-first-attempt-correctness.md`, `specs/implement-first-attempt-correctness.md` | sync settled-artifact readiness text from earlier authoring-stage wording to the real post-implementation next stage | keep touched lifecycle-managed artifacts truthful after `M1` completion and avoid stale earlier-stage readiness claims | lifecycle-truthfulness rules, isolated `code-review` finding | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-23-implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`, `git diff --check -- docs/proposals/2026-04-23-implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.test.md docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/changes/2026-04-23-implement-first-attempt-correctness` |
| `docs/plans/2026-04-23-implement-first-attempt-correctness.md` | closes the aligned-surface audit, records final `update` and `no-change` decisions, and logs targeted implementation proof | use the active plan as the authoritative pre-`code-review` audit surface required by this slice | `R5b`, `R5ba`, `R7c` | plan audit review, lifecycle validation |
| `docs/changes/2026-04-23-implement-first-attempt-correctness/` | creates the baseline change-local pack for this ordinary non-trivial workflow change | satisfy the repository docs-changes contract while leaving durable rationale for the implementation slice | docs-changes baseline contract, M1 plan | `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml` |
| `specs/implement-first-attempt-correctness.test.md` | advances test-spec readiness from `implement` to `code-review` after implementation completes | keep the active proof-planning artifact truthful about the next stage | active test-spec lifecycle rules | artifact-lifecycle validation, plan alignment review |

## Aligned-surface audit closeout

| Surface | Final decision | Rationale |
| --- | --- | --- |
| `skills/workflow/SKILL.md` | `update` | `R6a` and `R8c` required aligned canonical workflow wording in the first slice. |
| `docs/workflows.md` | `update` | Leaving the short operational summary unchanged would have left contributor-facing workflow guidance stale relative to the canonical skills. |
| generated `.codex/skills/` | `update` | Canonical `skills/` wording changed, so the generated adapter mirrors had to be rebuilt. |
| `AGENTS.md` | `no-change` | The practical summary already points to higher-priority workflow artifacts and remained truthful once the aligned lower-level surfaces were updated. |
| `CONSTITUTION.md` | `no-change` | This slice sharpened stage-local workflow wording without changing repository principles or source-of-truth order. |

## Tests added or changed

- `specs/implement-first-attempt-correctness.test.md`
  - Remains the focused proof surface for first-pass acceptability, required edge-case sources, smallest scope-complete change, preventable first-pass misses, aligned-surface audit behavior, preserved workflow boundaries, and targeted-versus-broad validation separation.
  - Its readiness was updated to keep the next stage truthful after implementation.

## Review and verification status

- `code-review`
  - Status: pending
  - Result: one isolated `code-review` finding identified stale readiness text in the touched proposal and spec; this follow-up sync addresses that finding and a rerun is still required
- `verify`
  - Status: pending
  - Result: not started in this invocation

## Verification evidence

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- `rg -n 'first-pass acceptable result|required edge case|smallest scope-complete change|preventable first-pass miss|unaffected with rationale|code-review' skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md .codex/skills`
- `git diff --check -- skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md specs/implement-first-attempt-correctness.test.md docs/changes/2026-04-23-implement-first-attempt-correctness .codex/skills docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/plan.md AGENTS.md CONSTITUTION.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-23-implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- `git diff --check -- docs/proposals/2026-04-23-implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.md specs/implement-first-attempt-correctness.test.md docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/changes/2026-04-23-implement-first-attempt-correctness`
- Hosted CI status: unobserved from this environment

## Alternatives rejected

- Updating `bugfix` and other implementation-adjacent skills in the same slice
  - Rejected because the approved spec explicitly deferred that vocabulary alignment to a later follow-up.
- Folding the invariant into `specs/rigorloop-workflow.md` in this implementation pass
  - Rejected because `R10a` remains a separate optional follow-up rather than part of this first slice.
- Treating broad smoke as the minimum pre-`code-review` gate
  - Rejected because the approved plan and spec require targeted proof for M1 handoff when that narrower evidence is sufficient.

## Scope control

- `AGENTS.md` remained unchanged because the practical summary already stayed truthful once the lower-level workflow surfaces were aligned.
- `CONSTITUTION.md` remained unchanged because no principle-level rule changed here.
- `bugfix` and other implementation-adjacent skills remained untouched in this first slice.
- `docs/plan.md` stayed under `Active` because the initiative is implemented but not yet reviewed or verified.
- `specs/rigorloop-workflow.md` remained untouched because durable workflow-spec fold-in is still a separate follow-up.

## Risks and follow-ups

- Hosted CI still needs downstream observation once the branch reaches later review or PR stages.
- If later work decides this wording should become a durable repository-wide invariant, that follow-up should update `specs/rigorloop-workflow.md` through a separate approved change.
- If implementation-adjacent skills such as `bugfix` need the same vocabulary, that alignment should happen in the deferred follow-up already named by the approved spec.

## Readiness

- The isolated `implement` stage is complete for `M1`.
- The next stage is `code-review`.
- This file mirrors the final aligned-surface audit decisions required before handoff.
