# Code Review M1 R3

Review ID: code-review-m1-r3
Stage: code-review
Round: M1 R3
Reviewer: Codex code-review skill
Target: M1 correction commit `7e20333b`
Reviewed artifact: M1 correction commit `7e20333b`
Reviewed milestone: M1. Unified State Model and Complete Policy Registry
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-21
Recording status: recorded
Material findings: BRF-M1-CR8, BRF-M1-CR9
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: none
- Next stage: review-resolution M1
- Review status: changes-requested
- Material findings: BRF-M1-CR8, BRF-M1-CR9
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m1-r3.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m1-r3
- Reviewed milestone: M1. Unified State Model and Complete Policy Registry
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M1-CR8, BRF-M1-CR9
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `7283ab40..7e20333b`.
- Tracked governing branch state: clean worktree at commit `7e20333b` before review evidence recording.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R018`, `BRF-R024`, `BRF-R035`-`BRF-R037`, `BRF-R068`-`BRF-R079`, and `BRF-R101`-`BRF-R102`.
- Governing architecture and ADR: immutable typed policy projection, canonical-position consistency, and capability-bound prepared receipts.
- Test spec: T3-T8 and T14-T15.
- Active plan: M1 review-requested handoff in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.

## Risk Map

Before consulting validation summaries or prior finding dispositions, the review prioritized policy/validator drift, impossible predecessor transitions, repeated-milestone rebinding, placeholder reconciliation evidence, and valid historical-record representation. Direct questions challenged arbitrary and backward `from_position` values, runtime mutation of reachability data, whitespace-only evidence, non-finite evidence, later-target/current-operation behavior, parent target completeness, and prepared/completed receipt distinctions. M2 state writes, public routing, legacy cutover, external actions, credentials, and generated adapters were intentionally out of scope.

## Diff Summary

The correction separates receipt destination from capability operation, adds operation-to-target rank checks, applies the common structured-target validator to parent maxima, recursively checks receipt postconditions and outputs, and expands M1 regressions. It does not add a writer, coordinator, public route, or legacy-state mutation.

## Prior-Finding Reconciliation

| Finding | R3 result | Evidence |
| --- | --- | --- |
| `BRF-M1-CR5` | failed-remediation | Destination equality is corrected, but canonical predecessor position remains unchecked and whitespace/non-finite evidence still passes as concrete. |
| `BRF-M1-CR6` | failed-remediation | The matrix covers the R2 examples but omits impossible/unknown from-position, policy mutation, whitespace, and non-finite evidence contrasts. |
| `BRF-M1-CR7` | resolved | Parent maximum targets now use the complete structured-target validator and reject missing milestone, plan, binding-time, and completion fields. |

## Findings

### BRF-M1-CR8: Receipt reachability ignores canonical from-position and uses a second mutable policy source

Finding ID: BRF-M1-CR8
- Severity: major
- Location: `scripts/validate_workflow_automation.py:94`, `scripts/validate_workflow_automation.py:108`, `scripts/validate_workflow_automation.py:366`, `scripts/validate_workflow_automation.py:981`, `scripts/test-validate-workflow-automation.py:265`
- Evidence: `from_position` is validated only as a nonempty string. A receipt with `from_position: not-a-canonical-position` passes, as does a backward transition from `verify` to a proposal-review capability targeting `spec`. The new `PUBLIC_TARGET_RANK` and `STAGE_TARGET_FRONTIER` tables check only whether an operation ranks no later than a destination; they do not check the canonical predecessor relation. They are also mutable dictionaries in the validator rather than part of `scripts/workflow_automation_policy.py`'s immutable typed projection. Mutating `STAGE_TARGET_FRONTIER['proposal-review']` at runtime changes a previously valid state's result. The coverage test proves key completeness only, not immutable ownership or semantic agreement with `predecessor_rule` and `next_stage_calculation`. This leaves canonical from-position and closed-transition-registry consistency unproven under `BRF-R018`, `BRF-R069`, `BRF-R079`, and the accepted architecture boundary.
- Required outcome: One immutable executable policy projection must own predecessor, operation, and target reachability, and every receipt must bind a recognized canonical from-position to an operation that is valid from that position and toward its destination.
- Safe resolution path: Move the closed position/predecessor/target relation into `workflow_automation_policy.py` as frozen or read-only typed data derived alongside the stage policies; make the validator consume that projection instead of local mutable rank/frontier dictionaries. Add regressions for unknown and backward positions, conditional architecture paths, correction/rereview paths, repeated milestones, semantic projection drift, and attempted runtime mutation.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M1-CR9: Concrete receipt evidence still accepts non-durable scalar placeholders

Finding ID: BRF-M1-CR9
- Severity: major
- Location: `scripts/validate_workflow_automation.py:278`, `scripts/test-validate-workflow-automation.py:624`
- Evidence: `_validate_concrete_value` treats every nonempty string and every integer/float as concrete. Direct fixtures with whitespace-only postcondition text and `float('nan')` both pass. Whitespace is not meaningful completion evidence, while NaN and infinity are not stable JSON identities and cannot support deterministic equality or reconciliation. The negative matrix checks null and empty strings but not stripped emptiness, non-finite numbers, or nested variants. This is a failed remediation of the concrete-evidence portion of `BRF-M1-CR5` and leaves `BRF-R073`-`BRF-R077` evidence-first recovery unsafe.
- Required outcome: Concrete evidence must be serializable, meaningful, and deterministic at every nested level.
- Safe resolution path: Require strings to remain nonempty after stripping, accept only finite numeric values, continue rejecting booleans/null/empty containers, and recursively apply the same rule to nested mappings and arrays. Add direct whitespace, NaN, positive/negative infinity, and nested placeholder regressions while retaining valid finite counts and identity strings.
- auto_fix_class: none
- needs-decision rationale: none

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-R018`, `BRF-R069`, and `BRF-R079` are compressed into mutable rank checks that omit canonical predecessor validation. |
| Test coverage | block | Passing tests omit all independently reproduced R3 cases. |
| Edge cases | block | Unknown/backward positions, mutable policy data, whitespace, and non-finite evidence pass. |
| Error handling | block | Invalid transition/evidence states receive no validation error. |
| Architecture boundaries | block | Validator-local mutable tables become a second executable policy owner. |
| Compatibility | pass | No public route, writer, migration, or legacy compatibility behavior changed. |
| Security/privacy | pass | No secret, credential, network, logging, or external-action surface changed. |
| Derived artifact currency | pass | No generated adapter artifact changed. |
| Unrelated changes | pass | The implementation diff remains scoped to M1 validation and its lifecycle evidence. |
| Validation evidence | concern | The named suites pass, but direct adversarial fixtures prove the selected cases are insufficient. |

## No-Finding Rationale

Not applicable; this review has two material findings.

## Residual Risks

M2 transaction writes, reconciliation execution, orchestration, public command routing, compatibility cutover, and final cross-milestone behavior remain unimplemented and were not reviewed as working behavior.

## Validation Challenge

- `python scripts/test-workflow-automation-policy.py` passed: 9 tests.
- `python scripts/test-validate-workflow-automation.py` passed: 30 tests.
- `python scripts/test-change-metadata-validator.py -k workflow_automation` passed: 4 selected tests.
- Direct fixture: unknown `from_position` passed unexpectedly.
- Direct fixture: backward `verify` to proposal-review operation passed unexpectedly.
- Direct fixture: whitespace-only postcondition passed unexpectedly.
- Direct fixture: NaN postcondition passed unexpectedly.
- Direct mutation: changing `STAGE_TARGET_FRONTIER` changed validation behavior, proving the reachability source is mutable.

## Recommended Next Stage

Enter `review-resolution` for `BRF-M1-CR8` and `BRF-M1-CR9`, return M1 to `review-requested` after targeted and broad validation, and rerun code-review M1. Do not start M2 before M1 is approved and closed. This direct review is isolated and performs no automatic downstream handoff.
