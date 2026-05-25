# Adopter-Facing Vision and README Principle Rewrite

## Status

accepted

## Problem

RigorLoop's internal principles are now clearer than the public story built
around them.

The current five principles are directionally right:

```text
1. Everything as code.
2. Interpretability: AI work can be understood by real humans.
3. Resumption: tasks are stateless and do not depend on a specific agent.
4. Change Traceability Chain: review all changes in one feature clearly.
5. Learn stage: turn mistakes into durable experience that improves the project.
```

The adoption gap is that these are still written mostly in project-internal
vocabulary. A new adopter does not yet know what "learn stage," "resumption
follows," or "everything as code" means. The public framing should state every
principle as a user benefit first, then explain the mechanism.

The current framing answers:

```text
How does RigorLoop think about itself?
```

The README and `VISION.md` need to answer:

```text
Why should I care?
What problem does this solve for me?
Why would I try this instead of just using an AI coding agent directly?
```

The stronger public story is:

```text
AI coding agents produce output fast, but the reasoning often vanishes.
RigorLoop turns that work into traceable, resumable, reviewable artifacts in Git.
```

The durable why is AI-assisted work that remains traceable, resumable, and
trustworthy because every important decision is a durable artifact.

## Goals

- Rewrite RigorLoop's vision and README positioning so the five principles read
  as adopter benefits, not internal mechanisms.
- Make traceability the central public differentiator.
- Make the first README screen pass a three-second comprehension test.
- Keep `VISION.md` as the source of truth for the durable why.
- Keep README vision content synchronized with `VISION.md` rather than creating
  a second source of truth.
- Add a visual traceability chain showing the lifecycle from idea to PR.
- Add or link to a concrete worked example that shows an artifact chain and
  resumption path.
- Preserve honest when-to-use and when-not-to-use guidance as a trust signal.
- Avoid changing runtime behavior, workflow semantics, skill behavior, CLI
  behavior, validators, release process, or adapter output.

## Non-goals

- Do not redefine RigorLoop's workflow semantics.
- Do not change lifecycle stage order.
- Do not change skill behavior or generated skill content.
- Do not change CLI commands in this proposal.
- Do not change release process, npm package behavior, or adapter packaging.
- Do not turn the README into a full manual.
- Do not make "learn stage" sound like the product is unstable or
  self-experimenting.
- Do not replace precise workflow docs with marketing copy.
- Do not create independent README vision text that can drift from `VISION.md`.
- Do not claim broad adoption or maturity that is not supported by evidence.
- Do not use vanity metrics as proof of value.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's existing artifact-first vision by making
it understandable to external adopters. The goal is not to make the project
more promotional. The goal is to make its actual value visible:

```text
AI-assisted work that can be inspected, resumed, reviewed, and improved because
the important decisions live as durable artifacts in the repository.
```

The proposal is falsified if:

```text
- the README becomes more attractive but less accurate;
- VISION.md and README vision text drift;
- the principles remain understandable only to existing maintainers;
- traceability is buried under mechanism language;
- the learn stage sounds like churn rather than reliability improvement;
- a cold reader cannot explain what RigorLoop does and why it matters;
- the rewrite removes honest when-not-to-use guidance.
```

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Everything as code | in scope | Adopter-facing principle set; README principles; `VISION.md` principles |
| Interpretability | in scope | Adopter-facing principle set; README principles; `VISION.md` principles |
| Resumption and statelessness | in scope | Adopter-facing principle set; README principles; `VISION.md` principles |
| Change traceability chain | in scope | Central differentiator; README diagram; `VISION.md` durable value |
| Learn stage | in scope | Reliability-oriented learn framing |
| Improve adoption | in scope | README first-screen contract and cold-read evidence |
| Preserve rigor | in scope | Non-goals, falsifier, verification strategy |
| Avoid internal-only wording | in scope | Problem, recommended direction, principle rewrite |
| Keep source-of-truth discipline | in scope | `VISION.md` and README synchronization contract |
| Avoid runtime, CLI, skill, adapter, validator, or release behavior changes | in scope | Non-goals, behavior-preservation proof, verification strategy |
| Full launch package, docs site, screenshots, GIFs, and GitHub metadata | out of scope | Non-goals and first-slice boundary |

