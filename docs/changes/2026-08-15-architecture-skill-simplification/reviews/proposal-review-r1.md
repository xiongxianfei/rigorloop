# Proposal Review R1: Architecture Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-15-architecture-skill-simplification.md`
Reviewed artifact: commit `63d3c383`
Review date: 2026-08-15
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: ARSIM-PR1, ARSIM-PR2, ARSIM-PR3
- Open blockers: assessment recording compatibility, mixed target operations and batch completion, and structural asset policy disposition require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, complete architecture assessment, or continue the workflow

## Overall assessment

The proposal selects the right package boundary: a compact assessment and routing core, one architecture-package-method reference, one governed-authoring reference, and the three existing copied assets. The two references correspond to real activation boundaries rather than arbitrary prose fragments.

It also protects the important invariants. The accepted C4 plus arc42 plus ADR method remains intact, architecture assessment stays distinct from artifact authoring, invalid governed signals fail closed, assets remain subordinate to procedure, all real profiles must shrink, and target-agent runtime acceptance is excluded.

Three contracts remain incomplete. Assessment results and their durable workflow representation are not reconciled with current consumers or direct no-impact recording behavior; the single create/revise axis cannot represent a combined canonical update and ADR set with mixed operations or one deterministic handoff; and the current architecture skeleton contains method policy that conflicts with the proposal's structural-only asset boundary.

## What is strong

### Progressive disclosure follows real execution boundaries

No-impact assessment does not need package construction or governed mutation. Portable architecture authoring needs the method but cannot mutate lifecycle state, while governed authoring needs both method and identity-bound state procedure.

### Universal architecture safety remains inline

Source precedence, upstream readiness, smallest-surface selection, accepted-design ownership, unresolved proposal/spec routing, classifications, stops, claims, resource triggers, and handoff remain available before conditional resources load.

### Existing architecture method and resource classes are preserved

The proposal does not reopen C4, arc42, ADR, canonical-package, or copied Mermaid-style decisions. It also preserves the established `READ` reference and `COPY` asset classes and canonical-through-installed parity model.

### Simplification evidence is honest

Assessment, portable authoring, and governed authoring are measured as real loaded assemblies. Assets and total package size remain separate, and no fixed percentage, tokenizer dependency, transcript grader, or target-agent runtime is introduced.

## Material findings

### ARSIM-PR1 — Major: assessment result, recording authority, and compatibility are not one closed contract

Finding ID: ARSIM-PR1
Severity: major
Location: Classification model; Loaded procedure assemblies; Assessment isolation and recording; Expected Behavior Changes
Evidence: The proposal uses `architecture-required`, `architecture-not-required`, and `architecture-ambiguous` as `architecture_assessment_outcome`, then says a workflow-managed assessment writes existing stage-owned evidence and a direct assessment never mutates another artifact. Current workflow completion evidence is parsed through fields `Stage: architecture-assessment`, `Applicability: required | not-required`, and exact `Spec identity`; the parser does not accept `ambiguous`, while the workflow contract describes the three route-level outcomes. The current architecture skill also directs a no-impact rationale to a plan, spec, change-metadata, or PR evidence surface. The proposal therefore changes direct recording behavior while claiming assessment semantics remain unchanged, and it does not map route labels to persisted fields or define how ambiguity is durably represented before pause.
Required outcome: Define one closed assessment execution and recording matrix that distinguishes isolated assessment from workflow-managed assessment, maps semantic outcome to persisted evidence and route result, names the exact input identity, and states whether direct no-impact recording is preserved, narrowed, or intentionally changed.
Safe resolution path: Keep assessment classification inline and use separate values for semantic result and persisted applicability. Preserve the existing workflow-owned evidence fields for `required` and `not-required`; define the existing durable pause evidence for ambiguity without inventing a new parser field. For direct assessment, either retain explicitly authorized project-local rationale recording or declare the no-write behavior as an intentional contract change with compatibility and scope treatment. Unknown, contradictory, or unrepresentable assessment state must stop.
needs-decision rationale: none; the proposal can retain its package design while closing the existing and proposed assessment representations.

### ARSIM-PR2 — Major: one target operation and independent commits do not close combined canonical and ADR authoring

Finding ID: ARSIM-PR2
Severity: major
Location: Classification model; Target and transaction model; Multi-file writes, retries, and recovery
Evidence: The proposal defines one invocation-level `target_operation: create | revise`, but `canonical-update-with-adr` may revise an existing canonical package while creating one ADR, revising another, or superseding a third. It later gives each target independent evidence and commit points and permits partial completion, but it does not define the batch result, when architecture-review becomes eligible, whether already committed targets may be reviewed while siblings remain incomplete, or how retry binds the complete target set. The specification would have to invent whether operation is invocation-wide or target-local and whether a partially committed batch is a valid architecture handoff.
Required outcome: Define per-target operations and one exhaustive batch completion and handoff model for canonical-only, ADR-only, and combined actions.
Safe resolution path: Replace the singular target operation with an ordered target manifest whose entries carry target kind, exact ID/path, operation, prior identity, intended identity, governing basis, and evidence path. Define batch results such as `complete`, `partial-blocked`, and `blocked-before-write`; allow per-target idempotent reconciliation but require every required target in the bound manifest to be complete and `review-required` before one combined architecture-review handoff. A changed target manifest is a new operation and must not be adopted as an identical retry.
needs-decision rationale: none; this does not require atomic rollback or a new persistent state when the existing authoring evidence can bind the manifest.

### ARSIM-PR3 — Major: the structural-only asset boundary conflicts with the current architecture skeleton

