# Workflow stage autoprogression plan

- Status: done
- Owner: maintainer + Codex
- Start date: 2026-04-21
- Last updated: 2026-04-21
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved workflow-stage autoprogression contract as a small, reviewable guidance-and-skill change.

This initiative should remove redundant user-confirmation pauses only where the repository already knows the next stage and no new user decision is needed:

- full-feature execution flow from `implement` through `pr`; and
- authoring-to-review handoffs for `proposal`, `spec`, and `architecture`.

The implementation must stay inside the approved v1 boundary:

- no executable workflow router;
- no persistent workflow state;
- no fast-lane or bugfix execution autoprogression;
- no merge, release, deploy, or destructive Git automation.

## Source artifacts

- Proposal: `docs/proposals/2026-04-21-workflow-stage-autoprogression.md`
- Spec: `specs/workflow-stage-autoprogression.md`
- Spec-review findings carried into this plan:
  - direct `pr` remains in scope for v1 and still opens the PR when readiness passes;
  - full-feature execution autoprogression is bounded from `implement` through `pr`;
  - upstream of `implement`, v1 covers only `proposal/spec/architecture -> matching review`;
  - review-to-next-authoring transitions remain out of scope;
  - the full-feature post-`verify` path is lane-aware and preserves the conditional `ci -> explain-change -> pr` chain;
  - advice-only stages such as `learn` remain non-automatic by default.
- Architecture: `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
- Architecture-review findings carried into this plan:
  - the architecture artifact had to be normalized from `draft` to `approved` before planning relied on it;
  - invocation-context handling is guidance- and skill-driven rather than router-driven;
  - fast-lane and bugfix execution remain intentionally outside v1 automation scope.
- Related workflow and ADR context:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `docs/adr/ADR-20260419-repository-source-layout.md`
- Test spec: `specs/workflow-stage-autoprogression.test.md`

## Context and orientation

- The authoritative workflow lane and stage model already lives in:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
- The approved architecture keeps this change small:
  - no repo-owned workflow router;
  - no persistent workflow state;
  - no second readiness registry;
  - stage-local behavior expressed through canonical skills plus workflow guidance.
- The main authored implementation surfaces are expected to be:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `skills/workflow/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/ci/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
- `.codex/skills/` remains generated output. Regenerate it; do not hand-edit it.
- Existing repo-owned proof surfaces already exist for skill/generation drift:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`
- The approved proposal, approved spec, approved architecture, and this new plan currently exist only as local worktree artifacts. Downstream stages must not rely on them as authoritative repository state until they are tracked.
- Two unrelated local proposal drafts remain out of scope:
  - `docs/proposals/2026-04-20-docs-changes-usage-policy.md`
  - `docs/proposals/2026-04-20-workflow-stage-handoff-clarity.md`

## Non-goals

- Build a repo-owned executable workflow router, queue, or persistent state store.
- Change fast-lane or bugfix execution behavior in v1.
- Auto-run `learn` by default.
- Change stage order outside the approved autoprogression contract.
- Add merge, release, deploy, tag publication, branch deletion, history rewrite, or rollback automation.
- Expand v1 into `proposal-review -> spec`, `spec-review -> architecture`, or `architecture-review -> plan` autoprogression.
- Pull the two unrelated local proposal drafts into this initiative.

## Pre-implementation prerequisites

- Track the accepted proposal, approved spec, approved architecture, and this plan before `test-spec` or `implement` relies on them as authoritative repository state:
  - `docs/proposals/2026-04-21-workflow-stage-autoprogression.md`
  - `specs/workflow-stage-autoprogression.md`
  - `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
  - `docs/plans/2026-04-21-workflow-stage-autoprogression.md`
