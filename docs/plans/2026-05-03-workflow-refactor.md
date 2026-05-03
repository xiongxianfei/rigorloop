# Workflow Refactor Execution Plan

## Status

- done

- Owner: maintainers
- Start date: 2026-05-03
- Last updated: 2026-05-03
- Related issue or PR: PR #26 merged at https://github.com/xiongxianfei/rigorloop/pull/26
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow governance, docs, skill guidance, validators, and generated outputs. Focused selector-selected checks, skill validation, lifecycle validation, generated-output drift checks, adapter validation, and the final explicit-path CI wrapper are the required proof unless plan-review, test-spec, code-review, review-resolution, or verify elevates broad smoke.

## Purpose / Big Picture

Implement the approved workflow refactor around lifecycle categories instead of one overloaded linear chain. The implementation must make the category model, stage-obligation metadata, `ci-maintenance` boundary, project-map no-reliance rule, periodic `learn` handling, and workflow-handoff ownership visible in the authoritative docs, stage skills, validation surfaces, and generated outputs.

This is workflow-governance work. It changes contributor-visible policy and operator guidance, not runtime architecture, product behavior, service boundaries, storage, deployment, or release packaging.

## Source Artifacts

- Proposal: [Workflow Refactor](../proposals/2026-05-01-workflow-refactor.md), accepted.
- Spec: [RigorLoop Workflow](../../specs/rigorloop-workflow.md), approved after spec-review on 2026-05-03.
- Spec-review outcome: approved with no material findings after the standing-artifact gates, project-map minimal rule, `Runs for every change` semantics, nonblocking `learn` closeout, affected-surface alignment, and temporary learn-recording surfaces were added.
- Architecture: not required. The approved work is a workflow-governance and artifact-routing refactor without a runtime or system-shape boundary.
- Test spec: [RigorLoop workflow test spec](../../specs/rigorloop-workflow.test.md) is active and was updated by the `test-spec` stage before M1 implementation.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on a repository map for architecture or module-boundary claims; orientation comes from the approved proposal, approved workflow spec, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, README, affected skills, and bounded file inventories. If implementation later relies on repository-shape claims outside these known workflow surfaces, refresh `docs/project-map.md` or record a narrower no-map rationale before relying on those claims.

## Context and Orientation

- `specs/rigorloop-workflow.md` is the canonical workflow contract. `docs/workflows.md` is the short operational summary.
- `VISION.md` is already the canonical project-vision artifact. This refactor must not reintroduce lowercase `vision.md` as canonical or carry a future vision-rename follow-up.
- Current summary surfaces still contain the old chain vocabulary in places, including `constitution / project-map when needed`, default-looking `explore` and `research`, `ci when needed`, and `learn` as advice-only or per-change-adjacent wording.
- `review-resolution` is closeout for material review findings, not a review stage. Required open closeout blocks `verify`, final `explain-change`, and `pr`.
- `ci-maintenance` is the contributor-visible stage/action label for CI infrastructure maintenance. The existing `skills/ci/` path remains allowed; validation execution stays under `verify`.
- `learn` is periodic or explicitly invoked. Triggered learning is closed by immediate capture, a scheduled follow-up, or an explicit no-learn rationale and blocks downstream only when a higher-priority artifact says it blocks.
- Workflow-governance changes must align affected operating and governance surfaces or record unaffected/deferred decisions in a contributor-visible tracked or review-visible surface.
- Canonical authored skill sources live under `skills/`. Generated `.codex/skills/` and `dist/adapters/` output must be refreshed through repository generators, not hand-edited.

### Affected Surface Record

| Surface | Initial disposition |
| --- | --- |
| `CONSTITUTION.md` | updated in M1 for project-map no-reliance, mandatory/triggered autoprogression wording, on-demand/periodic action wording, affected-surface governance, and learn capture wording |
| `AGENTS.md` | updated in M1 for project-map no-reliance, on-demand support, periodic learn, `ci-maintenance`, review-resolution, and mandatory/triggered autoprogression wording |
| `README.md` | updated in M1 for the category model, per-change chain, no-map rule, on-demand support, periodic learn, `ci-maintenance`, and verification boundary |
| `docs/workflows.md` | updated in M1 with workflow categories, stable obligation values, per-change chain, project-map no-reliance, learn closeout, review-resolution, `ci-maintenance`, and autoprogression wording |
| `specs/rigorloop-workflow.md` | affected; status normalized to approved and used as the canonical contract |
| `specs/rigorloop-workflow.test.md` | updated by the immediate `test-spec` stage before M1; active proof map for this refactor |
| Stage skills | updated in M2 for workflow categories, standing-artifact gates, proposal-review gate checks, `ci-maintenance`, periodic/explicit `learn`, and stale handoff wording |
| `.codex/skills/` and `dist/adapters/` | regenerated in M2 from canonical skill guidance through existing scripts |
| `docs/project-map.md` | absent; no reliance in this plan unless later refreshed or bypassed with rationale |

