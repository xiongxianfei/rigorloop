<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->

# Workflow Skill Simplification

## Owning change record

`docs/changes/2026-08-11-workflow-skill-simplification/change.yaml`

## Problem

The published `workflow` skill combines ordinary routing, governed lifecycle mutation, armed automation, detailed review-gate procedure, and project workflow-guide authoring in one 496-line, 4,333-word `SKILL.md`.
Every invocation therefore loads procedure that many routing and audit requests do not use.

The main file also repeats the standard lifecycle sequence, isolation and continuation rules, artifact placement, readiness boundaries, and stop conditions across multiple sections.
This makes the orchestrator harder to scan and creates several owners for rules that should have one source inside the skill package.

The problem is not excessive lifecycle rigor.
The problem is that universal routing safeguards, conditional state-transition procedure, automation-only policy, and guide-authoring procedure are not separated according to the authority that activates them.

## Goals

- Make generic routing invocations and audits that do not depend on a governed record shorter and easier to follow.
- Keep `SKILL.md` sufficient to classify every invocation and stop safely before loading conditional procedure.
- Give every behaviorally significant workflow rule one explicit owner and destination.
- Load governed lifecycle-transition procedure only when current change-local authority makes it applicable.
- Load bounded automation procedure only for an explicit automation command or current durable authorization for the same governed change.
- Load workflow-guide authoring procedure and its structural asset only when creating or substantially refreshing a project workflow guide.
- Preserve lifecycle ordering, isolation, artifact ownership, review settlement, milestone handling, claim boundaries, stops, and handoffs.
- Preserve deterministic canonical, generated, archived, and installed package resources.
- Measure each representative resource assembly separately from total package size so relocation is not misreported as deletion.

## Non-goals

- Changing the standard workflow stage order, stage obligations, review outcomes, or downstream authority.
- Changing the `change.yaml` schema, lifecycle state model, automation persistence model, or ownership boundaries as part of prose simplification.
- Weakening review independence, requirement-fidelity gates, review recording, milestone closeout, or final holistic review.
- Replacing specialized stage skills with workflow-owned authoring or review procedure.
- Rewriting `docs/workflows.md` unless a later approved contract identifies a required documentation correction.
- Optimizing other published skills in the same change.
- Introducing a routing engine, selector service, scheduler, new runtime, or persistent state store.
- Adding a permanent line-count, token-count, prose-quality, or simplicity validator.
- Executing or grading Codex, Claude Code, opencode, or another target-agent runtime for acceptance.
- Hand-editing generated adapter output or installed skill copies.

## Vision fit

fits the current vision

The change reduces context and navigation cost while retaining the durable artifacts, explicit authority, traceability, review gates, and resumability that distinguish RigorLoop.
It simplifies the product surface without replacing evidence with trust or removing rigor that affects outcomes.

## Context

`skills/workflow/SKILL.md` is currently the largest published skill common path:

| Resource | Lines | Words | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| `SKILL.md` | 496 | 4,333 | 32,074 |
| Boundary-first reference | 110 | 857 | 6,346 |
| Workflow-guide skeleton | 234 | 1,236 | 9,551 |
| Total package | 840 | 6,426 | 47,971 |

The largest main-file sections are invocation and continuation, boundary-first guidance, customer-project workflow-guide procedure, automated review routing, standard workflow routing, review and claim routing, and planned initiative state.
The full lifecycle sequence appears twice, and several stop, continuation, isolation, and artifact-location rules appear in overlapping sections.

