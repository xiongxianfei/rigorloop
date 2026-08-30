# Review Resolution: Consolidate RigorLoop Review Gates

## Summary

Closeout status: open

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-cli-fix-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m3-r1

- Reviews covered: `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `plan-review-r2`, `test-spec-review-r1`, `code-review-m1-r1`, `code-review-cli-fix-r1`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m3-r1`
- Findings resolved: 20
- Unresolved findings: 1
- Current result: M3 R2 found that combined reviews cannot complete through the Python stage-native verifier; CRG-M3-CR3 requires resolution and rereview.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CRG-SR1 | accepted | resolved | The later owner-approved cutover decision supersedes the earlier baseline choice: old progression remains authoritative until one complete release cutover, with no runtime topology machinery. |
| CRG-SR2 | accepted | resolved | Added deterministic authority and next-action semantics for every package-review outcome. |
| CRG-SR3 | accepted | resolved | Kept accepted proposal evidence outside multi-artifact package settlement and removed per-document hash recording. |
| CRG-SR4 | accepted | resolved | Bound design to the accepted Proposal Review ID and delivery to the approved aggregate design-package revision. |
| CRG-PLR2-1 | accepted | resolved | The revised plan requires current test-spec-review approval before M1 and before relying on a substantively changed proof map. |
| CRG-TSR1-1 | accepted | resolved | The registered revision maps every approved-plan validation command through exact command IDs, proof obligations, test cases, and M1-M7 milestone proof. |
| CRG-M1-CR1 | accepted | resolved | Removed the activation manifest, baseline, topology marker, interpreter, and inferred authority entirely. |
| CRG-M1-CR2 | accepted | resolved | Explicitly allowed later approved lifecycle features to supersede obsolete frozen fields; no legacy renderer or output-version mechanism was added. |
| CRG-CLI-CR1 | rejected | resolved | The owner rejected a mandatory commit or packet identity for direct clean-review settlement; the existing exact milestone evidence, review evidence, and review-log binding are sufficient for this workflow. |
| CRG-CLI-CR2 | rejected | resolved | The owner accepted the concise two-phase `complete-milestone` behavior and rejected adding another operation or documentation gate before M2. |
| CRG-M2-CR1 | accepted | resolved | Aggregate and hash-based replay were removed; the narrower remaining evidence-replay defect is CRG-M2-CR6. |
| CRG-M2-CR2 | accepted | resolved | Non-approved outcomes now block; the narrower incorrect-next-action defect is CRG-M2-CR7. |
| CRG-M2-CR3 | rejected | resolved | The owner explicitly rejected per-document content-hash registration; rereview confirms package authority no longer uses those hashes. |
| CRG-M2-CR4 | accepted | resolved | Finding ownership and correction targets now fail closed against the explicit member map. |
| CRG-M2-CR5 | accepted | resolved | Proposal Review replacement now invalidates dependent design authority while retaining the prior Design Review ID. |
| CRG-M2-CR6 | accepted | resolved | Exact settlement replay now rereads current package and review evidence before recognizing replay. |
| CRG-M2-CR7 | accepted | resolved | Settled non-approved package states now expose outcome-specific safe continuations. |
| CRG-M3-CR1 | accepted | resolved | Python automation now uses and proves the consolidated stage vocabulary and route. |
| CRG-M3-CR2 | partially-accepted | resolved | M3 detects and proves every invalid package state; M6 retains atomic activation ownership under CRG-R35 through CRG-R40. |
| CRG-M3-CR3 | needs-decision | open | Replace the scalar reviewed-artifact check with explicit package-aware completion verification. |

## Finding Details

### code-review-m3-r2

#### CRG-M3-CR3

Finding ID: CRG-M3-CR3
Disposition: needs-decision
Status: open
Owner: M3 implementation owner
Owning stage: implement M3
Decision owner: M3 implementation owner
Decision needed: accept the package-aware verifier correction or stop M3.
Chosen action: pending owner disposition.
Rationale: the consolidated stages are routable, but their completion verifier requests scalar package identities that the approved explicit member-map model does not define.
Required outcome: Design Review and Delivery Review completion verify the exact explicit package facts and canonical review occurrence without aggregate or per-document package hashes.
Safe resolution path: add a package-specific native verifier and direct valid/mismatch tests for both consolidated review stages.
Follow-up: resolve, implement, and rerun M3 Code Review.
Validation target: CRG-R22 through CRG-R24; CRG-T11; BND-STATE-001; BND-COMPOSE-001.
Validation evidence: pending.

