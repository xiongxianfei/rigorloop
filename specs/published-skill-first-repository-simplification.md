<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->

# Published-Skill-First Repository Simplification

## Owning change record

`docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-10-published-skill-first-repository-simplification.md`

## Goal and context

RigorLoop will validate the deterministic artifacts it publishes without maintaining target-agent behavior certification as a repository acceptance system.
Canonical skills, packaged resources, generated adapter packages, and release artifacts are the product proof chain.
Semantic skill quality remains a review responsibility, and lifecycle consistency remains a separate bounded governance concern.

This spec establishes the replacement contract and the proof-preserving migration rules.
It does not itself delete scripts or redefine the advertised workflow automation capability.

## Glossary

- **Gate A**: deterministic integrity proof for canonical skills and their packaged resources.
- **Gate B**: deterministic generation, inventory, transformation, archive, and byte-parity proof for Codex, Claude Code, and opencode adapter packages.
- **Gate C**: release-candidate integrity proof that composes Gates A and B with release metadata checks.
- **semantic review**: human or agent judgment about whether skill instructions are clear, correctly scoped, followable, and safe.
- **governance validator**: the single bounded owner for deterministic change-record and lifecycle consistency.
- **materialization smoke**: invocation of RigorLoop-owned installer or materializer logic in an empty temporary directory, followed only by filesystem inspection.
- **retirement ledger**: the mapping from an existing check to its protected failure, replacement owner, disposition, and rollback evidence.

## Examples first

### Example E1: a missing mapped resource fails canonical integrity

Given a canonical skill maps a required packaged resource
When that resource is absent or its path escapes the skill root
Then Gate A fails with the skill, resource path, violated invariant, and repair action.

### Example E2: stale generated adapter bytes fail package parity

Given canonical skill bytes change
When any Codex, Claude Code, or opencode package contains stale untransformed bytes
Then Gate B fails for that target without starting its runtime.

### Example E3: prose quality stays review-owned

Given a skill description is structurally valid but its trigger boundary is unclear
When repository acceptance runs
Then deterministic gates do not score the prose, and semantic review records any material clarity finding.

### Example E4: an LLM transcript is not acceptance evidence

Given a prompt appears to select the expected skill in one target-agent session
When repository correctness is evaluated
Then that transcript is neither required nor sufficient proof of canonical, package, or release integrity.

### Example E5: a pure-copy installer adds no gate

Given installer inspection proves that installation only copies package content already covered by Gate B
When the replacement gate set is defined
Then no installer smoke is required.

### Example E6: meaningful materialization gets narrow filesystem proof

Given RigorLoop-owned installer logic transforms paths or materializes files beyond a pure copy
When installer proof runs
Then it invokes only that logic in an empty temporary directory and inspects the resulting filesystem without starting Codex, Claude Code, or opencode or sending a prompt.

### Example E7: an undocumented protected failure stops retirement

Given an existing check fails on a fixture whose protected contract is unknown
When a retirement slice evaluates the check
Then retirement pauses until the failure is assigned to Gate A, Gate B, Gate C, governance, semantic review, or explicit de-contracting.

### Example E8: release proof reuses product gates

Given a local release candidate
When Gate C runs
Then it consumes current passing Gate A and Gate B proof and adds version, metadata, archive, checksum, release-note, and rollback-consistency checks rather than recreating skill or package semantics.

## Requirements

R1. Repository acceptance MUST treat canonical `skills/`, packaged skill resources, generated public adapter packages, and release artifacts as the primary published product boundary.

R2. Gate A MUST validate deterministic canonical-skill properties: parseable frontmatter, required contractual structure, valid Resource map entries, mapped-resource existence, normalized relative paths, path-traversal exclusion, packaged-resource completeness, unfilled placeholders, contractual closed vocabularies, and narrowly defined forbidden claims.

R3. Gate A MUST NOT judge prose quality, infer agent behavior, score semantic similarity, or predict skill routing.

R4. Gate B MUST generate and validate Codex, Claude Code, and opencode adapter packages from canonical `skills/` with equivalent proof of expected skill and file inventory, mapped-resource paths, untransformed byte parity, declared transformations, and archive contents.

