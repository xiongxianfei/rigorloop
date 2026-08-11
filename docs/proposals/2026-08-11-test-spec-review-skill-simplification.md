<!-- Template: proposal-skeleton-v1; Skill: proposal -->

# Test-Spec-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml`

## Problem

The published `test-spec-review` skill currently puts universal proof-quality review, formal lifecycle settlement, artifact discovery and recording, boundary-first procedure, status routing, and repeated result structure into one 359-line, 2,722-word `SKILL.md`.
An isolated advisory review therefore loads formal change-record and review-log procedure that it may not use, while ordinary test-spec reviews load detailed boundary guidance even when the governed feature does not activate that method.

The package already owns structural result and material-finding assets and maps two shared boundary-first references.
The main file nevertheless repeats or disperses several contracts across its workflow role, settlement, quick guide, purpose and usage, artifact placement, routing, rules, stops, isolation and recording, output skeleton, and expected-output sections.
The proof reference is also mapped behind a broad proof-completeness condition that is effectively part of every review rather than an explicit boundary-first activation condition.

The problem is not excessive review rigor.
The problem is duplicated rule ownership and conditional procedure in the common path, which makes the skill harder to scan and easier to apply inconsistently.

## Goals

- Make an ordinary isolated test-spec review materially shorter and easier to execute correctly.
- Keep `SKILL.md` self-sufficient for safe invocation classification, proof-quality judgment, material findings, statuses, stops, claim boundaries, and bounded handoff.
- Separate formal lifecycle review settlement from isolated advisory review without changing either authority model.
- Give boundary-first resources an exact, evidence-based activation predicate rather than loading them from conversational wording or every generic proof-map check.
- Give each behaviorally significant rule one explicit owner and destination.
- Use the existing assets as the sole copy-and-fill owners of result and finding structure while keeping policy outside the assets.
- Preserve requirement, edge-case, milestone, command, fixture, manual-proof, staleness, review-recording, and implementation-handoff semantics.
- Preserve deterministic canonical, generated, packed, and installed package resources.
- Measure loaded content by invocation assembly and report total package size separately, so relocation is not described as deletion.

## Non-goals

- Weakening proof-map coverage, negative-path testing, fixture determinism, command classification, manual-proof requirements, or review independence.
- Changing the closed review status, next-stage, implementation-handoff, or recording vocabularies established by `specs/test-spec-review-gate.md`.
- Changing lifecycle stage order, `change.yaml` schema, review-resolution ownership, workflow routing, test-spec authoring ownership, or implementation authorization.
- Making `test-spec-review` author or revise the test specification it reviews.
- Moving universal safety, evidence truthfulness, material-finding, status, or handoff rules behind a conditional reference.
- Changing the shared boundary-first method or proof resources in this initiative.
- Creating a cross-review-family policy reference, executable reviewer, scheduler, state store, model grader, or target-agent runtime harness.
- Adding a permanent line, word, byte, token, or prose-quality validator.
- Optimizing another skill in the same change.

## Vision fit

fits the current vision

The change reduces common-path ceremony while preserving explicit proof, durable formal review evidence, deterministic packaging, and safe lifecycle handoff.

## Context

The current authored package measures:

| Surface | Lines | Words | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| `skills/test-spec-review/SKILL.md` | 359 | 2,722 | 19,768 |
| Boundary-first method reference | 110 | 857 | 6,346 |
| Boundary-first proof reference | 41 | 356 | 2,305 |
| Result and finding assets | 39 | 187 | 1,412 |
| Total package | 549 | 4,122 | 29,831 |

The current contract has two independent behavioral axes:

1. an invocation is either an isolated advisory review or a formal lifecycle review with durable settlement duties; and
2. the reviewed feature either activates the governed boundary-first proof method or it does not.

Those axes should control loaded procedure.
They should not change universal review rigor or review status meanings.

The published-skill architecture already supports `SKILL.md` plus explicitly mapped references and assets, resource containment, raw-byte parity, generated and installed packaging, and fail-safe behavior when a required resource is unavailable.
The new reference remains owned by `test-spec-review`; it does not become a separate lifecycle owner.

### Initial intent preservation

| Initial user goal | Treatment | Where recorded |
| --- | --- | --- |
| Optimize `test-spec-review` next | in scope | Goals; Recommended Direction |
| Identify the best simplification solution | in scope | Options Considered; Decision Log |
| Start a new branch | in scope | Owning change record and branch history |
| Create a governed proposal | in scope | This artifact |
| Perform formal proposal review | in scope | Readiness and owning change record |

### Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal `SKILL.md` | core | This is the primary usability improvement. |
| Add one formal-settlement reference | core | Formal recording and settlement have one real activation boundary. |
| Preserve and precisely trigger both boundary-first references | same-slice dependency | They remain governed proof resources for applicable features. |
| Keep existing result and finding assets structural | same-slice dependency | Duplicate output layouts should have one owner. |
| Semantic and literal preservation evidence | same-slice dependency | Simplification must neither lose policy nor freeze incidental prose tests. |
| Canonical-to-installed package parity | same-slice dependency | The new mapped resource is published content. |
| Cross-review-family abstraction | out of scope | It would create coupling beyond this package. |
| Runtime reviewer or agent journey | out of scope | Packaged guidance does not require model-behavior testing. |

## Options Considered

### O0: keep the current package

This has no migration cost, but every invocation retains irrelevant formal procedure and repeated rule ownership remains unresolved.

### O1: edit and deduplicate only within `SKILL.md`

This can reduce repeated prose and is the smallest package change.
It cannot prevent isolated advisory reviews from loading formal settlement mechanics, so it only partially addresses the context problem.

### O2: extract only formal lifecycle settlement

This improves isolated review while leaving orientation, routing, stop, output, and boundary-first duplication in the main file.
It also leaves the current boundary resource trigger too broad.

### O3: compact universal skill plus one formal-settlement reference

Deduplicate the universal contract inline, move formal review recording and settlement procedure to one mapped conditional reference, retain the shared boundary resources behind an exact applicability trigger, and use existing assets as the only structural output templates.
This is the recommended direction.

### O4: add separate references for commands, fixtures, manual proof, staleness, and routing

This could minimize individual loads, but all reviews need those proof semantics.
Fragmentation would create more triggers and greater omission risk without a corresponding authority boundary.

### O5: replace the prose review with an executable or model-graded reviewer

An executable checker can validate some schemas, but it cannot replace semantic proof-map review.
This option adds runtime and compatibility scope unrelated to simplifying the published skill.

## Recommended Direction

Choose O3.

The expected final package is:

```text
skills/test-spec-review/
├── SKILL.md
├── references/
│   ├── boundary-first-method-v1.md
│   ├── boundary-first-proof-v1.md
│   └── formal-test-spec-review-settlement.md
└── assets/
    ├── review-result-skeleton.md
    └── material-finding.md
```

### Invocation classification

Use two independent predicates:

| Predicate | Required evidence |
| --- | --- |
| `formal_review_context` | A formal lifecycle invocation resolves exactly one active test-spec artifact, its owning change record, current authoring evidence, and a lifecycle state that requires `test-spec-review`. |
| `boundary_first_context` | Governing requirements or current proof-map evidence activate boundary-first-v1, including an applicable capability whose boundary, interaction, or proof applicability must be classified. |

Conversational wording alone establishes neither predicate.
An isolated review remains isolated even when the repository happens to contain an active change.
A formal request with missing, stale, ambiguous, mismatched, or non-current target evidence stops before review settlement.

Boundary-first applicability is determined from the governing feature contract and the reviewed proof map, not merely from the presence or absence of `BND-*`, `INT-*`, or `PRF-*` text.
When a potentially applicable capability cannot be classified from authoritative evidence, the reviewer stops or records a material upstream gap rather than silently treating the method as inapplicable.

### Loaded-resource assemblies

| Assembly | Formal review | Boundary-first | Loaded procedure |
| --- | ---: | ---: | --- |
| `TSR0-isolated` | no | no | `SKILL.md`; assets only when the caller requests a durable advisory record |
| `TSR0B-isolated-boundary` | no | yes | `SKILL.md` plus both boundary-first references; assets only for requested recording |
| `TSR1-formal` | yes | no | `SKILL.md`, formal-settlement reference, and result asset |
| `TSR1B-formal-boundary` | yes | yes | `SKILL.md`, formal-settlement reference, both boundary-first references, and result asset |

The material-finding asset is additionally copied once for each material finding in any recorded review.
No-material reviews do not copy an empty finding block.
Unknown or contradictory predicate combinations stop rather than guessing an assembly.

### Universal `SKILL.md` ownership

The compact main file remains sufficient for every isolated review and owns:

