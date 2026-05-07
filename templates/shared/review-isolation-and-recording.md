## Isolation and Recording

Isolation governs handoff. Recording follows material findings.

A direct or review-only request remains isolated by default: it does
not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

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

Clean reviews with no material findings remain lightweight and do not
require detailed review files.

For an isolated review with material findings, the final review output
must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed
