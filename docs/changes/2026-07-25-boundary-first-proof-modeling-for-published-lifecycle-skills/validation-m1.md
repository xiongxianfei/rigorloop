# M1 Validation Evidence

Stage: implement
Milestone: M1
Result: passed

## Commands

- `python scripts/test-boundary-proof.py` — passed 13 tests.
- `python scripts/validate-boundary-proof.py --help` — passed.
- `python -m py_compile scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py` — passed.
- `python scripts/test-artifact-lifecycle-validator.py` — passed 156 tests.

## Scope

The evidence covers the immutable typed projection, exact and unknown closed
values, record shape, applicability-dependent fields, reference integrity,
legacy/v1 parity, the exact incident registry, the compact simple fixture,
computed report aggregation, evidence requirements, and validator-owned
synthetic report serialization.

Direct negative proof covers malformed and duplicate example evidence IDs,
unrelated known requirements, mixed-reference ownership, every incident label
mutation, multi-trigger state, partial marker/scope combinations, missing,
unsafe and stale evidence, invalid not-run blockers, mapping-order byte
permutations, false blocking, extra lifecycle artifacts, and multiple
correction cycles.
