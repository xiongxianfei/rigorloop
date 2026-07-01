# Review-Fix Autoprogression Test Spec

## Status

active

## Related spec and plan

- Spec: [Review-Fix Autoprogression](review-fix-autoprogression.md)
- Plan: [Bounded Review-Fix Autoprogression in Chat Plan](../docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md)
- Proposal: [Bounded Review-Fix Autoprogression in Chat](../docs/proposals/2026-06-30-bounded-review-fix-autoprogression-in-chat.md)
- Architecture: [Canonical System Architecture](../docs/architecture/system/architecture.md)
- ADR: [ADR-20260630 Bounded Review-Fix Autoprogression](../docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md)
- Spec-review: [spec-review-r2](../docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/spec-review-r2.md), approved
- Architecture-review: [architecture-review-r2](../docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/architecture-review-r2.md), approved
- Plan-review: [plan-review-r2](../docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/plan-review-r2.md), approved

## Testing strategy

- Use unit and fixture-backed integration tests in `scripts/test-change-metadata-validator.py`, `scripts/change_metadata_semantics.py`, and `schemas/change.schema.json` for durable `workflow.autoprogression.review_fix` state, closed vocabulary, activation state, terminal transitions, and malformed-state failures.
- Use lifecycle and route tests in `scripts/test-artifact-lifecycle-validator.py`, `scripts/artifact_lifecycle_validation.py`, and `scripts/lifecycle_state_sync.py` for command target bounds, current-gate checks, proposal-start activation, direct-review isolation, architecture assessment routing, target-not-applicable, stale review stops, target-boundary stops, and state synchronization.
- Use review artifact tests in `scripts/test-review-artifact-validator.py`, `scripts/review_artifact_validation.py`, and `templates/review-resolution.md` for auto-safe classification, review-resolution disposition, budget evidence, changed-file limits, same-review rereview linkage, open-finding blocks, and closed closeout consistency.
- Use skill and generated guidance tests in `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/build-skills.py --check`, `scripts/test-build-skills.py`, and `scripts/test-adapter-distribution.py` for command wording, direct-review isolation, stage-skill claim boundaries, generated adapter support surfaces, and no hidden implementation/verify/PR/release handoff.
- Use end-to-end fixture proof in artifact-lifecycle and review-artifact fixtures for an explicitly armed proposal-side loop through `test-spec-review`, including safe-fix rereview and stop paths.
- Use manual contract review only for judgment-heavy wording that cannot be safely reduced to structural assertions, such as whether a proposed safe fix changes product direction or architecture meaning. Manual checks must cite the finding ID, owning artifact, and owner-decision rationale.
- Do not use network, publication, release, destructive, credential-accessing, or external-state commands in this proof. Those surfaces are out of scope for this profile.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`-`R3` | `T1`, `T5`, `T12` | integration, contract | Command shape, `status`, and `off` handling. |
| `R4`-`R9`, `R42` | `T1`, `T2`, `T12` | unit, integration | Durable state shape, closed profile/status/target values, required fields, and fail-closed unknown values. |
| `R9a`-`R9f`, `R39`, `R40` | `T2`, `T3`, `T4`, `T12` | integration | Activation gates, proposal-start gate, direct-review isolation with existing state, malformed state pause, terminal transitions, and explicit resume. |
| `R10`, `R16`, `R17`, `R44` | `T4`, `T11`, `T12` | integration, contract | Existing skills remain authoritative and direct review invocations do not activate or resume review-fix state. |
| `R11`, `R12`, `R21`, `R22` | `T5`, `T8`, `T11` | integration, contract | Proposal-side path, target boundary, no implementation/code-review/verify/PR/release/external effects. |
| `R13`-`R15`, `R20`, `R37`, `R43` | `T3`, `T7`, `T8`, `T12` | integration | Preflight inputs, ambiguity stops, current review requirement, stale review blocks, and invalid continuation combinations. |
| `R18`, `R19`, `R35`, `R36` | `T6`, `T7`, `T12` | integration | Review evidence before fixes, same-review rereview, disposition fields, changed files, validation evidence, and rereview linkage. |
| `R22a`-`R22g` | `T5` | integration | Architecture assessment values and conditional routing. |
| `R23`-`R29` | `T6`, `T9` | integration, manual | Driver-owned classification, auto-safe criteria, exact reviewer wording, non-auto-safe blockers, and generated ownership stops. |
| `R30`-`R34` | `T7` | integration | Cycle, finding, file, invocation, and target-stage budget stops. |
| `R38` | `T9`, `T11` | integration, contract | Generated or marker-owned output routes through canonical owner or stops. |
| `R41` | `T10`, `T11` | contract | Chat result summary fields and stop reason reporting. |
| `R45` | `T11`, `T13`, `T16` | integration, smoke | No partial user-visible mode before full proposal-side contract through `test-spec-review` passes. |
| Inputs and outputs | `T1`-`T13` | integration | Commands, artifacts, review records, review-resolution, metadata, and chat-visible summaries. |
| State and invariants | `T1`-`T9`, `T12` | integration | Review-fix state remains profile-local evidence, gates remain authoritative, target is upper bound, no dry-run/apply-mode state. |
| Error and boundary behavior | `T1`, `T3`, `T5`, `T7`, `T8`, `T9` | integration | Unknown target, missing evidence, blocked recording, stale review, non-auto-safe, budget, cancellation, and contradictory state. |
| Compatibility and migration | `T1`, `T4`, `T11`, `T13` | integration, contract | Historical records without `review_fix` are unarmed; existing profiles remain unchanged. |
| Observability | `T6`, `T7`, `T10`, `T12` | integration, contract | Review records, review-log, review-resolution, metadata, and chat summary. |
| Security and privacy | `T8`, `T9`, `T11` | integration, contract | No secrets, network, publication, release, destructive, credential, or external-state commands. |
| Accessibility and UX | `T10`, `T11` | contract | Text-only command output names invalid values, allowed targets, stop reasons, and next action. |
| Performance expectations | `T7`, `T12` | integration | Preflight and loop budgets bound expensive repeated work. |
| Acceptance criteria `AC1`-`AC6` | `T1`, `T2`, `T12` | unit, integration | Closed command/state/profile/status/class/disposition validation. |
| Acceptance criteria `AC7`-`AC13` | `T6`, `T7`, `T8`, `T9` | integration | Recorded evidence, auto-applied disposition, rereview, stops, budgets, and stale review. |
| Acceptance criteria `AC14`-`AC23` | `T2`, `T3`, `T4`, `T5`, `T8` | integration | Target bounds, activation, direct-review isolation, malformed state, terminal transitions, and architecture assessment. |
| Acceptance criteria `AC24`-`AC26` | `T10`, `T11`, `T13`, `T16` | integration, smoke | Existing profile preservation, no partial enablement, and chat result reporting. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T4`, `T11` | Direct review stays isolated and does not create review-fix state. |
| `E2` | `T1`, `T2`, `T3` | Target-stage command records durable authorization and starts only from clean gates. |
| `E3` | `T6`, `T7` | Safe finding is recorded, fixed, dispositioned, and rereviewed. |
| `E4` | `T6`, `T9`, manual review | Owner-decision architecture finding stops without editing. |
| `E5` | `T5`, `T8` | Target boundary prevents invoking `test-spec` after target `plan-review`. |
| `E6` | `T7` | Six material findings exceed per-cycle budget and stop. |
| `E7` | `T8` | Stale reviewed artifact blocks otherwise safe fixing. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| `EC1` | `T4` | Direct `spec-review` after arming remains isolated unless workflow command activated state. |
| `EC2` | `T6`, `T9` | Mixed auto-safe and `needs-decision` findings stop without partial hidden fixes. |
| `EC3` | `T6` | Exact reviewer wording without target section is `not-auto-safe`. |
| `EC4` | `T9`, `T11` | Generated adapter output must route through generator/canonical source or stop. |
| `EC5` | `T5` | Target `architecture` with `architecture-not-required` stops with `target-not-applicable`. |
| `EC6` | `T1` | `$workflow auto: verify` is rejected as outside target-stage enum. |
| `EC7` | `T3`, `T8` | Paused profile resume requires fresh preflight and matching review evidence. |
| `EC8` | `T3`, `T12` | Clean review plus open review-log finding stops for state repair. |

