# Architecture Skill Simplification: Change Rationale

## Summary

The architecture skill now keeps assessment, routing, safety, and claims in a 772-word universal path while loading detailed architecture method and governed transaction procedure only when authoring needs them. This reduces all three procedural assemblies and the total package without changing the accepted architecture method, lifecycle ownership, or adapter behavior.

## Problem

The previous 1765-word `SKILL.md` mixed ordinary impact assessment with arc42/C4/ADR method, governed `change.yaml` mutation, multi-target recovery, and copied asset guidance. Every invocation paid that full context cost, policy ownership overlapped assets, and the combined authoring transaction was difficult to review independently.

## Decision trail

The accepted proposal selected one method reference, one governed-authoring reference, and the three existing assets. R1-R54 formalized universal ownership, three loaded assemblies, fail-closed signals, current assessment binding, prepared manifests, dependency-safe commit groups, exact retries, structural assets, honest measurement, and package parity. The bounded architecture assessment returned `architecture-not-required` because existing packaged-skill and authoring-evidence models support the change without a new schema or owner.

The plan split work into M1 preservation inventories, M2 canonical package implementation, and M3 measurement/parity proof. Independent reviews closed each milestone and then approved the complete branch diff.

## Diff rationale by area

| Area | Change | Reason | Contract and evidence |
| --- | --- | --- | --- |
| `skills/architecture/SKILL.md` | Replaced the monolithic procedure with universal evidence, classification, applicability, signals, stops, claims, resource triggers, and compact result guidance. | Assessment must remain self-sufficient and fail safe without conditional resources. | R1-R20; T1-T5; `evidence/m2-package-implementation.md` |
| `references/architecture-package-method.md` | Added one owner for arc42, C4, diagrams, ADRs, quality, placement, and package consistency. | Portable and governed authoring need the same detailed method, while assessment does not. | R3; T1, T8, T11 |
| `references/governed-architecture-authoring.md` | Added current assessment binding, exact target manifests, prepared evidence, dependency groups, commit points, settlement, retry, and recovery. | Governed mutation needs identity-bound crash safety without widening portable authority. | R4, R17-R42; T5-T10 |
| `assets/architecture-skeleton.md` | Replaced policy-bearing prose with neutral prompts while retaining arc42 headings, links, tables, and placeholders. | Assets own structure, not applicability or method policy. | R43-R45; T11 |
| `scripts/test-skill-validator.py` | Added focused architecture package tests and migrated legacy assertions to inspect the new policy owner. | Closed vocabularies, mappings, transaction properties, assets, and unknown values need deterministic proof. | R46-R48; T1-T11 |
| Change-local ledgers and fixtures | Recorded 20 rule owners, 20 literal treatments, three-asset dispositions, 18 scenarios, invalid values, and the baseline. | Semantic preservation and exact compatibility must be auditable before prose moves. | M1; `evidence/m1-preservation-inventories.md` |
| Measurement and package evidence | Recorded canonical hashes, assembly/asset/package totals, semantic reconciliation, boundary validation, and adapter parity. | Relocated content must be measured honestly and every distributed package must match canonical resources. | R49-R54; T12-T14 |

## Tests and validation before final verify

The focused `ArchitectureSkillSimplificationTests` cover the three assemblies, mapped resources, all closed vocabularies, invalid governed signals, assessment identity, prepared-before-write ordering, dependency groups, retries, lifecycle limits, structural assets, missing-resource stops, and claim boundaries. The ledger suite proves closed owners and classifications, unique identities, scenario coverage, and baseline surfaces.

The final implementation evidence records these passing commands: architecture skill validation; seven focused contract tests; the full 359-test skill suite with 16 expected skips; seven build-skill tests; generated-skill check mode; full boundary validation; and 150 adapter-distribution tests across generated, archived, release-candidate, and installed surfaces. Formal verify still owns the final current rerun and branch-readiness judgment.

## Review resolution summary

Nine material findings across proposal, test-spec, and implementation reviews are accepted and closed with no `needs-decision` disposition or open review-log finding. The implementation finding `ARSIM-M2-CR1` restored exact R21, R26-R27, and R38-R42 manifest and recovery properties after independent review found that concise prose had compressed them. See [review-resolution.md](review-resolution.md) and the approving M2 rereview.

## Alternatives rejected

Inline compression alone would not separate conditional context or ownership. A single catch-all reference would still couple method and lifecycle authority. More granular references would add navigation without independent activation boundaries. An executable router, transaction engine, new schema, tokenizer, target-agent acceptance run, or manual semantic gate would add machinery outside the problem.

## Scope control

The change does not redesign C4, arc42, ADR practice, architecture-review settlement, workflow routing, adapter formats, lifecycle schema, or historical architecture documents. It does not publish packages or open a PR.

## Risks and follow-ups

The main residual risk is future duplication between the universal file and references; the owner ledgers and focused tests make that visible. Total package size is not hidden: it decreases from 17893 to 15554 bytes, while `AA0`, `AA1`, and `AA2` decrease by 51.58%, 32.06%, and 1.72% in bytes respectively. No follow-up is required before verify.

## Verify readiness

All milestones, material resolutions, and final holistic code review are closed. The change is ready for formal `verify`; branch readiness and PR readiness are not yet claimed.