R5. Every target-specific content transformation admitted by Gate B MUST declare its owner, canonical input, generated output, deterministic transformation rule, and proof oracle; undeclared transformation or drift MUST fail Gate B.

R6. Repository acceptance MUST NOT start Codex, Claude Code, or opencode, send prompts, grade target output, inspect model-routing transcripts, select model IDs, maintain target-runtime matrices, retry nondeterministic model runs, or certify model behavior.

R7. Gate C MUST require current Gate A and Gate B proof and MUST add deterministic version, package metadata, archive inventory, checksum, release metadata, tracked release-note, generated-package parity, and rollback or release-consistency validation.

R8. Gate C MUST reuse Gate A and Gate B results or their shared deterministic owners rather than implement a third independent interpretation of canonical skill and adapter correctness.

R9. The installer or materializer MUST receive a separate filesystem smoke only when an inventory demonstrates RigorLoop-owned transformation or materialization behavior that Gate B cannot prove.

R10. A materialization smoke MUST use an empty temporary directory, invoke only RigorLoop-owned installer or materializer logic, inspect deterministic filesystem results, avoid network dependence where a local package is available, and MUST NOT start a target-agent runtime or send a prompt.

R11. Semantic review of a changed published skill MUST assess description and trigger clarity, ownership, prerequisites, procedure, resources, stop conditions, claim boundaries, output, and handoff; deterministic gates MUST NOT substitute structural presence for that judgment.

R12. Repository lifecycle governance MUST have one bounded deterministic validation owner for change-record shape, legal lifecycle transitions, review and resolution references, dangling evidence, contradictory recorded state, and contractual closed vocabularies.

R13. The governance validator MUST fail closed on unknown closed-vocabulary values before applying consistency logic and MUST report the field, unknown value, allowed values, and repair surface.

R14. A new or retained script or check MUST have a retirement-ledger entry naming the concrete product, package, governance, or release failure it prevents; why deterministic automation is appropriate; why an existing gate cannot own it more simply; when it runs; what repair it reports; and what evidence permits later retirement.

R15. The default admission budget for this initiative MUST be zero new standalone validator CLIs, zero new selector or check-routing systems, and zero new validation caches or schedulers.

R16. Logic MAY be added to an existing gate owner only when it protects a requirement-owned deterministic invariant and does not introduce a competing parser or semantic oracle.

R17. Before an existing check is retired, the retirement slice MUST inventory its accepted and rejected fixtures and map each protected failure to Gate A, Gate B, Gate C, governance, semantic review, or an explicit approved decision that the failure is no longer contractual.

R18. Unknown, undocumented, or contradictory fixture behavior MUST pause retirement of the affected check until its contract owner and disposition are recorded.

R19. Each retirement slice MUST run the old and replacement proof paths over representative affected fixtures before removal and MUST record coverage differences, final disposition, and a recoverable rollback boundary.

R20. A check MAY be removed only when all of its contractual failures are caught by retained proof or explicitly de-contracted by an approved spec amendment.

R21. Continuous-integration workflows MUST remain thin and invoke stable product gates or one minimal transparent composition wrapper; selector, cache, scheduler, and meta-validation layers MUST NOT remain on the publication path without measured scale evidence and an approved exception.

R22. Command-count, runtime, changed-line, and maintenance-owner measurements MUST be recorded as simplification outcomes but MUST NOT substitute for the protected-failure mapping required by R17 through R20.

R23. The existing workflow stage order, formal review evidence, review independence, and target-bound automation product behavior MUST remain unchanged unless a separate approved proposal and spec change them.

R24. Historical prompt fixtures, transcripts, behavior-parity corpora, and clean-install evidence MAY remain as historical evidence, but new repository acceptance under this contract MUST NOT require target-runtime or LLM-output evidence.

R25. Existing selector, validation-cache, scheduler, broad-smoke, and validator-meta-test contracts MUST remain in force until the retirement slice that owns them records an exact amendment or supersession; this spec alone MUST NOT silently delete their still-active invariants.

R26. The following prospective skill-contract obligations are superseded for changes governed by this spec: `skill-contract.md` R35, R35a, R35b, R35e, R35f, R35g, R36i, R36j, R43d, R44a, R44e, R45, R45a through R45d, R52, R52a, R52b, the installed-target-tree portion of R55a, and R59b.

