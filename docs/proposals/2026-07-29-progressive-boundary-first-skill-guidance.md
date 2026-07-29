<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/proposal/SKILL.md -->
<!-- Readability contract: use semantic source lines; keep stable IDs and tables for repeated proof or mapping structures. -->

# Progressive Boundary-First Skill Guidance

## Owning change record

[Progressive boundary-first skill guidance change record](../changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml)

## Problem

RigorLoop has one portable `boundary-first-v1` method shared by ten lifecycle skills.
That consistency prevents semantic drift, but the current resource shape makes every governed stage load the same full authoring and proof model even when the stage needs only a small approved slice.

The resulting user experience has two opposite failure modes:

```text
method is not named by the user
-> a skill may not consider it early enough
```

```text
full method is loaded everywhere
-> stages repeat the same model
-> artifacts and reviews become harder to understand
```

Boundary awareness should be ordinary engineering behavior.
Users should not need to know the internal method name.
At the same time, automatic boundary awareness should not cause every task to emit a formal eight-dimension record or enumerate every possible scenario.

The project needs progressive boundary guidance that keeps one authoritative model, applies a concise boundary scan automatically, loads formal details only for the stage families that own them, and lets downstream stages consume approved boundary and proof records without recreating them.

## Goals

- Make a concise boundary scan part of normal specification, inspection, implementation, and review behavior without requiring a method-name prompt.
- Preserve one shared boundary vocabulary and one authoritative feature-spec boundary record.
- Preserve the existing rule that examples illustrate behavior but do not define it.
- Keep formal boundary records conditional on active-contract adoption rather than creating them for every task.
- Separate compact common guidance from feature-contract authoring detail and proof-map detail.
- Let each lifecycle stage contribute only its stage-owned decision.
- Let downstream skills read the boundary and proof rows relevant to the current milestone, diff, or verification claim.
- Add scenarios only for distinct outcomes, material interactions, or demonstrated risks.
- Preserve project portability, deterministic resource projection, adapter parity, and structural-versus-semantic claim boundaries.
- Align validation ownership with the artifact being checked so published skill text is not routed through artifact-lifecycle validation.
- Keep stage-owned lifecycle consistency checks on governed artifacts and their owning change records.
- Refine the pending capability before atomic activation rather than introduce another boundary model version prematurely.

## Non-goals

- Do not create a second boundary vocabulary or independent per-skill models.
- Do not remove any of the eight `boundary-first-v1` dimensions from the formal applicability contract in this proposal.
- Do not weaken direct proof for applicable boundaries or selected interactions.
- Do not require every possible partition, interaction, or scenario combination.
- Do not create a standalone boundary artifact, boundary context packet, or duplicated downstream boundary table.
- Do not add a boundary lifecycle stage, centralized runtime service, live agent certification, or model-specific behavior gate.
- Do not make deterministic validators decide semantic applicability or completeness.
- Do not delete lifecycle validation for governed proposals, specs, test specs, architecture, ADRs, plans, change records, or their closeout relationships.
- Do not treat published skills or generated adapter skill bodies as lifecycle-managed artifacts.
- Do not activate `boundary-first-v1` as part of proposal authoring.
- Do not migrate or rewrite historical accepted feature specs.
- Do not hand-edit generated adapter skill bodies.

## Vision fit

fits the current vision

