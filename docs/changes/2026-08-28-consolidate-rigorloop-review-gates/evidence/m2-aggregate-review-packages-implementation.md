# M2 Explicit Review Package Implementation Evidence

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M2
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Subject identity: sha256:0f37ca539a8d2fdc10ad4b982d69c95fe379f04ca4383a78877de34fe1a090f6
Validation result: pass

## Scope

M2 implements explicit design and delivery package membership, bounded package context, durable package-review registration, governed invalidation, and atomic package settlement. It does not activate consolidated routing; the current workflow remains authoritative until the later single cutover.

## Implemented result

- Design membership exposes the exact architecture, specification, and applicable ADR artifact ID-to-path map.
- Delivery membership exposes the exact plan and test-specification artifact ID-to-path map.
- Package review evidence and lifecycle state bind that visible map, one upstream review ID, review ID, round, outcome, findings, and correction targets.
- No aggregate package revision, package member revision, or per-document hash is calculated, requested, displayed, or persisted for package authority.
- `record-artifact-revision` invalidates any approved package containing that artifact by setting its status to `review-required` and withholding authority while retaining the prior review ID as history.
- A replacement approved Design Review invalidates a dependent delivery package whose upstream review ID no longer matches.
- A replacement Proposal Review invalidates dependent design authority by changing its status to `review-required` and withholding authority while retaining the prior Design Review ID.
- Exact settlement replay rereads the registered review and review log before returning `already-recorded`; changed evidence returns `RL_STALE_EVIDENCE` without mutation.
- Direct filesystem edits outside governed authoring operations are intentionally not detected.
- Approved outcomes grant package authority. `changes-requested`, `blocked`, and `inconclusive` remain visible, blocking, and non-authorizing.
- Settled non-approved outcomes expose their safe continuation: correction routing when a correction target exists, no automatic operation for an unrouteable block, and review recording after inconclusive evidence is refreshed.
- Artifact-local, cross-artifact, and upstream-direction finding scopes retain affected artifact IDs and owning stages.

## Outcome and authority matrix

| Review outcome | Durable status | Authority | Next operation |
| --- | --- | --- | --- |
| approved | approved | granted | workflow continuation |
| changes-requested | changes-requested | withheld | correction and rereview |
| blocked | blocked | withheld | resolve the named prerequisite |
| inconclusive | inconclusive | withheld | obtain evidence and rereview |

## Atomicity and recovery

Dry run preserves original bytes, exact settlement replay returns `already-recorded`, mismatched member maps or upstream review IDs fail without mutation, and injected post-validation failure restores prior authority. The lifecycle revision remains the sole optimistic-concurrency identity for mutation.

## Validation

- `node --test packages/rigorloop/test/lifecycle-evidence.test.js` — 13 passed.
- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-evidence.test.js packages/rigorloop/test/lifecycle-transaction.test.js` — 64 passed.
- `npm test --prefix packages/rigorloop` — 289 passed.
- `python scripts/test-review-artifact-validator.py` — 104 passed.
- `python scripts/test-governed-lifecycle-cli-validator.py` — 5 passed.
- `python scripts/test-change-metadata-validator.py` — 66 passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates` — passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml` — passed.
- `git diff --check` — passed.

## Aligned and unaffected surfaces

- `schemas/change.schema.json`, the change-metadata validator, review-artifact validator, package fixtures, and observability compatibility fixture now use the explicit map model.
- Generic governed artifact and evidence hashes remain unchanged because they belong to the existing artifact lifecycle contract, not package authority.
- M3 routing, M4 skills/templates, generated adapters, and cutover remain unchanged and out of M2 scope.

## Handoff

M2 is ready for rereview of explicit membership, governed invalidation, deterministic non-approved authority, finding attribution, and atomic recovery. M3 remains paused until M2 closes cleanly.
