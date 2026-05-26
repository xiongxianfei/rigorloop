# CI-Maintenance Skill Rename and Workflow Authoring Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: `2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring`
- Current owner: agent
- Current stage: implement
- Next stage: implement M2
- Blockers: none

## Purpose / Big Picture

Rename the authored `ci` skill to `ci-maintenance` as a hard identifier migration, then add the reusable GitHub Actions workflow skeleton, risk-to-check reference, validator coverage, and generated-adapter proof required by the approved spec.

The implementation must keep repository `.github/workflows/*.yml` behavior unchanged. This change improves the skill that authors and reviews CI infrastructure; it does not use the skill to rewrite this repository's own CI workflows.

## Source Artifacts

- Proposal: [2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md](../proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md)
- Spec: [ci-maintenance-skill.md](../../specs/ci-maintenance-skill.md)
- Test spec: [ci-maintenance-skill.test.md](../../specs/ci-maintenance-skill.test.md)
- Change record: [change.yaml](../changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml)
- Review log: [review-log.md](../changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-log.md)
- Review resolution: [review-resolution.md](../changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-resolution.md)
- Architecture: not required.

Architecture is intentionally skipped. The approved spec and spec-review record keep this change within existing authored-skill, packaged-resource, validator, generated-adapter, and release-note boundaries. It does not introduce a new runtime data flow, persistence model, deployment boundary, adapter architecture, or security/trust-boundary mechanism. The plan therefore records sequencing and proof for existing mechanisms instead of creating a separate architecture artifact.

## Context and Orientation

- The current authored skill source is `skills/ci/SKILL.md` with front matter `name: ci`, while the body already describes `ci-maintenance`.
- The approved spec requires a hard rename to `skills/ci-maintenance/SKILL.md`; no first-slice alias and no duplicate active `ci` skill body.
- Published skill front matter must include `name: ci-maintenance`, `version`, and `schema-version` matching the current published-skill contract.
- `ci-maintenance` may wire known project validation commands into workflow YAML, but it must not invent commands, design tests, run validation, wait for hosted CI, or claim readiness.
- The workflow skeleton is a `COPY` asset. The risk-to-check map is a `READ` reference with portable core rows, project-specific extension rows, and a fail-safe rule for unmapped changed surfaces.
- Existing governance surfaces contain known stale references that should be updated only where they mean the skill identifier or entrypoint, including `AGENTS.md`, `skills/workflow/SKILL.md`, `specs/skill-contract.md`, and `specs/workflow-stage-autoprogression.test.md`.
- Generic `CI` prose, shell script names, validation commands such as `scripts/ci.sh`, and actual `.github/workflows/*.yml` files are out of scope unless they are direct skill-identifier references.
- Current adapter manifest version is `v0.1.5`; generated adapter proof should use temporary output directories for `v0.1.3` and later rather than hand-editing generated package output.

## Non-Goals

- Do not change actual repository `.github/workflows/*.yml` behavior.
- Do not keep or introduce a first-slice `ci` compatibility alias.
- Do not install both `ci` and `ci-maintenance` as active skill directories.
- Do not add deployment, release publishing, self-hosted runner, or organization-level Actions policy support.
- Do not add language-specific workflow skeletons.
- Do not hand-edit generated public adapter package output.
- Do not proceed to implementation before plan-review and test-spec are complete.

## Requirements Covered

| Requirement area | Requirements |
| --- | --- |
| Skill identity and hard rename | `CIM-R1` through `CIM-R11` |
| Skill role and command boundary | `CIM-R12` through `CIM-R19`, `CIM-R46` through `CIM-R49` |
| Packaged resources | `CIM-R20` through `CIM-R33` |
| GitHub Actions authoring and review defaults | `CIM-R34` through `CIM-R45`, `CIM-R50` through `CIM-R54` |
| Validator coverage | `CIM-R55` through `CIM-R61` |
| Generated adapters and repository workflow non-change | `CIM-R62` through `CIM-R65` |
| Front matter metadata | `AC-CIM-FM-001` through `AC-CIM-FM-004` |
| Workflow sequencing | `AC-CIM-SEQ-001` through `AC-CIM-SEQ-004` |
| Permissions clarity | `AC-CIM-PERM-001` through `AC-CIM-PERM-004` |

