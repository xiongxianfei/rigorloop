# Script Output Optimization Explain Change

## Summary

This change makes `scripts/test-select-validation.py` compact on success and actionable on failure. Default passing runs now emit one ASCII summary line with suite identity, count, and duration; verbose mode preserves full pass detail; quiet success is silent; non-success quiet output still reports the reason.

The work also records the audit, behavior-preservation proof, review resolutions, and CI-wrapper preservation evidence required by the approved lifecycle. `scripts/ci.sh` was not changed because the M4 proof showed the existing wrapper already hides successful child output by default, exposes it under `--verbose`, and expands failed command output.

After the first final-verify attempt, PR-mode selected CI exposed a routing gap for four change-local evidence files created by this initiative. A narrow selector-maintenance patch now routes those evidence files through the existing lifecycle validation check and adds selector regression coverage for that routing.

## Problem

The proposal identified a maintainer-experience defect: passing validation output scaled with work performed instead of information needed to act. A passing 62-test run communicated one actionable fact through a long list of `ok` lines. The approved direction was presentation-only: shorten success output without changing validation behavior, selected tests, failure detection, exit codes, or repair evidence.

## Decision Trail

- Proposal: [docs/proposals/2026-05-21-script-output-optimization.md](/home/xiongxianfei/data/20260419-rigorloop/docs/proposals/2026-05-21-script-output-optimization.md:1)
  - Chose outcome-aware script output: quiet success, specific failure, full detail behind `--verbose`.
  - Resolved proposal-review blockers by fixing the first-slice target, proof route, quiet-mode semantics, zero-test behavior, and preservation-proof requirement.
- Spec: [specs/script-output-optimization.md](/home/xiongxianfei/data/20260419-rigorloop/specs/script-output-optimization.md:1)
  - Defined `[PASS]`, `[FAIL]`, and `[SKIP]` ASCII output conventions for the first slice.
  - Made `--verbose` and `--quiet` mutually exclusive usage errors.
  - Required quiet success to write no stdout or stderr.
  - Deferred new JSON support and required unsupported `--json` to fail without weakening the human-readable contract.
- Architecture: [docs/architecture/system/architecture.md](/home/xiongxianfei/data/20260419-rigorloop/docs/architecture/system/architecture.md:209)
  - Recorded script-output shaping inside the existing selector, test-runner, and CI-wrapper architecture.
  - No ADR was added because this did not introduce a new durable system boundary, persistence model, release model, or source-of-truth decision.
- Test spec: [specs/script-output-optimization.test.md](/home/xiongxianfei/data/20260419-rigorloop/specs/script-output-optimization.test.md:1)
  - Mapped default success/failure, verbose, quiet, conflicting flags, zero-test safety, rerun guidance, JSON deferral, wrapper preservation, and behavior-preservation proof to concrete tests.
- Plan: [docs/plans/2026-05-21-script-output-optimization.md](/home/xiongxianfei/data/20260419-rigorloop/docs/plans/2026-05-21-script-output-optimization.md:1)
  - Split the work into audit/baseline, tests, formatter implementation, CI-wrapper preservation, and lifecycle evidence milestones.
- Post-verify selector-maintenance decision:
  - Final verify found PR-mode CI blocked on `output-contract-red-test.md`, `script-output-audit.md`, `selected-tests-baseline.txt`, and `selected-tests-m3.txt` because those required evidence files were classified as `change-local-unsupported`.
  - The safe fix was to route those exact evidence filenames as `change-local-lifecycle`, reusing `artifact_lifecycle.validate` rather than weakening CI or renaming durable evidence after review.
  - Code-review `code-review-ci-routing-r1` closed this maintenance patch with no material findings.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Evidence |
