# Governed proposal authoring

Load only for `governed_proposal_candidate_context`. It owns governed authoring, not selection, judgment, gates, review settlement, routing, or claims.

## Authority validation

Validate the complete `change.yaml`, exact change, `lifecycle_contract: stage-owned-change-local-v1`, prerequisites, inputs, proposal identity/path, and legal state. Resolve one proposal entry by artifact ID, `kind`, and path. Candidate loading grants no writes; invalid authority stops without portable fallback.

## Change-record authoring transition

For governed work, read the complete `change.yaml` before writing and require `lifecycle_contract: stage-owned-change-local-v1`. Resolve the proposal entry by artifact ID, `kind`, and normalized `path`; for valid creation, create only that entry with a unique stable ID and `kind: proposal`. Set only the matching entry to `authoring`, remove any prior `review` only when revision authority permits it, bind `authoring_evidence`, and commit only at `review-required`. Preserve every other entry and stop on failed available change-metadata validation.

## Operation identity

`create-primary-proposal` binds change, artifact, normalized path, inputs, evidence path, and transaction identity. `revise-primary-proposal` also binds prior content and exact finding, upstream change, reopen, or revision authority. Mismatch, ambiguity, stale authority, or competing writes stop without adoption.

## Creation transaction

Creation requires absent entry and file. Create the matching `authoring` entry, write and validate content, record identity and evidence, then transition it to `review-required` as the commit point. Preserve all other state.

## Revision transaction

Revision requires matching entry/file identity and current authority. Downstream reliance requires workflow impact handling and explicit reopen. Preserve history, clear only the authorized current review mapping, record new content and evidence, and return only the matching entry to `review-required` for fresh review.

## Retry and concurrency

An identical interruption resumes at the first incomplete step; exact completion is idempotent success. Re-read before writes and stop on identity, path, basis, authority, or concurrency change. Never adopt partial matches.

## Stale-authoring reset

Changed partial `authoring` returns `authoring-reset-required` without mutation. Workflow validates identity and no reliance, authorizes reset, and routes recovery without mutating proposal-owned state.

Workflow reset authorization identifies the change, artifact, transaction, path, evidence, allowed surfaces, and authorization identity. It is current, identity-bound, single-use or idempotently consumable, and invalidated by identity, reliance, or write changes.

With exact authorization, reset only the matching incomplete entry and proposal-authored evidence. It must not mutate `workflow_state` or other surfaces and must not delete completed authoring or review evidence. Exact replay is idempotent; unsafe state stops. A later operation uses a new transaction identity, evidence path, and basis.

This handshake adds no lifecycle state, persistence mechanism, evidence type, or write owner. If safe recovery requires workflow to mutate proposal-owned state or any broader contract, stop and route to architecture and workflow-contract revision.
