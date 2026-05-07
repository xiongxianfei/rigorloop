# Milestone-Aware Review Handoff Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-07
- Last updated: 2026-05-07
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow-governance Markdown, stage skill guidance, static wording checks, generated skill mirrors, and public adapter skill copies. It does not add runtime data flow, storage, network boundaries, deployment behavior, release packaging, schemas, or executable plan-state validation.

## Purpose / Big Picture

Implement the approved milestone-aware handoff contract so workflow-managed full-feature execution does not route a clean non-final milestone review to `verify`.

The intended workflow is:

```text
implement M<n>
-> code-review M<n>
-> review-resolution M<n>, when triggered
-> implement fixes for M<n>, when needed
-> code-review M<n> rerun, when needed
-> close M<n>
-> implement M<n+1>, when another implementation milestone remains
```

`verify` becomes the next stage only after every in-scope implementation milestone is closed and no required review-resolution remains open.

## Source Artifacts

- Proposal: [Milestone-Aware Review Handoff](../proposals/2026-05-07-milestone-aware-review-handoff.md), accepted after clean proposal review on 2026-05-07.
- Spec: [Milestone-Aware Review Handoff](../../specs/milestone-aware-review-handoff.md), approved after clean spec review on 2026-05-07.
- Architecture: not required. The approved change is guidance and static wording checks only, with no new storage model, parser architecture, API, runtime boundary, deployment boundary, or executable plan-state validation.
- Test spec: [Milestone-Aware Review Handoff Test Spec](../../specs/milestone-aware-review-handoff.test.md), active.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for architecture, data flow, runtime flow, or ownership. Orientation comes from the constitution, approved proposal, approved spec, current workflow specs, stage skills, workflow docs, generated-output scripts, and existing static validator patterns.
- Review records: clean proposal and spec reviews settled artifact-locally. No material findings were recorded and no detailed review record is required for those reviews.

## Context and Orientation

- `specs/milestone-aware-review-handoff.md` is the approved source of truth for this change.
- `specs/workflow-stage-autoprogression.md` currently owns the full-feature autoprogression rule that says clean `code-review` proceeds to `verify`; it must become milestone-aware for planned implementation milestones.
- `specs/rigorloop-workflow.md` is the broader lifecycle contract and must preserve existing review-resolution, verify, explain-change, and PR closeout gates while adding the milestone loop.
- `docs/workflows.md` is the short contributor-facing operational summary and currently repeats the clean-review-to-verify shortcut.
- `skills/implement/SKILL.md` already treats implementation as milestone work and needs to state that post-implementation handoff is `review-requested`, not whole-plan verify readiness.
- `skills/code-review/SKILL.md` currently says workflow-managed `clean-with-notes` hands off to `verify`; it must inspect remaining in-scope implementation milestones before routing.
- `skills/plan/SKILL.md` needs explicit plan guidance for one milestone state field, same-milestone review-resolution, and current handoff summaries.
- `skills/workflow/SKILL.md` summarizes the full-feature chain and execution handoff rules; it likely needs the same milestone-aware exception.
- `AGENTS.md` is affected only if the concise root workflow summary would otherwise remain misleading. `CONSTITUTION.md` should remain high-level unless implementation finds a direct governance conflict.
- Canonical authored skills live under `skills/`. Generated Codex runtime mirrors under `.codex/skills/` and public adapter package output under `dist/adapters/` must be refreshed through generators, not hand-edited.
- The first implementation slice must stay guidance/static-check only. Do not add executable plan-state validation or a standalone `review-resolution` skill.
- Do not introduce or revise a plan template in this slice. Any existing template/example-plan cleanup is outside this approved implementation unless the test spec or plan-review identifies it as a blocking contradiction.

## Non-Goals

