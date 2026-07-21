# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: M1 R2
Reviewer: Codex code-review skill
Target: M1 correction commit `7283ab40`
Reviewed artifact: M1 correction commit `7283ab40`
Reviewed milestone: M1. Unified State Model and Complete Policy Registry
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-21
Recording status: recorded
Material findings: BRF-M1-CR5, BRF-M1-CR6, BRF-M1-CR7
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Open blockers: none
- Next stage: review-resolution M1
- Review status: changes-requested
- Recording status: recorded
- Reviewed milestone: M1. Unified State Model and Complete Policy Registry
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M1-CR5, BRF-M1-CR6, BRF-M1-CR7
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `22b57232..7283ab40`.
- Review surface: the M1 policy and automation-state validators, their tests, and synchronized lifecycle evidence.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R009`-`BRF-R017f`, `BRF-R024`-`BRF-R043`, `BRF-R068`-`BRF-R079`, and `BRF-R101`-`BRF-R102`.
- Test spec: T2-T5, T7-T8, and T14-T15 in `specs/single-bounded-review-fix-workflow-automation.test.md`.
- Plan milestone: M1 in `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`.

## Risk Map

Before consulting recorded validation summaries or prior finding dispositions, the rereview prioritized terminal-history acceptance, stale or cross-risk authority, policy/validator drift, repeated-stage target identity, and receipt authority/evidence semantics. Direct contrast fixtures challenged a valid later target with a current earlier-stage capability, an unbound implementation parent maximum target, and placeholder receipt evidence. M2 execution, public routing, external actions, generated adapters, and credentials remain out of scope.

## Prior-Finding Reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-M1-CR1` | resolved | Capability occurrence validation now derives from the immutable stage registry and rejects wrong internal occurrences and missing milestone IDs. |
| `BRF-M1-CR2` | resolved | Required basis identities and invalidation behavior now reject null, empty, unknown, and cross-risk forms. |
| `BRF-M1-CR3` | resolved with follow-on finding | The requested structural bindings were added; R2 identifies the distinct destination/operation semantic defect as `BRF-M1-CR5`. |
| `BRF-M1-CR4` | resolved with follow-on finding | The requested matrix was expanded; R2 identifies incorrect contrast semantics and remaining gaps as `BRF-M1-CR6`. |

## Findings

### BRF-M1-CR5: Receipt validation conflates the run target with the current stage operation and accepts placeholder evidence

Finding ID: BRF-M1-CR5
- Severity: major
- Status: reopened
- Location: `scripts/validate_workflow_automation.py:892`, `scripts/validate_workflow_automation.py:923`, `scripts/test-validate-workflow-automation.py:511`
- Evidence: A run may target a later stage while its next transition executes an earlier stage under that stage's effective capability. The accepted proposal illustrates `to_stage: implement`, a `code-review@M2` target, and an implementation capability in one prepared receipt. The validator instead requires `receipt.target` to equal `capability.stage`, so a valid run targeting `spec` with a proposal-review capability fails with `stage occurrence does not match receipt target`. Separately, `expected_postcondition: {review_occurrence: null}` and `outputs: [null]` both validate successfully because only container non-emptiness/type is checked. Such placeholders cannot support the evidence-first reconciliation required by `BRF-R073`-`BRF-R077`.
- Required outcome: Keep the structured run destination distinct from the concrete transition operation. Bind the operation through the effective capability (or an explicit closed transition-stage field if the approved contract is amended), validate that the operation is a permitted predecessor toward the target, and require concrete postcondition/output evidence where present.
- Safe resolution path: Remove direct target/capability equality; validate capability stage and occurrence against policy, canonical from-position, and target reachability. Add recursive or typed concrete-evidence validation for postconditions and non-empty outputs, while preserving an empty prepared-receipt output list. Add earlier-stage/later-target and null/empty evidence regressions.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M1-CR6: The negative proof matrix still confirms invalid records as valid

Finding ID: BRF-M1-CR6
- Severity: major
- Status: reopened
- Location: `scripts/test-validate-workflow-automation.py:283`, `scripts/test-validate-workflow-automation.py:525`
- Evidence: The all-capability positive matrix constructs implementation parent `maximum_target` as `implement + milestone` without milestone ID, plan identity, binding time, or completion predicate, and expects it to pass. The receipt stage-match test expects a valid later destination to fail. No test rejects null postcondition values or null output entries. All 25 validator tests therefore pass while the direct contrast fixtures demonstrate violations of the approved structured-target and recoverable-evidence contracts.
- Required outcome: Positive fixtures must be contract-valid and negative fixtures must challenge the semantic distinctions between maximum target, current operation, and durable reconciliation evidence.
- Safe resolution path: Correct the positive parent fixtures, replace receipt-equality proof with target-reachability/operation-binding proof, and add named unbound repeated-target and placeholder-evidence regressions.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M1-CR7: Parent maximum targets bypass the structured repeated-target contract

Finding ID: BRF-M1-CR7
- Severity: major
- Status: open
- Location: `scripts/validate_workflow_automation.py:553`, `scripts/test-validate-workflow-automation.py:397`
- Evidence: `_validate_parent` explicitly treats `maximum_target` as a reduced envelope containing only stage and occurrence kind. An implementation parent with `maximum_target: {stage: implement, occurrence: {kind: milestone}}` passes without milestone ID, plan identity, binding time, or completion predicate. `BRF-R024` requires a maximum structured target, and `BRF-R017a`-`BRF-R017d` require repeated-stage occurrence and completion binding before authorization state is persisted. This permits authorization to remain ambiguous across milestones.
- Required outcome: A persisted parent maximum target must satisfy the approved structured-target contract, including repeated-stage milestone and plan identity, binding time, and completion predicate, or the specification must define a distinct non-target consent-envelope type before implementation proceeds.
- Safe resolution path: Reuse the structured target validator for parent maximum targets and enforce capability/target subset rules. Add direct authoring, implementation, and verification parent positives plus missing milestone, plan identity, binding time, and completion predicate negatives.
- auto_fix_class: none
- needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | Receipt operation/target semantics and parent structured targets do not match the approved contract. |
| Test coverage | block | Passing tests encode both defects and omit concrete evidence contrast cases. |
| Edge cases | block | Later destinations, repeated-stage parent targets, and null evidence are mishandled. |
| Error handling | concern | Known vocabularies fail closed, but semantic placeholder values pass. |
| Architecture boundaries | pass | M1 remains non-public and no writer or orchestration engine was added. |
| Compatibility | pass | Legacy state remains read-only and no retired writer was enabled. |
| Security/privacy | pass | No external action, secret, credential, or network surface changed. |
| Derived artifact currency | pass | No generated adapter output changed. |
| Unrelated changes | pass | The correction remains scoped to M1 and its lifecycle evidence. |

## Validation

- `python scripts/test-workflow-automation-policy.py` passed: 9 tests.
- `python scripts/test-validate-workflow-automation.py` passed: 25 tests.
- `python scripts/test-change-metadata-validator.py -k workflow_automation` passed: 4 selected tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` passed before R2 evidence recording.
- Direct in-memory contrast: valid later target/current earlier capability was rejected.
- Direct in-memory contrast: unbound implementation parent maximum target passed.
- Direct in-memory contrast: null postcondition and null output evidence passed.

## Recommended Next Stage

Enter `review-resolution` for `BRF-M1-CR5`, `BRF-M1-CR6`, and `BRF-M1-CR7`. Keep M1 `resolution-needed` and do not start M2 until a fresh code review approves M1.
