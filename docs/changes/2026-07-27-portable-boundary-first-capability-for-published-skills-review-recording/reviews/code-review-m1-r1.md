# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1 commit f6617839
Reviewed artifact: commit f6617839
Reviewed milestone: M1
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M1-CR1
Immediate next stage: review-resolution M1
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: review invocation manifest, this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: PBF-M1-CR1
- Next stage: review-resolution M1
- Review status: changes-requested
- Material findings: PBF-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#code-review-m1-r1`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: PBF-M1-CR1
- Verify readiness: not-claimed

## Review inputs

- Diff surface: commit `f6617839`, inspected blind-first before implementation notes or validation-result summaries.
- Tracked governing branch state: approved proposal, spec, architecture, ADR, plan, test spec, and prior formal review evidence are tracked through commit `71af80d1`.
- Governing clauses: PBF-R046 through PBF-R050, test-spec T1 and T2, the test-spec security/privacy verification boundary, and plan milestone M1.
- Invocation evidence: `review-invocation-code-review-m1-r1.yaml`.

## Risk map

- Affected behavior: canonical-reference reads, ten skill-local writes, closed projection checks, and inventory identity.
- Highest-impact failures: repository-boundary escape through symlinked parents, incomplete consumer detection, stale bytes accepted, or non-reproducible identity.
- Changed boundaries: canonical source ownership, filesystem projection, governed consumer membership, and raw-byte digest.
- Expected evidence: direct negative tests for missing, stale, extra, unknown mode, symlink escape, and reproducible bytes.
- Direct inspection: path resolution, symlink handling, write behavior, unexpected projection enumeration, digest serialization, and portable reference content.
- Intentionally out of scope: skill resource maps, record validators, activation, adapters, installed targets, and final verification.
- Applicable risks: filesystem integrity, generated-output currency, contract fidelity, and compatibility.
- Non-applicable risks: external actions, credential handling, and network access because M1 performs only repository-local file projection.
- Falsifiable question: can a source or destination escape the repository through a symlinked ancestor? Yes; the direct reproduction below proves the destination case.

## Requirement-property decomposition

| Spec clause | Requirement property | Required surface | Result | Evidence |
| --- | --- | --- | --- | --- |
| PBF-R046-PBF-R048 | one canonical skill-local path, ten closed consumers, raw-byte identity | projection constants, writer, checker, tests | pass | Constants and byte comparisons cover the exact canonical path and ten projected paths. |
| PBF-R049 | deterministic validation covers mapped-resource presence and byte parity | checker and tests | pass | Missing, stale, unexpected, leaf-symlink, and digest cases have direct tests. |
| Test-spec security/privacy verification | path validation rejects symlink escape | source and destination path handling, tests | fail | A symlinked `skills/workflow/references` parent writes the canonical bytes outside the repository and returns `ok=True`. |
| PBF-R050 | deterministic code does not claim semantic completeness | CLI output and method text | pass | Results report projection integrity only; the method assigns semantic completeness to review. |
| T2/PBF-R044 | shared method contains portable method, not stage-local policy | canonical reference and content test | pass | The reference defines vocabulary and proof method while omitting handoff, recording, and readiness policy. |

## Diff summary

M1 adds one canonical boundary-first method, a closed ten-skill projection inventory, raw-byte digest support, a check/write CLI, seven unit tests, ten byte-identical skill-local projections, and focused implementation evidence.

## Findings

### PBF-M1-CR1 - Projection paths can escape the repository through symlinked parents

Finding ID: PBF-M1-CR1
Severity: major
Location: `scripts/boundary_first_reference.py:75`
Evidence: `project_reference()` rejects a symlink only when the source or final target itself is a symlink. It calls `target.parent.mkdir(...)` and `target.write_bytes(...)` without rejecting symlinked ancestors. A direct reproduction made `skills/workflow/references` a symlink to a sibling temporary directory; `mode="write"` returned `ok=True` and created `boundary-first-method-v1.md` outside the repository. The existing leaf-symlink test still passed, so it does not cover this escape.
Required outcome: Source reads and projection checks/writes must fail closed when any existing path component from the repository root to the canonical source or projected destination is a symlink, and write mode must not create or change an outside file.
Safe resolution path: Add a regression that constructs a symlinked projection-parent directory and proves `check` and `write` reject it without outside mutation. Add a shared repository-contained path guard and apply it before source reads, parent creation, target writes, and unexpected-projection enumeration. Add the equivalent canonical-source-parent regression if the same guard owns both paths.
needs-decision rationale: none
auto_fix_class: declared-safe
affected_paths: scripts/boundary_first_reference.py; scripts/test-boundary-first-reference.py
resolution_recipe: Add failing source-parent and destination-parent symlink-escape tests, then add one shared path-component guard used before every source or projection filesystem operation.
named_inputs: test-spec T1; test-spec Security/privacy verification; canonical source and closed ten-consumer inventory
named_outputs: deterministic projection error with no outside read or write
forbidden_paths: specs/; skills/; docs/architecture/; docs/adr/
acceptance_criteria: both parent-symlink regressions fail before the fix and pass after it; outside sentinel bytes remain unchanged; the existing seven tests and projection check still pass
required_validation_commands: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`
scope_preservation_rule: change only shared projection path validation and focused regression tests; do not change the approved method, consumers, digest, skill projections, or activation state
production_code_change: yes
behavior_test: `BoundaryFirstReferenceTests.test_parent_symlink_escape_fails_without_outside_mutation`

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | The test spec explicitly requires symlink-escape rejection, but parent symlinks are followed. |
| Test coverage | block | Leaf-symlink coverage passes while the parent-symlink escape remains untested. |
| Edge cases | block | The direct parent-symlink reproduction returns success and mutates an outside path. |
| Error handling | block | The invalid filesystem topology is accepted instead of failing before mutation. |
| Architecture boundaries | pass | The source, consumer list, and digest follow the accepted one-source projection ADR. |
| Compatibility | pass | Closed paths, raw bytes, and CLI modes match the approved M1 contract. |
| Security/privacy | block | A repository-local projection operation can cross the repository filesystem boundary. |
| Derived artifact currency | pass | Current ten projections match the canonical source; this does not cure unsafe future writes. |
| Unrelated changes | pass | Commit `f6617839` contains only M1 implementation and evidence. |
| Validation evidence | concern | Seven tests and the live parity check pass, but the adversarial reproduction proves the suite is incomplete. |

## Requirement-fidelity receipt

- Relevant spec clauses decomposed: yes
- Property matrix complete: yes for M1
- Multi-surface contracts identified: yes
- Validator assertions checked against spec: yes
- Compressed requirement risk: present; parent-symlink rejection was omitted from implementation and tests
- Requirement-fidelity no-finding rationale: not applicable because PBF-M1-CR1 is material

## Residual risks

M2 through M4 remain out of scope. M1 cannot close until path-component validation is corrected and independently rereviewed.

## Milestone handoff

- Reviewed milestone: M1
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2, M3, M4
- Next stage: review-resolution M1
- Final closeout readiness: not ready; PBF-M1-CR1, M2 through M4, final holistic review, explain-change, and verify remain open.
