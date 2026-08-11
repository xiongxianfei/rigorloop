# Verify Skill Simplification

## Owning change record

`docs/changes/2026-08-11-verify-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-11-verify-skill-simplification.md`

## Goal and context

Simplify the published `verify` skill so a scoped verification loads only the universal contract, while branch-readiness and workflow-final verification load one coherent conditional procedure.

The change preserves verification rigor, `branch-ready` ownership, lifecycle and review-closeout checks, evidence truthfulness, package integrity, and downstream authority.
It changes package composition and instruction ownership, not workflow stage order, runtime architecture, or readiness semantics.

## Glossary

- `requested outcome`: exactly one of `scoped-verification`, `branch-readiness`, or `workflow-final-verification`.
- `resolved target`: one repository plus one branch or commit, and, for final readiness, exactly one governed change or explicit evidence root whose evidence belongs to that identity.
- `execution mode`: exactly `isolated` or `governed-final`; it controls permitted writes and handoff, independently of loaded resources.
- `resource profile`: one of `VP0-scoped`, `VP0B-scoped-boundary`, `VP1-final-readiness`, or `VP1B-final-readiness-boundary`.
- `release_sensitive`: a boolean applicability flag that adds final evidence obligations without authorizing release, publication, or deployment claims.
- `item-level evidence semantics`: universal rules for deciding whether one command, CI result, generated output, manual proof, release artifact, or other evidence item is current and truthful.
- `final-readiness aggregation`: the conditional procedure that determines the complete applicable evidence set and combines it into `branch-ready` or `not-ready`.

## Examples first

### Example E1: scoped command verification stays on the common path

Given a user asks whether one named local validation command passed
When the command and its actual current output are assessed
Then the invocation is `scoped-verification`, loads `VP0-scoped`, and reports only a scoped `pass`, `fail`, or `inconclusive` verdict.

### Example E2: scoped evidence types do not require final closeout

Given a user asks whether one CI result, generated artifact, manual-proof record, or release-metadata file is valid
When no branch-readiness outcome is requested
Then the skill applies inline item-level evidence semantics without loading `branch-readiness-verification.md`.

### Example E3: direct branch readiness is isolated

Given a direct request resolves one repository, one branch or commit, and one governed change or explicit evidence root
When branch readiness is requested
Then the skill loads the branch-readiness reference, computes `branch-ready` or `not-ready`, and does not advance workflow state, prepare PR content, or invoke `pr`.

### Example E4: workflow-final verification requires governed authority

Given current governed evidence identifies final `verify` as the applicable stage for one change
When the workflow invokes final verification
Then the skill loads the branch-readiness reference in `governed-final` mode, performs only verify-owned recording, and hands control back to workflow for any progression toward `pr`.

### Example E5: informal readiness wording cannot create governed-final mode

Given a direct request says only "verify this is ready"
When no exact target and current governed final-verify authority can be resolved
Then the skill stops or performs only an explicitly resolved scoped verification; it does not infer `workflow-final-verification`.

### Example E6: release sensitivity adds evidence, not authority

Given a resolved final-readiness target has `release_sensitive: true`
When final evidence is assembled
Then applicable release evidence participates in the verdict, but the skill makes no publication, deployment, or release-completion claim.

### Example E7: required resource failure stops safely

Given a requested outcome requires `branch-readiness-verification.md`
When that mapped reference is missing or unreadable
Then verification stops before a dependent verdict, recording action, or handoff and does not reconstruct the procedure from memory.

### Example E8: boundary-first loading remains independently additive

Given an invocation has missing, stale, unknown, ambiguous, conflicting, or insufficient approved boundary or proof trace
When the boundary-first trigger applies
Then the existing boundary reference is added to the applicable `VP0` or `VP1` profile without changing execution authority.

## Requirements

R1. The published `verify` package MUST remain owned by `skills/verify/`, use normalized frontmatter and required core sections, and contain canonical `SKILL.md`, `references/boundary-first-method-v1.md`, and `references/branch-readiness-verification.md` as its complete authored package.

R2. `SKILL.md` MUST be self-sufficient for every valid scoped verification, including classification, target scoping, item-level evidence interpretation, safe execution, bounded claims, stop behavior, and result reporting.

R3. `SKILL.md` MUST retain universal ownership of purpose and routing, source precedence, requested-outcome and execution-mode classification, target resolution, evidence truthfulness, compact verification dimensions, validation integrity, isolation, claim boundaries, universal blockers, resource triggers, result shape, and handoff limits.

