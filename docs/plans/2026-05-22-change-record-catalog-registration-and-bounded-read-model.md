# Change-Record Catalog Registration and Bounded Read Model Plan

## Status

active

## Purpose / big picture

Implement the approved change-record catalog contract in reviewable slices. The implementation must make deterministic change-local evidence files route through registered evidence classes, make unregistered deterministic evidence produce registration debt before verify, and add bounded read/query paths for common change-record questions without weakening existing lifecycle, review, selector, validation, branch-readiness, or PR-readiness semantics.

The plan keeps the proposal's separation discipline: Workstream A ships first and owns evidence registration plus selector routing; Workstream B follows and owns bounded query helper behavior plus stage-skill read guidance.

## Source artifacts

- Proposal: `docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`
- Spec: `specs/change-record-catalog-registration-and-bounded-read-model.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`
- Test spec: `specs/change-record-catalog-registration-and-bounded-read-model.test.md`
- Proposal review: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/proposal-review-r1.md`
- Spec reviews: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r1.md`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/spec-review-r2.md`
- Architecture review: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md`
- Review resolution: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`

## Context and orientation

- `scripts/validation_selection.py` owns changed-path classification, stable check IDs, selected-check routing, and unclassified path diagnostics.
- `scripts/select-validation.py` is the CLI wrapper around validation selection.
- `scripts/ci.sh` runs selected checks and must preserve selected-check coverage, command exit behavior, and failure detection.
- `scripts/test-select-validation.py` is the selector and CI wrapper regression suite. It already contains route coverage for many `docs/changes/<change-id>/...` evidence names and should be extended for registered/unregistered evidence behavior.
- `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, and `scripts/validate-review-artifacts.py` remain validators. Query behavior must not move into `validate-change-metadata.py`.
- `schemas/change.schema.json` and compact metadata behavior remain valid unless the query helper needs read-only support for both legacy and compact shapes.
- `skills/` is the only authored skill source. Generated adapter output must be validated when canonical stage-skill text changes.
- `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/` is the change-local evidence root for this initiative.

## Non-goals

- Do not bulk-migrate historical change records.
- Do not weaken changed-path selector safety or let unregistered evidence silently pass.
- Do not make `manual-routing-required` a permanent workaround for deterministic in-repo evidence.
- Do not change workflow stage order, review status meanings, milestone state values, branch readiness, PR readiness, or final readiness semantics.
- Do not replace the active plan, review log, review resolution, explain-change, or other authoritative state owners.
- Do not make `change.yaml` the default source for questions owned by another artifact.
- Do not execute validation commands from query-helper reads.
- Do not add automated evidence-file scaffolding in this feature.

## Requirements covered

- CRM-R1 through CRM-R11: M1.
- CRM-R12 through CRM-R21: M2.
- CRM-R22 through CRM-R43, CRM-R53, CRM-R56: M3.
- CRM-R44 through CRM-R48: M4.
- CRM-R49 through CRM-R52: all implementation milestones and M5.
- CRM-R54 through CRM-R55: M1.
- AC-CRM-001 through AC-CRM-007: M1 and M2.
- AC-CRM-008 through AC-CRM-012, AC-CRM-014: M3.
- AC-CRM-013 and AC-CRM-016: M4.
- AC-CRM-015 and AC-CRM-017: all milestones and M5.

## Current Handoff Summary

- Current milestone: M5. Lifecycle evidence and final closeout
- Current milestone state: closed
- Last reviewed milestone: M5. Lifecycle evidence and final closeout closed by `code-review-m5-r2`
- Review status: `code-review-m5-r2` found no material findings after `CRM-M5-CR1` resolution.
- Remaining in-scope implementation milestones: none
- Next stage: hosted CI and human review for PR #87
- Final closeout readiness: PR #87 is open for hosted CI and human review.
- Reason final closeout is or is not ready: all in-scope implementation milestones are closed, explain-change is current, final local verification passed, and PR #87 is open; hosted CI and human review remain outside local verification.

