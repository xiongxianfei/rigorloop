# Behavior Preservation: Test-Spec Proof-Contract Upgrade

## Status

M3 implementation evidence.

## Scope

This record proves the M3 preservation requirements from `specs/test-spec-proof-contract-upgrade.md`: R27-R32, R35, and R36.

## Preservation Matrix

| Surface | Baseline | New proof | Result |
| --- | --- | --- | --- |
| Test-spec role | Proof design before implementation | `skills/test-spec/SKILL.md` still routes authored workflow-managed test specs to downstream review before implementation | preserved |
| Status model | `draft`, `active`, `abandoned`, `superseded`, `archived` | The status set remains unchanged; `active` remains the relied-on proof-planning state | preserved |
| Review route | `test-spec-review` before implementation | Formal workflow-managed test specs still use `test-spec-review` before implementation handoff | preserved |
| Requirement coverage | Required in authored test specs | Requirement coverage remains a required section and is not replaced by the command ledger | preserved |
| Example coverage | Required in authored test specs | Example coverage remains a required section and is not replaced by the command ledger | preserved |
| Command ownership | Broad or implicit | Validation-command rows now require ID, classification, owner, milestones, failure behavior, zero-test behavior, evidence artifact, and safe-mode boundary | strengthened |
| Manual QA | Existing checklist behavior | Manual QA checklist behavior remains unchanged; no manual-proof contract asset is added | preserved |
| Manual-proof contracts | Out of scope for this proposal | `skills/test-spec/assets/manual-proof.md` is absent and no manual-proof contract section is introduced | preserved |
| Milestone proof | Implicit in cases | Milestone proof-map rows now make proof timing explicit when plans are milestone-based | strengthened |
| Generated adapters | Generated from canonical skills and assets | Repository-owned generated-skill and adapter checks prove the revised skill and mapped assets are included from canonical authored sources | preserved |
| Historical test specs | No automatic migration | This change does not rewrite historical `specs/*.test.md` files unrelated to this change | preserved |

## Protected Boundary Evidence

- R27 is preserved by adding only the approved `assets/validation-command-row.md` and `assets/milestone-proof-row.md` entries to the `test-spec` asset inventory.
- R28 is preserved because `skills/test-spec/assets/manual-proof.md` was not created.
- R29 is preserved because the existing Manual QA checklist section remains the checklist surface; manual-proof contracts are not introduced.
- R30 is preserved because `Status: active` remains the relied-on test-spec state and approval still belongs to `test-spec-review`.
- R31 is preserved because formal workflow-managed test specs still route to `test-spec-review` before implementation.
- R32 is preserved because the skill text does not claim implementation completion, validation success, branch readiness, PR readiness, or verification.
- R35 is proven by the M3 generated-skill and adapter validation commands recorded in `change.yaml`.
- R36 is preserved because historical test specs are not automatically migrated; the only touched test spec is the approved change-local governing test spec for this initiative.

## Generated Output Handling

Generated output proof uses repository-owned scripts only:

- `python scripts/build-skills.py --check`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-skills.py`

No generated public adapter package body is hand-edited as part of this proof. If a generated-output check reports drift, the recovery path is to update canonical authored sources or run the repository-owned generator, then validate again.

## Historical Migration Boundary

Historical test specs are outside this proposal's migration scope. This M3 proof limits edits to canonical skill sources, validator tests, the approved governing spec/test-spec/plan artifacts, and change-local evidence for `2026-07-04-test-spec-proof-contract-upgrade`.