### code-review-m3-r1

#### CRG-M3-CR1

Finding ID: CRG-M3-CR1
Disposition: accepted
Status: resolved
Owner: M3 implementation owner
Owning stage: implement M3
Decision owner: M3 implementation owner
Decision needed: none; the owner accepted the correction.
Chosen action: replace the affected Python automation vocabulary, policy, and transition route with the consolidated sequence and add direct proof for both consolidated review stages.
Rationale: The JavaScript lifecycle can write `design-review` and `delivery-review`, but the Python automation engine rejects both values and retains the retired review sequence.
Required outcome: automation policy, state, validation, and tests represent the consolidated graph and can resume synchronized active automation projections.
Safe resolution path: replace the affected Python stage vocabulary and policies, update fixtures, and add end-to-end automation proof across both consolidated reviews.
Follow-up: implement the correction and rerun M3 Code Review.
Validation target: CRG-T11; M3 automation commands; BND-STATE-001; INT-005.
Validation evidence: Python automation policy, state, engine, and code-state suites passed 17, 65, 76, and 18 tests; the Node lifecycle routing packet passed 43 tests; details are recorded in `evidence/m3-consolidated-routing-implementation.md`.

#### CRG-M3-CR2

Finding ID: CRG-M3-CR2
Disposition: partially-accepted
Status: resolved
Accepted portion: M3 adds one compact shared assessment and direct proof for every invalid package-authority state.
Deferred portion: M6 activates that assessment as a downstream blocker in the single reviewed cutover revision.
Owner: M3 implementation owner
Owning stage: implement M3
Decision owner: M3 implementation owner
Decision needed: none; the owner accepted detection and proof in M3 and cutover-owned enforcement in M6.
Chosen action: add one shared downstream authority assessment that identifies missing, partial, stale, mixed, and historical-only package authority; expose it in status/context and prove every partition. Keep it advisory for the implementing change, then make the same assessment blocking atomically in M6.
Rationale: The missing detection is valid, but activating the blocker during M3 would violate CRG-R35 through CRG-R40 by retroactively forcing this implementing change onto the consolidated workflow. A special exception, migration, activation manifest, topology field, or runtime selector is explicitly rejected.
Required outcome: M3 exposes and directly proves all invalid downstream authority states; M6 activates the already-proved gate for Code Review, explanation, Verify, and PR in the single reviewed cutover revision.
Safe resolution path: centralize the assessment without hashes or topology metadata, add missing and historical-only regressions alongside stale/mixed proof, and retain the M6 activation dependency.
Follow-up: implement the correction and rerun M3 Code Review.
Validation target: CRG-T12; CRG-R41; CRG-R42; BND-COMPOSE-001; BND-COMPAT-001.
Validation evidence: lifecycle read and stage-advance tests directly prove missing, historical-only, partial, stale, mixed, and current authority partitions; the full package suite passed 296 tests; `enforcement: cutover-pending` and the M6 activation dependency are recorded in `evidence/m3-consolidated-routing-implementation.md`.

### spec-review-r1

#### CRG-SR1

Finding ID: CRG-SR1
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: specification author
Decision needed: resolved by the owner-approved single-cutover direction; no runtime pre/post classification remains.
Chosen action: superseded by the later owner-approved single-cutover decision: keep old progression authoritative during implementation, block cutover on legacy-dependent work, and introduce no activation manifest, baseline, topology marker, or runtime interpreter.
Rationale: runtime coexistence created the ambiguity identified by the finding; one complete cutover removes the need to classify changes by inferred epoch.
Required outcome: cutover is deterministic, release-bound, observable, and blocked while any nonterminal change depends on legacy progression.
Safe resolution path: keep old progression authoritative during implementation, validate the complete consolidated surface and legacy-work inventory, and retire old progression in one reviewed release revision.
Follow-up: prove the cutover boundary in M6; no additional activation artifact or review is required.
Validation target: CRG-R35, CRG-R38, EC9, EC10, BND-COMPAT-001, observability, compatibility acceptance criteria, and direct boundary proof ownership.
Validation evidence: current `specs/consolidated-review-gates.md`, ADR, plan, and test specification define the single-cutover contract; lifecycle and documentation validation passed after owner-authorized identity synchronization.

