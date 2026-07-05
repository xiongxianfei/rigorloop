# Test-Spec Proof-Contract Upgrade

## Status

approved

Approved after clean `spec-review-r1`.

## Related proposal

- [Test-Spec Proof-Contract Upgrade](../docs/proposals/2026-07-04-test-spec-proof-contract-upgrade.md)
- Proposal review: [proposal-review-r1](../docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/proposal-review-r1.md), approved

## Goal and context

This spec defines a proof-contract upgrade for the `test-spec` authoring skill. The change makes validation command ownership and milestone proof timing explicit before implementation relies on a test spec.

The current `test-spec` skill already owns proof planning before implementation, routes formal workflow-managed test specs to `test-spec-review`, and keeps the test-spec artifact state as `active`. This spec preserves those boundaries while adding required authoring structures for command ledgers, input artifact identities, milestone proof maps, and command-linked test cases.

This spec intentionally excludes manual-proof contract work. Existing Manual QA checklist behavior remains unchanged.

## Glossary

- `validation-command ledger`: the `Validation commands` section in a test spec that assigns stable command IDs and records command ownership, milestone timing, evidence behavior, and side-effect boundaries.
- `Command ID`: a stable identifier such as `CMD1` used by test cases, milestone proof maps, and evidence rows instead of relying only on raw command strings.
- `command classification`: the closed command reality and ownership value recorded for each command.
- `milestone proof map`: the test-spec section that maps implementation milestones to test IDs, command IDs, evidence artifacts, and the gate where proof becomes required.
- `input artifact identities`: the section recording upstream artifact paths, statuses, review records, and identities used to author the test spec.
- `planned command`: a command named by the proof map that does not exist or is not configured yet, but is expected to be created by a named owner milestone.

## Examples first

Example E1: command-backed proof uses the ledger
Given a test spec names `python scripts/test-skill-validator.py`
When the test spec includes test cases that depend on that command
Then the command appears in `Validation commands` with a stable command ID
And the test cases reference that command ID.

Example E2: command-free proof remains lightweight
Given a trivial test spec has no validation command dependency
When the test spec reaches the `Validation commands` section
Then it states that no validation commands are part of the proof map
And it gives a short rationale.

Example E3: planned command is not required too early
Given a test spec names a command that will be added during milestone `M2`
When milestone `M1` is reviewed
Then the command ledger shows the command as `planned-for-implementation`, owner `M2`, and first required milestone `M2`
And `M1` does not fail solely because the planned command is not yet executable.

Example E4: milestone proof map separates staged proof
Given an approved plan has milestones `M1` and `M2`
When the test spec is authored
Then the milestone proof map identifies the test IDs, command IDs, evidence artifacts, and required-before gate for each milestone.

Example E5: manual-proof contracts remain out of scope
Given a test spec includes a Manual QA checklist
When this upgrade is applied
Then the checklist behavior is unchanged
And no `assets/manual-proof.md` is added by this change.

## Requirements

R1. `skills/test-spec/SKILL.md` MUST define `Validation commands` as a conditional required section whenever a test spec names, references, or depends on validation commands.

R2. When no validation commands are part of a test spec proof map, the `Validation commands` section MUST explicitly state that no validation commands are part of the proof map and give a rationale.

R3. Every named, referenced, or depended-on validation command MUST have a stable Command ID.

R4. Test cases that use or depend on a validation command MUST reference at least one Command ID.

R5. Milestone proof-map rows that use or depend on validation commands MUST reference Command IDs.

R6. The command classification enum MUST be exactly:

```text
existing/configured
planned-for-implementation
release-owned
ci-owned
external-owned
not-applicable
```

R7. Unknown command classification values MUST fail closed in validator or representative fixture coverage.

R8. Each validation-command ledger entry MUST include command ID, command, classification, owner, owning milestone, first required milestone, failure behavior, zero-test behavior, evidence artifact, and safe-mode or side-effect boundary.

R9. A `planned-for-implementation` command MUST name an owner, owning milestone, and first required milestone.

R10. A planned command MUST NOT be treated as required before its first required milestone.

R11. A command expected to run tests MUST define zero-test behavior.

R12. Commands with network, publication, destructive, or external side effects MUST state the safe-mode or side-effect boundary.

