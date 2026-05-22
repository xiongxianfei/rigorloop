# Plan index

<!--
Index policy:
- Active and Blocked are complete and first.
- Done (recent) keeps the most recent 10 completed plans.
- Older Done entries move to docs/plan-archive.md.
- Done entries are one line: date, title, plan link, terminal state, PR/disposition.
- Do not place active, blocked, unresolved, or review-needed work in the archive.
-->

## Active
- [2026-05-22 Bounded Plan Index and Completed-Plan Archive](plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md) - M5 selection and CI routing implemented; next: code-review M5; blockers: none.
- [2026-05-21 Compact Change Validation Metadata](plans/2026-05-21-compact-change-validation-metadata.md) - active execution plan for implementing compact `schema_version: 2` change validation metadata while preserving legacy compatibility, exact command/path reconstruction, path-variable safety, stage-derived existence checks, review-artifact count cross-checks, and compactness proof; M1, M2, and M3 are closed after clean code reviews, ci-maintenance fixed selected-CI fixture routing, explain-change is refreshed, and final verify passed from clean tracked branch state; PR handoff is pending.
- [2026-05-20 Proposal-Family Assets Progressive Disclosure](plans/2026-05-20-proposal-family-assets-progressive-disclosure.md) - active execution plan for adding assets-only progressive disclosure to `proposal` and `proposal-review`; M2, M3, and M4 are closed after clean code reviews, explain-change and verify are recorded, and PR #81 is open for hosted CI and human review.

## Blocked
- none yet

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- [2026-05-21 Script Output Optimization](plans/2026-05-21-script-output-optimization.md) - done; terminal state: done; PR #83 merged.
- [2026-05-21 Review-Skill Family Consistency and Parser-Owned Finding Shape](plans/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md) - done; terminal state: done; PR #82 merged.
- [2026-05-20 Spec-Family Assets Progressive Disclosure](plans/2026-05-20-spec-family-assets-progressive-disclosure.md) - done; terminal state: done; PR #80 merged.
- [2026-05-20 Spec-Family Readability Pass](plans/2026-05-20-spec-family-readability-pass.md) - done; terminal state: done; PR #79 merged.
- [2026-05-20 Test-Spec Contract Normalization](plans/2026-05-20-test-spec-contract-normalization.md) - done; terminal state: done; PR #77 merged.
- [2026-05-19 Spec and Test-Spec Structural Hygiene](plans/2026-05-19-spec-and-test-spec-structural-hygiene.md) - done; terminal state: done; disposition recorded in plan body.
- [2026-05-19 Assets-First Progressive Disclosure Pilot](plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md) - done; terminal state: done; PR #75 passed hosted CI.
- [2026-05-19 Published Skill Design Plan Family Rollout](plans/2026-05-19-published-skill-design-plan-family.md) - done; terminal state: done; PR #74 merged.
- [2026-05-19 Published Skill Design Implement And Code-Review Rollout](plans/2026-05-19-published-skill-design-implement-code-review.md) - done; terminal state: done; PR #73 merged.
- [2026-05-19 Published Skill Design Spec Family Rollout](plans/2026-05-19-published-skill-design-spec-family.md) - done; terminal state: done; PR #72 merged.

## Superseded
- none yet
