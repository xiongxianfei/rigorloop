# Test-Spec Readiness And Skill Workflow Alignment Test Spec

## Status

active

## Related spec and plan

- Spec: `specs/test-spec-readiness-and-skill-workflow-alignment.md`
- Proposal: `docs/proposals/2026-05-25-spec-review-testability-routing-output-consolidation.md`
- Plan: `docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md`
- Change metadata: `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
- Review evidence: `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/spec-review-r3.md`, `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/plan-review-r2.md`
- Architecture/ADRs: not applicable. The approved plan states this is a localized skill-output contract, asset, validator, and generated-output change inside existing boundaries.

## Testing strategy

- Unit strategy: add focused helper/parser tests in `scripts/test-skill-validator.py` for controlled `spec-review` result text and fixture structures.
- Integration strategy: run skill validation and build checks against canonical `skills/spec-review/SKILL.md`, `skills/spec-review/assets/review-result-skeleton.md`, and generated local skill output.
- End-to-end strategy: use the M3 generated-output proof to build temporary adapter archives and validate that packaged skill bodies and assets contain the updated contract.
- Smoke strategy: run repository-owned skill, change metadata, review artifact, lifecycle, and diff hygiene commands named by the active plan.
- Manual strategy: review touched skill text and behavior-preservation evidence for scope preservation, adjacent-skill drift, and material-finding field ownership.
- Contract strategy: prove the closed `Immediate next stage` and `Eventual test-spec readiness` enums, status-to-routing bindings, and approval-to-readiness rule through deterministic fixtures where structurally inspectable.
- Migration strategy: no runtime migration is required; compatibility proof is that workflow order, review statuses, finding severities, recording statuses, material-finding asset shape, and autoprogression boundaries remain unchanged.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b` | `T1`, `T4` | contract | Covers separation of routing from readiness, the closed immediate-stage enum, and forward repository-stage distinction. |
| `R1c`, `R1d` | `T7` | manual | Confirms the focused spec remains the change contract and workflow invariant handling does not drift beyond the approved first slice. |
| `R2`, `R2a`, `R2b`, `R2c` | `T1`, `T4` | contract | Covers result fields, review status enum, immediate-stage enum, and pseudo-routing rejection. |
| `R2d`, `R2e`, `R2i`, `R2j` | `T3`, `T4` | contract | Covers approved status routing to `architecture` or `plan` only, and invalid cross-field pairings. |
| `R2f`, `R2g`, `R2h` | `T3`, `T4` | contract | Covers non-approved routing to `spec revision`, `review-resolution`, or `none` and missing-input stop conditions. |
| `R3`, `R3a`, `R3b`, `R3c` | `T2`, `T4` | contract | Covers readiness enum, approved readiness pairing, and named condition requirement. |
| `R3d`, `R3e`, `R3f`, `R3g`, `R3h`, `R3i` | `T2`, `T3` | contract | Covers `not-ready` behavior for non-approved reviews and downstream stop behavior. |
| `R3j`, `R3k` | `T1`, `T2`, `T3` | contract | Covers rejection of `not-assessed` readiness and `test-spec` as an immediate next stage. |
| `R4`, `R4a`, `R4b`, `R4c` | `T6`, `T7` | manual | Preserves workflow order, plan-review handoff to `test-spec`, and isolated review behavior. |
| `R5`, `R5a`, `R5b` | `T6` | manual | Covers `plan-review` handoff wording only if that skill is touched or drift is found. |
| `R6`, `R6a`, `R6b` | `T6` | manual | Covers `test-spec` prerequisites and rejection of unready upstream review outcomes. |
| `R7`, `R7a` | `T7` | manual | Covers first-pass scope boundary and prevents broad review-family normalization. |
| `R8`, `R8a`, `R8b`, `R8c` | `T1`, `T2`, `T3`, `T4` | unit, contract | Covers deterministic fixture and canonical enforcement for routing/readiness fields where inspectable. |
| `R8d` | `T5` | unit, manual | Covers material-finding field-label single ownership without prose overfit. |
| `R8e` | `T7`, `T9` | manual | Confirms recorded review-artifact field enforcement remains deferred unless parser support already exists. |
| `AC-SRTR-ROUTE-001` through `AC-SRTR-ROUTE-005` | `T1`, `T3`, `T4` | contract | Covers field naming, enum values, forward-stage distinction, stage-order derivation, and missing-input `none`. |
| `AC-SRTR-UX-001` through `AC-SRTR-UX-004` | `T7` | manual | Confirms the approved spec's text-only UX clarity requirements remain satisfied by implementation outputs. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T2`, `T3`, `T4` | Approved no-architecture case uses `Immediate next stage: plan` and readiness `ready`. |
| `E2` | `T2`, `T3`, `T4` | Approved architecture case uses `Immediate next stage: architecture` and readiness `conditionally-ready` with a named dependency. |
| `E3` | `T2`, `T3` | Missing eventual readiness becomes `changes-requested` or `blocked`, with `not-ready` and downstream stop behavior. |
| `E4` | `T6` | Approved plan-review keeps `test-spec` as the immediate next stage. |
| `E5` | `T6` | Test-spec authoring still requires approved spec and plan context. |
| `E6` | `T3` | Missing reviewer input uses `inconclusive`, `Immediate next stage: none`, readiness `not-ready`, and a stop condition. |
| `E7` | `T3`, `T4` | Approved spec-review cannot route backward or to `test-spec`. |

## Edge case coverage

- `Immediate next stage: test-spec` is rejected in controlled fixture coverage and canonical enforcement once enabled: `T1`, `T4`.
- `Review status: approved` with `Eventual test-spec readiness: not-ready` is rejected: `T2`, `T4`.
- `Review status: approved` with `Immediate next stage: spec revision`, `review-resolution`, or `none` is rejected: `T3`, `T4`.
- `changes-requested`, `blocked`, or `inconclusive` with `Immediate next stage: architecture` or `plan` is rejected where fields are structurally inspectable: `T3`.
- Missing reviewer input uses explicit `none`, not an empty field or `not-assessed`: `T2`, `T3`.
- `conditionally-ready` without a named condition is rejected or manually flagged as incomplete: `T2`.
- M1 must not enable canonical enforcement before canonical assets are changed in M2: `T1`, `T7`.
- `assets/material-finding.md` remains the structural owner of the complete material-finding field shape: `T5`.
- Generated adapter proof may be blocked by unavailable local tooling; the blocker and smallest next action must be recorded instead of claiming proof: `T8`.

## Test cases

### T1. Controlled fixtures enforce the immediate-stage enum

- Covers: `R1`, `R2`, `R2b`, `R2c`, `R3k`, `R8`, `R8a`, `AC-SRTR-ROUTE-001`, `AC-SRTR-ROUTE-002`
- Level: unit
- Fixture/setup: Controlled result fixtures in `scripts/test-skill-validator.py` or file-backed fixtures under `tests/fixtures/skills/` if the existing layout supports them.
- Steps:
  - Add controlled fixtures for each allowed `Immediate next stage` value: `spec revision`, `review-resolution`, `architecture`, `plan`, and `none`.
  - Add a controlled negative fixture with `Immediate next stage: test-spec`.
  - Add controlled negative fixtures for pseudo-routing labels such as `blocker handling`, `missing-context resolution`, and `ready for test-spec` if practical.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Allowed enum values pass; `test-spec` and pseudo-routing labels fail in controlled fixture validation.
- Failure proves: The historical direct-to-`test-spec` routing failure can recur or the enum is not structurally enforced.
- Automation location: `scripts/test-skill-validator.py`; optional `tests/fixtures/skills/`.

### T2. Controlled fixtures enforce eventual readiness values and approval pairing

