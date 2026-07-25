# Capability-Preserving Progressive Disclosure for Published Skills

## Status

draft

## Problem

RigorLoop already treats published skills as portable operating documentation
for capable agents and supports progressive disclosure through packaged
`references/`, `scripts/`, and `assets/`.

The current published surface nevertheless remains expensive to load across a
long lifecycle.
The 24 canonical `SKILL.md` files contain about 45,500 words and 6,100 lines.
The largest individual bodies are approximately:

| Skill | Words | Lines |
| --- | ---: | ---: |
| `code-review` | 4,068 | 486 |
| `workflow` | 4,017 | 474 |
| `implement` | 3,121 | 377 |

Nineteen skills repeat the same evidence-collection block.
Several skills also repeat routing, procedure, output, handoff, and claim
language across frontmatter, quick guides, body sections, inline examples, and
packaged assets.

This cost matters because a complete RigorLoop change can load many specialized
skills sequentially in one conversation.
Each skill may be individually readable while the cumulative harness becomes
overconstrained, repetitive, and harder for an agent to reconcile.

Anthropic reports that it removed more than 80 percent of Claude Code's system
prompt for its Claude 5 generation models without measurable loss on its coding
evaluations.
Its broader lesson is to let capable models exercise judgment, design expressive
interfaces instead of teaching tools through repeated examples, use progressive
disclosure, avoid repeating tool instructions across context layers, and keep
skills lightweight.
That result is useful evidence, but it is model- and harness-specific and does
not establish an 80-percent reduction target for RigorLoop.

RigorLoop cannot safely optimize only for fewer words.
Published skills own lifecycle gates, formal review recording, authorization
boundaries, stop conditions, validation obligations, and limits on what an
agent may claim.
Removing or hiding those capabilities could make the harness shorter while
making delivered changes less trustworthy.

The problem is therefore:

```text
How can RigorLoop reduce common-path and cumulative loaded context while proving
that every behavior-significant capability remains available at the point of
use?
```

## Goals

- Reduce common-path context loaded by published lifecycle skills.
- Preserve routing, procedure, judgment, safety, recording, validation,
  stop-condition, claim-boundary, and handoff capabilities.
- Give every behavior-significant instruction one clear owning context layer.
- Prefer expressive resource and tool interfaces over repeated tutorials and
  examples.
- Load detailed rubrics, variants, and edge-case matrices only when their
  trigger applies.
- Measure scenario-specific loaded context rather than only `SKILL.md` size.
- Detect duplicated, conflicting, unreachable, or always-loaded deferred
  content before rollout.
- Preserve portability and self-containment across supported adapter packages.
- Establish a focused `code-review` reference pilot before considering broader
  skill-family changes.
- Extend the existing skill contract instead of creating a second normative
  published-skill contract.

## Non-goals

- Do not use Anthropic's 80-percent result as a RigorLoop acceptance threshold.
- Do not rewrite all 24 skills in one change.
- Do not weaken formal review recording, destructive-action safeguards,
  authorization boundaries, claim ownership, validation, or fail-closed stops.
- Do not move rules into references merely to improve `SKILL.md` size metrics.
- Do not hide workflow policy in assets or examples.
- Do not make a resource optional when every valid invocation needs it.
- Do not replace specs, workflow state, validators, or typed tool interfaces
  with skill prose.
- Do not introduce model-specific behavior that makes the published skills
  depend on Claude 5.
- Do not create a broad semantic-prose scoring gate.
- Do not introduce build-time partials or a repository-wide shared-reference
  mechanism in the first slice.
- Do not modify `workflow`, `implement`, or `verify` in the first pilot.
- Do not overlap implementation with an active change that already modifies
  `code-review` unless the later plan records a safe ownership boundary.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted changes traceable, resumable, and
reviewable without becoming ceremony that teams ignore.
Capability-preserving context reduction supports that vision when it makes the
operating harness easier for agents to follow while retaining the evidence and
claim boundaries that humans rely on.

