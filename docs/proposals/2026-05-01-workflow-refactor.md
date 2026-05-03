# Workflow Refactor

## Status

- accepted

## Problem

RigorLoop's workflow guidance has grown by accretion. The current full-lifecycle summary mixes different kinds of artifacts in one linear chain:

```text
constitution / project-map when needed -> explore -> research when needed -> proposal -> ... -> pr
```

That line hides important lifecycle differences. `CONSTITUTION.md` is a standing governance artifact. `project-map` is a living reference that can go stale. `explore` and `research` are on-demand aids. `learn` is retrospective and periodic. The workflow skill, workflow spec, and workflow summary are infrastructure that govern the chain rather than stages inside it.

When these categories are blurred, contributors cannot tell what is mandatory, what is conditional, what should be refreshed, and what only runs when the work calls for it. The same ambiguity also scatters workflow-handoff rules across skill files instead of making the workflow definition easy to inspect in one authoritative place.

## Goals

- Refactor workflow guidance around explicit artifact categories instead of one overloaded chain.
- Classify stage-like workflow actions with stable obligation values, separate trigger text, whether they run for every change, and downstream-blocking behavior.
- Move `explore` and `research` out of the default per-change chain and into on-demand support.
- Move `learn` out of the per-change chain and into periodic or explicitly invoked retrospective work.
- Define category-level creation, revision, staleness, absence, and dependency rules.
- Make `project-map` a living reference with a minimal no-reliance rule when it is absent, known-stale, contradicted, or missing the relied-on area.
- Consolidate workflow-handoff ownership into the canonical workflow definition while preserving useful local skill guidance.
- Rename the ambiguous lifecycle label `ci` to `ci-maintenance` in workflow guidance so hosted validation remains owned by `verify`.
- Define the first-substantive-proposal rule and its bootstrap exemption.
- Define minimum triggers for periodic or explicitly invoked `learn`.
- Preserve a transition rule for in-flight work so existing active changes do not churn purely because the workflow wording changes.
- Record why `explore`, `research`, and `learn` are demoted from the visible per-change chain so future re-promotion proposals must address that reasoning.

## Non-goals

- Rewriting the project vision content.
- Recreating the already implemented `vision` skill from scratch.
- Implementing the project-map lifecycle model in this proposal's first change; freshness markers, calendar thresholds, and revision workflow should have a focused follow-up proposal.
- Implementing the final `learn` artifact model; per-session `docs/learn/YYYY-MM-DD-<slug>.md`, topic-organized `docs/learnings/<topic>.md`, and action-routing rules should have a focused follow-up proposal.
- Adding workflow lanes beyond the existing fast-lane and full-lifecycle model.
- Consolidating all skills or removing skill-local operational guidance that is still useful at the point of use.
- Changing CI coverage or release automation beyond clarifying the boundary of `ci-maintenance`.
- Making `explore`, `research`, or `learn` unavailable. They remain valid skills; they just stop appearing as default per-change stages.
- Creating a second normative workflow source that competes with `specs/rigorloop-workflow.md`.

## Vision fit

fits the current vision

This refactor supports the current vision by making AI-assisted delivery easier to inspect and reason about in Git. It strengthens source-of-truth clarity, makes workflow commitments more checkable, and reduces process theater by separating standing governance, living references, on-demand aids, per-change gates, and retrospective learning.

It does not revise the approved project vision or change the current root `VISION.md` artifact.

## Context

`CONSTITUTION.md` already says RigorLoop optimizes for reviewability, traceability, and trustworthy automation. It also says behavior and workflow-stage changes use the full lifecycle, and that `AGENTS.md` and `docs/workflows.md` should summarize governing artifacts rather than compete with them.

The current normative workflow contract lives in `specs/rigorloop-workflow.md`. The short operational summary lives in `docs/workflows.md`. The workflow skill provides operator-facing routing guidance, and individual stage skills contain handoff notes. This distribution is workable, but the same routing ideas now appear in several places with different framing.

There is currently no `docs/project-map.md`. The workflow still references `project-map when needed`, which is directionally useful but not enough to define absence, creation, or freshness behavior.

