# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Maintainer proposal-review
Target: docs/proposals/2026-05-07-review-skill-material-finding-recording.md
Status: revise

## Scope

Reviewed the proposal to clarify material-finding recording across formal review skills, including the shared subsection strategy, timing rule, tracked-artifact definition, initial review-record root, `review-resolution.md` boundary, validator scope, and isolated review output behavior.

## Findings

### RSV1: Recording timing is weaker than the existing first-pass principle

Finding ID: RSV1

Evidence: `docs/proposals/2026-05-07-review-skill-material-finding-recording.md` says a material finding that drives a tracked artifact edit requires a durable record before the edit is considered complete, and says review-driven revisions are incomplete until the finding is durably recorded.

Required outcome: Strengthen the timing rule so a material finding that will drive tracked artifact edits is recorded before review-driven edits begin.

Suggested resolution: State that material findings that will drive tracked artifact edits must be recorded before review-driven edits begin. If edits already began before the record was created, the record must be labeled reconstructed and disclose source, timing, available evidence, stable Finding IDs, and known fidelity loss. Keep the incomplete-until-recorded wording as a fallback, not the primary rule.

### RSV2: `tracked artifact` is defined too narrowly

Finding ID: RSV2

Evidence: The shared block defines a tracked artifact as any file governed by the formal lifecycle.

Required outcome: Broaden and clarify the definition so it covers all version-controlled repository files whose changes will be committed or reviewed.

Suggested resolution: Define tracked artifact as any version-controlled repository file whose change will be committed or reviewed as part of the work, including lifecycle artifacts, governance files, workflow summaries, skills, specs, schemas, scripts, generated outputs, README content, and change-local artifacts. Exclude ephemeral chat output, local scratch files, and unversioned drafts.

### RSV3: Minimum change-local record omits initial-root versus final-pack distinction

Finding ID: RSV3

Evidence: The proposal says the minimum record for an isolated material review case is `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/<stage>-r<n>.md`.

Required outcome: Clarify that the listed files are the initial review-record root, not final handoff completion.

Suggested resolution: State that the minimum record for an isolated material review case is the initial review-record root. It preserves review event and disposition evidence before or during the review-driven edit. Final handoff for non-trivial work still requires the baseline non-trivial change pack, including durable Markdown reasoning such as `explain-change.md` or another approved durable reasoning surface.

### RSV4: `review-resolution.md` should not be required for every detailed record unless material findings exist

Finding ID: RSV4

Evidence: The proposal's minimum record includes `review-resolution.md` whenever an isolated material finding drives edits, while the proposal also discusses detailed-record triggers such as explicit reviewer request and reconstructed evidence.

Required outcome: Preserve the existing boundary: `reviews/` requires `review-log.md`; material findings require `review-resolution.md`; no-material detailed reviews do not require empty `review-resolution.md`.

Suggested resolution: State that material findings require an initial root containing `change.yaml`, `review-log.md`, `review-resolution.md`, and `reviews/<stage>-r<n>.md`. If no material findings exist but another detailed-record trigger applies, the initial root contains `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`. `review-resolution.md` is required only when material findings or another approved review-resolution trigger exists.

### RSV5: Byte-equality shared-block strategy is brittle without a canonical block source

Finding ID: RSV5

Evidence: The proposal says review skills should share the same subsection verbatim and proposes byte-equality assertions, while also saying not to introduce a generation step.

Required outcome: Define the canonical source of the shared subsection.

Suggested resolution: Store the shared block in one canonical source file, such as `templates/shared/review-isolation-and-recording.md`, then copy it manually into the five formal review skills. Tests compare all five skills against that source. Do not use byte-equality with no defined source.

### RSV6: The shared block needs a practical local materiality trigger

Finding ID: RSV6

Evidence: The shared block says materiality is governed by `CONSTITUTION.md` and is not redefined.

Required outcome: Add a short operational test without redefining materiality.

Suggested resolution: Add an operational shortcut: if the finding changes or blocks a tracked artifact edit, changes scope, changes requirements, changes architecture, changes sequencing, changes validation, creates follow-up work, or requires disposition, treat it as material unless the reviewer explicitly records a non-material rationale.

### RSV7: Direct or review-only output should name both stop condition and recording obligation

Finding ID: RSV7

Evidence: The proposal says final review output for isolated material cases should name the isolated stop condition and required recording or resolution surface.

Required outcome: Add a final-output rule for isolated material reviews.

Suggested resolution: State that an isolated review with material findings must include isolated handoff status, material Finding IDs, required durable review record path or reconstruction requirement, whether `review-resolution.md` is required, and next allowed action: record before fix, reconstruct if already fixed, or stop for owner decision.

## Recommendation

Revise the proposal before downstream spec work. These findings are material because they affect the timing, scope, source, and visibility of the review-recording rule that future specs and skill updates will implement.