## Non-Goals

- Do not implement project-map lifecycle mechanics, freshness markers, calendar thresholds, or project-map skill behavior.
- Do not implement the final learn artifact model with `docs/learn/YYYY-MM-DD-<slug>.md`, `docs/learnings/<topic>.md`, or action-routing rules.
- Do not rename the existing `skills/ci/` directory.
- Do not add new workflow lanes beyond fast lane and full lifecycle.
- Do not revisit the completed `VISION.md` migration or rewrite project vision content.
- Do not change CI coverage, release automation, schemas, or runtime behavior beyond wording and validation needed for this workflow refactor.
- Do not remove useful skill-local preconditions, outputs, or failure modes; move duplicated workflow-contract rules to pointers or brief summaries.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R5` | Preserve fast-lane guidance while updating full-lifecycle framing in `docs/workflows.md`, README, `AGENTS.md`, and `skills/workflow/SKILL.md` |
| `R6`-`R6i` | Category model, standing-artifact gates, project-map no-reliance rule, affected-surface alignment, and bootstrap exception in workflow docs, proposal skills, and review guidance |
| `R7`-`R7be` | Stage-obligation table, `Runs for every change` semantics, periodic `learn` triggers, nonblocking default closeout, and temporary learn-recording surfaces |
| `R7c`-`R7w` | Autoprogression, immediate-next-stage language, stage-owned authority, branch-scoped claims, and review/verify/pr boundaries in workflow docs and directly affected skills |
| `R8`-`R8ja` | Planned milestone lifecycle, plan/index coherence, targeted proof and broad-smoke triggers, and stale lifecycle blocking |
| `R8ka`-`R8kg` | Artifact lifecycle summary, settlement versus closeout states, stale touched-artifact handling, and PR-reference behavior |
| `R8l`-`R8s` | Selector-selected targeted proof, CI wrapper semantics, broad-smoke triggers, and manual proof recording |
| `R9`-`R9b` | `ci-maintenance` label and boundary between CI infrastructure work and validation execution |
| `R10`-`R12f` | Durable reasoning, PR summary, review-resolution closeout, verify-report conditionality, and concise review summaries |
| `R20`-`R24a`, `R26`, `R27` | Canonical/generated boundaries, root guidance, structural validation, generated-output drift checks, and Git/PR/CI/human-review authority |
| Acceptance criteria | Reflected through updated test spec, manual guidance checks, repository validators, generated-output checks, and final explicit-path CI proof |

## Immediate Test-Spec Handoff

After `plan-review` approval, the immediate next repository stage is `test-spec`, not implementation.

The `test-spec` stage must update or replace `specs/rigorloop-workflow.test.md` so it is active for this refactor and maps the approved category, obligation, project-map, `learn`, `ci-maintenance`, review-resolution, affected-surface, lifecycle, skill, generated-output, and validation requirements to concrete proof.

The active test spec must own the workflow test-spec coverage maps and test cases for `R6` through `R7be`, the affected acceptance criteria, and any manual proof requirements before M1 implementation starts.

Implementation milestones are test-first within their scope: add or update assertions before implementation within the milestone; close the milestone only after the paired implementation makes those assertions and validation commands pass.

## Milestones

### M1. Align Workflow Summary and Root Governance

- Goal: Update contributor-facing workflow summaries and root governance so they present the approved category model, stage-obligation taxonomy, no-map rule, `learn` closeout rule, `review-resolution` closeout gate, and `ci-maintenance` boundary consistently.
- Requirements: `R1`-`R7be`, `R8`-`R8s`, `R9`-`R12f`, `R20`-`R24a`, `R26`, `R27`.
- Files/components likely touched:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `README.md`
  - `docs/workflows.md`
  - `docs/plan.md`
  - this plan
- Dependencies:
  - approved `specs/rigorloop-workflow.md`
  - accepted plan-review
  - active updated workflow test spec
- Tests to add/update:
  - Add or update any manual proof checklist, lifecycle assertion, or content assertion required by the active test spec before changing the paired guidance.
  - Ensure the test spec names the root guidance surfaces that must show category, obligation, `ci-maintenance`, learn, project-map, and review-resolution behavior.
- Implementation steps:
  - Replace the old overloaded full-lifecycle chain with a concise category summary and a per-change chain that keeps on-demand and periodic work out of the default path.
  - Align `AGENTS.md` normal execution wording to use `ci-maintenance` and the approved continuation language.
  - Align README workflow snippets and public documentation with the approved category model.
  - Align `CONSTITUTION.md` only where its current wording conflicts with the approved workflow contract.
  - Record any intentionally unaffected or deferred affected surface in this plan or the change-local pack.
- Validation commands:
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md README.md docs/workflows.md docs/plan.md docs/plans/2026-05-03-workflow-refactor.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md`
- Expected observable result:
  - A contributor can read the root and workflow summary surfaces and see standing artifacts, living references, workflow infrastructure, on-demand artifacts, the per-change chain, and periodic learning without relying on chat history.
