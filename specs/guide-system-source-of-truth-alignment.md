# Guide System Source-of-Truth Alignment

## Status

approved

## Related proposal

- Proposal: [RigorLoop Guide System Optimization and Source-of-Truth Alignment](../docs/proposals/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment.md)
- Proposal review: [proposal-review-r1](../docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/proposal-review-r1.md)
- Related workflow-map spec: [Workflow Skill Artifact-Location Map](workflow-skill-artifact-location-map.md)
- Related workflow spec: [RigorLoop Workflow](rigorloop-workflow.md)
- Related skill spec: [Skill Contract](skill-contract.md)

## Goal and context

RigorLoop has several guide-like surfaces that answer different contributor and adopter questions. This spec defines the observable contract that keeps those guides source-ranked, focused, portable, and testable.

The guide system must make common routing questions answerable without chat history or learn-session archaeology:

- Where do I start?
- Which guide is authoritative?
- Where does this artifact go?
- Which skill owns this artifact?
- Which file tells me current work state?
- Which guide applies in a customer project?

This spec owns guide taxonomy, guide ownership, source-of-truth alignment, guide-index behavior, cross-guide validation ownership, baseline drift treatment, and cold-read proof expectations. It does not replace the workflow-map spec's exact artifact-location registry contract.

## Glossary

- `artifact-location map`: the project-local artifact placement contract in `docs/workflows.md`, owned by the workflow-map contract.
- `baseline drift`: a known pre-existing inconsistency recorded as not migrated in the first guide-system slice.
- `change pack`: `docs/changes/<change-id>/`, the change-local evidence root.
- `cross-guide check`: validation that compares multiple guide surfaces, such as README links, workflow guide sections, project-map scope, plan-index boundaries, learn-session authority, or guide/source-of-truth drift.
- `guide ownership matrix`: a table that names which guide answers which question and which skill or artifact owns the answer.
- `guide system`: the set of RigorLoop orientation, governance, workflow, repository-map, plan-index, change-local, learn, skill, release, and package guide surfaces.
- `landing guide`: a first-contact orientation guide, especially `README.md`.
- `live routing authority`: current guidance that future work may rely on for artifact routing or workflow behavior.
- `portable default`: stage-skill placement or behavior guidance used when a project-local workflow guide is absent or silent.
- `stage skill`: an installed skill that owns one workflow stage's operating contract.
- `workflow guide`: `docs/workflows.md`.

## Examples first

Example E1: new contributor chooses the right guide
Given a contributor opens `README.md`
When they need to know where workflow artifacts go
Then README points them to `docs/workflows.md`
And README does not duplicate the full artifact-location contract.

Example E2: workflow guide owns guide routing
Given a contributor asks which guide owns current work state
When they read the guide ownership matrix in `docs/workflows.md`
Then it identifies `docs/plan.md` as the live work index
And it does not describe `docs/project-map.md` as the active work-state owner.

Example E3: project-map stays an orientation surface
Given a contributor reads `docs/project-map.md`
When they need repository structure, important components, validation surfaces, and boundaries
Then the project map answers those orientation questions
And it does not define lifecycle stage order or artifact placement policy.

Example E4: plan index stays bounded
Given `docs/plan.md` is updated during lifecycle work
When the update records active, blocked, superseded, or recent done work
Then it remains a bounded index
And detailed milestone journals remain in the canonical plan body location defined by the workflow-map contract.

Example E5: learn session produces a routing lesson
Given a learn session discovers that a review artifact was routed incorrectly
When the lesson changes future routing behavior
Then the live rule is promoted to `docs/workflows.md`, an approved spec, a schema, or owning stage-skill guidance
And the learn session remains historical rationale only.

Example E6: customer project lacks `docs/workflows.md`
Given a customer project has installed stage skills but no project-local workflow guide
When a stage skill needs an artifact path
Then it uses explicit user input, active metadata, governing local constraints, and portable defaults where safe
And it blocks if placement remains ambiguous.