## Test cases

### T1. Review-fix command targets and metadata vocabulary fail closed

- Covers: R1-R8, R42, AC1-AC6, EC6
- Level: unit
- Fixture/setup: Add valid and invalid change metadata fixtures under `tests/fixtures/change-metadata/review-fix-autoprogression/`.
- Steps:
  - Add a valid `workflow.autoprogression.review_fix` fixture using `profile: bounded-review-fix`, a valid `status`, and each valid `target_stage`.
  - Add negative fixtures for `$workflow auto: verify`, arbitrary target names, unknown `review_fix.profile`, unknown status, missing required fields, and raw non-enum target values.
  - Add regression tests with `unknown_value` or `not_in_vocabulary` in the test name for profile, status, target stage, stop reason, auto-fix class, review status, and disposition constants.
- Expected result: Valid review-fix state passes; unknown or missing closed-vocabulary values fail before route consistency checks.
- Failure proves: The profile can persist unsupported authority or silently accept stale command values.
- Automation location: `python scripts/test-change-metadata-validator.py -k review_fix`; `python scripts/validate-change-metadata.py <fixture>/change.yaml`.

### T2. Activation and terminal transitions require durable authorization and clean gates

- Covers: R4-R9f, R39, AC5, AC15, AC16, AC18, AC19, E2
- Level: integration
- Fixture/setup: Change-metadata and lifecycle fixtures for `off`, `armed`, `active`, `paused`, `completed`, `cancelled`, proposal-start activation, target completion, and malformed persisted state.
- Steps:
  - Assert proposal-start activation requires accepted proposal, approved recorded proposal-review, no open proposal-review findings, closed resolution when material findings existed, and unambiguous change/artifact placement.
  - Assert armed state becomes active only when durable authorization exists and the current stage gate passes from tracked artifacts.
  - Assert `$workflow auto: off`, cancellation, target reached, completed, and non-auto-safe blocker transitions deterministically update `workflow.autoprogression.review_fix`.
  - Assert unknown, missing, malformed, stale, or contradictory persisted state pauses before mutation or downstream continuation.
