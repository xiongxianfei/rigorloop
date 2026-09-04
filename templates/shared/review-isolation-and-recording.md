## Isolation and Recording

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created or updated.
- `Recording status: blocked` when the required review evidence could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

For `compact-current-state-v1`, update the target's stable current review record through the CLI. A clean review replaces its current judgment at the stable path. Material findings remain directly accessible in that record; only resolved decisions that continue to constrain the change belong in `material-decisions.md`. Do not create round-suffixed reviews, `review-log.md`, `review-resolution.md`, request files, or correction receipts.

For registered historical contracts, create the lightweight clean receipt or detailed review record required by that contract, index it in `review-log.md`, and create `review-resolution.md` only when triggered.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Do not merely tell the user that review artifacts should be created. Create or update them before final output, or report `Recording status: blocked` with the blocker and smallest next action.

For an isolated review with material findings, the final review output must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed
