# Requirement-Fidelity Gate Behavior Preservation

## Scope

This M5 evidence covers the first-slice requirement-fidelity gate after M1 through M4 implementation and review closeout.

Reviewed scope:

- canonical review guidance and workflow surfaces changed in M1;
- requirement-fidelity review and lifecycle validators changed in M2;
- R26 property-list by surface-list validator pilot changed in M3;
- requirement-compression calibration records and sampling validation changed in M4;
- generated skill and adapter output proof is performed through repository build commands, not hand-edited output.

## Preservation Matrix

| Surface | Baseline | Revised proof | Result |
| --- | --- | --- | --- |
| Review independence | Independent-review gate records fresh context, phase receipts, risk map, clean-review sufficiency evidence, and second-review/calibration behavior. | Existing review-artifact and lifecycle validator suites still pass after requirement-fidelity additions; no independent-review fixtures are rewritten by this slice. | strengthened |
| Clean automated review | Clean review could advance with independent-review sufficiency evidence. | Workflow-managed clean review now also records requirement-fidelity applicability and a valid fidelity receipt when applicable; direct and historical review behavior remains compatible. | strengthened |
| Spec canonical comparison | Review could compare implementation and validator agreement without first decomposing the governing spec clause. | Code-review guidance and review records now require spec-first packet ordering, requirement-property decomposition, and per-property evidence when applicable. | strengthened |
| Validator tests | Hand-listed assertions could encode a compressed subset of a spec clause. | Selected contracts use source-annotated property and surface constants; R26 and requirement-compression calibration have targeted negative tests for omitted or trivial required properties. | strengthened |
| Calibration | Review calibration did not measure requirement-compression recall. | Requirement-compression seeded defects, named iteration IDs, rotation triggers, sampling floors, and not-applicable audit fields are validated with closed vocabularies. | strengthened |
| Workflow stage order | Normal lifecycle order and implementation-through-verify phase boundaries governed handoff. | Stage order is unchanged; M1-M4 each closed only after implementation, review, and any required review-resolution, and M5 still requires code-review before explain-change or verify. | preserved |
| Historical reviews | Historical clean reviews remain durable evidence under their original contract. | R50 is preserved: historical clean reviews are not retroactively invalidated solely for lacking requirement-fidelity receipts. | preserved |
| Manual reviews | Manual reviews did not have mandatory first-slice requirement-fidelity applicability classification. | Manual reviews may voluntarily record a fidelity receipt, but mandatory manual-review applicability remains out of first-slice scope. | preserved |
| Finding behavior | Review quality was not governed by a finding quota. | No finding quota or forced-failure policy is introduced; calibration measures defect recall, not finding count. | preserved |
| Generated output | Public adapter outputs are generated release artifacts and must not be hand-edited. | M5 runs normal skill/adaptor build and validation commands; generated public adapter output is checked through temporary build output. | preserved |

## Requirement Coverage

| Requirement | Preservation evidence |
| --- | --- |
| `R46` | Existing independent-review and lifecycle validator suites are rerun after requirement-fidelity changes. |
| `R47` | The slice updates selected validators, selected skill guidance, fixtures, and evidence records only; it does not rewrite all historical reviews, all validators, or all specs. |
| `R48` | Applicability trigger and requirement-compression seeded-defect lists are represented as closed constants with validator or skill-validator coverage. |
| `R49` | Generated public adapter output is refreshed and checked only through normal build and validation commands. |
| `R50` | Historical clean reviews remain compatible; missing requirement-fidelity receipts are enforced only for current applicable workflow-managed review surfaces. |
| `AC-RFG-016` | Independent-review gate behavior remains covered by existing review-artifact and lifecycle tests. |
| `AC-RFG-017` | No implementation surface introduces a minimum finding count or forced-finding rule. |
| `AC-RFG-018` | Historical review records are not migrated or invalidated solely for missing fidelity receipts. |
| `AC-RFG-019` | Manual review fidelity receipts are voluntary in the first slice. |
| `AC-RFG-020` | Steady-state sampling floors are validated and cannot drop below the R17b floors without a follow-on amendment. |

## Generated Output Proof

M5 uses generated-output checks rather than direct edits to generated artifacts:

- `python scripts/test-build-skills.py`
- `python scripts/build-skills.py --check`
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`

If these checks modify no tracked generated output, M5 records that generated surfaces are current through normal generation.

## Lifecycle Closeout Boundary

This file is behavior-preservation evidence for M5 implementation handoff only.

It does not claim:

- final holistic code-review is complete;
- explain-change is complete;
- verify is complete;
- PR readiness;
- hosted CI or human review.

Those remain downstream lifecycle gates after M5 code-review.