## Milestones

### M0. Plan-review and test-spec handoff

- Milestone state: closed
- Goal: Review this plan, then create the focused test spec before implementation starts.
- Requirements: CRM-R1 through CRM-R56; AC-CRM-001 through AC-CRM-017.
- Files/components likely touched:
  - `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`
  - `docs/plan.md`
  - `specs/change-record-catalog-registration-and-bounded-read-model.test.md` after plan-review
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/`
- Dependencies:
  - Accepted proposal.
  - Approved spec.
  - Approved architecture-review.
- Tests to add/update:
  - None in this milestone; the test-spec is the next lifecycle artifact after plan-review.
- Implementation steps:
  - Run plan-review against this plan.
  - Resolve any material plan-review findings before test-spec.
  - Create `specs/change-record-catalog-registration-and-bounded-read-model.test.md` after plan-review approval.
  - Ensure the test spec covers selector registry behavior, actual changed-path proof, query helper slices, legacy/compact metadata compatibility, stage-skill guidance, and generated adapter validation.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path specs/change-record-catalog-registration-and-bounded-read-model.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`
  - `git diff --check -- docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md docs/plan.md docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`
- Expected observable result: plan-review can approve or challenge concrete sequencing, and test-spec has a clear downstream scope.
- Commit message: `M0: plan change record catalog model`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Starting implementation before test-spec exists could miss selector/query edge cases.
- Rollback/recovery:
  - Keep implementation blocked and revise the plan, spec, or architecture if plan-review finds an uncovered contract gap.

### M1. Evidence class registry and registered selector routing

- Milestone state: closed
- Goal: Add the evidence-class registry behavior and deterministic selector routing for registered recurring change-local evidence files.
- Requirements: CRM-R1 through CRM-R11, CRM-R20, CRM-R50 through CRM-R52, CRM-R54, CRM-R55; AC-CRM-001, AC-CRM-002, AC-CRM-005 through AC-CRM-007, AC-CRM-015, AC-CRM-017.
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py` only if output formatting or CLI exposure needs the registry metadata
  - `scripts/test-select-validation.py`
  - `tests/fixtures/` only if selector fixtures are moved out of inline tests
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`
- Dependencies:
  - Approved plan-review.
  - Approved focused test spec.
  - Existing selector routing and check IDs remain authoritative.
- Tests to add/update:
  - Registry entry shape includes evidence class ID, allowed root, bounded pattern or exact filename, selector routes, validator, lifecycle stage, and conditions.
  - Registered patterns such as `*-audit.md`, `*-identity.txt`, `*-preservation.md`, `behavior-preservation.md`, and `baseline.md` route deterministically.
  - Exact filename registration works for a novel evidence class.
  - Broad catch-all patterns such as `*.md` or `*.txt` are rejected.
  - Ambiguous evidence class matches fail.
  - Registry changes select selector regression coverage.
- Implementation steps:
  - Inspect current `docs/changes/<change-id>/...` routing logic.
  - Prefer a centralized selector-owned registry surface if it keeps the selector clear and testable.
  - If a separate registry file adds unnecessary churn, implement a selector-owned registry table in `scripts/validation_selection.py` with fixture-backed tests, as allowed by CRM-R55.
  - Add bounded pattern matching and ambiguity detection.
  - Keep registered evidence routing tied to existing check IDs and affected roots rather than creating new validation semantics.
  - Record behavior-preservation evidence comparing existing evidence routes before and after the registry.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
  - `git diff --check --`
- Expected observable result: registered evidence files route through declared selector checks, broad or ambiguous patterns fail tests, and existing valid change records remain valid.
- Commit message: `M1: add change evidence registry routing`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Registry patterns could be too broad and silently capture unrelated evidence.
  - Extracting a separate registry file could complicate selector startup or selected-CI behavior.
- Rollback/recovery:
  - Revert the registry layer and restore prior explicit selector routes while keeping tests that identify the unsafe broad or ambiguous cases.

