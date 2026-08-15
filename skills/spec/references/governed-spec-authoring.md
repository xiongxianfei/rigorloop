# Governed spec authoring

Load for `single-governed-candidate`; the parent owns universal policy and this reference governed transactions.

## Authority and writes

Read the complete current `change.yaml`. Require `lifecycle_contract: stage-owned-change-local-v1`, exact entry/path, settled inputs, accepted proposal when applicable, and legal state. Bind change ID, artifact ID, normalized canonical path, governing input identities, authoring-evidence path, retry identity, and operation before writing; conflict stops without portable fallback.

Write only spec, evidence, and matching transition; must not change `workflow_state`, routing, automation, review, other entries, or downstream state.

## Create-primary-spec

`create-primary-spec` requires absent entry/file and no competing primary. Create only the matching `authoring` entry; validate the complete spec; record content identity and evidence; move it to `review-required` as the commit point.

## Revise-primary-spec

`revise-primary-spec` binds prior content identity and exact reopen, finding, upstream-change, or revision authority. Preserve historical authoring and review evidence; clear only authorized review; record new identity/evidence; return only the matching entry to `review-required` for fresh `spec-review`. Downstream reliance first requires workflow impact, staleness handling, and legal reopen.

## Identical retry and stale detection

Identical interruption resumes at the first incomplete step; matching `review-required` completion is idempotent success without duplicate evidence or transition. Mismatched basis, unrelated asymmetry, path, stale authority, ambiguity, multiple primaries, or concurrency stops without adoption or overwrite.

Changed basis reports `stale-authoring-attempt` without overwrite, rebinding, evidence-pointer update, or new operation; detection grants no restart authority.

## Restart-stale-authoring

`restart-stale-authoring` applies to the same incomplete `authoring` entry under an explicit current user instruction or same-change workflow handoff naming the attempt and new basis. Validate artifact kind, artifact role, normalized path, old retry identity/inputs, new inputs, current authority, no review, reliance, or competition, and attributable content.

Evidence records authority source/request identity, old retry identity and governing input identities, new retry identity and governing input identities, and content state/identity.

| Partial content | Required disposition |
| --- | --- |
| File absent | Record `absent`; no snapshot. |
| Matching zero-byte file | Record `empty` and its identity. |
| Matching nonempty file | Preserve exact bytes and hash at a distinct change-local evidence path before replacement. |
| Unknown, unrelated, competing, or unpreservable file | Stop unchanged. |

The snapshot is byte-for-byte evidence. Restart writes only the same canonical spec file, new evidence, matching `authoring_evidence` pointer, and required snapshot. Preserve entry ID, artifact kind, artifact role, path, completed authoring and review evidence, and `authoring` state; do not change review mappings, other entries, or downstream artifacts. Restart leaves the entry in `authoring`; ordinary authoring commits `review-required`.

New schema, state, persistent authority, cross-stage mutation, or owner requires architecture and workflow-contract revision.

## Result and handoff

Completion ends at `review-required`; hand off to `spec-review` with identity, recovery, and blockers.
