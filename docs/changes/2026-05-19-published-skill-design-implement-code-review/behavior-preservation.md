# Published Skill Design Implement And Code-Review Behavior Preservation

Change: `2026-05-19-published-skill-design-implement-code-review`

## Purpose

This file tracks behavior-significant wording before and after the M3 rewrite.
M1 records the preservation targets. M3 must fill final evidence for any moved,
removed, or rewritten behavior-significant wording.

## Preservation Targets

| Skill | Behavior area | Baseline rule to preserve | M3 result |
|---|---|---|---|
| `implement` | Scope | Implement one approved milestone as the smallest scope-complete change. | Preserved in `Purpose`, `First-pass completeness`, `Scope rules`, and `Workflow role`; description now routes to one approved milestone or isolated request without broadening scope. |
| `implement` | Tests/proof first | Write or update tests/proof surfaces before implementation when feasible, and validate before handoff. | Preserved in `Quick operating guide`, `Implementation loop`, `TDD rules`, and `Output skeleton`; M3 added the regression test before skill edits. |
| `implement` | First-pass completeness | Address all in-scope requirements, required surfaces, edge cases, and targeted validation before code-review handoff. | Preserved unchanged in `First-pass completeness`; output wording now reports same-slice coverage without claiming review results. |
| `implement` | Plan ownership | Keep active plan progress, decisions, discoveries, and validation notes current during execution. | Preserved in opening guidance, `Plan update requirements`, and `Output skeleton` plan updates field. |
| `implement` | Milestone handoff | Move the current implementation milestone to `review-requested` only after implementation and targeted validation complete. | Preserved in `Milestone-aware handoff`, `Stop conditions`, and result skeleton `Milestone state: review-requested | blocked`. |
| `implement` | Claim boundaries | Do not claim review passed, branch-ready, PR-ready, final closeout readiness, or generated-output currency without owning evidence. | Preserved and made more visible in `Workflow role`, `Claims this skill must not make`, `Workflow handoff`, and `Expected output`. |
| `code-review` | Independence | Review actual diff or changed files against governing artifacts, tests, and validation evidence; do not review from memory. | Preserved in `Quick operating guide`, `Inputs to read`, `Independent-review mode`, and `Rules`; description now routes from actual diff and evidence. |
| `code-review` | First-pass record | Produce a first-pass review record before review-driven fixes or review-resolution. | Preserved in `Outputs`, `Rules`, `Workflow handoff behavior`, `Recommended clean review template`, and `Output skeleton`. |
| `code-review` | Finding shape | Material findings include evidence, required outcome, and safe resolution path or `needs-decision`. | Preserved in `Material findings`, `Isolation and Recording`, and `Output skeleton` findings placeholder. |
| `code-review` | Recording | Clean formal reviews create a clean receipt; material findings create detailed review records and review-resolution dispositions. | Preserved in `Isolation and Recording` and result skeleton fields for recording status, review record, review log, and review resolution. |
| `code-review` | Direct proof | Named edge cases require direct proof from targeted tests, validation output, or allowed manual notes. | Preserved in `Direct proof for named edge cases`; no rewrite weakened the proof source requirement. |
| `code-review` | Handoff | Clean non-final reviews close only that milestone; final closeout waits until all implementation milestones and required review-resolution are closed. | Preserved in `Handoff`, `Milestone-aware review handoff`, `Plan closeout check`, and result skeleton milestone fields. |
| `code-review` | Claim boundaries | Do not claim CI, verification, branch-ready, PR-ready, or implementation fixes unless separately owned. | Preserved and made more visible in `Workflow role`, `Claims this skill must not make`, and `Expected output`. |

## M1 No-Change Evidence

M1 does not change canonical skill bodies. All behavior preservation rows are
pending final M3 evidence.

## M3 Preservation Result

M3 preserves the behavior-significant implementation and review contracts while
moving routing into frontmatter descriptions, adding explicit workflow-role
blocks, and adding compact output skeletons. `python scripts/test-skill-validator.py`
and `python scripts/validate-skills.py` pass after the rewrite.
