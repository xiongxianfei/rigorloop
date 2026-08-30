<!-- Template: spec-skeleton-v1; Skill: spec; Template status: normative -->

# Consolidated Review Gates

## Owning change record

`docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

[Consolidate RigorLoop Review Gates](../docs/proposals/2026-08-28-consolidate-rigorloop-review-gates.md)

## Goal and context

This specification defines the observable workflow contract for consolidating artifact-specific review gates into decision-package reviews. It preserves proposal, architecture, specification, plan, and test-specification authoring as separately owned work while reducing the standard pre-implementation review sequence to Proposal Review, Design Review, and Delivery Review.

This contract amends the applicable stage-order, stage-obligation, review-recording, lifecycle, and boundary-ownership requirements in `specs/rigorloop-workflow.md` when the consolidated workflow is released. Requirements in that workflow spec that are not explicitly replaced here remain in force.

The first slice uses one atomic release cutover rather than runtime coexistence. The old artifact-specific progression mechanism remains authoritative while this change is implemented. The release cutover occurs only after the consolidated workflow, canonical skills, generated packages, validators, and release evidence are complete; after cutover, the consolidated workflow is the only supported progression mechanism. The implementing change therefore completes under the current contract, but no activation manifest, topology marker, legacy baseline, or permanent compatibility interpreter is introduced.

## Glossary

- `legacy artifact gates`: the retiring workflow with separate `spec-review`, `architecture-review`, `plan-review`, and `test-spec-review` progression gates.
- `consolidated review gates`: the standard workflow with `proposal-review`, `design-review`, `delivery-review`, `code-review`, and `verify` decision gates.
- `accepted proposal evidence`: the current accepted proposal artifact, its embedded Feasibility section, and its current Proposal Review ID and evidence. Any relied-on research conclusion must be captured in the proposal; links and separate research artifacts remain supporting inputs rather than hidden package members.
- `design package`: one explicit member map from stable artifact IDs to the repository-relative paths of the current architecture, specification, and applicable ADRs, plus the accepted proposal constraints they must preserve.
- `delivery package`: one explicit member map from stable artifact IDs to the repository-relative paths of the current plan and test specification, plus the approved design review they operationalize.
- `package member set`: the ordered mapping from component artifact IDs to their registered repository-relative paths for one design or delivery package. The lifecycle state exposes that map directly, and each package review record binds the same map.
- `upstream review`: the accepted Proposal Review ID for a design package or the approved Design Review ID for a delivery package.
- `package invalidation`: the lifecycle transition that changes an approved package to `review-required` when an owning authoring stage records a member revision or an upstream review settlement replaces the bound review ID. Package authority does not use aggregate or per-document content hashes.
- `component artifact`: an independently authored artifact included in a review package.
- `package settlement`: the atomic lifecycle transition that records one review decision over every component in the exact reviewed package.
- `finding scope`: the closed classification that identifies whether a finding is artifact-local, cross-artifact, or requires revision of an approved upstream direction.
- `cutover`: the reviewed release boundary that retires legacy progression and makes consolidated review gates the sole supported workflow after all required surfaces and evidence are complete.

## Examples first

### Example E1: proposal feasibility is embedded

Given: A new governed workflow-policy proposal after cutover.

When: Its author prepares the proposal.

Then: The proposal contains one `## Feasibility` section with an assessment, evidence or bounded assumptions, constraints, and blockers; Proposal Review evaluates that section with direction and scope; and no standalone feasibility artifact, skill, or review gate is created.

### Example E2: coherent design approval

Given: Architecture and specification are separately authored for one change, and both bind the same accepted proposal direction.

When: Design Review approves their explicit artifact IDs and repository-relative paths together with the applicable ADRs.

Then: The design package is approved atomically, planning may begin, and neither component has independent progression authority outside the approved package.

### Example E3: design contradiction blocks the package

Given: The specification requires behavior the architecture cannot support.

When: Design Review identifies the contradiction.

Then: The review records a cross-artifact finding naming both architecture and specification, neither component is settled as an approved design package, and workflow routes correction to the required authoring owners.

### Example E4: delivery review evaluates implementation and proof together

Given: A plan assigns requirements to milestones, and a test specification maps requirements and architectural boundaries to proof.

When: Delivery Review evaluates the exact pair.

Then: Approval requires a complete trace from requirement through architectural boundary, milestone, proof, and validation evidence, and approval authorizes implementation.

### Example E5: governed component edit requires package rereview

Given: An approved design package.

When: The owning authoring stage records a change to any included architecture, specification, or applicable ADR.

Then: The lifecycle CLI changes the design package to `review-required`, retains the previous review as history, and stops downstream progression until the explicit current member map is reviewed again.

### Example E6: cutover does not strand active work

Given: The consolidated workflow is ready for release and one governed change still depends on legacy progression.

When: Workflow evaluates cutover readiness.

