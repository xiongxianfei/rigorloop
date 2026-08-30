# Boundary-first proof guidance

Boundary model version: boundary-first-v1

Use this owner-scoped guidance with the compact core when authoring or reviewing a proof map.

## Test-spec proof record

The proof map consumes the exact boundary and interaction IDs from its governing feature contract.
It never defines, renames, infers, or repairs them.
Start with the same model version and scope, then use:

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Coverage state is exactly `covered` or `gap`.
A covered row supplies every field required by its proof and automation mode and uses `-` for the uncovered-gap ID.
A gap row supplies its requirements, boundary or interaction IDs, required milestone, and one stable gap ID.
It uses `-` for test case, proof level, automation mode, command, evidence, and manual-procedure fields.
A gap never counts as coverage and blocks downstream reliance.

Proof level is exactly `unit`, `integration`, `contract`, `end-to-end`, `smoke`, or `manual`.
Automation mode is exactly `automated`, `manual`, or `hybrid`.
Automated proof uses `-` for manual procedures.
Manual and hybrid proof cite a stable manual procedure and evidence artifact.

## Negative and composed proof

Where admitted by a boundary, proof covers valid, invalid, missing, additional, stale, substituted, unknown, and conflicting states.
Stateful proof covers legal and illegal transitions.
Mutation proof covers commit, partial, retry, reconciliation, conflict, and replay.
Composed proof exercises the public path and every material sibling path, not only a helper.

## Proof adequacy review

Confirm every applicable boundary and selected interaction has direct proof.
Confirm proof uses exact IDs from the governing feature contract.
Confirm the chosen proof level and automation mode establish the claimed outcome.
Confirm evidence is current, direct, and no broader than its claim.
Route missing proof without changed behavior to proof-map authoring.
Route any newly discovered or changed outcome to feature-spec authoring.
