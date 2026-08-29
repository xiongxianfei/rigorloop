# M2 Aggregate Review Package Implementation Evidence

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M2
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Subject identity: sha256:353734d3bc315fcd24134bb452dd2d00d2fc344aed34058a84c9a6e3a2b759ee
Validation result: pass

## Scope

M2 adds exact design and delivery package identities, bounded package context, durable package-review registration, and atomic package settlement. It does not activate consolidated routing; the current workflow remains authoritative until the later single cutover.

## Implemented result

- Design membership resolves one primary architecture artifact, one primary specification, and all registered supporting ADRs in deterministic artifact-ID order.
- Delivery membership resolves one primary plan followed by one primary test specification.
- `review-package-sha256-v1` binds package kind, ordered member IDs, current member bytes, and the exact upstream approval identity while keeping per-member hashes transient.
- `record-package-review` binds durable review evidence to the calculated package revision; `settle-review-package` atomically writes one compact package projection.
- Package findings use closed artifact-local, cross-artifact, or upstream-direction scopes and retain affected artifact IDs and correction owners.
- Approved outcomes grant package authority. Changes-requested, blocked, and inconclusive outcomes remain visible and withhold authority.
- Status and review context expose member IDs, upstream binding, aggregate revision, state, staleness, blockers, and the next operation without storing document hashes in authored documents.

## Aggregate identity vector

For the fixed design fixture with member IDs `architecture`, `spec`, and `adr-cache`, fixture bytes `# Architecture\n`, `# Specification\n`, and `# ADR cache\n`, and upstream binding `proposal-review-r1`, the aggregate revision is:

`sha256:77973cd683195f8c9b468ebff64e0cf1055fe0a093309ab4469507d033afda46`

The focused suite proves that a member-byte change, an added ordered ADR member, or a changed proposal-review binding produces a different aggregate revision.

## Outcome and authority matrix

| Review outcome | Durable state | Authority |
| --- | --- | --- |
| approved | approved | granted |
| changes-requested | changes-requested | withheld |
| blocked | blocked | withheld |
| inconclusive | inconclusive | withheld |

Both design and delivery approved settlement paths are covered. The non-approved matrix is exercised through the same package evaluator and transaction boundary.

## Atomicity and recovery

Dry run preserves the original bytes, exact settlement replay returns `already-recorded`, stale member settlement returns `RL_STALE_EVIDENCE` without mutation, and injected package post-validation failure restores the complete prior authority. Existing transaction fixtures also prove deterministic recovery before and after replacement.

## Validation

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-evidence.test.js packages/rigorloop/test/lifecycle-transaction.test.js` — 61 passed.
- `npm test --prefix packages/rigorloop` — 285 passed.
- `python scripts/test-review-artifact-validator.py` — 104 passed.
- `python scripts/test-governed-lifecycle-cli-validator.py` — 5 passed.
- `python scripts/test-change-metadata-validator.py` — 66 passed.

## Compatibility boundary

The approved observability specification permits a later approved feature to evolve detailed lifecycle facts without retaining an obsolete output mode. The exact output fixture now includes compact `review_packages` facts; the detailed renderer and concise shared facts remain coherent.

## Handoff

M2 is ready for code review of package composition, identity, state projection, atomic settlement, finding attribution, and recovery. M3 consolidated workflow routing remains out of scope for this implementation receipt.
