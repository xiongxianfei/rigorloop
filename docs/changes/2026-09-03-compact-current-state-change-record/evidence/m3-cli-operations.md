# M3 implementation evidence: Compact semantic operations and CLI

Milestone: M3
Subject path: `docs/plans/2026-09-03-compact-current-state-change-record.md`
Subject identity: `sha256:0c18ba75e3139f28415889279a453f2769b963dc37dd5d96da565fda2da7f67e`
Validation result: passed

## Result

- Skill: implement
- Status: M3 implementation complete and ready for Code Review
- Completed scope: fourteen semantic operations; lifecycle-derived progression and operation eligibility; typed pending-milestone selection and derived active work; stable review and finding non-loss; material-decision maintenance; explicit correction route, return, rereview, and settlement; typed evidence invalidation and direct read-time subject drift detection; Verify-readiness coupling; bounded projections; argument, stdin, and temporary-file transports; explicit recovery status/action; and legacy compact-write/migration denial
- Public activation: withheld until M4 and M5 align canonical consumers and the released writer set
- Current dependency: approved Design Review R11 and Delivery Review R8
- Claim limitations: this evidence does not claim M4 canonical-contract alignment, M5 activation, final verification, release, push, or pull-request readiness

## Test-first evidence

Focused tests first exposed missing semantic-operation modules. The implementation then added one pure evaluator, one eligibility derivation, bounded projection composition, and a public adapter over the reviewed M2 transaction boundary. Review-driven corrections removed caller-constructed candidate state and compact migration, separated correction input from durable correction state, kept corrections active through exact review settlement, separated progression blockers from operation-specific eligibility, preserved every unselected stable-record entry, completed the exact eligibility predicates, and made the evaluator derive the complete expected-file set.

Additional boundary checks cover first artifact registration, exact selection of one typed pending milestone, invalid selection with unchanged state, deterministic stale selection retry, milestone closure without durable closed active work, cross-target correction rejection, exact review replacement during finding resolution, non-lossy finding, decision, and evidence updates, milestone closure against current approving Code Review, final Verify readiness and subject binding, evidence-subject expected-file binding, rejection of missing and extra expected inputs, public recovery identity discovery, canonical complete-set recovery validation, safe format rejection, and current identity drift without manifest mutation.

## Validation results

- `node --test packages/rigorloop/test/compact-operations.test.js packages/rigorloop/test/compact-cli.test.js packages/rigorloop/test/compact-migration.test.js` — passed, 32 tests.
- `npm test --prefix packages/rigorloop` — passed, 455 tests total: 453 passed and 2 historical skips.
- `python scripts/test-lifecycle-cli-conformance.py` — passed (`invalid=6`, `protected=10`).
- `python scripts/test-cli-result-measurement.py` — passed, 4 tests.
- `python scripts/validate-governed-lifecycle-cli.py` — passed for 38 governed changes with three reported baseline warnings and no failures or activation errors.
- `python scripts/validate-npm-package.py` — passed.
- `git diff --check` — passed.

## Contract evidence

- The public boundary is limited to projection, semantic application, and explicit recovery/status. All transports normalize into the same operation envelope and evaluator, and successful requests are not retained.
- Requests contain semantic intent and exact expected identities, not caller identity, claimed permission, derived correction status, `change.yaml`, or arbitrary candidate files.
- Stable review replacement preserves every open finding or requires a final disposition; a material disposition must resolve to current decision memory.
- Correction routing derives `authoring`, explicit return derives `review-required`, and only settlement of the exact required review can clear, revise, or block the correction.
- Evidence dependencies are typed. Mutations bind observed subject paths and atomically stale dependent evidence and final readiness; projections directly hash only selected declared subject paths and report bounded drift without mutating evidence.
- Operation eligibility is derived independently of overall progression readiness, so an open blocking finding can leave a safe exact correction route available without authorizing downstream progression.
- Exact edge selection admits active-milestone review handoff and finding-owned correction return while requiring current approving gate judgments, current artifact authoring status, explicitly selected CI/remaining work, or successful Verify readiness as applicable. Stable review paths and reviewer responsibilities are validated as complete-set invariants, review settlement derives artifact status, and decision/evidence maintenance checks exact current ownership or selection.
- When no work is active at `implement`, `advance-milestone` admits only an exact typed pending milestone with `from_status: null` and `to_status: planned`; the evaluator removes that remaining-work entry, derives the active milestone, rejects missing, blocked, wrong-kind, wrong-owner, or stale selections unchanged, and clears active work rather than storing a closed active milestone.
- Public recovery status exposes only the bounded recovery identity and safe next operation. Recovery restores or accepts only a canonically validated complete compact set and does not use Git, pull-request state, a network, or local logs.
- Legacy records retain their registered contract and remain readable through existing tooling; compact projection, writes, and migration reject for them.

## Recovery

M3's public command wiring and semantic modules can be removed together while retaining the reviewed M1 model and M2 transaction adapter. Compact creation and activation remain withheld, so no governed change currently depends on the candidate writer.
