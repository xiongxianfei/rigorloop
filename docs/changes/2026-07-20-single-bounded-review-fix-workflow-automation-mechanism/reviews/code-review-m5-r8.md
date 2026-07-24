# Code Review M5 R8

Review ID: code-review-m5-r8
Stage: code-review
Round: M5 R8
Reviewer: independent same-session context-reset reviewer
Target: M5 correction commit `4dc746d2`
Reviewed artifact: M5 correction commit `4dc746d2`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: clean-with-notes
Review status: clean-with-notes
Review date: 2026-07-24
Recording status: recorded
Material findings: None
Immediate next stage: implement M6

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit range `d61a8e7c..4dc746d2`
- Requirement-fidelity gate: applicable to T18, `BRF-R090`, and `BRF-AC022`
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shared the implementation session and does not claim blind L2 independence; the verdict comes from a fresh spec-first diff read, a risk map fixed before recorded validation summaries, and independent command-representation probes

## Independent risk map

### Affected behavior

- T18's single permitted read-only Git subprocess.
- Exact command-type rejection before comparison.
- Equality-spoof resistance and saved-launcher containment.
- M5 milestone review closeout and M6 handoff.

### Highest-impact failure modes

- Exact-type rejection still occurs after user-defined behavior.
- A tuple subclass reaches the launcher by spoofing comparison.
- Tightening rejects the canonical positive probe.
- Validation counts obscure missing negative-domain proof.

### Changed boundaries

- `scripts/test-workflow-automation.py`: test-local Git-probe predicate and two negative proof surfaces.
- Change-local review closeout, validation evidence, and plan handoff.

### Expected evidence

- Non-exact types are rejected before equality.
- Tuple subclasses and custom comparison objects invoke neither comparison nor launcher behavior.
- The exact canonical-root built-in tuple executes exactly once.
- Existing alternate-root, extra-operation, argument, type, shell, and direct-`Popen` traps remain intact.

### Direct-inspection areas

- `run_exact_read_only_git_probe`.
- `test_verify_git_probe_allowlist_is_exact_and_root_bound`.
- `test_verify_git_probe_rejects_before_custom_comparison`.
- Verification transaction subprocess patching.

### Intentionally out-of-scope areas

- M6 public routing, legacy-writer cutover, generated adapters, and compatibility aliases.
- Final holistic review, explain-change, verify, and PR handoff.
- Unchanged production canonical code-state resolution.

### Risk classes

- Applicable: external-action containment, proof integrity, repository identity, and review currentness.
- Not applicable: end-user accessibility, personal-data processing, cryptographic protocol design, and deployed-service availability.

### Falsifiable questions

