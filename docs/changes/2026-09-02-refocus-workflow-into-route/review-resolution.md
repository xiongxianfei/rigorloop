# Review Resolution: Refocus Workflow into the Route Skill

## Summary

Closeout status: open

Review closeout: code-review-m2-r2
Review closeout: code-review-m3-r2
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m1-r3`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m3-r1`, `code-review-m3-r2`, `code-review-final-r1`
- Findings resolved: 9
- Unresolved findings: 1
- Current result: Final holistic Code Review R1 found that the active v3 CLI cannot record final-review completion or advance the first v3 example from Code Review to Verify.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RFR-M1-CR1 | accepted | resolved | Formal review locations now preserve their four distinct stage owners. |
| RFR-M1-CR2 | accepted | resolved | Variable projections are capped and unsafe lifecycle values are not disclosed. |
| RFR-M1-CR3 | accepted | resolved | Exact reads are isolated and TG-05 failure, retry, interruption, and freshness proof is complete. |
| RFR-M1-CR4 | accepted | resolved | Human output exposes candidate count, truncation, and exact-selection guidance. |
| RFR-M1-CR5 | accepted | resolved | Unexpected read and interrupted public invocation tests prove non-mutation directly. |
| RFR-M2-CR1 | accepted | resolved | Removed current stage-skill guide fallbacks and retired remaining callable guide/map validators. |
| RFR-M2-CR2 | accepted | resolved | Current skill prose names route wherever it identifies the semantic routing actor. |
| RFR-M3-CR1 | accepted | resolved | The unpublished v0.5.1 package metadata is bound to generated route-only archives while immutable v0.5.0 remains unchanged. |
| RFR-M3-CR2 | accepted | resolved | Normal `init --write-state` safely replaces only an exact lockfile-managed workflow target and rolls back failed replacement. |
| RFR-FINAL-CR1 | accepted | open | Implement the minimal identity-bound final holistic review completion and correction route after all implementation milestones close. |

## Finding Details

### proposal-review-r1

No material findings.

### code-review-m1-r1

#### RFR-M1-CR1

Finding ID: RFR-M1-CR1
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Replace the generic code-review-owned review location with a closed representation that preserves each formal review owner's authority and exposes deterministic review outputs.
Rationale: Location resolution is structural and cannot transfer proposal-review, design-review, or delivery-review evidence ownership to code-review.
Required outcome: Every formal-review location is represented without ownership collapse and has direct correct-owner and wrong-owner proof.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R4, RT-R8, BND-AUTH-001, TG-02, TG-03.
Validation evidence: Code Review M1 R2 inspected `47a87bb8..a8ec338c`; all four configured review-record kinds have their exact review-stage owner and wrong-owner overrides fail directly in the 174-test plan-selected suite.

#### RFR-M1-CR2

Finding ID: RFR-M1-CR2
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add deterministic collection, identifier, and encoded-output bounds and fail-safe redaction or rejection for invalid lifecycle values.
Rationale: Allowlisting some automation scalars does not bound candidate, milestone, package, receipt, or human output and does not protect raw lifecycle fields.
Required outcome: Large or malformed projections remain bounded, actionable, structural-only, and free of private absolute values.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R7, RT-R8, RT-R35, RT-R36, BND-INPUT-001, BND-ENV-001, TG-01, TG-02, TG-04.
Validation evidence: Code Review M1 R3 inspected the complete correction through `063bd6e5`; capped project/change projections, invalid-stage redaction, human truncation disclosure, and the complete planned test set passed.

#### RFR-M1-CR3

Finding ID: RFR-M1-CR3
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add a normalized filesystem-failure boundary, restore requested-change read isolation, and directly prove all TG-05 outcomes over the complete relevant tree.
Rationale: A generic process error and a one-file byte snapshot do not satisfy the approved recovery, retry, non-mutation, or freshness contract.
Required outcome: Success, failure, ambiguity, retry, interruption, and post-mutation stale identity produce bounded deterministic results without changing governed or configuration files.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: RT-R12, RT-R34, RT-R38, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, INT-005, TG-05.
Validation evidence: Code Review M1 R3 confirmed exact-read isolation, full governed/config snapshots, identical retry, stale-after-mutation identity, deterministic `RL_CONTEXT_READ_FAILED`, and interrupted public-process non-mutation proof.

### code-review-m1-r2

#### RFR-M1-CR4

Finding ID: RFR-M1-CR4
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Render existing candidate count and truncation facts in human output with an exact-selection instruction.
Rationale: Bounded output is actionable only when a human can see that entries were omitted and how to proceed.
Required outcome: Public human output reports total candidates, truncation, and exact `--change` selection when the project list is capped.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R3.
Validation target: RT-R35, RT-R36, TG-04.
Validation evidence: Code Review M1 R3 confirmed public human output reports `Candidate count: 41` and `showing 32; use --change <id>` for a capped project result.

#### RFR-M1-CR5

Finding ID: RFR-M1-CR5
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add a narrow deterministic read-fault seam and public interruption proof using the existing complete-tree snapshot.
Rationale: Ordinary configuration rejection does not execute the unexpected-read boundary or prove interruption behavior.
Required outcome: Direct unexpected-read and interrupted-invocation tests return or terminate safely and leave all governed/config bytes unchanged.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R3.
Validation target: RT-R38, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, TG-05.
Validation evidence: Code Review M1 R3 confirmed the direct read-fault result contains `RL_CONTEXT_READ_FAILED` without private details and the FIFO-blocked public process terminates without changing governed state or its input.