#### CRG-SR2

Finding ID: CRG-SR2
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: specification author
Decision needed: define one deterministic outcome-to-authority and handoff matrix for Design Review and Delivery Review.
Chosen action: add one deterministic four-outcome progression and next-action matrix, record correction targets separately, and withhold package authority for every non-approved outcome.
Rationale: a closed outcome vocabulary without state and handoff semantics permits incompatible routing and settlement implementations.
Required outcome: all four outcomes have unique progression, settlement, correction, stop, and rereview behavior.
Safe resolution path: add the normative matrix described in `spec-review-r1`, preserving workflow routing ownership and exact package rereview.
Follow-up: revise the specification and run `spec-review-r2`.
Validation target: CRG-R15, CRG-R21, CRG-R29 through CRG-R34, error behavior, acceptance criteria, and direct state/authority/recovery proof ownership.
Validation evidence: `specs/consolidated-review-gates.md` CRG-R29 through CRG-R34, BND-STATE-001, INT-007, and CRG-AC6 at `sha256:64fbc97dc179d86b24c9aa04434521f3fe73349b643e9bf7845ed227ebee2a62`; independently confirmed by `spec-review-r2`.

#### CRG-SR3

Finding ID: CRG-SR3
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: specification author
Decision needed: choose whether Proposal Review uses the universal deterministic package-manifest regime or an explicitly separate exact evidence contract.
Chosen action: define accepted proposal evidence as the proposal artifact and Proposal Review evidence, keep it outside package settlement, and use one aggregate revision only for Design Review and Delivery Review packages.
Rationale: optional cited research and semantic reliance currently conflict with universal exact package identity and byte-staleness rules.
Required outcome: Proposal Review and Verify consume one deterministic, testable, current proposal evidence identity with closed field applicability and staleness behavior.
Safe resolution path: include the proposal and every explicitly relied-on repository research artifact in a proposal-package manifest, or scope CRG-R22 through CRG-R24 to design and delivery and define an equally exact proposal evidence rule.
Follow-up: revise the specification and run `spec-review-r2`.
Validation target: glossary package terms, CRG-R10, CRG-R22 through CRG-R24, CRG-R42, EC2, input/temporal boundaries, and package acceptance criteria.
Validation evidence: `specs/consolidated-review-gates.md` glossary, CRG-R22 through CRG-R24, CRG-R42, EC2, observability, and CRG-AC4 at `sha256:64fbc97dc179d86b24c9aa04434521f3fe73349b643e9bf7845ed227ebee2a62`; independently confirmed by `spec-review-r2`.

### spec-review-r2

#### CRG-SR4

Finding ID: CRG-SR4
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: specification author
Decision needed: choose one aggregate upstream-binding rule that represents accepted proposal authority for design packages and approved design authority for delivery packages.
Chosen action: define one upstream binding whose design value is the accepted Proposal Review ID and whose delivery value is the approved aggregate design-package revision; include it in aggregate calculation, staleness, status, recording, and settlement checks.
Rationale: Design Review currently has no upstream package revision even though the aggregate formula names only that input.
Required outcome: a changed accepted Proposal Review ID changes the design-package aggregate revision, and a changed design-package revision changes the delivery-package aggregate revision.
Safe resolution path: introduce `applicable upstream binding`, define its two values, and include it in aggregate calculation and stale checks without adding per-document hashes.
Follow-up: completed by the specification revision and `spec-review-r3`.
Validation target: glossary package revision, CRG-R22 through CRG-R26, CRG-R42, BND-AUTH-001, BND-TEMPORAL-001, CRG-AC4, and CRG-AC5.
Validation evidence: `specs/consolidated-review-gates.md` glossary, CRG-R22 through CRG-R26, state invariants, boundary definitions, INT-003, observability, CRG-AC4, and CRG-AC5 at `sha256:ae8b9452fc028fadb9cdd616f3d6d07ce312847951ee178e874aab753a1c357c`; independently confirmed by `spec-review-r3`.

