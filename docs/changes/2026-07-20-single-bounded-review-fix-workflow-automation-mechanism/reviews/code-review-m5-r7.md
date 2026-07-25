# Code Review M5 R7

Review ID: code-review-m5-r7
Stage: code-review
Round: M5 R7
Reviewer: independent same-session context-reset reviewer
Target: M5 correction commit `65ca0de6`
Reviewed artifact: M5 correction commit `65ca0de6`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M5-CR14
Immediate next stage: review-resolution M5

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit range `fa9e3d54..65ca0de6`
- Requirement-fidelity gate: applicable
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shared the implementation session and does not claim blind L2 independence; the verdict comes from a fresh spec-first read of the committed diff, a risk map recorded before validation summaries, and a direct equality-spoof reproduction

## Independent risk map

### Affected behavior

- T18's single permitted read-only Git subprocess.
- Exact canonical-root command and invocation-shape enforcement.
- The saved real-`Popen` escape from the global subprocess trap.
- M5 review-resolution and rereview handoff.

### Highest-impact failure modes

- An object that is not an exact built-in tuple reaches user-defined comparison behavior inside the guard.
- A tuple subclass spoofs equality while carrying different executable arguments.
- A broader Git operation reaches the saved real `Popen`.
- Positive tests and broad smoke overstate the negative boundary they establish.

### Changed boundaries

- `scripts/test-workflow-automation.py`: test-local Git-probe runner, negative contrast test, and verification transaction trap.
- Change-local review closeout, validation evidence, and plan handoff.

### Expected evidence

- The guard checks exact built-in type before any equality operation.
- Only one built-in tuple equal to the canonical-root probe reaches the saved launcher.
- Tuple subclasses, custom comparison objects, alternate roots, extra operations, and alternate invocation shapes fail before comparison-side effects or launcher invocation.
- The successful verification transaction retains its no-external-action proof.

### Direct-inspection areas

- `run_exact_read_only_git_probe`.
- `test_verify_git_probe_allowlist_is_exact_and_root_bound`.
- `test_verify_transaction_stops_before_pr_without_external_action`.

### Intentionally out-of-scope areas

- Production canonical code-state resolution, which was unchanged by this correction.
- M6 public routing, legacy-writer cutover, generated adapters, and compatibility aliases.
- Final holistic review, explain-change, verify, and PR handoff.

### Risk classes

- Applicable: external-action containment, test-proof integrity, repository identity, and review currentness.
- Not applicable: end-user accessibility, personal-data processing, cryptographic protocol design, and deployed-service availability.

### Falsifiable questions

- Can a tuple subclass claim equality while carrying a different Git operation?
- Does the guard invoke user-defined comparison before rejecting a non-exact command type?
- Do the recorded tests contain either contrast?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M5-CR14`
- Next stage: review-resolution M5
- Review status: changes-requested
- Material findings: `BRF-M5-CR14`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m5-r7.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m5-r7`
- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution and rereview, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M5-CR14`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `fa9e3d54..65ca0de6`
- Tracked governing branch state: branch `proposal/single-bounded-review-fix-automation` at `65ca0de6`
- Governing artifacts: `BRF-R090`, `BRF-AC022`, T18, the approved architecture/ADR external-action boundary, active M5 plan, and accepted `BRF-M5-CR13` resolution
- Validation evidence challenged after risk-map recording: exact-allowlist test, six verify-selected tests, 58 full engine tests, review closeout, lifecycle/metadata/guide checks, and 11-check broad smoke

## Diff summary

The correction replaces suffix matching with a reusable test-local runner, binds its expected command to the resolved state-store root, restricts the accepted keyword set, adds common negative command-shape contrasts, and proves direct `Popen` remains patched in the integration transaction.

## Finding BRF-M5-CR14

Finding ID: BRF-M5-CR14
Severity: major
Location: `scripts/test-workflow-automation.py:97-111`
Evidence: The guard evaluates `command != expected_command` before it checks command type and accepts `isinstance(command, tuple)` rather than an exact built-in tuple. A tuple subclass can therefore override `__eq__` and `__ne__`, report equality with the permitted probe, retain underlying elements `("git", "-C", "/repo", "push", "origin", "HEAD")`, and reach the saved real `Popen`. A direct reproduction returned success and recorded that exact `git push` tuple as executed. The committed negative matrix covers built-in tuple, list, and string values, but not tuple subclasses or comparison side effects, so all recorded validation remains green despite the bypass.
Required outcome: The T18 gate must reject every command that is not an exact built-in tuple before invoking any user-defined equality behavior, and only then compare that tuple with the canonical-root probe before reaching the saved process launcher.
Safe resolution path: Reorder the predicate to check `type(command) is tuple` before equality. Add a tuple-subclass contrast whose equality methods spoof success and a non-tuple comparison sentinel whose equality methods fail if invoked; assert both are rejected, comparison is not invoked for the sentinel, and the saved launcher call count remains unchanged. Retain the existing command-shape, direct-`Popen`, and positive transaction contrasts.
needs-decision rationale: none; this is a deterministic correction inside the accepted T18 test boundary.

auto_fix_class: none

## Prior-finding reconciliation

| Prior finding | R7 result | Rationale |
| --- | --- | --- |
| `BRF-M5-CR13` | failed-remediation | The correction blocks ordinary alternate command shapes but its equality-before-exact-type guard still permits a broader operation to reach the saved launcher. |
| `BRF-M5-CR7` | reopened | The production final-code binding remains intact, but T18's external-action proof is still bypassable. Residual defect is `BRF-M5-CR14`. |

## Requirement-fidelity result

| Contract | Result |
| --- | --- |
| T18, `BRF-R090`, and `BRF-AC022` | block: the supposed exact allowlist permits a tuple-subclass command with different executable arguments |
| Approved architecture and ADR | pass for unchanged production boundaries; block only on proof of the required external-action prohibition |
| M5 plan | block: successful verification has not yet been proved against every reachable subprocess command representation |
| M6/public compatibility | pass for scope: public routing, aliases, skills, and adapters remain unchanged |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | T18 does not yet prove the `BRF-R090` external-action prohibition. |
| Test coverage | block | No tuple-subclass or comparison-before-type contrast exists. |
| Edge cases | block | A direct equality-spoof probe reaches the saved launcher with `git push`. |
| Error handling | block | Rejection occurs after user-defined comparison behavior for non-exact command types. |
| Architecture boundaries | pass | Production code and selected ownership boundaries are unchanged. |
| Compatibility | pass | The correction remains test-local and non-public. |
| Security/privacy | block | The external-action trap can be bypassed by a spoofed tuple representation. |
| Derived artifact currency | pass | No generated artifact changed; tracked lifecycle surfaces described the committed correction before R7. |
| Unrelated changes | pass | The diff is limited to the accepted correction, proof, and lifecycle evidence. |
| Validation evidence | concern | All named suites pass, but their negative domain excludes the reproduced command representation. |

## Direct proof

- A `tuple` subclass overrode equality to report a match with the permitted probe.
- Its underlying elements were `git -C /repo push origin HEAD`.
- `run_exact_read_only_git_probe` returned success and passed those underlying elements to the saved launcher.
- The committed exact-allowlist test and six verify-selected tests still pass because neither exercises this representation.

## Isolation and handoff

- This formal review is recorded.
- No automatic downstream handoff occurs because this is a direct isolated review.
- `BRF-M5-CR14` requires review-resolution before correction and M5 R8 rereview.
- No owner decision is required.
- M6, final closeout, explain-change, verify, and PR handoff remain blocked.
