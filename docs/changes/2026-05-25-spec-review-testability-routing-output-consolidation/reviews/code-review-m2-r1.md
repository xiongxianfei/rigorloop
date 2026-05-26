# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Target: commit 76a22755eec0587304ea403d2156160db52ccf2c
Reviewed artifact: M2 implementation for canonical spec-review routing/readiness contract
Review date: 2026-05-25
Reviewer: Codex code-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/code-review-m2-r1.md, docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-log.md, docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-resolution.md, docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md, docs/plan.md, docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml
- Open blockers: SRTR-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRTR-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-log.md
- Review resolution: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution, M3
- Required review-resolution: yes
- Finding IDs: SRTR-CR1
- Verify readiness: not-claimed

## Inputs Reviewed

- Commit: 76a22755eec0587304ea403d2156160db52ccf2c
- Plan: docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md
- Spec: specs/test-spec-readiness-and-skill-workflow-alignment.md
- Test spec: specs/test-spec-readiness-and-skill-workflow-alignment.test.md
- Workflow spec touched by M2: specs/rigorloop-workflow.md
- Change metadata: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml
- Prior review: docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/code-review-m1-r1.md

## Diff Summary

M2 adds canonical `spec-review` contract validation in `scripts/skill_validation.py`, adds canonical and adjacent-drift tests in `scripts/test-skill-validator.py`, updates `skills/spec-review/SKILL.md`, updates `skills/spec-review/assets/review-result-skeleton.md`, removes stale `not-assessed` wording from `skills/test-spec/SKILL.md`, updates the durable workflow spec, and records behavior-preservation evidence and plan state.

The skill and skeleton updates correctly separate `Immediate next stage` from `Eventual test-spec readiness`, exclude `test-spec` from the immediate-stage enum, preserve the approval-to-readiness rule, and de-duplicate the material-finding field list to the asset. The remaining issue is in the workflow-spec drift fix: two workflow-spec lines still carry the old missing or generic immediate-stage wording.

## Findings

## Finding SRTR-CR1

Finding ID: SRTR-CR1
Severity: major
Location: specs/rigorloop-workflow.md:958 and specs/rigorloop-workflow.md:1027
Evidence: The approved spec requires missing inputs to use `Immediate next stage: none` rather than an empty or missing field (`R2h`, `R3j`, and `AC-SRTR-ROUTE-005`). M2 explicitly edited `specs/rigorloop-workflow.md` because the durable workflow invariant still contained old empty-route wording. However, the M2 diff still leaves line 958 saying an `inconclusive` review may record a stop condition "without naming any immediate next repository stage" and line 1027 saying reviewers distinguish "immediate next repository stage" from readiness. That reintroduces the exact stale field semantics the M2 workflow-spec update was meant to remove.
Required outcome: The durable workflow spec must consistently describe the result field as `Immediate next stage`, use explicit `none` for inconclusive or missing-input cases, and reserve repository-stage language for the forward handoff values `architecture` and `plan`.
Safe resolution path: Revise the affected workflow-spec edge case and outcome wording so `inconclusive` examples name `Immediate next stage: none`, and generic `spec-review` wording refers to the `Immediate next stage` result field instead of "immediate next repository stage." Then rerun the M2 validation scope and code-review.
needs-decision rationale: none

## Checklist Coverage

| Check | Verdict | Evidence |
|---|---|---|
| Spec alignment | block | `specs/rigorloop-workflow.md:958` conflicts with approved `R2h`, `R3j`, and `AC-SRTR-ROUTE-005` by preserving missing immediate-stage wording. |
| Test coverage | concern | Validator and fixture coverage covers canonical skill/skeleton fields, but no adjacent-drift test rejects stale workflow-spec empty-route wording. |
| Edge cases | block | The named missing-input edge case still appears in the workflow spec as no immediate-stage value instead of explicit `Immediate next stage: none`. |
| Error handling | pass | The validator changes return explicit errors for invalid field combinations and do not introduce unsafe exception paths for reviewed fixtures. |
| Architecture boundaries | pass | The implementation stays within approved skill, asset, validator, test, and direct-drift workflow-spec boundaries. |
| Compatibility | concern | The stale workflow wording can mislead contributors even though the canonical `spec-review` skill and result skeleton are corrected. |
| Security/privacy | pass | The reviewed diff changes local Markdown and validation code only; it introduces no secrets, auth path, network behavior, or sensitive logging. |
| Derived artifact currency | pass | M2 correctly leaves public adapter proof to M3 and uses canonical authored skill source. |
| Unrelated changes | pass | The adjacent `test-spec` and workflow-spec edits are justified by direct drift dependencies; the finding concerns incomplete workflow-spec alignment, not unrelated scope. |
| Validation evidence | concern | The recorded validation commands passed, but the stale wording was only caught by targeted review search, not by the current automated checks. |

## No-Finding Rationale

Not applicable. `SRTR-CR1` requires resolution before M2 can close.

## Validation Reviewed

Implementation evidence records passing M2 commands:

- `python scripts/test-skill-validator.py -k spec_review`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py skills/spec-review/SKILL.md`
- `python scripts/validate-skills.py skills/test-spec/SKILL.md`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check -- ...`

This review additionally searched the touched workflow, skill, validator, and test files for stale `not-assessed`, empty-route, direct `test-spec`, and pseudo-routing wording. That search found the workflow-spec wording cited in `SRTR-CR1`.

## Residual Risk

No branch, PR, final verification, CI, or generated-output readiness is claimed. M3 remains blocked until M2 resolves `SRTR-CR1` and passes re-review.

## Handoff

M2 is not closed. The next stage is review-resolution for `SRTR-CR1`, followed by implementation fix and rerun code-review for M2.
