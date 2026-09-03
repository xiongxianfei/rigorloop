# Refine Explore and Research as Optional Discovery Skills

## Challenge

RigorLoop publishes separate `explore` and `research` skills, but their current boundaries and outputs do not make their distinct value obvious. Both can inspect existing artifacts, surface uncertainty, discuss risk, and recommend a next step, so developers may treat them as interchangeable or skip them because the extra procedure and artifact cost is unclear.

The current contracts reinforce that ambiguity. `explore` requires at least five predefined option types even when the real decision space is smaller, and it may place exploratory work beside or inside a proposal, blurring uncommitted option discovery with an approval-ready direction. `research` may either create a standalone artifact or collapse into another artifact, so explicit invocation does not guarantee independently inspectable evidence. Neither skill states a sufficiently clear common rule for how its conclusions support, but do not control, the lifecycle stage that owns the eventual decision.

## Goals

- Retain `explore` and `research` as separate published skills with immediately distinguishable responsibilities.
- Keep both skills optional and explicitly invoked rather than adding mandatory lifecycle stages or gates.
- Make an explicit invocation produce a concise, standalone, Git-tracked supporting artifact.
- Center `explore` on problem framing, proportional option discovery, decision criteria, and identification of questions that need evidence.
- Center `research` on bounded, sourced uncertainty reduction, confidence, decision implications, and remaining uncertainty.
- Prevent either skill from approving a direction, mutating another stage's owned contract, or progressing lifecycle state.
- Allow either skill to support Proposal, Design, Delivery, Implementation, Verify, or another identified decision owner.
- Give each artifact a clear handoff through which the owning stage may adopt, reject, or qualify its conclusions.
- Consolidate shared authority, artifact, and handoff conventions without merging divergent exploration with convergent research.
- Make routing clear enough to select `explore`, `research`, both, or neither without turning discovery into routine ceremony.
- Preserve useful evidence with proportional procedure and evaluate usefulness through decision quality and real use, not invocation volume alone.

## Scope and non-goals

The proposal covers these workstreams and boundaries:

| Workstream | Scope budget treatment | Boundary |
| --- | --- | --- |
| Distinct public responsibilities for `explore` and `research` | core to this proposal | `explore` expands materially different directions; `research` establishes decision-relevant facts with stated confidence. |
| Optional invocation and non-authoritative lifecycle role | core to this proposal | Neither skill becomes a mandatory stage, review gate, settlement owner, approval authority, or automatic progression mechanism. |
| Standalone Git-tracked artifacts for explicit invocations | core to this proposal | Exploration and research remain independently inspectable; incidental fact checks performed by another stage do not become Research invocations. |
| Proportional Explore option generation | core to this proposal | Generate enough materially distinct options to expose the real decision space; include status quo or deferral when credible, without a fixed quota or manufactured alternatives. |
| Bounded Research questions, evidence, confidence, and stopping | core to this proposal | Research distinguishes evidence, inference, and assumption and stops when more work is unlikely to change the supported decision. |
| Common discovery-support contract | same-slice dependency | Shared guidance covers topic, supported decision, owning stage or change when known, inputs, assumptions, uncertainty, authority, and recommended next owner. |
| Route selection guidance | same-slice dependency | Routing distinguishes option-space uncertainty from factual uncertainty and permits either, both in sequence, or neither. |
| Skill templates and conditionally loaded methods | separate implementation slice | Core skill files stay focused while detailed exploration and research methods move behind explicit triggers. |
| Governing specs, workflow guidance, validators, examples, and contributor docs | same-slice dependency | Every authoritative or user-facing surface affected by the public contract must agree at adoption. |
| Supported adapter generation and release artifacts | separate implementation slice | Generated output derives reproducibly from canonical `skills/` sources and follows the repository's current archive and manifest policy; generated skill bodies are not hand-edited into tracked source. |
| Post-adoption usefulness evaluation | deferable follow-up | After representative use exists, the owning product or Proposal decision should assess routing clarity, artifact usefulness, and avoidable overhead; increased invocation count alone is not success. |

This proposal does not merge the skills, add `explore-review` or `research-review`, create independent approval or settlement state, require either artifact before Proposal or Design, create a general knowledge base, require external research when repository evidence is sufficient, or impose fixed counts for options, sources, pages, or tokens. It does not redesign Proposal feasibility or the broader lifecycle.

Explore does not select an approved product direction, establish facts without evidence, write system requirements or detailed architecture, create an implementation plan, or progress lifecycle state. Research does not generate an open-ended option space, approve a broader proposal or design, expand scope silently, mutate specifications or architecture, collect evidence indefinitely, or present inference as established fact.

Exact template wording, conditional-reference decomposition, validation implementation, adapter-generation mechanics, rollout sequencing, and proof allocation belong to Design and Delivery. The post-adoption evaluation is intentionally deferred because useful invocation evidence cannot exist before the refined skills are used; it should be opened as a separately owned follow-up rather than hidden in implementation closeout.

## Governing principle

> Explore should expand the decision space, Research should reduce decision-relevant uncertainty, and the owning lifecycle stage should make the decision.

## Proposed direction

Keep `explore` and `research` as separate, optional supporting skills with one recognizable question each:

```text
Explore:  What materially different directions could we take?
Research: What decision-relevant facts are reliable enough to use?
```

