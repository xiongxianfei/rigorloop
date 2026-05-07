# Spec Review R2

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: Maintainer spec-review
Target: specs/formal-review-recording.md; specs/review-finding-resolution-contract.md; specs/rigorloop-workflow.md; CONSTITUTION.md; AGENTS.md; docs/workflows.md
Status: changes-requested

## Scope

Reviewed the spec amendments after the `SR1` resolution, including the refined split between material-finding recording and change-local review-file creation, then cross-checked higher-priority governance and operational guidance.

## Findings

### SR2: Isolated material output still assumes a change-local record path

Finding ID: SR2

Evidence: `specs/formal-review-recording.md:122` and `specs/formal-review-recording.md:124` now say material findings are always recorded, while change-local review files are required only when the finding affects tracked work or closeout. `specs/formal-review-recording.md:155` also allows an isolated or review-only material finding with no tracked change and no closeout need to omit a detailed review file unless durable capture is requested. However, `specs/formal-review-recording.md:259` through `specs/formal-review-recording.md:264`, `specs/rigorloop-workflow.md:571`, `specs/rigorloop-workflow.md:764`, and `specs/rigorloop-workflow.md:913` still require isolated material-review output to name a required durable review record path or reconstruction requirement.

Required outcome: The final-output requirements must distinguish the recording surface from the narrower change-local review-file requirement.

Suggested resolution: Update the isolated material-review output rules, boundary cases, examples, and acceptance criteria so the output states isolated handoff status, material Finding IDs, the recording surface, whether change-local review files are required, the durable review record path or reconstruction requirement only when change-local files are required, whether `review-resolution.md` is required, and the next allowed action. The next-action vocabulary should cover recording in review output or artifact-local settlement, creating the change-local record before fixing, reconstructing if fixes already began, and stopping for owner decision.

### SR3: Higher-priority and operational guidance still contradict the refined trigger

Finding ID: SR3

Evidence: `CONSTITUTION.md:167` says workflow-managed formal reviews that produce material findings must preserve a detailed review record. `AGENTS.md:40` and `docs/workflows.md:101` repeat the same broad trigger. These higher-priority and operational surfaces conflict with `specs/formal-review-recording.md:122`, `specs/formal-review-recording.md:124`, `specs/rigorloop-workflow.md:537`, and `specs/rigorloop-workflow.md:539`, which now split always-record material findings from the narrower change-local review-file trigger.

Required outcome: The governance and operational surfaces must be aligned in the same change, or the specs must explicitly require those updates before implementation or normalization relies on the refined trigger.

Suggested resolution: Update `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` to use the same split: material findings are always recorded; detailed change-local review files are required when a material finding affects tracked work or closeout, when a stage-owned non-approval outcome blocks or requires revision, when the review is reconstructed, when it will be cited as closeout evidence, or when a reviewer or maintainer explicitly requests durable capture.

## Recommendation

Request changes before approving the spec amendments. These findings are material because they affect the observable review-output contract and create a source-of-truth conflict between the draft specs and higher-priority workflow governance.
