# AR assessment browser pilot

## Purpose / big picture

Make the system Requirements view explain AR-046 implementation and verification using an explicitly selected operational account. Preserve uncertainty, criterion gaps and attribution in the same offline architecture browser.

## Current Handoff Summary

- Owning Change: `2026-10-04-system-requirements-view-design`; resume through `change context`.

Mutable progress and judgments remain in the owning operational Change.

## Source artifacts

The existing accepted requirement reuse covers IR-002, SR-008, SR-009, SR-085 and SR-086, FEAT-003/022 and SCN-008/084. FUNC-007/009/080/081 and MOD-004 retain their responsibilities. The owning [Requirements view contract](../../design/architecture/modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/requirement-tree.md#assessment-authority-and-presentation-data) defines selection, disclosure and applicability. AR-046 is the assessed obligation, not an implementation task. No independent prior-contract test specification is adopted.

## Context and orientation

The Python repository renderer assembles embedded data for the plain JavaScript offline reader. Add a small assessment validation module beside the existing projections; the reusable engineering model remains unchanged. Retain judgments through the existing Evidence attachment interface, select exact retained bytes, and disclose only the approved reading snapshot.

## Non-goals

No canonical requirement status changes, customer package qualification, database schema, automatic operational-store discovery, live status editing or external publication.

## Requirements covered

SR-008/009: preserve canonical relationships and explicit selected scope. SR-085: readable, attributable current and historical assessment details without satisfaction inference. SR-086: embedded offline data, with reproducible generated selection.

## Milestones

### M1. Select and interpret assessment data

After independent design and delivery review, implement strict versioned validation, explicit selection/replacement/clearing, deterministic companion generation and separate claim applicability. Prove rejection before publication, exact criterion coverage, duplicate and unsafe inputs, changed AR/material basis (including added, removed and reordered criteria with original criterion text retained) and unrelated edits. Existing empty-selection generation stays supported.

### M2. Present and exercise the pilot

Render separate states, actors, scope, identities, six criterion evidence/gap accounts and stale history on rows and both detail routes. Retain the actual independent assessment operationally and generate using its explicitly selected sanitized attachment. Prove empty, partial, failed, passed and stale presentations with synthetic evidence; synthetic cases do not become real AR judgments.

## Final review checkpoint

One independent whole-change Code Review covers the complete delivered browser refinement and interactions. Corrections require affected reassessment. A distinct scoped Verify establishes only this repository design-browser delivery, not complete AR-046 satisfaction or customer generator delivery.

## Change-level verification

### TG-FINAL-1. Attributable offline assessment reading

Demonstrate the real AR-046 account, default absence for other ARs, definition separation, criterion detail, no private path exposure or network dependency, and reproducible selection. Run existing browser/model checks and independent browser observations. Required proof includes invalid input rejection before output changes and historical labeling after basis changes.

## Validation plan

Use the focused architecture browser Python tests and Puppeteer checks, then `bash scripts/ci.sh --mode local` with the established pinned D2, Puppeteer and Chromium tools. Run prose/link checks and `git diff --check`. Keep actual commands/results in operational evidence.

## Risks and recovery

An underspecified assessment basis can mislead; independent review must inspect scope and selected subjects. A stale selection downgrades current indicators and retains history. Invalid selection fails before writes. Clear a selected account with `--clear-assessments` and regenerate to restore explicit absence. Preserve original operational evidence throughout.

## Dependencies

Independent preimplementation design/delivery review precedes M1. Final actual assessment identities follow the last material source edit. Source/test changes after assessment require explicit reassessment; generation never rebases claims silently.

## Material rationale

A frozen sanitized companion enables deterministic checks in other checkouts without granting the browser access to private operational records. Embedded data supports direct `index.html` reading. Implementation and verification remain separate supplied judgments.

## Readiness

See the owning Change for current review and execution standing.
