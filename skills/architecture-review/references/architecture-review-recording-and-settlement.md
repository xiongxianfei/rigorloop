# Architecture-review recording and settlement

Use only after durable recording is established. The parent and architecture method own judgment; this reference owns recording and formal CLI settlement.

## Recording and identity

`advisory-durable` writes only an authorized standalone record and creates no governed state. `formal-lifecycle` requires one exact governed root, writes the review before settlement, synchronizes `review-log.md`, and uses resolution only when required. Failure permits no settlement.

Bind one review subject and governing basis, ordered optional settlement targets, review ID, round, record path, and log path. Each target names exact artifact ID, kind, path, content identity, and applicable authoring evidence. Record-only no-impact or upstream-gap subjects use no settlement targets. Changed basis, target identity, order, or result requires a new occurrence.

One overall status applies and creates no partial approval. Approved canonical targets may settle approved and ADRs to their evidenced accepted or active result. Changes-requested affects only targets named by findings. Blocked target scope must be explicit. Inconclusive is record-only unless separate target-scoped blocker evidence exists.

## Prepared settlement manifest

Record the prepared settlement manifest before any CLI target operation. It binds subject, basis, target order, identity, disposition, expected result, and progress. For each target in order, run `rigorloop lifecycle context architecture-review --change <change-id> --format json`, submit `record-review` with its lifecycle revision, target ID, shared review path, and `stage_authority: architecture-review`, refresh context, then submit `settle-artifact` for that target.

The review record must name every target path and digest. The CLI derives the lifecycle result and rejects drift, stale identity, invalid authority, or unresolved findings. Never edit lifecycle fields. Only a fully successful set reports `settled`; a later block preserves evidence and reports `partial-retry-required`.

## Retry and handoff

Refresh context and replay only identical target requests; `already-recorded` is success and no evidence is duplicated. Changed identity, state, order, basis, authority, manifest, or concurrent evidence blocks without adoption. Settlement performs no workflow continuation.

Workflow-managed automation requires current formal authority, reviewer independence, neutral phase evidence, and separately owned correction authority. Record judgment before correction, rereview after any authorized correction, and return control without changing routing.

For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review. Treat reviewed architecture and ADRs as read-only.
