# Specification Revision: Milestone Authority and Replay Identity

Artifact path: specs/governed-lifecycle-cli.md
Artifact identity: sha256:06e8856209816c1692cc3baab4a41b3936b8118f6be4c668de7a80665f0c1b82
Authoring result: complete

## Resolution intent

- `RLCLI-DEADLOCK-CR1`: milestone completion now closes and reports eligibility without starting its successor; workflow selects continuation by requesting `start-milestone`, and the CLI atomically applies that closed workflow-authorized operation.
- `RLCLI-DEADLOCK-CR2`: milestone completion stores a normalized full evidence identity, and every current-revision replay revalidates the milestone proof, review receipt, canonical review-log occurrence, packet inventory, review facts, milestone identity, and authority before idempotent success.

## Validation

- `python3 scripts/validate-documentation-prose.py --mode audit --path specs/governed-lifecycle-cli.md`: passed with zero errors and warnings.
- `python3 scripts/validate-boundary-first.py --path specs/governed-lifecycle-cli.md`: the feature boundary record is structurally consumable; validation reports the expected downstream proof-map gap for newly added `INT-005`, E6, and E7, which is owned by the subsequent test-spec revision.

This revision does not claim spec-review approval, architecture settlement, implementation readiness, or finding closeout.
