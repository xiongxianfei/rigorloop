# Review Resolution: Separately Armed Implementation Autoprogression Through Verify

Closeout status: closed

## Resolution Entries

### proposal-review-r1

No material findings.

### spec-review-r1

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

Review closeout: code-review-m1-r1

#### CR-M1-R1-F1 - Named autoprogression containers can still own live workflow state

Finding ID: CR-M1-R1-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1 review-resolution
Decision owner: implementation author
Chosen action: Extracted `reject_autoprogression_live_state_fields`, called it for named-record containers and per-record validation, tightened `schemas/change.schema.json` with `additionalProperties: false` on the `workflow.autoprogression` container, and changed legacy metadata validation to report schema and semantic errors together.
Rationale: The code-review finding is correct. Profile policy metadata is an audit and authorization surface, not the live owner of current stage, next stage, review status, branch readiness, or PR readiness.
Validation target: Add a regression where `workflow.autoprogression.next_stage` appears beside an `implementation_through_verify` named record and fails validation, then run the focused autoprogression tests, full change metadata validator suite, change metadata validation, review artifact validation, artifact lifecycle validation, and diff whitespace checks.
Validation evidence: Added `tests/fixtures/change-metadata/implementation-autoprogression-container-next-stage/change.yaml` and regression tests covering named-record container `current_stage`, `next_stage`, `review_status`, `branch_readiness`, `pr_readiness`, all five fields together, legacy record rejection, authoring-record rejection, implementation-record rejection, and unrelated top-level `workflow` field acceptance. Direct proof command `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/implementation-autoprogression-container-next-stage/change.yaml` now fails with `workflow.autoprogression.next_stage: unexpected property` and `workflow.autoprogression.next_stage: profile policy must not own live workflow state`. `python scripts/test-change-metadata-validator.py -k autoprogression_policy`, `python scripts/test-change-metadata-validator.py -k named_autoprogression_policy`, `python scripts/test-change-metadata-validator.py -k forbidden_live_state`, `python scripts/test-change-metadata-validator.py -k forbidden`, and `python scripts/test-change-metadata-validator.py` passed. Rerun target: `code-review-m1-r2`. M1 closeout readiness is contingent on rereview returning clean and recorded.

## Pattern note

CR-M1-R1-F1 repeats the same structural pattern called out in prior lifecycle feedback: a state or field exists, the code reads past it, and a contract invariant is silently bypassed. The remediation used here is now the local convention for this initiative: extract the invariant into a named helper, call it from every path that can violate it, and fail closed when the input shape is unrecognized. A quick audit of `scripts/validate-change-metadata.py` found no other `AUTOPROGRESSION_NAMED_RECORDS` iteration beyond the fixed `validate_autoprogression_policy` path.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

No material findings.

### code-review-m3-r1

Review closeout: code-review-m3-r1

#### CR-M3-R1-F1 - Correction path locality can bypass reviewer-declared affected paths

Finding ID: CR-M3-R1-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M3 review-resolution
Chosen action: Correction path locality now computes the ordinary correction path set from the union of unresolved findings' reviewer-declared `affected_paths`; top-level `affected_paths`, when present, is verified against that union and no longer acts as an independent authority. Empty unresolved finding paths stop with `correction-finding-missing-affected-paths`; disagreement stops with `correction-affected-paths-disagree-with-findings`; approved generated outputs, workflow projections, and evidence records remain separate allowlists.
Rationale: The finding identifies a contract violation against `workflow-stage-autoprogression` R2bp. Automatic correction path locality must be based on reviewer-declared affected paths, not a caller-supplied top-level allowance that can diverge from the finding.
Validation target: Add a correction-guardrail regression with mismatched finding-level and top-level affected paths, then run focused correction guardrail tests and the full artifact lifecycle validator suite.
Validation evidence: Added regressions for top-level/finding path disagreement, changed paths outside the reviewer union, missing per-finding affected paths, approved generated-output allowance, approved projection/evidence allowance, and resolved-finding paths not contributing to the active correction set. `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails` now runs 15 tests, up from the previous M3 focused count of 4, and passed. `python scripts/test-artifact-lifecycle-validator.py` passed with 128 tests.

#### CR-M3-R1-F2 - Mechanical correction eligibility does not require deterministic authority

Finding ID: CR-M3-R1-F2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M3 review-resolution
Chosen action: Added `MECHANICAL_REQUIRED_FIELDS` and `DECLARED_SAFE_REQUIRED_FIELDS` constants and drove correction-finding eligibility from those enumerations. Mechanical findings now require nonempty `deterministic_authority`; empty-but-present values fail closed; the valid correction fixture now includes deterministic authority.
Rationale: The finding identifies a contract violation against `workflow-stage-autoprogression` R2bj and `review-finding-resolution-contract` R1h. Mechanical auto-fix eligibility must require deterministic authority before automatic correction can proceed.
Validation target: Add a correction-guardrail regression for a mechanical finding without deterministic authority, then run focused correction guardrail tests and the full artifact lifecycle validator suite.
Validation evidence: Added regressions for missing deterministic authority, empty deterministic authority, every mechanical required field, every declared-safe required field, complete mechanical fields, and unknown auto-fix class. `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails` now runs 15 tests, up from the previous M3 focused count of 4, and passed. `python scripts/test-artifact-lifecycle-validator.py` passed with 128 tests. `python scripts/test-review-artifact-validator.py` passed with 52 tests.

## M3 Review-Resolution Note

The M3 findings dogfooded the reviewer-owned `auto_fix_class=declared-safe` mechanism: both recipes were deterministic, path-bounded to `scripts/lifecycle_state_sync.py` and `scripts/test-artifact-lifecycle-validator.py`, named validation commands, and forbade governing-artifact changes. The recurring validation pattern is now empirical in this initiative: when specs enumerate required fields, validators should extract the required-field set into named constants, iterate those constants, and fail closed on unknown values rather than checking a remembered subset.

### code-review-m3-r2

No material findings.

### code-review-m4-r1

No material findings.

### code-review-m5-r1

No material findings.

### code-review-m5-r2

No material findings.
