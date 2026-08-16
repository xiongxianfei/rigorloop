# Architecture Review Skill Simplification

## Owning change record

[Architecture Review Skill Simplification change record](../changes/2026-08-16-architecture-review-skill-simplification/change.yaml)

## Problem

The current `architecture-review` skill is a flat 2,192-word, 15,982-byte procedure with no mapped references or structural assets. Every invocation loads target discovery, four review surfaces, detailed C4 and arc42 method, ADR checks, package-quality heuristics, material-finding rules, formal recording, lifecycle settlement, retry behavior, automation independence, and workflow handoff.

Those concerns do not all activate together. A no-architecture-impact rationale or upstream proposal/spec gap does not need the complete C4, arc42, diagram, and ADR package checklist. An isolated architecture review does not need exact `change.yaml` settlement mechanics unless durable recording or governed lifecycle authority applies. Conversely, universal evidence precedence, review judgment, materiality, stops, and claims must remain available before any optional resource is selected.

The flat package also overlaps policy ownership. Architecture method requirements appear in the approved architecture package specification and are repeated as reviewer procedure in `SKILL.md`, while lifecycle recording and settlement rules are mixed into the same path. This makes the common review contract harder to scan and increases the chance that later edits compress identity, retry, recording, or review-quality rules accidentally.

The May architecture-surface simplification already settled which surfaces architecture-review may review. The recently merged architecture skill simplification settled the packaged-skill direction for architecture authoring. This proposal must preserve those decisions rather than redesigning architecture practice.

## Goals

- Make universal architecture-review judgment shorter and easier to scan without weakening evidence, materiality, status, recording, or claim safety.
- Move detailed canonical-package, C4, arc42, diagram, and ADR review procedure behind one evidence-based trigger.
- Move detailed durable recording, exact governed settlement, retry, and workflow-managed automation procedure behind one independent trigger.
- Preserve the accepted review surfaces: `canonical-architecture-update`, `ADR`, `no-architecture-impact-rationale`, and `proposal-or-spec-gap`.
- Keep resource loading, semantic judgment, durable recording, lifecycle settlement, and automation authority as separate decisions.
- Preserve exact multi-target identity when one review covers a canonical architecture package and related ADRs.
- Prove semantic preservation, literal compatibility, real loaded-profile reduction, and canonical-through-installed package parity deterministically.

## Non-goals

- Redesigning the C4 plus arc42 plus ADR method.
- Reopening the accepted architecture surface model or restoring change-local architecture deltas as a normal review surface.
- Letting architecture-review settle product direction, specification behavior, workflow routing, implementation, or plan readiness.
- Changing review statuses, finding severity, material-finding dispositions, artifact lifecycle states, or review-recording ownership.
- Adding an executable classifier, architecture parser, diagram validator, generic review engine, lifecycle schema, persistence mechanism, or state owner.
- Adding new structural assets solely to move the current compact result and finding labels out of `SKILL.md`.
- Executing a target-agent runtime, grading transcripts, or adding a separate manual semantic-review acceptance stage.
- Hand-editing generated adapter packages or tracked generated public skill bodies.

## Vision fit

fits the current vision

The change makes architecture review easier to inspect and resume while preserving the evidence and lifecycle rules that make review trustworthy. It reduces irrelevant context rather than removing review rigor, keeps decisions in durable repository artifacts, and leaves normal PR review as the human semantic judgment surface.

## Context

`CONSTITUTION.md` requires architecture-affecting changes to update relevant architecture artifacts, requires formal lifecycle reviews to create durable evidence, and restricts review peers to their own review evidence and matching artifact settlement. `docs/workflows.md` makes `change.yaml` the only mutable lifecycle owner, keeps direct review isolated by default, and assigns workflow routing to `workflow`.

`specs/architecture-package-method.md` requires architecture-review to classify one of four surfaces before applying checks. It also defines C4 sufficiency, all 12 arc42 sections, Runtime and Deployment View applicability, ADR completeness, no-impact credibility, and the simple architecture-review finding format that remains additive to the repository-wide material-finding contract.

The current skill correctly implements those semantics, but places them in one common file. Its largest conditional clusters are the canonical-package method and package-quality checks, followed by detailed formal recording, lifecycle settlement, retry, and workflow-managed review independence.

