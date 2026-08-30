# Proposal Review: Governed Repository CLI Architecture

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex isolated proposal-review context
Target: `docs/proposals/2026-08-28-governed-repository-cli-architecture.md`

Reviewed artifact: `docs/proposals/2026-08-28-governed-repository-cli-architecture.md` at `sha256:41e02d64909f793f31ee1e8c4922baece81bd0d2774e79015c85f2d61063a8ea`
Review date: 2026-08-28
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: CLIARCH-PR1, CLIARCH-PR2, CLIARCH-PR3
- Open blockers: the enforcement claim lacks a provable boundary, governed file coverage remains open despite the stated universal goal, and the selected option bundles modularization with multi-file publication without comparing the lower-risk split
- Proposal readiness: not ready for specification
- Immediate next stage: isolated stop; proposal revision followed by same-stage proposal rereview
- Automatic downstream handoff: none
- Claim limitations: this isolated advisory review records judgment only; it does not settle the portable proposal, create its owning governed change, authorize specification, or continue workflow

## Overall Assessment

The proposal identifies a real architecture problem and chooses sound internal principles: one public executable, a thin command shell, a single operation registry, immutable snapshots, a pure domain, typed repository adapters, and concise result projection. It preserves Git-native truth, semantic ownership, workflow routing authority, compatibility, and portable skill use. The current code supports the diagnosis: the public binary is 2,221 lines, the lifecycle operation module is 740 lines, and the nominal transition evaluator receives a repository root and performs file and Markdown reads.

The proposal is not yet ready for specification because its enforcement and scope claims are not closed. A local CLI and a later CI job can validate resulting repository facts, but committed bytes do not reveal whether equivalent content was produced by the CLI or edited directly. The proposal currently treats provenance detection as both a planned enforcement capability and an open question. It also translates the user's universal `docs/changes/` direction into “supported” files while leaving the exact file classes open, so an incomplete command set could satisfy the text. Finally, it selects multi-file publication as inseparable from internal modularization without comparing the materially simpler option of first correcting the internal architecture while retaining the existing single-`change.yaml` transaction boundary.

## Material Findings

### Finding CLIARCH-PR1

Finding ID: CLIARCH-PR1

Severity: major

Location: `Goals`; `Scope budget`; `Testing and Verification Strategy`; `Rollout and Rollback`; `Risks and Mitigations`; open question 6

Evidence: The proposal plans “CI enforcement against unsupported direct change-local writes” and says CI tests should distinguish supported CLI publication from direct mutation. It simultaneously asks how CI can distinguish a CLI-produced diff from a semantically equivalent direct edit without hidden signatures or external state. The approved lifecycle CLI threat model explicitly says the CLI is not a cryptographic security perimeter and assigns stronger authorization to Git permissions, protected branches, and trusted CI. Once only equivalent repository bytes remain, ordinary validation can prove consistency but cannot prove which local process wrote them.

Required outcome: define enforcement truthfully at proposal level by choosing whether the product enforces valid resulting state, records non-authoritative operation provenance, or introduces an independently trustworthy authorization mechanism. Do not promise CI proof of CLI authorship without a durable trusted signal.

Safe resolution path: select invariant enforcement as the first boundary: governed skills and supported automation use typed commands, CI validates resulting state and rejects detectable invalid transitions, but CI does not claim writer provenance. If provenance is still valuable, classify an operation receipt as diagnostic or integrity evidence and state its limits; route cryptographically trustworthy authorship enforcement to a separate proposal involving trusted CI or signatures.

needs-decision rationale: the proposal author must choose the meaning of “mandatory” and “enforcement” before the specification can define acceptance criteria that are technically possible.

### Finding CLIARCH-PR2

Finding ID: CLIARCH-PR2

Severity: major

Location: `Goals`; `Initial intent preservation`; `Scope budget`; `Expected Behavior Changes`; open question 2; `Decision Log`

Evidence: The user's direction was that every operation under `docs/changes` should go through the CLI. The proposal classifies that goal as in scope, but repeatedly limits the boundary to “supported” governed files and leaves the exact file classes for the first publication slice open. It does not state the eventual closed set, treatment of unknown future file classes, or explicit exclusions for reads and transient lock, staging, and recovery files. Therefore a specification could cover only reviews and `change.yaml`, defer other durable evidence indefinitely, and still claim the proposal was satisfied.

Required outcome: state the complete policy boundary and classify every current durable `docs/changes/<change-id>/` artifact family, transient file family, and read-only operation as governed by typed publication, explicitly exempt, or separately routed. Preserve the user's goal or record and justify a deliberate narrowing.

