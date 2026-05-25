# Installed-Skill Artifact Placement Contract

## Status

approved

## Related proposal

- Proposal: [Installed-Skill Artifact Placement Contract](../docs/proposals/2026-05-25-installed-skill-artifact-placement-contract.md)
- Proposal review: [proposal-review-r2](../docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/proposal-review-r2.md)

## Goal and context

Installed RigorLoop skills are used outside the RigorLoop repository. A skill-only adopter may have the installed skill bodies but not this repository's `docs/workflows.md`, `CONSTITUTION.md`, or other repo-local guidance. The installed skill therefore needs enough artifact-placement contract text for a user to answer where the stage-owned artifact or formal review record goes.

This spec defines the portable placement contract that public stage skills must expose, the lookup precedence between explicit paths, project-local workflow maps, and portable defaults, the formal lifecycle review locality rule for early reviews, and the validation behavior that prevents drift between skill-stated defaults and `docs/workflows.md`.

This spec does not redefine exact review-record schemas, review-finding semantics, disposition semantics, or lifecycle stage order. Those remain owned by the existing formal review, workflow, schema, and validator contracts.

## Glossary

- `installed skill`: A shipped skill body available to a user outside the RigorLoop repository.
- `skill-only adopter`: A user or project that has installed skills but does not necessarily have RigorLoop repository-local docs.
- `portable default`: A default artifact path stated in a skill body and usable when no project-local placement map resolves the artifact.
- `project workflow guide`: A project-local `docs/workflows.md` artifact-location map, or equivalent explicit project-local workflow map when supported by the project.
- `change pack`: The change-local evidence root at `docs/changes/<change-id>/`.
- `formal lifecycle review`: A supported lifecycle review invocation that claims formal review evidence, such as `proposal-review`, `spec-review`, `plan-review`, `architecture-review`, or `code-review`.
- `isolated advisory review`: A direct review-like request that does not claim formal lifecycle recording or downstream workflow completion.
- `plan index`: The lifecycle index at `docs/plan.md`.
- `plan body`: The concrete execution plan at `docs/plans/YYYY-MM-DD-slug.md`.
- `workflow map`: The artifact-location and workflow summary at `docs/workflows.md`.

## Examples first

Example E1: skill-only adopter asks where a proposal-review record goes
Given an adopter has only the installed `proposal-review` skill
When the adopter reads the skill's artifact-placement section
Then the skill states that formal proposal-review records default to `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`
And the skill states that formal recording requires a change pack before claiming `Recording status: recorded`.

Example E2: formal spec-review starts before a change pack exists
Given a workflow-managed formal `spec-review` is requested
And no `docs/changes/<change-id>/` exists or is identified
When the review stage needs to record the review result
Then the stage creates or requests creation of the change pack before claiming recorded status
And the review record defaults to `docs/changes/<change-id>/reviews/spec-review-r<n>.md`
And a clean review records a review receipt and `review-log.md` without creating an empty `review-resolution.md`.

Example E3: partial project workflow guide
Given a project has `docs/workflows.md`
And the guide specifies proposal placement but does not specify spec-review record placement
When `spec-review` resolves where to record formal review evidence
Then the workflow guide takes precedence only for artifacts it specifies
And the skill's portable default fills the omitted spec-review placement.

Example E4: plan wording in an installed skill
Given a skill tells a user to update lifecycle state
When the state belongs to the active plan index
Then the skill names `docs/plan.md`
And when the instruction concerns concrete milestone progress
Then the skill names the active plan body under `docs/plans/YYYY-MM-DD-slug.md`.

## Requirements

R1. Public artifact-producing and review-producing skills MUST include an `Artifact placement` section or equivalent clearly labeled placement block.

R2. Each placement block MUST state the artifact or record type owned by the skill and the portable default path for that artifact or record type.

R3. Public review skills that produce formal lifecycle review evidence MUST state the default formal review record path under `docs/changes/<change-id>/reviews/`.

R4. `proposal-review` MUST state the default formal review record path `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`.

R5. `spec-review` MUST state the default formal review record path `docs/changes/<change-id>/reviews/spec-review-r<n>.md`.

R6. Public review skills that produce formal lifecycle review evidence MUST state that `docs/changes/<change-id>/review-log.md` is the default review log location.

R7. Public review skills that produce formal lifecycle review evidence MUST state that `docs/changes/<change-id>/review-resolution.md` is used only when material findings, blocking outcomes, accepted dispositions, or another governing review-resolution trigger require it.

R8. Formal lifecycle review skills MUST state that they create or request a change pack before claiming `Recording status: recorded` when no change pack exists or is identified.

R9. Formal lifecycle review locality MUST apply to clean formal reviews and material-finding reviews. The default location MUST NOT depend on whether the review result has material findings.

R10. Clean formal review guidance MUST preserve the existing rule that a clean receipt and `review-log.md` are recorded without creating an empty `review-resolution.md`.

