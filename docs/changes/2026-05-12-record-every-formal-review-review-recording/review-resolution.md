# Record Every Formal Review Review Resolution

## Scope

This record resolves material findings from formal lifecycle reviews for the record-every-formal-review amendment.

Closeout status: closed

## Resolution Entries

### spec-review-r1

Review closeout: spec-review-r1

#### SR-001

Finding ID: SR-001
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: spec
Decision owner: spec author
Decision needed: Choose and specify the minimal change-local root shape for isolated or review-only clean formal review receipts when no existing change root exists.
Chosen action: Added a clean receipt root rule to `specs/formal-review-recording.md`. Isolated or review-only clean formal reviews with no existing change root require `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`, and must not create `review-resolution.md` solely for the clean review.
Rationale: Every formal review receipt needs a durable, discoverable root. Clean receipts should remain lightweight, but validators and agents need a precise root shape.
Validation target: Rerun spec-review after the spec defines the isolated clean receipt root shape and update the test spec for generated clean receipt roots, review-log indexing, absence of `review-resolution.md`, and blocked recording when the change ID is ambiguous.
Validation evidence: Spec updated in `specs/formal-review-recording.md`; `spec-review-r2` approved the revised spec with no material findings.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.