### M2. Registration debt and actual changed-path proof

- Milestone state: closed
- Goal: Make unregistered deterministic evidence produce stable registration debt and require actual changed-path selector proof before verify.
- Requirements: CRM-R7 through CRM-R21, CRM-R49 through CRM-R52; AC-CRM-003 through AC-CRM-005, AC-CRM-015, AC-CRM-017.
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/ci.sh` only if selected/local mode output needs a stable diagnostic-preserving adjustment
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`
- Dependencies:
  - M1 registry routing is in place.
  - Test spec covers the difference between actual changed paths, explicit paths, and supplemental fixtures.
- Tests to add/update:
  - Deterministic unregistered evidence under a change root produces stable `manual-routing-required`.
  - Unresolved `manual-routing-required` is exposed as registration debt.
  - Owner-approved deferral shape can be recorded without making unregistered evidence silently route.
  - Actual changed-path routing proof is distinguishable from explicit-path lifecycle validation.
  - `python scripts/select-validation.py --mode local` or equivalent local changed-set command includes the branch's own new evidence files.
- Implementation steps:
  - Add stable selector diagnostics for unregistered deterministic evidence paths.
  - Ensure selected-CI output keeps diagnostics actionable and does not hide blocking routing results.
  - Add tests proving explicit-path validation does not substitute for local changed-path routing.
  - Record selector-routing proof for this branch's actual changed paths.
  - Keep verify readiness blocked by unresolved deterministic evidence routing debt unless owner-approved deferral is recorded.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode local`
  - `bash scripts/ci.sh --mode local`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/select-validation.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`
  - `git diff --check --`
- Expected observable result: unregistered deterministic evidence fails closed with stable registration debt, and local changed-path routing can prove this branch's own evidence files before verify.
- Commit message: `M2: surface change evidence registration debt`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Local changed-path proof can be noisy when unrelated active plans exist in the worktree.
  - A diagnostic-only path could accidentally become a selected-check pass.
- Rollback/recovery:
  - Revert diagnostic changes to the prior selector behavior and keep registered routing from M1 only if M1 remains independently safe.

### M3. Bounded change-record query helper

- Milestone state: closed
- Goal: Add the repository-owned query helper for bounded `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>` reads.
- Requirements: CRM-R22 through CRM-R43, CRM-R49 through CRM-R53, CRM-R56; AC-CRM-008 through AC-CRM-012, AC-CRM-014, AC-CRM-015, AC-CRM-017.
- Files/components likely touched:
  - `scripts/query-change-record.py`
  - `scripts/test-query-change-record.py`
  - `scripts/validate-change-metadata.py` only for importable read helpers, not query subcommands
  - `tests/fixtures/change-metadata/**` or `tests/fixtures/change-record-query/**`
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`
- Dependencies:
  - M1 and M2 are closed or deliberately left independent by plan-review.
  - Test spec defines expected query outputs and diagnostics.
  - Compact and legacy metadata shapes accepted by existing validators remain supported or produce stable unsupported-shape diagnostics.
- Tests to add/update:
  - `summary` returns change ID, canonical artifact paths, review state, latest validation state, blockers, and detail pointers.
  - `artifacts` returns canonical artifact paths only.
  - `validation --latest` returns only latest validation result, bundles, counts, blockers, and transcript pointer when present.
  - `validation --stage <stage>` returns only requested stage evidence and detail pointers.
  - Legacy metadata and compact metadata fixtures are supported where safe.
  - Malformed, ambiguous, unsupported, unknown change ID, unknown stage, and invalid subcommand cases produce stable diagnostics.
  - Query helper does not execute validation commands and does not modify files.
- Implementation steps:
  - Add a new script rather than a `validate-change-metadata.py` subcommand.
  - Reuse safe metadata loading/parsing helpers where practical without coupling query behavior to validation CLI semantics.
  - Define deterministic output shape suitable for assertions.
  - Return repo-relative paths only.
  - Add full-read escalation pointers in query output or diagnostics where bounded reading is insufficient.
  - Record behavior-preservation proof comparing query answers against manual full-file extraction for representative legacy and compact fixtures.
- Validation commands:
  - `python scripts/test-query-change-record.py`
  - `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary`
  - `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model artifacts`
  - `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model validation --latest`
  - `python scripts/test-change-metadata-validator.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/query-change-record.py --path scripts/test-query-change-record.py --path tests/fixtures/change-metadata --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
  - `git diff --check --`
