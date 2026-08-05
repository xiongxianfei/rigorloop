<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/spec/SKILL.md -->
<!-- Readability contract: use semantic source lines; keep stable IDs and tables for repeated proof or mapping structures. -->

# Progressive Boundary-First Skill Guidance

## Owning change record

[Progressive boundary-first skill guidance change record](../docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml)

## Related proposal

[Progressive Boundary-First Skill Guidance](../docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md)

## Goal and context

This spec refines how the pending `boundary-first-v1` capability is triggered,
packaged, loaded, consumed, and validated.

The feature makes a compact boundary scan ordinary behavior for the ten
governed lifecycle skills without requiring the user to name the method.
It keeps formal feature and proof records conditional, preserves one
authoritative semantic model, and prevents downstream stages from recreating
upstream boundary decisions.

This spec is a focused amendment to:

- [Boundary-First Proof Model](boundary-first-proof-model.md);
- [Skill Contract](skill-contract.md);
- [RigorLoop Workflow](rigorloop-workflow.md); and
- [Test Layering and Change-Scoped Validation](test-layering-and-change-scoped-validation.md).

On approval, `PBS-R001` through `PBS-R038` govern the refined behavior.
They supersede conflicting full-reference, explicit-trigger, and skill-path
artifact-lifecycle-selection clauses in those contracts.
All non-conflicting requirements remain in force.

| Existing contract surface | Relationship to this spec |
| --- | --- |
| `boundary-first-proof-model.md` `PBF-R042`, `PBF-R046` through `PBF-R048` | Amended by `PBS-R012` through `PBS-R016` and `PBS-R032` through `PBS-R034`; one full reference in every governed skill becomes one compact core plus only the stage-family resources each skill owns. |
| `skill-contract.md` `R57` through `R60` | Amended by `PBS-R012` through `PBS-R016` and `PBS-R032` through `PBS-R034`; deterministic mapping and parity remain, but the resource inventory becomes stage-family-specific. |
| `rigorloop-workflow.md` `R28` | Extended by `PBS-R005` through `PBS-R011`; the compact scan is prompt-independent, while formal record adoption remains active-only. |
| `test-layering-and-change-scoped-validation.md` `R8` through `R8c`, `R11`, and `R11a` | Preserved and clarified by `PBS-R025` through `PBS-R030`; skill checks remain, and lifecycle validation remains scoped to actual lifecycle-managed paths. |

The published capability is still `pending`.
This spec therefore does not carry the activation marker or claim active
formal adoption.

## Glossary

- `compact scan`: Four short questions used to identify outcome-changing
  inputs or actors, state or timing, public or alternate paths, and failure or
  compatibility conditions.
- `compact core`: The portable shared resource containing the closed boundary
  vocabulary, compact scan, stable-ID meaning, example-ownership rule,
  interaction-selection rule, no-Cartesian rule, and upstream-gap routing.
- `feature-authoring guidance`: The portable resource used by `spec` and
  `spec-review` to author or judge formal applicability, boundaries,
  interactions, invariants, outcomes, and example ownership.
- `proof guidance`: The portable resource used by `test-spec` and
  `test-spec-review` to author or judge proof obligations and adequacy.
- `qualifying invocation`: A governed-skill invocation whose decision can
  change observable behavior or whose inputs already cite an active boundary
  contract, boundary ID, interaction ID, or proof obligation ID.
- `formal adoption`: Creation or maintenance of the normalized feature-spec
  boundary record and matching test-spec proof record under an active
  `boundary-first-v1` contract.
- `artifact slice`: The exact approved boundary, interaction, plan, or proof
  rows cited by stable IDs for the current stage decision.
- `expansion trigger`: A missing, stale, unknown, ambiguous, conflicting, or
  escaped ID or outcome that requires reading more approved context or routing
  to the owning stage.
- `distinct outcome`: An observable success, failure, stale, interrupted,
  recovery, compatibility, authority, or stop result not already proved by
  another scenario.
- `published skill text`: Canonical skill instructions and their generated or
  packaged projections; it is a product instruction surface rather than a
  lifecycle-managed artifact.

## Examples first

### Example E1: the user does not name the method

Given a user asks `spec` to define behavior for a retryable operation
And the user does not mention `boundary-first-v1`
When `spec` evaluates the request
Then it performs the compact scan
And, after capability activation, it authors the required formal boundary
record without asking the user to name or opt into the method.

### Example E2: non-behavior work stays concise

