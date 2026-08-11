# Workflow Skill Simplification

## Owning change record

`docs/changes/2026-08-11-workflow-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-11-workflow-skill-simplification.md`

## Goal and context

This specification defines a behavior-preserving simplification of the published `workflow` skill package.
It shortens the universal dispatcher, moves governed lifecycle, bounded automation, and workflow-guide authoring procedures into conditionally loaded references, and retains the existing workflow-guide skeleton as a structural asset.

The change preserves workflow classification, source precedence, isolation, state ownership, lifecycle order, review settlement, milestone handling, automation identity, stop behavior, claim boundaries, and downstream handoff authority.
It does not add a runtime routing engine, change persistent workflow state, certify target-agent behavior, or make a numeric size target authoritative over semantic preservation.

This specification specializes `specs/skill-contract.md` and `specs/rigorloop-workflow.md` for the `workflow` package.

## Glossary

- **governing skill package**: canonical `skills/workflow/SKILL.md` plus every explicitly mapped reference and asset beneath `skills/workflow/`, with workflow policy ownership remaining at the `workflow` skill.
- **governed change context**: a valid current change record using `lifecycle_contract: stage-owned-change-local-v1` whose state is required for the current routing decision.
- **automation command context**: an explicit `$workflow auto: <target-stage>`, `$workflow auto: status`, or `$workflow auto: off` invocation before durable authorization is assumed.
- **armed automation context**: a current durable automation authorization or run bound to the same valid governed change.
- **guide-authoring context**: creation or substantial refresh of project-local `docs/workflows.md` or its artifact-location map.
- **automation bootstrap**: the transient `WPB-automation-bootstrap` sequence that establishes and validates governed identity before automation persistence.
- **stateless automation command**: `WPS-stateless-automation-command`, used only for `status` or `off` when no selected change and no active run exist.
- **resource assembly**: the unique canonical resources loaded for one valid invocation profile.
- **required resource**: a mapped reference or asset whose load or copy trigger is true for the classified invocation.

## Examples first

### Example E1: generic routing loads only the common path

Given a routing request that does not depend on a governed change, automation command, or guide-authoring task
When the workflow classifies the invocation
Then `WP0-generic-routing` loads `SKILL.md` only, plus the boundary reference only when independently triggered.

### Example E2: a read-only governed audit loads lifecycle procedure

Given a status explanation depends on current `change.yaml` state
When no mutation is requested
Then `WP1-governed` loads the governed lifecycle reference and preserves read-only authority.

### Example E3: a new automation target bootstraps before persistence

Given an explicit `auto: test-spec-review` command and no governed record
When workflow starts automation
Then `WPB-automation-bootstrap` loads automation command procedure, establishes and validates governed identity, reclassifies as governed, loads governed procedure, and only then persists authorization or run state.

### Example E4: command text does not arm automation

Given conversational wording asks the agent to continue automatically but no valid automation command or durable authorization exists
When the invocation is classified
Then armed-automation context is false and no automation state is created, resumed, rebound, or cancelled.

### Example E5: active automation and guide authoring do not combine

Given a current active automation run
When the same invocation requests a substantial `docs/workflows.md` refresh
Then workflow stops and requires guide authoring in a separate invocation after the run pauses, completes, or is cancelled.

### Example E6: a required reference is unavailable

Given a governed routing decision and an unreadable governed lifecycle reference
When workflow reaches the resource-availability gate
Then it stops before interpreting or mutating governed state and does not reconstruct the procedure from memory.

### Example E7: automation consumes governed transitions

Given a valid armed automation run reaches an architecture-assessment decision
When the next lifecycle transition is required
Then automation asks governed lifecycle procedure for the applicable transition and does not redefine stage order or applicability.

### Example E8: incidental wording does not become policy

Given an exact heading is consumed only by a wording-sensitive test
When the common path is simplified
Then the literal inventory classifies it as `test-only-incidental` and updates the test rather than preserving accidental prose.

### Example E9: stateless status has a valid assembly

Given an explicit `auto: status` command with no selected change and no active run
When the invocation is classified
Then `WPS-stateless-automation-command` loads `SKILL.md` plus the automation reference, returns `no-active-run`, and creates no state.

## Requirements

R1. The governing published `workflow` skill MUST consist of canonical `skills/workflow/SKILL.md` plus every explicitly mapped packaged reference and asset under the same skill root, while routing, lifecycle, automation, and readiness ownership remains with `workflow`.

