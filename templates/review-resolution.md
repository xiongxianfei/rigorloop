# Review Resolution: Change Title

## Summary

Closeout status: open

Review closeout: review-id

- Reviews covered: `review-id`
- Findings resolved: 0
- Unresolved findings: 0
- Final result: record the current closeout result in one sentence.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| finding-id | accepted | resolved | Summarize the chosen action and final state. |

## Common Resolution Metadata

Use this section only when multiple findings share owner, stage,
validation target, or validation evidence.

- Owner: owner or role
- Owning stage: stage
- Validation target: command, artifact, or proof expected
- Validation evidence: command result, artifact link, or closeout proof

## Finding Details

### review-id

#### finding-id - Short title

Finding ID: finding-id
Disposition: accepted
Status: resolved
Owner: owner or role
Owning stage: stage
Chosen action: state the action taken, stop state, or follow-up.
Rationale: explain why the disposition and action are correct.
Validation target: command, artifact, or proof expected.
Validation evidence: command result, artifact link, or closeout proof.

Optional review-fix auto-resolution fields, only when the workflow driver
auto-applied or stopped on a review-fix finding:

Review-fix auto-resolution: yes
Review-fix auto-applied: yes or no
Driver classification: mechanical | format-preserving | exact-reviewer-wording | status-normalization-with-evidence | recording-repair | cross-reference-repair | validation-command-shape-repair | not-auto-safe
Reason auto safe: deterministic rationale, or omit when not-auto-safe.
Files changed: changed paths, or omit when not-auto-safe.
Finding evidence: yes or no
Deterministic required outcome: yes or no
Review rerun: same-review rerun ID after auto-application.
Same-review rerun: yes or no
Reviewed artifact current: yes or no
Deterministic patch target: yes or no
Small diff: yes or no
Stop reason: required when not auto-applied.

## Shared Validation Evidence

| Validation area | Result | Notes |
|---|---|---|
| validation area | pass | Summarize shared proof once and reference it from finding details. |

## Closeout Checklist

- [ ] Every material finding has a disposition.
- [ ] Every accepted finding has a chosen action.
- [ ] Every rejected finding has rationale.
- [ ] Every deferred finding has follow-up or explicit no-follow-up rationale.
- [ ] Every `needs-decision` finding is resolved or blocks closeout.
- [ ] Validation evidence is recorded.
- [ ] Closeout status is correct.
