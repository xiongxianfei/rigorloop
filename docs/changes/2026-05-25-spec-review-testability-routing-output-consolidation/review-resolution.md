# Review Resolution: Spec-Review Testability Routing and Output Consolidation

## Scope

This record tracks material review finding closeout for the spec-review testability routing and output consolidation change.

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: plan-review-r1
Review closeout: plan-review-r2

- Reviews covered: `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `plan-review-r1`, `plan-review-r2`
- Findings resolved: 3
- Unresolved findings: 0
- Final result: `SRTR-SR1` and `SRTR-SR2` were accepted and resolved in the spec amendment. `spec-review-r2` and `spec-review-r3` approved the revised spec with no material findings. `SRTR-PR1` was accepted and resolved by revising the plan's M1/M2 milestone boundary. `plan-review-r2` approved the revised plan with no material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SRTR-SR1 | accepted | resolved | Spec wording now consistently uses `Immediate next stage` for the closed enum and distinguishes forward repository-stage handoff values from routing and no-handoff values. |
| SRTR-SR2 | accepted | resolved | Spec now includes the required `Accessibility and UX` section with a Markdown-output clarity rationale. |
| SRTR-PR1 | accepted | resolved | M1 is now fixture/parser scaffolding only; canonical enforcement begins in M2 with the canonical skill and result-skeleton updates. |

## Finding Details

### spec-review-r1

Review closeout: closed

#### SRTR-SR1

Finding ID: SRTR-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Aligned the amended spec terminology around the `Immediate next stage` result field. Replaced stale "immediate next repository stage" wording where the closed enum field is meant, clarified that generic repository stage-order derivation applies only to `architecture` and `plan`, and retitled Example E6 so it uses `Immediate next stage: none`.
Rationale: The finding is correct. The closed enum includes routing and no-handoff values that are not forward repository stages, so the spec must not use repository-stage wording for the whole field.
Validation target: Rerun lifecycle validation, review-artifact validation, change metadata validation, whitespace checks, and spec-review.
Validation evidence: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check -- ...` passed after the spec revision.

### spec-review-r2

Review closeout: closed

No material findings. Clean rerun approval is recorded in `reviews/spec-review-r2.md`.

### spec-review-r3

Review closeout: closed

No material findings. Clean rerun approval is recorded in `reviews/spec-review-r3.md`.

### plan-review-r1

Review closeout: closed

#### SRTR-PR1

Finding ID: SRTR-PR1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan revision
Chosen action: Revised the implementation milestone boundaries so M1 is scoped to controlled fixture/parser scaffolding that can pass without requiring unchanged canonical `spec-review` skill assets to satisfy the new routing/readiness output contract. Canonical enforcement against `skills/spec-review/SKILL.md` and `skills/spec-review/assets/review-result-skeleton.md` now begins in M2, the same milestone that updates those canonical assets. Added explicit milestone validation boundaries showing M1, M2, and M3 may request code-review only after their named validation can pass.
Rationale: The finding is correct. As written, M1 is expected to introduce checks that fail until M2 while also requiring passing validation and a code-review handoff for M1.
Validation target: Rerun plan-review after the plan revision and then rerun change metadata, review-artifact closeout validation, lifecycle validation, and whitespace checks.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check -- ...` passed after the plan revision.

### plan-review-r2

Review closeout: closed

No material findings. Clean rerun approval is recorded in `reviews/plan-review-r2.md`.

#### SRTR-SR2

Finding ID: SRTR-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Added the required `Accessibility and UX` section after `Security and privacy`. The section records that this Markdown workflow-contract amendment has no graphical UI surface and that its UX surface is text clarity in skill outputs and review records.
Rationale: The finding is correct. Current spec authoring requires the section or an explicit not-applicable rationale, and the amendment has a real text-only UX clarity concern.
Validation target: Rerun lifecycle validation, review-artifact validation, change metadata validation, whitespace checks, and spec-review.
Validation evidence: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check -- ...` passed after the spec revision.
