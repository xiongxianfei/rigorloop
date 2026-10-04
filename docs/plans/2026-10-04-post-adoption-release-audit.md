# Post-adoption guidance and release audit input

## Purpose / big picture

Make the first follow-up after requirement-first adoption resumable through the current CLI and restore a dependable input for Release's existing literal-ownership checks.

## Current Handoff Summary

Owning Change: `2026-10-04-post-adoption-release-audit`. Read `rigorloop change context --root . --change 2026-10-04-post-adoption-release-audit` for current state, review standing and next action.
Mutable progress and results belong to that local handoff.

## Source artifacts

- Requirement basis: [IR-010](../../design/requirements/IR-010-obtain-trustworthy-compatible-rigorloop-tools/ir.json), its SR-068/SR-069 and reused SCN-065/FEAT-020. No new need or entity.
- Owning [Release design](../design/engineering/release/release.md), particularly REL-SR-06/07/19 and the literal-baseline representation.
- Existing FUNC-067/FUNC-068 and Release responsibility remain unchanged. The existing scripts source/candidate identity includes authored resources.
- Proof: [preflight cases](../design/engineering/release/test-design/cases/preflight.json) and [profile/input cases](../design/engineering/release/test-design/cases/profile-input.json).
- Prior-contract test specification: none required for this scoped realization correction; existing historical parser fixtures remain supported inputs.

## Context and orientation

The reader in `scripts/lib/release/release_transaction.py` currently skips audit admission when a historical Change-local file is absent. Use a required authored resource under `scripts/resources/release/`, keeping the existing v1 classification parser. `validation_selection.py` must select release regressions for changes to this resource alone. Shared private release fixtures must provide the required input.

## Non-goals

No publication, release approval, merge, new version decision, exhaustive literal scanner, historical-record migration or SQLite schema change. Existing completed Change meaning is preserved.

## Requirements covered

SR-068 and REL-SR-06/07/19 require cheap, honest input/ownership diagnostics. SR-069 requires bounded proof against the actual source/candidate. Current guidance must point at the supported operational interface and actual owning Change without duplicating lifecycle state.

## Milestones

### M1. Reconcile current inputs and guidance

Prerequisite: accepted requirement reuse, integrated Design Review and Delivery Review.
Update plan-index command syntax and adoption ownership; replace the PR template's Proposal field with the requirement/design basis. Add a newly authored scoped literal inventory from current source observations, not recovered history. Change preflight to require it without a retired-path fallback. Update actual fixture builders, existing unauthorized-literal cases, and resource-only validation selection together.

Completion: the current resource is consumed, missing/malformed input rejects, classification semantics remain protected, and relevant fixture trees remain unchanged by preflight. The old Change path is absent from runtime lookup and current normative guidance; an explicit negative fixture may mention it to prove non-fallback.

Required proof: start with the existing valid prepared fixture. Add focused missing/malformed/unreadable resource alternatives and legacy-only rejection; verify attribution and unchanged state. Exercise the actual checked-in resource through preflight. Retain existing changed-unauthorized CLI, unknown-classification and historical-rationale tests. Add resource-only selector proof and update the existing case catalog's realization after proof exists.

## Final review checkpoint

One independent whole-change Code Review follows the complete implementation and required checks; distinct final Verify follows applicable approval. Corrections receive proportionate reassessment in the same gate. There is no milestone approval gate.

## Change-level verification

The CLI handoff is consumed by an independent reviewer with no reliance on an activity transcript. Core evidence records actual source scope and limitations. Missing/invalid resource tests expose the prior silent skip; existing release tests preserve composed preparation, qualification and publication safeguards without real publication.

## Validation plan

- `python tests/engineering/release/test-release-transaction.py ReleasePreflightTests LiteralAuditBaselineTests`: focused consumer/classification checks.
- `python tests/engineering/validation/test-select-validation.py`: selection and routing regression coverage, including resource-only edits.
- `bash scripts/ci.sh --mode local`: required affected-surface validation; use qualified Node 24 on PATH and declared D2/browser dependencies if selected.
- Inspect actual source observations in the new inventory and CLI context references. Do not claim an exhaustive source audit or live publication.

## Risks and recovery

Requiring an input can break incomplete copied repositories; update all actual fixture/candidate consumers and prove the complete selected scope. Existing release scripts identity binds resource bytes. Reverting the reviewed commit restores repository behavior; no database migration or external rollback is involved. Original operational history and published artifacts are not rewritten.

## Dependencies

Requirement Review precedes design reliance, integrated Design Review precedes delivery reliance, and Delivery Review precedes implementation. Hosted post-merge CI remains separately observed; the pending release executor is outside this Change's authority.

## Material rationale

An audit resource used by current tooling belongs with authored release inputs. Its absence must be an actionable prerequisite failure. Existing IR/SR/Function/Scenario ownership and classification semantics are reused.

## Readiness

See the owning local Change through the CLI.
