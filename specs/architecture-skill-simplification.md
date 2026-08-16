<!-- Template: spec-skeleton-v1 | Skill: spec | Template status: normative | Maintained alongside: skills/spec/SKILL.md | Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Architecture Skill Simplification

## Owning change record

`docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Architecture Skill Simplification](../docs/proposals/2026-08-15-architecture-skill-simplification.md)
- Approved [proposal-review R3](../docs/changes/2026-08-15-architecture-skill-simplification/reviews/proposal-review-r3.md)

## Goal and context

This specification defines a shorter published `architecture` skill package without weakening architecture applicability, accepted-design ownership, the approved C4 plus arc42 plus ADR method, customer-project portability, governed lifecycle safety, interruption recovery, or architecture-review handoff.

The universal skill owns applicability and routing. One conditional method reference owns detailed package construction, one conditional governed reference owns lifecycle-authorized transactions, and the three existing assets own copied structure and literal diagram styles. Workflow-managed authoring binds the current required assessment and persists a dependency-aware prepared manifest in existing change-local authoring evidence before any target-file mutation.

## Glossary

- `assessment basis`: the current architecture-required judgment plus exact assessment receipt, governing spec, and approving spec-review identities when workflow-managed.
- `target manifest`: the ordered set of canonical architecture and ADR targets, operations, file identities, dependencies, commit groups, and intermediate-validity decisions for one authoring action.
- `commit group`: targets that cannot leave a valid intermediate repository state independently and therefore must complete together before settlement.
- `prepared authoring evidence`: ordinary change-local architecture authoring evidence that records the complete manifest before target mutation; it is not a lifecycle state or new persistence owner.
- `batch result`: exactly `complete`, `partial-blocked`, or `blocked-before-write`.

## Examples first

### Example E1: assessment-only invocation

Given architecture applicability is being assessed, when no authoring action is selected, then only the compact universal procedure loads and returns one truthful assessment result.

### Example E2: portable authoring

Given no governed signal exists and a current inline judgment is `architecture-required`, when canonical or ADR authoring is requested, then the method reference loads and no lifecycle state is written.

### Example E3: invalid governed signal

Given a malformed or conflicting change identity is present, when authoring is requested, then classification stops without portable fallback.

### Example E4: stale assessment basis

Given a workflow-managed required assessment refers to an earlier spec identity, when architecture authoring begins, then authoring stops before mutation.

### Example E5: prepared manifest precedes writes

Given governed authoring is valid, when content preparation completes, then the full manifest and intended identities are durably recorded before the first architecture, diagram, or ADR file changes.

### Example E6: interrupted canonical package

Given diagrams were written from the persisted manifest but canonical Markdown was not, when an identical retry runs, then it validates the recorded identities and resumes without adopting unrecorded files.

### Example E7: dependency-safe combined update

Given a canonical update references a new ADR and diagram, when the batch commits, then dependencies complete first and canonical Markdown is written last.

### Example E8: partial batch

Given one target completes and another fails, when the completed target is independently valid, then it may remain committed as `partial-blocked`; otherwise its commit group remains unsettled.

### Example E9: ADR supersession

Given a replacement ADR supersedes a predecessor, when authoring runs, then replacement content is validated before predecessor and canonical-reference updates, while architecture-review retains approval authority.

### Example E10: missing conditional resource

Given a triggered reference or copied asset is unavailable, when dependent work begins, then the skill stops without reconstructing procedure from memory.

## Requirements

### Package and universal ownership

R1. The canonical package MUST contain `skills/architecture/SKILL.md`, `references/architecture-package-method.md`, `references/governed-architecture-authoring.md`, `assets/architecture-skeleton.md`, `assets/adr-skeleton.md`, and `assets/diagram-styles.mmd`.

R2. `SKILL.md` MUST remain self-sufficient for evidence precedence, upstream settlement, architecture applicability, smallest-surface selection, accepted-design boundaries, action and signal classification, universal write limits, stops, claims, resource triggers, result shape, and architecture-review handoff.

R3. The method reference MUST load only for canonical or ADR authoring and MUST own detailed arc42, C4, diagram, ADR, package-consistency, quality-scenario, and affected-surface procedure.

R4. The governed reference MUST load only for one valid governed authoring candidate and MUST own complete change-record validation, artifact-entry transactions, prepared evidence, retry, concurrency, recovery, and matching `authoring → review-required` transitions.

R5. Loading either reference MUST NOT grant applicability, mutation, review, settlement, routing, or continuation authority.

R6. The resource map MUST use `READ` for both references and `COPY` for all three assets with exact contained relative paths and deterministic load conditions.

R7. A missing, unreadable, escaped, stale, contradictory, or mixed-version required resource MUST stop dependent work before reconstruction or mutation.

### Classification and assessment

R8. Assessment mode MUST be exactly `isolated` or `workflow-managed`; assessment judgment MUST be exactly `required`, `not-required`, or `ambiguous`; and route result MUST be exactly `architecture-required`, `architecture-not-required`, or `architecture-ambiguous` with the corresponding deterministic mapping.

R9. Architecture action MUST be exactly `assessment-only`, `canonical-update`, `adr-only`, `canonical-update-with-adr`, or `blocked`.

R10. Governed-signal classification MUST be exactly `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`.

R11. Any explicit change ID, workflow-managed change identity, structured owning-change field, or matching lifecycle artifact entry MUST count as a governed signal, including malformed signals.

R12. A malformed, stale, duplicated, escaped, unsafe, mismatched, or conflicting governed signal MUST stop without portable fallback.

R13. Loaded procedural assemblies MUST be exactly `AA0-assessment`, `AA1-portable-authoring`, and `AA2-governed-authoring` according to action and signal classification.

R14. Workflow-managed required and not-required assessment receipts MUST preserve `Stage: architecture-assessment`, `Applicability: required | not-required`, and exact `Spec identity`; ambiguity MUST pause without a completion receipt.

R15. Isolated assessment MUST write only to an explicit valid user-provided evidence path and MUST NOT mutate proposal, spec, plan, PR, workflow, or change state implicitly.

### Current assessment basis

R16. Every architecture authoring action MUST have a current `architecture-required` judgment.

R17. Workflow-managed authoring MUST bind one current assessment receipt, `Applicability: required`, exact governing spec identity, and current approving spec-review identity.

R18. Missing, stale, contradictory, not-required, or ambiguous assessment evidence MUST block workflow-managed authoring before mutation.

R19. A change to the governing spec identity, approving spec-review identity, accepted decision basis, architecture-relevant requirements, or applicability evidence MUST make the prior assessment basis stale.

R20. Portable authoring MUST perform a current inline applicability judgment and MUST stop on `not-required`, `ambiguous`, or unresolved proposal or spec direction.

### Targets and prepared transactions

R21. Canonical architecture and every ADR MUST be distinct manifest targets with exact target kind, artifact ID, normalized path, operation, prior identity or absence, intended identity, governing inputs, and governed evidence path when applicable.

R22. Target operations MUST be exactly `create`, `revise`, `supersede`, and `deprecate`; create requires absence, while other operations require one exact current target and authority.

R23. A combined action MUST bind one complete ordered manifest without treating multiple targets as one artifact identity.

R24. Every combined manifest MUST record dependency target IDs, commit groups, and whether each target is independently valid after commit.

R25. Governed authoring MUST prepare and validate all intended content and compute every intended file identity before target mutation.

R26. Governed authoring MUST persist the complete manifest, assessment basis, baselines, dependencies, intended identities, and commit points in existing change-local authoring evidence before the first target-file write.

R27. Prepared authoring-evidence dispositions MUST be exactly `prepared`, `partial-blocked`, `complete`, and `abandoned`, and MUST NOT be interpreted as lifecycle states or independent authorization.

R28. After preparing evidence, the skill MUST re-read assessment, authority, and baseline identities and MUST stop without target mutation if any changed.

R29. Target writes and per-target progress MUST be limited to files and identities represented by the persisted manifest; unrecorded files MUST NOT be adopted.

R30. Only a completed governed target or commit group MAY transition its matching entry to `review-required`; unrelated entries and workflow, automation, plan, and review state MUST remain unchanged.

### Dependencies, commit points, and recovery

R31. A target MUST NOT commit until every required dependency is complete and validated.

R32. Targets that cannot leave a structurally and semantically valid intermediate repository state independently MUST share one commit group.

R33. Within the canonical architecture target, subordinate diagram sources MUST be written and validated before canonical Markdown, and canonical Markdown MUST be the target commit point.

R34. Canonical Markdown MUST NOT reference an incomplete diagram or ADR dependency.

R35. ADR supersession authoring MUST create and validate replacement content before predecessor status and superseded-by updates, and MUST complete those updates before canonical-reference updates.

R36. Architecture authoring MUST NOT approve an ADR or supersession; architecture-review MUST remain the settlement owner.

R37. Batch results MUST be exactly `complete`, `partial-blocked`, and `blocked-before-write`; only `complete` MAY qualify the full manifest for architecture-review handoff.

R38. `partial-blocked` MUST preserve only completed targets proven independently valid and MUST report every completed and incomplete target.

R39. `blocked-before-write` MUST perform no target-file mutation.

R40. An identical retry MUST bind the same ordered manifest, assessment basis, inputs, paths, identities, dependencies, commit groups, and authority and MUST resume without duplicate files, evidence, entries, or transitions.

R41. Adding, removing, reordering, or changing a target or dependency MUST create a new operation rather than an identical retry.

R42. Partial recovery MUST reconcile only state matching the persisted manifest and MUST stop on unrelated, ambiguous, dangling, changed, or conflicting files, entries, dependencies, or baselines.

### Asset ownership, preservation, and acceptance

R43. `architecture-skeleton.md` MUST own official headings, ordering, links, table shapes, placeholders, and neutral fill prompts; `adr-skeleton.md` MUST own ADR structure; `diagram-styles.mmd` MUST own literal copied styles.

R44. Assets MUST NOT determine applicability, affected-section adequacy, C4 level, ADR necessity, lifecycle authority, review status, or handoff.

R45. Every current non-heading asset instruction MUST receive one `structural`, `method-owned`, `literal-style`, `neutral-prompt`, or `removed-duplicate` disposition.

R46. Every behaviorally significant rule and duplicate cluster MUST receive one owner and disposition in `architecture-rule-disposition.yaml`.

R47. Every exact compatibility-sensitive heading, label, path, enum, resource verb, and consumed phrase MUST receive one classification and disposition in `architecture-literal-compatibility.yaml`.

R48. Every new or changed closed vocabulary MUST reject unknown values before consistency checks and MUST have an unknown-value regression test.

R49. Measurements MUST use canonical authored files, LF normalization, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded procedure once in `SKILL.md`, method-reference, governed-reference order.

R50. Measurements MUST report `AA0`, `AA1`, `AA2`, each procedural resource, each asset, representative copied output, and total package size separately.

R51. All three loaded procedural assemblies MUST decrease from baseline in words and bytes; total package growth MUST be reported and justified, and no fixed percentage may override semantic preservation.

R52. Canonical, generated, archived, release-candidate, and installed resources MUST retain required inventory and raw-byte parity.

R53. Acceptance MUST use deterministic contract, fixture, validator, package, and lifecycle proof and MUST NOT execute a target-agent runtime, grade transcripts, add a prose classifier, add a tokenizer dependency, or add a separate manual semantic-review gate.

R54. If the existing authoring-evidence and lifecycle model cannot represent the prepared manifest, target progress, dependency edges, and commit groups without a new schema, persistent authority, persistence surface, or write owner, architecture assessment for this simplification MUST return `architecture-required` before planning.

## Inputs and outputs

Inputs are the accepted proposal and reviews, current architecture skill and assets, governing workflow and skill contracts, canonical architecture method, package consumers, and one governed change record when lifecycle authoring applies.

Outputs are the simplified canonical skill, two references, revised structural assets when required by the disposition ledger, directly coupled validators and fixtures, semantic and literal ledgers, profile measurements, package parity evidence, and stage-owned lifecycle evidence.

## State and invariants

- `skills/` remains the sole authored skill source.
- Applicability remains universal and cannot be delegated to a conditional reference.
- Portable authoring writes no lifecycle state.
- Governed authoring changes only manifest targets, their evidence, and matching authoring transitions.
- Prepared evidence precedes target mutation and grants no independent authority.
- Architecture-review remains the only architecture and ADR settlement owner.
- Partial completion never qualifies the combined manifest for review handoff.

## Error and boundary behavior

Every unknown vocabulary, invalid governed signal, stale assessment, unresolved target, unsafe path, illegal operation, missing authority, changed baseline, unrecorded file, dependency failure, unsafe intermediate state, concurrent write, missing resource, or parity defect fails closed with a concrete blocker. Failure before the first permitted target write leaves target files unchanged. Interrupted permitted work may resume only through the exact persisted manifest.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R8, R9, R10, R11, R12, R13, R21, R22, R27, R37 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R14, R15, R16, R17, R18, R19, R20, R25, R26, R27, R28, R29, R30, R37, R38, R39, R40, R41, R42 | BND-STATE-001 | - |
| identity-authority | applicable | R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R30, R36 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R6, R7, R23, R24, R31, R32, R33, R34, R35, R43, R44, R45 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R25, R26, R27, R28, R29, R30, R31, R32, R37, R38, R39, R40, R41, R42 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R7, R26, R28, R29, R31, R32, R33, R34, R37, R38, R39, R40, R41, R42, R54 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R43, R44, R45, R46, R47, R48, R49, R50, R51, R52 | BND-COMPAT-001 | - |
| external-environment | applicable | R7, R15, R29, R39, R42, R52, R53 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R8, R9, R10, R11, R12, R13, R21, R22, R27, R37 | assessment, action, signal, target operation, evidence disposition, and batch-result values | unknown values fail before consistency checks | one valid classification proceeds; invalid input stops | R8 |
| BND-STATE-001 | state-lifecycle | R14, R15, R16, R17, R18, R19, R20, R25, R26, R27, R28, R29, R30, R37, R38, R39, R40, R41, R42 | assessment-only, prepared, partial, complete, interrupted, stale, or conflicting state | prepared evidence precedes writes and only complete targets settle | valid work completes or reconciles; unsafe state blocks | R26 |
| BND-AUTH-001 | identity-authority | R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R30, R36 | portable, valid governed, invalid governed, current assessment, stale assessment, authoring authority, review authority | loading and assessment do not grant mutation or settlement | exact current authority permits bounded writes; other states stop | R17 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R6, R7, R23, R24, R31, R32, R33, R34, R35, R43, R44, R45 | common file, two references, three assets, canonical Markdown, diagrams, and ADR targets | one owner per rule and no exposed incomplete dependency | valid composed package proceeds; missing or unsafe composition stops | R1 |
| BND-TEMPORAL-001 | temporal-retry | R25, R26, R27, R28, R29, R30, R31, R32, R37, R38, R39, R40, R41, R42 | first attempt, pre-write interruption, partial write, identical retry, changed operation, concurrent write | retry identity never silently rebinds | exact retry resumes once; changed or competing state stops | R40 |
| BND-RECOVERY-001 | failure-recovery | R7, R26, R28, R29, R31, R32, R33, R34, R37, R38, R39, R40, R41, R42, R54 | no write, safe partial target, unsafe group, missing evidence capability, unrecorded file | only persisted and independently valid state can be preserved | safe state reconciles; unsafe state or missing architecture support blocks | R42 |
| BND-COMPAT-001 | compatibility-migration | R43, R44, R45, R46, R47, R48, R49, R50, R51, R52 | structural, method-owned, literal, parser-sensitive, incidental, obsolete, canonical, or derived content | semantic and literal preservation are separate and derived packages match canonical bytes | atomic migration and honest measurement pass or block | R45 |
| BND-ENV-001 | external-environment | R7, R15, R29, R39, R42, R52, R53 | writable explicit path, filesystem interruption, canonical and derived package, unavailable runtime or resource | acceptance is repository-owned and non-runtime | deterministic proof passes or the claim blocks | R53 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R10, R11, R12, R17, R18 | BND-INPUT-001, BND-AUTH-001 | malformed ownership or stale assessment falls through to portable or governed mutation | every signal and assessment basis is validated and invalid state stops |
| INT-002 | R25, R26, R28, R29, R40, R41, R42 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | interruption leaves files without a durable identity basis | the manifest is durable before writes and retry reconciles only recorded state |
| INT-003 | R24, R31, R32, R33, R34, R35, R38 | BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | partial commit exposes broken diagram or ADR references | dependencies and groups prevent unsafe commit; only independently valid targets persist |
| INT-004 | R45, R46, R47, R49, R50, R51, R52 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | prose relocation hides behavior loss or package drift | ledgers, real-profile reduction, and raw-byte parity all remain required |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R8, R13 | BND-INPUT-001 | - | - |
| E2 | illustration | R20 | BND-AUTH-001 | - | - |
| E3 | regression | R10, R11, R12 | BND-INPUT-001, BND-AUTH-001 | ARSIM-PR4 | - |
| E4 | regression | R17, R18, R19 | BND-STATE-001, BND-AUTH-001 | ARSIM-PR4 | - |
| E5 | regression | R26 | BND-STATE-001, BND-RECOVERY-001 | ARSIM-PR5 | - |
| E6 | illustration | R29, R40, R42 | BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |
| E7 | regression | R31, R33, R34 | BND-COMPOSE-001, BND-RECOVERY-001 | ARSIM-PR6 | - |
| E8 | regression | R37, R38 | BND-STATE-001, BND-RECOVERY-001 | ARSIM-PR6 | - |
| E9 | illustration | R35 | BND-COMPOSE-001 | - | - |
| E10 | illustration | R7 | BND-COMPOSE-001, BND-ENV-001 | - | - |

## Compatibility and migration

Historical architecture artifacts and ADRs remain unchanged. The canonical skill, references, assets, validators, fixtures, and generated package inventories migrate atomically. Parser-sensitive literals change only with every consumer, while incidental prose assertions are updated rather than preserved as policy. Rollback restores the previous main skill and assets, removes both references, restores coupled expectations, and regenerates derived packages without rewriting historical architecture.

## Observability

The change is observable through resource maps, rule and literal ledgers, static scenario results, profile and total-package measurements, validator output, raw-byte package parity, authoring evidence, review records, and lifecycle metadata. Reports distinguish configured commands from executed commands and relocated content from removed content.

## Security and privacy

The change introduces no credentials, secrets, network operation, external persistence, or personal-data processing. Existing destructive-action, publication, and external-state boundaries remain mandatory, and unrecorded or conflicting files cannot be adopted.

## Accessibility and UX

Not applicable to end-user interface accessibility. Published Markdown must remain readable, keep complete prose sentences intact, use stable IDs and tables for repeated mappings, and emit no placeholders.

## Performance expectations

All three real loaded procedural assemblies must use fewer LF-normalized UTF-8 bytes and Unicode whitespace-separated words than baseline. Total package size is reported separately, and no runtime latency contract is introduced.

## Edge cases

EC1. A direct assessment concludes not-required: return the rationale without loading method or governed procedure.

EC2. A spec changes after a required assessment: stop authoring until assessment is refreshed.

EC3. A prepared record exists but no target file changed: resume after exact revalidation.

EC4. A diagram exists but is absent from the manifest: do not adopt it.

EC5. A replacement ADR is valid but predecessor update fails: preserve it only when independently valid and report `partial-blocked`.

EC6. Canonical Markdown would link to an incomplete dependency: do not write the canonical commit point.

## Non-goals

- Redesigning C4, arc42, ADR semantics, canonical paths, lifecycle stages, or architecture-review authority.
- Adding a runtime router, generic architecture engine, new asset, tokenizer, prose classifier, permanent simplicity gate, or target-agent journey.
- Optimizing `architecture-review` in this change.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every normative requirement maps to deterministic proof in the test specification. |
| AC2 | All three procedural assemblies decrease in words and bytes while total package size remains visible. |
| AC3 | Assessment and governed-signal classifications fail closed for unknown, stale, malformed, and conflicting values. |
| AC4 | Workflow-managed authoring binds current required assessment, spec, and spec-review identities. |
| AC5 | Prepared evidence containing the complete manifest exists before every target mutation scenario. |
| AC6 | Dependency, commit-group, canonical commit-point, ADR supersession, partial-result, and retry scenarios have direct proof. |
| AC7 | Every current rule, literal, and asset instruction receives one disposition and owner. |
| AC8 | Required-resource failures stop without fallback reconstruction. |
| AC9 | Canonical-through-installed resource inventories and bytes match. |
| AC10 | Acceptance executes no target-agent runtime and introduces no separate manual semantic-review gate. |

## Open questions

None. Exact evidence field names and fixture encoding may vary while preserving R16 through R42 and must be settled by the plan and test specification.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment.
- Execution plan and test specification after required reviews settle.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This artifact does not claim review approval, architecture completion, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