R13. `skills/test-spec/SKILL.md` MUST define `Input artifact identities` as required when implementation or code-review will rely on the test spec.

R14. The input artifact identities structure MUST record input kind, path, status or review state, and identity for the feature spec, relevant review records, plan, plan review, and architecture or ADR inputs when applicable.

R15. `skills/test-spec/SKILL.md` MUST define `Milestone proof map` as required when the approved plan has milestones, staged validation, staged commands, or milestone-specific code-review boundaries.

R16. When no milestone proof map is applicable, the test spec MUST state `Not applicable` or equivalent explicit rationale.

R17. Each implementation milestone in a milestone-based plan MUST map to test IDs, command IDs, evidence artifacts, or an explicit not-applicable rationale.

R18. The milestone proof map MUST identify which proof is required before milestone code-review.

R19. The milestone proof map MUST identify proof deferred to later milestones, verify, release-owned evidence, or another explicitly named stage.

R20. No milestone may rely on a command whose ownership starts in a later milestone unless the row explicitly marks the command as planned and not yet required.

R21. The test-case format MUST include `Command IDs`, `Evidence artifact`, and `Required by milestone` fields.

R22. `assets/test-spec-skeleton.md` MUST include sections for `Input artifact identities`, `Validation commands`, and `Milestone proof map`.

R23. `assets/test-case.md` MUST include `Command IDs`, `Evidence artifact`, and `Required by milestone` fields.

R24. `assets/validation-command-row.md` MUST be added as a repeated structure for validation-command ledger rows.

R25. `assets/milestone-proof-row.md` MUST be added as a repeated structure for milestone proof-map rows.

R26. `skills/test-spec/SKILL.md` MUST map every `test-spec` asset in its resource map using `COPY`, including the new validation-command and milestone-proof assets.

R27. This spec amends the earlier `test-spec` asset inventory limit in `specs/spec-family-assets-progressive-disclosure.md` only for `assets/validation-command-row.md` and `assets/milestone-proof-row.md`.

R28. This change MUST NOT add `assets/manual-proof.md` or manual-proof contract requirements.

R29. Existing Manual QA checklist behavior MUST remain unchanged.

R30. The test-spec artifact status model MUST remain unchanged: `active` is the relied-on proof-planning state and approval lives in `test-spec-review`.

R31. Formal workflow-managed test specs MUST still route from `test-spec` to `test-spec-review` before implementation.

R32. `test-spec` MUST NOT claim implementation completion, validation success, branch readiness, PR readiness, or verification.

R33. Representative fixture coverage MUST include a valid command ledger and negative cases for named command missing from ledger, command missing classification, planned command missing owner or milestone, milestone plan missing milestone proof map, and raw command string in a test case without Command ID.

R34. Representative fixture coverage MUST include a trivial non-milestone, command-free test spec that passes with explicit not-applicable rationale.

R35. Generated skill and adapter proof MUST show the revised `test-spec` skill and all mapped assets are included from canonical authored sources.

R36. Historical test specs MUST NOT be automatically migrated by this change.

## Inputs and outputs

Inputs:

- accepted proposal `docs/proposals/2026-07-04-test-spec-proof-contract-upgrade.md`;
- approved `proposal-review-r1`;
- canonical `skills/test-spec/SKILL.md`;
- current `skills/test-spec/assets/` files;
- current skill validation and generated-output scripts;
- governing skill contracts, including `specs/spec-family-assets-progressive-disclosure.md` and `specs/skill-contract.md`.

Outputs:

- updated `skills/test-spec/SKILL.md`;
- updated `skills/test-spec/assets/test-spec-skeleton.md`;
- updated `skills/test-spec/assets/test-case.md`;
- new `skills/test-spec/assets/validation-command-row.md`;
- new `skills/test-spec/assets/milestone-proof-row.md`;
- validator or representative fixture coverage for the new proof-contract shape;
- generated skill and adapter inclusion proof;
- behavior-preservation evidence for unchanged role, state model, review route, and Manual QA behavior.

## State and invariants

- `test-spec` remains an authoring skill for pre-implementation proof design.
- `test-spec-review` remains the independent review gate for proof adequacy.
- The test-spec artifact remains `active` while relied on.
- Command IDs are stable within a test spec.
- Command classifications are closed vocabulary values.
- The skeleton owns structure; `SKILL.md` owns policy.
- Manual-proof contracts are outside this change.

