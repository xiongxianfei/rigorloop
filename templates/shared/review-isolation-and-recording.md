## Isolation and Recording

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does
not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every supported formal lifecycle review invocation requires durable review
recording.

Every material finding requires a durable change-local review record
under:

`docs/changes/<change-id>/reviews/<stage>-r<n>.md`

The review record must be indexed in `review-log.md` and resolved in
`review-resolution.md`.

Create the durable record before fixing.

A material finding must include:

- evidence
- required outcome
- safe resolution path, or `needs-decision` rationale

Every material finding must also preserve complete finding shape:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Use the formal review recording change-ID selection rule. If no change ID can
be selected, report `Recording status: blocked` and state the smallest action
needed.

Clean formal reviews use lightweight review receipts. Material findings use
detailed review records.

### Recording status output

`Recording status` is separate from the review verdict.

For supported formal lifecycle review invocations, use exactly one:

- `recorded`: required review-recording artifacts were created or updated.
- `blocked`: required review-recording artifacts could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the
formal lifecycle review model.

For material findings, `recorded` requires a detailed review record,
`review-log.md`, and `review-resolution.md`.

For clean formal reviews, `recorded` requires a lightweight review receipt and
`review-log.md`.

For no-material detailed-record triggers, `recorded` requires a detailed review
record and `review-log.md`. Do not require an empty `review-resolution.md` for a
no-material review event.

Formal review output must include `Recording status`, `Recording blocker`,
`Review record`, `Review log`, and `Review resolution` (`path`,
`not-required`, or `blocked`).

If `Recording status: blocked`, include `Recording blocker` and the smallest
action needed.

Do not merely tell the user that review artifacts should be created. Create
or update them before final output, or report `Recording status: blocked`.

For an isolated review with material findings, the final review output
must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed
