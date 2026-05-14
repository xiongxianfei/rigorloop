# Cost-Bounded Rigor First Slice Explain-Change

## Summary

This change implements the first slice of cost-bounded rigor: broad proposals now get explicit scope-budget guidance, proposal-review now checks broad-scope classification, and `docs/workflows.md` now owns the bounded-evidence path/state discovery rule.

The implementation intentionally stops short of selector behavior, release validation, adapter packaging, lifecycle token-cost summary artifacts, dynamic benchmark requirements, and full progressive-loading work. The goal was to reduce early workflow amplification without weakening review, verification, material-finding, release, or full-file-read safety rules.

## Problem

After the single-authored skill source and follow-up ownership work, the remaining cost problem was workflow amplification:

- broad or multi-workstream proposals carrying too much work downstream;
- proposal reviews approving broad scope without explicit classification;
- broad path and state searches before exact paths, active state, metadata, headings, counts, line ranges, or diffs were tried.

The approved first slice addresses those early multipliers before later validation-budget, lifecycle-cost-summary, or progressive-loading work.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Adopt cost-bounded rigor as "smallest sufficient decision, evidence, artifact set, and validation set." |
| Proposal review | Narrow the first slice, keep scope-budget broadness as proposal/proposal-review judgment, add do-not-under-read wording, defer lifecycle token-cost summary details, and avoid absorbing progressive-loading work. |
| Spec | Requirements `R1` through `R19b` define M1 as proposal guidance, proposal-review guidance, `docs/workflows.md`, focused static proof, and lifecycle bookkeeping only. |
| Test spec | Tests `T1` through `T11` map the requirements to static phrase checks, manual review, selected validation, lifecycle validation, and warning-only token measurement. |
| Architecture | Not required. The approved scope changes workflow guidance and static proof, not runtime architecture, APIs, persistence, deployment, security boundaries, or hard-to-reverse data flow. |
| Plan | M1 covers proposal scope-budget guidance, proposal-review scope-budget review, workflow bounded-evidence wording, focused static proof, validation, and lifecycle state sync. |
| Code review | `code-review-r1` reviewed commit `dc59864bdc4f36a248be573c551b553c501dd0d6` and returned `clean-with-notes` with no material findings. |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/proposal/SKILL.md` | Added scope-budget trigger, table shape, treatment values, small-proposal exemption, follow-up routing, and single-source skill boundaries. | Broad proposals need to classify current work, later slices, follow-ups, separate proposals, and exclusions before downstream reliance. | Spec `R3`-`R7b`; test spec `T2`, `T3`, `T5`. | `test_cost_bounded_rigor_m1_proposal_scope_budget_guidance`; code-review `clean-with-notes`. |
| `skills/proposal-review/SKILL.md` | Added scope-budget review checks and `changes-requested` outcomes for missing or misleading classification, hidden follow-ups, silent narrowing, blank treatment/reason cells, omitted routing, and misleading treatment values. | Proposal-review owns semantic broadness judgment in the first slice; validators must not infer broadness. | Spec `R8`-`R11b`; test spec `T4`, `T5`. | `test_cost_bounded_rigor_m1_proposal_review_scope_budget_guidance`; code-review `clean-with-notes`. |
| `docs/workflows.md` | Added the bounded evidence sequence for path/state discovery, broad-search discouragement, and the do-not-under-read escape. | `docs/workflows.md` remains the full project-local guide for artifact locations, follow-up routing, and bounded-evidence behavior. | Spec `R12`-`R15b`, `R16a`; test spec `T6`, `T7`. | `test_cost_bounded_rigor_m1_workflows_bounded_evidence_guidance`; selected CI passed. |
| `scripts/test-skill-validator.py` | Added three focused static checks for stable M1 wording. | The first slice needed proof without adding broad semantic validators or natural-language scoring. | Spec `R11`-`R11b`, `R16`; test spec `T2`-`T8`. | Focused checks failed before implementation for missing wording and passed after implementation; full skill-validator suite passed. |
| Proposal/spec/test-spec/plan/change-local artifacts | Recorded accepted proposal, approved spec, active maintainer-approved test spec, reviewed active plan, validation evidence, and lifecycle handoffs. | The repository workflow requires durable artifacts and synchronized state for non-trivial workflow-governance changes. | Spec `R19`-`R19b`; test spec `T10`, `T11`; plan validation notes. | Artifact lifecycle, review-artifact, and change-metadata validation passed. |
| `reviews/code-review-r1.md` and `review-log.md` | Recorded a clean first-pass implementation review for M1. | Formal lifecycle reviews require durable review evidence even when there are no material findings. | Code-review skill; workflow review-recording rules. | `validate-review-artifacts.py --mode closeout` passed. |

## Tests Added Or Changed

`scripts/test-skill-validator.py` gained focused checks for:

- proposal scope-budget triggers, table shape, treatment values, follow-up routing, and single-source skill boundaries;
- proposal-review scope-budget review behavior, `changes-requested` outcomes, small-proposal exemption, and non-standard treatment handling;
- workflow bounded-evidence guidance, path/state sequence, do-not-under-read escape, and no copied full evidence sequence in proposal/proposal-review skills.

These are static phrase and shape checks by design. They do not infer whether a real proposal is broad, and they do not fail a proposal solely because it lacks a `Scope budget` heading.

## Validation Evidence Available Before Final Verify

Implementation validation passed:

- `python scripts/test-skill-validator.py SkillValidatorFixtureTests.test_cost_bounded_rigor_m1_proposal_scope_budget_guidance SkillValidatorFixtureTests.test_cost_bounded_rigor_m1_proposal_review_scope_budget_guidance SkillValidatorFixtureTests.test_cost_bounded_rigor_m1_workflows_bounded_evidence_guidance` failed before implementation for the expected missing guidance, then passed after implementation.
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/measure-skill-tokens.py`
- `python scripts/select-validation.py --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path docs/workflows.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`
- `bash scripts/ci.sh --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path docs/workflows.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`