- Expected result: Activation and terminal transitions are deterministic, durable, and gate-backed.
- Failure proves: Chat-only intent or contradictory metadata can authorize mutation or continuation.
- Automation location: `python scripts/test-change-metadata-validator.py -k review_fix`; `python scripts/test-artifact-lifecycle-validator.py -k review_fix`.

### T3. Preflight resolves current route and blocks ambiguity before work

- Covers: R9a-R9e, R13-R15, R20, R37, R40, R43, AC13, AC15, AC18, EC7, EC8
- Level: integration
- Fixture/setup: Lifecycle fixtures for missing change ID, ambiguous artifact path, missing review evidence, stale artifact after review, open review-log finding, paused resume with mismatched cursor, and valid resume with matching cursor.
- Steps:
  - Assert preflight reads change ID, target artifact, review state, requested target, review-fix state, artifact freshness, and next transition before authoring, review, fixing, or continuation.
  - Assert missing or ambiguous placement, contradictory state, stale review evidence, open findings, and mismatched resume cursor stop before mutation.
  - Assert a valid paused resume requires explicit user resume plus matching artifact and review evidence.
- Expected result: The driver never infers readiness from artifact existence or stale review evidence.
- Failure proves: The workflow can mutate or advance from ambiguous or stale state.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`.

### T4. Direct review invocations stay isolated even when review-fix state exists

- Covers: R9d, R10, R16, R17, R44, AC4, AC17, AC24, E1, EC1
- Level: integration
- Fixture/setup: Lifecycle fixtures with existing armed/paused review-fix state and direct invocations of `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `test-spec-review`, and `code-review`.
- Steps:
  - Assert direct review invocation records its review result but does not create, activate, resume, or advance `workflow.autoprogression.review_fix`.
  - Assert review skills remain independent gates and do not edit reviewed artifacts during review.
  - Assert existing `authoring-through-plan-review` and `implementation-through-verify` profile semantics are unchanged.
