# Workflow Skill Artifact-Location Map Review Resolution

## Scope

This record closes formal lifecycle review findings for the workflow skill artifact-location map proposal revision.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2

## Resolution Entries

### proposal-review-r1

#### WFO-PR1

Finding ID: WFO-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised the proposal again after owner correction to choose `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body location, keep `docs/plan.md` as the global plan index, and keep `docs/changes/<change-id>/` as the change-local evidence pack.
Rationale: The repository's `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `plan` skill already establish `docs/plans/` as the best-practice plan-body location, and the owner explicitly required preserving that practice.
Validation target: Proposal defines one forward canonical plan-body location and does not leave plan placement as a blocking open question.
Validation evidence: Proposal sections `Context`, `Recommended Direction`, `Plan-location Decision`, `Acceptance Criteria`, `Open Questions`, and `Decision Log`.

#### WFO-PR2

Finding ID: WFO-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised the proposal to require `docs/workflows.md` to contain both a canonical fenced YAML artifact registry for validators and synchronized human-readable Markdown tables for users.
Rationale: Validators need deterministic structure, while maintainers need a readable workflow guide.
Validation target: Proposal defines a single machine-checkable workflow-map source and requires Markdown tables not to contradict it.
Validation evidence: Proposal sections `Workflow Map Representation`, `Testing and Verification Strategy`, `Acceptance Criteria`, `Open Questions`, and `Decision Log`.

#### WFO-PR3

Finding ID: WFO-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised the proposal to edit stage skills in the same first slice only when their placement text directly contradicts the approved workflow map or source-rank model. The proposal names `workflow`, `plan`, `proposal-review`, and `spec-review` as required first-slice candidates when their text conflicts.
Rationale: The change should close real drift without bulk-editing all lifecycle skills for stylistic consistency.
Validation target: Proposal defines the stage-skill edit boundary before spec.
Validation evidence: Proposal sections `Stage-Skill Edit Policy`, `Scope budget`, `Architecture Impact`, `Acceptance Criteria`, `Open Questions`, and `Decision Log`.

### proposal-review-r2

No material findings.

### spec-review-r2

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

No material findings.

### code-review-m2-r1

#### WFO-CR1

Finding ID: WFO-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Chosen action: Added `architecture_record` and `adr` to the workflow artifact-map required registry-entry set and added targeted regression coverage that removes each entry from the real workflow map and expects an artifact-specific missing-entry diagnostic.
Rationale: R15 requires both architecture records and ADRs in the canonical artifact registry, and the validator must fail deterministically when either required entry is absent.
Required outcome: The workflow-map validator fails when either `architecture_record` or `adr` is missing from `artifact_locations`.
Validation target: `python scripts/test-skill-validator.py -k workflow_map_m2`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, selected lifecycle validation, and selected CI for the touched M2 surfaces.
Validation evidence: `python scripts/test-skill-validator.py -k workflow_map_m2`, `python scripts/test-skill-validator.py -k workflow`, `python scripts/test-skill-validator.py`, and `python scripts/validate-skills.py` passed after the fix.

### code-review-m2-r2

No material findings.

### spec-review-r1

#### WFO-SR1