The proposal makes boundary reasoning easier to apply and easier to review while preserving a durable trace from requirements to proof and implementation.
It reduces repeated instruction and artifact cost without hiding decisions in chat, introducing a platform dependency, or weakening human review.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Users should not need to name boundary-first before skills consider boundaries | in scope | Goals, Recommended Direction |
| Specs, code inspection, implementation, and code review should cover key boundaries | in scope | Recommended Direction, Expected Behavior Changes |
| Boundary analysis should avoid excessive scenarios and unreadable results | in scope | Recommended Direction, Scenario-selection rule |
| Every related skill should not recreate or fully reload the same model | in scope | Recommended Direction, Stage-specific consumption |
| One shared boundary vocabulary should prevent semantic drift | in scope | Goals, Architecture Impact |
| Formal records should remain available for governed behavior changes | in scope | Recommended Direction |
| Downstream stages should consume approved boundary decisions by ID | in scope | Stage-specific consumption |
| Artifact-lifecycle checking is not useful for published skill text | in scope | Validation ownership, Expected Behavior Changes |
| Useful governed-artifact lifecycle safeguards should be removed with the skill-text check | rejected option | Non-goals, Option 6 |
| Runtime certification should prove semantic behavior automatically | out of scope | Non-goals |
| Existing historical specs should be rewritten into the refined shape | out of scope | Non-goals, Rollout and Rollback |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Automatic compact boundary scan | core to this proposal | Boundary awareness should not depend on user terminology. |
| One authoritative feature-spec model | core to this proposal | Downstream stages need stable ownership rather than repeated definitions. |
| Compact common boundary reference | core to this proposal | Every governed skill needs shared language without full authoring and proof detail. |
| Feature-contract authoring reference | first-slice candidate | `spec` and `spec-review` own formal applicability, definitions, interactions, and examples. |
| Proof-map reference | first-slice candidate | `test-spec` and `test-spec-review` own proof-record structure and adequacy. |
| Stage-specific artifact slicing | core to this proposal | Planning, implementation, review, and verification should read only relevant approved rows before expanding. |
| Canonical projection and resource-map changes | same-slice dependency | Published packages need deterministic, self-contained resources. |
| Skill and adapter validation changes | same-slice dependency | Resource presence, containment, and parity must remain fail-closed. |
| Remove artifact-lifecycle routing for published skill text | same-slice dependency | Skill text is a product instruction surface, not a lifecycle-state owner. |
| Stage-owned lifecycle resolution for governed artifacts | separate implementation slice | The stale embedded-status contract is a validator defect independent of boundary guidance and should be fixed and reviewed separately. |
| Prompt-independent and over-generation fixtures | same-slice dependency | The refinement must catch both missed boundaries and unnecessary formal expansion. |
| Boundary contract and skill-contract amendments | same-slice dependency | Current approved contracts require one full byte-identical reference in every governed skill. |
| Architecture and ADR assessment | same-slice dependency | Resource ownership, projection, packaging, and rollback cross several components. |
| Dynamic runtime certification | out of scope | It is not part of the portable published-skill capability. |
| Hard token or document-length gate | deferable follow-up | Baseline measurements should precede a release-blocking budget. |
| Formal contract-version increment | open question | Specification and architecture should decide whether the pending v1 resource refinement requires a version change. |

## Context

The accepted [Portable Boundary-First Capability for Published Skills](./2026-07-27-portable-boundary-first-capability-for-published-skills.md) selected one portable method, one-source deterministic projection, ten governed skills, and atomic prospective activation.
The approved [boundary-first proof model](../../specs/boundary-first-proof-model.md) assigns each governed skill a distinct responsibility but requires every skill to map the same full reference.

That baseline correctly separates semantic ownership:

```text
feature spec owns boundaries
-> test spec owns proof
-> plan owns sequencing
-> implementation realizes approved behavior
-> reviews challenge their own layer
-> verify closes the trace
```

The remaining problem is consumption.
The same reference currently contains the closed vocabulary, formal feature-record schema, example classification, interaction method, complete proof-map schema, audit procedure, validation distinction, and stop conditions.
Most downstream stages need the approved artifact rows and their own stage guidance, not the full instructions for authoring every upstream record.

The capability is still pending activation.
That creates an opportunity to refine the first active release without invalidating active `boundary-first-v1` artifacts or creating a second live method.

## Options Considered

### Option 0: Keep the current full shared reference

Every governed skill continues to package and load the same complete method when its current trigger applies.

This preserves the smallest repository diff and strongest byte-parity simplicity.
It does not solve prompt-dependent adoption, repeated context, or downstream reconstruction pressure.

Not recommended because the user-facing cost remains after the method becomes active.

### Option 1: Keep one full reference and improve trigger wording only

Skills automatically consider boundary-first for qualifying work, but every governed stage still loads the full reference.

This fixes the explicit-invocation problem with limited contract change.
It retains unnecessary authoring and proof detail in workflow, planning, implementation, code review, and verification invocations.

Not recommended as the complete solution.
The trigger correction is useful but does not address progressive consumption.

### Option 2: Use one compact core with stage-family references and artifact-sliced consumption

All governed skills share a compact common core.
Feature-contract authoring and review load a separate authoring reference.
Proof-map authoring and review load a separate proof reference.
Planning, implementation, code review, and verification consume exact approved artifact rows and use their existing stage-local skill instructions.
Any stage can expand to the compact core or upstream artifact when it discovers an unknown or escaped boundary.

