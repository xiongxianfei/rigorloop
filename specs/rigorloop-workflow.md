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

## Goal and context

This spec defines the externally observable workflow contract for the first RigorLoop starter-kit release. The goal is to make AI-assisted software delivery explicit, reviewable, and auditable for individual contributors and maintainers without forcing the full artifact lifecycle onto trivial work.

This amendment updates the workflow contract around explicit artifact categories, stable stage-obligation metadata, living-reference handling, workflow-handoff ownership, the final learn artifact model, and PR-self-contained lifecycle completion. It keeps `specs/rigorloop-workflow.md` as the canonical workflow definition and keeps `docs/workflows.md` as the short operational summary.

This amendment also clarifies that isolated formal review requests stop downstream handoff but do not suppress durable recording. Every material finding is recorded, and all material findings require change-local review files.

RigorLoop is a Git-first starter kit. It does not replace pull requests, CI, or human review. It provides a repeatable path, artifact model, and validation rules so contributors can move from idea to reviewed change with traceable evidence.

## Glossary

- `fast lane`: the reduced path for trivial or low-risk work.
- `full lifecycle`: the default path for non-trivial work that uses the staged workflow artifacts.
- `planned milestone work`: work governed by a concrete plan that defines one or more explicit milestones.
- `change artifact`: a durable Markdown document that explains proposal, spec, plan, tests, verification, or rationale for a change.
- `change metadata`: machine-readable traceability data for a change.
- `change.yaml`: the first-release canonical machine-readable traceability file for a non-trivial change.
- `canonical source`: the authored workflow content from which generated output is derived.
- `generated output`: derived distribution content that can be rebuilt and is not the source of truth.
- `adapter`: tool-specific guidance or generated output layered on top of generic workflow content.
- `workflow-managed completion flow`: a change flow that is being carried through its normal downstream stages toward completion under the active lane.
- `isolated stage request`: a request for the output of one stage only, such as standalone review, verification, or explanation work.
- `tracked artifact`: any version-controlled repository file whose change will be committed or reviewed as part of the work.
- `shared review-skill recording subsection`: the identical `## Isolation and Recording` guidance copied into all formal review skills from `templates/shared/review-isolation-and-recording.md`.
- `scan-first review resolution`: a `review-resolution.md` structure that exposes closeout status, covered reviews, finding counts, disposition overview, shared validation evidence, and per-finding details without forcing reviewers to read repeated prose first.
- `immediate next repository stage`: the next mandatory or triggered downstream repository stage for the current lane and invocation context.
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

## Examples first

### Example E1: golden-path feature change

Given a contributor wants immediate feedback when adding or editing a skill
When they implement "Add a skill metadata validator and CI check"
Then the change follows the full lifecycle, produces linked artifacts, adds structural validation commands, and ends with a PR that summarizes the change and links to durable reasoning.

### Example E2: trivial docs-only fix

Given a contributor fixes a typo in workflow documentation
When the change does not alter behavior, workflow order, schemas, CI behavior, or generated output logic
Then the contributor may use the fast lane with a spec, targeted verification, and a PR instead of the full lifecycle.

### Example E3: fast-lane rejection

Given a contributor changes workflow stage ordering or CI behavior
When they attempt to classify the change as fast-lane
Then the change is rejected from the fast lane and must use the full lifecycle because it changes contributor-visible behavior and review gates.

### Example E4: planned milestone work in one PR

Given a contributor executes planned milestone work under a concrete plan
When milestone `M1` and milestone `M2` both complete with updated plan evidence and milestone commits
Then one pull request may contain both milestone commits if the combined review unit is clearer than opening a separate pull request for each milestone.

### Example E5: single-slice change without milestone commit format

Given a contributor makes a fast-lane change or a non-trivial unplanned single-slice change with no plan-defined milestone boundary
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
Then `verify`, final `explain-change`, and `pr` do not proceed until required review-resolution closeout is complete.

### Example E9: CI maintenance is not validation execution

