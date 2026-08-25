# Governed spec-review settlement

Load only after `governed-spec-entry` authority is established. The parent owns judgment, recording rules, status, findings, stops, claims, and handoff; loading does not grant settlement, correction, or continuation authority.

## Change-record review settlement

Run settlement only after universal review recording succeeds. Run `rigorloop lifecycle context spec-review --change <change-id> --format json`, submit `record-review` with its lifecycle revision, exact spec ID, review path, and `stage_authority: spec-review`, refresh context, then submit `settle-artifact` for the same target and authority. The CLI validates reviewed bytes, round, log, findings, authority, and freshness and may settle only the matching spec entry.

Never edit settlement fields. Preserve a successfully recorded review when settlement blocks. `already-recorded` is identical success. Independent review stops without routing; workflow owns continuation.

## Workflow-managed automation

For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review.

During Phase 1 of independent automated review rollout, workflow-managed automated `spec-review` should at least record a review invocation manifest before automated handoff. This is manifest-only evidence for `spec-review`; it does not yet require the full blind-first automated review protocol unless a later approved slice adopts it. Direct or review-only `spec-review` requests remain isolated by default.

Use neutral packet and ordered receipts. Corrections require separate authority, named surfaces and proof, and fresh rereview. Pause on blocked or inconclusive results, owner decisions, scope expansion, new finding classes, stale identity, invalid phase order, or exhausted bounds. Return control to workflow without redefining lifecycle order or architecture assessment.

## Resource failure

If this reference is unavailable, contradictory, escaped, or mixed-version after recording, preserve the record and stop settlement. Report the blocker and never reconstruct procedure.
