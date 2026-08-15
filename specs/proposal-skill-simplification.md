<!-- Template: spec-skeleton-v1 --><!-- Skill: spec --><!-- Template status: normative --><!-- Maintained alongside: skills/spec/SKILL.md --><!-- Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Proposal Skill Simplification

## Owning change record

`docs/changes/2026-08-14-proposal-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Proposal Skill Simplification](../docs/proposals/2026-08-14-proposal-skill-simplification.md)
- Approved [proposal-review R4](../docs/changes/2026-08-14-proposal-skill-simplification/reviews/proposal-review-r4.md)

## Goal and context

This specification defines a shorter published `proposal` skill package without weakening proposal decision quality, intent preservation, standing-artifact gates, lifecycle authority, transaction recovery, structural output, package integrity, or proposal-review handoff.

The universal skill remains sufficient for portable proposal judgment. One conditional reference owns governed authoring and recovery procedure, one independently triggered reference owns strategic and broad-scope gates, and the existing skeleton is the sole structural owner. The contract measures actual loaded assemblies separately from total package size and excludes target-agent acceptance and an additional manual semantic-review gate.

## Glossary

- `portable operation`: proposal creation or revision resolved from one exact artifact path and file state without requiring a lifecycle entry.
- `governed candidate`: evidence pointing to exactly one current governed change; it selects the governed reference but grants no mutation authority.
- `governed authority`: validated permission from the complete change record, lifecycle marker, exact proposal identity or deterministic intended identity, settled prerequisites, and legal authoring state.
- `specialized predicate`: one of `vision_exception_context`, `standing_artifact_context`, `initial_intent_table_context`, or `scope_budget_context`.
- `authoring-reset-required`: a non-persistent transaction result indicating that a stale incomplete governed proposal attempt cannot resume or be replaced without workflow authorization and proposal-owned reset execution.
- `reset authorization`: current workflow-owned evidence binding one stale transaction and the exact proposal-owned surfaces that may be reset.
- `structural asset`: a copy-and-fill resource that owns labels, section order, tables, and placeholders but no semantic or lifecycle policy.

## Examples first

### Example E1: ordinary portable creation loads the common path

Given no governed candidate and no specialized predicate, when a user creates a proposal at an absent exact path, then the skill loads `SKILL.md` and the skeleton, creates only the proposal artifact, and writes no lifecycle state.

### Example E2: portable revision needs no proposal entry

Given an exact portable proposal file exists without an owning change entry, when the user explicitly requests revision, then the skill may revise that artifact without creating or mutating `change.yaml`.

### Example E3: governed candidate loading does not grant authority

Given a structured owning-change pointer selects the governed reference, when the complete change record does not provide legal proposal-authoring authority, then the skill stops before content or lifecycle mutation and does not fall back to portable authoring.

### Example E4: governed creation is recoverable

Given one governed change authorizes a new primary proposal, when authoring starts, then the skill creates only the matching `authoring` entry, writes and validates the proposal and evidence, and commits by moving that entry to `review-required`.

### Example E5: identical retry resumes once

Given an interrupted governed operation has the same change, artifact, path, inputs, prior identity when applicable, and evidence identity, when retried, then it resumes or completes the exact transaction without duplicate entries, evidence, or transitions.

### Example E6: stale recovery preserves stage ownership

Given an incomplete governed proposal attempt has a changed basis, when workflow proves no review or downstream reliance and records exact current reset authorization, then proposal resets only its authorized incomplete entry and proposal-authored evidence while workflow does not mutate those surfaces.

### Example E7: changed recovery evidence stops

Given reset authorization was valid but the proposal identity, reliance state, or competing-write state changes before consumption, when proposal validates the authorization, then it stops without mutation and returns to workflow for a new decision.

### Example E8: strategic groups compose independently

Given vision exception, standing-artifact, initial-intent, and scope-budget predicates are all true, when the proposal is authored, then the gates reference loads once and the skeleton includes all four applicable groups without one suppressing another.

### Example E9: applicable unresolved group remains visible

Given one specialized predicate is true but required data is unavailable, when output is composed, then the applicable group reports an explicit blocker rather than being omitted or left with placeholders.

### Example E10: missing conditional procedure fails safely

Given a governed or specialized trigger is true and its required reference is missing, unreadable, contradictory, escaped, or mixed-version, when authoring begins, then the skill stops before dependent judgment or mutation and does not reconstruct the procedure from memory.

### Example E11: downstream reliance blocks ordinary revision

Given an accepted proposal identity is already used by a spec, architecture record, plan, or implementation, when ordinary governed revision is requested, then the skill stops until workflow completes impact handling and grants explicit reopen authority.

### Example E12: simplification reports context honestly

Given the package is revised, when measurements are recorded, then every real loaded assembly, each resource, representative copied output, and total package size are reported separately and relocated content is not described as deleted.

## Requirements

### Package and universal contract

R1. The canonical package MUST contain `skills/proposal/SKILL.md`, `references/governed-proposal-authoring.md`, `references/strategic-and-scope-gates.md`, and `assets/proposal-skeleton.md`.

R2. `SKILL.md` MUST remain self-sufficient for purpose, evidence precedence, problem and option quality, recommendation rationale, ordinary vision fit, universal intent preservation, risks, stops, claims, portable isolation, handoff, and every resource trigger.

R3. `SKILL.md` MUST map both references with `READ` and the skeleton with `COPY`, using repository-valid relative paths and exact activation conditions.

R4. Missing, unreadable, escaped, contradictory, or mixed-version required resources MUST stop dependent judgment or mutation before any fallback reconstruction.

R5. The governed reference MUST own only governed proposal authority validation, creation, revision, retry, authorized stale-attempt reset, concurrency, evidence, and legal authoring transitions.

R6. The strategic reference MUST own only vision-exception, standing-artifact bootstrap, detailed intent classification, scope-budget classification, and follow-up-routing procedure.

R7. Neither reference MUST override universal rules, grant authority owned by another stage, or duplicate the other reference's governing procedure.

### Invocation and operation classification

R8. The loaded assemblies MUST be exactly `PA0-portable`, `PA0G-portable-gated`, `PA1-governed`, and `PA1G-governed-gated`.

R9. `governed_proposal_candidate_context` MUST select the governed reference only from one explicit change ID, one workflow-managed exact current change, or one valid structured owning-change pointer.

R10. Conversational references to a workflow, lifecycle, or change MUST NOT establish a governed candidate or mutation authority.

R11. After loading, the governed reference MUST validate the complete change, lifecycle marker, exact proposal entry or deterministic intended identity, normalized path, settled prerequisites, governing inputs, and legal authoring state before mutation.

R12. A failed governed-authority validation MUST stop and MUST NOT fall back to portable creation or revision.

R13. The supported artifact operations MUST be exactly `create-primary-proposal` and `revise-primary-proposal`; `authoring-reset-required` is a transaction result, not another authoring operation or lifecycle state.

R14. Portable creation MUST require an absent exact target, portable revision MUST require an existing exact target, and ambiguous, conflicting, or unresolved targets MUST stop.

R15. Portable authoring MUST write only the proposal artifact and MUST NOT create or mutate lifecycle, review, automation, or routing state.

### Governed creation, revision, and retry

R16. Governed creation MUST bind the change ID, artifact ID, normalized intended path, governing input identities, and authoring-evidence path before writing.

R17. Governed creation MUST prove that the target entry and file are absent and no competing primary proposal exists before creating only the matching entry in `authoring`.

R18. Governed creation MUST validate the proposal, compute and record its content identity in complete authoring evidence, and use the matching transition to `review-required` as its commit point.

R19. Governed revision MUST bind every creation identity plus the prior proposal identity and exact reopen, finding, upstream-change, or legal revision authority.

R20. Governed revision MUST preserve historical authoring and review records, clear only the matching current review mapping when authorized, produce a new identity, return only the matching entry to `review-required`, and require fresh proposal review.

R21. A governed accepted or otherwise settled proposal with downstream reliance MUST NOT be revised until workflow completes impact and staleness handling and grants a legal reopen state.

R22. An identical interrupted creation or revision MUST resume from the first incomplete step and an identical completed retry MUST be idempotent.

R23. Mismatched basis, unrelated file or entry asymmetry, different path, stale authority, ambiguous attempts, multiple primary candidates, or concurrent competing writes MUST stop without adoption or overwrite.

### Stale-attempt authorization and reset

R24. An incomplete attempt whose path, governing inputs, prior identity, or authorization basis changes MUST return `authoring-reset-required` and MUST NOT start another transaction.

R25. Workflow MUST own stale-attempt identity validation, no-review and no-downstream-reliance proof, reset authorization, and recovery routing while preserving proposal-owned entry and evidence state.

R26. Workflow reset authorization MUST identify the change, artifact, stale transaction, normalized path, proposal-authoring evidence, allowed reset surfaces, and current authorization identity.

R27. Reset authorization MUST be current, identity-bound, invalidated by relevant identity, reliance, or competing-write changes, and single-use or idempotently consumable.

R28. Proposal MUST validate current exact workflow authorization before resetting only its own matching incomplete `authoring` entry and incomplete proposal-authored evidence.

R29. Proposal reset MUST preserve every review record, completed authoring record, other artifact entry, workflow field, automation record, and downstream artifact.

R30. An exact already-completed reset MUST return idempotent success; stale, mismatched, ambiguous, relied-upon, or competing state MUST stop without mutation.

R31. A new proposal operation MUST begin only after reset completion validates and MUST receive a new transaction identity, evidence path, and current governing basis.

R32. The recovery handshake MUST NOT add a lifecycle state, persistence mechanism, evidence type, or write owner; a design requiring workflow to mutate proposal-owned state MUST route to architecture and workflow-contract revision.

### Strategic predicates and structural output

R33. The specialized predicate vocabulary MUST be exactly `vision_exception_context`, `standing_artifact_context`, `initial_intent_table_context`, and `scope_budget_context`.

R34. Predicate truth MUST remain proposal judgment; deterministic validation MAY validate closed names and result shape but MUST NOT infer semantic truth from proposal prose.

R35. Every true specialized predicate MUST apply independently and the strategic reference MUST load exactly once for any non-empty predicate set.

R36. Late predicate discovery MUST complete before dependent drafting or readiness selection, and unresolved applicability that can affect safe output MUST stop.

R37. `scope_budget_context` MUST include multiple independent work items, multiple lifecycle families, multiple plausible downstream specs or plans, workflow or release or validation policy, generated output or public skill behavior, and current review concern about silent narrowing, hidden follow-up, or multi-workstream ambiguity.

R38. The skeleton MUST contain the universal proposal structure plus independently composable `Vision exception or revision`, `Standing artifact dependency or bootstrap`, `Initial intent preservation`, and `Scope budget` groups.

R39. The skeleton MUST own only labels, ordering, table shapes, and placeholders; `SKILL.md` and applicable references MUST own semantics, applicability, authority, readiness, and handoff.

R40. Inapplicable groups MUST be omitted, applicable resolved groups MUST be complete, applicable unresolved groups MUST report explicit blockers, and no emitted proposal MUST contain unfilled placeholders.

### Preservation, measurement, and acceptance

R41. Every behaviorally significant current rule or duplicate cluster MUST receive exactly one disposition and destination in a change-local semantic-rule ledger.

R42. Every exact heading, label, path, enum, or phrase consumed by contracts, parsers, packages, fixtures, or tests MUST receive one separate literal-compatibility classification and disposition.

R43. Normative literals MUST remain exact unless their governing contract changes, parser or package contracts MUST migrate atomically with every consumer, and incidental tests MUST NOT freeze accidental prose.

R44. Every new or changed closed vocabulary MUST fail explicitly on unknown values before consistency checks and MUST have an unknown-value regression test.

R45. Measurements MUST use canonical authored files, LF normalization, each unique loaded procedure once in documented order, UTF-8 bytes, and Unicode whitespace-separated words.

R46. Measurements MUST report all four loaded assemblies, `SKILL.md`, each reference, the skeleton, representative copied output, and total package size separately.

R47. Every real loaded assembly MUST decrease from baseline or receive one specific independently reviewed semantic-preservation exception; no fixed percentage may override preservation.

R48. Canonical, generated, packed, archived, release-candidate, and installed resources MUST retain required relative-path inventory and raw-byte parity.

R49. Acceptance MUST use deterministic contract and package proof plus ordinary proposal review, code review, and human PR review; it MUST NOT execute Codex, Claude Code, opencode, or another target-agent runtime or add another manual semantic-review stage.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R8, R9, R10, R11, R12, R13, R14, R15, R33, R34, R35, R36, R37 | BND-INPUT-001, BND-INPUT-002 | - |
| state-lifecycle | applicable | R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-STATE-001, BND-STATE-002 | - |
| identity-authority | applicable | R9, R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-AUTH-001, BND-AUTH-002 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R6, R7, R33, R34, R35, R36, R37, R38, R39, R40 | BND-COMPOSE-001, BND-COMPOSE-002 | - |
| temporal-retry | applicable | R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R4, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-RECOVERY-001, BND-RECOVERY-002 | - |
| compatibility-migration | applicable | R41, R42, R43, R44, R45, R46, R47, R48 | BND-COMPAT-001 | - |
| external-environment | applicable | R4, R48, R49 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R8, R9, R10, R11, R12, R13, R14, R15, R33, R34, R35, R36, R37 | portable or governed candidate; create or revise; exact or ambiguous target | loading and operation do not grant authority | valid classification proceeds; unknown or ambiguous input stops | R8 |
| BND-INPUT-002 | input-domain | R8, R9, R10, R11, R12, R13, R14, R15, R33, R34, R35, R36, R37 | empty, single, multiple, late, or unresolved specialized predicate set | every true predicate applies once | empty uses core; non-empty loads gates once; unresolved material ambiguity stops | R33 |
| BND-STATE-001 | state-lifecycle | R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | absent, `authoring`, `review-required`, settled, stale, or conflicting entry and file state | only the exact proposal entry changes | legal create or revise commits at `review-required`; illegal state stops | R16 |
| BND-STATE-002 | state-lifecycle | R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | resumable partial, stale partial, authorized reset, completed reset, or relied-upon state | `authoring-reset-required` is not persisted state | identical retry resumes; authorized reset completes; unsafe state stops | R24 |
| BND-AUTH-001 | identity-authority | R9, R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | candidate evidence, full authority, missing authority, stale authority | candidate selection never grants writes | full authority permits bounded operation; every authority defect stops | R9 |
| BND-AUTH-002 | identity-authority | R9, R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | current exact authorization, stale authorization, mismatched authorization, or changed reliance | workflow authorizes and proposal writes only proposal-owned reset surfaces | exact authorization permits reset; every mismatch stops | R25 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R6, R7, R33, R34, R35, R36, R37, R38, R39, R40 | common path, governed reference, strategic reference, skeleton, missing or mixed resource | each rule and structure has one owner | valid assembly proceeds; missing or contradictory resource stops | R1 |
| BND-COMPOSE-002 | composition-path | R1, R2, R3, R4, R5, R6, R7, R33, R34, R35, R36, R37, R38, R39, R40 | core plus any valid combination of four conditional groups | asset owns structure only and predicates compose independently | applicable groups are complete; inapplicable groups are absent | R38 |
| BND-TEMPORAL-001 | temporal-retry | R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | first attempt, identical retry, completed retry, stale retry, concurrent attempt | retry identity never silently rebinds | identical work resumes or no-ops; stale or competing work stops | R22 |
| BND-RECOVERY-001 | failure-recovery | R4, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | interruption before or after partial writes; reset authorization and consumption | recovery cannot broaden stage write authority | exact recovery reconciles once; unsafe recovery stops without unrelated mutation | R24 |
| BND-RECOVERY-002 | failure-recovery | R4, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | required resource present, absent, unreadable, escaped, contradictory, or mixed | shortened common path never reconstructs conditional procedure | valid resource loads; every integrity defect stops dependent work | R4 |
| BND-COMPAT-001 | compatibility-migration | R41, R42, R43, R44, R45, R46, R47, R48 | normative, parser/package, incidental, historical, obsolete, canonical, or derived consumer | semantic and literal preservation remain separate | preserve or migrate true contracts atomically; retire incidental coupling | R41 |
| BND-ENV-001 | external-environment | R4, R48, R49 | canonical, generated, packed, archived, release-candidate, installed, and unavailable package surfaces | acceptance remains deterministic and repository-owned | parity passes or blocks; no target runtime or external mutation occurs | R48 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R9, R10, R11, R12, R13, R14, R15 | BND-INPUT-001, BND-AUTH-001 | a governed candidate or conversational wording is mistaken for mutation authority | reference selection occurs first, full authority validation occurs second, and failure never falls back to portable mutation |
| INT-002 | R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32 | BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-001, BND-RECOVERY-001 | stale partial authoring is silently rebound, reset by workflow, or reset without current no-reliance proof | workflow authorizes only; proposal validates and resets only exact proposal-owned partial state; changed evidence stops |
| INT-003 | R33, R34, R35, R36, R37, R38, R39, R40 | BND-INPUT-002, BND-COMPOSE-002 | one strategic predicate suppresses another or the skeleton becomes a policy owner | every true predicate composes independently and the asset remains structural only |
| INT-004 | R4, R41, R42, R43, R44, R45, R46, R47, R48, R49 | BND-COMPOSE-001, BND-RECOVERY-002, BND-COMPAT-001, BND-ENV-001 | simplification appears successful while dropping behavior or omitting a packaged reference | ledgers, loaded-profile measurements, deterministic fixtures, and full package parity all remain required |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R8, R14, R15 | BND-INPUT-001 | - | - |
| E2 | illustration | R14, R15 | BND-INPUT-001 | - | - |
| E3 | illustration | R9, R10, R11, R12 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E4 | illustration | R16, R17, R18 | BND-STATE-001, BND-AUTH-001 | - | - |
| E5 | illustration | R22, R23 | BND-TEMPORAL-001 | - | - |
| E6 | regression | R24, R25, R26, R27, R28, R29, R30, R31 | BND-STATE-002, BND-AUTH-002, BND-RECOVERY-001 | PRSIM-R3-PR1 | - |
| E7 | illustration | R27, R30 | BND-AUTH-002, BND-TEMPORAL-001 | - | - |
| E8 | illustration | R33, R34, R35, R36, R37 | BND-INPUT-002, BND-COMPOSE-002 | - | - |
| E9 | illustration | R36, R40 | BND-COMPOSE-002 | - | - |
| E10 | illustration | R4 | BND-COMPOSE-001, BND-RECOVERY-002 | - | - |
| E11 | illustration | R21 | BND-STATE-001, BND-AUTH-001 | - | - |
| E12 | illustration | R48 | BND-COMPAT-001, BND-ENV-001 | - | - |

## Inputs and outputs

Inputs are the accepted proposal and approved review, current `proposal` package, governing skill and workflow contracts, exact literal and validator consumers, package inventories, and one governed change record when lifecycle authoring applies.

Outputs are the simplified canonical skill, two references, revised skeleton, directly coupled contract fixtures and validator registrations, semantic-rule and literal-compatibility ledgers, deterministic profile measurements, package parity evidence, and stage-owned lifecycle evidence. Target-agent transcripts, runtime scores, external mutations, and another manual semantic-review artifact are not outputs.

## State and invariants

- `skills/` remains the only authored skill source.
- Portable authoring writes no lifecycle state.
- Governed authoring changes only its proposal artifact, proposal-owned entry, and proposal-authored evidence under exact authority.
- Workflow owns routing, no-reliance decisions, and reset authorization but never proposal-owned mutation.
- Proposal review remains the only proposal settlement owner.
- The skeleton remains structural and conditional references remain skill-owned procedure.
- Every completed authoring transaction ends at `review-required`.
- Automation never expands stage write authority.

## Error and boundary behavior

Every unknown closed-vocabulary value, ambiguous assembly, unresolved target, illegal state, missing authority, stale identity, unrelated collision, mismatched retry, changed reset authorization, downstream reliance, competing write, and required-resource defect fails closed with a concrete blocker. Failure before a permitted write leaves governed state unchanged. An interrupted permitted write may be reconciled only through its exact retry identity or the authorized stale-reset handshake.

## Compatibility and migration

Historical proposals and review evidence remain unchanged and readable. New or substantively revised proposals use the revised skeleton and conditional groups. Parser or package contracts migrate atomically with every consumer; incidental snapshots do not freeze prose. Canonical and every derived package layer adopt both references and the revised asset atomically. Rollback restores the prior skill and skeleton, removes both references and their registrations, and regenerates derived packages.

## Observability

The change is observable through canonical diffs, resource maps, rule and literal ledgers, static scenario results, validator output, loaded-profile and total-package reports, package parity evidence, review records, and lifecycle metadata. Reports distinguish configured commands from executed commands and relocated content from deleted content.

## Security and privacy

The change introduces no credentials, secrets, network operation, external persistence, or personal-data processing. Existing command and external-action boundaries remain mandatory. The automation and acceptance process must not push, publish, release, deploy, merge, perform destructive Git operations, or execute a target-agent runtime.

## Accessibility and UX

Not applicable to end-user interface accessibility. Published Markdown must remain readable: complete prose sentences stay intact, repeated mappings use tables, and copied structures contain no unfilled placeholders.

## Performance expectations

Every real loaded procedural assembly must use fewer LF-normalized UTF-8 bytes and Unicode whitespace-separated words than its baseline unless one specific independently reviewed semantic-preservation exception is recorded. Total package growth is reported separately and no runtime latency contract is introduced.

## Edge cases

EC1. A request mentions a change conversationally but supplies no exact structured identity: remain portable when portable authoring is otherwise valid.

EC2. An owning-change pointer resolves a missing or invalid record: load the governed reference and stop without portable fallback.

EC3. Portable create targets an existing file: stop and require explicit revision.

EC4. Governed creation is interrupted after entry creation but before file creation: an exact retry resumes.

EC5. Governed revision is interrupted after content write but before evidence completion: an exact retry validates and completes the same transaction.

EC6. A partial attempt's basis changes before retry: return `authoring-reset-required` and do not start another operation.

EC7. Workflow authorization matches but a review appears before reset: proposal stops without mutation.

EC8. Reset already completed for the exact authorization: return idempotent success.

EC9. A proposal is accepted and used downstream: ordinary revision stops until legal reopen and impact handling exist.

EC10. Two specialized predicates become true after drafting begins: load the strategic reference once and include both groups before readiness selection.

EC11. A specialized group is applicable but owner data is unavailable: include the group with an explicit blocker.

EC12. Total package size grows while all loaded profiles shrink: report and justify growth without failing solely on percentage.

EC13. A derived package omits one reference: parity fails even when canonical validation passes.

## Non-goals

- Changing proposal purpose, lifecycle stage order, proposal-review settlement, vision values, intent-treatment values, scope-budget values, or downstream claims.
- Allowing proposal to create a governed change root, approve itself, advance workflow, or mutate another stage's state.
- Allowing workflow to mutate proposal-owned entries or evidence.
- Adding a runtime engine, classifier, scheduler, state store, tokenizer dependency, permanent simplicity validator, or target-agent acceptance harness.
- Adding another proposal template, result asset, packaged script, or more than two references.
- Rewriting historical proposals solely to adopt the new package.
- Optimizing another skill in this change.
- Adding a separate manual semantic-review acceptance stage.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-PRSIM-001` | The package contains one universal skill, two independently triggered references, and one structural skeleton. |
| `AC-PRSIM-002` | Candidate, authority, operation, and specialized-predicate classifications are closed and evidence-based. |
| `AC-PRSIM-003` | Portable create and revise use exact file state without requiring or creating lifecycle entries. |
| `AC-PRSIM-004` | Governed create and revise use identity-bound entry-first transactions with deterministic commit and retry behavior. |
| `AC-PRSIM-005` | A failed governed candidate never falls back to portable authoring. |
| `AC-PRSIM-006` | Workflow authorizes stale recovery without mutating proposal-owned state. |
| `AC-PRSIM-007` | Proposal resets only the exact authorized incomplete proposal entry and evidence and preserves every unrelated surface. |
| `AC-PRSIM-008` | Reset authorization is current, identity-bound, invalidated by relevant changes, and single-use or idempotently consumable. |
| `AC-PRSIM-009` | Every stale-recovery state has one deterministic reset, idempotent, or stop result. |
| `AC-PRSIM-010` | Every specialized predicate has one independently composable structural destination. |
| `AC-PRSIM-011` | Assets own structure only, and emitted proposals omit inapplicable groups and contain no unfilled placeholders. |
| `AC-PRSIM-012` | Missing or contradictory required resources stop before dependent work without memory-based reconstruction. |
| `AC-PRSIM-013` | Semantic rules and literal dependencies have separate complete disposition ledgers. |
| `AC-PRSIM-014` | Every new or changed closed vocabulary rejects unknown values before consistency checks. |
| `AC-PRSIM-015` | Static fixtures cover every valid and invalid assembly, operation, transaction, recovery, predicate, resource, and write-authority outcome. |
| `AC-PRSIM-016` | Every real loaded assembly decreases or has one specific independently reviewed preservation exception, and total package size is reported separately. |
| `AC-PRSIM-017` | Canonical, generated, packed, archived, release-candidate, and installed resources retain required path and raw-byte parity. |
| `AC-PRSIM-018` | Acceptance executes no target-agent runtime and adds no separate manual semantic-review gate. |

## Open questions

None. Exact metadata field names, current literal consumers, fixture organization, and measurement-record shape are downstream design details constrained by the requirements above.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment with expected `architecture-not-required`.
- Execution plan and `plan-review`.
- Test specification and independent `test-spec-review`.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This authoring result does not claim spec approval, architecture completion, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
