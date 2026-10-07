# Declare REM edition and KPS basis

## Purpose / big picture

Record the user's selected REM edition and exact KPS basis in one authoritative declaration, with clear limits on what the relationship establishes.

## Current Handoff Summary

Owning Change: `2026-10-07-rem-version-basis`; resume through `rigorloop change context`. Mutable progress, review and execution evidence remain in that local Change.

## Source artifacts

Reuse IR-006, SR-032, SR-033 and SR-056 with applicable Feature/Scenario guidance context. FUNC-032/033 remain responsible for finding and explaining guidance; MOD-008 owns [REM composition](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md). Existing allocation, Interfaces and assessment responsibilities are unchanged. Current accepted bases and review standing are recorded in the Change.

## Context and orientation

The tracked REM tree has no canonical method-version declaration. Nine incoming reference documents are untracked user material with their own imported metadata. Inspect these sources directly; no project-map reliance is needed. Preserve the imports byte-for-byte for the separately proposed reference consolidation.

## Non-goals

Reference-content consolidation, KPS conformance certification, changes to current REM rules, product package versioning, publication status, commit/push and PR updates are outside this bounded declaration.

## Requirements covered

SR-032 requires one identifiable metadata owner and direct navigation. SR-033 requires unambiguous based-on meaning. SR-056 requires consistent interpretation without conflating method edition, document identity, bibliographic dates and actual inspection evidence.

## Milestones

### M1. Declare and reconcile the basis

Prerequisites: independent requirement reuse, integrated design and delivery reviews.

Create `rem/metadata.md` with the exact user-selected REM and KPS versions in a YAML block. Use Markdown because the repository already classifies and validates REM Markdown; no new runtime schema, closed vocabulary validator or CI routing is needed. Do not invent a release status. The declaration owns version values; README links it and explains inheritance for maintained REM knowledge. Reconcile the improvement Practice's earlier no-KPS-release wording with the explicit based-on decision. The owning composition describes authority and the distinction from conformance. Preserve historical plans and original inspections.

Completion requires correct single-owner values, useful navigation, no contradictory current claim and unchanged engineering rules and imported reference inputs.

## Final review checkpoint

One independent whole-change Code Review follows complete implementation and required checks. Findings return to the author and are reassessed within the same gate. Distinct final Verify assesses current evidence and records completion; publication is separate.

## Change-level verification

A reader can identify the REM edition and its exact KPS basis, distinguish based-on from conformance and product release, and locate document-specific provenance without interpreting imported metadata as a competing declaration.

## Validation plan

- Parse the declaration's YAML block and compare its values with the user's explicit selection.
- Inspect README/composition/Practice consistency, changed local links and unchanged Model/Method owners.
- Compare all nine incoming reference fingerprints with the saved before-state; retain their current broken-link and imported-metadata issues for separate consolidation.
- Run `python3 scripts/project-operational-guidance.py --check` and `git diff --check`; this change selects no new packaged resource and no projected canonical content.
- Track only newly authored declaration/plan paths, then run `bash scripts/ci.sh --mode explicit --path PATH` for every delivered path using qualified Node and D2. Explicit selection preserves the untracked user imports outside this bounded assessment.
- No permanent test that merely mirrors the declared numbers is needed; independent semantic inspection and existing selected checks provide proportionate proof.

## Risks and recovery

A version can be mistaken for release approval or KPS certification. State the relationship precisely and preserve inspection provenance independently. Restore this bounded change from its recorded source baseline if needed, leaving user imports untouched. A later content consolidation must reconcile the imported metadata and links before adopting those files into maintained REM guidance.

## Dependencies

Requirement Review precedes design reliance, integrated Design Review precedes delivery reliance, and Delivery Review precedes implementation. Whole-change review and distinct final Verify precede completion.

## Readiness

See the owning Change for actual current status and evidence.
