# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2. Broad-smoke capture and wrapper-mode consistency guard review-resolution for `BSO-M2-CR1`
Status: clean-with-notes

## Review inputs

- Review surface: M2 review-resolution diff for `scripts/test-select-validation.py`, `review-resolution.md`, `review-log.md`, the active plan, plan index, and change metadata after `BSO-M2-CR1`.
- Governing artifacts: `specs/script-output-optimization.md` R51 and R52; `specs/script-output-optimization.test.md` TSRO-020; M2 in `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`.
- Validation evidence: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml` records focused guard validation, broad-smoke default and verbose runs, selected explicit CI, lifecycle validation, review-artifact validation, change-metadata validation, and patch hygiene after `BSO-M2-CR1`.
- Related code inspected: current `scripts/ci.sh` `run_check`, `run_broad_smoke`, `run_selected_mode`, and mode dispatch.

## Diff summary

The review-resolution broadens the wrapper-mode consistency guard in `scripts/test-select-validation.py`. The guard now keeps the helper-level `run_check()` capture assertion, verifies selected-CI and broad-smoke mode dispatch, requires a documented selected-CI policy exception, scans repository-owned `run_*` orchestration functions for validation producer calls outside `run_check`, allows command-array construction, rejects direct producer execution outside `run_check`, and rejects direct bare `"$@"` streaming outside `run_check`.

The test now includes negative fixture coverage for a new validation-producing `run_new_validation_mode()` outside `run_check()` and a direct bare `"$@"` streaming `run_direct_streaming_mode()`. Lifecycle records mark `BSO-M2-CR1` accepted and resolved, with M2 returned for this re-review.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. The broadened guard covers R51/R52 by checking the current `scripts/ci.sh` validation-producing orchestration paths and requiring capture policy or documented exception.
- Test coverage: pass. TSRO-020 is covered by the current-wrapper positive guard plus negative fixtures for a new direct validation producer mode and a direct bare `"$@"` streaming mode.
- Edge cases: pass. The guard keeps the `run_check()` helper assertion, allows command-array construction used by broad-smoke lifecycle/review artifact commands, and still rejects direct producer execution outside capture.
- Error handling: pass. The guard failure messages name the offending mode-like function and direct producer or streaming path, making regressions actionable.
- Architecture boundaries: pass. The fix stays in the existing selector/wrapper regression test surface and does not add a shell parser, shared helper library, or runtime behavior change.
- Compatibility: pass. `scripts/ci.sh` runtime behavior and selected-CI behavior are unchanged by this resolution; the selected-CI exception is documented with spec and test-spec references.
- Security/privacy: pass. The diff adds static test assertions and lifecycle summaries only; it does not add secret logging or broaden runtime output.
- Derived artifact currency: pass. No generated skills, adapters, release artifacts, or public adapter outputs changed.
- Unrelated changes: pass. The reviewed resolution is scoped to the M2 guard gap and lifecycle state/evidence updates.
- Validation evidence: pass. Recorded validation includes `python scripts/test-select-validation.py --verbose -k broad_smoke_wrapper_mode_consistency_guard_is_enforced`, `python scripts/test-select-validation.py --verbose -k broad_smoke`, full `python scripts/test-select-validation.py`, default and verbose broad-smoke, selected explicit CI, lifecycle/review/change metadata validators, and `git diff --check --`.

## No-finding rationale

`BSO-M2-CR1` required the guard to move beyond checking only `run_check()` and to fail when a validation-producing orchestration mode/path streams directly. The updated guard now has two layers: helper-level capture proof and mode/function-level policy scanning. The negative fixtures directly prove the two named regression shapes fail with diagnostics that identify the offending mode/path. The existing broad-smoke behavior tests and recorded validation continue to prove default success capture, failure evidence, verbose output, and selected-CI regression behavior.

## Residual risks

The guard is intentionally semi-structural rather than a full shell parser. It matches the current `scripts/ci.sh` function-based orchestration style and is fixture-backed for the required regression class. If future CI modes are implemented directly in the `case` block instead of through `run_*` functions, the guard should be extended in that future change.

## Handoff

Reviewed milestone: M2. Broad-smoke capture and wrapper-mode consistency guard
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M3. First producer compact default and verbose compatibility
Remaining implementation milestones: M3, M4
Verify readiness: not-claimed