The proposal would conflict with the vision if token savings were allowed to
outrank review quality, durable evidence, portability, or cross-session
resumability.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Apply the new context-engineering lesson to RigorLoop's published skills | in scope | Problem, Context, Recommended Direction |
| Improve published skills through progressive disclosure | in scope | Goals, Layer Ownership Model |
| Preserve existing skill capabilities | in scope | Capability Preservation Contract |
| Follow repository best practices rather than copying a vendor target | in scope | Non-goals, Testing and Verification Strategy |
| Change every published skill immediately | rejected option | Non-goals, Options Considered |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Published-skill context audit | core to this proposal | A baseline is required before content moves. |
| Capability ledger and layer classification | core to this proposal | This is the preservation mechanism. |
| Scenario-specific loaded-context measurement | core to this proposal | Flat file size can reward ineffective deferral. |
| `code-review` reference pilot | first-slice candidate | It is the largest deliberative skill and an already-recorded reference candidate. |
| `code-review` assets and resource-map alignment | same-slice dependency | The pilot must remove body/asset duplication without changing output shape. |
| Skill and adapter validation updates | same-slice dependency | Deferred resources must remain packaged, mapped, and current. |
| Behavior-parity and transcript evaluation | same-slice dependency | Structural and token checks cannot prove capability preservation. |
| `workflow` context reduction | separate proposal | It is an orchestration surface and may overlap the active automation initiative. |
| `implement` and `verify` reduction | deferable follow-up | Expand only after the deliberative pilot is proven. |
| Shared cross-skill reference or build-time partial system | separate proposal | It changes package and source ownership beyond one skill. |
| Model-specific prompt variants | out of scope | Published skills must remain portable. |

## Context

### Existing contract

The accepted Published Skill Design Contract already establishes that:

- skills are portable operating documentation for capable agents;
- frontmatter `description` is the routing surface;
- bodies contain the normal execution path;
- hard constraints are reserved for consequential boundaries;
- long examples and optional detail should move to packaged resources;
- changed skills require routing and behavior-preservation evidence.

The accepted assets-first pilot proved structural progressive disclosure for
`plan`.
It also identified deliberative skills such as `code-review`, `verify`, and
review-family skills as future `references/` candidates.

The resource-integrity architecture pilot subsequently established explicit
`COPY`, `READ`, and `RUN` resource classes, canonical-to-installed parity, and
the rule that runtime fallback cannot make a broken package valid.

This proposal is a follow-on to those accepted directions.
It does not replace them.

### External context-engineering lesson

The July 24, 2026 Anthropic article, [The new rules of context engineering for
Claude 5 generation
models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models),
argues for:

- judgment over broad preference rules;
- interfaces over repeated tool examples;
- progressive disclosure over putting everything upfront;
- simple tool descriptions over duplicated instructions;
- richer references and rubrics when detailed context is needed;
- lightweight skills containing team- or product-specific operating knowledge.

RigorLoop should adopt the model-neutral parts of this lesson.
Its published packages serve Codex, Claude Code, opencode, and future adapters,
so capability claims must be demonstrated on RigorLoop's own artifacts and
evaluation corpus.

### Current context layers

Published skill behavior is currently spread across:

```text
frontmatter description
SKILL.md body
packaged references
packaged assets
packaged scripts
project-local workflow and governance artifacts
repository-owned runtime tools and validators
```

The main design risk is not the existence of multiple layers.
It is unclear or duplicated ownership between them.

## Options Considered

### Option 1: Keep the existing skills unchanged

Pros:

- No capability-regression risk.
- No migration or packaging work.
- Existing validation remains sufficient.

Cons:

- Cumulative lifecycle context remains high.
- Repeated and conflicting guidance remains harder to detect.
- The existing progressive-disclosure contract is underused for deliberative
  skills.
- Context cost grows as new workflow features are added.

### Option 2: Apply an aggressive universal deletion target

Delete or compress a fixed percentage of every `SKILL.md`, using Anthropic's
reported reduction as the benchmark.

Pros:

- Simple measurable target.
- Large immediate reduction.
- Forces authors to challenge old guidance.

Cons:

- Confuses one vendor's harness result with a portable product requirement.
- Rewards removing difficult safety and lifecycle rules.
- Does not prove that deferred content is available when needed.
- Treats simple and high-risk skills as equivalent.

Rejected.

### Option 3: Move most skill bodies into references

Keep a thin router in each `SKILL.md` and place procedure, rubrics, and edge
cases in packaged references.

Pros:

- Very small skill bodies.
- Clear progressive-disclosure appearance.
- Existing packaging already supports references.

Cons:

- If every invocation reads the reference, loaded context does not improve.
- Essential stop or claim boundaries may be skipped.
- File splitting can create duplicate or contradictory owners.
- A missing load trigger can silently remove capability.

Rejected as a general rule.

### Option 4: Capability-preserving layered pilot

Inventory behavior-significant capability, assign each item to one appropriate
context layer, use scenario-specific load triggers, and prove parity before
rolling out one deliberative-skill pilot.

Pros:

