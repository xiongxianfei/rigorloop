# Code Review M3 R1: CLI trust boundary

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M3 compact semantic-operation contract and current implementation foundation
Reviewed milestone: M3
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M3-CR1
Recording status: recorded

## Result

- Open blockers: CCSR-M3-CR1
- Next stage: review-resolution and upstream correction
- Required review-resolution: yes
- Verify readiness: not-claimed

## Finding CCSR-M3-CR1

Finding ID: CCSR-M3-CR1
Severity: major
Location: `specs/compact-current-state-change-record.md` SR-22, SR-32, SR-41; the compact operation schema and validator; architecture and delivery allocation
Evidence: The approved operation envelope required a caller-supplied `authority` value and described the local CLI as checking claimed authority. Any process able to invoke the local CLI can choose that value, so the field cannot authenticate a caller or grant permission. Retaining it would turn workflow responsibility metadata into a misleading security claim.
Required outcome: Remove caller identity and authority claims from the operation envelope; derive structural operation eligibility from current lifecycle state, active work, operation target, and exact identities; retain owner/reviewer/producer labels only as responsibility and provenance; state that actual execution access belongs to OS, sandbox, or enclosing-runner controls; align Proposal, Design, Delivery, schema, implementation, and tests.
Safe resolution path: Accept the finding, route the direction correction to Proposal, obtain fresh Proposal Review, register and approve the exact revised Design package, approve the revised Delivery package, align the M1/M2 foundation, and rereview the affected implementation before continuing M3.
needs-decision rationale: none; a self-asserted request field provides no authentication, and the user's direction explicitly rejects treating the CLI as a permission principal.

## Handoff

M3 remains implementing and blocked on the upstream correction chain. The 36 focused compact tests pass for the corrected local foundation, but prior Proposal, Design, Delivery, M1, and M2 judgments are stale until rereviewed against the refined trust boundary.
