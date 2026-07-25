# Code Review M5 R6

Review ID: code-review-m5-r6
Stage: code-review
Round: M5 R6
Reviewer: independent same-session context-reset reviewer
Target: M5 correction commit `1b8a8ec4`
Reviewed artifact: M5 correction commit `1b8a8ec4`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M5-CR13
Immediate next stage: review-resolution M5

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit range `a60bd1f7..1b8a8ec4`
- Requirement-fidelity gate: applicable
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shared the implementation session and does not claim blind L2 independence; the verdict comes from a fresh read of the committed diff, governing clauses, focused tests, and a direct subprocess-allowlist contrast

## Independent risk map

### Affected behavior

- Git repository classification before provider selection.
- State-store repository-root ownership before verification readiness.
- Immutable final-review commit binding.
- T18 subprocess, network, and external-action containment.
- M5 review-resolution and rereview handoff.

### Highest-impact failure modes

- A test-only provider executes inside a Git worktree.
- A mutable review revision silently retargets newer code.
- Ambiguous Git classification falls through to fixture authority.
- The external-action trap exempts a command broader than the intended read-only Git probe.
- Passing validation overstates the proof actually enforced by the trap.

### Changed boundaries

- `scripts/workflow_code_state.py`: Git classification and reviewed-commit validation.
- `scripts/workflow_automation.py`: state-store root validation before readiness.
- `scripts/test-workflow-code-state.py`: top-level, subdirectory, linked-worktree, revision-expression, and ambiguous-classification contrasts.
- `scripts/test-workflow-automation.py`: T18 read-only Git subprocess allowance and pre-readiness root rejection.

### Expected evidence

- Provider injection is rejected for a Git root, subdirectory, and linked worktree.
- True non-Git fixtures remain explicit and test-only.
- Only a canonical full commit object ID satisfies the final-review anchor.
- Ambiguous Git classification fails before provider invocation.
- The T18 subprocess exception is an exact command-and-root allowlist; every extra operation or alternate root remains trapped.

### Direct-inspection areas

- `resolve_canonical_code_state`.
- `GitCodeStateAnchorResolver.resolve`.
- `coordinate_non_public_implementation_stage`.
- T18's `allow_read_only_git_probe`.
- Provider and verify-focused regressions.

### Intentionally out-of-scope areas

- M6 public activation and legacy-writer cutover.
- Final holistic review of the complete six-milestone branch.
- PR, publication, deployment, merge, and release actions.

### Risk classes

