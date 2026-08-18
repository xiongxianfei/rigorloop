# Governed workflow explanation

## Eligibility and placement

Resolve one change root, `change.yaml`, target, stage, and authority. Use `docs/changes/<change-id>/explain-change.md` unless authority names legacy placement. Invalid identity stops.

Require closed milestones, promotion evidence, and clean final holistic code review. Inspect `review-log.md`. `Closeout status: open` or `needs-decision` blocks; `Closeout status: closed` requires final dispositions and evidence. A stage-owned non-approval outcome requires a same-stage later review round or explicit reviewer or owner closeout; `review-resolution.md` alone is not a silent substitute. no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.

## Reviewed-change basis

Bind change, repository, base revision, reviewed-subject revision, base-to-subject diff identity, final holistic code-review ID and subject identity, governing identities, review-resolution basis, validation-evidence cutoff, explanation path, and prior identity.

Final reviewed diff means base to reviewed-subject. The reviewed-subject revision `S`, final-review-recording revision `R`, explanation-recording revision `E`, and handoff revision remain distinct; no commit contains its own identity.

Completion requires exact linear non-merge `S -> R -> E`. `R` contains only the final-review record, invocation, log, optional resolution, and final-review-owned `change.yaml` fields. `E` contains only the explanation and explain-change-owned workflow-handback fields; it is the handoff revision. Path-only validation is insufficient: an unknown or sibling-owned shared-metadata field blocks.

Only exact `S -> R` is resumable; finish unchanged `E` without repeating review. Reviewed-subject-only, reversed, intervening, additional, merge, broader, or changed-basis tails block or require new review. Product code, tests, specifications, architecture, plans, dependencies, configuration, generated output, unrelated documentation, and another stage's evidence are forbidden in `R` and `E`. Later verify-owned evidence is outside this tail and does not stale an unchanged explanation or cutoff.

## Governed result and handback

Durable output records `Stage: explain-change`, current or blocked status, final diff and review identities, and basis. Governed inline reports the same facts.

`Workflow handback` reports explanation status and basis, cutoff, blockers, control return, and `Next-stage decision owner: workflow`. Never imply `verify-ready`, `verification-passed`, `branch-ready`, `pr-body-ready`, `pr-open-ready`, `release-ready`, or `lifecycle-complete`. Workflow alone routes; isolated invocation stops.