- Reduces context without treating size as the only quality signal.
- Makes ownership and load conditions explicit.
- Builds on existing resource-integrity support.
- Supports deterministic checks plus realistic behavior evaluation.
- Limits regression risk to one skill.

Cons:

- Requires a detailed baseline and preservation ledger.
- Some behavior proof remains review- or transcript-based.
- The first pilot may reveal that less content is safely deferrable than
  expected.

Recommended.

### Option 5: Centralize all lifecycle guidance in the workflow skill

Pros:

- One global policy location.
- Less duplication across stage skills.
- Easier global updates.

Cons:

- Makes stage skills less self-contained.
- Loads unrelated lifecycle policy.
- Recreates a monolithic context surface.
- Conflicts with specialized stage ownership.

Rejected.

## Recommended Direction

Choose Option 4.

Amend the existing published-skill contract with a
capability-preserving progressive-disclosure method, then pilot it on
`code-review`.

The method should have five parts:

1. baseline the skill's capabilities and representative invocation scenarios;
2. classify each behavior-significant instruction by its correct context layer;
3. remove duplication and introduce conditional resource loads;
4. prove resource integrity, capability parity, and scenario-specific context
   improvement;
5. stop the rollout if quality or capability evidence regresses.

### Capability Preservation Contract

For each changed skill, create a capability ledger covering:

| Capability class | Examples |
| --- | --- |
| Routing | positive triggers, near misses, competing skills |
| Procedure | normal execution sequence and escalation points |
| Judgment | rubrics, decision matrices, severity or applicability rules |
| Authority and safety | permitted actions, destructive boundaries, trust sources |
| Recording and output | required artifacts, fields, formats, durable evidence |
| Validation | required checks, proof sources, failure interpretation |
| Stop conditions | missing evidence, ambiguity, stale state, invalid package |
| Claims and handoff | what may be claimed and the next owning stage |

Every baseline capability should receive one disposition:

```text
preserved-inline
preserved-reference
preserved-asset
preserved-script-or-tool
removed-duplicate
removed-obsolete
behavior-change-requires-separate-approval
```

`removed-duplicate` should identify the remaining owner.
`removed-obsolete` should cite the higher-priority artifact or current behavior
that proves it is obsolete.
An unclassified behavior-significant instruction should block rollout.

### Layer Ownership Model

| Layer | Owns | Does not own |
| --- | --- | --- |
| `description` | capability, triggers, important near-miss routing | execution procedure |
| `SKILL.md` | normal path, mandatory inputs, load triggers, stop/authority/claim boundaries, compact output and handoff contract | long variants, repeated examples, full output templates |
| `references/` | conditionally needed rubrics, edge matrices, variants, recovery guidance | hidden routing or universally required safety rules |
| `assets/` | copy-and-fill output structures | workflow policy or judgment rules |
| `scripts/` and tool interfaces | deterministic transformation, validation, enums, state transitions | discretionary product or review judgment |
| project artifacts | change-specific requirements, state, evidence, architecture, and plans | generic skill package behavior |

The primary invariant is:

```text
One behavior-significant rule has one authoritative owner and an explicit path
to load or execute it when its scenario applies.
```

### Constraint classification

Skill authors should distinguish:

| Constraint class | Treatment |
| --- | --- |
| Security, privacy, destructive action, authorization | hard inline boundary |
| Formal review recording, claim ownership, schema, required validation | hard inline boundary or deterministic interface |
| Project-specific convention | defer to project-local evidence |
| Judgment heuristic | concise guidance with rationale |
| Generic coding or writing preference | remove unless evidence shows a recurring RigorLoop-specific failure |
| Rare variant or edge matrix | conditional reference |
| Repeated output structure | asset |
| Closed mechanical decision | script, schema, enum, or tool interface |

### `code-review` pilot boundary

The first slice should modify only:

```text
skills/code-review/SKILL.md
skills/code-review/references/
skills/code-review/assets/
skill/resource validation and fixtures needed for the pilot
adapter packaging and parity proof needed for changed resources
change-local capability and context evidence
```

The pilot should preserve inline:

- routing and workflow role;
- the compact independent-review procedure;
- minimum evidence and actual-diff requirement;
- formal review status and recording boundary;
- authority, stop, claim, and handoff boundaries;
- resource load conditions;
- compact result contract.

Candidate conditional references include:

- generated-document and artifact-placement guidance;
- planned-milestone and final-closeout variants;
- autoprogression review behavior;
- requirement-fidelity and named-edge proof rubrics;
- recovery and mixed-evidence decision matrices.

These are candidates, not predetermined moves.
The capability ledger and scenario analysis should decide whether each one is
actually conditional.

