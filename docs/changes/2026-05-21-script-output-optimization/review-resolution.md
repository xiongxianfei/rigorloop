# Script Output Optimization Review Resolution

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m3-r1
Review closeout: code-review-m3-r2

## Resolution Entries

### proposal-review-r1

## Findings

#### SOO-PR1

Finding ID: SOO-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised the scope budget and first-slice boundary to define the first slice as script-output audit plus `scripts/test-select-validation.py`, with `scripts/ci.sh` touched only if the audit or runner change shows a wrapper update is needed.
Rationale: The first slice needs a single target boundary before planning so script-runner work does not expand into a broad CI wrapper rewrite.
Validation target: Proposal defines an unambiguous first-slice decision.
Validation evidence: Proposal sections `Scope budget` and `First-slice decision`.

#### SOO-PR2

Finding ID: SOO-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added a `Proof route` section requiring a focused test spec before implementation and keeping spec amendment conditional on an existing-contract gap.
Rationale: The proposal introduces new output-mode behavior, so downstream planning needs an explicit proof route.
Validation target: Proposal blocks implementation until the plan names an approved proof route.
Validation evidence: Proposal sections `Proof route`, `Testing and verification strategy`, and `Rollout and rollback`.

#### SOO-PR3

Finding ID: SOO-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Defined `--quiet` success as no output and `--quiet` failure as the same failure summary and failure details as default mode for first-slice scripts.
Rationale: Quiet mode should be useful for wrappers and shell pipelines without hiding failure evidence.
Validation target: Proposal defines single quiet-mode semantics for first-slice scripts.
Validation evidence: Proposal sections `Verbosity tiers`, `Quiet-mode decision`, and `Acceptance criteria`.

#### SOO-PR4

Finding ID: SOO-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added zero-test behavior for first-slice test-runner scripts: zero executed tests fail unless an explicit mode permits zero selection, and success summaries include nonzero counts.
Rationale: Pass counts are useful only if they cannot mask silent suite collapse.
Validation target: Proposal defines zero-test behavior before implementation.
Validation evidence: Proposal sections `Zero-test behavior`, `Risks and mitigations`, and `Acceptance criteria`.

#### SOO-PR5

Finding ID: SOO-PR5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added a behavior-preservation proof matrix requiring baseline and new evidence for exit codes, selected tests/checks, failure detection, failure evidence, verbose output, quiet failure output, and CI semantics when touched.
Rationale: Output-shape tests alone do not prove the change preserved validation behavior, selected checks, or exit codes.
Validation target: Proposal requires preservation evidence for each touched script.
Validation evidence: Proposal sections `Behavior-preservation proof`, `Testing and verification strategy`, and `Acceptance criteria`.

## Validation

- Proposal revised to resolve all material findings from `proposal-review-r1`.
- Review log records no open findings for `proposal-review-r1`.
- Downstream planning still requires a proposal-review rerun before reliance.

### proposal-review-r2

No material findings.

### spec-review-r1

## Findings

#### SRO-SR1

Finding ID: SRO-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: spec author
Decision needed: Resolved by spec revision. `--verbose` and `--quiet` are mutually exclusive and combined use fails before tests run.
Chosen action: Added requirements R15a-R15d, Example E9, edge case EC6, and acceptance criterion AC6 specifying that combined `--verbose --quiet` exits with a nonzero usage error, names both flags in stderr, leaves stdout empty, selects and runs no tests, and prints no success, failure, or selected-check summaries.
Rationale: Rejection is clearer and more testable than precedence because the flags express opposite output intent.
Required outcome: The spec defines one testable combined-flag behavior before downstream reliance.
Safe resolution path: Add a requirement that `scripts/test-select-validation.py` rejects combined `--verbose` and `--quiet` with a nonzero usage error naming both conflicting flags, then add matching edge case and acceptance criterion.
Validation target: Revised `specs/script-output-optimization.md` contains deterministic combined-flag behavior.
Validation evidence: Spec sections `Examples first`, `Requirements`, `Error and boundary behavior`, `Edge cases`, and `Acceptance criteria`.

#### SRO-SR2

