# ADR-20260522-change-record-catalog-registration-and-bounded-read-model: Change Records as Registered and Queryable Catalogs

## Status

accepted

## Context

RigorLoop change records under `docs/changes/<change-id>/` have grown into durable evidence packs. They record change metadata, review evidence, validation evidence, explanations, and other proof artifacts. Two recurring failures exposed one architecture gap:

- deterministic evidence files can be useful and valid but still reach verify before the changed-path selector knows how to route them;
- agents can read an entire `change.yaml` or whole change record to answer a narrow stage-owned question because no bounded query model exists.

The approved proposal and spec frame both failures as the same missing catalog contract. The change record should not be treated as an append-only transcript where every consumer guesses how to find information. It should be treated as a catalog with registered evidence classes for writes and bounded query paths for reads.

## Decision

Treat change records as registered and queryable catalogs.

Workstream A adds an evidence registration and selector-routing architecture. Recurring deterministic change-local evidence files are classified by evidence class. A registry entry defines stable evidence class ID, allowed root, bounded filename pattern or exact filename, selector route, required validator, lifecycle stage, and allowed/required/forbidden conditions. The selector routes registered evidence files to declared check IDs and governing change metadata context. Unregistered deterministic in-repo evidence produces stable `manual-routing-required` and becomes registration debt rather than silently passing or failing only at verify.

The registry should be centralized in one registry surface when the selector architecture supports it. If the first selector slice cannot safely support a separate registry file, a selector-owned registry table with fixture-backed tests is an acceptable first implementation. Broad catch-all patterns and ambiguous matches are invalid.

Workstream B adds a bounded read/query architecture after query-helper commands are stable. `scripts/query-change-record.py` is the query surface because querying and validation have different purposes. The helper returns slices such as `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>` without executing validation commands or making `validate-change-metadata.py` responsible for read behavior.

Stage-skill guidance may reference query-helper commands only after those commands are stable, and generated adapter validation is required when canonical stage-skill text changes. Full reads remain valid for forensic reconstruction, disputed evidence, selector debugging, migration checks, unsupported query shapes, and whole-record review.

Workstream A ships before Workstream B so CI-routing risk and skill/read-behavior risk remain separately reviewable and rollbackable.

## Alternatives considered

### Do nothing

Rejected because useful new evidence files would continue to risk late `manual-routing-required`, and agents would continue broad-reading change records for narrow questions.

### Patch only the current selector blocker

Rejected as the durable architecture because one-off selector routes fix instances, not the recurring mechanism. Instance fixes may still happen as CI maintenance, but they do not replace registered evidence classes.

### Add only the query helper

Rejected because bounded reads do not solve deterministic routing gaps for new evidence files.

### Add only evidence registration

Rejected because selector safety improves, but stage-owned reads remain discipline-based instead of mechanism-supported.

### Ship both workstreams in one implementation slice

Rejected because selector routing and skill/query guidance have different risk profiles and rollback surfaces. They belong in one architecture decision but separate implementation slices.

## Consequences

- New recurring change-local evidence classes require registry coverage or stable registration-debt diagnostics.
- Selector regression coverage must include registered evidence files, unregistered deterministic evidence, broad-pattern rejection, and ambiguous match rejection.
- Verify should no longer be the first stage to discover deterministic evidence routing gaps introduced earlier in a change.
- `manual-routing-required` remains a diagnostic but not a durable workaround for deterministic in-repo evidence.
- `scripts/query-change-record.py` becomes the bounded read surface for common change-record questions.
- `validate-change-metadata.py` remains a validator and does not acquire query semantics.
- Stage-skill read guidance becomes command/slice-specific after query-helper commands stabilize.
- Existing valid change records remain valid; first-slice work does not bulk-migrate historical evidence files.
- Full forensic reconstruction remains available when bounded slices are insufficient or unsafe.

## Follow-up

- Update the canonical architecture package to record registered evidence routing, registration debt, bounded query helper responsibilities, and Workstream A before Workstream B sequencing.
- Create architecture-review evidence for this ADR and canonical package update.
- Create the execution plan after architecture-review approves the design.
