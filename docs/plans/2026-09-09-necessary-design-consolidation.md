# Necessary Design Consolidation Delivery Plan

## Purpose / big picture

Adopt the reviewed necessary-design contract and complete the selected source cleanup in one coherent documentation slice. Replace redundant validation descriptions with precise owner navigation, remove the selected ADR and diagram, and retain necessary operational source contracts and historical judgments.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-09-simplify-required-validation-and-design-retention/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing and closeout readiness live only in this record.

## Source artifacts

- Proposal: [merged direction](../proposals/2026-09-09-consolidate-necessary-design-and-retire-superseded-sources.md), reviewed by proposal-review-r2.
- Design: [Design](../design/design/design.md), [Test](../design/test/test.md) and [System](../design/system/system.md), including System's exact necessary-design consolidation map and candidate-owner boundaries.
- Scoped legacy amendments: [published-skill-first specification](../../specs/published-skill-first-repository-simplification.md) and [test specification](../../specs/published-skill-first-repository-simplification.test.md), selected new-profile-only amendments reviewed with the models.
- Architecture: [mixed architecture](../architecture/system/architecture.md); only the exact System-mapped sections and current navigation are changed.
- Prior-contract test spec: the linked retained test specification supplies historical/unmigrated intent; its old ledger, dual-run and measurement allocations do not override the exact approved Test amendment for this slice. No independent historical runtime suite is reactivated.
- Governing evidence: current Design rereview and candidate-spec-disposition-audit in the owning change. They establish this slice's boundaries, not approval of all legacy clauses.

## Context and orientation

The three models and two scoped amendments are authored before this plan. Implementation adopts their agreed source dispositions without modifying their reviewed engineering meaning. The two removal targets are redundant prose/diagram sources; no code, skill, schema, package input or candidate metadata edit is selected. There is one implementation milestone because splitting deletion from owner/navigation reconciliation would leave a misleading intermediate checkout.

The exact source diff is measured from commit `748ff69f`, the inspected audit baseline. That comparison isolates implementation and planning from already-authored Design. Final whole-change review additionally includes the complete branch contribution from its first proposal commit, using parent `ca440d8e^` as the complete proposal/design/delivery/implementation comparison basis. Historical records and earlier reviewer identities remain attributable.

## Non-goals

No whole-spec deletion, new model file, public skill change, validation runner or check retirement, CI interface rename, package regeneration without an affected input, archive purge, installation, release or publication. No automatic creation of snapshots or redirects. FU-013/014 and remaining skill adoption stay separate work.

## Requirements covered

| Governing obligations | Allocation |
| --- | --- |
| DES-SR-13/18/21: complete meaning, consumer alignment and necessary-source retention | M1/TG-01–02; TG-FINAL-01 |
| TEST-SR-08/10/12/14: protected boundaries, actual consumer impact and proportionate allocation | M1/TG-02–03; TG-FINAL-01 |
| SYS-SR-02/04/06/07/08/09: precise composition, current/historical distinction, bounded follow-ups and recoverability | M1/TG-01–03; TG-FINAL-01 |
| DES Identity/authority and Compatibility/migration; Test Input domain, Composition/path, Temporal/retry and Compatibility/migration; System Composition/path, Compatibility/migration and Failure/recovery | M1 evidence contrasts removed duplication, retained mixed obligations, unchanged operational inputs and an owned stop for any newly discovered necessary reader. Existing runtime/installer scenarios are unaffected, not rerun as documentation proof. |
| RC-SR-15 and final-closeout policy | Evidence reuse has affirmative unchanged-basis support; final fresh whole-change Code Review precedes distinct Verify. |

## Milestones

### M1. Adopt owner navigation and retire selected duplicate sources