- Commit message: `M1: align workflow governance surfaces`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Root guidance may become too long or duplicate the spec.
- Rollback/recovery:
  - Revert the root guidance edits and keep `specs/rigorloop-workflow.md` as the only approved contract until a narrower summary can be accepted.

### M2. Align Stage Skills and Regenerate Outputs

- Goal: Update affected canonical skill guidance so local preconditions, outputs, failure modes, and handoff pointers match the approved workflow contract without duplicating the full routing table.
- Requirements: `R6`-`R7w`, `R9`-`R12f`, `R20`-`R24a`, `R27`.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/ci/SKILL.md`
  - `skills/learn/SKILL.md`
  - other stage skills whose handoff sections still duplicate old workflow-contract wording
  - `.codex/skills/`
  - `dist/adapters/`
- Dependencies:
  - M1 guidance decisions
  - active workflow test spec
- Tests to add/update:
  - Add or update focused skill-validator assertions before changing the paired skill wording when the active test spec requires machine-checkable skill-contract proof.
  - Keep manual-only wording checks in the test spec when automation would be brittle or overly broad.
- Implementation steps:
  - Update `skills/workflow/SKILL.md` to route by category, obligation, and trigger instead of the old full-prefix chain.
  - Update `proposal` and `proposal-review` for the first-substantive-proposal rule, bootstrap exception, and standing-artifact gates.
  - Update `ci` skill wording so its visible stage/action is `ci-maintenance` while the path remains `skills/ci/`.
  - Update `learn` skill wording so it is periodic or explicitly invoked and records immediate capture, scheduled follow-up, or no-learn rationale as required.
  - Update directly affected handoff sections to summarize the workflow spec rather than restating complete routing tables.
  - Regenerate `.codex/skills/` and public adapter output from canonical skill sources.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `git diff --check -- skills .codex/skills dist/adapters scripts/test-skill-validator.py`
- Expected observable result:
  - Skill users see the same workflow categories, triggers, and handoff boundaries as the approved workflow spec, and generated outputs match canonical skills.
- Commit message: `M2: align workflow stage skills`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Skill updates may unintentionally remove useful local operational guidance.
- Rollback/recovery:
  - Restore the affected canonical skill sections from the previous commit, rerun generators, and retain only the root-summary updates until narrower skill changes can be reviewed.

### M3. Update Validator and Regression Coverage

- Goal: Make repository-owned tests and selectors prove the updated workflow contract where automation is appropriate, while leaving intentionally manual content checks in the test spec.
- Requirements: `R6db`, `R7`-`R7be`, `R8k`-`R8s`, `R9`-`R12f`, `R20`-`R24a`, acceptance criteria for categories, obligation values, project-map no-reliance, learn closeout, `ci-maintenance`, affected surfaces, lifecycle status, and generated-output alignment.
- Files/components likely touched:
  - `scripts/test-select-validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-skill-validator.py`
  - `scripts/validation_selection.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/artifact_lifecycle_contracts.py`
- Dependencies:
  - active workflow test spec
  - M1 and M2 surface decisions
- Tests to add/update:
  - Add or update selector and lifecycle assertions before changing validation logic.
  - Add or update skill-validator assertions before changing canonical skill wording when a skill-contract guarantee is intended to be machine-checked.
  - Keep broad prose-quality and subjective content judgments out of scripts unless the approved test spec makes the assertion stable.
- Implementation steps:
  - Implement the selector, lifecycle, and skill-validator assertions required by the active workflow test spec.
  - Add selector regressions for the changed workflow, root guidance, skills, generated output, and lifecycle-managed artifacts.
  - Add lifecycle-validator coverage for the approved spec status, active plan/index coherence, and touched authoritative artifacts.
  - Add any focused skill-validator assertions required to keep stale old-chain wording out of canonical skills.
  - Avoid adding project-map freshness markers or learn artifact-model mechanics.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-skill-validator.py`
  - `git diff --check -- scripts`
