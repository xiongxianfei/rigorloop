# Change-Record Catalog Registration and Bounded Read Model Rationale

## Status

- current

## Scope

This change implements the approved change-record catalog contract.

The work has two deliberately separated implementation workstreams:

- Workstream A registers deterministic change-local evidence classes and routes them through the changed-path selector.
- Workstream B adds bounded change-record query reads and stage-skill guidance that names those bounded reads.

The change does not alter workflow stage order, review status meanings, milestone state values, final readiness semantics, branch readiness, or PR readiness.

## Problem

Two recurring failures had the same root cause.

First, useful change-local evidence files could be written before the selector knew how to route them. That left deterministic evidence at risk of reaching verify with `manual-routing-required`.

Second, stage agents could read a whole `change.yaml` or a whole change record to answer narrow questions because there was no repository-owned bounded read path.

The durable invariant is:

```text
A change record is a queried catalog, not a transcript.
```

## Decision Trail

| Decision point | Decision | Source |
| --- | --- | --- |
| Proposal direction | Use one proposal with two separated workstreams. | `docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md` |
| Workstream sequence | Ship evidence registration and routing before query/helper skill guidance. | `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/proposal-review-r1.md`; active plan |
| Architecture boundary | Keep selector routing, query reads, validation, and stage skills as separate responsibilities. | `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md` |
| Registry placement | Keep the first registry table selector-owned. | `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md` |
| Query helper shape | Add `scripts/query-change-record.py` instead of adding query subcommands to metadata validation. | Spec CRM-R53; active plan M3 |
| Skill guidance timing | Update stage-skill guidance only after query-helper commands are stable. | Spec CRM-R47; active plan M4 |

## What Changed

### M1. Evidence Class Registry And Registered Routing

- Added selector-owned evidence class registration for recurring change-local evidence names and patterns.
- Registered evidence now routes to declared selected check IDs, the evidence file, the governing `change.yaml`, and the governing change root.
- Broad catch-all and ambiguous evidence patterns are rejected by selector regression tests.
- `behavior-preservation.md` records the route-preservation evidence for existing and new evidence classes.
- Code-review finding `CRM-M1-CR1` was accepted and resolved by adding the missing affected-root output for registered evidence.

### M2. Registration Debt And Actual Changed-Path Proof

- Added deterministic `unregistered-change-evidence` classification.
- Unregistered deterministic evidence now produces visible `manual-routing-required` registration debt instead of silently passing.
- Owner-approved deferrals require owner, path, reason, validation impact, and follow-up location.
- Complete deferrals can unblock verify readiness visibly without converting unregistered evidence into a registered route.
- Actual local changed-path selector proof is distinct from explicit-path lifecycle validation.
- Code-review finding `CRM-M2-CR1` was accepted and resolved by adding the complete owner-approved deferral contract and regression fixtures.

### M3. Bounded Change-Record Query Helper

- Added `scripts/query-change-record.py` with bounded `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>` reads.
- The helper is read-only, deterministic, and returns repo-relative paths.
- Query tests cover compact and legacy metadata, unknown stages, unsupported shapes, unsafe paths, no-validation cases, and read-only behavior.
- Compact `path_vars` artifact extraction uses an explicit artifact-key allowlist.
- Code-review finding `CRM-M3-CR1` was accepted and resolved so valid compact metadata with artifact paths in `path_vars` no longer returns a successful empty artifact inventory.

### M4. Stage-Skill Bounded Read Guidance

- Updated `proposal-review`, `code-review`, `verify`, `pr`, and `plan` skill guidance to name bounded change-record slices or query-helper commands.
- The skills keep active plan `Current Handoff Summary` as the live workflow-state owner.
- The skills preserve full `change.yaml` escalation for forensic reconstruction, unsupported shapes, disputed evidence, selector-routing investigation, migration checks, and whole-record review.
- Static skill tests now guard the bounded-read sections, helper command references, and full-read escalation terms.
- Generated skill and adapter proof was recorded using the current archive-based adapter validation path.

### M5. Lifecycle Evidence

- This file is the durable Markdown rationale for the change-local baseline pack.
- The active plan, plan index, and change metadata are synchronized after clean M5 re-review.
- Code-review finding `CRM-M5-CR1` was accepted and resolved by updating the governing final selected-CI proof from unsupported `bash scripts/ci.sh --mode selected` references to the repository-supported `bash scripts/ci.sh --mode local` command.
- Final `verify`, branch readiness, PR body readiness, and PR opening remain downstream lifecycle gates.

## Compatibility And Non-Goals Preserved

- Existing valid legacy and compact change records remain supported.
- Historical change records are not bulk-migrated.
- Changed-path selector safety is not weakened.
- Unregistered deterministic evidence does not silently pass.
- Query behavior does not execute validation commands.
- Validation selection, selected-check coverage, command exit behavior, and failure detection remain owned by the existing selector and CI scripts.
- `change.yaml` remains a metadata surface, not the live workflow-state owner.

## Review Resolution Summary

Review resolution is closed in `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`.

- Material findings resolved: 5.
- Unresolved findings: 0.
- Accepted and resolved findings: `CRM-SR1`, `CRM-M1-CR1`, `CRM-M2-CR1`, `CRM-M3-CR1`, and `CRM-M5-CR1`.
- M4 code-review and M5 re-review had no material findings.

## Validation Evidence

Detailed command evidence is recorded in the active plan and `change.yaml`.

Important proof surfaces include:

- selector regression tests for registered evidence, unregistered evidence, owner-approved deferrals, and selected-check routing;
- direct selector proof for registered evidence and unregistered evidence diagnostics;
- local changed-path selector and selected-CI proof for the branch;
- query-helper regression tests for bounded reads, compact and legacy metadata, stable diagnostics, unsafe paths, and read-only behavior;
- metadata validator regression for existing valid metadata fixtures;
- skill validator proof for bounded-read guidance and query-helper command references;
- canonical skill validation and generated skill checks;
- current archive-based adapter generation and adapter validation;
- final selected-CI proof through `bash scripts/ci.sh --mode local`, the supported branch-local wrapper mode;
- review artifact closeout validation with all material findings resolved;
- artifact lifecycle and change metadata validation for the active change.

Validation compatibility note:

- Current repository guidance for v0.1.3 and later treats public adapter skill bodies as release archives. M4, M5, and final verify therefore use temporary v0.1.5 archive generation plus `scripts/validate-adapters.py` as the supported adapter proof. This change does not alter adapter packaging semantics.

## Risks And Follow-Ups

- The selector-owned registry can be revisited as a shared registry file if a later slice finds that it reduces selector complexity.
- Automated scaffolding for registered evidence files remains a follow-on, not part of this implementation.
- Bulk migration of historical evidence filenames remains out of scope.
- Broader workflow-skill read-model conventions beyond change records remain a follow-on.
- The retired adapter-tree `--check` mismatch is kept out of this feature's final proof path because the repository's current public adapter contract is release-archive based.

## Current Handoff

Use the active plan `Current Handoff Summary` for live workflow state.

This rationale is scoped lifecycle evidence. It does not claim final verification, branch readiness, PR readiness, or lifecycle Done.