- Do not redesign the full lifecycle stage order.
- Do not remove `code-review`, `review-resolution`, `verify`, `explain-change`, or `pr`.
- Do not add a new lifecycle stage.
- Do not add a standalone `review-resolution` skill.
- Do not add executable plan-state validation in this first slice.
- Do not require every milestone to be a separate PR.
- Do not treat lifecycle-closeout milestones as unfinished implementation work.
- Do not change fast-lane, bugfix, review-only, direct `pr`, merge, release, deploy, destructive Git, or publishing behavior.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not introduce or revise a plan template in this slice.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R1b`, `R10`-`R10a` | `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `docs/workflows.md`, and `skills/workflow/SKILL.md` full-feature routing guidance |
| `R2`-`R2c` | milestone state vocabulary in workflow specs, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`, and `skills/code-review/SKILL.md` |
| `R3`-`R3b` | `skills/implement/SKILL.md`, workflow specs, and static wording checks for `review-requested` handoff and no implement-owned verify readiness |
| `R4`-`R4d`, `R6`-`R6b` | `skills/code-review/SKILL.md`, workflow specs, handoff summary wording, and static checks for plan inspection, inconclusive state, and no non-final verify handoff |
| `R5`-`R5e` | workflow specs, review-resolution contract references where needed, `skills/code-review/SKILL.md`, `skills/implement/SKILL.md`, and `skills/plan/SKILL.md` same-milestone resolution loop |
| `R7`-`R7b` | workflow specs and plan guidance for plan revision before removing milestones from scope |
| `R8`-`R8d` | plan guidance, code-review output guidance, workflow summary, and static wording checks for current handoff summaries |
| `R9`-`R9b` | workflow specs, plan guidance, and workflow summary distinguishing lifecycle-closeout milestones from implementation milestones |
| `R11`-`R11b` | test spec, skill-validator assertions, and plan validation that first implementation remains guidance/static-check only |
| `AC1`-`AC8` | matching test spec, static validators, selected CI, generated-output drift checks, and final verify evidence |

## Immediate Test-Spec Handoff

`plan-review` must approve this plan before implementation starts. After plan-review, create `specs/milestone-aware-review-handoff.test.md` to map each approved requirement and edge case to concrete proof.

The test spec should require focused static assertions for:

- clean non-final milestone review closing the milestone and routing to `implement <next milestone>`;
- clean final milestone review closing the milestone and routing to `verify`;
- findings routing to review-resolution for the same milestone;
- inconclusive or ambiguous plan state blocking `verify`;
- exactly one `Milestone state` field with the approved allowed values;
- `implementation-complete` and `review-clean` not being milestone state values;
- lifecycle-closeout milestones not blocking verify as implementation milestones;
- first-slice proof staying static and not adding executable plan-state validation;
- generated `.codex/skills/` and adapter output staying derived when canonical skills change.

## Current Handoff Summary

- Current milestone: M3
- Current milestone state: planned
- Last reviewed milestone: M2
- Review status: clean-with-notes
- Remaining in-scope implementation milestones: M3, M4
- Next stage: implement M3
- Verify readiness: not ready
- Reason verify is not ready: implementation milestones M3 and M4 remain open.

## Milestones

### M1. Define Static Proof Surfaces

- Milestone state: closed
- Goal: Add or update the static proof surfaces that will fail until milestone-aware workflow guidance is present and consistent.
- Requirements: `R2`-`R8d`, `R11`-`R11b`, `AC3`-`AC8`.
- Files/components likely touched:
  - `specs/milestone-aware-review-handoff.test.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `specs/rigorloop-workflow.test.md`
  - `scripts/test-skill-validator.py`
  - selector or artifact lifecycle tests only if existing coverage requires a small static assertion update
  - this plan
- Dependencies:
  - plan-review approval
  - matching test spec drafted before implementation
- Tests to add/update:
  - [x] Static assertions for the approved milestone state vocabulary.
  - [x] Static assertions that `implementation-complete` and `review-clean` are not milestone state values in the new guidance.
  - [x] Static red-state assertions that pending `code-review` clean non-final milestone output must name the next implementation milestone, not `verify`.
  - [x] Static red-state assertions that pending `implement` guidance must route post-implementation milestone state to `review-requested`.
  - [x] Static red-state assertions that pending same-milestone review-resolution blocks the next milestone and `verify`.
  - [x] Static assertions that no executable plan-state validation was added in this first slice.