- Expected observable result:
  - The repository-owned proof map and tests cover the workflow refactor without inventing deferred project-map or learn lifecycle mechanics.
- Commit message: `M3: add workflow refactor validation coverage`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Validator assertions may become brittle if they overfit exact prose.
- Rollback/recovery:
  - Keep semantic test coverage tied to stable IDs, table headers, stage names, and allowed values; revert brittle prose assertions and keep the requirement as manual proof in the test spec.

### M4. Close Change-Local Evidence and Final Verification

- Goal: Create or update the durable change-local pack, record affected-surface decisions, verify generated and authoritative artifacts, and prepare the final explanation and PR package.
- Requirements: `R6da`-`R6db`, `R7be`, `R8a`-`R8j`, `R8kf`, `R10`-`R12f`, `R24`, `R26`, `R27`.
- Files/components likely touched:
  - `docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - optional `docs/changes/2026-05-03-workflow-refactor/review-resolution.md` if material findings require it
  - optional `docs/changes/2026-05-03-workflow-refactor/verify-report.md` if verification evidence cannot stay concise
  - `docs/plans/2026-05-03-workflow-refactor.md`
  - `docs/plan.md`
- Dependencies:
  - M1 through M3 complete
  - code-review findings closed or validly deferred before verify
- Tests to add/update:
  - Add or update metadata and lifecycle assertions before changing validator logic if closeout reveals a missing proof requirement.
  - No new learn artifact-model tests; record no-learn rationale or scheduled follow-up in an allowed surface if a learn trigger occurs.
- Implementation steps:
  - Create the baseline non-trivial change-local pack with paths to proposal, spec, plan, test spec, implementation artifacts, validation evidence, and review state.
  - Record affected surfaces as updated, unaffected with rationale, or deferred with owner and follow-up.
  - Record the no-map rationale and any learn follow-up or no-learn rationale in tracked/review-visible surfaces.
  - Update this plan's progress, decision log, surprises, validation notes, and readiness.
  - Run final targeted validation through repository-owned scripts.
  - Move plan/index lifecycle state only when the outcome is known under the governing closeout rule.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m3-r1.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/workflow/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/ci/SKILL.md --path skills/learn/SKILL.md --path skills/verify/SKILL.md --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-skill-validator.py --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m3-r1.md`
  - `git diff --check --`
- Expected observable result:
  - Reviewers can trace the refactor from accepted proposal to approved spec, active test spec, active plan, implemented surfaces, generated outputs, validation evidence, explanation, and PR summary.
- Commit message: `M4: close workflow refactor evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Final closeout may uncover material review findings that require `review-resolution`.
- Rollback/recovery:
  - Stop before `verify` or PR if required review-resolution remains open; revert or defer only with final disposition, owner, follow-up, and validation evidence.

## Validation Plan

Use the smallest relevant proof first in each milestone, then run final explicit-path CI over the changed authoritative surfaces. Do not use broad smoke unless a higher-priority artifact, review-resolution item, or verification finding elevates it.

Core validation commands expected before PR:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/test-adapter-distribution.py
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-select-validation.py
python scripts/test-artifact-lifecycle-validator.py
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md
bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/workflow/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/ci/SKILL.md --path skills/learn/SKILL.md --path skills/verify/SKILL.md --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-skill-validator.py --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md
git diff --check --
```

