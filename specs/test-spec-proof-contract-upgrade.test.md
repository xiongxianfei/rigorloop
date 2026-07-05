# Test-Spec Proof-Contract Upgrade Test Spec

## Status

active

## Related spec and plan

- Spec: `specs/test-spec-proof-contract-upgrade.md`
- Plan: `docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md`
- Architecture/ADRs: not required; architecture assessment recorded in `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/spec-review-r1.md`

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Proposal | `docs/proposals/2026-07-04-test-spec-proof-contract-upgrade.md` | accepted | `proposal-review-r1` |
| Proposal review | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/proposal-review-r1.md` | approved | `proposal-review-r1` |
| Feature spec | `specs/test-spec-proof-contract-upgrade.md` | approved | `spec-review-r1` |
| Spec review | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/spec-review-r1.md` | approved | `spec-review-r1` |
| Plan | `docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md` | active; plan-review approved | `plan-review-r1` |
| Plan review | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/plan-review-r1.md` | approved | `plan-review-r1` |
| Architecture | not applicable | architecture-not-required | `spec-review-r1` |

## Testing strategy

Use structural skill validation, focused unit tests, artifact lifecycle checks, generated-output checks, and behavior-preservation evidence.

Unit and fixture coverage should prove asset shape, resource-map entries, closed command classifications, required command fields, test-case command references, milestone proof-map rows, and command-free not-applicable behavior. Integration and smoke coverage should prove generated skills and adapter packages include the revised `test-spec` skill and new assets from canonical source. Manual QA is limited to behavior-preservation review of role, status model, review route, Manual QA preservation, historical migration boundary, and no generated-output hand edits.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R2 | T1, T9, T14 | unit, integration | Conditional validation-command ledger and no-command rationale. |
| R3-R5 | T1, T6, T13 | unit | Command IDs and references from test cases and milestone map. |
| R6-R7 | T2, T10 | unit | Closed classification enum and unknown-value failure. |
| R8-R12 | T1, T3, T4, T11 | unit, integration | Required command fields, planned command ownership, zero-test behavior, and side-effect boundary. |
| R13-R14 | T5 | unit | Input artifact identity section fields. |
| R15-R20 | T6, T12 | unit, integration | Milestone proof-map requirements and staged-command timing. |
| R21-R26 | T7, T8 | unit | Test-case asset fields, skeleton sections, row assets, and resource map. |
| R27-R29 | T15 | manual, contract | Asset inventory amendment, no manual-proof asset, Manual QA unchanged. |
| R30-R32 | T16 | manual, contract | Status model, review route, and claim boundaries preserved. |
| R33-R34 | T9, T10, T11, T12, T13, T14 | unit, integration | Representative positive and negative fixtures. |
| R35 | T17 | smoke | Generated skill and adapter inclusion proof. |
| R36 | T18 | manual, migration | Historical test specs are not migrated. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T13 | Command-backed proof uses ledger and Command IDs. |
| E2 | T14 | Command-free proof records rationale. |
| E3 | T3, T12 | Planned command timing is explicit. |
| E4 | T6, T12 | Milestone proof map separates staged proof. |
| E5 | T15, T16 | Manual-proof contracts remain out of scope and Manual QA is unchanged. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T14 | Command-free test spec remains valid with rationale. |
| EC2 | T14 | One-shot non-milestone change records milestone map not applicable. |
| EC3 | T4 | CI-owned command records ownership and safe boundary. |
| EC4 | T4 | Release-owned command records evidence ownership and stage. |
| EC5 | T3, T12 | Planned later command is not required too early. |
| EC6 | T18 | Historical test specs are not migrated solely for missing sections. |
| EC7 | T15 | Manual-proof requests remain outside this change. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/validate-skills.py skills/test-spec/SKILL.md` | existing/configured | implement | M1 | M1 closeout | fail milestone validation | not applicable; structural validator | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | local only; no network |
| CMD2 | `python scripts/test-skill-validator.py -k test_spec` | existing/configured | implement | M2 | M2 closeout | fail milestone validation | zero selected tests fail | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | local only; no network |
| CMD3 | `python scripts/build-skills.py --check` | existing/configured | implement | M3 | M3 closeout | fail generated-output validation | not applicable; build check | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | local generated-output check only; no hand edits |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M3 | M3 closeout | fail generated-skill proof | zero selected tests fail | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | local only; no network |
| CMD5 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 closeout | fail adapter inclusion proof | zero selected tests fail | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | local package/fixture proof; no publication |
| CMD6 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-proof-contract-upgrade.md --path specs/test-spec-proof-contract-upgrade.test.md --path docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md --path docs/plan.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | existing/configured | test-spec / verify | lifecycle closeout | test-spec-review closeout | block downstream handoff on lifecycle inconsistency | not applicable; lifecycle validator | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | local only; no network |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1, T3, T4, T5, T6, T7, T8, T15, T16 | none | CMD1, CMD6 | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`; behavior-preservation draft when created | code-review M1 | Proves skill and asset structure plus preserved boundaries. |
| M2 | T2, T9, T10, T11, T12, T13, T14 | none | CMD1, CMD2, CMD6 | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | code-review M2 | Proves representative fixture and closed-vocabulary coverage. |
| M3 | T15, T16, T17, T18 | none | CMD3, CMD4, CMD5, CMD6 | `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md`; `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | code-review M3 | Proves generated output, no historical migration, and final behavior preservation. |

