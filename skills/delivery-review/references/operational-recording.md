# Current operational handoff

The current supported interface is targeted-recording-v2 with rigorloop-records-v4. Use the executing package's capabilities and command help; do not infer availability from a design document or skill installation. Customer authority and selected workflow still govern. These procedures do not migrate old stores or authorize publication.

```bash
rigorloop capabilities --root .
rigorloop change context --root . --change navigation --format json
```

Use an explicit project root and Change. Review and Verification IDs are unique within that Change and record kind; findings additionally belong to a Review. Prefer meaningful stable IDs for current accounts. The project owns its stable identity configuration. If configuration or compatible storage is unavailable, report that prerequisite; do not silently create a replacement, execute SQL, or edit private runtime files.

## Read the handoff

Read goal and authority, governing basis, progress, issues/rationale, evidence, review standing and next action. Missing or conflicting support is not approval. Recorded attribution and reported applicability are not authenticated independence or mechanical proof. Completed Changes describe historical acceptance; they do not certify the current repository.

For a narrower read, change context accepts a selector body on stdin. An exact Change-only selector with observations disabled returns the complete available_selectors index, including unselected and advisory Reviews. Use that index when aggregate context is too large; never hide unresolved findings to shorten a handoff.

```json
{"schema_version":2,"interface":"targeted-recording-v2","contract":"rigorloop-records-v4","selectors":[{"kind":"change","id":"navigation"}],"include_observations":false}
```

The supported follow-ups are review show ID and verification show [ID], or another exact context selector. Attachment reads return metadata and the CLI-selected retained location. Do not scan database tables, infer records from directory listings or read large logs by default.

## Explicit updates

Ordinary mutation requests use this envelope, with the actual current revision returned by inspection:

```json
{
  "schema_version": 2,
  "interface": "targeted-recording-v2",
  "contract": "rigorloop-records-v4",
  "change_id": "navigation",
  "expected_revision": "opaque-revision-returned-by-current-inspection",
  "reads": [],
  "input": {"next_action": {"action":"Assess the complete implementation","owner":{"id":"reviewer-b","role":"review"},"rationale":"Implementation and relevant checks are complete"}}
}
```

```bash
rigorloop change update --root . --change navigation --input - --format json < update.json
```

Creation alone uses expected_revision=null. Its input supplies intent, RR request, authority, activity and nullable next_action. Updating does not infer authority or approval. Empty reads means no additional mechanical file comparison; never claim it proves unchanged bytes. Selection-based tasks let the CLI observe the explicitly selected subjects. If compared support is supplied, its selected observations must actually agree.

Load the packaged request/record schemas when constructing a task input; they define closed fields and types without exposing SQL. Unknown fields, duplicate keys and incompatible versions reject. Supply at most 64 engineering entries and at most 1 MiB of JSON per task. Omitted update sections and named neighbors remain unchanged. Issue disposition is explicit; omission never resolves an issue.

| Responsibility | Task |
| --- | --- |
| Current goal/authority/progress, work, blockers, comparable evidence, rationale, bases, plan and retention | change update |
| Prepare exact review scope without a judgment | review prepare ID |
| Actual reviewer assessment, findings, dispositions and applicability | review record ID |
| Actual scoped or final verification assessment and related evidence | verification record ID |
| Compact historical acceptance after current successful final Verify | change complete |

Review purposes are requirements, design, delivery and code. Formal approval and its current applicability are separate supplied conclusions. Advisory scope is code-only, has no formal judgment and cannot select a gate. One whole-change gate may have several correction/reassessment attempts; milestones have no approval field.

A newly accepted Basis requires its current compatible formal approval. Later adverse support remains recordable: the Basis retains its original decision and exposes a current reliance gap. Replacing Evidence or a Review never silently renews dependent Verification. Only an explicit verifier submission can renew its support; persistence does not decide whether the result is adequate.

Update at meaningful transitions and before transfer. Keep current comparable evidence summaries and useful rationale. Retain an attachment only when its bytes support a decision; evidence input can supply retain entries with a contained source, safe name and media type. Existing selected names cannot be overwritten. Routine rerun outputs remain caller-owned; retained payloads use new names when content changes. Retention explicitly drops only no-longer-needed detail, with actor and reason, while preserving unresolved obligations and remaining references.

## Interpret actual outcomes

saved establishes persistence, unchanged establishes a checked no-op, and preview establishes no reservation or future success. None grants workflow permission or an engineering judgment. JSON always reports committed=true, false or null according to known effects.

On revision conflict, read current context and reconcile the intended update. On busy, respect the other operation and retry only after reconsidering current expectations. After interruption or missing output, inspect before resubmitting; do not assume the previous operation failed. A confirmed commit survives response failure; uncertainty stays explicit. SQLite handles its internal transaction recovery. Store backup/restore/migrate are separately authorized maintenance tasks; there is no ordinary change recover command or automatic semantic replay.

Keep an existing qualified earlier executable for unmigrated legacy work when explicitly selected by project authority. The successor has no fallback writer for earlier record contracts. Historical Proposal or milestone judgments keep their original meaning and are not promoted to requirement or whole-change approval.