Then: Cutover remains blocked until that change completes under the old mechanism or an independently approved migration contract is implemented. Runtime topology inference is not introduced.

### Example E7: hybrid authority is rejected

Given: Historical evidence contains an old `spec-review` approval and current work requires Design Review authority.

When: Workflow evaluates design progression.

Then: The old individual approval remains historical evidence but grants no consolidated package authority, and the package proceeds only from one current Design Review over the complete exact package.

### Example E8: reviewer does not become author

Given: Design Review or Delivery Review finds a defect.

When: The reviewer records the finding.

Then: The reviewer does not silently edit and approve the reviewed artifacts, and workflow routes the finding to the owning authoring stage or stages before rereview.

### Example E9: CLI syntax remains an architecture decision

Given: The lifecycle CLI must record and settle package reviews atomically.

When: Architecture defines the implementation.

Then: It may extend existing generic lifecycle operations or introduce another compatible request shape, and the observable behavior in this specification remains mandatory regardless of command spelling.

## Requirements

### Stage authority

CRG-R1. After cutover, RigorLoop MUST support one standard review-gate sequence and MUST NOT require or infer a per-change review-topology value.

CRG-R2. The standard pre-implementation sequence MUST be `proposal -> proposal-review -> architecture -> spec -> design-review -> plan -> test-spec -> delivery-review -> implement`, with authoring reconciliation permitted between architecture and spec before Design Review and between plan and test spec before Delivery Review.

CRG-R3. Proposal Review, Design Review, Delivery Review, Code Review, and Verify MUST remain distinct decisions. Review depth MAY scale with change complexity, but an applicable decision gate MUST NOT be omitted because an artifact is brief.

CRG-R4. `design-review` MUST replace `spec-review` and `architecture-review` as progression authority. `delivery-review` MUST replace `plan-review` and `test-spec-review` as progression authority.

CRG-R5. At cutover, `spec-review`, `architecture-review`, `plan-review`, and `test-spec-review` MUST be retired as public progression entrypoints. Their historical records remain readable but grant no authority to new or resumed work after cutover.

CRG-R6. `design-review` and `delivery-review` MUST be canonical formal review responsibilities with independently invocable skills or equivalent public entrypoints. Retired review entrypoints MUST NOT remain as ambiguous aliases for package approval.

### Proposal and feasibility

CRG-R7. Every new governed proposal after cutover MUST contain exactly one `## Feasibility` section. The canonical proposal template and proposal authoring guidance MUST include that section.

CRG-R8. The Feasibility section MUST state an assessment, the evidence or bounded assumptions supporting it, material constraints, and any blocker that would prevent responsible design work. It MAY link to research when uncertain external or technical facts require supporting evidence.

CRG-R9. Feasibility MUST remain part of the proposal artifact. The first slice MUST NOT create a standalone feasibility artifact type, authoring skill, lifecycle state, or mandatory review gate.

CRG-R10. Proposal Review MUST evaluate direction, scope, and feasibility together. Missing, unsupported, contradicted, materially stale, or blocking feasibility evidence MUST route to proposal revision and MUST NOT authorize architecture or specification work.

CRG-R11. Proposal Review approval MUST authorize architecture and specification authoring only. It MUST NOT approve the detailed design, delivery package, implementation, or proof adequacy.

### Design package

CRG-R12. A Design Review package MUST include exactly one current architecture artifact, exactly one current specification artifact, every applicable current ADR, and the exact accepted proposal constraints relied on by the design.

CRG-R13. Architecture and specification MUST remain separately authored artifacts. Architecture owns the technical design envelope; specification owns observable behavior. Either authoring stage MAY expose a required correction in the other, but neither may silently redefine the other's owned contract.

CRG-R14. Design Review MUST determine whether architecture can support specified behavior, specification respects actual technical constraints, accepted goals are preserved, authority and system boundaries are coherent, compatibility and failure behavior agree, and contradictions are resolved.

CRG-R15. Design Review approval MUST settle the exact design package atomically and authorize plan and test-specification authoring. It MUST NOT authorize implementation.

CRG-R16. A current design package MUST NOT expose a progression-authorizing partial state in which only architecture or only specification is approved. Artifact-level projections MAY remain inspectable, but package authority exists only when the complete exact package is approved.

### Delivery package

CRG-R17. A Delivery Review package MUST include exactly one current execution plan, exactly one current test specification, and the exact approved design package they implement and prove.

CRG-R18. Plan and test specification MUST remain separately authored artifacts. Plan owns implementation sequence, milestone boundaries, dependencies, and recovery intent; test spec owns proof obligations, fixtures, validation commands, manual-evidence boundaries, and pass/fail criteria.

CRG-R19. Delivery Review MUST evaluate the trace `requirement -> architectural boundary -> implementation milestone -> required proof -> validation command or manual evidence` for every applicable requirement and architecture risk.