Recommended because it preserves one semantic model while aligning loaded guidance with stage ownership.

### Option 3: Give every skill an independent boundary model

Each skill receives a custom vocabulary, record shape, and scenario method.

This can make individual skill files locally convenient.
It creates semantic drift, duplicated maintenance, incompatible identifiers, and ambiguous upstream ownership.

Rejected because consistency is more important than local duplication avoidance.

### Option 4: Generate a boundary context packet for each stage

A new derived artifact summarizes relevant boundary and proof rows for the next skill.

This can reduce repeated lookup.
It introduces another artifact whose freshness, ownership, validation, and disagreement behavior must be governed.

Rejected for the first slice because direct stable-ID reads from the feature spec, test spec, and plan already provide the necessary source chain.

### Option 5: Centralize boundary selection in a runtime service

A service classifies tasks, selects boundaries, and supplies each skill with a computed view.

This could support dynamic context optimization.
It conflicts with the portable, repository-local product boundary and introduces availability, versioning, trust, and recovery concerns.

Rejected because the improvement should remain usable from installed skills and project artifacts alone.

### Option 6: Delete artifact-lifecycle validation

Remove the artifact-lifecycle checker from every validation path.

This eliminates the stale embedded-status failure and reduces validation surface area.
It also removes useful safeguards for governed-artifact identity, terminal closeout, plan consistency, release evidence, and change-record relationships.

Rejected because the defect is incorrect checker ownership and a stale state source, not the existence of governed-artifact lifecycle validation.

## Recommended Direction

Choose Option 2.

Adopt a three-layer consumption model:

```text
always-on compact scan
-> formal stage-family guidance when the active contract requires it
-> exact approved artifact slices for downstream execution and review
```

### Always-on compact scan

Related lifecycle skills use four concise questions:

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

The scan is ordinary engineering reasoning.
It does not itself create formal boundary records, IDs, proof maps, or extra artifacts.
It does not depend on the user saying `boundary-first-v1`.

### Progressive formal guidance

The published capability is divided by ownership while preserving one semantic source set:

| Resource layer | Consumers | Content |
| --- | --- | --- |
| Compact common core | all governed skills when interpretation is needed | closed vocabulary, four-question scan, ID meaning, example ownership principle, interaction-selection principle, no-Cartesian rule, upstream-gap routing |
| Feature-contract authoring guidance | `spec`, `spec-review` | formal applicability, boundary definitions, selected interactions, example ownership, authoring and semantic-review rules |
| Proof-map guidance | `test-spec`, `test-spec-review` | proof obligations, coverage states, proof levels, automation modes, negative coverage, composed proof, adequacy review |
| Stage-local skill text | each owning stage | planning, implementation, review, verification, handoff, stop, mutation, and claim boundaries |

Canonical resources remain authored once and projected deterministically.
The exact source-file layout and resource names remain architecture decisions.

### Stage-specific consumption

Each stage reads only the information needed for its owned decision:

| Stage | Default boundary input | Stage-owned contribution |
| --- | --- | --- |
| `workflow` | marker, artifact pointers, unresolved gap identities | route to the correct owner |
| `spec` | compact core and feature-authoring guidance | define the authoritative boundary record |
| `spec-review` | complete feature boundary record and authoring guidance | judge applicability and semantic completeness |
| `plan` | approved boundary and interaction rows | assign milestones, dependencies, rollback units, affected surfaces, and proof timing |
| `plan-review` | plan mappings plus cited approved rows | judge isolation, sequencing, and recovery |
| `test-spec` | approved boundary and interaction rows plus proof guidance | define proof obligations |
| `test-spec-review` | proof map plus cited approved rows | judge proof adequacy |
| `implement` | current milestone IDs and their proof obligations | realize the approved slice |
| `code-review` | diff-related boundary, interaction, and proof IDs | detect implementation escapes and sibling-path omissions |
| `verify` | complete stable-ID trace | confirm final coherence once |

Downstream stages do not restate the full applicability table or redefine boundary outcomes.
They cite exact IDs and route newly discovered normative behavior to `spec`.

### Scenario-selection rule

Add a scenario only when it:

