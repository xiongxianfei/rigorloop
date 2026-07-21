# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: M1 R1
Reviewer: Codex code-review skill
Target: M1 commit `22b57232`
Reviewed artifact: M1 commit `22b57232`
Reviewed milestone: M1. Unified State Model and Complete Policy Registry
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-21
Recording status: recorded
Material findings: BRF-M1-CR1, BRF-M1-CR2, BRF-M1-CR3, BRF-M1-CR4
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m1-r1.md, docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md, docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md, docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md, docs/plan.md, docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml
- Open blockers: none
- Next stage: review-resolution M1
- Review status: changes-requested
- Material findings: BRF-M1-CR1, BRF-M1-CR2, BRF-M1-CR3, BRF-M1-CR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m1-r1
- Reviewed milestone: M1. Unified State Model and Complete Policy Registry
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M1-CR1, BRF-M1-CR2, BRF-M1-CR3, BRF-M1-CR4
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `22b57232^..22b57232`.
- Review surface: `schemas/change.schema.json`, `scripts/workflow_automation_policy.py`, `scripts/validate_workflow_automation.py`, `scripts/validate-change-metadata.py`, their M1 tests, and lifecycle handoff evidence.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R024`-`BRF-R046`, `BRF-R069`-`BRF-R071`, `BRF-R079`-`BRF-R080`, and `BRF-R099`-`BRF-R102`.
- Test spec: `specs/single-bounded-review-fix-workflow-automation.test.md`, especially T2, T3, T4, T7, and T8.
- Plan milestone: `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` M1.
- Validation evidence inspected after blind-first review: all five recorded M1 commands passed, including 7 policy tests, 3 selected vocabulary tests, 4 selected metadata tests, and 52 metadata-validator tests.
- Review challenge commands: the policy suite, selected vocabulary suite, selected metadata suite, full metadata suite, and four direct in-memory malformed-state reproductions.

## Risk Map

Before consulting recorded validation summaries, the review prioritized permissive schema bypass, incomplete closed vocabularies, policy/validator drift, executable parent authorization, effective-capability scope widening, repeated-stage occurrence ambiguity, and accidental public activation. The expected proof was exhaustive policy projection, unknown-value rejection before consistency checks, stage-relative authority validation, structured target/receipt validation, and explicit evidence that M1 did not expose a writer or public route. M2-M6 behavior was out of scope except where M1 claimed the foundational record contract.

## Diff Summary

M1 adds the unified automation schema, a frozen eighteen-stage policy registry, a structural/semantic validator, metadata-validator integration, and focused unit tests. It intentionally leaves the state writer and public command routing disabled. The architectural direction is correct, but the executable validator does not yet enforce several stage-policy and durable-record invariants that M1 claims as complete.

## Findings

### BRF-M1-CR1: Effective-capability occurrence validation omits internal stages and milestone identity

Finding ID: BRF-M1-CR1
- Severity: major
- Status: open
- Location: `scripts/validate_workflow_automation.py:72`, `scripts/validate_workflow_automation.py:514`, `scripts/test-workflow-automation-policy.py:34`
- Evidence: `STAGE_OCCURRENCES` is constructed from public targets only. `_validate_capability` applies occurrence compatibility only when a capability stage appears in that partial map, so internal stages such as `proposal`, `architecture-assessment`, `review-resolution`, `ci-maintenance`, `final-holistic-code-review`, and `explain-change` can carry an occurrence that contradicts their immutable `StagePolicy` and still pass. The capability path also does not require `milestone_id` for milestone-bound `implement` or `code-review`; that requirement exists only for run targets. A direct review reproduction changed an internal-stage capability to a wrong occurrence and received `[]`. The tests assert public occurrence rules but do not challenge internal or milestone capability occurrences. This leaves `BRF-R033`, `BRF-R035`, `BRF-R079`, and T3/T8 unproven.
- Required outcome: Every effective capability must validate its stage occurrence against the canonical immutable stage policy, and milestone-bound capabilities must carry their exact milestone identity and other required occurrence basis.
- Safe resolution path: Derive one stage-to-policy lookup from `STAGE_POLICIES` and use it for every capability stage rather than maintaining a public-only occurrence map. Add direct regressions for each internal occurrence family, missing milestone identity, and changed repeated-stage occurrence.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M1-CR2: Stage basis and invalidation records accept null or empty authority evidence

Finding ID: BRF-M1-CR2
- Severity: major
- Status: open
- Location: `scripts/validate_workflow_automation.py:38`, `scripts/validate_workflow_automation.py:432`, `scripts/validate_workflow_automation.py:531`
- Evidence: Stage-relative basis validation checks only that required keys exist, not that their identity values are concrete and non-empty. Parent and capability invalidation records are accepted when they are empty objects, and `INVALIDATION_ACTIONS` is declared but never applied. Direct review reproductions set `proposal_identity` to null and both invalidation objects to `{}`; each malformed state received `[]`. This permits an effective capability without a concrete basis and durable authorization records without deterministic invalidation behavior, contrary to `BRF-R024`, `BRF-R033`, `BRF-R037`, and T7/T8.
- Required outcome: Every stage-required basis identity and every required invalidation rule must be concrete, type-valid, non-empty, and drawn from its closed vocabulary before cross-record consistency is evaluated.
- Safe resolution path: Add stage-relative basis-value validators and closed invalidation schemas instead of key-presence checks. Add direct null, empty, wrong-type, and unknown-action regressions for every capability kind and parent authorization class.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M1-CR3: Transition receipts are not validated as complete capability-bound records

Finding ID: BRF-M1-CR3
- Severity: major
- Status: open
- Location: `scripts/validate_workflow_automation.py:325`, `scripts/validate_workflow_automation.py:696`
- Evidence: Receipt vocabulary validation calls only `_validate_target_vocabulary`, and structural validation checks required keys, mapping-key identity, and whether the capability ID exists. It does not call the structured target validator, so an incompatible `proposal-review + milestone` receipt target passes; a direct review reproduction returned `[]`. The validator also does not require the referenced capability to remain active or match the receipt stage/occurrence, does not bind receipt `run_id` and `change_id` to the active records, and does not validate non-empty `input_identities`, `expected_postcondition`, `outputs`, or the complete canonical-sync shape. M2 owns transaction execution, but M1 explicitly owns the complete `BRF-R069` record contract and structural validation.
- Required outcome: A receipt must be rejected unless its structured target is valid and its run, change, policy, and effective-capability bindings are internally consistent with concrete input and postcondition evidence.
- Safe resolution path: Reuse the common structured-target validator for receipt targets; validate run/change/policy identities, active capability status, stage/occurrence agreement, evidence object/list shapes, and canonical-sync fields. Add regressions for incompatible targets, stale/wrong capability binding, mismatched IDs, and empty evidence.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M1-CR4: The required exhaustive negative proof matrix is incomplete

Finding ID: BRF-M1-CR4
- Severity: major
- Status: open
- Location: `scripts/test-workflow-automation-policy.py:50`, `scripts/test-validate-workflow-automation.py:91`
- Evidence: Policy tests directly reject only an unknown stage and retry policy; they do not directly reject unknown occurrence, authorization class, capability kind, mutation category, applicability, correction, or stop behavior, nor a missing/incomplete policy field. Validator vocabulary tests cover core statuses and a subset of receipt/review values, but omit direct unknown-value regressions for external actions, allowed capability entries, mutation categories, internal capability stages/occurrences, parent/capability/receipt policy versions, and invalidation actions. T2 requires one proof per closed enum, T3 requires incomplete and changed-occurrence mutations, T7/T8 require complete positive and negative records for each authorization class/capability kind, and `AGENTS.md` requires an unknown-value regression for every new closed-vocabulary constant. All current suites pass despite the three malformed-state reproductions above.
- Required outcome: The M1 proof suite must directly exercise every closed vocabulary, every policy-field mutation family, and complete/invalid records for all parent classes and capability kinds.
- Safe resolution path: Expand table-driven tests with explicitly named `unknown_value` or `not_in_vocabulary` cases; mutate each policy field and occurrence rule; and add stage-relative valid/missing/stale/expanded capability fixtures. Keep test selection compatible with the plan's `-k vocabulary` command.
- auto_fix_class: none
- needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | BRF-M1-CR1 through BRF-M1-CR3 leave required occurrence, authority-basis, invalidation, and receipt contracts permissive. |
| Test coverage | block | BRF-M1-CR4 shows the approved exhaustive proof matrix is incomplete. |
| Edge cases | block | Wrong internal occurrences, null basis identities, empty invalidation behavior, and incompatible receipt targets pass. |
| Error handling | concern | Covered unknown values produce useful paths, but unvalidated values receive no error. |
| Architecture boundaries | concern | Public routing and the writer remain disabled as required, but occurrence semantics are duplicated in a public-only map instead of projected from the canonical policy registry. |
| Compatibility | pass | Legacy reads remain available and no new public route or legacy writer was added in M1. |
| Security/privacy | pass | No credentials, external actions, network mutation, or sensitive data handling were introduced. |
| Derived artifact currency | pass | No generated public adapter output was changed. |
| Unrelated changes | pass | The implementation surface is scoped to M1; the additional commit artifacts are its governing lifecycle package and handoff evidence. |
| Validation evidence | concern | Existing suites pass, but the passing set does not exercise the reproduced malformed states or complete closed-vocabulary matrix. |

## No-Finding Rationale

Not applicable. This review has four material findings.

## Residual Risks

This isolated review did not apply implementation corrections or start M2. Runtime mutation, reconciliation, orchestration, stage integration, and public cutover remain intentionally deferred to M2-M6 and were not assessed as implemented behavior.

## Validation

- `python scripts/test-workflow-automation-policy.py` passed: 7 tests.
- `python scripts/test-validate-workflow-automation.py -k vocabulary` passed: 3 selected tests.
- `python scripts/test-change-metadata-validator.py -k workflow_automation` passed: 4 selected tests.
- `python scripts/test-change-metadata-validator.py` passed: 52 tests.
- Direct in-memory review reproductions returned no validation errors for: null required basis identity, wrong internal-stage occurrence, incompatible receipt target occurrence, and empty invalidation behavior.
- `python scripts/validate-review-artifacts.py --mode structure ...` passed with 19 reviews, 26 findings, 19 log entries, and 26 resolution entries.
- `python scripts/validate-change-metadata.py .../change.yaml` passed.
- `python scripts/validate-guide-system.py` passed.
- Explicit-path lifecycle validation passed for the synchronized plan and review evidence with the existing lifecycle-language warning.
- `git diff --check` passed.

## Recommended Next Stage

Enter `review-resolution` for `BRF-M1-CR1` through `BRF-M1-CR4`, apply targeted M1 validator and proof corrections, rerun all M1 validation commands, return M1 to `review-requested`, and rerun `code-review M1`. Do not start M2 before M1 is approved and closed.
