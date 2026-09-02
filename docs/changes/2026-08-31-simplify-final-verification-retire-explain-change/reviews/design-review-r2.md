# Design Review R2: Sole Current V3 Contract and Historical Readability

Review ID: design-review-r2
Stage: design-review
Round: r2
Reviewer: Independent Codex design-review rereview context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-impact-aware-final-verification`
Reviewed artifact: design package `architecture`, `spec`, `adr-impact-aware-final-verification`
Review date: 2026-09-01
Package kind: design
Package members: architecture=docs/architecture/2026-08-31-impact-aware-final-verification.md, spec=specs/impact-aware-final-verification.md, adr-impact-aware-final-verification=docs/adr/ADR-20260831-impact-aware-final-verification.md
Upstream review ID: proposal-review-r1
Status: approved
Material findings: none
Correction targets: none
Recording status: recorded

## Result

- Skill: design-review
- Review status: approved
- Package members: architecture=`docs/architecture/2026-08-31-impact-aware-final-verification.md`, spec=`specs/impact-aware-final-verification.md`, adr-impact-aware-final-verification=`docs/adr/ADR-20260831-impact-aware-final-verification.md`
- Upstream review ID: proposal-review-r1
- Review ID and round: design-review-r2, r2
- Material findings: none
- Correction targets: none
- Recording status: recorded
- Settlement status: pending exact-package CLI settlement
- Open blockers: none in the revised Design package; open M4 implementation-review findings and stale Delivery authority remain separate downstream state
- Immediate next stage: workflow after successful package settlement; the amended plan requires independent Delivery Review before further implementation authority
- Claim limitations: approval grants authority only to this exact Design package and does not approve the amended plan, settle Delivery, authorize implementation, or claim verification, branch, PR, release, or deployment readiness

## Design coherence

The exact revised architecture, specification, and ADR form one coherent realization of the accepted proposal and the explicit simplicity decision that v3 is the sole current executable contract after activation. The specification owns the observable lifecycle, historical-read, evidence-applicability, failure, identity, activation, and PR-consumption outcomes. The architecture realizes those outcomes through a single v3 lifecycle interpreter, the approved Delivery verification map, impact classifier, applicability evaluator, freshness classes, always-current set, Verify-owned result, closed evidence tail, generated-package boundary, and atomic release cutover. The ADR records the durable single-current-contract, explanation ownership, evidence reuse, cache separation, bootstrap closeout, and recovery decisions.

Historical readability is separated from execution authority rather than implemented as a frozen compatibility graph. Completed v1/v2 artifacts and immutable release archives retain their historical content and producing context. Current tooling may identify a record as non-v3 history, but it cannot enter a legacy stage graph, consult a continuation allowlist, or grant lifecycle progression. Non-v3 progression, unknown contracts, contract-class mismatches, mixed packages, and active explain-change values in v3 fail closed before consistency interpretation. This satisfies FV-R4 through FV-R7 and INT-004 without carrying current v1/v2 checker branches.

The final-readiness design remains internally coherent. Verify starts from the approved Delivery allocation, classifies each relevant surface with conservative `unknown`, applies exactly one evidence decision and freshness class, runs every required current or fresh check, and emits the final explanation only inside a complete successful report. The `S -> R -> V` identity keeps the reviewed subject fixed, excludes product and governing drift from the Verify tail, and makes PR consume the exact registered evidence basis without self-referential commit identity.

## Bootstrap and recovery assessment

The package explicitly prevents self-stranding activation. The implementing change remains v2, completes through the last coherent v2 release package, and must be complete before the atomic v3 release cutover. Only after that closeout do new-change scaffolding and current lifecycle tooling accept v3 progression exclusively. Before the first v3 record, rollback restores the prior coherent v2 release; afterward recovery is forward through v3 and never reintroduces a legacy progression branch.

The amended plan direction is compatible with this design only in its stated candidate-versus-activation separation: M5 may assemble and review a v3-only source and publication candidate, while M6 performs this change's v2 closeout through the last coherent v2 package and public activation remains a separately authorized later action. Whether every M5/M6 dependency and command expresses that separation precisely belongs to the required new Delivery Review; this Design Review does not approve or settle the plan.

## Boundary assessment

All eight boundary-first dimensions remain classified exactly once. The compatibility boundary now partitions current v3 from historical non-v3 without enumerating executable legacy contracts. INT-004 composes lifecycle state, package composition, and compatibility so historical content remains readable while any progression attempt or mixed current package fails. The authority, recovery, temporal, composition, input, and environment boundaries continue to cover owner correction, conservative applicability, freshness precedence, closed evidence-tail identity, exact PR consumption, and external proof. Every example remains requirement-owned and illustrative; none creates a legacy execution path or new normative outcome.

## Proposal preservation and feasibility

The revised package preserves the accepted direction: retire standalone explain-change, generate rationale only after successful Verify, reduce unnecessary evidence execution, broaden on uncertainty, preserve explicit freshness, keep Verify read-only, maintain reverse traceability, retain historical records without migration, and make PR consume the exact Verify result. The sole-current-v3 decision simplifies current checkers and skills without weakening those safeguards.

Implementation is feasible without a current compatibility allowlist. A one-time preactivation completion check can run under the last coherent v2 package, historical releases preserve old interpretation context, and the activated source can use a generic non-v3 historical classification plus fail-closed progression rejection. Exact serialization, fixture selection, source-switch ordering, and release commands remain Delivery decisions.

## ADR assessment

The included ADR is necessary and agrees with the architecture and specification. Its rejection of maintained v1/v2 progression branches is scoped to current tooling after activation; it does not rewrite settled records or historical archives. Its supersession of the prior explanation tail and universal actual-run consequence remains bounded to v3 explanation ownership and affirmatively current impact-sensitive evidence. No additional ADR is required before Delivery Review.

## Validation performed

- `python scripts/validate-boundary-first.py --check` — passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-31-simplify-final-verification-retire-explain-change` — passed before recording R2.
- `git diff --check b3e0aba7^..b3e0aba7` — passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml` — blocked on stale Delivery initialization/review state and the two open M4 implementation-review findings; these are lifecycle reconciliation consequences, not Design package contradictions.
- Explicit-path artifact lifecycle validation reported the same lifecycle-state blockers and no package-content defect.

## Independence statement

This rereview did not author or edit the proposal, architecture, specification, ADR, plan, implementation, authoring evidence, review resolution, or workflow routing state. It writes only Design Review evidence, its review-log occurrence, and exact CLI request artifacts and settlement state.

## No-finding statement

No material finding was identified in the exact revised Design package. The package is coherent, bounded, feasible, proposal-preserving, and sufficiently explicit for a fresh Delivery Review of the amended plan.