## Current Handoff Summary

- Current milestone: M2 - Validator and Fixture Coverage
- Current milestone state: planned
- Last reviewed milestone: M1 - Canonical skill rename and packaged resources
- Review status: M1 code-review-r1 completed with no material findings; M1 is closed
- Remaining in-scope implementation milestones: M2, M3
- Next stage: implement M2
- Final closeout readiness: not ready
- Reason: M1 is closed after clean code review. Validator/fixture coverage and generated-adapter proof remain pending.

## Milestones

### M1 - Canonical Skill Rename and Packaged Resources

- Milestone state: closed
- Goal: Rename the authored skill to `ci-maintenance`, add the skeleton and risk-map resources, and update direct authored skill-identifier references without changing repository CI workflows.
- Requirements: `CIM-R1` through `CIM-R49`, `CIM-R65`, `AC-CIM-FM-001` through `AC-CIM-FM-004`, `AC-CIM-PERM-001` through `AC-CIM-PERM-004`.
- Likely files:
  - `skills/ci/SKILL.md`
  - `skills/ci-maintenance/SKILL.md`
  - `skills/ci-maintenance/assets/github-workflow-skeleton.yml`
  - `skills/ci-maintenance/references/risk-to-check-map.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `specs/skill-contract.md`
  - `specs/skill-contract.test.md`
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `specs/token-and-runtime-efficient-scanning.test.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/behavior-preservation.md`
- Steps:
  1. Move the canonical authored skill source from `skills/ci/` to `skills/ci-maintenance/`.
  2. Normalize front matter to `name: ci-maintenance`, `version: "1.0.0"`, and `schema-version: skill-readability-v1` unless the current reviewed skill contract names a newer schema before implementation.
  3. Rewrite the skill body around the approved role, command ownership boundary, PR/boundary split, safety defaults, review output, and direct-invocation behavior.
  4. Add `assets/github-workflow-skeleton.yml` as a copy-and-fill GitHub Actions skeleton with least-privilege permissions, concurrency, timeouts, action-reference placeholders, deterministic install placeholders, validation-command placeholders, and cache-key or cache-omission guidance.
  5. Add `references/risk-to-check-map.md` as a portable core plus project-specific extension reference with an unmapped-surface fail-safe.
  6. Update direct `ci` skill-identifier references in governing authored surfaces and fixtures. Preserve generic continuous-integration prose and script names.
  7. Record behavior-preservation evidence proving skill identity is corrected, workflow behavior is unchanged, and authoring capability is strengthened.
- Validation:
  - `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-m1-skills/skills`
  - `rg -n "name: ci|role_name: ci|skills/ci/SKILL.md|skills/ci/|when ci is run|when \`ci\` is run|ci-mantance" skills docs specs AGENTS.md`
  - `git diff --check --`
- Result: closed after clean code-review-r1. Canonical skill source moved to `skills/ci-maintenance/SKILL.md`, packaged skeleton and risk-map resources were added, direct entrypoint references were updated, behavior preservation was recorded, and no `.github/workflows/*.yml` behavior changed.
- Risks:
  - Overbroad text replacement could alter generic CI prose or script names.
  - The published skill could become too repository-internal if RigorLoop-specific rows are not clearly labeled as examples.
- Rollback:
  - Restore `skills/ci/`, remove the new resources, and revert identifier-reference edits if validation proves the hard rename cannot be completed in this slice.

### M2 - Validator and Fixture Coverage

- Milestone state: planned
- Goal: Make the rename, resource map, skeleton defaults, risk-map boundary, command blocker, and workflow-review checks deterministic through repository-owned validation.
- Requirements: `CIM-R50` through `CIM-R61`, `AC-CIM-FM-004`, `AC-CIM-PERM-001` through `AC-CIM-PERM-004`.
- Likely files:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - existing or new validator fixtures under `tests/fixtures/skills/`
  - `docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/behavior-preservation.md`
  - `docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`
- Steps:
  1. Add positive validation for `ci-maintenance` front matter, resource-map verbs, skeleton presence, reference presence, permissions defaults, concurrency, PR trigger structure, boundary structure, timeout placeholders, action-reference placeholders, command placeholders, cache guidance, portable/project-specific risk-map split, and unmapped-surface fail-safe.
  2. Add negative validation for stale `name: ci`, stale `role_name: ci`, stale direct-invocation handoff wording, missing `version`, missing `schema-version`, missing or wrong resource-map verbs, missing resource files, missing permissions defaults, and contradictory permissions wording.
  3. Add review-authoring fixtures proving overbroad permissions, unsafe path filters, slow comprehensive PR checks, and missing validation command sources are flagged rather than silently accepted.
  4. Keep validator checks stable and text-scoped; do not introduce AI-dependent semantic tests.
- Validation:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-m2-skills/skills`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`
  - `git diff --check --`
- Result: pending
- Risks:
  - Validator assertions could become brittle if they overfit exact prose instead of checking stable contract markers.
  - Review fixtures could accidentally test behavior that belongs to `verify` or `test-spec`.
- Rollback:
  - Revert the new validator assertions and fixtures while keeping M1 skill/resource changes available for narrower validation redesign.

### M3 - Generated Adapter Proof and Migration Evidence

- Milestone state: planned
- Goal: Prove generated public adapters include `ci-maintenance` and packaged resources, prove generated adapters do not expose active `ci`, and record adopter-visible hard-rename guidance.
- Requirements: `CIM-R7` through `CIM-R11`, `CIM-R62` through `CIM-R65`, `AC-CIM-013` through `AC-CIM-015`.
- Likely files:
  - `dist/adapters/manifest.yaml`
  - `dist/adapters/README.md`
  - `docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/behavior-preservation.md`
  - `docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/generated-output-proof.md`
  - `docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`
  - `docs/plans/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md`
- Steps:
  1. Update tracked adapter support metadata so the manifest exposes `ci-maintenance` and no active `ci` skill for the first slice.
  2. Add adopter-facing migration guidance that direct `ci` invocations must move to `ci-maintenance`.
  3. Build generated local skill output from canonical skills and prove the renamed skill and resources appear.
  4. Build temporary public adapter archives for `v0.1.5` and validate those archives.
  5. Inspect generated archive contents or validation output to prove `ci-maintenance` resources are packaged and no active `ci` skill body is exposed.
  6. Record behavior-preservation and generated-output proof.
- Validation:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-m3-skills/skills`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
  - `python scripts/build-adapters.py --check --version v0.1.5 --verbose`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md --path specs/ci-maintenance-skill.md --path specs/ci-maintenance-skill.test.md --path docs/plans/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md --path docs/plan.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-log.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-resolution.md`
  - `git diff --check --`
- Result: pending
- Risks:
  - `build-adapters.py --check` may report expected tracked-tree deferral for `v0.1.3` and later; temporary output build plus `validate-adapters.py` remains the packaging proof.
  - Adapter metadata could be updated without validating archive contents.
- Rollback:
  - Revert adapter support metadata and migration guidance while keeping canonical skill changes available until generated packaging is repaired.

## Validation Plan

Before implementation starts, plan-stage validation is limited to artifact lifecycle and metadata checks:

- `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md --path specs/ci-maintenance-skill.md --path docs/plans/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md --path docs/plan.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-log.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-resolution.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/proposal-review-r1.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/proposal-review-r2.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/proposal-review-r3.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/spec-review-r1.md --path docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/spec-review-r2.md`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring`
- `git diff --check --`

After plan-review, the test-spec must map each `MUST` and acceptance criterion to concrete tests before implementation starts.

Final pre-PR validation must include the milestone validations plus:

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-final-skills/skills`
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
- `bash scripts/ci.sh --mode explicit --path skills/ci-maintenance/SKILL.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path dist/adapters/manifest.yaml --path dist/adapters/README.md --path specs/ci-maintenance-skill.md --path specs/ci-maintenance-skill.test.md`
- `git diff --check --`

## Risks and Recovery

| Risk | Mitigation | Recovery |
| --- | --- | --- |
| Hard rename breaks generated adapter routing | Validate temporary adapter archives and manifest metadata before PR. | Revert adapter metadata and block for a later alias/routing spec if hard rename cannot validate. |
| Stale `ci` references remain in identifier surfaces | Use validator assertions and targeted stale-reference scans. | Fix only identifier references; preserve generic CI prose and command names. |
| Public skill becomes RigorLoop-specific | Keep RigorLoop surfaces in project-specific extension rows and public text portable. | Move repo-specific details back to governance/change-local docs. |
| Skeleton encourages invented commands or invented SHAs | Keep placeholders explicit and enforce command-source and action-reference rules. | Replace concrete invented values with placeholders and blocker behavior. |
| Validator checks become brittle | Check stable markers, resources, and fixture outcomes rather than broad prose. | Narrow validator assertions to contract-owned text and fixture shapes. |
| Repository workflow behavior changes accidentally | Exclude `.github/workflows/*.yml` from scope and record diff proof. | Revert workflow changes unless a separate approved change owns them. |

## Dependencies

- Approved proposal and approved spec are present.
- Proposal-review and spec-review material findings are closed in `review-resolution.md`.
- Architecture artifact is not required for this slice for the rationale recorded above.
- Plan-review must approve this plan before test-spec.
- Test-spec must be created and reviewed enough to guide implementation before M1 starts.
- Current adapter version for generated-output proof is `v0.1.5`.

## Progress

- 2026-05-26: Proposal accepted after review and revision.
- 2026-05-26: Spec approved after resolving `CIM-SR1`, `CIM-SR2`, and `CIM-SR3`.
- 2026-05-26: Execution plan created; implementation not started.
- 2026-05-26: Plan-review approved the plan with no material findings.
- 2026-05-26: Test spec created; implementation not started.
- 2026-05-26: M1 implementation started.
- 2026-05-26: M1 implementation completed and handed to code-review.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-26 | Skip a separate architecture artifact. | The approved spec uses existing skill/resource/validator/adapter boundaries and does not introduce new runtime, data-flow, deployment, or trust-boundary architecture. | Add architecture artifact before planning. |
| 2026-05-26 | Use three implementation milestones. | The work separates cleanly into canonical skill/resources, deterministic validation, and generated-adapter/migration proof. | One large implementation slice; generated proof bundled into validator work. |
| 2026-05-26 | Keep hard rename behavior in the plan. | The approved spec determined no safe current alias mechanism for the first slice and forbids duplicate active skill bodies. | Compatibility alias in the first slice; duplicate `ci` and `ci-maintenance` installed directories. |

## Surprises and Discoveries

- None yet.

## Validation Notes

- `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring` passed with 5 reviews, 6 findings, 5 log entries, and 6 resolution entries.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the proposal, spec, plan, plan index, change metadata, review log, review resolution, and proposal/spec review records.
- `git diff --check --` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml` passed after test-spec creation.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring` passed after test-spec creation with 6 reviews, 6 findings, 6 log entries, and 6 resolution entries.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed after test-spec creation for the proposal, spec, test spec, plan, plan index, change metadata, review log, review resolution, and review records.
- `git diff --check --` passed after test-spec creation.
- `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md` passed for M1.
- `python scripts/validate-skills.py` passed for M1, validating 23 canonical skill files.
- `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-cim-m1-skills/skills` passed for M1.
- `python scripts/test-skill-validator.py` passed for M1 with 184 tests.
- M1 stale-reference scan found only intentional hard-rename spec/test references and false positives from `name: ci-maintenance` / `role_name: ci-maintenance`.
- `git diff -- .github/workflows` produced no output for M1.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml` passed after M1.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring` passed after M1.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed after M1 for the proposal, spec, test spec, plan, plan index, change metadata, review log, review resolution, and review records.
- `git diff --check --` passed after M1.
- Further implementation validation is deferred until the next implementation milestone after M1 review closes.

## Outcome and Retrospective

Pending. This plan remains active until all implementation milestones close and downstream `explain-change`, `verify`, and `pr` gates are complete.

## Readiness

Ready for code-review M1.

Remaining gates before Done:

- code-review M1
- implementation milestone M2
- code-review M2
- implementation milestone M3
- code-review M3
- review-resolution, when triggered
- ci-maintenance, when triggered
- explain-change
- verify
- pr