The repository currently uses root `VISION.md` as the canonical project vision. The `vision.md` to `VISION.md` migration has already landed, so this workflow refactor builds on that source-of-truth state instead of carrying a root-vision artifact migration.

## Options considered

### Option 1: Keep the current workflow chain

Advantages:

- No new governance work.
- No transition cost for existing docs, skills, specs, tests, or generated output.
- Existing contributors already know the current chain.

Disadvantages:

- Keeps standing artifacts, living references, on-demand aids, per-change stages, and retrospective work in one visual sequence.
- Leaves "when needed" under-specified.
- Continues to make contributors infer mandatory versus conditional stages from scattered guidance.
- Does not address stale living references.

### Option 2: Rewrite only the summary chain

Advantages:

- Small documentation diff.
- Makes `docs/workflows.md` easier to read quickly.
- Avoids deeper spec and skill changes.

Disadvantages:

- Leaves the normative workflow spec and stage skills with the older mental model.
- Does not create a durable category contract.
- Risks making the summary nicer while the real routing rules remain scattered.

### Option 3: Refactor the workflow contract around artifact categories

Advantages:

- Fixes the source of the ambiguity by defining each category's lifecycle rules.
- Makes mandatory, conditional, and on-demand stages visible.
- Moves `explore`, `research`, and `learn` to the categories that match how they are actually used.
- Keeps `specs/rigorloop-workflow.md` as the canonical workflow definition and `docs/workflows.md` as its summary.
- Gives project-map a clear living-reference role without mixing the full project-map skill redesign into this change.
- Allows skill handoff sections to point to one definition instead of restating the contract in full.

Disadvantages:

- Touches several authoritative surfaces.
- Requires careful transition handling so active work is not forced through churn.
- Requires a focused test/spec update to prove category classification, stage obligations, and handoff ownership.

### Option 4: Combine workflow refactor with project-map lifecycle, CI, and skill consolidation

Advantages:

- Could solve several related governance problems in one initiative.
- Would create a more complete end-state for workflow routing and living references.
- Could also revisit adjacent root-vision artifact policy.

Disadvantages:

- Too broad for one proposal.
- Makes it harder to review the core workflow classification decision.
- Risks delaying the useful refactor behind project-map, CI, and adjacent artifact-policy details.
- Increases rollback cost.

## Recommended direction

Choose Option 3.

The workflow should be presented as a category model, not as a single chain that begins with every possible upstream aid. The proposal uses these six labels because they describe distinct lifecycle behavior:

| Category | Artifacts or stages | Creation rule | Revision or refresh rule | Staleness or absence check | Dependents |
| --- | --- | --- | --- | --- | --- |
| Standing artifacts | `VISION.md`, `CONSTITUTION.md` | Created once near project genesis or governance adoption | Revised deliberately when project identity or governing principles change | Absence gates differ by artifact: `VISION.md` blocks the first substantive proposal except vision bootstrap; `CONSTITUTION.md` blocks governance adoption, workflow-governance, and source-of-truth changes except constitution bootstrap | All proposal, spec, workflow, and review stages |
| Living references | `docs/project-map.md` | Created when repository structure is not obvious enough for safe architecture or planning | Minimal rule only: refresh or record a no-map rationale before relying when the map is absent, known-stale, contradicted, or missing the relied-on area | Detailed freshness markers, calendar thresholds, and revision workflow are deferred | Architecture, plan, code-review, and onboarding-heavy work |
| Workflow infrastructure | `specs/rigorloop-workflow.md`, `docs/workflows.md`, affected root operating guidance, affected stage skills, and generated skill or adapter outputs when canonical skills change | Created and maintained as workflow governance | Revised when stage order, routing, handoff, or category policy changes | Unresolved drift across affected operating and governance surfaces blocks workflow-change readiness | Every lifecycle stage |
| On-demand artifacts | `explore`, `research` | Created only when the problem warrants durable option expansion or external evidence | Revised when their assumptions or findings are materially outdated | Absence is not a blocker unless the current work depends on unresolved options or uncertain facts | Proposal, spec, architecture, and plan when their decisions depend on the artifact |
| Per-change chain | `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution -> verify -> explain-change -> pr` plus conditional `ci-maintenance` support | Created or run according to stage obligation metadata | Updated as the change moves through the lifecycle | Missing required or triggered actions block downstream readiness | The current change and PR package |
| Periodic artifacts | `learn` | Run on cadence, after incidents, repeated findings, failed release or adapter smoke, accepted postmortem actions, or explicit maintainer request | Revised by adding or updating lessons, not by changing lifecycle state | Absence does not block ordinary PRs when the trigger is closed by lesson capture, a scheduled follow-up, or an explicit no-learn rationale; it blocks only when a higher-priority artifact makes it blocking | Future proposals, specs, workflow updates, and skill refinements |