- proves a distinct observable outcome;
- crosses authority or trust;
- can leave partial or irreversible state;
- changes correctness through retry, replay, ordering, or concurrency;
- exercises a material public or sibling path;
- covers compatibility or external dependency behavior; or
- preserves a known incident or regression.

Stop adding scenarios when every applicable boundary and selected interaction has direct proof and another scenario would repeat an already-proven outcome.
A scenario that reveals a new normative outcome is a discovery routed upstream, not permission for a downstream stage to enlarge the contract.

### Automatic formal adoption

After capability activation, `spec` applies the formal method automatically for a new behavior-changing feature spec.
`spec-review` determines whether a changed grandfathered feature spec is substantively normative.
Existing marked artifacts continue to drive downstream stages by record identity.
Non-behavior work uses only the compact scan and does not create formal records.

Users are told concisely when formal boundary records were applied and why, but they are not asked to name or opt into a required method.

### Validation ownership

Published skill text is validated as a product instruction surface.
Canonical `skills/*/SKILL.md` changes use the existing skill-contract, skill-regression, deterministic projection, adapter, applicable boundary-first, and documentation-prose checks.
Generated adapter skill bodies remain reproducibility outputs rather than authored lifecycle artifacts.

The validation selector does not route a skill path to artifact-lifecycle validation merely to scan lifecycle wording.
If merge-dependent or mutable-state language in published skills remains worth checking, that rule belongs in the skill validator or a narrowly named governance-prose check with skill-specific fixtures and diagnostics.
It does not justify treating the skill as a lifecycle artifact.

Artifact-lifecycle validation remains responsible for governed proposals, specs, test specs, architecture documents, ADRs, plans, and related lifecycle relationships.
For a current `stage-owned-change-local-v1` artifact, it resolves mutable state from the exact normalized artifact entry in the owning `change.yaml`.
It does not require an embedded `## Status`, and it rejects newly introduced mutable lifecycle status in governed artifact content.
Historical artifacts outside the current contract may retain the legacy embedded-status behavior needed for compatibility.

This validator correction is delivered as a separate implementation slice from boundary-guidance changes.
The separation keeps the defect fix reviewable and allows the proposal branch to consume the corrected validator without combining unrelated implementation.

The existing-contract correction and the new selector policy have different gates:

- The embedded-status defect may proceed independently as a bug fix under approved `SLA-R013`, `SLA-R014`, and `SLA-R070`.
- Removing skill paths as an artifact-lifecycle selector source is new contributor-visible validation behavior governed by this proposal.
- The selector change follows amended feature contracts and `spec-review`, then the architecture, plan, and test-spec artifacts with their owning reviews; it is not part of the prerequisite bug fix.
- Boundary-guidance and selector implementation begin only after their shared architecture, plan, and test-spec gates settle.

## Expected Behavior Changes

- Equivalent requests behave consistently whether or not the user names `boundary-first-v1`.
- Related skills perform a concise boundary scan before making their stage-owned decision.
- New behavior-contract authoring applies the formal method automatically after atomic activation.
- Simple non-behavior work does not create an applicability table or proof map.
- `spec` and `spec-review` load formal feature-authoring guidance.
- `test-spec` and `test-spec-review` load formal proof guidance.
- Planning, implementation, code review, and verification begin from cited approved artifact rows rather than recreating the model.
- A stage expands its reads when an ID is missing, stale, ambiguous, or newly escaped.
- Scenario counts are driven by distinct outcomes and material hazards rather than possible combinations.
- Installed adapter packages remain self-contained and preserve deterministic resource identity.
- Published skill paths no longer select artifact-lifecycle validation solely for generic lifecycle-language warnings.
- Skill-specific checks continue to validate canonical skill quality, projection, packaging, and boundary guidance.
- Current governed artifacts obtain lifecycle state from their exact owning `change.yaml` entry rather than an embedded status section.
- Legacy lifecycle artifacts retain an explicit compatibility path instead of silently adopting current-contract behavior.

## Architecture Impact

This proposal affects the published-skill resource boundary and therefore needs architecture assessment.

Likely affected components are:

- the canonical boundary reference source under `specs/references/`;
- deterministic projection support under `scripts/`;
- resource maps and boundary guidance in the ten governed canonical skills;
- skill validation, boundary validation, adapter distribution tests, and fixtures;
- validation-selection ownership for canonical and generated skill paths;
- stage-owned artifact resolution in artifact-lifecycle validation as a separate prerequisite fix;
- `specs/boundary-first-proof-model.md`;
- `specs/skill-contract.md`;
- `specs/rigorloop-workflow.md`;
- the matching test specifications;
- generated local skill checks and release-archive parity.

