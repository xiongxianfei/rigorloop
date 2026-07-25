# Code Review M5 R2

Review ID: code-review-m5-r2
Stage: code-review
Round: M5 R2
Reviewer: independent context-reset reviewer
Target: M5 correction commit `1498cefd`
Reviewed artifact: M5 correction commit `1498cefd`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M5-CR6, BRF-M5-CR7, BRF-M5-CR8, BRF-M5-CR9
Immediate next stage: review-resolution M5

## Invocation manifest

- Review ID: `code-review-m5-r2`
- Review target: commit `1498cefd`
- Review base: commit `34a1360f`
- Reviewed milestone: `M5`
- Invocation mode: workflow-managed milestone rereview
- Independence level: `L2-context-reset`
- Initial packet: the commit range, changed paths, approved specification, approved test specification, active plan milestone, approved architecture, and formal code-review criteria
- Initially withheld: prior review conclusions and finding content, implementation validation summaries, implementation safety narrative, desired outcome, and correction eligibility
- Requirement-fidelity gate: applicable
- Risk tier: elevated
- Second-review gate: not reached because material findings stop the review

## Independent risk map

### Affected behavior

- Repository-derived implementation-correction authority and bounded mutation.
- Prepared-receipt ordering, capability binding, rollback, convergence, and rereview routing.
- Canonical milestone and review-evidence selection.
- Final verification authorization and execution readiness.
- Closed-vocabulary validation for correction recipes, evidence, and state.

### Highest-impact failure modes

- An implementation correction mutates code or review evidence without complete reviewer-owned authority.
- Correction scope is broader than the stage policy, parent authorization, effective capability, or reviewed finding permits.
- Partial mutation or failed validation leaves code, evidence, and automation state inconsistent.
- Stale, contradictory, ambiguous, or symlink-escaped lifecycle evidence is accepted as canonical.
- A verify capability is derived or consumed from synthetic, stale, incomplete, or caller-asserted closeout evidence.
- Verification failure repairs code automatically or successful verification crosses the PR/external-action boundary.
- A repeated milestone target or review occurrence silently rebinds to another milestone.

### Changed boundaries

- `scripts/workflow_automation.py` now coordinates implementation correction and verification evidence.
- `scripts/workflow_automation_state.py` now interprets plan, review, resolution, explanation, promotion, branch, and verification artifacts.
- `scripts/workflow_automation_policy.py` projects implementation-correction mutation authority.
- `scripts/validate_workflow_automation.py` validates the persisted correction basis and recipe vocabulary.
- Focused tests exercise the coordinator, state interpreter, policy, validator, and lifecycle artifacts.

### Expected evidence

- Direct tests for exact reviewer classification and deterministic recipe binding.
- Direct tests for stale identities, ambiguous milestones, conflicting reviews, unknown values, and path escape.
- Transaction tests proving the prepared receipt predates mutation and rollback restores all partially changed files.
- Convergence tests proving the unresolved set strictly shrinks and accepted findings remain on the same milestone.
- Verification tests grounded in repository artifacts, including final review, resolution, explanation, promotion, branch state, command identity, failure pause, and external-action traps.
- Static and lifecycle validation showing the active plan and formal review artifacts remain synchronized.

### Direct-inspection areas

- Correction recipe parsing and capability derivation.
- Mutation-path containment and identity checks.
- Review-resolution and review-log update logic.
- Receipt preparation/finalization and rollback paths.
- Canonical review selection and stale-review invalidation.
- Verification-readiness derivation and final verify transaction.
- Negative tests for each fail-closed boundary.

### Intentionally out-of-scope areas

- Public `$workflow auto: <stage>` activation and legacy adapter cutover, which remain M6 work.
- Final holistic review of the complete multi-milestone branch.
- PR creation, publication, deployment, merge, destructive Git, credentials, and network execution.

### Risk classes

- Applicable: authorization, integrity, transaction recovery, lifecycle-state consistency, path containment, compatibility, and external-action containment.
- Not applicable: end-user UI accessibility, personal-data processing, cryptographic protocol design, and deployed-service availability.

### Falsifiable review questions

1. Can any correction mutation occur without an active effective capability whose parent, occurrence, basis, recipe, and scope all match?
2. Can a valid reviewer-owned correction class be compressed into a narrower implementation-only vocabulary without an explicit approved contract?
3. Can a correction close global review resolution while unrelated findings remain open?
4. Can a later review for the same milestone evade staleness detection through display-text variation?
5. Can verification readiness substitute a plan identity for the final diff or accept promotion/branch evidence that does not prove the required closeout facts?
6. Can validation or verification failure leave mutated files, a consumed capability, or a completed receipt?
7. Can any successful path invoke or imply PR, network, credential, publication, deployment, merge, or destructive-Git action?

