# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M3 closeout rejection and actual-run boundary enforcement
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: VIC-IH-CR-M3-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md`
- Review resolution: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: VIC-IH-CR-M3-001
- Verify readiness: not-claimed
- Next stage: review-resolution for M3

## Review Inputs

- Reviewed commit: `b5f221c` (`M3: enforce helper closeout boundary`)
- Plan: `docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Test spec: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Implementation files: `scripts/validate-change-metadata.py`, `scripts/artifact_lifecycle_validation.py`
- Test files: `scripts/test-change-metadata-validator.py`, `scripts/test-artifact-lifecycle-validator.py`, `tests/fixtures/change-metadata/compact-invalid-helper-closeout-command/change.yaml`
- Validation evidence: M3 validation notes in the active plan and `change.yaml`

## Diff Summary

M3 adds compact change metadata validation that rejects a closeout pass whose lifecycle bundle command is `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop ...` unless a direct `--mode explicit-paths` lifecycle command is also present. It mirrors that closeout-boundary rejection in artifact lifecycle validation and adds fixtures/tests for helper command closeout rejection.

## Findings

### VIC-IH-CR-M3-001

Finding ID: VIC-IH-CR-M3-001
Severity: major
Location: `scripts/validate-change-metadata.py:630`; `scripts/artifact_lifecycle_validation.py:759`

Evidence: The M3 implementation detects helper closeout commands only when the command uses the space-separated spelling `--mode explicit-paths-inner-loop`. `validate-change-metadata.py` only looks for a token exactly equal to `--mode` followed by `explicit-paths-inner-loop`, and `artifact_lifecycle_validation.py` searches for the literal substring `--mode explicit-paths-inner-loop`. Python `argparse` accepts the equivalent form `--mode=explicit-paths-inner-loop`; a compact closeout bundle using that spelling would avoid both new M3 rejection paths while still being the helper mode.

Required outcome: Closeout rejection must apply to helper lifecycle proof commands regardless of whether the mode flag is written as `--mode explicit-paths-inner-loop` or `--mode=explicit-paths-inner-loop`.

Safe resolution path: Normalize lifecycle command mode parsing through token handling that recognizes both `--mode VALUE` and `--mode=VALUE`, then use the same command-mode interpretation in metadata validation and artifact lifecycle validation. Add direct tests or fixtures for the equals-form helper closeout command in both validator paths.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | R150 requires rejecting helper closeout proof commands, but the implementation misses the supported `--mode=explicit-paths-inner-loop` argv spelling. |
| Test coverage | block | Tests cover only the space-separated mode flag and do not prove rejection for the equivalent equals-form command. |
| Edge cases | concern | Direct `cache-hit-inner-loop` evidence rejection remains covered, but helper command spelling variants are not. |
| Error handling | pass | Existing invalid evidence-kind and legacy metadata rejection paths remain intact. |
| Architecture boundaries | pass | The change stays inside metadata and lifecycle validators without broadening cache eligibility. |
| Compatibility | pass | Direct `explicit-paths` closeout evidence remains allowed by the M3 logic. |
| Security/privacy | pass | No new secret, credential, or local-path output surfaces are introduced. |
| Derived artifact currency | pass | No generated artifacts are touched. |
| Unrelated changes | pass | The diff is scoped to M3 closeout-boundary validation and tests. |
| Validation evidence | pass | Recorded M3 commands pass, but they do not cover the equals-form helper command gap. |

## No-Finding Rationale

Not applicable; one material finding requires review-resolution before M3 can close.

## Residual Risks

Selector routing and measurement remain planned for M4/M5 and are not assessed as complete in this M3 review.