Given a user asks a governed skill for a spelling-only documentation change
When the skill performs the compact scan
Then it creates no applicability table, boundary IDs, proof map, or additional
scenario inventory
And it continues under the skill's ordinary stage contract.

### Example E3: downstream implementation consumes a slice

Given an approved spec and test spec define several boundary and proof rows
And the current plan milestone cites two boundary IDs and their proof
obligations
When `implement` begins that milestone
Then it reads the cited rows first
And it does not reconstruct the full applicability model.

### Example E4: a material sibling path adds proof

Given a public entry point and a sibling entry point can produce different
failure behavior
When `test-spec` selects scenarios
Then it adds proof for the distinct sibling-path outcome
And it does not generate unrelated combinations of all dimensions.

### Example E5: skill-only validation is purpose-built

Given the changed set contains only canonical governed skill text
When the validation selector evaluates the changed paths
Then it selects the applicable skill, boundary, projection, and adapter checks
And it does not select `artifact_lifecycle.validate` for the skill path.

### Example E6: a mixed change retains lifecycle validation

Given the changed set contains governed skill text and a feature spec
When the validation selector evaluates the changed paths
Then the skill path receives its purpose-built checks
And the feature-spec path receives `artifact_lifecycle.validate`
And removing lifecycle selection from the skill path does not remove it from
the governed artifact.

## Requirements

### Contract relationship and activation

PBS-R001. This spec MUST amend only the trigger, resource-consumption,
stage-slicing, scenario-selection, selector-ownership, projection, and
compatibility behavior stated here.
Non-conflicting requirements in the four related contracts MUST remain valid.

PBS-R002. The refined semantic contract version MUST remain
`boundary-first-v1`.
Splitting or progressively loading resources MUST NOT create a second boundary
vocabulary, identifier grammar, applicability model, feature record, or proof
record.

PBS-R003. The capability MUST remain `pending` until the compact core,
stage-family resources, governed skill mappings, deterministic projections,
validators, generated output, package archives, and clean-install evidence are
current together.

PBS-R004. While capability state is `pending`, a new or revised feature spec
MUST NOT claim active formal adoption solely because it uses this refinement
spec.

PBS-R005. After capability state becomes `active`, a new behavior-changing
feature spec MUST adopt the formal method automatically.
A user MUST NOT be required to name `boundary-first-v1` or provide a separate
opt-in.

PBS-R006. After activation, `spec-review` MUST classify whether a changed
grandfathered feature spec is substantively normative according to the
existing boundary-first compatibility contract.
An undecidable classification MUST block review.

### Compact scan and formalization

PBS-R007. Every governed skill MUST apply this compact scan before making a
qualifying stage-owned decision:

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can
   change the outcome?

PBS-R008. The compact scan MUST NOT by itself create formal boundary records,
IDs, proof maps, new artifacts, or a user-visible scenario inventory.

PBS-R009. An invocation that is non-behavioral and has no active boundary,
interaction, or proof identity MUST continue without formal adoption after the
compact scan finds no outcome-changing condition.

PBS-R010. When a qualifying invocation cites an active boundary contract or
stable boundary, interaction, or proof IDs, the governed skill MUST follow
those identities without requiring the user to repeat the method name.

PBS-R011. Users MUST receive a concise explanation when a formal boundary
record is created or an upstream boundary gap blocks progress.
The workflow MUST NOT request redundant consent for method application already
required by the active contract.

### Progressive resource ownership

PBS-R012. The portable semantic source set MUST contain exactly these logical
resource layers:

| Resource layer | Required consumers | Owned content |
| --- | --- | --- |
| compact core | all ten governed skills | closed vocabulary, compact scan, stable-ID meaning, example rule, interaction rule, no-Cartesian rule, upstream-gap routing |
| feature-authoring guidance | `spec`, `spec-review` | formal applicability, boundary definitions, interactions, invariants, outcomes, example ownership, semantic authoring and review |
| proof guidance | `test-spec`, `test-spec-review` | proof obligations, coverage states, proof levels, automation modes, negative and composed proof, adequacy review |
| stage-local skill text | its owning skill | stage decision, artifact mutation, stop conditions, review authority, handoff, and claim boundaries |

PBS-R013. Architecture MUST select exact canonical filenames, resource-map
entries, projection metadata, and compatibility aliases while preserving the
logical ownership in `PBS-R012`.

PBS-R014. Every governed skill package MUST contain the compact core.
`spec` and `spec-review` MUST additionally contain feature-authoring guidance.
`test-spec` and `test-spec-review` MUST additionally contain proof guidance.
No other governed skill MUST be required to package feature-authoring or proof
guidance.

