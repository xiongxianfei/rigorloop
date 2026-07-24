# Code Review M6 R1

Review ID: code-review-m6-r1
Stage: code-review
Round: M6 R1
Reviewer: independent same-session context-reset reviewer
Target: M6 implementation commit `02c3bc79`
Reviewed artifact: M6 implementation commit `02c3bc79`
Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M6-CR1, BRF-M6-CR2, BRF-M6-CR3, BRF-M6-CR4
Immediate next stage: review-resolution M6

## Review context

- Invocation mode: direct isolated milestone review
- Independence level: `L1-same-session-context-reset`
- Review surface: commit range `cbb3b266..02c3bc79`
- Requirement-fidelity gate: applied to `BRF-R002` through `BRF-R005`, `BRF-R087` through `BRF-R102`, T19 through T23, and T25 through T30
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shared the prior implementation session and does not claim blind L2 independence; the review intentionally reset to the approved specification, M6 proof map, architecture boundaries, and actual commit before reading the recorded M6 validation summary

## Independent risk map

### Affected behavior

- Public current and legacy workflow command normalization and activation.
- Unified target selection, status, cancellation, and authority boundaries.
- Dual-read, single-write migration and legacy writer retirement.
- Cross-spec ownership validation and public result observability.
- Canonical skill guidance, generated adapters, and selected-CI routing.

### Highest-impact failure modes

- Public activation exposes wrappers that do not compose into the complete mechanism.
- Legacy `off` leaves an active unified run after an interrupted cancellation.
- A missing cross-spec ledger selector passes because the validator derives its required set from the ledger under test.
- Status or run results omit canonical position, transition, or decision evidence required for tracked resume.
- Public authorizations cannot materialize bounded correction authority.
- Public guidance claims behavior that direct runtime proof does not establish.

### Changed boundaries

- `scripts/workflow_automation.py`: public target, status, off, compatibility, and stage wrappers.
- `scripts/validate_workflow_automation.py`: exact cross-spec disposition validation.
- `scripts/workflow_automation_state.py`: public status projection.
- `scripts/validation_selection.py`: selected proof routing.
- `skills/workflow/SKILL.md`, `docs/workflows.md`, and README: public command contract.

### Expected evidence

- Interrupted and terminal legacy cancellation have one safe terminal result.
- The cross-spec validator compares the Markdown ledger with an independent closed affected-selector registry.
- Every public result contains current tracked position, authority, transition, review, decision, artifact, and stop evidence.
- Clean, correction, interruption, cancellation, migration, missing-authority, and final-success flows traverse the public composition.
- Repeated identical and reversed-order composed runs produce equivalent state and no external action.

### Direct-inspection areas

- `validate_repository_cross_spec_dispositions`.
- `_public_command_result`, `execute_public_control_command`, and `start_public_run`.
- Public stage wrappers and parent-authorization construction.
- New M6 engine and validator tests.
- Public workflow skill and guide claims.

### Intentionally out-of-scope areas

- Final holistic cross-milestone review.
- `explain-change`, final `verify`, and PR handoff.
- Previously closed M1 through M5 behavior except where M6 makes it publicly reachable.

### Risk classes

- Applicable: authorization integrity, interruption recovery, compatibility, normative ownership, observability, external-action containment, generated-output currency, and validation selection.
- Not applicable: personal-data processing, cryptographic protocol design, accessibility UI, and deployed-service availability.

### Falsifiable questions

