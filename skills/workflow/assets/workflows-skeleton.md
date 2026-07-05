<!-- Template: workflows-skeleton -->

<!-- Skill: workflow -->

<!-- Template status: normative -->

<!-- Maintained alongside: skills/workflow/SKILL.md -->

# Workflow guide

## Status

- Owner skill: workflow
- Purpose: project-local workflow and artifact-location guide
- Last reviewed: <date or change ID>
- Guide status: <current | partial | stale>
- Project-local customizations: <none or summary>

## Source rank

Use this order when deciding artifact placement:

1. Explicit user path or change ID.
2. Existing active artifact metadata, active plan metadata, or active change metadata.
3. Approved specs or schemas.
4. This workflow guide for artifact types it specifies.
5. Stage-skill portable default.
6. Block on ambiguity.

## Lifecycle graph

```text
proposal
-> proposal-review
-> spec
-> spec-review
-> architecture, when required
-> architecture-review, when required
-> plan
-> plan-review
-> test-spec
-> test-spec-review, when required by this workflow
-> implement
-> code-review
-> review-resolution, when triggered
-> ci-maintenance, when triggered
-> explain-change
-> verify
-> pr
```

## Stage obligations

| Stage | Obligation | Required input | Output artifact | Blocks downstream when |
| --- | --- | --- | --- | --- |
| <stage> | <mandatory, conditional, on-demand, or project policy> | <required input> | <output artifact or none> | <blocking condition or none> |

Fill this table from the approved workflow contract and project-local policy.
Keep entries concise and do not redefine lifecycle approval rules or artifact schemas here.

## Artifact registry

```yaml
artifact_locations:
  workflow_guide:
    owner: workflow
    path: docs/workflows.md
    required_when: RigorLoop is adopted or project-local artifact routing is needed
    notes: project-local workflow and artifact-location guide

  proposal:
    owner: proposal
    path: docs/proposals/<change-id>.md
    required_when: proposal stage is active
    notes: decision-oriented change proposal

  spec:
    owner: spec
    path: specs/<slug>.md
    required_when: feature behavior requires a durable contract
    notes: approved feature contract

  test_spec:
    owner: test-spec
    path: specs/<slug>.test.md
    required_when: proof map is required before implementation
    notes: active proof-planning surface

  architecture_record:
    owner: architecture
    path: docs/architecture/<scope>/architecture.md
    required_when: architecture is required
    notes: current architecture package or project-local equivalent

  adr:
    owner: architecture
    path: docs/adr/ADR-YYYYMMDD-<slug>.md
    required_when: durable architecture decision is required
    notes: architecture decision record

  plan_index:
    owner: plan / workflow
    path: docs/plan.md
    required_when: planning exists
    notes: global index, not detailed milestone journal

  change_plan:
    owner: plan
    path: docs/plans/YYYY-MM-DD-<slug>.md
    required_when: workflow-managed change has an execution plan
    notes: detailed plan for one change

  change_metadata:
    owner: workflow
    path: docs/changes/<change-id>/change.yaml
    required_when: formal workflow-managed lifecycle recording begins
    notes: metadata and validation ledger

  review_record:
    owner: review skills
    path: docs/changes/<change-id>/reviews/<stage>-r<n>.md
    required_when: formal review is recorded
    notes: formal review artifact

  review_log:
    owner: review skills
    path: docs/changes/<change-id>/review-log.md
    required_when: formal reviews exist
    notes: review and finding index

  review_resolution:
    owner: review-resolution
    path: docs/changes/<change-id>/review-resolution.md
    required_when: material findings or blocking outcomes require disposition
    notes: finding disposition record

  explain_change:
    owner: explain-change
    path: docs/changes/<change-id>/explain-change.md
    required_when: final explanation is required
    notes: human-readable change rationale

  verify_report:
    owner: verify
    path: docs/changes/<change-id>/verify-report.md
    required_when: verify stage runs
    notes: branch-readiness evidence

  pr_handoff:
    owner: pr
    path: docs/changes/<change-id>/pr.md
    required_when: PR stage is reached
    notes: local PR handoff artifact; external PR URL is metadata

  learn_session:
    owner: learn
    path: docs/learn/sessions/YYYY-MM-DD-<slug>.md
    required_when: learn trigger occurs
    notes: historical learning evidence, not live routing authority
```

## Artifact location table

