# Explain Change: Spec Skill Simplification

## Summary

The change makes portable `spec` authoring materially shorter while keeping governed lifecycle mutation explicit and conditional. `SKILL.md` remains the universal contract, both existing boundary references still load initially, one new governed reference owns lifecycle-authorized creation, revision, retry, and stale restart, and the existing skeleton owns one conditional formal-boundary insertion point.

## Problem

The previous package mixed portable contract judgment with `change.yaml` mutation and detailed authoring recovery. Every invocation therefore loaded governed procedure even when it could not use it, while ordinary layout and formal boundary composition were partly duplicated. The goal was to reduce both real loaded profiles without weakening customer portability, contract quality, boundary-first adoption, stage ownership, content preservation, or `spec-review` handoff.

## Decision trail

- Proposal: selected one governed-authoring reference while retaining both always-loaded boundary references and one structural skeleton.
- Specification: R1-R67 closed package shape, tri-state governed signals, portable operations, governed transactions, stale restart, boundary-block transitions, semantic/literal preservation, measurements, and package parity.
- Architecture: `architecture-not-required`; the change reuses the existing packaged-skill, artifact-entry, authoring-evidence, and generated-adapter models.
- M1: recorded 28 semantic rules, 50 literal dependencies, 34 deterministic scenarios, unknown-value fixtures, and the baseline.
- M2: implemented the package split, focused tests, packaged-resource registration, and structural marker; code review required and then approved two semantic corrections.
- M3: recorded final measurements, reconciled every rule and literal, and proved archive and clean-install parity.

## Diff rationale by area

| Area | Change | Reason | Source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/spec/SKILL.md` | Replaced mixed common-path prose with a compact universal dispatcher and closed signals, operations, stops, claims, composition, and resource triggers. | R2-R20 require portable self-sufficiency and no invalid governed fallback. | Approved spec and SRULE-001-SRULE-007, SRULE-014, SRULE-018-SRULE-028. | `SpecSkillSimplificationTests`; broad skill suite; final review. |
| `skills/spec/references/governed-spec-authoring.md` | Added exact authority, create/revise, retry, stale detection, authorized restart, preservation, write, and handoff procedure. | R21-R42 require identity-bound governed mutation without a new state or owner. | Approved spec; `SPSIM-M2-CR1`. | Focused transaction assertions; lifecycle contract tests. |
| `skills/spec/assets/spec-skeleton.md` | Added one marker between error behavior and compatibility. | R43-R56 require a single structural insertion point while the feature reference owns formal content. | Approved proposal/spec and SRULE-017. | Focused ordering and uniqueness assertion. |
| `scripts/test-skill-validator.py` | Added six focused tests and migrated directly coupled lifecycle and initial-boundary consumers. | R57-R62 require deterministic invariant owners and atomic consumer migration. | Test spec T1-T16; `SPSIM-M2-CR2`. | Focused and full 348-test suite. |
| `scripts/skill_validation.py` | Added the governed reference to the existing packaged-resource allowlist. | The new mapped reference must pass the existing package contract. | R1, R3-R5, R66. | Canonical validation, build checks, adapter validation. |
| Change-local ledgers, fixtures, reviews, measurements, and proof | Recorded decisions, corrections, profile accounting, semantics, and package evidence. | R57-R67 require auditable preservation and honest measurement without permanent machinery. | M1-M3 and lifecycle contract. | CMD1-CMD11 and formal reviews. |

The existing boundary references were intentionally unchanged and remain byte-identical to baseline. Generated adapter trees were built only in temporary directories; no generated public adapter output was hand-edited.

## Tests added or changed

`SpecSkillSimplificationTests` proves the two profiles and exact resource map, tri-state governed signals, portable authority, R21-R42 transaction groups, boundary-block and anchor states, universal semantic preservation, missing-resource stops, and forbidden claims. Existing stage-owned lifecycle tests now read the conditional governed reference when checking `spec`. Existing boundary-first tests now enforce the approved initial loading for `spec`. The existing validator and adapter suites remain the owners of package structure, generated inventory, archives, and clean installs.

This is the appropriate proof level because the change alters published Markdown contracts and package composition, not an agent runtime. Static contract scenarios, repository validators, ordinary review, and byte-level package checks are deterministic; target-agent transcript grading would add a different runtime acceptance system.

## Validation evidence available before final verify

- CMD1 passed with 28 rules, 50 literals, 34 scenarios, and unknown values rejected first.
- `python scripts/validate-skills.py skills/spec/SKILL.md` passed.
- The focused suite passed six tests; the full skill suite passed 348 tests with 16 skips.
- `python scripts/test-build-skills.py` passed seven tests, and `python scripts/build-skills.py --check` passed.
- Boundary-first validation passed for the approved specification.
- `python scripts/test-adapter-distribution.py` passed all discovered tests.
- Fresh v0.4.0 Codex, Claude, and opencode archives and clean `spec` installs passed validation.
- Change metadata, review closeout, documentation prose, and diff checks passed at their recorded handoffs.
- Hosted CI status is not yet known; final verify owns current branch and CI-readiness judgment.

## Review resolution summary

All eight material findings are accepted and closed, with no `needs-decision` disposition and no open review-log finding. Five proposal findings closed the direction and recovery contracts. `SPSIM-M1-CR1` completed the inventories. `SPSIM-M2-CR1` made governed transactions explicit, and `SPSIM-M2-CR2` restored incomplete universal rules. See `review-resolution.md` for the durable dispositions and validation links.

## Alternatives rejected

- Inline compression alone could not remove governed procedure from portable loads.
- Moving boundary procedure behind a new trigger would violate the already approved initial-loading contract.
- Multiple narrow governed references would add navigation without distinct activation boundaries.
- A runtime classifier, new validator family, tokenizer dependency, or target-agent evaluation would introduce machinery disproportionate to a content and package refactor.
- Silent overwrite or workflow-owned stale restart would weaken content preservation and stage ownership.

## Scope control

The change does not alter spec purpose, review settlement, workflow order, lifecycle schema, adapter transformation, publication behavior, historical specs, or boundary semantics. It adds no second skeleton, persistent authorization subsystem, manual-proof contract, manual semantic-review gate, target runtime, or permanent size threshold.

## Risks and follow-ups

`SA1-governed` decreases by only 34 bytes because transaction semantics remain explicit; future edits should preserve behavior rather than chase a percentage. Total package bytes increase by 27 because the new conditional resource and marker are visible, while total words and both loaded profiles decrease. Final verify must recheck current branch state, the full approved command ledger, lifecycle coherence, and PR handoff eligibility. No product or architecture follow-up is currently required.

## Verify readiness

All implementation milestones and required reviews are closed, review resolution is closed, and the rationale reflects the final reviewed diff. The change is eligible for formal `verify`; branch and PR readiness remain unclaimed until that result is recorded.