- Expected observable result: common change-record questions can be answered through bounded query commands without reading full validation history or running proof commands.
- Commit message: `M3: add change record query helper`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Query helper could hide failure or blocker evidence.
  - Reusing validator internals could blur validation and query responsibilities.
- Rollback/recovery:
  - Revert the helper and tests without changing evidence files or selector routing from Workstream A.

### M4. Stage-skill read guidance and generated adapter proof

- Milestone state: closed
- Goal: Update affected stage skills to name bounded change-record slices or query-helper commands after helper command names are stable, then validate generated adapter output.
- Requirements: CRM-R44 through CRM-R48, CRM-R49 through CRM-R52; AC-CRM-013, AC-CRM-014, AC-CRM-016, AC-CRM-017.
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/plan/SKILL.md` only if plan state guidance needs a bounded-read reference
  - `scripts/test-skill-validator.py` or targeted static proof if existing validation does not catch stale command references
  - generated adapter validation output only; do not hand-edit generated public adapter package output
- Dependencies:
  - M3 query-helper command names are stable.
  - Test spec names which stage skills need read guidance.
  - Skill changes preserve public/customer-portable wording and keep repository-maintainer details out of published skills where required.
- Tests to add/update:
  - Static proof that affected skills name bounded slices or query-helper commands for common stage-owned questions.
  - Static proof that stage skills include full-read escalation conditions.
  - Generated adapter validation or drift proof for changed skill text.
  - Optional proof that skill-referenced query commands exist in `scripts/query-change-record.py` help or command registry.
- Implementation steps:
  - Update only the affected canonical skills.
  - Avoid broad "read `change.yaml`" wording when a bounded query exists.
  - Keep current live workflow state owned by active plans, not query helper output.
  - Add or update static proof for command-name drift if no existing validator covers it.
  - Run skill checks and repository-supported adapter archive validation required for canonical skill changes.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `tmp=$(mktemp -d) && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmp" && python scripts/validate-adapters.py --root "$tmp" --version v0.1.5`
  - `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary`
  - `bash scripts/ci.sh --mode explicit --path skills/proposal-review/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path scripts/query-change-record.py`
  - `git diff --check --`
- Expected observable result: stage skills guide bounded reads and escalation without relying on chat discipline, and generated adapter checks prove public skill output compatibility.
- Commit message: `M4: add bounded change record read guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Skill guidance could drift from the helper interface.
  - User-facing skills could expose repository-maintainer-only implementation details.
- Rollback/recovery:
  - Revert skill guidance and proof changes while keeping the query helper available; rebuild or revalidate adapters after revert.

### M5. Lifecycle evidence and final closeout

- Milestone state: closed
- Goal: Complete downstream lifecycle evidence after all implementation milestones are closed.
- Requirements: CRM-R49 through CRM-R52; AC-CRM-015, AC-CRM-017.
- Files/components likely touched:
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/explain-change.md`
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/verify-report.md` when verify-report is triggered
  - `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
  - `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`
  - `docs/plan.md`
- Dependencies:
  - M1 through M4 closed.
  - Required code-review and review-resolution loops closed.
  - ci-maintenance run if selected CI or routing gaps are triggered.
- Tests to add/update:
  - No new implementation tests unless explain-change, verify, or ci-maintenance identifies a gap.
