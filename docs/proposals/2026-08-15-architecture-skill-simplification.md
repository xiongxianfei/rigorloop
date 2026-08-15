<!-- Template: proposal-skeleton-v1 | Skill: proposal | Template status: normative | Maintained alongside: skills/proposal/SKILL.md | Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Architecture Skill Simplification

## Owning change record

`docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`

## Problem

The published `architecture` skill loads the same 1,765-word procedure for every invocation, whether the task is a small architecture-assessment decision, portable canonical-package authoring, governed lifecycle authoring, or an ADR-only update.

The common path mixes four different concerns: architecture applicability, workflow-managed assessment evidence, lifecycle-authorized artifact mutation, and detailed C4, arc42, diagram, and ADR method guidance. The three existing assets already own copied structure, but detailed method procedure and governed mutation remain inline even when the invocation cannot use them.

This increases routine context and makes authority harder to inspect. A no-impact assessment does not need canonical-package construction or ADR supersession procedure, and portable authoring must not load or imply `change.yaml` mutation. At the same time, moving too much behind references could hide architecture applicability, accepted-design boundaries, upstream settlement, or review handoff.

The problem is not the C4 plus arc42 plus ADR method. That accepted method, the smallest-surface architecture decision, canonical-package ownership, change-local assessment routing, and architecture-review boundary remain valuable. The problem is that universal selection, conditional method detail, and governed mutation do not have distinct package owners.

## Goals

- Reduce the procedural context loaded for architecture assessment, portable authoring, and governed authoring without weakening architecture applicability, accepted-design boundaries, or lifecycle safety.
- Keep a self-sufficient universal `SKILL.md` for evidence precedence, upstream readiness, assessment, action classification, source ownership, universal stops, claims, resource triggers, result shape, and handoff.
- Move detailed C4, arc42, diagram, ADR, package-consistency, and supersession procedure into one conditionally loaded architecture-package-method reference.
- Move exact `change.yaml` validation, artifact-entry transactions, authoring evidence, retries, concurrency handling, recovery, and matching `authoring → review-required` transitions into one conditionally loaded governed-authoring reference.
- Preserve the current three structural assets and keep policy, applicability, adequacy, lifecycle, and settlement decisions out of them.
- Separate architecture assessment from architecture artifact authoring, and separate action, target operation, governed signal, and execution authority.
- Measure real loaded profiles and total package size separately so relocation is not presented as deletion.

## Non-goals

- Replacing or weakening the accepted C4 plus official arc42 plus ADR method.
- Changing the architecture-assessment outcomes, workflow routing, architecture-review authority, plan handoff, or stage order.
- Reintroducing change-local architecture deltas as a normal authoring surface or using architecture to select unresolved product direction or behavior.
- Changing canonical architecture paths, ADR paths, diagram source format, official arc42 headings, required C4 levels, ADR semantics, or historical artifact validity.
- Adding another asset, a new lifecycle state, a new persistence or authorization mechanism, a runtime router, a generic architecture engine, a tokenizer dependency, a permanent simplicity validator, a prose classifier, a target-agent journey test, or a separate manual semantic-review acceptance gate.
- Optimizing `architecture-review` in the same proposal.

## Vision fit

fits the current vision

The change makes architecture decisions and authoring authority easier to inspect while preserving durable current design, decision history, reproducible validation, and independent human review. It reduces avoidable common-path context without weakening the traceability chain.

## Context

The current canonical package is:

```text
skills/architecture/
├── SKILL.md
└── assets/
    ├── architecture-skeleton.md
    ├── adr-skeleton.md
    └── diagram-styles.mmd
```

Current canonical measurements are:

| Resource | Lines | Words | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| `SKILL.md` | 233 | 1,765 | 13,105 |
| Architecture skeleton | 93 | 530 | 3,855 |
| ADR skeleton | 25 | 68 | 571 |
| Diagram styles | 6 | 37 | 362 |
| Complete package | 357 | 2,400 | 17,893 |

The accepted architecture method uses one canonical architecture package, all 12 official arc42 sections, C4 context and container diagrams by default, and ADRs for durable decisions. The later surface-simplification ADR removed change-local architecture deltas from the normal path and established four useful outcomes: no-impact rationale, canonical update, ADR work, or blocked routing to proposal/spec.

The workflow contract now separates a required post-spec-review architecture assessment from conditional architecture authoring. The assessment records `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`; only `architecture-required` enters architecture authoring and architecture review. The current skill still presents assessment and artifact authoring as one undifferentiated body.

The published-skill resource-integrity contract already recognizes the architecture skeleton and ADR skeleton as copy-and-fill assets and permits copied Mermaid styles as an asset because the file contains literal copied material. The proposed method reference is read-only packaged guidance and does not change those classifications.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `architecture` skill | in scope | Goals and Recommended Direction |
| Identify the best solution rather than only compressing prose | in scope | Options Considered and Recommended Direction |
| Create a new branch | in scope | Decision Log |
| Generate a governed proposal | in scope | This artifact and owning change record |
| Run `proposal-review` after authoring | in scope | Next Artifacts and Readiness |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Simplify universal assessment and routing | core to this proposal | This creates the smallest common path and preserves safe selection. |
| Add one architecture-package-method reference | core to this proposal | Detailed C4, arc42, diagram, ADR, and consistency procedure is conditional on artifact authoring. |
| Add one governed-authoring reference | core to this proposal | Lifecycle mutation is conditional on exact governed authority. |
| Preserve and clarify the three existing assets | same-slice dependency | Structural ownership and resource-map parity must remain coherent. |
| Update directly coupled skill validators and package fixtures | same-slice dependency | New references, closed profiles, and missing-resource behavior need deterministic proof. |
| Add change-local semantic, literal, scenario, and measurement evidence | same-slice dependency | Simplification must preserve behavior and report relocation honestly. |
| Update bounded architecture documentation examples if they depict a flat package | same-slice dependency | Existing architecture documentation must not contradict the final package inventory. |
| Change the C4, arc42, or ADR method | out of scope | Those accepted semantics are preserved. |
| Optimize `architecture-review` | separate proposal | Review judgment and settlement have a different common path and ownership boundary. |

## Options Considered

### Option 1: leave the package unchanged

This avoids compatibility risk and additional resources, but every no-impact and portable invocation continues loading governed mutation and detailed method procedure. It does not address the common-path problem.

### Option 2: compress only `SKILL.md`

Editorial compression can remove repetition and examples with little package change. It cannot create a durable authority boundary between portable work and governed mutation, and future maintenance can easily restore the same mixture.

### Option 3: extract only the architecture method

Moving C4, arc42, diagram, and ADR detail into one reference would make assessment materially shorter. Portable authoring would still load governed lifecycle transitions, evidence, retry, and concurrency procedure, so the authority boundary would remain mixed.

### Option 4: use one method reference and one governed-authoring reference

This makes `SKILL.md` the universal assessment and routing owner, loads method procedure only for actual architecture artifact authoring, and loads governed mutation only when both an authoring action and a governed candidate are present. It follows two real activation boundaries and reuses the existing asset and package model.

This is the recommended option.

### Option 5: split arc42, C4, diagrams, ADRs, assessment, and governed transactions into separate references

This would minimize some individual loads but create many navigation decisions, overlapping applicability, and fragile combined profiles. C4, arc42, diagrams, and ADRs form one coherent architecture-package method and do not justify four separate procedure owners in the first version.

### Option 6: replace prose with an executable architecture router

A router could enforce closed values, but architecture applicability, affected-section selection, diagram sufficiency, and ADR necessity remain judgment-heavy. A new runtime or state engine would be disproportionate to a package-content refactor.

## Recommended Direction

Adopt Option 4.

The final package should be:

```text
skills/architecture/
├── SKILL.md
├── references/
│   ├── architecture-package-method.md
│   └── governed-architecture-authoring.md
└── assets/
    ├── architecture-skeleton.md
    ├── adr-skeleton.md
    └── diagram-styles.mmd
```

### Classification model

Classify assessment execution, semantic judgment, route result, architecture action, governed signal, and target manifest before dependent reads or writes.

```text
assessment_mode:
  isolated
  workflow-managed

assessment_judgment:
  required
  not-required
  ambiguous

route_result:
  architecture-required
  architecture-not-required
  architecture-ambiguous

architecture_action:
  assessment-only
  canonical-update
  adr-only
  canonical-update-with-adr
  blocked

governed_signal:
  no-governed-signal
  single-governed-candidate
  invalid-or-ambiguous-governed-signal
```

Assessment judgment, route result, and architecture action are related but not interchangeable. `required`, `not-required`, and `ambiguous` map respectively to `architecture-required`, `architecture-not-required`, and `architecture-ambiguous`. A workflow-managed `assessment-only` invocation records or pauses on one judgment and does not author canonical architecture or ADR artifacts. `architecture-required` permits later authoring when its other prerequisites pass; it does not itself create authoring authority.

Any explicit change ID, workflow-managed change identity, structured owning-change field, or matching lifecycle artifact entry is a governed signal. A malformed, stale, conflicting, duplicated, escaped, or otherwise invalid signal produces `invalid-or-ambiguous-governed-signal` and stops without portable fallback.