- Create `specs/workflow-stage-autoprogression.test.md` after `plan-review` and before implementation.
- Keep the two unrelated local proposal drafts out of scope and out of any later PR.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R2g`, `R9`-`R10a` | `specs/rigorloop-workflow.md`, `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, `skills/workflow/SKILL.md` |
| `R3`-`R3f`, `R5`, `R7`, `R8a`-`R8d` | `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/ci/SKILL.md`, `skills/explain-change/SKILL.md`, `skills/pr/SKILL.md`, `skills/learn/SKILL.md` |
| `R2c`-`R2g`, `R7`, `R9` | `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/workflow/SKILL.md` |
| `R6`-`R6c` | `skills/pr/SKILL.md`, `skills/workflow/SKILL.md`, workflow guidance surfaces, readiness wording |
| `EC1`-`EC14` and acceptance criteria | test spec coverage plus manual scenario checks over workflow docs, canonical skills, generated `.codex/skills/`, and repo-owned validation commands |

## Milestones

### M1. Align the authoritative workflow and governance surfaces

- Goal:
  - Encode the bounded v1 autoprogression contract in the repository's authoritative workflow and shared continuation surfaces before stage-local execution behavior is updated.
- Requirements:
  - `R1`-`R2g`, `R5`, `R8c`, `R8d`, `R9`, `R10`, `R10a`
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `skills/workflow/SKILL.md`
  - generated `.codex/skills/`
- Dependencies:
  - approved spec
  - approved architecture
  - tracked-source-artifact prerequisite must be satisfied before downstream stages treat this milestone as authoritative repository state
- Tests to add/update:
  - the future test spec should cover:
    - workflow-managed versus isolated-stage classification;
    - full-feature-only execution autoprogression scope;
    - direct `pr` remaining in scope;
    - conditional `verify -> ci/explain-change -> pr`;
    - advice-only `learn`;
    - non-goals for fast-lane and bugfix execution.
- Implementation steps:
  - update `specs/rigorloop-workflow.md` so workflow summaries and stage descriptions match the approved autoprogression contract;
  - update `docs/workflows.md` with the short operational summary for bounded v1 autoprogression;
  - update `AGENTS.md` and `CONSTITUTION.md` where repository-level workflow guidance changes;
  - update `skills/workflow/SKILL.md` so the shared lane, invocation-context, and generic continuation-rule guidance matches the approved contract before stage-local skills inherit it;
  - regenerate `.codex/skills/` after canonical workflow-skill changes;
  - remove any stale wording that still implies universal manual stage re-invocation or accidental fast-lane/bugfix expansion.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'workflow-managed|isolated|direct `pr`|fast-lane|bugfix|learn|ci' specs/rigorloop-workflow.md docs/workflows.md AGENTS.md CONSTITUTION.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md skills/workflow/SKILL.md .codex/skills`
- Expected observable result:
  - the repository's workflow contract, short guidance, and shared workflow skill agree on where autoprogression applies in v1 and where explicit invocation remains the default.
- Commit message: `M1: align workflow autoprogression guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - workflow summaries may drift from the approved feature spec;
  - guidance may accidentally imply fast-lane or bugfix automation in v1.
- Rollback/recovery:
  - revert the workflow and governance guidance files together;
  - restore the prior explicit-step wording if a narrower rewrite is needed.

### M2. Align full-feature execution-stage skills and direct-PR behavior

- Goal:
  - Make the stage-local behavior for full-feature execution match the approved `implement`-through-`pr` autoprogression contract.
- Requirements:
  - `R1`, `R1b`-`R1d`, `R2`, `R2a`, `R2b`, `R2ba`, `R3`-`R3f`, `R5`, `R6`-`R6c`, `R7`, `R8a`-`R8d`, `R9`
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/ci/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
  - generated `.codex/skills/`
- Dependencies:
  - M1 guidance surfaces should be stable first so stage skills inherit the same vocabulary and scope boundaries
- Tests to add/update:
  - the future test spec should cover:
    - `implement -> code-review`;
    - `code-review <-> review-resolution`;
    - `code-review -> verify`;
    - `verify -> ci` when the workflow contract elevates `ci`;
    - `verify -> explain-change` otherwise;
    - `ci -> explain-change -> pr`;
    - direct `pr` opening the PR when ready;
    - direct `verify` remaining isolated;
    - `learn` remaining non-automatic.