- Expected result: Isolation controls downstream handoff while recording still happens.
- Failure proves: Direct review requests can accidentally become workflow-managed continuation.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`; `python scripts/test-skill-validator.py -k review_fix`.

### T5. Proposal-side route and architecture assessment obey target bounds

- Covers: R11, R12, R21-R22g, AC14, AC20-AC23, E5, EC5
- Level: integration
- Fixture/setup: Lifecycle fixtures for target stages from `proposal-review` through `test-spec-review`, plus architecture assessments `architecture-required`, `architecture-not-required`, and `architecture-ambiguous`.
- Steps:
  - Assert the driver route is limited to `proposal -> proposal-review -> spec -> spec-review -> architecture when required -> architecture-review when required -> plan -> plan-review -> test-spec -> test-spec-review`.
  - Assert no route invokes `implement`, `code-review`, `verify`, `pr`, release, publication, network, destructive, or external-state operations.
  - Assert approved recorded `spec-review` requires exactly one architecture assessment before routing.
  - Assert `architecture-required` routes through architecture stages, `architecture-not-required` skips them, skipped conditional targets stop with `target-not-applicable`, and `architecture-ambiguous` stops for owner decision.
  - Assert the driver stops when the target stage is reached and never continues past the armed target.
- Expected result: Target stage is an upper bound, not permission to skip prerequisites or exceed the user's intent.
- Failure proves: Conditional architecture routing or target stops can silently overrun the armed boundary.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`.

### T6. Auto-safe classification is driver-owned and fail-closed

- Covers: R18, R23-R29, R35, R36, AC7, AC8, AC10, E3, E4, EC2, EC3
- Level: integration
- Fixture/setup: Review artifact fixtures with material findings for `mechanical`, `format-preserving`, `exact-reviewer-wording`, `status-normalization-with-evidence`, `recording-repair`, `cross-reference-repair`, `validation-command-shape-repair`, and `not-auto-safe`.
- Steps:
  - Assert the driver computes authoritative classification even when a reviewer hint exists.
  - Assert auto-safe findings require stable finding ID, evidence, deterministic outcome, deterministic patch target, small diff, current reviewed artifact, and same-review rereview path.
  - Assert product, scope, requirement, architecture, milestone sequencing, validation ownership, public behavior, release policy, external state, generated ownership, `needs-decision`, ambiguous alternatives, missing evidence, missing target, and reviewer-declared downstream block are `not-auto-safe`.
  - Assert exact reviewer wording requires target artifact, target section or line range, exact quoted replacement, no owner-decision rationale, and no semantic scope change.
- Expected result: Only deterministic bounded fixes classify as auto-safe; all judgment-bearing findings stop.
- Failure proves: The driver can auto-apply semantic or owner-owned decisions.
- Automation location: `python scripts/test-review-artifact-validator.py -k review_fix`; `python scripts/test-artifact-lifecycle-validator.py -k review_fix`.

### T7. Auto-fix budgets, dispositions, and same-review reruns are mandatory

- Covers: R18-R20, R30-R36, R41, R43, AC7-AC12, E3, E6
- Level: integration
- Fixture/setup: Review-resolution fixtures for safe fixes, missing disposition fields, missing rereview linkage, six findings, more than two cycles, more than three changed files per cycle, and more than ten changed files per invocation.
- Steps:
  - Assert review evidence is recorded before planned disposition or fix application.
  - Assert auto-applied dispositions include finding ID, driver classification, rationale, files changed, validation evidence, and rereview linkage.
  - Assert same-review rereview is required after every auto-fix cycle before continuation.
  - Assert budget exhaustion stops without partially applying hidden fixes and reports exhausted budget, remaining findings, changed files, review state, and owner action.
- Expected result: Auto-fixes are bounded, auditable, and never self-approved.
- Failure proves: Review gates can disappear behind auto-fix bookkeeping.
- Automation location: `python scripts/test-review-artifact-validator.py -k review_fix`; `python scripts/validate-review-artifacts.py --mode structure <fixture-root>`.

### T8. Stale review and invalid continuation combinations block downstream progress

