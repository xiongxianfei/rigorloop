# Clean Review Receipt Root Example

This example is non-normative. Authoritative rules live in `specs/formal-review-recording.md`.

```text
docs/changes/2026-05-12-example-spec-review-recording/
  change.yaml
  review-log.md
  reviews/spec-review-r1.md
```

`review-resolution.md` is absent because the review has no material findings, no blocking findings, and no other review-resolution trigger.

## Minimal change metadata

```yaml
change_id: 2026-05-12-example-spec-review-recording
title: Example spec review recording
classification: review-recording
risk: low
artifacts:
  spec: specs/example.md
review:
  status: approved
  unresolved_items: 0
  review_log: docs/changes/2026-05-12-example-spec-review-recording/review-log.md
```

## Review log

```md
# Review Log

| Review ID | Stage | Round | Reviewed artifact | Record | Status | Material findings | Recording |
|---|---|---:|---|---|---|---:|---|
| spec-review-r1 | spec-review | 1 | `specs/example.md` | `reviews/spec-review-r1.md` | approved | 0 | recorded |
```

## Clean receipt

```md
# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Target: specs/example.md
Reviewed artifact: specs/example.md
Review date: 2026-05-12
Reviewer: Codex spec-review
Recording status: recorded
Status: approved

## Outcome

- Review status: approved
- Material findings: none
- Blocking findings: none

## Scope checked

- Reviewed the example spec requirements, edge cases, and lifecycle readiness.

## No-finding statement

Clean formal review completed with no material findings.
```
