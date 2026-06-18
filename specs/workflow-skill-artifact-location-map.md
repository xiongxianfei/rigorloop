# Workflow Skill Artifact-Location Map

## Status

approved

## Related proposal

- Proposal: [Workflow Skill Artifact-Location Map](../docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md)
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md)
- Proposal review R2: [proposal-review-r2](../docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md)
- Related spec: [Installed-Skill Artifact Placement Contract](installed-skill-artifact-placement-contract.md)
- Related workflow spec: [RigorLoop Workflow](rigorloop-workflow.md)

## Goal and context

The workflow skill must create or refresh a deterministic project-local artifact-location map in `docs/workflows.md`. That map tells maintainers and agents where workflow-managed artifacts go, who owns each artifact type, and when each artifact is required.

The map does not replace stage-skill ownership of artifact content. Stage skills continue to own their own artifact schemas, stage-specific rules, and portable defaults for skill-only adopters. The workflow map customizes project-local placement and must stay synchronized with the workflow skill and directly relevant stage-skill placement text.

This spec turns the accepted proposal into a contract for:

- `docs/workflows.md` as a tracked project-local workflow map;
- canonical machine-checkable artifact registry data inside that guide;
- human-readable table projections of the registry;
- repository-standard workflow-managed plan-body placement;
- formal review-record placement;
- source-rank and ambiguity handling;
- drift validation across workflow map, workflow skill, stage skills, and generated adapters when packaged.

## Glossary

- `artifact registry`: The canonical fenced YAML block in `docs/workflows.md` that lists workflow-managed artifact types, canonical paths, owner skills, and required triggers.
- `artifact-location map`: The project-local placement contract in `docs/workflows.md`, composed of the artifact registry plus human-readable Markdown projections.
- `change pack`: The workflow-managed change-local root at `docs/changes/<change-id>/`.
- `change plan`: The detailed execution plan for one planned initiative at `docs/plans/YYYY-MM-DD-slug.md`.
- `formal lifecycle evidence`: Recorded workflow artifacts such as change metadata, review records, review log, review resolution, explain-change, verify report, and PR handoff. The detailed plan body is lifecycle state, but it remains under `docs/plans/` rather than inside the change pack.
- `plan index`: The global lifecycle index at `docs/plan.md`.
- `portable default`: A default placement rule carried by a stage skill for projects that do not have a project-local workflow map.
- `stage skill`: A specialized skill such as `proposal`, `spec`, `plan`, `proposal-review`, `spec-review`, `code-review`, `verify`, or `pr` that owns the content and stage rules for its artifact.
- `workflow guide`: `docs/workflows.md`.
- `workflow-managed change`: A change using the formal RigorLoop lifecycle and durable artifact chain.

## Examples first

Example E1: workflow guide contains a canonical registry
Given a repository uses the workflow skill to create or refresh `docs/workflows.md`
When a maintainer inspects the `Artifact registry` section
Then the guide contains a fenced YAML block with `artifact_locations`
And each repository-local artifact type has one canonical project-local path, owner skill, and required trigger.

Example E2: human-readable table matches registry
Given the artifact registry contains `change_plan.path: docs/plans/YYYY-MM-DD-slug.md`
When the `Artifact location map` Markdown table is inspected
Then the `Change plan` row shows `docs/plans/YYYY-MM-DD-slug.md`
And validation fails if the table shows a conflicting path.

Example E3: new workflow-managed change plan
Given a new workflow-managed change has change ID `2026-06-17-example`
When the plan stage creates the detailed execution plan
Then the plan is created at `docs/plans/2026-06-17-example.md`
And `docs/plan.md` remains the global plan index.

Example E4: existing plan body
Given an existing plan body exists at `docs/plans/2026-05-01-example.md`
When this spec is implemented
Then that file is not moved by this slice
And `docs/plans/` remains the canonical location for detailed plan bodies.

Example E5: formal proposal-review record
Given formal `proposal-review` records a review for change ID `2026-06-17-example`
When the review result is recorded
Then the detailed review record goes under `docs/changes/2026-06-17-example/reviews/`
And the review log is `docs/changes/2026-06-17-example/review-log.md`.

Example E6: project without workflow guide
Given a customer project has installed stage skills but lacks `docs/workflows.md`
When a stage skill resolves artifact placement
Then it uses explicit user paths, active metadata, governing constraints, and portable defaults where safe
And it blocks when placement remains ambiguous.

Example E7: unknown artifact type
Given the workflow guide has no registry entry for `release_attestation`
When the workflow skill is asked to route that artifact type
Then it does not infer a path from naming convention
And it blocks or requests a workflow-map update.

