# Code Review M3 R3

Review ID: code-review-m3-r3
Stage: code-review
Round: 3
Reviewer: two fresh isolated Codex code-review agents
Target: M3 correction commit 834c780b
Reviewed artifact: commit 834c780b
Reviewed milestone: M3
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M3-CR14, PBF-M3-CR15
Immediate next stage: review-resolution M3
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Review status: changes-requested
- Reviewed correction: `157843ea..834c780b`
- Prior findings: PBF-M3-CR9 through PBF-M3-CR13 resolved
- New findings: PBF-M3-CR14 and PBF-M3-CR15
- M3 closeout: blocked
- Second review: required and completed; independently changes-requested
- Next stage: review-resolution M3

## Prior-finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| PBF-M3-CR9 | resolved | Later adoption preserves immutable activation history and accepted marked artifacts survive rollback. |
| PBF-M3-CR10 | resolved | Explicit and derived feature/proof companions reject symlink escapes. |
| PBF-M3-CR11 | resolved | Valid aligned separators pass while malformed separators fail. |
| PBF-M3-CR12 | resolved | Deleted proofs and orphaned tests fail while paired deletion may pass. |
| PBF-M3-CR13 | resolved | Historical leaf and `specs/` root symlinks fail before reads. |

## Findings

### PBF-M3-CR14 - Rollback trusts self-declared current lifecycle status

Finding ID: PBF-M3-CR14
Severity: major
Location: `scripts/boundary_first_validation.py`
Evidence: In `rolled-back` state, a brand-new marked feature with current status `approved` and a structurally valid proof map returns no validation issues. Current lifecycle text is treated as proof that the artifact was accepted before rollback.
Required outcome: Rollback must stop new adoption while preserving only marked artifacts durably known to have been accepted before rollback.
Safe resolution path: Persist or derive a closed pre-rollback accepted-marker inventory and require every marked artifact during rollback to belong to it; add new-after-rollback and preserved-before-rollback regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR15 - Fixed authoritative inputs may follow external symlinks

Finding ID: PBF-M3-CR15
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: `specs/boundary-first-activation.yaml` and `specs/boundary-first-proof-model.md` are read without leaf containment. Replacing either with an outside byte-identical symlink produces no issue, and changed-spec validation also trusts the symlinked activation record.
Required outcome: Every authoritative fixed input must be a repository-contained, non-symlink regular file before any read.
Safe resolution path: Use a fixed-path containment helper for the activation record and proof-model spec in activation and changed-spec validation; add pending-state leaf-symlink regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

## Independent validation

- CMD6: 44 passed
- CMD7: passed
- CMD8: 134 passed from clean committed checkouts
- Reference projection suite: 10 passed
- Python compilation, metadata validation, and diff checks: passed
- Direct rollback and fixed-input symlink attacks produced the two findings above

## Handoff

M3 remains `resolution-needed`. Apply correction cycle 3, rerun CMD6-CMD8,
and complete same-stage independent R4 before M4.
