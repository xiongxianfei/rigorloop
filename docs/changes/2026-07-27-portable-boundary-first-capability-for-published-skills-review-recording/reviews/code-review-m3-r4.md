# Code Review M3 R4

Review ID: code-review-m3-r4
Stage: code-review
Round: 4
Reviewer: two fresh isolated Codex code-review agents
Target: M3 correction commit 6c22abc7
Reviewed artifact: commit 6c22abc7
Reviewed milestone: M3
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M3-CR16
Immediate next stage: blocked pending renewed correction authority for review-resolution M3
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Review status: changes-requested
- Reviewed correction: `7d3abae5..6c22abc7`
- PBF-M3-CR14: partially resolved; recomputed-inventory bypass remains
- PBF-M3-CR15: resolved
- New finding: PBF-M3-CR16
- M3 closeout: blocked
- Second review: required and completed; independently changes-requested
- Next stage: blocked pending renewed correction authority for review-resolution M3

## Prior-finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| PBF-M3-CR14 | partially-resolved | An unchanged inventory rejects new markers, but adding current post-rollback path and bytes and recomputing the digest makes both changed-spec and activation validation pass. |
| PBF-M3-CR15 | resolved | Activation YAML, proof-model spec, and `specs/` parent symlinks fail before reads. |

## Findings

### Prior-finding residual

PBF-M3-CR14 remains open because adding a new marked spec's current path and
SHA-256 to `rollback_preserved_specs` and recomputing the inventory digest
makes both validators pass. Its original R3 finding record owns the unresolved
disposition.

### PBF-M3-CR16 - Rollback inventory omits accepted proof maps

Finding ID: PBF-M3-CR16
Severity: major
Location: `scripts/boundary_first_validation.py`
Evidence: A rolled-back activation record with an exact preserved feature entry but no corresponding `.test.md` returns no activation issues. CMD7 therefore permits rollback to omit an accepted proof map.
Required outcome: The rollback baseline must preserve and authenticate feature/proof pairs, including proof existence, containment, raw bytes, and coherence.
Safe resolution path: Add proof-map identities to the trusted pre-transition inventory or add a separate closed proof inventory, then align the spec, test spec, ADR, fixtures, and validator.
needs-decision rationale: The proof identity must share the unresolved trusted pre-transition evidence owner; the correction budget is exhausted.
auto_fix_class: needs-decision

## Independent validation

- CMD6: 47 passed
- CMD7: passed
- CMD8: 134 passed from clean committed checkouts
- Reference projection suite: 10 passed
- Review structure, metadata, Python compilation, and diff checks: passed
- Direct recomputed-inventory and missing-proof attacks produced the findings

## Automation boundary

The active implementation authorization granted two automatic correction
cycles, and the user previously granted one additional cycle. M3 R1-R3
corrections consumed all three. R4 therefore records the unresolved findings
but does not enter another correction until the user renews correction
authority.

## Handoff

M3 remains `resolution-needed` and the unified workflow is blocked pending
renewed correction authority. M4 and final verify cannot begin.