- Milestone kind: implementation.
- Engineering purpose: perform source removal and necessary consumer reconciliation together so the current checkout has complete owners and no broken required reader.
- Requirements: DES-SR-13/18/21; TEST-SR-08/10/12/14; SYS-SR-02/04/06/07/08/09.
- Architecture responsibility: System's necessary-design consolidation and consumer maps; DES-DEC-06, TEST-DEC-06 and SYS-DEC-04.
- Dependencies: current approved Design package and Delivery Review; no outstanding required findings; original subjects available for before/after inspection.
- Implementation scope: delete `docs/adr/ADR-20260810-published-skill-first-validation-architecture.md` and `docs/architecture/system/diagrams/component-published-skill-validation.mmd`; remove the complete architecture subsections “Level 2 White-Box: Published-Skill Validation”, “Published-skill product-gate and retirement flow” and “Published-skill-first validation boundary”; reconcile the four current ADR/diagram navigation locations identified below. Route updates only FU-012's receiving direction and remaining responsibility. Preserve other sections, specs, diagrams, old plans/reviews and operational fixtures.
- Files/components likely touched: the two removal targets, `docs/architecture/system/architecture.md`, `docs/follow-ups.md`, `docs/plan.md`, this plan and stage-owned records. Already-reviewed models/spec amendments remain unchanged unless a discovered gap returns to Design.
- Required verification: TG-01 complete meaning and historical distinction; TG-02 actual current references/readers; TG-03 unchanged operational/package boundary.
- Evidence expectations: an exact before/after source disposition, original/replacement owner references, preserved historical citation and section comparison, concrete inspected dependency disposition, actual commands/results and limitations.
- Implementation steps: inspect the original ADR, diagram and exact selected subsections; confirm their mapped destination clauses and rationale; apply the named removals; replace the ADR and diagram entries in the architecture source list with local-owner navigation, replace the inline diagram reference in Validation and Generation Scripts, and remove the redundant validation ADR Architecture Decisions summary. Keep the historical follow-on ADR sentence about its original proposal unchanged. Route reconciles FU-012 to distinguish completed Skill adoption, this bounded cleanup and remaining execution work without mandating a new Validation model.
- Validation commands: all commands in the Validation plan below, scoped to this milestone's changed subjects and source/reference boundary.
- Expected observable result: the two redundant sources and three duplicate subsections are absent; necessary content remains at explicit current owners or retained operational sources; current navigation resolves; historical judgments have not been retargeted.
- Completion criteria: TG-01–03 have assessed evidence, the removal selection is fully implemented, no required consumer is left broken, and remaining work stays explicitly owned.
- Required evidence: registered M1 implementation evidence and independent milestone Code Review; any findings recorded before correction.
- Review handoff: complete M1 diff and relevant owner/source mappings, preserved negative/failure meaning and unaffected package evidence.
- Optional commit boundary: `M1: Retire redundant validation sources with coherent owner navigation`.
- Risks: an incidental-looking source has an actual reader, or a removed paragraph contains unique meaning. Stop that removal, retain the source and return the gap to Design; do not invent equivalence or expand scope.
- Rollback/recovery: restore only the affected source/navigation slice from the pre-M1 commit if needed; assess the restored subjects and preserve intervening user changes. No state migration or historic approval rewrite is part of recovery.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1 and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered branch contribution, including proposal, Design, Delivery and implementation interactions. A milestone review alone is insufficient.
- Evidence: exact final subjects, independent reviewer basis, judgment and concern dispositions.
- Successor: distinct final Verify; corrections return to their owner and require affected reassessment.

This checkpoint applies even though the change is documentation-only. No verification-group non-applicability rationale waives it.

## Change-level verification

### TG-FINAL-01. Coherent necessary-design adoption

- Covers: all allocated obligations, M1, final current/historical owner distinction and complete source-retention decision.
- Demonstrate: a reader follows System to the actual local contracts; the removed ADR/diagram need not be reconstructed from history; mixed specs retain precise surviving populations; candidate owners remain provisional; publication and model creation are not inferred. Required historical records retain original identities and current approval concerns remain visible.
- Evidence expectations: independent final diff/meaning assessment plus current structural/reference and record checks. Applicable M1 checks may be reused only when their subjects/dependencies/configuration/environment remain unchanged under RC-SR-15; final whole-change review itself is fresh.
- Non-applicability: runtime, package and release execution are not required when TG-03 establishes their inputs and consumers are unaffected. A newly discovered effect changes that disposition and requires its directly protective checks before closeout.

