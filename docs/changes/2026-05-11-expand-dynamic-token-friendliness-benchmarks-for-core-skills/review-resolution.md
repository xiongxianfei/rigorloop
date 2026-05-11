# Review Resolution: Expand Dynamic Token-Friendliness Benchmarks For Core Skills

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m3-r1
Review closeout: code-review-m3-r2
Review closeout: code-review-m4-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `plan-review-r2`, `code-review-m1-r1`, `code-review-m2-r1`, `code-review-m3-r1`, `code-review-m3-r2`, `code-review-m4-r1`
- Findings resolved: 7
- Unresolved findings: 1
- Final result: Proposal-review R1 requested revisions for release-report identity and result-quality gate semantics. The proposal author accepted both findings, revised the proposal, and recorded owner closeout evidence. Proposal-review R2 approved the revised proposal with no material findings. Spec-review R1 requested revisions for waiver authority consistency and claimed optional benchmark gate semantics. The spec author accepted both findings and revised the spec. Spec-review R2 approved the revised spec with no material findings. Architecture-review R1 approved the canonical architecture update with no material findings. Plan-review R1 requested revisions for test-spec sequencing and M5 release-validation scope. The plan author accepted both findings and revised the plan. Plan-review R2 approved the revised plan with no material findings. Code-review M1 R1 approved M1 with no material findings. Code-review M2 R1 approved M2 with no material findings. Code-review M3 R1 requested a validator/test fix for mismatched optional benchmark coverage metadata and dynamic run result-quality status. EDTF-CR1 was accepted and resolved in the M3 validator and tests. Code-review M3 R2 approved M3 with no material findings. Code-review M4 R1 requested a fix because the real release-validation command path does not yet supply or derive changed surfaces for required benchmark context generation.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| EDTF-PR1 | accepted | resolved | Proposal now requires explicit supersession or historical preservation when a v2 transition report would collide with the existing tracked `v0.1.1` v1 report path. |
| EDTF-PR2 | accepted | resolved | Proposal now scopes result-quality blockers to required, transition carryover, changed-skill-required, or explicitly claimed optional benchmark coverage. |
| EDTF-SR1 | accepted | resolved | Spec now uses `valid required-benchmark result-quality waiver` and the R9 allowed role enum as the single authority. |
| EDTF-SR2 | accepted | resolved | Spec now treats optional benchmarks claimed as release coverage as release-required for evidence and result-quality gates. |
| EDTF-PL1 | accepted | resolved | Plan now separates the pre-implementation `test-spec` gate from implementation milestones. |
| EDTF-PL2 | accepted | resolved | Plan now uses fixture-focused integration proof in release validation integration and keeps real `validate-release.py --version v0.1.1` in the report-evidence milestone. |
| EDTF-CR1 | accepted | resolved | Validator now reconciles optional coverage `result_quality_status` against matching dynamic run `result_quality.status` and derives optional warnings from actual run status. |
| EDTF-CR2 | needs-decision | open | Code-review M4 R1 found that the real release-validation command path does not analyze changed surfaces or require a changed-surface source before building v2 required benchmark context. |

## Finding Details

### proposal-review-r1

#### EDTF-PR1 - v2 transition target conflicts with existing tracked v0.1.1 v1 report