CRG-R20. Delivery Review MUST reject missing milestone ownership, unsafe or overly broad sequencing, proof at the wrong boundary, architecture risk without validation, compatibility or migration work without evidence, and test design that requires a different implementation order than the plan provides.

CRG-R21. Delivery Review approval MUST settle the exact delivery package atomically and authorize implementation. Plan review and test-spec review MUST NOT remain separate progression gates after cutover.

### Package identity, invalidation, and CLI behavior

CRG-R22. Every Design Review and Delivery Review record MUST bind the package kind, an explicit member mapping from stable artifact IDs to normalized repository-relative paths, one upstream review ID, review ID, review round, reviewer authority, outcome, findings, and evidence path. Package lifecycle and review records MUST NOT contain or require an aggregate package revision or per-document content hashes.

For Design Review, the upstream review ID MUST be the accepted Proposal Review ID and the review MUST consume the corresponding accepted proposal evidence. For Delivery Review, the upstream review ID MUST be the approved Design Review ID.

CRG-R23. Package membership MUST be deterministic and directly inspectable. Design members MUST appear as primary architecture, primary specification, then applicable ADRs ordered by artifact ID. Delivery members MUST appear as primary plan then primary test specification. Each member path MUST be normalized, repository-relative, safe, and consistent with its registered artifact ID, kind, role, and authoring owner.

CRG-R24. When a governed authoring operation records a revision of a package member, or when Proposal Review or Design Review settlement replaces the package's upstream review ID, the lifecycle CLI MUST atomically change the affected approved package to `review-required`, retain the prior review ID as historical evidence, and withhold progression until a current package review is approved. Direct edits outside the governed authoring workflow are not automatically detected in this first slice and MUST NOT cause the implementation to introduce content hashing as a substitute.

CRG-R25. The lifecycle CLI MUST expose enough read-only context and status information to identify each package member ID and exact path, upstream review ID, current review ID and round, package status, blockers, correction targets, and the next permitted operation without requiring users to infer paths from IDs or inspect content hashes.

CRG-R26. Lifecycle mutation MUST support authority-checked, lifecycle-revision-checked, atomic package review recording and settlement. Recording and settlement MUST validate the current explicit member map, upstream review ID, review evidence, and current package status. A failed, interrupted, mismatched, or unauthorized mutation MUST leave no progression-authorizing partial package settlement. Exact replay of an already-recorded identical review decision is idempotent.

CRG-R27. This specification does not require a new top-level CLI command name. Architecture MUST decide whether existing generic lifecycle operations are extended or another compatible request shape is introduced, while preserving the concise state-based behavior in CRG-R22 through CRG-R26.

CRG-R28. Unknown package kinds, component roles, review outcomes, finding scopes, artifact kinds, or settlement states MUST produce explicit validation or CLI errors before consistency logic can accept them.

### Findings, ownership, and correction

CRG-R29. Package review outcomes MUST use exactly `approved`, `changes-requested`, `blocked`, or `inconclusive`. Existing code-review-specific outcomes remain governed by the code-review contract.

The outcome-to-authority mapping MUST be deterministic:

| Outcome | Progression authority | Required next action |
| --- | --- | --- |
| `approved` | Design Review authorizes plan and test-specification authoring; Delivery Review authorizes implementation. | Record and atomically settle the current explicit member map and review ID, then return routing control to workflow. |
| `changes-requested` | None. | Record the attempted package review and findings; use `review-resolution` when material findings require disposition; route the named artifact-local or cross-artifact correction targets to their owners; require current package rereview after revision. |
| `blocked` | None. | Record the attempted review and the missing or contradictory upstream prerequisite; use `review-resolution` when disposition is required; route only to the named upstream owner or stop when no authorized route exists. |
| `inconclusive` | None. | Record the missing evidence and stop with no forward handoff; obtain the required input and rerun the same package review. |

Correction targets MUST be recorded separately from the outcome so one cross-artifact result can name every required owner without inventing partial package authority.

Every outcome MUST remain visible as the latest package-review attempt. Only `approved` creates or refreshes progression-authorizing package settlement. Every other outcome MUST withhold package authority, expose itself as a blocker, preserve any prior approval only as historical evidence, and expose one safe correction, evidence-acquisition, or rereview operation.

CRG-R30. Every material Design Review or Delivery Review finding MUST use exactly one finding scope: `artifact-local`, `cross-artifact`, or `upstream-direction`.

CRG-R31. An `artifact-local` finding MUST identify exactly one owning component artifact. A `cross-artifact` finding MUST identify at least two affected artifact IDs. An `upstream-direction` finding MUST identify the approved upstream artifact or package whose direction requires reconsideration.

CRG-R32. Review evidence MUST preserve stable Finding IDs, evidence, required outcome, safe resolution or decision-needed rationale, owning stage or stages, and affected artifact IDs. Consolidation MUST NOT weaken existing material-finding recording or review-resolution obligations.

