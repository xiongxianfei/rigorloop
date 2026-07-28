# Code Review M3 R2

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: two fresh isolated Codex code-review agents
Target: M3 correction commit 77c4a4eb
Reviewed artifact: commit 77c4a4eb
Reviewed milestone: M3
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M3-CR9, PBF-M3-CR10, PBF-M3-CR11, PBF-M3-CR12, PBF-M3-CR13
Immediate next stage: review-resolution M3
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Review status: changes-requested
- Reviewed correction: `197d150b..77c4a4eb`
- Prior findings: PBF-M3-CR1 through PBF-M3-CR8 resolved
- New findings: PBF-M3-CR9 through PBF-M3-CR13
- M3 closeout: blocked
- Second review: required and completed; independently changes-requested
- Next stage: review-resolution M3

## Prior-finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| PBF-M3-CR1 | resolved | Live Markdown, Status-owned markers, separator width, and corrected fixtures pass direct attacks. |
| PBF-M3-CR2 | resolved | Malformed records remain bounded; proof references and gap IDs fail vocabulary checks. |
| PBF-M3-CR3 | resolved | Mixed projection bytes fail even with a recomputed aggregate. |
| PBF-M3-CR4 | resolved | Pending changed feature and test paths share `BFR-MARKER-INACTIVE`. |
| PBF-M3-CR5 | resolved | Ordinary omitted and ineligible historical membership fails. |
| PBF-M3-CR6 | resolved | Explicit absolute, traversal, non-spec, and symlink paths fail. |
| PBF-M3-CR7 | resolved | Serialized private values use stable redacted identities. |
| PBF-M3-CR8 | resolved | CMD8 passes from a clean committed checkout containing `197d150b`. |

## Findings

### PBF-M3-CR9 - Activation-time history conflicts with later adoption and rollback preservation

Finding ID: PBF-M3-CR9
Severity: major
Location: `scripts/boundary_first_validation.py`
Evidence: A grandfathered accepted spec legitimately revised into a valid marked adopting contract produces stale-hash and membership failures because the immutable activation record is compared with current bytes and current unmarked eligibility. Under `rolled-back`, an already accepted marked artifact is rejected as an inactive marker.
Required outcome: Preserve activation-time inventory identities as historical evidence while validating current marked revisions independently; rollback must stop new activation without invalidating already accepted marked artifacts.
Safe resolution path: Separate immutable recorded baseline validation from current-file adoption validation, retain recorded membership after later marking, and distinguish preserved accepted marked artifacts from prohibited new rollback adoption.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR10 - Derived companion paths bypass containment

Finding ID: PBF-M3-CR10
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: A normal changed test-spec path can cause its symlinked governing feature outside the repository to be read. The symmetric derived proof companion has the same risk.
Required outcome: Every explicit or derived feature/proof path must pass one repository-contained, non-symlink top-level-spec resolver before reads.
Safe resolution path: Centralize companion resolution, reject leaf and parent-component symlinks, and add both feature-to-proof and proof-to-feature escape regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR11 - Valid aligned Markdown separators are rejected

Finding ID: PBF-M3-CR11
Severity: major
Location: `scripts/boundary_first_validation.py`
Evidence: Valid CommonMark alignment cells `:---`, `---:`, and `:---:` fail because separator validation accepts only literal `---`.
Required outcome: Reject malformed separators while accepting valid alignment forms without changing table width or column identity.
Safe resolution path: Require exact width and `^:?-{3,}:?$` per separator cell; retain the two-dash negative and add aligned feature/proof positives.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR12 - Deleted adopting test specs bypass validation

Finding ID: PBF-M3-CR12
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: Validation returns success immediately when the selected path is absent. Deleting a required test spec while its adopting feature remains therefore bypasses `BFR-PROOF-MAP-MISSING`.
Required outcome: A deleted proof map fails while its adopting feature survives; an orphaned test reports a missing feature; paired deletion may pass only when no surviving counterpart establishes an obligation.
Safe resolution path: Classify feature/test paths and inspect the contained counterpart before the nonexistence return; add deleted-feature, deleted-test, orphan, and paired-deletion cases.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR13 - Historical inventory paths may follow symlinks outside the repository

Finding ID: PBF-M3-CR13
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: Grandfathered eligibility enumeration and recorded-byte checks follow a historical path symlink to outside bytes; a recomputed active record can pass.
Required outcome: Historical inventory membership and hashes must use repository-contained, non-symlink regular files.
Safe resolution path: Apply contained no-symlink resolution to the specs root, every eligibility candidate, and every recorded historical path before reads; add leaf and parent-directory symlink regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

## Independent validation

- CMD6: 39 passed
- CMD7: passed
- CMD8: 134 passed from a clean committed checkout
- Reference projection suite: 10 passed
- Python compilation and scoped diff check: passed
- Direct near-negative attacks produced the five findings above

## Handoff

M3 remains `resolution-needed`. Record and apply correction cycle 2, rerun
CMD6-CMD8, and complete same-stage independent R3 before M4.
