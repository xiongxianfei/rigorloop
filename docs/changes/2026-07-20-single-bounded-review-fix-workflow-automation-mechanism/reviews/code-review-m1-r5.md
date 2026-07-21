# Code Review M1 R5

Review ID: code-review-m1-r5
Stage: code-review
Round: M1 R5
Reviewer: Codex code-review skill
Target: M1 correction commit `edfd5497`
Reviewed artifact: M1 correction commit `edfd5497`
Reviewed milestone: M1. Unified State Model and Complete Policy Registry
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-21
Recording status: recorded
Material findings: BRF-M1-CR11
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: none
- Next stage: review-resolution M1
- Review status: changes-requested
- Material findings: BRF-M1-CR11
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m1-r5.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m1-r5
- Reviewed milestone: M1. Unified State Model and Complete Policy Registry
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M1-CR11
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: commit range `0cc88d01..edfd5497`, focused on the four changed policy, validator, and test modules before lifecycle evidence was consulted.
- Tracked governing branch state: clean worktree at `edfd5497` before R5 evidence recording.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R009`-`BRF-R017`, `BRF-R035`, `BRF-R053`, `BRF-R069`-`BRF-R071`, `BRF-R079`, and `BRF-R081`-`BRF-R084`.
- Test spec: T3-T5 and T14, with M1 owning the immutable policy and structural validation surfaces and later milestones owning live coordination.
- Active plan: M1 review-requested handoff in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.

## Risk Map

Blind-first inspection challenged exact-target overrun, valid-path rejection, conditional branch enforcement, repeated-stage occurrence enforcement, parent/capability versus receipt consistency, malformed transition vocabulary, and policy-projection immutability.

The falsifiable questions were whether a conditional edge can execute without its guard, whether a repeated-stage edge can ignore `same-milestone` or `next-milestone`, whether exact targets still stop cyclic work, and whether valid correction and conditional paths remain representable.

M2 persistence, public command routing, migration, external actions, generated adapters, and final composed-engine behavior remained out of scope.

## Diff Summary

The correction replaces breadth-first cyclic reachability with frozen `TransitionRule` records carrying predecessor, operation, allowed target frontier, guard, and occurrence constraint.

Receipt target validation now selects a rule by predecessor, operation, and target stage.

The tests add the two exact-target negative fixtures and closed-vocabulary checks for the new rule fields.

The correction does not add a writer, coordinator, public route, or migration adapter.

## Prior-Finding Reconciliation

| Finding | R5 result | Evidence |
| --- | --- | --- |
| `BRF-M1-CR10` | failed-remediation | The two named exact-target reproductions now fail as intended, but the accepted required outcome also required branch- and occurrence-aware evaluation and fail-closed handling when context is absent. The runtime selectors never inspect `guard` or `occurrence_constraint`, and complete invalid conditional and repeated-stage receipts still pass. |

## Findings

### BRF-M1-CR11: Transition predicates are recorded but never enforced

Finding ID: BRF-M1-CR11
- Severity: major
- Location: `scripts/workflow_automation_policy.py:191-214`, `scripts/workflow_automation_policy.py:260-270`, `scripts/workflow_automation_policy.py:282-294`, `scripts/workflow_automation_policy.py:632-650`, `scripts/validate_workflow_automation.py:365-410`, `scripts/test-workflow-automation-policy.py:52-107`, `scripts/test-validate-workflow-automation.py:598-684`
- Evidence: `TransitionRule` records `guard` and `occurrence_constraint`, but `can_transition`, `can_transition_toward_target`, and `can_operation_toward_target` select rules using only predecessor, operation, and target membership. The validator passes no branch or source-occurrence evidence to those selectors. A complete `architecture-assessment -> plan` receipt with only proposal input identity and no architecture-applicability evidence returns `[]`, so the `architecture-not-required` guard is decorative. A complete `code-review -> implement@M99` receipt toward final `verify`, with no source milestone or plan-order evidence, also returns `[]`, so `next-milestone` is decorative. This contradicts `BRF-R015`-`BRF-R017`, the complete next-stage policy required by `BRF-R079`, and the accepted `BRF-M1-CR10` outcome requiring branch- and occurrence-aware evaluation that fails closed when context is absent.
- Required outcome: Transition validation must evaluate every selected rule's guard and occurrence constraint against concrete, identity-bound receipt/canonical evidence; absence, mismatch, or ambiguity must fail closed. A policy field that is not yet executable in M1 must not be presented or validated as an enforced transition permission.
- Safe resolution path: Define typed evaluation inputs for architecture applicability, review/correction state, CI trigger, all-milestones-closed state, source and destination milestone identities, and plan order. Make the transition selector return a matching rule only after its guard and occurrence constraint pass. Require the receipt or authoritative basis to carry the identities needed for that evaluation. Add complete-state negative fixtures for missing/wrong guard evidence and arbitrary/same/out-of-order next milestones, plus positive fixtures for architecture-required, architecture-not-required, same-milestone review, and the unique next milestone. Keep later engine execution deferred, but make M1 structural validation fail closed when required context is absent.
- auto_fix_class: none
- needs-decision rationale: none; the approved specification and accepted review outcome already determine the safe behavior.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Conditional and repeated-stage rule predicates are not enforced, contrary to `BRF-R015`-`BRF-R017` and the complete policy contract in `BRF-R079`. |
| Test coverage | block | The tests prove target-frontier membership and enum typing, but contain no complete guard or occurrence-constraint contrasts. |
| Edge cases | block | Missing architecture applicability and arbitrary next-milestone identity both validate successfully. |
| Error handling | block | Missing predicate context returns no actionable error instead of failing closed. |
| Architecture boundaries | concern | The immutable policy remains the owner, but executable selectors discard two policy fields that determine routing. |
| Compatibility | pass | No public command, legacy adapter, migration, or writer changed. |
| Security/privacy | pass | No secrets, network access, authentication, logging, or external-action behavior changed. |
| Derived artifact currency | pass | No generated or adapter artifact is part of this correction. |
| Unrelated changes | pass | The implementation remains scoped to M1 policy/validator behavior and lifecycle evidence. |
| Validation evidence | concern | All focused suites pass, but direct complete-state adversarial proof demonstrates the suites do not cover the declared predicates. |

## No-Finding Rationale

Not applicable; this review has one material finding.

## Direct Proof and Validation Challenge

- `python scripts/test-workflow-automation-policy.py` passed 13 tests.
- `python scripts/test-validate-workflow-automation.py` passed 37 tests.
- `python scripts/test-change-metadata-validator.py -k workflow_automation` passed 4 selected tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` passed before R5 recording.
- Direct complete-state proof: architecture skip without architecture-applicability evidence returned no validation errors.
- Direct complete-state proof: `code-review -> implement@M99` toward final `verify`, without source-milestone or plan-order evidence, returned no validation errors.
- The two exact-target fixtures introduced by the correction now reject their invalid states; the remaining issue is predicate enforcement rather than target-frontier membership.

## Residual Risks

M2 state writes, engine routing, stage invocation, migration, public activation, and final cross-milestone behavior remain unimplemented and were not reviewed as working behavior.

## Recommended Next Stage

Record and resolve `BRF-M1-CR11`, return M1 to `review-requested` only after proof-first predicate-context regressions and the full M1 validation set pass, then rerun code-review M1.

Do not start M2 before M1 is approved and closed.

This direct review is isolated and performs no automatic downstream handoff.
