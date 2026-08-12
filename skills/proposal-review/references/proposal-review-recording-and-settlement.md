# Proposal-review recording and settlement

Load this reference exactly when `durable_recording_context` is true. The parent skill remains the owner of judgment, materiality, mode classification, statuses, claims, stops, result applicability, and handoff. Loading this procedure grants no authority.

## Recording procedure

Use the classified recording and automation modes. `none` never enters this reference. `advisory-durable/manual`, `formal-lifecycle/manual`, and `formal-lifecycle/workflow-managed-automated` are valid; every other automated pair stops before writes.

### Location and record selection

Clean non-formal recording explicitly requested by the user may use a valid user path or project-local advisory location and stays standalone. Material, non-approval, blocked, inconclusive, and formal recording follows the formal-review-recording change-ID order:

1. existing active owning root;
2. reviewed-artifact metadata;
3. explicit user change ID;
4. generated `YYYY-MM-DD-<subject>-review-recording` fallback.

Ambiguous identity, unrelated-root collision, unsafe path, or write failure blocks recording. Keep the complete findings in the invocation result and claim neither recording nor formal completion.

A generated fallback creates only the minimal recording-only root required by the formal-review-recording contract. It grants no proposal settlement, workflow activation, automation, or continuation authority.

Create a lightweight clean receipt for clean formal review and index it in `review-log.md`; do not create empty resolution. Create a detailed record for material or blocking outcomes, synchronize the log, and create `review-resolution.md` only when disposition is required. Use `assets/material-finding.md` once per finding and `assets/review-result-skeleton.md` for the result.

Retry an identical interrupted write by reconciling and completing it exactly once. Do not duplicate a receipt, finding, resolution, or log entry. Conflicting reuse of a review ID for another target, identity, or result stops without mutation.

## Advisory-durable completion

`advisory-durable/manual` may write only the explicitly authorized standalone review or required finding evidence. It must not update a formal review log unless the resolved owning root requires that log, create lifecycle settlement, report formal next-stage eligibility, advance workflow, or write automation evidence.

When no valid location can be resolved, report `Recording status: blocked`, the exact blocker, and the smallest location decision needed. Do not create governed lifecycle authority merely to satisfy advisory recording.

## Formal lifecycle settlement

Run only in `formal-lifecycle`. Write the durable review evidence first. Then read complete `change.yaml`, require `lifecycle_contract: stage-owned-change-local-v1`, and resolve exactly one proposal entry by artifact ID, `kind`, and normalized path. Require current review authority and complete authoring evidence.

Set only the exact proposal review mapping with `id`, `artifact_id`, `outcome`, `record`, and `round`, remove matching authoring evidence when the governing lifecycle contract requires it, and map `approved` to `accepted`, `changes-requested` to `revision-required`, and `blocked` or `inconclusive` to `blocked`. Preserve every other artifact entry, milestone, and workflow field.

Formal settlement must not advance workflow. Retry identical incomplete settlement without rerunning review; conflicting review-ID reuse, mismatched identity, illegal transition, stale evidence, or failed available metadata validation stops without unrelated mutation.

## Change-record review settlement

The formal procedure above must read the complete `change.yaml`, require `lifecycle_contract: stage-owned-change-local-v1`, Require `review-required` and complete authoring evidence, Write the durable review record first, remove `authoring_evidence`, and write only `id`, `artifact_id`, `outcome`, `record`, and `round`. It maps `approved` to `accepted`, `changes-requested` to `revision-required`, and `blocked` or `inconclusive` to `blocked`. Retry identical incomplete settlement without rerunning the review, stop on failed available change-metadata validation, and stops without advancing routing.

## Workflow-managed automated review

Run only in `formal-lifecycle/workflow-managed-automated` with current same-change authorization. Reset context to the tracked proposal, governing sources, formal criteria, and relevant recorded findings; do not rely on hidden authoring reasoning or edit the proposal during review.

For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review.

Use a neutral packet, record the independent first-pass result before correction classification, and produce ordered phase receipts. Only separately authorized mechanical or declared-safe corrections may run; each stays within named surfaces, reruns named proof, records the cycle, and returns to independent rereview. Pause on blocked or inconclusive results, owner decisions, scope expansion, new finding classes, non-shrinking correction, stale identity, or exhausted bounds.

Automation records packet, receipt, correction, pause, and promotion evidence only. It invokes but does not redefine formal settlement or workflow continuation. After valid settlement and automation receipts, return control to workflow; this procedure must not advance workflow itself.

## Resource failure

If this reference or a required asset is unavailable, unreadable, contradictory, escaped, or mixed-version, stop before its dependent write or claim. Preserve findings in the diagnostic and do not reconstruct procedure from memory.
