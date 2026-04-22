# Test-Spec Readiness And Skill Workflow Alignment Explain Change

## Summary

This change implements the approved distinction between immediate repository-stage handoff and downstream readiness for later proof planning. It updates the durable workflow rule, the short workflow summary, and the directly affected workflow-facing skills so `spec-review`, `plan-review`, and `test-spec` no longer blur "what happens next" with "what could be ready later."

## Problem

The repository had approved a focused contract saying workflow-facing skills must distinguish immediate next stage from later-stage readiness, but the durable workflow rule and stage-local skill guidance still left room for ambiguous closing language. In practice that ambiguity could let `spec-review` imply `test-spec` too early, treat missing context like a pseudo-stage, or weaken the preserved prerequisites for `test-spec` authoring.

## Decision trail

- Proposal: `docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- Spec: `specs/test-spec-readiness-and-skill-workflow-alignment.md`
- Test spec: `specs/test-spec-readiness-and-skill-workflow-alignment.test.md`
- Requirements: `R1`-`R8a`
- Architecture: none for this approved first slice
- Plan milestone:
  - M1: implement immediate-next-stage versus downstream-readiness alignment

## Diff rationale by area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `specs/rigorloop-workflow.md` | adds glossary terms, normative handoff/readiness rules, negative-output requirements, preserved `test-spec` prerequisites, and edge cases | move the enduring invariant into the durable workflow rule instead of leaving it only in the focused spec | `R1`-`R6b`, approved workflow-spec ownership split | focused test spec `T1`-`T6`, manual contract review |
| `docs/workflows.md` | adds short-form summary bullets for `spec-review` and `plan-review` handoff versus downstream readiness | keep the contributor-facing operational summary truthful without moving detail out of the authoritative workflow spec | `R1`-`R5b`, observability section | targeted wording review |
| `skills/spec-review/SKILL.md` | requires explicit review outcome, immediate-next-stage field, eventual `test-spec` readiness field, and stop-condition behavior | make `spec-review` output match the approved contract and forbid pseudo-routing states | `R2`-`R3k`, `T1`-`T4` | skill validation, focused manual review |
| `skills/test-spec/SKILL.md` | preserves approved spec, spec-review findings, concrete plan, and relevant architecture/ADR inputs as prerequisites | prevent proof authoring from silently proceeding off an unready upstream review result | `R6`-`R6b`, `T6` | focused manual review |
| `skills/workflow/SKILL.md` | teaches the distinction between immediate next stage and downstream readiness across the workflow lane | keep orchestration guidance consistent with the durable workflow rule and focused spec | `R1`-`R5b`, `T1`-`T5` | skill validation, wording review |
| `skills/plan-review/SKILL.md` | narrows output wording so `test-spec` remains the immediate next handoff and any implementation readiness is clearly downstream | fix the only adjacent stage-local wording defect found during implementation | `R5`-`R5b`, `T5`, plan scope rule | manual contract review |
| `.codex/skills/` mirrors | regenerated derived skill surfaces | keep generated compatibility output synchronized with canonical `skills/` | `R7`-`R8a`, `T8` | `python scripts/build-skills.py`, `python scripts/build-skills.py --check` |
| `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/` | creates the required change-local pack | satisfy the repository docs-changes baseline while leaving durable review rationale behind | plan M1, docs-changes baseline | metadata validation, lifecycle validation |

## Tests added or changed

- `specs/test-spec-readiness-and-skill-workflow-alignment.test.md`
  - Owns proof for immediate next stage versus eventual readiness, negative output shapes, preserved stage order, conditional `plan-review` handoff wording, preserved `test-spec` prerequisites, narrow first-pass scope, and repo-owned validation surfaces.

## Verification evidence so far

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`

Additional lifecycle, metadata, diff-integrity, and smoke validation will be appended here as the workflow-managed review and verify stages complete.

## Scope control

- `skills/plan-review/SKILL.md` was touched because implementation found a real wording defect around immediate handoff versus downstream implementation readiness; it was not widened beyond that fix.
- `AGENTS.md` is expected to remain unchanged if the current practical workflow summary is still truthful after the new workflow-spec and skill wording lands.
- `CONSTITUTION.md` is expected to remain unchanged because this slice refines workflow guidance rather than introducing a new repository principle.
- No new workflow router, readiness-pattern validator, persistence layer, or broader review-stage normalization was introduced.

## Risks and follow-ups

- Hosted CI will still need downstream observation once the branch reaches PR.
- If later work shows the wording pattern is stable enough for machine enforcement, that should go through a separate proposal/spec track rather than widening this v1 slice.
- If another review-stage skill outside the approved first-pass scope turns out to conflict with the new invariant, that should be handled in an explicit follow-up instead of silently broadening this change.