The published-skill contract already treats a skill as canonical `SKILL.md` plus explicitly mapped packaged resources.
The completed `code-review` and `implement` simplifications demonstrated that conditional policy can remain owned by the skill package while moving behind exact `READ` triggers.
They also demonstrated the need to separate semantic-rule disposition from literal dependency compatibility and to report invocation-loaded content separately from total package content.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `workflow` skill next | in scope | Goals and Recommended direction |
| Choose the best solution rather than blindly shorten prose | in scope | Options considered and Recommended direction |
| Preserve workflow rigor and routing correctness | in scope | Non-goals, Expected behavior changes, and Risks and mitigations |
| Start a new branch | in scope | Branch `proposal/workflow-skill-simplification` |
| Create a formal proposal | in scope | This artifact and owning change record |
| Run proposal review immediately afterward | in scope | Next artifacts and Readiness |
| Make this change own architecture work if it changes `change.yaml` architecture | in scope | Architecture impact and Scope budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Inventory and disposition current workflow rules | core to this proposal | Semantic preservation requires explicit source-to-destination ownership. |
| Consolidate the universal routing contract | core to this proposal | Every invocation loads it. |
| Add governed lifecycle-routing reference | core to this proposal | Detailed mutation and closeout procedure requires current change-local authority. |
| Add bounded automation reference | core to this proposal | Target, resume, correction, packet, and promotion policy applies only when armed. |
| Add workflow-guide authoring reference | core to this proposal | Guide creation and refresh are independent of ordinary routing. |
| Retain the workflow-guide skeleton as structural asset | core to this proposal | The existing asset already owns guide layout. |
| Preserve the shared boundary reference | same-slice dependency | The governed boundary-first contract requires it. |
| Add semantic-rule and literal-compatibility inventories | core to this proposal | Behavior and incidental textual coupling are different evidence classes. |
| Extend existing skill and adapter package proof | same-slice dependency | New mapped resources require deterministic distribution proof. |
| Reuse permanent contract and package validators | same-slice dependency | Durable public invariants remain enforced by their existing owners. |
| Keep ledgers, scenarios, measurements, and semantic review change-local | core to this proposal | One-change simplification evidence must not become a new validator family. |
| Record an architecture assessment | same-slice dependency | The package and change-record boundaries require an explicit assessment. |
| Author and review architecture owned by this change if `change.yaml` architecture changes | same-slice dependency | A schema, ownership, or persistence change cannot be delegated or hidden inside simplification. |
| Build a deterministic routing engine | out of scope | It changes architecture and maintenance responsibility without evidence that prose orchestration is insufficient. |
| Optimize other skills | separate proposal | Each skill has distinct authority and conditional boundaries. |
| Add a permanent simplicity validator | out of scope | Size evidence is change-local, not a durable product invariant. |

## Options considered

### O0: Keep the current skill

This avoids migration risk and preserves exact wording.
It leaves the 4,333-word common path, duplicated ownership, and unconditional automation and guide-authoring procedure unchanged.

### O1: Editorial compression only

Merge repeated paragraphs and shorten prose while keeping all procedure inline.
This has the smallest packaging change and could reduce the main file by roughly 15–25 percent, but every routing request would still load lifecycle mutation, automation, and guide-authoring details.

### O2: Extract only bounded automation

Consolidate universal prose and move `$workflow auto` procedure into one conditional reference.
This removes the largest clearly conditional block with limited package complexity, but governed mutation and workflow-guide authoring would remain mixed into ordinary routing.

### O3: Use a compact dispatcher with three conditionally loaded procedure references

Keep classification, universal safety, core stage order, authority boundaries, stops, claims, resource triggers, and output in `SKILL.md`.
Move governed lifecycle transitions, bounded automation, and workflow-guide authoring into three flat references selected by exact evidence predicates.
Retain the existing boundary reference and workflow-guide skeleton.

This addresses both duplication and unnecessary loading while keeping all resources one level below `SKILL.md` and under the ownership of the `workflow` package.

### O4: Replace prose orchestration with a deterministic state-transition engine

Move routing and mutation into a script or service and leave the skill as a thin interface.
This could enforce transitions more mechanically, but it would introduce a new execution boundary, architecture, error model, compatibility surface, and maintenance owner.
It is not justified by the current simplification problem.

## Recommended direction

Choose O3.

### Universal `SKILL.md` contract

Keep the following inline because it is required before any optional resource can be selected:

| Inline content | Reason |
| --- | --- |
| Purpose, trigger, workflow role, and competing-skill boundaries | Required to classify the invocation. |
| Source-of-truth, evidence precedence, and unknown-artifact or unknown-stage behavior | Required before routing or mutation. |
| Core lifecycle graph and conditional-stage concept | Required for every routing decision. |
| Invocation classification predicates | Required to load the correct resources. |
| Manual invocation isolation | Must apply even when no reference is loaded. |
| High-level stage and state ownership | Prevents unauthorized write-back. |
| Universal claim boundaries and stop conditions | Must act before optional procedure. |
| Compact boundary-first bridge | Identifies when the shared method is required. |
| Resource map with exact load conditions | Makes progressive disclosure deterministic. |
| Compact handoff and result contract | Required for every invocation. |