| Inline contract | Reason |
| --- | --- |
| Purpose, trigger, workflow role, and near-miss routing | Required before any reference is selected. |
| Formal versus isolated and boundary-first classification | Determines procedure and authority. |
| Input authority, target identity, and evidence precedence | Universal to every verdict. |
| Compact four-question boundary scan and exact resource triggers | Applicability must be classified before optional guidance loads. |
| Proof-map adequacy | Every review judges requirement, negative, milestone, command, fixture, and manual-proof coverage. |
| Command and evidence truthfulness | Configured, executed, manual, skipped, pending, stale, and unknown proof are never interchangeable. |
| Review dimensions and material-finding threshold | Universal review rigor cannot depend on formal mode. |
| Closed statuses, stages, handoff values, and deterministic routing | Every result must have one bounded meaning. |
| Staleness, universal stops, isolation, and claim boundaries | Safety applies before optional procedure. |
| Formal recording obligation and ownership boundary | Formal reviews must know that recording is required even if detailed mechanics are conditional. |
| Compact output semantics and asset applicability | The skill decides what structures apply; assets do not own policy. |

Universal proof rules remain inline, including:

- every normative requirement and acceptance criterion has adequate positive or negative proof;
- edge cases and failure paths are explicit rather than inferred from happy-path tests;
- tests map to executable milestones and name their validation command or bounded manual proof;
- command scope, prerequisites, environment assumptions, expected result, and evidence class are truthful;
- fixtures are deterministic enough to reproduce the intended boundary;
- manual proof identifies actor, action, environment, expected observation, and durable evidence;
- missing, stale, circular, conflicting, or insufficient evidence cannot support approval; and
- substantive test-spec edits make prior approval stale and require rereview.

### Formal settlement reference ownership

`references/formal-test-spec-review-settlement.md` owns only formal lifecycle procedure:

- locating and validating the owning change record and current test-spec artifact entry;
- checking that authoring evidence is current and that the test-spec is in a reviewable lifecycle state;
- choosing and creating the detailed review record or lightweight clean receipt;
- registering material findings in `review-log.md` and requiring `review-resolution.md` when findings exist;
- applying the proposal-independent review round, artifact ID, outcome, record path, and settlement fields;
- retry and conflict handling for concurrent or stale review evidence;
- settling only the test-spec artifact entry and matching review evidence under reviewer authority; and
- reporting blocked recording without claiming that an unrecorded formal review passed.

The reference does not own proof adequacy, materiality, status meaning, downstream authorization, universal stops, or lifecycle routing.
Those remain inline or with the existing workflow owner.
The reviewer does not revise the test spec, update workflow routing, or authorize implementation independently of the closed status-to-handoff contract.

### Boundary-first resources

The existing boundary resources remain unchanged and retain their governed ownership:

- `boundary-first-method-v1.md` supplies the detailed boundary and interaction classification method; and
- `boundary-first-proof-v1.md` supplies the proof-map completeness method for applicable boundary records.

When `boundary_first_context` is true, both references load once in their documented order.
When it is false, neither loads.
The compact inline scan remains sufficient to decide applicability safely but is not sufficient to reconstruct the detailed method when a required resource is unavailable.

### Structural assets

The result asset owns labels and layout for one recorded review result.
The finding asset owns labels and layout for one material finding.

The assets do not define:

- when recording is required;
- what a status or severity means;
- when implementation handoff is allowed;
- which fields or groups apply to isolated versus formal review; or
- how lifecycle settlement works.

Inapplicable optional sections are omitted, and unfilled placeholders are forbidden.
The main file and formal reference own applicability and policy.

### Resource ownership and conflict rule

| Contract | Owner |
| --- | --- |
| Universal review and proof semantics | `SKILL.md` |
| Formal lifecycle recording and settlement mechanics | `formal-test-spec-review-settlement.md` |
| Detailed boundary classification | Existing boundary-first method reference |
| Detailed boundary proof completeness | Existing boundary-first proof reference |
| Result labels and layout | Existing result asset |
| Material-finding labels and layout | Existing finding asset |
| Workflow routing and lifecycle continuation | `workflow`, not this package |

A conditional reference may specialize procedure for its activation context.
It may not override an inline universal rule or another resource's owned contract.
Any contradiction among `SKILL.md` and mapped resources is a package defect and stops the dependent action.

### Missing-resource behavior