CRG-R33. A combined reviewer MUST NOT edit and approve the package it reviews. Artifact-local findings route to the owning authoring stage; cross-artifact findings route to every necessary owner for reconciliation; upstream-direction findings route through workflow to the upstream proposal or design owner.

CRG-R34. Review resolution closes findings but MUST NOT substitute for a required current same-stage package rereview when reviewed component identities changed or the review outcome requires rereview.

### Cutover and recovery

CRG-R35. The consolidated workflow MUST be introduced through one reviewed release cutover. The implementation MUST NOT add an activation manifest, activation baseline, per-change `review_topology` field, or runtime old/new topology selector.

CRG-R36. Cutover MUST remain blocked while any nonterminal governed change still requires legacy progression. Such a change MUST complete before cutover unless a separate approved migration contract defines its transition; this slice MUST NOT invent automatic in-place migration.

CRG-R37. Separate historical artifact reviews MUST NOT be inferred to equal a current package review. Historical evidence remains readable but MUST NOT authorize consolidated progression.

CRG-R38. Cutover MUST be workflow-governance-owned and atomic at one reviewed release revision. It requires approved specification and architecture, canonical skill and template updates, lifecycle and validation support, no nonterminal legacy-dependent changes, and deterministic generated-package parity. Partial cutover MUST grant no consolidated progression authority.

CRG-R39. This slice MUST NOT add rollback-specific lifecycle state, CLI behavior, fixtures, or evidence requirements. Recovery within the workflow uses a forward correction or a separately approved migration and MUST NOT destructively rewrite current or historical review evidence.

CRG-R40. The implementing change itself MUST complete under the pre-cutover workflow. Approval or implementation of this specification MUST NOT retroactively change the review authority governing its own in-flight artifacts.

### Preserved downstream assurance and surfaces

CRG-R41. Milestone Code Review, required final holistic Code Review, review-resolution, `ci-maintenance` when triggered, `explain-change`, Verify, and PR ownership MUST retain their current semantic responsibilities.

CRG-R42. Verify MUST consume the current accepted proposal evidence, approved Design Review ID and member map, approved Delivery Review ID and member map, implementation and Code Review evidence, current explanation, and current validation results. Review-required, legacy-only, or partial package evidence MUST block readiness.

CRG-R43. Canonical workflow specifications, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, affected skills, skill-contract surfaces, templates, schemas, CLI behavior, validators, fixtures, examples, generated adapter manifests, and release archives MUST be updated, marked unaffected with rationale, or deferred with owner and follow-up before cutover.

CRG-R44. Generated and packaged outputs MUST be reproducible from canonical authored sources and MUST expose the same supported gate inventory and stage responsibilities as those sources.

CRG-R45. Structural validation MAY prove vocabulary, identities, references, package completeness, review-record shape, state consistency, and generated parity. It MUST NOT replace independent semantic judgment about feasibility, design coherence, delivery adequacy, implementation fidelity, or final readiness.

## Inputs and outputs

### Inputs

- one governed change identity;
- an accepted proposal with embedded feasibility evaluation;
- current architecture, specification, and applicable ADR artifact IDs and paths for Design Review;
- current plan and test-specification artifact IDs and paths for Delivery Review;
- current accepted proposal evidence and applicable upstream review IDs;
- current review findings, resolutions, and lifecycle revision;
- canonical skill, template, schema, CLI, validation, documentation, and packaging sources.

### Outputs

- a Proposal Review decision over direction and feasibility;
- a deterministic design-package member map, review record, status, and atomic settlement;
- a deterministic delivery-package member map, review record, status, and atomic settlement;
- precisely attributed findings and workflow-owned correction routes;
- package-aware lifecycle status and permitted-operation output;
- cutover evidence proving no nonterminal change depends on legacy progression;
- deterministic canonical and generated package parity evidence.

## State and invariants

- Mutable lifecycle and routing state remains solely in `docs/changes/<change-id>/change.yaml`; governed Markdown artifacts contain stable intent and one owning-change pointer.
- A design or delivery approval belongs to one explicit member ID-to-path map and one review ID.
- Every package includes exactly one current upstream review ID.
- Durable lifecycle and review state records member IDs, exact repository-relative paths, review identity, and status without aggregate or per-document content hashes.
- Component artifacts retain separate owners and identities even when package approval is atomic.
- No component-only state authorizes progression.
- A governed member-revision event or replacement upstream-review settlement invalidates the affected package approval in the first slice. Unrecorded direct edits are outside automatic detection.
- Review authority remains separate from authorship authority.
- Workflow remains the owner of routing and correction coordination.
- Package review evidence is durable and findings remain attributable to exact artifacts or relationships.
- Code Review and Verify remain separate semantic gates.

## Error and boundary behavior

