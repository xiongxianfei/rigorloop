# Adopt a Compact Current-State Change Record

## Challenge

RigorLoop records lifecycle state, reviews, findings, resolutions, validation evidence, correction routing, transition inputs, and final verification in Git. That traceability is valuable, but the active change record can describe one workflow event across several overlapping files: an operation request, review record, review log, resolution ledger, correction route and return receipt, authoring evidence, validation evidence, and repeated history in `change.yaml`.

The resulting working tree mixes current truth with superseded procedure. A resuming developer or agent may need to inspect many records to determine the current stage, authoritative artifacts, open findings, still-applicable decisions, current evidence, blockers, and remaining work. Context cost therefore grows with review rounds, corrections, transitions, and evidence events even when two changes have the same effective state.

Traceability does not require every successful command input, transport receipt, superseded review round, or repeated summary to remain in the active tree. The required resume contract is narrower: a new developer or agent must be able to reconstruct the current effective state, open findings, material resolved decisions, current evidence basis, and remaining work without loading complete workflow history.

The current projection model also conflates overall lifecycle readiness with the eligibility of one corrective operation. Open findings, stale evidence, and invalidated downstream reviews correctly prevent progression, but those same expected conditions can make an authoring context report an undifferentiated blocked result even when the corrective operation is structurally safe and necessary. A global blocker must not become accidental authority that disables its own resolution.

## Goals

- Establish one compact, authoritative working set for each governed change.
- Make current state directly reconstructable without loading complete workflow history.
- Preserve current independent review judgments, open findings, and their ownership and blocking effect.
- Preserve resolved decisions that materially constrain later work.
- Preserve the provenance, scope, outcome, subject identity, and freshness of evidence currently relied upon.
- Discard superseded procedural detail after every continuing consequence has been retained in the authoritative current working set.
- Stop committing successful operation requests and routine transport receipts by default.
- Replace per-round review files with stable current review records and remove duplicated review indexes and resolution summaries.
- Provide bounded CLI projections for routing, resumption, review, and verification.
- Distinguish overall progression readiness from operation-specific eligibility so expected correction blockers cannot deadlock their owning recovery work.
- Separate a reviewer's current judgment, a decision owner's explicit acceptance, and lifecycle progression so routine gates do not require a universal `approved` outcome.
- Reduce repository noise, merge surfaces, maintenance cost, and agent-context growth without weakening independent review or readiness evidence.

## Scope and non-goals

### In scope

This direction covers `change.yaml`; formal review records; open-finding and material-resolution retention; current evidence; lifecycle-transition inputs; correction-route and correction-return receipts; routine stage-authoring evidence; review indexes and logs; CLI current-state and resume projections; relevant skills, templates, references, schemas, validators, fixtures, governance, architecture, and contributor guidance; and generated packages for supported adapters.

### Initial intent treatment

| Initial goal or constraint | Treatment | Destination |
| --- | --- | --- |
| One compact authoritative working set | in scope | Target working set and retention classes |
| Direct reconstruction of current state and remaining work | in scope | `change.yaml` and bounded CLI projections with derived allowed operations |
| Current review judgments and open findings remain durable | in scope | Stable current review records |
| Material resolved decisions remain durable | in scope | `material-decisions.md` |
| Current evidence remains attributable and freshness-aware | in scope | `evidence.yaml` and final Verify report |
| Superseded procedure leaves the governed record | in scope | Promotion-before-replacement invariant and disposable-history policy |
| Routine requests, receipts, authoring evidence, logs, and ledgers are retired | in scope | Prospective retention policy |
| Independent review and readiness proof remain mandatory | in scope | Review and verification boundaries |
| Exact schemas, commands, concurrency protocol, and freshness algorithm | deferred follow-up | Design and Delivery |
| Completed historical changes are compacted or rewritten | out of scope | Prospective compatibility policy |
| Full raw test output or CLI diagnostics are committed by default | out of scope | External or machine-local detail retention |
| Hosted state service, external database, or tamper-proof audit ledger | out of scope | Product boundary |

### Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact working-set and retention policy | core to this proposal | This is the direction being approved. |
| Current-state `change.yaml` semantics | core to this proposal | Lifecycle coordination needs one current owner. |
| Stable review records and open-finding visibility | core to this proposal | Independent judgment must remain directly accessible. |
| Material-decision memory | core to this proposal | Non-obvious resolved constraints must survive compaction. |
| Current evidence manifest and final Verify report | core to this proposal | Readiness still requires attributable, current proof. |
| Retirement of routine requests, receipts, logs, ledgers, and authoring evidence | core to this proposal | These duplications create the history-heavy active model. |
| Bounded current-state and skill-context projections | core to this proposal | Consumers need a supported alternative to broad directory scans. |
| Scoped operation eligibility and blocker classification | core to this proposal | Global downstream blockers must remain visible without disabling a safe corrective operation. |
| Review judgment, decision authority, and progression separation | core to this proposal | A universal approval outcome duplicates state and obscures who actually decides or permits an operation. |
| Git-independent bootstrap closeout for this implementing change | same-slice dependency | The replacement cannot responsibly activate through a final gate that requires the Git identity or superseded history it removes. |
| Constitution, workflow/spec, architecture/ADR, skill, CLI, validator, fixture, documentation, and adapter updates | same-slice dependency | Activation is unsafe while authoritative and public surfaces disagree. |
| Exact file schemas, mutation ownership, atomicity, revision checks, concurrency, evidence invalidation, and commands | first-slice candidate | These are Design decisions, not proposal decisions. |
| Implementation sequencing, prospective activation, rollback steps, and proof allocation | separate implementation slice | Delivery must make the cross-surface cutover reviewable and recoverable. |
| Historical change rewriting | out of scope | Existing completed records remain valid historical evidence. |

### Non-goals

This proposal does not remove independent review, open findings, material resolution rationale, current validation evidence, or Git-tracked proposal, specification, architecture, ADR, and plan artifacts. It does not require reconstruction of every historical transition from the current working tree, discard information merely to meet a file-count or token target, combine all change information into one large file, standardize complete raw test output, or approve detailed schemas, APIs, commands, algorithms, implementation sequencing, or verification design.

## Governing principle

> **RigorLoop should retain only the authoritative state needed to resume and justify the current change; reviews record judgment, decision owners make material choices, and the CLI derives structural eligibility without inventing authority.**

## Proposed direction

Adopt a compact current-state change record with five applicable durable surfaces:

```text
docs/changes/<change-id>/
├── change.yaml
├── reviews/
│   ├── proposal-review.md
│   ├── design-review.md
│   ├── delivery-review.md
│   └── code-review-<target>.md
├── material-decisions.md
├── evidence.yaml
└── verify-report.md
```

Only applicable records should exist; the structure is not a requirement to create empty files. Approved engineering artifacts remain in their canonical locations and are referenced from the change record.

`change.yaml` should be the current lifecycle-coordination snapshot. It should identify the effective stage and revision, current artifact identities, review-package states, active milestone, open-finding and evidence references, blockers, remaining work, and readiness. It should reference authoritative records rather than duplicate their contents and should not retain a verbose ledger of prior transitions, routes, returns, review rounds, request payloads, evidence events, or a caller-maintained list of allowed operations. The CLI should derive currently allowed structural operations for projections from the current state and target.

Each formal review gate or Code Review target should use one stable current review path. A new round updates that record with its current round, reviewed subject identity, outcome, open findings, ownership, blocking effect, material-decision references, and progression limitations. Before replacement, the CLI must prove that every open finding remains visible and every still-constraining resolved decision has been promoted to `material-decisions.md`. Superseded review wording and non-material resolved findings may then be discarded. A consumer must not reconstruct current truth from superseded files or routing history.

The ordinary artifact-review loop should be owned by review settlement rather than a separate correction route and return. After an author submits a Proposal for Proposal Review, the reviewer records the current judgment. A current review with no blocking findings is clear and satisfies the gate; a review with findings returns the subject to its owning stage for refinement; a blocked or inconclusive review remains at the review gate. The same pattern should apply at other formal gates. The caller should not separately choose the resulting artifact status or next stage.

