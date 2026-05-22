# Explain Change - Compact Change Validation Metadata

Date: 2026-05-22
Change ID: `2026-05-21-compact-change-validation-metadata`
Status: recorded before final verify

## Summary

This change adds compact `schema_version: 2` validation metadata support to `validate-change-metadata.py` while keeping legacy change metadata valid. Compact metadata stores path variables, validation bundles, stage events, structured counts, derived summaries, and optional transcript references instead of repeating long command paths and prose result strings in every validation entry.

The implementation keeps the core audit invariant intact: compact storage is allowed only when reviewers can still reconstruct what validation bundles ran, which paths were checked at each stage, what the result was, what counts were observed, and whether blockers remain.

## Problem

The accepted proposal identified that durable `change.yaml` validation evidence had become transcript-like: repeated long change IDs, repeated validation commands, growing lifecycle path lists, and prose-encoded pass strings made common review expensive. The goal was not to hide evidence, but to make the common read cheaper while preserving reconstructable proof.

Because `validate-change-metadata.py` owns the metadata contract, the fix had to be a schema and validator update rather than a one-off edit to a single `change.yaml`.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Choose compact validation bundles and structured stage results, with optional transcript splitting as a controlled extension. |
| Proposal | Use explicit `schema_version: 2` so the dual-read validator can branch deterministically instead of guessing by field presence. |
| Proposal | Reject mixed legacy and compact validation evidence within one file, while allowing legacy and compact files to coexist across the repository. |
| Spec | Preserve legacy compatibility, require compact `path_vars`, `validation_bundles`, `validation_events`, and `validation_summary`, and keep validation command selection unchanged. |
| Spec | Use dated `change_id` for event artifacts and derived undated `slug` for durable specs and test specs. |
| Spec | Treat `validation_summary` as checked derived data rather than independent truth. |
| Plan | Split implementation into M1 shape compatibility, M2 path/lifecycle safety, and M3 evidence consistency and compactness proof. |
| Architecture | No separate architecture artifact was required; the approved plan scoped the work to the existing validator, fixtures, and tests. |

## Diff Rationale By Area

| Area | Files | Change | Reason | Source/Test Evidence |
| --- | --- | --- | --- | --- |
| Proposal and spec contract | `docs/proposals/2026-05-21-compact-change-validation-metadata.md`, `specs/compact-change-validation-metadata.md` | Recorded the compact metadata contract, migration rules, path-variable model, bundle/event model, summary derivation, and non-goals. | Establish the behavior before coding validator semantics. | Proposal acceptance criteria and spec R1-R83 / AC1-AC27. |
| Test contract | `specs/compact-change-validation-metadata.test.md` | Mapped requirements to fixture, helper, manual, and smoke tests. | Keep implementation test-driven and traceable across compatibility, safety, reconstruction, counts, compactness, and no-execution behavior. | TCVM-001 through TCVM-024. |
| Plan and lifecycle state | `docs/plans/2026-05-21-compact-change-validation-metadata.md`, `docs/plan.md`, change-local review files | Sequenced M1, M2, M3, recorded review outcomes, review-resolution, and current handoff state. | Keep workflow state durable and milestone-aware. | Plan-review R1, code-review M1 R1, M2 R2, M3 R2. |
| Validator compact branch | `scripts/validate-change-metadata.py` | Added explicit compact detection through `schema_version: 2` and a compact semantic validation path separate from legacy schema validation. | Support dual-read migration without invalidating existing metadata. | R1-R7, TCVM-001 through TCVM-003. |
| Path variables and artifact existence | `scripts/validate-change-metadata.py` | Added `change_id`/`slug` derivation, closed `{var}` interpolation, doubled-brace escaping, recursive/unresolved variable rejection, canonical spec/test-spec paths, path safety, lifecycle-stage ordering, and first-exists filesystem checks. | Prevent compact metadata from hiding bad paths, machine-local values, dated durable contracts, or missing stage-required artifacts. | R8-R24, R63-R75, R83, TCVM-006 through TCVM-011. |
| Bundle command safety | `scripts/validate-change-metadata.py` | Added lexical safety validation for compact bundle command strings without executing them. | Close `CVM-M2-CR1`, which found unsafe bundle commands could contain local paths, credential URLs, or secret-like values. | Review-resolution `CVM-M2-CR1`, unsafe bundle-command fixtures. |
| Events, counts, and summaries | `scripts/validate-change-metadata.py` | Added bundle reference checks, result enum validation, failure detail requirements, integer counts, duplicate stage rejection, skipped/not-run handling, exact summary derivation, and exact blocker-set comparison. | Make compact event evidence machine-checkable and prevent stored summaries from hiding drift or blockers. | R25-R50, R76-R82, TCVM-004, TCVM-005, TCVM-014 through TCVM-017. |
| Reconstruction and compactness | `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py`, compactness fixtures | Added path-expanding bundle reconstruction, common-read surface extraction, compactness measurement, and representative legacy/compact fixture proof. | Satisfy the audit boundary: compact storage is acceptable only after exact reconstruction passes. | R29-R32, R59-R61, AC18, AC23, TCVM-013 and TCVM-019. |
| Review count cross-checking | `scripts/validate-change-metadata.py` | Reused existing review-artifact parser output when referenced review artifacts exist. | Avoid copied count drift and keep parser output authoritative. | R43-R44, R49, R82, TCVM-017. |
| No-execution proof | `scripts/test-change-metadata-validator.py` | Added a sentinel command that would create a file if the validator executed bundle commands. | Prove metadata validation inspects command strings only and does not run validation bundles. | R57-R58, AC24, TCVM-020, `CVM-M3-CR3`. |
| Fixtures | `tests/fixtures/change-metadata/**` | Added valid compact metadata, invalid compact cases, unsafe path/command cases, review-count fixtures, transcript fixture, and representative compactness fixture pair. | Exercise the public CLI against real metadata shapes instead of relying only on helper-level assertions. | TCVM-001 through TCVM-020. |