R4. The requested-outcome vocabulary MUST be exactly `scoped-verification`, `branch-readiness`, and `workflow-final-verification`; unknown, missing, contradictory, or ambiguous outcomes MUST fail closed before conditional procedure loads.

R5. `scoped-verification` MUST resolve one explicit command, artifact, requirement, evidence item, or validation surface and MUST permit only scoped `pass`, `fail`, or `inconclusive` claims.

R6. `branch-readiness` MUST resolve one repository, one branch or commit, and exactly one governed change or explicit evidence root; evidence from another identity MUST NOT contribute to the verdict.

R7. `workflow-final-verification` MUST require current governed evidence for the same change identity showing that final `verify` is the applicable stage; conversational wording alone MUST NOT establish this outcome.

R8. Missing, stale, contradictory, cross-target, or multiply resolved identity evidence MUST stop final-readiness verification and identify the unresolved target before loading or partially applying final-readiness procedure.

R9. `release_sensitive` MUST be a boolean final-evidence applicability flag, MUST NOT create another requested outcome, and MUST NOT authorize publication, deployment, release completion, or external action.

R10. Execution mode MUST be exactly `isolated` or `governed-final` and MUST be classified independently of the loaded-resource profile.

R11. `isolated` mode MUST NOT advance lifecycle state, mutate workflow routing, invoke `pr`, prepare PR content, or perform governed-final recording merely because a clean branch-readiness verdict was produced.

R12. `governed-final` mode MUST perform only recording already owned by `verify`; `workflow` MUST retain lifecycle transition and continuation ownership, and `pr` MUST retain PR preparation and opening ownership.

R13. Resource assembly MUST use exactly four profiles: `VP0-scoped` (`SKILL.md`), `VP0B-scoped-boundary` (`SKILL.md` plus boundary reference), `VP1-final-readiness` (`SKILL.md` plus branch-readiness reference), and `VP1B-final-readiness-boundary` (`SKILL.md` plus both references).

R14. `branch-readiness-verification.md` MUST load exactly for `branch-readiness` and `workflow-final-verification`, MUST remain owned by the `verify` package, and MUST NOT become an independent lifecycle or claim owner.

R15. The existing boundary-first reference and trigger MUST remain unchanged in behavior and independently additive to either scoped or final-readiness assembly.

R16. A missing or unreadable triggered reference MUST stop before dependent interpretation, verdict, recording, or handoff; an untriggered reference MUST not load or block scoped verification; memory-based reconstruction MUST be forbidden.

R17. Inline item-level evidence semantics MUST distinguish configured from actually run commands, current from stale evidence, local validation from observed hosted CI, and `passed`, `failed`, `skipped`, `pending`, `not-run`, and `unknown`; generated-output and manual-proof claims MUST remain source- and evidence-bound.

R18. The branch-readiness reference MUST own final prerequisite selection, related-artifact assembly, traceability, lifecycle and review closeout, applicable targeted/broad/CI/generated/manual/release evidence composition, blocker aggregation, final verdict calculation, and mode-specific completion procedure only.

R19. The branch-readiness reference MUST NOT redefine evidence-item meaning, status vocabulary, universal stops, claim authority, workflow stage order, recording ownership, or PR authorization.

R20. Scoped verification MUST be able to assess any supported individual evidence class, including CI, generated output, manual proof, command output, and release metadata, without loading final-readiness aggregation.

R21. The simplification MUST preserve verification dimensions covering contract and requirement satisfaction, proof validity, architecture and lifecycle coherence, review closure, validation evidence, drift, risk, generated outputs, release safety, and handoff readiness when applicable.

R22. `verify` MUST retain sole ownership of `branch-ready` and MUST NOT claim PR-ready, PR-body readiness, PR-open readiness, review approval without cited review evidence, hosted CI success without observed evidence, or generated-output currency without proof.

R23. A change-local semantic rule-disposition ledger MUST inventory every behaviorally significant current rule with stable ID, source locations, behavior, governing requirements, applicable profiles, one closed disposition, destination, and preservation proof.

R24. Semantic dispositions MUST be exactly `retained-inline`, `retained-branch-readiness-reference`, `retained-boundary-reference`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; missing or unknown values MUST fail closed before consistency checks.