Given validation commands already exist and hosted CI can run them
When a contributor reaches verification
Then the `verify` stage owns validation evidence, while `ci-maintenance` runs only if hosted workflow automation or related CI infrastructure is missing, stale, or wrong for a material risk.

### Example E10: learn runs on triggers, not by default

Given a small ordinary change completes with no repeated findings, incidents, failed release smoke, postmortem action, cadence run, or maintainer request
When the PR package is ready
Then `learn` is not treated as a final per-change stage.

### Example E11: plan closes inside the completing PR

Given a planned initiative completes implementation, review-resolution, verification, explain-change, and PR handoff inside one branch
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

## Requirements

R1. The starter kit MUST support two contributor-visible paths:
- a fast lane for trivial or low-risk work;
- a full lifecycle for non-trivial work.

R2. The fast lane MUST be limited to the following categories unless a maintainer explicitly reclassifies the change:
- typos;
- formatting-only changes;
- small documentation clarifications;
- comment-only changes;
- small test-fixture corrections;
- small non-behavioral renames;
- minor generated-artifact refreshes that do not change generator behavior.

R3. A change MUST NOT use the fast lane when it touches any of the following:
- public behavior;
- workflow order or stage policy;
- skill triggering rules;
- architecture boundaries;
- security-sensitive behavior;
- CI behavior;
- release packaging;
- schemas;
- generated-output logic;
- changes that are hard to roll back safely.

R4. A fast-lane change MUST record a spec containing:
- intent;
- expected change;
- out of scope;
- validation.

R5. The fast-lane spec MUST be present in at least one contributor-visible location:
- PR body;
- issue comment;
- commit message;
- dedicated change note linked from the PR.

R6. The workflow contract MUST document workflow categories using the following category table:

| Category | Artifacts or stages | Creation rule | Revision or refresh rule | Staleness or absence check | Dependents |
| --- | --- | --- | --- | --- | --- |
| Standing artifacts | `VISION.md`, `CONSTITUTION.md` | Created once near project genesis or governance adoption. | Revised deliberately when project identity or governing principles change. | Absence gates differ by artifact and are defined in `R6a`. | All proposal, spec, workflow, and review stages. |
| Living references | `docs/project-map.md` | Created when repository structure is not obvious enough for safe architecture or planning. | Refreshed or bypassed with a no-map rationale before reliance when absent, known-stale, contradicted, or missing the relied-on area. | Detailed freshness markers, calendar thresholds, and revision workflow are deferred to a focused project-map lifecycle change. | Architecture, plan, code-review, and onboarding-heavy work. |
| Workflow infrastructure | `specs/rigorloop-workflow.md`, `docs/workflows.md`, affected root operating guidance, affected stage skills, and generated skill or adapter outputs when canonical skills change. | Created and maintained as workflow governance. | Revised when stage order, routing, handoff, obligation, or category policy changes. | Unresolved drift across affected operating and governance surfaces blocks workflow-change readiness. | Every lifecycle stage. |
| On-demand artifacts | `explore`, `research`. | Created only when the problem warrants durable option expansion or external evidence. | Revised when their assumptions or findings are materially outdated. | Absence is not a blocker unless the current work depends on unresolved options or uncertain facts. | Proposal, spec, architecture, and plan when their decisions depend on the artifact. |
| Per-change chain | `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution -> verify -> explain-change -> pr`, with conditional `ci-maintenance` support. | Created or run according to stage-obligation metadata. | Updated as the change moves through the lifecycle. | Missing required or triggered actions block downstream readiness. | The current change and PR package. |
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

R7. The starter kit MUST document stage expectations using the following obligation model:
- `mandatory`: required whenever the row's trigger applies;
- `conditional`: required only when the trigger applies or the artifact/action is cited as a dependency;
- `on-demand`: created or run only when explicitly invoked or when the current work depends on its output;
- `periodic`: run on cadence, incident, repeated finding, failed smoke, accepted postmortem action, or explicit maintainer request rather than as a per-change stage.

