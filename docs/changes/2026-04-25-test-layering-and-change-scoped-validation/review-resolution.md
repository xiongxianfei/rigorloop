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