The architecture should preserve:

- one canonical semantic source set;
- deterministic projection with no hand-edited copies;
- skill-root-relative resource containment;
- canonical, generated, packed, and installed parity for every mapped resource;
- feature specs as boundary owners and test specs as proof owners;
- no new durable boundary-summary artifact;
- no runtime, model, network, hosted-service, or workspace-interception dependency.

The architecture should decide the exact resource split, filenames, projection manifest, and rollback identity.

## Testing and Verification Strategy

The eventual test specification should cover both under-application and over-application.

Structural and packaging proof should establish:

- every governed skill maps exactly the resources required by its stage family;
- every mapped resource exists beneath the skill root;
- canonical resources project deterministically;
- generated, packed, and installed resources match their canonical owners;
- missing, additional, stale, unknown, or divergent mappings fail closed;
- downstream skills do not claim authoring ownership over feature or proof records.
- canonical and generated skill-only changes do not select artifact-lifecycle validation;
- the appropriate skill, projection, adapter, boundary, and prose checks remain selected.

Lifecycle-validator proof in the separate prerequisite slice should establish:

- a current stage-owned governed artifact without embedded `## Status` resolves its state from the exact owning change-record entry;
- mutable embedded lifecycle status is rejected for current-contract artifacts;
- a valid historical artifact can still use its explicitly supported legacy status contract;
- missing, duplicate, ambiguous, mismatched, or unknown ownership and state values fail closed;
- removing the skill-path route does not suppress lifecycle validation when a governed artifact or change record is also changed.

The final item is specification evidence for the later selector-policy slice.
It is not implemented as part of the existing-contract embedded-status correction.

Behavior-contract fixtures should establish:

- a new behavior-changing feature spec is routed to formal adoption after activation without a method-name prompt;
- a formatting-only or documentation-only change does not create a formal record;
- a substantive grandfathered revision is routed to `spec-review`;
- a simple formal record can mark most dimensions not applicable concisely;
- selected interactions come from requirement-owned hazards rather than a Cartesian product.

Stage-consumption fixtures should establish:

- `plan` maps approved IDs without redefining outcomes;
- `test-spec` maps proof without inventing IDs;
- `implement` consumes only the current milestone's governed slice before expanding;
- `code-review` checks diff-related public, sibling, failure, stale, and recovery paths;
- `verify` traces the complete chain without reapproving upstream semantics;
- an unknown or escaped boundary routes to its upstream owner.

Measurement should record before-and-after common-reference bytes, mapped-resource counts, and representative loaded-resource counts by stage family.
These measurements inform later budgets but do not become hard release gates in the first slice.

No live agent runtime is required to claim deterministic pass or fail.
Independent semantic review fixtures may challenge the guidance, but their results remain bounded review evidence rather than runtime certification.

## Rollout and Rollback

Refine the capability while repository activation remains `pending`.
Do not permit a feature spec to claim active formal adoption until the common core, stage-family resources, governed skill mappings, validators, generated output, adapter packages, and clean-install parity are current together.

Historical accepted specs remain valid.
Existing immutable released packages retain their shipped resource layout.
In-flight work follows the existing compatibility rules until the refined capability is atomically activated.

Rollback before activation restores the current single-reference mapping and projection rules.
Rollback after activation selects the immediately preceding immutable release through the existing read-only release metadata mechanism.
Rollback does not rewrite accepted feature specs, proof maps, plans, or historical release artifacts.

