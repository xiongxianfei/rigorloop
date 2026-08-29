<!-- Template: proposal-skeleton-v1; Skill: proposal; Template status: normative -->

# Consolidate RigorLoop Review Gates

## Owning change record

`docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml`

## Problem

RigorLoop currently assigns a separate review gate to nearly every major authoring artifact:

```text
proposal
-> proposal-review
-> spec
-> spec-review
-> architecture
-> architecture-review
-> plan
-> plan-review
-> test-spec
-> test-spec-review
-> implement
-> code-review
-> verify
```

Each artifact has a useful and distinct authoring responsibility, but a separate artifact does not always represent a separate engineering decision. Architecture and specification jointly define the design that delivery must realize. The execution plan and test specification jointly define how that design will be implemented and proved. Reviewing each half independently permits one artifact to be approved before its necessary counterpart exposes a contradiction, missing constraint, untestable requirement, poor milestone boundary, or inadequate proof strategy.

Artifact-by-artifact approval also makes lifecycle state, retry behavior, review recording, settlement, routing, skill instructions, and compatibility handling more complicated than the underlying decisions require. Agents and developers repeat closely related review work, while ordinary changes pay the coordination cost of four pre-implementation artifact reviews even when the real authorization questions are only whether the design is coherent and whether delivery is executable and provable.

This structure makes later simplification risky. In particular, reducing proposal-stage detail before downstream ownership is organized around clear decision gates could remove information without establishing where the displaced reasoning belongs.

RigorLoop needs to preserve useful authored artifacts and independent review while consolidating mandatory reviews around the distinct decisions that authorize progression.

## Goals

- Reduce the number of mandatory review gates without removing useful authoring artifacts.
- Preserve independent review, durable review evidence, and author/reviewer separation.
- Organize review authority around distinct engineering decisions rather than file boundaries.
- Keep one explicit feasibility evaluation inside the proposal and have Proposal Review assess it with the proposed direction.
- Let architecture constraints shape the specification before either is approved.
- Review the execution plan and proof strategy as one coherent delivery package.
- Make the authority granted by each review gate explicit.
- Preserve precise traceability from every finding to one artifact, a cross-artifact relationship, or an upstream decision.
- Prevent partial package states that imply one mutually dependent artifact is approved while the other requires revision.
- Reduce lifecycle, settlement, retry, routing, validation, and repeated skill-instruction complexity.
- Establish a stable workflow foundation before separately simplifying the proposal-stage contract.
- Keep workflow depth proportional while retaining strong assurance for ordinary and high-risk engineering changes.

## Non-goals

- Do not merge architecture and specification into one authoring artifact.
- Do not merge the execution plan and test specification into one authoring artifact.
- Do not introduce combined `design` or `delivery` authoring skills.
- Do not simplify proposal contents in this change.
- Do not remove feasibility analysis from proposal-stage decision-making.
- Do not define the exact lifecycle schema or `change.yaml` representation.
- Do not define CLI commands for package settlement or review recording.
- Do not define detailed hashing, identity, retry, stale-evidence, migration, or settlement mechanics.
- Do not remove milestone-level code review when the approved delivery design requires it.
- Do not change the semantic responsibilities of `explain-change`, final verification, or pull-request preparation.
- Do not establish multiple workflow profiles or separate workflow lanes by change size or risk.
- Do not require long documents merely to prove that each named artifact exists.
- Do not create a standalone feasibility artifact, authoring skill, or review gate; feasibility remains an explicit part of the proposal and Proposal Review.

## Vision fit

fits the current vision

The proposal preserves RigorLoop's traceable chain of durable, separately owned artifacts while making review evidence correspond more directly to the decisions humans and agents need to trust. Package-level review strengthens design-to-implementation consistency, keeps findings reviewable in Git, and makes workflow state easier to understand and resume. It does not trade away independent review, proof design, verification, or human judgment for speed.

## Context