- Covers: `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `R3g`, `R3h`, `R3i`, `R3j`, `R8b`, `E1`, `E2`, `E3`, `E6`
- Level: unit
- Fixture/setup: Controlled `spec-review` result fixtures.
- Steps:
  - Add positive fixtures for `Review status: approved` with readiness `ready` and `conditionally-ready`.
  - Add a negative fixture for `Review status: approved` with `Eventual test-spec readiness: not-ready`.
  - Add a negative fixture for readiness `not-assessed`.
  - Add a negative or manual-contract fixture for `conditionally-ready` without a named condition when the validator can inspect condition text.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Approved results require `ready` or `conditionally-ready`; `not-ready` and `not-assessed` fail for approved results; conditional readiness names the condition where inspectable.
- Failure proves: The readiness field can become a rubber stamp or an unassessed escape hatch.
- Automation location: `scripts/test-skill-validator.py`; optional `tests/fixtures/skills/`.

### T3. Controlled fixtures enforce status-to-routing bindings and missing-input behavior

- Covers: `R2d`, `R2e`, `R2f`, `R2g`, `R2h`, `R2i`, `R2j`, `R3d`, `R3e`, `R3i`, `R3j`, `E3`, `E6`, `E7`, `AC-SRTR-ROUTE-003`, `AC-SRTR-ROUTE-004`, `AC-SRTR-ROUTE-005`
- Level: unit
- Fixture/setup: Controlled `spec-review` result fixtures.
- Steps:
  - Add positive fixtures for approved results routing to `architecture` and `plan`.
  - Add negative fixtures for approved results routing to `spec revision`, `review-resolution`, `none`, or `test-spec`.
  - Add positive fixtures for `changes-requested` routing to `spec revision` or `review-resolution`.
  - Add positive fixtures for `blocked` routing to `review-resolution` or `none`.
  - Add a positive missing-input fixture with `Review status: inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition.
  - Add negative fixtures for non-approved statuses routing to `architecture` or `plan`.
  - Run `python scripts/test-skill-validator.py`.
- Expected result: Status-to-routing contradictions fail, and missing input uses the explicit `none` value with `not-ready` and a stop condition.
- Failure proves: The new routing field can contradict review status or reintroduce empty/missing immediate-stage behavior.
- Automation location: `scripts/test-skill-validator.py`; optional `tests/fixtures/skills/`.

### T4. Canonical spec-review skill and result skeleton enforce the contract

