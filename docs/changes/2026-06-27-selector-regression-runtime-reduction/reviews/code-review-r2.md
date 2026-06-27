# Code Review R2: M2 Fixture Reuse and In-Process Selector Conversion

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2. Fixture Reuse and In-Process Selector Conversion
Reviewed artifact: commit `158994be`
Reviewed commit: `158994be`
Review date: 2026-06-27
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r2.md
- Open blockers: none
- Next stage: implement next milestone
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r2.md
- Review log: docs/changes/2026-06-27-selector-regression-runtime-reduction/review-log.md
- Review resolution: docs/changes/2026-06-27-selector-regression-runtime-reduction/review-resolution.md#code-review-r2
- Reviewed milestone: M2. Fixture Reuse and In-Process Selector Conversion
- Milestone closeout: closed
- Remaining implementation milestones: M3
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `158994be`
- Governing spec: `specs/selector-regression-runtime-reduction.md`
- Test spec: `specs/selector-regression-runtime-reduction.test.md`
- Active plan: `docs/plans/2026-06-27-selector-regression-runtime-reduction.md`
- M2 evidence: `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`
- Relevant implementation files: `scripts/validation_selection.py`, `scripts/test-select-validation.py`
- Validation evidence inspected: M2 validation notes in the active plan and change metadata, preservation evidence, actual diff, and tracked commit history.

## Diff Summary

M2 adds a reusable immutable `RepositoryPreflightContext` with repository root, worktree-presence, tracked path, and unmerged path state. `SelectionRequest` can now carry that context, and selector preflight validates that a provided context belongs to the same resolved repository root before reuse.

`ValidationSelectionTests` builds one root preflight context and reuses it for pure selector calls. The default selector command path still builds preflight context internally when no context is provided. The change adds `test_shared_preflight_context_requires_matching_repository_identity` to prove mismatched context reuse fails.

The preservation evidence records the approved unittest identifier delta, the selected-check identity for the M2 touched path set, the representative table runtime improvement, retained CLI/subprocess coverage, and unchanged broad-smoke, cache, final verify, branch-readiness, PR-readiness, and hosted-CI boundaries.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M2 reduces repeated repository-state discovery, matching `R3`, while default `python scripts/test-select-validation.py` remains the complete path under `R1` and `R2`. The diff does not introduce cache, broad-smoke parallelism, workers, broad validator composition, or final/PR readiness behavior forbidden by `R19` and `R28`. |
| Test coverage | pass | The new `test_shared_preflight_context_requires_matching_repository_identity` covers the reusable-context identity guard required by `R30`/EC9. Existing full-command and selector-filtered validation prove the retained default coverage and selector fixtures. |
| Edge cases | pass | EC3 is recorded as an approved test-structure delta in preservation evidence. EC9 has direct proof through the identity-guard test. EC1, EC2, EC6, EC7, and EC10 remain covered by retained default-command, CLI-boundary, missing-route, broad-smoke classification, cache-status, and diagnostics tests cited in preservation evidence. |
| Error handling | pass | `_preflight_results` rejects a context whose resolved root differs from the request root, and `build_repository_preflight_context` preserves the prior non-git behavior by recording `inside_worktree=False` and returning no preflight results. |
| Architecture boundaries | pass | The diff adds no persistent worker, shared cache, broad validator composition, broad-smoke parallel execution, or cross-process protocol. The helper is an in-process test/runtime API seam for selector preflight reuse. |
| Compatibility | pass | Existing callers of `SelectionRequest` need not pass `preflight_context`; default selector behavior still computes preflight internally. Selected-CI compatibility evidence ran the explicit wrapper command and selected `artifact_lifecycle.validate` plus `selector.regression`. |
| Security/privacy | pass | The diff records repository-relative evidence and timing only; no secrets, credentials, tokens, or private keys are introduced. |
| Derived artifact currency | pass | No generated output is changed. Plan body, plan index, preservation evidence, and change metadata are synchronized for M2 review-requested state before this review. |
| Unrelated changes | pass | The functional diff is limited to selector preflight reuse and its regression test; supporting documentation is the approved change-local evidence and plan bookkeeping for the same milestone. |
| Validation evidence | pass | M2 validation evidence includes the identity test, representative table timing, `python scripts/test-select-validation.py -k selector`, full `/usr/bin/time -p python scripts/test-select-validation.py`, selected-CI explicit wrapper proof, artifact lifecycle validation, change metadata validation, review artifact validation, and diff hygiene. |

## No-Finding Rationale

The change targets the measured M2 bottleneck without deleting selector rows or moving coverage to an optional path. Reusing a frozen repository preflight context eliminates repeated `git` discovery for pure selector tests, while the root identity guard prevents cross-repository reuse. The default selector command still exercises the complete suite, subprocess-backed CLI and selected-CI tests remain present, and preservation evidence records the test ID delta and retained behavior surfaces.

## Residual Risks

M2 records one full revised timing run as implementation evidence. M3 still owns the formal revised runtime result YAML, paired-runtime comparison where practical, selected-CI timeout status conclusion, and final follow-up decision. This review does not claim final verification, branch readiness, PR readiness, or hosted CI success.

## Handoff

M2 is closed after clean code review. The next stage is `implement M3`. This review does not start M3 automatically and does not claim final verification, branch readiness, PR readiness, or hosted CI success.