- Covers: R20, R21, R22, R37, R39, R40, R43, AC13, AC14, EC7, EC8
- Level: integration
- Fixture/setup: Lifecycle fixtures for stale reviewed artifact, open findings with approved continuation, continuation past target stage, closed closeout with unresolved findings, and manual fix followed by resume.
- Steps:
  - Assert reviewed artifact changes after review evidence block fix application and continuation.
  - Assert open findings cannot coexist with approved continuation.
  - Assert continuation past target stage fails validation.
  - Assert closed review-resolution with unresolved findings fails validation.
  - Assert manual fixes do not resume paused profile without explicit resume and matching cursor.
- Expected result: Continuation requires current clean review evidence and target-bound state.
- Failure proves: Stale or inconsistent evidence can authorize downstream work.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`; `python scripts/validate-review-artifacts.py --mode closeout <fixture-root>`.

### T9. Generated ownership, unsafe effects, and security boundaries stop the loop

- Covers: R12, R27, R28, R38, Security/privacy, EC2, EC4
- Level: integration, manual
- Fixture/setup: Fixtures for generated adapter output, marker-owned content, release/publication/network commands, destructive commands, credential-accessing commands, and external-state updates.
- Steps:
  - Assert generated or marker-owned artifacts can be changed only through their owning generator or canonical source.
  - Assert review-fix routes stop before release, publication, network, destructive, credential, or external-state operations.
  - Assert scope, requirement, architecture, validation ownership, release policy, and owner-decision changes remain non-auto-safe.
- Expected result: The profile cannot mutate generated/public/external surfaces directly or cross security-sensitive boundaries.
- Failure proves: Review-fix automation can escape its proposal-side artifact scope.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`; `python scripts/test-review-artifact-validator.py -k review_fix`; manual contract review of generated-output guidance.

### T10. Chat result and error messages are complete and bounded

- Covers: R41, Accessibility and UX, AC26
- Level: contract
- Fixture/setup: Workflow skill output examples or validator fixtures for approved, changes-requested, blocked, inconclusive, target reached, budget exhausted, stale review, invalid target, and target-not-applicable outcomes.
- Steps:
  - Assert each run summary reports mode, target stage, current stage, review status, auto-applied fixes, human decisions required, artifacts changed, review rerun status, next stage run, and stop reason.
  - Assert invalid target messages name the invalid value and allowed target-stage values.
  - Assert stopped findings name finding IDs and required owner action.
- Expected result: Users can audit what changed, what stopped, and what happens next without hidden continuation.
- Failure proves: The profile becomes opaque or hard to recover from.
- Automation location: `python scripts/test-skill-validator.py -k review_fix`; manual contract review of `skills/workflow/SKILL.md`.

### T11. Workflow and stage skills preserve claim boundaries and generated guidance

- Covers: R10-R17, R38, R41, R44, R45, AC24-AC26, E1
- Level: smoke, contract
- Fixture/setup: `skills/workflow/SKILL.md`, proposal-side stage skills, review skills, `docs/workflows.md`, `scripts/build-skills.py`, adapter validation surfaces.
- Steps:
  - Assert user-facing skill text names `bounded-review-fix` only as explicitly armed workflow-managed behavior.
  - Assert direct review skills still say direct/review-only invocations remain isolated.
  - Assert no stage handoff implies implementation, code-review, verify, PR, release, publication, network, or external operations.
  - Assert generated skill and adapter checks pass after canonical skill changes.