The final command list must be updated during implementation to include every touched skill, script, generated output dependency, change-local artifact, and any review-resolution or verify-report file that exists.

## Risks and Recovery

- Risk: the category model gets repeated too many times and creates drift.
  Recovery: keep full normative tables in the spec, concise summaries in `docs/workflows.md`, and pointers or local summaries in skills.
- Risk: `learn` guidance becomes too detailed and preempts the later learn refactor.
  Recovery: keep only triggers, nonblocking default, and temporary recording-surface rules in this change.
- Risk: project-map wording accidentally creates freshness thresholds or markers.
  Recovery: revert to the minimal no-reliance rule and defer mechanics to a future project-map lifecycle proposal.
- Risk: generated output drifts from canonical skills.
  Recovery: rerun the generators and validate with `--check` commands before review.
- Risk: implementation touches a stage skill whose local guidance is not actually affected.
  Recovery: revert that skill edit and record the surface as unaffected with rationale in this plan or the change-local pack.
- Risk: stale plan/index state blocks final verification.
  Recovery: update this plan and `docs/plan.md` together before claiming branch-ready.

## Dependencies

- `plan-review` must accept this plan before `test-spec` and implementation proceed.
- `test-spec` must update or replace `specs/rigorloop-workflow.test.md` before implementation begins.
- Canonical skill changes must precede generated `.codex/skills/` and `dist/adapters/` refreshes.
- Material code-review findings require `review-resolution` closeout before `verify`, final `explain-change`, or `pr`.
- Final PR readiness depends on plan/index lifecycle coherence and explicit-path validation over every touched authoritative surface.

## Progress

- [x] Proposal accepted.
- [x] Spec approved after spec-review.
- [x] Plan created and indexed.
- [x] Plan reviewed.
- [x] Test spec updated and active.
- [x] M1 complete: workflow summary and root governance aligned.
- [x] M2 complete: stage skills aligned and generated outputs refreshed.
- [x] M3 complete: validator and regression coverage updated.
- [x] M4 complete: change-local evidence and final verification closed.
- [x] Code review complete.
- [x] Review-resolution complete if triggered.
- [x] Verify complete.
- [x] Explain-change complete.
- [x] PR ready.

## Decision Log

- 2026-05-03: Use the refactored workflow contract for this initiative because the work directly touches the refactored workflow surfaces.
- 2026-05-03: Normalized `specs/rigorloop-workflow.md` from `draft` to `approved` before creating the plan, per the approved spec-review closeout.
- 2026-05-03: Architecture stage is not required because the change is governance, documentation, skill guidance, validation, and generated-output alignment without runtime architecture impact.
- 2026-05-03: `docs/project-map.md` is absent. This plan records a no-map rationale and does not rely on it for architecture or repository-shape claims.
- 2026-05-03: Keep `test-spec` as the immediate next stage after `plan-review`; implementation milestones remain test-first within each milestone.
- 2026-05-03: Do not run broad smoke by default. Focused selector, skill, lifecycle, generated-output, adapter, and explicit-path CI checks are sufficient unless a later artifact elevates broad smoke.
- 2026-05-03: M1 created the baseline change-local pack early because implementation owns ordinary non-trivial change-local evidence, even though final closeout remains scheduled for M4.
- 2026-05-03: M2 kept `skills/ci/` as the implementation path while using `ci-maintenance` as the visible stage/action label, per the approved spec.
- 2026-05-03: M3 added selector and lifecycle regression coverage without production validator changes because the existing selector and lifecycle expansion behavior already satisfied the approved workflow test spec.
- 2026-05-03: M4 did not add a standalone `verify-report.md` because the closeout evidence remained concise enough in `change.yaml`, `explain-change.md`, and this plan. The later `verify` stage still owns branch-ready.
- 2026-05-03: M4 recorded an explicit no-learn rationale because no new learn trigger occurred during closeout.
- 2026-05-03: `code-review-m4-r1` returned `clean-with-notes`; no new review-resolution work was triggered.
- 2026-05-03: Verify did not run broad smoke because `broad_smoke_required` is `false` and selector output reported no broad-smoke trigger.
- 2026-05-03: Verify did not trigger `ci-maintenance`; existing `.github/workflows/ci.yml` delegates pull-request and main-branch validation to `scripts/ci.sh`.
- 2026-05-03: Final explain-change expanded the existing milestone summary into the required reviewer-facing rationale artifact before PR handoff.
- 2026-05-03: PR #26 merged. The merge-dependent lifecycle transition to `Done` is now complete in this plan body and `docs/plan.md`.