- Covers: `R1`, `R1a`, `R1b`, `R2`, `R2a-R2j`, `R3`, `R3a-R3k`, `R8a`, `R8b`, `R8c`, `E1`, `E2`, `E7`
- Level: integration
- Fixture/setup: `skills/spec-review/SKILL.md`, `skills/spec-review/assets/review-result-skeleton.md`, and M1 helper checks.
- Steps:
  - Update canonical `spec-review` skill text and result skeleton in M2.
  - Enable canonical enforcement only after the canonical assets are updated.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-skills.py skills/spec-review/SKILL.md`.
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/build-skills.py --check`.
- Expected result: Canonical skill and skeleton expose `Immediate next stage`, `Eventual test-spec readiness`, and `Stop condition` distinctly; direct `test-spec` routing and approved/not-ready contradictions fail validation.
- Failure proves: Controlled fixtures pass but the shipped canonical skill still teaches the wrong output contract.
- Automation location: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/build-skills.py`.

### T5. Material-finding field shape has one structural owner

- Covers: `R8d`
- Level: unit, manual
- Fixture/setup: `skills/spec-review/SKILL.md`, `skills/spec-review/assets/material-finding.md`, and validator helper support if feasible.
- Steps:
  - Confirm `assets/material-finding.md` still contains the complete required material-finding field-label set.
  - Confirm `SKILL.md` preserves the material-finding sufficiency rule.
  - Confirm `SKILL.md` does not re-enumerate the complete material-finding field-label set in a second prose block.
  - Add a targeted structural single-ownership validator check if feasible without exact-prose overfitting.
  - Run `python scripts/test-skill-validator.py` and `python scripts/validate-skills.py`.
- Expected result: The asset owns field structure; the skill may reference the asset and sufficiency rule without duplicating the full field shape.
- Failure proves: The drift surface remains because field shape is still duplicated or the asset no longer owns the complete structure.
- Automation location: `scripts/test-skill-validator.py` if feasible; otherwise manual contract evidence in code review and behavior-preservation proof.

### T6. Adjacent plan-review and test-spec prerequisites remain intact

- Covers: `R4b`, `R5`, `R5a`, `R5b`, `R6`, `R6a`, `R6b`, `E4`, `E5`
- Level: manual
- Fixture/setup: `skills/plan-review/SKILL.md`, `skills/test-spec/SKILL.md`, active plan, and approved spec-review evidence.
- Steps:
  - Inspect `skills/plan-review/SKILL.md` only if implementation touches it or validation shows direct drift.
  - Confirm approved `plan-review` still routes immediately to `test-spec`.
  - Inspect `skills/test-spec/SKILL.md` only if implementation touches it or validation shows direct drift.
  - Confirm `test-spec` authoring still requires an approved spec, spec-review findings, concrete execution plan, and approved architecture or ADR inputs when relevant.
  - Confirm `test-spec` authoring rejects upstream `not-ready` spec-review outcomes and returns work to the appropriate upstream gate.
- Expected result: The change does not obscure `plan-review -> test-spec` or weaken `test-spec` prerequisites.
- Failure proves: The implementation fixed `spec-review` while moving the routing/readiness confusion into adjacent stages.
- Automation location: Manual review during M2 and code-review.

### T7. Scope, workflow order, isolation, and UX clarity are preserved

- Covers: `R1c`, `R1d`, `R4`, `R4a`, `R4c`, `R7`, `R7a`, `R8e`, `AC-SRTR-UX-001` through `AC-SRTR-UX-004`
- Level: manual
- Fixture/setup: Active plan, approved spec, touched skill files, `docs/workflows.md` if touched, and behavior-preservation evidence.
- Steps:
  - Compare the final diff to the active plan's first-slice boundary.
  - Confirm no broad review-family rewrite, workflow stage-order change, autoprogression expansion, or new lifecycle stage was introduced.
  - Confirm direct or review-only `spec-review` remains isolated by default.
  - Confirm recorded review-artifact result-field validation is deferred unless the existing parser can inspect those fields without broad parser redesign.
  - Confirm Markdown output clarity remains the UX surface and the implementation does not introduce irrelevant graphical UI requirements.
- Expected result: The implementation clarifies the output contract without changing workflow topology or expanding scope.
- Failure proves: The slice drifted from output-contract consolidation into broader workflow redesign.
- Automation location: Manual review during M2/M3, code-review, and verify.

### T8. Generated local skills and public adapter proof include updated spec-review content

- Covers: `R4`, `R4a`, `R4b`, `R4c`, `R7`, `R7a`, `R8e`
- Level: integration, e2e
- Fixture/setup: Canonical `skills/`, temporary adapter output directory, and current adapter version from repository release guidance or manifest.
- Steps:
  - Run `python scripts/build-skills.py --check`.
  - Build temporary adapter archives with `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`.
  - Validate temporary adapter output with `python scripts/validate-adapters.py --root <tmpdir> --version <version>`.
  - Inspect generated Codex, Claude, and opencode adapter content for the updated `spec-review` skill body and result skeleton.
  - If local tooling is unavailable, record the blocker and smallest next action instead of claiming generated-output proof.
- Expected result: Generated outputs are current from canonical `skills/` and include the updated routing/readiness contract.
- Failure proves: Canonical source and shipped adapter surfaces can diverge.
- Automation location: `scripts/build-skills.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, bounded archive-content checks.

### T9. Lifecycle, review, metadata, and diff hygiene validation remain green

- Covers: supporting proof for all requirements and touched lifecycle artifacts
- Level: smoke
- Fixture/setup: Active change-local artifact pack and touched lifecycle artifacts.
- Steps:
  - Run `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`.
  - Run `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation` when findings are closed.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`.
  - Run explicit-path lifecycle validation for touched spec, test spec, plan, plan index, changed skill assets, behavior-preservation evidence when created, and change-local review artifacts.
  - Run `git diff --check -- <touched files>`.
- Expected result: Lifecycle-managed artifacts, review evidence, change metadata, and diff hygiene are valid after each milestone.
- Failure proves: The implementation may be behaviorally correct but leaves stale lifecycle or review state that blocks PR readiness.
- Automation location: `scripts/validate-review-artifacts.py`, `scripts/validate-change-metadata.py`, `scripts/validate-artifact-lifecycle.py`, `git diff --check --`.

## Fixtures and data

- Controlled result fixtures for valid and invalid `spec-review` output field combinations.
- Canonical authored skill and asset files:
  - `skills/spec-review/SKILL.md`
  - `skills/spec-review/assets/review-result-skeleton.md`
  - `skills/spec-review/assets/material-finding.md`
- Adjacent skills only when directly touched or drift is proven:
  - `skills/plan-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