## Tests Added Or Changed

- `scripts/test-change-metadata-validator.py` now covers legacy compatibility, compact required sections, mixed-shape rejection, bundle references, result enums, failure details, structured counts, path-variable parsing, path safety, lifecycle stages, first-exists behavior, transcript references, reconstruction, derived summaries, review-count cross-checking, compactness proof, and no-execution behavior.
- `TCVM-001` through `TCVM-003` prove legacy/compact migration behavior.
- `TCVM-006` through `TCVM-012` prove path variables, lifecycle stages, first-exists behavior, and transcript references.
- `TCVM-013` proves accumulated path reconstruction for path-expanding bundles.
- `TCVM-014` through `TCVM-017` prove summary derivation, blockers, skipped/not-run handling, and review-count cross-checks.
- `TCVM-019` proves material compactness only after reconstruction passes.
- `TCVM-020` proves the validator does not execute bundle commands.

The test level is mostly fixture-driven integration because the public contract is the behavior of `scripts/validate-change-metadata.py` against real `change.yaml` files. Helper-level checks are used only for parsing, safety helpers, reconstruction, and compactness measurement where direct assertions are clearer.

## Validation Evidence Available Before Final Verify

Validation recorded during implementation and review-resolution includes:

- `python scripts/test-change-metadata-validator.py`
- `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`
- `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
- direct expected-failure checks for unresolved variables, missing transcript references, unknown lifecycle stages, unsafe bundle commands, summary conflicts, review-count mismatches, and extra summary blockers
- direct validation of `compactness-representative-legacy` and `compactness-representative-compact`
- `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/review_artifact_validation.py`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`
- lifecycle explicit-path validation over the proposal, spec, test spec, plan, plan index, change metadata, review log, review-resolution, and code-review records
- `git diff --check --`

Final verify and selected CI are still pending and are not claimed by this explanation.

## Review Resolution Summary

`review-resolution.md` is closed and contains seven accepted, resolved findings:

- Spec review: `CVM-SR1`, `CVM-SR2`, `CVM-SR3`.
- M2 code review: `CVM-M2-CR1`.
- M3 code review: `CVM-M3-CR1`, `CVM-M3-CR2`, `CVM-M3-CR3`.

The M2 finding added bundle-command safety validation. The M3 findings tightened summary blocker derivation, replaced the inline compactness proof with representative reconstruction-gated fixtures, and made the no-execution sentinel test meaningful.

See `docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md` for the durable dispositions.

## Alternatives Rejected

- Keep the verbose legacy validation list only: rejected because common inspection remains expensive and metadata continues to scale with reruns.
- Suppress validation detail entirely: rejected because it loses durable audit value.
- Shorten prose result strings only: rejected because it does not solve repeated commands, repeated paths, or structured queryability.
- Allow mixed legacy and compact evidence in one file: rejected because it creates ambiguous precedence between conflicting evidence.
- Standardize transcript internals in this slice: deferred because the first slice only needs optional reference syntax and target existence.
- Bulk-migrate historical `change.yaml` files: deferred until validator support exists and a separate migration proposal justifies it.

## Scope Control

The implementation preserves these non-goals:

- Legacy valid metadata remains accepted.
- No bulk historical migration was performed.
- Validation selectors, command exit behavior, and failure detection semantics were not changed.
- Review-record, review-log, and review-resolution semantics were not changed.
- Transcript internals were not standardized.
- No CLI scaffolding was added for writing compact metadata.
- Compactness proof is subordinate to reconstruction and count-preservation checks.

Unrelated local lifecycle-validator edits and untracked learn artifacts are present in the worktree but are not part of this committed branch diff or this explanation.

## Risks And Follow-Ups

- Final selected CI has not run yet.
- Final verify has not run yet.
- PR handoff has not been prepared.
- Compactness proof uses a representative fixture pair, so future changes to fixture formatting should keep reconstruction and count preservation ahead of byte-count assertions.
- Follow-on work remains possible for bulk migration, a standardized `change.validation-log.yaml` internal schema, and CLI scaffolding that writes compact metadata automatically.

## Current Readiness

All implementation milestones are closed after clean code review. This explanation records the rationale needed before final verification. The next workflow stage is `verify`; this artifact does not claim verify, CI, branch, or PR readiness.
