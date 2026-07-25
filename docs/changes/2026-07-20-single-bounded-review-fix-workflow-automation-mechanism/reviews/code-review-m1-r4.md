# Code Review M1 R4

Review ID: code-review-m1-r4
Stage: code-review
Round: M1 R4
Reviewer: Codex code-review skill
Target: M1 correction commit `0cc88d01`
Reviewed artifact: M1 correction commit `0cc88d01`
Reviewed milestone: M1. Unified State Model and Complete Policy Registry
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-21
Recording status: recorded
Material findings: BRF-M1-CR10
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: none
- Next stage: review-resolution M1
- Review status: changes-requested
- Material findings: BRF-M1-CR10
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m1-r4.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m1-r4
- Reviewed milestone: M1. Unified State Model and Complete Policy Registry
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M1-CR10
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction commit `0cc88d01`, with implementation review focused on the policy, validator, and test changes relative to `7e20333b`.
- Tracked governing branch state: clean worktree at `0cc88d01` before R4 evidence recording.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R009`-`BRF-R017`, `BRF-R018`, `BRF-R035`, `BRF-R053`, `BRF-R068`-`BRF-R079`, and `BRF-R081`-`BRF-R084`.
- Governing architecture and ADR: the approved specification owns semantics; one immutable typed policy projection owns predecessor and next-stage calculation.
- Test spec: T3-T5 and T14, with M1 limited to policy and structural-validation proof.
- Active plan: M1 review-requested handoff in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.

## Risk Map

Blind-first inspection prioritized cyclic target reachability, exact-target stopping behavior, conditional and correction routing, repeated-stage occurrence identity, policy-source immutability, hostile evidence values, and validator crash safety. The falsifiable questions were whether a post-target operation could reach the same target through a cycle, whether occurrence identity prevents that bypass, whether correction after an exact review target is rejected, and whether nested non-deterministic evidence fails safely. M2 state writes, command routing, legacy cutover, external actions, and generated adapters remained out of scope.

## Diff Summary

The correction replaces validator-local rank/frontier tables with typed workflow positions and an immutable adjacency projection, validates receipt `from_position` against the operation predecessor set, uses graph reachability to bound operations by run and parent targets, and recursively rejects stripped-empty, non-finite, cyclic, and over-nested evidence. It also updates M1 tests and lifecycle evidence. It does not add a writer, coordinator, public route, or compatibility adapter.

## Prior-Finding Reconciliation

| Finding | R4 result | Evidence |
| --- | --- | --- |
| `BRF-M1-CR8` | failed-remediation | Immutable ownership and immediate predecessor checks are present, but cyclic graph reachability accepts operations after an exact target has already been reached. The required correction and repeated-stage contrast proof is incomplete. |
| `BRF-M1-CR9` | resolved | Direct whitespace, NaN, positive/negative infinity, nested invalid, cyclic, excessive-depth, finite numeric, and large-integer checks behave deterministically without validator failure. |

## Findings

### BRF-M1-CR10: Cyclic reachability permits execution beyond the exact target boundary

Finding ID: BRF-M1-CR10
- Severity: major
- Location: `scripts/workflow_automation_policy.py:258`, `scripts/workflow_automation_policy.py:259`, `scripts/workflow_automation_policy.py:391`, `scripts/validate_workflow_automation.py:381`, `scripts/test-workflow-automation-policy.py:64`, `scripts/test-validate-workflow-automation.py:593`
- Evidence: `can_reach_target` performs unqualified graph search. Because `implement -> code-review -> implement` and `proposal -> proposal-review -> proposal` are cycles, the validator treats post-target work as being “toward” the target. A complete receipt for `code-review@M1`, with canonical `from_position: implement`, validates with no errors when the exact run and parent target is `implement@M1`, even though `BRF-R081`-`BRF-R082` require that target to stop at `review-requested` without implying or executing review. A second complete receipt for proposal correction, with `from_position: proposal-review`, validates with no errors when the exact target is `proposal-review`, contrary to `BRF-R053` exact-target stopping semantics. The new tests assert adjacency membership and generic reachability but do not exercise these complete validator contrasts. This is a failed remediation of the correction/repeated-stage portion of `BRF-M1-CR8`.
- Required outcome: Target-bound validation must prove that the concrete transition remains before or at the exact structured target for its workflow episode and occurrence; it must reject transitions that start after that target was reached even when a later cycle can revisit the same stage name.
- Safe resolution path: Replace unqualified stage-name reachability with an immutable typed transition rule evaluated from `from_position`, operation stage/occurrence, structured target, and required branch context. Encode conditional edges such as proposal correction and next-milestone implementation with explicit predicates or target-frontier semantics. Fail closed when the current M1 structural record lacks enough occurrence or branch evidence. Add complete-state regressions that reject `code-review@M1` under exact `implement@M1` and proposal correction under exact `proposal-review`, while retaining legitimate earlier-stage/later-target, architecture-not-applicable, correction-to-later-target, rereview, and repeated-next-milestone cases with concrete identities.
- auto_fix_class: none
- needs-decision rationale: none

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Exact target stopping under `BRF-R053` and `BRF-R081`-`BRF-R082` is bypassed by cyclic reachability. |
| Test coverage | block | The correction/repeated-stage tests inspect policy membership but omit complete exact-target negative states. |
| Edge cases | block | Two post-target cyclic transitions validate successfully. |
| Error handling | block | Invalid post-target receipts return no actionable validation error. |
| Architecture boundaries | concern | Policy ownership is now immutable and centralized, but `next_stage_calculation` is represented as unconditional adjacency rather than a deterministic branch-aware calculation. |
| Compatibility | pass | No public command, writer, migration, or legacy compatibility path changed. |
| Security/privacy | pass | No secrets, credentials, logging, network, or external-action behavior changed. |
| Derived artifact currency | pass | No generated or adapter artifact changed. |
| Unrelated changes | pass | The implementation remains scoped to M1 policy/state validation and review evidence. |
| Validation evidence | concern | Focused suites pass, but direct complete-state reproductions show the selected contrasts are insufficient. |

## No-Finding Rationale

Not applicable; this review has one material finding.

## Direct Proof and Validation Challenge

- `python scripts/test-workflow-automation-policy.py` passed 11 tests.
- `python scripts/test-validate-workflow-automation.py` passed 35 tests.
- `python scripts/test-change-metadata-validator.py -k workflow_automation` passed 4 selected tests.
- Direct complete-state proof: `code-review@M1` under exact `implement@M1` target returned no validation errors.
- Direct complete-state proof: proposal correction after `proposal-review` under exact `proposal-review` target returned no validation errors.
- Direct excessive-depth proof returned the expected bounded-nesting validation error.

## Residual Risks

M2 transaction writes, engine routing, stage invocation, compatibility migration, public activation, and final cross-milestone behavior remain unimplemented and were not reviewed as working behavior.

## Recommended Next Stage

Enter `review-resolution` for `BRF-M1-CR10`, return M1 to `review-requested` after proof-first exact-target regressions and the full M1 validation set pass, then rerun code-review M1. Do not start M2 before M1 is approved and closed. This direct review is isolated and performs no automatic downstream handoff.