- Does deleting one canonical ledger row fail repository validation?
- Can interruption during legacy `off` persist an active unified run?
- Does terminal legacy `off` return a non-mutating terminal result?
- Does a new public run report a concrete canonical-position source?
- Can the public parent/capability path enter proposal or implementation correction?
- Is T30's repeated and reversed-order public composition present?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M6-CR1`, `BRF-M6-CR2`, `BRF-M6-CR3`, `BRF-M6-CR4`
- Next stage: review-resolution M6
- Review status: changes-requested
- Material findings: `BRF-M6-CR1`, `BRF-M6-CR2`, `BRF-M6-CR3`, `BRF-M6-CR4`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m6-r1.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m6-r1`
- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6 resolution and rereview
- Required review-resolution: yes
- Finding IDs: `BRF-M6-CR1`, `BRF-M6-CR2`, `BRF-M6-CR3`, `BRF-M6-CR4`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `02c3bc79` against parent `cbb3b266`.
- Tracked governing branch state: approved specification, approved test specification, approved architecture, accepted ADR, active M6 plan, and closed pre-M6 review resolution.
- Direct proof: missing-ledger-row, interrupted legacy-off, terminal legacy-off, and public-result field probes in temporary repositories.
- Validation evidence challenged: focused engine, validator, state, and policy suites plus the recorded selected-CI, adapter, skill, lifecycle, and broad-smoke evidence.

## Diff summary

The implementation exposes current and legacy command adapters through the unified Python engine, adds public status/off and run-start entry points, projects public stage wrappers over the previously non-public coordinators, and adds a repository cross-spec validator.

It replaces public three-profile guidance with one target-driven mechanism, updates affected skills, and teaches explicit-path CI to select all four workflow-automation suites.

## Findings

### BRF-M6-CR1 — Repository cross-spec validation derives its closed set from the ledger under test

Finding ID: BRF-M6-CR1
Severity: major
Location: `scripts/validate_workflow_automation.py:256-277` and `scripts/test-validate-workflow-automation.py:426-486`
Evidence: `validate_repository_cross_spec_dispositions` parses the canonical ledger and then constructs `required` from those same parsed rows. Deleting the exact `R1e` disposition row from a temporary canonical spec returned no validation errors. The generic unit test can detect a missing row only because it receives an independently supplied `required_selectors`; the repository entry point supplies no independent registry. This violates `BRF-R098h`, `AC-BRF-SR5-1`, and `AC-BRF-SR6-2`.
Required outcome: Repository validation must compare the canonical Markdown projection against an independent, immutable closed registry of every affected source selector and must reject an absent selector before any consistency inference.
Safe resolution path: Add a typed closed affected-selector registry separate from the parsed ledger, validate selector uniqueness in each affected source, compare parsed rows exactly with that registry, and add a temporary-repository regression that deletes one canonical ledger row while leaving the four source specs unchanged.
needs-decision rationale: none; the approved specification already requires an independent closed set.
auto_fix_class: none

### BRF-M6-CR2 — Legacy `off` exposes an active migrated run and mishandles terminal legacy state

Finding ID: BRF-M6-CR2
Severity: major
Location: `scripts/workflow_automation.py:2939-2981` and `scripts/test-workflow-automation.py:788-843`
Evidence: Legacy-only `off` calls `start_public_run`, which persists an active migrated unified run, and only then calls `store.cancel` in a second write. A temporary-store probe that interrupted `cancel` left `run.status: active` with a migration receipt even though the user requested off. A terminal `implementation-through-verify` record produced `AutomationContractError: terminal legacy state is read-only and cannot migrate` instead of a non-mutating terminal result. The committed test asserts only the uninterrupted active-legacy happy path. This contradicts the direct-cancel mapping in `BRF-R098a`, idempotent terminal behavior in `BRF-R007c`, and T16/T19/T20.
Required outcome: Legacy cancellation must have one recoverable terminal outcome, never expose a newly active run between migration and cancellation, preserve the legacy record byte-for-byte, and return the correct non-mutating result for terminal legacy state.
Safe resolution path: Add a state-adapter operation that projects active legacy state directly into one cancelled unified record with its migration and cancellation evidence in a single compare-and-swap write. Handle terminal legacy records as read-only `already-completed` or the exact approved terminal projection, and add interruption, terminal, repeated-off, and byte-identity regressions.
needs-decision rationale: none; the approved cancellation and compatibility contracts already define the result.
auto_fix_class: none

### BRF-M6-CR3 — Public status and run results omit required tracked workflow evidence

Finding ID: BRF-M6-CR3
Severity: major
Location: `scripts/workflow_automation.py:2872-2914`, `scripts/workflow_automation.py:3108-3122`, and `scripts/workflow_automation_state.py:1607-1647`
Evidence: `start_public_run` persists no `canonical_position_source` or observed canonical identities. A direct public plan-review start returned `canonical_position_source: None`. `_public_command_result` reports only the currently prepared receipt as `transitions_attempted`, always reports empty fixes and artifacts, and has no stage-completion input from which those values could be derived. Legacy-only status similarly has no structured target, authority boundary, canonical position, or latest evidence projection. The new tests assert mechanism, target, and read-only bytes but do not assert the complete `BRF-R006`/`BRF-R099` field semantics required by T22.
Required outcome: Every public target, status, pause, cancellation, review, and completion result must project concrete tracked canonical-position, authority, capability, transition-history, review/gate, decision, artifact, stop, and next-action evidence, using explicit absence only where the contract permits it.
Safe resolution path: Resolve canonical position before public persistence, store only its observed identities and source, project all attempted receipts rather than only the in-flight receipt, derive changed artifacts and fixes from finalized stage evidence, define the legacy read-only projection, and add active/paused/prepared/completed/migrated/review-result field-by-field tests with before/after byte checks.
needs-decision rationale: none; `BRF-R006`, `BRF-R099`, and T22 already enumerate the output.
auto_fix_class: none

### BRF-M6-CR4 — Public cutover does not prove or expose the complete bounded correction composition

Finding ID: BRF-M6-CR4
Severity: major
Location: `scripts/workflow_automation.py:2652-2707`, `scripts/workflow_automation.py:3023-3082`, and `scripts/test-workflow-automation.py:570-843`
Evidence: The public stage functions are thin context wrappers around non-public coordinators, but none is invoked by the new M6 tests. `start_public_run` creates authoring parents that permit only `proposal-review` and `post-proposal-authoring`, and implementation parents that permit only `implementation`; neither public path can derive the proposal-correction or implementation-correction capabilities required for the bounded review-fix loops. No public authorization-extension or resume composition is added. The four M6 tests independently exercise two route evaluators, start, status/off, and one active legacy migration, but do not perform T28's proposal-review-through-verify scenarios or T30's repeated and reversed-order full-engine comparison.
Required outcome: The public mechanism must expose a complete receipt-backed path from target selection through risk-boundary authorization, bounded proposal and implementation correction when authorized, interruption recovery, cancellation, migration, final verification, and stop-before-PR; the composed path must have deterministic repeat/reverse-order proof.
Safe resolution path: Add one public orchestration/resume entry point that materializes only basis-valid effective capabilities and accepts separately bounded correction consent/budgets without widening risk classes. Drive the existing coordinators through it in fresh temporary repositories for clean, correction, interruption, cancellation, migration, missing-authority, and final-success flows; run each fixed-input scenario twice and in reversed declared order and compare canonical state, receipts, status, teardown, and external-action trap counts.
needs-decision rationale: none; T25, T28, T30, `BRF-R060` through `BRF-R067`, and the approved architecture already define this composition.
auto_fix_class: none

## Requirement-fidelity result

| Contract | Result | Evidence |
| --- | --- | --- |
| `BRF-R002` through `BRF-R005` / T25 | concern | Public guidance and unified writes are present, but the complete public composition is not exercised. |
| `BRF-R006`, `BRF-R099`, `BRF-R100` / T22 | block | Canonical position and complete tracked transition/artifact evidence are absent from public results. |
| `BRF-R060` through `BRF-R067` / T28 | block | Public parent construction cannot authorize either bounded correction kind and no public end-to-end correction flow exists. |
| `BRF-R091` through `BRF-R098d` / T16, T19, T20 | block | Legacy cancellation persists an active intermediate run and terminal legacy off errors. |
| `BRF-R098e` through `BRF-R098i` / T21 | block | The repository validator has no independent closed affected-selector set. |
| `BRF-R101`, `BRF-R102` | pass | New disposition vocabulary has an unknown-value test and vocabulary checks precede consistency checks. |
| T30 | block | No repeated/reversed-order composed public-engine proof is present. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M6-CR1` through `BRF-M6-CR4` identify direct requirement compression. |
| Test coverage | block | Focused suites pass, but omit the directly reproduced missing-row, interrupted/terminal off, complete-result, and composed-determinism cases. |
| Edge cases | block | Interruption, terminal legacy state, absent ledger selector, and missing canonical position are not handled safely. |
| Error handling | block | Legacy off can leave the opposite of the requested terminal state. |
| Architecture boundaries | concern | The sole state writer is retained, but the two-write compatibility cancellation violates the architecture's recoverable cancellation flow. |
| Compatibility | block | Active and terminal legacy cancellation semantics are incomplete. |
| Security/privacy | pass with residual concern | No secret or external-action path was found in the M6 diff; complete public external-action trapping still belongs to the missing T28/T30 proof. |
| Derived artifact currency | pass | Canonical skills and temporary adapter drift checks support textual currency; no generated package body is tracked. |
| Unrelated changes | pass | The diff remains scoped to public cutover, proof selection, guidance, and lifecycle evidence. |
| Validation evidence | block for adequacy | All focused suites pass, but direct adversarial probes reproduce four uncovered contract gaps. |

