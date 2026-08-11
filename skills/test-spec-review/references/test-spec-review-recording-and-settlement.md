# Test-spec-review recording and settlement

Load this reference exactly when `durable_recording_context` is true. The
parent skill remains the owner of lifecycle and handoff classification, proof
quality, materiality, statuses, staleness, claims, stops, and output meaning.
This reference owns durable recording mechanics and the separate formal-only
settlement procedure.

## Shared recording procedure

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created or updated.
- `Recording status: blocked` when the required review evidence could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

## Artifact placement

Resolve the record root from the explicit user path, then the active change
record, plan, reviewed artifact, current metadata, project workflow guide, and
portable defaults. Block on remaining ambiguity. If formal recording is
required and no change pack exists, create or request
`docs/changes/<change-id>/` before claiming `Recording status: recorded`.

Formal test-spec-review records default to:

`docs/changes/<change-id>/reviews/test-spec-review-r<n>.md`

Register every recorded review in:

`docs/changes/<change-id>/review-log.md`

Use `docs/changes/<change-id>/review-resolution.md` only when material findings,
blocking outcomes, or another approved disposition trigger requires it.

If the user requested an isolated advisory review and no formal recording is
required, do not create lifecycle artifacts unless explicitly asked.

For a clean review, create the lightweight review receipt required by the formal review recording spec and index it in `review-log.md`. Do not create an empty `review-resolution.md` solely for a clean review.

For material findings or blocking outcomes, create the required detailed review record and disposition artifacts.
Use a detailed review record for material or blocking review outcomes.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Copy `assets/review-result-skeleton.md` for every durable result and
`assets/material-finding.md` exactly once per material finding. Never put
applicability, status meaning, settlement, claim, or handoff policy in an asset.

Do not merely tell the user that review artifacts should be created. Create or update them before final output, or report `Recording status: blocked` with the blocker and smallest next action.

For an isolated review with material findings, the final review output must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

Retry an identical interrupted write by reconciling existing evidence and
completing it once. Do not duplicate receipts, findings, or log entries. Stop
without mutation when a review ID is reused for a different target, evidence
identity, or result.

If the reference, result asset, or required finding asset is unavailable, keep
findings visible and report blocked recording with the exact missing path and
smallest corrective action. Do not reconstruct the resource from memory.

## Formal-only settlement

Advisory lifecycle mode must not execute this section. Formal mode performs it
only after durable review evidence is written. Treat the reviewed test spec,
upstream artifacts, other artifact entries, milestones, and routing as
read-only.

Before settlement, read the complete `change.yaml` and require
`lifecycle_contract: stage-owned-change-local-v1`. Resolve exactly one active
test-spec entry by artifact ID, `kind`, and normalized reviewed path. Require
`review-required` and complete authoring evidence, and require the current
lifecycle state to request `test-spec-review`.

Write the durable review record first. Then remove `authoring_evidence` and set
the exact review mapping with `id`, `artifact_id`, `outcome`, `record`, and
`round`. Map `approved` to `active`, `changes-requested` to
`revision-required`, and `blocked` or `inconclusive` to `blocked`.

The procedure must settle only the matching test-spec entry. Preserve every other artifact entry,
milestone, workflow route, and next-stage field. The review may report handoff
but stops without advancing routing and must not invoke implementation.

Retry identical incomplete settlement without rerunning the review. Stop on
ambiguous identity, stale evidence, conflicting review-ID reuse, illegal
transition, or failed available change-metadata validation.