R7a. The full lifecycle for non-trivial work MUST be documented using the following stage-obligation table. The `Runs for every change` column applies within the full-lifecycle lane after the row trigger makes the stage applicable; it MUST NOT override fast-lane eligibility or the trigger column.

| Stage or action | Role | Obligation | Trigger | Runs for every change | Blocks downstream when missing |
| --- | --- | --- | --- | --- | --- |
| `explore` | Expand options. | `on-demand` | Strategic ambiguity, unclear problem framing, option expansion, architecture-level uncertainty, or maintainer request. | `false` | `true` |
| `research` | Verify external facts. | `on-demand` | Current external docs, APIs, versions, competitors, standards, laws, pricing, or operational facts affect the decision. | `false` | `true` |
| `proposal` | Choose direction. | `mandatory` | New direction, public behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract. | `true` | `true` |
| `proposal-review` | Challenge direction. | `conditional` | Workflow-governance, direction-setting, high-risk, or maintainer-requested proposals. | `false` | `true` |
| `spec` | Define behavior or contract. | `mandatory` | Externally observable behavior, workflow policy, schema, generated output, compatibility, security-sensitive behavior, or public contributor expectation changes. | `true` | `true` |
| `spec-review` | Check ambiguity and testability. | `mandatory` | Behavior, workflow, schema, compatibility, or safety-sensitive changes. | `true` | `true` |
| `architecture` | Define system shape. | `conditional` | Boundary, data flow, generated package, CI infrastructure, integration, storage, deployment, or long-lived design impact. | `false` | `true` |
| `architecture-review` | Challenge design. | `conditional` | High-risk, cross-component, migration-heavy, security-sensitive, or hard-to-reverse design. | `false` | `true` |
| `plan` | Sequence implementation. | `conditional` | Multi-file, risky, ambiguous, migration-heavy, sequencing-sensitive, or milestone-based work. | `false` | `true` |
| `plan-review` | Validate execution plan. | `conditional` | Multi-milestone, sequencing-sensitive, recovery-sensitive, or maintainer-requested work. | `false` | `true` |
| `test-spec` | Define proof. | `mandatory` | Behavior or workflow-contract proof is required. | `true` | `true` |
| `implement` | Make the change. | `mandatory` | The accepted contract is ready to change tracked artifacts. | `true` | `true` |
| `code-review` | Inspect the diff. | `mandatory` | Non-trivial changes. | `true` | `true` |
| `review-resolution` | Close review findings. | `conditional` | Material review findings, non-final dispositions, or review outcomes require explicit closeout. | `false` | `true` |
| `verify` | Prove result. | `mandatory` | Every contributed change. | `true` | `true` |
| `ci-maintenance` | Create or update hosted CI workflow automation. | `conditional` | Hosted workflow automation or related CI infrastructure for a material risk is missing, stale, or wrong. | `false` | `true` |
| `explain-change` | Explain final diff. | `mandatory` | Non-trivial changes require standalone durable explanation; all changes require PR-summary explanation. | `true` | `true` |
| `pr` | Prepare review package. | `mandatory` | Every contributed change. | `true` | `true` |
| `learn` | Capture retrospective lessons. | `periodic` | Cadence run, incident response, contributor observation, repeated review findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem action changing workflow guidance, or explicit maintainer request. | `false` | `false` |

R7b. For conditional and on-demand rows, downstream blocking applies only after the trigger is active, the artifact/action has been cited as a dependency, or a higher-priority artifact requires it. For periodic rows, downstream blocking applies only when a higher-priority artifact explicitly makes the triggered periodic work blocking.

R7ba. `learn` is a periodic or explicitly invoked retrospective artifact. A cadence run, incident response, contributor observation, repeated review finding, blocker or major workflow-process finding, failed release or adapter smoke, accepted postmortem action changing workflow guidance, or explicit maintainer request MUST be sufficient to trigger `learn`.

R7bb. Triggered `learn` MUST NOT block ordinary `verify`, final `explain-change`, or `pr` closeout by default.