### Loaded procedure assemblies

Use three primary procedural assemblies:

| Assembly | Action | Governed signal | Loaded procedure |
| --- | --- | --- | --- |
| `AA0-assessment` | `assessment-only` or `blocked` | any valid classification | `SKILL.md` |
| `AA1-portable-authoring` | canonical or ADR authoring | `no-governed-signal` | `SKILL.md` plus `architecture-package-method.md` |
| `AA2-governed-authoring` | canonical or ADR authoring | `single-governed-candidate` | portable-authoring procedure plus `governed-architecture-authoring.md` |

The structural assets are copied only when their output is applicable and are measured separately from procedural context. An invalid or ambiguous governed signal stops before a loaded assembly can grant mutation authority.

Late discovery of actual architecture authoring loads the method reference before selecting affected sections, diagrams, or ADR procedure. Late discovery of a governed signal loads the governed reference before lifecycle interpretation or mutation. Loading either reference grants no applicability, mutation, review, settlement, or continuation authority.

### Universal `SKILL.md` ownership

Keep these contracts inline:

- purpose, evidence access, source precedence, upstream readiness, and customer-project portability;
- the architecture assessment and smallest-surface decision;
- accepted design versus unresolved proposal/spec ownership;
- the closed action, operation, signal, and assembly vocabulary;
- canonical architecture, ADR, diagram, and historical-source ownership at a compact level;
- portable isolation and universal write boundaries;
- universal stops, claims, missing-resource behavior, result shape, and architecture-review handoff;
- exact resource triggers and the rule that assets own structure only.

The common file remains sufficient to return a truthful assessment or blocker without reconstructing conditional authoring procedure.

### Architecture-package-method reference ownership

The method reference owns detailed procedure for:

- selecting affected arc42 sections and maintaining all 12 official headings;
- C4 context, container, component, and deployment applicability;
- diagram source, propagation, linking, and style use;
- ADR triggers, create/revise/supersede/deprecate behavior, alternatives, consequences, and links;
- canonical-package consistency, quality scenarios, risks, glossary, and affected/unaffected reporting;
- full-document and bounded-update composition using the existing assets.

It must not own architecture applicability, upstream settlement, lifecycle mutation, review approval, routing, or claims.

### Governed-authoring reference ownership

The governed reference owns detailed procedure for:

- complete `change.yaml` inspection and exact authority validation;
- exact architecture-package and ADR artifact-entry resolution;
- deterministic intended paths for creation and current content identities for revision;
- authoring evidence, legal entry transitions, retries, concurrency detection, and idempotency;
- partial canonical-package, diagram, and ADR recovery;
- the matching `authoring → review-required` transition after complete artifact and evidence validation.

It must preserve every unrelated artifact entry and all workflow, automation, plan, and review state. It may not settle architecture review or advance workflow.

### Assessment basis for authoring

Every architecture authoring action requires a current `architecture-required` judgment. Workflow-managed authoring must bind one current architecture-assessment receipt whose exact specification and approving spec-review identities match the authoring manifest, with no later contradictory assessment and no unresolved `architecture-ambiguous` pause.

The workflow-managed assessment basis contains:

```text
assessment receipt identity
applicability: required
exact governing spec identity
current approving spec-review identity
```

Portable authoring does not require a RigorLoop assessment receipt, but it performs the same current inline applicability judgment before selecting `canonical-update`, `adr-only`, or `canonical-update-with-adr`. A portable judgment of `not-required`, `ambiguous`, or blocked by unresolved proposal or specification direction stops before mutation.

An assessment becomes stale when any decision-bearing basis changes, including the governing spec identity, approving spec-review identity, accepted proposal or durable decision basis, architecture-relevant requirements, or architecture-applicability evidence. Missing, stale, contradictory, `not-required`, or ambiguous assessment evidence cannot authorize artifact writes.

### Target manifest and transaction model

Canonical architecture and each ADR are distinct targets. Every authoring action binds one ordered target manifest before writes. A combined `canonical-update-with-adr` action resolves one canonical-package target and one or more exact ADR targets rather than treating the batch as one artifact identity.

Each target manifest entry contains:

```text
target kind
artifact ID
normalized path
operation
prior content identity or absent
intended content identity when known
governing input identities
authoring-evidence path when governed
assessment receipt identity when workflow-managed
exact governing spec identity
current approving spec-review identity
dependency target IDs
commit group
independently valid after commit: true or false
```

