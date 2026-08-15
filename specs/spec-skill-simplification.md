<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/spec/SKILL.md -->
<!-- Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Spec Skill Simplification

## Owning change record

`docs/changes/2026-08-15-spec-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Spec Skill Simplification](../docs/proposals/2026-08-15-spec-skill-simplification.md)
- Approved [proposal-review R3](../docs/changes/2026-08-15-spec-skill-simplification/reviews/proposal-review-r3.md)

## Goal and context

This specification defines a shorter published `spec` skill package without weakening behavioral-contract quality, customer-project portability, boundary-first adoption, governed lifecycle safety, structural consistency, compatibility, or `spec-review` handoff.

The universal skill remains sufficient for portable specification judgment. One conditional reference owns governed authoring and recovery procedure, the two existing boundary-first references retain their approved initial-loading contract, and the existing skeleton owns ordinary structure plus one conditional formal-boundary insertion point. Acceptance measures actual loaded profiles separately from total package size and excludes target-agent execution and an additional manual semantic-review gate.

## Glossary

- `governed signal`: an explicit change ID, workflow-managed change identity, or structured owning-change field, including an invalid field.
- `governed-signal classification`: exactly `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`.
- `portable operation`: spec creation or revision resolved from one exact artifact path and file state after `no-governed-signal` is established.
- `governed authority`: validated permission from the complete change record, lifecycle marker, exact spec identity or deterministic intended identity, settled inputs, and legal authoring state.
- `stale-authoring-attempt`: a diagnostic transaction result for an incomplete governed operation whose basis changed; it grants no restart authority.
- `restart-stale-authoring`: an explicitly authorized same-entry recovery operation owned by the governed spec procedure.
- `formal boundary block`: the contiguous `Boundary model`, `Boundary definitions`, `Selected interactions`, and `Example ownership` sections.
- `structural anchors`: the `Error and boundary behavior` and `Compatibility and migration` headings that surround the formal boundary insertion point.

## Examples first

### Example E1: ordinary portable creation

Given no governed signal exists and the exact spec target is absent, when portable creation runs, then the skill loads the common procedure and both approved boundary references, copies the skeleton, creates only the spec artifact, and writes no lifecycle state.

### Example E2: malformed ownership cannot become portable

Given an existing spec contains a malformed owning-change field, when revision is requested, then classification returns `invalid-or-ambiguous-governed-signal` and stops before portable or governed mutation.

### Example E3: multiple governed signals must agree

Given the invocation supplies an explicit change ID and the spec contains a structured owning-change field, when they resolve to different changes, then classification stops without loading mutation authority or falling back to portable revision.

### Example E4: governed candidate loading does not grant authority

Given one valid governed candidate selects the governed reference, when the complete change record does not grant legal spec-authoring authority, then the skill stops without mutation or portable fallback.

### Example E5: governed creation commits at review-required

Given one governed change authorizes a new primary spec, when authoring completes, then the skill creates only the matching entry, writes and validates the spec and evidence, and commits by moving that entry from `authoring` to `review-required`.

### Example E6: identical retry resumes once

Given an interrupted governed operation retains the same change, artifact, path, basis, prior identity when applicable, and retry identity, when retried, then it resumes or completes exactly once without duplicate evidence or transitions.

### Example E7: stale detection does not restart

Given an incomplete governed attempt has a changed basis, when the skill detects it, then it returns `stale-authoring-attempt`, performs no overwrite or pointer update, and waits for explicit current restart authority.

### Example E8: authorized restart preserves nonempty bytes

Given a current user request or same-change workflow handoff names the exact stale attempt and new basis and the matching partial file is nonempty, when restart runs, then it preserves the exact prior bytes and hash before replacing the canonical spec and leaves the entry in `authoring`.

### Example E9: unrelated partial content blocks restart

Given partial file identity cannot be tied to the stale attempt or contains competing changes, when restart validation runs, then it stops without snapshot adoption, replacement, or lifecycle mutation.

### Example E10: new behavior-changing spec emits the formal block

Given the active boundary contract requires formal adoption and the current skeleton is used, when the spec is authored, then the complete formal boundary block is inserted after `Error and boundary behavior` and before `Compatibility and migration`.

### Example E11: grandfathered adoption needs valid anchors

Given a grandfathered spec newly requires formal adoption, when both structural anchors exist exactly once and in order, then the complete block is inserted at the owned position; otherwise an explicitly authorized full rewrite is required or authoring stops.

### Example E12: existing boundary block is not removed implicitly

Given an existing complete formal block and a later non-behavioral or currently non-applicable edit, when no approved deactivation or supersession exists, then the block remains unchanged.

### Example E13: malformed boundary structure fails closed

Given a formal boundary block is incomplete, duplicated, or misplaced, when any revision is requested, then authoring stops for structural correction and does not insert another block ad hoc.

### Example E14: missing required resource fails safely

Given an initially required boundary reference, triggered governed reference, or required skeleton is missing or unreadable, when dependent work begins, then the skill stops and does not reconstruct procedure or layout from memory.

### Example E15: simplification reports relocation honestly

Given the package is revised, when measurements are recorded, then both loaded profiles, every procedural resource, the skeleton, representative output, and total package size are reported separately.

## Requirements

### Package and universal contract

R1. The canonical package MUST contain `skills/spec/SKILL.md`, `references/governed-spec-authoring.md`, `references/boundary-first-method-v1.md`, `references/boundary-first-feature-authoring-v1.md`, and `assets/spec-skeleton.md`.

R2. `SKILL.md` MUST remain self-sufficient for purpose, evidence use, observable behavior, requirements, examples, errors, compatibility, quality dimensions, stops, claims, portable isolation, handoff, governed-signal classification, and resource triggers.

R3. `SKILL.md` MUST initially load both boundary-first references for every invocation and MUST conditionally load the governed reference only for `single-governed-candidate`.

R4. `SKILL.md` MUST map references with `READ` and the skeleton with `COPY`, using repository-valid relative paths and exact load conditions.

R5. A missing, unreadable, escaped, contradictory, stale, or mixed-version required resource MUST stop dependent judgment or mutation before fallback reconstruction.

R6. The governed reference MUST own only governed proposal-settlement validation, spec creation, revision, retry, authorized same-entry restart, concurrency, authoring evidence, and legal authoring transitions.

R7. The boundary-first method reference MUST remain the owner of shared vocabulary, dimensions, identifiers, examples, interactions, stop rules, and structural-validation limits.

R8. The boundary-first feature-authoring reference MUST remain the owner of formal applicability, boundary definitions, selected interactions, example ownership, the four formal headings and tables, and semantic authoring procedure.

R9. The skeleton MUST own ordinary headings, ordering, placeholders, and one conditional insertion position but MUST NOT own lifecycle policy, semantic adequacy, applicability, status, or handoff.

### Governed-signal and operation classification

R10. Governed-signal classification MUST use exactly `no-governed-signal`, `single-governed-candidate`, and `invalid-or-ambiguous-governed-signal`.

R11. Any explicit change ID, workflow-managed change identity, or structured owning-change field MUST count as a governed signal even when malformed.

R12. Conversational references to a workflow, proposal, or change MUST NOT establish a governed signal.

R13. `no-governed-signal` MUST require the absence of every governed signal and MUST be the only classification that permits portable authoring.

R14. `single-governed-candidate` MUST require every present signal to parse safely and resolve to the same exact change.

R15. A malformed, stale, duplicated, escaped, unsafe, missing-root, mismatched, or conflicting signal MUST produce `invalid-or-ambiguous-governed-signal` and MUST stop without portable fallback.

R16. The loaded procedural profiles MUST be exactly `SA0-portable` for `no-governed-signal` and `SA1-governed` for `single-governed-candidate`; invalid or ambiguous signal state is a stop result rather than a profile.

R17. The artifact operations MUST be exactly `create-primary-spec` and `revise-primary-spec`; stale detection and restart are transaction results or recovery operations rather than additional artifact operations.

R18. Portable creation MUST require an absent exact target, portable revision MUST require an existing exact target, and ambiguous, conflicting, or unresolved target state MUST stop.

R19. Portable authoring MUST write only the spec artifact and MUST NOT create or mutate lifecycle, review, automation, or routing state.

R20. A governed candidate MUST load the governed reference before complete authority validation, and failed validation MUST stop without reclassification as portable.

### Governed creation, revision, and identical retry

R21. Governed authority MUST validate the complete current change record, `lifecycle_contract: stage-owned-change-local-v1`, exact spec entry or deterministic intended path, settled governing inputs, accepted proposal settlement when applicable, and legal spec-authoring state.

R22. Governed creation MUST bind the change ID, artifact ID, normalized intended path, governing input identities, authoring-evidence path, and retry identity before writing.

R23. Governed creation MUST prove that the target entry and file are absent and no competing primary spec exists before creating only the matching entry in `authoring`.

R24. Governed creation MUST validate the complete spec, compute and record its content identity, and use the matching transition to `review-required` as its commit point.

R25. Governed revision MUST additionally bind the prior spec identity and exact reopen, review finding, upstream input change, or legal revision authority.

R26. Governed revision MUST preserve historical authoring and review evidence, clear only the matching current review mapping when authorized, produce a new content identity, return only the matching entry to `review-required`, and require fresh `spec-review`.

R27. A settled spec with downstream reliance MUST NOT be revised until workflow completes impact and staleness handling and establishes legal reopen or revision authority.

R28. An identical interrupted creation or revision MUST resume from the first incomplete step, and an identical completed retry MUST return idempotent success without duplicate evidence or transitions.

R29. Mismatched basis, unrelated file or entry asymmetry, different path, stale authority, ambiguous attempts, multiple primary candidates, or concurrent competing writes MUST stop without adoption or overwrite.

### Stale detection and authorized same-entry restart

R30. An incomplete governed attempt whose governing input basis changes MUST return `stale-authoring-attempt` and stop without overwriting content, rebinding identity, updating evidence pointers, or starting another operation.

R31. `restart-stale-authoring` MUST be a separate governed spec operation over the same incomplete entry and MUST NOT be inferred from stale detection or routing alone.

R32. Restart authority MUST be either an explicit current user instruction or a current same-change workflow handoff that names the exact stale attempt and new governing basis.

R33. Restart MUST validate the exact `authoring` entry, artifact ID, kind, role, normalized path, old retry identity and governing inputs, new governing inputs, current authority, absence of review and downstream reliance, absence of competition, and attributable partial-file state.

R34. The new authoring evidence MUST record the restart authority source and request identity, old retry identity and governing inputs, new retry identity and governing inputs, and partial-content state and identity.

R35. An absent partial file MUST be recorded as `absent` without a snapshot, and a matching zero-byte file MUST be recorded as `empty` with its identity.

R36. Every matching nonempty partial file MUST be preserved byte-for-byte with a hash at a distinct change-local evidence path before replacement.

R37. Unknown, unrelated, conflicting, unattributable, or unpreservable partial content MUST stop restart without mutation.

R38. Restart MAY write only the same canonical spec file, a new authoring-evidence record, the matching entry's `authoring_evidence` pointer, and the immutable snapshot required for matching nonempty prior bytes.

R39. Restart MUST preserve the entry ID, kind, role, normalized path, and `authoring` state and MUST NOT change review mappings, another artifact entry, workflow state, automation state, or downstream artifacts.

R40. Restart MUST preserve completed authoring and review evidence and MUST leave the matching entry in `authoring` for the ordinary governed transaction to complete.

R41. A matching already-completed authoring operation at `review-required` MUST return idempotent success rather than restart.

R42. Restart MUST use the existing artifact-entry and authoring-evidence model; any required schema, lifecycle state, persistent authorization subsystem, cross-stage mutation, or new write owner MUST stop and route to architecture and workflow-contract revision.

### Structural composition and boundary transitions

R43. The skeleton MUST contain exactly one conditional formal-boundary insertion position after `## Error and boundary behavior` and before `## Compatibility and migration`.