- Implementation steps:
  - update the workflow skill to carry and surface workflow-managed, isolated, and direct-`pr` invocation context;
  - update `implement`, `code-review`, `verify`, `ci`, `explain-change`, and `pr` so they no longer wait for redundant user re-invocation when the full-feature next stage is already known;
  - keep direct `pr` as a submit/open stage rather than a draft-only stage when readiness passes;
  - keep direct `code-review`, `verify`, and `explain-change` isolated by default;
  - keep `learn` advice-only in v1;
  - regenerate `.codex/skills/`.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'workflow-managed|isolated|direct `pr`|code-review|verify|ci|explain-change|learn' skills/workflow/SKILL.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/ci/SKILL.md skills/explain-change/SKILL.md skills/pr/SKILL.md skills/learn/SKILL.md .codex/skills`
  - `git diff --check -- skills .codex/skills`
- Expected observable result:
  - full-feature execution skills continue automatically where the v1 contract requires it, `pr` opens directly when ready, and isolated/direct-stage exceptions remain explicit.
- Commit message: `M2: align workflow autoprogression execution skills`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - stage-local wording may diverge across execution skills;
  - `pr` behavior may still read as draft-only if readiness wording is not updated consistently.
- Rollback/recovery:
  - revert the execution-stage skill changes together;
  - regenerate `.codex/skills/` after rollback and rerun drift checks.

### M3. Align authoring-to-review skills and complete repo-wide proof

- Goal:
  - Finish upstream handoff coverage for `proposal`, `spec`, and `architecture`, then prove the repository guidance set is internally consistent.
- Requirements:
  - `R2c`-`R2g`, `R7`, `R8a`-`R8d`, `R9`, `R10`
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/workflow/SKILL.md` if shared wording still needs alignment
  - `scripts/ci.sh` if repo-wide smoke proof needs a wrapper fix for generated-output handling
  - generated `.codex/skills/`
- Dependencies:
  - M1 and M2 should land first so shared vocabulary and execution-stage behavior are already stable
- Tests to add/update:
  - the future test spec should cover:
    - `proposal -> proposal-review`;
    - `spec -> spec-review`;
    - `architecture -> architecture-review`;
    - standalone review-only requests staying isolated;
    - review-to-next-authoring transitions remaining out of scope.
- Implementation steps:
  - update proposal/spec/architecture authoring skills so workflow-managed completion flows hand off into the matching review stage automatically when that review is the next required or default downstream step;
  - update the paired review skills so standalone review-only requests remain isolated unless the user asks to continue;
  - keep review-to-next-authoring transitions explicitly out of scope in stage-local guidance;
  - if repo-wide smoke proof still fails because generated `.codex/skills/` paths are being treated as authored artifacts, narrow the CI-wrapper explicit-path scope so generated drift stays enforced by `build-skills.py --check` instead of the authored-artifact lifecycle validator;
  - regenerate `.codex/skills/`;
  - run repo-wide validation and manual scenario checks covering the approved examples and edge cases.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`
  - `rg -n "proposal-review|spec-review|architecture-review|workflow-managed|isolated|review-only" skills/proposal/SKILL.md skills/proposal-review/SKILL.md skills/spec/SKILL.md skills/spec-review/SKILL.md skills/architecture/SKILL.md skills/architecture-review/SKILL.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md skills .codex/skills`
- Expected observable result:
  - authoring-to-review handoffs behave consistently with the v1 contract, review-only requests remain isolated, and repo-wide validation passes without generated drift.
- Commit message: `M3: finish workflow autoprogression skill alignment`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - authoring skills may accidentally imply `proposal-review -> spec` or similar out-of-scope transitions;
  - generated skill output may drift if regeneration is incomplete.
- Rollback/recovery:
  - revert the authoring/review skill changes together;
  - regenerate `.codex/skills/` from the last known-good canonical sources.

## Validation plan

- Planning change validation:
  - `rg -n "^# Workflow stage autoprogression plan$|^## (Purpose / big picture|Source artifacts|Context and orientation|Non-goals|Pre-implementation prerequisites|Requirements covered|Milestones|Validation plan|Risks and recovery|Dependencies|Progress|Decision log|Surprises and discoveries|Validation notes|Outcome and retrospective|Readiness)$" docs/plans/2026-04-21-workflow-stage-autoprogression.md`
  - `git diff --check -- docs/plan.md docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
  - `git diff --no-index --check -- /dev/null docs/plans/2026-04-21-workflow-stage-autoprogression.md`