Remove the separate quick guide after its unique obligations are consolidated into the required core sections.
Express the standard lifecycle graph once.
Consolidate overlapping readiness, continuation, isolation, stop, and output rules under their single required owners.

### Governed lifecycle reference

Add:

```text
skills/workflow/references/governed-lifecycle-routing.md
```

Load it exactly when a routing, audit, status, resume, settlement, or mutation decision depends on a current governed change record under `lifecycle_contract: stage-owned-change-local-v1`.
The trigger is evidence dependency, not mutation intent: a read-only audit of current lifecycle state loads this reference even when no state will change.

It owns:

- complete change-record inspection and identity resolution;
- lifecycle and architecture-assessment applicability and routing;
- artifact settlement consumption and stage-transition procedure;
- workflow-owned versus stage-owned mutation limits;
- planned milestone advancement and review-resolution return;
- final holistic review and lifecycle-closeout routing;
- stale, ambiguous, illegal, or contradictory state handling; and
- workflow-owned transition evidence.

It does not own stage-specific authoring, review, implementation, verification, or PR policy.

### Bounded automation reference

Add:

```text
skills/workflow/references/bounded-workflow-automation.md
```

Load it for `$workflow auto: <target-stage>`, `$workflow auto: status`, `$workflow auto: off`, or a durable active, paused, or resumable automation record for the same change.

An explicit automation command creates command context only; it does not create armed-automation context.
Armed automation requires a valid governed change identity and current durable authorization for that same change.
For a new target request without an existing change record, enter a transient automation-bootstrap profile, establish or resolve a valid governed change identity through the existing workflow authority, validate it, reclassify the invocation as governed, and only then persist automation; stop when that identity cannot be created or resolved safely.
The bootstrap profile is never persisted as an armed run.
A persisted or resumable automation record without a current matching governed change is invalid and stops before mutation.
Conversational wording alone cannot create, resume, rebind, or cancel durable automation.

`$workflow auto: status` with no selected change and no active run loads only the automation reference and returns `no-active-run` without mutation.
`$workflow auto: off` with no active run likewise loads only the automation reference and returns the existing no-active-run result without creating governed state.
Status or cancellation of a current run loads both the governed and automation references because the result depends on canonical lifecycle position and durable automation identity.

The reference owns:

- target, occurrence, status, cancellation, and resume semantics;
- durable automation identity and staleness checks;
- neutral review invocation packets and phase receipts;
- independent and requirement-fidelity gate receipts and automation-specific promotion conditions;
- bounded review-fix correction cycles;
- transition budgets, pause reasons, and target completion; and
- automation-only prohibited actions and result fields.

Automation asks the governed lifecycle procedure for the next legal lifecycle transition.
It does not redefine stage order, stage applicability, settlement, architecture-assessment applicability, or final-review applicability.

Universal destructive-action boundaries, isolation, authority, claim limits, and stop behavior remain inline.

### Workflow-guide authoring reference

Add:

```text
skills/workflow/references/workflow-guide-authoring.md
```

Load it only when creating a new project-local `docs/workflows.md` or substantially refreshing a stale guide or artifact-location map.

It owns:

- guide creation and refresh triggers;
- instructions for rendering established routing rules and project-local artifact locations into the guide;
- project-local customization and fallback documentation procedure;
- migration and update-reason recording; and
- instructions for copying and filling `assets/workflows-skeleton.md`.

The asset continues to own guide labels, order, and layout only.
It does not own workflow policy, lifecycle meaning, or artifact authority.

### Trigger model, bootstrap, and representative assemblies

Use four predicates:

```text
governed_change_context
automation_command_context
armed_automation_context
workflow_guide_authoring_context
```

`governed_change_context` means that a valid current governed change record already exists.
`automation_command_context` means that the invocation is an explicit `$workflow auto: <target-stage>`, `$workflow auto: status`, or `$workflow auto: off` command, including the interval before any governed identity or authorization is persisted.
`armed_automation_context` means that a current durable automation authorization or run exists for the same valid governed change.
The command form may establish automation-command context, but it cannot by itself establish armed-automation context.
`workflow_guide_authoring_context` is independent and may coexist with governed routing.
Workflow-guide authoring and active automation are mutually exclusive within one invocation in the first version; guide work requires a separate invocation after automation pauses, completes, or is cancelled.
The boundary-first trigger remains independently additive.