Finding ID: SRO-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: spec author
Decision needed: Resolved by spec revision. Quiet-mode success writes no stdout or stderr output.
Chosen action: Replaced subjective "no nonessential success output" wording with a no-output stdout/stderr contract in Example E4, R12, and AC5. Added R12a and AC5a clarifying that non-success outcomes may emit bounded actionable diagnostics.
Rationale: Quiet success must be directly testable while preserving failure, usage-error, validation-error, and zero-test diagnostics.
Required outcome: Quiet-mode success has one testable output contract.
Safe resolution path: Replace "no nonessential success output" with "`--quiet` success writes no output to stdout or stderr." Update Example E4 and AC5 to match; limit warnings or usage diagnostics to non-success outcomes if needed.
Validation target: Revised `specs/script-output-optimization.md` contains deterministic quiet-success output behavior.
Validation evidence: Spec sections `Examples first`, `Requirements`, and `Acceptance criteria`.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

## Findings

#### SRO-M1-CR1

Finding ID: SRO-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Added `selected-tests-baseline.txt` with the ordered selected unittest identifiers, recorded the SHA-256 hash and hash input rule in `behavior-preservation.md`, and updated the selected tests/checks matrix row to reference the list and hash.
Rationale: The approved test spec requires count/list/hash or another stable proof for the selected test/check set. Count alone cannot prove a later presentation-only change preserved the same selected tests.
Required outcome: M1 baseline evidence must let reviewers compare the post-change selected test/check set against the baseline without relying only on the count.
Safe resolution path: Generate an ordered list of baseline unittest identifiers or a stable hash from that ordered list, record it in `behavior-preservation.md` or linked change-local evidence, update the matrix row, and rerun M1 validation.
Validation target: Review-resolution rerun proves `behavior-preservation.md` contains durable selected-set proof and the change-local review artifacts remain structurally valid.
Validation evidence: `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/script-output-audit.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/selected-tests-baseline.txt --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md`, `git diff --check --`, and selected CI passed after the evidence update.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

## Findings

#### SRO-M2-CR1

Finding ID: SRO-M2-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Removed `@unittest.expectedFailure` masking from `ScriptOutputContractTests`, excluded that class from ordinary validation through `load_tests`, added `ValidationSelectionTests.test_output_contract_red_tests_are_unmasked_and_separate` as a default guard, and recorded explicit red-test proof in `output-contract-red-test.md`.
Rationale: The approved M2 proof route requires tests that fail for old noisy output and pass only when the approved output contract is satisfied. `unittest.expectedFailure` makes the normal test command pass while required formatter behavior is still absent.
Required outcome: M2 must expose unmet output-contract behavior as failing proof or otherwise ensure M3 validation fails if any required output-contract case remains expected-failing.
Safe resolution path: Remove `@unittest.expectedFailure` from acceptance tests, or move pre-M3 red proof into a separate explicit command/artifact and add a guard that prevents M3 handoff while expected-failure output-contract cases remain.
Validation target: Rerun `python scripts/test-select-validation.py`, explicit red-test proof, selected CI, lifecycle validation, change metadata validation, and diff check after the M2 test proof is revised.
Validation evidence: `python scripts/test-select-validation.py` passed with 63 tests; `python scripts/test-select-validation.py ScriptOutputContractTests` exited nonzero with `FAILED (failures=9)` as pre-M3 red-test proof; lifecycle validation, change metadata validation, selected CI, and `git diff --check --` passed after the test-proof update.

### code-review-m2-r2

No material findings.

### code-review-m3-r1

## Findings

#### SRO-M3-CR1

Finding ID: SRO-M3-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Removed the post-M3 `load_tests` exclusion so `ScriptOutputContractTests` run as part of ordinary `python scripts/test-select-validation.py` validation. Kept the explicit `python scripts/test-select-validation.py ScriptOutputContractTests` command as a focused diagnostic rerun.
Rationale: The required output-contract tests pass only through an explicit command after M3, while the ordinary selector regression command still excludes `ScriptOutputContractTests`.
Required outcome: Ordinary post-M3 validation must execute the required output-contract acceptance cases, or an equivalent ordinary validation guard must fail when any required output-contract case fails.
Safe resolution path: Remove or revise the `load_tests` filter now that the formatter exists, or add an equivalent default-suite guard that invokes `ScriptOutputContractTests`; update behavior-preservation evidence and rerun M3 validation.
Validation target: Rerun `python scripts/test-select-validation.py`, output-contract proof if retained, selected CI, lifecycle validation, change metadata validation, and `git diff --check --` after the test-routing fix.
Validation evidence: `python scripts/test-select-validation.py` passed with `73` tests, including `10` `ScriptOutputContractTests`; `python scripts/test-select-validation.py ScriptOutputContractTests` passed as a focused diagnostic command; selected CI, lifecycle validation, change metadata validation, and `git diff --check --` passed after the test-routing fix.

### code-review-m3-r2

No material findings.
