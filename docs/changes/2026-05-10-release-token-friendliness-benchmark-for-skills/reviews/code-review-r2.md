# Code Review R2

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M1 metadata schema and validator
Status: changes-requested
Date: 2026-05-11

## Review Inputs

- Diff range: `ed5d21d..7150dcf`
- Review surface: M1 code-review R1 resolution commit plus tracked M1 validator state.
- Spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`
- Plan milestone: `docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md`, M1.
- Architecture: `docs/architecture/system/architecture.md`
- Prior review: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r1.md`
- Review resolution: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md`
- Validation evidence recorded in the active plan and change metadata.
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Diff Summary

The R1 resolution adds RC reuse validation and Markdown/YAML pairing validation to `scripts/validate-token-cost-report.py`, extends `scripts/test-token-cost-report-validation.py` with failing and passing coverage for those paths, records `code-review-r1`, closes the R1 findings in `review-resolution.md`, and returns M1 to code-review rerun state in the plan and plan index.

## Findings

### RTF-CR3 - RC reuse surface coverage accepts an incomplete checked-surface rationale

Finding ID: RTF-CR3
Severity: major
Dimension: spec alignment, edge cases, test coverage

Evidence:

- The approved spec requires that when `benchmark_relevant_changes_since_rc` is false, the rationale state the checked surfaces, "including public skills, adapter output, workflow guide, benchmark prompts, analyzer, fixture, model or tool version when known, and release packaging" (`specs/release-token-friendliness-benchmark-for-skills.md`, R22c).
- The validator defines those surface markers in `scripts/validate-token-cost-report.py`, but `validate_rc_reuse` only requires `any(marker in checked_text for marker in BENCHMARK_RELEVANT_SURFACE_MARKERS)`.
- The test added for this path only rejects `"No relevant changes."` and accepts a rationale with all surfaces; it does not prove that a rationale with only one checked surface is rejected.

Problem:

Metadata can satisfy the validator with `benchmark_relevant_changes_since_rc: false` while naming only one benchmark-relevant surface. That leaves reviewers without the complete RC reuse decision surface required by R22c.

Required outcome:

For `benchmark_relevant_changes_since_rc: false`, the validator and tests must require the RC reuse rationale or checked-surface text to cover all required R22c surface categories, with a practical allowance for model/tool version wording.

Safe resolution:

Change the RC reuse checked-surface validation from an `any` match to a required-surface check. Require at least these categories to be named across `checked_surface` and `rationale`: public skills, adapter output, workflow guide, benchmark prompts, analyzer, fixture, model or tool version, and release packaging. Add negative tests where one required category is missing and positive coverage where all required categories are present.

Owner: implementer
Owning stage: implement M1

## Checklist Coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | block | R22c requires a complete checked-surface rationale for false RC reuse decisions; the implementation accepts any one surface marker. |
| Test coverage | block | Added RC reuse tests cover missing field and no-surface cases, but not partial-surface cases. |
| Edge cases | block | Partial RC reuse rationale is a named edge case for release-owner decision evidence. |
| Error handling | pass | Existing validator errors are field-oriented and actionable for the covered paths. |
| Architecture boundaries | pass | The diff stays inside the standalone M1 validator/test boundary and does not touch M5 release integration. |
| Compatibility | pass | No generated adapter output or release-level validation wiring changed. |
| Security/privacy | pass | The reviewed diff does not expose secrets and preserves raw JSONL omission handling. |
| Derived artifact currency | pass | No generated artifacts were edited. |
| Unrelated changes | pass | Changes are scoped to M1 validator/tests and required lifecycle artifacts. |
| Validation evidence | concern | Recorded validation commands are relevant, but current tests do not prove partial-surface RC reuse rejection. |

## Review Status

changes-requested

## Recommended Next Stage

Review-resolution for M1, then implement the RTF-CR3 validator/test fix and rerun code-review for M1.

This is a direct code-review request. There is no automatic downstream handoff beyond recording the required review state.