R2. `SKILL.md` MUST keep purpose, trigger, workflow role, competing-skill boundaries, source rank, evidence precedence, unknown-artifact and unknown-stage behavior, the core lifecycle graph, classification predicates, isolation, high-level state ownership, universal stop and claim boundaries, the compact boundary-first bridge, exact resource triggers, and the compact result and handoff contract inline.

R3. The simplified package MUST map `references/governed-lifecycle-routing.md`, `references/bounded-workflow-automation.md`, and `references/workflow-guide-authoring.md` with the literal verb `READ`; it MUST retain the mapped boundary-first reference and `assets/workflows-skeleton.md` with their contract-required verbs and triggers.

R4. Invocation classification MUST use exactly `governed_change_context`, `automation_command_context`, `armed_automation_context`, and `workflow_guide_authoring_context`, with the meanings defined in this specification.

R5. Classification MUST admit exactly `WP0-generic-routing`, `WP1-governed`, `WP2-governed-automated`, `WP3-guide-authoring`, `WP4-governed-guide-authoring`, transient `WPB-automation-bootstrap`, and `WPS-stateless-automation-command`; every other predicate combination MUST have an explicit stop result.

R6. An explicit automation command MUST establish automation-command context only and MUST NOT establish armed-automation context without a current durable authorization or run bound to the same valid governed change.

R7. `WPB-automation-bootstrap` MUST perform, in order: command recognition; automation-reference loading; governed identity resolution or creation under existing workflow authority; governed-record validation; governed reclassification; governed-reference loading; and only then persistence of authorization, target, or run state.

R8. The bootstrap profile MUST remain transient and MUST NOT be persisted as an armed run; failure to create, resolve, or validate governed identity MUST stop before automation persistence.

R9. Active or resumable automation without a matching valid governed record MUST stop, and active automation combined with guide authoring in one invocation MUST stop and require a separate invocation after automation becomes inactive.

R10. The governed lifecycle reference MUST load whenever routing, audit, status, resume, settlement, or mutation depends on a current governed change record, including read-only decisions.

R11. The governed lifecycle reference MUST exclusively own governed identity interpretation, lifecycle and architecture-assessment applicability, artifact settlement, stage transitions, workflow-versus-stage mutation limits, milestone advancement, review-resolution return, final holistic review, closeout routing, contradictory-state handling, and workflow-owned transition evidence.

R12. The automation reference MUST own only automation command, target, occurrence, authorization, identity, status, pause, resume, cancellation, packet, receipt, budget, correction-cycle, and automation-specific promotion procedure; it MUST ask governed procedure for lifecycle transitions and MUST NOT redefine stage order, applicability, settlement, architecture assessment, final review, or closeout.

R13. The guide-authoring reference MUST own only guide creation and refresh triggers, rendering established routing and project-local artifact locations, customization and fallback documentation, migration notes, and skeleton use; it MUST NOT own source rank, unknown-artifact behavior, lifecycle policy, or artifact authority.

R14. `assets/workflows-skeleton.md` MUST own guide labels, section order, tables, registry structure, and placeholders only; applicability, routing meaning, policy, and authority MUST remain in `SKILL.md` or the applicable reference.

R15. A conditional reference MAY specialize procedure for its activation context but MUST NOT override inline universal policy or another reference's owned contract; any contradiction among mapped package resources MUST be treated as a package defect and stop the affected operation without precedence guessing.

R16. After classification and before resource-dependent interpretation or action, workflow MUST confirm every required resource is present and readable; a missing or unreadable governed, automation, guide, or skeleton resource MUST stop before the action that requires it.

R17. A mixed-version required-resource assembly MUST stop as a package-integrity blocker, and workflow MUST NOT invent, recall, or partially reconstruct missing conditional procedure from the shortened common path.

R18. When no conditional trigger applies, `WP0` MUST continue from `SKILL.md`; a false trigger MUST NOT cause its resource to load.

R19. `auto: status` and `auto: off` without a selected change or active run MUST classify as `WPS-stateless-automation-command`, load only `SKILL.md` and the automation reference, return `no-active-run`, and create no governed or automation state; with a current run they MUST classify as `WP2-governed-automated` and load both governed and automation references.

R20. A persisted automation identity that is stale or mismatches the selected change MUST stop without rebind, resume, cancellation, or mutation.

