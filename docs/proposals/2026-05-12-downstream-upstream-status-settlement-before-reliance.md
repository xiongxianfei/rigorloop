# Downstream Upstream-Status Settlement Before Reliance

## Status

draft

## Problem

Formal review skills can approve upstream artifacts while the artifact itself still carries an earlier lifecycle status such as `draft`. Directly making review skills update proposal, spec, architecture, ADR, or plan lifecycle status is broader than the review-recording guardrail and risks mixing review output with downstream reliance behavior.

The remaining problem is reliance: downstream skills should not rely on a stale upstream artifact status when the upstream review result clearly settled that artifact.

## Goals

- Define when downstream skills must reconcile stale upstream lifecycle/status/readiness surfaces before relying on an artifact.
- Keep formal review skills from directly updating upstream lifecycle status solely as review closeout.
- Preserve artifact-specific lifecycle vocabulary such as proposal `accepted`, spec `approved`, test spec `active`, architecture `approved`, ADR `accepted` or `active`, and plan-owned readiness state.
- Make stale upstream status a visible blocker or settlement action before reliance.
- Cover downstream skills that rely on upstream artifacts: `spec`, `architecture`, `plan`, `test-spec`, `implement`, `explain-change`, and `verify`.

## Non-goals

- Do not change material-finding recording rules.
- Do not require formal review skills to update upstream artifact status directly.
- Do not introduce one universal approved status for every artifact type.
- Do not let downstream skills override unresolved material findings.
- Do not add semantic review-quality judgment in the first slice.

## Vision fit

fits the current vision

This follow-up keeps lifecycle state durable and reviewable while preserving the boundary between review output and downstream reliance.

## Recommended direction

Add a downstream reliance rule:

```text
Before a downstream skill relies on an upstream lifecycle-managed artifact, it must check whether that artifact has a clean or approving formal review result but stale owned lifecycle/status/readiness state.

If the next status is clear from the artifact type and no material findings remain open, settle the upstream artifact before relying on it.

If the next status is ambiguous or findings remain open, stop and report the blocker.
```

Candidate affected skills:

- `spec`
- `architecture`
- `plan`
- `test-spec`
- `implement`
- `explain-change`
- `verify`

The follow-up should define artifact-specific settlement targets and the blocker vocabulary in a focused spec amendment before skill implementation.

## Testing and verification strategy

- Add test-spec coverage for stale upstream status before reliance.
- Add static skill-validator checks only after the governing contract is approved.
- Use lifecycle validation where it can check concrete stale-status cases without semantic review judgment.
- Regenerate generated Codex skills and public adapters after canonical skill edits.

## Next artifacts

- proposal-review
- focused spec amendment
- architecture only if the settlement flow changes validation architecture or artifact ownership
- plan
- test-spec
- implementation
- code-review
- explain-change
- verify

## Follow-on artifacts

None yet.

## Readiness

Ready for proposal-review when the maintainer wants to schedule the downstream settlement work.
