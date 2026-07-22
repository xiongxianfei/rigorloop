# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: M2 R1
Reviewer: Codex code-review skill
Target: M2 commit `56a3f62a`
Reviewed artifact: M2 commit `56a3f62a`
Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M2-CR1, BRF-M2-CR2, BRF-M2-CR3, BRF-M2-CR4
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m2-r1.md`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md`, `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`, `docs/plan.md`, `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml`
- Open blockers: none
- Next stage: review-resolution M2
- Review status: changes-requested
- Material findings: BRF-M2-CR1, BRF-M2-CR2, BRF-M2-CR3, BRF-M2-CR4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution needed, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M2-CR1, BRF-M2-CR2, BRF-M2-CR3, BRF-M2-CR4
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `54b8569a..56a3f62a`.
- Review surface: the M2 state adapter, automation and metadata validators, change-record query projection, schema changes, focused tests, and lifecycle handoff evidence.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R006`-`BRF-R008f`, `BRF-R068`-`BRF-R077`, and `BRF-R091`-`BRF-R098`.
- Test spec: `specs/single-bounded-review-fix-workflow-automation.test.md`, especially T14-T16, T19, T22, T23, and T29.
- Architecture and ADR: the approved sole-writer, capability-bound receipt, evidence-first recovery, and dual-read/single-write migration boundaries.
- Plan milestone: `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` M2 and its tracked `review-requested` handoff.
- Validation evidence inspected after blind-first review: CMD4-CMD9 and compilation/diff evidence recorded by implementation, then rerun by this review.

## Risk Map

Before consulting the recorded validation summaries, the review prioritized four falsifiable risks: recovery could act on evidence that was never durably prepared; a receipt could widen retry authority beyond the immutable stage policy; complete-file replacement or migration could corrupt or ambiguously bind state; and status could turn malformed durable state into apparently valid operator output. Direct inspection focused on receipt lookup, policy provenance, transition-key inputs, cancellation and migration settlement, atomic replacement, query validation, and the exact M2 determinism proof. Public command routing and stage orchestration remain intentionally out of scope until M3-M6.

## Diff Summary

M2 adds a complete-file atomic state adapter, deterministic transition-key generation, prepared and finalized receipt operations, evidence-first recovery decisions, cancellation settlement, legacy status and migration handling, unified status projection, migration schema/validation, and focused tests. Public workflow routing remains unchanged. Atomic replacement and legacy-source identity binding are directionally sound, but the recovery API can currently authorize retry from caller-supplied data that is neither the persisted receipt nor the immutable stage policy, the status query bypasses unified-state validation, and the milestone-required determinism proof is incomplete.

## Findings

### BRF-M2-CR1: Recovery can retry a receipt that was never persisted

Finding ID: BRF-M2-CR1
- Severity: major
- Status: open
- Location: `scripts/workflow_automation_state.py:201-235`, `scripts/test-workflow-automation-state.py:138-170`
- Evidence: `evaluate_receipt_recovery` accepts a caller-supplied receipt object, counts prepared receipts in automation state, but never proves that the supplied receipt is the unique persisted prepared receipt. The positive recovery tests construct `state = valid_automation()` with an empty `transition_receipts` mapping and pass a separate receipt object. A direct review reproduction changed that unpersisted receipt to `idempotent-retry`; the evaluator returned `RecoveryDecision(action='retry', invoke_stage=True, reason='no-completion-evidence')`. This permits stage reinvocation without the write-ahead evidence required by `BRF-R068`, `BRF-R072`, and `BRF-R073`.
- Required outcome: Recovery must evaluate exactly the unique prepared receipt durably stored under the requested transition ID and reject an absent, mismatched, duplicated, or caller-substituted receipt before returning any retry or reconciliation action.
- Safe resolution path: Change the recovery API to accept a transition ID or retrieve the receipt internally, compare the persisted mapping key and full immutable receipt identity, and add absent-receipt, different-receipt, wrong-ID, and unique-persisted-receipt regressions. Keep retry disabled unless that lookup succeeds.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M2-CR2: Receipt-controlled retry policy overrides the immutable stage policy

Finding ID: BRF-M2-CR2
- Severity: major
- Status: open
- Location: `scripts/workflow_automation_state.py:100-114`, `scripts/workflow_automation_state.py:224-238`, `scripts/validate_workflow_automation.py:1064-1078`
- Evidence: Recovery reads `receipt.retry_policy` directly. The receipt validator checks the value only when present, does not require it, and does not compare it with the effective capability stage's immutable `StagePolicy.retry_policy`. `compute_transition_key` also omits the receipt retry policy. In a direct reproduction, proposal-review's registry policy was `reconcile-only`, the receipt was changed to `idempotent-retry`, validation/recovery accepted that closed value, the transition key remained unchanged, and recovery returned `retry`. This violates `BRF-R071` and `BRF-R075` by letting durable/caller input manufacture idempotent authority.
- Required outcome: Recovery authority must derive from the immutable policy for the effective capability's bound stage. Any persisted retry-policy projection must be required, must equal that policy, and must be bound by the transition key; otherwise it must be omitted as non-authoritative.
- Safe resolution path: Resolve the persisted capability stage through `STAGE_POLICY_BY_STAGE`, use that policy as the only retry decision, reject receipt/policy mismatch, and bind any retained projection into the deterministic transition key. Add one mismatch test per retry-policy family plus a missing-policy contrast.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M2-CR3: T29 does not execute its required repeat and reverse-order proof

Finding ID: BRF-M2-CR3
- Severity: major
- Status: open
- Location: `scripts/test-workflow-automation-state.py:116-126`, `scripts/test-workflow-automation-state.py:525-543`; `specs/single-bounded-review-fix-workflow-automation.test.md` T29
- Evidence: T29 requires the M2 transactional and migration subset to run twice with identical inputs and again in reverse declared order, comparing normalized receipts, transition keys, migration records, canonical files, and teardown. The implementation only reverses dictionary insertion order for one transition-key calculation and runs two identical migration calls that compare migration receipt dictionaries. It does not execute the receipt/cancellation/migration subset in two declared orders, compare canonical files, or prove teardown/no shared state. CMD6 passes because no test encodes those required properties.
- Required outcome: The M2 suite must directly implement T29's fixed-clock, fresh-root, identical-run, reverse-order, normalized-state, canonical-file, and teardown assertions.
- Safe resolution path: Add a deterministic scenario runner that creates a fresh temporary root per case, accepts an explicit operation order, captures normalized receipts/keys/migrations and canonical bytes, verifies cleanup, and compares two identical runs plus the approved reverse order. Keep M6 composed-engine determinism deferred to T30.
- auto_fix_class: none
- needs-decision rationale: none

### BRF-M2-CR4: Unified status projection reports malformed automation state as successful

Finding ID: BRF-M2-CR4
- Severity: major
- Status: open
- Location: `scripts/query-change-record.py:382-410`, `scripts/test-query-change-record.py:211-228`
- Evidence: The query helper calls `project_automation_status` directly after only its general safe-path shape checks; it does not use the state adapter's validated read or call `validate_workflow_automation`. A direct temporary-repository reproduction changed `run.status` to `impossible`; `query-change-record.py ... summary` returned exit code 0, top-level `status: ok`, and `automation_policy.run_status: impossible`. The positive query test covers only valid paused state. This contradicts T22's exact unknown/ambiguous diagnostic requirement and makes operator status less fail-closed than the canonical state reader.
- Required outcome: Unified status must validate the automation subsection before projecting it and return a stable error diagnostic for malformed or unknown durable state without mutating the file.
- Safe resolution path: Route unified status through the validated state-reader boundary or call the canonical automation validator before projection, convert validation errors to the query helper's stable error envelope, and add unknown run status, receipt status, policy version, and malformed migration regressions with byte-stability assertions.
- auto_fix_class: none
- needs-decision rationale: none

## Requirement Fidelity

| Requirement properties | Result | Evidence |
| --- | --- | --- |
| `BRF-R006` read-only, complete status from tracked state | block | Projection is byte-stable for valid input, but `BRF-M2-CR4` shows malformed state is reported as valid. |
| `BRF-R007`-`BRF-R007c` terminal cancellation and idempotent outcomes | pass | Focused cancellation tests cover active, prepared, cancelled, completed, and absent unified runs; settlement preserves receipts and revokes/invalidates active authority. |
| `BRF-R068`-`BRF-R070` durable capability-bound receipt | block | Preparation persists and validates receipts, but `BRF-M2-CR1` shows recovery is not bound to that persisted record. |
| `BRF-R071`-`BRF-R075` immutable retry authority and evidence-first resume | block | `BRF-M2-CR2` shows receipt data can widen retry authority. |
| `BRF-R076`-`BRF-R077` drift, partial output, unknown and multiple state | concern | Focused tests cover several contrasts, but safe recovery still depends on the two unbound inputs above. |
| `BRF-R091`-`BRF-R097` dual-read/single-write migration | pass | Exact source-record hashing, one-way receipts, terminal reads, repeat no-op, and mixed-writer rejection have direct proof. Rollback and public adapters remain assigned to M6. |
| T29 deterministic M2 proof | block | `BRF-M2-CR3` identifies the missing scenario/order/file/teardown assertions. |

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | BRF-M2-CR1 and BRF-M2-CR2 violate the prepared-receipt and immutable retry-policy contracts. |
| Test coverage | block | BRF-M2-CR3 leaves the approved M2 determinism proof materially compressed. |
| Edge cases | block | Unpersisted receipts, retry-policy mismatch, and unknown status all reproduce unsafe outcomes. |
| Error handling | block | BRF-M2-CR4 returns successful operator output for malformed durable state. |
| Architecture boundaries | concern | The sole writer and atomic replacement boundary are present, but recovery and query callers bypass the authoritative persisted-record/validated-read boundaries. |
| Compatibility | pass | Legacy records remain read-only, exact migration binding is checked, and no public or retired writer changed. |
| Security/privacy | pass | No credentials, external-system calls, secret output, or widened external authority were introduced. |
| Derived artifact currency | pass | No generated adapter or derived public skill output changed in M2. |
| Unrelated changes | pass | The diff is scoped to the M2 writer, validation, query, proof, and lifecycle handoff surfaces. |
| Validation evidence | concern | CMD4-CMD9 all pass when rerun, but the direct reproductions and T29 audit show the selected tests are insufficient. |

## No-Finding Rationale

Not applicable. This review has four material findings.

## Residual Risks

Cancellation actor/timestamp fields are not yet schema-validated, but the approved spec defines revocation state rather than a closed cancellation-evidence schema, so this review does not elevate that observation to a material finding. M3-M6 orchestration, public commands, adapters, rollback, cross-spec checks, and full-engine determinism remain intentionally deferred and were not reviewed as implemented behavior.

## Validation

- `python scripts/test-change-metadata-validator.py` passed: 53 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` passed before review recording.
- `python scripts/test-workflow-automation-state.py` passed: 24 tests.
- `python scripts/test-validate-workflow-automation.py -k receipt` passed: 15 selected tests.
- `python scripts/test-validate-workflow-automation.py -k migration` passed: 3 selected tests.
- `python scripts/test-query-change-record.py` passed: 17 tests.
- Python compilation and commit-range diff checks passed.
- Direct recovery reproduction: an unpersisted idempotent receipt returned `retry` with `invoke_stage=True`.
- Direct policy reproduction: proposal-review's immutable `reconcile-only` policy was overridden by receipt value `idempotent-retry`; recovery returned `retry` and the transition key did not change.
- Direct status reproduction: unknown `run.status: impossible` returned exit code 0 and top-level `status: ok`.
- Static T29 audit found no reverse declared scenario execution or canonical-file comparison beyond dictionary-order and duplicate-migration checks.

## Milestone Handoff

- Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M2-CR1` through `BRF-M2-CR4`
- Remaining in-scope implementation milestones: M2 resolution needed, M3, M4, M5, M6
- Next stage: review-resolution M2
- Final closeout readiness: not ready because M2 has four open findings and M3-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed. Enter `review-resolution` for `BRF-M2-CR1` through `BRF-M2-CR4`, apply targeted M2 fixes, rerun CMD4-CMD9 and the direct contrasts, return M2 to `review-requested`, and rerun `code-review M2`. Do not start M3 while these findings remain open.
