# Learn Session: Review Artifact Field Shape

## Frame

- Date: 2026-05-20
- Status: session-recorded; durable lesson routed to topic guidance
- Trigger: maintainer explicitly invoked `learn` after review artifact validation caught that a material finding block used prose bullets instead of machine-readable `Finding ID`, `Severity`, `Location`, `Evidence`, `Required outcome`, and `Safe resolution path` fields.
- Trigger type: explicit maintainer request after validation catch.
- Scope: root cause and first-pass prevention practices for material finding records in detailed review artifacts.
- Session path: `docs/learn/sessions/2026-05-20-review-artifact-field-shape.md`

## Evidence Reviewed

- Current failed edit and corrected edit in `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md`
- Review artifact validator failure:
  - `review-log Material findings reference unknown Finding ID PFA-M1-CR1`
  - `review-log Open findings reference unknown Finding ID PFA-M1-CR1`
  - `review-resolution.md references unknown Finding ID`
- Current valid review record after adding explicit fields.
- `scripts/review_artifact_validation.py` field parsing behavior for `Finding ID`.
- `scripts/test-review-artifact-validator.py` fixture examples that use explicit material-finding labels.
- Prior learn session `docs/learn/sessions/2026-05-05-review-record-placement.md`.
- Prior learn session `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md`.

## Exclusions

- No workflow, spec, validator, or skill behavior is changed by this session.
- No review-resolution fix for `PFA-M1-CR1` is performed here.
- No PR readiness, verify readiness, or code-review closeout is claimed.

## Prior Learnings Reviewed

- `2026-05-05-review-record-placement` established that detailed review records are conditional, but material findings require durable traceability.
- `2026-05-06-isolated-review-material-finding-records` established that material findings must not remain chat-only and that isolation does not suppress recording.

## Observations

### O1: The reviewer wrote human-readable finding bullets but missed the parser contract

The first review record used bullets for `Location`, `Evidence`, `Requirement`, `Required outcome`, and `Safe resolution path`. To a human, the finding looked complete. To the validator, it did not define a material finding because `Finding ID:` was absent from the finding block.

Evidence:

- The validator reported that `PFA-M1-CR1` was unknown from `review-log.md` and `review-resolution.md`.
- Adding explicit `Finding ID: PFA-M1-CR1`, `Severity: major`, `Location: ...`, `Evidence: ...`, `Required outcome: ...`, and `Safe resolution path: ...` made structure validation pass.

### O2: The root cause is source-shape substitution

The root cause was not missing intent or missing evidence. The root cause was substituting a prose review-writing habit for the repository's machine-readable field shape.

The reviewer satisfied the conceptual checklist but did not instantiate the structural checklist before linking the finding from `review-log.md` and `review-resolution.md`.

### O3: This is a first-pass completeness failure, not an unavoidable validator discovery

The required field names are known and stable. The code-review skill, review artifact validator fixtures, and prior learn sessions all point to the same boundary: material findings are detailed records with explicit labeled fields. A first-pass review record should use that field block before any validation run.

### O4: Review artifact validation is still useful as a guardrail

The validator caught the issue before the malformed record could persist. The failure mode was recoverable and local. The goal is not to rely less on validation, but to write the validator-shaped record first and use validation as confirmation.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | Topic guidance | Maintainer explicit learn request plus repeated review-record evidence | The problem is a reusable pattern: human-readable findings can be invalid if they do not use the parser-owned material-finding labels. |
| O2 | durable-lesson | durable-lesson | Topic guidance | Maintainer explicit learn request plus validator evidence | The root cause generalizes to other structured artifacts: do not replace required field labels with prose bullets. |
| O3 | process-follow-up | observation | None | Current evidence | Existing skill/validator/test surfaces already own the rule; no artifact update is needed unless recurrence continues after this session. |
| O4 | observation | observation | None | Current validation evidence | Validation worked as intended; the lesson is to pre-shape the record before validation. |

Contributor confirmation status: confirmed by explicit maintainer request for root cause and best-practice capture.

## Routing Results

- Observation routing: recorded in this session.
- Durable lesson routing: added `docs/learn/topics/review-artifact-recording.md`.
- Artifact update routing: none; existing authoritative artifacts already require material finding fields.
- Decision routing: none.
- Process follow-up routing: none scheduled.

## Root Cause

The immediate miss was writing a material finding as readable Markdown instead of as validator-readable fields.

The deeper workflow cause was insufficient first-pass use of the output contract:

1. The review content was drafted from memory and narrative style.
2. The review log and review-resolution were updated as if the finding ID existed structurally.
3. The validator then discovered that no `Finding ID:` field had been parsed from the detailed review record.

The failure was not a lack of knowledge about the finding. It was a shape mismatch between human prose and the repository's durable artifact contract.

## Best Practices

1. Start material findings from the field block, not from prose.

Use this order every time:

```text
Finding ID:
Severity:
Location:
Evidence:
Required outcome:
Safe resolution path:
```

Add narrative context only after these fields exist.

2. Treat cross-file references as requiring a parsed source field.

Before adding a finding ID to `review-log.md` or `review-resolution.md`, confirm the detailed review record contains a literal `Finding ID: <id>` line.

3. Use validator fixture shape as the example source.

When unsure, inspect `scripts/test-review-artifact-validator.py` fixture records rather than improvising a Markdown shape.

4. Validate before committing review records.

For open findings, run structure mode first:

```bash
python scripts/validate-review-artifacts.py --mode structure docs/changes/<change-id>
```

Use closeout mode only when review-resolution is intentionally closed.

5. Make the first-pass checklist structural as well as conceptual.

For material findings, "complete" means both:

- the finding has evidence, required outcome, and safe resolution path;
- the finding uses the exact labels the review artifact parser expects.

## Follow-Ups

- None scheduled.
- If this recurs, consider a small review-record snippet or reusable review artifact helper in the action-owning skill or validator fixture docs. This session alone does not change workflow policy.