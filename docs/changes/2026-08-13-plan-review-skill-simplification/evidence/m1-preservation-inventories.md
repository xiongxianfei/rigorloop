# M1 Preservation Inventories

- Milestone: M1
- Result: implementation-complete; ready for code review
- Canonical skill prose changed: no
- Semantic rules: 22
- Literal dependencies: 20
- Static scenarios: 23
- Invalid closed-vocabulary fixtures: 2
- Baseline: `evidence/profile-size-baseline.md`

The semantic ledger separates universal inline judgment and recording, governed transaction procedure, boundary procedure, structural assets, and duplicate removal. The literal inventory separately classifies normative, parser/package, incidental-test, obsolete, and historical dependencies. Unknown disposition and classification fixtures prove fail-closed validation ordering.

## Validation

- M1 change-local standard-library evidence proof: passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-13-plan-review-skill-simplification/change.yaml`: passed before implementation-state handoff.
- Independent source and consumer audit: completed against the full current skill and targeted repository consumers.

## Unchanged required surfaces

- `skills/plan-review/SKILL.md`: intentionally unchanged until M2 because M1 freezes ownership first.
- Existing boundary reference: unaffected; its exact path and bytes remain governed by the existing projection contract.
- Specs, validators, and package generators: unaffected in M1; their required changes belong to M2 or M3.

## Claim limitations

M1 does not claim the skill is simplified, reviewed, verified, branch-ready, or PR-ready.