Example E8: PR handoff uses a structured non-path registry entry
Given the artifact registry includes `pr_handoff`
When validators inspect the registry
Then `pr_handoff` may use `external_surface: pull_request_body` or `policy: project_pr_process` instead of `path`
And validators fail if the entry omits both a repository-local path and a structured non-path representation.

Example E9: review customization stays change-local
Given a project customizes proposal-review filenames
When the customization is recorded in `docs/workflows.md`
Then formal review records still route under `docs/changes/<change-id>/reviews/`
And validation fails if the customization moves formal review records outside the change pack without a higher-priority explicit path, approved spec, schema, safety constraint, or user instruction.

## Requirements

R1. The workflow skill MUST state that it creates or refreshes `docs/workflows.md` when a project adopts RigorLoop, artifact locations change, or the guide contradicts current accepted placement policy.

R2. `docs/workflows.md` MUST be treated as tracked workflow contract documentation maintained by the workflow skill. It MUST NOT be treated as disposable generated output.

R3. `docs/workflows.md` MUST identify itself as the project-local artifact-location map and workflow guide.

R4. The workflow skill MUST state that stage skills own artifact content, artifact schemas, and stage-specific rules for their own artifacts.

R5. The workflow skill MUST state that stage skills retain portable defaults for projects without `docs/workflows.md`.

R6. `docs/workflows.md` MUST contain an `Artifact registry` section with a fenced YAML block.

R7. The artifact registry YAML block MUST use top-level key `artifact_locations`.

R8. Each repository-local `artifact_locations` entry MUST contain exactly one canonical `path` value for the artifact type.

R8a. Registry entries for artifacts that are not necessarily repository-local, such as PR handoff, MUST contain exactly one structured placement representation: either `path`, `external_surface`, or `policy`.

R8b. A registry entry MUST NOT contain multiple placement representations for the same artifact type unless an approved schema explicitly defines a composite artifact.

R9. Each `artifact_locations` entry MUST contain an `owner` value naming the owning skill or ownership group.

R10. Each `artifact_locations` entry MUST contain a `required_when` value or equivalent trigger field.

R11. `docs/workflows.md` MUST contain human-readable Markdown tables that project the artifact registry for maintainers.

R12. Markdown artifact-location tables MUST NOT contradict the canonical YAML registry.

R13. Validators MUST treat the YAML artifact registry as the machine-checkable source of truth for project-local artifact placement.

R14. Validators MUST detect when a Markdown artifact-location table contradicts the YAML artifact registry.

R15. The artifact registry MUST include entries for proposals, specs, test specs, architecture records, ADRs, plan index, change plan, change metadata, formal review records, review log, review resolution, explain-change, verify report, PR handoff, and learn sessions.

R16. The artifact registry MUST document `docs/plan.md` as the plan index only.