## Validation challenge

- `python scripts/test-workflow-automation.py`: 63 tests passed.
- `python scripts/test-validate-workflow-automation.py`: 67 tests passed.
- `python scripts/test-workflow-automation-state.py`: 60 tests passed.
- `python scripts/test-workflow-automation-policy.py`: 16 tests passed.
- The recorded selected-CI, adapter, skill, lifecycle, and exact broad-smoke results are credible for the commands run.
- Temporary-repository probes independently reproduced missing-row acceptance, interrupted legacy-off active state, terminal legacy-off failure, and missing canonical-position result evidence.
- Passing counts do not establish T28/T30 composition because those scenarios are absent from the M6 test diff.

## Direct-proof gaps

- No committed test deletes one row from the real canonical cross-spec ledger while holding an independent expected registry.
- No committed test interrupts legacy cancellation between migration and terminalization.
- No committed test covers terminal legacy `off`.
- No committed test asserts every `BRF-R099` result field across active, paused, completed, migrated, and review-result states.
- No committed test executes T28 or T30 through the public composition.

## Milestone handoff

- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes; `BRF-M6-CR1` through `BRF-M6-CR4`
- Remaining in-scope implementation milestones: M6 resolution and rereview
- Next stage: review-resolution M6
- Final closeout readiness: not ready; M6 findings, M6 rereview, final holistic review, explanation, verification, and PR handoff remain

This direct review is isolated. It records the findings but does not begin correction automatically.