R44. The formal boundary block MUST contain exactly these contiguous headings in order: `## Boundary model`, `## Boundary definitions`, `## Selected interactions`, and `## Example ownership`.

R45. Boundary-reference loading and formal-block emission MUST be classified independently.

R46. Boundary-block state MUST be exactly `absent`, `present-complete`, `present-incomplete`, `present-duplicated`, or `present-misplaced`.

R47. Structural-anchor state MUST be exactly `unique-ordered`, `missing`, `duplicated`, or `misordered`.

R48. A required absent block in a new current-skeleton spec or a spec with `unique-ordered` anchors MUST be inserted completely at the owned position.

R49. A grandfathered spec requiring adoption without `unique-ordered` anchors MUST use an explicitly authorized full rewrite through the current skeleton that preserves stable requirement IDs and semantic content, or MUST stop.

R50. A `present-complete` required block MUST be preserved with stable boundary IDs and MUST be updated in place only when the authorized revision changes governed boundary semantics.

R51. An absent non-applicable block MUST remain omitted.

R52. A `present-complete` non-applicable block MUST remain unchanged unless explicit approved deactivation or supersession authority includes downstream-impact handling and required historical and stable-ID traceability.

R53. A `present-incomplete`, `present-duplicated`, or `present-misplaced` block MUST stop any revision until structural correction is explicitly authorized and MUST NOT be repaired by ad hoc insertion.