- Implementation steps:
  - Convert the approved spec requirements and edge cases into the matching test spec.
  - Add focused static checks before changing canonical workflow and skill wording.
  - Reuse existing validator test style in `scripts/test-skill-validator.py` where possible.
  - Avoid semantic plan parsing or runtime workflow simulation.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path specs/milestone-aware-review-handoff.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py`
  - `bash scripts/ci.sh --mode explicit --path specs/milestone-aware-review-handoff.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md`
  - `git diff --check -- specs/milestone-aware-review-handoff.test.md specs/workflow-stage-autoprogression.test.md specs/rigorloop-workflow.test.md scripts/test-skill-validator.py docs/plans/2026-05-07-milestone-aware-review-handoff.md`
- Expected observable result: static proof fails against the old non-milestone-aware clean-review handoff and passes only after canonical guidance is aligned.
- Commit message: `M1: add milestone-aware handoff proof`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone state updated to `review-requested` before code-review handoff
  - [x] milestone committed
- Risks:
  - Static wording checks can become brittle if they overfit exact paragraphs instead of required invariant terms.
  - Tests could accidentally become executable plan-state validation.
- Rollback/recovery:
  - Replace brittle exact text assertions with stable term, heading, and forbidden-term checks mapped to the approved test spec.
  - Remove any parser-like plan-state validation and keep that enforcement for a later approved slice.

### M2. Align Authoritative Workflow Contracts

- Milestone state: closed
- Goal: Amend the approved workflow contracts so the source of truth routes clean non-final milestone reviews to the next implementation milestone and final clean reviews to `verify`.
- Requirements: `R1`-`R10a`, `AC1`-`AC4`.
- Files/components likely touched:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/rigorloop-workflow.md`
  - `specs/review-finding-resolution-contract.md` only if the same-milestone finding loop needs cross-spec clarification
  - related test specs from M1
  - this plan
- Dependencies:
  - M1 static proof in place
- Tests to add/update:
  - Adjust only the M1 proof if contract wording exposes a missing requirement trace.
