# Downstream Status Settlement Before Reliance Test Spec

## Status

active

## Related spec and plan

- Spec: [Downstream Status Settlement Before Reliance](downstream-status-settlement-before-reliance.md), approved.
- Plan: [Downstream Status Settlement Before Reliance Plan](../docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md), active.

## Testing strategy

This change is a workflow and skill-guidance contract. The first implementation slice is verified through:

- static skill-validator tests for canonical skill guidance;
- canonical skill validation;
- generated local Codex skill mirror drift checks;
- public adapter generation and validation;
- change metadata, review artifact, and artifact lifecycle validation;
- manual review of milestone evidence during `code-review`, `explain-change`, and `verify`.

No runtime lifecycle-validator stale-status detection is required in this slice. Semantic stale-status validation remains later-slice scope.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| `R1` | `T1`, `T2` |
| `R2` | `T2`, `T7` |
| `R3` | `T2`, `T7` |
| `R4` | `T1`, `T5` |
| `R5` | `T1` |
| `R6` | `T1`, `T5` |
| `R7` | `T1`, `T5` |
| `R8` | `T1`, `T7` |
| `R9` | `T3` |
| `R10` | `T3`, `T4` |
| `R11` | `T3` |
| `R12` | `T3` |
| `R13` | `T3` |
| `R14` | `T3` |
| `R15` | `T4` |
| `R16` | `T4` |
| `R17` | `T4` |
| `R17a` | `T4`, `T6` |
| `R18` | `T6` |
| `R19` | `T6` |
| `R20` | `T6` |
| `R21` | `T6` |
| `R22` | `T6` |
| `R23` | `T6` |
| `R23a` | `T6` |
| `R23b` | `T6` |
| `R23c` | `T6` |
| `R23d` | `T6` |
| `R24` | `T6` |
| `R24a` | `T6` |
| `R25` | `T7` |
| `R26` | `T7` |
| `R27` | `T7` |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` | `T3`, `T6` |
| `E2` | `T3`, `T6` |
| `E3` | `T3`, `T6` |
| `E4` | `T4`, `T6` |
| `E5` | `T6` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` | `T4` |
| `EC2` | `T4` |
| `EC3` | `T4` |
| `EC4` | `T4` |
| `EC5` | `T4`, manual `code-review` |
| `EC6` | `T5` |
| `EC7` | `T6` |
| `E11` | `T6` |
| `E12` | `T6` |

## Test cases

### T1. First-slice downstream skills contain settlement guardrail

- Covers: `R1`, `R4`-`R8`
- Level: unit
- Fixture/setup: canonical `skills/spec/SKILL.md`, `skills/architecture/SKILL.md`, and `skills/plan/SKILL.md`
- Steps:
  - Add or update static checks in `scripts/test-skill-validator.py`.
  - Assert each first-slice skill contains concise upstream status settlement guidance.
  - Assert the guidance limits settlement to workflow-managed downstream execution.
  - Assert the guidance limits edits to lifecycle/status/readiness/follow-on/closeout metadata and excludes substantive content rewrites.
- Expected result: `python scripts/test-skill-validator.py` passes.
- Failure proves: first-slice skills do not expose the settlement contract needed for downstream agents.
- Automation location: `scripts/test-skill-validator.py`

### T2. First-slice scope excludes review skills and later downstream skills

- Covers: `R1`-`R3`, `R25`-`R27`
- Level: unit
- Fixture/setup: canonical skills for formal reviews and later downstream skills
- Steps:
  - Assert `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` do not gain standardized `Status sync`, `Status artifact`, or `Status sync blocker` fields.
  - Assert `test-spec`, `implement`, `explain-change`, `verify`, and `pr` are not required to perform operational upstream status settlement in this slice.
  - Assert any later-slice mentions are framed as future scope only.
- Expected result: `python scripts/test-skill-validator.py` passes.
- Failure proves: the first slice leaked into review-side status sync or later-slice downstream behavior.
- Automation location: `scripts/test-skill-validator.py`

### T3. Settlement mappings and clear-review evidence are present

- Covers: `R9`-`R14`
- Level: unit
- Fixture/setup: canonical first-slice skills
- Steps:
  - Assert first-slice guidance includes clear review evidence conditions: durable review evidence, approving/clean outcome, no later contradiction, no open findings, closed material findings when required, and explicit mapping.
  - Assert mapping text covers proposal to `accepted` for `spec`.
  - Assert mapping text covers spec to `approved` for `architecture` and `plan`.
  - Assert mapping text covers architecture package to `approved` for `plan`.
- Expected result: `python scripts/test-skill-validator.py` passes.
- Failure proves: downstream skills may settle based on incomplete evidence or missing mappings.
- Automation location: `scripts/test-skill-validator.py`

### T4. Unknown and blocked settlement cases are represented

- Covers: `R10`, `R15`-`R17a`, `EC1`-`EC5`
- Level: unit
- Fixture/setup: canonical first-slice skills
- Steps:
  - Assert first-slice guidance says unresolved material findings block settlement.
  - Assert contradictory or later conflicting review evidence blocks settlement.
  - Assert missing status surface, unknown artifact type, unknown lifecycle field, or unmapped next status blocks settlement.
  - Assert ADR settlement is allowed only for known `accepted` or `active` target vocabulary.
  - Assert unknown-target blocked settlement uses `New status: not-applicable`.
- Expected result: `python scripts/test-skill-validator.py` passes.
- Failure proves: downstream skills may guess status settlement or invent target states.
- Automation location: `scripts/test-skill-validator.py`

### T5. Isolation and edit-boundary behavior are covered

