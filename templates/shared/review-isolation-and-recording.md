## Isolation and Recording

Isolation governs handoff. Recording follows the finding. These are
independent.

A direct or review-only review request remains isolated by default: it
does not automatically continue into downstream workflow stages.
Isolation does not suppress recording.

A material finding requires a durable change-local review record under
`docs/changes/<change-id>/reviews/`. This applies regardless of whether
the review was workflow-managed or isolated.

The durable record must be created before review-driven edits begin. If
review-driven edits already began before the durable record exists, the
record is reconstructed and must disclose source, timing, available
evidence, stable Finding IDs, and known fidelity loss.

A tracked artifact is any version-controlled repository file whose
change will be committed or reviewed as part of the work. This includes
lifecycle artifacts, governance files, workflow summaries, skills,
specs, schemas, scripts, generated outputs, README content, and
change-local artifacts. Edits to ephemeral chat output, local scratch
files, or unversioned drafts are not tracked artifact edits.

The recording obligation is also a resolution-step gate. A revision
made in response to a material finding is incomplete until the finding
is durably recorded.

Materiality is governed by `CONSTITUTION.md` and is not redefined here.
A material finding requires evidence, required outcome, and a safe
resolution path or `needs-decision` rationale before it drives fixes.

Operational shortcut: if a finding changes or blocks a tracked artifact
edit, changes scope, changes requirements, changes architecture,
changes sequencing, changes validation, creates follow-up work, or
requires disposition, treat it as material unless the reviewer
explicitly records a non-material rationale.

Reconstructed records are governed by `specs/rigorloop-workflow.md`.

Clean reviews with no material findings remain lightweight and may
settle in the reviewed artifact when no detailed-record trigger
applies.

For an isolated review with material findings, final review output names
the isolated handoff status, material Finding IDs, required durable
review record path or reconstruction requirement, confirms
`review-resolution.md` is required, and states the next allowed action:
`create-change-local-record-before-fixing`,
`reconstruct-record-because-fixes-already-began`, or
`stop-for-owner-decision`. Downstream handoff remains stopped unless
explicitly requested.
