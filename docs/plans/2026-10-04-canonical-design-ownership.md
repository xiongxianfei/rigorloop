# Canonical engineering definition ownership

## Purpose / big picture

Remove `docs/design/` after reconciling its surviving meaning into the current REM owners. A reader starts at `design/`, follows stable requirements and accountable Modules, and can reach detailed rules and coverage without a second architectural hierarchy.

## Current Handoff Summary

- Owning Change: `2026-10-04-consolidate-engineering-design`; resume with `rigorloop change context`.

Mutable progress, review judgments, exact migration disposition and execution evidence belong to the CLI-managed operational handoff. This plan carries stable execution intent.

## Source artifacts

- Requirement basis: existing SR-001/003/004/005/008/013/014/015/032 and their parent IRs; no new stakeholder obligation or entity is introduced by relocation.
- Logical behavior and architecture: existing Function allocations and MOD-006–015 responsibilities; architecture composition retains system-wide policy, and repository development/validation remains supporting engineering practice.
- Detailed ownership: [Engineering definition ownership](../../design/support/ownership.md).
- Source baseline: `85a1b9ba7cd1a43ad9e72b924edd88a68fe15872`, original `docs/design/` tree. The operational disposition inventories all 104 original files with identities, clause references and destinations.

## Context and orientation

Detailed Markdown rules and coverage remain useful; their ownership and active consumers must agree with the REM model. Preserve both numbered and unnumbered behavior, formats, failure cases, rationale, useful examples and protective tests. The explicit contract registry supports these subordinate documents; it does not declare a second Module model. Historical synthetic v3 fixture bytes and operational judgments keep their original meaning.

## Non-goals

No new CLI behavior, storage format, stakeholder need, Module decomposition, bulk draft-status promotion, historical review reinterpretation, release publication or merge. Customer portable document validation remains supported.

## Requirements covered

| Basis | Delivery and proof |
| --- | --- |
| SR-001/003/005 | Transfer retained detail and rationale with stable entity and clause identities; compare original inventory and removed sections. |
| SR-004/008/032 | Reconcile current entry guidance, relationships, skill resources, generated browser and owner navigation; inspect current readers. |
| SR-013/014 | Update registry, selection and native validation consumers; preserve malformed-contract and unknown-value protection; conformance remains distinct from approval. |
| SR-015 | Explicit source disposition, recoverable history and byte-identical historical judgments/fixtures; no silent adoption. |

## Milestones

### M1. Reconcile owners and canonical detail

Transfer all surviving contracts to their assigned current owners. Replace the former System/Skill/CLI/Engineering architecture hierarchy with current composition and supporting contracts. Retain useful coverage catalogs, clause identities and rationale. Resolve duplicate statements against current canonical owners without silently changing behavior. Inspect removed sections and record their preservation or retirement rationale in the operational disposition. Update root authority and model navigation. Completion requires all 104 original sources dispositioned, including non-numbered obligations, not just moved.

### M2. Reconcile consumers and remove retired paths

Update exact contract registrations, selected coverage paths, example readers, active provenance, relative links, validation selection and fixture factories. Historical JSON fixtures move unchanged; their synthetic old paths remain historical data. Current operational history is not rewritten. Reconcile generated browser and other generated resources using their existing generators. Remove every file beneath `docs/design/` and remove obsolete repository assumptions in consumers in the same change. No redirects, compatibility copies or dual authority.

### M3. Prove the complete composition

Run focused boundary/selection/resource and model checks, then the applicable local CI selection. Inspect current ownership, rendered views and resolved links; compare retained source clauses and exact fixture bytes. Resolve actual failures and repeat only affected checks. Meaningful native regressions should exercise relocated contract admission and selection, and rejection of malformed declared contracts; do not add a permanent historical migration report test.

Milestones are implementation/check checkpoints, without mandatory reviews between them. Dependencies run M1 → M2 → M3; active ownership gaps block the affected transfer.

## Final review checkpoint

One independent whole-change Code Review assesses complete source transfer, current consumers, historical preservation and proof. Corrections receive proportionate independent reassessment within that gate. Distinct final Verify follows applicable approval and evidence. Only then commit/push and submit the authorized PR; no merge or release is included.

## Change-level verification

Inspect the original 104-file population against current owners, section dispositions, all active readers and generated outputs. Current meaning must be readable without fetching Git history or the local database. Retained obsolete-version examples must be clearly bounded, not presented as current runtime support. A still-used old path or a missing obligation blocks completion even if structural tests pass.

## Validation plan

Use the qualified Node runtime selected by the project and the available D2/browser dependencies for generated views.

- `python scripts/validate-boundary-first.py --check`: exact supporting-contract structures and coverage.
- `python tests/engineering/validation/test-boundary-first-validation.py`: current contract and negative-boundary protection.
- `python tests/engineering/validation/test-select-validation.py`: changed-path admission, dependency selection and isolated fixture consumers.
- `python scripts/render-rem-architecture-browser.py` and `python scripts/render-rem-architecture-browser.py --check`: resolve changed source paths and regenerate deterministic browser projections.
- `bash scripts/ci.sh --mode local`: complete applicable selected checks; retain actual results, failures and limits in operational evidence.
- `git diff --check`, current-link inspection, exact historical fixture-byte comparison and original source/section disposition review: migration-specific proof that runtime tests alone cannot provide.

## Risks and recovery

A naive replacement can alter historical identities or break relative links. Resolve links using their original source location; preserve original historical JSON and operational records. A path move can bypass CI selection; exercise actual selector consumers and malformed current contracts. Broad relocation can conceal omitted semantics; compare original clauses and section-owned guarantees independently. Generated views may refer to moved locators; regenerate and inspect them.

The migration is reversible in Git before external handoff. Preserve the original base and avoid irreversible data operations. On an unresolved ownership or proof gap, stop the affected removal and correct its design; do not preserve a competing active copy merely to bypass a check.

## Dependencies and readiness

The migration is based on PR #205 while that PR remains open; submit a stacked PR against its branch unless it has merged. Requirement, integrated Design and Delivery reviews establish the respective bases before reliance. Current stage and readiness remain in the owning Change, not this plan.