- Implementation steps:
  - Update the full-feature autoprogression rule to inspect the active plan when the plan is milestone-based.
  - Add the single milestone state vocabulary and transition rules.
  - Preserve isolated review, fast-lane, bugfix, direct `pr`, merge, release, deploy, and destructive-action boundaries.
  - Add same-milestone review-resolution wording without creating a standalone skill.
  - Distinguish lifecycle-closeout milestones from implementation milestones for verify readiness.
  - Convert any M1 pending expected-failure assertions for aligned workflow contract surfaces into ordinary passing assertions.
  - Record any deliberately unaffected overlap spec with rationale in this plan.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md`
  - `bash scripts/ci.sh --mode explicit --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md`
  - `git diff --check -- specs/milestone-aware-review-handoff.md specs/workflow-stage-autoprogression.md specs/rigorloop-workflow.md specs/workflow-stage-autoprogression.test.md specs/rigorloop-workflow.test.md scripts/test-skill-validator.py docs/plans/2026-05-07-milestone-aware-review-handoff.md`
- Expected observable result: governing workflow specs no longer imply that a clean review of `M1` makes a multi-milestone plan ready for `verify`.
- Commit message: `M2: align milestone-aware workflow contract`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone state updated to `review-requested` before code-review handoff
  - [x] milestone committed
- Risks:
  - Overlap specs could retain stale `clean-with-notes -> verify` wording.
  - Wording could accidentally weaken review-resolution closeout before verify.
- Rollback/recovery:
  - Revert contract wording and rerun lifecycle validation if the milestone-aware rule conflicts with a higher-priority artifact.
  - Keep review-resolution closeout text explicit and restore older surrounding text if the new wording broadens scope.

### M3. Align Operating Docs and Stage Skills

- Milestone state: planned
- Goal: Update contributor guidance and authored skills so `implement`, `code-review`, `plan`, and workflow orchestration use the approved milestone loop.
- Requirements: `R3`-`R10a`, `AC5`-`AC6`.
- Files/components likely touched:
  - `docs/workflows.md`
  - `AGENTS.md` if the root workflow summary needs a concise milestone-aware reminder
  - `CONSTITUTION.md` only if implementation reveals a direct governance conflict
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `scripts/test-skill-validator.py`
  - this plan
- Dependencies:
  - M1 static proof in place
  - M2 workflow contract alignment
- Tests to add/update:
  - Skill-validator assertions for the post-implement `review-requested` state.
  - Skill-validator assertions for `code-review` non-final clean review routing.
  - Skill-validator assertions for current handoff summary fields.
  - Static checks that `implementation-complete` and `review-clean` remain evidence descriptions, not milestone state values.
- Implementation steps:
  - Update `docs/workflows.md` to summarize the milestone-aware loop and preserve ordinary full-feature downstream gates.
  - Update `skills/implement/SKILL.md` so milestone implementation handoff is not treated as full milestone closeout or whole-plan verify readiness.
  - Update `skills/code-review/SKILL.md` so `clean-with-notes` closes the reviewed milestone directly when no review-resolution is required, then routes to the next in-scope implementation milestone or `verify` depending on remaining milestones.
  - Update `skills/plan/SKILL.md` to require one milestone state field and current handoff summaries for milestone-based plans.
  - Update `skills/workflow/SKILL.md` where its full-feature chain would otherwise conflict with the new milestone-aware rule.
  - Convert any remaining M1 pending expected-failure skill assertions into ordinary passing assertions after authored skill guidance is aligned.
  - Decide whether `AGENTS.md` needs one concise reminder; if unchanged, record unaffected rationale in this plan.
  - Leave `CONSTITUTION.md` unchanged unless a direct conflict is found; record unaffected rationale if no edit is needed.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path AGENTS.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/plan/SKILL.md --path skills/workflow/SKILL.md --path scripts/test-skill-validator.py`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path AGENTS.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/plan/SKILL.md --path skills/workflow/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md`
  - `rg -n 'clean-with-notes.*verify|code-review -> verify|implementation-complete|review-clean|review-requested|resolution-needed|lifecycle-closeout' docs/workflows.md AGENTS.md CONSTITUTION.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/plan/SKILL.md skills/workflow/SKILL.md`
  - `git diff --check -- docs/workflows.md AGENTS.md CONSTITUTION.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/plan/SKILL.md skills/workflow/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-07-milestone-aware-review-handoff.md`
- Expected observable result: stage skills and operating docs consistently route milestone-based clean reviews through the next in-scope implementation milestone until the final implementation milestone is closed.
- Commit message: `M3: align milestone-aware workflow skills`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone state updated to `review-requested` before code-review handoff
  - [ ] milestone committed
- Risks:
  - Root guidance can become too detailed for `AGENTS.md`.
  - Skill wording can accidentally make clean review stop instead of continuing to the next valid stage.
- Rollback/recovery:
  - Keep detailed routing rules in specs and `docs/workflows.md`; reduce `AGENTS.md` to a pointer if it becomes verbose.
  - Restore autoprogression wording while preserving the milestone-aware next-stage decision.

### M4. Refresh Generated Output and Close Implementation Evidence

- Milestone state: planned
- Goal: Propagate canonical skill changes through generated outputs and prepare the implementation slice for final code review.
- Requirements: `R11`-`R11b`, `AC6`-`AC8`, generated-output alignment for changed skills.
- Files/components likely touched:
  - generated `.codex/skills/` mirrors for changed canonical skills
  - generated public adapter skill output under `dist/adapters/`
  - generated adapter manifests if generator output changes them
  - `docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml`
  - this plan
- Dependencies:
  - M1 through M3 complete
- Tests to add/update:
  - No generator behavior test is expected. Add or adjust generated-output tests only if generator behavior changes unexpectedly.
- Implementation steps:
  - Create the baseline change-local artifact pack with `docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` plus durable Markdown reasoning when implementation evidence is ready.
  - Run `python scripts/build-skills.py` after canonical skill changes.
  - Run `python scripts/build-adapters.py --version 0.1.1` after canonical skill changes.
  - Inspect generated diffs for expected skill-content propagation only.
  - Do not patch generated files manually.
  - Update this plan's progress, current handoff summary, validation notes, decisions, and surprises before code-review.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/plan/SKILL.md --path skills/workflow/SKILL.md --path .codex/skills/implement/SKILL.md --path .codex/skills/code-review/SKILL.md --path .codex/skills/plan/SKILL.md --path .codex/skills/workflow/SKILL.md --path dist/adapters/codex/.agents/skills/implement/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/plan/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/claude/.claude/skills/implement/SKILL.md --path dist/adapters/claude/.claude/skills/code-review/SKILL.md --path dist/adapters/claude/.claude/skills/plan/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/implement/SKILL.md --path dist/adapters/opencode/.opencode/skills/code-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/plan/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md`
  - `git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-07-milestone-aware-review-handoff docs/plans/2026-05-07-milestone-aware-review-handoff.md`
