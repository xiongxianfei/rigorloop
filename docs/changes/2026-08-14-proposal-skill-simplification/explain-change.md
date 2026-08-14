# Explain Change: Proposal Skill Simplification

## Summary

The proposal skill now keeps universal decision quality and safety in a shorter `SKILL.md`, loads governed mutation procedure only for an evidence-backed governed candidate, loads strategic and scope procedure only when one of four semantic predicates applies, and uses one skeleton for the universal proposal plus four conditional groups. This reduces every real loaded profile while preserving lifecycle authority, exact vocabulary, customer portability, and proposal-review handoff.

## Problem

Portable proposal authoring previously loaded detailed `change.yaml` mutation, standing-artifact, intent-table, and scope-budget procedure even when those concerns were absent. Repeated output shapes also lived partly in prose and partly in the skeleton. The change needed to reduce real loaded context without presenting relocated content as deletion or weakening proposal judgment.

## Decision trail

The accepted proposal selected two conditional references rather than inline-only compression, a catch-all reference, fragmented resources, or an executable engine. Requirements R1-R49 closed package ownership, four assemblies, portable/governed operations, identity-bound retry and reset, four specialized predicates, structural applicability, preservation, measurement, package parity, and a deterministic acceptance boundary. The architecture assessment found no new architecture because the design reuses the existing packaged-skill and stage-owned state models. M1 froze semantic/literal ownership and baseline evidence, M2 implemented and corrected the package, and M3 proved preservation and distribution parity.

## Diff rationale by area

| Area | Change | Reason | Source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/proposal/SKILL.md` | Retains universal evidence, decision, vision, scope, claims, triggers, and handoff in 1,092 words | Keep portable authoring self-sufficient while removing conditional procedure | R2-R4, R8-R15, R33-R40 | CMD2-CMD4; PA0 measurement |
| `references/governed-proposal-authoring.md` | Adds authority validation, create/revise transactions, retry, concurrency, and authorized stale reset | Give governed state procedure one conditional owner without granting authority from loading | R5, R9-R12, R16-R32 | Focused authority/retry/reset tests |
| `references/strategic-and-scope-gates.md` | Adds standing-artifact, vision-exception, intent, scope-budget, and follow-up procedure | Load exceptional strategic judgment only when one of four predicates applies | R6-R7, R33-R37 | Focused predicate/vocabulary tests |
| `assets/proposal-skeleton.md` | Adds four independently composable conditional groups | Make one asset own labels and layout without owning policy | R38-R40 | Focused group-composition tests and asset validation |
| `scripts/skill_validation.py` | Allows the two approved proposal references | Migrate the existing packaged-resource contract atomically | R1, R3, R48 | CMD2, CMD4-CMD8 |
| `scripts/test-skill-validator.py` | Adds six focused tests and points legacy assertions to current owners | Prove the new package while avoiding tests as accidental prose owners | R41-R44 | CMD3-CMD4 |
| Change-local ledgers and fixtures | Records 25 rules, 39 exact literals, 25 scenarios, and unknown-value fixtures | Separate semantic preservation from literal compatibility and fail closed | R41-R44 | CMD1 |
| Measurement and package evidence | Records four profiles, resource hashes, total package, and adapter parity | Prove real context reduction and disclose package growth honestly | R45-R49 | CMD5-CMD9 and M3 evidence |

## Tests added or changed

`ProposalSkillSimplificationTests` proves the exact package inventory and assemblies, portable versus governed authority, governed retry/reset boundaries, the closed specialized predicate and enum vocabularies, four structural groups, and non-overlapping reference ownership. Existing proposal scope, standing-artifact, lifecycle, portability, readability, and package tests now inspect the applicable owner rather than requiring every conditional rule inline. The test level is static contract validation because this refactor changes published procedure and package composition, not a target-agent runtime.

## Validation evidence available before final verify

CMD1 reports 25 rules, 39 literals, and 25 scenarios with unknown values rejected first. Proposal validation, six focused tests, the 342-test broad suite, seven generated-skill tests, generated drift checking, boundary validation, change metadata validation, and review artifact validation pass. Adapter distribution tests pass, and a fresh v0.4.0 build validates Codex, Claude, and opencode archives and clean installs for `proposal`. Final branch-wide CI remains owned by `verify`.

## Review resolution summary

Nine material findings across proposal and implementation review are accepted and closed; none remain open or `needs-decision`. M1 review split two composite compatibility rows into twelve exact values. M2 review required the combined profile to shrink in bytes as well as words. Both corrections received clean context-reset rereviews. See `review-resolution.md` and the final holistic review for durable details.

## Alternatives rejected

Inline-only compression could not isolate governed and strategic procedure. One catch-all reference would load unrelated concerns together. More fragments would add navigation without stronger authority boundaries. An executable routing engine would add runtime and architecture beyond the problem. Removing the skeleton or adding multiple output assets would either recreate structure ad hoc or fragment one document shape.

## Scope control

The change does not add a runtime, selector, state, schema, service, tokenizer, permanent simplicity gate, target-agent acceptance journey, or separate manual semantic-review stage. It does not change proposal-review settlement, workflow routing ownership, or generated adapter source-of-truth rules.

## Risks and follow-ups

The combined profile has the smallest margin, decreasing 510 bytes and 301 words, so future additions should preserve owner discipline rather than rely on a fixed percentage gate. Total package bytes increase by 478 because the skeleton now carries complete conditional structure; this is an explicit maintenance tradeoff, not hidden context. No follow-up is required before verify.

## Readiness

All implementation milestones, material finding resolutions, and the final holistic review are closed. The explanation is current for revision `f8450c8c`; the workflow may proceed to final `verify`. This artifact does not claim verification, branch readiness, or PR readiness.
