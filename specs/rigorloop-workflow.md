# RigorLoop Workflow

## Status
- approved

## Related proposal

- [RigorLoop Project Direction](../docs/proposals/2026-04-19-rigorloop-project-direction.md)
- [Implementation Milestone Commit Policy](../docs/proposals/2026-04-19-implementation-milestone-commit-policy.md)

## Goal and context

This spec defines the externally observable workflow contract for the first RigorLoop starter-kit release. The goal is to make AI-assisted software delivery explicit, reviewable, and auditable for individual contributors and maintainers without forcing the full artifact lifecycle onto trivial work.

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

R6. The default full lifecycle for non-trivial work MUST be documented using the following stage-classification table:
| Stage                 | Role                    | Start as                          | Eventually enforce when                                                              |
| --------------------- | ----------------------- | --------------------------------- | ------------------------------------------------------------------------------------ |
| `explore`             | expand options          | advice                            | strategic, ambiguous, architecture-level, or high-risk work                          |
| `research`            | verify external facts   | advice                            | claims depend on current external docs, APIs, versions, or competitors               |
| `proposal`            | choose direction        | default                           | new feature, public behavior change, or workflow change                              |
| `proposal-review`     | challenge direction     | advice/default                    | major feature, risky direction, or maintainer-requested                              |
| `spec`                | define behavior         | default                           | any user-visible or agent-visible behavior change                                    |
| `spec-review`         | check ambiguity         | default                           | public behavior, schemas, workflow stages, or skill trigger rules                    |
| `architecture`        | define system shape     | conditional default               | boundaries, generated artifacts, package layout, CI, storage, or integrations change |
| `architecture-review` | challenge design        | advice                            | high-risk or multi-module architecture change                                        |
| `plan`                | sequence implementation | default                           | multi-step work or more than trivial changes                                         |
| `plan-review`         | validate execution plan | default                           | multi-milestone work                                                                 |
| `test-spec`           | define proof            | default                           | any behavior change                                                                  |
| `implement`           | make change             | enforced                          | always                                                                               |
| `code-review`         | inspect diff            | default                           | all non-trivial PRs                                                                  |
| `review-resolution`   | handle suggestions      | enforced if review comments exist | any accepted/rejected/deferred review item                                           |
| `verify`              | prove result            | enforced                          | every PR                                                                             |
| `ci`                  | create or update risk-focused GitHub workflows | conditional default | automation needed to cover a material risk is missing or stale                       |
| `explain-change`      | explain final diff      | default                           | standalone artifact for non-trivial work; PR summary for all work                    |
| `pr`                  | review package          | enforced                          | every contribution                                                                   |
| `learn`               | retrospective           | advice                            | surprising, repeated, failed, or large changes                                       |


R7. The starter kit MUST document stage expectations using the following enforcement model:
- `advice`: recommended when useful but not required for every eligible change;
- `default`: expected for normal non-trivial work unless explicitly waived;
- `enforced`: missing evidence blocks the change from being considered complete.

R7a. When the stage-classification table uses a combined classification, it MUST be interpreted as follows:
- `advice/default`: advice by default, but elevated to `default` when the listed trigger applies;
- `conditional default`: not required for every change, but treated as `default` when the listed trigger applies;
- `enforced if review comments exist`: not required when no review feedback exists, but treated as `enforced` when review feedback exists.

R7b. The "Eventually enforce when" column in the stage-classification table MUST be treated as the authoritative trigger list for elevating a stage from its starting classification to a stricter expectation.

R8. The starter kit MUST treat the following stages as enforced for every contributed change:
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

R8h. When the outcome is already known before PR creation, a `Done` transition SHOULD be recorded before the PR is opened. A merge-dependent `Done` transition MAY be completed in immediate post-merge cleanup only when merged state is the deciding event for completion.

R8i. `Blocked` and `Superseded` lifecycle transitions for planned initiatives MUST be recorded as soon as they are decided.

R8j. `verify` MUST treat stale lifecycle state between `docs/plan.md` and the plan body as blocking PR readiness for planned initiatives.

R8ja. At minimum, stale lifecycle state includes:
- a completed, blocked, or superseded planned initiative still listed under `## Active`;
- `docs/plan.md` and the corresponding plan body presenting conflicting lifecycle state;
- a plan body marked done, blocked, or superseded while still presenting itself as active or in progress through status or readiness wording.

R9. Once repository CI exists, the starter kit MUST treat routine CI validation results as enforced for every pull request.

R9a. In the lifecycle stage table, `ci` MUST refer to creating or updating GitHub workflows or related repository automation needed to cover material change risk. It MUST NOT refer only to waiting for existing CI checks to run.

R10. The starter kit MUST treat `explain-change` as:
- required in PR summary form for every change;
- required as a standalone durable artifact for non-trivial changes.

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

R12a. When review feedback exists for a change, each review item MUST be recorded as:
- accepted;
- rejected; or
- deferred,
with rationale for the recorded disposition.

R12b. Review resolution MAY be recorded in any of the following contributor-visible locations:
- PR body;
- explain-change artifact;
- standalone `review-resolution.md` artifact.

R12c. A standalone `review-resolution.md` artifact MUST be used when any of the following is true:
- review feedback changes behavior defined by the spec;
- review feedback changes architecture or ADR direction;
- review feedback changes the implementation plan;
- review feedback changes test strategy;
- review feedback raises security, correctness, compatibility, or data-risk concerns that future maintainers must understand;
- review feedback creates rejected or deferred items with durable project value;
- the change goes through multiple material review rounds;
- a maintainer explicitly requests a standalone review-resolution artifact.

