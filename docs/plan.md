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
- [2026-05-25 Installed-Skill Artifact Placement Contract](plans/2026-05-25-installed-skill-artifact-placement-contract.md) - active execution plan for implementing portable installed-skill artifact placement contracts, change-pack-first review locality wording, workflow-map synchronization, deterministic drift validation, and generated-output/cold-read proof; M1 code-review requested changes for `SAP-M1-CR1`, so review-resolution is next.
- [2026-05-24 Cache-Aware Inner-Loop Lifecycle Validation Helper](plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md) - active execution plan for implementing `--mode explicit-paths-inner-loop` as a cache-aware inner-loop lifecycle validation helper while preserving direct actual-run closeout, CI, and PR-readiness boundaries; final verify passed from clean tracked branch state and PR handoff is next.
- [2026-05-22 Bounded Plan Index and Completed-Plan Archive](plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md) - branch-ready after final verify; PR #86 open for hosted CI and human review; blockers: none.
- [2026-05-21 Compact Change Validation Metadata](plans/2026-05-21-compact-change-validation-metadata.md) - active execution plan for implementing compact `schema_version: 2` change validation metadata while preserving legacy compatibility, exact command/path reconstruction, path-variable safety, stage-derived existence checks, review-artifact count cross-checks, and compactness proof; M1, M2, and M3 are closed after clean code reviews, ci-maintenance fixed selected-CI fixture routing, explain-change is refreshed, and final verify passed from clean tracked branch state; PR handoff is pending.
- [2026-05-20 Proposal-Family Assets Progressive Disclosure](plans/2026-05-20-proposal-family-assets-progressive-disclosure.md) - active execution plan for adding assets-only progressive disclosure to `proposal` and `proposal-review`; M2, M3, and M4 are closed after clean code reviews, explain-change and verify are recorded, and PR #81 is open for hosted CI and human review.

## Blocked
- none yet

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- [2026-05-23 Public Discovery and Developer Adoption Surface](plans/2026-05-23-public-discovery-and-developer-adoption-surface.md) - done; terminal state: done; PR #90 merged.
- [2026-05-23 Release Process Contract](plans/2026-05-23-release-process-contract.md) - done; terminal state: done; PR #89 merged.
- [2026-05-23 Validation Idempotency and Cache-Hit Safety](plans/2026-05-23-validation-idempotency-cache-hit-safety.md) - done; terminal state: done; PR #88 merged.
- [2026-05-22 Change-Record Catalog Registration and Bounded Read Model](plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md) - done; terminal state: done; PR #87 merged.
- [2026-05-22 Broad-Smoke and Fixture-Suite Output Compaction](plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md) - done; terminal state: done; PR #85 merged.
- [2026-05-21 Script Output Optimization](plans/2026-05-21-script-output-optimization.md) - done; terminal state: done; PR #83 merged.
- [2026-05-21 Review-Skill Family Consistency and Parser-Owned Finding Shape](plans/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md) - done; terminal state: done; PR #82 merged.
- [2026-05-20 Spec-Family Assets Progressive Disclosure](plans/2026-05-20-spec-family-assets-progressive-disclosure.md) - done; terminal state: done; PR #80 merged.
- [2026-05-20 Spec-Family Readability Pass](plans/2026-05-20-spec-family-readability-pass.md) - done; terminal state: done; PR #79 merged.
- [2026-05-20 Test-Spec Contract Normalization](plans/2026-05-20-test-spec-contract-normalization.md) - done; terminal state: done; PR #77 merged.

## Superseded
- none yet
