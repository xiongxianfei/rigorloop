# Code Review M3 R5

Review ID: code-review-m3-r5
Stage: code-review
Round: 5
Reviewer: two fresh isolated Codex code-review agents
Target: M3 correction commit 95c7f72d
Reviewed artifact: commit 95c7f72d
Reviewed milestone: M3
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M3-CR17
Immediate next stage: blocked pending owner decision and renewed correction authority
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Review status: changes-requested
- Reviewed correction: `c335e8a5..95c7f72d`
- PBF-M3-CR14: resolved for M3 and safely deferred to M4
- PBF-M3-CR16: resolved for M3 and safely deferred to M4
- New finding: PBF-M3-CR17
- M3 closeout: blocked
- Second review: required and completed; clean-with-notes disagreement
- Normalized gate result: changes-requested
- Next stage: blocked pending owner decision and renewed correction authority

## Prior-finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| PBF-M3-CR14 | resolved for M3; deferred to M4 | Null, missing, fake, malformed, and recomputed receipt identities cannot authorize rolled-back activation or markers in M3. |
| PBF-M3-CR16 | resolved for M3; deferred to M4 | Missing proof maps cannot bypass M3; the M4 contract requires paired feature/proof identities. |
| PBF-M3-CR15 | resolved | Fixed authoritative paths remain contained before reads. |

## Finding

### PBF-M3-CR17 - M4 receipt has no executable writer contract

Finding ID: PBF-M3-CR17
Severity: major
Location: `specs/boundary-first-proof-model.test.md`; `docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md`
Evidence: CMD12 limits the activation writer to the proof-model status and activation record only, excluding `specs/boundary-first-rollback-receipt.yaml`. M4 targeted validation invokes neither CMD12 nor another rollback writer, although PBF-R057, T13, the ADR, and the plan require receipt preparation, binding, transition, recovery, and validation.
Required outcome: Define one M4 command that owns receipt creation, activation binding, rollback validation, interruption recovery, and evidence; map it to T13 and the M4 proof and validation surfaces.
Safe resolution path: Either extend CMD12 explicitly or add a dedicated rollback transaction command, then align the command table, T13, milestone proof map, M4 validation list, and recovery contract.
needs-decision rationale: The owner must choose whether activation and rollback share CMD12 or use distinct commands, and the authorized correction cycle is exhausted.
auto_fix_class: needs-decision

## Independent validation

- CMD6: 48 passed
- CMD7: passed
- CMD8: 134 passed
- Reference projection suite: 10 passed
- Review structure, metadata, lifecycle, compilation, and diff checks: passed
- Direct rolled-back activation and marker attacks fail closed

## Automation boundary

The fourth authorized M3 correction cycle produced R5. R5 records the new
command-ownership decision but does not begin another correction without
renewed authority.

## Handoff

M3 remains `resolution-needed`. M4 and final verify remain blocked.