| --- | --- | --- | --- | --- |
| `scripts/test-select-validation.py` | Added result collection and formatted default output for pass, fail, verbose, quiet, conflict, zero-test, rerun, and unsupported JSON behavior | Implement the approved output contract while preserving the unittest validation surface | spec `R1`-`R24`, test spec `TSRO-001`-`TSRO-010`, plan `M3` | `python scripts/test-select-validation.py` passes 73 tests; focused output-contract tests pass |
| `scripts/test-select-validation.py` tests | Added `ScriptOutputContractTests` and fixture failure coverage, then included them in ordinary validation after M3 review | Make required output-contract cases fail before implementation and pass in the default regression path after implementation | test spec, `SRO-M2-CR1`, `SRO-M3-CR1` | `python scripts/test-select-validation.py ScriptOutputContractTests` passes 10 tests; default command includes the output-contract coverage |
| `docs/changes/2026-05-21-script-output-optimization/script-output-audit.md` | Recorded first-slice audit and target choice | Prove the change starts with `scripts/test-select-validation.py` and avoids broad script rewrites | proposal `SOO-PR1`, spec `R25`-`R27`, plan `M1` | lifecycle validation plus manual route for change-local unsupported audit evidence |
| `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md` | Recorded before/after preservation for exit codes, selected tests, failure detection, failure evidence, verbose behavior, quiet behavior, and CI-wrapper semantics | Protect the presentation-only invariant | proposal `SOO-PR5`, spec `R32`-`R35`, plan `M1`/`M3`/`M5` | selected-test list/hash evidence and M5 preservation proof |
| `selected-tests-baseline.txt`, `selected-tests-m3.txt` | Recorded ordered selected-test identifiers and SHA-256 hashes | Make selected-test preservation durable and reviewable, not count-only | `SRO-M1-CR1`, `SRO-M3-CR1` | baseline hash `sha256:af470dd836f5b1b44c702be35206934f77621a1477d88cafae923e50a7f492bd`; M3 hash `sha256:878bd8dfce24e987ee50ab36d686f54e8d821bf4a5b11fe831d381c57d164047` |
| `output-contract-red-test.md` | Recorded the temporary pre-M3 red-test proof and its closure after M3 | Show old formatter violations without masking them as expected failures | `SRO-M2-CR1` | pre-M3 focused command failed intentionally; post-M3 output-contract cases pass normally |
| `docs/architecture/system/architecture.md` | Added the durable repository architecture note for actionability-scaled validation output | Keep the long-lived architecture package aligned with the approved output contract | architecture stage | architecture-review R1 clean |
| `docs/proposals`, `specs`, `docs/plans`, `docs/plan.md`, `change.yaml` | Added and maintained lifecycle artifacts, requirements, milestone state, validation notes, and active-plan index state | Keep this non-trivial change reviewable and avoid chat-only lifecycle state | repository workflow contract and active plan | metadata, lifecycle, and review-artifact validation |
| `review-log.md`, `review-resolution.md`, `reviews/` | Recorded material findings and clean review receipts across proposal, spec, architecture, plan, and implementation milestones | Preserve review evidence and required dispositions | formal review recording rules | closeout review-artifact validation reports 14 reviews, 10 findings, 14 log entries, and 10 resolution entries |
| `scripts/ci.sh` | No production change | M4 proved existing wrapper behavior already satisfied the first-slice boundary | spec `R28`-`R31`, plan `M4` | wrapper default, verbose, failed-output expansion, and focused wrapper regression proofs passed |
| `scripts/validation_selection.py` | Routed `output-contract-red-test.md`, `script-output-audit.md`, `selected-tests-baseline.txt`, and `selected-tests-m3.txt` as `change-local-lifecycle` | Final verify proved PR-mode CI otherwise blocked before validating required evidence files | post-verify CI blocker, `TSRO-014`, code-review `code-review-ci-routing-r1` | PR-mode CI now passes and selects `artifact_lifecycle.validate` for the evidence files |
| `scripts/test-select-validation.py` selector fixtures | Added exact path fixtures for the four evidence filenames | Keep the selector-routing fix deterministic and regression-tested | selector maintenance review, `TSRO-014` | `python scripts/test-select-validation.py` passes 73 tests |

## Tests Added Or Changed

- `ScriptOutputContractTests` covers default success summary, default failure detail, verbose pass-list preservation, quiet success silence, quiet failure diagnostics, conflicting `--verbose --quiet`, zero-test safety, reliable-only scoped rerun commands, safe broad rerun fallback, and JSON deferral.
- `ScriptOutputFixtureTests.fixture_contract_failure` provides a controlled failing target so failure output can be tested without changing the real validation suite.
- The default validation command now includes output-contract acceptance coverage after the `SRO-M3-CR1` review fix.
- Existing CI-wrapper regression tests were used for M4 to prove default child-output hiding, failed child-output expansion, and verbose output ordering without editing `scripts/ci.sh`.
- Selector regression fixtures now prove the four script-output evidence files classify as `change-local-lifecycle` and route to `artifact_lifecycle.validate`, closing the PR-mode CI blocker found by final verify.

## Validation Evidence Before Final Verify

- `python scripts/test-select-validation.py`
  - M5 result: `[PASS] test-select-validation: 73 passed ...`
- `python scripts/test-select-validation.py ScriptOutputContractTests`
  - M3 result after implementation: 10 output-contract tests passed.
- Focused M3 behavior checks:
  - `--quiet` success: exit 0, empty stdout, empty stderr.
  - `--verbose --quiet`: exit 2, stdout empty, stderr names both flags.
  - `--json`: exit 2 unsupported, preserving JSON deferral.
  - `-k definitely_no_script_output_tests`: exit 1 zero-test `[FAIL]`.
  - `--quiet ScriptOutputFixtureTests.fixture_contract_failure`: exit 1 with `[FAIL]`, failure name, message, location, and scoped rerun.
  - `NoSuchTest`: exit 1 without a misleading scoped `-k` rerun.
