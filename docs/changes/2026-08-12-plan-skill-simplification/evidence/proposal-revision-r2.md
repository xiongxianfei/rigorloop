# Proposal Revision R2: Plan Skill Simplification

Stage: proposal
Date: 2026-08-13
Artifact: `docs/proposals/2026-08-12-plan-skill-simplification.md`
Responds to: `proposal-review-r2`

## Changes made

- Resolved `PLSIM-PR4` by separating governed change authority from closed `create-primary-plan` and `revise-primary-plan` operations, including exact file/entry absence, presence, identity, conflict, and idempotent creation behavior.
- Resolved `PLSIM-PR5` by selecting post-approval initialization, binding the plan-owned initializer to clean plan and review identities, making identical retry a no-op, blocking existing mismatch, and routing post-initialization baseline changes to governed replan or migration.
- Resolved `PLSIM-PR6` by adopting `stage-owned-change-local-v1` read-old/write-new compatibility, preserving historical documents, making `change.yaml` the sole active-state authority, blocking incomplete active legacy state, and prohibiting reverse synchronization.

## Contract effect

This revision explicitly changes the current lifecycle contract's initialization timing. The downstream specification must amend the existing pre-review initialization clauses and directly coupled workflow, skill-contract, validator, parser, and fixture surfaces. It must preserve plan ownership of the initial derivation and workflow ownership of every later transition.

## Preservation result

The package shape, boundary activation, three-asset limit, portable and governed profiles, structural measurement model, plan-review ownership, and target-runtime exclusion remain unchanged. No new runtime, persistence model, schema selector, stage, skill, reference, or asset is introduced.

## Review request

The proposal is returned to `review-required` for independent proposal-review round 3. This revision does not claim approval or specification readiness.