## Scope Budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| `VISION.md` benefit-first rewrite | first-slice candidate | It owns the durable why and prevents README drift. |
| README first-screen rewrite | first-slice candidate | It is the adopter-facing landing surface. |
| README Mermaid traceability diagram | first-slice candidate | It makes the central differentiator visible and reviewable. |
| README principles section | first-slice candidate | It preserves the five principles while reframing them as benefits. |
| Worked example link or placeholder follow-up | first-slice candidate | It supports adoption without inventing unsupported examples. |
| Vision / README sync proof | first-slice candidate | It proves the README has not forked `VISION.md`. |
| Cold-read review evidence | first-slice candidate | It validates first-screen comprehension. |
| Behavior-preservation proof | first-slice candidate | It demonstrates no runtime or generated-output behavior changed. |
| Command-source proof | same-slice dependency | Required only if the first slice changes or introduces exact README command examples. |
| Mermaid diagram caption | same-slice dependency | Required so the full lifecycle diagram is framed as the recommended complete-delivery chain, not mandatory ceremony for every task. |
| Worked-example follow-up trigger | same-slice dependency | Required when no public-friendly real example is selected, so example curation is scheduled rather than open-ended. |
| Generated README vision block automation | deferable follow-up | Manual sync proof is enough for the first slice; automation can wait for repeated drift. |
| Public worked-example curation | deferable follow-up | A real example should be selected only after public suitability is checked. |
| GIF, screenshots, docs site, launch campaign, GitHub metadata, npm metadata | out of scope | These are broader adoption or distribution work, not part of this source-of-truth rewrite. |

## Context

The current root `VISION.md` already positions RigorLoop as a rigorous workflow
for AI coding agents that turns product intent into traceable artifacts, tests,
validation evidence, and review decisions. The proposal keeps that direction
but changes the public ordering and vocabulary so the user benefit is visible
before the mechanism.

The principle mapping for this proposal is:

| Internal principle | Adopter-facing benefit |
| --- | --- |
| Everything as code | Every decision, spec, and review is a version-controlled file, not a lost chat log. |
| Interpretability | A human can understand what the AI did and why. |
| Resumption / statelessness | Any agent can pick up the task because state lives in the repo. |
| Change Traceability Chain | A feature can be traced from proposal to PR, with proof along the way. |
| Learn stage | Mistakes become durable lessons, so the workflow gets more reliable. |

The vision should lead with the problem, not the mechanism. Traceability and
interpretability should be foregrounded, while code-as-artifacts,
statelessness, and learn remain supporting mechanisms.

For the README, the same direction calls for a first-two-line hook, a visual
traceability chain, a concrete worked example, and a "why it is built this way"
section placed after the hook, quick start, and visual.

## Options Considered

### Option 1: Keep the five principles as-is

Pros:

- No rewrite risk.
- Preserves the maintainer's internal terminology.
- Minimal work.

Cons:

- Still reads like an internal project manifesto.
- Does not answer a new adopter's "why should I care?" question.
- Leaves the strongest differentiator, traceability, under-leveraged.

### Option 2: Add the five principles as a README bullet list

Pros:

- Easy to implement.
- Keeps all principles visible.
- Low risk of changing meaning.

Cons:

- Still leads with mechanisms.
- Can read like a feature list.
- Does not create a sharp public positioning spine.

### Option 3: Rewrite only the README first screen

Pros:

- Highest immediate landing-page impact.
- Lower governance surface than changing `VISION.md`.
- Faster to review.

Cons:

- Creates drift risk if README vision diverges from `VISION.md`.
- Does not fix the durable source-of-truth framing.
- Leaves the internal/external voice mismatch in the vision artifact.

### Option 4: Rewrite `VISION.md` and synchronize README vision and first screen

Pros:

- Fixes the durable why and public landing page together.
- Preserves source-of-truth discipline.
- Lets README reflect the vision instead of inventing a parallel one.
- Makes traceability the stable differentiator.

Cons:

- Touches a governed artifact.
- Requires careful review to avoid changing product direction unintentionally.

### Option 5: Full adoption rewrite across vision, README, docs site, launch posts, examples, and screenshots

Pros:

- Largest adoption impact.
- Could create a complete public launch package.

Cons:

- Too broad for one slice.
- Risks mixing positioning, docs, website, and promotion.
- Harder to review for accuracy.

## Recommended Direction

Choose Option 4.

Rewrite the durable vision first, then synchronize the README's public hook and
vision block from that source.

The governing rule:

```text
VISION.md owns the durable why.
README presents the adopter-facing landing page.
The README vision section must reflect VISION.md, not fork it.
```

The README should still include a concise "why it is built this way" section
with the five principles, but only after the hook, quick start, visual
traceability chain, and worked example. The principles should link out for depth
rather than dominate the first screen.

The proposed adopter-facing principle set is:

### Reviewable artifacts, not lost chat logs

Internal phrase:

```text
Everything as code.
```

Adopter-facing phrasing:

```text
Every decision, proposal, spec, test plan, review, and validation result is a
file in your repository: version-controlled, diffable, and reviewable in a PR.
Nothing important has to live only in a chat log.
```

### Human-understandable AI work

Internal phrase:

```text
Interpretability.
```

Adopter-facing phrasing:

```text
You can understand what the AI changed and why. RigorLoop keeps the reasoning,
evidence, and review decisions in plain artifacts so a human remains in control.
```

### Resumable work across sessions and agents

Internal phrase:

```text
Resumption / stateless tasks.
```

Adopter-facing phrasing:

```text
Pick up the work with any agent, any time. The task state lives in Git, not in
one model session, so work survives interruptions, handoffs, and agent changes.
```

### Traceable feature chain

Internal phrase:

```text
Change Traceability Chain.
```

Adopter-facing phrasing:

```text
Trace a feature end to end: proposal -> spec -> tests -> plan -> implementation
-> review -> verification -> PR. Months later, you can see why the change was
made and what proved it correct.
```

This should be the central differentiator.

### Lessons become durable improvements

Internal phrase:

```text
Learn stage.
```

Adopter-facing phrasing:

```text
When something goes wrong, the lesson becomes a durable artifact. The workflow
gets more reliable over time because mistakes become reusable guidance, not
one-off memories.
```

The public framing should avoid making learn sound like unstable product
self-experimentation. The safer framing is reliability for the adopter.

## Expected Behavior Changes

- `VISION.md` leads with the adopter problem and RigorLoop's durable
  differentiator.
- README first screen answers what RigorLoop is, who it is for, and why it
  matters.
- The five principles are reframed as user benefits.
- Traceability becomes the public positioning spine.
- README includes a visual traceability chain.
- The traceability chain visual is captioned as the recommended full path for
  complete AI-assisted delivery, while acknowledging that individual skills can
  be used in isolation when the full lifecycle is not needed.
- README links to a worked example or records a follow-up if no example is
  ready. If deferred, the follow-up should have an owner, trigger, and candidate
  selection path rather than remaining open-ended.
- README vision section and `VISION.md` remain synchronized.
- No runtime behavior changes.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| `VISION.md` | Update durable vision language and principles. |
| `README.md` | Update first screen, workflow diagram, principles framing, and example link. |
| README vision markers | Must remain synchronized with `VISION.md` if the marker model is active. |
| `docs/changes/<change-id>/vision-readme-sync-proof.md` | New evidence artifact recommended. |
| `docs/changes/<change-id>/cold-read-review.md` | New evidence artifact recommended. |
| `docs/changes/<change-id>/behavior-preservation.md` | New evidence artifact recommended. |
| CLI / runtime | No change. |
| Skills / adapters | No change. |
| Validators | Optional check for vision-marker synchronization only if such a validator already exists. |
| Release process | No change. |

## README Ownership Boundary

This proposal separates README vision-marker content from README landing-page
prose.

README vision marker block:

- Source of truth: `VISION.md`.
- Update only through the existing vision-marker synchronization contract.
- Do not hand-edit generated marker content.
- If markers are missing, malformed, nested, or duplicated, block marker sync
  until the owner approves marker repair or a documented sync exception.

