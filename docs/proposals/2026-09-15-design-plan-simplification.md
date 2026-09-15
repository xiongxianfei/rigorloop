# Simplify Design and Plan authoring guidance

## Challenge

Authors need to understand what to produce, which authority applies and how to hand off a complete artifact. In the current [Plan entrypoint](../../skills/plan/SKILL.md), detailed recording construction precedes the purpose and invocation classification. Scope, outputs and handoff duties also recur across several sections. This creates an opportunity to reduce reading and interpretation work while preserving delivery rigor.

[Design](../../skills/design/SKILL.md) already places scope and its reconciliation procedure first and keeps governed recording in a conditional reference. Its remaining opportunity is narrower: clarify navigation between the core procedure, model and architecture guidance, and output expectations wherever their overlap causes unnecessary interpretation. These are source-inspection observations, not measured usability defects. The [completed inventory proposal](2026-09-15-skill-simplification.md) justified retaining Design and making only a small Plan cleanup; this round selects a deeper, bounded assessment rather than treating that outcome as a failure.

## Goals

- Make the core authoring task, required inputs, expected artifact and next handoff immediately understandable for both skills.
- Reduce repeated guidance and irrelevant procedural reading without weakening engineering decisions, acceptance intent, delivery allocation or evidence obligations.
- Keep conditional methods discoverable, complete and usable in standalone installed packages.
- Preserve the chain from Design through independent Design Review to Plan and independent Delivery Review.

## Scope and non-goals

| Work item | Treatment | Bound |
| --- | --- | --- |
| Simplify `design` and `plan` entrypoints and their selected local resources | core to this proposal | Assess both complete packages; make justified improvements and retain guidance where a change offers no clear benefit. |
| Reconcile their owning Designs, output assets and directly affected validation or packaging consumers | same-slice dependency | Preserve applicable obligations and package integrity; make only changes necessary for the selected authoring improvements. |
| Check compatibility with `design-review` and `delivery-review` | same-slice dependency | Assess actual author outputs against reviewer inputs; limit corrections to compatibility required by this scope. |
| Redesign other skill families or shared workflow policy | out of scope | The wider adoption responsibilities in [FU-015–018](../follow-ups.md) remain separate; this selects only Design/Plan authoring from FU-015. |
| Change document formats, review gates, authority, record operations or public invocation names | out of scope | Simplification preserves their current meaning and supported paths. |
| Require a separate project-use pilot, token benchmark or length quota | out of scope | Normal project use supplies subsequent feedback; this change adds no recurring experiment or reporting duty. |
| Publish a release or install into active user environments | out of scope | Package qualification does not authorize distribution or installation. |

## Governing principle

Make the required task easier to understand and perform while preserving every applicable obligation.

## Proposed direction

Organize each skill around its authoring responsibility: establish scope and authority, identify required inputs, perform the core work, produce a usable artifact and hand it to the correct independent reviewer. Keep essential selection rules and stops visible before dependent action. Place substantial conditional procedure behind explicit triggers where doing so improves the selected reading path; do not relocate compact unconditional rules merely to shorten an entrypoint.

Use the merged Implement/Code Review treatment as a reference, adapting it to each authoring skill. Design already follows much of this approach and may need only small improvements or justified retention. Plan is the stronger candidate for presentation changes. The [Skill Design](../design/skill/skill.md#presentation-and-preservation) limits the existing equivalent layout to Implement/Code Review; any new equivalent needs its own explicit owning Design decision and independent assessment.

Preserve the distinction between Design's required behavior, realization, decisions and acceptance intent, and Plan's safe sequencing, proof allocation, recovery and reviewable milestones. Preserve supported legacy authoring, portable and governed paths, missing-resource stops and Plan's narrowly authorized approved-work initialization. Keep assets structural and review judgments independent. Detailed factoring, layout decisions and verification allocation belong to Design and Delivery.

## Feasibility

Assessment: feasible within the existing architecture, with no known blocker to beginning Design after direction approval. [Design authoring](../design/skill/authoring/design.md) and [Plan authoring](../design/skill/authoring/plan.md) already separate their responsibilities and support conditional resources. Both packages have existing governed references and output structures; current skill and adapter validation provide established consumers to reconcile.

The main uncertainty is whether further changes to Design improve clarity, and which apparent Plan repetitions remain useful safeguards. Whole-package inspection and independent semantic assessment must settle that before removal. Moving text or passing structural checks alone cannot establish improvement. Necessary compatibility corrections remain in scope; a discovery requiring changed authority, formats or reviewer responsibilities returns to its owner for a separate direction decision.

## Decision requested

Approve this bounded direction for simplifying Design and Plan authoring, including necessary consumer compatibility and justified retention. Submit it to independent Proposal Review, then reconcile the affected Designs and delivery allocation. This proposal requests no broader family adoption, separate usage pilot, implementation approval or publication authority.
