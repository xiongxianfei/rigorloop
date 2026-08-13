# Plan-Review Skill Simplification Specification

## Owning change record

`docs/changes/2026-08-13-plan-review-skill-simplification/change.yaml`

## Related proposal

`docs/proposals/2026-08-13-plan-review-skill-simplification.md`

## Goal and context

The `plan-review` package must reduce the procedural context loaded for portable and governed review while preserving plan-quality judgment, formal recording, reviewed-plan initialization and settlement, boundary-first behavior, automation limits, lifecycle ownership, and truthful claims. The package will keep universal review and recording policy in `SKILL.md`, place exact governed plan-entry transaction procedure in one conditional reference, retain the existing boundary reference, and use two structural assets for results and material findings.

## Glossary

| Term | Meaning |
| --- | --- |
| Portable review | A formal plan review without a governed change candidate; it records evidence but cannot settle a governed plan entry. |
| Governed candidate | Evidence identifying a possible governed change and plan entry; it triggers reference loading but grants no authority. |
| Validated governed entry | One exact current change and plan entry that passes the governed reference's identity, lifecycle, and operation checks. |
| Initial review | Semantic plan judgment for an exact reviewable plan tuple when no current clean review exists. |
| Settlement retry | A later invocation for an exact plan tuple that already has one current clean review; it reuses judgment and never performs semantic rereview. |
| Plan tuple | Stable artifact identity plus reviewed revision identity: artifact ID, kind `plan`, role `primary`, normalized path, review ID, round, review record path, reviewed artifact path, and reviewed repository revision or commit. |
| Transaction result | The lifecycle or recording result of an invocation, distinct from semantic review status. |
| Basis evidence | Authoring, clean review, and plan-owned initialization evidence bound to the reviewed plan transaction. |

## Examples first

Example E1: portable review avoids governed procedure
Given a formal plan review with no governed candidate and no boundary trigger
When the review package is assembled
Then only `SKILL.md` and applicable structural output resources are used, full plan judgment and recording remain possible, and no governed settlement is claimed.

Example E2: governed candidate fails validation
Given explicit change metadata identifies a governed candidate
When the governed reference finds a stale or mismatched plan entry
Then the invocation stops without governed mutation or portable fallback.

Example E3: clean initial review waits for initialization
Given a validated governed plan entry is `review-required`, `planned_work` is absent, and no exact current clean review exists
When plan review approves the plan and records its clean receipt
Then review status is `approved`, the entry remains `review-required`, transaction result is `initialization-required`, and test-spec eligibility is withheld.

Example E4: repeated invocation before initialization
Given one exact current clean review exists and `planned_work` remains absent
When plan review is invoked again for the same plan tuple
Then the operation is `settlement-retry`, the prior judgment is reused, transaction result remains `initialization-required`, and no review evidence is duplicated.

Example E5: matching settlement activates the entry
Given one exact clean review and matching plan-owned initialization basis exist for a `review-required` entry
When settlement retry runs
Then only that entry is compare-and-set to `active`, transaction result is `settled-active`, basis evidence is retained, and formal test-spec eligibility is reported.

Example E6: already-active retry is idempotent
Given the exact matching entry is already `active`
When the same settlement retry is repeated
Then transaction result is `settled-active`, `state_changed` is false, and no review, resolution, log, receipt, transition, or other evidence is duplicated.

Example E7: invalid retry has no semantic verdict
Given a retry has multiple matching review records or mismatched initialization evidence
When the transaction is evaluated
Then transaction result is `blocked`, the exact blocker is reported, and the judgment group is omitted unless one exact prior judgment was safely resolved.

Example E8: non-clean initial review has deterministic effects
Given a governed initial review produces `changes-requested`, `blocked`, or `inconclusive`
When recording succeeds
Then the matching entry and transaction result follow the status-specific mapping and no clean-review initialization path is claimed.

Example E9: required resource is unavailable
Given a governed or boundary trigger is true
When the required mapped resource is missing, unreadable, contradictory, or mixed-version
Then dependent interpretation and mutation stop without reconstructing procedure from memory.

Example E10: size reduction cannot hide semantic loss
Given `SKILL.md` becomes shorter
When simplification acceptance is evaluated
Then acceptance still fails unless portable and governed loaded profiles decrease, every significant rule and literal is dispositioned, duplicate clusters have one owner, lifecycle scenarios pass, and semantic review approves the package.

## Requirements

R1. The canonical published package MUST remain owned by `skills/plan-review/` and MUST contain `SKILL.md`, `references/governed-plan-review-settlement.md`, `references/boundary-first-method-v1.md`, `assets/review-result-skeleton.md`, and `assets/material-finding.md`.

R2. `SKILL.md` MUST remain self-sufficient for portable formal plan judgment, recording obligations, status selection, safe output, stops, claims, and isolated routing without the governed reference.

R3. Every explicit `plan-review` invocation MUST be formal and MUST create required durable review evidence or report blocked recording.

R4. Operation MUST be exactly `initial-review` or `settlement-retry` and MUST be selected from complete current transaction state before semantic judgment or writes.

R5. `initial-review` MUST require a reviewable current plan revision, a matching `review-required` entry when governed, current required authoring evidence, absent `planned_work`, and no current clean review for the exact plan tuple.

R6. `initial-review` MUST perform semantic plan judgment and create exactly one new review occurrence.

R7. Once one exact current clean review exists for the plan tuple, every later same-tuple invocation MUST be `settlement-retry`, including when `planned_work` remains absent.

R8. A settlement retry MUST reuse the existing judgment and record and MUST NOT perform semantic rereview or create another receipt, finding set, resolution entry, review-log entry, review ID, or review round.

R9. A changed plan identity MUST make the prior judgment stale and MUST require a fresh initial review.

R10. Multiple matching clean reviews, multiple initialization bases, an open review resolution, `planned_work` without one valid current clean review, mismatched initialization basis, or contradictory transaction evidence MUST block before mutation.

R11. `governed_plan_candidate_context` MUST be a load-only predicate established by explicit change identity, reviewed-plan metadata, current workflow-managed plan-review evidence, or an identical retry request.

R12. A governed candidate MUST load the governed reference but MUST NOT establish a valid entry, legal state, settlement authority, automation authority, or continuation authority.

R13. The governed reference MUST classify exactly `validated-governed-plan-entry` or `invalid-governed-candidate`; invalid candidates MUST stop without governed mutation or portable fallback.

R14. Validated governed context MUST resolve one exact current change, lifecycle marker, plan entry, legal plan state, stable artifact identity, and reviewed revision identity; stable artifact identity MUST be artifact ID, kind `plan`, role `primary`, and normalized path, reviewed revision identity MUST be review ID, round, record path, reviewed artifact path, and reviewed repository revision or commit, and the change MUST NOT add a governed-document hash or `content_identity` field.

R15. Governed initial review MUST additionally require complete current authoring evidence, while retry MUST additionally require one exact current clean review; initialization evidence MUST then be classified as absent, matching, or invalid.

R16. Settlement mode MUST be exactly `isolated-recording` or `governed-plan-entry`, and execution mode MUST be exactly `manual` or `workflow-managed`.

R17. Loading a resource, detecting a candidate, or using workflow wording MUST NOT grant settlement, mutation, automation, or continuation authority.

R18. Review status MUST remain exactly `approved`, `changes-requested`, `blocked`, or `inconclusive` and MUST describe semantic plan judgment only.

R19. Transaction result MUST remain exactly `recorded-isolated`, `initialization-required`, `revision-required`, `blocked`, `settled-active`, or `not-settled` and MUST remain separate from semantic review status.

R20. A portable clean initial review MUST record one clean receipt and log entry, return `recorded-isolated`, and report `test-spec` only as a possible next stage without formal eligibility.

R21. A governed clean initial review with absent `planned_work` MUST record the exact clean review mapping, leave the entry `review-required`, return `initialization-required`, and withhold formal test-spec eligibility.

R22. A governed `changes-requested` result MUST create detailed review and resolution evidence, map the entry to `revision-required`, and return transaction result `revision-required`.

R23. A governed `blocked` result MUST create detailed review and resolution evidence before settlement and MUST map the entry and transaction result to `blocked` only after recording succeeds.

R24. A governed `inconclusive` result MUST be recorded when possible, MUST leave the entry `review-required`, and MUST return transaction result `blocked` with reason `review-inconclusive`.

R25. Blocked required recording MAY expose the review judgment but MUST leave the entry unchanged, return `not-settled`, report blocked paths and the smallest corrective action, and MUST NOT claim formal completion or eligibility.

R26. A settlement retry with absent `planned_work` MUST reuse the prior approved judgment, leave the entry `review-required`, return `initialization-required`, and create no new review evidence.

R27. A settlement retry with matching initialization and a `review-required` entry MUST compare-and-set only that exact entry to `active`, return `settled-active`, and report formal test-spec eligibility.