Target operations are exactly `create`, `revise`, `supersede`, and `deprecate`. `create` requires the exact target to be absent, while the other operations require the exact current target and identity. An existing canonical package or ADR cannot be replaced through `create`; a complete rewrite is still a revision. `supersede` and `deprecate` apply only to ADR targets under current durable-decision authority. Ambiguous targets, unsafe paths, duplicate candidates, or file/entry conflicts stop.

Governed creation additionally requires an absent matching entry and file. Governed revision requires one matching entry, file, current identity, and legal authoring or reopen authority. Downstream-reliant architecture or ADR content requires workflow-owned impact handling before revision authority is granted.

For a canonical package, the transaction identity includes the architecture artifact ID, canonical Markdown path, exact set of intended diagram paths, assessment basis, governing spec identity, authoring-evidence path, and baseline content identities. Each ADR transaction additionally binds its ADR ID, path, prior identity when revising, and create/revise/supersede/deprecate authority.

Dependency edges prevent a target from committing before its required dependencies are complete and validated. Targets that cannot leave a safe intermediate repository state independently share one commit group. The manifest's order remains deterministic, but order does not substitute for explicit dependencies or intermediate-validity proof.

### Multi-file writes, retries, and recovery

Governed authoring uses the existing authoring-evidence surface as a prepared write-ahead record. The complete ordered manifest is durable before the first architecture, diagram, or ADR file mutation. The first version uses evidence dispositions `prepared`, `partial-blocked`, `complete`, and `abandoned`; these describe the existing authoring transaction evidence and do not add lifecycle states or a new state owner.

The write sequence is:

1. Resolve the current required assessment, authority, targets, paths, operations, dependencies, commit groups, and baseline identities.
2. Prepare and validate all intended target content and compute every intended file identity.
3. Write a `prepared` authoring-evidence record containing the complete ordered manifest, assessment basis, dependencies, baselines, intended identities, and commit points.
4. Re-read the assessment, authority, and baseline identities; stop without target mutation if any changed.
5. Write only target files represented by the persisted manifest and record per-target progress on the same evidence surface.
6. Transition only completed governed entries to `review-required` after their commit-group and intermediate-validity checks pass.
7. Finalize the authoring evidence as `complete`, or record the exact safe partial result as `partial-blocked`.

An interruption before prepared evidence creates no target write. An interruption after a partial write reconciles only files, identities, and dependencies recorded in the prepared manifest. A file absent from that manifest is never adopted.

For a combined canonical and ADR action, each target has its own lifecycle entry and target progress inside the shared prepared authoring evidence. A target may commit independently only when the manifest proves that the resulting intermediate repository state is structurally and semantically valid without incomplete targets. Targets that cannot be independently valid commit through one group; failure must not mark an incomplete group member `review-required`.

Within the canonical architecture target, prepare all Markdown and diagram files together, write and validate subordinate diagram sources first, and write the canonical architecture Markdown last as the target commit point. The canonical Markdown must not expose links to incomplete diagrams or ADR dependencies.

ADR supersession uses this order: create and validate the replacement ADR; update predecessor ADR status and its superseded-by link; update canonical architecture references; then hand the complete target group to architecture-review. Authoring records the proposed supersession but does not approve it; architecture-review remains the settlement owner.

Batch results are exactly `complete`, `partial-blocked`, and `blocked-before-write`. `complete` requires every required manifest target to be complete and, for governed work, `review-required`. `partial-blocked` preserves only completed targets that remain independently valid, reports every committed and incomplete target, and blocks combined architecture-review handoff. `blocked-before-write` reports the blocker and performs no target write.

An identical retry resumes from the first incomplete target or file and never duplicates evidence, ADRs, diagrams, entries, or transitions. It requires the exact ordered manifest, inputs, paths, identities, and authority. Adding, removing, reordering, or changing a target creates a new operation and cannot be adopted as an identical retry.

Partial state is recoverable only when every existing file and entry matches the persisted transaction identity, baseline, dependency graph, and intended identity. A completed dependency may remain only when it is independently valid as an unreferenced artifact; a target that cannot be independently valid must not commit outside its group. An unregistered diagram, unrelated ADR, dangling artifact entry, changed dependency, changed canonical package, or ambiguous partial batch stops for explicit reconciliation. The proposal does not authorize destructive deletion of unknown or conflicting files.

Architecture-review handoff is eligible only after the entire required manifest reaches `complete`. The handoff names the exact target set so architecture-review can review the canonical update, related diagrams, and ADRs as one bounded change surface without treating them as one artifact identity.

### Assessment isolation and recording