## Phase receipts

### `risk-map-recorded`

- Status: completed
- Recorded before validation summaries, evidence menus, implementation notes, and prior finding content were consulted
- Risk map identity: this review record at commit-worktree state immediately after invocation-manifest creation

### `evidence-menu-released`

- Status: completed
- Released after `risk-map-recorded`
- Evidence menu: M5 commit diff; `BRF-R033`-`BRF-R046`, `BRF-R060`-`BRF-R090`; T13, T17, T18, and T24; M5 plan scope and handoff; approved automation architecture; focused runtime, validator, and test modules

## Requirement-fidelity decomposition

| Requirement properties | Required surfaces |
| --- | --- |
| `BRF-R033`-`BRF-R046`: executable capability is parent-bound, stage-relative, current, subset-scoped, immutable in scope, and conflict-free | policy registry, capability derivation, persisted-state validator, coordinator, negative tests |
| `BRF-R060`-`BRF-R065`: review remains independent; implementation correction uses the reviewer’s complete recorded classification and recipe; missing or divergent authority pauses | review parser, correction coordinator, review-resolution mutation, convergence checks, negative tests |
| `BRF-R067`: verification failure pauses and performs no automatic repair | verify coordinator, transaction state, failure tests |
| `BRF-R068`-`BRF-R077`: mutation is preceded by one capability-bound prepared receipt and interrupted work reconciles without unsafe retry or authority rebinding | state adapter, coordinator, completion verifier, rollback path, recovery tests |
| `BRF-R078`-`BRF-R085`: stage owners remain authoritative; stage policies bound mutation; milestone review/resolution and final holistic review/explanation/verification remain distinct and ordered | policy registry, stage-native evidence parser, routing, plan parser, integration tests |
| `BRF-R086` and `BRF-R090`: successful verification stops before PR and performs no prohibited external action | verify completion verifier, coordinator result, fail-on-call external-action proof |
| T13 | eligible reviewer recipe execution, missing/changed class, non-shrinking set, budget, scope, stale evidence, and validation failure |
| T17 | milestone order, validation-before-review, approval, truthful resolution, and no target rebinding |
| T18 | closed milestones, clean final review, current explanation, verification failure/no repair, success-before-PR, and external-action trap |
| T24 | all M5 implementation integration remains unreachable from public command surfaces |

### `evidence-results-released`

- Status: completed
- Released after the independent risk map and requirement-property decomposition
- Focused correction tests: 13 passed
- Focused verification tests: 4 passed
- Focused non-public-boundary tests: 5 passed
- State/recovery suite: 60 passed
- Policy suite: 15 passed
- Python compilation and commit-range diff check: passed
- Evidence challenge result: current fixtures do not exercise the preserved correction vocabulary, global closeout with unrelated open findings, milestone-title drift, post-explanation source drift, or a fail-on-call external-action trap

### `prior-findings-released`

- Status: completed
- Released after blind-first source inspection, requirement decomposition, focused validation, and adversarial probes
- Prior review consulted: `code-review-m5-r1`

### `verdict-recorded`

