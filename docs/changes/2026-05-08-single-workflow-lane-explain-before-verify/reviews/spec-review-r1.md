# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/skill-contract.md`
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Workflow spec amendment: `specs/rigorloop-workflow.md`
- Autoprogression spec amendment: `specs/workflow-stage-autoprogression.md`
- Skill contract spec amendment: `specs/skill-contract.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`
- Workflow summary: `docs/workflows.md`
- Prior proposal review: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/proposal-review-r2.md`

## Findings

### SR1 - Proportional evidence conflicts with mandatory stage wording

Finding ID: SR1
Severity: major

Evidence: `specs/rigorloop-workflow.md` says tiny low-risk proportional evidence may use "`explain-change` or PR-summary rationale, depending on change size and repository policy" in `R2`. The same section says proportional evidence "MUST NOT bypass `code-review`, `verify`, `explain-change`, `pr`" in `R4`. The stage table later marks `code-review` mandatory only for non-trivial changes and says `explain-change` covers standalone durable explanation for non-trivial changes while all changes require PR-summary explanation.

Required outcome: The spec must define the tiny-change minimum without implying that every tiny low-risk change must run standalone `code-review` and standalone `explain-change`, while still preserving final rationale, validation, PR readiness, and all triggered stages.

Safe resolution: Rewrite `R4` and the `explain-change` table row so the invariant is explicit: proportional evidence does not bypass required final rationale, final `verify`, PR handoff, or any stage whose trigger is active. State that standalone `code-review` and standalone `explain-change` are required when their triggers apply, while tiny low-risk changes may satisfy rationale through PR-summary rationale when repository policy allows it.

### SR2 - Milestone closeout still routes clean final reviews directly to verify

Finding ID: SR2
Severity: major

Evidence: `specs/workflow-stage-autoprogression.md` now says the final workflow-managed sequence is `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`. But `R3bb` still says a clean final implementation milestone must "continue to `verify`" when implementation milestones are closed, and the acceptance criteria still says only final clean implementation milestone reviews can make `verify` the next stage. `specs/rigorloop-workflow.md` also keeps acceptance wording that clean final implementation milestone reviews can route to `verify`.

Required outcome: Milestone closeout requirements and acceptance criteria must agree that a clean final implementation milestone reaches final closeout, not direct `verify`.

Safe resolution: Change direct `verify` routing language to final-closeout routing language. Use `ci-maintenance` when triggered; otherwise `explain-change`; then `verify`; then `pr`. Keep existing verify-readiness guardrails only as prerequisites for reaching final closeout, not as the immediate next-stage route.

### SR3 - Amended spec lifecycle sections have stale or incomplete next-artifact guidance

Finding ID: SR3
Severity: major

Evidence: `specs/skill-contract.md` is now a draft amendment ready for `spec-review`, but its `Next artifacts` section still says "Plan-review for the execution plan" and "Matching test spec after plan-review." `specs/workflow-stage-autoprogression.md` is also a draft amendment ready for `spec-review`, but its `Next artifacts` section still carries older architecture, architecture-review, test spec, and plan entries before adding the current spec-review entry. `specs/rigorloop-workflow.md` has no current `Next artifacts` section for this draft amendment.

Required outcome: Each amended spec must truthfully tell downstream agents what comes next for this amendment, without mixing old completed lifecycle history into the current next-stage queue.

Safe resolution: For each touched draft spec, update `Next artifacts` to name the current next stage and required follow-on artifacts for this amendment, such as `spec-review`, matching test-spec updates, and execution planning. Move historical or already-completed artifacts into `Follow-on artifacts` or leave them there as history. If a spec intentionally does not need architecture or plan, say so explicitly rather than leaving stale old next-artifact entries.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | SR1 and SR2 leave conflicting interpretations for tiny-change gates and final milestone closeout routing. |
| Normative language | concern | Normative `MUST` language in `R4` and `R3bb` conflicts with nearby requirements. |
| Completeness | concern | Current next-artifact guidance is incomplete or stale for the amended specs. |
| Testability | concern | Tests could reasonably assert either PR-summary rationale or mandatory standalone `explain-change`; tests could also assert either direct `verify` or final-closeout routing. |
| Examples | pass | New examples generally match the intended direction, though stale requirements need alignment. |
| Compatibility | pass | In-flight work and active-plan transition rules are covered. |
| Observability | pass | Validation evidence, static checks, and workflow-guide expectations are observable. |
| Security/privacy | pass | No new security-sensitive behavior is introduced, and generated/public surfaces remain bounded. |
| Non-goals | pass | Scope excludes runtime redesign, generator script creation, replacement lanes, and broad semantic scoring. |
| Acceptance criteria | concern | Acceptance criteria still include stale direct-verify milestone wording. |

## Review outcome

Changes requested.

No automatic downstream handoff is performed because this was a direct `spec-review` request.

Immediate next repository stage: none

Eventual `test-spec` readiness: not-ready

Stop condition: upstream spec fixes are required in `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, and `specs/skill-contract.md` before downstream test-spec, planning, or implementation should rely on the amended contract.
