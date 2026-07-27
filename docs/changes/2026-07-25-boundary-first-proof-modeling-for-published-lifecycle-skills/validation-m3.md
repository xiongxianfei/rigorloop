# M3 Validation: Downstream Projection and Preservation

Date: 2026-07-27

Milestone: M3

Result: pass

## Scope

- Added the mapped boundary-proof reference to `implement`, `code-review`, and
  `verify`; all eight governed skills now carry the shared reference bytes.
- Added stage-owned boundary-first implementation, review, verification, and
  workflow routing guidance.
- Added invocation-free preservation generation and validation.
- Materialized immutable before snapshots from baseline commit
  `cc6065ab03aab10427d7908973ed4952ca614e0f`.
- Published preservation run
  `run-029e566b0597c59e9bc029ce60562e9d`.

## Automated evidence

| Command | Result |
| --- | --- |
| `python scripts/validate-skills.py` | pass; 24 skills |
| `python scripts/test-skill-validator.py` | pass; 260 tests |
| `python scripts/build-skills.py --check` | pass |
| `python scripts/test-boundary-proof.py` | pass; 111 tests |
| `python scripts/boundary_proof_behavior.py generate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` | pass; 40 pairs; zero upstream invocations |
| `python scripts/boundary_proof_behavior.py validate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` | pass; 40 pairs; zero upstream invocations |
| `git diff --check` | pass |

The preservation regression covers missing and duplicate pair entries, stale
origin commits, cross-pair after references, stale materialized bytes, exact
historical origins, current skill and resource identities, and the closed
eight-skill by five-category key set.

## Manual review boundary

The harness proves structure, origin, identity, completeness, and absence of
upstream reinvocation. It marks every pair as requiring semantic review.
`code-review` remains responsible for deciding whether routing, claim
boundaries, review recording, isolation, and handoff meaning were preserved.