- Missing or invalid Feasibility content stops at Proposal Review and routes to proposal revision.
- A missing design or delivery component makes the package incomplete and prevents review settlement.
- Conflicting upstream review IDs, duplicate component roles, unsafe paths, unknown vocabulary, or stale lifecycle revisions fail closed.
- A contradiction between package members is a cross-artifact finding and prevents approval.
- A finding that changes accepted direction routes upstream and cannot be silently absorbed by a downstream author.
- A reviewer-authored component edit invalidates independence and requires author-owned revision plus rereview.
- An interrupted package mutation leaves the prior complete state authoritative and exposes recovery information without partial authorization.
- A retired artifact-review operation cannot authorize consolidated progression.
- A nonterminal legacy-dependent change blocks cutover rather than triggering runtime inference.
- Generated-package drift blocks cutover and release packaging.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: CRG-R1, CRG-R2, CRG-R3, CRG-R4, CRG-R5, CRG-R6, CRG-R7, CRG-R8, CRG-R9, CRG-R10, CRG-R11, CRG-R12, CRG-R13, CRG-R14, CRG-R15, CRG-R16, CRG-R17, CRG-R18, CRG-R19, CRG-R20, CRG-R21, CRG-R22, CRG-R23, CRG-R24, CRG-R25, CRG-R26, CRG-R27, CRG-R28, CRG-R29, CRG-R30, CRG-R31, CRG-R32, CRG-R33, CRG-R34, CRG-R35, CRG-R36, CRG-R37, CRG-R38, CRG-R39, CRG-R40, CRG-R41, CRG-R42, CRG-R43, CRG-R44, CRG-R45

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | CRG-R1, CRG-R7, CRG-R8, CRG-R9, CRG-R10, CRG-R12, CRG-R17, CRG-R22, CRG-R28 | BND-INPUT-001 | - |
| state-lifecycle | applicable | CRG-R2, CRG-R12, CRG-R15, CRG-R16, CRG-R17, CRG-R19, CRG-R21, CRG-R24, CRG-R29, CRG-R34, CRG-R35 | BND-STATE-001 | - |
| identity-authority | applicable | CRG-R5, CRG-R13, CRG-R14, CRG-R18, CRG-R22, CRG-R29, CRG-R31, CRG-R33, CRG-R35, CRG-R37 | BND-AUTH-001 | - |
| composition-path | applicable | CRG-R12, CRG-R14, CRG-R15, CRG-R16, CRG-R17, CRG-R19, CRG-R21, CRG-R31, CRG-R33, CRG-R42 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | CRG-R23, CRG-R24, CRG-R25, CRG-R26, CRG-R27, CRG-R34 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | CRG-R10, CRG-R13, CRG-R18, CRG-R20, CRG-R26, CRG-R33, CRG-R39 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | CRG-R1, CRG-R5, CRG-R35, CRG-R36, CRG-R37, CRG-R38, CRG-R40 | BND-COMPAT-001 | - |
| external-environment | applicable | CRG-R25, CRG-R26, CRG-R27, CRG-R38, CRG-R43, CRG-R44 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | CRG-R1, CRG-R7, CRG-R8, CRG-R9, CRG-R10, CRG-R12, CRG-R17, CRG-R22, CRG-R28 | complete or incomplete feasibility; complete, missing, duplicate, unknown, or unsafe package inputs | Every admitted package has one known kind, required member roles, stable artifact IDs, and safe exact repository-relative paths. | Complete known input may proceed; missing, duplicate, unsafe, mismatched, or unknown input fails closed before review settlement. | CRG-R22 |
| BND-STATE-001 | state-lifecycle | CRG-R2, CRG-R12, CRG-R15, CRG-R16, CRG-R17, CRG-R19, CRG-R21, CRG-R24, CRG-R29, CRG-R34, CRG-R35 | authoring, review-required, approved package, changes requested, blocked, inconclusive, correction, terminal | Progression authority exists only for one current atomically approved package; every non-approved outcome grants none. | Legal transitions advance atomically; governed member edits invalidate approval; changes requested route named corrections; blocked routes upstream or stops; inconclusive stops for evidence; partial or illegal transitions stop. | CRG-R29 |
| BND-AUTH-001 | identity-authority | CRG-R5, CRG-R13, CRG-R14, CRG-R18, CRG-R22, CRG-R29, CRG-R31, CRG-R33, CRG-R35, CRG-R37 | author, reviewer, workflow router, lifecycle mutation authority, upstream-review authority, release-cutover authority | Each role mutates only its owned surface; package decisions bind one explicit member map and upstream review ID; release governance owns cutover. | Authorized operations record owned evidence; invalid upstream authority, self-approval, wrong-stage operations, cross-owner edits, and premature cutover are rejected. | CRG-R33 |
| BND-COMPOSE-001 | composition-path | CRG-R12, CRG-R14, CRG-R15, CRG-R16, CRG-R17, CRG-R19, CRG-R21, CRG-R31, CRG-R33, CRG-R42 | artifact-local path, cross-artifact path, upstream-review path, downstream verification path | Package approval covers local quality, current upstream authority, and all selected cross-artifact coherence hazards. | Coherent composition may approve; invalid upstream review, contradiction, or missing trace produces attributable blockers or findings and blocks progression. | CRG-R14 |
| BND-TEMPORAL-001 | temporal-retry | CRG-R23, CRG-R24, CRG-R25, CRG-R26, CRG-R27, CRG-R34 | first record, exact duplicate retry, stale lifecycle retry, governed member change, upstream-review change, rereview | The expected lifecycle revision, explicit member map, upstream review ID, and package status remain current throughout a mutation. | Exact duplicate is idempotent; stale lifecycle requests are rejected; governed member or upstream-review changes set the package to review-required. | CRG-R26 |
| BND-RECOVERY-001 | failure-recovery | CRG-R10, CRG-R13, CRG-R18, CRG-R20, CRG-R26, CRG-R33, CRG-R39 | review rejection, interrupted mutation, correction route | Failure never grants partial progression authority and preserves the last complete recoverable state. | Findings route to owners; interrupted settlement restores or retains prior state; workflow recovery uses forward correction or separately approved migration. | CRG-R26 |
| BND-COMPAT-001 | compatibility-migration | CRG-R1, CRG-R5, CRG-R35, CRG-R36, CRG-R37, CRG-R38, CRG-R40 | pre-cutover implementation, nonterminal legacy work, clean cutover, historical evidence | Only one progression mechanism is active at a time; historical individual reviews are not package authority; records are not destructively rewritten. | Complete prerequisites permit cutover; legacy-dependent work, partial surface updates, or mixed authority block it. | CRG-R35 |
| BND-ENV-001 | external-environment | CRG-R25, CRG-R26, CRG-R27, CRG-R38, CRG-R43, CRG-R44 | canonical sources, local CLI, generated packages, release archives, unavailable dependency | Canonical and generated public surfaces expose the same supported gates without requiring external services. | Parity permits cutover and packaging; drift, unavailable required local support, or inconsistent archives blocks the affected handoff. | CRG-R44 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | CRG-R14, CRG-R16, CRG-R31 | BND-COMPOSE-001, BND-STATE-001 | One design component appears acceptable while the other contradicts it. | Record a cross-artifact finding and leave the whole design package without progression authority. |
| INT-002 | CRG-R20, CRG-R21, CRG-R31 | BND-COMPOSE-001, BND-STATE-001 | Plan sequence and proof sequence are individually plausible but mutually incompatible. | Record a cross-artifact finding and reject atomic delivery settlement. |
| INT-003 | CRG-R24, CRG-R26, CRG-R34 | BND-TEMPORAL-001, BND-AUTH-001, BND-STATE-001 | A governed component or upstream review changes before or after package settlement. | Atomically mark the package review-required, withhold progression, and require a current package rereview; stale lifecycle requests fail unchanged. |
| INT-004 | CRG-R26 | BND-RECOVERY-001, BND-STATE-001 | Settlement interrupts after writing only part of an authoritative projection. | Preserve or restore the last complete authoritative state; partial projection grants no authority. |
| INT-005 | CRG-R35, CRG-R37 | BND-COMPAT-001, BND-AUTH-001, BND-INPUT-001 | Historical individual review evidence is presented as current package authority. | Reject it with an actionable package-authority error. |
| INT-006 | CRG-R38, CRG-R44 | BND-ENV-001, BND-COMPAT-001, BND-STATE-001 | Canonical sources switch to consolidated gates while generated packages or guidance still expose legacy progression. | Block cutover until parity and legacy-retirement proof are current. |
| INT-007 | CRG-R29, CRG-R31, CRG-R33 | BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001 | A non-approved package result names multiple correction owners or lacks evidence needed to choose one. | Grant no progression; record correction targets separately for changes requested, route a named upstream blocker, or stop an inconclusive review for missing evidence. |
| INT-008 | CRG-R35, CRG-R38 | BND-COMPAT-001, BND-AUTH-001, BND-STATE-001 | Cutover is attempted while a nonterminal change still requires legacy progression. | Block cutover and identify the change; do not add runtime topology inference or rewrite its evidence. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | CRG-R7, CRG-R8, CRG-R9, CRG-R10 | BND-INPUT-001 | - | - |
| E2 | illustration | CRG-R12, CRG-R15, CRG-R16 | BND-STATE-001, BND-COMPOSE-001 | - | - |
| E3 | illustration | CRG-R14, CRG-R31, CRG-R33 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E4 | illustration | CRG-R17, CRG-R19, CRG-R21 | BND-STATE-001, BND-COMPOSE-001 | - | - |
| E5 | illustration | CRG-R24, CRG-R34 | BND-STATE-001, BND-TEMPORAL-001 | - | - |
| E6 | illustration | CRG-R35, CRG-R36, CRG-R40 | BND-COMPAT-001 | - | - |
| E7 | illustration | CRG-R5, CRG-R37 | BND-AUTH-001, BND-COMPAT-001 | - | - |
| E8 | illustration | CRG-R13, CRG-R18, CRG-R33 | BND-AUTH-001, BND-RECOVERY-001 | - | - |
| E9 | illustration | CRG-R25, CRG-R26, CRG-R27 | BND-ENV-001, BND-TEMPORAL-001 | - | - |

