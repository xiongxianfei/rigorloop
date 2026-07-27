# Boundary-First Proof Modeling Test-Spec Review R21

Review ID: test-spec-review-r21

Stage: test-spec-review

Round: 21

Reviewer: Codex test-spec-review skill with context-separated independent reviewer

Target: specs/rigorloop-workflow.test.md

Reviewed artifact: R54/R26/R20-synchronized proof map at 688fff3c

Status: changes-requested

Review status: changes-requested

Material findings: BFP-TSR21-1

Recording status: recorded

Immediate next stage: test-spec revision

Implementation handoff: not-allowed

Review date: 2026-07-27

Context separation mechanism: separate-agent

Reviewed commit: `688fff3c`

## Finding

### BFP-TSR21-1 - Parent-only candidate isolation lacks direct proof

Finding ID: BFP-TSR21-1

Severity: major

Location: `specs/rigorloop-workflow.test.md`, T49/T52

Evidence:

T52 proves invariant comparison, alternative stage-owned decompositions,
scenario-bound reviews, and diagnostic behavior, but does not directly assert
that candidate paths, identities, and bytes are absent from the child-readable
workspace, every serialized lifecycle request surface, and child access
observations.

Required outcome:

Directly prove candidates remain input-bound for parent comparison while
unavailable to every child stage.

Safe resolution:

Inspect the complete assembled child-workspace inventory, every serialized
stage request/prompt/attachment/artifact context, and child access
observations. Require candidate paths, identities, and content to be absent,
while the authoritative scenario is present where specified. Add a contrast
that deliberately exposes a candidate and fails before accepted stage output
or publication. Confirm only the parent invariant evaluator consumes candidate
bytes.

## Other dimensions

All other review dimensions passed. The input identities are current; T49/T52
cover the invariant projection, stage-owned alternatives, scenario-bound
reviews, dedicated diagnostic, preflight exclusion, and M2 command/evidence
mapping.

## Handoff

Revise the proof map and rerun independent test-spec review. Implementation
remains blocked.