Standing artifacts include `VISION.md` and `CONSTITUTION.md`, but their absence has different gates. `VISION.md` absence blocks the first substantive proposal unless the proposal bootstraps project vision. `CONSTITUTION.md` absence blocks governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal bootstraps the constitution.

Stage-like workflow actions should use stable obligation metadata, not bracketed prose labels. For conditional or on-demand rows, downstream blocking applies only after the trigger is active or the artifact has been cited as a dependency.

| Stage or action | Obligation | Trigger | Runs for every change | Blocks downstream when missing |
| --- | --- | --- | --- | --- |
| `explore` | `on-demand` | Strategic ambiguity, unclear problem framing, option expansion, architecture-level uncertainty, or maintainer request. | `false` | `true` |
| `research` | `on-demand` | Current external docs, APIs, versions, competitors, standards, laws, pricing, or operational facts affect the decision. | `false` | `true` |
| `proposal` | `mandatory` | New direction, public behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract. | `true` | `true` |
| `proposal-review` | `conditional` | Mandatory when the proposal is workflow-governance, direction-setting, high-risk, or maintainer-requested; otherwise conditional. | `false` | `true` |
| `spec` | `mandatory` | Externally observable behavior, workflow policy, schema, generated output, compatibility, security-sensitive behavior, or public contributor expectation changes. | `true` | `true` |
| `spec-review` | `mandatory` | Behavior, workflow, schema, compatibility, or safety-sensitive changes. | `true` | `true` |
| `architecture` | `conditional` | Boundary, data flow, generated package, CI infrastructure, integration, storage, deployment, or long-lived design impact. | `false` | `true` |
| `architecture-review` | `conditional` | High-risk, cross-component, migration-heavy, security-sensitive, or hard-to-reverse design. | `false` | `true` |
| `plan` | `conditional` | Multi-file, risky, ambiguous, migration-heavy, sequencing-sensitive, or milestone-based work. | `false` | `true` |
| `plan-review` | `conditional` | Multi-milestone, sequencing-sensitive, recovery-sensitive, or maintainer-requested work. | `false` | `true` |
| `test-spec` | `mandatory` | Behavior or workflow-contract proof is required. | `true` | `true` |
| `implement` | `mandatory` | The accepted contract is ready to change tracked artifacts. | `true` | `true` |
| `code-review` | `mandatory` | Non-trivial changes. | `true` | `true` |
| `review-resolution` | `conditional` | Material review findings, non-final dispositions, or review outcomes require explicit closeout. | `false` | `true` |
| `verify` | `mandatory` | Every contributed change. | `true` | `true` |
| `ci-maintenance` | `conditional` | Hosted workflow automation or related CI infrastructure for a material risk is missing, stale, or wrong. | `false` | `true` |
| `explain-change` | `mandatory` | Non-trivial changes require standalone durable explanation; all changes require PR-summary explanation. | `true` | `true` |
| `pr` | `mandatory` | Every contributed change. | `true` | `true` |
| `learn` | `periodic` | Repeated review findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem action changing workflow guidance, cadence run, or explicit maintainer request. | `false` | `false` |

The `Runs for every change` column applies within the full-lifecycle lane after the row trigger makes the stage applicable. It does not override fast-lane eligibility or the trigger column.

