# Behavior Preservation Proof

Change ID: `2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
Proof date: 2026-06-18

## Scope

This proof covers the guide-system first slice required by `specs/guide-system-source-of-truth-alignment.md` R43-R50 and `specs/guide-system-source-of-truth-alignment.test.md` GST-009 through GST-011.

It records forward guide ownership, baseline drift treatment, and compatibility preservation. It does not migrate historical artifacts, change lifecycle stage order, change artifact schemas, or hand-edit generated adapter output.

## Preservation Matrix

| Surface | Baseline behavior | New proof | Preservation |
| --- | --- | --- | --- |
| `README.md` | Landing guide with first-contact orientation and links into deeper docs. | Adds a compact `Where to go next` guide index linking `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, and `skills/`. It keeps the workflow-at-a-glance summary rather than full workflow contracts. | Strengthened. README remains orientation, not source of exact workflow policy. |
| `VISION.md` | Canonical project vision for identity, target users, commitments, and proposal fit. | Unchanged by implementation; README links to it as project direction. `CONSTITUTION.md` still ranks it below governance for vision/proposal-fit questions. | Preserved. |
| `CONSTITUTION.md` | Highest-priority repository governance and source-of-truth order. | Unchanged by implementation; guide-system spec and workflow guide remain subordinate. | Preserved. |
| `docs/workflows.md` | Project-local workflow guide and artifact-location map. | Adds guide ownership routing and source-rank guidance while preserving the workflow-map registry/table owner boundary. M2 validator now composes `validate_workflow_artifact_map_contract` for registry/table consistency. | Strengthened without changing exact artifact-location semantics. |
| `docs/project-map.md` | Living repository orientation map. | Clarifies that it does not own workflow stage order, exact lifecycle artifact placement, or current milestone state. | Strengthened. |
| `docs/plan.md` | Bounded lifecycle index of active, blocked, recent done, and superseded planned work. | Keeps only the active guide-system index entry and points detailed state to the concrete plan body. | Preserved. |
| Stage skills | Portable stage operating contracts for skill-only adopters. | No canonical `skills/` files changed in this initiative. Existing workflow and plan skills still carry portable defaults, project-local guidance lookup, and block-on-ambiguity behavior. | Preserved. |
| Learn sessions | Historical learning evidence and rationale. | Workflow guide now states learn sessions are not live routing authority unless the rule is promoted to a live guide, approved spec, schema, or owning stage skill. No learn sessions were migrated. | Clarified. |
| Generated adapters | Generated public adapter bodies are not tracked source for current releases. | Branch diff contains no `skills/`, `.codex/skills/`, or generated adapter package output changes. Adapter packaging proof is not triggered for this slice. | Preserved. |

## Compatibility Checks

| Requirement | Proof |
| --- | --- |
| Baseline drift is recorded, not migrated. | M1 and M3 plan notes state historical artifacts were not migrated. `docs/workflows.md` customization notes preserve existing `docs/plans/*.md` placement and do not move historical records. |
| Historical migration requires separate approval. | No historical artifact paths were moved. New proof files are change-local evidence under the active change pack. |
| Lifecycle stage order is unchanged. | README keeps the same standard lifecycle chain from proposal through PR; no workflow stage order code or spec change is introduced. |
| Artifact schemas are unchanged. | No schema files are modified. Validators inspect guide shape and existing workflow-map contracts; they do not change artifact content schemas. |
| Validation command behavior remains scoped to approved validator contracts. | M2 adds selected guide-system validation and composes the existing workflow-map validator; no broad natural-language scoring or second registry contract remains. |
| Generated adapter output is not hand-edited. | Branch diff contains no `dist/adapters/` generated bodies and no canonical skill changes that trigger adapter packaging proof. |
| Security and privacy posture is unchanged. | The change adds local docs and local validation only; no secrets, network dependencies, credentials, auth behavior, or hosted-service claims are introduced. |

## Evidence Links

- Guide-system spec: `specs/guide-system-source-of-truth-alignment.md`
- Test spec: `specs/guide-system-source-of-truth-alignment.test.md`
- Workflow guide: `docs/workflows.md`
- Active plan: `docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md`
- Change metadata and validation ledger: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`

## Result

The guide-system slice strengthens orientation and drift detection while preserving governance, exact artifact-location ownership, plan-body placement, stage-skill portability, historical artifact placement, generated output policy, lifecycle order, and artifact schemas.
