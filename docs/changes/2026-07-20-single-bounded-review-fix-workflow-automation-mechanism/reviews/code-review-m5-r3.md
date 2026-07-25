# Code Review M5 R3

Review ID: code-review-m5-r3
Stage: code-review
Round: M5 R3
Reviewer: independent same-session context-reset reviewer
Target: M5 correction commit `3e7df2fc`
Reviewed artifact: M5 correction commit `3e7df2fc`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M5-CR10
Immediate next stage: review-resolution M5

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit range `0c89e15e..3e7df2fc`
- Requirement-fidelity gate: applicable
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer participated in the preceding implementation turn, so this review does not claim blind L2 independence; the risk map below was reconstructed from the tracked diff and governing requirements before implementation validation summaries were consulted during this review pass

## Independent risk map

### Affected behavior

- Reviewer-owned implementation-correction recipe parsing, persistence, execution, rollback, and review-resolution closeout.
- Stage-policy mutation-category projection and enforcement during capability derivation and durable-state validation.
- Canonical milestone-review chronology after display-title changes.
- Verification authorization currentness, final-code identity, and the external-action prohibition.
- M5 lifecycle evidence and transition back to milestone rereview.

### Highest-impact failure modes

- An accepted correction recipe is persisted or executed with a compressed, ambiguous, or class-inconsistent shape.
- A correction mutates a category permitted by its capability class but not by its exact stage policy or parent authorization.
- Multi-path correction partially mutates files or evidence and fails to restore every original byte.
- Bounded correction marks global review resolution closed while an unrelated finding remains open.
- A later review of the same `M<n>` occurrence is ignored because its display title changed.
- Final-code currentness covers only an evidence-declared subset of changed code, allowing unlisted source drift after final review or explanation.
- The verify transaction invokes a prohibited subprocess, network, URL, shell, credential, PR, publication, deployment, merge, destructive-Git, or external-mutation surface.
- Review artifacts claim resolution or milestone closeout without proof matching the tracked commit.

### Changed boundaries

- `scripts/workflow_automation.py`: correction recipe compiler, bounded correction transaction, full-ledger closeout decision, final-code identity, and verification readiness.
- `scripts/workflow_automation_policy.py`: immutable stage-local mutation sets.
- `scripts/validate_workflow_automation.py`: persisted recipe and stage-policy-scope validation.
- `scripts/workflow_automation_state.py`: milestone occurrence normalization and bound review-resolution verification.
- Architecture, ADR, plan, and change-local review evidence: clarification and lifecycle synchronization.

### Expected evidence

- Property-by-surface coverage for all preserved mechanical kinds and the declared-safe field set.
- Negative proof for unknown recipe values, path-set mismatches, forbidden paths, stale identities, and stage-policy/parent scope expansion.
- Multi-path transaction proof including rollback after a later operation or evidence update fails.
- Full-ledger proof with older open, `needs-decision`, and multi-review findings.
- Same-milestone renamed-title and malformed-occurrence review chronology proof.
- Final-code proof derived from a canonical complete code-state boundary, including drift in a changed path omitted from caller- or evidence-supplied lists.
- Fail-on-call proof for prohibited external-action surfaces around the composed verify transaction.
- Tracked lifecycle, review-closeout, metadata, and selected repository-boundary evidence.

### Direct-inspection areas

- Recipe normalization parity between compiler and durable validator.
- Capability derivation and stored-state mutation-category checks.
- Mutation ordering, original-byte capture, rollback, and postcondition comparison.
- Complete review-log/review-resolution closure predicate.
- `_review_applicability` and canonical occurrence ordering.
- `_final_code_identity_from_branch_evidence` and every consumer of the resulting identity.
- External-action test doubles and their placement around actual stage invocation.

### Intentionally out-of-scope areas

- M6 public command activation and legacy-writer cutover.
- Final holistic review of the complete multi-milestone branch.
- PR opening, publication, deployment, merge, and release execution.

### Risk classes

