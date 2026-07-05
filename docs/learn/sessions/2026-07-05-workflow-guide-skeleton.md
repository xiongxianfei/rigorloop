# Workflow Guide Skeleton

## Frame

- Trigger: maintainer invoked `learn` and observed that the `workflow` skill does not include a skeleton for `docs/workflows.md` in user projects.
- Trigger type: explicit maintainer request and contributor observation.
- Scope: best practices for creating a project-local workflow guide skeleton, coordinating it with stage skills, and avoiding repeated guidance across skills.
- Session path: `docs/learn/sessions/2026-07-05-workflow-guide-skeleton.md`
- Evidence reviewed:
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `specs/workflow-skill-artifact-location-map.md`
  - `specs/workflow-skill-artifact-location-map.test.md`
  - `specs/skill-contract.md`
  - `docs/learn/README.md`
  - `docs/learn/topics/skill-asset-design.md`
  - `docs/learn/topics/workflow-stage-order.md`
- Explicit exclusions:
  - No implementation was performed in this learn session.
  - No new topic entry was created because the proposed improvement changes workflow and skill behavior and needs an owning artifact.
  - No generated adapter output was inspected or changed.
- Prior learnings reviewed:
  - `docs/learn/topics/skill-asset-design.md` says substantial copy-and-fill structures can earn packaged assets, while tiny formats should remain inline.
  - `docs/learn/topics/workflow-stage-order.md` confirms authoritative workflow order remains in `docs/workflows.md`, `specs/rigorloop-workflow.md`, active plans, and accepted workflow specs.

## Observe

### O1. Workflow guide creation lacks a copy-and-fill skeleton

Evidence:

- `skills/workflow/SKILL.md` says the workflow skill creates or refreshes project-local `docs/workflows.md`, but `skills/workflow/` currently contains only `SKILL.md`.
- `specs/workflow-skill-artifact-location-map.md` requires `docs/workflows.md` to be the tracked project-local artifact-location map and workflow guide with a registry, source rank, placement tables, and ambiguity handling.
- The approved skill contract allows substantial structural assets when they earn a file and warns against duplicating full layouts in both `SKILL.md` and an asset.

Observation:

The workflow skill has creation responsibility for a substantial, structured artifact, but lacks a packaged skeleton that agents can copy into a customer project. That increases the chance that agents either omit the guide or recreate partial guidance inconsistently.

### O2. Centralization should use source-of-truth layering, not prose duplication

Evidence:

- `docs/workflows.md` identifies itself as the project-local user-facing artifact-location map.
- `skills/workflow/SKILL.md` says the guide tells users where artifacts go, while stage skills still own artifact content, schemas, stage rules, and portable defaults.
- `specs/workflow-skill-artifact-location-map.md` requires validation to detect drift between the workflow guide, workflow skill defaults, directly relevant stage-skill placement text, and generated adapters when packaged.
- The recent change-id refinement centralized detailed change-id wording in `docs/workflows.md` and changed `workflow` and `implement` skills to reference that guide.

Observation:

The best-practice pattern is already emerging: detailed project-local routing rules belong in the workflow guide; skills should carry short lookup, ownership, and fallback rules rather than duplicated policy prose.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | `direction` | candidate: `direction` | proposal or workflow-spec update; possible workflow skill asset | pending maintainer confirmation | The observation proposes new behavior and packaged skill structure. It is not a durable lesson by itself until accepted in an owning artifact. |
| O2 | `artifact-update` | candidate: `artifact-update` | workflow spec, skill contract if needed, workflow skill, tests, guide-system validation | pending maintainer confirmation | The repository already has an approved centralization model, but adding a skeleton and validation would change authoritative artifacts. |

Contributor confirmation status: pending. This session records the candidate direction and best-practice recommendation, but does not route or update topic files.

## Best-Practice Recommendation

Use a three-layer contract:

1. The approved spec owns normative requirements for what the workflow guide must contain and how it cooperates with skills.
2. The workflow skill owns creation and refresh behavior, plus a resource map that points to a packaged copy-and-fill skeleton.
3. Each project's `docs/workflows.md` owns project-local artifact placement, source rank, routing tables, and concise operational guidance.

Avoid duplicating the same guidance in multiple skills:

- Put detailed artifact-placement, source-rank, change-id, and workflow-guide content in `docs/workflows.md`.
- Keep `skills/workflow/SKILL.md` focused on when to create or refresh the guide, how to resolve conflicts, and when to block.
- Keep stage skills focused on their own artifact content and portable defaults for projects without a workflow guide.
- Make stage skills reference `docs/workflows.md` for project-local path lookup instead of copying path tables or long workflow-guide prose.
- Use validators to enforce registry, table, skill-default, adapter, and skeleton parity.

A workflow guide skeleton should be a packaged workflow-skill asset only if it remains structural:

- include headings, registry shape, required tables, placeholders, and brief instructions;
- avoid hiding lifecycle transition policy or long procedural rules inside the asset;
- keep normative behavior in specs and concise skill instructions;
- include a resource-map entry in `skills/workflow/SKILL.md` with `COPY assets/workflows-skeleton.md` when adopting RigorLoop or creating a missing project-local workflow guide.

## Route

No derivative artifact updates were made because final classification is pending confirmation.

Recommended follow-up if accepted:

- Create a proposal or amend the existing workflow artifact-location spec to add a workflow-guide skeleton contract.
- Add `skills/workflow/assets/workflows-skeleton.md` as a normative copy-and-fill asset.
- Add a `Resource map` entry to `skills/workflow/SKILL.md`.
- Add validator coverage proving the skeleton exists, is packaged, and stays aligned with `docs/workflows.md` registry requirements without duplicating detailed guidance across stage skills.
- Update generated adapter validation if the workflow skill packages the new asset.

## No-Learn Rationale

No durable topic entry was added. The maintainer observation is actionable, but it changes workflow and skill behavior, so it must be accepted through the owning proposal, spec, workflow, skill, and validation artifacts before curated learn guidance can summarize it.

## Validation

- Not run yet. This session only records a learn observation and candidate direction.