Code-review recording validation passed:

- `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md`
- `python scripts/test-change-metadata-validator.py`
- `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`

Static token measurement was diagnostic only. No before/after dynamic benchmark comparison was required because the accepted first slice changes proposal/evidence wording and no runtime benchmark surface.

Final `verify` has not run yet. Hosted CI status is not claimed here.

## Review Resolution Summary

`review-resolution.md` is closed.

- `proposal-review-r2`: six material findings, all accepted and closed.
- `spec-review-r1`: inconclusive missing-spec stop condition closed by creating `specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`; later `spec-review-r2` approved the spec.
- `code-review-r1`: clean-with-notes, no material findings, no review-resolution entry required.

## Alternatives Rejected

- Hard token gates were not added because the proposal and spec keep token measurement diagnostic until enough comparable lifecycle data exists.
- Selector broadness inference was not added because broadness is semantic and belongs to proposal/proposal-review judgment in the first slice.
- Lifecycle token-cost summary artifacts were not added because they are a deferred conditional diagnostic feature.
- Release validation, adapter packaging validation, generated public adapter bodies, and dynamic benchmark comparison were not added because M1 did not touch their trigger surfaces.
- Full progressive-loading work for `workflow`, `implement`, and `code-review` was not absorbed into this slice.

## Scope Control

Preserved non-goals:

- no validation-selector behavior change;
- no broad-smoke trigger change;
- no release validation or adapter packaging change;
- no lifecycle token-cost summary artifact;
- no dynamic benchmark requirement;
- no full progressive-loading implementation;
- no generated public adapter skill body reintroduction;
- no weakening of formal review, verify, PR, material-finding, release, or full-file-read guidance.

Unrelated local README, project-map, selector, and `docs/workflows.md` project-map row changes are not justified by this explain-change because they are not part of the M1 implementation commits.

## Risks And Follow-Ups

Remaining risks are guidance-interpretation risks, not runtime risks:

- contributors could over-apply scope budgets to small proposals despite the explicit exemption;
- agents could under-read if they ignore the explicit full-file-read escape;
- future slices could accidentally pull validation-budget or lifecycle-cost reporting into unrelated work.

No new follow-up is required for M1. Later accepted slices already own validation-budget guidance, lifecycle token-cost summary design, and progressive-loading follow-through if maintainers choose to proceed.

## Readiness

This explain-change records the durable rationale required before final verification.

Next stage: `verify`.