- Implementation steps:
  - Record explain-change after implementation and review-resolution closeout.
  - Run verify against all touched authoritative artifacts and selected CI.
  - Update plan body and `docs/plan.md` lifecycle state before PR handoff.
  - Prepare PR handoff only after verify passes.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-query-change-record.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `tmp=$(mktemp -d) && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmp" && python scripts/validate-adapters.py --root "$tmp" --version v0.1.5`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path specs/change-record-catalog-registration-and-bounded-read-model.md --path specs/change-record-catalog-registration-and-bounded-read-model.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`
  - `bash scripts/ci.sh --mode local`
  - `git diff --check --`
- Expected observable result: all in-scope implementation milestones are closed, final rationale and verification evidence exist, plan state is synchronized, and PR handoff can proceed.
- Commit message: `M5: close change record catalog lifecycle`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Active plan state could drift from `docs/plan.md` before PR.
  - Final selected CI could surface unregistered evidence files created during this change.
- Rollback/recovery:
  - Keep the plan active, resolve stale state or selector routing debt, rerun verify, and only then proceed to PR.

## Validation plan

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`: validates formal review evidence and review-resolution closeout.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`: validates this change metadata while the plan evolves.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path specs/change-record-catalog-registration-and-bounded-read-model.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`: validates lifecycle-managed artifact state.
- `python scripts/test-select-validation.py`: selector and CI wrapper regression suite for Workstream A.
- `python scripts/select-validation.py --mode local`: actual changed-path selector proof for Workstream A.
- `bash scripts/ci.sh --mode local`: actual changed-path selected-CI proof before verify when deterministic evidence files are added.
- `python scripts/test-query-change-record.py`: query helper regression suite once M3 adds it.
- `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary`: active change bounded read smoke after M3.
- `python scripts/test-change-metadata-validator.py`: legacy and compact metadata compatibility proof.
- `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/build-skills.py --check`, and release-archive adapter generation plus `python scripts/validate-adapters.py --root "$tmp" --version v0.1.5`: canonical skill and generated adapter proof when M4 edits skills.
- `bash scripts/ci.sh --mode local`: final branch-local changed-path selected-CI proof over the branch changed paths.
- `git diff --check --`: whitespace and patch hygiene.

## Risks and recovery

- Risk: Registry patterns become too broad.
  - Recovery: Keep broad-pattern rejection and ambiguity tests blocking before selector routing uses the pattern.
- Risk: New deterministic evidence still reaches verify with `manual-routing-required`.
  - Recovery: Treat the diagnostic as registration debt, keep the plan active, and resolve routing or owner-approved deferral before verify.
- Risk: Query helper hides failures or blockers.
  - Recovery: Require blocker/detail-pointer assertions and full-read escalation cases in M3 tests; revert helper output changes if they omit failure evidence.
- Risk: Stage skills drift from query helper command names.
  - Recovery: Add static drift proof in M4 or keep skill guidance deferred until command names stabilize.
- Risk: Workstream B changes obscure Workstream A rollback.
  - Recovery: Keep Workstream A and B commits/milestones separate; revert query/helper/skill slices without removing evidence registry routing.
- Risk: Existing valid change records fail during migration.
  - Recovery: Run legacy metadata and representative change-record validation; preserve legacy path behavior or revert the offending milestone.

## Dependencies

- Plan-review must approve this plan before test-spec.
- Matching test spec must be written and approved before implementation starts.
- Workstream A must close before Workstream B skill guidance changes.
- Existing selector check IDs and validator responsibilities remain authoritative.
- Existing compact and legacy metadata contracts remain valid unless a later approved spec amendment changes them.
- No new third-party dependency is expected.

## Progress

