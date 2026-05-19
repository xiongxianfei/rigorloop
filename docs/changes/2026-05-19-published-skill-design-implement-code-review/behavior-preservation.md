# Published Skill Design Implement And Code-Review Behavior Preservation

Change: `2026-05-19-published-skill-design-implement-code-review`

## Purpose

This file tracks behavior-significant wording before and after the M3 rewrite.
M1 records the preservation targets. M3 must fill final evidence for any moved,
removed, or rewritten behavior-significant wording.

## Preservation Targets

| Skill | Behavior area | Baseline rule to preserve | M3 result |
|---|---|---|---|
| `implement` | Scope | Implement one approved milestone as the smallest scope-complete change. | Pending M3. |
| `implement` | Tests/proof first | Write or update tests/proof surfaces before implementation when feasible, and validate before handoff. | Pending M3. |
| `implement` | First-pass completeness | Address all in-scope requirements, required surfaces, edge cases, and targeted validation before code-review handoff. | Pending M3. |
| `implement` | Plan ownership | Keep active plan progress, decisions, discoveries, and validation notes current during execution. | Pending M3. |
| `implement` | Milestone handoff | Move the current implementation milestone to `review-requested` only after implementation and targeted validation complete. | Pending M3. |
| `implement` | Claim boundaries | Do not claim review passed, branch-ready, PR-ready, final closeout readiness, or generated-output currency without owning evidence. | Pending M3. |
| `code-review` | Independence | Review actual diff or changed files against governing artifacts, tests, and validation evidence; do not review from memory. | Pending M3. |
| `code-review` | First-pass record | Produce a first-pass review record before review-driven fixes or review-resolution. | Pending M3. |
| `code-review` | Finding shape | Material findings include evidence, required outcome, and safe resolution path or `needs-decision`. | Pending M3. |
| `code-review` | Recording | Clean formal reviews create a clean receipt; material findings create detailed review records and review-resolution dispositions. | Pending M3. |
| `code-review` | Direct proof | Named edge cases require direct proof from targeted tests, validation output, or allowed manual notes. | Pending M3. |
| `code-review` | Handoff | Clean non-final reviews close only that milestone; final closeout waits until all implementation milestones and required review-resolution are closed. | Pending M3. |
| `code-review` | Claim boundaries | Do not claim CI, verification, branch-ready, PR-ready, or implementation fixes unless separately owned. | Pending M3. |

## M1 No-Change Evidence

M1 does not change canonical skill bodies. All behavior preservation rows are
pending final M3 evidence.
