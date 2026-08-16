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
- Bind every formal judgment to one exact review subject and complete governing basis independently from any settlement targets.
- Use finding-scoped and blocker-scoped target dispositions without introducing partial semantic approval.
- Persist a prepared settlement manifest before any target-state mutation and make partial physical recovery identity-bound.
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

### Shared recording compatibility

The exact `## Isolation and Recording` subsection remains inline in `SKILL.md` and byte-identical to the shared formal-review recording block. Its compatibility classification is closed:

| Property | Value |
| --- | --- |
| Classification | `normative-cross-skill-literal` |
| Normative owner | `specs/formal-review-recording.md` |
| Projection source | `templates/shared/review-isolation-and-recording.md` |
| Treatment | Preserve exactly |

The recording reference owns only architecture-review-specific placement, synchronization, settlement, retry, and automation procedure outside that shared block. It must not restate, paraphrase, or become a second owner of the shared isolation and recording contract.

Before editing, the literal inventory must capture the exact shared bytes and every consuming review skill. Any future change to the block requires one atomic amendment to the governing specification, projection template, all consuming review skills, and their validators; this simplification does not make such an amendment.

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

Loading this reference grants no settlement, automation, correction, or continuation authority. The main file owns whether durable recording is required, while this reference owns how the selected valid authority combination is executed. It must consume the inline shared isolation and recording contract without duplicating it.

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

artifact_settlement:
  none
  exact-target-set

execution_mode:
  manual
  workflow-managed-automated
```

`recording_mode: none` is valid only for non-formal review-like feedback that requests no durable status or evidence and produces no material or non-approval result. An explicit `architecture-review` request that asks for formal review status or lifecycle evidence is formal.

The first version permits only these combinations:

| Recording mode | Artifact settlement | Execution mode | Required behavior and handoff |
| --- | --- | --- | --- |
| `none` | `none` | `manual` | Return chat or result output only; perform no durable write or downstream continuation. |
| `advisory-durable` | `none` | `manual` | Write only to an explicitly authorized standalone review-evidence location; perform no lifecycle mutation or downstream continuation. |
| `formal-lifecycle` | `none` | `manual` | Write formal review evidence and required review-log or review-resolution evidence; settle no artifact and remain isolated. |
| `formal-lifecycle` | `exact-target-set` | `manual` | Write formal review evidence and settle only the validated exact target set; remain isolated and report the possible next stage without invoking it. |
| `formal-lifecycle` | `none` | `workflow-managed-automated` | Write formal review and automation evidence, settle no artifact, and return the blocked or record-only result to `workflow`. |
| `formal-lifecycle` | `exact-target-set` | `workflow-managed-automated` | Write formal review and automation evidence, settle only the validated exact target set, and return control to `workflow`. |

Every unlisted combination is invalid and stops before recording, settlement, automation evidence, or handoff. In particular, automation never runs with `none` or `advisory-durable`, and artifact settlement never runs without `formal-lifecycle` recording.

`advisory-durable` requires an explicit valid user-provided evidence path or a project-local standalone advisory location authorized by workflow guidance. When neither location resolves safely, return the complete judgment and findings with `recording_status: blocked`; do not create a governed change root, formal review log, review resolution, lifecycle entry, or continuation authority.

The permitted side effects are also closed:

| Authority combination | Standalone evidence | Formal record and log | Review resolution when triggered | Exact artifact transition | Automation packet or receipt | Workflow routing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| None/manual | no | no | no | no | no | no |
| Advisory/manual | yes | no | no | no | no | no |
| Formal record-only/manual | no | yes | yes | no | no | no |
| Formal target-set/manual | no | yes | yes | yes | no | no |
| Formal record-only/automated | no | yes | yes | no | yes | no |
| Formal target-set/automated | no | yes | yes | yes | yes | no |

Resource loading and authority remain separate:

```text
loaded resources determine available procedure
recording mode and artifact settlement determine permitted writes
execution mode determines permitted automated branches and return behavior
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