- 2026-05-22: Plan created after proposal acceptance, spec-review approval, architecture update, ADR acceptance, and clean architecture-review.
- 2026-05-22: Clean plan-review recorded in `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/plan-review-r1.md`.
- 2026-05-22: Test spec created at `specs/change-record-catalog-registration-and-bounded-read-model.test.md`; ready for M1 implementation.
- 2026-05-22: M1 implemented selector-owned evidence class registry, registered evidence routing, registry validation tests, representative route fixture updates, and `behavior-preservation.md`.
- 2026-05-22: `code-review-m1-r1` recorded material finding `CRM-M1-CR1`; M1 moved to `resolution-needed`.
- 2026-05-22: `CRM-M1-CR1` accepted and fixed by adding governing change-root output to registered evidence routing and extending selector regression coverage; M1 moved back to `review-requested`.
- 2026-05-22: `code-review-m1-r2` recorded clean re-review for `CRM-M1-CR1`; M1 closed and handoff moved to M2 implementation.
- 2026-05-22: M2 implemented `unregistered-change-evidence` classification, stable registration-debt diagnostics for deterministic unregistered evidence, registered `selector-routing-proof.md` as routing-coverage evidence, and added actual local changed-path proof distinguishing local routing from explicit-path selection.
- 2026-05-22: `code-review-m2-r1` recorded material finding `CRM-M2-CR1`; M2 moved to `resolution-needed`.
- 2026-05-22: `CRM-M2-CR1` accepted and fixed by adding owner-approved deferral parsing/evaluation, no-deferral, incomplete-deferral, mismatched-path, and complete-deferral selector tests; M2 moved back to `review-requested`.
- 2026-05-22: M3 implemented the bounded change-record query helper and resolved `CRM-M3-CR1`; `code-review-m3-r2` closed M3 and handoff moved to M4 implementation.
- 2026-05-22: M4 implemented bounded change-record read guidance in `proposal-review`, `code-review`, `verify`, `pr`, and `plan`, with static skill proof and adapter validation evidence.
- 2026-05-22: `code-review-m4-r1` recorded clean review for bounded change-record read guidance. M4 closed and handoff moved to M5 implementation.
- 2026-05-22: M5 recorded `explain-change.md`, updated change metadata and active plan state, and prepared lifecycle evidence for code-review handoff.
- 2026-05-22: `code-review-m5-r1` recorded material finding `CRM-M5-CR1`; M5 moved to `resolution-needed`.
- 2026-05-22: `CRM-M5-CR1` accepted and fixed by replacing final `bash scripts/ci.sh --mode selected` proof references with repository-supported `bash scripts/ci.sh --mode local` references in the test spec and active plan. M5 moved back to `review-requested`.
- 2026-05-22: `code-review-m5-r2` recorded clean re-review for `CRM-M5-CR1`; M5 closed and handoff moved to final closeout.
- 2026-05-22: Final closeout refreshed `explain-change.md` after M5 re-review and moved handoff to verify.
- 2026-05-22: Verify passed after replacing stale adapter `--check` proof references with current release-archive adapter validation. Handoff moved to PR.
- 2026-05-22: PR #87 opened for hosted CI and human review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-22 | Sequence Workstream A before Workstream B. | Selector/CI routing risk and query/skill guidance risk have different rollback surfaces, and the approved proposal/spec require Workstream A as the first implementation slice. | Ship registry, query helper, and skill guidance in one implementation milestone. |
| 2026-05-22 | Keep evidence registry selector-owned in the first slice. | The selector owns changed-path routing and stable check IDs; a centralized registry file is preferred only when it reduces rather than increases selector complexity. | Add a separate registry file unconditionally before proving selector fit. |
| 2026-05-22 | Add a new query helper script for reads. | The approved spec and ADR keep querying separate from validation proof work. | Add query subcommands to `validate-change-metadata.py`. |
| 2026-05-22 | Update stage-skill guidance only after query-helper commands are stable. | Skill guidance must not reference unstable commands and must preserve generated adapter compatibility. | Edit skills in the same milestone as initial query-helper implementation. |

## Surprises and discoveries

- M1 kept the registry table in `scripts/validation_selection.py` rather than adding a separate registry file because the selector already owns path classification and check ID routing. This follows CRM-R55 for the first slice.
- Some existing recurring evidence names, such as `script-output-audit.md`, naturally match broader evidence classes like `audit`; the registry avoids duplicate exact entries for those names so ambiguity tests remain meaningful.