### plan-review-r1

No material finding was evaluated or created. The formal invocation stopped before semantic review because lifecycle routing remained at `plan` and exposed only the workflow-owned `advance-stage` operation. The blocker is recorded in `reviews/plan-review-r1.md`; workflow advancement followed by a fresh review is required, and this entry provides no plan approval or settlement.

### plan-review-r2

#### CRG-PLR2-1

Finding ID: CRG-PLR2-1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Decision owner: plan author
Decision needed: make current test-spec-review approval an explicit pre-implementation dependency and require rereview after substantive proof-map changes.
Chosen action: add clean current test-spec-review settlement to M1 and repository-wide implementation dependencies, with substantive proof-map rereview before affected implementation continues.
Rationale: The current plan requires the proof map before M1 but does not require its mandatory independent review until the lifecycle-closeout dependency, after implementation would already have occurred.
Required outcome: the execution sequence must not permit M1 or later implementation to rely on an unreviewed or substantively changed test specification.
Safe resolution path: add current test-spec-review settlement to the global and M1 dependencies and require rereview after substantive proof-map changes.
Follow-up: run a fresh plan review against the registered revised plan.
Validation target: M1 Dependencies, repository Dependencies, and the test-spec/test-spec-review handoff.
Validation evidence: `docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md` lines 68-72 and 389-399 at `sha256:e4de52bb785e50e85631cc417f227ff903842979c05cc5118c403f73f6b5b5c1`, registered by `evidence/plan-revision-r1.md`.

### plan-review-r3

No new material finding was evaluated or created. The invocation stopped before semantic rereview because `CRG-PLR2-1` remains open with disposition `needs-decision`. The blocker is recorded in `reviews/plan-review-r3.md`; this entry supplies no plan approval, finding disposition, or settlement.

### test-spec-review-r1

#### CRG-TSR1-1

Finding ID: CRG-TSR1-1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Decision owner: test-spec author
Decision needed: preserve every approved plan validation command in the test-spec command ledger and milestone proof map, or route any intended command removal back to the plan owner.
Chosen action: add CMD-010 through CMD-022 for the omitted focused, lifecycle, workflow, documentation, conformance, and closeout commands; update affected proof obligations, test cases, and all milestone rows without changing plan sequencing.
Rationale: The current proof map omits focused validator, workflow, lifecycle conformance, documentation, and closeout commands that the approved plan requires at M1 through M7.
Required outcome: Every approved-plan validation command has an exact test-spec command ID and retains its owner, first required milestone, failure behavior, zero-test behavior, evidence target, and side-effect boundary.
Safe resolution path: Revise the test specification to add and map the omitted commands; revise the plan first only if an approved command is intentionally removed; then rerun `test-spec-review` against the exact registered revision.
Follow-up: run independent `test-spec-review-r2` against the registered revision.
Validation target: Validation commands, milestone proof map, affected test-case command IDs, and PRF command mappings for M1 through M7.
Validation evidence: `specs/consolidated-review-gates.test.md` at `sha256:cb69d565f9744fb086172037f4b5872d3e2c2f0555e67142f1553a6108774596`; `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/evidence/test-spec-revision-r1.md`; documentation prose validation with zero errors and warnings; explicit-path lifecycle validation passed.

### code-review-m1-r1

#### CRG-M1-CR1

Finding ID: CRG-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: remove the entire dual-topology activation mechanism rather than repairing its missing-manifest fallback.
Rationale: The owner chose to retire old progression at one release cutover, so a manifest, baseline, per-change marker, and interpreter provide no steady-state value.
Required outcome: current runtime and metadata contain no activation authority; cutover is governed by complete release evidence and absence of nonterminal legacy-dependent work.
Safe resolution path: remove the manifest, schema, parser, new-change assignment, lifecycle projection, validators, and fixtures; align approved authored contracts; rerun focused and lifecycle validation.
Follow-up: run `code-review-m1-r2` over the corrected packet.
Validation target: CRG-R35, CRG-AC7, BND-COMPAT-001, INT-008, and CRG-T01.
Validation evidence: `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js` passed 155 tests; `python scripts/test-change-metadata-validator.py` passed 64 tests; `python scripts/test-artifact-lifecycle-validator.py` passed 170 tests; correction evidence is recorded in `evidence/m1-topology-foundation-implementation.md`.