## Test cases

### T1. Validation-command ledger required when commands are named

- Covers: R1-R5, R8, E1
- Level: unit
- Command IDs: CMD1, CMD2
- Fixture/setup: edited `skills/test-spec/SKILL.md`, `assets/test-spec-skeleton.md`, and representative valid output fixture.
- Steps: Check that a test spec naming a validation command includes a `Validation commands` section, stable Command IDs, and test-case references to Command IDs.
- Expected result: The valid fixture passes and the skill/resource map describes the conditional ledger requirement.
- Failure proves: command-backed proof can still rely on raw command strings without ownership.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T2. Closed command classification enum fails unknown values

- Covers: R6, R7
- Level: unit
- Command IDs: CMD2
- Fixture/setup: negative fixture with unsupported command classification.
- Steps: Run representative validation against the fixture.
- Expected result: Validation fails with a diagnostic naming the unsupported classification.
- Failure proves: command classification is not fail-closed.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T3. Planned command records owner and first required milestone

- Covers: R8-R10, EC5, E3
- Level: unit
- Command IDs: CMD2
- Fixture/setup: positive and negative fixtures for `planned-for-implementation`.
- Steps: Validate a planned command with owner/milestone fields and a planned command missing owner or milestone.
- Expected result: Complete planned-command fixture passes; incomplete planned-command fixture fails.
- Failure proves: planned commands can appear executable or required too early.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T4. Command entries record zero-test and side-effect behavior

- Covers: R8, R11, R12, EC3, EC4
- Level: unit
- Command IDs: CMD1, CMD2
- Fixture/setup: command-row asset and representative fixtures with test-running, CI-owned, and release-owned commands.
- Steps: Inspect or validate that required fields include zero-test behavior and safe-mode/side-effect boundary.
- Expected result: Required fields are present in the asset and representative fixtures.
- Failure proves: command execution and evidence ownership remain ambiguous.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/test-spec/SKILL.md`; `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M1, M2

### T5. Input artifact identity section is present

