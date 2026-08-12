# Governed spec-review settlement

Load this reference only after `governed-spec-entry` authority is established. The parent skill owns judgment, status, severity, materiality, recording, boundary activation, stops, claims, and handoff. Loading this procedure does not grant settlement, automation, correction, or continuation authority.

## Change-record review settlement

Run settlement only after universal review recording succeeds. Before settlement, read the complete `change.yaml` before writing and require `lifecycle_contract: stage-owned-change-local-v1`. Resolve exactly one spec entry by artifact ID, `kind`, and normalized reviewed path. Require `review-required` and complete authoring evidence, plus a lifecycle state that requests `spec-review`.

Write the durable review record first. Then remove `authoring_evidence`, set only the exact review mapping with `id`, `artifact_id`, `outcome`, `record`, and `round`, and map `approved` to `approved`, `changes-requested` to `revision-required`, and `blocked` or `inconclusive` to `blocked`. The procedure must settle only the matching spec entry. Preserve every other artifact entry, milestone, workflow route, and next-stage field.

Retry identical incomplete settlement without rerunning the review. Stop without unrelated mutation on ambiguity, stale evidence, mismatched identity, conflicting review-ID reuse, illegal transition, or failed available change-metadata validation.

An independent invocation stops without advancing routing. Workflow remains the sole continuation owner.

## Workflow-managed automation

Run this section only when current durable authorization matches the same governed change and spec entry. Automated mode shares the SR2 resource assembly; it is not another profile.

For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review.

During Phase 1 of independent automated review rollout, workflow-managed automated `spec-review` should at least record a review invocation manifest before automated handoff. This is manifest-only evidence for `spec-review`; it does not yet require the full blind-first automated review protocol unless a later approved slice adopts it. Direct or review-only `spec-review` requests remain isolated by default.

Use a neutral packet and ordered phase receipts. Only separately authorized mechanical or declared-safe corrections may run; each remains within named surfaces, reruns named proof, records the bounded cycle, and returns to independent rereview. Pause on blocked or inconclusive results, owner decisions, scope expansion, new finding classes, stale identity, invalid phase order, or exhausted bounds.

After valid recording, settlement, and automation receipts, return control to workflow. This procedure records packet, receipt, correction, pause, and promotion evidence but does not redefine status, lifecycle order, architecture assessment, or workflow continuation.

## Missing procedure and conflicts

If this reference becomes unavailable, unreadable, contradictory, escaped, or mixed-version after universal recording, preserve the valid record and stop settlement and automation. Report the exact resource blocker and do not reconstruct procedure from memory.
