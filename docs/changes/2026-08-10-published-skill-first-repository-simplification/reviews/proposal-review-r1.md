# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: independent Codex proposal-review peer
Target: docs/proposals/2026-08-10-published-skill-first-repository-simplification.md
Reviewed artifact: docs/proposals/2026-08-10-published-skill-first-repository-simplification.md
Review date: 2026-08-10
Status: changes-requested
Recording status: recorded
Material findings: PSR-PR1-001
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PSR-PR1-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-resolution.md`
- Open blockers: PSR-PR1-001
- Immediate next stage: proposal revision

## Material Findings

## Finding PSR-PR1-001

Finding ID: PSR-PR1-001
Severity: major
Location: `Recommended Direction`, canonical skill quality gate; `Testing and Verification Strategy`
Evidence: The proposal makes published skills the primary product boundary, but its four gates prove static skill structure, package parity, clean installation, and release integrity. It delegates semantic prose quality to human review without defining a durable product-level behavior evaluation. A skill can therefore package and install perfectly while failing representative routing, resource-use, stage-boundary, or claim-boundary journeys. The current `specs/skill-contract.md` already distinguishes structural validation from routing fixtures and transcript review, so static validity is not sufficient evidence of published-skill effectiveness.
Required outcome: Add an explicit published-skill behavior proof surface to the recommended direction and verification strategy, with representative user journeys, durable review evidence, and a clear boundary between deterministic checks and human or model-based evaluation.
Safe resolution path: Expand the canonical skill quality gate rather than adding another standalone validator. Require a small versioned journey set covering routing-description behavior, resource use, stage ownership, stop conditions, and claim boundaries. Let deterministic checks validate fixture shape and stable mappings only; record reviewed transcript or equivalent behavior evidence for changed core skills and release-required coverage. State that packaging parity and installation smoke do not substitute for this behavior proof.
needs-decision rationale: none; this correction preserves the selected product-first direction and does not require a new product choice.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The maintenance imbalance and self-reinforcing validation problem are concrete and supported by current counts. |
| User value | pass | A smaller product-oriented contribution and release surface has clear maintainer and adopter value. |
| Option diversity | pass | Deferral, freeze-only, consolidation, tooling separation, and a broad reset are meaningfully compared. |
| Decision rationale | pass | The freeze plus bounded consolidation follows safety, rollback, and product-boundary criteria. |
| Scope control | pass | Bulk deletion, workflow-automation retirement, repository splitting, and publication are explicitly excluded or separately routed. |
| Architecture awareness | pass | Skills, generation, installation, lifecycle governance, CI, and release ownership boundaries are visible. |
| Testability | block | The primary product has no explicit behavior-evaluation proof beyond static and packaging checks. |
| Risk honesty | concern | Hidden safety loss is covered, but semantic product-quality loss is not tied to a durable proof surface. |
| Rollout realism | pass | Old-versus-new execution and slice-level rollback are credible without destructive migration. |
| Readiness for spec | block | The spec cannot define sufficient product gates until PSR-PR1-001 is resolved and rereviewed. |

## Scope Preservation Review

- Scope-preservation result: pass.
- Repository simplification, published-skill priority, validator-growth control, and retention of necessary scripts are all classified as in scope.
- Branch creation and the requested proposal/review workflow are also explicitly preserved.
- Automatic-workflow retirement is routed to a separate proposal instead of disappearing from scope without rationale.

## Recommended Proposal Edits

- Recommended edits: revise the canonical skill quality gate to include a small published-skill behavior evaluation rather than creating a fifth standalone script family.
- Add representative journeys and durable reviewed behavior evidence to `Testing and Verification Strategy`.
- Add semantic behavior loss to `Risks and Mitigations` and require the old-versus-new coverage matrix to include behavior evidence, not only accepted and rejected structural fixtures.
- Clarify in `Expected Behavior Changes` that installation and byte parity prove delivery, while behavior evaluation proves usefulness and contract adherence.
- Normalize the scope-budget treatment for one-step bulk deletion to an allowed value during revision; this is editorial and not a separate material finding because the current intent is unambiguous.

## Recommendation

- Recommendation: changes-requested. Preserve the selected published-skill-first consolidation direction, add an explicit behavior-proof surface inside the canonical skill quality gate, then run proposal-review R2 before specification. This review is isolated: no automatic downstream handoff occurred, the required record was created before fixing, and no owner decision is needed.