- Covers: R13, R14
- Level: unit
- Command IDs: CMD1
- Fixture/setup: edited skeleton and skill text.
- Steps: Confirm `Input artifact identities` appears in the skeleton and skill guidance with input, path, status/review state, and identity fields.
- Expected result: The section and required fields are present.
- Failure proves: implementation and review can rely on stale upstream artifacts without recorded identities.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/test-spec/SKILL.md`
- Required by milestone: M1

### T6. Milestone proof map is required for milestone plans

- Covers: R15-R20, E4
- Level: unit
- Command IDs: CMD1, CMD2
- Fixture/setup: skeleton, milestone-proof-row asset, and representative milestone-based fixture.
- Steps: Confirm milestone-based fixture maps milestones to test IDs, command IDs, evidence artifacts, and required-before gates.
- Expected result: Complete milestone proof map passes.
- Failure proves: staged proof timing can still be inferred late.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T7. Test-case asset includes command and evidence fields

- Covers: R21, R23
- Level: unit
- Command IDs: CMD1
- Fixture/setup: `skills/test-spec/assets/test-case.md`.
- Steps: Inspect or validate that the asset includes Command IDs, Evidence artifact, and Required by milestone fields.
- Expected result: The fields are present and named consistently.
- Failure proves: test cases can omit command/evidence ownership.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/test-spec/SKILL.md`
- Required by milestone: M1

### T8. Skeleton and resource map include new assets

- Covers: R22, R24-R26
- Level: unit
- Command IDs: CMD1
- Fixture/setup: `skills/test-spec/SKILL.md` and `skills/test-spec/assets/`.
- Steps: Check resource-map entries and asset existence for skeleton, test-case, coverage-map-row, validation-command-row, and milestone-proof-row.
- Expected result: Every mapped asset exists and uses `COPY` guidance.
- Failure proves: authoring guidance can reference missing or unmapped structures.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/test-spec/SKILL.md`
- Required by milestone: M1

### T9. Named command missing from ledger fails

- Covers: R1-R3, R33
- Level: unit
- Command IDs: CMD2
- Fixture/setup: negative fixture with a test case naming a command without a ledger row.
- Steps: Run representative validation.
- Expected result: Validation fails with a diagnostic naming the missing ledger mapping.
- Failure proves: the recent command-ownership omission can recur.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T10. Command missing classification fails

- Covers: R6, R7, R33
- Level: unit
- Command IDs: CMD2
- Fixture/setup: negative fixture with command row missing classification.
- Steps: Run representative validation.
- Expected result: Validation fails with a classification diagnostic.
- Failure proves: command reality can remain ambiguous.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T11. Planned command missing owner or milestone fails

- Covers: R8-R10, R33
- Level: unit
- Command IDs: CMD2
- Fixture/setup: negative fixture with incomplete planned command metadata.
- Steps: Run representative validation.
- Expected result: Validation fails with owner or milestone diagnostic.
- Failure proves: planned commands can be relied on before ownership exists.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T12. Milestone plan missing milestone proof map fails

- Covers: R15-R20, R33, E3, E4
- Level: integration
- Command IDs: CMD2
- Fixture/setup: negative fixture that references a milestone-based plan but omits milestone proof map.
- Steps: Run representative validation.
- Expected result: Validation fails with a missing milestone proof-map diagnostic.
- Failure proves: staged proof timing can remain implicit.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T13. Raw command string without Command ID fails

- Covers: R3-R5, R21, R33
- Level: unit
- Command IDs: CMD2
- Fixture/setup: negative fixture where a test case uses a raw command string but no Command ID.
- Steps: Run representative validation.
- Expected result: Validation fails with a Command ID diagnostic.
- Failure proves: test cases can bypass the command ledger.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T14. Trivial command-free non-milestone fixture passes

- Covers: R2, R16, R34, EC1, EC2, E2
- Level: integration
- Command IDs: CMD2
- Fixture/setup: valid fixture with no commands and no milestone-based plan.
- Steps: Run representative validation.
- Expected result: Fixture passes with explicit no-command and milestone-map not-applicable rationale.
- Failure proves: the upgrade overburdens trivial test specs.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k test_spec`
- Required by milestone: M2

### T15. Manual-proof asset remains absent