R7bc. Triggered `learn` MUST block downstream only when a higher-priority artifact explicitly makes it blocking, such as an active plan, `review-resolution`, postmortem action, release contract, or maintainer decision.

R7bd. If a `learn` invocation reaches the `Frame` phase, it MUST create or update a tracked session record under `docs/learn/sessions/YYYY-MM-DD-<slug>.md`. This requirement applies even when the session finds no observations or no durable lesson.

R7be. Review-visible no-record surfaces for scheduled follow-up, deferral, or explicit no-learn rationale MUST be allowed only for pre-session trigger closeout when `learn` does not actually run as a session. Chat-only notes MUST NOT satisfy required tracked or review-visible closeout.

R7bf. Learn session routing MUST follow `specs/learn-artifact-model.md`: session records live under `docs/learn/sessions/`, durable topic guidance lives under `docs/learn/topics/` only when confirmed durable lessons justify it, and behavior, workflow, validation, skill, architecture, or decision changes go to the affected action-owning artifact. Topic files are curated guidance and MUST NOT override authoritative artifacts.

R7c. The starter kit MUST distinguish workflow-managed completion flows from isolated stage requests when deciding whether a stage result should continue automatically into a downstream stage.

R7d. When an approved continuation contract applies, a workflow-managed completion flow MUST continue automatically into the next mandatory or triggered downstream stage for the current lane unless a documented stop condition applies. Redundant user re-invocation MUST NOT be required merely to enter that already-known downstream stage.

R7e. Unless a later approved change broadens scope, v1 continuation applies only to:
- authoring-to-review handoffs for `proposal`, `spec`, and `architecture` when the matching review stage is the next mandatory or triggered downstream step;
- full-feature execution flow from `implement` through `pr`.

R7f. In v1, fast-lane and bugfix execution remain explicit-step by default, and on-demand or periodic actions such as `explore`, `research`, and `learn` MUST NOT auto-run unless the user explicitly requests them or a later approved rule elevates them.

R7g. Direct invocation of `pr` remains allowed. Isolation prevents downstream continuation beyond `pr`, but it MUST NOT downgrade `pr` itself from opening a pull request when readiness passes.

R7h. Workflow-facing review outputs that report both stage handoff and later-stage fitness MUST distinguish immediate next repository stage from downstream readiness.

R7i. `spec-review` output MUST report review outcome, immediate next repository stage, and eventual `test-spec` readiness separately.

R7j. `spec-review` immediate next repository stage MUST use only repository stages:
- `architecture` when the review outcome is approved and a separate architecture step remains required;
- `plan` when the review outcome is approved and no separate architecture step remains required;
- `spec` when the review outcome is `changes-requested` or `blocked`;
- omitted or explicitly empty when the review outcome is `inconclusive`.

R7k. `spec-review` eventual `test-spec` readiness MUST use exactly one of:
- `ready`;
- `conditionally-ready`;
- `not-ready`;
- `not-assessed`.

R7l. Approved `spec-review` MUST pair only with eventual `test-spec` readiness `ready` or `conditionally-ready`. `conditionally-ready` MUST name the remaining intermediate dependency or dependencies.

R7m. `changes-requested` and `blocked` spec-review outcomes MUST pair with eventual `test-spec` readiness `not-ready`. `inconclusive` MUST pair with eventual `test-spec` readiness `not-assessed`.

R7n. When eventual `test-spec` readiness is `not-ready`, the output MUST state that downstream planning stops, name `spec` as the required upstream fix surface, and identify the blocking defect category. When eventual `test-spec` readiness is `not-assessed`, the output MUST record the stop condition and missing required input without naming any immediate next repository stage.

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

R8. The starter kit MUST treat the following stages as mandatory for every contributed change:
- implement;
- verify;
- pr.