R27. R26 MUST NOT weaken deterministic structural, resource, transformation, archive, or byte-parity clauses in `skill-contract.md`; those obligations move to Gate A or Gate B.

R28. Release and adapter contracts that require Codex, Claude Code, and opencode support MUST remain compatible through equivalent Gate B package proof even though target runtimes are not executed.

R29. `skill-contract.md` R35c and R35d remain active: no repository evidence may claim deterministic runtime skill selection, and broad semantic scoring remains prohibited.

## Boundary model

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R2, R4, R7, R14, R17 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R17, R18, R19, R20, R25 | BND-STATE-001 | - |
| identity-authority | applicable | R1, R3, R5, R11, R12, R13, R14, R15, R16 | BND-AUTH-001 | - |
| composition-path | applicable | R4, R7, R8, R12, R21 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R18, R19, R20, R24, R25 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R5, R13, R18, R19, R20 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R23, R24, R25, R26, R27, R28 | BND-COMPAT-001 | - |
| external-environment | applicable | R6, R9, R10, R28, R29 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R2, R4, R7, R14, R17 | valid, invalid, missing, unknown, undeclared | Every accepted input belongs to a named deterministic gate or review owner. | Valid input proceeds; invalid input fails its owner; unknown ownership stops retirement. | R17 |
| BND-STATE-001 | state-lifecycle | R17, R18, R19, R20, R25 | inventoried -> dual-proof -> removable -> retired; any state -> paused | Removal follows recorded proof and approved contract disposition. | Complete slices retire; incomplete or contradictory slices pause. | R20 |
| BND-AUTH-001 | identity-authority | R1, R3, R5, R11, R12, R13, R14, R15, R16 | product gate, governance, semantic review, explicit de-contracting | No owner silently claims another owner's judgment. | Correct owner decides; missing or competing owner blocks. | R14 |
| BND-COMPOSE-001 | composition-path | R4, R7, R8, R12, R21 | canonical -> Gate A -> Gate B -> Gate C; lifecycle -> governance; prose -> review | Publication proof composes forward while governance and semantics remain separate. | Direct composition passes or fails without selector-owned semantics. | R8 |
| BND-TEMPORAL-001 | temporal-retry | R18, R19, R20, R24, R25 | old-only, dual-run, replacement-only, rollback | A retirement slice never removes the old proof before replacement coverage is classified. | Dual proof enables removal; mismatch pauses; rollback restores the last slice. | R19 |
| BND-RECOVERY-001 | failure-recovery | R5, R13, R18, R19, R20 | actionable failure, unknown failure, partial migration, rollback | Failures name repair and owner; unknowns do not pass silently. | Actionable failure routes repair; unknown or partial state pauses; rollback is recoverable. | R18 |
| BND-COMPAT-001 | compatibility-migration | R23, R24, R25, R26, R27, R28 | historical evidence, active old contract, superseded clause, retained target support | Exact clause disposition precedes deletion and all adapter targets retain deterministic package support. | Historical evidence remains; active clauses govern until amended; superseded clauses stop imposing runtime proof. | R25 |
| BND-ENV-001 | external-environment | R6, R9, R10, R28, R29 | repository files, local release candidate, empty temporary directory, target runtime, network | Acceptance is deterministic and repository-owned; target runtimes are excluded. | Local filesystem proof may pass or fail; runtime or prompt execution is rejected as acceptance proof. | R6 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R4, R5, R17, R18, R19, R20 | BND-INPUT-001, BND-AUTH-001, BND-TEMPORAL-001 | A target-specific transform is mistaken for parity and its old check is removed. | Gate B rejects undeclared transformation before the old proof can retire. |
| INT-002 | R7, R8, R21 | BND-COMPOSE-001, BND-RECOVERY-001 | Gate C reimplements stale Gate A or B semantics behind a wrapper. | Release proof consumes current owners and identifies the failed underlying gate. |
| INT-003 | R11, R12, R13, R14, R15, R16 | BND-AUTH-001, BND-COMPOSE-001 | A structural validator becomes a semantic skill reviewer. | The validator stops at deterministic facts and routes semantic judgment to review. |
| INT-004 | R17, R18, R19, R20, R25 | BND-STATE-001, BND-TEMPORAL-001, BND-COMPAT-001 | Implementation deletes a check while its governing spec remains active. | Retirement pauses until exact contract disposition and dual-proof evidence exist. |
| INT-005 | R6, R9, R10 | BND-ENV-001, BND-AUTH-001 | Installer smoke expands into target-runtime behavior certification. | Proof ends after RigorLoop-owned filesystem inspection; target execution is rejected. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R2 | BND-INPUT-001 | - | - |
| E2 | illustration | R4 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E3 | illustration | R3, R11 | BND-AUTH-001 | - | - |
| E4 | illustration | R6 | BND-ENV-001 | - | - |
| E5 | illustration | R9 | BND-ENV-001 | - | - |
| E6 | illustration | R10 | BND-ENV-001 | - | - |
| E7 | illustration | R18 | BND-STATE-001, BND-RECOVERY-001 | - | - |
| E8 | illustration | R7, R8 | BND-COMPOSE-001 | - | - |