- Expected observable result: generated Codex and public adapter outputs match canonical skill guidance, change-local metadata captures implementation evidence, and the implementation slice is ready for milestone `code-review`.
- Commit message: `M4: refresh milestone-aware generated guidance`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone state updated to `review-requested` before code-review handoff
  - [ ] milestone committed
- Risks:
  - Generated output may include broader churn if generators derive related metadata from changed skill text.
  - Change metadata can drift from the actual implementation if created too early.
- Rollback/recovery:
  - Revert generated output and rerun generator check commands from canonical sources.
  - Regenerate change metadata from the final diff before verify if implementation scope changes.

### Lifecycle Closeout Gates. Review, Verify, Explain, PR

- Milestone type: lifecycle-closeout
- Goal: Complete required downstream gates after all in-scope implementation milestones are closed.
- Requirements: all approved requirements and acceptance criteria.
- Files/components likely touched:
  - `docs/plan.md`
  - this plan
  - `docs/changes/2026-05-07-milestone-aware-review-handoff/review-log.md` and detailed review records if detailed-record triggers apply
  - `docs/changes/2026-05-07-milestone-aware-review-handoff/review-resolution.md` only if material findings or another trigger requires it
  - `docs/changes/2026-05-07-milestone-aware-review-handoff/explain-change.md`
  - final changed authored, generated, and test surfaces from M1 through M4
- Dependencies:
  - all in-scope implementation milestones closed
  - code-review complete
  - review-resolution closed when triggered
- Tests to add/update:
  - None expected unless code-review, review-resolution, or verify identifies a missing proof.
