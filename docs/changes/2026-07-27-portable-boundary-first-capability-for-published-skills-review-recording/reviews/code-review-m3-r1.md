# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: two fresh isolated Codex code-review agents
Target: M3 implementation commit 12c0981b
Reviewed artifact: commit 12c0981b
Reviewed milestone: M3
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M3-CR1, PBF-M3-CR2, PBF-M3-CR3, PBF-M3-CR4, PBF-M3-CR5, PBF-M3-CR6, PBF-M3-CR7, PBF-M3-CR8
Immediate next stage: review-resolution M3
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Reviewed range: `e4ae823e..12c0981b`
- Material findings: PBF-M3-CR1 through PBF-M3-CR8
- Open blockers: all eight findings
- Next stage: review-resolution M3
- Remaining implementation milestones: M3, M4
- Second review: required and completed; independently changes-requested
- M3 closeout: blocked

## Review inputs

- Approved feature spec: `specs/boundary-first-proof-model.md`
- Approved test spec: `specs/boundary-first-proof-model.test.md`
- Accepted ADR:
  `docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md`
- Active plan:
  `docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md`
- Neutral invocation:
  `review-invocation-code-review-m3-r1.yaml`

## Risk map

The review treated malformed Markdown, closed-vocabulary ordering, exact proof
ownership, activation identity, historical compatibility, changed-path
containment, privacy-bounded diagnostics, and reproducible selector execution
as the highest-risk surfaces. Active-state writing, final inventory
generation, adapter/install parity, publication, network behavior, runtime
attestation, and M4 rollback remain outside this milestone.

## Findings

### PBF-M3-CR1 - Markdown structure is not context-safe

Finding ID: PBF-M3-CR1
Severity: blocker
Location: `scripts/boundary_first_validation.py`; durable feature fixtures
Evidence: A full boundary record inside a fenced code block passes; a marker outside `## Status` passes; a malformed table separator passes. The positive fixtures also omit the required Status-owned marker placement.
Required outcome: Parse only live Markdown, require exactly one marker after the lifecycle value in `## Status`, and validate exact table separators.
Safe resolution path: Add fence-aware section parsing, Status marker checks, exact separator validation, corrected positive fixtures, and missing/duplicate/misplaced-marker regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR2 - Malformed rows and identifiers bypass bounded vocabulary handling

Finding ID: PBF-M3-CR2
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: A short boundary-definition row can cause `_feature_contract()` to raise `IndexError`; proof references serialized without comma-space reach reference consistency diagnostics; uncovered-gap IDs bypass stable-ID validation.
Required outcome: Malformed records never traceback, and reference lists and every required stable identifier fail in the vocabulary phase before consistency.
Safe resolution path: Short-circuit proof validation on malformed governing records, make `_feature_contract()` shape-safe, validate proof references and gap IDs, and add ordering regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR3 - Aggregate projection identity can bless mixed bytes

Finding ID: PBF-M3-CR3
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: Changing one governed projection and recomputing `projection_sha256` yields no issue because activation validation never compares each projection directly with the canonical bytes.
Required outcome: Every governed projection must equal the canonical reference bytes independently of the aggregate digest.
Safe resolution path: Compare each projection raw hash with the canonical raw hash before accepting the inventory digest and add a mixed-projection regression.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR4 - Test-spec validation bypasses inactive marker enforcement

Finding ID: PBF-M3-CR4
Severity: blocker
Location: `scripts/boundary_first_validation.py`; `scripts/validation_selection.py`
Evidence: Under pending activation, a marked feature path returns `BFR-MARKER-INACTIVE`, while its changed matching test-spec path validates successfully; normal selector routing passes only the changed test-spec path.
Required outcome: Feature and test-spec paths must share one activation and feature-marker gate.
Safe resolution path: Apply activation-marker checks before branching by feature or test-spec path and add pending feature/test pairs.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR5 - Active grandfathered inventory membership is not validated

