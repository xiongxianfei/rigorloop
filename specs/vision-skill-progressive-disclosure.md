<!-- Template: spec-skeleton-v1 | Skill: spec | Template status: normative | Maintained alongside: skills/spec/SKILL.md | Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Vision Skill Progressive Disclosure

## Owning change record

`docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Vision Skill Progressive Disclosure](../docs/proposals/2026-08-17-vision-skill-progressive-disclosure.md)
- Approved [proposal-review R5](../docs/changes/2026-08-17-vision-skill-progressive-disclosure/reviews/proposal-review-r5.md)
- Existing consolidated behavior contract: [Vision Skill](vision-skill.md)

## Goal and context

This specification defines progressive disclosure for the published `vision` skill without weakening the consolidated vision contract. The compact universal file retains operation, authority, safety, and resource selection. One strategic-authoring reference owns detailed positioning and drafting method, one README-synchronization reference owns marker mechanics, and two copied assets own the distinct stable structures of `VISION.md` and `docs/vision/strategic-positioning.md`.

This focused contract supplements `specs/vision-skill.md`. Where it defines package composition, internal operation classification, conditional resource loading, secondary-artifact actions, operation manifests, or package acceptance, this contract is the more specific source. Existing vision content, word-limit, marker, privacy, research, proposal-fit, and canonical-path requirements remain unchanged.

## Glossary

- `pre-resolved skip`: an exact current owner instruction authorizing README omission before marker inspection.
- `late skip`: a skip selected after the README synchronization reference has loaded or marker evidence has contributed to the decision.
- `operation manifest`: the identity-bound record of one mutation-capable or skip-settled invocation, including applicable targets, actions, baselines, intended identities, and evidence state.
- `primary assembly`: a normal synchronization path used for acceptance measurement: `VA0-readme-sync`, `VA1-editorial-sync`, or `VA2-strategic-sync`.
- `secondary skip assembly`: a pre-resolved skip path: `VA0S-readme-skip`, `VA1S-editorial-skip`, or `VA2S-strategic-skip`.
- `marker-evidence state`: either an exact marker state produced by README procedure or `not-evaluated-under-exact-skip`.

## Examples first

### Example E1: normal README synchronization

Given `VISION.md` exists and README synchronization is requested without pre-resolved skip authority, when the skill classifies resources, then `VA0-readme-sync` loads the README reference and no strategic reference.

### Example E2: pre-resolved README skip

Given an exact current owner instruction authorizes README omission before marker inspection, when `sync-readme` runs, then `VA0S-readme-skip` loads no README reference, parses no markers, changes no files, and settles through an operation manifest with unchanged file identities.

### Example E3: marker-dependent late skip

Given marker state must be inspected before skip can be selected, when the README reference loads and the final action becomes skip, then the invocation retains the corresponding non-`S` assembly.

### Example E4: editorial revision becomes strategic

Given a proposed editorial revision reveals changed strategic assumptions, when classification is refined, then the strategic reference loads before final judgment or mutation and the invocation becomes `VA2` or `VA2S` according to README authority.

### Example E5: material repositioning with README sync

Given an authorized material repositioning affects canonical vision and positioning rationale, when the invocation prepares its operation manifest, then intended content and identities for all applicable targets are validated before `VISION.md`, rationale, and README commit in source-first order.

### Example E6: interrupted derived write

Given canonical vision and rationale match the manifest but README synchronization was interrupted, when an exact retry runs, then it may complete only the pending README target after revalidating every recorded identity and authority.

### Example E7: malformed markers without authority

Given revision or sync encounters missing, malformed, nested, duplicate, or ambiguous markers without exact current insertion or skip authority, when marker procedure classifies the state, then the operation stops before any target write.

### Example E8: historical narrow revision

Given an existing historical `VISION.md` needs a narrow authorized edit, when revision proceeds, then existing structure is preserved and the new skeleton is not imposed solely to adopt this package change.

### Example E9: missing required resource

Given a triggered reference or copied asset is missing, unreadable, escaped, contradictory, stale, or from a mixed package version, when dependent work begins, then the skill stops without reconstructing procedure from memory.

### Example E10: lost portable manifest

Given a portable multi-target operation is interrupted and its manifest is unavailable in a later invocation, when recovery is requested, then the skill stops for explicit owner-directed recovery instead of adopting or overwriting partial state.

## Requirements

### Package and universal ownership

R1. The canonical package MUST contain `skills/vision/SKILL.md`, `references/strategic-vision-authoring.md`, `references/readme-vision-sync.md`, `assets/vision-skeleton.md`, and `assets/strategic-positioning-skeleton.md` and MUST contain no helper script for this feature.

R2. `SKILL.md` MUST remain self-sufficient for workflow placement, source precedence, canonical paths, operation and repository-state classification, revision significance, edit authority, privacy, research, resource triggers, stops, claims, result fields, and no-automatic-handoff behavior.

R3. The strategic reference MUST own detailed strategic-positioning, product-category, methodology applicability, drafting heuristic, word-limit application, full-content quality, and strategic summary procedure.

R4. The README reference MUST own exact marker parsing, invalid-marker classification, deterministic authorized insertion, front-matter derivation, bounded replacement, outside-byte preservation, idempotence, and README result procedure.

R5. Loading a reference or copying an asset MUST NOT grant establishment, revision, insertion, skip, lifecycle, routing, review, or continuation authority.

R6. The resource map MUST use `READ` for both references and `COPY` for both assets with exact contained relative paths and deterministic triggers.

R7. A missing, unreadable, escaped, stale, contradictory, or mixed-version required resource MUST stop dependent judgment or mutation without remembered reconstruction.

### Operation, significance, and resource classification

R8. Mutation operation MUST be exactly `establish-vision`, `revise-vision`, or `sync-readme`; ordinary read-only questions MUST remain outside the mutation-operation vocabulary.

R9. `revise-vision` significance MUST be classified internally as `editorial`, `substantive-nonmaterial`, or `material-repositioning` while preserving the existing public `editorial` and `substantive` result vocabulary.

R10. Strategic procedure context MUST be exactly `false` or `true`; README procedure context MUST be exactly `required` or `skipped`; and the two contexts MUST be classified independently after operation resolution.

R11. `blocked` MUST be an operation result and MUST NOT be represented as a loaded assembly.

R12. Establishment MUST require absent canonical `VISION.md` plus explicit establishment intent; existing canonical vision MUST route establishment intent to explicit revision.

R13. Revision MUST require existing canonical `VISION.md` plus exact update intent; absent canonical vision MUST route revision intent to establishment.

R14. README synchronization MUST require existing canonical `VISION.md` and MUST leave it unchanged.

R15. An editorial revision MUST NOT load strategic procedure unless uncertainty, changed assumptions, or conflict prevents safe editorial classification.

R16. A substantive revision MUST load strategic procedure before final classification or mutation.

R17. Late strategic evidence MUST load the strategic reference and reclassify the assembly before dependent judgment or mutation.

### README applicability and authority

R18. Establishment MUST synchronize README and MUST load the README reference; automatic insertion authority remains limited to initial establishment under the consolidated contract.

R19. Revision and explicit sync MUST load README procedure by default.

R20. A secondary skip assembly MAY be selected only when one exact current owner instruction authorizes README omission before marker inspection.

R21. A pre-resolved skip MUST bind the complete current README content identity, MUST use `marker_state: not-evaluated-under-exact-skip`, MUST NOT parse markers, and MUST NOT claim marker validity.

R22. If README procedure or marker inspection contributes to a skip decision, the invocation MUST retain the corresponding non-`S` assembly even when its final README action is `skip`.

R23. Missing, malformed, nested, duplicate, or ambiguous markers MUST NOT imply skip authority and MUST stop mutation unless exact current insertion or skip authority applies.

R24. Silence, conversational omission, remembered approval, historical authority, or malformed marker state MUST NOT establish insertion or skip authority.

R25. Every insertion or skip MUST bind one governing requirement or exact current owner instruction, operation, operation-manifest identity, prior and intended canonical vision identities, current README identity, marker-evidence state, and authorized action.

R26. An exact planned prior-to-intended canonical transition MUST preserve the bound README action; any other canonical identity, README identity, action, manifest, or authority change MUST invalidate it.

R27. A marker change MUST invalidate any action whose authority used inspected marker evidence; a pre-resolved skip MUST instead be invalidated by any whole-file README identity change.

### Secondary artifacts and structural assets

R28. Positioning action MUST be exactly `unchanged`, `create`, `update`, `full-rewrite`, or `blocked`; README action MUST be exactly `synchronize-existing`, `insert-and-synchronize`, `skip`, or `blocked`.

R29. Positioning and README actions MUST be classified independently from public revision significance.

R30. Initial establishment MUST create positioning rationale; an unrelated pre-existing rationale MUST block adoption.

R31. Editorial revision and substantive nonmaterial revision with no positioning effect MUST leave rationale unchanged.

R32. Changed positioning assumptions or one authorized discovered-conflict correction MUST update rationale; unresolved owner choice MUST block.

R33. Material repositioning MUST update rationale, create it when required and absent, or perform an explicitly authorized full rewrite.

R34. `vision-skeleton.md` MUST own canonical vision headings, ordering, optional methodology and open-question insertion points, and placeholders only.

R35. `strategic-positioning-skeleton.md` MUST own the ten approved positioning headings, their order, the canonical-authority statement location, and placeholders only.

R36. Neither asset MUST own applicability, evidence quality, word limits, authority, lifecycle, README behavior, strategic adequacy, or review status.

R37. Vision skeleton context MUST be exactly `not-required` or `create-or-full-rewrite` and MUST select the asset only for establishment or explicitly authorized full canonical rewrite.

R38. Positioning skeleton context MUST be exactly `not-required` or `create-or-full-rewrite` and MUST select the asset when positioning action is `create` or `full-rewrite`.

R39. Asset selection MUST be independent from strategic-reference and README-reference selection, and narrow historical revisions MUST preserve existing structure.

### Loaded assemblies and operation manifests

R40. Loaded assemblies MUST be exactly `VA0-readme-sync`, `VA0S-readme-skip`, `VA1-editorial-sync`, `VA1S-editorial-skip`, `VA2-strategic-sync`, and `VA2S-strategic-skip`.

R41. `VA0`, `VA1`, and `VA2` MUST be the normal primary measurement profiles; `VA0S`, `VA1S`, and `VA2S` MUST be secondary pre-resolved authority variants and MUST NOT substitute for primary-profile acceptance.

R42. Initial establishment MUST use `VA2-strategic-sync`.

R43. Every mutation-capable or skip-settled invocation MUST resolve one exact operation manifest before the first target write or final skip result.

R44. Every manifest target MUST record path, role, action, prior identity or confirmed absence, intended identity, and applicable evidence state.

R45. A skipped README MUST remain a manifest target with action `skip` and equal prior and intended identities.

R46. A zero-write sync skip manifest MUST include unchanged canonical vision and skipped README targets, equal prior and intended identities for both, and `not-evaluated-under-exact-skip` for README marker state.

R47. Before target mutation or skip settlement, the skill MUST validate operation, significance, actions, paths, authority, content, applicable marker evidence, privacy, provenance, baselines, and intended identities and MUST re-read every target identity.

R48. Target writes MUST occur in source-first order: canonical `VISION.md`, applicable positioning rationale, then derived README.

R49. Immediately before README mutation or skip settlement, the skill MUST revalidate intended canonical identity, prior README identity, applicable marker evidence, authority, and unchanged manifest identity.

R50. Completion MUST require read-back of every required target, including unchanged and skipped targets.

R51. Operation result MUST be exactly `complete`, `partial-retry-required`, or `blocked-before-write`.

R52. A zero-write skip MAY return `complete` only with no changed files, canonical vision reported unchanged, README front-matter reported skipped, and no synchronization or marker-validity claim.

R53. `blocked-before-write` MUST perform no target mutation; `partial-retry-required` MUST report committed targets, pending targets, current identities, manifest identity, and required retry action without claiming synchronization.

R54. Governed work MUST persist the complete operation manifest in existing authorized change-local authoring evidence before the first target write when that evidence model supports the contract.

R55. An identical retry MUST bind the same operation, manifest, targets, inputs, identities, actions, and authority and MAY complete only matching pending targets without duplicate writes or evidence.

R56. Unrelated, stale, ambiguous, lost, or concurrently changed state MUST stop without adoption, overwrite, or destructive rollback.

R57. Portable cross-session recovery MUST remain unsupported when the operation manifest is unavailable; adding it requires prior architecture and contract work.

### Preservation, measurement, and package acceptance

R58. Every behaviorally significant current skill rule MUST receive one disposition and owner in a change-local semantic-rule ledger before refactoring.

R59. Every exact consumed heading, label, path, enum, resource verb, marker, and compatibility-sensitive phrase MUST receive one classification and disposition in a separate literal-compatibility ledger.

R60. Every new or changed closed vocabulary MUST reject unknown values before consistency checks and MUST have an unknown-value regression test.

R61. Measurement MUST use canonical authored files, normalized LF, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded procedural resource once in `SKILL.md`, strategic-reference, README-reference order.

R62. Measurement MUST report all six assemblies, each procedural resource, both assets, and total package size separately.

R63. Each primary and secondary procedural assembly MUST decrease from the 2,268-word and 15,845-byte flat baseline; total package growth MUST remain visible and justified by clearer ownership.

R64. Canonical, generated, archived, release-candidate, and clean-installed resources MUST retain required inventory and raw-byte parity.

R65. Acceptance MUST use deterministic contract, fixture, validator, lifecycle, and package proof and MUST NOT execute a target-agent runtime, grade transcripts, add a prose classifier, add a tokenizer dependency, or add a separate manual semantic-review gate.

R66. If governed manifests require a new persistence surface, schema, lifecycle state, or authority owner, architecture assessment MUST return `architecture-required` before planning.

## Inputs and outputs

Inputs are the accepted proposal and review, consolidated vision contract, current canonical vision skill, repository state and current vision artifacts, exact user authority, package consumers, and a governed change record when lifecycle authoring applies.

Outputs are the compact canonical skill, two references, two assets, directly coupled contract and test updates, semantic and literal ledgers, scenario fixtures, profile measurements, package parity evidence, and stage-owned lifecycle evidence. This feature does not update the project’s current `VISION.md`, strategic-positioning rationale, or README front-matter.

## State and invariants

- `VISION.md` remains the canonical project-vision artifact.
- README front-matter remains derived and marker-bounded.
- Strategic-positioning rationale remains supporting evidence and never overrides canonical vision.
- Resource loading never grants mutation authority.
- Every skip is explicitly authorized and identity-bound.
- Every multi-target or skip-settled result is backed by one operation manifest.
- Historical vision artifacts are not rewritten merely to adopt new skeletons.
- `skills/` remains the only authored skill source.

## Error and boundary behavior

Unknown operations, significance values, contexts, actions, assemblies, results, or marker states fail closed before consistency checks. Ambiguous intent, absent canonical source, invalid authority, malformed markers without handling authority, missing resources, stale identities, unsafe partial state, concurrency, package drift, and lost recovery evidence stop with a concrete blocker. No stop may be reinterpreted as permission to reconstruct procedure, adopt unrelated state, or broaden write scope.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R8, R9, R10, R11, R28, R40, R51 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R30, R31, R32, R33, R43, R47, R48, R49, R50, R51, R52, R53, R54 | BND-STATE-001 | - |
| identity-authority | applicable | R5, R12, R13, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R30, R32, R33, R43, R44, R45, R46, R47, R49, R54 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R6, R7, R10, R15, R16, R17, R34, R35, R36, R37, R38, R39, R40, R41, R42 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R25, R26, R27, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R7, R11, R17, R23, R32, R47, R49, R51, R52, R53, R54, R55, R56, R57, R66 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R34, R35, R36, R37, R38, R39, R58, R59, R60, R61, R62, R63, R64 | BND-COMPAT-001 | - |
| external-environment | applicable | R7, R43, R47, R48, R49, R50, R53, R54, R56, R57, R64, R65, R66 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R8, R9, R10, R11, R28, R40, R51 | three operations, three significance values, two context axes, secondary actions, six assemblies, and three results | unknown vocabulary fails before consistency checks | one valid classification proceeds; invalid input blocks | R8 |
| BND-STATE-001 | state-lifecycle | R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R30, R31, R32, R33, R43, R47, R48, R49, R50, R51, R52, R53, R54 | absent or existing canonical state; editorial, substantive, sync, prepared, writing, skipped, partial, complete, and blocked states | classification and manifest preparation precede dependent writes or settlement | valid work completes or exact partial state is reported; unsafe state blocks | R43 |
| BND-AUTH-001 | identity-authority | R5, R12, R13, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R30, R32, R33, R43, R44, R45, R46, R47, R49, R54 | establishment, revision, insertion, pre-resolved skip, late skip, stale, absent, malformed, or conflicting authority | resource loading and marker state never manufacture authority | exact current authority permits bounded action; other states stop | R25 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R6, R7, R10, R15, R16, R17, R34, R35, R36, R37, R38, R39, R40, R41, R42 | universal file, strategic reference, README reference, two assets, primary and secondary assemblies | each rule and structure has one owner and late evidence loads required resources | exact assembly proceeds; missing, mixed, or under-loaded composition stops | R40 |
| BND-TEMPORAL-001 | temporal-retry | R25, R26, R27, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57 | first attempt, planned canonical transition, zero-write skip, interruption, exact retry, changed basis, lost manifest, and concurrent write | source-first order and retry identity never silently rebind | exact work settles once; changed or unavailable evidence stops | R55 |
| BND-RECOVERY-001 | failure-recovery | R7, R11, R17, R23, R32, R47, R49, R51, R52, R53, R54, R55, R56, R57, R66 | blocked before write, safe partial, unsafe partial, exact retry, lost portable context, or insufficient governed evidence model | partial state is never completion and unrelated state is never adopted | exact pending work may resume; unsafe state or missing architecture support blocks | R53 |
| BND-COMPAT-001 | compatibility-migration | R34, R35, R36, R37, R38, R39, R58, R59, R60, R61, R62, R63, R64 | current and historical structures, semantic rules, literal consumers, canonical and derived package resources | structural adoption is prospective and semantic/literal preservation remain separate | atomic package migration and honest metrics pass or block | R58 |
| BND-ENV-001 | external-environment | R7, R43, R47, R48, R49, R50, R53, R54, R56, R57, R64, R65, R66 | available or missing filesystem resources, atomic writes, generated/archive/install surfaces, target runtime absent | acceptance is repository-owned, deterministic, and non-runtime | package proof passes or readiness blocks | R65 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R10, R15, R16, R17, R40 | BND-INPUT-001, BND-COMPOSE-001 | an apparently editorial path discovers strategic impact after selecting a smaller assembly | strategic procedure loads and assembly reclassifies before judgment or mutation |
| INT-002 | R20, R21, R22, R23, R25, R27, R40, R45, R46, R52 | BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001 | a no-reference skip depends on hidden marker parsing or lacks settlement identity | only pre-resolved authority uses an `S` assembly, whole-file identity and uninspected marker state settle the zero-write result |
| INT-003 | R25, R26, R43, R47, R48, R49, R50, R53, R54, R55, R56 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001 | canonical vision changes invalidate or race supporting and derived writes | one manifest binds the planned transition, source-first writes revalidate identities, and exact retry adopts no unrelated state |
| INT-004 | R34, R35, R36, R37, R38, R39, R58, R59, R61, R62, R63, R64 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | prose relocation hides behavior loss, historical rewrites, or derived-package drift | separate ledgers, independent asset selection, real-profile measurement, and byte parity prove migration |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R14, R19 | BND-STATE-001 | - | - |
| E2 | regression | R43, R45, R46, R52 | BND-TEMPORAL-001 | VISSIM-R4-PR1 | - |
| E3 | regression | R22 | BND-AUTH-001 | VISSIM-R4-PR1 | - |
| E4 | illustration | R15, R16, R17 | BND-STATE-001, BND-COMPOSE-001 | - | - |
| E5 | illustration | R33, R43, R47, R48, R49, R50 | BND-STATE-001 | - | - |
| E6 | illustration | R53, R55, R56 | BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |
| E7 | illustration | R23, R24 | BND-AUTH-001 | - | - |
| E8 | illustration | R39 | BND-COMPAT-001 | - | - |
| E9 | illustration | R7 | BND-COMPOSE-001, BND-ENV-001 | - | - |
| E10 | illustration | R57, R66 | BND-RECOVERY-001 | - | - |

## Compatibility and migration

Existing `VISION.md`, strategic-positioning rationale, README front-matter, proposals, specs, reviews, and historical lowercase-path references remain unchanged. The canonical skill, references, assets, validators, fixtures, selector expectations, package manifests, generated output, archive output, release-candidate output, and installed package migrate as one reviewed slice. Rollback restores the prior flat skill and coupled consumer expectations, removes the new resources, and regenerates derived packages without changing vision artifacts.

## Observability

The change is observable through resource maps, semantic and literal ledgers, deterministic scenario results, profile and total-package measurements, validator output, package inventories and content identities, authoring evidence, review evidence, and lifecycle metadata. Reports must distinguish relocated content from removed content and configured commands from executed commands.

## Security and privacy

The change introduces no credentials, external persistence, network operation, personal-data processing, or publication authority. Existing privacy and research boundaries remain inline. Unsafe paths, unrelated files, sensitive content, and conflicting state stop without adoption or overwrite.

## Accessibility and UX

No graphical end-user interface is changed. Published Markdown MUST remain readable, use complete prose sentences, preserve stable IDs and literal markers, and emit no unfilled placeholders.

## Performance expectations

All six loaded procedural assemblies must use fewer normalized words and UTF-8 bytes than the flat baseline. Total package size is reported separately; no runtime latency or tokenizer-specific contract is introduced.

## Edge cases

EC1. `sync-readme` receives pre-resolved skip authority while README markers are malformed: skip binds whole-file identity without parsing or claiming marker state.

EC2. A skip instruction arrives only after marker inspection: the invocation remains in a non-`S` assembly.

EC3. README changes after pre-resolved skip authority is bound: skip settlement stops because whole-file identity changed.

EC4. A full canonical rewrite skips README: the vision skeleton remains required despite the skip assembly.

EC5. Material repositioning requires absent rationale creation while README is skipped: the positioning skeleton remains required.

EC6. Canonical vision commits but rationale or README remains pending: report `partial-retry-required`, not completion.

EC7. An unknown marker-evidence value reaches validation: reject it before action consistency checks.

EC8. A copied resource exists canonically but is missing from installed output: package parity fails.

## Non-goals

- Changing current project vision, positioning rationale, README front-matter, content structure, word limits, marker literals, or public result vocabulary.
- Restoring lowercase `vision.md` migration behavior or public operating modes.
- Adding `assess-vision`, a normal workflow stage, `vision-review`, a helper script, runtime engine, tokenizer, prose classifier, or target-agent acceptance journey.
- Migrating historical vision artifacts merely to adopt new skeletons.
- Optimizing another skill in this change.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every normative requirement maps to deterministic proof in the test specification. |
| AC2 | Exactly three mutation operations, two resource predicates, independent asset predicates, and six loaded assemblies are enforced. |
| AC3 | Pre-resolved and marker-dependent late skips have distinct loading, evidence, manifest, and claim behavior. |
| AC4 | Every mutation-capable or skip-settled path has an exact operation manifest and every multi-target write follows source-first order. |
| AC5 | Partial, retry, stale, concurrent, lost-manifest, and insufficient-evidence-model outcomes fail closed as specified. |
| AC6 | Positioning, README, vision-skeleton, and positioning-skeleton actions are independently classified and authorized. |
| AC7 | Every current semantic rule and literal consumer receives one owner and disposition. |
| AC8 | Every new closed vocabulary rejects unknown values before consistency checks. |
| AC9 | All six procedural assemblies decrease while assets and total package size remain visible. |
| AC10 | Canonical-through-installed inventories and bytes match and acceptance executes no target-agent runtime or separate manual semantic-review gate. |

## Open questions

None. Exact manifest field names and fixture serialization may vary while preserving R43 through R57 and must be closed by the plan and test specification.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment.
- Reviewed execution plan and test specification after required upstream settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This artifact does not claim review approval, architecture completion, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