The current workflow contract requires or conditionally invokes `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `test-spec-review`, `code-review`, and `verify`. Prior accepted changes deliberately added independent test-spec review and strengthened review independence and durable recording. This proposal retains those assurances but changes where pre-implementation judgment is assembled: proof-map adequacy becomes part of a broader delivery decision, and architecture/specification coherence becomes part of a broader design decision.

The governing principle is:

> A review gate should exist only when it authorizes a distinct engineering decision, not merely because a separate artifact exists.

The repository currently has no canonical standalone `feasibility` skill or feasibility artifact type. This proposal therefore keeps feasibility as an explicit section within the proposal, optionally supported by linked research when the assessment depends on uncertain external or technical facts. Proposal Review evaluates that section together with the proposed direction. This preserves feasibility judgment without introducing another authoring artifact, authoring skill, or review gate.

The intended first-slice workflow is:

```text
Proposal
  |
Feasibility evidence
  |
Proposal Review
  |
Architecture
  |
Specification
  ^
  | design reconciliation
  v
Design Review
  |
Plan
  |
Test Specification
  ^
  | delivery reconciliation
  v
Delivery Review
  |
Implementation milestones <-> Code Review
  |
Final Code Review, when required
  |
Explain Change
  |
Verify
  |
Pull Request
```

The authoring artifacts remain separate because they own different reasoning. Consolidation applies to approval decisions and package settlement, not authorship.

## Feasibility

Assessment: feasible with a bounded release-cutover constraint.

The first slice preserves the existing proposal, architecture, specification, execution-plan, and test-specification authoring responsibilities. It changes how related artifacts are reviewed and settled rather than merging their contents or transferring their ownership. This limits implementation risk compared with simultaneously consolidating reviews, merging authoring artifacts, simplifying proposal content, and redesigning the complete lifecycle.

No known conceptual blocker prevents Design Review from evaluating architecture and specification as one package or Delivery Review from evaluating plan and test specification as one package. Existing independent-review, durable-recording, finding-attribution, review-resolution, and final-verification mechanisms provide reusable foundations, although their stage vocabularies and package identities will require coordinated amendment.

The principal feasibility constraint is cutover. The old progression mechanism remains authoritative while this change is implemented, and the consolidated mechanism becomes authoritative only in one complete reviewed release after nonterminal legacy-dependent work is closed. The downstream specification and architecture must prove that boundary without adding a permanent activation manifest, per-change topology marker, baseline inventory, or compatibility interpreter.

The change also requires coordinated updates to workflow routing, lifecycle interpretation, review recording and settlement, canonical review skills and assets, validation vocabularies, documentation, examples, and generated adapter or release packages. Those surfaces are substantial but bounded and already participate in repository-owned generation and validation paths.

The direction remains feasible only if package review preserves exact component-artifact identity, independent judgment, precise finding ownership, and a recoverable cutover. Failure to define those properties would block implementation rather than justify falling back to implicit or mixed gate authority.

## Options Considered

### Option 1: Retain artifact-by-artifact review

Keep `spec-review`, `architecture-review`, `plan-review`, and `test-spec-review` as separate progression gates.

This avoids migration and preserves existing skills and lifecycle state unchanged. It also preserves the current coordination cost and allows mutually dependent artifacts to reach mismatched review states. Reject because it does not address the challenge.

### Option 2: Consolidate only one package

Create either Design Review for architecture and specification or Delivery Review for plan and test specification, while retaining separate reviews for the other pair.

This limits migration scope and could provide early evidence about package review. It leaves the same underlying artifact-versus-decision mismatch in the unconsolidated half, creates an asymmetrical workflow, and delays much of the lifecycle simplification. Reject as the target direction, though downstream implementation may still roll out the approved packages sequentially.

### Option 3: Merge authoring artifacts as well as reviews

Replace architecture plus specification with one design artifact and plan plus test specification with one delivery artifact.

This could reduce artifact count and make package identity simple. It would combine distinct authorship responsibilities, require a much broader contract and migration redesign, and make it harder to attribute findings and preserve specialized reasoning. Reject for the first slice.

### Option 4: Consolidate approval around coherent decision packages

Keep the existing authoring responsibilities, but replace separate architecture/specification approval with Design Review and separate plan/test-spec approval with Delivery Review. Preserve Proposal Review, Code Review, and Verify as distinct gates.

This aligns each gate with one authorization decision, exposes semantic coupling that already exists, preserves precise artifact ownership, and reduces mandatory gate count without discarding useful evidence. It requires broader reviewers and coordinated cutover work, but those costs directly support a simpler steady-state lifecycle. Recommend this option.

## Recommended Direction

Adopt Option 4 and organize the standard workflow around five review decisions:

```text
Should we pursue it?
-> Proposal Review

