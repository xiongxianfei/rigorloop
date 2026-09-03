---
name: explore
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Expand a materially unclear problem or solution space into distinct directions before its decision owner commits. Use when framing, user value, scope, reversibility, or available options are unsettled; use research instead when the options are known and an uncertain fact is the blocker.
argument-hint: [problem, decision, idea, change, or owning stage]
---

# Option discovery

Explore answers: What materially different directions are available, and what would make each direction suitable or unsuitable?

## Workflow role

- role_name: explore
- stage: support
- upstream: an explicitly invoked problem or decision with material option-space uncertainty
- downstream: the named decision owner, or research for bounded factual questions before returning to that owner
- summary: Expand and compare the real decision space without approving a direction.

Explore owns only its standalone supporting artifact. It does not become a lifecycle stage or acquire the decision owner's authority.

## Purpose

Clarify the problem, challenge solution-biased framing, distinguish facts from assumptions and unknowns, generate enough materially distinct options to expose the real decision space, compare them against useful criteria, and give the owner an inspectable handoff.

## When to use

Use Explore when the real problem, affected users or systems, user value, scope, materially different directions, or reversibility is unsettled. Use it when a request assumes a solution too early or an owning stage cannot proceed because the option space is insufficiently understood.

An explicit invocation creates or explicitly revises one standalone artifact. Incidental option consideration inside another stage is not an Explore invocation and creates no Explore-completion claim.

## When not to use

Do not invoke Explore merely because a decision exists. Skip it when the problem, direction, and relevant facts are sufficiently clear. Use Research when the options are understood and a bounded uncertain fact is the material blocker. Do not use Explore to approve product direction, establish disputed facts, freeze requirements or architecture, create an implementation plan, or progress lifecycle state.

## Inputs to read

Identify the decision or problem, affected users, systems, and workflows, the intended decision owner when known, and the smallest relevant project evidence. Read governing or approved artifacts when the exploration may intersect an existing decision. Use targeted evidence first and expand only when missing context could change the option space.

Separate established facts supported by inspected inputs, assumptions that are useful but unproved, and unknowns that could change the comparison.

## Stop conditions

Stop before creating or revising the artifact when the target is unsafe, ambiguous, escaped, colliding, or unrelated; required mapped resources are missing or unreadable; the supported decision or owner is too ambiguous to produce a useful handoff; scope would expand materially; or owner judgment is required.

Stop option generation when enough materially distinct options expose the real decision space and another option would only restate an existing direction. Stop investigation when additional work is unlikely to affect the supported decision. Route an approved-decision contradiction to that decision's owner without editing the approved artifact.

## Operating sequence

1. State the problem or decision and the owner it supports when known.
2. Resolve one absent repository-relative target at `docs/explorations/YYYY-MM-DD-slug.md`, or one explicitly selected exact existing exploration for material revision. Never overwrite an unrelated artifact.
3. Load the common support rules and the exploration skeleton.
4. Identify affected users, systems, or workflows and separate facts, assumptions, and unknowns.
5. Challenge framing that assumes one solution. Generate enough materially distinct options to expose the real decision space.
6. Include status quo or deferral when credible, but do not manufacture weak alternatives. A small decision may need only the current behavior and one credible change.
7. Define useful decision criteria and compare directions at the level needed by the owner. Use the option methods only when reframing or deliberate divergence needs more guidance; use the high-impact method only for strategically broad or difficult-to-reverse decisions.
8. Identify bounded factual questions that could materially change the comparison and hand those questions to Research when invoked.
9. Record a leading option or next investigation only as advice for consideration, then hand the artifact to the decision owner.

## Proportional option rule

Generate enough materially distinct options to reveal genuine trade-offs. Do not require a fixed count or predefined taxonomy. Prefer two strong alternatives over quota filler. Include a status-quo or defer direction only when it is credible, and explain what would make each direction suitable or unsuitable.

## Outputs

Produce one concise Git-tracked exploration artifact containing the supported decision or problem, facts, assumptions, unknowns, options, criteria, comparison, questions requiring Research, remaining uncertainty, and recommended handoff. A recommendation may identify a leading option or next investigation, but it is not approval.

## Handoff

Return the artifact to the named Proposal, Design, Delivery, Implementation, Verify, or other decision owner. When comparison depends on material unanswered facts, hand bounded questions to Research and then return both support artifacts to the same owner. Stop without downstream mutation when no owner is known or an owner decision is required.

## Claims this skill must not make

Do not claim that a direction is approved, a disputed fact is established without evidence, feasibility is final, requirements or architecture are settled, implementation is planned, a lifecycle stage progressed, or an owning artifact changed. Explore completion proves only that its supporting artifact was produced or explicitly revised.

## Resource map

- READ `references/discovery-support.md` for every explicit invocation before creating or revising the supporting artifact.
- READ `references/option-discovery-methods.md` when solution-biased framing, weak differentiation, or deliberate option generation needs more than the core sequence.
- READ `references/high-impact-decision-method.md` when the decision is strategically broad, difficult to reverse, or warrants deeper stakeholder, failure, and reversibility analysis.
- COPY `assets/exploration-skeleton.md` when producing every explicit Explore artifact. Fill every applicable structure and remove unused prompts; do not emit unfilled placeholders.

## Output skeleton

```md
COPY `assets/exploration-skeleton.md` and fill <supported decision>, <examined inputs>, <facts, assumptions, and unknowns>, <options and criteria>, <comparison>, <research questions>, <remaining uncertainty>, and <handoff>. Do not emit unfilled placeholders.
```

## Expected output

Return the exploration artifact path, a compact option-space summary, material research questions, remaining uncertainty, the recommended next owner, and the explicit limitation that the owner has not yet approved a direction.