Architecture assessment remains a distinct workflow-managed micro-stage. Its semantic judgment and current recording owner remain governed by the workflow contract, not by either new reference.

The `architecture` skill computes and returns the assessment because it owns architecture applicability judgment. Assessment behavior is closed as follows:

| Assessment mode | Judgment | Required result |
| --- | --- | --- |
| `isolated` | any | Return the judgment and rationale; write only to an explicit valid user-provided evidence path. |
| `workflow-managed` | `required` | Write the existing stage-owned completion receipt with `Stage: architecture-assessment`, `Applicability: required`, and the exact `Spec identity`. |
| `workflow-managed` | `not-required` | Write the existing stage-owned completion receipt with `Stage: architecture-assessment`, `Applicability: not-required`, and the exact `Spec identity`. |
| `workflow-managed` | `ambiguous` | Do not claim stage completion; return `architecture-ambiguous` and let workflow record its existing pause and owner-decision evidence. |
| any | identity or evidence conflict | Stop without assessment completion or authoring mutation. |

This intentionally narrows the current broad instruction to record a direct no-impact rationale in a plan, spec, change record, or PR surface. Direct assessment no longer mutates another stage's artifact implicitly. A user may supply one exact valid evidence path, while workflow-managed recording remains governed by the existing assessment and pause contracts.

`architecture-not-required` and `architecture-ambiguous` do not load the package-method or governed-authoring reference. `architecture-required` records applicability but loads authoring procedure only when the same or a later invocation actually enters a canonical or ADR authoring action. The proposal adds no new assessment field, parser vocabulary, lifecycle state, or pause owner.

### Asset ownership

Retain exactly the three current assets.

| Asset | Structural ownership |
| --- | --- |
| `architecture-skeleton.md` | Canonical architecture headings, ordering, links, table shapes, placeholders, and short fill prompts. |
| `adr-skeleton.md` | ADR headings, ordering, labels, and placeholders. |
| `diagram-styles.mmd` | Literal copied Mermaid role styles. |

Assets must not determine architecture applicability, affected-section adequacy, C4 level, ADR necessity, lifecycle authority, review status, or handoff. Missing a triggered skeleton or required copied styles stops before partial output. Missing an untriggered asset does not block assessment.

Classify current asset content as follows:

| Current content | Final disposition and owner |
| --- | --- |
| Official arc42 headings and section order | Retain in `architecture-skeleton.md`. |
| Related-artifact, diagram-link, ADR-link, and follow-on slots | Retain as structural placeholders in `architecture-skeleton.md`. |
| Neutral field prompts and table shapes | Retain in the applicable skeleton when they describe what to fill without deciding applicability or adequacy. |
| Canonical diagram source-format, location, linking, and propagation rules | Move to `architecture-package-method.md`. |
| Context, container, component, and deployment diagram applicability | Move to `architecture-package-method.md`. |
| Runtime, deployment, cross-cutting, and `Not applicable` decision rules | Move to `architecture-package-method.md`. |
| ADR trigger, link, supersession, and deprecation semantics | Move to `architecture-package-method.md`. |
| Quality-scenario stimulus, environment, response, and measure semantics | Move to `architecture-package-method.md`; retain only the structural table shape in the skeleton. |
| Literal Mermaid class definitions | Retain byte-for-byte in `diagram-styles.mmd` unless a separately approved style change applies. |

The asset inventory must classify every non-heading instruction before editing. A short fill prompt may remain only when it is neutral structural assistance and the rule ledger names the method reference as the sole normative owner. Full composition proof must show that method procedure plus copied assets preserve current output obligations without duplicate loaded policy.

### Resource failure

The shortened `SKILL.md` is sufficient for assessment and safe classification. It is intentionally insufficient to reconstruct detailed package-method or governed-authoring procedure.

A missing, unreadable, escaped, contradictory, stale, or mixed-version triggered reference or asset stops before its dependent judgment or write. The skill must not invent, recall, or partially reconstruct the missing procedure. Existing canonical-through-installed resource validation remains the deterministic prevention mechanism.

### Semantic preservation and literal compatibility

Create two separate change-local inventories before editing.

`architecture-rule-disposition.yaml` maps every behaviorally significant rule and duplicate cluster to one current owner, applicable assemblies, disposition, destination, and preservation proof.

`architecture-literal-compatibility.yaml` inventories exact headings, resource verbs, paths, enum values, result labels, arc42 titles, C4 terms, ADR labels, and phrases consumed by contracts, parsers, validators, packages, or incidental tests. Classify each as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `historical-fixture`, or `obsolete`.

