# Governed proposal authoring

Load only for `governed_proposal_candidate_context`. It owns governed authoring, not selection, judgment, gates, review settlement, routing, or claims.

## Authority validation

Validate the complete `change.yaml`, exact change, `lifecycle_contract: stage-owned-change-local-v1`, prerequisites, inputs, proposal identity/path, and legal state. Resolve one proposal entry by artifact ID, `kind`, and path. Candidate loading grants no writes; invalid authority stops without portable fallback.

## Change-record authoring transition

For governed work, read the complete `change.yaml` before writing and require `lifecycle_contract: stage-owned-change-local-v1`. Resolve by artifact ID, `kind`, and normalized `path`; create only that entry with a unique stable ID and `kind: proposal`. Set it to `authoring`, remove any prior `review` only with revision authority, bind `authoring_evidence`, and commit at `review-required`. Preserve every other entry and stop on failed available change-metadata validation.

## Operation identity

`create-primary-proposal` binds change, artifact, path, inputs, evidence, and transaction. `revise-primary-proposal` also binds prior content and exact revision authority. Mismatch, ambiguity, staleness, or concurrency stops without adoption.

## Creation transaction

Creation requires absent entry and file. Create the matching `authoring` entry, write and validate content, record identity and evidence, then transition it to `review-required` as the commit point. Preserve all other state.

## Revision transaction

Revision requires matching identity and authority. Downstream reliance requires workflow impact handling and reopen. Preserve history, clear only the authorized review mapping, record new content/evidence, and return the entry to `review-required`.

## Retry and concurrency

An identical interruption resumes at the first incomplete step; exact completion is idempotent success. Re-read before writes and stop on identity, path, basis, authority, or concurrency change. Never adopt partial matches.

## Stale-authoring reset

Changed partial `authoring` returns `authoring-reset-required`. Workflow proves identity and no reliance, authorizes reset, and routes without mutating proposal state.

Workflow reset authorization identifies change, artifact, transaction, path, evidence, allowed surfaces, and authority. It is identity-bound, single-use or idempotently consumable, and invalidated by reliance or write changes.

With exact authorization, reset only the matching incomplete entry/evidence. It must not mutate `workflow_state` or other surfaces and must not delete completed authoring or review evidence. Replay is idempotent; unsafe state stops. Later work uses a new transaction identity.

This handshake adds no lifecycle state, persistence mechanism, evidence type, or write owner. If safe recovery requires workflow to mutate proposal-owned state or any broader contract, stop and route to architecture and workflow-contract revision.