- Implementation steps:
  - Run code-review for the completed implementation milestone or aggregate slice.
  - If findings exist, keep the workflow on the same milestone until findings are dispositioned, fixes are validated, and required re-review or owner closeout is complete.
  - Run final `verify` only after all in-scope implementation milestones are closed.
  - Create or update explain-change evidence.
  - Synchronize this plan body and `docs/plan.md` to Done before PR readiness if no true downstream event remains.
  - Prepare PR handoff after verify and explain-change pass.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/proposals/2026-05-07-milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/proposals/2026-05-07-milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/workflows.md --path AGENTS.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/plan/SKILL.md --path skills/workflow/SKILL.md --path .codex/skills/implement/SKILL.md --path .codex/skills/code-review/SKILL.md --path .codex/skills/plan/SKILL.md --path .codex/skills/workflow/SKILL.md --path dist/adapters/codex/.agents/skills/implement/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/plan/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/claude/.claude/skills/implement/SKILL.md --path dist/adapters/claude/.claude/skills/code-review/SKILL.md --path dist/adapters/claude/.claude/skills/plan/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/implement/SKILL.md --path dist/adapters/opencode/.opencode/skills/code-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/plan/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml`
  - generated-output drift commands from M4
  - `git diff --check -- docs/plan.md docs/plans/2026-05-07-milestone-aware-review-handoff.md docs/proposals/2026-05-07-milestone-aware-review-handoff.md specs/milestone-aware-review-handoff.md specs/milestone-aware-review-handoff.test.md specs/workflow-stage-autoprogression.md specs/workflow-stage-autoprogression.test.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/plan/SKILL.md skills/workflow/SKILL.md scripts/test-skill-validator.py docs/changes/2026-05-07-milestone-aware-review-handoff .codex/skills dist/adapters`
- Expected observable result: verify passes only after all in-scope implementation milestones are closed, explain-change records the reasoning, and PR handoff can cite coherent plan/spec/test/review evidence.
- Risks:
  - The plan index and plan body can drift during final closeout.
  - Review-resolution findings could broaden scope into a later milestone.
- Rollback/recovery:
  - Treat stale plan lifecycle state as blocking verify and update `docs/plan.md` plus this plan in the same PR.
  - If a finding changes a later milestone's scope, update this plan before continuing.

## Validation Plan

Per-milestone validation is listed in each milestone and should be copied into the matching test spec.

Final validation should include:

- focused static tests for milestone-aware wording;
- lifecycle validation for touched proposal, spec, test spec, plan, and change-local artifacts;
- selected explicit CI over touched workflow, skill, docs, test, generated, and change-local surfaces;
- generated skill and adapter drift checks after canonical skill changes;
- `git diff --check` over touched files.

`python scripts/validate-artifact-lifecycle.py --mode local` is not the default proof surface for this initiative because the working tree may contain unrelated local drafts or staged lifecycle artifacts. Use explicit paths or selected CI unless the worktree is known clean.

## Risks and Recovery

- Risk: old `clean-with-notes -> verify` wording remains in an overlap surface.
  - Recovery: use static searches and skill-validator assertions over workflow specs, workflow docs, and stage skills before code-review.
- Risk: the milestone state vocabulary expands back into parallel state machines.
  - Recovery: keep the approved single-field vocabulary and move implementation completion or clean review details into evidence fields.
- Risk: static checks become brittle.
  - Recovery: assert stable contract phrases and forbidden state values instead of whole paragraphs.
- Risk: generated output is hand-edited or stale.
  - Recovery: rerun `build-skills.py` and `build-adapters.py`, then use drift checks as the source of truth.
- Risk: plan-template/example-plan questions distract from the first slice.
  - Recovery: keep template/example-plan changes out of this implementation unless plan-review or the approved test spec identifies a blocking contradiction.

## Dependencies

- `plan-review` must approve this plan before implementation.
- `test-spec` must create the matching proof map before implementation.
- Architecture remains unnecessary unless plan-review or test-spec identifies new executable routing, parsing, storage, API, or boundary decisions.
- Code-review must happen after each implementation milestone or aggregate slice.
- Review-resolution must close when triggered before the workflow advances to the next implementation milestone or `verify`.
- Generated output depends on canonical skill changes and must be produced through repository scripts.

## Progress

- [x] Proposal accepted.
- [x] Spec approved.
- [x] Architecture not required, with rationale recorded.
- [x] Execution plan created and indexed.
- [x] Plan-review completed.
- [x] Matching test spec created.
- [x] M1 static proof surfaces complete.
- [x] M1 code-review complete.
- [x] M2 workflow contract alignment complete.
- [x] M2 code-review complete.
- [ ] M3 docs and skill guidance alignment complete.
- [ ] M3 code-review complete.
- [ ] M4 generated output and implementation evidence complete.
- [ ] M4 code-review complete.
- [ ] Review-resolution closed if triggered.
- [ ] Verify complete.
- [ ] Explain-change complete.
- [ ] PR handoff complete.
- [ ] Plan lifecycle synchronized to Done when no true downstream event remains.

## Decision Log

- 2026-05-07: Use four implementation milestones plus a lifecycle-closeout section. Rationale: proof surfaces, authoritative contract edits, skill/docs guidance, and generated output have different review and validation risks.
- 2026-05-07: No architecture artifact is required. Rationale: the approved first slice is guidance and static wording checks only, with no executable routing or plan-state parser.
- 2026-05-07: Keep plan-template/example-plan work out of this implementation slice. Rationale: the approved proposal and spec explicitly limit the first slice and avoid introducing a template-level change.
- 2026-05-07: Treat `AGENTS.md` as conditionally affected and `CONSTITUTION.md` as conditionally unaffected unless implementation finds a direct conflict. Rationale: root guidance should stay concise, while normative workflow detail belongs in specs and `docs/workflows.md`.
- 2026-05-07: Use explicit-path lifecycle validation for planning proof. Rationale: it is the narrow stable proof for newly created and touched lifecycle artifacts.
- 2026-05-07: Keep the test spec proof surface static and guidance-focused. Rationale: the approved first slice explicitly forbids executable plan-state validation and a standalone `review-resolution` skill.
- 2026-05-07: Start M1 with proof-surface edits only. Rationale: M1 defines tests and static proof before M2/M3 amend the authoritative workflow and skill guidance.
- 2026-05-07: Use `unittest.expectedFailure` for the two pending M2/M3 skill-validator assertions. Rationale: M1 must install red-state checks before canonical guidance edits while still leaving milestone validation green enough for code-review handoff.
- 2026-05-07: Start M2 by splitting the pending stale-handoff assertion into spec-level passing proof and M3 docs/skills pending proof. Rationale: M2 owns authoritative specs, while `docs/workflows.md` and authored stage skills remain M3 scope.
- 2026-05-07: Leave `specs/review-finding-resolution-contract.md` unchanged for M2. Rationale: the approved same-milestone review-resolution loop is now explicit in the two authoritative workflow specs, and the focused review-resolution record spec does not need new standalone-skill or parser behavior for this slice.

## Surprises and Discoveries

- 2026-05-07: The old guidance still contains unconditional clean-review-to-verify shortcuts in `docs/workflows.md`, `skills/code-review/SKILL.md`, `skills/workflow/SKILL.md`, and `specs/workflow-stage-autoprogression.md`; the new pending skill-validator checks capture that red state for M2/M3.
- 2026-05-07: `specs/rigorloop-workflow.md` also needed to distinguish implementation handoff evidence from a milestone `closed` state. The M2 wording now keeps the existing milestone commit evidence rule while making review closeout the source of the `closed` milestone state.

## Validation Notes

- 2026-05-07 planning validation:
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/proposals/2026-05-07-milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.md` passed and selected `artifact_lifecycle.validate`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/proposals/2026-05-07-milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.md` passed with an existing historical lifecycle-language warning in `docs/plan.md` at line 14.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/proposals/2026-05-07-milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.md` passed.
  - `git diff --check -- docs/plan.md docs/plans/2026-05-07-milestone-aware-review-handoff.md docs/proposals/2026-05-07-milestone-aware-review-handoff.md specs/milestone-aware-review-handoff.md` passed for tracked diff content.
  - `rg -n '[[:blank:]]$|\t' docs/plan.md docs/plans/2026-05-07-milestone-aware-review-handoff.md docs/proposals/2026-05-07-milestone-aware-review-handoff.md specs/milestone-aware-review-handoff.md` found no trailing whitespace or tab characters.