Every example above illustrates requirement-owned behavior. No example creates normative behavior.

## Compatibility and migration

The old and consolidated progression mechanisms do not coexist in a released runtime. While this implementing change is in progress, the old mechanism remains authoritative. The reviewed release revision is the cutover: it removes the old progression entrypoints and publishes the complete consolidated workflow together.

Cutover requires no nonterminal governed change to depend on the old mechanism. Such work completes before release unless a separate approved migration contract is introduced. Historical review records remain readable evidence, but separate historical approvals cannot be combined into current package authority. No per-change topology marker, baseline inventory, or compatibility interpreter is required.

This slice adds no rollback-specific workflow mechanism or proof obligation. Workflow recovery uses a forward correction or separately approved migration so current evidence is not stranded or rewritten.

At cutover, the following `specs/rigorloop-workflow.md` surfaces are replaced: the per-change chain in R6, the affected stage rows in R7a, the authoring continuation stages in R7e and the active automation route, the `spec-review` handoff contract in R7i through R7o, the `plan-review` handoff in R7p, the separate test-spec-review progression contract in R7qa through R7qk, the review-skill projection in R8ka, the allowed formal review stages in R12ao, and the boundary-first stage ownership in R29c through R29g and R34 through R35. All unaffected requirements remain mandatory.