Finding ID: EDTF-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised `Versioning and comparison` to state that a v2 transition report must not silently overwrite an existing release token report path. If v2 also targets `v0.1.1`, the existing tracked pre-release v1 report must be explicitly superseded and preserved as historical evidence or overlap-comparison evidence. If `v0.1.1` is finalized before v2 lands, v2 moves to the next release line or RC path.
Required outcome: Clarify release-report identity so v2 transition evidence does not overwrite or ambiguously replace existing v1 release-report evidence.
Safe resolution: Revise `Versioning and comparison` to state that an expanded v2 transition report must not silently overwrite an existing `docs/reports/token-cost/releases/<release>.yaml` report. If `v0.1.1` remains the first v2 target, the proposal should say whether the existing tracked `v0.1.1` v1 report is updated before public release, preserved under a historical path, or superseded with explicit evidence. Otherwise, target the next release or RC report path that does not collide.
Rationale: The proposal says existing v1 reports remain valid historical evidence, but the repository already contains `docs/reports/token-cost/releases/v0.1.1.yaml` with `benchmark_suite.id: skill-token-runtime-v1`.
Validation target: Proposal versioning section and decision log.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`; `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-log.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-resolution.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/proposal-review-r1.md`; `git diff --check -- docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`.

#### EDTF-PR2 - Result-quality blocker wording can make optional benchmarks release-blocking

Finding ID: EDTF-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised `Release gate behavior` to scope `fail`, `not-reviewed`, and unwaived `inconclusive` blockers to required core, transition carryover, changed-skill-required, or explicitly claimed optional benchmark coverage. Optional extended benchmark failures that are not release-required now warn with notes and follow-up and must not be summarized as coverage pass.
Required outcome: Align release-gate wording with the two-tier benchmark model so optional benchmarks remain non-blocking unless they are claimed as covered or become required because their public skill changed.
Safe resolution: Revise `Release gate behavior` to block on result-quality `fail`, `not-reviewed`, or unwaived `inconclusive` only for required benchmarks, transition carryover benchmarks, changed-skill-required benchmarks, or optional benchmarks explicitly claimed as release coverage. Optional extended benchmark failures that are not release-required should warn with notes and follow-up and must not be summarized as coverage pass.
Rationale: The proposal says optional or periodic skills should not become release-blocking, but the blocking list currently says `result-quality status is fail` without scoping it to required benchmarks.
Validation target: Proposal release-gate behavior and benchmark coverage metadata examples.
Validation evidence: Shared proposal-review R1 resolution validation evidence.

### proposal-review-r2

No material findings.

### spec-review-r1

#### EDTF-SR1 - Required benchmark waiver role is internally inconsistent

Finding ID: EDTF-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Replaced the narrow `release-owner waiver` wording with `valid required-benchmark result-quality waiver` and added R9d-R9f to define required-benchmark result-quality waiver fields, allowed roles, and review-visible benchmark specificity.
Required outcome: The spec must use one waiver authority rule for required benchmark result-quality waivers.
Safe resolution: Change R8g to refer to a valid required-benchmark result-quality waiver, then let R9 define the allowed approval roles. If the desired policy is stricter, change R9a to only allow `release-owner` for required benchmark waivers and move the broader role enum to non-required or non-final waivers.
Rationale: R8g says a required benchmark `fail` or `inconclusive` result needs a valid `release-owner` waiver, while R9a and R9b define three allowed waiver approval roles.
Validation target: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md` R8 and R9.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`; `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-log.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-resolution.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/proposal-review-r1.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/proposal-review-r2.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/spec-review-r1.md`; `git diff --check -- docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`.

#### EDTF-SR2 - Claimed optional benchmark failure semantics are underspecified

Finding ID: EDTF-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Added R8j-R8l and R15e to state that optional benchmarks claimed as release coverage are treated as release-required for evidence and result-quality gates, and that failed claimed coverage may pass only if the claim is removed and the run is recorded as optional warning evidence instead.
Required outcome: The spec must define release-gate behavior for optional benchmarks that are explicitly claimed as release coverage.
Safe resolution: Add a requirement that an optional benchmark claimed as release coverage is treated as release-required for evidence and result-quality purposes: missing, invalid, failed, not-reviewed, or unwaived inconclusive claimed optional coverage blocks final release. Alternatively, require the report to remove the claim and record the run as optional warning evidence before validation can pass.
Rationale: R4a blocks missing optional benchmarks when coverage is claimed, while R8h only defines warning behavior when optional benchmarks are not required and not claimed. Claimed optional failures, inconclusive results, and not-reviewed results are not specified.
Validation target: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md` R4, R8, R15, and acceptance criteria.
Validation evidence: Shared spec-review R1 resolution validation evidence.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

#### EDTF-PL1 - Test-spec is modeled as an implementation milestone