R8a. For planned milestone work, a milestone MUST NOT be treated as complete until all of the following are true:
- the milestone deliverable is complete;
- relevant validation for that milestone has passed;
- when targeted tests are applicable, those tests have passed;
- when targeted tests are not applicable, a contributor-visible no-test rationale has been recorded;
- the concrete plan's progress and validation notes reflect the milestone outcome;
- any milestone-level decision changes are recorded in the plan or related artifact;
- the milestone changes are committed to git as one coherent milestone commit with no unrelated changes included.

R8b. A completed milestone commit MUST use the subject format:
- `M<n>: <completed milestone outcome>`

R8c. A completed milestone commit SHOULD include a short body that summarizes the milestone deliverable and records milestone validation command output or a reference to contributor-visible validation evidence.

R8d. The workflow MUST allow a pull request to contain one or more completed milestone commits. A completed milestone only needs a separate pull request when it is independently reviewable, independently verified, and safe to merge on its own.

R8e. The milestone commit requirements in `R8a` through `R8d` apply only to planned milestone work. Fast-lane changes and non-trivial single-slice changes without a plan-defined milestone boundary MAY use normal commit subjects and do not require milestone-formatted commits.

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

R9b. The existing `skills/ci/` path MAY remain the skill entrypoint for CI infrastructure work as long as contributor-visible workflow guidance uses `ci-maintenance` for the stage/action label and keeps validation execution under `verify`.

R10. The starter kit MUST treat `explain-change` as:
- required in PR summary form for every change;
- required as a standalone durable artifact for non-trivial changes.

R10a. For new non-trivial work, the default standalone durable reasoning artifact MUST be `docs/changes/<change-id>/explain-change.md`.

R10b. PR text alone MUST NOT satisfy the standalone durable reasoning requirement for non-trivial work.

R10c. The only allowed equivalent to the default standalone durable reasoning artifact is another artifact class explicitly named by this workflow spec as satisfying durable reasoning for the change.

R10d. Approved legacy top-level explain artifacts, including approved artifacts under `docs/explain/`, MUST remain valid durable reasoning surfaces until they are migrated, superseded, archived, or otherwise retired.

R10e. New top-level explain artifacts MUST NOT be created unless this workflow spec explicitly allows that artifact class.

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

R12ae. `needs-decision` is not a final disposition. It is an unresolved stop state and MUST block `verify`, `explain-change`, and `pr` until an authorized owner resolves the decision or explicitly defers it.

R12af. `review-resolution.md` MUST have a top-level closeout status of exactly `Closeout status: open` or `Closeout status: closed`.

R12ag. `Closeout status: open` means one or more material findings are not yet fully resolved for handoff. `Closeout status: closed` means every material finding has a final disposition, all disposition-specific closeout requirements are satisfied, and `review-log.md` lists no open findings.

R12ah. A finding with disposition `accepted` may count toward `Closeout status: closed` only when the chosen action and validation evidence are recorded.

R12ai. A finding with disposition `rejected` may count toward `Closeout status: closed` only when rationale is recorded.

R12aj. A finding with disposition `deferred` may count toward `Closeout status: closed` only when deferral rationale and a follow-up owner, owning stage, or explicit no-follow-up reason are recorded.

R12ak. A finding with disposition `partially-accepted` may count toward `Closeout status: closed` only when the accepted portion has action and validation evidence, and the rejected or deferred portion has its required rationale and follow-up or no-follow-up record.

R12al. A first-pass review outcome that requires revision, changes, or blocks downstream progress MUST be closed by a valid same-stage later review round or by explicit reviewer or owner closeout evidence naming the original Review ID. `review-resolution.md` alone MUST NOT silently replace required re-review or owner closeout.

R12am. `verify`, final `explain-change` closeout, and `pr` handoff MUST NOT proceed while `review-log.md` still lists open findings.

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

R12bda. The output MUST state isolated handoff status, material Finding IDs, required durable review record path or reconstruction requirement, that `review-resolution.md` is required, and next allowed action.