The existing material-finding and review-result assets should remain structural
output owners.
Inline templates that duplicate those assets should be removed or reduced to
compact resource instructions.

### Context measurement

Measure at least:

```text
metadata context
SKILL.md body context
resources loaded for the scenario
total scenario-loaded context
total packaged skill content
```

The pilot should use representative scenarios:

| Scenario | Expected conditional context |
| --- | --- |
| Isolated implementation diff review | core review procedure only |
| Planned non-final milestone review | milestone handoff guidance |
| Review of a finding correction | review-resolution and mixed-evidence guidance |
| Workflow-automated review | autoprogression review guidance |
| Final implementation review | final closeout guidance |
| Generated Markdown or governance diff | generated-document guidance |

Moving content to a reference that every scenario loads should not count as
common-path improvement.

## Expected Behavior Changes

- `code-review` loads a smaller common-path body.
- Detailed review guidance is loaded only when its documented trigger applies.
- The agent can locate every deferred capability through the Resource map.
- Output structures remain owned by packaged assets rather than duplicated
  inline templates.
- Formal review status, recording, safety, stop, claim, and handoff behavior
  remain unchanged.
- Skill and adapter validation report missing, stale, unmapped, or
  inappropriately always-loaded pilot resources.
- Maintainers receive scenario-level context measurements and behavior-parity
  results rather than one flat token number.
- No other published skill changes in the first implementation slice.

## Architecture Impact

The proposal reuses the existing packaged-resource architecture:

```text
canonical skills/
-> skill build
-> adapter package
-> installed skill and mapped resources
```

Expected affected components:

| Surface | Expected impact |
| --- | --- |
| `specs/skill-contract.md` | Add capability-ledger, layer-ownership, load-efficiency, and pilot rules. |
| `specs/skill-contract.test.md` | Add proof mapping for preservation and context measurement. |
| `skills/code-review/` | Split conditional judgment guidance into mapped references while preserving core behavior. |
| Skill validation | Check ledger coverage, mapped resources, load triggers, and prohibited duplicate owners where deterministic. |
| Token/context measurement | Measure scenario-loaded context, not only file size. |
| Adapter validation | Preserve raw-byte resource parity and clean-install availability. |
| Runtime workflow state | No intended change. |
| Workflow stage order | No change. |

An architecture assessment should occur after spec approval.
An architecture amendment is expected only if implementation introduces a new
shared-resource owner, context-loading runtime, or package boundary.

## Testing and Verification Strategy

### Deterministic proof

| Proof area | Expected evidence |
| --- | --- |
| Capability ledger completeness | Every behavior-significant baseline item has exactly one disposition and destination. |
| Resource integrity | Every mapped reference exists and survives canonical-to-installed parity. |
| Load contract | Every reference has a specific trigger and intended scenarios. |
| Duplicate ownership | Closed enums, full templates, and copied normative blocks do not acquire a second pilot owner. |
| Scenario context | Metadata, body, loaded resources, and total loaded context are measured per scenario. |
| Output parity | Existing result and material-finding assets retain required structure. |
| Adapter parity | Changed resources are present and current in every claimed adapter package. |
| Unknown values | New closed vocabularies fail closed with direct regression tests. |

### Behavior-parity corpus

Use representative historical review artifacts and fresh fixtures covering:

- clean review;
- changes requested;
- blocked and inconclusive outcomes;
- direct named-edge negative proof;
- milestone review and final closeout;
- review-resolution rerun;
- missing or stale governing evidence;
- automated review routing;
- generated or governance Markdown.

For every scenario, compare:

```text
review outcome
finding materiality and shape
recording behavior
required evidence
stop behavior
milestone or final handoff
claims withheld
resources loaded
```

### Forward evaluation

Use fresh-context transcript evaluation where available.
Give the evaluator the installed skill package and task artifact, not the
intended answer or suspected regression.

Evaluate:

- under-triggering and over-triggering;
- missing resource loads;
- unnecessary resource loads;
- ignored or over-applied instructions;
- review-finding recall and false positives;
- output and handoff parity.

Prompt fixtures and transcript review should not claim deterministic
model-selection proof unless an approved routing harness supplies that oracle.

### Improvement gate

Behavior parity outranks context reduction.

The spec should define a measurable pilot threshold using scenario-loaded
context.
A recommended starting point is:

```text
- at least 20 percent reduction in median scenario-loaded context;
- no scenario may load more context without a recorded capability reason;
- total packaged content growth above 10 percent blocks rollout;
- any regression in formal review, safety, validation, stop, claim, or handoff
  behavior blocks rollout.
```