#### CRG-M1-CR2

Finding ID: CRG-M1-CR2
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: specification author
Decision needed: resolved by the specification owner: do not preserve obsolete exact-output behavior by adding rendering or version-selection complexity.
Chosen action: amend R21-R22 and AC6 so a later approved feature may intentionally supersede affected lifecycle fields when its governing spec, fixtures, and release note change together; remove the abandoned topology fields from M1 output.
Rationale: compatibility protects against accidental drift, not against an explicitly approved release-visible feature change, and the single-cutover design no longer needs topology output.
Required outcome: no legacy renderer or output-version selector is added; public fixtures are changed only with an approved governing behavior change.
Safe resolution path: update the observability contract, remove topology output, and run the exact public-output fixture.
Follow-up: run `code-review-m1-r2` over the corrected packet.
Validation target: consolidated-review CRG-R35/CRG-AC7 and CLI-observability R21-R22/AC6/BND-COMPAT-001.
Validation evidence: `node --test packages/rigorloop/test/result-renderer.test.js` passed all 14 tests, including T10.

### code-review-m1-r2

No new material finding was created. The corrected local packet resolves the behavior described by `CRG-M1-CR1` and `CRG-M1-CR2`, but the rereview is inconclusive because the governing M1 artifacts remain untracked and the dirty runtime files contain unrelated lifecycle CLI work. This administrative entry supplies the review-log anchor required for the detailed inconclusive record; it creates no finding disposition, does not reopen review-resolution, and does not settle M1. A fresh review requires an identity-stable tracked M1 packet.

### code-review-cli-fix-r1

#### CRG-CLI-CR1

Finding ID: CRG-CLI-CR1
Disposition: rejected
Status: resolved
Owner: CLI specification owner
Owning stage: spec
Decision owner: CLI specification owner
Decision needed: none; the owner supplied the final disposition.
Chosen action: retain the implemented direct-review settlement contract unchanged.
Rationale: the owner rejected the proposed additional identity as unnecessary complexity. Direct settlement already binds the milestone implementation evidence, exact review evidence, and canonical review-log occurrence; automated review continues to require its packet identity.
Required outcome: none beyond preserving the implemented direct-versus-automated evidence distinction.
Safe resolution path: no implementation change required.
Follow-up: none.
Validation target: `specs/governed-lifecycle-cli.md` R16/E7, direct review settlement, completion fingerprint, and stale replay.
Validation evidence: owner rejection recorded 2026-08-29; targeted lifecycle suite passed 53 tests in Code Review CLI Fix R1.

### code-review-m2-r1

#### CRG-M2-CR1

Finding ID: CRG-M2-CR1
Disposition: accepted
Status: resolved
Owner: M2 implementation owner
Owning stage: implement
Decision owner: workflow owner
Decision needed: resolved; use explicit lifecycle invalidation rather than aggregate or per-document hashes.
Chosen action: remove `aggregate_revision`, content-derived package identity, and hash-based replay from the specification, ADR, schema, CLI, validators, fixtures, and tests.
Rationale: The owner requires a simple workflow. The reviewed stale-replay defect is real in the current mechanism, but removing that mechanism is safer and smaller than repairing its hash protocol.
Required outcome: package approval binds explicit member IDs and paths plus the review ID; authoring through the governed workflow marks the affected package `review-required`.
Safe resolution path: revise the governed contract first, simplify M2 implementation and proof, then rerun code review.
Follow-up: rerun M2 Code Review after implementation correction and targeted proof.
Validation target: CRG-R24, CRG-R26, CRG-T09, BND-TEMPORAL-001, INT-003.
Validation evidence: `code-review-m2-r2.md` confirms aggregate replay removal; the remaining evidence-order issue is recorded separately as CRG-M2-CR6.

#### CRG-M2-CR2

