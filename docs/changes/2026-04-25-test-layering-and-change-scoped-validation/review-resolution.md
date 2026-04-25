# Review Resolution

Closeout status: closed

### architecture-review-r1

Finding ID: AR1-F1
Disposition: accepted
Owner: architecture owner
Owning stage: architecture
Chosen action: Add a broad-smoke trigger-source model with source-attributed `broad_smoke.required` and `broad_smoke.sources` data, plus detection and consumption rules for mode, explicit flag, active plan, test spec, review-resolution, and release metadata sources.
Rationale: The selector and wrapper need source attribution so broad-smoke requirements remain tied to authoritative artifacts instead of becoming an unexplained boolean or bare CLI flag.
Validation target: Validate lifecycle and review artifacts, then rerun architecture-review.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` passed; `python scripts/validate-review-artifacts.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation` passed.

Finding ID: AR1-F2
Disposition: accepted
Owner: architecture owner
Owning stage: architecture
Chosen action: Define durable manual-proof storage in `docs/changes/<change-id>/verify-report.md` for normal changes and release metadata for release smoke, with `verify` owning manual-proof closeout validation.
Rationale: Manual proof is handoff evidence, not selector state, so durable storage and closeout validation belong to workflow artifacts and `verify`.
Validation target: Validate lifecycle and review artifacts, then rerun architecture-review.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` passed; `python scripts/validate-review-artifacts.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation` passed.

Finding ID: AR1-F3
Disposition: accepted
Owner: architecture owner
Owning stage: architecture
Chosen action: Define v1 unclassified path behavior as `status: "blocked"` with `unclassified-path`; do not implement conservative fallback until a later approved change defines the exact fallback check set.
Rationale: Blocking is simpler and safer for v1 because no deterministic fallback set has been specified.
Validation target: Validate lifecycle and review artifacts, then rerun architecture-review.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` passed; `python scripts/validate-review-artifacts.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation` passed.

### architecture-review-r2

Review closeout: architecture-review-r1
Review closeout: architecture-review-r2

### plan-review-r1

Finding ID: PR1-F1
Disposition: accepted
Owner: plan owner
Owning stage: plan
Chosen action: Route expected blocked selector and wrapper proof through `python scripts/test-select-validation.py` instead of listing raw expected-failure commands as milestone pass gates.
Rationale: `python scripts/test-select-validation.py` can assert nonzero selector and wrapper behavior while still exiting `0` when the expected blocked result is observed.
Validation target: Validate lifecycle and review artifacts, then rerun plan-review.
Validation evidence: `python scripts/validate-review-artifacts.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md --path specs/test-layering-and-change-scoped-validation.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml` passed.

### plan-review-r2

Review closeout: plan-review-r1
Review closeout: plan-review-r2

### code-review-r1

Finding ID: CR1-F1
Disposition: accepted
Owner: implementation owner
Owning stage: implement
Chosen action: Add direct regression proof for ambiguous direct files under `docs/releases/`, then tighten release-version inference so only paths nested under `docs/releases/<version>/...` infer a release version.
Rationale: The user accepted the code-review finding and clarified that direct files under `docs/releases/` are ambiguous in v1 and must block with `release-version-required` or manual routing.
Validation target: `python scripts/test-select-validation.py`
Validation evidence: `python scripts/test-select-validation.py` passed with 16 tests after the fix; direct probe `python scripts/select-validation.py --mode explicit --path docs/releases/release-notes.md` returned `status: "blocked"`, `release-version-required`, and exit `2`.

Finding ID: CR1-F2
Disposition: accepted
Owner: implementation owner
Owning stage: implement
Chosen action: Add direct targeted proof for every named M1 selector mode and the missing first-slice category representatives using table-driven tests and a temporary Git range fixture for valid PR/main behavior.
Rationale: The user accepted the direct-proof gap and instructed that nearby or partial cases must not substitute for named test-spec coverage.
Validation target: `python scripts/test-select-validation.py`
Validation evidence: `python scripts/test-select-validation.py` passed with 16 tests, including table-driven first-slice representative coverage and valid PR/main Git range fixtures.

### code-review-r2

Review closeout: code-review-r1
Review closeout: code-review-r2

### code-review-r3

Finding ID: CR3-F1
Disposition: accepted
Owner: implementation owner
Owning stage: implement
Chosen action: Add a focused CI wrapper regression test that feeds selector fixture JSON with a valid check ID and a tampered non-catalog command, then asserts `scripts/ci.sh` rejects the payload before executing the selected check.
Rationale: The implementation already validates selected commands against the catalog, but the approved test spec requires direct proof that arbitrary selector JSON command text cannot bypass the trusted catalog contract.
Validation target: `python scripts/test-select-validation.py`
Validation evidence: `python scripts/test-select-validation.py` passed with 24 tests after adding `test_ci_wrapper_rejects_selector_command_mismatch`; `bash scripts/ci.sh --mode explicit --path specs/test-layering-and-change-scoped-validation.md` passed; `bash scripts/ci.sh --mode explicit --path scripts/ci.sh` passed; `bash scripts/ci.sh --mode broad-smoke` passed.

### code-review-r4

Review closeout: code-review-r3
Review closeout: code-review-r4

### code-review-r5

Review closeout: code-review-r5

### code-review-r6

Review closeout: code-review-r6

### code-review-r7

Review closeout: code-review-r7