Do not preserve exact prose solely because a snapshot contains it. Preserve normative and parser-sensitive literals exactly or migrate every consumer atomically.

### Measurement and success

Record current and final LF-normalized Unicode whitespace-separated words and UTF-8 bytes for:

- `AA0-assessment`;
- `AA1-portable-authoring`;
- `AA2-governed-authoring`;
- each procedural resource;
- each structural asset;
- the complete package.

Count each unique loaded procedural resource once in `SKILL.md`, method-reference, governed-reference order. Exclude copied assets from procedural totals and report representative copied output separately. Record paths, assembly order, and content identities.

Acceptance requires all three real procedural profiles to decrease in words and bytes, every semantic rule and literal dependency to have one disposition, and every identified duplicate cluster to have one loaded owner. Total package growth is allowed only when reported and justified; no fixed percentage overrides semantic or lifecycle preservation.

Token estimates are optional and may be reported only when an existing repository-owned pinned implementation already supports the exact assemblies. Do not add a tokenizer dependency.

### Proposal acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-ARSIM-001` | Isolated and workflow-managed architecture assessment use separate closed recording authority. |
| `AC-ARSIM-002` | `required`, `not-required`, and `ambiguous` map deterministically to route results and existing durable workflow behavior. |
| `AC-ARSIM-003` | Workflow completion receipts retain `Stage`, `Applicability`, and exact `Spec identity`, while ambiguity pauses without claiming completion. |
| `AC-ARSIM-004` | Direct assessment performs no implicit cross-stage mutation and records only to an explicit valid evidence path. |
| `AC-ARSIM-005` | Every canonical architecture or ADR target has one exact target-local operation and identity basis. |
| `AC-ARSIM-006` | Combined authoring binds one ordered target manifest and does not treat several artifacts as one identity. |
| `AC-ARSIM-007` | `partial-blocked` and `blocked-before-write` cannot claim combined architecture-review eligibility. |
| `AC-ARSIM-008` | Identical retry cannot add, remove, reorder, or change a manifest target. |
| `AC-ARSIM-009` | Every current asset instruction has one structural, method-owned, literal-style, or removed-duplicate disposition. |
| `AC-ARSIM-010` | Method applicability and adequacy rules are not duplicated in copied assets. |
| `AC-ARSIM-011` | `AA0`, `AA1`, and `AA2` all decrease in words and UTF-8 bytes from the recorded baseline. |
| `AC-ARSIM-012` | Missing triggered references or assets stop before dependent judgment or writes. |
| `AC-ARSIM-013` | Canonical, generated, archived, release-candidate, and installed resources retain required inventory and raw-byte parity. |
| `AC-ARSIM-014` | No target-agent runtime, transcript grader, prose classifier, separate manual semantic-review gate, tokenizer dependency, or permanent simplicity validator is introduced. |
| `AC-ARSIM-015` | Every workflow-managed authoring manifest binds one current `architecture-required` assessment receipt. |
| `AC-ARSIM-016` | Assessment, specification, and approving spec-review identities match the authoring manifest. |
| `AC-ARSIM-017` | Missing, stale, contradictory, `not-required`, or ambiguous assessment evidence blocks authoring. |
| `AC-ARSIM-018` | Portable authoring performs a current applicability judgment before mutation. |
| `AC-ARSIM-019` | A changed decision-bearing basis makes prior assessment evidence stale. |
| `AC-ARSIM-020` | The complete ordered manifest and every intended file identity are durably recorded before the first target-file mutation. |
| `AC-ARSIM-021` | An interruption before prepared evidence causes no target write, while a later interruption reconciles only recorded manifest files. |
| `AC-ARSIM-022` | A file not represented by the persisted manifest is never adopted. |
| `AC-ARSIM-023` | Combined manifests record dependency edges, commit groups, and intermediate-validity decisions. |
| `AC-ARSIM-024` | A target commits independently only when the resulting partial repository state is valid. |
| `AC-ARSIM-025` | Canonical architecture Markdown cannot reference incomplete diagrams or ADR dependencies. |
| `AC-ARSIM-026` | ADR supersession writes use deterministic dependency order and remain subject to architecture-review approval. |
| `AC-ARSIM-027` | `partial-blocked` preserves only independently valid completed targets. |
| `AC-ARSIM-028` | Architecture assessment changes to `architecture-required` if existing evidence cannot support prepared recovery and dependency-aware progress without new architecture. |

## Expected Behavior Changes

