# Review Resolution: Simplified Proposal Contract

## Summary

Closeout status: closed

Review closeout: code-review-m4-r1

- Reviews covered: `delivery-review-r1`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m2-r3`, `code-review-m2-r4`, `code-review-m2-r5`, `code-review-m3-r1`, `delivery-review-r3`, `code-review-m3-r2`, `code-review-m4-r1`
- Findings resolved: 10
- Unresolved findings: 0
- Current result: all findings are resolved. Review closeout now uses stable occurrence, stage, and numeric round instead of Markdown source order.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| SPC-DR1 | accepted | resolved | The plan now identifies the existing test specification and the current Delivery Review gate. |
| SPC-M2-CR1 | accepted | resolved | Current selected-path scope now distinguishes changed settled governed proposals from untouched settled history. |
| SPC-M2-CR2 | accepted | resolved | Explicitly selected stage-owned proposal/change-record pairs now fail when the primary proposal path differs. |
| SPC-M2-CR3 | accepted | resolved | Complete simplified shape is recognized before the settled-history legacy exception. |
| SPC-M2-CR4 | accepted | resolved | Selected governed inputs are correlated directly without a filename-equality rule. |
| SPC-M2-CR5 | accepted | resolved | Mismatch inference now considers only selected records that declare a primary proposal entry. |
| SPC-M2-CR6 | accepted | resolved | Mismatch inference is limited to an unambiguous one-proposal/one-primary-record selection. |
| SPC-M3-CR1 | accepted | resolved | Current temporary parity is owned by CMD-07; CMD-08 validates immutable v0.4.1 evidence through its recorded source. |
| SPC-M3-CR2 | accepted | resolved | The M3 evidence now attributes its corrected proof split to Delivery Review R3. |
| SPC-M4-CR1 | accepted | resolved | Closeout validation now recognizes higher-round rereviews for the same stable occurrence independently of canonical review-log section order. |

## Finding Details

### code-review-m4-r1

#### SPC-M4-CR1

Finding ID: SPC-M4-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: implementation author
Decision needed: none; the bounded validator correction is accepted.
Chosen action: Compare blocking reviews against all parsed entries using stable occurrence identity, stage, and normalized numeric round, with focused positive and negative regressions.
Rationale: The canonical review log places clean receipts before detailed findings, while the validator searches only entries physically below a blocking occurrence. Seven reviews with valid higher-round nonblocking rereviews are therefore reported unresolved.
Required outcome: A blocking review is closed by a higher-round nonblocking rereview for the same stable occurrence regardless of canonical section placement, while a review with no later round for that occurrence or explicit closeout remains blocking.
Safe resolution path: Compare each blocking review against all parsed entries using stable occurrence identity (for example, review ID without final `-rN`), stage, and numeric round; add canonical-order positive, no-rereview negative, and different-milestone negative regressions; rerun review-artifact tests plus structure and closeout validation, record the accepted resolution, and request final holistic rereview.
Follow-up: final holistic code-review M4 R3.
Validation target: closeout mode passes this fully resolved prior review history, keeps the open M4 occurrence blocking, and still rejects a blocking occurrence without a same-occurrence higher-round nonblocking review or explicit closeout.
Validation evidence: correction commit `c1863b7a`; independent `code-review-m4-r2.md`; review-artifact validator 108/108; canonical-order positive, same-round negative, and cross-milestone negative regressions passed; closeout validation no longer reports the seven false historical failures; structure validation, change metadata, and diff check passed.

### code-review-m3-r2

#### SPC-M3-CR2

Finding ID: SPC-M3-CR2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: implementation author
Decision needed: none; the focused evidence-attribution correction is accepted.
Chosen action: Changed only the stale review ID in the M3 evidence from `delivery-review-r2` to `delivery-review-r3`.
Rationale: Durable M3 evidence must cite the exact Delivery package that approved the commands and proof boundary it reports.
Required outcome: The M3 evidence identifies `delivery-review-r3` as the exact approved package.
Safe resolution path: Change only `delivery-review-r2` to `delivery-review-r3` in the M3 evidence, record an accepted disposition, validate review artifacts and change metadata, run `git diff --check`, and request focused M3 R3 rereview.
Follow-up: focused code-review M3 R3.
Validation target: M3 evidence, `change.yaml`, and Delivery Review R3 all identify the same exact authorizing review.
Validation evidence: `code-review-m3-r2.md`; corrected M3 evidence, corrected plan/test-spec commit `3c4aff53`, Delivery Review R3 receipt `004b711d`, current `change.yaml` package authority, review/change-metadata validation, and diff check.

### code-review-m3-r1

#### SPC-M3-CR1

Finding ID: SPC-M3-CR1
Disposition: accepted
Status: resolved
Owner: delivery package authors and implementation author
Owning stage: plan, test-spec, and implement
Decision owner: Delivery Review
Decision needed: none; Delivery Review R3 approved the corrected proof split.
Chosen action: Assign current temporary archive and clean-install parity to CMD-07, validate published v0.4.1 through `--recorded-source-auto` in CMD-08, and restore every historical metadata and package expectation byte changed by the initial implementation.
Rationale: Current-source generation and published-release integrity are distinct proof boundaries and must not share an already-published identity.
Required outcome: Preserve the published `v0.4.1` report, bundled metadata, release index, and package expectation; prove current proposal-stage publication parity without reusing that historical identity.
Safe resolution path: Route the command and proof wording to plan/test-spec ownership, approve the corrected Delivery package, revert the historical metadata and expectation changes, update M3 evidence, rerun the corrected proof, and independently rereview M3.
Follow-up: independent code-review M3 R2.
Validation target: recorded-source `v0.4.1` validation passes with original checksums while current canonical proposal/proposal-review packages pass all supported temporary adapter projection checks.
Validation evidence: Delivery Review R3 commit `004b711d`; correction commit `2acecb1c`; local build tests 8/8; focused three-adapter proposal-stage archive/install parity passed; `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto` passed for recorded source `a9f1220040acd590f50ff0ed2d50f72d0990bcf0`; diff check passed.

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
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: developer
Decision needed: none; the user's `go ahead` authorized the bounded correction and mandatory rereview.
Chosen action: Use the validator's existing selected-path scope so a settled governed legacy proposal is historical only when reached through its change record and current when the proposal itself is selected.
Rationale: The validator exempts changed accepted legacy proposals because terminal lifecycle state is treated as sufficient historical identity.
Required outcome: Preserve untouched settled history while requiring changed, unsettled, and new current proposals to satisfy the simplified contract.
Safe resolution path: Accept the focused scope in `code-review-m2-r1.md`, correct the selector using existing validation-scope facts without a new hash, version, field, document, or CLI command, then rerun M2 proof and rereview.
Validation target: governed fixtures distinguish untouched settled legacy evidence from changed settled, unsettled, and new current proposals.
Validation evidence: correction commit `f3fd200c`; artifact-lifecycle validator 155/155; review-artifact validator 107/107; current proposal, review structure, change metadata, and diff checks passed.

#### SPC-M2-CR2

Finding ID: SPC-M2-CR2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: developer
Decision needed: none; the user's `go ahead` authorized the bounded correction and mandatory rereview.
Chosen action: When a current proposal and same-named stage-owned change record are selected together, require that record's primary proposal entry to match before portable fallback is allowed.
Rationale: The one-way ownership model loses the legacy reverse-pointer correlation and currently treats a selected mismatched proposal as portable.
Required outcome: Block a selected governed proposal/change-record path mismatch while preserving the genuinely portable path.
Safe resolution path: Accept the focused scope in `code-review-m2-r1.md`, correlate selected current inputs at the validation-scope boundary without restoring reverse metadata, add direct fixtures, then rerun M2 proof and rereview.
Validation target: matching governed and portable proposals pass while a selected mismatched proposal/change-record pair fails with an ownership diagnostic.
Validation evidence: correction commit `f3fd200c`; direct mismatch regression passed; artifact-lifecycle validator 155/155; review-artifact validator 107/107; current proposal, review structure, change metadata, and diff checks passed.

### code-review-m2-r2

#### SPC-M2-CR3

Finding ID: SPC-M2-CR3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: developer
Decision needed: none; the user's `go ahead` authorized the bounded correction and mandatory rereview.
Chosen action: Recognize a complete simplified proposal shape before applying the settled-history legacy exception, while still treating a selected settled legacy proposal as current.
Rationale: Terminal lifecycle state currently overrides simplified proposal shape and causes an unchanged accepted simplified proposal to be validated as legacy.
Required outcome: Preserve readable unchanged settled proposals under both the legacy and simplified contracts while changed legacy work uses the current contract.
Safe resolution path: Accept the focused scope in `code-review-m2-r2.md`, adjust only current-versus-historical shape selection, add the accepted simplified governed regression, rerun M2 proof, and rereview.
Validation target: an accepted simplified governed proposal selected only through its change record passes the simplified contract while the existing legacy partitions retain their outcomes.
Validation evidence: correction commit `b98e9926`; accepted simplified, accepted legacy, changed legacy, and unsettled legacy regressions pass; artifact-lifecycle validator 156/156 and review-artifact validator 107/107 pass.

#### SPC-M2-CR4

Finding ID: SPC-M2-CR4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: developer
Decision needed: none; the user's `go ahead` authorized the bounded correction and mandatory rereview.
Chosen action: Correlate one explicitly selected stage-owned change record with the selected proposal directly, regardless of their filenames.
Rationale: The correction detects only same-named proposal/change-record pairs even though the approved ownership contract defines no filename equality requirement.
Required outcome: Block an unambiguous selected governed path mismatch without imposing a new proposal/change-record naming contract or breaking portable proposals.
Safe resolution path: Accept the focused scope in `code-review-m2-r2.md`, correlate selected scope directly, add the different-identity mismatch regression, rerun M2 proof, and rereview.
Validation target: same-named and different-identity selected mismatches fail, matching governed proposals pass, and a proposal with no selected governing record remains portable.
Validation evidence: correction commit `b98e9926`; different-change-ID mismatch regression passed; artifact-lifecycle validator 156/156 and review-artifact validator 107/107 pass.

### code-review-m2-r3

#### SPC-M2-CR5

Finding ID: SPC-M2-CR5
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: developer
Decision needed: none; the user's `go ahead` authorized the bounded correction and mandatory rereview.
Chosen action: Track selected stage-owned records with a primary proposal entry separately and apply mismatch correlation only to that set.
Rationale: The current condition couples a portable proposal to any single selected stage-owned change record, including a record with no proposal entry.
Required outcome: Preserve portable proposal validity when an unrelated selected change record has no proposal entry, while keeping different-ID governed mismatch detection when the record declares proposal ownership.
Safe resolution path: Accept the focused scope in `code-review-m2-r3.md`, narrow only the ownership inference, add the composition regression, rerun M2 proof, and rereview.
Validation target: portable proposal plus unrelated non-proposal change record passes; matching governed proposal passes; different-ID selected proposal mismatch still fails.
Validation evidence: correction commit `f395ab51`; portable-plus-spec-only-record and different-ID mismatch regressions pass; artifact-lifecycle validator 157/157 and review-artifact validator 107/107 pass.

### code-review-m2-r4

#### SPC-M2-CR6

Finding ID: SPC-M2-CR6
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement
Decision owner: developer
Decision needed: none; the finding is an in-scope, safely actionable correction to the approved M2 behavior.
Chosen action: Narrow mismatch inference so a valid portable proposal remains independent when another proposal and its matching primary-proposal record are selected in the same validation scope, while retaining the unambiguous selected mismatch diagnostic.
Rationale: The scope-wide condition treats one selected primary-proposal record as the owner of every selected proposal and therefore violates portable composition.
Required outcome: Portable and governed proposals compose in one validation scope without weakening the existing unambiguous governed mismatch check.
Safe resolution path: Correlate only an unambiguous one-proposal/one-primary-record selection, or use another bounded selected-scope correlation that introduces no filename rule, hash, version, reverse pointer, repository inventory, or new CLI mechanism; add the mixed portable/governed regression and rerun M2 proof.
Follow-up: bounded M2 correction followed by independent code-review R5.
Validation target: portable proposal plus correctly governed proposal/change-record pair passes; matching governed proposal and portable-only cases pass; different-ID single selected mismatch still fails.
Validation evidence: correction commit `e757b2a3`; mixed portable/governed composition and direct mismatch regressions pass; artifact-lifecycle validator 158/158, review-artifact validator 107/107, current explicit-path validation, metadata validation, boundary validation, and aggregate diff check passed.
