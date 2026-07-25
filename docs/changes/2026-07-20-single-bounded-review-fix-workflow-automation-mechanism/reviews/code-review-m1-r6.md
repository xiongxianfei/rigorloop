# Code Review M1 R6

Review ID: code-review-m1-r6
Stage: code-review
Round: M1 R6
Reviewer: Codex code-review skill
Target: M1 correction commit `ff270c41`
Reviewed artifact: M1 correction commit `ff270c41`
Reviewed milestone: M1. Unified State Model and Complete Policy Registry
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-21
Recording status: recorded
Material findings: BRF-M1-CR12
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: none
- Next stage: review-resolution M1
- Review status: changes-requested
- Material findings: BRF-M1-CR12
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m1-r6.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m1-r6
- Reviewed milestone: M1. Unified State Model and Complete Policy Registry
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M1-CR12
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: commit range `edfd5497..ff270c41`, inspected first across the four changed policy, validator, and test modules before consulting the R5 conclusion or implementation validation ledger.
- Tracked governing branch state: clean worktree at `ff270c41` before R6 evidence recording.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R009`-`BRF-R017f`, `BRF-R035`, `BRF-R069`-`BRF-R071`, `BRF-R079`, and `BRF-R081`-`BRF-R084`.
- Test spec: T3-T5 and T14, with M1 owning the immutable policy and structural validation surfaces and later milestones owning live target binding and coordination.
- Active plan: M1 review-requested handoff in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.

## Risk Map

Blind-first inspection challenged whether receipt validation consumes every guard and occurrence constraint, exact targets remain stopping boundaries, repeated-stage targets can still reach their bound later occurrence, malformed evidence fails closed, and valid conditional and milestone paths remain representable.

The decisive falsifiable contrast was whether the same valid `code-review@M1 -> implement@M2` edge is permitted for targets `implement@M2`, `code-review@M2`, and final `verify`, while still rejecting continuation after an already-reached M1 target.

M2 persistence, live canonical-plan reconciliation, public command routing, migration, external actions, generated adapters, and composed-engine behavior remain out of scope.

## Diff Summary

The correction introduces immutable `TransitionContext` and `TransitionEvaluation` records and evaluates transition guards and occurrence constraints before a receipt can authorize an operation.

Receipt validation now supplies input evidence, plan identity, operation milestone identity, and target milestone ID to the typed evaluator. Tests add positive and missing-evidence contrasts for every guard and same/next milestone constraints.

The correction does not add a writer, coordinator, public route, or migration adapter.

## Prior-Finding Reconciliation

| Finding | R6 result | Evidence |
| --- | --- | --- |
| `BRF-M1-CR11` | failed-remediation | Guard and occurrence predicates are now enforced, resolving the two R5 reproductions. However, target permission remains stage-only: the next-milestone rule allows only target stage `verify`, so the evaluator rejects valid transitions toward the bound repeated targets `implement@M2` and `code-review@M2`. The accepted outcome required occurrence-aware transition evaluation without breaking valid repeated-stage paths. |

## Findings

### BRF-M1-CR12: Stage-only target frontiers reject valid later milestone targets

Finding ID: BRF-M1-CR12
- Severity: major
- Location: `scripts/workflow_automation_policy.py:181-188`, `scripts/workflow_automation_policy.py:304-311`, `scripts/workflow_automation_policy.py:662-675`, `scripts/workflow_automation_policy.py:828-854`, `scripts/test-workflow-automation-policy.py:166-351`
- Evidence: The `code-review -> implement` next-milestone rule is created with target frontier `verify`, and `allowed_targets` stores only stage names. With complete source M1, next M2, plan, order, and milestone identity evidence, `evaluate_transition` returns `allowed=False` for persisted targets `implement@M2` and `code-review@M2`, but returns `allowed=True` for final target `verify`. This makes a user unable to stop at the next implementation or its review even though structured targets explicitly bind milestone occurrences. It contradicts `BRF-R009`-`BRF-R013`, the stage/occurrence contract in `BRF-R017a`-`BRF-R017e`, the complete next-stage policy required by `BRF-R079`, and ordered milestone progression in `BRF-R084`.
- Required outcome: Target permission for cyclic/repeated stages must evaluate the structured target occurrence, not only the target stage. A valid transition from reviewed M1 to bound M2 must be allowed when the target is `implement@M2`, `code-review@M2`, or any valid later target, while a target already satisfied at M1 must still stop without continuing.
- Safe resolution path: Replace the stage-only `allowed_targets` decision for repeated-stage edges with an occurrence-aware target-boundary predicate using the persisted target milestone, source milestone, next milestone, and plan/order identities. Add direct positive tests for M1-to-M2 toward `implement@M2` and `code-review@M2`, retain final-verify progression, and add negative tests proving exact `implement@M1` and `code-review@M1` targets cannot advance to M2 or silently rebind.
- auto_fix_class: none
- needs-decision rationale: none; the approved structured-target contract already determines the required behavior.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Valid repeated-stage targets cannot reach their bound milestone occurrence. |
| Test coverage | block | Next-milestone positive coverage uses only target `verify`; it omits `implement@M2` and `code-review@M2` contrast cases. |
| Edge cases | block | The evaluator cannot distinguish an already-reached M1 target from the same stage bound to later M2. |
| Error handling | pass | Missing and contradictory guard/occurrence evidence now produces explicit fail-closed errors. |
| Architecture boundaries | pass | The immutable policy evaluator remains the sole structural transition authority and no writer or public route was added. |
| Compatibility | pass | No public command, legacy adapter, migration, or writer changed. |
| Security/privacy | pass | No secrets, network access, authentication, logging, or external-action behavior changed. |
| Derived artifact currency | pass | No generated or adapter artifact is part of this correction. |
| Unrelated changes | pass | The implementation remains scoped to M1 policy/validator behavior and lifecycle evidence. |
| Validation evidence | concern | All focused suites pass, but the direct complete-context repeated-target contrast exposes the missing proof case. |

## No-Finding Rationale

Not applicable; this review has one material finding.

## Direct Proof and Validation Challenge

- `python scripts/test-workflow-automation-policy.py` passed 15 tests.
- `python scripts/test-validate-workflow-automation.py` passed 41 tests.
- `python scripts/test-change-metadata-validator.py -k workflow_automation` passed 4 selected tests.
- `python scripts/test-change-metadata-validator.py` passed 52 tests.
- Python compilation and `git diff --check edfd5497..ff270c41` passed.
- Direct guard contrasts rejected wrong proposal outcome, incomplete architecture-applicability evidence, non-closed milestone state, and wrong next-milestone identity while accepting the complete final-target next-milestone case.
- Direct repeated-target contrast: complete `code-review@M1 -> implement@M2` evidence returned `allowed=False` for `implement@M2`, `allowed=False` for `code-review@M2`, and `allowed=True` for final `verify`.

## Residual Risks

M2 state writes, engine routing, stage invocation, migration, public activation, and final cross-milestone behavior remain unimplemented and were not reviewed as working behavior.

## Recommended Next Stage

Record and resolve `BRF-M1-CR12`, return M1 to `review-requested` only after occurrence-aware repeated-target frontier regressions and the full M1 validation set pass, then rerun code-review M1.

Do not start M2 before M1 is approved and closed.

This direct review is isolated and performs no automatic downstream handoff.