Finding ID: CRG-M2-CR2
Disposition: accepted
Status: resolved
Owner: M2 implementation owner
Owning stage: implement
Decision owner: M2 implementation owner
Decision needed: resolved; implement the approved blocker and next-action mapping.
Chosen action: keep each non-approved package status blocking and expose the single workflow-owned correction or rereview operation.
Rationale: Code Review directly observed blocked and inconclusive package outcomes as overall current state with no blockers and no next permitted operation.
Required outcome: every non-approved package outcome remains a blocker and exposes its contract-defined correction or rereview continuation.
Safe resolution path: derive blockers and next operations from non-approved package states and add direct status/context matrix tests.
Follow-up: rerun M2 Code Review after implementation correction and targeted proof.
Validation target: CRG-R25, CRG-R29, CRG-T06, CRG-T07, BND-STATE-001, INT-007.
Validation evidence: `code-review-m2-r2.md` confirms all non-approved statuses block; the remaining next-action issue is recorded separately as CRG-M2-CR7.

#### CRG-M2-CR3

Finding ID: CRG-M2-CR3
Disposition: rejected
Status: resolved
Owner: M2 implementation owner
Owning stage: implement
Decision owner: workflow owner
Decision needed: resolved; do not require per-document hashes.
Chosen action: reject content-hash freshness as package authority. Keep exact member IDs and paths visible and rely on governed authoring transitions to invalidate package approval.
Rationale: Per-document hashes and aggregate content hashing add bookkeeping and retry complexity that the project does not need. Direct out-of-workflow edits are an accepted limitation of the lightweight contract.
Required outcome: no package member content hashes are persisted or required; path, kind, role, owner, package status, and review evidence remain explicit.
Safe resolution path: remove hash requirements from the contract and implementation and test CLI-owned invalidation instead.
Follow-up: rerun M2 Code Review after implementation correction and targeted proof.
Validation target: CRG-R22, CRG-R26, CRG-T04, CRG-T09, BND-AUTH-001, INT-003.
Validation evidence: `code-review-m2-r2.md`; focused lifecycle 63/63 and full package 288/288 confirm the no-hash governed-invalidation model.

#### CRG-M2-CR4

Finding ID: CRG-M2-CR4
Disposition: accepted
Status: resolved
Owner: M2 implementation owner
Owning stage: implement
Decision owner: M2 implementation owner
Decision needed: resolved; enforce the approved member-to-owner mapping.
Chosen action: validate finding scope, affected member IDs, owning stages, and correction targets as one mapping resolved from the package's explicit ID-to-path members.
Rationale: Code Review recorded an artifact-local specification finding while naming plan as the owner and correction target.
Required outcome: finding scope, affected artifacts, owners, and correction targets form one valid authority mapping and contradictory mappings fail before recording.
Safe resolution path: validate owners from affected member kinds and upstream bindings, require cross-artifact coverage, constrain correction targets, and add mapping regressions.
Follow-up: rerun M2 Code Review after implementation correction and targeted proof.
Validation target: CRG-R30 through CRG-R33, CRG-T08, BND-AUTH-001, INT-001, INT-002, INT-007.
Validation evidence: `code-review-m2-r2.md`; `package review rejects contradictory finding owner and correction target mappings` passes through the public CLI.

### code-review-m2-r2

#### CRG-M2-CR5

Finding ID: CRG-M2-CR5
Disposition: accepted
Status: resolved
Owner: M2 implementation owner
Owning stage: implement
Decision owner: M2 implementation owner
Decision needed: resolved by owner instruction on 2026-08-30.
Chosen action: implement the already approved Proposal Review replacement invalidation path.
Rationale: Delivery invalidation exists for replacement Design Review, but Proposal Review settlement does not invalidate its dependent approved design package.
Required outcome: replacing the bound Proposal Review ID atomically sets design status to review-required, withholds authority, and retains the prior review ID.
Safe resolution path: add dependent design invalidation to proposal settlement and cover it through the public CLI.
Follow-up: resolve, implement, and rerun M2 Code Review.
Validation target: CRG-R24, CRG-R26, CRG-T09, BND-TEMPORAL-001, INT-003.
Validation evidence: public CLI regression `replacement Proposal Review invalidates approved design authority`; focused lifecycle 64/64 and full package 289/289 pass.

