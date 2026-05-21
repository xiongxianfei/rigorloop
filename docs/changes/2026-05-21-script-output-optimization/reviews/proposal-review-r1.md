# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-21-script-output-optimization.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-21-script-output-optimization.md`
- User-supplied proposal-review result in chat on 2026-05-21
- Governing boundaries: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Result

- Material findings: `SOO-PR1`, `SOO-PR2`, `SOO-PR3`, `SOO-PR4`, `SOO-PR5`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-21-script-output-optimization/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-05-21-script-output-optimization/review-log.md`
- Review resolution: `docs/changes/2026-05-21-script-output-optimization/review-resolution.md`
- Open blockers: first-slice target ambiguity, proof-route ambiguity, output-mode contract gaps, CI-wrapper preservation boundary, behavior-preservation evidence
- Immediate next stage: proposal revision, then plan or spec/test-spec path as clarified
- No automatic downstream handoff: this review does not start spec, plan, implementation, or code-review work.

## Overall verdict

Good direction, changes requested before planning.

The proposal identifies a real maintainer-experience problem: successful script output can be much noisier than the information needed to act. The direction is correct: quiet on success, loud and specific on failure, with `--verbose` preserving full detail and `--quiet` never hiding failure reasons.

The main gaps are scope and testability. The proposal needs an unambiguous first slice, an explicit proof route, sharper quiet-mode semantics, defined zero-test behavior, and behavior-preservation evidence beyond output-shape tests.

## Findings

### SOO-PR1 - First-slice target is still ambiguous

Finding ID: SOO-PR1
Severity: major
Location: `First-slice boundary`, `Scope budget`, `Open questions`
Evidence: The proposal says the first implementation should be audit-first, names `scripts/test-select-validation.py` and `scripts/ci.sh` as candidate first-slice targets, but later asks which script is the exact first target.
Required outcome: Define the first slice unambiguously before planning.
Safe resolution: Add a first-slice decision: audit plus `scripts/test-select-validation.py`, with `scripts/ci.sh` touched only if needed to preserve quiet-success and loud-failure behavior after the runner change.

### SOO-PR2 - Proof route is too conditional

Finding ID: SOO-PR2
Severity: major
Location: `Rollout and rollback`, `Next artifacts`
Evidence: The proposal says to write or amend a focused spec and test spec only if the output contract is not already covered by existing script conventions, while also introducing new default, `--verbose`, `--quiet`, and optional `--json` behavior.
Required outcome: Name the proof route explicitly.
Safe resolution: Require a focused test spec before implementation. Keep spec amendment conditional on whether existing script-output contracts already cover the new output modes.

### SOO-PR3 - `--quiet` semantics need a single decision

Finding ID: SOO-PR3
Severity: major
Location: `Verbosity tiers`, `Open questions`
Evidence: The proposal says `--quiet` success output may be nothing or one minimal summary line, then leaves that choice open.
Required outcome: Decide `--quiet` success behavior before implementation.
Safe resolution: For first-slice scripts, `--quiet` success prints nothing; `--quiet` failure prints the same failure summary and failure details as default mode; exit code is preserved.

### SOO-PR4 - Zero-test behavior is unresolved but central to the success contract

Finding ID: SOO-PR4
Severity: major
Location: `Risks and mitigations`, `Open questions`, `Acceptance criteria`
Evidence: The proposal says pass count is required to avoid silent test collapse but leaves zero selected or zero executed test behavior open.
Required outcome: Define zero-test behavior for first-slice scripts.
Safe resolution: For first-slice test-runner scripts, zero executed tests is a failure unless the mode explicitly permits zero selection; default success summaries include nonzero counts.

### SOO-PR5 - Behavior-preservation proof needs more than output-shape tests

Finding ID: SOO-PR5
Severity: major
Location: `Behavior preservation`, `Testing and verification strategy`
Evidence: The proposal says exit code, selection, failure detection, failure data, validation evidence, and CI semantics remain unchanged, but mostly lists output-shape tests.
Required outcome: Add a preservation matrix for each touched script.
Safe resolution: Require implementation to record baseline and new proof for pass/fail exit codes, selected tests/checks, failure detection, failure evidence, verbose output, quiet failure output, and CI semantics when touched.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal clearly identifies noisy success output and insufficiently actionable log shape. |
| User value | pass | Faster CI/local log scanning and better failure repair context are concrete benefits. |
| Option diversity | pass | The proposal compares do-nothing, silence-on-success, wrapper-only, and outcome-aware script output. |
| Decision rationale | pass | Option 4 follows from improving both local and CI usage while preserving verbose mode. |
| Scope control | concern | First-slice target is ambiguous. See `SOO-PR1`. |
| Architecture awareness | pass | The proposal separates script runner behavior from CI wrapper behavior and avoids generated output changes. |
| Testability | concern | Needs proof route, quiet-mode decision, zero-test rule, and behavior-preservation matrix. |
| Risk honesty | pass | Risks around silent test collapse, over-truncation, quiet-mode errors, and wrapper suppression are named. |
| Rollout realism | concern | Rollout is plausible after first-slice and proof-route decisions are fixed. |
| Readiness for plan | changes-requested | Direction is good; revise the five issues before planning. |

## Scope-preservation result

Pass.

The proposal preserves the user intent to optimize script output, collapse passing logs, keep failure evidence actionable, preserve verbose mode, avoid broad rewrites, and include CI wrapper behavior.

## Recommended next stage

Revise the proposal to resolve `SOO-PR1`, `SOO-PR2`, `SOO-PR3`, `SOO-PR4`, and `SOO-PR5`, then rerun proposal-review before downstream plan reliance.