A universal `approved` review outcome should not be required. The current review record should express independent judgment, conceptually `clear`, `findings-open`, or `blocked`; exact vocabulary belongs to Design. Lifecycle progression should be derived from a current exact-subject review, the absence of blocking findings, current required evidence, and the applicable transition rules. Explicit decision-owner acceptance should be recorded only when a discretionary direction, exception, limitation, or residual risk requires that owner's judgment. It should not be duplicated as routine review, settlement, and readiness statuses.

Resolved findings should remain in `material-decisions.md` only when their resolution continues to constrain the change—for example, by changing a requirement, architecture invariant, authority or security boundary, compatibility behavior, accepted limitation, residual risk, non-obvious implementation direction, or downstream verification obligation. Routine wording, formatting, assertion, and localized defect corrections need not remain in an active resolution ledger. Uncertain materiality should favor temporary retention until the decision no longer constrains the change.

`evidence.yaml` should describe the evidence currently relied upon for review, progression, and verification, including the evaluated claim or verification group, exact subject paths and identities, method, outcome, covered surfaces, detail location when retained elsewhere, and freshness. It should normally retain metadata and provenance rather than raw output. The CLI should compare only these explicit bounded identities—without Git or PR data—and block reliance when a subject has drifted until an explicit mutation replaces or invalidates the evidence. Superseded evidence metadata may be discarded once it no longer supports a current claim, blocker, material decision, or readiness judgment.

Successful final Verify should create or update one `verify-report.md` bound to the exact passing subject. It should record the readiness verdict, impact classification, reused and rerun evidence, limitations or residual risks, final explanation of what changed and why, and PR handoff information. Failed attempts may update current state and evidence but should not create a successful readiness explanation.

Successful lifecycle-operation requests, routine correction-route and correction-return receipts, redundant stage-authoring evidence, `review-log.md`, broad resolution ledgers, correction-history summaries, and workflow-history summaries should no longer be mandatory committed artifacts. A finding raised by the review immediately following an artifact's authoring should use the ordinary review-settlement loop and should not create separate correction routing state.

When a later gate discovers a non-adjacent upstream problem, the workflow should support an explicit current-state correction. Routing starts correction authoring at the responsible upstream stage. An explicit return means only that the exact corrected content is ready for its required review; it moves to that review while keeping the correction active and never implies approval. Review settlement then either returns findings to correction authoring, retains a blocked or inconclusive review, or closes the correction after a clear current judgment with no blocking finding. On closure, the CLI derives the earliest downstream gate whose decision basis must be re-established before the original source stage may be resumed. That revalidation path is projection output, not a caller-supplied or independently stored `invalidated_gates` list.

Active correction state should expose only current coordination such as source findings, owner, destination, correction status, required review, and eventual resume target. After review settlement closes it, only current lifecycle state, current review judgment, applicable evidence, and any material decision remain active. Bounded machine-local logs may retain command-execution diagnostics, but they are optional, non-authoritative, and never required for resumption, progression, review, or verification.

The CLI should accept semantic intent and stage-owned content, then mechanically derive and atomically update authoritative current records. Callers should not construct or submit the resulting `change.yaml`, derived references, readiness, allowed-operation list, lifecycle revision, required review, or downstream revalidation path. The CLI should evaluate whether an operation is structurally eligible; it should neither demand a ceremonial approval label nor grant human or stage permission. The CLI should provide bounded human-readable and machine-readable projections for current state, reviews, open findings, material decisions, current evidence, remaining work, derived allowed operations, required revalidation, and exact skill-required paths.

Those projections must distinguish overall progression readiness from the eligibility of the requested stage operation. Global blockers remain visible and continue to prevent downstream advancement, while operation-specific blockers determine whether the requested mutation may run. A change may therefore be globally blocked yet expose a safe corrective operation as actionable. An undifferentiated `blocked` label, stored status, or diagnostic list must not itself grant or deny an operation; eligibility is derived from the operation, current lifecycle state, target, exact identities, and applicable invariants. The exact projection fields and diagnostic vocabulary belong to Design.