- Per-milestone validation is listed inside each milestone and should be copied into the later test spec.
- Final initiative validation should run the repo-owned skill/generation checks and any narrower scenario checks named by the test spec before `verify`.

## Risks and recovery

- Risk: stage-skill guidance diverges from workflow docs and the approved spec.
  - Recovery: keep M1 ahead of skill work, then regenerate `.codex/skills/` and rerun drift checks after every skill milestone.
- Risk: direct `pr` still behaves like a draft-only stage in some surfaces.
  - Recovery: keep `pr` and `workflow` wording paired in the same milestone and treat readiness wording drift as a blocker at code-review.
- Risk: fast-lane, bugfix, or `learn` autoprogression leaks into v1 by implication.
  - Recovery: keep explicit grep-based checks for out-of-scope lane wording and advice-only `learn`.
- Risk: downstream stages rely on local-only proposal/spec/architecture/plan artifacts that are not yet tracked.
  - Recovery: make tracked-source normalization a hard prerequisite before `test-spec` or `implement`.

## Dependencies

- The accepted proposal, approved spec, approved architecture, and this plan must be tracked before `test-spec` or `implement`.
- The accepted proposal, approved spec, approved architecture, this plan, and the active test spec must remain tracked before `implement`.
- `plan-review` must approve this execution split before implementation starts.
- `specs/workflow-stage-autoprogression.test.md` must exist before `implement`.
- `python scripts/build-skills.py` and `python scripts/build-skills.py --check` remain the authoritative generated-skill path; do not hand-edit `.codex/skills/`.
- `bash scripts/ci.sh` remains the repository-wide validation wrapper for final milestone proof.

## Progress

- [x] 2026-04-21: architecture metadata normalized to `approved` in the planning change so this plan relies on a truthful reviewed design.
- [x] 2026-04-21: plan created and indexed under `Active` in `docs/plan.md`.
- [x] 2026-04-21: tracked-source prerequisite satisfied for proposal, spec, architecture, plan, and test spec before downstream implementation reliance.
- [x] 2026-04-21: test spec created at `specs/workflow-stage-autoprogression.test.md`.
- [x] 2026-04-21: M1 completed. The workflow contract, operational summary, repository guidance, and shared workflow skill now agree on bounded v1 autoprogression scope.
- [x] 2026-04-21: M2 completed. The execution-stage skills now express the full-feature downstream chain, direct `pr` opening, isolated review/verification/explanation behavior, and advice-only `learn`.
- [x] 2026-04-21: M3 completed. The authoring/review skills now express the bounded authoring-to-review handoffs, review-only isolation, and repo-wide smoke proof passes without treating generated `.codex/skills/` output as authored lifecycle-managed source.

## Decision log

- 2026-04-21: split implementation into workflow/guidance first, full-feature execution skills second, and authoring-to-review skills last. Reason: this keeps review slices small and makes the highest-risk continuation rules settle before broader skill churn.
- 2026-04-21: excluded executable router work from this plan. Reason: the approved architecture keeps v1 guidance- and skill-driven.
- 2026-04-21: kept fast-lane and bugfix execution out of implementation scope. Reason: the approved spec explicitly narrows v1 to full-feature execution plus authoring-to-review handoffs.
- 2026-04-21: kept M1 limited to shared workflow and governance surfaces plus `skills/workflow/SKILL.md`. Reason: the approved architecture makes `workflow` the owner of lane, invocation-context, and generic continuation rules, while stage-local execution skills remain M2 work.
- 2026-04-21: tightened the shared workflow contract from optional to required continuation when the approved autoprogression rule applies, and removed `learn` from the full-feature lane's default required sequence. Reason: M1 review found those two wording drifts kept manual handoff and automatic `learn` behavior implicitly allowed in the shared surfaces.
- 2026-04-21: removed `learn` from the remaining required/default lifecycle summaries in `docs/workflows.md` and the shared workflow skill's canonical artifact order. Reason: `learn` is advice-only in the approved spec and should not appear as part of the default auto-run lane.
- 2026-04-21: left `skills/workflow/SKILL.md` unchanged in M2. Reason: M1 already carried the shared invocation-context and lane-aware handoff rules, so M2 only needed to align the stage-local execution skills that inherit that contract.
- 2026-04-21: kept M2 focused on execution-stage skill behavior and direct-`pr` semantics, while leaving repo-wide smoke proof to M3. Reason: the approved plan already reserves `bash scripts/ci.sh` as part of the final repo-wide proof milestone rather than the narrower execution-skill alignment slice.
- 2026-04-21: left `skills/workflow/SKILL.md` unchanged in M3. Reason: the shared authoring-to-review and isolated-stage boundary rules were already correct after M1, so M3 only needed stage-local authoring/review alignment plus the repo-wide smoke-proof wrapper fix.
- 2026-04-21: filtered generated `.codex/skills/*` paths out of the CI wrapper's explicit-path artifact lifecycle fallback. Reason: generated-skill drift is already enforced by `build-skills.py --check`, while the lifecycle validator correctly treats generated output as non-authored source.
- 2026-04-21: normalized `specs/workflow-stage-autoprogression.test.md` readiness away from `Ready for implement` once execution advanced into review. Reason: active test specs are settled proof-planning surfaces, and their readiness must not imply earlier pending stages remain.

