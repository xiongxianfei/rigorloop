# Review Resolution

Closeout status: closed

### spec-review-r1

Finding ID: CRM-SR1
Disposition: accepted
Owner: spec author
Owning stage: spec
Chosen action: Revise the spec's `Next artifacts` section so `test-spec` follows required architecture, plan, and plan-review stages instead of preceding them.
Rationale: The spec-review finding identifies a workflow-order conflict that would misroute downstream lifecycle work if left unresolved.
Validation target: Rerun spec-review after the spec revision, then run review artifact, change metadata, artifact lifecycle, whitespace, and selected-CI validation for the touched spec and change-local review artifacts.
Validation evidence: Spec revision applied in `specs/change-record-catalog-registration-and-bounded-read-model.md`; `spec-review-r2` recorded clean approval. Final validation evidence is recorded in `change.yaml`.

### spec-review-r2

Finding closeout for `spec-review-r2`.

Material findings: None
Disposition: accepted
Owner: spec-review
Owning stage: spec-review
Chosen action: Record clean spec-review approval after CRM-SR1 resolution.
Rationale: R2 found no material findings and confirmed CRM-SR1 was resolved.
Validation target: Review artifact, change metadata, artifact lifecycle, whitespace, and selected-CI validation for the touched spec and change-local review artifacts.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/change-record-catalog-registration-and-bounded-read-model.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/proposal-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r2.md`; `git diff --check -- specs/change-record-catalog-registration-and-bounded-read-model.md docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `bash scripts/ci.sh --mode explicit --path specs/change-record-catalog-registration-and-bounded-read-model.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/proposal-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r2.md` passed.

### architecture-review-r1

Finding closeout for `architecture-review-r1`.

Material findings: None
Disposition: accepted
Owner: architecture-review
Owning stage: architecture-review
Chosen action: Record clean architecture-review approval for the canonical architecture update and ADR.
Rationale: Architecture review found no material findings and no required canonical or ADR updates.
Validation target: Review artifact, change metadata, artifact lifecycle, whitespace, and selected-CI validation for the touched architecture, ADR, and change-local review artifacts.
Validation evidence: Pending final architecture-review validation recorded in `change.yaml`.

### plan-review-r1

Finding closeout for `plan-review-r1`.

Material findings: None
Disposition: accepted
Owner: plan-review
Owning stage: plan-review
Chosen action: Record clean plan-review approval for the execution plan.
Rationale: Plan-review found no material findings and no required plan changes.
Validation target: Review artifact, change metadata, artifact lifecycle, whitespace, and selected-CI validation for the touched plan and review artifacts.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path specs/change-record-catalog-registration-and-bounded-read-model.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/proposal-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r2.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/architecture-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/plan-review-r1.md`; `git diff --check -- docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md docs/plan.md docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/proposal-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r2.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/architecture-review-r1.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/plan-review-r1.md` passed.

### code-review-m1-r1

Finding ID: CRM-M1-CR1
Disposition: accepted
Status: resolved after re-review
Owner: implementer
Owning stage: implement
Chosen action: Added affected-root output for registered evidence routing and direct test coverage for the affected root assertion.
Rationale: The first-pass code review identified that registered evidence selected lifecycle validation paths but omitted the affected change root required by CRM-R9 and CRM-T004.
Validation target: Rerun M1 selector tests, explicit registered-evidence routing, selected CI for selector/evidence paths, lifecycle validation, change metadata validation, and whitespace checks after the fix.
Validation evidence: `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`; `python scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `git diff --check --`.
Follow-up: `code-review-m1-r2` found no material findings. M1 is closed; M2 through M5 remain separate implementation milestones and are not claimed ready from this review.

### code-review-m1-r2

Finding closeout for `code-review-m1-r2`.

Material findings: None
Disposition: accepted
Owner: code-review
Owning stage: code-review
Chosen action: Record clean M1 re-review after CRM-M1-CR1 resolution.
Rationale: R2 found no material findings and confirmed the accepted affected-root fix satisfies CRM-R9 and CRM-T004.
Validation target: Review artifact closeout, change metadata, artifact lifecycle, selected CI, and whitespace validation for the touched review, plan, and lifecycle artifacts.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/code-review-m1-r2.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/code-review-m1-r2.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `git diff --check --`.

### code-review-m2-r1

