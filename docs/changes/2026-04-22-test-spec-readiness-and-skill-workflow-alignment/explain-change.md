# Test-Spec Readiness And Skill Workflow Alignment Explain Change

## Summary

This change implements the approved distinction between immediate repository-stage handoff and downstream readiness for later proof planning. It updates the durable workflow rule, the short workflow summary, and the directly affected workflow-facing skills so `spec-review`, `plan-review`, and `test-spec` no longer blur "what happens next" with "what could be ready later."

## Problem

The repository had approved a focused contract saying workflow-facing skills must distinguish immediate next stage from later-stage readiness, but the durable workflow rule and stage-local skill guidance still left room for ambiguous closing language. In practice that ambiguity could let `spec-review` imply `test-spec` too early, treat missing context like a pseudo-stage, or weaken the preserved prerequisites for `test-spec` authoring.

## Decision trail

- Exploration: none; the problem statement was already concrete enough to move directly into proposal/spec work.
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
| `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`, `docs/plan.md` | created and maintained the one-milestone execution plan, recorded the clean first-pass review and verify outcomes, and kept readiness truthful | preserve lifecycle truth in tracked artifacts rather than chat-only stage handoffs | active-plan policy, plan `M1` | lifecycle validation, `git diff --check` |
| `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/` | creates the required change-local pack | satisfy the repository docs-changes baseline while leaving durable review rationale behind | plan M1, docs-changes baseline | metadata validation, lifecycle validation |

## Tests added or changed

- `specs/test-spec-readiness-and-skill-workflow-alignment.test.md`
  - Owns proof for immediate next stage versus eventual readiness, negative output shapes, preserved stage order, conditional `plan-review` handoff wording, preserved `test-spec` prerequisites, narrow first-pass scope, and repo-owned validation surfaces.

## Review and verification outcomes

- First-pass `code-review`
  - Status: `clean-with-notes`
  - Result: no blocking or required-change findings; the clean result was grounded in the actual committed diff, approved artifacts, checklist coverage, and recorded validation evidence
  - Durable location: `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- `verify`
  - Verdict: `ready`
  - Result: no blockers, no stale lifecycle drift, and no missing validation evidence after the post-review bookkeeping updates
  - Durable location: `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`

## Verification evidence

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/rigorloop-workflow.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- `rg -n 'immediate next repository stage|downstream readiness|eventual \`?test-spec\`? readiness|ready|conditionally-ready|not-ready|not-assessed|approved|changes-requested|blocked|inconclusive|stop condition' skills/spec-review/SKILL.md skills/test-spec/SKILL.md skills/workflow/SKILL.md skills/plan-review/SKILL.md docs/workflows.md specs/test-spec-readiness-and-skill-workflow-alignment.md specs/rigorloop-workflow.md .codex/skills`
- `rg -n 'spec-review|test-spec|plan-review|architecture|workflow' AGENTS.md CONSTITUTION.md docs/workflows.md specs/rigorloop-workflow.md`
- `rg -n '^## (Active|Blocked|Done|Superseded)$|2026-04-22-test-spec-readiness-and-skill-workflow-alignment' docs/plan.md`
- `git diff --check -- specs/test-spec-readiness-and-skill-workflow-alignment.test.md specs/test-spec-readiness-and-skill-workflow-alignment.md specs/rigorloop-workflow.md skills/spec-review/SKILL.md skills/test-spec/SKILL.md skills/workflow/SKILL.md skills/plan-review/SKILL.md docs/workflows.md docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md docs/plan.md`
- `git diff --check -- docs/plan.md docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md specs/test-spec-readiness-and-skill-workflow-alignment.test.md docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
- `bash scripts/ci.sh`
- manual contract review over:
  - `spec-review` immediate-next-stage versus eventual-readiness wording
  - negative output shapes for `not-ready` and `not-assessed`
  - preserved `plan-review -> test-spec` handoff wording
  - preserved `test-spec` prerequisites including relevant architecture or ADR inputs
  - no-change decisions for `AGENTS.md` and `CONSTITUTION.md`
- Hosted CI status: unobserved from this environment

## Alternatives rejected

- Broad review-stage normalization across every workflow-facing skill
  - Rejected because the approved first slice was intentionally narrow and only named `spec-review`, `test-spec`, `workflow`, and `plan-review` when a real defect existed there.
- A dedicated readiness-wording validator in v1
  - Rejected because the approved spec explicitly deferred machine enforcement until the wording contract stabilizes.
- Pseudo-routing states such as `missing-context resolution` or `blocker handling`
  - Rejected because the approved contract treats those as stop conditions, not repository stages.
- A separate architecture artifact for this slice
  - Rejected because the implementation stayed inside workflow guidance and skill alignment rather than changing boundaries or system shape.

## Scope control

- `skills/plan-review/SKILL.md` was touched because implementation found a real wording defect around immediate handoff versus downstream implementation readiness; it was not widened beyond that fix.
- `AGENTS.md` was left unchanged because the existing practical workflow summary remained truthful once `docs/workflows.md` and the workflow spec carried the new wording.
- `CONSTITUTION.md` was left unchanged because this slice refined workflow wording without introducing a new repository principle.
- `docs/plan.md` stayed under `Active` because the initiative is not done yet; only the next-stage readiness moved from `explain-change` to `pr`.
- No new workflow router, readiness-pattern validator, persistence layer, or broader review-stage normalization was introduced.

## Risks and follow-ups

- Hosted CI will still need downstream observation once the branch reaches PR.
- If later work shows the wording pattern is stable enough for machine enforcement, that should go through a separate proposal/spec track rather than widening this v1 slice.
- If another review-stage skill outside the approved first-pass scope turns out to conflict with the new invariant, that should be handled in an explicit follow-up instead of silently broadening this change.

## PR-ready summary

- The durable workflow rule now distinguishes immediate next repository stage from downstream readiness for later `test-spec` authoring.
- `spec-review`, `test-spec`, `workflow`, and the necessary `plan-review` wording now use the same approved handoff, stop-condition, and preserved-prerequisite contract.
- The initiative carries its own accepted proposal, approved spec, active test spec, active plan, change metadata, clean review record, verify result, and durable explanation so PR review does not need to reconstruct the reasoning from chat history.

## Readiness

- `explain-change` is complete for this initiative.
- The next stage is `pr`.
- This invocation was a direct `explain-change` request, so no automatic handoff to `pr` was performed here.
