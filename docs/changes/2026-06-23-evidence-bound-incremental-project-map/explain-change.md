# Explain Change

Change: `2026-06-23-evidence-bound-incremental-project-map`

Status: recorded before final verify

## Summary

This change turns `project-map` from a lightweight orientation prompt into an
evidence-bound, freshness-aware, packaged public skill without changing its
mandate. It still describes current repository reality. It does not design
future architecture, replace source inspection, or become a backlog.

The implementation adds normalized skill metadata, explicit workflow role,
operating modes, metadata and freshness rules, evidence classes, root and area
map contracts, source-rank guidance, downstream reliance limits, a copy-and-fill
skeleton asset, focused validator coverage, representative output proof,
cold-read proof, generated adapter proof, and lifecycle evidence.

## Problem

The accepted proposal identified six reliability gaps in the old skill:

- current-state claims were not classified precisely;
- map freshness was undefined;
- root and area maps were allowed but not structurally connected;
- the required output shape lived only as prose in `SKILL.md`;
- source-of-truth boundaries did not sufficiently separate current code from
  future intent;
- downstream reliance was underspecified.

The approved spec preserves the orientation-only role while requiring maps to
say what they cover, what evidence supports material claims, which claims are
inferred, what remains unknown, and when direct source inspection is still
required.

## Decision Trail