- Covers: `R4`, `R6`-`R8`, `EC6`
- Level: unit
- Fixture/setup: canonical first-slice skills
- Steps:
  - Assert guidance says review-only, no-edit, or manual inspection requests stay isolated and do not enter downstream settlement behavior.
  - Assert guidance says workflow-managed downstream execution does not ask whether edits are allowed.
  - Assert settlement must not rewrite substantive content.
- Expected result: `python scripts/test-skill-validator.py` passes.
- Failure proves: the first slice can blur isolated review behavior or over-edit upstream artifacts.
- Automation location: `scripts/test-skill-validator.py`

### T6. Settlement output contract is testable

- Covers: `R18`-`R24a`, `E1`-`E5`, `E11`, `E12`, `EC7`
- Level: unit
- Fixture/setup: canonical first-slice skills
- Steps:
  - Assert settlement output is required for updated, blocked, or stale-status-detected cases.
  - Assert the output shape includes upstream artifact, review evidence, previous status, new status, settlement result, and settlement blocker.
  - Assert result values include `updated`, `blocked`, and `not-needed`.
  - Assert blocked known-target settlement reports the intended target status.
  - Assert blocked unknown-target settlement reports `New status: not-applicable`.
  - Assert `not-needed` may be omitted or reported when already settled or irrelevant.
- Expected result: `python scripts/test-skill-validator.py` passes.
- Failure proves: downstream skill output cannot reliably explain settlement decisions.
- Automation location: `scripts/test-skill-validator.py`

### T7. Lifecycle-validator stale-status detection remains deferred

- Covers: `R25`-`R27`
- Level: unit
- Fixture/setup: canonical skills and validator tests
- Steps:
  - Assert first-slice skill guidance does not require semantic lifecycle-validator stale-status detection.
  - Assert test/spec references keep later lifecycle-validator detection as future scope.
  - Assert no implementation milestone adds lifecycle-validator stale-status enforcement.
- Expected result: `python scripts/test-skill-validator.py` and plan/code review pass.
- Failure proves: the first slice exceeded the approved scope.
- Automation location: `scripts/test-skill-validator.py`; manual code-review of touched validator files

### T8. Generated skill and adapter output mirrors canonical guidance

- Covers: generated public-surface consistency for `R1`-`R24a`
- Level: integration
- Fixture/setup: canonical skill changes complete
- Steps:
  - Run generated skill and adapter drift checks before regeneration and record expected drift.
  - Regenerate generated local Codex skills and public adapter output.
  - Validate generated output and adapter structure.
- Expected result: generated outputs are in sync and adapter validation passes.
- Failure proves: public/runtime skill surfaces do not match the canonical contract.
- Automation location: `scripts/build-skills.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, `scripts/test-adapter-distribution.py`

### T9. Change-local metadata and lifecycle artifacts remain valid

- Covers: workflow evidence and closeout integrity
- Level: integration
- Fixture/setup: change-local pack and lifecycle artifacts
- Steps:
  - Validate review artifacts in closeout mode.
  - Validate change metadata.
  - Run explicit artifact lifecycle validation for the proposal, spec, test spec, plan, plan index, change metadata, review log, and review resolution.
  - Run scoped `git diff --check`.
- Expected result: metadata, review artifacts, lifecycle artifacts, and whitespace checks pass.
- Failure proves: implementation evidence is not durable or reviewable.
- Automation location: validation commands in the plan

## Fixtures and data

No new runtime fixtures are required in the first slice.

Static tests may use the existing canonical skill files as fixtures:

- `skills/spec/SKILL.md`
- `skills/architecture/SKILL.md`
- `skills/plan/SKILL.md`
- related formal review and later downstream skill files for negative checks

## Mocking/stubbing policy

No mocks or stubs are required. This is static contract validation over repository-owned Markdown surfaces and generated outputs.

## Migration or compatibility tests

No bulk migration is required. Compatibility is verified by:

- preserving formal review recording rules;
- excluding later downstream skills from first-slice operational settlement;
- validating generated public adapter output after canonical skill changes.

## Observability verification

Observability is verified through static guidance requiring `Upstream status settlement` output for updated, blocked, or stale-status-detected cases, plus change-local validation evidence during implementation.

## Security/privacy verification

No new secrets, authentication, authorization, or private-data handling are introduced.

Security/privacy verification is limited to checking that settlement guidance prevents substantive upstream content rewrites and keeps review-only/no-edit requests isolated.

## Performance checks

No performance benchmark is required.

Manual code-review should verify that guidance encourages targeted upstream artifact and review-evidence reads rather than broad repository searches.

## Manual QA checklist

- Confirm M1 changes only canonical first-slice skills, static checks, and change-local/plan evidence.
- Confirm M2 changes only generated output and change-local/plan evidence.
- Confirm formal review skills do not gain review-side artifact-status sync fields.
- Confirm later downstream skills are not made operational settlement owners in this slice.
- Confirm generated outputs are not hand-edited.

## What not to test

- Do not test runtime lifecycle-validator stale-status detection; it is later-slice scope.
- Do not test `test-spec`, `implement`, `explain-change`, `verify`, or `pr` operational settlement behavior; they are excluded from the first slice.
- Do not add end-to-end repository scenarios for every possible artifact lifecycle status; the first slice uses static skill guidance and generated-output proof.
- Do not require bulk historical artifact migration tests.

## Uncovered gaps

None. Any attempt to implement semantic lifecycle-validator stale-status detection should return to spec or a follow-up proposal first.

## Next artifacts

- implement M1
- code-review M1
- implement M2
- code-review M2
- explain-change
- verify
- pr

## Follow-on artifacts

None yet.

## Readiness

Active proof-planning surface for implementation.