## Surprises and discoveries

- 2026-04-21: `python scripts/build-skills.py --check` is meaningful milestone proof only after regeneration has completed. The final M1 validation set was rerun sequentially so generated-skill drift evidence reflects the post-sync state.
- 2026-04-21: a local exploratory `bash scripts/ci.sh` run still blocks when tracked-diff explicit-path lifecycle validation sees changed `.codex/skills/*` files as generated outputs rather than authored sources. That repo-wide proof issue is recorded for M3 instead of being silently ignored.
- 2026-04-21: the repo-wide smoke failure did not require relaxing the lifecycle validator itself. A small wrapper fix in `scripts/ci.sh` was enough because generated-skill drift and authored-artifact lifecycle validation are intentionally separate proof surfaces.
- 2026-04-21: independent `code-review` of M3 surfaced a stale settled-state readiness line in `specs/workflow-stage-autoprogression.test.md`. The fix was to keep the test spec active while removing the outdated `implement` handoff wording instead of relaxing lifecycle validation.

## Validation notes

- 2026-04-21: `specs/workflow-stage-autoprogression.test.md` created and reviewed for required section coverage.
- 2026-04-21: tracked-source prerequisite satisfied by moving the proposal, spec, architecture, plan, and test spec into git-tracked state for downstream reliance.
- 2026-04-21: M1 updated `specs/rigorloop-workflow.md`, `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, and `skills/workflow/SKILL.md`, then regenerated `.codex/skills/`.
- 2026-04-21: M1 validation passed with:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'workflow-managed|isolated|direct \`pr\`|fast-lane|bugfix|learn|ci' specs/rigorloop-workflow.md docs/workflows.md AGENTS.md CONSTITUTION.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md skills/workflow/SKILL.md .codex/skills`
- 2026-04-21: M1 review-fix validation passed after tightening `R7d` and making `learn` conditional in the shared workflow skill:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'workflow-managed|isolated|direct \`pr\`|fast-lane|bugfix|learn|ci' specs/rigorloop-workflow.md docs/workflows.md AGENTS.md CONSTITUTION.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- docs/plans/2026-04-21-workflow-stage-autoprogression.md`
- 2026-04-21: M1 learn-consistency validation passed after removing `learn` from the remaining default lifecycle summaries:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n 'workflow-managed|isolated|direct \`pr\`|fast-lane|bugfix|learn|ci' specs/rigorloop-workflow.md docs/workflows.md AGENTS.md CONSTITUTION.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- docs/plans/2026-04-21-workflow-stage-autoprogression.md`
- 2026-04-21: M2 updated `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/ci/SKILL.md`, `skills/explain-change/SKILL.md`, `skills/pr/SKILL.md`, and `skills/learn/SKILL.md`, then regenerated `.codex/skills/`.
- 2026-04-21: M2 targeted validation passed with:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `rg -n -- 'workflow-managed|isolated|direct \`pr\`|code-review|verify|ci|explain-change|learn' skills/workflow/SKILL.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/ci/SKILL.md skills/explain-change/SKILL.md skills/pr/SKILL.md skills/learn/SKILL.md .codex/skills`
  - `git diff --check -- skills .codex/skills`