| Artifact type | Canonical path | Owner skill | Required when | Notes |
| --- | --- | --- | --- | --- |
| Workflow guide | `docs/workflows.md` | `workflow` | RigorLoop is adopted or routing needs local guide | This file |
| Proposal | `docs/proposals/<change-id>.md` | `proposal` | Proposal stage | Decision artifact |
| Spec | `specs/<slug>.md` | `spec` | Spec stage | Behavior contract |
| Test spec | `specs/<slug>.test.md` | `test-spec` | Test-spec stage | Active proof map |
| Architecture record | `docs/architecture/<scope>/architecture.md` | `architecture` | Architecture required | Architecture package |
| ADR | `docs/adr/ADR-YYYYMMDD-<slug>.md` | `architecture` | Durable architecture decision | ADR |
| Plan index | `docs/plan.md` | `plan` / `workflow` | Planning exists | Global index |
| Change plan | `docs/plans/YYYY-MM-DD-<slug>.md` | `plan` | Workflow-managed change | Detailed plan |
| Change metadata | `docs/changes/<change-id>/change.yaml` | `workflow` | Formal change lifecycle | Metadata ledger |
| Review record | `docs/changes/<change-id>/reviews/<stage>-r<n>.md` | review skill | Formal review | Review evidence |
| Review log | `docs/changes/<change-id>/review-log.md` | review skills | Formal review exists | Review index |
| Review resolution | `docs/changes/<change-id>/review-resolution.md` | review-resolution | Findings require disposition | Resolution evidence |
| Explain change | `docs/changes/<change-id>/explain-change.md` | `explain-change` | Final explanation | Change rationale |
| Verify report | `docs/changes/<change-id>/verify-report.md` | `verify` | Verify stage | Branch-readiness proof |
| PR handoff | `docs/changes/<change-id>/pr.md` | `pr` | PR stage | Local handoff |
| Learn session | `docs/learn/sessions/YYYY-MM-DD-<slug>.md` | `learn` | Learn trigger | Historical rationale |

## Review record placement

| Review type | Path | Creates review-log entry? | Creates review-resolution? |
| --- | --- | ---: | ---: |
| Proposal review | `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` | yes | only when findings or blockers require disposition |
| Spec review | `docs/changes/<change-id>/reviews/spec-review-r<n>.md` | yes | only when findings or blockers require disposition |
| Architecture review | `docs/changes/<change-id>/reviews/architecture-review-r<n>.md` | yes | only when findings or blockers require disposition |
| Plan review | `docs/changes/<change-id>/reviews/plan-review-r<n>.md` | yes | only when findings or blockers require disposition |
| Test-spec review | `docs/changes/<change-id>/reviews/test-spec-review-r<n>.md` | yes | only when findings or blockers require disposition |
| Code review | `docs/changes/<change-id>/reviews/code-review-<milestone>-r<n>.md` | yes | only when findings or blockers require disposition |

## Plan surfaces

| Surface | Path | Purpose |
| --- | --- | --- |
| Plan index | `docs/plan.md` | Small global index of active, blocked, and recently completed work |
| Change plan | `docs/plans/YYYY-MM-DD-<slug>.md` | Detailed execution plan for one workflow-managed change |
| Change metadata | `docs/changes/<change-id>/change.yaml` | Metadata, validation, and evidence ledger |

## Guide ownership

| Question | Primary source | Secondary source |
| --- | --- | --- |
| Why does this project exist? | `VISION.md` | README summary |
| What governance rules apply? | `CONSTITUTION.md` | workflow guide summary |
| Where does an artifact go? | `docs/workflows.md` | stage-skill portable default |
| What does the repository contain? | `docs/project-map.md` | README links |
| What work is active? | `docs/plan.md` | active change pack |
| What happened in one change? | `docs/changes/<change-id>/` | plan index |
| How do I perform one stage? | `skills/<stage>/SKILL.md` | this workflow guide |
| Why did a rule change? | proposal/spec/learn session | workflow guide after accepted update |

## Customization rules

- Record project-local path customizations in the artifact registry and table.
- Do not rely on chat history or learn sessions as live routing authority.
- If a stage skill's portable default conflicts with this guide, use this guide for the project-local workflow and record the drift for validation.
- If this guide conflicts with a governing spec or schema, stop and resolve the conflict before writing new artifacts.
- Unknown artifact types block instead of using inferred paths.

## Migration notes

- Historical artifacts may remain in prior locations unless an approved migration says otherwise.
- Forward placement for new workflow-managed artifacts follows this guide.
- Record any legacy path exceptions here.

## Validation notes

- Validate registry and table consistency.
- Validate workflow-skill default paths against this guide.
- Validate directly relevant stage-skill placement text against this guide.
- Validate generated adapter packaging when the workflow skill ships this skeleton.