#### CRG-M2-CR6

Finding ID: CRG-M2-CR6
Disposition: accepted
Status: resolved
Owner: M2 implementation owner
Owning stage: implement
Decision owner: M2 implementation owner
Decision needed: resolved by owner instruction on 2026-08-30.
Chosen action: revalidate current package and review evidence before exact replay returns.
Rationale: settlement replay currently returns before rereading the registered review evidence and log.
Required outcome: exact replay revalidates current package and review evidence before returning already-recorded.
Safe resolution path: move replay recognition after evidence revalidation and add a public regression.
Follow-up: resolve, implement, and rerun M2 Code Review.
Validation target: CRG-R26, CRG-T06, BND-TEMPORAL-001.
Validation evidence: public CLI settlement-replay regression changes registered review evidence after settlement and receives `RL_STALE_EVIDENCE`; focused lifecycle 64/64 and full package 289/289 pass.

#### CRG-M2-CR7

Finding ID: CRG-M2-CR7
Disposition: accepted
Status: resolved
Owner: M2 implementation owner
Owning stage: implement
Decision owner: M2 implementation owner
Decision needed: resolved by owner instruction on 2026-08-30.
Chosen action: derive one safe next action from each non-approved package status.
Rationale: settled non-approved packages currently recommend settlement replay instead of correction, upstream resolution, or evidence acquisition and rereview.
Required outcome: each non-approved settled status exposes exactly one safe outcome-specific next action.
Safe resolution path: derive next action from status and correction targets and add a three-outcome public status matrix.
Follow-up: resolve, implement, and rerun M2 Code Review.
Validation target: CRG-R25, CRG-R29, CRG-T07, BND-STATE-001, INT-007.
Validation evidence: public three-outcome matrix confirms `route-correction` for changes requested, no automatic operation for an unrouteable block, and `record-package-review` for inconclusive; focused lifecycle 64/64 and full package 289/289 pass.

### code-review-cli-fix-r1 (continued)

#### CRG-CLI-CR2

Finding ID: CRG-CLI-CR2
Disposition: rejected
Status: resolved
Owner: CLI specification owner
Owning stage: spec
Decision owner: CLI specification owner
Decision needed: none; the owner supplied the final disposition.
Chosen action: retain the concise two-phase `complete-milestone` operation unchanged.
Rationale: the owner rejected an additional lifecycle operation and review cycle. The existing operation is state-specific: `implementing` requests review, while `review-requested` plus clean review evidence closes the milestone.
Required outcome: none beyond preserving the tested state-specific behavior.
Safe resolution path: no implementation change required.
Follow-up: none.
Validation target: `specs/governed-lifecycle-cli.md` E6/R3/R16/state invariants and `specs/rigorloop-workflow.md` R7x/R7xa.
Validation evidence: owner rejection recorded 2026-08-29; targeted lifecycle suite passed 53 tests in Code Review CLI Fix R1.

### spec-review-r4

#### CRG-SR5

Finding ID: CRG-SR5
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: workflow owner
Decision needed: resolved; the lightweight package contract invalidates authority from governed revision events, not repository byte inspection.
Chosen action: replace the byte-change invariant with explicit governed member-revision and upstream-review-settlement triggers.
Rationale: The owner explicitly rejected aggregate and per-document hashing. Requiring automatic detection of every direct byte edit would silently reintroduce the same content-inspection mechanism.
Required outcome: CRG-R24, invariants, boundaries, examples, and acceptance criteria describe one consistent no-hash invalidation boundary.
Safe resolution path: revise the specification through the active correction route, record the new spec revision, and rerun `spec-review`.
Follow-up: rerun focused Spec Review R5 after the authoring correction.
Validation target: CRG-R22 through CRG-R26, CRG-AC4, BND-STATE-001, BND-TEMPORAL-001, and INT-003.
Validation evidence: `node --test packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-evidence.test.js` passed 15 tests; `python scripts/validate-review-artifacts.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates` passed structure validation; direct inspection confirms CRG-R24, the package invalidation glossary, State and invariants, and EC11 now use one governed-event, no-hash contract. Boundary proof-map validation remains a downstream test-spec revision dependency and is not claimed here.