R12bdb. The next allowed action MUST be one of `create-change-local-record-before-fixing`, `reconstruct-record-because-fixes-already-began`, or `stop-for-owner-decision`.

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
- verification evidence cannot remain concise in `docs/changes/<change-id>/explain-change.md`;
- the change requires a durable standalone verification record for reviewer or maintainer audit;
- the change has multiple verification commands, environments, or result groups that need separate traceable reporting;
- repository policy for the change type explicitly requires a standalone verification artifact;
- a reviewer or maintainer explicitly requests a standalone verify report;
- the verification stage is itself a reviewed deliverable for the change.

R12e. When none of the `R12d` triggers apply, verification evidence MAY remain in `docs/changes/<change-id>/explain-change.md` or the PR summary, provided the workflow's durability and concision requirements remain satisfied.

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

R25h. Fast-lane changes MAY omit `change.yaml` unless a maintainer explicitly requires structured metadata for that change.

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
- generated adapter distribution content;
- local and CI validation results.

## State and invariants

- Canonical workflow content remains editable source material.
- Generated distribution content remains rebuildable derived output.
- Every mandatory or triggered blocking stage has contributor-visible evidence.
- Stage-obligation values remain stable and machine-checkable: `mandatory`, `conditional`, `on-demand`, and `periodic`.
- `specs/rigorloop-workflow.md` remains the canonical workflow definition, while `docs/workflows.md` remains a summary.
- Skill handoff sections summarize local preconditions, outputs, failure modes, and brief next-stage pointers without duplicating the full workflow contract.
- Fast-lane work stays limited to trivial or low-risk changes.
- Full-lifecycle work remains traceable from proposal/spec direction through PR summary and verification evidence.
- Completed planned milestones remain visible as coherent branch or pull-request review boundaries even when multiple milestones share one pull request.
- Repo-local lifecycle state in a review-open PR is true within that PR's tracked tree.
- Merge integrates pre-validated repo-local lifecycle state; it does not perform routine lifecycle closeout.

## Error and boundary behavior

- A change classified as fast-lane but matching any full-lifecycle exclusion in `R3` MUST be rejected from fast-lane treatment.
- A fast-lane change missing the required spec fields in `R4` MUST be considered incomplete.
- A planned milestone closed without the completion evidence required by `R8a` or without the standardized milestone commit subject required by `R8b` MUST be considered incomplete.
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
- An isolated review output with material findings that omits handoff status, material Finding IDs, required record path or reconstruction requirement, `review-resolution.md` requirement, or next allowed action MUST be considered incomplete.
- A copied formal review skill `## Isolation and Recording` subsection that differs from `templates/shared/review-isolation-and-recording.md`, or contains stage-specific insertions inside the shared block, MUST fail structural validation.
- A new `review-resolution.md` that removes required per-finding parseable labels for scan-first formatting MUST be considered invalid for review closeout.
- `verify`, final `explain-change`, and `pr` MUST stop while required `review-resolution` closeout remains open.
- Triggered `learn` MUST NOT stop ordinary `verify`, final `explain-change`, or `pr` when no higher-priority artifact makes it blocking and either the pre-session closeout is recorded or the session record captures the outcome after Frame.
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
- In-flight work MAY complete on the workflow contract that was active when it started unless the active owner opts into the refactored model or the work touches refactored workflow surfaces directly.
- Planned initiatives and change-local metadata SHOULD record the selected workflow contract, such as `pre-refactor` or `refactored`, when that distinction affects review or verification.
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
- PR-self-contained lifecycle completion warnings SHOULD be contributor-visible and identify the tracked file that contains merge-dependent language.

## Security and privacy

- Baseline validation commands MUST NOT require repository secrets to validate skill structure or generated-output drift.
- The workflow MUST avoid making external network access a requirement for routine structural validation.
- Tool-specific adapters MUST NOT weaken the generic workflow requirement that human review and repository controls remain authoritative.

## Accessibility and UX

- Contributor-facing templates SHOULD use concise, repeatable section headings so contributors can follow the workflow without reverse-engineering hidden rules.
- Fast-lane instructions SHOULD fit comfortably inside common PR or issue workflows without requiring extra tooling.
- New `review-resolution.md` records SHOULD prefer summary-first structure, an overview table, compact finding details, shared validation evidence, and a closeout checklist when those elements make the file easier to scan.