PBS-R015. Resource maps MUST use the existing allowed resource verbs and MUST
state a stage-specific load condition.
A missing required mapped resource, unknown layer, additional unowned layer,
or path escaping the skill root MUST fail closed.

PBS-R016. The compact scan MAY be expressed directly in stage-local skill text
so that deciding whether deeper context is needed does not require loading the
formal authoring or proof resources.

### Stage-specific artifact consumption

PBS-R017. Stage responsibilities MUST remain:

| Stage | Default approved input | Stage-owned contribution |
| --- | --- | --- |
| `workflow` | contract marker, artifact pointers, unresolved gap identities | route to the owning stage |
| `spec` | compact core and feature-authoring guidance | own the formal feature boundary record |
| `spec-review` | complete feature record and authoring guidance | judge semantic completeness |
| `plan` | approved boundary and interaction rows | assign milestones, dependencies, affected surfaces, rollback units, and proof timing |
| `plan-review` | plan mappings and cited approved rows | judge isolation, sequencing, dependencies, and recovery |
| `test-spec` | approved boundary and interaction rows plus proof guidance | own proof obligations |
| `test-spec-review` | proof map and cited approved rows | judge proof adequacy |
| `implement` | current milestone IDs and proof obligations | realize the approved slice |
| `code-review` | diff-related boundary, interaction, and proof IDs | detect escapes and omitted material paths |
| `verify` | complete stable-ID trace | confirm final coherence |

PBS-R018. `plan`, `plan-review`, `implement`, `code-review`, and `verify` MUST
begin with the exact artifact slice cited for their current decision.
They MUST NOT recreate the full applicability table, redefine outcomes, or
rename upstream IDs.

PBS-R019. A downstream stage MUST expand its approved reads when an ID is
missing, stale, unknown, ambiguous, conflicting, or newly escaped, or when the
cited slice cannot explain an observed outcome.

PBS-R020. If expansion discovers a new normative outcome or changes an
existing outcome, the downstream stage MUST stop and route the gap to `spec`.
If it discovers a missing proof obligation without changing behavior, it MUST
route the gap to `test-spec`.

### Scenario selection

PBS-R021. A scenario MUST be added when it proves at least one of:

- a distinct observable outcome;
- an authority or trust crossing;
- partial or irreversible state;
- retry, replay, ordering, concurrency, or idempotency behavior;
- a material public, helper, sibling, alternate, or bypass path;
- compatibility, migration, rollback, or external dependency behavior; or
- a named incident or regression.

PBS-R022. Scenario selection MUST stop when every applicable boundary and
selected interaction has direct proof and another scenario would repeat an
already-proved outcome without covering a trigger in `PBS-R021`.

PBS-R023. No stage or validator MUST require a Cartesian product of
dimensions, partitions, boundaries, interactions, or scenario inputs.

PBS-R024. A scenario that exposes behavior not owned by an approved
requirement MUST be recorded as a discovery and routed upstream.
It MUST NOT silently enlarge the contract.

### Validation selection and claim boundaries

PBS-R025. A canonical or generated published skill path MUST NOT select
`artifact_lifecycle.validate` solely because it is skill text or contains
lifecycle-related wording.

PBS-R026. A canonical governed skill change MUST continue to select
`skills.validate`, `skills.regression`, and `skills.drift`.
It MUST select applicable boundary-reference, boundary-validation, projection,
and adapter checks when the changed surface can affect them.

PBS-R027. A selector or selector-test change implementing this policy MUST
select `selector.regression`.

PBS-R028. A lifecycle-managed proposal, feature spec, test spec, architecture
document, ADR, plan, or matching change record MUST continue to select its
applicable artifact-lifecycle and change-metadata checks.

PBS-R029. For a mixed changed set, removing
`artifact_lifecycle.validate` from skill paths MUST NOT remove or narrow the
check for lifecycle-managed paths in the same set.
The check's affected paths MUST contain only paths owned by that check.

PBS-R030. If lifecycle-like wording in published skills remains governed, it
MUST be checked by `skills.validate` or a narrowly named skill/governance-prose
check with skill-specific fixtures and diagnostics.
Such a check MUST NOT claim lifecycle settlement.

PBS-R031. Deterministic validation MUST prove only structure, closed values,
resource mapping, containment, projection, selected-check routing, and package
parity.
It MUST NOT claim semantic applicability, completeness, scenario adequacy,
proof adequacy, implementation fidelity, or final coherence.