R11. Isolated advisory review guidance MUST remain available. Skills MUST NOT require a change pack for review-like requests that do not claim formal lifecycle recording unless the user explicitly requests an artifact.

R12. Workflow-managed proposal authoring MUST create or identify the change pack when it is the first formal lifecycle entry for a non-trivial change.

R13. Review skills MUST treat change-pack creation during review as a fallback for formal review requests where proposal authoring did not create or identify the pack.

R14. Artifact placement lookup MUST use this precedence when sources conflict: explicit user path or change ID; active artifact, plan, or change metadata; governing spec or schema constraints; project workflow guide for the artifact it specifies; skill portable default; block on ambiguity.

R15. A project workflow guide MUST take precedence over a portable default only for artifact types it specifies. A present but partial workflow guide MUST NOT suppress portable defaults for omitted artifact types.

R16. An explicit user path or change ID MUST NOT override higher-priority governance, safety, schema, or security constraints.

R17. Skills MUST block instead of guessing when placement remains ambiguous after the lookup sequence or when a governing spec or schema forbids the resolved path.

R18. Skills that mention plan-related surfaces MUST distinguish the workflow map `docs/workflows.md`, the plan index `docs/plan.md`, the plan body `docs/plans/YYYY-MM-DD-slug.md`, change metadata `docs/changes/<change-id>/change.yaml`, and change-local evidence under `docs/changes/<change-id>/`.

R19. Skills MUST NOT use ambiguous instructions such as "update the plan" when the required surface can be named more precisely.

R20. `docs/workflows.md` MUST remain a project-local artifact-location map and customization surface. It MUST NOT be the only source of portable placement rules for installed-skill users.

R21. `docs/workflows.md` MUST summarize the same portable defaults required by this spec for the updated first-slice skills.

R22. Public skill text MUST avoid requiring RigorLoop repository-internal docs, scripts, reports, generated mirrors, adapter paths, or maintainer-only implementation mechanics to answer basic artifact-placement questions.

R23. Skills MUST state placement and recording boundaries without duplicating full review-record schemas, lifecycle validator field rules, or disposition semantics.

R24. The first implementation slice MUST update `proposal-review` and `spec-review` placement guidance and plan-surface wording needed to resolve the observed adopter gap.

R25. The first implementation slice MUST keep bulk historical artifact migration, CLI scaffolding for new changes, generated shared partials, and review schema redesign out of scope.

R26. `validate-skills.py` or the skill-validation module it invokes MUST include deterministic checks that updated public skills state the required review-record paths, pre-change-pack behavior, and plan-surface distinctions.

R27. The first drift check MUST be owned by skill validation. Artifact lifecycle validation MUST NOT duplicate the same skill/workflow placement drift check in the first slice.

R28. Validation MUST detect a mismatch between updated skill-stated placement defaults and the matching `docs/workflows.md` artifact-location rows.

R29. Generated skill or adapter validation MUST prove that installable skill output includes the revised skill bodies when canonical public skill files change.

R30. The implementation proof MUST include a cold-read check or equivalent fixture showing that installed-skill text alone answers where a proposal-review record goes, where a spec-review record goes before a change pack exists, and which plan surface should be updated.

## Inputs and outputs

Inputs:

- Canonical public skill source under `skills/`.
- Project-local workflow map at `docs/workflows.md`.
- Existing review-recording, workflow, and skill-structure specs.
- Change metadata and review logs under `docs/changes/<change-id>/` when workflow-managed recording is active.
- Explicit user paths, change IDs, or active artifact metadata when provided.

Outputs:

- Updated public skill bodies that include concise placement contracts.
- Updated `docs/workflows.md` rows that remain synchronized with skill-stated defaults.
- Skill-validation checks or fixtures that detect missing placement text and skill/workflow placement drift.
- Generated installable skill or adapter output that contains the revised skill text.
- Change-local evidence for reviews and implementation proof when the workflow requires it.

## State and invariants

- Installed skills remain the portable user-facing contract for stage-owned artifact placement.
- `docs/workflows.md` remains the project-local map and customization layer, not the only placement contract.
- Exact artifact schemas and review-resolution semantics remain owned by their existing specs, schemas, and validators.
- Formal lifecycle evidence has a change-local home under `docs/changes/<change-id>/` from the first recorded stage.
- Isolated advisory use remains possible without forced lifecycle artifact creation.
- Canonical authored skill source remains under `skills/`; generated public adapter output is not hand-edited.

## Error and boundary behavior

- If a formal lifecycle review cannot determine or create a valid change pack, the review MUST report `Recording status: blocked` and identify the missing placement decision.
- If a user provides a path that conflicts with a governing spec, schema, security rule, or safety constraint, the skill MUST reject or block on that path rather than silently using it.
- If `docs/workflows.md` conflicts with a higher-priority explicit path, active metadata, spec, schema, or safety constraint, the higher-priority source wins and the workflow guide is treated as stale for that artifact.
- If `docs/workflows.md` is present but silent for an artifact, skills MUST fall through to the portable default when the default is safe.
- If generated installable skill output cannot be validated, the change MUST NOT claim that installed skills contain the revised placement contract.

