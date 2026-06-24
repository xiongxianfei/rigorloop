# Review Finding Resolution Contract

## Status

- approved

## Related proposal

- [Review Finding Resolution Contract](../docs/proposals/2026-04-24-review-finding-resolution-contract.md)
- [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- [Separately Armed Implementation Autoprogression Through Verify](../docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md)

## Goal and context

This spec defines the contributor-visible contract for complete review findings, durable review records, review-resolution closeout, verification proof for accepted fixes, concise final explanation, and PR-body review summaries.

The goal is to make review feedback actionable and auditable without turning every clean review into artifact boilerplate. A material review finding is not complete until it says what evidence supports it, what outcome is required, and at least one safe way to resolve it or why an owner decision is needed first.

This spec intentionally expands the current workflow disposition vocabulary from `accepted`, `rejected`, and `deferred` to include `partially-accepted` and `needs-decision`. `needs-decision` is an unresolved stop state, not a final closeout state.

This amendment also requires new `review-resolution.md` records to be scan-first for humans while preserving validator-readable field labels for structural and closeout validation.

This amendment also defines reviewer-owned auto-fix classification fields for material code-review findings when the separately armed implementation profile is active. The classification determines whether the workflow may automatically apply a correction recipe or must pause for human judgment.

## Glossary

- `review record`: a durable review artifact or review output that records the review stage, target, status, findings, and suggested resolution path.
- `formal lifecycle review`: one of `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, or `code-review`.
- `detailed review file`: a Markdown file under `docs/changes/<change-id>/reviews/` that preserves one formal lifecycle review round.
- `Review ID`: a stable identifier for one detailed review file.
- `review-log.md`: the change-local index that lists detailed review records and their outcomes.
- `first-pass review record`: the initial durable record created when a formal review returns material feedback, before review-driven fixes are made.
- `finding`: a review item that identifies a defect, proof gap, required decision, advisory follow-up, or other review-relevant observation.
- `material finding`: a finding that must be accepted, rejected, deferred, partially accepted, or resolved from a decision-needed state before downstream closeout.
- `Finding ID`: a stable identifier for one finding within a change.
- `review-resolution.md`: the change-local artifact that records the top-level closeout status plus each material finding disposition, rationale, owner, action, validation target, and validation evidence.
- `scan-first review resolution`: a `review-resolution.md` structure that exposes closeout status, covered reviews, finding counts, disposition overview, shared validation evidence, and per-finding details without forcing reviewers to read repeated prose first.
- `common resolution metadata`: owner, owning stage, validation target, or validation evidence shared by multiple finding entries and recorded once for human readability.
- `disposition`: the recorded decision for a material finding.
- `closeout status`: the top-level state of `review-resolution.md`, either `open` or `closed`.
- `final disposition`: a disposition that may be relied on before `verify`, `explain-change`, or `pr`.
- `needs-decision`: a non-final disposition meaning an authorized owner decision is required before the finding can be closed.
- `reconstructed review record`: a late durable review record created after review-driven fixes have already begun, explicitly labeled as reconstructed and preserving original review evidence when available.
- `authorized owner`: the maintainer, reviewer, plan owner, spec owner, architecture owner, or other role identified by the repository workflow as allowed to resolve or defer the decision.
- `reviewer or owner closeout`: explicit approval from the relevant reviewer or authorized owner that a review outcome requiring revision no longer blocks the next workflow stage.
- `stage-owned non-approval outcome`: a review outcome in that stage's vocabulary that blocks downstream progress or requires revision.
- `initial review-record root`: the smallest `docs/changes/<change-id>/` root created before review-driven fixes or downstream routing when a detailed review file is required but no change-local root exists yet.
- `artifact-local settlement`: final status, decision log, readiness, follow-on, or closeout text in the reviewed proposal, spec, architecture artifact, ADR, or plan.
- `semantic review-quality automation`: automation that judges whether a finding's evidence is persuasive, a suggested solution is best, or a disposition is substantively correct.
- `generated public adapter`: generated installable adapter output under `dist/adapters/`.
- `auto_fix_class`: a reviewer-owned material-finding field whose closed values are `none`, `mechanical`, and `declared-safe`.
- `auto_fix_kind`: the closed mechanical finding kind used when `auto_fix_class` is `mechanical`.
- `declared-safe recipe`: a reviewer-declared deterministic correction recipe for a finding that is not purely mechanical but contains no owner decision.
- `affected paths`: the bounded paths a reviewer authorizes an automatic correction to touch.

## Examples first

### Example E1: complete finding can enter review-resolution

Given a `code-review` finding says a required edge case lacks direct proof
And it cites the relevant requirement, test-spec item, and changed test file
When the finding states that the required outcome is direct proof for the edge case
And it suggests adding or updating a targeted test as a safe resolution
Then the finding is complete enough to enter `review-resolution`.

### Example E2: incomplete finding cannot drive a fix loop

Given a review record says only "this needs more validation"
When it does not identify supporting evidence, required outcome, or a safe resolution path
Then the finding is incomplete and must be revised before it can be accepted, rejected, deferred, or partially accepted.

### Example E3: reviews directory requires review-log

Given a non-trivial change creates `docs/changes/<change-id>/reviews/code-review-r1.md`
When there is only one detailed review file
Then `docs/changes/<change-id>/review-log.md` still exists and references that Review ID.

### Example E4: needs-decision blocks downstream closeout

Given `review-resolution.md` records finding `CR1-F2` as `needs-decision`
When no authorized owner has resolved or explicitly deferred that decision
Then `verify`, `explain-change`, and `pr` are blocked.

### Example E5: partially accepted finding closes only with sub-decisions

Given a finding asks for a test and a broad documentation rewrite
When the test request is accepted and the rewrite is deferred
Then `review-resolution.md` may use `partially-accepted` only if it records the accepted portion, the deferred portion, rationale, follow-up owner or no-follow-up reason, and validation evidence for the accepted test.

### Example E6: PR body stays concise

Given a change has three accepted findings, one rejected finding, and one deferred finding
When `pr` drafts the PR body
Then it includes a review-resolution summary with counts and a link to `review-resolution.md`, not a duplicate transcript of every finding and suggestion.

### Example E7: canonical skill changes regenerate adapters

Given implementation updates canonical review-stage skills
When those skills are shipped through public adapters
Then `.codex/skills/`, `dist/adapters/codex/`, `dist/adapters/claude/`, `dist/adapters/opencode/`, and `dist/adapters/manifest.yaml` remain generated and validated in sync.

### Example E8: first-pass review is recorded before fixes

Given `architecture-review` returns `revise` with findings `AR1` and `AR2`
When the implementer intends to fix the architecture
Then `docs/changes/<change-id>/reviews/architecture-review-r1.md` is created before those fixes
And `review-log.md` references `architecture-review-r1`
And `review-resolution.md` contains entries for `AR1` and `AR2` before revision work begins.

### Example E9: resolution does not replace required re-review

Given a first-pass review outcome is `revise`
And `review-resolution.md` records both findings as accepted and fixed
When no same-stage re-review or explicit reviewer or owner closeout exists
Then the change cannot advance to the next workflow stage.

### Example E10: open review-resolution is not final closeout

Given `review-resolution.md` records finding `AR1` with disposition `accepted`
And `review-resolution.md` has top-level `Closeout status: open`
When validation evidence is still pending
Then `verify`, `explain-change`, and `pr` must treat `AR1` as unresolved.

### Example E11: reconstructed review record is explicit

Given review-driven fixes already began before a durable review record was created
When the contributor repairs the missing record
Then the detailed review file says `Record mode: reconstructed`
And it preserves the original review source and evidence or durable links to them
And it states that the record was created after fixes had begun.

### Example E12: review-log uses canonical line blocks

Given `docs/changes/<change-id>/review-log.md` records two formal reviews
When structural validation reads the ledger
Then each counted ledger entry is a `### Review entry` block
And each counted block contains exactly one `Review ID: <id>` line plus stage, round, status, detailed record, resolution, material findings, and open findings lines.

### Example E13: no-material non-approval review record has no empty resolution

Given `plan-review` returns `rethink`
And the review creates no material findings
When that outcome blocks downstream routing
Then `docs/changes/<change-id>/reviews/plan-review-r1.md` is created
And `review-log.md` indexes `plan-review-r1`
And no empty `review-resolution.md` is required solely for that review event.

### Example E14: review-resolution is scan-first and validator-readable

Given `proposal-review-r1` records seven accepted findings
When `review-resolution.md` closes those findings
Then the file starts with closeout status, covered reviews, resolved and unresolved counts, and a resolution overview table
And each finding detail still contains parseable `Finding ID:`, `Disposition:`, `Owner:`, `Owning stage:`, `Chosen action:`, `Rationale:`, `Validation target:`, and `Validation evidence:` labels.

### Example E15: unclassified finding pauses implementation autoprogression

Given `code-review` records material finding `CR-1`
And `CR-1` lacks `auto_fix_class`
When the implementation profile evaluates automatic correction eligibility
Then `CR-1` is treated as `auto_fix_class=none` and the profile pauses.

### Example E16: mechanical finding includes deterministic authority

Given `code-review` records a formatter-output finding
When the reviewer classifies it as `auto_fix_class=mechanical`
Then the finding names `auto_fix_kind`, affected paths, deterministic authority, and required validation before any automatic correction may run.

### Example E17: declared-safe production-code fix includes proof

Given `code-review` records a production-code finding with `auto_fix_class=declared-safe`
When the reviewer provides a deterministic recipe
Then the recipe includes changed-behavior test proof or cites existing test-spec mappings that already cover the changed behavior.

## Requirements

R1. A material review finding MUST include evidence supporting the finding.

R1a. Finding evidence MUST identify at least one concrete support surface such as a file reference, requirement ID, test-spec item, validation output, artifact inconsistency, review input, or explicit missing-evidence condition.

R1b. A material review finding MUST state the outcome required to satisfy the review gate.

R1c. A material review finding MUST state at least one safe resolution path or state that an authorized owner decision is required before a safe resolution can be chosen.

R1d. A finding that lacks evidence, required outcome, or either a safe resolution path or decision-needed rationale MUST be treated as incomplete.

R1e. A material code-review finding created while `implementation-through-verify` is active MUST include `auto_fix_class`; if the field is absent, the workflow MUST treat it as `none`.

R1f. `auto_fix_class` values MUST be closed to:
- `none`;
- `mechanical`;
- `declared-safe`.

R1g. `auto_fix_class=none` MUST be used when owner intent is required, alternatives remain, behavior or compatibility could change, a governing artifact may need revision, affected paths are unbounded, validation is not deterministic, or classification is omitted.

R1h. `auto_fix_class=mechanical` MUST identify `auto_fix_kind`, affected paths, deterministic authority, and required validation.

R1i. Mechanical `auto_fix_kind` values MUST be closed to:
- `formatter-output`;
- `lint-autofix`;
- `generated-output-refresh`;
- `exact-approved-rename`;
- `unique-required-field-value`;
- `mechanical-state-projection-sync`;
- `deterministic-manifest-regeneration`.

R1j. `auto_fix_class=declared-safe` MUST identify affected paths, resolution recipe, named inputs, named outputs, forbidden paths, acceptance criteria, required validation commands, and scope-preservation rule.

R1k. A `declared-safe` recipe that changes production code MUST include a test that exercises the changed behavior or cite existing test-spec mappings that already prove the changed behavior.

R1l. Reviewers MUST NOT use `mechanical` or `declared-safe` when the safe resolution path contains an owner decision, compatibility choice, governing-artifact revision, new dependency, new component, new public interface, new external integration, new security boundary, migration, or unplanned generated artifact class.

R2. Detailed review files under `docs/changes/<change-id>/reviews/` MUST include a Review ID, stage, round, reviewer, target, and status.

R2a. Review ID values MUST be stable ASCII identifiers within the change.

R2b. Stage values MUST identify the formal lifecycle review stage that produced the detailed review file.

R2c. Formal lifecycle review stages for `reviews/` are `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.

R2d. A dedicated `pr-review` stage MUST NOT be treated as a valid formal lifecycle review stage unless a later approved spec explicitly adds it and updates validation.

R2da. Maintainer PR review comments MUST NOT be automatically copied into `reviews/` for this version.

R2e. Round values MUST identify the review round for that stage.

R2f. Target values MUST identify the proposal, spec, plan, diff, commit range, artifact, or other review surface inspected.

R2g. Status values MUST identify the stage-owned review outcome and MUST be present even when the vocabulary is stage-specific.

R2h. Review IDs MUST be unique within a single `docs/changes/<change-id>/` change.

R2i. Review ID uniqueness MUST be scoped to the change, not to the whole repository.

R2j. A detailed review record MUST have exactly one Review ID.

R2k. A detailed review record MUST NOT reuse a Review ID already used by another detailed review record or by another review-log entry for the same change.

R2l. A Review ID MUST identify one review event, not a review stage class.

R2m. Material review findings MUST be recorded before fixes begin.

R2m-exception. If fixes have already begun before the durable review record was created, a late repair is allowed only by creating a reconstructed review record. A reconstructed record MUST:
- be labeled `Record mode: reconstructed`;
- preserve the original review source when available;
- include original review evidence or a durable link to it;
- state that the record was created after fixes had begun;
- record all material findings with stable Finding IDs;
- record any known loss of fidelity.

R2n. Detailed review files MUST preserve first-pass review history and MUST NOT be rewritten to hide or replace material findings after fixes begin.

R2o. Corrections, decisions, fixes, and validation evidence for findings MUST be recorded in `review-resolution.md`, a later review round, or other explicit closeout artifact rather than by mutating the first-pass review record.

R2p. A detailed review file MUST be created for a formal lifecycle review when any of the following is true:
- the review produces material findings;
- the review returns a stage-owned non-approval outcome that blocks downstream progress or requires revision;
- the review is reconstructed;
- the review findings will be cited as closeout evidence;
- a reviewer or maintainer explicitly requests a detailed record.

R2pa. Material findings MUST always be recorded.

R2pb. All material findings require change-local review files.

R2q. Stage-owned non-approval outcomes MUST include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent stage-specific outcomes that prevent downstream progress.

R2r. A clean formal review with no material findings MUST NOT require an empty detailed review file solely because the review was required.

R2s. A required formal review with no material findings MAY be recorded through artifact-local settlement when no `R2p` trigger applies.

R2t. If a workflow-managed formal review triggers a detailed review file before a change-local root exists, the change MUST create an initial review-record root before review-driven fixes or downstream routing proceed.

R2u. If material findings exist, the initial review-record root MUST include `docs/changes/<change-id>/change.yaml`, `docs/changes/<change-id>/review-log.md`, `docs/changes/<change-id>/review-resolution.md`, and `docs/changes/<change-id>/reviews/<stage>-r<n>.md`.

R2v. If `R2p` requires a detailed review file for a no-material trigger, the initial review-record root MUST include `docs/changes/<change-id>/change.yaml`, `docs/changes/<change-id>/review-log.md`, and `docs/changes/<change-id>/reviews/<stage>-r<n>.md`. `review-resolution.md` MUST NOT be created solely because `reviews/` exists.

R2w. The initial review-record root exists to preserve the review event and make it discoverable. It MUST NOT be treated as the final non-trivial change-local pack.

R3. If `docs/changes/<change-id>/reviews/` exists, `docs/changes/<change-id>/review-log.md` MUST exist.

R3a. `review-log.md` MUST reference every Review ID from detailed review files under `reviews/`.

R3b. `review-log.md` MUST NOT reference a Review ID that has no corresponding detailed review file in `reviews/`.

R3c. The `reviews/` to `review-log.md` rule MUST apply even when there is only one detailed review file.

R3d. If `review-log.md` exists, each Review ID MUST appear exactly once in the review log for that change.

R3e. `review-log.md` MUST identify, for each detailed review event, the Review ID, stage, round, status, detailed record path, material Finding IDs, and whether those findings remain open.

R3f. `review-log.md` MUST use a parseable Review ID entry for each detailed review event so structural validation can distinguish intentional ledger entries from incidental prose mentions.

R3g. `review-log.md` MUST be updated when material finding closeout changes whether a review event still has open findings.

R3h. When `review-resolution.md` has `Closeout status: closed`, every review-log entry MUST have an empty open-finding set.

R3i. If any `Open findings:` value in `review-log.md` still lists Finding IDs, closeout validation MUST fail.

R3j. `verify`, final `explain-change` closeout, and `pr` handoff MUST NOT proceed while `review-log.md` still lists open findings.

R3k. Each review-log entry MUST contain exactly one `Resolution:` line in the canonical form `Resolution: review-resolution.md#<Review ID>`.

R3l. For v1, `Resolution:` is a repository-internal symbolic resolution reference. Structural validation MUST fail when the field is missing, the target file is not exactly `review-resolution.md`, the anchor does not exactly match the entry's Review ID, or the referenced Review ID cannot be found in `review-resolution.md` when that artifact exists.

R3la. The symbolic `Resolution:` ledger field MUST NOT by itself require a `review-resolution.md` file when no material finding exists and no other approved review-resolution trigger exists.

R3m. For v1, each parseable `review-log.md` ledger entry MUST use this line-based block format:

```md
### Review entry
Review ID: RV-001
Stage: architecture-review
Round: 1
Status: revise
Detailed record: reviews/architecture-review-r1.md
Resolution: review-resolution.md#RV-001
Material findings: AR1, AR2
Open findings: AR1, AR2
```

R3n. For v1, structural validation MUST count only `Review ID: <id>` lines inside `### Review entry` blocks as review-log ledger references.

R3o. Incidental prose mentions of Review IDs MUST NOT count as review-log ledger references.

R3p. Each `### Review entry` block MUST contain exactly one `Review ID: <id>` line.

R4. Material findings recorded in detailed review files MUST have Finding IDs.

R4a. Finding IDs MUST be unique within a single `docs/changes/<change-id>/` change.

R4b. Finding ID values MUST be stable ASCII identifiers with no whitespace.

R4c. Non-material positive notes, nits, or informational observations MAY omit Finding IDs when they do not require a disposition.

R5. A change with material findings MUST record review resolution in `docs/changes/<change-id>/review-resolution.md`.

R5a. `review-resolution.md` MUST reference only Finding IDs that exist in the change's review records.

R5b. Every material Finding ID MUST appear in `review-resolution.md`.

R5c. `review-resolution.md` MUST record the disposition, rationale, final action or stop state, and required evidence for each referenced material finding.

R5d. A material Finding ID is unresolved until it has a disposition entry in `review-resolution.md`.

R5e. `review-resolution.md` MUST contain an entry for every material Finding ID before review-driven fixes for those findings begin.

R5f. An initial resolution entry MUST record the Finding ID, disposition, owner, owning stage, chosen action or stop state, rationale when known, and validation target or expected proof.

R5g. If no decision has been made yet, the initial disposition MUST be `needs-decision`; otherwise the initial disposition MUST use one of the approved disposition values and `review-resolution.md` MUST remain `open` until the required closeout record exists.

R5h. During revision work, `review-resolution.md` MUST be updated with the chosen action, changed files or artifacts when known, rationale, validation target, and validation evidence as those facts become available.

R5i. `review-resolution.md` MUST separate suggested resolution from final action when the final action differs from the reviewer suggestion.

R6. Review-resolution dispositions MUST use only the approved disposition values:
- `accepted`;
- `rejected`;
- `deferred`;
- `partially-accepted`;
- `needs-decision`.

R6a. Before `verify`, `explain-change`, or `pr`, every material finding MUST have a final disposition.

R6b. The only final dispositions are:
- `accepted`;
- `rejected`;
- `deferred`;
- `partially-accepted`.

R6c. `needs-decision` MUST NOT be treated as a final disposition.

R6d. `needs-decision` MUST block `verify`, `explain-change`, and `pr` until an authorized owner resolves the decision or explicitly defers it.

R6e. A `needs-decision` record MUST identify the decision owner, decision needed, and owning stage.

R6f. `review-resolution.md` MUST have a top-level closeout status of exactly one of:
- `open`;
- `closed`.

R6g. `open` means one or more material findings are not yet fully resolved for handoff. `closed` means every material finding has a final disposition and all disposition-specific closeout requirements are satisfied.

R6h. A finding with disposition `accepted` MAY count toward `closed` only when the chosen action is recorded and validation evidence for the accepted fix is recorded.

R6i. A finding with disposition `rejected` MAY count toward `closed` only when rationale is recorded.

R6j. A finding with disposition `deferred` MAY count toward `closed` only when deferral rationale is recorded and a follow-up owner, owning stage, or explicit no-follow-up reason is recorded.

R6k. A finding with disposition `partially-accepted` MAY count toward `closed` only when the accepted portion meets accepted closeout requirements and the rejected or deferred portion meets its own closeout requirements.

R6l. A finding with disposition `needs-decision` is not a final disposition and always keeps closeout status `open`.

R6m. Before `verify`, `explain-change`, or `pr`, `review-resolution.md` MUST have `Closeout status: closed`.

R7. An `accepted` disposition MUST record the chosen action and validation evidence proving the action worked.

R7a. A `rejected` disposition MUST record why the finding will not be acted on.

R7b. A `deferred` disposition MUST record the deferral reason and a follow-up owner, owning stage, or explicit no-follow-up reason.

R7c. A `partially-accepted` disposition MUST record the accepted portion, rejected or deferred portion, rationale for the non-accepted portion, and validation evidence for the accepted portion.

R7d. A `partially-accepted` disposition MUST NOT be final until all accepted and non-accepted sub-decisions have the required records.

R8. `verify` MUST check accepted and partially accepted review fixes against recorded findings, final actions, and validation evidence.

R8a. `verify` MUST block when any material finding remains `needs-decision`.

R8b. `verify` MUST block when an accepted or accepted portion of a partially accepted finding lacks validation evidence.

R8c. `verify` MUST block when a rejected, deferred, or non-accepted portion lacks required rationale.

R8d. `verify` MUST block when any material Finding ID is missing from `review-resolution.md`.

R8e. `pr` handoff MUST NOT proceed while any material Finding ID is missing from `review-resolution.md`.

R8f. If a formal review outcome is a stage-owned non-approval outcome that blocks downstream progress or requires revision, including `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, or an equivalent stage-specific outcome, the change MUST NOT advance to the next workflow stage until the same review stage is rerun or explicit reviewer or authorized owner closeout is recorded.

R8g. `review-resolution.md` alone MUST NOT silently replace a required re-review or explicit closeout when the first-pass review outcome blocks downstream progress.

R8h. `verify`, `explain-change`, and `pr` MUST block when `review-resolution.md` has `Closeout status: open`.

R9. `explain-change.md` MUST summarize review-driven changes concisely and link to review-resolution details when they exist.

R9a. `explain-change.md` MUST NOT become a duplicate transcript of every finding, suggestion, and resolution detail.

R10. PR bodies for changes with `review-resolution.md` MUST include a compact review-resolution summary.

R10a. The PR summary MUST include counts by disposition category and a link to `docs/changes/<change-id>/review-resolution.md`.

R10b. The PR body MUST NOT duplicate every detailed finding and suggested solution when durable review artifacts already contain them.

R10c. The PR body MUST NOT claim PR handoff readiness when any material finding remains `needs-decision`.

R11. Repository-owned structural validation MUST detect the following conditions:
- `reviews/` exists without `review-log.md`;
- a detailed review file lacks Review ID, stage, round, target, or status;
- a detailed review file lacks reviewer;
- a reconstructed review record lacks `Record mode: reconstructed`, original review source when available, original review evidence or durable link, after-fix timing disclosure, stable Finding IDs, or known loss-of-fidelity notes;
- a detailed review file has zero Review IDs or more than one Review ID;
- duplicate Review IDs exist within the change;
- a Review ID from a detailed review file is missing from `review-log.md`;
- `review-log.md` references a non-existent detailed Review ID;
- a Review ID appears more than once in `review-log.md`;
- a review-log entry lacks required ledger fields for a detailed review event;
- a Review ID appears outside the canonical `### Review entry` block form and is incorrectly counted as a ledger reference;
- duplicate Finding IDs exist within the change;
- a material Finding ID is missing from `review-resolution.md`;
- `review-resolution.md` references a non-existent Finding ID;
- `review-resolution.md` uses an unsupported disposition value;
- `review-resolution.md` lacks top-level closeout status or uses a closeout status other than `open` or `closed`;
- a closeout-gated validation mode sees `Closeout status: open`, unresolved `needs-decision`, or a finding counted toward `closed` without its disposition-specific closeout requirements.
- an implementation-profile code-review finding with `auto_fix_class=mechanical` lacks `auto_fix_kind`, affected paths, deterministic authority, or required validation;
- an implementation-profile code-review finding with `auto_fix_class=declared-safe` lacks affected paths, resolution recipe, named inputs, named outputs, forbidden paths, acceptance criteria, required validation commands, or scope-preservation rule;
- an implementation-profile code-review finding uses an unsupported `auto_fix_class` or `auto_fix_kind`.

R11a. Structural validation MUST NOT attempt semantic review-quality automation in this version.

R11b. Structural validation MUST NOT judge whether the evidence is persuasive, the suggested solution is best, or the final action is substantively correct.

R12. When implementation changes canonical skills that are shipped through adapters, generated outputs MUST remain synchronized.

R12a. Generated sync scope MUST include `.codex/skills/`, `dist/adapters/codex/`, `dist/adapters/claude/`, `dist/adapters/opencode/`, and `dist/adapters/manifest.yaml`.

R12b. The implementation MUST NOT update only `.codex/skills/` while leaving generated public adapter output stale.

R12c. Adapter validation MUST run when canonical adapter-shipped skill behavior changes.

R13. This feature MUST preserve the existing clean-review lightweight path.

R13a. A clean review with no material findings MUST NOT require empty `review-resolution.md`, `review-log.md`, or `reviews/` boilerplate solely because this feature exists.

R13b. If a change independently creates `reviews/`, the `review-log.md` requirement applies even when the review has no material findings.

R14. This feature MUST update the existing workflow contract where it currently names only `accepted`, `rejected`, and `deferred` dispositions.

R14a. Stage tables, review-resolution rules, governance summaries, and skills MUST NOT contradict the expanded disposition vocabulary or final-closeout rules.

R15. New `review-resolution.md` records MUST be human-readable and useful, not merely structurally valid.

R15a. A new `review-resolution.md` record MUST expose closeout status, covered Review IDs, count of resolved findings, count of unresolved findings, and final result near the top of the file.

R15b. A new `review-resolution.md` record MUST include a resolution overview that lets a reviewer scan each material Finding ID, disposition, status, and short resolution summary without reading the full per-finding detail.

R15c. When multiple findings share owner, owning stage, validation target, or validation evidence, `review-resolution.md` MAY record common resolution metadata once for human readability.

R15d. Common resolution metadata MUST NOT remove validator-readable field labels from individual material finding entries.

R15e. Each material finding detail in `review-resolution.md` MUST retain parseable labels for `Finding ID:`, `Disposition:`, `Owner:`, `Owning stage:`, `Chosen action:` or another approved action field, `Rationale:`, `Validation target:` or expected proof, and `Validation evidence:` when closeout is claimed.

R15f. A new `review-resolution.md` record SHOULD include shared validation evidence when multiple findings are proven by the same validation run.

R15g. A new `review-resolution.md` record SHOULD include a closeout checklist that makes final readiness auditable.

R15h. `review-resolution.md` MUST NOT become a transcript of every review comment, suggestion, and resolution discussion.

R15i. The readability invariant for `review-resolution.md` is that a reviewer can understand closeout status in 30 seconds and audit any individual finding in 2 minutes.

## Inputs and outputs

Inputs:

- formal lifecycle review records;
- artifact-local settlement in reviewed artifacts when clean formal reviews do not trigger detailed records;
- detailed review files under `docs/changes/<change-id>/reviews/` when present;
- `docs/changes/<change-id>/review-log.md` when `reviews/` exists;
- `docs/changes/<change-id>/review-resolution.md` when material findings exist;
- validation evidence for accepted or partially accepted findings;
- generated skill and adapter output when canonical shipped skills change.

Outputs:

- complete review findings with evidence, required outcome, and safe resolution or decision-needed rationale;
- implementation-profile material finding fields for `auto_fix_class`, `auto_fix_kind`, affected paths, deterministic authority, resolution recipe, forbidden paths, acceptance criteria, and required validation when applicable;
- initial review-record roots for triggered formal reviews before a change-local root exists;
- review-log index entries for detailed review files;
- initial and final review-resolution state with top-level closeout status plus finding-level disposition, owner, action, rationale, validation target, and evidence;
- scan-first review-resolution summaries, overview tables, common metadata, shared validation evidence, and closeout checklists when `review-resolution.md` exists;
- verification proof that accepted fixes worked;
- concise explain-change and PR summaries;
- structural validation failures for missing IDs, missing references, duplicate finding IDs, unsupported dispositions, and stale generated output.

## State and invariants

- Every detailed review file has a Review ID, stage, round, target, and status.
- Every detailed review file identifies the reviewer.
- Every detailed review file has exactly one Review ID.
- First-pass review records are created before review-driven fixes.
- Detailed review files are created for material findings, blocking stage-owned non-approval outcomes, reconstructed review evidence, closeout evidence citation, and explicit durable-record requests.
- Clean formal reviews remain artifact-local when no detailed-record trigger applies.
- No-material detailed records are indexed by `review-log.md` without requiring empty `review-resolution.md`.
- Initial review-record roots do not replace the final non-trivial change-local pack.
- Review IDs are unique within a change.
- Every Review ID in `reviews/` is indexed exactly once by `review-log.md`.
- Review-log entries identify detailed record paths, statuses, material findings, and open finding state.
- Finding IDs are unique within a change.
- Every material Finding ID appears in `review-resolution.md`.
- `needs-decision` is never final.
- A disposition value is not final closeout while `review-resolution.md` has `Closeout status: open` or required disposition-specific evidence is missing.
- New `review-resolution.md` records remain both scan-first for humans and parseable for validators.
- Review outcomes that require revision do not advance without same-stage re-review or explicit reviewer or owner closeout.
- `verify`, `explain-change`, and `pr` do not proceed while material findings remain unresolved.
- Clean reviews do not create empty resolution boilerplate.
- Canonical skills remain the source of truth for generated Codex and public adapter outputs.

## Error and boundary behavior

- If a material finding is incomplete, the review record must be corrected before a fix loop relies on it.
- If review-driven fixes begin before the first-pass review record exists, the workflow state is invalid and may be repaired only through a reconstructed review record satisfying `R2m-exception`.
- If the original review output cannot be reconstructed with durable evidence, the workflow must stop for an authorized owner decision.
- If a required detailed review file is missing, review-driven fixes or downstream routing must stop until the review evidence is created or reconstructed.
- If a formal review has no material findings and no `R2p` trigger, artifact-local settlement is sufficient and no empty review artifacts are required.
- If a no-material `R2p` trigger requires a detailed review file before a change-local root exists, the initial review-record root needs `change.yaml`, `review-log.md`, and the detailed review file, but not an empty `review-resolution.md`.
- If `reviews/` exists without `review-log.md`, structural validation fails.
- If a detailed review file lacks Review ID, stage, round, target, or status, structural validation fails.
- If a detailed review file lacks reviewer, structural validation fails.
- If a detailed review file has zero Review IDs or more than one Review ID, structural validation fails.
- If Review IDs are duplicated within a change, structural validation fails.
- If `review-log.md` omits or dangles a Review ID, structural validation fails.
- If `review-log.md` lists the same Review ID more than once, structural validation fails.
- If `review-log.md` lacks required ledger fields for a detailed review event, structural validation fails.
- If structural validation counts a Review ID outside a canonical `### Review entry` block, validation fails.
- If Finding IDs are duplicated within a change, structural validation fails.
- If a material Finding ID is missing from `review-resolution.md`, structural validation fails when material findings are structurally identifiable.
- If review-driven fixes begin before material findings have resolution entries, the workflow state is invalid and must be repaired with durable resolution entries before continuing.
- If `review-resolution.md` references a missing Finding ID, structural validation fails.
- If `review-resolution.md` uses an unsupported disposition, structural validation fails.
- If a resolution entry has a final disposition value but `review-resolution.md` has `Closeout status: open`, downstream closeout fails.
- If any material Finding ID is missing from `review-resolution.md`, `verify` blocks branch readiness and `pr` handoff stops.
- If `needs-decision` remains before `verify`, `explain-change`, or `pr`, the workflow stops and reports the decision owner, decision needed, and owning stage.
- If accepted-fix validation evidence is missing, `verify` blocks branch readiness.
- If a blocking review outcome has no same-stage re-review or explicit reviewer or owner closeout, the workflow cannot advance to the next stage.
- If scan-first formatting removes required per-finding parseable labels, structural or closeout validation fails.
- If a review-resolution record duplicates long shared validation evidence in every finding, it remains structurally valid but fails the readability guidance and should be revised before handoff when the file is new or substantively revised.

## Compatibility and migration

- This feature changes workflow-stage policy and review-gate behavior, so it requires the full lifecycle.
- Existing historical review artifacts do not need retroactive migration unless they are touched, generated, or relied on as current authoritative guidance for a new change.
- Existing clean review settlements in proposals, specs, architecture artifacts, ADRs, or plans remain valid historical evidence when no detailed-record trigger applied.
- Existing references that list only `accepted`, `rejected`, and `deferred` must be updated when they govern current behavior.
- The new `partially-accepted` and `needs-decision` values are additive for authoring review-resolution records, but `needs-decision` is not a closeout value.
- Existing historical `review-resolution.md` files do not need retroactive readability migration unless they are touched or used as current templates.
- Rollback may revert the expanded vocabulary and structural validation while preserving the older requirement that review items have accepted, rejected, or deferred dispositions with rationale.
- Public adapter packages must remain deterministic generated output from canonical skills.

## Observability

- Structural validation output must identify the path and reason for each review artifact structure failure.
- `verify` output must identify unresolved `needs-decision` findings and missing accepted-fix evidence.
- PR bodies must expose the review-resolution summary and artifact link when `review-resolution.md` exists.
- Change-local artifacts should make review and resolution traceability inspectable without reading chat history.
- Reviewers should be able to scan a new `review-resolution.md` top section to identify closeout status, covered reviews, resolved counts, unresolved counts, and where to audit any one finding.

## Security and privacy

- Review records and resolution artifacts MUST NOT include secrets, credentials, private keys, or sensitive runtime values from diffs or validation output.
- Structural validation MUST NOT require network access or repository secrets.
- Adapter generation and validation MUST NOT weaken the generic workflow requirement that human review and repository controls remain authoritative.

## Accessibility and UX

- Review artifact headings and required fields should be concise and repeatable.
- New `review-resolution.md` records should prefer a summary, resolution overview table, compact finding details, shared validation evidence, and closeout checklist.
- PR review-resolution summaries should be readable without requiring reviewers to scan every detailed review record first.
- No UI-specific accessibility behavior is introduced by this feature.

## Performance expectations

- Structural review-artifact validation should be lightweight enough to run as part of repository-owned local validation and CI.
- The validator should inspect tracked review artifacts and generated output structure without invoking external review tools.

## Edge cases

1. A single detailed review file under `reviews/` still requires `review-log.md`.
2. A clean review with no material findings does not require empty `review-resolution.md`.
3. A change that creates `reviews/` for archival reasons still needs `review-log.md`, even when no finding requires resolution.
4. A finding with evidence and required outcome but no safe resolution path is incomplete unless it identifies the owner decision needed first.
5. `needs-decision` may appear during review-resolution, but it blocks `verify`, `explain-change`, and `pr`.
6. A `partially-accepted` finding with validation for the accepted portion but no rationale for the rejected portion is not closed.
7. A deferred finding without follow-up owner or explicit no-follow-up reason is not closed.
8. A review-log entry that references a Review ID with no detailed file is invalid.
9. A detailed review file with two Review IDs is invalid.
10. Two detailed review files cannot reuse the same Review ID in one change.
11. Two detailed review files cannot reuse the same Finding ID for different findings in one change.
12. A material Finding ID absent from `review-resolution.md` blocks `verify` and `pr`.
13. Maintainer PR comments are not copied into `reviews/` by this version unless a future approved change adds that behavior.
14. Semantic disagreement about whether review evidence is persuasive is not decided by structural validation.
15. Canonical skill changes without regenerated public adapter output fail generated-output drift validation.
16. A first-pass review with a stage-owned non-approval outcome that blocks downstream progress or requires revision cannot be closed by editing `review-resolution.md` alone.
17. An accepted resolution entry remains unresolved while `review-resolution.md` has `Closeout status: open`.
18. A `review-log.md` prose mention of a Review ID does not count as the required ledger entry unless it uses the documented parseable review-log form.
19. A late review record created after fixes began is valid only when it is labeled `Record mode: reconstructed` and preserves durable original review evidence or a fidelity-loss note.
20. A closed handoff with any `Open findings:` IDs still listed in `review-log.md` is invalid.
21. A review-log `Resolution:` field that points outside `review-resolution.md`, uses an anchor different from the entry Review ID, duplicates the field, or references a missing review-resolution Review ID is invalid.
22. A clean required `proposal-review` can settle through proposal status and decision log without creating review files.
23. A `plan-review` with `rethink` but no material findings creates a detailed review file and `review-log.md`, but no empty `review-resolution.md`.
24. A material `architecture-review` finding before any change-local root creates an initial review-record root with `review-resolution.md` before design fixes proceed.
25. A final PR-ready handoff is incomplete if only the initial review-record root exists and durable Markdown reasoning was never added.
26. A `review-resolution.md` file with seven accepted findings and the same validation run records the validation once as shared evidence while each finding keeps parseable `Validation evidence:` labels.
27. A prettier `review-resolution.md` that replaces `Finding ID:` with only a table row is invalid for closeout because the finding entry is no longer parseable.
28. A new `review-resolution.md` without an overview table or equivalent scan-first overview is not ready for review handoff, even if its fields are structurally parseable.
29. An isolated material finding requires change-local review files even when it does not affect tracked work, affect closeout, or create follow-up work. Isolation stops handoff, not recording.

## Non-goals

- Automatically copying maintainer PR review comments into `reviews/` in this version.
- Automating semantic review-quality judgment.
- Requiring a full review artifact pack for every non-trivial change.
- Requiring empty review-resolution files for clean reviews.
- Replacing human review, reviewer judgment, or maintainer decisions.
- Turning `review-resolution.md` into a transcript or long review commentary archive.
- Changing runtime product behavior outside the repository workflow contract.

## Acceptance criteria

- A reviewer can tell whether a material finding is complete by checking for evidence, required outcome, and safe resolution or decision-needed rationale.
- A reviewer can locate every detailed review file through `review-log.md` when `reviews/` exists.
- A reviewer can tell which first-pass review records were created before fixes began.
- A reviewer can tell from `review-log.md` which review events still have open material findings.
- A reviewer can trace every material Finding ID from review record to review-resolution disposition.
- Closeout validation fails when `review-log.md` still lists open findings.
- A reviewer can distinguish an open `review-resolution.md` from final closeout.
- `verify` blocks material Finding IDs missing from `review-resolution.md`.
- `verify` blocks unresolved `needs-decision` findings.
- `verify` blocks `Closeout status: open` and accepted or partially accepted findings without validation evidence.
- `verify` checks validation evidence for accepted and partially accepted findings.
- A change with a stage-owned non-approval review outcome that blocks downstream progress or requires revision cannot advance without same-stage re-review or explicit reviewer or owner closeout.
- `explain-change.md` summarizes review-driven changes without duplicating the full review transcript.
- The PR body summarizes review-resolution counts and links `review-resolution.md`.
- Structural validation detects missing review-log, missing Review ID fields, missing reviewer, invalid reconstructed records, multiple Review IDs in one detailed file, duplicate Review IDs, dangling review-log references, malformed resolution links, incomplete review-log ledger entries, duplicate Finding IDs, material findings missing from review-resolution, unsupported disposition values, open top-level closeout status in closeout-gated validation, stale open findings in closeout-gated validation, and review-resolution references to missing findings.
- Adapter generation and validation catch stale `.codex/skills/` or `dist/adapters/` output after canonical adapter-shipped skill changes.
- Clean reviews remain lightweight and do not create empty review-resolution boilerplate.
- A contributor can tell which formal lifecycle review outcomes require a detailed review file.
- A contributor can create a no-material initial review-record root without creating an empty `review-resolution.md`.
- A reviewer can distinguish the initial review-record root from the final non-trivial change-local pack.
- A reviewer can understand a new `review-resolution.md` closeout state in 30 seconds.
- A reviewer can audit any individual material finding in a new `review-resolution.md` in 2 minutes.
- A new scan-first `review-resolution.md` remains valid under structural and closeout validation.
- A contributor can tell that every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.

## Open questions

- What exact dogfood sample threshold should trigger a follow-on proposal for `test-spec-review` if implementation-profile settlement evidence proves insufficient?

## Next artifacts

- Architecture assessment for review-record schema, material-finding fields, automatic correction evidence, and generated adapter impact.
- Architecture and architecture-review when the assessment requires architecture.
- Test-spec amendments for review-finding auto-fix classification and loop guardrails.
- Plan and plan-review before implementation.

## Follow-on artifacts

- `docs/architecture/2026-04-24-review-finding-resolution-contract.md`
- `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/architecture-review-r1.md`
- `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/architecture-review-r2.md`
- `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/spec-review-r1.md`
- `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/spec-review-r2.md`
- `docs/changes/2026-04-24-review-finding-resolution-contract/review-log.md`
- `docs/changes/2026-04-24-review-finding-resolution-contract/review-resolution.md`
- `docs/plans/2026-04-25-review-finding-resolution-contract.md`
- `specs/review-finding-resolution-contract.test.md`
- Proposal amendment: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- Spec-review: approved on 2026-05-07 with no material findings.
- Execution plan: [Review Skill Material Finding Recording plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md)
- Plan-review: approved on 2026-05-07 with no material findings.
- Test spec: [Review Finding Resolution Contract test spec](review-finding-resolution-contract.test.md) updated for the review skill material-finding recording amendment.
- `proposal`: [Separately Armed Implementation Autoprogression Through Verify](../docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md)
- `proposal-review`: approved in [proposal-review-r1](../docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/proposal-review-r1.md)
- `spec-review`: approved in [spec-review-r1](../docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/spec-review-r1.md)

## Readiness

- Approved amendment for implementation-profile reviewer-owned auto-fix classification and correction evidence.
- Ready for architecture assessment before downstream planning or implementation relies on the new profile.