- Applicable: authorization, integrity, transaction recovery, path containment, lifecycle-state consistency, review independence, compatibility, verification currentness, and external-action containment.
- Not applicable: end-user UI accessibility, personal-data processing, cryptographic protocol design, and deployed-service availability.

### Falsifiable review questions

1. Can an implementation-correction capability include a category outside its exact stage-local set while remaining within the parent and capability class?
2. Can any preserved mechanical or declared-safe recipe shape be accepted by one surface and rejected or reinterpreted by another?
3. Can a multi-path correction leave a partial mutation after any later operation, review-resolution update, or review-log update fails?
4. Can unrelated open or `needs-decision` findings coexist with `Closeout status: closed` after automatic correction?
5. Can a later review for the same normalized milestone ID fail to invalidate an earlier approval after title drift?
6. Can code outside `Final code paths` change after review while verification readiness still succeeds?
7. Can any prohibited external-action API be called during the composed verify transaction?
8. Do the tracked review and plan surfaces truthfully represent the result of this exact review?

## Phase receipts

### `risk-map-recorded`

- Status: completed
- Recorded before this review pass consulted implementation validation summaries
- Risk map identity: this review record at its initial tracked-worktree state

### `evidence-results-released`

- Status: completed
- Released after the risk map and requirement-property inspection
- Policy suite: 16 passed
- State/recovery suite: 60 passed
- Engine suite: 56 passed
- Durable-state validator suite: 65 passed
- Direct final-code omission probe: failed; verification readiness remained valid after an unlisted repository source file changed
- Evidence challenge result: the passing source-drift tests cover only a path already named by the branch-state artifact and do not prove that the named path set is complete

### `prior-findings-reconciled`

- Status: completed
- Released after the blind-first source inspection, requirement decomposition, full focused suites, and direct adversarial probe
- Prior review: `code-review-m5-r2`

### `verdict-recorded`