Safe resolution path: define the target as all durable governed writes under the change root, including `change.yaml`, review records, `review-log.md`, conditional `review-resolution.md`, registered evidence, explanation, verification report, and workflow-owned receipts. Exclude reads and CLI-owned transient lock, staging, and recovery files. Require new durable change-local artifact classes to register a typed owner and publication operation before enforcement applies to them. Then use the scope budget to identify which command families activate in the first implementation slice without weakening the final policy.

needs-decision rationale: the proposal author must decide whether the universal boundary is the actual target or whether some durable change-local writers intentionally remain direct.

### Finding CLIARCH-PR3

Finding ID: CLIARCH-PR3

Severity: major

Location: `Problem`; `Goals`; `Scope budget`; `Options Considered`; `Recommended Direction`; `Architecture Impact`

Evidence: The proposal establishes two independent product changes as one core decision: refactor the existing CLI into a pure modular architecture, and expand mutation from one `change.yaml` replacement to recoverable multi-file semantic publication. O1 keeps both the current structure and current transaction, while O2 changes both. The option set does not evaluate modularizing the engine and operation registry while preserving stage-owned direct Markdown writes and the existing single-file lifecycle transaction. That lower-risk option could resolve the documented 2,221-line entrypoint, 740-line evaluator, filesystem access inside policy, and duplicated vocabularies without introducing multi-file crash recovery or a new semantic publication UX.

Required outcome: compare the modular-single-file alternative against the selected combined direction using explicit criteria such as defect isolation, evidence/state coherence, user friction, data-loss exposure, migration cost, token reduction, and enforcement value. Establish why multi-file publication is necessary to solve the stated problem, or split it into a separately decidable proposal.

Safe resolution path: add an option that delivers the thin shell, operation registry, immutable snapshot, pure domain, and compatibility adapter while retaining the approved single-file transaction and current stage-owned Markdown publication. If evidence/state coherence justifies multi-file publication, show why registration-after-write cannot provide sufficient integrity and retain the combined direction; otherwise select modularization first and route governed semantic publication to a follow-up proposal.

needs-decision rationale: the proposal author owns the investment decision between a focused architecture correction and a broader persistence-boundary expansion.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The implementation coupling and incomplete evidence/state boundary are described separately and concretely. |
| User value | concern | Reduced lifecycle mechanics and fewer adjacent defects are valuable, but the incremental value of multi-file publication over modularization alone is not established. |
| Option diversity | block | The strongest lower-risk alternative—modular architecture with the existing single-file transaction—is missing. |
| Decision rationale | block | O2 changes two independent boundaries without criteria showing why they must move together. |
| Vision fit | pass | The direction remains local, Git-native, inspectable, resumable, and non-autonomous. |
| Scope control | block | “Supported” file wording and an open file-class set do not preserve the stated universal `docs/changes/` goal. |
| Architecture awareness | pass | The proposal correctly identifies domain, application, repository, transaction, compatibility, observability, and workflow boundaries. |
| Testability | block | CI authorship detection is not testable from equivalent final bytes under the stated trust model. |
| Risk honesty | concern | Transaction and compatibility risks are strong; inability to prove local writer provenance is not resolved. |
| Rollout realism | concern | Compatibility gates are sensible, but enforcement cannot activate until its meaning and complete writer coverage are closed. |
| Readiness for spec | changes-requested | Resolve CLIARCH-PR1 through CLIARCH-PR3 and perform a same-stage rereview. |

## Scope Preservation Review

- Scope-preservation result: changes-requested. Most initial goals are explicitly classified, but the universal `docs/changes/` write boundary is narrowed to an undefined “supported” subset without a complete destination or explicit justification.

## Recommended Proposal Edits

- Replace writer-provenance enforcement claims with a selected and technically provable integrity boundary, or explicitly add the trusted mechanism required for provenance.
- Add a closed change-local artifact-family applicability table distinguishing durable governed writes, reads, and CLI-owned transient files.
- Add and evaluate the modular-single-file alternative before retaining or splitting multi-file semantic publication.
- Define “mandatory” as a support and governance contract separately from what repository-only CI can detect.
- Keep the current semantic-author, workflow-route, pure-domain, compatibility, token-friendly output, and Git-native decisions; they are well supported.

## Recommendation

- Recommendation: changes-requested. Retain the modular CLI direction, resolve the three proposal-level decisions, and run a new isolated proposal review. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: the scope budget is present and mostly well classified, but it leaves the universal governed-write target and the relationship between modularization and multi-file publication unresolved
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-28-governed-repository-cli-architecture-review-recording/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record and `review-resolution.md#proposal-review-r1`