Triggered `learn` should either capture the lesson immediately or record a follow-up to capture it later. It does not block ordinary `verify`, final `explain-change`, or `pr` closeout by default. It blocks downstream only when a higher-priority artifact explicitly makes it blocking, such as an active plan, review-resolution, postmortem action, release contract, or maintainer decision. If no such blocking artifact exists, the required closeout action is a scheduled follow-up or explicit no-learn rationale.

Until a focused `learn` refactor defines the final learning artifact model, scheduled `learn` follow-ups and explicit no-learn rationales should be recorded in a contributor-visible tracked or review-visible surface, such as the active plan, `docs/changes/<change-id>/change.yaml`, `review-resolution.md`, `explain-change.md`, PR body or draft PR body, linked issue, or a named governance artifact. Chat-only notes should not satisfy this recording requirement.

The workflow definition document should remain `specs/rigorloop-workflow.md`. That file already has the correct source-of-truth priority for normative behavior. `docs/workflows.md` should remain a short operational summary, and skill handoff sections should point to the spec for category and routing rules rather than duplicating the full contract.

The ownership split should be explicit:

- Workflow spec owns stage order, obligation level, autoprogression and stop conditions, routing rules, category definitions, and downstream-blocking semantics.
- Skill files own local preconditions, local outputs, local failure modes, and a short pointer to the next stage.
- Skill handoff sections should summarize the workflow contract and link or point to it; they should not duplicate full routing tables.

Workflow-governance changes should keep affected operating and governance guidance aligned. Affected surfaces may include `CONSTITUTION.md`, `AGENTS.md`, `README.md` when it contains workflow, contribution, or operating guidance, `docs/workflows.md`, `specs/rigorloop-workflow.md`, affected stage skills, generated `.codex/skills/`, and generated public adapters under `dist/adapters/` when canonical skills change. Downstream handoff should wait until each affected surface is updated, explicitly marked unaffected with rationale, or recorded as deferred with owner and follow-up.

Unaffected-surface rationales and affected-surface deferrals should be recorded in a contributor-visible tracked or review-visible surface, such as the proposal, spec, active plan, change-local artifacts, PR body or draft PR body, linked issue, or affected governance artifact.

The first-proposal prerequisite should be enforced by the `proposal` skill. A substantive proposal is any proposal that chooses product direction, user-facing behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract. When no root `VISION.md` exists, `proposal` should stop before creating a substantive proposal unless the proposal is explicitly bootstrap work to create or migrate project vision. `CONSTITUTION.md` absence separately blocks governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal bootstraps the constitution. Bootstrap proposals must say so in `Vision fit`, and `proposal-review` should check that exemption.

`review-resolution` is not a review stage. It is the closeout stage for review findings. It is required when material review findings, non-final dispositions, or review outcomes require explicit closeout. `verify`, final `explain-change`, and `pr` must not proceed while required review-resolution work is open.

Project-map should receive only a minimal living-reference rule in this refactor: consumers must not rely on `docs/project-map.md` when it is absent, known-stale, contradicted by the current repository, or missing the relied-on area. They must refresh it or record a no-map rationale. Detailed freshness markers, calendar thresholds, and project-map skill behavior belong in the follow-up.

The `ci` stage label should become `ci-maintenance` in workflow guidance. The associated skill creates and updates CI infrastructure such as workflow files, validation automation, and platform configuration. It does not run validation, design tests, or specify validation commands; those responsibilities belong to `verify`, `test-spec`, and the spec or plan.

In-flight work should complete on the workflow contract that was active when it started, unless the active owner opts into the new model or the work touches the refactored workflow surfaces directly. Planned initiatives and change-local metadata should record the selected workflow contract, such as `pre-refactor` or `refactored`, when that distinction affects review or verification.

## Expected behavior changes