- Lifecycle and review artifacts:
  - `specs/test-spec-readiness-and-skill-workflow-alignment.md`
  - `specs/test-spec-readiness-and-skill-workflow-alignment.test.md`
  - `docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/`
- Temporary generated adapter output under `/tmp` for M3.

## Mocking/stubbing policy

- Prefer controlled text fixtures and real repository files over mocks.
- Do not mock canonical skill files; canonical enforcement must inspect actual `skills/` content after M2 updates it.
- Do not mock generated adapter archives in M3; use repository-owned build output or record a tooling blocker.

## Migration or compatibility tests

- Confirm no runtime migration, persistent state migration, or user data migration is introduced.
- Confirm review status values, finding severity values, recording status values, material-finding asset shape, workflow order, and autoprogression boundaries remain unchanged.
- Confirm generated-output validation uses temporary output and does not hand-edit tracked public adapter archives.

## Observability verification

- `spec-review` output exposes `Review status`, `Immediate next stage`, `Eventual test-spec readiness`, and `Stop condition`.
- Validator failures identify invalid routing/readiness combinations by field value rather than broad prose scoring.
- Behavior-preservation evidence records approval readiness, routing, readiness, material findings, recording, statuses, severities, and generated-output proof.
- Change metadata records validation commands and results for each lifecycle gate and milestone.

## Security/privacy verification

- Confirm the change introduces no new secret handling, credential path, network dependency, or destructive action.
- Confirm review-output examples and validation fixtures do not include secrets or sensitive runtime values.
- Confirm no higher-priority security or privacy policy is weakened while editing workflow-facing skills.

## Performance checks

- No runtime performance checks are required.
- Validator additions should remain bounded to deterministic field/fixture checks and avoid broad natural-language scoring or expensive repository-wide parsing beyond existing validation commands.

## Manual QA checklist

- [ ] `Immediate next stage` enum is exactly `spec revision`, `review-resolution`, `architecture`, `plan`, and `none`.
- [ ] `Immediate next stage: test-spec` fails controlled fixture validation and canonical enforcement after M2.
- [ ] `Eventual test-spec readiness` enum is exactly `ready`, `conditionally-ready`, and `not-ready`.
- [ ] `not-assessed` is not accepted as eventual readiness.
- [ ] `approved` pairs only with `ready` or `conditionally-ready`.
- [ ] `conditionally-ready` names its remaining condition.
- [ ] Missing reviewer input uses `inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition.
- [ ] `approved` routes only to `architecture` or `plan`.
- [ ] Non-approved statuses do not route to `architecture` or `plan`.
- [ ] `assets/material-finding.md` remains the field-shape owner and `SKILL.md` does not duplicate the complete field-label list.
- [ ] `plan-review` remains the immediate handoff to `test-spec` if its wording is in scope.
- [ ] `test-spec` prerequisites remain approved spec, spec-review findings, concrete plan, and relevant approved architecture/ADR inputs.
- [ ] No workflow-order, autoprogression, review-status, severity, recording-status, or broad review-family changes are introduced.
- [ ] Generated-output proof uses canonical source and temporary adapter output.

## What not to test and why

- Do not add runtime product tests; this change affects workflow-facing skills, assets, validators, and generated documentation.
- Do not test every review-family skill; the approved first slice is scoped to `spec-review` plus adjacent-skill drift only when directly proven.
- Do not require recorded review-artifact result-field enforcement unless existing parser support can inspect those fields without broad redesign.
- Do not use snapshot-only tests for the behavior contract; field-level assertions and controlled fixtures are required.
- Do not hand-edit or assert tracked public adapter package skill bodies; generated proof must come from repository-owned build/validation commands.

## Uncovered gaps

None. The approved spec and plan are precise enough for implementation proof. Recorded review-artifact result-field enforcement is intentionally deferred by `R8e` unless parser support already exists.

## Next artifacts

- implement M1
- code-review M1
- implement M2
- code-review M2
- implement M3
- code-review M3
- explain-change
- verify
- pr

## Follow-on artifacts

None yet.

## Readiness

This test spec is active and ready to govern implementation.

Immediate next stage: implement M1.

Implementation readiness: ready for M1 only. M2 and M3 remain gated by M1 closeout and their milestone-specific validation.
