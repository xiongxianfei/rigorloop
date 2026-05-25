# Explain Change: Installed-Skill Artifact Placement Contract

## Summary

This change makes installed skills self-contained for first-slice artifact-placement questions. It adds deterministic validation for placement wording, updates `proposal-review`, `spec-review`, and `plan` skill text, synchronizes `docs/workflows.md` as a project-local map, records generated adapter and cold-read proof, and keeps the exact review-record schema and lifecycle semantics outside the skill bodies.

The practical outcome is that a skill-only adopter can answer:

- where a formal `proposal-review` record goes;
- where a formal `spec-review` record goes before a change pack exists;
- which plan surface is the workflow map, plan index, plan body, change metadata, or change-local evidence.

## Problem

External adopter sessions showed that installed RigorLoop skills could ask for lifecycle evidence without carrying enough placement guidance. The old answer often lived in repository-local guidance such as `docs/workflows.md`, but a skill-only adopter may not have that file.

The approved direction was to make installed skills carry concise portable placement defaults, keep `docs/workflows.md` as a synchronized project-local customization map, and use validation to prevent drift.

## Decision Trail

| Decision surface | Decision | Resulting implementation |
|---|---|---|
| Proposal | Choose concise placement-in-skills plus change-pack-first formal review locality. | First-slice skills now state formal review paths, review-log path, conditional review-resolution path, pre-change-pack behavior, and isolated advisory behavior. |
| Spec R1-R8 | Public artifact/review skills must state owned placement and formal review paths. | `proposal-review` and `spec-review` now include `Artifact placement` sections with stage-owned default paths. |
| Spec R9-R13 | Formal lifecycle review locality applies to clean and material reviews; isolated advisory remains lightweight. | Review skills state create/request change pack before `Recording status: recorded`, and preserve isolated advisory review without lifecycle artifacts. |
| Spec R14-R17 | Lookup precedence honors explicit paths, metadata, schemas, workflow rows, portable defaults, then block. | Skill wording and `docs/workflows.md` state per-artifact workflow-guide precedence and fallback to portable defaults. |
| Spec R18-R19 | Plan surfaces must be named precisely. | `plan` now distinguishes `docs/workflows.md`, `docs/plan.md`, `docs/plans/YYYY-MM-DD-slug.md`, `docs/changes/<change-id>/change.yaml`, and `docs/changes/<change-id>/`. |
| Spec R20-R23 | Workflow guide remains secondary; schemas stay outside skills. | `docs/workflows.md` now says it summarizes/customizes placement but does not replace owning skill contracts. |
| Spec R26-R28 | Skill validation owns first drift checks. | `scripts/skill_validation.py` and `scripts/test-skill-validator.py` validate first-slice paths, stage-owned wording, workflow drift, and plan surfaces. |
| Spec R29-R30 | Generated output and cold-read proof are required. | `behavior-preservation.md` records adapter archive proof and cold-read answers. |
| Plan | Split implementation into M1 validator scaffolding, M2 public wording, M3 generated-output proof. | Each milestone was implemented and code-reviewed separately. |
| Architecture | Not required. | No new architecture artifact was created; the change stays within existing skill, docs, validator, and lifecycle surfaces. |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `scripts/skill_validation.py` | Added first-slice placement constants and helper checks for review paths, stage-owned record type wording, review-log path, conditional review-resolution, create/request change-pack behavior, isolated advisory carve-out, workflow-map sync, and plan-surface paths. Wired canonical checks for `proposal-review`, `spec-review`, and `plan`. | The placement contract needed deterministic drift protection and a cold-read failure mode for wrong stage-owned wording. | Spec R1-R8, R18-R19, R26-R28; test spec T1-T6. | `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; code-review M1/M2. |
| `scripts/test-skill-validator.py` | Added compliant and negative fixture tests, including the regression where `spec-review` had the correct path but still said `proposal-review records`. | The validator must reject right-path/wrong-stage text because installed-skill readers need both path and owned record type. | Spec R2, R4-R5, R26; test spec T1-T4, T6. | Tests passed after M1 and M2; `SAP-M1-CR1` resolution proved wrong-stage wording now fails. |
| `skills/proposal-review/SKILL.md` | Added concise `Artifact placement` guidance naming `proposal-review` record path, review log, conditional review resolution, change-pack-first formal recording, clean review receipt behavior, isolated advisory behavior, and workflow fallback. | Skill-only adopters need placement answers from the installed skill itself. | Spec R1-R11, R14-R17, R22-R23; AC1, AC3-AC5. | Canonical skill validation; generated adapter archive content check. |
| `skills/spec-review/SKILL.md` | Added the same placement contract for `spec-review`, with the `spec-review-r<n>.md` stage-owned path. | Resolves the early-lifecycle `spec-review` placement gap before a change pack exists. | Spec R1-R11, R14-R17, R22-R23; AC2-AC5. | Canonical skill validation; cold-read proof; generated adapter archive content check. |
| `skills/plan/SKILL.md` | Added explicit plan-surface definitions and partial workflow-guide fallback wording. | Removes ambiguity around "the plan" by naming the workflow map, plan index, plan body, change metadata, and change-local evidence. | Spec R18-R19; AC8. | Plan-surface validator helper and canonical plan-skill check. |
| `docs/workflows.md` | Clarified that the workflow guide is a project-local customization map, not the owning portable contract, and that it takes precedence only for artifact types it specifies. | Keeps customization without making `docs/workflows.md` the only source of installed-skill placement rules. | Spec R14-R15, R20-R21, R28; proposal Option 3. | Workflow-map drift check through skill validation. |
| `specs/installed-skill-artifact-placement-contract.md` | Recorded the approved contract: portable placement defaults, change-pack-first locality, lookup precedence, plan-surface naming, generated-output proof, and non-goals. | Converts the proposal into normative requirements for implementation and review. | Proposal and proposal-review observations. | Spec-review approved. |
| `specs/installed-skill-artifact-placement-contract.test.md` | Mapped requirements and edge cases to validator tests, manual cold-read proof, generated-output proof, and behavior preservation. | Makes the contract testable before implementation. | Spec R1-R30, examples E1-E4, EC1-EC8. | Test spec approved; plan-review approved. |
| `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/behavior-preservation.md` | Recorded generated adapter archive proof, cold-read answers, behavior-preservation matrix, and boundary checks. | M3 needed durable evidence that installed output contains the revised skill bodies and that the contract preserves custom paths and schema ownership. | Spec R29-R30; test spec T8, T10, T11. | `build-skills`, `build-adapters`, `validate-adapters`, exact archive content checks. |
| `docs/changes/2026-05-25-installed-skill-artifact-placement-contract/*` | Added change metadata, review log, review records, review resolution, and lifecycle evidence. | The workflow requires durable review and validation evidence for proposal/spec/plan/test/implementation/review loops. | `docs/workflows.md`, formal review contract, active plan. | Review artifact validation, change metadata validation, lifecycle validation. |
| `docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md` and `docs/plan.md` | Created and maintained the active plan, milestone states, validation notes, and current handoff. | Multi-milestone work needed explicit sequencing and state synchronization. | Plan policy and plan-review. | Plan-review approved; code-review M2/M3 caught and closed state-sync issues. |

## Tests Added Or Changed

| Test surface | What it proves | Why this level is appropriate |
|---|---|---|
| `test_installed_skill_artifact_placement_contract_helper_accepts_compliant_review_skills` | Correct `proposal-review` and `spec-review` placement blocks pass. | Unit-level fixture proof is enough for deterministic text contract checks. |
| Wrong-record-type tests | `proposal-review` text cannot claim `spec-review records`, and `spec-review` text cannot claim `proposal-review records`. | This directly covers the M1 review finding and the cold-read adopter gap. |
| Missing-path and missing-change-pack tests | Missing default record path or pre-change-pack behavior fails. | These are stable string and behavior-boundary requirements from R3-R8. |
| Workflow-map sync test | A stale workflow-guide formal-review row fails against the skill defaults. | Drift between dual placement surfaces is the core validator responsibility. |
| Plan-surface tests | Ambiguous plan wording fails; explicit surface names pass. | R18-R19 require deterministic plan-surface clarity. |
| Canonical skill checks | Updated public `proposal-review`, `spec-review`, and `plan` skill bodies pass the first-slice validators. | M2 is the point where fixture scaffolding became public skill enforcement. |
| Generated-output proof | Temporary Codex, Claude, and opencode adapter archives contain the revised skill bodies. | R29/AC10 require installable output, not just canonical source, to contain the revised contract. |
| Cold-read proof | Skill text alone answers the three adopter questions. | The original problem is adopter-facing discoverability, so manual proof is appropriate and durable. |

## Validation Evidence Available Before Final Verify

Validation recorded during implementation and review includes:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m3-adapters
python scripts/validate-adapters.py --root /tmp/rigorloop-m3-adapters --version v0.1.5
python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-installed-skill-artifact-placement-contract
python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
git diff --check -- ...
```

Manual checks recorded in `behavior-preservation.md` and `code-review-m3-r1.md` confirmed that Codex, Claude, and opencode adapter archives under `/tmp/rigorloop-m3-adapters` contain the revised `proposal-review`, `spec-review`, and `plan` skill-body paths.

CI status is not claimed by this artifact.

## Review Resolution Summary

Material findings were recorded and closed in `review-resolution.md`.

| Finding ID | Disposition | Result |
|---|---|---|
| `SAP-M1-CR1` | accepted | Validator helpers/tests now reject wrong stage-owned record-type wording. |
| `SAP-M2-CR1` | accepted | Plan readiness state was synchronized before M2 closeout and M3 handoff. |

Closeout status is `closed`; unresolved findings are `0`. M3 code review recorded no material findings.

## Alternatives Rejected

- Updating only `docs/workflows.md` was rejected because installed skills travel independently of this repository's workflow guide.
- Copying full artifact-location tables into every skill was rejected because it would bloat skill text and raise drift risk.
- Beside-source early review records and mirror-later placement were rejected because they split lifecycle evidence and require reconciliation rules.
- CLI scaffolding for new change packs was deferred because this slice only needed wording, validation, and generated-output proof.
- Build-time shared partials were deferred because the first slice needed a small proof before adding another abstraction.
- Bulk migration of historical artifacts was out of scope.

## Scope Control

The implementation stayed within the first slice:

- updated `proposal-review`, `spec-review`, and required `plan` wording;
- updated `docs/workflows.md` as the synchronized project map;
- added validator and test coverage for placement contracts;
- recorded generated-output and cold-read proof.

It did not change review schema fields, review statuses, severity or disposition semantics, lifecycle stage order, CLI behavior, historical artifact locations, or generated adapter package source. Generated adapter archives were built in `/tmp` and were not tracked.

## Risks And Follow-Ups

- The first slice covers `proposal-review`, `spec-review`, and `plan`; other review skills should receive the same placement pattern in a later slice.
- The generated archive content check is recorded as manual proof rather than a new reusable script; a future slice could add a formal archive-content assertion if this proof becomes recurring.
- Change-pack creation remains wording-driven; CLI scaffolding such as `rigorloop new-change` remains a follow-up.
- Final `verify`, branch readiness, PR readiness, and hosted CI status are not claimed here.

## Current Handoff

All implementation milestones are closed after code review. This explain-change artifact is recorded so the next stage can run `verify`.
