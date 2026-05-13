# Project Artifact Location Guide and Examples Surface Review Resolution

## Scope

This record tracks material findings from formal lifecycle reviews for the project artifact location guide and examples surface change.

Closeout status: closed

## Resolution Entries

### proposal-review-r1

No material findings.

### spec-review-r1

Review closeout: closed

#### SR-001

Finding ID: SR-001
Disposition: accepted
Owner: spec author
Owning stage: spec
Chosen action: Distinguish source-rank precedence from token-efficient lookup order. Update `R5a` so public stage skills use `docs/workflows.md` as the concise artifact-location index while still obeying known governing spec/schema constraints and the `R2` source-rank rule when conflicts exist.
Rationale: Specs and schemas must not be bypassed, but public skills should not waste tokens broad-searching authoritative documents solely to find artifact paths. `docs/workflows.md` should serve as the user-facing path map; specs and schemas remain the authority for exact shapes, constraints, and conflicts.
Validation target: Add static or test coverage proving shared skill lookup wording references `R2` precedence or known spec/schema constraints and discourages broad path searches, then rerun `spec-review`.
Validation evidence: Spec updated in `specs/project-artifact-location-guide-and-examples-surface.md`; `spec-review-r2` approved the revised contract with no material findings.

### spec-review-r2

No material findings.

### plan-review-r1

Finding ID: PR-001
Disposition: accepted
Owner: plan author
Owning stage: plan
Chosen action: Revise the plan to keep M1-M4 as separate implementation milestones and require each milestone to hand off to `code-review` after implementation and targeted validation. M4 now represents generated-output implementation plus its own final milestone review handoff rather than the first code review for M1-M3.
Rationale: The plan is milestone-based, so repository workflow requires implementation and code review to repeat for each in-scope implementation milestone.
Validation target: Rerun `plan-review` after the plan sequencing and Current Handoff Summary language are updated.
Validation evidence: Plan updated in `docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md`; `plan-review-r2` approved the revised milestone sequencing with no material findings.

### plan-review-r2

No material findings.

### code-review-r1

No material findings.

### code-review-r2

No material findings.