## Validation plan

1. `python scripts/validate-boundary-first.py --path docs/design/design/design.md --path docs/design/test/test.md --path docs/design/system/system.md --path specs/published-skill-first-repository-simplification.md --path specs/published-skill-first-repository-simplification.test.md` — current reviewed model/legacy structure.
2. `python scripts/validate-documentation-prose.py --mode enforce --path docs/design/design/design.md --path docs/design/test/test.md --path docs/design/system/system.md --path docs/plans/2026-09-09-necessary-design-consolidation.md --path docs/plan.md --path docs/follow-ups.md` — current authored prose. For the mixed architecture and legacy sources, use the same validator in `--mode audit`, inspect new/changed paragraphs and compare any findings with the unchanged baseline; pre-existing header/comment findings are not claimed passing or fixed by unrelated edits.
3. `python scripts/validate-markdown-readability.py docs/plans/2026-09-09-necessary-design-consolidation.md docs/architecture/system/architecture.md docs/follow-ups.md` — readability, with non-blocking advisories reported honestly.
4. `node scripts/validate-record-store.mjs docs/changes/2026-09-09-simplify-required-validation-and-design-retention/change.json` and `git diff --check` — recorded structure/references and whitespace.
5. `git diff --name-status 748ff69f` and `git diff 748ff69f -- skills scripts packages dist schemas templates` — inspect exact scope and require the operational comparison to be empty for TG-03. Inspect `packages/rigorloop/package.json` shipped paths and adapter source/resource inputs; search the deleted filenames with `rg -n -F` across scripts, packages, skills, specs and docs. Classify every surviving reference as current owner mapping, a reconciled actual reader or historical citation. A search's no-match exit is an observation, not a failed proof command.
6. TG-01 manual semantic proof: implementer and independent reviewer read the original selected text and receiving clauses/rationale; record where each necessary decision or obligation survives, why the removed presentation adds no unique requirement, and which untouched architecture sections/history remain byte-identical. Syntax or keyword presence alone cannot establish meaning. This evidence expires if selected text, replacement meaning or a relied-on consumer changes.
7. TG-02 reference proof: check new Markdown destinations and exact heading boundaries; inspect the original historical ADR follow-on sentence and preserve it. Demonstrate the failure contrast by inspecting a known missing/retired target and rejecting its use as a current owner; no new permanent validator or test harness is needed.
8. TG-03 candidate metadata: inspect whether changed sources enter the adapter/candidate build inputs and whether current metadata or dependent assertions describe changed archives. With no affected inputs and unchanged metadata, record an inspected unaffected disposition. If a required correction changes package bytes, return for the necessary allocation, regenerate through the existing owning builder and run directly dependent checks. Never invent hashes, rewrite release history or introduce publication work.

No new tests are written for prose-only removal. No useful test is deleted or demoted; existing scoped record writes retain their normal runtime safety checks.

## Risks and recovery

Historical citations intentionally outlive their source file without becoming current authority. A missing historical original must not be reused as current evidence; this change's independent review establishes the new contract. An actual required reader blocks deletion until resolved. Recovery restores the source and directly related references together; restoring a file does not renew an old judgment.

## Dependencies

Reviewed Design and Delivery precede M1. Existing Skill, Test, Review and Closeout, CLI/Record Format, Distribution/Installation/Release legacy sources and operational ledger fixtures remain dependencies. Current source-only scope makes no claim that their entire baseline implementation is correct. Broader consolidation remains separately owned.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-09 | One source/consumer milestone, followed by separate final review and Verify | The edits are one bounded recoverable composition change | Separate deletion/navigation milestones would expose a broken intermediate source set |
| 2026-09-09 | Focused source/reference checks with affirmative package unaffected evidence | No behavior-bearing input is selected; semantic preservation is the main claim | Blanket package/runtime reruns, a new validator or a deletion-count target |

## Readiness

See the owning change record for current workflow state. Design and Delivery approval, implementation evidence, milestone review, fresh final whole-change Code Review and distinct Verify remain the relevant completion gates; this plan is not a completion claim.