Finding ID: CRM-M2-CR1
Disposition: accepted
Status: resolved after re-review
Owner: implementer
Owning stage: implement
Chosen action: Added an owner-approved deferral evidence shape and tests proving complete deferrals satisfy CRM-R18 while incomplete deferrals remain blocking.
Rationale: Code-review M2 R1 found that M2 emits registration debt but does not implement or test the approved owner-approved deferral path required by CRM-R17 through CRM-R19 and CRM-T009.
Validation target: Rerun M2 selector tests, direct unregistered evidence proof, local changed-path proof, selected CI, lifecycle validation, change metadata validation, review artifact validation, and whitespace checks after the fix.
Validation evidence: `python scripts/test-select-validation.py`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/unregistered-evidence.md`; `python scripts/select-validation.py --mode local`; `bash scripts/ci.sh --mode local`; `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `git diff --check --`.
Follow-up: `code-review-m2-r2` found no material findings. M2 is closed; M3 through M5 remain separate implementation milestones and are not claimed ready from this review.

### code-review-m2-r2

Finding closeout for `code-review-m2-r2`.

Material findings: None
Disposition: accepted
Owner: code-review
Owning stage: code-review
Chosen action: Record clean M2 re-review after CRM-M2-CR1 resolution.
Rationale: R2 found no material findings and confirmed the accepted owner-approved deferral fix satisfies CRM-R17 through CRM-R19 and CRM-T009.
Validation target: Review artifact closeout, change metadata, artifact lifecycle, selected CI, and whitespace validation for the touched review, plan, and lifecycle artifacts.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/code-review-m2-r2.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/code-review-m2-r2.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `git diff --check --`.

### code-review-m3-r1

Finding ID: CRM-M3-CR1
Disposition: accepted
Status: resolved after re-review
Owner: implementer
Owning stage: implement
Chosen action: Updated the M3 query helper so compact artifact path metadata is returned from accepted compact `path_vars` shapes, with direct fixture proof.
Rationale: Code-review M3 R1 found that the helper returns an empty successful artifact list for an accepted compact metadata shape whose artifact paths live in `path_vars`, violating CRM-R29, CRM-R36, and CRM-T016.
Validation target: Rerun query helper tests, metadata validator regression, active query commands, selected CI for query/helper/metadata paths, lifecycle validation, review-artifact validation, and whitespace checks after the fix.
Validation evidence: `python scripts/test-query-change-record.py`; `tmp=$(mktemp -d) && mkdir -p "$tmp/docs/changes/compact-valid" && cp tests/fixtures/change-metadata/compact-valid/change.yaml "$tmp/docs/changes/compact-valid/change.yaml" && python scripts/query-change-record.py compact-valid artifacts --repo-root "$tmp" && python scripts/query-change-record.py compact-valid summary --repo-root "$tmp"`; `python scripts/test-change-metadata-validator.py`; `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`; `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary`; `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model artifacts`; `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model validation --latest`; `bash scripts/ci.sh --mode explicit --path scripts/query-change-record.py --path scripts/test-query-change-record.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/validate-change-metadata.py --path scripts/test-change-metadata-validator.py`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `bash scripts/ci.sh --mode explicit --path scripts/query-change-record.py --path scripts/test-query-change-record.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `git diff --check --`.
Follow-up: `code-review-m3-r2` found no material findings. M3 is closed; M4 and M5 remain separate implementation milestones and are not claimed ready from this review.

### code-review-m3-r2

Finding closeout for `code-review-m3-r2`.

Material findings: None
Disposition: accepted
Owner: code-review
Owning stage: code-review
Chosen action: Record clean M3 re-review after CRM-M3-CR1 resolution.
Rationale: R2 found no material findings and confirmed the accepted compact `path_vars` artifact extraction fix satisfies CRM-R29, CRM-R32, CRM-R33, CRM-R36, CRM-T016, and the CRM-M3-CR1 regression.
Validation target: Review artifact closeout, change metadata, artifact lifecycle, selected CI, and whitespace validation for the touched review, plan, query-helper, and lifecycle artifacts.
Validation evidence: `python scripts/test-query-change-record.py`; `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary`; `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model artifacts`; direct compact `path_vars` fixture proof using `tests/fixtures/change-metadata/compact-valid/change.yaml` copied under a temporary `docs/changes/compact-valid/change.yaml`; final review artifact closeout, change metadata, artifact lifecycle, selected CI, and whitespace validation are recorded in `change.yaml`.