Is the design sound?
-> Design Review

Can we implement and prove it?
-> Delivery Review

Did we implement it correctly?
-> Code Review

Does the complete evidence support readiness?
-> Verify
```

### Proposal Review

Proposal Review consumes the proposal, including its Feasibility section and any linked supporting research. It decides whether the direction is valuable, sufficiently bounded, and feasible enough to justify design work. Approval authorizes architecture and specification authoring; it does not approve detailed behavior, architecture, implementation, or proof design.

Feasibility does not receive a separate authoring artifact, skill, or mandatory review gate. The downstream specification must define how Proposal Review judges the embedded evaluation, when supporting research is needed, and how insufficient or stale feasibility evidence routes back to proposal revision.

### Design Review

Design Review consumes architecture, specification, applicable ADRs, and the accepted proposal package, including feasibility constraints. Architecture should normally establish the technical design envelope before specification is finalized, while specification may expose missing architecture decisions. The two authoring owners reconcile their artifacts until the package is mutually coherent.

The review decides whether architecture and specification form a sound, feasible, internally consistent design that preserves the accepted proposal direction. It evaluates whether architecture supports the specified behavior, specification respects real constraints, approved goals were not weakened for implementation convenience, system and authority boundaries are coherent, compatibility and migration concerns align, and contradictions are resolved.

Approval authorizes plan and test-spec authoring. It settles the design package only when all included artifacts and applicable ADRs are coherent and material findings are resolved. It does not authorize implementation.

### Delivery Review

Delivery Review consumes the execution plan, test specification, and accepted design package. Plan and test-spec owners reconcile implementation structure and proof strategy before the package is reviewed.

The review decides whether the design can be implemented in safe, reviewable increments and whether planned evidence can adequately prove it. It evaluates the complete chain:

```text
requirement
-> architectural boundary
-> implementation milestone
-> required proof
-> validation command or manual evidence
```

Review should detect requirements without milestone ownership, milestones that are too broad or poorly ordered, proof at the wrong boundary, architecture risks without validation, compatibility or migration work without evidence, and tests whose feasible sequencing contradicts the plan.

Approval authorizes implementation. Plan approval and test-spec approval no longer operate as separate mandatory progression gates.

### Code Review

Code Review remains independent from implementation authorship. It consumes the implementation changes, accepted design and delivery packages, and current test and validation evidence. It decides whether the implementation correctly realizes the accepted design and satisfies the relevant milestone and proof obligations.

Milestone-level review continues when the delivery package calls for it. A final holistic review remains available or required when cross-milestone interactions cannot be assessed adequately in isolation. Clean required Code Review authorizes final explanation and verification work, subject to review-resolution and other existing closeout gates.

### Verify

Verify remains separate from Code Review. It consumes the current proposal, design, and delivery packages; implementation and Code Review evidence; the explain-change artifact; and current validation results. It decides whether the complete, current, coherent evidence set supports readiness for pull-request integration. Passing implementation tests or Code Review alone does not establish readiness.

### Separate authorship and precise findings

Consolidated review must not create consolidated authorship:

```text
architecture owns architecture artifacts
spec owns specification artifacts
plan owns execution-plan artifacts
test-spec owns proof-design artifacts
review skills own independent findings and review evidence
workflow owns routing
```

A combined reviewer must not silently edit and approve its review targets. Every material finding identifies one of these scopes:

```text
F-12 -> specification
F-13 -> architecture
F-14 -> architecture/specification inconsistency
F-15 -> accepted proposal direction may need revision
F-16 -> plan/test-spec inconsistency
```

Artifact-local findings route to the owning authoring stage. Cross-artifact findings route to each necessary owner for reconciliation. Findings that require changing an accepted upstream direction route back to Proposal rather than being silently resolved within Design Review or Delivery Review.

### Coherent package settlement

Design Review should not leave a current package in a state equivalent to `specification: approved` and `architecture: revision required`. Delivery Review should not leave a current package in a state equivalent to `plan: approved` and `test specification: revision required`. Package approval applies only to the exact mutually coherent set reviewed together.

The downstream specification and architecture own exact state, identity, hashing, stale-evidence, retry, migration, and settlement mechanics. Those mechanics should preserve artifact-level traceability without allowing partial package approval to authorize progression.

### Proportional depth

The standard gate sequence remains consistent, but evidence depth scales with the change. An ordinary bug fix may have brief proposal-linked feasibility, small design artifacts, one delivery increment, a focused proof set, and concise review receipts. A high-risk change may require substantially deeper evidence at the same gates. Artifact existence alone is not evidence quality.

## Expected Behavior Changes

- The standard pre-implementation path uses `proposal-review`, `design-review`, and `delivery-review` instead of five artifact-specific review gates.
- Every proposal using the consolidated workflow contains one explicit feasibility evaluation, and Proposal Review evaluates it with direction and scope rather than relying on an additional artifact or gate.
- Architecture and specification may iterate before one Design Review settles their exact coherent package.
- Plan and test specification may iterate before one Delivery Review settles their exact coherent package.
- A material change to either member of a settled package makes the package review stale according to downstream identity rules.
- Review results attribute findings to exact artifacts, cross-artifact relationships, or accepted upstream decisions.
- Authoring skills continue to own and revise only their artifacts; consolidated reviewers own judgment and evidence, not silent fixes.
- Implementation begins only after the delivery package is accepted and all prerequisite package evidence is current.
- Milestone Code Review, final holistic Code Review, review-resolution, explain-change, Verify, and PR responsibilities remain intact.
- Cutover is blocked until no nonterminal governed change depends on the old progression mechanism.
- Public workflow explanations become shorter and center on decision authority while retaining artifact-level traceability.

## Architecture Impact

This is a cross-component, compatibility-sensitive workflow architecture change. It affects workflow routing, stage and artifact identity, lifecycle interpretation, review settlement, stale-evidence propagation, correction routing, review-record schemas, validation vocabularies, skill inventory, packaged resources, generated adapter archives, contributor guidance, examples, and release cutover.

The architecture work should define package identity without erasing component artifact identity, assign settlement and retry authority, preserve workflow as the routing owner, define how a reviewer proves independent evaluation of multiple artifacts, and determine how current artifact entries project into package-level state. Design Review and Delivery Review become new canonical skills, and the four current progression entrypoints are retired at cutover rather than retained as compatibility facades.

Because current contracts explicitly require `spec-review`, conditionally require `architecture-review`, require `plan-review` in relevant work, and require `test-spec-review` before implementation, the consolidated workflow must amend those higher-priority contracts before any implementation or published skill claims the consolidated route is active.

## Testing and Verification Strategy

Downstream proof should cover at least:

- Proposal Review receiving and evaluating the proposal's Feasibility section and any linked supporting research;
- missing, unsupported, contradicted, or stale feasibility evaluation routing to proposal revision instead of design work;
- Design Review accepting only a mutually coherent architecture/specification package;
- either design artifact changing after review and making the package evidence stale;
- Design Review findings attributed to architecture, specification, their inconsistency, or accepted upstream direction;
- Delivery Review tracing each requirement and architecture boundary through milestone ownership and proof;
- either delivery artifact changing after review and making the package evidence stale;
- Delivery Review findings attributed to plan, test specification, their inconsistency, or upstream design;
- rejection of unknown package states, review outcomes, artifact kinds, and finding-scope vocabulary values;
- authoring/review separation and prohibition on reviewer-owned silent fixes;
- milestone Code Review and conditional final holistic Code Review routing;
- Verify consuming exact current package and implementation evidence;
- concise clean-review receipts and detailed material-finding records;
- cutover blocking while a nonterminal change still depends on old progression;
- consolidated changes rejecting stale or historical old-gate evidence as sufficient authorization;
- deterministic canonical-skill, generated-package, release-archive, manifest, documentation, and example alignment;
- pre-adoption code revert and post-adoption forward recovery without corrupting governed state.

Repository-owned validators should fail closed on every new closed vocabulary before consistency checks. Semantic package coherence remains an independent review judgment rather than being replaced by structural validation.

## Rollout and Rollback

Adopt the consolidated workflow only after specification, architecture, review-skill design, lifecycle behavior, validation, generated packages, and legacy-work checks are accepted together. Canonical workflow guidance, runtime behavior, generated packages, and release archives become authoritative in one reviewed cutover revision rather than through runtime activation state.

Existing nonterminal governed changes complete under the old mechanism before cutover. If that cannot happen, cutover remains blocked unless a separate approved migration contract is introduced. Historical review records remain readable but do not become coherent package authority.

Before the first consolidated change begins, rollback restores the prior release through a normal reviewed code revert. After adoption begins, recovery uses a forward correction or separately approved migration. Neither path destructively rewrites existing review records or infers that separate old reviews equal a coherent package.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Consolidated reviewers become too broad or superficial | Local defects or cross-artifact contradictions escape | Define focused package decision criteria, independent context requirements, and exact finding attribution. |
| One small artifact edit causes expensive package rereview | Routine revisions become slower | Make stale-evidence rules materiality-aware where safe, preserve exact identities, and permit concise rereview of unchanged dimensions without reusing stale judgment blindly. |
| Package settlement erases component traceability | Reviewers cannot tell what was reviewed or changed | Bind package identity to exact artifact revisions and keep artifact-local finding and ownership records. |
| Cutover occurs while old work remains active | Active changes become ambiguous or incorrectly authorized | Block cutover until legacy-dependent work closes or a separate migration contract is approved. |
| Removing named gates weakens prior independent-review assurance | Proof or architecture defects are discovered only during implementation | Preserve independent Design and Delivery reviews, durable recording, author/reviewer separation, and current downstream Code Review and Verify backstops. |
| New review skills duplicate large amounts of existing text | Public skill maintenance remains complex | Define shared review responsibilities and package-specific criteria during architecture without hand-editing generated output. |
| Feasibility evaluation becomes shallow or stale | Proposal Review authorizes design work without credible constraints | Require an explicit proposal section, linked research when needed, and proposal revision when evidence is insufficient, contradicted, or stale. |
| Proposal simplification expands into this change | Scope grows and downstream ownership remains unsettled | Keep proposal-contract simplification in a separate follow-up proposal after the consolidated topology is proven. |
| Proportional-depth language becomes an informal fast lane | Assurance varies unpredictably | Keep one gate sequence and scale evidence depth, not the existence or authority of required decisions. |

## Open Questions

- What exact artifact identities and hashes form a Design Review package and a Delivery Review package?
- Does a non-material edit to one package member require full rereview, scoped rereview, or deterministic confirmation that reviewed semantics are unchanged?
- How should applicable ADRs participate in Design Review identity and staleness?
- How should release validation enumerate nonterminal changes that still depend on old progression?
- When is final holistic Code Review mandatory after clean milestone reviews?
- How should autoprogression targets and profiles that currently name old review stages be retired at cutover?
- Which semantic criteria belong in review judgment and which closed structural invariants belong in repository validators?

None of these questions changes the requested directional decision. They must be resolved by specification and architecture before the new topology is enforced.

## Decision Log

- Recommend replacing separate `spec-review` and `architecture-review` progression gates with one `design-review` decision.
- Recommend replacing separate `plan-review` and `test-spec-review` progression gates with one `delivery-review` decision.
- Retain `proposal-review`, `code-review`, and `verify` as distinct gates.
- Retain separate proposal, architecture, specification, plan, and test-spec authorship; keep one feasibility evaluation inside the proposal without inventing a standalone artifact or skill.
- Make Proposal Review the owner of the direction-and-feasibility decision.
- Make Design Review the owner of coherent architecture-and-specification approval.
- Make Delivery Review the owner of coherent implementation-and-proof approval.
- Preserve independent review, durable evidence, precise finding ownership, review-resolution, and upstream correction routing.
- Require one atomic cutover contract before enforcing consolidated review gates; do not add runtime coexistence machinery.
- Defer proposal-stage simplification until this workflow refactor establishes stable downstream decision ownership.
- Defer lifecycle schema, CLI, package identity, retry, settlement, and migration mechanics to specification and architecture.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Reduce mandatory review gates without removing useful authoring artifacts | in scope | Goals, Recommended Direction |
| Organize gates around distinct engineering decisions | in scope | Problem, Recommended Direction |
| Let architecture constraints shape specification before approval | in scope | Design Review |
| Review plan and proof strategy as one delivery package | in scope | Delivery Review |
| Keep Proposal Review, Code Review, and Verify distinct | in scope | Recommended Direction, Decision Log |
| Keep one feasibility evaluation inside the proposal and have Proposal Review assess it | in scope | Feasibility, Proposal Review |
| Preserve separate artifact ownership and prevent reviewer self-approval | in scope | Separate authorship and precise findings |
| Attribute findings to exact artifacts and cross-artifact relationships | in scope | Separate authorship and precise findings |
| Settle related artifacts as coherent packages | in scope | Coherent package settlement |
| Preserve milestone-level and final holistic Code Review where required | in scope | Code Review |
| Preserve `explain-change`, Verify, and PR semantics | in scope | Non-goals, Expected Behavior Changes |
| Define the cutover before enforcing consolidated review gates | in scope | Rollout and Rollback |
| Keep workflow depth proportional without creating multiple profiles | in scope | Proportional depth, Non-goals |
| Refactor review topology before simplifying proposal content | in scope | Goals, Decision Log |
| Leave exact lifecycle schema, CLI, settlement, retry, and migration mechanics downstream | deferred follow-up | Non-goals, Open Questions |
| Avoid merging authoring artifacts or creating combined authoring skills | rejected option | Non-goals, Options Considered |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Consolidated review-gate direction and authority | core to this proposal | This is the decision the proposal asks reviewers to accept. |
| Embedded proposal feasibility evaluation | core to this proposal | Direction and feasibility jointly authorize design work without a separate artifact or skill. |
| Design Review for architecture and specification | core to this proposal | It replaces two artifact-specific approval decisions with one coherent package decision. |
| Delivery Review for plan and test specification | core to this proposal | It replaces two artifact-specific approval decisions with one implementation-and-proof decision. |
| Finding attribution and upstream correction ownership | core to this proposal | Consolidation is unsafe without precise artifact and relationship ownership. |
| Coherent package settlement principle | core to this proposal | Partial package approval must not authorize progression. |
| Cutover direction for active governed changes | same-slice dependency | Consolidated gates cannot be enforced safely while nonterminal work depends on old progression. |
| Workflow, governance, canonical skill, template, and reference updates | separate implementation slice | These surfaces implement the accepted direction after spec and architecture settle the contract. |
| Lifecycle schema, package identity, retry, staleness, and settlement mechanics | separate implementation slice | These are downstream design decisions explicitly excluded from proposal approval. |
| Validation rules and unknown-vocabulary regression proof | separate implementation slice | Enforcement follows the approved schema and review-record contracts. |
| Generated adapter and release-archive updates | separate implementation slice | Generated output follows canonical authored skill changes and package validation. |
| Existing-change migration tooling or compatibility interpreter | out of scope | The selected cutover blocks until legacy-dependent work closes; any migration requires a separate approved change. |
| Proposal artifact simplification | separate proposal | It should use the stable downstream ownership established by this change. |
| Standalone feasibility artifact, authoring skill, or review gate | out of scope | The selected direction keeps feasibility evaluation inside the proposal and Proposal Review. |
| Merging architecture with specification or plan with test spec | out of scope | Separate authorship and artifact traceability are intentionally preserved. |
| Multiple workflow profiles | out of scope | The proposal keeps one standard gate sequence with proportional evidence depth. |

## Next Artifacts

- Independent `proposal-review` of this direction and its feasibility evidence.
- If accepted, specification amendments defining observable gate authority, embedded-feasibility review behavior, package inputs, review outcomes, cutover expectations, finding attribution, staleness behavior, and acceptance criteria.
- Architecture and applicable ADR work defining package identity, lifecycle projection, settlement ownership, review-skill boundaries, migration design, and generated-package impact.
- A reviewed execution plan and proof design only after the consolidated design contract is approved under the workflow contract then in force.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. Approval would authorize specification and architecture work for the consolidated review-gate model. It would not approve the exact lifecycle schema, CLI interface, package identity, settlement or retry mechanics, migration procedure, review templates, generated package changes, or any future merging or simplification of authoring artifacts.
