# Code Review M5 R1: Compact activation integration

Review ID: code-review-m5-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M5 coherent activation and full-workflow integration
Reviewed milestone: M5
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M5-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Open blockers: CCSR-M5-CR1
- Next stage: implement correction, then Code Review M5 R2
- Review status: changes-requested
- Required review-resolution: yes
- Verify readiness: not-claimed

## Finding CCSR-M5-CR1

Finding ID: CCSR-M5-CR1
Severity: major
Location: `packages/rigorloop/dist/lib/workflow-context.js`
Evidence: The compact exact-change branch projected the parsed coordinator directly instead of delegating to the complete-set compact reader. It therefore skipped transaction-recovery checks, complete authoritative-set validation, and direct evidence-subject drift observation. The project branch also selected active changes only through legacy `workflow_state.lifecycle_state`, so a compact change was omitted when no exact change ID was supplied. Route and other skills consume `workflow-context`; either path could therefore hide or omit current compact state even though `compact project` returned the correct bounded result.
Required outcome: Both exact-change and project-level `workflow-context` paths must use the same bounded compact reader as `compact project`, surface drift and recovery failures, and include active compact candidates without reintroducing historical scanning.
Safe resolution path: Delegate compact projection to `executeCompactCli`, map its validated result into the compatibility context envelope, add public exact-change drift and no-change discovery regressions, rerun the full Node suite and broad smoke, then request Code Review M5 R2.
needs-decision rationale: none; SR-20, SR-21, TG-12, and TG-22 already require one bounded authoritative projection path.

## Review judgment

The activation discriminator, prospective writer, stable current-set operations, rollback behavior, adapter candidate metadata, and legacy write denial otherwise align with the approved package. The finding is blocking because the documented primary routing projection did not yet share the compact reader's correctness boundary.

## No downstream handoff

M5 remains open until the correction is recorded, exact tests and broad smoke pass on the corrected bytes, and an independent clean M5 rereview is recorded.
