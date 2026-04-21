# Workflow stage autoprogression rationale

## Summary

This explanation covers the workflow-stage autoprogression feature stack from `900f0b0` through `3215bcb`.

The change adds a bounded v1 autoprogression contract for this repository's workflow, aligns the governing workflow surfaces and canonical/generated skills with that contract, fixes the repo-wide smoke wrapper so generated `.codex/skills/` output is not misclassified as authored lifecycle-managed source, and closes the initiative itself during verify once the on-branch outcome is known.

The feature is mostly workflow-contract and contributor-guidance work rather than runtime product behavior. The large file count comes from aligning authoritative docs and canonical/generated skill surfaces, not from introducing a new workflow router or runtime subsystem.

## Problem

The repository already had a stage model, but it still paused between known downstream gates in ways that made the user act as a manual router:

- after `implement`, the next required gate was already `code-review`, but agents still waited for another explicit request;
- after `pr`, the repository still treated PR creation like a confirmation gate instead of the stage's normal action;
- authoring stages such as `proposal`, `spec`, and `architecture` did not consistently hand off into their matching review stages;
- direct one-stage requests and workflow-managed completion flows were not clearly distinguished across stage-local skills;
- repo-wide smoke validation failed once generated `.codex/skills/` output entered authored-artifact lifecycle validation.

The approved direction was to remove only redundant pauses that the workflow could already classify safely, while keeping fast-lane and bugfix execution explicit-step and keeping review-only requests isolated by default.

## Decision trail

| Artifact | Decision carried into the change | How it shaped the diff |
| --- | --- | --- |
| [`2026-04-21-workflow-stage-autoprogression.md`](../proposals/2026-04-21-workflow-stage-autoprogression.md) | Use a general autoprogression policy instead of one-off exceptions, but apply it only to workflow-managed completion flows, not review-only requests. | The diff updates the workflow contract and skills to carry lane-aware downstream handoffs and stop conditions rather than adding isolated stage hacks. |
| [`workflow-stage-autoprogression.md`](../../specs/workflow-stage-autoprogression.md) | Bound v1 to full-feature execution from `implement` through `pr` plus `proposal/spec/architecture -> matching review`, keep direct `pr` in scope, preserve conditional `ci`, and keep `learn` advice-only. | The diff aligns workflow docs and stage-local skills to that exact lane model and avoids broadening fast-lane or bugfix behavior. |
| [`workflow-stage-autoprogression.test.md`](../../specs/workflow-stage-autoprogression.test.md) | Use manual contract review plus repo-owned smoke checks instead of inventing a workflow router or synthetic orchestration harness. | The diff emphasizes guidance alignment, generated-skill synchronization, and `bash scripts/ci.sh` as the main proof surfaces. |
| [`2026-04-21-workflow-stage-autoprogression.md`](../architecture/2026-04-21-workflow-stage-autoprogression.md) | Keep the mechanism guidance- and skill-driven, with no new persistence, no second readiness registry, and no executable router in v1. | The diff changes canonical skills and the thin CI wrapper rather than adding a new runtime subsystem. |
| [`2026-04-21-workflow-stage-autoprogression.md`](../plans/2026-04-21-workflow-stage-autoprogression.md) | Split work into workflow/governance alignment, execution-stage skill alignment, and authoring/review alignment plus repo-wide smoke proof. | The branch lands as M1 (`900f0b0`, `5e460b7`, `769dbb5`), M2 (`776ae86`), M3 (`7fe7e5a`), review-resolution (`a4e1c67`), verify-readiness sync (`d15ce0d`), and verify closeout (`3215bcb`). |

## Milestone map

| Milestone or stage | Commits | Outcome |
| --- | --- | --- |
| M1 | `900f0b0`, `5e460b7`, `769dbb5` | Added the proposal/spec/architecture/plan/test-spec trail, aligned the governing workflow surfaces and shared workflow skill, tightened continuation from `MAY` to `MUST`, and removed `learn` from default auto-run lane summaries. |
| M2 | `776ae86` | Aligned execution-stage skills so the full-feature lane expresses `implement -> code-review -> verify -> ci/explain-change -> pr`, keeps direct stage requests isolated where required, and treats `pr` as an open/submit stage. |
| M3 | `7fe7e5a` | Added bounded authoring-to-review handoff wording to proposal/spec/architecture skills and their review counterparts, and fixed `scripts/ci.sh` so generated `.codex/skills/` output is validated by drift checks instead of authored-artifact lifecycle validation. |
| Review-resolution | `a4e1c67` | Normalized stale settled-state readiness in the active test spec after code-review correctly flagged it. |
| Verify lifecycle sync | `d15ce0d`, `3215bcb` | Synced the active plan from post-code-review state into verify, then moved the initiative from `Active` to `Done` once the verified on-branch outcome was known. |

## Diff rationale by area

