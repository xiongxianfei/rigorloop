# Review Resolution: Simplified Proposal Contract

## Summary

Closeout status: open

Review closeout: delivery-review-r1

- Reviews covered: `delivery-review-r1`, `code-review-m2-r1`
- Findings resolved: 1
- Unresolved findings: 2
- Current result: `SPC-DR1` remains resolved. `SPC-M2-CR1` and `SPC-M2-CR2` await an owner disposition before M2 correction begins.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| SPC-DR1 | accepted | resolved | The plan now identifies the existing test specification and the current Delivery Review gate. |
| SPC-M2-CR1 | needs-decision | open | Decide whether to accept the current-versus-historical compatibility correction. |
| SPC-M2-CR2 | needs-decision | open | Decide whether to accept the governed proposal-path mismatch correction. |

## Finding Details

### delivery-review-r1

#### SPC-DR1

Finding ID: SPC-DR1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Decision owner: plan author
Decision needed: none; the user authorized refinement and rereview.
Chosen action: corrected only the test-specification source entry and remaining-gates sentence, then registered and returned the revised plan through the lifecycle CLI.
Rationale: The reviewed plan contradicts the exact package membership and the current consolidated review topology.
Required outcome: The plan accurately identifies the existing test specification and Delivery Review as the remaining pre-implementation gate.
Safe resolution path: Correct only the two plan statements, register the revised plan through its authoring lifecycle operation, record validation and a final disposition, and request a fresh Delivery Review.
Follow-up: delivery-review-r2 over the revised exact package.
Validation target: plan/test-spec package membership, `design-review-r2` authority, and current consolidated stage order.
Validation evidence: plan identity `sha256:fae8129d5d066e23a1dbf5ec6da1c0e6cf0b2a2f29f0341fe676addf15b02a9b`; plan authoring evidence `sha256:aa92b304d7a916f4af8808ce8b043fca097a816700b2b7aeb579dd1900f9b314`; correction return `evidence/delivery-review-r1-plan-return.md`; documentation prose validation passed with 0 errors and 0 warnings.

### code-review-m2-r1

#### SPC-M2-CR1

Finding ID: SPC-M2-CR1
Disposition: needs-decision
Status: open
Owner: developer
Owning stage: review-resolution
Decision owner: developer
Decision needed: Accept, reject, defer, or partially accept the required current-versus-historical compatibility correction.
Stop state: M2 remains in code-review with resolution required; no implementation correction or rereview is authorized by this record alone.
Rationale: The validator exempts changed accepted legacy proposals because terminal lifecycle state is treated as sufficient historical identity.
Required outcome: Preserve untouched settled history while requiring changed, unsettled, and new current proposals to satisfy the simplified contract.
Safe resolution path: Accept the focused scope in `code-review-m2-r1.md`, correct the selector using existing validation-scope facts without a new hash, version, field, document, or CLI command, then rerun M2 proof and rereview.
Validation target: governed fixtures distinguish untouched settled legacy evidence from changed settled, unsettled, and new current proposals.
Validation evidence: pending owner disposition and corrected M2 validation.

#### SPC-M2-CR2

Finding ID: SPC-M2-CR2
Disposition: needs-decision
Status: open
Owner: developer
Owning stage: review-resolution
Decision owner: developer
Decision needed: Accept, reject, defer, or partially accept the required governed proposal-path mismatch correction.
Stop state: M2 remains in code-review with resolution required; no implementation correction or rereview is authorized by this record alone.
Rationale: The one-way ownership model loses the legacy reverse-pointer correlation and currently treats a selected mismatched proposal as portable.
Required outcome: Block a selected governed proposal/change-record path mismatch while preserving the genuinely portable path.
Safe resolution path: Accept the focused scope in `code-review-m2-r1.md`, correlate selected current inputs at the validation-scope boundary without restoring reverse metadata, add direct fixtures, then rerun M2 proof and rereview.
Validation target: matching governed and portable proposals pass while a selected mismatched proposal/change-record pair fails with an ownership diagnostic.
Validation evidence: pending owner disposition and corrected M2 validation.