| Assembly | Governed record | Automation command or run | Guide authoring | Loaded procedure or result |
| --- | ---: | ---: | ---: | --- |
| `WP0-generic-routing` | no | no | no | `SKILL.md` only; boundary reference only when independently triggered |
| `WP1-governed` | yes | no | no | `SKILL.md` plus governed lifecycle reference |
| `WP2-governed-automated` | yes | yes | no | `SKILL.md` plus governed lifecycle and automation references |
| `WP3-guide-authoring` | no | no | yes | `SKILL.md` plus guide reference and skeleton |
| `WP4-governed-guide-authoring` | yes | no | yes | `SKILL.md` plus governed lifecycle and guide resources |
| `WPB-automation-bootstrap` | no | new target command only | no | Load automation reference, establish and validate governed identity, then reclassify before persistence |
| Invalid | no | active or resumable automation | any | Stop; durable automation requires matching governed change authority |
| Invalid | any | active automation | yes | Stop; require separate guide-authoring invocation after the run is inactive |

For `WPB-automation-bootstrap`, use this closed sequence:

1. `SKILL.md` recognizes the explicit automation command.
2. Load the automation reference for command and bootstrap semantics.
3. Resolve or create the governed change identity under existing workflow authority.
4. Validate the resulting governed record.
5. Reclassify the invocation as governed.
6. Load the governed lifecycle reference.
7. Only then persist authorization, target, or run state.

For measurement, use these exact assemblies and add the boundary reference only to separately reported boundary-triggered variants.
Count each unique loaded resource once.

Apply these command-specific load cases:

| Invocation | Governed reference | Automation reference | Result boundary |
| --- | ---: | ---: | --- |
| Generic route or audit that does not depend on a current change record | no | no | Base routing only. |
| Read-only audit, status explanation, or route decision based on current `change.yaml` | yes | no | No mutation unless separately authorized. |
| Governed stage advancement, settlement, or mutation | yes | no | Existing lifecycle authority applies. |
| New `auto: <target>` without an existing change record | after identity validation | yes | Enter `WPB`; establish and validate governed identity, reclassify, then persist automation. |
| `auto: <target>` or resume for an existing matching change | yes | yes | Target and transition remain bound to that change. |
| `auto: status` with a current run | yes | yes | Read-only status from canonical lifecycle and automation state. |
| `auto: status` with no selected change and no active run | no | yes | Return `no-active-run`; create no state. |
| `auto: off` with a current run | yes | yes | Reconcile and cancel under existing automation policy. |
| `auto: off` with no active run | no | yes | Return the existing no-active-run outcome; create no state. |
| Persisted automation identity mismatches the selected change | stop | stop | No rebind, resume, cancellation, or mutation. |

### Ownership and duplication rules

Use this non-overlapping ownership model:

| Contract | Owner |
| --- | --- |
| Source rank, evidence precedence, unknown-artifact and unknown-stage behavior | Inline `SKILL.md` |
| Invocation classification, resource triggers, isolation, destructive-action boundaries, and claim boundaries | Inline `SKILL.md` |
| Canonical lifecycle and architecture-assessment applicability | Governed lifecycle reference |
| State interpretation, stage transitions, settlement, milestones, review-resolution return, final review, and closeout routing | Governed lifecycle reference |
| Automation commands, target, occurrence, authorization, identity, status, pause, resume, and cancellation | Automation reference |
| Automation receipts, budgets, correction cycles, and automation-specific promotion conditions | Automation reference |
| Guide creation and refresh, skeleton use, customization recording, and migration notes | Guide-authoring reference |
| Project-local paths and customizations | Generated project `docs/workflows.md` |
| Guide labels, section order, tables, and placeholders | `assets/workflows-skeleton.md` |

The references may point to stable concepts in `SKILL.md`, but they may not duplicate governing procedure from one another.
The dependency direction is one way: automation asks governed procedure for the next valid lifecycle transition, and guide authoring renders established routing rules into `docs/workflows.md`.
Neither reference redefines the contract it consumes.

A conditional reference may specialize procedure for its activation context, but it may not override an inline universal rule or another reference's owned contract.
Any contradiction among `SKILL.md` and mapped references is a package defect and stops the affected operation rather than being resolved by local precedence guessing.

### Required-resource failure boundary

After invocation classification and before any resource-dependent interpretation or action, confirm that every required mapped resource is available and readable:

| Situation | Required behavior |
| --- | --- |
| `WP0` and no conditional resource is triggered | Continue from `SKILL.md`. |
| Governed context and governed reference unavailable | Stop before governed state interpretation or mutation. |
| Automation command or run and automation reference unavailable | Stop before target, status, resume, cancellation, or persistence action. |
| Guide-authoring context and guide reference unavailable | Stop before creating or refreshing the guide. |
| Guide skeleton unavailable | Stop before writing a partial guide. |
| Required reference exists but cannot be read | Stop the affected operation. |
| Installed package contains mixed resource versions | Treat it as a package-integrity blocker; do not combine partial procedures. |
| A conditional trigger is false | Do not load that resource; continue with the applicable assembly. |

The shortened `SKILL.md` is self-sufficient for generic routing and safe classification.
It is intentionally insufficient to reconstruct governed, automation, or guide-authoring procedure when a required resource is missing.
The skill must stop rather than invent, recall, or partially reconstruct missing procedure.
This fail-safe does not add runtime hashing or a new integrity service; existing package and adapter parity checks remain the deterministic prevention mechanism.

Create two separate change-local inventories before moving prose:

1. `workflow-rule-disposition.yaml` records every behaviorally significant rule or duplication cluster, applicable assemblies, one destination, and one closed disposition.
2. `workflow-literal-compatibility.yaml` records exact headings, values, phrases, and consumers, classifying them as normative contract, parser or package contract, test-only incidental, or obsolete.

Closed semantic dispositions should be:

```text
retained-inline
retained-governed-reference
retained-automation-reference
retained-guide-reference
asset-owned
removed-duplicate
removed-obsolete-with-approved-contract-change
```

No semantic rule may disappear without a disposition.
Tests that merely assert incidental prose should be updated rather than becoming policy owners.

## Expected behavior changes

- Generic route and audit requests that do not depend on current governed state encounter a shorter linear dispatcher without lifecycle, automation, or guide-authoring procedure.
- Read-only and mutating decisions that depend on a governed change load lifecycle procedure after current change authority is established.
- A new automation target without a governed record enters a transient bootstrap, establishes and validates governed identity, then reclassifies before any automation state is persisted.
- Armed automation loads both governed and automation procedure, remains bound to the same durable change identity, and delegates lifecycle-transition decisions to the governed procedure.
- Workflow-guide creation loads authoring guidance and the skeleton only when that task applies.
- Active automation and workflow-guide authoring require separate invocations.
- Invalid or stale authority stops before resource-dependent mutation.
- A missing, unreadable, contradictory, or mixed-version required resource stops the affected conditional operation without fallback reconstruction.
- The standard lifecycle order, stage obligations, review outcomes, isolation defaults, milestone transitions, claim ownership, and downstream readiness remain unchanged.
- Canonical, generated, archived, and installed skill packages include every mapped resource at the same relative path and with required byte parity.

## Architecture impact

The selected direction changes the internal packaging of the published `workflow` skill by adding three mapped references.
It does not intentionally change runtime control flow, persistent state, APIs, dependencies, lifecycle ownership, or the normative definition of a published skill package.

The expected architecture assessment outcome is `architecture-not-required` because existing architecture already supports canonical `SKILL.md` plus mapped references and assets as one skill-owned package.
A bounded architecture documentation update may be appropriate if existing diagrams or examples describe the `workflow` package as flat.

If downstream specification changes the `change.yaml` schema, lifecycle ownership, transition model, automation persistence, or another architecture boundary, this change becomes the owner of the corresponding architecture document and review.
That architecture work must be registered in this change's `change.yaml`; it must not be hidden inside the skill edit or assigned to an unrelated change.

A new ADR is warranted only if the normative package model or lifecycle ownership changes.

## Testing and verification strategy

Use four proof classes:

1. A semantic rule-disposition ledger that fails closed on unknown dispositions and maps every significant current rule to one destination.
2. A separate literal-compatibility inventory that distinguishes normative and parser contracts from incidental tests and obsolete wording.
3. Static scenario fixtures for `WP0` through `WP4` and `WPB`, governed read-only and mutating cases, new-target identity establishment and reclassification, status and off with and without a current run, invalid ungoverned automation, active automation combined with guide authoring, stale or mismatched change identity, ambiguous lifecycle state, required-resource absence or unreadability, mixed package resources, guide-authoring triggers, review findings, milestone closeout, and final holistic review.
4. Existing skill, package, adapter, archive, and clean-install validation plus independent semantic review of the complete package.