- Workflow readers see standing artifacts, living references, workflow infrastructure, on-demand artifacts, the per-change chain, and periodic learning as separate categories.
- `explore` and `research` stop appearing as default prerequisites for every non-trivial change.
- `learn` stops appearing as a final per-change stage and is treated as periodic or explicitly invoked retrospective capture.
- Stage expectations become scannable through stable obligation values, trigger text, whether they run for every change, and downstream-blocking behavior.
- The first substantive proposal in a project is blocked until the project has a standing vision artifact, except for bootstrap work that creates or migrates that artifact.
- Required `review-resolution` closeout blocks `verify`, final `explain-change`, and `pr` while material review findings, non-final dispositions, or review outcomes still require explicit closeout.
- Architecture and planning work that relies on `docs/project-map.md` checks whether the map is absent, known-stale, contradicted, or missing the relied-on area before relying on it, without requiring full project-map lifecycle mechanics in this change.
- Workflow handoff rules become easier to audit because the workflow spec owns the definition and skill-local handoff sections become pointers or brief summaries.
- Workflow guidance uses `ci-maintenance` for automation maintenance and leaves validation execution under `verify`.

## Architecture impact

This is a workflow-governance and artifact-routing change, not a runtime architecture change.

Likely touched authoritative surfaces:

- `CONSTITUTION.md` for category-level governance and source-of-truth alignment.
- `AGENTS.md` for concise repository operating rules.
- `specs/rigorloop-workflow.md` as the canonical workflow definition document.
- `specs/rigorloop-workflow.test.md` for category, stage-obligation, transition, and handoff-ownership coverage.
- `docs/workflows.md` as the short summary.
- `README.md` links and workflow summary snippets.
- `skills/workflow/SKILL.md` and stage skills whose handoff sections duplicate workflow-definition rules.
- `skills/proposal/SKILL.md` for the first-substantive-proposal prerequisite and bootstrap exemption.
- `skills/ci/SKILL.md` for the `ci-maintenance` scope boundary.
- Generated `.codex/skills/` and `dist/adapters/` output through existing generators when canonical skills change.

No service boundary, storage layer, network integration, or deployment architecture is expected to change.

## Testing and verification strategy

The future implementation should prove both authored-contract alignment and generated-output determinism.

Likely checks:

```bash
python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/workflow/SKILL.md --path skills/proposal/SKILL.md --path skills/ci/SKILL.md
bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path skills/workflow/SKILL.md --path skills/proposal/SKILL.md --path skills/ci/SKILL.md
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-select-validation.py
git diff --check --
```

Focused proof should cover:

- the category model appears in the workflow definition and summary without conflicting wording;
- stage-like workflow actions have stable obligation values, trigger text, whether they run for every change, and downstream-blocking behavior;
- `explore`, `research`, and `learn` are not described as default per-change stages;
- `proposal` defines substantive proposals and the bootstrap exemption when root `VISION.md` is missing;
- required `review-resolution` closeout blocks `verify`, final `explain-change`, and `pr` until open review findings are closed;
- `ci-maintenance` is distinct from running validation, designing tests, or specifying validation commands;
- minimum `learn` triggers are visible, with immediate capture, scheduled follow-up, or explicit no-learn rationale as the default non-blocking closeout path, and temporary recording surfaces for non-captured closeout are defined;
- generated Codex and public adapter outputs match canonical skill sources.

## Rollout and rollback

Rollout should use the full lifecycle because the change alters workflow policy, skill guidance, and generated output.

Recommended rollout:

1. Proposal review settles the category model, obligation taxonomy, handoff ownership split, `ci-maintenance` label, and project-map minimal rule.
2. Spec and spec review define the contract.
3. Architecture is skipped with rationale unless spec review finds generated-output or validation routing design risk that warrants an architecture package.
4. Plan and plan review sequence the refactor.
5. Test spec maps each category, obligation value, transition rule, first-substantive-proposal rule, and `learn` trigger.
6. Implementation updates canonical sources first, then regenerates derived outputs.
7. Code review, review-resolution when triggered, verify, explain-change, and PR close the change.

Rollback should revert the workflow category contract, obligation taxonomy, and affected skill wording consistently.

## Risks and mitigations

- Risk: The category model creates more vocabulary than value.
  Mitigation: keep categories small, define behavior per category, and remove the overloaded linear prefix that caused the ambiguity.

