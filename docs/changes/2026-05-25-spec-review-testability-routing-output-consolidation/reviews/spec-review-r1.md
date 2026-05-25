# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Target: specs/test-spec-readiness-and-skill-workflow-alignment.md
Reviewed artifact: specs/test-spec-readiness-and-skill-workflow-alignment.md
Review date: 2026-05-25
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SRTR-SR1, SRTR-SR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/spec-review-r1.md
- Review log: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-log.md
- Review resolution: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-resolution.md
- Open blockers: SRTR-SR1, SRTR-SR2
- Immediate next stage: spec revision

## Findings

## Finding SRTR-SR1

Finding ID: SRTR-SR1
Severity: major
Location: specs/test-spec-readiness-and-skill-workflow-alignment.md, `R1`, `R1a`, Example E6 title, and related `immediate next repository stage` wording
Evidence: The amendment introduces a closed `spec-review` immediate next-stage enum that includes `spec revision`, `review-resolution`, `architecture`, `plan`, and `none`, but inherited wording still says workflow-facing skills distinguish the "immediate next repository stage" and Example E6 is titled "missing reviewer input produces no immediate-next-stage value." This conflicts with the amended contract where `none` is an explicit immediate-next-stage value and some allowed values are not repository stages.
Required outcome: Align the top-level terminology, R1/R1a wording, and Example E6 heading with the amended field semantics so the spec consistently treats the field as `Immediate next stage`, not only as a repository-stage field or an empty value on missing inputs.
Safe resolution path: Replace stale "immediate next repository stage" wording in the amended sections with `Immediate next stage` where the closed enum is meant, clarify that the generic stage-order derivation applies to forward stage values, and retitle Example E6 to reflect `Immediate next stage: none`.
needs-decision rationale: none

## Finding SRTR-SR2

Finding ID: SRTR-SR2
Severity: minor
Location: specs/test-spec-readiness-and-skill-workflow-alignment.md, required spec sections
Evidence: The current `spec` authoring contract requires an `Accessibility and UX` section in feature specs. The amended spec has `Security and privacy` and `Performance expectations`, but no `Accessibility and UX` section or not-applicable rationale.
Required outcome: Add the required `Accessibility and UX` section or an explicit not-applicable rationale so the amended spec satisfies the current feature-spec structure before downstream test-spec or implementation work relies on it.
Safe resolution path: Add `## Accessibility and UX` after `Security and privacy` with a short statement that this Markdown workflow-contract change has no graphical UI surface and that user-facing clarity is covered by the skill-output wording requirements.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
|---|---|---|
| requirement clarity | concern | The routing/readiness requirements are mostly precise, but SRTR-SR1 leaves stale repository-stage and empty-route wording in the same contract. |
| normative language | pass | The new `MUST` clauses are testable through skill text, skeletons, fixtures, and validator behavior. |
| completeness | concern | SRTR-SR2 identifies one missing required section from the current spec structure. |
| testability | pass | R8a-R8e provide concrete deterministic validation expectations and an explicit parser-support deferral boundary. |
| examples | concern | E6's title conflicts with its amended expected output shape. |
| compatibility | pass | The amendment preserves stage order and autoprogression boundaries while tightening field values. |
| observability | pass | The spec names result fields, validator outcomes, stop conditions, and parser-support boundaries as observable proof. |
| security/privacy | pass | The spec introduces no secrets, network dependency, destructive action, or weakening of security-sensitive workflow rules. |
| non-goals | pass | Non-goals exclude stage-order redesign, broad review-family rewrites, `not-assessed`, and `test-spec` as immediate routing. |
| acceptance criteria | concern | Acceptance criteria should align with the fixed terminology after SRTR-SR1. |

## Eventual test-spec readiness

not-ready

The contract substance is close, but the spec still needs revision before test-spec authoring can safely map the amended field semantics without guessing around `none` and "repository stage" wording.

## Stop condition

Material findings SRTR-SR1 and SRTR-SR2 require spec revision before approval.

## Recommended spec edits

- Replace amended-scope uses of "immediate next repository stage" with `Immediate next stage` where the field may contain `spec revision`, `review-resolution`, or `none`.
- Preserve repository-stage wording only where the spec is specifically discussing forward values `architecture` and `plan`.
- Retitle Example E6 to avoid saying it produces no immediate-next-stage value.
- Add an `Accessibility and UX` section with a not-applicable or Markdown skill-text rationale.

## No-finding statement

Not applicable. This review recorded material findings.