### Projection, compatibility, and recovery

PBS-R032. Each logical resource layer MUST have one canonical authored owner.
All skill-local, generated, packed, and installed copies MUST be deterministic
projections and MUST NOT be hand-edited.

PBS-R033. Projection and package validation MUST fail closed on a missing,
additional, stale, mixed-version, path-divergent, or byte-divergent required
resource at any governed canonical, generated, packed, or installed layer.

PBS-R034. Activation MUST remain atomic across the compact core,
stage-family resources, all ten governed skills, supported adapter archives,
and clean installed targets.
Partial progressive-resource activation MUST fail closed.

PBS-R035. Existing accepted feature specs, proof maps, plans, and immutable
released packages MUST remain valid under the existing grandfathering and
compatibility rules.
This refinement MUST NOT require historical artifact rewrites.

PBS-R036. Before activation, rollback MUST restore the preceding pending
resource mappings, selector policy, projections, and generated outputs as one
reviewed change.
After activation, rollback MUST use the existing immutable-release mechanism
and MUST NOT rewrite accepted project artifacts.

PBS-R037. Validation and review diagnostics MUST identify the affected skill
or artifact, stable check or finding ID, resource layer or cited stable ID,
expected outcome, and blocking reason without exposing secrets or private
machine paths.

PBS-R038. The feature MUST remain usable from published skill packages and
project-local artifacts without a particular model, runtime, hosted service,
network connection, workspace interceptor, or repository-local attestation
service.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: PBS-R001, PBS-R002, PBS-R003, PBS-R004, PBS-R005, PBS-R006, PBS-R007, PBS-R008, PBS-R009, PBS-R010, PBS-R011, PBS-R012, PBS-R013, PBS-R014, PBS-R015, PBS-R016, PBS-R017, PBS-R018, PBS-R019, PBS-R020, PBS-R021, PBS-R022, PBS-R023, PBS-R024, PBS-R025, PBS-R026, PBS-R027, PBS-R028, PBS-R029, PBS-R030, PBS-R031, PBS-R032, PBS-R033, PBS-R034, PBS-R035, PBS-R036, PBS-R037, PBS-R038

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| `input-domain` | applicable | PBS-R005, PBS-R007, PBS-R008, PBS-R009, PBS-R010, PBS-R015, PBS-R019, PBS-R021, PBS-R022 | BND-INPUT-001, BND-INPUT-002 | - |
| `state-lifecycle` | applicable | PBS-R003, PBS-R004, PBS-R005, PBS-R006, PBS-R034, PBS-R036 | BND-STATE-001, BND-STATE-002 | - |
| `identity-authority` | applicable | PBS-R012, PBS-R014, PBS-R017, PBS-R018, PBS-R020, PBS-R025, PBS-R026, PBS-R028, PBS-R030, PBS-R031, PBS-R032 | BND-AUTH-001, BND-AUTH-002, BND-AUTH-003 | - |
| `composition-path` | applicable | PBS-R014, PBS-R017, PBS-R018, PBS-R019, PBS-R021, PBS-R022, PBS-R023, PBS-R026, PBS-R028, PBS-R029, PBS-R032, PBS-R033 | BND-COMPOSE-001, BND-COMPOSE-002, BND-COMPOSE-003 | - |
| `temporal-retry` | applicable | PBS-R003, PBS-R021, PBS-R022, PBS-R024, PBS-R033, PBS-R034, PBS-R036 | BND-TEMPORAL-001 | - |
| `failure-recovery` | applicable | PBS-R015, PBS-R019, PBS-R020, PBS-R024, PBS-R029, PBS-R033, PBS-R034, PBS-R036, PBS-R037 | BND-RECOVERY-001, BND-RECOVERY-002 | - |
| `compatibility-migration` | applicable | PBS-R001, PBS-R002, PBS-R004, PBS-R006, PBS-R025, PBS-R028, PBS-R029, PBS-R035, PBS-R036 | BND-COMPAT-001, BND-COMPAT-002 | - |
| `external-environment` | applicable | PBS-R032, PBS-R033, PBS-R034, PBS-R037, PBS-R038 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| `BND-INPUT-001` | `input-domain` | PBS-R005, PBS-R007, PBS-R008, PBS-R009, PBS-R010 | behavioral request; non-behavior request; active governed IDs; no governed IDs | Method-name presence never controls applicability. | Qualifying work scans and follows active identities; non-behavior work avoids formal output. | PBS-R007 |
| `BND-INPUT-002` | `input-domain` | PBS-R015, PBS-R019, PBS-R021, PBS-R022 | known ID; missing ID; stale ID; unknown ID; ambiguous ID; conflicting ID; escaped outcome | Only approved stable IDs can authorize downstream reliance. | Known IDs permit sliced consumption; every invalid or escaped state triggers expansion or upstream routing. | PBS-R019 |
| `BND-STATE-001` | `state-lifecycle` | PBS-R003, PBS-R004, PBS-R005, PBS-R006, PBS-R034 | pending; activation-ready; active; partial or mixed activation | Formal automatic adoption is active-only and activation is atomic. | Pending forbids active claims; complete activation enables automatic adoption; partial activation blocks. | PBS-R003 |
| `BND-STATE-002` | `state-lifecycle` | PBS-R034, PBS-R036 | current pending bundle; reviewed replacement; current active release; immutable rollback release | Rollback never creates a mixed live resource set or rewrites accepted artifacts. | Pre-activation rollback restores one coherent pending bundle; post-activation rollback selects an immutable release. | PBS-R036 |
| `BND-AUTH-001` | `identity-authority` | PBS-R012, PBS-R014, PBS-R017 | compact semantics; feature-authoring semantics; proof semantics; stage-local policy | Each semantic or stage decision has one owner. | Consumers load only owned resources; unknown or additional ownership blocks mapping validation. | PBS-R012 |
| `BND-AUTH-002` | `identity-authority` | PBS-R017, PBS-R018, PBS-R020, PBS-R031 | feature owner; proof owner; plan owner; implementation/review consumer; deterministic validator | Downstream stages and validators cannot create upstream semantics. | Owned decisions proceed; new behavior routes to `spec`; missing proof routes to `test-spec`; validators remain structural. | PBS-R020 |
| `BND-AUTH-003` | `identity-authority` | PBS-R025, PBS-R026, PBS-R028, PBS-R030 | published skill text; lifecycle-managed artifact; change metadata | Validation authority follows the changed surface. | Skills receive purpose-built checks; governed artifacts retain lifecycle checks; no check claims another owner's settlement. | PBS-R025 |
| `BND-COMPOSE-001` | `composition-path` | PBS-R014, PBS-R032, PBS-R033 | canonical resource; skill-local projection; generated skill; packed adapter; installed skill | Required resource identity and containment remain deterministic across layers. | Exact layers pass; missing, additional, escaped, or divergent layers fail closed. | PBS-R032 |
| `BND-COMPOSE-002` | `composition-path` | PBS-R017, PBS-R018, PBS-R019, PBS-R021, PBS-R022, PBS-R023 | full approved record; cited slice; public path; helper path; sibling or alternate path | A slice can narrow reading but cannot narrow governed behavior. | Sufficient slices permit the stage decision; unexplained or materially different paths trigger expansion or proof. | PBS-R018 |
| `BND-COMPOSE-003` | `composition-path` | PBS-R026, PBS-R027, PBS-R028, PBS-R029 | skill-only changed set; lifecycle-only changed set; mixed changed set; selector changed set | Each path retains every check owned by its surface. | Skill-only excludes lifecycle validation; lifecycle paths retain it; mixed sets preserve both; selector changes add regression proof. | PBS-R029 |
| `BND-TEMPORAL-001` | `temporal-retry` | PBS-R003, PBS-R021, PBS-R022, PBS-R024, PBS-R033, PBS-R034, PBS-R036 | initial generation; repeated generation; interrupted projection; retry; activation; rollback | Repetition is deterministic and no interrupted or retried operation may expose a mixed active bundle. | Idempotent repetition preserves identity; interruption or drift blocks activation; rollback restores a coherent prior bundle. | PBS-R034 |
| `BND-RECOVERY-001` | `failure-recovery` | PBS-R015, PBS-R019, PBS-R020, PBS-R024, PBS-R037 | missing resource or ID; stale resource or ID; semantic discovery; proof gap | Failure is visible and routed to the owning stage. | Package defects block locally; semantic discoveries route to `spec`; proof gaps route to `test-spec`. | PBS-R020 |
| `BND-RECOVERY-002` | `failure-recovery` | PBS-R029, PBS-R033, PBS-R034, PBS-R036 | selector omission; projection drift; mixed bundle; failed activation; failed rollback validation | Recovery cannot suppress checks belonging to unaffected governed paths. | Faulty bundles or routes fail closed; recovery restores the last coherent mapping or immutable release. | PBS-R036 |
| `BND-COMPAT-001` | `compatibility-migration` | PBS-R001, PBS-R002, PBS-R004, PBS-R006, PBS-R035 | pending contract; grandfathered spec; new post-activation spec; substantively revised grandfathered spec | The semantic version and historical acceptance remain stable. | Pending work makes no active claim; historical specs remain valid; new or substantive post-activation specs adopt automatically. | PBS-R035 |
| `BND-COMPAT-002` | `compatibility-migration` | PBS-R025, PBS-R028, PBS-R029, PBS-R036 | old selector route; refined selector route; pre-activation rollback; post-activation rollback | Removing a skill-path route cannot remove lifecycle coverage from actual governed artifacts. | Refined routing reduces irrelevant skill checks while preserving governed-artifact safety and reversible rollout. | PBS-R029 |
| `BND-ENV-001` | `external-environment` | PBS-R032, PBS-R033, PBS-R034, PBS-R037, PBS-R038 | canonical repository; generated tree; package archive; clean installed target; unavailable external tool | Repository-owned proof is portable and does not depend on one hosted runtime. | Available layers receive deterministic proof; missing required local proof blocks; unavailable external operation cannot be claimed complete. | PBS-R038 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| `INT-001` | PBS-R003, PBS-R014, PBS-R032, PBS-R033, PBS-R034 | BND-STATE-001, BND-COMPOSE-001, BND-TEMPORAL-001 | Activation occurs while one stage-family resource or package layer is stale. | Activation blocks before any active claim; all layers remain on the prior coherent bundle. |
| `INT-002` | PBS-R018, PBS-R019, PBS-R020, PBS-R021 | BND-INPUT-002, BND-AUTH-002, BND-COMPOSE-002, BND-RECOVERY-001 | A downstream slice omits a sibling path whose outcome differs from the cited path. | The stage expands context, records proof when behavior is already owned, or routes a new normative outcome to `spec`. |
| `INT-003` | PBS-R025, PBS-R026, PBS-R028, PBS-R029 | BND-AUTH-003, BND-COMPOSE-003, BND-COMPAT-002 | Removing lifecycle validation from a skill path accidentally suppresses lifecycle validation for a feature spec in the same changed set. | Purpose-built skill checks and governed-artifact lifecycle checks are both retained with correctly scoped affected paths. |
| `INT-004` | PBS-R005, PBS-R006, PBS-R007, PBS-R009, PBS-R035 | BND-INPUT-001, BND-STATE-001, BND-COMPAT-001 | Automatic adoption is applied while pending or to a non-behavioral or grandfathered non-substantive change. | No formal record is created; active-only and substantive-revision rules remain authoritative. |
| `INT-005` | PBS-R015, PBS-R032, PBS-R033, PBS-R036, PBS-R038 | BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-002, BND-ENV-001 | A generated or installed resource is missing and a runtime fallback attempts to hide the packaging defect. | Validation fails closed at the first divergent layer; rollback restores a coherent package and runtime fallback cannot establish parity. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| `E1` | `illustration` | PBS-R005, PBS-R007, PBS-R010 | BND-INPUT-001 | - | - |
| `E2` | `illustration` | PBS-R008, PBS-R009 | BND-INPUT-001 | - | - |
| `E3` | `illustration` | PBS-R017, PBS-R018, PBS-R019 | BND-COMPOSE-002 | - | - |
| `E4` | `illustration` | PBS-R021, PBS-R022, PBS-R023 | BND-COMPOSE-002 | - | - |
| `E5` | `regression` | PBS-R025, PBS-R026, PBS-R030 | BND-AUTH-003 | REG-PBS-001 | - |
| `E6` | `regression` | PBS-R028, PBS-R029 | BND-AUTH-003, BND-COMPOSE-003, BND-COMPAT-002 | REG-PBS-002 | - |