## Validation notes

- 2026-05-22: Plan-review recording validation passed: review artifact closeout, change metadata, artifact lifecycle explicit paths, whitespace, and explicit selected CI.
- 2026-05-22: Test-spec authoring validation passed: review artifact closeout, change metadata, artifact lifecycle explicit paths, whitespace, and explicit selected CI.
- 2026-05-22: M1 validation passed: `python scripts/test-select-validation.py`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`; `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`.
- 2026-05-22: M1 post-recording selected CI passed with `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- 2026-05-22: Code-review M1 R1 recording validation passed with review artifact structure validation, change metadata validation, artifact lifecycle validation, whitespace check, and explicit selected CI.
- 2026-05-22: `CRM-M1-CR1` resolution validation passed: `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`; `python scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `git diff --check --`.
- 2026-05-22: Code-review M1 R2 recording validation passed: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/code-review-m1-r2.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/code-review-m1-r2.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `git diff --check --`.
- 2026-05-22: M2 selector validation passed: `python scripts/test-select-validation.py`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-25-example/notes.md` blocked with `manual-routing-required` registration debt; `python scripts/select-validation.py --mode local` routed actual M2 changed paths and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`; `bash scripts/ci.sh --mode local` passed selected local checks; `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/select-validation.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md` passed supplemental explicit selected CI; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `git diff --check --`.
- 2026-05-22: Code-review M2 R1 recording validation passed with review artifact structure validation, change metadata validation, artifact lifecycle validation, explicit selected CI, and whitespace check.
- 2026-05-22: `CRM-M2-CR1` resolution validation passed: `python scripts/test-select-validation.py`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/unregistered-evidence.md`; `python scripts/select-validation.py --mode local`; `bash scripts/ci.sh --mode local`; `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md --path docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md --path docs/plan.md`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model`; `git diff --check --`.
- 2026-05-22: Code-review M2 R2 found no material findings and closed M2 after `CRM-M2-CR1` resolution. Review reran `python scripts/test-select-validation.py` and direct unregistered-evidence selector proof; post-recording validation passed with review artifact closeout, change metadata validation, artifact lifecycle validation, explicit selected CI, and whitespace check.
- 2026-05-22: M3 query helper tests were written before implementation and initially failed because `scripts/query-change-record.py` did not exist. After implementation, `python scripts/test-query-change-record.py` passed 11 tests covering compact and legacy summary queries, artifact-only output, validation latest and stage-scoped reads, no-validation and stage-not-found diagnostics, unknown change/query diagnostics, unsafe path fail-closed behavior, read-only behavior, deterministic output, and active change summary.
- 2026-05-22: M3 selector support was added for `scripts/query-change-record.py` and `scripts/test-query-change-record.py` so selected CI routes query-helper changes through `change_record_query.regression` and supported metadata-shape regression. `python scripts/test-select-validation.py` passed after the selector update.
- 2026-05-22: M3 active query proof passed: `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary`; `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model artifacts`; `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model validation --latest`.
- 2026-05-22: Code-review M3 R1 found `CRM-M3-CR1`: the query helper returns an empty artifact list for an accepted compact metadata shape whose artifact paths live in `path_vars`; M3 remains `resolution-needed`.
- 2026-05-22: `CRM-M3-CR1` resolution validation passed: `python scripts/test-query-change-record.py`; direct compact `path_vars` fixture proof using `tests/fixtures/change-metadata/compact-valid/change.yaml` copied under a temporary `docs/changes/compact-valid/change.yaml`; `python scripts/test-change-metadata-validator.py`; `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`; active `summary`, `artifacts`, and `validation --latest` query commands; explicit selected CI for query/helper/metadata paths. M3 returned to `review-requested`.
- 2026-05-22: `code-review-m3-r2` recorded clean re-review for `CRM-M3-CR1`; M3 closed and handoff moved to M4 implementation.
- 2026-05-22: M4 validation passed: `python scripts/test-skill-validator.py` initially failed before skill edits on missing bounded-read guidance, then passed 161 tests after updates; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; `python scripts/test-adapter-distribution.py`; archive adapter proof with `python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmp"` plus `python scripts/validate-adapters.py --root "$tmp" --version v0.1.5`; active query-helper summary smoke; explicit selected CI for changed skill, skill-test, and query-helper paths; `git diff --check --`.
- 2026-05-22: `python scripts/build-adapters.py --check` still fails against baseline retired tracked adapter-tree expectations: default version `0.1.1` mismatches tracked `v0.1.5`, and `v0.1.5 --check` expects repository-tree adapter skill bodies that current `AGENTS.md` and `dist/adapters/README.md` say are release archives for `v0.1.3` and later. M4 used release-archive generation and validation as the current supported adapter proof and recorded the baseline check mismatch for code-review visibility.
- 2026-05-22: M4 implemented bounded change-record read guidance in `proposal-review`, `code-review`, `verify`, `pr`, and `plan` skills. Added static regression proof that affected skills name bounded slices or query commands and full-read escalation conditions. M4 moved to `review-requested`.
- 2026-05-22: Code-review M4 R1 found no material findings. Review recording validation passed with review artifact closeout, change metadata validation, artifact lifecycle validation, explicit selected CI, and whitespace check.
- 2026-05-22: M5 validation passed: `python scripts/test-select-validation.py`; `python scripts/test-query-change-record.py`; `python scripts/test-change-metadata-validator.py`; `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`; `python scripts/build-skills.py --check`; release archive adapter proof with `python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmp"` plus `python scripts/validate-adapters.py --root "$tmp" --version v0.1.5`; review artifact closeout; change metadata validation; artifact lifecycle validation; local selected CI with `bash scripts/ci.sh --mode local`; and `git diff --check --`.
- 2026-05-22: M5 recorded that `python scripts/build-adapters.py --check` still fails against retired tracked adapter-tree expectations, and `bash scripts/ci.sh --mode selected` is no longer a supported wrapper mode. The current equivalents used for M5 are release-archive adapter validation and `bash scripts/ci.sh --mode local`.
- 2026-05-22: Code-review M5 R1 recording validation passed with review artifact structure validation, change metadata validation, artifact lifecycle validation, explicit selected CI, and whitespace check.
- 2026-05-22: `CRM-M5-CR1` resolution validation passed: `bash scripts/ci.sh --mode local`; `python scripts/validate-change-metadata.py docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`; artifact lifecycle explicit-path validation over the touched test spec, plan, change metadata, review artifacts, explain-change, and plan index; review artifact closeout; and whitespace check.
- 2026-05-22: Code-review M5 R2 found no material findings after `CRM-M5-CR1` resolution. Review recording validation passed with review artifact closeout, change metadata validation, artifact lifecycle validation, selected local CI, and whitespace check.
- 2026-05-22: Explain-change refresh validation passed with review artifact closeout, change metadata validation, artifact lifecycle validation, selected local CI, and whitespace check.
- 2026-05-22: Verify discovered that the test spec and active plan still listed `python scripts/build-adapters.py --check`, which fails against retired tracked adapter-tree expectations. The governing adapter proof references were updated to the current release-archive validation path from `AGENTS.md` and `dist/adapters/README.md`.
- 2026-05-22: Final verify passed: selector regression, query-helper regression, metadata validator regression, skill validation, skill validator regression, generated skill check, adapter distribution tests, release-archive adapter generation and validation, active query summary smoke, local selector proof, review artifact closeout, change metadata validation, artifact lifecycle validation over governing lifecycle artifacts, local selected CI, and whitespace check.

## Outcome and retrospective

- Pending completion.

## Readiness

- See `Current Handoff Summary`.
- PR #87 is open for hosted CI and human review; not Done.
