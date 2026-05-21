# Script Output Optimization Review Resolution

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1

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