## Inputs and outputs

Inputs:

- capability activation state;
- governed skill identity and current stage;
- user request and current artifact type;
- approved feature, boundary, interaction, plan, and proof IDs;
- changed repository paths and validation mode;
- canonical resource owners, projection metadata, package archives, and clean
  installed targets.

Outputs:

- a compact-scan decision with no formal artifact when formalization is not
  required;
- formal feature and proof records when the active contract requires them;
- stage-specific approved artifact slices;
- upstream gap routing;
- deterministic resource projections and package parity evidence;
- selector output with purpose-built checks and correctly scoped lifecycle
  checks.

## State and invariants

- The semantic contract remains `boundary-first-v1`.
- Capability state remains exactly `pending` or `active`.
- Automatic formal adoption occurs only while active.
- The eight boundary dimensions, identifier grammars, feature record, and
  proof record retain one authoritative definition.
- Every semantic resource layer and stage decision has one owner.
- Downstream slices never redefine upstream outcomes or IDs.
- Scenario count follows distinct outcomes and material hazards, not possible
  combinations.
- Published skill text is not a lifecycle-managed artifact.
- Governed artifacts retain lifecycle validation.
- Generated, packed, and installed resources remain derived and deterministic.
- Activation and rollback never expose a mixed live resource bundle.