## Surprises and Discoveries

- M1 root guidance alignment did not require changing canonical stage skills, generated `.codex/skills/`, generated public adapters, or validator logic. Those surfaces remain scheduled for M2 and M3.
- M2 found that `skills/verify/SKILL.md` had direct stale handoff wording and needed alignment even though the initial named skill list focused on workflow, proposal, proposal-review, CI, and learn.
- The first M2 skill-validator assertion for stale `verify -> ci` wording was too broad because it also matched `verify -> ci-maintenance`; the assertion now rejects the old bare-stage sequence without blocking the approved `ci-maintenance` wording.
- M3 confirmed that workflow-refactor selector routing and lifecycle plan-context expansion were already implemented; the milestone only needed focused regression coverage.
- M4 found no additional affected operating or governance surfaces to defer. `docs/project-map.md` remains absent and not relied on, and the final learn artifact model remains intentionally outside this refactor.
- M4 code review reran targeted metadata, review-artifact closeout, lifecycle, and whitespace checks over the review surface and found no required fixes.
- Verify found one stale pre-verify sentence in `explain-change.md`; it was updated before the final validation pass.
- Final explain-change found no new affected surfaces or validation gaps. The remaining lifecycle transition to `Done` is merge-dependent.

## Validation Notes

- 2026-05-03 planning-stage checks passed:
  - `git diff --check --`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md`
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md`
- 2026-05-03 test-spec stage updated `specs/rigorloop-workflow.test.md` from archived historical evidence to the active proof-planning surface for this workflow refactor.
- 2026-05-03 M1 checks passed:
  - `rg -n <stale-root-guidance-patterns> README.md AGENTS.md CONSTITUTION.md docs/workflows.md`
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - `git diff --check -- CONSTITUTION.md AGENTS.md README.md docs/workflows.md docs/plan.md docs/plans/2026-05-03-workflow-refactor.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/changes/2026-05-03-workflow-refactor`
  - Selected check IDs: `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, `selector.regression`.
- 2026-05-03 M1 review-resolution checks passed after fixing stale test-spec status wording in this plan:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md`
  - `python scripts/select-validation.py --mode explicit --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m1-r1.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m1-r1.md`
  - `git diff --check -- docs/plans/2026-05-03-workflow-refactor.md docs/changes/2026-05-03-workflow-refactor`
  - Selected check IDs: `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`.
- 2026-05-03 M2 checks passed:
  - `python scripts/test-skill-validator.py` first failed as expected after adding focused M2 assertions and before the paired skill wording changes.
  - `python scripts/test-skill-validator.py`
  - `rg -n <stale-stage-skill-patterns> skills/workflow/SKILL.md skills/proposal/SKILL.md skills/proposal-review/SKILL.md skills/ci/SKILL.md skills/learn/SKILL.md skills/verify/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check` failed before regeneration with stale generated skill output, then passed after `python scripts/build-skills.py`.
  - `python scripts/build-adapters.py --version 0.1.1 --check` failed before regeneration with stale generated adapter output, then passed after `python scripts/build-adapters.py --version 0.1.1`.
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `git diff --check -- skills .codex/skills dist/adapters scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md`
  - `git diff --check -- docs/plans/2026-05-03-workflow-refactor.md docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/select-validation.py --mode explicit --path <M2-current-diff-paths>`
  - `bash scripts/ci.sh --mode explicit --path <M2-current-diff-paths>`
  - Selected check IDs: `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`.
- 2026-05-03 M3 checks passed:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md`
  - `git diff --check -- scripts`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-skill-validator.py --path docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `git diff --check -- scripts docs/plans/2026-05-03-workflow-refactor.md docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - Selected check IDs: `skills.regression`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, `selector.regression`.