| Decision point | Outcome | Evidence |
| --- | --- | --- |
| Proposal direction | Option 4 plus the skeleton asset was accepted: add evidence, freshness, scope, and area-map contracts while preserving observation-only behavior. | `docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md` |
| Spec contract | `specs/project-map.md` approved R1-R84 for role boundaries, modes, freshness, evidence classes, root/area maps, skeleton packaging, downstream reliance, generated adapter inclusion, no migration, and proof requirements. | `specs/project-map.md` |
| Architecture correction | PMAP-AR1-F1 was accepted: Project maps are a first-class repository container, separate from Architecture. | `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md`; `docs/architecture/system/architecture.md`; `docs/architecture/system/diagrams/container.mmd` |
| Plan sequencing | PMAP-PLAN1-F1 split M1 and M2 so each milestone closed with passing validation. PMAP-PLAN2-F1 and PMAP-PLAN3-F1 corrected lifecycle status synchronization. | `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md`; `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md` |
| Milestones | M1 added controlled validator scaffolding; M2 updated canonical skill and skeleton; M3 added representative output and cold-read proof; M4 proved generated adapter inclusion. | `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md` |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/project-map/SKILL.md` | Normalized frontmatter, workflow role, modes, metadata/freshness, evidence/source-rank, command/runtime distinctions, root/area contract, diagram rules, downstream reliance, result shape, and stop conditions. | Implements R1-R77 while preserving the orientation-only role. | `specs/project-map.md` R1-R77; proposal goals and non-goals. | `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py -k project_map`; code-review M2 R1. |
| `skills/project-map/assets/project-map-skeleton.md` | Added copy-and-fill map skeleton with metadata fields, required sections, area registration table, and evidence trail shape. | Implements R58-R65 without moving policy out of `SKILL.md`. | `specs/project-map.md` R58-R65. | Canonical validator checks; generated adapter proof; code-review M2 R1 and M4 R1. |
| `scripts/skill_validation.py` | Added project-map contract constants and structural validation for fixtures and canonical skill/skeleton. | Proves the stable parts of the contract without building a broad produced-map artifact validator. | `specs/project-map.md` R78-R80; test spec T4-T11. | `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`. |
| `scripts/test-skill-validator.py` | Added controlled valid/invalid fixture tests, canonical corruption tests, and representative proof assertions. | Covers normalized metadata, skeleton mapping, hidden-policy rejection, representative output labels, stale/correction proof, and cold-read proof. | `specs/project-map.test.md` T4-T17. | Full skill-validator regression passed with 228 tests after M3. |
| `tests/fixtures/skills/project-map-contract/valid/` | Added controlled project-map contract fixture and skeleton asset. | Lets M1 prove the validator behavior without requiring unchanged canonical skill sources to satisfy the new contract. | Plan M1 and PMAP-PLAN1-F1 resolution. | `python scripts/test-skill-validator.py -k project_map`; `python scripts/select-validation.py --mode explicit --path tests/fixtures/skills`. |
| `scripts/validation_selection.py` and `scripts/test-select-validation.py` | Classified `tests/fixtures/skills` as validator-skill input and registered project-map output proof evidence files. | Keeps approved selected-validation commands closeable and routes deterministic M3 evidence files through lifecycle validation instead of manual-routing debt. | Plan M1 discovery and M3 selected-CI failure. | `python scripts/test-select-validation.py`; selected CI `selector.regression`. |
| `docs/architecture/system/architecture.md` and `docs/architecture/system/diagrams/container.mmd` | Added Project maps as a first-class logical repository container, distinct from Architecture. | Resolves PMAP-AR1-F1 and aligns C4 with the Building Block View. | Architecture review R1 finding; review-resolution PMAP-AR1-F1. | Architecture-review R2/R3; lifecycle and selected CI validation. |
| `docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md` | Recorded preservation matrix and linked M3 proof surfaces. | Proves orientation-only role, current-state focus, eleven-section coverage, citations, inference split, narrow-area support, risk routing, handoff, and customer-project mode. | `specs/project-map.md` R83; test spec T16. | `scripts/test-skill-validator.py` M3 assertions; lifecycle validation. |
| `docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md` | Added root/area/stale/correction representative excerpts. | Proves metadata, required sections, root registration, parent maps, overlap ownership, evidence classes, command distinctions, diagram evidence, and no placeholders without a full artifact validator. | `specs/project-map.test.md` T12-T15. | `scripts/test-skill-validator.py` M3 assertions. |
| `docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md` | Added small repository, monorepo or multi-service, and stale-map cold-read proof. | Satisfies R84 and keeps confidence durable rather than chat-only. | `specs/project-map.md` R84; test spec T17. | `scripts/test-skill-validator.py` M3 assertions. |
| `docs/changes/2026-06-23-evidence-bound-incremental-project-map/generated-output-proof.md` | Recorded generated local skill parity, temporary adapter archive validation, and skeleton paths for Codex, Claude, and opencode. | Satisfies generated adapter inclusion and no-hand-edited-output boundaries. | `specs/project-map.md` R81-R82; test spec T18-T20. | `python scripts/build-skills.py --check`; adapter build/validation; direct archive inspection. |
| `specs/project-map.md` and `specs/project-map.test.md` | Added approved behavior and test contracts for the revised skill. | Makes the desired behavior reviewable before implementation. | Proposal and user-approved test spec. | Spec-review R1; test-spec user approval. |
| `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md`, `docs/plan.md`, and `change.yaml` | Recorded lifecycle state, milestone progress, validation evidence, changed files, and review handoffs. | Keeps the single active-plan state owner synchronized with compact change metadata. | Workflow and plan contracts. | Artifact lifecycle validation, change metadata validation, selected CI. |
| `docs/changes/.../reviews/*.md`, `review-log.md`, and `review-resolution.md` | Recorded formal reviews, material finding dispositions, clean code-review receipts, and review ledger entries. | Required by formal review recording and lifecycle gates. | Proposal/spec/architecture/plan/code review skills and workflow contract. | `python scripts/validate-review-artifacts.py`. |

## Tests Added Or Changed

| Test or proof | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `test_project_map_contract_valid_controlled_fixture_passes` | Controlled fixture satisfies the approved structural contract. | Unit-style fixture proof keeps M1 closeable before canonical skill changes. |
| Missing baseline, missing mode, missing skeleton `COPY`, and hidden skeleton policy tests | Validator rejects stable structural contract violations with expected diagnostics. | Negative fixtures are green tests because expected diagnostics are the proof. |
| Canonical project-map contract tests and corrupted canonical copies | After M2, canonical skill and skeleton satisfy enforcement and fail stable corruptions. | Canonical enforcement belongs with the canonical skill/skeleton update. |
| Representative output assertions | M3 proof includes metadata, required sections, evidence classes, command distinction, correction note, future-intent boundary, diagram evidence, and no placeholders. | String assertions are sufficient for drift-prone proof artifacts and avoid a general artifact validator. |
| Cold-read proof assertion | M3 proof covers small, multi-service, and stale-map cases with no deferral. | The test spec allows manual proof plus optional fixture assertions. |
| Selector evidence-class regression | New project-map proof evidence files route through lifecycle validation. | Prevents deterministic evidence files from creating selected-CI manual-routing debt. |
| `build-skills.py --check` and adapter build/validation | Generated local skills and adapter archives include the revised skill and skeleton. | Generated-output proof must use repository-owned generation and validation scripts. |

## Validation Evidence Available Before Final Verify

Implementation and review stages recorded these passed commands:

- `python scripts/test-skill-validator.py -k project_map`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py skills/project-map/SKILL.md`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-project-map-adapter-proof`
- `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-project-map-adapter-proof`
- `python scripts/test-select-validation.py ValidationSelectionTests.test_registered_change_evidence_patterns_and_exact_names_match_once`
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check -- ...`
- `git diff --name-only -- docs/project-map.md dist/adapters .codex/skills .agents/skills .claude/skills .opencode/skills`

Direct generated-output proof also inspected temporary adapter archives and found:

- `.agents/skills/project-map/assets/project-map-skeleton.md`
- `.claude/skills/project-map/assets/project-map-skeleton.md`
- `.opencode/skills/project-map/assets/project-map-skeleton.md`

Final `verify` has not run yet.

## Review Resolution Summary

Material findings recorded before implementation:

| Finding | Disposition | Result |
| --- | --- | --- |
| PMAP-AR1-F1 | accepted | Resolved by adding Project maps as a first-class logical repository container in architecture and the C4 container diagram. |
| PMAP-PLAN1-F1 | accepted | Resolved by making M1 fixture/helper scaffolding independently closeable and M2 own canonical source plus enforcement. |
| PMAP-PLAN2-F1 | accepted | Resolved by synchronizing the plan index next stage with the plan body. |
| PMAP-PLAN3-F1 | accepted | Resolved by tying readiness wording to the Current Handoff Summary. |

`review-resolution.md` is closed. Code-review M1, M2, M3, and M4 all recorded
`clean-with-notes` with no material findings.

## Alternatives Rejected

- Keeping the current skill unchanged was rejected because freshness, evidence quality, area-map ownership, and downstream reliance would remain implicit.
- A readability-only pass was rejected because it would not solve stale maps, evidence classification, or current-versus-planned confusion.
- Adding only the skeleton asset was rejected because structure alone would not define evidence, freshness, source rank, or map splitting.
- Automatic repository graph generation was deferred because import graphs do not replace semantic current-state orientation and would add language-specific maintenance.
- Runtime tracing was deferred because the first slice can distinguish static, test-demonstrated, executed, and inferred evidence without mandatory instrumentation.
- A dedicated produced-map artifact validator was not added because the approved first slice asked for skill/skeleton/representative proof first and no two produced-map drift cases justified it.

## Scope Control

The change deliberately preserves these boundaries:

- `project-map` remains an observation and orientation skill, not architecture design.
- Plans, proposals, specs, and ADRs are intent artifacts, not proof of current implementation.
- Existing `docs/project-map.md` was not automatically migrated.
- Generated public adapter bodies were not hand-edited.
- No runtime application code changed.
- No remote scanning, telemetry, or external indexing was added.
- Risks and open questions in maps remain orientation evidence, not automatic backlog entries.

## Risks And Follow-Ups

Remaining workflow steps:

- Final `verify` must still validate branch-wide coherence and readiness.
- PR handoff must still summarize the final reviewed diff and validation evidence.

Residual risks:

- The project-map contract is intentionally structural and representative, not a complete produced-map validator.
- Future produced maps may still need human review for claim quality, path evidence, and inference labeling.
- Existing maps remain historical until intentionally refreshed under the new contract.

Potential follow-ons remain outside this slice:

- automatic dependency or entry-point extraction;
- runtime-flow evidence collection;
- ownership-map integration;
- a produced-map artifact validator if concrete output drift recurs.
