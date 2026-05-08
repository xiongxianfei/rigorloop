# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-08-skill-contract-optimization.md
Status: revise

## Review inputs

- Proposal: `docs/proposals/2026-05-08-skill-contract-optimization.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Learn evidence: `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`, `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`

## Findings

### SCO1 - First implementation slice is still not settled

Finding ID: SCO1
Severity: major
Evidence: The rollout names `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn` as first-phase skills, while the open questions still ask which skills should be normalized in the first accepted implementation slice.
Required outcome: Choose the first implementation slice in the proposal.
Safe resolution: Add a `First implementation slice` section listing the seven canonical skill files in scope and remove the open question asking which skills are first.

### SCO2 - Normative source is ambiguous

Finding ID: SCO2
Severity: major
Evidence: The architecture impact says `specs/rigorloop-workflow.md` may be touched if the standard skill contract or stage claim ownership becomes normative workflow behavior.
Required outcome: Decide where the skill contract lives.
Safe resolution: Make `specs/skill-contract.md` the normative home for standard skill shape, claim boundaries, result output expectations, shared-block rules, generated-output boundaries, and evidence-reading guidance. Add the ownership split with `specs/rigorloop-workflow.md`, `docs/workflows.md`, and `skills/*/SKILL.md`.

### SCO3 - Standard section shape should not be one-size-fits-all

Finding ID: SCO3
Severity: major
Evidence: The proposal recommends a full standard shape with sections including `Preconditions`, `Workflow`, `Validation / proof`, `Failure modes`, and `Examples`, even though existing skills contain useful specialized sections.
Required outcome: Define a small required core plus optional skill-type sections.
Safe resolution: Replace the full mandatory shape with required core sections, conditional sections, and skill-type variants for authoring, review, execution, and periodic skills.

### SCO4 - Shared-block source boundary needs a governance decision

Finding ID: SCO4
Severity: major
Evidence: The proposal introduces `templates/shared/*.md` as a likely affected authored surface and says shared blocks can be copied into skills with drift checks.
Required outcome: Define shared-block authority and source boundary.
Safe resolution: Add a `Shared-block source of truth` section naming `templates/shared/<block-name>.md` as canonical authored source for copied skill subsections, with verbatim copy and validator comparison rules.

### SCO6 - `review-resolution guidance` is not a skill but appears as a skill row

Finding ID: SCO6
Severity: major
Evidence: The claim-ownership table includes `review-resolution guidance` as a row in a table otherwise framed around skills.
Required outcome: Rename the row or move it so future authors do not infer a standalone `review-resolution` skill.
Safe resolution: Rename the row to `review-resolution artifact/guidance`.

### SCO7 - Output result block should be adapted by skill type

Finding ID: SCO7
Severity: concern
Evidence: The proposed common result block is `Stage`, `Status`, `Changed artifacts`, `Open blockers`, `Next stage`, and `Validation`.
Required outcome: Define a minimal common result plus optional type-specific fields.
Safe resolution: Replace the common result block with required core fields `Skill`, `Status`, `Artifacts changed`, `Open blockers`, and `Next stage`; list optional fields for validation, review, milestone, readiness, follow-up, authoring, and learn outputs.

### SCO8 - Examples may bloat skills

Finding ID: SCO8
Severity: concern
Evidence: The standard shape includes `Examples`.
Required outcome: Make examples optional and bounded.
Safe resolution: State that examples are optional, short, limited to one minimal valid example and one invalid example when they prevent recurring errors, and that long examples belong in `examples/` or templates.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Problem framing | pass | The proposal targets recurring skill overclaim and state-confusion issues. |
| Source alignment | revise | SCO2 requires a clear normative source for the skill contract. |
| Scope discipline | revise | SCO1 requires an explicit first implementation slice. |
| Structure quality | revise | SCO3 requires required core sections plus conditional variants. |
| Shared-source governance | revise | SCO4 requires shared-block authority. |
| Claim precision | revise | SCO6 requires wording that does not imply a standalone review-resolution skill. |
| Output contract | concern | SCO7 requires type-adapted result fields. |
| Concision | concern | SCO8 requires examples to be optional and bounded. |

## Recommended next stage

Revise the proposal to resolve SCO1, SCO2, SCO3, SCO4, SCO6, SCO7, and SCO8, then rerun proposal-review before downstream spec authoring relies on the proposal.