## Error and boundary behavior

- Missing, unknown, additional, escaped, or mismapped resources fail closed.
- Missing, stale, unknown, ambiguous, conflicting, or escaped stable IDs stop
  downstream reliance and trigger expansion or upstream routing.
- A new normative outcome discovered downstream routes to `spec`.
- A missing proof obligation routes to `test-spec`.
- A skill-only changed set selecting artifact-lifecycle validation is a selector
  defect.
- A mixed changed set omitting lifecycle validation for a governed artifact is
  a blocking selector defect.
- Structural validation cannot repair or approve a semantic gap.
- A partial or byte-divergent package bundle blocks activation.
- External tool unavailability cannot be reported as successful package or
  installation proof.

## Compatibility and migration

The capability remains pending until atomic activation.
Existing accepted feature specs and immutable packages remain valid.
The resource refinement does not require historical artifact migration or a
new boundary contract version.

Before activation, the repository may replace the full shared-reference
mapping with the progressive resource set as one reviewed bundle.
After activation, new behavior-changing specs adopt automatically and
substantive grandfathered revisions are classified by `spec-review`.

Rollback restores one coherent prior mapping or immutable release.
It does not rewrite accepted feature specs, test specs, plans, or review
evidence.

## Observability

- Skill validation identifies the skill, mapped resource layer, expected path
  or identity, and first failing condition.