R28. A settlement retry with matching initialization and an already `active` entry MUST return idempotent `settled-active` with `state_changed: false` and MUST perform no durable write or duplicate evidence.

R29. Invalid, stale, ambiguous, conflicting, or unsupported retry state MUST leave lifecycle state unchanged, return `blocked`, report the exact blocker, and route correction to the owning stage.

R30. The governed settlement sequence MUST read the complete current change record, validate exact plan, clean-review, repository-revision, initialization, entry-state, and resolution identities, reject conflicts before mutation, perform at most one exact compare-and-set transition, preserve basis evidence, validate the resulting record, and report the result.

R31. Authoring, review, and initialization evidence MUST remain durable historical evidence after settlement and MUST NOT be optionally or mandatorily deleted by this change.

R32. A failure before compare-and-set MUST leave state unchanged; interruption after compare-and-set MUST reconcile from the exact active entry and matching identities without semantic rereview or duplicate evidence.

R33. The package MUST use exactly four procedural profiles: `PRV0-portable`, `PRV0B-portable-boundary`, `PRV1-governed`, and `PRV1B-governed-boundary`.

R34. `PRV0-portable` MUST load only `SKILL.md`; `PRV0B-portable-boundary` MUST add only the boundary reference; `PRV1-governed` MUST add only the governed reference; and `PRV1B-governed-boundary` MUST add both references once in documented order.

R35. Late candidate or boundary discovery MUST load and validate the required reference before dependent interpretation, recording-location selection, status, write, or handoff claim.

R36. A missing, unreadable, escaped, contradictory, or mixed-version required resource MUST stop dependent work; an untriggered resource MUST not load or block, and memory-based reconstruction MUST be forbidden.

R37. `SKILL.md` MUST retain purpose, trigger, near-miss routing, evidence precedence, operation and authority classifications, plan-quality dimensions, materiality, severity, status and transaction meanings, concise formal recording, isolation, universal stops, claims, handoff boundaries, resource triggers, and result applicability.

R38. The governed reference MUST own complete change-record inspection, candidate validation, exact entry and identity resolution, operation-state validation, initial-review mapping, retry comparison and settlement, concurrency and interruption handling, workflow-managed review procedure, and fail-closed governed diagnostics.

R39. The governed reference MUST NOT own plan-quality judgment, finding materiality, universal recording requirements, plan edits, `planned_work` initialization or mutation, workflow routing, automation target state, test-spec authoring, or implementation authorization.

R40. The existing boundary-first trigger and `boundary-first-method-v1.md` MUST retain their existing version, identifier grammar, byte-parity obligations, activation meaning, and ownership.

R41. Boundary procedure MUST load only when cited approved boundary or interaction evidence is missing, stale, unknown, ambiguous, conflicting, or insufficient for plan review.

R42. The result asset MUST contain a universal core-operation group, a semantic-judgment group, a durable-recording group, a governed-settlement group, a boundary-review group, and a workflow-managed group.

R43. The core-operation and durable-recording groups MUST appear for every formal invocation; semantic judgment MUST appear only when judgment was performed or one exact prior judgment was safely reused; other inapplicable groups MUST be omitted.

R44. An invalid retry MUST report operation, blocked transaction result, exact blocker, no new evidence, and MUST omit the judgment group unless one exact prior judgment was safely resolved.

R45. Applicable groups with unavailable data MUST report explicit `blocked` or `unknown` state and the blocker; unfilled placeholders MUST be forbidden.

R46. Assets MUST own only headings, labels, order, tables, placeholders, and fill hints and MUST NOT decide applicability, status, severity, settlement, authority, automation, or handoff.

R47. `assets/material-finding.md` MUST preserve the byte-identical parser-owned review-family finding block, and existing review-family validation MUST be extended rather than creating a new validator family.

R48. A change-local semantic rule-disposition ledger MUST give every significant current rule a stable identity, source locations, behavior, governing requirements, applicable profiles, one closed disposition, destination, and preservation proof.

R49. Semantic dispositions MUST be exactly `retained-inline`, `retained-governed-reference`, `retained-boundary-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; unknown or missing values MUST fail closed before consistency checks.

R50. A separate literal-compatibility inventory MUST record each exact dependency, source, consumers, required semantics, classification, disposition, and replacement; classifications MUST be exactly `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `obsolete`, or `historical-fixture`.