R54. Unresolved block applicability MUST stop authoring or readiness.

R55. A non-behavioral revision MUST NOT implicitly remove, relocate, or rewrite an existing complete formal block.

R56. `spec-review` MUST retain final authority to classify whether a changed grandfathered spec is substantively normative under the existing boundary-first contract.

### Preservation, measurement, and acceptance

R57. Every behaviorally significant current rule or duplicate cluster MUST receive exactly one disposition and destination in `spec-rule-disposition.yaml`.

R58. The semantic-rule disposition vocabulary MUST be exactly `retained-inline`, `retained-governed-reference`, `retained-boundary-reference`, `asset-owned`, `removed-duplicate`, and `removed-obsolete-with-approved-contract-change`.

R59. Every exact heading, label, path, enum, resource command, or phrase consumed by contracts, parsers, packages, fixtures, or tests MUST receive one separate classification and disposition in `spec-literal-compatibility.yaml`.

R60. The literal classification vocabulary MUST be exactly `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `historical-fixture`, and `obsolete`.

R61. Normative literals MUST remain exact unless their governing contract changes, parser or package contracts MUST migrate atomically with every consumer, and incidental tests MUST NOT freeze accidental prose.

R62. Every new or changed closed vocabulary MUST fail explicitly on unknown values before consistency checks and MUST have an unknown-value regression test.

R63. Measurements MUST use canonical authored files, LF normalization, each unique loaded procedure once in documented order, UTF-8 bytes, and Unicode whitespace-separated words.

R64. Measurements MUST report `SA0-portable`, `SA1-governed`, `SKILL.md`, each reference, the skeleton, representative copied output, and total package size separately.

R65. Both loaded profiles MUST decrease from the recorded 3,020-word and 21,523-byte baseline; a smaller main file alone is insufficient, and no fixed percentage may override semantic or lifecycle preservation.

R66. Canonical, generated, packed, archived, release-candidate, and installed resources MUST retain required relative-path inventory and raw-byte parity.

R67. Acceptance MUST use deterministic contract, fixture, validator, and package proof plus ordinary lifecycle and PR review; it MUST NOT execute Codex, Claude Code, opencode, or another target-agent runtime or add another manual semantic-review stage.

## Inputs and outputs

Inputs are the accepted proposal and approved review, the current canonical `spec` package, existing boundary-first resources and loading profile, governing skill and workflow contracts, exact literal and validator consumers, package inventories, and one governed change record when lifecycle authoring applies.

Outputs are the simplified canonical skill, one governed reference, revised skeleton, directly coupled contract fixtures and validator registrations, semantic-rule and literal-compatibility ledgers, deterministic profile measurements, package parity evidence, and stage-owned lifecycle evidence. Target-agent transcripts, runtime scores, external mutations, and another manual semantic-review artifact are not outputs.

## State and invariants

- `skills/` remains the only authored skill source.
- Both boundary-first references retain their approved initial-loading contract and semantic ownership.
- Portable authoring writes no lifecycle state.
- Governed authoring changes only its spec artifact, matching spec entry, and spec-authored evidence under exact authority.
- Stale detection writes nothing, and restart requires separate current authority.
- Workflow may route or explicitly hand off restart but never mutates spec-owned state.
- `spec-review` remains the only spec settlement owner and final grandfathered substantive-revision classifier.
- The skeleton remains structural, references remain subordinate skill-owned procedure, and formal boundary IDs remain stable unless explicitly superseded.
- Every completed creation or revision ends at `review-required`; restart itself leaves the entry in `authoring`.

## Error and boundary behavior

Every unknown closed-vocabulary value, invalid governed signal, unresolved target, illegal state, missing authority, stale identity, unrelated collision, mismatched retry, absent restart authority, unknown partial content, unpreservable bytes, downstream reliance, competing write, malformed formal block, unresolved applicability, and required-resource defect fails closed with a concrete blocker. Failure before a permitted write leaves governed state unchanged. An interrupted permitted write may be reconciled only through its exact retry identity or explicitly authorized same-entry restart.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66, R67

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R10, R11, R12, R13, R14, R15, R16, R17, R18 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55 | BND-STATE-001 | - |
| identity-authority | applicable | R10, R11, R12, R13, R14, R15, R20, R21, R22, R25, R27, R30, R31, R32, R33, R34, R38, R39, R40, R41, R42, R49, R52, R56 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R6, R7, R8, R9, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R5, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R49, R53, R54 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66 | BND-COMPAT-001 | - |
| external-environment | applicable | R5, R36, R37, R38, R42, R66, R67 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R10, R11, R12, R13, R14, R15, R16, R17, R18 | no signal, one candidate, invalid or ambiguous signal; create or revise; exact or unresolved target | only no signal permits portable authoring | valid classification selects one profile; every invalid or ambiguous signal stops | R10 |
| BND-STATE-001 | state-lifecycle | R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55 | absent, `authoring`, `review-required`, settled, stale, or conflicting entry and file state; identical retry, stale detection, authorized restart, completed operation, or unsafe state; absent, complete, incomplete, duplicated, or misplaced formal block | only the exact spec entry changes, stale detection is write-free, restart leaves `authoring`, and the formal block remains contiguous and complete | legal authoring commits at `review-required`; exact retry or authorized restart reconciles; valid block adoption, preservation, or deactivation proceeds; every illegal or unresolved state stops | R21 |
| BND-AUTH-001 | identity-authority | R10, R11, R12, R13, R14, R15, R20, R21, R22, R25, R27, R30, R31, R32, R33, R34, R38, R39, R40, R41, R42, R49, R52, R56 | no signal, one matching candidate, conflicting candidate, full or failed authoring authority, current or stale restart authority, deactivation authority, full-rewrite authority | classification and reference loading never grant mutation authority, and every destructive or structural transition has current explicit authority | exact authority permits only the named bounded action; every missing, conflicting, or stale authority stops without fallback | R10 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R6, R7, R8, R9, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56 | main file, governed reference, two boundary references, skeleton, ordinary structure plus omitted, inserted, preserved, updated, deactivated, or malformed formal block | each rule and structure has one owner, and the skeleton owns position while the feature reference owns block content | a complete package and valid structure proceed; missing, contradictory, or malformed composition stops | R1 |
| BND-TEMPORAL-001 | temporal-retry | R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41 | first attempt, identical retry, completed retry, stale attempt, authorized restart, concurrent attempt | retry identity never silently rebinds | identical work resumes or no-ops; explicitly authorized restart creates a new retry identity; competition stops | R28 |
| BND-RECOVERY-001 | failure-recovery | R5, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R49, R53, R54 | absent, empty, matching nonempty, unknown, unpreservable, unrelated, or competing partial file; required resource present or unavailable; valid anchors or full rewrite; malformed block; unresolved applicability | matching nonempty bytes are preserved before replacement, and no missing procedure or malformed structure is reconstructed ad hoc | safe content and dependencies reconcile within bounded writes; every unsafe dependency or content state stops unchanged | R35 |
| BND-COMPAT-001 | compatibility-migration | R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66 | new current skeleton, grandfathered document, existing complete block, approved deactivation or supersession, semantic rule, normative literal, parser contract, incidental test, historical fixture, obsolete literal, canonical or derived resource | historical acceptance and stable IDs remain traceable, while semantics and literal compatibility remain separate | adopt or preserve structures safely, migrate true contracts atomically, retire incidental coupling, and stop on parity defects | R49 |
| BND-ENV-001 | external-environment | R5, R36, R37, R38, R42, R66, R67 | writable evidence path, preservation failure, canonical, generated, archived, release-candidate, installed, and unavailable package surfaces | acceptance remains deterministic, repository-owned, and non-runtime | exact bytes and package parity pass or block; no target runtime or external mutation occurs | R36 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R10, R11, R12, R13, R14, R15 | BND-INPUT-001, BND-AUTH-001 | malformed or conflicting ownership is treated as absence and portable revision overwrites a governed artifact | every structured signal participates in tri-state classification and no invalid signal or failed authority can fall back to portable mutation |
| INT-002 | R30, R31, R32, R33, R34, R38, R39, R40, R41 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001 | stale detection is mistaken for destructive authority or matching user bytes are discarded | detection stops; explicit current authority is recorded; nonempty matching bytes are preserved; only bounded same-entry writes occur |
| INT-003 | R49, R52 | BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001 | a grandfathered or non-behavioral edit removes, duplicates, or inserts the formal block at an ad hoc location | valid anchors or an authorized full rewrite govern adoption; existing blocks persist absent approved deactivation; malformed structure stops |
| INT-004 | R66 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | simplification appears successful while dropping behavior, hiding package growth, or omitting a required resource | rule and literal ledgers, both loaded-profile reductions, deterministic fixtures, and full package parity all remain required |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R13, R16, R18 | BND-INPUT-001 | - | - |
| E2 | regression | R10, R11, R13, R15 | BND-INPUT-001, BND-AUTH-001 | SPSIM-R2-PR1 | - |
| E3 | illustration | R11, R14, R15 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E4 | illustration | R20, R21 | BND-AUTH-001 | - | - |
| E5 | illustration | R22 | BND-STATE-001, BND-AUTH-001 | - | - |
| E6 | illustration | R28, R29 | BND-TEMPORAL-001 | - | - |
| E7 | regression | R30, R31, R32 | BND-STATE-001, BND-AUTH-001 | SPSIM-R2-PR2 | - |
| E8 | regression | R32, R33, R34, R38, R39, R40 | BND-AUTH-001, BND-RECOVERY-001 | SPSIM-R2-PR2 | - |
| E9 | illustration | R33, R37 | BND-RECOVERY-001 | - | - |
| E10 | illustration | R43, R44, R45, R48 | BND-STATE-001, BND-COMPOSE-001 | - | - |
| E11 | regression | R49 | BND-AUTH-001, BND-COMPAT-001 | SPSIM-R2-PR3 | - |
| E12 | regression | R50, R51, R52, R55 | BND-STATE-001, BND-COMPAT-001 | SPSIM-R2-PR3 | - |
| E13 | illustration | R53, R54 | BND-STATE-001, BND-RECOVERY-001 | - | - |
| E14 | illustration | R5 | BND-COMPOSE-001, BND-RECOVERY-001 | - | - |
| E15 | illustration | R66 | BND-COMPAT-001, BND-ENV-001 | - | - |

## Compatibility and migration

Historical specs and review evidence remain unchanged and readable. New behavior-changing specs use the revised skeleton and formal insertion point. Grandfathered specs remain valid under the active boundary contract; substantive adoption uses bounded insertion only with unique ordered anchors or an explicitly authorized full rewrite. Existing complete formal blocks remain unless an approved deactivation or supersession addresses downstream reliance and stable-ID traceability.

Exact parser, fixture, and package consumers migrate atomically according to the literal ledger. Canonical and every derived package layer adopt the new governed reference and revised skeleton together. Rollback removes the governed reference, restores governed procedure to `SKILL.md`, restores the prior skeleton and validator expectations, and regenerates derived packages without rewriting historical specs.

## Observability

The change is observable through canonical diffs, resource maps, rule and literal ledgers, static scenario results, validator output, loaded-profile and total-package reports, package parity evidence, review records, and lifecycle metadata. Reports distinguish configured commands from executed commands and relocated content from deleted content.

## Security and privacy

The change introduces no credentials, secrets, network operation, external persistence, or personal-data processing. Existing destructive-action, publication, and external-state boundaries remain mandatory. Restart cannot adopt unrelated content, and acceptance cannot execute a target-agent runtime.

## Accessibility and UX

Not applicable to end-user interface accessibility. Published Markdown must remain readable: complete prose sentences stay intact, repeated mappings use tables, and copied structures contain no unfilled placeholders.

## Performance expectations

Both real loaded procedural profiles must use fewer LF-normalized UTF-8 bytes and Unicode whitespace-separated words than the recorded baseline. Total package size is reported separately, no fixed percentage overrides preservation, and no runtime latency contract is introduced.

## Edge cases

EC1. A request mentions a change conversationally but supplies no structured signal: remain portable when portable prerequisites are otherwise valid.

EC2. A structured owning-change field exists but cannot be parsed: stop as `invalid-or-ambiguous-governed-signal`.

EC3. Multiple valid signals resolve to the same exact change: classify one governed candidate and validate authority once.

EC4. Multiple signals resolve to different changes: stop without selecting either change.

EC5. A governed candidate's change root disappears after classification: authority validation stops without portable fallback.

EC6. Stale detection occurs without an explicit restart request: report the stale attempt and make no write.

EC7. A matching partial file is zero bytes: record `empty` and its identity without a separate byte copy.

EC8. A matching partial file is nonempty but the snapshot path is unavailable: stop before replacement.

EC9. Restart authority names a different stale retry identity or basis: stop.

EC10. The matching entry reaches `review-required` before restart: return idempotent completed success and do not restart.

EC11. A grandfathered spec has only one insertion anchor: require an authorized full rewrite or stop.

EC12. A complete formal block exists during a formatting-only edit: preserve it unchanged.

EC13. Explicit deactivation exists but downstream-impact handling is absent: preserve the block and stop removal.

EC14. The skeleton is available but one always-loaded boundary reference is missing: stop before creating a partial spec.

EC15. A new closed-value validator receives an unknown value: report an explicit vocabulary error before consistency checks.

## Non-goals

- Changing `boundary-first-v1`, its resource identities, feature-record shape, capability activation, grandfathering authority, or approved initial-loading profile.
- Reducing specification rigor, removing stable requirement IDs, or allowing examples to become normative owners.
- Changing `spec-review`, workflow routing, architecture assessment, planning, implementation, verification, or PR authority.
- Adding a runtime engine, schema compiler, target-agent evaluator, tokenizer dependency, permanent simplicity gate, or separate manual semantic-review acceptance stage.
- Rewriting historical specs merely to adopt the new skeleton.
- Adding another structural asset or fragmenting universal quality guidance into optional references.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | The final canonical package contains one main file, one governed reference, both existing boundary references, and one revised skeleton. |
| AC2 | Only `no-governed-signal` permits portable authoring, and every invalid or conflicting signal fails closed. |
| AC3 | Governed reference loading and complete mutation authority remain separate decisions. |
| AC4 | Portable create and revise, governed create and revise, identical retry, stale detection, and authorized restart have closed results and write boundaries. |
| AC5 | Restart requires explicit current authority and preserves every matching nonempty partial file before replacement. |
| AC6 | Restart uses the existing entry and authoring-evidence model and leaves the entry in `authoring`. |
| AC7 | The skeleton owns one insertion point and the feature-authoring reference owns the complete formal block. |
| AC8 | Block state, applicability, anchor state, adoption, preservation, deactivation, malformed structure, and unresolved state each have deterministic outcomes. |
| AC9 | `spec-review` retains final grandfathered substantive-revision classification authority. |
| AC10 | Every semantic rule and exact literal dependency has one classified disposition. |
| AC11 | Unknown closed-vocabulary values fail explicitly before consistency checks. |
| AC12 | Both loaded profiles shrink from baseline and total package size remains separately visible. |
| AC13 | Canonical through installed resource inventories and bytes retain required parity. |
| AC14 | Acceptance uses deterministic proof and ordinary lifecycle review without target-agent execution or another manual semantic-review stage. |

## Open questions

None at contract level. The execution plan may select exact authoring-evidence field names and fixture filenames while preserving every required semantic field, identity, stop, write boundary, and proof obligation defined here.

## Next artifacts

- Bounded architecture assessment.
- Execution plan after architecture applicability is settled.
- Test specification after an approved plan.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This specification does not claim review approval, architecture disposition, planning readiness, implementation readiness, verification, branch readiness, or PR readiness.
