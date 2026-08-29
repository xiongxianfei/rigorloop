# Review Resolution: Consolidate RigorLoop Review Gates

## Summary

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: code-review-m1-r1

- Reviews covered: `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `plan-review-r2`, `test-spec-review-r1`, `code-review-m1-r1`
- Findings resolved: 8
- Unresolved findings: 0
- Current result: Both Code Review M1 R1 findings are resolved through the owner-approved single-cutover correction. M1 requires fresh code review; resolution does not substitute for rereview.

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

## Finding Details

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