Finding ID: WFO-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Suggested resolution: Resolve the conflict with the approved installed-skill artifact placement contract before downstream reliance.
Final action: Revised the proposal and spec to preserve `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body path, remove the proposed `docs/changes/<change-id>/plan.md` forward contract, and state that this spec aligns with rather than amends the installed-skill artifact placement contract.
Rationale: The repository's existing plan-body contract is authoritative for this change after owner correction, so the safe resolution is to remove the conflicting draft path instead of superseding established practice.
Expected proof: Revised proposal and spec name `docs/plans/YYYY-MM-DD-slug.md` as the plan-body path, validation passes, and no unresolved plan-path contradiction remains.
Validation evidence: Revised proposal `Plan-location Decision` and spec requirements R17-R20, R24, R31a, R45, EC6, and AC8-AC10 preserve `docs/plans/YYYY-MM-DD-slug.md` as the detailed plan-body path and reject `docs/changes/<change-id>/plan.md` as a canonical plan-body path.

#### WFO-SR2

Finding ID: WFO-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Suggested resolution: Define the canonical PR handoff path or add a structured exception for PR handoff with a required non-path representation such as `external_surface` or `policy`.
Final action: Revised the spec so repository-local artifacts require a single `path`, while PR handoff and other non-repository-local artifacts require exactly one structured placement representation: `path`, `external_surface`, or `policy`.
Rationale: Existing repository practice treats PR body handoff as a PR-stage/readiness surface rather than a consistently tracked `pr.md` file, so the registry must support deterministic non-path representation without guessing.
Expected proof: Revised spec updates R8/R15, examples, acceptance criteria, and validator expectations so PR handoff validation is deterministic.
Validation evidence: Revised spec example E8, requirements R8-R8b, R15, observability text, and AC19 define deterministic PR handoff registry representation through `path`, `external_surface`, or `policy`.

#### WFO-SR3

Finding ID: WFO-SR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Suggested resolution: Clarify whether safe project-local customization for formal review records must remain under the change pack, or define the conditions under which a custom path outside `docs/changes/<change-id>/reviews/` is allowed despite R35.
Final action: Revised the spec so safe project-local formal review customization may customize filenames, review-type templates, or substructure under `docs/changes/<change-id>/reviews/`, but cannot route formal review records outside the change pack unless a higher-priority explicit path, active metadata, approved spec, schema, or user instruction permits it.
Rationale: R35 requires review records under the change pack, while R36/R37 allow safe project-local customizations without defining the boundary.
Expected proof: Revised spec updates R35-R37, related edge cases, and acceptance criteria so validators can distinguish valid and invalid custom review paths.
Validation evidence: Revised spec example E9, requirements R35-R37a, EC14a, EC14b, and AC20 define the formal review customization boundary under `docs/changes/<change-id>/reviews/`.

## Validation Evidence

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 1 review, 3 findings, 1 log entry, and 3 resolution entries.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md` passed.
- `git diff --check -- docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 2 reviews, 3 findings, 2 log entries, and 3 resolution entries after proposal-review R2.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` passed after proposal-review R2.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md` passed after proposal-review R2.
- `git diff --check -- docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed after proposal-review R2.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md` passed after spec authoring.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` passed after spec authoring.
- `git diff --check -- docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md specs/workflow-skill-artifact-location-map.md docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed after spec authoring.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` after spec authoring.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 3 reviews, 6 findings, 3 log entries, and 6 resolution entries after spec-review R1 recording.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` passed after spec-review R1 recording.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r1.md` passed after spec-review R1 recording.
- `git diff --check -- docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md specs/workflow-skill-artifact-location-map.md docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed after spec-review R1 recording.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r1.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` after spec-review R1 recording.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map` failed before adding validation evidence for resolved WFO-SR1 through WFO-SR3.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 3 reviews, 6 findings, 3 log entries, and 6 resolution entries after spec revision.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` passed after spec revision.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r1.md` passed after spec revision.
- `git diff --check -- docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md specs/workflow-skill-artifact-location-map.md docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed after spec revision.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r1.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` after spec revision.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 4 reviews, 6 findings, 4 log entries, and 6 resolution entries after spec-review R2.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` passed after spec-review R2.
- `git diff --check -- docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed after spec-review R2.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 4 reviews, 6 findings, 4 log entries, and 6 resolution entries after spec-review R2.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md` passed after spec-review R2.
- `bash scripts/ci.sh --mode explicit --path specs/workflow-skill-artifact-location-map.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r1.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` after spec-review R2.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 5 reviews, 6 findings, 5 log entries, and 6 resolution entries after plan-review R1.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map` passed with 5 reviews, 6 findings, 5 log entries, and 6 resolution entries after plan-review R1.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` passed after plan-review R1.
- `git diff --check -- docs/changes/2026-06-17-workflow-skill-artifact-location-map docs/plans/2026-06-18-workflow-skill-artifact-location-map.md docs/plan.md specs/workflow-skill-artifact-location-map.md` passed after plan-review R1.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/workflow-skill-artifact-location-map.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/plan-review-r1.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md` passed after plan-review R1.
- `bash scripts/ci.sh --mode explicit --path specs/workflow-skill-artifact-location-map.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r2.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/plan-review-r1.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` after plan-review R1.