- Risk: A workflow definition under `docs/` would compete with the approved spec.
  Mitigation: keep `specs/rigorloop-workflow.md` as the canonical definition and use `docs/workflows.md` only as a summary.

- Risk: Moving `explore` and `research` out of the chain makes contributors skip useful thinking.
  Mitigation: state on-demand triggers clearly and keep both skills available when ambiguity, options, or external facts matter.

- Risk: Moving `learn` to periodic work hides lessons that should affect future changes.
  Mitigation: define minimum triggers now, defer cadence details, and keep explicit invocation available when a durable lesson emerges.

- Risk: `project-map` freshness checks become vague and unenforceable.
  Mitigation: use only a minimal no-reliance rule in this refactor, then handle markers, refresh workflow, thresholds, and project-map skill behavior in a focused follow-up.

- Risk: Renaming `ci` in workflow guidance creates churn with the existing `ci` skill path.
  Mitigation: make the proposal-level decision about the visible workflow label, and allow the existing `skills/ci/` path to remain while its scope wording changes.

- Risk: In-flight work churns because the workflow model changes midstream.
  Mitigation: allow active work to finish under the old contract unless it directly touches the refactored workflow surfaces or opts into the new model, and record the selected workflow contract when it affects review.

## Open questions

None block downstream planning.

The approved spec settles the lower-level `ci-maintenance` path question by allowing the existing `skills/ci/` path to remain. It also leaves periodic `learn` cadence and the final learn artifact model outside this refactor beyond the minimum trigger and temporary recording-surface rules.

## Decision log

- 2026-05-01: Draft proposal recommends a category-based workflow refactor, with `specs/rigorloop-workflow.md` as the canonical workflow definition document and `docs/workflows.md` as the operational summary.
- 2026-05-01: Rejected a vision-only or project-map-only refactor. Reason: the primary issue is category conflation across the workflow.
- 2026-05-01: Rejected creating a competing `docs/workflow.md` definition. Reason: the repository already gives approved specs higher authority than workflow summaries.
- 2026-05-03: The root `vision.md` to `VISION.md` migration has landed. This workflow refactor builds on `VISION.md` as the canonical project-vision artifact instead of carrying a root-vision migration.
- 2026-05-01: Chose stable obligation metadata over bracketed prose status tags. Reason: tests, validators, and skill alignment need durable values.
- 2026-05-01: Chose `ci-maintenance` as the workflow label for CI infrastructure work. Reason: `verify` owns validation execution, while the CI skill owns hosted automation maintenance.
- 2026-05-01: Deferred project-map lifecycle mechanics to a focused follow-up. Reason: project-map needs freshness markers and revision triggers, but this refactor only needs a minimal no-reliance rule.
- 2026-05-03: Deferred final learn artifact design to a focused follow-up. Reason: this refactor only needs a minimal closeout recording rule; the future learn refactor can define per-session output, topic-organized durable lessons, and action routing.

## Next artifacts

- `plan-review` for [Workflow Refactor Execution Plan](../plans/2026-05-03-workflow-refactor.md).
- Matching update to `specs/rigorloop-workflow.test.md` after plan-review.
- Follow-up proposal for project-map lifecycle and freshness markers.
- Follow-up proposal for learn artifact model and learning-skill refactor.

## Follow-on artifacts

- `spec`: [RigorLoop Workflow](../../specs/rigorloop-workflow.md)
- `plan`: [Workflow Refactor Execution Plan](../plans/2026-05-03-workflow-refactor.md)
- Future focused `learn` refactor for per-session output, topic-organized durable lessons, and action routing into affected artifacts or ADRs.

## Readiness

Accepted. The downstream workflow spec amendment is approved, and execution planning now owns sequencing the implementation.

The proposal resolves the main direction decisions: use category-based workflow guidance, keep `specs/rigorloop-workflow.md` as the canonical workflow definition, classify stage-like actions with stable obligation metadata, define the first-substantive-proposal prerequisite through `proposal`, use a minimal project-map no-reliance rule, rename the visible CI infrastructure stage to `ci-maintenance`, define minimum `learn` triggers, and let in-flight work finish on the old contract unless it opts in or touches the refactored surfaces.
