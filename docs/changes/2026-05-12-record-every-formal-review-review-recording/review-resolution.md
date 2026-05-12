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

### code-review-m1-r1

No material findings.

### code-review-m2-r1

Review closeout: code-review-m2-r1

#### CR-M2-001

Finding ID: CR-M2-001
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Add clean receipt root metadata validation and negative tests for missing reviewed artifact, missing review-log path, and nonzero unresolved items.
Rationale: The approved M2 scope requires validation for the minimal clean-receipt root metadata shape, and current validation accepts malformed clean roots.
Validation target: `python scripts/test-review-artifact-validator.py`, `python scripts/test-change-metadata-validator.py`, and focused temporary negative checks or equivalent tests showing malformed clean receipt root metadata fails.
Validation evidence: `python scripts/test-review-artifact-validator.py` passed with 35 tests; `python scripts/test-change-metadata-validator.py` passed with 7 tests; clean receipt fixture metadata and structure validation passed.

### code-review-m2-r2

Review closeout: code-review-m2-r2

#### CR-M2-002

Finding ID: CR-M2-002
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Require `review.status: clean` for strict clean receipt root metadata validation, emit the exact error `review.status must be 'clean' for clean receipt roots`, and add invalid-status negative tests for both validators.
Rationale: Clean receipt roots must be discoverable as clean receipt roots. Accepting another status such as `approved` leaves the root ambiguous while still passing clean-root validation.
Validation target: `python scripts/test-review-artifact-validator.py`, `python scripts/test-change-metadata-validator.py`, and focused validation proving `review.status: approved` and another non-clean value fail for clean receipt roots.
Validation evidence: `python scripts/test-review-artifact-validator.py` passed with 35 tests; `python scripts/test-change-metadata-validator.py` passed with 7 tests; both validator test suites reject `review.status: approved` and `review.status: changes-requested` for clean receipt roots.

### code-review-m2-r3

No material findings.
