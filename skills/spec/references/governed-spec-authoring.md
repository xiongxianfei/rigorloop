# Governed spec authoring

Load only for `single-governed-candidate`. The parent owns universal policy; this reference owns governed transactions.

## Authority and writes

Read the complete current `change.yaml`. Require `lifecycle_contract: stage-owned-change-local-v1`; resolve operation, artifact ID, normalized canonical path, inputs, authoring-evidence path, and authority; validate proposal settlement. Conflict stops without portable fallback.

Write only the spec, evidence, and matching entry transition; it must not change `workflow_state`, routing, automation, peer review, other entries, or downstream state.

## Create-primary-spec

`create-primary-spec` requires an absent entry and file, deterministic path, no competing primary, and bound identities. Create the `authoring` entry, write and identify valid content, record evidence, then move only that entry to `review-required` as the commit point. Matching completion returns idempotent success without duplication.

## Revise-primary-spec

`revise-primary-spec` requires prior identity and exact reopen, finding, upstream-change, or revision authority. Preserve history; clear only the authorized review mapping, record new identity and evidence, and return to `review-required` for fresh `spec-review`. Downstream reliance requires workflow impact handling; stale, mismatched, lossy, competing, or ambiguous state stops.

## Identical retry and stale detection

Retry identity binds change, artifact, path, inputs, evidence, and prior revision identity. Identical interruption resumes and identical completion is idempotent success; changed, unrelated, stale, ambiguous, or concurrent state stops without adoption. Changed basis reports `stale-authoring-attempt` and writes nothing; detection grants no restart authority.

## Restart-stale-authoring

`restart-stale-authoring` applies to the same incomplete `authoring` entry and requires an explicit current user instruction or same-change workflow handoff naming the attempt and new basis. Require the exact entry, both bases, no reliance or competition, and attributable content; record authority, old/new identities and inputs, and content state.

| Partial content | Required disposition |
| --- | --- |
| File absent | Record `absent`; no snapshot. |
| Matching zero-byte file | Record `empty` and its identity. |
| Matching nonempty file | Preserve exact bytes and hash at a distinct change-local evidence path before replacement. |
| Unknown, unrelated, competing, or unpreservable file | Stop unchanged. |

The snapshot is byte-for-byte evidence. Restart writes only the canonical spec, new evidence, matching `authoring_evidence` pointer, and required snapshot. It preserves identity, history, and state; it must not change `workflow_state`, routing, automation, review mappings, other entries, or downstream artifacts. Restart leaves the entry in `authoring`; ordinary authoring commits `review-required`. New schema, state, authority, cross-stage mutation, or owner requires architecture and workflow-contract revision.

## Result and handoff

Completed work ends at `review-required` and hands off to `spec-review`; report identity, recovery, validation, and blockers.