- Status: completed
- Verdict: `changes-requested`
- Requirement-fidelity outcome: failed for final-code completeness
- Automatic downstream handoff: stopped because this is a direct isolated review

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M5-CR10`
- Next stage: review-resolution M5
- Review status: changes-requested
- Material findings: `BRF-M5-CR10`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m5-r3.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m5-r3`
- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution and rereview, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M5-CR10`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `0c89e15e..3e7df2fc`
- Tracked governing branch state: branch `proposal/single-bounded-review-fix-automation` at `3e7df2fc`
- Governing artifacts: approved unified automation spec, preserved review-finding-resolution contract, active test spec, approved architecture and ADR, active M5 plan, and the R2 review-resolution dispositions
- Validation evidence: full policy, state/recovery, engine, and durable-state validator suites plus a direct final-code path-omission probe

## Diff summary

The correction commit expands implementation-correction recipes to the preserved mechanical and declared-safe shapes, enforces immutable stage-local mutation sets, normalizes milestone-review applicability to `M<n>`, preserves global closeout when unrelated findings remain open, binds verification evidence to a file-manifest identity, adds external-action traps, and synchronizes M5 review evidence.

## Finding BRF-M5-CR10

Finding ID: BRF-M5-CR10
Severity: major
Location: `scripts/workflow_automation.py:328-374`, `scripts/test-workflow-automation.py:3299-3414`, and `scripts/test-workflow-automation.py:3952-4021`
Evidence: `_final_code_identity_from_branch_evidence` reads `Final code paths` from the same branch-state artifact that asserts `Final code identity`, hashes only those named paths, and never compares that set with a canonical repository diff, tree, tracked change set, or independently owned manifest. Both positive tests construct a one-file identity from the same evidence-supplied list. A direct probe added `scripts/unlisted.py`, established readiness with only `scripts/listed.py` in `Final code paths`, changed the unlisted source, and observed that `resolve_verification_readiness` still succeeded. The final-review `complete_final_diff: reviewed` label therefore remains self-asserted for omitted paths.
Required outcome: Verification authorization and final verification must bind to a canonical complete final-code state so any changed, added, deleted, renamed, dirty, or otherwise in-scope code path omitted from stage evidence invalidates readiness.
Safe resolution path: Derive the final-code identity and complete path set from an independently trusted repository boundary such as the tracked base-to-head diff/tree plus explicitly governed worktree state, or inject a trusted canonical code-state provider for non-Git fixtures. Treat `Final code paths` as a projection that must exactly match that canonical set, bind every final review/explanation/promotion/branch/command artifact to the resulting identity, and add omission, addition, deletion, rename, dirty-file, and untracked-file contrasts.
needs-decision rationale: none for the required behavior; if the repository cannot choose between a Git-derived identity and another independent canonical provider within the approved architecture boundary, record that implementation-level selection in the architecture package before coding.
auto_fix_class: none

## Prior-finding reconciliation

| Prior finding | R3 result | Rationale |
| --- | --- | --- |
| `BRF-M5-CR6` | resolved | Compiler and durable validator project both classes, all seven mechanical kinds, declared-safe fields, multi-path shapes, and exact stage-local mutation-category subset checks. |
| `BRF-M5-CR7` | failed-remediation | Listed-file drift and external-action traps are now covered, but final-code completeness remains evidence-supplied; residual defect is `BRF-M5-CR10`. |
| `BRF-M5-CR8` | resolved | Canonical review applicability normalizes the reviewed milestone to `M<n>` and the renamed-title contrast rejects the stale earlier approval. |
| `BRF-M5-CR9` | resolved | Correction evaluates all other resolution entries and review-log open IDs before changing global closeout; the integration test preserves open state for unrelated work. |

## Requirement-fidelity result

| Contract | Result |
| --- | --- |
| `BRF-R033`-`BRF-R046` and `BRF-R079` | pass for the reviewed correction: stage-local, capability, and parent mutation scopes are enforced in derivation and durable validation |
| `BRF-R063`-`BRF-R065` plus preserved `R1f`-`R1k` | pass for the reviewed correction vocabulary and bounded operation shapes |
| `BRF-R081`-`BRF-R084` / T17 | pass for normalized milestone occurrence chronology and truthful bound/global resolution distinction |
| `BRF-R043c`, `BRF-R085`, and complete-final-diff obligations | block: a self-declared partial path list can satisfy final-code currentness |
| `BRF-R086`, `BRF-R090`, and T18 external-action boundary | pass for the inspected composed transaction traps, but does not cure the final-code completeness block |
| T24 | pass: no public command or skill surface changed in the reviewed commit |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M5-CR10` violates complete final-code and fresh verification obligations. |
| Test coverage | block | Listed-path drift is covered; omitted changed-path drift is not and the direct probe reproduces it. |
| Edge cases | block | Added/deleted/renamed/dirty/untracked path completeness is not proved. |
| Error handling | concern | Stale listed identities fail closed and correction rollback is bounded, but omitted paths never enter the stale check. |
| Architecture boundaries | block | Stage evidence currently selects its own supposedly complete identity domain instead of projecting an independently canonical code state. |
| Compatibility | pass | Public command routing, legacy adapters, and M6 cutover surfaces are unchanged. |
| Security/privacy | concern | External-action traps are present, but incomplete code identity can authorize verification of an unreviewed code state. |
| Derived artifact currency | block | Final-review, explanation, promotion, branch, and command evidence agree with each other while all omit the same changed source. |
| Unrelated changes | pass | The commit is limited to the four R2 corrections, aligned architecture clarification, tests, and lifecycle evidence. |
| Validation evidence | concern | All 197 focused tests pass, but the direct omission probe demonstrates that their final-code fixture is insufficient. |

## Direct-proof gaps

- No automated test proves exact equality between `Final code paths` and an independently derived complete repository code-state set.
- No test covers omitted added, deleted, renamed, dirty, or untracked code paths.

## Milestone handoff

- Reviewed milestone: M5
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M5-CR10`
- Remaining in-scope implementation milestones: M5 resolution and rereview, M6
- Next stage: review-resolution M5
- Final closeout readiness: not ready because M5 has one open material finding and M6 remains unimplemented
- Automatic downstream handoff: none; this direct review remains isolated