Example E7: guide drift validation
Given README links to `docs/workflows.md`
When the target file is renamed, deleted, or no longer contains the required guide ownership section
Then guide-system validation fails with a guide-check failure.

Example E8: baseline drift
Given a historical artifact uses an older placement convention
When the first guide-system slice runs
Then the artifact is not moved automatically
And any migration requires separate approval with preservation and rollback proof.

## Requirements

R1. The guide system MUST classify major guide surfaces by purpose, including README, `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, `docs/changes/<change-id>/`, `docs/learn/sessions/`, `skills/*/SKILL.md`, release docs, and package guide surfaces.

R2. `README.md` MUST operate as a landing guide for first-contact orientation.

R3. `README.md` MUST include a compact guide index or equivalent "where to go next" section.

R4. `README.md` MUST link to `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, and stage-skill usage guidance when those surfaces exist.

R5. `README.md` MUST NOT duplicate the full workflow contract, full artifact-location contract, full artifact schema contract, or full stage-skill operating instructions.

R6. `VISION.md` MUST remain the canonical project-vision artifact subordinate to `CONSTITUTION.md`.

R7. `CONSTITUTION.md` MUST remain the repository governance and source-of-truth policy surface.

R8. `docs/workflows.md` MUST identify itself as the project-local workflow guide and artifact-location map.

R9. `docs/workflows.md` MUST include guide ownership or source-rank guidance that tells users which guide answers common questions.

R10. `docs/workflows.md` MUST include a guide ownership matrix or equivalent guide index for guide-system routing.

R11. The guide ownership matrix MUST identify the primary guide for project vision, governance, artifact placement, repository structure, active work, one-change evidence, stage execution, and historical rationale.

R12. `docs/workflows.md` MUST distinguish guide ownership from stage-skill artifact-content ownership.

R13. Exact artifact-location registry semantics MUST remain owned by `specs/workflow-skill-artifact-location-map.md` or its approved successor.

R14. When drift validation is in scope, `docs/workflows.md` MUST include a canonical machine-checkable artifact registry and human-readable Markdown projections as required by the workflow-map contract.

R15. Guide-system work MUST NOT introduce a second canonical artifact-location registry outside the workflow guide unless a later accepted proposal changes the guide architecture.

R16. `docs/project-map.md` MUST remain a repository orientation map.

R17. `docs/project-map.md` MUST NOT own workflow stage order, exact lifecycle artifact placement, or current milestone state.

R18. `docs/project-map.md` SHOULD identify major directories, important components, runtime boundaries, generated artifacts, validation surfaces, external boundaries, and known orientation risks when those areas are relevant and current.

R19. `docs/plan.md` MUST remain a bounded live-work index for active, blocked, superseded, and recent done work.

R20. `docs/plan.md` MUST NOT contain full milestone journals, long review summaries, complete historical transcripts, or detailed implementation plans.

R21. Detailed workflow-managed plan-body placement MUST align with the approved workflow-map contract.

R22. The guide system MUST NOT leave `docs/plans/*.md` and `docs/changes/<change-id>/plan.md` as competing canonical locations for the same workflow-managed plan role.

R23. Under the currently approved workflow-map contract, guide-system updates MUST treat `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body path for workflow-managed planned initiatives.

R24. Under the currently approved workflow-map contract, guide-system updates MUST treat `docs/plan.md` as the plan index only.

R25. Learn sessions MUST NOT be treated as live routing authority.

R26. If a learn session changes future artifact routing, workflow behavior, or guide ownership, the live rule MUST be promoted to `docs/workflows.md`, an approved spec, a schema, or owning stage-skill guidance.

R27. Stage skills MUST remain self-contained enough for skill-only adopters.

R28. Stage skills MUST retain portable defaults for customer projects that do not have `docs/workflows.md`.

R29. Stage skills MUST use project-local workflow guidance when present and relevant, then portable defaults where safe, and block when placement remains ambiguous.

R30. First-slice stage-skill edits MUST be limited to text that directly contradicts the approved workflow guide, source-rank model, or artifact-location registry.

R31. First-slice work MUST NOT bulk-edit lifecycle skills for style, symmetry, or wording cleanup alone.

R32. Cross-guide validation MUST be owned by a dedicated guide-system validator or an artifact-lifecycle guide-system mode.

R33. `validate-skills.py` MUST remain scoped to skill-file checks unless a check directly inspects packaged skill content.

R34. Cross-guide validation MUST NOT place README, project-map, plan-index, learn-session, or constitution checks in `validate-skills.py` unless those checks directly concern packaged skill content.

R35. Guide-system validation MUST check that README links to required primary guides when those guides exist.

R36. Guide-system validation MUST check that `docs/workflows.md` includes guide ownership and artifact-location sections when drift validation is in scope.

R37. Guide-system validation MUST check that `docs/workflows.md` distinguishes guide ownership from stage-skill content ownership.

R38. Guide-system validation MUST check that `docs/project-map.md` does not claim ownership of workflow stage order.

R39. Guide-system validation MUST check that `docs/plan.md` remains a bounded index.

R40. Guide-system validation MUST check that learn sessions are not cited as live routing authority without promotion to an owning live surface.

R41. Guide-system validation MUST check directly affected stage-skill placement text for contradiction with the approved workflow map.

R42. Guide-system validation MUST preserve the workflow-map validator's canonical-registry/table consistency checks rather than duplicating them as a second contract.

R43. Generated adapter validation MUST prove updated skill guide content is packaged when canonical changed skills affect generated adapters.

R44. Existing guide inconsistencies MUST be recorded as baseline drift instead of automatically migrated in the first guide-system slice.

R45. Historical artifact or guide migration MUST require separate approval unless an accepted plan for this change explicitly includes migration with preservation and rollback proof.

R46. Guide-system changes MUST NOT change lifecycle stage order.

R47. Guide-system changes MUST NOT change artifact content schemas.

R48. Guide-system changes MUST NOT change validation command semantics, selected-check behavior, command exit behavior, or required validation evidence except through approved validator contracts.

R49. Guide-system changes MUST NOT hand-edit generated public adapter output.

R50. The first implementation slice MUST include behavior-preservation proof for README, `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, stage skills, and learn sessions.

R51. The first implementation slice MUST include cold-read proof showing that a reviewer can answer common guide-routing questions without prior chat context.

R52. The spec-review and later validation flow MUST treat stale touched, referenced, generated, or authoritative guide artifacts as blocking when they contradict this spec or a higher-priority source.

## Inputs and outputs

Inputs:

- Accepted proposal `docs/proposals/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment.md`.
- Proposal-review evidence under `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/`.
- `CONSTITUTION.md`, `VISION.md`, `README.md`, `docs/workflows.md`, `docs/project-map.md`, and `docs/plan.md`.
- Canonical skill sources under `skills/` when their placement or guide-source wording is directly affected.
- Related specs, especially `specs/workflow-skill-artifact-location-map.md`, `specs/rigorloop-workflow.md`, and `specs/skill-contract.md`.
- Repository-owned validation scripts and adapter generation/validation when implementation changes validators or canonical skills.

Outputs:

- This spec.
- Updated guide surfaces in the first implementation slice.
- Directly necessary canonical skill wording updates.
- Guide-system validation checks or an artifact-lifecycle guide-system mode.
- Change-local behavior-preservation and cold-read proof.
- Generated adapter proof when changed canonical skill content is packaged.

## State and invariants

- `CONSTITUTION.md` remains the highest-priority repository governance source below external runtime instructions.
- `VISION.md` remains the canonical vision artifact subordinate to `CONSTITUTION.md`.
- `docs/workflows.md` remains the project-local workflow guide and artifact-location map.
- The workflow-map spec owns exact artifact-location registry semantics.
- `docs/project-map.md` orients to repository structure and boundaries.
- `docs/plan.md` indexes live work state.
- Stage skills own stage behavior and portable defaults.
- Learn sessions record historical rationale, not live routing authority.
- Baseline drift does not imply automatic migration.

## Error and boundary behavior

EC1. Missing guide surface: README or `docs/workflows.md` may omit links to absent optional guides, but it must not claim an absent guide is available.

EC2. Stale guide link: guide validation fails when a required guide index link targets a missing file.

EC3. Guide ownership conflict: when README, `docs/workflows.md`, `docs/project-map.md`, or `docs/plan.md` claim conflicting ownership for the same question, the higher-priority source wins and validation must report the lower-priority drift when the touched area is in scope.

EC4. Workflow-map conflict: when guide-system wording conflicts with the approved workflow-map spec on exact artifact placement, the workflow-map spec wins and guide-system wording must be revised.

EC5. Stage-skill conflict: when affected stage-skill placement text contradicts the approved workflow map, the first implementation slice must update the directly contradictory text or explicitly record why the skill is unaffected.

EC6. Learn-only rule: if a live routing rule exists only in a learn session, downstream workflow reliance is blocked until the rule is promoted to an owning live guide or contract.

EC7. Historical artifact drift: historical artifacts that do not match the new guide system are not moved or rewritten unless a separate migration artifact approves that work.

EC8. Validator overreach: if a proposed guide check would require broad natural-language scoring or fragile prose matching, the implementation must narrow the check to stable headings, links, paths, check IDs, or explicitly reviewed fixture text.

## Compatibility and migration

This spec is compatibility-sensitive because it affects contributor-visible workflow and source-of-truth guidance.

The first implementation slice must preserve:

- lifecycle stage order;
- artifact schemas;
- the approved workflow-map contract for exact artifact placement;
- customer-project portability through stage-skill defaults;
- historical artifacts in place;
- generated adapter reproducibility from canonical sources.

Existing guide inconsistencies are baseline drift unless the implementation slice touches and relies on the inconsistent surface. Migration of historical artifacts or guide families is out of scope without separate approval.

Rollback is guide-text and validator-scoped: revert guide wording or guide checks that create source-of-truth confusion, while leaving historical artifacts unmoved.

## Observability

Observable proof surfaces include:

- guide-system validator output or artifact-lifecycle guide-system mode output;
- selected CI output for touched guide, skill, validator, adapter, and change-local paths;
- behavior-preservation proof under `docs/changes/<change-id>/`;
- cold-read proof under `docs/changes/<change-id>/`;
- review records and review-log entries for formal review stages.

Validation output must name failed guide checks with stable IDs where practical.

## Security and privacy

The guide system must not require secrets, credentials, private tokens, usernames, machine-local paths, or private environment details.

Guide validation must not require network access or hosted service state for ordinary guide checks.

Stage-skill portability wording must not instruct customer projects to depend on RigorLoop repository-internal paths unless those paths are explicitly project-local in that customer repository or packaged with the installed skill.

## Accessibility and UX

No application UI is changed.

Guide UX requirements:

- README guide navigation must be concise enough for first-contact users.
- `docs/workflows.md` guide ownership content must be scannable as a matrix, table, or equivalent compact structure.
- Dense guide details should remain in the owning guide or spec rather than being duplicated in README.

## Performance expectations

Guide-system validation should run inside the repository's selected explicit CI flow for touched guide surfaces.

Cross-guide checks should prefer deterministic parsing of links, headings, fenced YAML, tables, stable check IDs, and fixture text over broad natural-language scans.

The first implementation slice must not require broad smoke solely because README, guide text, or proposal/spec artifacts changed, unless another authoritative trigger requires it.

## Edge cases

EC1. README links to a guide that exists but is stale: validation may pass link integrity but spec-review or verify must still report authoritative stale drift when the stale guide is touched, referenced, generated, or authoritative for the change.

EC2. A customer project has stage skills but no `docs/workflows.md`: stage skills use portable defaults and block on ambiguity.

EC3. `docs/workflows.md` has artifact-location registry entries but no guide ownership matrix: guide-system validation fails once this spec is in force for the touched workflow guide.

EC4. `docs/project-map.md` mentions workflow surfaces for orientation: valid, provided it does not own lifecycle order or artifact placement policy.

EC5. `docs/plan.md` links to plan bodies: valid, provided it remains a bounded index and does not become the detailed plan journal.

EC6. A learn session includes historical routing rationale: valid, provided the live rule is promoted before downstream reliance.

EC7. A stage skill and `docs/workflows.md` use different wording but the same path and source-rank behavior: not a contradiction by itself.

EC8. A stage skill omits a project-local customization mentioned in `docs/workflows.md`: not a contradiction if the skill's portable default remains safe and the source-rank behavior says the project-local workflow guide wins for specified artifact types.

## Non-goals

- Do not rewrite every guide in one slice.
- Do not create `docs/guides.md` in the first slice.
- Do not change lifecycle stage order.
- Do not change artifact content schemas.
- Do not change exact artifact-location registry semantics outside the workflow-map contract.
- Do not make README the authoritative workflow manual.
- Do not make `docs/workflows.md` the only source for skill-only adopters.
- Do not treat learn sessions as live routing authority.
- Do not migrate historical artifacts in the first slice.
- Do not add a new CLI scaffold.
- Do not hand-edit generated adapter output.
- Do not bulk-edit stage skills for style or symmetry.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-GUIDE-SPEC-001 | The spec defines each major guide surface and its ownership boundary. |
| AC-GUIDE-SPEC-002 | README requirements keep README as a landing guide with a compact guide index. |
| AC-GUIDE-SPEC-003 | `docs/workflows.md` requirements identify it as the project-local workflow guide and artifact-location map. |
| AC-GUIDE-SPEC-004 | `docs/workflows.md` requirements include guide ownership or source-rank guidance. |
| AC-GUIDE-SPEC-005 | `docs/project-map.md` requirements scope it to repository orientation, not workflow policy. |
| AC-GUIDE-SPEC-006 | `docs/plan.md` requirements preserve it as a bounded live work index. |
| AC-GUIDE-SPEC-007 | Learn-session requirements prevent learn sessions from becoming live routing authority. |
| AC-GUIDE-SPEC-008 | Stage-skill requirements preserve portable defaults for skill-only adopters. |
| AC-GUIDE-SPEC-009 | Validation ownership requirements keep non-skill cross-guide checks out of `validate-skills.py`. |
| AC-GUIDE-SPEC-010 | The spec aligns plan-body placement with the approved workflow-map contract and does not introduce competing canonical plan locations. |
| AC-GUIDE-SPEC-011 | Baseline drift requirements prevent automatic historical migration in the first slice. |
| AC-GUIDE-SPEC-012 | Behavior-preservation and cold-read proof are required for the first implementation slice. |
| AC-GUIDE-SPEC-013 | The spec preserves lifecycle order, artifact schemas, validation semantics, and generated-output rules. |

## Open questions

None.

The exact implementation form of the guide-system validator may be either a dedicated script or an artifact-lifecycle guide-system mode, provided it satisfies this spec's ownership boundaries.

## Next artifacts

- implement
- code-review
- explain-change
- verify
- pr

## Follow-on artifacts

- Spec review R1: `../docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/spec-review-r1.md`
- Spec review R2: `../docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/spec-review-r2.md`
- Plan: `../docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md`
- Plan review R1: `../docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/plan-review-r1.md`
- Test spec: `guide-system-source-of-truth-alignment.test.md`

## Readiness

Approved after spec-review. Planning and test-spec follow-on artifacts are recorded. Current downstream handoff: `implement M1`.
