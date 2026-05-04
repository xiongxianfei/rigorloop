# Formal Review Recording Change Explanation

## Summary

This change implements the approved formal review recording contract through the M4 implementation closeout.

Formal lifecycle review records are now stage-neutral across `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`. Detailed review records are required only when the approved trigger policy applies, clean reviews can remain artifact-local, no-material detailed records do not require empty `review-resolution.md` files, material findings remain traceable through stable Finding IDs, and `pr-review` remains unsupported.

M1-M4 implementation milestones and M4 code-review are complete. Downstream verify, final explain-change, and PR handoff still own branch readiness and PR readiness.

## Problem

The repository already had durable change-local review artifacts, but the trigger policy was too code-review-centered. Proposal, spec, architecture, and plan reviews could produce material findings or blocking non-approval outcomes without clear rules for when to create detailed review records, how to avoid empty `review-resolution.md` files, and how to keep reviewed artifact status separate from review evidence.

The implementation needed to align the governing contracts, validator coverage, review skills, generated outputs, and lifecycle evidence without adding a dedicated `pr-review` stage or turning every clean review into boilerplate.

## Decision Trail

- Proposal: `docs/proposals/2026-05-04-formal-review-recording.md`
- Spec: `specs/formal-review-recording.md`, requirements `R1`-`R16b`
- Test spec: `specs/formal-review-recording.test.md`, tests `T1`-`T16`
- Existing governing contracts: `specs/review-finding-resolution-contract.md` and `specs/rigorloop-workflow.md`
- Plan: `docs/plans/2026-05-04-formal-review-recording.md`
- Architecture: not required. The approved work reuses the existing `docs/changes/<change-id>/reviews/`, `review-log.md`, `review-resolution.md`, and review artifact validator model without adding a new storage, parser, deployment, or integration boundary.

## Diff Rationale By Area

| File or area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `specs/formal-review-recording.md` and `specs/formal-review-recording.test.md` | Define the stage-neutral formal review recording contract and matching test map. | Establishes the authoritative behavior and proof plan for `R1`-`R16b`. | Lifecycle validation and explicit CI. |
| `specs/review-finding-resolution-contract.md` and `.test.md` | Align detailed-record, initial-root, no-material, reconstructed-record, and closeout wording with formal review recording. | Keeps the existing review-resolution contract compatible with upstream formal review stages. | `T17`; lifecycle validation. |
| `specs/rigorloop-workflow.md` and `.test.md` | Add workflow requirements for detailed-record triggers, supported review stages, no-material roots, and artifact status boundaries. | Keeps lifecycle routing consistent across proposal, spec, architecture, plan, and code review. | `T27`; lifecycle validation. |
| `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` | Add concise contributor-facing rules for formal review records and material finding closeout. | Prevents operational guidance from preserving a code-review-only model. | Selector-selected explicit CI. |
| `scripts/review_artifact_validation.py` | Treat `rethink` and `inconclusive` as blocking closeout statuses. | Matches the approved stage-owned non-approval outcome vocabulary. | `python scripts/test-review-artifact-validator.py`. |
| `scripts/test-review-artifact-validator.py` | Adds supported-stage, unsupported `pr-review`, upstream material finding, no-material `plan-review`, and closeout blocking coverage. | Proves the validator supports the approved structural contract. | Review artifact regression suite. |
| Review-stage skills | Add detailed review record trigger guidance to `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`. | Satisfies `R15` so contributors see the same trigger policy from each formal review skill. | `python scripts/test-skill-validator.py`. |
| Downstream closeout skills | Update `workflow`, `verify`, `explain-change`, and `pr` with no-material record and closeout blocking boundaries. | Preserves `R12`-`R13` downstream handoff rules. | Skill validator and explicit CI. |
| Generated outputs | Regenerate `.codex/skills/**` and `dist/adapters/**` from canonical skills. | Satisfies `R15a` without hand-editing generated files. | Build drift checks and adapter validation. |
| `docs/changes/2026-05-04-formal-review-recording/` | Adds and updates change metadata, explanation, review log, review-resolution, and reconstructed review evidence. | Provides durable traceability for the non-trivial workflow-governance change. | Change metadata and review artifact validation. |
| `docs/plan.md` and the plan body | Track M1-M4 completion and clean M4 code-review while keeping the initiative Active for downstream gates. | Keeps lifecycle state accurate until verify, final explanation, and PR handoff complete. | Artifact lifecycle validation. |

