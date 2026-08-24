# Test-spec-review recording and settlement

Load this reference exactly when `durable_recording_context` is true. The parent owns review meaning and handoff; this reference owns recording and the separate formal-only settlement procedure.

## Shared recording procedure

Isolation governs handoff, not recording. Direct or review-only work never continues automatically.

Every formal lifecycle review result must be recorded or explicitly blocked.

- `Recording status: recorded` when the required review evidence was created or updated.
- `Recording status: blocked` when the required review evidence could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

## Artifact placement

Resolve the root from explicit path, active change, plan, reviewed artifact, metadata, guidance, then portable defaults; ambiguity blocks. Create or request the change pack before claiming `Recording status: recorded`. A formal test-spec-review record uses `docs/changes/<change-id>/reviews/test-spec-review-r<n>.md` and indexes `docs/changes/<change-id>/review-log.md`. Use `docs/changes/<change-id>/review-resolution.md` only when material findings, blocking outcomes, or dispositions require it. An isolated advisory review proceeds without lifecycle artifacts unless durable recording is requested.

For a clean review, create the lightweight review receipt required by the formal review recording spec and index it in `review-log.md`. Do not create an empty `review-resolution.md` solely for a clean review.

Material or blocking outcomes use a detailed record and required dispositions.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Copy `assets/review-result-skeleton.md` for every durable result and `assets/material-finding.md` once per finding. Assets own structure, not policy.

Create or update required review artifacts before final output, or report blocked recording with the smallest next action. Isolated material results name the finding IDs, record path, owner decision, and lack of automatic handoff.

Reconcile an identical interrupted write once without duplicate evidence. Conflicting review-ID reuse stops unchanged.

Missing required resources keep findings visible and produce blocked recording with the exact path; never reconstruct them.

## Formal-only settlement

Advisory lifecycle mode must not execute this section. Formal mode performs it
only after durable review evidence and its log entry are written. Run
`rigorloop lifecycle context test-spec-review --change <change-id> --format
json`, submit `record-review` with the returned lifecycle revision, exact
test-spec ID, review path, and `stage_authority: test-spec-review`, refresh
context, then submit `settle-artifact` for the same target and authority.

The CLI validates identity, outcome, round, log, findings, freshness, and
derives the lifecycle result. Never edit settlement fields directly. Preserve
a successfully recorded review when settlement blocks. Treat identical
`already-recorded` as success; otherwise report the stable diagnostic and stop.
Settlement never changes routing or invokes implementation.
Treat the reviewed test spec and all upstream artifacts as read-only throughout recording and settlement.