## Compatibility and migration

- Existing project-local workflow maps remain valid customization surfaces.
- Existing historical review records do not need to be moved in the first slice.
- Existing isolated advisory review behavior remains valid when no formal lifecycle recording is claimed.
- Existing review-record schemas, severity semantics, disposition values, and review-status values remain unchanged.
- Existing generated public adapter output must be regenerated or validated from canonical `skills/` when canonical public skill text changes; generated output must not be hand-edited.
- Existing projects with partial workflow guides gain fallback behavior to portable defaults for omitted artifact types.

## Observability

- `docs/workflows.md` exposes the project-local artifact-location map for contributors.
- Skill-validation output reports missing placement strings, missing pre-change-pack behavior, missing plan-surface distinctions, and skill/workflow placement mismatches.
- Change-local review logs expose recorded formal reviews and receipt paths.
- Generated adapter validation output reports whether installable skill bodies include the revised canonical text.
- Cold-read proof records whether installed-skill text alone answers the targeted placement questions.

## Security and privacy

- Placement guidance MUST NOT require secrets, credentials, host-specific paths, or private repository internals.
- Public skill text MUST NOT expose maintainer-only generated-output paths, local `.codex/skills/` state, release archive internals, or repository-private implementation details as required adopter knowledge.
- Explicit user paths remain subject to governance, schema, safety, and security constraints.

## Accessibility and UX

No UI behavior is in scope. User-facing skill text should be concise, clearly headed, and readable in plain Markdown. The placement answer should be findable from the relevant skill without scanning unrelated repository docs.

## Performance expectations

Validation checks should be deterministic text or fixture checks suitable for normal skill validation. The first slice does not require broad semantic proof or expensive repository-wide searches to prove placement wording.

## Edge cases

EC1. A formal review is requested without a change ID: the skill creates or requests a valid change ID and change pack before recording, or blocks without claiming recorded status.

EC2. A project workflow guide exists but omits spec-review placement: `spec-review` uses its portable default.

EC3. A project workflow guide specifies a custom review-record path: the custom path wins only when it does not conflict with higher-priority constraints.

EC4. A clean formal review occurs before any material finding exists: the review records a clean receipt and review log entry, and omits empty `review-resolution.md`.

EC5. An isolated advisory review is requested in chat only: the skill may answer without creating lifecycle artifacts and must not claim formal lifecycle recording.

EC6. A generated adapter archive is stale after canonical skill edits: generated-output validation fails or the plan records an explicit blocker; the change cannot claim installed-skill readiness.

EC7. A skill says "plan" without naming a surface: validation or review treats the wording as ambiguous when the intended surface can be known.

EC8. A user-provided path points outside allowed project artifacts or conflicts with a schema: the skill blocks rather than using the unsafe path.

## Non-goals

- Redefining review finding severity, review status, disposition, or closeout semantics.
- Rewriting review-record schemas or lifecycle validator field contracts.
- Changing lifecycle stage order.
- Bulk migrating historical artifacts.
- Adding CLI scaffolding for change-pack creation.
- Adding build-time shared partials for placement wording.
- Making `docs/workflows.md` irrelevant.
- Requiring adopter projects to copy the full RigorLoop repository docs.

## Acceptance criteria

AC1. `proposal-review` states `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` as the default formal review record path.

AC2. `spec-review` states `docs/changes/<change-id>/reviews/spec-review-r<n>.md` as the default formal review record path.

AC3. Updated review skills state that formal lifecycle recording requires a change pack before claiming `Recording status: recorded`.

AC4. Updated review skills preserve isolated advisory review behavior without forced lifecycle artifact creation.

AC5. Updated skill wording states that clean formal reviews record receipts and `review-log.md` without creating empty `review-resolution.md`.

AC6. `docs/workflows.md` matches the updated skill-stated defaults for first-slice placement rows.

AC7. Skill validation detects missing review-record path wording, missing pre-change-pack behavior, and skill/workflow placement mismatch for the first-slice skills.

AC8. Plan-related skill wording distinguishes `docs/workflows.md`, `docs/plan.md`, `docs/plans/YYYY-MM-DD-slug.md`, and `docs/changes/<change-id>/change.yaml` where those surfaces are relevant.

AC9. A cold-read proof from installed skill text alone answers where proposal-review records go, where spec-review records go before a change pack exists, and which plan surface should be updated.

AC10. Generated installable skill or adapter validation confirms the revised canonical skill text is present in generated output.

AC11. Exact review-record field schemas remain owned outside the placement wording and are not duplicated in the updated skills.

AC12. Explicit user paths and valid project-local workflow-map customizations continue to override portable defaults where safe.

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

- Plan: [Installed-Skill Artifact Placement Contract Plan](../docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md)
- Test spec: [Installed-Skill Artifact Placement Contract Test Spec](installed-skill-artifact-placement-contract.test.md)

## Readiness

Approved and ready for `plan`.