| Situation | Required behavior |
| --- | --- |
| Isolated ordinary review and no conditional resource applies | Continue from `SKILL.md`. |
| Formal review and settlement reference is missing or unreadable | Stop before formal recording or lifecycle settlement. |
| Boundary-first context and either governed boundary reference is missing or unreadable | Stop before the boundary-dependent proof verdict. |
| Formal recorded result asset is missing | Stop before writing a partial formal result. |
| A material finding must be recorded and the finding asset is missing | Stop before recording an incomplete finding. |
| Installed resources have mixed versions | Treat as a package-integrity blocker; do not combine procedures. |
| A conditional trigger is false | Do not load that resource and do not treat its absence as a blocker. |

The shortened common path must not reconstruct missing conditional procedure from memory.

### Semantic and literal preservation

Implementation creates two change-local inventories.

`docs/changes/2026-08-11-test-spec-review-skill-simplification/test-spec-review-rule-disposition.yaml` gives every behaviorally significant current rule exactly one disposition:

```text
retained-inline
retained-formal-reference
retained-boundary-reference
asset-owned
removed-duplicate
removed-obsolete-with-approved-contract-change
```

Each entry records source locations, behavior, governing requirement, applicable assemblies, destination, and preservation proof.
No rule may disappear without a disposition.

`docs/changes/2026-08-11-test-spec-review-skill-simplification/test-spec-review-literal-compatibility.yaml` classifies exact headings, phrases, capitalization, paths, and vocabulary consumers separately:

```text
normative-contract
parser-or-package-contract
test-only-incidental
obsolete
```

Normative literals remain exact unless their governing contract changes.
Parser or package literals are preserved or migrated with every consumer atomically.
Incidental tests are updated rather than becoming prose-policy owners.

### Measurement convention

For each loaded-resource assembly, use canonical authored files, normalize line endings to LF, count each unique resource once, and concatenate in documented load order.
Record UTF-8 bytes, Unicode whitespace-separated words, file paths, and file identities for:

- `SKILL.md`;
- each valid loaded assembly;
- each conditional reference and asset; and
- the total authored package.

Words and bytes are primary portable measurements.
A token estimate is optional only when an existing repository-owned, version-pinned implementation supports the exact assembly; do not add a tokenizer dependency for this change.

A 30–40 percent reduction in `SKILL.md` words is a planning target, not a normative semantic gate.
Acceptance requires complete rule disposition, one owner for each duplicate cluster, material ordinary-path reduction, honest total-package accounting, and no behavioral loss.

## Expected Behavior Changes

- An isolated ordinary review loads a shorter `SKILL.md` and no formal-settlement or boundary-first procedure.
- A formal ordinary review loads the same universal review contract plus formal settlement procedure and the result asset.
- Boundary-first reviews load both existing detailed boundary resources; non-boundary reviews do not.
- Formal and isolated reviews use the same proof-quality, finding, status, stop, and claim semantics.
- Repeated quick-guide, routing, stop, and output wording has one prose or asset owner.
- Missing required resources fail safely instead of producing a partial verdict or record.
- Formal review still records durable evidence and settles only the test-spec artifact entry; isolated review remains advisory and does not authorize implementation.

## Architecture Impact

The expected assessment result is `architecture-not-required` if the current architecture already defines a published skill as canonical `SKILL.md` plus mapped references and assets with deterministic derived packaging.

The change introduces no new runtime, persistent state, dependency, service, scheduler, selector, lifecycle owner, or package-ownership model.
The new reference remains governed by `test-spec-review`.

A bounded architecture documentation update is required only if an existing diagram, table, or package example incorrectly depicts `skills/test-spec-review/` as flat or says it has no conditional resources.
If such an update is required, this change owns the architecture artifact entry in its `change.yaml` and the matching assessment or documentation update.
An ADR is warranted only if implementation would change the normative published-skill package model or assign independent policy ownership to a reference; this proposal rejects both changes.

## Testing and Verification Strategy

Acceptance uses three proof classes only.

### Deterministic structural proof

Reuse or extend existing owners to validate:

- frontmatter, required normalized headings, closed vocabularies, and fail-closed unknown values;
- resource-map syntax, load verbs, path containment, mapped-resource existence, and placeholder absence;
- canonical, generated, archive, manifest, and installed resource parity;
- asset applicability and absence of unfilled placeholders; and
- no forbidden deterministic readiness or handoff claims.

### Static contract fixtures

Change-local fixtures cover at least:

- isolated ordinary approval and isolated material findings;
- formal approval, changes-requested, blocked, and inconclusive outcomes;
- formal review with missing, stale, ambiguous, or mismatched change evidence;
- exact status, next-stage, and implementation-handoff mappings, including unknown-value failure;
- stale approval after substantive test-spec revision;
- command, fixture, manual-proof, and negative-case insufficiency;
- ordinary review not loading boundary resources;
- applicable boundary review loading both resources exactly once;
- ambiguous boundary applicability stopping or producing an upstream material gap;
- missing formal, boundary, result, and finding resources;
- formal versus isolated recording and settlement authority; and
- canonical-to-installed package completeness.

These fixtures describe inputs and required or forbidden contract outcomes.
They do not execute a model.

### Independent semantic review

Review the final package and both preservation inventories for trigger clarity, ownership, prerequisites, proof adequacy, status routing, stops, recording, claim boundaries, output usefulness, missing-resource behavior, and semantic preservation.

No Codex, Claude Code, opencode, or other target-agent runtime is executed or graded for implementation, verification, or release acceptance.
Do not add prompt journeys, transcript grading, runtime-version evidence, a permanent simplicity validator, or a prose-quality score.

Change-local line, word, byte, duplicate-cluster, and disposition measurements remain explanatory evidence rather than durable product invariants.

## Rollout and Rollback

1. Inventory semantic rules and exact literal consumers before editing the package.
2. Establish static contract fixtures for the current approved behavior.
3. Add the conditional formal-settlement reference and compact `SKILL.md` atomically.
4. Reuse the existing assets and boundary references without hand-editing generated output.
5. Regenerate and validate all supported package and adapter representations.
6. Record loaded-assembly and total-package measurements plus independent semantic review.

Rollback reverts the canonical package and directly coupled contract or package updates as one change, then regenerates derived outputs.
Do not roll back only `SKILL.md` while leaving a mapped reference or package inventory behind.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal proof policy is hidden in the formal reference | Closed ownership table and semantic rule-disposition ledger keep proof semantics inline. |
| Formal and isolated authority become conflated | Two-axis classification and static authority fixtures keep loading separate from settlement permission. |
| Boundary resources load too often or not often enough | Evidence-based applicability predicate, compact inline scan, and positive, negative, and ambiguous fixtures. |
| Assets become policy owners | Assets own only labels and layout; applicability and meaning remain in procedure. |
| Simplification freezes incidental literals | Separate literal inventory distinguishes contracts from test-only coupling. |
| Relocation is reported as deletion | Loaded assemblies and total package size are measured separately. |
| Package ships without the new resource | Existing deterministic package-chain parity plus explicit runtime stop behavior. |
| Percentage pressure removes necessary rules | Reduction target is advisory; semantic preservation controls acceptance. |
| Architecture examples become stale | Bounded assessment updates only affected examples, owned by this change when required. |

## Open Questions

None.

The proposal closes the package shape, invocation axes, resource triggers, ownership, failure behavior, proof boundary, testing boundary, measurement convention, and expected architecture assessment needed for specification.

## Decision Log

| Decision | Outcome | Rationale |
| --- | --- | --- |
| Package design | Compact `SKILL.md` plus one formal-settlement reference | Formal settlement is the largest coherent conditional authority boundary. |
| Boundary guidance | Keep both governed references unchanged and trigger them together when applicable | Method and proof completeness are distinct governed resources for one capability. |
| Universal proof rules | Keep inline | Any isolated review may need them. |
| Result structure | Reuse current assets as sole structural owners | Avoids synchronized inline templates. |
| Formal versus isolated | Separate predicate and settlement authority | Repository state alone must not turn advisory review into formal mutation. |
| Simplification evidence | Semantic and literal ledgers plus assembly metrics | Prevents silent policy loss and misleading size claims. |
| Runtime testing | Excluded | Static contracts and semantic review prove this guidance change without model-behavior machinery. |
| Architecture | Bounded assessment, default `architecture-not-required` | The existing packaged-skill model should already cover this resource layout. |

## Next Artifacts

When proposal review approves this direction:

1. a focused amendment or specification for the `test-spec-review` published-skill contract;
2. the bounded architecture assessment and any change-owned architecture entry it triggers;
3. an execution plan;
4. a traceable test specification; and
5. implementation, review, rationale, verification, and PR evidence through the governed lifecycle.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review` only.
This proposal does not claim acceptance, specification readiness, implementation readiness, branch readiness, or PR readiness.