| Area | Files | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- | --- |
| Durable feature artifacts | [`2026-04-21-workflow-stage-autoprogression.md`](../proposals/2026-04-21-workflow-stage-autoprogression.md), [`workflow-stage-autoprogression.md`](../../specs/workflow-stage-autoprogression.md), [`workflow-stage-autoprogression.test.md`](../../specs/workflow-stage-autoprogression.test.md), [`2026-04-21-workflow-stage-autoprogression.md`](../architecture/2026-04-21-workflow-stage-autoprogression.md), [`2026-04-21-workflow-stage-autoprogression.md`](../plans/2026-04-21-workflow-stage-autoprogression.md) | Added the full proposal/spec/test-spec/architecture/plan trail and kept the plan current through implementation, code review, verify, and closeout. | The repository needed tracked workflow memory and truthful lifecycle state, not chat-only stage decisions. | Proposal, spec, architecture, test spec, plan; `CONSTITUTION.md` lifecycle rules | Review history in the plan; final `docs/plan.md` closeout; validator checks over the active test spec and plan |
| Shared workflow and governance surfaces | [`specs/rigorloop-workflow.md`](../../specs/rigorloop-workflow.md), [`docs/workflows.md`](../workflows.md), [`AGENTS.md`](../../AGENTS.md), [`CONSTITUTION.md`](../../CONSTITUTION.md), [`skills/workflow/SKILL.md`](../../skills/workflow/SKILL.md), [`.codex/skills/workflow/SKILL.md`](../../.codex/skills/workflow/SKILL.md) | Added the bounded v1 autoprogression rule, isolated-vs-workflow-managed distinction, advice-only `learn`, and the “continue automatically to the next eligible downstream stage” rule. | Contributors needed one consistent shared source for lane-aware continuation before stage-local skills could follow it safely. | Spec `R1`-`R3`, `R5`, `R8`, `R10`; plan M1 | `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; grep-based wording checks recorded in the plan |
| Full-feature execution stages | [`skills/implement/SKILL.md`](../../skills/implement/SKILL.md), [`skills/code-review/SKILL.md`](../../skills/code-review/SKILL.md), [`skills/verify/SKILL.md`](../../skills/verify/SKILL.md), [`skills/ci/SKILL.md`](../../skills/ci/SKILL.md), [`skills/explain-change/SKILL.md`](../../skills/explain-change/SKILL.md), [`skills/pr/SKILL.md`](../../skills/pr/SKILL.md), [`skills/learn/SKILL.md`](../../skills/learn/SKILL.md), matching [`.codex/skills/`](../../.codex/skills/) files | Made the full-feature path explicit from `implement` through `pr`, kept direct review/verify/explain requests isolated, and kept `learn` advice-only. | The spec required lane-aware downstream gates and direct-`pr` behavior without expanding fast-lane or bugfix execution. | Spec `R1d`, `R3`-`R3f`, `R6`, `R8c`, `R8d`; plan M2 | Generated-skill drift checks; manual contract review per `T2`, `T4`, `T5`, `T6`; `bash scripts/ci.sh` |
| Authoring-to-review stages | [`skills/proposal/SKILL.md`](../../skills/proposal/SKILL.md), [`skills/proposal-review/SKILL.md`](../../skills/proposal-review/SKILL.md), [`skills/spec/SKILL.md`](../../skills/spec/SKILL.md), [`skills/spec-review/SKILL.md`](../../skills/spec-review/SKILL.md), [`skills/architecture/SKILL.md`](../../skills/architecture/SKILL.md), [`skills/architecture-review/SKILL.md`](../../skills/architecture-review/SKILL.md), matching [`.codex/skills/`](../../.codex/skills/) files | Added explicit `proposal/spec/architecture -> matching review` handoffs and kept review-to-next-authoring transitions isolated and out of scope. | The approved v1 scope includes only authoring-to-review automation upstream of `implement`; it intentionally does not auto-start `spec`, `architecture`, or `plan` from review gates. | Spec `R2c`-`R2g`, `R7`; architecture interfaces and failure modes; plan M3 | Manual `T3` review; generated-skill drift proof; repo-wide smoke validation |
| CI wrapper and generated-output boundary | [`scripts/ci.sh`](../../scripts/ci.sh) | Filtered generated `.codex/skills/*` paths out of explicit-path authored-artifact lifecycle validation. | Repo-wide smoke proof was failing for the right reason: generated output should be checked by `build-skills.py --check`, not by authored lifecycle validation. The correct fix was to narrow the wrapper, not weaken the validator. | Architecture generated-boundary rule; plan M3 discovery and decision log | `bash scripts/ci.sh` before/after; active-plan validation notes; final smoke pass |
| Review and verify lifecycle closeout | [`workflow-stage-autoprogression.test.md`](../../specs/workflow-stage-autoprogression.test.md), [`2026-04-21-workflow-stage-autoprogression.md`](../plans/2026-04-21-workflow-stage-autoprogression.md), [`docs/plan.md`](../plan.md) | Removed stale `Ready for implement` wording from the active test spec, synced the plan to post-code-review and verify state, and closed the initiative to `Done` in both the plan body and index. | The repository's lifecycle validator and verify rules require settled artifacts and plan/index bookkeeping to stay truthful after each gate. | Verify lifecycle rules in `CONSTITUTION.md`; plan closeout precedent; plan/test-spec lifecycle contracts | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `bash scripts/ci.sh`; manual review of `docs/plan.md` and plan-body closeout surfaces |

## Tests added or changed

This feature did not add a new executable workflow router or runtime behavior harness. Its proof surface is therefore mostly tracked contract artifacts plus repository-owned smoke validation.

- [`workflow-stage-autoprogression.test.md`](../../specs/workflow-stage-autoprogression.test.md) was added as the tracked test plan. It maps `R1`-`R10a`, `E1`-`E10`, and `EC1`-`EC14` into manual and smoke checks across the workflow docs, stage-local skills, generated skill mirror, and CI wrapper.
- No new runtime test suite was added because the approved architecture explicitly kept executable orchestration out of scope for v1.
- The main executable tests reused by this feature were existing repo-owned validation surfaces:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`

That test level is appropriate because the feature changes contributor workflow contracts and stage guidance, not product runtime logic. The critical failure modes were wording drift across skills and incorrect smoke-wrapper behavior, both of which are covered by the repository's skill and CI validation surfaces.

## Verification evidence

Final verification was run against the branch tip through `3215bcb`.

Commands run:

- `python scripts/validate-skills.py`
  - pass
  - important output: `validated 22 skill files under .../skills`
- `python scripts/build-skills.py --check`
  - pass
  - important output: `generated skills are in sync under .../.codex/skills`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-stage-autoprogression.test.md --path docs/plans/2026-04-21-workflow-stage-autoprogression.md`
  - pass
  - important output: `validated 6 artifact files in explicit-paths mode`
- `bash scripts/ci.sh`
  - pass
  - important output: repo-owned CI wrapper passed, including skill validation, skill fixtures, generated-skill drift check, artifact lifecycle validator fixtures, and tracked-diff lifecycle validation
- `git diff --check 776ae86..HEAD -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md skills .codex/skills scripts/ci.sh docs/plans/2026-04-21-workflow-stage-autoprogression.md specs/workflow-stage-autoprogression.test.md`
  - pass during code-review rerun
- `git diff --check -- docs/plan.md docs/plans/2026-04-21-workflow-stage-autoprogression.md`
  - pass during verify closeout

Manual checks:

- reviewed the shared workflow surfaces to confirm full-feature execution stays bounded and `learn` remains advice-only;
- reviewed execution-stage and authoring/review-stage skills to confirm direct isolated requests remain isolated and review-to-next-authoring transitions remain out of scope;
- confirmed `docs/plan.md` and the plan body now agree that the initiative is `Done` on-branch while downstream `explain-change` and `pr` remain next workflow stages.

Validation boundary:

- Hosted GitHub Actions CI was not observed from this environment, so this explanation does not claim hosted CI passed.
- Two unrelated untracked proposal drafts remain in the working tree and stayed out of every validation scope.

## Alternatives rejected

- Broadening v1 into fast-lane or bugfix execution autoprogression.
  - Rejected because the approved spec intentionally confines automation to full-feature execution plus authoring-to-review handoffs.
- Adding a repo-owned workflow router now.
  - Rejected because the approved architecture keeps v1 guidance- and skill-driven and treats any executable router as a separate future decision.
- Treating direct `pr` as draft-only or confirmation-only behavior.
  - Rejected because the accepted proposal and approved spec define `pr` as the stage that opens the PR when readiness passes.
- Relaxing the artifact lifecycle validator to allow generated `.codex/skills/` paths.
  - Rejected because the validator was correct; the bug was in the wrapper's choice of authored paths.
- Leaving the active test spec or plan in stale post-implementation state.
  - Rejected during code-review and verify because the lifecycle contract requires settled artifacts and plan/index bookkeeping to stay truthful.

## Scope control

This feature intentionally did not:

- add merge, deploy, release, or destructive Git automation;
- broaden autoprogression into fast-lane or bugfix execution;
- auto-continue from `proposal-review` into `spec`, from `spec-review` into `architecture` or `test-spec`, or from `architecture-review` into `plan`;
- add persistent workflow state or a second readiness registry;
- add network-dependent orchestration or hosted-CI assumptions;
- hand-edit generated `.codex/skills/` outside the normal regeneration path.

## Risks and follow-ups

- Hosted CI remains unobserved from this environment.
- The current work is on `feat/artifact-status-lifecycle-ownership`, which already exists remotely. The `pr` stage should verify whether that updates an existing PR or whether a new review branch is needed for this feature.
- Two unrelated untracked proposal drafts remain out of scope and must stay out of any PR:
  - [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md)
  - [`2026-04-20-workflow-stage-handoff-clarity.md`](../proposals/2026-04-20-workflow-stage-handoff-clarity.md)

## PR-ready summary

- Added the full proposal/spec/test-spec/architecture/plan trail for workflow-stage autoprogression.
- Aligned the governing workflow surfaces and canonical/generated skills to the approved bounded v1 autoprogression contract.
- Fixed the CI smoke wrapper so generated `.codex/skills/` output is validated by drift checks instead of authored-artifact lifecycle validation.
- Normalized the active test spec and plan lifecycle state during code-review and verify so settled artifacts stayed truthful.
- Closed the initiative to `Done` during verify because the on-branch implementation outcome was already known.