- Projection and package validation identify the first canonical, generated,
  packed, or installed layer that diverges.
- Selector output identifies changed paths, selected check IDs, affected
  paths, rationale, and blocking status.
- Upstream gap records identify the stable missing or escaped ID, observed
  outcome, owning stage, and stop reason.
- Diagnostics use repository-relative paths and do not expose private machine
  paths or secrets.

## Security and privacy

The compact scan includes identity, authority, trust, and external conditions
when they can change outcomes.
It does not require recording credentials, secrets, personal data, private
machine paths, model identity, or runtime attestation.

Stable redacted evidence identities are used when raw evidence could contain
sensitive data.
Selector and validation diagnostics expose only the minimum repository-local
information required to resolve a failure.

## Accessibility and UX

No graphical interface is introduced.
Published guidance remains readable Markdown and does not rely on color,
diagrams, or tool-specific UI.

Users are not required to know the internal method name.
Formal application and blockers are explained concisely.
Non-behavior work is not burdened with formal tables or scenario inventories.

## Performance expectations

The compact scan MUST remain four questions and MUST NOT require loading
feature-authoring or proof guidance merely to decide that formalization is not
applicable.

Implementation validation MUST record before-and-after canonical resource
bytes, mapped-resource counts, and representative loaded-resource counts by
stage family.
The first slice MUST NOT introduce a hard token, document-length, or runtime
budget without a later approved contract.

## Edge cases

EC1. The user names no method, but the task changes observable behavior;
the compact scan and active formal-adoption rules still apply.

EC2. The user names `boundary-first-v1` for spelling-only work;
the compact scan runs, but no formal record is created solely from the name.

EC3. A grandfathered spec receives only link or formatting changes;
`spec-review` does not classify it as substantive.

EC4. A compact scan finds an unknown outcome while capability state is pending;
the owning stage records or routes the behavior gap without claiming active
formal adoption.

EC5. A downstream stage receives a valid ID whose cited row does not explain a
material sibling-path result; it expands context and stops if behavior
ownership is missing.

EC6. Two scenarios use different inputs but prove the same outcome and no
material hazard; the second is not required.

EC7. One scenario covers a distinct recovery outcome despite sharing the same
input partition; it remains required.

EC8. A governed skill maps proof guidance even though it is not `test-spec` or
`test-spec-review`; resource-map validation fails.

EC9. `spec-review` lacks feature-authoring guidance or `test-spec-review`
lacks proof guidance; package-integrity validation fails.