## Inputs and outputs

Inputs are canonical skills and resources, adapter target declarations, generated package trees and archives, release-candidate metadata, installer behavior inventory, change-local lifecycle records, existing check fixtures, and governing validation contracts.

Outputs are three stable product-gate results, one governance result, semantic review evidence, a script retirement ledger, per-slice compatibility dispositions, and simplification measurements.

Every deterministic failure output identifies the owning gate, affected artifact, violated invariant, and actionable repair.

## State and invariants

- `skills/` remains the only authored skill source.
- Codex, Claude Code, and opencode remain supported generated adapter targets.
- Gate A owns canonical integrity; Gate B owns generated package parity; Gate C owns release integrity.
- Semantic review and lifecycle governance are not publication gates and do not inherit each other's authority.
- Unknown closed-vocabulary values fail closed.
- An old check remains until protected failures and contract dispositions are classified.
- Historical evidence remains immutable even when its prospective requirement is superseded.
- No target-agent execution is necessary to prove repository correctness.

## Error and boundary behavior

- A malformed canonical skill, unsafe resource path, missing resource, or forbidden placeholder fails Gate A.
- Missing target inventory, stale bytes, undeclared transformation, or malformed archive fails Gate B for the affected target and blocks Gate C.
- Missing release metadata, checksum mismatch, stale package proof, or absent tracked release notes fails Gate C.
- An unknown lifecycle value, illegal transition, dangling review reference, or contradictory recorded state fails governance validation.
- A semantic concern that cannot be decided deterministically becomes a review finding, not a validator heuristic.
- An unknown protected failure, conflicting active contract, incomplete dual run, or unrecoverable retirement slice pauses removal.
- A request to use target-agent execution or LLM-output grading as acceptance proof is outside this contract.

## Compatibility and migration

Migration proceeds in reviewable slices:

1. Freeze admission of new standalone validation subsystems under R14 through R16.
2. Inventory checks, fixtures, governing clauses, invocation sites, and protected failures.
3. Define Gate A, Gate B, Gate C, and the single governance owner by consolidating existing deterministic behavior where possible.
4. Run old and replacement proof together and record differences.
5. Amend or supersede each affected active contract before removing its implementation.
6. Remove one bounded subsystem slice and preserve a recoverable rollback point.

R26 is the exact prospective disposition for existing skill-contract behavior and clean-install proof clauses.
All other selector, cache, scheduler, broad-smoke, lifecycle, release-transaction, workflow-automation, token-cost, and meta-validation clauses remain active until their owning retirement slice records exact disposition.

Rollback restores the most recently retired slice and its direct invocation without changing canonical skill bytes, public package formats, release history, or historical evidence.

## Observability

Each product gate reports a stable gate name, affected target or artifact, deterministic invariant, pass or fail result, and repair guidance.
Each retirement slice records old and replacement commands, fixture coverage, differences, removed invocation sites, rollback point, command count, runtime, changed lines, and maintenance owner.
No runtime transcript, model ID, prompt result, retry log, or LLM score is required.

## Security and privacy

Gate inputs and evidence MUST use repository-local or local release-candidate artifacts and MUST NOT require credentials, private prompts, user transcripts, model logs, or external publication.
Materialization smoke uses a temporary directory and local package input when available.
Path validation rejects traversal outside owned roots.

