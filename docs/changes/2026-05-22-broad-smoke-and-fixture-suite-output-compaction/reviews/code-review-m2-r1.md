# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2. Broad-smoke capture and wrapper-mode consistency guard in working tree
Status: changes-requested

## Review inputs

- Review surface: M2 working-tree diff for `scripts/ci.sh`, `scripts/test-select-validation.py`, `behavior-preservation.md`, `script-output-layer-audit.md`, `broad-smoke-child-commands-post-m2.txt`, the active plan, plan index, and change metadata.
- Governing artifacts: `specs/script-output-optimization.md` R39 through R52 and R63 through R65; `specs/script-output-optimization.test.md` TSRO-017, TSRO-018, TSRO-019, and TSRO-020; M2 in `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`.
- Validation evidence: M2 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml` and the active plan, including focused broad-smoke tests, default/verbose broad-smoke runs, selected explicit CI, lifecycle validation, metadata validation, review-artifact validation, and patch hygiene.
- Related code inspected: current `scripts/ci.sh` `run_check`, `run_broad_smoke`, and the M2 broad-smoke wrapper tests in `scripts/test-select-validation.py`.

## Diff summary

M2 changes broad-smoke `run_check` to capture combined child stdout/stderr, suppress successful child output by default, print captured output on failure, emit successful child output under `--verbose`, and replace streamed success output with one aggregate `[PASS] broad-smoke` line. It adds wrapper tests for broad-smoke default success, failure evidence, verbose output, and a structural consistency guard. It also records post-M2 behavior-preservation evidence and unchanged broad-smoke command identity.

## Findings

### BSO-M2-CR1: Wrapper-mode consistency guard does not check every orchestration mode

Finding ID: BSO-M2-CR1
Severity: major
Location: `scripts/test-select-validation.py:661`

Evidence: `assert_ci_wrapper_consistency_guard_passes` extracts only the `run_check()` function body and asserts that it contains `"$@" 2>&1`, `Captured output:`, and `verbose`, and that the body does not contain a bare `"$@"` line. The negative fixture is also only a non-capturing `run_check()` body. This proves the broad-smoke helper captures output, but it does not inspect the `scripts/ci.sh` orchestration modes or fail if a future mode runs validation producers through another direct-streaming path outside `run_check`.

The approved spec requires R51: "A wrapper-mode consistency guard MUST check every `scripts/ci.sh` orchestration mode that runs validation producers." R52 further requires each checked mode to either use capture-on-success/show-on-failure-or-verbose behavior or carry a documented exception. TSRO-020 requires a guard against every orchestration mode that runs validation producers, plus a negative fixture that introduces a validation-producing mode without capture or documented exception.

Required outcome: The M2 guard must be broadened so it checks every `scripts/ci.sh` orchestration mode that runs validation producers, or explicitly recognizes an approved documented exception. It must fail for a negative fixture that adds a validation-producing orchestration mode or path that streams child output directly without capture.

Safe resolution path: Add a structural helper that enumerates the repository-owned orchestration paths in `scripts/ci.sh` that can run validation producers, including selected-CI paths and broad-smoke, and asserts each uses the expected capture policy or an approved spec/test-spec exception. Extend the negative fixture so it adds a new validation-producing mode/path outside the current `run_check()` helper and prove the guard fails with that mode/path identified. Keep the existing `run_check` body assertion as one part of the guard, not the whole guard.

## Checklist coverage

- Spec alignment: concern. Broad-smoke capture behavior aligns with R39 through R50, but the wrapper-mode consistency guard does not satisfy R51/R52.
- Test coverage/proof: concern. TSRO-017, TSRO-018, and TSRO-019 have direct tests. TSRO-020 is only partially covered because the guard checks one helper body rather than every relevant orchestration mode.
- Edge cases: pass. Default success suppresses child stdout/stderr, failure output includes captured evidence, and verbose output preserves successful child detail.
- Error handling: pass. Failing child exit status is preserved in the fixture, and failure output names the child, command, exit status, duration, and captured output.
- Architecture boundaries: pass. The implementation stays within existing shell wrapper and test surfaces, with no new helper library or generated-output change.
- Compatibility: pass. Broad-smoke command identity hash remains unchanged; selected explicit CI and `selector.regression` are recorded as passing.
- Security/privacy: pass. The diff does not introduce secret logging or environment dumps; captured output is child command output already owned by validation scripts.
- Derived artifact currency: pass. No generated skills, adapters, or release outputs changed in M2.
- Unrelated changes: pass. The reviewed runtime diff is scoped to `scripts/ci.sh`, `scripts/test-select-validation.py`, and M2 evidence/state updates.
- Validation evidence: concern. The recorded M2 validation is relevant and credible for broad-smoke behavior, but it does not close the R51/R52 guard scope gap.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M2. Broad-smoke capture and wrapper-mode consistency guard
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `BSO-M2-CR1`
Remaining implementation milestones: M2 resolution, M3, M4
Verify readiness: not-claimed