Finding ID: EDTF-PL1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Revised the Current Handoff Summary to make `test-spec` the next stage after plan-review, added a pre-implementation test-spec gate, removed test-spec authoring from the implementation milestone list, and renumbered implementation milestones to start with manifest and prompt fixtures.
Required outcome: Separate the `test-spec` gate from implementation milestones.
Safe resolution: Move test-spec authoring out of the implementation milestone list and into the plan's handoff/dependency section. Rename the first implementation milestone to the first code/fixture change, such as manifest and required core prompt fixtures. Update `Current Handoff Summary` so the immediate next stage after plan-review is `test-spec`, and the remaining in-scope implementation milestones start after test-spec is complete.
Rationale: The plan currently lists `M1. Test spec for v2 benchmark expansion` as the current implementation milestone even though `test-spec` is the next workflow authoring stage after plan-review.
Validation target: `docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md` Current Handoff Summary and milestone list.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`; `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/plan.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-log.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-resolution.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/plan-review-r1.md`; `git diff --check -- docs/plan.md docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`.

#### EDTF-PL2 - M5 release validation command is sequenced before v2 report evidence exists

Finding ID: EDTF-PL2
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Revised the release validation integration milestone to use focused tests and fixtures instead of real final release validation, and kept `python scripts/validate-release.py --version v0.1.1` in the report-evidence milestone after v2 report metadata exists.
Required outcome: M5 validation must prove release-validation delegation and required benchmark context behavior without depending on final v2 report evidence that belongs to M6.
Safe resolution: In M5, use focused tests and fixtures to prove release validation context generation, token-cost validator delegation, changed-skill benchmark requirements, and invalid governed metadata blocking. Move the real `python scripts/validate-release.py --version v0.1.1` command to M6 after the v2 report metadata exists.
Rationale: M5 currently lists `python scripts/validate-release.py --version v0.1.1` even though M6 is where v2 release report metadata is created or updated.
Validation target: `docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md` M5 and M6 validation commands.
Validation evidence: Shared plan-review R1 resolution validation evidence.

### plan-review-r2

No material findings.

### code-review-m1-r1

No material findings.

### code-review-m2-r1

No material findings.

### code-review-m3-r1

#### EDTF-CR1 - Optional run result-quality can be hidden by mismatched coverage metadata

Finding ID: EDTF-CR1
Disposition: accepted
Status: resolved
Owner: implementation owner
Owning stage: code-review
Chosen action: Updated `scripts/validate-token-cost-report.py` to collect actual dynamic run `result_quality.status` by run id, reconcile optional coverage `result_quality_status` against the matching dynamic run, and derive optional warning requirements from the actual run status.
Required outcome: The validator must reject or otherwise block inconsistent v2 metadata where `benchmark_coverage.optional_run[*].result_quality_status` does not match the corresponding dynamic run's `result_quality.status`.
Safe resolution: Track each dynamic run's `result_quality.status` by `dynamic_runtime.runs[*].id`, compare it against `benchmark_coverage.optional_run[*].result_quality_status`, validate optional warning requirements from the reconciled actual run status, and add focused negative and positive tests for mismatched optional `fail` and `inconclusive` cases.
Rationale: Optional extended benchmarks with `fail` or `inconclusive` must warn when not required and not claimed as release coverage. Mismatched coverage metadata can currently hide an actual optional run failure by reporting `result_quality_status: pass`.
Validation target: `scripts/validate-token-cost-report.py` and `scripts/test-token-cost-report-validation.py`.
Validation evidence: `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_v2_optional_coverage_result_quality_must_match_dynamic_run` failed before the fix and passed after the fix; `python scripts/test-token-cost-report-validation.py` passed with 16 tests; `python -m py_compile scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py` passed.

### code-review-m3-r2

No material findings.

### code-review-m4-r1

#### EDTF-CR2 - Real release-validation command does not analyze changed surfaces

Finding ID: EDTF-CR2
Disposition: needs-decision
Status: open
Owner: implementation owner
Owning stage: code-review
Chosen action: pending
Decision owner: implementation owner
Decision needed: Accept EDTF-CR2 and add a release changed-surface source to the real release-validation path, or reject with evidence that another approved release-validation path supplies changed surfaces before v2 token-cost validation.
Required outcome: The release-validation path used by maintainers and CI must provide release changed-surface data to required benchmark context generation before token-cost validation runs.
Safe resolution: Add an explicit release changed-surface source to the release validation path. Acceptable first-slice options are adding a CLI/debug flag such as `--changed-paths-file` or `--changed-path` and requiring it for v2 final validation when changed-skill decisions are needed, or implementing a small release change-surface helper that derives changed paths from the approved release diff range and passes them into `validate_release_output(...)`. Add focused proof that the real release-validation entry point constructs required benchmark context from changed canonical and generated skill paths and propagates the missing required benchmark failure.
Rationale: R10b, R10c, R11a, and R12 require release validation to detect changed canonical/generated public skill surfaces and pass the resulting required benchmark context to token-cost validation. The implementation only enforces those rules when a caller manually passes `changed_paths`; `scripts/validate-release.py` does not.
Validation target: `scripts/validate-release.py`, `scripts/adapter_distribution.py`, and `scripts/test-adapter-distribution.py`.
Validation evidence: pending