- M4 wrapper proof:
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --jobs 1` passed and hid successful child output by default.
  - Same command with `--verbose` passed and exposed child `[PASS]` output.
  - Focused wrapper regression command passed 3 tests.
- M5 and review-recording proof:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed after `code-review-m5-r1`: 14 reviews, 10 findings, 14 log entries, 10 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the lifecycle-managed artifacts used in M5 and review recording.
  - `git diff --check --` passed.
  - Selected CI after `code-review-m5-r1` passed with `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- Explain-change recording proof:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/explain-change.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed.
  - `git diff --check --` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-21-script-output-optimization/explain-change.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --jobs 1` passed.
- Selector-maintenance and review proof:
  - `python scripts/test-select-validation.py` passed after routing maintenance.
  - `bash scripts/ci.sh --mode pr --base $(git merge-base HEAD main) --head HEAD --jobs 1` passed after routing maintenance, selecting `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed after `code-review-ci-routing-r1`: 15 reviews, 10 findings, 15 log entries, 10 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the review-recording artifacts.
  - `git diff --check --` passed.
  - Selected CI for the review-recording artifacts passed with `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.

These are pre-final-verify results. Final `verify` has not run yet.

## Review Resolution Summary

- Proposal review R1 raised five material findings:
  - `SOO-PR1` first-slice ambiguity.
  - `SOO-PR2` proof-route ambiguity.
  - `SOO-PR3` quiet-mode semantics.
  - `SOO-PR4` zero-test behavior.
  - `SOO-PR5` behavior-preservation proof.
- Spec review R1 raised two material findings:
  - `SRO-SR1` conflicting `--verbose` and `--quiet` behavior.
  - `SRO-SR2` quiet-success wording.
- Code review raised three milestone findings:
  - `SRO-M1-CR1` required ordered selected-test proof and hash.
  - `SRO-M2-CR1` required removing expected-failure masking and recording explicit red-test proof.
  - `SRO-M3-CR1` required output-contract tests to run in the ordinary post-M3 validation path.
- All ten material findings were accepted and resolved in [review-resolution.md](/home/xiongxianfei/data/20260419-rigorloop/docs/changes/2026-05-21-script-output-optimization/review-resolution.md:1).
- Clean follow-up reviews closed M1, M2, M3, M4, M5, and the post-verify selector-routing maintenance patch with no material findings.

## Alternatives Rejected

- Do nothing: rejected because the pass list remained noisy and inconsistent with evidence-efficiency goals.
- Suppress all success output: rejected because pass count and duration are useful for catching silent suite collapse and performance regressions.
- Wrapper-only suppression: rejected as incomplete because local script runs would stay noisy and failure formatting would still depend on raw output.
- New JSON support in the first slice: deferred because it is a separate machine-readable contract.
- Common script-output helper library: deferred until more scripts adopt the pattern and shared abstraction pressure is real.
- Broad CI-wrapper rewrite: rejected by the first-slice boundary and unnecessary after M4 proof.
- Manual-only routing for the four evidence files after final verify: rejected because hosted PR CI uses `scripts/ci.sh --mode pr`, so those files needed deterministic selector routing before PR handoff.

## Scope Control

- The first implementation target stayed `scripts/test-select-validation.py`.
- `scripts/ci.sh` was audited and tested but left unchanged.
- Test selection and validation behavior were preserved except for adding required output-contract acceptance tests to the ordinary validation path after M3.
- No generated adapters, public skills, workflow specs, JSON schema, release artifacts, or lifecycle-validator behavior were changed for this initiative.
- Selector classification logic changed only in the post-verify maintenance patch needed to route this initiative's required evidence files through existing lifecycle validation.
- The shorter output contract does not hide failure evidence behind `--verbose`, and quiet mode remains silent only for successful outcomes.

## Risks And Follow-Ups

- Final local `verify` has not run yet; it remains the next lifecycle stage.
- PR handoff has not happened, and hosted CI has not been observed for this branch.
- If additional scripts adopt the same output shape, a common helper library can be proposed later.
- JSON output and broader CI log standardization remain follow-on proposals, not part of this first slice.
- The selector-routing maintenance is intentionally narrow. Additional change-local evidence filenames should still require explicit routing decisions instead of becoming blanket `docs/changes/**` pass-throughs.

## Readiness

- `explain-change` is complete for this initiative.
- Next stage: `verify`.
- This artifact does not claim final verification, branch readiness, PR readiness, or hosted CI success.