The recently merged architecture skill package uses a compact universal file, one conditional architecture method reference, one conditional governed-authoring reference, and structural assets. Architecture-review should follow the same progressive-disclosure principle without importing or cross-linking another skill's private reference. The architecture package specification remains the shared normative source; the new review reference should contain reviewer-specific procedure and failure signals only.

## Options Considered

### Option 0: Keep the current flat skill

This avoids immediate change and preserves one-file navigation. It retains the highest common-path context cost, overlapping ownership, and the risk that changes to one concern disturb unrelated review modes.

### Option 1: Compress the existing file editorially

This removes repetition and can improve readability with the smallest package diff. It does not create a conditional loading boundary, leaves method and settlement procedure mixed, and makes future growth likely to recreate the current problem.

### Option 2: Extract only architecture-package review method

This moves the largest C4, arc42, diagram, ADR, and package-quality cluster into one reference. It materially helps no-impact and upstream-gap review, but formal recording, exact lifecycle settlement, retry, and workflow automation remain mixed into the universal path.

### Option 3: Add one package-review reference and one recording-and-settlement reference

This creates two independent activation boundaries: semantic package-method depth and durable review side effects. It supports compact no-impact and upstream-gap review, method-rich canonical and ADR review, isolated durable review, and governed formal settlement without multiplying narrow resources.

The tradeoff is that a normal governed canonical or ADR review loads both references, so success must be measured against that real assembly rather than inferred from a shorter `SKILL.md`.

### Option 4: Split references by C4, arc42, ADR, recording, settlement, automation, and review surface

This maximizes theoretical selectivity but creates excessive navigation and makes combined canonical-plus-ADR review assemble many small policy fragments. The boundaries are too fine-grained for the number of independent user-facing activation conditions.

### Option 5: Replace prose review orchestration with an executable review engine

This could enforce routing and record shapes mechanically. It would introduce runtime machinery, semantic classification pressure, new maintenance surfaces, and architecture beyond the problem. Architecture judgment remains evidence-sensitive and reviewer-owned.

## Recommended Direction

Choose Option 3.

Use this package shape:

```text
skills/architecture-review/
├── SKILL.md
└── references/
    ├── architecture-package-review.md
    └── architecture-review-recording-and-settlement.md
```

Do not add an output asset in the first version. The current result and finding shapes are compact, and creating an asset would add package surface without removing a substantial repeated structure. If later evidence shows repeated structural drift, that should be a separate scoped decision.

### Universal `SKILL.md` ownership

Keep these rules inline:

- purpose, review authority, and project-local evidence behavior;
- target resolution and exact reviewed revision;
- the four accepted review surfaces and compact surface selection;
- evidence precedence and bounded reading;
- universal spec alignment and architecture-impact judgment;
- core review dimensions, status values, severity, and materiality;
- the compact no-impact credibility scan and upstream proposal/spec routing;
- durable-recording trigger classification and isolation;
- material-finding completeness;
- missing-resource behavior, stops, claims, and handoff limits;
- exact resource triggers and the compact result contract.

The main file must remain capable of rejecting ambiguous targets, spec conflicts, unsupported no-impact claims, incomplete findings, unavailable required procedure, unsafe writes, and overbroad claims before any optional resource is trusted.

### `architecture-package-review.md` ownership

Load this reference when the review surface is `canonical-architecture-update` or `ADR`, including a canonical update whose reviewed target set contains related ADRs.

The reference owns:

- the detailed C4 and arc42 review procedure;
- diagram sufficiency, level, role, technology-label, and relationship checks;
- Runtime View, Deployment View, Crosscutting Concepts, quality-scenario, risk, and glossary checks;
- Building Block View hierarchy and responsibility checks;
- canonical package consistency, diagram-source linkage, and legacy-document boundaries;
- ADR context, decision, alternatives, consequences, supersession, and canonical-link checks;
- reviewer-specific package-quality failure signals and conditional component/deployment-diagram judgment;
- full-file requirements specific to canonical package or ADR review.

This reference must not duplicate the complete architecture authoring method or become a second normative architecture specification. It consumes the approved project-local architecture method and specializes how a reviewer applies it.

### `architecture-review-recording-and-settlement.md` ownership

Load this reference when durable recording is required. Durable recording is required for a formal lifecycle review, an explicit durable-record request, any material finding, or status `changes-requested`, `blocked`, or `inconclusive`.

The reference owns:

- review-record placement and clean versus detailed record selection;
- review-log synchronization and conditional review-resolution creation;
- isolated durable recording boundaries;
- complete `change.yaml` validation for governed settlement;
- exact artifact target resolution, write ordering, lifecycle-state mapping, and preservation of unrelated state;
- identical retry, review-ID reuse, partial settlement, concurrency, and failed-validation behavior;
- workflow-managed automated review independence, packets, receipts, correction limits, and return to workflow.

Loading this reference grants no settlement, automation, correction, or continuation authority. The main file owns whether durable recording is required, while this reference owns how the valid recording mode is executed.

### Independent classification axes

Use four independent classifications.

```text
review_surface:
  canonical-architecture-update
  ADR
  no-architecture-impact-rationale
  proposal-or-spec-gap

recording_mode:
  none
  advisory-durable
  formal-lifecycle

settlement_mode:
  isolated
  governed

automation_mode:
  manual
  workflow-managed-automated
```

`recording_mode: none` is valid only for non-formal review-like feedback that requests no durable status or evidence and produces no material or non-approval result. An explicit `architecture-review` request that asks for formal review status or lifecycle evidence is formal. `workflow-managed-automated` is valid only with `formal-lifecycle` and `governed` authority.

Resource loading and authority remain separate:

```text
loaded resources determine available procedure
recording and settlement modes determine permitted writes
automation mode determines permitted automated branches
```

Unknown, mixed, contradictory, or unresolved classifications stop before dependent judgment or writes.

### Loaded assemblies

Use these assemblies:

| Assembly | Package-method context | Durable-recording context | Loaded procedure |
| --- | ---: | ---: | --- |
| `ARR0-core` | no | no | `SKILL.md` |
| `ARR0M-method` | yes | no | core plus package-review reference |
| `ARR1-recorded` | no | yes | core plus recording-and-settlement reference |
| `ARR1M-recorded-method` | yes | yes | core plus both references |

The primary real profiles are isolated formal no-impact review, isolated formal canonical or ADR review, governed formal no-impact review, and governed formal canonical or ADR review. Informal feedback may be measured but must not be used as the sole simplification success surface.

Late discovery of package-method or durable-recording context must load the required reference before dependent judgment, recording, status, or settlement. Each reference loads at most once.

### Exact target and review-occurrence identity

Every formal review occurrence binds:

```text
review ID and round
repository revision
primary review surface
ordered target IDs
target kinds and normalized paths
target content identities
authoring-evidence identities when governed
review record and log paths
```

A canonical package target may include its architecture Markdown and linked diagram sources as one package identity. Related ADRs remain distinct lifecycle targets in the ordered set. A standalone ADR review uses the `ADR` surface. A canonical update with related ADRs uses `canonical-architecture-update` as the primary surface and includes each ADR as an exact target.

The first version retains one semantic review status for the exact occurrence and target set. It does not introduce partial semantic approval. A finding against any required target prevents the complete target set from receiving an approved occurrence.

No-impact rationale and proposal/spec-gap review are record-only surfaces unless an existing governed artifact entry explicitly represents the reviewed rationale. They must not invent an architecture or ADR lifecycle target merely to settle a review.

### Judgment, recording, and settlement results

Keep semantic judgment separate from execution results.

```text
review_status:
  approved
  changes-requested
  blocked
  inconclusive

recording_status:
  not-required
  recorded
  blocked

settlement_result:
  not-applicable
  recorded-isolated
  settled
  partial-retry-required
  not-settled
  blocked
```

An approved judgment with blocked recording does not complete formal review. A valid identical retry may finish recording or settlement using one exact prior judgment without rerunning semantic review or creating duplicate records. A retry must stop if revision, target set, identity, authority, status, or review ID changed.

For governed multi-target settlement, write the durable review record first and settle only the exact ordered target set. An interruption may leave an identity-proven partial settlement that an identical retry completes, but the invocation cannot claim settled review until every required target reaches the prescribed state. Unrelated artifact entries, milestone state, and workflow routing remain unchanged.

### Resource failure behavior

If the package-review reference is required but missing, unreadable, escaped, contradictory, or mixed-version, stop before a canonical-package or ADR verdict. Do not reconstruct detailed method from memory.

If the recording-and-settlement reference is required but unavailable, preserve the complete semantic findings in the invocation result, report `recording_status: blocked`, and claim neither formal completion nor lifecycle settlement. Missing untriggered resources do not block another profile.

### Output behavior