- Can a tuple subclass invoke comparison or reach the launcher?
- Can a non-tuple object's comparison methods run before rejection?
- Does the exact positive tuple still execute exactly once?
- Do the committed tests directly prove these outcomes?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review receipt, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: none for M5
- Next stage: implement M6
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m5-r8.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m5-r8`; no new finding resolution required
- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Milestone closeout: closed
- Remaining implementation milestones: M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Clean-review sufficiency receipt

- Review target identity: commit `4dc746d2`
- Independence level: `L1-same-session-context-reset`
- Governing artifacts inspected: `BRF-R090`, `BRF-AC022`, T18, approved external-action architecture/ADR boundary, M5 plan, and `BRF-M5-CR14` resolution
- Risk classes considered: external-action containment, test-proof integrity, repository identity, review currentness, compatibility, generated artifacts, and scope containment
- Adversarial hypotheses tested: equality-spoofing tuple subclass, non-tuple comparison side effect, saved-launcher reachability, exact positive probe regression, and validation-domain insufficiency
- Direct proofs performed: a tuple subclass and custom sentinel were rejected; neither equality method ran; the launcher received only the exact canonical-root probe; both committed focused regressions and all seven verify-selected tests passed
- Validation evidence challenged: focused test results were compared with the changed branches and independent probes; the 59-test engine and 11-check broad-smoke counts were treated as supporting rather than sufficient evidence
- Unreviewed or uncertain surfaces: M6 public activation, final holistic review, final verification, and PR handoff
- Confidence: high for the bounded R8 correction
- No-finding rationale: Exact built-in type is now checked as the first short-circuit predicate, direct proof establishes no user-defined comparison or launcher access for non-exact types, and the positive and prior negative command matrix remain covered.

## Review inputs

- Review surface: commit `4dc746d2` against parent `d61a8e7c`.
- Tracked governing branch state: approved specification, test specification, architecture, ADR, active plan, and closed review resolution are tracked.
- Direct review proof: independent equality-spoof, comparison-sentinel, positive-launcher-count, focused regression, and verify-selected runs.
- Released validation evidence: 12 code-state, 59 engine, M5 selected suites, review/lifecycle/skill/metadata validation, and final 11-check broad smoke.

## Diff summary

The correction changes the Git-probe predicate from equality-before-`isinstance` to exact built-in tuple type before equality.

It adds an equality-spoofing tuple subclass to the rejected command matrix and a separate custom comparison sentinel proving rejection occurs without `__eq__`, `__ne__`, or saved-launcher invocation.

## Prior-finding reconciliation

| Prior finding | R8 result | Evidence |
| --- | --- | --- |
| `BRF-M5-CR14` | resolved | Exact built-in type short-circuits before equality; spoofed tuple and comparison-sentinel probes invoke no comparison or launcher behavior. |
| `BRF-M5-CR13` | resolved | The complete matrix now rejects ordinary alternate command shapes and equality-spoofed tuple representations. |
| `BRF-M5-CR7` | resolved for milestone-local proof | The production final-code boundary remains intact and T18's subprocess, socket, URL, shell, and direct-`Popen` traps retain negative proof. |

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | T18 directly proves the `BRF-R090` stop before PR/external-action boundary for M5. |
| Test coverage | pass | Exact positive, ordinary negative shapes, tuple subclass, comparison sentinel, shell, and direct-`Popen` cases are present. |
| Edge cases | pass | Non-exact types fail before comparison; spoofed equality cannot reach the launcher. |
| Error handling | pass | Every rejected representation raises the same fail-closed external-action assertion. |
| Architecture boundaries | pass | The correction is test-local and does not change production ownership or persistence. |
| Compatibility | pass | Public workflow commands, legacy aliases, adapters, and M6 activation remain unchanged. |
| Security/privacy | pass | The changed trap no longer permits user-defined comparison to bypass subprocess containment; no secret or credential surface changed. |
| Derived artifact currency | pass | No generated or derived public artifact changed. |
| Unrelated changes | pass | The diff is limited to the accepted test correction and lifecycle evidence. |
| Validation evidence | pass | Direct adversarial proof covers the changed predicate; focused and broad repository checks support the result. |

## Requirement-fidelity result

| Contract property | Result | Evidence |
| --- | --- | --- |
| Successful verify stops before PR | pass | The transaction still reports `pr` next without invoking PR or external action. |
| External actions remain unreachable | pass for M5 | Only the exact root-discovery tuple reaches the saved launcher; other subprocess/network/shell surfaces remain trapped. |
| Failure does not trigger repair | pass | The unchanged verification-failure test remains in the seven-test verify selection. |
| Public activation remains deferred | pass | No public skill, command adapter, alias, or generated adapter changed. |

## No-finding rationale

The R8 correction addresses the shared cause rather than adding another value-specific exception: representation type is established before any comparison behavior. Independent probes and committed regressions both prove the formerly exploitable path is rejected without side effects, while the intended Git root probe remains executable. No contradictory in-scope evidence was found.

## Residual risks

- M6 public activation and complete composed-engine proof remain unimplemented and unreviewed.
- A final holistic code review is still required after M6 before explain-change or verify.
- The existing lifecycle merge-language warning remains non-blocking baseline evidence.

## Milestone handoff

- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no; all 92 material findings are resolved
- Remaining in-scope implementation milestones: M6
- Next stage: implement M6
- Final closeout readiness: not ready; M6, final holistic review, explanation, verification, and PR handoff remain

This direct review is isolated and does not start M6 automatically.