## Error and boundary behavior

- A test spec that names a validation command without a ledger entry is invalid for representative validation.
- A test case that uses a raw command string without a Command ID is invalid for representative validation.
- A planned command without owner, owning milestone, or first required milestone is invalid for representative validation.
- A milestone-based plan without a milestone proof map or explicit not-applicable rationale is invalid for representative validation.
- Unknown command classifications fail closed.
- Missing generated-output inclusion proof blocks readiness for PR.

## Compatibility and migration

This change is additive for future authored test specs and does not migrate historical test specs. Existing test specs remain historical evidence unless they are changed or used as current authoritative proof for new implementation.

Rollback is to remove the new `test-spec` proof-contract structures, remove the two new assets, restore the previous skeleton and test-case asset fields, and rebuild generated output from canonical sources. Generated adapter output must not be hand-edited.

## Observability

The change is observable through canonical skill diffs, asset diffs, resource-map entries, representative fixture results, validator output, generated-output proof, behavior-preservation evidence, review records, and downstream verification artifacts.

## Security and privacy

The command ledger must surface network, publication, destructive, and external side-effect boundaries before commands are relied on. The change does not execute commands during `test-spec` authoring and does not introduce secrets or new credential handling.

## Accessibility and UX

Not applicable. This change affects repository workflow artifacts and published skill text, not end-user UI.

## Performance expectations

The added proof-contract structure should avoid broad semantic validation as the primary enforcement mechanism. Deterministic asset-shape checks and representative fixtures are preferred. Token-cost impact should be considered during implementation, but correctness and proof clarity take precedence.

## Edge cases

EC1. A command-free test spec: the `Validation commands` section records no commands with rationale.

EC2. A one-shot non-milestone change: the `Milestone proof map` section records not-applicable rationale.

EC3. A command exists in CI but not locally: classify it as `ci-owned` and state evidence ownership and local safe-mode boundary.

EC4. A release-owned command cannot be run during implementation: classify it as `release-owned` and identify the evidence artifact and owning stage.

EC5. A planned command is created in a later milestone: record planned ownership and first required milestone before downstream reliance.

EC6. Historical test specs lack the new sections: do not migrate them solely because this spec is approved.

EC7. Manual proof is requested during implementation: route that concern through existing Manual QA behavior or a separate manual-proof proposal, not this change.

## Non-goals

- Executing validation commands during `test-spec` authoring.
- Implementing tests or production code.
- Replacing `test-spec-review`.
- Changing the test-spec status model.
- Adding manual-proof contracts or `assets/manual-proof.md`.
- Migrating historical test specs.
- Hand-editing generated adapter output.
- Building a full semantic validator for every future test-spec artifact in this slice.

## Acceptance criteria

AC1. `test-spec` requires a validation-command ledger whenever commands are named, referenced, or depended on.

AC2. Every named command has a stable Command ID and closed classification.

AC3. Planned commands identify owner, owning milestone, and first required milestone.

AC4. Command entries include failure behavior, zero-test behavior, evidence artifact, and safe-mode boundary.

AC5. Test cases reference Command IDs when commands are involved.

AC6. Milestone-based plans include a milestone proof map.

AC7. The skeleton includes `Input artifact identities`, `Validation commands`, and `Milestone proof map`.

AC8. Repeated structures for validation-command rows and milestone-proof rows exist as packaged assets and are mapped in `SKILL.md`.

AC9. Manual proof contracts and `assets/manual-proof.md` are absent from this change.

AC10. The upgraded skill still routes formal workflow-managed test specs to `test-spec-review`.

AC11. The test-spec artifact state model remains unchanged.

AC12. Representative fixtures catch missing command ownership and missing milestone proof mapping.

AC13. Generated adapters include the revised skill and new assets.

AC14. Historical test specs are not automatically migrated.

## Open questions

None.

## Next artifacts

```text
spec-review
architecture assessment
plan
plan-review
test-spec
test-spec-review
```

## Follow-on artifacts

- Spec review: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/spec-review-r1.md`

## Readiness

Approved after clean `spec-review-r1`; ready for `plan`.
