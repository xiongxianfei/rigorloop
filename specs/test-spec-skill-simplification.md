<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/spec/SKILL.md -->
<!-- Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Test-Spec Skill Simplification

## Owning change record

`docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Test-Spec Skill Simplification](../docs/proposals/2026-08-13-test-spec-skill-simplification.md)
- Approved [proposal-review R4](../docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r4.md)

## Goal and context

This specification defines a shorter published `test-spec` skill package without weakening the existing proof-design, lifecycle, boundary-first, resource-integrity, or handoff contracts. The universal skill remains sufficient for portable proof design, while one conditionally loaded reference owns exact governed creation, revision, retry, and same-entry stale-authoring restart procedure.

The change preserves both existing boundary-first references as initially loaded procedure and preserves exactly five structural assets. It removes duplicated stage-local procedure and layout, makes each repeated structure single-owned, and measures the portable and governed loaded profiles separately from total package size.

## Glossary

- `portable profile`: `TSA0-portable`, consisting of `SKILL.md` plus both required boundary-first references and no governed authoring reference.
- `governed profile`: `TSA1-governed`, consisting of the portable profile plus `references/governed-test-spec-authoring.md` after candidate evidence activates it.
- `governed candidate`: evidence pointing to exactly one current `stage-owned-change-local-v1` change that plausibly requires test-spec creation or revision; it selects a reference but does not grant write authority.
- `retry identity`: the complete identity tuple that permits reconciliation of one interrupted creation or revision attempt without silently rebinding it.
- `same-entry restart`: a test-spec-owned restart of one stale, incomplete, unreviewed `authoring` entry that preserves its artifact ID and canonical path while replacing its authoring-evidence path and retry identity.
- `structural asset`: one of the five existing copy-and-fill files that owns output labels, ordering, placeholders, or repeated row or case shape but no proof or lifecycle policy.
- `optional manual verification`: the existing manual or hybrid evidence mode represented through current proof, case, milestone, and optional Manual QA structures; it is not a separate artifact or new contract.

## Examples first

### Example E1: portable authoring loads no governed procedure

Given a user requests a test specification without current governed change authority, when `test-spec` classifies the invocation, then it loads the universal skill and both required boundary references, does not load the governed reference, and writes no change-local lifecycle state.

### Example E2: governed creation establishes its entry before content

Given exactly one governed change authorizes a new primary test spec at a deterministic path, when authoring begins, then `test-spec` creates only the matching entry in `authoring`, binds its authoring evidence, writes and validates the artifact, and leaves that entry `review-required`.

### Example E3: candidate loading does not grant authority

Given conversational or repository evidence plausibly identifies a governed test-spec operation, when the governed reference loads but exact change, input, state, or path validation fails, then authoring stops before content or lifecycle mutation.

### Example E4: an identical creation retry resumes

Given an interrupted creation has the same change, artifact ID, path, authoring-evidence path, and governing input identities, when it is retried, then the procedure resumes or completes the exact partial transaction without creating another entry or authoring occurrence.

### Example E5: changed-basis creation restarts the same entry

Given an incomplete unreviewed `authoring` entry was created from stale governing inputs and workflow has routed a valid restart, when `test-spec` proves there is no review or downstream reliance, then it preserves the entry ID and canonical path, replaces only its authoring-evidence path, binds current inputs and a new retry identity, and never uses `abandoned` or a duplicate entry.

### Example E6: revision invalidates prior settlement

Given a review finding or authorized upstream change requires revision of one exact test spec, when revision is permitted, then `test-spec` preserves prior authoring and review evidence as history, writes a new content identity, returns the matching entry to `review-required`, and requires fresh `test-spec-review`.

### Example E7: active implementation reliance blocks ordinary revision

Given implementation has relied on the active test-spec identity, when ordinary `test-spec` revision is requested, then the skill stops and routes to a separately governed reopen, replan, or proof-contract migration decision.

### Example E8: structural composition has one owner per shape

Given a complete new test spec is authored, when the output is composed, then the skeleton owns section order and insertion positions while the case and row assets own their repeated bodies, and no insertion marker or unfilled placeholder is emitted.

### Example E9: automated proof adds no manual ceremony

Given automation fully proves an obligation, when the test case and milestone rows are authored, then no manual procedure ID is invented and existing inapplicable sentinels are used where the owning structure requires them.

### Example E10: manual or hybrid evidence uses existing owners

Given the governing proof contract requires manual or hybrid evidence, when the proof map is authored, then current proof, test-case, milestone, and optional Manual QA structures carry the required fields without a new manual-proof record or asset.

### Example E11: missing required resource fails safely

Given either required boundary reference is missing or a governed candidate requires an unavailable governed reference, when authoring starts, then the skill stops before dependent interpretation or mutation rather than reconstructing procedure from memory.

### Example E12: simplification reports loaded and total size honestly

Given the package is revised, when change evidence is calculated, then `TSA0-portable`, `TSA1-governed`, each resource, representative asset assemblies, and the complete package are reported separately, and relocation is not described as deletion.

## Requirements

### Package and universal contract

R1. The canonical published package MUST contain `skills/test-spec/SKILL.md`, `references/governed-test-spec-authoring.md`, the two existing boundary-first references, and exactly the five existing test-spec assets.

R2. `SKILL.md` MUST remain self-sufficient for purpose, inputs, proof-design policy, requirement and boundary coverage, validation-command ownership, milestone proof timing, gaps, stops, claims, portable isolation, handoff, and every resource trigger.

R3. `SKILL.md` MUST map every packaged reference with `READ` and every packaged asset with `COPY`, using repository-valid relative paths and explicit use conditions.

R4. Both existing boundary-first references MUST remain initially loaded for every test-spec authoring profile, and their canonical bytes and projection ownership MUST remain unchanged by this change.

R5. A required reference or applicable structural asset that is missing, unreadable, escaped, contradictory, or mixed-version MUST block the dependent operation before interpretation or mutation.

R6. The skill MUST NOT reconstruct missing governed, boundary, or structural procedure from remembered content.

R7. The governed reference MUST contain only governed test-spec authoring procedure and MUST NOT own universal proof semantics, peer-review settlement, workflow routing, implementation authority, or claims.

### Invocation and authority

R8. The supported procedural profiles MUST be exactly `TSA0-portable` and `TSA1-governed`.

R9. `governed_test_spec_candidate_context` MUST be an evidence-based load predicate and MUST NOT itself grant mutation authority.

R10. Conversational wording alone MUST NOT establish a governed candidate or authorize a governed write.

R11. After loading, the governed reference MUST resolve exactly one change, lifecycle contract, operation, artifact identity or intended identity, normalized path, governing input basis, and current authoring authority before mutation.

R12. The governed operations MUST be the closed values `create-primary-test-spec`, `revise-primary-test-spec`, and `restart-stale-authoring`.

R13. Missing, stale, ambiguous, conflicting, multiple, or illegal authority evidence MUST stop before content or lifecycle mutation.

R14. Loading resources MUST NOT authorize modification of another artifact entry, `workflow_state`, routing, automation state, review evidence, or implementation state.

### Governed creation and identical retry

R15. New governed creation MUST resolve one stable artifact ID, deterministic normalized path, authoring-evidence path, and current governing input identities without requiring a pre-existing test-spec entry or file.

R16. Before substantive content is written, creation MUST prove that no unrelated file, entry, or competing primary test spec occupies the intended identities and MUST create only the matching entry in `authoring`.

R17. Creation MUST write the composed test-spec artifact, write complete authoring evidence, validate artifact and evidence identities, and move only the same entry from `authoring` to `review-required`.

R18. Creation retry identity MUST include change ID, artifact ID, normalized path, authoring-evidence path, and every governing input identity.

R19. An identical retry MUST reconcile only the same partial transaction and MUST return idempotent success when the matching entry is already `review-required` with the same complete basis.

R20. A file without its matching entry, an entry with different identity data, multiple candidates, or a changed intended content or governing basis MUST fail closed.

R21. Creation MUST NOT write review evidence, settle the entry to `active`, change workflow routing, or authorize implementation.

### Same-entry stale-authoring restart

R22. A changed-basis incomplete creation MUST first return `stale-authoring-attempt` without implicitly adopting, overwriting, abandoning, or rebinding the attempt.

R23. Workflow MAY validate and route stale-attempt recovery but MUST NOT mutate the test-spec artifact entry or content.

R24. `restart-stale-authoring` MUST be owned by `test-spec`, require the exact entry to remain `authoring`, and prove that no review or downstream reliance exists.

R25. Restart MUST preserve artifact ID, kind, role, normalized canonical path, and `authoring` state and MUST replace only the entry's `authoring_evidence` path.

R26. Restart evidence MUST identify the change, artifact, path, stale retry identity, old and current governing inputs, no-reliance proof, new retry identity, and any preserved partial-content evidence path.

R27. Before replacing incomplete content at the canonical path, restart MUST either record the prior partial bytes as unnecessary incomplete output or preserve required bytes at a distinct change-local evidence path.

R28. Restart MUST NOT use a terminal state, create another primary entry, duplicate the canonical path, mutate review or workflow state, or write automation state.

R29. A non-authoring entry, review or downstream reliance, ambiguous attempt identity, or failure to preserve required partial evidence MUST block restart.

### Governed revision

R30. Revision MUST require exactly one existing entry and file, a known prior content identity, current governing inputs, a legal revision state, one current review finding or authorized upstream-change identity, and no competing revision.

R31. Revision MUST be permitted for current `revision-required`, identical `authoring` retry, authorized pre-settlement correction, or explicitly reopened pre-reliance `active` state and MUST fail for unsupported states.

R32. Ordinary revision of an active test spec already relied on by implementation MUST stop pending a separately governed reopen, replan, or proof-contract migration.

R33. Revision retry identity MUST bind change ID, artifact ID, normalized path, prior content identity, current governing inputs, authorizing finding or upstream change, and revision-authoring evidence path.

R34. Before revising content, `test-spec` MUST move only its matching entry to `authoring`, remove the current review mapping when required, and bind the new authoring-evidence path.

R35. Revision MUST preserve prior authoring and review records as historical evidence for the prior content identity.

R36. Revision MUST compute and record a new content identity, validate the revised artifact and evidence, move only the matching entry to `review-required`, and require fresh independent `test-spec-review`.

R37. An identical revision retry MUST reconcile only the same bound revision attempt; any changed identity component MUST stop rather than silently rebind.

### Settlement and handoff ownership

R38. `test-spec` authoring MUST end with only its matching entry at `review-required` and MUST NOT write peer-review settlement.

R39. Only `test-spec-review` MAY record independent review evidence and settle the matching entry from `review-required` to `active` when approved.

R40. Workflow MAY validate active artifact, review, proof completeness, and synchronization for later routing but MUST NOT rewrite test-spec content or peer-review settlement.

R41. Workflow-managed execution MUST NOT enlarge the `test-spec` write set, and `test-spec` MUST return control to workflow after its authoring result.

R42. The skill MUST NOT claim implementation, validation, verification, branch, PR, release, deployment, or publication readiness.

### Structural assets and optional manual verification

R43. `assets/test-spec-skeleton.md` MUST be the sole owner of full-document section order, headings, table headers, insertion locations, and document-level placeholders.

R44. `assets/test-case.md`, `assets/coverage-map-row.md`, `assets/validation-command-row.md`, and `assets/milestone-proof-row.md` MUST each be the sole owner of its repeated body shape.

R45. The full skeleton MUST NOT duplicate example body rows or complete test-case bodies owned by smaller assets.

R46. New full-document authoring MUST use the skeleton plus every applicable repeated asset; bounded revision MUST load only the structural assets needed for the changed structures.

R47. Insertion markers and unfilled placeholders MUST NOT appear in authored output.

R48. Assets MUST own labels, ordering, columns, and placeholders only; applicability, adequacy, status meaning, lifecycle authority, and claims MUST remain in `SKILL.md`, references, or governing specs.

R49. Optional manual verification MUST continue using the existing proof reference, proof-obligation structure, test-case fields, milestone manual-proof IDs, and optional Manual QA location.

R50. This change MUST NOT add a manual-proof contract, conditional manual-proof asset group, or sixth test-spec asset.

R51. Automated proof MUST omit manual procedure IDs when inapplicable, while manual and hybrid proof MUST cite the current required procedure and evidence fields using existing structures.

### Semantic preservation, validation, and measurement

R52. Every behaviorally significant current rule MUST receive exactly one disposition and destination in `test-spec-rule-disposition.yaml`.

R53. Every exact current literal consumer MUST receive one classification and treatment in `test-spec-literal-compatibility.yaml`, separate from semantic rule preservation.

R54. Closed vocabularies introduced or changed by this work MUST reject unknown values before consistency checks and MUST include unknown-value regression proof.

R55. Static contract fixtures MUST cover every valid and invalid profile, authority, creation, retry, restart, revision, settlement, structural composition, resource failure, proof mode, and forbidden-write outcome defined by this specification.

R56. Acceptance MUST use deterministic structure and package proof, static fixtures, and independent semantic review and MUST NOT execute Codex, Claude Code, opencode, or another target-agent runtime.

R57. Required profile measurements MUST use canonical files, LF-normalized content, UTF-8 bytes, Unicode whitespace-separated words, documented load order, and each unique loaded resource exactly once.

R58. `TSA0-portable`, `TSA1-governed`, representative full-create and bounded-revision assemblies, every resource, duplicate clusters, and total package size MUST be reported separately.

R59. Both procedural profiles MUST decrease from baseline, every duplicate cluster MUST have one loaded owner, and semantic and lifecycle behavior MUST be preserved; no fixed percentage MAY override preservation.

R60. Token estimates MAY be reported only through an existing repository-owned pinned implementation and MUST NOT require a new tokenizer dependency.

R61. Change-local ledgers, measurements, duplicate counts, and prose judgments MUST NOT create a new permanent validator family or permanent size gate.

R62. Canonical, generated, packed, archived, and clean-installed skill packages MUST preserve required paths and raw-byte parity for every mapped untransformed resource.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R8, R9, R10, R11, R12, R13, R14, R18, R30, R33 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | BND-STATE-001, BND-STATE-002 | - |
| identity-authority | applicable | R9, R10, R11, R12, R13, R14, R18, R19, R20, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37 | BND-AUTH-001, BND-AUTH-002 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R6, R7, R43, R44, R45, R46, R47, R48, R49, R50, R51 | BND-COMPOSE-001, BND-COMPOSE-002 | - |
| temporal-retry | applicable | R18, R19, R20, R22, R23, R24, R25, R26, R27, R28, R29, R33, R34, R35, R36, R37 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R5, R6, R20, R22, R23, R24, R25, R26, R27, R28, R29, R37 | BND-RECOVERY-001, BND-RECOVERY-002 | - |
| compatibility-migration | applicable | R4, R35, R49, R50, R51, R52, R53, R62 | BND-COMPAT-001 | - |
| external-environment | applicable | R5, R42, R56, R62 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R8, R9, R10, R11, R12, R13, R14, R18, R30, R33 | portable request; exact governed candidate; missing, stale, conflicting, or multiple identity inputs | one invocation resolves one profile and at most one governed operation | valid inputs select procedure; invalid inputs stop before write | R11 |
| BND-STATE-001 | state-lifecycle | R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | absent entry to `authoring` to `review-required`; review-owned transition to `active` | each stage mutates only its owned entry or evidence | legal transition succeeds; illegal or cross-owner transition stops | R38 |
| BND-STATE-002 | state-lifecycle | R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | incomplete creation; stale creation; revision-required; reopened active; relied-on active | restart stays `authoring`; revision returns to `review-required`; relied-on active is immutable to ordinary authoring | exact operation proceeds; unsupported state stops | R24 |
| BND-AUTH-001 | identity-authority | R9, R10, R11, R12, R13, R14, R18, R19, R20, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37 | candidate evidence; exact stage authority; conversational suggestion; workflow routing | loading is not authority; workflow cannot write stage-owned entry | exact authority permits bounded operation; other evidence stops | R9 |
| BND-AUTH-002 | identity-authority | R9, R10, R11, R12, R13, R14, R18, R19, R20, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37 | exact retry tuple; changed tuple; ambiguous or competing attempts | retry never silently rebinds | exact retry reconciles; changed or ambiguous identity stops | R18 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R6, R7, R43, R44, R45, R46, R47, R48, R49, R50, R51 | portable resources; governed reference; missing or mixed package | every packaged resource has one map entry and one procedure owner | correct assembly loads; defective required assembly stops | R3 |
| BND-COMPOSE-002 | composition-path | R1, R2, R3, R4, R5, R6, R7, R43, R44, R45, R46, R47, R48, R49, R50, R51 | full creation; bounded revision; automated, manual, or hybrid proof | skeleton owns frame; smaller assets own repeated bodies; no sixth asset | applicable assets compose output; duplicate or placeholder output fails | R43 |
| BND-TEMPORAL-001 | temporal-retry | R18, R19, R20, R22, R23, R24, R25, R26, R27, R28, R29, R33, R34, R35, R36, R37 | interruption before file, before evidence, before transition, after completion; repeated restart or revision | one identity-bound attempt produces one effective result | exact retry resumes or is idempotent; changed basis routes to restart or stops | R19 |
| BND-RECOVERY-001 | failure-recovery | R5, R6, R20, R22, R23, R24, R25, R26, R27, R28, R29, R37 | stale partial content absent, disposable, or audit-relevant; review or reliance present | same entry and path persist; required bytes are preserved before replacement | safe restart proceeds; unsafe or relied-on attempt blocks | R27 |
| BND-RECOVERY-002 | failure-recovery | R5, R6, R20, R22, R23, R24, R25, R26, R27, R28, R29, R37 | missing resource; collision; mismatched file and entry; conflicting retry | no fallback invention or implicit adoption | dependent operation stops with concrete blocker | R5 |
| BND-COMPAT-001 | compatibility-migration | R4, R35, R49, R50, R51, R52, R53, R62 | current boundary resources; historical test specs and review evidence; current literal consumers | historical evidence remains historical; resource bytes and stable semantics remain compatible | new package works; history is not rewritten; incompatible drift blocks | R62 |
| BND-ENV-001 | external-environment | R5, R42, R56, R62 | canonical source; generated, packed, archived, installed trees; external or target-agent execution | acceptance is repository-local and package parity is deterministic | parity passes locally; missing installed resource blocks; external action remains unauthorized | R56 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R18, R19, R20 | BND-AUTH-001, BND-STATE-001 | a plausible governed candidate is mistaken for permission to create or transition state | reference selection occurs first, exact authority validation occurs second, and failure stops before mutation |
| INT-002 | R23, R24, R25, R26, R27, R28, R29 | BND-AUTH-002, BND-TEMPORAL-001, BND-RECOVERY-001 | an interrupted attempt is rebound to changed inputs or replaced through an illegal terminal/duplicate path | changed basis reports stale, workflow routes, and test-spec restarts the same entry under a new bound attempt |
| INT-003 | R35 | BND-STATE-002, BND-AUTH-001, BND-COMPAT-001 | revision invalidates review or implementation reliance silently | prior evidence remains historical, new identity requires fresh review, and relied-on active state blocks ordinary revision |
| INT-004 | R49, R50, R51 | BND-COMPOSE-002, BND-COMPAT-001 | simplification removes proof behavior or adds manual ceremony while deduplicating structure | current semantics remain, one asset owns each shape, and deterministic fixtures prove all modes without a target runtime |
| INT-005 | R5 | BND-COMPOSE-001, BND-RECOVERY-002, BND-ENV-001 | a smaller main file hides a required-resource packaging failure | every required package layer retains exact resources and dependent use stops when one is missing |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R8, R9, R10 | BND-INPUT-001 | - | - |
| E2 | illustration | R15, R16, R17 | BND-STATE-001 | - | - |
| E3 | illustration | R9, R10, R11, R12, R13, R14 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E4 | illustration | R18, R19, R20 | BND-AUTH-002, BND-TEMPORAL-001 | - | - |
| E5 | regression | R22, R23, R24, R25, R26, R27, R28, R29 | BND-STATE-002, BND-TEMPORAL-001, BND-RECOVERY-001 | TSSIM-PR7 | - |
| E6 | illustration | R35 | BND-STATE-002, BND-AUTH-002, BND-COMPAT-001 | - | - |
| E7 | illustration | R32 | BND-STATE-002, BND-AUTH-001 | - | - |
| E8 | illustration | R43, R44, R45, R46, R47, R48 | BND-COMPOSE-002 | - | - |
| E9 | illustration | R49, R50, R51 | BND-COMPOSE-002, BND-COMPAT-001 | - | - |
| E10 | illustration | R49, R50, R51 | BND-COMPOSE-002, BND-COMPAT-001 | - | - |
| E11 | illustration | R5, R6 | BND-COMPOSE-001, BND-RECOVERY-002 | - | - |
| E12 | illustration | R62 | BND-ENV-001 | - | - |

## Inputs and outputs

Inputs are the accepted proposal and approved review, the current `test-spec` skill package, governing skill/resource/lifecycle/proof contracts, exact current literal and validator consumers, canonical and derived package inventories, and one governed change record when governed authoring applies.

Outputs are a simplified canonical skill, one new governed reference, revised existing structural assets where needed to remove duplication, directly coupled deterministic validation and fixtures, generated/package parity evidence, two change-local preservation ledgers, profile measurements, and stage-owned lifecycle evidence. No target-agent transcript, runtime score, new manual-proof artifact, or external-system mutation is an output.

## State and invariants

- `skills/` remains the only authored skill source; generated and installed copies are derived.
- Portable authoring writes no governed state.
- Governed authoring changes only its exact test-spec content, authoring evidence, and matching artifact entry.
- Authoring completion is `review-required`; `active` is review-owned settlement.
- Same-entry restart preserves the artifact identity and path and does not use a terminal state.
- Prior review evidence remains bound to its prior content identity.
- Workflow-managed automation does not enlarge stage write authority.
- Boundary references retain their current initial-loading and byte-identity contract.
- Assets remain structural leaves and never become policy owners.

## Error and boundary behavior

Every unknown closed-vocabulary value, missing required resource, ambiguous profile, unresolved identity, illegal state, unrelated file collision, mismatched retry, concurrent competing attempt, review or downstream reliance during stale restart, and active implementation reliance during ordinary revision fails closed with a concrete blocker. Failure before a permitted write leaves governed state unchanged. An interrupted permitted write may be reconciled only through the exact creation, restart, or revision retry identity defined above.

## Compatibility and migration

Historical test specs, reviews, and evidence are not rewritten. Existing boundary references and their initial-loading contract remain unchanged. Existing optional Manual QA behavior and proof fields remain unchanged. New authored packages use the revised ownership model, while exact parser or package literals are either preserved or migrated with every consumer in the same implementation slice. Rollback atomically restores the prior skill, assets, validators, and generated packages; change-local evidence may remain as historical rationale.

## Observability

The change is observable through canonical diffs, resource-map inventory, semantic-rule and literal ledgers, static scenario results, validator output, portable and governed size reports, duplicate-cluster counts, package parity evidence, review records, and lifecycle metadata. These surfaces must distinguish configured commands from commands actually run and must not describe relocated content as deleted.

## Security and privacy

The change introduces no credentials, secrets, network operation, external persistence, or new personal-data processing. Existing command side-effect boundaries remain mandatory. The skill and acceptance workflow must not publish, deploy, release, push, merge, or execute a target-agent runtime.

## Accessibility and UX

Not applicable to end-user interface accessibility. The published Markdown must remain readable: complete prose sentences stay intact, repeated mappings use tables, and output assets contain no unfilled placeholders.

## Performance expectations

Both procedural profiles must use fewer LF-normalized UTF-8 bytes and Unicode whitespace-separated words than their baselines. Measurement must be deterministic and change-local. No runtime latency or throughput contract is introduced.

## Edge cases

EC1. A direct request says “use the current change” but no exact governed identity resolves: use `TSA0-portable` only when portable authoring is otherwise valid; do not infer governed mutation.

EC2. A governed candidate resolves but the reference is absent: stop before reading or writing governed state.

EC3. Creation is interrupted after entry creation but before file creation: an exact retry resumes file creation.

EC4. Creation is interrupted after file creation but before complete authoring evidence: an exact retry validates the content basis and completes evidence.

EC5. Governing inputs change after partial creation: report `stale-authoring-attempt`; do not silently rebind.

EC6. Stale restart finds review or implementation reliance: stop without replacing evidence or content.

EC7. Required partial bytes cannot be preserved: stop before same-path replacement.

EC8. Revision is requested from `active` before implementation reliance and workflow explicitly reopens it: revision may proceed under exact authority.

EC9. Revision is requested from `active` after implementation reliance: ordinary authoring stops.

EC10. A revision retry has the same file but a different authorizing finding: stop as a different attempt.

EC11. A bounded revision changes only validation-command rows: load the command-row asset and other required procedure, not unrelated output assets.

EC12. Automated proof fully covers a requirement: do not add a manual procedure or Manual QA step.

EC13. Manual evidence is required by the existing proof contract: use current structures and reject incomplete required evidence.

EC14. Total package size grows while loaded profiles shrink: report and justify the growth; do not fail solely on a percentage when all normative gates pass.

EC15. A generated or installed package omits the new governed reference: package parity fails even if canonical validation passes.

## Non-goals

- Reducing proof rigor, coverage, validation-command ownership, milestone timing, stop conditions, or claim boundaries.
- Changing `boundary-first-v1`, its stable IDs, its two test-spec projections, or their initial-loading policy.
- Changing workflow stage order, peer-review authority, implementation authorization, or PR behavior.
- Adding a runtime engine, scheduler, schema-driven generator, target-agent evaluation, tokenizer dependency, or permanent simplicity validator.
- Adding a manual-proof contract, conditional manual-proof group, or sixth asset.
- Optimizing `test-spec-review` or another skill in this change.
- Rewriting historical test specs or review evidence.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-TSSIM-001` | The package contains the universal skill, one governed reference, both unchanged boundary references, and exactly five structural assets. |
| `AC-TSSIM-002` | Portable and governed profiles use exact evidence-based load rules and loading never grants mutation authority. |
| `AC-TSSIM-003` | New creation establishes one `authoring` entry before content and ends with only that entry `review-required`. |
| `AC-TSSIM-004` | Every interrupted creation state has one deterministic resume, idempotent, stale, or stop result bound to the complete retry identity. |
| `AC-TSSIM-005` | Stale recovery restarts the same `authoring` entry and never uses `abandoned`, a duplicate primary entry, or a duplicate canonical path. |
| `AC-TSSIM-006` | Required partial bytes are preserved at a distinct evidence path before replacement. |
| `AC-TSSIM-007` | Revision has closed authority, state, identity, write, retry, historical-evidence, fresh-review, and active-reliance behavior. |
| `AC-TSSIM-008` | `test-spec`, `test-spec-review`, and workflow retain non-overlapping authoring, settlement, and routing write boundaries. |
| `AC-TSSIM-009` | The skeleton and four repeated-body assets each have one structural ownership boundary and emit no duplicate bodies or placeholders. |
| `AC-TSSIM-010` | Optional manual verification uses only existing structures and no new manual-proof contract or asset exists. |
| `AC-TSSIM-011` | Missing, invalid, ambiguous, conflicting, unknown, or mixed-version inputs fail before dependent interpretation or mutation. |
| `AC-TSSIM-012` | Semantic rules and exact literal dependencies have separate complete disposition ledgers. |
| `AC-TSSIM-013` | Every new or changed closed vocabulary has unknown-value-first regression proof. |
| `AC-TSSIM-014` | Static fixtures cover the complete valid and invalid profile, transaction, resource, proof-mode, and write-authority matrix. |
| `AC-TSSIM-015` | No Codex, Claude Code, opencode, or other target-agent runtime executes for acceptance. |
| `AC-TSSIM-016` | Both procedural profiles decrease from baseline and total package change is reported separately without a normative percentage gate. |
| `AC-TSSIM-017` | Canonical, generated, packed, archived, and clean-installed mapped resources retain required relative-path and raw-byte parity. |
| `AC-TSSIM-018` | Independent semantic review confirms proof, lifecycle, boundary, compatibility, and handoff behavior are preserved. |

## Open questions

None. Exact current literal consumers, validator command owners, and approved manual-evidence field names are implementation inventories, not unresolved contract decisions.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment with expected `architecture-not-required`.
- Execution plan and `plan-review`.
- Test specification and independent `test-spec-review`.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This authoring result does not claim spec approval, architecture completion, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
