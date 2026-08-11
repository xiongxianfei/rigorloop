# Review Resolution: Test-Spec-Review Skill Simplification

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: test-spec-review-r1

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `test-spec-review-r1`
- Findings resolved: 2
- Unresolved findings: 2
- Current result: proposal and spec findings are resolved; test-spec findings require correction and rereview.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `TSRSIM-PR1` | accepted | resolved | Added an independent durable-recording trigger and phase-aware recording overlay without downstream handoff. |
| `TSRSIM-SR1` | accepted | resolved | Added the closed lifecycle-by-handoff matrix and rejected advisory plus workflow-managed before review. |
| `TSRSIM-TSR1` | accepted | open | Align M1 proof with baseline-only evidence and keep completed measurement in M3. |
| `TSRSIM-TSR2` | accepted | open | Add deterministic interrupted-retry and conflicting-review-ID proof. |

## Common Resolution Metadata

- Owner: proposal author
- Owning stage: proposal
- Validation target: revised proposal, lifecycle metadata, and independent proposal-review rerun
- Validation evidence: revised proposal and `evidence/proposal-revision-r2.md`

## Finding Details

### test-spec-review-r1

#### TSRSIM-TSR1 - Correct milestone proof timing

Finding ID: TSRSIM-TSR1
Disposition: accepted
Status: open
Owner: test-spec author
Owning stage: test-spec
Chosen action: Remove T8 from the M1 required test set while retaining baseline measurement evidence in M1 and complete before-and-after measurement in M3.
Rationale: T8 requires the post-refactor package and cannot close before M1 code review.
Validation target: revised milestone proof map, unchanged plan alignment, boundary validation, and independent test-spec rereview.
Validation evidence: pending test-spec revision.

#### TSRSIM-TSR2 - Add recording retry and conflict proof

Finding ID: TSRSIM-TSR2
Disposition: accepted
Status: open
Owner: test-spec author
Owning stage: test-spec
Chosen action: Extend T16 with interrupted identical settlement retry and conflicting review-ID reuse fixtures, steps, expected results, and failure meaning.
Rationale: R13 and PRF-005 require direct temporal proof rather than record-shape inference.
Validation target: revised T16, PRF-005 alignment, existing command ownership, boundary validation, and independent test-spec rereview.
Validation evidence: pending test-spec revision.

### spec-review-r1

#### TSRSIM-SR1 - Close lifecycle and handoff validity

Finding ID: TSRSIM-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add a closed lifecycle-by-handoff validity matrix that permits formal with either handoff mode and advisory only with isolated handoff, and make advisory plus workflow-managed an explicit pre-review stop.
Rationale: Workflow-managed continuation requires current formal review identity and settlement; advisory approval cannot establish implementation eligibility.
Validation target: revised requirements, state invariants, errors, edge cases, acceptance criteria, boundary ownership, static fixture strategy, and independent spec rereview.
Validation evidence: R39, E9, EC13, AC-TSRSIM-019, revised boundary and interaction rows, state and error rules, and `evidence/spec-revision-r2.md`.

### proposal-review-r1

#### TSRSIM-PR1 - Preserve isolated material-finding recording

Finding ID: TSRSIM-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add an independent durable-recording trigger, broaden the conditional reference to recording and formal settlement, and make result and finding resources mandatory for isolated material or blocking outcomes while preserving isolated handoff.
Rationale: Repository governance requires every material finding to be recorded and defines isolation as a handoff restriction, not a recording exemption.
Validation target: revised predicate model, resource assemblies, ownership table, missing-resource behavior, static fixtures, and independent proposal rereview.
Validation evidence: revised `Invocation classification`, `Loaded-resource assemblies`, `Recording-and-settlement reference ownership`, `Structural assets`, `Missing-resource behavior`, `Testing and Verification Strategy`, and `Expected Behavior Changes`; `evidence/proposal-revision-r2.md`.

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale or none exist.
- [x] Every deferred finding has follow-up or none exist.
- [x] Every `needs-decision` finding is resolved or none exist.
- [ ] Test-spec correction validation evidence is recorded.
- [x] Spec correction validation evidence is recorded.
- [x] Proposal revision validation evidence is recorded.
- [x] Closeout status is correct.