Finding ID: PBF-M3-CR5
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: Validation checks only supplied entries and their hashes. It does not reject omitted eligible accepted/approved/active top-level feature specs or included nonterminal specs.
Required outcome: In active and rolled-back baselines, inventory membership must equal the deterministic eligible set while semantic revision classification remains with `spec-review`.
Safe resolution path: Enumerate top-level lifecycle-eligible feature specs, compare exact sorted membership, and add historical, in-flight, new, omitted, and ineligible fixtures. Pending may retain its empty pre-activation record.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR6 - Changed paths can escape the repository

Finding ID: PBF-M3-CR6
Severity: blocker
Location: `scripts/boundary_first_validation.py`; `scripts/validate-boundary-first.py`
Evidence: `--path /etc/passwd` returns passed; absolute, traversal, non-spec, and symlink-escaping targets are not rejected before reads.
Required outcome: Accept only normalized repository-relative top-level feature and test-spec paths whose resolved target remains inside the repository.
Safe resolution path: Add strict lexical and resolved containment checks before filesystem access plus CLI regressions for absolute, traversal, non-spec, and symlink escape.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR7 - Diagnostics expose offending private payloads

Finding ID: PBF-M3-CR7
Severity: blocker
Location: `scripts/boundary_first_validation.py`; `scripts/test-boundary-first-validation.py`
Evidence: `ValidationIssue.as_dict()` emits `offending_value` verbatim. The privacy test checks only field names, so a credential-like invalid value appears unchanged in JSON output.
Required outcome: Diagnostics retain stable failure identity without emitting credential-like or private payloads.
Safe resolution path: Emit a deterministic redacted digest/shape for offending values and add negative assertions that literal payloads never appear.
needs-decision rationale: none
auto_fix_class: declared-safe

### PBF-M3-CR8 - Recorded selector evidence is not reproducible from the review commit

Finding ID: PBF-M3-CR8
Severity: major
Location: `scripts/test-select-validation.py`; uncommitted workflow-coordinator bugfix
Evidence: A clean archive of `12c0981b` reports one selector failure and 133 passes. The local 134-pass result depended on the separately authorized but uncommitted workflow-coordinator correction in `scripts/workflow_automation.py` and its regression test.
Required outcome: CMD8 must pass from committed repository state without hidden worktree dependencies.
Safe resolution path: Complete and validate the already-authorized coordinator bugfix as its own scoped commit, then rebase the M3 correction evidence on that committed state and rerun the full selector suite.
needs-decision rationale: No new owner decision is required because the user previously authorized the coordinator bugfix; it must remain a separate change slice.
auto_fix_class: none

## Requirement-fidelity receipt

| Proof area | Result | Evidence |
| --- | --- | --- |
| T4 concise and complex records | block | Positive fixtures violate marker placement and malformed separators can pass. |
| T5 closed vocabulary ordering | block | Reference serialization and gap IDs bypass vocabulary checks. |
| T7 proof ownership and coverage | block | Malformed governing rows can traceback. |
| T8 pending and mixed activation | block | Mixed projection bytes can pass with a recomputed aggregate. |
| T9 compatibility inventory | block | Eligible inventory membership is not compared. |
| T15 validation selection | block | Path containment and clean-commit CMD8 fail. |
| T17 privacy evidence | block | Offending values are emitted verbatim. |
| Semantic non-overclaim | pass | Structurally valid semantic omissions remain accepted. |

## Independent validation

- `python scripts/test-boundary-first-validation.py`: 30 passed
- `python scripts/validate-boundary-first.py --check`: passed
- `python scripts/test-select-validation.py`: primary clean archive failed
  1 / passed 133; second reviewer workspace passed 134 because the unrelated
  coordinator correction was present
- Python compilation and scoped diff checking: passed
- Direct adversarial reproductions confirmed every finding above

## Handoff

M3 is `resolution-needed`. Record accepted dispositions, apply the bounded
corrections, produce clean committed CMD6-CMD8 evidence, and run same-stage
independent code-review R2 before M4.
