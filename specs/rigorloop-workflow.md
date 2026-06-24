# RigorLoop Workflow

## Status
- approved

## Related proposal

- [RigorLoop Project Direction](../docs/proposals/2026-04-19-rigorloop-project-direction.md)
- [Implementation Milestone Commit Policy](../docs/proposals/2026-04-19-implementation-milestone-commit-policy.md)
- [Workflow Refactor](../docs/proposals/2026-05-01-workflow-refactor.md)
- [Optimize Learn Skill](../docs/proposals/2026-05-03-optimize-learn-skill.md)
- [PR-Self-Contained Lifecycle Completion](../docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md)
- [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- [Milestone-Aware Review Handoff](../docs/proposals/2026-05-07-milestone-aware-review-handoff.md)
- [Skill Contract Optimization](../docs/proposals/2026-05-08-skill-contract-optimization.md)
- [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md)
- [Proposal-Gated Authoring Autoprogression Through Plan Review](../docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md)
- [Separately Armed Implementation Autoprogression Through Verify](../docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md)

## Goal and context

This spec defines the externally observable workflow contract for the first RigorLoop starter-kit release. The goal is to make AI-assisted software delivery explicit, reviewable, and auditable for individual contributors and maintainers while allowing users to request isolated individual skill outputs without implying full workflow completion.

This amendment updates the workflow contract around explicit artifact categories, stable stage-obligation metadata, living-reference handling, workflow-handoff ownership, the final learn artifact model, PR-self-contained lifecycle completion, one recommended standard workflow, isolated manual skill invocation, final `explain-change -> verify -> pr` ordering, and project-portable published skill surfaces. It keeps `specs/rigorloop-workflow.md` as the canonical workflow definition and keeps `docs/workflows.md` as the short operational summary.

This amendment also clarifies that isolated formal review requests stop downstream handoff but do not suppress durable recording. Every material finding is recorded, and all material findings require change-local review files.

This amendment also defines the bounded `authoring-through-plan-review` autoprogression profile. The profile is change-local, explicitly armed, starts only after a clean accepted proposal gate, runs deterministic authoring and review stages through clean `plan-review`, and stops before `test-spec` or implementation.

This amendment also defines the separately armed `implementation-through-verify` autoprogression profile. The profile is change-local, requires clean planning and its own authorization, uses deterministic test-spec settlement, runs implementation and independent code-review loops only within persisted phase authority, may run fresh `verify` in Phase C, and stops before `pr`.

`specs/skill-contract.md` owns skill-contract behavior. It owns standard skill shape, claim boundaries, result output expectations, shared-block rules, generated-output boundaries, evidence-reading guidance, and minimum viable skill rules. `specs/rigorloop-workflow.md` continues to own stage order, stage obligation, handoff, and downstream-blocking semantics.

RigorLoop is a Git-first starter kit. It does not replace pull requests, CI, or human review. It provides a repeatable path, artifact model, and validation rules so contributors can move from idea to reviewed change with traceable evidence.

## Glossary

- `standard workflow`: the single recommended RigorLoop workflow model used when a contributor or agent claims complete AI-assisted delivery for a change, with mandatory, conditional, on-demand, and periodic stages.
- `manual skill invocation`: a user-requested run of one individual skill for focused output. It is isolated by default and does not imply that upstream or downstream workflow stages are complete.
- `planned milestone work`: work governed by a concrete plan that defines one or more explicit milestones.
- `milestone-based plan`: a concrete execution plan with one or more in-scope implementation milestones that must be implemented, reviewed, and closed before final closeout readiness.
- `in-scope implementation milestone`: a planned milestone whose current scope still includes implementation work for the change.
- `lifecycle-closeout milestone`: a milestone or plan step that contains only downstream lifecycle gates such as `ci-maintenance`, `explain-change`, `verify`, PR handoff, release, deploy, or other closeout work, and not unfinished implementation work.
- `change artifact`: a durable Markdown document that explains proposal, spec, plan, tests, verification, or rationale for a change.
- `change metadata`: machine-readable traceability data for a change.
- `change.yaml`: the first-release canonical machine-readable traceability file for a non-trivial change.
- `canonical source`: the authored workflow content from which generated output is derived.
- `generated output`: derived distribution content that can be rebuilt and is not the source of truth.
- `adapter`: tool-specific guidance or generated output layered on top of generic workflow content.
- `workflow-managed completion flow`: a change flow that is being carried through its normal downstream stages toward completion under the standard workflow.
- `isolated stage request`: a request for the output of one stage only, such as standalone review, verification, or explanation work.
- `tracked artifact`: any version-controlled repository file whose change will be committed or reviewed as part of the work.
- `shared review-skill recording subsection`: the identical `## Isolation and Recording` guidance copied into all formal review skills from `templates/shared/review-isolation-and-recording.md`.
- `scan-first review resolution`: a `review-resolution.md` structure that exposes closeout status, covered reviews, finding counts, disposition overview, shared validation evidence, and per-finding details without forcing reviewers to read repeated prose first.
- `immediate next repository stage`: the next mandatory or triggered downstream repository stage for the current workflow state and invocation context.
- `downstream readiness`: an assessment of whether a later stage can be relied on after required intermediate stages complete.
- `eventual test-spec readiness`: the downstream-readiness assessment for later `test-spec` authoring.
- `stop condition`: a documented reason the workflow must stop rather than continue into downstream reliance or stage continuation.
- `review surface`: the changed files, staged diff, unstaged diff, PR diff, patch, or commit range being inspected by `code-review`.
- `tracked governing branch state`: the tracked Git state that can support branch-scoped authority or readiness conclusions for the reviewed change.
- `governing artifact`: a proposal, spec, test spec, architecture document, ADR, plan, or other cited workflow artifact used as review or readiness authority.
- `local-only governing artifact`: a governing artifact visible in the local worktree but absent from tracked governing branch state.
- `learn session`: a periodic, incident-driven, contributor-observed, or explicitly requested retrospective run that examines evidence and records what was or was not learned.
- `learn session record`: the dated historical record for one learn session under `docs/learn/sessions/`.
- `learn topic file`: curated topic-organized guidance under `docs/learn/topics/`.
- `branch-ready`: the `verify` stage conclusion that the tracked branch state satisfies required validation and authoritative-artifact checks.
- `pr-body-ready`: the `pr` stage conclusion that the PR body is accurate, concise, and grounded in verified artifacts.
- `pr-open-ready`: the `pr` stage conclusion that branch, base, remote, worktree, PR body, and action prerequisites are ready for PR opening.
- `direct proof`: targeted evidence tied to a named requirement or test-spec item, such as a targeted test, targeted validation output, or an explicit manual verification note when manual verification is allowed.
- `targeted proof`: selector-selected validation checks that directly prove the changed surfaces and governing dependencies before review handoff.
- `broad smoke`: broader repository validation run before final handoff, main, release, or another authoritative trigger; it is not the default first proof for every local edit.
- `manual proof`: durable structured evidence for a check that cannot reasonably be automated.
- `standing artifact`: a project-level governance or identity artifact that is created once near project genesis or governance adoption and revised deliberately.
- `living reference`: a durable reference artifact that helps contributors reason about the repository but can go stale and must be refreshed or bypassed with rationale before reliance when absent, known-stale, contradicted, or missing the relied-on area.
- `repo-local lifecycle state`: tracked repository state that records whether an artifact, plan, review resolution, change-local record, or readiness surface is draft, active, accepted, approved, done, blocked, superseded, closed, or otherwise current within the repository tree.
- `PR-self-contained lifecycle completion`: the rule that a PR performing the work that makes a repo-local lifecycle state true records that state in the PR before it opens for review.
- `downstream completion event`: a deploy, release, package publication, external migration, observed hosted result, or other event that cannot be made true by the PR tree itself.
- `review-open PR`: a PR or equivalent review package that is ready for reviewer action. A draft PR used for early CI or discussion is not review-open until it is marked ready for review or otherwise asks reviewers to judge the branch as a reviewable package.
- `merge-dependent language`: tracked wording such as "after merge", "post-merge", "once this lands", or equivalent wording that implies repo-local lifecycle state should change after merge.
- `known-stale project-map`: a `docs/project-map.md` with current evidence that its claims about the relied-on area conflict with repository paths, ownership, runtime flow, test layout, generated output, or another map claim. This refactor defines no calendar threshold.
- `workflow infrastructure`: the workflow spec, summary, skill guidance, and handoff pointers that govern how stages route and block.
- `on-demand artifact`: an artifact or action created only when the work depends on option expansion, external facts, or another explicit trigger.
- `per-change chain`: the stage sequence used to move one change from direction to reviewed PR package.
- `periodic artifact`: an artifact or action run on cadence, incident, repeated finding, postmortem action, or explicit maintainer request rather than for every change.
- `stage obligation`: one of `mandatory`, `conditional`, `on-demand`, or `periodic`.
- `ci-maintenance`: the visible workflow label for creating or updating hosted CI workflow files, validation automation, or platform configuration. It does not mean running validation.
- `review-requested`: the milestone state after implementation and targeted validation are complete and the milestone has been handed to `code-review`.
- `resolution-needed`: the milestone state after `code-review` produces findings that require review-resolution, fixes, owner decision, or re-review before the milestone can close.
- `autoprogression profile`: a closed workflow policy value that defines a bounded set of downstream stages a workflow-managed change may run without redundant confirmation.
- `authoring-through-plan-review`: the profile that may run `spec`, `spec-review`, recorded architecture assessment, conditional `architecture`, conditional `architecture-review`, `plan`, and `plan-review`, then stop.
- `implementation-through-verify`: the profile that may run settled `test-spec`, implementation milestones, independent `code-review`, bounded reviewer-declared correction loops, `explain-change`, and fresh `verify` according to phase authority, then stop before `pr`.
- `auto-fix classification`: reviewer-owned material-finding metadata that says whether a finding is not auto-fixable, mechanical, or declared safe for a deterministic recipe.
- `test-spec settlement`: deterministic evidence that the test spec is active, complete, synchronized with its inputs, and ready to authorize implementation.
- `profile phase`: the persisted rollout phase for `implementation-through-verify`, selected from `A`, `B`, or `C`.
- `proposal gate`: the artifact and review state proving that proposal direction is settled enough for downstream authoring.
- `gate-ready proposal`: a proposal whose artifacts and review evidence satisfy the proposal gate, independent of user authorization.
- `armed profile`: a user-authorized profile that is waiting for its activation gate.
- `architecture assessment`: the recorded workflow-managed micro-stage after approved `spec-review` that returns `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`.

## Examples first

### Example E1: standard workflow feature change

Given a contributor wants immediate feedback when adding or editing a skill
When they implement "Add a skill metadata validator and CI check"
Then the change follows the standard workflow, produces linked artifacts when their triggers apply, adds structural validation commands, creates durable reasoning before final verification, and ends with a PR that summarizes the change and links to durable reasoning.

### Example E2: manual skill invocation stays isolated

Given a user asks only for `verify` on the current branch
When the request does not ask to carry the change through the full workflow
Then `verify` returns its focused output and does not imply that proposal, spec, review, explanation, or PR stages are complete.

### Example E3: manual skill output is not workflow completion

Given a user manually invokes `pr` for a branch
When the `pr` skill prepares or opens a PR
Then that output does not claim that omitted upstream or downstream workflow stages were completed unless their evidence exists.

### Example E4: planned milestone work in one PR

Given a contributor executes planned milestone work under a concrete plan
When milestone `M1` and milestone `M2` both complete with updated plan evidence and milestone commits
Then one pull request may contain both milestone commits if the combined review unit is clearer than opening a separate pull request for each milestone.

### Example E5: single-slice change without milestone commit format

Given a contributor makes an unplanned single-slice change with no plan-defined milestone boundary
When they commit the change
Then the workflow does not require the `M<n>: <completed milestone outcome>` subject format for that commit.

### Example E6: workflow category routing

Given a contributor starts a non-trivial workflow-governance change
When they inspect the workflow contract
Then they see standing artifacts, living references, workflow infrastructure, on-demand artifacts, per-change stages, and periodic learning as distinct lifecycle categories instead of one overloaded linear prefix.

### Example E7: project-map no-reliance rule

Given architecture work depends on a repository map
When `docs/project-map.md` is absent, known-stale, contradicted by current repository structure, or missing the relied-on area
Then the contributor refreshes the map or records a no-map rationale before relying on repository-shape claims downstream.

### Example E8: review-resolution closeout gate

Given `code-review` records material findings for a non-trivial change
When those findings are still open or have non-final dispositions
Then final `explain-change`, `verify`, and `pr` do not proceed until required review-resolution closeout is complete.

### Example E9: CI maintenance is not validation execution

Given validation commands already exist and hosted CI can run them
When a contributor reaches verification
Then the `verify` stage owns validation evidence, while `ci-maintenance` runs only if hosted workflow automation or related CI infrastructure is missing, stale, or wrong for a material risk.

### Example E10: learn runs on triggers, not by default

Given a small ordinary change completes with no repeated findings, incidents, failed release smoke, postmortem action, cadence run, or maintainer request
When the PR package is ready
Then `learn` is not treated as a final per-change stage.

### Example E11: plan closes inside the completing PR

Given a planned initiative completes implementation, review-resolution, explain-change, verification, and PR handoff inside one branch
When the branch opens a review-open PR
Then `docs/plan.md` and the plan body both record the initiative as `Done` in that PR rather than promising post-merge closeout.

### Example E12: downstream completion keeps a plan active

Given a planned initiative depends on a later release or deploy before it is actually complete
When the code-change PR opens for review
Then the plan remains `Active`, names the downstream completion event, and defers the `Done` transition to a later PR or automation after that event.

### Example E13: broader lifecycle artifact state stays self-contained

Given a PR resolves every material review finding and records the required dispositions and evidence
When the PR opens for review after those fixes
Then `review-resolution.md` records `Closeout status: closed` in the same PR, and `verify` treats contradictory open closeout wording as stale lifecycle state.

### Example E14: isolated review recording follows the finding

Given a direct `spec-review` returns material finding `SR1`
And the contributor will revise a tracked spec in response
When the contributor prepares the revision
Then the direct review remains isolated for handoff, but `SR1` is recorded under `docs/changes/<change-id>/reviews/` before the spec edit begins.

### Example E15: review-resolution is scan-first and parseable

Given `proposal-review-r1` records seven accepted material findings
When `review-resolution.md` closes those findings with the same validation evidence
Then the file starts with closeout status, covered reviews, resolved and unresolved counts, and a resolution overview
And each finding detail keeps validator-readable labels for Finding ID, disposition, owner, owning stage, chosen action, rationale, validation target, and validation evidence.

### Example E16: milestone-aware clean review routing

Given a workflow-managed standard workflow change uses a milestone-based plan
And `code-review` returns clean for a clean non-final implementation milestone
When another in-scope implementation milestone remains open
Then the reviewed milestone closes and the next stage is the next in-scope implementation milestone, not `verify`.

### Example E17: final clean milestone reaches final closeout

Given a workflow-managed standard workflow change uses a milestone-based plan
And `code-review` returns clean for a clean final implementation milestone
When all in-scope implementation milestones are closed and no required review-resolution remains open
Then the next stage is `ci-maintenance` when triggered; otherwise it is `explain-change`, followed by `verify` and `pr`.

### Example E18: lifecycle closeout is not implementation work

Given all in-scope implementation milestones are closed
And the remaining plan work is a lifecycle-closeout milestone for `ci-maintenance`, `explain-change`, `verify`, or PR handoff
When no required review-resolution remains open
Then final closeout may proceed instead of treating the closeout milestone as unfinished implementation work.

### Example E19: proposal-gated authoring profile stops at plan-review

Given a proposal is accepted
And formal proposal-review is approved, recorded, and has no material findings or open blockers
And the user has authorized `auto-through: plan-review`
When workflow-managed execution resumes before spec authoring
Then the workflow may run `spec`, `spec-review`, recorded architecture assessment, required architecture stages, `plan`, and `plan-review`
And a clean `plan-review` reports `test-spec` next without invoking it.

### Example E20: direct review remains isolated despite an armed profile

Given `authoring-through-plan-review` is armed for a change
When the user directly invokes a review stage without workflow-managed resume context
Then the review result is recorded when required and downstream handoff remains isolated.

### Example E21: implementation profile stops before PR

Given clean planning completed
And the user separately authorized `auto-through: verify`
And `implementation-through-verify` phase `C` is active
When implementation milestones, independent review, `explain-change`, and fresh `verify` complete
Then the workflow reports `pr` as next and stops without opening a PR.

## Requirements

R1. The starter kit MUST support one recommended standard workflow. Public workflow guidance MUST NOT classify work as fast-lane, full-lane, tiny, low-risk, high-risk, small-change, or mini-spec routes.

R2. Users MAY manually invoke an individual skill, such as `implement`, `code-review`, `verify`, `explain-change`, or `pr`, for a focused task.

R3. Manual skill invocation MUST be isolated by default unless the user explicitly asks to continue through the standard workflow or workflow-managed context is already active.

R4. Manual skill output MUST NOT claim that the full standard workflow is complete and MUST NOT claim that omitted upstream or downstream stages have passed.

R5. Workflow completion claims MUST be supported by evidence from the relevant standard workflow stages, including review, final rationale, final verification, and PR readiness when those claims are made.

R6. The workflow contract MUST document workflow categories using the following category table:

| Category | Artifacts or stages | Creation rule | Revision or refresh rule | Staleness or absence check | Dependents |
| --- | --- | --- | --- | --- | --- |
| Standing artifacts | `VISION.md`, `CONSTITUTION.md` | Created once near project genesis or governance adoption. | Revised deliberately when project identity or governing principles change. | Absence gates differ by artifact and are defined in `R6a`. | All proposal, spec, workflow, and review stages. |
| Living references | `docs/project-map.md` | Created when repository structure is not obvious enough for safe architecture or planning. | Refreshed or bypassed with a no-map rationale before reliance when absent, known-stale, contradicted, or missing the relied-on area. | Detailed freshness markers, calendar thresholds, and revision workflow are deferred to a focused project-map lifecycle change. | Architecture, plan, code-review, and onboarding-heavy work. |
| Workflow infrastructure | `specs/rigorloop-workflow.md`, `docs/workflows.md`, affected root operating guidance, affected stage skills, and generated skill or adapter outputs when canonical skills change. | Created and maintained as workflow governance. | Revised when stage order, routing, handoff, obligation, or category policy changes. | Unresolved drift across affected operating and governance surfaces blocks workflow-change readiness. | Every lifecycle stage. |
| On-demand artifacts | `explore`, `research`. | Created only when the problem warrants durable option expansion or external evidence. | Revised when their assumptions or findings are materially outdated. | Absence is not a blocker unless the current work depends on unresolved options or uncertain facts. | Proposal, spec, architecture, and plan when their decisions depend on the artifact. |
| Per-change chain | `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution -> ci-maintenance -> explain-change -> verify -> pr`, with conditional stages governed by obligation metadata. | Created or run according to stage-obligation metadata. | Updated as the change moves through the lifecycle. | Missing required or triggered actions block downstream readiness. | The current change and PR package. |
| Periodic artifacts | `learn`. | Run on cadence, after incidents, contributor observations, repeated findings, failed release or adapter smoke, accepted postmortem actions, or explicit maintainer request. When a session reaches Frame, create or update `docs/learn/sessions/YYYY-MM-DD-<slug>.md`. | Revised by adding or updating session records, curated topic guidance, or affected action-owning artifacts, not by changing lifecycle state. | Absence does not block ordinary PRs. Triggered `learn` blocks only when a higher-priority artifact makes it blocking; if a trigger is closed before a session runs, the scheduled follow-up, deferral, or no-learn rationale must be recorded in a tracked or review-visible surface. | Future proposals, specs, workflow updates, skill refinements, ADRs, and action-owning artifacts. |

R6a. Standing artifacts include `VISION.md` and `CONSTITUTION.md`, but their absence has different gates. Their absence effects MUST be documented using the following table:

| Artifact | Role | Absence effect |
| --- | --- | --- |
| `VISION.md` | Project identity, target users, commitments, refusals, proposal-fit reference. | Blocks the first substantive proposal unless the proposal bootstraps vision. |
| `CONSTITUTION.md` | Repository governance, source-of-truth hierarchy, workflow principles. | Blocks governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal bootstraps constitution. |

R6b. `docs/project-map.md` MUST be treated as a living reference. Consumers MUST NOT rely on it when it is absent, known-stale, contradicted by the current repository, or missing the relied-on area. They MUST refresh it or record a no-map rationale.

R6c. This workflow refactor MUST NOT define calendar thresholds, freshness markers, or the full project-map revision workflow.

R6d. Workflow-governance changes MUST keep affected operating and governance guidance aligned. Affected surfaces MAY include `CONSTITUTION.md`, `AGENTS.md`, `README.md` when it contains workflow, contribution, or operating guidance, `docs/workflows.md`, `specs/rigorloop-workflow.md`, affected stage skills, generated `.codex/skills/`, and generated public adapters under `dist/adapters/` when canonical skills change.

R6da. A workflow-governance change MUST NOT be ready for downstream handoff until each affected surface is updated, explicitly marked unaffected with rationale, or recorded as deferred with owner and follow-up.

R6db. Unaffected-surface rationales and affected-surface deferrals under `R6da` MUST be recorded in a contributor-visible tracked or review-visible surface, such as the accepted proposal, approved spec, active plan, `docs/changes/<change-id>/change.yaml`, `review-resolution.md`, `explain-change.md`, PR body or draft PR body, linked issue, or the affected governance artifact. Chat-only notes MUST NOT satisfy this recording requirement.

R6dc. Workflow-governance changes that alter repo-local lifecycle synchronization MUST update `CONSTITUTION.md` with the changed governance rule. PR-self-contained lifecycle completion MUST be reflected in `CONSTITUTION.md` by stating that synchronization happens within the PR that performs the lifecycle transition before the PR opens for review, and that PR merge is a fast-forward of pre-validated state rather than a trigger for further lifecycle changes.

R6e. A substantive proposal is any proposal that chooses product direction, user-facing behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract.

R6f. `VISION.md` absence MUST block the first substantive proposal unless the proposal is bootstrap work to create or migrate the project vision.

R6g. `CONSTITUTION.md` absence MUST block governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal is bootstrap work to create or migrate the constitution.

R6h. Bootstrap proposals under `R6f` or `R6g` MUST identify the bootstrap exception in `Vision fit`, and `proposal-review` MUST check that exemption.

R6i. When architecture is required, the `architecture` stage MUST produce or update the architecture package defined by `specs/architecture-package-method.md` before planning continues. This workflow spec owns only stage-level routing and handoff for that method; the focused architecture package method spec owns the C4, arc42, ADR, template, and package lifecycle contract.

R6j. The `workflow` skill MUST own creation and refresh of `docs/workflows.md` when requested or when adopting RigorLoop into a project. The skill MUST NOT create or rewrite a local workflow spec unless the user explicitly requests workflow-contract authoring.

R6k. When `docs/workflows.md` is created or refreshed by the `workflow` skill, it MUST include:
- a source-of-truth note;
- one standard workflow;
- manual skill invocation and isolation behavior;
- stage obligation meanings;
- ordered workflow sequence;
- milestone-based implementation and review loop;
- `review-resolution` trigger;
- `ci-maintenance` boundary;
- `explain-change -> verify -> pr` final order;
- verify and PR ownership;
- learn trigger summary;
- skill index.

R6l. `docs/workflows.md` MUST remain a readable workflow guide and MUST NOT become a competing workflow spec.

R6m. When an active plan is affected by the transition to `explain-change -> verify -> pr`, the plan MUST record a transition note in its current handoff, readiness, or progress section.

R6n. The active plan transition note under `R6m` MUST state:
- the current final order is `explain-change -> verify -> pr`;
- prior verification evidence before `explain-change` is preliminary;
- final `verify` runs after `explain-change.md` exists and is current.

R7. The starter kit MUST document stage expectations using the following obligation model:
- `mandatory`: required whenever the row's trigger applies;
- `conditional`: required only when the trigger applies or the artifact/action is cited as a dependency;
- `on-demand`: created or run only when explicitly invoked or when the current work depends on its output;
- `periodic`: run on cadence, incident, repeated finding, failed smoke, accepted postmortem action, or explicit maintainer request rather than as a per-change stage.

R7a. The standard workflow MUST be documented using the following stage-obligation table. The `Runs for every change` column applies after the row trigger makes the stage applicable; it MUST NOT override the trigger column.

| Stage or action | Role | Obligation | Trigger | Runs for every change | Blocks downstream when missing |
| --- | --- | --- | --- | --- | --- |
| `explore` | Expand options. | `on-demand` | Strategic ambiguity, unclear problem framing, option expansion, architecture-level uncertainty, or maintainer request. | `false` | `true` |
| `research` | Verify external facts. | `on-demand` | Current external docs, APIs, versions, competitors, standards, laws, pricing, or operational facts affect the decision. | `false` | `true` |
| `proposal` | Choose direction. | `mandatory` | New direction, public behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract. | `true` | `true` |
| `proposal-review` | Challenge direction. | `conditional` | Workflow-governance, direction-setting, broad-impact, hard-to-reverse, or maintainer-requested proposals. | `false` | `true` |
| `spec` | Define behavior or contract. | `mandatory` | Externally observable behavior, workflow policy, schema, generated output, compatibility, security-sensitive behavior, or public contributor expectation changes. | `true` | `true` |
| `spec-review` | Check ambiguity and testability. | `mandatory` | Behavior, workflow, schema, compatibility, or safety-sensitive changes. | `true` | `true` |
| `architecture` | Define system shape. | `conditional` | Boundary, data flow, generated package, CI infrastructure, integration, storage, deployment, or long-lived design impact. | `false` | `true` |
| `architecture-review` | Challenge design. | `conditional` | Broad-impact, cross-component, migration-heavy, security-sensitive, boundary-changing, or hard-to-reverse design. | `false` | `true` |
| `plan` | Sequence implementation. | `conditional` | Multi-file, risky, ambiguous, migration-heavy, sequencing-sensitive, or milestone-based work. | `false` | `true` |
| `plan-review` | Validate execution plan. | `conditional` | Multi-milestone, sequencing-sensitive, recovery-sensitive, or maintainer-requested work. | `false` | `true` |
| `test-spec` | Define proof. | `mandatory` | Behavior or workflow-contract proof is required. | `true` | `true` |
| `implement` | Make the change. | `mandatory` | The accepted contract is ready to change tracked artifacts. | `true` | `true` |
| `code-review` | Inspect the diff. | `mandatory` | Non-trivial changes. | `true` | `true` |
| `review-resolution` | Close review findings. | `conditional` | Material review findings, non-final dispositions, or review outcomes require explicit closeout. | `false` | `true` |
| `ci-maintenance` | Create or update hosted CI workflow automation, validation automation, or related platform configuration. | `conditional` | Hosted workflow automation, validation automation, or related platform configuration for a material risk must be created or changed. | `false` | `true` |
| `explain-change` | Explain final diff. | `mandatory` | Non-trivial changes require standalone durable explanation; all changes require PR-summary explanation. | `true` | `true` |
| `verify` | Prove result. | `mandatory` | Every contributed change. | `true` | `true` |
| `pr` | Prepare review package. | `mandatory` | Every contributed change. | `true` | `true` |
| `learn` | Capture retrospective lessons. | `periodic` | Cadence run, incident response, contributor observation, repeated review findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem action changing workflow guidance, or explicit maintainer request. | `false` | `false` |

R7b. For conditional and on-demand rows, downstream blocking applies only after the trigger is active, the artifact/action has been cited as a dependency, or a higher-priority artifact requires it. For periodic rows, downstream blocking applies only when a higher-priority artifact explicitly makes the triggered periodic work blocking.

R7ba. `learn` is a periodic or explicitly invoked retrospective artifact. A cadence run, incident response, contributor observation, repeated review finding, blocker or major workflow-process finding, failed release or adapter smoke, accepted postmortem action changing workflow guidance, or explicit maintainer request MUST be sufficient to trigger `learn`.

R7bb. Triggered `learn` MUST NOT block ordinary final `explain-change`, `verify`, or `pr` closeout by default.

R7bc. Triggered `learn` MUST block downstream only when a higher-priority artifact explicitly makes it blocking, such as an active plan, `review-resolution`, postmortem action, release contract, or maintainer decision.

R7bd. If a `learn` invocation reaches the `Frame` phase, it MUST create or update a tracked session record under `docs/learn/sessions/YYYY-MM-DD-<slug>.md`. This requirement applies even when the session finds no observations or no durable lesson.

R7be. Review-visible no-record surfaces for scheduled follow-up, deferral, or explicit no-learn rationale MUST be allowed only for pre-session trigger closeout when `learn` does not actually run as a session. Chat-only notes MUST NOT satisfy required tracked or review-visible closeout.

R7bf. Learn session routing MUST follow `specs/learn-artifact-model.md`: session records live under `docs/learn/sessions/`, durable topic guidance lives under `docs/learn/topics/` only when confirmed durable lessons justify it, and behavior, workflow, validation, skill, architecture, or decision changes go to the affected action-owning artifact. Topic files are curated guidance and MUST NOT override authoritative artifacts.

R7c. The starter kit MUST distinguish workflow-managed completion flows from isolated stage requests when deciding whether a stage result should continue automatically into a downstream stage.

R7d. When an approved continuation contract applies, a workflow-managed completion flow MUST continue automatically into the next mandatory or triggered downstream stage for the current workflow state unless a documented stop condition applies. Redundant user re-invocation MUST NOT be required merely to enter that already-known downstream stage.

R7e. Unless a later approved change broadens scope, continuation applies only to:
- authoring-to-review handoffs for `proposal`, `spec`, and `architecture` when the matching review stage is the next mandatory or triggered downstream step;
- standard workflow execution flow from `implement` through `pr`;
- the separately armed `authoring-through-plan-review` profile;
- the separately armed `implementation-through-verify` profile.

R7ea. The closed autoprogression profile values are `off`, `authoring-through-plan-review`, and `implementation-through-verify`.

R7eb. Unknown autoprogression profile values MUST fail closed before downstream execution.

R7ec. `auto-through: plan-review` is the user-facing authorization for `autoprogression.profile: authoring-through-plan-review`.

R7ed. `authoring-through-plan-review` MUST be explicitly authorized by the user for one change and MUST NOT be enabled by a repository-wide default.

R7ee. The profile MUST activate only when both the profile is armed and the proposal gate passes.

R7ef. The proposal gate MUST require an existing accepted proposal, approved recorded proposal-review, no proposal-review material findings, no open proposal blockers, proposal scope and non-goals settled enough for spec, non-blocking proposal open questions, satisfied standing artifact gates, and unambiguous change ID and artifact placement.

R7eg. User authorization MUST NOT be treated as proposal-gate evidence. An unarmed but otherwise gate-ready proposal is gate-ready with profile `off`.

R7eh. When active, `authoring-through-plan-review` MUST run only `spec`, `spec-review`, recorded architecture assessment, conditional `architecture`, conditional `architecture-review`, `plan`, and `plan-review`.

R7ei. `authoring-through-plan-review` MUST stop after clean `plan-review`, mark the profile completed, and report `test-spec` as the next stage without invoking it.

R7ej. `authoring-through-plan-review` MUST NOT run `test-spec`, implementation, code-review, explain-change, verify, pr, release, deploy, merge, or automatic review-fix loops.

R7ek. After approved `spec-review`, the active profile MUST record architecture assessment as `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`.

R7el. `architecture-ambiguous` MUST pause the profile. `architecture-required` MUST route to `architecture` and `architecture-review` unless another stop condition applies. `architecture-not-required` MUST route to `plan` unless another stop condition applies.

R7em. Review stages run by the profile MUST remain independent formal review stages. They MUST inspect tracked artifacts, use formal review criteria, record results before downstream routing, and avoid editing the reviewed artifact during review.

R7en. The profile MUST pause on incomplete proposal gate, missing required artifact, ambiguous artifact placement, review recording failure, non-approved review status, material finding, open `needs-decision`, proposal/spec conflict, architecture ambiguity, owner-selection requirement, unresolved upstream ambiguity, contradictory workflow state, unreliable partial stage completion, transition-budget exhaustion, user pause, or user cancellation.

R7eo. User cancellation MUST set the profile to `off`. Manual fixes MUST NOT auto-resume a paused profile.

R7ep. The normal profile transition budget MUST be six stage slots per activation: `spec`, `spec-review`, `architecture`, `architecture-review`, `plan`, and `plan-review`. Unneeded architecture slots are skipped slots, not permission to run other stages.

R7eq. A resumed profile after explicit rereview authorization MUST be limited to remaining uncompleted stages plus explicitly authorized rereview stages.

R7er. Profile policy metadata MUST be recorded change-locally before any profile-driven transition. The workflow MUST persist profile authorization at `docs/changes/<change-id>/change.yaml` as the canonical surface, falling back to `docs/changes/<change-id>/workflow-policy.yaml` only when the change-metadata contract explicitly rejects policy data.

The workflow MUST pause and report a stop condition when, at activation time, no durable authorization record exists, the record is malformed, required fields are missing, the record is partially written, or the persistence write fails. Persistence failures are stop conditions, not retry conditions.

The workflow MUST NOT use profile policy metadata as the live owner of current stage, next stage, review status, branch readiness, or PR readiness. Existing workflow-state surfaces continue to own those fields.

R7es. Additional profiles, including `authoring-through-test-spec` and future implementation profiles beyond `implementation-through-verify`, require separate proposal and spec amendments. Existing profiles MUST NOT be widened silently.

R7et. `implementation-through-verify` MUST be authorized separately from `authoring-through-plan-review`; authoring-profile authorization MUST NOT imply implementation-profile authorization.

R7eu. `implementation-through-verify` MUST activate only after clean planning, explicit ordered implementation milestones, complete test-spec inputs, durable authorization persistence, clean governing artifacts, recorded working-tree baseline, approved commands, absent or excluded unrelated dirty changes, and workflow-state synchronization.

R7ev. `implementation-through-verify` MUST persist phase `A`, `B`, or `C` and MUST refuse transitions outside the persisted phase.

R7ew. Phase `A` is audit-only, Phase `B` may run through final clean code-review but not `explain-change` or `verify`, and Phase `C` may run `explain-change` and fresh `verify` only after promotion evidence is linked.

R7ex. Before implementation, `implementation-through-verify` MUST run deterministic test-spec settlement and record input artifact identities. The first milestone's code-review MUST recheck those identities and pause on mismatch.

R7ey. Every implementation milestone under `implementation-through-verify` MUST run in approved order and receive independent code-review before closing.

R7ez. Under `implementation-through-verify`, material code-review findings MUST include reviewer-owned `auto_fix_class`; missing classification is `none` and pauses the profile.

R7faa. Automatic correction under `implementation-through-verify` MUST be limited to reviewer-classified `mechanical` or `declared-safe` findings that include the fields required by the focused autoprogression and review-finding contracts.

R7fab. Automatic correction rounds under `implementation-through-verify` MUST be limited to three per milestone, strictly shrink unresolved findings, pause on new finding IDs or classes, remain path-local, avoid new scope, avoid substantive governing-artifact edits, and use only approved commands.

R7fac. `implementation-through-verify` MUST require final full code-review before `explain-change`, fresh actual-run verify evidence in Phase C, and a pause without repair on verify failure.

R7fad. Successful `implementation-through-verify` completion MUST compute branch readiness from recorded verify evidence through workflow-state synchronization, report `pr` next, require human authorization for `pr`, and MUST NOT invoke `pr`.

R7f. In v1, manual skill invocations and bugfix skill invocations remain isolated or explicit-step by default, and on-demand or periodic actions such as `explore`, `research`, and `learn` MUST NOT auto-run unless the user explicitly requests them or a later approved rule elevates them.

R7g. Direct invocation of `pr` remains allowed. Isolation prevents downstream continuation beyond `pr`, but it MUST NOT downgrade `pr` itself from opening a pull request when readiness passes.

R7h. Workflow-facing review outputs that report both stage handoff and later-stage fitness MUST distinguish the `Immediate next stage` result field from downstream readiness.

R7i. `spec-review` output MUST report review outcome, `Immediate next stage`, and eventual `test-spec` readiness separately.

R7j. `spec-review` `Immediate next stage` MUST use exactly one of:
- `spec revision`;
- `review-resolution`;
- `architecture`;
- `plan`;
- `none`.

For forward repository-stage handoff values, `spec-review` uses:
- `architecture` when the review outcome is approved and a separate architecture step remains required;
- `plan` when the review outcome is approved and no separate architecture step remains required.

The values `spec revision`, `review-resolution`, and `none` are revision, disposition, or no-handoff routing values, not forward repository-stage handoff values.

R7k. `spec-review` eventual `test-spec` readiness MUST use exactly one of:
- `ready`;
- `conditionally-ready`;
- `not-ready`.

R7l. Approved `spec-review` MUST pair only with eventual `test-spec` readiness `ready` or `conditionally-ready`. `conditionally-ready` MUST name the remaining intermediate dependency or dependencies.

R7m. `changes-requested`, `blocked`, and `inconclusive` spec-review outcomes MUST pair with eventual `test-spec` readiness `not-ready`.

R7n. When eventual `test-spec` readiness is `not-ready`, the output MUST state that downstream planning stops, name the required upstream fix surface as `spec revision` or `review-resolution`, and identify the blocking defect category. For inconclusive reviews, the output MUST use `Immediate next stage: none` and record the stop condition and missing required input.

R7o. Missing input and blocker conditions MUST be expressed as stop conditions rather than pseudo-routing states in immediate-next-stage fields.

R7p. `plan-review` remains the normal immediate handoff into `test-spec`. If it reports implementation readiness or other later-stage fitness, it MUST present that as downstream readiness rather than replacing the immediate `test-spec` handoff.

R7q. `test-spec` authoring MUST continue to require an approved feature spec, spec-review findings, a concrete execution plan, and approved architecture or ADR inputs when relevant to the changed boundaries.

R7r. Workflow-facing execution and review stages MUST keep stage-owned language and branch-scoped authority claims distinct.

R7ra. `implement` MAY report implementation completion, milestone validation, blockers, readiness for `code-review`, or the next milestone, but it MUST NOT claim completed review findings or `branch-ready`.

R7rb. `code-review` owns first-pass review findings and review-status conclusions.

R7rc. `verify` owns `branch-ready`.

R7rd. `pr` owns `pr-body-ready` and `pr-open-ready`.

R7re. Workflow-facing outputs SHOULD avoid unqualified `PR-ready` as live guidance or status language. Unqualified `PR-ready` MAY remain only as negative guidance, historical context, or a quoted term definition.

R7s. The tracked-branch requirement MUST apply to branch-scoped authority and readiness claims, not as a blanket rule that every reviewed code change is already committed.

R7sa. `code-review` MAY inspect a review surface consisting of changed files, staged changes, unstaged diffs, PR diffs, or commit ranges, depending on the review context.

R7sb. When `code-review` cites a governing artifact as authoritative support for a clean branch-scoped conclusion, it MUST confirm that artifact is present in tracked governing branch state.

R7sc. A local-only governing artifact MAY inform reviewer background understanding, but it MUST NOT support a clean branch-scoped conclusion.

R7t. Missing tracked governing authority MUST prevent `clean-with-notes`, but it MUST NOT suppress independently supported findings.

R7ta. When the review surface independently supports a fixable defect, `code-review` MUST use `changes-requested` even if tracked governing authority for a clean result is incomplete.

R7tb. When the review surface independently supports a blocking defect, `code-review` MUST use `blocked` even if tracked governing authority for a clean result is incomplete.

R7tc. `code-review` MUST use `inconclusive` only when missing evidence prevents both a supported finding and a clean conclusion.

R7u. When `verify` evaluates `branch-ready`, required authoritative artifacts missing from tracked governing branch state MUST be treated as a blocking condition.

R7v. Clean branch-scoped review conclusions for named edge cases MUST cite direct proof. Code-shape inference alone is insufficient.

R7va. Actionable named edge-case proof gaps MUST be reported as findings rather than allowed inside a clean result.

R7vb. Unresolved named edge-case proof gaps MUST block `branch-ready`.

R7w. These branch-reality and traceability rules supplement the earlier `code-review` independence contract. They MUST NOT remove the first-pass review record, approved review statuses, workflow-managed `review-resolution` handoff for fixable findings, or isolated-review stop behavior defined by the governing workflow artifacts.

R7x. For a milestone-based plan, each implementation milestone MUST have exactly one authoritative `Milestone state` selected from:
- `planned`;
- `implementing`;
- `review-requested`;
- `resolution-needed`;
- `closed`.

R7xa. `review-requested` means implementation and targeted validation are complete, and the milestone has been handed to `code-review`.

R7xb. `resolution-needed` means `code-review` produced findings that require review-resolution, fixes, owner decision, or re-review before the milestone can close.

R7xc. `implementation-complete` and `review-clean` MAY appear as evidence descriptions, but they MUST NOT be milestone state values.

R7xd. In a milestone-based plan, a clean non-final implementation milestone MUST close the reviewed milestone and hand off to the next in-scope implementation milestone, not `verify`.

R7xe. In a milestone-based plan, a clean final implementation milestone MUST close the reviewed milestone and may hand off to final closeout only when all in-scope implementation milestones are closed and no required review-resolution remains open.

R7xf. In a milestone-based plan, review-resolution and fix loops MUST stay attached to the reviewed milestone until findings are dispositioned and required fixes, validation, owner decisions, and re-review obligations are closed.

R7xg. In a milestone-based plan, `code-review` MUST move the reviewed milestone to `resolution-needed` when findings require review-resolution, fixes, owner decision, or re-review. The workflow MUST NOT advance to the next implementation milestone, `ci-maintenance`, final `explain-change`, `verify`, or `pr` while that required milestone closeout remains open.

R7xh. In a milestone-based plan, if the reviewed milestone, remaining in-scope implementation milestones, review status, or required review-resolution state cannot be determined from the active plan and review output, the workflow MUST stop as inconclusive or require a plan update instead of handing off to final closeout.

R7xi. In a milestone-based plan, milestones MUST NOT be postponed or hidden solely to make final closeout available. If a planned milestone no longer belongs in the current change, the plan MUST be revised before downstream handoff, and final closeout may proceed only after no in-scope implementation milestone remains open or unresolved.

R7xj. A lifecycle-closeout milestone MUST NOT be treated as an unfinished implementation milestone for final closeout readiness decisions. A mixed milestone that still contains implementation work remains an in-scope implementation milestone until that implementation work is closed or the plan is revised.

R8. The starter kit MUST treat the following stages as mandatory for every contributed change:
- implement;
- verify;
- pr.

R8a. For planned milestone work, milestone implementation handoff evidence MUST NOT be treated as complete until all of the following are true:
- the milestone deliverable is complete;
- relevant validation for that milestone has passed;
- when targeted tests are applicable, those tests have passed;
- when targeted tests are not applicable, a contributor-visible no-test rationale has been recorded;
- the concrete plan's progress and validation notes reflect the milestone outcome;
- any milestone-level decision changes are recorded in the plan or related artifact;
- the milestone changes are committed to git as one coherent milestone commit with no unrelated changes included.

R8aa. The implementation handoff evidence in `R8a` does not by itself make a milestone `closed` in a milestone-based plan. The milestone reaches `closed` only after clean `code-review` with no required review-resolution, or after required review-resolution and re-review or owner closeout are complete.

R8b. A completed milestone commit MUST use the subject format:
- `M<n>: <completed milestone outcome>`

R8c. A completed milestone commit SHOULD include a short body that summarizes the milestone deliverable and records milestone validation command output or a reference to contributor-visible validation evidence.

R8d. The workflow MUST allow a pull request to contain one or more completed milestone commits. A completed milestone only needs a separate pull request when it is independently reviewable, independently verified, and safe to merge on its own.

R8e. The milestone commit requirements in `R8a` through `R8d` apply only to planned milestone work. Manual skill invocations and non-trivial single-slice changes without a plan-defined milestone boundary MAY use normal commit subjects and do not require milestone-formatted commits.

R8f. For planned initiatives, `docs/plan.md` MUST remain the lifecycle index rather than the body of a plan.

R8g. For planned initiatives, `implement` MUST keep the active plan body's progress, decisions, discoveries, and validation notes current during execution. When lifecycle state changes, final lifecycle closeout MUST update both `docs/plan.md` and the plan body.

R8h. Synchronization of `docs/plan.md` and the plan body MUST happen within the PR that performs the planned-initiative lifecycle transition, before that PR opens for review. The merge of a PR MUST be treated as a fast-forward of pre-validated repository state, not as a trigger for further planned-initiative lifecycle changes.

R8ha. When a PR performs the work that completes a planned initiative, the PR MUST record the `Done` transition in both `docs/plan.md` and the plan body before it opens for review.

R8hb. When planned-initiative completion depends on a downstream completion event, the PR MUST keep the plan `Active`, name the downstream event or follow-up condition in contributor-visible plan wording, and defer the `Done` transition to a later PR or repository-owned automation after that event occurs.

R8hc. A planned initiative MUST NOT use merge itself as a routine downstream completion event. Merge-SHA recording rules are out of scope until a later approved spec defines them.

R8i. `Blocked` and `Superseded` lifecycle transitions for planned initiatives MUST be recorded as soon as they are decided.

R8j. `verify` MUST treat stale lifecycle state between `docs/plan.md` and the plan body as blocking `branch-ready` for planned initiatives.

R8ja. At minimum, stale lifecycle state includes:
- a completed, blocked, or superseded planned initiative still listed under `## Active`;
- `docs/plan.md` and the corresponding plan body presenting conflicting lifecycle state;
- a plan body marked done, blocked, or superseded while still presenting itself as active or in progress through status or readiness wording.

R8jb. A PR that opens for review with merge-dependent language in tracked plan lifecycle wording MUST classify that language as either a true downstream completion event or stale lifecycle wording requiring correction.

R8k. Top-level lifecycle-managed workflow artifacts MUST keep their lifecycle status inside the artifact itself as tracked source of truth. Git branch state, PR state, merge state, and chat-only review outcomes MUST NOT replace artifact-local lifecycle state for proposals, top-level specs, test specs, architecture documents, or ADRs.

R8ka. The starter kit MUST document the repository-wide artifact lifecycle summary using the following table:

| Artifact | Required for | Authoring skill | Review skill | Settlement states | Closeout or terminal states |
| --- | --- | --- | --- | --- | --- |
| Proposal | non-trivial direction choice | `proposal` | `proposal-review` | `accepted` | `rejected`, `abandoned`, `superseded`, `archived` |
| Spec | behavior changes | `spec` | `spec-review` | `approved` | `abandoned`, `superseded`, `archived` |
| Architecture | boundary or system-shape changes | `architecture` | `architecture-review` | `approved` | `abandoned`, `superseded`, `archived` |
| Test spec | behavior proof | `test-spec` | repository-defined review surface | `active` | `abandoned`, `superseded`, `archived` |
| ADR | long-lived design decision | `architecture` | `architecture-review` when relevant | `accepted`, `active` | `deprecated`, `superseded`, `archived`, `abandoned` |

R8kb. Detailed per-artifact lifecycle rules MUST be delegated to the canonical template, example, and skill surfaces for each artifact class instead of being duplicated in full inside this workflow spec.

R8kc. For proposals, top-level specs, test specs, and architecture documents, `reviewed` MUST be treated as transitional review output rather than a durable relied-on artifact state.

R8kd. Settlement and closeout MUST remain distinct:
- `accepted`, `approved`, and `active` are settlement states that may still be relied on as current guidance;
- `done`, `deprecated`, `rejected`, `abandoned`, `superseded`, and `archived` are closeout or terminal states.

R8ke. `Next artifacts` MUST record planned next steps while an artifact remains active. `Follow-on artifacts` or `Closeout` MUST record actual downstream artifacts, replacement, or terminal disposition, and a premature `Follow-on artifacts` section MUST say `None yet` instead of remaining empty.

R8kf. `verify` MUST block on stale or inconsistent lifecycle-managed artifacts that are touched, referenced, generated, or authoritative for the changed area, and it MUST report unrelated stale baseline artifacts as warnings rather than blockers.

R8kg. PR-body references participate in `verify` only when draft PR text already exists. Before PR text exists, `verify` MUST use the pre-PR handoff surfaces such as `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, and the touched, referenced, generated, or authoritative artifacts for the changed area.

R8kh. When a PR performs the work that makes a repo-local lifecycle state true for a lifecycle-managed artifact, review-resolution closeout, change-local artifact, readiness surface, or terminal artifact state, the PR MUST record that lifecycle state before it opens for review.

R8ki. Broader lifecycle artifact inconsistency MUST block `branch-ready` when the inconsistent artifact is touched, referenced, generated, or authoritative for the changed area. At minimum, broader lifecycle artifact inconsistency includes:
- a lifecycle-managed proposal, spec, test spec, architecture document, or ADR whose status conflicts with the PR-contained evidence it relies on;
- `review-resolution.md` saying `Closeout status: open` after all material findings have final dispositions and required closeout evidence in the PR;
- `review-resolution.md` saying `Closeout status: closed` while required findings, dispositions, rationale, follow-up, validation evidence, or `review-log.md` closeout evidence remain missing;
- active test-spec, verify, explain-change, or change-local readiness wording that describes the PR as incomplete after the PR has completed and recorded its own scope.

R8kj. Repository-owned validation or review guidance MUST flag merge-dependent language in tracked files as a non-blocking reviewer-attention warning unless another requirement makes the specific lifecycle inconsistency blocking. The first enforcement slice MUST NOT require inspecting hosted PR-description event metadata.

R8l. Non-trivial implementation and review handoff SHOULD use targeted proof before broad smoke when the repository-owned selector can classify the changed surfaces.

R8m. Targeted proof SHOULD be selected through `python scripts/select-validation.py` or executed through `scripts/ci.sh --mode explicit --path <path>...` when explicit changed paths are known.

R8n. Selector-selected checks MUST use stable check IDs such as `skills.validate`, `review_artifacts.validate`, and `broad_smoke.repo` rather than prose-only validation categories.

R8o. `scripts/ci.sh` is an execution wrapper for selected checks. Running the wrapper in PR or explicit mode does not imply broad smoke for every PR.

R8p. Broad smoke MUST be triggered by an authoritative source, such as selector mode `main` or `release`, an explicit `--broad-smoke` request, active plan field `broad_smoke_required: true`, test-spec requirement, review-resolution requirement, or release metadata.

R8q. Planned initiatives MUST record targeted proof during implementation or review handoff and broad smoke evidence before final `verify` branch-ready closeout.

R8r. Required manual proof for normal changes MUST be stored durably in `docs/changes/<change-id>/verify-report.md` when standalone verification evidence is required, and release smoke manual proof MUST remain in release metadata under `docs/releases/<version>/`.

R8s. Manual proof records MUST identify the check, result, performer, date, evidence, and why it is `manual by design`; `fail`, `blocked`, and `not-run` results keep handoff open unless a governing release or stage contract explicitly allows the temporary state.

R9. Once repository CI exists, the starter kit MUST treat routine CI validation results as enforced for every pull request.

R9a. In the lifecycle stage table, `ci-maintenance` MUST refer to creating or updating hosted CI workflow files, validation automation, or related platform configuration needed to cover material change risk. It MUST NOT refer to running validation, designing tests, specifying validation commands, or waiting for existing CI checks to run.

R9b. The `skills/ci-maintenance/` path is the skill entrypoint for CI infrastructure work. Contributor-visible workflow guidance uses `ci-maintenance` for the stage/action label and keeps validation execution under `verify`.

R10. The starter kit MUST treat `explain-change` as:
- required in PR summary form for every change;
- required as a standalone durable artifact for non-trivial changes.

R10a. For new non-trivial work, the default standalone durable reasoning artifact MUST be `docs/changes/<change-id>/explain-change.md`.

R10b. PR text alone MUST NOT satisfy the standalone durable reasoning requirement for non-trivial work.

R10c. The only allowed equivalent to the default standalone durable reasoning artifact is another artifact class explicitly named by this workflow spec as satisfying durable reasoning for the change.

R10d. Approved legacy top-level explain artifacts, including approved artifacts under `docs/explain/`, MUST remain valid durable reasoning surfaces until they are migrated, superseded, archived, or otherwise retired.

R10e. New top-level explain artifacts MUST NOT be created unless this workflow spec explicitly allows that artifact class.

R10f. Final `explain-change` MUST run before final `verify` so final `verify` can validate the completed change-local pack, including durable reasoning.

R10g. Before final `verify`, `explain-change` MAY summarize implementation scope, review outcomes, validation commands already run, known validation gaps, and expected final verification checks. It MUST NOT claim final `verify`, `branch-ready`, PR-ready, or CI-final status.

R10h. `verify` MUST validate that the required explain-change artifact exists, is current, and matches the final changed surfaces. If it is missing or stale, `verify` MUST route back to `explain-change` instead of creating the explanation itself.

R11. The starter kit MUST define the explain-change split as follows:
- PR text carries reviewer-facing summary;
- durable Markdown artifacts carry reusable reasoning;
- structured metadata carries machine-readable traceability.

R12. For non-trivial changes, PR text MUST include:
- what changed;
- why it changed;
- validation run or no-test rationale;
- review focus or major risk;
- links to relevant durable artifacts when they exist.

R12a. A material review finding MUST include:
- evidence supporting the finding;
- the required outcome needed to satisfy the review gate;
- a safe resolution path or a `needs-decision` rationale naming the authorized owner decision needed before a safe resolution can be chosen.

R12aa. A material review finding that lacks evidence, required outcome, or either a safe resolution path or decision-needed rationale MUST be treated as incomplete and MUST NOT silently drive review-resolution or fixes.

R12ab. Material review findings MUST be recorded before review-driven fixes begin. If fixes already began before a durable review record existed, the durable record MUST be labeled as reconstructed and preserve the original review source, available evidence, after-fix timing disclosure, stable finding IDs, and any known loss of fidelity.

R12ac. When formal lifecycle review findings are recorded under `docs/changes/<change-id>/reviews/`, `docs/changes/<change-id>/review-log.md` MUST exist and every material Finding ID MUST appear in `docs/changes/<change-id>/review-resolution.md`.

R12ad. Review-resolution dispositions MUST use only:
- `accepted`;
- `rejected`;
- `deferred`;
- `partially-accepted`;
- `needs-decision`.

R12ae. `needs-decision` is not a final disposition. It is an unresolved stop state and MUST block `explain-change`, `verify`, and `pr` until an authorized owner resolves the decision or explicitly defers it.

R12af. `review-resolution.md` MUST have a top-level closeout status of exactly `Closeout status: open` or `Closeout status: closed`.

R12ag. `Closeout status: open` means one or more material findings are not yet fully resolved for handoff. `Closeout status: closed` means every material finding has a final disposition, all disposition-specific closeout requirements are satisfied, and `review-log.md` lists no open findings.

R12ah. A finding with disposition `accepted` may count toward `Closeout status: closed` only when the chosen action and validation evidence are recorded.

R12ai. A finding with disposition `rejected` may count toward `Closeout status: closed` only when rationale is recorded.

R12aj. A finding with disposition `deferred` may count toward `Closeout status: closed` only when deferral rationale and a follow-up owner, owning stage, or explicit no-follow-up reason are recorded.

R12ak. A finding with disposition `partially-accepted` may count toward `Closeout status: closed` only when the accepted portion has action and validation evidence, and the rejected or deferred portion has its required rationale and follow-up or no-follow-up record.

R12al. A first-pass review outcome that requires revision, changes, or blocks downstream progress MUST be closed by a valid same-stage later review round or by explicit reviewer or owner closeout evidence naming the original Review ID. `review-resolution.md` alone MUST NOT silently replace required re-review or owner closeout.

R12am. Final `explain-change`, `verify`, and `pr` handoff MUST NOT proceed while `review-log.md` still lists open findings.

R12an. A detailed review file MUST be created for a formal lifecycle review when the review produces material findings; returns a stage-owned non-approval outcome that blocks downstream progress or requires revision; is reconstructed; will be cited as closeout evidence; or is explicitly requested by a reviewer or maintainer.

R12ana. Material findings MUST always be recorded.

R12anb. All material findings MUST require change-local review files.

R12ao. Formal lifecycle review stages for detailed review files are `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`. A dedicated `pr-review` detailed file MUST NOT be used unless a later approved spec extends the allowed stage set and validator.

R12ap. Stage-owned non-approval outcomes MUST include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent stage-specific outcomes that prevent downstream progress.

R12aq. A clean formal review with no material findings MUST NOT require an empty detailed review file solely because the review was required. It MAY be recorded through artifact-local settlement when no detailed-record trigger applies.

R12ar. When a workflow-managed formal review triggers a detailed review file before a change-local root exists, the change MUST create an initial review-record root before review-driven fixes or downstream routing proceed.

R12as. If material findings exist, a detailed review file is required, and `review-resolution.md` is required, the initial review-record root MUST include `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/<stage>-r<n>.md`.

R12at. If a detailed review file is required but `review-resolution.md` is not required, the initial review-record root MUST include `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`. It MUST NOT include an empty `review-resolution.md` solely because `reviews/` exists.

R12au. The initial review-record root MUST NOT be treated as the final non-trivial change-local pack. Final handoff for non-trivial work still needs `change.yaml` plus durable Markdown reasoning under `R14b`.

R12av. Review files MUST preserve review event evidence and finding closeout. They MUST NOT replace proposal, spec, architecture artifact, ADR, or plan status.

R12aw. Isolation MUST govern formal review handoff only; recording MUST follow the finding.

R12ax. A direct or review-only formal lifecycle review request MUST remain isolated by default and MUST NOT automatically continue into downstream workflow stages.

R12ay. Isolation MUST NOT suppress material-finding recording.

R12az. A material finding MUST have a durable change-local review record under `docs/changes/<change-id>/reviews/`, regardless of whether the review was workflow-managed or isolated. When the finding drives fixes or downstream routing, the record MUST exist before review-driven edits or routing begin.

R12ba. If review-driven edits already began before the durable record exists, the detailed review file MUST be reconstructed and MUST disclose source, timing, available evidence, stable Finding IDs, and known fidelity loss.

R12bb. A tracked artifact MUST be any version-controlled repository file whose change will be committed or reviewed as part of the work. Tracked artifacts include lifecycle artifacts, governance files, workflow summaries, skills, specs, schemas, scripts, generated outputs, README content, and change-local artifacts. Ephemeral chat output, local scratch files, and unversioned drafts MUST NOT be treated as tracked artifact edits.

R12bc. For review recording decisions, a finding MUST be treated as material when it changes or blocks a tracked artifact edit, changes scope, changes requirements, changes architecture, changes sequencing, changes validation, creates follow-up work, or requires disposition, unless the reviewer explicitly records a non-material rationale.

R12bd. For an isolated or review-only formal review with material findings, final review output MUST show that isolation stops handoff, not recording.

R12bda. The output MUST state no automatic downstream handoff, material Finding IDs, required review record path, whether the record must be created before fixing or reconstructed, and whether owner decision is needed.

R12bdb. The output MUST make the next action clear without requiring enum-style action strings.

R12bdc. The output MUST NOT offer review-output-only or artifact-local-only settlement for material findings.

R12bdd. `review-resolution.md` is required when material findings exist.

R12be. Canonical formal review skills MUST include one identical `## Isolation and Recording` subsection copied from `templates/shared/review-isolation-and-recording.md`. Static validation MUST compare each copied skill subsection against that canonical source byte-for-byte and MUST fail if stage-specific guidance appears inside the shared block.

R12bf. New `review-resolution.md` records MUST remain scan-first for humans while preserving validator-readable field labels for each material finding.

R12bg. The material-finding recording trigger MUST NOT be implemented until affected governance and operating guidance are updated or explicitly marked unaffected with rationale. `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` MUST use the same rule: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.

R12b. Routine non-material review notes MAY remain in PR body, the explain-change artifact, or another contributor-visible review surface when they do not require material finding disposition.

R12c. A standalone `review-resolution.md` artifact MUST be used when any of the following is true:
- a non-trivial change has material review findings;
- review feedback changes behavior defined by the spec;
- review feedback changes architecture or ADR direction;
- review feedback changes the implementation plan;
- review feedback changes test strategy;
- review feedback raises security, correctness, compatibility, or data-risk concerns that future maintainers must understand;
- review feedback creates rejected, deferred, partially accepted, or decision-needed items with durable project value;
- the change goes through multiple material review rounds;
- a maintainer explicitly requests a standalone review-resolution artifact.

R12ca. PR text and explain-change summaries MUST keep review-resolution details concise. When `review-resolution.md` exists, they SHOULD summarize counts by disposition and link the artifact instead of duplicating every detailed finding and suggestion.

R12d. A standalone `verify-report.md` artifact MUST be used when at least one of the following is true:
- final verification evidence cannot remain concise in a contributor-visible handoff surface;
- the change requires a durable standalone verification record for reviewer or maintainer audit;
- the change has multiple verification commands, environments, or result groups that need separate traceable reporting;
- repository policy for the change type explicitly requires a standalone verification artifact;
- a reviewer or maintainer explicitly requests a standalone verify report;
- the verification stage is itself a reviewed deliverable for the change.

R12e. When none of the `R12d` triggers apply, validation evidence that exists before final `verify` MAY remain in `docs/changes/<change-id>/explain-change.md`; final verification evidence MAY remain in `change.yaml`, the PR summary, or another contributor-visible handoff surface, provided the workflow's durability and concision requirements remain satisfied.

R12f. Contributors SHOULD NOT infer that `verify-report.md` is universally required merely because the proof-of-value example contains one.

R13. The first proof-of-value example shipped by the starter kit MUST be a skill metadata validator change that demonstrates the workflow end to end.

R14. The proof-of-value example MUST include durable artifacts for proposal, spec, plan, test-spec, verify report, and explain-change.

R14a. `docs/changes/0001-skill-validator/` MUST be treated as a rich reference example rather than the minimum universal pack for every non-trivial change.

R14b. The ordinary baseline non-trivial change-local pack MUST be `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning, with standalone `review-resolution.md` and `verify-report.md` remaining conditional when their governing triggers do not apply.

R15. The starter kit MUST provide a local skill-structure validation command that checks, at minimum:
- a source skill contains `SKILL.md`;
- `SKILL.md` begins with YAML frontmatter;
- skill metadata includes a non-empty `name`;
- skill metadata includes a non-empty `description`;
- the Markdown body includes exactly one top-level `#` title;
- the Markdown body includes an `## Expected output` section;
- skill names are unique;
- placeholder text such as `TODO` or `TBD` is rejected;
- generated output is not treated as authored source of truth.

R15a. For the first release, the skill validator contract MUST remain intentionally simple. It MUST NOT require richer skill metadata beyond the fields and sections listed in `R15`.

R16. The starter kit MUST provide automated fixture-based tests for the skill validator that cover, at minimum:
- a valid skill passes;
- missing name fails;
- missing description fails;
- duplicate skill name fails;
- missing top-level title fails;
- missing `## Expected output` section fails;
- placeholder text fails.

R17. The starter kit MUST provide a generated-output drift check so contributors can verify that derived distribution content is in sync with canonical source content.

R18. The starter kit MUST run the following checks in CI on pull requests:
- skill validation;
- validator fixture tests;
- generated-output drift check.

R19. Early CI enforcement MUST focus on structural correctness and drift detection rather than subjective writing-quality or philosophy scoring.

R20. The starter kit MUST separate canonical generic workflow content from tool-specific adapter guidance.

R20a. This workflow contract MAY leave exact repository layout details for methodology documents, templates, schemas, core skills, adapter files, and generated distribution directories to the architecture artifact, provided that:
- canonical authored content remains clearly distinguishable from generated output;
- root repository guidance identifies the actual authored and generated paths in use;
- contract-level required paths defined elsewhere in this spec remain stable.

R20b. Published skill text MUST be project-portable. It MAY reference portable project surfaces such as:
- `AGENTS.md`;
- `docs/workflows.md`;
- `VISION.md`;
- `docs/changes/<change-id>/`;
- `docs/plans/<plan>.md`;
- local workflow contract, when the adopting project has one;
- project validation command, when supplied by the adopting project.

R20c. Published skill text MUST NOT reference RigorLoop repository-internal surfaces or mechanics, including:
- `specs/rigorloop-workflow.md`;
- `specs/skill-contract.md`;
- `.codex/skills/`;
- `dist/adapters/`;
- `scripts/select-validation.py`;
- `scripts/build-adapters.py`;
- `templates/shared/`;
- RigorLoop-local examples;
- selector path constraints;
- drift-check mechanics;
- shared-block implementation mechanics.

R20d. The public skill portability checks in `R20b` and `R20c` MUST apply to canonical skill files shipped to users, generated public skill copies, and public adapter skill copies. They MUST NOT apply to internal specs, plans, tests, generator scripts, maintainer docs, or repository-only contributor docs.

R20e. Internal RigorLoop repository details MAY remain in repository specs, tests, plans, maintainer docs, generator code, and repository-only contributor docs.

R20f. Static validation MUST fail when public workflow or skill surfaces contain current-route references to case-insensitive hyphen or space variants of `fast lane`, `full lane`, `full-feature lane`, `mini-spec`, `small-change lane`, `tiny low-risk`, `low-risk lane`, `high-risk lane`, `proportional evidence`, unconditional `verify -> explain-change`, unconditional `code-review -> verify` for milestone-based work, or public skill references to RigorLoop-internal paths or commands.

R20g. Static validation MUST prove that public workflow or skill surfaces contain `standard workflow`, manual skill invocation isolation, `explain-change -> verify -> pr`, `ci-maintenance -> explain-change -> verify -> pr` when CI maintenance is triggered, and `docs/workflows.md` as the workflow guide created or refreshed by the `workflow` skill.

R20h. Static validation for this change MUST remain phrase-based and MUST NOT become semantic prose scoring.

R21. Canonical generic workflow content MUST include, at minimum:
- methodology documents;
- workflow templates;
- machine-readable schemas;
- core reusable skills.

R22. Codex-specific instructions MUST live in a Codex adapter layer rather than inside the generic methodology content.

R23. Codex-oriented generated output MUST be derived from canonical source content and MUST NOT be the source of truth for manual editing.

R24. The root repository guidance MUST identify:
- canonical authored locations;
- generated locations that should not be hand-edited;
- validation commands contributors are expected to run before PR.

R24a. When exact repository layout details are not fixed by this spec, the architecture artifact MUST define the concrete directory layout for:
- canonical generic workflow content;
- tool-specific adapter content;
- generated distribution output.

R25. For each non-trivial change, the starter kit MUST define a canonical machine-readable traceability file at:
- `docs/changes/<change-id>/change.yaml`

R25a. The first release MUST use YAML as the canonical machine-readable traceability format for `change.yaml`.

R25b. For each non-trivial change, `change.yaml` MUST include at least the following top-level fields:
- `change_id`;
- `title`;
- `classification`;
- `risk`;
- `artifacts`;
- `requirements`;
- `tests`;
- `validation`;
- `changed_files`;
- `review`.

R25c. The `artifacts` mapping in `change.yaml` MUST record paths to the durable Markdown artifacts that exist for the change. Artifact keys that are not applicable to a given change MAY be omitted.

R25d. The `validation` field in `change.yaml` MUST be a list of validation records. Each validation record MUST include:
- `command`;
- `result`.

R25e. The `review` field in `change.yaml` MUST include:
- `status`;
- `unresolved_items`.

R25f. Narrative rationale for a change MUST live in Markdown artifacts rather than being replaced by `change.yaml` alone.

R25g. Reviewer-facing summary for a change MUST live in PR text. `change.yaml` MUST NOT be the only reviewer-facing explanation of a change.

R25h. Manual skill invocations MAY omit `change.yaml` when they are not used to claim complete workflow delivery for a change. Complete workflow delivery for non-trivial work requires the baseline change-local pack unless a higher-priority artifact defines a narrower requirement.

R26. The starter kit MUST support phased enforcement maturity:
- early releases enforce structure and validation evidence first;
- later releases may enforce artifact presence and traceability by change type.

R27. The starter kit MUST preserve Git, pull requests, CI, and human review as the source of truth rather than replacing them with orchestration state.

## Inputs and outputs

### Inputs

- contributor change classification;
- repository guidance and workflow docs;
- standing artifacts and living references;
- stage-obligation metadata;
- repo-local lifecycle state in plans, lifecycle-managed artifacts, review-resolution closeout, readiness wording, and change-local artifacts;
- change-local autoprogression profile policy and user authorization when present;
- durable authorization persistence result for `authoring-through-plan-review` activation, including fallback path evidence when `workflow-policy.yaml` is used;
- proposal status, proposal-review evidence, review-log state, and review-resolution closeout when proposal-gate activation is evaluated;
- recorded architecture assessment outcome when authoring autoprogression reaches post-spec-review routing;
- change artifacts and PR text;
- local validation commands and CI workflow configuration;
- tool-specific adapter inputs when an adapter is enabled.

### Outputs

- contributor-visible workflow documentation;
- workflow category guidance;
- stage-obligation tables;
- durable change artifacts;
- synchronized repo-local lifecycle state for review-open PRs;
- contributor-visible lifecycle warnings for tracked merge-dependent language;
- PR summary and validation notes;
- machine-readable change metadata for non-trivial work at `docs/changes/<change-id>/change.yaml`;
- profile state and authoring autoprogression audit evidence when `authoring-through-plan-review` is armed, paused, active, or completed;
- `authorization-not-persisted` stop evidence when durable profile authorization is missing, malformed, incomplete, or cannot be written;
- recorded architecture assessment result when authoring autoprogression evaluates architecture need;
- generated adapter distribution content;
- local and CI validation results.

## State and invariants

- Canonical workflow content remains editable source material.
- Generated distribution content remains rebuildable derived output.
- Every mandatory or triggered blocking stage has contributor-visible evidence.
- Stage-obligation values remain stable and machine-checkable: `mandatory`, `conditional`, `on-demand`, and `periodic`.
- `specs/rigorloop-workflow.md` remains the canonical workflow definition, while `docs/workflows.md` remains a summary.
- Skill handoff sections summarize local preconditions, outputs, failure modes, and brief next-stage pointers without duplicating the full workflow contract.
- RigorLoop uses one recommended standard workflow, not separate fast-lane, full-lane, tiny, low-risk, or high-risk routes.
- Manual skill invocations are allowed but remain isolated by default.
- Direct review-only invocations remain isolated by default even when a change has an armed authoring profile.
- Manual skill output is not proof that the full standard workflow is complete.
- `authoring-through-plan-review` is a distinct, explicitly armed profile and does not alter default behavior when profile is `off`.
- `authoring-through-plan-review` completes at clean `plan-review` and cannot start `test-spec` or implementation.
- Profile policy metadata is an audit and authorization surface, not a live workflow-state owner.
- Durable profile policy metadata is required before any profile-driven transition.
- Complete workflow delivery remains traceable from proposal/spec direction through durable reasoning, final verification evidence, and PR summary.
- Completed planned milestones remain visible as coherent branch or pull-request review boundaries even when multiple milestones share one pull request.
- In a milestone-based plan, a milestone implementation handoff and a closed milestone are distinct lifecycle facts.
- In a milestone-based plan, final closeout is not available until all in-scope implementation milestones are closed and no required review-resolution remains open.
- Repo-local lifecycle state in a review-open PR is true within that PR's tracked tree.
- Merge integrates pre-validated repo-local lifecycle state; it does not perform routine lifecycle closeout.

## Error and boundary behavior

- A manual skill invocation that claims omitted upstream or downstream stages have passed MUST be considered incomplete unless the claimed stage evidence exists.
- A complete workflow claim without evidence from the relevant standard workflow stages MUST be considered incomplete.
- An authoring autoprogression activation without both an armed profile and a gate-ready proposal MUST be considered incomplete and must not enter `spec`.
- An authoring autoprogression activation without a durable authorization record, with a malformed or incomplete authorization record, or with a failed authorization-persistence write MUST pause with an authorization-persistence stop condition before any profile-driven transition.
- An unknown profile value, contradictory profile state, ambiguous architecture assessment, non-clean review, material finding, open owner decision, missing or malformed authorization persistence, authorization persistence write failure, or exhausted transition budget MUST pause the profile.
- A paused profile MUST NOT resume from manual file changes alone.
- A planned milestone closed without the completion evidence required by `R8a` or without the standardized milestone commit subject required by `R8b` MUST be considered incomplete.
- A milestone-based plan with an open in-scope implementation milestone, a `review-requested` milestone that has not been reviewed, a `resolution-needed` milestone, ambiguous remaining implementation scope, or stale final-closeout readiness wording MUST be considered incomplete for final closeout.
- A planned initiative completed by a PR but still listed as active in `docs/plan.md` or the plan body when that PR opens for review MUST be considered incomplete.
- A PR with broader lifecycle artifact inconsistency under `R8ki` MUST be considered incomplete for `branch-ready`.
- Merge-dependent language in tracked files MUST produce a reviewer-attention warning unless the language is corrected or classified as a true downstream completion event.
- A non-trivial change missing required PR explanation or validation evidence MUST be considered incomplete.
- A substantive proposal attempted without `VISION.md` MUST stop unless it is explicit bootstrap work under `R6f`.
- Governance adoption, workflow-governance, or source-of-truth changes attempted without `CONSTITUTION.md` MUST stop unless the proposal is explicit bootstrap work under `R6g`.
- Architecture, plan, code-review, or onboarding-heavy work that would rely on `docs/project-map.md` MUST stop, refresh the map, or record a no-map rationale when the map is absent, known-stale, contradicted, or missing the relied-on area.
- Workflow-governance changes with affected operating or governance surfaces that are not updated, explicitly marked unaffected with rationale, or deferred with owner and follow-up MUST be considered incomplete.
- Review-driven fixes or downstream routing after a formal lifecycle review MUST stop when a required detailed review file or required initial review-record root is missing.
- Review-driven tracked artifact edits after an isolated formal review material finding MUST stop until the required durable review record exists, or until a reconstructed record repairs late capture.
- An isolated review output with material findings that omits handoff status, material Finding IDs, required record path, record-before-fixing or reconstruction status, or owner-decision status MUST be considered incomplete.
- A copied formal review skill `## Isolation and Recording` subsection that differs from `templates/shared/review-isolation-and-recording.md`, or contains stage-specific insertions inside the shared block, MUST fail structural validation.
- A new `review-resolution.md` that removes required per-finding parseable labels for scan-first formatting MUST be considered invalid for review closeout.
- Final `explain-change`, `verify`, and `pr` MUST stop while required `review-resolution` closeout remains open.
- Triggered `learn` MUST NOT stop ordinary final `explain-change`, `verify`, or `pr` when no higher-priority artifact makes it blocking and either the pre-session closeout is recorded or the session record captures the outcome after Frame.
- Invalid skill structure MUST fail local validation and CI validation.
- Generated-output drift MUST fail the drift check until derived output is rebuilt or the change is reverted.
- The starter kit MUST allow validation to run without requiring network access or Codex installation for the baseline structural checks.

## Compatibility and migration

- The first release may start with lightweight structural enforcement and add stronger traceability enforcement in later versions.
- Codex-specific guidance is optional and adapter-scoped; the generic workflow remains usable without Codex-specific installation.
- Compatibility output for legacy or project-specific Codex setups MAY be generated, but generated compatibility directories remain derived output rather than authored source.
- Later releases MAY add JSON compatibility or alternative export formats, but `docs/changes/<change-id>/change.yaml` remains the canonical first-release contract.
- Existing repositories adopting RigorLoop MAY phase in the contract incrementally, beginning with documentation and structural checks before stricter enforcement.
- Repositories adopting lifecycle-managed artifact ownership MAY phase migration of unrelated stale baseline artifacts, but they MUST normalize stale touched or relied-on artifacts before downstream stages rely on them as current guidance.
- Repositories that squash, rebase, or otherwise rewrite commit history MAY collapse milestone commit boundaries after merge. The first-release contract guarantees milestone visibility during branch and pull-request review, not preservation under every default-branch merge strategy.
- For new non-trivial work, the default standalone durable reasoning artifact is `docs/changes/<change-id>/explain-change.md`. Approved legacy top-level explain artifacts under `docs/explain/` remain valid until migrated or retired.
- In-flight work SHOULD use the current standard workflow at the next handoff. If an active plan has not yet reached final verification, it uses `explain-change -> verify -> pr`.
- Existing change records without durable autoprogression profile policy remain profile `off` unless the user re-asserts authorization and the workflow records it durably before activation.
- Existing workflow-managed and isolated flows remain compatible because `authoring-through-plan-review` requires explicit change-local user authorization and gate readiness.
- If the downstream change-metadata spec rejects workflow policy in `change.yaml`, the policy surface for this profile migrates to `docs/changes/<change-id>/workflow-policy.yaml` without changing live state ownership, and the fallback decision must be visible in the activation audit trail.
- If in-flight work already ran verification before `explain-change`, that verification evidence is preliminary. Final `verify` MUST rerun after the durable explain-change artifact exists and is current.
- Active plans affected by this transition MUST record the short transition note defined in `R6m` and `R6n` rather than carrying a detailed historical explanation of the old order.
- Existing plans or lifecycle artifacts that already contain merge-dependent completion wording MAY be migrated through a one-time cleanup PR. New plans and lifecycle artifacts authored after this amendment is adopted MUST follow PR-self-contained lifecycle completion.
- A lifecycle state that depends on a downstream completion event MUST remain active until a later PR or repository-owned automation records the state after that event.
- Merge-SHA recording remains unspecified by this contract and MUST NOT be invented as an implicit exception to PR-self-contained lifecycle completion.
- The `vision.md` to `VISION.md` migration is already complete for this repository. This workflow refactor MUST use `VISION.md` as the standing project-vision artifact and MUST NOT reintroduce lowercase `vision.md` as canonical.
- The project-map lifecycle markers, calendar freshness thresholds, and project-map revision workflow are deferred to a focused follow-up and MUST NOT be invented in this workflow refactor.
- The final `learn` artifact model is defined by `specs/learn-artifact-model.md`. Existing pre-adoption learning notes outside `docs/learn/` may remain unless a later approved migration plan relies on them as current guidance.
- Existing historical review skills, generated skill mirrors, generated adapter output, and review-resolution records do not require migration until touched, generated, or relied on as current guidance.

## Observability

- Verification evidence for non-trivial work MUST record the commands run and their results in a contributor-visible location.
- PR text MUST state validation run or a no-test rationale for every change.
- When review feedback exists, the recorded review resolution MUST be visible to reviewers in the PR, explain-change artifact, or a standalone review-resolution artifact.
- Triggered detailed formal review records MUST be discoverable through `review-log.md` when they exist, while clean artifact-local settlements remain discoverable in the reviewed artifact.
- Isolated review output with material findings MUST make the handoff stop and durable recording obligation visible before fixes or downstream routing proceed.
- New `review-resolution.md` records SHOULD make closeout status, covered reviews, resolved counts, unresolved counts, and finding audit locations visible near the top of the file.
- `change.yaml` SHOULD make artifact and validation traceability inspectable without reading every Markdown artifact.
- For planned milestone work, contributor-visible branch or pull-request history SHOULD make milestone boundaries visible through the standardized milestone commit subjects defined in `R8b`.
- Workflow summary and skill guidance SHOULD make category, obligation, and handoff ownership visible enough that contributors do not need chat history to know which stage blocks downstream readiness.
- Authoring autoprogression output MUST state which profile is armed, active, paused, completed, or off; which stage ran automatically; and why progression paused or completed.
- Authoring autoprogression output MUST report `authorization-not-persisted` when activation pauses because durable authorization is absent, malformed, incomplete, or cannot be written.
- Architecture assessment output MUST make the recorded architecture routing decision visible.
- Clean profile completion MUST state that `test-spec` is the next stage and was not invoked.
- PR-self-contained lifecycle completion warnings SHOULD be contributor-visible and identify the tracked file that contains merge-dependent language.

## Security and privacy

- Baseline validation commands MUST NOT require repository secrets to validate skill structure or generated-output drift.
- The workflow MUST avoid making external network access a requirement for routine structural validation.
- Tool-specific adapters MUST NOT weaken the generic workflow requirement that human review and repository controls remain authoritative.
- Authoring autoprogression MUST NOT cross into implementation, code execution, PR opening, publication, release, deploy, merge, destructive Git actions, or any external-boundary action.
- Profile authorization metadata MUST NOT contain secrets, credentials, or private data beyond ordinary workflow attribution.
- Profile authorization metadata MUST be limited to workflow policy fields such as profile name, `authorized_by`, authorization timestamp, change ID, profile status, and fallback-path evidence.

## Accessibility and UX

- Contributor-facing templates SHOULD use concise, repeatable section headings so contributors can follow the workflow without reverse-engineering hidden rules.
- Contributor-facing workflow instructions SHOULD be concise enough for common PR or issue workflows and SHOULD make isolated manual skill use visibly distinct from complete workflow delivery.
- New `review-resolution.md` records SHOULD prefer summary-first structure, an overview table, compact finding details, shared validation evidence, and a closeout checklist when those elements make the file easier to scan.

## Performance expectations

- Local structural validation and drift checks SHOULD be lightweight enough to run as part of normal contributor pre-PR workflow.
- The first release does not define numeric latency budgets for validation commands.

## Edge cases

1. A generated-artifact refresh with no generator logic change may be checked through a manual skill invocation, but that output does not claim complete workflow delivery unless the relevant standard workflow stage evidence exists.
2. A documentation-only change that alters workflow order, classification rules, or contributor obligations follows the standard workflow because it changes contributor-visible behavior.
3. A change that adds CI automation without altering product behavior still follows the standard workflow because CI behavior is contributor-visible workflow infrastructure.
4. A repository may carry both generic workflow content and Codex-specific adapters, but contributors must still edit canonical source rather than generated distribution output.
5. A PR with no automated tests run may still be valid only when the PR text states why tests were not applicable and the omission is supported by the governing workflow evidence.
6. A non-trivial change may resolve review feedback entirely inside the PR or explain-change artifact when the feedback is routine and does not create durable project memory beyond the current review.
7. A non-trivial change may omit some artifact keys from `change.yaml` when those artifact types are not applicable to the change, but it may not omit the required top-level fields listed in `R25b`.
8. A completed milestone that is not independently safe to merge may remain inside a larger pull request, but it still requires the completion evidence and milestone commit boundary defined in `R8a` and `R8b`.
9. An unplanned single-slice change may use a normal commit subject because milestone-formatted commits are reserved for planned milestone work.
10. An accepted proposal, approved spec, approved architecture document, active test spec, or accepted or active ADR may remain current guidance without immediate closeout as long as its readiness text is truthful and terminal disposition has not occurred.
11. Final PR text may reference additional authoritative artifacts only after `verify` is rerun against those new references or an equivalent updated pre-PR handoff surface.
12. An ordinary non-trivial change may satisfy the baseline change-local pack with `docs/changes/<change-id>/change.yaml` plus `docs/changes/<change-id>/explain-change.md` when standalone `review-resolution.md` and `verify-report.md` triggers do not apply.
13. `docs/changes/0001-skill-validator/` may include more artifacts than an ordinary non-trivial change without making those additional artifacts universal requirements.
14. Approved legacy top-level explain artifacts under `docs/explain/` remain valid for already-shipped work until they are migrated, superseded, archived, or otherwise retired.
15. Successful `spec-review` may still report `Immediate next stage: architecture` while separately reporting `Eventual test-spec readiness: conditionally-ready`; `architecture` is a forward repository-stage handoff value.
16. `inconclusive` `spec-review` uses `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition naming the missing input, blocker, or ambiguity. The `Immediate next stage` field is not omitted or left empty for inconclusive or missing-input cases.
17. `plan-review` may mention implementation readiness only after preserving `test-spec` as the immediate next handoff.
18. `explore` and `research` may be absent from a normal non-trivial change when the problem and facts are already settled, but they block downstream reliance after their triggers are active or their artifacts are cited as dependencies.
19. `learn` may be absent from an ordinary PR package, but a repeated finding, blocker or major workflow-process finding, failed release or adapter smoke, accepted postmortem action, cadence run, incident response, contributor observation, or explicit maintainer request must be closed through a `docs/learn/sessions/**` session record once Frame is reached, or through a scheduled follow-up, deferral, or explicit no-learn rationale before a session runs. It blocks downstream only when a higher-priority artifact explicitly makes it blocking.
20. `ci-maintenance` may be skipped when hosted workflow automation already covers the material risk, but it is required when automation is missing, stale, or wrong.
21. A repository without `docs/project-map.md`, with a known-stale or contradicted map, or with a map missing the relied-on area may proceed only when consumers do not rely on the map or record a no-map rationale for the relevant architecture, planning, review, or onboarding-heavy decision.
22. A bootstrap proposal may proceed without an existing `VISION.md` only when its `Vision fit` explicitly identifies that it is creating or migrating the missing standing artifact.
23. A bootstrap proposal may proceed without an existing `CONSTITUTION.md` for governance adoption, workflow-governance, or source-of-truth changes only when its `Vision fit` explicitly identifies that it is creating or migrating the missing constitution.
24. A change with open material review findings may not proceed to final `explain-change`, `verify`, or `pr` even when implementation tests pass.
25. Existing active work may finish under its starting workflow contract unless it opts into the refactored contract or touches refactored workflow surfaces directly.
26. A clean required `proposal-review` may settle in proposal status or decision log without creating empty review artifacts when no detailed-record trigger applies.
27. A no-material `plan-review` with `rethink` creates a detailed review file and `review-log.md`, but not an empty `review-resolution.md`.
28. A material `architecture-review` finding before any change-local root creates an initial review-record root with `review-resolution.md` before design fixes proceed.
29. A final PR-ready handoff is incomplete if only the initial review-record root exists and durable Markdown reasoning was never added.
30. A draft PR may run early CI or collect discussion without being review-open, but lifecycle state must be synchronized before the PR is marked ready for review or reviewers are asked to judge the branch as complete.
31. A reopened PR or reused branch must satisfy PR-self-contained lifecycle completion before reviewer action resumes.
32. A release, deploy, package publication, external migration, or unobserved hosted check may keep an otherwise implemented plan active because the completion event is downstream of the PR tree.
33. A tracked plan sentence that says "move to Done after merge" is a warning candidate. It becomes blocking stale lifecycle state when the PR itself already contains the evidence that makes `Done` true.
34. A top-level spec updated by a PR may remain `draft` while awaiting `spec-review`; if `spec-review` approves it and downstream artifacts rely on it, the same PR records `approved` before review-ready handoff continues.
35. A direct `proposal-review` material finding that will revise a tracked proposal creates durable review evidence before the proposal edit begins, while downstream handoff remains isolated.
36. A direct `spec-review` material finding that already drove tracked spec edits before recording can continue only after a reconstructed detailed review file discloses source, timing, available evidence, stable Finding IDs, and known fidelity loss.
37. A material review finding that changes `README.md`, `CONSTITUTION.md`, a skill file, a script, a schema, generated adapter output, or a change-local artifact is still a tracked artifact edit.
38. A new `review-resolution.md` with common validation evidence may record the shared proof once, but each material finding detail still keeps parseable closeout labels.
39. A formal review skill with stage-specific wording inserted inside the shared `## Isolation and Recording` block fails validation even if the wording is substantively correct.
40. An isolated material finding requires change-local review files even when it does not affect tracked work, affect closeout, or create follow-up work. Isolation stops handoff, not recording.
41. A clean non-final implementation milestone review closes that milestone and routes to the next in-scope implementation milestone, not `verify`.
42. A clean final implementation milestone review reaches final closeout only when all in-scope implementation milestones are closed and no required review-resolution remains open; final closeout then runs `ci-maintenance` when triggered, `explain-change`, `verify`, and `pr`.
43. A milestone review with findings moves the reviewed milestone to `resolution-needed` and keeps the workflow on that same milestone until findings are resolved, deferred with rationale, rejected, or otherwise closed under the governing review contract.
44. A plan may include a lifecycle-closeout milestone for downstream gates, but that lifecycle-closeout milestone does not behave like an open implementation milestone for final closeout readiness.
45. A mixed milestone that still contains implementation work remains an implementation milestone until the implementation scope is closed or the plan is revised.
46. An unarmed but otherwise gate-ready proposal remains profile `off`; the workflow may report `spec` next but does not automatically enter it.
47. An armed profile with proposal status still `draft` pauses before `spec` until upstream status settlement makes the proposal `accepted`.
48. An active authoring profile with `architecture-required` runs architecture and architecture-review; an active profile with `architecture-not-required` routes to plan; `architecture-ambiguous` pauses.
49. A direct `proposal-review`, `spec-review`, `architecture-review`, or `plan-review` invocation remains isolated unless the user invokes workflow-managed resume.
50. A clean `plan-review` under `authoring-through-plan-review` marks the profile completed and reports `test-spec` next without invoking it.
51. Manual edits after a paused profile do not resume the profile until the user explicitly authorizes resume.

## Non-goals

- Building a hosted orchestration platform.
- Replacing Git-based review workflows with agent-managed state.
- Enforcing subjective writing-quality scores in early CI.
- Requiring manual skill invocations to claim completion of omitted workflow stages.
- Hardcoding every future adapter implementation detail into the first workflow contract.
- Implementing detailed project-map freshness markers, calendar thresholds, or revision workflow in this refactor.
- Creating learn session templates, topic templates, empty topic files, a fixed topic taxonomy, automated lesson triage, or historical-note migration.
- Removing `explore`, `research`, or `learn`; they remain available through their trigger rules.
- Rewriting project vision content or revisiting the completed `VISION.md` migration.
- Adding a duplicate active legacy CI-maintenance entrypoint.
- Inspecting hosted PR-description event metadata for merge-dependent language in the first enforcement slice.
- Defining a merge-SHA recording exception before a real immutable-merge-metadata case exists.
- Treating deploy, release, package publication, or external migration completion as repo-local lifecycle state that can be made true by the PR tree.
- Adding semantic validator detection for tracked artifact edits that mention unresolved review findings in the first review-recording slice.
- Generating formal review skill shared subsections instead of manually copying a canonical block.
- Widening `authoring-through-plan-review` to test-spec, implementation, verify, PR, or automatic review-fix loops.
- Adding new autoprogression profiles without separate proposal and spec amendments.
- Making autoprogression policy metadata the live owner of current stage, next stage, review status, branch readiness, or PR readiness.

## Acceptance criteria

- A contributor can follow the standard workflow and produce a complete PR with standard workflow evidence for direction, implementation, review, rationale, final `verify`, and PR handoff when those claims are made.
- A contributor can follow the standard workflow for the skill validator example and produce linked durable artifacts plus validation evidence.
- A contributor can close a planned milestone with updated plan evidence and a standardized milestone commit without being forced to open a separate pull request for that milestone.
- A contributor can make an unplanned single-slice change without using a milestone-formatted commit and still remain within the workflow contract.
- The workflow clearly distinguishes standing artifacts, living references, workflow infrastructure, on-demand artifacts, the per-change chain, and periodic artifacts.
- The workflow clearly distinguishes `mandatory`, `conditional`, `on-demand`, and `periodic` obligations.
- A contributor can tell which stage-like actions run for every change and which block downstream only when triggered.
- The starter kit contract clearly separates generic methodology from Codex-specific adapters and generated output.
- The first CI contract is limited to structural validation, validator fixture testing, and generated-output drift detection.
- A contributor can distinguish settlement states from closeout or terminal states for lifecycle-managed proposals, specs, test specs, architecture docs, and ADRs without relying on chat history.
- A reviewer can determine from the PR plus artifacts why a change exists, how it was validated, and which content is canonical versus generated.
- A reviewer can determine the disposition and rationale of review feedback without guessing whether it lives in PR text, explain-change, or a standalone review-resolution artifact.
- A reviewer can locate structured traceability for a non-trivial change in `docs/changes/<change-id>/change.yaml` and find at least the required fields defined by `R25b`.
- A reviewer can distinguish the ordinary baseline non-trivial change-local pack from the richer `docs/changes/0001-skill-validator/` example pack.
- A reviewer can tell that new non-trivial work defaults to `docs/changes/<change-id>/explain-change.md` while approved legacy top-level explain artifacts remain valid until retired.
- A reviewer can distinguish milestone commit boundaries from pull-request boundaries by inspecting standardized milestone commit subjects and the associated plan updates.
- A reviewer can tell that planned implementation milestone state uses one authoritative field and that `review-requested` and `resolution-needed` block premature final closeout readiness.
- A reviewer can tell that clean non-final implementation milestone reviews route to the next implementation milestone, while clean final implementation milestone reviews route to final closeout.
- A reviewer can tell that `spec-review` output distinguishes the `Immediate next stage` result field from `Eventual test-spec readiness`, that only `architecture` and `plan` are forward repository-stage handoff values, and that `test-spec` is not an `Immediate next stage` value.
- Only `architecture` and `plan` are forward repository-stage handoff values for `spec-review`; `spec revision`, `review-resolution`, and `none` are routing or no-handoff values.
- A reviewer can tell that `plan-review` preserves `test-spec` as the immediate next handoff even when later implementation readiness is also discussed.
- A contributor can tell that `explore` and `research` are on-demand support rather than default prerequisites.
- A contributor can tell that triggered `learn` creates a tracked session record after Frame, that pre-session follow-up, deferral, or no-learn closeout is recorded in an allowed contributor-visible tracked or review-visible surface, that durable topic guidance uses `docs/learn/topics/**`, and that triggered `learn` blocks downstream only when a higher-priority artifact explicitly makes it blocking.
- A contributor can tell that `ci-maintenance` means CI infrastructure maintenance and not validation execution.
- A contributor can tell that `review-resolution` is the closeout stage for review findings and that open required closeout blocks final `explain-change`, `verify`, and `pr`.
- A contributor can tell which formal lifecycle review outcomes require detailed review files, when clean reviews remain artifact-local, and when no-material review records omit empty `review-resolution.md`.
- A reviewer can distinguish an initial review-record root from the final non-trivial change-local pack.
- A contributor can distinguish isolated review handoff from material-finding recording obligations.
- A contributor can tell that every material finding is recorded and all material findings require change-local review files.
- A contributor can identify tracked artifacts for review-recording purposes.
- An isolated review output with material findings exposes handoff status, material Finding IDs, required record path, record-before-fixing or reconstruction status, and owner-decision status.
- Isolated material-review output makes clear that material findings require change-local review files even when downstream handoff stops.
- `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` teach the broad rule that every material finding requires a detailed change-local review file.
- Formal review skills contain a byte-identical `## Isolation and Recording` block copied from a canonical template.
- A reviewer can understand a new `review-resolution.md` closeout state in 30 seconds and audit any individual material finding in 2 minutes.
- A new scan-first `review-resolution.md` remains valid under structural and closeout validation.
- A contributor can tell that `docs/project-map.md` is a living reference and must be refreshed or bypassed with a no-map rationale before reliance when absent, known-stale, contradicted, or missing the relied-on area.
- A contributor can tell that `VISION.md` and `CONSTITUTION.md` are standing artifacts with different absence gates.
- A reviewer can confirm that affected operating and governance surfaces are updated, explicitly marked unaffected with rationale, or deferred with owner and follow-up in an allowed contributor-visible tracked or review-visible surface.
- A contributor can tell that plan lifecycle synchronization happens inside the PR that performs the lifecycle transition, before the PR opens for review.
- A reviewer can tell that merge is a fast-forward of pre-validated repo-local lifecycle state, not a trigger for routine lifecycle closeout.
- A contributor can keep a plan active when completion depends on a true downstream event and can identify the later event or follow-up condition.
- A reviewer can see broader lifecycle artifact inconsistency block `branch-ready` for touched, referenced, generated, or authoritative lifecycle artifacts.
- A reviewer can see merge-dependent language in tracked files flagged as a non-blocking reviewer-attention warning unless it is also a blocking lifecycle inconsistency.
- A contributor can tell RigorLoop has one recommended standard workflow, not separate small-change, fast, full, low-risk, or high-risk lanes.
- A contributor can tell that manual skill invocations are isolated by default and do not claim full workflow completion.
- A contributor can tell the final closeout order is `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`.
- A reviewer can verify that `explain-change` does not claim final `verify`, `branch-ready`, PR-ready, or CI-final status.
- A reviewer can verify that final `verify` validates the presence and currency of the required explain-change artifact.
- A reviewer can distinguish portable published skill surfaces from RigorLoop repository-internal surfaces.
- A workflow guide created or refreshed by the `workflow` skill includes the required sections without becoming a competing workflow spec.
- An affected active plan records the short transition note before using final `explain-change -> verify -> pr`.
- A contributor can identify when `authoring-through-plan-review` is off, armed, active, paused, or completed.
- A contributor can tell that `auto-through: plan-review` maps to `autoprogression.profile: authoring-through-plan-review`.
- A reviewer can verify that the proposal gate is separate from user authorization and that activation requires `armed && gate-ready`.
- A reviewer can verify that direct review requests remain isolated despite an armed profile.
- A reviewer can verify that architecture assessment is recorded and that ambiguity pauses the profile.
- A reviewer can verify that the profile stops after clean plan-review and does not invoke test-spec or implementation.
- A reviewer can verify that profile policy metadata does not own live workflow state.
- A reviewer can verify that profile authorization is recorded durably before activation and that missing, malformed, incomplete, or failed authorization persistence pauses the profile before any profile-driven transition.
- A reviewer can verify that future profiles require separate proposal and spec amendments.

## Open questions

- What exact validation schema should enforce `workflow.autoprogression.profile` in `change.yaml` if the change-metadata contract accepts policy data there?
- The visible stage/action label and skill entrypoint are both `ci-maintenance`; detailed periodic `learn` cadence scheduling remains outside this workflow contract.

## Next artifacts

- Architecture assessment for implementation-profile policy, phase gating, workflow orchestration, review classification, correction loops, verify-boundary behavior, and generated adapter impact.
- Architecture and architecture-review when the assessment requires architecture.
- Plan and plan-review before implementation.
- Test-spec amendments for `implementation-through-verify`.

## Follow-on artifacts

- `proposal`: [Workflow Refactor](../docs/proposals/2026-05-01-workflow-refactor.md)
- `plan`: [Workflow Refactor Execution Plan](../docs/plans/2026-05-03-workflow-refactor.md)
- `learn proposal`: [Optimize Learn Skill](../docs/proposals/2026-05-03-optimize-learn-skill.md)
- `learn spec`: [Learn Artifact Model](learn-artifact-model.md)
- `learn test spec`: [Learn Artifact Model test spec](learn-artifact-model.test.md)
- `learn plan`: [Learn Artifact Model Implementation Plan](../docs/plans/2026-05-04-learn-artifact-model.md)
- `proposal`: [PR-Self-Contained Lifecycle Completion](../docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md)
- `plan`: [PR-Self-Contained Lifecycle Completion Plan](../docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md)
- `plan-review`: approved with no material findings.
- `test-spec`: [RigorLoop workflow test spec](rigorloop-workflow.test.md) updated with PR-self-contained lifecycle completion coverage.
- `implementation`: PR-self-contained lifecycle completion M1 through M4 complete.
- `review-resolution`: material M2 code-review finding accepted, fixed, and closed.
- `verify`: completed for PR handoff after PR-mode selected validation and broad smoke.
- `explain-change`: completed in the change-local evidence pack.
- `pr`: PR #30 opened for human review.
- `proposal`: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- `spec`: [Formal Review Recording](formal-review-recording.md) amendment for isolation-versus-recording behavior.
- `spec`: [Review Finding Resolution Contract](review-finding-resolution-contract.md) amendment for scan-first `review-resolution.md` records.
- `spec-review`: approved on 2026-05-07 with no material findings.
- `plan`: [Review Skill Material Finding Recording plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md)
- `plan-review`: approved on 2026-05-07 with no material findings.
- `test-spec`: [RigorLoop workflow test spec](rigorloop-workflow.test.md) updated with review skill material-finding recording amendment coverage.
- `proposal`: [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md)
- `proposal-review`: approved in [proposal-review-r2](../docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/proposal-review-r2.md)
- `spec-review`: approved in [spec-review-r5](../docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r5.md)
- `architecture`: [Canonical System Architecture](../docs/architecture/system/architecture.md) approved for the direct workflow-governance package update.
- `architecture-review`: approved in [architecture-review-r1](../docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/architecture-review-r1.md)
- `plan`: [Single Workflow Lane, Explain-Change Before Verify Execution Plan](../docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md)
- `plan-review`: approved in [plan-review-r2](../docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/plan-review-r2.md)
- `test-spec`: [RigorLoop workflow test spec](rigorloop-workflow.test.md), [Workflow stage autoprogression test spec](workflow-stage-autoprogression.test.md), [Milestone-aware review handoff test spec](milestone-aware-review-handoff.test.md), and [Skill contract test spec](skill-contract.test.md) confirm the active implementation proof map.
- `proposal`: [Separately Armed Implementation Autoprogression Through Verify](../docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md)
- `proposal-review`: approved in [proposal-review-r1](../docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/proposal-review-r1.md)
- `spec-review`: approved in [spec-review-r1](../docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/spec-review-r1.md)

## Readiness

- Approved amendment for separately armed implementation autoprogression through verify.
- Ready for architecture assessment before downstream planning or implementation relies on the new profile.
