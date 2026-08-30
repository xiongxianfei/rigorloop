# Code Review M2 R1: Aggregate Review Package Authority

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex isolated independent code-review context with fresh-assumption reset
Review date: 2026-08-29
Target: commit `2dee37d9118c9fdeaee58785867040e06e3f92b2`
Reviewed milestone: M2
Reviewed artifact: M2 committed package-authority implementation
Status: changes-requested
Review status: changes-requested
Material findings: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m2-r1.md`, `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`, and `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Open blockers: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
- Verify readiness: not-claimed

## Review inputs

- Commit range: `a24f52c0d3472182bdaabca6d897818dc4111367..2dee37d9118c9fdeaee58785867040e06e3f92b2`
- Governing authority: `specs/consolidated-review-gates.md` CRG-R12 through CRG-R34; `docs/adr/ADR-20260828-consolidated-review-package-topology.md`; M2 in `docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md`; CRG-T04 through CRG-T10 in `specs/consolidated-review-gates.test.md`
- Implementation evidence: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/evidence/m2-aggregate-review-packages-implementation.md`
- Current lifecycle state: M2 `review-requested`, current stage `code-review`; M3 through M6 remain planned
- Reviewed surfaces: package composition and identity, lifecycle request and settlement evaluation, read-model projection, schema and Python validators, public output fixture, focused tests, and transaction proof

## Actual-diff summary

M2 introduces deterministic design and delivery package composition, `review-package-sha256-v1`, package review registration and settlement operations, compact package projections, package status/context output, closed schema and validator vocabularies, transaction tests, and an updated detailed-output compatibility fixture. The implementation correctly avoids durable per-member content hashes and reuses the single-file lifecycle transaction boundary, but four public and authority paths remain unsafe or incomplete.

## Findings

### Finding CRG-M2-CR1

Finding ID: CRG-M2-CR1
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:742-752`; stale replay path in `packages/rigorloop/dist/lib/lifecycle-cli.js:206-216`
Evidence: `settle-review-package` returns `already-recorded` from the stored projection at lines 744-746 before recalculating current package membership, member bytes, upstream binding, or review evidence. The CLI explicitly invokes this evaluator when the request lifecycle revision is stale. Direct public-CLI proof settled a design package, changed the specification bytes, and replayed the original settlement request; the command exited 0 with `status: already-recorded` and no errors. CRG-R24, CRG-R26, BND-TEMPORAL-001, INT-003, and CRG-T09 require changed inputs to reject stale authority and require rereview.
Required outcome: Exact replay may return `already-recorded` only after current package and review evidence are recalculated and shown identical to the settled projection; a changed member, membership, upstream binding, or evidence identity must return stale evidence without mutation.
Safe resolution path: Move semantic replay recognition after package-context and review-evidence freshness checks, add post-settlement member, binding, and evidence-change replay tests through the public CLI, and retain idempotent success only for byte-identical current inputs.
needs-decision rationale: none

### Finding CRG-M2-CR2

Finding ID: CRG-M2-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-packages.js:114-134`; package status projection in `packages/rigorloop/dist/lib/lifecycle-read.js:273-319`
Evidence: Package blockers are created only for stale projections, and `next_permitted_operation` becomes null whenever a current projection exists. Direct public status proof after settling `blocked` and `inconclusive` reviews reported overall `effective_state: current`, an empty blocker list, no next operation, and withheld package authority. CRG-R29 requires every non-approved result to expose itself as a blocker and defines acquisition of evidence plus same-package rereview for inconclusive results; CRG-R25 requires a safe next permitted operation.
Required outcome: Changes-requested, blocked, and inconclusive package states must be explicit blockers with outcome-specific correction or rereview continuation facts. A non-approved current projection must not appear as an unblocked current lifecycle state or suppress the required next review operation.
Safe resolution path: Derive blockers and next operations from every non-approved state, distinguish correction routing from same-package rereview, and add status/context assertions for all three non-approved outcomes with and without material findings.
needs-decision rationale: none

### Finding CRG-M2-CR3

Finding ID: CRG-M2-CR3
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-packages.js:95-110`; `packages/rigorloop/dist/lib/lifecycle-operations.js:724-761`
Evidence: Package composition verifies registration path, kind, and role but never requires the registered `artifact_sha256` to match current member bytes. Package mutations then evaluate without rejecting the interpreted change's stale-evidence blockers. Direct public-CLI proof changed the specification without recording an author-owned artifact revision; context reported `stale_evidence: [spec]`, yet `record-package-review` and `settle-review-package` both exited 0 and persisted `authority: granted`. This bypasses the stage-owned revision boundary and violates the ADR's current-registered-artifact rule, CRG-R22, CRG-R26, BND-AUTH-001, and INT-003.
Required outcome: Package review recording and settlement must require every member's current bytes to match its author-owned exact artifact registration and must reject unresolved lifecycle freshness blockers that invalidate package authority.
Safe resolution path: Validate current content identity against each member registration during composition or mutation, reject stale authoring registrations before review recording and settlement, and add public tests proving that authoring revision registration is required before a changed member can enter a package review.
needs-decision rationale: none

