# Proposal-review recording and settlement

Load exactly when `durable_recording_context` is true. The parent owns judgment, modes, claims, stops, and handoff; this reference owns recording and formal CLI settlement.

## Recording

Valid modes are `advisory-durable/manual`, `formal-lifecycle/manual`, and `formal-lifecycle/workflow-managed-automated`; every other automated pair blocks. Resolve formal identity from the active owning root, reviewed metadata, explicit change ID, then a minimal recording-only fallback. Ambiguity, collision, unsafe path, or write failure reports `Recording status: blocked` and preserves findings in the result.

A generated `YYYY-MM-DD-<subject>-review-recording` fallback grants no settlement authority. Review recording and settlement must not advance workflow.

Clean formal review writes one receipt and `review-log.md` entry without empty resolution. Material or blocking outcomes write a detailed record, synchronize the log, and create `review-resolution.md` only when required. Use the mapped result asset and one finding asset per finding. An identical retry reconciles once; conflicting review-ID reuse stops unchanged. Advisory recording creates no governed settlement or continuation authority.

## Formal lifecycle settlement

After writing the review and log, run `rigorloop lifecycle context proposal-review --change <change-id> --format json`. Submit `record-review` with its lifecycle revision, exact proposal ID, review path, and `stage_authority: proposal-review`; refresh context and submit `settle-artifact` for the same target and authority. The CLI validates identity, round, findings, freshness, and authority and derives the result.

Never edit settlement fields. Preserve a successfully recorded review when settlement blocks. `already-recorded` is identical success. Settlement never advances routing; workflow owns continuation.

## Workflow-managed automated review

For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review.

Use neutral packet and ordered receipts; corrections require separate authority, named surfaces, named proof, and rereview. Pause on owner decisions, scope expansion, stale identity, new finding classes, non-shrinking correction, or exhausted bounds. Return control to workflow without redefining settlement or continuation.

## Resource failure

Missing, unreadable, contradictory, escaped, or mixed-version resources block their dependent write or claim. Preserve findings and never reconstruct procedure.