- Covers: R27-R29, E5, EC7
- Level: contract
- Command IDs: CMD1, CMD6
- Fixture/setup: `skills/test-spec/assets/` inventory and behavior-preservation evidence.
- Steps: Confirm `assets/manual-proof.md` is not added and Manual QA checklist behavior is recorded as unchanged.
- Expected result: No manual-proof asset exists; behavior-preservation evidence records Manual QA unchanged.
- Failure proves: out-of-scope manual-proof work leaked into the change.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md`
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; manual contract review
- Required by milestone: M1, M3

### T16. Status model and review route are preserved

- Covers: R30-R32, E5
- Level: contract
- Command IDs: CMD1, CMD6
- Fixture/setup: edited `skills/test-spec/SKILL.md` and behavior-preservation evidence.
- Steps: Confirm status enum remains unchanged, formal workflow-managed test specs still route to `test-spec-review`, and `test-spec` does not claim implementation, validation, branch, PR, or verify readiness.
- Expected result: Protected lifecycle boundaries are unchanged.
- Failure proves: proof-contract detail blurred stage ownership.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md`
- Automation location: `python scripts/validate-skills.py skills/test-spec/SKILL.md`; manual contract review
- Required by milestone: M1, M3

### T17. Generated skills and adapters include new assets

- Covers: R35
- Level: smoke
- Command IDs: CMD3, CMD4, CMD5
- Fixture/setup: canonical `skills/test-spec/` after M1 and M2.
- Steps: Run generated skill and adapter validation commands.
- Expected result: Generated outputs include revised `test-spec` skill and mapped assets from canonical sources.
- Failure proves: public installations can miss the proof-contract structures.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- Automation location: `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`
- Required by milestone: M3

### T18. Historical test specs are not migrated

- Covers: R36, EC6
- Level: migration
- Command IDs: CMD6
- Fixture/setup: changed-file list and behavior-preservation evidence.
- Steps: Confirm implementation changes canonical skill/assets/validators/proof artifacts only and does not rewrite historical `specs/*.test.md` files unrelated to this change.
- Expected result: Historical test specs are unchanged unless separately touched for an approved reason.
- Failure proves: the change creates broad migration churn outside proposal scope.
- Evidence artifact: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md`
- Automation location: lifecycle validation and diff review
- Required by milestone: M3

## Fixtures and data

Expected fixtures include:

- valid command-ledger output fixture;
- invalid named-command-missing-ledger fixture;
- invalid command-missing-classification fixture;
- invalid planned-command-missing-owner-or-milestone fixture;
- invalid milestone-plan-without-milestone-proof-map fixture;
- invalid raw-command-without-command-ID fixture;
- valid trivial non-milestone command-free fixture.

Exact fixture paths are selected during M2 implementation based on the existing validator harness.

## Mocking/stubbing policy

Use static Markdown fixtures and temporary generated output where existing repository tests already do so. Do not call network services, publish packages, mutate external state, or execute release-owned commands.

## Migration or compatibility tests

T18 proves historical test specs are not automatically migrated. T14 proves simple command-free and non-milestone test specs can still pass with explicit rationale.

## Observability verification

Change evidence is recorded in `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`, review records, behavior-preservation evidence, and validation command outputs recorded by implementation and verify stages.

## Security/privacy verification

T4 verifies safe-mode and side-effect boundary fields for commands with network, publication, destructive, or external side effects. The test spec does not require secrets or credentialed systems.

## Performance checks

No runtime performance requirement applies. Validation should avoid broad semantic scoring and use deterministic structural checks or representative fixtures.

## Manual QA checklist

- Review `behavior-preservation.md` for unchanged Manual QA behavior, test-spec status model, `test-spec-review` route, and no generated hand edits.
- Review changed files to confirm no unrelated historical test specs were migrated.

## What not to test and why

- Do not test manual-proof contract fields; manual-proof contracts are out of scope.
- Do not run release publication, network, destructive, or external-state commands.
- Do not require a full semantic validator for every future test spec in this slice.
- Do not test production behavior unrelated to authored skill and validation surfaces.

## Uncovered gaps

None.

## Next artifacts

```text
test-spec-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review`. This test spec does not authorize implementation until `test-spec-review` approves it and the active plan state is synchronized.