## Performance expectations

- Local structural validation and drift checks SHOULD be lightweight enough to run as part of normal contributor pre-PR workflow.
- The first release does not define numeric latency budgets for validation commands.

## Edge cases

1. A generated-artifact refresh with no generator logic change may use the fast lane if the fast-lane spec states that only derived output was refreshed and targeted verification confirms no source logic changed.
2. A documentation-only change that alters workflow order, classification rules, or contributor obligations is not fast-lane eligible because it changes contributor-visible behavior.
3. A change that adds CI automation without altering product behavior still requires the full lifecycle because CI behavior is explicitly excluded from fast-lane eligibility.
4. A repository may carry both generic workflow content and Codex-specific adapters, but contributors must still edit canonical source rather than generated distribution output.
5. A PR with no automated tests run may still be valid only when the PR text states why tests were not applicable and the change remains within fast-lane or otherwise approved scope.
6. A non-trivial change may resolve review feedback entirely inside the PR or explain-change artifact when the feedback is routine and does not create durable project memory beyond the current review.
7. A non-trivial change may omit some artifact keys from `change.yaml` when those artifact types are not applicable to the change, but it may not omit the required top-level fields listed in `R25b`.
8. A completed milestone that is not independently safe to merge may remain inside a larger pull request, but it still requires the completion evidence and milestone commit boundary defined in `R8a` and `R8b`.
9. A fast-lane change or non-trivial unplanned single-slice change may use a normal commit subject because milestone-formatted commits are reserved for planned milestone work.
10. An accepted proposal, approved spec, approved architecture document, active test spec, or accepted or active ADR may remain current guidance without immediate closeout as long as its readiness text is truthful and terminal disposition has not occurred.
11. Final PR text may reference additional authoritative artifacts only after `verify` is rerun against those new references or an equivalent updated pre-PR handoff surface.
12. An ordinary non-trivial change may satisfy the baseline change-local pack with `docs/changes/<change-id>/change.yaml` plus `docs/changes/<change-id>/explain-change.md` when standalone `review-resolution.md` and `verify-report.md` triggers do not apply.
13. `docs/changes/0001-skill-validator/` may include more artifacts than an ordinary non-trivial change without making those additional artifacts universal requirements.
14. Approved legacy top-level explain artifacts under `docs/explain/` remain valid for already-shipped work until they are migrated, superseded, archived, or otherwise retired.
15. Successful `spec-review` may still say the immediate next repository stage is `architecture` while separately reporting eventual `test-spec` readiness `conditionally-ready`.
16. `inconclusive` may record a missing-input stop condition without naming any immediate next repository stage.
17. `plan-review` may mention implementation readiness only after preserving `test-spec` as the immediate next handoff.
18. `explore` and `research` may be absent from a normal non-trivial change when the problem and facts are already settled, but they block downstream reliance after their triggers are active or their artifacts are cited as dependencies.
19. `learn` may be absent from an ordinary PR package, but a repeated finding, blocker or major workflow-process finding, failed release or adapter smoke, accepted postmortem action, cadence run, incident response, contributor observation, or explicit maintainer request must be closed through a `docs/learn/sessions/**` session record once Frame is reached, or through a scheduled follow-up, deferral, or explicit no-learn rationale before a session runs. It blocks downstream only when a higher-priority artifact explicitly makes it blocking.
20. `ci-maintenance` may be skipped when hosted workflow automation already covers the material risk, but it is required when automation is missing, stale, or wrong.
21. A repository without `docs/project-map.md`, with a known-stale or contradicted map, or with a map missing the relied-on area may proceed only when consumers do not rely on the map or record a no-map rationale for the relevant architecture, planning, review, or onboarding-heavy decision.
22. A bootstrap proposal may proceed without an existing `VISION.md` only when its `Vision fit` explicitly identifies that it is creating or migrating the missing standing artifact.
23. A bootstrap proposal may proceed without an existing `CONSTITUTION.md` for governance adoption, workflow-governance, or source-of-truth changes only when its `Vision fit` explicitly identifies that it is creating or migrating the missing constitution.
24. A change with open material review findings may not proceed to `verify`, final `explain-change`, or `pr` even when implementation tests pass.
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