- 2026-05-07 plan-review resolution validation:
  - `python scripts/select-validation.py --mode explicit --path dist/adapters/codex/.agents/skills/implement/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/plan/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/claude/.claude/skills/implement/SKILL.md --path dist/adapters/claude/.claude/skills/code-review/SKILL.md --path dist/adapters/claude/.claude/skills/plan/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/implement/SKILL.md --path dist/adapters/opencode/.opencode/skills/code-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/plan/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md` passed with no `unclassified-path` result.
- 2026-05-07 test-spec validation:
  - `python scripts/select-validation.py --mode explicit --path specs/milestone-aware-review-handoff.test.md --path specs/milestone-aware-review-handoff.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed and selected `artifact_lifecycle.validate` plus `change_metadata.validate`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path specs/milestone-aware-review-handoff.test.md --path specs/milestone-aware-review-handoff.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
- 2026-05-07 M1 validation:
  - `python scripts/test-skill-validator.py` passed with 32 tests and 2 expected failures. The expected failures are the M2/M3 red-state checks for pending milestone-aware guidance alignment.
  - `python scripts/select-validation.py --mode explicit --path specs/milestone-aware-review-handoff.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed with no unclassified paths and selected `skills.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/milestone-aware-review-handoff.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed with an existing lifecycle-language warning in `specs/rigorloop-workflow.test.md`.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path specs/milestone-aware-review-handoff.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `test ! -e skills/review-resolution/SKILL.md` passed.
  - `git diff --check -- specs/milestone-aware-review-handoff.test.md specs/workflow-stage-autoprogression.test.md specs/rigorloop-workflow.test.md scripts/test-skill-validator.py docs/plans/2026-05-07-milestone-aware-review-handoff.md` passed.
  - `rg -n '[[:blank:]]$|\t' specs/milestone-aware-review-handoff.test.md specs/workflow-stage-autoprogression.test.md specs/rigorloop-workflow.test.md scripts/test-skill-validator.py docs/plans/2026-05-07-milestone-aware-review-handoff.md` found no trailing whitespace or tab characters.
- 2026-05-07 M1 code-review closeout:
  - Reviewed commit: `018fb4f M1: add milestone-aware handoff proof`.
  - Review status: `clean-with-notes`.
  - Material findings: none.
  - Detailed review record: not required because the review was clean with no material findings and no detailed-record trigger.
  - `python scripts/test-skill-validator.py` passed with 32 tests and 2 expected failures for pending M2/M3 guidance alignment.
  - `bash scripts/ci.sh --mode explicit --path specs/milestone-aware-review-handoff.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `test ! -e skills/review-resolution/SKILL.md` passed.
  - `git diff --check HEAD~1..HEAD` passed.