Fixtures should prove required and forbidden resource loads, mutation authority, stop behavior, stage outcome, and handoff without executing a model runtime.
No acceptance test should invoke or grade Codex, Claude Code, opencode, or another target agent.

Measure normalized-LF canonical files using UTF-8 bytes and Unicode whitespace-separated words.
Record the exact resource list and count each unique resource once for every representative assembly.
Report separately:

- `SKILL.md` lines, words, and bytes;
- each reference and asset contribution;
- `WP0` through `WP4` and `WPB` loaded words and bytes;
- boundary-triggered variants;
- total package words and bytes;
- duplicate rule-cluster count and owner; and
- mapped resource count.

A 35–50 percent reduction in `WP0-generic-routing` is a planning target, not a normative acceptance threshold.
Acceptance requires a material `WP0` reduction, no unjustified regression in `WP1` through `WP4` or `WPB`, honest total-package accounting, one owner per duplicated rule, and preserved semantic and lifecycle behavior.
Do not introduce a permanent tokenizer or simplicity gate.

### Validation ownership

Permanent repository validation retains its existing owners for durable public invariants:

- frontmatter, required sections, and closed public vocabulary;
- `Resource map` syntax, coverage, containment, and mapped-resource existence;
- placeholder, portability, and deterministic claim restrictions already governed by the skill contract; and
- canonical, generated, archived, and temporary installed resource inventory and byte parity.

Extend those existing checks only where the new mapped resources exercise the same durable invariant.
Do not create a `workflow`-simplicity validator or another permanent validator family.

Keep these as change-local evidence:

- semantic-rule and literal-compatibility ledgers;
- positive and negative static scenario fixtures;
- profile resource assemblies and word or byte measurements;
- duplicate-cluster counts and ownership summaries; and
- independent semantic review of the complete package.

Unknown change-local ledger dispositions and literal classifications fail closed in the change-local proof command, but they do not become a recurring selector evidence class.
Do not add a permanent profile-size gate, tokenizer dependency, prose score, generic simplification-fixture framework, target-agent journey, transcript grader, or runtime-version oracle.

## Rollout and rollback

Ship the canonical workflow package, new references, existing asset, focused validator updates, and package proof atomically.
Generate adapter and installed outputs only through existing repository-owned commands and temporary package flows.

Invocation-time resource availability is checked after classification and before conditional action.
Missing, unreadable, contradictory, or mixed-version required resources stop safely; the skill does not reconstruct conditional procedure from the shortened main file.
This is a fail-safe usage rule, not a new runtime hash-verification mechanism.

Rollback restores the prior complete canonical package and regenerates every derived target.
Do not roll back only `SKILL.md` while leaving mapped references or validator expectations in place.

No user data migration, feature flag, external service rollout, or dependency change is expected.
If the approved specification introduces a `change.yaml` architecture change, it requires its own migration and rollback design in the architecture artifact owned by this change.

## Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Universal routing policy moves behind a conditional trigger | Direct routing could miss a stop, authority, or claim boundary. | Define inline ownership before editing and prove `WP0` independently. |
| Automation authority is inferred from chat | An agent could resume or mutate the wrong change. | Require durable matching change identity; make ungoverned automation invalid. |
| Automation bootstrap is mistaken for an armed run | State could be persisted before governed authority exists. | Separate command context from armed context; keep `WPB` transient; reclassify only after validating governed identity. |
| Governed and automation references duplicate transition policy | The package could develop conflicting state owners. | Assign transition ownership to the governed reference and automation-loop ownership to the automation reference. |
| Guide authoring becomes a competing workflow contract | Project guidance could redefine lifecycle policy. | Keep the guide reference procedural and retain policy ownership in the workflow package and governing project artifacts. |
| Active automation and guide authoring alter the same interpretation surface | A running workflow could observe routing guidance that changes mid-run. | Require separate invocations and an inactive automation run before guide authoring. |
| A required conditional resource is unavailable or inconsistent | The skill could invent or partially apply governing procedure. | Stop before affected interpretation or action; prohibit fallback reconstruction; retain existing package parity proof. |
| Main-file shrinkage hides loaded-profile growth | Relocation could be mistaken for simplification. | Measure all representative assemblies and total package content separately. |
| Literal dependencies freeze accidental prose | Simplification could preserve duplication solely for tests. | Classify literal consumers separately and migrate incidental tests. |
| Similar repeated paragraphs encode distinct behavior | Deduplication could erase meaningful exceptions. | Use source-located semantic dispositions and independent review. |
| New resources drift in generated packages | Installed adapters could miss governing procedure. | Extend existing resource inventory, archive, and clean-install parity checks. |
| Change-local evidence becomes permanent infrastructure | A one-time refactor could create lasting selector and validator maintenance. | Keep ledgers, scenarios, measurements, duplication accounting, and semantic review change-local; reuse existing permanent contract and package owners only. |
| Simplification silently changes `change.yaml` architecture | Lifecycle ownership or migration could change without design review. | Keep schema changes out of scope; if later required, register architecture under this change and review it before planning. |