### Finding CRG-M2-CR4

Finding ID: CRG-M2-CR4
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-packages.js:151-171,196-199`
Evidence: Finding validation requires only a non-empty `owning_stages` list and validates correction targets only as unique safe identifiers. It does not bind an artifact-local owner to its affected artifact, require cross-artifact owners to cover affected artifacts, or restrict correction targets to the finding's authorized owners. Direct public-CLI proof recorded an artifact-local finding affecting `spec` while naming `plan` as its owner and sole correction target; the operation exited 0. CRG-R31 through CRG-R33, BND-AUTH-001, INT-001, INT-002, and INT-007 require precise ownership and routing to every necessary owner.
Required outcome: Finding scope, affected artifact IDs, owning stages, and correction targets must form one validated authority mapping; contradictory or incomplete mappings must fail before recording.
Safe resolution path: Derive or validate allowed owning stages from package-member kinds and upstream bindings, require cross-artifact ownership coverage, constrain correction targets to the validated owner set, support the approved decision-needed alternative, and add artifact-local, cross-artifact, upstream-direction, missing-owner, extra-owner, and mismatched-target fixtures.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CRG-M2-CR1 through CRG-M2-CR4 violate CRG-R22 through CRG-R34 authority, retry, blocker, and attribution outcomes. |
| Test coverage | block | The 285-test suite passes, but it omits stale replay after completed settlement, blocker semantics for finding-free non-approved outcomes, stale registration admission, and mismatched ownership. |
| Edge cases | block | Stale post-settlement retry succeeds; blocked and inconclusive states appear current; stale registered members can be approved. |
| Error handling | block | Four invalid or stopped paths return success or an unblocked state rather than a closed error or blocker. |
| Architecture boundaries | block | Review authority can consume an authoring revision that its owner never registered, and correction targets are not bound to owning stages. |
| Compatibility | pass | The approved observability contract permits the detailed lifecycle facts added by this feature, and the exact fixture was updated with the governing spec already amended. |
| Security/privacy | pass | No secret, personal-data, credential, network, logging, or external-account surface was introduced. |
| Derived artifact currency | pass | M2 changes runtime, schema, validators, and fixtures only; canonical skill and generated adapter work remains explicitly assigned to M4 and M5 before cutover. |
| Unrelated changes | pass | Commit `2dee37d9` is bounded to M2 package authority, validators, tests, evidence, and the required output fixture. |
| Validation evidence | concern | Named suites pass and transaction rollback proof is relevant, but the direct public counterexamples show that the selected assertions are insufficient for CRG-T06 through CRG-T09. |

## Direct proof

```text
stale-settled-replay => exit 0, status already-recorded, errors []
blocked-status => effective current, blockers [], next_permitted_operation null
inconclusive-status => effective current, blockers [], next_permitted_operation null
unregistered-revision => stale_evidence [spec], record exit 0, settle exit 0, authority granted
mismatched-owner => record exit 0, status success, errors []
```

The implementation evidence reports 61 focused lifecycle tests, 285 package tests, 104 review-validator tests, 5 governed-CLI validator tests, and 66 metadata-validator tests passing. Those results remain useful regression evidence, but they do not negate the public counterexamples above.

## Handoff

This direct formal review is isolated. There is no automatic downstream handoff or lifecycle-state mutation. M2 remains open and requires review-resolution, implementation correction, targeted regression proof for all four findings, and a fresh M2 code review. No upstream product or architecture decision is required unless the implementation owner disputes the approved mappings.