## Observability

- Design and delivery status MUST show the member artifact ID-to-path map, upstream review ID, review ID and round, package status, outcome, correction targets, open findings, blockers, and next permitted operation. It MUST NOT calculate, expose, or require an aggregate or per-document content hash for package authority.
- Review logs MUST make artifact-local, cross-artifact, and upstream-direction finding ownership visible without requiring chat history.
- CLI errors MUST name the violated invariant and relevant package, artifact, review, or lifecycle identities.
- Cutover evidence MUST identify canonical-source parity, generated-package parity, legacy-entrypoint retirement, and the absence of nonterminal legacy-dependent changes.

## Security and privacy

The consolidated workflow introduces no new secret, credential, personal-data, network, or external-account requirement. Package member sets and review evidence MUST contain stable artifact IDs and normalized repository-relative paths, not machine-local absolute paths, private runtime data, aggregate content hashes, or per-document content hashes. Review consolidation MUST NOT weaken existing author/reviewer separation, lifecycle authority checks, or repository control boundaries.

## Accessibility and UX

No end-user graphical interface is introduced. Contributor-facing CLI and Markdown output MUST use stable headings, concise decision language, and actionable errors. Design Review and Delivery Review status MUST distinguish package authority from component artifact state so users do not need to infer progression from multiple files.

## Performance expectations

Package membership resolution, status inspection, and structural validation SHOULD remain suitable for ordinary local workflow use. The first slice defines no numeric latency budget. Implementations SHOULD resolve only registered IDs, paths, review evidence, and lifecycle state and SHOULD avoid rereading document contents, unrelated repository history, or external services to determine package authority.

## Edge cases

EC1. A proposal with a Feasibility heading but no assessment or supporting basis fails Proposal Review rather than creating a separate feasibility artifact.

EC2. Supporting research changes after Proposal Review. If the change contradicts or materially weakens a feasibility conclusion captured in the accepted proposal evidence, Proposal Review evidence becomes stale and routes to proposal revision or rereview. An external link by itself is supplementary and does not become a hidden package member.

EC3. An ADR becomes applicable after Design Review. The design package is incomplete and must be rebuilt and rereviewed with the ADR included.

EC4. A spelling-only edit is recorded through the owning authoring stage. The affected package becomes `review-required`; the workflow does not attempt content hashing or semantic-equivalence inference.

EC5. Design Review approves architecture but requests specification changes. The package outcome is `changes-requested`; architecture has no independent progression authority.

EC6. Delivery Review finds adequate proof but unsafe milestone order. The package outcome is `changes-requested`, and plan revision plus package rereview are required.

EC7. One finding belongs to the specification and another to an architecture/specification contradiction. Each finding receives its own scope and affected artifact IDs.

EC8. A review finding would weaken the accepted proposal goal for convenience. It is classified `upstream-direction` and routes to proposal ownership rather than being resolved silently in design.

EC9. A nonterminal legacy change exists at the proposed cutover revision. Release validation blocks cutover and identifies it; runtime coexistence is not enabled.

