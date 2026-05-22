# Code Review M2 R2 - Plan Index Archive Validator Contract

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2. Validator contract and fixtures
Reviewed artifact: commits `e04c13d` and `92a2fb9`
Review date: 2026-05-22
Status: clean-with-notes
Recording status: recorded

## Review inputs

- Diff/review surface: `e04c13d M2: validate plan index archive contract`; `92a2fb9 M2: fix plan-body terminal conservation`
- Prior review: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/code-review-m2-r1.md`
- Review resolution: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md#code-review-m2-r1`
- Plan: `docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Spec: `specs/plan-index-lifecycle-ownership.md`
- Test spec: `specs/plan-index-lifecycle-ownership.test.md`
- Changed validator: `scripts/artifact_lifecycle_validation.py`
- Changed tests: `scripts/test-artifact-lifecycle-validator.py`

## Diff summary

M2 implements structural lifecycle validation for plan archive surfaces and explicit plan-body lifecycle markers. The rerun fix adds a plan-body-only terminal conservation regression and updates the validator to run terminal conservation when either plan index surfaces are scoped or a scoped plan body has an explicit terminal lifecycle marker.

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-log.md`
- Review resolution: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md`
- Reviewed milestone: M2. Validator contract and fixtures
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4, M5, M6
- Required review-resolution: no

## Findings

No blocking or required-change findings.

## Prior finding resolution check

| Finding ID | Result | Evidence |
| --- | --- | --- |
| `BPIX-M2-CR1` | pass | `scripts/test-artifact-lifecycle-validator.py` now includes `test_plan_body_terminal_marker_alone_requires_done_location`, which scopes validation to only `docs/plans/2026-05-02-done-plan.md` and expects `terminal plan missing from Done (recent) and Done (archive)`. The validator trigger now includes `_explicit_terminal_plan_body_in_scope`, while `test_plan_lifecycle_marker_does_not_infer_terminal_state_from_prose` preserves the legacy prose-only exemption. |

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `R3g`-`R3p`, `R15`-`R15d`, and `R17b`-`R17h` are represented by marker parsing, terminal conservation, cap/link checks, archive-only nonterminal rejection, and supersession field checks. |
| Test coverage | pass | Direct tests cover valid terminal conservation, missing and duplicate terminal entries, scoped plan-body terminal conservation, prose-only no-inference, recent cap, archive-only nonterminal placement, contradictory/unknown markers, and active supersession structure. |
| Edge cases | pass | EC10, EC11, EC12, EC13, and EC14 have direct fixture coverage; BPIX-M2-CR1 adds the previously missing plan-body-only terminal edge case. |
| Error handling | pass | Invalid markers, missing links, duplicate/missing terminal entries, cap overflow, archive-only nonterminal entries, and invalid active-context placement produce blocking diagnostics. |
| Architecture boundaries | pass | No runtime architecture or ADR boundary is touched. |
| Compatibility | pass | Legacy prose-only plan status is not parsed as terminal, preserving the migration-proof-owned compatibility path. |
| Security/privacy | pass | The validator change uses tracked repository artifacts and does not introduce secrets, host-only state, or hidden lifecycle state. |
| Derived artifact currency | pass | No generated artifacts are changed by M2. |
| Unrelated changes | pass | Diff is scoped to approved lifecycle artifacts, validator code, tests, and change-local review evidence. |
| Validation evidence | pass | Recorded commands include focused regression, full artifact lifecycle test suite, compile check, review artifact validation, change metadata validation, active plan lifecycle validation, and diff hygiene. |

## No-finding rationale

The rerun fix directly covers the prior missing edge case and keeps the explicit marker/no-prose-inference boundary intact. The implementation now satisfies the M2 scope well enough for the migration milestone to use the validator as a structural proof mechanism.

## Residual risks

M3 still owns real index/archive migration, migration-proof quality, and semantic review of compact Done summaries.

## Handoff

Close M2 and proceed to M3 implementation. This review does not claim branch readiness, PR readiness, final verification, or CI status.