R51. Profile measurement MUST use LF-normalized canonical files, count each unique procedural resource once in documented order, and report UTF-8 bytes and Unicode whitespace-separated words for each resource, all four procedural profiles, both assets, and the total package.

R52. Acceptance MUST require lower loaded words and bytes for both `PRV0-portable` and `PRV1-governed`, one loaded owner per duplicate cluster, complete rule and literal disposition, no unexplained profile growth, honest total-package accounting, and preserved semantic and lifecycle behavior; no fixed percentage may override safety or preservation.

R53. Acceptance MUST use deterministic structural checks, static contract scenarios, existing package-chain validation, and independent semantic review and MUST NOT execute a target-agent runtime, grade transcripts, add prompt journeys, add a tokenizer dependency, or create a permanent simplicity validator family.

R54. Canonical, generated, packed, archived, and clean-installed resources MUST retain required inventory, path, and byte parity, and rollout or rollback MUST update the complete package and directly coupled consumers atomically.

R55. A bounded architecture assessment MUST precede planning and MUST select `architecture-not-required` when the existing packaged-skill and state-ownership model remains accurate; if the change alters that model, the same change MUST own the required architecture update and review before planning.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R4, R11, R13, R16, R18, R19 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R4, R5, R7, R9, R10, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-STATE-001 | - |
| identity-authority | applicable | R5, R7, R8, R10, R11, R12, R13, R14, R15, R16, R17, R27, R28, R29, R30, R39 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R12, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R4, R5, R6, R7, R8, R9, R10, R26, R27, R28, R29, R30, R31, R32 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R10, R13, R24, R25, R29, R30, R32, R35, R36, R44, R45, R49, R50, R52, R53, R54, R55 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R18, R19, R31, R40, R47, R48, R49, R50, R51, R52, R53, R54, R55 | BND-COMPAT-001 | - |
| external-environment | applicable | R36, R51, R53, R54 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R4, R11, R13, R16, R18, R19 | initial or retry; candidate or portable; isolated or governed; manual or managed; known or unknown vocabulary | every invocation resolves one supported classification before dependent work | valid profile and operation or fail-closed stop | R4 |
| BND-STATE-001 | state-lifecycle | R4, R5, R7, R9, R10, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | no review, clean review, absent/matching/invalid initialization, review-required, revision-required, blocked, active, interrupted | judgment precedes initialization and settlement; only exact retry activates | recorded-isolated, initialization-required, revision-required, blocked, settled-active, or not-settled | R19 |
| BND-AUTH-001 | identity-authority | R5, R7, R8, R10, R11, R12, R13, R14, R15, R16, R17, R27, R28, R29, R30, R39 | portable, candidate, validated entry, invalid candidate, workflow-managed authorization | candidate and resources never grant authority; exact identities bind every write | bounded exact-entry mutation or authority blocker | R17 |
| BND-COMPOSE-001 | composition-path | R1, R2, R12, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47 | four procedural profiles, two references, two assets, canonical and derived packages | one owner per rule and structure; resources load once; portable review stays executable | exact assembly, safe missing-resource stop, or parity failure | R33 |
| BND-TEMPORAL-001 | temporal-retry | R4, R5, R6, R7, R8, R9, R10, R26, R27, R28, R29, R30, R31, R32 | first review, pending initialization, matching retry, already-active retry, stale identity, concurrent conflict, interruption | one semantic review per exact tuple and one settlement transition | idempotent reuse, exact activation, fresh review requirement, or stop | R7 |
| BND-RECOVERY-001 | failure-recovery | R10, R13, R24, R25, R29, R30, R32, R35, R36, R44, R45, R49, R50, R52, R53, R54, R55 | blocked recording, missing resource, invalid vocabulary, ambiguity, interrupted write, unsafe reduction, architecture ambiguity | failure never invents judgment, authority, procedure, or semantic deletion | explicit blocker, owner route, reconciliation, or rollback | R36 |
| BND-COMPAT-001 | compatibility-migration | R18, R19, R31, R40, R47, R48, R49, R50, R51, R52, R53, R54, R55 | retained/moved/duplicate/obsolete rules; normative/parser/incidental/obsolete/historical literals; old/current packages | statuses, finding fields, boundary identities, and basis evidence remain compatible | preserved package, atomic consumer migration, or complete rollback | R54 |
| BND-ENV-001 | external-environment | R36, R51, R53, R54 | canonical, generated, packed, archived, installed trees; target runtime present or absent | acceptance is deterministic and filesystem/package based | parity proof or package-integrity failure | R53 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R4, R5, R7, R11, R12, R13, R14, R15 | BND-INPUT-001, BND-AUTH-001 | candidate loading or absent initialization could be mistaken for transaction authority | load the governed reference, validate exact authority, then select initial or retry sub-result without mutation by inference |
| INT-002 | R7, R8, R21, R26 | BND-STATE-001, BND-TEMPORAL-001 | repeated invocation while initialization is pending could duplicate clean review | reuse one exact clean judgment and return initialization-required with no new evidence |
| INT-003 | R27, R28, R30, R31, R32 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | settlement retry or interruption could duplicate mutation or delete traceability | compare-and-set at most once, retain basis evidence, and reconcile exact active state idempotently |
| INT-004 | R29, R42, R43, R44, R45 | BND-STATE-001, BND-COMPOSE-001, BND-RECOVERY-001 | invalid retry could manufacture a blocked semantic verdict | report blocked transaction while omitting semantic judgment unless exact reuse is safe |
| INT-005 | R33, R34, R35, R36, R38, R39, R40, R41 | BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001 | conditional procedure could override universal judgment or be reconstructed when missing | enforce non-overlapping ownership and stop dependent work on required-resource failure |
| INT-006 | R48, R49, R50, R51, R52, R53 | BND-RECOVERY-001, BND-COMPAT-001 | size targets or incidental tests could remove governing behavior | closed ledgers, profile reduction, static scenarios, and semantic review block unsafe simplification |
| INT-007 | R47, R54 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | a generated or installed package could omit or alter new resources | package-chain inventory and byte parity fail before release or dependent use |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R2, R20, R33, R34 | BND-COMPOSE-001 | - | - |
| E2 | illustration | R11, R12, R13, R14 | BND-AUTH-001, BND-RECOVERY-001 | - | - |
| E3 | illustration | R5, R6, R21 | BND-STATE-001, BND-TEMPORAL-001 | - | - |
| E4 | illustration | R7, R8, R26 | BND-STATE-001, BND-TEMPORAL-001 | - | - |
| E5 | illustration | R27, R30, R31 | BND-STATE-001, BND-AUTH-001 | - | - |
| E6 | illustration | R28, R32 | BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |
| E7 | illustration | R10, R29, R43, R44 | BND-STATE-001, BND-RECOVERY-001 | - | - |
| E8 | illustration | R22, R23, R24, R25 | BND-STATE-001 | - | - |
| E9 | illustration | R35, R36 | BND-COMPOSE-001, BND-RECOVERY-001 | - | - |
| E10 | illustration | R48, R49, R50, R51, R52, R53 | BND-RECOVERY-001, BND-COMPAT-001 | - | - |