Retain the current compact result fields and simple finding shape inline. The result must distinguish review surface, review status, recording status, settlement result, exact targets, material findings, blockers, required canonical or ADR updates, next stage, and claim limitations.

For a retry that performs no new semantic review, report the safely reused review ID and status separately from the retry transaction result. Do not manufacture a new review round or status.

## Expected Behavior Changes

- No-impact and upstream-gap review no longer load the detailed canonical package and ADR checklist.
- Canonical and ADR review load one reviewer-focused method reference rather than keeping the complete checklist inline.
- Durable recording and lifecycle settlement load one independent procedure and do not become implied by package-method loading.
- Combined canonical-plus-ADR reviews bind one exact ordered target set and cannot settle unrelated or ambiguous targets.
- Identical recording or settlement retries reuse one exact judgment without duplicate semantic review evidence.
- Missing triggered procedure fails closed at the dependent claim boundary.
- Review surfaces, statuses, severity, material-finding obligations, lifecycle ownership, and workflow handoff remain behaviorally unchanged.

## Architecture Impact

The expected bounded assessment is `architecture-not-required`. The design uses the existing published-skill package model, existing formal-review evidence, existing artifact entries, and existing review settlement ownership. It adds no service, runtime router, persistence mechanism, schema, lifecycle state, dependency, or independent policy owner.

A documentation-only architecture update is appropriate only if the current architecture package inventory depicts `architecture-review` as permanently flat or lists an exact resource inventory that becomes stale.

Architecture becomes required if the specification discovers that exact multi-target retry requires a new persisted transaction record, review schema, lifecycle state, or write owner. The implementation must not weaken recovery merely to preserve the expected no-architecture result.

## Testing and Verification Strategy

Before editing the skill, create separate change-local inventories for:

- every behaviorally significant rule and its current owner;
- every exact heading, status, field, path, and phrase consumed by validators, fixtures, packages, or governance contracts;
- the current `SKILL.md`, real loaded-profile, and total-package word and UTF-8 byte baselines.

Classify literal dependencies as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `historical-fixture`, or `obsolete`. Do not preserve prose merely because a snapshot contains it.

Add deterministic static scenarios for:

- each of the four review surfaces;
- all four loaded assemblies;
- combined canonical and ADR targets;
- exact target identity, stale revision, ambiguous target, and conflicting authoring evidence;
- isolated versus governed recording and settlement;
- clean, material, blocked, and inconclusive outcomes;
- no-impact credibility and upstream proposal/spec routing;
- identical retry, partial settlement, review-ID collision, and concurrent change;
- missing triggered and untriggered references;
- forbidden edits to reviewed artifacts, unrelated entries, milestone state, or routing;
- absence of duplicate policy ownership and unfilled result fields.

Validate canonical `skills/architecture-review/` resources, generated packages, release archives, release candidates, and clean-installed Codex, Claude, and opencode resources through existing repository scripts. Do not hand-edit derived output.

Acceptance uses deterministic contract fixtures, existing validators, package parity, lifecycle validation, and ordinary proposal, spec, code, and PR review. It must not execute Codex, Claude Code, opencode, or another target-agent runtime; grade transcripts; infer semantic architecture quality mechanically; or create a separate manual semantic-review gate.

Measure canonical UTF-8 bytes and Unicode whitespace-separated words with LF normalization. Report each real loaded assembly, each reference, and the complete package separately. Token estimates are optional only when an existing pinned repository-owned implementation supports the exact assembly; do not add a tokenizer dependency.

Acceptance requires a reduction in the primary isolated formal and governed formal loaded profiles where their required resource sets changed, complete semantic-rule disposition, one owner for every duplicate cluster, and no unexplained package growth. A fixed percentage must not override semantic or lifecycle preservation.

## Rollout and Rollback

Rollout proceeds through proposal review, focused skill-contract specification, bounded architecture assessment, execution plan, test specification, implementation, independent review, explanation, final verification, and PR handoff.

Implementation edits only canonical content under `skills/architecture-review/` and directly coupled validation or contract surfaces. Generated, archived, release-candidate, and installed packages refresh through existing build and validation paths.

Rollback restores the prior canonical skill package and directly coupled tests or package metadata. Because the proposal adds no state or schema, rollback does not require data migration. Review records created under the unchanged formal-review contract remain durable historical evidence.

## Risks and Mitigations

