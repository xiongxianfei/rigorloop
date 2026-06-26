# Code Review R3: M3 Broad-Smoke Child Classification

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review skill
Target: M3. Broad-Smoke Child Classification
Reviewed artifact: commit `ca48a834594aca1287499f22fcb27144ffedb1ae`
Reviewed commit: `ca48a834594aca1287499f22fcb27144ffedb1ae`
Review date: 2026-06-26
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r3.md
- Open blockers: none
- Next stage: code-review (final holistic)
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r3.md
- Review log: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md
- Review resolution: not-required
- Reviewed milestone: M3. Broad-Smoke Child Classification
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `ca48a834594aca1287499f22fcb27144ffedb1ae`
- Governing spec: `specs/validation-runtime-follow-through.md`
- Test spec: `specs/validation-runtime-follow-through.test.md`
- Active plan: `docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md`
- M3 evidence: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md`
- Relevant implementation files: `scripts/validation_selection.py`, `scripts/test-select-validation.py`
- Validation evidence inspected: implementation commit body, active plan validation notes, `change.yaml`, and broad-smoke child classification evidence.

## Diff Summary

M3 adds a read-only broad-smoke child classification artifact, registers that artifact as command-output evidence for lifecycle routing, and adds static selector tests that compare the classification rows against the actual `run_broad_smoke` `run_check` calls in `scripts/ci.sh`.

The implementation does not edit `scripts/ci.sh`, enable broad-smoke parallelism, enable caching, compose validators, or claim final verify, branch readiness, PR readiness, or hosted CI success.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M3 covers R16-R19 by producing broad-smoke child classification before parallelism and keeping broad-smoke execution unchanged. R20-R24 boundaries are preserved because no cache, composition, final-verify, branch-readiness, PR-readiness, or hosted-CI claims were introduced. |
| Test coverage | pass | `scripts/test-select-validation.py` adds `test_broad_smoke_child_classification_covers_ci_children`, `test_broad_smoke_classification_blocks_unsafe_candidate_claims`, and `test_broad_smoke_classification_keeps_runtime_sequential`. |
| Edge cases | pass | The unsafe-candidate test checks rows with writes, shared outputs, or low confidence are not clean parallel-safe candidates; the sequential test rejects `ThreadPoolExecutor`, `run_parallel_safe_chunk`, `parallel_safe`, and backgrounded `run_check` calls in broad-smoke. |
| Error handling | pass | Existing broad-smoke failure-output tests remain in place; M3 classification explicitly preserves captured failure output and rerun-command attachment for each child. |
| Architecture boundaries | pass | No persistent worker, cache service, cross-process protocol, broad validator composition, or broad-smoke execution change was introduced. |
| Compatibility | pass | `scripts/ci.sh` is not modified, and the new evidence route only classifies `broad-smoke-child-classification.md` for lifecycle validation. |
| Security/privacy | pass | The classification artifact records commands, read/write behavior, and resource expectations; it does not include secrets, credentials, tokens, private keys, or machine-local debug paths. |
| Derived artifact currency | pass | No generated artifacts are edited in M3. |
| Unrelated changes | pass | The code diff is limited to selector evidence routing and selector regression tests; lifecycle updates are expected plan, metadata, and evidence surfaces for M3. |
| Validation evidence | pass | M3 evidence names the red missing-artifact test, targeted broad-smoke classification tests, registry routing tests, full selector regression, selected-wrapper validation, change metadata validation, review artifact validation, artifact lifecycle validation, and diff hygiene. |

## No-Finding Rationale

The implementation satisfies the M3 objective as an inventory-only slice. The classification artifact records all R17 fields for each broad-smoke child, and the tests bind the table order and IDs to the actual `run_check` list rather than a manually maintained count. Broad-smoke remains sequential because `scripts/ci.sh` is unchanged and the new tests assert the broad-smoke body does not use the selected-mode parallel execution helpers or backgrounded child checks.

The selected-validation route for `broad-smoke-child-classification.md` is deterministic and goes through `artifact_lifecycle.validate`, so the required evidence artifact no longer creates registration debt.

## Residual Risks

The child classifications are still conservative inventory judgments. They do not prove future broad-smoke parallelism is safe, and the plan correctly leaves that to a later approved slice with side-effect and resource-budget proof.

## Handoff

M3 is closed after clean code review. No in-scope implementation milestones remain. The next stage is a final holistic code-review for the complete cross-milestone diff before `explain-change`, `verify`, or PR handoff. This review does not claim final verification, branch readiness, PR readiness, or hosted CI success.
