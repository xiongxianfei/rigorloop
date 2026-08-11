# Code-Review Skill Simplification Explain Change

## Summary

This change makes the published `code-review` skill materially smaller on the ordinary review path while preserving its review, recording, status, stop, claim-boundary, milestone, and handoff contract.
Universal policy remains in `SKILL.md`.
Workflow-managed automation procedure now lives in one explicitly mapped conditional reference.
The existing assets remain the sole owners of repeated output structure.

The final implementation reduces `SKILL.md` from 4,514 to 2,650 words and from 8,160 to 4,818 estimated tokens.
That is a 41.3 percent word reduction and a 41.0 percent estimated-token reduction.
The complete package also becomes smaller, from 5,569 to 4,591 words and from 10,116 to 8,523 estimated tokens.
All seven identified duplication clusters have one owner, and the skill has no inline output-template duplication.

## Problem

The prior skill mixed universal review rules with repeated guidance, inline output structures, shared boundary detail, and workflow-managed automation procedure.
A direct review therefore loaded and navigated content that applied only to an armed automated correction loop.
Simply deleting prose or enforcing a size percentage would risk weakening the public review contract.

## Decision trail

- Proposal option O3 was selected: consolidate the core and progressively disclose conditional policy.
- Proposal review required the conditional-reference ownership model, runtime-free acceptance, and rule-ownership success criteria instead of a hard percentage gate.
- Requirements `R1` through `R25` define package ownership, inline universal rules, conditional loading, deterministic packaging, fail-closed fixtures, measurements, compatibility, and non-runtime proof.
- The canonical architecture defines a published skill as its `SKILL.md` plus explicitly mapped references and assets, while lifecycle and policy ownership remain at the skill level.
- M1 froze rule ownership and acceptance fixtures.
- M2 performed the package refactor and focused validator changes.
- M3 proved package parity, semantic preservation, compatibility, and measured reduction.
- Verify R1 found architecture ownership and selector-routing blockers.
- Architecture revision R2 transferred the canonical architecture pointer to this change, and architecture-review R3 approved the correction.
- CI maintenance reused the existing owner-deferral contract for nested deterministic evidence and restored the existing “selected checks” semantic in the simplified skill.
- The first fresh PR-mode verify run exposed a case-sensitive shared review-resolution vocabulary regression; the skill now preserves the lowercase `required outcome` and `safe resolution` literals without changing their meaning.
- Final holistic code-review R3 approved the complete corrected diff with no material findings.

## Diff rationale by area

| Area | Change | Reason | Source and proof |
| --- | --- | --- | --- |
| `skills/code-review/SKILL.md` | Reorganized the common path around purpose, authority, stops, review sequence, finding/status rules, recording, claims, handoff, and resource loading; removed repeated templates and conditional automation detail. | Keeps every direct or isolated review self-sufficient while eliminating common-path repetition. | `R1`-`R8`, `R10`, `R17`, `R19`; T2-T6, T8, T12; M2 and MP1. |
| `skills/code-review/SKILL.md` validation sentence | Names “selected checks and validation evidence.” | Restores the existing validation-layering contract exposed by the full selector regression suite. | `test_workflow_guidance_aligns_with_validation_layering_contract`; refreshed CMD10 and CMD11. |
| `skills/code-review/SKILL.md` finding sentence | Preserves lowercase `evidence`, `required outcome`, and `safe resolution path` literals. | Maintains the shared review-resolution vocabulary contract while retaining the same finding fields and semantics. | `test_review_stage_skills_align_with_review_resolution_contract`; final holistic code-review R3. |
| `skills/code-review/references/workflow-managed-automated-review.md` | Added the single conditional procedure for formally armed workflow-managed automated review or correction loops. | Automation phases and correction-loop procedure do not need to load for ordinary reviews. | `R5`-`R7`, `R23`-`R25`; T3-T5, T13-T14; CMD3 and CMD6. |
| Existing `skills/code-review/assets/` | Retained the mapped review-result and finding assets as the only repeated output structures. | Prevents inline and asset templates from drifting while leaving policy in `SKILL.md`. | `R4`, `R7`, `R11`, `R21`-`R22`; T4, T6-T8. |
| `scripts/skill_validation.py` | Added a narrow allowlist for the exact workflow-managed automation reference mapping. | Extends the existing mapped-resource owner instead of creating a validator family. | `R4`, `R8`-`R10`, `R15`-`R16`; CMD2 and CMD3. |
| `scripts/test-skill-validator.py` | Added focused package tests for ownership, the exact load trigger, resources, assets, vocabulary, and forbidden runtime machinery. | Proves the structural contract without executing a model runtime. | T2-T6, T8-T10, T13-T14; 290 tests with 16 governed skips. |
| Rule ledger and fixtures | Added 22 stable rule dispositions, seven static scenarios, and one invalid disposition fixture. | Ensures no significant rule silently disappears and unknown dispositions fail closed. | `R2`, `R9`, `R13`, `R15`-`R16`, `R18`, `R20`; T1, T9-T10; CMD1. |
| `docs/architecture/system/architecture.md` | Transfers the stable owning-change pointer to this change. | The change that modifies the canonical architecture owns its current revision. | Verify blocker `VR-CRSIM-001`; architecture-review R3; lifecycle validation. |
| `scripts/validation_selection.py` | Applies the existing complete owner-deferral mechanism to nested `change-local-unsupported` evidence. | Allows exact one-change fixtures to remain visibly deferred without silent routing or a broad registry entry. | CRM-R17 through CRM-R19; selector regression; verify blocker `VR-CRSIM-002`. |
| `scripts/test-select-validation.py` | Adds red-then-green nested complete-deferral coverage and preserves existing immediate, missing, incomplete, and mismatched cases. | Proves nested evidence remains blocking unless all required deferral fields are present and match the exact path. | 153 selector tests. |
| Change metadata and CI evidence | Records three exact repository-maintainer deferrals with owner, path, reason, validation impact, and follow-up. | Keeps registration debt visible while preserving mandatory CMD1 and CMD11 proof. | Explicit selector result: no blockers and three `owner-deferred` records. |
| Measurement and semantic evidence | Records baseline/final common-path and package metrics plus independent semantic review. | Separates context reduction from maintenance footprint and makes semantic preservation primary. | `R12`-`R14`, `R17`; T11-T12; CMD10, CMD11, MP1. |