The validator prerequisite rolls back independently.
Restoring the prior skill-path selector route is safe but reintroduces a low-value generic warning.
Restoring the embedded-status requirement for current-contract artifacts is not a valid steady-state rollback because it conflicts with the approved stage-owned lifecycle contract; recovery instead reverts to the last validator version that correctly reads change-local state.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Splitting references creates semantic drift | Keep one canonical semantic source set, deterministic projections, explicit resource ownership, and parity validation. |
| The compact scan becomes vague advice | Use the same four stable questions across governed skills and fixture both expected detection and non-expansion cases. |
| Automatic adoption surprises users | Apply formal records only under the active contract and report the reason concisely without requesting redundant consent. |
| Skills classify the same work differently | Let `spec` own new adoption and `spec-review` own substantive-revision classification; downstream stages follow artifact identity. |
| Downstream slicing omits needed context | Require expansion on missing, stale, ambiguous, or escaped IDs and preserve full-read escape conditions. |
| Multiple resources increase packaging complexity | Extend existing resource manifests and canonical-to-installed parity checks rather than introducing a new packaging system. |
| Formal records remain verbose | Keep all eight applicability decisions concise, define only requirement-owned boundaries, and select interactions by distinct hazards. |
| Scenario reduction misses a material failure | Expand on authority, irreversible mutation, retry, sibling path, compatibility, external dependency, and incident triggers. |
| Validators overclaim semantic correctness | Preserve the structural-versus-semantic claim boundary and independent review ownership. |
| Removing lifecycle routing from skill paths hides useful skill defects | Preserve all skill-specific, projection, adapter, boundary, and prose checks; add selector regression coverage for the retained set. |
| A change contains both skills and governed artifacts | Select lifecycle validation from the governed artifact or change-record path, not from the skill path; regression-test mixed changes. |
| Stage-owned lookup binds an artifact to the wrong change | Normalize repository-relative paths, require exactly one owner, and fail closed on missing, duplicate, ambiguous, or mismatched entries. |
| Legacy artifacts lose compatibility | Keep legacy behavior explicit and bounded to artifacts outside the current stage-owned contract. |
| The refinement delays activation | Bound the first slice to guidance, resource ownership, projection, validation, and parity; defer hard budgets and runtime evaluation. |

## Open Questions

None block proposal review.

Specification and architecture should resolve:

- whether the pending `boundary-first-v1` semantic version remains valid when only resource composition and loading change;
- whether the current shared filename becomes the compact core or remains as a compatibility alias;
- the exact canonical paths and projection manifest for stage-family resources;
- the smallest artifact-slice lookup rules that remain portable when a project lacks RigorLoop-specific indexes;
- which static measurements provide a useful baseline before any hard context budget is proposed.