- Expected result: Canonical and generated guidance describe one consistent bounded profile.
- Failure proves: Users or public adapters can receive broader or stale workflow behavior.
- Automation location: `python scripts/test-skill-validator.py -k review_fix`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`.

### T12. Integrated lifecycle fixtures prove review-fix state synchronization

- Covers: R1-R45, AC1-AC26, State and invariants, Observability
- Level: e2e
- Fixture/setup: End-to-end fixture set under `tests/fixtures/artifact-lifecycle/review-fix-autoprogression/` plus matching review-artifact and change-metadata fixtures.
- Steps:
  - Build a valid armed loop from clean proposal gate through `test-spec-review`.
  - Include branches for auto-safe rereview, non-auto-safe stop, target boundary stop, architecture-not-required skip, architecture-required route, architecture-ambiguous stop, and target-not-applicable.
  - Assert plan state, review-log, review-resolution, change metadata, and artifact lifecycle projections remain synchronized.
- Expected result: The full proposal-side profile is proven across metadata, review artifacts, lifecycle routing, and plan state.
- Failure proves: Individual validators pass while the integrated workflow state drifts.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

### T13. Existing profiles and historical records remain compatible

- Covers: R44, R45, Compatibility and migration, AC24, AC25
- Level: integration
- Fixture/setup: Existing authoring-through-plan-review fixtures, implementation-through-verify fixtures, and historical change records without `workflow.autoprogression.review_fix`.
- Steps:
  - Assert historical records without review-fix state are treated as unarmed.
  - Assert `authoring-through-plan-review` keeps its stop-before-test-spec boundary.
  - Assert `implementation-through-verify` keeps separate phase-gated authorization and stop-before-PR behavior.
  - Assert no partial user-visible review-fix mode is enabled until the full contract through `test-spec-review` passes.
- Expected result: The new profile is additive and does not widen existing automation.
- Failure proves: Review-fix support regresses established workflow profiles or migration behavior.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k autoprogression`; `python scripts/test-change-metadata-validator.py -k autoprogression`.

### T14. M1 state schema and metadata validation proof

- Covers: Plan M1, R1-R10, R39, R42, AC1-AC6, AC15-AC19
- Level: unit, integration
- Fixture/setup: Change metadata schema and semantic fixtures.
- Steps:
  - Implement tests named in M1 for valid state, unknown profile/status/target/stop reason, required fields, direct-review-only metadata, and terminal transitions.
  - Run the M1 validation commands from the plan.
- Expected result: M1 can close only when review-fix state is durable and invalid metadata fails closed.
- Failure proves: Implementation starts from unstable authorization state.
- Automation location: `python scripts/test-change-metadata-validator.py -k review_fix`; `python scripts/test-change-metadata-validator.py`; `python scripts/validate-change-metadata.py docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`.

### T15. M2 and M3 routing plus review-resolution proof

- Covers: Plan M2, Plan M3, R11-R38, R41-R43, AC7-AC24, AC26
- Level: integration
- Fixture/setup: Lifecycle and review-artifact fixtures for route evaluator, preflight, architecture assessment, target bounds, classification, budgets, stale evidence, generated ownership, and rereview linkage.
- Steps:
  - Implement route evaluator tests from M2.
  - Implement review-resolution and classification tests from M3.
  - Run the M2 and M3 validation commands from the plan.
- Expected result: Routing and mutation are safe only when review evidence, target bounds, budgets, and rereview proof align.
- Failure proves: The driver can continue, fix, or record results outside the approved contract.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py -k review_fix`; `python scripts/test-review-artifact-validator.py -k review_fix`.

### T16. M4 and M5 guidance, generated output, and final integration proof

- Covers: Plan M4, Plan M5, R39-R45, AC1-AC26
- Level: smoke, e2e
- Fixture/setup: Changed canonical skills, `docs/workflows.md`, generated-skill checks, adapter distribution checks, behavior-preservation evidence, and final validation bundle.
- Steps:
  - Run skill-validator checks for review-fix command wording, direct-review isolation, no hidden downstream handoff, and existing profile preservation.
  - Run generated skill and adapter checks after canonical skill changes.
  - Add behavior-preservation evidence proving direct reviews, `authoring-through-plan-review`, `implementation-through-verify`, review recording, rereview, and stop boundaries remain intact.
  - Run the final M5 validation commands after all implementation milestones close.
- Expected result: The full proposal-side feature is proven end to end and safe to expose.
- Failure proves: The implementation is locally correct but not distributable or behavior-preserving.
- Automation location: `python scripts/test-skill-validator.py -k review_fix`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`; `bash scripts/ci.sh --mode explicit ...`.

## Fixtures and data

- Add change metadata fixtures under `tests/fixtures/change-metadata/review-fix-autoprogression/` for valid state, unknown values, missing required fields, terminal transitions, and historical unarmed records.
- Add artifact lifecycle fixtures under `tests/fixtures/artifact-lifecycle/review-fix-autoprogression/` for route evaluation, target boundaries, architecture assessment, direct-review isolation, stale review, paused resume, and integrated proposal-side loops.
- Add review artifact fixtures under `tests/fixtures/review-artifacts/review-fix-autoprogression/` for auto-safe classification, non-auto-safe blockers, review-resolution disposition, budget exhaustion, missing rereview linkage, and closed/open closeout combinations.
- Use the active change record `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml` only as lifecycle evidence for this initiative, not as a reusable generic fixture.