EC10. A historical change lacks consolidated package evidence. Its old review records remain readable, but they do not authorize resumed consolidated progression.

EC11. After recording a package review, a caller refreshes lifecycle context and retries with the current lifecycle revision and the same review ID, explicit member map, upstream review ID, outcome, and evidence path. The operation reports the existing identical decision without creating another review. A retry with a stale lifecycle revision or mismatched review data is rejected.

EC12. Generated adapter archives expose old review skills at the proposed cutover. Release and public enforcement remain blocked until parity is restored.

EC13. A manual `design-review` or `delivery-review` invocation remains isolated by default. It records required evidence but does not route downstream unless workflow-managed continuation is authorized.

EC14. A one-milestone ordinary fix still follows Proposal Review, Design Review, Delivery Review, Code Review, and Verify when those gates apply, but each artifact and receipt may be concise.

## Non-goals

- Merging architecture and specification into one artifact.
- Merging plan and test specification into one artifact.
- Creating combined design-authoring or delivery-authoring skills.
- Simplifying the broader proposal content contract beyond adding and evaluating Feasibility.
- Creating a standalone feasibility artifact, skill, state, or review gate.
- Prescribing exact `change.yaml` package-state placement, CLI command spelling, or request-envelope schema before architecture.
- Automatically classifying component edits as semantically non-material.
- Migrating active legacy changes in place in the first slice.
- Inferring coherent package approval from separate historical reviews.
- Removing milestone Code Review, final holistic Code Review when required, review-resolution, `explain-change`, Verify, or PR preparation.
- Adding multiple workflow profiles or risk-based workflow lanes.
- Requiring large documents where concise evidence satisfies the same contract.

## Acceptance criteria

| Acceptance ID | Criteria | Governing requirements |
| --- | --- | --- |
| CRG-AC1 | A new proposal template contains one Feasibility section, Proposal Review evaluates it, and no standalone feasibility artifact or skill exists. | CRG-R7 through CRG-R10 |
| CRG-AC2 | A contributor can author architecture and specification separately, reconcile them, and obtain one Design Review decision over a visible current artifact ID-to-path member map. | CRG-R12 through CRG-R16 |
| CRG-AC3 | A contributor can author plan and test specification separately and obtain one Delivery Review decision that proves full requirement-to-evidence traceability. | CRG-R17 through CRG-R21 |
| CRG-AC4 | A governed component or upstream-review change sets the affected package to review-required and blocks progression until current rereview, without aggregate or per-document hashes. | CRG-R22 through CRG-R24 |
| CRG-AC5 | CLI status exposes exact member IDs and paths, upstream review, package status, blockers, and permitted operation, while mutation is lifecycle-revision-checked, authority-checked, idempotent, and atomic. | CRG-R25 through CRG-R28 |
| CRG-AC6 | Every package-review outcome has deterministic authority and next-action semantics, and findings are precisely classified and routed without reviewer-owned silent fixes or loss of existing review-resolution evidence. | CRG-R29 through CRG-R34 |
| CRG-AC7 | One reviewed release cutover retires old progression only after no nonterminal change depends on it; no activation manifest, baseline inventory, topology marker, or runtime selector is introduced. | CRG-R35 through CRG-R40 |
| CRG-AC8 | Code Review, Verify, explanation, and PR responsibilities retain their distinct assurance roles. | CRG-R41, CRG-R42 |
| CRG-AC9 | Canonical skills, templates, specs, guidance, schemas, CLI, validators, fixtures, generated packages, and release archives agree before cutover. | CRG-R38, CRG-R43 through CRG-R45 |
| CRG-AC10 | Every closed vocabulary rejects an unknown value before consistency checks, with regression proof for the rejection. | CRG-R28, CRG-R29, CRG-R30 |
| CRG-AC11 | All eight boundary dimensions and selected composed hazards map to direct proof without requiring a Cartesian scenario inventory. | CRG-R1 through CRG-R45 |

## Open questions

- Which smallest `change.yaml` mapping shape best exposes stable member IDs and exact repository-relative paths without duplicating unrelated artifact state?
- Should the lifecycle CLI extend existing `record-review` and settlement operations or add package-specific request operations while keeping one `lifecycle` command family?
- How should applicable ADR discovery be made deterministic before Design Review context is issued?
- Which public result fields best distinguish component state, package state, and progression authority without excessive output?

These questions are architecture-owned and do not change the observable outcomes required by this specification.

## Next artifacts

- `spec-review` for this specification under the implementing change's pre-cutover contract.
- Architecture and applicable ADR work defining explicit package membership, compact lifecycle projections, CLI invalidation and settlement shape, release cutover, review-skill composition, and generated-package impact.
- Architecture review under the implementing change's pre-cutover contract.
- A reviewed execution plan and test specification after the design is approved.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`. This specification does not claim review approval, architecture readiness, implementation readiness, verification, branch readiness, or PR readiness.
