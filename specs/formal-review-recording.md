# Formal Review Recording

## Status

- draft

## Related proposal

- [Formal Review Recording](../docs/proposals/2026-05-04-formal-review-recording.md)
- [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- [Review Recording Guardrail and Downstream Status Settlement](../docs/proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md)

## Goal and context

This spec defines when formal lifecycle reviews create durable change-local review records, how upstream review findings are preserved before fixes, and how review evidence stays separate from proposal, spec, architecture, and plan status.

The repository already has a review artifact model under `docs/changes/<change-id>/reviews/`, `review-log.md`, and `review-resolution.md`. The gap is the trigger policy for stages before `code-review`: `proposal-review`, `spec-review`, `architecture-review`, and `plan-review`.

The goal is stage-neutral recording for material review findings without forcing detailed files for every clean review.

This amendment clarifies that isolated review handoff behavior and material-finding recording are independent. A direct or review-only review remains isolated by default, but every material finding still requires durable change-local review evidence.

This 2026-05-12 draft amendment makes the recording obligation operational in formal review skill output. It requires formal review skills to report whether required review-recording artifacts were created, were not required, or were blocked; it requires complete material-finding shape including `Location`; and it keeps examples under `docs/examples/` instead of active lifecycle directories. It intentionally does not implement downstream upstream-status settlement in this first slice.

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
- `recording status`: the formal review output field that reports whether required review-recording artifacts were not required, recorded, or blocked.
- `complete material-finding shape`: the minimum fields needed for a future reader to understand a material finding without chat history.
- `Location`: the material-finding field that identifies the affected file, section, line, artifact, missing artifact, or other specific review surface.
- `examples surface`: `docs/examples/**`, the non-normative directory for illustrative artifact examples that must not be treated as active lifecycle state.

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

### Example E11: material review output records before final response

Given `plan-review` produces material finding `PR-001`
When the review output is ready to return
Then the review creates or updates the required change-local review record, `review-log.md`, and `review-resolution.md`
And the final output reports `Recording status: recorded` and the artifact paths.

### Example E12: blocked recording is explicit

Given `proposal-review` produces a material finding
And the change ID cannot be selected from the active change root, reviewed artifact metadata, user input, or deterministic fallback rule
When the review output is returned
Then the output reports `Recording status: blocked`
And it includes the `Recording blocker` and the smallest action needed to create the record.

### Example E13: material findings include Location

Given `spec-review` reports a material finding about missing testability requirements
When the finding is recorded
Then the finding includes `Location` pointing to the affected spec section or to the missing expected artifact path with a not-present rationale.

### Example E14: examples are not active lifecycle state

Given an illustrative plan example exists
When the repository lists active plans or validates current lifecycle state
Then `docs/examples/plans/example-plan.md` is not treated as an active plan.

### Example E15: no review-side artifact-status sync field

Given `proposal-review` returns a clean approval
When the review output is generated
Then the output may settle the proposal artifact-local status only when no detailed-record trigger applies under the existing clean-review rule
And it does not add `Status sync`, `Status artifact`, or `Status sync blocker` fields to the review result.

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

R24. Formal review skill output MUST include a `Recording status` field.

R24a. `Recording status` MUST use exactly one of:
- `not-required`;
- `recorded`;
- `blocked`.

R24b. `not-required` MUST mean no material findings and no detailed-record trigger.

R24c. `recorded` MUST mean every artifact required by the active recording trigger exists or was updated.

R24d. `blocked` MUST mean required review-recording artifacts could not be created or updated.

R24e. `Recording status` MUST NOT be treated as the review verdict.

R25. Formal review skill output MUST include review-recording artifact path fields:
- `Review record`;
- `Review log`;
- `Review resolution`.

R25a. `Review resolution` MUST be reported as a path, `not-required`, or `blocked`.

R25b. If `Recording status: blocked`, the output MUST include `Recording blocker` and the smallest action needed to create or update the required artifacts.

R26. For material findings, `Recording status: recorded` MUST require:
- a detailed review record;
- `review-log.md`;
- `review-resolution.md`.

R26a. For no-material detailed-record triggers, `Recording status: recorded` MUST require:
- a detailed review record;
- `review-log.md`.

R26b. A no-material detailed-record trigger MUST NOT require an empty `review-resolution.md` unless another approved review-resolution trigger applies.

R27. Every material finding in formal review output or a durable review record MUST include complete material-finding shape:
- Finding ID;
- Severity;
- Location;
- Evidence;
- Required outcome;
- Safe resolution path, or `needs-decision` rationale.

R27a. `Location` MAY be a file path and section, file path and line or range, artifact and milestone or requirement ID, missing expected artifact path, or review surface with a not-present rationale.

R27b. `Location` MUST be specific enough that a future reader can find the affected surface without chat history.

R28. Formal review skills MUST NOT merely tell the user that required review artifacts should be created when recording is required.

R28a. The review skill MUST create or update the required review-recording artifacts before final output, or report `Recording status: blocked`.

R29. Formal review skills MUST include concise recording-status guidance covering:
- `Recording status`;
- `not-required`;
- `recorded`;
- `blocked`;
- material-finding artifact requirements;
- no-material detailed-record artifact requirements;
- `Recording blocker`;
- complete material-finding shape;
- the rule not to merely tell the user to create review artifacts.

R29a. Static skill validation MUST cover the stable terms required by `R29`.

R29b. Static validation MAY use exact negative field checks to prevent standardized review-side artifact-status sync fields in formal review skills.

R30. Formal review skills MUST NOT include standardized review-side artifact-status sync fields for this amendment.

R30a. The disallowed standardized fields are:
- `Status settlement recommendation`;
- `Status sync`;
- `Status artifact`;
- `Status sync blocker`.

R30b. Formal review skills MAY mention stale lifecycle status only as a normal review finding, concern, or note when it affects the reviewed surface.

R31. Normative change-ID selection, `Location`, and detailed recording artifact rules MUST live in this spec or a linked formal review recording reference.

R31a. Formal review skills MUST NOT duplicate long change-ID algorithms or long `Location` example sets.

R31b. Full illustrative examples for change-ID selection and material-finding `Location` SHOULD live under `docs/examples/formal-review-recording/`.

R32. `docs/examples/**` MUST be treated as a non-normative examples surface.

R32a. `docs/examples/README.md` MUST state that examples are illustrative, non-normative, and not active lifecycle artifacts.

R32b. The plan example SHOULD move from `docs/plans/0000-00-00-example-plan.md` to `docs/examples/plans/example-plan.md`.

R32c. The shipped skill-validator example change pack SHOULD move from `docs/changes/0001-skill-validator/` to `docs/examples/changes/skill-validator/`.

R32d. If the shipped skill-validator example change pack is not moved in the first implementation slice, the implementation MUST record explicit fixture-coupling rationale in a tracked or review-visible surface.

R32e. Tests, validators, selectors, and guidance that reference moved examples MUST be updated in the same slice as the move.

R32f. Lifecycle validation and selector behavior MUST NOT treat `docs/examples/**` as active lifecycle state.

R33. The first implementation slice for this amendment MUST NOT update downstream authoring or execution skills for upstream status settlement.

R33a. Downstream status settlement before reliance MAY be specified in a follow-up proposal, plan, or later milestone.

R33b. If downstream status settlement is specified later, downstream skill execution MAY imply permission for minimal upstream lifecycle/status settlement before reliance, but that behavior is outside this amendment's first implementation slice.

## Inputs and outputs

Inputs:

- formal lifecycle review output;
- isolated formal lifecycle review output;
- formal review skill result output;
- reviewed proposal, spec, architecture artifact, ADR, plan, code, tests, validation, or generated output;
- tracked artifacts that will be committed or reviewed as part of the work;
- existing `docs/changes/<change-id>/` root when present;
- change ID sources such as active change roots, reviewed artifact metadata, user-provided IDs, or deterministic fallback IDs;
- maintainer PR comments when they are promoted as evidence;
- `change.yaml`, `review-log.md`, `review-resolution.md`, and detailed review files when they exist.
- example artifact files under active lifecycle directories or `docs/examples/**`.

Outputs:

- artifact-local settlement for clean required reviews;
- detailed review files for triggered formal lifecycle reviews;
- initial review-record root when an `R2` trigger requires a detailed review file before a change-local root exists;
- review-log entries indexing detailed review files;
- review-resolution entries for material Finding IDs;
- aggregate `change.yaml.review` status and optional pointers;
- formal review output that reports `Recording status`, review artifact paths, and blockers when applicable;
- shared formal review skill guidance from `templates/shared/review-isolation-and-recording.md`;
- non-normative examples under `docs/examples/**`.

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
- Review files do not become proposal, spec, architecture, ADR, or plan sources of truth.
- The final non-trivial change-local pack includes durable Markdown reasoning even when an initial review-record root was created earlier.
- The shared review-skill recording subsection remains byte-identical across formal review skills.
- `Recording status` reports recording completion only and does not replace the review verdict.
- Material findings preserve complete material-finding shape, including `Location`.
- Normative review-recording rules live in specs or linked references, while examples live in `docs/examples/**`.
- `docs/examples/**` is never active lifecycle state.
- The first implementation slice does not change downstream skill upstream-status settlement behavior.

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
- If a formal review produces material findings but returns without `Recording status: recorded` or `Recording status: blocked`, the review output is incomplete.
- If a material finding omits `Location`, the finding is incomplete and cannot be treated as durably recorded.
- If required recording artifacts cannot be created or updated, the review output must use `Recording status: blocked` and name the blocking condition.
- If a formal review skill adds standardized `Status sync`-style fields in this amendment's first slice, static validation should fail.
- If a selector or lifecycle validator treats `docs/examples/**` as current lifecycle state, validation behavior is wrong for this amendment.

## Compatibility and migration

- Existing historical change packs do not require migration unless touched, generated, or relied on as current authoritative guidance.
- Existing clean review settlements in proposal, spec, architecture, ADR, or plan artifacts remain valid historical evidence when no detailed-record trigger applied.
- Existing validator support for `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review` remains the target stage set.
- This spec does not require a `change.yaml` schema change because additional `review` pointer fields are optional under the current permissive object shape.
- Rollback may remove the new trigger guidance while keeping already-authored upstream review records as valid historical artifacts.
- Existing historical review skills and generated adapter output do not need migration until the implementation slice updates canonical skill behavior.
- Moving examples out of active lifecycle directories is a path migration for illustrative fixtures only; it must update tests, selectors, validators, and guidance that reference those paths.
- If `docs/changes/0001-skill-validator/` is retained temporarily because validator fixtures still depend on it, the implementation must record explicit rationale and follow-up ownership.

## Observability

- Reviewers can find detailed formal review records through `review-log.md`.
- Reviewers can tell from `change.yaml.review.unresolved_items`, `review-log.md`, and `review-resolution.md` whether material findings remain open.
- Reviewers can distinguish artifact-local settlement from detailed review-event evidence.
- Reviewers can tell from isolated review output whether downstream continuation stopped and what durable recording action is required before fixes.
- Reviewers can tell from formal review output whether review recording was not required, completed, or blocked.
- Reviewers can find illustrative examples under `docs/examples/**` without confusing them for current project state.
- Validation output should identify malformed review artifact paths and relationship failures.

## Security and privacy

- Review records, `review-log.md`, `review-resolution.md`, and `change.yaml` MUST NOT include secrets, credentials, private keys, or sensitive runtime values from review evidence.
- PR comment promotion MUST preserve only the evidence needed for review closeout and MUST NOT copy sensitive context unnecessarily.
- Example files under `docs/examples/**` MUST NOT include real secrets, credentials, private keys, or sensitive runtime values.
- Structural validation MUST NOT require network access or repository secrets.

## Accessibility and UX

No UI behavior is introduced.

Review artifacts SHOULD use stable labels and concise sections so contributors can scan Review IDs, Finding IDs, status, and closeout without reading transcripts.

The shared review-skill recording subsection SHOULD be short enough to remain readable inside each formal review skill without requiring a spec lookup mid-review.

Formal review skills SHOULD keep the recording-status block concise and link or point to the project review-recording process instead of embedding long example sets.

## Performance expectations

Review artifact validation SHOULD remain lightweight enough for targeted local validation and CI.

This spec MUST NOT require broad smoke solely because upstream review records exist.

Moving examples to `docs/examples/**` MUST NOT make selector or lifecycle validation scan active lifecycle directories more broadly than before.

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
18. A formal review output reports material findings but no `Recording status`; the output is incomplete.
19. A formal review output reports `Recording status: recorded`, but the required review record path does not exist; the output is false and validation or review must block.
20. A material finding names evidence and required outcome but omits `Location`; the finding is incomplete.
21. A material finding concerns an absent artifact; `Location` points to the missing expected artifact path or review surface with a not-present rationale.
22. A no-material detailed-record trigger reports `Review resolution: not-required`.
23. A formal review skill contains a standardized `Status sync:` field in the first slice; static validation fails.
24. A selector lists `docs/examples/plans/example-plan.md` as an active plan; selector behavior is wrong.
25. `docs/changes/0001-skill-validator/` cannot move in the first slice because a validator fixture path still depends on it; the implementation records explicit rationale and follow-up ownership.

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
- Implementing downstream upstream-status settlement in the first slice.
- Adding standardized review-side artifact-status sync result fields.
- Treating `docs/examples/**` as active lifecycle state.
- Rewriting substantive artifact content when moving illustrative examples.

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
- Formal review skills expose `Recording status` with only `not-required`, `recorded`, and `blocked`.
- Formal review output distinguishes `Recording status` from the review verdict.
- Material review findings include Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or `needs-decision` rationale.
- Material findings require review record, `review-log.md`, and `review-resolution.md` paths when recorded.
- No-material detailed-record triggers report `Review resolution: not-required` instead of creating an empty `review-resolution.md`.
- Formal review skills do not include standardized `Status sync`, `Status artifact`, `Status sync blocker`, or `Status settlement recommendation` fields.
- Normative change-ID and `Location` rules live in this spec or a linked formal review recording reference.
- Full illustrative examples live under `docs/examples/**`.
- `docs/examples/README.md` states examples are non-normative and not active lifecycle artifacts.
- The plan example is moved to `docs/examples/plans/example-plan.md`.
- The shipped skill-validator example change pack is moved to `docs/examples/changes/skill-validator/` or retained with explicit fixture-coupling rationale.
- Selectors and lifecycle validation do not treat `docs/examples/**` as active lifecycle state.
- Downstream upstream-status settlement is not implemented in the first slice.

## Open questions

- Whether the full change-ID and `Location` rules should stay directly in this spec or move to a small linked formal review recording reference. This does not block spec review because the owning surface requirement is defined.
- Whether `docs/changes/0001-skill-validator/` can move in the first implementation slice or must be retained temporarily with fixture-coupling rationale. This does not block spec review because both acceptable outcomes are defined.
- Which downstream status-settlement questions should be answered in a follow-up proposal versus a later implementation plan. This does not block spec review because downstream settlement is excluded from the first implementation slice.

## Next artifacts

- Spec-review for this 2026-05-12 draft amendment.
- Implementation plan for review recording output guardrail and examples cleanup.
- Test-spec update or review for this amendment.
- Review skill and static validator updates.
- Generated skill and adapter refresh.
- Optional downstream status-settlement follow-up proposal.

## Follow-on artifacts

- Plan: [Formal Review Recording plan](../docs/plans/2026-05-04-formal-review-recording.md)
- Test spec: [Formal Review Recording test spec](formal-review-recording.test.md)
- Proposal amendment: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- Spec-review: approved on 2026-05-07 with no material findings.
- Execution plan: [Review Skill Material Finding Recording plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md)
- Plan-review: approved on 2026-05-07 with no material findings.
- Test spec: [Formal Review Recording test spec](formal-review-recording.test.md) updated for the review skill material-finding recording amendment.
- Proposal amendment: [Review Recording Guardrail and Downstream Status Settlement](../docs/proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md), accepted.

## Readiness

Ready for `spec-review`.

This draft amendment defines the formal review recording output guardrail and examples cleanup contract. Downstream upstream-status settlement remains follow-up scope.
