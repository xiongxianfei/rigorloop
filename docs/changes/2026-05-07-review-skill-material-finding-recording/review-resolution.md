# Review Resolution: Review Skill Material Finding Recording

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: code-review-r1
Review closeout: code-review-r2

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `code-review-r1`, `code-review-r2`
- Findings resolved: 13
- Unresolved findings: 0
- Final result: proposal-review, spec-review, `code-review-r1`, and `code-review-r2` findings were accepted, resolved, and validated. The aggregate implementation slice is ready for post-commit code-review rerun.

This record resolves the material findings from `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, and `spec-review-r3` for the review skill material-finding recording proposal and spec amendments. It also resolves the `code-review-r2` aggregate closeout finding through the aggregate milestone closeout commit.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| RSV1 | accepted | resolved | Strengthened timing rule: record material findings before review-driven edits begin; reconstructed records disclose after-fix timing. |
| RSV2 | accepted | resolved | Broadened tracked-artifact definition to any version-controlled repository file committed or reviewed as part of the work. |
| RSV3 | accepted | resolved | Clarified that the listed review files are the initial review-record root, not final non-trivial handoff completion. |
| RSV4 | accepted | resolved | Preserved the boundary: material findings require `review-resolution.md`; no-material detailed records do not require empty `review-resolution.md`. |
| RSV5 | accepted | resolved | Defined `templates/shared/review-isolation-and-recording.md` as the canonical source for the shared review-skill subsection. |
| RSV6 | accepted | resolved | Added an operational materiality shortcut while preserving `CONSTITUTION.md` as the authority. |
| RSV7 | accepted | resolved | Added required final-output guidance for isolated reviews with material findings. |
| SR1 | accepted | resolved | Clarified that material findings are always recorded, while change-local review files are required under the approved detailed-record triggers. |
| SR2 | accepted | resolved | Initially split recording surface from change-local requirements; later superseded by SR4 owner decision to use the simpler broad trigger. |
| SR3 | accepted | resolved | Aligned governance with the active material-finding trigger; later updated again for the SR4 broad-trigger decision. |
| SR4 | accepted | resolved | Simplified the rule: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording. |
| CR1-F1 | accepted | resolved | Changed the shared review block from "should" to "must", tightened static coverage, and regenerated skill and adapter outputs. |
| CR2-F1 | accepted | resolved | Created the aggregate M1-M3 closeout commit before treating code-review as the required post-closeout rerun. |

## Common Resolution Metadata for RSV Findings

- Owner: proposal author
- Owning stage: proposal
- Validation target: revise the proposal and rerun lifecycle, review-artifact, metadata, whitespace, diff, and selector-selected validation.
- Validation evidence: targeted review-artifact, metadata, lifecycle, whitespace, diff, and selector-selected validation passed after the proposal revision.

## Resolution Entries

### proposal-review-r1

#### RSV1 - Record before edit

Finding ID: RSV1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Strengthened the timing rule so material findings that will drive tracked artifact edits are recorded before review-driven edits begin. If edits already began, the record must be reconstructed and disclose source, timing, available evidence, stable Finding IDs, and known fidelity loss.
Rationale: The finding is correct. A completion-only rule can still permit fixing first and recording later, which weakens first-pass review evidence.
Validation target: Covered by common resolution metadata.
Validation evidence: Covered by shared validation evidence.

#### RSV2 - Broaden tracked-artifact definition

Finding ID: RSV2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Broadened the tracked-artifact definition to any version-controlled repository file whose change will be committed or reviewed as part of the work. Examples now include lifecycle artifacts, governance files, workflow summaries, skills, specs, schemas, scripts, generated outputs, README content, and change-local artifacts.
Rationale: The finding is correct. Material review findings should be recorded when they drive edits to any tracked repository artifact, not only formal lifecycle files.
Validation target: Covered by common resolution metadata.
Validation evidence: Covered by shared validation evidence.

#### RSV3 - Initial review-record root is not final handoff

Finding ID: RSV3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Clarified that the listed review files form the initial review-record root only. Final non-trivial handoff still requires durable Markdown reasoning such as `explain-change.md` or another approved durable reasoning surface.
Rationale: The finding is correct. Initial review evidence and final non-trivial handoff serve different purposes.
Validation target: Covered by common resolution metadata.
Validation evidence: Covered by shared validation evidence.

#### RSV4 - Preserve material/no-material review-resolution boundary

Finding ID: RSV4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Preserved the existing no-material boundary while aligning material findings with the simplified rule: material findings require `review-resolution.md`; detailed records with no material findings require `change.yaml`, `review-log.md`, and the detailed review file; empty `review-resolution.md` is not required for no-material detailed records unless another approved trigger applies.
Rationale: The finding is correct. `review-resolution.md` is for finding dispositions, not for every review event.
Validation target: Covered by common resolution metadata.
Validation evidence: Covered by shared validation evidence.

#### RSV5 - Canonical source for shared review subsection

Finding ID: RSV5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Defined `templates/shared/review-isolation-and-recording.md` as the canonical source for the shared subsection. The five formal review skills copy the subsection manually, and tests compare copied blocks against that source. No generation step is introduced.
Rationale: The finding is correct. Without a canonical source, byte-equality checks would be brittle and arbitrary.
Validation target: Covered by common resolution metadata.
Validation evidence: Covered by shared validation evidence.

#### RSV6 - Operational materiality shortcut

Finding ID: RSV6
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added an operational shortcut: treat a finding as material when it changes or blocks tracked artifact edits, scope, requirements, architecture, sequencing, validation, follow-up work, or disposition, unless a non-material rationale is explicitly recorded.
Rationale: The finding is correct. The shortcut helps prevent agents from relabeling material findings as minor while preserving `CONSTITUTION.md` as the authority.
Validation target: Covered by common resolution metadata.
Validation evidence: Covered by shared validation evidence.

#### RSV7 - Isolated material review output

Finding ID: RSV7
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added a final-output rule for isolated reviews with material findings. After the SR4 owner decision, the output must state isolated handoff status, material Finding IDs, required durable review record path or reconstruction requirement, that `review-resolution.md` is required, and next allowed action.
Rationale: The finding is correct. The obligation must be visible at review-output time, not only implied by later workflow rules.
Validation target: Covered by common resolution metadata.
Validation evidence: Covered by shared validation evidence.

### spec-review-r1

#### SR1 - Isolated material-finding trigger conflict

Finding ID: SR1
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Updated the formal review recording, review finding resolution, and workflow specs to clarify the active rule after the SR4 owner decision: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
Rationale: The finding is correct. Without an explicit precedence rule, `R2` and `R5` in `specs/formal-review-recording.md` can be read as requiring and allowing omission of the same detailed review file.
Validation target: Revised spec wording plus review-artifact closeout, metadata, lifecycle, whitespace, diff, and selector-selected validation.
Validation evidence: Covered by shared validation evidence after SR1 resolution.

### spec-review-r2

#### SR2 - Isolated material output still assumes a change-local path

Finding ID: SR2
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Initially updated isolated material-review output requirements to distinguish the recording surface from the change-local detailed-record requirement. After the SR4 owner decision, replaced that split with the simpler output rule: isolated material-review output states handoff status, Finding IDs, required durable review record path or reconstruction requirement, that `review-resolution.md` is required, and the next allowed action.
Rationale: The original finding identified a real inconsistency in the refined split. The owner later chose the simpler broad trigger, so the durable resolution is to remove the split rather than keep refining it.
Validation target: Revised spec wording, examples, boundary cases, and acceptance criteria in the formal review recording and workflow specs.
Validation evidence: Covered by shared validation evidence after SR4 resolution.

#### SR3 - Governance and workflow summaries still conflict

Finding ID: SR3
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Updated `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` to teach the same active broad rule: material findings are always recorded; all material findings require change-local review files; isolation stops handoff, not recording.
Rationale: Governance and operational guidance must match the active spec. After the SR4 owner decision, the older split was removed.
Validation target: Aligned governance and operational wording plus lifecycle, review-artifact, metadata, whitespace, diff, and selector-selected validation.
Validation evidence: Covered by shared validation evidence after SR4 resolution.

### spec-review-r3

#### SR4 - Standalone review-resolution trigger reintroduces broad material-finding rule

Finding ID: SR4
Disposition: accepted
Status: resolved
Owner: spec owner
Owning stage: spec
Chosen action: Applied the owner decision to simplify the rule across the proposal, formal review recording spec, review finding resolution spec, workflow spec, `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md`: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
Rationale: The owner chose the broad trigger as the clearer contract. That resolves the conflict by making `R12c` intentional instead of accidental drift.
Validation target: Revised proposal, spec, governance, workflow summary, and review closeout artifacts plus lifecycle, review-artifact, metadata, whitespace, diff, and selector-selected validation.
Validation evidence: Covered by shared validation evidence after SR4 resolution.

### code-review-r1

#### CR1-F1 - Shared timing rule weakens a MUST to should

Finding ID: CR1-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Update the canonical shared review block and all copied/generated review-skill outputs so the durable review record must be created before review-driven edits begin.
Rationale: The finding is correct. The approved specs require material review findings to be recorded before fixes begin, so skill guidance should not express that rule as optional or advisory.
Validation target: Update timing wording and static assertions, regenerate generated outputs, then rerun selected validation for skill, review-artifact, adapter, lifecycle, metadata, selector, whitespace, and explicit CI checks.
Validation evidence: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py`, `python scripts/build-adapters.py --version 0.1.1`, and the final selected `bash scripts/ci.sh --mode explicit --path ...` validation passed after the fix.