- 2026-05-07 M2 validation:
  - `python scripts/test-skill-validator.py` failed before contract edits with 17 expected red-state failures for missing milestone-aware terms in the workflow specs and the stale unconditional `code-review` to `verify` shortcut in `specs/workflow-stage-autoprogression.md`.
  - `python scripts/test-skill-validator.py` passed with 33 tests and 2 expected failures. The remaining expected failures are M3 docs/skill guidance checks.
  - `python scripts/select-validation.py --mode explicit --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed with no unclassified paths and selected `skills.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed with existing lifecycle-language warnings in `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`.
  - `python scripts/test-change-metadata-validator.py` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `test ! -e skills/review-resolution/SKILL.md` passed.
  - `git diff --check -- specs/workflow-stage-autoprogression.md specs/rigorloop-workflow.md scripts/test-skill-validator.py docs/plans/2026-05-07-milestone-aware-review-handoff.md docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `rg -n '[[:blank:]]$|\t' specs/workflow-stage-autoprogression.md specs/rigorloop-workflow.md scripts/test-skill-validator.py docs/plans/2026-05-07-milestone-aware-review-handoff.md docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` found no trailing whitespace or tab characters.
- 2026-05-07 M2 code-review closeout:
  - Reviewed commit: `66a3815 M2: align milestone-aware workflow contract`.
  - Review status: `clean-with-notes`.
  - Material findings: none.
  - Detailed review record: not required because the review was clean with no material findings and no detailed-record trigger.
  - `python scripts/test-skill-validator.py` passed with 33 tests and 2 expected failures for pending M3 docs/skill guidance alignment.
  - `python scripts/select-validation.py --mode explicit --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed with no unclassified paths and selected `skills.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed with existing lifecycle-language warnings in `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`.
  - `python scripts/test-change-metadata-validator.py` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path specs/milestone-aware-review-handoff.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-07-milestone-aware-review-handoff.md --path docs/changes/2026-05-07-milestone-aware-review-handoff/change.yaml` passed.
  - `git diff --check HEAD~1..HEAD` passed.
  - `test ! -e skills/review-resolution/SKILL.md` passed.

## Outcome and Retrospective

Active. Next stage: `implement M3`. Verify is not ready because implementation milestones M3 and M4 remain open.