- 2026-05-03 M4 checks passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m3-r1.md`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/workflow/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/ci/SKILL.md --path skills/learn/SKILL.md --path skills/verify/SKILL.md --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-skill-validator.py --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m3-r1.md`
  - `git diff --check --`
  - Selected check IDs: `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, `selector.regression`.
- 2026-05-03 code-review-m4-r1 checks passed:
  - `python scripts/select-validation.py --mode explicit --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m3-r1.md`
  - `git diff --check HEAD~1..HEAD -- docs/changes/2026-05-03-workflow-refactor/change.yaml docs/changes/2026-05-03-workflow-refactor/explain-change.md docs/plans/2026-05-03-workflow-refactor.md`
  - Selected check IDs: `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`.
- 2026-05-03 code-review-m4-r1 recording checks passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m4-r1.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m4-r1.md`
  - `git diff --check -- docs/plans/2026-05-03-workflow-refactor.md docs/changes/2026-05-03-workflow-refactor`
  - Selected check IDs: `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`.
- 2026-05-03 verify checks passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-03-workflow-refactor`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/ci/SKILL.md --path .codex/skills/learn/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path .codex/skills/proposal/SKILL.md --path .codex/skills/verify/SKILL.md --path .codex/skills/workflow/SKILL.md --path AGENTS.md --path CONSTITUTION.md --path README.md --path dist/adapters/claude/.claude/skills/ci/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/proposal/SKILL.md --path dist/adapters/claude/.claude/skills/verify/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/codex/.agents/skills/ci/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/codex/.agents/skills/proposal/SKILL.md --path dist/adapters/codex/.agents/skills/verify/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/ci/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal/SKILL.md --path dist/adapters/opencode/.opencode/skills/verify/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m1-r1.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m2-r1.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m3-r1.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m4-r1.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/proposals/2026-05-01-workflow-refactor.md --path docs/workflows.md --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-select-validation.py --path scripts/test-skill-validator.py --path skills/ci/SKILL.md --path skills/learn/SKILL.md --path skills/proposal-review/SKILL.md --path skills/proposal/SKILL.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m4-r1.md`
  - `bash scripts/ci.sh --mode explicit --path .codex/skills/ci/SKILL.md --path .codex/skills/learn/SKILL.md --path .codex/skills/proposal-review/SKILL.md --path .codex/skills/proposal/SKILL.md --path .codex/skills/verify/SKILL.md --path .codex/skills/workflow/SKILL.md --path AGENTS.md --path CONSTITUTION.md --path README.md --path dist/adapters/claude/.claude/skills/ci/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/proposal-review/SKILL.md --path dist/adapters/claude/.claude/skills/proposal/SKILL.md --path dist/adapters/claude/.claude/skills/verify/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/codex/.agents/skills/ci/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/proposal-review/SKILL.md --path dist/adapters/codex/.agents/skills/proposal/SKILL.md --path dist/adapters/codex/.agents/skills/verify/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/ci/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/proposal/SKILL.md --path dist/adapters/opencode/.opencode/skills/verify/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m1-r1.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m2-r1.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m3-r1.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m4-r1.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/proposals/2026-05-01-workflow-refactor.md --path docs/workflows.md --path scripts/test-artifact-lifecycle-validator.py --path scripts/test-select-validation.py --path scripts/test-skill-validator.py --path skills/ci/SKILL.md --path skills/learn/SKILL.md --path skills/proposal-review/SKILL.md --path skills/proposal/SKILL.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md`
  - `git diff --check --`
  - Selected check IDs: `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, `selector.regression`.
- 2026-05-03 final explain-change and PR-handoff checks passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-01-workflow-refactor.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md --path docs/changes/2026-05-03-workflow-refactor/review-log.md --path docs/changes/2026-05-03-workflow-refactor/review-resolution.md --path docs/changes/2026-05-03-workflow-refactor/reviews/code-review-m4-r1.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - `git diff --check --`
  - Selected check IDs: `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`.
- 2026-05-03 post-merge lifecycle closeout checks passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-03-workflow-refactor.md --path docs/changes/2026-05-03-workflow-refactor/change.yaml --path docs/changes/2026-05-03-workflow-refactor/explain-change.md`
  - `git diff --check --`
  - Selected check IDs: `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`.

## Outcome and Retrospective

Implementation, review, verify, explain-change, PR handoff, and merged PR #26 are complete. The refactor is now the active workflow baseline, with the project-map lifecycle mechanics and final learn artifact model left as focused follow-ups.

## Readiness

Lifecycle complete through merged PR #26.