Operation eligibility should not come from a caller-supplied permission or identity claim. The CLI is a local consistency tool, not an authentication or authorization service: filesystem and execution access remain the enclosing trust boundary, while owner, reviewer, and producer labels record responsibility and provenance only. It should not require or provide governed historical reconstruction. The exact command vocabulary, schemas, revision protocol, concurrency controls, and evidence-freshness algorithm belong to Design.

Every lifecycle datum should have one retention class: current authoritative state, material decision memory, current evidence basis, disposable superseded procedure, or optional operational diagnostics. Before creating a governed change-local artifact, RigorLoop should ask whether that exact record is needed to understand current state, an open finding, a material decision, current evidence, or remaining work. If not, it should be derived, logged locally when operationally useful, or omitted. Before replacing current state, the CLI must prove that all information still needed for resumption, decision justification, or readiness remains in a current authoritative surface.

The model applies prospectively after a coherent activation. Completed historical changes retain their existing structures, and ordinary changes already in flight finish under their registered contract. The first compact version provides no general in-place legacy migration; no skill may silently reinterpret an existing change.

The change implementing this replacement needs one bounded preactivation closeout rule because requiring it to finish through Git-bound identity and history-wide legacy validation would make the retired model a permanent dependency of its successor. That rule should bind final review and Verify to one deterministic exact-current-set identity covering the authoritative contracts, implementation, current review state, current evidence, lifecycle revision, and activation manifest. It should validate only current consequential state, treat already-settled superseded procedure as historical, leave this change structurally in its registered contract, and activate compact writing only after final review is clear and Verify passes. It is not a general migration path or a validation bypass.

## Feasibility

**Assessment: Feasible, with a broad contract-replacement constraint.**

The required information already exists in RigorLoop, but ownership is distributed across overlapping files. The CLI already mediates governed transitions, and current skills and validators already reason about artifact identity, review findings, validation outcomes, lifecycle revision, and permitted operations. These provide a credible basis for consolidating current lifecycle truth in `change.yaml`, current judgment in stable review records, durable rationale in `material-decisions.md`, current proof in `evidence.yaml`, and final readiness in `verify-report.md`.

The existing workflow has demonstrated the scoped-eligibility problem directly: an invalidated Design package and open finding correctly blocked downstream progression while the authoring context simultaneously identified a structurally permitted artifact-revision operation. Resolving that contradiction requires projection and consumer-contract changes, not a new service or authority mechanism, so it does not undermine feasibility.

The direction intentionally supersedes parts of the accepted compact-validation and bounded-read models that require event-oriented reconstruction from `change.yaml`, treat `review-log.md` and `review-resolution.md` as current authorities, require routine approval-shaped outcomes, or bind final readiness to Git or PR state. It also conflicts with current constitutional and workflow rules that mandate some of those behaviors. Acceptance of this direction therefore authorizes Design to define a coherent replacement package and the bounded implementing-change bootstrap; it does not itself activate the model or permit lower-priority artifacts or code to diverge. Responsible Design must identify every affected higher-priority contract, define historical readability and in-flight adoption, and prevent mixed-model progression. No known conceptual blocker requires each operation or review round to remain a separately committed file or each successful review to carry a universal approval label.

## Impact and major trade-offs

The active record should scale mainly with current engineering content, open findings, material decisions, and current proof rather than procedural history. This makes resumption more predictable and reduces repository noise, repeated summaries, merge surfaces, validator complexity, and context loading.

The accepted trade-off is deliberate loss of procedural chronology. Prior requests, routes, returns, review wording, routine resolved findings, and stale evidence may become permanently unavailable after their continuing consequences are represented in the authoritative current working set. Exact event replay and historical reconstruction are not part of the resume contract.

Stable records concentrate responsibility. An incorrect update could hide an open finding or present stale evidence as current, and multiple actors could contend for one review target. Design must therefore define one lifecycle-derived operation-eligibility matrix, responsibility metadata, expected-revision checks, bounded subject-identity resolution, atomic multi-record updates, finding consistency, evidence invalidation, mechanically derived resulting state, and rejection of stale concurrent writes. It must not claim that a local CLI can prove who invoked it.