## Mocking/stubbing policy

- Prefer real repository parsers, schemas, validators, and fixture directories over mocks.
- Stub only command invocation interpretation where no command runner exists yet; the stub must produce deterministic route-evaluator inputs and must not execute external commands.
- Do not mock review artifact parsing, change metadata parsing, lifecycle state parsing, or generated-output checks.
- Do not use network, publication, release, destructive, credential, or external-state stubs as passing proof; those surfaces are out of scope and should assert stop behavior.

## Migration or compatibility tests

- Historical change records without `workflow.autoprogression.review_fix` are unarmed and remain valid.
- Existing `authoring-through-plan-review` fixtures preserve stop-before-test-spec behavior.
- Existing `implementation-through-verify` fixtures preserve separate authorization, phase gating, reviewer-owned correction authority, fresh verify evidence, and stop-before-PR behavior.
- Rollback tests prove disabling the profile removes automatic continuation and safe-fix application without invalidating historical review records or review-resolution entries.

## Observability verification

- Review-fix metadata records `target_stage`, `profile`, `status`, `armed_by`, `armed_at`, `current_stage`, `current_review`, `stop_reason`, and `last_updated_evidence` when known.
- Review records and `review-log.md` prove each formal review invocation.
- `review-resolution.md` records every auto-applied material finding with driver classification, rationale, changed files, validation evidence, and rereview linkage.
- Chat-visible summaries report mode, target stage, current stage, review status, auto-applied fixes, human decisions required, artifacts changed, review rerun status, next stage run, and stop reason.

## Security/privacy verification

- Tests assert this profile cannot run network, publication, release, destructive, credential-accessing, or external-state commands.
- Tests assert durable authorization does not rely on untracked private chat state.
- Review and metadata fixtures must not include secrets, tokens, credentials, private keys, or host-specific private paths.
- Generated or marker-owned artifacts cannot be hand-edited by the driver.

## Performance checks

- Preflight checks run before expensive authoring, review, or validation work in lifecycle fixtures.
- Loop-budget tests assert no more than two auto-fix/rereview cycles per review gate.
- Finding-budget tests assert no more than five material findings per cycle.
- Changed-file budget tests assert no more than three files per cycle and ten files per chat invocation.
- Selected validation commands use the milestone-specific commands named in the plan before broader CI.

## Manual QA checklist

- Confirm final workflow skill output for `$workflow auto: <target-stage>`, `$workflow auto: status`, and `$workflow auto: off` is concise and names allowed targets.
- Confirm stage skills do not imply direct review invocations activate or resume review-fix state.
- Confirm examples in docs and skills do not show `verify`, `pr`, release, network, or external operations under this profile.
- Confirm behavior-preservation evidence names direct reviews, `authoring-through-plan-review`, `implementation-through-verify`, review recording, rereview, and stop boundaries.

## What not to test and why

- Do not test implementation, code-review, verify, PR, release, publication, network, or external-state automation under this profile; the approved spec excludes them.
- Do not test dry-run or apply-mode state; the approved spec explicitly has no dry-run or apply-mode state in this contract.
- Do not test review skills as editors of reviewed artifacts; the approved contract keeps review skills as independent gates.
- Do not test generated public adapter package bodies as hand-edited sources; generated public adapter package output is not tracked source.
- Do not prove semantic owner decisions by automation alone; those require manual owner judgment and must stop the loop.

## Uncovered gaps

None. Every `MUST`, example, edge case, acceptance criterion, and implementation milestone has a planned proof surface.

## Next artifacts

- `test-spec-review`
- implementation milestone M1 after clean `test-spec-review`

## Follow-on artifacts

None yet.

## Readiness

Ready for `test-spec-review`. This test spec does not authorize implementation until `test-spec-review` approves it and the active plan state is synchronized.
