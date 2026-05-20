---
name: spec
description: Use this fixture when validating generated output asset presence.
---

# Spec

## Resource map

- COPY `assets/spec-skeleton.md` when creating a new spec.
  Fill: status, summary, requirements, acceptance criteria, decision log.
  Do not emit unfilled placeholders.
- COPY `assets/requirement-row.md` once per normative requirement.
  Fill: requirement ID, statement, rationale, acceptance link, owner.
  Do not emit unfilled placeholders.
- COPY `assets/acceptance-criterion-row.md` once per acceptance criterion.
  Fill: criterion ID, requirement link, condition, expected outcome.
  Do not emit unfilled placeholders.
- COPY `assets/decision-log-row.md` once per recorded decision.
  Fill: date, decision, reason, alternatives rejected.
  Do not emit unfilled placeholders.

## Expected output

- Compact output summary: status, requirements, acceptance criteria, decision log.