## Tests Added Or Changed

- `specs/formal-review-recording.test.md`
  - Maps `R1`-`R16b` to review artifact, workflow, skill, generated-output, and final validation proof.
- `specs/review-finding-resolution-contract.test.md`
  - Adds the paired contract proof for formal review recording changes.
- `specs/rigorloop-workflow.test.md`
  - Adds workflow proof for the expanded review recording contract.
- `scripts/test-review-artifact-validator.py`
  - Covers all five supported formal lifecycle review stages, rejects `pr-review`, validates material upstream Finding ID traceability, accepts no-material `plan-review` records without `review-resolution.md`, and blocks unresolved `rethink` and `inconclusive` outcomes.
- `scripts/test-skill-validator.py`
  - Covers stable skill guidance phrases for detailed review triggers, PR comment promotion, no-material records, `review-log.md`, `review-resolution.md`, and downstream closeout boundaries.

## Review Resolution Summary

`docs/changes/2026-05-04-formal-review-recording/review-resolution.md` is closed.

| Finding | Disposition | Resolution |
| --- | --- | --- |
| `CR-M2-F1` | accepted | Created reconstructed review evidence for the M2 finding, fixed stale summary/scope wording, and validated the review-log/review-resolution closeout. |

The later M3 direct code-review was clean and produced no material findings, so no new detailed review record or resolution entry was required.

M4 code-review returned `clean-with-notes` with no blocking or required-change findings. Because it produced no material findings and no detailed-record trigger, the result is recorded artifact-locally in the plan instead of creating an empty review file.

## Validation Evidence

M4 final validation passed with the planned focused scope:

- `python scripts/test-review-artifact-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-formal-review-recording`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-formal-review-recording`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-formal-review-recording/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
- `python scripts/select-validation.py --mode explicit --path <M4 changed surface>` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `review_artifacts.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- `bash scripts/ci.sh --mode explicit --path <M4 changed surface>` passed the selected checks.

Broad smoke was not required by the plan, selector output, or review state.

## Alternatives Rejected

- Requiring detailed records for every clean review: rejected because the approved contract keeps clean reviews artifact-local when no detailed-record trigger applies.
- Creating empty `review-resolution.md` files for no-material detailed records: rejected because `review-resolution.md` is required for material findings or another approved trigger, not merely because `reviews/` exists.
- Adding a dedicated `pr-review` stage: rejected by `R1b` and `R11c`; material PR comments must be promoted into a supported formal lifecycle review record before disposition.
- Making review files authoritative for proposal, spec, architecture, ADR, or plan status: rejected because artifact status remains artifact-local.
- Adding semantic review-quality judgment to the structural validator: rejected because `R16b` keeps validation structural.

## Scope Control

- No product runtime behavior, service behavior, deployment, storage, API, or external integration changed.
- No new review directory taxonomy was added.
- Historical change packs were not migrated.
- Generated `.codex/skills/` and `dist/adapters/` output was refreshed only through repository generators.
- The plan remains Active after M4 because downstream verify, final explain-change, and PR handoff have not completed.

## Risks And Follow-Ups

- Hosted CI has not been observed in this environment.
- Downstream `verify` still owns `branch-ready`.
- `pr` still owns PR body readiness and PR opening.

## Readiness

M1-M4 implementation milestones and M4 code-review are complete. The next workflow stage is verify.
