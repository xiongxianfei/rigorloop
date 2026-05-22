# Code Review M3 R1 - Compact Change Validation Metadata

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M3. Reconstruction, Summary Derivation, Review Counts, And Compactness Proof
Reviewed artifact: commit `3de6253` (`M3: add compact metadata evidence checks`)
Review date: 2026-05-21
Status: changes-requested
Recording status: recorded

## Review inputs

- Diff/review surface: commit `3de6253`, including `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py`, M3 compact fixtures, active plan updates, plan index updates, and change metadata updates.
- Tracked governing branch state: committed proposal, approved spec, approved test spec, active plan with M3 `review-requested`, and M1/M2 code-review closeout through `7107def`.
- Governing artifacts:
  - `specs/compact-change-validation-metadata.md`
  - `specs/compact-change-validation-metadata.test.md`
  - `docs/plans/2026-05-21-compact-change-validation-metadata.md`
- Validation evidence:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-summary-conflict/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid-review-counts/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-review-counts/change.yaml`
  - `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/review_artifact_validation.py`
  - `git diff --check --`
  - active change metadata, review-artifact closeout, and lifecycle explicit-path validation before M3 handoff

## Diff summary

M3 adds compact path-set reconstruction helpers, summary consistency checks, skipped-event validation, review-artifact count cross-checking through the existing parser, compactness measurement helper coverage, no-execution test coverage for bundle commands, and fixtures for M3 valid and invalid compact metadata. The active plan and change metadata now mark M3 implementation as review-requested.

## Findings

### CVM-M3-CR1 - Extra summary blockers are accepted as derived truth

Finding ID: CVM-M3-CR1
Severity: major
Location: `scripts/validate-change-metadata.py:1185`
Evidence: `validate_compact_summary` derives `blocker_stages` from stored `validation_summary.open_validation_blockers` and checks only whether non-pass events are missing blockers. It never rejects blocker entries whose `stage` does not correspond to a derived non-pass event. A compact file can therefore record all events as `pass`, set `validation_summary.all_passed: false`, add an arbitrary blocker, and pass this summary-consistency check even though R46 says stored summary fields that disagree with event-derived truth must fail and R50 says open blockers are derived from non-pass events.
Required outcome: Compact validation must reject `open_validation_blockers` entries that are not derived from a non-pass event requiring blocker representation. The stored blocker list must be checked as derived data, not only as a minimum set.
Safe resolution path: Derive the expected blocker stages from `validation_events` and accepted skip rules. Compare the stored blocker stages to that derived set, rejecting missing blockers and extra blockers with stable diagnostics. Add an invalid fixture proving an all-pass event list with an extra blocker fails.

### CVM-M3-CR2 - Compactness proof is not the representative reconstruction-gated fixture proof required by M3

Finding ID: CVM-M3-CR2
Severity: major
Location: `scripts/test-change-metadata-validator.py:316`
Evidence: `test_compact_common_read_reduction_helper` measures byte reduction on inline strings, not on a representative high-rerun legacy/compact fixture pair. The compact string is not a valid compact `change.yaml` common-read surface: it omits required `lifecycle_stage`, complete `validation_summary`, counts, and reconstruction-preservation validation. The test never validates the compact fixture or calls `reconstruct_compact_path_sets` before measuring the threshold. This does not satisfy R59-R61, AC23, the M3 plan's compactness-proof step, or TCVM-019's requirement that reconstruction, summary, and count preservation pass before the 30% size check is evaluated.
Required outcome: M3 must include a representative high-rerun legacy/compact proof where the compact common-read surface is measured only after reconstruction preservation passes.
Safe resolution path: Add a representative fixture pair, or equivalent tracked fixture surfaces, with repeated legacy validation evidence and an equivalent compact form. The test must first validate/reconstruct the compact evidence and only then assert the compact common-read surface is at least 30% smaller. Avoid using a trivial inline string that is not itself contract-valid compact metadata.

### CVM-M3-CR3 - No-execution sentinel test would pass even if the bundle command ran

Finding ID: CVM-M3-CR3
Severity: major
Location: `scripts/test-change-metadata-validator.py:338`
Evidence: `test_compact_validator_does_not_execute_bundle_commands` uses `command: python -c create_compact_command_sentinel` and then checks that a sentinel file does not exist. If that command were actually executed by a future regression, Python would raise a `NameError` and still would not create the sentinel file. The test therefore does not prove TCVM-020 or AC24 because it would pass for the relevant failure mode.
Required outcome: The no-execution test must use a bundle command that would create the sentinel file if executed and remain valid as compact command metadata. The validator must still pass the metadata without creating the sentinel.
Safe resolution path: Replace the inert command string with a command that writes the sentinel path if executed, for example a `python -c` command whose script writes a repo-relative sentinel file. Keep the assertion that the sentinel file is absent after metadata validation.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | M3 implements much of R29-R32 and R43-R50, but CVM-M3-CR1 violates R46/R50 derived-summary consistency and CVM-M3-CR2 leaves R59-R61/AC23 unproven. |
| Test coverage | block | M3 adds many useful fixtures, but the compactness proof is not representative/reconstruction-gated and the no-execution sentinel test would pass for the regression it is meant to catch. |
| Edge cases | block | Named M3 edge cases for extra summary drift, reconstruction-gated compactness, and command no-execution proof are not fully covered. |
| Error handling | concern | Invalid summary/count states produce stable diagnostics for several cases, but extra blocker drift has no rejection path. |
| Architecture boundaries | pass | The implementation stays in the existing validator/test/fixture surfaces and reuses the existing review-artifact parser instead of creating a parallel parser. |
| Compatibility | pass | Legacy metadata remains on the existing validation path, and the recorded legacy/basic fixture validation passed. |
| Security/privacy | concern | The validator code does not execute commands, but the direct no-execution regression test is ineffective for proving that boundary. |
| Derived artifact currency | pass | No generated artifacts are involved; plan and change metadata were updated for the M3 handoff. |
| Unrelated changes | pass | Reviewed commit `3de6253` contains compact-metadata implementation, tests, fixtures, and lifecycle state only. Separate lifecycle title-case edits and untracked learn artifacts remain outside this review surface. |
| Validation evidence | concern | The recorded commands are relevant, but they do not cover the extra-blocker drift and do not provide a valid reconstruction-gated compactness proof or effective no-execution sentinel proof. |

## No-finding rationale

Not applicable; this review found material M3 issues.

## Residual risks

- Review-artifact count cross-checking is tied to current parser closeout counts; rerun review should re-check whether this is compatible with any stage-level historical count semantics after the material findings are fixed.
- This review does not claim final branch, verify, CI, or PR readiness.

## Milestone handoff

- Reviewed milestone: M3. Reconstruction, Summary Derivation, Review Counts, And Compactness Proof
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 fixes
- Required review-resolution: yes
- Next stage: review-resolution for CVM-M3-CR1, CVM-M3-CR2, and CVM-M3-CR3
