---
name: research
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Reduce a bounded, decision-relevant factual uncertainty with attributable evidence and explicit confidence. Use when platform behavior, compatibility, standards, policies, prices, performance, security, scale, or operational facts could materially change a known decision; use explore instead when the option space itself is unclear.
argument-hint: [decision, bounded question, assumption, dependency, or owning stage]
---

# Decision-relevant research

Research answers: What decision-relevant facts can be established with sufficient confidence, and what remains uncertain?

## Workflow role

- role_name: research
- stage: support
- upstream: an explicitly invoked supported decision with one or more bounded factual questions
- downstream: the named decision owner, or evidence acquisition when a responsible answer is not yet possible
- summary: Reduce material uncertainty without approving or mutating the decision it supports.

Research owns only its standalone supporting artifact. It does not become a lifecycle stage or acquire the decision owner's authority.

## Purpose

Define bounded research questions, inspect suitable evidence, distinguish evidence from inference and assumption, report source quality and confidence, and explain only the implications relevant to the supported decision. Stop when more investigation is unlikely to change that decision.

## When to use

Use Research when a material decision depends on uncertain platform or dependency behavior, compatibility or migration constraints, a current standard, API, policy, price, or external rule, or a performance, security, scale, or operational claim that needs evidence. Use it for bounded questions emitted by Explore.

An explicit invocation creates or explicitly revises one standalone artifact. A small local fact check inside another stage is not a Research invocation and creates no Research-completion claim.

## When not to use

Do not use Research for open-ended option generation or questions that cannot materially affect the supported decision. Skip it when repository evidence already settles the fact with sufficient confidence. Use Explore when the material uncertainty is which directions exist. Do not use Research to bypass a missing specification, silently expand scope, approve a product direction, or mutate another stage's artifact or lifecycle state.

## Inputs to read

Identify the supported decision, intended decision owner when known, bounded questions, acceptable evidence types, evidence that could change the result, and a material stopping condition before collecting evidence.

When the answer may already be governed or observable locally, inspect the smallest relevant repository evidence first: approved artifacts, manifests, lockfiles, code, schemas, generated output, tests, CI, or deployment configuration. Use external sources only when current or niche facts require them, and preserve applicable citation and source-use rules.

## Stop conditions

Stop before creating or revising the artifact when the target is unsafe, ambiguous, escaped, colliding, or unrelated; required mapped resources are missing or unreadable; the supported decision or questions are not bounded; necessary evidence or authority is unavailable; scope would expand materially; or owner judgment is required.

Stop investigation when further evidence is unlikely to change the supported decision. Qualify confidence and remaining uncertainty when responsible partial support is possible. Stop without a completion claim when unavailable or unreliable evidence prevents a responsible answer. Route an approved-decision contradiction to that decision's owner without editing the approved artifact.

## Operating sequence

1. State the supported decision, its owner when known, and bounded questions.
2. Define acceptable evidence, what could change the answer, and when to stop.
3. Resolve one absent repository-relative target at `docs/research/YYYY-MM-DD-slug.md`, or one explicitly selected exact existing research artifact for material revision. Never overwrite an unrelated artifact.
4. Load the common support rules and research skeleton.
5. Inspect repository evidence first when appropriate. Load the source method when source authority, freshness, local-versus-external selection, or citation needs more guidance.
6. Use suitable authoritative and fresh external sources only when local evidence is insufficient. Load the experiment method only when a benchmark, experiment, or non-trivial confidence assessment can materially answer the question.
7. Record evidence and source quality separately from inference and assumption. State confidence in each material finding and in the bounded answer.
8. Explain implications for the supported decision, remaining uncertainty, and the recommended handoff. A bounded answer is advice to the owner, not approval of the broader direction.

## Evidence and confidence rules

Every established factual finding needs an attributable basis. Evaluate source authority, relevance, and freshness in proportion to volatility and decision impact. State inference as inference and assumption as assumption. Do not promote missing, stale, or conflicting evidence into a fact. Record secrets, credentials, unnecessary private raw input, and machine-local absolute paths nowhere in the artifact.

## Outputs

Produce one concise Git-tracked research artifact containing the supported decision, bounded questions, inputs examined, evidence and source quality, findings, inference and assumptions, confidence, decision implications, remaining uncertainty, and recommended handoff. An explicit Research invocation never silently collapses into an inline section of another artifact.

## Handoff

Return the artifact to the named Proposal, Design, Delivery, Implementation, Verify, or other decision owner. The owner may adopt, reject, qualify, or request more evidence through its own artifact and normal review. Stop for evidence acquisition when a responsible answer is unavailable; stop for owner judgment when the remaining question is no longer factual.

## Claims this skill must not make

Do not claim that evidence approves a proposal, design, delivery package, implementation, verification result, or product direction; that another stage's artifact or lifecycle state changed; that unsourced inference is established fact; or that unavailable evidence proves absence. Research completion proves only that its supporting artifact was produced or explicitly revised.

## Resource map

- READ `references/discovery-support.md` for every explicit invocation before creating or revising the supporting artifact.
- READ `references/source-and-repository-method.md` when source selection, freshness, repository-first investigation, external evidence, or citation needs more than the core sequence.
- READ `references/experiment-and-confidence-method.md` when a benchmark, experiment, or non-trivial confidence assessment can materially answer a bounded question.
- COPY `assets/research-skeleton.md` when producing every explicit Research artifact. Fill every applicable structure and remove unused prompts; do not emit unfilled placeholders.

## Output skeleton

```md
COPY `assets/research-skeleton.md` and fill <supported decision>, <bounded questions>, <examined inputs>, <evidence and source quality>, <findings and confidence>, <implications>, <remaining uncertainty>, and <handoff>. Do not emit unfilled placeholders.
```

## Expected output

Return the research artifact path, bounded answer, confidence, material implications, remaining uncertainty, recommended next owner, and the explicit limitation that the owning decision has not been approved or mutated.