The primary procedural acceptance surfaces are `ARR1-recorded` and `ARR1M-recorded-method`, because every formal review loads the recording reference and canonical or ADR review also loads the method reference. Manual and workflow-managed automated executions may share a loaded assembly, but their distinct authority and handoff semantics require separate static fixtures. Informal feedback may be measured but must not be used as the sole simplification success surface.

Late discovery of package-method or durable-recording context must load the required reference before dependent judgment, recording, status, or settlement. Each reference loads at most once.

### Review subject, governing basis, and settlement targets

Every formal review occurrence binds three separate identities:

```text
review subject:
  primary review surface
  stable subject ID and kind
  ordered source paths and content identities

governing basis:
  governing specification path and identity
  approving spec-review identity
  architecture-assessment receipt identity when applicable
  accepted proposal or decision basis when relevant
  architecture-method contract path and identity
  repository revision

settlement targets:
  ordered artifact IDs
  target kinds and normalized paths
  target content identities
  authoring-evidence identities
```

The review occurrence also binds its review ID, round, review record, and review-log path. A canonical package subject includes its architecture Markdown, linked diagram sources, related ADRs, and governing basis. Related ADRs remain distinct optional settlement targets. A standalone ADR subject includes the exact ADR, its current canonical architecture linkage, and governing basis. A canonical update with related ADRs uses `canonical-architecture-update` as the primary surface and includes every reviewed source in one ordered subject identity.

No-impact rationale binds the exact architecture-assessment receipt and exact proposal or specification basis used by the rationale. Proposal/spec-gap review binds the exact proposal or specification identities and the architecture question or conflict being reviewed. These record-only surfaces have an exact review subject but an empty settlement-target set. A direct formal record-only review whose stable subject identity cannot be resolved reports blocked recording or remains advisory; it must not create an identity-free formal occurrence.

The first version retains one semantic review status for the exact review subject. It does not introduce partial semantic approval. A finding against any required source or settlement target prevents the complete subject from receiving an approved occurrence.

No-impact rationale and proposal/spec-gap review are always review-evidence-only in the first version. They never settle an architecture or ADR entry, and they must not invent a rationale artifact, artifact kind, lifecycle entry, schema, or settlement target. Workflow remains the owner of architecture assessment and routing decisions derived from those results.

Artifact settlement is available only for an exact target set of canonical architecture packages and ADRs whose governed entries already exist at `review-required`. Every target must match its artifact ID, normalized path, current content identity, authoring-evidence identity, reviewed repository revision, target kind, and governing basis. A missing, stale, ambiguous, conflicting, or differently ordered target blocks the complete settlement attempt.

A prior judgment may be reused only when the review subject identity, complete governing-basis identity, ordered settlement-target identity, review status, review ID, and round all match. A changed specification, approving spec review, assessment receipt, accepted decision basis, architecture-method contract, repository revision, or target identity requires a new review occurrence even when architecture file bytes are unchanged.

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

An approved judgment with blocked recording does not complete formal review. A valid identical retry may finish recording or settlement using one exact prior judgment without rerunning semantic review or creating duplicate records. A retry must stop if the subject, governing basis, repository revision, target set, identity, authority, status, review ID, or round changed.

For governed multi-target settlement, write the durable review record, findings, review log, and required review resolution first. Then persist the complete prepared settlement manifest before mutating any target. Settle only the exact ordered target set. An interruption may leave an identity-proven partial settlement that an identical retry completes, but the invocation cannot claim settled review until the manifest is complete. Unrelated artifact entries, milestone state, and workflow routing remain unchanged.

Architecture-review retains one semantic status for the complete ordered subject. Target settlement is finding-scoped and blocker-scoped. Every material finding identifies its affected target IDs, and every blocking result uses exactly one scope: `review-occurrence`, `target-set`, or `target:<artifact-id>`.

Use this deterministic target-disposition mapping:

| Overall review status | Target scope | Required target result |
| --- | --- | --- |
| `approved` | Every required target | Transition canonical architecture to `approved`; transition each ADR to the intended `accepted` or `active` state recorded by current authoring evidence. Missing or ambiguous intended state blocks the complete settlement. |
| `changes-requested` | Targets named by material findings | Transition affected targets to `revision-required`; leave every unaffected target at `review-required`. |
| `blocked` | Target-scoped blockers | Transition only named blocked targets to `blocked`; leave unaffected targets at `review-required`. |
| `blocked` | Target-set blocker | Transition every target to `blocked` only when the evidence establishes a genuinely target-set-wide blocker. |
| `blocked` | Review-occurrence blocker | Perform no target settlement. |
| `inconclusive` | Default | Perform no target settlement and leave every target at `review-required`. |
| Any recording or authority failure | Any | Perform no target settlement. |

An overall status other than `approved` grants no target approval and no downstream architecture-review eligibility. Leaving an unaffected target at `review-required` is not partial approval; the target remains unsettled and participates in the complete rereview.

### Prepared settlement manifest

The complete settlement manifest is durable on the existing formal-review evidence surface before any canonical architecture or ADR entry is transitioned. It binds:

```text
manifest ID and state
review ID and round
review subject identity
governing-basis identity
ordered settlement-target identity
per target:
  artifact ID, kind, path, and content identity
  authoring-evidence identity
  validated pre-state
  finding or blocker disposition
  expected post-state
  settlement progress
```

Manifest states are `prepared`, `partial`, `complete`, or `blocked`. The write protocol is closed:

1. Complete semantic judgment.
2. Write the exact review record and findings.
3. Synchronize the review log and required review resolution.
4. Persist the complete `prepared` settlement manifest.
5. Re-read `change.yaml`, authority, governing basis, and all target identities.
6. Compare-and-set targets in manifest order.
7. Record or verify each target's completion against the same manifest.
8. Finalize the manifest as `complete`.
9. Report `settled`.

A physical interruption after some exact target writes produces only `partial-retry-required`, never partial semantic approval or downstream eligibility. Retry reuses the same review ID, round, semantic judgment, subject identity, governing-basis identity, manifest identity, ordered targets, target identities, authoring-evidence identities, pre-states, dispositions, and expected post-states. It completes only pending matching writes and stops on any changed identity, state, order, basis, authority, or concurrency evidence. A changed subject, basis, target set, or manifest requires a new review occurrence rather than retry adoption.

### Resource failure behavior

If the package-review reference is required but missing, unreadable, escaped, contradictory, or mixed-version, stop before a canonical-package or ADR verdict. Do not reconstruct detailed method from memory.

If the recording-and-settlement reference is required but unavailable, preserve the complete semantic findings in the invocation result, report `recording_status: blocked`, and claim neither formal completion nor lifecycle settlement. Missing untriggered resources do not block another profile.

### Output behavior

Retain the current compact result fields and simple finding shape inline. The result must distinguish review surface, review status, recording status, settlement result, exact targets, material findings, blockers, required canonical or ADR updates, next stage, and claim limitations.

For a retry that performs no new semantic review, report the safely reused review ID and status separately from the retry transaction result. Do not manufacture a new review round or status.

