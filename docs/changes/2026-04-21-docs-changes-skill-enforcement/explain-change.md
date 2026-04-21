# Docs Changes Skill Enforcement Explain Change

## Why this change exists

The repository already approved the baseline docs-changes contract for ordinary non-trivial work, but the stage-local skills still left too much of that requirement to contributor memory. This follow-up makes the skills operationalize the contract directly.

## Approved source trail

- proposal: `docs/proposals/2026-04-21-docs-changes-skill-enforcement.md`
- spec: `specs/docs-changes-skill-enforcement.md`
- plan: `docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
- test spec: `specs/docs-changes-skill-enforcement.test.md`

## What changed so far

- M1 aligned `workflow` and `implement` so ordinary non-trivial work carries the baseline change-local pack while fast-lane omission stays narrow.
- M2 aligned `verify`, `pr`, and `explain-change` so missing required baseline packs become explicit blockers and the default durable reasoning surface stays change-local for new ordinary non-trivial work.
- M3 confirmed no directly related summary drift remained and the standard repo-owned smoke path (`bash scripts/ci.sh`) still passed with the updated skill guidance.
- Final verify confirmed the full feature diff remained coherent against the approved spec, related proof surfaces, and the stacked docs-changes contract.

## Scope boundaries

- no `change.yaml` schema redesign
- no change to the approved baseline-versus-conditional docs-changes contract
- no validator-side inference for missing packs without a `change.yaml`
- no broadening of docs-changes requirements into fast-lane work

## Change-local note

This file is the default durable reasoning surface for the feature itself. It stays concise and points back to the approved top-level proposal, spec, plan, and test spec instead of duplicating them.
