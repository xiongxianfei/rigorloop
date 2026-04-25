# Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex architecture-review skill
Target: `docs/architecture/2026-04-24-review-finding-resolution-contract.md`
Status: revise

## Scope

This is the first-pass architecture review record for the review finding resolution contract architecture. Treat this file as append-only review history; record decisions and fixes in `docs/changes/2026-04-24-review-finding-resolution-contract/review-resolution.md`.

## Summary

Verdict: revise.

The design direction is sound, but the architecture needs tighter parser and closeout contracts before execution planning can safely proceed.

## Findings

### AR1: Review-resolution closeout fields are underspecified

Finding ID: AR1

Evidence: The approved spec requires `review-resolution.md` entries to record rationale, final action or stop state, required evidence, decision owner fields for `needs-decision`, and sub-decision records for `partially-accepted`. The architecture currently defines only `Finding ID:` and `Disposition:` labels, then models `ResolutionRecord` with optional closeout fields.

Required outcome: The architecture must define which closeout fields are parseable and which validation phase blocks on them.

Suggested resolution: Add a resolution closeout field convention defining required labels per disposition, and define separate structural validation and final-closeout validation behavior, such as a closeout mode used by `verify`, `explain-change`, and `pr`.

### AR2: Review-log exact-once parsing is underspecified

Finding ID: AR2

Evidence: The approved spec requires each Review ID to appear exactly once in `review-log.md`, but the architecture defines stable field labels only for detailed review files and does not define the log entry shape that validation should count.

Required outcome: The architecture must let validation distinguish intentional review-log entries from arbitrary prose mentions.

Suggested resolution: Require one `Review ID: <id>` label per log entry, or a single supported `Review ID` table column, and state that the validator counts only that structure.

## Dimension Results

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | `AR1` and `AR2` need revision before planning. |
| Boundary clarity | pass | Dedicated review-artifact validation is a clean boundary. |
| Data ownership | pass | Authored review artifacts and generated outputs remain separate. |
| Interface safety | concern | Parser contracts need tightening. |
| Failure handling | pass | Failure modes are explicit. |
| Security/privacy | pass | No network, secrets, or new trust boundary. |
| Performance/scalability | pass | File-local validation is appropriate. |
| Observability | pass | Validator output expectations are concrete. |
| Testing feasibility | concern | Missing parseable closeout and log fields would make tests ambiguous. |
| Complexity discipline | pass | Dedicated small validator is proportionate. |
| ADR quality | pass | No new ADR needed. |
| Plan readiness | concern | Not ready for plan until `AR1` and `AR2` are resolved. |

## Readiness

Not ready for `plan`. Revise the architecture, update `review-resolution.md`, then rerun `architecture-review` or obtain explicit architecture-review closeout.
