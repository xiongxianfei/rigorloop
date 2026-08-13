# Proposal Revision R3: Plan Skill Simplification

Stage: proposal
Date: 2026-08-13
Artifact: `docs/proposals/2026-08-12-plan-skill-simplification.md`
Responds to: `proposal-review-r3`

## Changes made

- Resolved `PLSIM-PR7` by adding the closed `initialize-approved-plan` operation, defining legal temporary primary-plan and `planned_work` combinations, separating clean review evidence from settlement, and requiring an identical plan-review settlement retry without rerunning judgment.
- Resolved `PLSIM-PR8` by defining stable plan identity as artifact ID, kind, role, and normalized path and reviewed revision identity through existing review and repository-revision evidence, with no content hash or new identity field.
- Resolved `PLSIM-PR9` by selecting `architecture-required`, requiring canonical system-architecture updates and a narrow successor to ADR-20260729, and keeping architecture assessment status and artifact pointers in the owning change record.

## Contract effect

The downstream specification must amend the current primary-plan versus `planned_work` invariant, review settlement sequencing, directly coupled skill and workflow contracts, validators, parsers, and fixtures. The architecture package must define the evidence-initialization-settlement transaction before execution planning.

## Preservation result

The package shape, four loading profiles, exactly three assets, boundary activation, plan-owned initial derivation, plan-review-owned judgment and settlement, workflow-owned routing and later transitions, read-old/write-new migration, and no-runtime acceptance boundary remain unchanged. This revision introduces no hash, lifecycle stage, service, dependency, state store, or independent callback owner.

## Review request

The proposal is returned to `review-required` for independent proposal-review round 4. This revision does not claim approval, specification readiness, architecture completion, or automatic downstream handoff.