## Inputs and outputs

Inputs are the exact plan and revision, project instructions, accepted proposal, approved specification, relevant architecture evidence, current change record and plan entry when governed, current authoring and review evidence, plan-owned initialization basis when present, boundary evidence when applicable, and workflow authorization when managed.

Outputs use the result asset and one finding asset per material finding. Every formal invocation reports its operation, transaction result, blockers, action or handoff, claim limits, recording state, and applicable judgment, governed, boundary, or workflow-managed evidence.

## State and invariants

- Exactly one semantic review may be current for an exact plan tuple.
- Initialization is plan-owned and occurs only after a clean review; plan-review never initializes or mutates `planned_work`.
- Settlement retry is judgment reuse, not semantic rereview.
- Only one exact matching plan entry may move from `review-required` to `active`.
- Basis evidence remains durable after settlement.
- Workflow owns routing and continuation; plan-review returns control after its owned recording and settlement.
- Resource availability and output structure never grant authority.

## Error and boundary behavior

Unknown closed-vocabulary values fail before consistency checks. Missing or ambiguous identity, stale plan revision, conflicting review identity, duplicate bases, open resolution, invalid initialization, blocked recording, unavailable required resource, illegal transition, and mixed package versions all fail closed with the smallest exact blocker. A failure never silently falls back from governed to portable operation and never invents a semantic judgment.

## Compatibility and migration

The change preserves review statuses, transaction meanings, finding fields, review dimensions, boundary identifiers, lifecycle ownership, plan-entry states, and recording artifacts. It introduces package resources but no new persistent schema or lifecycle state. Exact parser and contract literals migrate atomically when necessary; incidental assertions are updated instead of becoming prose owners.