### code-review-m1-r3

No material findings.

### code-review-m2-r1

#### RFR-M2-CR1

Finding ID: RFR-M2-CR1
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Remove current workflow-guide fallbacks and retire current guide/map validation behavior while preserving portable placement and historical evidence.
Rationale: Passing a narrow exact-path scan does not satisfy the approved prohibition on current guide consultation or parsing.
Required outcome: Current skills and validators have no guide authority, lookup, parsing, or fallback behavior, and a semantic reintroduction fixture fails.
Follow-up: Apply the bounded M2 correction and run Code Review M2 R2.
Validation target: RT-R19, RT-R21, RT-R25, RT-R33, TG-09, TG-10.
Validation evidence: The M2 R1 correction removes the guide/map parser constants and callable functions from `scripts/skill_validation.py`; replaces stage fallback text with authoritative CLI context; adds `ROUTE-GUIDE-009`; and passes `python scripts/test-guide-system-validator.py`, `python scripts/test-skill-validator.py`, and all M2 plan validation commands. Code Review M2 R2 remains required for closeout.

#### RFR-M2-CR2

Finding ID: RFR-M2-CR2
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Replace semantic public-actor uses of workflow with route and add bounded negative coverage without renaming stable protocol vocabulary.
Rationale: The current package cannot expose two names for the same semantic routing actor after the clean rename.
Required outcome: Current public skill prose consistently identifies route as the semantic actor and explicitly allowed workflow protocol/history contexts remain unchanged.
Follow-up: Apply the bounded M2 correction and run Code Review M2 R2.
Validation target: RT-R1, RT-R26-RT-R29, RT-R33, BND-AUTH-001, TG-08, TG-09.
Validation evidence: The M2 R1 correction replaces semantic old-public-actor wording across current skill packages while preserving `stage_authority: workflow`, `workflow.automation`, workflow-managed operation labels, and generic CI workflow vocabulary; adds `ROUTE-GUIDE-010`; and passes the complete M2 validation set. Code Review M2 R2 remains required for closeout.

### code-review-m2-r2

No material findings. R2 independently confirmed both M2 R1 findings are resolved and the complete M2 validation allocation passes.

### code-review-m3-r1

#### RFR-M3-CR1

Finding ID: RFR-M3-CR1
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Create one coherent unpublished post-v0.5.0 package and adapter candidate whose bundled metadata, generated route archives, docs, and installer preflight agree.
Rationale: Published v0.5.0 is immutable and explicitly excluded the workflow-to-route implementation; reusing its identity makes the changed CLI reject its own selected archives.
Required outcome: Real bundled candidate metadata selects a route-only archive, published v0.5.0 remains unchanged, documentation makes candidate status accurate, and no publication occurs.
Follow-up: Apply the bounded M3 correction and run Code Review M3 R2.
Validation target: RT-R29-RT-R32, TG-13-TG-15, BND-COMPAT-001.
Validation evidence: Complete bundled v0.5.1 metadata equals metadata recomputed from freshly generated route-only archives; the historical v0.5.0 metadata hash remains `74f2d940ce8ef358092609884e9377d0a3955c731e7f437ca63d995862227885`; all seven M3 commands pass without publication.

#### RFR-M3-CR2

Finding ID: RFR-M3-CR2
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Make obsolete-package recovery state-aware and prove the complete migration for both unmanaged and lockfile-managed installs.
Rationale: Removing only the obsolete skill invalidates a managed root hash, so the documented rerun cannot complete under current safety checks.
Required outcome: The supported remediation preserves unrelated targets, reaches one coherent route package, remains retry-safe after interruption, and does not rewrite lifecycle automation state.
Follow-up: Apply the bounded M3 correction and run Code Review M3 R2.
Validation target: RT-R27, RT-R28, RT-R30, TG-13, TG-16, BND-RECOVERY-001.
Validation evidence: CLI tests prove the `--write-state` instruction, exact managed replacement, unrelated-target preservation, coherent route-only result, and rollback restoring the prior target, manifest, and lockfile; the full 367-test package suite and broad smoke pass.

### code-review-m3-r2

No material findings. R2 independently confirmed both M3 R1 findings are resolved and the complete M3 validation allocation passes.

### code-review-final-r1

#### RFR-FINAL-CR1

Finding ID: RFR-FINAL-CR1
Disposition: accepted
Status: open
Owner: implement
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Chosen action: Add one route-recorded final-review receipt, consume it for `code-review -> verify`, and allow final-occurrence implementation correction without a fabricated milestone.
Rationale: The route implementation correctly consumes authoritative CLI context, but the current v3 coordination model cannot represent the final holistic review authority that its own stage graph requires. Silently editing workflow state or treating the plan's Delivery Review as final Code Review would violate stage ownership.
Required outcome: Record exact final-review identity and outcome, reject stale or non-clean evidence, support an implementation correction route with no active milestone, and permit the clean `code-review -> verify` transition through the CLI.
Follow-up: After disposition, implement the bounded lifecycle correction under the owning stage and rerun final holistic Code Review.
Validation target: FV-R1, FV-R8, TG-FINAL-01, TG-FINAL-03, final-review identity and correction-route tests.
Validation evidence: Current exact-change `workflow-context` reports all milestones closed and no blockers but withholds `advance-stage`; source inspection shows `stageIsComplete` has no code-review completion representation.
