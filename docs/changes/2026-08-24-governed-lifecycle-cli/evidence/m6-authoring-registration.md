# M6 Authoring Registration Evidence

Milestone: M6
Validation result: passed
Subject: commit `aaa298a9`

## Delivered

- Added the closed `record-artifact-revision` operation for proposal, spec, architecture, ADR, plan, and test-spec creation or revision.
- Bound authoring evidence to the exact artifact path and SHA-256, required the owning stage authority, and required the registered prior identity on revision.
- Derived `review-required`, invalidated review/validation/resolution registrations for replaced bytes, and left workflow routing unchanged.
- Seeded supported current artifact and available authoring-evidence identities during migration without changing settlement state.

## Proof

- `node --test packages/rigorloop/test/lifecycle-artifact-revision.test.js packages/rigorloop/test/lifecycle-migration-repair.test.js`: passed, 4 tests.
- `npm test --prefix packages/rigorloop`: passed, 159 tests.

Direct review found and corrected two pre-closeout gaps: authoring evidence initially was not required to bind the exact completed artifact, and migration initially left existing artifacts without the prior identity needed for their first later revision.
