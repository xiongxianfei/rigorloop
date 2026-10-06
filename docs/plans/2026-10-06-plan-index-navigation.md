<!-- Template: plan-skeleton-v4 -->
<!-- Skill: plan -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/plan/SKILL.md -->

# Repair plan-index navigation

## Purpose / big picture

Make the plan index usable when an earlier record is unavailable, preserving the original reference without presenting it as a working file link.

## Current Handoff Summary

- Owning Change: `2026-10-06-plan-index-navigation`; resume through `rigorloop change context --root . --change 2026-10-06-plan-index-navigation`.

Mutable progress, review judgments and actual results belong to that Change.

## Source artifacts

- Requirement basis: IR-003 / SR-024, with FEAT-007 and SCN-025, limited to consumer reconciliation and truthful historical availability.
- Logical behavior: FUNC-024, limited to preservation of original meaning and explicit incomplete outcomes.
- Architecture: MOD-006, AR-075 and its [planning contract](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/planning.md), particularly PLAN-SR-03/07.
- Preservation policy: [Constitution](../../CONSTITUTION.md#repository-cleanup-and-historical-retention) and [ownership](../../design/support/ownership.md).
- Prior-contract test spec: none applies to this bounded correction.

## Context and orientation

[The plan index](../plan.md) owns navigation. Plan bodies keep their original intent; current Change records own mutable work. Historical file paths must not be retargeted to newer records. Inspect actual sources directly; no project-map currency claim is needed.

## Non-goals

No historical record reconstruction, storage migration, lifecycle-status inference, model/REM rule change, public validation framework, commit or publication.

## Requirements covered

SR-024 and PLAN-SR-03/07 are covered by M1's navigation and provenance checks. This does not establish complete retention-system or historical-work satisfaction.

## Milestones

### M1. Restore truthful index navigation

- Milestone kind: implementation.
- Engineering purpose: repair one navigation consumer under its existing owner.
- Requirements and architecture: the scoped sources above; accepted requirements/design and Delivery Review precede correction.
- Implementation scope: `docs/plan.md` and this plan's navigation entry. Preserve every existing live plan link, title, entry order, current Change identifier and pre-existing user edit.
- Method: inspect each missing historical target and available local Git history/current Change lookup. Use a verified original commit/path only if established; otherwise preserve the exact former repository-relative path in an explicit non-clickable unavailable-record note. Clarify its difference from a current Change reference.
- Required verification: rerun the exact private link-reproduction command; compare surviving links and all historical path occurrences; inspect the complete diff; run the repository's explicit checks for both changed files.
- Validation commands: `python .rigorloop/artifacts/plan-index-navigation/check-index.py`; `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-10-06-plan-index-navigation.md`; `git diff --check`.
- Expected observable result: no missing live index link, unchanged intended plan destinations, exact preserved former paths, bounded historical availability language and no unrelated source changes.
- Evidence expectations: actual before/after observations, identical reproduction-script identity, inspected source/provenance results and final subject identities, retained in the owning Change.
- Completion criteria: required checks and reading task support the scoped outcome; contradictions return to their owner before review.
- Whole-change review contribution: the complete two-file delivered delta, pre-existing work comparison, source searches, checks and participant observations.
- Optional commit boundary: none requested.
- Risks and recovery: follow the bounded preservation and restoration procedure below.

## Final review checkpoint

After complete correction and required proof, one independent whole-change Code Review assesses the delivered scope. Corrections are reassessed within that gate. A distinct final Verify then assesses completion; no milestone approval gate or publication follows automatically.

## Change-level verification

### TG-FINAL-1. Navigate a plan and interpret its record reference

A fresh agent reads the corrected index, locates the Historical-path compatibility retirement plan, explains its historical-record availability, and identifies the Selective REM integration plan's current Change and CLI inspection route. Require correct destinations, supported availability/status distinctions and source explanations. Prepare expectations before execution; retain actual response, source state and assistance. One agent reading result cannot establish human usability or all historical plans' correctness.

## Validation plan

M1 combines file reachability with semantic preservation inspection and the fresh reading task. The explicit repository selector supplies guide-boundary and current-record checks; it does not replace link or meaning checks. Keep the reproduction private to this correction; no permanent test is needed for fixed historical path literals. The task-local qualified Node runtime may be placed on PATH for existing record-validation commands without changing project configuration.

## Risks and recovery

An invented replacement would rewrite history; an unavailable note could be misread as completion. Preserve the exact old path, state the local availability limit and retain the index's navigation/status distinction. Recover this correction using the captured pre-edit index and this Change's exact delta; never reset or overwrite unrelated working changes. Remove the newly authored plan only if abandoning this Change and after reconciling its navigation reference.

## Dependencies

Use the existing local repository and supported record CLI. Remote history, external backups and historical record migration are outside the proof and correction scope. Missing historical content is explicitly unavailable rather than manufactured.

## Material rationale

This is a documentation consumer repair under existing MOD-006 ownership. Logical responsibility and Development placement are covered in prose; the reading task covers the relevant user situation. No Process or Physical behavior changes, and no new diagram adds necessary information.

## Readiness

See the owning Change for current state and assessed support.