R25. A separate change-local literal-compatibility inventory MUST record exact literal, source, consumers, required semantics, disposition, and replacement, and classify each dependency exactly as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`; missing or unknown classifications MUST fail closed.

R26. Normative literals MUST remain exact unless their governing contract changes; parser/package literals MUST migrate with every consumer; incidental test wording MUST be updated rather than promoted to policy; obsolete literals MUST have removal evidence.

R27. Profile measurement MUST use canonical LF-normalized resources, count each unique resource once in documented load order, and report UTF-8 bytes and Unicode whitespace-separated words for `SKILL.md`, each resource, all four profiles, and the total package.

R28. The 30-40 percent `VP0` reduction MUST remain advisory; acceptance MUST require complete rule disposition, one owner per duplicate cluster, material scoped-profile reduction, no unjustified final-readiness growth, separate total-package accounting, and semantic preservation.

R29. Acceptance MUST use deterministic structural checks, static contract fixtures, existing package-chain proof, and independent semantic review; it MUST NOT execute Codex, Claude Code, opencode, or another target-agent runtime or add prompt journeys, transcript grading, runtime certification, a permanent simplicity validator, or a new tokenizer dependency.

R30. Existing validation owners MUST prove normalized skill structure, closed vocabulary, both resource mappings, resource existence and containment, canonical/generated/packed/installed parity, and boundary-reference identity across supported adapters.

R31. The refactor MUST preserve existing direct and governed verification behavior, review and lifecycle closeout semantics, validation and release safety, claims, stops, outputs, and handoffs except for the approved resource-loading and ownership changes.

R32. A recorded architecture assessment MUST precede planning; it MUST select `architecture-not-required` when the existing packaged-skill model remains accurate and MUST route through architecture authoring and review if implementation would change that model or require a current architecture correction.

R33. Rollout and rollback MUST operate on one complete package revision with every mapped resource and coupled literal consumer, and mixed or partial package versions MUST fail package validation and runtime-dependent procedure.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R4, R5, R6, R7, R8, R9 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R7, R8, R9, R10, R11, R12, R16, R32, R33 | BND-STATE-001 | - |
| identity-authority | applicable | R6, R7, R8, R9, R10, R11, R12, R14, R18, R19, R22 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R13, R14, R15, R16, R17, R18, R19, R20, R30, R31 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R7, R8, R16, R17, R33 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R4, R8, R16, R24, R25, R26, R28, R29, R32, R33 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R23, R24, R25, R26, R30, R31, R32, R33 | BND-COMPAT-001 | - |
| external-environment | applicable | R16, R27, R29, R30, R33 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R4, R5, R6, R7, R8, R9 | three valid outcomes; exact, missing, unknown, ambiguous, contradictory, cross-target identities; release flag true or false | one outcome and one permitted target identity govern a verdict | valid scoped/final classification or fail-closed stop | R4 |
| BND-STATE-001 | state-lifecycle | R7, R8, R9, R10, R11, R12, R16, R32, R33 | isolated/governed-final; current/stale authority; complete/missing resource; assessed/unassessed architecture; complete/partial rollout | resource availability never grants execution authority; only owners write their state | permitted mode-specific completion or stop before dependent work | R10 |
| BND-AUTH-001 | identity-authority | R6, R7, R8, R9, R10, R11, R12, R14, R18, R19, R22 | direct caller, governed workflow, verify, workflow, and pr authority; same/mismatched identity | verify owns branch-ready only; workflow and pr retain their existing ownership | bounded verdict and handoff, or authority stop | R12 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R13, R14, R15, R16, R17, R18, R19, R20, R30, R31 | VP0, VP0B, VP1, VP1B; inline item semantics; conditional final aggregation; canonical through installed packages | every rule and resource has one owner; scoped paths remain self-sufficient | exact load assembly and behavior-preserving result | R13 |
| BND-TEMPORAL-001 | temporal-retry | R7, R8, R16, R17, R33 | current/stale evidence; retry after missing resource; pre/post package revision | stale evidence never supports a current claim; retry reclassifies from current evidence | current verdict or explicit stale/package blocker | R17 |
| BND-RECOVERY-001 | failure-recovery | R4, R8, R16, R24, R25, R26, R28, R29, R32, R33 | unknown vocabulary, unresolved target, unreadable reference, unsafe reduction, ambiguous architecture, partial rollout | failures stop at the owning boundary without invented procedure | correction at owner, atomic rollback, or explicit blocker | R16 |
| BND-COMPAT-001 | compatibility-migration | R23, R24, R25, R26, R30, R31, R32, R33 | normative/parser/incidental/obsolete literal; prior/current package; rollout/rollback | behaviorally significant rules never disappear; consumers migrate atomically | compatible current package or complete prior-package rollback | R26 |
| BND-ENV-001 | external-environment | R16, R27, R29, R30, R33 | canonical/generated/packed/installed filesystems; supported adapters; runtime present/absent | acceptance is deterministic and filesystem/package based, never model-runtime based | parity proof, package-integrity failure, or safe omission of runtime proof | R29 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R4-R8, R13-R14 | BND-INPUT-001, BND-COMPOSE-001 | ambiguous outcome or target could load final procedure | stop before `VP1` assembly and name the unresolved identity |
| INT-002 | R10-R12, R18-R19 | BND-AUTH-001, BND-COMPOSE-001 | shared final-readiness procedure could leak governed writes into direct use | loaded resources stay shared while mode-specific writes remain isolated |
| INT-003 | R16-R20 | BND-COMPOSE-001, BND-RECOVERY-001 | moving item semantics behind the reference could under-specify scoped checks | universal semantics stay inline and missing final procedure stops only dependent outcomes |
| INT-004 | R7-R8, R16-R17 | BND-STATE-001, BND-TEMPORAL-001 | stale authority or evidence could be replayed as current | reclassify from current evidence or stop; never reuse stale authority |
| INT-005 | R23-R28, R31 | BND-RECOVERY-001, BND-COMPAT-001 | size pressure or incidental tests could remove semantic rules | closed ledgers, semantic review, and advisory metrics preserve the contract |
| INT-006 | R29-R30, R33 | BND-COMPOSE-001, BND-ENV-001 | one target package could omit or transform a required reference | existing package-chain checks prove complete raw-byte-consistent resources |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R2, R5, R13, R17 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E2 | illustration | R17, R20 | BND-COMPOSE-001 | - | - |
| E3 | illustration | R6, R10-R11, R14 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E4 | illustration | R7, R10, R12, R14 | BND-STATE-001, BND-AUTH-001 | - | - |
| E5 | illustration | R4, R7-R8 | BND-INPUT-001, BND-RECOVERY-001 | - | - |
| E6 | illustration | R9, R18, R22 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E7 | illustration | R16, R33 | BND-RECOVERY-001, BND-ENV-001 | - | - |
| E8 | illustration | R13, R15 | BND-COMPOSE-001 | - | - |

## Inputs and outputs

Inputs are the direct request or governed invocation, repository and revision identity, governed change or explicit evidence root when final readiness is requested, current project-local contracts and lifecycle artifacts, actual diff, validation evidence, CI evidence when observed, review records, manual proof, generated-output authority, and release metadata when applicable.

Every output records requested outcome, resolved scope or target, execution mode, loaded-resource profile, evidence considered, verdict, blockers, validation status, claim limitations, and next valid handoff.
Scoped outputs use `pass`, `fail`, or `inconclusive`; final-readiness outputs use `branch-ready` or `not-ready` within the existing verify claim boundary.

## State and invariants

- Requested outcome, resource profile, and execution mode are separate closed classifications.
- Conditional resources provide procedure but never authority.
- One verdict uses one repository/revision and one final evidence identity.
- Item-level evidence meaning remains inline; only final applicability and aggregation are conditional.
- Verify-owned recording does not imply workflow-owned progression.
- The full published skill is `SKILL.md` plus explicitly mapped references under one `verify` owner.
- Rule and literal inventories are change-local proof, not recurring product state.

## Error and boundary behavior

- Unknown or ambiguous outcomes stop before conditional loading.
- Missing, stale, contradictory, or cross-target final identities stop with the unresolved identity named.
- An unreadable triggered reference is a package-integrity blocker; the skill does not reconstruct it.
- Unknown ledger vocabulary fails before destination or consistency validation.
- Missing or failed validation is not evidence of success.
- Isolated success cannot advance workflow or invoke `pr`.
- Governed-final invocation without current same-change authority stops rather than degrading to a formal final verdict.

## Compatibility and migration

Current verification verdict meanings, status vocabulary, lifecycle and review checks, result fields, claim boundaries, and handoff ownership remain compatible.
The migration moves conditional procedure and deduplicates prose; it does not migrate user data or change `change.yaml`.

Canonical skill changes, mapped resources, affected literal consumers, generated packages, archives, and installed-package proof roll out atomically.
Rollback restores the complete prior canonical package and consumer set, then regenerates and revalidates derived packages.

## Observability

Implementation evidence records the semantic rule ledger, literal inventory, scenario fixtures, baseline and after measurements, per-profile loaded resources, duplicate-cluster disposition, package-chain proof, and independent semantic review.
Command evidence names the exact command, owner, milestone, result, and evidence artifact.
No transcript, model identity, or target-runtime output is acceptance evidence.

## Security and privacy

The change introduces no network, credential, secret, user-data, or external-action requirement.
Static fixtures and package checks use repository-local content only.
Path containment and package parity prevent references from escaping the skill root or disappearing in an installed target.

## Accessibility and UX

No graphical interface is changed.
The shorter common path and closed vocabulary improve instruction scanability, while exact diagnostics identify unresolved targets and missing resources.

## Performance expectations

`VP0-scoped` loaded words and bytes must be materially lower than the baseline without weakening semantic coverage.
The 30-40 percent reduction is advisory, and total package size is reported separately.
No runtime performance, latency, or model-token guarantee is introduced.

## Edge cases

EC1. A request names a branch but two active changes; final readiness stops as ambiguous.

EC2. A direct request says "final verify" without governed evidence; it cannot enter `governed-final` mode.

EC3. A scoped CI check has only local output; it may report local evidence but cannot claim hosted CI passed.

EC4. A generated artifact exists but its source or generation contract is unknown; the result is inconclusive or blocked, not current.

EC5. Manual proof is asserted without performer, date, procedure, or evidence; it cannot support the claim.

EC6. The branch-readiness reference is absent from one installed adapter; package validation and dependent verification fail.

EC7. Boundary-first is triggered during scoped verification; only the boundary reference is added and the branch-readiness reference remains unloaded.

EC8. `release_sensitive` is missing when materially undecidable; final readiness stops rather than assuming false.

EC9. An incidental test expects an old sentence; the test migrates while normative semantics remain.

EC10. The common path shrinks but final package content duplicates universal rules; acceptance fails semantic ownership review.

## Non-goals

- Changing workflow stages, state schemas, review settlement, planned-work semantics, CI policy, release policy, or PR authorization.
- Giving `verify` release, deployment, publication, PR preparation, or PR opening authority.
- Adding a result asset or fragmenting final readiness into multiple references.
- Building an executable verifier, scheduler, selector, cache, state store, or target-agent test harness.
- Adding permanent size, prose-quality, tokenizer, fixture-framework, or runtime-certification validators.
- Optimizing another skill or introducing a cross-skill abstraction.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-VFSIM-001 | Every invocation resolves one closed requested outcome or stops before conditional loading. |
| AC-VFSIM-002 | Final readiness resolves exactly one repository revision and one change or evidence root. |
| AC-VFSIM-003 | Release sensitivity changes evidence applicability only. |
| AC-VFSIM-004 | Exactly four resource profiles are assembled, with boundary-first independently additive. |
| AC-VFSIM-005 | Resource profile and execution mode are independently classified. |
| AC-VFSIM-006 | Isolated final readiness neither mutates workflow state nor invokes or prepares `pr`. |
| AC-VFSIM-007 | Governed-final recording and handoff preserve verify, workflow, and pr ownership. |
| AC-VFSIM-008 | Item-level evidence semantics remain inline and scoped checks need no final-readiness reference. |
| AC-VFSIM-009 | The branch reference owns final applicability and aggregation only. |
| AC-VFSIM-010 | Missing triggered resources stop before dependent work and are never reconstructed. |
| AC-VFSIM-011 | Every semantic rule and literal dependency has one valid classified disposition. |
| AC-VFSIM-012 | Measurements report profile and package words/bytes separately and keep percentage reduction advisory. |
| AC-VFSIM-013 | Acceptance executes no target-agent runtime and introduces no permanent simplicity machinery. |
| AC-VFSIM-014 | Canonical, generated, packed, and installed packages preserve every mapped resource and required raw-byte parity. |
| AC-VFSIM-015 | Existing verification, lifecycle, review, evidence, release, claim, stop, output, and handoff semantics remain intact. |
| AC-VFSIM-016 | Architecture applicability is recorded before planning, and rollout and rollback remain complete-package operations. |

## Open questions

None.

## Next artifacts

- Independent `spec-review`.
- Recorded architecture assessment and architecture work only if required.
- Execution plan and independent `plan-review`.
- Test specification and independent `test-spec-review`.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.
The specification closes the requested-outcome, target, execution-authority, resource-ownership, evidence, failure, compatibility, measurement, and proof contracts without authorizing implementation.