- Risk: Moving detailed checks behind a reference could let a canonical or ADR review proceed without the full method. Mitigation: use a closed positive trigger, late-discovery loading, missing-resource failure, and static profile scenarios.
- Risk: The recording reference could become a second owner of review status or materiality. Mitigation: keep judgment, trigger classification, statuses, and claim boundaries inline and assign only recording mechanics and settlement to the reference.
- Risk: A shorter common file could omit no-impact or proposal/spec-gap safety. Mitigation: keep the compact impact scan and upstream routing inline and prove both as core-only scenarios.
- Risk: Combined target settlement could widen architecture-review authority. Mitigation: bind one ordered exact target set, retain one occurrence status, forbid partial semantic approval, and preserve every unrelated state surface.
- Risk: The main file shrinks while real formal review profiles do not improve. Mitigation: make loaded formal profiles the primary measurement surfaces and report total package accounting separately.
- Risk: Reviewer method drifts from architecture authoring method. Mitigation: keep the approved architecture package specification normative and make the reference reviewer-specific rather than a copied authoring guide.
- Risk: Tests freeze incidental prose. Mitigation: separate semantic-rule and literal-compatibility inventories and update incidental snapshots instead of turning them into policy.
- Risk: More files increase package drift. Mitigation: require canonical-through-installed resource parity through existing build and adapter validation.

## Open Questions

None at proposal level. Exact field names, parser-sensitive literals, baseline identities, and fixture commands remain evidence-dependent specification and planning details within the closed semantics above.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-16 | Select one package-review reference and one recording-and-settlement reference. | These are the two independent activation and ownership boundaries in the current flat skill. | Flat skill, editorial compression only, method-only extraction, fragmented references, executable engine. |
| 2026-08-16 | Keep universal judgment, no-impact safety, materiality, statuses, stops, and claims inline. | Optional resources must not weaken the minimum safe review contract. | Moving all review policy behind references. |
| 2026-08-16 | Keep one semantic status for one exact ordered target set in the first version. | This preserves current occurrence semantics while making multi-target identity and retry explicit. | Partial semantic approval or independent per-target review occurrences. |
| 2026-08-16 | Add no structural asset in the first version. | The existing result and finding shapes are compact and do not justify another package surface. | New result and finding assets without demonstrated duplication value. |
| 2026-08-16 | Use deterministic proof and ordinary PR review without target-agent or separate manual semantic acceptance. | The change is a content and ownership refactor, and human PR review already owns final semantic judgment. | Runtime journeys, transcript graders, prose classifiers, or a new manual gate. |

## Next Artifacts

- Focused `architecture-review` skill-contract specification.
- Bounded architecture assessment with expected result `architecture-not-required`.
- Execution plan with preservation inventory, package implementation, and measurement/parity milestones.
- Test specification mapping review surfaces, profiles, identity, recording, settlement, recovery, resource failure, and package parity.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent proposal review. This proposal does not claim acceptance, specification readiness, architecture settlement, implementation readiness, verification, or PR readiness.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `architecture-review` skill after completing the architecture skill simplification. | in scope | Problem, Goals, Recommended Direction |
| Use progressive disclosure without weakening architecture judgment or lifecycle safety. | in scope | Universal ownership, reference ownership, resource failure, testing |
| Create the work on a new branch and record a governed proposal. | in scope | Owning change record and governed authoring evidence |
| Run independent proposal review after authoring. | in scope | Readiness and change-local review handoff |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal architecture-review contract | core to this proposal | It defines the safe common path and resource triggers. |
| Reviewer-focused architecture package reference | core to this proposal | It is the primary conditional semantic-method boundary. |
| Durable recording and governed settlement reference | core to this proposal | It separates side-effect procedure from review judgment. |
| Exact multi-target identity and retry | same-slice dependency | Safe recording and settlement cannot remain ambiguous after extraction. |
| Rule, literal, profile, and package-parity proof | same-slice dependency | Published skill behavior and generated resources require deterministic preservation evidence. |
| Architecture documentation correction | first-slice candidate | Update only if bounded assessment finds a stale flat-package inventory. |
| New review assets | out of scope | The current compact shapes do not justify extra package surface. |
| Generic review engine or shared cross-skill runtime | separate proposal | It would introduce architecture and ownership beyond this skill refactor. |
| Target-agent evaluation or separate manual semantic gate | out of scope | Existing deterministic proof and ordinary PR review are proportionate. |