Scoped eligibility adds one presentation obligation: consumers must not mistake an actionable correction for overall readiness, or a downstream blocker for a prohibition on its owning correction. Design must make both conclusions explicit and fail closed when the requested operation itself has unresolved authority, identity, state, or recovery blockers.

Materiality cannot be reduced entirely to file mechanics. Skills and reviewers need shared criteria, and ambiguous cases should favor retention until the responsible owner determines that a decision no longer constrains the change. Public guidance must preserve independent review and readiness rigor so compaction cannot become an excuse to erase adverse evidence.

Replacing universal approval with a clear review judgment reduces ceremony but makes derived progression rules more important. Design must ensure that `clear` always binds the exact current subject, that any material owner decision remains explicit, and that revision or evidence drift removes progression eligibility without rewriting the reviewer's historical judgment.

Existing approved specs, governance, architecture, skills, validators, fixtures, and adapter packages encode the history-oriented model. Activation must be coherent across those surfaces, preserve historical readability, provide rollback, and avoid a period in which different consumers treat different files as authoritative.

The implementing-change bootstrap is intentionally exceptional. Its narrow identity and activation conditions must be inspectable and fail closed; broad grandfathering or ignoring current findings would weaken the same readiness guarantees this proposal preserves.

## Decision requested

Approve the direction to:

1. replace RigorLoop's history-heavy active change record with a compact current-state model;
2. use `change.yaml`, stable current review records, `material-decisions.md`, `evidence.yaml`, and `verify-report.md` as the applicable durable change-local working set;
3. keep proposal, specification, architecture, applicable ADRs, and plan as canonical engineering contracts referenced by the change record;
4. make `change.yaml` a current-state coordination snapshot rather than a transition-history ledger;
5. use one stable current review record per gate or Code Review target, with open findings directly visible, and make review settlement derive either revision by the owning stage, blocked review, or downstream progression from a clear exact-subject judgment;
6. retain only materially constraining resolved decisions in `material-decisions.md`;
7. record current evidence provenance, scope, outcome, subject identity, and freshness in `evidence.yaml`, while retaining raw output elsewhere by exception;
8. retire mandatory committed successful-operation requests, routine correction route/return receipts, routine authoring evidence, duplicated review logs, broad resolution ledgers, and history summaries while retaining explicit current-state route and return operations for non-adjacent corrections;
9. avoid relying on Git history, pull-request history, or machine-local logs for resumption, progression, review, or verification, and allow superseded non-material procedure to be discarded once its continuing consequences are retained in the authoritative current working set;
10. require bounded CLI projections for current-state, resume, review, and verification questions, including any derived downstream revalidation path, without requiring governed historical reconstruction;
11. distinguish overall progression readiness, downstream blockers, and operation-specific eligibility so a globally blocked change may still expose the exact safe operation needed to resolve its blockers;
12. apply the model prospectively after coherent contract, tooling, skill, validation, documentation, and adapter activation while leaving completed historical changes unchanged; and
13. separate review judgment, explicit decision-owner acceptance, and lifecycle progression; treat a clear current review with no blocking findings as the ordinary review prerequisite for progression rather than requiring a universal `approved` outcome;
14. make explicit correction return mean review-ready rather than approved, and require the returning review to establish the new current judgment;
15. require ordinary in-flight legacy changes to finish under their registered contract, omit general in-place legacy migration from the first compact version, and preserve independent review, open findings, current evidence, and final readiness proof throughout the prospective cutover; and
16. authorize one bounded Git-independent preactivation closeout rule for this implementing change, using an exact-current-set identity and current consequential validation before coherent activation.

Approval establishes the compact change-record direction and retention boundaries. It does not approve exact schemas, CLI commands, concurrency controls, evidence-freshness algorithms, implementation sequencing, or verification design, and it does not override current higher-priority contracts before their governed amendment and coherent activation.