- 2026-04-21: exploratory repo-wide smoke validation was run early:
  - `bash scripts/ci.sh`
  - result: failed because local explicit-path artifact lifecycle validation blocks changed `.codex/skills/*` paths as generated outputs
  - handling: recorded as an M3 repo-wide-proof discovery rather than treating it as a hidden pass or expanding M2 into CI/lifecycle-validator changes
- 2026-04-21: M3 updated `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture/SKILL.md`, `skills/architecture-review/SKILL.md`, and `scripts/ci.sh`, then regenerated `.codex/skills/`.
- 2026-04-21: M3 targeted validation passed with:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`
  - `rg -n "proposal-review|spec-review|architecture-review|workflow-managed|isolated|review-only" skills/proposal/SKILL.md skills/proposal-review/SKILL.md skills/spec/SKILL.md skills/spec-review/SKILL.md skills/architecture/SKILL.md skills/architecture-review/SKILL.md skills/workflow/SKILL.md .codex/skills`
  - `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md skills .codex/skills scripts/ci.sh`
- 2026-04-21: M3 code-review rerun will include the test-spec readiness fix with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-stage-autoprogression.test.md`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`
  - `git diff --check -- specs/workflow-stage-autoprogression.test.md docs/plans/2026-04-21-workflow-stage-autoprogression.md`
- 2026-04-21: M3 code-review passed after the readiness fix. The review-resolution loop did not require further skill or workflow changes beyond normalizing the active test-spec and plan readiness wording.
- 2026-04-21: verify-stage lifecycle closeout passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-stage-autoprogression.test.md --path docs/plans/2026-04-21-workflow-stage-autoprogression.md`
  - `bash scripts/ci.sh`
  - `git diff --check -- docs/plan.md docs/plans/2026-04-21-workflow-stage-autoprogression.md`
  - manual review -> passed (`docs/plan.md` and this plan body now agree that the initiative is done on-branch while downstream `explain-change` and `pr` remain next workflow stages`)

## Outcome and retrospective

- This plan is done on-branch and now belongs in `docs/plan.md` under `Done`.
- What changed: the feature aligned the workflow contract, governance surfaces, canonical/generated execution skills, authoring-to-review skills, and CI smoke wrapper with the approved bounded v1 autoprogression model.
- What went well: splitting the work into workflow/guidance, execution-skill, and authoring/review slices kept review findings narrow and made it easy to correct wording drift without reopening the broader contract.
- What was harder than expected: the repo-wide smoke proof initially failed because generated `.codex/skills/` output was entering authored-artifact lifecycle validation; the right fix was a thin `scripts/ci.sh` wrapper change, not relaxing the lifecycle validator.
- Spec accuracy: the approved spec held through implementation once v1 scope was narrowed to full-feature execution plus authoring-to-review handoffs. The most important constraint was keeping fast-lane, bugfix, and review-to-next-authoring transitions out of scope.
- Test effectiveness: manual contract review plus generated-skill drift checks were the right proof surface for this guidance-driven feature, and repo-owned smoke validation caught the one real integration issue around generated-output handling and later the stale active test-spec readiness wording.
- Architecture accuracy: the approved guidance-and-skill-driven architecture was sufficient. The feature did not need a router, persistent workflow state, or a second readiness registry.
- Process issues: workflow-managed autoprogression is only safe when lifecycle-managed artifacts stay current after each review gate. The code-review and verify stages both needed explicit plan/test-spec readiness normalization rather than assuming milestone completion notes were enough.
- Follow-up actions: complete `explain-change`, then prepare the PR from the verified branch tip; keep the two unrelated local proposal drafts out of scope.

## Readiness

- This plan is done.
- `plan-review` is complete.
- The tracked-source prerequisite and test spec are in place.
- Implementation, `code-review`, and `verify` are complete through M3.
- `explain-change` is complete at `docs/explain/2026-04-21-workflow-stage-autoprogression.md`.
- The next stage is `pr`.