## Accessibility and UX

No end-user interface is introduced.
Contributor-facing commands and diagnostics use stable gate names and actionable plain-language repair guidance.

## Performance expectations

Routine canonical-skill contribution SHOULD require direct Gate A and affected Gate B proof rather than release-only or unrelated orchestration checks.
The migration records baseline and replacement wall time and command count for each slice.
No numeric speed target may justify loss of protected-failure coverage.

## Edge cases

EC1. A check protects both deterministic and semantic concerns: retain or move only the deterministic portion and route the semantic portion to review.

EC2. A target-specific adapter transform changes bytes intentionally: Gate B accepts it only with the complete R5 contract.

EC3. Installer logic differs by target: materialization proof covers only the RigorLoop-owned branches not already proved by package parity and still stops before target runtime execution.

EC4. An old fixture encodes behavior not named in any spec: retirement pauses for ownership and de-contracting review.

EC5. An existing cache or selector improves runtime measurably: it remains eligible only through an approved exception that names its scale evidence and deterministic owner.

EC6. A release candidate passes package parity but carries wrong version or release notes: Gate C fails independently.

EC7. A historical transcript or behavior corpus is useful to a reviewer: it may be consulted as non-acceptance context but does not become a required gate.

EC8. A retirement slice discovers that a supposedly duplicate lifecycle parser has distinct closed-vocabulary behavior: consolidation pauses until the single owner preserves it with unknown-value regression proof.

## Non-goals

- Deleting all scripts or setting a line-count quota.
- Weakening deterministic negative-path, adapter, archive, release, or lifecycle proof.
- Certifying target-agent interpretation of skill instructions.
- Redesigning the workflow automation product.
- Publishing, releasing, tagging, deploying, or mutating external systems.
- Retiring every validation subsystem in one implementation milestone.

## Acceptance criteria

| ID | Acceptance criterion | Requirement IDs |
| --- | --- | --- |
| AC1 | Gate A accepts valid canonical skills and rejects each named deterministic integrity failure with repair guidance. | R1-R3 |
| AC2 | Gate B proves equivalent deterministic package parity for Codex, Claude Code, and opencode and rejects stale or undeclared transformations. | R4, R5, R28 |
| AC3 | Gate C composes current Gate A and Gate B proof with release-specific integrity checks. | R7, R8 |
| AC4 | Repository acceptance contains no target-runtime start, prompt execution, transcript grading, model matrix, nondeterministic retry requirement, or deterministic runtime-selection claim. | R6, R24, R26, R29 |
| AC5 | Installer inventory either proves Gate B is sufficient or identifies a narrow deterministic materialization smoke satisfying R10. | R9, R10 |
| AC6 | Semantic review criteria and the single bounded governance owner have distinct documented authority. | R11-R13 |
| AC7 | Every retained or added script has the complete R14 admission record and no prohibited new subsystem is introduced. | R14-R16 |
| AC8 | Every retired check has fixture inventory, protected-failure mapping, dual-proof comparison, exact contract disposition, and rollback evidence. | R17-R20, R25 |
| AC9 | CI invokes stable gates directly or through one transparent composition owner, with any exception backed by approved measured evidence. | R21 |
| AC10 | Simplification metrics are recorded without replacing failure-coverage proof. | R22 |
| AC11 | Workflow behavior remains unchanged and historical evidence remains available without imposing prospective runtime acceptance. | R23, R24 |
| AC12 | The exact skill-contract clauses named in R26 no longer require prompt, transcript, semantic behavior-parity, or all-target clean-install evidence, while deterministic parity remains enforced. | R26, R27 |

## Open questions

- Which existing lifecycle validator becomes the single governance entry point after consolidation analysis?
- Which current installer branches perform meaningful transformation beyond package copying?
- Which token-cost checks remain release-critical rather than optional maintainer analysis?
- What measured repository scale would justify a temporary selector, cache, or scheduler exception?

These are architecture and planning decisions within the accepted direction; none permits target-runtime acceptance.

## Next artifacts

- Formal spec review.
- Recorded architecture assessment.
- Architecture and ADR updates if the assessment is `architecture-required`.
- Execution plan and plan review.
- Test specification and test-spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.