## Tests added or changed

- Focused skill-validator tests prove direct-review sufficiency, exact conditional loading, universal-policy placement, asset ownership, vocabulary preservation, mapped-resource integrity, and absence of target-runtime acceptance machinery.
- CMD1 proves the seven scenarios and verifies that an unknown ledger disposition fails closed.
- Adapter-distribution tests and trusted `v0.3.6` temporary archives prove the canonical skill, conditional reference, and assets across Codex, Claude, and opencode packages and clean temporary installations.
- MP1 checks trigger clarity, ownership, prerequisites, operating sequence, evidence, stops, claim boundaries, outputs, handoff, and the conditional load trigger.
- The selector regression proves that a complete deferral can unblock exact nested evidence while missing, incomplete, or mismatched deferrals remain blocking.
- The review-artifact regression proves that review-stage skills preserve the shared finding and resolution vocabulary.
- No test executes a target agent.

## Validation evidence available before final verify

- CMD1 passed with 22 ledger rules, seven scenarios, and the unknown disposition rejected.
- `python scripts/validate-skills.py skills/code-review/SKILL.md` passed.
- `python scripts/test-skill-validator.py` passed 290 tests with 16 governed skips.
- `python scripts/build-skills.py --check` passed against a temporary generated tree.
- `python scripts/test-adapter-distribution.py` passed.
- Corrected CMD6 validated trusted `v0.3.6` Codex, Claude, and opencode archives and clean installations for `code-review`.
- Boundary-first validation passed for the feature spec and test spec.
- CMD10 and CMD11 produced the refreshed common-path and total-package metrics.
- `python scripts/test-select-validation.py` passed 153 tests.
- Explicit selection of the ledger and fixtures returned no blockers and three visible complete owner deferrals.
- PR-mode selection through reviewed commit `76b94468` returned 13 selected checks, no blockers, three owner-deferred records, and no broad-smoke requirement.
- The first full PR-mode execution after R2 found the lowercase review-resolution vocabulary regression; the focused 103-test review-artifact suite passed after the capitalization-only correction.
- Explicit lifecycle validation passed after the architecture ownership transfer.
- Review-artifact structure validation passed with 18 reviews and nine resolved findings.
- Final verification has not yet been claimed.

## Review resolution summary

Earlier authoring reviews produced nine material findings, and every finding has a final disposition in `review-resolution.md`.
No finding remains open or `needs-decision`.
Implementation reviews M1, M2, M3, final R1, architecture-review R3, and final holistic code-review R2 introduced no new material finding.

## Alternatives rejected

- Keeping the skill unchanged would preserve unnecessary common-path loading.
- Deduplicating only inside `SKILL.md` would leave automation-only procedure on every direct review path.
- Replacing the skill with a generic checklist would remove lifecycle rigor and repository-specific claim boundaries.
- A normative 35-45 percent reduction gate would put numeric optimization ahead of semantic preservation.
- A dedicated simplicity validator or change-specific selector registry entry would create unnecessary permanent infrastructure.
- A broad nested-fixture route would risk silently validating unrelated evidence with the wrong check.
- A second change-local architecture source would duplicate canonical design truth.
- Prompt journeys, transcript grading, and target-agent execution are not acceptance proof.

## Scope control

- Review status, severity, formal recording, isolation, milestone settlement, rereview, and downstream authority semantics are unchanged.
- The change creates no new lifecycle owner, validator family, runtime, selector, scheduler, persistent state, external dependency, or model-behavior test system.
- Existing boundary-first guidance and structural assets retain their established owners.
- Generated adapter archives remain derived output, and canonical authorship stays under `skills/`.
- Owner deferrals apply only to the three exact one-change evidence paths and do not create a generic bypass.

## Risks and follow-ups

- Future drift between universal and conditional policy is constrained by exact mapping, package tests, the rule ledger, and generated-package parity.
- Token estimates remain approximate change evidence rather than a permanent gate.
- The three selector deferrals remain visible registration debt by design and cannot match other paths.
- CMD6 uses immutable trusted fixture `v0.3.6` after the synthetic-version proof failure was corrected and rereviewed.
- PR preparation remains a separate downstream stage outside this workflow target.

## Readiness

All implementation milestones, architecture correction, CI-maintenance correction, and final holistic code review are closed.
This explanation is current for reviewed commit `05e6fd53` and is ready for final `verify`.
It does not claim branch or PR readiness before that stage runs.