- Architecture assessment loads only the compact universal procedure and does not load detailed authoring method or governed mutation.
- Isolated assessment writes only to an explicit valid evidence path, while workflow-managed required/not-required receipts retain current fields and ambiguity remains a workflow-owned pause.
- Portable canonical-package and ADR authoring load the universal procedure plus one architecture-package-method reference.
- Governed authoring additionally loads one exact lifecycle procedure after candidate classification and before mutation.
- C4, arc42, diagram, ADR, assessment, review, and handoff semantics remain unchanged.
- Invalid or ambiguous governed signals fail closed rather than falling back to portable authoring.
- Canonical packages, diagrams, and ADRs receive per-target operations, an ordered manifest, exact retry boundaries, closed batch results, and partial-state reporting.
- Workflow-managed authoring binds the current required assessment, exact spec identity, and approving spec-review identity; portable authoring performs the same current applicability judgment inline.
- Governed authoring persists the complete prepared manifest before mutation and records target progress on the existing authoring-evidence surface.
- Combined targets use explicit dependency edges, commit groups, and intermediate-validity checks; canonical Markdown is written after its diagram and ADR dependencies.
- Existing assets remain the only copied structural resources; policy-bearing skeleton text moves to the method reference under an explicit disposition ledger.

## Architecture Impact

The expected assessment is `architecture-not-required` because the change applies the existing published-skill package model, accepted architecture method, resource-integrity contract, assessment evidence, authoring evidence, and stage-owned lifecycle model. That result is conditional on the existing authoring-evidence model supporting a durable prepared manifest, per-target progress, dependency edges, and commit groups without a new schema, persistent authority, or write owner.

A bounded architecture documentation update is required only if the current canonical package, ADR inventory, or diagram depicts `skills/architecture/` as permanently flat, assigns detailed method policy to assets, or omits packaged references as a supported skill resource. A new ADR is not expected.

If specification discovers that prepared recovery or dependency-aware combined commits require a new persisted transaction record, schema, lifecycle state, or write owner, the architecture assessment must change to `architecture-required` before planning. Recovery must not be weakened merely to preserve the expected no-architecture result.

## Testing and Verification Strategy

Use deterministic static proof and existing package validators.

- Build rule and literal inventories before editing, with invalid unknown-value fixtures that fail closed before consistency checks.
- Add static scenarios for isolated and workflow-managed assessment, required/not-required completion receipts, ambiguous pause, direct explicit-path recording, current and stale assessment bases, portable applicability, action and signal combinations, canonical-only, ADR-only, mixed-operation combined manifests, durable pre-write preparation, interruption before and after preparation, identical retry, changed manifest, dependencies, commit groups, canonical commit order, ADR supersession order, each batch result, concurrency, stale basis, missing resources, unsafe paths, and forbidden writes or claims.
- Validate the canonical skill and exact resource map, including required `READ` and `COPY` verbs, containment, presence, and duplicate ownership.
- Validate an asset-content disposition for every current non-heading instruction and prove that method semantics have one loaded owner.
- Prove the three procedural assemblies and assets with deterministic word/byte accounting.
- Run the existing skill-validator, build-skills, adapter-distribution, boundary, lifecycle, change-metadata, and review-artifact checks selected by the later plan and test spec.
- Build fresh local release candidates and inspect canonical, generated, archived, release-candidate, and clean-installed resource inventories and raw-byte identities for Codex, Claude, and opencode.
- Use ordinary proposal, spec, plan, code, verification, and PR review as the human judgment surfaces.

Do not execute Codex, Claude Code, opencode, or another target-agent runtime for acceptance. Do not grade transcripts, add a separate manual semantic-review acceptance stage, infer semantic classifications with a prose validator, or add a permanent simplicity or tokenizer gate.

## Rollout and Rollback

Rollout is one atomic canonical package change after proposal, spec, architecture assessment, plan, test-spec, and required reviews settle. Add the two references, shorten `SKILL.md`, revise policy-bearing skeleton instructions according to the approved disposition while retaining exactly three assets, update directly coupled validators and fixtures, and prove generated/archive/install parity in the same implementation change.

Do not hand-edit `.agents/skills/`, `.codex/skills/`, generated adapter bodies, release archives, or installed target trees. Canonical source remains under `skills/`, and generated or installed proof comes from repository-owned build and packaging commands.