### code-review-r2

#### CR2-F1 - Aggregate closeout commit missing before required code-review rerun

Finding ID: CR2-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Create the aggregate milestone closeout commit `M1: implement review recording proof and guidance`, include former M1/M2/M3 sub-slice scope and validation evidence in the commit body, then rerun `code-review` against the committed aggregate slice.
Rationale: The finding is correct. The active plan explicitly makes the aggregate commit part of aggregate closeout before the required post-closeout code-review rerun and `verify`.
Validation target: `git log --oneline -1` or equivalent shows the aggregate `M1:` commit and a later same-stage code-review rerun records no blocking aggregate-closeout finding.
Validation evidence: Aggregate validation passed before the closeout commit: `python scripts/test-skill-validator.py`, `python scripts/test-review-artifact-validator.py`, `python scripts/validate-skills.py`, `python scripts/test-select-validation.py`, `python scripts/test-adapter-distribution.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`, `python scripts/test-change-metadata-validator.py`, `bash scripts/ci.sh --mode local`, `git diff --check -- .`, and whitespace scan over changed paths.

## Shared Validation Evidence

| Validation area | Result | Notes |
|---|---|---|
| Review-artifact closeout validation for RSV findings | pass | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording` passed before `spec-review-r1` opened `SR1`. |
| Review-artifact structure validation after SR1 | pass | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording` |
| Review-artifact closeout validation after SR1 resolution | pass | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording` |
| Review-artifact structure validation after spec-review-r2 recording | pass | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording` passed with `reviews=3`, `findings=10`, `log_entries=3`, and `resolution_entries=10`. |
| Change metadata validation | pass | `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` |
| Artifact lifecycle validation | pass | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` |
| Diff whitespace validation | pass | `git diff --check -- ...` |
| Whitespace scan | pass | `rg -n '[[:blank:]]$|\t' ...` found no matches. |
| Selector-selected validation | pass | `bash scripts/ci.sh --mode explicit --path ...` passed selected checks. |
| Selector-selected validation after spec-review-r2 recording | pass | `bash scripts/ci.sh --mode explicit --path ...` passed selected checks for the proposal, spec amendments, and review artifacts. |
| Review-artifact closeout validation after SR2/SR3 resolution | pass | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording` passed with `reviews=3`, `findings=10`, `log_entries=3`, and `resolution_entries=10`. |
| Change metadata validation after SR2/SR3 resolution | pass | `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` |
| Artifact lifecycle validation after SR2/SR3 resolution | pass | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed with existing lifecycle-language warnings in `docs/workflows.md` and `specs/rigorloop-workflow.md`. |
| Diff whitespace validation after SR2/SR3 resolution | pass | `git diff --check -- ...` |
| Whitespace scan after SR2/SR3 resolution | pass | `rg -n '[[:blank:]]$|\t' ...` found no matches. |
| Selector-selected validation after SR2/SR3 resolution | pass | `bash scripts/ci.sh --mode explicit --path ...` passed selected checks for governance, workflow, spec, proposal, change metadata, and review artifacts. |
| Review-artifact structure validation after spec-review-r3 recording | pass | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording` passed with `reviews=4`, `findings=11`, `log_entries=4`, and `resolution_entries=11`. |
| Change metadata validation after spec-review-r3 recording | pass | `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` |
| Artifact lifecycle validation after spec-review-r3 recording | pass | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed with existing lifecycle-language warnings in `docs/workflows.md` and `specs/rigorloop-workflow.md`. |
| Diff whitespace validation after spec-review-r3 recording | pass | `git diff --check -- ...` |
| Whitespace scan after spec-review-r3 recording | pass | `rg -n '[[:blank:]]$|\t' ...` found no matches. |
| Selector-selected validation after spec-review-r3 recording | pass | `bash scripts/ci.sh --mode explicit --path ...` passed selected checks for governance, workflow, spec, proposal, change metadata, and review artifacts. |
| Review-artifact closeout validation after SR4 resolution | pass | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording` passed with `reviews=4`, `findings=11`, `log_entries=4`, and `resolution_entries=11`. |
| Change metadata validation after SR4 resolution | pass | `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml` |
| Artifact lifecycle validation after SR4 resolution | pass | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed with existing lifecycle-language warnings in `docs/workflows.md` and `specs/rigorloop-workflow.md`. |
| Diff whitespace validation after SR4 resolution | pass | `git diff --check -- ...` |
| Whitespace scan after SR4 resolution | pass | `rg -n '[[:blank:]]$|\t' ...` found no matches. |
| Selector-selected validation after SR4 resolution | pass | `bash scripts/ci.sh --mode explicit --path ...` passed selected checks for governance, workflow, spec, proposal, change metadata, and review artifacts. |
| Skill regression after CR1-F1 fix | pass | `python scripts/test-skill-validator.py` passed after adding mandatory timing wording coverage. |
| Authored skill validation after CR1-F1 fix | pass | `python scripts/validate-skills.py` passed. |
| Generated output refresh after CR1-F1 fix | pass | `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1` passed. |
| Selector-selected validation after CR1-F1 fix | pass | `bash scripts/ci.sh --mode explicit --path ...` passed selected checks for authored skills, generated outputs, review artifacts, lifecycle, metadata, selector, adapters, and whitespace-relevant surfaces. |
| Aggregate validation before closeout commit | pass | `python scripts/test-skill-validator.py`, `python scripts/test-review-artifact-validator.py`, `python scripts/validate-skills.py`, `python scripts/test-select-validation.py`, `python scripts/test-adapter-distribution.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-07-review-skill-material-finding-recording`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`, `python scripts/test-change-metadata-validator.py`, `bash scripts/ci.sh --mode local`, and `git diff --check -- .` passed. |
| Aggregate whitespace scan before closeout commit | pass | Whitespace scan over changed paths found no trailing whitespace or tab matches. |
| Review closeout validation after CR2-F1 resolution | pass | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`, `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`, lifecycle validation, selected CI for closeout files, `git diff --check -- .`, and whitespace scan passed. |

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every accepted finding has rationale.
- [x] Every accepted finding has validation evidence.
- [x] No findings remain `needs-decision`.
- [x] No findings remain open.
- [x] Review closeout is recorded for `proposal-review-r1`.
- [x] Review closeout is recorded for `spec-review-r1`.
- [x] Review closeout is recorded for `spec-review-r2`.
- [x] Review closeout is recorded for `spec-review-r3`.
- [x] Review closeout is recorded for `code-review-r1`.
- [x] Review closeout is recorded for `code-review-r2`.
- [x] Closeout status is `closed`.