- Applicable: authorization, repository identity, review currentness, verification freshness, external-action containment, and proof integrity.
- Not applicable: end-user accessibility, personal-data processing, cryptographic protocol design, and deployed-service availability.

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M5-CR13`
- Next stage: review-resolution M5
- Review status: changes-requested
- Material findings: `BRF-M5-CR13`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m5-r6.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m5-r6`
- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution and rereview, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M5-CR13`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `a60bd1f7..1b8a8ec4`
- Tracked governing branch state: branch `proposal/single-bounded-review-fix-automation` at `1b8a8ec4`
- Governing artifacts: approved unified automation spec, active test spec, approved architecture and ADR, active M5 plan, R5 review record, and the `BRF-M5-CR12` resolution
- Validation evidence challenged: twelve provider tests, five verify-focused engine tests, recorded full automation suites, lifecycle closeout, and final-source broad smoke
- Conditional evidence rationale: the architecture, ADR, R5 record, and resolution define the exact code-state and external-action boundaries changed by this correction

## Diff summary

The correction replaces `.git` marker inference with canonical Git top-level discovery, validates state-store root identity before readiness, rejects mutable review revision expressions, preserves a true non-Git fixture provider, and narrows the T18 subprocess trap to commands ending in the Git top-level probe arguments.

## Finding BRF-M5-CR13

Finding ID: BRF-M5-CR13
Severity: major
Location: `scripts/test-workflow-automation.py:4130-4167`
Evidence: The new `allow_read_only_git_probe` does not compare the subprocess command with one exact expected tuple. It permits every tuple with length at least five whose first element is `git` and whose final two elements are `rev-parse`, `--show-toplevel`, then invokes it through the saved real `Popen` while the global `Popen` trap is bypassed. A direct predicate probe showed that the intended command, an alternate-root command, and `("git", "-C", "/repo", "push", "origin", "HEAD", "rev-parse", "--show-toplevel")` are all classified as allowed. The latter two are outside the intended single read-only probe. The five passing verify tests execute only the intended tuple, so they do not prove that extra Git operations remain trapped. This weakens T18 and reopens the external-action proof established for `BRF-M5-CR7`.
Required outcome: T18 must allow exactly the single repository-root-bound read-only Git discovery command required by canonical classification and must reject every alternate root, additional Git operation, argument insertion, direct `Popen`, shell, network, and external-action attempt.
Safe resolution path: Build the expected tuple from the state store's canonical root and compare the observed command for exact equality before invoking the saved `Popen`. Prefer a small test-local exact-command runner that can be exercised directly. Add negative contrasts for an alternate root, an inserted Git operation such as `push`, extra prefix/suffix arguments, list-versus-tuple substitutions, and direct `Popen`; retain the existing successful verification transaction as the positive contrast.
needs-decision rationale: none; T18 and `BRF-R090` already require the external-action trap, and exact allowlisting is inside the approved M5 test scope.

auto_fix_class: none

## Prior-finding reconciliation

| Prior finding | R6 result | Rationale |
| --- | --- | --- |
| `BRF-M5-CR12` | resolved | Git classification precedes provider selection, state-store root validation precedes readiness, mutable review revisions are rejected, and the direct provider/revision contrasts pass. |
| `BRF-M5-CR7` | reopened | The production final-code binding remains present, but the new broad subprocess exception weakens the external-action trap that formed part of CR7's validation proof. Residual defect is `BRF-M5-CR13`. |

## Requirement-fidelity result

| Contract | Result |
| --- | --- |
| `BRF-R043c` and `BRF-R044` | pass for the reviewed correction: repository classification, root identity, and immutable review commit fail closed |
| `BRF-R085` | pass for canonical final-code currentness within the reviewed M5 harness |
| T18, `BRF-R090`, and `BRF-AC022` | block: the subprocess trap's exception is not an exact read-only command allowlist |
| Approved architecture and ADR | pass for canonical provider and review-anchor ownership |
| M6/public compatibility | pass for scope: public and legacy routing remain unchanged |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | T18's external-action containment proof admits commands beyond the required read-only probe. |
| Test coverage | block | No test challenges the allowlist with alternate roots or inserted Git operations. |
| Edge cases | block | Direct predicate contrasts show both alternate-root and extra-operation tuples are allowed. |
| Error handling | pass | Git absence, ambiguous classification, root mismatch, and mutable reviewed revisions fail closed. |
| Architecture boundaries | pass | Production resolver, provider, state-store root, and immutable anchor ownership match the ADR. |
| Compatibility | pass | The M5 harness remains non-public and legacy behavior is unchanged. |
| Security/privacy | block | The saved real `Popen` can be reached by commands broader than the intended read-only exception. |
| Derived artifact currency | pass | Plan, review resolution, metadata, and implementation handoff were synchronized before R6. |
| Unrelated changes | pass | The commit is limited to CR12 code, tests, and required lifecycle evidence. |
| Validation evidence | concern | Focused and broad suites pass, but they exercise only the positive subprocess exception and cannot establish the claimed negative boundary. |

## Direct proof

- The allowlist predicate returned `True` for the intended probe.
- It also returned `True` for the same probe against `/other`.
- It returned `True` for a tuple containing `push origin HEAD` before the final probe arguments.
- `python scripts/test-workflow-code-state.py` passed twelve provider tests.
- `python scripts/test-workflow-automation.py -k verify` passed five tests; none includes a negative allowlist contrast.

## Isolation and handoff

- This formal review is recorded.
- No automatic downstream handoff occurs because this is a direct isolated review.
- `BRF-M5-CR13` requires review-resolution before correction and M5 R7 rereview.
- No owner decision is required.
- M6, final closeout, explain-change, verify, and PR handoff remain blocked.