R17. The artifact registry MUST document `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body path for workflow-managed planned initiatives.

R18. The artifact registry MUST NOT document `docs/changes/<change-id>/plan.md` as a competing canonical detailed plan-body path.

R19. The implementation slice MUST retain existing `docs/plans/*.md` files in place and MUST NOT migrate them into change packs.

R20. The implementation slice MUST preserve the existing `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `plan` skill contract that detailed plan bodies live under `docs/plans/`.

R21. The implementation slice MUST update workflow skill defaults so they match the artifact registry.

R22. The implementation slice MUST update directly contradictory stage-skill placement text in the same slice.

R23. The implementation slice MUST NOT bulk-edit stage skills only for stylistic consistency.

R24. Directly contradictory stage-skill placement text MUST include plan-body placement text that claims `docs/changes/<change-id>/plan.md` is the canonical detailed plan-body path.

R25. Directly contradictory stage-skill placement text MUST include formal review placement text that conflicts with `docs/changes/<change-id>/reviews/<stage>-r<n>.md`.

R26. The workflow map source rank MUST be explicit and ordered as: explicit user path or change ID; active artifact metadata, active plan metadata, or active change metadata; approved specs or schemas; `docs/workflows.md` artifact registry for specified artifact types; stage-skill portable default; block on ambiguity.

R27. `docs/workflows.md` MUST state that explicit user paths and change IDs do not override higher-priority governance, safety, schema, security, or compatibility constraints.

R28. `docs/workflows.md` MUST state that it takes precedence over portable defaults only for artifact types it specifies.

R29. If `docs/workflows.md` is present but silent for an artifact type, stage skills MUST fall back to their portable default when the default is safe.

R30. If an artifact type is unknown to the workflow map and no safe portable default exists, the workflow skill and stage skills MUST block instead of inferring a path.

R31. Formal workflow-managed lifecycle recording MUST create or identify `docs/changes/<change-id>/` before recording change metadata, formal review records, review log, review resolution, explain-change, verify report, or change-local PR handoff evidence.

R31a. Formal workflow-managed lifecycle recording MUST NOT require the detailed plan body itself to live under `docs/changes/<change-id>/`.

R32. If a change ID is explicit or already present in active metadata, the workflow-managed stage MUST create or refresh the corresponding change pack before recording formal lifecycle evidence.

R33. If no change ID exists for formal workflow-managed recording, the stage MUST stop and request one or route to the stage that creates it.

R34. Isolated advisory review behavior MUST remain available and MUST NOT create lifecycle artifacts unless the user explicitly asks or formal recording is claimed.

R35. Formal review records MUST route under `docs/changes/<change-id>/reviews/`.

R36. Proposal-review records MUST use `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` unless a higher-priority explicit path, active metadata, approved spec, schema, or user instruction overrides it.

R37. Spec-review records MUST use `docs/changes/<change-id>/reviews/spec-review-r<n>.md` unless a higher-priority explicit path, active metadata, approved spec, schema, or user instruction overrides it.

R37a. Safe project-local customization for formal review records MAY customize filenames, review-type templates, or substructure under `docs/changes/<change-id>/reviews/`, but it MUST NOT route formal review records outside that directory unless a higher-priority source explicitly permits the outside path.

R38. Review logs MUST use `docs/changes/<change-id>/review-log.md` for workflow-managed formal reviews.

R39. Review resolution MUST use `docs/changes/<change-id>/review-resolution.md` only when material findings, blocking outcomes, accepted dispositions, or another governing review-resolution trigger require it.

R40. Learn sessions MUST NOT be treated as live artifact-placement authority.

R41. Learn sessions MAY be cited as historical rationale only when the current rule also exists in `docs/workflows.md`, an approved spec, a schema, or owning stage-skill guidance.

R42. Validation MUST detect drift between workflow skill default paths and the `docs/workflows.md` artifact registry.

R43. Validation MUST detect directly contradictory placement text between the artifact registry and first-slice affected stage skills.

R44. Validation MUST include the `workflow`, `plan`, `proposal-review`, and `spec-review` skills when their placement text is affected by the first slice.

R45. Validation MUST detect the stale plan-body placement conflict if the registry says `docs/changes/<change-id>/plan.md` while workflow or stage skill defaults say `docs/plans/YYYY-MM-DD-slug.md` for workflow-managed planned initiatives.

R46. Validation MUST detect when formal review records are routed outside `docs/changes/<change-id>/reviews/` without an allowed higher-priority customization.

R47. Validation MUST detect unknown artifact types in workflow-map validation input and report that placement is unresolved instead of deriving a path.

R48. If generated adapters include the workflow skill, adapter validation MUST prove that generated adapter output includes the updated workflow skill behavior.

R49. The first implementation slice MUST include a cold-read proof that answers where a proposal-review record goes, where a workflow-managed change plan goes, and what `docs/plan.md` is for.

R50. The change MUST NOT change lifecycle stage order.

R51. The change MUST NOT redefine proposal, spec, plan, review, verify, PR, or learn artifact content schemas.

R52. The change MUST NOT hand-edit generated public adapter output.

R53. The change MUST preserve customer-project portability by allowing stage-skill portable defaults when `docs/workflows.md` is absent or silent for an artifact type.

## Inputs and outputs

Inputs:

- Accepted proposal `docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md`.
- Existing workflow guide `docs/workflows.md`.
- Existing governance guidance `CONSTITUTION.md` and `AGENTS.md`.
- Canonical authored skill sources for `workflow`, `plan`, `proposal-review`, `spec-review`, and any directly contradictory stage skill.
- Related specs, especially `specs/installed-skill-artifact-placement-contract.md` and `specs/rigorloop-workflow.md`.
- Generated adapter output only through repository-owned generation and validation paths, not hand edits.

Outputs:

- Updated workflow skill behavior text.
- Updated `docs/workflows.md` with canonical YAML registry and synchronized Markdown tables.
- Updated `CONSTITUTION.md` and other affected guidance only if they are stale or inconsistent with the repository-standard `docs/plans/` plan-body contract.
- Updated directly contradictory stage-skill placement text.
- Validation checks or fixtures for registry shape, registry/table agreement, source-rank behavior, plan path drift, review path drift, unknown artifact blocking, and adapter packaging when relevant.
- Change-local evidence and cold-read proof for the implementation slice.

## State and invariants

- `docs/workflows.md` is the project-local artifact-location map.
- Stage skills own artifact content and portable defaults.
- The YAML registry is the machine-checkable placement source inside `docs/workflows.md`.
- Markdown tables are human-readable projections and must not contradict the YAML registry.
- `docs/plan.md` is the plan index.
- `docs/plans/YYYY-MM-DD-slug.md` is the detailed workflow-managed plan-body path.
- Existing `docs/plans/*.md` files remain canonical plan bodies and are not migrated.
- `docs/changes/<change-id>/` is the change-local evidence pack, not the plan-body directory.
- Formal workflow-managed review records live under `docs/changes/<change-id>/reviews/`.
- Learn sessions are history and rationale, not live routing authority.
- Lifecycle stage order remains unchanged.

## Error and boundary behavior

EC1. Missing `docs/workflows.md`: stage skills use explicit paths, active metadata, governing constraints, and portable defaults where safe; otherwise they block.

EC2. Partial `docs/workflows.md`: rows or registry entries that exist take precedence for their artifact type; omitted artifact types fall through to portable defaults when safe.

EC3. Registry/table mismatch: validation fails and identifies the artifact type and conflicting paths.

EC4. Duplicate canonical paths for one artifact type: validation fails.

EC5. Missing registry owner or required trigger: validation fails for that artifact type.

EC6. `docs/changes/<change-id>/plan.md` appears as the workflow-managed detailed plan-body canonical path after this spec is implemented: validation fails unless the text explicitly identifies it as a non-canonical example, rejected alternative, or historical reference.

EC7. Formal lifecycle recording lacks change ID: the stage blocks or routes to change ID creation before recording.

EC8. Explicit user path conflicts with schema, safety, security, or higher-priority governance: the stage blocks rather than using the path.

EC9. A generated adapter archive is stale after canonical workflow skill edits: adapter proof fails or records a blocker before installed-skill readiness is claimed.

EC10. A validator cannot parse the YAML registry: validation fails with a workflow-map parse diagnostic.

EC11. A learn session contradicts the artifact registry: the registry, approved spec, schema, or owning stage-skill guidance is authoritative; the learn session remains historical rationale only.

## Compatibility and migration

- Existing `docs/plans/*.md` files remain in place and are not migrated in this slice.
- Existing historical lifecycle artifacts remain valid unless a later migration proposal changes them.
- New workflow-managed detailed plan bodies use `docs/plans/YYYY-MM-DD-slug.md`.
- This spec aligns with `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and the installed-skill artifact placement contract instead of amending their `docs/plans/` plan-body rule.
- `docs/workflows.md`, workflow skill defaults, and directly contradictory stage-skill placement text must be updated together in the implementation slice to avoid split authority.
- Customer projects without `docs/workflows.md` remain supported through stage-skill portable defaults and clear blockers.
- Generated adapter output must be refreshed through repository-owned generation when packaged; generated public adapter bodies must not be hand-edited.
- Rollback must revert the workflow skill, `docs/workflows.md`, governance guidance, stage-skill placement edits, and validation expectations together.

## Observability

- `docs/workflows.md` exposes the YAML registry and Markdown tables to maintainers.
- Validation output reports registry parse failures, missing artifact fields, duplicate or conflicting placement representations, registry/table mismatches, workflow skill drift, directly contradictory stage-skill text, stale plan path text, formal review path drift, unknown artifact types, and stale generated adapter output when relevant.
- Change-local implementation evidence records cold-read answers for proposal-review placement, workflow-managed change plan placement, and `docs/plan.md` purpose.
- Review logs and review-resolution artifacts expose formal review outcomes for this change.

## Security and privacy

- The artifact registry must not require secrets, credentials, personal data, machine-local usernames, host-specific paths, or private filesystem details.
- Explicit user paths remain subordinate to security, privacy, schema, and governance constraints.
- The workflow map must not encourage writing artifacts outside the repository or into untracked machine-local locations.
- No new external service, credential, telemetry, or private data handling is introduced by this spec.

## Accessibility and UX

No UI is introduced. The human-readable Markdown tables in `docs/workflows.md` must remain understandable in plain Markdown and code review. The YAML registry must be colocated with the readable guide so maintainers do not need to inspect validator code to answer basic placement questions.

## Performance expectations

Validation for the artifact registry and placement drift should use bounded parsing of `docs/workflows.md` and directly relevant skill files. It should not require broad repository scans or generated output reads unless adapter proof is triggered by packaged workflow skill changes.

## Edge cases

EC12. `docs/workflows.md` contains a Markdown row for an artifact missing from YAML: validation fails.

EC13. `docs/workflows.md` contains a YAML artifact entry with no Markdown projection: validation fails unless the artifact type is explicitly marked machine-only with a documented reason.

EC14. A project customizes proposal paths in the registry: the custom path wins for proposals only when it does not conflict with higher-priority constraints.

EC14a. A project customizes formal review filenames under `docs/changes/<change-id>/reviews/`: the customization is valid when it remains change-local and does not conflict with higher-priority constraints.

EC14b. A project-local workflow map routes formal review records to `docs/reviews/`: validation fails unless a higher-priority explicit path, active metadata, approved spec, schema, or user instruction permits the outside-change-pack path.

EC15. A stage skill has no safe portable default and the workflow guide is absent: the stage blocks with a placement ambiguity message.

EC16. A review-only request does not claim formal lifecycle recording: the skill may answer without creating `docs/changes/<change-id>/`.

EC17. A clean formal review occurs: the review records the required receipt and review log without creating a new empty `review-resolution.md` solely for that clean review.

EC18. A material review finding occurs before a change pack exists: the stage creates or requests the change pack before claiming recorded status.

EC19. The workflow guide conflicts with an approved spec: the approved spec wins and the workflow guide is stale for that artifact until refreshed.

EC20. Adapter validation is not relevant because the workflow skill is not packaged in the slice: the plan or change evidence records adapter proof as not applicable with rationale.

## Non-goals

- Do not change lifecycle stage order.
- Do not redefine artifact content schemas for proposals, specs, test specs, plans, reviews, verify reports, PR handoff, or learn records.
- Do not migrate existing `docs/plans/*.md` files in this slice.
- Do not introduce a new CLI scaffold for change pack creation.
- Do not remove stage-skill portable defaults.
- Do not make `docs/workflows.md` override explicit user paths, active metadata, approved specs, schemas, safety constraints, or security constraints.
- Do not treat learn sessions as live routing authority.
- Do not hand-edit generated adapter output.
- Do not bulk-edit stage skills for wording style alone.

## Acceptance criteria

AC1. The workflow skill states that it creates or refreshes `docs/workflows.md`.

AC2. `docs/workflows.md` states that it is the project-local artifact-location map.

AC3. `docs/workflows.md` contains a canonical fenced YAML registry with `artifact_locations`.

AC4. `docs/workflows.md` contains synchronized human-readable Markdown artifact-location tables.

AC5. Validation fails when a Markdown table path contradicts the YAML registry path.

AC6. Each required artifact type has exactly one canonical placement representation in the registry.

AC7. `docs/plan.md` is documented only as the plan index.

AC8. New workflow-managed detailed plan bodies are documented under `docs/plans/YYYY-MM-DD-slug.md`.

AC9. Existing `docs/plans/*.md` files are not migrated by the first slice and remain valid plan bodies.

AC10. The spec and implementation preserve the repository-standard `docs/plans/` plan-body contract in `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and the `plan` skill.

AC11. Formal review records are documented under `docs/changes/<change-id>/reviews/`.

AC12. Unknown artifact types block rather than infer a path.

AC13. Customer projects without `docs/workflows.md` can still use stage-skill portable defaults or get a clear blocker.

AC14. Workflow skill defaults match the artifact registry.

AC15. Directly contradictory first-slice stage-skill placement text is updated.

AC16. Validation detects workflow skill, `docs/workflows.md`, stage-skill, and generated adapter drift when those surfaces are in scope.

AC17. Cold-read proof answers where a proposal-review record goes, where a workflow-managed change plan goes, and what `docs/plan.md` is for.

AC18. No lifecycle order, artifact content schema, or downstream readiness claim changes.

AC19. PR handoff has a deterministic registry representation through `path`, `external_surface`, or `policy`.

AC20. Project-local formal review customization remains under `docs/changes/<change-id>/reviews/` unless a higher-priority source explicitly permits another path.

## Open questions

None.

## Next artifacts

```text
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Spec review R2: [spec-review-r2](../docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md)
- Plan: [Workflow Skill Artifact-Location Map Plan](../docs/plans/2026-06-18-workflow-skill-artifact-location-map.md)
- Test spec: [Workflow Skill Artifact-Location Map Test Spec](workflow-skill-artifact-location-map.test.md)

## Readiness

Approved by spec-review R2 and ready for execution planning.