R21. Implementation MUST create `docs/changes/2026-08-11-workflow-skill-simplification/workflow-rule-disposition.yaml` and account for every behaviorally significant current rule or duplication cluster with stable rule ID, source locations, behavior, governing requirement IDs, applicable assemblies, disposition, destination, and preservation proof.

R22. Semantic-rule disposition MUST use exactly one of `retained-inline`, `retained-governed-reference`, `retained-automation-reference`, `retained-guide-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; unknown or missing values MUST fail closed before destination consistency checks, and no rule MAY disappear without one disposition.

R23. Implementation MUST separately create `docs/changes/2026-08-11-workflow-skill-simplification/workflow-literal-compatibility.yaml` with literal ID, literal, source location, consumers, classification, required semantics, disposition, and replacement when applicable.

R24. Literal classification MUST use exactly one of `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`; unknown or missing values MUST fail closed before treatment consistency checks. Normative literals MUST be preserved unless their governing contract changes, parser or package literals MUST migrate atomically with consumers, incidental tests MUST be updated instead of owning prose, and obsolete literals MUST be removed only with evidence.

R25. Permanent validation MUST retain existing owners for approved contract literals, closed vocabulary, required headings and schema, Resource-map syntax, containment, mapped-resource existence, generated inventory, archive and installed package parity, placeholders, and deterministic claim restrictions; change-local ledgers, scenarios, measurements, duplication counts, and semantic review MUST NOT create a new permanent validator family.

R26. Resource measurement MUST use canonical authored files normalized to LF, count each unique loaded resource once, and report exact resource identities, UTF-8 bytes, and Unicode whitespace-separated words for `SKILL.md`, every reference and asset, `WP0` through `WP4`, `WPB`, `WPS`, independently boundary-triggered variants, and the total package.

R27. Acceptance MUST require material `WP0-generic-routing` reduction, no unjustified regression in other assemblies, complete semantic and literal inventories, one owner per duplicated rule, honest total-package accounting, and preserved semantic and lifecycle behavior. The proposed 35–50 percent `WP0` reduction MUST remain a non-normative planning target.

R28. Acceptance proof MUST use deterministic structural checks, static contract fixtures, existing package and adapter parity checks, and independent semantic review; it MUST cover every valid assembly including `WPS`, bootstrap order, governed reads and mutation, status and off with and without a run, invalid authority, active automation plus guide authoring, contradictory state, missing or mixed resources, milestone settlement, review findings, and final holistic review.

R29. Implementation, verification, release, and repository acceptance MUST NOT execute or grade Codex, Claude Code, opencode, or another target-agent runtime, send prompt journeys, retain transcripts, select model versions, or use nondeterministic retry evidence.

R30. Existing lifecycle stage order, stage obligations, isolation, mutation authority, review outcomes, milestone semantics, automation persistence schema and authorization meaning, claim ownership, and downstream handoff MUST remain unchanged except for the specified resource-loading and fail-safe behavior.

R31. The change MUST receive one recorded architecture assessment after approved spec review. The assessment MUST classify whether the existing architecture's workflow-automation component wording and package model require an architecture update; ambiguity MUST pause automation, and any required architecture work MUST remain owned by this change.

R32. Rollout MUST update canonical `SKILL.md`, all three new references, the retained boundary reference and skeleton mapping, inventories, static fixtures, validator consumers, and package proof atomically; rollback MUST restore the prior complete canonical package and regenerate every derived target without mixed ownership or resource versions.

## Boundary model

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R4, R5, R19, R22, R24, R28 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R6, R7, R8, R9, R10, R11, R19, R20, R30, R31 | BND-STATE-001 | - |
| identity-authority | applicable | R1, R2, R6, R7, R9, R11, R12, R13, R20, R24, R30 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R5, R10, R12, R13, R14, R15, R18 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R7, R8, R9, R19, R20, R28, R30, R32 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R8, R9, R15, R16, R17, R20, R22, R24, R27, R31, R32 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R24, R25, R30, R31, R32 | BND-COMPAT-001 | - |
| external-environment | applicable | R16, R17, R25, R26, R28, R29, R32 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R4, R5, R19, R22, R24, R28 | four predicates; seven valid assemblies; invalid combinations; closed ledger values | Every invocation has one assembly or explicit stop; closed values fail before consistency checks. | Valid inputs select exact resources; invalid combinations stop; unknown values fail closed. | R5 |
| BND-STATE-001 | state-lifecycle | R6, R7, R8, R9, R10, R11, R19, R20, R30, R31 | command -> bootstrap -> governed validation -> armed persistence; governed read or transition; status or cancellation | Command context is not durable authority; lifecycle transitions remain governed-owned. | Current valid state proceeds; stale, mismatched, ambiguous, or illegal state stops without mutation. | R7 |
| BND-AUTH-001 | identity-authority | R1, R2, R6, R7, R9, R11, R12, R13, R20, R24, R30 | workflow, governed record, automation command, durable run, references, guide, asset, tests | Durable state establishes authority; each package resource has one owner; tests and chat do not own policy. | The declared owner decides; inferred, stale, conflicting, or incidental authority is rejected. | R1 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R5, R10, R12, R13, R14, R15, R18 | `SKILL.md` plus conditionally loaded governed, automation, guide, boundary, and skeleton resources | Universal rules remain inline; exact triggers assemble unique resources; references do not override or duplicate contracts. | Complete applicable assemblies proceed; contradictory, duplicated, escaped, or inapplicable loading stops or fails proof. | R3 |
| BND-TEMPORAL-001 | temporal-retry | R7, R8, R9, R19, R20, R28, R30, R32 | pre-persistence bootstrap, current or stale run, pause, resume, cancellation, rollout, rollback | Bootstrap is transient; identity remains bound to one change; package versions change atomically. | Valid ordering proceeds; early persistence, stale resume, combined guide mutation, or partial rollout stops. | R8 |
| BND-RECOVERY-001 | failure-recovery | R8, R9, R15, R16, R17, R20, R22, R24, R27, R31, R32 | invalid profile, contradiction, missing resource, mixed version, unknown ledger value, architecture ambiguity, rollback | Unsafe or unknown conditions fail closed without weakening the last valid contract or package. | Repair routes to the owning spec, package, evidence, or architecture surface; no missing procedure is invented. | R17 |
| BND-COMPAT-001 | compatibility-migration | R24, R25, R30, R31, R32 | normative and parser literals, incidental tests, existing state schema, architecture wording, generated packages | Existing lifecycle and persistence semantics remain valid; real contracts migrate atomically. | Contract consumers remain compatible; stale documentation is updated by its owner; rollback preserves history. | R30 |
| BND-ENV-001 | external-environment | R16, R17, R25, R26, R28, R29, R32 | canonical filesystem, generated trees, adapter archives, installed packages, unavailable files, target runtime | Acceptance is repository-owned and deterministic; required resources remain contained and present. | Filesystem and package proof passes or fails deterministically; target-runtime evidence is rejected. | R29 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R6, R7, R8, R20 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | An automation command is persisted as armed authority before governed identity is valid. | Bootstrap remains transient and persistence occurs only after governed validation and reclassification. |
| INT-002 | R5, R9, R13 | BND-INPUT-001, BND-STATE-001, BND-COMPOSE-001 | Guide authoring changes the interpretation surface of an active automated run. | The combined invocation stops and guide authoring waits for an inactive run. |
| INT-003 | R10, R11, R12, R15 | BND-AUTH-001, BND-COMPOSE-001 | Automation or guide procedure redefines lifecycle applicability or source precedence. | Governed and inline owners remain authoritative and contradiction stops the operation. |
| INT-004 | R16, R17, R18 | BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001 | Progressive disclosure attempts to continue with a missing or mixed required resource. | The affected operation stops without fallback reconstruction while untriggered resources remain unloaded. |
| INT-005 | R21, R22, R23, R24 | BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001 | A semantic rule disappears or an incidental test literal freezes duplicated prose. | Separate ledgers preserve behavior and migrate only genuine literal contracts. |
| INT-006 | R25, R26, R27, R29 | BND-RECOVERY-001, BND-ENV-001 | File shrinkage or model-runtime evidence disguises package growth or semantic loss. | Assembly and total-package metrics remain honest and semantic acceptance uses deterministic proof. |
| INT-007 | R30, R31, R32 | BND-STATE-001, BND-COMPAT-001, BND-RECOVERY-001 | Packaging changes silently alter workflow state architecture or leave stale architecture guidance. | Architecture assessment routes required documentation under this change and rollout preserves existing state semantics. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R5 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E2 | illustration | R10 | BND-STATE-001 | - | - |
| E3 | illustration | R7 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | - | - |
| E4 | illustration | R6 | BND-STATE-001, BND-AUTH-001 | - | - |
| E5 | illustration | R9 | BND-STATE-001 | - | - |
| E6 | illustration | R16, R17 | BND-RECOVERY-001, BND-ENV-001 | - | - |
| E7 | illustration | R12 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E8 | illustration | R24 | BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001 | - | - |
| E9 | illustration | R19 | BND-INPUT-001, BND-STATE-001, BND-TEMPORAL-001 | - | - |

## Inputs and outputs

Inputs:

- accepted proposal and approving proposal-review evidence;
- current canonical `workflow` package and mapped resources;
- governing skill, workflow, boundary-first, package-integrity, and architecture contracts;
- existing lifecycle and automation state schemas and deterministic validators;
- current exact-text consumers, adapter targets, and installed package proof.

Outputs:

- simplified canonical `SKILL.md`;
- governed lifecycle, bounded automation, and guide-authoring references;
- retained boundary reference and workflow-guide skeleton mapping;
- semantic-rule and literal-compatibility inventories;
- static assembly, authority, failure, lifecycle, and package fixtures;
- before-and-after assembly and total-package measurements;
- deterministic package proof and independent semantic review.

## State and invariants

- `skills/workflow/` remains the only authored workflow package source.
- `workflow` remains the lifecycle and routing owner.
- Every invocation has one of seven valid assemblies or an explicit stop outcome.
- Command context never substitutes for durable automation authority.
- Bootstrap is transient and persists nothing before governed validation.
- Universal safety and classification remain inline.
- Governed procedure owns applicability and lifecycle transitions.
- Automation and guide procedure consume but do not redefine governing contracts.
- Required resources fail safe; untriggered resources remain unloaded.
- Existing lifecycle and automation schemas and meanings remain unchanged.
- Generated, archived, and installed packages remain derived and equivalent.

## Error and boundary behavior

- Missing, stale, mismatched, contradictory, or ambiguous governed or automation identity stops before mutation.
- Invalid predicate combinations stop with an explicit reason.
- Active automation plus guide authoring stops without modifying either surface.
- Missing or unreadable required resources stop before dependent interpretation or action.
- Mixed package versions stop without combining partial procedure.
- Package contradictions stop instead of using guessed precedence.
- Unknown semantic dispositions or literal classifications fail closed.
- A significant rule without one destination blocks acceptance.
- A target-agent journey, transcript grader, model selector, or nondeterministic retry is rejected as acceptance proof.
- Architecture ambiguity pauses before planning.
- Partial rollout restores the last complete package.

## Compatibility and migration

Existing lifecycle order, state schema, automation persistence, command spelling, `no-active-run` outcome, stage authority, review settlement, milestone behavior, and handoff meanings remain compatible.
No user-data or persistent-state migration is required.

Real parser, package, schema, and normative-text dependencies migrate atomically with their consumers.
Incidental wording tests may change with simplified prose.
Historical review records and adapter archives remain immutable historical evidence.

Rollback restores the prior complete canonical package and regenerates derived targets from that revision.

## Observability

Change-local evidence records:

- classified assembly and exact loaded resources;
- bootstrap ordering and persistence boundary;
- rule and literal counts, owners, classifications, and destinations;
- deterministic scenario and selected-validator outcomes;
- common-path and total-package measurements;
- canonical, generated, archived, and installed resource parity;
- architecture assessment and independent semantic review results.

Diagnostics identify the invocation profile, missing or conflicting authority, affected resource, violated invariant, and owning repair surface.
No prompt, transcript, model identity, or runtime retry is recorded as acceptance proof.

## Security and privacy

Acceptance uses repository-local source, fixtures, temporary generated trees, adapter archives, and review artifacts.
No credentials, private prompts, model transcripts, network model access, or user data are required.
Mapped-resource containment rejects traversal outside the workflow skill root.

## Accessibility and UX

No graphical interface is introduced.
The shortened dispatcher and diagnostics retain stable command spellings, stage names, result vocabulary, IDs, and actionable stop guidance.

## Performance expectations

`WP0-generic-routing` must show material loaded-word and UTF-8-byte reduction without semantic loss.
Other assemblies must not regress without explicit justification.
The 35–50 percent `WP0` range is advisory and cannot override lifecycle correctness, package parity, or review quality.

## Edge cases

EC1. A rule applies to every assembly: retain it inline even when related conditional procedure moves.

EC2. A read-only audit depends on current governed state: load governed procedure but do not infer mutation authority.

EC3. `auto: status` has no selected change and no run: classify as `WPS`, load automation procedure only, and return `no-active-run` without state creation.

EC4. A new automation target cannot establish governed identity: stop in `WPB` without persisting an armed run.

EC5. Automation identity names another change: stop without rebind, resume, cancellation, or mutation.

EC6. Guide authoring occurs with a governed record but no active automation: `WP4` is valid and loads governed plus guide resources.

EC7. A required reference is present but unreadable: treat it as unavailable and stop the affected operation.

EC8. A required reference and `SKILL.md` disagree: stop as a package defect rather than selecting a local winner.

EC9. A phrase has both parser and test consumers: classify it as `parser-or-package-contract` and migrate every consumer atomically.

EC10. Main-file reduction increases `WP1` or total package size: report the delta and require semantic and profile-level justification.

EC11. The architecture model already supports mapped references but names only `SKILL.md` as the automation-semantics location: update the owning architecture wording under this change without inventing a new ADR unless the normative model changes.

## Non-goals

- Changing standard workflow order, lifecycle state, automation persistence, review gates, milestones, claims, or handoff authority.
- Simplifying another skill or creating a new stage skill.
- Creating a routing engine, selector service, scheduler, runtime, API, state store, or dependency.
- Certifying target-agent interpretation or deterministic model routing.
- Adding prompt journeys, transcript grading, model matrices, runtime-version evidence, or nondeterministic retries.
- Adding permanent simplicity, tokenizer, line-count, word-count, prose-quality, selector, or standalone validator machinery.
- Hand-editing generated adapter packages or installed skill copies.
- Rewriting historical review records or adapter archives.

## Acceptance criteria

| ID | Acceptance criterion | Requirement IDs |
| --- | --- | --- |
| AC1 | Exactly four predicates produce the seven valid assemblies and explicit stops for every other combination. | R4-R5, R9, R19 |
| AC2 | Command context is not armed authority and bootstrap validates governed identity before persistence. | R6-R8 |
| AC3 | Universal classification, precedence, isolation, stop, claim, ownership, boundary, trigger, and result policy remains inline. | R2 |
| AC4 | Governed procedure owns lifecycle and architecture applicability and loads for read-only as well as mutating governed decisions. | R10-R11 |
| AC5 | Automation consumes governed transitions and owns only automation-specific procedure. | R12, R19-R20 |
| AC6 | Guide authoring and the skeleton own only guide procedure and structure; active automation cannot combine with guide authoring. | R9, R13-R14 |
| AC7 | References cannot override one another and every required-resource failure stops without fallback reconstruction. | R15-R18 |
| AC8 | Every significant semantic rule has one valid disposition, destination, assembly set, and preservation proof. | R21-R22 |
| AC9 | Every discovered literal dependency has one valid classification and treatment separate from semantic preservation. | R23-R24 |
| AC10 | Permanent validation retains existing invariant owners and no new simplicity validator family is introduced. | R25 |
| AC11 | Assembly and package measurements use canonical LF-normalized resources, words, bytes, and exact identities. | R26-R27 |
| AC12 | Static fixtures directly prove valid, invalid, bootstrap, authority, failure, lifecycle, and package outcomes. | R28 |
| AC13 | No acceptance step executes or grades a target-agent runtime or introduces runtime evidence. | R29 |
| AC14 | Existing lifecycle, persistence, review, milestone, claim, and handoff semantics remain unchanged. | R30 |
| AC15 | A recorded architecture assessment resolves documentation and model applicability under this change before planning. | R31 |
| AC16 | Atomic rollout and rollback preserve one complete canonical and derived package revision. | R3, R32 |

## Open questions

None.

The plan must inventory exact literal consumers and existing validator commands, but those execution details do not alter this behavioral contract.

## Next artifacts

- Formal spec review.
- Recorded architecture assessment.
- Architecture and architecture review when the assessment is `architecture-required`.
- Execution plan and plan review.
- Test specification and test-spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.

The contract defines observable loading, ownership, bootstrap, failure, compatibility, proof, and rollout behavior without changing the existing workflow state model or introducing target-runtime acceptance.