Rollback restores the previous `SKILL.md`, removes both new references, restores the prior resource map and directly coupled validator expectations, and rebuilds generated packages from canonical source. Preserve change-local proposals, reviews, inventories, and measurements as historical evidence.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| The core becomes too short to classify assessment and authority safely | Keep evidence precedence, assessment, closed classifications, stops, claims, and resource triggers inline. |
| The method reference becomes an independent policy owner | State that it specializes detailed procedure and cannot override universal applicability, lifecycle, or review contracts. |
| Assets retain or accumulate hidden method policy | Classify every current instruction and move normative method rules to the reference while retaining only structure, neutral prompts, and literal styles. |
| Combined canonical and ADR work leaves inconsistent partial state | Bind one ordered per-target manifest, use closed batch results, and require complete manifest settlement before review handoff. |
| Authoring proceeds from stale applicability evidence | Bind workflow-managed manifests to the current required assessment, spec, and approving review identities, and repeat current applicability judgment for portable work. |
| An interruption leaves files that cannot be distinguished from unrelated content | Persist the complete manifest and intended identities before mutation and reconcile only recorded targets. |
| Independent commits expose broken diagram, ADR, or supersession relationships | Record dependencies and commit groups, write subordinate files before canonical Markdown, and preserve only independently valid targets. |
| Assessment wording diverges from workflow evidence | Separate judgment, route result, and persisted completion fields; keep ambiguity as a pause rather than a completed receipt. |
| Invalid governed metadata falls through to portable mutation | Use tri-state governed signals and stop on every malformed, stale, conflicting, or ambiguous signal. |
| Additional resources increase total package size | Measure all profiles and total package separately; require every real profile to shrink and justify total growth. |
| Tests freeze incidental prose | Separate semantic-rule and literal inventories and migrate incidental assertions rather than treating snapshots as policy. |
| Package outputs omit or transform a new reference | Reuse raw-byte canonical-through-installed parity and clean-install proof for all supported adapters. |

## Open Questions

None at proposal level. Exact evidence field names, scenario fixture encoding, measurement commands, and directly coupled consumer lists belong to specification and planning after bounded inventory.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-15 | Create branch `proposal/architecture-skill-simplification` from merged `origin/main` at `dcf357cec292`. | Isolate the initiative from the merged spec-skill change. | Reuse the merged feature branch. |
| 2026-08-15 | Select one method reference and one governed-authoring reference. | The resources follow independent authoring-method and lifecycle-authority boundaries. | Inline compression, method-only extraction, highly fragmented references, and an executable router. |
| 2026-08-15 | Keep assessment procedure and universal safety inline. | Assessment and fail-closed classification must work before optional authoring resources are selected. | Moving assessment behind a reference. |
| 2026-08-15 | Preserve exactly the three existing assets. | They already own copied structure and styles and do not need another structural resource. | New result, assessment, diagram, or transaction assets. |
| 2026-08-15 | Require all three real procedural profiles to shrink. | A smaller main file alone would not prove assessment, portable, or governed invocation improvement. | Main-file-only or fixed-percentage acceptance. |
| 2026-08-15 | Resolve `ARSIM-PR1` with separate assessment mode, judgment, route, and existing persistence behavior. | Assessment ambiguity is a workflow pause, and direct assessment must not mutate another stage implicitly. | One overloaded outcome value or a new persisted assessment schema. |
| 2026-08-15 | Resolve `ARSIM-PR2` with an ordered per-target manifest and complete-manifest review handoff. | Combined architecture and ADR work can mix target operations without requiring atomic rollback or new lifecycle state. | One invocation-wide operation or independent review handoff from a partial batch. |
| 2026-08-15 | Resolve `ARSIM-PR3` with an asset-content disposition. | Current skeleton prose includes method semantics that need one normative owner. | Keeping duplicated policy or adding another asset. |
| 2026-08-15 | Resolve `ARSIM-PR4` by binding authoring to one current required assessment basis. | Applicability must remain current across spec and review revisions rather than being implied by generic authoring authority. | Unbound later authoring or a new authorization subsystem. |
| 2026-08-15 | Resolve `ARSIM-PR5` with a durable prepared manifest on the existing authoring-evidence surface. | Exact interruption recovery requires the manifest and intended identities before the first target write. | In-memory retry identity or weakened recovery claims. |
| 2026-08-15 | Resolve `ARSIM-PR6` with dependency edges, commit groups, and deterministic commit points. | Partial completion is safe only when each preserved target is independently valid. | Universal atomic rollback or unsafe independent commits. |

## Next Artifacts

- Independent `proposal-review` of this proposal.
- Focused amendment to the published skill contract and architecture-package method contract after proposal approval.
- Bounded architecture assessment after spec review.
- Execution plan and test specification after the contract and assessment settle.

## Follow-on Artifacts

None yet

## Readiness

Revised after `proposal-review-r2` and ready for independent proposal rereview. This proposal does not claim proposal approval, specification readiness, architecture-assessment completion, implementation readiness, verification, branch readiness, or PR readiness.