- Status: completed
- Verdict: `changes-requested`
- Requirement-fidelity outcome: failed
- Automatic downstream handoff: stopped

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M5-CR6`, `BRF-M5-CR7`, `BRF-M5-CR8`, `BRF-M5-CR9`
- Next stage: review-resolution M5
- Review status: changes-requested
- Material findings: `BRF-M5-CR6`, `BRF-M5-CR7`, `BRF-M5-CR8`, `BRF-M5-CR9`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m5-r2.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m5-r2`
- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution and rereview, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M5-CR6`, `BRF-M5-CR7`, `BRF-M5-CR8`, `BRF-M5-CR9`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `34a1360f..1498cefd`
- Tracked governing branch state: branch `proposal/single-bounded-review-fix-automation` at `1498cefd`
- Governing artifacts: approved unified automation spec, preserved review-finding-resolution contract, approved test spec, architecture and ADR, and active M5 plan
- Validation evidence: focused correction, verify, non-public, state/recovery, and policy suites plus direct adversarial probes

## Diff summary

The correction commit adds a repository-backed implementation-correction transaction, stronger plan and formal-review parsing, verification-basis artifact loading, expanded implementation-correction capability mutation categories, stricter persisted recipe validation, and focused regression tests. It also records the five R1 findings as resolved and returns M5 to rereview.

## Findings

### BRF-M5-CR6 — Correction authority compresses the preserved recipe contract and bypasses the stage-policy mutation bound

Finding ID: BRF-M5-CR6
Severity: major
Location: `scripts/workflow_automation.py:596-643`, `scripts/workflow_automation.py:2810-2815`, `scripts/workflow_automation_policy.py:560-567`, `scripts/workflow_automation_policy.py:587`, and `scripts/validate_workflow_automation.py:1535-1605`
Evidence: The repository contract preserves `mechanical` and `declared-safe` correction classes, seven closed mechanical kinds, multi-path recipes, and the declared-safe required fields. The new loader and persisted-state validator accept only `mechanical`, only `exact-approved-rename`, and exactly one affected path. Separately, the `review-resolution` stage policy still permits only `change-local-evidence`, while capability derivation labels the capability-wide category set as the stage-policy bound and therefore permits `production-code`, `tests`, and review-evidence mutation. A direct policy projection reports `stage_permitted=change-local-evidence` while the executable capability admits all four categories.
Required outcome: The executable correction contract must project the complete preserved reviewer vocabulary, or explicitly pause only under an approved unsupported-operation rule, and every actual mutation category must be authorized by the bound stage policy as well as the capability and parent.
Safe resolution path: Introduce typed recipe variants for all preserved mechanical kinds and declared-safe fields, validate each exact shape and path set, represent the review-resolution stage's permitted mutation set without a singular-category mismatch, and add property-by-surface tests proving each accepted class/kind and every policy-exceeding category.
needs-decision rationale: none; the approved cross-spec ledger already preserves this vocabulary and the architecture makes the stage policy normative.
auto_fix_class: none

### BRF-M5-CR7 — Verification currentness is not bound to the final code state and T18 still lacks an external-action trap

Finding ID: BRF-M5-CR7
Severity: major
Location: `scripts/workflow_automation.py:328-445` and `scripts/test-workflow-automation.py:3873-3923`
Evidence: `resolve_verification_readiness` compares `Final diff identity` to the closed plan file hash, not to a commit, tree, or final diff identity. Promotion, branch-state, and verification-command artifacts require only matching `Stage` and `Status` labels. An adversarial probe changed a repository source file after the final review and explanation without changing those six evidence files; verification readiness still succeeded. The positive T18 transaction similarly writes the plan hash as `Final diff identity` and trusts an `External actions performed: no` report field; it installs no fail-on-call double for PR, push, network, credentials, publication, deployment, merge, destructive Git, or external mutation.
Required outcome: Verification authority must become stale whenever the reviewed/explained final code state changes, and T18 must directly prove that all prohibited external-action surfaces remain uncalled.
Safe resolution path: Bind final review, explanation, promotion, branch state, and verification command evidence to one canonical commit/tree or deterministic final-diff identity; require the stage-owned fields and finalized receipts that establish those facts; then add source-drift and fail-on-call external-action regressions around the composed verify transaction.
needs-decision rationale: none; BRF-R043c, BRF-R085, BRF-R090, and T18 already define these boundaries.
auto_fix_class: none

### BRF-M5-CR8 — Latest-review selection compares milestone display text instead of occurrence identity

Finding ID: BRF-M5-CR8
Severity: major
Location: `scripts/workflow_automation_state.py:527-570`
Evidence: `_canonical_review_occurrence` decides whether a later review is applicable by comparing the entire `Reviewed milestone` string. The structured workflow contract binds repeated stages to `milestone_id`, not to a mutable title. A direct probe recorded R1 approved for `M2. Old title` and a later R2 inconclusive for `M2. Renamed title`; the helper returned the stale R1 as canonical.
Required outcome: Any later formal review of the same milestone occurrence must invalidate the earlier occurrence regardless of title or other presentation text.
Safe resolution path: Parse and compare the closed milestone ID from each reviewed-milestone field, bind it to the active plan occurrence, preserve separate final-scope handling, and add same-ID/renamed-title plus malformed-ID regressions.
needs-decision rationale: none; repeated-stage occurrence identity is already settled by BRF-R014 through BRF-R016 and BRF-R084.
auto_fix_class: none

### BRF-M5-CR9 — Automatic correction can close the global resolution gate while unrelated findings remain open

Finding ID: BRF-M5-CR9
Severity: major
Location: `scripts/workflow_automation.py:574-590` and `scripts/workflow_automation.py:2175-2198`
Evidence: The correction loader validates only entries matching the current review's finding IDs. After resolving those entries, the transaction unconditionally changes the single top-level `Closeout status: open` to `closed` without evaluating other resolution entries or review-log occurrences. An adversarial rerun of the positive correction transaction injected an unrelated accepted/open finding; the transaction and all existing assertions still passed and the global closeout was marked closed.
Required outcome: Automatic correction must close only the bound findings and may set global closeout to `closed` only when the canonical review-resolution predicate proves every finding that contributes to closeout is closed.
Safe resolution path: Update the bound finding entries first, reparse the complete review log and review-resolution document, calculate the repository's canonical closure state, preserve `Closeout status: open` when any unrelated finding remains open, and add older/open, needs-decision, and multi-review regressions to the integrated correction test.
needs-decision rationale: none; the review-resolution contract and BRF-R083 already require truthful global closure.
auto_fix_class: none

## Prior-finding reconciliation

| Prior finding | R2 result | Rationale |
| --- | --- | --- |
| `BRF-M5-CR1` | failed-remediation | The transaction is now executable, but its accepted recipe vocabulary and effective mutation scope compress the preserved reviewer-owned contract; residual defect is `BRF-M5-CR6`. |
| `BRF-M5-CR2` | failed-remediation | Caller booleans were removed, but final-code currentness and the external-action trap remain absent; residual defect is `BRF-M5-CR7`. |
| `BRF-M5-CR3` | resolved | Duplicate required evidence fields and duplicate plan milestone IDs now fail closed, with focused state tests. |
| `BRF-M5-CR4` | failed-remediation | Symlink containment is fixed, but later-review applicability is still presentation-text-sensitive; residual defect is `BRF-M5-CR8`. |
| `BRF-M5-CR5` | failed-remediation | Stage completion now distinguishes `not-required` from material `closed`, but the integrated correction path can manufacture global closure; residual defect is `BRF-M5-CR9`. |

## Requirement-fidelity result

| Contract | Result |
| --- | --- |
| BRF-R033-BRF-R046 and BRF-R079 | block: executable mutation categories are not bounded by the recorded stage-policy category |
| BRF-R063-BRF-R065 plus preserved R1f-R1k | block: accepted recipe vocabulary is compressed to one mechanical kind and one path |
| BRF-R068-BRF-R077 | pass for the tested exact-rename transaction and rollback paths |
| BRF-R081-BRF-R084 / T17 | block: later review selection can miss the same milestone after title drift, and global resolution can be falsely closed |
| BRF-R085-BRF-R090 / T18 | block: final code drift is not observed and prohibited external actions lack fail-on-call proof |
| T24 | pass: focused non-public-entry tests reject public, direct, bugfix, and legacy contexts |

## Checklist coverage

| Check | Result |
| --- | --- |
| Spec alignment | block |
| Test coverage | block |
| Edge cases | block |
| Error handling | concern; rollback and durable pause are present, but global closeout and stale-currentness cases fail |
| Architecture boundaries | block |
| Compatibility | block for the preserved correction vocabulary; pass for non-public activation boundary |
| Security/privacy | block on mutation-authority projection and external-action proof |
| Derived artifact currency | pass for the reviewed commit before this review record |
| Unrelated changes | pass |
| Validation evidence | concern; focused suites pass but encode or omit the reproduced defects |

## Direct-proof gaps and reproductions

- `python scripts/test-workflow-automation.py -k correction`: 13 passed.
- `python scripts/test-workflow-automation.py -k verify`: 4 passed.
- `python scripts/test-workflow-automation.py -k non_public`: 5 passed.
- `python scripts/test-workflow-automation-state.py`: 60 passed.
- `python scripts/test-workflow-automation-policy.py`: 15 passed.
- Python compilation and `git diff --check 34a1360f..1498cefd`: passed.
- Direct probe: source mutation after final review/explanation remained verification-ready.
- Direct probe: later `M2` inconclusive review with a changed title did not stale the earlier approval.
- Direct probe: an unrelated open resolution finding did not prevent automatic global closeout.
- Direct policy probe: the review-resolution stage projects `change-local-evidence`, while its capability admits code, tests, review evidence, and change-local evidence.

## Milestone handoff

- M5 remains `resolution-needed`.
- Required review-resolution: yes.
- M6 remains blocked.
- Final closeout readiness: not ready because implementation findings remain open and an implementation milestone remains unresolved.
- No automatic downstream handoff is authorized by this isolated code-review invocation.