Canonical resources and directly coupled validation, fixtures, package inventories, and generated archives roll out together. Rollback restores the prior complete package and consumers, regenerates derived output, and validates parity. Historical review records and plan artifacts remain unchanged.

## Observability

Change-local evidence records semantic rule disposition, literal compatibility, duplicate ownership, before-and-after profile words and bytes, static scenario results, package inventory and byte parity, and independent semantic review. Every durable review and transition cites stable identities and exact paths. Target-agent transcripts and runtime execution are not acceptance evidence.

## Security and privacy

The simplification introduces no credentials, network access, secret handling, or user-data processing. Acceptance must remain local and deterministic. Existing authority checks, external-action limits, and safe recording boundaries remain unchanged.

## Accessibility and UX

Not applicable to a user interface. Published Markdown remains user-facing and must preserve readable semantic source lines, scannable headings, stable identifiers, and concise output groups.

## Performance expectations

Portable and governed procedural profiles must each use fewer loaded words and UTF-8 bytes than their current equivalents. No fixed percentage is required. Validation runtime must not be expanded by target-agent execution, transcript grading, or a new tokenizer dependency.

## Edge cases

EC1. A candidate is discovered only after portable classification begins; dependent work waits for governed loading and validation.

EC2. A clean review exists but initialization is absent; retry returns `initialization-required` without rereview.

EC3. Initialization exists without a current clean review; the transaction blocks as contradictory.

EC4. The plan changes after clean review; the prior judgment is stale and a fresh initial review is required.

EC5. Two clean reviews or two initialization bases match; ambiguity blocks.

EC6. The entry is already active with exact matching identities; retry succeeds idempotently without writes.

EC7. Recording fails after judgment but before settlement; formal completion and settlement are withheld.

EC8. Compare-and-set completes but result reporting is interrupted; retry reconciles exact active state without duplicate evidence.

EC9. A required reference is missing while its trigger is true; dependent work stops without memory reconstruction.

EC10. An applicable output group has unavailable data; it reports blocked or unknown with the exact blocker rather than an empty placeholder.

EC11. A new literal appears in validation; unknown classification fails before disposition consistency checks.

EC12. `SKILL.md` shrinks while the governed loaded profile grows; acceptance fails absent an explained, preservation-required reason and lower final governed profile.

## Non-goals

- Changing plan-quality criteria, review status values, lifecycle stages, `planned_work` ownership, workflow routing, or implementation authorization.
- Optimizing adjacent skills or redesigning reviewed-plan initialization.
- Adding a generic review engine, state store, scheduler, selector, target-agent journey, transcript grader, tokenizer dependency, or permanent size gate.
- Rewriting historical plan or review evidence.
- Adding more than one new procedural reference or more than the two review-family structural assets.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | The canonical package contains exactly the selected main file, two references, and two assets with valid resource mapping. |
| AC2 | Portable review performs complete plan judgment and recording without the governed reference. |
| AC3 | Candidate loading and validated governed authority remain distinct and invalid candidates fail closed. |
| AC4 | An exact clean review prevents duplicate semantic review while initialization is pending. |
| AC5 | Every valid and invalid initial-review and settlement-retry state has one deterministic result and write set. |
| AC6 | Already-active exact settlement is idempotent and creates no duplicate evidence. |
| AC7 | Invalid retries do not manufacture a semantic review status. |
| AC8 | Settlement retains authoring, review, and initialization evidence and performs at most one entry transition. |
| AC9 | Result and finding assets remain structural owners and never determine policy. |
| AC10 | Required-resource failure stops dependent behavior without reconstruction; untriggered resources do not load. |
| AC11 | Every significant rule and literal has one closed, validated disposition. |
| AC12 | Portable and governed loaded words and bytes both decrease, and total package change is reported honestly. |
| AC13 | Static scenarios directly prove each applicable boundary and selected interaction without a Cartesian test inventory. |
| AC14 | Existing package validation proves canonical, generated, packed, archived, and installed parity. |
| AC15 | No target-agent runtime, prompt journey, transcript grader, tokenizer dependency, or permanent simplicity validator is introduced. |
| AC16 | Independent semantic review approves the final skill package and lifecycle behavior. |

## Open questions

None.

## Next artifacts

- Formal `spec-review`.
- Bounded architecture assessment.
- Execution plan and `plan-review`.
- Test specification and `test-spec-review`.

## Follow-on artifacts

None yet

## Readiness

Ready for formal `spec-review`. This specification does not claim review approval, architecture completion, planning completion, implementation readiness, verification, branch readiness, or PR readiness.