Use `explore` when the problem, user value, scope, or available directions are insufficiently understood. It clarifies the decision, affected users or systems, facts, assumptions, and unknowns; challenges solution-biased framing; generates enough materially distinct options to expose the real decision space; identifies comparison criteria; and identifies questions that require Research. A credible status-quo or defer option should be included, but the skill must not manufacture weak alternatives to meet a quota. Its recommendation may name a leading option or next investigation for consideration, but must not claim approval.

An explicit Explore invocation creates a standalone artifact under `docs/explorations/YYYY-MM-DD-slug.md` by default. The artifact records the decision or problem, facts, assumptions and unknowns, options, criteria, direction-level comparison, questions requiring research, and recommended handoff.

Use `research` when a material decision depends on an uncertain fact. It identifies the supported decision, defines bounded questions and stopping conditions, examines repository evidence before external sources when appropriate, selects sources for authority and freshness, separates evidence from inference and assumption, states confidence, and explains decision implications and remaining uncertainty. It may recommend an answer to its bounded question, but that answer does not approve the broader direction.

An explicit Research invocation always creates a standalone artifact under `docs/research/YYYY-MM-DD-slug.md` by default rather than silently becoming an inline section elsewhere. The artifact records the supported decision, research questions, inputs and source quality, findings, confidence, implications, remaining uncertainty, and recommended handoff. Another stage may still perform a small local fact check without invoking the Research skill or creating a Research artifact.

Both artifact types share a discovery-support contract: identify the topic, supported decision, owning stage or change when known, inputs examined, important assumptions, remaining uncertainty, and recommended next owner; preserve the artifact in Git; distinguish established facts from inference and assumptions; stop when more work cannot materially affect the supported decision; do not silently change an approved upstream decision or edit another stage's artifact; and route contradictions to the owner of the affected decision. Shared mechanics should live in common guidance, while each skill retains its distinct reasoning method.

The owning stage gives conclusions lifecycle effect by adopting them into its own artifact and submitting them to its normal review. An exploration recommendation therefore becomes a proposed direction only when Proposal selects it, and a research finding becomes governed feasibility or design evidence only when the owning Proposal, Design, Delivery, Implementation, or Verify activity relies on it within that stage's authority.

Routing should select `explore` for unclear problems, premature solution framing, materially different possible directions, unsettled scope or value, difficult-to-reverse choices, or an owning stage blocked by an insufficiently understood option space. It should select `research` for uncertain platform or dependency behavior, compatibility or migration constraints, current standards, APIs, policies, prices or external rules, and material performance, security, scale, or operational claims. It should select both when exploration produces factual questions that could change the option comparison, and neither when the problem, direction, and relevant facts are already sufficiently clear.

The public skill packages should use progressive disclosure. Their core `SKILL.md` files retain purpose, authority, artifact outcome, stopping rules, and handoff conditions; conditional references hold detailed reframing, option-generation, source-quality, repository research, external research, experiment, and confidence-reporting methods. Canonical guidance, validation, documentation, examples, and supported adapter release outputs must adopt the refined contract coherently.

## Feasibility

**Assessment: feasible.** Direct inspection of the current authored skills confirms that their foundations are already distinct: `skills/explore/SKILL.md` focuses on problem framing and option generation, while `skills/research/SKILL.md` focuses on scoped evidence and assumption validation. The same inspection confirms the avoidable overlap and weight described above: Explore mandates five predefined options and permits proposal-adjacent or inline output; Research permits inline output; and current Route guidance distinguishes them only briefly.

The work is primarily a contract and package refinement across existing canonical skills, shared references and assets, routing guidance, governing specs, validation, documentation, and reproducible adapter outputs. No new lifecycle state, identity scheme, review stage, or CLI transition is required. The principal constraints are keeping all authoritative surfaces coherent, preserving canonical `skills/` ownership and release-archive rules, and defining adoption and handoff language that supports multiple stages without transferring their authority. These constraints require Design and Delivery work but present no blocker to entering Design.

## Impact and major trade-offs

Keeping two public skills preserves two packages with relatively infrequent use, but it also preserves the ability to invoke and inspect divergent option discovery separately from convergent evidence gathering. A shared supporting-artifact contract and progressive disclosure limit duplication without obscuring the different reasoning modes.

Standalone artifacts improve resumability, attribution, and independent inspection, at the cost of more repository documentation. Optional invocation, concise defaults, bounded stopping rules, and permission for stage-local fact checks constrain that cost.

Difficult decisions may require two invocations when Explore surfaces facts that Research must establish. That is an accepted cost when the decision genuinely needs separate option expansion and uncertainty reduction. Low usage remains acceptable when routing correctly reserves both skills for material uncertainty; the meaningful outcome is better-supported owner decisions with proportionate overhead.

## Decision requested

Approve refinement of `explore` and `research` as separate, optional published supporting skills: Explore owns proportional option-space expansion; Research owns bounded, sourced uncertainty reduction; explicit invocations create standalone Git-tracked artifacts in separate default locations; both share common authority and handoff conventions; Route selects one, both, or neither based on the uncertainty; and canonical guidance, templates, conditional references, validation, examples, and supported adapter release outputs are updated coherently.

Approval authorizes Architecture and Specification to define the exact artifact contracts, shared-reference boundary, progressive-disclosure triggers, routing behavior, compatibility and adoption expectations, and affected validation surfaces. It does not create lifecycle stages, review gates, settlement state, approval authority, automatic progression, exact template text, implementation sequencing, proof allocation, or release authority for either supporting skill.