## Non-goals

- Building a hosted orchestration platform.
- Replacing Git-based review workflows with agent-managed state.
- Enforcing subjective writing-quality scores in early CI.
- Requiring the full lifecycle for trivial or low-risk work.
- Hardcoding every future adapter implementation detail into the first workflow contract.
- Implementing detailed project-map freshness markers, calendar thresholds, or revision workflow in this refactor.
- Creating learn session templates, topic templates, empty topic files, a fixed topic taxonomy, automated lesson triage, or historical-note migration.
- Removing `explore`, `research`, or `learn`; they remain available through their trigger rules.
- Rewriting project vision content or revisiting the completed `VISION.md` migration.
- Renaming the `skills/ci/` directory as a contract requirement.
- Inspecting hosted PR-description event metadata for merge-dependent language in the first enforcement slice.
- Defining a merge-SHA recording exception before a real immutable-merge-metadata case exists.
- Treating deploy, release, package publication, or external migration completion as repo-local lifecycle state that can be made true by the PR tree.
- Adding semantic validator detection for tracked artifact edits that mention unresolved review findings in the first review-recording slice.
- Generating formal review skill shared subsections instead of manually copying a canonical block.

## Acceptance criteria

- A contributor can follow the documented fast lane for a trivial change and produce a complete PR with spec and validation.
- A contributor can follow the documented full lifecycle for the skill validator example and produce linked durable artifacts plus validation evidence.
- A contributor can close a planned milestone with updated plan evidence and a standardized milestone commit without being forced to open a separate pull request for that milestone.
- A contributor can make a fast-lane or non-trivial single-slice change without using a milestone-formatted commit and still remain within the workflow contract.
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
- A reviewer can tell when `spec-review` is reporting immediate next repository stage versus eventual `test-spec` readiness without inferring that `test-spec` skips required intermediate stages.
- A reviewer can tell that `plan-review` preserves `test-spec` as the immediate next handoff even when later implementation readiness is also discussed.
- A contributor can tell that `explore` and `research` are on-demand support rather than default prerequisites.
- A contributor can tell that triggered `learn` creates a tracked session record after Frame, that pre-session follow-up, deferral, or no-learn closeout is recorded in an allowed contributor-visible tracked or review-visible surface, that durable topic guidance uses `docs/learn/topics/**`, and that triggered `learn` blocks downstream only when a higher-priority artifact explicitly makes it blocking.
- A contributor can tell that `ci-maintenance` means CI infrastructure maintenance and not validation execution.
- A contributor can tell that `review-resolution` is the closeout stage for review findings and that open required closeout blocks `verify`, final `explain-change`, and `pr`.
- A contributor can tell which formal lifecycle review outcomes require detailed review files, when clean reviews remain artifact-local, and when no-material review records omit empty `review-resolution.md`.
- A reviewer can distinguish an initial review-record root from the final non-trivial change-local pack.
- A contributor can distinguish isolated review handoff from material-finding recording obligations.
- A contributor can tell that every material finding is recorded and all material findings require change-local review files.
- A contributor can identify tracked artifacts for review-recording purposes.
- An isolated review output with material findings exposes handoff status, material Finding IDs, required record path or reconstruction requirement, `review-resolution.md` requirement, and next allowed action.
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

## Open questions

- None for the review skill material-finding recording amendment. The `skills/ci/` path remains allowed while the visible stage/action label becomes `ci-maintenance`; detailed periodic `learn` cadence scheduling remains outside this workflow contract.

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

## Readiness

Approved amendment for review skill material-finding recording and scan-first review-resolution guidance. Matching test spec is updated; the active plan now governs M1 proof-map work.
