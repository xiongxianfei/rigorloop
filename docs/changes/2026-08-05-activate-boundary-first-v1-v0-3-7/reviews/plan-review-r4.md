# Plan Review: Boundary Activation Release R4

Review ID: plan-review-r4
Stage: plan-review
Round: 4
Reviewer: independent Codex plan-review peer
Target: `docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md`
Target revision: `8d60d681cee48294ba950bd4256d5d3bfeb42a7c`
Status: approved
Material findings: None
Immediate next stage: test-spec revision and review
Implementation readiness: blocked on stale test spec, not on plan defects

## Result

- Review status: approved
- Recording status: recorded
- Recording blocker: none
- Open blockers in plan: none
- Test-spec readiness: not-ready until proof-map alignment and review

The plan matches the approved `P ... B -> T ... R -> C ... H` contract. It
separates candidate `T..R` from readiness `T..H`, requires immediate `R -> C`
and `C` containment in `H`, retains readiness-returned full `H` in the publish
invocation, and uses that exact SHA with `T` in the atomic refspec.

## Review Dimensions

Scope, sequencing, dependencies, recovery, architecture alignment, validation
strategy, command executability, state ownership, maintainability, and
test-driven handoff all pass at the plan gate.

The current test spec remains stale and must add `candidate_validation_head`,
EC7A/EC11A, `R -> C`, `C` in `H`, candidate-at-R versus readiness-at-H, and
same-invocation exact-H/head-movement proof before implementation resumes.

## Validation Evidence

- `git diff --check 34ce51a0..8d60d681` passed.
- The checkpoint shell extracted from the plan passed `bash -n`.
- Change metadata, explicit artifact lifecycle, and review artifacts passed.
- The boundary-first spec validator does not accept plan paths; that input-contract rejection is not a plan validation failure.

## Clarification

The checkpoint conservatively preserves the local tag once `--publish` is
invoked. This is compatible with BFA-R027, which permits deleting or ignoring
the local candidate tag. The test spec should distinguish preview failure from
publish-invocation failure explicitly.

## Recommendation

Approve the plan and route directly to test-spec revision and fresh review.
