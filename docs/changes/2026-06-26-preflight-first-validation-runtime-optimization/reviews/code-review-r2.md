# Code Review R2: M2 Selector Preservation and Missing-Route Blockers

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2. Selector Preservation and Missing-Route Blockers
Reviewed artifact: commit `77ca0065fe439153fb10b46ba771a0e965b2158b`
Reviewed commit: `77ca0065fe439153fb10b46ba771a0e965b2158b`
Review date: 2026-06-26
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r2.md
- Open blockers: none
- Next stage: implement next milestone
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r2.md
- Review log: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md
- Review resolution: not-required
- Reviewed milestone: M2. Selector Preservation and Missing-Route Blockers
- Milestone closeout: closed
- Remaining implementation milestones: M3
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `77ca0065fe439153fb10b46ba771a0e965b2158b`
- Governing spec: `specs/validation-runtime-follow-through.md`
- Test spec: `specs/validation-runtime-follow-through.test.md`
- Active plan: `docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md`
- M2 evidence: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md`
- Relevant implementation files: `scripts/validation_selection.py`, `scripts/test-select-validation.py`
- Validation evidence inspected: implementation commit body, active plan validation notes, `change.yaml`, and selector preservation evidence.

## Diff Summary

M2 adds selector preservation proof for the selector-change surface, strengthens the unregistered change-evidence blocker with path-class and affected-class diagnostics, and adds regression coverage proving explicit diagnostic broad-smoke does not turn a missing-route blocker into a clean selected-validation pass.

The implementation records a no-safe-reduction decision for `selector.regression` runtime. It does not enable broad-smoke parallelism, enable caching, compose validators, or claim final verify, branch readiness, PR readiness, or hosted CI success.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M2 covers R7-R15 and R20/R24/R25 by preserving selector identity and failure sensitivity, keeping cache/final-verify boundaries intact, and making the missing-route blocker explicit for unregistered change evidence. |
| Test coverage | pass | `scripts/test-select-validation.py` adds coverage for selector surface identity, unregistered change-evidence diagnostics, and diagnostic broad-smoke preserving the blocked selected-validation result. |
| Edge cases | pass | The diagnostic broad-smoke fixture requests broad-smoke explicitly and asserts `broad_smoke.repo` is selected while `manual-routing-required` still blocks selected validation. |
| Error handling | pass | The missing-route blocker continues to return `status: blocked`, includes the path and blocker ID, adds class fields, and gives corrective guidance to register selector routing or record a complete owner-approved deferral. |
| Architecture boundaries | pass | No persistent worker, cache service, cross-process protocol, broad validator composition, or broad-smoke execution change was introduced. |
| Compatibility | pass | Existing selector APIs and standalone test commands remain compatible; the change only adds diagnostics and regression fixtures. |
| Security/privacy | pass | M2 evidence records local validation facts and no secrets, credentials, tokens, or private keys. |
| Derived artifact currency | pass | No generated artifacts are edited in M2. |
| Unrelated changes | pass | The code diff is limited to selector diagnostics and selector regression tests; lifecycle updates are the expected plan, metadata, and evidence surfaces for M2. |
| Validation evidence | pass | M2 evidence names focused selector tests, full selector regression, selected-wrapper validation with the 300-second timeout, change metadata validation, review artifact validation, artifact lifecycle validation, and diff hygiene. |

## No-Finding Rationale

The implementation satisfies the M2 objective without trading away proof. The selector-change surface still selects `selector.regression`, the additional lifecycle check is explained by the new registered preservation evidence artifact, expected failure fixtures still fail, expected pass fixtures still pass, and diagnostic broad-smoke remains additive evidence rather than a way to clear selected-validation blockers. The no-safe-reduction rationale is explicit and preserves the M1 timeout behavior for follow-up work.

## Residual Risks

The missing-route blocker proof is focused on the unregistered change-evidence class exercised by the existing selector fixtures. Additional known path classes remain a future coverage-expansion risk if M3 or later work adds new artifact classes outside the current selector registry.

## Handoff

M2 is closed after clean code review. The next stage is implementation of M3, `Broad-Smoke Child Classification`. This review does not claim final verification, branch readiness, PR readiness, or hosted CI success.