## Proposal Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-ARRSIM-001` | The exact shared `## Isolation and Recording` block remains inline and byte-identical to its normative projection. |
| `AC-ARRSIM-002` | The recording reference owns only architecture-review-specific mechanics outside the shared block. |
| `AC-ARRSIM-003` | Recording mode, artifact settlement, and execution mode have one exhaustive valid-combination matrix. |
| `AC-ARRSIM-004` | Every valid combination has explicit write, settlement, automation-evidence, isolation, and handoff behavior. |
| `AC-ARRSIM-005` | Every unlisted or contradictory authority combination stops before side effects. |
| `AC-ARRSIM-006` | No-impact rationale and proposal/spec-gap reviews always remain review-evidence-only. |
| `AC-ARRSIM-007` | Governed settlement requires exact existing canonical architecture or ADR entries and matching authoring evidence. |
| `AC-ARRSIM-008` | Canonical architecture and ADR target dispositions are deterministic and evidence-scoped for every review status. |
| `AC-ARRSIM-009` | Interrupted physical settlement supports only exact `partial-retry-required` reconciliation and never partial semantic approval. |
| `AC-ARRSIM-010` | The `ARR1-recorded` and `ARR1M-recorded-method` loaded words and UTF-8 bytes decrease from their baselines without semantic loss. |
| `AC-ARRSIM-011` | Acceptance uses deterministic repository proof and ordinary PR review, with no target-agent runtime or separate manual semantic gate. |
| `AC-ARRSIM-012` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-ARRSIM-013` | Review subject, governing basis, and settlement targets are represented separately. |
| `AC-ARRSIM-014` | Every formal review binds one exact governing specification and architecture-method basis. |
| `AC-ARRSIM-015` | No-impact and proposal/spec-gap surfaces bind exact review subjects but have no settlement targets. |
| `AC-ARRSIM-016` | A changed specification, spec review, assessment receipt, decision basis, method identity, or repository revision invalidates judgment reuse. |
| `AC-ARRSIM-017` | One overall semantic status remains authoritative for the complete review subject. |
| `AC-ARRSIM-018` | A non-approved review never approves an individual target or grants downstream eligibility. |
| `AC-ARRSIM-019` | `changes-requested` transitions only finding-affected targets to `revision-required`. |
| `AC-ARRSIM-020` | `inconclusive` performs no target settlement by default. |
| `AC-ARRSIM-021` | Every blocker records `review-occurrence`, `target-set`, or exact target scope. |
| `AC-ARRSIM-022` | A complete prepared settlement manifest is durable before target writes. |
| `AC-ARRSIM-023` | The manifest records pre-state, disposition, expected post-state, and per-target progress. |
| `AC-ARRSIM-024` | Partial retry reuses the exact subject, basis, manifest, review ID, and round. |
| `AC-ARRSIM-025` | Changed or concurrent target state blocks retry rather than being adopted. |
| `AC-ARRSIM-026` | Architecture becomes required when existing formal-review evidence cannot support the prepared-manifest contract. |
| `AC-ARRSIM-027` | Advisory durable recording without an authorized location reports blocked and creates no governed state. |
| `AC-ARRSIM-028` | No target-agent runtime executes during acceptance. |

## Expected Behavior Changes

- No-impact and upstream-gap review no longer load the detailed canonical package and ADR checklist.
- Canonical and ADR review load one reviewer-focused method reference rather than keeping the complete checklist inline.
- Durable recording and lifecycle settlement load one independent procedure and do not become implied by package-method loading.
- Combined canonical-plus-ADR reviews bind one exact ordered target set and cannot settle unrelated or ambiguous targets.
- Every formal judgment binds an exact subject and governing basis even when it has no settlement targets.
- No-impact rationale and proposal/spec-gap reviews never settle lifecycle artifacts.
- Manual and workflow-managed automated executions use the same closed authority matrix but retain different isolation and return behavior.
- Non-approved reviews mutate only targets supported by finding-scoped or blocker-scoped evidence; `inconclusive` leaves targets unsettled by default.
- Multi-target settlement persists a prepared manifest before writes and records per-target progress for exact recovery.
- Identical recording or settlement retries reuse one exact judgment without duplicate semantic review evidence.
- Missing triggered procedure fails closed at the dependent claim boundary.
- Review surfaces, statuses, severity, material-finding obligations, lifecycle ownership, and workflow handoff remain behaviorally unchanged.

## Architecture Impact

The expected bounded assessment is provisionally `architecture-not-required`. The design uses the existing published-skill package model, existing formal-review evidence, existing artifact entries, existing authoring evidence for the intended ADR accepted state, and existing review settlement ownership. It adds no rationale artifact, service, runtime router, persistence mechanism, lifecycle state, dependency, or independent policy owner.

A documentation-only architecture update is appropriate only if the current architecture package inventory depicts `architecture-review` as permanently flat or lists an exact resource inventory that becomes stale.

The bounded assessment must confirm that current formal-review evidence can represent the complete governing basis, target dispositions, expected states, and per-target settlement progress before retaining `architecture-not-required`. Architecture becomes required if exact multi-target retry needs a new persisted transaction record, review schema, lifecycle state, or write owner. The implementation must not weaken recovery merely to preserve the expected no-architecture result.

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
- exact subject identity, complete governing basis, record-only subject identity, stale decision input, ambiguous target, and conflicting authoring evidence;
- every valid recording, artifact-settlement, and execution combination plus representative invalid combinations;
- isolated manual versus workflow-managed automated return behavior and forbidden workflow routing;
- clean, material, blocked, and inconclusive outcomes;
- no-impact credibility and upstream proposal/spec routing with no artifact settlement;
- finding-scoped and blocker-scoped canonical architecture and ADR dispositions for every review status, including unaffected targets and missing or ambiguous intended ADR state;
- prepared manifest durability before writes, per-target completion, identical retry, exact partial settlement, changed-basis or changed-target rejection, review-ID collision, and concurrent change;
- missing triggered and untriggered references;
- forbidden edits to reviewed artifacts, unrelated entries, milestone state, or routing;
- byte-identical shared recording-block projection and absence of a duplicate reference-owned copy;
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
- Risk: Extracting recording procedure could alter the normative cross-skill isolation and recording literal. Mitigation: preserve the shared block byte-identically inline, classify it explicitly, and validate it against the shared projection.
- Risk: A shorter common file could omit no-impact or proposal/spec-gap safety. Mitigation: keep the compact impact scan and upstream routing inline and prove both as core-only scenarios.
- Risk: Authority modes could combine into an unintended write path. Mitigation: permit only the six enumerated combinations, define their side effects, and stop every unlisted combination.
- Risk: Combined target settlement could widen architecture-review authority. Mitigation: make rationale and gap surfaces unconditionally record-only, bind one ordered exact canonical/ADR target set, apply deterministic evidence-scoped dispositions, forbid partial semantic approval, and preserve every unrelated state surface.
- Risk: A prior judgment could be reused after its specification, assessment, or architecture-method basis changes. Mitigation: bind one complete governing-basis identity and require a new review occurrence on any decision-bearing change.
- Risk: One overall non-approval status could over-mutate unaffected targets. Mitigation: keep one semantic status while using finding-scoped and blocker-scoped dispositions, leaving unsupported targets at `review-required`.
- Risk: Interrupted settlement could reconstruct intended writes from mutable current state. Mitigation: persist the full prepared manifest and per-target progress before mutation and reconcile only its exact identity.
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
| 2026-08-16 | Preserve the shared isolation and recording block byte-identically inline. | The block is a normative cross-skill literal, while only architecture-review-specific procedure belongs in the new recording reference. | Moving or paraphrasing the shared block in the reference. |
| 2026-08-16 | Permit only six explicit recording, settlement, and execution combinations. | An exhaustive authority matrix prevents loading a procedure from being mistaken for write, automation, or continuation authority. | Independent axes without valid-combination and side-effect closure. |
| 2026-08-16 | Make no-impact and proposal/spec-gap surfaces unconditionally record-only and settle only exact canonical architecture or ADR entries. | No approved rationale artifact lifecycle exists, and exact existing targets provide the narrowest safe settlement boundary. | Inventing rationale entries, implicit settlement, or partial semantic approval. |
| 2026-08-16 | Separate review subject, governing basis, and settlement targets. | Record-only surfaces still need durable identity, while changed decision-bearing inputs must invalidate judgment reuse independently from artifact bytes. | Treating settlement targets as the entire review identity. |
| 2026-08-16 | Keep one overall status but use finding-scoped and blocker-scoped target dispositions. | This avoids unsupported mutation of unaffected targets without introducing partial semantic approval. | Applying every non-approval result to every target or introducing per-target approval. |
| 2026-08-16 | Persist a prepared settlement manifest before target writes. | Exact crash recovery requires durable pre-state, intended post-state, disposition, and progress for every target. | Reconstructing retry intent from overall status and current mutable state. |

## Next Artifacts

- Focused `architecture-review` skill-contract specification.
- Bounded architecture assessment with expected result `architecture-not-required`.
- Execution plan with preservation inventory, package implementation, and measurement/parity milestones.
- Test specification mapping review surfaces, profiles, identity, recording, settlement, recovery, resource failure, and package parity.

## Follow-on Artifacts

None yet

## Readiness

Revised for independent proposal rereview. This proposal does not claim acceptance, specification readiness, architecture settlement, implementation readiness, verification, or PR readiness.

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