EC10. A canonical skill change also changes a feature spec;
purpose-built skill checks and artifact-lifecycle validation are both selected
for their owned paths.

EC11. A generated skill path alone is present in changed paths;
the selector proves derivation and drift without treating the generated file
as authored lifecycle state.

EC12. A skill contains words such as `active`, `blocked`, or `after merge`;
those words do not make the skill a lifecycle-managed artifact.

EC13. One installed adapter contains the compact core but omits its required
stage-family resource; activation fails closed.

EC14. Projection retry produces the same complete bytes;
validation passes idempotently.

EC15. Projection is interrupted after updating only some governed skills;
the mixed bundle cannot activate.

EC16. A runtime can supply fallback instructions for a missing resource;
the package still fails deterministic validation.

EC17. A future proposal seeks hard context budgets;
it requires separate measurements and an approved contract.

## Non-goals

- Do not add or remove core boundary dimensions.
- Do not create a second boundary model version.
- Do not require formal records for every task.
- Do not generate every scenario combination.
- Do not create a standalone boundary context packet or lifecycle stage.
- Do not let downstream stages redefine feature or proof records.
- Do not let deterministic validators decide semantic completeness.
- Do not remove lifecycle validation from governed artifacts or change records.
- Do not treat canonical or generated skill text as lifecycle-managed state.
- Do not hand-edit generated skill or adapter output.
- Do not activate the capability in this spec-authoring change.
- Do not rewrite historical accepted artifacts.
- Do not add a runtime service, network dependency, model gate, or attestation
  service.
- Do not introduce a hard token or document-length gate in the first slice.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-PBS-001` | Qualifying governed skills perform the four-question compact scan without requiring the user to name the method. |
| `AC-PBS-002` | Non-behavior work creates no formal boundary record or scenario inventory solely because the compact scan ran or the user named the method. |
| `AC-PBS-003` | The semantic version, dimensions, IDs, feature record, proof record, and stage responsibilities remain one `boundary-first-v1` model. |
| `AC-PBS-004` | The compact core, feature-authoring guidance, proof guidance, and stage-local text have explicit non-overlapping ownership. |
| `AC-PBS-005` | Governed skill packages contain exactly the resource layers required by their stage family. |
| `AC-PBS-006` | Downstream stages consume cited approved rows first and route missing, invalid, conflicting, or escaped behavior to the owning stage. |
| `AC-PBS-007` | Scenario selection covers distinct outcomes and material hazards without requiring Cartesian combinations. |
| `AC-PBS-008` | Skill-only paths retain purpose-built validation without selecting artifact-lifecycle validation. |
| `AC-PBS-009` | Governed artifact and mixed changed sets retain correctly scoped artifact-lifecycle validation. |
| `AC-PBS-010` | Canonical, generated, packed, and installed resources preserve deterministic containment and byte parity. |
| `AC-PBS-011` | Missing, additional, stale, mixed-version, path-divergent, or byte-divergent resources fail closed. |
| `AC-PBS-012` | Activation remains pending until the complete progressive resource and package bundle is current atomically. |
| `AC-PBS-013` | Historical artifacts and immutable packages remain compatible, and rollback restores one coherent prior bundle without rewriting accepted artifacts. |
| `AC-PBS-014` | Structural validation remains bounded to structural claims and semantic review remains stage-owned. |
| `AC-PBS-015` | Diagnostics are actionable, repository-relative, and privacy-bounded. |
| `AC-PBS-016` | The first slice records resource and representative loading measurements without imposing an unapproved hard budget. |

## Open questions

Architecture must resolve:

- exact canonical filenames and compatibility aliases for the three portable
  resource layers;
- projection-manifest shape and identity;
- whether the compact scan remains duplicated as four short stage-local
  questions or is injected through an existing generated shared block;
- representative stage-family loading measurements and fixtures; and
- the atomic rollback unit for selector, resource maps, projections, and
  generated packages.

These questions do not alter the observable contract or block spec review.

## Next artifacts

1. Complete independent `spec-review`.
2. Record architecture assessment.
3. Create and review the architecture package.
4. Create and review the execution plan.
5. Create and review one matching test specification.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.

The spec defines prompt-independent compact scanning, conditional formal
adoption, progressive resource ownership, stable-ID artifact slicing,
hazard-driven scenario selection, skill-specific validation ownership,
governed-artifact lifecycle preservation, deterministic projection, atomic
activation, compatibility, and rollback behavior.
