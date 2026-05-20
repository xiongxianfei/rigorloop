# Code Review M1 R1: Spec and Test-Spec Structural Hygiene

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1. Test-spec structural grouping
Reviewed artifact: implementation diff `origin/main..HEAD`
Review date: 2026-05-19
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: CR-M1-001
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/review-log.md
- Review resolution: docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/review-resolution.md
- Reviewed milestone: M1. Test-spec structural grouping
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1
- Required review-resolution: yes
- Finding IDs: CR-M1-001
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `origin/main..HEAD`
- Tracked governing branch state: commit `06360fd` on `proposal/spec-test-structural-hygiene`
- Governing artifacts:
  - `docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md`
  - `specs/skill-contract.md`
  - `specs/skill-contract.test.md`
  - `docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md`
  - `docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml`
- Validation evidence:
  - Requirement coverage row preservation check
  - Acceptance criteria coverage row preservation check
  - Test-case heading preservation check
  - Test-case body preservation check
  - `git diff --check`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene`

## Diff summary

The implementation adds the structural-hygiene proposal, change-local review evidence, an active plan, spec navigation/growth-strategy text, slice headers in the skill-contract Requirements and Acceptance criteria sections, and matching slice headers in the skill-contract test spec's Requirement coverage map, Acceptance criteria coverage map, and Test cases section.

## Findings

### CR-M1-001 - Baseline acceptance criteria are grouped under Foundational

Finding ID: CR-M1-001
Severity: major
Location: `specs/skill-contract.md`, lines 927-937.
Evidence: The new `### Foundational (R1-R7)` acceptance-criteria group includes:

- `A contributor can identify which skills belong to the baseline normalization first slice.`
- `A contributor can identify the later normalization phases without guessing.`
- `A reviewer can confirm that normalized skills include local do-not-overclaim guidance.`

Those criteria correspond to baseline-slice requirements `R8`, `R9`, and `R10`, not the Foundational `R1-R7` band. The test spec's Acceptance criteria coverage map already places the same criteria under `### Baseline normalization first slice (R8-R26)`, so spec/test-spec structural parity is inconsistent.
Required outcome: Acceptance criteria must be grouped under the slice header matching their governing R-clause band while preserving criterion text.
Safe resolution path: Move the three criteria from the Foundational group to the Baseline normalization first slice group in `specs/skill-contract.md`, preserving exact text and order within the baseline slice. Rerun the acceptance-criterion preservation check and lifecycle validation.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | The implementation follows the navigation-only scope, but `CR-M1-001` violates the approved slice grouping for three acceptance criteria. |
| Test coverage | pass | The plan records preservation checks for requirement coverage rows, acceptance criteria coverage rows, test-case headings, and test-case bodies. |
| Edge cases | concern | The named risk "wrong slice header while preserving text" occurred in `specs/skill-contract.md` acceptance criteria. |
| Error handling | pass | No runtime error path is changed; rollback/recovery is documented in the plan. |
| Architecture boundaries | pass | No runtime, data-flow, persistence, deployment, or security architecture boundary is touched. |
| Compatibility | pass | IDs, test-case headings, and cross-reference style are preserved. |
| Security/privacy | pass | Documentation-only change introduces no secrets, credentials, unsafe logging, or auth behavior. |
| Derived artifact currency | pass | No generated output is in scope or touched. |
| Unrelated changes | pass | The diff is limited to the approved proposal/spec/test-spec/plan/change-local surfaces. |
| Validation evidence | concern | Validation is relevant and credible for text preservation, but it did not catch the wrong acceptance-criteria slice grouping identified in `CR-M1-001`. |

## No-finding rationale

Not applicable. One material finding requires resolution before M1 can close.

## Residual risks

- After the grouping fix, rerun preservation checks to confirm the criterion text remains unchanged and only the header boundary changed.

## Handoff

This review is recorded and isolated. No automatic downstream fix was applied. Next stage is `review-resolution` for `CR-M1-001`.
