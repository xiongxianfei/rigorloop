# Formal Review Recording

## Status

- approved

## Related proposal

- [Formal Review Recording](../docs/proposals/2026-05-04-formal-review-recording.md)
- [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- [Review Skill Recording and Status Output Guardrail](../docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md)

## Goal and context

This spec defines when formal lifecycle reviews create durable change-local review records, how upstream review findings are preserved before fixes, and how review evidence stays separate from proposal, spec, architecture, and plan status.

The repository already has a review artifact model under `docs/changes/<change-id>/reviews/`, `review-log.md`, and `review-resolution.md`. The gap is the trigger policy for stages before `code-review`: `proposal-review`, `spec-review`, `architecture-review`, and `plan-review`.

The goal is stage-neutral recording for material review findings without forcing detailed files for every clean review.

This amendment clarifies that isolated review handoff behavior and material-finding recording are independent. A direct or review-only review remains isolated by default, but every material finding still requires durable change-local review evidence.

This amendment also defines formal review output status guardrails. Review output must distinguish review verdicts, review-recording state, and artifact-status synchronization state. Clean or approving review results must synchronize the reviewed artifact's owned lifecycle surface when the status owner is clear, or report a concrete status-sync blocker.

## Glossary

- `formal lifecycle review`: one of `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, or `code-review`.
- `detailed review file`: a Markdown file under `docs/changes/<change-id>/reviews/` that records one formal lifecycle review event.
- `stage-owned non-approval outcome`: a review outcome in that stage's vocabulary that blocks downstream progress or requires revision.
- `initial review-record root`: the smallest `docs/changes/<change-id>/` root created before review-driven fixes or downstream routing when a detailed review file is required but no change-local root exists yet.
- `artifact-local settlement`: final status, decision log, readiness, follow-on, or closeout text in the reviewed proposal, spec, architecture artifact, ADR, or plan.
- `material finding`: a review finding that changes or blocks tracked work, requires disposition, changes scope or risk, creates follow-up work, exposes process problems, or changes the review outcome.
- `PR comment promotion`: durable capture of a material maintainer PR comment through a review record so it can receive a stable Finding ID and review-resolution disposition.
- `isolated review request`: a direct or review-only review invocation that reports a review result without automatically continuing into downstream workflow stages.
- `tracked artifact`: any version-controlled repository file whose change will be committed or reviewed as part of the work.
- `shared review-skill recording subsection`: the identical `## Isolation and Recording` guidance copied into all formal review skills from `templates/shared/review-isolation-and-recording.md`.
- `recording status`: the review-output field that reports whether required review-recording artifacts were not required, recorded, or blocked.
- `recording blocker`: the review-output field that explains why required review-recording artifacts could not be created or updated.
- `status sync`: the review-output field that reports whether the reviewed artifact's durable lifecycle/status surface was not required, updated, or blocked.
- `status sync blocker`: the review-output field that explains why an expected artifact-status update could not be made.
- `status artifact`: the reviewed artifact whose lifecycle/status surface is updated by status sync.
- `clean or approving review result`: a review status that approves the reviewed artifact for its immediate next lifecycle state, including `approved`, `approve`, `clean`, and `clean-with-notes`.
- `artifact-status sync`: the act of updating only the reviewed artifact's owned lifecycle/status/readiness/closeout surface to match a clean or approving review result.

## Examples first

### Example E1: upstream material findings open a review-record root

Given `spec-review` returns material findings before `docs/changes/<change-id>/` exists
When the workflow-managed change will fix those findings
Then the contributor creates `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/spec-review-r1.md` before fixes proceed.

### Example E2: clean required review stays artifact-local

Given `proposal-review` is required
And it has no material findings
When the proposal records accepted status and a decision log entry
Then no empty detailed review file, `review-log.md`, or `review-resolution.md` is required solely for that clean review.

### Example E3: no-material non-approval review outcome

Given `plan-review` returns `rethink`
And it does not create material findings
When that outcome prevents downstream routing
Then a detailed `reviews/plan-review-r1.md` record is required.
And the required initial review-record root includes `change.yaml`, `review-log.md`, and `reviews/plan-review-r1.md`.
And `review-resolution.md` is not required solely for that no-material review event.

### Example E4: PR comment requires promotion before disposition

Given a maintainer PR comment identifies a material issue
When the issue requires disposition in `review-resolution.md`
Then the material finding first appears with a stable Finding ID in a durable review record, and `review-resolution.md` references that Finding ID.

### Example E5: change.yaml remains an aggregate summary

Given `review-log.md` and `review-resolution.md` exist
When `change.yaml` records review status
Then `review.status` and `review.unresolved_items` remain present, optional `review_log` and `review_resolution` pointers may appear, and detailed finding text stays out of `change.yaml`.

### Example E6: detailed review files are indexed exactly once

Given `docs/changes/<change-id>/reviews/spec-review-r1.md` exists
When structural validation reads `review-log.md`
Then that Review ID appears exactly once in a canonical review-log entry.

### Example E7: isolated material finding is recorded before edits

Given a direct `proposal-review` returns material finding `PR1`
And the contributor will revise the tracked proposal in response
When the contributor prepares the revision
Then the change creates `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/proposal-review-r1.md` before the proposal edit begins.

### Example E8: late isolated-review capture is reconstructed

Given a direct `spec-review` returns material finding `SR1`
And the contributor already began editing the tracked spec before creating a durable review record
When the contributor repairs the missing evidence
Then the detailed review file is labeled reconstructed and discloses source, timing, available evidence, stable Finding IDs, and known fidelity loss.

### Example E9: isolated review output names the recording obligation

Given an isolated `architecture-review` produces material findings
When the review output is reported
Then the output names no automatic downstream handoff, material Finding IDs, required review record path, whether the record must be created before fixing or reconstructed, and whether owner decision is needed.

### Example E10: formal review skills share identical recording guidance

Given the formal review skills are updated for this behavior
When validation compares their `## Isolation and Recording` sections
Then every copied section matches `templates/shared/review-isolation-and-recording.md` byte-for-byte, and stage-specific text appears only outside the shared block.

### Example E11: material finding output reports recording state

Given `proposal-review` reports material finding `PR1`
When the review output is final
Then `Recording status` is `recorded` if all required artifacts exist or were updated.
And `Review record`, `Review log`, and `Review resolution` name the required paths.

### Example E12: no-material detailed record has no empty resolution

Given `plan-review` returns `rethink` with no material findings
When a detailed review record is required because the outcome blocks downstream progress
Then `Recording status` is `recorded`.
And the output names the detailed review record and `review-log.md`.
And `review-resolution.md` is not required solely for that no-material review event.

### Example E13: clean proposal review synchronizes proposal status

Given `proposal-review` returns `approved`
And the reviewed proposal has `Status: draft`
And no instruction forbids edits
When the review completes
Then the proposal status is updated to `accepted`.
And the output reports `Status sync: updated` with the proposal path and status field.

### Example E14: no-edit isolated review blocks status sync

Given the user invokes isolated `spec-review` and says "do not modify files"
And the review returns `approved`
When the review completes
Then the spec is not edited.
And the output reports `Status sync: blocked`.
And `Status sync blocker` names the no-edit instruction and the manual action needed.

### Example E15: ambiguous status target blocks status sync

Given `architecture-review` approves an artifact whose lifecycle field is missing or ambiguous
When the next status cannot be chosen from this spec's status table or the artifact-local lifecycle field
Then the output reports `Status sync: blocked`.
And the review does not guess a status value.

### Example E16: code-review clean result updates plan-owned review state

Given `code-review` returns `clean-with-notes` for a planned milestone
When the active plan owns milestone review state
Then status sync updates the active plan milestone state according to the milestone contract.
And it does not edit source files solely to record code-review status.

## Requirements

R1. Formal review recording MUST be stage-neutral across `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.

R1a. A detailed review file's `Stage:` value MUST be one of the formal lifecycle review stages unless a later approved spec extends the allowed stage set.

R1b. A dedicated `pr-review` stage MUST NOT be treated as valid under this spec unless a later approved spec explicitly adds it and updates validation.

R2. A detailed review file MUST be created for a formal lifecycle review when any of the following is true:
- the review produces material findings;
- the review returns a stage-owned non-approval outcome that blocks downstream progress or requires revision;
- the review is reconstructed;
- the review findings will be cited as closeout evidence;
- a reviewer or maintainer explicitly requests a detailed record.

R2a. Stage-owned non-approval outcomes MUST include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent stage-specific outcomes that prevent downstream progress.

R2b. A clean formal review with no material findings MUST NOT require an empty detailed review file solely because the review was required.

R2c. Material findings MUST always be recorded.

R2d. All material findings require change-local review files.

R3. A required formal review with no material findings MAY be recorded through artifact-local settlement.

R3a. Artifact-local settlement MAY use the reviewed artifact's status, decision log, readiness, follow-on artifacts, or closeout section.

R3b. Artifact-local settlement MUST NOT replace detailed review records when any `R2` trigger applies.

R4. When a workflow-managed formal review triggers a detailed review file before a change-local root exists, the change MUST create an initial review-record root before review-driven fixes or downstream routing proceed.

R4a. The initial review-record root exists to preserve the review event and make it discoverable. It MUST NOT be treated as the final non-trivial change-local pack.

R4b. If material findings exist, the initial review-record root MUST include:
- `docs/changes/<change-id>/change.yaml`;
- `docs/changes/<change-id>/review-log.md`;
- `docs/changes/<change-id>/review-resolution.md`;
- `docs/changes/<change-id>/reviews/<stage>-r<n>.md`.

R4c. `review-resolution.md` is required in the initial review-record root when a detailed review file records material findings.

R4d. If `R2` requires a detailed review file for a no-material trigger, the initial review-record root MUST include:
- `docs/changes/<change-id>/change.yaml`;
- `docs/changes/<change-id>/review-log.md`;
- `docs/changes/<change-id>/reviews/<stage>-r<n>.md`.

R4e. `review-resolution.md` MUST NOT be created solely because `reviews/` exists. It is required when material findings exist or another approved review-resolution trigger applies.

R4f. The initial review-record root MUST preserve the first-pass review record before fixes or downstream routing proceed.

R4g. Final handoff for non-trivial work MUST still satisfy the baseline non-trivial pack, including durable Markdown reasoning such as `docs/changes/<change-id>/explain-change.md` or another approved durable reasoning surface.

R5. If a review is isolated or review-only and has no material findings, a detailed review file MAY be omitted unless another `R2` trigger applies.

R5a. If an isolated or review-only review has material findings, the isolated final output MUST identify the required change-local review files even though downstream handoff remains stopped.

R6. Material findings MUST be recorded before review-driven fixes proceed.

R6a. If fixes already began before the durable review record existed, the detailed review file MUST use the reconstructed-record rules from the review finding resolution contract.

R6b. Corrections, decisions, fixes, and validation evidence for material findings MUST be recorded in `review-resolution.md`, a later review round, or another explicit closeout artifact rather than by rewriting the first-pass detailed review file.

R7. A review finding MUST be treated as material when it:
- changes or blocks the reviewed proposal, spec, architecture, plan, code, tests, validation, or generated output;
- requires a disposition in `review-resolution.md`;
- changes scope, behavior, architecture, sequencing, proof strategy, or risk;
- creates follow-up action;
- exposes a workflow or process problem;
- is classified as blocker, major, or review-outcome-changing.

R7a. Minor copyedits, formatting nits, positive notes, and non-actionable observations MUST NOT require review-resolution disposition unless the reviewer explicitly marks them material.

R8. If `docs/changes/<change-id>/reviews/` exists, `docs/changes/<change-id>/review-log.md` MUST exist.

R8a. Every detailed review file under `reviews/` MUST contain exactly one stable `Review ID`.

R8b. Every detailed review file's `Review ID` MUST appear exactly once in `review-log.md`.

R8c. `review-log.md` MUST NOT contain ledger entries for Review IDs that lack matching detailed review files.

R9. Every material Finding ID dispositioned in `review-resolution.md` MUST originate in a durable review record.

R9a. `review-resolution.md` MUST NOT introduce new material Finding IDs that do not exist in a detailed review file.

R9b. `review-resolution.md` MUST contain an entry for every material Finding ID before review-driven fixes for those findings begin.

R10. `change.yaml.review` MUST keep the existing schema-required fields:
- `status`;
- `unresolved_items`.

R10a. `change.yaml.review` MAY include optional pointer fields such as:
- `review_log`;
- `review_resolution`.

R10b. `change.yaml` MUST NOT duplicate detailed review records, review transcripts, or detailed finding text.

R10c. `change.yaml.review` status values MAY use the current project vocabulary until a later approved schema change constrains the value set.

R11. Maintainer PR comments MUST NOT be automatically copied into `reviews/`.

R11a. A material maintainer PR comment that requires review-resolution disposition MUST first be promoted into a durable review record with a stable Finding ID.

R11b. The durable review record MAY be a formal lifecycle review record that cites the PR comment as evidence.

R11c. A dedicated `pr-review` detailed file MUST NOT be used unless a later approved spec explicitly adds `pr-review` to the allowed review-stage set and validator.

R12. A first-pass review outcome that requires revision, changes, or blocks downstream progress MUST be closed by a valid same-stage later review round or explicit reviewer or owner closeout evidence naming the original Review ID.

R12a. `review-resolution.md` alone MUST NOT silently replace required re-review or explicit closeout for blocking first-pass outcomes.

R13. `verify`, final `explain-change`, and `pr` handoff MUST NOT proceed while `review-log.md` lists open material findings or required `review-resolution.md` closeout remains open.

R14. This spec MUST preserve artifact-local source-of-truth boundaries.

R14a. Proposal status MUST remain in the proposal.

R14b. Spec status MUST remain in the spec.

R14c. Architecture and ADR status MUST remain in the architecture artifact or ADR.

R14d. Plan status MUST remain in the plan body and plan index where applicable.

R14e. Review files MUST preserve review event evidence and finding closeout, not final artifact settlement.

R15. Canonical review-stage skill guidance MUST describe the detailed review record triggers consistently when those skills are updated for this behavior.

R15a. If canonical skills shipped through generated adapters change, generated `.codex/skills/` and public adapter output MUST be regenerated and validated through existing repository-owned generation checks.

R16. Structural validation MUST continue to reject malformed detailed review records, missing `review-log.md`, duplicate or dangling Review IDs, material Finding IDs missing from required `review-resolution.md`, and `review-resolution.md` Finding IDs that do not exist in review records.

R16a. New validation for upstream stages SHOULD reuse the existing review-artifact validator instead of creating a second parser model.

R16b. Validation MUST NOT perform semantic review-quality judgment.

R17. Isolation MUST govern handoff only; recording MUST follow the finding.

R17a. A direct or review-only formal lifecycle review request MUST remain isolated by default and MUST NOT automatically continue into downstream workflow stages.

R17b. Isolation MUST NOT suppress material-finding recording.

R17c. A material finding MUST have a durable change-local review record under `docs/changes/<change-id>/reviews/` regardless of whether the review was workflow-managed or isolated.

R17d. If review-driven edits already began before the durable record exists, the detailed review file MUST be a reconstructed record and MUST disclose source, timing, available evidence, stable Finding IDs, and known fidelity loss.

R17e. A revision made in response to a material finding remains incomplete until the finding is durably recorded, even when the record was created late and reconstructed.

R18. A tracked artifact MUST be any version-controlled repository file whose change will be committed or reviewed as part of the work.

R18a. Tracked artifacts include lifecycle artifacts, governance files, workflow summaries, skills, specs, schemas, scripts, generated outputs, README content, and change-local artifacts.

R18b. Ephemeral chat output, local scratch files, and unversioned drafts MUST NOT be treated as tracked artifact edits.

R19. For review recording decisions, a finding MUST be treated as material when it changes or blocks a tracked artifact edit, changes scope, changes requirements, changes architecture, changes sequencing, changes validation, creates follow-up work, or requires disposition, unless the reviewer explicitly records a non-material rationale.

R19a. `CONSTITUTION.md` remains authoritative for materiality; the operational shortcut in `R19` MUST NOT narrow or replace higher-priority materiality rules.

R20. For an isolated or review-only formal review with material findings, the final review output MUST state that isolation stops downstream handoff but does not suppress recording.

R20a. The output MUST state:
- no automatic downstream handoff;
- material Finding IDs;
- required review record path;
- whether the record must be created before fixing or reconstructed;
- whether owner decision is needed.

R20b. The output MUST make the next action clear without requiring enum-style action strings.

R20c. The output MUST NOT offer review-output-only or artifact-local-only settlement for material findings.

R21. Canonical formal review skills MUST include one identical `## Isolation and Recording` subsection copied from `templates/shared/review-isolation-and-recording.md`.

R21a. The shared subsection MUST appear in `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.

R21b. Stage-specific guidance MAY appear above or below the shared subsection, but MUST NOT appear inside the shared subsection.

R21c. `code-review` MUST adopt the shared isolation-versus-recording rule without an additive code-review-specific layer for this concern.

R21d. Static validation MUST compare each copied skill subsection against `templates/shared/review-isolation-and-recording.md` byte-for-byte from the `## Isolation and Recording` heading up to, but not including, the next `##` heading.

R22. This spec's material-finding trigger MUST NOT be implemented until affected governance and operating guidance are updated or explicitly marked unaffected with rationale.

R22a. The implementation MUST update or explicitly mark unaffected `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md`.

R22b. Those surfaces MUST use the same rule: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.

R23. First-slice validation for this clarification MUST remain structural. It MUST NOT add semantic flagging for tracked artifact edits that reference unresolved review findings.

R24. Formal review output MUST distinguish:
- the review verdict;
- recording status;
- artifact-status sync state.

R24a. Review verdicts MUST NOT be used as a substitute for recording status or artifact-status sync state.

R24b. Recording status and status sync MUST NOT be used as substitutes for the review verdict.

R25. Formal review output MUST include `Recording status` using exactly one of:
- `not-required`;
- `recorded`;
- `blocked`.

R25a. `Recording status: not-required` means no material findings exist and no detailed-record trigger applies.

R25b. `Recording status: recorded` means every artifact required by the active recording trigger exists or was updated.

R25c. `Recording status: blocked` means required review-recording artifacts could not be created or updated.

R25d. If `Recording status` is `blocked`, review output MUST include `Recording blocker`.

R25e. `Recording blocker` MUST name the blocker and the smallest action needed to create or update the required recording artifacts.

R26. For material findings, `Recording status: recorded` MUST require:
- a detailed review record;
- `review-log.md`;
- `review-resolution.md`.

R26a. For no-material detailed-record triggers, `Recording status: recorded` MUST require:
- a detailed review record;
- `review-log.md`.

R26b. `review-resolution.md` MUST be required only when material findings exist or another approved review-resolution trigger applies.

R27. Formal review output that records material findings MUST preserve complete material-finding shape:
- Finding ID;
- Severity;
- Location;
- Evidence;
- Required outcome;
- Safe resolution path or `needs-decision` rationale.

R27a. `Location` MUST be specific enough for a future reader to find the affected surface without chat history.

R27b. `Location` MAY be a file path and section, file path and line or range, artifact and milestone or requirement ID, missing expected artifact path, or review surface plus not-present rationale for absence-based findings.

R28. When recording is required and no active change root is obvious, review skills MUST choose the change ID in this order:
1. active `docs/changes/<change-id>/change.yaml`, when the reviewed work already has a change root;
2. active plan or reviewed artifact metadata, when it names the change ID;
3. user-provided change ID;
4. generated review-recording change ID in the form `YYYY-MM-DD-<reviewed-artifact-or-topic>-review-recording`.

R28a. If the change ID remains ambiguous after this order, review output MUST use `Recording status: blocked`.

R29. Formal review output MUST include `Status sync` using exactly one of:
- `not-required`;
- `updated`;
- `blocked`.

R29a. `Status sync: not-required` means the review outcome is not approving or clean, or no lifecycle status change is expected for that review result.

R29b. `Status sync: updated` means the reviewed artifact's owned lifecycle/status/readiness/closeout surface was updated to the next artifact-specific state.

R29c. `Status sync: blocked` means an approving or clean review result expected an artifact-status update, but the update could not be made.

R29d. If `Status sync` is `blocked`, review output MUST include `Status sync blocker`.

R29e. `Status sync blocker` MUST name the intended next status, the blocker, and the smallest manual action needed.

R29f. If `Status sync` is `updated`, review output MUST include the status artifact path and the exact status field or section changed.

R30. For clean or approving formal review results, review skills MUST update the reviewed artifact's owned lifecycle/status/readiness/closeout surface when the target is clear and edits are allowed; otherwise they MUST report `Status sync: blocked`.

R30a. Status sync MUST NOT be treated as downstream workflow continuation.

R30b. Explicit user instructions that forbid file edits MUST block status sync.

R30c. When edits are forbidden, review output MUST use `Status sync: blocked` and MUST name the manual status update needed.

R30d. Review skills MUST NOT edit reviewed artifact content beyond the minimal lifecycle/status/readiness/follow-on/closeout fields needed to make the clean review result durable.

R31. Artifact-status sync MUST use these artifact-specific targets:

| Review skill | Clean or approving review result | Status sync target |
|---|---|---|
| `proposal-review` | `approved` | proposal `Status: accepted` |
| `spec-review` | `approved` | spec `Status: approved` |
| `architecture-review` | `approved` for architecture package | architecture `Status: approved` |
| `architecture-review` | `approved` for ADR | ADR `Status: accepted` or `Status: active`, according to the ADR's existing lifecycle field |
| `plan-review` | `approve` | plan review/readiness section says ready for `test-spec`; `docs/plan.md` index updated only if the index owns active-plan state |
| `code-review` | `clean` or `clean-with-notes` | active plan milestone state updated according to the milestone contract; no source artifact status edit unless the reviewed artifact explicitly owns that state |

R31a. If the next status cannot be chosen from the table or an artifact-local lifecycle field, review output MUST use `Status sync: blocked`.

R31b. Status sync MUST preserve artifact-specific lifecycle vocabulary unless a later approved spec changes that vocabulary.

R32. Formal review skill final output MUST include this status shape or equivalent labeled fields:
- Skill;
- Review status;
- Material findings;
- Recording status;
- Recording blocker;
- Status sync;
- Status artifact;
- Status sync blocker;
- Review record;
- Review log;
- Review resolution;
- Open blockers;
- Immediate next stage.

R32a. `Recording blocker` MAY be empty or `not applicable` unless `Recording status` is `blocked`.

R32b. `Status sync blocker` MAY be empty or `not applicable` unless `Status sync` is `blocked`.

R33. Canonical review-stage skill guidance MUST describe recording status and status sync consistently when those skills are updated for this behavior.

R33a. If canonical skills shipped through generated adapters change for recording status or status sync, generated `.codex/skills/` and public adapter output MUST be regenerated and validated through existing repository-owned generation checks.

## Inputs and outputs

Inputs:

- formal lifecycle review output;
- isolated formal lifecycle review output;
- explicit user edit-permission instructions for isolated or review-only requests;
- reviewed proposal, spec, architecture artifact, ADR, plan, code, tests, validation, or generated output;
- tracked artifacts that will be committed or reviewed as part of the work;
- existing `docs/changes/<change-id>/` root when present;
- maintainer PR comments when they are promoted as evidence;
- `change.yaml`, `review-log.md`, `review-resolution.md`, and detailed review files when they exist.

Outputs:

- artifact-local settlement for clean required reviews;
- formal review output fields for review verdict, recording status, recording blocker, status sync, status artifact, and status sync blocker;
- detailed review files for triggered formal lifecycle reviews;
- initial review-record root when an `R2` trigger requires a detailed review file before a change-local root exists;
- review-log entries indexing detailed review files;
- review-resolution entries for material Finding IDs;
- aggregate `change.yaml.review` status and optional pointers.
- shared formal review skill guidance from `templates/shared/review-isolation-and-recording.md`.
- artifact-status updates to the reviewed artifact's owned lifecycle/status/readiness/closeout surface when a clean or approving review result requires status sync.

## State and invariants

- Formal lifecycle review recording is stage-neutral.
- Isolation affects downstream handoff only and does not affect material-finding recording obligations.
- Clean reviews stay lightweight unless a detailed-record trigger applies.
- Material findings are recorded in change-local review files.
- Material isolated-review findings require change-local review files even when downstream handoff remains stopped.
- Review-log entries and detailed review files remain in one-to-one Review ID correspondence.
- Material Finding IDs originate in review records before they are dispositioned.
- `change.yaml.review.status` and `change.yaml.review.unresolved_items` remain present.
- Final artifact status remains artifact-local.
- Clean or approving review results do not leave the reviewed artifact's owned lifecycle/status surface stale when the status owner is clear and edits are allowed.
- Status sync changes only the reviewed artifact's lifecycle/status/readiness/closeout surface and does not imply downstream workflow continuation.
- Explicit no-edit instructions block status sync even when the review result is clean or approving.
- Review files do not become proposal, spec, architecture, ADR, or plan sources of truth.
- The final non-trivial change-local pack includes durable Markdown reasoning even when an initial review-record root was created earlier.
- The shared review-skill recording subsection remains byte-identical across formal review skills.

## Error and boundary behavior

- If a required detailed review file is missing, review-driven fixes or downstream routing must stop until the review evidence is created or reconstructed.
- If material findings are acted on before durable review records exist, the repair path is a reconstructed detailed review record.
- If an isolated material review finding lacks required change-local review files, review-driven edits and downstream routing must stop until the durable review record exists.
- If an isolated review output with material findings omits the required review record path, whether the record must be created before fixing or reconstructed, or whether owner decision is needed, the review output is incomplete and must be revised before fixes or downstream routing proceed.
- If a copied `## Isolation and Recording` skill subsection differs from the canonical template, static validation fails.
- If stage-specific text appears inside the shared subsection, static validation fails.
- If `reviews/` exists without `review-log.md`, structural validation fails.
- If a detailed review file has zero or multiple Review IDs, structural validation fails.
- If a Review ID is missing from or duplicated in `review-log.md`, structural validation fails.
- If `review-resolution.md` references a Finding ID absent from review records, structural validation fails.
- If a clean review is recorded only through artifact-local settlement, no `review-log.md` or `review-resolution.md` is required solely for that review.
- If a PR comment is material but has no durable review record, it cannot be dispositioned in `review-resolution.md`.
- If a dedicated `pr-review` file appears before the allowed stage set is extended, validation must treat it as unsupported.
- If a no-material `R2` trigger requires a detailed review file before a change-local root exists, the initial review-record root needs `change.yaml`, `review-log.md`, and the detailed review file, but not an empty `review-resolution.md`.
- If a non-trivial change reaches final handoff without durable Markdown reasoning, final handoff is incomplete even if the initial review-record root exists.
- If `Recording status` is `blocked` and `Recording blocker` is missing, review output is incomplete.
- If `Status sync` is `blocked` and `Status sync blocker` is missing, review output is incomplete.
- If a clean or approving review result has a clear status sync target and edits are allowed, leaving the status artifact stale makes review output incomplete.
- If explicit no-edit instructions are present, status sync must not edit files and must instead report `Status sync: blocked`.
- If a status sync target cannot be chosen from `R31` or an artifact-local lifecycle field, review output must report `Status sync: blocked` rather than guessing.
- If status sync for `code-review` would require editing source files only to record review status, the review output must report a status-sync blocker or use the active plan/review-owned surface instead.

## Compatibility and migration

- Existing historical change packs do not require migration unless touched, generated, or relied on as current authoritative guidance.
- Existing clean review settlements in proposal, spec, architecture, ADR, or plan artifacts remain valid historical evidence when no detailed-record trigger applied.
- Existing validator support for `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` remains the target stage set.
- This spec does not require a `change.yaml` schema change because additional `review` pointer fields are optional under the current permissive object shape.
- This spec does not require a new artifact status vocabulary. It preserves existing artifact-specific settlement states unless a later approved spec changes them.
- Existing review outputs do not need retroactive status-sync fields unless touched, regenerated, or relied on as current authoritative guidance.
- Rollback may remove the new trigger guidance while keeping already-authored upstream review records as valid historical artifacts.
- Existing historical review skills and generated adapter output do not need migration until the implementation slice updates canonical skill behavior.

## Observability

- Reviewers can find detailed formal review records through `review-log.md`.
- Reviewers can tell from `change.yaml.review.unresolved_items`, `review-log.md`, and `review-resolution.md` whether material findings remain open.
- Reviewers can distinguish artifact-local settlement from detailed review-event evidence.
- Reviewers can tell from isolated review output whether downstream continuation stopped and what durable recording action is required before fixes.
- Reviewers can tell from formal review output whether required recording artifacts were not required, recorded, or blocked.
- Reviewers can tell from formal review output whether artifact-status sync was not required, updated, or blocked.
- Reviewers can distinguish recording blockers from status-sync blockers.
- Validation output should identify malformed review artifact paths and relationship failures.

## Security and privacy

- Review records, `review-log.md`, `review-resolution.md`, and `change.yaml` MUST NOT include secrets, credentials, private keys, or sensitive runtime values from review evidence.
- PR comment promotion MUST preserve only the evidence needed for review closeout and MUST NOT copy sensitive context unnecessarily.
- Structural validation MUST NOT require network access or repository secrets.

## Accessibility and UX

No UI behavior is introduced.

Review artifacts SHOULD use stable labels and concise sections so contributors can scan Review IDs, Finding IDs, status, and closeout without reading transcripts.

The shared review-skill recording subsection SHOULD be short enough to remain readable inside each formal review skill without requiring a spec lookup mid-review.

## Performance expectations

Review artifact validation SHOULD remain lightweight enough for targeted local validation and CI.

This spec MUST NOT require broad smoke solely because upstream review records exist.

## Edge cases

1. A clean required `proposal-review` can settle through proposal status and decision log without creating review files.
2. A clean required `spec-review` can settle through spec readiness when no detailed-record trigger applies.
3. A `plan-review` with `rethink` creates a detailed review file and a no-material initial review-record root because the outcome blocks downstream progress.
4. A material `architecture-review` finding before any change-local root creates an initial review-record root with `review-resolution.md` before design fixes proceed.
5. An isolated review-only material finding requires change-local review files even when no tracked change proceeds.
6. If the same isolated finding later drives tracked changes, the tracked change relies on the existing durable evidence or reconstructs it if it was created late.
7. A material PR comment cannot be added directly to `review-resolution.md`; it needs a durable review record first.
8. A `pr-review-r1.md` file remains unsupported unless a later spec extends the formal stage set.
9. `change.yaml.review` may include `review_log` and `review_resolution`, but it still requires `status` and `unresolved_items`.
10. A detailed review file with no material findings still needs `review-log.md` if it was created because a reviewer explicitly requested it.
11. A detailed review file created only for reconstructed evidence must include reconstructed-record metadata under the review finding resolution contract.
12. A final PR-ready handoff is incomplete if only the initial review-record root exists and durable Markdown reasoning was never added.
13. A direct `proposal-review` material finding that will revise a tracked proposal creates durable review evidence before the proposal edit begins.
14. A direct `spec-review` material finding that already drove spec edits before recording is repaired only through a reconstructed detailed review file.
15. A material isolated review output that omits Finding IDs, required record path, record-before-fixing or reconstruction status, or owner-decision status is incomplete.
16. A skill-specific paragraph inserted inside the shared `## Isolation and Recording` block fails static validation.
17. A tracked generated adapter file changed because of a material review finding is a tracked artifact edit.
18. A clean `proposal-review` changes proposal `Status: draft` to `Status: accepted` when edits are allowed.
19. A clean `spec-review` changes spec `Status: draft` to `Status: approved` when edits are allowed.
20. A clean `architecture-review` for an ADR with an existing `Status` field chooses `accepted` or `active` from the ADR's artifact-local lifecycle field, not from review status wording alone.
21. A `plan-review` approval updates plan readiness text and the plan index only when those surfaces own the reviewed plan state.
22. A `code-review` clean result updates active plan or review-owned milestone state but does not edit source code solely to record review status.
23. A review-only request with explicit no-edit instructions reports `Status sync: blocked` instead of updating the artifact.
24. A formal review output can have `Recording status: not-required` and `Status sync: updated` for a clean approval.
25. A formal review output can have `Recording status: recorded` and `Status sync: blocked` when material findings were recorded but an expected status update was forbidden.

## Non-goals

- Creating separate review directories per stage.
- Requiring detailed review files for every clean review.
- Automatically copying maintainer PR comments into review records.
- Adding `pr-review` to the supported formal review-stage set in this spec.
- Replacing artifact-local status for proposals, specs, architecture artifacts, ADRs, or plans.
- Replacing `review-resolution.md` with `change.yaml`.
- Automating semantic review-quality judgment.
- Adding semantic validator detection for tracked artifact edits that mention unresolved review findings in the first slice.
- Generating formal review skill shared subsections instead of manually copying a canonical block.
- Migrating historical review packs that are not otherwise touched.
- Changing artifact-specific lifecycle vocabulary such as proposal `accepted` or spec `approved`.
- Treating status sync as permission to continue into downstream authoring, implementation, verify, or PR stages.
- Editing reviewed artifact content beyond lifecycle/status/readiness/follow-on/closeout fields.
- Requiring status sync when user instructions explicitly forbid file edits.

## Acceptance criteria

- A contributor can tell which formal lifecycle review outcomes require a detailed review file.
- A contributor can record a clean required review without creating empty review artifacts.
- A contributor can open an initial review-record root before fixing upstream material findings.
- A contributor can open an initial review-record root for a no-material non-approval review without creating an empty `review-resolution.md`.
- A reviewer can trace every material Finding ID from detailed review record to `review-resolution.md`.
- A reviewer can verify that `change.yaml.review` keeps `status` and `unresolved_items`.
- A reviewer can distinguish the initial review-record root from the final non-trivial change-local pack.
- A material PR comment cannot be dispositioned without first being captured in a durable review record.
- Existing review-artifact validation remains the structural proof path for review files.
- Final handoff blocks when open review findings, open review-resolution closeout, or missing durable Markdown reasoning remain.
- Isolation and recording are distinguishable: direct review requests stop downstream handoff but still record material findings.
- Important material findings are always recorded, and all material findings require change-local review files.
- A contributor can identify what counts as a tracked artifact for recording-trigger purposes.
- Isolated review outputs with material findings expose Finding IDs, required review record path, record-before-fixing or reconstruction status, and owner-decision status.
- `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` teach the same rule: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
- Formal review skills contain a byte-identical `## Isolation and Recording` block from a canonical template.
- Formal review output separates review status, recording status, and status sync.
- Formal review output includes `Recording blocker` when recording is blocked.
- Formal review output includes `Status sync blocker` when status sync is blocked.
- A clean or approving review result updates the reviewed artifact's status surface when the target is clear and edits are allowed.
- A clean or approving review result reports `Status sync: blocked` when the target is ambiguous or edits are forbidden.
- Artifact-status sync uses the artifact-specific status table and does not guess outside the table or artifact-local lifecycle fields.

## Open questions

- None.

## Next artifacts

- Implementation M1 under the active review skill material-finding recording plan.
- Spec-review for this recording/status-sync amendment.
- Test-spec update for formal review output recording and artifact-status sync.
- Execution plan update with M1 recording-status guardrail and M2 artifact-status sync guardrail.
- `code-review` after implementation milestones complete.
- `verify`.
- `explain-change`.
- `pr`.

## Follow-on artifacts

- Plan: [Formal Review Recording plan](../docs/plans/2026-05-04-formal-review-recording.md)
- Test spec: [Formal Review Recording test spec](formal-review-recording.test.md)
- Proposal amendment: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- Spec-review: approved on 2026-05-07 with no material findings.
- Execution plan: [Review Skill Material Finding Recording plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md)
- Plan-review: approved on 2026-05-07 with no material findings.
- Test spec: [Formal Review Recording test spec](formal-review-recording.test.md) updated for the review skill material-finding recording amendment.
- Proposal amendment: [Review Skill Recording and Status Output Guardrail](../docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md)
- Learn session: [Review Approval Status Sync](../docs/learn/sessions/2026-05-12-review-approval-status-sync.md)
- Spec-review R1: changes requested with material finding `SR1`, accepted and closed after `R30` revision.
- Spec-review R2: approved with no material findings.

## Readiness

Approved amendment for formal review output recording and artifact-status sync. Ready for test-spec update and execution planning.