README landing-page prose outside the marker block:

- Source of truth: `README.md`, constrained by `VISION.md`.
- May include hook, quick explanation, Mermaid diagram, worked-example link,
  and "why it is built this way" section.
- Must not contradict `VISION.md`.
- Must not claim unsupported CLI, workflow, skill, release, or adoption
  behavior.

The implementation should record which README sections are marker-owned and
which are landing-page prose in `vision-readme-sync-proof.md`.

## First Action / Command-Source Boundary

This proposal may improve the README hook and point readers toward the Quick
Start, but it does not independently change CLI command contracts.

If exact commands are shown in the rewritten first screen, implementation
should prove they match the current approved CLI contract and current package
docs. If target-native init work is still in progress, use command-neutral
first-action wording such as:

```text
Start with the Quick Start below.
```

or link to the Quick Start section without rewriting command examples.

Command freshness and version pinning are owned by the public discovery /
CLI-command adoption surface work unless this plan explicitly takes that proof
on.

## Testing and Verification Strategy

| Check ID | What is verified |
| --- | --- |
| `VRP-001` | `VISION.md` leads with the adopter problem, not internal mechanism. |
| `VRP-002` | `VISION.md` names traceability and reviewability as the differentiator. |
| `VRP-003` | The five principles are expressed as adopter benefits. |
| `VRP-004` | README first two lines explain what RigorLoop is, who it is for, and why it matters. |
| `VRP-005` | README includes a traceability chain visual. |
| `VRP-006` | README principles section appears below hook, quick start, and visual. |
| `VRP-007` | README includes or links to a concrete worked example, or records a follow-up if none is ready. |
| `VRP-008` | README keeps when-to-use and when-not-to-use guidance. |
| `VRP-009` | README vision content is synchronized with `VISION.md`. |
| `VRP-010` | Cold-read reviewer can explain the value proposition and first action. |
| `VRP-011` | No unsupported CLI, workflow, release, skill, or adoption claim is introduced. |
| `VRP-012` | No runtime, skill, adapter, validator, or release artifact behavior changes. |
| `VRP-013` | README marker ownership is identified and generated marker content is not hand-edited. |
| `VRP-014` | README landing-page prose outside the marker is checked against `VISION.md` for consistency. |
| `VRP-015` | Missing, malformed, nested, or duplicated README vision markers block marker sync unless owner-approved handling is recorded. |
| `VRP-016` | Exact CLI command examples are changed only with command-source proof, or avoided in favor of a Quick Start link. |
| `VRP-017` | Cold-read evidence may identify the first action as "go to Quick Start" when exact command text is out of scope. |
| `VRP-018` | README changes do not conflict with the approved target-native init / Quick Start command source. |
| `VRP-019` | The traceability diagram caption frames the chain as the recommended complete-delivery path and names isolated skill use as possible. |
| `VRP-020` | If no worked example is selected, the follow-up has a concrete trigger, owner, and candidate selection path. |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-VRP-001` | `VISION.md` states RigorLoop's adopter-facing problem before its mechanisms. |
| `AC-VRP-002` | `VISION.md` presents traceability, resumability, and reviewability as the durable value proposition. |
| `AC-VRP-003` | The five principles are reframed as user benefits. |
| `AC-VRP-004` | README first screen explains what RigorLoop is, who it is for, why it matters, and how to try it or learn more. |
| `AC-VRP-005` | README includes a traceability chain visual. |
| `AC-VRP-006` | README keeps detailed mechanisms below the hook, quick start, and visual. |
| `AC-VRP-007` | README keeps honest when-to-use and when-not-to-use guidance. |
| `AC-VRP-008` | README vision content is synchronized with `VISION.md`. |
| `AC-VRP-009` | Cold-read evidence confirms a new reader can identify the value proposition, target user, first action, and traceability chain. |
| `AC-VRP-010` | Learn-stage wording is framed as adopter reliability improvement, not project churn. |
| `AC-VRP-011` | No unsupported runtime, CLI, release, workflow, skill, or adoption claim is introduced. |
| `AC-VRP-012` | No runtime, skill, adapter, validator, release, or generated artifact behavior changes occur. |
| `AC-VRP-013` | The implementation identifies the README vision marker block, if present, and does not hand-edit generated marker content. |
| `AC-VRP-014` | README landing-page prose outside the marker block is checked against `VISION.md` for consistency. |
| `AC-VRP-015` | Missing, malformed, nested, or duplicated README vision markers block marker sync unless owner-approved handling is recorded. |
| `AC-VRP-016` | The proposal does not introduce or change exact CLI command examples unless command-source proof is recorded. |
| `AC-VRP-017` | Cold-read evidence may identify "go to Quick Start" as the first action when exact command text is owned by another change. |
| `AC-VRP-018` | README changes do not conflict with the approved target-native init / Quick Start command source. |
| `AC-VRP-019` | The Mermaid traceability diagram includes a caption that says the chain is recommended for complete AI-assisted delivery and that individual skills can be used in isolation. |
| `AC-VRP-020` | If the first slice cannot link a clean public-friendly real example, it records a scheduled worked-example follow-up with owner, trigger, and candidate criteria. |

Suggested validation commands:

```bash
git diff --check --
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path VISION.md \
  --path README.md \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/plans/<change-id>.md \
  --path docs/plan.md
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
```

If a README or link checker exists, run it. If not, record manual link
validation in the cold-read evidence.

The first implementation slice should also create:

```text
docs/changes/<change-id>/vision-readme-sync-proof.md
docs/changes/<change-id>/cold-read-review.md
docs/changes/<change-id>/behavior-preservation.md
```

The sync proof should identify `VISION.md` as the source of truth, identify the
README marker range or anchor, distinguish marker-owned content from
landing-page prose, and compare claims for traceable AI work, resumable work,
reviewable artifacts, and learn / reliability.

The cold-read evidence should ask a reviewer who has not worked on this
proposal what RigorLoop is, who it is for, why someone would use it, what the
first action is, what the traceability chain is, what "learn" means here, and
whether anything sounds unsupported, overbroad, or unstable. When exact command
text is out of scope, "go to Quick Start" is an acceptable first-action answer.

The behavior-preservation proof should record that runtime CLI behavior, skill
behavior, adapter output, release process, and generated artifacts are unchanged
because those surfaces are not touched.

The recommended traceability diagram caption is:

```text
This is the recommended full chain for complete AI-assisted delivery. Individual
skills can also be used in isolation when the project does not need the full
lifecycle.
```

If no real worked example is selected in the first slice, the change should
record a follow-up similar to:

```text
Worked example follow-up required: no public-friendly real example selected in
this slice. Candidate selection should prioritize a short, public-safe change
that shows proposal/spec/test/plan/review/verify/PR evidence and demonstrates
resumption from artifacts.
```

## Rollout and Rollback

Rollout:

1. Approve this proposal.
2. Revise `VISION.md` with benefit-first vision framing.
3. Update README hook and first-screen content.
4. Add Mermaid workflow diagram.
5. Add "Why RigorLoop is built this way" using adopter-facing principle names.
6. Add or link a worked example, or record a follow-up if no suitable example is
   ready.
7. Preserve when-to-use and when-not-to-use guidance.
8. Record sync proof, cold-read review, and behavior-preservation proof.
9. Run lifecycle, metadata, link, and patch-hygiene validation.
10. Review as a positioning and documentation change.

Rollback:

- Revert README first-screen wording if it overpromises or confuses cold
  readers.
- Revert `VISION.md` wording if it changes project direction rather than
  clarifying it.
- Remove or revise the diagram if it implies false automation or a mandatory
  full lifecycle for all uses.
- Keep any sync-proof artifact if it remains useful for diagnosing drift.
- Do not roll back runtime artifacts because none should change.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Vision becomes marketing copy | Keep falsifier, when-not-to-use guidance, and source-of-truth discipline. |
| README and `VISION.md` drift | Add sync proof and, if available, marker validation. |
| Traceability diagram implies mandatory full lifecycle | Caption it as recommended for complete delivery; isolated skills remain possible. |
| Learn stage sounds like instability | Frame it as mistakes becoming reliability improvements. |
| First screen becomes too long | Keep the hook short; move principles lower. |
| Worked example becomes stale or permanently deferred | Link to a maintained example or record a scheduled follow-up with owner, trigger, and candidate criteria instead of fabricating one. |
| Unsupported CLI claims appear | Use command-neutral first-action wording unless command-source proof is recorded. |
| The rewrite changes product direction | Proposal review should check vision semantics before implementation. |

## Open Questions

- None blocking after proposal-review revisions.

Resolved during proposal review:

- This should remain standalone, or an explicitly isolated sub-slice, because
  `VISION.md` is a source-of-truth artifact with stronger governance than README
  presentation.
- README should use Mermaid first because it is diffable, reviewable, and lower
  maintenance than a static image.
- The worked example should use an existing real change only if it is clean,
  public-friendly, and not too internally noisy. If no example passes that bar,
  record a follow-up instead of inventing a synthetic example.
- README marker content should use the existing marker / synchronization
  mechanism if it already applies. README prose outside the marker should be
  manually updated and proven consistent with `VISION.md`.
- Final principle names should prefer "Reviewable artifacts,"
  "Human-understandable AI work," "Resumable across sessions and agents,"
  "Traceable from idea to PR," and "Durable lessons."

Questions for plan to answer explicitly:

- Determine whether `README.md` already has a valid `VISION.md` marker-sync
  mechanism or whether any marker work would be new scope.
- Identify a genuinely cold reader for cold-read evidence; a reviewer who has
  seen this proposal or discussion is not valid proof for that check.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-25 | Lead with adopter benefit, not mechanism. | Internal principle names do not answer "why should I care?" | Keep five internal bullets as primary copy. |
| 2026-05-25 | Make traceability the public spine. | The proposal-to-PR chain is RigorLoop's strongest differentiator. | Treat all five principles as equal feature bullets. |
| 2026-05-25 | Keep `VISION.md` as source of truth. | README vision text must not fork durable project vision. | Rewrite README only. |
| 2026-05-25 | Use Mermaid first. | Diffable, reviewable, low maintenance. | GIF or image first. |
| 2026-05-25 | Frame learn as reliability. | "Optimizes itself" can sound like churn to adopters. | Internal learn-stage framing in public hook. |
| 2026-05-25 | Separate README marker-owned content from landing-page prose. | Generated marker sync and normal README prose have different owners and constraints. | Treat all README positioning text as generated vision content. |
| 2026-05-25 | Keep exact command changes out of scope unless command-source proof is recorded. | Quick Start and target-native init command shape are owned by related public discovery / CLI-command work. | Independently rewrite README command examples in this proposal. |
| 2026-05-25 | Treat proposal-review observations as plan obligations. | Review approved the proposal with non-blocking observations about diagram caption and worked-example deferral. | Leave the observations as chat-only advice. |

## Next Artifacts

Planned next artifacts:

```text
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Use a spec amendment only if the existing `VISION.md` / README marker
synchronization contract is missing or ambiguous.

Recommended route:

```text
proposal-review -> plan -> plan-review -> implementation -> code-review -> verify -> pr
```

## Follow-on Artifacts

Proposal review: approved with observations on 2026-05-25. Durable review
record: `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/reviews/proposal-review-r1.md`.

Execution plan: `docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`.

Potential follow-on proposals after this slice:

- Generated README vision block from `VISION.md`.
- Public worked-example curation.
- README GIF or CLI demo after target-native init stabilizes.
- GitHub repository metadata update if not already handled.
- Off-platform launch post after landing-page cold-read review passes.

## Readiness

Ready for `plan`.

Core invariant:

```text
RigorLoop's public story should lead with the value a user gets:

AI-assisted work that remains traceable, resumable, and reviewable after the
chat ends.

The mechanisms -- everything as code, stateless resumption, traceability chain,
and learn stage -- matter because they create that adopter benefit. The vision
and README must say that plainly without changing runtime behavior or forking
the project's source of truth.
```