R13. The first proof-of-value example shipped by the starter kit MUST be a skill metadata validator change that demonstrates the workflow end to end.

R14. The proof-of-value example MUST include durable artifacts for proposal, spec, plan, test-spec, verify report, and explain-change.

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
- change artifacts and PR text;
- local validation commands and CI workflow configuration;
- tool-specific adapter inputs when an adapter is enabled.

### Outputs

- contributor-visible workflow documentation;
- durable change artifacts;
- PR summary and validation notes;
- machine-readable change metadata for non-trivial work at `docs/changes/<change-id>/change.yaml`;
- generated adapter distribution content;
- local and CI validation results.

## State and invariants

- Canonical workflow content remains editable source material.
- Generated distribution content remains rebuildable derived output.
- Every enforced stage has contributor-visible evidence.
- Fast-lane work stays limited to trivial or low-risk changes.
- Full-lifecycle work remains traceable from proposal/spec direction through PR summary and verification evidence.
- Completed planned milestones remain visible as coherent branch or pull-request review boundaries even when multiple milestones share one pull request.

## Error and boundary behavior

- A change classified as fast-lane but matching any full-lifecycle exclusion in `R3` MUST be rejected from fast-lane treatment.
- A fast-lane change missing the required spec fields in `R4` MUST be considered incomplete.
- A planned milestone closed without the completion evidence required by `R8a` or without the standardized milestone commit subject required by `R8b` MUST be considered incomplete.
- A non-trivial change missing required PR explanation or validation evidence MUST be considered incomplete.
- Invalid skill structure MUST fail local validation and CI validation.
- Generated-output drift MUST fail the drift check until derived output is rebuilt or the change is reverted.
- The starter kit MUST allow validation to run without requiring network access or Codex installation for the baseline structural checks.

## Compatibility and migration

- The first release may start with lightweight structural enforcement and add stronger traceability enforcement in later versions.
- Codex-specific guidance is optional and adapter-scoped; the generic workflow remains usable without Codex-specific installation.
- Compatibility output for legacy or project-specific Codex setups MAY be generated, but generated compatibility directories remain derived output rather than authored source.
- Later releases MAY add JSON compatibility or alternative export formats, but `docs/changes/<change-id>/change.yaml` remains the canonical first-release contract.
- Existing repositories adopting RigorLoop MAY phase in the contract incrementally, beginning with documentation and structural checks before stricter enforcement.
- Repositories that squash, rebase, or otherwise rewrite commit history MAY collapse milestone commit boundaries after merge. The first-release contract guarantees milestone visibility during branch and pull-request review, not preservation under every default-branch merge strategy.

## Observability

- Verification evidence for non-trivial work MUST record the commands run and their results in a contributor-visible location.
- PR text MUST state validation run or a no-test rationale for every change.
- When review feedback exists, the recorded review resolution MUST be visible to reviewers in the PR, explain-change artifact, or a standalone review-resolution artifact.
- `change.yaml` SHOULD make artifact and validation traceability inspectable without reading every Markdown artifact.
- For planned milestone work, contributor-visible branch or pull-request history SHOULD make milestone boundaries visible through the standardized milestone commit subjects defined in `R8b`.

## Security and privacy

- Baseline validation commands MUST NOT require repository secrets to validate skill structure or generated-output drift.
- The workflow MUST avoid making external network access a requirement for routine structural validation.
- Tool-specific adapters MUST NOT weaken the generic workflow requirement that human review and repository controls remain authoritative.

## Accessibility and UX

- Contributor-facing templates SHOULD use concise, repeatable section headings so contributors can follow the workflow without reverse-engineering hidden rules.
- Fast-lane instructions SHOULD fit comfortably inside common PR or issue workflows without requiring extra tooling.

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

## Non-goals

- Building a hosted orchestration platform.
- Replacing Git-based review workflows with agent-managed state.
- Enforcing subjective writing-quality scores in early CI.
- Requiring the full lifecycle for trivial or low-risk work.
- Hardcoding every future adapter implementation detail into the first workflow contract.

## Acceptance criteria

- A contributor can follow the documented fast lane for a trivial change and produce a complete PR with spec and validation.
- A contributor can follow the documented full lifecycle for the skill validator example and produce linked durable artifacts plus validation evidence.
- A contributor can close a planned milestone with updated plan evidence and a standardized milestone commit without being forced to open a separate pull request for that milestone.
- A contributor can make a fast-lane or non-trivial single-slice change without using a milestone-formatted commit and still remain within the workflow contract.
- The workflow clearly distinguishes what is advice, default, and enforced.
- The starter kit contract clearly separates generic methodology from Codex-specific adapters and generated output.
- The first CI contract is limited to structural validation, validator fixture testing, and generated-output drift detection.
- A reviewer can determine from the PR plus artifacts why a change exists, how it was validated, and which content is canonical versus generated.
- A reviewer can determine the disposition and rationale of review feedback without guessing whether it lives in PR text, explain-change, or a standalone review-resolution artifact.
- A reviewer can locate structured traceability for a non-trivial change in `docs/changes/<change-id>/change.yaml` and find at least the required fields defined by `R25b`.
- A reviewer can distinguish milestone commit boundaries from pull-request boundaries by inspecting standardized milestone commit subjects and the associated plan updates.

## Open questions

- None for the workflow contract. Exact repository layout details may be delegated to the architecture artifact as long as the source-of-truth separation and required contract paths in this spec are preserved.

Spec review is complete. This approved spec now governs the merged first-release workflow baseline.
