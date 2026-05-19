# Plan Review R1: Assets-First Progressive Disclosure Pilot for Published Skills

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md
Status: changes-requested
Reviewed artifact: docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: APD-PLR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/plan-review-r1.md
- Review log: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md
- Review resolution: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-resolution.md
- Open blockers: APD-PLR1
- Immediate next stage: plan revision

## Findings

### APD-PLR1 - Test-spec authoring is mixed into implementation milestone

Finding ID: APD-PLR1
Severity: major
Location: `docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md`, M1 and Dependencies.
Evidence: The plan correctly states that the related test spec is "to be amended after plan-review" and that `specs/skill-contract.test.md` must be amended and owner-approved before implementation. However, M1 lists `specs/skill-contract.test.md` as a likely touched implementation file, lists "test-spec coverage for R37-R45" under tests to add/update, and includes "Amend `specs/skill-contract.test.md` to map R37-R45 to concrete tests" as an implementation step. The project workflow orders the lifecycle as `plan -> plan-review -> test-spec -> implement`.
Required outcome: Keep the `test-spec` stage distinct from implementation. M1 must start only after the test-spec amendment is approved, and M1 must implement validator/tests/fixtures from that approved test spec rather than authoring the test spec inside the implementation milestone.
Safe resolution path: Revise the plan to add or strengthen a pre-implementation prerequisite for the test-spec amendment, remove `specs/skill-contract.test.md` from M1's implementation-owned touched files, replace the M1 implementation step with "Implement the tests defined by the approved test-spec amendment," and keep the immediate next stage as `test-spec` after a clean plan-review.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Self-contained context | pass | The plan names the proposal, approved spec, review evidence, change root, scoped files, and relevant validator entrypoints. |
| Source alignment | concern | R37-R45 are mapped, but M1 crosses the workflow boundary between `test-spec` and `implement`. |
| Milestone size | pass | M1, M2, and M3 are reasonably reviewable slices: validation mechanics, skill asset split, and adapter/token/parity proof. |
| Sequencing | concern | `test-spec` must remain a lifecycle stage after `plan-review`; it should not be authored as an implementation step in M1. |
| Scope discipline | pass | The plan keeps the pilot limited to `plan`, four assets, validators, adapter proof, and evidence. |
| Validation quality | pass with concern | Commands are concrete and tied to the slice, but the test-spec authority must be settled before the tests are implemented. |
| TDD readiness | concern | M1 is intended to make the requirements testable, but test-spec authoring belongs in the downstream `test-spec` stage. |
| Risk coverage | pass | Token, fingerprint brittleness, adapter packaging, and handoff-rule risks are named with recovery paths. |
| Architecture alignment | pass | The no-architecture rationale is credible for a Markdown/static-validator/package-proof change. |
| Operational readiness | pass | The plan names adapter build/validation and avoids hand-editing generated adapter output. |
| Plan maintainability | pass | Current Handoff Summary, dependencies, validation notes, and rollback paths are present. |

## Missing Milestones Or Dependencies

No new milestone is required. The missing boundary is a stage dependency: the test-spec amendment should happen after this review and before M1 implementation.

## Exact Suggested Edits

- Keep the top-level related test spec note that the test spec is to be amended after plan-review.
- Add a `Pre-implementation prerequisites` section, or strengthen `Dependencies`, to say the approved test-spec amendment is the next stage after a clean plan-review.
- In M1, remove `specs/skill-contract.test.md` from implementation-owned likely touched files, or mark it explicitly as `test-spec stage only`.
- In M1, replace "Amend `specs/skill-contract.test.md` to map R37-R45 to concrete tests" with "Implement the tests defined by the approved `specs/skill-contract.test.md` amendment."
- In M1 tests, replace "test-spec coverage for R37-R45" with concrete test implementation/fixture work derived from the approved test spec.

## Immediate Next Stage

Plan revision. After APD-PLR1 is resolved and plan-review is clean, the immediate next stage is `test-spec`, not implementation.

## Implementation Readiness

Not ready. The plan is close, but implementation should not start until the test-spec boundary is corrected and the test-spec amendment is approved.