The 20-percent value is a pilot forcing function, not a universal skill target.
Proposal review or spec work may revise it if baseline measurements show that a
different threshold better distinguishes meaningful improvement from file
shuffling.

## Rollout and Rollback

### Rollout

1. Review and accept this proposal.
2. Amend `specs/skill-contract.md`; do not create a competing skill contract.
3. Review the amended spec.
4. Assess whether existing package architecture is sufficient.
5. Create and review an execution plan and matching test spec.
6. Capture the current `code-review` capability ledger, scenario corpus, and
   context baseline before editing the skill.
7. Perform the single-skill reference pilot.
8. Run structural, resource-integrity, adapter, behavior-parity, transcript,
   and scenario-context proof.
9. Stop or revise the pilot if parity or improvement gates fail.
10. After verified closeout, decide through a separate proposal or explicit
    follow-on whether another skill family should adopt the pattern.

### Rollback

- Restore the prior `code-review` skill and resource layout together.
- Rebuild adapter packages from canonical source.
- Preserve the capability ledger and evaluation evidence.
- Keep generally valid validator improvements only when they continue to
  support flat skills and existing packaged resources.
- Do not leave a reference path in `SKILL.md` after removing its packaged file.
- Do not hand-copy resources into installed adapters as a durable rollback.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Token reduction hides capability loss. | Require a complete capability ledger and scenario behavior parity before rollout. |
| A reference is nominally conditional but always loaded. | Measure total scenario-loaded context and reject file-shuffling gains. |
| Critical safety or recording rules become optional. | Keep authority, safety, formal recording, stop, claim, and required validation boundaries inline. |
| Multiple files create contradictory owners. | Require one authoritative layer and exact disposition for every moved or removed instruction. |
| The pilot overfits Claude 5. | Use model-neutral contracts, adapter parity, and RigorLoop-specific behavior evidence. |
| Context metrics become a proxy for quality. | Make behavior parity blocking and context improvement secondary. |
| Review performance becomes less thorough. | Include material-finding recall, negative proof, stale evidence, and final handoff in the evaluation corpus. |
| References are missing from installed packages. | Reuse existing path, raw-byte parity, and clean-install checks. |
| A new semantic validator becomes brittle. | Keep static checks structural and use bounded transcript or human review for qualitative behavior. |
| The pilot overlaps active `code-review` work. | Start implementation only after the overlapping change settles or records a safe ownership boundary. |
| Shared duplication remains after one pilot. | Record it as follow-on evidence; do not introduce shared-resource architecture implicitly. |

## Open Questions

None block proposal review.

The spec should settle:

1. the exact capability-ledger schema and behavior-significant-item boundary;
2. the exact scenario corpus and weighting for the 20-percent pilot threshold;
3. which candidate `code-review` sections are truly conditional;
4. the deterministic boundary between duplicate-owner lint and qualitative
   review;
5. the available cross-model or cross-adapter transcript matrix for the pilot.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-25 | Extend the existing skill contract. | It already owns published-skill structure, progressive disclosure, and resources. | Create a second context-engineering spec. |
| 2026-07-25 | Optimize scenario-loaded context, not only body size. | File splitting does not help when every scenario loads the moved content. | Measure only `SKILL.md` words or tokens. |
| 2026-07-25 | Require a capability ledger. | Every behavior-significant instruction needs a reviewable disposition and owner. | Rely on prose claims of equivalent behavior. |
| 2026-07-25 | Keep consequential boundaries inline. | Safety, recording, validation, stop, claim, and authority rules cannot depend on optional discovery. | Move nearly all content to references. |
| 2026-07-25 | Pilot `code-review` only. | It is the largest deliberative skill, already uses assets, and was identified by prior work as a reference candidate. | Rewrite all skills; pilot `workflow`; reopen `plan`. |
| 2026-07-25 | Use a RigorLoop-specific improvement gate. | Anthropic's 80-percent result is not portable evidence for all models or skills. | Adopt 80 percent as a universal target. |
| 2026-07-25 | Defer shared-resource architecture. | A one-skill pilot can use existing package boundaries. | Introduce build-time partials or global shared references now. |

## Next Artifacts

```text
proposal-review
spec amendment: specs/skill-contract.md
spec-review
architecture assessment
plan
plan-review
test-spec amendment: specs/skill-contract.test.md
test-spec-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on Artifacts

None yet

## Readiness

Ready for `proposal-review`.

The proposal does not claim acceptance, spec readiness, implementation
readiness, behavior parity, or context improvement.