## Open questions

- Which existing exact headings, vocabulary values, and phrases are normative or parser-sensitive rather than incidental test dependencies?
- Does the current architecture documentation contain a flat-package example that needs a bounded update?

These questions can be answered during specification, architecture assessment, and test-spec authoring without changing the selected package direction.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Select O3: compact dispatcher plus governed lifecycle, bounded automation, and guide-authoring references. | It follows three real authority boundaries and provides the greatest useful common-path reduction without changing runtime architecture. | O0 and O1 leave conditional overload; O2 leaves two large conditional concerns inline; O4 expands architecture beyond the problem. |
| 2026-08-11 | Make armed automation require the same valid governed change. | It prevents chat-only activation and ambiguous state ownership. | Independent ungoverned automation would require a new authority model. |
| 2026-08-11 | Treat workflow-guide authoring as an independent additive predicate. | Guide creation can occur with or without a governed delivery change. | Forcing it into a mutually exclusive profile would misrepresent real usage. |
| 2026-08-11 | Keep size targets non-normative. | Semantic and lifecycle preservation take precedence over numeric optimization. | A hard threshold could encourage hiding universal safeguards. |
| 2026-08-11 | Exclude target-agent runtime acceptance. | Static contract proof, package validation, and independent semantic review cover the owned boundary. | Model journeys would create an unstable behavior-test system. |
| 2026-08-11 | Make this change own architecture work if later requirements change `change.yaml` architecture. | Schema, persistence, and ownership changes must remain traceable to the initiating change. | Assigning the work elsewhere would weaken lifecycle ownership. |
| 2026-08-11 | Define governed context by dependency on current lifecycle state, including read-only routing and audit. | Safe routing can require governed semantics even when no mutation occurs. | Mutation-only loading would under-specify audits and status explanations. |
| 2026-08-11 | Keep simplification ledgers, scenarios, profile measurements, and semantic review change-local. | They prove this refactor but are not durable product invariants. | A new permanent validator or selector evidence class would add unrelated maintenance scope. |
| 2026-08-11 | Separate automation-command context from armed-automation context and add transient `WPB-automation-bootstrap`. | A command may arrive before governed identity exists, but durable automation cannot. | Treating command text as armed authority creates circular and unsafe bootstrap semantics. |
| 2026-08-11 | Disallow active automation and guide authoring in the same first-version invocation. | Guide changes can alter the routing interpretation surface of a running workflow. | A combined profile would need additional synchronization and consistency rules outside this simplification. |
| 2026-08-11 | Give lifecycle applicability and transitions exclusively to the governed reference, with automation and guide authoring as consumers. | One owner prevents competing routing answers. | Shared or locally overriding ownership would preserve the duplication being removed. |
| 2026-08-11 | Stop when a required conditional resource is missing, unreadable, contradictory, or version-mixed. | The common path cannot safely reconstruct deliberately disclosed procedure. | Remembered or partial fallback would weaken the package boundary; runtime hashing would expand scope unnecessarily. |

## Next artifacts

- Formal proposal review.
- Contract-level workflow-skill simplification specification after proposal approval.
- Recorded architecture assessment after approved specification review, followed by architecture authoring and review when required.
- Execution plan and traceable test specification after contract and architecture settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for proposal rereview after the R2 findings are recorded as resolved.

The proposal now selects a non-circular bootstrap and complete profile lattice, assigns every universal and conditional contract to one owner, defines fail-safe required-resource behavior, preserves definitive permanent and change-local validation ownership, and retains explicit architecture ownership if a later `change.yaml` change is required.