The validator-ownership direction is settled at proposal level.
The governing spec and validator design should define the exact legacy-detection rule and whether the generic lifecycle-language warning is retired or moved into a skill-focused checker.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-29 | Keep one authoritative boundary vocabulary and record model. | Multiple models would trade context savings for semantic drift. | Independent per-skill models |
| 2026-07-29 | Make concise boundary awareness automatic and prompt-independent. | Users should describe behavior, not internal method names. | Explicit method-name invocation |
| 2026-07-29 | Keep formal records conditional on active behavior-contract adoption. | Automatic awareness should not create universal artifact ceremony. | Formal records for every task |
| 2026-07-29 | Split compact common guidance from authoring and proof detail. | Stage families should load only the rules they own. | One full reference in every governed invocation |
| 2026-07-29 | Use stable-ID artifact slices downstream. | Approved specs and test specs already own the authoritative content. | Generated boundary context packets |
| 2026-07-29 | Select scenarios by distinct outcome and material hazard. | Possible combinations are unbounded and often prove no new behavior. | Cartesian scenario coverage |
| 2026-07-29 | Preserve deterministic packaging and semantic review boundaries. | Progressive loading must not weaken portability or correctness claims. | Runtime service or validator-owned semantics |
| 2026-07-29 | Refine before atomic activation. | The pending state allows a coherent first active release without historical migration. | Partial activation or immediate v2 fork |
| 2026-07-29 | Stop routing published skill text through artifact-lifecycle validation. | Skills do not own mutable artifact lifecycle state and already have purpose-built validation. | Keep the generic lifecycle-warning route |
| 2026-07-29 | Retain lifecycle validation for governed artifacts and make it stage-owned aware. | The current failure comes from a stale embedded-status source, while other governed-artifact safeguards remain valuable. | Delete the checker entirely |
| 2026-07-29 | Deliver the validator correction as a separate prerequisite slice. | A focused defect fix is easier to test, review, merge, and roll back than mixing it with boundary resource changes. | Combine validator implementation into the boundary-guidance slice |
| 2026-07-29 | Gate selector removal behind amended specifications and review. | Selector routing is contributor-visible validation behavior, while only the embedded-status correction is already specified. | Implement selector removal as part of the prerequisite bug fix |
| 2026-07-29 | Settle each lifecycle artifact through its owning review stage and create one test specification after the reviewed plan. | Feature contracts, architecture, plans, and proof maps have different owners; preserving their order prevents duplicate proof work and review-authority overlap. | Amend test specifications before architecture and planning, or settle them through `spec-review` |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-PBS-001` | Users do not need to name the method before qualifying skills consider key boundaries. |
| `AC-PBS-002` | One authoritative feature-spec record continues to own boundary definitions and outcomes. |
| `AC-PBS-003` | One authoritative test-spec proof map continues to own boundary and interaction proof obligations. |
| `AC-PBS-004` | All governed skills share compact vocabulary and routing rules without loading unrelated formal schemas by default. |
| `AC-PBS-005` | Feature-authoring and proof-authoring details are loaded only by their owning stage families. |
| `AC-PBS-006` | Downstream stages cite approved IDs and do not redefine upstream boundaries or proof obligations. |
| `AC-PBS-007` | Additional scenarios correspond to a distinct outcome, material interaction, or demonstrated risk. |
| `AC-PBS-008` | Simple non-behavior work does not create formal boundary artifacts. |
| `AC-PBS-009` | Unknown, stale, ambiguous, or escaped boundary ownership routes upstream. |
| `AC-PBS-010` | Canonical, generated, packed, and installed resources retain deterministic validated parity. |
| `AC-PBS-011` | Structural validators continue to avoid semantic-completeness claims. |
| `AC-PBS-012` | Activation remains atomic and historical accepted artifacts remain compatible. |
| `AC-PBS-013` | A canonical or generated skill-only change does not select artifact-lifecycle validation. |
| `AC-PBS-014` | Removing the skill-path lifecycle route preserves the skill, projection, adapter, applicable boundary-first, and prose checks owned by that surface. |
| `AC-PBS-015` | A current governed artifact resolves lifecycle state from exactly one normalized entry in its owning stage-owned change record and does not require embedded mutable status. |
| `AC-PBS-016` | Missing, duplicate, ambiguous, mismatched, or unknown stage-owned artifact state fails closed. |
| `AC-PBS-017` | Legacy embedded-status compatibility remains explicit and bounded, while mixed skill-and-governed-artifact changes still run lifecycle validation for the governed paths. |

## Next Artifacts

Independent existing-contract prerequisite:

- A separate bug-fix change may correct stage-owned artifact resolution under approved `SLA-R013`, `SLA-R014`, and `SLA-R070`.
- That bug fix does not remove skill paths from validation selection and does not implement boundary-guidance behavior.

If this proposal is accepted:

1. amend the boundary-first proof model, skill contract, workflow contract, and validation-selection feature contracts for every new behavior in `AC-PBS-001` through `AC-PBS-014` and the mixed-change portion of `AC-PBS-017`;
2. settle those feature contracts through independent `spec-review`;
3. create the architecture package for resource ownership, projection, packaging, selector composition, compatibility, and rollback, then settle it through `architecture-review`;
4. create a small-slice execution plan and settle it through `plan-review`;
5. create or amend one matching test specification from the approved feature contracts, architecture, and plan, including selector retention, mixed-change, prompt-independence, over-generation, packaging, and rollback proof, then settle it through `test-spec-review`;
6. implement skill-path selector removal and boundary-guidance behavior only after all preceding gates settle.

## Follow-on Artifacts

None yet

## Readiness

Proposal revisions after `PBS-PR1` and `PBS-PR2` are complete and ready for proposal-review R3.

The proposal selects one compact shared core, stage-family formal guidance, automatic prompt-independent boundary awareness, stable-ID artifact slicing, and hazard-driven scenario selection.
It preserves the existing semantic model, portability, deterministic packaging, independent review, and pending atomic activation boundary.
It also assigns published skill validation to purpose-built skill checks and retains stage-owned lifecycle validation only for governed artifacts and their change-record relationships.

The downstream artifact order now preserves one owner and one review gate per artifact:
feature contracts and `spec-review`, architecture and `architecture-review`, plan and `plan-review`, then one test specification and `test-spec-review`.
No test specification is authored before the reviewed plan, and `spec-review` does not settle test-spec content.

The independent validator prerequisite now resolves current artifact state from the owning change record and has separate regression evidence.
It corrects only already-approved stage-owned behavior.
Every new selector and published-skill behavior remains behind feature-contract review, architecture review, plan review, and the later test-spec review.