Finding ID: ARSIM-PR3
Severity: major
Location: Goals; Architecture-package-method reference ownership; Asset ownership; Rollout and Rollback
Evidence: The proposal says the method reference owns diagram applicability, source and propagation, affected-section selection, quality scenarios, and package consistency, while assets own only headings, ordering, links, shapes, placeholders, and short fill prompts. The current architecture skeleton contains procedural rules: diagrams must be separate authored source, default diagram format is Mermaid, shared role styles should be used, component diagrams are conditional, runtime/deployment sections use explicit applicability rules, ADR links have semantic requirements, and quality scenarios use a specific stimulus/environment/response/measure model. The rollout says to preserve the assets unless a structural correction is approved, so the same method rules could remain loaded in both the reference and copied asset or be removed without an explicit compatibility disposition.
Required outcome: Classify every policy-bearing instruction in the three current assets and decide which text remains structural, moves to the method reference, or is preserved as a necessary short fill prompt without becoming a second policy owner.
Safe resolution path: Add an asset-content disposition table. Keep official headings, placeholders, relative-link slots, table shapes, and literal Mermaid styles in assets. Move applicability, source-format requirements, conditional diagram selection, adequacy rules, and quality-scenario semantics into the method reference; retain only compact non-normative fill prompts when the artifact would otherwise be unusable, with one explicit cross-reference owner. Prove new full-package composition rather than assuming byte-identical assets.
needs-decision rationale: none; the proposal already allows structural correction within the same slice and needs only a closed ownership decision.

## Architecture assessment

The expected result remains `architecture-not-required` if the revised assessment contract reuses current workflow evidence, the target manifest lives in existing authoring evidence, and asset cleanup changes no durable package method. A bounded architecture documentation correction remains appropriate only for stale package inventories or examples.

Architecture becomes required if combined authoring introduces a new persisted batch record, lifecycle state, transaction owner, or cross-target settlement authority. The revised proposal should keep this condition explicit.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-ARSIM-001` | Isolated and workflow-managed architecture assessment have separate closed recording authority. |
| `AC-ARSIM-002` | Semantic assessment outcomes map deterministically to current persisted evidence and route results. |
| `AC-ARSIM-003` | Architecture ambiguity has one durable pause representation without invented fallback. |
| `AC-ARSIM-004` | Direct no-impact rationale behavior is explicitly preserved or intentionally changed with compatibility treatment. |
| `AC-ARSIM-005` | Every canonical or ADR target has its own exact operation and identity basis. |
| `AC-ARSIM-006` | A combined action binds one complete ordered target manifest. |
| `AC-ARSIM-007` | Partial target completion has one result and cannot claim combined architecture-review eligibility. |
| `AC-ARSIM-008` | Identical retry cannot add, remove, or change a target in the manifest. |
| `AC-ARSIM-009` | Every current asset instruction has one structural, method-reference, literal-style, or removed disposition. |
| `AC-ARSIM-010` | Method applicability and adequacy rules are not duplicated in copied assets. |
| `AC-ARSIM-011` | Assessment, portable-authoring, and governed-authoring profiles all decrease in words and bytes. |
| `AC-ARSIM-012` | No target-agent runtime or separate manual semantic-review acceptance stage is introduced. |
| `AC-ARSIM-013` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path assessment, method, and governed procedure are concrete and measured. |
| User value | pass | Assessment and portable authoring should load materially less irrelevant procedure. |
| Option diversity | pass | Unchanged, editorial compression, method-only extraction, two references, fragmented references, and executable routing are materially different. |
| Decision rationale | pass | Two references follow genuine method and authority boundaries. |
| Vision fit | pass | The change supports inspectable, durable architecture work and reproducible validation. |
| Scope control | pass | Architecture-review optimization, method redesign, runtime machinery, historical rewriting, and permanent gates are excluded. |
| Assessment model | block | Semantic results, persisted fields, ambiguity, and direct recording behavior are not reconciled. |
| Resource ownership | pass with revisions | The two references have clear procedural roles, but current asset content overlaps the method owner. |
| Target transactions | block | Combined targets can require mixed operations and lack one batch handoff rule. |
| Recovery and idempotency | concern | Per-target recovery is sound, but retry identity must include the complete target manifest. |
| Structural ownership | block | Existing skeleton instructions conflict with the proposed structural-only boundary. |
| Testing boundary | pass | Static proof, package parity, and ordinary lifecycle review are proportionate; runtime execution is excluded. |
| Measurement | pass | All real procedural profiles and total package size are separated. |
| Architecture awareness | pass with revisions | `architecture-not-required` is plausible if no new batch persistence or owner is added. |
| Readiness for spec | changes-requested | ARSIM-PR1 through ARSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; optimization, solution selection, branch creation, governed proposal authoring, and formal review are all visible and classified.

## Recommended Proposal Edits

- Recommended edits: add the assessment execution/recording matrix and persisted-value mapping; replace the singular target operation with a per-target manifest and closed batch handoff; classify policy-bearing asset content and give every instruction one owner; then update risks, architecture impact, scenarios, and acceptance criteria before rereview.

## Specialized-gate group

- Active gate predicates: `initial_intent_table_context`, `scope_budget_context`
- Gate outcomes: pass for the reviewed artifact; all user goals and public-skill work items are classified with valid treatments
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-15-architecture-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-15-architecture-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-15-architecture-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-15-architecture-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-15-architecture-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

- Recommendation: revise the proposal to resolve ARSIM-PR1 through ARSIM-PR3, then run a new independent proposal review against the committed revision. No automatic downstream handoff follows this review.
