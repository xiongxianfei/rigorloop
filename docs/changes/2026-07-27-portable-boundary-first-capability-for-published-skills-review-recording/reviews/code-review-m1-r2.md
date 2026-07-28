# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M1 correction commit 0b198866
Reviewed artifact: commit 0b198866
Reviewed milestone: M1
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M1-CR2, PBF-M1-CR3
Immediate next stage: review-resolution M1
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: R2 invocation manifest, this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: PBF-M1-CR2, PBF-M1-CR3
- Next stage: review-resolution M1
- Review status: changes-requested
- Material findings: PBF-M1-CR2, PBF-M1-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#code-review-m1-r2`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: PBF-M1-CR2, PBF-M1-CR3
- Verify readiness: not-claimed

## Review inputs

- Diff surface: correction commit `0b198866`, inspected before prior finding content and implementation validation summaries.
- Governing clauses: PBF-R046 through PBF-R050, test-spec T1, security/privacy verification, and M1 recovery boundaries.
- Tracked governing branch state: all governing artifacts and the R1 finding resolution are tracked through `d2732f8c`.
- Invocation evidence: `review-invocation-code-review-m1-r2.yaml`.

## Risk map

- Affected behavior: filesystem containment for canonical-source reads and projection checks and writes.
- Highest-impact failures: remaining ancestor escape, outside mutation before rejection, broken-symlink bypass, or loss of closed consumer detection.
- Changed boundaries: path-component validation and unexpected-projection enumeration.
- Expected evidence: direct source-parent, destination-parent, leaf-symlink, outside-sentinel, missing, stale, and unexpected-consumer proof.
- Direct inspection: path guard ordering, symlink predicates, parent creation, read and write call sites, and enumeration traversal.
- Intentionally out of scope: method content, skill mappings, activation, packages, installed targets, and later milestones.
- Applicable risks: filesystem integrity, generated-output currency, regression safety, and test isolation.
- Non-applicable risks: external actions, credentials, and network access.

## Diff summary

The correction adds one shared path-component guard, applies it before source and destination operations, replaces glob traversal with symlink-avoiding enumeration, and adds source-parent and destination-parent escape regressions.

## Prior-finding reconciliation

| Finding | R2 result | Evidence |
| --- | --- | --- |
| PBF-M1-CR1 | resolved | The guard rejects source, parent, and leaf symlink components before reads or writes; the outside sentinel stays unchanged in both check and write modes. |
| PBF-M1-CR2 | new-finding | Independent second review and direct reproduction show symlinked unexpected skill or reference directories are silently skipped while the check returns success. |
| PBF-M1-CR3 | new-finding | The regression fixture creates sibling temporary directories that are outside the cleanup scope of `TemporaryDirectory`. |

## Findings

### PBF-M1-CR2 - Symlinked unexpected consumers evade closed-inventory validation

Finding ID: PBF-M1-CR2
Severity: major
Location: `scripts/boundary_first_reference.py:92`
Evidence: `_unexpected_projections()` skips a symlinked ungoverned skill directory or symlinked `references` directory instead of rejecting it. Independent second review reproduced both forms. A local direct probe created `skills/proposal` as a symlink to an outside skill containing the boundary reference; `project_reference(..., mode="check")` returned `ok=True` and no errors.
Required outcome: Unexpected-consumer enumeration must reject symlinked skill or reference directory components without traversing them, while preserving the rule that every extra boundary reference or unsafe consumer topology fails explicitly.
Safe resolution path: Add regressions for an ungoverned symlinked skill root and an ungoverned skill with a symlinked `references` directory. Change enumeration to emit a stable symlink-topology error for both cases without reading through either link.
needs-decision rationale: none
auto_fix_class: declared-safe
affected_paths: scripts/boundary_first_reference.py; scripts/test-boundary-first-reference.py
resolution_recipe: Add the two failing unexpected-consumer symlink tests, then reject the encountered symlink component during non-recursive skill/reference enumeration.
named_inputs: test-spec T1; test-spec Security/privacy verification; closed governed consumer inventory
named_outputs: deterministic unsafe unexpected-consumer error and unsuccessful projection result
forbidden_paths: specs/; skills/; docs/architecture/; docs/adr/
acceptance_criteria: both unexpected-consumer symlink forms fail explicitly without following the link; missing, stale, ordinary unexpected, and ten-consumer live checks remain correct
required_validation_commands: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`
scope_preservation_rule: change only unexpected-consumer enumeration and focused tests; do not broaden consumers or change method bytes
production_code_change: yes
behavior_test: `BoundaryFirstReferenceTests.test_unexpected_consumer_symlink_topologies_fail_closed`

### PBF-M1-CR3 - Symlink regressions leak their outside fixtures

Finding ID: PBF-M1-CR3
Severity: minor
Location: `scripts/test-boundary-first-reference.py:134`
Evidence: Both new regressions derive an outside path as `root.parent / f"{root.name}-outside"` or `root.parent / f"{root.name}-source"`. Cleanup registered by `make_repository()` removes only `root`, not those siblings. Repeated direct test runs left multiple matching directories in `/tmp`, so the test suite is not filesystem-isolated.
Required outcome: Every outside fixture created by the symlink regressions must have explicit managed cleanup while remaining outside the repository fixture.
Safe resolution path: Allocate each outside path with its own `tempfile.TemporaryDirectory()`, register its cleanup, and use that directory as the symlink target. Add an assertion or direct before/after proof that cleanup removes the outside fixture.
needs-decision rationale: none
auto_fix_class: mechanical
auto_fix_kind: test-fixture-cleanup
affected_paths: scripts/test-boundary-first-reference.py
deterministic_authority: PBF-M1-CR2 safe resolution path and Python TemporaryDirectory cleanup contract
required_validation: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Source and destination containment now satisfy the named symlink-escape boundary. |
| Test coverage | concern | Required escape paths are covered, but their fixtures are not fully managed. |
| Edge cases | pass | Parent, leaf, missing, stale, unexpected, raw-byte, and unknown-mode paths have direct proof. |
| Error handling | pass | Symlink topology fails before source read, parent creation, or destination write. |
| Architecture boundaries | pass | The correction preserves the one-source, closed-consumer, shared-digest architecture. |
| Compatibility | pass | Existing CLI modes, diagnostics, consumer paths, and reference bytes remain stable. |
| Security/privacy | pass | The implementation no longer follows an existing source or destination symlink component. |
| Derived artifact currency | pass | Ten projections and the inventory digest remain current. |
| Unrelated changes | concern | Test runs leave unmanaged temporary siblings outside the fixture root. |
| Validation evidence | concern | Nine tests pass, but passing runs themselves reproduce the cleanup defect. |

## Second-review evidence

- Second reviewer: isolated `/root/m1_second_review`
- Second-review result: changes-requested
- Agreement: PBF-M1-CR1 is resolved.
- New finding: PBF-M1-CR2 was independently reproduced for both ungoverned skill-root and references-directory symlinks.
- Confidence: high.

## Requirement-fidelity receipt

- Relevant spec clauses decomposed: yes
- Property matrix complete: yes for M1 correction scope
- Multi-surface contracts identified: yes
- Validator assertions checked against spec: yes
- Compressed requirement risk: present in closed unexpected-consumer enforcement
- Requirement-fidelity no-finding rationale: not applicable because PBF-M1-CR2 and PBF-M1-CR3 are recorded

## Milestone handoff

- Reviewed milestone: M1
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2, M3, M4
- Next stage: review-resolution M1
- Final closeout readiness: not ready; PBF-M1-CR2, PBF-M1-CR3, and downstream work remain open.
